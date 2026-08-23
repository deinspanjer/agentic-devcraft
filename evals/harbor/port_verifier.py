import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable

from evals.harbor.engineering_benchmark import sha256_file, tree_digest


CONTRACT_FIELDS = {"id", "stage", "description", "evidence"}


def load_contracts(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if set(value) != {"version", "contracts"} or value["version"] != "vanilla-port-v1":
        raise ValueError("invalid contract inventory")
    ids: set[str] = set()
    for contract in value["contracts"]:
        if set(contract) != CONTRACT_FIELDS or contract["stage"] not in {"initial", "extension"}:
            raise ValueError("invalid contract entry")
        if not contract["id"] or contract["id"] in ids:
            raise ValueError("contract ids must be unique and non-empty")
        if not contract["evidence"] or not all(isinstance(item, str) for item in contract["evidence"]):
            raise ValueError("every contract requires visible evidence")
        if any("history" in item.lower() or "adr" in item.lower() for item in contract["evidence"]):
            raise ValueError("contract inventory cites excluded context")
        ids.add(contract["id"])
    return value


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows))


def _hidden_cases(root: Path) -> list[dict[str, str]]:
    descendant = root / "descendant"
    _write_jsonl(
        descendant / "sessions/2026/07/31/hidden-root.jsonl",
        [
            {"timestamp": "2026-07-31T12:00:00Z", "type": "session_meta", "payload": {"id": "hidden-root", "source": "cli", "cwd": "/workspace/hidden"}},
            {"timestamp": "2026-07-31T12:00:01Z", "type": "event_msg", "payload": {"type": "task_started", "turn_id": "r1"}},
            {"timestamp": "2026-07-31T12:00:02Z", "type": "turn_context", "payload": {"turn_id": "r1", "model": "gpt-5.6-terra", "effort": "high"}},
            {"timestamp": "2026-07-31T12:00:03Z", "type": "event_msg", "payload": {"type": "token_count", "info": {"last_token_usage": {"input_tokens": 12345, "cached_input_tokens": 2345, "cache_write_input_tokens": 345, "output_tokens": 456, "reasoning_output_tokens": 56, "total_tokens": 12801}}}},
            {"timestamp": "2026-07-31T12:00:21Z", "type": "event_msg", "payload": {"type": "task_complete", "turn_id": "r1"}},
        ],
    )
    _write_jsonl(
        descendant / "archived_sessions/hidden-child.jsonl",
        [
            {"timestamp": "2026-07-31T12:00:05Z", "type": "session_meta", "payload": {"id": "hidden-child", "parent_thread_id": "hidden-root", "source": {"subagent": {"review": "reviewer"}}}},
            {"timestamp": "2026-07-31T12:00:06Z", "type": "event_msg", "payload": {"type": "task_started", "turn_id": "c1"}},
            {"timestamp": "2026-07-31T12:00:07Z", "type": "turn_context", "payload": {"turn_id": "c1", "model": "gpt-5.6-luna", "effort": "medium"}},
            {"timestamp": "2026-07-31T12:00:08Z", "type": "event_msg", "payload": {"type": "token_count", "info": {"last_token_usage": {"input_tokens": 678, "cached_input_tokens": 78, "cache_write_input_tokens": 8, "output_tokens": 90, "reasoning_output_tokens": 9, "total_tokens": 768}}}},
            {"timestamp": "2026-07-31T12:00:16Z", "type": "event_msg", "payload": {"type": "task_complete", "turn_id": "c1"}},
        ],
    )
    _write_jsonl(
        descendant / "session_index.jsonl",
        [{"id": "hidden-root", "thread_name": "Hidden descendant case", "updated_at": "2026-07-31T12:01:00Z"}],
    )

    single = root / "single"
    _write_jsonl(
        single / "sessions/2026/01/20/solo.jsonl",
        [
            {"timestamp": "2026-01-20T00:00:00Z", "type": "session_meta", "payload": {"id": "solo", "source": "cli", "cwd": "/workspace/solo"}},
            {"timestamp": "2026-01-20T00:00:01Z", "type": "event_msg", "payload": {"type": "task_started", "turn_id": "s1"}},
            {"timestamp": "2026-01-20T00:00:02Z", "type": "turn_context", "payload": {"turn_id": "s1", "model": "gpt-5.2-codex", "effort": "medium"}},
            {"timestamp": "2026-01-20T00:00:03Z", "type": "event_msg", "payload": {"type": "token_count", "info": {"last_token_usage": {"input_tokens": 2000, "cached_input_tokens": 500, "cache_write_input_tokens": 0, "output_tokens": 100, "reasoning_output_tokens": 40, "total_tokens": 2100}}}},
            {"timestamp": "2026-01-20T00:00:11Z", "type": "event_msg", "payload": {"type": "task_complete", "turn_id": "s1"}},
        ],
    )
    return [
        {"id": "descendant", "rollout": "hidden-root", "home": str(descendant)},
        {"id": "single", "rollout": "solo", "home": str(single)},
    ]


def _run(command: list[str], cwd: Path, timeout_sec: float = 120.0) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
    )
    return {"returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}


def _python_command(script: Path, rollout: str, home: Path, json_output: bool) -> list[str]:
    command = ["python3", str(script), rollout, "--codex-home", str(home)]
    return [*command, "--json"] if json_output else command


def _cargo_binary(workspace: Path) -> tuple[list[dict[str, Any]], Path | None]:
    checks = []
    build = _run(["cargo", "build", "--quiet"], workspace, 300)
    checks.append({"id": "public-build", "passed": build["returncode"] == 0, "detail": build["stderr"][-1000:]})
    tests = _run(["cargo", "test", "--quiet"], workspace, 300)
    checks.append({"id": "public-focused-checks", "passed": tests["returncode"] == 0, "detail": tests["stderr"][-1000:]})
    if not checks[0]["passed"]:
        return checks, None
    metadata = _run(["cargo", "metadata", "--no-deps", "--format-version", "1"], workspace)
    if metadata["returncode"]:
        checks[0].update(passed=False, detail=metadata["stderr"][-1000:])
        return checks, None
    value = json.loads(metadata["stdout"])
    members = set(value.get("workspace_default_members") or value.get("workspace_members") or [])
    packages = [item for item in value["packages"] if item["id"] in members]
    targets = [target for package in packages for target in package["targets"] if "bin" in target["kind"]]
    if len(targets) != 1:
        checks[0].update(passed=False, detail=f"expected one default binary target, found {len(targets)}")
        return checks, None
    suffix = ".exe" if __import__("os").name == "nt" else ""
    return checks, Path(value["target_directory"]) / "debug" / f"{targets[0]['name']}{suffix}"


def _behavior_checks(
    cases: list[dict[str, str]],
    expected: dict[str, dict[str, Any]],
    invoke: Callable[[str, Path, bool], dict[str, Any]],
) -> list[dict[str, Any]]:
    actual: dict[str, dict[str, Any]] = {}
    for case in cases:
        json_run = invoke(case["rollout"], Path(case["home"]), True)
        text_run = invoke(case["rollout"], Path(case["home"]), False)
        try:
            parsed = json.loads(json_run["stdout"]) if json_run["returncode"] == 0 else None
        except json.JSONDecodeError:
            parsed = None
        actual[case["id"]] = {"json": parsed, "json_run": json_run, "text_run": text_run}

    single_equal = actual["single"]["json"] == expected["single"]["json"]
    descendant = actual["descendant"]["json"] or {}
    expected_descendant = expected["descendant"]["json"]
    descendant_equal = all(
        descendant.get(key) == expected_descendant.get(key)
        for key in ("tree", "by_rollout_type")
    )
    aggregation_equal = all(
        (actual[case]["json"] or {}).get("by_model") == expected[case]["json"].get("by_model")
        and (actual[case]["json"] or {}).get("rollout") == expected[case]["json"].get("rollout")
        for case in ("single", "descendant")
    )
    human_ok = True
    for case in cases:
        output = actual[case["id"]]["text_run"]["stdout"]
        oracle = expected[case["id"]]["json"]
        required = [
            f"Codex rollout {case['rollout']}",
            "Tokens and estimated cost by model",
            "Pricing:",
            *oracle["by_model"].keys(),
        ]
        human_ok = human_ok and actual[case["id"]]["text_run"]["returncode"] == 0 and all(item in output for item in required)

    missing = invoke("definitely-missing", Path(cases[0]["home"]), False)
    missing_ok = missing["returncode"] != 0 and "not found" in (missing["stdout"] + missing["stderr"]).lower()
    return [
        {"id": "json-report-parity", "passed": single_equal, "detail": "single-rollout JSON matches oracle" if single_equal else "single-rollout JSON differs"},
        {"id": "descendant-aggregation", "passed": descendant_equal, "detail": "tree and rollout-type aggregation match oracle" if descendant_equal else "descendant aggregation differs"},
        {"id": "model-token-cost-aggregation", "passed": aggregation_equal, "detail": "model, token, duration, and cost values match oracle" if aggregation_equal else "model/token/cost aggregation differs"},
        {"id": "human-report", "passed": human_ok, "detail": "human reports expose required facts" if human_ok else "human report omitted discoverable facts"},
        {"id": "missing-rollout-error", "passed": missing_ok, "detail": "missing rollout fails visibly" if missing_ok else "missing rollout behavior differs"},
    ]


def verify_initial(snapshot: Path, oracle_script: Path, contracts_path: Path) -> dict[str, Any]:
    contracts = load_contracts(contracts_path)
    original_digest = tree_digest(snapshot, include_git=True)
    if not shutil.which("cargo") or not shutil.which("python3"):
        return {"status": "verifier_error", "error": "cargo and python3 are required"}
    try:
        with tempfile.TemporaryDirectory(prefix="devcraft-port-verifier-") as raw:
            root = Path(raw)
            candidate = root / "candidate"
            shutil.copytree(snapshot, candidate, symlinks=True)
            cases = _hidden_cases(root / "evaluator-inputs")
            expected: dict[str, dict[str, Any]] = {}
            for case in cases:
                machine = _run(_python_command(oracle_script, case["rollout"], Path(case["home"]), True), root)
                if machine["returncode"]:
                    raise RuntimeError("Python oracle failed")
                expected[case["id"]] = {"json": json.loads(machine["stdout"])}
            checks, binary = _cargo_binary(candidate)
            if binary is not None:
                checks.extend(
                    _behavior_checks(
                        cases,
                        expected,
                        lambda rollout, home, json_output: _run(
                            [str(binary), rollout, "--codex-home", str(home), *(["--json"] if json_output else [])],
                            candidate,
                        ),
                    )
                )
            else:
                checks.extend(
                    {"id": item["id"], "passed": False, "detail": "not run because the candidate did not build"}
                    for item in contracts["contracts"]
                    if item["stage"] == "initial" and item["id"] not in {check["id"] for check in checks}
                )
    except (OSError, RuntimeError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        return {"status": "verifier_error", "error": type(exc).__name__}

    return {
        "status": "passed" if all(item["passed"] for item in checks) else "failed",
        "stage": "initial",
        "contracts": checks,
        "provenance": {
            "snapshot_digest": original_digest,
            "contracts_digest": sha256_file(contracts_path),
            "oracle_digest": sha256_file(oracle_script),
            "verifier_digest": sha256_file(Path(__file__)),
        },
        "snapshot_unchanged": tree_digest(snapshot, include_git=True) == original_digest,
        "evaluator_inputs_subject_visible": False,
    }


def _price_cost(result: dict[str, Any], model: str, expected: float) -> bool:
    scopes = [
        result.get("rollout", {}),
        result.get("tree", {}),
        result.get("by_model", {}).get(model, {}),
        result.get("by_rollout_type", {}).get("root", {}),
    ]
    return all(
        scope.get("estimated_cost_usd") == expected
        and scope.get("known_model_cost_usd") == expected
        for scope in scopes
    )


def verify_extension(snapshot: Path, oracle_script: Path, contracts_path: Path) -> dict[str, Any]:
    initial = verify_initial(snapshot, oracle_script, contracts_path)
    original_digest = tree_digest(snapshot, include_git=True)
    if initial["status"] == "verifier_error":
        return {"status": "verifier_error", "stage": "extension", "initial": initial}
    try:
        with tempfile.TemporaryDirectory(prefix="devcraft-price-verifier-") as raw:
            root = Path(raw)
            candidate = root / "candidate"
            shutil.copytree(snapshot, candidate, symlinks=True)
            cases = _hidden_cases(root / "evaluator-inputs")
            checks, binary = _cargo_binary(candidate)
            if binary is None:
                extension_checks = [
                    {"id": "initial-contract-regression", "passed": False, "detail": "candidate did not build"},
                    {"id": "built-in-price-defaults", "passed": False, "detail": "candidate did not build"},
                    {"id": "user-price-file", "passed": False, "detail": "candidate did not build"},
                    {"id": "invalid-price-file", "passed": False, "detail": "candidate did not build"},
                ]
            else:
                expected = {}
                defaults_ok = True
                for case in cases:
                    oracle = _run(
                        _python_command(oracle_script, case["rollout"], Path(case["home"]), True),
                        root,
                    )
                    candidate_run = _run(
                        [str(binary), case["rollout"], "--codex-home", case["home"], "--json"],
                        candidate,
                    )
                    expected[case["id"]] = json.loads(oracle["stdout"])
                    try:
                        defaults_ok = defaults_ok and candidate_run["returncode"] == 0 and json.loads(candidate_run["stdout"]) == expected[case["id"]]
                    except json.JSONDecodeError:
                        defaults_ok = False

                custom_home = root / "evaluator-inputs/custom"
                _write_jsonl(
                    custom_home / "sessions/2026/07/31/custom.jsonl",
                    [
                        {"timestamp": "2026-07-31T00:00:00Z", "type": "session_meta", "payload": {"id": "custom", "source": "cli", "cwd": "/workspace/custom"}},
                        {"timestamp": "2026-07-31T00:00:01Z", "type": "event_msg", "payload": {"type": "task_started", "turn_id": "x1"}},
                        {"timestamp": "2026-07-31T00:00:02Z", "type": "turn_context", "payload": {"turn_id": "x1", "model": "private-test-model", "effort": "medium"}},
                        {"timestamp": "2026-07-31T00:00:03Z", "type": "event_msg", "payload": {"type": "token_count", "info": {"last_token_usage": {"input_tokens": 2000, "cached_input_tokens": 500, "cache_write_input_tokens": 0, "output_tokens": 100, "reasoning_output_tokens": 40, "total_tokens": 2100}}}},
                        {"timestamp": "2026-07-31T00:00:11Z", "type": "event_msg", "payload": {"type": "task_complete", "turn_id": "x1"}},
                    ],
                )
                prices = root / "prices.json"
                prices.write_text(
                    json.dumps(
                        {
                            "models": {
                                "gpt-5.2-codex": {"input": 4.0, "cached_input": 0.4, "cache_write": 5.0, "output": 20.0},
                                "private-test-model": {"input": 4.0, "cached_input": 0.4, "cache_write": 5.0, "output": 20.0},
                            }
                        }
                    )
                )

                def priced(rollout: str, home: Path, model: str) -> bool:
                    run = _run(
                        [str(binary), rollout, "--codex-home", str(home), "--json", "--prices", str(prices)],
                        candidate,
                    )
                    try:
                        return run["returncode"] == 0 and _price_cost(json.loads(run["stdout"]), model, 0.0082)
                    except json.JSONDecodeError:
                        return False

                valid_ok = priced("solo", Path(cases[1]["home"]), "gpt-5.2-codex") and priced("custom", custom_home, "private-test-model")
                malformed = root / "malformed.json"
                malformed.write_text("{")
                invalid = root / "invalid.json"
                invalid.write_text('{"models":{"bad":{"input":-1,"cached_input":0,"cache_write":0,"output":1}}}')
                invalid_runs = [
                    _run([str(binary), "solo", "--codex-home", cases[1]["home"], "--prices", str(path)], candidate)
                    for path in (root / "missing.json", malformed, invalid)
                ]
                invalid_ok = all(
                    item["returncode"] != 0 and bool((item["stdout"] + item["stderr"]).strip())
                    for item in invalid_runs
                )
                initial_ok = initial["status"] == "passed"
                extension_checks = [
                    {"id": "initial-contract-regression", "passed": initial_ok, "detail": "initial contracts reran" if initial_ok else "initial contract regression"},
                    {"id": "built-in-price-defaults", "passed": defaults_ok, "detail": "default JSON is unchanged" if defaults_ok else "default JSON changed"},
                    {"id": "user-price-file", "passed": valid_ok, "detail": "override and added-model prices apply" if valid_ok else "valid price-file behavior differs"},
                    {"id": "invalid-price-file", "passed": invalid_ok, "detail": "invalid files fail visibly" if invalid_ok else "invalid file did not fail visibly"},
                ]
    except (OSError, RuntimeError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        return {"status": "verifier_error", "stage": "extension", "error": type(exc).__name__}

    return {
        "status": "passed" if all(item["passed"] for item in extension_checks) else "failed",
        "stage": "extension",
        "contracts": extension_checks,
        "initial": initial,
        "provenance": {
            "snapshot_digest": original_digest,
            "contracts_digest": sha256_file(contracts_path),
            "oracle_digest": sha256_file(oracle_script),
            "verifier_digest": sha256_file(Path(__file__)),
        },
        "snapshot_unchanged": tree_digest(snapshot, include_git=True) == original_digest,
        "evaluator_inputs_subject_visible": False,
    }
