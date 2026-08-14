from __future__ import annotations

import subprocess
from pathlib import Path

from cwah.security.secrets import is_filtered


def workspace_files(
    root: Path, extra_excludes: list[str] | None = None
) -> tuple[list[str], list[str]]:
    """Return tracked and untracked files, always relative to and contained by root."""
    tracked = _git_files(root, "--cached")
    untracked = _git_files(root, "--others", "--exclude-standard")
    if tracked is None or untracked is None:
        names = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]
        return [], _safe_names(root, names, extra_excludes)
    return (
        _safe_names(root, tracked, extra_excludes),
        _safe_names(root, untracked, extra_excludes),
    )


def _git_files(root: Path, *args: str) -> list[str] | None:
    result = subprocess.run(
        ["git", "ls-files", "-z", *args, "--", "."],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.split("\0")[:-1] if result.returncode == 0 else None


def _safe_names(root: Path, names: list[str], excludes: list[str] | None) -> list[str]:
    safe: list[str] = []
    for raw in names:
        name = raw.replace("\\", "/").removeprefix("./")
        try:
            (root / name).resolve().relative_to(root.resolve())
        except ValueError:
            continue
        if name and not is_filtered(name, excludes):
            safe.append(name)
    return sorted(set(safe))


def tracked_files(root: Path, extra_excludes: list[str] | None = None) -> list[str]:
    tracked, untracked = workspace_files(root, extra_excludes)
    return sorted([*tracked, *untracked])


def read_snippet(path: Path, max_chars: int = 8000) -> tuple[str, int, int, bool]:
    text = path.read_text("utf-8", errors="replace")
    lines = text.splitlines()
    chunk = "\n".join(lines)
    if len(chunk) <= max_chars:
        return chunk, 1, max(1, len(lines)), False
    selected = chunk[:max_chars].rsplit("\n", 1)[0]
    return selected, 1, selected.count("\n") + 1, True
