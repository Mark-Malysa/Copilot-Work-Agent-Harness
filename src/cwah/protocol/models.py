from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ActionType = Literal[
    "list_files",
    "read_file",
    "search_files",
    "graph_query",
    "graph_explain",
    "graph_path",
    "git_status",
    "git_diff",
    "create_file",
    "edit_file",
    "delete_file",
    "run_command",
    "run_tests",
    "complete",
]


class Action(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    type: ActionType
    path: str | None = None
    query: str | None = None
    symbol: str | None = None
    source: str | None = None
    target: str | None = None
    command: str | None = None
    cwd: str | None = None
    payload_id: str | None = None
    pattern: str | None = None

    @model_validator(mode="after")
    def required_fields(self) -> Action:
        if self.type in {"read_file", "create_file", "edit_file", "delete_file"} and not self.path:
            raise ValueError("path required")
        if self.type in {"create_file", "edit_file"} and not self.payload_id:
            raise ValueError("payload_id required")
        if self.type == "run_command" and not self.command:
            raise ValueError("command required")
        return self


class Response(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["continue", "complete"]
    summary: str = ""
    actions: list[Action] = Field(default_factory=list)
