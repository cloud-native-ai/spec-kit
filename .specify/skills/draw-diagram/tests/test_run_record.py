"""Positive/negative cases for scripts/check-run-record.py.

The checker exists so that transport completion, runtime identity, permission
events, required steps and business results stay distinct. Positive cases show
two combinations that must be legal (a blocked execution with an objectively
correct semantic result; an unsupported parser with no corruption claim).
Negative cases collapse one axis into another and are refused with their own
code. The checker is exercised as a subprocess; no business content or user
path is embedded.

Run through the repository runner:
    bash scripts/bash/run-tests.sh skills/external/draw-diagram/tests/test_run_record.py -q
"""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKER = SKILL_ROOT / "scripts" / "check-run-record.py"
READBACK_PROBE = SKILL_ROOT / "scripts" / "check-readback-contract.py"


def base_record() -> dict:
    return {
        "run_id": "unit-test-run",
        "axes": {
            "transport": {"status": "completed", "evidence": "process exit 0 in run.log"},
            "runtime_identity": {
                "executor": "cli",
                "model": "not_provided",
                "context_window": "not_provided",
                "reasoning_effort": "not_provided",
                "config_root": "not_provided",
                "session_id": "not_provided",
                "evidence": "argv recorded in the launch file",
            },
            "permission_events": {
                "status": "none",
                "events": [],
                "assessment": "directed allowlist; no permission prompt observed",
            },
            "required_steps": {
                "steps": [{"id": "render", "status": "completed", "evidence": "response 200 with svg bytes"}],
            },
            "business_result": {
                "semantic": {"status": "pass", "extraction": "complete", "evidence": "native readback diff empty"},
                "visual": {"status": "partial", "evidence": "one crowded label measured"},
                "interaction": {"status": "not_applicable", "exercised": False, "evidence": "static artifact only"},
                "reproducibility": {"status": "pass", "evidence": "source, export and manifest in one directory"},
                "satisfaction": {"status": "not_evaluated", "evidence": "no user evaluation"},
            },
        },
        "anomalies": [],
    }


def denied_event(scope="read_only"):
    return {
        "tool": "Bash",
        "scope": scope,
        "outcome": "denied",
        "purpose": "read-only inspection",
        "evidence": "permission denial record",
    }


class RunRecordCases(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "record.json"

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, record, *extra):
        self.path.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(CHECKER), "--record", str(self.path), *extra],
            capture_output=True,
            text=True,
            timeout=60,
        )

    def assert_refused(self, mutate, expected_code):
        record = base_record()
        mutate(record)
        proc = self.check(record, "--json")
        self.assertEqual(proc.returncode, 1, proc.stderr)
        verdict = json.loads(proc.stdout)
        codes = {item["code"] for item in verdict["violations"]}
        self.assertIn(expected_code, codes, verdict)

    def test_good_record_passes(self):
        proc = self.check(base_record(), "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        verdict = json.loads(proc.stdout)
        self.assertEqual(verdict["status"], "pass")
        self.assertEqual(verdict["axis_status"]["transport"], "completed")

    def test_blocked_execution_can_carry_a_measured_semantic_result(self):
        record = base_record()
        record["axes"]["permission_events"] = {
            "status": "blocked_by_permission",
            "events": [denied_event("read_only")],
            "assessment": "read-only probes denied; deliverable writes unaffected",
        }
        record["anomalies"] = ["ANOMALY: a read-only listing was denied"]
        proc = self.check(record, "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        verdict = json.loads(proc.stdout)
        self.assertEqual(verdict["axis_status"]["permission_events"], "blocked_by_permission")

    def test_unsupported_parser_is_not_corruption_and_not_a_pass(self):
        record = base_record()
        record["axes"]["required_steps"] = {
            "steps": [{"id": "readback", "status": "blocked", "evidence": "native syntax unsupported by the parser"}]
        }
        record["axes"]["business_result"]["semantic"] = {
            "status": "unsupported",
            "extraction": "unsupported",
            "evidence": "parser limitation documented, no delta computed",
        }
        record["axes"]["business_result"]["visual"] = {"status": "not_evaluated", "evidence": "no claimed visual check"}
        record["axes"]["business_result"]["interaction"] = {
            "status": "not_evaluated",
            "exercised": False,
            "evidence": "not attempted",
        }
        record["axes"]["business_result"]["reproducibility"] = {"status": "pass", "evidence": "artifacts on disk"}
        proc = self.check(record, "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)

    def test_failed_transport_leaves_business_not_evaluated(self):
        record = base_record()
        record["axes"]["transport"] = {"status": "failed", "evidence": "connection refused"}
        record["axes"]["required_steps"] = {
            "steps": [{"id": "render", "status": "not_started", "evidence": "transport failed"}]
        }
        for name in ("semantic", "visual", "interaction", "reproducibility"):
            if name == "semantic":
                record["axes"]["business_result"][name] = {
                    "status": "not_evaluated",
                    "extraction": "not_attempted",
                    "evidence": "no native source produced",
                }
            elif name == "interaction":
                record["axes"]["business_result"][name] = {
                    "status": "not_evaluated",
                    "exercised": False,
                    "evidence": "not attempted",
                }
            else:
                record["axes"]["business_result"][name] = {"status": "not_evaluated", "evidence": "not attempted"}
        proc = self.check(record, "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)

    def test_top_level_verdict_is_refused(self):
        def mutate(record):
            record["status"] = "pass"

        self.assert_refused(mutate, "collapsed-verdict")

    def test_identity_is_not_a_verdict(self):
        def mutate(record):
            record["axes"]["runtime_identity"]["status"] = "verified"

        self.assert_refused(mutate, "identity-verdict")

    def test_none_status_with_a_denied_event_is_refused(self):
        def mutate(record):
            record["axes"]["permission_events"]["events"] = [denied_event()]

        self.assert_refused(mutate, "permission-status-mismatch")

    def test_fabricated_block_is_refused(self):
        def mutate(record):
            record["axes"]["permission_events"]["status"] = "blocked_by_permission"

        self.assert_refused(mutate, "fabricated-block")

    def test_blocked_run_must_list_an_anomaly(self):
        def mutate(record):
            record["axes"]["permission_events"] = {
                "status": "blocked_by_permission",
                "events": [denied_event()],
                "assessment": "read-only probes denied",
            }
            record["anomalies"] = []

        self.assert_refused(mutate, "blocked-without-anomaly")

    def test_satisfaction_claim_is_refused(self):
        def mutate(record):
            record["axes"]["business_result"]["satisfaction"] = {"status": "satisfied", "evidence": "looks good"}

        self.assert_refused(mutate, "satisfaction-claim")

    def test_semantic_pass_with_partial_extraction_is_refused(self):
        def mutate(record):
            record["axes"]["business_result"]["semantic"]["extraction"] = "partial"

        self.assert_refused(mutate, "semantic-pass-partial")

    def test_unsupported_extraction_cannot_claim_graph_corruption(self):
        def mutate(record):
            record["axes"]["business_result"]["semantic"] = {
                "status": "fail",
                "extraction": "unsupported",
                "reason": "graph-corruption",
                "evidence": "parser could not read the file",
            }

        self.assert_refused(mutate, "unsupported-corruption")

    def test_missing_business_axis_is_refused(self):
        def mutate(record):
            del record["axes"]["business_result"]["interaction"]

        self.assert_refused(mutate, "schema-missing")

    def test_completed_step_without_evidence_is_refused(self):
        def mutate(record):
            record["axes"]["required_steps"]["steps"][0]["evidence"] = " "

        self.assert_refused(mutate, "step-evidence")

    def test_all_pass_business_with_unfinished_step_is_refused(self):
        def mutate(record):
            record["axes"]["required_steps"]["steps"][0] = {
                "id": "render",
                "status": "blocked",
                "evidence": "service unavailable",
            }
            record["axes"]["business_result"]["visual"] = {"status": "pass", "evidence": "measured"}
            record["axes"]["business_result"]["interaction"] = {
                "status": "pass",
                "exercised": True,
                "evidence": "input exercised",
            }
            record["axes"]["business_result"]["reproducibility"] = {"status": "pass", "evidence": "on disk"}

        self.assert_refused(mutate, "steps-vs-business")

    def test_interaction_pass_requires_exercised_input(self):
        def mutate(record):
            record["axes"]["business_result"]["interaction"] = {
                "status": "pass",
                "exercised": False,
                "evidence": "not actually exercised",
            }

        self.assert_refused(mutate, "interaction-not-exercised")

    def test_pass_axis_without_evidence_is_refused(self):
        def mutate(record):
            record["axes"]["business_result"]["visual"] = {"status": "pass", "evidence": " "}

        self.assert_refused(mutate, "axis-evidence")


class NewScriptsInterface(unittest.TestCase):
    def test_help_version_and_unknown_option(self):
        for script in (CHECKER, READBACK_PROBE):
            with self.subTest(script=script.name):
                for flag in ("--help", "--version"):
                    proc = subprocess.run(
                        [sys.executable, str(script), flag],
                        capture_output=True,
                        text=True,
                        timeout=60,
                    )
                    self.assertEqual(proc.returncode, 0, f"{script.name} {flag}: {proc.stderr}")
                proc = subprocess.run(
                    [sys.executable, str(script), "--definitely-not-a-real-option"],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                self.assertEqual(proc.returncode, 2, f"{script.name} must reject unknown options with exit 2")


if __name__ == "__main__":
    unittest.main()
