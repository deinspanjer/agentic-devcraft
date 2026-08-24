# Codex Cost Meter report experiment candidates

Date: 2026-08-24

## Bottom line

All six enhancements are worth preserving, but they make a stronger evaluation set when combined into four scenarios. The combinations preserve causal sequences that an isolated feature prompt would erase: project reporting exposed the need for a cache, while corpus reporting and date grouping were designed as one reporting surface.

| Priority | Candidate | Enhancements covered | Primary capability under test |
| --- | --- | --- | --- |
| 1 | Legacy fork replay correction | Forked-thread token correction | Forensic bug diagnosis and conservative accounting correction |
| 2 | Fast-tier pricing | Fast-mode detection | Evidence-calibrated inference under incomplete historical data |
| 3 | Corpus date reports | All-level report; date filtering and grouping | Temporal semantics, aggregation, and fail-open performance pruning |
| 4 | Project reporting, then caching | Project-level report; cache introduction | Ambiguous domain discovery followed by evidence-driven performance redesign |

This ordering reflects experimental distinctiveness, not product importance. The fork and Fast cases force the agent to revise an initially tempting accounting model. The date case is the strongest specification exercise. The project/cache case is broader and more expensive, but uniquely tests whether the agent responds to problems revealed by realistic use rather than prematurely designing a cache.

## Evidence method and limitations

This inventory uses only local primary evidence: immutable Git commits and diffs in `/Users/dre/src/codex-cost-meter`, preserved OpenSpec artifacts in those commits, and Codex rollout JSONL/session records. Contextify was used only to locate sessions; its index reported that it was catching up, so material claims were corroborated against Git or raw rollout artifacts.

Project and cache work predated this repository's preserved OpenSpec workflow, so no OpenSpec artifact exists for their initial design. Their requirement history comes from raw sessions and commit history. The date-report session was located through Contextify entries, but its raw rollout path was not recovered before the research stop; direct owner refinements below are therefore cited by entry ID, while the complete final contract is cited to preserved OpenSpec. This is the only material session-provenance gap.

## Candidate 1: legacy fork replay correction

### Suggested experiment

Give the agent the historical `ccusage` context-copy TODO and access to a Codex source checkout plus a rollout corpus. Ask it to determine whether forked rollouts double count tokens and propose and implement only a correction supported by forensic evidence.

### Explicit initial requirements

The owner asked the agent to:

- investigate the TODO's reported context-copy problem;
- use subagents to inspect `~/src/codex` for how explicit forks work now or worked historically;
- determine how copied context affects what is actually submitted to the API, rather than equating stored records with billing;
- find evidence in the owner's rollouts; and
- report findings and suggested solutions only after understanding Codex behavior.

Evidence: Codex thread `01a031d8-87fb-77b2-97e8-22d44712007f`, raw artifact `/Users/dre/.codex/archived_sessions/rollout-2026-08-23T23-37-49-01a031d8-87fb-77b2-97e8-22d44712007f.jsonl`, initial user message.

### Hidden or discovered requirements

Investigation established the actual invariant and narrowed the safe correction:

- Legacy explicit forks physically copy a leading prefix of the parent's historical `TokenCount` records. Those copies are not new API requests, but the inherited prompt tokens on the child's first genuine request remain billable.
- Eligibility must require nonempty `forked_from_id`, explicit-fork lineage/history behavior, a readable parent, and matching copied-history structure. A missing history-mode field was an observed legacy default, not evidence of a subagent fork.
- Compare the exact leading parent/child usage tuples across every token component while ignoring rewritten timestamps. Stop suppression at the first mismatch. A concurrent-parent race may leave one additional parent record absent from the snapshot.
- Suppressed records must still advance the child's cumulative baseline; otherwise the first genuine child request is calculated incorrectly.
- Missing parents, pagination, non-forks, and unmatched records must retain all usage. Timing bursts, fuzzy signatures, suffix searches, and session-agnostic deduplication were rejected because they could undercount legitimate requests.
- Parent-dependent adjustment invalidates the ordinary per-file analysis cache only for a child with a nonzero matched prefix. The design deliberately avoided adding parent revision state to the cache schema.
- Cold targeted discovery must inspect canonical rollout metadata because the Codex SQLite projection lacks `forked_from_id`. Filesystem recovery remains required.
- The deterministic correction is silent: no approximation marker or user-facing switch. Corpus evidence in repository artifacts must be sanitized.

Evidence: `openspec/changes/suppress-legacy-fork-usage-replay/{proposal.md,design.md,specs/fork-replay-accounting/spec.md,tasks.md}` as preserved by Git commit `86ca301` (merged as `aad4ae3`; conflict resolution `2e45872`), plus the raw session above.

### What this tests

This is the highest-value candidate. It distinguishes filesystem representation from API billing, rewards source-and-corpus triangulation, and penalizes plausible but unsafe heuristics. It also tests whether an agent can modify an accounting algorithm and its cache/discovery boundary without broadening the fix.

## Candidate 2: Fast-tier pricing

### Suggested experiment

Start with the request to handle Fast-mode pricing. Supply mixed Standard/Fast/missing-tier rollouts, repository history, and public-release evidence captured in the original task. Evaluate whether the agent produces an explicit classification matrix instead of treating all missing tier data as either definitely Standard or unknowable.

### Explicit initial requirements

- Explore and implement Fast-mode price handling through OpenSpec.
- Run the tool against mixed Fast/Standard threads and projects and show real output.
- Break model rows down by service tier and mark Fast with the Codex lightning glyph.
- Explain the pricing cutoff and missing attribution, including whether historical missing values can be proven to predate Fast.

Evidence: Codex thread `01a02b8e-5dad-7fe1-86c3-e5ce39442af8`, raw artifact `/Users/dre/.codex/archived_sessions/rollout-2026-08-22T18-19-05-01a02b8e-5dad-7fe1-86c3-e5ce39442af8.jsonl`, user messages beginning 2026-08-22T22:19Z.

### Hidden or discovered requirements

The first implementation treated missing attribution too cautiously. Owner grilling and release/source investigation established a best-effort historical contract:

- Explicit `standard`/`default`, `priority`/`fast`, and unsupported explicit tiers win. Unsupported explicit tiers remain unpriced rather than silently becoming Standard.
- Missing tier is estimated as Standard, but the report distinguishes definite pre-public Standard from assumed Standard after Fast became publicly possible.
- Creator version and actual usage timestamp are independent evidence dimensions. Old creators can have later usage.
- The first public prerelease boundary is `0.108.0-alpha.2`; Fast premium pricing applies only when an explicit Fast signal is possible at or after stable `0.144.0`, published `2026-07-09T16:47:12Z`. A July 30 name change is not the launch boundary.
- Historical missing-tier observations from the March prerelease onward are assumed Standard, not unpriced. Before first public availability they are definite Standard. Matrix gaps must be called out rather than hidden.
- Cost classification uses event model, timestamp, tier, and gross input. At 272,001 input tokens the long-context multiplier applies to the entire request; 272,000 does not cross the boundary.
- Reports describe an applied-tier API-list estimate, not proven served or billed tier; Fast can downgrade.
- Model rows nest Standard, assumed Standard, Fast, and unavailable cost classes. Turns and durations remain model-level because a turn can contain multiple tier events.
- Changing event facts requires an analysis-cache version bump, not a migration shim. Repository documentation must not leak private home paths.

Evidence: final OpenSpec `openspec/changes/add-fast-mode-pricing/`; Git commit `6f52f5d` (merged as `3bed427`); raw session above, especially the owner's requested classification matrix on 2026-08-23.

### What this tests

This scenario tests uncertainty calibration, chronological state modeling, pricing-boundary correctness, and willingness to revise blanket uncertainty after the owner demands a useful estimate. It is especially good at detecting agents that fabricate certainty or collapse “missing,” “Standard,” and “Fast” into one price.

## Candidate 3: corpus date reports

### Suggested experiment

Ask for an all-rollout report with date filters and date grouping. After the first implementation, add the original steering: filter candidate files by metadata bounds, rerun a fixed range grouped only by date, compare with `ccusage` daily JSON, and explain semantic differences.

### Explicit initial requirements

- Add `report --all` covering every discovered rollout exactly once, across project and rollout types; reject conflicts with an explicit thread or `--project`.
- Add inclusive `--since` and `--through` local-calendar dates, defaulting to the host OS timezone. Reject malformed or inverted ranges.
- Support exactly one grouping period—day, Monday-based week, or month—and optionally one additional rollout-type or model dimension while retaining an overall aggregate.
- Apply filtering and grouping consistently to project and corpus reports.
- When `--since` is present, prune rollouts whose metadata `updated` value is before the boundary. When `--through` is present, prune those created on or after the next local midnight.
- For the acceptance run, group the same range by date only, with no rollout/model dimension, then compare its JSON to `ccusage` daily JSON and explain differences.

Evidence: `openspec/changes/archive/2026-08-23-add-corpus-date-reports/` at Git commit `3b4b661` (implementation commit `1f4cded`); Contextify owner-entry IDs `34e23f02` and `3d746273` for the post-implementation refinement and comparison request. The raw session-path gap is noted above.

### Hidden or discovered requirements

- Date filtering has two clocks: usage/cost uses each event timestamp, while turns/duration are attributed wholly to the turn start. Untimestamped records are excluded and make the range visibly incomplete; lifetime output remains unchanged.
- DST must be handled by converting local calendar boundaries, not subtracting fixed 24-hour intervals.
- Metadata bounds are fail-open pruning hints, not inventory truth: missing or unusable metadata retains the candidate. Filesystem fallback must recover projection lag/unindexed JSONLs.
- Sparse buckets are the default. `--include-empty` requires both range bounds and may synthesize only time buckets, never fake model/type values.
- Streaming cached timestamped records avoids materializing an entire corpus. The new timestamp facts require an analysis-cache version bump.
- Exact-thread date filtering, presets, a timezone flag, multiple simultaneous time groupings, and model/type filters were explicitly left out.
- The design accepted the semantic consequence that a turn crossing midnight belongs entirely to its start date; parity with `ccusage` is a comparison to explain, not an assumption to copy.

Evidence: archived OpenSpec proposal, design, delta spec, and tasks at commit `3b4b661`; implementation diff and tests in `1f4cded`.

### What this tests

This is a strong specification and data-semantics benchmark: inclusive calendar ranges, DST, multi-clock attribution, empty-bucket rules, cache evolution, and performance pruning all interact. The `ccusage` comparison also tests whether the agent explains metric-definition differences instead of forcing false parity.

## Candidate 4: project reporting, then caching

### Suggested experiment

Use two stages. First ask for lifetime project reporting and exercise it against nested, Desktop-created, CLI-only, and projectless threads. Then expose the real large-project runtime and exact-report regression and ask for a grilled cache design. This preserves why the cache exists.

### Explicit initial requirements

Project stage:

- Apply the existing thread report to a selected project or working directory. Defer day/week/month views; the initial feature is lifetime only.
- Keep one `report [THREAD_ID]` command and add optional `--project [NAME_OR_PATH]`: thread plus project validates membership; a thread alone derives its owner; neither defaults from the current workspace.
- Resolve Desktop Project membership even when Codex creates a different worktree CWD. Writable related directories do not change ownership, and explicitly projectless app sessions exist.
- Prefer Desktop project metadata/name, then paths. CLI sessions without project metadata must remain reportable.
- Preserve existing incomplete/unpriced semantics and counts rather than presenting false completeness.

Cache stage—the exact initial request is preserved verbatim in the session:

- Record calculated rollout data in SQLite with an update watermark so unchanged rollouts return without reprocessing, unless a refresh argument is passed.
- Investigate whether adding tables to Codex's existing session database is safe before creating a separate database.
- Grill the design, document settled domain terms, implement it, and determine when the observed full-corpus work was introduced.

Evidence: project thread `01a00305-385c-7220-a194-9c48e3a0cfde`, raw artifact `/Users/dre/.codex/archived_sessions/rollout-2026-08-14T21-24-29-01a00305-385c-7220-a194-9c48e3a0cfde.jsonl`; cache thread `01a024b0-f80b-7cc3-9e33-51819c86d8df`, raw artifact `/Users/dre/.codex/archived_sessions/rollout-2026-08-21T10-19-33-01a024b0-f80b-7cc3-9e33-51819c86d8df.jsonl`, initial user message at 2026-08-21T14:19:36Z.

### Hidden or discovered requirements

Project investigation and pressure testing added:

- Name resolution allows fuzzy local-project matches, then historical CWD matches, but must fail clearly on zero or multiple high-confidence candidates. A nested project in a monorepo must not be swallowed by a parent path.
- Thread plus `--project` can roll up a projectless CLI thread using its initial CWD and related descendants; CWD is an internal resolution input, not a third user-facing selector.
- Real project runs revealed minute-scale execution and required progress reporting. The project report had to preserve exact thread-report behavior after an early regression.
- Human output needed compact large-token values, separate incomplete-root and incomplete-turn language, an explanation for the lower-bound `+`, per-model durations, and humanized day/hour/minute/second duration.

Cache grilling and source investigation added:

- Do not write into Codex's `state_5.sqlite`: Codex owns, migrates, and can split it, and provides no third-party schema contract. Use a private app-owned `$CODEX_HOME/codex-cost-meter.sqlite` “Rollout Analysis Cache.”
- The cache is disposable and never authoritative. Cache parsed rollout facts only; pricing and aggregation remain live.
- The owner's proposed Codex `updated_at_ms` watermark is itself derived from file mtime and the SQLite projection can lag or fail. Freshness therefore uses direct mtime plus byte length.
- The actual regression was architectural: exact reports opened roughly 4,467 rollouts before selecting a workset. Selection must happen before analysis, with a separate targeted-discovery correction; the cache stores only selected roots and descendants.
- A warm hit performs metadata checks but does not reopen/reparse unchanged JSONL. `--refresh` refreshes only the selected workset.
- SQLite errors warn once and fail open to uncached rollouts for that command. Filesystem discovery recovers projection lag. Discovery and analysis versions provide semantic invalidation.
- First creation is visible; a cache doctor was deferred to TODO. A Windows lint failure revealed a Unix-only test helper and required a platform gate.
- The isolated benchmark improved from about 0.63 seconds cold to 0.04 seconds warm on an 11.1 MB tree; refresh was about 0.07 seconds.

Evidence: project release squash `b90f05a` and component commits `18715ce`, `53048b8`, `048df85`, `de5eeb8`, `c481a3d`, `2ee85de`, `fa207f2`; cache commit `5908b25` (merged as `7923083`), targeted-discovery commit `3c6574e`, and raw sessions above. No preserved OpenSpec exists for these pre-OpenSpec changes.

### What this tests

The staged case tests product/domain ambiguity, state-store reverse engineering, realistic corpus testing, performance diagnosis, cache trust boundaries, invalidation, fail-open behavior, and cross-platform closeout. Keeping the stages together reveals whether the agent learns from observed performance rather than adding speculative infrastructure in advance.

## Recommended use

If the experiment budget supports four scenarios, retain all four. For a smaller suite, retain legacy fork replay, Fast-tier pricing, and corpus date reports. Add the staged project/cache case when evaluating long-horizon agents, because much of its value lies in steering, real-corpus pressure testing, and follow-on redesign rather than a single implementation pass.

The benchmark prompts should expose only the explicit initial requirements at first. Hidden requirements should become controller steering, discoverable source facts, or acceptance checks. Supplying the hidden list up front would turn the most valuable reasoning work into ordinary implementation.

## Session-search provenance

Contextify Total Recall was queried with skill fingerprint `d06c6623` and CLI
version `1.7.7`. Its index was catching up, so recent results were treated as
provisional and corroborated against Git or raw rollouts where available. Exact
search-result counts were not retained and are therefore unavailable.

The strongest session anchors were owner entries `34e23f02` (corpus/date report
requirements), `6cb76888` (the cache is disposable, not authoritative), and
`542fffd7` (warm-hit and fail-open cache behavior). Entry `3d746273` was a
truncated duplicate of the corpus/date-report discussion, not independent
evidence.
