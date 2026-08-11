# Security and privacy

Every tool path is canonicalized under the repository; `..`, outside absolute paths, and symlink escapes are rejected. Primary scope is the normal write boundary; outside-scope writes are explicitly labeled and approved. Context directories expand reads. Secret-like files (`.env*`, keys, credentials, secrets), Git internals, dependencies, builds, and configured patterns are filtered from automatic context.

Normal/safe modes require write and command approval; trusted mode may allow ordinary in-scope edits in integrations, but commands still require consent. Obvious recursive deletion, disk formatting, reboot/shutdown commands are denied regardless. This is a heuristic—not OS sandboxing. Review requests, diffs, and pre-existing work. CWAH records actions/results/touched paths in `.cwah/sessions`, does not store prompt clipboard contents there, and never reverts, commits, or pushes automatically.

CWAH has no model provider/API integration. It only copies/pastes through the OS clipboard or user-provided response files, and never drives the Copilot UI, extracts cookies/tokens, or uses private endpoints. Clipboard data remains subject to OS/application behavior. CWAH does not bypass organizational security controls. Users are responsible for authorization and compliance on every machine, repository, and Copilot conversation.
