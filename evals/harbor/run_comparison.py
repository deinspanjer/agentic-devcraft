import argparse
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evals.harbor.cold_read_verifier import verify_cold_read
from evals.harbor.coexistence_verifier import verify_coexistence
from evals.harbor.comparison_summary import summarize_comparison
from evals.harbor.decision_verifier import verify_decision_evolution
from evals.harbor.prepare_arm import prepare_arm
from evals.harbor.review_verifier import verify_review
from evals.harbor.trial_result import build_trial_result, write_trial_result
from evals.harbor.validate_comparisons import validate_comparison
from evals.harbor.workflow_verifier import verify_workflow_ownership


BASE_DOCKERFILE = Path(__file__).parent / "tasks/subject-smoke/environment/Dockerfile"
MODEL_HOSTS = {
    "codex": ["chatgpt.com"],
    "claude-code": ["api.anthropic.com", "statsig.anthropic.com", "sentry.io"],
}


def create_task(
    prepared: Path, task: Path, timeout_sec: float, interaction: str = "headless"
) -> None:
    shutil.copytree(prepared / "workspace", task / "environment/workspace")
    (task / "environment/Dockerfile").write_text(
        BASE_DOCKERFILE.read_text()
        + "\nCOPY --chown=node:node workspace/ /app/\n"
    )
    verifier = (
        "#!/usr/bin/env bash\nset -euo pipefail\n"
        "mkdir -p /logs/verifier\necho 1 > /logs/verifier/reward.txt\n"
    )
    step_config = ""
    if interaction == "headless":
        (task / "instruction.md").write_bytes((prepared / "workspace/instruction.md").read_bytes())
        (task / "tests").mkdir()
        (task / "tests/test.sh").write_text(verifier)
        (task / "tests/test.sh").chmod(0o755)
    elif interaction == "scripted":
        prompts = sorted((prepared / "workspace").glob("turn-*.md"))
        if len(prompts) < 2:
            raise ValueError("scripted fixtures require at least two turn-*.md prompts")
        for prompt in prompts:
            step = task / "steps" / prompt.stem
            (step / "tests").mkdir(parents=True)
            (step / "instruction.md").write_bytes(prompt.read_bytes())
            (step / "tests/test.sh").write_text(verifier)
            (step / "tests/test.sh").chmod(0o755)
            step_config += f'[[steps]]\nname = "{prompt.stem}"\nmin_reward = 1.0\n\n'
    else:
        raise ValueError(f"comparison runner does not support {interaction} interaction")
    (task / "task.toml").write_text(
        "schema_version = \"1.4\"\n\n"
        "[task]\nname = \"agentic-devcraft/behavioral-comparison\"\nversion = \"1.0.0\"\n\n"
        + step_config
        +
        f"[agent]\ntimeout_sec = {float(timeout_sec)}\nuser = \"node\"\n\n"
        "[verifier]\ntimeout_sec = 30.0\n\n"
        "[environment]\nbuild_timeout_sec = 600.0\ncpus = 1\nmemory_mb = 2048\n"
        "storage_mb = 4096\ngpus = 0\nmcp_servers = []\nnetwork_mode = \"allowlist\"\n"
        "allowed_hosts = []\n\n[environment.env]\n\n[verifier.env]\n\n[solution.env]\n"
    )


def _response_json(trajectory: dict[str, Any]) -> dict[str, Any]:
    for step in reversed(trajectory.get("steps", [])):
        if step.get("source") not in {"agent", "assistant"} or not isinstance(step.get("message"), str):
            continue
        text = step["message"].strip()
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end >= start:
            return json.loads(text[start : end + 1])
    raise ValueError("agent trajectory has no JSON response")


def _verify(comparison_id: str, response: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    if comparison_id == "cold-read":
        expected = json.loads((repo_root / "evals/harbor/expectations/cold-read.json").read_text())
        checks = verify_cold_read(expected, response)
        return {"status": "passed" if all(value["passed"] for value in checks.values()) else "failed", **checks}
    if comparison_id in {"review-clean", "review-seeded"}:
        case = comparison_id.removeprefix("review-")
        expected = json.loads((repo_root / f"evals/harbor/expectations/review-integrity/{case}.json").read_text())
        return verify_review(expected, response)
    if comparison_id == "decision-evolution":
        expected = json.loads((repo_root / "evals/harbor/expectations/decision-evolution.json").read_text())
        checks = verify_decision_evolution(expected, response)
        return {"status": "passed" if all(value["passed"] for value in checks.values()) else "failed", **checks}
    return {"status": "not_configured"}


def _duration(result: dict[str, Any]) -> float | None:
    try:
        execution = result.get("agent_execution") or result
        start = datetime.fromisoformat(execution["started_at"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(execution["finished_at"].replace("Z", "+00:00"))
        return (end - start).total_seconds()
    except (KeyError, TypeError, ValueError):
        return None


def run_arm(
    comparison_id: str,
    arm: dict[str, Any],
    repetition: int,
    repo_root: Path,
    harbor_bin: Path,
    run_dir: Path,
) -> dict[str, Any]:
    trial_root = run_dir / f"{arm['id']}-{repetition}"
    prepared = trial_root / "prepared"
    task = trial_root / "task"
    setup = prepare_arm(arm, repo_root, prepared)
    create_task(prepared, task, arm["timeout_sec"], arm["interaction"])

    command = [
        str(harbor_bin), "run", "--path", str(task), "--agent", arm["host"],
        "--model", arm["model"]["name"], "--jobs-dir", str(trial_root / "harbor"),
        "--n-concurrent", "1", "--delete", "--artifact", "/app", "--yes",
    ]
    for key, value in arm["model"]["settings"].items():
        command.extend(["--agent-kwarg", f"{key}={value}"])
    staged_skills = prepared / "skills"
    if staged_skills.exists():
        command.extend(["--skill", str(staged_skills)])
    for source in setup["setup"]["remote_skills"]:
        command.extend(["--skill", source])
    hook_config = setup["setup"]["hook_config"]
    if hook_config and arm["host"] == "codex":
        command[command.index("codex")] = "evals.harbor.evaluation_agents:EvaluationCodex"
        command.extend(["--agent-kwarg", f"hooks_path={hook_config}"])
        command.extend(["--agent-kwarg", "dangerously_bypass_hook_trust=true"])
    elif hook_config:
        command.extend(["--agent-kwarg", f"config={hook_config}"])
    for host in MODEL_HOSTS[arm["host"]]:
        command.extend(["--allow-agent-host", host])
    if arm["interaction"] == "scripted":
        command.append("--resume-trajectory")

    env = {**os.environ, "PYTHONPATH": f"{repo_root}{os.pathsep}{os.environ.get('PYTHONPATH', '')}"}
    completed = subprocess.run(command, cwd=repo_root, env=env)
    if completed.returncode:
        setup["setup"].update(status="failed", reason=f"Harbor exited {completed.returncode}")
        return build_trial_result(setup, {"steps": []}, prepared / "workspace", None, {"arm": arm["id"]})

    trial_results = [
        path
        for path in (trial_root / "harbor").glob("**/result.json")
        if (path.parent / "trial.log").is_file()
    ]
    if len(trial_results) != 1:
        raise RuntimeError(f"expected one Harbor trial result, found {len(trial_results)}")
    harbor_result = json.loads(trial_results[0].read_text())
    if harbor_result.get("exception_info"):
        setup["setup"].update(
            status="failed",
            reason=harbor_result["exception_info"].get("exception_type", "Harbor trial failed"),
        )
        result = build_trial_result(
            setup, {"steps": []}, prepared / "workspace", None, {"arm": arm["id"]}
        )
        write_trial_result(trial_root / "trial.json", result)
        return result

    trajectories = sorted((trial_root / "harbor").glob("**/agent/trajectory.json"))
    expected_trajectories = 1 if arm["interaction"] == "headless" else len(list((task / "steps").iterdir()))
    if len(trajectories) != expected_trajectories:
        raise RuntimeError(f"expected {expected_trajectories} trajectories, found {len(trajectories)}")
    trial_dir = trajectories[-1].parent.parent
    # A resumed Harbor trajectory already contains the preceding conversation.
    trajectory = json.loads(trajectories[-1].read_text())
    workspace = trial_dir / "artifacts/app"
    if comparison_id == "workflow-ownership":
        expected = json.loads((repo_root / "evals/harbor/expectations/workflow-ownership.json").read_text())
        checks = verify_workflow_ownership(prepared / "workspace", workspace, expected)
        verifier = {"status": "passed" if all(value["passed"] for value in checks.values()) else "failed", **checks}
    elif comparison_id == "peters-coexistence":
        record_path = workspace / "evaluation-record.json"
        try:
            coexistence_record = json.loads(record_path.read_text())
            record_found = isinstance(coexistence_record, dict)
        except (OSError, json.JSONDecodeError):
            coexistence_record, record_found = None, False
        verifier = {"status": "pending_comparison" if record_found else "failed", "record_found": record_found}
    else:
        try:
            verifier = _verify(comparison_id, _response_json(trajectory), repo_root)
        except (KeyError, TypeError, ValueError) as exc:
            verifier = {"status": "failed", "malformed_response": str(exc)}
    provenance = {
        "comparison": comparison_id,
        "arm": arm["id"],
        "repetition": repetition,
        "host": harbor_result.get("agent_info"),
        "harness": "harbor-0.21.0",
        "configuration": setup["setup"],
    }
    result = build_trial_result(setup, trajectory, workspace, verifier, provenance)
    agent_results = [
        result.get("agent_result") or {}
        for result in (harbor_result.get("step_results") or [harbor_result])
    ]
    def total(field: str) -> int | None:
        values = [result.get(field) for result in agent_results]
        return sum(values) if values and all(isinstance(value, int) for value in values) else None

    result.update(
        arm=arm["id"],
        duration_sec=_duration(harbor_result),
        turns=len(trajectories),
        tool_calls=sum(len(step.get("tool_calls") or []) for step in trajectory.get("steps", [])),
        input_tokens=total("n_input_tokens"),
        cache_tokens=total("n_cache_tokens"),
        output_tokens=total("n_output_tokens"),
    )
    if comparison_id == "cold-read":
        result["correctness"] = int(verifier["status"] == "passed")
    elif comparison_id.startswith("review-"):
        result["correctness"] = int(not verifier["missed_findings"])
        result["false_positives"] = len(verifier["fabricated_findings"])
    elif comparison_id in {"decision-evolution", "workflow-ownership"}:
        result["correctness"] = int(verifier["status"] == "passed")
    if comparison_id == "workflow-ownership":
        result["workflow_adherence"] = int(verifier["status"] == "passed")
    if comparison_id == "peters-coexistence" and verifier["record_found"]:
        result["coexistence_record"] = coexistence_record
    write_trial_result(trial_root / "trial.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("host", choices=MODEL_HOSTS)
    parser.add_argument("model")
    parser.add_argument("comparison")
    parser.add_argument("--repetitions", type=int)
    parser.add_argument("--arm")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    comparison_path = repo_root / f"evals/harbor/comparisons/{args.comparison}.json"
    comparison = validate_comparison(json.loads(comparison_path.read_text()))
    arms = [arm for arm in comparison["arms"] if arm["host"] == args.host]
    if args.arm:
        arms = [arm for arm in arms if arm["id"] == args.arm]
    if not arms:
        raise SystemExit(f"comparison has no {args.host} arms")
    for arm in arms:
        arm["model"]["name"] = args.model

    run_id = datetime.now(timezone.utc).strftime("%Y-%m-%d__%H-%M-%S")
    run_dir = repo_root / f"evals/harbor/jobs/comparisons/{run_id}-{args.comparison}"
    run_dir.mkdir(parents=True)
    harbor_bin = Path(os.environ.get("HARBOR_BIN", repo_root / ".venv/bin/harbor"))
    results = [
        run_arm(args.comparison, arm, repetition, repo_root, harbor_bin, run_dir)
        for arm in arms
        for repetition in range(1, (args.repetitions or arm["repetitions"]) + 1)
    ]
    comparison_verifier = None
    if args.comparison == "peters-coexistence":
        records = {
            result["arm"]: result["coexistence_record"]
            for result in results
            if "coexistence_record" in result
        }
        if len(records) == 3:
            try:
                measured = verify_coexistence(records)
                comparison_verifier = {"status": "measured", **measured}
                for result in results:
                    arm = measured["arms"][result["arm"]]
                    outcome = arm["outcome"] if isinstance(arm["outcome"], dict) else {}
                    result["correctness"] = int(bool(outcome.get("preserves-save-contract")))
                    result["workflow_adherence"] = int(
                        not arm["duplicate_phases"] and not arm["conflicting_invocations"]
                    )
            except (KeyError, TypeError, ValueError) as exc:
                comparison_verifier = {"status": "failed", "malformed_record": str(exc)}
    output = {
        "comparison": args.comparison,
        "trials": results,
        "comparison_verifier": comparison_verifier,
        "summary": summarize_comparison(results),
    }
    write_trial_result(run_dir / "comparison.json", output)
    print(run_dir / "comparison.json")
    return 0 if all(result["status"] == "valid" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
