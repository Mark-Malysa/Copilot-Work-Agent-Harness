from fnmatch import fnmatch
from pathlib import PurePath

from cwah.config import DEFAULT_EXCLUDES


def is_filtered(path: str, extra: list[str] | None = None) -> bool:
    p = PurePath(path)
    patterns = DEFAULT_EXCLUDES + (extra or [])
    return any(
        fnmatch(p.name, pat) or any(fnmatch(part, pat) for part in p.parts) for pat in patterns
    )
