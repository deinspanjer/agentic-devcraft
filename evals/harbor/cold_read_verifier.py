from typing import Any


def verify_cold_read(expected: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    expected_claims = expected["claims"]
    claims = response.get("claims")
    if not isinstance(expected_claims, dict) or not isinstance(claims, list):
        raise ValueError("expected claims map and response claims list are required")

    by_id = {
        claim.get("id"): claim
        for claim in claims
        if isinstance(claim, dict) and isinstance(claim.get("id"), str)
    }
    missing = sorted(set(expected_claims) - set(by_id))
    extra = sorted(set(by_id) - set(expected_claims))
    incorrect = sorted(
        claim_id
        for claim_id, status in expected_claims.items()
        if claim_id in by_id
        and (
            by_id[claim_id].get("status") != status
            or not str(by_id[claim_id].get("evidence", "")).strip()
        )
    )
    design = response.get("design") if isinstance(response.get("design"), dict) else {}
    return {
        "enumeration_coverage": {
            "passed": not missing and not extra,
            "missing": missing,
            "extra": extra,
        },
        "factual_verification": {
            "passed": not missing and not incorrect,
            "incorrect": incorrect,
        },
        "design_correction": {
            "passed": design.get("status") == "change"
            and design.get("replacement") == expected["replacement"],
            "actual": design.get("replacement"),
        },
    }
