# Proposal

## Why

OpenCode needs a native, versioned way to discover and download Devcraft skills without interpreting Claude/Codex marketplace manifests or borrowing another client's installed cache. An HTTP catalog hosted on GitHub Pages provides that path with minimal packaging machinery.

## What Changes

- Generate OpenCode's `index.json` catalog and complete skill directories directly from the canonical `plugins/agentic-devcraft/skills/` payload.
- Publish that generated artifact through GitHub Pages when a stable GitHub release is published, using the release's tagged source rather than the current default branch.
- Give every catalog entry the shared release version and include a small per-skill `release.json` record matching the companion compatibility change's status-reader contract.
- Document the stable catalog URL, installation configuration, version-driven updates, provenance, explicit invocation, and uninstall.
- Keep the existing Claude/Codex marketplaces and canonical skill source intact; do not create host-specific source copies or an executable OpenCode plugin.
- Verify a valid catalog, reachable listed files, and native loading of a skill with its supporting resource. Rely on OpenCode's documented update mechanism rather than investigate its downloader internals.

## Capabilities

### New Capabilities

- `http-skill-distribution`: Native OpenCode catalog generation, release-based GitHub Pages delivery, per-skill release provenance, and documented installation lifecycle.

### Modified Capabilities

None. Runtime portability of the four skills is planned separately in `opencode-skill-compatibility`.

## Impact

- A small catalog generator, focused packaging checks, and a GitHub Pages deployment workflow.
- Generated output contains only released skill files and generated provenance; it is a deployment artifact, not another editable source tree.
- `USERS.md`, `DEVELOPERS.md`, and `README.md` gain the appropriate installation and publishing guidance. Harbor evaluations remain local; the new Actions workflow is only for distribution.
- The companion change owns skill behavior, on-call metadata, and reading local provenance. Both changes must land before advertising all four skills as OpenCode compatible.
- This proposal authorizes no deployment, GitHub setting change, release publication, or normal-user skill installation. Those actions require the later implementation/publication request.
