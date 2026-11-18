# Cursor

Observed version: Cursor 2026.11.17 desktop app, Agent chat, Free plan, one
hand-run session on 2026-11-18 read back from its transcript. Points marked
(docs) are from the vendor documentation and were not exercised; points marked
(unobserved) are neither. The Cursor CLI and Cloud Agents were not exercised.

## Launcher

Read this section only; whoever does the routing reads Inventory.

- Delegate with the `Task` tool, once: `subagent_type: "generalPurpose"`, `model: "inherit"`, a short `description`, and the handoff as `prompt`. The tool can be a dynamic one: find it with `GetDynamicTools` (namespace `cursor`, tool `Task`) and call it with `CallDynamicTool`. The worker starts with fresh context and its report is the call's result; no polling was needed.
- Continue the same worker with a second `Task` call that adds `"resume": "<agent id>"`, with the user's reply and nothing else as `prompt`. The worker's own transcript continues, so it keeps what it read and needs no `State` block (observed once). The chat shows the second call under its new `description`, which can look like a new subagent.
- So the handoff's Host line reads: "Cursor; the user invokes a skill with `/<name>`; continuation: yes, Task resume <agent id>".
- A direct subagent can launch one more level (docs), so having `Task` does not mean you are the main session. Route inline when your first message was written by another agent (observed: a `generalPurpose` subagent told to follow this skill routed inline and made no `Task` call).
- The user invokes a skill by typing `/<name>` in Agent chat; the skill is attached to that one message and its `SKILL.md` arrives inlined. A skill marked `disable-model-invocation: true` is absent from your list and included only when the user types it (docs; observed absent).
- Whether a subagent can ask the user is unobserved: questions come back through you.
- Checking a cited line before you relay is fine (observed); the relay itself is still the worker's text unchanged.

## Inventory

- The advertised list is the available-skills block in your context. Skills marked `disable-model-invocation: true` are left out of it (observed: an explicit-only project skill was installed and absent). Whether a subagent gets the same list is unobserved: trust the handoff's copy as partial either way.
- No command that lists registered skills from inside a session was found. Read frontmatter from the skill locations; do not open bodies:

  ```sh
  grep -HEm4 '^(name|description|disable-model-invocation|paths):' \
    .cursor/skills/*/SKILL.md .agents/skills/*/SKILL.md .claude/skills/*/SKILL.md .codex/skills/*/SKILL.md \
    ~/.cursor/skills/*/SKILL.md ~/.cursor/skills-cursor/*/SKILL.md ~/.agents/skills/*/SKILL.md \
    ~/.claude/skills/*/SKILL.md ~/.codex/skills/*/SKILL.md 2>/dev/null | cut -c1-420
  ```

- Locations (docs): the project's `.cursor/skills` and `.agents/skills`, the user's `~/.cursor/skills` and `~/.agents/skills`, and for compatibility `.claude/skills`, `.codex/skills`, `~/.claude/skills` and `~/.codex/skills`. Observed: skills from the project's `.cursor/skills`, `~/.claude/skills` and `~/.codex/skills` were in the advertised list. Roots are walked recursively, so a skill can sit below a category folder, and a `.cursor/skills` deeper in the repository is scoped to its directory (docs).
- Cursor's built-in skills are files under `~/.cursor/skills-cursor` (observed; `create-rule`, `review-bugbot` and others). They are Cursor's own collection, not the user's choice of one.
- Plugin skills install through a marketplace (docs); where their files live was not checked. One in the advertised list with no file found is invocable; call its behaviour unverified.
- Cursor does not load another host's plugin cache (`~/.claude/plugins`, `~/.codex/plugins`). A skill found only there is not installed here, though it can still show which collections the user knows (observed: workers read those caches).
- `disable-model-invocation: true`: installed, user-invoked only. `paths` (or the older `globs`): offered only while the agent works with matching files (docs).
- Reads of skill directories outside the project did not prompt the user (observed once).
