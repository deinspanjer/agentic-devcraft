import tempfile
import unittest
from pathlib import Path

from evals.harbor.engineering_benchmark import load_matrix
from evals.harbor.run_engineering_benchmark import (
    BENCHMARK,
    HARNESS_FILES,
    _trial_artifacts,
    codex_config_toml,
    create_task,
    plan,
    stage_host_metrics,
    stage_trajectories,
    trial_command,
)


class EngineeringRunnerTest(unittest.TestCase):
    def test_provenance_covers_normalization_and_summary_code(self):
        names = {path.name for path in HARNESS_FILES}
        self.assertIn("trial_result.py", names)
        self.assertIn("comparison_summary.py", names)

    def test_task_and_command_keep_fixture_code_only(self):
        matrix = load_matrix(BENCHMARK / "baseline-matrix.json")
        arm = matrix["arms"][0]
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            fixture = root / "fixture"
            fixture.mkdir()
            (fixture / "rollout_stats.py").write_text("print('fixture')\n")
            task = root / "task"
            create_task(fixture, task, arm["limits"]["timeout_sec"])
            self.assertTrue((task / "environment/workspace/rollout_stats.py").is_file())
            self.assertTrue((task / "task.toml").is_file())
            self.assertTrue((task / "tests/test.sh").stat().st_mode & 0o111)
            self.assertIn(
                "COPY --chown=node:node workspace/ /app/",
                (task / "environment/Dockerfile").read_text(),
            )
            self.assertIn(
                "rustup component add rustfmt clippy",
                (task / "environment/Dockerfile").read_text(),
            )
            self.assertFalse((task / "environment/workspace/extension.md").exists())
            self.assertEqual(
                (task / "instruction.md").read_text(),
                (BENCHMARK / "initial.md").read_text(),
            )
            config = root / "config.json"
            config.write_text("{}")
            command = trial_command(
                root / "harbor", task, root / "jobs", arm, matrix["controller"], config
            )
            rendered = " ".join(str(item) for item in command)
            self.assertIn("subject_agent=codex", rendered)
            self.assertIn("controller_agent=codex", rendered)
            self.assertIn("verifier_oracle_path=", rendered)
            self.assertNotIn("--skill", command)
            self.assertNotIn("claude", rendered.lower())
            self.assertIn("multi_agent = false", codex_config_toml(arm))
            self.assertIn(
                "multi_agent = true", codex_config_toml(matrix["arms"][2])
            )

    def test_trial_artifacts_ignore_job_summary(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "result.json").write_text("job summary")
            agent = root / "job/task__one/agent"
            agent.mkdir(parents=True)
            (agent / "controller.json").write_text("{}")
            trial_result = agent.parent / "result.json"
            trial_result.write_text("trial result")
            self.assertEqual(_trial_artifacts(root), (agent, trial_result))

    def test_resumed_stage_metrics_are_stage_local(self):
        metrics = stage_host_metrics(
            {
                "initial": {
                    "final_metrics": {
                        "total_prompt_tokens": 100,
                        "total_cached_tokens": 80,
                        "total_completion_tokens": 30,
                    }
                },
                "extension": {
                    "final_metrics": {
                        "total_prompt_tokens": 120,
                        "total_cached_tokens": 90,
                        "total_completion_tokens": 11,
                    }
                },
            }
        )
        self.assertEqual(metrics["extension"]["reported_tokens"]["output_tokens"], 11)

    def test_resumed_stage_trajectory_excludes_initial_prefix(self):
        initial = {"steps": [{"source": "agent", "message": "initial"}]}
        extension = {
            "steps": [*initial["steps"], {"source": "agent", "message": "extension"}],
            "final_metrics": {"total_completion_tokens": 11},
        }
        trajectories = stage_trajectories(
            [
                {"stage": "initial", "trajectory": initial},
                {"stage": "extension", "trajectory": extension},
            ]
        )
        self.assertEqual(
            trajectories["extension"]["steps"],
            [{"source": "agent", "message": "extension"}],
        )
        self.assertEqual(
            trajectories["extension"]["final_metrics"]["total_completion_tokens"], 11
        )
        with self.assertRaisesRegex(RuntimeError, "does not continue"):
            stage_trajectories(
                [
                    {"stage": "initial", "trajectory": initial},
                    {
                        "stage": "extension",
                        "trajectory": {
                            "steps": [{"source": "agent", "message": "different"}]
                        },
                    },
                ]
            )

    def test_plan_is_interleaved_plumbing_evidence_without_cost_guess(self):
        matrix = load_matrix(BENCHMARK / "baseline-matrix.json")
        value = plan(matrix)
        self.assertEqual(len(value["schedule"]), 4)
        self.assertEqual(value["authenticated_monetary_cost"], "unavailable-subscription-usage")
        self.assertEqual(value["subject_reported_output_token_ceiling"], 1_000_000)
        self.assertIn(
            "per stage", value["limit_semantics"]["interaction_turns"]
        )
        self.assertIn("not reported", value["limit_semantics"]["controller"])
        self.assertIn("plumbing", value["note"])


if __name__ == "__main__":
    unittest.main()
