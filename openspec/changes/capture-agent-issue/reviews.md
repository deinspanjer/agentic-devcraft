# Proposal reviews

Reviewed on 2026-11-05. The initial reviews below were followed by revisions and a later side-chat pressure test, recorded separately. No skill implementation was requested or performed as part of these planning/review workflows.

## Astra High

Independent read-only subagent using `gpt-6-astra` with high reasoning effort. Read the four planning artifacts and returned:

> No. I found no material correctness, risk, feasibility, or scope issue requiring a design change.

## Claude

Requested through codex-mcp-bridge from the verified session titled **Opus 5.5 editorial review for experiment**. Bridge delivery reached `reply_received`.

Claude returned three material findings:

1. **Worker handoffs were underspecified.** Clarification and optional late parent self-assessment depended on a worker waiting for user/parent input without a defined mechanism. Accepted: define compact result states, parent-mediated clarification and resume/relaunch, and an optional pre-launch self-assessment sidecar read after first-pass reviewer findings. No worker pause is required, and prompt ordering is not claimed as enforceable blinding.
2. **Authorship and human-turn counting needed explicit provenance.** Claude user-role records also include peer requests, metadata, compaction summaries, and tool results. Accepted and independently checked against the named session's record types: human and peer origin fields coexist with generated user records. Revised packet attribution, human/peer counts, unknown-origin handling, and synthetic verification tasks.
3. **Cross-project default saves need a normal approval route.** The central checkout may be outside a caller's writable roots. Accepted with scope qualification: this depends on the host's actual writable roots and approval capability. Specify native approval first and a compact parent handoff using a temporary sanitized draft if the worker cannot request approval. No packet text needs to enter parent context. Add cross-project checks on both harnesses, including approval refusal and non-overwrite behavior.

Claude additionally requested verification that Codex exposes a trustworthy subject-session identity/locator. That route is now explicit in the integration task; missing identity produces locator clarification instead of guessing among sessions.

## Verification after corrections

- `openspec validate capture-agent-issue --strict`: passed.
- `git diff --check`: passed.
- All four required planning artifacts exist; implementation task checkboxes remain open.

## Follow-up: temporary output and recognizable names

The user replaced the checkout-based default with a host-temp directory containing recognizable project and subject-session names, a frozen UTC capture-start date/hour/minute, and a unique suffix. The user clarified that output names must not be de-identified or slugified; only filesystem-required changes are intended. Payload privacy is separate: retain the original de-identification default unless the user requests full details or specific exceptions, subject to enforced policy.

The four planning artifacts now reflect that direction. Claude's follow-up found no material remaining defect in the temporary-output approach. Its suggestion to reconfirm temporary retention was not adopted as another approval gate: the user already explicitly chose temporary storage, and cleanup semantics are documented.

## Follow-up: native side-chat entrypoint (potential change only)

The user proposed documenting Codex `/side $capture-agent-issue <issue>` and Claude `/btw /capture-agent-issue <issue>`, with direct capture in an already isolated session and delegation only as fallback. This option has not been adopted into the behavior contract or implementation tasks.

### Claude assessment

Claude verified the user's Desktop side/fork session had normal tools, a separate identity/title, copied parent history, and extra fork-boundary records. Its installed CLI inspection still found a tool-less terminal `/btw` path plus a separate tool-capable fork path. These client differences explain why the terminal documentation does not establish Desktop behavior.

Its material concerns were:

1. **Original subject versus collector identity and cutoff.** A side/fork session's own title, age, bytes, turns, and tools are not the original session's measurements. Use original subject records up to the source fork boundary; inherited child records and synthetic boundary events must not be misclassified as parent behavior.
2. **Fresh-worker independence versus context inheritance.** Claude recommends always retaining the fresh worker and treating side chat as an optional launcher location. This is a recommendation requiring judgment, not an established requirement from the original user: the user asked for separate accounts and self-reflection, not formal blinded judging. An inherited-context reviewer needs honest labeling; whether another worker is worth its handoff is a design trade-off.
3. **Exact nested skill command support remains unverified.** Tool access alone does not prove that the inner explicit-only skill is expanded. Document the exact command only after a client-specific harmless smoke check establishes skill loading and the intended execution path.

The parent independently confirmed tool-capable bridge communication with the user's fork and 230 shared user/assistant UUIDs bearing the original parent session ID. This establishes inherited records, not exact nested slash-skill resolution or universal client behavior.

### Stronger Astra review prompt supplied by Claude

The proposed improvement makes runtime checking explicit rather than allowing an internal-consistency review of planning text. That is a plausible process improvement, not proof of why a particular prior Astra review passed. More findings alone do not establish a better review; each finding still needs evidence.

```text
Review request: evidence-led plan review

Goal
Decide, on primary or runtime evidence, whether a competent expert would materially change this plan. No material issues is a valid result after the evidence ledger is complete.

Inputs
- Plan files: <paths>
- Hosts, clients, and versions: <scope>
- Permitted read-only sources: installed binaries/packages, local session and rollout records, relevant user/project configuration, and official documentation.
- Do not modify files/configuration, send messages, start sessions, use Computer Use, or run live tests without separate authorization.

Method
1. Inventory the load-bearing assumptions: those whose failure breaks a requirement, metric, privacy property, or user workflow. Include implicit identity, record-content, permissions, command-expansion, ordering, and timing assumptions.
2. Attempt to falsify each using the closest primary evidence. Do not count consistency between plan files as runtime evidence. When documentation and observed behavior differ, distinguish client/version/surface and explain the evidence boundary.
3. Trace a concrete run for each supported host and entrypoint: user input, expansion, process/agent, exposed identities/paths, reads/writes, permissions, and result. Mark the first unverified step.
4. Check relevant different-project, side/fork, long/compacted history, denied-write, peer-message, and schema-change cases. Keep investigation proportional to the actual workflow.
5. Only then decide. Findings need a concrete trigger, failing step, consequence, and evidence. Unknown behavior is an unknown with an observable settling check; it is neither a demonstrated defect nor a verified pass.

Avoid
- Style-only or speculative findings without a concrete trigger.
- Assuming another reviewer's claims are correct or incorrect.
- Padding findings or suppressing issues to produce a clean pass.
- Conflating shared context with identical session identity, or fresh-worker execution with guaranteed blinding.

Reply
1. Yes/No: would a competent expert materially change the plan?
2. At most five material findings: file:line, trigger, failing step, consequence, likelihood, source evidence, and smallest correction.
3. Evidence ledger: load-bearing assumption -> verified/falsified/unverified -> evidence or settling check. Include it even with no findings.
4. Material unknowns with a focused observable check for each.
```

This method was passed to the Astra High pressure-test reviewer while its independent source inspection was in progress, without supplying Claude's verdict as authority.

### Astra High pressure-test result

A fresh `gpt-6-astra` reviewer at high effort returned **Yes: side-first is a useful simplification, with three material qualifications**. It produced an assumption/evidence ledger and concrete execution traces rather than the initial review's unsupported blanket pass.

1. **Separate client surfaces.** Installed Claude CLI 2.1.318 retains a tool-less `/btw` path. Claude Desktop 4.16336.0 implements a new `/btw` side-session fork with feature/eligibility checks and an older side-question fallback. The observed Desktop fork used the embedded 2.1.317 runtime and actually executed Bash/MCP tools. This is a client distinction, not evidence that the user's observed tools were imaginary or that all `/btw` implementations are identical.
2. **Keep original-subject identity and an immutable cutoff.** The observed fork contains 230 shared user/assistant UUIDs retaining the parent's session ID. Child line 701 synthesized an interrupted tool result, while parent line 693 later records success for the same invocation. At the fork boundary that parent result was pending. A collector must not call the synthetic child event a parent failure or silently incorporate later parent events. Another explicitly named subject overrides default ancestry. Collector context usage and child counts must remain separate from original-subject metrics.
3. **Use capability-aware, bounded fallback.** Installed ChatGPT Desktop 26.1029.70936 build 24905 supplies side-conversation instructions permitting inspection and explicitly requested local mutations but prohibiting subagents. Source tracing established their application to ephemeral and persistent side forks. Always requiring a new worker inside that mode would therefore be incorrect. Direct capture in a suitable confirmed side session fits the observed restrictions; ordinary-chat invocation can retain one-hop delegation. Unknown identity/capability should produce one clarification or a concrete limitation, not recursive isolation attempts.

The reviewer distinguishes inherited-context evidence assessment from a fresh acting-agent self-assessment. It rejects the claim that a fresh worker is inherently required for this capture goal: the user did not require formal blinded judging. Honest attribution, explicit context provenance, and primary record verification are necessary either way. The parent agrees this is a design trade-off rather than a categorical independence requirement.

**Still unverified:** exact nested explicit-only skill loading for the proposed `/side $capture-agent-issue …` and `/btw /capture-agent-issue …` command forms, across the intended clients. Actual skill attachment/command tags, usable permissions, trustworthy source/cutoff exposure, synthetic packet creation, and absence of unintended parent transcript additions need a bounded client-specific smoke check before documenting a form as supported. No live skill test was run by either reviewer.

**Source locators retained from Astra's read-only inspection:**

- Claude child record `5202a5f9-63bf-4654-b619-26c16ff78e2c.jsonl` under `~/.claude/projects/-Users-dre-src-agentic-devcraft/`, lines 701–704, 716–719, 735–739; parent `b0db7ce7-ef5b-4dea-935a-eca31677fbf0.jsonl`, line 693.
- Claude Desktop ASAR members `/.vite/build/index.chunk-_xHmE7Nf.js`, offset 11462 (side fork); `index.chunk-CqaSnEfn.js`, offsets 675596, 685093, 693605 (fallback); `index.chunk-DZWftBCb.js` (`Ar`/`Mr` reminder).
- ChatGPT Desktop ASAR members `/webview/assets/async/104621.7cc9031f55.js`, offset 144636 (side instructions); `/webview/assets/async/299250.3353e2695c.js`, offset 22982 (`AqOV` application); `/webview/assets/async/283304.78fc79feb0.js`, offset 25709 (`vBFC` application).

### Current disposition

The temporary-output and recognizable-name/payload-preference revisions are in the four planning artifacts and pass strict validation. On 2026-11-06 the user adopted the execution rule: direct capture in a confirmed tool-capable side session, one-hop delegation from an ordinary session, and one focused clarification or concrete limitation for unknown identity/capability without recursive isolation. The four artifacts now encode that rule and original-record subject/cutoff provenance. Exact nested one-line invocations remain unverified until the requested probe runs; the real capture skill is not implemented or installed by this update.

## Disposable Desktop probe prepared on 2026-11-06

At the user's explicit request, prepared a separate `agent-issue-probe` under `/var/folders/h2/v24t58z935jbjh4phhvkhc3r0000gp/T/agent-issue-probe-x_ca7_l8/agent-issue-probe` and installed non-destructive discovery symlinks at `~/.claude/skills/agent-issue-probe` and `~/.codex/skills/agent-issue-probe`. Source and marker output are temporary, outside worktrees. This probe does not invoke or implement the real issue-capture skill.

It uses the same native explicit-only metadata, requests direct execution without further forks/subagents, and records a small temp JSON marker plus self-reported collector/subject/isolation evidence. It does not retrieve transcript contents or send messages. A skill-body token verifies that the probe instructions were available; the marker explicitly does not claim that token possession proves native expansion. Native skill attachment/command evidence still needs inspection after the user runs the commands.

Local preparation checks passed: shared skill validation with the documented Claude extension checked separately, both explicit-only flags, helper execution/readback, private directory/file permissions, distinct outputs, wrong-token rejection, and installation-link resolution. Helper runs are explicitly labeled `helper-self-test`; neither Desktop entrypoint has been run or counted as passing.

User test inputs, one in each Desktop client's original chat:

```text
/btw /agent-issue-probe claude-desktop-side
/side $agent-issue-probe codex-desktop-side
```

Expected result is `PROBE_RECORDED` plus a temp result path, or the actual unsupported-command/loading/tool/permission failure. Do not recover a failed native invocation by manually reading the skill: that would invalidate this check. After the two results are inspected, remove only the two probe symlinks and this disposable probe's temp artifacts when no longer needed.


## Desktop probe results verified on 2026-11-06

Both user-run Desktop side probes passed native loading, shell execution, private marker write, and record readback. These are real Desktop runs, not helper self-tests. The original result JSON files were left unchanged; a separate verification summary is at `/var/folders/h2/v24t58z935jbjh4phhvkhc3r0000gp/T/agent-issue-probe-x_ca7_l8/verification.json`.

### Claude Desktop result

- Result: `/var/folders/h2/v24t58z935jbjh4phhvkhc3r0000gp/T/agent-issue-probe-claude-desktop-side-_b93ce2d/probe-result.json`.
- Native loading: child transcript lines 16564–16565 contain the host command event and injected skill body. The only new tool was Bash; the helper actually wrote/read the marker. Recorded runtime: 2.1.317.
- Collector: `b4485ece-0ac1-4729-8491-a80367af9001`. Original subject: `0c06ad46-45c2-42e2-aea0-2c1c2faa3c47`, titled **Implementation Advisor**, in a different project's worktree. This also exercises invocation outside the skill's source checkout.
- Original and child files share an exact 16,552-line / 39,901,503-byte prefix. The source cutoff UUID is `103def4c-fb8f-4736-8ded-6ed5f7f73800`, timestamp `2026-11-06T17:35:03.332Z`; the first own child conversation event links to it through `parentUuid`. Child lines 16562–16563 are synthetic boundary events, excluded from subject evidence and metrics.
- No child-own conversation UUID appeared in the parent; the parent's post-cutoff records contain no occurrence of the unique result marker. This supports isolation for the observed run.

### Codex Desktop result

- Result: `/var/folders/h2/v24t58z935jbjh4phhvkhc3r0000gp/T/agent-issue-probe-codex-desktop-side-mc6g4xxg/probe-result.json`.
- Native loading: side-rollout lines 13 and 15 contain the skill link and expanded skill attachment. Two shell calls ran; neither call ID appears as a call in the parent. Runtime: 0.167.0-alpha.3.2.
- Collector: `01a1b1ee-403a-7250-b303-ad0927296ab9`. Subject: `01a1ac44-55a2-7171-972c-48e1378c463c`, this capture-design chat; its title is available from native read-thread metadata.
- `session_meta.forked_from_id` and `history_base.thread_id` identify the subject. `history_base.end_ordinal_exclusive` is 901 and `end_byte_offset` is 3,048,845; the source prefix ends on a newline at ordinal 900, timestamp `2026-11-06T17:34:56.150Z`. `forked_from_ordinal_exclusive` corroborates the boundary. Native turn trigger: `side_chat`.
- Parent ordinals 901–903 contain settings/current-turn metadata only. Ordinal 904 is the user's pasted results; no child response or probe execution was automatically inserted before that report.

### Probe disposition

The immediate-metadata gaps reported by the probe are recoverable through targeted host-record inspection. No further manual probe is needed to settle the Desktop execution rule. These runs establish usable native side entry, tools/temp writes, source identity/cutoff retrieval, and observed parent separation on the tested runtimes. They do not establish full capture correctness, generalized CLI support, automatic-invocation behavior under unrelated prompts, or all approval paths. Those remain scoped implementation checks. The real capture skill remains unimplemented; the probe and its symlinks are retained for now.


## Implementation and local installation on 2026-11-06

Implemented the 130-word router, collector procedure, revised packet template,
harness-specific retrieval/accounting reference, and a stdlib-only metrics/private-save
helper. Installed one shared source through both `~/.claude/skills/capture-agent-issue`
and `~/.codex/skills/capture-agent-issue`; both links and supporting files verified.
Removed only the earlier draft's obsolete checkout-capture ignore rule and updated
user/developer documentation. Unrelated working changes were retained.

Verification:

- Nine focused helper tests pass: native user provenance and legacy deduplication,
  human/peer/generated-message classification, cutoff validation, repeated tool IDs,
  missing telemetry, fork boundary exclusions, private non-overwriting writes,
  recognizable names/UTC minute, fallback names, worktree-temp rejection, and symlink refusal.
- Shared skill validation passed with Claude's documented frontmatter extension
  verified separately; both native explicit-only flags are set.
- Native read-only metrics from the earlier Codex and Claude probe source prefixes
  extracted model/effort, size, turns, tools, and reported context usage. Codex
  capacity was recorded; Claude capacity was explicitly unavailable rather than
  inferred. Claude unknown-origin messages remained separate from human turns.
- Independent delegated Codex collectors produced four synthetic packets: default
  de-identified, requested full detail, contradicted complaint/no substantiated
  error, and unavailable-record/allegation-only. A fifth ambiguous request returned
  `needs_clarification` and no packet. No further delegation or source remediation
  was performed. Default payload removed invented identifiers while names in the
  temp output path remained recognizable; full-detail payload retained the invented
  names/URL/path. Both edit-incident packets distinguished attempted writes from
  unverified persisted changes.
- Forward-test outputs, native metric summaries and fixture material are private
  temporary artifacts under `/var/folders/h2/v24t58z935jbjh4phhvkhc3r0000gp/T/capture-agent-issue-validation-mfwp0qt3/`
  and the helper-created `agent-issues/` temp directories. No real transcript was
  copied into the repository or a packet.

These generated-packet tests used Codex collectors for both source formats. At
that stage, the disposable Desktop probes established native loading separately
from actual capture. The subsequent user-confirmed installed-skill pass below
closes task 4.1; no further client matrix is required.


## Shared plugin marketplace installation (2026-11-06)

At the user's request, promoted capture-agent-issue from proposals into the shared
plugin and versioned both host manifests at 0.2.0. Registered the local checkout
as marketplace agentic-devcraft and used native marketplace add/install commands
for both hosts. Both native registries report agentic-devcraft@agentic-devcraft
0.2.0 installed and enabled. Claude component inventory lists capture-agent-issue
and status. All six skill files in both installation caches match the shared source
by SHA-256. Removed only the two verified standalone capture-agent-issue symlinks
and the byte-identical duplicate candidate source after successful installation.
No GitHub commit/push/publication or unrelated plugin changes occurred.

Moved the two untracked packet artifacts unchanged to captures/agent-issues/ and
verified their hashes and Git-ignore status. Removed the public README backlink
to the private packet; the capture default remains host temp. Focused helper tests
pass from the packaged source path.

## Installed-skill acceptance — 2026-11-16

The user confirmed that the actual installed skill had already been tested and
successfully captures an issue packet. Task 4.1 is passed on that acceptance
evidence. The expanded synthetic client matrix is removed, not deferred; no
additional integration work is outstanding. This is user-confirmed acceptance,
not a new agent-observed run or a claim that every former matrix case was tested.
