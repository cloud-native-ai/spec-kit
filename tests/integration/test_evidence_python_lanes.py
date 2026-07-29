"""Integration tests for the native Python lanes (runs/feedback), degradation, and package exclusion.

Spec 034 US3 — contracts C-E4.3 / C-E9 / C-E10 / C-F13, SC-003.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / ".specify" / "scripts" / "python" / "evidence-utils.py"


def run_cli(*args, cwd, env=None):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=str(cwd), timeout=300, env=env,
    )


def make_workspace(tmp_path: Path, *, complete_team=True, partial_team=True,
                   feedback_entries=0, with_index=True) -> Path:
    ws = tmp_path / "ws"
    (ws / ".specify" / "memory" / "evidence").mkdir(parents=True)
    fb = ws / ".specify" / "memory" / "feedback"
    fb.mkdir(parents=True)
    teams = ws / ".specify" / "teams"
    teams.mkdir(parents=True)

    if complete_team:
        team = teams / "full-team"
        (team / "runs").mkdir(parents=True)
        (team / "runs" / "20260101T000000Z-report.md").write_text("# r1\n", encoding="utf-8")
        (team / "runs" / "20260102T000000Z-report.md").write_text("# r2\n", encoding="utf-8")
        (team / "STATE.md").write_text(
            "# Team State — full-team\n\n## High Priority\n\n## Watch List\n\n## Recent Noise\n\n"
            "## Post-Run Critique (每 cycle 追加，用于晋级判据)\n"
            "- 2026-01-01T00:00:00Z: cycle ok / secret sk-abcdefghijklmnopqrstuv should be masked\n",
            encoding="utf-8")
        rows = [
            {"cycle": "2026-01-01T00:00:00Z", "maturity": "L1", "items_found": 5,
             "actions_taken": 0, "escalations": 2, "tokens_estimate": 45000, "outcome": "report-only"},
            {"cycle": "2026-01-02T00:00:00Z", "maturity": "L1", "items_found": 3,
             "actions_taken": 1, "escalations": 1, "tokens_estimate": 30000, "outcome": "report-only"},
        ]
        (team / "run-log.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")

    if partial_team:
        team = teams / "bare-team"
        (team / "runs").mkdir(parents=True)
        (team / "runs" / "20260103T000000Z-report.md").write_text("# r\n", encoding="utf-8")

    entries = []
    for i in range(feedback_entries):
        eid = f"2026010{(i % 9) + 1}T00000{i}Z-skill-demo"
        fname = f"{eid}.md"
        point = "tighten reference extraction step" if i % 2 == 0 else f"unique point {i}"
        (fb / fname).write_text(
            f"---\nid: {eid}\nunit_id: skill:demo\nunit_type: skill\nrun_id: r{i}\n"
            f"scope: local\nfeature: \"\"\npartial: false\ncreated: 2026-01-0{(i % 9) + 1}T00:00:0{i}Z\n"
            f"summary: demo {i}\n---\n\n## Review\nok\n\n## Optimization Points\n- {point}\n",
            encoding="utf-8")
        entries.append({"id": eid, "file": fname, "unit_id": "skill:demo",
                        "unit_type": "skill", "run_id": f"r{i}", "feature": "",
                        "partial": False, "created": f"2026-01-0{(i % 9) + 1}T00:00:0{i}Z",
                        "summary": f"demo {i}"})
    if with_index and feedback_entries:
        (fb / "index.json").write_text(json.dumps({
            "store": "feedback", "updated": "2026-01-09T00:00:00Z", "threshold": 10,
            "count_since_submission": feedback_entries, "submitted_at": None,
            "entries": entries}), encoding="utf-8")
    return ws


class TestRunsLane:
    def test_partial_degradation_for_incomplete_team(self, tmp_path):
        ws = make_workspace(tmp_path, feedback_entries=1)
        result = run_cli("--action", "collect", "--target", "project", "--lanes", "runs", cwd=ws)
        assert result.returncode == 0, result.stderr
        out = json.loads(result.stdout)
        assert out["lanes"]["runs"] == "partial"
        findings = json.loads((ws / out["path"] / "findings.json").read_text(encoding="utf-8"))
        assert findings["lanes"]["runs"]["teamsScanned"] == 2
        team_items = [e for e in findings["evidence"] if e["lane"] == "runs"]
        assert len(team_items) == 2
        full = next(e for e in team_items if "full-team" in e["summary"])
        assert full["evidenceState"] == "Exercised"
        assert full["signals"]["loggedCycles"] == 2
        assert full["signals"]["escalations"] == 3

    def test_all_complete_team_is_available(self, tmp_path):
        ws = make_workspace(tmp_path, partial_team=False, feedback_entries=1)
        result = run_cli("--action", "collect", "--target", "project", "--lanes", "runs", cwd=ws)
        out = json.loads(result.stdout)
        assert out["lanes"]["runs"] == "available"

    def test_no_teams_dir_unavailable(self, tmp_path):
        ws = make_workspace(tmp_path, complete_team=False, partial_team=False, feedback_entries=1)
        import shutil
        shutil.rmtree(ws / ".specify" / "teams")
        result = run_cli("--action", "collect", "--target", "project", "--lanes", "runs", cwd=ws)
        assert result.returncode == 0
        out = json.loads(result.stdout)
        assert out["lanes"]["runs"] == "unavailable"

    def test_critique_secret_masked(self, tmp_path):
        ws = make_workspace(tmp_path, feedback_entries=1)
        result = run_cli("--action", "collect", "--target", "project", "--lanes", "runs", cwd=ws)
        out = json.loads(result.stdout)
        lane_file = ws / out["path"] / "lanes" / "runs.json"
        assert "sk-abcdefghijklmnopqrstuv" not in lane_file.read_text(encoding="utf-8")


class TestFeedbackLane:
    def test_recurrence_aggregation(self, tmp_path):
        ws = make_workspace(tmp_path, feedback_entries=6)
        result = run_cli("--action", "collect", "--target", "project", "--lanes", "feedback", cwd=ws)
        assert result.returncode == 0, result.stderr
        out = json.loads(result.stdout)
        assert out["lanes"]["feedback"] == "available"
        findings = json.loads((ws / out["path"] / "findings.json").read_text(encoding="utf-8"))
        assert findings["lanes"]["feedback"]["entries"] == 6
        recurring = [e for e in findings["evidence"]
                     if e["lane"] == "feedback" and "recurrence" in e["signals"]]
        assert recurring, "expected a recurring-theme evidence item"
        assert recurring[0]["signals"]["recurrence"] == 3
        assert recurring[0]["evidenceRefs"], "recurrence item must reference entry paths"

    def test_index_missing_fallback_partial(self, tmp_path):
        ws = make_workspace(tmp_path, feedback_entries=4, with_index=False)
        result = run_cli("--action", "collect", "--target", "project", "--lanes", "feedback", cwd=ws)
        out = json.loads(result.stdout)
        assert out["lanes"]["feedback"] == "partial"


class TestNoNodeDegradation:
    def test_collect_all_without_node(self, tmp_path):
        """SC-003: three Node lanes degrade explicitly; runs/feedback still deliver."""
        ws = make_workspace(tmp_path, feedback_entries=2)
        env = dict(os.environ)
        env["PATH"] = "/usr/bin-nonexistent"  # no node resolvable
        result = run_cli("--action", "collect", "--target", "project", "--lanes", "all",
                         cwd=ws, env=env)
        assert result.returncode == 0, result.stderr
        out = json.loads(result.stdout)
        for lane in ("session", "project", "assets"):
            assert out["lanes"][lane] == "unavailable", lane
        assert out["lanes"]["runs"] in ("available", "partial")
        assert out["lanes"]["feedback"] == "available"
        findings = json.loads((ws / out["path"] / "findings.json").read_text(encoding="utf-8"))
        manifest = json.loads((ws / out["path"] / "manifest.json").read_text(encoding="utf-8"))
        for lane in ("session", "project", "assets"):
            assert manifest["lanes"][lane]["reason"], lane
            node_items = [e for e in findings["evidence"] if e["lane"] == lane]
            assert node_items and node_items[0]["evidenceState"] == "Unobserved"


class TestCompareBasics:
    def test_compare_two_runs_signal_deltas(self, tmp_path):
        ws = make_workspace(tmp_path, feedback_entries=2)
        r1 = run_cli("--action", "collect", "--target", "project", "--lanes", "feedback", cwd=ws)
        assert r1.returncode == 0
        # add two more feedback entries to change signals
        fb = ws / ".specify" / "memory" / "feedback"
        for i in (7, 8):
            fname = f"20260107T00000{i}Z-skill-demo.md"
            (fb / fname).write_text(
                f"---\nid: x{i}\nunit_id: skill:demo\nunit_type: skill\nrun_id: rr{i}\n"
                f"scope: local\nfeature: \"\"\npartial: false\ncreated: 2026-01-07T00:00:0{i}Z\n"
                f"summary: d{i}\n---\n\n## Review\nok\n\n## Optimization Points\n- tighten reference extraction step\n",
                encoding="utf-8")
        # index is now stale → lane goes partial but still counts files? No: index used as-is.
        # Remove index to force full scan of all 4 files.
        (fb / "index.json").unlink()
        r2 = run_cli("--action", "collect", "--target", "project", "--lanes", "feedback", cwd=ws)
        assert r2.returncode == 0
        result = run_cli("--action", "compare", "--target", "project", cwd=ws)
        assert result.returncode == 0, result.stdout
        payload = json.loads(result.stdout)
        assert payload["baseline"] and payload["current"]
        entry_deltas = [d for d in payload["signalDeltas"] if d["signalKey"] == "entries"]
        assert entry_deltas and entry_deltas[0]["after"] > entry_deltas[0]["before"]
