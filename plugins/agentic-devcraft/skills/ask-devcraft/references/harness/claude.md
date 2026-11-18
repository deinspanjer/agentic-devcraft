# Claude Code

Observed version: Claude Code 2.1.326, headless (`claude -p`) and one hand-run
interactive terminal session (2026-11-18). Points marked (docs) are from the
vendor documentation and were not exercised; the Desktop app was not exercised
at all.

## Launcher

Read this section only; whoever does the routing reads Inventory.

- Delegate with the `Agent` tool, `subagent_type: "general-purpose"`, once. The call returns at once with an agent ID and the report arrives later as a task notification. Do not poll, and do not read the output file the result names.
- Not `Explore` or `Plan`: they return no agent ID and cannot be continued (docs). Not a fork (`/subtask`, or an `Agent` call that inherits this conversation): the worker must start with fresh context.
- Continue the same worker with `SendMessage`: `to` is that agent ID, plus `summary` and `message`. Its reply arrives as another notification. `SendMessage` can be a deferred tool: load it with `ToolSearch` (`select:SendMessage`) first. `message` is the user's reply and nothing else.
- So the handoff's Host line reads: "Claude Code; the user invokes a skill with `/<name>`; continuation: yes, SendMessage <agent id>". Never write that the worker cannot be continued (observed: a launcher wrote that, and the worker returned a needless State block).
- The notification that hands the report back asks you to tell the user about it in your own words. That frame is not a reason to paraphrase: your reply is the worker's **Answer** or **Ask**, character for character, as the whole message. Observed 2026-11-18: three of four relays were reworded (a status dropped, a claim added, an answer turned into bullets, the closing line replaced by the launcher's own question), and the user's reply was rewritten into coaching for the worker.
- Without a `model`, a `general-purpose` subagent runs on the subagent default, which can be smaller than the session's (observed: Haiku in one session, one of whose workers skipped `index.md`). Pass `model` (`"sonnet"`, `"opus"`, `"haiku"` or `"fable"`; per Claude Code 2.1.326 itself) set to this session's model family, or `"sonnet"` when unsure.
- A subagent keeps the `Agent` tool down to three layers below the main conversation (docs; `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`), so having the tool does not mean you are the main session. Route inline when your first message was written by another agent or you are a fork (observed: a `general-purpose` subagent told to follow this skill routed inline).
- The user invokes a skill with `/<name>`, a plugin's with `/<plugin>:<name>`. A skill marked `disable-model-invocation: true` is absent from your list and the `Skill` tool refuses it; only the user can start it.
- A subagent has no `AskUserQuestion`: questions for the user come back through you.

## Inventory

- The advertised list is every skill the model may invoke. A subagent gets the same list as the main session (observed: 38 advertised, 44 registered). Skills marked `disable-model-invocation: true` are in neither.
- No command that lists registered skills from inside a session was found. Read frontmatter from the skill locations; do not open bodies:

  ```sh
  home="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
  plugins=$(claude plugin list --json 2>/dev/null | python3 -c 'import json,sys
  print(" ".join(p["installPath"]+"/skills/*/SKILL.md" for p in json.load(sys.stdin) if p.get("enabled")))')
  grep -HEm4 '^(name|description|disable-model-invocation|user-invocable):' \
    .claude/skills/*/SKILL.md "$home"/skills/*/SKILL.md "$home"/skills/synced/*/*/SKILL.md $plugins 2>/dev/null | cut -c1-420
  ```

- Locations: the project's `.claude/skills` (also in each parent directory up to the repository root); personal `$CLAUDE_CONFIG_DIR/skills`, default `~/.claude/skills`; skills synced from claude.ai under `skills/synced/`, named `anthropic-skills:<name>`; each enabled plugin's `<installPath>/skills`, named `<plugin>:<name>`. An organization's managed skills directory also loads (docs); its path was not checked.
- `disable-model-invocation: true`: installed, user-invoked only. `user-invocable: false`: the model can load it and the user cannot type it. A `skillOverrides` setting can hide a skill without touching its file (docs).
- Bundled skills (`code-review`, `simplify`, `verify`, `debug` and others) have no file. One in the advertised list is invocable; call its behaviour unverified.
- When the shell command is denied, list the same locations with `Glob` and `Grep`; headless, those reads outside the project were allowed without a prompt. Whether they prompt in an interactive session is unverified. A background subagent's permission prompts surface in the main session (docs).
