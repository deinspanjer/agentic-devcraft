# Spec Delta

## Purpose

Integrate OpenCode V2 records into the existing agent issue capture workflow without confusing subject activity, collector activity, or post-cutoff state.

## ADDED Requirements

### Requirement: Trustworthy subject and collector identity
Capture SHALL establish collector identity, subject identity, execution mode, and a source cutoff using native evidence. Parent ancestry alone MUST NOT prove a fork, and user text alone MUST NOT prove isolation. An explicitly named subject SHALL override default ancestry.

#### Scenario: Collector is a verified fork
- **WHEN** native fork metadata identifies the source session and boundary and the mode permits capture tools
- **THEN** capture reads the original subject through that boundary and records inherited context separately

#### Scenario: Identity cannot be established
- **WHEN** native evidence cannot resolve the subject or collector safely
- **THEN** capture asks one focused locator question or reports the specific limitation without scanning unrelated sessions

### Requirement: Context-preserving OpenCode routing
Capture SHALL run directly in a confirmed suitable side/fork session and delegate exactly once from an ordinary session with permitted delegation. The parent MUST pass only the bounded locator handoff and receive compact results. A collector MUST NOT recursively delegate.

#### Scenario: Ordinary OpenCode session requests capture
- **WHEN** trusted identity, cutoff, and a fresh-worker capability are available
- **THEN** the parent delegates once without inherited conversation history or parent-curated excerpts

#### Scenario: Confirmed fork forbids further delegation
- **WHEN** the fork permits reads and writes but prohibits subagents
- **THEN** it captures directly without spawning another session

#### Scenario: Required delegation is unavailable
- **WHEN** ordinary-session capture cannot create a permitted fresh worker
- **THEN** it reports that limitation instead of investigating inline or bypassing host policy

### Requirement: Original native records with immutable cutoffs
The collector SHALL retrieve authorized OpenCode source records through a verified native route, validate their session identity, and bound evidence and metrics to a frozen source boundary. Pagination and inherited events MUST NOT introduce omissions, duplicate accounting, or post-cutoff outcomes.

#### Scenario: Subject continues after capture begins
- **WHEN** new subject events arrive or a pending tool later completes
- **THEN** neither the new activity nor the updated outcome appears as evidence at the earlier cutoff

#### Scenario: Cutoff is invalid or records are inaccessible
- **WHEN** a boundary cannot be validated or a required page fails
- **THEN** capture reports the exact gap and never silently substitutes whole-session, collector, or empty-success records

### Requirement: Attributable OpenCode metrics
Metrics SHALL use subject records at the cutoff, deduplicate native calls and usage, and distinguish human, peer, generated, and unknown-origin messages. Every value MUST state source, scope, units, and as-of semantics. Missing values MUST remain unavailable, not zero or inferred from current defaults.

#### Scenario: Messages include generated content
- **WHEN** source records include synthetic messages, skill attachments, compaction, or peer-origin requests
- **THEN** human-turn counts exclude generated content, peer requests remain separate, and missing provenance remains unknown

#### Scenario: Only serialized API output size is available
- **WHEN** OpenCode exposes no physical transcript-prefix byte measure
- **THEN** physical transcript size is unavailable and any export-size measure is labeled separately rather than presented as transcript size

#### Scenario: Session totals include auxiliary generation
- **WHEN** native totals include title, compaction, capture, or later generation
- **THEN** metrics do not relabel those totals as issue-time context occupancy or selected subject activity

### Requirement: Retain packet privacy and bounded authority
OpenCode capture SHALL retain the existing capture workflow's packet contents, account attribution, de-identification defaults, frozen capture-start time, private exclusive temporary writes, output override, and compact result conventions. It MUST NOT change telemetry, publish, remediate the subject task, or expose private reasoning.

#### Scenario: Save needs approval
- **WHEN** the intended packet destination requires host approval
- **THEN** capture uses the normal approved write or compact prepared-draft handoff without claiming staging is a final packet

### Requirement: Native execution proves support
OpenCode capture support SHALL require successful native full-skill ordinary-session and suitable-fork acceptance on recorded V2 versions, including identity, cutoffs, private output, and compact parent results. Helper tests or an unsupported-host notice alone MUST NOT satisfy compatibility.

#### Scenario: Runtime capability remains unverified
- **WHEN** safe cutoff reconstruction or native routing has not been demonstrated
- **THEN** the integration remains incomplete and publication does not describe it as fully compatible
