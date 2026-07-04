from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

from .context import Context
from .modules import MODULES
from .runner import Runner
from .system import detect


PROFILES = {
    "minimal": ("base",),
    "devops": ("base", "devops", "integrations"),
    "workstation": ("base", "firmware", "devops", "desktop", "multimedia", "vscode", "integrations"),
    "full": ("base", "firmware", "devops", "desktop", "multimedia", "vscode", "dell", "virtualization", "nvidia", "hyperx", "hashicorp", "integrations"),
}


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description="Bootstrap Fedora/Ubuntu para DevOps e OpenShift")
    selection = command.add_mutually_exclusive_group()
    selection.add_argument("--profile", choices=PROFILES)
    selection.add_argument("--modules", nargs="+", choices=MODULES)
    selection.add_argument("--interactive", action="store_true")
    command.add_argument("--dry-run", action="store_true")
    command.add_argument("--upgrade", action="store_true", help="atualiza todo o sistema antes da instalação")
    command.add_argument("--force-hardware", action="store_true", help="força módulos de hardware/virtualização")
    command.add_argument("--keyboard-layout", choices=("us", "us-intl", "br"))
    command.add_argument("--hardware-profile", choices=("auto", "precision-3591"), default="auto")
    command.add_argument("--terminal-config", action=argparse.BooleanOptionalAction, default=None)
    command.add_argument("--openshift-cli", action=argparse.BooleanOptionalAction, default=None)
    command.add_argument("--show-hardware", action="store_true")
    command.add_argument("--list-modules", action="store_true")
    return command


def _yes_no(prompt: str, default: bool) -> bool:
    suffix = "[S/n]" if default else "[s/N]"
    answer = input(f"{prompt} {suffix} ").strip().lower()
    if not answer:
        return default
    return answer in {"s", "sim", "y", "yes"}


def _interactive(args: argparse.Namespace) -> None:
    print("Perfis: minimal, devops, workstation, full")
    args.profile = input("Perfil [workstation]: ").strip() or "workstation"
    if args.profile not in PROFILES:
        raise SystemExit(f"Perfil inválido: {args.profile}")
    args.upgrade = _yes_no("Atualizar o sistema inteiro?", False)
    args.terminal_config = _yes_no("Instalar terminal-config?", True)
    args.openshift_cli = _yes_no("Instalar CLIs OpenShift/Kubernetes?", True)
    layout = input("Layout do teclado [us/us-intl/br, vazio=não alterar]: ").strip()
    if layout:
        if layout not in {"us", "us-intl", "br"}:
            raise SystemExit(f"Layout inválido: {layout}")
        args.keyboard_layout = layout


def main(argv: list[str] | None = None) -> None:
    args = parser().parse_args(argv)
    if args.list_modules:
        print("\n".join(MODULES))
        return

    facts = detect()
    if args.show_hardware:
        print(facts.to_json())
        if not args.profile and not args.modules and not args.interactive:
            return

    if args.interactive:
        _interactive(args)
    if not args.profile and not args.modules:
        if sys.stdin.isatty():
            _interactive(args)
        else:
            parser().error("informe --profile, --modules ou --interactive")

    selected = tuple(args.modules or PROFILES[args.profile])
    terminal = args.terminal_config if args.terminal_config is not None else "integrations" in selected
    openshift = args.openshift_cli if args.openshift_cli is not None else "integrations" in selected

    print(f"🖥️ Sistema: {facts.pretty_name}; RAM={facts.memory_gib} GiB; WSL={facts.wsl}")
    print(f"🧩 Módulos: {', '.join(selected)}")
    ctx = Context(
        root=Path(__file__).resolve().parents[1],
        home=Path.home(),
        facts=facts,
        runner=Runner(args.dry_run),
    )
    for name in selected:
        module = importlib.import_module(f"workstation_setup.modules.{name}")
        module.install(
            ctx,
            upgrade=args.upgrade,
            force=args.force_hardware,
            keyboard_layout=args.keyboard_layout,
            hardware_profile=args.hardware_profile,
            terminal_config=terminal,
            openshift_cli=openshift,
        )
    print("✅ Bootstrap concluído. Revise mensagens de reboot/logout.")
