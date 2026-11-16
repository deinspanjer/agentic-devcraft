---
name: status
description: Report the loaded Agentic Devcraft status skill's version, provenance, and plugin state when asked about this installation or its version.
metadata:
  opencode/autoinvoke: false
---

# Agentic Devcraft Status

Loading this skill shows only that this skill is available. It does not show that
a plugin is installed or enabled.

Use only files inside this installation. Never use a manifest from another
installation, another client's home or cache, or the current project checkout
unless this skill was loaded from that checkout.

## Version evidence

1. `release.json` beside this `SKILL.md`. It is valid when it is a JSON object with
   `schema` equal to `agentic-devcraft-skill-release/v1`, `skill` equal to `status`,
   and non-empty `version`, `repository`, `source_path`, and `revision`. An invalid
   or unreadable file is not evidence; say it was invalid.
2. Package manifests, only when this skill directory is `<root>/skills/status` and
   `<root>` holds `.codex-plugin/plugin.json` or `.claude-plugin/plugin.json` whose
   `name` is `agentic-devcraft`. Read `version` from each one present. A manifest
   without `version` gives no version.

Decide:

- All versions found agree: report that version.
- Versions disagree: report `conflict` and list each file with its value. Do not
  pick one.
- No version found: report `unknown`. Do not invent a release or development
  version.

## Plugin state

- `active`: this harness loaded the skill under the plugin's namespace
  (`agentic-devcraft:status`), or its own plugin listing, already available without
  a network call, shows the plugin enabled.
- `not applicable`: the skill is a standalone directory with no package manifest,
  such as an OpenCode skill source or catalog installation.
- `not verified`: anything else.

## Report

```text
Agentic Devcraft status skill: loaded
Version: <version | unknown | conflict: file=value, file=value>
Source: <release record: repository@revision | package manifest: path | none>
Plugin: <active | not applicable | not verified>
Updates: not checked
```

This check is read-only. Do not update, install, remove, change configuration, or
use the network.
