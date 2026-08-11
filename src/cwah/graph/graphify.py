from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GraphResult:
    ok: bool
    output: str


class GraphifyAdapter:
    def __init__(self, root: Path):
        self.root = root

    def version(self) -> str | None:
        if not shutil.which("graphify"):
            return None
        r = subprocess.run(
            ["graphify", "--version"], capture_output=True, text=True, check=False, timeout=10
        )
        return (r.stdout or r.stderr).strip() if r.returncode == 0 else None

    def _run(self, args: list[str]) -> GraphResult:
        try:
            r = subprocess.run(
                ["graphify", *args],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
                timeout=120,
            )
            return GraphResult(r.returncode == 0, (r.stdout + r.stderr)[:12000])
        except (OSError, subprocess.TimeoutExpired) as e:
            return GraphResult(False, str(e))

    def index(self, scope: str = ".") -> GraphResult:
        return self._run(["index", scope, "--code-only"])

    def query(self, query: str) -> GraphResult:
        return self._run(["query", query])

    def explain(self, symbol: str) -> GraphResult:
        return self._run(["explain", symbol])

    def path(self, source: str, target: str) -> GraphResult:
        return self._run(["path", source, target])
