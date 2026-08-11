from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from cwah.context.files import tracked_files


def search(root: Path, query: str, limit: int = 30) -> list[str]:
    if shutil.which("rg"):
        r = subprocess.run(
            ["rg", "-n", "--no-heading", "--color=never", "-F", query, str(root)],
            text=True,
            capture_output=True,
            check=False,
        )
        return r.stdout.splitlines()[:limit]
    out = []
    for name in tracked_files(root):
        p = root / name
        try:
            for no, line in enumerate(p.read_text("utf-8", errors="ignore").splitlines(), 1):
                if query in line:
                    out.append(f"{name}:{no}:{line}")
                if len(out) >= limit:
                    return out
        except OSError:
            pass
    return out
