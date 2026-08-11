# Graphify

Graphify is an **optional external CLI** used only for navigation/retrieval: queries, symbol explanations, paths, and scoped indexing. CWAH uses its results to choose authoritative source snippets; it never pastes a giant graph wholesale.

Install Graphify from its current upstream documentation (syntax/version varies), place it on PATH, and verify `graphify --version` then `cwah doctor`. `cwah index . --scope src` invokes `graphify index src --code-only`. CWAH's adapter contains version-sensitive invocation and converts failures/timeouts into tool results instead of crashing.

Only use CODE-ONLY / LOCAL Graphify operation. Do not configure external LLM enrichment or ingestion of documentation/PDFs/images. Disable it with `[graphify] enabled = false` in `.cwah.toml`. When absent/disabled/failing, CWAH uses Git listing, explicit references, ripgrep, or Python search. If stale, rerun `cwah index`; inspect the Graphify output and its upstream version-specific help.
