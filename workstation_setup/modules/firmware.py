from ..context import Context


def install(ctx: Context, **_: object) -> None:
    if ctx.facts.wsl:
        print("🪟 WSL detectado: firmware pertence ao host Windows")
        return
    print("🔋 Módulo firmware/LVFS")
    ctx.packages(fedora=["fwupd"], ubuntu=["fwupd"], debian=["fwupd"])
    ctx.runner.run(
        ["systemctl", "enable", "--now", "fwupd-refresh.timer"],
        sudo=True,
        check=False,
    )
    ctx.runner.run(["fwupdmgr", "refresh", "--force"], check=False)
    ctx.runner.run(["fwupdmgr", "get-devices"], check=False)
    ctx.runner.run(["fwupdmgr", "get-updates"], check=False)
    print("ℹ️ Atualizações não são aplicadas automaticamente; revise antes de usar fwupdmgr update.")
