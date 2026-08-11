from __future__ import annotations

import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path


class UnsafeCommand(ValueError):
    pass


DANGEROUS = [
    r"\brm\s+-(?:rf|fr)\b",
    r"\bformat\s+[a-z]:",
    r"\bmkfs\b",
    r"\bshutdown\b",
    r"\breboot\b",
    r"Remove-Item.*-Recurse.*-Force",
    r":\(\)\s*\{",
]


def validate_command(command: str) -> None:
    if any(re.search(p, command, re.I) for p in DANGEROUS):
        raise UnsafeCommand("Obviously destructive command denied")


@dataclass
class CommandResult:
    command: str
    cwd: str
    stdout: str
    stderr: str
    exit_code: int
    duration: float
    timed_out: bool = False


def run_command(command: str, cwd: Path, timeout: int = 120) -> CommandResult:
    validate_command(command)
    start = time.monotonic()
    try:
        r = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as e:
        stdout = (
            e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        )
        stderr = (
            e.stderr.decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        )
        return CommandResult(command, str(cwd), stdout, stderr, -1, time.monotonic() - start, True)
    return CommandResult(
        command, str(cwd), r.stdout, r.stderr, r.returncode, time.monotonic() - start
    )
