import json
import shutil
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


def _source(repo_root: Path, value: str) -> Path:
    source = (repo_root / value).resolve()
    if not source.is_relative_to(repo_root.resolve()) or not source.exists():
        raise ValueError(f"declared source is unavailable: {value}")
    return source


def _merge_hooks(paths: list[Path]) -> dict[str, Any]:
    merged: dict[str, list[Any]] = {}
    for path in paths:
        value = json.loads(path.read_text())
        hooks = value.get("hooks") if isinstance(value, dict) else None
        if not isinstance(hooks, dict) or not all(
            isinstance(event, str) and isinstance(groups, list)
            for event, groups in hooks.items()
        ):
            raise ValueError(f"invalid hook definition: {path}")
        for event, groups in hooks.items():
            merged.setdefault(event, []).extend(groups)
    return {"hooks": merged}


def prepare_arm(arm: dict[str, Any], repo_root: Path, destination: Path) -> dict[str, Any]:
    if destination.exists():
        raise ValueError(f"destination already exists: {destination}")

    fixture = _source(repo_root, arm["fixture"])
    if not fixture.is_dir():
        raise ValueError("fixture must be a directory")
    workspace = destination / "workspace"
    shutil.copytree(fixture, workspace)

    remote_skills = [
        value for value in arm["skills"] if urlparse(value).scheme in {"http", "https"}
    ]
    skill_paths = [
        _source(repo_root, value) for value in arm["skills"] if value not in remote_skills
    ]
    if any(not path.is_dir() or not (path / "SKILL.md").is_file() for path in skill_paths):
        raise ValueError("each skill must be a directory containing SKILL.md")
    staged_skills = destination / "skills"
    for path in skill_paths:
        target = staged_skills / path.name
        if target.exists():
            raise ValueError(f"duplicate staged skill name: {path.name}")
        shutil.copytree(path, target)

    hook_paths = [_source(repo_root, value) for value in arm["hooks"]]
    hook_config = _merge_hooks(hook_paths)
    hook_config_path = None
    if hook_paths:
        config_dir = destination / "config"
        config_dir.mkdir()
        config_name = "hooks.json" if arm["host"] == "codex" else "settings.json"
        hook_config_path = config_dir / config_name
        hook_config_path.write_text(json.dumps(hook_config, indent=2) + "\n")

    manifest = {
        "arm": arm["id"],
        "setup": {
            "status": "passed",
            "fixture": arm["fixture"],
            "skills": arm["skills"],
            "remote_skills": remote_skills,
            "hooks": arm["hooks"],
            "skill_transport": "harbor-native",
            "hook_transport": "agent-config",
            "hook_config": str(hook_config_path) if hook_config_path else None,
        },
        "behavioral_score": None,
    }
    (destination / "setup.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest
