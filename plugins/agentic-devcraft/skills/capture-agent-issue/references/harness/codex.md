# Codex records

Observed version: Codex Desktop 0.167.0-alpha.3.2 (0.166 also supplied
model/effort/token events).

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
