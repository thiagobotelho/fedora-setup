from ..context import Context


def install(
    ctx: Context,
    *,
    force: bool = False,
    keyboard_layout: str | None = None,
    **_: object,
) -> None:
    if ctx.facts.wsl:
        print("🪟 WSL detectado: configure o teclado HyperX pelo Windows")
        return
    if not ctx.facts.hyperx and not force:
        print("ℹ️ Dispositivo HyperX não detectado; módulo ignorado")
        return

    print(f"⌨️ Módulo HyperX/OpenRGB ({', '.join(ctx.facts.hyperx_usb_ids) or 'forçado'})")
    ctx.packages(fedora=["openrgb"], ubuntu=["openrgb"], debian=["openrgb"])
    if keyboard_layout:
        keymaps = {
            "us": ("us", ["us"]),
            "us-intl": ("us", ["us", "", "intl"]),
            "br": ("br-abnt2", ["br"]),
        }
        console, x11 = keymaps[keyboard_layout]
        ctx.runner.run(["localectl", "set-keymap", console], sudo=True)
        ctx.runner.run(["localectl", "set-x11-keymap", *x11], sudo=True)
    print("ℹ️ O NGENUITY é exclusivo do Windows; no Linux, use OpenRGB para iluminação compatível.")
