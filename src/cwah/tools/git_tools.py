from __future__ import annotations

import subprocess
from pathlib import Path


def git(root: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    return (r.stdout + r.stderr).strip()


def snapshot(root: Path) -> dict[str, str]:
    return {
        "branch": git(root, "branch", "--show-current"),
        "status": git(root, "status", "--short"),
        "diff": git(root, "diff", "--no-ext-diff"),
    }
