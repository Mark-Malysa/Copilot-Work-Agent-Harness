# Troubleshooting

- **Response will not parse / Copilot ignored protocol:** copy the entire reply, including both markers. Paste CWAH's automatic repair prompt and copy the corrected whole reply. Do not hand-edit unless using `ingest-response` for clipboard recovery.
- **Clipboard failed:** verify an interactive desktop/RDP clipboard, install platform clipboard facilities, or save UTF-8 and run `cwah ingest-response response.txt`.
- **Graphify unavailable:** expected and nonfatal; check PATH/`graphify --version`, or disable it. Git/search fallback is automatic.
- **Graphify index stale:** run `cwah index --scope YOUR_SCOPE`; check version-specific upstream CLI help if its syntax changed.
- **ripgrep unavailable:** Python fallback is slower but functional. Install `rg` and reopen the terminal for speed.
- **Command failed/timed out:** its exit code/stdout/stderr become the next tool result. Approve a corrected command; increase `command_timeout_seconds` if appropriate.
- **`SEARCH text not found` / ambiguous:** ask Copilot to reread the file and return exact unique text. CWAH never approximates.
- **Scope blocked or labels a read/write:** add `--context`/config for intended reads; explicitly approve a justified outside-scope write or restart with the correct scope.
- **Conversation too long:** run `cwah context --full`, start a fresh Copilot conversation, paste it, and continue. Local session state remains authoritative.
- **Dirty Git tree:** CWAH snapshots initial status/diff and never reverts. Commit/stash only if *you* choose; inspect `cwah changes` carefully.
- **Windows PATH:** use `where.exe python`, `where.exe git`, `where.exe cwah`; reopen PowerShell after installation or invoke `.venv\Scripts\cwah.exe` directly.
