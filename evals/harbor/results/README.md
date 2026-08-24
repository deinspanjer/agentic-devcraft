# Evaluation Results and Findings

This index is the shortest path from the project's claims to the evidence that
supports them.

## Current findings

- The Harbor harness can run isolated, subscription-authenticated subjects,
  continue sessions, detect contamination, verify behavior, and retain exact
  fixture and prompt provenance.
- Six workflow and skill projects passed setup, discovery, and use probes on
  Claude Code and Codex. This establishes host compatibility, not engineering
  efficacy.
- All 12 Codex vanilla-port trials passed every enforced behavior. Sol at low
  reasoning with direct execution was the most suitable configuration for this
  task as designed: it delivered the same verified behavior with the lowest
  median reported token use in both stages and the most localized extension.
- That configuration finding is provisional. The run did not apply the richer
  qualitative rubric, did not calculate a standardized monetary cost, and did
  not test Terra at low reasoning. It supports a narrow efficiency choice for
  small, well-specified work, not a general model ranking.
- Merely making subagents available did not produce delegation. A future
  orchestration comparison must direct orchestration and verify that it occurred.
- The one-repetition date-filter calibration passed every required contract in
  all three arms and demonstrated a cheap end-to-end benchmark loop. Sol low
  used the fewest reported tokens, but the correctness ceiling and sample size
  make that an observation rather than a model recommendation.

## Evidence map

| Question | Human explanation | Durable evidence |
|---|---|---|
| Can the selected projects be installed, discovered, and used on both hosts? | [Subject smoke matrix](2026-08-21-subject-smoke-matrix.md) | [Subject declarations](../subjects/) |
| What happened in the 12-trial vanilla baseline? | [Baseline report](2026-08-22-vanilla-port-codex-baseline.md) | [Machine baseline](../baselines/vanilla-port-codex-v1.json) |
| What happened in the date-filter calibration? | [Calibration report](2026-08-23-date-filter-codex-calibration.md) | [Machine calibration record](../baselines/date-filter-codex-calibration-v1.json) |
| What exactly was supplied and verified? | [Benchmark fixture](../benchmarks/vanilla-port/README.md) | [Pinned public source](https://github.com/deinspanjer/codex-cost-meter/tree/0b5eb56978c91e1fa1631d9ec84ac3767e8fce79), [manifest](../benchmarks/vanilla-port/manifest.json), and [behavior contracts](../benchmarks/vanilla-port/contracts.json) |
| How should the results be interpreted? | [Evaluation methodology](../../../docs/EVALUATION.md) | [Executed matrix](2026-08-22-vanilla-port-proposed-matrix.md) |

## Reuse and replication

Raw trajectories, snapshots, controller records, and subject workspaces are not
committed because they are large and may contain private subject-authored text.
That prevents independent re-grading of every historical output. The repository
instead commits the harness, declared inputs, prompts, verifier contracts,
digests, per-trial measures, and reports needed to understand the study and
replicate it without treating private raw artifacts as permanent project data.
