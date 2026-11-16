# Developing Agentic Devcraft

## Repository structure

- `plugins/agentic-devcraft/` is the single released plugin payload shared by
  the Claude and Codex marketplaces. Its `skills/` directory is also the source of
  the OpenCode catalog.
- `scripts/build_opencode_catalog.py` generates that catalog;
  `.github/workflows/opencode-catalog.yml` publishes it for stable releases.
- `proposals/skills/` contains unreleased skill sources under evaluation.
- `evals/harbor/` contains the local evaluation harness, fixtures, declarations,
  deterministic verifiers, and committable evidence.
- `evals/harbor/jobs/` contains ignored private trial artifacts.
- `openspec/` records capability specifications and completed change history.

Do not copy one skill into separate host-specific trees. A candidate has one
source under `proposals/skills/<name>/`; graduation moves that directory into
`plugins/agentic-devcraft/skills/<name>/`, where both marketplaces publish it
through the same plugin payload. OpenCode does not read the marketplace manifests;
it receives the same directories as standalone skills, so each skill must work from
its own directory alone.

### Harness-specific instructions

Keep `SKILL.md` and shared files harness-neutral. Put what differs by harness in
`references/harness/<harness>.md` inside that skill (`codex.md`, `claude.md`,
`opencode.md`), one harness per file, and have the skill tell the agent to read only
the file for the relevant harness. Create a file only when there is real content
for it; a missing file means the skill has no rules for that harness. There is no
shared router skill: a standalone installation has only its own directory.
Capture selects by the harness holding the subject's records; cleanup selects by
target harness, not the harness running the skill.

Every released skill sets `metadata: opencode/autoinvoke: false`, which makes it
on-call in OpenCode without changing Claude or Codex invocation policy.

## Local checks

Create the project environment and install the pinned Harbor dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r evals/harbor/requirements.txt
```

Run the deterministic suite and declaration checks:

```bash
.venv/bin/python -m unittest discover -s evals/harbor/tests -p 'test_*.py'
python3 evals/harbor/validate_subjects.py evals/harbor/subjects/*.json
python3 evals/harbor/validate_comparisons.py evals/harbor/comparisons/*.json
```

See [the Harbor developer guide](evals/harbor/DEVELOPERS.md) for authenticated
local trials, fixture construction, result paths, and rescoring. See
[the evaluation methodology](docs/EVALUATION.md) before interpreting results or
designing a new rubric.

For the packaged `capture-agent-issue` skill, run the focused stdlib helper checks
with `.venv/bin/python -m unittest discover -s evals/harbor/tests -p test_capture_agent_issue.py`.
They cover source-cutoff/authorship accounting, including OpenCode message
boundaries and outcomes recorded after a fork, and exclusive private packet writes;
they do not substitute for native skill-loading probes or model-based packet review.

## OpenCode catalog

Generate the catalog from the checked-out source into an empty directory:

```bash
python3 scripts/build_opencode_catalog.py --output /tmp/devcraft-site --tag v0.4.0
```

`--tag` must be `v<version>` and match `version` in both
`plugins/agentic-devcraft/.claude-plugin/plugin.json` and
`.codex-plugin/plugin.json`; a mismatch fails. `--revision` defaults to `git HEAD`
and must be a full commit SHA. The output is `opencode/skills/index.json` plus one
directory per skill containing every regular file of the canonical skill. Hidden
files, `__pycache__`, bytecode, and editor debris are skipped; symlinks are
refused. Nothing outside `plugins/agentic-devcraft/skills/` is copied. The output
is build output: never edit it or commit it as another skill tree.

The generator writes `release.json` into each skill, and the status skill reads it:

```json
{
  "schema": "agentic-devcraft-skill-release/v1",
  "skill": "status",
  "version": "0.4.0",
  "repository": "https://github.com/deinspanjer/agentic-devcraft",
  "source_path": "plugins/agentic-devcraft/skills/status",
  "revision": "<full commit SHA>"
}
```

Do not add a `release.json` to the source; generation fails if one exists. Changing
this shape means changing `skills/status/SKILL.md` in the same release. Packaging
checks are in `evals/harbor/tests/test_opencode_catalog.py`.

To try a generated catalog, serve the output directory over local HTTP and list
`http://127.0.0.1:<port>/opencode/skills/` under `skills` in a throwaway project's
`opencode.json`, using an isolated OpenCode home rather than your normal one.

### Publishing

Publishing changes repository settings and public content, so it needs the
maintainer's explicit go-ahead each time.

1. One-time: in the repository's **Settings → Pages**, set the source to
   **GitHub Actions**. Then in **Settings → Environments → github-pages**, add a
   deployment tag rule for `v*`: the workflow runs on the release tag, and that
   environment allows only the default branch unless a tag rule exists.
2. Give changed skills a new version in both plugin manifests and commit it.
3. Publish a GitHub release tagged `v<version>`, not a draft or prerelease. The
   workflow checks out that tag, generates and validates the catalog, and deploys
   only the generated site. Drafts, prereleases, and branch pushes do not publish.
4. Fetch `index.json` and a listed file from the deployed URL, expected to be
   `https://deinspanjer.github.io/agentic-devcraft/opencode/skills/`, and load one
   skill from it in an isolated OpenCode instance.

OpenCode refreshes a catalog skill when its `version` changes, so republishing
changed files under an old version does not reach existing users.

## Skill lifecycle

The `agent-instructions-cleanup` and `documentation-pattern-refactor` skills were
extracted from the existing `ai-tools-internal/.skills/` sources into the shared
plugin in version `0.3.0`. Keep their supporting scripts, references, and metadata
with the skill. The documentation baseline is bundled in `references/pattern_spec.md`;
the former machine-specific repository path is not a runtime dependency. References
to unavailable historical improvement-plan files were removed during extraction.
The cleanup skill was copied unchanged at extraction; documentation workflow changes
were limited to portable paths and host-aware invocation names. OpenCode support
later moved cleanup's Codex file-selection rules into its harness file, changed the
documentation helpers' default output to `<root>/.agents/artifacts/doc-pattern`
(the planner defaults to the divergence report's directory), and stopped treating a
nested `AGENTS.md` as a divergence.

Packaging validation covers both host manifests, skill frontmatter, and a temporary
fixture exercising section classification, hidden-directory exclusion, all three
plan levels, and preservation of the audited input files. These checks establish
packaging/helper behavior, not model-based effectiveness of the refactoring workflows.
Air consumes these same sources through its skill directory/registry support; see
[USERS.md](USERS.md#air-in-jetbrains-ides) for setup options.

1. Write one candidate source under `proposals/skills/`.
2. Add deterministic failure-mode fixtures and comparison declarations that
   reference that source directly.
3. Run repeated control and treatment trials; retain machine-readable evidence
   and a human interpretation.
4. Promote only after the evidence and compatibility review support release.
5. Move the source into the shared plugin payload and update both host manifests
   only when their schemas require a release change.

## Documentation placement rules

- `README.md` is the entry point: purpose, capability summary, and links.
- `USERS.md` owns installation, configuration, runtime behavior, and user
  troubleshooting.
- `DEVELOPERS.md` owns architecture, local setup, tests, extension practices,
  and documentation policy.
- `TODO.md` contains only actionable future work and unresolved design gaps.
- Focused evidence and methodology may live under `docs/` when linked from the
  appropriate root audience document.

Prefer one canonical explanation with audience-appropriate links over duplicate
procedures.

## Change-driven documentation matrix

Use this matrix during implementation review, architecture changes, module
refactors, and test or debug-tooling updates.

- CLI, environment, or runtime configuration changes update `USERS.md`, and
  `DEVELOPERS.md` when development setup is affected.
- User-visible workflow or actionable error behavior updates `USERS.md`.
- A major capability updates `README.md`, the relevant audience guides, and
  `TODO.md` only for unfinished follow-up work.
- Internal refactors and developer tooling/tests update `DEVELOPERS.md` when
  they change how contributors work.
- Deferred work and design questions update `TODO.md`, not current-behavior docs.
