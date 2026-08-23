## 1. Code-Only Fixture

- [x] 1.1 Add a fixture manifest with an explicit Python-source allowlist, source revisions, output paths, privacy classes, and expected digests; verify missing fields, unsafe paths, duplicate entries, and source drift fail validation.
- [x] 1.2 Add a deterministic builder that copies only the declared Python implementation and self-tests, writes the approved minimal README and two exact stage prompts, and generates synthetic multi-session Codex state; verify the Python report and embedded checks execute against the generated state.
- [x] 1.3 Add the frozen direct-question answer policy with no historical or architectural guidance; verify unsupported material questions resolve to `scenario_gap` and policy entries cannot mention the extension before stage two.
- [x] 1.4 Initialize the built fixture as fresh local Git history with no source remote, alternates, reflog leakage, or later objects; verify a contamination scan cannot find excluded Rust code, history, ADRs, architecture-heavy instructions, workflow content, personal paths, or private identifiers.
- [x] 1.5 Build the fixture twice and verify matching tracked-tree, prompt, synthetic-state, policy, and manifest digests while generated/private paths remain ignored by Git.

## 2. Vanilla Factors and Isolation

- [x] 2.1 Extend benchmark-arm validation with explicit host, model, reasoning, subagent availability, context, fixture, prompt, verifier, and repetition fields; verify the first scenario rejects non-Codex hosts, context values other than `code-only`, and undeclared differences between compared arms.
- [x] 2.2 Add a vanilla preparation path that provisions no compared skills, hooks, plugins, marketplaces, sessions, or personal instructions; verify the prepared home contains only sanitized Codex authentication, declared model settings, and harness-required files.
- [x] 2.3 Record launch arguments, allowed environment keys, subject-visible configuration inventory, and exact hashes before prompting; verify secret values are redacted and unsupported Codex model/reasoning/orchestration combinations fail before launch.
- [x] 2.4 Recheck the repository and agent home at each stage boundary and trial end; verify seeded undeclared instructions, hidden verifier files, later prompts, personal configuration, and unrelated host paths invalidate the trial with contamination evidence.
- [x] 2.5 Change multi-arm scheduling to recorded repetition rounds while preserving the single-arm diagnostic path; verify a synthetic matrix runs arm A1, B1, A2, B2 and records the effective order and optional seed.

## 3. Two-Stage Scenario and Controller

- [x] 3.1 Extend controller decisions to cite frozen answer-policy entries, request neutral progress evidence, stop safely, or return `scenario_gap`; verify free-form material answers and volunteered architecture/history fail closed.
- [x] 3.2 Add declared read-only observations for Git state, recent commits, changed paths, validation claims, and stage status; verify file contents, verifier expectations, other arms, and undeclared paths never enter controller requests.
- [x] 3.3 Checkpoint the initial-port stage on completion or limit with an immutable workspace copy, Git state, transcript prefix, effective configuration, and verifier record; verify the extension prompt is absent from all stage-one subject-visible evidence.
- [x] 3.4 Resume the same native subject session with the exact pricing-file extension prompt and produce a separate extension checkpoint; verify session identity, prompt order, and initial-to-extension workspace ancestry in a deterministic two-stage trial.
- [x] 3.5 Retain partial evidence and precise termination for completion, `scenario_gap`, repeated question, turn/time/token limit, unsafe authority, setup contamination, and controller error; verify each boundary with scripted subject responses.

## 4. Discoverable Behavioral Verifier

- [x] 4.1 Create a contract inventory that links every initial-stage expectation to the supplied Python code, self-tests, README, prompt, or synthetic fixture; verify no contract cites excluded history or the historical Rust implementation.
- [x] 4.2 Add evaluator-owned black-box fixtures outside the subject workspace for text and exposed JSON report output, cost and token aggregation, model/session variation, filtering or command behavior present in the Python source, and visible error cases; verify subjects cannot list or read evaluator inputs or expected outputs.
- [x] 4.3 Implement stage-one verification with one result per discoverable report contract plus public build and focused-check results; verify the supplied Python behavior passes as the fixture oracle and targeted omitted behaviors fail independently.
- [x] 4.4 Add stage-two contracts for loading valid user price JSON and retaining built-in defaults when no file is supplied, plus invalid-input behavior consistent with visible command conventions; verify initial report contracts rerun to expose regressions.
- [x] 4.5 Calibrate both stages with at least one materially different compliant implementation shape and targeted plausible defects; verify alternatives pass, defects fail, and source/module similarity is never an input.
- [x] 4.6 Run verification against copies of stage snapshots and report verifier setup/execution failure separately from product failure; verify retained subject workspaces and original verifier records remain unchanged.

## 5. Evidence, Rescoring, and Comparisons

- [x] 5.1 Extend normalized results with stage-nested `product`, `engineering`, and `process` sections plus exact fixture, prompt, harness, verifier, model, configuration, and provisioned-content provenance; verify no aggregate score or ranking field is emitted.
- [x] 5.2 Extract trajectory evidence for source/self-test inspection, questions, assumptions, controller steering, commands, focused checks, commits, process artifacts, cleanup, turns, duration, tool calls, and reported tokens; verify unavailable host measures remain explicitly unavailable.
- [x] 5.3 Compare the two stage snapshots for changed modules, pricing ownership, duplicated logic, and extension locality, and record scope-control signals for unnecessary platform or packaging work; verify raw line count alone is never labeled design quality or rework.
- [x] 5.4 Add an optional arm-blinded qualitative record for scope control, module ownership, duplication, focused checks, and repository-instruction conflicts; verify the judge input omits arm/model labels and remains separate from deterministic results.
- [x] 5.5 Add append-only offline rescoring from retained stage snapshots; verify a rescore links the immutable trial and verifier revisions without rewriting the original transcript, workspace evidence, or executed score.
- [x] 5.6 Extend summaries with recorded execution order, repetitions, per-stage per-measure availability and medians, and plumbing-evidence labeling for one repetition; verify a summary preserves every trial and produces no composite conclusion.

## 6. Safety, Documentation, and Deterministic Gate

- [x] 6.1 Enforce local-only Git and declared-network authority for scenario trials; verify synthetic hosted push, release, signing, external mutation, and undeclared-network attempts are blocked and recorded.
- [x] 6.2 Add fixture, configuration, trajectory, result, and rescore privacy checks using synthetic credentials, personal paths, task IDs, and session identifiers; verify committable artifacts redact them while authentication remains usable only during an authorized trial.
- [x] 6.3 Document source prerequisites, fixture construction and review, factor declarations, vanilla guarantees, deterministic calibration, controller simulation, offline rescoring, result paths, privacy limits, macOS/Linux boundaries, interpretation rules, and local-only execution.
- [x] 6.4 Run the complete deterministic suite, fixture drift and contamination checks, declaration validation, verifier calibration, controller simulation, offline-rescore check, shell syntax checks, and strict OpenSpec validation; verify existing marketplaces and production skills remain unchanged.
- [x] 6.5 Produce the exact proposed Codex-only vanilla arm matrix, repetitions, supported factor combinations, execution order, model/token limits, and estimated authenticated cost for user review; do not launch subscription-backed trials before explicit approval.

## 7. Approved Vanilla Baseline Execution

- [x] 7.1 After explicit approval of the matrix and cost, run one interleaved plumbing repetition for every approved Codex vanilla arm and verify equivalent fixture/configuration evidence, session continuity, both stage snapshots, contamination status, verifier output, and credential redaction.
- [x] 7.2 Review the plumbing results for fixture, controller, verifier, factor-support, safety, privacy, and evidence defects; verify failures block further repetitions as benchmark defects rather than model outcomes.
- [x] 7.3 After the plumbing gate passes and the user approves any remaining cost, run the approved repetitions and publish a local non-ranking baseline report with every trial, stage, factor, unavailable measure, median, question, assumption, and steering event visible.
