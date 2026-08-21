---
name: status
description: Report whether Agentic Devcraft is active and identify its packaged version when asked about this plugin's installation or version.
---

# Agentic Devcraft Status

The presence of this skill means Agentic Devcraft is active.

Resolve the plugin root by ascending two directories from this skill directory. Read the host manifest there:

- `.codex-plugin/plugin.json`: report its `version`.
- `.claude-plugin/plugin.json`: report its `version` when present; otherwise report `commit-versioned development build`.

Return one line: `Agentic Devcraft: active (<version>)`.

This check is read-only. Do not update, install, remove, or use the network.
