# Large repositories

Choose the narrowest useful scope: `cwah start . --scope backend/payments --context backend/common --context shared/contracts`. Scope prioritizes context and bounds ordinary writes; context directories authorize supporting reads, not ordinary writes. Do not scope an entire monorepo when one service is responsible.

CWAH uses `git ls-files` (plus nonignored untracked files), a shallow capped map, task path extraction, bounded snippets, exact search, optional Graphify navigation, Git state, and session history. It does not recursively read every file. A task mentioning `docs/ingestion-design.md` includes that file first even outside scope, unless secret filtering blocks it.

`context_budget_chars` (default 45,000) is a hard selection budget with room for instructions. Large files become labeled line-range snippets; omissions are declared. Generated/ignored/secret paths are excluded. `.cwah/cache` is reserved for reusable local metadata; the MVP relies on cheap Git metadata rather than a database. Re-run `cwah index --scope backend/payments` after structural changes when Graphify is enabled.
