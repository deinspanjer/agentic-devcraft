# Subject smoke matrix — 2026-08-21

Harbor 0.21.0 ran each subject in a disposable Docker container. A pass requires setup provenance, host discovery, and actual skill use; installation alone cannot pass.

| Subject | Codex 0.149.0 / gpt-5.6-sol | Claude Code 2.1.239 / claude-sonnet-4-6 |
|---|---|---|
| Devcraft Status | Passed (2/2) | Passed (2/2) |
| Superpowers | Passed | Passed |
| GSD | Passed | Passed |
| Pocock Skills | Passed | Passed |
| OpenSpec | Passed | Passed |
| Spec Kit | Passed | Passed |

All supported rows completed setup, discovery, and use. No declared combination is unsupported.

This matrix establishes host compatibility only. It does not measure whether a
toolkit or skill improves engineering outcomes. Authenticated subject trials use
Harbor's fail-closed network capability probe and stop when the selected Docker
backend cannot enforce the declared policy.
