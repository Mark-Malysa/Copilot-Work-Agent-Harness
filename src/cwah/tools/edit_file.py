from __future__ import annotations

import re
from pathlib import Path


class EditError(ValueError):
    pass


_PATTERN = re.compile(r"<<<<<<< SEARCH\n(.*?)\n=======\n(.*?)\n>>>>>>> REPLACE", re.S)


def apply_search_replace(path: Path, payload: str) -> int:
    pairs = _PATTERN.findall(payload)
    if not pairs:
        raise EditError("No valid SEARCH/REPLACE blocks")
    content = path.read_text("utf-8")
    for search, replacement in pairs:
        count = content.count(search)
        if count == 0:
            raise EditError("SEARCH text not found")
        if count > 1:
            raise EditError("SEARCH text is ambiguous")
        content = content.replace(search, replacement, 1)
    path.write_text(content, "utf-8")
    return len(pairs)


def create_file(path: Path, payload: str) -> None:
    if path.exists():
        raise EditError("File already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, "utf-8")
