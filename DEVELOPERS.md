# Developing Agentic Devcraft

## Repository structure

- `plugins/agentic-devcraft/` is the single released plugin payload shared by
  the Claude and Codex marketplaces.
- `proposals/skills/` contains unreleased skill sources under evaluation.
- `evals/harbor/` contains the local evaluation harness, fixtures, declarations,
  deterministic verifiers, and committable evidence.
- `evals/harbor/jobs/` contains ignored private trial artifacts.
- `openspec/` records capability specifications and completed change history.

Do not copy one skill into separate host-specific trees. A candidate has one
source under `proposals/skills/<name>/`; graduation moves that directory into
`plugins/agentic-devcraft/skills/<name>/`, where both marketplaces publish it
through the same plugin payload.

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
They cover source-cutoff/authorship accounting and exclusive private packet writes;
they do not substitute for native skill-loading probes or model-based packet review.

## Skill lifecycle

The `agent-instructions-cleanup` and `documentation-pattern-refactor` skills were
extracted from the existing `ai-tools-internal/.skills/` sources into the shared
plugin in version `0.3.0`. Keep their supporting scripts, references, and metadata
with the skill. The documentation baseline is bundled in `references/pattern_spec.md`;
the former machine-specific repository path is not a runtime dependency. References
to unavailable historical improvement-plan files were removed during extraction.
The cleanup skill was copied unchanged; documentation workflow changes are limited
to portable paths and host-aware invocation names.

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
