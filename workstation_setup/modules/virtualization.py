from ..catalog import VIRTUALIZATION
from ..context import Context


def install(ctx: Context, *, force: bool = False, **_: object) -> None:
    if ctx.facts.wsl:
        print("🪟 WSL detectado: virtualização de host ignorada")
        return
    if ctx.facts.memory_gib < 12 and not force:
        print(f"⚠️ Virtualização ignorada: apenas {ctx.facts.memory_gib} GiB de RAM (use --force-hardware)")
        return
    print("🧱 Módulo KVM/libvirt")
    ctx.packages(
        fedora=VIRTUALIZATION["fedora"],
        ubuntu=VIRTUALIZATION["ubuntu"],
        debian=VIRTUALIZATION["debian"],
    )
    user = ctx.home.name
    for group in ("libvirt", "kvm"):
        ctx.runner.run(["usermod", "-aG", group, user], sudo=True)
    ctx.runner.run(["systemctl", "enable", "--now", "libvirtd"], sudo=True, check=False)
