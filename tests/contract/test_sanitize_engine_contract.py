"""Contract tests for sanitize-utils.py engine CLI (requirement 045 / Feature 047).

Pins contracts/sanitize-engine.md: action surface (exactly collect/record/status/apply),
exit-code table (0 ok / 1 CliError / 2 verification failure), JSON output envelope,
write confinement (collect writes only the store), and the apply confirmation gate.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "sanitize-utils.py"
STORE_REL = Path(".specify") / "memory" / "sanitize" / "findings.json"
PLAN_REL = Path(".specify") / "memory" / "sanitize" / "cleanup-plan.json"


def run_engine(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        cwd=str(cwd), capture_output=True, text=True, timeout=120,
    )


def out_json(proc: subprocess.CompletedProcess) -> dict:
    return json.loads(proc.stdout)


def make_finding(**overrides) -> dict:
    import hashlib
    base = {
        "category": "stale-residue",
        "target": ".specify/memory/todo/example.md",
        "severity": "high",
        "summary": "claims unlanded work that commit abc1234 merged",
        "evidenceRefs": [{"kind": "commit", "ref": "abc1234"}],
        "detection": "semantic",
        "disposition": "delete",
        "reversibility": "irreversible",
        "state": "pending",
    }
    base.update(overrides)
    if "id" not in overrides:
        base["id"] = hashlib.sha1(f"{base['category']}|{base['target']}".encode()).hexdigest()[:12]
    return base


# --- action surface & exit codes -----------------------------------------------

def test_unknown_action_exits_1_with_json_error(tmp_path):
    proc = run_engine(["--action", "bogus", "--workspace-root", str(tmp_path)], cwd=tmp_path)
    assert proc.returncode == 1
    assert "error" in out_json(proc)


def test_missing_action_exits_1(tmp_path):
    proc = run_engine(["--workspace-root", str(tmp_path)], cwd=tmp_path)
    assert proc.returncode == 1


def test_collect_on_empty_workspace_exits_0(tmp_path):
    proc = run_engine(["--action", "collect", "--workspace-root", str(tmp_path)], cwd=tmp_path)
    assert proc.returncode == 0
    payload = out_json(proc)
    assert payload["ok"] is True
    assert payload["semanticCandidates"] == []


def test_status_exits_0(tmp_path):
    run_engine(["--action", "collect", "--workspace-root", str(tmp_path)], cwd=tmp_path)
    proc = run_engine(["--action", "status", "--workspace-root", str(tmp_path)], cwd=tmp_path)
    assert proc.returncode == 0
    assert out_json(proc)["ok"] is True


def test_record_without_file_exits_1(tmp_path):
    proc = run_engine(["--action", "record", "--workspace-root", str(tmp_path)], cwd=tmp_path)
    assert proc.returncode == 1


def test_apply_with_missing_plan_file_exits_1(tmp_path):
    proc = run_engine(
        ["--action", "apply", "--plan", str(tmp_path / "nope.json"), "--workspace-root", str(tmp_path)],
        cwd=tmp_path,
    )
    assert proc.returncode == 1


# --- write confinement ----------------------------------------------------------

def test_collect_creates_store_and_writes_nothing_else(tmp_path):
    before = {p: p.stat().st_mtime_ns for p in tmp_path.rglob("*") if p.is_file()}
    run_engine(["--action", "collect", "--workspace-root", str(tmp_path)], cwd=tmp_path)
    store = tmp_path / STORE_REL
    assert store.is_file(), "collect must persist the findings store"
    after = {p: p.stat().st_mtime_ns for p in tmp_path.rglob("*") if p.is_file() and p != store}
    assert after == before, "collect must not modify any file other than the store"
    assert not list((tmp_path / ".specify" / "memory" / "sanitize").glob("*.part")), "no .part residue"


def test_status_is_zero_write(tmp_path):
    run_engine(["--action", "collect", "--workspace-root", str(tmp_path)], cwd=tmp_path)
    store = tmp_path / STORE_REL
    before = (store.read_bytes(), store.stat().st_mtime_ns)
    run_engine(["--action", "status", "--workspace-root", str(tmp_path)], cwd=tmp_path)
    after = (store.read_bytes(), store.stat().st_mtime_ns)
    assert before == after


# --- record: schema gate (all-or-nothing) ---------------------------------------

def test_record_with_schema_violation_exits_2_and_writes_nothing(tmp_path):
    run_engine(["--action", "collect", "--workspace-root", str(tmp_path)], cwd=tmp_path)
    store = tmp_path / STORE_REL
    before = store.read_text(encoding="utf-8")
    bad = make_finding(id="deadbeef0000")  # C-1: id must equal stable_id(category|target)
    verdicts = tmp_path / "verdicts.json"
    verdicts.write_text(json.dumps({"findings": [bad]}), encoding="utf-8")
    proc = run_engine(
        ["--action", "record", "--file", str(verdicts), "--workspace-root", str(tmp_path)],
        cwd=tmp_path,
    )
    assert proc.returncode == 2
    assert store.read_text(encoding="utf-8") == before, "all-or-nothing: no partial merge"


def test_record_accepts_valid_semantic_finding(tmp_path):
    run_engine(["--action", "collect", "--workspace-root", str(tmp_path)], cwd=tmp_path)
    verdicts = tmp_path / "verdicts.json"
    verdicts.write_text(json.dumps({"findings": [make_finding()]}), encoding="utf-8")
    proc = run_engine(
        ["--action", "record", "--file", str(verdicts), "--workspace-root", str(tmp_path)],
        cwd=tmp_path,
    )
    assert proc.returncode == 0
    store = json.loads((tmp_path / STORE_REL).read_text(encoding="utf-8"))
    assert len(store["findings"]) == 1
    assert store["findings"][0]["state"] == "pending"


# --- apply: confirmation gate ----------------------------------------------------

def test_apply_rejects_unknown_finding_exits_2(tmp_path):
    plan = tmp_path / "cleanup-plan.json"
    plan.parent.mkdir(parents=True, exist_ok=True)
    plan.write_text(json.dumps({
        "created": "2026-08-20T00:00:00Z", "confirmed": True,
        "items": [{"findingId": "nope", "disposition": "delete", "target": ".specify/memory/todo/x.md"}],
    }), encoding="utf-8")
    proc = run_engine(
        ["--action", "apply", "--plan", str(plan), "--workspace-root", str(tmp_path)],
        cwd=tmp_path,
    )
    assert proc.returncode == 2


def test_apply_rejects_disposition_mismatch_exits_2(tmp_path):
    finding = make_finding()  # suggested disposition: delete
    todo = tmp_path / ".specify" / "memory" / "todo"
    todo.mkdir(parents=True, exist_ok=True)
    (todo / "example.md").write_text("x\n", encoding="utf-8")
    store_path = tmp_path / STORE_REL
    store_path.parent.mkdir(parents=True, exist_ok=True)
    store_path.write_text(json.dumps({"version": 1, "updated": "x", "findings": [finding]}), encoding="utf-8")
    plan = tmp_path / "cleanup-plan.json"
    plan.write_text(json.dumps({
        "created": "x", "confirmed": True,
        "items": [{"findingId": finding["id"], "disposition": "archive", "target": finding["target"]}],
    }), encoding="utf-8")
    proc = run_engine(
        ["--action", "apply", "--plan", str(plan), "--workspace-root", str(tmp_path)],
        cwd=tmp_path,
    )
    assert proc.returncode == 2
    assert (todo / "example.md").is_file(), "rejected plan must leave the material untouched"


def test_apply_repair_is_state_only(tmp_path):
    finding = make_finding(
        category="dead-reference", target=".specify/memory/todo/example.md#scripts/x.py",
        detection="programmatic", disposition="repair", severity="medium",
        evidenceRefs=[{"kind": "path", "ref": "scripts/x.py"}],
    )
    todo = tmp_path / ".specify" / "memory" / "todo"
    todo.mkdir(parents=True, exist_ok=True)
    (todo / "example.md").write_text("x\n", encoding="utf-8")
    store_path = tmp_path / STORE_REL
    store_path.parent.mkdir(parents=True, exist_ok=True)
    store_path.write_text(json.dumps({"version": 1, "updated": "x", "findings": [finding]}), encoding="utf-8")
    plan = tmp_path / "cleanup-plan.json"
    plan.write_text(json.dumps({
        "created": "x", "confirmed": True,
        "items": [{"findingId": finding["id"], "disposition": "repair", "target": finding["target"]}],
    }), encoding="utf-8")
    proc = run_engine(
        ["--action", "apply", "--plan", str(plan), "--workspace-root", str(tmp_path)],
        cwd=tmp_path,
    )
    assert proc.returncode == 0
    assert (todo / "example.md").read_text(encoding="utf-8") == "x\n", "repair is state-only; the agent edits content"
    store = json.loads((tmp_path / STORE_REL).read_text(encoding="utf-8"))
    assert store["findings"][0]["state"] == "resolved"


def test_apply_archive_moves_to_archive_root(tmp_path):
    finding = make_finding(
        category="redundant", target=".specify/memory/draft/old.md",
        severity="low", summary="superseded by /speckit.docs rewrite",
        evidenceRefs=[{"kind": "path", "ref": ".specify/memory/todo/new.md"}],
        detection="semantic", disposition="archive",
    )
    draft = tmp_path / ".specify" / "memory" / "draft"
    draft.mkdir(parents=True, exist_ok=True)
    (draft / "old.md").write_text("old\n", encoding="utf-8")
    store_path = tmp_path / STORE_REL
    store_path.parent.mkdir(parents=True, exist_ok=True)
    store_path.write_text(json.dumps({"version": 1, "updated": "x", "findings": [finding]}), encoding="utf-8")
    plan = tmp_path / "cleanup-plan.json"
    plan.write_text(json.dumps({
        "created": "x", "confirmed": True,
        "items": [{"findingId": finding["id"], "disposition": "archive", "target": finding["target"]}],
    }), encoding="utf-8")
    proc = run_engine(
        ["--action", "apply", "--plan", str(plan), "--workspace-root", str(tmp_path)],
        cwd=tmp_path,
    )
    assert proc.returncode == 0
    assert not (draft / "old.md").exists(), "archived material leaves its origin"
    archived = tmp_path / ".specify" / "archive" / "memory" / "draft" / "old.md"
    assert archived.is_file() and archived.read_text(encoding="utf-8") == "old\n"
    report = out_json(proc)
    assert any(a["change"] == "archived" for a in report["artifacts"])


def _make_plan(tmp_path, confirmed: bool) -> Path:
    finding = make_finding()
    todo = tmp_path / ".specify" / "memory" / "todo"
    todo.mkdir(parents=True, exist_ok=True)
    (todo / "example.md").write_text("---\nstatus: parked\n---\nclaims unlanded\n", encoding="utf-8")
    verdicts = tmp_path / "verdicts.json"
    verdicts.write_text(json.dumps({"findings": [finding]}), encoding="utf-8")
    run_engine(["--action", "record", "--file", str(verdicts), "--workspace-root", str(tmp_path)], cwd=tmp_path)
    plan = tmp_path / PLAN_REL
    plan.parent.mkdir(parents=True, exist_ok=True)
    plan.write_text(json.dumps({
        "created": "2026-08-20T00:00:00Z",
        "confirmed": confirmed,
        "items": [{"findingId": finding["id"], "disposition": "delete", "target": finding["target"]}],
    }), encoding="utf-8")
    return plan


def test_apply_rejects_unconfirmed_plan_exits_2_zero_execution(tmp_path):
    plan = _make_plan(tmp_path, confirmed=False)
    material = tmp_path / ".specify" / "memory" / "todo" / "example.md"
    proc = run_engine(
        ["--action", "apply", "--plan", str(plan), "--workspace-root", str(tmp_path)],
        cwd=tmp_path,
    )
    assert proc.returncode == 2
    assert material.is_file(), "no deletion before user confirmation"


def test_apply_rejects_out_of_whitelist_target_exits_2(tmp_path):
    finding = make_finding(
        category="dead-reference", target="src/leak.py", detection="programmatic",
        disposition="delete", severity="medium", evidenceRefs=[{"kind": "path", "ref": "x"}],
    )
    # register the finding via record (record validates target whitelist too, so
    # bypass via direct store write is not possible; instead test apply on a plan
    # whose target escapes the roots even though the finding was hand-inserted)
    store_path = tmp_path / STORE_REL
    store_path.parent.mkdir(parents=True, exist_ok=True)
    store_path.write_text(json.dumps({"version": 1, "updated": "2026-08-20T00:00:00Z", "findings": [finding]}), encoding="utf-8")
    victim = tmp_path / "src" / "leak.py"
    victim.parent.mkdir(parents=True, exist_ok=True)
    victim.write_text("print('user code')\n", encoding="utf-8")
    plan = tmp_path / PLAN_REL
    plan.write_text(json.dumps({
        "created": "2026-08-20T00:00:00Z", "confirmed": True,
        "items": [{"findingId": finding["id"], "disposition": "delete", "target": "src/leak.py"}],
    }), encoding="utf-8")
    proc = run_engine(
        ["--action", "apply", "--plan", str(plan), "--workspace-root", str(tmp_path)],
        cwd=tmp_path,
    )
    assert proc.returncode == 2
    assert victim.is_file(), "user code must never be deleted"


def test_apply_executes_confirmed_delete_and_updates_state(tmp_path):
    plan = _make_plan(tmp_path, confirmed=True)
    material = tmp_path / ".specify" / "memory" / "todo" / "example.md"
    proc = run_engine(
        ["--action", "apply", "--plan", str(plan), "--workspace-root", str(tmp_path)],
        cwd=tmp_path,
    )
    assert proc.returncode == 0
    assert not material.exists(), "confirmed delete must remove the material"
    report = out_json(proc)
    assert report["executed"][0]["outcome"] == "ok"
    store = json.loads((tmp_path / STORE_REL).read_text(encoding="utf-8"))
    assert store["findings"][0]["state"] == "resolved"


# --- CLI examples pinned for quickstart.md (contract sanitize-engine §6) --------

def test_quickstart_cli_grammar_matches_engine():
    """The exact flags used in quickstart.md must remain valid engine syntax."""
    for argv in (
        ["--action", "collect", "--workspace-root", ".", "--format", "json"],
        ["--action", "record", "--file", "/tmp/sanitize-verdicts.json", "--workspace-root", ".", "--format", "json"],
        ["--action", "status", "--workspace-root", ".", "--format", "json"],
        ["--action", "apply", "--plan", ".specify/memory/sanitize/cleanup-plan.json", "--workspace-root", ".", "--format", "json"],
    ):
        proc = subprocess.run(
            [sys.executable, str(ENGINE), "--action", argv[1], "--help"],
            capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0
    source = ENGINE.read_text(encoding="utf-8")
    for flag in ("--workspace-root", "--format", "--file", "--plan", "--roots"):
        assert flag in source, f"flag {flag} disappeared from the engine"
