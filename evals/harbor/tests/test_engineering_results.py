import json
import tempfile
import unittest
from pathlib import Path

from evals.harbor.comparison_summary import summarize_engineering_comparison
from evals.harbor.trial_result import (
    blinded_qualitative_input,
    build_engineering_result,
    offline_rescore,
    trajectory_evidence,
    write_qualitative_record,
)


class EngineeringResultTest(unittest.TestCase):
    def test_committed_baseline_preserves_trials_without_overclaiming(self):
        path = Path(__file__).parents[1] / "baselines/vanilla-port-codex-v1.json"
        baseline = json.loads(path.read_text())
        self.assertEqual(baseline["schema_version"], 2)
        trials = baseline["trials"]
        self.assertEqual([trial["order"] for trial in trials], list(range(1, 13)))
        self.assertTrue(
            all(
                trial["initial"]["contracts"] == "7/7"
                and trial["extension"]["contracts"] == "4/4"
                for trial in trials
            )
        )
        orchestration = next(
            arm for arm in baseline["arms"] if arm["id"] == "sol-high-orchestrated"
        )
        self.assertEqual(
            orchestration["orchestration"], "subagents-available-not-directed"
        )
        self.assertEqual(
            baseline["availability"]["actual_subscription_cost"], "unavailable"
        )
        self.assertNotIn("ranking", baseline)
        self.assertNotIn("composite", baseline)
        self.assertTrue(
            all(
                stage["interaction_turns"] == 1
                and stage["controller_continuations"] == 0
                and "turns" not in stage
                for trial in trials
                for stage in (trial["initial"], trial["extension"])
            )
        )

    def test_committed_calibration_uses_corrected_process_terms(self):
        path = (
            Path(__file__).parents[1]
            / "baselines/date-filter-codex-calibration-v1.json"
        )
        baseline = json.loads(path.read_text())
        self.assertEqual(baseline["evidence"], "plumbing-only")
        self.assertEqual(len(baseline["trials"]), 3)
        self.assertTrue(
            all(
                stage["interaction_turns"] == 1
                and stage["controller_continuations"] == 0
                and "turns" not in stage
                for trial in baseline["trials"]
                for stage in (trial["initial"], trial["extension"])
            )
        )
    def test_stage_evidence_locality_blinding_and_summary(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            initial = root / "initial"
            extension = root / "extension"
            (initial / "src").mkdir(parents=True)
            (extension / "src").mkdir(parents=True)
            (initial / "src/report.rs").write_text("fn report() {}\n")
            (extension / "src/report.rs").write_text("fn report() {}\n")
            (extension / "src/pricing.rs").write_text("fn load_price_rate() {}\n")
            (initial / "target").mkdir()
            (extension / "target").mkdir()
            (initial / "target/build").write_text("initial")
            (extension / "target/build").write_text("extension")
            (initial / "__pycache__").mkdir()
            (extension / "__pycache__").mkdir()
            (initial / "__pycache__/report.cpython-314.pyc").write_bytes(b"initial")
            (extension / "__pycache__/report.cpython-314.pyc").write_bytes(b"extension")
            (initial / ".git").mkdir()
            (extension / ".git").mkdir()
            (initial / ".git/index").write_bytes(b"initial")
            (extension / ".git/index").write_bytes(b"extension")
            (extension / "tests").mkdir()
            (extension / "tests/cli.rs").write_text("fn price_test() {}\n")
            checkpoints = [
                {
                    "stage": stage,
                    "workspace_digest": stage,
                    "inventory": [{"path": "src/report.rs"}],
                    "git": {"changed_paths": ["src/report.rs"]},
                    "controller": {
                        "interaction_turns": 1,
                        "termination": "completed",
                        "decisions": [],
                    },
                    "verifier": {
                        "status": "passed",
                        "contracts": [{"id": "contract", "passed": True}],
                        "robustness": [
                            {"id": "edge", "outcome": "accepted", "detail": "observed"}
                        ],
                    },
                }
                for stage in ("initial", "extension")
            ]
            trajectory = {
                "steps": [
                    {
                        "source": "agent",
                        "message": "Assuming local scope. Is JSON required?",
                        "tool_calls": [{"command": "sed -n 1,20p rollout_stats.py\ncargo test"}],
                    },
                    {
                        "source": "agent",
                        "message": "",
                        "tool_calls": [{"command": "cargo check"}],
                    },
                    {"source": "agent", "message": "Done.", "tool_calls": []},
                ]
            }
            result = build_engineering_result(
                checkpoints=checkpoints,
                trajectories={"initial": trajectory, "extension": trajectory},
                snapshot_paths={"initial": initial, "extension": extension},
                provenance={
                    "trial_id": "trial-1",
                    "arm": "secret-arm",
                    "repetition": 1,
                    "execution_order": 1,
                    "fixture": "fixture-digest",
                    "prompts": {"initial": "one", "extension": "two"},
                    "harness": "harness-digest",
                    "verifier": "verifier-digest",
                    "host": "codex",
                    "model": "secret-model",
                    "configuration": "config-digest",
                    "provisioned_content": "empty-digest",
                    "historical_context": "none",
                },
            )
            process = result["stages"]["initial"]["process"]
            self.assertTrue(process["source_inspection"])
            self.assertEqual(process["interaction_turns"], 1)
            self.assertEqual(process["assistant_updates"], 1)
            self.assertEqual(process["controller_continuations"], 0)
            self.assertNotIn("turns", process)
            self.assertEqual(
                result["stages"]["initial"]["product"]["robustness"][0]["id"],
                "edge",
            )
            self.assertEqual(process["duration_sec"], {"available": False, "value": None})
            comparison = result["stages"]["extension"]["engineering"]["extension_comparison"]
            self.assertEqual(comparison["pricing_owners"], ["src/pricing.rs"])
            self.assertNotIn("target/build", comparison["changed_paths"])
            self.assertNotIn(
                "__pycache__/report.cpython-314.pyc", comparison["changed_paths"]
            )
            self.assertNotIn(".git/index", comparison["changed_paths"])
            self.assertEqual(comparison["extension_changed_file_count"], 2)
            self.assertIn("not design-quality", comparison["interpretation"])

            blinded = blinded_qualitative_input(result)
            self.assertNotIn("secret-arm", repr(blinded))
            self.assertNotIn("secret-model", repr(blinded))
            self.assertEqual(blinded["rubric"]["kind"], "shared-framework")
            self.assertIn(
                "explicit-requirements", blinded["rubric"]["criteria"]
            )
            qualitative_path = root / "qualitative.json"
            qualitative = write_qualitative_record(
                qualitative_path, result, {"scope_control": "reviewed"}
            )
            self.assertNotIn("secret-arm", repr(qualitative["input"]))
            with self.assertRaises(FileExistsError):
                write_qualitative_record(qualitative_path, result, {})
            summary = summarize_engineering_comparison([result], plumbing=True)
            self.assertEqual(summary["evidence"], "plumbing-only")
            self.assertEqual(summary["execution_order"], [1])
            self.assertNotIn("aggregate", summary)
            self.assertEqual(
                summary["arms"]["secret-arm"]["stages"]["initial"]["measures"]["product.contracts_passed"]["median"],
                1,
            )

    def test_discovery_telemetry_recognizes_the_calibration_fixture(self):
        evidence = trajectory_evidence(
            {
                "steps": [
                    {
                        "source": "agent",
                        "message": "done",
                        "tool_calls": [
                            {
                                "command": "sed -n '1,200p' report.py; sed -n '1,200p' test_report.py; python3 -m unittest -v"
                            }
                        ],
                    }
                ]
            }
        )
        self.assertTrue(evidence["source_inspection"])
        self.assertTrue(evidence["self_test_inspection"])
        self.assertTrue(evidence["focused_checks"])
        self.assertEqual(evidence["assistant_updates"], 1)
        self.assertNotIn("turns", evidence)

    def test_offline_rescore_is_append_only(self):
        from evals.harbor.tests.test_port_verifier import CONTRACTS, ORACLE

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            trial = root / "trial.json"
            trial.write_text('{"status":"valid"}\n')
            snapshot = root / "snapshot"
            snapshot.mkdir()
            (snapshot / "README.md").write_text("incomplete")
            before = trial.read_bytes()
            output = root / "rescores/one.json"
            record = offline_rescore(
                original_trial=trial,
                snapshots={"initial": snapshot},
                oracle_script=ORACLE,
                contracts_path=CONTRACTS,
                output=output,
            )
            self.assertEqual(trial.read_bytes(), before)
            self.assertEqual(record["kind"], "offline-rescore")
            self.assertEqual(record["verifiers"]["initial"]["status"], "failed")
            with self.assertRaises(FileExistsError):
                offline_rescore(
                    original_trial=trial,
                    snapshots={"initial": snapshot},
                    oracle_script=ORACLE,
                    contracts_path=CONTRACTS,
                    output=output,
                )


if __name__ == "__main__":
    unittest.main()
