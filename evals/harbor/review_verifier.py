from typing import Any


def _matches(expected: dict[str, Any], finding: dict[str, Any]) -> bool:
    return (
        finding.get("file") == expected["file"]
        and finding.get("category") == expected["category"]
        and isinstance(finding.get("start_line"), int)
        and isinstance(finding.get("end_line"), int)
        and finding["start_line"] <= expected["end_line"]
        and finding["end_line"] >= expected["start_line"]
    )


def verify_review(expected: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    expected_findings = expected.get("findings")
    findings = response.get("findings")
    if not isinstance(expected_findings, list) or not isinstance(findings, list):
        raise ValueError("expected and response require findings lists")

    unmatched = list(range(len(findings)))
    supported: list[dict[str, Any]] = []
    missed: list[dict[str, Any]] = []
    for expected_finding in expected_findings:
        match = next(
            (index for index in unmatched if _matches(expected_finding, findings[index])),
            None,
        )
        if match is None:
            missed.append(expected_finding)
        else:
            unmatched.remove(match)
            supported.append(findings[match])

    fabricated = [findings[index] for index in unmatched]
    passed = not missed and not fabricated
    return {
        "status": "passed" if passed else "failed",
        "correct_empty": not expected_findings and not findings,
        "supported_findings": supported,
        "missed_findings": missed,
        "fabricated_findings": fabricated,
    }
