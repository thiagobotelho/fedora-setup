from __future__ import annotations

from ..context import Context


PACKAGES = {
    "fedora": [
        "ddcutil", "i2c-tools", "fwupd", "bolt", "thermald",
        "switcheroo-control", "power-profiles-daemon",
    ],
    "ubuntu": [
        "ddcutil", "i2c-tools", "fwupd", "bolt", "thermald",
        "switcheroo-control", "power-profiles-daemon",
    ],
    "debian": [
        "ddcutil", "i2c-tools", "fwupd", "bolt", "thermald",
        "switcheroo-control", "power-profiles-daemon",
    ],
}


def install(
    ctx: Context,
    *,
    force: bool = False,
    **_: object,
) -> None:
    if ctx.facts.wsl:
        print("🪟 WSL detectado: monitor/firmware devem ser gerenciados pelo host Windows")
        return

    if not ctx.facts.dell_hardware and not force:
        print("ℹ️ Hardware Dell não detectado; módulo ignorado")
        return

    print("🖥️ Módulo de hardware Dell/DDC-CI")
    ctx.packages(
        fedora=PACKAGES["fedora"],
        ubuntu=PACKAGES["ubuntu"],
        debian=PACKAGES["debian"],
    )

    ctx.runner.run(["modprobe", "i2c-dev"], sudo=True)
    ctx.runner.run(
        ["tee", "/etc/modules-load.d/ddcutil.conf"],
        sudo=True,
        input_text="i2c-dev\n",
    )
    ctx.runner.run(
        ["tee", "/etc/udev/rules.d/60-ddcutil-i2c.rules"],
        sudo=True,
        input_text='KERNEL=="i2c-[0-9]*", GROUP="i2c", MODE="0660"\n',
    )
    user = ctx.home.name
    ctx.runner.run(["groupadd", "--force", "i2c"], sudo=True)
    ctx.runner.run(["usermod", "-aG", "i2c", user], sudo=True)
    ctx.runner.run(["udevadm", "control", "--reload-rules"], sudo=True)
    ctx.runner.run(["udevadm", "trigger", "--subsystem-match=i2c-dev"], sudo=True)

    helper = ctx.root / "assets/bin/dell-monitor"
    destination = ctx.home / ".local/bin/dell-monitor"
    ctx.runner.run(["install", "-Dm0755", helper, destination])

    for service in ("fwupd-refresh.timer", "bolt.service", "switcheroo-control.service"):
        ctx.runner.run(["systemctl", "enable", "--now", service], sudo=True, check=False)
    ctx.runner.run(["fwupdmgr", "refresh", "--force"], check=False)
    ctx.runner.run(["fwupdmgr", "get-updates"], check=False)

    print("ℹ️ Ative DDC/CI no OSD do monitor antes de usar o helper.")
    print("ℹ️ Após logout/login: dell-monitor detect; dell-monitor capabilities")
