from __future__ import annotations

import platform
from pathlib import Path

from ..context import Context


def install(ctx: Context, **_: object) -> None:
    print("🏗️ Módulo HashiCorp (Terraform, Packer, Vault)")
    temp = Path("/tmp/fedora-setup-hashicorp")
    if ctx.facts.distro == "fedora":
        repo = temp.with_suffix(".repo")
        ctx.runner.run([
            "curl", "-fsSL",
            "https://rpm.releases.hashicorp.com/fedora/hashicorp.repo",
            "-o", repo,
        ])
        ctx.runner.run(
            ["install", "-m", "0644", repo, "/etc/yum.repos.d/hashicorp.repo"],
            sudo=True,
        )
        ctx.runner.run(["dnf", "install", "-y", "terraform", "packer", "vault"], sudo=True)
        return

    if not ctx.facts.codename:
        raise RuntimeError("Codename Debian/Ubuntu não identificado para o repositório HashiCorp")
    key = temp.with_suffix(".asc")
    keyring = temp.with_suffix(".gpg")
    ctx.runner.run([
        "curl", "-fsSL", "https://apt.releases.hashicorp.com/gpg", "-o", key,
    ])
    ctx.runner.run(["gpg", "--dearmor", "--yes", "--output", keyring, key])
    ctx.runner.run(
        ["install", "-m", "0644", keyring, "/usr/share/keyrings/hashicorp-archive-keyring.gpg"],
        sudo=True,
    )
    architecture = {"x86_64": "amd64", "aarch64": "arm64"}.get(platform.machine(), platform.machine())
    source = (
        f"deb [arch={architecture} signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] "
        f"https://apt.releases.hashicorp.com {ctx.facts.codename} main\n"
    )
    ctx.runner.run(
        ["tee", "/etc/apt/sources.list.d/hashicorp.list"],
        sudo=True,
        input_text=source,
    )
    ctx.runner.run(["apt-get", "update"], sudo=True)
    ctx.runner.run(["apt-get", "install", "-y", "terraform", "packer", "vault"], sudo=True)
