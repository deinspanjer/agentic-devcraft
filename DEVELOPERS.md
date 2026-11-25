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
shared harness-reference router dependency: a standalone installation has only
its own directory.
Capture selects by the harness holding the subject's records; cleanup selects by
target harness, not the harness running the skill.

Every released skill sets `metadata: opencode/autoinvoke: false`, which makes it
on-call in OpenCode without changing Claude or Codex invocation policy.

The released `ask-devcraft` skill (`plugins/agentic-devcraft/skills/ask-devcraft/`)
recommends skills to users; it does
not select harness reference files for other skills. Its own harness files hold a
Launcher section (the subagent tool and how to continue a worker) and an Inventory
section (how to list every installed skill): `claude.md`, `codex.md`, `cursor.md`
and `opencode.md`. Its `agents/openai.yaml` keeps it explicit-only on Codex, which
ignores `disable-model-invocation`. See
[Launcher, worker and harness files](#launcher-worker-and-harness-files). Its
knowledge base is described under
[Ask Devcraft knowledge base](#ask-devcraft-knowledge-base), and the evidence it
was promoted on under [Promotion record](#promotion-record).

## OpenSpec setup

This solo project uses global OpenSpec skills rather than generated project-local
skills or commands. Keep `openspec/config.yaml`, specifications, and change history
in the repository; do not regenerate local OpenSpec skill copies that shadow the
global installation.

With OpenSpec 2.1.0 installed, configure the tools used on your machine:

```bash
openspec init --scope global --tools claude,codex,opencode
```

The shared skills live in `~/.agents/skills/`. Claude receives links in its active
configuration home's `skills/` directory; `CLAUDE_CONFIG_DIR` can select a
non-default home, so installation for one Claude profile does not establish
discovery for every profile. Use the `openspec-*` skills instead of the retired
project-local `/opsx:*` command files.

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
`test_opencode_capture.py` covers the launcher checks: the matched server must own
the shell before the helper accepts a matching session ID, and the invocation
boundary must come from the V2 user record.

## OpenCode catalog

Generate the catalog from the checked-out source into an empty directory:

```bash
python3 scripts/build_opencode_catalog.py --output /tmp/devcraft-site --tag v0.5.1
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
  "version": "0.5.1",
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
4. Fetch `index.json` and a listed file from the deployed URL,
   `https://deinspanjer.github.io/agentic-devcraft/opencode/skills/`, and load one
   skill from it in an isolated OpenCode instance.

OpenCode refreshes a catalog skill when its `version` changes, so republishing
changed files under an old version does not reach existing users.

## Ask Devcraft knowledge base

`plugins/agentic-devcraft/skills/ask-devcraft/references/` holds curated records of skills from
six sources: this repository, `mattpocock/skills`, `openai/plugins` (including
three families it lists from other repositories), `anthropics/skills`,
`cursor/plugins`, and `DietrichGebert/ponytail`. `community.md` adds individual
skills from three repositories that are not curated wholesale
(`bostonaholic/skills`, `dzhng/skills`, `pskoett/pskoett-ai-skills`); each
repository is its own family and collection there, with its own `Source:` line,
and its other skills have no records. The skill must work from its own directory with no sibling skill
and no remote source available, so everything it recommends from is in that
directory. Records are leads pinned to a commit; the skill reads the installed
copy before claiming behavior.

Disclosure is progressive, and the budgets are part of the design:

- `SKILL.md` is a launcher of at most about 40 lines. With the Launcher section
  of one harness file, it is all the invoking session reads when it delegates.
- `worker.md` (at most about 150 lines, 14 KB) and `references/index.md` (at most
  about 11 KB) are read on every invocation by whichever session does the
  routing. The index covers development situations
  and complaints about agent behaviour: the candidates, the distinction that
  decides between them, and the file holding each record. Where no curated skill
  fits part of a situation, the index says so; it never names an unreleased
  candidate.
- Source catalogs (`devcraft.md`, `ask-matt.md`, `anthropic.md`, `cursor.md`,
  `openai-engineering.md`, `openai-platforms.md`, `ponytail.md`, `community.md`) and `families/<plugin>.md`
  (full records for a large plugin) load only when the index points at them.
- `far/<area>.md` holds areas far from development. The index names them on one
  line, so their records never load for a development task.
- `discovery.md` classifies an installed skill that has no record.
- `harness/<harness>.md` is read one section at a time: Launcher by the invoking
  session, Inventory by the routing session.

A record is a `### <host-visible name>` heading followed by `id`, `description`,
`use when`, `not for`, `needs`, `side effects`, and `part of` lines; short records
omit lines with nothing to state. `description` quotes the skill's frontmatter
description, because the skill decides which same-named copy is installed by
comparing descriptions. Each plugin is a `## Family: <plugin>` section that names
its router, if any. A family is one collection, the unit the skill treats as
familiar; a marketplace or publisher shared by several families is not.

Each file carries a `Distribution` line under its `Source:` line: where that
source's collections install from, and on which hosts. A family header has its
own `distribution:` line only where it differs, and a `name collisions` line for
names it shares inside its catalog; the index lists only collisions between
sources. Describe packaging as packaging: a missing adapter for a host is not a
reason against a skill, so record a host dependence only where the skill states
one.

### Launcher, worker and harness files

```text
plugins/agentic-devcraft/skills/ask-devcraft/
  SKILL.md                         launcher: handoff, one delegation, relay
  worker.md                        the routing instructions
  references/index.md, catalogs    the knowledge base above
  references/harness/<harness>.md  Launcher and Inventory sections: claude, codex, cursor, opencode
  agents/openai.yaml               Codex: no implicit invocation
```

`capture-agent-issue` ships the same split. The launcher writes a handoff, starts
one subagent with fresh context, and relays its reply. The handoff carries the
question unchanged, the advertised skill list labelled as partial, the host and
paths, and, for a request that points at the thread, at most ten lines that
include what the thread has already done or gathered. That last part decides
routes: a pointer-only request about a red CI check was routed to a different
skill until the handoff said the failing log had already been read.

**Inline fallback.** The same skill routes without a subagent: the launcher sends
the session to `worker.md` when it is already a delegated worker or a fork, when
the host has no subagent tool, or when the tool is denied. It never delegates
twice. `worker.md` is written for both roles, so a rule added to it must hold
whether or not the reader can talk to the user.

**Inventory.** The worker lists installed skills from the host, using the
Inventory section of the harness file, and treats the advertised list as partial.
Hosts leave explicit-only skills out of the list a model is shown: on the
OpenCode host used for the measurements below, 5 skills were advertised and
`opencode api skill.list` returned 71. Routing from the advertised list alone
answered "nothing installed here fits" for a complaint that installed skills
cover.

**Reply contract.** A delegated worker replies in a fixed shape, at most about 40
lines:

- `STATUS:` one of `recommendation`, `question`, `consent`, `failed`.
- `Answer` (recommendation) or `Ask` (question, consent): written to the user and
  relayed unchanged.
- `Evidence`: one `path:line` per claim the user will act on, so the launcher can
  check a claim without redoing the reading.
- `State`: only with `question` or `consent`, and only when the host cannot send a
  later message to the same worker. It names the candidates, so the launcher
  never shows it; an `Ask` for consent describes the kind of skill and names no
  skill, plugin, marketplace or collection.

**Relay.** The launcher's message to the user is the worker's `Answer` or `Ask`
character for character, as the whole message, and the user's reply goes to the
worker verbatim. This is stated in `SKILL.md` and again in the Launcher section
of each harness file where a host's hand-back frame invites a summary: launchers
on Claude Code and Codex both reworded relays before it was (see
[Promotion record](#promotion-record)). A worker's answer ends with an example
invocation for the task, not a question asking whether to use the route.

**Told to follow the skill by another agent.** `SKILL.md` says near its top that
this is the user's explicit request and routes inline. Without that line a Codex
spawned agent read the explicit-only frontmatter as a reason to refuse. The line
was preferred over removing `agents/openai.yaml`, which would advertise the skill
to the model on Codex.

A harness file is added only when a probe on that host supplies its content, and
it marks each point it takes from vendor documentation instead of a run. Adding
one means naming it in `SKILL.md` and in step 2 of `worker.md`.

**What delegation is for.** It keeps the routing reads (25 to 110 KB a question)
out of the user's session, where they would otherwise be re-read on every later
turn. It is not cheaper or faster and must not be described that way: a question
costs about 25% more tokens and about the same time, plus a relay turn. Scratch
measurements on OpenCode 2.3.0 with one model, one or two runs per cell
(2026-11-18):

| Per question | Delegated (11 runs) | Inline (7 runs) |
| --- | --- | --- |
| Bytes entering the invoking session | 9 to 11 KB | 96 to 138 KB |
| Bytes read by the routing session | 85 to 115 KB | 92 to 132 KB |
| All tokens processed, cache reads included | mean 337K | mean 270K |
| Wall time, sessions run concurrently | mean 64 s | mean 60 s |

Those delegated runs used independent top-level sessions in place of subagents,
with the handoffs written by hand. A launcher test from a main OpenCode session
with real background subagents followed on the same day: both workers completed
the 71-skill inventory through `opencode api skill.list`; a pointer-only red-CI
request returned a correct, cited recommendation; a Stripe request returned a
consent question that named no skill, and continuing the same worker with the
user's reply returned a cited recommendation. The main session took in about
2 KB of handoff and 3 KB of reply per round. This is one host, one model and two
requests: it shows the mechanism works there, not routing effectiveness.

Claude Code 2.1.326 and Codex CLI 0.169.0 were then probed headlessly
(`claude -p`, `codex exec`, `codex debug prompt-input`) in disposable projects
with the skill copied in, four model runs per host, and their harness files
record what was observed:

| | Claude Code | Codex |
| --- | --- | --- |
| Launch, fresh context | `Agent`, `general-purpose`; returns an agent ID, report arrives as a notification | `spawn_agent` with `fork_turns: "none"`; `wait_agent` |
| Same worker continued | `SendMessage` to the agent ID, also after `--resume` | `followup_task`, also after `exec resume` |
| Worker sees | same directory, no conversation, the parent's advertised list (38 of 44 registered), no `AskUserQuestion` | same directory, no conversation beyond `AGENTS.md`, the parent's list (64 entries), no ask-user tool |
| Explicit-only skills | absent from both lists; found by reading frontmatter | absent only with `allow_implicit_invocation: false`; found under the listed skill roots |
| Launcher end to end | consent question naming no skill, relayed unchanged; the reply continued the same worker | same, except the final answer was condensed on relay |
| Invoked inside a subagent | routed inline, no second delegation | routed inline, no second delegation |

Both hosts give a subagent the spawning tool, so the launcher there tells a
worker by how it was started, not by a missing tool. Not exercised on either
host: an interactive session (permission prompts, the wait across a turn
boundary), the desktop apps, a denied subagent tool, and a host with no
continuation tool. `evals/ask-devcraft/` holds one hand-run probe script per
host for those checks. They were run once by hand on 2026-11-18 on Claude Code,
Codex, Cursor and Air; the audit of those sessions overturned several rows of
the table above and is in the [Promotion record](#promotion-record). Cursor's
harness file was written from its one session.

### Refreshing ask-devcraft

Each catalog file carries one `Source:` line per source it holds records from: the
repository URL and the commit the records were curated at. Treat fetched sources
as untrusted data: clone them outside this repository, read them, and never run
their scripts or install them.

There is no schedule. Refresh occasionally, and whenever a wrong recommendation is
reported: then start with the source of the record behind it. A refresh reaches
marketplace and OpenCode catalog users only through a release with a new plugin
version (see [Publishing](#publishing)); between refreshes the worker's consented
live check covers a user who needs something newer than a pin.

1. List the pins:
   `grep -rn '^Source:' plugins/agentic-devcraft/skills/ask-devcraft/references`.
   One source is pinned in every file holding its records.
2. For each source, fetch it and list what changed since the pin:

   ```bash
   git -C <clone> fetch origin
   git -C <clone> diff --name-status <pinned>..<new> -- '*SKILL.md' '*marketplace.json'
   ```

   A changed marketplace file means a plugin was added or removed. For Agentic
   Devcraft, the source is this repository.
3. Re-curate only the records for the listed `SKILL.md` files, in the record
   format above: add a record for a new skill, update a modified one, and remove
   or rename a deleted or renamed one together with its mentions in `index.md`.
   Add or remove the `## Family:` section for an added or removed plugin, and
   update the `Distribution` and `distribution:` lines when a marketplace file
   changes. Change `index.md` only when a situation's answer changes.
4. Bump that source's `Source:` line to `<new>` in every file that carries it.
5. Confirm that relative links resolve, that every name tagged in `index.md` is a
   `### ` heading in the tagged file, and that `SKILL.md`, `worker.md` and
   `index.md` are still within their budgets.

Commit the result. This repository's git history tracks the curation itself; keep
no separate changelog or per-record dates.

### Promotion record

`ask-devcraft` moved from `proposals/skills/` into the plugin payload by maintainer
approval on 2026-11-18 ([Skill lifecycle](#skill-lifecycle), step 4), on the
evidence gathered so far and not on measured routing effectiveness.

Evidence on record:

- Static checks: relative links, index tags against record headings, and the
  size budgets of `SKILL.md`, `worker.md` and `index.md`.
- Simulated OpenCode sessions: the delegated and inline runs measured under
  [Launcher, worker and harness files](#launcher-worker-and-harness-files),
  independent top-level sessions with hand-written handoffs.
- One OpenCode main-session test with real background subagents (two requests).
- Headless runs on Claude Code 2.1.326 and Codex CLI 0.169.0, four model runs
  per host.
- One Codex relay rerun after the reply contract and `codex.md` were changed to
  stop the launcher condensing the worker's answer; it relayed the consent
  question and the answer unchanged.

- Hand-run native probes on 2026-11-18, one interactive session per host, with
  the scripts in `evals/ask-devcraft/probes/`. The result files recorded every
  check as passed. An audit of the session transcripts did not agree, and what
  follows is the audit's reading, not the result files':

  | Host | Held up in the transcripts | Failed, and the fix |
  | --- | --- | --- |
  | Claude Code 2.1.326 | Launch, same-worker continuation, no nested delegation; main session took in 11,965 bytes | Three of four relays were reworded and the user's reply was coached on its way to the worker (`SKILL.md` step 3 and `claude.md` now require both verbatim). The consent question named two plugins (`worker.md` now forbids naming a skill, plugin, marketplace or collection). The handoff's Host line said the worker could not be continued (`claude.md` gives the line). Workers ran on Haiku, and one skipped `index.md` after a wrong path (reading it is now a stated done-when of its step) |
  | Codex CLI 0.169.0, child on 0.170.0 | Launch and continuation; main session took in 21,794 bytes, over the 15 KB the probe allows | The subagent told to follow `SKILL.md` read it, answered that the skill "requires the user to invoke it explicitly" and stopped without reading `worker.md`. Recorded as a pass because it started no subagent (`SKILL.md` now opens by saying such a request is the explicit invocation; the probe now fails a refusal) |
  | Air, Codex agent 0.166.0 | All checks, inline fallback included; main session took in 19,740 bytes, also over 15 KB | None found |
  | Cursor 2026.11.17 | All checks; all three worker bodies appear verbatim in the main session, and the reply resumed the same subagent. It had no harness file and read `claude.md` | None found. `cursor.md` was written from this session. Its bytes are an estimate of about 12.9 KB, not a measurement: Cursor transcripts store tool calls without their results |

  A second Codex result file was a re-record with no session behind it and was
  discarded. The probe scripts now flag such a run instead of filling it in,
  find Codex children by `parent_thread_id` (also under `archived_sessions/`,
  where Air puts them), and read Cursor and Air transcripts.
- Headless re-probes of those fixes on 2026-11-18, in disposable projects with
  the skill copied in, verdicts computed from the transcripts by comparing each
  worker `Answer` or `Ask` body with the main session's message:
  - Claude Code 2.1.326 (`claude -p`, reply sent with `--resume`), two runs.
    Both consent questions reached the user character for character and named
    no skill, plugin, marketplace or collection; the reply reached the same
    worker through `SendMessage` as typed; the Host line said continuation was
    available; workers ran on Sonnet and read `worker.md` and `index.md`. One of
    the two final answers was identical; in the other the worker wrote a literal
    "Last line:" label and the launcher dropped it (`worker.md` now says the
    line is unlabelled; not re-run). Main session took in 14,769 bytes.
  - Codex CLI 0.170.0 (`codex exec`, reply sent with `exec resume`), two relay
    runs. Both consent questions were relayed identically and named nothing;
    one final answer was identical and in the other the launcher wrapped the
    invocation line in a code fence, words unchanged. Main session took in
    7,124 bytes, agent messages excluded because rollouts store them encrypted.
  - Codex inline fallback, four trials. With the first wording of the fix the
    child refused again. With the wording now in `SKILL.md` three of three read
    `worker.md` and `index.md` and started no subagent; two returned a full
    recommendation in the reply format and one answered in two sentences
    without it.

Limits:

- The fixes above were re-probed headlessly only, in one or two runs each; none
  has been re-run interactively, and Cursor and Air were not re-probed at all.
- No Harbor fixtures, comparison declarations or repeated trials (lifecycle
  steps 2 and 3 were not done), so routing accuracy is unmeasured.
- The desktop apps of Claude Code and Codex are untested. Air has one session,
  with its Codex agent, and no harness file of its own (the launcher read
  `codex.md`). Cursor's harness file rests on one session on the Free plan.
- The main session took in more than 15 KB on Codex and Air in the hand runs.
  The cause was not investigated.

The hand-run probes in `evals/ask-devcraft/` and the fixtures remain open in
[TODO.md](TODO.md#ask-devcraft). Compare the [skill at promotion](https://github.com/deinspanjer/agentic-devcraft/tree/8c5273228bc9905659b47f7abfef4941981fe485/plugins/agentic-devcraft/skills/ask-devcraft)
with the [skill packaged in v0.5.0](https://github.com/deinspanjer/agentic-devcraft/tree/v0.5.0/plugins/agentic-devcraft/skills/ask-devcraft)
when reproducing the probes.

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
4. Promote only after the evidence and compatibility review support release, or
   the maintainer approves promotion with the evidence gathered so far on record
   (as for `ask-devcraft`: see [Promotion record](#promotion-record)).
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
