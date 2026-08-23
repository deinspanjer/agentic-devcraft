import json
import tempfile
import textwrap
import unittest
from pathlib import Path

from evals.harbor.date_filter_verifier import (
    load_contracts,
    verify_extension,
    verify_initial,
)


ROOT = Path(__file__).resolve().parents[3]
BENCHMARK = ROOT / "evals/harbor/benchmarks/date-filter"


def write_candidate(root: Path, *, support_until: bool = True) -> None:
    root.mkdir()
    until = (
        "parser.add_argument('--until', type=date.fromisoformat)\n"
        if support_until
        else ""
    )
    until_filter = (
        "    if args.until is not None: rows = [row for row in rows if date.fromisoformat(row['date']) <= args.until]\n"
        if support_until
        else ""
    )
    (root / "report.py").write_text(
        textwrap.dedent(
            f"""
            import argparse, json
            from collections import Counter
            from datetime import date

            parser = argparse.ArgumentParser()
            parser.add_argument('path')
            parser.add_argument('--json', action='store_true')
            parser.add_argument('--since', type=date.fromisoformat)
            {until.strip()}
            args = parser.parse_args()
            rows = [json.loads(line) for line in open(args.path) if line.strip()]
            if args.since is not None: rows = [row for row in rows if date.fromisoformat(row['date']) >= args.since]
            {until_filter.strip()}
            result = {{'total': len(rows), 'by_status': dict(sorted(Counter(row['status'] for row in rows).items()))}}
            if args.json: print(json.dumps(result, sort_keys=True))
            else:
                print(f"Total: {{result['total']}}")
                for status, count in result['by_status'].items(): print(f"{{status}}: {{count}}")
            """
        ).lstrip()
    )
    (root / "README.md").write_text(
        "# Report\n\nUse `--since YYYY-MM-DD` and `--until YYYY-MM-DD`.\n"
    )
    (root / "test_report.py").write_text(
        "import unittest\n\nclass ReportTest(unittest.TestCase):\n"
        "    def test_fixture(self): self.assertTrue(True)\n"
    )


class DateFilterVerifierTest(unittest.TestCase):
    def test_contracts_separate_required_behavior_from_robustness(self):
        inventory = load_contracts(BENCHMARK / "contracts.json")
        kinds = {item["kind"] for item in inventory["contracts"]}
        self.assertEqual(kinds, {"required", "robustness"})
        self.assertTrue(
            all(
                item["scored"] is (item["kind"] == "required")
                for item in inventory["contracts"]
            )
        )

    def test_correct_candidate_passes_required_contracts_and_preserves_snapshot(self):
        with tempfile.TemporaryDirectory() as raw:
            candidate = Path(raw) / "candidate"
            write_candidate(candidate)
            initial = verify_initial(
                candidate, BENCHMARK / "rubric.json", BENCHMARK / "contracts.json"
            )
            extension = verify_extension(
                candidate, BENCHMARK / "rubric.json", BENCHMARK / "contracts.json"
            )
            self.assertEqual(initial["status"], "passed", initial)
            self.assertEqual(extension["status"], "passed", extension)
            self.assertTrue(initial["snapshot_unchanged"])
            self.assertTrue(extension["snapshot_unchanged"])
            self.assertTrue(all(item["passed"] for item in initial["contracts"]))
            self.assertTrue(all(item["passed"] for item in extension["contracts"]))
            self.assertTrue(extension["robustness"])

    def test_missing_extension_fails_only_extension_requirements(self):
        with tempfile.TemporaryDirectory() as raw:
            candidate = Path(raw) / "candidate"
            write_candidate(candidate, support_until=False)
            initial = verify_initial(
                candidate, BENCHMARK / "rubric.json", BENCHMARK / "contracts.json"
            )
            extension = verify_extension(
                candidate, BENCHMARK / "rubric.json", BENCHMARK / "contracts.json"
            )
            self.assertEqual(initial["status"], "passed", initial)
            self.assertEqual(extension["status"], "failed", extension)
            checks = {item["id"]: item["passed"] for item in extension["contracts"]}
            self.assertTrue(checks["initial-contract-regression"])
            self.assertFalse(checks["until-inclusive"])
            self.assertFalse(checks["combined-range"])


if __name__ == "__main__":
    unittest.main()
