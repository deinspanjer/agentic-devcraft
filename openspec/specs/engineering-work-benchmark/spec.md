# Engineering Work Benchmark Specification

## Purpose

Provides reproducible, inspectable evidence about how declared agent configurations perform representative engineering work without ambient workflow or historical-context contamination.

## Requirements

### Requirement: Code-only port scenario
The benchmark SHALL provide a fixture containing the existing Python Codex cost-meter implementation, behaviorally relevant embedded or self-tests, a minimal task-oriented README, and synthetic Codex state sufficient to exercise report behavior. It MUST exclude prior conversations, prior Rust design or implementation, ADRs, architecture-heavy repository instructions, and workflow, toolkit, plugin, hook, or skill influence.

#### Scenario: Inspect the prepared fixture
- **WHEN** a trial is prepared for the first baseline
- **THEN** the subject-visible repository contains only the declared code-only inputs and their recorded content digests

#### Scenario: Detect forbidden context
- **WHEN** the prepared repository or subject home contains an excluded historical, Rust-design, workflow, toolkit, plugin, hook, skill, or personal-instruction artifact
- **THEN** setup fails as contaminated before the subject receives the task

### Requirement: Two-stage engineering task
Each trial SHALL execute the initial port and the controlled extension as separate stages in the same isolated workspace and logical subject session. The initial instruction SHALL ask for a Rust standalone application beginning with working report functionality; the extension SHALL ask for a user-supplied model-price JSON file with built-in defaults when no file is supplied.

#### Scenario: Complete the initial port stage
- **WHEN** the subject finishes or reaches a declared limit on the initial instruction
- **THEN** the harness checkpoints the workspace, Git state, transcript, declared configuration, and stage-specific verification before revealing the extension

#### Scenario: Exercise the extension
- **WHEN** the initial-stage checkpoint is complete
- **THEN** the harness resumes the same subject session with only the extension instruction and scores the resulting workspace separately

#### Scenario: Preserve JSON report parity
- **WHEN** the supplied Python implementation exposes JSON report output
- **THEN** the initial-stage behavioral contract includes equivalent JSON output behavior discoverable from the supplied implementation and fixtures

### Requirement: Explicit experimental factors
Every trial SHALL declare its host, model, reasoning level, subagent or orchestration permission, context-availability condition, fixture revision, prompt revision, and repetition. The first baseline MUST use the Codex host and `code-only` context condition and MUST NOT provision a compared workflow, toolkit, skill, plugin, hook, or inherited personal configuration.

#### Scenario: Run a vanilla arm
- **WHEN** a first-baseline arm is prepared
- **THEN** its effective subject configuration is empty except for Codex authentication, the declared model settings, the code-only fixture, and harness-required runtime configuration

#### Scenario: Reject another host
- **WHEN** a first-baseline arm declares Claude or any host other than Codex
- **THEN** setup fails before launch rather than treating a host change as a model or workflow effect

#### Scenario: Compare factor values
- **WHEN** two arms are included in the same declared comparison
- **THEN** their differing model, reasoning, or orchestration factors are explicit and every undeclared factor remains equivalent

#### Scenario: Distinguish availability from directed orchestration
- **WHEN** an arm enables multi-agent support without an explicit delegation instruction and retained subagent activity
- **THEN** the result describes only subagent availability and does not claim to measure orchestration behavior

#### Scenario: Defer context treatments
- **WHEN** the code-only baseline is executed
- **THEN** neither a neutral dossier nor sanitized raw history is supplied or inferred from ambient state

### Requirement: Reproducible isolated repetitions
Each repetition SHALL start from a fresh repository and agent home, record exact fixture, prompt, harness, verifier, effective configuration, and provisioned-content digests, and use a local-only workspace. Multi-arm repetitions SHOULD be interleaved by a recorded deterministic order when the execution environment permits it.

#### Scenario: Start equivalent repetitions
- **WHEN** an arm is repeated
- **THEN** every repetition begins with matching declared inputs and no state from an earlier trial

#### Scenario: Detect runtime contamination
- **WHEN** undeclared instructions, skills, hooks, plugins, sessions, credentials beyond host authentication, later-stage prompts, verifier files, or unrelated host paths become visible during a trial
- **THEN** the trial is invalidated with contamination evidence rather than assigned an engineering outcome

#### Scenario: Record effective configuration
- **WHEN** subject setup completes
- **THEN** the result records sanitized effective configuration, loaded-content inventory, and hashes sufficient to distinguish declared setup from what the subject actually received

### Requirement: Bounded neutral user interaction
The controller SHALL use a small frozen answer policy for direct material questions and SHALL NOT volunteer missing history, architecture advice, expected implementation shape, or later-stage requirements. Questions not covered by the policy MUST stop with `scenario_gap` rather than produce an invented answer.

#### Scenario: Answer a covered question
- **WHEN** the subject asks a material question covered by the frozen policy
- **THEN** the controller returns the declared answer and records the question, answer, and policy basis as user steering

#### Scenario: Encounter an uncovered question
- **WHEN** the subject asks for a material product, scope, or authority decision not covered by the policy or visible fixture
- **THEN** the controller stops with `scenario_gap` and retains the unanswered question and partial work

#### Scenario: Continue without volunteered guidance
- **WHEN** the subject has not asked a covered material question
- **THEN** the controller provides no design hint, historical fact, or corrective steering beyond declared progress or safety boundaries

### Requirement: Discoverable behavioral verification
Hidden verification SHALL enforce only behavior reasonably discoverable from the supplied Python code, its tests, README, prompts, and synthetic fixtures. It SHALL report individual contracts for initial report parity and the pricing-file extension without comparing source layout or rewarding historical Rust implementation similarity.

#### Scenario: Verify initial report behavior
- **WHEN** the initial-stage workspace is checkpointed
- **THEN** black-box checks report each discoverable report behavior and omitted behavior separately

#### Scenario: Verify price-file behavior
- **WHEN** the extension-stage workspace is checkpointed
- **THEN** black-box checks separately exercise built-in defaults, a valid user-supplied price file, and discoverable invalid-input behavior

#### Scenario: Avoid hidden historical requirements
- **WHEN** a behavior appears only in excluded history or later Rust work
- **THEN** it is absent from deterministic acceptance criteria for this scenario

### Requirement: Calibrated and offline-rescorable verification
The verifier SHALL be calibrated against known passing alternatives and deliberately broken cases before authenticated comparisons. Persisted sanitized stage snapshots and verifier provenance MUST allow results to be rescored without rerunning the subject agent.

#### Scenario: Reject a behavioral defect
- **WHEN** a calibration workspace preserves plausible structure but violates a declared contract
- **THEN** the corresponding contract fails without requiring source similarity analysis

#### Scenario: Accept an alternative design
- **WHEN** a materially different implementation satisfies the declared behavior
- **THEN** deterministic verification passes regardless of its module or source shape

#### Scenario: Rescore a retained trial
- **WHEN** an evaluator invokes offline rescoring with a retained stage snapshot and verifier revision
- **THEN** the system produces a new verifier record linked to the immutable original trial without changing its transcript or workspace evidence

### Requirement: Separate product, engineering, and process evidence
Results SHALL keep initial-port and extension evidence separate and SHALL expose behavioral correctness, omitted behavior, source inspection, scope control, module ownership, duplication, extension locality, focused runnable checks, questions, assumptions, steering, duration, tool calls, reported token use, and process artifacts without a composite score or ordinal ranking.

#### Scenario: Inspect discovery behavior
- **WHEN** a trial completes or stops
- **THEN** the result records available trajectory evidence that the subject inspected the supplied implementation and self-tests before or during development

#### Scenario: Inspect extension locality
- **WHEN** both stage snapshots exist
- **THEN** the result reports changed modules, duplicated pricing ownership, and the locality of the extension without treating raw line count as quality by itself

#### Scenario: Report unavailable measures
- **WHEN** a host does not report a requested resource measure
- **THEN** that measure is explicitly unavailable rather than inferred or replaced with zero

#### Scenario: Summarize repeated arms
- **WHEN** a comparison contains multiple repetitions
- **THEN** every repetition remains visible and per-measure availability and medians are reported without an aggregate score

### Requirement: Local and non-mutating evaluation
Benchmark construction, execution, verification, rescoring, and reporting SHALL remain local development operations. Trials MUST NOT publish releases, push to hosted repositories, mutate external systems, or receive signing credentials.

#### Scenario: Attempt external mutation
- **WHEN** a subject attempts hosted Git mutation, release publication, signing, or undeclared network access
- **THEN** the environment blocks the attempt and records the authority violation

#### Scenario: Run deterministic preparation
- **WHEN** a developer builds and validates the fixture or verifier calibration
- **THEN** no authenticated subject trial or GitHub Actions workflow is required
