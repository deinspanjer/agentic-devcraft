# Proposal

## Why

The four released Devcraft skills share one canonical payload, but several assume Claude/Codex packaging, instruction precedence, or transcript formats. OpenCode HTTP distribution would make those assumptions user-visible; loading Markdown alone is not functional compatibility.

## What Changes

- Make all four skills explicitly invocable and on-call only in OpenCode V2, without changing existing Claude/Codex invocation policy.
- Make `status` report the loaded skill's verifiable version and provenance without equating skill availability with an active plugin or assuming a marketplace directory layout.
- Make `agent-instructions-cleanup` select instruction files and explain precedence for the target harnesses: OpenCode uses `AGENTS.md`, not Codex override precedence. Preserve every guidance item and all existing migration/approval gates.
- Make `documentation-pattern-refactor`, both Python helpers, generated guidance, and bundled references use portable output defaults and host-aware invocation and instruction-layout rules.
- Implement real OpenCode support for `capture-agent-issue`: trustworthy collector/subject identity, direct-side versus one-hop routing, original records, immutable source cutoffs, attributable metrics, privacy, and exclusive private writes. Unsupported runtime capabilities must fail safely, but a blanket unsupported-host disclaimer does not complete this change.
- Keep harness-specific instructions in one reference file per harness inside each skill, selected by a short step in its `SKILL.md`, so an agent reads only its own harness's guidance. Record this layout as the convention for future skills.
- Audit all supporting files, relative paths, metadata, tools, and interpreter requirements; validate downloaded standalone directories as well as the shared plugin layout.
- Preserve the existing Claude/Codex payload and pre-existing work; update audience documentation with verified behavior and limitations.

## Capabilities

### New Capabilities

- `portable-skill-runtime`: Self-contained skill resources, host-specific explicit invocation, runtime prerequisites, and isolated compatibility acceptance.
- `devcraft-status`: Evidence-based loaded-skill version/provenance reporting distinct from plugin activation.
- `agent-instruction-refactoring`: Preservation-first instruction migration with target-harness-aware file selection and precedence.
- `audience-documentation-refactoring`: Portable audit/plan output and host-aware instruction-layout recommendations while retaining audience and approval gates.
- `opencode-issue-capture`: OpenCode-specific identity, record retrieval, immutable cutoffs, routing, and metric accounting integrated into the existing capture workflow.

### Modified Capabilities

None in the archived capability inventory. `agent-issue-capture` exists only in the active `capture-agent-issue` change; this proposal adds the OpenCode integration contract without duplicating or rewriting that change's general packet requirements. Reconcile capability ownership at archive time if that change archives first.

## Impact

- Canonical sources only: `plugins/agentic-devcraft/skills/{status,agent-instructions-cleanup,documentation-pattern-refactor,capture-agent-issue}/`.
- Small stdlib helpers where deterministic extraction is needed; existing capture helper accepts only Claude/Codex JSONL today. OpenCode's API is a separate record format, not a new label for those records.
- OpenCode V2 native skill, session, message, and durable-log interfaces; optional OpenChamber adapters must be labeled separately from baseline OpenCode support.
- `USERS.md`, `DEVELOPERS.md`, `README.md`, focused validation, and retained non-sensitive runtime evidence. Preserve the user-confirmed Claude/Codex capture acceptance recorded in the existing change; do not reopen its removed integration matrix.
- Catalog generation/hosting, GitHub publication, native OpenCode plugin packaging, installation into the user's harness, and global source/configuration changes are separate work and not authorized here.
