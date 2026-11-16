---
name: documentation-pattern-refactor
description: Establish and enforce an audience-based documentation layout with README/USERS/DEVELOPERS/TODO rules, classify existing content into those domains, report structural and domain mismatches, and execute audit/scaffolding/restructuring refactors with explicit confirmation gates.
---

# Documentation Pattern Refactor

Use this skill to apply documentation governance based on two equally required checks:
1) physical structure (`README.md` / `USERS.md` / `DEVELOPERS.md` / top-level `TODO.md`), and
2) information-domain classification (what content belongs in which audience doc).

## Classification-First Compliance Gate (Mandatory)
Never return a "compliant" verdict from file presence alone.

Compliance can be declared only when both pass:
1. Structural presence checks, and
2. Section-level classification checks with evidence.

If classification evidence is missing, the verdict must remain "not yet compliant" and the response must request or produce the missing section-level classification audit.

## Refactor Levels (Required)
Always confirm the requested level before making recommendations or edits.

- `audit`
  - Generate audit artifacts and report how current docs align to both structure and domain classification rules.
  - No file edits.
- `scaffolding`
  - Create missing audience docs and add guidance/relocation markers in existing sections.
  - Do not relocate substantive content yet.
- `restructuring`
  - Relocate content to correct audience docs and split large single-topic blocks into focused sub-domain files to improve indexing and progressive disclosure.
  - Reduce redundant documentation by converging equivalent guidance to one canonical location and replacing non-canonical copies with concise links.

If user intent is ambiguous, default to `audit` and ask whether they want `scaffolding` or `restructuring` next.

## Redundancy Reduction Policy (Mandatory for `restructuring` and cleanup/improve requests)
When user intent includes cleanup, reducing duplication, or improving maintainability, treat redundancy reduction as an explicit required objective.

Rules:
1. For each repeated topic, choose one canonical section (`canonical source`) based on audience ownership and the Change-Driven Update Matrix.
2. Remove non-canonical duplicate prose where content is materially equivalent.
3. Replace removed duplicate prose with a short audience-appropriate pointer to the canonical location.
4. Keep duplication only when the content is intentionally audience-specific and non-equivalent (for example: brief README capability summary vs USERS operational steps vs DEVELOPERS implementation details).
5. Do not keep parallel full-procedure copies across docs for the same audience intent.
6. Every dedupe decision must be traceable in artifacts (`source -> canonical -> action -> rationale`).

## Quick Start
Resolve scripts and references relative to this skill directory, not the target workspace.
The examples below run from the skill directory; use absolute script paths when
running from another working directory.

1. Run an audit:
```bash
python3 scripts/audit_docs_pattern.py --root <workspace> --scope root --strictness balanced --output-dir <workspace>/.codex/artifacts/doc-pattern
```
By default, hidden leading-dot directories (for example `.codex`, `.agents`) are excluded to reduce false positives. Include them only when explicitly requested:
```bash
# Include one specific hidden directory
python3 scripts/audit_docs_pattern.py --root <workspace> --scope root --output-dir <workspace>/.codex/artifacts/doc-pattern --include-hidden-dir .codex

# Include all hidden directories
python3 scripts/audit_docs_pattern.py --root <workspace> --scope root --output-dir <workspace>/.codex/artifacts/doc-pattern --include-hidden-dirs
```
Use `--scope all` only when the user explicitly asks to enforce module/subdirectory triads.
2. Review significant divergences in `divergence_report.md`.
3. Build and review `classification_report.md` from the audit output (section-level mapping with rationale).
4. Ask whether to generate and execute a refactor plan.
5. Generate a level-aware plan:
```bash
python3 scripts/generate_refactor_plan.py --divergence-json <workspace>/.codex/artifacts/doc-pattern/divergence_report.json --output-dir <workspace>/.codex/artifacts/doc-pattern --level <audit|scaffolding|restructuring>
```
6. Confirm level-aware artifacts exist:
- `migration_markers.md` for `scaffolding`
- `migration_actions.md` for `restructuring`
7. Before edits, offer a stash snapshot.

## Domain Classification Rules (Mandatory)
The portable baseline is bundled in `references/pattern_spec.md`, including the Documentation Placement Rules and Change-Driven Placement Matrix. No external repository is required.

Apply these rules when classifying content:

### `README.md` - Entry Point
Use for:
- high-level project description
- capability summary
- links to deeper docs

Avoid:
- configuration details
- operator workflows
- developer implementation instructions

### `USERS.md` - Operators / Runbook
Use for:
- installation/startup
- configuration and runtime flags
- UI/runtime behavior and troubleshooting
- operator workflows

Avoid:
- internal architecture
- implementation patterns

### `DEVELOPERS.md` - Developers
Use for:
- architecture/code structure
- local setup/build/test/debug
- implementation standards and extension patterns
- documentation placement and change-driven update rules

Avoid:
- operator runbook narratives

### `TODO.md` - Future Work Only
Use for:
- actionable enhancements
- known gaps/refactors
- deferred design questions

Avoid:
- restating current behavior
- documenting already-implemented requirements

### Change-Driven Update Matrix
Use this matrix when deciding where to place updates:
- New/changed CLI flag or env var -> `USERS.md` (+ `DEVELOPERS.md` if dev-impacting)
- UI behavior changes -> `USERS.md`
- Operator-actionable error/logging behavior -> `USERS.md` (+ `DEVELOPERS.md` if debugging-related)
- New major capability -> `README.md` + `USERS.md` + `DEVELOPERS.md` (+ `TODO.md` for follow-ups)
- Internal refactor with no user impact -> `DEVELOPERS.md` (if useful)
- New dev tooling/tests -> `DEVELOPERS.md`
- Deferred work/design questions -> `TODO.md`

## Required Introductory Reply (Non-Compliant Repos)
When the target repo is not currently aligned, the first substantive response must include:
1. a brief explanation that both structure and domain classification will be audited,
2. a concise summary of the placement rules above (`README.md`, `USERS.md`, `DEVELOPERS.md`, `TODO.md`),
3. a concise summary of the Change-Driven Update Matrix (at least flag/env, UI behavior, operator-actionable errors, major capability, internal refactor, dev tooling/tests, deferred work),
4. the available refactor levels (`audit`, `scaffolding`, `restructuring`) and what each does,
5. the default scope rule (`root` unless user explicitly requests `all`).

Do not skip this intro when the repo is non-compliant.

### Intro Response Minimum Content Contract (Non-Compliant)
Treat repos as non-compliant when divergence is known or strongly suspected until the audit proves otherwise.
The first substantive response must be concise and actionable, and must explicitly include:
- Dual compliance statement: structure + section-level domain classification are both required.
- Placement-rules summary: what belongs in `README.md`, `USERS.md`, `DEVELOPERS.md`, `TODO.md`.
- Change-driven matrix summary: where updates go by change type.
- Refactor levels: `audit`, `scaffolding`, `restructuring`.
- Scope default: `root` unless user explicitly requests `all`.

## Pattern Definition
Read `references/pattern_spec.md` before proposing any refactor.

Core expectations:
- `README.md`: high-level entry point and links.
- `USERS.md`: operator/runbook usage and troubleshooting.
- `DEVELOPERS.md`: architecture, setup, testing, implementation conventions.
- `TODO.md`: curated future enhancements only.
- Root directory triad (`README.md`, `USERS.md`, `DEVELOPERS.md`) is the default recommendation.
- Evaluate subdirectory/module triads only when the user explicitly requests module-level enforcement.
- Keep `TODO.md` top-level only.

## Workflow
1. Confirm refactor level (`audit`, `scaffolding`, `restructuring`) and scope (`root` default, `all` only by explicit request).
2. If non-compliant, provide the required introductory reply.
3. Audit workspace docs with `scripts/audit_docs_pattern.py`.
4. Produce a domain-classification report with misplaced-content findings by file/section.
5. Present significant divergences first (high/medium), then advisories.
6. Ask whether to proceed with refactor planning.
7. Generate a written plan via `scripts/generate_refactor_plan.py`.
8. Ask whether to execute the refactor.
9. Before execution, offer a stash backup command:
```bash
git stash push -u -m "doc-pattern-refactor-prep-<timestamp>"
```
10. Execute by level:
- `audit`: no edits.
- `scaffolding`: add missing docs/templates, add relocation markers (for example `<!-- DOC-RELOCATE: move to USERS.md#runtime-flags -->`) without moving substantive content.
- `restructuring`: relocate content to proper audience docs; split oversized single-topic sections into sub-domain docs where useful for indexing/progressive disclosure.
  - During `restructuring`, perform redundancy reduction per policy: collapse materially equivalent content into one canonical section and replace duplicates with concise links.
11. For `scaffolding` and `restructuring`, ensure the destination repo `DEVELOPERS.md` includes the Documentation Placement Rules and Change-Driven Update Matrix (or links to an equivalent canonical section).
12. Offer rollback commands after any refactor:
```bash
git stash list
git stash show -p stash@{n}
git stash apply stash@{n}
```

## Completion Gate - DEVELOPERS Rules Propagation (PLAN-03)
Before marking `scaffolding` or `restructuring` complete, explicitly validate all of the following:
- Destination repo `DEVELOPERS.md` includes Documentation Placement Rules and Change-Driven Update Matrix, or explicit links to an equivalent canonical section.
- Validation result is stated in the final response as a completion gate outcome (`pass`/`fail`).
- If missing, task status remains incomplete and the response must include a concrete follow-up action.
- Do not waive this gate for "quick fix", "minimal", or time-boxed requests.

## Strictness Modes
- `balanced`: default. Emphasize structural and major audience mismatches.
- `strict`: escalate all divergence severities one level.
- `advisory`: downgrade hard failures into recommendations.

## AGENTS Handling
Audit `AGENTS.md` issues but do not auto-edit AGENTS files. If AGENTS refactoring is needed, recommend using the sibling `agent-instructions-cleanup` skill (`$agentic-devcraft:agent-instructions-cleanup` in Codex, `/agentic-devcraft:agent-instructions-cleanup` in Claude, or attach the skill in Air).

## Output Requirements
Always produce or reference these artifacts when running the scripted audit/plan flow:
- `doc_inventory.json`
- `divergence_report.json`
- `divergence_report.md`
- `refactor_plan.md`

For domain-classification/refactor levels, also produce:
- `classification_report.md` (section-level mapping: current location -> target location -> rationale)
- `migration_markers.md` (for scaffolding) or `migration_actions.md` (for restructuring)

For redundancy-reduction `restructuring`/cleanup work, also produce:
- `redundancy_actions.md` (or section in `migration_actions.md`) with one row per duplicate group:
  - duplicate sources,
  - chosen canonical location,
  - action taken (`remove`, `replace-with-link`, `retain-audience-summary`),
  - rationale tied to placement/matrix rules.

`classification_report.md` must include, at minimum, one row per relevant section with:
- source file + section heading,
- target file + target section,
- placement rationale tied to the documented audience/placement rules.

`divergence_report.md` must include domain-mismatch findings with actionable relocation targets (not structural findings only).

## Implementation Guardrails
- Do not silently apply documentation refactors.
- Keep recommendations evidence-based with file paths and rule IDs.
- Prefer moving content over duplicating content.
- Prefer canonicalization + linkback over maintaining parallel prose for equivalent guidance.
- Keep terminology and headings consistent across related docs.
- Exclude leading-dot directories from audit/classification by default; include them only when the user explicitly requests hidden-directory analysis.
- Do not require subdirectory audience-doc triads unless audit scope is explicitly `all`.
- Do not claim compliance based only on file presence; verify domain placement/classification.
- Do not close `scaffolding` or `restructuring` without explicitly reporting the DEVELOPERS rules-propagation gate result.
- Do not close redundancy-reduction work until duplicate groups are mapped to canonical owners and link replacements are validated.

## Rationalization Counters
| Rationalization | Counter |
| --- | --- |
| "The files exist, so the docs are compliant." | Structural presence is necessary but insufficient; run domain classification and placement checks. |
| "I can answer compliance from top-level triad presence alone." | A compliance verdict requires section-level classification evidence and relocation rationale where mismatches exist. |
| "I can skip the standards summary in the intro." | For non-compliant repos, the first substantive response must include placement rules, matrix summary, levels, and scope default. |
| "Scaffolding and restructuring are basically the same." | Keep levels distinct: scaffolding adds structure/markers only; restructuring performs relocations/splits. |
| "I should skip the policy section to keep changes small." | `scaffolding`/`restructuring` are incomplete until `DEVELOPERS.md` includes (or links to) Documentation Placement Rules and Change-Driven Update Matrix. |
| "Keeping duplicate text is safer than linking." | For materially equivalent guidance, keep one canonical source and replace other copies with concise links to prevent drift. |
| "Both copies are useful, so I’ll keep full text in both files." | Preserve discoverability with audience-specific summaries, but avoid full parallel procedures; link to canonical details. |
| "I can infer module enforcement from context." | Confirm scope explicitly (`root` or `all`) before module-level expectations. |
| "Missing subdirectory docs are always high severity." | Subdirectory triad gaps are reportable only when scope is `all`. |
| "Script outputs are fine with just divergence and plan files." | PLAN-05 requires classification and level-aware migration artifacts (`classification_report.md`, `migration_markers.md`, `migration_actions.md`). |
| "Hidden directories should always be scanned." | Hidden leading-dot directories are excluded by default to reduce false positives; include only when user explicitly requests them. |

## Red Flags
- Reporting only structural gaps without classifying content domains.
- Declaring compliance without section-level classification evidence.
- Finishing `restructuring` cleanup without a canonical-source decision per duplicate topic.
- Retaining materially equivalent full-procedure copies across files instead of replacing with canonical links.
- Omitting the introductory standards brief in a non-compliant repo.
- Initial response missing matrix summary and explicit scope/level framing.
- Failing to present or honor refactor levels (`audit`/`scaffolding`/`restructuring`).
- Performing restructuring edits when user approved only scaffolding.
- Recommending module triad creation without explicit `scope=all` request.
- Running refactor edits before explicit execution approval.
- Completing `scaffolding` or `restructuring` without validating the destination `DEVELOPERS.md` policy baseline.
- Scripted flow emits only structural artifacts (no `classification_report.md` or level-aware migration artifact for the selected level).
- Hidden leading-dot directories are scanned without an explicit user request.
