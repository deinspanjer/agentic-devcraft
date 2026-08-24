# Codex Date-filter Calibration

## Why this was run

This inexpensive scenario checks that the engineering benchmark can exercise a
small existing Python CLI, continue the same session with a related extension,
verify required behavior separately from robustness probes, and retain useful
process and resource evidence.

Each arm first added an inclusive `--since YYYY-MM-DD` filter, then added an
inclusive `--until YYYY-MM-DD` filter that could compose with it as a closed
range. The supplied fixture, prompts, contracts, and qualitative anchors are in
the [date-filter benchmark](../benchmarks/date-filter/README.md).

## Outcome

All three one-repetition arms passed all four initial and four extension
contracts. Each inspected the supplied source and tests, changed the same three
product files, updated documentation, and retained focused runnable checks.
Malformed lower and upper dates were rejected in every arm. The unscored
inverted-range probe returned an empty result in every arm.

No subject asked a question, stated an assumption, needed a controller
continuation, or created process scaffolding. Each stage was one interaction
turn. This makes the run useful as plumbing and verifier-calibration evidence,
but it does not exercise collaboration or distinguish behavioral quality.

## Observed measures

### Initial `--since` change

| Arm | Contracts | Input | Cached input | Output | Interaction turns | Assistant updates | Controller continuations | Tool calls | Files |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sol high, direct | 4/4 | 110,109 | 92,160 | 2,862 | 1 | 3 | 0 | 7 | 3 |
| Sol low, direct | 4/4 | 93,786 | 62,976 | 2,540 | 1 | 3 | 0 | 6 | 3 |
| Terra high, direct | 4/4 | 96,815 | 81,152 | 2,950 | 1 | 3 | 0 | 6 | 3 |

### `--until` extension

| Arm | Contracts | Input | Cached input | Output | Interaction turns | Assistant updates | Controller continuations | Tool calls | Files |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sol high, direct | 4/4 | 74,226 | 67,584 | 1,556 | 1 | 1 | 0 | 3 | 3 |
| Sol low, direct | 4/4 | 68,390 | 56,320 | 1,499 | 1 | 1 | 0 | 3 | 3 |
| Terra high, direct | 4/4 | 71,645 | 65,536 | 1,812 | 1 | 1 | 0 | 3 | 3 |

Sol low used the fewest reported tokens in both stages while producing the same
verified behavior. With one repetition per arm and a correctness ceiling, that
is a useful observation about this run, not a stable model recommendation.

Correction, 2026-08-23: an earlier summary called every assistant trajectory
entry a “turn.” Retained controller records establish one interaction turn per
stage and no controller continuations for every arm. This report and the
[machine record](../baselines/date-filter-codex-calibration-v1.json) use the
corrected terms and count visible intermediate assistant updates separately.
