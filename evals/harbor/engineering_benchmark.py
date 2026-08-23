import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any


MANIFEST_FIELDS = {"id", "source", "resources", "outputs", "privacy"}
SOURCE_FIELDS = {"repository_env", "revision", "files"}
SOURCE_FILE_FIELDS = {"id", "path", "destination", "sha256", "privacy"}
RESOURCE_FIELDS = {"id", "path", "sha256", "privacy"}
OUTPUT_FIELDS = {"generated_path", "fixture_subdir", "evaluator_subdir", "audit_subdir"}
PRIVACY_FIELDS = {"committed", "generated", "subject", "evaluator"}
MATRIX_FIELDS = {"id", "scenario", "order_seed", "controller", "arms"}
ARM_FIELDS = {
    "id",
    "host",
    "model",
    "reasoning",
    "orchestration",
    "context",
    "fixture",
    "prompt",
    "verifier",
    "repetitions",
    "limits",
}
REASONING_LEVELS = {"low", "medium", "high", "xhigh", "max", "ultra"}
ORCHESTRATION = {"direct", "subagents-allowed"}
CODEX_REASONING_SUPPORT = {
    "gpt-5.6-sol": {"low", "medium", "high", "xhigh", "max", "ultra"},
    "gpt-5.6-terra": {"low", "medium", "high", "xhigh", "max", "ultra"},
    "gpt-5.6-luna": {"low", "medium", "high", "xhigh", "max"},
}
FORBIDDEN_WORKSPACE_PATHS = {
    "AGENTS.md",
    "CLAUDE.md",
    ".agents",
    ".claude",
    ".codex",
    ".superpowers",
    ".devcraft-evaluator",
    "openspec",
    "docs/adr",
}
SECRET_RE = re.compile(
    r"(?:sk-[A-Za-z0-9_-]{8,}|(?:token|secret|password)=[^\s]+)", re.IGNORECASE
)
UUID_RE = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    re.IGNORECASE,
)
PERSONAL_PATH_RE = re.compile(r"/(?:Users|home)/[^/\s]+")


def _safe_relative(value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty relative path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} must be a safe relative path")
    return path


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def tree_inventory(root: Path, *, include_git: bool = False) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if not include_git and relative.parts and relative.parts[0] == ".git":
            continue
        if path.is_symlink():
            entries.append({"path": relative.as_posix(), "symlink": os.readlink(path)})
        elif path.is_file():
            content = path.read_bytes()
            entries.append(
                {
                    "path": relative.as_posix(),
                    "size": len(content),
                    "sha256": sha256_bytes(content),
                    "executable": bool(path.stat().st_mode & 0o111),
                }
            )
    return entries


def tree_digest(root: Path, *, include_git: bool = False) -> str:
    inventory = tree_inventory(root, include_git=include_git)
    return sha256_bytes(json.dumps(inventory, sort_keys=True).encode())


def _unique_records(records: Any, fields: set[str], label: str) -> list[dict[str, Any]]:
    if not isinstance(records, list) or not records:
        raise ValueError(f"{label} must be a non-empty list")
    ids: set[str] = set()
    result: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict) or set(record) != fields:
            raise ValueError(f"{label}[{index}] fields must be exactly {sorted(fields)}")
        record_id = record.get("id")
        if not isinstance(record_id, str) or not re.fullmatch(r"[a-z0-9-]+", record_id):
            raise ValueError(f"{label}[{index}].id is invalid")
        if record_id in ids:
            raise ValueError(f"duplicate evidence id: {record_id}")
        ids.add(record_id)
        result.append(record)
    return result


def validate_manifest(value: Any, manifest_path: Path | None = None) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != MANIFEST_FIELDS:
        raise ValueError(f"manifest fields must be exactly {sorted(MANIFEST_FIELDS)}")
    if not isinstance(value["id"], str) or not re.fullmatch(r"[a-z0-9-]+", value["id"]):
        raise ValueError("manifest id is invalid")

    source = value["source"]
    if not isinstance(source, dict) or set(source) != SOURCE_FIELDS:
        raise ValueError(f"source fields must be exactly {sorted(SOURCE_FIELDS)}")
    if not re.fullmatch(r"[A-Z][A-Z0-9_]+", str(source["repository_env"])):
        raise ValueError("source.repository_env must be an environment variable name")
    if not re.fullmatch(r"[0-9a-f]{40}", str(source["revision"])):
        raise ValueError("source.revision must be a full commit id")
    files = _unique_records(source["files"], SOURCE_FILE_FIELDS, "source.files")
    destinations: set[Path] = set()
    for index, record in enumerate(files):
        _safe_relative(record["path"], f"source.files[{index}].path")
        destination = _safe_relative(
            record["destination"], f"source.files[{index}].destination"
        )
        if destination in destinations:
            raise ValueError(f"duplicate fixture destination: {destination}")
        destinations.add(destination)
        if not re.fullmatch(r"[0-9a-f]{64}", str(record["sha256"])):
            raise ValueError(f"source.files[{index}].sha256 is invalid")
        if record["privacy"] != "public-source":
            raise ValueError(f"source.files[{index}].privacy must be public-source")

    resources = _unique_records(value["resources"], RESOURCE_FIELDS, "resources")
    for index, record in enumerate(resources):
        path = _safe_relative(record["path"], f"resources[{index}].path")
        if not re.fullmatch(r"[0-9a-f]{64}", str(record["sha256"])):
            raise ValueError(f"resources[{index}].sha256 is invalid")
        if manifest_path is not None:
            resource_path = manifest_path.parent / path
            if not resource_path.is_file() or sha256_file(resource_path) != record["sha256"]:
                raise ValueError(f"resource drift: {record['id']}")

    outputs = value["outputs"]
    if not isinstance(outputs, dict) or set(outputs) != OUTPUT_FIELDS:
        raise ValueError(f"outputs fields must be exactly {sorted(OUTPUT_FIELDS)}")
    for field, path in outputs.items():
        _safe_relative(path, f"outputs.{field}")
    privacy = value["privacy"]
    if not isinstance(privacy, dict) or set(privacy) != PRIVACY_FIELDS:
        raise ValueError(f"privacy fields must be exactly {sorted(PRIVACY_FIELDS)}")
    if privacy != {
        "committed": "sanitized",
        "generated": "ignored",
        "subject": "fixture-only",
        "evaluator": "never-subject-visible",
    }:
        raise ValueError("privacy classifications are invalid")
    return value


def load_manifest(path: Path) -> dict[str, Any]:
    return validate_manifest(json.loads(path.read_text()), path)


def _git(repo: Path, *args: str, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        env={**os.environ, **(env or {})},
    )
    return completed.stdout.decode().strip()


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows))


def _write_synthetic_state(fixture: Path) -> None:
    home = fixture / "fixtures/codex-home"
    root_rows = [
        {"timestamp": "2026-07-30T00:00:00Z", "type": "session_meta", "payload": {"id": "root", "source": "cli", "cwd": "/workspace/project"}},
        {"timestamp": "2026-07-30T00:00:01Z", "type": "event_msg", "payload": {"type": "task_started", "turn_id": "root-turn"}},
        {"timestamp": "2026-07-30T00:00:02Z", "type": "turn_context", "payload": {"turn_id": "root-turn", "model": "gpt-5.6-terra", "effort": "high"}},
        {"timestamp": "2026-07-30T00:00:03Z", "type": "event_msg", "payload": {"type": "token_count", "info": {"last_token_usage": {"input_tokens": 1000000, "cached_input_tokens": 200000, "cache_write_input_tokens": 100000, "output_tokens": 50000, "reasoning_output_tokens": 10000, "total_tokens": 1050000}}}},
        {"timestamp": "2026-07-30T00:01:01Z", "type": "event_msg", "payload": {"type": "task_complete", "turn_id": "root-turn"}},
    ]
    child_rows = [
        {"timestamp": "2026-07-30T00:00:10Z", "type": "session_meta", "payload": {"id": "child", "parent_thread_id": "root", "source": {"subagent": {"thread_spawn": {"parent_thread_id": "root"}}}}},
        {"timestamp": "2026-07-30T00:00:11Z", "type": "event_msg", "payload": {"type": "task_started", "turn_id": "child-turn"}},
        {"timestamp": "2026-07-30T00:00:12Z", "type": "turn_context", "payload": {"turn_id": "child-turn", "model": "gpt-5.6-luna", "effort": "medium"}},
        {"timestamp": "2026-07-30T00:00:13Z", "type": "event_msg", "payload": {"type": "token_count", "info": {"last_token_usage": {"input_tokens": 10000, "cached_input_tokens": 2000, "cache_write_input_tokens": 1000, "output_tokens": 500, "reasoning_output_tokens": 100, "total_tokens": 10500}}}},
        {"timestamp": "2026-07-30T00:00:41Z", "type": "event_msg", "payload": {"type": "task_complete", "turn_id": "child-turn"}},
    ]
    _write_jsonl(home / "sessions/2026/07/30/root.jsonl", root_rows)
    _write_jsonl(home / "archived_sessions/child.jsonl", child_rows)
    _write_jsonl(
        home / "session_index.jsonl",
        [{"id": "root", "thread_name": "Synthetic report fixture", "updated_at": "2026-07-30T00:02:00Z"}],
    )


def _resource(manifest: dict[str, Any], resource_id: str, manifest_path: Path) -> Path:
    record = next(item for item in manifest["resources"] if item["id"] == resource_id)
    return manifest_path.parent / record["path"]


def _run_python_oracle(fixture: Path, evaluator: Path) -> None:
    evaluator.mkdir(parents=True)
    oracle_dir = evaluator / "oracle"
    oracle_dir.mkdir()
    shutil.copy2(fixture / "rollout_stats.py", oracle_dir / "rollout_stats.py")
    command = [
        "python3",
        str(fixture / "rollout_stats.py"),
        "root",
        "--codex-home",
        str(fixture / "fixtures/codex-home"),
    ]
    self_test = subprocess.run(
        ["python3", str(fixture / "rollout_stats.py"), "--self-test"],
        check=True,
        capture_output=True,
        text=True,
    )
    (evaluator / "python-self-test.txt").write_text(self_test.stdout)
    human = subprocess.run(command, check=True, capture_output=True, text=True)
    machine = subprocess.run([*command, "--json"], check=True, capture_output=True, text=True)
    (evaluator / "expected-report.txt").write_text(human.stdout)
    (evaluator / "expected-report.json").write_text(
        json.dumps(json.loads(machine.stdout), indent=2, sort_keys=True) + "\n"
    )


def scan_fixture(fixture: Path) -> list[str]:
    issues: list[str] = []
    for forbidden in FORBIDDEN_WORKSPACE_PATHS:
        if (fixture / forbidden).exists():
            issues.append(f"forbidden path: {forbidden}")
    alternates = fixture / ".git/objects/info/alternates"
    if alternates.exists():
        issues.append("git alternates are present")
    try:
        if _git(fixture, "remote"):
            issues.append("git remote is present")
        if _git(fixture, "rev-list", "--all", "--count") != "1":
            issues.append("fixture history is not a single fresh commit")
    except (OSError, subprocess.CalledProcessError):
        issues.append("fixture git repository is invalid")
    for entry in tree_inventory(fixture):
        path = fixture / entry["path"]
        try:
            text = path.read_text()
        except (OSError, UnicodeDecodeError):
            continue
        if "/Users/" in text:
            issues.append(f"personal path in {entry['path']}")
        if SECRET_RE.search(text):
            issues.append(f"credential-like value in {entry['path']}")
    return sorted(set(issues))


def build_fixture(
    manifest_path: Path,
    output_root: Path,
    source_repo: Path | None = None,
) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    if output_root.exists() and any(output_root.iterdir()):
        raise ValueError(f"generated output is not empty: {output_root}")
    output_root.mkdir(parents=True, exist_ok=True)
    source_repo = source_repo or Path(os.environ.get(manifest["source"]["repository_env"], ""))
    if not source_repo.is_dir():
        raise ValueError(f"source repository is unavailable; set {manifest['source']['repository_env']}")
    revision = _git(source_repo, "rev-parse", f"{manifest['source']['revision']}^{{commit}}")
    if revision != manifest["source"]["revision"]:
        raise ValueError("source revision drift")

    fixture = output_root / manifest["outputs"]["fixture_subdir"]
    evaluator = output_root / manifest["outputs"]["evaluator_subdir"]
    audit = output_root / manifest["outputs"]["audit_subdir"]
    fixture.mkdir()
    for record in manifest["source"]["files"]:
        content = subprocess.run(
            ["git", "-C", str(source_repo), "show", f"{revision}:{record['path']}"],
            check=True,
            capture_output=True,
        ).stdout
        if sha256_bytes(content) != record["sha256"]:
            raise ValueError(f"source digest drift: {record['id']}")
        destination = fixture / record["destination"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        mode = _git(source_repo, "ls-tree", revision, record["path"]).split()[0]
        destination.chmod(0o755 if mode == "100755" else 0o644)

    shutil.copy2(_resource(manifest, "fixture-readme", manifest_path), fixture / "README.md")
    _write_synthetic_state(fixture)
    _run_python_oracle(fixture, evaluator)

    subprocess.run(["git", "init", "--quiet", "--initial-branch=main", str(fixture)], check=True)
    _git(fixture, "add", ".")
    fixed_env = {
        "GIT_AUTHOR_NAME": "Devcraft Fixture",
        "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
        "GIT_COMMITTER_NAME": "Devcraft Fixture",
        "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
        "GIT_AUTHOR_DATE": "2000-01-01T00:00:00Z",
        "GIT_COMMITTER_DATE": "2000-01-01T00:00:00Z",
    }
    _git(fixture, "commit", "--quiet", "-m", "chore: create code-only fixture", env=fixed_env)
    issues = scan_fixture(fixture)
    if issues:
        raise ValueError("fixture contamination: " + "; ".join(issues))

    audit.mkdir()
    (audit / "source-map.json").write_text(
        json.dumps(
            {
                "revision": revision,
                "sources": [
                    {"id": item["id"], "git_path": item["path"], "sha256": item["sha256"]}
                    for item in manifest["source"]["files"]
                ],
            },
            indent=2,
        )
        + "\n"
    )
    record = {
        "benchmark": manifest["id"],
        "source_revision": revision,
        "fixture_head": _git(fixture, "rev-parse", "HEAD"),
        "fixture_tree": _git(fixture, "rev-parse", "HEAD^{tree}"),
        "fixture_digest": tree_digest(fixture),
        "manifest_digest": sha256_file(manifest_path),
        "resources": {item["id"]: item["sha256"] for item in manifest["resources"]},
        "inventory": tree_inventory(fixture),
    }
    (output_root / "build-record.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


def validate_matrix(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != MATRIX_FIELDS:
        raise ValueError(f"matrix fields must be exactly {sorted(MATRIX_FIELDS)}")
    if not isinstance(value["id"], str) or not re.fullmatch(r"[a-z0-9-]+", value["id"]):
        raise ValueError("matrix id is invalid")
    if value["scenario"] != "vanilla-port-v1":
        raise ValueError("matrix scenario must be vanilla-port-v1")
    if isinstance(value["order_seed"], bool) or not isinstance(value["order_seed"], int):
        raise ValueError("order_seed must be an integer")
    controller = value["controller"]
    if not isinstance(controller, dict) or set(controller) != {"host", "model", "reasoning"}:
        raise ValueError("controller requires host, model, and reasoning")
    if controller["host"] != "codex" or controller["reasoning"] not in REASONING_LEVELS:
        raise ValueError("controller must be a declared Codex configuration")
    arms = value["arms"]
    if not isinstance(arms, list) or not arms:
        raise ValueError("matrix requires arms")
    ids: set[str] = set()
    paired: dict[str, Any] | None = None
    for index, arm in enumerate(arms):
        if not isinstance(arm, dict) or set(arm) != ARM_FIELDS:
            raise ValueError(f"arms[{index}] fields must be exactly {sorted(ARM_FIELDS)}")
        if not isinstance(arm["id"], str) or not re.fullmatch(r"[a-z0-9-]+", arm["id"]):
            raise ValueError(f"arms[{index}].id is invalid")
        if arm["id"] in ids:
            raise ValueError("arm ids must be unique")
        ids.add(arm["id"])
        if arm["host"] != "codex":
            raise ValueError("vanilla port baseline is Codex-only")
        if not isinstance(arm["model"], str) or not arm["model"]:
            raise ValueError(f"arms[{index}].model is invalid")
        if arm["reasoning"] not in REASONING_LEVELS:
            raise ValueError(f"arms[{index}].reasoning is invalid")
        if arm["model"] not in CODEX_REASONING_SUPPORT or arm["reasoning"] not in CODEX_REASONING_SUPPORT[arm["model"]]:
            raise ValueError(f"arms[{index}] declares an unsupported Codex model/reasoning combination")
        if arm["orchestration"] not in ORCHESTRATION:
            raise ValueError(f"arms[{index}].orchestration is invalid")
        if arm["context"] != "code-only" or arm["fixture"] != value["scenario"]:
            raise ValueError("first baseline requires code-only vanilla-port-v1")
        if arm["prompt"] != "initial-prompt" or arm["verifier"] != "vanilla-port-v1":
            raise ValueError("arm prompt or verifier differs from the scenario")
        if isinstance(arm["repetitions"], bool) or not isinstance(arm["repetitions"], int) or arm["repetitions"] < 1:
            raise ValueError(f"arms[{index}].repetitions must be positive")
        limits = arm["limits"]
        if not isinstance(limits, dict) or set(limits) != {"turns", "timeout_sec", "reported_output_tokens"}:
            raise ValueError(f"arms[{index}].limits are invalid")
        if not all(isinstance(item, int) and not isinstance(item, bool) and item > 0 for item in limits.values()):
            raise ValueError(f"arms[{index}].limits must be positive integers")
        invariant = {key: arm[key] for key in ("host", "context", "fixture", "prompt", "verifier", "repetitions", "limits")}
        if paired is None:
            paired = invariant
        elif invariant != paired:
            raise ValueError("arms differ in an undeclared factor")
    return value


def load_matrix(path: Path) -> dict[str, Any]:
    return validate_matrix(json.loads(path.read_text()))


def schedule_trials(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    validate_matrix(matrix)
    return [
        {"arm": arm["id"], "repetition": repetition, "order": order}
        for order, (repetition, arm) in enumerate(
            (
                (repetition, arm)
                for repetition in range(1, max(item["repetitions"] for item in matrix["arms"]) + 1)
                for arm in matrix["arms"]
                if repetition <= arm["repetitions"]
            ),
            start=1,
        )
    ]


def codex_config(arm: dict[str, Any]) -> dict[str, Any]:
    return {
        "model_reasoning_effort": arm["reasoning"],
        "web_search": "disabled",
        "features": {"multi_agent": arm["orchestration"] == "subagents-allowed"},
    }


def codex_launch_args(arm: dict[str, Any]) -> list[str]:
    feature = "--enable" if arm["orchestration"] == "subagents-allowed" else "--disable"
    return [
        "--model",
        arm["model"],
        "-c",
        f"model_reasoning_effort={arm['reasoning']}",
        "-c",
        "web_search=disabled",
        feature,
        "multi_agent",
    ]


def validate_codex_runtime(arm: dict[str, Any], features_output: str) -> None:
    supported = CODEX_REASONING_SUPPORT.get(arm["model"], set())
    if arm["reasoning"] not in supported:
        raise ValueError("unsupported Codex model/reasoning combination")
    if arm["orchestration"] == "subagents-allowed" and not re.search(
        r"^multi_agent\s+stable\s+true$", features_output, re.MULTILINE
    ):
        raise ValueError("Codex multi-agent orchestration is unavailable")


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    if not isinstance(value, str):
        return value
    value = SECRET_RE.sub("[REDACTED]", value)
    value = PERSONAL_PATH_RE.sub("$HOME", value)
    return UUID_RE.sub("[ID]", value)


def privacy_issues(value: Any) -> list[str]:
    text = json.dumps(value, sort_keys=True)
    issues = []
    if SECRET_RE.search(text):
        issues.append("credential-like value")
    if PERSONAL_PATH_RE.search(text):
        issues.append("personal path")
    if UUID_RE.search(text):
        issues.append("private identifier")
    return issues


def prepare_vanilla_arm(arm: dict[str, Any], fixture: Path, destination: Path) -> dict[str, Any]:
    validate_matrix(
        {
            "id": "single-arm-validation",
            "scenario": "vanilla-port-v1",
            "order_seed": 0,
            "controller": {"host": "codex", "model": "controller", "reasoning": "medium"},
            "arms": [arm],
        }
    )
    if destination.exists():
        raise ValueError(f"destination already exists: {destination}")
    workspace = destination / "workspace"
    home = destination / "home"
    shutil.copytree(fixture, workspace, symlinks=True)
    home.mkdir(parents=True)
    config = codex_config(arm)
    config_path = destination / "codex-config.json"
    config_path.write_text(json.dumps(config, indent=2) + "\n")
    record = {
        "status": "passed",
        "arm": arm["id"],
        "authentication": "harbor-managed-codex-auth",
        "launch": {
            "host": "codex",
            "model": arm["model"],
            "reasoning": arm["reasoning"],
            "orchestration": arm["orchestration"],
            "config": config,
            "args": codex_launch_args(arm),
        },
        "allowed_environment_keys": ["CODEX_AUTH_JSON_PATH"],
        "workspace_digest": tree_digest(workspace),
        "home_inventory": tree_inventory(home, include_git=True),
        "config_digest": sha256_file(config_path),
    }
    (destination / "setup.json").write_text(json.dumps(redact(record), indent=2) + "\n")
    return record


def runtime_contamination(
    workspace: Path,
    home: Path,
    *,
    stage: str,
    extension_prompt: str,
) -> list[str]:
    issues: list[str] = []
    allowed_home = {".codex/auth.json", ".codex/config.toml"}
    for entry in tree_inventory(home, include_git=True):
        if entry["path"] not in allowed_home:
            issues.append(f"undeclared home file: {entry['path']}")
    for forbidden in FORBIDDEN_WORKSPACE_PATHS:
        if (workspace / forbidden).exists():
            issues.append(f"undeclared workspace path: {forbidden}")
    if stage == "initial":
        for entry in tree_inventory(workspace):
            try:
                if extension_prompt in (workspace / entry["path"]).read_text():
                    issues.append(f"extension prompt leaked into {entry['path']}")
            except (OSError, UnicodeDecodeError):
                pass
    return sorted(set(issues))


def authority_violation(command: str, local_origin: Path | None = None) -> str | None:
    lowered = command.lower()
    if re.search(r"\b(?:gh|hub)\b", lowered):
        return "hosted Git mutation is not allowed"
    if re.search(r"\b(?:cargo\s+publish|codesign|notarytool|signtool)\b", lowered):
        return "publication or signing is not allowed"
    if re.search(r"\bgit\s+push\b", lowered):
        if local_origin is None or str(local_origin.resolve()) not in command:
            return "only the declared local Git origin may receive pushes"
    if re.search(r"\b(?:curl|wget|git\s+clone)\b[^\n]*https?://", command) and not re.search(
        r"https://(?:chatgpt\.com|static\.crates\.io|index\.crates\.io|crates\.io)",
        command,
    ):
        return "undeclared network destination"
    return None
