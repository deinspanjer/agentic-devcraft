# cursor/plugins family: cursor-team-kit
Source: https://github.com/cursor/plugins @ e559e62b729e040186bc9d573e71255e5a96f50d
Distribution (cursor/plugins): the Cursor marketplace `cursor-plugins` (`.cursor-plugin/marketplace.json`); in Cursor, `/add-plugin <plugin>`. The same repository holds a Claude Code marketplace (`.claude-plugin/marketplace.json`; `/plugin marketplace add cursor/plugins`) that lists only `pstack` and `origin-apps`. Skill directories are `<plugin>/skills/<skill>/`. A "Cursor packaging only" manifest note describes packaging, not where a skill can run: the family header names the Cursor features (Task subagents, hooks, Canvas, rules) a skill depends on.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `cursor-team-kit` family. The catalog entry is in cursor.md. `cli-for-agents`, `continual-learning`, `thermos`, `thermo-nuclear-review` and the `pr-review-canvas` plugin, named in the records below, belong to other families in that catalog.

## Family: cursor-team-kit
- source repo: https://github.com/cursor/plugins, path `cursor-team-kit/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Ships a background `ci-watcher` agent (model: fast; reports every PR-attached check, fixes nothing), a `thermo-nuclear-code-quality-review` agent, and two always-applied rules (`no-inline-imports`, `typescript-exhaustive-switch`) that change how TypeScript is written wherever the plugin is active. README's "no third-party service integrations" means no bundled connector, not no GitHub: PR skills need `gh` and push rights.
- name collisions: `pr-review-canvas` is also the skill of the separate `pr-review-canvas` plugin (Cursor Canvas, model-invocable; this copy writes an HTML page and is explicit-only). `thermo-nuclear-code-quality-review` is byte-identical in `thermos`; recommend the thermos copy.
- router: none; no global router. Local sequences: `verify-this` picks `control-cli` or `control-ui` as measurement surface; `review-and-ship` and `new-branch-and-pr` are end-to-end entries that call no named skill.
- development distance: core-dev
- disclosure recommendation: rich: eighteen skills on genuinely different scenarios (review, shipping, CI, proof, upkeep, reporting) with no router; full records in a progressively disclosed file.

### check-compiler-errors
- id: cursor-team-kit:check-compiler-errors (source path: cursor-team-kit/skills/check-compiler-errors/SKILL.md)
- description: "Run compile and type-check commands and report failures"
- use when: Compile or type errors are blocking local checks or CI and the user wants them fixed.
- not for: `fix-ci` (red PR checks, pushes); `run-smoke-tests` (runtime end-to-end).
- needs: the repo's real compile and type-check commands, installed toolchain, editable source.
- side effects: local source edits only.
- part of: standalone: run, group errors by file and kind, fix highest-confidence first, repeat until clean or blocked.

### control-cli
- id: cursor-team-kit:control-cli (source path: cursor-team-kit/skills/control-cli/SKILL.md)
- description: "Build or adapt a local harness to drive, inspect, and profile an interactive CLI or TUI without external services. Use for CLI UX checks, startup regressions, memory leaks, hangs, prompt flows, or terminal demos."
- use when: Reproduce or profile an interactive CLI/TUI: hang, key or prompt flow bug, resize, startup slowdown, memory growth, or a repeatable terminal demo.
- not for: `cli-for-agents` (changes the CLI's contract); `control-ui` (browser/Electron); `verify-this` (adds baseline, comparison, verdict).
- needs: command and repro, the repo's own harness or tmux/Expect/Python/Node PTY; optional inspector or recorder.
- side effects: launches local processes, writes temporary artifacts and cleans them up; sends no credentials or destructive commands; adds a permanent test only if asked.
- part of: standalone; measurement surface for terminal claims inside `verify-this`.

### control-ui
- id: cursor-team-kit:control-ui (source path: cursor-team-kit/skills/control-ui/SKILL.md)
- description: "Build or adapt a local browser/CDP harness to drive and inspect a web, IDE, or Electron UI. Use for local UI verification, screenshots, accessibility snapshots, perf profiles, visual diffs, or reproducing UI bugs."
- use when: Drive a real web, Electron or IDE surface to reproduce a UI bug or capture focus, keyboard, render, screenshot, accessibility, trace, performance or memory evidence.
- not for: `run-smoke-tests` (runs an existing Playwright suite); `control-cli` (terminal only); `verify-this` (verdict on a claim).
- needs: documented local app start, existing browser tooling (Playwright, Cypress, etc.); Electron needs a supported debug port. Adds no Playwright dependency unless asked.
- side effects: starts app, browser and debug processes, writes temporary artifacts and cleans up; consent needed before storing privacy-sensitive screenshots or heaps.
- part of: standalone; measurement surface for UI claims inside `verify-this`.

### deslop
- id: cursor-team-kit:deslop (source path: cursor-team-kit/skills/deslop/SKILL.md)
- description: "Remove AI-generated code slop and clean up code style"
- use when: The branch diff has AI-style clutter: unneeded comments, abnormal defensive checks or try/catch, `any` casts that dodge types, deep nesting unlike the surrounding file.
- not for: abstraction layers, wrappers or other over-engineering (its focus list is comments, defensive checks, `any` casts and nesting); `thermo-nuclear-code-quality-review` (demands restructuring, edits nothing); `make-pr-easy-to-review` (history and description, no code).
- needs: git diff against main and the surrounding code's conventions.
- side effects: small local edits, behavior unchanged unless fixing a clear bug.
- part of: standalone.

### fix-ci
- id: cursor-team-kit:fix-ci (source path: cursor-team-kit/skills/fix-ci/SKILL.md)
- description: "Find failing PR checks, inspect logs or external check links, and apply focused fixes"
- use when: An existing PR or branch has failing checks and needs diagnosis and a focused fix to green.
- not for: `loop-on-ci` (checks still pending, flake and main-merge policy); `check-compiler-errors` (local only); `ci-watcher` agent (reports, fixes nothing).
- needs: active PR, `gh` with read/log access and push rights; external check links when not GitHub Actions.
- side effects: pushes a fix to the PR branch each iteration and triggers CI; the source has no ask-before-push step.
- part of: standalone loop: first actionable error, smallest fix, push, recheck via `gh pr checks`.

### fix-merge-conflicts
- id: cursor-team-kit:fix-merge-conflicts (source path: cursor-team-kit/skills/fix-merge-conflicts/SKILL.md)
- description: "Resolve merge conflicts non-interactively, validate build and tests, and finalize conflict resolution"
- use when: A merge is in progress with conflicted files and the tree must become buildable.
- not for: `review-and-ship` and `new-branch-and-pr` (both commit and push).
- needs: conflicted checkout, knowledge of both sides' intent, package manager and toolchain.
- side effects: edits and stages files and regenerates lockfiles; never pushes or tags; no broad refactors.
- part of: standalone; runs compile, lint and relevant tests before staging.

### get-pr-comments
- id: cursor-team-kit:get-pr-comments (source path: cursor-team-kit/skills/get-pr-comments/SKILL.md)
- description: "Fetch and summarize review comments from the active pull request"
- use when: The user wants outstanding reviewer feedback on the current branch's PR as a prioritized action list.
- not for: `pr-review-canvas` (explains the diff); `review-and-ship` (fresh review and changes).
- needs: a resolvable current-branch PR and some way to read review and discussion comments (no CLI named).
- side effects: none; read-only. No fixes, no replies posted.
- part of: standalone.

### loop-on-ci
- id: cursor-team-kit:loop-on-ci (source path: cursor-team-kit/skills/loop-on-ci/SKILL.md)
- description: "Monitor PR checks and fix failures until green. Uses gh pr checks as the source of truth for PR-attached checks."
- use when: Keep watching a PR and fixing failures until required checks are green, including checks still running.
- not for: `fix-ci` (known red check, shortest path); `ci-watcher` agent (status only).
- needs: PR on the current branch, git, `gh` with read/log and push access, repair toolchain.
- side effects: repeated pushes; may merge latest main for an unrelated failure already fixed there; retries a flaky failure once; never `--no-verify`.
- part of: standalone CI-loop entry point; inspect first, `gh pr checks --watch --fail-fast` for pending, recheck after every push.

### make-pr-easy-to-review
- id: cursor-team-kit:make-pr-easy-to-review (source path: cursor-team-kit/skills/make-pr-easy-to-review/SKILL.md)
- description: "Prepare PRs for review by cleaning noisy history, improving PR descriptions, and adding reviewer guidance without changing code behavior. Use for "make this easy to review", "tidy this PR", "clean up commits", or "annotate the diff"."
- use when: The user's own PR is noisy and needs tidier history, a clearer description, reviewer entry points or a split recommendation, with no behavior change.
- not for: `deslop` (edits code); `pr-review-canvas` (reader-side walkthrough that leaves the PR unchanged).
- needs: PR URL or current branch, git, `gh`, push permission.
- side effects: edits the PR description; rewrites history and force-pushes only after the user agrees to a proposed plan; checks the final tree matches the recorded original.
- part of: standalone.

### new-branch-and-pr
- id: cursor-team-kit:new-branch-and-pr (source path: cursor-team-kit/skills/new-branch-and-pr/SKILL.md)
- description: "Create a fresh branch, complete work, and open a pull request"
- use when: Start a scoped task from latest main and deliver it as a fresh pull request.
- not for: `review-and-ship` (starts from changes that already exist).
- needs: git checkout with remote access, push and PR-creation rights, requirements and toolchain.
- side effects: creates a branch, commits, pushes, opens a PR.
- part of: entry point of branch-to-PR: clean tree, branch from main, implement and test, focused commit, concise PR.

### pr-review-canvas
- id: cursor-team-kit:pr-review-canvas (source path: cursor-team-kit/skills/pr-review-canvas/SKILL.md)
- description: "Generate an interactive PR review walkthrough as an HTML page. Fetches PR data via gh API, categorizes files into core vs mechanical changes, adds reviewer annotations, and renders diffs with moved-code detection. Use when the user pastes a GitHub PR URL and asks for a review, walkthrough, or summary, or says "review this PR"."
- use when: The user pastes a GitHub PR URL and wants an interactive annotated HTML walkthrough (core versus mechanical files, moved-code detection, review checklist). Explicit invocation only.
- not for: `pr-review-canvas` in the `pr-review-canvas` plugin (Cursor Canvas version, model-invocable); `get-pr-comments`; `thermo-nuclear-review` (findings, not a reading surface).
- needs: PR owner/repo/number, `gh api`, `jq`, `python3`, a browser; bundled `styles.css`, `renderer.js`, `template.html`.
- side effects: writes diff patches to `/tmp/pr-patches-<n>.json` and HTML under `/tmp/pr-review-<n>*`; starts `python3 -m http.server 8432 --bind 127.0.0.1` from `/tmp` in the background (next port if taken), with no shutdown step specified, so `/tmp` remains served on loopback until the server stops. Posts nothing to GitHub.
- part of: standalone. Same frontmatter name as the plugin skill; the view drops import-only lines and folds whitespace, so it is filtered, not the raw diff.

### review-and-ship
- id: cursor-team-kit:review-and-ship (source path: cursor-team-kit/skills/review-and-ship/SKILL.md)
- description: "Review the current branch for bugs, intent fit, and test coverage; run or write tests; commit focused work; open or update a PR."
- use when: Existing branch changes need a correctness, security and intent review, critical fixes, tests, and delivery to a PR.
- not for: `thermo-nuclear-review`, `thermo-nuclear-code-quality-review` (review only, never ship); `new-branch-and-pr` (starts from main); `deslop` (cleanup only).
- needs: diff and base, tests and toolchain, git and `gh` with push and PR write access; parallel subagents for larger diffs.
- side effects: edits code and tests, commits, pushes, opens or updates a PR. "Review" here authorizes shipping.
- part of: entry point of review, verify/fix, ship; fixes critical findings and reruns tests; judges readiness from `gh pr checks`.

### run-smoke-tests
- id: cursor-team-kit:run-smoke-tests (source path: cursor-team-kit/skills/run-smoke-tests/SKILL.md)
- description: "Run Playwright smoke tests, debug failures, and verify fixes"
- use when: Run an existing Playwright smoke suite before or after a change, debug failures from traces and logs, and verify the fix.
- not for: `control-ui` (ad-hoc probe of one UI surface); `verify-this` (baseline versus treatment); `check-compiler-errors`.
- needs: a Playwright smoke suite and its build; examples assume npm scripts `smoketest` and `smoketest-no-compile`, which a repo may lack.
- side effects: local edits and reruns; quarantines a test only if explicitly asked.
- part of: standalone validation and fix loop.

### thermo-nuclear-code-quality-review
- id: cursor-team-kit:thermo-nuclear-code-quality-review (source path: cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)
- description: "Run an extremely strict maintainability review for abstraction quality, giant files, and spaghetti-condition growth. Use for a thermo-nuclear code quality review, thermonuclear review, deep code quality audit, or especially harsh maintainability review."
- use when: The user explicitly asks for a deliberately harsh maintainability audit of branch changes: abstraction quality, files crossing 1,000 lines, spaghetti branching. Explicit invocation only.
- not for: `thermo-nuclear-review` (bugs and security); `deslop` (minimal cleanup); `review-and-ship`; same-named skill in `thermos` (byte-identical copy). Not a cure for over-engineered code: it pushes for deletion where it can, but also for moving conditionals into a dedicated abstraction, helper, state machine or policy object and for splitting files near 1,000 lines.
- needs: branch diff plus full changed-file contents and before/after sizes; optional bundled review agent.
- side effects: none; read-only. Findings and an approval judgment; edits nothing.
- part of: standalone rubric. Byte-identical to `thermos:thermo-nuclear-code-quality-review`; the thermos README says it moved there, so prefer that copy if both are installed.

### verify-this
- id: cursor-team-kit:verify-this (source path: cursor-team-kit/skills/verify-this/SKILL.md)
- description: "Verify a claim with fresh local evidence: restate it falsifiably, capture baseline and treatment, compare artifacts, and return VERIFIED, NOT VERIFIED, or INCONCLUSIVE."
- use when: "Prove this fix works", "did latency or memory improve", "show before and after" for one measurable claim.
- not for: `run-smoke-tests` (suite pass/fail, no baseline); `thermo-nuclear-code-quality-review` (judges structure, not a measurable claim).
- needs: a falsifiable claim with metric and threshold, a valid old-state baseline, matched command, data and environment, local measurement tooling.
- side effects: runs the app, tests or profiles; writes `/tmp/verify-this/<claim-slug>/` when safe (sensitive artifacts stay inline unless the user agrees).
- part of: entry point of the evidence sequence; delegates measurement to `control-cli` or `control-ui`. Ends in exactly VERIFIED, NOT VERIFIED or INCONCLUSIVE; ships nothing.

### weekly-review
- id: cursor-team-kit:weekly-review (source path: cursor-team-kit/skills/weekly-review/SKILL.md)
- description: "Produce a weekly synthesis of authored commits with highlights by bugfix, tech debt, and net-new work"
- use when: A weekly status, retro or planning recap of the user's own commits from the last 7-10 days, grouped as bugfix, tech debt and net-new work.
- not for: `what-did-i-get-done` (any stated period, no weekly classification); `workflow-from-chats` (preferences, not accomplishments).
- needs: git history and the configured git user email (it asks the user to set one if missing).
- side effects: none; read-only git. Excludes merge commits.
- part of: standalone.

### what-did-i-get-done
- id: cursor-team-kit:what-did-i-get-done (source path: cursor-team-kit/skills/what-did-i-get-done/SKILL.md)
- description: "Summarize authored commits over a user-specified time period into a concise update"
- use when: A short accomplishment update for yesterday, the last three days or another stated interval.
- not for: `weekly-review` (fixed 7-10 day window with bugfix/tech-debt/net-new framing).
- needs: requested time window, git authored history and the user's git email (no rule if it is unset; sibling `weekly-review` asks the user to set it, so say to set `git config user.email` first).
- side effects: none; read-only git. Excludes merges, uncommitted work and cosmetic-only changes.
- part of: standalone.

### workflow-from-chats
- id: cursor-team-kit:workflow-from-chats (source path: cursor-team-kit/skills/workflow-from-chats/SKILL.md)
- description: "Extract durable working preferences from recent Cursor chats and convert them into skills, rules, or workflow docs. Use when asked to learn preferences, mine feedback, personalize workflows, or generate team/person-specific agent guidance."
- use when: Turn recurring feedback in recent Cursor chats (default last 7 days) into reusable guidance for shipping, review, debugging or delegation.
- not for: `continual-learning` (keeps two bounded `AGENTS.md` sections fresh on a cadence); `weekly-review` (recap).
- needs: Cursor parent and subagent transcripts and a target workflow; where artifacts are written is not specified.
- side effects: reads chat transcripts (cites parent chats only, no local paths or private data); drafts a skill, rule or workflow doc or none; contradicted evidence means ask before writing.
- part of: standalone: rate evidence strong/medium/weak/contradicted, then choose artifact type.
