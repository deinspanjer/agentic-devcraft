---
name: agent-instructions-cleanup
description: This skill should be used when refactoring AGENTS.md / AGENTS.override.md across a project tree to enforce progressive disclosure while preserving all guidance via mandatory migration into other docs and a structured preservation map/report.
---

# Agent Instructions Cleanup

## Overview
Refactor agent instruction files into minimal, progressive-disclosure form while preserving all valuable guidance by migrating removed content into appropriate documentation and producing a dated shallow mirror plus a structured report.

## When to Use
Use this skill for any request to clean up, refactor, or minimize AGENTS instructions (AGENTS.md or AGENTS.override.md) across a repository or module tree.

## Workflow (Sequential)
1. Establish scope.
   - Identify the project tree root (user-provided or current workspace root).
   - Enumerate instruction files and supporting docs (AGENTS.md, AGENTS.override.md, README.md, DEVELOPERS.md, CONTRIBUTING.md, docs/**/*.md).

2. Inventory current guidance.
   - Extract every instruction line or rule into a numbered list.
   - Capture source path and context (which AGENTS file, section title).

3. Build the content preservation map (mandatory).
   - For each instruction, decide one destination: keep in AGENTS, move to existing doc, move to new doc, or keep with pointer.
   - Do not edit AGENTS until this map exists.
   - Enforce the “no orphaned guidance” rule: if an instruction is removed from AGENTS, it must be migrated to another doc or kept with an explicit pointer.

4. Resolve conflicts and uncertainty.
   - If instructions conflict or the correct destination doc is unclear, stop and ask for direction before proceeding.
   - Do not guess the target doc when uncertainty remains.

5. Apply progressive disclosure.
   - Enforce one effective instruction file per directory level: choose exactly one of `AGENTS.override.md` or `AGENTS.md` (never both at the same level).
   - Choose `AGENTS.override.md` only when a hard replacement is actually required at that level (for example temporary or directory-specific full replacement).
   - Otherwise keep or create `AGENTS.md` as the single effective file for that level.
   - If both files already exist at one level, treat this as conflict-risk and stop to ask unless the user explicitly asks to keep both files on disk.

6. Perform mandatory doc refactors.
   - If any instruction is removed from AGENTS, refactor the target documentation to include it.
   - When target docs do not exist, create them and link from AGENTS.

7. Write outputs to a dated shallow mirror.
   - Create `docs/agents-refactor/YYYY-MM-DD/`.
   - Output only changed/new files and the directories containing them.
   - Do not overwrite original files without approval.

8. Produce the structured report and index.
   - Write `report.md` and `index.md` in the dated output directory.
   - Ensure the report includes the preservation map and destinations for every instruction.

9. Add repo hygiene recommendations (conditional).
   - First determine whether the touched directory is inside a Git worktree.
   - Only when inside a Git repo, recommend adding `AGENTS.override.md` to `.gitignore` (or to an existing `.gitignore`) and explain why:
     - `AGENTS.override.md` commonly contains temporary or user-local hard overrides.
     - Ignoring it reduces accidental commits of personal/local guidance.
   - Only when inside a Git repo, recommend adding `docs/agents-refactor/` to `.git/info/exclude` if it is not already present.
   - Prefer `.git/info/exclude` for `docs/agents-refactor/` so local scratch output is protected without adding repository-wide `.gitignore` noise.
   - Do not recommend `.gitignore` or `.git/info/exclude` changes when the touched directory is not a Git repo.

10. Request confirmation.
   - Ask before any in-place edits or replacements.

## Required Outputs
- Dated output folder: `docs/agents-refactor/YYYY-MM-DD/`
- Shallow mirror of changed/new files
- `report.md` with preservation map and refactor justifications
- `index.md` explaining how to apply the mirror

## Required Report Format (Structured)
Use this exact structure in `report.md`:

```
# Agent Instructions Cleanup Report (YYYY-MM-DD)

## Summary
- Scope:
- Key changes:
- Conflicts resolved:

## Content Preservation Map (mandatory)
| # | Instruction (verbatim) | Source | Decision | Destination | Notes |
|---|------------------------|--------|----------|-------------|-------|
| 1 | ... | path/to/AGENTS.md | Move | docs/xyz.md#section | Rationale |

## Removed From AGENTS (with destinations)
- [ ] Instruction ... -> docs/xyz.md#section

## Kept In AGENTS (minimal set)
- [ ] Instruction ...

## Doc Refactors Performed
- File: docs/xyz.md
  - Added: ...
  - Reason: migrated from AGENTS

## Rationalizations & Counters (mandatory)
- Rationalization: "..."
  - Counter: "..."

## Open Questions / Stop-and-Ask Items
- ...
```

## Guardrails (Must Enforce)
- Enforce content preservation map before editing AGENTS.
- Enforce “no orphaned guidance.”
- Enforce stop-and-ask when target docs are unclear.
- Enforce doc refactors for every removal from AGENTS.
- Enforce creation or extension of target docs when missing.
- Enforce Codex precedence: `AGENTS.override.md` is checked before `AGENTS.md`; Codex uses only the first non-empty file at that level.
- Enforce per-level XOR: do not create both `AGENTS.md` and `AGENTS.override.md` in the same directory unless the user explicitly requests dual-file-on-disk compatibility.
- Enforce Git-context gating for ignore recommendations: only recommend `.gitignore`/`.git/info/exclude` actions when the touched directory is in a Git repo.
- Enforce local-exclude preference for refactor artifacts: recommend `docs/agents-refactor/` in `.git/info/exclude` (if missing), not repo `.gitignore`, to avoid repository clutter.

## Rationalization Counters (Required)
- "It is just docs; details can be dropped." -> "Docs encode operational guidance; preserve or migrate everything."
- "We can decide destinations later." -> "Stop and ask before moving anything without a clear target."
- "If no target doc exists, skip the content." -> "Create or extend a target doc and link it."
- "Summaries are enough." -> "Preserve verbatim instructions in the preservation map."
- "The report is optional." -> "Structured report is mandatory."
- "We should always generate both AGENTS.md and AGENTS.override.md." -> "Codex reads one file per level by precedence; choose one effective file unless user explicitly wants both present on disk."
- "A minimal AGENTS.md plus full AGENTS.override.md is always safer." -> "That creates avoidable ambiguity; default to a single effective file and document the choice."
- "We can skip ignore guidance; users will remember not to commit local files." -> "Add explicit ignore recommendations in Git repos to prevent accidental commits."
- "Put refactor outputs in repo .gitignore by default." -> "Prefer `.git/info/exclude` for local refactor artifacts to avoid polluting shared ignore rules."
- "Recommend Git ignore changes everywhere." -> "Only recommend ignore/exclude changes when the directory is actually inside a Git repo."

## Red Flags
- Editing AGENTS before the preservation map exists.
- Removing instructions without explicit destinations.
- Guessing target docs despite uncertainty.
- Failing to create/extend missing target docs.
- Skipping the structured report format.
- Writing outputs outside the dated shallow mirror.
- Creating both `AGENTS.md` and `AGENTS.override.md` at the same directory level by default.
- Treating `AGENTS.override.md` as additive instead of replacement-precedence.
- Recommending `.gitignore` or `.git/info/exclude` updates without checking Git context.
- Omitting `AGENTS.override.md` ignore recommendation in Git repos when override files are involved.
- Recommending `docs/agents-refactor/` in repo `.gitignore` instead of `.git/info/exclude` without explicit user request.

## Output File Requirements
- AGENTS file at target level (choose one by precedence and intent):
  - `AGENTS.md` as the default single effective file when no hard replacement is needed.
  - `AGENTS.override.md` only when a hard replacement is intended; include explicit “replaces AGENTS.md here” marker.
  - Do not output both at the same directory level unless explicitly requested by the user.
- report.md: structured as above, including preservation map.
- index.md: file list, purpose, apply steps, optional next steps.
