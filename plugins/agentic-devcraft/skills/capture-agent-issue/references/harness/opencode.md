# OpenCode records

Session reads use the OpenCode 2.3.x API. The launcher helper requires Python 3.9+
and a local Unix shell whose process descends from the session's server.

## Launcher

Read this section only; the collector reads the rest.

1. Run `python3 /absolute/skill/scripts/opencode_capture.py launch` in the shell
   tool. The helper checks the server PID against the shell's process ancestry
   before checking the session ID. A different service can return the same
   session ID from shared storage, and bare `opencode api` can start that service.
   Use the helper for all capture reads. If it fails, report its concrete error.
   For an unregistered local server, use a host-supplied `CAPTURE_OPENCODE_SERVER`
   loopback URL. Do not guess the endpoint or fall back to service discovery.
2. Route on the helper's `mode`. For `fork`, capture directly. For `worker`,
   collect directly with the original handoff. For `ordinary`, confirm that
   `invocation.text` matches the active invocation before using `invocation.id`
   as the exclusive cutoff. If it differs, do not use a newer message as the
   cutoff; resolve the original invocation or ask one focused question.
3. In an ordinary session, call `subagent` once. Pass the invocation unchanged,
   invoking session ID, invocation message ID as the exclusive cutoff for that
   session, directory, frozen capture-start UTC, and the absolute `worker.md`
   path. If delegation is denied or unavailable, report it.
   Wait for the automatic `<subagent>` result by ending your turn. If you reply
   before it arrives, report that capture is pending, not failed or complete.

## Collector identity and subject

- Run `python3 /absolute/skill/scripts/opencode_capture.py identify`. Record the
  returned `id` as the collector. A worker's `parentID` must equal the subject ID
  in the handoff, unless the invocation names a different subject. A mismatch is
  a clarification, not a reason to search sessions.
- For an explicitly named different subject, use a boundary verified in its
  export. Never pass the invoking session's message ID to metrics for that
  subject.
- A fork's subject is `fork.sessionID`. `fork.boundary` is `before` or `through` a
  message ID in the original. Your own `created_ms` (epoch milliseconds) is the
  cutoff time.
- Read the subject's name and project directory from the export's
  `.data.info.title` and `.data.info.location.directory`. A missing title is
  `untitled-session`.

## Records and cutoff

- Make a private temp directory. In the shell tool, set `umask 077` and run
  `python3 /absolute/skill/scripts/opencode_capture.py export SUBJECT_ID > "$private_dir/export.json"`.
  Wait for a successful exit before reading the export or running metrics.
  On failure, report the evidence gap. Never treat the output file as an empty
  transcript.
- Inspect bounded slices of `.data.messages`. User records have `id`, `type`,
  `text`, and `time.created`. Assistant records have a `content` array. For tool
  parts (`type == "tool"`), use `name`, `state.input`, `state.content`, and
  `time.completed`. Do not read or include reasoning parts.
- Projected messages change after the fact. A tool still running at a fork later
  shows its result inside the same original message. With a `through` boundary, treat
  any part or response whose `time.completed` is later than the cutoff time as
  pending: its outcome is not evidence at the cutoff.
- The export omits a message that is still in progress; the message list includes
  it. When a `through` boundary message is absent from the export, it was still
  running: pass the same `--through-message-id` with `--cutoff-ms`, and the helper
  bounds the prefix by the cutoff time and reports `boundary_in_export: false`. That
  message and any tool call it started are then unmeasured; say so.
- A fork's copied messages are frozen at fork time, omit a boundary message that was
  still in progress, and carry new IDs with the original timestamps. Use them to
  corroborate the prefix; cite original message IDs.
- An ordinary capture uses the messages before the invocation message.
- `/api/experimental/session/SUBJECT_ID/log` returned only its current sequence
  number, with no earlier events, on the observed version. Do not rely on it for
  history.

## Metrics

```sh
python3 /absolute/skill/scripts/capture_support.py metrics \
  --harness opencode --transcript /private/temp/export.json \
  --subject-id SUBJECT_ID --before-message-id INVOCATION_MESSAGE_ID
```

For a fork use the recorded boundary and add the cutoff time:
`--through-message-id BOUNDARY_ID --cutoff-ms FORK_CREATED_MS` (or
`--before-message-id` for a `before` boundary).

- Human turns are `user` messages in a top-level session. `synthetic` (including
  `<subagent>` reports), `skill`, `shell`, `system`, and `compaction` messages are
  generated. In a session with a `parentID` the sender of `user` messages is not
  recorded, so they count as unknown origin.
- Assistant messages give `model` (provider, ID, variant), `tokens`, and tool parts.
  Reported context usage is the latest response completed by the cutoff: input +
  cache read + cache write. `pending_at_cutoff` lists tool calls whose outcome was
  not yet recorded.
- The session record's `tokens` and `cost` are current whole-session totals that
  include later and auxiliary generation; they are not issue-time values.
- Not recorded: context capacity, harness version at issue time, and physical
  transcript size. The helper's `server_version` is the current server version
  only. `export_prefix_bytes` is serialized export size, a separate measure.
