# Claude Code / Desktop records

Observed version: Claude Desktop embedded 2.1.317.

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
