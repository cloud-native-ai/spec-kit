"""Integration: house-keeping flow primitives on a temp target project.

This does not execute the chat orchestration; it exercises the two read-only
inventory scripts and the retention engine exactly as the skill invokes them,
on a target that is not the framework repo.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "external" / "sdd-house-keeping"
INVENTORY = SKILL / "scripts" / "mechanism-inventory.py"
LOGICAL = SKILL / "scripts" / "logical-framework.py"
RETENTION = ROOT / "scripts" / "python" / "record-retention.py"
OLD = "2026-09-01T00:00:00Z"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], capture_output=True,
                          text=True, timeout=120)


def _json(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), proc.stderr
    return json.loads(proc.stdout)


def _target(tmp_path: Path) -> Path:
    memory = tmp_path / ".specify" / "memory"
    memory.mkdir(parents=True)
    (memory / "constitution.md").write_text("# Constitution\n", encoding="utf-8")
    (memory / "features.md").write_text("# Features\n", encoding="utf-8")
    (memory / "features").mkdir()
    (tmp_path / ".specify" / "skills").mkdir()
    (tmp_path / ".specify" / "templates").mkdir()
    (tmp_path / ".specify" / "instructions.md").write_text(
        "# Instructions\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "index.md").write_text("# Docs\n", encoding="utf-8")
    return tmp_path


def test_inventory_scripts_run_read_only_on_target(tmp_path: Path) -> None:
    target = _target(tmp_path)
    before = {p: p.stat().st_mtime_ns for p in target.rglob("*") if p.is_file()}
    inv = _run(str(INVENTORY), "--project", str(target), "--json")
    assert inv.returncode == 0, inv.stderr
    payload = _json(inv)
    assert payload["grade"] in ("absent", "degraded", "partial", "complete")
    logic = _run(str(LOGICAL), "--project", str(target), "--json")
    assert logic.returncode in (0, 1), logic.stderr
    assert isinstance(_json(logic), dict)
    after = {p: p.stat().st_mtime_ns for p in target.rglob("*") if p.is_file()}
    assert before == after, "inventory scripts must not write to the target"


def test_retention_engine_flow_primitives_on_target(tmp_path: Path) -> None:
    target = _target(tmp_path)
    records = target / ".specify" / "memory" / "exec-quant" / "records"
    records.mkdir(parents=True)
    (records / "old.json").write_text(json.dumps({
        "kind": "speckit.exec-quant",
        "schema_version": 2,
        "unit_id": "/speckit.plan",
        "unit_type": "command",
        "run_id": "r-old",
        "collected_at": OLD,
        "quality": {"tokens": "not_evaluated"},
    }) + "\n", encoding="utf-8")
    feedback = target / ".specify" / "memory" / "feedback"
    feedback.mkdir(parents=True)
    (feedback / "20260901T000000Z-speckit-plan.md").write_text(f"""---
id: "20260901T000000Z-speckit-plan"
unit_id: "/speckit.plan"
unit_type: "command"
run_id: "r-old"
disposition: "processed"
created: "{OLD}"
summary: "done"
disposition_reason: "consumed"
---

## Review
done
""", encoding="utf-8")

    scan = _run(str(RETENTION), "--action", "scan", "--workspace-root",
                str(target))
    assert scan.returncode == 0, scan.stderr
    assert _json(scan)["stores"]["exec-quant"]["blocked"] == 1
    distill = _run(str(RETENTION), "--action", "distill", "--workspace-root",
                   str(target))
    assert distill.returncode == 0, distill.stderr
    plan = _run(str(RETENTION), "--action", "plan", "--workspace-root",
                str(target))
    assert plan.returncode == 0, plan.stderr
    plan_path = Path(_json(plan)["plan"])
    node = json.loads(plan_path.read_text(encoding="utf-8"))
    node["confirmed"] = True
    plan_path.write_text(json.dumps(node, indent=2) + "\n", encoding="utf-8")
    apply = _run(str(RETENTION), "--action", "apply", "--workspace-root",
                 str(target), "--plan", str(plan_path), "--allow-unversioned")
    assert apply.returncode == 0, apply.stderr
    payload = _json(apply)
    assert payload["removed"] == 2
    assert payload["conservation_ok"] is True
    assert not (records / "old.json").exists()
    assert not (feedback / "20260901T000000Z-speckit-plan.md").exists()
    assert (target / ".specify" / "memory" / "retention" / "ledger"
            ).is_dir()
