from pathlib import Path

from ..context import Context
from .rpmfusion import enable as enable_rpm_fusion


def install(ctx: Context, *, force: bool = False, **_: object) -> None:
    if ctx.facts.wsl:
        print("🪟 WSL detectado: driver NVIDIA pertence ao host Windows")
        return
    if not ctx.facts.nvidia and not force:
        print("ℹ️ NVIDIA não detectada; módulo ignorado")
        return

    print("🎮 Módulo NVIDIA")
    if ctx.facts.distro == "fedora":
        enable_rpm_fusion(ctx)
        if ctx.facts.secure_boot == "enabled":
            ctx.runner.run(
                ["dnf", "install", "-y", "kmodtool", "akmods", "mokutil", "openssl"],
                sudo=True,
            )
            if not Path("/etc/pki/akmods/certs/public_key.der").exists():
                ctx.runner.run(["kmodgenca", "-a"], sudo=True, check=False)
            print(
                "⚠️ Secure Boot: antes do reboot, execute "
                "`sudo mokutil --import /etc/pki/akmods/certs/public_key.der` "
                "e conclua Enroll MOK na próxima inicialização."
            )
        ctx.runner.run(
            [
                "dnf", "install", "-y", "akmod-nvidia",
                "xorg-x11-drv-nvidia-cuda", "switcheroo-control",
            ],
            sudo=True,
        )
        ctx.runner.run(["akmods", "--force"], sudo=True)
        ctx.runner.run(["modinfo", "-F", "version", "nvidia"], check=False)
        ctx.runner.run(
            ["systemctl", "enable", "--now", "switcheroo-control.service"],
            sudo=True,
            check=False,
        )
    else:
        ctx.runner.run(
            [
                "apt-get", "install", "-y", "ubuntu-drivers-common",
                "nvidia-prime", "switcheroo-control",
            ],
            sudo=True,
        )
        ctx.runner.run(["ubuntu-drivers", "install"], sudo=True)
        ctx.runner.run(
            ["systemctl", "enable", "--now", "switcheroo-control.service"],
            sudo=True,
            check=False,
        )

    print(f"ℹ️ Secure Boot: {ctx.facts.secure_boot}. Reinicie após concluir.")
    if ctx.facts.secure_boot == "enabled":
        print("⚠️ Confirme que a chave do módulo foi registrada antes de diagnosticar falha do driver.")
    print("ℹ️ Após reiniciar, valide: nvidia-smi e switcherooctl list")
