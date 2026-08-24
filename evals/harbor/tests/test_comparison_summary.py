import unittest

from evals.harbor.comparison_summary import summarize_comparison


class ComparisonSummaryTest(unittest.TestCase):
    def test_keeps_measures_and_repetitions_separate(self):
        trials = [
            {
                "arm": "control",
                "correctness": 1,
                "false_positives": 0,
                "workflow_adherence": 1,
                "duration_sec": 10,
                "interaction_turns": 1,
                "assistant_updates": 3,
                "controller_continuations": 0,
                "tool_calls": 2,
                "input_tokens": None,
                "cache_tokens": None,
                "output_tokens": None,
            },
            {
                "arm": "control",
                "correctness": 0,
                "false_positives": 1,
                "workflow_adherence": 1,
                "duration_sec": 20,
                "interaction_turns": 2,
                "assistant_updates": 1,
                "controller_continuations": 1,
                "tool_calls": 4,
                "input_tokens": None,
                "cache_tokens": None,
                "output_tokens": None,
            },
        ]
        summary = summarize_comparison(trials)
        metrics = summary["arms"]["control"]["metrics"]
        self.assertEqual(metrics["correctness"]["median"], 0.5)
        self.assertEqual(metrics["false_positives"]["median"], 0.5)
        self.assertEqual(len(summary["arms"]["control"]["trials"]), 2)
        self.assertIsNone(summary["aggregate_score"])

    def test_unreported_token_metrics_remain_unavailable(self):
        summary = summarize_comparison([{"arm": "treatment", "correctness": 1}])
        tokens = summary["arms"]["treatment"]["metrics"]["input_tokens"]
        self.assertEqual(tokens["availability"], "unavailable")
        self.assertEqual(tokens["values"], [{"available": False, "value": None}])
        self.assertIsNone(tokens["median"])


if __name__ == "__main__":
    unittest.main()
