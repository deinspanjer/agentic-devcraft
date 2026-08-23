from pathlib import Path
from typing import Any


def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def verify_workflow_ownership(
    before: Path, after: Path, expected: dict[str, Any]
) -> dict[str, Any]:
    before_files = _files(before)
    after_files = _files(after)
    changed = sorted(
        path
        for path in set(before_files) | set(after_files)
        if before_files.get(path) != after_files.get(path)
    )
    detours = [path for path in changed if path.startswith(".devcraft/")]
    duplicates = [path for path in changed if path.startswith("docs/plans/")]
    unauthorized = sorted(set(changed) - set(expected["allowed_changes"]))
    required = {
        path: after_files.get(path) == content.encode()
        for path, content in expected["files"].items()
    }
    return {
        "workflow_result": {"passed": all(required.values()), "files": required},
        "detours": {"passed": not detours, "paths": detours},
        "duplicate_workflow_entry": {"passed": not duplicates, "paths": duplicates},
        "unauthorized_workflow_mutation": {
            "passed": not unauthorized,
            "paths": unauthorized,
        },
    }
