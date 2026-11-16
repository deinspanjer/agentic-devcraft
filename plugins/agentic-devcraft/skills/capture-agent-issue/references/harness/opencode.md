# OpenCode records

Observed version: OpenCode 2.3.0, isolated server. Session reads below are
experimental API routes; check actual fields and report differences as gaps.

## Launcher

Read this section only; the collector reads the rest.

- Your session ID is `OPENCODE_SESSION_ID` in the shell tool's environment.
- Reach the server with `opencode api` from the shell tool. Confirm the connection
  first: `opencode api GET /api/session/$OPENCODE_SESSION_ID` must return that same
  `id`. A failure or another ID means this CLI is not connected to the server running
  the session. Report that limitation or ask for the server; do not try other
  binaries, guessed ports, the database file, or a session listing.
- Mode comes from that response, not from user text:
  - `fork` present: a fork of `fork.sessionID`. Capture directly; do not delegate.
  - `parentID` present, no `fork`: a delegated worker with fresh context, not a fork.
  - neither: an ordinary session. Delegate once.
- Ordinary boundary: the newest user message is the capture invocation.
  `opencode api GET "/api/session/$OPENCODE_SESSION_ID/message?order=desc&limit=1&type=user"`
  gives its `id`; the subject stops before it.
- Delegate with the `subagent` tool, once. Hand over the invocation text, your
  session ID as subject, that boundary message ID, the project directory,
  capture-start, and the absolute `worker.md` path. The worker runs in the
  background and its result arrives as a `<subagent>` message; do not poll, sleep, or
  duplicate its work. If `subagent` is unavailable or denied, report that limitation.

## Collector identity and subject

- Your own session ID is `OPENCODE_SESSION_ID` in the shell tool's environment;
  `opencode api GET /api/session/$OPENCODE_SESSION_ID` returns your session record
  and must show that same `id`. Record it as the collector. A worker's `parentID` must equal the subject ID it
  was handed, unless the invocation names a different subject. A mismatch is a
  clarification, not a reason to search sessions.
- A fork's subject is `fork.sessionID`. `fork.boundary` is `before` or `through` a
  message ID in the original. Your own `time.created` (epoch milliseconds) is the
  cutoff time.
- `title` and `location.directory` in the subject's session record give the session
  name and project directory. A missing title is `untitled-session`.

## Records and cutoff

- Save the subject's records to a private temp file without printing them:
  `opencode api GET /api/experimental/session/SUBJECT_ID/export > /private/temp/export.json`.
  Let that command finish before anything reads the file; do not run it in the same
  batch of tool calls as the metrics helper. Read needed turns from that file with
  bounded reads. Paged
  `/api/session/SUBJECT_ID/message` is equivalent once the session is idle: first
  page `order=asc&limit=N`, later pages `limit=N&cursor=<cursor.next>` without
  `order` (the server rejects the combination), repeating any `type` filter. A
  failed page is a reported gap, never an empty result.
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
  transcript size. `opencode --version` from the connection confirmed above is the
  current version only. `export_prefix_bytes` is serialized export size, a separate
  measure.
