import copy
import json
import unittest
from pathlib import Path

from evals.harbor.validate_subjects import validate_subject


SUBJECT = json.loads(
    (Path(__file__).parents[1] / "subjects/devcraft-status.json").read_text()
)


class SubjectValidationTest(unittest.TestCase):
    def test_accepts_complete_subject(self):
        self.assertEqual(validate_subject(SUBJECT)["id"], "devcraft-status")

    def test_rejects_incomplete_subject_before_launch(self):
        subject = copy.deepcopy(SUBJECT)
        del subject["use_probe"]

        with self.assertRaisesRegex(ValueError, "missing=.*use_probe"):
            validate_subject(subject)

    def test_rejects_missing_host_stage(self):
        subject = copy.deepcopy(SUBJECT)
        del subject["discovery"]["codex"]

        with self.assertRaisesRegex(ValueError, "declared hosts"):
            validate_subject(subject)

    def test_accepts_cited_unsupported_host(self):
        subject = copy.deepcopy(SUBJECT)
        subject["hosts"].remove("claude-code")
        for field in ("network_hosts", "install", "configuration", "discovery", "use_probe"):
            del subject[field]["claude-code"]
        subject["unsupported"]["claude-code"] = {
            "reason": "The upstream host matrix excludes Claude Code.",
            "evidence": ["https://example.test/support-matrix"],
        }

        self.assertEqual(
            validate_subject(subject)["unsupported"]["claude-code"]["reason"],
            "The upstream host matrix excludes Claude Code.",
        )

    def test_rejects_unsupported_host_without_source_evidence(self):
        subject = copy.deepcopy(SUBJECT)
        subject["hosts"].remove("claude-code")
        for field in ("network_hosts", "install", "configuration", "discovery", "use_probe"):
            del subject[field]["claude-code"]
        subject["unsupported"]["claude-code"] = {
            "reason": "Unsupported",
            "evidence": [],
        }

        with self.assertRaisesRegex(ValueError, "source URLs"):
            validate_subject(subject)


if __name__ == "__main__":
    unittest.main()
