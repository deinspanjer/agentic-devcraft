# Spec Delta

## Purpose

Preserve project guidance while simplifying instruction files according to the harnesses that will actually consume them.

## ADDED Requirements

### Requirement: Select instruction files by target harness
The workflow SHALL establish the target harness or harnesses before recommending file selection or precedence. OpenCode V2 SHALL use `AGENTS.md`; Codex override precedence MUST NOT be applied as a universal rule.

#### Scenario: OpenCode is the only target
- **WHEN** the user requests instruction cleanup for OpenCode V2
- **THEN** the plan uses `AGENTS.md`, explains combined instruction scope, and does not recommend `AGENTS.override.md` as an OpenCode override

#### Scenario: Codex is a target
- **WHEN** the target includes Codex
- **THEN** the plan retains Codex's first-non-empty-file selection semantics at each level and does not describe an override as erasing ancestor guidance

#### Scenario: Target is unclear or shared
- **WHEN** file selection could change which instructions the intended harnesses receive
- **THEN** the workflow clarifies the target or obtains approval for an explicitly documented cross-host layout before proposing replacements

### Requirement: Preserve guidance from every inventoried file
The workflow SHALL include every instruction in the preservation map before proposing removal, migration, or replacement, including guidance in files ignored by the current host. Every removal MUST have an explicit retained or migrated destination.

#### Scenario: OpenCode ignores an existing override file
- **WHEN** the inventory contains both `AGENTS.md` and `AGENTS.override.md`
- **THEN** the workflow preserves both files' guidance in its map and does not silently delete the override merely because OpenCode ignores it

### Requirement: Retain staging and approval gates
The workflow SHALL stage proposed changes in a dated shallow mirror, produce the preservation report and index, stop on conflicting or uncertain destinations, and require confirmation before in-place edits. Ignore recommendations MUST depend on Git context and target-host relevance.

#### Scenario: User has not approved application
- **WHEN** the mirror and report are ready but in-place approval is absent
- **THEN** original instruction files remain unchanged

#### Scenario: Override ignore advice is irrelevant
- **WHEN** the target is OpenCode-only and no relevant local override use is established
- **THEN** the workflow does not prescribe a Codex override ignore rule as a prerequisite
