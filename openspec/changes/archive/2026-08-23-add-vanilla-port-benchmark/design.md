## Context

See [proposal.md](proposal.md) for motivation and [the engineering-work benchmark spec](specs/engineering-work-benchmark/spec.md) for observable requirements.

The completed Harbor scaffold already supports authenticated Codex and Claude launch, native session resume, isolated homes, network allowlisting, fresh comparison arms, trajectories, final artifacts, deterministic verifier records, and per-measure summaries. This scenario uses only Codex and should extend those paths rather than create another runner.

A historically guided replay would mix prior analysis and workflow influence into the first measurement. This design instead uses a purpose-built code-only fixture to establish vanilla Codex baselines before context, host, or workflow projects become experimental factors.

## Goals / Non-Goals

**Goals:**

- Make the subject's actual starting context and effective configuration inspectable and reproducible.
- Measure an initial implementation and a plausible extension separately in one continuous development trial.
- Accept behaviorally correct Rust designs without depending on the historical port.
- Support Codex model, reasoning, and subagent-availability comparisons while holding host and code-only context fixed.
- Retain enough immutable evidence for verifier improvements and offline rescoring.

**Non-Goals:**

- Reconstruct the historical meter session or infer a developer persona from it.
- Compare Claude Code with Codex in this change.
- Compare Ponytail, Superpowers, OpenSpec, or other workflow projects in this change.
- Add evidence dossiers or raw-history replay to the first baseline.
- Benchmark release publication, signing, installation packaging, or native schedulers.
- Build the later canonical-source or discover-before-inventing scenario families.
- Produce a composite score or public leaderboard.

## Decisions

### 1. Build a synthetic code-only repository, not a historical Git boundary

Add a deterministic fixture builder that selects the Python report implementation and its behaviorally relevant tests, writes a minimal neutral README, and generates synthetic Codex state. The builder records every source and output digest and rejects paths outside its explicit allowlist.

The resulting repository gets fresh local Git history created for the benchmark. It does not clone the developer's cost-meter repository, so excluded objects cannot be recovered from refs, reflogs, alternates, remotes, or object storage.

Alternatives considered:

- **Clone an early historical revision:** retains unrelated instructions, design history, and target-shaping context.
- **Copy the whole Python-era tree:** makes fixture boundaries implicit and harder to audit.
- **Hand-copy behavior into a new fixture:** risks changing the source problem and losing discoverable self-tests.

### 2. Treat context as a declared factor with `code-only` as the sole first value

Extend arm declarations with explicit `host`, `model`, `reasoning`, `orchestration`, and `context` fields. The first checked-in scenario accepts only `host: codex`, `context: code-only`, and no provisioned workflow content. Future Claude, dossier, and raw-history values require a separate OpenSpec change and new fixture digests.

The v1 `subagents-allowed` value means only that Codex multi-agent support is enabled. It does not instruct the subject to delegate and cannot be interpreted as an orchestration treatment. A future directed-orchestrator value requires an arm-specific instruction plus retained evidence that subagents were actually used.

An empty vanilla control means a disposable agent home containing only host authentication and required runtime settings. Preparation records an inventory and digest of all subject-visible configuration before the prompt is sent. The inventory is checked again after execution to distinguish agent-created artifacts from setup contamination.

Alternatives considered:

- **Use the developer's normal Codex home:** ambient skills and instructions make “vanilla” unverifiable.
- **Include Claude arms immediately:** changes the host CLI, model family, defaults, and configuration loading before the scenario and verifier are calibrated.
- **Model context as free-form arm notes:** cannot enforce equivalence or detect accidental history.
- **Include a neutral dossier immediately:** skips the code-only baseline needed to measure the dossier's later effect.

### 3. Run two checkpoints in one native session

Use Harbor's existing resume support. Stage one receives exactly the approved port prompt. At completion or a declared limit, retain an immutable workspace copy, Git state, trajectory prefix, configuration evidence, and initial verifier result. Stage two resumes the same session with exactly the pricing-file extension prompt and creates a second snapshot and result.

The extension therefore measures how the subject's own initial structure accommodates a new requirement. It is not a fresh agent repairing someone else's code. A failed or limited first stage may still receive the extension when the scenario declaration permits it, but both results retain the first-stage status so extension evidence is not mistaken for clean incremental work.

Alternatives considered:

- **Independent agents for each stage:** tests handoff quality instead of adaptability of the chosen design.
- **Only verify after stage two:** loses evidence about what initially worked and which regressions the extension introduced.
- **Tell the initial agent about the extension:** invites speculative abstractions and defeats the controlled reveal.

### 4. Keep owner interaction small and declarative

Reuse the adaptive controller with a frozen answer policy containing only decisions needed to make the supplied task executable. The controller can select a prewritten answer after a direct material question, request neutral progress evidence at declared bounds, stop for safety, or return `scenario_gap`. It cannot synthesize a design answer or volunteer historical portability, storage, parser, command, or feature-boundary analysis.

Questions, assumptions stated by the subject, controller answers, and all follow-up steering become process outcomes. Procedural model behavior that does not require a user answer is not converted into artificial conversation.

Alternatives considered:

- **No controller:** an otherwise useful trial can deadlock on a simple covered question.
- **Unconstrained testing-agent role-play:** silently introduces different architecture guidance between arms.
- **Replay historical user messages:** mixes the context treatment into the baseline.

### 5. Derive hidden contracts only from subject-visible evidence

Create evaluator-owned black-box probes by tracing the selected Python code, self-tests, README, and synthetic inputs. The inventory records the visible source for every contract. JSON output is included when the selected Python implementation exposes it. The extension adds only contracts implied by its prompt: custom prices, default fallback when absent, and input behavior discoverable from the existing command conventions.

Calibrate with minimal fixtures: at least one behaviorally valid alternative shape and targeted broken workspaces for important contracts. Historical Rust modules, names, edge cases, and architecture are not calibration inputs.

Run verification against copied stage snapshots. Store verifier revision, contract inventory digest, fixture digest, command outputs, and per-contract results. Verifier infrastructure failure is distinct from product failure.

Alternatives considered:

- **Use the historical Rust test suite:** imports undiscoverable requirements and source-shape bias.
- **Use only the visible self-tests:** under-measures black-box parity and makes test deletion attractive.
- **Use an LLM judge as the correctness oracle:** less reproducible for deterministic command behavior.

### 6. Make rescoring append-only

The original trial record points to immutable stage snapshots and the verifier revision used at execution. An offline rescore reads a snapshot, runs a selected verifier revision, and writes a new linked record; it never rewrites the original outcome, transcript, or artifacts.

This permits verifier fixes without paying for another authenticated agent run while preserving exactly what was known at each evaluation time.

Alternatives considered:

- **Overwrite old scores:** destroys auditability.
- **Rerun the subject after every verifier correction:** changes both the implementation sample and model nondeterminism.

### 7. Record factors and measures, not a verdict

Extend normalized results with peer sections for `product`, `engineering`, and `process`, nested by stage. Deterministic contracts populate product evidence. Trajectory-derived discovery, questions, assumptions, steering, commands, and artifacts populate process evidence. Static inspection and an optional arm-blinded rubric may describe scope control, ownership, duplication, focused checks, and extension locality.

Comparison summaries retain individual repetitions and compute availability and medians for compatible numeric measures. They emit neither weighted totals nor rankings. A one-repetition run is labeled plumbing evidence.

Alternatives considered:

- **Weighted engineering score:** hides the trade-off between correctness, scope, and cost.
- **Raw diff size as scope or rework:** rewards terseness without establishing design quality.
- **Judge labels visible to the reviewer:** can bias qualitative interpretation toward model expectations.

### 8. Interleave through the existing local runner

Change comparison scheduling from arm-major order to deterministic repetition rounds when multiple arms run: repetition one across all arms, then repetition two, and so on. Record the actual order and an optional declared seed. Single-arm runs remain unchanged.

The runner continues to write local Harbor jobs. Deterministic fixture construction, validation, calibration, and rescoring run without authentication; authenticated baseline execution remains a separate developer-invoked command.

Alternatives considered:

- **Randomize without recording:** reduces temporal bias but harms reproducibility.
- **Add a queue or orchestration service:** unnecessary for local serial trials.
- **Move evaluation to CI:** conflicts with local subscription authentication and the intended development cycle.

## Risks / Trade-offs

- **The selected Python files accidentally omit behavior users would consider essential** → Inventory visible commands and self-tests, review the fixture diff, and treat later discoveries as a new fixture revision rather than silently changing an active comparison.
- **Synthetic Codex state is too simple** → Include multiple sessions and model/usage combinations needed to exercise visible report branches, then calibrate against the Python implementation.
- **Effective configuration cannot be perfectly observed inside a host CLI** → Record filesystem inventory, environment allowlist, launch arguments, and hashes; label any unobservable host-default layer explicitly unavailable.
- **Codex model arms differ in unsupported reasoning or orchestration semantics** → Validate factor support before launch and mark unsupported combinations invalid rather than approximating them.
- **The extension result is dominated by a broken first stage** → Preserve both stage outcomes and report extension locality only with its initial-state qualification.
- **Qualitative design measures introduce judge variance** → Keep them arm-blinded, versioned, optional, and separate from deterministic behavior.
- **Interleaving increases elapsed wall time for one arm's full set** → Prefer reduced temporal bias for comparisons; retain a single-arm diagnostic path.
- **Offline rescoring can create multiple apparently conflicting outcomes** → Keep every score append-only with verifier provenance and identify the originally executed versus later rescore records.

## Migration Plan

1. Add and validate the code-only fixture manifest, builder, synthetic state, prompt files, and contamination rules.
2. Add the Codex-only two-stage scenario declaration and vanilla factor validation using the existing isolated preparation and resume paths.
3. Add stage snapshots, effective-configuration inventories, exact digests, and append-only offline rescoring.
4. Build and calibrate the visible-source-linked deterministic verifier.
5. Extend result normalization, engineering/process evidence, comparison interleaving, and non-composite summaries.
6. Run deterministic self-checks and a controller-only two-stage simulation.
7. Present the exact baseline arm matrix and authenticated execution cost before launching subscription-backed trials.

Rollback removes the benchmark-specific fixture, declarations, verifier, and result extensions. Existing Harbor smoke tasks and comparisons remain usable.
