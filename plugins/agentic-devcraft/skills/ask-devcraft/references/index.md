# Index: development situations

Names are host-visible; a family in parentheses separates same-named copies. A tag names the record's file and covers names back to the previous tag: `[matt]` ask-matt.md, `[cursor]` cursor.md, `[eng]` openai-engineering.md, `[plat]` openai-platforms.md, `[anth]` anthropic.md, `[dev]` devcraft.md, `[pony]` ponytail.md, `[comm]` community.md, `[f/x]` families/x.md. ⚠ acts beyond the working tree (push, merge, deploy, spend, code sent out). "Playbook": a `poteto-mode` playbook.

## Routers

- `ask-matt` [matt]: the next step from idea to shipped code; continue, clear, compact, hand off or delegate at a phase boundary.
- `using-superpowers` [eng]: a skill check before every response; only for a user wanting it all session, else name one skill.
- `poteto-help` (picks a pstack skill; starts no work), `poteto-mode` ⚠ (runs a task under a playbook; needs a goal and pass/fail check) [f/pstack]; `dyl-mode` (stricter gates) [cursor].

## Bug or failing test

- Hard, intermittent, regressed: `diagnosing-bugs` [matt] (red command before any theory); `systematic-debugging` [eng] (root cause before any fix; stops after 3 failed fixes); Bug fix playbook ⚠ [f/pstack] (ends in a ready PR).
- Rendered web UI: `frontend-testing-debugging` [plat] (fix loop); `webapp-testing` [f/example-skills] (evidence, no fix); `control-ui` [f/cursor-team-kit]; `investigation-mode` [f/vercel].
- A platform's debugger outranks a general one (Platforms). Production errors: `sentry` [eng] (read-only).
- Compile errors, merge conflicts: `check-compiler-errors`, `fix-merge-conflicts` [f/cursor-team-kit]. Incoming reports: `triage` [matt].

## Red or flaky CI, PRs, landing

- GitHub checks: `fix-ci` ⚠ (known red check; pushes unasked), `loop-on-ci` ⚠ (pending checks, flakes) [f/cursor-team-kit]; Babysit playbook (never merges) [f/pstack].
- CircleCI: `circleci-builds`, `circleci-config` [eng].
- Flaky test: `diagnosing-bugs` [matt]. CI evidence favours the CI skill; a local repro, the debugger.
- PR shape: `pr` [matt]; `make-pr-easy-to-review` [f/cursor-team-kit]. Landing: `finishing-a-development-branch` ⚠ [eng].

## Clarifying and planning

- Interview an idea; the artifact decides: `grill-with-docs` (repo; glossary, ADRs), `grill-me` (no repo) [matt]; `brainstorming` [eng] (no code until approved; commits a spec); `doc-coauthoring` [f/example-skills] (the document is the deliverable).
- Shape before code: `architect`, `arena` (contested) [f/pstack]; `codebase-design`, `prototype` (runnable answer) [matt].
- Multi-session plan; the executor takes its own source's artifact: `to-spec` -> `to-tickets` [matt]; `writing-plans` [eng]; Multi-phase plan playbook [f/pstack].
- Too big and foggy: `wayfinder` [matt] (decisions, not deliverables); `figure-it-out` [f/pstack] (executes).

## Implementing with a process

- The plan artifact decides: tickets -> `implement`, `implement-spec` (parallel) [matt]; superpowers plan -> `subagent-driven-development`, `executing-plans` [eng]; a goal and a check -> Feature playbook ⚠ [f/pstack].
- Test-first; strictness decides: `test-driven-development` [eng] (code written before its test is deleted); `tdd` (Pocock) [matt] (red-green slices; seams agreed first); `tdd` (pstack) [f/pstack] (skips if the test path is unclear).
- Refactor: `improve-codebase-architecture` [matt] (finds candidates); Refactoring playbook, `principle-*` leaves (one rule each) [f/pstack]; `deslop` [f/cursor-team-kit] (diff clutter, not structure).
- Performance: Perf issue playbook, `benchmark-checklist` [f/pstack].

## Code review

What the user wants back decides.

- Independent, local: `requesting-code-review` [eng] (reviewer subagent); `code-review` (Pocock) [matt] (two axes: standards, spec). Correctness first, lean last: `ponytail-review` (diff), `ponytail-audit` (repo, ranked) [pony].
- Hard bug hunt or strict structure verdict: `thermo-nuclear-review`, `thermos` (findings only) [cursor]; try to break it: `interrogate`, `blast-radius` [f/pstack].
- Vendor review ⚠ (diff leaves the machine): `code-review` (coderabbit), `qodo-review` [eng].
- Review, fix and ship ⚠: `review-and-ship` [f/cursor-team-kit]. Merge risk: `assess-patch-risk` [f/codex-security].
- Feedback to act on: `receiving-code-review` [eng]; `get-pr-comments` [f/cursor-team-kit].

## Security

- Find: `security-scan` (repo), `security-diff-scan` (PR or diff) [f/codex-security] (Codex plugin; terminal fallback); `thermo-nuclear-review` [cursor].
- Findings exist: `triage-finding` -> `fix-finding` -> `verify-fix`; `threat-model` [f/codex-security].
- Platform posture: see Platforms. Secrets only a human can supply: `wizard` [matt].

## Testing and verification

- "Is it done?": `verification-before-completion` [eng] (proving command run fresh); `verify-this` [f/cursor-team-kit] (baseline vs treatment).
- Browser: `webapp-testing` [f/example-skills]; `run-smoke-tests` [f/cursor-team-kit] (existing Playwright suite).
- Reusable app-driving or model-checking skill: `create-verification-skill`, `create-formal-verification-skill` [f/pstack].

## Building apps

- Web UI from an idea: `frontend-app-builder` [plat] (concept image, then code; Codex); `frontend-design` [f/example-skills] (any stack, no tools); `index` (product-design) [plat] (prototype router).
- From a design: `figma-design-to-code` [f/figma]; `build-figma` [cursor]; `image-to-code`, `url-to-code` [plat].
- Next.js, React, shadcn: [f/vercel]. iOS: [f/build-ios-apps]. macOS: [f/build-macos-apps]. React Native: [f/expo]. Android (QA only): `android-emulator-qa` [plat].
- Game: `game-studio` (router). Charts, maps, diagrams: `data-visualization` (router) [plat].
- CLI: `cli-for-agents` [cursor]. Voice: `add-voice` [cursor] (xAI).

## Platforms, vendor SDKs, deploying

The platform decides; its debug, security and deploy skills share a file.

- Vercel: `deployments-cicd` ⚠ [f/vercel]. Cloudflare: `cloudflare` (router: product choice only), `wrangler` ⚠ [f/cloudflare]. Expo: `expo-deployment` ⚠ [f/expo]. Shopify: `shopify-onboarding-dev` [f/shopify]. Twilio: a `twilio-*-advisor` or `twilio-*-architect` planner unless the product is named [f/twilio-developer-kit].
- `supabase`, `temporal-developer`, `stripe-best-practices` [plat]; `start` (Zoom router) [f/zoom].
- `development-workflow` (Falcon Foundry router), `workflows` (Fusion router), `posthog` [eng]. `origin-api` (Cursor Origin router) [cursor].

## LLM apps, MCP servers, agents

- The provider decides; ask when unstated. Claude: `claude-api` [anth]. OpenAI: `openai-platform-api-key` first (credential gate before code), then `agents-sdk` (openai-developers) [f/openai-developers]. Several: `ai-sdk` [f/vercel].
- MCP server: `mcp-builder` [f/example-skills] (any API; no deploy); `building-mcp-server-on-cloudflare` ⚠ [f/cloudflare]; `build-chatgpt-app` [f/openai-developers].
- Host an agent: `building-ai-agent-on-cloudflare` ⚠, `agents-sdk` (cloudflare) [f/cloudflare]; `workflow` [f/vercel]; `cursor-sdk` [cursor] (Cursor agents from code).

## Agent behaviour

`principle-*` leaves are passive rules: they steer later work and fix nothing already written.

- Drifted from what was wanted. A spec or issue exists: `code-review` (Pocock) [matt] (spec axis; flags scope creep); `requesting-code-review` [eng] (against requirements). No spec: `in-your-own-words` [f/pstack] (restates the goal). Goal changed: `grill-with-docs` [matt] (re-interview; writes glossary, ADRs). Prevent: `intent-framed-agent` [comm] (may load unasked; intent frame, boundary checks).
- Does more than asked, or keeps cruft. Code (layers, speculative options, scope creep, shims, needless guards), `ponytail` [pony] (session-long mode, levels; may load unasked), or one passive rule: `principle-laziness-protocol`, `principle-subtract-before-you-add`, `principle-minimize-reader-load`, `principle-migrate-callers-then-delete-legacy-apis` (internal APIs) [f/pstack]; clean a diff: `deslop` [f/cursor-team-kit] (comments, try/catch, any-casts; not abstractions). Tests (brittle, per-function): `principle-test-behavior-not-implementation` [f/pstack] (one test at a time); `tdd` (Pocock) [matt] (agree seams first). Suite-wide redundancy: `auditing-tests` (report only; removals verified), `audit-tests` (edits) [comm]. Nothing curated fits: file backups.
- Asks, plans or reports instead of acting: `principle-never-block-on-the-human` [f/pstack] (reversible work, or narrating: do, then present). The gate is often another skill's: skip it. Finding never checked: `interrogate` [f/pstack] (run-proven only), `diagnosing-bugs` [matt] (red loop first). Nothing curated fits: cutting ceremony.
- Padded docs, comments or agent rules: AGENTS.md pruning `writing-for-agents` [matt]; prose `technical-writing`, `unslop`, comments `no-comments` [f/pstack]. `agent-instructions-cleanup` [dev] moves rules, never deletes.

## Skills, plugins, agent instructions

- Write or improve a skill; evaluation style decides: `skill-creator` [f/example-skills] (with/without runs); `writing-skills` [eng] (pressure scenarios); `writing-for-agents` [matt] (wording reference, no process).
- Score one: `plugin-eval` (router); package a plugin: `plugin-creator` (Codex) [eng], `create-plugin-scaffold` [cursor].
- Oversized AGENTS.md: `agent-instructions-cleanup` [dev] (edits after approval).
- Lessons into the setup: `retro` [matt] (suggests, then stops); `correct` ⚠ [f/pstack], `continual-learning` [cursor]; `capture-agent-issue` [dev] (evidence only).
- Can agents work in this repo: `check-agent-compatibility` [cursor].

## Long-running and multi-agent work

- One agent until a condition holds: `ralph-loop` (no enforced limit) [cursor], Autonomous run playbook [f/pstack].
- Many agents; what is split decides: ticket graph -> `implement-spec` [matt]; plan tasks -> `subagent-driven-development`; unrelated problems -> `dispatching-parallel-agents` [eng]; one brief N times -> `arena`; slices or a race -> `swarm` [f/pstack]; cloud planner tree -> `orchestrate` ⚠ [cursor].
- Catch up: `ketchup`, `recall` [f/pstack]. Move work elsewhere: `handoff` [matt].

## Repo docs, understanding, onboarding

- Layout, duplicates (README/USERS/DEVELOPERS/TODO): `documentation-pattern-refactor` [dev]. Wording: `technical-writing` [f/pstack].
- How or why code works: `how`, `why`, `teach` (pstack) [f/pstack]; `qodo-codebase-wisdom` [eng] (cross-repo). Domain terms, ADRs: `domain-modeling` [matt].

## Outside development

- `far/<area>.md`, only for a task there: documents (Office, PDF), workspace (Drive, Notion), media (Adobe, Canva, video), science, finance, gpu-simulation (NVIDIA), learning, assistant-behaviour (post-answer nudges), social (X), network (Tailscale).
- Adjacent: data analysis, `index` (data-analytics) [eng]; video as code, `hyperframes`, `remotion-best-practices` [plat].

## Same-name collisions

The description identifies the installed copy.

- `teach`: pstack (explains a change or subsystem) or Pocock (multi-session study workspace).
- `tdd`: Pocock or pstack. `code-review`: Pocock or coderabbit ⚠. `research`: Pocock or product-design.
- `index` (routers): product-design or data-analytics.
- `agents-sdk`: cloudflare or openai-developers.
