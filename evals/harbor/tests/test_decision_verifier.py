import json
import unittest
from pathlib import Path

from evals.harbor.decision_verifier import verify_decision_evolution


EXPECTED = json.loads(Path("evals/harbor/expectations/decision-evolution.json").read_text())


class DecisionVerifierTest(unittest.TestCase):
    def test_scores_each_decision_evolution_concern_separately(self):
        response = {
            "changed_basis": [{"id": "B1", "from": "30 days allowed", "to": "7 days maximum"}],
            "current_decision": {"id": "D2", "value": "retain-7-days"},
            "history": [{"id": "D1", "status": "superseded", "replaced_by": "D2"}],
            "downstream": [
                {"id": "batch-window", "value": "7-days-max"},
                {"id": "storage-estimate", "value": "210-gb"},
            ],
        }
        result = verify_decision_evolution(EXPECTED, response)
        self.assertTrue(result["changed_basis"]["passed"])
        self.assertTrue(result["replacement_decision"]["passed"])
        self.assertTrue(result["supersession_history"]["passed"])
        self.assertTrue(result["downstream_effects"]["passed"])

    def test_missing_downstream_update_does_not_erase_other_successes(self):
        response = {
            "changed_basis": [{"id": "B1", "from": "30 days allowed", "to": "7 days maximum"}],
            "current_decision": {"id": "D2", "value": "retain-7-days"},
            "history": [{"id": "D1", "status": "superseded", "replaced_by": "D2"}],
            "downstream": [{"id": "batch-window", "value": "7-days-max"}],
        }
        result = verify_decision_evolution(EXPECTED, response)
        self.assertTrue(result["replacement_decision"]["passed"])
        self.assertFalse(result["downstream_effects"]["passed"])


if __name__ == "__main__":
    unittest.main()
