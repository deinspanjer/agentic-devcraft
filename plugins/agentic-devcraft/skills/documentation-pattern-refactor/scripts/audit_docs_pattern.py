#!/usr/bin/env python3
"""Audit workspace markdown docs against an audience-based documentation pattern."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALWAYS_EXCLUDED_PARTS = {
    ".git",
    ".venv",
    ".pytest_cache",
    "node_modules",
    "__pycache__",
    ".mypy_cache",
    ".idea",
}

CORE_TRIO = ("README.md", "USERS.md", "DEVELOPERS.md")
ROOT_ONLY_DOCS = {"TODO.md", "AGENTS.md"}
AUDIENCE_DOCS = {"README.md", "USERS.md", "DEVELOPERS.md", "TODO.md"}

OPERATOR_KEYWORDS = {
    "operator",
    "workflow",
    "runbook",
    "troubleshooting",
    "runtime",
    "hotkey",
    "screen",
    "launch",
    "configuration",
    "install",
    "startup",
    "flag",
    "flags",
    "env",
    "ui",
}

DEVELOPER_KEYWORDS = {
    "architecture",
    "implementation",
    "test",
    "pytest",
    "debug",
    "refactor",
    "module",
    "code",
    "dependency",
    "local setup",
    "schema",
    "build",
    "design",
}

ENTRYPOINT_KEYWORDS = {
    "overview",
    "documentation",
    "capabilities",
    "links",
    "getting started",
    "summary",
    "introduction",
}

TODO_OPERATIONAL_KEYWORDS = {
    "install",
    "run",
    "workflow",
    "config",
    "troubleshooting",
    "usage",
    "launch",
}

HEADING_HINTS = {
    "USERS.md": {
        "install",
        "setup",
        "start",
        "startup",
        "run",
        "runtime",
        "operator",
        "workflow",
        "runbook",
        "troubleshooting",
        "flag",
        "flags",
        "env",
        "config",
        "configuration",
        "ui",
    },
    "DEVELOPERS.md": {
        "architecture",
        "implementation",
        "internals",
        "design",
        "schema",
        "build",
        "test",
        "testing",
        "debug",
        "contributing",
        "extension",
        "standards",
        "module",
    },
    "README.md": {
        "overview",
        "introduction",
        "summary",
        "capabilities",
        "documentation",
        "quickstart",
    },
    "TODO.md": {"todo", "backlog", "deferred", "future", "roadmap", "next"},
}


@dataclass
class Divergence:
    rule_id: str
    severity: str
    category: str
    path: str
    summary: str
    evidence: str
    recommended_action: str
    requires_confirmation: bool

    def as_dict(self) -> dict[str, Any]:
        base = {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "category": self.category,
            "path": self.path,
            "summary": self.summary,
            "evidence": self.evidence,
            "recommended_action": self.recommended_action,
            "requires_confirmation": self.requires_confirmation,
        }
        digest = hashlib.sha1(
            f"{self.rule_id}|{self.path}|{self.summary}".encode("utf-8")
        ).hexdigest()[:12]
        base["id"] = f"div-{digest}"
        return base


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Workspace root to audit")
    parser.add_argument(
        "--scope",
        choices=("root", "all"),
        default="root",
        help="Audit scope: root-only by default, or include module triad checks with 'all'",
    )
    parser.add_argument(
        "--strictness",
        choices=("balanced", "strict", "advisory"),
        default="balanced",
        help="Divergence severity profile",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for audit artifacts (default: <root>/.agents/artifacts/doc-pattern)",
    )
    parser.add_argument(
        "--include-hidden-dirs",
        action="store_true",
        help=(
            "Include markdown files under all leading-dot directories. "
            "Default behavior excludes leading-dot directories to reduce false positives."
        ),
    )
    parser.add_argument(
        "--include-hidden-dir",
        action="append",
        default=[],
        help=(
            "Include markdown files under specific leading-dot directory names "
            "(repeatable, for example: --include-hidden-dir .codex)."
        ),
    )
    return parser.parse_args()


def normalize_hidden_includes(values: list[str]) -> set[str]:
    includes: set[str] = set()
    for value in values:
        item = value.strip()
        if not item:
            continue
        if not item.startswith("."):
            item = f".{item}"
        includes.add(item)
    return includes


def is_excluded(
    path: Path,
    include_hidden_dirs: bool = False,
    include_hidden_named: set[str] | None = None,
) -> bool:
    include_hidden_named = include_hidden_named or set()
    for part in path.parts:
        if part in ALWAYS_EXCLUDED_PARTS:
            return True
        if part.startswith("."):
            if include_hidden_dirs:
                continue
            if part in include_hidden_named:
                continue
            return True
    return False


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9_\-]+", text.lower())


def count_hits(tokens: list[str], keyword_set: set[str]) -> int:
    joined = " ".join(tokens)
    hits = 0
    for key in keyword_set:
        if " " in key:
            hits += joined.count(key)
        else:
            hits += tokens.count(key)
    return hits


def normalize_lines(text: str) -> set[str]:
    output: set[str] = set()
    for line in text.splitlines():
        line = line.strip().lower()
        if len(line) < 40:
            continue
        line = re.sub(r"\s+", " ", line)
        output.add(line)
    return output


def adjust_severity(severity: str, strictness: str) -> str:
    if strictness == "balanced":
        return severity
    if strictness == "strict":
        return {"low": "medium", "medium": "high", "high": "high"}[severity]
    return {"low": "low", "medium": "low", "high": "medium"}[severity]


def collect_markdown(
    root: Path,
    include_hidden_dirs: bool = False,
    include_hidden_named: set[str] | None = None,
) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if is_excluded(
            rel,
            include_hidden_dirs=include_hidden_dirs,
            include_hidden_named=include_hidden_named,
        ):
            continue
        files.append(path)
    return sorted(files)


def extract_sections(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    headings: list[tuple[int, str]] = []
    for idx, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            headings.append((idx + 1, match.group(2).strip()))

    if not headings:
        return [
            {
                "heading": "Document Body",
                "line": 1,
                "content": text.strip(),
            }
        ]

    sections: list[dict[str, Any]] = []
    for i, (line_no, heading) in enumerate(headings):
        start_idx = line_no
        end_idx = headings[i + 1][0] - 1 if i + 1 < len(headings) else len(lines)
        content = "\n".join(lines[start_idx:end_idx]).strip()
        sections.append({"heading": heading, "line": line_no, "content": content})
    return sections


def classify_target_doc(
    source_doc: str,
    heading: str,
    section_tokens: list[str],
) -> tuple[str, str]:
    heading_tokens = tokenize(heading)
    combined_tokens = heading_tokens + section_tokens
    op_hits = count_hits(combined_tokens, OPERATOR_KEYWORDS)
    dev_hits = count_hits(combined_tokens, DEVELOPER_KEYWORDS)
    entry_hits = count_hits(combined_tokens, ENTRYPOINT_KEYWORDS)

    hints: dict[str, int] = {}
    heading_set = set(heading_tokens)
    for target_doc, keywords in HEADING_HINTS.items():
        hints[target_doc] = len(heading_set & keywords)

    hint_target = max(hints, key=lambda key: hints[key]) if hints else source_doc
    if hints.get(hint_target, 0) >= 2:
        return hint_target, (
            f"Heading terms favor {hint_target} (heading_match={hints[hint_target]}, "
            f"operator_hits={op_hits}, developer_hits={dev_hits}, entry_hits={entry_hits})."
        )

    if source_doc == "README.md":
        if dev_hits >= op_hits + 2 and dev_hits >= 3:
            return "DEVELOPERS.md", (
                f"Developer indicators outweigh entrypoint intent (developer_hits={dev_hits}, "
                f"operator_hits={op_hits}, entry_hits={entry_hits})."
            )
        if op_hits >= dev_hits + 2 and op_hits >= 3:
            return "USERS.md", (
                f"Operator/runbook indicators outweigh entrypoint intent (operator_hits={op_hits}, "
                f"developer_hits={dev_hits}, entry_hits={entry_hits})."
            )
        return "README.md", (
            f"Entry-point indicators are sufficient for README placement "
            f"(entry_hits={entry_hits}, operator_hits={op_hits}, developer_hits={dev_hits})."
        )

    if source_doc == "USERS.md":
        if dev_hits >= op_hits + 2 and dev_hits >= 3:
            return "DEVELOPERS.md", (
                f"Section appears implementation-heavy for USERS.md "
                f"(developer_hits={dev_hits}, operator_hits={op_hits})."
            )
        return "USERS.md", (
            f"Section remains operator-focused for USERS.md "
            f"(operator_hits={op_hits}, developer_hits={dev_hits})."
        )

    if source_doc == "DEVELOPERS.md":
        if op_hits >= dev_hits + 2 and op_hits >= 3:
            return "USERS.md", (
                f"Section appears runbook-heavy for DEVELOPERS.md "
                f"(operator_hits={op_hits}, developer_hits={dev_hits})."
            )
        return "DEVELOPERS.md", (
            f"Section remains developer-focused for DEVELOPERS.md "
            f"(developer_hits={dev_hits}, operator_hits={op_hits})."
        )

    if source_doc == "TODO.md":
        return "TODO.md", "TODO content stays in TODO unless explicitly converted to current-state docs."

    if op_hits >= dev_hits + 2 and op_hits >= max(entry_hits, 2):
        return "USERS.md", (
            f"Operator indicators dominate section classification "
            f"(operator_hits={op_hits}, developer_hits={dev_hits}, entry_hits={entry_hits})."
        )
    if dev_hits >= op_hits + 2 and dev_hits >= max(entry_hits, 2):
        return "DEVELOPERS.md", (
            f"Developer indicators dominate section classification "
            f"(developer_hits={dev_hits}, operator_hits={op_hits}, entry_hits={entry_hits})."
        )
    return "README.md", (
        f"Fallback to README entrypoint classification "
        f"(entry_hits={entry_hits}, operator_hits={op_hits}, developer_hits={dev_hits})."
    )


def classify_target_section(target_doc: str, heading: str) -> str:
    normalized = "-".join(tokenize(heading))

    if target_doc == "README.md":
        if any(term in normalized for term in ("overview", "intro", "summary")):
            return "overview"
        if any(term in normalized for term in ("doc", "link", "references")):
            return "documentation"
        return "capabilities"

    if target_doc == "USERS.md":
        if any(term in normalized for term in ("install", "setup", "startup")):
            return "installation-and-startup"
        if any(term in normalized for term in ("config", "flag", "env", "runtime")):
            return "configuration-and-runtime-flags"
        if any(term in normalized for term in ("troubleshoot", "error", "debug")):
            return "troubleshooting"
        return "operator-workflows"

    if target_doc == "DEVELOPERS.md":
        if any(term in normalized for term in ("architect", "schema", "design")):
            return "architecture"
        if any(term in normalized for term in ("setup", "build", "local")):
            return "local-setup-build"
        if any(term in normalized for term in ("test", "debug", "lint")):
            return "test-and-debug"
        return "implementation-standards"

    return "future-work"


def build_classification_rows(
    root: Path,
    files: list[Path],
    text_cache: dict[Path, str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for path in files:
        if path.name not in AUDIENCE_DOCS:
            continue
        rel_path = path.relative_to(root).as_posix()
        sections = extract_sections(text_cache[path])

        for section in sections:
            section_tokens = tokenize(section["content"])
            target_doc, rationale = classify_target_doc(
                path.name, section["heading"], section_tokens
            )
            target_section = classify_target_section(target_doc, section["heading"])
            move_required = target_doc != path.name

            rows.append(
                {
                    "source_file": rel_path,
                    "source_heading": section["heading"],
                    "source_line": section["line"],
                    "target_file": target_doc,
                    "target_section": target_section,
                    "rationale": rationale,
                    "move_required": move_required,
                }
            )

    return rows


def build_inventory(root: Path, files: list[Path], scope: str) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for path in files:
        rel = path.relative_to(root).as_posix()
        role = "other"
        if path.name in CORE_TRIO:
            role = path.name.replace(".md", "").lower()
        elif path.name in ROOT_ONLY_DOCS:
            role = path.name.replace(".md", "").lower()
        records.append(
            {
                "path": rel,
                "name": path.name,
                "directory": str(Path(rel).parent),
                "size_bytes": path.stat().st_size,
                "role_hint": role,
            }
        )

    modules: dict[str, set[str]] = defaultdict(set)
    for path in files:
        if path.name in CORE_TRIO:
            modules[str(path.parent.relative_to(root))].add(path.name)

    root_present = modules.get(".", set())
    module_rows = [
        {
            "module": ".",
            "present": sorted(root_present),
            "missing": [name for name in CORE_TRIO if name not in root_present],
        }
    ]
    if scope == "all":
        for module, present in sorted(modules.items()):
            if module == ".":
                continue
            missing = [name for name in CORE_TRIO if name not in present]
            module_rows.append(
                {
                    "module": module,
                    "present": sorted(present),
                    "missing": missing,
                }
            )

    return {
        "root": str(root),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "markdown_files": records,
        "modules": module_rows,
    }


def detect_divergences(
    root: Path,
    files: list[Path],
    strictness: str,
    scope: str,
    classification_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    divergences: list[Divergence] = []
    text_cache: dict[Path, str] = {path: read_text(path) for path in files}
    token_cache: dict[Path, list[str]] = {
        path: tokenize(text) for path, text in text_cache.items()
    }

    modules: dict[Path, set[str]] = defaultdict(set)
    for path in files:
        if path.name in CORE_TRIO:
            modules[path.parent].add(path.name)

    root_present = modules.get(root, set())
    root_missing = [name for name in CORE_TRIO if name not in root_present]
    if root_missing:
        divergences.append(
            Divergence(
                rule_id="missing_core_doc",
                severity=adjust_severity("high", strictness),
                category="structure",
                path=".",
                summary="Root documentation set is incomplete.",
                evidence=f"Present: {sorted(root_present)}; missing: {root_missing}",
                recommended_action=(
                    "Create the missing root audience docs (README.md, USERS.md, DEVELOPERS.md)."
                ),
                requires_confirmation=True,
            )
        )

    if scope == "all":
        for module_path, present in sorted(modules.items()):
            if module_path == root:
                continue
            missing = [name for name in CORE_TRIO if name not in present]
            if not missing:
                continue
            rel_module = module_path.relative_to(root).as_posix()
            divergences.append(
                Divergence(
                    rule_id="missing_core_doc",
                    severity=adjust_severity("high", strictness),
                    category="structure",
                    path=rel_module,
                    summary="Module-level documentation set is incomplete.",
                    evidence=f"Present: {sorted(present)}; missing: {missing}",
                    recommended_action=(
                        "Add the missing audience docs or consolidate the module docs into a single owner location."
                    ),
                    requires_confirmation=True,
                )
            )

    for path in files:
        rel = path.relative_to(root)
        rel_str = rel.as_posix()
        if path.name == "TODO.md" and rel.parent != Path("."):
            divergences.append(
                Divergence(
                    rule_id="todo_not_top_level",
                    severity=adjust_severity("high", strictness),
                    category="structure",
                    path=rel_str,
                    summary="TODO.md should stay at repository root.",
                    evidence="Found TODO.md in a subdirectory.",
                    recommended_action="Move TODO content to the top-level TODO.md and remove nested TODO files.",
                    requires_confirmation=True,
                )
            )

    for path in files:
        if path.name not in AUDIENCE_DOCS:
            continue
        rel_str = path.relative_to(root).as_posix()
        tokens = token_cache[path]
        op_hits = count_hits(tokens, OPERATOR_KEYWORDS)
        dev_hits = count_hits(tokens, DEVELOPER_KEYWORDS)
        entry_hits = count_hits(tokens, ENTRYPOINT_KEYWORDS)

        if path.name == "README.md" and (op_hits >= 8 or dev_hits >= 8):
            evidence = (
                "README keyword balance suggests deep procedural content "
                f"(operator_hits={op_hits}, developer_hits={dev_hits}, entry_hits={entry_hits})."
            )
            divergences.append(
                Divergence(
                    rule_id="audience_mismatch",
                    severity=adjust_severity("medium", strictness),
                    category="audience",
                    path=rel_str,
                    summary="README appears to contain audience-specific procedural detail.",
                    evidence=evidence,
                    recommended_action=(
                        "Keep README high-level and move operational/developer procedures into USERS.md or DEVELOPERS.md."
                    ),
                    requires_confirmation=True,
                )
            )

        if path.name == "USERS.md" and dev_hits > (op_hits + 6):
            evidence = (
                f"USERS appears developer-heavy (operator_hits={op_hits}, developer_hits={dev_hits})."
            )
            divergences.append(
                Divergence(
                    rule_id="audience_mismatch",
                    severity=adjust_severity("medium", strictness),
                    category="audience",
                    path=rel_str,
                    summary="USERS.md appears to include developer-focused implementation detail.",
                    evidence=evidence,
                    recommended_action=(
                        "Move architecture/implementation sections into DEVELOPERS.md and keep USERS.md operator-focused."
                    ),
                    requires_confirmation=True,
                )
            )

        if path.name == "DEVELOPERS.md" and op_hits > (dev_hits + 6):
            evidence = (
                f"DEVELOPERS appears operator-heavy (operator_hits={op_hits}, developer_hits={dev_hits})."
            )
            divergences.append(
                Divergence(
                    rule_id="audience_mismatch",
                    severity=adjust_severity("medium", strictness),
                    category="audience",
                    path=rel_str,
                    summary="DEVELOPERS.md appears to include operator runbook content.",
                    evidence=evidence,
                    recommended_action="Move runbook and runtime workflow sections into USERS.md.",
                    requires_confirmation=True,
                )
            )

        if path.name == "TODO.md":
            todo_ops_hits = count_hits(tokens, TODO_OPERATIONAL_KEYWORDS)
            status_markers = tokens.count("status")
            if todo_ops_hits >= 10 and status_markers < 2:
                evidence = (
                    "TODO content includes many operational terms "
                    f"(operational_hits={todo_ops_hits}, status_markers={status_markers})."
                )
                divergences.append(
                    Divergence(
                        rule_id="audience_mismatch",
                        severity=adjust_severity("medium", strictness),
                        category="backlog",
                        path=rel_str,
                        summary="TODO.md may contain current-state runbook details instead of backlog items.",
                        evidence=evidence,
                        recommended_action=(
                            "Keep TODO actionable and future-facing; move current behavior docs into USERS.md/DEVELOPERS.md."
                        ),
                        requires_confirmation=True,
                    )
                )

    normalized_lines = {path: normalize_lines(text_cache[path]) for path in files}
    doc_candidates = [path for path in files if path.name in {"README.md", "USERS.md", "DEVELOPERS.md"}]
    for idx, left in enumerate(doc_candidates):
        for right in doc_candidates[idx + 1 :]:
            lset = normalized_lines[left]
            rset = normalized_lines[right]
            if not lset or not rset:
                continue
            overlap = lset & rset
            min_size = min(len(lset), len(rset))
            if min_size == 0:
                continue
            ratio = len(overlap) / min_size
            if len(overlap) >= 8 and ratio >= 0.35:
                left_rel = left.relative_to(root).as_posix()
                right_rel = right.relative_to(root).as_posix()
                divergences.append(
                    Divergence(
                        rule_id="significant_duplication",
                        severity=adjust_severity("medium", strictness),
                        category="duplication",
                        path=f"{left_rel} <-> {right_rel}",
                        summary="Substantial duplicate prose detected across audience docs.",
                        evidence=f"Overlapping long lines: {len(overlap)} ({ratio:.0%} of smaller document).",
                        recommended_action="Consolidate duplicate sections into one owner doc and link from the others.",
                        requires_confirmation=True,
                    )
                )

    for row in classification_rows:
        if not row["move_required"]:
            continue
        source_ref = f"{row['source_file']}#{row['source_heading']}"
        divergences.append(
            Divergence(
                rule_id="section_domain_mismatch",
                severity=adjust_severity("medium", strictness),
                category="classification",
                path=source_ref,
                summary="Section is placed in the wrong audience document.",
                evidence=row["rationale"],
                recommended_action=(
                    f"Move section '{row['source_heading']}' from {row['source_file']} "
                    f"to {row['target_file']}#{row['target_section']}."
                ),
                requires_confirmation=True,
            )
        )

    return [item.as_dict() for item in divergences]


def write_markdown_report(
    output_path: Path,
    root: Path,
    scope: str,
    strictness: str,
    divergences: list[dict[str, Any]],
    inventory: dict[str, Any],
) -> None:
    counts = Counter(item["severity"] for item in divergences)
    significant = [item for item in divergences if item["severity"] in {"high", "medium"}]
    advisory = [item for item in divergences if item["severity"] == "low"]

    lines: list[str] = []
    lines.append("# Documentation Pattern Divergence Report")
    lines.append("")
    lines.append(f"- Root: `{root}`")
    lines.append(f"- Scope: `{scope}`")
    lines.append(f"- Strictness: `{strictness}`")
    lines.append(f"- Markdown files scanned: `{len(inventory['markdown_files'])}`")
    lines.append("")
    lines.append("## Severity Summary")
    lines.append("")
    lines.append(f"- high: {counts.get('high', 0)}")
    lines.append(f"- medium: {counts.get('medium', 0)}")
    lines.append(f"- low: {counts.get('low', 0)}")
    lines.append("")

    lines.append("## Significant Divergences")
    lines.append("")
    if not significant:
        lines.append("No high/medium divergences detected.")
        lines.append("")
    else:
        for item in significant:
            lines.append(f"### {item['id']} - {item['summary']}")
            lines.append("")
            lines.append(f"- Severity: `{item['severity']}`")
            lines.append(f"- Category: `{item['category']}`")
            lines.append(f"- Rule: `{item['rule_id']}`")
            lines.append(f"- Path: `{item['path']}`")
            lines.append(f"- Evidence: {item['evidence']}")
            lines.append(f"- Recommended action: {item['recommended_action']}")
            lines.append("")

    lines.append("## Advisory Findings")
    lines.append("")
    if not advisory:
        lines.append("No advisory findings.")
        lines.append("")
    else:
        for item in advisory:
            lines.append(f"- `{item['id']}` `{item['path']}`: {item['summary']}")
        lines.append("")

    lines.append("## Coverage")
    lines.append("")
    modules = inventory.get("modules", [])
    if not modules:
        lines.append("No coverage rows available.")
    else:
        for module in modules:
            lines.append(
                f"- `{module['module']}` present={module['present']} missing={module['missing']}"
            )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_classification_report(output_path: Path, rows: list[dict[str, Any]]) -> None:
    lines: list[str] = []
    lines.append("# Classification Report")
    lines.append("")
    lines.append(
        "Section-level mapping: source location to target audience doc/section with placement rationale."
    )
    lines.append("")

    if not rows:
        lines.append("No audience-document sections were detected for classification.")
        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    move_required = sum(1 for row in rows if row["move_required"])
    lines.append(f"- Classified sections: `{len(rows)}`")
    lines.append(f"- Sections requiring relocation: `{move_required}`")
    lines.append("")
    lines.append(
        "| Source file + heading | Target file + section | Move required | Placement rationale |"
    )
    lines.append("| --- | --- | --- | --- |")

    for row in rows:
        source = f"`{row['source_file']}` :: `{row['source_heading']}`"
        target = f"`{row['target_file']}` :: `{row['target_section']}`"
        move = "yes" if row["move_required"] else "no"
        rationale = row["rationale"].replace("|", "\\|")
        lines.append(f"| {source} | {target} | {move} | {rationale} |")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    output_dir = (
        Path(args.output_dir).resolve()
        if args.output_dir
        else root / ".agents" / "artifacts" / "doc-pattern"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    include_hidden_named = normalize_hidden_includes(args.include_hidden_dir)

    files = collect_markdown(
        root,
        include_hidden_dirs=args.include_hidden_dirs,
        include_hidden_named=include_hidden_named,
    )
    text_cache: dict[Path, str] = {path: read_text(path) for path in files}
    inventory = build_inventory(root, files, args.scope)
    classification_rows = build_classification_rows(root, files, text_cache)
    divergences = detect_divergences(
        root, files, args.strictness, args.scope, classification_rows
    )

    inventory_path = output_dir / "doc_inventory.json"
    divergence_json_path = output_dir / "divergence_report.json"
    divergence_md_path = output_dir / "divergence_report.md"
    classification_json_path = output_dir / "classification_report.json"
    classification_md_path = output_dir / "classification_report.md"

    inventory_path.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    classification_json_path.write_text(
        json.dumps({"root": str(root), "rows": classification_rows}, indent=2) + "\n",
        encoding="utf-8",
    )

    payload = {
        "root": str(root),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": args.scope,
        "strictness": args.strictness,
        "include_hidden_dirs": args.include_hidden_dirs,
        "include_hidden_named": sorted(include_hidden_named),
        "divergence_count": len(divergences),
        "classification_count": len(classification_rows),
        "classification_findings": [row for row in classification_rows if row["move_required"]],
        "divergences": divergences,
    }
    divergence_json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    write_markdown_report(
        divergence_md_path, root, args.scope, args.strictness, divergences, inventory
    )
    write_classification_report(classification_md_path, classification_rows)

    print(f"Wrote {inventory_path}")
    print(f"Wrote {divergence_json_path}")
    print(f"Wrote {divergence_md_path}")
    print(f"Wrote {classification_json_path}")
    print(f"Wrote {classification_md_path}")
    print(f"Detected {len(divergences)} divergences")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
