#!/usr/bin/env bash
set -euo pipefail

mkdir -p /logs/verifier

if [[ -f /app/turn-1-complete ]] \
  && [[ "$(tr -d '\r\n' < /app/turn-1-complete)" == "ready" ]] \
  && [[ -f /app/harbor-conversation.txt ]] \
  && [[ "$(tr -d '\r\n' < /app/harbor-conversation.txt)" == "devcraft-resume-7f3c" ]]; then
  echo 1 > /logs/verifier/reward.txt
  exit 0
fi

echo 0 > /logs/verifier/reward.txt
exit 1
