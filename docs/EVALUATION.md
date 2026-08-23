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
contract, so the scenario did not distinguish the arms on correctness.

That result has important limits:

- It is a plumbing baseline, not evidence that one model configuration is best.
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

## Target rubric

Each scenario must define an evidence-backed ideal before execution: load-bearing
requirements, expected documentation effects, acceptable implementation shapes,
known ambiguities, and a frozen owner-answer policy. Hidden criteria may enforce
only behavior discoverable from the supplied materials or explicit owner policy.

Deterministic contracts remain pass/fail. Qualitative criteria use an anchored
profile rather than an unexplained overall grade:

- `0` — absent, contradictory, or harmful;
- `1` — materially incomplete;
- `2` — core behavior works but important gaps remain;
- `3` — complete and consistent with only minor shortcomings;
- `4` — matches the frozen ideal or an explicitly acceptable alternative;
- `N/A` — evidence is unavailable or the criterion does not apply.

The profile covers:

### Behavioral completeness

Required behavior, error handling, compatibility, and regression safety. Omitted
behavior and unsupported additions remain visible separately.

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

### Orchestration fidelity

Whether the arm was merely capable of delegation or was directed to orchestrate,
whether subagents were actually used, what responsibilities they received, and
whether their work improved coverage without conflict or redundant effort.

### Resource and economic efficiency

Record total input, cached input reads, cache writes when reported, output,
controller, and subagent tokens separately. Derive uncached input only when the
host's metric semantics support it. Report wall time and tool calls alongside a
standardized API-equivalent cost calculated from a frozen model-pricing snapshot.
Actual subscription cost remains unavailable; the proxy exists so materially
more expensive output is visible next to any quality improvement.

## Interpretation

Do not infer efficacy from installation, a single trial, or a scenario where all
arms hit the rubric ceiling. Compare the full criterion profile, trial variance,
and cost evidence. A future aggregate may be added only after the component
rubrics are calibrated and its weighting has an explicit decision use; until
then, tradeoffs remain visible rather than collapsed into a ranking.
