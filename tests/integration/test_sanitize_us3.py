"""Integration test: US3 confirmed-cleanup journey (requirement 045 / Feature 047).

Unconfirmed apply rejected with zero deletion/move -> user confirms -> apply
executes -> finding state pending->resolved -> execution report carries the
three elements (SC-003).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "sanitize-utils.py"
STORE_REL = Path(".specify") / "memory" / "sanitize" / "findings.json"
PLAN_REL = Path(".specify") / "memory" / "sanitize" / "cleanup-plan.json"
FIXTURE = ROOT / "tests" / "fixtures" / "sanitize" / "stale-todo" / "parked-todo.md"


def run_engine(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        cwd=str(cwd), capture_output=True, text=True, timeout=120,
    )


def sid(category: str, target: str) -> str:
    return hashlib.sha1(f"{category}|{target}".encode()).hexdigest()[:12]


def assemble(tmp_path: Path) -> Path:
    todo = tmp_path / ".specify" / "memory" / "todo"
    todo.mkdir(parents=True, exist_ok=True)
    (todo / "20260812-backlog.md").write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "scripts" / "python").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "python" / "evidence-utils.py").write_text("#\n", encoding="utf-8")
    (tmp_path / "scripts" / "js").mkdir(parents=True, exist_ok=True)  # silence path refs
    subprocess.run(["git", "init", "-q"], cwd=str(tmp_path), capture_output=True)
    return tmp_path


def record_stale_finding(ws: Path) -> dict:
    target = ".specify/memory/todo/20260812-backlog.md"
    finding = {
        "id": sid("stale-residue", target),
        "category": "stale-residue", "target": target, "severity": "high",
        "summary": "claims five items unlanded while abc1234 landed them",
        "evidenceRefs": [{"kind": "commit", "ref": "abc1234"}],
        "detection": "semantic", "disposition": "delete",
        "reversibility": "irreversible", "state": "pending",
    }
    verdicts = ws / "verdicts.json"
    verdicts.write_text(json.dumps({"findings": [finding]}), encoding="utf-8")
    proc = run_engine(["--action", "record", "--file", str(verdicts),
                       "--workspace-root", str(ws)], cwd=ws)
    assert proc.returncode == 0, proc.stdout
    return finding


def make_plan(ws: Path, finding: dict, confirmed: bool) -> Path:
    plan = ws / PLAN_REL
    plan.parent.mkdir(parents=True, exist_ok=True)
    plan.write_text(json.dumps({
        "created": "2026-08-20T00:00:00Z", "confirmed": confirmed,
        "items": [{"findingId": finding["id"], "disposition": "delete",
                   "target": finding["target"]}],
    }), encoding="utf-8")
    return plan


def test_us3_gate_then_confirmed_apply(tmp_path):
    ws = assemble(tmp_path)
    run_engine(["--action", "collect", "--workspace-root", str(ws)], cwd=ws)
    finding = record_stale_finding(ws)
    material = ws / finding["target"]

    # 1) unconfirmed plan -> rejected, zero deletion (SC-003 first half)
    plan = make_plan(ws, finding, confirmed=False)
    proc = run_engine(["--action", "apply", "--plan", str(plan),
                       "--workspace-root", str(ws)], cwd=ws)
    assert proc.returncode == 2
    assert material.is_file()
    store = {f["id"]: f for f in json.loads((ws / STORE_REL).read_text(encoding="utf-8"))["findings"]}
    assert store[finding["id"]]["state"] == "pending"

    # 2) user confirms -> apply executes
    plan = make_plan(ws, finding, confirmed=True)
    proc = run_engine(["--action", "apply", "--plan", str(plan),
                       "--workspace-root", str(ws)], cwd=ws)
    assert proc.returncode == 0, proc.stdout
    assert not material.exists(), "confirmed delete must remove the material"

    # 3) state updated + plan marked executed (audit trace)
    store = {f["id"]: f for f in json.loads((ws / STORE_REL).read_text(encoding="utf-8"))["findings"]}
    assert store[finding["id"]]["state"] == "resolved"
    executed_plan = json.loads((ws / PLAN_REL).read_text(encoding="utf-8"))
    assert executed_plan.get("executed") is True

    # 4) execution report three elements (SC-003 second half)
    report = json.loads(proc.stdout)
    assert report["executed"] and report["executed"][0]["outcome"] == "ok"
    assert any(a["change"] == "deleted" for a in report["artifacts"])
    assert report["modifyPaths"], "modification paths must be listed"
    assert report["failures"] == []


def test_us3_dismissal_keeps_material_and_state_dismissed(tmp_path):
    ws = assemble(tmp_path)
    run_engine(["--action", "collect", "--workspace-root", str(ws)], cwd=ws)
    finding = record_stale_finding(ws)
    material = ws / finding["target"]
    plan = make_plan(ws, finding, confirmed=True)
    plan.write_text(json.dumps({
        "created": "x", "confirmed": True,
        "items": [{"findingId": finding["id"], "disposition": "dismiss",
                   "target": finding["target"]}],
    }), encoding="utf-8")
    proc = run_engine(["--action", "apply", "--plan", str(plan),
                       "--workspace-root", str(ws)], cwd=ws)
    assert proc.returncode == 0
    assert material.is_file(), "dismissal never deletes anything"
    store = {f["id"]: f for f in json.loads((ws / STORE_REL).read_text(encoding="utf-8"))["findings"]}
    assert store[finding["id"]]["state"] == "resolved"
