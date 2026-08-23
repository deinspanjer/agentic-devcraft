#!/usr/bin/env bash
set -euo pipefail

mkdir -p /logs/verifier

if [[ -f /app/adaptive-ready ]] \
  && [[ "$(tr -d '\r\n' < /app/adaptive-ready)" == "ready" ]] \
  && [[ -f /app/adaptive-result ]] \
  && [[ "$(tr -d '\r\n' < /app/adaptive-result)" == "adaptive-controller-ok" ]]; then
  echo 1 > /logs/verifier/reward.txt
  exit 0
fi

echo 0 > /logs/verifier/reward.txt
exit 1
