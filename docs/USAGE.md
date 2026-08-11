# CLI usage

- `cwah doctor [REPO]`: Python, Git/repository, clipboard, Graphify, ripgrep, scope, directory.
- `cwah start [REPO] [--scope DIR] [--context DIR ...] [--task TEXT] [--no-wait]`: create/persist a session, build/copy initial context, and normally run the clipboard loop. `--no-wait` only prepares the prompt.
- `cwah ingest-response FILE [--repo REPO]`: process a UTF-8 saved Copilot response for the latest session.
- `cwah index [REPO] [--scope DIR]`: invoke optional Graphify `index SCOPE --code-only`; otherwise report fallback.
- `cwah status [REPO]`: latest persisted session summary.
- `cwah changes [REPO]`: current Git diff (CWAH never commits/pushes).
- `cwah sessions [REPO]`: list resumable sessions.
- `cwah resume ID [REPO]`: validate/display a persisted session and handoff guidance.
- `cwah context [REPO] [--full]`: print current selected context; `--full` regenerates a fresh-conversation handoff including protocol instructions.
- `cwah demo`: deterministic temporary Git repository using the real parser, tools, sessions, command runner, and agent loop.

Repository `.cwah.toml` supplies defaults; CLI scope/context override them. Run `cwah COMMAND --help` for generated option syntax.
