import unittest

from evals.harbor.coexistence_verifier import verify_coexistence


class CoexistenceVerifierTest(unittest.TestCase):
    def test_reports_overlap_overhead_and_outcomes_without_aggregating(self):
        result = verify_coexistence(
            {
                "peters-only": {
                    "phases": ["design", "review", "plan"],
                    "invocations": ["peters-toolkit:critical-design-review"],
                    "turns": 3,
                    "outcome": {"preserves-save-contract": True},
                },
                "devcraft-only": {
                    "phases": ["design", "review", "plan"],
                    "invocations": ["review-integrity"],
                    "turns": 3,
                    "outcome": {"preserves-save-contract": True},
                },
                "combined": {
                    "phases": ["design", "review", "review", "plan"],
                    "invocations": [
                        "peters-toolkit:critical-design-review",
                        "review-integrity",
                    ],
                    "turns": 5,
                    "outcome": {"preserves-save-contract": False},
                },
            }
        )
        self.assertEqual(result["arms"]["combined"]["duplicate_phases"], ["review"])
        self.assertEqual(result["arms"]["combined"]["conflicting_invocations"], ["review"])
        self.assertEqual(result["arms"]["combined"]["extra_turns"], 2)
        self.assertTrue(result["outcome_differences"])


if __name__ == "__main__":
    unittest.main()
