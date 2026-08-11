# Architecture

```mermaid
flowchart TD
 CLI --> Session[JSON session store]
 CLI --> Context[budgeted hybrid context]
 Context --> Git
 Context --> Search[rg/Python]
 Context --> Graph[optional Graphify adapter]
 CLI --> Clipboard
 Clipboard --> Parser[Pydantic protocol parser]
 Parser --> Registry[tool registry]
 Registry --> Paths[path/scope security]
 Registry --> Edits[exact edit engine]
 Registry --> Commands[command runner]
 Registry --> Git
 Registry --> Session
```

`config.py` loads typed `.cwah.toml`. `context/` discovers Git-visible files, explicit natural-language paths, snippets, filters, and budget omissions without wholesale reads. `protocol/` separates small validated JSON from raw payloads and builds full/follow-up/repair prompts. `security/` canonicalizes boundaries and filters secrets. `tools/` implements local reads/search/Git/Graphify, exact edits, creation/deletion, and captured commands. `agent/` persists state and drives identical real and scripted response processing. `transport/` isolates system and memory clipboards.

```mermaid
sequenceDiagram
 participant H as Human
 participant C as CWAH
 participant M as Copilot chat
 C->>C: map, select, persist
 C->>H: copy initial prompt
 H->>M: paste
 M->>H: marked response
 H->>C: copy whole response + Enter
 C->>C: parse, validate, approve, execute
 C->>H: copy compact results
```

Large-repo performance comes from Git metadata, capped maps, targeted reads/search and a character budget—not embeddings, databases, services, or repository-wide ingestion.
