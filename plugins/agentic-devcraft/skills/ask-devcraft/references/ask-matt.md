# Ask Matt (Matt Pocock skills)
Source: https://github.com/mattpocock/skills @ 5863806dd4e15c63174bee4e7515a4256792ecfa
Distribution (mattpocock/skills): one collection, the plugin `mattpocock-skills` (marketplace `mattpocock`, in the repository). Its README gives a route per host: Claude Code (`claude plugin install mattpocock-skills@claude-plugins-official`), Codex and GitHub Copilot (`plugin marketplace add mattpocock/skills`), Gemini CLI, and `npx skills@latest add mattpocock/skills -a <agent>` for Cursor, OpenCode and other agents. Skill directories are `skills/<group>/<skill>/`.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Availability lines are one OpenCode host's snapshot from 2026-11-17 (plugin `mattpocock-skills` 1.3.2), not proof of installation anywhere else.

## Delegation

`ask-matt` is this source's own router. Hand its kind of question to it instead of re-deriving the routing here; this file decides whether to hand off and matches single skills.

- ask-matt is installed and the question is its kind (what comes next between an idea and shipped code, which of the grilling, spec, ticket, implementation, review or retro skills applies, or whether to continue, clear, compact, hand off or delegate at a phase boundary): recommend that the user invoke `ask-matt`. It is user-invoked only, so give its host-visible name.
- Preserve its sequence and gates (the `gates` and `phase boundaries` lines of its record below) when relaying its answer or reading it as a reference. Its own rule applies too: read the target SKILL.md before describing a skill or advising a skipped step. A substitute skill from another source is a different workflow and must be labelled as one.
- Check the next step. ask-matt names skills whether or not they are installed. Verify that the immediate next step is exposed in the session and describe later steps as unverified. Name an uninstalled step directly as remote-only, not as a step the user can invoke now.
- ask-matt is not installed, but Pocock skills are (an installed skill's name matches a record below and its description matches that record's description): match a single skill from the records below and recommend the one that fits first. Then add one line: installing `ask-matt` from the same source (`skills/engineering/ask-matt/`, with its `PHASE-BOUNDARIES.md`; it is in the `mattpocock-skills` plugin manifest) would give better answers next time. That note is never a prerequisite and never displaces a fitting installed skill. The router record is orientation, not a replacement for the installed router.
- No Pocock skill is installed: this is a source the user does not have; ask before introducing it.
- One skill plainly fits: route to it directly, without the router (a hard bug is `diagnosing-bugs`, a message that did not land is `wait-what`).
- Outside the collection: ask-matt routes only its own skills; the twelve upstream skills outside the plugin manifest (last two sections) are not in its map.

## Family: mattpocock-skills
- source repo: https://github.com/mattpocock/skills (plugin `mattpocock-skills` 1.3.2; skills in `skills/engineering/`, `skills/productivity/`, `skills/in-progress/`, `skills/misc/`)
- manifest notes: Claude Code plugin only (`.claude-plugin`; 27 skills listed, ask-matt included). No Codex or Cursor manifest, MCP server, connector, hook or command. No auth policy. Engineering skills assume an issue tracker, triage labels and doc layout set up by `setup-matt-pocock-skills`. Skills call each other with "Call the Skill tool with ..." and ask-matt assumes `/clear` and `/compact`. The `in-progress/` and `misc/` skills (12) are outside the plugin manifest. Copied as loose directories (for example through a skill catalog) they have no namespace; the plugin form is `mattpocock-skills:<name>`. pstack also ships a `teach`: a different skill, so match by description.
- router: `ask-matt`, covering the whole manifest (26 skills referenced). Its record below carries the main flow, on-ramps, gates and phase boundaries.
- development distance: core-dev (the `in-progress` writing and personal-workflow skills are adjacent; `scaffold-exercises` is course-authoring)
- disclosure recommendation: router-delegated. ask-matt owns the sequence and gates, so the other records are matching one-liners. Partial installs often lack the post-grilling main flow (`to-spec` to `pr`) and the setup precondition: check each step against the inventory and present an absent one as not installed, never as invocable.

### ask-matt
- id: mattpocock-skills:ask-matt; source path: skills/engineering/ask-matt/SKILL.md (+ `PHASE-BOUNDARIES.md`)
- description: "Ask which skill or flow fits your situation. A router over the skills in this repo."
- use when: "I don't remember which skill or flow fits my situation": what comes next from idea to shipped code, whether to continue, clear, compact, hand off or delegate at a phase boundary.
- not for: a single obvious skill (a hard bug is `diagnosing-bugs`, a message that did not land is `wait-what`); discovering or routing skills outside this collection. Its engineering flows can apply to platform or service code too.
- needs: access to target SKILL.md files before describing them, plus `PHASE-BOUNDARIES.md` for boundary decisions; user-invoked only (`disable-model-invocation: true`, Codex `allow_implicit_invocation: false`). Routes to every skill in its map whether or not it is installed, including prototype, to-spec, to-tickets, implement, implement-spec, tdd, code-review, pr, wayfinder, to-questionnaire, setup-matt-pocock-skills and Pocock's teach (not pstack's `teach`).
- side effects: none; read-only. It names a skill or flow and stops.
- part of: entry router for mattpocock-skills.
- routes: main flow `grill-with-docs` (`grill-me` if no working directory) -> [needs a runnable answer? `handoff` out, `prototype`, `handoff` back] -> multi-session build? yes: `to-spec` -> `to-tickets` -> `implement` per ticket (`/clear` between) or `implement-spec` for the whole spec; no: `implement` in the same context -> `tdd` and `code-review` (run by implement) -> `pr` -> `retro`. On-ramps: `triage` (only issues you did not create), `diagnosing-bugs` -> `retro` -> `improve-codebase-architecture` if no seam, `wayfinder` (hands off at `to-spec`, never straight to `implement` unless the effort turned out small). Spare moment: `improve-codebase-architecture`, its pick goes into `grill-with-docs`, designed with `codebase-design`. Vocabulary: `domain-modeling`, `codebase-design`. Standalone: `research`, `to-questionnaire`, `wizard`, `wait-what`, `teach`, `writing-for-agents`.
- gates: steps 1-3 in one unbroken context window (no compact or clear until after `to-tickets`; compact at the nearest boundary near ~150k tokens); each `implement` starts fresh from its ticket; run `retro` in the session it reviews, before clearing; do not triage `to-tickets` output; read the target SKILL.md before describing it or advising a skipped step; run `setup-matt-pocock-skills` before the first engineering flow.
- phase boundaries (PHASE-BOUNDARIES.md; decide only at a boundary, first yes wins): 1 continue if the next phase needs this as a primary source or fits the smart zone; 2 `/clear` if the context is irrelevant; 3 `handoff` only for a new harness, directory or repo, colleague, or a mid-phase side task; 4 subagent if tightly scoped and unattended; 5 otherwise `/compact` with an instruction (default, not the first reach).
- invocation: upstream user-invoked only.

## Records: mattpocock-skills (matching only; ask-matt owns routing)

### grill-with-docs
- id: mattpocock-skills:grill-with-docs; source path: skills/engineering/grill-with-docs/SKILL.md
- description: "A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go."
- use when: You have a plan inside a repo and want it stress-tested while the vocabulary and key decisions are written down; step 1 of the ask-matt main flow. For a plan, or a goal that changed; it does not check built work against intent.
- side effects: writes `GLOSSARY.md` and ADR files as terms and decisions settle (it runs `grilling` and `domain-modeling`).
- invocation: upstream user-invoked only

### prototype
- id: mattpocock-skills:prototype; source path: skills/engineering/prototype/SKILL.md
- description: "Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like."
- use when: A design question needs a runnable answer: does a state model or logic feel right, or what should a UI look like (throwaway code).
- invocation: upstream model-invocable

### to-spec
- id: mattpocock-skills:to-spec; source path: skills/engineering/to-spec/SKILL.md
- description: "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed."
- use when: The idea is settled and a multi-session build follows: turn the conversation into a spec without a new interview.
- invocation: upstream user-invoked only

### to-tickets
- id: mattpocock-skills:to-tickets; source path: skills/engineering/to-tickets/SKILL.md
- description: "Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker)."
- use when: Split a spec, plan or conversation into tracer-bullet tickets that declare blocking edges.
- invocation: upstream user-invoked only

### implement
- id: mattpocock-skills:implement; source path: skills/engineering/implement/SKILL.md
- description: "Implement a piece of work based on a spec or set of tickets."
- use when: Build one ticket or a small piece of work in the current context; runs `tdd` and `code-review` per ticket.
- invocation: upstream user-invoked only

### implement-spec
- id: mattpocock-skills:implement-spec; source path: skills/engineering/implement-spec/SKILL.md
- description: "Implement the result of /to-spec and /to-tickets in code."
- use when: Build a whole to-spec/to-tickets result in one orchestrated run with parallel implementer subagents.
- invocation: upstream user-invoked only

### tdd
- id: mattpocock-skills:tdd; source path: skills/engineering/tdd/SKILL.md
- description: "Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests."
- use when: Build a feature or fix a bug test-first (red, green, refactor), or write integration tests, without a full spec. Seams are written down and confirmed with the user before any test, so effort lands on critical paths, not every edge case; one test per slice. Names implementation-coupled, tautological and horizontally sliced tests as anti-patterns.
- invocation: upstream model-invocable

### code-review
- id: mattpocock-skills:code-review; source path: skills/engineering/code-review/SKILL.md
- description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X"."
- use when: Review a branch, PR or work in progress since a fixed point on two axes, repo standards and spec, "review since X". The Spec axis reports missing requirements, behaviour that was not asked for (scope creep) and wrong implementations, quoting the spec; the Standards axis adds a smell baseline that flags speculative generality and middle-man layers. Reports only; edits nothing.
- needs: a fixed point (it asks when none is given); a spec source (issue references in the commits, a path, or a file under `docs/`, `specs/` or `.scratch/`), without which the Spec axis is skipped and reported as "no spec available"; the tracker set up by `setup-matt-pocock-skills`; two parallel sub-agents.
- invocation: upstream model-invocable

### pr
- id: mattpocock-skills:pr; source path: skills/engineering/pr/SKILL.md
- description: "Use when writing a PR body."
- use when: Writing a pull request body: smallest visual, before/after evidence, one-way or two-way door.
- invocation: upstream model-invocable

### retro
- id: mattpocock-skills:retro; source path: skills/engineering/retro/SKILL.md
- description: "Conduct a retrospective on a coding session."
- use when: After a build that went sideways or a bug diagnosis: what in the agent's environment (pointers, checks, standards, AGENTS.md) should change; suggestions only. Also when AGENTS.md or steering files are large: it looks for no-op instructions and for steering lines that belong in checks or coding standards.
- invocation: upstream user-invoked only

### triage
- id: mattpocock-skills:triage; source path: skills/engineering/triage/SKILL.md
- description: "Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs."
- use when: Raw incoming issues or external PRs pile up and need categorising, verifying and agent-ready briefs; only issues you did not create.
- invocation: upstream user-invoked only

### diagnosing-bugs
- id: mattpocock-skills:diagnosing-bugs; source path: skills/engineering/diagnosing-bugs/SKILL.md
- description: "Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow."
- use when: Something is broken, throwing, failing or slow, especially hard, intermittent or a regression; builds a feedback loop before theorising. Also for a claimed bug nobody reproduced: Phase 1 demands a pass/fail signal that goes red on this bug.
- invocation: upstream model-invocable

### wayfinder
- id: mattpocock-skills:wayfinder; source path: skills/engineering/wayfinder/SKILL.md
- description: "Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear."
- use when: A huge, foggy effort too big for one session; plan it as a map of decision tickets, never a well-scoped feature.
- invocation: upstream user-invoked only

### improve-codebase-architecture
- id: mattpocock-skills:improve-codebase-architecture; source path: skills/engineering/improve-codebase-architecture/SKILL.md
- description: "Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick."
- use when: A spare moment to find refactors that turn shallow modules into deep ones; HTML report then a grilling loop on the pick.
- not for: undoing what an agent over-built in one change: it is a user-invoked survey of the whole codebase that ends in a grilling session, not a diff cleanup.
- invocation: upstream user-invoked only

### codebase-design
- id: mattpocock-skills:codebase-design; source path: skills/engineering/codebase-design/SKILL.md
- description: "Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary."
- use when: Designing a module's interface, deciding where a seam goes, or making code more testable; deep-module vocabulary.
- invocation: upstream model-invocable

### domain-modeling
- id: mattpocock-skills:domain-modeling; source path: skills/engineering/domain-modeling/SKILL.md
- description: "Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR."
- use when: A fuzzy or overloaded domain term, editing `GLOSSARY.md`, or recording a hard-to-reverse decision as an ADR.
- invocation: upstream model-invocable

### research
- id: mattpocock-skills:research; source path: skills/engineering/research/SKILL.md
- description: "Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent."
- use when: You want a topic or API facts researched from primary sources by a background agent while you keep working.
- invocation: upstream model-invocable

### wizard
- id: mattpocock-skills:wizard; source path: skills/engineering/wizard/SKILL.md
- description: "Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself."
- use when: Steps only a human can do (credentials, CI secrets, a third-party dashboard, a one-off migration or cutover) need a guided script.
- invocation: upstream model-invocable

### setup-matt-pocock-skills
- id: mattpocock-skills:setup-matt-pocock-skills; source path: skills/engineering/setup-matt-pocock-skills/SKILL.md
- description: "Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills."
- use when: Once per repo before the first engineering flow: configure issue tracker, triage labels and domain doc layout.
- invocation: upstream user-invoked only

### grill-me
- id: mattpocock-skills:grill-me; source path: skills/productivity/grill-me/SKILL.md
- description: "A relentless interview to sharpen a plan or design."
- use when: Sharpen a plan, design or piece of writing when there is no working directory under it; saves nothing. In a repo use `grill-with-docs`.
- invocation: upstream user-invoked only

### grilling
- id: mattpocock-skills:grilling; source path: skills/productivity/grilling/SKILL.md
- description: "Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases."
- use when: You say "grill me" and no wrapper fits: rounds of numbered questions with recommended answers until understanding is shared.
- invocation: upstream model-invocable

### handoff
- id: mattpocock-skills:handoff; source path: skills/productivity/handoff/SKILL.md
- description: "Compact the current conversation into a handoff document for another agent to pick up."
- use when: Move work to a new harness, directory or colleague, or fork a side task mid-phase; not a substitute for `/clear` or `/compact`.
- invocation: upstream user-invoked only

### to-questionnaire
- id: mattpocock-skills:to-questionnaire; source path: skills/productivity/to-questionnaire/SKILL.md
- description: "Turn a decision you can't fully answer into a questionnaire for someone else to fill in."
- use when: The blocker is knowledge in someone else's head: turn an unanswerable decision into a questionnaire for them to fill in.
- invocation: upstream user-invoked only

### teach
- id: mattpocock-skills:teach; source path: skills/productivity/teach/SKILL.md
- description: "Teach the user a new skill or concept, within this workspace."
- use when: Learn a topic over several sessions in a stateful teaching workspace (MISSION.md, RESOURCES.md, HTML lessons, learning records). The installed `teach` is a different skill.
- invocation: upstream user-invoked only

### wait-what
- id: mattpocock-skills:wait-what; source path: skills/productivity/wait-what/SKILL.md
- description: "Stop. That last message did not land: re-pitch it."
- use when: The agent's last message did not land; re-pitch it in plain Simplified Technical English using glossary terms.
- invocation: upstream user-invoked only

### writing-for-agents
- id: mattpocock-skills:writing-for-agents; source path: skills/productivity/writing-for-agents/SKILL.md
- description: "Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md."
- use when: Creating or editing skills, `AGENTS.md`, `CLAUDE.md` or docs an agent is pointed at. Its Pruning section is the reference for cutting agent-facing docs: duplicated meanings, restated environment facts, stale sediment and no-op sentences. A wording reference with no process and no outputs.
- invocation: upstream model-invocable

## Not referenced by ask-matt: in-progress skills (5)

Upstream `skills/in-progress/`, outside the plugin manifest and ask-matt's map: a plugin install does not bring them. Match them directly.

### chief-of-staff
- id: mattpocock-skills:chief-of-staff; source path: skills/in-progress/chief-of-staff/SKILL.md
- description: "Pursue a long-running goal in a single session by co-ordinating subagents."
- use when: Pursue a long-running goal in one session by coordinating background subagents and schedules, keeping memory in a wiki.
- invocation: upstream user-invoked only; outside the plugin manifest, so a plugin install does not bring it

### loop-me
- id: mattpocock-skills:loop-me; source path: skills/in-progress/loop-me/SKILL.md
- description: "Grill me about specs for the workflows I want to build, within this workspace."
- use when: Design specs for recurring personal workflows (loops) by grilling; not a software-engineering step.
- invocation: upstream user-invoked only; outside the plugin manifest, so a plugin install does not bring it

### writing-fragments
- id: mattpocock-skills:writing-fragments; source path: skills/in-progress/writing-fragments/SKILL.md
- description: "Writing, explore: mine raw fragments, no structure yet."
- use when: Writing, explore phase: an interview that appends raw fragments to one Markdown file with no structure imposed.
- invocation: upstream user-invoked only; outside the plugin manifest, so a plugin install does not bring it

### writing-shape
- id: mattpocock-skills:writing-shape; source path: skills/in-progress/writing-shape/SKILL.md
- description: "Writing, exploit: shape raw material into an article, paragraph by paragraph."
- use when: Writing, exploit phase: shape a raw-material file into an article paragraph by paragraph from two or three candidate openings.
- invocation: upstream user-invoked only; outside the plugin manifest, so a plugin install does not bring it

### writing-beats
- id: mattpocock-skills:writing-beats; source path: skills/in-progress/writing-beats/SKILL.md
- description: "Writing, exploit; assemble raw material into a journey of beats, grounding each term before a beat leans on it."
- use when: Writing, exploit phase: build the article as beats the user picks one at a time (alternative to `writing-shape`).
- invocation: upstream user-invoked only; outside the plugin manifest, so a plugin install does not bring it

## Not referenced by ask-matt: other in-progress and misc skills (7)

Upstream `skills/in-progress/` and `skills/misc/`, outside the plugin manifest and ask-matt's map.

### claude-handoff
- id: mattpocock-skills:claude-handoff; source path: skills/in-progress/claude-handoff/SKILL.md
- description: "Hand the current conversation off to a fresh background agent that picks up the work immediately."
- use when: Hand the conversation to a fresh background Claude Code agent that starts immediately (`claude --bg`); Claude Code only.
- invocation: upstream user-invoked only; outside the plugin manifest, so a plugin install does not bring it

### setup-ts-deep-modules
- id: mattpocock-skills:setup-ts-deep-modules; source path: skills/in-progress/setup-ts-deep-modules/SKILL.md
- description: "Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and reachable only through its entry-point files. User-invoked."
- use when: Wire dependency-cruiser into a TypeScript repo so each package is a deep module reachable only through its root entry files.
- invocation: upstream user-invoked only; outside the plugin manifest, so a plugin install does not bring it

### software-factory
- id: mattpocock-skills:software-factory; source path: skills/in-progress/software-factory/SKILL.md
- description: "Shared language for designing a software factory: the tasks it runs and the services it plugs into."
- use when: Designing a software factory (agents turning tickets, PRs and schedules into merged code): shared vocabulary for tasks, runs, runners and services.
- invocation: upstream user-invoked only; outside the plugin manifest, so a plugin install does not bring it

### git-guardrails-claude-code
- id: mattpocock-skills:git-guardrails-claude-code; source path: skills/misc/git-guardrails-claude-code/SKILL.md
- description: "Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code."
- use when: Block destructive git commands (push, reset --hard, clean, branch -D) with Claude Code PreToolUse hooks; Claude Code only.
- invocation: upstream model-invocable; outside the plugin manifest, so a plugin install does not bring it

### migrate-to-shoehorn
- id: mattpocock-skills:migrate-to-shoehorn; source path: skills/misc/migrate-to-shoehorn/SKILL.md
- description: "Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data."
- use when: Replace `as` type assertions in TypeScript test files with `@total-typescript/shoehorn` for partial test data.
- invocation: upstream model-invocable; outside the plugin manifest, so a plugin install does not bring it

### scaffold-exercises
- id: mattpocock-skills:scaffold-exercises; source path: skills/misc/scaffold-exercises/SKILL.md
- description: "Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section."
- use when: Create course exercise directory structures (sections, problems, solutions, explainers) that pass `ai-hero-cli` lint.
- invocation: upstream model-invocable; outside the plugin manifest, so a plugin install does not bring it

### setup-pre-commit
- id: mattpocock-skills:setup-pre-commit; source path: skills/misc/setup-pre-commit/SKILL.md
- description: "Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing."
- use when: Set up Husky pre-commit hooks with lint-staged (Prettier), typecheck and tests in a JS/TS repo.
- invocation: upstream model-invocable; outside the plugin manifest, so a plugin install does not bring it
