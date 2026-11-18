import copy
import json
import tempfile
import unittest
from pathlib import Path

from evals.harbor.prepare_arm import prepare_arm
from evals.harbor.run_comparison import _response_json, create_task
from evals.harbor.trial_result import build_trial_result
from evals.harbor.validate_comparisons import validate_comparison


ARM = {
    "id": "control",
    "host": "codex",
    "model": {"name": "gpt-5.6-sol", "settings": {"reasoning_effort": "high"}},
    "fixture": "evals/harbor/fixtures/review-integrity",
    "interaction": "headless",
    "skills": [],
    "hooks": [],
    "workflow_context": [],
    "timeout_sec": 300,
    "repetitions": 3,
}
ROOT = Path(__file__).parents[3]


class ComparisonValidationTest(unittest.TestCase):
    def comparison(self):
        treatment = copy.deepcopy(ARM)
        treatment.update(id="skills", skills=["code-review"])
        return {"id": "review-integrity", "arms": [copy.deepcopy(ARM), treatment]}

    def test_accepts_paired_arms(self):
        self.assertEqual(validate_comparison(self.comparison())["id"], "review-integrity")

    def test_unreleased_skills_are_tested_outside_shared_plugin_payload(self):
        released = {
            path.parent.name
            for path in (ROOT / "plugins/agentic-devcraft/skills").glob("*/SKILL.md")
        }
        self.assertEqual(
            released,
            {
                "agent-instructions-cleanup",
                "ask-devcraft",
                "capture-agent-issue",
                "documentation-pattern-refactor",
                "status",
            },
        )
        for path in (ROOT / "evals/harbor/comparisons").glob("*.json"):
            comparison = json.loads(path.read_text())
            for arm in comparison["arms"]:
                for skill in arm["skills"]:
                    if skill.startswith("http"):
                        continue
                    self.assertTrue(skill.startswith("proposals/skills/"), skill)
                    self.assertTrue((ROOT / skill / "SKILL.md").is_file(), skill)

        codex = json.loads(
            (ROOT / "plugins/agentic-devcraft/.codex-plugin/plugin.json").read_text()
        )
        claude = json.loads(
            (ROOT / "plugins/agentic-devcraft/.claude-plugin/plugin.json").read_text()
        )
        self.assertEqual(codex["skills"], claude["skills"])

    def test_rejects_incomplete_arm(self):
        comparison = self.comparison()
        del comparison["arms"][1]["hooks"]
        with self.assertRaisesRegex(ValueError, "missing=.*hooks"):
            validate_comparison(comparison)

    def test_rejects_unpaired_fixture(self):
        comparison = self.comparison()
        comparison["arms"][1]["fixture"] = "evals/harbor/fixtures/other"
        with self.assertRaisesRegex(ValueError, "may differ only"):
            validate_comparison(comparison)

    def test_prepares_fresh_workspace_with_skill_and_hook_setup_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture = root / "fixture"
            skill = root / "skill"
            hook = root / "hook.json"
            fixture.mkdir()
            skill.mkdir()
            (fixture / "task.txt").write_text("fixture\n")
            (skill / "SKILL.md").write_text("---\nname: test\n---\n")
            hook.write_text(json.dumps({"hooks": {"SessionStart": [{"hooks": []}]}}))
            arm = copy.deepcopy(ARM)
            arm.update(
                fixture="fixture",
                skills=["skill", "https://example.com/org/repo/tree/revision/skills"],
                hooks=["hook.json"],
            )

            manifest = prepare_arm(arm, root, root / "prepared")

            self.assertEqual(manifest["setup"]["status"], "passed")
            self.assertIsNone(manifest["behavioral_score"])
            self.assertTrue((root / "prepared/workspace/task.txt").is_file())
            self.assertTrue((root / "prepared/skills/skill/SKILL.md").is_file())
            self.assertTrue((root / "prepared/config/hooks.json").is_file())
            self.assertEqual(
                manifest["setup"]["remote_skills"],
                ["https://example.com/org/repo/tree/revision/skills"],
            )

    def test_normalizes_valid_trial_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            (workspace / "result.txt").write_text("done\n")
            result = build_trial_result(
                {"setup": {"status": "passed"}},
                {"steps": [{"source": "user", "message": "work"}, {"source": "agent", "message": "done"}]},
                workspace,
                {"status": "passed", "score": 1, "checks": {"answer": True}},
                {"host": "codex", "model": "gpt-5.6-sol", "harness": "harbor-0.21.0"},
            )

            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["behavioral_score"], 1)
            self.assertEqual([step["source"] for step in result["transcript"]], ["user", "agent"])
            self.assertEqual(result["workspace"][0]["path"], "result.txt")

    def test_setup_failure_is_invalid_and_unscored(self):
        with tempfile.TemporaryDirectory() as temp:
            result = build_trial_result(
                {"setup": {"status": "failed", "reason": "missing skill"}},
                {"steps": []},
                Path(temp),
                {"status": "passed", "score": 1},
                {"host": "codex"},
            )

            self.assertEqual(result["status"], "invalid")
            self.assertIsNone(result["behavioral_score"])
            self.assertEqual(result["verifier"]["status"], "not_run")

    def test_builds_harbor_task_from_prepared_workspace(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "prepared/workspace"
            workspace.mkdir(parents=True)
            (workspace / "instruction.md").write_text("Do the task.\n")
            create_task(root / "prepared", root / "task", 30)
            self.assertIn("network_mode = \"allowlist\"", (root / "task/task.toml").read_text())
            self.assertIn("COPY --chown=node:node workspace/ /app/", (root / "task/environment/Dockerfile").read_text())

    def test_extracts_json_from_final_agent_message(self):
        response = _response_json(
            {"steps": [{"source": "agent", "message": "```json\n{\"ok\": true}\n```"}]}
        )
        self.assertEqual(response, {"ok": True})


if __name__ == "__main__":
    unittest.main()
