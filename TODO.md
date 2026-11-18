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

## Ask Devcraft

`ask-devcraft` was promoted by maintainer approval on 2026-11-18; the evidence and
its limits are in [DEVELOPERS.md](DEVELOPERS.md#promotion-record).

- Evaluate `ask-devcraft` on native hosts: ranking installed
  skills ahead of uninstalled ones, naming uninstalled skills only from
  collections the user already has (a collection, not the marketplace that lists
  it), asking before introducing another collection, delegating to an installed
  router and recommending a missing one, same-name skills from different
  sources, an installed copy older than the curated record, uncurated installed
  skills, skills that state a dependence on another host, complaints about agent
  behaviour, including the parts where no curated skill fits, an
  unavailable source during a live check, and consent before expanded search or
  execution. Add failure-mode fixtures/comparison declarations and retain
  native-host loading and behavioral evidence; link, index, and size checks on
  the Markdown do not establish routing effectiveness.
- Re-run the `ask-devcraft` probes in
  [evals/ask-devcraft/](evals/ask-devcraft/README.md) only when a host release
  or a launcher/worker change gives reason to, and audit the transcripts before
  keeping the result files ([DEVELOPERS.md](DEVELOPERS.md#promotion-record)
  holds the 2026-11-18 audit and headless re-probe). Not yet observed, and worth
  a look on such a re-run: the final answer's unlabelled last line (two
  launchers altered a labelled one), the Claude Code `model` pass-through added
  to `claude.md`, and Cursor with `cursor.md` in place. Unobserved points the
  harness files mark "(docs)" or "(unobserved)" stay labelled there until a
  user or probe hits them.
- Add fixtures for the delegated `ask-devcraft` flow: a pointer-only request
  whose thread already holds the evidence, a consent flow continued in the same
  worker and one re-dispatched from the returned state, an `Ask` that must not
  name the unfamiliar skill, a clarifying `question` reply, a failed or denied
  delegation, and a reply whose cited lines are checked against the files.
- Measure what `ask-devcraft` loads per invocation against its disclosure
  budgets (about 40 lines for the launcher, about 150 lines for `worker.md`,
  about 11 KB for the index, about 40 lines for a worker's reply), including
  whether a development task ever opens a `far/` file. Measure the bytes entering
  the main session per invocation on native hosts, delegated and inline; the
  OpenCode figures are in
  [DEVELOPERS.md](DEVELOPERS.md#launcher-worker-and-harness-files).
- `ask-devcraft` has no curated skill to recommend for several complaints about
  agent behaviour: cutting ceremony, file backups where Git is the backup, and
  narrating instead of acting. Two earlier gaps are filled from
  `references/community.md`: redundant tests across a suite (`auditing-tests`,
  `audit-tests`) and a preventive drift check (`intent-framed-agent`); neither
  has been run here, so exercise them before relying on the records. Drift
  prevention is `intent-framed-agent`; `decision-evolution` does not cover drift:
  it tracks a decision whose basis changed and has no check of current work
  against the request. The file-backups gap stays open, with no skill or
  instruction planned. The other gaps map to unreleased candidates:
  `evidence-before-complexity` (over-engineering, and cutting ceremony through
  its rule to match the process to the size of the work) and `review-integrity`
  and `cold-read` (findings nobody validated). Use the complaints as scenarios
  when evaluating those candidates.

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
