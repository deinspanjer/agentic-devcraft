# Executed Codex Vanilla Port v1 Matrix

Status: historical declaration for the completed v1 baseline. Future orchestration comparisons must use a directed-orchestrator factor instead of this matrix's capability-only arm.

## Fixed inputs

- Host: Codex only
- Context: code-only fixture `608c678bb27de1da07011472328cbf2f5a26df7a68308c671fdf5e4ed3440652`
- Initial task: Python-to-Rust report port
- Extension: declared `--prices <path>` JSON contract
- Controller: Codex `gpt-5.6-luna`, medium reasoning
- Container: Codex CLI 0.149.0, Rust 1.88.0, Node 24.19.0
- Provisioned workflows, skills, hooks, plugins, marketplaces, and history: none
- Plumbing: one completed diagnostic repetition
- Baseline: three fresh repetitions per arm; benchmark evidence

## Execution order

| Order | Arm | Subject model | Reasoning | Orchestration |
|---:|---|---|---|---|
| 1 | `sol-high-direct` | `gpt-5.6-sol` | high | direct |
| 2 | `sol-low-direct` | `gpt-5.6-sol` | low | direct |
| 3 | `sol-high-orchestrated` | `gpt-5.6-sol` | high | subagents available, not directed |
| 4 | `terra-high-direct` | `gpt-5.6-terra` | high | direct |

This is repetition-major scheduling. The approved baseline order is A1, B1, C1,
D1, then A2, B2, C2, D2, then A3, B3, C3, D3.

## Supported factors and limits

- Codex 0.149.0 reported stable `multi_agent` support. This enabled the feature but did not instruct or verify delegation.
- Declared reasoning support: Sol and Terra accept low through ultra; Luna accepts low through max. The proposed matrix exercises only the combinations shown above.
- Turn limit: 20 subject responses per stage, at most 40 across the two-stage trial.
- Time limit: 5,400 seconds shared by both stages in one trial.
- Reported subject-output limit: 250,000 tokens per trial, 3,000,000 across the 12-trial baseline.
- Controller bound: at most 38 structured decisions per trial, 456 across the baseline. Controller tokens are not currently reported by the harness.
- Execution is sequential, so the declared wall-clock ceiling is 18 hours before container build and verifier overhead. The successful diagnostic trial took about 17 minutes, suggesting roughly 3.5 hours if that rate holds.

## Authenticated usage and interpretation

Both the subject and controller use the local ChatGPT subscription authentication supplied through `CODEX_AUTH_JSON_PATH`. Harbor does not report an incremental monetary charge for this subscription-backed usage, so dollar cost is unavailable rather than estimated as zero. The runs consume subscription capacity and remain subject to plan limits.

The diagnostic repetition establishes only that fixture isolation, controller
behavior, session continuity, verification, privacy, and factor plumbing work end
to end. The three-repetition baseline reports per-measure medians while retaining
every trial; model outcomes remain separate measures with no composite score or
ranking.
