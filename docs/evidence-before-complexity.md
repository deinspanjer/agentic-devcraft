# Lessons from the retired complexity experiments

The November 2026 experiments tried to measure whether a short instruction to
check evidence before adding complexity improved agent decisions. The approach
used paired control/treatment runs in isolated Harbor workspaces, frozen owner
replies, independent outcome checks, and limited human review. Scenarios covered
account sync, a book-club handout, and a JSONB query repair.

The work did not establish a practically useful, general improvement. The sync
tasks had ambiguous requirements and a defective uncertainty case. The handout
tasks largely produced acceptable behavior in both conditions. A small JSONB
comparison changed scope choices consistently, but both choices passed correctness
checks and preserving compatibility had a defensible rationale. A scope
clarification also produced the simpler repair without the candidate instruction.
These observations neither establish efficacy nor prove the instruction useless.

## What to avoid repeating

- Calibrate the agent decision, not just the broken program. A reproducible SQL
  timeout does not demonstrate that the agent will make the suspected mistake.
- State the job's required behavior before judging extra complexity. An inherited
  test is not automatically an owner requirement, and more code is not
  automatically an error.
- Do not use correctness ties as evidence of a quality or efficiency improvement.
  A different scope choice alone does not establish practical benefit.
- Check that a small scenario exposes the target behavior before building a
  repetition schedule, reporting pipeline, or human-review workflow.
- Keep human review proportional. Presentation revisions, blinded packets, and
  repeated judging consumed substantial effort without resolving the central
  effectiveness question.
- Prefer an ordinary requirement clarification when it settles the actual job.
  More process instructions are not necessarily the missing ingredient.

The owner chose to delete the experiment-specific runners, fixtures, verifiers,
tests, baselines, detailed reports, and unexecuted proposals rather than maintain
or privately archive them. Their tests protected retired experiment machinery,
not supported product behavior. This note retains the methodological lessons,
not an auditable study or reproducible benchmark. The candidate instruction
remains unreleased; no follow-up experiment is scheduled by this note.
