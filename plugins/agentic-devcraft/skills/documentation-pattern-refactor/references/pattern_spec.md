# Documentation Pattern Spec

## Intent
Create clear sources of truth by separating documentation by audience and intent, then validating both structure and content-domain placement.

## Canonical Roles
- `README.md`: entry-point context, capability summary, and links.
- `USERS.md`: installation/runtime behavior, operational workflows, and troubleshooting.
- `DEVELOPERS.md`: architecture, local setup, tests, debugging, implementation conventions, and documentation placement rules.
- `TODO.md`: future enhancements, known gaps, and refactor candidates.

## Classification-First Requirement
A repository is compliant only when BOTH are true:
1. Structural layout is present (`README.md`, `USERS.md`, `DEVELOPERS.md`, and top-level `TODO.md` policy).
2. Content is classified into the correct audience domain.

Do not treat file presence alone as compliance.

## Placement Rules
### README.md
Use for high-level overview, capabilities, and doc links.
Do not store operator runbooks or developer implementation details.

### USERS.md
Use for install/startup, runtime config/flags, runbooks, UI/runtime behavior, troubleshooting.
Do not store architecture or implementation internals.

### DEVELOPERS.md
Use for architecture/code structure, local setup/build/test/debug, extension patterns, and documentation policy.
Do not store operator runbook narratives.

### TODO.md
Use for future actionable work only.
Do not restate current behavior or implemented requirements.

## Change-Driven Placement Matrix
- Changed CLI/env/runtime config -> `USERS.md` (+ `DEVELOPERS.md` if dev-impacting)
- UI behavior/workflow changes -> `USERS.md`
- Operator-actionable errors/logging -> `USERS.md` (+ `DEVELOPERS.md` for debugging context)
- New major capability -> `README.md` + `USERS.md` + `DEVELOPERS.md` (+ `TODO.md` follow-ups)
- Internal refactor/no user impact -> `DEVELOPERS.md`
- New dev tooling/tests -> `DEVELOPERS.md`
- Deferred questions/future work -> `TODO.md`

## Refactor Levels
- `audit`: report-only alignment for structure + classification; no edits.
- `scaffolding`: add missing docs and relocation markers; no substantive content moves.
- `restructuring`: relocate misplaced content and split oversized topic blocks into focused sub-domain docs for indexing/progressive disclosure.

## Audit Scope Defaults
- Default scope is `root`: enforce audience-doc expectations at repository root only.
- Optional scope is `all`: enforce module/subdirectory triad completeness where module docs exist.
- Enable `all` only when the user explicitly asks for module-level evaluation.

## Divergence Classes
- `missing_core_doc`: required audience docs missing at root (and modules only when scope is `all`).
- `todo_not_top_level`: `TODO.md` appears outside repository root.
- `agents_not_top_level`: `AGENTS.md` appears outside repository root.
- `audience_mismatch`: dominant content appears in the wrong audience doc.
- `classification_gap`: content cannot be confidently mapped to domain rules and needs explicit placement decisions.
- `significant_duplication`: substantial overlap between docs that should be consolidated.

## Severity Model
- `high`: structural violations or missing core docs.
- `medium`: major audience mismatch, classification gaps, or major duplication.
- `low`: advisory inconsistencies, weak linking, or minor drift.

## Strictness Overrides
- `balanced`: keep baseline severities.
- `strict`: upgrade `low -> medium`, `medium -> high`.
- `advisory`: downgrade `high -> medium`, `medium -> low`.

## AGENTS Policy
- Do not auto-edit AGENTS files in this skill.
- Report AGENTS-related issues with recommendation to use the sibling `agent-instructions-cleanup` skill (Codex: `$agentic-devcraft:agent-instructions-cleanup`; Claude: `/agentic-devcraft:agent-instructions-cleanup`; Air: attach the skill).

## Refactor Execution Policy
- Always require explicit confirmation before edits.
- Offer `git stash push -u` backup before applying changes.
- Provide stash restore commands after execution.

## Required Intro for Non-Compliant Repos
Before deep work, provide a concise standards brief that includes:
- structure + classification dual requirement,
- placement rules summary,
- available levels (`audit` / `scaffolding` / `restructuring`),
- scope default (`root` unless `all` explicitly requested).
