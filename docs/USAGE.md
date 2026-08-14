# CLI usage

- `cwah doctor [REPO] [--scope DIR]`: environment checks plus invocation, workspace, scope, current worktree/common Git directory, branch, and file counts.
- `cwah workspace [REPO] [--scope DIR]`: diagnose workspace/Git boundaries, counts, and the first 20 visible files without starting a session.
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

`REPO` is the workspace boundary, not shorthand for Git's top-level directory. Paths supplied
with either Windows (`src\\ingestion`) or POSIX (`src/ingestion`) separators have the same
repository-style representation. Scope is relative to this explicit workspace. CWAH asks Git
separately for the checked-out worktree and common directory and never changes branches.
