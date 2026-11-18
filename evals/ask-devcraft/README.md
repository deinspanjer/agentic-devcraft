# ask-devcraft native-host probes

Hand-run probes for the released `ask-devcraft` skill
(`plugins/agentic-devcraft/skills/ask-devcraft/`). They are not part of the Harbor harness: each
one walks a person through a real interactive session on one host and records
what they saw. The headless runs behind the harness files could not exercise an
interactive session, permission prompts, or the desktop and IDE hosts.

| Script | Host | Loads the skill from |
| --- | --- | --- |
| `probes/claude-code.sh` | Claude Code CLI | `.claude/skills/` |
| `probes/codex.sh` | Codex CLI | `.agents/skills/` |
| `probes/air.sh` | JetBrains Air in an IDE | `.agents/skills/` (the project's shared skill directory) |
| `probes/cursor.sh` | Cursor | `.cursor/skills/` |

Transcripts the scripts read, and an audit can read afterwards:

| Host | Location |
| --- | --- |
| Claude Code | `<config dir>/projects/<project slug>/<session>.jsonl`, subagents under `<session>/subagents/` |
| Codex, and Air with the Codex agent | `$CODEX_HOME/sessions/<y>/<m>/<d>/rollout-*.jsonl`, `$CODEX_HOME/archived_sessions/` |
| Cursor | `~/.cursor/projects/<project slug>/agent-transcripts/<session>/`, subagents under `subagents/` |

Run one from a terminal, with the host's session in a second window:

```bash
bash evals/ask-devcraft/probes/claude-code.sh
```

Each script creates a disposable project under the temp directory, copies the
skill and two fixture skills into it, tells you exactly what to type, and asks
for pass, fail or skip with a one-line note after each check:

- the skill loads from the project directory;
- the main session starts one subagent with fresh context;
- the worker's inventory includes `zebra-migration-probe`, a fixture that is
  explicit-only and so absent from the model's own skill list;
- inventory reads outside the project do not prompt;
- the bytes that entered the main session for one question, computed from the
  session transcript: Claude Code's project transcript, Codex rollouts under
  `sessions/` and `archived_sessions/` (where Air's Codex agent puts them) with
  children matched by `parent_thread_id`, and an estimate on Cursor, whose
  transcripts store tool calls without their results;
- a consent question that names no skill, plugin, marketplace or collection, then
  the reply continuing the same worker, with both relayed word for word;
- the inline fallback when the skill is followed inside a subagent. The script
  prints what the subagent's transcript shows: a subagent that refused, stopped or
  never read `worker.md` is a FAIL even though it started no subagent of its own.

A run with no session transcript behind it is flagged in its result file and its
bytes row is recorded as UNVERIFIED without asking for a verdict. Discard such a
file: it is a re-record, not evidence. The pass, fail and skip answers are a
person's reading of the chat. Audit them against the transcripts before citing
them; the first audit overturned several
([DEVELOPERS.md](../../DEVELOPERS.md#promotion-record)).

Results go to `~/.cache/ask-devcraft-probes/results/<host>-<timestamp>.md`; set
`RESULTS_DIR` to write elsewhere and `ASK_DEVCRAFT_SRC` to probe another copy of
the skill. A result file names local paths and may quote installed skill
names, so read it before committing one as evidence. Nothing is installed into a
host's home configuration.

The scripts are built from the `wizard` skill's `template.sh`. Everything above
the `STAGES` marker is that template unchanged; shellcheck reports SC1087 and
SC2329 there and nothing in the authored part.
