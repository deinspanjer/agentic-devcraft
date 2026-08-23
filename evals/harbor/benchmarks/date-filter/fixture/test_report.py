import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class ReportTest(unittest.TestCase):
    def test_json_summary(self):
        with tempfile.TemporaryDirectory() as raw:
            source = Path(raw) / "records.jsonl"
            source.write_text(
                json.dumps({"id": "one", "date": "2026-01-01", "status": "open"})
                + "\n"
                + json.dumps({"id": "two", "date": "2026-01-02", "status": "closed"})
                + "\n"
            )
            result = subprocess.run(
                ["python3", str(ROOT / "report.py"), str(source), "--json"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                json.loads(result.stdout),
                {"total": 2, "by_status": {"closed": 1, "open": 1}},
            )


if __name__ == "__main__":
    unittest.main()
