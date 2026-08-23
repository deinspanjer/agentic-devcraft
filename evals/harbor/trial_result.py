import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evals.harbor.engineering_benchmark import privacy_issues, redact, sha256_file, tree_digest


def workspace_state(root: Path) -> list[dict[str, Any]]:
    state: list[dict[str, Any]] = []
    for current, directories, files in os.walk(root, followlinks=False):
        directories.sort()
        for name in sorted(files):
            path = Path(current) / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                state.append({"path": relative, "symlink": os.readlink(path)})
                continue
            content = path.read_bytes()
            state.append(
                {
                    "path": relative,
                    "size": len(content),
                    "sha256": hashlib.sha256(content).hexdigest(),
                }
            )
    return state


def normalized_transcript(trajectory: dict[str, Any]) -> list[dict[str, Any]]:
    steps = trajectory.get("steps")
    if not isinstance(steps, list):
        raise ValueError("trajectory requires a steps list")
    return [
        {
            key: step[key]
            for key in ("source", "message", "tool_calls", "observation", "timestamp")
            if key in step
        }
        for step in steps
        if isinstance(step, dict) and step.get("source") in {"user", "agent"}
    ]


def build_trial_result(
    setup: dict[str, Any],
    trajectory: dict[str, Any],
    workspace: Path,
    verifier: dict[str, Any] | None,
    provenance: dict[str, Any],
) -> dict[str, Any]:
    valid = setup.get("setup", {}).get("status") == "passed"
    verifier_result = verifier if valid and verifier is not None else {"status": "not_run"}
    return {
        "status": "valid" if valid else "invalid",
        "setup": setup["setup"],
        "transcript": normalized_transcript(trajectory) if valid else [],
        "workspace": workspace_state(workspace) if valid else [],
        "verifier": verifier_result,
        "behavioral_score": verifier_result.get("score") if valid else None,
        "provenance": provenance,
    }


def write_trial_result(path: Path, result: dict[str, Any]) -> None:
    path.write_text(json.dumps(result, indent=2) + "\n")


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [text for item in value.values() for text in _strings(item)]
    if isinstance(value, list):
        return [text for item in value for text in _strings(item)]
    return []


def trajectory_evidence(
    trajectory: dict[str, Any],
    *,
    duration_sec: float | None = None,
    reported_tokens: dict[str, int | None] | None = None,
) -> dict[str, Any]:
    steps = trajectory.get("steps") if isinstance(trajectory, dict) else []
    steps = steps if isinstance(steps, list) else []
    agent_messages = [
        step.get("message", "")
        for step in steps
        if isinstance(step, dict) and step.get("source") in {"agent", "assistant"}
    ]
    tool_calls = [
        call
        for step in steps
        if isinstance(step, dict)
        for call in (step.get("tool_calls") or [])
    ]
    tool_text = "\n".join(_strings(tool_calls))
    message_text = "\n".join(message for message in agent_messages if isinstance(message, str))
    commands = sorted(set(line.strip() for line in tool_text.splitlines() if line.strip()))
    token_values = {
        key: (reported_tokens or {}).get(key)
        for key in ("input_tokens", "cached_input_tokens", "output_tokens")
    }
    return {
        "source_inspection": bool(re.search(r"(?:rollout_stats|report)\.py", tool_text)),
        "self_test_inspection": bool(
            re.search(r"(?:--self-test|self_test|test_report\.py|unittest)", tool_text)
        ),
        "questions": [line.strip() for line in message_text.splitlines() if "?" in line],
        "assumptions": [line.strip() for line in message_text.splitlines() if re.search(r"\bassum", line, re.IGNORECASE)],
        "commands": commands,
        "focused_checks": [
            line
            for line in commands
            if re.search(
                r"\b(?:cargo\s+(?:test|check)|python3?\s+(?:-m\s+unittest|\S+\s+--self-test))\b",
                line,
            )
        ],
        "commits": [line for line in commands if re.search(r"\bgit\s+commit\b", line)],
        "cleanup_commands": [line for line in commands if re.search(r"\b(?:rm|rmdir|git\s+clean)\b", line)],
        "turns": len(agent_messages),
        "tool_calls": len(tool_calls),
        "duration_sec": {"available": duration_sec is not None, "value": duration_sec},
        "reported_tokens": {
            key: {"available": isinstance(value, int), "value": value if isinstance(value, int) else None}
            for key, value in sorted(token_values.items())
        },
    }


def compare_stage_snapshots(initial: Path, extension: Path) -> dict[str, Any]:
    initial_state = {
        item["path"]: item
        for item in workspace_state(initial)
        if not item["path"].startswith("target/")
    }
    extension_state = {
        item["path"]: item
        for item in workspace_state(extension)
        if not item["path"].startswith("target/")
    }
    changed = sorted(
        path
        for path in initial_state.keys() | extension_state.keys()
        if initial_state.get(path) != extension_state.get(path)
    )
    source_paths = [
        path
        for path in changed
        if Path(path).suffix in {".rs", ".toml", ".py"}
        and Path(path).parts[0] not in {"tests", "fixtures"}
        and (extension / path).is_file()
    ]
    pricing_owners = []
    for path in source_paths:
        try:
            text = (extension / path).read_text()
        except (OSError, UnicodeDecodeError):
            continue
        if re.search(r"(?:price|pricing|rate)", text, re.IGNORECASE):
            pricing_owners.append(path)
    platform_patterns = re.compile(r"(?:launchd|launchctl|codesign|notary|installer|msi|release|github/workflows)", re.IGNORECASE)
    platform_scaffolding = [path for path in extension_state if platform_patterns.search(path)]
    return {
        "changed_paths": changed,
        "changed_modules": sorted({Path(path).parts[0] for path in changed if Path(path).parts}),
        "pricing_owners": pricing_owners,
        "pricing_ownership_count": len(pricing_owners),
        "duplication_signal": "multiple-pricing-owners" if len(pricing_owners) > 1 else None,
        "extension_changed_file_count": len(changed),
        "platform_or_packaging_scaffolding": sorted(platform_scaffolding),
        "interpretation": "Path and ownership signals require review; file or line counts are not design-quality scores.",
    }


def build_engineering_result(
    *,
    checkpoints: list[dict[str, Any]],
    trajectories: dict[str, dict[str, Any]],
    snapshot_paths: dict[str, Path],
    provenance: dict[str, Any],
    host_metrics: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    required_provenance = {
        "trial_id",
        "arm",
        "repetition",
        "execution_order",
        "fixture",
        "prompts",
        "harness",
        "verifier",
        "host",
        "model",
        "configuration",
        "provisioned_content",
        "historical_context",
    }
    if set(provenance) != required_provenance or provenance["historical_context"] != "none":
        raise ValueError("engineering result requires exact code-only provenance")
    by_stage = {item["stage"]: item for item in checkpoints}
    stages = {}
    for stage, checkpoint in by_stage.items():
        verifier = checkpoint.get("verifier") or {"status": "not_run", "contracts": []}
        contracts = verifier.get("contracts") or []
        stages[stage] = {
            "product": {
                "status": verifier.get("status"),
                "contracts": contracts,
                "contracts_passed": sum(bool(item.get("passed")) for item in contracts),
                "contracts_total": len(contracts),
                "robustness": verifier.get("robustness", []),
            },
            "engineering": {
                "workspace_digest": checkpoint.get("workspace_digest"),
                "changed_paths": checkpoint.get("git", {}).get("changed_paths", []),
                "process_artifacts": [
                    item["path"]
                    for item in checkpoint.get("inventory", [])
                    if re.search(r"(?:AGENTS\.md|openspec|docs/|plan)", item.get("path", ""), re.IGNORECASE)
                ],
            },
            "process": {
                **trajectory_evidence(
                    trajectories.get(stage, {}),
                    duration_sec=(host_metrics or {}).get(stage, {}).get("duration_sec"),
                    reported_tokens=(host_metrics or {}).get(stage, {}).get("reported_tokens"),
                ),
                "termination": checkpoint.get("controller", {}).get("termination"),
                "steering": checkpoint.get("controller", {}).get("decisions", []),
                "process_artifacts": [
                    item["path"]
                    for item in checkpoint.get("inventory", [])
                    if re.search(r"(?:AGENTS\.md|openspec|docs/|plan)", item.get("path", ""), re.IGNORECASE)
                ],
            },
        }
    if {"initial", "extension"} <= snapshot_paths.keys():
        stages["extension"]["engineering"]["extension_comparison"] = compare_stage_snapshots(
            snapshot_paths["initial"], snapshot_paths["extension"]
        )
    return {"status": "valid", "stages": stages, "provenance": provenance}


def blinded_qualitative_input(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "stages": {
            stage: {
                "product": value.get("product"),
                "engineering": value.get("engineering"),
                "process": {
                    key: value.get("process", {}).get(key)
                    for key in (
                        "source_inspection",
                        "self_test_inspection",
                        "questions",
                        "assumptions",
                        "focused_checks",
                        "process_artifacts",
                        "turns",
                        "tool_calls",
                        "duration_sec",
                        "reported_tokens",
                    )
                    if key in value.get("process", {})
                },
            }
            for stage, value in result.get("stages", {}).items()
        },
        "rubric": {
            "kind": "shared-framework",
            "criteria": [
                "explicit-requirements",
                "engineering-robustness",
                "documentation-consistency",
                "scope-control",
                "design-ownership-and-extension-locality",
                "test-quality",
                "discovery-and-interaction",
                "resource-efficiency",
            ],
        },
    }


def write_qualitative_record(
    path: Path, result: dict[str, Any], assessment: dict[str, Any]
) -> dict[str, Any]:
    if path.exists():
        raise FileExistsError(path)
    judge_input = blinded_qualitative_input(result)
    record = {
        "input_digest": hashlib.sha256(
            json.dumps(judge_input, sort_keys=True).encode()
        ).hexdigest(),
        "input": judge_input,
        "assessment": redact(assessment),
    }
    if issues := privacy_issues(record):
        raise ValueError("qualitative record failed privacy check: " + ", ".join(issues))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2) + "\n")
    return record


def offline_rescore(
    *,
    original_trial: Path,
    snapshots: dict[str, Path],
    oracle_script: Path,
    contracts_path: Path,
    output: Path,
    verifier_module: str = "evals.harbor.port_verifier",
) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(output)
    original_bytes = original_trial.read_bytes()
    snapshot_digests = {
        stage: tree_digest(path, include_git=True) for stage, path in snapshots.items()
    }
    import importlib

    module = importlib.import_module(verifier_module)
    verify_initial = module.verify_initial
    verify_extension = module.verify_extension

    verifiers = {}
    if "initial" in snapshots:
        verifiers["initial"] = verify_initial(
            snapshots["initial"], oracle_script, contracts_path
        )
    if "extension" in snapshots:
        verifiers["extension"] = verify_extension(
            snapshots["extension"], oracle_script, contracts_path
        )
    if original_trial.read_bytes() != original_bytes or any(
        tree_digest(path, include_git=True) != snapshot_digests[stage]
        for stage, path in snapshots.items()
    ):
        raise RuntimeError("offline rescore mutated retained evidence")
    record = {
        "kind": "offline-rescore",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "original_trial_digest": hashlib.sha256(original_bytes).hexdigest(),
        "snapshot_digests": snapshot_digests,
        "contracts_digest": sha256_file(contracts_path),
        "reference_digest": sha256_file(oracle_script),
        "verifiers": verifiers,
    }
    if issues := privacy_issues(record):
        raise ValueError("rescore failed privacy check: " + ", ".join(issues))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x") as stream:
        json.dump(record, stream, indent=2)
        stream.write("\n")
    return record
