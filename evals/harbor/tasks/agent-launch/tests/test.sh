#!/usr/bin/env bash
set -euo pipefail

mkdir -p /logs/verifier

if [[ -f /app/harbor-spike.txt ]] \
  && [[ "$(tr -d '\r\n' < /app/harbor-spike.txt)" == "agentic-devcraft harbor spike ok" ]]; then
  echo 1 > /logs/verifier/reward.txt
  exit 0
fi

echo 0 > /logs/verifier/reward.txt
exit 1
