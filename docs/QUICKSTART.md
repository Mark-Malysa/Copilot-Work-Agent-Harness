# Quickstart

1. Install Python 3.11+, Git, and optionally uv. Clone CWAH and run `uv sync` (or `python -m pip install .`).
2. Enter the **target** Git repository and run `cwah doctor`.
3. Run `cwah start . --scope path/to/component`. Enter a concrete task; mention design/test files by path.
4. CWAH copies its initial prompt. Paste it into the normal Microsoft Copilot chat application.
5. Copy the entire Copilot response, return to the terminal, and press Enter. Approve only changes and commands you understand.
6. Repeat until `Task complete`; inspect `cwah status` and `cwah changes`.

Clipboard unavailable? Save Copilot's whole response as UTF-8 and run `cwah ingest-response response.txt`. Try the deterministic installation check with `cwah demo`.
