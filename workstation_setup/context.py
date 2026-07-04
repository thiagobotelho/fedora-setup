from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .runner import Runner
from .system import Facts


@dataclass
class Context:
    root: Path
    home: Path
    facts: Facts
    runner: Runner

    def packages(
        self,
        *,
        fedora: list[str],
        ubuntu: list[str],
        debian: list[str] | None = None,
        check: bool = True,
    ) -> None:
        if self.facts.distro == "fedora":
            self.runner.run(["dnf", "install", "-y", *fedora], sudo=True, check=check)
            return
        selected = debian if self.facts.distro == "debian" and debian is not None else ubuntu
        self.runner.run(["apt-get", "install", "-y", *selected], sudo=True, check=check)

    def ensure_apt_index(self) -> None:
        if self.facts.package_manager == "apt":
            self.runner.run(["apt-get", "update"], sudo=True)

    def git_checkout(self, url: str, destination: Path) -> None:
        if (destination / ".git").exists():
            self.runner.run(["git", "-C", destination, "pull", "--ff-only"])
        elif destination.exists():
            raise RuntimeError(f"Destino existe e não é repositório Git: {destination}")
        else:
            self.runner.run(["git", "clone", url, destination])
