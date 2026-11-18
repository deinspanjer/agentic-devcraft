# Codex

Observed version: Codex CLI 0.169.0 and 0.170.0, headless (`codex exec`, and the
prompt rendered by `codex debug prompt-input`) and one hand-run interactive
session; 0.166.0 as the Codex agent of JetBrains Air. Points marked (docs) are
from the vendor documentation and were not exercised; the Desktop app was not
exercised at all.

## Launcher

Read this section only; whoever does the routing reads Inventory.

- Delegate with `spawn_agent`, once: a `task_name`, the handoff as `message`, and `fork_turns: "none"`. The default, `all`, copies this whole conversation into the worker. The call returns the worker's task name (`/root/<task_name>`).
- Wait with one `wait_agent` call and a long timeout: it wakes when the worker reports, so short polls buy nothing. The worker's final answer arrives as a message from that task name.
- Continue the same worker with `followup_task` and that task name as `target`. Not `send_message`, which queues text without starting a turn. A session with no `followup_task` (the older multi-agent tools) was not exercised: start a new worker from the returned `State` there.
- The agent tools can be deferred or switched off (`[agents] enabled = false`). Search your tool list before concluding there are none, then route inline.
- A spawned agent has `spawn_agent` too, so having the tool does not mean you are the main session. You are a worker when you were given a task name below `/root`: route inline (observed: a spawned agent told to follow this skill routed inline). A request that names this skill or its file is the explicit invocation, so being explicit-only is no reason to decline as a worker (observed twice on 2026-11-18, before `SKILL.md` said so: a spawned agent read the file, answered that the skill "requires the user to invoke it explicitly" and stopped).
- The user invokes a skill with `$<name>` or the `/skills` picker, a plugin's with `$<plugin>:<name>`. Codex ignores `disable-model-invocation`; a skill is explicit-only when its `agents/openai.yaml` sets `policy.allow_implicit_invocation: false`, and then it is absent from your list.
- A spawned agent has no tool for asking the user: questions come back through you.
- So the handoff's Host line reads: "Codex; the user invokes a skill with `$<name>`; continuation: yes, followup_task <task name>".
- Relay the worker's **Answer** or **Ask** verbatim, as a Markdown quote (`> ` on each line), with nothing condensed, reworded or dropped; the quote is the whole message. A condensed relay was observed to lose "not installed here" and the closing line.

## Inventory

- The advertised list is the `## Skills` block in your context: a `Skill roots` table (`r0`, `r1`, ...) and one line per skill with its file under a root. A spawned agent gets the same block (observed: 64 entries in both). It leaves out explicit-only skills and skills disabled in configuration, and it shortens or drops entries when the list outgrows its budget (docs).
- The roots table is the authority for what is loaded: the plugin cache also holds versions and plugins that are not enabled. For each root in your own table, read frontmatter and the invocation policy; do not open bodies:

  ```sh
  for root in <each root from the table>; do
    find "$root" -name SKILL.md -maxdepth 4 | while read -r f; do
      printf '%s | %s | ' "$f" "$(grep -hs allow_implicit_invocation "$(dirname "$f")/agents/openai.yaml")"
      grep -Em2 '^(name|description):' "$f" | cut -c1-320 | tr '\n' ' '; echo
    done
  done
  ```

- A skill with `allow_implicit_invocation: false` is installed and user-invoked only (observed: a plugin skill with that setting was under a listed root and absent from the list).
- `[[skills.config]]` entries with `enabled = false` in `$CODEX_HOME/config.toml` (default `~/.codex`), matched by `name` or `path`, disable a skill: report it as installed but not exposed.
- Without a roots table, the locations are `$CODEX_HOME/skills`, `~/.agents/skills`, `.agents/skills` in the working directory and each parent up to the repository root, `/etc/codex/skills`, and `$CODEX_HOME/plugins/cache/<marketplace>/<plugin>/<version>/skills`.
- Plugin skills are named `<plugin>:<name>`. The same name can appear under two roots; both load, so tell copies apart by path and description.
