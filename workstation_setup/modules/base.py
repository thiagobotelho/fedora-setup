from ..catalog import BASE
from ..context import Context


def install(ctx: Context, *, upgrade: bool = False, **_: object) -> None:
    print("📦 Módulo base")
    if ctx.facts.package_manager == "dnf":
        if upgrade:
            ctx.runner.run(["dnf", "upgrade", "--refresh", "-y"], sudo=True)
    else:
        ctx.ensure_apt_index()
        if upgrade:
            ctx.runner.run(["apt-get", "dist-upgrade", "-y"], sudo=True)
    ctx.packages(
        fedora=BASE["fedora"],
        ubuntu=BASE["ubuntu"],
        debian=BASE["debian"],
    )
    if ctx.facts.distro == "ubuntu":
        ctx.runner.run(["add-apt-repository", "-y", "universe"], sudo=True)
        ctx.runner.run(["apt-get", "update"], sudo=True)
    ctx.runner.run(["git", "lfs", "install"])
