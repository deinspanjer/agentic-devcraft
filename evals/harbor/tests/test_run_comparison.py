import tempfile
import unittest
from pathlib import Path

from evals.harbor.run_comparison import create_task


class CreateTaskTests(unittest.TestCase):
    def test_scripted_task_uses_each_turn(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            workspace = root / "prepared/workspace"
            workspace.mkdir(parents=True)
            (workspace / "turn-1.md").write_text("first")
            (workspace / "turn-2.md").write_text("second")

            create_task(root / "prepared", root / "task", 30, "scripted")

            config = (root / "task/task.toml").read_text()
            self.assertIn('name = "turn-1"', config)
            self.assertIn('name = "turn-2"', config)
            self.assertEqual(
                (root / "task/steps/turn-2/instruction.md").read_text(), "second"
            )


if __name__ == "__main__":
    unittest.main()
