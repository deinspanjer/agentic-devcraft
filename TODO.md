# Future Work

## Evaluation rubric v2

- Define frozen, scenario-specific ideals and acceptable variants before trials.
- Add anchored qualitative judgments for completeness, documentation
  consistency, scope, ownership/locality, behavioral test quality, discovery,
  interaction, and actual orchestration.
- Record uncached input, cache reads and writes when available, output,
  controller, and subagent tokens separately.
- Add a frozen pricing snapshot for standardized API-equivalent cost while
  keeping actual subscription cost explicitly unavailable.
- Calibrate every criterion against compliant alternatives and targeted defects
  before using it for comparisons.

The detailed target rubric is in [docs/EVALUATION.md](docs/EVALUATION.md).

## Baselines

- Replace the misleading “subagents allowed” arm with a directed-orchestrator
  arm whose prompt requires delegation and whose verifier confirms subagent use.
- Add a scenario with enough behavioral and design ambiguity to avoid the
  correctness ceiling encountered by the first port baseline.
- Preserve the original baseline as historical plumbing evidence rather than
  rerunning it under changed factor semantics.

## Proposed skills

- Run repeated efficacy comparisons for `cold-read`, `decision-evolution`, and
  `review-integrity` before promoting them into the released plugin.
- Exercise each candidate alone and alongside supported workflows, including
  Peters Toolkit where its behavior overlaps the proposed enhancement.
- Define a promotion record that links evidence, known limitations, compatible
  hosts/workflows, and the exact promoted source digest.

## Later scenario families

- Competing derivations and canonical-source ownership.
- Discover-before-inventing behavior.
- Neutral context dossiers and sanitized history as explicit context factors.
