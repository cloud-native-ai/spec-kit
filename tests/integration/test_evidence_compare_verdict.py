"""Integration tests for compare's intervention verdict (spec 034 US6, C-E7/C-F14)."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / ".specify" / "scripts" / "python" / "evidence-utils.py"


def run_cli(*args, cwd):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=str(cwd), timeout=300,
    )


def write_feedback(ws: Path, count: int, start: int = 0):
    fb = ws / ".specify" / "memory" / "feedback"
    fb.mkdir(parents=True, exist_ok=True)
    for i in range(start, start + count):
        fname = f"20260101T0000{i:02d}Z-skill-demo.md"
        (fb / fname).write_text(
            f"---\nid: e{i}\nunit_id: skill:demo\nunit_type: skill\nrun_id: r{i}\n"
            f"scope: local\nfeature: \"\"\npartial: false\ncreated: 2026-01-01T00:00:{i:02d}Z\n"
            f"summary: d{i}\n---\n\n## Review\nok\n\n## Optimization Points\n- shared recurring theme point\n",
            encoding="utf-8")


def make_two_runs(tmp_path: Path, extra_entries: int = 2):
    ws = tmp_path / "ws"
    (ws / ".specify" / "memory" / "evidence").mkdir(parents=True)
    write_feedback(ws, 2)
    r1 = run_cli("--action", "collect", "--target", "project", "--lanes", "feedback", cwd=ws)
    assert r1.returncode == 0, r1.stderr
    baseline_id = json.loads(r1.stdout)["runId"]
    write_feedback(ws, extra_entries, start=10)
    r2 = run_cli("--action", "collect", "--target", "project", "--lanes", "feedback", cwd=ws)
    assert r2.returncode == 0, r2.stderr
    current_id = json.loads(r2.stdout)["runId"]
    if baseline_id == current_id:
        pytest.skip("run ids collided within one second")
    return ws, baseline_id, current_id


def baseline_finding_id(ws: Path, baseline_id: str) -> str:
    findings = json.loads(
        (ws / ".specify" / "memory" / "evidence" / baseline_id / "findings.json")
        .read_text(encoding="utf-8"))
    return findings["evidence"][0]["id"]


def write_intervention(ws: Path, baseline_id: str, *, target=None, signal_key="entries",
                       direction="improve"):
    target = target or baseline_finding_id(ws, baseline_id)
    payload = {
        "targetFinding": target,
        "change": "test change",
        "baselineRunId": baseline_id,
        "expectedSignal": {"signalKey": signal_key, "direction": direction},
    }
    path = ws / ".specify" / "memory" / "evidence" / baseline_id / "intervention.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


class TestVerdict:
    def test_improved_signal_outcome_supported(self, tmp_path):
        ws, baseline_id, current_id = make_two_runs(tmp_path, extra_entries=3)
        ledger = write_intervention(ws, baseline_id, signal_key="entries", direction="improve")
        result = run_cli("--action", "compare", "--target", "project", cwd=ws)
        assert result.returncode == 0, result.stdout
        payload = json.loads(result.stdout)
        assert payload["intervention"]["verdict"] == "Outcome-supported"
        assert json.loads(ledger.read_text(encoding="utf-8"))["verdict"] == "Outcome-supported"

    def test_no_comparable_signal_unobserved(self, tmp_path):
        ws, baseline_id, current_id = make_two_runs(tmp_path)
        ledger = write_intervention(ws, baseline_id, signal_key="nonexistentSignal")
        result = run_cli("--action", "compare", "--target", "project", cwd=ws)
        payload = json.loads(result.stdout)
        assert payload["intervention"]["verdict"] == "Unobserved"
        assert json.loads(ledger.read_text(encoding="utf-8"))["verdict"] == "Unobserved"

    def test_wrong_direction_stays_unobserved(self, tmp_path):
        ws, baseline_id, current_id = make_two_runs(tmp_path, extra_entries=3)
        write_intervention(ws, baseline_id, signal_key="entries", direction="reduce")
        result = run_cli("--action", "compare", "--target", "project", cwd=ws)
        payload = json.loads(result.stdout)
        assert payload["intervention"]["verdict"] == "Unobserved"

    def test_unknown_target_finding_errors(self, tmp_path):
        ws, baseline_id, current_id = make_two_runs(tmp_path)
        write_intervention(ws, baseline_id, target="ev-999")
        result = run_cli("--action", "compare", "--target", "project", cwd=ws)
        assert result.returncode == 1
        assert "targetFinding" in json.loads(result.stdout)["error"]

    def test_verdict_write_back_idempotent(self, tmp_path):
        ws, baseline_id, current_id = make_two_runs(tmp_path, extra_entries=3)
        ledger = write_intervention(ws, baseline_id)
        run_cli("--action", "compare", "--target", "project", cwd=ws)
        first = ledger.read_text(encoding="utf-8")
        run_cli("--action", "compare", "--target", "project", cwd=ws)
        assert ledger.read_text(encoding="utf-8") == first
