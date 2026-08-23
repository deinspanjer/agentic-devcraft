# Harbor Evaluation Developer Guide

Harbor evaluations run locally in disposable Docker environments. They are not
GitHub Actions jobs. The pinned Python dependencies, agent versions, subject
revisions, and container images in this directory define the reproducible setup.

## Setup

From the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r evals/harbor/requirements.txt
```

Run deterministic checks before authenticated work:

```bash
.venv/bin/python -m unittest discover -s evals/harbor/tests -p 'test_*.py'
python3 evals/harbor/validate_subjects.py evals/harbor/subjects/*.json
python3 evals/harbor/validate_comparisons.py evals/harbor/comparisons/*.json
```

## Subscription authentication

### Codex

Harbor accepts a ChatGPT-authenticated Codex `auth.json` through
`CODEX_AUTH_JSON_PATH`. The runner defaults to `$CODEX_HOME/auth.json` or
`~/.codex/auth.json`. Harbor uploads it into temporary container state and removes
that state after the trial.

```bash
evals/harbor/run-spike.sh codex
CODEX_AUTH_JSON_PATH=/path/to/auth.json \
  evals/harbor/run-spike.sh codex gpt-5.6-sol
```

### Claude Code

Generate a subscription token once and store it outside the repository. On
macOS, the runner reads the `agentic-devcraft.claude-oauth` Keychain item unless
`CLAUDE_CODE_OAUTH_TOKEN` is already set.

```zsh
claude setup-token

read -rs 'token?Paste token: '
echo
security add-generic-password \
  -U \
  -a "$USER" \
  -s agentic-devcraft.claude-oauth \
  -w "$token"
unset token

evals/harbor/run-spike.sh claude-code
```

Generate and store a replacement the same way when the token expires. Set
`DEVCRAFT_CLAUDE_KEYCHAIN_SERVICE` to choose a different service name.

## Network prerequisite

Authenticated trials use Harbor's fail-closed Docker allowlist. The selected
Docker backend must pass Harbor's nftables capability probe. If it fails, update
or change the Docker backend and retry; use a compatible Linux host when the
local backend cannot enforce the policy. Do not bypass the probe or move Harbor
evaluations into CI merely to avoid the prerequisite.

## Harness probes

Run a one-shot agent launch:

```bash
evals/harbor/run-spike.sh codex gpt-5.6-sol
evals/harbor/run-spike.sh claude-code opus
```

Run a fixed resumed session or adaptive testing-agent conversation:

```bash
evals/harbor/run-spike.sh codex gpt-5.6-sol conversation
evals/harbor/run-spike.sh codex gpt-5.6-sol adaptive
```

Run the disposable-home privacy and isolation probe:

```bash
evals/harbor/run-spike.sh codex gpt-5.6-sol isolation
```

## Subject compatibility

Subject declarations under `subjects/` contain the pinned source, supported and
sourced-unsupported hosts, network hosts, installation actions, configuration,
discovery check, and use probe.

```bash
evals/harbor/run-spike.sh codex gpt-5.6-sol subject devcraft-status
evals/harbor/run-spike.sh claude-code opus subject devcraft-status
```

A pass requires setup, discovery, and use. Installation alone cannot pass.

## Behavioral comparisons

Comparison declarations under `comparisons/` pair fresh arms that may differ only
in their declared skill and hook inputs. Candidate Devcraft skills come from
`proposals/skills/`; marketplace installation is outside the behavioral score.

```bash
DEVCRAFT_COMPARISON_REPETITIONS=1 \
  evals/harbor/run-spike.sh codex gpt-5.6-sol comparison cold-read
```

One repetition is a plumbing check. Use repeated interleaved trials for
comparative evidence. Keep deterministic verification separate from optional
arm-blinded qualitative judgment.

## Engineering benchmarks

### Date-filter calibration

Build and validate the committed tiny Python CLI fixture, then inspect the local
matrix without using subscription capacity:

```bash
.venv/bin/python -m evals.harbor.run_engineering_benchmark \
  --scenario date-filter build-fixture
.venv/bin/python -m evals.harbor.run_engineering_benchmark \
  --scenario date-filter validate
.venv/bin/python -m evals.harbor.run_engineering_benchmark \
  --scenario date-filter plan
```

Run one repetition first as plumbing evidence. Authenticated execution still
requires the explicit gate:

```bash
CODEX_AUTH_JSON_PATH=/path/to/auth.json \
  .venv/bin/python -m evals.harbor.run_engineering_benchmark \
  --scenario date-filter run --execute --repetitions 1
```

The declared matrix contains three direct arms with three repetitions. It omits
orchestration because delegation is not justified by this task's size. Review
the one-repetition evidence before approving the full calibration matrix.

### Vanilla port benchmark

The first benchmark builds a sanitized fixture from the public
[Codex Cost Meter source](https://github.com/deinspanjer/codex-cost-meter/tree/0b5eb56978c91e1fa1631d9ec84ac3767e8fce79)
at the revision pinned in
[`manifest.json`](benchmarks/vanilla-port/manifest.json), then runs Codex-only,
code-only arms.

```bash
.venv/bin/python -m evals.harbor.run_engineering_benchmark build-fixture \
  --source /path/to/codex-cost-meter \
  --output /tmp/vanilla-port-review

.venv/bin/python -m evals.harbor.run_engineering_benchmark validate
.venv/bin/python -m evals.harbor.run_engineering_benchmark plan
```

After reviewing the plan and explicitly approving subscription use:

```bash
CODEX_AUTH_JSON_PATH=/path/to/auth.json \
  .venv/bin/python -m evals.harbor.run_engineering_benchmark run --execute
```

Use `--arm <id>` for a diagnostic arm or `--repetitions <n>` only after reviewing
the resulting schedule and usage ceiling again.

Rescore retained snapshots without rerunning an agent:

```bash
.venv/bin/python -m evals.harbor.run_engineering_benchmark rescore \
  /path/to/trial.json \
  /path/to/snapshots/initial \
  /path/to/snapshots/extension \
  /path/to/rescores/verifier-v2.json
```

## Evidence and privacy

Raw jobs, trajectories, snapshots, controller records, and subject workspaces are
written under `jobs/` and ignored. They may contain private subject-authored text.
Committed reports and baselines must be recursively redacted and independently
understandable without the raw directory.

Read [the project methodology](../../docs/EVALUATION.md) before adding a rubric
or interpreting token, file-count, interaction, orchestration, or cost evidence.
