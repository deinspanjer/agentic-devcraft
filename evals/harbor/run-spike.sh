#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
harbor_bin="${HARBOR_BIN:-$repo_root/.venv/bin/harbor}"
jobs_dir="${HARBOR_JOBS_DIR:-$repo_root/evals/harbor/jobs}"
agent="${1:-}"
model="${2:-}"
mode="${3:-one-shot}"
subject="${4:-devcraft-status}"
harbor_agent="$agent"
harbor_args=()

usage() {
  echo "usage: $0 <codex|claude-code> [model] [one-shot|conversation|adaptive|isolation|subject|comparison] [subject-or-comparison]" >&2
}

load_claude_token() {
  if [[ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" && -x /usr/bin/security ]]; then
    local keychain_service token
    keychain_service="${DEVCRAFT_CLAUDE_KEYCHAIN_SERVICE:-agentic-devcraft.claude-oauth}"
    if token="$(/usr/bin/security find-generic-password -a "${USER:?USER is required for Keychain lookup}" -s "$keychain_service" -w 2>/dev/null)"; then
      export CLAUDE_CODE_OAUTH_TOKEN="$token"
      unset token
    fi
  fi
  if [[ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]]; then
    echo "Claude OAuth token not found in CLAUDE_CODE_OAUTH_TOKEN or macOS Keychain." >&2
    echo "Generate one with 'claude setup-token'; see evals/harbor/DEVELOPERS.md for storage instructions." >&2
    exit 2
  fi
  export CLAUDE_FORCE_OAUTH=1
  unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN
}

if [[ "$agent" != "codex" && "$agent" != "claude-code" ]]; then
  usage
  exit 2
fi

case "$mode" in
  one-shot)
    task_path="$repo_root/evals/harbor/tasks/agent-launch"
    ;;
  conversation)
    task_path="$repo_root/evals/harbor/tasks/session-resume"
    harbor_args+=(--resume-trajectory)
    ;;
  adaptive)
    task_path="$repo_root/evals/harbor/tasks/adaptive-controller"
    ;;
  isolation)
    task_path="$repo_root/evals/harbor/tasks/isolation"
    ;;
  subject)
    task_path="$repo_root/evals/harbor/tasks/subject-smoke"
    ;;
  comparison)
    task_path=""
    ;;
  *)
    usage
    exit 2
    ;;
esac

if [[ ! -x "$harbor_bin" ]]; then
  echo "Harbor is not installed at $harbor_bin" >&2
  echo "Run: python3 -m venv .venv && .venv/bin/python -m pip install -r evals/harbor/requirements.txt" >&2
  exit 2
fi

case "$agent" in
  codex)
    model="${model:-${DEVCRAFT_CODEX_MODEL:-gpt-5.6-sol}}"
    export CODEX_AUTH_JSON_PATH="${CODEX_AUTH_JSON_PATH:-${CODEX_HOME:-$HOME/.codex}/auth.json}"
    if [[ ! -r "$CODEX_AUTH_JSON_PATH" ]]; then
      echo "Codex auth file is not readable: $CODEX_AUTH_JSON_PATH" >&2
      exit 2
    fi
    unset CODEX_FORCE_AUTH_JSON OPENAI_API_KEY
    model_hosts=(chatgpt.com)
    ;;
  claude-code)
    model="${model:-${DEVCRAFT_CLAUDE_MODEL:-opus}}"
    load_claude_token
    model_hosts=(api.anthropic.com statsig.anthropic.com sentry.io)
    ;;
esac

if [[ "$mode" == "adaptive" ]]; then
  load_claude_token
  export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
  harbor_agent="evals.harbor.adaptive_agent:AdaptiveAgent"
  controller_policy="Inspect the latest response. If it reports that adaptive-ready is ready, send a user message asking the agent to create /app/adaptive-result containing exactly adaptive-controller-ok. Otherwise stop and explain why."
  harbor_args+=(
    --agent-kwarg "subject_agent=$agent"
    --agent-kwarg "controller_policy=$controller_policy"
  )
fi

if [[ "$mode" == "subject" ]]; then
  subject_path="$repo_root/evals/harbor/subjects/$subject.json"
  python3 "$repo_root/evals/harbor/validate_subjects.py" "$subject_path"
  export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
  harbor_agent="evals.harbor.subject_agent:SubjectLifecycleAgent"
  harbor_args+=(
    --agent-kwarg "subject_agent=$agent"
    --agent-kwarg "subject_path=$subject_path"
  )
  while IFS= read -r host; do
    harbor_args+=(--allow-agent-host "$host")
  done < <(python3 -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["network_hosts"][sys.argv[2]]))' "$subject_path" "$agent")
  for host in "${model_hosts[@]}"; do
    harbor_args+=(--allow-agent-host "$host")
  done
  harbor_args+=(--n-attempts "${DEVCRAFT_SUBJECT_ATTEMPTS:-1}")
fi

if [[ "$mode" == "isolation" ]]; then
  synthetic_secret="devcraft-synthetic-$(/usr/bin/uuidgen)"
  isolation_jobs="$jobs_dir/isolation-$(date +%Y%m%d-%H%M%S)"
  harbor_args+=(--verifier-env "DEVCRAFT_SYNTHETIC_SECRET=$synthetic_secret")
else
  isolation_jobs="$jobs_dir"
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker is unavailable; start Docker and ensure this process can access its socket." >&2
  exit 2
fi

if [[ "$mode" == "subject" || "$mode" == "comparison" ]] && ! "$repo_root/.venv/bin/python" -c '
import sys
from harbor.environments.docker.docker import DockerEnvironment
raise SystemExit(0 if sys.platform == "linux" or DockerEnvironment._egress_control_kernel_support() else 1)
'; then
  echo "This Docker backend cannot enforce Harbor network allowlists." >&2
  echo "Update or change the Docker backend, then rerun the capability probe; see evals/harbor/DEVELOPERS.md." >&2
  exit 2
fi

if [[ "$mode" == "comparison" ]]; then
  export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
  comparison_args=("$agent" "$model" "$subject")
  if [[ -n "${DEVCRAFT_COMPARISON_REPETITIONS:-}" ]]; then
    comparison_args+=(--repetitions "$DEVCRAFT_COMPARISON_REPETITIONS")
  fi
  if [[ -n "${DEVCRAFT_COMPARISON_ARM:-}" ]]; then
    comparison_args+=(--arm "$DEVCRAFT_COMPARISON_ARM")
  fi
  exec "$repo_root/.venv/bin/python" -m evals.harbor.run_comparison "${comparison_args[@]}"
fi

mkdir -p "$isolation_jobs"

harbor_command=(
  "$harbor_bin" run
  --path "$task_path"
  --agent "$harbor_agent"
  --model "$model"
  --jobs-dir "$isolation_jobs"
  --n-concurrent 1
  --delete
  "${harbor_args[@]}"
  --yes
)

if [[ "$mode" != "isolation" && "$mode" != "subject" ]]; then
  exec "${harbor_command[@]}"
fi

if [[ "$mode" == "subject" ]]; then
  "${harbor_command[@]}"
  leaked_containers=0
  while IFS= read -r result; do
    session_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["id"])' "$result")"
    if docker ps --all --quiet --filter "name=$session_id" | rg -q .; then
      echo "Harbor did not tear down subject environment $session_id." >&2
      leaked_containers=1
    fi
  done < <(find "$jobs_dir" -path '*subject-smoke__*/result.json' -mmin -30 -type f)
  exit "$leaked_containers"
fi

synthetic_home="$(mktemp -d "${TMPDIR:-/tmp}/agentic-devcraft-home.XXXXXX")"
host_docker_config="${DOCKER_CONFIG:-$HOME/.docker}"
trap 'rm -rf "$synthetic_home"' EXIT
mkdir -p \
  "$synthetic_home/.agents/skills/undeclared-personal-skill" \
  "$synthetic_home/.claude/hooks" \
  "$synthetic_home/.claude/plugins" \
  "$synthetic_home/.claude/sessions" \
  "$synthetic_home/.claude/skills/undeclared-personal-skill" \
  "$synthetic_home/.codex/sessions" \
  "$synthetic_home/.codex/skills/undeclared-personal-skill"
touch \
  "$synthetic_home/.agents/skills/undeclared-personal-skill/SKILL.md" \
  "$synthetic_home/.claude/settings.json" \
  "$synthetic_home/.claude/skills/undeclared-personal-skill/SKILL.md" \
  "$synthetic_home/.codex/config.toml" \
  "$synthetic_home/.codex/skills/undeclared-personal-skill/SKILL.md" \
  "$synthetic_home/AGENTS.md" \
  "$synthetic_home/CLAUDE.md"

HOME="$synthetic_home" DOCKER_CONFIG="$host_docker_config" "${harbor_command[@]}"

if rg -l -F "$synthetic_secret" "$isolation_jobs"; then
  echo "Synthetic secret remained in persisted Harbor output." >&2
  exit 1
fi
if ! rg -q -F '[REDACTED]' "$isolation_jobs"; then
  echo "Harbor output did not contain evidence of synthetic-secret redaction." >&2
  exit 1
fi

echo "Isolation and result redaction verified: $isolation_jobs"
