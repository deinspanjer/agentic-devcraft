import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from evals.harbor.engineering_benchmark import sha256_file, tree_digest


CONTRACT_FIELDS = {"id", "stage", "kind", "scored", "description", "evidence"}


def load_contracts(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if set(value) != {"version", "contracts"} or value["version"] != "date-filter-v1":
        raise ValueError("invalid date-filter contract inventory")
    ids = set()
    for contract in value["contracts"]:
        if set(contract) != CONTRACT_FIELDS:
            raise ValueError("invalid date-filter contract entry")
        if contract["stage"] not in {"initial", "extension"}:
            raise ValueError("invalid contract stage")
        if contract["kind"] not in {"required", "robustness"}:
            raise ValueError("invalid contract kind")
        if contract["scored"] is not (contract["kind"] == "required"):
            raise ValueError("only required contracts determine pass/fail")
        if not contract["id"] or contract["id"] in ids:
            raise ValueError("contract ids must be unique and non-empty")
        if not contract["evidence"] or not all(
            isinstance(item, str) for item in contract["evidence"]
        ):
            raise ValueError("every contract requires visible evidence")
        ids.add(contract["id"])
    return value


def _run(command: list[str], cwd: Path) -> dict[str, Any]:
    result = subprocess.run(
        command, cwd=cwd, capture_output=True, text=True, timeout=30
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def _records(path: Path) -> None:
    rows = [
        {"id": "before", "date": "2026-01-01", "status": "open"},
        {"id": "start-a", "date": "2026-01-10", "status": "closed"},
        {"id": "start-b", "date": "2026-01-10", "status": "open"},
        {"id": "after", "date": "2026-02-01", "status": "blocked"},
    ]
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def _report(candidate: Path, source: Path, *arguments: str) -> dict[str, Any]:
    return _run(
        ["python3", str(candidate / "report.py"), str(source), *arguments, "--json"],
        candidate,
    )


def _matches(result: dict[str, Any], expected: dict[str, Any]) -> bool:
    if result["returncode"]:
        return False
    try:
        return json.loads(result["stdout"]) == expected
    except json.JSONDecodeError:
        return False


def _initial_checks(candidate: Path, source: Path) -> list[dict[str, Any]]:
    tests = _run(["python3", "-m", "unittest", "-v"], candidate)
    default = _report(candidate, source)
    since = _report(candidate, source, "--since", "2026-01-10")
    try:
        readme = (candidate / "README.md").read_text().lower()
    except OSError:
        readme = ""
    return [
        {
            "id": "focused-checks",
            "passed": tests["returncode"] == 0,
            "detail": "unittest suite passes" if tests["returncode"] == 0 else "unittest suite fails",
        },
        {
            "id": "default-report-regression",
            "passed": _matches(
                default,
                {"total": 4, "by_status": {"blocked": 1, "closed": 1, "open": 2}},
            ),
            "detail": "default JSON report is unchanged",
        },
        {
            "id": "since-inclusive",
            "passed": _matches(
                since,
                {"total": 3, "by_status": {"blocked": 1, "closed": 1, "open": 1}},
            ),
            "detail": "inclusive lower boundary filters the report",
        },
        {
            "id": "since-documentation",
            "passed": "--since" in readme and "yyyy-mm-dd" in readme,
            "detail": "README documents --since and its date format",
        },
    ]


def _robustness(candidate: Path, source: Path, stage: str) -> list[dict[str, Any]]:
    invalid_since = _report(candidate, source, "--since", "not-a-date")
    observations = [
        {
            "id": "invalid-since",
            "outcome": "rejected" if invalid_since["returncode"] else "accepted",
            "detail": "invalid lower boundary should fail visibly",
        }
    ]
    if stage == "extension":
        invalid_until = _report(candidate, source, "--until", "not-a-date")
        inverted = _report(
            candidate,
            source,
            "--since",
            "2026-02-01",
            "--until",
            "2026-01-01",
        )
        observations.extend(
            [
                {
                    "id": "invalid-until",
                    "outcome": "rejected" if invalid_until["returncode"] else "accepted",
                    "detail": "invalid upper boundary should fail visibly",
                },
                {
                    "id": "inverted-range",
                    "outcome": "rejected" if inverted["returncode"] else "accepted",
                    "detail": "inverted-range policy was not explicitly required",
                },
            ]
        )
    return observations


def _provenance(
    snapshot_digest: str, reference_path: Path, contracts_path: Path
) -> dict[str, str]:
    return {
        "snapshot_digest": snapshot_digest,
        "contracts_digest": sha256_file(contracts_path),
        "rubric_digest": sha256_file(reference_path),
        "verifier_digest": sha256_file(Path(__file__)),
    }


def verify_initial(
    snapshot: Path, reference_path: Path, contracts_path: Path
) -> dict[str, Any]:
    load_contracts(contracts_path)
    rubric = json.loads(reference_path.read_text())
    if rubric.get("scenario") != "date-filter-v1":
        return {"status": "verifier_error", "error": "invalid rubric"}
    original_digest = tree_digest(snapshot, include_git=True)
    try:
        with tempfile.TemporaryDirectory(prefix="devcraft-date-filter-") as raw:
            candidate = Path(raw) / "candidate"
            shutil.copytree(snapshot, candidate, symlinks=True)
            source = Path(raw) / "records.jsonl"
            _records(source)
            checks = _initial_checks(candidate, source)
            robustness = _robustness(candidate, source, "initial")
    except (OSError, subprocess.SubprocessError) as exc:
        return {"status": "verifier_error", "error": type(exc).__name__}
    return {
        "status": "passed" if all(item["passed"] for item in checks) else "failed",
        "stage": "initial",
        "contracts": checks,
        "robustness": robustness,
        "provenance": _provenance(original_digest, reference_path, contracts_path),
        "snapshot_unchanged": tree_digest(snapshot, include_git=True) == original_digest,
        "evaluator_inputs_subject_visible": False,
    }


def verify_extension(
    snapshot: Path, reference_path: Path, contracts_path: Path
) -> dict[str, Any]:
    load_contracts(contracts_path)
    rubric = json.loads(reference_path.read_text())
    if rubric.get("scenario") != "date-filter-v1":
        return {"status": "verifier_error", "error": "invalid rubric"}
    original_digest = tree_digest(snapshot, include_git=True)
    try:
        with tempfile.TemporaryDirectory(prefix="devcraft-date-range-") as raw:
            candidate = Path(raw) / "candidate"
            shutil.copytree(snapshot, candidate, symlinks=True)
            source = Path(raw) / "records.jsonl"
            _records(source)
            initial = _initial_checks(candidate, source)
            until = _report(candidate, source, "--until", "2026-01-10")
            combined = _report(
                candidate,
                source,
                "--since",
                "2026-01-10",
                "--until",
                "2026-01-10",
            )
            try:
                readme = (candidate / "README.md").read_text().lower()
            except OSError:
                readme = ""
            checks = [
                {
                    "id": "initial-contract-regression",
                    "passed": all(item["passed"] for item in initial),
                    "detail": "initial required contracts remain intact",
                },
                {
                    "id": "until-inclusive",
                    "passed": _matches(
                        until,
                        {"total": 3, "by_status": {"closed": 1, "open": 2}},
                    ),
                    "detail": "inclusive upper boundary filters the report",
                },
                {
                    "id": "combined-range",
                    "passed": _matches(
                        combined,
                        {"total": 2, "by_status": {"closed": 1, "open": 1}},
                    ),
                    "detail": "lower and upper boundaries compose",
                },
                {
                    "id": "until-documentation",
                    "passed": "--until" in readme and "--since" in readme,
                    "detail": "README documents --until and combined use",
                },
            ]
            robustness = _robustness(candidate, source, "extension")
    except (OSError, subprocess.SubprocessError) as exc:
        return {"status": "verifier_error", "error": type(exc).__name__}
    return {
        "status": "passed" if all(item["passed"] for item in checks) else "failed",
        "stage": "extension",
        "contracts": checks,
        "robustness": robustness,
        "provenance": _provenance(original_digest, reference_path, contracts_path),
        "snapshot_unchanged": tree_digest(snapshot, include_git=True) == original_digest,
        "evaluator_inputs_subject_visible": False,
    }
