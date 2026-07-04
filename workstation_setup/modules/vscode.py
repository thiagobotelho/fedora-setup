from pathlib import Path

from ..context import Context


def install(ctx: Context, **_: object) -> None:
    if ctx.facts.wsl:
        print("🪟 WSL detectado: use VS Code no Windows com a extensão Remote WSL")
        return

    print("🧑‍💻 Módulo Visual Studio Code")
    if ctx.facts.distro == "fedora":
        ctx.runner.run(
            ["rpm", "--import", "https://packages.microsoft.com/keys/microsoft.asc"],
            sudo=True,
        )
        repo = """[code]
name=Visual Studio Code
baseurl=https://packages.microsoft.com/yumrepos/vscode
enabled=1
autorefresh=1
type=rpm-md
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc
"""
        ctx.runner.run(
            ["tee", "/etc/yum.repos.d/vscode.repo"],
            sudo=True,
            input_text=repo,
        )
        ctx.runner.run(["dnf", "install", "-y", "code"], sudo=True)
        return

    temp_key = Path("/tmp/fedora-setup-microsoft.asc")
    temp_ring = Path("/tmp/fedora-setup-microsoft.gpg")
    ctx.runner.run([
        "curl", "-fsSL", "https://packages.microsoft.com/keys/microsoft.asc",
        "-o", temp_key,
    ])
    ctx.runner.run(["gpg", "--dearmor", "--yes", "--output", temp_ring, temp_key])
    ctx.runner.run(
        ["install", "-m", "0644", temp_ring, "/usr/share/keyrings/microsoft.gpg"],
        sudo=True,
    )
    sources = """Types: deb
URIs: https://packages.microsoft.com/repos/code
Suites: stable
Components: main
Architectures: amd64 arm64 armhf
Signed-By: /usr/share/keyrings/microsoft.gpg
"""
    ctx.runner.run(
        ["tee", "/etc/apt/sources.list.d/vscode.sources"],
        sudo=True,
        input_text=sources,
    )
    ctx.runner.run(["apt-get", "update"], sudo=True)
    ctx.runner.run(["apt-get", "install", "-y", "code"], sudo=True)
