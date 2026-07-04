from __future__ import annotations

import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Runner:
    dry_run: bool = False

    def run(
        self,
        args: Iterable[str | Path],
        *,
        sudo: bool = False,
        check: bool = True,
        capture: bool = False,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command = [str(item) for item in args]
        if sudo:
            command.insert(0, "sudo")
        print("🔧", shlex.join(command))
        if self.dry_run:
            return subprocess.CompletedProcess(command, 0, "", "")
        return subprocess.run(
            command,
            check=check,
            text=True,
            capture_output=capture,
            input=input_text,
        )
