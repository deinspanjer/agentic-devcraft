#!/usr/bin/env python3
"""Generate a documentation refactor plan from divergence JSON output."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--divergence-json",
        required=True,
        help="Path to divergence_report.json from audit_docs_pattern.py",
    )
    parser.add_argument(
        "--output-dir",
        default=".codex/artifacts/doc-pattern",
        help="Directory where plan artifacts will be written",
    )
    parser.add_argument(
        "--level",
        choices=("audit", "scaffolding", "restructuring"),
        default="audit",
        help="Refactor level for level-aware artifact generation",
    )
    return parser.parse_args()


def severity_rank(value: str) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get(value, 3)


def extract_migration_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = payload.get("classification_findings", [])
    if rows:
        return rows

    fallback_rows: list[dict[str, Any]] = []
    for item in payload.get("divergences", []):
        if item.get("rule_id") != "section_domain_mismatch":
            continue

        path = item.get("path", "")
        if "#" in path:
            source_file, source_heading = path.split("#", 1)
        else:
            source_file, source_heading = path, "(section)"

        action = item.get("recommended_action", "")
        target_file = "(unknown)"
        target_section = "(unknown)"
        if " to " in action and "#" in action:
            _, right = action.split(" to ", 1)
            right = right.rstrip(".")
            if "#" in right:
                target_file, target_section = right.split("#", 1)

        fallback_rows.append(
            {
                "source_file": source_file,
                "source_heading": source_heading,
                "target_file": target_file,
                "target_section": target_section,
                "rationale": item.get("evidence", ""),
                "move_required": True,
            }
        )

    return fallback_rows


def build_plan_markdown(payload: dict[str, Any], level: str) -> str:
    divergences = payload.get("divergences", [])
    significant = [d for d in divergences if d.get("severity") in {"high", "medium"}]
    advisories = [d for d in divergences if d.get("severity") == "low"]

    by_path: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in sorted(
        significant,
        key=lambda x: (severity_rank(x.get("severity", "low")), x.get("path", "")),
    ):
        by_path[item.get("path", "(unknown)")].append(item)

    counts = Counter(item.get("severity", "unknown") for item in divergences)
    migration_rows = extract_migration_rows(payload)

    lines: list[str] = []
    lines.append("# Documentation Refactor Plan")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Generated at: `{datetime.now(timezone.utc).isoformat()}`")
    lines.append(f"- Root: `{payload.get('root', '')}`")
    lines.append(f"- Scope: `{payload.get('scope', 'root')}`")
    lines.append(f"- Strictness: `{payload.get('strictness', 'balanced')}`")
    lines.append(f"- Requested level: `{level}`")
    lines.append(
        f"- Divergences: `{len(divergences)}` (high={counts.get('high', 0)}, medium={counts.get('medium', 0)}, low={counts.get('low', 0)})"
    )
    lines.append(f"- Section migration candidates: `{len(migration_rows)}`")
    lines.append("")

    lines.append("## Significant Divergences")
    lines.append("")
    if not significant:
        lines.append("No high/medium divergences were found.")
        lines.append("")
    else:
        for path, items in by_path.items():
            lines.append(f"### `{path}`")
            lines.append("")
            for item in items:
                lines.append(f"- [{item['severity']}] `{item['rule_id']}` {item['summary']}")
                lines.append(f"  - Evidence: {item['evidence']}")
                lines.append(f"  - Recommended action: {item['recommended_action']}")
            lines.append("")

    lines.append("## Level-Specific Deliverables")
    lines.append("")
    lines.append("- `audit`: findings and reports only; no file edits.")
    lines.append(
        "- `scaffolding`: creates missing audience docs/templates and relocation markers only; no substantive moves."
    )
    lines.append(
        "- `restructuring`: executes relocations/splits into audience-correct docs with explicit migration actions."
    )
    lines.append("")
    if level == "scaffolding":
        lines.append("Generated level artifact: `migration_markers.md`")
    elif level == "restructuring":
        lines.append("Generated level artifact: `migration_actions.md`")
    else:
        lines.append("No migration artifact generated for `audit` level.")
    lines.append("")

    lines.append("## Proposed Change Steps")
    lines.append("")
    if level == "audit":
        lines.append("1. Review divergence and classification reports.")
        lines.append("2. Decide whether to proceed with scaffolding or restructuring.")
    elif level == "scaffolding":
        lines.append("1. Create missing root audience docs/templates if required.")
        lines.append("2. Add `DOC-RELOCATE` markers for each migration candidate.")
        lines.append("3. Keep substantive content in place until restructuring is approved.")
    else:
        lines.append("1. Relocate sections to target audience docs using migration actions.")
        lines.append("2. Split oversized single-topic sections into focused sub-docs.")
        lines.append("3. Update links and summaries for progressive disclosure.")
    lines.append("")

    lines.append("## Confirmation Gates")
    lines.append("")
    lines.append("1. Confirm whether to proceed from audit report to refactor planning.")
    lines.append("2. Confirm whether to create a pre-refactor stash snapshot.")
    lines.append("3. Confirm whether to apply the planned file edits.")
    lines.append("")

    lines.append("## Safety and Rollback")
    lines.append("")
    lines.append("Use these commands before and after refactor execution:")
    lines.append("")
    lines.append("```bash")
    lines.append('git stash push -u -m "doc-pattern-refactor-prep-<timestamp>"')
    lines.append("git stash list")
    lines.append("git stash show -p stash@{n}")
    lines.append("git stash apply stash@{n}")
    lines.append("```")
    lines.append("")

    lines.append("## AGENTS Handling")
    lines.append("")
    lines.append("If AGENTS layout issues are present, do not auto-edit AGENTS files in this workflow.")
    lines.append("Recommend the sibling `agent-instructions-cleanup` skill for AGENTS refactoring (Codex: `$agentic-devcraft:agent-instructions-cleanup`; Claude: `/agentic-devcraft:agent-instructions-cleanup`; Air: attach the skill).")
    lines.append("")

    lines.append("## Advisory Backlog")
    lines.append("")
    if not advisories:
        lines.append("No low-severity advisory items.")
    else:
        for item in advisories:
            lines.append(f"- `{item['id']}` `{item['path']}`: {item['summary']}")

    return "\n".join(lines) + "\n"


def build_migration_markers_markdown(rows: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    lines.append("# Migration Markers")
    lines.append("")
    lines.append("Use these relocation markers during scaffolding. Do not move substantive content yet.")
    lines.append("")

    if not rows:
        lines.append("No relocation markers required.")
        return "\n".join(lines) + "\n"

    for row in rows:
        marker = (
            f"<!-- DOC-RELOCATE: move section '{row['source_heading']}' "
            f"to {row['target_file']}#{row['target_section']} -->"
        )
        lines.append(f"- Source: `{row['source_file']}#{row['source_heading']}`")
        lines.append(f"- Marker: `{marker}`")
        lines.append(f"- Rationale: {row['rationale']}")
        lines.append("")

    return "\n".join(lines) + "\n"


def build_migration_actions_markdown(rows: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    lines.append("# Migration Actions")
    lines.append("")
    lines.append("Concrete source-to-destination relocation actions for restructuring.")
    lines.append("")

    if not rows:
        lines.append("No migration actions required.")
        return "\n".join(lines) + "\n"

    lines.append("| Source file + heading | Destination file + section | Rationale |")
    lines.append("| --- | --- | --- |")
    for row in rows:
        source = f"`{row['source_file']}` :: `{row['source_heading']}`"
        target = f"`{row['target_file']}` :: `{row['target_section']}`"
        rationale = row["rationale"].replace("|", "\\|")
        lines.append(f"| {source} | {target} | {rationale} |")

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    divergence_path = Path(args.divergence_json).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = json.loads(divergence_path.read_text(encoding="utf-8"))
    markdown = build_plan_markdown(payload, args.level)

    output_path = output_dir / "refactor_plan.md"
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Wrote {output_path}")

    rows = extract_migration_rows(payload)
    if args.level == "scaffolding":
        markers_path = output_dir / "migration_markers.md"
        markers_path.write_text(build_migration_markers_markdown(rows), encoding="utf-8")
        print(f"Wrote {markers_path}")
    elif args.level == "restructuring":
        actions_path = output_dir / "migration_actions.md"
        actions_path.write_text(build_migration_actions_markdown(rows), encoding="utf-8")
        print(f"Wrote {actions_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
