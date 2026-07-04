from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


SUPPORTED = {"fedora", "ubuntu", "debian"}


def _os_release() -> dict[str, str]:
    values = {}
    for line in Path("/etc/os-release").read_text().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value.strip().strip('"')
    return values


def _output(args: list[str]) -> str:
    try:
        return subprocess.check_output(args, text=True, stderr=subprocess.DEVNULL)
    except (OSError, subprocess.CalledProcessError):
        return ""


def _read_text(path: Path) -> str:
    try:
        return path.read_text().strip()
    except OSError:
        return ""


def _edid_model(data: bytes) -> str:
    if len(data) < 128:
        return ""
    for offset in range(54, 126, 18):
        descriptor = data[offset:offset + 18]
        if descriptor[:5] == b"\x00\x00\x00\xfc\x00":
            return descriptor[5:18].decode("ascii", errors="ignore").strip("\x00\n ")
    return ""


def _monitor_models() -> tuple[str, ...]:
    models = []
    for path in Path("/sys/class/drm").glob("*/edid"):
        try:
            model = _edid_model(path.read_bytes())
        except OSError:
            continue
        if model:
            models.append(model)
    return tuple(sorted(set(models)))


def _secure_boot_from_efivarfs() -> str:
    for path in Path("/sys/firmware/efi/efivars").glob("SecureBoot-*"):
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if len(data) >= 5:
            return "enabled" if data[4] == 1 else "disabled"
    return "unknown"


@dataclass(frozen=True)
class Facts:
    distro: str
    version: str
    codename: str
    pretty_name: str
    computer_vendor: str
    computer_model: str
    architecture: str
    wsl: bool
    memory_gib: float
    nvidia: bool
    nvidia_devices: tuple[str, ...]
    hyperx: bool
    hyperx_usb_ids: tuple[str, ...]
    monitor_models: tuple[str, ...]
    dell_hardware: bool
    desktop: bool
    secure_boot: str

    @property
    def package_manager(self) -> str:
        return "dnf" if self.distro == "fedora" else "apt"

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)


def detect() -> Facts:
    release = _os_release()
    distro = release.get("ID", "").lower()
    if distro not in SUPPORTED:
        raise RuntimeError(f"Distribuição não suportada: {distro or 'desconhecida'}")

    kernel = platform.release().lower()
    wsl = "microsoft" in kernel or bool(os.environ.get("WSL_DISTRO_NAME"))
    memory_kib = 0
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemTotal:"):
            memory_kib = int(line.split()[1])
            break

    pci = _output(["lspci", "-nn"])
    nvidia_lines = tuple(line.strip() for line in pci.splitlines() if "nvidia" in line.lower())
    if not nvidia_lines:
        detected_nvidia = []
        for path in Path("/sys/bus/pci/devices").glob("*/vendor"):
            try:
                if path.read_text().strip().lower() == "0x10de":
                    detected_nvidia.append(str(path.parent))
            except OSError:
                continue
        nvidia_lines = tuple(detected_nvidia)
    usb = _output(["lsusb"])
    hyperx_ids = list(
        match.lower()
        for match in re.findall(r"\b0951:[0-9a-fA-F]{4}\b", usb)
    )
    if not hyperx_ids:
        for vendor in Path("/sys/bus/usb/devices").glob("*/idVendor"):
            try:
                if vendor.read_text().strip().lower() == "0951":
                    product = vendor.with_name("idProduct")
                    if product.exists():
                        hyperx_ids.append(f"0951:{product.read_text().strip().lower()}")
            except OSError:
                continue

    secure_boot = _secure_boot_from_efivarfs()
    if shutil.which("mokutil"):
        output = _output(["mokutil", "--sb-state"]).lower()
        if "enabled" in output:
            secure_boot = "enabled"
        elif "disabled" in output:
            secure_boot = "disabled"

    computer_vendor = _read_text(Path("/sys/class/dmi/id/sys_vendor"))
    computer_model = (
        _read_text(Path("/sys/class/dmi/id/product_name"))
        or _read_text(Path("/sys/class/dmi/id/product_version"))
    )
    monitors = _monitor_models()
    return Facts(
        distro=distro,
        version=release.get("VERSION_ID", ""),
        codename=release.get("UBUNTU_CODENAME") or release.get("VERSION_CODENAME", ""),
        pretty_name=release.get("PRETTY_NAME", distro),
        computer_vendor=computer_vendor,
        computer_model=computer_model,
        architecture=platform.machine(),
        wsl=wsl,
        memory_gib=round(memory_kib / 1024 / 1024, 1),
        nvidia=bool(nvidia_lines),
        nvidia_devices=nvidia_lines,
        hyperx=bool(hyperx_ids),
        hyperx_usb_ids=tuple(sorted(set(hyperx_ids))),
        monitor_models=monitors,
        dell_hardware=(
            "dell" in computer_vendor.lower()
            or any("dell" in model.lower() for model in monitors)
        ),
        desktop=bool(os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION")),
        secure_boot=secure_boot,
    )
