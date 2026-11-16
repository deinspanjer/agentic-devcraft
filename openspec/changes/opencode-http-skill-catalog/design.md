# Design

## Context

See `proposal.md` and `specs/http-skill-distribution/spec.md` for scope and behavior. The existing plugin payload and both host manifests identify release `0.3.0`. There is no existing `.github/` workflow in the inspected checkout.

The companion `opencode-skill-compatibility` change owns runtime behavior and on-call metadata. This change owns generation and hosting only. Both publish from `plugins/agentic-devcraft/skills/`, never from installed client caches.

This design is included because release automation and the shared provenance record cross the two changes' boundary.

## Goals / Non-Goals

**Goals:** A small static catalog, one stable URL, release-derived files and versions, and an ordinary native-loading check.

**Non-Goals:** An npm plugin, marketplace-manifest emulation, OpenChamber UI integration, another editable skill tree, downloader/cache research, transactional multi-skill updates, or moving Harbor evaluations into GitHub Actions.

## Decisions

### 1. GitHub Pages with a generated deployment artifact

Use a custom GitHub Pages Actions workflow, not a committed `gh-pages` source tree. A small stdlib Python generator reads the canonical released skill directories and writes only the deployment payload:

```text
<site>/
  opencode/
    skills/
      index.json
      status/
        SKILL.md
        release.json
      capture-agent-issue/
        SKILL.md
        worker.md
        packet-template.md
        release.json
        references/...
        scripts/...
      agent-instructions-cleanup/...
      documentation-pattern-refactor/...
```

The expected URL is `https://deinspanjer.github.io/agentic-devcraft/opencode/skills/`. Use the URL returned by the actual Pages deployment in final operator documentation if repository hosting differs. Enabling Pages with Actions as its source is a straightforward implementation setup step, not a research gate.

The generator discovers skill directories containing `SKILL.md` under the canonical released root and includes complete regular supporting files, preserving their relative layout. Exclude bytecode/cache and OS/editor debris. Do not copy the repository root, proposals, captures, or evaluation output. Reject symlinks and escaping paths instead of resolving arbitrary external content. Sort entries and file lists for repeatable output.

Alternatives: raw GitHub branch URLs can serve a hand-maintained index but couple development edits to publication; release assets are good for downloads but not a nested file catalog. Pages directly serves the format OpenCode expects without requiring an executable plugin.

### 2. One release version, tagged source

Trigger publication on GitHub release `published`, filtered to non-draft, non-prerelease releases. Check out the event's tag, not the default branch. Require the release tag `v<version>` and both package manifests to agree; resolve its full commit SHA once for provenance.

Give all entries that release version. A changed released payload gets a new release version using the existing release discipline. This deliberately favors simple shared release versioning over content-hash versions or per-skill release management.

Generate and validate the complete artifact before the deploy step. Use standard Pages configure/upload/deploy actions with read-only source access and the deployment permissions GitHub requires (`pages: write`, `id-token: write`). Pin action revisions according to project practice when implementing. The workflow uploads only the generated site directory.

No timer, custom updater, or cross-skill transaction layer is needed. OpenCode's documented behavior refreshes a skill when its catalog version changes; do not promise an exact refresh interval. A single release version is a labeling convention, not an atomic install guarantee.

### 3. Shared local provenance contract

Generate a `release.json` inside each skill directory and list it in the catalog entry's `files`. The companion status implementation reads it without a network call. Agree on this minimal shape:

```json
{
  "schema": "agentic-devcraft-skill-release/v1",
  "skill": "status",
  "version": "0.3.0",
  "repository": "https://github.com/deinspanjer/agentic-devcraft",
  "source_path": "plugins/agentic-devcraft/skills/status",
  "revision": "<full-tagged-commit-sha>"
}
```

The version above illustrates the format, not authorization to publish the current checkout or reuse a version for changed skills. The generator owns this record; the compatibility change owns validation and reporting. No timestamps, secondary handwritten version file, signing scheme, or per-file hash registry is necessary.

Treat the record as source attribution, not proof that arbitrary installed files are untampered. Manual copies without it retain the compatibility plan's truthful unknown-version fallback.

### 4. Document native source configuration, not another installer

`USERS.md` shows a mergeable `opencode.json(c)` example with the published schema and a `skills` array containing the catalog URL. It explains that users preserve existing settings and skill sources; this work never edits their global configuration automatically.

Document updates by changing the published release version and relying on native catalog loading; use the normal config reload path if the user wants to reload the source. Do not invent a skill-update CLI. Explain local provenance and exact skill IDs, linking to the companion change's on-call invocation guidance.

Uninstall means remove this URL from every applicable configuration that contributes it and use normal reload behavior. Removing a source does not erase skill instructions already in a conversation, and another configured source can still define the same IDs. Do not prescribe broad cache deletion.

Distinguish OpenChamber's Git-backed Skills Catalog, which copies individual directories, from this HTTP source. Do not tell users to paste this URL into a Git repository source field or use `plugin add` for it. Claude/Codex retain their own marketplace instructions.

`DEVELOPERS.md` owns generator usage, release inputs, artifact boundaries, and Pages setup. `README.md` links to the installation guide. Keep each full procedure in one place.

### 5. Small validation boundary

Protect packaging mistakes that can silently omit supporting files or publish the wrong source/version. Use a small fixture to exercise a nested resource and excluded cache material, and a mismatch case for release metadata. Do not duplicate host-runtime acceptance owned by the companion change.

Check the generated index and listed paths locally. After an authorized publication, fetch the index and listed URLs and load one skill plus a supporting resource using an isolated OpenCode V2 source. This is enough for distribution acceptance.

Do not investigate catalog polling cadence, network-retry internals, or cache implementation. If a real loading problem occurs, diagnose that concrete failure.

## Risks / Trade-offs

- [Missing support files produce a discoverable but unusable skill] → Generate the complete canonical directory and verify listed files plus one native resource read.
- [A default-branch checkout publishes different bytes than the release] → Check out the release tag and emit its full revision in the generated record.
- [Publishing the whole repository leaks private or unreleased content] → Build from the released skill root and deploy only generated output.

## Migration Plan

Implement the generator/workflow and documentation alongside the companion compatibility edits, then validate locally without changing normal user installations. The compatibility implementation must be ready before the first release advertised as supporting all four skills.

Configure Pages for Actions and publish only when the user authorizes repository setup/publication. The first published catalog uses a new appropriate release version; no release number is selected by this planning change.

Existing Claude/Codex consumers need no migration. OpenCode users add the new URL themselves when ready. To remove the source, follow the documented configuration removal; do not delete canonical skills or unrelated installations.

## References

- [OpenCode V2 HTTP catalogs](https://opencode.ai/docs/skills/).
- [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
- Companion change: `../opencode-skill-compatibility/design.md`.
