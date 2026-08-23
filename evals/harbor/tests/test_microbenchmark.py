import json
import shutil
import tempfile
import unittest
from pathlib import Path

from evals.harbor.engineering_benchmark import build_local_fixture, load_matrix
from evals.harbor.run_engineering_benchmark import (
    SCENARIOS,
    create_task,
    scenario,
    trial_command,
)


ROOT = Path(__file__).resolve().parents[3]
BENCHMARK = ROOT / "evals/harbor/benchmarks/date-filter"


class MicrobenchmarkTest(unittest.TestCase):
    def test_local_fixture_build_is_deterministic_and_clean(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "source"
            shutil.copytree(
                BENCHMARK / "fixture",
                source,
                ignore=shutil.ignore_patterns("__pycache__", "*.py[co]"),
            )
            first = build_local_fixture(source, root / "first")
            cache = source / "__pycache__"
            cache.mkdir()
            (cache / "report.cpython-test.pyc").write_bytes(b"runtime cache")
            second = build_local_fixture(source, root / "second")
            self.assertEqual(first["fixture_head"], second["fixture_head"])
            self.assertEqual(first["fixture_digest"], second["fixture_digest"])
            self.assertEqual(first["source_digest"], second["source_digest"])
            self.assertFalse((root / "second/fixture/__pycache__").exists())
            self.assertFalse((root / "first/fixture/extension.md").exists())

    def test_scenario_uses_small_direct_only_matrix_and_dynamic_verifier(self):
        config = scenario("date-filter")
        matrix = load_matrix(config["benchmark"] / "baseline-matrix.json")
        self.assertEqual(matrix["scenario"], "date-filter-v1")
        self.assertTrue(all(arm["orchestration"] == "direct" for arm in matrix["arms"]))
        self.assertEqual(config["verifier_module"], "evals.harbor.date_filter_verifier")
        self.assertIn("date-filter", SCENARIOS)

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            fixture = root / "fixture"
            fixture.mkdir()
            (fixture / "report.py").write_text("print('fixture')\n")
            task = root / "task"
            create_task(fixture, task, 30, config)
            command = trial_command(
                root / "harbor",
                task,
                root / "jobs",
                matrix["arms"][0],
                matrix["controller"],
                root / "config.toml",
                config,
            )
            rendered = " ".join(str(item) for item in command)
            self.assertIn("verifier_module=evals.harbor.date_filter_verifier", rendered)
            self.assertIn("verifier_reference_path=", rendered)
            self.assertNotIn("crates.io", rendered)
            self.assertIn("FROM python:", (task / "environment/Dockerfile").read_text())

    def test_rubric_is_scenario_specific_and_has_no_composite(self):
        rubric = json.loads((BENCHMARK / "rubric.json").read_text())
        self.assertEqual(rubric["scenario"], "date-filter-v1")
        self.assertEqual(rubric["aggregation"], "profile-only")
        self.assertNotIn("weight", repr(rubric))
        self.assertTrue(rubric["criteria"])
        for criterion in rubric["criteria"]:
            self.assertEqual(set(criterion["anchors"]), {"0", "1", "2", "3", "4"})
            self.assertTrue(criterion["evidence"])


if __name__ == "__main__":
    unittest.main()
