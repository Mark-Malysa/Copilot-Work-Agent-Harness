# Development

```bash
uv sync --extra dev
uv run ruff format .
uv run ruff check .
uv run mypy
uv run pytest
uv run cwah demo
uv build
```

Source is under `src/cwah`: CLI/config; `agent` loop/session; `context` selection; `protocol` models/parser/prompts; `security`; optional `graph`; local `tools`; clipboard `transport`. Tests use temporary Git repositories and `MemoryClipboard`, never the developer clipboard.

To add an action, extend the literal/field validation in `protocol/models.py`, implement authorization/execution in `tools/registry.py`, update initial instructions and protocol/usage/security docs, then test malformed and success cases. Protocol changes require new markers rather than silently changing V1. Keep raw multiline data outside JSON.

Graphify CLI variability belongs exclusively in `GraphifyAdapter`; mock `_run` in tests and preserve graceful fallback. Clipboard behavior belongs behind the `Clipboard` protocol.

For a Windows executable install the dev extra, then run `uv run python scripts/build_exe.py`; test `dist\cwah.exe --help`, `doctor`, and `demo` on Windows. PyInstaller is development-only and Graphify stays external.
