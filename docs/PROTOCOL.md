# CWAH protocol v1

Users copy the **entire** rendered reply. The parser ignores everything outside the last complete outer marker pair and strips a harmless outer `json` fence.

```text
CWAH_RESPONSE_V1_START
{"status":"continue","summary":"Need source","actions":[{"id":"a1","type":"read_file","path":"src/a.py"}]}
CWAH_RESPONSE_V1_END
```

`status` is `continue` or `complete`; `summary` is concise; actions have unique caller-chosen `id` and one supported `type`. Fields are strictly validated (unknown fields/types are rejected). File actions use `path`; search/query use `query`/`pattern`; explain uses `symbol`; graph path uses `source` and `target`; commands use `command` and optional repository-relative `cwd`. `run_tests` uses configured testing command. `complete` is a control action.

## Raw payloads and edits

```text
CWAH_RESPONSE_V1_START
{"status":"continue","summary":"Fix it","actions":[{"id":"a1","type":"edit_file","path":"src/a.py","payload_id":"p1"}]}
CWAH_PAYLOAD_START p1
<<<<<<< SEARCH
exact old text
=======
replacement text
>>>>>>> REPLACE
CWAH_PAYLOAD_END p1
CWAH_RESPONSE_V1_END
```

Each create/edit payload ID must exist exactly once. Create payload is raw file content. Edit payload supports multiple blocks; each SEARCH must occur exactly once at its application step. Missing/ambiguous matches fail safely and the error is returned next iteration. Delete has no payload.

Malformed JSON, missing markers/payloads, unknown actions, or validation failure execute **nothing**. CWAH preserves the session and copies a repair prompt asking for the same intended actions. A saved whole response can be processed by `cwah ingest-response response.txt`.
