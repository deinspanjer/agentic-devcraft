## Why

The current Harbor smoke tests establish agent launch and isolation, but they do not yet provide a trustworthy baseline for how models perform representative engineering work. A code-only Python-to-Rust port gives the project a discoverable, behaviorally verifiable scenario before model, orchestration, context, or toolkit effects are compared.

## What Changes

- Add a reproducible two-stage engineering benchmark: first port the supplied Python report functionality to Rust, then add user-supplied model pricing while preserving built-in defaults.
- Build a deliberately code-only fixture containing the Python implementation, its self-tests, a minimal README, and synthetic Codex state, while excluding prior conversations, Rust designs or implementations, architecture-heavy instructions, and workflow/toolkit influence.
- Establish genuinely empty vanilla Codex arms whose declared experimental factors are model, reasoning level, and subagent availability; the host remains Codex and context availability remains code-only for this change. This v1 factor enables multi-agent support but does not direct or prove delegation.
- Add deterministic behavior-oriented verification, verifier calibration, per-trial contamination detection, effective configuration and content digests, retained trajectories and artifacts, offline rescoring, and interleaved repetitions where practical.
- Report initial-port and extension results separately across correctness, discovery, scope control, design locality, runnable checks, questions, assumptions, steering, resource use, and process artifacts without a composite score or ranking.
- Defer Claude, toolkit comparisons, neutral context dossiers, sanitized raw-history replay, canonical-source ownership, and discover-before-inventing scenarios until the vanilla Codex baseline is proven.
- Defer directed orchestration and its observed-delegation contract to a follow-up matrix rather than relabeling the completed capability-only arm.

## Capabilities

### New Capabilities

- `engineering-work-benchmark`: Defines reproducible vanilla engineering scenarios, controlled factors, isolated execution, staged behavioral verification, contamination evidence, offline rescoring, and non-composite comparison reporting.

### Modified Capabilities

None.

## Impact

- Extends the local Harbor evaluation fixture, runner, result, verifier, and comparison machinery under `evals/harbor/`.
- Reads selected source material from the local Codex Cost Meter repository only while constructing the sanitized fixture; benchmark trials receive no access to that repository or its history.
- Produces local generated fixtures, trial jobs, trajectories, workspaces, and reports; authenticated benchmark execution remains an explicit later apply-phase action.
- Does not modify Agentic Devcraft marketplaces or production skills and does not add CI or GitHub Actions for Harbor evaluations.
