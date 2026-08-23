import json
import unittest
from pathlib import Path

from evals.harbor.review_verifier import verify_review


EXPECTATIONS = Path("evals/harbor/expectations/review-integrity")


class ReviewVerifierTest(unittest.TestCase):
    def expected(self, case):
        return json.loads((EXPECTATIONS / f"{case}.json").read_text())

    def test_accepts_empty_findings_for_clean_case(self):
        result = verify_review(self.expected("clean"), {"findings": []})
        self.assertEqual(result["status"], "passed")
        self.assertTrue(result["correct_empty"])

    def test_reports_supported_seeded_finding(self):
        finding = {
            "file": "app.py",
            "start_line": 4,
            "end_line": 4,
            "category": "correctness",
            "summary": "Port zero is accepted.",
        }
        result = verify_review(self.expected("seeded"), {"findings": [finding]})
        self.assertEqual(result["supported_findings"], [finding])
        self.assertEqual(result["missed_findings"], [])
        self.assertEqual(result["fabricated_findings"], [])

    def test_keeps_missed_and_fabricated_findings_separate(self):
        fabricated = {
            "file": "app.py",
            "start_line": 2,
            "end_line": 2,
            "category": "maintainability",
            "summary": "Rename the function.",
        }
        result = verify_review(self.expected("seeded"), {"findings": [fabricated]})
        self.assertEqual(len(result["missed_findings"]), 1)
        self.assertEqual(result["fabricated_findings"], [fabricated])

    def test_persona_wording_is_not_finding_evidence(self):
        persona_only = {
            "file": "app.py",
            "start_line": 2,
            "end_line": 2,
            "category": "maintainability",
            "summary": "A senior reviewer should require more documentation.",
        }
        result = verify_review(self.expected("clean"), {"findings": [persona_only]})
        self.assertEqual(result["supported_findings"], [])
        self.assertEqual(result["fabricated_findings"], [persona_only])


if __name__ == "__main__":
    unittest.main()
