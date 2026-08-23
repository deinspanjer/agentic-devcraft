from typing import Any


def verify_decision_evolution(expected: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    changed_basis = response.get("changed_basis")
    basis = next(
        (
            item
            for item in changed_basis
            if isinstance(item, dict) and item.get("id") == expected["basis_id"]
        ),
        None,
    ) if isinstance(changed_basis, list) else None
    decision = response.get("current_decision")
    history = response.get("history")
    superseded = next(
        (
            item
            for item in history
            if isinstance(item, dict) and item.get("id") == expected["superseded"]["id"]
        ),
        None,
    ) if isinstance(history, list) else None
    downstream = response.get("downstream")
    downstream_by_id = {
        item.get("id"): item.get("value")
        for item in downstream
        if isinstance(item, dict)
    } if isinstance(downstream, list) else {}

    return {
        "changed_basis": {
            "passed": basis is not None
            and bool(str(basis.get("from", "")).strip())
            and bool(str(basis.get("to", "")).strip())
        },
        "replacement_decision": {"passed": decision == expected["decision"]},
        "supersession_history": {
            "passed": superseded is not None
            and superseded.get("status") == "superseded"
            and superseded.get("replaced_by") == expected["superseded"]["replaced_by"]
        },
        "downstream_effects": {
            "passed": downstream_by_id == expected["downstream"],
            "actual": downstream_by_id,
        },
    }
