from __future__ import annotations

import secrets
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, Field


class Session(BaseModel):
    id: str
    task: str
    repo_root: str
    invocation_directory: str = ""
    workspace_root: str = ""
    git_worktree_root: str = ""
    git_common_dir: str = ""
    scope: str = "."
    context_dirs: list[str] = Field(default_factory=list)
    relevant_files: list[str] = Field(default_factory=list)
    files_read: list[str] = Field(default_factory=list)
    actions: list[dict[str, object]] = Field(default_factory=list)
    command_results: list[dict[str, object]] = Field(default_factory=list)
    files_touched: list[str] = Field(default_factory=list)
    initial_git: dict[str, str] = Field(default_factory=dict)
    summary: str = ""
    iteration: int = 0
    protocol_version: str = "1"
    completed: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class SessionStore:
    def __init__(self, root: Path):
        self.directory = root / ".cwah" / "sessions"

    def create(self, **kwargs: object) -> Session:
        session = Session.model_validate(
            {
                "id": datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(2),
                **kwargs,
            }
        )
        self.save(session)
        return session

    def save(self, s: Session) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        (self.directory / f"{s.id}.json").write_text(s.model_dump_json(indent=2), "utf-8")

    def load(self, id: str) -> Session:
        return Session.model_validate_json((self.directory / f"{id}.json").read_text("utf-8"))

    def list(self) -> list[Session]:
        return (
            [
                Session.model_validate_json(p.read_text("utf-8"))
                for p in sorted(self.directory.glob("*.json"), reverse=True)
            ]
            if self.directory.exists()
            else []
        )

    def latest(self) -> Session:
        sessions = self.list()
        if not sessions:
            raise FileNotFoundError("No CWAH sessions in this repository")
        return sessions[0]
