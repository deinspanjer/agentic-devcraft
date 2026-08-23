import json
import tempfile
import unittest
from pathlib import Path

from evals.harbor.port_verifier import (
    _behavior_checks,
    _hidden_cases,
    _python_command,
    _run,
    load_contracts,
    verify_extension,
    verify_initial,
)


ROOT = Path(__file__).resolve().parents[3]
CONTRACTS = ROOT / "evals/harbor/benchmarks/vanilla-port/contracts.json"
ORACLE = ROOT / "evals/harbor/generated/vanilla-port/evaluator/oracle/rollout_stats.py"


class PortVerifierTest(unittest.TestCase):
    def test_contract_inventory_is_visible_and_initial_only(self):
        inventory = load_contracts(CONTRACTS)
        self.assertTrue(inventory["contracts"])
        self.assertEqual({item["stage"] for item in inventory["contracts"]}, {"initial", "extension"})
        self.assertEqual(
            len([item for item in inventory["contracts"] if item["stage"] == "extension"]),
            4,
        )
        self.assertNotIn("prior", repr(inventory).lower())

    def test_python_oracle_passes_behavior_and_targeted_defect_is_local(self):
        self.assertTrue(ORACLE.is_file(), "build the vanilla-port fixture first")
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            cases = _hidden_cases(root / "hidden")
            expected = {}
            for case in cases:
                run = _run(_python_command(ORACLE, case["rollout"], Path(case["home"]), True), root)
                expected[case["id"]] = {"json": json.loads(run["stdout"])}

            def invoke(rollout, home, machine):
                return _run(_python_command(ORACLE, rollout, home, machine), root)

            passing = _behavior_checks(cases, expected, invoke)
            self.assertTrue(all(item["passed"] for item in passing), passing)

            def omit_descendant(rollout, home, machine):
                result = invoke(rollout, home, machine)
                if rollout == "hidden-root" and machine and result["returncode"] == 0:
                    value = json.loads(result["stdout"])
                    value["tree"] = value["rollout"]
                    value["by_rollout_type"] = {"root": value["by_rollout_type"]["root"]}
                    result["stdout"] = json.dumps(value)
                return result

            defects = {item["id"]: item["passed"] for item in _behavior_checks(cases, expected, omit_descendant)}
            self.assertFalse(defects["descendant-aggregation"])
            self.assertTrue(defects["json-report-parity"])
            self.assertTrue(defects["human-report"])
            self.assertTrue(defects["missing-rollout-error"])

            def wrong_model_totals(rollout, home, machine):
                result = invoke(rollout, home, machine)
                if rollout == "hidden-root" and machine and result["returncode"] == 0:
                    value = json.loads(result["stdout"])
                    value["by_model"]["gpt-5.6-terra"]["input_tokens"] += 1
                    result["stdout"] = json.dumps(value)
                return result

            defects = {item["id"]: item["passed"] for item in _behavior_checks(cases, expected, wrong_model_totals)}
            self.assertFalse(defects["model-token-cost-aggregation"])
            self.assertTrue(defects["descendant-aggregation"])

            def broken_text(rollout, home, machine):
                result = invoke(rollout, home, machine)
                if not machine and result["returncode"] == 0:
                    result["stdout"] = "report complete\n"
                return result

            defects = {item["id"]: item["passed"] for item in _behavior_checks(cases, expected, broken_text)}
            self.assertFalse(defects["human-report"])
            self.assertTrue(defects["json-report-parity"])

            def accepts_missing(rollout, home, machine):
                result = invoke(rollout, home, machine)
                if rollout == "definitely-missing":
                    result.update(returncode=0, stdout="empty report", stderr="")
                return result

            defects = {item["id"]: item["passed"] for item in _behavior_checks(cases, expected, accepts_missing)}
            self.assertFalse(defects["missing-rollout-error"])
            self.assertTrue(defects["json-report-parity"])

    def test_build_failure_is_product_failure_and_snapshot_is_unchanged(self):
        self.assertTrue(ORACLE.is_file(), "build the vanilla-port fixture first")
        with tempfile.TemporaryDirectory() as raw:
            snapshot = Path(raw) / "snapshot"
            snapshot.mkdir()
            (snapshot / "README.md").write_text("incomplete")
            before = (snapshot / "README.md").read_text()
            result = verify_initial(snapshot, ORACLE, CONTRACTS)
            self.assertEqual(result["status"], "failed")
            self.assertTrue(result["snapshot_unchanged"])
            self.assertEqual((snapshot / "README.md").read_text(), before)
            infrastructure = verify_initial(
                snapshot, Path(raw) / "missing-oracle.py", CONTRACTS
            )
            self.assertEqual(infrastructure["status"], "verifier_error")

    def test_alternative_black_box_passes_both_stages(self):
        self.assertTrue(ORACLE.is_file(), "build the vanilla-port fixture first")
        with tempfile.TemporaryDirectory() as raw:
            workspace = Path(raw) / "workspace"
            (workspace / "src").mkdir(parents=True)
            (workspace / "Cargo.toml").write_text(
                '[package]\nname = "alternate-port"\nversion = "0.1.0"\nedition = "2024"\n'
            )
            (workspace / "src/main.rs").write_text(
                'use std::process::{Command, exit};\n'
                'fn main() {\n'
                '  let status = Command::new("python3")\n'
                '    .arg(concat!(env!("CARGO_MANIFEST_DIR"), "/candidate.py"))\n'
                '    .args(std::env::args().skip(1)).status().unwrap();\n'
                '  exit(status.code().unwrap_or(1));\n'
                '}\n'
            )
            (workspace / "rollout_stats.py").write_bytes(ORACLE.read_bytes())
            (workspace / "candidate.py").write_text(
                "import importlib.util,json,sys\n"
                "from pathlib import Path\n"
                "spec=importlib.util.spec_from_file_location('meter',Path(__file__).with_name('rollout_stats.py'))\n"
                "meter=importlib.util.module_from_spec(spec);sys.modules['meter']=meter;spec.loader.exec_module(meter)\n"
                "if '--prices' in sys.argv:\n"
                " i=sys.argv.index('--prices'); path=sys.argv[i+1]; del sys.argv[i:i+2]\n"
                " value=json.loads(Path(path).read_text())\n"
                " if set(value)!={'models'} or not isinstance(value['models'],dict): raise ValueError('invalid price file')\n"
                " for model,rates in value['models'].items():\n"
                "  if set(rates)!={'input','cached_input','cache_write','output'}: raise ValueError('invalid rate entry')\n"
                "  values=tuple(rates[key] for key in ('input','cached_input','cache_write','output'))\n"
                "  if any(item is not None and (not isinstance(item,(int,float)) or isinstance(item,bool) or item<0) for item in values): raise ValueError('invalid rate entry')\n"
                "  meter.PRICE_HISTORY[model]=[('0001-01-01',values)]\n"
                "meter.main()\n"
            )
            result = verify_extension(workspace, ORACLE, CONTRACTS)
            self.assertEqual(result["status"], "passed", result)
            self.assertTrue(all(item["passed"] for item in result["contracts"]))
            self.assertTrue(result["snapshot_unchanged"])
            candidate = workspace / "candidate.py"
            candidate.write_text(
                candidate.read_text().replace(
                    "  meter.PRICE_HISTORY[model]=[('0001-01-01',values)]",
                    "  pass # plausible defect: validates but ignores supplied rates",
                )
            )
            defect = verify_extension(workspace, ORACLE, CONTRACTS)
            checks = {item["id"]: item["passed"] for item in defect["contracts"]}
            self.assertFalse(checks["user-price-file"])
            self.assertTrue(checks["built-in-price-defaults"])
            self.assertTrue(checks["initial-contract-regression"])
            self.assertNotIn("source_similarity", repr(defect))


if __name__ == "__main__":
    unittest.main()
