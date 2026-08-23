import json
import unittest
from pathlib import Path

from evals.harbor.cold_read_verifier import verify_cold_read


EXPECTED = json.loads(Path("evals/harbor/expectations/cold-read.json").read_text())


class ColdReadVerifierTest(unittest.TestCase):
    def test_scores_coverage_facts_and_correction_separately(self):
        result = verify_cold_read(
            EXPECTED,
            {
                "claims": [
                    {"id": "C1", "status": "false", "evidence": "storage.py:4 returns None"},
                    {"id": "C2", "status": "false", "evidence": "storage.py:8 returns None"},
                ],
                "design": {"status": "change", "replacement": "serialize-writes"},
            },
        )
        self.assertTrue(result["enumeration_coverage"]["passed"])
        self.assertTrue(result["factual_verification"]["passed"])
        self.assertTrue(result["design_correction"]["passed"])

    def test_missing_sibling_does_not_hide_correct_first_fact(self):
        result = verify_cold_read(
            EXPECTED,
            {
                "claims": [{"id": "C1", "status": "false", "evidence": "storage.py:4"}],
                "design": {"status": "change", "replacement": "serialize-writes"},
            },
        )
        self.assertEqual(result["enumeration_coverage"]["missing"], ["C2"])
        self.assertEqual(result["factual_verification"]["incorrect"], [])
        self.assertTrue(result["design_correction"]["passed"])


if __name__ == "__main__":
    unittest.main()
