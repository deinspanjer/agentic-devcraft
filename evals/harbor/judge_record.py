from typing import Any
from pathlib import PurePosixPath


MECHANICAL_CRITERIA = {"correctness", "false-positives", "workflow-adherence"}


def build_judge_record(
    config: dict[str, Any],
    artifacts: list[str],
    result: dict[str, Any],
    deterministic_verifier: dict[str, Any],
) -> dict[str, Any]:
    criteria = config.get("rubric", {}).get("criteria")
    if not isinstance(criteria, list) or not criteria:
        raise ValueError("judge rubric requires criteria")
    ids = {criterion.get("id") for criterion in criteria if isinstance(criterion, dict)}
    if ids & MECHANICAL_CRITERIA:
        raise ValueError("judge rubric duplicates mechanically verified criteria")
    if not artifacts or any(
        not PurePosixPath(path).parts
        or not PurePosixPath(path).parts[0].startswith("candidate-")
        for path in artifacts
    ):
        raise ValueError("judge artifacts must use blinded candidate labels")
    return {
        "deterministic_verifier": deterministic_verifier,
        "judge": {
            "identity": config["identity"],
            "rubric": config["rubric"],
            "artifacts": artifacts,
            "result": result,
        },
    }
