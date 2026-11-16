# Spec Delta

## Purpose

Give users truthful Devcraft status for both marketplace plugins and standalone skills, including OpenCode catalog installations.

## ADDED Requirements

### Requirement: Report the loaded skill's version evidence
Status SHALL identify the loaded skill's version and provenance from locally available evidence tied to that installation. It MUST NOT substitute a remote latest version, another installation's manifest, or the current checkout's version.

#### Scenario: Catalog skill has a local release record
- **WHEN** the loaded skill directory contains valid distribution provenance
- **THEN** status reports that skill's recorded release and source, not a marketplace manifest found elsewhere

#### Scenario: No reliable release evidence exists
- **WHEN** a copied standalone skill has no valid local release record or applicable package manifest
- **THEN** status reports the skill as loaded with version unknown rather than inventing a release or development version

#### Scenario: Release records conflict
- **WHEN** applicable local version records disagree
- **THEN** status reports the conflict instead of silently preferring a convenient value

### Requirement: Separate skill availability from plugin activation
Status SHALL distinguish a loaded skill from verified active plugin state. Loading this skill alone MUST NOT establish that a plugin is installed or enabled.

#### Scenario: Standalone OpenCode catalog installation
- **WHEN** status is loaded without a native Devcraft plugin
- **THEN** it reports skill availability and local version evidence without claiming an active plugin

#### Scenario: Native plugin state is verifiable
- **WHEN** a permitted local native registry confirms the relevant Devcraft plugin's active state
- **THEN** status can report that state separately from the skill's version evidence

### Requirement: Status remains read-only
Status SHALL avoid network access, installation changes, updates, removals, and configuration mutation.

#### Scenario: User asks whether an update exists
- **WHEN** status has only local installed-version evidence
- **THEN** it reports that evidence and states that remote update availability was not checked
