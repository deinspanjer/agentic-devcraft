# Cursor plugins (cursor/plugins)
Source: https://github.com/cursor/plugins @ e559e62b729e040186bc9d573e71255e5a96f50d
Distribution (cursor/plugins): the Cursor marketplace `cursor-plugins` (`.cursor-plugin/marketplace.json`); in Cursor, `/add-plugin <plugin>`. The same repository holds a Claude Code marketplace (`.claude-plugin/marketplace.json`; `/plugin marketplace add cursor/plugins`) that lists only `pstack` and `origin-apps`. Skill directories are `<plugin>/skills/<skill>/`. A "Cursor packaging only" manifest note describes packaging, not where a skill can run: the family header names the Cursor features (Task subagents, hooks, Canvas, rules) a skill depends on.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Order: core-dev families first (pstack with its Claude Code host variant `harness` (families/pstack.md), dyl-stack, then the tool plugins advisor, agent-compatibility, cli-for-agent, continual-learning, cursor-sdk, cursor-team-kit, orchestrate, origin-apps, pr-review-canvas, ralph-loop, thermos), then adjacent (create-plugin, docs-canvas, grok-voice, pstack-benny), then one-line pointers to families far from development, then cross-family notes. Most plugins ship a Cursor manifest only; each family's manifest line says which hosts it is packaged for and which Cursor features its skills depend on. Observed-host notes are one OpenCode host's snapshot from 2026-11-17.

## Family: pstack
- router: `poteto-help` (which pstack skill, setup, cost, a misbehaving run; starts no work) and `poteto-mode` (runs work under one of 22 playbooks; needs a goal plus a pass/fail check; unmatched, large or unattended work goes to `figure-it-out`). When either is installed, hand pstack routing to it. Router-delegated: the other 56 records are one-liners for matching.
- covers: Cursor's pstack plugin (v0.15.43, 58 skills): playbooks, design and review skills (`architect`, `arena`, `interrogate`), read-only advisors (`how`, `why`, `teach`), prose skills and 24 single-rule `principle-*` leaves. Cursor-first; the Claude Code variant `harness` (typed `/pstack:<name>`) is described in the full records. Every skill is explicit-invocation except `setup-pstack`. Bare `tdd` and `teach` also exist in mattpocock-skills; say which source.
- development distance: core-dev
- skills (58): `poteto-help`, `poteto-mode`, `architect`, `arena`, `automate-me`, `benchmark-checklist`, `blast-radius`, `bro`, `correct`, `create-formal-verification-skill`, `create-verification-skill`, `figure-it-out`, `how`, `in-your-own-words`, `interrogate`, `ketchup`, `ketchup-video`, `maintain-formal-verification-skill`, `maintain-verification-skill`, `make-bot-ui`, `no-comments`, `recall`, `reflect`, `setup-pstack`, `sharpen`, `show-me-your-work`, `statechart`, `swarm`, `tdd`, `teach`, `technical-writing`, `typescript-best-practices`, `unslop`, `why`, `principle-attack-the-premise`, `principle-boundary-discipline`, `principle-build-the-lever`, `principle-encode-lessons-in-structure`, `principle-exhaust-the-design-space`, `principle-experience-first`, `principle-explain-the-number`, `principle-fix-root-causes`, `principle-foundational-thinking`, `principle-guard-the-context-window`, `principle-laziness-protocol`, `principle-make-operations-idempotent`, `principle-migrate-callers-then-delete-legacy-apis`, `principle-minimize-reader-load`, `principle-model-the-domain`, `principle-never-block-on-the-human`, `principle-outcome-oriented-execution`, `principle-prove-it-works`, `principle-redesign-from-first-principles`, `principle-separate-before-serializing-shared-state`, `principle-sequence-verifiable-units`, `principle-subtract-before-you-add`, `principle-test-behavior-not-implementation`, `principle-type-system-discipline`
- Full records: families/pstack.md

## Family: dyl-stack
- source repo: https://github.com/cursor/plugins, directory `dyl-stack/` (v0.1.0, Dylan Gattey, MIT).
- plugin manifest: `.cursor-plugin/plugin.json` (`skills`, `agents`). One subagent, `dyl-agent` (background; the runner for `/dyl-mode`; substituting `generalPurpose` skips its required reads). No MCP server, hook, command or rule; no auth policy; no Codex or Claude manifest (Cursor packaging only). Depends on other plugins: pstack (detected by `setup-pstack` in the skill list), cursor-team-kit (`control-ui`, `verify-this`, `deslop`), thermos (its two review subagents), and for build-figma the Figma plugin with its MCP connected. When a required plugin is missing the relevant skill stops, names it and says `/add-plugin <name>`. All five skills except build-figma disable model invocation; wording alone does not auto-invoke those four.
- router: `dyl-mode`. Todo item 1 is reading pstack poteto-mode's Principles; then match a poteto-mode playbook, then shared triggers, then the Dylan gates, which win on conflict. Routes "get PR green" to dyl-ready-pr, "review like me" to dyl-review, a Figma URL to build-figma. Choose it over poteto-mode only for its gates (root-cause todo, The Algorithm, /bro voice, never merge without current-turn authorization).
- development distance: core-dev (build-figma is adjacent: design-to-code)
- disclosure recommendation: router-delegated. dyl-mode owns the routing for the five skills, which are a thin personal-style overlay on pstack; one-line records suffice.

### dyl-mode
- id: dyl-stack:dyl-mode (source path: dyl-stack/skills/dyl-mode/SKILL.md)
- description: "Dylan's agent style on top of pstack: concise verified delivery, root causes over symptom patches, The Algorithm before design, plain /bro replies, live UI proof, reuse/simplify, and hard merge gates. Use for Dylan, /dyl-mode, or his style. "Get PR green" → /dyl-ready-pr. "Review this PR like me" → /dyl-review. Figma URL → /build-figma."
- use when: You want Dylan's gated style on non-trivial engineering work: root-cause todo before any fix, The Algorithm before design, never merge unauthorized. Runs in the dyl-agent subagent over poteto-mode.
- needs: pstack and cursor-team-kit plugins; stops and names a missing plugin.
- side effects: commits, pushes and PRs only when asked or implied by a slash invocation.
- part of: entry router for dyl-stack; hands off to dyl-ready-pr, dyl-review, build-figma, principle-the-algorithm.

### dyl-ready-pr
- id: dyl-stack:dyl-ready-pr (source path: dyl-stack/skills/dyl-ready-pr/SKILL.md)
- description: "Get a PR merge-ready for Dylan: deep /dyl-review till 🟢, mark it ready, resolve conflicts, then babysit CI and comments. Use for /dyl-ready-pr, "get PR green", "make the PR mergeable", "/dyl-review till green then ready", or ready-to-merge asks under /dyl-mode."
- use when: You have one PR and say "get PR green": loops deep dyl-review and fixes, marks it ready, resolves conflicts, babysits CI until merge-ready; never merges. Unlike dyl-review, it acts.
- needs: pstack, cursor-team-kit, thermos, gh.
- side effects: pushes fixes to the PR branch, marks it ready, merges base in (no force-push).
- part of: step of dyl-mode; calls dyl-review as Phase 1.

### dyl-review
- id: dyl-stack:dyl-review (source path: dyl-stack/skills/dyl-review/SKILL.md)
- description: "Review one or more PRs in Dylan's style: up to 7 copy-pasteable asks and one 🟢/🟡/🔴 call. Quick by default; "deep" adds thermos and Bugbot. Use for /dyl-review, "review this PR like me", or terse design/correctness comments. Never posts to the PR."
- use when: You want a PR reviewed "like me": one 🟢/🟡/🔴 call and up to 7 pasteable asks. Quick by default; "deep" adds thermos and Bugbot. Drafts only.
- needs: pstack, gh or origin pr, and a Task/subagent tool at either depth; deep adds thermos, Bugbot and a local PR checkout.
- side effects: none to the PR; writes a diff file and launches review workers at either depth; deep may create and remove a throwaway /tmp worktree.
- part of: standalone entry; Phase 1 of dyl-ready-pr.

### principle-the-algorithm
- id: dyl-stack:principle-the-algorithm (source path: dyl-stack/skills/principle-the-algorithm/SKILL.md)
- description: "Apply to any non-trivial change before designing it. Make the requirement less dumb, delete, optimize, accelerate, automate, in that order, then run it again on the result. The reply names the requirement you questioned and what you deleted."
- use when: Before designing any non-trivial change or adding a flag, layer, retry or step: question the requirement, delete, optimize, accelerate, automate, then rerun on the result. Guidance; reached via dyl-mode.

### build-figma
- id: dyl-stack:build-figma (source path: dyl-stack/skills/build-figma/SKILL.md)
- description: "Use for "/build-figma", a figma.com/design URL with node-id, or "implement this Figma" into a web, desktop, or shared UI. Orchestrates Figma MCP intake, maps nodes to the repo's own design system, then a verify-this visual judge. Do not paste Figma Tailwind."
- use when: You paste a figma.com/design URL with node-id, or say "implement this Figma": built from the repo's own primitives and tokens, then visually judged. Refuses URLs without node-id.
- needs: Figma plugin with MCP connected, cursor-team-kit, a way to run and capture the UI.
- side effects: edits product UI code and writes /tmp/build-figma/<slug>/intake.md.

## Family: advisor
- source repo: https://github.com/cursor/plugins, path `advisor/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Ships a read-only `advisor-subagent` (default model a Grok at high effort) and hooks on afterFileEdit, afterAgentResponse, subagentStop and stop (loop_limit 3) that need Bash and `jq` (exit quietly without `jq`). State in `.cursor/advisor/`. Normal Cursor model limits apply; one advisor-model call per consult. No auth policy.
- router: none; the single skill is itself the whole sequence: resolve model, write state, consult at four checkpoints (concrete plan before a major decision; same error after two real attempts; before declaring done on logic or multi-file changes; on request), foreground advisor-subagent, act on proceed / proceed with changes / stop, report in 1-2 lines; one follow-up per checkpoint.
- development distance: core-dev
- disclosure recommendation: simple: one skill with strict opt-in semantics; the full record in the source catalog is enough.

### advisor
- id: advisor:advisor (source path: advisor/skills/advisor/SKILL.md)
- description: "Advisor mode. Consult a stronger (or different) model at key checkpoints: before major decisions, when stuck on an error, and before declaring a task done. Use when the user types /advisor, asks to turn the advisor on or off, picks an advisor model, or explicitly asks for a second opinion from a stronger or different model. Never enable it on your own."
- use when: The user types `/advisor`, turns it on or off, names an advisor model, asks for status, or explicitly wants a stronger or different model's second opinion on a plan, a stuck error, or "is this done".
- not for: `thermo-nuclear-code-quality-review` (harsh maintainability rubric, no second model); `review-and-ship` (reviews and ships; the advisor only advises).
- needs: Cursor Task subagents with per-subagent model selection; `jq` and Bash for hooks; paid model calls. A bare "second opinion" with mode off is a one-off consult (no state written, no transcript shared).
- side effects: writes `.cursor/advisor/` state and logs (never stage it; `/advisor off` deletes it); no other writes. Never enable on its own.
- part of: entry point of the advisor sequence: briefing, then `advisor-subagent`, then the main agent acts and stays accountable.

## Family: agent-compatibility
- source repo: https://github.com/cursor/plugins, path `agent-compatibility/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Ships four `model: fast` subagents (`compatibility-scan-review`, `startup-review`, `validation-review`, `docs-reliability-review`) labelled read-only yet instructed to run real setup, start and validation commands. The scanner is not bundled: it runs `npx -y agent-compatibility@latest --json <path>`.
- router: none; the single skill orchestrates: scan, startup, validation, docs reviews (one subagent each, never combined), score = round(0.7 * deterministic + 0.3 * average of startup, validation, docs), one score plus prioritized `Top fixes`. No formula is given when the scanner cannot run: say the scan gap is reported separately and the score is then not comparable.
- development distance: core-dev
- disclosure recommendation: simple: one skill.

### check-agent-compatibility
- id: agent-compatibility:check-agent-compatibility (source path: agent-compatibility/skills/check-agent-compatibility/SKILL.md)
- description: "Run the full repository compatibility pass: scanner score, startup path, validation loop, and docs reliability."
- use when: "Can an agent actually set up this repository, validate a small change, and trust its instructions?" and the user wants one readiness score with prioritized fixes.
- not for: `cli-for-agents` (shapes one command-line interface); `verify-this` (proves one claim, does not grade the repo).
- needs: npm/npx with network (downloads and executes a published package), the four named subagents, the repo's own toolchain, possibly Docker, services or secrets.
- side effects: downloads and runs an npm package; runs the target repo's setup, start and validation commands. Assessment only: fixes nothing.
- part of: entry router for agent-compatibility; scanner score weighted 70%, behavioral reviews 30%; environment-caused scanner failure is not charged to the repo.

## Family: cli-for-agent
- source repo: https://github.com/cursor/plugins, path `cli-for-agent/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Skills only; the plugin directory is `cli-for-agent` but the skill is `cli-for-agents`. No install or auth policy. Names no Cursor feature, so it reads as portable guidance (inferred, not stated).
- router: none
- development distance: core-dev
- disclosure recommendation: simple: one skill.

### cli-for-agents
- id: cli-for-agent:cli-for-agents (source path: cli-for-agent/skills/cli-for-agents/SKILL.md)
- description: "Designs or reviews CLIs so coding agents can run them reliably: non-interactive flags, layered --help with examples, stdin/pipelines, fast actionable errors, idempotency, dry-run, and predictable structure. Use when building a CLI, adding commands, writing --help, or when the user mentions agents, terminals, or automation-friendly CLIs."
- use when: Building, reworking or reviewing a CLI that automation gets stuck on: missing flags, unhelpful `--help`, interactive prompts, non-idempotent retries, no stdin or pipeline support, no dry-run.
- not for: `control-cli` (drives and profiles an existing interactive CLI/TUI, does not change its contract); `check-agent-compatibility` (grades a whole repository).
- needs: nothing beyond the repo
- side effects: none beyond edits the user asks for. On missing flags advise fail-fast with an example invocation (two of its three rules; one line still allows an interactive fallback).
- part of: standalone design/review checklist.

## Family: continual-learning
- source repo: https://github.com/cursor/plugins, path `continual-learning/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Ships the `agents-memory-updater` subagent (model: inherit) and a stop hook run by Bun that maintains `.cursor/hooks/state/continual-learning.json`. Reads transcripts under `~/.cursor/projects/<workspace-slug>/agent-transcripts/`. README says trial mode is on in the hook config, but config and code default it off: cadence is 10 turns and 120 minutes unless env vars say otherwise.
- router: none; the single skill only delegates: eligible stop hook asks for it, it calls exactly `agents-memory-updater` and returns its result (parent never mines transcripts or edits files).
- development distance: core-dev
- disclosure recommendation: simple: one skill.

### continual-learning
- id: continual-learning:continual-learning (source path: continual-learning/skills/continual-learning/SKILL.md)
- description: "Orchestrate continual learning by delegating transcript mining and AGENTS.md updates to `agents-memory-updater`."
- use when: The user wants recurring corrections and stable workspace facts from past Cursor chats folded into `AGENTS.md` (usually fired by the plugin's stop hook). Explicit-invocation only (`disable-model-invocation`).
- not for: `workflow-from-chats` (one-time, confidence-rated design of one workflow's guidance); `weekly-review` (recap, no memory).
- needs: Cursor transcripts, the `agents-memory-updater` subagent, write access to `AGENTS.md` and the state index; Bun for the hook.
- side effects: edits `AGENTS.md` (at most 12 bullets under `## Learned User Preferences` and `## Learned Workspace Facts`) and the transcript index; reads chat transcripts. The updater's guardrail is "Keep only these sections", so assume other hand-written `AGENTS.md` sections can be dropped: have the user commit a curated file first.
- part of: step inside the hook-driven loop; hands off entirely to `agents-memory-updater`.

## Family: cursor-sdk
- source repo: https://github.com/cursor/plugins, path `cursor-sdk/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Skills plus references (runtime-choice, auth, mcp, errors, streaming). Needs the external `@cursor/sdk` package and a Cursor API key (user key or team service-account key) passed as `apiKey` or `CURSOR_API_KEY`; the SDK does not read `.env` or a keychain. Cloud runs need a GitHub repo URL and repo access for the key's owner.
- router: none; the skill is an integration-pattern reference: if the SDK was named build directly, otherwise propose it and wait for confirmation; `Agent.prompt` one-shot, `Agent.create`+`send` multi-turn, `Agent.resume` across processes. Runtime order: needs GitHub PR, outlive caller, or separate isolation => cloud; checked-out dev/CI loop or non-GitHub/uncommitted tree => local.
- development distance: core-dev
- disclosure recommendation: simple: one large skill whose references load on demand.

### cursor-sdk
- id: cursor-sdk:cursor-sdk (source path: cursor-sdk/skills/cursor-sdk/SKILL.md)
- description: "Guide users building apps, scripts, CI pipelines, or automations on top of the Cursor TypeScript SDK (`@cursor/sdk`). Use this skill whenever the user mentions integrating, installing, or writing code against the Cursor SDK; whenever they say `Agent.create`, `Agent.prompt`, `Agent.resume`, `agent.send`, `run.stream`, `CursorAgentError`, or `@cursor/sdk`; whenever they ask to run Cursor agents programmatically from a script, CI/CD pipeline, GitHub Action, backend service, or any other code that isn't the Cursor IDE itself; and whenever they want to pick between local and cloud runtime, configure MCP servers for an SDK agent, or handle streaming, cancellation, or errors from an SDK agent. Also trigger when a user is wiring Cursor into an automation, writing a bot that runs Cursor, or porting REST `/v1/agents` calls to the SDK, even if they don't explicitly name the package. Use this eagerly rather than answering from memory; the SDK surface evolves and this skill plus its references are the source of truth for the external package."
- use when: Writing or debugging a script, bot, CI step, backend or webhook that runs Cursor agents programmatically; choosing local versus cloud runtime; MCP for an SDK agent; streaming, cancel, resume, error handling; porting REST `/v1/agents` calls to TypeScript.
- not for: `orchestrate` (ready-made cloud task tree that depends on this skill); `new-branch-and-pr` (ships current work interactively).
- needs: TypeScript/JavaScript runtime, `@cursor/sdk`, Cursor API key; local runs need `cwd` and a model; cloud needs GitHub repo and access.
- side effects: authoring guidance only, but what it builds can edit local files, push branches, open PRs and request reviewers (use `skipReviewerRequest: true` in CI) and consumes Cursor usage. `Agent.prompt` disposes itself (one best-practice line wrongly lists it for manual disposal); `Agent.create`/`Agent.resume` need `finally` or `await using`.
- part of: standalone reference router; offers the host `canvas` skill for agent dashboards only after the user accepts. REST, non-TS, hooks, private workers go to external docs.

## Family: cursor-team-kit
- router: none; no global router. Local sequences: `verify-this` picks `control-cli` or `control-ui` as measurement surface; `review-and-ship` and `new-branch-and-pr` are end-to-end entries that call no named skill.
- covers: eighteen skills for branch and PR work in Cursor: review (`review-and-ship`, `thermo-nuclear-code-quality-review`, `pr-review-canvas`, `get-pr-comments`); shipping (`new-branch-and-pr`, `make-pr-easy-to-review`, `fix-merge-conflicts`); CI and checks (`fix-ci`, `loop-on-ci`, `check-compiler-errors`, `run-smoke-tests`); proof (`verify-this`, `control-cli`, `control-ui`); upkeep (`deslop`, `workflow-from-chats`); reporting (`weekly-review`, `what-did-i-get-done`). The PR skills need `gh` and push rights, and the plugin brings two always-applied TypeScript rules.
- Full records: families/cursor-team-kit.md

## Family: orchestrate
- source repo: https://github.com/cursor/plugins, path `orchestrate/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Manifest 1.1.0 registers only the skill; ships a Bun/TypeScript orchestration CLI, schemas, role prompts and Slack adapter as implementation assets (not MCP, hooks or subagent definitions). Needs Bun, `bun install` in the skill's `scripts/`, `CURSOR_API_KEY`, GitHub access for the key's caller; optional `SLACK_BOT_TOKEN` plus channel (kickoff fails before spawning if the token is set and the channel missing). Key type: tell the user to use a personal/user API key (skill and dispatcher reference require it); README and `cursor-sdk` say team service-account keys also work, but do not promise that.
- router: none; the single skill is itself a two-role orchestrator: local dispatcher (clarify only a missing goal, kick off, return the cloud root planner's URL, stop) then root planner and subplanners who publish `plan.json`, spawn workers and verifiers, read handoffs, replan. Run exits 0 done, 100 rerun, else read state; finished only when every in-flight task is terminal.
- development distance: core-dev
- disclosure recommendation: simple: one skill; its references load on demand.

### orchestrate
- id: orchestrate:orchestrate (source path: orchestrate/skills/orchestrate/SKILL.md)
- description: "Use only when the user explicitly types `/orchestrate <goal>` to decompose a large task, spawn a tree of parallel cloud-agent workers/subplanners/verifiers via the Cursor SDK, and collect structured handoffs; do not invoke autonomously."
- use when: The user typed `/orchestrate <goal>` for a job too large for one agent; it is explicit-invocation only (`disable-model-invocation`), so a mere wish for parallel help or an ordinary coding task does not qualify.
- not for: `ralph-loop` (one local session re-fed the same prompt); `thermos` (fixed two-pass review); `cursor-sdk` (code the user owns that calls Cursor).
- needs: Bun, installed script dependencies, `CURSOR_API_KEY`, target GitHub repo and base ref the key's owner can access; must read `cursor-sdk` first; optional Slack app with chat, files, reactions and history scopes.
- side effects: cloud-agent usage (price unstated); commits and pushes branches; goal, state and handoffs synced into git by default (`syncStateToGit: false` opts out); optional Slack posts and uploads; optional draft PRs (`openPR` defaults false). No credentials in the goal text.
- part of: entry router for orchestrate; depends on `cursor-sdk`. Integration is not automatic: only a planner-published worker named `merge-<slice>` gets merge instructions (its prompt still carries the generic "Do NOT merge" line), so tell the user to check the merged branch.

## Family: origin-apps
- source repo: https://github.com/cursor/plugins, path `origin-apps/`
- manifest: Multi-host: Cursor, Claude Code, Codex and any Agent Skills host (Cursor, Claude and root Agent Plugins manifests, version 0.1.0). Skills only; "Origin" names apps being built, not an installed connector. Needs runtime network access to `https://cursor.com/docs/api/origin/*`. Reading source and writing a brief needs no Origin credentials; live API work needs whatever the live docs dictate. Install both skills together: the port skill depends on `origin-api`.
- distribution: also in the repository's Claude Code marketplace (`/plugin install origin-apps@cursor-plugins`).
- router: `origin-api`: docs router for any Origin question (fetch `llms.txt`, then only the section needed; docs override the skill); hands whole GitHub App migrations to `port-github-app-to-origin`, which follows `origin-api`, writes a brief via `references/brief.md`, and stops for the team.
- development distance: core-dev
- disclosure recommendation: simple: two skills.

### origin-api
- id: origin-apps:origin-api (source path: origin-apps/skills/origin-api/SKILL.md)
- description: "Routes questions about the Cursor Origin API to the right section of the Origin docs and names the few rules to check first. Use when a task mentions Origin, the Origin API, Origin Apps, or Origin webhooks, including creating an Origin App, authenticating as one, calling Origin endpoints, or handling Origin webhook deliveries."
- use when: A developer must create or authenticate an Origin App, call an Origin endpoint, explain a `403` on a mirrored repo, debug silent webhook subscriptions, or verify delivery signatures.
- not for: `port-github-app-to-origin` (whole existing GitHub App migration brief).
- needs: network access to the Origin docs; no credentials for lookup. A large spec download may be cached outside the app repo.
- side effects: none; read-only guidance. Rules to check first: native versus GitHub-mirror repo (mirror: calls beyond metadata and contents reads return 403), signature over the raw body before parsing, dedupe delivery ID, acknowledge 2xx.
- part of: entry router for Origin API work; step inside `port-github-app-to-origin`.

### port-github-app-to-origin
- id: origin-apps:port-github-app-to-origin (source path: origin-apps/skills/port-github-app-to-origin/SKILL.md)
- description: "Plans the port of an existing GitHub App to a Cursor Origin App. Use when the task is to bring a GitHub App to Origin or compare what it uses against the Origin API. Reads the app's needs out of its code, maps them onto the live Origin spec, and writes a porting brief with feedback for Cursor. Planning only."
- use when: The team has a GitHub App and wants to know whether it can run on Cursor Origin, what changes and gaps it faces, and what to tell Cursor before implementing.
- not for: `origin-api` (one contract question or a new Origin app).
- needs: run inside the app's source tree with read access; network to Origin docs; somewhere outside the repo to cache the spec; no Origin credentials.
- side effects: writes `ORIGIN-PORTING-BRIEF.md` at the repo root and `ORIGIN-FEEDBACK.md` when gaps warrant; planning only: no code changes, does not run the proposed test or send feedback (the team sends it).
- part of: entry point of the port sequence; invokes `origin-api`, then hands decisions, feedback and implementation authorization to the team.

## Family: pr-review-canvas
- source repo: https://github.com/cursor/plugins, path `pr-review-canvas/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Version 0.1.0, skills only. Needs Cursor with Canvas enabled and the unbundled host `canvas` skill and SDK declarations; `gh` access to the PR. README accepts a local branch or Graphite stack; the skill requires a PR reference and forbids local `git diff` fallback. Route by the skill.
- name collisions: `pr-review-canvas` is also a skill in `cursor-team-kit` (plain HTML page, explicit-only; this one writes a Cursor Canvas). Tell them apart by plugin id.
- router: none
- development distance: core-dev
- disclosure recommendation: simple: one skill.

### pr-review-canvas
- id: pr-review-canvas:pr-review-canvas (source path: pr-review-canvas/skills/pr-review-canvas/SKILL.md)
- description: "Render a PR diff review as a Cursor Canvas that groups changes by reviewer importance, separates boilerplate from core logic, and highlights tricky or unexpected code. Use when reviewing a pull request, summarizing a diff for review, or when the user asks for a PR review canvas, diff walkthrough, or change-set overview."
- use when: A reviewer has a specific GitHub PR and wants a Cursor Canvas that orders changes by reviewer value (core logic, wiring, boilerplate) with old-versus-new traces for tricky logic.
- not for: `pr-review-canvas` in `cursor-team-kit` (plain HTML page, explicit-only, needs only `gh`, `jq`, Python); `thermo-nuclear-review` (findings verdict); `get-pr-comments` (existing feedback).
- needs: Cursor with Canvas, the host `canvas` skill and `sdk/index.d.ts` read first, `gh pr diff` access. No PR reference means stop, ask and wait; no current-branch or local-diff guess.
- side effects: writes the Canvas wherever the host skill dictates; posts nothing to GitHub.
- part of: standalone, with mandatory delegation to the host `canvas` skill. Same frontmatter name as the team-kit skill; tell them apart by plugin.

## Family: ralph-loop
- source repo: https://github.com/cursor/plugins, path `ralph-loop/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Registers skills and hooks: `afterAgentResponse` (`capture-response.sh`) and `stop` (`stop-hook.sh`, `loop_limit: null`). Hooks need Bash, `jq`, `perl`; state in `.cursor/ralph/`. Repeated turns spend agent usage with no budget cap. Completion promise is documented as a `<promise>TEXT</promise>` tag, but the script also matches a whole untagged response equal to the promise (static reading): advise a distinctive phrase plus `max_iterations`.
- router: none; lifecycle: `ralph-loop` writes state at iteration 1 and starts the task, the response hook marks completion, the stop hook re-feeds the same prompt or ends (done flag, iteration limit, deleted state, invalid state, empty prompt). `cancel-ralph` removes state; `ralph-loop-help` only explains.
- development distance: core-dev
- disclosure recommendation: simple: three small skills.

### cancel-ralph
- id: ralph-loop:cancel-ralph (source path: ralph-loop/skills/cancel-ralph/SKILL.md)
- description: "Cancel an active Ralph Loop. Use when the user wants to stop, cancel, or abort a running ralph loop."
- use when: The user wants the active Ralph loop stopped or aborted.
- not for: `ralph-loop-help` (explains only).
- needs: the project's `.cursor/ralph/scratchpad.md` and permission to delete the directory.
- side effects: runs `rm -rf .cursor/ralph` without confirmation; reverts no edits and does not interrupt a command already running. Reports the iteration reached or "No active Ralph loop found."
- part of: exit step of the `ralph-loop` lifecycle; usable independently.

### ralph-loop-help
- id: ralph-loop:ralph-loop-help (source path: ralph-loop/skills/ralph-loop-help/SKILL.md)
- description: "Explain the Ralph Loop plugin, how it works, and available skills. Use when the user asks for help with ralph loop, wants to understand the technique, or needs usage examples."
- use when: The user asks what a Ralph loop is, which options exist, how to start or stop it, or whether their task suits repeated autonomous iteration.
- not for: `ralph-loop` (starts work); `cancel-ralph` (stops it).
- needs: nothing to explain; using the mechanism needs the plugin's hooks.
- side effects: none; read-only explanation.
- part of: standalone informational entry; not a prerequisite for starting.

### ralph-loop
- id: ralph-loop:ralph-loop (source path: ralph-loop/skills/ralph-loop/SKILL.md)
- description: "Start a Ralph Loop for iterative self-referential development. Use when the user asks to run a ralph loop, start an iterative loop, or wants repeated autonomous iteration on a task until completion."
- use when: The user asks for a Ralph loop or repeated autonomous iteration on a well-defined task with verifiable completion, such as fixing known failing checks or implementing a specified feature.
- not for: `orchestrate` (parallel cloud task tree); `ralph-loop-help` (explains only).
- needs: Cursor with the plugin's hooks active, Bash, `jq`, `perl`, writable `.cursor/ralph/`; optional `max_iterations` (default 0, unlimited) and `completion_promise` (default none).
- side effects: writes `.cursor/ralph/` state; the same prompt re-runs after every turn, editing whatever the task edits, until a stop condition. The skill recommends a limit but neither default enforces one.
- part of: entry point of the hook-driven loop; hands off to `cancel-ralph` to stop.

## Family: thermos
- source repo: https://github.com/cursor/plugins, path `thermos/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Registers skills and two Task subagents (`thermo-nuclear-review-subagent`, `thermo-nuclear-code-quality-review-subagent`). All three skills are explicit-invocation only. Manifest advertises "take-the-wheel and FSD merge-ready flows" that the plugin does not contain, so there is no thermos route to merge-ready. README says the quality skill and agent moved here from `cursor-team-kit`; both plugins still ship the skill. Correctness pass may need `gh` or `glab` read access, never to submit a review.
- name collisions: `thermo-nuclear-code-quality-review` is byte-identical in `cursor-team-kit`; the thermos README says it moved here, so recommend this copy and treat the two ids as one skill.
- router: `thermos:thermos`: determine scope, gather diff and file context, in one message launch both subagents with `run_in_background: true` and identical context, wait for both, synthesize findings first (dedupe, weight overlaps, resolve disagreements, no wholesale repeat of summaries). Subagents may not spawn nested agents.
- development distance: core-dev
- disclosure recommendation: simple: three skills; the router launches the other two but each is also chosen alone, so full records are small enough to keep in the source catalog.

### thermo-nuclear-code-quality-review
- id: thermos:thermo-nuclear-code-quality-review (source path: thermos/skills/thermo-nuclear-code-quality-review/SKILL.md)
- description: "Run an extremely strict maintainability review for abstraction quality, giant files, and spaghetti-condition growth. Use for a thermo-nuclear code quality review, thermonuclear review, deep code quality audit, or especially harsh maintainability review."
- use when: The user explicitly wants an extremely strict maintainability and architecture review of branch changes, including blocking working code that should be restructured.
- not for: `thermo-nuclear-review` (bugs, security, breakage); `thermos` (both together); `deslop`; `pr-review-canvas` (reading surface). Not a cure for over-engineered code: it pushes for deletion where it can, but also for moving conditionals into a dedicated abstraction, helper, state machine or policy object and for splitting files near 1,000 lines.
- needs: branch diff, relevant code context, before/after file sizes (1,000-line crossing is a presumptive blocker); can run in the main agent or via the matching subagent.
- side effects: none; read-only. Ordered findings and an approval judgment; no edits, review posts or merges.
- part of: standalone; step inside `thermos` via its subagent. Byte-identical to `cursor-team-kit:thermo-nuclear-code-quality-review`; recommend this copy.

### thermo-nuclear-review
- id: thermos:thermo-nuclear-review (source path: thermos/skills/thermo-nuclear-review/SKILL.md)
- description: "Comprehensive security and correctness audit of a branch's changes. Use for thermo nuclear, thermonuclear, or deep review requests, or branch/PR diff audits focused on bugs, breaking changes, security issues, devex regressions, and feature-gate leaks."
- use when: The user explicitly wants a deep audit of a checked-out branch or PR for bugs, security holes, cross-package breakage, dev-setup regressions or feature-flag leaks, reported only for added or modified code.
- not for: `thermo-nuclear-code-quality-review` (maintainability even when behavior is correct); `review-and-ship` (reviews and ships).
- needs: checked-out branch plus related client/server code; `gh` or `glab` read access only for the final discussion step, run only after the independent audit, if a PR exists and findings are medium or higher.
- side effects: none; read-only. No fixes, no posted review.
- part of: standalone; step inside `thermos` via its subagent. Can start from a current branch with no PR URL.

### thermos
- id: thermos:thermos (source path: thermos/skills/thermos/SKILL.md)
- description: "Launch both thermo-nuclear review subagents in parallel, then synthesize their findings. Use for thermos, double thermo review, or combined bug/security and code-quality branch audits."
- use when: The user explicitly asks for "thermos", a double thermo review, or combined bug/security and strict maintainability audit of the same changes.
- not for: either single thermo skill when only one dimension is wanted; `orchestrate` (arbitrary cloud implementation, not a fixed two-pass audit).
- needs: a host with named Task subagents and background launch (Cursor), both bundled agents, a diff and file context; two extra agent runs; conditional `gh`/`glab` as for the correctness pass.
- side effects: none; read-only. One deduplicated verdict with file references and remaining uncertainty.
- part of: entry router for thermos; launches `thermo-nuclear-review-subagent` and `thermo-nuclear-code-quality-review-subagent`, each loading its same-named skill.

## Family: create-plugin
- source repo: https://github.com/cursor/plugins, path `create-plugin/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Ships read-only `plugin-architect` (model: inherit) and an always-applied quality rule (valid metadata, existing relative in-plugin paths, local default output). README advertises a `/create-plugin` command but no command file exists; entry points are the two skills. No publish automation.
- router: none; documented authoring flow is decide components (`plugin-architect`), scaffold, then review before publishing; nothing invokes the next step automatically.
- development distance: adjacent (produces Cursor plugin files, outside typical application development)
- disclosure recommendation: simple: two skills, full records here are enough.

### create-plugin-scaffold
- id: create-plugin:create-plugin-scaffold (source path: create-plugin/skills/create-plugin-scaffold/SKILL.md)
- description: "Create a new Cursor plugin scaffold with a valid manifest, component directories, and marketplace wiring. Use when starting a new plugin or adding a plugin to a multi-plugin repository."
- use when: A new Cursor plugin idea needs the actual directory, manifest, component skeletons, or a marketplace entry in a multi-plugin repo.
- not for: `review-plugin-submission` (audits an existing plugin); `plugin-architect` agent (plans only, edits nothing).
- needs: lowercase kebab-case name, purpose, component set (rules, skills, agents, commands, hooks, mcpServers), single-plugin or marketplace repo, a writable destination.
- side effects: writes files; default output `~/.cursor/plugins/local/<name>/` makes the plugin live in Cursor at once (another path needs the user to say so). Publishes nothing.
- part of: entry point of the authoring flow; follow-on is `review-plugin-submission`, not auto-invoked. Cursor plugin format only.

### review-plugin-submission
- id: create-plugin:review-plugin-submission (source path: create-plugin/skills/review-plugin-submission/SKILL.md)
- description: "Audit a Cursor plugin for marketplace readiness. Use when validating manifests, component metadata, discovery paths, and submission quality before publishing."
- use when: A built Cursor plugin is about to be released or submitted and needs manifest, metadata, discovery-path, README and marketplace checks.
- not for: `create-plugin-scaffold` (creates missing structure); `check-agent-compatibility` (app readiness, not Cursor packaging).
- needs: the plugin tree, manifest, component files, README; optional marketplace file and logo.
- side effects: none; read-only. Output is pass/fail by section, prioritized fixes, a submission recommendation; publishes nothing.
- part of: final step of the create-plugin flow; also usable standalone as an audit.

## Family: docs-canvas
- source repo: https://github.com/cursor/plugins, path `docs-canvas/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Version 0.1.0; README calls it an initial scaffold and the skill a placeholder. Requires Cursor with Canvas enabled and the unbundled host files `~/.cursor/skills-cursor/canvas/SKILL.md` and `sdk/index.d.ts` (not inspected).
- router: none
- development distance: adjacent (documentation rendered as an interactive Cursor Canvas)
- disclosure recommendation: simple: one placeholder skill.

### docs-canvas
- id: docs-canvas:docs-canvas (source path: docs-canvas/skills/docs-canvas/SKILL.md)
- description: "Render a documentation-style Cursor Canvas that organizes architecture notes, API references, walkthroughs, and how-tos into a navigable layout with sections, tables of contents, and cross-references. Use when the user asks for a docs canvas, documentation overview, architecture walkthrough, API reference page, or wants to render structured documentation as an interactive canvas."
- use when: Architecture notes, an API reference, a runbook, a Markdown collection or a codebase walkthrough should be rendered as a navigable Cursor Canvas.
- not for: `pr-review-canvas` (PR diffs); the host's base `canvas` skill (the generation policy this one depends on).
- needs: Cursor with Canvas enabled; must first read the host `canvas` skill and SDK declarations (not bundled, unverified); a source directory, URL, outline or codebase question.
- side effects: writes a canvas file wherever the base Canvas skill dictates.
- part of: step inside the base `canvas` workflow; self-described placeholder, recommend only as a starting outline.

## Family: grok-voice
- source repo: https://github.com/cursor/plugins, directory `grok-voice/` (v0.1.0, Eric Zakariasson, MIT).
- plugin manifest: `.cursor-plugin/plugin.json` (`skills` only). No agents, MCP, hooks, commands or rules. No auth policy in the manifest; the three add-* skills need an xAI API key (`XAI_API_KEY`) on the target app's server and live access to api.x.ai, with usage billed per the xAI docs. debug-voice instruments an existing integration and needs no key itself. Skills target the user's app, not the IDE. Vendor-specific: xAI/Grok only. UI convention: waveform icon = voice mode, microphone = dictation, speaker = read aloud.
- router: none. The skills cross-reference each other by scope (add-voice points to add-dictation, add-read-aloud and debug-voice); debug-voice is the shared debug target.
- development distance: adjacent (adds voice features to an app; xAI-specific)
- disclosure recommendation: simple. Four skills for four different scenarios in one vendor ecosystem; full records here are enough.

### add-voice
- id: grok-voice:add-voice (source path: grok-voice/skills/add-voice/SKILL.md)
- description: "Use when the user runs /add-voice, types Voice Mode, or asks to add Grok realtime voice to an app, including replacing an STT-LLM-TTS cascade or OpenAI Realtime.   Wire speech-to-speech, safe auth, and app mic. Composer: waveform button, mic icon reserved for dictation. For mic-to-text only use /add-dictation; to speak text replies use /add-read-aloud. To add debug logging and fix from logs use /debug-voice."
- use when: Add a two-way talking "Voice Mode" to your app on Grok realtime speech-to-speech, or replace an STT-LLM-TTS cascade or OpenAI Realtime. Wires mic capture, playback with barge-in, transcript rows and a waveform composer button, plus a TS skeleton and a Python twin.
- not for: add-dictation (speech to text only), add-read-aloud (speak text replies one-way), debug-voice (fix an existing session).
- needs: an xAI account and XAI_API_KEY on the server; browser/mobile clients need a backend minting ephemeral client secrets; an app with a composer UI.
- side effects: edits app code and adds a server route; the key never goes in the client bundle; usage cost at about $0.08/min per the docs.
- part of: first step of the grok-voice sequence; hands off to debug-voice for instrumentation.

### add-dictation
- id: grok-voice:add-dictation (source path: grok-voice/skills/add-dictation/SKILL.md)
- description: "Use when the user runs /add-dictation or wants speech turned into text with Grok speech-to-text: a mic button that dictates into the composer, live captions, or transcribing recorded audio (files, uploads, URLs) with word timestamps, diarization, subtitles, meeting notes. STT, transcribe, transcription. For a voice agent that talks back use /add-voice."
- use when: Add Grok speech-to-text: a mic button that dictates into the composer, live captions, or transcribing recorded audio (files, uploads, URLs) with timestamps, diarization or subtitles. Batch route by default, streaming via your own backend relay.
- not for: add-voice (the model talks back), add-read-aloud (the reverse direction).
- needs: XAI_API_KEY on the server only; no ephemeral-token flow, so browser streaming goes through your relay; must read the docs' model list and pass the latest model id.
- side effects: edits app code and adds a server route; per-request cost; max file 500 MB.
- part of: standalone; shares PCM capture with add-voice; hands off to debug-voice.

### add-read-aloud
- id: grok-voice:add-read-aloud (source path: grok-voice/skills/add-read-aloud/SKILL.md)
- description: "Use when the user runs /add-read-aloud or wants the app to speak text with Grok text-to-speech: read-aloud button on assistant replies, auto-speak, TTS, voice output, narration, IVR prompts, speech tags, voice_id. For a two-way voice agent use /add-voice. For speech-to-text use /add-dictation."
- use when: Add Grok text-to-speech: a speaker button on assistant replies, opt-in auto-speak, narration or IVR prompts. Batch MP3 route by default; streaming only when audio must start before the text is done or exceeds 15,000 characters.
- not for: add-voice (two-way), add-dictation (speech to text).
- needs: XAI_API_KEY on the server only; language is required on batch requests.
- side effects: edits app code and adds a server route; per-request cost; voice cloning is out of scope.
- part of: standalone; shares audio code with add-voice; hands off to debug-voice.

### debug-voice
- id: grok-voice:debug-voice (source path: grok-voice/skills/debug-voice/SKILL.md)
- description: "Use when the user runs /debug-voice, says voice mode has flaws, asks to see or capture what happened in a Grok realtime voice session, or a voice integration has no debug logging yet. Proposes a plan, then installs a dev-only log pipeline (client logger → local NDJSON) in the app's own language and conventions, then runs the fix loop: match the user's report to log signatures, fix one thing, re-test."
- use when: Your Grok realtime voice mode misbehaves (silence, self-interruption, choppy audio, no user transcript, slow first word) and you cannot hear it from the agent: shows a change list, installs a dev-only NDJSON log pipeline, then fixes one thing per re-test from log signatures.
- not for: add-voice (builds the session; this repairs it).
- needs: an existing Grok realtime client in the app, a running dev server, and you testing in the real app and reporting the session id.
- side effects: edits app code after approval: /api/voice/log route (404 in production unless VOICE_LOG=1), client logger, .gitignore entry and local .voice-logs/<sessionId>.ndjson files. A single-process app may append directly without HTTP. Records confirmed fixes in the skill and updates add-voice when a fix changes how voice should be built.
- part of: step 8 of the add-voice sequence and debug hand-off for add-dictation and add-read-aloud; also standalone.

## Family: pstack-benny
- source repo: https://github.com/cursor/plugins, directory `pstack/automations/benny/skills/`. Labeled as not registered skills: the pack is dormant, not exposed by the plugin manifest, has no slash name, and is absent from the Claude Code copy. Entry is pointing Cursor at `pstack/automations/benny/FOR_AGENTS.md` and naming the target repository.
- plugin manifest notes: none of its own; needs Cursor Automations with Slack thread read/reply, a configured tracker adapter, repo and draft-PR access, a control-adapter skill, a committed feature map, and project-scoped pstack. Secrets stay out of files; subagents never get Slack credentials. Drafts only: never merges or deploys.
- router: none; fixed sequence setup-benny (once) -> benny-triage automation (triage-issue-reports) -> benny-reproduce automation (reproduce-and-fix-issues). Gate: neither automation is enabled until the 7-point thread-safety test passes.
- development distance: adjacent (Slack bug triage and automated repro/draft-PR workflow, Cursor-only)
- disclosure recommendation: simple; three niche, sequential, Cursor-only skills, so full records in the source catalog suffice.

### setup-benny
- id: pstack-benny:setup-benny (source path: pstack/automations/benny/skills/setup-benny/SKILL.md)
- description: "Configure Benny and prepare its triage and repro automations. Use when installing Benny or changing its Slack, tracker, repository, routing, control, model, or budget settings."
- use when: Install Benny (Slack bug triage plus repro/fix automations) in a repo, or change its Slack, tracker, repository, routing, control, model or budget settings.
- not for: triage-issue-reports and reproduce-and-fix-issues (runtime skills, not setup).
- needs: Cursor with Slack actions, an issue-tracker adapter (Linear or GitHub examples), repo and PR access, a control-adapter skill that drives the target app, built-in `automate` skill, project-scoped pstack; optional BENNY_SLACK_BOT_TOKEN kept out of files.
- side effects: merges the pack into `<repo>/.cursor/automations/benny/` preserving local edits, enables pstack in `.cursor/settings.json`, writes external-to-pack config and feature map (user commits); creation/update requires explicit request; enables neither automation until the 7-point thread-safety test passes
- part of: step 1 of the Benny sequence (not a registered slash skill); new automations use `automate`'s reviewed editor handoff one at a time; existing automations get a user editor checklist, never `automate` updates or replacements.

### triage-issue-reports
- id: pstack-benny:triage-issue-reports (source path: pstack/automations/benny/skills/triage-issue-reports/SKILL.md)
- description: "Triage Slack issue reports with one thread-only verdict, evidence review, cause-aware routing, tracker dedupe, and fail-closed ticket creation. Use only from the configured Benny triage automation."
- use when: Runtime of the `benny-triage` automation: classify one new Slack bug report, dedupe against the tracker, and file a ticket only for a clear new bug. A human triaging one bug by hand is a poteto-mode Bug fix instead.
- not for: reproduce-and-fix-issues (next stage, does the repro); poteto-mode Bug fix (human-driven).
- needs: Benny config, Slack thread read/reply, tracker adapter, pstack why/unslop/principles.
- side effects: at most one substantive source-thread verdict with one marker (`[benny:bug]`, `[benny:performance]`, or `[benny:other]`, optionally followed by `tracker=URL`); may create/update tracker issues, and must cancel/close/delete a newly created issue if the Slack handoff fails; bounded direct follow-up replies allowed, no second marker; duplicate/preflight failures suppress posting; never reproduces or fixes
- part of: step 2 of the Benny sequence; its marker is the gate for reproduce-and-fix-issues.

### reproduce-and-fix-issues
- id: pstack-benny:reproduce-and-fix-issues (source path: pstack/automations/benny/skills/reproduce-and-fix-issues/SKILL.md)
- description: "Reproduce triaged Slack bugs through a configured app-control adapter, verify existing fixes, and open a bounded draft pull request only after before-and-after proof. Use only from the configured Benny repro automation."
- use when: Runtime of the `benny-reproduce` automation: a Slack report with a trusted `bug` or `performance` marker needs a UI reproduction, verification of an existing fix, or a bounded draft PR.
- not for: triage-issue-reports (previous stage); poteto-mode Bug fix (human-driven).
- needs: Benny config, a control-adapter skill (launch, navigate, drive real UI, read-only state inspection, screenshots, recording, cleanup) and a completed feature map; Slack, repo and PR access; pstack why/tdd/unslop/principles.
- side effects: launches/drives the real UI, records media, posts to Slack, commits and opens a draft PR; cleans up through the control adapter; never merges or deploys. Requires a trusted marker, twice-reproduced symptom, media review, closed rejection window, runtime root cause and budget fit before authoring a fix; human fix ownership stops it, an existing PR/commit switches to verification without a competing patch.
- part of: step 3 of the Benny sequence, after triage-issue-reports.

## Far from development (pointers only)
- teaching (`create-learning-path`, `run-learning-retrospective`: learning roadmaps and retrospectives for any topic) -> far/learning.md
- third_party/google-drive (`google-drive`: usage guide for Cursor's Google Drive MCP connector) -> far/workspace.md
- third_party/google-docs (`google-docs`: usage guide for the Google Docs MCP connector) -> far/workspace.md
- third_party/google-sheets (`google-sheets`: usage guide for the Google Sheets MCP connector) -> far/workspace.md
- third_party/google-slides (`google-slides`: usage guide for the Google Slides MCP connector) -> far/workspace.md
- third_party/x (`X MCP guide`: reading, searching and posting on X and X Chat through its MCP connector) -> far/social.md
- third_party/x-money (`X Money guide`: money movement through X Money; Grok Bot and Sand only, not Cursor) -> far/finance.md
- third_party/tailscale (`tailscale-setup`: Grok Bot's Tailscale connection; Grok Bot and Sand only) -> far/network.md
- third_party connector-only entries (no records): 116 of 123 `third_party/` entries have no skill; route by the requested service connection (including developer tools), with its declared authentication and read/write capabilities.

## Cross-family notes
- Collision: `pr-review-canvas` is a skill in `cursor-team-kit` and in its own `pr-review-canvas` plugin; same frontmatter name, different output, tools and gates (HTML page via `gh api`, explicit-only, versus Cursor Canvas via `gh pr diff`, model-invocable, PR link mandatory). Distinguish by plugin id.
- Collision: `thermo-nuclear-code-quality-review` is byte-identical (verified by diff) in `cursor-team-kit` and `thermos`; the thermos README says it moved there, so recommend the thermos copy and treat the two ids as one skill.
- Same-name skills elsewhere: `google-drive`, `google-docs`, `google-sheets`, `google-slides` also exist in OpenAI's catalog as different skills.
- Explicit-invocation only (`disable-model-invocation: true`) among the tool plugins: `continual-learning`, team-kit `pr-review-canvas`, both `thermo-nuclear-code-quality-review` copies, `thermo-nuclear-review`, `thermos`, `orchestrate`. The pstack and dyl-stack headers state their own (every pstack skill except setup-pstack; every dyl-stack skill except build-figma).
