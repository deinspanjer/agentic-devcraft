# OpenCode

Observed version: OpenCode 2.3.0.

## Launcher

Read this section only; whoever does the routing reads Inventory.

- Delegate with the `subagent` tool, agent `general`, once. It runs in the background: the call returns a `sessionID` and the result arrives as a `<subagent>` message. Do not poll or sleep.
- Continue the same worker by calling `subagent` again with that `sessionID` and the user's reply.
- A session with a `parentID` is itself a subagent and has no `subagent` tool (nesting depth is one): route inline.
- The user invokes a skill with `@<id>`. Skills marked `opencode/autoinvoke: false` or `disable-model-invocation: true` are loadable by the user but absent from your advertised list.

## Inventory

- The advertised list in a session is the permitted skills that have a description and are not on-call. Where most installed skills are on-call, that list is a small part of the inventory (observed: 5 advertised of 71 registered).
- Registered skills: `opencode api skill.list` returns every registered skill with its full content. Never print it raw. Keep `id`, `description`, `autoinvoke` and `path`:

  ```sh
  opencode api skill.list | python3 -c 'import json,sys
  for s in json.load(sys.stdin)["data"]: print(s["id"], "|", s.get("autoinvoke"), "|", s["path"], "|", (s.get("description") or "")[:300])'
  ```

- `autoinvoke` of `False` is an on-call skill: the user can invoke it, the model is not offered it.
- A `path` starting `skill://` is a built-in with no file. Its text is that entry's `content` field; without reading it, call the skill's behaviour unverified.
- Without that command, read the frontmatter of each `SKILL.md` under the configured locations: `~/.config/opencode/skills`, `~/.agents/skills`, `~/.claude/skills`, the project's `.opencode/skills`, `.agents/skills` and `.claude/skills`, and the directories in the `skills` array of `opencode.json`.
- A `skill` permission rule with effect `deny` makes a registered skill unloadable. `opencode api agent.get --param agentID=<agent>` shows the rules; the last matching rule wins. Report such a skill as installed but not exposed.
