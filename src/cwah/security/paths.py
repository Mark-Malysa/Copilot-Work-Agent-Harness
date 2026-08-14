from __future__ import annotations

from pathlib import Path


class PathSecurityError(ValueError):
    pass


class Workspace:
    def __init__(self, root: Path, scope: str = ".", contexts: list[str] | None = None):
        self.root = root.resolve()
        self.scope = self.resolve(_normalize(scope))
        self.contexts = [self.resolve(p) for p in (contexts or [])]

    def resolve(self, path: str | Path) -> Path:
        if isinstance(path, str):
            path = _normalize(path)
        candidate = Path(path)
        candidate = (
            candidate.resolve() if candidate.is_absolute() else (self.root / candidate).resolve()
        )
        try:
            candidate.relative_to(self.root)
        except ValueError as exc:
            raise PathSecurityError(f"Path escapes workspace: {path}") from exc
        return candidate

    def relative(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def in_read_scope(self, path: str | Path) -> bool:
        p = self.resolve(path)
        return any(_within(p, base) for base in [self.scope, *self.contexts])

    def in_write_scope(self, path: str | Path) -> bool:
        return _within(self.resolve(path), self.scope)


def _within(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def _normalize(path: str) -> str:
    return path.replace("\\", "/")
