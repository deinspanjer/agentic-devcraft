import json
import unittest
from pathlib import Path

from evals.harbor.judge_record import build_judge_record


CONFIG = json.loads(Path("evals/harbor/judges/decision-rationale.json").read_text())


class JudgeRecordTest(unittest.TestCase):
    def test_keeps_judge_inputs_and_result_separate_from_deterministic_checks(self):
        deterministic = {"correctness": {"passed": True}}
        record = build_judge_record(
            CONFIG,
            ["candidate-a/transcript.json", "candidate-a/workspace.json"],
            {"rationale-clarity": {"score": 2, "reason": "Traceable basis."}},
            deterministic,
        )
        self.assertEqual(record["deterministic_verifier"], deterministic)
        self.assertEqual(record["judge"]["identity"], CONFIG["identity"])
        self.assertEqual(record["judge"]["rubric"], CONFIG["rubric"])
        self.assertEqual(record["judge"]["artifacts"][0], "candidate-a/transcript.json")

    def test_rejects_unblinded_arm_names(self):
        with self.assertRaisesRegex(ValueError, "blinded"):
            build_judge_record(CONFIG, ["control/transcript.json"], {}, {})


if __name__ == "__main__":
    unittest.main()
