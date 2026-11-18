# Ponytail (DietrichGebert/ponytail)
Source: https://github.com/DietrichGebert/ponytail @ 96608e078b2d5ea607c5c3b8b5a54d1c1fba6846
Distribution (DietrichGebert/ponytail): one collection, the plugin `ponytail` 5.3.3 (marketplace `ponytail`, in the repository). Its INSTALL.md gives a route per host: Claude Code (`/plugin marketplace add DietrichGebert/ponytail`, then `/plugin install ponytail@ponytail`, as two separate prompts), Codex (`codex plugin marketplace add DietrichGebert/ponytail`, `codex plugin add ponytail@ponytail`, then trust its two hooks in `/hooks`), OpenCode (`opencode plugin add @dietrichgebert/ponytail`), plus Copilot CLI, Gemini CLI, Pi, Hermes, Devin, Qoder, Kimi, Grok Build and others. For the six skills alone: `npx skills add DietrichGebert/ponytail` (no hooks, no always-on ruleset). Skill directories are `skills/<skill>/`. The README says to install only from `DietrichGebert/ponytail` or npm `@dietrichgebert/ponytail`.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Read from a shallow clone; no script was run and no host was observed, so there are no availability lines. Host claims below are the repository's own.

## Family: ponytail
- source repo: https://github.com/DietrichGebert/ponytail (single author, MIT; skills in `skills/`, six skills)
- manifest notes: manifests for Claude Code (`.claude-plugin`), Codex (`.codex-plugin`; marketplace policy installation AVAILABLE, authentication ON_INSTALL), Copilot CLI, Gemini CLI, Devin, Qoder, Kimi, Hermes, Pi and an OpenCode npm plugin; rule files for Cursor, Windsurf, Cline, Kiro and Copilot Chat; a compact ruleset in `AGENTS.md`. No MCP server or app connector. `.openclaw/skills/` holds the same six names with different, shorter descriptions: match an installed copy by description. The plugins run `node` hooks (SessionStart, SubagentStart, UserPromptSubmit); without `node` on PATH each hook call errors but the skills still work.
- mode: `ponytail` is a persistent session mode, not a one-shot. With the plugin or hooks it is on from session start at `full` (default from `PONYTAIL_DEFAULT_MODE`, then `~/.config/ponytail/config.json`, then `full`), re-injected each turn and into subagents, and `/ponytail lite|full|ultra|off` switches it. Installed as skills only, nothing re-injects it; hosts without hooks (Goose, Kimi, Antigravity) do not persist the level. The other five skills are one-shot reports or displays.
- router: none. `ponytail-help` is a reference card for this collection's levels, commands and config; it routes nothing.
- development distance: core-dev
- disclosure recommendation: simple. Six skills, no router; they fit one catalog file.
- name collisions: none with another curated source. `ponytail-help` is this collection's card, not pstack's `poteto-help` (a router over pstack skills).
- vs neighbours: `ponytail` is an active mode: it changes how code is written for the rest of the session and ends each reply with what was skipped. pstack's `principle-*` leaves are one rule each, user-invoked, loaded for later work. `ponytail-review` and `ponytail-audit` judge existing code and edit nothing; `deslop` edits a diff.
- familiarity: per whole repository (one author); any installed skill whose description matches a record below makes the collection familiar.

### ponytail
- id: ponytail:ponytail; source path: skills/ponytail/SKILL.md
- description: "Lazy senior dev mode: the smallest change that fully solves the task, and a reply a busy human understands in one read. Use on any coding task (writing, fixing, refactoring, reviewing, choosing dependencies) and when the user says "ponytail", "be lazy", "simplest solution", "yagni", or complains about over-engineering or bloat. Levels: lite, full (default), ultra."
- use when: The agent builds more than asked (layers, options, new dependencies, "for later" code) and you want that held off for the whole session, or you want the smallest complete change on a coding task. Walks a ladder (needs to exist? already in the codebase? stdlib or platform? installed dependency? one line? minimum code), reads callers first, finishes the tests and fixtures its change breaks, leaves one small test for new non-trivial logic, marks known limits as `shortcut: <limit>, <when to upgrade>` comments, and ends the reply with what was skipped and any risk. Levels: `lite` (names the smaller option, you pick), `full` (default), `ultra` (also pushes back on parts of the request the need does not justify). Never cuts trust-boundary validation, data-loss error handling, security or accessibility.
- not for: fixing code already written (it shapes new work; `ponytail-review` or `ponytail-audit` judge existing code; `deslop` in cursor-team-kit cleans a diff's comments and guards); one rule loaded for a single refactor (`principle-laziness-protocol`, `principle-subtract-before-you-add`, `principle-minimize-reader-load` in pstack are passive, user-invoked leaves, not a mode); test-first process (`tdd` or `test-driven-development`: it asks for one small test after the logic, not before); work where the user wants the larger design built as asked (say "stop ponytail", or use `lite`).
- needs: nothing for the instructions. Persistence across turns and new sessions needs the plugin, hooks or rules file for the host (see the family `mode` line); the hooks need `node`. Not user-invoked only: its description invites the model to apply it on any coding task, so it may load without being asked.
- side effects: edits project code like any coding task, and adds `shortcut:` comments and small tests. The plugin writes a mode flag (`~/.claude/.ponytail-active`) and `~/.config/ponytail/config.json`, may nudge once to add a `statusLine` entry to `~/.claude/settings.json` (a prompt to the agent, to be accepted), and in Claude Code can write a per-task cost and token ledger to `~/.config/ponytail/band/<project>.csv` (default on). ⚠ An optional webhook URL, empty by default, sends each task row to that address.
- part of: the core skill of ponytail; its levels and rules also ship as `AGENTS.md` and per-agent rule files.

### ponytail-review
- id: ponytail:ponytail-review; source path: skills/ponytail-review/SKILL.md
- description: "Quality review of a change: is the logic right, is it safe, does it hold under real load, is risky code tested, is it fast enough, and is every line needed. Reads the connected code, not only the diff. Each finding is explained in plain English. Use for "review this", "code review", "review the last commit", "review my PR", "is this over-engineered", /ponytail-review."
- use when: A diff, branch, PR or last commit needs a review that puts correctness first and checks leanness last: bugs, security, scale, missing tests, speed, then code to delete, reuse or merge. It reads callers of every changed function and the tests, assumes a load from the repo, and ranks findings Must fix, Should fix, Nice to have, each with what it is, the problem, a fix and what happens if skipped, then a verdict. Names the target in plain words (`uncommitted`, `staged`, `branch`, a PR link); with none, the uncommitted changes or the last commit. Reports only.
- not for: checking the change against an issue or spec (`code-review` in mattpocock-skills has a spec axis and a fixed point, and runs two sub-agents); a strict structure verdict or paired bug and maintainability passes (`thermos`, `thermo-nuclear-review` in cursor/plugins); reviewing then fixing (`review-and-ship` in cursor-team-kit); fixing the code (it edits nothing; `deslop` edits). A bare "review this" may also match other installed review skills, so pick by what you want back.
- needs: a diff or named files and read access to the code around them; no CLIs or credentials beyond reading a PR link, if given.
- side effects: none; read-only. Lists findings and changes no code.
- part of: reports on code that `ponytail` shapes; also runs without it.

### ponytail-audit
- id: ponytail:ponytail-audit; source path: skills/ponytail-audit/SKILL.md
- description: "Quality audit of a whole repo: bugs, security holes, what breaks under real load, risky code without tests, slow paths, and what to delete, merge or split. Ranked, each finding explained in plain English. One-shot report, changes nothing. Use for "audit this codebase", "review the whole repo", "find bloat", "what can I delete", /ponytail-audit."
- use when: An inherited or unfamiliar repo, a folder or a package needs a ranked "what to fix first" list covering the same checks as `ponytail-review`. It maps first (README, deploy config, entry points, tests, expected load), traces the main flows, goes deep where a mistake costs most and says what it did not read; up to 20 numbered findings, a verdict and a lean count (lines and dependencies that could go).
- not for: a single change (`ponytail-review`); security-only scanning with finding triage (`security-scan` in codex-security); finding structural deepening candidates to redesign (`improve-codebase-architecture` in mattpocock-skills); making the deletions, since it reports only.
- needs: read access to the repo; time proportional to its size, which it spends on the highest-risk paths.
- side effects: none; read-only. One-shot report.
- part of: the repo-wide counterpart of `ponytail-review`.

### ponytail-debt
- id: ponytail:ponytail-debt; source path: skills/ponytail-debt/SKILL.md
- description: "List every `shortcut:` comment (and older `ponytail:` ones) as a debt ledger. One-shot report, changes nothing. Use for "ponytail debt", "what did ponytail defer", "list the shortcuts", /ponytail-debt."
- use when: Code written under `ponytail` left `shortcut: <limit>, <when to upgrade>` comments and you want them collected: one row per marker with its ceiling and upgrade trigger, markers with no trigger tagged `no-trigger`, and a count. Pass your own marker word (`/ponytail-debt TODO`) to ledger that instead; it can write the ledger to a file such as `PONYTAIL-DEBT.md` when asked.
- not for: finding bugs or bloat in code (`ponytail-review`, `ponytail-audit`); tracking issues or tickets (`triage` in mattpocock-skills). It is only as good as the comments: a repo that never used the `shortcut:` convention gives an empty ledger.
- needs: `git` (it runs `git grep`) or a plain grep over the tree.
- side effects: none by default; read-only. Writes the ledger file only on request.
- part of: companion to `ponytail`, which writes the markers.

### ponytail-gain
- id: ponytail:ponytail-gain; source path: skills/ponytail-gain/SKILL.md
- description: "Show ponytail's measured savings (code, cost, speed) from the benchmark. One-shot display. Use for /ponytail-gain, "what does ponytail save", "ponytail impact"."
- use when: You want the published benchmark scoreboard (39 tasks, 5 runs, Opus 5.5: lines of code 47% of the no-skill baseline, output tokens 55%, cost 74%, time 59%) and a pointer to `ponytail-debt` and `ponytail-audit`. The figures are the author's own benchmark, not an independent result.
- not for: savings in this repo (it refuses to print a per-repo number, since the unbuilt version never existed); judging or reviewing code. Marketing display; no development task depends on it.
- needs: nothing.
- side effects: none; one-shot display, changes no mode.
- part of: standalone display for the collection.

### ponytail-help
- id: ponytail:ponytail-help; source path: skills/ponytail-help/SKILL.md
- description: "Quick reference for ponytail levels, skills and commands. One-shot display. Use for /ponytail-help, "ponytail help", "how do I use ponytail"."
- use when: A question about Ponytail itself: its levels (`lite`, `full`, `ultra`), the six skills, how to stop it ("stop ponytail", "normal mode", `/ponytail off`), the default-mode env var and config file, the Claude Code band, and how to update the plugin.
- not for: choosing a skill (`poteto-help` in pstack covers pstack skills only, and this card covers Ponytail only; for any other collection use the index); starting Ponytail work.
- needs: nothing; Codex invokes skills as `$ponytail:<skill>`, Claude Code and OpenCode as slash commands.
- side effects: none; one-shot display, writes no flag file and changes no mode.
- part of: reference card for the collection; it routes nothing.
