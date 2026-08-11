from __future__ import annotations

import re
from pathlib import Path


def find_explicit_refs(task: str, root: Path) -> list[str]:
    candidates = re.findall(
        r"(?<![\w])(?:[\w.-]+[\\/])+[\w.@() -]+\.[A-Za-z0-9]+|(?<![\w])[\w.-]+\.(?:py|md|toml|json|ya?ml|js|ts|tsx|rs|go)",
        task,
    )
    found = []
    for raw in candidates:
        value = raw.strip("'\"`.,:;!?()[]{}").replace("\\", "/")
        if (root / value).is_file() and value not in found:
            found.append(value)
    return found
