from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

DEFAULT_EXCLUDES = [
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "id_rsa",
    "id_ed25519",
    "credentials.*",
    "secrets.*",
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "coverage",
    "target",
    "__pycache__",
]


class GraphifyConfig(BaseModel):
    enabled: bool = True
    auto_update: bool = True


class TestingConfig(BaseModel):
    command: str = "pytest"


class ExcludeConfig(BaseModel):
    patterns: list[str] = Field(default_factory=list)


class Config(BaseModel):
    scope: str = "."
    context_dirs: list[str] = Field(default_factory=list)
    context_budget_chars: int = Field(default=45000, ge=5000)
    approval_mode: Literal["safe", "normal", "trusted"] = "normal"
    iteration_limit: int = Field(default=30, ge=1)
    command_timeout_seconds: int = Field(default=120, ge=1)
    graphify: GraphifyConfig = Field(default_factory=GraphifyConfig)
    testing: TestingConfig = Field(default_factory=TestingConfig)
    exclude: ExcludeConfig = Field(default_factory=ExcludeConfig)


def load_config(root: Path) -> Config:
    path = root / ".cwah.toml"
    return (
        Config.model_validate(tomllib.loads(path.read_text("utf-8"))) if path.exists() else Config()
    )
