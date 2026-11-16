# Catalog delivery evidence

Recorded 2026-11-16.

- Pages source set to GitHub Actions; the `github-pages` environment allows
  `branch:main` and `tag:v*`.
- Release `v0.4.0` (not draft, not prerelease) at revision
  `a82c8e4597894198363dafd28fbbbec8f1afffe3`. The publishing workflow ran on the
  release event and succeeded on its first run.
- Deployed catalog: `https://deinspanjer.github.io/agentic-devcraft/opencode/skills/`.
  `index.json` lists the four skills at version `0.4.0`; all 21 listed files returned
  200. `status/release.json` names version `0.4.0` and the release revision above.
- Native load: an isolated OpenCode 2.3.0 server with only that URL under `skills`
  listed all four skills with `autoinvoke: false` and cached their files, including
  each `release.json`. The first listing request returned before the download
  finished and was empty; the next one was complete.
- Not done against the deployed URL: a model run of `status`. The free model's usage
  limit was reached. The same generated catalog served locally had reported its
  release record correctly, and from a local-checkout source `status` reported
  `0.4.0` in the OpenCode CLI and OpenChamber.
