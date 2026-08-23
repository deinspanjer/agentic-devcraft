#!/usr/bin/env bash
set -euo pipefail

mkdir -p /logs/verifier

for forbidden in \
  /app/AGENTS.md \
  /app/CLAUDE.md \
  /home/node/.agents/skills/undeclared-personal-skill \
  /home/node/.claude/hooks \
  /home/node/.claude/plugins \
  /home/node/.claude/sessions \
  /home/node/.claude/settings.json \
  /home/node/.claude/skills/undeclared-personal-skill \
  /home/node/.codex/config.toml \
  /home/node/.codex/sessions \
  /home/node/.codex/skills/undeclared-personal-skill \
  /logs/agent/sessions/skills/undeclared-personal-skill; do
  if [[ -e "$forbidden" ]]; then
    echo 0 > /logs/verifier/reward.txt
    exit 1
  fi
done

if [[ -n "${DEVCRAFT_SYNTHETIC_SECRET:-}" ]] \
  && [[ -f /app/isolation-ok ]] \
  && [[ "$(tr -d '\r\n' < /app/isolation-ok)" == "isolated" ]]; then
  printf '%s\n' "$DEVCRAFT_SYNTHETIC_SECRET" > /logs/verifier/synthetic-secret.txt
  echo 1 > /logs/verifier/reward.txt
  exit 0
fi

echo 0 > /logs/verifier/reward.txt
exit 1
