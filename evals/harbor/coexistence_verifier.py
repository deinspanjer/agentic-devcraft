from collections import Counter
from typing import Any


OVERLAPS = {
    "fact-check": {"thorough-brainstorming", "cold-read"},
    "review": {"critical-design-review", "review-integrity"},
    "revision": {"update-design-doc", "decision-evolution"},
}


def verify_coexistence(records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if set(records) != {"peters-only", "devcraft-only", "combined"}:
        raise ValueError("records require peters-only, devcraft-only, and combined arms")
    min_turns = min(record["turns"] for record in records.values())
    arms: dict[str, Any] = {}
    for name, record in records.items():
        phase_counts = Counter(record.get("phases", []))
        duplicates = sorted(phase for phase, count in phase_counts.items() if count > 1)
        invoked = {value.split(":")[-1] for value in record.get("invocations", [])}
        conflicts = sorted(
            family for family, skills in OVERLAPS.items() if len(invoked & skills) > 1
        )
        arms[name] = {
            "duplicate_phases": duplicates,
            "conflicting_invocations": conflicts,
            "extra_turns": record["turns"] - min_turns,
            "outcome": record.get("outcome"),
        }
    outcomes = {name: value["outcome"] for name, value in arms.items()}
    return {"arms": arms, "outcome_differences": len({repr(value) for value in outcomes.values()}) > 1}
