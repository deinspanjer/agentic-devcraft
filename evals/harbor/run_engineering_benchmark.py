import argparse
import copy
import importlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evals.harbor.comparison_summary import summarize_engineering_comparison
from evals.harbor.engineering_benchmark import (
    build_fixture,
    build_local_fixture,
    codex_config,
    load_manifest,
    load_matrix,
    local_fixture_source_digest,
    privacy_issues,
    redact,
    scan_fixture,
    schedule_trials,
    sha256_file,
    sha256_bytes,
    tree_digest,
    validate_codex_runtime,
)
from evals.harbor.trial_result import (
    build_engineering_result,
    offline_rescore,
    write_trial_result,
)
ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = ROOT / "evals/harbor/benchmarks/vanilla-port"
GENERATED = ROOT / "evals/harbor/generated/vanilla-port"
JOBS = ROOT / "evals/harbor/jobs/engineering"
NETWORK_HOSTS = ("chatgpt.com", "crates.io", "static.crates.io", "index.crates.io")
COMMON_HARNESS_FILES = (
    Path(__file__),
    ROOT / "evals/harbor/adaptive_agent.py",
    ROOT / "evals/harbor/controller.py",
    ROOT / "evals/harbor/trial_result.py",
    ROOT / "evals/harbor/comparison_summary.py",
)
PORT_SCENARIO = {
    "id": "vanilla-port-v1",
    "benchmark": BENCHMARK,
    "generated": GENERATED,
    "jobs": JOBS,
    "task_name": "agentic-devcraft/vanilla-port",
    "verifier_module": "evals.harbor.port_verifier",
    "verifier_path": ROOT / "evals/harbor/port_verifier.py",
    "reference": GENERATED / "evaluator/oracle/rollout_stats.py",
    "reference_argument": "verifier_oracle_path",
    "network_hosts": NETWORK_HOSTS,
    "build_kind": "pinned-repository",
    "resources": {"build_timeout_sec": 900, "cpus": 4, "memory_mb": 8192, "storage_mb": 8192},
}
DATE_FILTER_BENCHMARK = ROOT / "evals/harbor/benchmarks/date-filter"
DATE_FILTER_GENERATED = ROOT / "evals/harbor/generated/date-filter"
DATE_FILTER_SCENARIO = {
    "id": "date-filter-v1",
    "benchmark": DATE_FILTER_BENCHMARK,
    "generated": DATE_FILTER_GENERATED,
    "jobs": ROOT / "evals/harbor/jobs/engineering/date-filter",
    "task_name": "agentic-devcraft/date-filter",
    "verifier_module": "evals.harbor.date_filter_verifier",
    "verifier_path": ROOT / "evals/harbor/date_filter_verifier.py",
    "reference": DATE_FILTER_BENCHMARK / "rubric.json",
    "reference_argument": "verifier_reference_path",
    "network_hosts": ("chatgpt.com",),
    "build_kind": "committed-fixture",
    "resources": {"build_timeout_sec": 600, "cpus": 1, "memory_mb": 2048, "storage_mb": 4096},
}
SCENARIOS = {"vanilla-port": PORT_SCENARIO, "date-filter": DATE_FILTER_SCENARIO}
HARNESS_FILES = (*COMMON_HARNESS_FILES, BENCHMARK / "Dockerfile")


def scenario(name: str) -> dict[str, Any]:
    return SCENARIOS[name]


def create_task(
    fixture: Path,
    task: Path,
    timeout_sec: int,
    config: dict[str, Any] = PORT_SCENARIO,
) -> None:
    benchmark = config["benchmark"]
    resources = config["resources"]
    shutil.copytree(fixture, task / "environment/workspace")
    shutil.copy2(benchmark / "Dockerfile", task / "environment/Dockerfile")
    (task / "instruction.md").write_bytes((benchmark / "initial.md").read_bytes())
    (task / "tests").mkdir()
    test = task / "tests/test.sh"
    test.write_text(
        "#!/usr/bin/env bash\nset -euo pipefail\n"
        "mkdir -p /logs/verifier\nprintf '1\\n' > /logs/verifier/reward.txt\n"
    )
    test.chmod(0o755)
    (task / "task.toml").write_text(
        'schema_version = "1.4"\n\n'
        f'[task]\nname = "{config["task_name"]}"\nversion = "1.0.0"\n\n'
        f"[agent]\ntimeout_sec = {float(timeout_sec)}\nuser = \"node\"\n\n"
        '[verifier]\ntimeout_sec = 30.0\n\n'
        f'[environment]\nbuild_timeout_sec = {float(resources["build_timeout_sec"])}\n'
        f'cpus = {resources["cpus"]}\nmemory_mb = {resources["memory_mb"]}\n'
        f'storage_mb = {resources["storage_mb"]}\ngpus = 0\nmcp_servers = []\nnetwork_mode = "allowlist"\n'
        'allowed_hosts = []\n\n[environment.env]\n\n[verifier.env]\n\n[solution.env]\n'
    )


def codex_config_toml(arm: dict[str, Any]) -> str:
    config = codex_config(arm)
    enabled = "true" if config["features"]["multi_agent"] else "false"
    return (
        f'model_reasoning_effort = "{config["model_reasoning_effort"]}"\n'
        f'web_search = "{config["web_search"]}"\n\n'
        f"[features]\nmulti_agent = {enabled}\n"
    )


def trial_command(
    harbor: Path,
    task: Path,
    jobs: Path,
    arm: dict[str, Any],
    controller: dict[str, str],
    config_path: Path,
    scenario_config: dict[str, Any] = PORT_SCENARIO,
) -> list[str]:
    limits = arm["limits"]
    benchmark = scenario_config["benchmark"]
    command = [
        str(harbor),
        "run",
        "--path",
        str(task),
        "--agent",
        "evals.harbor.adaptive_agent:AdaptiveAgent",
        "--model",
        arm["model"],
        "--jobs-dir",
        str(jobs),
        "--n-concurrent",
        "1",
        "--delete",
        "--artifact",
        "/app",
        "--agent-kwarg",
        "subject_agent=codex",
        "--agent-kwarg",
        "controller_agent=codex",
        "--agent-kwarg",
        f"controller_model={controller['model']}",
        "--agent-kwarg",
        f"controller_reasoning={controller['reasoning']}",
        "--agent-kwarg",
        f"scenario_policy_path={benchmark / 'answer-policy.json'}",
        "--agent-kwarg",
        f"extension_prompt_path={benchmark / 'extension.md'}",
        "--agent-kwarg",
        f"verifier_contracts_path={benchmark / 'contracts.json'}",
        "--agent-kwarg",
        f"{scenario_config['reference_argument']}={scenario_config['reference']}",
        "--agent-kwarg",
        f"verifier_module={scenario_config['verifier_module']}",
        "--agent-kwarg",
        f"max_turns={limits['turns']}",
        "--agent-kwarg",
        f"max_reported_tokens={limits['reported_output_tokens']}",
        "--agent-kwarg",
        f"conversation_timeout_sec={limits['timeout_sec']}",
        "--agent-kwarg",
        f"reasoning_effort={arm['reasoning']}",
        "--agent-kwarg",
        f"config={config_path}",
    ]
    for host in scenario_config["network_hosts"]:
        command.extend(["--allow-agent-host", host])
    command.append("--yes")
    return command


def _single(path: Path, pattern: str) -> Path:
    matches = list(path.glob(pattern))
    if len(matches) != 1:
        raise RuntimeError(f"expected one {pattern}, found {len(matches)}")
    return matches[0]


def _trial_artifacts(harbor_root: Path) -> tuple[Path, Path]:
    agent_dir = _single(harbor_root, "**/agent/controller.json").parent
    result_path = agent_dir.parent / "result.json"
    if not result_path.is_file():
        raise RuntimeError("Harbor trial result is missing")
    return agent_dir, result_path


def stage_host_metrics(trajectories: dict[str, dict[str, Any]]) -> dict[str, Any]:
    metric_fields = {
        "input_tokens": "total_prompt_tokens",
        "cached_input_tokens": "total_cached_tokens",
        "output_tokens": "total_completion_tokens",
    }
    return {
        stage: {
            "duration_sec": None,
            "reported_tokens": {
                target: metrics.get(source)
                if isinstance(metrics.get(source), int)
                else None
                for target, source in metric_fields.items()
            },
        }
        for stage, trajectory in trajectories.items()
        if (metrics := trajectory.get("final_metrics") or {})
    }


def stage_trajectories(checkpoints: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    trajectories = {
        item["stage"]: item.get("trajectory", {"steps": []}) for item in checkpoints
    }
    if {"initial", "extension"} <= trajectories.keys():
        initial_steps = trajectories["initial"].get("steps") or []
        extension_steps = trajectories["extension"].get("steps") or []
        if extension_steps[: len(initial_steps)] != initial_steps:
            raise RuntimeError("extension trajectory does not continue initial trajectory")
        trajectories["extension"] = {
            **trajectories["extension"],
            "steps": extension_steps[len(initial_steps) :],
        }
    return trajectories


def normalize_trial(
    trial_root: Path,
    arm: dict[str, Any],
    repetition: int,
    execution_order: int,
    fixture_record: dict[str, Any],
    scenario_config: dict[str, Any] = PORT_SCENARIO,
) -> dict[str, Any]:
    benchmark = scenario_config["benchmark"]
    agent_dir, result_path = _trial_artifacts(trial_root / "harbor")
    harbor_result = json.loads(result_path.read_text())
    controller = json.loads((agent_dir / "controller.json").read_text())
    checkpoints = controller.get("checkpoints") or []
    trajectories = stage_trajectories(checkpoints)
    host_metrics = stage_host_metrics(trajectories)
    snapshots = {item["stage"]: agent_dir / "snapshots" / item["stage"] for item in checkpoints}
    configuration_path = trial_root / "codex-config.toml"
    provenance = {
        "trial_id": trial_root.name,
        "arm": arm["id"],
        "repetition": repetition,
        "execution_order": execution_order,
        "fixture": fixture_record["fixture_digest"],
        "prompts": {
            "initial": sha256_file(benchmark / "initial.md"),
            "extension": sha256_file(benchmark / "extension.md"),
        },
        "harness": {
            path.relative_to(ROOT).as_posix(): sha256_file(path)
            for path in (*COMMON_HARNESS_FILES, benchmark / "Dockerfile")
        },
        "verifier": {
            "implementation": sha256_file(scenario_config["verifier_path"]),
            "contracts": sha256_file(benchmark / "contracts.json"),
            "reference": sha256_file(scenario_config["reference"]),
        },
        "host": "codex",
        "model": {"name": arm["model"], "reasoning": arm["reasoning"], "orchestration": arm["orchestration"]},
        "configuration": sha256_file(configuration_path),
        "provisioned_content": {
            "workspace": tree_digest(trial_root / "task/environment/workspace"),
            "skills": sha256_bytes(b"[]"),
            "hooks": sha256_bytes(b"[]"),
            "plugins": sha256_bytes(b"[]"),
        },
        "historical_context": "none",
    }
    normalized = build_engineering_result(
        checkpoints=checkpoints,
        trajectories=trajectories,
        snapshot_paths=snapshots,
        provenance=provenance,
        host_metrics=host_metrics,
    )
    normalized["harbor"] = {
        "status": "failed" if harbor_result.get("exception_info") else "completed",
        "agent_info": harbor_result.get("agent_info"),
    }
    normalized = redact(normalized)
    if issues := privacy_issues(normalized):
        raise RuntimeError("normalized result failed privacy check: " + ", ".join(issues))
    return normalized


def run_trial(
    arm: dict[str, Any],
    repetition: int,
    execution_order: int,
    matrix: dict[str, Any],
    fixture_record: dict[str, Any],
    harbor: Path,
    run_dir: Path,
    auth_path: Path,
    scenario_config: dict[str, Any] = PORT_SCENARIO,
) -> dict[str, Any]:
    trial_root = run_dir / f"{execution_order:02d}-{arm['id']}-r{repetition}"
    task = trial_root / "task"
    create_task(
        scenario_config["generated"] / "fixture",
        task,
        arm["limits"]["timeout_sec"],
        scenario_config,
    )
    config_path = trial_root / "codex-config.toml"
    config_path.write_text(codex_config_toml(arm))
    command = trial_command(
        harbor,
        task,
        trial_root / "harbor",
        arm,
        matrix["controller"],
        config_path,
        scenario_config,
    )
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env={
            **os.environ,
            "CODEX_AUTH_JSON_PATH": str(auth_path),
            "PYTHONPATH": f"{ROOT}{os.pathsep}{os.environ.get('PYTHONPATH', '')}",
        },
    )
    if completed.returncode:
        raise RuntimeError(f"Harbor exited {completed.returncode}")
    result = normalize_trial(
        trial_root, arm, repetition, execution_order, fixture_record, scenario_config
    )
    write_trial_result(trial_root / "trial.json", result)
    return result


def benchmark_defects(result: dict[str, Any]) -> list[str]:
    defects = []
    if result.get("status") != "valid":
        defects.append("trial result is invalid")
    if result.get("harbor", {}).get("status") != "completed":
        defects.append("Harbor trial did not complete")
    stages = result.get("stages") or {}
    for stage, evidence in stages.items():
        termination = evidence.get("process", {}).get("termination")
        if termination in {"controller_error", "setup_contamination"}:
            defects.append(f"{stage} controller terminated with {termination}")
        if evidence.get("product", {}).get("status") in {"error", "not_run"}:
            defects.append(f"{stage} verifier did not run successfully")
    if (
        stages.get("initial", {}).get("process", {}).get("termination")
        in {"completed", "turn_limit"}
        and "extension" not in stages
    ):
        defects.append("completed initial stage has no extension evidence")
    return defects


def plan(matrix: dict[str, Any]) -> dict[str, Any]:
    schedule = schedule_trials(matrix)
    return {
        "matrix": matrix["id"],
        "host": "codex",
        "controller": matrix["controller"],
        "schedule": schedule,
        "arms": matrix["arms"],
        "authenticated_monetary_cost": "unavailable-subscription-usage",
        "subject_reported_output_token_ceiling": sum(
            arm["limits"]["reported_output_tokens"] * arm["repetitions"]
            for arm in matrix["arms"]
        ),
        "limit_semantics": {
            "turns": "per stage; bounded independently for each stage",
            "timeout_sec": "one wall-clock limit shared by both stages",
            "reported_output_tokens": "cumulative subject-output limit per trial",
            "controller": "bounded by the configured stage turns; controller tokens are not reported by the harness",
        },
        "note": "One repetition is plumbing evidence only; no authenticated trials run during planning.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=SCENARIOS, default="vanilla-port")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("plan")
    subparsers.add_parser("validate")
    build = subparsers.add_parser("build-fixture")
    build.add_argument("--source", type=Path)
    build.add_argument("--output", type=Path)
    run = subparsers.add_parser("run")
    run.add_argument("--execute", action="store_true")
    run.add_argument("--arm")
    run.add_argument("--repetitions", type=int)
    rescore = subparsers.add_parser("rescore")
    rescore.add_argument("trial", type=Path)
    rescore.add_argument("initial", type=Path)
    rescore.add_argument("extension", type=Path)
    rescore.add_argument("output", type=Path)
    args = parser.parse_args()
    scenario_config = scenario(args.scenario)
    benchmark = scenario_config["benchmark"]
    generated = scenario_config["generated"]
    verifier = importlib.import_module(scenario_config["verifier_module"])
    matrix = load_matrix(benchmark / "baseline-matrix.json")
    if args.command == "plan":
        print(json.dumps(plan(matrix), indent=2))
        return 0
    if args.command == "validate":
        verifier.load_contracts(benchmark / "contracts.json")
        record_path = generated / "build-record.json"
        if not record_path.is_file():
            raise SystemExit("generated fixture is absent; run build-fixture")
        record = json.loads(record_path.read_text())
        issues = scan_fixture(generated / "fixture")
        if record["fixture_digest"] != tree_digest(generated / "fixture"):
            issues.append("generated fixture digest drift")
        if scenario_config["build_kind"] == "pinned-repository":
            manifest = load_manifest(benchmark / "manifest.json")
            if record["manifest_digest"] != sha256_file(benchmark / "manifest.json"):
                issues.append("generated fixture manifest digest is stale")
            if record["source_revision"] != manifest["source"]["revision"]:
                issues.append("generated fixture source revision drift")
        elif record["source_digest"] != local_fixture_source_digest(benchmark / "fixture"):
            issues.append("committed fixture source drift")
        if issues:
            raise SystemExit("fixture validation failed: " + "; ".join(issues))
        print(json.dumps({"status": "passed", "fixture": record["fixture_digest"]}, indent=2))
        return 0
    if args.command == "build-fixture":
        output = args.output or generated
        if scenario_config["build_kind"] == "pinned-repository":
            if args.source is None:
                raise SystemExit("vanilla-port build-fixture requires --source")
            record = build_fixture(
                benchmark / "manifest.json", output, args.source.resolve()
            )
        else:
            if args.source is not None:
                raise SystemExit("date-filter uses its committed fixture; omit --source")
            record = build_local_fixture(benchmark / "fixture", output)
        print(json.dumps(record, indent=2))
        return 0
    if args.command == "rescore":
        offline_rescore(
            original_trial=args.trial,
            snapshots={"initial": args.initial, "extension": args.extension},
            oracle_script=scenario_config["reference"],
            contracts_path=benchmark / "contracts.json",
            output=args.output,
            verifier_module=scenario_config["verifier_module"],
        )
        print(args.output)
        return 0
    if not args.execute:
        raise SystemExit("authenticated execution requires --execute after reviewing plan")
    if args.repetitions is not None:
        if args.repetitions < 1:
            raise SystemExit("repetitions must be positive")
        matrix = copy.deepcopy(matrix)
        for arm in matrix["arms"]:
            arm["repetitions"] = args.repetitions
    if args.arm:
        matrix = copy.deepcopy(matrix)
        matrix["arms"] = [arm for arm in matrix["arms"] if arm["id"] == args.arm]
        if not matrix["arms"]:
            raise SystemExit(f"unknown arm: {args.arm}")
    auth = Path(os.environ.get("CODEX_AUTH_JSON_PATH", Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "auth.json"))
    if not auth.is_file():
        raise SystemExit(f"Codex auth file is unavailable: {auth}")
    if not (generated / "build-record.json").is_file():
        raise SystemExit("build the fixture before running authenticated trials")
    features = subprocess.run(["codex", "features", "list"], capture_output=True, text=True, check=True).stdout
    for arm in matrix["arms"]:
        validate_codex_runtime(arm, features)
    run_id = datetime.now(timezone.utc).strftime("%Y-%m-%d__%H-%M-%S")
    run_dir = scenario_config["jobs"] / f"{run_id}-{matrix['id']}"
    run_dir.mkdir(parents=True)
    harbor = Path(os.environ.get("HARBOR_BIN", ROOT / ".venv/bin/harbor"))
    fixture_record = json.loads((generated / "build-record.json").read_text())
    by_id = {arm["id"]: arm for arm in matrix["arms"]}
    results = []
    for item in schedule_trials(matrix):
        result = run_trial(
            by_id[item["arm"]],
            item["repetition"],
            item["order"],
            matrix,
            fixture_record,
            harbor,
            run_dir,
            auth,
            scenario_config,
        )
        results.append(result)
        if defects := benchmark_defects(result):
            output = {
                "comparison": matrix["id"],
                "trials": results,
                "summary": summarize_engineering_comparison(results, plumbing=False),
                "execution": {"status": "blocked", "defects": defects},
            }
            write_trial_result(run_dir / "comparison.json", output)
            raise RuntimeError("benchmark blocked: " + "; ".join(defects))
    output = {
        "comparison": matrix["id"],
        "trials": results,
        "summary": summarize_engineering_comparison(results, plumbing=all(arm["repetitions"] == 1 for arm in matrix["arms"])),
    }
    write_trial_result(run_dir / "comparison.json", output)
    print(run_dir / "comparison.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
