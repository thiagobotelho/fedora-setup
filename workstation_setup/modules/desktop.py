from ..catalog import DESKTOP, FLATPAKS
from ..context import Context


def install(ctx: Context, **_: object) -> None:
    if ctx.facts.wsl:
        print("🪟 WSL detectado: módulo desktop ignorado")
        return
    print("🖥️ Módulo desktop")
    ctx.packages(
        fedora=DESKTOP["fedora"],
        ubuntu=DESKTOP["ubuntu"],
        debian=DESKTOP["debian"],
    )
    ctx.runner.run([
        "flatpak", "remote-add", "--if-not-exists", "flathub",
        "https://flathub.org/repo/flathub.flatpakrepo",
    ])
    for app in FLATPAKS:
        ctx.runner.run(["flatpak", "install", "-y", "flathub", app])
