# Examples

## 1. Fix a failing unit test

Run `cwah start . --scope src --task "Fix this failing unit test: tests/test_total.py"`. Iteration 1 Copilot requests the explicit test and implementation. CWAH reads them. Iteration 2 requests an exact SEARCH/REPLACE; you approve. Iteration 3 requests `run_tests`; approve the displayed command/cwd. Copilot analyzes output, corrects any failure, reruns, then returns complete. Review `cwah changes`.

## 2. Documentation-led ingestion pipeline

`cwah start . --scope src/ingestion --context docs` and task `Based on docs/ingestion-design.md implement the ingestion pipeline.` CWAH extracts/inserts the document first, maps scoped source/tests, and includes bounded snippets. Copilot requests missing contracts, creates pipeline/tests with raw payloads, runs configured tests, inspects failures, edits exact text, reruns, and completes.

## 3. Large payments monorepo

```powershell
cwah start . --scope backend/payments --context backend/common
# Task: Fix duplicate payment processing and add regression tests.
```

Iteration 1: exact search/optional graph query identifies payment handler and idempotency store. Iteration 2: read-only requests inspect those files and related tests; an outside-scope request is visible. Iteration 3: Copilot proposes grouped handler/test edits; approve after reviewing paths. Iteration 4: approve a targeted test command; its failure (for example, race setup) is returned verbatim. Iteration 5: Copilot rereads and makes a unique second replacement. Iteration 6: tests pass, Copilot returns `complete`, and CWAH prints completion. Use `cwah status` and `cwah changes`; commit manually.
