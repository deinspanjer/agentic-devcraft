import copy
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from evals.harbor.engineering_benchmark import (
    authority_violation,
    build_fixture,
    load_manifest,
    load_matrix,
    prepare_vanilla_arm,
    privacy_issues,
    redact,
    runtime_contamination,
    schedule_trials,
    sha256_file,
    tree_digest,
    validate_codex_runtime,
    validate_manifest,
    validate_matrix,
)
from evals.harbor.run_engineering_benchmark import benchmark_defects


ROOT = Path(__file__).parents[3]
BENCHMARK = ROOT / "evals/harbor/benchmarks/vanilla-port"


def git(repo: Path, *args: str, env=None) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, **(env or {})},
    ).stdout.strip()


class EngineeringBenchmarkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = load_manifest(BENCHMARK / "manifest.json")
        self.matrix = load_matrix(BENCHMARK / "baseline-matrix.json")

    def test_manifest_rejects_incomplete_unsafe_duplicate_and_drifted_inputs(self):
        incomplete = copy.deepcopy(self.manifest)
        del incomplete["privacy"]
        with self.assertRaisesRegex(ValueError, "manifest fields"):
            validate_manifest(incomplete)

        unsafe = copy.deepcopy(self.manifest)
        unsafe["outputs"]["generated_path"] = "../private"
        with self.assertRaisesRegex(ValueError, "safe relative"):
            validate_manifest(unsafe)

        duplicate = copy.deepcopy(self.manifest)
        duplicate["source"]["files"].append(copy.deepcopy(duplicate["source"]["files"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate evidence id"):
            validate_manifest(duplicate)

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            manifest_path = root / "manifest.json"
            local = copy.deepcopy(self.manifest)
            for resource in local["resources"]:
                (root / resource["path"]).write_text("changed")
            manifest_path.write_text(json.dumps(local))
            with self.assertRaisesRegex(ValueError, "resource drift"):
                load_manifest(manifest_path)

    def test_builds_fresh_deterministic_fixture_and_runs_oracle(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "source"
            source.mkdir()
            script = source / "rollout_stats.py"
            script.write_text(
                "#!/usr/bin/env python3\n"
                "import json,sys\n"
                "if '--self-test' in sys.argv: print('self-test passed')\n"
                "elif '--json' in sys.argv: print(json.dumps({'ok': True}))\n"
                "else: print('report ok')\n"
            )
            script.chmod(0o755)
            subprocess.run(["git", "init", "--quiet", "--initial-branch=main", str(source)], check=True)
            git(source, "add", ".")
            fixed = {
                "GIT_AUTHOR_NAME": "Fixture",
                "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                "GIT_COMMITTER_NAME": "Fixture",
                "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
                "GIT_AUTHOR_DATE": "2000-01-01T00:00:00Z",
                "GIT_COMMITTER_DATE": "2000-01-01T00:00:00Z",
            }
            git(source, "commit", "--quiet", "-m", "fixture", env=fixed)

            resources = root / "resources"
            resources.mkdir()
            values = {
                "README.md": "# Fixture\n",
                "initial.md": "initial\n",
                "extension.md": "extension\n",
                "answer-policy.json": "{}\n",
                "contracts.json": "{}\n",
            }
            for name, content in values.items():
                (resources / name).write_text(content)
            manifest = copy.deepcopy(self.manifest)
            manifest["source"]["revision"] = git(source, "rev-parse", "HEAD")
            manifest["source"]["files"][0].update(
                path="rollout_stats.py", sha256=sha256_file(script)
            )
            for resource in manifest["resources"]:
                resource["path"] = f"resources/{resource['path']}"
                resource["sha256"] = sha256_file(root / resource["path"])
            manifest_path = root / "manifest.json"
            manifest_path.write_text(json.dumps(manifest))

            first = build_fixture(manifest_path, root / "first", source)
            second = build_fixture(manifest_path, root / "second", source)

            self.assertEqual(first["fixture_head"], second["fixture_head"])
            self.assertEqual(first["fixture_tree"], second["fixture_tree"])
            self.assertEqual(first["fixture_digest"], second["fixture_digest"])
            self.assertEqual(git(root / "first/fixture", "remote"), "")
            self.assertEqual(git(root / "first/fixture", "rev-list", "--all", "--count"), "1")
            self.assertEqual((root / "first/evaluator/python-self-test.txt").read_text(), "self-test passed\n")
            self.assertFalse((root / "first/fixture/extension.md").exists())
            self.assertNotIn(str(source), (root / "first/build-record.json").read_text())

    def test_matrix_is_codex_only_paired_and_interleaved(self):
        self.assertEqual(
            [(item["arm"], item["repetition"]) for item in schedule_trials(self.matrix)],
            [(arm["id"], 1) for arm in self.matrix["arms"]],
        )
        repeated = copy.deepcopy(self.matrix)
        for arm in repeated["arms"][:2]:
            arm["repetitions"] = 2
        repeated["arms"] = repeated["arms"][:2]
        self.assertEqual(
            [(item["arm"], item["repetition"]) for item in schedule_trials(repeated)],
            [
                (repeated["arms"][0]["id"], 1),
                (repeated["arms"][1]["id"], 1),
                (repeated["arms"][0]["id"], 2),
                (repeated["arms"][1]["id"], 2),
            ],
        )
        claude = copy.deepcopy(self.matrix)
        claude["arms"][0]["host"] = "claude-code"
        with self.assertRaisesRegex(ValueError, "Codex-only"):
            validate_matrix(claude)
        history = copy.deepcopy(self.matrix)
        history["arms"][0]["context"] = "raw-history"
        with self.assertRaisesRegex(ValueError, "code-only"):
            validate_matrix(history)
        unpaired = copy.deepcopy(self.matrix)
        unpaired["arms"][0]["limits"]["turns"] += 1
        with self.assertRaisesRegex(ValueError, "undeclared factor"):
            validate_matrix(unpaired)
        unsupported = copy.deepcopy(self.matrix)
        unsupported["arms"][0]["model"] = "unknown-model"
        with self.assertRaisesRegex(ValueError, "unsupported Codex"):
            validate_matrix(unsupported)
        with self.assertRaisesRegex(ValueError, "orchestration is unavailable"):
            validate_codex_runtime(
                self.matrix["arms"][2], "multi_agent stable false\n"
            )
        validate_codex_runtime(
            self.matrix["arms"][2], "multi_agent stable true\n"
        )

    def test_controller_errors_block_later_trials(self):
        result = {
            "status": "valid",
            "harbor": {"status": "completed"},
            "stages": {
                "initial": {
                    "product": {"status": "passed"},
                    "process": {"termination": "controller_error"},
                }
            },
        }
        self.assertEqual(
            benchmark_defects(result),
            ["initial controller terminated with controller_error"],
        )

    def test_prepares_empty_home_records_config_and_detects_contamination(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            fixture = root / "fixture"
            fixture.mkdir()
            (fixture / "README.md").write_text("fixture")
            subprocess.run(["git", "init", "--quiet", str(fixture)], check=True)
            prepared = root / "prepared"
            record = prepare_vanilla_arm(self.matrix["arms"][0], fixture, prepared)
            self.assertEqual(record["home_inventory"], [])
            self.assertFalse(record["launch"]["config"]["features"]["multi_agent"])
            self.assertIn("--disable", record["launch"]["args"])
            self.assertEqual(tree_digest(prepared / "workspace"), record["workspace_digest"])
            (prepared / "home/AGENTS.md").write_text("personal")
            issues = runtime_contamination(
                prepared / "workspace",
                prepared / "home",
                stage="initial",
                extension_prompt="secret extension",
            )
            self.assertIn("undeclared home file: AGENTS.md", issues)
            (prepared / "workspace/leak.txt").write_text("secret extension")
            (prepared / "workspace/.devcraft-evaluator").mkdir()
            issues = runtime_contamination(
                prepared / "workspace",
                prepared / "home",
                stage="initial",
                extension_prompt="secret extension",
            )
            self.assertIn("extension prompt leaked into leak.txt", issues)
            self.assertIn("undeclared workspace path: .devcraft-evaluator", issues)

    def test_redacts_private_values_and_blocks_external_authority(self):
        redacted = redact(
            {
                "secret": "sk-test-secret-value",
                "path": "/Users/developer/project",
                "id": "123e4567-e89b-12d3-a456-426614174000",
            }
        )
        self.assertEqual(redacted["secret"], "[REDACTED]")
        self.assertEqual(redacted["path"], "$HOME/project")
        self.assertEqual(redacted["id"], "[ID]")
        self.assertEqual(privacy_issues(redacted), [])
        self.assertEqual(
            set(
                privacy_issues(
                    {
                        "trajectory": "token=synthetic-secret /Users/developer/project",
                        "session": "123e4567-e89b-12d3-a456-426614174000",
                    }
                )
            ),
            {"credential-like value", "personal path", "private identifier"},
        )
        self.assertIsNotNone(authority_violation("gh release create v1"))
        self.assertIsNotNone(authority_violation("cargo publish"))
        self.assertIsNotNone(authority_violation("codesign --sign identity app"))
        self.assertIsNotNone(authority_violation("git push origin main"))
        self.assertIsNotNone(authority_violation("curl https://example.com"))
        self.assertIsNone(
            authority_violation('const PRICING_SOURCE: &str = "https://example.com";')
        )
        self.assertIsNone(authority_violation("cargo test"))


if __name__ == "__main__":
    unittest.main()
