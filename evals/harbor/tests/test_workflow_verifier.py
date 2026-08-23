import json
import shutil
import tempfile
import unittest
from pathlib import Path

from evals.harbor.workflow_verifier import verify_workflow_ownership


FIXTURE = Path("evals/harbor/fixtures/workflow-ownership")
EXPECTED = json.loads(Path("evals/harbor/expectations/workflow-ownership.json").read_text())


class WorkflowVerifierTest(unittest.TestCase):
    def test_accepts_only_the_selected_openspec_workflow(self):
        with tempfile.TemporaryDirectory() as temp:
            before = Path(temp) / "before"
            after = Path(temp) / "after"
            shutil.copytree(FIXTURE, before)
            shutil.copytree(FIXTURE, after)
            (after / "greeting.txt").write_text("hello\n")
            (after / "openspec/changes/add-greeting/tasks.md").write_text(
                "- [x] Create `greeting.txt` containing `hello`.\n"
            )
            result = verify_workflow_ownership(before, after, EXPECTED)
            self.assertTrue(result["workflow_result"]["passed"])
            self.assertTrue(result["detours"]["passed"])
            self.assertTrue(result["unauthorized_workflow_mutation"]["passed"])

    def test_reports_competing_route_and_duplicate_entry_separately(self):
        with tempfile.TemporaryDirectory() as temp:
            before = Path(temp) / "before"
            after = Path(temp) / "after"
            shutil.copytree(FIXTURE, before)
            shutil.copytree(FIXTURE, after)
            (after / ".devcraft").mkdir()
            (after / ".devcraft/route-entered").touch()
            (after / "docs/plans").mkdir(parents=True)
            (after / "docs/plans/greeting.md").write_text("duplicate plan\n")
            result = verify_workflow_ownership(before, after, EXPECTED)
            self.assertEqual(result["detours"]["paths"], [".devcraft/route-entered"])
            self.assertEqual(result["duplicate_workflow_entry"]["paths"], ["docs/plans/greeting.md"])
            self.assertEqual(len(result["unauthorized_workflow_mutation"]["paths"]), 2)


if __name__ == "__main__":
    unittest.main()
