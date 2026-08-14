from __future__ import annotations

from collections.abc import Callable

from cwah.config import Config
from cwah.context.files import read_snippet, tracked_files
from cwah.context.search import search
from cwah.graph.graphify import GraphifyAdapter
from cwah.protocol.models import Action
from cwah.security.paths import Workspace
from cwah.tools.edit_file import apply_search_replace, create_file
from cwah.tools.git_tools import git
from cwah.tools.run_command import run_command


def execute(
    action: Action,
    payloads: dict[str, str],
    workspace: Workspace,
    config: Config,
    approve: Callable[[str], bool] = lambda _: True,
) -> dict[str, object]:
    root = workspace.root
    t = action.type
    try:
        if t == "list_files":
            return {"id": action.id, "ok": True, "output": tracked_files(root)[:1000]}
        if t == "read_file":
            p = workspace.resolve(action.path or "")
            content, start, end, trunc = read_snippet(p, 16000)
            return {
                "id": action.id,
                "ok": True,
                "path": workspace.relative(p),
                "lines": f"{start}-{end}",
                "truncated": trunc,
                "output": content,
            }
        if t == "search_files":
            return {
                "id": action.id,
                "ok": True,
                "output": search(root, action.query or action.pattern or ""),
            }
        if t in {"git_status", "git_diff"}:
            return {
                "id": action.id,
                "ok": True,
                "output": git(root, "status", "--short", "--", ".")
                if t == "git_status"
                else git(root, "diff", "--", "."),
            }
        if t.startswith("graph_"):
            g = GraphifyAdapter(root)
            r = (
                g.query(action.query or "")
                if t == "graph_query"
                else g.explain(action.symbol or "")
                if t == "graph_explain"
                else g.path(action.source or "", action.target or "")
            )
            return {"id": action.id, "ok": r.ok, "output": r.output}
        if t in {"create_file", "edit_file", "delete_file"}:
            p = workspace.resolve(action.path or "")
            outside = not workspace.in_write_scope(p)
            if not approve(
                f"{t} {workspace.relative(p)}" + (" (outside scope)" if outside else "")
            ):
                return {"id": action.id, "ok": False, "error": "denied"}
            if t == "create_file":
                create_file(p, payloads[action.payload_id or ""])
            elif t == "edit_file":
                apply_search_replace(p, payloads[action.payload_id or ""])
            else:
                p.unlink()
            return {"id": action.id, "ok": True, "changed": workspace.relative(p)}
        if t in {"run_command", "run_tests"}:
            command = action.command if t == "run_command" else config.testing.command
            cwd = workspace.resolve(action.cwd or ".")
            if not approve(f"run `{command}` in {cwd}"):
                return {"id": action.id, "ok": False, "error": "denied"}
            return {
                "id": action.id,
                "ok": True,
                "result": run_command(command or "", cwd, config.command_timeout_seconds).__dict__,
            }
        return {"id": action.id, "ok": True, "output": "complete"}
    except Exception as exc:
        return {"id": action.id, "ok": False, "error": str(exc)}
