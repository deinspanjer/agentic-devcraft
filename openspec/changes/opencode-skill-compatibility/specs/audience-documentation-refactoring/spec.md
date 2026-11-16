# Spec Delta

## Purpose

Make audience-based documentation audits and refactor plans portable across agent hosts without weakening classification or approval requirements.

## ADDED Requirements

### Requirement: Portable artifact destinations
The audit and planning helpers SHALL default to the same host-neutral artifact directory. Examples and generated instructions MUST agree on path resolution, preserve explicit output overrides, and avoid requiring `.codex` or another client's home.

#### Scenario: Audit and plan use defaults
- **WHEN** both helpers run using their documented default destination from the same workspace
- **THEN** the plan consumes the audit artifacts without relying on a harness-specific directory

#### Scenario: Existing user specifies an output path
- **WHEN** a caller supplies an explicit legacy or custom output directory
- **THEN** the helpers honor that destination rather than silently migrating its contents

### Requirement: Host-aware instruction layout findings
Documentation audits SHALL NOT classify a nested `AGENTS.md` as invalid solely because it is nested when the target harness supports scoped instructions. They MUST NOT automatically rewrite instruction files and SHALL refer substantive instruction cleanup to the sibling skill through host-appropriate invocation.

#### Scenario: OpenCode module has scoped instructions
- **WHEN** an OpenCode-targeted audit discovers `packages/web/AGENTS.md`
- **THEN** nesting alone does not produce a relocation violation

#### Scenario: Instruction guidance actually conflicts
- **WHEN** an audit identifies an instruction issue beyond supported nesting
- **THEN** it reports evidence and recommends instruction cleanup without editing the file

### Requirement: Preserve documentation workflow safeguards
The skill SHALL retain structure-plus-classification compliance, root scope by default, explicit scope and level selection, level-appropriate artifacts, restructuring traceability, and confirmation before edits. Scaffolding and restructuring MUST retain the developer-rules propagation completion gate.

#### Scenario: File presence passes but classification is missing
- **WHEN** expected audience documents exist without section-level classification evidence
- **THEN** the verdict remains not yet compliant

#### Scenario: Only audit is authorized
- **WHEN** the user selects audit
- **THEN** only requested audit artifacts are produced and target documentation is not refactored

### Requirement: Invocation references are portable
Skill prose, bundled references, and generated plans SHALL document OpenCode explicit invocation without applying the Claude/Codex plugin namespace to standalone skill IDs. Host-specific metadata MUST remain limited to its intended host.

#### Scenario: OpenCode user follows generated cleanup advice
- **WHEN** a generated plan recommends the sibling cleanup skill
- **THEN** its OpenCode invocation names the standalone skill ID and does not require a Claude/Codex marketplace namespace
