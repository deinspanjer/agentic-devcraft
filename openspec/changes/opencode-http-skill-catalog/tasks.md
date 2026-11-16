# Tasks

## 1. Catalog generation and provenance

- [x] 1.1 Implement a small generator for the native index and complete skill directories from `plugins/agentic-devcraft/skills/`, excluding caches/debris and refusing escaping paths or symlinks. Verify a small fixture preserves a nested resource and excludes non-payload content; inspect the real four-skill output without modifying canonical sources.
- [x] 1.2 Generate the agreed per-skill `release.json` and shared catalog version from the tagged release, requiring both host manifests and the release tag to agree. Verify mismatch rejection and provenance containing the actual source revision; use the generated status directory with the companion reader to confirm producer/consumer agreement.
- [x] 1.3 Document local generation, version inputs, provenance shape, and output boundaries in `DEVELOPERS.md`; run the documented generation command and verify every index entry references existing output files.

## 2. GitHub Pages release workflow

- [x] 2.1 Add a stable-release publishing workflow that checks out the release tag, generates/validates the artifact, and uploads only the generated site for Pages deployment. Inspect its release filter, source revision, and required Pages permissions; verify it does not run Harbor evaluations or publish default-branch development edits.
- [x] 2.2 Document enabling Pages with Actions as its source and the release publishing procedure in `DEVELOPERS.md`; verify the documented paths, tag convention, and expected catalog URL match the workflow. Do not change GitHub settings or publish during local implementation without explicit authorization.

## 3. Native use documentation and delivery acceptance

- [x] 3.1 Add the catalog configuration, version-driven update explanation, provenance, explicit invocation link, and source-removal procedure to `USERS.md`, with a short `README.md` link. Inspect that instructions preserve existing configuration, distinguish OpenChamber's Git catalog and native package plugins, and do not claim normal-user installation has already occurred.
- [x] 3.2 Run `openspec validate opencode-http-skill-catalog --strict`, focused generator checks, and a local HTTP/OpenCode loading smoke using generated files and isolated configuration. Verify a skill loads a supporting resource, and the generated status provenance is reported by the companion implementation; confirm existing marketplaces and global user sources remain untouched.
- [x] 3.3 After explicit publication authorization and companion compatibility completion, enable/configure Pages if needed and publish the chosen stable release. Fetch the deployed index and listed file URLs, confirm one native skill/resource load from the deployed URL, and record the actual URL and result. No polling/cache-internals investigation or multi-skill transaction check is required.

## Workflow follow-up

- Review both changes before apply; this task list is not permission to implement, change repository settings, or publish now.
- Land skill compatibility before advertising the first catalog release as supporting all four workflows. Catalog generation can be implemented independently; its status integration uses the companion reader contract.
- Keep only useful delivery evidence; do not retain disposable build output as another source tree.
