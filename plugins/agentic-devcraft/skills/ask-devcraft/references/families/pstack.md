# cursor/plugins family: pstack (with its Claude Code variant harness)
Source: https://github.com/cursor/plugins @ e559e62b729e040186bc9d573e71255e5a96f50d
Distribution (cursor/plugins): the Cursor marketplace `cursor-plugins` (`.cursor-plugin/marketplace.json`); in Cursor, `/add-plugin <plugin>`. The same repository holds a Claude Code marketplace (`.claude-plugin/marketplace.json`; `/plugin marketplace add cursor/plugins`) that lists only `pstack` and `origin-apps`. Skill directories are `<plugin>/skills/<skill>/`. A "Cursor packaging only" manifest note describes packaging, not where a skill can run: the family header names the Cursor features (Task subagents, hooks, Canvas, rules) a skill depends on.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `pstack` family and its `harness` host-variant note. The catalog entry is in cursor.md.

## Family: pstack
- source repo: https://github.com/cursor/plugins, directory `pstack/` (v0.15.43, Lauren Tan, MIT); 58 skills. Source paths below are relative to the repo root.
- distribution: pstack is its own collection, one author's plugin, and the unit of familiarity: installed pstack skills say nothing about the other cursor/plugins plugins. Cursor: `/add-plugin pstack`. Claude Code: `/plugin marketplace add cursor/plugins`, then `/plugin install pstack@cursor-plugins`, which installs the generated copy in `harness/pstack/claude-code/` (Family: harness). Skill directories are `pstack/skills/<skill>/`; the two agents are in `pstack/agents/`. Other hosts load or copy the skill directories (on the observed OpenCode host OpenChamber's skill catalog copied them in), so a missing adapter is no reason to hold a skill back: name where the skill is, and say which part needs a Cursor tool when its record or the `outside Cursor and Claude Code` line says so.
- plugin manifest notes: `pstack/.cursor-plugin/plugin.json` registers `skills: ./skills/` and `agents: ./agents/` (agents `poteto-agent`, the code delegate for poteto-mode runs that must read poteto-mode first, and `comment-sicko`, the comment-deleting reviewer); a generic agent-plugins `pstack/plugin.json` also exists. No MCP server, app connector, hook, command or rule, and no auth policy. Host: Cursor (Task tool, AskQuestion, Custom Modes, /loop, `~/.cursor/rules/pstack-models.mdc` written by /setup-pstack). Claude Code gets the generated copy described under Family: harness. No Codex or OpenCode adapter exists; the `outside Cursor and Claude Code` line below says which skills name Cursor tools, and the rest was not checked on other hosts. Every skill has `disable-model-invocation: true` except setup-pstack: it runs only when the user types it or a loaded workflow reads it, never from wording alone. Not bundled but named by many steps: cursor-team-kit (`/deslop`, control-ui, control-cli, verify-this), thermos subagents, Cursor built-ins (`/loop`, `/create-skill`, `automate`, Bugbot, cloud agents, Custom Modes).
- router: `poteto-help` (questions: which skill, setup, cost, a run that misbehaved, personalising; answers and does not start work) and `poteto-mode` (work: restate goal and smallest change -> match one of 22 playbooks -> copy steps into the todo tool -> run skills at triggers, citing only principle leaves read this session; unmatched, large or unattended work goes to `figure-it-out`). Recommended start for first use (README order): install, `/setup-pstack`, then a real task under `/poteto-mode` stated as a goal plus a pass/fail check. A hand-written skill list is discouraged because it drops playbook steps.
- delegation: when `poteto-help` or `poteto-mode` is installed, hand pstack routing to it (`poteto-help` for which-skill questions, `poteto-mode` for work) instead of re-deriving it from the matching records. When pstack skills are installed without the routers, recommend the fitting installed skill first and treat any pstack workflow as a remote lead; then add one line that installing the routers from this source would give better answers next time, never as a prerequisite. In Claude Code the routers are `/pstack:poteto-help` and `/pstack:poteto-mode` (Family: harness).
- development distance: core-dev
- disclosure recommendation: router-delegated; poteto-help and poteto-mode cover the family's situations, so the 56 other records are one-liners for matching, with poteto-mode's playbook list carrying the sequences. Recommend the router for "do this work rigorously" and a single skill only when the user wants exactly that piece.
- partial installs: leaves are often copied without the routers (for example through a skill catalog), so they stand alone and the mode, playbooks and other pstack workflows are leads to name, not steps to invoke. Copies of 15 skills taken before a later upstream rewrite carry a longer earlier wording with the same name and description; count them as pstack. `teach` and `technical-writing` hand off to `unslop`, and `principle-type-system-discipline` names `typescript-best-practices`; where those are not installed, recommend the leaf for its single rule only. `teach` invokes `how` and `why` in parallel for larger subjects; `how` requires a Cursor `Task` subagent, while `why` specifies no subagent. Map that dependency to the host's subagent tool or say it cannot run as written.
- name collisions: bare `tdd` and `teach` also exist in mattpocock-skills. Say which source when recommending.
- principle leaves: passive rules of a few lines each, with no steps, outputs or side effects, and user-invoked (`disable-model-invocation: true`). Invoking one loads the rule for the work that follows. It does not edit what is already written, so pair it with a request to redo the work; to make it last, the rule goes into the agent instructions or a check (`correct`). By complaint: over-built `principle-laziness-protocol`, `principle-subtract-before-you-add`, `principle-minimize-reader-load`; shims kept `principle-migrate-callers-then-delete-legacy-apis`; guards everywhere `principle-boundary-discipline`; brittle tests `principle-test-behavior-not-implementation`; asks too much `principle-never-block-on-the-human`; "done" unproved `principle-prove-it-works`; the same mistake again `principle-encode-lessons-in-structure`, `correct`.
- outside Cursor and Claude Code (checked for 19 of the 58 skills): `principle-redesign-from-first-principles`, `principle-separate-before-serializing-shared-state`, `principle-sequence-verifiable-units`, `principle-subtract-before-you-add`, `principle-test-behavior-not-implementation`, `principle-type-system-discipline`, `unslop`, `technical-writing`, `sharpen`, `why`, `tdd`, `statechart` and `typescript-best-practices` name no Cursor tool in their text (statechart still needs a shell and network on first run); `recall`, `reflect`, `setup-pstack`, `show-me-your-work` and `swarm` depend on Cursor paths or subagent models.
- playbook link: `poteto-mode/playbooks/bug-fix.md` step 5 routes to tdd for cheap local test paths; skips expensive, integration-heavy or unclear tests.

### poteto-help
- id: pstack:poteto-help (source path: pstack/skills/poteto-help/SKILL.md)
- description: "Guides users through pstack setup, /poteto-mode, and picking the skill, playbook, or principle for a task. Type /poteto-help with a question."
- use when: Ask which pstack skill, playbook or principle fits a task, how to set up, cut cost, or why a run misbehaved; it answers with at most one prompt to send and a public link, and does not start the work.
- not for: poteto-mode (a real work request such as "use pstack to fix this bug" is not a help question: help reads poteto-mode and works under it); setup-pstack (writes the model rule; help only suggests it); sharpen (rewrites a prompt).
- needs: explicit `/poteto-help` plus a question; local plugin docs; optionally checks for ~/.cursor/rules/pstack-models.mdc and project verify-* skills. No credentials.
- side effects: help questions are read-only; an actual work request hands off to poteto-mode and inherits its playbook's side effects.
- part of: entry router for pstack questions. Sequence: infer the need, else ask one multiple-choice (set up / start a task / pick a skill / fix a run / make pstack mine) -> check only answer-changing state -> offer /setup-pstack at most once per chat -> read the target skill before quoting it (target wins over its map) -> reply.

### poteto-mode
- id: pstack:poteto-mode (source path: pstack/skills/poteto-mode/SKILL.md)
- description: "poteto's agent style for concise, detailed responses, deliberate subagents, unslopped prose, simple code, and verified work. Use for poteto, /poteto-mode, or requests to work in this style."
- use when: Explicitly want pstack's rigorous workflow for a concrete bug, feature, refactor, measurement, investigation, PR lifecycle or autonomous queue; it matches one of 22 playbooks and runs the other pstack skills at their triggers.
- not for: poteto-help (advice only); figure-it-out (where the mode itself sends large, cross-cutting, unattended or unmatched work); architect/arena/interrogate for a single step.
- needs: a goal plus a checkable done condition; todo tool; Task subagents with per-role models (`poteto-agent`, reads worker.md); cursor-team-kit for /deslop, control-ui, control-cli; git and authenticated `gh` (or `origin pr`, never Graphite) for PR playbooks; Bun for the PR watcher; Cursor /loop and Custom Modes. Models: ~/.cursor/rules/pstack-models.mdc, defaults Opus 5.5 xhigh-fast, panel Fable 5.2 / Opus 5.5 / Gemini.
- side effects: varies by playbook: commits, ready (non-draft) PRs, merges (Shipping, Autopilot-full), force-with-lease on own branches, worktree/simulator deletion (Worktree cleanup), token cost. The PR watcher runs `bun install --frozen-lockfile` with no prompt. Reversible work and team-chat/ticket updates proceed without asking; it pauses for force-push to shared branches, deploys, data deletion, customer messages. Team-chat and ticket posts are not confirmed (the mode's own rule; principle-never-block-on-the-human's "external messages" confirmation does not cover them here): warn the user they go out unasked.
- part of: entry router for pstack work. Sequence: restate goal and smallest change -> match playbook -> copy steps into the todo tool -> run skills at triggers (architect across boundaries, swarm fan-out, arena bakeoff, interrogate contested, unslop prose, technical-writing docs, no-comments before review, benchmark-checklist for numbers, show-me-your-work for long runs). Hands off to figure-it-out when no playbook fits.
  - playbooks and where each stops (steps live in playbooks/<kebab-title>.md, not slash skills): Investigation (read-only cited answer; no PR); Bug fix (reproduce on real surface, root-cause, scoped fix, ready PR); Perf issue (baseline, "don't do it" ... "cheaper" in order, post-fix trace, PR); Hillclimb (frozen harness, keep only noise-clearing wins, PR); Runtime forensics (live capture and instrumentation or hotfix, diagnosis only); Trace forensics (existing capture, diagnosis only); Feature (architect, mandatory arena if several valid shapes, ready PR); Refactoring (pin behavior first, delete old API with callers, PR); Prototype (throwaway scratch, never shippable); Visual parity (screenshot baseline, zero diff per component, PRs); Authoring a skill (create-skill, PR); Eval (blinded multi-model, recommendation only); Babysit (drive/threads-only/check; stops merge-ready, never merges or force-pushes); Shipping (verified green stack, merges lowest PR first); Autonomous run (/loop to a checkable predicate); Autopilot-full (queue of PRs to merged, merges); Autopilot-stack (same, never merges); Session pickup; Pause safely (one wip: commit); Multi-phase plan (writes the plan, does not implement); Worktree cleanup (deletes worktrees); Opening a PR (ready PR, not every playbook ends in it).

## Records: pstack (matching only; poteto-help and poteto-mode own routing)

### architect
- id: pstack:architect (source path: pstack/skills/architect/SKILL.md)
- description: "Sketch types, signatures, and module structure before code, then stay in the loop while implementation fills in. Use for /architect, 'architect this', 'design this', or non-trivial work where jumping to code would lock in the wrong shape."
- use when: Non-trivial change where jumping to code would lock in the wrong shape: settle types, signatures and module boundaries first (two sketched shapes, pick the one with single state owners). Escalates to arena if the design is large or contested.

### arena
- id: pstack:arena (source path: pstack/skills/arena/SKILL.md)
- description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
- use when: One attempt at a non-trivial artifact would lock in the wrong shape; want N parallel candidates merged into one (frame, fan out, cross-judge, pick, graft, verify). Contrast: interrogate keeps every verified finding instead of one base.
- needs: Task/subagent tool, worktrees or temp dirs, at least two model runners from the `arena runners` line of ~/.cursor/rules/pstack-models.mdc (defaults Fable 5.2, Opus 5.5, Gemini); judge from another vendor than the parent (disclosed if impossible).
- side effects: creates candidate artifacts in separate worktrees or temporary directories, integrates the chosen result and runs verification; cost: N parallel model runs plus a judge when available

### automate-me
- id: pstack:automate-me (source path: pstack/skills/automate-me/SKILL.md)
- description: "Use for "automate me", "create/update/refresh my -mode skill", "turn/capture my preferences or working style into a skill", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill via create-skill + unslop, optionally pulling fresh evidence from recent transcripts."
- use when: Capture my working style and preferences into a personal `<handle>-mode` skill by mining this workspace's transcripts. Task-specific skills are create-skill alone, not this.
- needs: Cursor create-skill (built-in), unslop; reads this workspace's agent-transcripts only (never across projects)
- side effects: private chat history is read; worktree, commit and PR for the new skill

### benchmark-checklist
- id: pstack:benchmark-checklist (source path: pstack/skills/benchmark-checklist/SKILL.md)
- description: "Vet a perf measurement (limiter, tuning, limits, errors, repeatability, relevance, and whether the work happened) before you report or act on it. Use when you run a benchmark or report a speedup or regression you measured."
- use when: About to report or act on a benchmark, speedup or regression (or pick between options on one): seven questions, verdict faster/slower/no measurable difference/inconclusive. Reasoning rule version: principle-explain-the-number.
- needs: a runnable benchmark and profilers (>=5 alternating runs per side)

### blast-radius
- id: pstack:blast-radius (source path: pstack/skills/blast-radius/SKILL.md)
- description: "Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it's safe because of by running real code instead of writing it up. Use for 'blast radius of X', 'what could this break', or reviewing a small diff you don't trust."
- use when: "What could this break?" for a small diff you do not trust: proves the one fact it is safe because of by running real code. Contrast: interrogate is the heavier multi-model attack on the diff itself; how/why explain, not prove.
- needs: read access to diff/PR and library source, ability to run scripts; unslop
- side effects: runs real code, so not read-only

### bro
- id: pstack:bro (source path: pstack/skills/bro/SKILL.md)
- description: "Restate the last message in plain human language, with no jargon."
- use when: Last assistant message was not understood; restate it in plain words with no jargon. Contrast: in-your-own-words restates the user's goals, not the assistant's message.

### correct
- id: pstack:correct (source path: pstack/skills/correct/SKILL.md)
- description: "Find the mistakes agents keep repeating in this repo and make each one impossible. Try architecture first, then types, then a lint whose error names the fix, then a test, and write docs last. Prove each check fails on a real past mistake. Repeat this each time the operator corrects you. Use for /correct."
- use when: Agents keep making the same mistake in this repo; make each class impossible at the highest working level (architecture, types, lint naming the fix, test, docs last). A class counts after two occurrences.
- needs: repo history (commits, reverts, review comments); ability to add lint/CI checks
- side effects: one commit per mistake class, CI changes, a rule table in the agent instruction file

### create-formal-verification-skill
- id: pstack:create-formal-verification-skill (source path: pstack/skills/create-formal-verification-skill/SKILL.md)
- description: "Generate a project-local skill that formally verifies the code where a bug costs the most and tests reach the least, in any language, with whichever verification tool fits. Use for /create-formal-verification-skill, "model-check this race", "prove this invariant", or when concurrency, retries, state machines, parsers, or unsafe code need more than tests."
- use when: Concurrency, retries, state machines, parsers or unsafe code need more than tests ("model-check this race", "prove this invariant"). Writes a project-local verify skill. Contrast: create-verification-skill drives the app like a user.
- needs: a fitting verifier (TLA+ via statechart for event order; code-level verifier, proof assistant, or generated-input tests otherwise)
- side effects: writes a skill and verification files, runs the verifier and a deliberately broken scratch variant of real code, then drops the scratch change; no retained product-code changes unless asked. Generated-input fallback is not an all-input proof.

### create-verification-skill
- id: pstack:create-verification-skill (source path: pstack/skills/create-verification-skill/SKILL.md)
- description: "Generate a project-local verification skill that drives your app the way a user does — any language, framework, or platform. Use for /create-verification-skill, "make a control skill for this repo", or when a project has no scripted way to prove UI/CLI/service behavior."
- use when: No scripted way to launch and drive the real app (UI/CLI/service) and capture evidence; writes `.cursor/skills/verify-<app>/SKILL.md` plus a feature map, proven by one end-to-end run.
- needs: an app that builds and starts; Playwright/CDP/tmux/PTY/HTTP as fits
- side effects: starts processes and ports; writes verification scaffolding

### figure-it-out
- id: pstack:figure-it-out (source path: pstack/skills/figure-it-out/SKILL.md)
- description: "Design an auditable playbook when no narrower one fits: a large migration, an ambitious multi-part change, or work a human reviews after stepping away. Scales rigor to the task, runs a hypothesis loop, and logs decisions. Use for /figure-it-out or 'figure it out'."
- use when: Large migration, ambitious multi-part change, or work a human reviews after stepping away, where no narrower playbook fits. poteto-mode routes here for large, cross-cutting, unattended or unmatched tasks; architect covers only the design shape.
- needs: poteto-mode Principles, show-me-your-work for the trail; worktrees for fan-out; possibly long-running
- side effects: executes the designed workflow, edits and verifies real artifacts, reverts unsuccessful experiments, and usually commits the audit trail; a multi-hour run gets one checkpoint before commitment

### how
- id: pstack:how (source path: pstack/skills/how/SKILL.md)
- description: "Use for "how does X work", code walkthroughs before changing something, and placement / ownership / layering questions ("where should this live", "which package owns this", "is this the right layer"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
- use when: "How does X work", a code walkthrough before changing something, or "where should this live / which package owns this". Present mechanics and placement; why covers motivation, blast-radius covers breakage.
- needs: a read-only subagent (Cursor Task, `generalPurpose`); map to the host subagent tool elsewhere

### in-your-own-words
- id: pstack:in-your-own-words (source path: pstack/skills/in-your-own-words/SKILL.md)
- description: "Restate in your own words what you think the user's goals are and what problem they're trying to solve. Use for /in-your-own-words."
- use when: Check the agent understood the user's goal and problem before it starts; restatement only. Also the intent-framing step of interrogate. Also mid-session as a drift check: the agent restates, the user compares; it checks nothing itself.

### interrogate
- id: pstack:interrogate (source path: pstack/skills/interrogate/SKILL.md)
- description: "Use for "interrogate", "adversarial review", "multi-model review", "challenge this", "stress test this code", "find blind spots", or "tear this apart". Adversaries try to break a change or design, and only findings proven by a run survive."
- use when: Adversarial or multi-model review of a change or design: "stress test this code", "tear this apart". Parallel adversaries selected via arena's runner rules; only findings rerun by the coordinator survive; reports only, applies no fixes. Contrast: blast-radius focuses on breakage outside the diff. Also for a claimed finding nobody reproduced, when it concerns a change or design in scope.
- needs: named scope or default branch diff through the working tree; Task subagents, isolated worktrees with scoped uncommitted changes copied in, and `interrogate reviewers` model line (arena defaults when absent); designs/plans require a runnable prototype or current-tree probe
- side effects: creates worktrees and repro artifacts, runs real-code probes and coordinator reruns; cost follows the configured reviewer count, not a fixed four

### ketchup
- id: pstack:ketchup (source path: pstack/skills/ketchup/SKILL.md)
- description: "Catch the user up on what changed in this chat since their last message, in plain words and small visuals. List every item waiting on them with what they need to decide it from the reply alone. Use for /ketchup."
- use when: Back in this chat after agents, PRs or CI ran: plain catch-up since the user's last message plus every decision waiting on them. Cross-chat history is recall, not this.
- side effects: read-only turn: no edits, no jobs started, no posting

### ketchup-video
- id: pstack:ketchup-video (source path: pstack/skills/ketchup-video/SKILL.md)
- description: "Catch the user up like /ketchup, with a short subtitled video of slides for what happened and the waiting calls as text under it. Use for /ketchup-video."
- use when: Returning to a long chat and wanting the catch-up as a short subtitled video (<=10 slides) instead of ketchup's text.
- needs: a way to render and check video frames (tool unspecified)
- side effects: writes a video file outside the repo (the one exception to ketchup's read-only turn)

### maintain-formal-verification-skill
- id: pstack:maintain-formal-verification-skill (source path: pstack/skills/maintain-formal-verification-skill/SKILL.md)
- description: "Bring a project's formal verification back in line with the code after the code changes: find the commits that touched verified code, update the model, harness, or properties to describe the code as it is now, rerun, and say whether each failure is drift in the verification or a bug in the code. Use for /maintain-formal-verification-skill, "is the model still true to the code", or after merges and refactors that touched verified code without rechecking it."
- use when: Code covered by a project's formal verification skill changed without rechecking ("is the model still true to the code"); reports per check in sync / updated / bug / blocked. Follow-up of create-formal-verification-skill.
- needs: an existing project-local verify skill (any model checker, prover or code-level verifier) and git history
- side effects: retains edits only to verification files unless product changes are requested; runs checks and temporarily breaks real code to prove updated checks can fail, then drops the break

### maintain-verification-skill
- id: pstack:maintain-verification-skill (source path: pstack/skills/maintain-verification-skill/SKILL.md)
- description: "Periodic pass that keeps a project's verification skill and feature map honest: parallel source readers per feature, one live session driving every feature, at most one PR of proven corrections. Use for /maintain-verification-skill or "audit the verify skill"."
- use when: Periodic audit of the project's verify-<app> skill and feature map ("audit the verify skill"); follow-up of create-verification-skill.
- needs: an existing project-local verification skill with launch/drive sections and a feature map (usually `.cursor/skills/verify-*/`), read-only subagents per feature, and a drivable live app
- side effects: launches and drives every mapped feature, retains evidence after cleanup; edits only the verification skill's own directory, never product code; at most one PR of proven corrections

### make-bot-ui
- id: pstack:make-bot-ui (source path: pstack/skills/make-bot-ui/SKILL.md)
- description: "Use when building a custom UI (page, dashboard, buttons) that should wake a Grok Bot over a webhook, when the user must provide a webhook sender key, or when exposing that UI on Tailscale."
- use when: Build a custom page or dashboard whose buttons wake a "Grok Bot" through a webhook routine. Runtime-specific, not a general web scaffolder.
- needs: Cursor-bot runtime (`update_state`, `SendToUser` secret-request card, routines panel); Tailscale; sudo; cannot complete in the Claude Code copy
- side effects: creates a webhook routine (waits on any confirmation card), stores the sender key in server-side UI config, starts a server bound to 0.0.0.0 and probes the webhook; may install Tailscale via `curl | sudo sh` and run `tailscale up`

### no-comments
- id: pstack:no-comments (source path: pstack/skills/no-comments/SKILL.md)
- description: "Spawn Comment Sicko, fix accepted findings, and offer encodings for claimed constraints."
- use when: About to review a scoped change and want comments, suppressions and workaround justifications stripped by a reviewer that did not write them, with in-scope root-cause fixes. Not a lint and not a diff review (use interrogate).
- needs: diff or base branch (default main); a subagent tool that runs the plugin's `comment-sicko` agent (Cursor `Task`; Claude Code `Agent` through the harness copy). The agent is defined in `pstack/agents/comment-sicko.md`, outside `skills/`, so a copy of the skill directory alone does not bring it
- side effects: deletes comments and edits product code within the caller's scope; constraint encoding waits for interactive approval (caller preapproval for unattended/eval runs), but if not approved the comment is still deleted and reported open. Proven external constraints survive. Assume the comment-sicko subagent deletes comments itself (its agent file; README and guide call it read-only); the parent deletes constraint comments and edits code

### recall
- id: pstack:recall (source path: pstack/skills/recall/SKILL.md)
- description: "Reconstruct your recent working context from your own chat history, live state, and the shared record (user reports, prior fixes, incidents), then hand back a tight current-state brief. Use for 'recall my work on X', 'catch me up', 'what have I been working on', 'where did I leave off', before starting or resuming work."
- use when: "Catch me up" or "where did I leave off on X": rebuilds your recent context from your chats, PRs and the shared record into a capped brief and stops; no work done.
- not for: resuming one specific prior chat (session-pickup), habit capture (automate-me), or a human-readable work summary.
- needs: this workspace's chat transcripts (Cursor layout; Claude Code port maps to ~/.claude/projects), git, gh; subagents for larger chat corpora and one agent-mode investigator per available shared-record source. A named topic requires the shared-record sweep; unavailable MCP sources are skipped with disclosure.
- side effects: none; read-only.

### reflect
- id: pstack:reflect (source path: pstack/skills/reflect/SKILL.md)
- description: "Mine the active transcript for durable learnings and route each to a concrete edit on an existing skill. Use when the user says reflect."
- use when: End of session, you say "reflect": proposes skill edits from this conversation's corrections and stops for approval.
- needs: the active transcript; writable .cursor/skills or ~/.cursor/skills (Claude Code port: .claude/skills or ~/.claude/skills).
- side effects: after approval, copies a skill into a skills folder and edits the copy; never pushes or opens a PR.

### setup-pstack
- id: pstack:setup-pstack (source path: pstack/skills/setup-pstack/SKILL.md)
- description: "Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices."
- use when: First-time pstack setup, or changing which models pstack uses per role and at what reasoning budget. Model-invocable, unlike most pstack skills.
- needs: a way to list model slugs (subagent tool or pasted).
- side effects: overwrites ~/.cursor/rules/pstack-models.mdc (Claude Code port: ~/.claude/rules/pstack-models.md) after you confirm roles.

### sharpen
- id: pstack:sharpen (source path: pstack/skills/sharpen/SKILL.md)
- description: "Make a task deeper, not bigger, then rewrite the prompt. Use for /sharpen."
- use when: You have a rough task prompt and want it deeper, not bigger: answers four questions (what a top professional adds, rawest source, methods, an outside check) and returns a rewritten prompt for you to send; does not run the task.

### show-me-your-work
- id: pstack:show-me-your-work (source path: pstack/skills/show-me-your-work/SKILL.md)
- description: "Keep a reviewable decision trail for long-running or unattended work: a TSV log with one row per decision (what, why, evidence, result). Local by default; commit it when a reviewer needs the trail to trust the result. Use for /show-me-your-work, autonomous or multi-phase runs, or work a human reviews after stepping away."
- use when: Long-running or unattended work a human will review later: keeps an append-only decision log and ends with a cross-vendor "reviewed by" Attention section.
- needs: a subagent on another vendor's model (the Claude Code port falls back to the session model); the run's transcript.
- side effects: writes a local TSV (decisions.tsv or .audit/<task-slug>.tsv), uncommitted by default; commits it when a reviewer needs the trail to trust the result.

### statechart
- id: pstack:statechart (source path: pstack/skills/statechart/SKILL.md)
- description: "Check a TLA+ model of a system that moves between states, such as a product flow, a protocol, or a service, and draw it as a Mermaid statechart. The report gives the shortest path to each state that breaks a rule. Use for /statechart, or to show a bug as a path through states."
- use when: You want a stateful flow, protocol or service modelled in TLA+ and drawn as a Mermaid statechart, or a bug shown as the shortest path through states.
- needs: a TypeScript-capable runtime, mise and network on first run; Pele for rendered images.
- side effects: first run installs TLC and Java with mise; writes models, reports and charts to a scratch folder outside the repo. Image rendering installs `pele@1.9.0` outside the repo and writes SVGs.

### swarm
- id: pstack:swarm (source path: pstack/skills/swarm/SKILL.md)
- description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
- use when: "Swarm this" or any task wanting N parallel workers (sliced coverage, a race, a gauntlet, exploration): Frame, Fan out, Aggregate, Report, with evidence required from each worker.
- needs: a Task/subagent tool; Cursor cloud agents by default; worker model from the swarm-workers line written by setup-pstack.
- side effects: spawns many background agents (cost); workers get separate writable outputs when the assigned task writes. The skill itself does not direct a push.

### tdd
- id: pstack:tdd (source path: pstack/skills/tdd/SKILL.md)
- description: "Use only when the user explicitly asks for TDD, a failing test, or a regression test, OR when the bug has an obvious cheap local test target. Skip when the test path is unclear, expensive, integration-heavy, or not requested."
- use when: You asked for TDD or a regression test, or the bug has a cheap local test target: write the test, watch it fail for the intended reason, then the minimal fix. Skips when the test path is unclear. Same bare name as mattpocock-skills tdd. Prefers no new test to a bad one and avoids unrelated coverage expansion.
- needs: an existing test setup for the code path.

### teach
- id: pstack:teach (source path: pstack/skills/teach/SKILL.md)
- description: "Explain a body of work plainly so a person actually understands it. Runs the `how` and `why` skills and weaves what they find into one clear explanation. Use for 'teach me this', 'help me really understand X', 'explain this change or subsystem to me'."
- use when: "Teach me this" or "explain this change or subsystem": a paced plain explanation, diagram by diagram, built from how and why. Same bare name as a mattpocock-skills skill.
- needs: how and why skills; an image tool for spatial ideas.
- side effects: none to product code; requires generated images for spatial explanations, potentially a progressive series.

### technical-writing
- id: pstack:technical-writing (source path: pstack/skills/technical-writing/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Layered technical-writing standard: Diátaxis structure, Google developer style sentences, STE instruction rules, Global English syntax. Use for /technical-writing or when writing or reviewing docs, RFCs, readmes, PR descriptions, or commit messages."
- use when: Writing or reviewing docs, RFCs, READMEs, PR descriptions or commit messages: one Diataxis mode per document plus Google developer style and plain-English sentence rules. PR descriptions and commit messages explicitly skip the Diataxis layer. Your own commit/PR conventions should win over it. Also for padded or verbose docs ("cut every word that does no work"). It hands the AI-tell catalogue to `unslop`, so that part is missing where `unslop` is not installed.
- not for: product UI strings; use the product's copy guidelines.

### typescript-best-practices
- id: pstack:typescript-best-practices (source path: pstack/skills/typescript-best-practices/SKILL.md)
- description: "TypeScript best practices. Use when reading or editing any .ts or .tsx file."
- use when: You are reading or editing any .ts or .tsx file: rule table (discriminated unions, no `as`, unknown over any, schemas before guards, exhaustiveness). Still explicit-invoke only despite its paths glob.
- needs: assumes a runtime schema library in the repo.

### unslop
- id: pstack:unslop (source path: pstack/skills/unslop/SKILL.md)
- description: "Cut AI tells from any writing."
- use when: Prose reads like AI output (replies included): rewrites to cut AI patterns, meaning kept. Strict numbered rules (no dashes, one hedge); cited by teach, technical-writing and recall.

### why
- id: pstack:why (source path: pstack/skills/why/SKILL.md)
- description: "Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Returns a cited read on decisions and tradeoffs. Use how for runtime behavior."
- use when: "Why does X work this way", design rationale, regressions, postmortems: a cited read of decisions from commits and PR discussion; marks inferences. Runtime behavior is how, not why.
- needs: git history; probably gh for PR discussion.
- side effects: none; read-only.

## Records: pstack principle leaves (matching only; single-rule guidance)

### principle-attack-the-premise
- id: pstack:principle-attack-the-premise (source path: pstack/skills/principle-attack-the-premise/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply when two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that assumes it."
- use when: Two or more fixes that share one assumption failed the same check: write the shared premise down and test it directly before the next fix. First failure is fix-root-causes instead.

### principle-boundary-discipline
- id: pstack:principle-boundary-discipline (source path: pstack/skills/principle-boundary-discipline/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions."
- use when: Validation or nil checks scattered through internal code, or a network/CLI/framework adapter leaking transport types into core logic: parse at ingress, keep business logic pure. Also for try/catch and re-validation wrapped around trusted internal paths.

### principle-build-the-lever
- id: pstack:principle-build-the-lever (source path: pstack/skills/principle-build-the-lever/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, or a skill your subagents follow) instead of working by hand. The tool is the artifact a reviewer can rerun."
- use when: A non-trivial edit, migration, analysis or check would otherwise be done by hand: build a rerunnable script, codemod, generator or delegate skill, proven on the first unit.
- side effects: creates tooling files; rerunning can mutate targets

### principle-encode-lessons-in-structure
- id: pstack:principle-encode-lessons-in-structure (source path: pstack/skills/principle-encode-lessons-in-structure/SKILL.md)
- description: "Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime check, or script instead of more text."
- use when: The same correction or instruction is about to be written a second time: encode it as a lint, metadata flag, runtime check or script. The full repo-wide workflow is correct.

### principle-exhaust-the-design-space
- id: pstack:principle-exhaust-the-design-space (source path: pstack/skills/principle-exhaust-the-design-space/SKILL.md)
- description: "Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. Build 2-3 competing prototypes and compare side by side before committing."
- use when: Novel interaction or architecture with no precedent, or product feel that argument cannot settle: build 2-3 competing prototypes and compare before committing.

### principle-experience-first
- id: pstack:principle-experience-first (source path: pstack/skills/principle-experience-first/SKILL.md)
- description: "Apply when product, UX, or feature-scope tradeoffs come up. Choose user delight over implementation convenience; ship fewer polished features over more rough ones."
- use when: Feature-scope or UX tradeoff: choose polish over extra features; maintainers and library consumers count as users.

### principle-explain-the-number
- id: pstack:principle-explain-the-number (source path: pstack/skills/principle-explain-the-number/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply before you measure, and before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, a latency, or an eval result. Find what limits it, and rule out that it measured something other than the work you think."
- use when: Before measuring or trusting a speedup, regression, latency, throughput or eval number: write the decision first, find the limiter, rule out cached/skipped/error work. Hands performance numbers to benchmark-checklist.

### principle-fix-root-causes
- id: pstack:principle-fix-root-causes (source path: pstack/skills/principle-fix-root-causes/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply when debugging. Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate."
- use when: Debugging, especially when a fix is about to add a guard, retry, clamp or swallowed error at the symptom: reproduce, trace to the first wrong decision, fix there.

### principle-foundational-thinking
- id: pstack:principle-foundational-thinking (source path: pstack/skills/principle-foundational-thinking/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious."
- use when: Before writing logic: choosing core types and data structures, whether scaffolding precedes features, and what concurrent actors share.

### principle-guard-the-context-window
- id: pstack:principle-guard-the-context-window (source path: pstack/skills/principle-guard-the-context-window/SKILL.md)
- description: "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads."
- use when: Large outputs, long files, repeated reads or fan-out planning are filling the main thread: delegate bulk to subagents and keep summaries.
- needs: a delegation-capable harness

### principle-laziness-protocol
- id: pstack:principle-laziness-protocol (source path: pstack/skills/principle-laziness-protocol/SKILL.md)
- description: "Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem."
- use when: A refactor or diff is growing wrappers, abstractions, layers or signal threading: keep each decision in one source of truth (passing the result on as a simple flag is its own advice) and make the smallest change. It does not forbid config flags; for speculative options the nearer rule is principle-subtract-before-you-add ("no speculative validators, parsers, or guards"). Feature's mandatory arena overrides it; Prototype inverts it. Also when the agent built more than was asked.

### principle-make-operations-idempotent
- id: pstack:principle-make-operations-idempotent (source path: pstack/skills/principle-make-operations-idempotent/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries. Converge to the same end state regardless of partial prior runs."
- use when: A command, job or loop may retry or restart after a partial write, stale lock or half-claimed job: reconcile actual state to the goal so a second run or a crash converges.

### principle-migrate-callers-then-delete-legacy-apis
- id: pstack:principle-migrate-callers-then-delete-legacy-apis (source path: pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md)
- description: "Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers."
- use when: Introducing a new internal API while old callers remain and no external users depend on compatibility: migrate every caller and delete the old API in one wave. Wrong for public APIs. Also for deprecated wrappers and compatibility shims kept after their callers could move.

### principle-minimize-reader-load
- id: pstack:principle-minimize-reader-load (source path: pstack/skills/principle-minimize-reader-load/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply when reviewing or shaping code that's hard to trace. Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope."
- use when: Code a maintainer cannot trace quickly through wrappers or mutable state: collapse one-caller layers and shrink mutable scope until origin and mutability are answerable in 30 seconds. Also when the agent built more than was asked.

### principle-model-the-domain
- id: pstack:principle-model-the-domain (source path: pstack/skills/principle-model-the-domain/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files."
- use when: Every new behavior adds an if/else branch, a synchronized boolean or a repeated shape assumption across files: encode the domain as a state machine, typed model, table or reducer.

### principle-never-block-on-the-human
- id: pstack:principle-never-block-on-the-human (source path: pstack/skills/principle-never-block-on-the-human/SKILL.md)
- description: "Apply when tempted to ask 'should I do X?' on reversible work."
- use when: About to ask permission for a reversible execution choice during directed work: proceed and explain. Still confirms force-push, deleting production data and external messages; product direction stays human. The leaf for "stop asking, just do it" and needless confirmations. It also covers narrating instead of acting ("Proceed, then present. Do the work, show the result."). It removes no plan or review step that another skill imposes.

### principle-outcome-oriented-execution
- id: pstack:principle-outcome-oriented-execution (source path: pstack/skills/principle-outcome-oriented-execution/SKILL.md)
- description: "Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code."
- use when: A planned rewrite or migration with explicit phase checkpoints is piling up throwaway compatibility adapters: converge on the target architecture with declared, scoped, reversible breakage and full final verification.

### principle-prove-it-works
- id: pstack:principle-prove-it-works (source path: pstack/skills/principle-prove-it-works/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'"
- use when: About to declare done from a green compile, old output or another agent's report: run the feature, read the real value or inspect the diff instead.
- needs: the real artifact; project control skills (control-ui, control-cli, or a verify-* skill) where the surface is UI/CLI

### principle-redesign-from-first-principles
- id: pstack:principle-redesign-from-first-principles (source path: pstack/skills/principle-redesign-from-first-principles/SKILL.md)
- description: "Apply when integrating a new requirement into an existing design."
- use when: A new requirement is landing on an existing design and the tempting move is to bolt it on; read all affected files, ask what you would build from scratch with it, propagate through types, docs and examples, then deliver incrementally. Guidance only.

### principle-separate-before-serializing-shared-state
- id: pstack:principle-separate-before-serializing-shared-state (source path: pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply when concurrent actors might write to the same file, branch, key, or state object. Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant."
- use when: Several agents, workers or processes might write the same file, branch, key or state object: give each its own output and merge at read time; use a lock or single writer only for a real invariant. Guidance only; pairs with swarm.

### principle-sequence-verifiable-units
- id: pstack:principle-sequence-verifiable-units (source path: pstack/skills/principle-sequence-verifiable-units/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer."
- use when: A migration, sweep, run of similar edits, or a commit/PR stack: split into small units that each end checkable and do not advance until the current one is green. Guidance only.

### principle-subtract-before-you-add
- id: pstack:principle-subtract-before-you-add (source path: pstack/skills/principle-subtract-before-you-add/SKILL.md)
- description: "Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references first, then build on the simpler base."
- use when: You are ordering an addition, refactor or rewrite and want to delete dead code, redundant validators and stub references first, then build on the simpler base. The plugin's central "write less" rule. Guidance only. Also when the agent built more than was asked.

### principle-test-behavior-not-implementation
- id: pstack:principle-test-behavior-not-implementation (source path: pstack/skills/principle-test-behavior-not-implementation/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply when you write, change, or keep a test. Assert what the code's users can observe, so that the test fails when that behavior breaks and keeps passing when only the internals change."
- use when: You are writing, changing, keeping or reviewing a test: break the behavior (the test must fail), change internals only (it must still pass); rewrite or delete tests that fail either check. A test-quality rubric; tdd is the bug-fix procedure. It judges tests one at a time: redundant tests all pass it, so it does not shrink an over-tested suite.

### principle-type-system-discipline
- id: pstack:principle-type-system-discipline (source path: pstack/skills/principle-type-system-discipline/SKILL.md; an earlier upstream wording is longer, with the same name and description)
- description: "Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust variants, derive from authoritative schemas."
- use when: You are designing types, reviewing a function signature, or writing any statically typed language: brand primitives, parse external data at the boundary, derive from schemas. Language-agnostic; typescript-best-practices is the TS rule table.

## Family: harness (pstack's Claude Code host variant; note only, no records)
- source repo: https://github.com/cursor/plugins, directory `harness/pstack/claude-code/`: the Claude Code port of pstack, generated and never hand-edited. Its manifest copy matches pstack's (v0.15.43); the repo's Claude marketplace `cursor-plugins` lists it as plugin `pstack`. In Claude Code the skills are `pstack:<name>` and are typed `/pstack:<name>`; agents are `pstack:poteto-agent` and `pstack:comment-sicko`. Install: `/plugin marketplace add cursor/plugins`, then `/plugin install pstack@cursor-plugins`. No MCP, hooks or auth.
- relation to pstack: 58 skill names, the same as pstack. 36 `SKILL.md` files are byte-identical to `pstack/`; 22 add one paragraph telling the agent to read `docs/harness/claude-code.md` once per session before following the skill. The 22: architect, arena, automate-me, create-formal-verification-skill, create-verification-skill, figure-it-out, how, interrogate, maintain-formal-verification-skill, maintain-verification-skill, make-bot-ui, no-comments, poteto-help, poteto-mode, principle-type-system-discipline, recall, reflect, setup-pstack, show-me-your-work, swarm, teach, technical-writing. Verified by `cmp`.
- what the adapter changes: `Task` becomes `Agent`, `AskQuestion` becomes `AskUserQuestion`, `generalPurpose` becomes `general-purpose`, read-only becomes Explore plus a no-edit brief, `.cursor/skills` becomes `.claude/skills`, transcripts map to `~/.claude/projects`. Calling another pstack skill means reading its SKILL.md because the Skill tool refuses most of them. Claude slugs become `opus`/`sonnet`/`haiku`/`fable` plus effort with `-fast` dropped; non-Claude slugs run on the session model with disclosure, so this mapping does not guarantee cross-vendor reviews. `setup-pstack` writes `~/.claude/rules/pstack-models.md`. Cloud workers map to worktree isolation; only steps requiring the actual cloud agent service are skipped. Existing Bugbot checks/comments are handled through the forge; starting, waiting for or configuring Bugbot is skipped when the PR has no Bugbot check or comment. Cursor-only Automations and unsupported steps get a one-line `Skipped in Claude Code: ...` and the run continues. `/loop`, Custom Modes, `/deslop`, control-ui and control-cli have no adapter row: verify them before recommending playbooks that name them. `pstack/automations` (Benny) and `pstack/assets` are omitted.
- The source README says Claude Code leaves marketplace auto-update off for third-party marketplaces, so an installed copy can lag the source; platform behavior was not independently verified.
- router: poteto-mode and poteto-help, same as pstack. development distance: core-dev. disclosure recommendation: router-delegated; no separate records, reuse pstack's and add the one line "in Claude Code type /pstack:<name> and read the adapter first".
