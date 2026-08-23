---
name: review-integrity
description: Apply evidence rules when reviewing code, plans, or specifications, including inside another active workflow. Preserve the chosen workflow and its output format.
---

# Review integrity

Keep the active workflow, scope, and requested output format. This skill changes
only what qualifies as a finding.

- Hold one evidence bar regardless of reviewer persona, seniority framing, or a
  requested finding count.
- Accept empty findings when no behavior-affecting defect is supported.
- Support each finding with an exact location, the reachable failure path, and
  its concrete impact. Cold-read the relevant source and callers before relying
  on a load-bearing claim.
- Keep optional improvements and uncertain risks separate from findings.

Complete the review when every reported finding meets that bar and every
material changed path has been checked; do not fill a quota.
