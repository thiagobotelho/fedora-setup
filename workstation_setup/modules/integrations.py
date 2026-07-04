from __future__ import annotations

from ..context import Context


REPOSITORIES = {
    "terminal": (
        "https://github.com/thiagobotelho/terminal-config.git",
        "terminal-config",
    ),
    "openshift": (
        "https://github.com/thiagobotelho/openshift-cli-installer.git",
        "openshift-cli-installer",
    ),
}


def install(
    ctx: Context,
    *,
    terminal_config: bool = True,
    openshift_cli: bool = True,
    **_: object,
) -> None:
    print("🔗 Módulo de integrações")
    targets = []
    if terminal_config:
        targets.append("terminal")
    if openshift_cli:
        targets.append("openshift")

    for name in targets:
        url, directory = REPOSITORIES[name]
        destination = ctx.home / directory
        ctx.git_checkout(url, destination)
        command = ["python3", destination / "install.py"]
        if name == "terminal":
            if ctx.facts.wsl:
                command += ["--profile", "wsl"]
            else:
                command += ["--modules", "core", "fonts", "neovim"]
        ctx.runner.run(command)
