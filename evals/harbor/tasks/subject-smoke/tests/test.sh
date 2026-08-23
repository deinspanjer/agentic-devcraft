#!/usr/bin/env bash
set -euo pipefail

mkdir -p /logs/verifier

outcome="$(node -p 'require("/logs/agent/subject-lifecycle.json").outcome')"
if [[ "$outcome" == "unsupported" ]]; then
  echo 0 > /logs/verifier/reward.txt
  exit 0
fi

if node -e '
  const report = require("/logs/agent/subject-lifecycle.json");
  const stages = report.stages;
  const setup = stages.setup;
  if (report.outcome !== "passed" || report.isolation?.status !== "passed") process.exit(1);
  if (setup.status !== "passed" || !setup.revision || !setup.digest?.value) process.exit(1);
  if (stages.discovery.status !== "passed" || stages.use.status !== "passed") process.exit(1);
'; then
  echo 1 > /logs/verifier/reward.txt
  exit 0
fi

echo 0 > /logs/verifier/reward.txt
exit 1
