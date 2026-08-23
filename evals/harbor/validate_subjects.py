import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED = {
    "id",
    "source",
    "hosts",
    "unsupported",
    "network_hosts",
    "install",
    "configuration",
    "discovery",
    "use_probe",
}
HOSTS = {"codex", "claude-code"}


def _command(value: Any, label: str) -> None:
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ValueError(f"{label} must be a non-empty argv list")


def validate_subject(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != REQUIRED:
        missing = sorted(REQUIRED - set(value if isinstance(value, dict) else {}))
        raise ValueError(f"subject fields must be exactly {sorted(REQUIRED)}; missing={missing}")

    if not isinstance(value["id"], str) or not re.fullmatch(r"[a-z0-9-]+", value["id"]):
        raise ValueError("id must contain lowercase letters, numbers, and hyphens")

    source = value["source"]
    if not isinstance(source, dict) or set(source) != {"repository", "revision"}:
        raise ValueError("source requires repository and revision")
    if not all(isinstance(source[key], str) and source[key] for key in source):
        raise ValueError("source values must be non-empty strings")

    hosts = value["hosts"]
    if not isinstance(hosts, list) or not hosts or len(hosts) != len(set(hosts)):
        raise ValueError("hosts must be a non-empty unique list")
    if not set(hosts) <= HOSTS:
        raise ValueError(f"unsupported host name; expected one of {sorted(HOSTS)}")

    unsupported = value["unsupported"]
    if not isinstance(unsupported, dict) or set(hosts) & set(unsupported):
        raise ValueError("supported and unsupported hosts must not overlap")
    if set(hosts) | set(unsupported) != HOSTS:
        raise ValueError("every known host must be supported or explicitly unsupported")
    for host, outcome in unsupported.items():
        if not isinstance(outcome, dict) or set(outcome) != {"reason", "evidence"}:
            raise ValueError(f"unsupported.{host} requires reason and evidence")
        evidence = outcome["evidence"]
        if not isinstance(outcome["reason"], str) or not outcome["reason"]:
            raise ValueError(f"unsupported.{host}.reason must be non-empty")
        if not isinstance(evidence, list) or not evidence or not all(
            isinstance(citation, str) and citation.startswith("https://")
            for citation in evidence
        ):
            raise ValueError(f"unsupported.{host}.evidence must contain source URLs")

    for field in ("network_hosts", "install", "configuration", "discovery", "use_probe"):
        mapping = value[field]
        if not isinstance(mapping, dict) or set(mapping) != set(hosts):
            raise ValueError(f"{field} must define exactly the declared hosts")

    for host in hosts:
        network_hosts = value["network_hosts"][host]
        if not isinstance(network_hosts, list) or not all(
            isinstance(name, str) and re.fullmatch(r"(?:\*\.)?[a-z0-9.-]+", name)
            for name in network_hosts
        ):
            raise ValueError(f"network_hosts.{host} must contain hostnames")
        commands = value["install"][host]
        if not isinstance(commands, list) or not commands:
            raise ValueError(f"install.{host} must contain at least one command")
        for index, command in enumerate(commands):
            _command(command, f"install.{host}[{index}]")
        configuration = value["configuration"][host]
        if not isinstance(configuration, dict) or not all(
            isinstance(key, str)
            and key
            and isinstance(setting, str)
            for key, setting in configuration.items()
        ):
            raise ValueError(f"configuration.{host} must contain environment strings")
        for field in ("discovery", "use_probe"):
            probe = value[field][host]
            required = {"command", "expect"} if field == "discovery" else {"prompt", "expect"}
            allowed = required if field == "discovery" else required | {"expect_paths"}
            if not isinstance(probe, dict) or not required <= set(probe) <= allowed:
                raise ValueError(f"{field}.{host} requires {sorted(required)}")
            if field == "discovery":
                _command(probe["command"], f"discovery.{host}.command")
            if not isinstance(probe["expect"], str):
                raise ValueError(f"{field}.{host}.expect must be a string")
            if field == "use_probe" and (
                not probe["prompt"] or not probe["expect"]
            ):
                raise ValueError(f"{field}.{host} values must be non-empty strings")
            if "expect_paths" in probe and (
                not isinstance(probe["expect_paths"], list)
                or not probe["expect_paths"]
                or not all(
                    isinstance(path, str) and path.startswith("/app/")
                    for path in probe["expect_paths"]
                )
            ):
                raise ValueError(f"{field}.{host}.expect_paths must contain /app paths")

    return value


def load_subject(path: Path) -> dict[str, Any]:
    return validate_subject(json.loads(path.read_text()))


def main(paths: list[str]) -> int:
    if not paths:
        print("usage: validate_subjects.py <subject.json> [...]", file=sys.stderr)
        return 2
    for raw_path in paths:
        try:
            load_subject(Path(raw_path))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"{raw_path}: {exc}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
