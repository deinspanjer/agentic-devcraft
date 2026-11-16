# Spec Delta

## Purpose

Keep the four Devcraft skills usable from self-contained OpenCode installations without borrowing other harnesses' configuration or caches.

## ADDED Requirements

### Requirement: Self-contained runtime resources
Each skill SHALL resolve its scripts, references, templates, and metadata relative to its loaded skill directory. OpenCode execution MUST NOT require another client's home, plugin cache, sibling skills, or marketplace manifest.

#### Scenario: Skill runs outside its checkout
- **WHEN** a complete individual skill directory is installed in an isolated OpenCode source and invoked from an unrelated workspace
- **THEN** its required supporting files resolve without accessing Claude/Codex homes or an original checkout

### Requirement: Harness-specific instructions are isolated per harness
Instructions that apply to only one harness SHALL live in a separate file per harness inside the skill that uses them. The skill's main instructions MUST direct the agent to the file for the relevant harness only and MUST NOT require reading another harness's instructions or loading a sibling skill to obtain them.

#### Scenario: OpenCode agent needs harness-specific steps
- **WHEN** a skill running in OpenCode reaches a step that differs by harness
- **THEN** it reads that skill's OpenCode file and is not directed to Claude or Codex instructions

#### Scenario: Harness has no file
- **WHEN** the relevant harness has no instruction file in the skill
- **THEN** the skill reports that limitation or asks a focused question rather than applying another harness's instructions

### Requirement: OpenCode invocation is on-call only
All four skills SHALL remain registered for explicit OpenCode invocation but omitted from automatic model selection. Existing Claude/Codex invocation policies MUST remain unchanged.

#### Scenario: Normal task without a skill request
- **WHEN** OpenCode assembles its available-skill list for ordinary work
- **THEN** none of the four Devcraft skills is advertised for automatic selection

#### Scenario: User explicitly selects a skill
- **WHEN** a user selects an installed Devcraft skill through the client's native skill attachment or invocation mechanism
- **THEN** OpenCode loads that skill by its exact ID despite its on-call-only setting

### Requirement: Prerequisites and capability failures are explicit
Skills SHALL state required interpreters and host capabilities. Missing capabilities MUST produce a specific limitation or focused clarification without installing dependencies, changing global configuration, or silently substituting another host's tools or records.

#### Scenario: Python or session access is absent
- **WHEN** a requested workflow needs an unavailable interpreter or native session capability
- **THEN** it identifies the unmet prerequisite and does not claim successful execution

### Requirement: Compatibility claims require runtime evidence
OpenCode support SHALL be accepted against a recorded V2 runtime in an isolated environment using complete standalone skill directories. Validation MUST distinguish discovery, explicit loading, helper behavior, and full workflow execution, and preserve unrelated user state.

#### Scenario: Helper checks pass but capture has not run
- **WHEN** deterministic checks pass without a native end-to-end capture
- **THEN** documentation reports that distinction and does not claim capture compatibility complete

#### Scenario: Acceptance uses another installation
- **WHEN** an OpenCode probe is run
- **THEN** evidence records the executable path, runtime version, source provenance, tested client, and any capability gaps without modifying the user's normal installations
