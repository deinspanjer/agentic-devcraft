# OpenCode compatibility evidence

Recorded 2026-11-16 against source revision `db0cef4` plus the uncommitted working
tree of this change. All session content was synthetic. Paths, passwords, and
session IDs of the disposable runtime are omitted.

## Runtime

- Binary: `/Applications/OpenChamber.app/Contents/Resources/opencode-cli/opencode`,
  version 2.3.0, run as `opencode serve` on a loopback port.
- Isolation: `env -i` with a temporary `HOME` and temporary
  `XDG_CONFIG_HOME`/`XDG_DATA_HOME`/`XDG_CACHE_HOME`/`XDG_STATE_HOME`. No normal
  harness home, cache, or live session was read or written; nothing was installed.
- Model for agent runs: `opencode/big-pickle` (free). Skill sources were plain
  copies of the four canonical skill directories, listed by absolute path in a
  throwaway project's `opencode.json`; workspaces were unrelated temp repositories.

## Schema and routes observed

- `GET /api/skill?location[directory]=<dir>` returns `id`, `name`, `description`,
  `autoinvoke`, `path`, `content`. Prompt body: `{text, skills: [{id}]}`.
- Session record: `id`, `title`, `location.directory`, `time.created`, `model`,
  `tokens`, `cost`; a fork adds `fork: {sessionID, boundary: {type, messageID}}` and
  has no `parentID`; a subagent child has `parentID` and no `fork`.
- `GET /api/session/<id>/message`: `order`, `limit`, `type`, `cursor`. `cursor.next`
  pages forward; `order` cannot be combined with `cursor` (`InvalidCursorError`).
  Four pages of five reproduced the unpaged list and the export exactly (16
  messages, no duplicates) on an idle session.
- `GET /api/experimental/session/<id>/export` returns the message list but omits a
  message still in progress; the message list includes it.
- `GET /api/experimental/session/<id>/log` returned only `log.synced` with the
  current sequence, no history. Not used for cutoff.
- `OPENCODE_SESSION_ID` is set in the shell tool's environment, and a bare
  `opencode api` there reached the server running that session.

## Results

| Check | Result |
| --- | --- |
| Listing | All four skills listed with `autoinvoke: false`. |
| On-call | A session asked to list its skills named only the built-ins. |
| Status, standalone copy | `unknown` / `none` / `not applicable`. |
| Status, release record | Version and `repository@revision` from `release.json`. |
| Status, conflicting records | `conflict` listing `release.json` 0.2.9 and manifests 0.3.0. |
| Status, package layout | 0.3.0 from manifests, plugin `not verified`. |
| Capture, ordinary session | Delegated once; worker (`parentID` = subject) saved a packet; parent relayed a compact result. |
| Capture, fork | Captured directly, no child session; subject = `fork.sessionID`. |
| Capture, other named subject | Delegated once; worker captured the named session, not its parent. |
| Capture, delegation denied | Reported the limitation; no packet, no collection in the parent. |
| Late tool outcome | Fork taken while a tool ran: before completion the export lacked the boundary message (`boundary_in_export: false`, bounded by fork time); after completion the same call is listed under `pending_at_cutoff` and its outcome is not measured. |
| Cleanup, OpenCode only | OpenCode rules applied; override guidance inventoried and given a proposed destination. |
| Cleanup, Codex + OpenCode | Both rule files applied; conflict surfaced as a question. |
| Cleanup, Codex only | Codex override precedence applied. |
| Cleanup, unlisted harness | `AGENTS.md` treated as its file; no other harness's rules applied. |
| Cleanup originals | Unchanged in all four runs (checksums); output only in the dated mirror. |
| Docs audit and plan | Default output under `.agents/artifacts/doc-pattern`; hidden directory excluded; nested `AGENTS.md` not a divergence; inputs unchanged. Helper-only run also covered `--scope all`, explicit output paths, and all three plan levels. |

## Gaps and deviations

- A missing or mismatched session identity was not reproducible in this runtime;
  that branch is instruction-only.
- In the ordinary capture the parent read `worker.md` although told to read only
  the launcher section. Routing and results were still correct.
- An early fork capture hit the in-progress-boundary case before the helper handled
  it and recorded it as a gap; the helper and profile were fixed and re-verified
  against live exports, but that full agent run was not repeated.
- Context capacity, issue-time harness version, and physical transcript size are
  not in the records; packets mark them unavailable.
- Claude packaging was checked with `claude plugin validate`. The Codex payload was
  checked by manifest and reference resolution; in addition the maintainer loaded a
  copy of `status` (with the `metadata` frontmatter) from a throwaway project's
  `.agents/skills` in the Codex CLI and got the expected report. The plugin
  marketplace install path was not re-run in Codex.
- Maintainer check of selection forms from a local-checkout source: `@status` works
  in the OpenCode CLI and in OpenChamber; `$status` works in OpenChamber only. Both
  reported version 0.4.0 from the package manifests.
- The session-read routes are experimental. The initial checks used 2.3.0.

## Capture regression on OpenCode 2.3.2

Recorded 2026-11-23. In an OpenChamber Desktop session, bare `opencode api`
started a second service. Both services could return the same session ID.
The launcher initially checked the response root rather than `.data.id`;
the session was available and the original capture later saved a verified packet.

The revised helper identified the actual OpenChamber server from the shell's
process ancestry and its managed registration. It rejected the second service
even with valid authentication and exported the original subject through
OpenChamber. The metrics helper resolved the original invocation message as the
exclusive cutoff. This check did not modify the original session or its packet.

In a separate 2.3.2 server with an isolated home and the revised standalone skill,
`opencode/big-pickle` ran two synthetic captures. The ordinary session delegated
once, and its worker exported the original subject and used the invocation
message as the exclusive boundary. The fork collected directly with no child,
used the original subject ID, and supplied the native fork boundary and timestamp
to metrics. Both wrote a private Markdown packet. The readback hashes matched
the save receipts, and the invoking sessions returned the packet paths.
The final helper passed a second run with explicit checks of the parent and
worker tool calls, including that the ordinary parent did not export the subject.
