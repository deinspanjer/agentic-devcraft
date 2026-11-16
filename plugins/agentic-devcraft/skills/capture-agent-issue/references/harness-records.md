# Harness records: read only the relevant profile

Observed versions: Claude Desktop embedded 2.1.317; Codex Desktop 0.167.0-alpha.3.2
(0.166 also supplied model/effort/token events). Check actual fields. Report schema
gaps, not guessed defaults or generic history-loss caveats. No Computer Use of agent apps.

## Codex

- `CODEX_THREAD_ID` may expose collector identity to its shell. Locate that exact
  rollout under `~/.codex/sessions/<date>/`, not a global transcript-content dump.
- A side's `session_meta.forked_from_id` identifies its source. `history_base` gives
  `thread_id`, `end_ordinal_exclusive`, and `end_byte_offset` for the original prefix;
  `forked_from_ordinal_exclusive` corroborates it. Validate against the original file.
  The side boundary and `task_started.turn_attribution.turn_trigger: side_chat`
  corroborate isolation. In an ordinary session exclude its capture-invocation event.
- Native read-thread metadata can supply original title; otherwise `untitled-session`.
  Do not create/message chats for a title. Source `cwd` provides project context.
- `session_meta.cli_version`, `turn_context.model`/`effort`, and latest
  `event_msg/token_count.info` give settings, `last_token_usage`, `total_token_usage`,
  and `model_context_window`. New `token_usage_record` may supplement; never count
  both representations as separate model calls.
- Older records can expose canonical `event_msg/user_message`; count these rather
  than duplicate response items. In the tested paginated Desktop records these
  events were absent: `response_item` user messages instead expose
  `internal_chat_message_metadata_passthrough.content_item_kinds: [user.text]`.
  Count that provenance, excluding generated instructions/attachments. Honor
  explicit human/peer origin metadata and leave unrecognized origins unknown.
  `client_authored:false` also appears on real human input and is not an authorship test.
  Count unique function/custom-tool `call_id`, not outputs or wrapper text.

```sh
python3 /absolute/skill/scripts/capture_support.py metrics \
  --harness codex --transcript /exact/parent-rollout.jsonl \
  --subject-id ORIGINAL_ID --end-ordinal-exclusive 901
```

## Claude Code / Desktop

- Runtime/scratchpad or native metadata supplies collector ID. Locate its exact
  `<id>.jsonl` in the relevant directory of `~/.claude/projects/`.
- A fork preserves copied rows' `sessionId`. Its first own conversation event's
  `parentUuid` references an ancestor UUID: resolve that to the original source and
  validate the copied prefix for an immutable cutoff. No majority-ID heuristic;
  `isSidechain:false` alone does not mean an ordinary chat.
- Exclude generated boundary state/assistant/tool-result events. A fork may insert
  an interrupted result for a parent tool still pending at the cutoff; neither the
  synthetic error nor the parent's later success is in that source snapshot.
- Use original `custom-title`/`cwd` within the cutoff. A native `local_...` task ID
  need not match a transcript ID. Unresolvable ancestry needs locator clarification.
- `assistant.version`, `.effort`/`.perTurnEffort`, `message.model`/`usage` expose
  settings and usage. Context input snapshot = input + cache-creation input +
  cache-read input on the latest distinct response, not summed streamed usage.
  `api-request.params.output_config.effort` can supplement. No request-blob reads
  just to count tokens.
- Existing attributable status-line snapshots may expose context capacity/usage.
  Without one or an explicit record field, capacity is unavailable. No reconfiguration.
- Human turns: `origin.kind: human`, excluding `isMeta`, `isCompactSummary`, and
  tool-result messages. Peer requests count separately, even when `isMeta` is true.
  Missing origin stays unknown unless a native source establishes it. Unique
  `tool_use.id` counts calls; streamed blocks/results do not add calls.
- Without authoritative start metadata, first observed timestamp gives lower-bound
  age. Compaction markers do not by themselves mean older raw records disappeared.

```sh
python3 /absolute/skill/scripts/capture_support.py metrics \
  --harness claude --transcript /exact/original-session.jsonl \
  --subject-id ORIGINAL_ID --through-uuid LAST_ORIGINAL_EVENT_UUID
```

## Cutoff and helper limits

`metrics` requires one cutoff: exclusive ordinal, exclusive byte offset, inclusive
line number, inclusive UUID, or exclusive timestamp. Prefer native ordinal/UUID/byte
evidence over time approximations. Invalid/mismatched boundaries fail instead of
counting the whole file. No conversation text is emitted, only metadata/metrics and
source-line/accounting information. The helper is neither reviewer nor redaction
engine: render its data under payload privacy, not as an unfiltered attachment.
