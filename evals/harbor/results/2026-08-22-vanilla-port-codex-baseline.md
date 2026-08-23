# Codex Vanilla Python-to-Rust Port Baseline

## Why this was run

The first engineering benchmark needed a clean control before Devcraft or any
other toolkit was introduced. Each subject received only a Python cost meter,
its self-tests, a minimal README, synthetic Codex state, and this task:

The sanitized fixture was built from the public
[Codex Cost Meter source at the pinned revision](https://github.com/deinspanjer/codex-cost-meter/tree/0b5eb56978c91e1fa1631d9ec84ac3767e8fce79).

> Port the existing Python Codex cost meter in this repository to Rust so it can
> be distributed as a standalone application for macOS and eventually Windows.
> Start with a working version of the report functionality.

The same session then received a controlled extension: load model prices from a
user-supplied JSON file while retaining built-in defaults.

## Experimental design

Four Codex configurations ran three times each in fresh repositories, interleaved
by repetition. Fixture, prompts, controller, verifier, limits, network policy,
and code-only context were fixed. No workflow, skill, hook, plugin, marketplace,
personal instruction, or historical project context was supplied.

One arm was originally named `sol-high-orchestrated`. It only enabled Codex's
multi-agent capability; the prompt did not direct delegation and no subject used
a subagent. This report therefore treats it as `subagents available`, not as an
orchestration experiment.

## Behavior covered

The initial verifier covered build and focused checks, JSON parity, descendant
aggregation, model/token/cost aggregation, human-readable output, and visible
missing-rollout failure. The extension verifier covered initial regression
safety, retained built-in prices, valid custom prices, and invalid price files.

The canonical descriptions and subject-visible evidence for all eleven checks
are in [the contract inventory](../benchmarks/vanilla-port/contracts.json).

## Outcome

All 12 trials completed both stages. The initial ports passed 84/84 discoverable
contracts and the extensions passed 48/48. No trial required a material owner
answer, produced a process artifact, or added platform/packaging scaffolding.

This is strong plumbing evidence and limited comparative evidence. Every arm hit
the behavioral-correctness ceiling, so the run does not identify a correctness
winner. Within that ceiling, Sol at low reasoning with direct execution was the
most suitable configuration for this task as designed: it had the lowest median
reported input, cached-input, and output token counts in both stages, and its
extension had the fewest turns and tool calls while changing two files with one
pricing owner.

That is provisional resource-efficiency evidence for small, well-specified work,
not evidence that Sol or low reasoning is generally superior. The qualitative
rubric was not applied, monetary cost was unavailable, and Terra was tested only
at high reasoning, so model and reasoning effects cannot be separated.

## Median observed measures

### Initial port

| Arm | Contracts | Input | Cached input | Output | Turns | Tools |
|---|---:|---:|---:|---:|---:|---:|
| Sol high, direct | 7/7 | 872,116 | 787,456 | 24,672 | 21 | 20 |
| Sol low, direct | 7/7 | 844,954 | 781,056 | 14,744 | 23 | 22 |
| Sol high, subagents available | 7/7 | 1,047,101 | 931,328 | 23,191 | 22 | 21 |
| Terra high, direct | 7/7 | 1,079,271 | 989,952 | 17,414 | 25 | 24 |

### Pricing-file extension

| Arm | Contracts | Input | Cached input | Output | Turns | Tools | Files | Pricing owners |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Sol high, direct | 4/4 | 1,062,542 | 1,035,008 | 10,386 | 14 | 13 | 4 | 2 |
| Sol low, direct | 4/4 | 563,343 | 546,560 | 5,605 | 11 | 10 | 2 | 1 |
| Sol high, subagents available | 4/4 | 984,472 | 956,928 | 10,535 | 14 | 13 | 4 | 2 |
| Terra high, direct | 4/4 | 1,315,003 | 1,279,488 | 10,145 | 18 | 17 | 3 | 1 |

These measures describe the runs; they do not grade documentation completeness,
test quality, architectural ownership, or overall value. In particular, fewer
files is not automatically better.

## What was learned

- The fixture, controller, continued-session boundary, verifier, contamination
  checks, repeated scheduling, provenance, and reporting operate end to end.
- Sol low with direct execution was the most resource-efficient suitable arm for
  this task under the measures available, without sacrificing verified behavior.
- The scenario needs a richer rubric or a more discriminating task before model
  quality can be compared.
- Making subagents available caused no subject to delegate and made no observed
  behavioral difference. Orchestration must be an explicit instruction with
  observed delegation, not a feature flag.
- Interaction cannot be evaluated merely by counting questions. A future
  scenario needs meaningful ambiguity and a frozen owner-answer policy.
- Token and file counts must be interpreted beside completeness, documentation,
  tests, and standardized cost.

The target rubric and implications are maintained in
[the evaluation methodology](../../../docs/EVALUATION.md).

## Availability and correction

Stage duration, controller tokens, actual subscription cost, and a standardized
cost proxy were unavailable. They are not treated as zero.

The executed normalizer's extension trajectory included the initial prefix even
though its token metrics were stage-local. The published machine baseline removes
that exact prefix for turns, tool calls, inspection, questions, and assumptions.
Future normalization performs the same removal and fails closed when the two
trajectories are not an exact continuation.

## Durable evidence

The [machine baseline](../baselines/vanilla-port-codex-v1.json) contains every
trial, factor, median, per-stage measure, availability marker, and fixture/prompt
digest needed for later comparisons. Raw Harbor jobs remain ignored local
artifacts because they may contain private subject-authored text and add
substantial volume. The committed fixture declarations, prompts, contracts,
harness, provenance, and reports preserve enough detail to replicate the study;
they do not support independent re-grading of every historical subject output.
