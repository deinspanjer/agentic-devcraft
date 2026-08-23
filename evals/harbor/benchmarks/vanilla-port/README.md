# Codex Cost Meter Python Prototype

`rollout_stats.py` reports token usage, model attribution, elapsed agent time, and estimated API-list-price cost for one Codex rollout and its descendants.

The Python implementation and its embedded self-test are the source of truth for the report behavior in this repository.

```bash
python3 rollout_stats.py --self-test
python3 rollout_stats.py root --codex-home fixtures/codex-home
python3 rollout_stats.py root --codex-home fixtures/codex-home --json
```

Keep this project focused on a locally runnable report. Packaging, signing, release publication, schedulers, and platform integration are outside the requested work.
