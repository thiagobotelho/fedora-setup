from ..context import Context
from .rpmfusion import enable as enable_rpm_fusion


FEDORA_PACKAGES = [
    "ffmpeg", "ffmpeg-libs", "libva", "libva-utils", "intel-media-driver",
    "openh264", "gstreamer1-plugin-openh264", "mozilla-openh264",
    "libfreeaptx", "libldac", "fdk-aac", "fuse-libs",
    "google-noto-sans-fonts", "google-noto-serif-fonts",
    "liberation-sans-fonts", "liberation-serif-fonts",
    "liberation-mono-fonts", "7zip", "unrar",
]

APT_PACKAGES = [
    "ffmpeg", "libavcodec-extra", "vainfo", "ubuntu-restricted-addons",
    "libfuse2t64", "fonts-noto-core", "fonts-liberation",
    "p7zip-full", "unrar",
]

DEBIAN_PACKAGES = [
    "ffmpeg", "vainfo", "libfuse2", "fonts-noto-core", "fonts-liberation",
    "p7zip-full",
]


def install(ctx: Context, **_: object) -> None:
    if ctx.facts.wsl:
        print("🪟 WSL detectado: módulo multimídia ignorado")
        return
    print("🎞️ Módulo multimídia/codecs")
    if ctx.facts.distro == "fedora":
        enable_rpm_fusion(ctx)
        ctx.runner.run(
            ["dnf", "swap", "-y", "ffmpeg-free", "ffmpeg", "--allowerasing"],
            sudo=True,
            check=False,
        )
        ctx.runner.run(
            ["dnf", "group", "upgrade", "-y", "multimedia"],
            sudo=True,
            check=False,
        )
        ctx.packages(fedora=FEDORA_PACKAGES, ubuntu=[], debian=[])
        ctx.runner.run(
            [
                "dnf", "config-manager", "setopt",
                "fedora-cisco-openh264.enabled=1",
            ],
            sudo=True,
            check=False,
        )
        return

    if ctx.facts.distro == "ubuntu":
        ctx.runner.run(["add-apt-repository", "-y", "multiverse"], sudo=True)
        ctx.runner.run(["apt-get", "update"], sudo=True)
    ctx.packages(fedora=[], ubuntu=APT_PACKAGES, debian=DEBIAN_PACKAGES)
