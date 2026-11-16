# Design

## Context

See `proposal.md` for scope and the five delta specs for contracts. This design is needed because host-specific instruction selection and capture provenance affect safety across multiple skills.

The audited canonical payload is `plugins/agentic-devcraft/skills/`. Its two marketplace manifests remain independently consumed by Claude/Codex. OpenCode HTTP catalogs install individual skill directories, so neither those manifests nor a sibling skill is necessarily present.

Observed defects and boundaries:

- `status/SKILL.md` treats presence as activation and assumes two parent traversals reach a package manifest.
- Cleanup's workflow, guardrails, counters, red flags, and output rules apply Codex override selection globally. “Hard replacement” also needs clarification: per-directory file selection is not erasure of ancestor instructions.
- Documentation prose and both helpers default to `.codex/artifacts/doc-pattern`. Generated plans and `references/pattern_spec.md` omit OpenCode invocation. `audit_docs_pattern.py` emits `agents_not_top_level` for any nested `AGENTS.md`; the bundled baseline repeats that rule.
- Capture's launcher is portable prose, but `references/harness-records.md` and `capture_support.py metrics` implement only Claude/Codex JSONL. `save` is already a separate stdlib operation with useful exclusive-write coverage.
- `agents/openai.yaml` is Codex-specific metadata, not an OpenCode tool declaration. Python helpers use modern annotations and must declare and verify their minimum supported interpreter rather than assuming Python exists.
- Existing `capture-agent-issue` planning now records user-confirmed installed-skill acceptance on 2026-11-16. Preserve that accepted baseline; do not reopen its removed integration matrix or overwrite that change's files.

Read-only checks identified the managed executable as `/Applications/OpenChamber.app/Contents/Resources/opencode-cli/opencode`, version `2.3.0`. No user skills were installed or global configuration changed.

## Goals / Non-Goals

**Goals:** Operate from one complete downloaded skill directory; keep host differences explicit and narrow; demonstrate safe OpenCode routing and record reconstruction before claiming compatibility.

**Non-Goals:** Build or deploy the HTTP catalog, publish a release, add an OpenCode runtime plugin, reconfigure harness homes, install skills globally, introduce a transcript database or telemetry daemon, or redesign packet privacy/retention.

## Decisions

### 1. One source with narrow host profiles

Keep all edits inside the existing canonical skills and audience documentation. Do not create alternative OpenCode `SKILL.md` source trees. Supporting code remains stdlib Python where feasible.

Put harness-specific instructions in `references/harness/<harness>.md` inside the skill that needs them (`opencode.md`, `codex.md`, `claude.md`). The skill's main text stays harness-neutral: it names the task (“locate the session transcript per your harness file”) and carries one short step that identifies the relevant harness and reads only that file. No file mixes profiles for several harnesses, so nothing forces an agent to read another harness's guidance. Create a harness file only where real harness-specific content exists; a skill with none needs no such directory. An unlisted harness gets the skill's stated limitation or clarification, not a guess from another harness's file.

The selecting harness is normally the one executing the skill. Cleanup is the exception: it reads the file for each target harness whose instructions it is refactoring (decision 3).

`DEVELOPERS.md` records this layout as the convention for future skills. If two or more skills later need identical harness content, keep one shared source and have the catalog generator copy it into each skill at build time; do not build that now.

Use `metadata.opencode/autoinvoke: false` for all four skills. This hides them from OpenCode's advertised list while allowing explicit ID loading. Do not set the cross-host `disable-model-invocation` flag on refactoring/status skills merely to achieve OpenCode-only behavior; retain capture's existing explicit-only controls.

Document OpenCode's `@skill-id` form separately from OpenChamber's `$` picker and Claude/Codex namespaced forms. Do not promise UI syntax is uniform across clients.

Alternatives rejected:

- A runtime plugin to inject tools or provenance. It would make the skills-only HTTP installation depend on another installation and complicate the chosen distribution direction.
- A separate “meta-harness” router skill holding every harness's instructions. Loading a sibling skill is itself harness-specific (namespaced IDs in Claude/Codex, path-derived IDs in OpenCode), it conflicts with on-call-only registration because the router would have to be model-invocable, single-directory installs would not include it, and today no harness content is shared between skills. Per-skill harness files give the same selective reading without a cross-skill dependency.

### 2. Self-contained status evidence, not inferred activation

Read a small optional `release.json` beside each distributed `SKILL.md`, using the exact schema and fields defined in `../opencode-http-skill-catalog/design.md`, decision 3. The catalog publisher owns generating that record from one release snapshot; this change owns reading and validating it and documenting the handoff. It is publisher provenance, not a signature or proof that arbitrary local content is untampered.

Status resolves its own loaded base directory first. Prefer its applicable local release record; use a package manifest only when that directory is verifiably part of the actual loaded package. Compare applicable records and surface disagreement. A directory-only development copy without release evidence has an unknown version; do not contact GitHub or search other installations.

Report loaded-skill availability/version separately from plugin state. Only an available permitted native registry can establish active plugin state. With HTTP catalog installation, no Devcraft plugin is expected. A missing registry is unknown/not applicable, not proof of an inactive plugin.

Alternative rejected: hardcode `0.3.0` in prose or fetch remote latest. Neither proves which bytes this session loaded.

### 3. Instruction semantics follow the target, not the executing agent

Establish the intended consuming harnesses, which can differ from the host running the cleanup. For OpenCode V2, use `AGENTS.md` and explain that discovered files are combined, not automatically resolved by a Codex override rule. Keep Codex's file-selection rule scoped to Codex; do not call it full ancestor replacement. For multiple targets, preserve existing files and ask before changing which host sees which guidance. File-selection and precedence rules live in cleanup's per-harness files; the main skill keeps the harness-neutral preservation workflow and loads the file for each target.

Inventory ignored files too. Every instruction still enters the verbatim preservation map, and every proposed removal still gets a destination before any original file is edited. Keep the dated mirror, report/index, uncertainty stop, and in-place approval gate.

Audit every repeated XOR/override assertion, not just the first workflow paragraph. Override ignore advice becomes conditional on actual override use and Git context; local artifact exclusions retain their existing Git-aware preference.

Alternative rejected: simply delete override guidance. That would break useful Codex behavior and risk losing guidance in mixed-host repositories.

### 4. Portable documentation artifacts and scoped-instruction policy

Use `<workspace>/.agents/artifacts/doc-pattern` as the documented default. Resolve the audit's default against `--root`; resolve the planner's omitted destination beside its explicit divergence input. Preserve explicit paths, including existing `.codex` paths, and document the default-path change without moving existing output.

Update prose, both argument defaults/resolution, generated invocation advice, and the bundled baseline together. Nested `AGENTS.md` alone is valid for OpenCode and Codex; remove the unconditional root-only violation rather than merely replacing the host label. Continue reporting evidenced instruction issues without auto-editing them. Keep hidden-directory exclusions, root/all scope, classification, level controls, redundancy tracking, and developer-rule propagation gates.

Alternative rejected: an OpenCode-only output flag or a nested-file exception bolted onto a universally incorrect nesting rule. Host-neutral defaults and evidence-based findings are simpler.

### 5. Capture uses native OpenCode records through the existing connection

Add an OpenCode collector profile at `references/harness/opencode.md`, separate from JSONL parsing. Split the existing combined `references/harness-records.md` into `codex.md` and `claude.md` beside it, moving each profile's text unchanged and keeping the shared preamble in the worker; this relocates accepted content without altering it. Prefer available native OpenCode tools; discover exact operations rather than embedding assumed MCP names. For gaps, use the selected runtime's `opencode api` through its configured service/authentication context. Do not inspect a different Homebrew runtime's database or construct an alternate unauthenticated connection.

The official V2 API contract currently exposes:

- `Session.Info.id`, `parentID`, and an optional `fork` with source `sessionID` and `before`/`through` message boundary.
- Original projected messages with cursor pagination.
- A durable session event log with aggregate sequence and finite reads when not following.
- Message-level model/tokens/cost and distinct auxiliary usage events.

These are design inputs, not locally verified capture behavior. First compare the actual runtime schema and demonstrate the route using disposable synthetic sessions in an isolated runtime. Do not inspect unrelated live user sessions to find a convenient example.

Resolve identity and the boundary from native execution context, not guessed environment variables or recent-session ordering. A `parentID` can identify a child without establishing a copied-history fork. In ordinary mode, pass only invocation, available trusted source/collector locators, frozen pre-invocation boundary, workspace, capture-start, and absolute worker path to a fresh worker. Use the host's available native delegation tool, honoring policy and the existing compact result convention. OpenChamber session-control tools are not a baseline OpenCode requirement or a substitute for one-hop subagent routing.

For evidence at a cutoff, prefer original durable events bounded by sequence with validated message-boundary linkage. Projected messages can be mutable: a tool pending at fork time may later complete inside the same message. Merely filtering today's messages by message ID can leak future outcomes. Reconstruct or otherwise prove a frozen original prefix; fail explicitly if the runtime cannot provide it. Keep original and collector identity, fork ancestry, boundary, and inherited context distinct. No full raw export enters the ordinary parent's context.

Extend deterministic metrics only after inspecting supported schemas. A separate small normalizer for bounded native event exports is preferable to pretending OpenCode uses Claude JSONL. Keep the common private `save` operation. Count stable invocation IDs once, preserve origin uncertainty, and distinguish auxiliary generation and cumulative totals from latest request occupancy. Physical transcript bytes are unavailable unless the native source actually exposes them; serialized export bytes have a different label.

Retain only non-sensitive fixture/evidence summaries. Never render private reasoning content. Missing individual metrics can still yield a useful partial packet; missing trustworthy identity, isolation, or cutoff is a routing/evidence limitation and cannot be hidden by an unsupported-host disclaimer.

Alternative rejected: copy Markdown and declare support, use latest session totals, or treat a fresh worker as a fork. Those fail the existing capture contract.

### 6. Acceptance protects meaningful boundaries

Use focused deterministic tests for silent misaccounting, cutoff contamination, conflicting provenance, and forbidden output/side effects. Reuse existing capture save checks instead of duplicating their fixture matrix. Inspect obvious documentation/metadata changes directly and exercise native explicit loading, not string-only assertions.

Run acceptance against standalone directories in isolated temp HOME/XDG/config/data locations and an isolated V2 service. Use only required synthetic sessions; any native fork/delegation probes must remain isolated and policy-permitted. Record binary/version, client, source revision, record schema, and capability results. Do not borrow `~/.claude`, `~/.codex`, Air-generated views, or user caches.

Smoke the shared Claude/Codex payload without changing their real installations. Preserve their existing auto-invocation behavior and accepted capture baseline; these regression checks do not reopen the prior capture change's removed integration matrix.

## Risks / Trade-offs

- [Experimental session APIs can differ from published docs] → Inspect the actual targeted schema; keep the first implementation task a native capability gate. If safe routing or cutoff reconstruction is impossible, leave the task incomplete and return for a revised decision rather than weakening acceptance.
- [Catalog metadata may be absent in manual copies] → Report unknown; the skill remains useful and truthful. Catalog generation must later supply the agreed local record.
- [Host identity can be ambiguous] → Distinguish execution host from target instruction consumers; ask once before material file-selection changes.
- [Changed helper defaults affect callers] → Preserve explicit output overrides, document the new resolution rules, and do not relocate old artifacts.
- [Shared guidance changes affect existing clients] → Keep host-specific metadata scoped, preserve all gates, and smoke existing package layouts.
- [Public fixture evidence can leak session data] → Use synthetic records and scrubbed summaries only; keep packets and drafts private.

## Migration Plan

Implement the runtime preflight first, then shared portability/status, instruction and documentation changes, and native capture extraction. Keep the current canonical directories and marketplace sources intact.

Update audience docs only with behavior actually demonstrated. Coordinate release provenance with the separately explored catalog, but do not deploy it here. Do not pick a new release number by guessing or publish a partially verified compatibility claim.

Rollback consists of reverting only this change's eventual scoped implementation after inspecting concurrent work; existing packets and unrelated changes remain untouched. No global installs are part of migration or rollback.

## References

- OpenCode V2 [skills](https://opencode.ai/docs/skills/), [instructions](https://opencode.ai/docs/instructions/), [API](https://opencode.ai/docs/api/), and [OpenAPI](https://opencode.ai/docs/openapi.json), checked 2026-11-16.
- OpenChamber [skill invocation](https://docs.openchamber.dev/skills/).
- Existing `../capture-agent-issue/` proposal, design, spec delta, and tasks remain authoritative for the generic packet workflow.
