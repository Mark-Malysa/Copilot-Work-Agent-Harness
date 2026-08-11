from __future__ import annotations

from collections.abc import Callable, Iterable
from pathlib import Path

from cwah.agent.session import Session, SessionStore
from cwah.config import Config
from cwah.protocol.parser import ProtocolError, parse_response, repair_prompt
from cwah.protocol.prompts import followup_prompt
from cwah.security.paths import Workspace
from cwah.tools.registry import execute
from cwah.transport.clipboard import Clipboard


def process_response(
    text: str,
    session: Session,
    store: SessionStore,
    config: Config,
    clipboard: Clipboard,
    approve: Callable[[str], bool] = lambda _: True,
) -> bool:
    try:
        parsed = parse_response(text)
    except ProtocolError as exc:
        clipboard.copy(repair_prompt(exc))
        return False
    workspace = Workspace(Path(session.repo_root), session.scope, session.context_dirs)
    results = []
    for action in parsed.control.actions:
        result = execute(action, parsed.payloads, workspace, config, approve)
        results.append(result)
        session.actions.append(action.model_dump())
        if result.get("changed") and result["changed"] not in session.files_touched:
            session.files_touched.append(str(result["changed"]))
        if action.type == "read_file" and action.path and action.path not in session.files_read:
            session.files_read.append(action.path)
        if "result" in result:
            session.command_results.append(result["result"])  # type: ignore[arg-type]
    session.iteration += 1
    session.summary = parsed.control.summary
    session.completed = parsed.control.status == "complete" or any(
        a.type == "complete" for a in parsed.control.actions
    )
    store.save(session)
    if not session.completed:
        clipboard.copy(followup_prompt(session, results))
    return session.completed


def run_scripted(
    session: Session,
    store: SessionStore,
    config: Config,
    clipboard: Clipboard,
    responses: Iterable[str],
) -> bool:
    done = False
    for response in responses:
        done = process_response(response, session, store, config, clipboard)
        if done:
            break
    return done
