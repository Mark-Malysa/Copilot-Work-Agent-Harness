from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


def normalize_relative(value: str) -> str:
    """Normalize a user-facing repository path without giving it host-specific separators."""
    normalized = value.replace("\\", "/").strip()
    return normalized.rstrip("/") or "."


@dataclass(frozen=True)
class GitWorktree:
    root: Path
    git_dir: Path
    common_dir: Path
    branch: str


@dataclass(frozen=True)
class WorkspaceInfo:
    invocation_directory: Path
    root: Path
    scope: str
    git: GitWorktree | None


def resolve_workspace(
    repo: Path, scope: str = ".", invocation: Path | None = None
) -> WorkspaceInfo:
    invocation_directory = (invocation or Path.cwd()).resolve()
    workspace_root = (
        repo.resolve() if repo.is_absolute() else (invocation_directory / repo).resolve()
    )
    if not workspace_root.is_dir():
        raise ValueError(f"Workspace is not a directory: {workspace_root}")
    normalized_scope = normalize_relative(scope)
    # Workspace performs the canonical escape/symlink check without creating a dependency here.
    candidate = (workspace_root / Path(normalized_scope)).resolve()
    try:
        candidate.relative_to(workspace_root)
    except ValueError as exc:
        raise ValueError(f"Scope escapes workspace: {scope}") from exc
    return WorkspaceInfo(
        invocation_directory, workspace_root, normalized_scope, discover_git(workspace_root)
    )


def discover_git(cwd: Path) -> GitWorktree | None:
    root = _git(cwd, "rev-parse", "--show-toplevel")
    if root is None:
        return None
    git_dir = _git(cwd, "rev-parse", "--git-dir")
    common_dir = _git(cwd, "rev-parse", "--git-common-dir")
    if git_dir is None or common_dir is None:
        return None
    return GitWorktree(
        Path(root).resolve(),
        _absolute_git_path(cwd, git_dir),
        _absolute_git_path(cwd, common_dir),
        _git(cwd, "branch", "--show-current") or "(detached HEAD)",
    )


def _absolute_git_path(cwd: Path, value: str) -> Path:
    path = Path(value)
    return (path if path.is_absolute() else cwd / path).resolve()


def _git(cwd: Path, *args: str) -> str | None:
    result = subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else None
