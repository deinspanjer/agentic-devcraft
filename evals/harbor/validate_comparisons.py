import json
import re
import sys
from pathlib import Path
from typing import Any


FIELDS = {
    "id",
    "host",
    "model",
    "fixture",
    "interaction",
    "skills",
    "hooks",
    "workflow_context",
    "timeout_sec",
    "repetitions",
}
HOSTS = {"codex", "claude-code"}
INTERACTIONS = {"headless", "scripted", "adaptive"}


def _names(value: Any, label: str) -> None:
    if not isinstance(value, list) or len(value) != len(set(value)) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ValueError(f"{label} must be a unique string list")


def validate_comparison(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {"id", "arms"}:
        raise ValueError("comparison requires exactly id and arms")
    if not isinstance(value["id"], str) or not re.fullmatch(r"[a-z0-9-]+", value["id"]):
        raise ValueError("comparison id must contain lowercase letters, numbers, and hyphens")

    arms = value["arms"]
    if not isinstance(arms, list) or len(arms) < 2:
        raise ValueError("arms must contain at least two paired definitions")

    ids: set[str] = set()
    for index, arm in enumerate(arms):
        label = f"arms[{index}]"
        if not isinstance(arm, dict) or set(arm) != FIELDS:
            missing = sorted(FIELDS - set(arm if isinstance(arm, dict) else {}))
            raise ValueError(f"{label} fields must be exactly {sorted(FIELDS)}; missing={missing}")
        if not isinstance(arm["id"], str) or not re.fullmatch(r"[a-z0-9-]+", arm["id"]):
            raise ValueError(f"{label}.id is invalid")
        if arm["id"] in ids:
            raise ValueError("arm ids must be unique")
        ids.add(arm["id"])
        if arm["host"] not in HOSTS:
            raise ValueError(f"{label}.host must be one of {sorted(HOSTS)}")
        model = arm["model"]
        if not isinstance(model, dict) or set(model) != {"name", "settings"}:
            raise ValueError(f"{label}.model requires name and settings")
        if not isinstance(model["name"], str) or not model["name"] or not isinstance(model["settings"], dict):
            raise ValueError(f"{label}.model values are invalid")
        fixture = arm["fixture"]
        if not isinstance(fixture, str) or not fixture or Path(fixture).is_absolute() or ".." in Path(fixture).parts:
            raise ValueError(f"{label}.fixture must be a safe relative path")
        if arm["interaction"] not in INTERACTIONS:
            raise ValueError(f"{label}.interaction must be one of {sorted(INTERACTIONS)}")
        for field in ("skills", "hooks", "workflow_context"):
            _names(arm[field], f"{label}.{field}")
        if isinstance(arm["timeout_sec"], bool) or not isinstance(arm["timeout_sec"], (int, float)) or arm["timeout_sec"] <= 0:
            raise ValueError(f"{label}.timeout_sec must be positive")
        if isinstance(arm["repetitions"], bool) or not isinstance(arm["repetitions"], int) or arm["repetitions"] < 1:
            raise ValueError(f"{label}.repetitions must be a positive integer")

    paired_fields = FIELDS - {"id", "skills", "hooks"}
    baseline = {field: arms[0][field] for field in paired_fields}
    if any({field: arm[field] for field in paired_fields} != baseline for arm in arms[1:]):
        raise ValueError("paired arms may differ only in id, skills, and hooks")
    if len({(tuple(arm["skills"]), tuple(arm["hooks"])) for arm in arms}) < 2:
        raise ValueError("paired arms must declare different skill or hook configuration")
    return value


def main(paths: list[str]) -> int:
    if not paths:
        print("usage: validate_comparisons.py <comparison.json> [...]", file=sys.stderr)
        return 2
    for raw_path in paths:
        try:
            validate_comparison(json.loads(Path(raw_path).read_text()))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"{raw_path}: {exc}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
