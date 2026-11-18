# Agentic Devcraft
Source: https://github.com/deinspanjer/agentic-devcraft @ a3a7f4169d0efaca06d864941593b36166c403e7
Distribution (agentic-devcraft): one collection. Claude Code and Codex: plugin `agentic-devcraft@agentic-devcraft`, with the repository as the marketplace. OpenCode: the skill catalog `https://deinspanjer.github.io/agentic-devcraft/opencode/skills/`, added to the `skills` array of `opencode.json`. Released skill directories are `plugins/agentic-devcraft/skills/<skill>/`; the repository's USERS.md has the commands.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Curated 2026-11-17 at plugin 0.4.0. The uncommitted working-tree changes at that commit are docs only. `ask-devcraft` itself is released (`plugins/agentic-devcraft/skills/ask-devcraft/`) and needs no record here; the Source pin is bumped to the release commit when one exists. Released skills come first; unreleased candidates are in their own section at the end. Agentic Devcraft is always a familiar collection, because ask-devcraft is itself a Devcraft skill: a released skill that is not installed is named directly with its install prerequisites, and an unreleased candidate is never recommended unless the inventory already lists it as installed.

## Family: agentic-devcraft
- source repo: https://github.com/deinspanjer/agentic-devcraft (released skills in `plugins/agentic-devcraft/skills/`; unreleased candidates in `proposals/skills/`)
- manifest notes: Claude Code plugin and Codex plugin, both 0.4.0 ("Composable development-workflow skills"); Codex marketplace policy installation AVAILABLE, authentication ON_INSTALL. No MCP server, app connector, hook, command, subagent or Cursor manifest. OpenCode and Air load the skill directories directly (no plugin manifest); on OpenCode every released skill is on-call (`opencode/autoinvoke: false`). Candidates ship in no distribution and may be auto-selected if a host loads the checkout. No skill needs credentials; python3 3.9+ for two of them.
- router: none. No skill sequences the others; the only cross-reference is `documentation-pattern-refactor` to `agent-instructions-cleanup`. Three candidates explicitly preserve the active workflow; `evidence-before-complexity` is a scope guard.
- development distance: core-dev (agent-instruction and docs maintenance, review and planning discipline, agent-session evidence)
- disclosure recommendation: simple. Eight records (4 released skills, 4 candidates; ask-devcraft itself needs none), no router; they fit one source catalog without a separate disclosure file.

### status
- id: agentic-devcraft:status; status: released (plugin 0.4.0); source path: plugins/agentic-devcraft/skills/status/SKILL.md
- description: "Report the loaded Agentic Devcraft status skill's version, provenance, and plugin state when asked about this installation or its version."
- use when: A question about this Devcraft installation: which version is loaded, where it came from, whether the plugin is active.
- not for: A skill inventory or what else is installed (use the host's own skill list); it reports nothing about the project.
- needs: nothing beyond `release.json` beside it or the plugin manifest of the package it loaded from; no network. Generic name: in OpenCode it can collide with another source's `status`, so identify the copy by source.
- side effects: none; read-only (fixed five-line report, never checks for updates).
- part of: standalone.

### capture-agent-issue
- id: agentic-devcraft:capture-agent-issue; status: released (plugin 0.4.0); source path: plugins/agentic-devcraft/skills/capture-agent-issue/SKILL.md
- description: "Capture a local agent issue packet for skill tuning and experiments. Only run when the user explicitly invokes capture-agent-issue."
- use when: "The agent just did something wrong or unexpected and I want it recorded as evidence for skill tuning." Explicit invocation only.
- not for: fixing the task, reviewing code, or proposing environment changes (`retro` in mattpocock-skills proposes those); it only records evidence.
- needs: readable records of the subject session (Claude `~/.claude/projects`, Codex `~/.codex/sessions` + `CODEX_THREAD_ID`, OpenCode `opencode api` + `OPENCODE_SESSION_ID` + the `subagent` tool); python3 3.9+. User-invoked only on every harness.
- side effects: prepares a private host-temp draft and saves one Markdown packet, de-identified by default, to `<host-temp>/agent-issues/...` unless the user supplies `--output`; never overwrites. Publishes, uploads and commits nothing.
- part of: standalone; delegates once to a fresh-context worker in an ordinary session.

### agent-instructions-cleanup
- id: agentic-devcraft:agent-instructions-cleanup; status: released (plugin 0.4.0); source path: plugins/agentic-devcraft/skills/agent-instructions-cleanup/SKILL.md
- description: "This skill should be used when refactoring AGENTS.md / AGENTS.override.md across a project tree to enforce progressive disclosure while preserving all guidance via mandatory migration into other docs and a structured preservation map/report."
- use when: "AGENTS.md is too big to navigate; restructure our agent instructions across the repo without losing any rule." It relocates guidance into the right docs and never deletes a rule.
- not for: pruning: cutting obsolete, duplicated or no-op rules. Its "no orphaned guidance" rule migrates every removed line, so the bloat moves; for a cut use the Pruning section of `writing-for-agents` or `retro`, both in mattpocock-skills. Also `documentation-pattern-refactor` (README/USERS/DEVELOPERS/TODO layout; it audits AGENTS issues but never edits those files); `writing-for-agents` in mattpocock-skills is wording guidance, not a migration.
- needs: a repo tree with AGENTS.md / AGENTS.override.md; the target harnesses that will read them (Codex per-level override vs OpenCode nearest-to-root); no CLIs or credentials.
- side effects: deliberately cautious (mandatory preservation map, dated mirror, approval before any in-place edit): writes a dated proposal mirror, `report.md` and `index.md` under `docs/agents-refactor/YYYY-MM-DD/`; no in-place edit until approved.
- part of: standalone; receives referrals from `documentation-pattern-refactor`.

### documentation-pattern-refactor
- id: agentic-devcraft:documentation-pattern-refactor; status: released (plugin 0.4.0); source path: plugins/agentic-devcraft/skills/documentation-pattern-refactor/SKILL.md
- description: "Establish and enforce an audience-based documentation layout with README/USERS/DEVELOPERS/TODO rules, classify existing content into those domains, report structural and domain mismatches, and execute audit/scaffolding/restructuring refactors with explicit confirmation gates."
- use when: "Is our README/USERS/DEVELOPERS/TODO split right?" Docs are misplaced or duplicated, or the audience-based layout needs scaffolding.
- not for: `agent-instructions-cleanup` for AGENTS.md changes; the four candidate disciplines are overlays, not alternatives.
- needs: python3 for its bundled scripts; a target workspace; Git optional (offers a `git stash push -u` snapshot). Confirms level (audit/scaffolding/restructuring) and scope (root/all) first.
- side effects: writes audit artifacts to `<workspace>/.agents/artifacts/doc-pattern` even at audit level; scaffolding and restructuring edit docs only after confirmation. Deliberately cautious: confirmation gates and an offered stash snapshot.
- part of: standalone; its own audit, plan, execute flow; hands AGENTS.md work to `agent-instructions-cleanup`.

## Unreleased candidates

These four live in `proposals/skills/` and ship in no distribution, so no plugin, marketplace or catalog install brings them. A session has one only if its host loads the checkout directory, where it may be selected automatically.

Never recommend one to a user as something to get: they exist for this repository's own evaluation. The records below identify a candidate that the session's inventory already lists.

### cold-read
- id: agentic-devcraft:cold-read; status: candidate (unreleased); source path: proposals/skills/cold-read/SKILL.md
- description: "Verify load-bearing repository facts before accepting or revising a plan, review, or design decision. Use inside the user's active workflow without replacing it."
- use when: A plan, review or design decision rests on repository facts nobody re-checked; verify them from primary sources before accepting or revising it.
- not for: `review-integrity` sets the bar for review findings (and requires a cold read); `decision-evolution` tracks how decisions change, not whether facts are true.
- needs: read access to the repo. Unreleased: available only if a host loads the checkout directory; may be selected automatically.
- side effects: none; read-only.
- part of: overlay inside the user's active workflow; run alongside, never as a replacement.

### decision-evolution
- id: agentic-devcraft:decision-evolution; status: candidate (unreleased); source path: proposals/skills/decision-evolution/SKILL.md
- description: "Track how decisions change when their evidence, constraints, or assumptions change. Use within the active planning or specification workflow without replacing it."
- use when: During planning or spec work, new evidence or a changed constraint undercuts an earlier decision and the record should show it as superseded.
- not for: `cold-read` checks whether the facts under a decision are true; this one records how the decision changed.
- needs: material decisions and their evidence/constraints; preserve the active planning/spec artifact format when recording changes. Unreleased: available only if a host loads the checkout directory.
- side effects: edits the existing plan/spec artifact (marks old decision superseded, adds replacement).
- part of: overlay inside the active planning/spec workflow.

### evidence-before-complexity
- id: agentic-devcraft:evidence-before-complexity; status: candidate (unreleased); source path: proposals/skills/evidence-before-complexity/SKILL.md
- description: "Check whether added machinery is needed and keep one-time requests scoped before expanding a change."
- use when: The agent is about to add a mode, gate or workflow beyond what was asked, a one-time review request is growing, or the process outweighs a small change; it matches the process to the size of the work and checks the need first.
- not for: `review-integrity`, `cold-read` and `decision-evolution` govern evidence quality; this one governs scope.
- needs: nothing. Unreleased: available only if a host loads the checkout directory. States no overlay clause, so it reads as a standalone guard.
- side effects: none; read-only. Asks the user only before a scope expansion that is hard to reverse.
- part of: standalone behavioural guard.

### review-integrity
- id: agentic-devcraft:review-integrity; status: candidate (unreleased); source path: proposals/skills/review-integrity/SKILL.md
- description: "Apply evidence rules when reviewing code, plans, or specifications, including inside another active workflow. Preserve the chosen workflow and its output format."
- use when: Reviewing code, plans or specs, especially with a requested number of findings or a persona/seniority framing; keep one evidence bar.
- not for: `cold-read` for a plan or decision resting on repo facts rather than a review; `evidence-before-complexity` for scope.
- needs: read access to the code or plan under review. Unreleased: available only if a host loads the checkout directory.
- side effects: none; read-only.
- part of: overlay inside another active review workflow; keeps its output format.
