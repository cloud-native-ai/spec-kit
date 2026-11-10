"""Integration tests for the real 074 split → merge-back → seal round (Feature 099, P8).

Contract: ``.specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md``
Clauses:  C-043 — the round's adjudication is reproducible: the merge manifest, the
          seal receipt or refusal list and the front-end status agree; a rerun in
          the blocked state MUST reproduce the same list, never a different verdict.

Scope: read-only. The test drives ``merge-plan`` (a zero-write action) against the
real ``.specify/specs/074-goal-team-sdd-unification/`` tree and reads the round's
recorded evidence. It MUST NOT write into the 074 tree; the git-status comparison
below turns a write into a red assertion.

Evidence the round produced (captured by T039/T041/T043):

* ``test-evidence/074-merge-plan-before.json`` — the pre-fix plan, whose
  ``conflicts[]`` names the ``factory-doc-ref-ambiguous`` class 36 times.
* ``test-evidence/074-merge-plan-after.json`` — the post-fix plan (0 open conflicts).
* ``test-evidence/074-round-20261110.txt`` — the pre-fix round's adjudication,
  kept unchanged as the before snapshot of the P8b rerun.
* ``test-evidence/074-round-rerun-20261111.txt`` — the rerun on the repaired
  engine: two seal runs, the same refusal list, the FR-027 floor covered.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
EVIDENCE = REPO_ROOT / ".specify" / "specs" / "099-speckit-seal" / "test-evidence"
PARENT = REPO_ROOT / ".specify" / "specs" / "074-goal-team-sdd-unification"
SLICE_A = "074a-authorized-routing"
SLICE_B = "074b-nested-governance"
ROUND_EVIDENCE = EVIDENCE / "074-round-rerun-20261111.txt"

#: The declared mappings the round MUST honour (074a / 074b `## Parent Mapping`).
DECLARED_STR_MAPPINGS = {
    (SLICE_A, "STR-010"): "STR-011",
    (SLICE_B, "STR-004"): "STR-007",
    (SLICE_B, "STR-005"): "STR-008",
    (SLICE_B, "STR-006"): "STR-009",
    (SLICE_B, "STR-007"): "STR-010",
}


def _git_status_074() -> str:
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain", "--", str(PARENT)],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.returncode == 0, f"git status failed: {proc.stderr[-400:]!r}"
    return proc.stdout


def _run_plan() -> tuple[subprocess.CompletedProcess, dict]:
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "merge-plan",
         "--spec-dir", str(PARENT), "--repo", str(REPO_ROOT), "--json"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, encoding="utf-8",
        check=False,
    )
    assert proc.stdout.strip(), (
        f"expected a stdout payload; exit={proc.returncode} "
        f"stderr={proc.stderr[-800:]!r}"
    )
    return proc, json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# The live, read-only merge-plan face
# ---------------------------------------------------------------------------


def test_live_plan_identifies_both_slices_from_the_split_record():
    proc, payload = _run_plan()
    plan = payload["plan"]
    assert proc.returncode == 0, (
        "the settled round must leave a conflict-free plan; exit=%d payload=%r"
        % (proc.returncode, payload.get("conditions"))
    )
    slices = plan["slices"]
    assert [item["slug"] for item in slices] == [SLICE_A, SLICE_B], (
        "C-012: the split record's declared order (074a → 074b) decides the order"
    )
    assert [item["order"] for item in slices] == [1, 2]
    assert {item["order_basis"] for item in slices} == {"split-record"}, (
        "C-012: the order MUST be taken from `.specify/state/074-*.md` § 拆分记录"
    )
    assert plan["checks"]["open_conflicts"] == 0, (
        "the round's disposed conflicts must not reappear: %r"
        % payload.get("conditions")
    )


def test_declared_str_mappings_are_honoured_in_the_id_maps():
    _proc, payload = _run_plan()
    str_entries = {
        (entry["slice"], entry["slice_id"]): entry["parent_id"]
        for entry in payload["plan"]["id_maps"]["STR"]
    }
    for key, parent_id in DECLARED_STR_MAPPINGS.items():
        assert str_entries.get(key) == parent_id, (
            "C-016: the slice's declared `## Parent Mapping` decides the target; "
            f"{key} must map to {parent_id}, got {str_entries.get(key)!r}"
        )


def test_the_round_named_the_factory_doc_conflict_class_it_disposed():
    before_path = EVIDENCE / "074-merge-plan-before.json"
    assert before_path.is_file(), (
        "T039's pre-fix capture is part of the round record; it is what names the "
        "conflict classes before disposal"
    )
    before = json.loads(before_path.read_text(encoding="utf-8"))
    conflicts = before["plan"]["conflicts"]
    ambiguous = [c for c in conflicts if c["code"] == "factory-doc-ref-ambiguous"]
    assert len(ambiguous) == 36, (
        "the pre-fix plan names 36 factory-doc-ref-ambiguous records "
        "(18 source references × source/mirror scan); got %d" % len(ambiguous)
    )
    units = {c["unit"] for c in ambiguous}
    assert {"STR-004", "STR-005", "STR-006", "STR-007"} <= units, (
        "the two same-number groups the round disposes MUST be named by id: %r" % units
    )


# ---------------------------------------------------------------------------
# Blocked-state rerun consistency (C-043)
# ---------------------------------------------------------------------------


def _adjudication_blocks(text: str) -> list[dict]:
    """The two recorded seal runs, split on the round's own run separators."""
    blocks = []
    current = None
    for line in text.splitlines():
        if line.startswith("=== RUN "):
            if current is not None:
                blocks.append(current)
            current = {"header": line, "lines": []}
            continue
        if current is not None:
            current["lines"].append(line)
    if current is not None:
        blocks.append(current)
    return blocks


def test_blocked_state_rerun_is_identical_and_names_the_same_verdict():
    assert ROUND_EVIDENCE.is_file(), (
        "the blocked round's adjudication is carried by "
        "`test-evidence/074-round-rerun-20261111.txt` (P8b rerun; the pre-fix "
        "round stays as `074-round-20261110.txt`)"
    )
    blocks = _adjudication_blocks(ROUND_EVIDENCE.read_text(encoding="utf-8"))
    assert len(blocks) == 2, (
        "T043 records exactly two seal runs (verdict + reproducibility rerun); "
        "found %d" % len(blocks)
    )
    first = [line for line in blocks[0]["lines"] if line.strip()]
    second = [line for line in blocks[1]["lines"] if line.strip()]
    assert first == second, (
        "C-043: a rerun in the blocked state MUST reproduce the same refusal list"
    )
    body = "\n".join(first)
    assert "closure-input-defect" in body, (
        "the round's recorded refusal names the closure input defect it found"
    )
    for item in ("FR-027(a)", "FR-027(b)", "FR-027(c)", "FR-027(d)", "FR-027(e)"):
        assert item in body, (
            "SC-006: the refusal list covers the FR-027 floor item by item; "
            f"{item} is not named"
        )


# ---------------------------------------------------------------------------
# Read-only: the test never rewrites the 074 tree
# ---------------------------------------------------------------------------


def test_the_round_probe_writes_nothing_into_the_074_tree():
    before = _git_status_074()
    _run_plan()
    after = _git_status_074()
    assert before == after, (
        "T042: this test MUST NOT rewrite the 074 tree; git status changed from "
        f"{before!r} to {after!r}"
    )
