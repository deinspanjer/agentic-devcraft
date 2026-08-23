import json
import shutil
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from harbor.models.agent.context import AgentContext

from evals.harbor.adaptive_agent import (
    AdaptiveAgent,
    CONTROLLER_SCHEMA,
    normalize_controller_decision,
)
from evals.harbor.controller import validate_decision


class FakeEnvironment:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace

    async def exec(self, command, **_):
        if "rev-parse --abbrev-ref" in command:
            return SimpleNamespace(stdout="main\nfixture-head\n", return_code=0)
        if "log -5" in command:
            return SimpleNamespace(stdout="fixture commit\n", return_code=0)
        if "status --porcelain" in command:
            return SimpleNamespace(stdout="?? src/\n", return_code=0)
        return SimpleNamespace(stdout="", return_code=0)

    async def download_dir(self, _source: str, target: Path) -> None:
        self.assert_target_exists = target.is_dir()
        shutil.copytree(self.workspace, target, dirs_exist_ok=True)


class FakeSubject:
    def __init__(self, logs: Path, workspace: Path, extension: str) -> None:
        self.logs = logs
        self.workspace = workspace
        self.extension = extension
        self.session_id = "same-native-session"
        self.messages = []
        self.steps = []

    def _record(self, role: str, message: str) -> None:
        self.steps.append({"source": role, "message": message})
        (self.logs / "trajectory.json").write_text(json.dumps({"steps": self.steps}))

    async def run(self, instruction, _environment, _context):
        self.messages.append(instruction)
        self._record("user", instruction)
        (self.workspace / "initial.txt").write_text("initial")
        self._record("agent", "Initial implementation complete; cargo test passed.")

    async def resume(self, message, _environment, _context):
        self.messages.append(message)
        self._record("user", message)
        if message == self.extension:
            (self.workspace / "extension.txt").write_text("extension")
            self._record("agent", "Extension implementation complete; cargo test passed.")
        else:
            self._record("agent", "Continued.")

    def populate_context_post_run(self, _context):
        pass


class AdaptiveScenarioTest(unittest.IsolatedAsyncioTestCase):
    def test_controller_schema_is_strict_and_nullable(self):
        self.assertEqual(
            set(CONTROLLER_SCHEMA["required"]),
            set(CONTROLLER_SCHEMA["properties"]),
        )
        self.assertIn("null", CONTROLLER_SCHEMA["properties"]["reason"]["type"])
        self.assertEqual(
            normalize_controller_decision(
                {
                    "action": "complete",
                    "category": None,
                    "basis_ids": ["validation_claims"],
                    "message": None,
                    "reason": "validated",
                }
            ),
            {"action": "complete", "basis_ids": [], "reason": "validated"},
        )
        policy = {
            "version": "v1",
            "progress": {"id": "progress", "message": "status"},
            "answers": [],
            "stop_reasons": ["scenario_gap"],
        }
        decision = normalize_controller_decision(
            {
                "action": "complete",
                "category": "progress",
                "basis_ids": ["progress"],
                "message": "status",
                "reason": "validated",
            }
        )
        self.assertEqual(
            validate_decision(decision, policy=policy, stage="initial"),
            {"action": "complete", "basis_ids": [], "reason": "validated"},
        )
        self.assertEqual(
            normalize_controller_decision(
                {
                    "action": "complete",
                    "category": None,
                    "basis_ids": [],
                    "message": None,
                    "reason": None,
                }
            ),
            {"action": "complete", "basis_ids": [], "reason": "completed"},
        )

    def test_authority_scan_uses_commands_not_patch_contents(self):
        trajectory = {
            "steps": [
                {
                    "tool_calls": [
                        {
                            "arguments": {
                                "input": "const patch = 'gh release https://example.com'; tools.apply_patch(patch);"
                            }
                        },
                        {
                            "arguments": {
                                "input": 'await tools.exec_command({cmd:"cargo test"});'
                            }
                        },
                    ]
                }
            ]
        }
        self.assertEqual(
            AdaptiveAgent._command_inputs(trajectory),
            ['await tools.exec_command({cmd:"cargo test"});'],
        )

    async def test_two_stage_scenario_keeps_session_and_separate_checkpoints(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            logs = root / "logs"
            workspace = root / "workspace"
            logs.mkdir()
            workspace.mkdir()
            policy_path = root / "policy.json"
            extension_path = root / "extension.md"
            policy_path.write_text(
                json.dumps(
                    {
                        "version": "v1",
                        "progress": {"id": "progress", "message": "status"},
                        "answers": [],
                        "stop_reasons": ["scenario_gap"],
                    }
                )
            )
            extension_path.write_text("Add price-file support.\n")
            agent = AdaptiveAgent(
                logs_dir=logs,
                model_name="gpt-5.6-sol",
                subject_agent="codex",
                controller_agent="codex",
                scenario_policy_path=str(policy_path),
                extension_prompt_path=str(extension_path),
                max_turns=10,
            )
            subject = FakeSubject(logs, workspace, "Add price-file support.")
            agent._subject = subject
            requests = []

            async def complete(request):
                requests.append(request)
                return {"action": "complete", "basis_ids": [], "reason": "validated"}

            agent._testing_agent = complete
            with patch(
                "evals.harbor.adaptive_agent.verify_initial",
                return_value={"status": "passed", "contracts": []},
            ), patch(
                "evals.harbor.adaptive_agent.verify_extension",
                return_value={"status": "passed", "contracts": []},
            ):
                agent._verifier_contracts = root / "contracts.json"
                agent._verifier_oracle = root / "oracle.py"
                environment = FakeEnvironment(workspace)
                result = await agent._run_scenario(
                    "Port the report.", environment, AgentContext(), time.monotonic()
                )

            self.assertEqual(result["session_id"], "same-native-session")
            self.assertTrue(environment.assert_target_exists)
            self.assertEqual(subject.messages, ["Port the report.", "Add price-file support."])
            self.assertTrue((logs / "snapshots/initial/initial.txt").is_file())
            self.assertFalse((logs / "snapshots/initial/extension.txt").exists())
            self.assertTrue((logs / "snapshots/extension/extension.txt").is_file())
            self.assertNotEqual(
                result["checkpoints"][0]["workspace_digest"],
                result["checkpoints"][1]["workspace_digest"],
            )
            self.assertEqual(result["checkpoints"][0]["verifier"]["status"], "passed")
            self.assertEqual(result["checkpoints"][1]["verifier"]["status"], "passed")
            self.assertNotIn(
                "OPENAI_API_KEY",
                result["checkpoints"][0]["effective_configuration"]["controller_environment_keys"],
            )
            self.assertEqual(
                result["checkpoints"][1]["parent_workspace_digest"],
                result["checkpoints"][0]["workspace_digest"],
            )
            self.assertNotIn("Add price-file support.", repr(result["checkpoints"][0]))
            self.assertEqual([request["stage"] for request in requests], ["initial", "extension"])
            self.assertNotIn("arm", repr(requests).lower())
            self.assertNotIn("expected", repr(requests).lower())


if __name__ == "__main__":
    unittest.main()
