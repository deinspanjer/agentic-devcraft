from statistics import median
from typing import Any


METRICS = (
    "correctness",
    "false_positives",
    "workflow_adherence",
    "duration_sec",
    "turns",
    "tool_calls",
    "input_tokens",
    "cache_tokens",
    "output_tokens",
)


def summarize_comparison(trials: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for trial in trials:
        grouped.setdefault(trial["arm"], []).append(trial)

    arms: dict[str, Any] = {}
    for arm, repetitions in grouped.items():
        metrics: dict[str, Any] = {}
        for metric in METRICS:
            raw = [trial.get(metric) for trial in repetitions]
            numeric = [
                isinstance(value, (int, float)) and not isinstance(value, bool)
                for value in raw
            ]
            available = [value for value, present in zip(raw, numeric) if present]
            availability = (
                "complete" if len(available) == len(raw)
                else "partial" if available
                else "unavailable"
            )
            metrics[metric] = {
                "availability": availability,
                "values": [
                    {"available": present, "value": value if present else None}
                    for value, present in zip(raw, numeric)
                ],
                "median": median(available) if available else None,
            }
        arms[arm] = {"trials": repetitions, "metrics": metrics}
    return {"arms": arms, "aggregate_score": None}


def _numeric_measures(value: Any, prefix: str = "") -> dict[str, float | int | None]:
    if isinstance(value, dict):
        if set(value) == {"available", "value"}:
            return {prefix: value["value"] if value["available"] else None}
        result = {}
        for key, item in value.items():
            result.update(_numeric_measures(item, f"{prefix}.{key}" if prefix else key))
        return result
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return {prefix: value}
    return {}


def summarize_engineering_comparison(
    trials: list[dict[str, Any]], *, plumbing: bool = False
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for trial in trials:
        grouped.setdefault(trial["provenance"]["arm"], []).append(trial)
    arms = {}
    for arm, repetitions in grouped.items():
        stages = {}
        stage_names = sorted({stage for trial in repetitions for stage in trial.get("stages", {})})
        for stage in stage_names:
            per_trial = [
                _numeric_measures(trial.get("stages", {}).get(stage, {}))
                for trial in repetitions
            ]
            measures = {}
            for name in sorted({key for item in per_trial for key in item}):
                raw = [item.get(name) for item in per_trial]
                available = [value for value in raw if isinstance(value, (int, float)) and not isinstance(value, bool)]
                measures[name] = {
                    "availability": "complete" if len(available) == len(raw) else "partial" if available else "unavailable",
                    "values": [
                        {"available": isinstance(value, (int, float)) and not isinstance(value, bool), "value": value if isinstance(value, (int, float)) and not isinstance(value, bool) else None}
                        for value in raw
                    ],
                    "median": median(available) if available else None,
                }
            stages[stage] = {"measures": measures}
        arms[arm] = {"repetitions": repetitions, "stages": stages}
    return {
        "evidence": "plumbing-only" if plumbing else "benchmark",
        "execution_order": [trial.get("provenance", {}).get("execution_order") for trial in trials],
        "arms": arms,
    }
