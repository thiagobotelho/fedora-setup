from ..context import Context


def enable(ctx: Context) -> None:
    version = ctx.facts.version
    for channel in ("free", "nonfree"):
        url = (
            f"https://mirrors.rpmfusion.org/{channel}/fedora/"
            f"rpmfusion-{channel}-release-{version}.noarch.rpm"
        )
        ctx.runner.run(["dnf", "install", "-y", url], sudo=True)

    enabled = ctx.runner.run(
        ["dnf", "repolist", "--enabled"],
        capture=True,
        check=False,
    ).stdout
    for channel in ("free", "nonfree"):
        if f"rpmfusion-{channel}-rawhide" not in enabled:
            continue
        print(f"⚠️ RPM Fusion {channel} Rawhide detectado; corrigindo para repositórios estáveis.")
        for option in (
            f"rpmfusion-{channel}.enabled=1",
            f"rpmfusion-{channel}-updates.enabled=1",
            f"rpmfusion-{channel}-rawhide.enabled=0",
        ):
            ctx.runner.run(["dnf", "config-manager", "setopt", option], sudo=True)
