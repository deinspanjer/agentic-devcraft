#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from pathlib import Path


def load_records(path: Path) -> list[dict[str, str]]:
    records = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict) or not all(
            isinstance(value.get(field), str) for field in ("id", "date", "status")
        ):
            raise ValueError(f"invalid record on line {line_number}")
        records.append(value)
    return records


def summarize(records: list[dict[str, str]]) -> dict[str, object]:
    return {
        "total": len(records),
        "by_status": dict(sorted(Counter(record["status"] for record in records).items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize JSONL work records")
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = summarize(load_records(args.path))
    if args.json:
        print(json.dumps(result, sort_keys=True))
        return
    print(f"Total: {result['total']}")
    for status, count in result["by_status"].items():
        print(f"{status}: {count}")


if __name__ == "__main__":
    main()
