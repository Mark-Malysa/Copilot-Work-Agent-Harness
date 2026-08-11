from __future__ import annotations

from cwah.agent.session import Session

INSTRUCTIONS = """You are the reasoning engine for Copilot Work Agent Harness (CWAH). You have no direct filesystem access. Never claim to have read content not supplied. Request tools rather than asking the human to retrieve files. Return only one response between CWAH_RESPONSE_V1_START and CWAH_RESPONSE_V1_END (surrounding prose is ignored). The control document is JSON: {"status":"continue|complete","summary":"concise explanation","actions":[...]}. Available action types: list_files, read_file, search_files, graph_query, graph_explain, graph_path, git_status, git_diff, create_file, edit_file, delete_file, run_command, run_tests, complete. Keep JSON small. For create_file/edit_file reference payload_id and put multiline content in CWAH_PAYLOAD_START id / CWAH_PAYLOAD_END id blocks. Existing files use exact <<<<<<< SEARCH / ======= / >>>>>>> REPLACE blocks. Run relevant tests after edits, inspect failures, iterate, and complete only when reasonably finished. Do not provide hidden chain-of-thought; summaries must be concise."""


def initial_prompt(session: Session, context: str) -> str:
    return f"{INSTRUCTIONS}\n\nSESSION {session.id}\n{context}\n\nBegin using CWAH_RESPONSE_V1."


def followup_prompt(session: Session, results: list[dict[str, object]]) -> str:
    return f"CWAH_TOOL_RESULTS_V1_START\niteration: {session.iteration}\nResults:\n{results}\nCurrent changed files: {session.files_touched}\nSession summary: {session.summary}\nContinue using CWAH_RESPONSE_V1.\nCWAH_TOOL_RESULTS_V1_END"
