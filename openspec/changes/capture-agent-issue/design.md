# Design

## Context

See `proposal.md` for motivation and `specs/agent-issue-capture/spec.md` for the behavior contract. The initial candidate draft was reconciled into the implementation. At the user's subsequent request, this skill was promoted into the shared plugin and installed through both native marketplace workflows at version 0.2.0. The default remains temporary storage; the separately requested local packet archive is git-ignored.

The project keeps one shared source for this packaged skill at `plugins/agentic-devcraft/skills/capture-agent-issue/`. Both marketplace manifests refer to the shared plugin payload; native installation caches are managed by the harnesses. Both harnesses support explicit-only invocation through different metadata. Other agents can read the same Markdown instructions.

Read-only inspection during discussion established these local record fields (observations, not a claim that every version has an identical schema):

| Harness | Observed record fields | Additional documented interface |
| --- | --- | --- |
| Codex 0.166.0-alpha.6 | `session_meta.cli_version`; `turn_context.model` and `.effort`; `event_msg` / `token_count` with `info.total_token_usage`, `last_token_usage`, and `model_context_window`; `token_usage_record` events | App Server documents `thread/tokenUsage/updated` |
| Claude Code 2.1.317 | Assistant events with `.version`, `.effort`, `.perTurnEffort`, `message.model`, and `message.usage` including cache token categories | Status-line payload documents `transcript_path`, session identity, model, effort, context capacity, and context usage |

The inspected Claude transcript retains user/assistant events before its compaction boundary. Session/rollout records are the primary history; there is no established reason here to assume compaction removes that history. A record's last timestamp/event is an evidence locator, not grounds for inventing missing history.

Primary documentation checked during design:
- [Claude skill invocation controls, substitutions, and supporting files](https://code.claude.com/docs/en/skills)
- [Claude status-line data](https://code.claude.com/docs/en/statusline#available-data)
- [Codex skill invocation metadata](https://learn.chatgpt.com/docs/build-skills#optional-metadata)
- [Codex App Server](https://learn.chatgpt.com/docs/app-server)

## Goals / Non-Goals

**Goals:** Keep the main-session payload small; capture directly in a suitable confirmed side session or delegate once from an ordinary session; retrieve source records directly; produce useful packets despite individual metric gaps; retain enough provenance to design a later comparison.

**Non-Goals:** A general transcript indexing service, a new telemetry hook or daemon, changes to user status-line settings, automatic diagnosis/remediation, remote reporting, Harbor integration, or remote GitHub publication. No automatic model override for the capture worker.

## Decisions

### 1. One skill, a tiny router, and collector-only supporting files

Use a single `capture-agent-issue` directory with `SKILL.md`, `worker.md`, `packet-template.md`, `agents/openai.yaml`, and a small collector-only harness reference if needed. Target no more than 150 prose words in the router; this is a maintainability budget, not a claim of measured token savings. An ordinary parent must not read the detailed supporting files. A confirmed suitable side collector reads them directly; `worker.md` serves the same capture procedure in either route.

Set Claude `disable-model-invocation: true` in frontmatter and Codex `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Do not make a second discoverable worker skill. Do not use Claude `context: fork` for the whole workflow: its documented subagent does not inherit the conversation. Instead adopt this bounded execution rule:

- Confirmed tool-capable side/fork session with permitted capture reads/writes: collect directly, honoring that mode's restrictions (including any ban on subagents).
- Ordinary session: delegate once and retain the compact return convention below.
- Unknown subject identity or capability: ask one focused question or report the exact limitation. Do not recursively fork/delegate, guess from user-supplied mode claims, or silently run the bulk investigation in an ordinary parent.

Use native mode instructions/reminders and corroborating source metadata for isolation evidence; the observed Claude fork's `isSidechain:false` does not establish ordinary-mode execution. A fresh worker is not required for formal independence: preserve account attribution and disclose inherited context instead of claiming blinding. Exact nested side-command skill expansion must be established separately on each supported client before its one-liner is documented as verified.

On 2026-11-06 the user-run disposable probe established native explicit-only skill expansion, shell execution, and private temp output in both tested Desktop side sessions: Claude's embedded runtime 2.1.317 and Codex Desktop runtime 0.167.0-alpha.3.2. Claude recorded a native command event and injected skill body; Codex recorded the skill link and expanded skill attachment. This verifies the entrypoint form with the disposable skill, not the future capture implementation or CLI clients. See `reviews.md` for evidence and scope.

On the ordinary-session route, the parent passes only the invocation text, subject-session identifier/locator already exposed by its harness, current project directory, worker path, pre-capture boundary (the invocation event/turn), and capture-start timestamp. Freeze capture-start in UTC when capture begins and preserve it through clarification or approval handoffs. If the subject is another named session, the collector resolves that reference through authorized read tools or records. Do not make the ordinary parent search or read transcript content. No automatic full-history fork is needed on the ordinary-session route. Verify subject identity on each host during smoke checks; if no trustworthy identity is exposed, return one request for a locator instead of guessing among sessions.

The collector (direct side session or delegated worker) can read scoped evidence and write the requested packet or a temporary prepared draft for the approved-save handoff below. A worker returns a compact result; its parent does not reload the packet. A direct side collector handles its own clarification/approval when its host permits it. If ordinary-session delegation is forbidden/unavailable, report that limitation rather than silently collecting inline. A side-mode ban on subagents does not block otherwise permitted direct capture.

Use a small result convention, not a general orchestration framework:

| Result | Parent action |
| --- | --- |
| `complete` | Report final path, synopsis, and material gaps |
| `needs_clarification` | Ask the single returned question; resume/relaunch the worker with the answer and existing source locators; no packet has been saved |
| `needs_save_approval` | Use normal host approval for the exact temporary prepared draft and intended destination; perform an exclusive, non-overwriting file transfer through shell tools without loading the packet text into context |
| `failed` | Report the concrete failure and recovery option; do not claim a saved packet |

Delegated workers are not required to ask the user directly or remain paused for a reply; the parent handles their compact results. A direct side collector can ask the user and use its own normal approval flow. No route is required to spawn an agent merely to request clarification or approval. A failed or declined approval leaves no claimed final packet and identifies any retained prepared temporary draft for recovery.

### 2. Direct record retrieval is the default

Use the actual subject transcript/rollout as primary evidence, with tool-supported session lookup where necessary. Identity-check the selected record before analysis. Inspect only the issue-relevant turns and associated task material, expanding backward for necessary instructions and decisions. Streaming/parsing a whole file to compute counts is different from loading its whole text into model context.

Use a stable pre-capture event/turn boundary for issue evidence and metrics. The capture invocation and subsequent collection tools are excluded from subject activity totals. Keep a source inventory with safe evidence locators and mark genuine access failures or absent fields; do not introduce generic transcript-completeness warnings without observed evidence.

For native side/fork entry, keep subject identity, collector identity, original-record locator, and immutable source-fork boundary separately. Use the original session through that boundary, not the child's file size/start or inherited context token count. The original parent may continue afterwards. Copied records preserve ancestor IDs and fork creation can synthesize interrupted tool results: an inspected child did so for a call that later succeeded in its parent. At the boundary that result was pending; neither the synthetic child error nor the later parent success belongs in the source snapshot. Another explicitly named subject overrides default ancestry and needs its own stated cutoff.

Verified retrieval routes from the two Desktop probes:

- **Codex:** `session_meta.forked_from_id` identifies the subject. `history_base.thread_id`, `end_ordinal_exclusive`, and `end_byte_offset` identify the original-record prefix exactly; `forked_from_ordinal_exclusive` corroborates the ordinal. Validate these against the original file rather than substituting fork time or collector context. `task_started.turn_attribution.turn_trigger: side_chat` supplies native mode evidence. Native read-thread metadata exposes the subject title.
- **Claude:** the saved fork preserves original `sessionId` values. Its first own conversation event's `parentUuid` links to the ancestor event UUID. Resolve that event to the parent source record and compare the original prefix; exclude synthetic child tool results and state metadata inserted at the boundary. The tested fork had an exact 16,552-line shared prefix and linked to its last source event. Source `custom-title` events provided the parent title. These facts were retrievable even though the probe's visible prompt did not expose ancestry. Do not rely on a majority-ID heuristic when explicit linkage is available; genuinely ambiguous ancestry still needs clarification.

For both tested runs, child tool/event identities were absent from the parent records. Codex had only settings/current-turn metadata between its source cutoff and the user's pasted report; Claude's parent had no occurrence of the unique probe-result marker. This supports transcript isolation for these runs, not a guarantee about every client/version or other side-chat action.

Retrieved text is evidence, not authority to execute instructions embedded in transcripts. Read access to a named record does not authorize messaging its live agent or modifying its project.

### 3. Separate allegation, self-assessment, and reviewer assessment

The worker extracts the user's account and any acting-agent self-assessment already present. It preserves recorded authorship: human input, peer-relayed account, system-generated content, or unknown origin. A peer claiming to quote the user is not independently observed human testimony. Its own interpretation is reviewer analysis.

The same attribution rules apply to a direct side collector. Inherited context must be disclosed; it is neither proof of formal independence nor grounds to relabel reviewer analysis as a new first-person reflection from the original acting agent.

If fresh self-reflection is requested from the current acting agent, the parent may write a brief optional sidecar in a private host-temp directory before launch and pass its locator; this must not create a worktree artifact. The worker first forms its evidence-based findings, then reads that sidecar and attributes it separately before saving. This ordering reduces anchoring without claiming that a prompt provides enforceable blinding. There is no worker pause or post-review parent reflection round trip. Another session's agent must not be contacted implicitly. Absent self-assessment is explicit, not filled in by the reviewer.

Include counterevidence and a valid no-substantiated-error result. Behavioral explanations must reference observable decisions and evidence; hypotheses and experiment suggestions are not established root causes. Do not expose private chain-of-thought.

### 4. Metrics use small harness profiles and explicit semantics

Document verified retrieval routes for the two initial harnesses. Prefer transcript fields for issue-time model/effort/version and usage, not current defaults or reviewer settings. Use any already-accessible native telemetry snapshot for context capacity/usage when needed. Claude's documented status-line payload is a capability, not proof that a snapshot is persisted and readable: implementation must verify a usable route before claiming that field is collected. Do not add hooks or reconfigure the status line merely to fill it.

No extraction script is required initially. If native records require repeated deterministic parsing to obtain trustworthy counts, add one narrow read-only helper with no dependency on model calls. Do not create a general adapter framework. If a helper is introduced, protect meaningful counting semantics with small synthetic records.

| Field | Meaning |
| --- | --- |
| Harness/model/effort | Recorded effective values for the issue-time turn; relevant changes listed separately |
| Context used/capacity | Latest recorded subject usage and reported capacity at/before cutoff, with the harness's accounting convention; never cumulative billed tokens labeled as context |
| Age | Cutoff timestamp minus recorded start, with source timestamps; elapsed wall time, not active working time |
| Transcript size | Decimal KB, bytes/1000, for the physical record prefix through cutoff; whole-file bytes separately labeled if prefix size cannot be established |
| Turns | Human-origin user messages and following assistant activity; exclude metadata, compaction summaries, tool results, and peer messages; count peer requests separately and report unknown origin |
| Tool calls | Unique invocation IDs, not tool results, streamed duplicates, or both a normalized event and its underlying call |

Keep subject and child/reviewer activity separate; counts default to subject only. Do not sum repeated usage attached to chunks of the same response. Each metric has source/locator, scope, units, cutoff/as-of, and measured/derived/estimated/unavailable status with reason or method. Optional field failure does not invalidate the rest of a packet. Profile/schema mismatch is an explicit gap, not an invitation to guess.

Claude origin classification uses recorded `origin.kind` along with `isMeta`, `isCompactSummary`, and content block types. A read-only check of the named review session confirmed human, peer, tool-result, metadata, and compaction-summary user records coexist. Other host versions need their own evidenced classification; absent origin fields alone are not proof of human input.

### 5. One versioned Markdown packet

Use `agent-issue/v1` as a template version, not a new machine ingestion API. Sections cover identity/cutoff/source coverage; project/task and expected behavior; user account; supplied self-assessment; evidence and decision/correction/recovery timeline; findings and counterevidence; effective instruction/configuration provenance; constraints/tool failures; runtime/session metrics; experiment candidates and reproduction; privacy and limitations.

Capture the relevant instruction text and precedence when supported, plus version/hash provenance when available. Distinguish historical evidence from current project state. Candidate experiments should specify the failure trigger, minimal replay context, observable pass/fail criteria, competing explanations, and a nearby appropriate-behavior case to detect overcorrection. Unknowns remain unknown; capture does not promise every incident is reproducible.

Apply the user's payload-privacy preference. Without an override, de-identify identities, internal locations, proprietary code/business information, and unnecessary identifiers throughout the packet body, including metadata, examples, and embedded evidence locators. Retain public technical names and the failure mechanism. A request for a full-detail payload or specific retained details overrides that default where enforced policy permits. Record the applied preference, required omissions, and any resulting loss of evaluability; do not claim guaranteed anonymity. Do not attach a raw transcript or reversible alias map automatically. Local output path names are governed separately below and remain recognizable in either payload mode.

### 6. Local destination and installation

Default to this layout, independent of the skill's installation location:

```text
<host-temp>/agent-issues/<project-name>/<session-name>/<YYYY-MM-DDTHH-mmZ>-<unique>/packet.md
```

Resolve the temp root using the host's standard OS temp-directory facility, honoring its configured temp root (for example, macOS `$TMPDIR` or `/tmp` on many Unix hosts). Confirm the resolved default is outside the invoking worktree, subject worktree, and skill checkout; if a misconfigured temp root points inside one, report the configuration problem instead of silently creating capture artifacts there. A user-specified output path takes precedence and can intentionally choose another location.

Use the subject project's available display name, falling back to the basename of its recorded project directory, then `unknown-project`. Use the subject session's recorded/display title, falling back to `untitled-session`; document missing names in the packet. A capture about another session uses that session's project/title, not the worker's identity. Preserve recognizable names, including case, spaces, and supported Unicode: do not de-identify, lowercase, transliterate, slugify, or arbitrarily truncate them. Replace only characters forbidden by the host filesystem or requiring path separation, and handle reserved dot-components or actual length limits only as needed to obtain a valid contained component. Use a readable replacement and a short disambiguator when a required transformation loses distinguishing text. Names are literal path data, never interpolated executable shell text or unrestricted paths.

The timestamp is capture-start time, not the subject's historical start or cutoff time. Format the frozen UTC time as `YYYY-MM-DDTHH-mmZ`; do not use the caller's local timezone or recompute it after a clarification. Create the leaf directory through an exclusive OS temporary-directory operation with an unpredictable suffix; repeated names and captures within the same minute must not overwrite. Keep the leaf directory private to its owner and create packet files with owner-only access using the host's equivalent permissions. Never reuse an existing capture directory solely because its names match.

Local path names are intentionally recognizable and are not de-identified. Filesystem-required character handling is independent of payload privacy. The user may prefer a de-identified or full-detail payload without changing that naming rule. Returned local paths naturally contain the requested names; references embedded in a de-identified payload continue to follow its selected privacy preference.

Temporary storage is not durable project evidence: document that OS cleanup may remove captures, with no automatic promotion, repository copy, or retention service. Default packet, staging, and self-assessment artifacts must stay out of worktrees. The user also requested a deliberately retained local archive at `captures/agent-issues/`; keep that directory git-ignored. This optional archive does not change the default output or make private packets part of the plugin.

The temp default avoids the ordinary cross-project checkout write, but actual host permissions still apply. For explicit destinations or unusual temp-root restrictions, use the host's normal approved write mechanism when the worker can request it. If it cannot, return `needs_save_approval` with a private temporary prepared draft path and the exact intended destination; the parent performs the approved exclusive transfer without reading the contents. Staging is explicitly reported as staging, not an alternative final destination. Only a refusal, unavailable approval capability, or failed approved write is a failed save. Return that exact limitation and offer a user-requested alternate path or explicit inline delivery; do not flood the main session automatically. No publishing, committing, uploading, remote issue creation, or underlying-task changes.

Use native marketplace registration and plugin installation for both harnesses, sourcing this checkout for uncommitted development. Verify version, installed/enabled registry state, packaged content hashes, and component inventory. Only after verified installation remove the old standalone capture-agent-issue links and duplicate candidate source, leaving unrelated skills intact. The current registrations are local marketplaces, not a GitHub publication. The user confirmed successful installed-skill capture on 2026-11-16; no additional integration matrix is required. No credential or unrelated configuration changes are required.

## Risks / Trade-offs

- [Prompt-only de-identification can miss indirect identifiers] → Synthetic privacy case plus human review before later deliberate sharing; output stays local and uncommitted.
- [Transcript schemas differ across versions] → Record tested versions, parse only supported fields, report actual mismatch, and retain useful partial packets.
- [Capture work can be confused with subject work] → Explicit subject identity and pre-capture cutoff; reviewer metadata separate.
- [Parent handoff can bias reviewer] → Direct raw evidence and no parent-curated conclusion or excerpts; self-assessment separately attributed.
- [Minimal launcher still launches an agent with host startup overhead] → Claim reduced parent context loading only; do not claim lower total cost without measurement.

## Migration Plan

The implementation uses the router/collector split and temporary output layout. For the requested marketplace promotion, place the skill in the shared plugin, update both manifests to 0.2.0, register the local checkout and install through each native marketplace CLI. Verify cache contents and inventory before removing the former standalone links/source. Retain unrelated work and preserve packet bytes while relocating the two private packets to the ignored local archive. Installed-skill capture has passed by user confirmation; the expanded acceptance matrix was removed rather than deferred. Rollback uses native plugin management for this plugin only and leaves packets intact; remote publication is not part of this request.
