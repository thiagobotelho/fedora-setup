from ..catalog import DEVOPS
from ..context import Context


def install(ctx: Context, **_: object) -> None:
    print("🧰 Módulo DevOps/Infra")
    ctx.packages(
        fedora=DEVOPS["fedora"],
        ubuntu=DEVOPS["ubuntu"],
        debian=DEVOPS["debian"],
    )
    if not ctx.facts.wsl:
        user = ctx.home.name
        ctx.runner.run(["usermod", "-aG", "wireshark", user], sudo=True, check=False)
