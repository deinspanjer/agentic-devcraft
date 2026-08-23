# Evaluation Methodology and Learnings

Agentic Devcraft treats a plausible skill as a hypothesis. Installation checks
show that a host can load it; behavioral comparisons determine whether it helps.
Those are different claims and remain separate in the evidence.

## Evidence artifacts

Evaluation produces two durable views:

- Human reports under `evals/harbor/results/` explain the question, controls,
  outcome, limits, and implications.
- Machine baselines under `evals/harbor/baselines/` retain stable factors,
  provenance, per-trial measures, and availability for future comparison.

Raw Harbor jobs remain ignored because they are large, may contain private
subject-authored text, and are reproducible from the committed harness and
declared inputs. A durable report may cite a raw local run, but must not depend
on that run being present for its main conclusions.

## Experimental principles

1. Start with a genuinely empty control and make context availability an
   explicit factor.
2. Hold fixtures, prompts, verifier contracts, limits, and scheduling constant
   except for the declared factor.
3. Separate setup failure, behavioral correctness, qualitative engineering
   judgment, interaction, and resource use.
4. Prefer behavior-level hidden contracts derived from subject-visible evidence.
5. Retain individual trials and per-measure medians; do not hide tradeoffs behind
   one composite score.
6. Treat one repetition as plumbing evidence. Use repeated interleaved trials
   before making comparative claims.
7. Record unavailable measures as unavailable rather than zero or estimates
   presented as observations.

## What the foundation established

- Subscription-authenticated Codex and Claude can run one-shot and resumed
  sessions in disposable Harbor environments.
- Devcraft Status, Superpowers, GSD, Pocock Skills, OpenSpec, and Spec Kit passed
  setup, discovery, and use probes on both hosts. This is compatibility evidence,
  not efficacy evidence.
- Selective network isolation depends on the Docker backend supporting Harbor's
  required nftables capability. The durable rule is to probe and fail closed;
  historical Docker version troubleshooting is not part of the project method.
- Candidate content can be injected directly for behavioral evaluation while
  canonical marketplace installation is tested separately.

## What the first vanilla baseline established

The code-only Python-to-Rust port baseline proved that the fixture, controller,
continued sessions, black-box verifier, contamination checks, provenance,
repetitions, and reporting work together. All 12 trials passed every behavioral
contract, so the scenario did not distinguish the arms on correctness. Within
that ceiling, Sol at low reasoning with direct execution was the most suitable
configuration for this task as designed: it used the fewest reported tokens and
produced the most localized extension. This is provisional resource-efficiency
evidence for small, well-specified work, not a general model ranking.

That result has important limits:

- It is primarily a plumbing baseline, not evidence that one model configuration
  is generally best or that the tied implementations were equal in quality.
- “Subagents allowed” measured capability availability, not orchestration. No
  agent delegated. Future orchestration arms must explicitly instruct the root
  agent to orchestrate and must verify actual subagent activity.
- The task supplied enough discoverable behavior that no subject needed owner
  clarification. Future interaction evaluation needs frozen owner preferences or
  meaningful ambiguity, not a rubric that rewards asking questions regardless of
  need.
- Output tokens and files touched describe effort and locality but do not grade
  completeness, documentation consistency, or test quality by themselves.
- The run exposed a mixed stage-telemetry boundary; the normalization now removes
  the exact initial trajectory prefix before reporting extension evidence.

See the [human baseline report](../evals/harbor/results/2026-08-22-vanilla-port-codex-baseline.md)
and [machine baseline](../evals/harbor/baselines/vanilla-port-codex-v1.json).

## Rubric framework

This document defines shared evaluation dimensions, not a complete rubric by
itself. Each scenario must supply an evidence-backed rubric before execution:
load-bearing requirements, expected documentation effects, acceptable
implementation shapes, known ambiguities, a frozen owner-answer policy, evidence
sources, and scenario-specific scoring anchors. Hidden criteria may enforce only
behavior discoverable from the supplied materials or explicit owner policy.

A full scenario rubric must identify which criteria determine behavioral
pass/fail, distinguish required behavior from engineering judgment, describe the
evidence available to a judge, provide acceptable alternatives, and calibrate
its anchors against compliant implementations and targeted defects. Rubric
profiles remain unaggregated unless a later decision explicitly justifies
weights.

Deterministic contracts remain pass/fail. Qualitative criteria use an anchored
profile rather than an unexplained overall grade:

- `0` — absent, contradictory, or harmful;
- `1` — materially incomplete;
- `2` — core behavior works but important gaps remain;
- `3` — complete and consistent with only minor shortcomings;
- `4` — matches the frozen ideal or an explicitly acceptable alternative;
- `N/A` — evidence is unavailable or the criterion does not apply.

The shared framework covers:

### Explicit requirement fulfillment

Whether the implementation delivers the requested behavior, preserves explicit
regression contracts, and satisfies compatibility requirements stated or
discoverable in the supplied materials. Missing explicit behavior receives the
strongest negative interpretation and cannot be offset by polish elsewhere.

### Engineering robustness

Error handling, boundary behavior, regression risks outside explicit contracts,
and compatibility holes supported by repository evidence. Robustness is judged
separately so defensive work cannot compensate for missing requirements.
Speculative hardening and unsupported backward-compatibility machinery may be
neutral or negative when they expand scope without an evidence-backed need.

### Documentation completeness and consistency

Whether affected user and developer documentation was identified and updated,
whether unchanged docs remain accurate, and whether new prose contradicts code,
tests, or other canonical documentation.

### Scope and file impact

The number and kind of touched files, necessary versus speculative changes, and
unrequested platform, packaging, dependency, or process scaffolding. Fewer files
is not automatically better; every touched file should have a task-linked reason.

### Design ownership and extension locality

Canonical ownership, duplicated policy or pricing logic, module boundaries, and
how locally the controlled extension can be implemented without rework elsewhere.

### Test quality

Runnable checks that cover observable behavior, invariants, boundaries, and
meaningful failure cases. Tests that merely encode the literal patch or mirror
implementation structure score below tests that would catch plausible regressions.

### Discovery and interaction

Inspection of supplied code, tests, and documentation; explicit assumptions; and
questions or steering required. A question is valuable only when it surfaces a
material ambiguity. No question is required when the frozen materials determine
an acceptable answer.

### Orchestration telemetry and judgment

Always record whether delegation was available, directed, and actually used,
including assigned responsibilities, conflicts, duplication, cost, and latency.
Do not reward orchestration merely for occurring. When a prompt explicitly
requires it, failure is instruction-adherence evidence. Score orchestration
judgment separately only in a scenario designed to test whether autonomous
delegation was appropriate and useful.

### Resource and economic efficiency

Record total input, cached input reads, cache writes when reported, output,
controller, and subagent tokens separately. Derive uncached input only when the
host's metric semantics support it. Report wall time and tool calls alongside a
standardized API-equivalent cost calculated from a frozen model-pricing snapshot.
Actual subscription cost remains unavailable; the proxy exists so materially
more expensive output is visible next to any quality improvement.

## Scenario tiers

Use small calibration scenarios for frequent, inexpensive validation of the
harness, rubric sensitivity, requirement completion, documentation, tests,
scope, robustness, and process cost. Treat them as evidence about small changes,
not as proxies for architecture, prolonged collaboration, or orchestration.

Use representative scenarios such as the Python-to-Rust port less frequently to
evaluate design ownership, extension locality, sustained interaction, and other
behaviors that require enough work to become observable. A result applies only
to the scenario class it exercised.

The first calibration scenario is the
[date-filter microbenchmark](../evals/harbor/benchmarks/date-filter/README.md).

## Interpretation

Do not infer efficacy from installation, a single trial, or a scenario where all
arms hit the rubric ceiling. Compare the full criterion profile, trial variance,
and cost evidence. A future aggregate may be added only after the component
rubrics are calibrated and its weighting has an explicit decision use; until
then, tradeoffs remain visible rather than collapsed into a ranking.
