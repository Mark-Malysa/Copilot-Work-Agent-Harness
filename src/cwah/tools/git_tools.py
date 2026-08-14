from __future__ import annotations

import subprocess
from pathlib import Path


def git(root: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    return (r.stdout + r.stderr).strip()


def snapshot(root: Path) -> dict[str, str]:
    worktree = git(root, "rev-parse", "--show-toplevel")
    common = git(root, "rev-parse", "--git-common-dir")
    common_path = Path(common)
    if common and not common_path.is_absolute():
        common = str((root / common_path).resolve())
    return {
        "branch": git(root, "branch", "--show-current"),
        "worktree_root": str(Path(worktree).resolve()) if worktree else "",
        "git_common_dir": common,
        "status": git(root, "status", "--short", "--", "."),
        "diff": git(root, "diff", "--no-ext-diff", "--", "."),
    }
