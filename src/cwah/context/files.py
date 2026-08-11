from __future__ import annotations

import subprocess
from pathlib import Path

from cwah.security.secrets import is_filtered


def tracked_files(root: Path, extra_excludes: list[str] | None = None) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        names = result.stdout.splitlines()
    else:
        names = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]
    return sorted(x for x in names if not is_filtered(x, extra_excludes))


def read_snippet(path: Path, max_chars: int = 8000) -> tuple[str, int, int, bool]:
    text = path.read_text("utf-8", errors="replace")
    lines = text.splitlines()
    chunk = "\n".join(lines)
    if len(chunk) <= max_chars:
        return chunk, 1, max(1, len(lines)), False
    selected = chunk[:max_chars].rsplit("\n", 1)[0]
    return selected, 1, selected.count("\n") + 1, True
