# Future Work

## Rubric calibration

- Calibrate the date-filter scenario's anchored qualitative criteria against
  compliant alternatives and targeted defects before using judge output for
  comparisons.
- Keep explicit requirement fulfillment separate from engineering robustness so
  defensive polish cannot offset omitted requested behavior.
- Record uncached input, cache reads and writes when available, output,
  controller, and subagent tokens separately.
- Add a frozen pricing snapshot for standardized API-equivalent cost while
  keeping actual subscription cost explicitly unavailable.
- Add arm-blinded judge records that cite retained evidence for each score.

The detailed target rubric is in [docs/EVALUATION.md](docs/EVALUATION.md).

## Baselines

- Run one date-filter repetition per arm as a plumbing check, then review the
  declared three-repetition schedule before authenticated calibration trials.
- Add a directed-orchestrator arm only to a representative scenario where
  delegation is justified; verify actual use and evaluate its consequences.
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
