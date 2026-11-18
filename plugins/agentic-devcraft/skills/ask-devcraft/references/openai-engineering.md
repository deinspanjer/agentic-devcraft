# openai/plugins: engineering workflow, security, review, CI, observability and agent tooling
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Source: https://github.com/CrowdStrike/foundry-skills @ 5037f4a6ebf5518140572718e9f6226fa0605809
Source: https://github.com/CrowdStrike/fusion-skills @ 89980d207b3db841d9a5026d71833ccc4972450e
Source: https://github.com/qodo-ai/qodo-skills @ 80240e3f5b40d4b8e39935926770f7be0ddb5cde
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Plugins from the OpenAI marketplace that support the engineering loop itself: a development-discipline workflow, security scanning, code review, CI, error and product analytics, and tooling for building agents, skills and plugins. Three families are hosted outside openai/plugins and reached through its marketplace: `crowdstrike-falcon-foundry`, `crowdstrike-falcon-fusion` and `qodo`; their marketplace entries carry no `ref`, so the commits above are the curated snapshot, not a pin. App building and vendor developer platforms are in openai-platforms.md, which also lists the far families and the marketplace entries that ship no skills.

Reading the records: a record heading is the host-visible skill name (the SKILL.md frontmatter `name`); `id` is `<plugin>:<skill directory>` followed by the SKILL.md path inside the source repository; `description` quotes the frontmatter description (whitespace collapsed), so compare it with an installed skill's description to establish that the installed copy is the one recorded here. Full records carry `use when`, `not for`, `needs`, `side effects` and `part of`; short records omit fields with nothing to state. A family marked router-delegated keeps its routing in the `router` line: when that router is installed, hand the task to it instead of re-deriving the route from the short records.

Families in order. Core-dev: `superpowers`, `codex-security` (families/codex-security.md), `coderabbit`, `qodo`, `circleci`, `sentry`, `openai-developers` (families/openai-developers.md), `crowdstrike-falcon-foundry`. Adjacent: `plugin-eval`, `plugin-creator`, `posthog`, `mixpanel-headless`, `openai-ads-conversions`, `data-analytics`, `crowdstrike-falcon-fusion`.

## Family: superpowers
- source path: `plugins/superpowers`
- manifest notes: v6.3.0, author Jesse Vincent. Marketplace policy: products CODEX only, authentication ON_INSTALL. No MCP, connectors or hooks (`hooks` is empty). Skill text names Claude Code, Codex CLI/App, Copilot CLI and Gemini CLI as subagent-capable harnesses, and Codex needs `multi_agent = true` for subagent skills. Some skills bundle scripts and prompt templates; brainstorming offers an optional browser "visual companion". defaultPrompts: "I've got an idea for something I'd like to build."; "Let's add a feature to this project."
- router: `using-superpowers` covers the whole plugin. Rule: invoke any skill with even a 1% chance of relevance BEFORE any response, including clarifying questions; process skills (`brainstorming`, `systematic-debugging`) before implementation skills; ignored by dispatched subagents; user instructions (AGENTS.md, direct requests) override skills. Architectural sequence: `brainstorming` (HARD-GATE: no code until the user approves; commits a spec) -> `writing-plans` -> `using-git-worktrees` -> `subagent-driven-development` (or `executing-plans` without subagents), using `test-driven-development` per task and `requesting-code-review` -> `verification-before-completion` -> `finishing-a-development-branch`. Brainstorming's bounded path implements after approval without a plan document; its spike path returns a recommendation with any code labeled throwaway. Side branches: `systematic-debugging` for any bug, `receiving-code-review`, `dispatching-parallel-agents`, `writing-skills`. Aggressive: it forces skill invocation even for simple questions, so recommend the whole plugin only to a user who wants that discipline; a user who wants one discipline should get that single skill. In Falcon Foundry app repos, the Foundry plugin's orchestrator replaces `brainstorming` and `writing-plans`.
- development distance: core-dev
- disclosure: router-delegated. `using-superpowers` already sequences every skill, so records stay one-liners for matching.

### using-superpowers
- id: superpowers:using-superpowers (source path: plugins/superpowers/skills/using-superpowers/SKILL.md)
- description: "Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions"
- use when: Start of any conversation: the plugin router; forces skill invocation before any response, ignored by subagents, overridden by user instructions.

### brainstorming
- id: superpowers:brainstorming (source path: plugins/superpowers/skills/brainstorming/SKILL.md)
- description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
- use when: I have an idea, want to add a feature, or ask "can we...?": design first; no code until the user approves (spike, bounded, or architectural path).
- not for: a small change you just want made: the approval gate applies to every task on every path, a config change included, and when in doubt it takes the heavier path. Misapplied it is a source of ceremony.
- side effects: On the architectural path writes and commits a spec to `docs/superpowers/specs/` and hands off only to `writing-plans`. Bounded work implements after approval without a plan document; spikes may create approved throwaway code.

### writing-plans
- id: superpowers:writing-plans (source path: plugins/superpowers/skills/writing-plans/SKILL.md)
- description: "Use when you have a spec or requirements for a multi-step task, before touching code"
- use when: An approved spec for a multi-step task: write a bite-sized plan at `docs/superpowers/plans/`, then choose `subagent-driven-development` or `executing-plans`.

### using-git-worktrees
- id: superpowers:using-git-worktrees (source path: plugins/superpowers/skills/using-git-worktrees/SKILL.md)
- description: "Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback"
- use when: Need an isolated workspace before feature work or plan execution; used by both executors.
- side effects: Creates a worktree unless already isolated or the user declines; asks before creation unless a preference is declared. Automatically installs dependencies, runs baseline tests, and may commit a `.gitignore` change.

### subagent-driven-development
- id: superpowers:subagent-driven-development (source path: plugins/superpowers/skills/subagent-driven-development/SKILL.md)
- description: "Use when executing implementation plans with independent tasks in the current session"
- use when: Execute a plan of mostly independent tasks in this session when subagents are available (recommended executor).
- not for: a small change: every task gets a spec-and-quality review with up to five fix rounds, then a whole-branch review.
- needs: A subagent-capable harness (Codex needs `multi_agent = true`), a plan file, git.
- side effects: Many commits; runs without pausing between tasks and stops for destructive or security-sensitive actions, outside-worktree actions requiring approval, or a plan so broken that every path forward is a guess; deletes its plan-specific scratch workspace at the end.

### executing-plans
- id: superpowers:executing-plans (source path: plugins/superpowers/skills/executing-plans/SKILL.md)
- description: "Use when you have a written implementation plan to execute in a separate session with review checkpoints"
- use when: Execute a written plan inline in one session; fallback when subagents are unavailable (its text says to prefer `subagent-driven-development` when they are).

### test-driven-development
- id: superpowers:test-driven-development (source path: plugins/superpowers/skills/test-driven-development/SKILL.md)
- description: "Use when implementing any feature or bugfix, before writing implementation code"
- use when: Implementing any feature, bugfix or refactor: red-green-refactor with a failing test first; code written before its test is deleted.
- not for: a suite that is already over-tested: its checklist requires a test for every new function or method and lists "too simple to test" as a rationalization, so misapplied it is a source of test bloat.
- needs: A runnable test framework.

### systematic-debugging
- id: superpowers:systematic-debugging (source path: plugins/superpowers/skills/systematic-debugging/SKILL.md)
- description: "Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes"
- use when: Any bug, test or build failure or unexpected behavior: find the root cause before any fix; after three failed fixes question the architecture with the user.

### dispatching-parallel-agents
- id: superpowers:dispatching-parallel-agents (source path: plugins/superpowers/skills/dispatching-parallel-agents/SKILL.md)
- description: "Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies"
- use when: Two or more independent failures or tasks sharing no state: one subagent per problem, then integrate and run the full suite.
- needs: Subagent support.

### requesting-code-review
- id: superpowers:requesting-code-review (source path: plugins/superpowers/skills/requesting-code-review/SKILL.md)
- description: "Use when completing tasks, implementing major features, or before merging to verify work meets requirements"
- use when: A task or feature is done or about to merge: dispatch a reviewer subagent with the base and head SHAs and fix Critical and Important findings.
- needs: Subagent support and git SHAs.

### receiving-code-review
- id: superpowers:receiving-code-review (source path: plugins/superpowers/skills/receiving-code-review/SKILL.md)
- description: "Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation"
- use when: Review feedback (user, reviewer, GitHub PR comments) is about to be acted on: verify each item, clarify unclear ones first, push back technically.
- needs: `gh` to reply in PR comment threads.

### verification-before-completion
- id: superpowers:verification-before-completion (source path: plugins/superpowers/skills/verification-before-completion/SKILL.md)
- description: "Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always"
- use when: About to say work is done, fixed or passing, or to commit or open a PR: run the proving command fresh and read the output first.

### finishing-a-development-branch
- id: superpowers:finishing-a-development-branch (source path: plugins/superpowers/skills/finishing-a-development-branch/SKILL.md)
- description: "Use when implementation is complete, all tests pass, and you need to decide how to integrate the work"
- use when: Implementation is complete and tests pass: choose merge locally, push and open a PR, or keep as is; terminal step of both executors.
- needs: Git, a test command, `gh` or the forge CLI for PRs.
- side effects: Merges, pushes, opens PRs, deletes branches, removes worktrees under `.worktrees/` or `worktrees/`; never force-pushes; discard only on explicit typed confirmation.

### writing-skills
- id: superpowers:writing-skills (source path: plugins/superpowers/skills/writing-skills/SKILL.md)
- description: "Use when creating new skills, editing existing skills, or verifying skills work before deployment"
- use when: Creating, editing or verifying a skill, test-first with subagent pressure scenarios.
- needs: `test-driven-development` as background; subagents.

## Family: codex-security
- router: none. Three scan entry skills: `security-scan` (whole repo or path, one pass), `deep-security-scan` (multi-pass), `security-diff-scan` (PR, commit, branch or working-tree diff, which runs the four phase skills).
- covers: Codex Security: repository and diff vulnerability scans, threat models, triage of imported findings, fix and verify, patch merge risk, tracker filing, disclosure writeups, hardening proposals and SECURITY.md policy. Codex-only marketplace entry with a bundled `codex-security` MCP server; other hosts fall back to a terminal workflow.
- development distance: core-dev
- skills (15): `security-scan`, `deep-security-scan`, `security-diff-scan`, `threat-model`, `finding-discovery`, `validation`, `attack-path-analysis`, `define-security-policy`, `triage-finding`, `fix-finding`, `verify-fix`, `assess-patch-risk`, `track-findings`, `vulnerability-writeup`, `propose-security-hardening`
- Full records: families/codex-security.md

## Family: coderabbit
- source path: `plugins/coderabbit` (v1.1.4; upstream coderabbitai/codex-plugin)
- manifest notes: Codex-only marketplace entry; no MCP or app connector; depends on the external `coderabbit` CLI, which the skill installs via a downloaded shell installer if missing.
- router: none
- development distance: core-dev
- disclosure: simple. One skill.

### code-review
- id: coderabbit:coderabbit-review (source path: plugins/coderabbit/skills/coderabbit-review/SKILL.md)
- description: "Reviews code changes using CodeRabbit AI. Use when user asks for code review, PR feedback, code quality checks, security issues, or requests fix-review cycles."
- use when: Run CodeRabbit on my changes or PR diff, get severity-ordered issues with fixes, then optionally implement them.
- not for: workers-best-practices (Workers-specific review); circleci-builds (a failing CI run). Name `code-review` is generic: match by this description.
- needs: a git repo, the `coderabbit` CLI, passing `coderabbit auth status --agent`, network.
- side effects: sends the diff to CodeRabbit's service; installs the CLI via `curl | sh` and logs in if absent; fixes edit local files. A CLI failure stops with no manual-review fallback.
- part of: standalone.

## Family: qodo
- source repo: https://github.com/qodo-ai/qodo-skills, git-subdir `codex-packages/qodo` (no `ref` in the OpenAI entry). Curated at commit 80240e3f5b40d4b8e39935926770f7be0ddb5cde (plugin v2.3.1). 5 skills.
- distribution: a `git-subdir` source (`codex-packages/qodo`) in the openai/plugins Codex marketplace. The qodo-ai/qodo-skills repository also carries its own marketplace `qodo` for Claude Code (`packages/qodo`) and Codex (`codex-packages/qodo`).
- manifest notes: only a Codex manifest (`.codex-plugin/plugin.json`) and root `plugin.json`; no MCP server, app connector, hooks, agents or commands, and no auth policy in the package. Needs the Qodo CLI >= 2.0.0 (`qodo read ...`, `qodo review`, `qodo pr-review-session ...`, `qodo review-notes ...`) or a host-connected "QAR managed-tools" MCP server that this package does not define, plus a signed-in Qodo account and an organization deployment with indexed repositories. `qodo review` is closed preview (org enrolment; otherwise the skill stops). The skills never handle credentials or request API keys. On the CLI path, every skill first runs `qodo --version` and requires >= 2.0.0; connected MCP paths skip CLI probes, login and catalog refresh.
- security caveats that affect recommending it: no hooks; unpinned install (no `ref`). qodo-review sends the diff, untracked files and session context to Qodo's service; qodo-review-resolver status writes change Qodo's review database and release the merge-policy block (each needs separate explicit approval); qodo-review-notes publishes notes visible to other sessions and reviewers; qodo-setup may install or update a CLI after asking.
- router: none. Loose relationships: qodo-setup is the prerequisite every skill hands to on a missing CLI or login; qodo-review (local, pre-PR) -> qodo-review-notes (before opening the PR) -> qodo-review-resolver (findings on the PR); qodo-review-resolver reads non-local code through qodo-codebase-wisdom. A review of an unchanged pushed snapshot is not duplicated.
- development distance: core-dev (code review, codebase history, PR upkeep).
- disclosure: simple; five skills from one vendor, all gated on the same Qodo CLI/account.

### qodo-setup
- id: qodo:qodo-setup (source path: codex-packages/qodo/skills/qodo-setup/SKILL.md)
- description: "Set up Qodo in a coding agent — install the CLI, sign in, and verify tools. Use after plugin installation, on setup requests, or when a Qodo skill finds a missing CLI or login."
- use when: Qodo was just added, the user asks to set up or connect Qodo, or another Qodo skill reports a missing CLI or login.
- needs: a shell (or a host-connected QAR managed-tools MCP); host approval to install the Qodo CLI (>= 2.0.0); sign-in goes through the CLI.
- side effects: may install or update the Qodo CLI with covering authorization or one approval request, then refreshes the tool catalog (`qodo tools --refresh`) only after identity is verified; MCP-only setup uses a harmless read and hands back; never handles credentials.
- part of: prerequisite for the other four skills, which hand to it on a missing CLI or login; returns to the original task.

### qodo-codebase-wisdom
- id: qodo:qodo-codebase-wisdom (source path: codex-packages/qodo/skills/qodo-codebase-wisdom/SKILL.md)
- description: "Understand how code works, how a change was done before, and which repos are coupled — to answer a question, plan a code change, debug a regression, or scope a fix, using Qodo managed tools through MCP or the CLI. Use when a task needs to understand a codebase, its history, or how its repos relate — especially for a repo you don't have checked out or work spanning repos — "how does X work", "where is X defined", "who changed X", "explain this service", "plan the change for X", "what would changing X affect", "which repos depend on X", "why did X regress / when did it break", "has this been fixed before", "how did we solve X"."
- use when: "How does X work, who changed it and why, which repos depend on it, has this been fixed before", especially for repos not checked out or work spanning repos.
- not for: local grep or the IDE for exact branch, uncommitted changes, edits or tests; qodo-review-resolver for a PR's review findings.
- needs: Qodo CLI >= 2.0.0 signed in, or a connected QAR MCP; indexed repositories in the user's Qodo deployment.
- side effects: none; read-only, cited answers (repo, path:line, PR, SHA); never calls the write tools.
- part of: standalone; qodo-review-resolver uses it for code that is not local.

### qodo-review
- id: qodo:qodo-review (source path: codex-packages/qodo/skills/qodo-review/SKILL.md)
- description: "Review local changes with Qodo during substantive coding milestones and before a PR or completed-work handoff. Use light background checkpoints while coding, collect and assess findings with session context, and run a final review before handing off. Also use for "review my local diff", "pre-PR review", or "run qodo review". Use qodo-review-resolver for findings already posted on a PR."
- use when: "Review my local diff" or review local changes, including unpushed work on an existing PR, with light checkpoints while coding and a final review before handoff.
- not for: qodo-review-resolver (findings already posted on a PR).
- needs: Qodo CLI >= 2.0.0 signed in with review API v2, or MCP `start-pre-pr-review` plus a tested local input collector with equivalent scope/exclusions; base commit on the remote; `qodo review` is closed preview (needs org enrolment, otherwise it stops).
- side effects: sends the diff, untracked files and session context to Qodo; writes local context files and, during coding, commits task changes before review only under the user's commit policy (review-only or unauthorized commits are skipped). Applies fixes and stored dismissals only with their respective authorization; never pushes or posts.
- part of: step before opening a PR; pairs with qodo-review-notes, then qodo-review-resolver once the PR exists.

### qodo-review-resolver
- id: qodo:qodo-review-resolver (source path: codex-packages/qodo/skills/qodo-review-resolver/SKILL.md)
- description: "Read or resolve a pull request's Qodo review using Qodo managed tools through MCP or the CLI — fetch structured status, reviewed commit SHA, and findings for ANY PR as JSON, with optional extended details and citation evidence for audits, then optionally resolve open findings and record outcomes, once or until clean. Use this — never `gh`/`curl` scraping of review comments — for "is the review clean on PR #N", "get Qodo's findings for <pr> as JSON", "audit the review evidence", "show finding citations", "what did Qodo flag", "is this review up to date with head", "check before merging", "resolve my PR review", "fix the review findings", or "babysit this PR until it's clean"."
- use when: "Is the Qodo review clean on PR #N", "what did Qodo flag", resolve the open findings, or babysit the PR until clean.
- not for: qodo-review (local, unpushed changes).
- needs: authenticated Qodo CLI >= 2.0.0 with review API v2, or QAR MCP; exact PR URL and head SHA; resolution requires a completed current-head review. To edit code, the checkout must match the PR repository and reviewed head (or a verified descendant produced by this same fix workflow).
- side effects: fixes need authorization; `dismiss` and `mark-implemented` need separate explicit approval and change Qodo's review database, restyle PR comments and release the merge-policy block; never scrapes comments with gh or curl; asks before pushing.
- part of: step after qodo-review once the PR exists; uses qodo-codebase-wisdom for non-local code.

### qodo-review-notes
- id: qodo:qodo-review-notes (source path: codex-packages/qodo/skills/qodo-review-notes/SKILL.md)
- description: "Preserve reasoning for independent review of plans and PRs through Qodo notes tools. Use during substantive planning and development, when decisions, scope or validation change, when resuming or handing off work, and before opening or updating a PR. Tracks hold the evolving plan across issues and repositories; PR notes explain one change. Also use to read or maintain reviewer context. This skill does not review or approve a plan or code, implement it, or open a PR."
- use when: Preserve plan, decisions and validation for reviewers and later sessions: resuming or handing off work, or before opening or updating a PR (Development Track notes and PR notes).
- not for: qodo-review (reviews code) and qodo-review-resolver (reads findings).
- needs: Qodo CLI >= 2.0.0 with `localGitCapture: true` for PR notes, or a trusted MCP; a connected workspace and registered repositories.
- side effects: authorized maintenance writes drafts or publishes notes visible to other sessions and reviewers (no secrets); read/review requests alone grant no write authority, and draft-only instructions are preserved. It does not commit, push, open the PR or review code.
- part of: supporting step before the PR (`prepare-pr`, then the PR is opened, then `bind-pr`); entered from qodo-review; missing credentials go to qodo-setup.

## Family: circleci
- source path: `plugins/circleci` (v1.0.4; upstream circleci-public/skills)
- manifest notes: no MCP or app connector bundled (a CircleCI MCP is only mentioned as an optional external log source); no manifest-level auth policy beyond marketplace ON_INSTALL; not host-restricted. Only `chunk` needs real onboarding (GitHub App, tokens, Homebrew).
- router: none. `chunk` only routes inside itself: classify UI / CLI / mixed -> confirm repo, branch, GitHub integration and model provider -> load chunk-ui.md or chunk-cli.md -> report blockers and next safest action. The other three are separate entry points.
- development distance: core-dev
- disclosure: simple. Four skills with clearly separate triggers.

### circleci-builds
- id: circleci:builds (source path: plugins/circleci/skills/builds/SKILL.md)
- description: "Diagnose and fix failing CircleCI builds quickly and safely. Use when users ask to investigate failed CircleCI jobs, triage flaky pipelines, identify root causes from logs, and implement minimal fixes in configuration, test setup, or build-related code paths."
- use when: A CircleCI job is red or a pipeline fails intermittently and I want the first real cause found and fixed with a minimal patch.
- not for: circleci-cli (status, rerun, trigger commands only); circleci-config (systemic slowness or waste); chunk (CircleCI's own agent does the repair).
- needs: failing pipeline/job, branch, SHA, first failing step and logs, whether the same commit passes on rerun.
- side effects: writes local config/test/code patches; may rerun CI.
- part of: standalone. Classifies transient vs deterministic before any retry.

### chunk
- id: circleci:chunk (source path: plugins/circleci/skills/chunk/SKILL.md)
- description: "Use CircleCI Chunk for AI-assisted CI/CD work through either the Chunk web UI or the chunk-cli. Trigger this skill when users ask to set up Chunk, troubleshoot or fix failing builds with Chunk, configure Chunk environments, schedule/proactively run Chunk tasks, or use chunk-cli commands such as init, validate, build-prompt, auth, sandbox, task, and skill install."
- use when: Turn on CircleCI's Chunk agent, use its Fix buttons, schedule repo maintenance, set its environment, or run `chunk` CLI tasks and sandboxes.
- not for: circleci-builds (you diagnose and repair, no hosted agent); circleci-cli (the `circleci` CLI).
- needs: CircleCI GitHub App on the org, "Allow Chunk tasks", a model provider. CLI path: Homebrew, gh auth, CIRCLE_TOKEN. Beta; sandboxes may be private preview.
- side effects: launches cloud tasks and sandboxes; may configure project hooks.
- part of: entry router for Chunk (UI / CLI / mixed); no mandatory chain of other skills.

### circleci-cli
- id: circleci:cli (source path: plugins/circleci/skills/cli/SKILL.md)
- description: "Operate and troubleshoot CircleCI using the CircleCI CLI. Use when users ask to authenticate CLI access, inspect pipeline/workflow/job status, validate configuration locally, rerun pipelines/jobs, trigger pipelines, or gather actionable diagnostics from CLI outputs."
- use when: Show this pipeline's status, authenticate the CircleCI CLI, validate config locally, or rerun/trigger a pipeline or job.
- not for: circleci-builds (cause analysis and repair); circleci-config (redesigning config); chunk (the separate `chunk` CLI).
- needs: installed `circleci` CLI, token and org permissions for remote calls, branch/project slug. If the installed CLI lacks a cloud-log command, use the CircleCI UI or an external CircleCI MCP.
- side effects: rerun, trigger or cancel changes pipeline state and can run downstream deploy jobs.
- part of: standalone. Checks `--help` for available commands; read-only diagnostics before mutations.

### circleci-config
- id: circleci:config (source path: plugins/circleci/skills/config/SKILL.md)
- description: "Optimize CircleCI configuration for speed, reliability, and maintainability. Use when users ask to improve `.circleci/config.yml`, reduce CI runtime, tune caching/workspaces/parallelism, remove pipeline waste, or fix flaky pipeline behavior caused by configuration choices."
- use when: CI is slow or expensive: caches miss, jobs rebuild identical artifacts, test parallelism is unbalanced, or release/schedule filters waste runs in `.circleci/config.yml`.
- not for: circleci-builds (an active failing run); circleci-cli (run commands, not design); web-perf (page-load speed, not CI runtime).
- needs: `.circleci/` YAML, slowest-job and runtime baseline; timing-based test splitting needs JUnit XML uploaded via `store_test_results`.
- side effects: edits CI config, which changes build, test and deploy filtering.
- part of: standalone. Baseline first, then waste removal, artifact flow, parallelism; keeps deploy approval gates.

## Family: sentry
- source path: `plugins/sentry` (v0.1.2, author OpenAI)
- manifest notes: `.mcp.json` declares the hosted Sentry MCP (https://mcp.sentry.dev/mcp) but the skill never uses it; it calls the Sentry API through a bundled Python script. Manifest lists a Write capability while the skill is strictly read-only. Not host-restricted.
- router: none
- development distance: core-dev
- disclosure: simple. One skill.

### sentry
- id: sentry:sentry (source path: plugins/sentry/skills/sentry/SKILL.md)
- description: "Use when the user asks to inspect Sentry issues or events, summarize recent production errors, or pull basic Sentry health data via the Sentry API; perform read-only queries with the bundled script and require `SENTRY_AUTH_TOKEN`."
- use when: What is erroring in production? Show recent Sentry issues and events and summarize the top errors.
- not for: no in-plugin alternative; changing Sentry state or using the Sentry MCP's tools is outside this skill.
- needs: `SENTRY_AUTH_TOKEN` with read scopes (project:read, event:read, org:read) in the environment, python3, network, and real org/project names (defaults are literal placeholders). Defaults: last 24h, env prod, 20 results.
- side effects: none; GET-only. Redacts emails and IPs, shows no raw stack traces, never asks for the token in chat.
- part of: standalone. Reports only; no triage or resolution.

## Family: openai-developers
- router: none. Credential gate: for OpenAI-backed or provider-unspecified AI work, `openai-platform-api-key` runs before any design, code, scaffolding or smoke test; then `agents-sdk` or `build-chatgpt-app`; `openai-api-troubleshooting` after a runtime failure.
- covers: Building on the OpenAI platform: API key gate, OpenAI Agents SDK apps, ChatGPT apps and their submission, API error triage. Codex-only marketplace entry. `agents-sdk` shares its host-visible name with Cloudflare's `agents-sdk`.
- development distance: core-dev
- skills (5): `openai-platform-api-key`, `agents-sdk`, `build-chatgpt-app`, `chatgpt-app-submission`, `openai-api-troubleshooting`
- Full records: families/openai-developers.md

## Family: crowdstrike-falcon-foundry
- source repo: https://github.com/CrowdStrike/foundry-skills.git (url source in openai/plugins; no `ref` there). Curated at commit 5037f4a6ebf5518140572718e9f6226fa0605809 (plugin v1.7.1); upstream `main` was 593a9b30249d24130585b1362c64c4fcf4bb862b, which differs only in one reference-file line (no SKILL.md change). 14 skills.
- distribution: a `url` source in the openai/plugins Codex marketplace. The CrowdStrike/foundry-skills repository also carries its own marketplace `foundry-marketplace` for Claude Code and Codex, and a Cursor manifest.
- manifest notes: Claude, Cursor and Codex manifests; no MCP server or app connector. OpenAI's marketplace entry says AVAILABLE / ON_INSTALL, while the repository's own marketplace file pins tag v1.7.1 with INSTALLED_BY_DEFAULT / ON_USE. Each policy belongs to its own marketplace: via openai/plugins treat it as opt-in and unpinned, never as preinstalled. Needs the Foundry CLI (`brew install crowdstrike/foundry-cli/foundry`, >= 2.1.0 for exec/test/logs), an authenticated profile (CrowdStrike API client), Node/Python/Go per app, `pyyaml` (plus `crowdstrike-falconpy` for app-upgrades). Skill names are plain (`api-integrations`, `ui-development`); hosts may list them as `crowdstrike-falcon-foundry:<name>`.
- security caveats that affect recommending it: (1) ships always-on hooks (session start, every prompt, every tool call): the router hook injects advice to use development-workflow and runs the spec adapter automatically on `foundry api-integrations create`, which rewrites the spec in place and can deny the call (Swagger 2.0, adapter failure); the CLI guard is advisory with a bypass (`FOUNDRY_SKIP_NAME_CONFIRM=1`); a bridge hook redirects `superpowers:brainstorming` and `writing-plans` toward development-workflow in any repository, Claude only. Per Codex itself (2026-11-18, not observed in a run), a Codex install runs the repo's bundled hooks: `.codex-plugin/plugin.json` declares only `skills`, and `hooks/hooks.json` sits at the repository root (README: Codex runs them only after the user trusts them via `/hooks`). Both the openai/plugins entry and CrowdStrike's own marketplace install the same repository, so the route does not change this; warn the user before recommending. Skill-symlink installs get none, and the routing hooks need `jq`. (2) Unpinned install from the OpenAI entry (see above). (3) Network fetches of code: Swagger 2.0 conversion runs `npx -y -p swagger2openapi@7.0.8`; app-upgrades pulls template versions from GitHub. (4) Live-tenant effects: deploy and release hit a real CID, a gated RBAC release can lock users out, and e2e-testing needs a Falcon console username, password and TOTP secret and installs/uninstalls the app in a real tenant. Recommend only to a user doing Falcon Foundry work with their own tenant access.
- router: `development-workflow` covers the whole family. New app -> confirm the app name with the user -> CLI check (`foundry version`, `profile list`, `apps list`) -> `foundry apps create ... --no-prompt --no-git` (never mkdir) -> capabilities in dependency order (API integrations -> collections -> `foundry apps validate`, stop on failure -> functions -> knowledge bases -> agents -> workflows -> UI pages -> extensions) -> load the matching capability skill before writing content -> build UI, deploy once with `deploy_and_release.py` (never twice on timeout), release. Existing app: add capability -> that skill; template-installed app -> app-upgrades; review -> app-audit; failure -> debugging-workflows; security review -> security-patterns; Playwright -> e2e-testing; no app needed -> fusion-redirect. Cross-cutting gates: `--no-prompt`, run from the app root, manifest.yml and vite.config.js are CLI-owned apart from narrow documented exceptions, commit deploy-written IDs. Every capability skill says to load it first for a new app.
- development distance: core-dev (vendor-specific: it builds apps with functions, UI and workflows for the CrowdStrike Falcon platform).
- disclosure: router-delegated; development-workflow owns the decision tree, so records stay one-liners for matching.

### development-workflow
- id: crowdstrike-falcon-foundry:development-workflow (source path: skills/development-workflow/SKILL.md)
- description: "Orchestrates the complete Falcon Foundry app lifecycle from requirements through deployment. TRIGGER when user asks to "create a Foundry app", "build a Foundry app", "plan a Foundry app", runs any `foundry apps` CLI command, or discusses Foundry app architecture. DO NOT TRIGGER when user is working on a specific capability (UI, function, workflow, collection) within an existing app — use the appropriate sub-skill instead. This skill OWNS the entire Foundry development flow. Do not delegate Foundry app creation to superpowers:brainstorming or superpowers:writing-plans — those skills do not know about the Foundry CLI."
- use when: "Build me a Falcon Foundry app" or any `foundry apps` command: the whole new-app lifecycle (confirm app name, scaffold, add capabilities in dependency order, build, deploy once, release). Use it instead of superpowers:brainstorming/writing-plans for Foundry apps.
- needs: Foundry CLI (>= 2.1.0 for exec/test/logs), an authenticated profile for the right tenant/cloud, Node for UI builds, Python.
- side effects: writes the app directory; deploys and releases to a real CrowdStrike CID.
- part of: entry router for crowdstrike-falcon-foundry; hands off to the capability skills, app-upgrades, app-audit, debugging-workflows, security-patterns, e2e-testing and fusion-redirect.

### api-integrations
- id: crowdstrike-falcon-foundry:api-integrations (source path: skills/api-integrations/SKILL.md)
- description: "Expose external APIs to Falcon Foundry via OpenAPI specs. TRIGGER when user asks to "create an API integration", "adapt an OpenAPI spec for Foundry", "expose an API to workflows", "connect to a third-party API", or runs `foundry api-integrations create`. Also trigger when user has an OpenAPI/Swagger spec and wants it working in Falcon Foundry. DO NOT TRIGGER when user wants to call Falcon platform APIs from function code — use functions-falcon-api instead."
- use when: Connect a third-party API (or a Falcon API family FalconPy lacks) to a Foundry app from a vendor OpenAPI/Swagger spec.
- needs: Foundry CLI; Python with `pyyaml`; Node/npx for Swagger 2.0 conversion (npm download); `gh`/`curl` to fetch a remote spec.
- side effects: the mandatory adapter rewrites OpenAPI specs in place, including deleting unsupported auth schemes; Swagger 2.0 conversion writes a neighboring `.openapi3.*` file even with `--dry-run`. Creates local integration files and deploys to the CID; credentials are collected at install.
- part of: capability step 1 of development-workflow.

### collections-development
- id: crowdstrike-falcon-foundry:collections-development (source path: skills/collections-development/SKILL.md)
- description: "Design JSON Schema collections and CRUD patterns for Falcon Foundry apps. TRIGGER when user asks to "create a collection", "define a JSON schema", "store data in Foundry", runs `foundry collections create`, or needs help with indexable fields, FQL queries, or collection access patterns. DO NOT TRIGGER for workflow YAML, function handlers, or UI components — use the appropriate sub-skill."
- use when: Store app data in Foundry: define a collection and JSON schema, FQL search, indexable fields, or expose a collection to workflows/agents.
- side effects: scaffolding writes the collection schema and manifest; CRUD operations write/delete deployed collection data. Custom-storage collections cannot be tightened after use; collection deletion is console-only and deleted names cannot be reused under the same app ID.
- part of: capability step 2 of development-workflow.

### functions-development
- id: crowdstrike-falcon-foundry:functions-development (source path: skills/functions-development/SKILL.md)
- description: "Build serverless Go or Python functions for Falcon Foundry apps. TRIGGER when user asks to "create a function", "write a serverless function", "build backend logic", runs `foundry functions create`, or needs help with FDK handler patterns, function testing, or collection integration from functions. Also TRIGGER when user asks to "execute a function", "run my function", "debug this function", "get function logs", "check execution status", "write function tests", "test my function handler", or "add test cases for my function". DO NOT TRIGGER for generic "write integration tests" or "write tests" without function context — ask which capability they want to test first. DO NOT TRIGGER for calling Falcon platform APIs from functions — use functions-falcon-api instead. DO NOT TRIGGER for workflow YAML or UI components. DO NOT TRIGGER for Playwright/e2e/browser tests — use e2e-testing instead."
- use when: Write a Go or Python serverless Foundry function or handler, call collections/API integrations from it, or exec/test/get logs of a deployed function.
- needs: Foundry CLI >= 2.1.0, Go or Python; a deployed function for exec/test.
- side effects: exec and test run against the deployed function, not local code; it asks before any deploy or run.
- part of: capability step of development-workflow; calls to Falcon platform APIs go to functions-falcon-api.

### functions-falcon-api
- id: crowdstrike-falcon-foundry:functions-falcon-api (source path: skills/functions-falcon-api/SKILL.md)
- description: "Call CrowdStrike Falcon platform APIs (detections, alerts, hosts, RTR) from within Foundry function handlers. TRIGGER when user asks to "call Falcon APIs from a function", "use FalconPy in a function", "use gofalcon in a function", or needs to integrate Falcon platform APIs within serverless function code. DO NOT TRIGGER when user wants to expose external third-party APIs to Foundry — use api-integrations instead."
- use when: A function handler must call CrowdStrike Falcon platform APIs (alerts, hosts, RTR, NGSIEM, AgentWorks) with FalconPy or gofalcon; third-party APIs belong to api-integrations.
- needs: `auth.scopes` declared in the manifest for direct platform calls (a missing scope is a runtime 403 that validate does not catch).
- part of: companion to functions-development.

### ai-agents-development
- id: crowdstrike-falcon-foundry:ai-agents-development (source path: skills/ai-agents-development/SKILL.md)
- description: "Build AI agents and knowledge bases for Falcon Foundry apps. TRIGGER when user asks to "create an AI agent", "add a Foundry agent", "build a knowledge base", "give my agent documents", "expose a collection as an agent tool", "expose an API operation to an agent", "put my agent in Charlotte", "expose an agent as a tool for other agents", "delete an agent or knowledge base", runs `foundry agents create`, `foundry agents delete`, `foundry knowledge-bases create`, or `foundry knowledge-bases delete`, or needs help with the `ai.agents` / `ai.knowledge_bases` manifest blocks, agent system prompts, agent input/output formats, agent exposure, or agent tool references. DO NOT TRIGGER for Fusion SOAR workflow YAML — use workflows-development. DO NOT TRIGGER for serverless function handlers — use functions-development. DO NOT TRIGGER for designing a collection schema itself — use collections-development, then return here to wire the collection up as an agent tool."
- use when: Add an AI agent or knowledge base to a Foundry app, expose a collection or API operation as an agent tool, or expose an agent to Charlotte.
- needs: a CID with AgentWorks/Charlotte; knowledge bases are created before agents.
- side effects: `agents delete` is local only and leaves a platform orphan.
- part of: capability step of development-workflow.

### workflows-development
- id: crowdstrike-falcon-foundry:workflows-development (source path: skills/workflows-development/SKILL.md)
- description: "Create and configure Falcon Fusion SOAR workflow YAML for Falcon Foundry apps. TRIGGER when user asks to "create a workflow", "build an automation", "configure Falcon Fusion SOAR", "add an on-demand workflow", runs `foundry workflows create`, or needs help with Falcon Fusion YAML syntax, triggers, actions, or variable references. DO NOT TRIGGER for UI pages, functions, or collection schemas — use the appropriate sub-skill."
- use when: Write Falcon Fusion SOAR workflow YAML inside a Foundry app, including calling the app's functions, API integrations or agents.
- needs: Workflow Author plus Falcon Developer roles; action IDs from CLI discovery, never guessed.
- side effects: installing the app provisions its `provision_on_install: true` workflows, switched on.
- part of: capability step of development-workflow; a standalone workflow with no app belongs to fusion-redirect / the Fusion plugin.

### ui-development
- id: crowdstrike-falcon-foundry:ui-development (source path: skills/ui-development/SKILL.md)
- description: "Build UI pages and extensions for Falcon Foundry apps using React or Vue with the Shoelace design system and Foundry-JS. TRIGGER when user asks to "create a UI page", "build a UI extension", "add a Shoelace component", "call an API from the UI", runs `foundry ui pages create` or `foundry ui run`, or needs help with Vite config, Foundry-JS, or Falcon console theming. DO NOT TRIGGER for backend functions, workflow YAML, or collection schemas."
- use when: Build a Foundry UI page or extension (React/Vue/Vanilla with Shoelace and foundry-js), or run `foundry ui run`.
- side effects: writes local UI files and runs dev-server commands; extensions need `--sockets` or the picker hangs.
- part of: capability step of development-workflow.

### security-patterns
- id: crowdstrike-falcon-foundry:security-patterns (source path: skills/security-patterns/SKILL.md)
- description: "Security patterns for Falcon Foundry apps including OAuth scopes, RBAC, input validation, UI security, and credential management. TRIGGER when user asks to "configure OAuth scopes", "secure a Foundry app", "handle secrets", "add input validation", or needs to review a Foundry app for security concerns (XSS, CSP, credential management). Also trigger during pre-deployment security reviews."
- use when: Configure RBAC or OAuth scopes, secrets handling, input validation or a pre-deployment security review (XSS/CSP) of a Foundry app.
- side effects: an RBAC rollout can lock users out (deploy, assign the role, then release); adding a scope forces a Major release.

### app-audit
- id: crowdstrike-falcon-foundry:app-audit (source path: skills/app-audit/SKILL.md)
- description: "Audit an existing Falcon Foundry app for documented anti-patterns and fix the safe ones, like npm audit. TRIGGER when user asks to "audit my Foundry app", "check my app for problems", "review this Foundry app", "scan for anti-patterns", "why might this deploy fail", or runs `audit_app.py`. DO NOT TRIGGER for creating a new app (use development-workflow) or for debugging an error the user already has (use debugging-workflows)."
- use when: Statically scan an existing local Foundry app for known anti-patterns before deploy (16 checks); use debugging-workflows when an error already exists.
- needs: Python 3 with pyyaml; no API calls or CLI auth.
- side effects: `--fix` applies two single-line fixes after telling the user.

### debugging-workflows
- id: crowdstrike-falcon-foundry:debugging-workflows (source path: skills/debugging-workflows/SKILL.md)
- description: "Systematic troubleshooting for Falcon Foundry CLI errors, manifest validation failures, deploy failures, artifact runtime errors, and development server issues. TRIGGER when user encounters CLI errors, `foundry ui run` not working, deploy failures, authentication issues, function execution failures, "debug my function", "why did this fail", or any unexpected behavior during Foundry app development. Also trigger for headless/CI environment setup failures."
- use when: Something fails in Foundry development: CLI errors, `foundry ui run` problems, deploy/validate failures, function errors, 403s, a UI change that does not appear, or a stuck release.
- needs: authenticated Foundry profile; headless runs need API client env vars.
- side effects: recovery steps include `profile delete`, `apps delete --force-delete` and redeploys; a jammed release needs a support ticket, not retries.

### app-upgrades
- id: crowdstrike-falcon-foundry:app-upgrades (source path: skills/app-upgrades/SKILL.md)
- description: "Upgrade a Falcon Foundry app that was installed from a template to a newer version of that template, in place. TRIGGER when user asks to "upgrade an app", "update an app installed from a template", "pull the latest template into my app", "update a sample app installed in my CID to the latest version", or gives an app ID plus a newer template archive, directory, or GitHub repo. DO NOT TRIGGER for creating a new app (use development-workflow) or for deploying changes to an app the user develops locally (use development-workflow's deploy steps)."
- use when: Upgrade a Foundry app that was installed from a template/sample into a CID to a newer template version in place, keeping the customer's IDs.
- not for: development-workflow (an app the user develops locally).
- needs: app ID; Foundry CLI with a profile that owns the app; pyyaml (crowdstrike-falconpy for template discovery); Node/npm for UI builds; GitHub access for remote templates, or a supplied archive/directory.
- side effects: replaces customer customizations with the template, deploys and releases to the CID; removals or existing permission changes require confirmation and can delete collection data or widen access. A Major update requires customer Accept update; a first release requires catalog installation.

### e2e-testing
- id: crowdstrike-falcon-foundry:e2e-testing (source path: skills/e2e-testing/SKILL.md)
- description: "End-to-end testing for Falcon Foundry apps using Playwright and @crowdstrike/foundry-playwright. TRIGGER when user asks to "add e2e tests", "add playwright tests", "write end-to-end tests", "test my app", or mentions "e2e", "playwright", or "end-to-end" in the context of testing a Foundry app. DO NOT TRIGGER during normal app creation, UI development, or function development. This skill is opt-in; not all apps need e2e tests."
- use when: Only when explicitly asked: Playwright end-to-end tests for a Foundry app.
- needs: Falcon console username, password and TOTP secret in `.env`, plus Node/Playwright.
- side effects: tests install and uninstall the app in a real tenant; the CI pattern deploys, releases and deletes it; concurrent logins can lock the account.

### fusion-redirect
- id: crowdstrike-falcon-foundry:fusion-redirect (source path: skills/fusion-redirect/SKILL.md)
- description: "TRIGGER when user asks for a "standalone Falcon Fusion workflow" that needs NO Foundry app — just a trigger plus actions that already exist in their CID, with no UI, function, collection, or custom API integration to build. DO NOT TRIGGER when the request needs anything built (a custom action, a UI page, a function, a collection) — that is a Foundry app and development-workflow owns it. This skill exists so the redirect works without hooks and yields to the real Falcon Fusion plugin when both are loaded."
- use when: A standalone Falcon Fusion workflow with nothing to build (trigger plus existing actions): produces no artifact, names the crowdstrike-falcon-fusion plugin and how to get it. Use development-workflow when anything must be built.
- part of: redirect from development-workflow to the Fusion family's workflows.

## Family: plugin-eval
- source path: `plugins/plugin-eval` (plugin v0.1.2, package 0.1.0)
- manifest notes: Codex-only marketplace entry. No MCP or app. Needs the local Node >=20 `plugin-eval` CLI from a checkout (private package, not on public npm). Live benchmarks need working `codex exec`. Four fixture skills ship under fixtures/ and are test inputs, never real routes.
- router: `plugin-eval` resolves the target (named skill: ~/.codex/skills/<name> then repo skills/<name>; ask if still ambiguous) and runs `start`. Evaluate or "why this score" -> `analyze` (skill -> evaluate-skill, plugin root -> evaluate-plugin); token budget -> static estimate; measured usage -> `init-benchmark`, human review of `.plugin-eval/benchmark.json`, live `benchmark`, `analyze --observed-usage`; rewrite -> improve-skill; custom rubric -> metric-pack-designer. Estimates are never presented as measurements.
- development distance: adjacent (tooling for authoring agent skills and plugins)
- disclosure: router-delegated. The umbrella routes every real skill; fixtures are excluded from matching.

### plugin-eval
- id: plugin-eval:plugin-eval (source path: plugins/plugin-eval/skills/plugin-eval/SKILL.md)
- description: "Help engineers evaluate a local skill or plugin, explain why it scored that way, show what to fix first, measure real token usage, benchmark starter scenarios, or decide what to run next. Use when the user says things like "evaluate this skill", "give me an analysis of the game dev skill", "why did this score that way", "what should I fix first", "measure the real token usage of this skill", or "what should I run next?"."
- use when: Evaluate a local skill or plugin, explain its score, measure real token usage, set up a benchmark, or I am unsure what to run.
- side effects: `init-benchmark` writes `.plugin-eval/`; a live benchmark launches real Codex sessions, so review its config first.

### evaluate-plugin
- id: plugin-eval:evaluate-plugin (source path: plugins/plugin-eval/skills/evaluate-plugin/SKILL.md)
- description: "Evaluate a local Codex plugin in engineer-friendly language. Use when the user says "evaluate this plugin", "audit this plugin", "why did this score that way", "what should I fix first", "help me benchmark this plugin", or asks for a plugin-wide report before comparing versions."
- use when: Audit a whole local Codex plugin bundle, compare versions, or set up a plugin benchmark.
- needs: a plugin root with `.codex-plugin/plugin.json`.

### evaluate-skill
- id: plugin-eval:evaluate-skill (source path: plugins/plugin-eval/skills/evaluate-skill/SKILL.md)
- description: "Evaluate a local Codex skill in engineer-friendly terms. Use when the user says "evaluate this skill", "give me an analysis of the game dev skill", "audit this skill", "why did this score that way", "what should I fix first", or asks for a skill-specific report before benchmarking it."
- use when: Evaluate one local skill. An "analysis" request also writes `.plugin-eval/benchmark.json` and asks scenario questions instead of stopping at the report.

### improve-skill
- id: plugin-eval:improve-skill (source path: plugins/plugin-eval/skills/improve-skill/SKILL.md)
- description: "Turn plugin-eval findings into a concrete rewrite brief for a Codex skill. Use when the user already evaluated a skill and now wants Codex to improve it, especially after asking what to fix first."
- use when: Rewrite a skill using findings from a prior plugin-eval run.
- needs: prior findings; step 3 hard-codes `/Users/benlesh/.codex/skills/skill-creator/SKILL.md`, another author's home path with no fallback: tell the user to point step 3 at their own `skill-creator` skill, or skip it.

### metric-pack-designer
- id: plugin-eval:metric-pack-designer (source path: plugins/plugin-eval/skills/metric-pack-designer/SKILL.md)
- description: "Design custom metric packs for plugin-eval so teams can add local evaluation rubrics that emit schema-compatible checks and metrics. Use when the user wants their own evaluation criteria or visualizations."
- use when: Add a team-specific evaluation rubric or custom metrics to plugin-eval.
- side effects: writes a manifest plus an executable evaluator that `analyze --metric-pack` runs as arbitrary local code.

### minimal-plugin-skill
- id: plugin-eval:minimal-plugin-skill (source path: plugins/plugin-eval/fixtures/minimal-plugin/skills/minimal-plugin-skill/SKILL.md)
- description: "Minimal plugin skill fixture. Use when a test needs a valid plugin skill."
- use when: Never for a user task: plugin-eval test fixture (one-skill plugin).

### minimal-skill
- id: plugin-eval:minimal-skill (source path: plugins/plugin-eval/fixtures/minimal-skill/SKILL.md)
- description: "Minimal example skill for plugin-eval tests. Use when the user wants a compact demonstration of a well-structured skill."
- use when: Never for a user task: plugin-eval test fixture (standalone skill).

### alpha
- id: plugin-eval:alpha (source path: plugins/plugin-eval/fixtures/multi-skill-plugin/skills/alpha/SKILL.md)
- description: "Alpha fixture skill. Use when plugin-eval tests need one of two bundled skills."
- use when: Never for a user task: plugin-eval test fixture (first of two bundled skills).

### beta
- id: plugin-eval:beta (source path: plugins/plugin-eval/fixtures/multi-skill-plugin/skills/beta/SKILL.md)
- description: "Beta fixture skill. Use when plugin-eval tests need the second bundled skill."
- use when: Never for a user task: plugin-eval test fixture (second of two bundled skills).

## Family: plugin-creator
- source path: repo-level skill at `.agents/skills/plugin-creator/` (not a marketplace plugin entry)
- distribution: not a marketplace entry; the skill directory is `.agents/skills/plugin-creator/` in openai/plugins.
- manifest notes: no manifest of its own; its output is a Codex plugin (`.codex-plugin/plugin.json`) and marketplace entries. Bundled stdlib-only Python scaffolder; no network or auth.
- router: none
- development distance: adjacent (plugin scaffolding for the Codex host)
- disclosure: simple. One skill.

### plugin-creator
- id: openai/plugins:plugin-creator (source path: .agents/skills/plugin-creator/SKILL.md)
- description: "Create and scaffold plugin directories for Codex with a required `.codex-plugin/plugin.json`, optional plugin folders/files, and baseline placeholders you can edit before publishing or testing. Use when Codex needs to create a new personal plugin, add optional plugin structure, or generate or update personal or repo-root `.agents/plugins/marketplace.json` entries for plugin ordering and availability metadata."
- use when: Scaffold a new Codex plugin directory with `.codex-plugin/plugin.json` and optionally register it in a personal or repo `.agents/plugins/marketplace.json`.
- not for: create-plugin-scaffold (same job for Cursor; pick by target host); review-plugin-submission (Cursor plugin audit); skill-creator (a skill's content, complementary).
- needs: Python 3 and a writable destination; the Codex app only for the View/Share links.
- side effects: writes `~/plugins/<name>` by default; writes `~/.agents/plugins/marketplace.json` only when marketplace registration is selected. An existing manifest blocks without `--force`; with it, the placeholder manifest replaces existing contents. Asks personal vs team before registration if a repo marketplace exists and intent is unspecified.
- part of: standalone, early packaging step before content authoring.

## Family: posthog
- source path: `plugins/posthog` (v1.0.0)
- manifest notes: bundles app `posthog` (asdk_app_699caef2d680819188727b0ddbb349dd) and `.mcp.json` for HTTP MCP https://mcp.posthog.com/mcp; the manifest has no `mcpServers` pointer, so automatic MCP loading is unestablished. OAuth required (self-hosted instance chosen during OAuth); marketplace ON_INSTALL; not host-restricted.
- router: `posthog` is the entry to the connected app's own skills and tools: tools absent -> connect, OAuth, pick org/project, restart if needed, finish the answer and ask to retry -> clarify goal -> discover live skills/tools, docs first -> batch reads -> writes -> explicit impact confirmation for destructive or broad changes -> summary with numbers and links.
- development distance: adjacent (product analytics and tooling)
- disclosure: simple. One skill.

### posthog
- id: posthog:posthog (source path: plugins/posthog/skills/posthog/SKILL.md)
- description: "Analyze product data and manage product tooling in PostHog. Use when the user wants product analytics or insights, HogQL/SQL queries, feature flags, experiments and A/B tests, error tracking, session replay, surveys, LLM analytics, dashboards, data warehouse, or PostHog documentation."
- use when: How is our funnel or retention doing? Query events with HogQL, inspect errors, replays or LLM costs, or manage flags, experiments, surveys and dashboards in PostHog.
- not for: openai-ads-conversions-setup (instrument Ads conversion code); sentry (read-only Sentry error report).
- needs: PostHog app authorized via OAuth, org and project confirmed even for reads, date range and entity IDs.
- side effects: reads customer data; writes manage flags, experiments, surveys, dashboards and insights. Destructive or broad changes (such as production flag toggles or ending experiments) require stated impact and confirmation first.
- part of: entry router for the PostHog connected app.

## Family: mixpanel-headless
- source path: `plugins/mixpanel-headless` (v0.1.2)
- manifest notes: Codex-only manifest; no MCP server, app connector or hooks. MIT; category Data & Analytics. Everything runs through the `mixpanel_headless` Python SDK and the `mp` CLI. Credentials: Mixpanel service account, OAuth browser login (PKCE) or `MP_OAUTH_TOKEN`; the setup skill installs the SDK and its Python dependencies. Remote/sandboxed sessions cannot do OAuth login or interactive account add (use the `mp account export-bridge` bridge file instead).
- router: none. Informal sequence: `mixpanel-headless-setup` (install + verify credentials) -> `mixpanel-auth` (accounts/projects) -> `mixpanelyst` (analysis; auto-triggers on analytics questions) -> `dashboard-expert` (dashboards). Secrets are never requested in chat.
- development distance: adjacent (Python analytics against a product-analytics service; mutating entity CRUD, no application code)
- disclosure: simple. Four related skills for Mixpanel setup, authentication, analysis and dashboards; the sequence is informal, not mandatory.

### mixpanel-headless-setup
- id: mixpanel-headless:setup (source path: plugins/mixpanel-headless/skills/setup/SKILL.md)
- description: "This skill installs mixpanel_headless, pandas, numpy, matplotlib, seaborn, networkx, anytree, scipy (and pyarrow on Python 3.11+), then verifies Mixpanel credentials. It should be invoked when setting up a new environment for Mixpanel data analysis, when dependencies are missing, or when configuring service account or OAuth credentials for the first time."
- use when: I want to start analyzing Mixpanel data in Python and the SDK, dependencies or credentials are not set up yet.
- not for: `mixpanel-auth` (ongoing account/project switching after setup) and `mixpanelyst` (the analysis itself).
- needs: Python 3.10+, uv or pip, network, a Mixpanel service account or OAuth; no OAuth login or interactive account add in remote sessions.
- side effects: installs Python packages (mixpanel_headless, pandas, numpy, matplotlib, scipy and others); never asks for secrets in chat.
- part of: step 1 of setup -> mixpanel-auth -> mixpanelyst -> dashboard-expert; hands off to `mixpanel-auth` and `mixpanelyst`.

### mixpanel-auth
- id: mixpanel-headless:mixpanel-auth (source path: plugins/mixpanel-headless/skills/mixpanel-auth/SKILL.md)
- description: "Manage Mixpanel Headless authentication: check session state, list/add/use accounts, run OAuth login, switch projects/workspaces, manage targets, and check bridge credentials."
- use when: I want to see or switch the active Mixpanel account, project or workspace, add or test credentials, or check the bridge file.
- not for: `mixpanel-headless-setup` (first-time install and verification) and `mixpanelyst` (queries).
- needs: `PLUGIN_ROOT` set to the plugin directory, Python, the SDK installed; the user adds secrets in their own terminal.
- side effects: switching project, workspace or target writes `~/.mp/config.toml`.
- part of: step 2 of the informal sequence; standalone after setup.

### mixpanelyst
- id: mixpanel-headless:mixpanelyst (source path: plugins/mixpanel-headless/skills/mixpanelyst/SKILL.md)
- description: "This skill should be used when the user asks about Mixpanel product analytics, event data, funnel analysis, retention curves, cohort analysis, segmentation queries, user behavior, conversion rates, churn, DAU/MAU, ARPU, revenue metrics, feature adoption, A/B test results, user paths, flow analysis, or any request to query, explore, visualize, or analyze Mixpanel data using Python. Also use when the user asks to read, write, or manage Mixpanel "business context" — the markdown documentation that grounds AI assistants in an organization's structure and goals."
- use when: I want to query Mixpanel (funnels, retention, flows, cohorts, DAU/MAU, conversion, churn) in Python, or read or write Mixpanel business context.
- not for: `dashboard-expert` when the target artifact is a Mixpanel dashboard; `metric-diagnostics` (data-analytics) for source-agnostic diagnosis ending in a report.
- needs: the SDK installed and authenticated; org-level business-context writes need `edit_project_info` (typically OAuth).
- side effects: reads by default; entity CRUD can create, update or delete flags, experiments, alerts, cohorts, schema rules and data, and `set_business_context` fully replaces the text.
- part of: step 3, the main analysis skill; hands dashboard building to `dashboard-expert`.

### dashboard-expert
- id: mixpanel-headless:dashboard-expert (source path: plugins/mixpanel-headless/skills/dashboard-expert/SKILL.md)
- description: "Full CRUD and analysis for Mixpanel dashboards. Use when the user asks to build, create, analyze, read, understand, explain, modify, update, enhance, or manage dashboards, or asks about dashboard layout, text cards, or report arrangement. Covers dashboard analysis (read + understand existing), creation (new builds), modification (update existing), and explanation (data-driven annotation)."
- use when: I want to build, read, change or annotate a Mixpanel dashboard, including layout and text cards.
- not for: `mixpanelyst` for queries and other Mixpanel entities; use this only when the dashboard is the target.
- needs: the SDK authenticated with a workspace.
- side effects: creates, updates and deletes dashboards and cells and pins them, which makes them team-visible.
- part of: step 4; handed dashboard work by `mixpanelyst`.

## Family: openai-ads-conversions
- source path: `plugins/openai-ads-conversions` (v0.1.2)
- manifest notes: no MCP, app or hooks; ships two local Python verification helpers and public-doc snapshots. Provisions no credentials: CAPI uses existing server secret references and the skill never requests, creates, stores or prints keys. Not host-restricted.
- router: none (single skill: inspect repo and analytics -> confirm mode and success-boundary plan -> smallest patch or review -> local verification -> report and advertiser review before deploy)
- development distance: adjacent (analytics instrumentation)
- disclosure: simple. One skill.

### openai-ads-conversions-setup
- id: openai-ads-conversions:openai-ads-conversions-setup (source path: plugins/openai-ads-conversions/skills/openai-ads-conversions-setup/SKILL.md)
- description: "Guide Codex through instrumenting or extending repositories with OpenAI Ads Measurement Pixel and optional Conversions API (CAPI). Use when adding Ads conversion tracking, browser pixel events, server-side conversion events, event_id deduplication, CAPI secret placeholders, incremental conversion coverage, or validating Ads conversion setup. Applies to local repositories and PR review contexts; prioritize safe, reviewable diffs and never place API keys or secrets in source code or client bundles."
- use when: Add or review OpenAI Ads conversion tracking (browser Pixel, server Conversions API) in my repo, extend coverage after new flows, or deduplicate browser and server events.
- not for: posthog (product analytics on existing data); openai-platform-api-key (OpenAI Platform keys, not Ads CAPI secrets).
- needs: repo, mode (`pixel`, `capi`, `pixel+capi`), runtime surface, propose/apply/review intent, conversion success points; Pixel ID if Pixel is in scope, secret-reference or placeholder plan if CAPI is in scope.
- side effects: writes a small local patch; deployed code sends conversion and user-matching data. Infra or deploy requirements trigger clarification; advertiser review required before deploy.
- part of: standalone. For CAPI web events, settles `oppref` and sanitized `source_url` strategy before editing.

## Family: data-analytics
- source path: `plugins/data-analytics` (v0.2.8)
- manifest notes: Codex-only manifest. Declares a local MCP server `dataAnalyticsWidgets` (`node ./mcp/server.cjs --stdio`; renders charts, tables, dashboards, reports and validates artifacts) and an `.app.json` with 23 optional connectors (Slack, Teams, Notion, Gmail, Outlook Email/Calendar, Google Calendar/Drive, SharePoint, Databricks, BigQuery, Snowflake, GitHub, Statsig, Amplitude, Mixpanel, PostHog, Sites, Hex, Deepnote, Omni, Metabase, ThoughtSpot); declarations are routing hints, not proof of installation. Proprietary; no credential, payment or pricing policy. Runtime branching keys on ChatGPT/Codex signals (surface `chatgpt_web`/Desktop, mode Work Mode/Chat); the three `report-to-*` skills disable implicit invocation.
- router: `index` (routing only; covers every focused skill). Order: in ChatGPT web Chat the first turn only recommends Work Mode and does nothing else; require quantitative evidence (else not eligible); explicit save-context requests go to `create-data-context`; discover and verify sources before querying; choose a report for analysis with findings, inline only for quick bounded lookups; read selected skill bodies first. Analysis workflows (`product-business-analysis`, `metric-diagnostics`, `kpi-reporting`, `market-sizing`) run `gather-business-context` -> analysis -> `build-report` (visuals via `visualize-data`) unless waived. A concrete task with no usable data ends with an Upload data / Use sample data (synthetic) choice; connector installs happen only for a concrete task, one at a time.
- development distance: adjacent (data analysis and BI artifacts; produces SQL/Python notebooks and dashboards, not application code)
- disclosure: router-delegated. `index` owns eligibility, runtime and delivery gates, so records stay one-liners for matching.

### index
- id: data-analytics:index (source path: plugins/data-analytics/skills/index/SKILL.md)
- description: "Route Data Analytics plugin-level requests and broad analytics work to the right focused workflow. Use when Data Analytics is at-mentioned, or for analytics requests involving data, metrics, dashboards, reports, charts, notebooks, spreadsheets, KPIs, market sizing, or semantic layers."
- use when: I @-mention Data Analytics, ask "what can you do with this data?", or have a quantitative request with no clear focused skill; it routes only.
- needs: ChatGPT/Codex runtime; in ChatGPT web Chat the first turn only recommends Work Mode.
- side effects: may request connector/plugin installs, sequentially, only for a concrete task with missing evidence.

### analyze-data-quality
- id: data-analytics:analyze-data-quality (source path: plugins/data-analytics/skills/analyze-data-quality/SKILL.md)
- description: "Assess whether structured data, query results, dashboards, or analytical evidence are trustworthy enough to use. Use when the task is to check data quality, reconcile conflicting sources or metric definitions, or decide whether evidence is safe to cite."
- use when: Can I trust this table? Why do two dashboards disagree? Did a backfill add duplicates or missing partitions?

### build-dashboard
- id: data-analytics:build-dashboard (source path: plugins/data-analytics/skills/build-dashboard/SKILL.md)
- description: "Build source-backed dashboards for monitoring performance, exploring drivers, or acting on product and business metrics. Use when the task needs a dashboard, scorecard, or monitoring view with clear metrics, filters, source definitions, and QA."
- use when: Give the team a reusable, filterable monitor of a metric (BI platform, MCP artifact, Sites, HTML; Streamlit only on explicit request).
- side effects: Sites output is a deployed dated snapshot; a BI branch writes to the BI platform.

### build-report
- id: data-analytics:build-report (source path: plugins/data-analytics/skills/build-report/SKILL.md)
- description: "Build polished analytical reports for executive, product, business, or technical audiences. Use when the task needs a durable answer-first narrative with evidence-backed findings, visuals or tables, caveats, and source context."
- use when: Write up analysed findings as one durable, evidence-backed report for exactly one audience.
- side effects: builds one artifact; in Work Mode a durable report publishes through Sites automatically when the full lifecycle is callable, otherwise uses self-contained HTML (also the fallback after publishing failure, unless Sites-only was explicitly requested).

### report-to-google-doc
- id: data-analytics:report-to-google-doc (source path: plugins/data-analytics/skills/build-report/report-to-google-doc/SKILL.md)
- description: "Narrow conversion skill. Invoke only when the user explicitly asks to convert an existing local or blob-hosted HTML analytics report into a Google Doc, DOCX, or shareable document."
- use when: Explicit request only: convert an existing HTML analytics report into a Google Doc or DOCX (delivered as a DOCX-backed Drive file, not a forced native Google Doc).
- needs: a real local HTML report, Python with beautifulsoup4, pillow, python-docx; authenticated Codex-app Google Drive.
- side effects: writes local files, may install missing Python dependencies in a local virtual environment, and uploads to Google Drive after conversion preflight passes.

### report-to-google-slides
- id: data-analytics:report-to-google-slides (source path: plugins/data-analytics/skills/build-report/report-to-google-slides/SKILL.md)
- description: "Narrow conversion skill. Invoke only when the user explicitly asks to convert an existing HTML analytics report into a native Google Slides deck."
- use when: Explicit request only: turn an existing HTML analytics report into a native Google Slides deck.
- needs: a real local HTML report, Python with beautifulsoup4, pillow, python-pptx, `unzip`; Codex-app Google Drive native-Slides import.
- side effects: writes local files and imports a deck into Google Drive.

### report-to-pdf
- id: data-analytics:report-to-pdf (source path: plugins/data-analytics/skills/build-report/report-to-pdf/SKILL.md)
- description: "Narrow conversion skill. Invoke only when the user explicitly asks to convert an existing Data Analytics report, dashboard, or inline chart export into a PDF artifact."
- use when: Explicit request only: print an existing report, dashboard or chart export to a verified PDF.
- needs: a static HTML source and Chrome/Chromium (or an equivalent faithful renderer); pdf inspection tools.
- side effects: writes local files only.

### create-data-context
- id: data-analytics:create-data-context (source path: plugins/data-analytics/skills/create-data-context/SKILL.md)
- description: "Create, update, inspect, or repair Data Analytics semantic layers. Use when the user asks to save data context or create a semantic layer that future Data Analytics work can inspect and cite."
- use when: Save our canonical metric definitions and source rules as a reusable semantic layer for future analyses (explicit request only), or repair one.
- side effects: persists a generated skill to the ChatGPT personal Skills library or local `$CODEX_HOME/skills/<area>-semantic-layer` according to runtime (both when both destinations are available); returns a portable package if persistence is unavailable; creates weekly refresh only on explicit approval or a direct recurring-refresh request.

### design-kpis
- id: data-analytics:design-kpis (source path: plugins/data-analytics/skills/design-kpis/SKILL.md)
- description: "Design KPI frameworks, metric definitions, targets, guardrails, and measurement plans for product or business decisions. Use when success metrics, drivers, guardrails, targets, or the measurement approach need to be defined or improved."
- use when: How should we measure this launch? Pick success metrics, drivers, guardrails and targets; answered inline by default.

### gather-business-context
- id: data-analytics:gather-business-context (source path: plugins/data-analytics/skills/gather-business-context/SKILL.md)
- description: "Gather business context from connected or provided sources so downstream analysis starts with the right framing. Use when an analytical question depends on missing context, such as what a metric means, what changed recently, or which sources should be checked. If the same prompt asks for diagnosis, recommendation, or a deliverable, gather context first and continue to the focused skill."
- use when: Before diagnosing a metric, find its definition, owner, recent changes and source of truth; retrieval only, then continue to the requested work.

### jupyter-notebooks
- id: data-analytics:jupyter-notebooks (source path: plugins/data-analytics/skills/jupyter-notebooks/SKILL.md)
- description: "Create, edit, or validate reproducible SQL or Python notebooks. Use for notebooks, SQL/Python scratchpads, reproducible exploration, audit trails, or runnable companions where the analysis should be reviewable or rerunnable."
- use when: Make this SQL or Python analysis rerunnable, refactor a notebook, or keep an executed audit trail.
- side effects: writes and executes notebooks locally; optional `uv pip install jupyterlab nbformat nbclient ipykernel`.

### kpi-reporting
- id: data-analytics:kpi-reporting (source path: plugins/data-analytics/skills/kpi-reporting/SKILL.md)
- description: "Prepare KPI readouts, scorecards, WBR/MBR/QBR updates, and executive summaries from quantitative business or product metrics; use when the task is to report status, compare against targets, explain validated drivers, and state operating implications."
- use when: Prepare the monthly/quarterly operating review or KPI status against target and pace, with validated drivers; quick status can stay inline.

### market-sizing
- id: data-analytics:market-sizing (source path: plugins/data-analytics/skills/market-sizing/SKILL.md)
- description: "Estimate market, segment, or opportunity size with transparent assumptions and uncertainty. Use for TAM/SAM/SOM, sizing scenarios, or comparing the scale of possible opportunities."
- use when: What is our addressable market? TAM/SAM/SOM or segment opportunity with assumptions and sensitivity.

### metric-diagnostics
- id: data-analytics:metric-diagnostics (source path: plugins/data-analytics/skills/metric-diagnostics/SKILL.md)
- description: "Diagnose why a metric changed or differs from expectation. Use when the task is to identify likely drivers of a metric movement, anomaly, gap, or discrepancy."
- use when: Why did this metric move, which region or segment drove it, or why do these totals differ?

### product-business-analysis
- id: data-analytics:product-business-analysis (source path: plugins/data-analytics/skills/product-business-analysis/SKILL.md)
- description: "Analyze product or business data to support a decision or recommendation. Use when a decision depends on metric-backed evidence, such as choosing a direction, prioritizing an opportunity, evaluating a change, segmenting users, sizing tradeoffs, or deciding what to do next."
- use when: Should we ship, hold or iterate? Which segment deserves investment? A decision that needs metric-backed evidence.

### publish-artifact-to-sites
- id: data-analytics:publish-artifact-to-sites (source path: plugins/data-analytics/skills/publish-artifact-to-sites/SKILL.md)
- description: "Publish a validated Data Analytics report or dashboard artifact through Sites. Use automatically for durable artifacts in any positively identified Work Mode when the full Sites lifecycle is callable, or in ChatGPT Desktop outside Work Mode only after an explicit Sites request or acceptance of the optional post-handoff sharing offer."
- use when: Publish a validated report or dashboard through Sites: automatic in Work Mode, or after an explicit Sites request on desktop.
- needs: callable `sites-building` and `sites-hosting`, a Sites account, `export_artifact_package`.
- side effects: deploys the artifact and its data snapshot to a hosted Sites URL; seeds creator editing only from a verified owner-only policy, otherwise preserves existing editor state; changes reader access or disables editing only on explicit request.

### validate-data
- id: data-analytics:validate-data (source path: plugins/data-analytics/skills/validate-data/SKILL.md)
- description: "Validate whether an analysis is accurate, well-supported, and ready to share or use for a decision. Use when reviewing methodology, calculations, comparisons, visuals, caveats, or conclusions."
- use when: Is this analysis ready for leadership? Independent QA of methodology, calculations and conclusions before sharing.

### visualize-data
- id: data-analytics:visualize-data (source path: plugins/data-analytics/skills/visualize-data/SKILL.md)
- description: "Design, build, revise, or QA quantitative charts and figures. Use when an analytical answer needs visual judgment, whether for an inline answer, report, dashboard, notebook, or artifact."
- use when: Choose, build or QA a chart for an answer, report or dashboard, or fix a misleading visual.
- needs: host chart widgets or the packaged HTML builder, depending on runtime.

## Family: crowdstrike-falcon-fusion
- source repo: https://github.com/CrowdStrike/fusion-skills.git (url source in openai/plugins; no `ref` there). Curated at commit 89980d207b3db841d9a5026d71833ccc4972450e (plugin v1.4.0). 7 skills (the README lists six and omits `setup`).
- distribution: a `url` source in the openai/plugins Codex marketplace. The CrowdStrike/fusion-skills repository carries its own marketplace file and Claude, Cursor and Codex manifests.
- manifest notes: Claude, Cursor and Codex manifests; no MCP server or app connector. OpenAI's marketplace entry says AVAILABLE / ON_INSTALL; the repository's own marketplace file pins v1.4.0 with INSTALLED_BY_DEFAULT / ON_USE. Each policy belongs to its own marketplace: via openai/plugins treat it as opt-in and unpinned, never as preinstalled. Every skill declares `compatibility: Claude Code >=1.0`, but the bodies and README support Codex, Copilot CLI, Cursor and Antigravity; go by the README, the field is stale. Needs a Falcon CID with Fusion access, an API client with Workflow scope (NGSIEM Lookup Files scope for lookups), Python 3.13+, FalconPy and PyYAML (unpinned in `requirements.txt`). Several skill names are generic (`setup`, `workflows`, `execution`, `deployment`, `authoring`); hosts may list them as `crowdstrike-falcon-fusion:<name>`, so match on the family prefix, not the bare name.
- security caveats that affect recommending it: (1) always-on hooks: a session-start hook (120 s timeout) builds or refreshes a Python venv at `~/.cache/claude-code-fusion/venv` and installs unpinned `crowdstrike-falconpy` and `pyyaml` from PyPI or a mirror, in sessions unrelated to Fusion, and carries on silently when it fails; prompt and tool-call hooks add advisory routing reminders (they need `jq`) and a Fusion/Foundry bridge. They are non-blocking. Per Codex itself (2026-11-18, not observed in a run), a Codex install runs the repo's bundled hooks, the session-start venv with unpinned packages included: as in Foundry, `.codex-plugin/plugin.json` declares only `skills`, and `hooks/hooks.json` sits at the repository root (README: Codex runs them only after `/hooks` trust; symlink-only installs get none). Both the openai/plugins entry and CrowdStrike's own marketplace install the same repository, so the route does not change this; warn the user before recommending. (2) Unpinned install from the OpenAI entry. (3) Live-tenant writes: deployment imports and releases workflows in a real CID (release enables real event processing; `--replace` deletes every same-named definition), execution can contain hosts, lock accounts, send messages and call third-party services, lookup-files overwrites and deletes security reference data. (4) Credentials: reads `FALCON_CLIENT_ID`/`FALCON_CLIENT_SECRET` or `~/.cache/crowdstrike-falcon-fusion/credentials.toml`; optional `op run` mode exposes resolved secrets to child processes for the session. (5) Authoring text allows plausible organization-domain recipient addresses in CI runs; prefer asking for a real address. (6) Settled source contradictions: on an import 500, stop at the first occurrence and report the `trace_id` (no re-import unless local validation finds a real YAML defect); when a dependency needs a Foundry app, redirect and write no workflow YAML until the user confirms the app exists. Recommend only to a user doing Falcon work with their own tenant access, never "just to look".
- router: `workflows` only routes (it never writes YAML or calls APIs): authoring (scope check, resolve every action ID, discover trigger, write YAML, validate) -> deployment (duplicate check, import, release after authorization; carries `definition_id`) -> execution (trigger with test payload, capture `execution_id`, monitor, verify). Stops: do not deploy when validation fails or an action ID is unresolved; do not run an unreleased workflow; a failed run goes back to authoring or the console, not a blind retry. A build-only request ends with validated YAML and the question "Deploy this to your CID now?". Branches: lookup-files for lookup tables; Foundry for anything that must be built (no partial workflow YAML meanwhile); `foundry-redirect` is the hook-independent safety net.
- development distance: adjacent (produces workflow YAML and deploys it to a live security-automation platform; outside typical application development).
- disclosure: router-delegated; `workflows` covers the lifecycle and branches, so records stay one-liners for matching.

### workflows
- id: crowdstrike-falcon-fusion:workflows (source path: skills/workflows/SKILL.md)
- description: "Orchestrates the full Falcon Fusion workflow lifecycle from discovery through deployment and execution. TRIGGER when user asks to "create a Fusion workflow", "build a Fusion playbook", "automate CrowdStrike actions", or mentions Fusion workflows without specifying a sub-task. DO NOT TRIGGER when user is working in a Foundry app context, mentions manifest.yml, or asks to "build a Foundry app" — use foundry-skills instead."
- use when: "Build a playbook that enriches detections and alerts my team" or "automate CrowdStrike response" without naming a phase. It only routes (never writes YAML or calls APIs): authoring -> deployment -> execution, plus lookup-files and a Foundry hand-off.
- needs: Falcon Fusion-enabled CID; delegated skills inherit credentials, Python 3.13+, FalconPy, PyYAML.
- side effects: none itself; a build-only request ends with validated YAML and asks "Deploy this to your CID now?".
- part of: entry router for crowdstrike-falcon-fusion. Phase stops: do not deploy on failed validation or an unresolved action ID; do not run an unreleased workflow; a failed run goes back to authoring or the console, not a blind retry.

### authoring
- id: crowdstrike-falcon-fusion:authoring (source path: skills/authoring/SKILL.md)
- description: "Discover Falcon Fusion actions via live API, author workflow YAML with correct schema, validate against Charlotte JSON schema, and use templates/examples. TRIGGER when user asks to write workflow YAML, find actions, validate a workflow, use CEL expressions, or needs action discovery. DO NOT TRIGGER for deploying, importing, executing, or monitoring workflows — use deployment or execution skills. DO NOT TRIGGER when the request is for a Falcon Foundry app, a UI extension/page, an API integration, custom actions from a third-party API, or a manifest.yml — those are foundry-skills territory; advise foundry-skills instead of authoring a workflow."
- use when: Write or edit Fusion workflow YAML, find the real Falcon action IDs, fix CEL, validate; also a standalone workflow with a one-off HTTP call.
- needs: Python 3.13+, FalconPy, PyYAML and Falcon API credentials (validation does a live dry-run); Workflow read and import-validation scope.
- side effects: writes local YAML and a one-hour discovery cache; imports or releases nothing.
- part of: step 1 of workflows; hands to deployment; app-shaped work goes to Foundry first.

### deployment
- id: crowdstrike-falcon-fusion:deployment (source path: skills/deployment/SKILL.md)
- description: "Import, release, and manage Falcon Fusion workflow definitions in a CID. TRIGGER when user asks to import a workflow, release a workflow version, list existing workflows, check for duplicates, or manage workflow definitions. DO NOT TRIGGER for writing YAML (use authoring), executing workflows, or monitoring (use execution)."
- use when: Import a validated workflow into a CID, release it, or list, export, delete or replace definitions.
- needs: Workflow read/write scope; explicit user go-ahead to import and to release.
- side effects: writes to a live CID: release enables real event processing; `--replace` deletes every same-named definition and reimports under a new ID, disabled; delete is permanent.
- part of: step 2 of workflows.

### execution
- id: crowdstrike-falcon-fusion:execution (source path: skills/execution/SKILL.md)
- description: "Trigger Falcon Fusion workflows, monitor execution status, and debug failures. TRIGGER when user asks to run a workflow, check execution status, tail logs, get execution results, or debug a workflow failure. DO NOT TRIGGER for writing YAML (use authoring) or importing/releasing workflows (use deployment)."
- use when: Run a released workflow with test parameters, check or monitor an execution, debug a failed or stalled run, or analyse failure rates across workflows.
- needs: an enabled definition ID and required parameters to start a run, or an execution ID to inspect one; Workflow scope; fleet analysis also needs Next-Gen SIEM search access.
- side effects: can contain hosts or run production response actions; helpers cannot cancel a run. ActionRequired needs console input.
- part of: step 3 of workflows.

### lookup-files
- id: crowdstrike-falcon-fusion:lookup-files (source path: skills/lookup-files/SKILL.md)
- description: "Manage Falcon Next-Gen SIEM lookup files (CSV/JSON/TXT) for CQL match() queries. TRIGGER when user asks to create, list, update, or delete lookup files, or needs help with CQL match() function. DO NOT TRIGGER for Fusion workflows, action discovery, or workflow deployment — use the workflows/authoring/deployment skills."
- use when: Upload, update, download or delete a Next-Gen SIEM lookup file (CSV/JSON/TXT), or debug why CQL `match()` returns nothing.
- needs: an NG-SIEM-enabled CID; NGSIEM Lookup Files read (browse) or read/write (manage).
- side effects: an upload with an existing name silently overwrites, so it lists first; deletes are permanent. Content updates do not preserve UI labels. The maintainer `verify_lookup.py` uploads, queries and deletes data (not read-only verification), and additionally needs NGSIEM read/write scope.
- part of: standalone branch from workflows.

### setup
- id: crowdstrike-falcon-fusion:setup (source path: skills/setup/SKILL.md)
- description: "Configure CrowdStrike Falcon API credentials for the fusion-skills plugin. TRIGGER when user asks to set up credentials, configure API access, or runs into authentication errors."
- use when: Falcon API credentials are missing or failing, or the user wants to switch cloud/profile or use 1Password references for the Fusion helpers.
- needs: a Falcon API client; optional signed-in 1Password CLI.
- side effects: writes `~/.cache/crowdstrike-falcon-fusion/credentials.toml` (secrets are typed into the user's own editor, never chat) and may install a CLI after asking.
- part of: standalone prerequisite helper; unnecessary when auth already works.

### foundry-redirect
- id: crowdstrike-falcon-fusion:foundry-redirect (source path: skills/foundry-redirect/SKILL.md)
- description: "TRIGGER when the user asks to "build a Foundry app", "create a Foundry app", mentions manifest.yml, or needs a UI page/extension, serverless function, collection, or a custom API integration from a third-party API (Okta, ServiceNow, Jira, etc.) built. DO NOT TRIGGER for a standalone Fusion workflow that only wires together existing actions. This skill declines Foundry-app requests and points to the crowdstrike-falcon-foundry plugin, so the redirect works even without plugin hooks; it yields to the real Foundry plugin when that plugin is also installed."
- use when: Something must be built (Foundry app, UI page, function, collection, reusable custom API action, manifest.yml): declines to write YAML and points to the crowdstrike-falcon-foundry plugin. A one-off HTTP call or alert-population query stays in Fusion authoring.
- part of: redirect to crowdstrike-falcon-foundry:development-workflow, which it yields to when installed.
