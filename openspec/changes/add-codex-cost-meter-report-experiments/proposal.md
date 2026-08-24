## Why

The first engineering benchmarks reached a correctness ceiling on small,
well-specified work. Recent Codex Cost Meter report enhancements provide four
source-backed scenarios with richer diagnosis, uncertainty, temporal semantics,
domain discovery, and design-evolution behavior worth preserving for future
evaluation.

The candidate inventory already separates initial owner requirements from the
requirements discovered through grilling, source investigation, corpus testing,
and implementation. Capturing the intended benchmark work in OpenSpec keeps it
discoverable without prematurely fixing fixture, verifier, or matrix designs.

## What Changes

- Add future representative benchmark scenarios for legacy fork replay
  correction, Fast-tier pricing, corpus date reports, and staged project
  reporting followed by caching.
- Use the explicit initial requirements from the
  [source-backed candidate inventory](../../../evals/harbor/results/2026-08-24-codex-cost-meter-report-experiment-candidates.md)
  as subject-visible starting instructions.
- Preserve hidden and discovered requirements as controlled steering,
  discoverable fixture evidence, robustness probes, or behavioral contracts;
  do not expose them all in the initial prompt or enforce undiscoverable facts.
- Reuse the existing Harbor engineering-benchmark machinery and keep each
  scenario's evidence, interpretation limits, and experimental factors explicit.
- Defer the capability delta, design, tasks, fixture selection, verifier
  contracts, matrices, and authenticated execution until a scenario is selected
  for implementation.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `engineering-work-benchmark`: Would add source-backed representative scenarios
  derived from completed Codex Cost Meter report work.

## Impact

- Future work would extend `evals/harbor/benchmarks/`, scenario registration,
  deterministic verifiers, and benchmark documentation.
- Source construction may read selected Codex Cost Meter commits, OpenSpec
  artifacts, and sanitized rollout evidence, while subject workspaces must remain
  isolated from private history and undeclared context.
- This proposal alone adds no runnable scenario, specification, design, task
  plan, verifier, matrix, authenticated trial, or production behavior.
