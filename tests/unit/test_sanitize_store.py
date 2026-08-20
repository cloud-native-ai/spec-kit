"""Unit tests for the sanitize findings store (requirement 045 / Feature 047).

Pins contracts/sanitize-findings.md: stable ID, atomic persistence + corruption
rebuild, schema validation C-1..C-7, merge semantics C-8..C-13, and the
partial-scan guard C-14.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))

from script_api import sanitize_utils as su  # noqa: E402

RUN_TS = "2026-08-20T00:00:00Z"


def sid(category: str, target: str) -> str:
    return hashlib.sha1(f"{category}|{target}".encode()).hexdigest()[:12]


def finding(**overrides) -> dict:
    base = {
        "category": "dead-reference",
        "target": ".specify/memory/todo/x.md",
        "severity": "medium",
        "summary": "references missing scripts/python/nope.py",
        "evidenceRefs": [{"kind": "path", "ref": "scripts/python/nope.py"}],
        "detection": "programmatic",
        "disposition": "repair",
        "reversibility": "reversible",
        "state": "pending",
    }
    base.update(overrides)
    if "id" not in overrides:
        base["id"] = sid(base["category"], base["target"])
    return base


def init_store(tmp_path: Path, findings: list[dict]) -> Path:
    store_path = tmp_path / ".specify" / "memory" / "sanitize" / "findings.json"
    store_path.parent.mkdir(parents=True, exist_ok=True)
    store_path.write_text(json.dumps({"version": 1, "updated": RUN_TS, "findings": findings}), encoding="utf-8")
    return store_path


# --- stable id -------------------------------------------------------------------

def test_stable_id_is_sha1_of_category_and_target():
    assert su.stable_id("dead-reference", "docs/a.md") == hashlib.sha1(b"dead-reference|docs/a.md").hexdigest()[:12]


# --- load / save ------------------------------------------------------------------

def test_load_store_missing_returns_empty_with_note(tmp_path):
    store, notes = su.load_store(tmp_path)
    assert store["findings"] == []
    assert notes == []


def test_load_store_corrupt_rebuilds_empty_with_note(tmp_path):
    store_path = init_store(tmp_path, [])
    store_path.write_text("{not json", encoding="utf-8")
    store, notes = su.load_store(tmp_path)
    assert store["findings"] == []
    assert any("corrupt" in n or "rebuilt" in n for n in notes)


def test_save_store_atomic_no_part_residue(tmp_path):
    su.save_store(tmp_path, {"version": 1, "updated": RUN_TS, "findings": []})
    store_path = tmp_path / ".specify" / "memory" / "sanitize" / "findings.json"
    assert store_path.is_file()
    assert not list(store_path.parent.glob("*.part"))


# --- schema validation C-1..C-7 ----------------------------------------------------

def make_ws(tmp_path):
    (tmp_path / ".specify" / "memory" / "todo").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs").mkdir(exist_ok=True)
    return tmp_path


def test_validate_rejects_wrong_id(tmp_path):
    errs = su.validate_finding(finding(id="000000000000"), tmp_path)
    assert any("id" in e for e in errs)


def test_validate_rejects_bad_enums(tmp_path):
    errs = su.validate_finding(finding(category="bogus"), tmp_path)
    assert errs
    errs = su.validate_finding(finding(severity="extreme"), tmp_path)
    assert errs
    errs = su.validate_finding(finding(disposition="nuke", reversibility="reversible"), tmp_path)
    assert errs


def test_validate_rejects_semantic_without_commit_or_path_evidence(tmp_path):
    f = finding(
        category="stale-residue", detection="semantic", disposition="delete",
        reversibility="irreversible", severity="high",
        evidenceRefs=[{"kind": "output", "ref": "whatever"}],
    )
    errs = su.validate_finding(f, tmp_path)
    assert any("evidence" in e for e in errs)


def test_validate_rejects_disposition_reversibility_mismatch(tmp_path):
    errs = su.validate_finding(finding(disposition="delete", reversibility="reversible"), tmp_path)
    assert any("revers" in e for e in errs)


def test_validate_rejects_non_pending_state_on_write(tmp_path):
    errs = su.validate_finding(finding(state="resolved"), tmp_path)
    assert any("pending" in e for e in errs)


def test_validate_requires_delegate_command_in_summary(tmp_path):
    errs = su.validate_finding(finding(disposition="delegate", summary="go away"), tmp_path)
    assert any("delegate" in e for e in errs)


def test_validate_rejects_target_outside_material_roots(tmp_path):
    errs = su.validate_finding(finding(target="src/app.py"), tmp_path)
    assert any("target" in e for e in errs)


def test_validate_accepts_minimal_valid_finding(tmp_path):
    assert su.validate_finding(finding(), tmp_path) == []


# --- merge semantics C-8..C-13 ------------------------------------------------------

DET = {"dead-reference", "index-inconsistency", "broken-symlink", "mirror-drift"}
SEM = {"stale-residue", "redundant"}


def merge(store_findings, new_findings, scanned=DET):
    store = {"version": 1, "updated": RUN_TS, "findings": [dict(f) for f in store_findings]}
    stats = su.merge_findings(store, [dict(f) for f in new_findings], RUN_TS, scanned)
    return store, stats


def test_c8_new_finding_appended_pending():
    store, stats = merge([], [finding()])
    assert len(store["findings"]) == 1
    assert store["findings"][0]["state"] == "pending"
    assert stats["added"] == 1


def test_c9_pending_redetect_refreshes_not_duplicates():
    existing = finding()
    store, stats = merge([existing], [finding()])
    assert len(store["findings"]) == 1
    assert stats["refreshed"] == 1
    assert store["findings"][0]["lastSeenRun"] == RUN_TS


def test_c10_pending_not_redetected_auto_resolves():
    existing = finding()
    store, stats = merge([existing], [])
    assert store["findings"][0]["state"] == "resolved"
    assert store["findings"][0]["resolvedAt"] == RUN_TS
    assert stats["auto_resolved"] == 1


def test_c10_not_redetected_note_recorded():
    existing = finding()
    store, _ = merge([existing], [])
    assert any("not re-detected" in n for n in store["findings"][0]["notes"])


def test_c11_resolved_redetect_reopens():
    existing = finding(state="resolved", resolvedAt="2026-08-01T00:00:00Z")
    store, stats = merge([existing], [finding()])
    assert store["findings"][0]["state"] == "pending"
    assert stats["reopened"] == 1


def test_c12_dismissed_redetect_stays_dismissed():
    existing = finding(state="dismissed")
    store, stats = merge([existing], [finding()])
    assert store["findings"][0]["state"] == "dismissed"
    assert stats["kept"] == 1


def test_c13_terminal_untouched_keeps_history():
    existing = finding(state="resolved", resolvedAt="2026-08-01T00:00:00Z")
    store, _ = merge([existing], [])
    assert store["findings"][0]["state"] == "resolved"


def test_c14_partial_scan_does_not_auto_resolve_unscanned_categories():
    existing = finding(category="stale-residue", detection="semantic", disposition="delete",
                       reversibility="irreversible", severity="high",
                       evidenceRefs=[{"kind": "commit", "ref": "abc"}])
    store, stats = merge([existing], [], scanned=DET)  # semantic category not scanned
    assert store["findings"][0]["state"] == "pending"
    assert stats["auto_resolved"] == 0


# --- roots enumeration & whitelist ---------------------------------------------------

def test_probe_roots_missing_root_is_empty_not_error(tmp_path):
    roots = su.probe_roots(tmp_path)
    assert all("exists" in r for r in roots)
    assert not any(r["exists"] for r in roots)


def test_is_material_target_whitelist(tmp_path):
    make_ws(tmp_path)
    assert su.is_material_target(tmp_path, ".specify/memory/todo/a.md")
    assert su.is_material_target(tmp_path, "docs/reference/x.md")
    assert not su.is_material_target(tmp_path, "src/app.py")
    assert not su.is_material_target(tmp_path, "tests/unit/test_x.py")
    assert not su.is_material_target(tmp_path, ".git/config")
