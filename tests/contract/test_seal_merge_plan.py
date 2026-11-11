"""Contract tests for the seal engine's ``merge-plan`` action (Feature 099, work package P3).

Contract: ``.specify/specs/099-speckit-seal/contracts/merge-back.contract.md``
Clauses:  C-011 … C-018 (the plan face) — the two-condition slice set, the declared
          slice order with its trace, the closed 15-candidate universe and its
          per-artifact action classification, directory candidates as file-level
          units (same-name three states), dated-record pointer inclusions (never a
          copy), the token→registry binding check, the ID-family maps and the
          conflict records that block when open.

Fixture trees: ``tests/fixtures/seal/`` — ``split-pair/`` (clean two-slice merge),
``conflict-injections/`` (every injected conflict class) and ``factory-doc/``
(a framework document citing a slice-local id).

Red-first: this file landed before the ``merge-plan`` body existed; the red reading
lives in ``.specify/specs/099-speckit-seal/notes/red-first-evidence.md``.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "seal"
ARCHIVE_FIXTURES = REPO_ROOT / "tests" / "fixtures" / "seal-archive"

PARENT = "099-fixture-parent"
ALPHA = "099a-fixture-alpha"
BETA = "099b-fixture-beta"
CONFLICT_ALPHA = "099a-fixture-conflict"
CONFLICT_BETA = "099b-fixture-conflict"

ARCHIVE_PARENT = "100-fixture-parent"
ARCHIVE_ALPHA = "100a-fixture-alpha"
ARCHIVE_BETA = "100b-fixture-beta"

#: C-013: the candidate universe is closed at exactly these fifteen names.
CANDIDATES = {
    "requirements.md", "plan.md", "tasks.md", "data-model.md", "contracts",
    "research.md", "quickstart.md", "feature-ref.md", "verification.md",
    "review.md", "code-review.md", "checklists", "checkpoints", "test-evidence",
    "notes",
}
ACTIONS = {"merge", "create", "keep", "not-applicable"}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _copy_fixture(name: str, tmp_path: Path) -> Path:
    """Copy one fixture root into the test's tmp tree (the engine runs read-only)."""
    source = FIXTURES / name
    assert source.is_dir(), (
        f"fixture tree missing: {source} — this is the expected red-first reading "
        "for T018/T019 before the fixture work package lands"
    )
    target = tmp_path / name.replace("/", "-")
    shutil.copytree(source, target)
    return target


def _copy_archive_fixture(tmp_path: Path) -> Path:
    """Copy the archived-pair fixture into the test's tmp tree."""
    source = ARCHIVE_FIXTURES / "archived-pair"
    assert source.is_dir(), (
        f"fixture tree missing: {source} — T007 creates it before the red-first run"
    )
    target = tmp_path / "archived-pair"
    shutil.copytree(source, target)
    return target


def _run_plan(repo: Path, spec: str = PARENT):
    spec_dir = repo / ".specify" / "specs" / spec
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "merge-plan",
         "--spec-dir", str(spec_dir), "--repo", str(repo), "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.stdout.strip(), (
        f"expected a stdout payload; exit={proc.returncode} stderr={proc.stderr[-800:]!r}"
    )
    return proc, json.loads(proc.stdout)


def _plan(repo: Path, spec: str = PARENT) -> dict:
    return _run_plan(repo, spec)[1]["plan"]


def _artifacts(plan: dict) -> dict:
    return {row["name"]: row for row in plan["artifacts"]}


def _conflicts(plan: dict, code=None) -> list:
    return [c for c in plan["conflicts"] if code is None or c.get("code") == code]


def _entries(plan: dict, family: str) -> list:
    return plan["id_maps"].get(family, [])


def _entry(entries: list, slice_slug: str, slice_id: str) -> dict:
    found = [e for e in entries
             if e["slice"] == slice_slug and e["slice_id"] == slice_id]
    assert len(found) == 1, (
        f"expected exactly one id_map entry for {slice_slug} {slice_id}; "
        f"got {found!r}"
    )
    return found[0]


def _snapshot(root: Path) -> dict:
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*")) if p.is_file()
    }


# ---------------------------------------------------------------------------
# C-011 — the slice set is decided by two conditions at once
# ---------------------------------------------------------------------------

def test_c011_slice_set_uses_both_conditions(tmp_path):
    plan = _plan(_copy_fixture("split-pair", tmp_path))
    assert [s["slug"] for s in plan["slices"]] == [ALPHA, BETA]
    assert [s["order"] for s in plan["slices"]] == [1, 2]
    assert plan["checks"]["slice_conditions"] == ["name-family", "parent-declaration"]
    assert plan["checks"]["slice_count"] == 2
    assert not _conflicts(plan, "slice-candidate-unconfirmed"), (
        "C-011: a clean split pair yields no unconfirmed-candidate conflicts"
    )
    for entry in plan["slices"]:
        assert entry["carrier_tasks"].endswith("/tasks.md"), (
            "each confirmed slice names the tasks.md it hands over (C-022 carrier)"
        )


def test_c011_half_condition_candidates_are_named_conflicts(tmp_path):
    plan = _plan(_copy_fixture("conflict-injections", tmp_path))
    assert [s["slug"] for s in plan["slices"]] == [CONFLICT_ALPHA, CONFLICT_BETA]
    excluded = {c["unit"]: c for c in _conflicts(plan, "slice-candidate-unconfirmed")}
    assert set(excluded) == {"099y-fixture-name-only", "slice-099z-declared-only"}, (
        "C-011: a directory satisfying only one condition MUST NOT enter the set "
        "and MUST surface as a `slice-candidate-unconfirmed` conflict"
    )
    name_only = json.dumps(excluded["099y-fixture-name-only"], ensure_ascii=False)
    declared_only = json.dumps(excluded["slice-099z-declared-only"], ensure_ascii=False)
    assert "parent-declaration" in name_only, (
        "the name-family-only candidate MUST name the unmet declaration condition"
    )
    assert "name-family" in declared_only, (
        "the declaration-only candidate MUST name the unmet name-family condition"
    )
    for item in excluded.values():
        assert item["status"] == "open"
        assert item["candidates"], "every conflict carries candidate dispositions"


# ---------------------------------------------------------------------------
# C-012 — the order is the declared order; a fallback leaves a trace
# ---------------------------------------------------------------------------

def test_c012_split_record_order_with_basis_and_source(tmp_path):
    plan = _plan(_copy_fixture("split-pair", tmp_path))
    assert [s["slug"] for s in plan["slices"]] == [ALPHA, BETA]
    for entry in plan["slices"]:
        assert entry["order_basis"] == "split-record", (
            "C-012: the order MUST come from the split record's proposed_slices list"
        )
        assert ".specify/state/099-fixture-parent.md" in entry["order_source"]
        assert "proposed_slices" in entry["order_source"]


def test_c012_letter_order_fallback_leaves_a_trace(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path)
    (repo / ".specify" / "state" / "099-fixture-parent.md").unlink()
    plan = _plan(repo)
    assert [s["slug"] for s in plan["slices"]] == [ALPHA, BETA]
    for entry in plan["slices"]:
        assert entry["order_basis"] == "letter-order", (
            "C-012: with no split record the fallback MUST be letter order and "
            "MUST be recorded, never directory enumeration order"
        )
        assert entry["order_source"]


# ---------------------------------------------------------------------------
# C-013 — the closed 15-candidate universe, four actions, one flow
# ---------------------------------------------------------------------------

def test_c013_candidate_universe_is_the_closed_fifteen(tmp_path):
    plan = _plan(_copy_fixture("split-pair", tmp_path))
    roots = {row["name"].split("/")[0] for row in plan["artifacts"]}
    assert roots == CANDIDATES, (
        "C-013: the candidate universe is closed at exactly the fifteen names"
    )
    arts = _artifacts(plan)
    assert arts["requirements.md"]["action"] == "merge"
    assert arts["plan.md"]["action"] == "merge"
    assert arts["tasks.md"]["action"] == "merge", (
        "C-013 mandatory floor: tasks.md is disposed whether or not slices produce it"
    )
    assert arts["data-model.md"]["action"] == "create"
    assert arts["research.md"]["action"] == "keep"
    assert arts["feature-ref.md"]["action"] == "keep"
    assert arts["quickstart.md"]["action"] == "not-applicable"
    assert arts["quickstart.md"]["basis"], (
        "C-013: `not-applicable` MUST carry its basis"
    )
    assert arts["notes"]["action"] == "not-applicable"
    assert arts["notes"]["basis"]
    assert {row["action"] for row in plan["artifacts"]} == ACTIONS, (
        "all four closed actions are exercised by the split-pair fixture"
    )
    for row in plan["artifacts"]:
        assert row["action"] in ACTIONS
        assert [p["slice"] for p in row["per_slice"]] == [ALPHA, BETA], (
            "C-013/V9: every artifact row records presence per slice"
        )


def test_c013_directory_candidates_are_file_level_units(tmp_path):
    plan = _plan(_copy_fixture("split-pair", tmp_path))
    arts = _artifacts(plan)
    core = arts["contracts/core.contract.md"]
    assert core["action"] == "merge", (
        "C-013: a file present on both sides is the merge unit"
    )
    assert core["unit"] == "directory-file"
    assert all(item["present"] for item in core["per_slice"])
    extra = arts["contracts/extra-alpha.md"]
    assert extra["action"] == "create", (
        "C-013: a slice-only file is created under the parent directory"
    )
    assert extra["per_slice"] == [
        {"slice": ALPHA, "present": True},
        {"slice": BETA, "present": False},
    ]
    assert extra["sources"] == [ALPHA]
    assert arts["contracts/core.contract.md"]["action"] == "merge"
    assert arts["checklists/requirements.md"]["action"] == "merge"
    assert arts["checklists/plan-review.md"]["action"] == "create"


def test_c013_dated_records_are_pointer_inclusions(tmp_path):
    plan = _plan(_copy_fixture("split-pair", tmp_path))
    arts = _artifacts(plan)
    same = arts["checkpoints/cp-2026-11-01.txt"]
    assert same["action"] == "keep", (
        "C-020: a same-name dated record keeps the parent copy"
    )
    assert same["pointer"]["kind"] == "slice-original"
    assert any(ALPHA in path for path in same["pointer"]["paths"]), (
        "the keep row records a pointer to the slice original"
    )
    evidence = arts["test-evidence/run-2026-11-01.txt"]
    assert evidence["action"] == "keep"
    assert evidence["pointer"]["kind"] == "slice-original"
    only = arts["checkpoints/cp-2026-11-05.txt"]
    assert only["action"] == "create", (
        "C-020: a slice-only dated record becomes a parent pointer view"
    )
    assert only["pointer_view"] is True
    evidence_only = arts["test-evidence/run-2026-11-02.txt"]
    assert evidence_only["action"] == "create"
    assert evidence_only["pointer_view"] is True


def test_c013_mandatory_floor_pointer_views(tmp_path):
    plan = _plan(_copy_fixture("split-pair", tmp_path))
    arts = _artifacts(plan)
    for name in ("verification.md", "review.md", "code-review.md"):
        row = arts[name]
        assert row["action"] == "create", (
            "C-013 mandatory floor: with a non-empty slice set the parent "
            "verification/review/code-review views MUST be produced (absent → create)"
        )
        assert row["pointer_view"] is True
        assert row["basis"]
    assert "tasks.md" in arts
    assert plan["checks"]["candidate_count"] == 15


# ---------------------------------------------------------------------------
# C-015 — ID families: parent mapping reuse, slice-unique append in merge order
# ---------------------------------------------------------------------------

def test_c015_id_maps_families(tmp_path):
    plan = _plan(_copy_fixture("split-pair", tmp_path))

    fr = _entries(plan, "FR")
    mapped = _entry(fr, ALPHA, "FR-001")
    assert mapped["parent_id"] == "FR-001"
    assert mapped["kind"] == "localization", (
        "C-016: a declared mapping with differing text is legal localization, "
        "not a conflict"
    )
    appended = _entry(fr, ALPHA, "FR-005")
    assert (appended["parent_id"], appended["kind"]) == ("FR-003", "appended")
    assert _entry(fr, BETA, "FR-002")["kind"] == "localization"
    assert _entry(fr, BETA, "FR-005")["parent_id"] == "FR-004", (
        "C-015: slice-unique ids append in merge order (alpha first)"
    )

    sc = _entries(plan, "SC")
    assert _entry(sc, ALPHA, "SC-001")["parent_id"] == "SC-001"

    strings = _entries(plan, "STR")
    assert _entry(strings, ALPHA, "STR-002")["kind"] == "mapped"
    assert _entry(strings, ALPHA, "STR-003")["kind"] == "appended"
    assert _entry(strings, BETA, "STR-002")["parent_id"] == "STR-002"

    tasks = _entries(plan, "T")
    assert [
        _entry(tasks, ALPHA, "T001")["parent_id"],
        _entry(tasks, ALPHA, "T002")["parent_id"],
        _entry(tasks, BETA, "T001")["parent_id"],
        _entry(tasks, BETA, "T002")["parent_id"],
    ] == ["T002", "T003", "T004", "T005"], (
        "C-015: task rows renumber by merge order after the retained parent rows"
    )
    assert all(entry["kind"] == "appended" for entry in tasks)

    clauses = _entries(plan, "C")
    assert _entry(clauses, ALPHA, "C-001")["parent_id"] == "C-001"
    assert _entry(clauses, ALPHA, "C-005")["parent_id"] == "C-003", (
        "C-015: clause appends use the parent file's next free C-N"
    )
    assert _entry(clauses, ALPHA, "C-007")["parent_id"] == "C-001", (
        "a contract file absent from the parent starts its own clause sequence"
    )
    assert _entry(clauses, BETA, "C-002")["parent_id"] == "C-002"

    entities = _entries(plan, "E")
    assert _entry(entities, ALPHA, "E1")["kind"] == "appended"


def test_c015_id_maps_are_rerun_stable(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path)
    first = _plan(repo)
    second = _plan(repo)
    assert first["id_maps"] == second["id_maps"], (
        "C-014/C-015: the same family MUST map identically on every run"
    )


# ---------------------------------------------------------------------------
# C-016 — semantic alignment trusts only the declared mapping table
# ---------------------------------------------------------------------------

def test_c016_unmapped_entry_is_a_conflict(tmp_path):
    proc, payload = _run_plan(_copy_fixture("conflict-injections", tmp_path))
    assert proc.returncode == 1
    assert payload["verdict"] == "refused"
    assert payload["exit_code"] == 1
    conflicts = _conflicts(payload["plan"], "no-mapping")
    assert len(conflicts) == 1, (
        "C-016: a slice entry colliding with a parent entry and carrying no "
        "declared mapping MUST be exactly one conflict"
    )
    item = conflicts[0]
    assert item["unit"] == "FR-002"
    assert item["status"] == "open"
    assert CONFLICT_ALPHA in json.dumps(item)
    assert [c["code"] for c in payload["conditions"]].count("no-mapping") == 1, (
        "C-006/C-018: an open conflict is named in the refusal conditions"
    )


# ---------------------------------------------------------------------------
# C-017 — token→registry binding, same-number-different-meaning, factory docs
# ---------------------------------------------------------------------------

def test_c017_same_number_different_meaning_conflict(tmp_path):
    plan = _plan(_copy_fixture("conflict-injections", tmp_path))
    conflicts = _conflicts(plan, "str-same-number-different-meaning")
    assert len(conflicts) == 1
    blob = json.dumps(conflicts[0], ensure_ascii=False)
    assert "parent-a" in blob and "conflict-a" in blob, (
        "C-017: the conflict MUST present both literals side by side"
    )
    assert "conflict-a-two" not in blob, (
        "the same-number conflict carries the STR-001 literals, not another row's"
    )
    assert conflicts[0]["status"] == "open"


def test_c017_factory_doc_slice_local_detection(tmp_path):
    proc, payload = _run_plan(_copy_fixture("factory-doc", tmp_path))
    plan = payload["plan"]
    assert proc.returncode == 0 and payload["verdict"] == "ok", (
        "a deterministically resolvable factory-doc reference is a recorded "
        "resolution, not an open conflict"
    )
    refs = plan["factory_doc_refs"]
    assert len(refs) == 1
    ref = refs[0]
    assert ref["path"] == "skills/internal/demo-factory/SKILL.md"
    assert ref["token"] == "STR-001"
    assert ref["slice"] == "099a-fixture-fd"
    assert ref["parent_id"] == "STR-007", (
        "C-017: the declared mapping identifies the merged parent id"
    )
    assert ref["resolution"]["kind"] == "repoint"
    assert ref["status"] == "resolved"
    assert not _conflicts(plan)


def test_c017_cross_registry_ambiguity_is_a_conflict(tmp_path):
    plan = _plan(_copy_fixture("conflict-injections", tmp_path))
    ambiguous = _conflicts(plan, "factory-doc-ref-ambiguous")
    assert len(ambiguous) == 1, (
        "C-017: an undeclared-registry reference hitting two slice registries "
        "with differing literals MUST be a conflict (never a guess)"
    )
    blob = json.dumps(ambiguous[0], ensure_ascii=False)
    assert "skills/internal/demo-factory/SKILL.md" in blob
    assert "STR-002" in blob
    assert "conflict-a-two" in blob and "conflict-b-two" in blob
    refs_blob = json.dumps(plan["factory_doc_refs"], ensure_ascii=False)
    assert "STR-888" not in refs_blob, (
        "a token that hits no slice registry is not a slice-local reference "
        "and does not change meaning under this merge"
    )
    assert "STR-888" not in json.dumps(plan["conflicts"], ensure_ascii=False)


# ---------------------------------------------------------------------------
# C-018 — conflicts are first-class records; open means blocked
# ---------------------------------------------------------------------------

def test_c018_same_anchor_dual_edit_is_a_conflict(tmp_path):
    plan = _plan(_copy_fixture("conflict-injections", tmp_path))
    conflicts = _conflicts(plan, "same-anchor-dual-edit")
    assert len(conflicts) == 1, (
        "C-021/plan ruling 1: a slice-declared rewrite of an anchor the parent "
        "also owns MUST be a conflict, not a silent pick"
    )
    blob = json.dumps(conflicts[0], ensure_ascii=False)
    assert "Execution Model" in blob
    assert conflicts[0]["status"] == "open"


# ---------------------------------------------------------------------------
# read-only surface and exit semantics
# ---------------------------------------------------------------------------

def test_merge_plan_is_read_only(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path)
    before = _snapshot(repo)
    _plan(repo)
    assert _snapshot(repo) == before, (
        "C-001/C-008: merge-plan is a read-only action and MUST write nothing"
    )


def test_merge_plan_is_rerun_stable(tmp_path):
    repo = _copy_fixture("conflict-injections", tmp_path)
    first = _run_plan(repo)
    second = _run_plan(repo)
    assert first[0].returncode == second[0].returncode == 1
    assert first[0].stdout == second[0].stdout, (
        "C-006/C-010: the same input reproduces the same report byte for byte"
    )
    assert first[0].stderr == "" and second[0].stderr == ""


def test_merge_plan_exit_semantics(tmp_path):
    clean, clean_payload = _run_plan(_copy_fixture("split-pair", tmp_path))
    assert clean.returncode == 0
    assert clean_payload["verdict"] == "ok"
    assert clean_payload["exit_code"] == 0
    assert clean_payload["conditions"] == []
    dirty, dirty_payload = _run_plan(_copy_fixture("conflict-injections", tmp_path))
    assert dirty.returncode == 1
    assert dirty_payload["verdict"] == "refused"
    assert dirty_payload["exit_code"] == 1
    assert dirty_payload["conditions"], (
        "C-002: an open conflict refuses with exit 1 and a complete read-only report"
    )
    for condition in dirty_payload["conditions"]:
        assert set(condition) == {"code", "evidence", "fix_path", "rerun"}


# ---------------------------------------------------------------------------
# C-112 — archived slices are discovered from `archive-manifest.json`
# ---------------------------------------------------------------------------

def test_c112_archived_pair_keeps_the_slice_set_and_order(tmp_path):
    repo = _copy_archive_fixture(tmp_path)
    proc, payload = _run_plan(repo, ARCHIVE_PARENT)
    assert proc.returncode == 0, (
        "C-112: an archived pair is the same slice set, not an empty one; "
        "exit=%d conditions=%r" % (proc.returncode, payload.get("conditions"))
    )
    plan = payload["plan"]
    assert [entry["slug"] for entry in plan["slices"]] == [ARCHIVE_ALPHA, ARCHIVE_BETA]
    assert [entry["order"] for entry in plan["slices"]] == [1, 2]
    assert {entry["order_basis"] for entry in plan["slices"]} == {"split-record"}, (
        "C-112: the order basis recorded at archive time is carried through unchanged"
    )
    assert plan["checks"]["slice_count"] == 2
    assert plan["checks"]["open_conflicts"] == 0
    assert all("/" not in entry["slug"] for entry in plan["slices"]), (
        "C-112: `slices/` is never read as a new slice candidate"
    )


def test_c112_archived_slices_are_read_from_their_archived_paths(tmp_path):
    repo = _copy_archive_fixture(tmp_path)
    plan = _plan(repo, ARCHIVE_PARENT)
    for entry in plan["slices"]:
        assert entry["carrier_tasks"] == (
            ".specify/specs/%s/slices/%s/tasks.md" % (ARCHIVE_PARENT, entry["slug"])
        ), "C-112: the archived slice record is read at its `to` path"
    mapped = _entry(_entries(plan, "FR"), ARCHIVE_ALPHA, "FR-001")
    assert mapped["parent_id"] == "FR-001", (
        "C-112: the id maps are derived from the archived requirements, byte for byte"
    )


def test_c112_empty_archive_directory_falls_back_to_the_sibling_scan(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path)
    (repo / ".specify" / "specs" / PARENT / "slices").mkdir()
    plan = _plan(repo)
    assert [entry["slug"] for entry in plan["slices"]] == [ALPHA, BETA], (
        "C-112: an empty `slices/` directory is the absent-manifest fallback case"
    )


def test_c112_unparsable_archive_manifest_is_an_input_error(tmp_path):
    repo = _copy_archive_fixture(tmp_path)
    manifest = repo / ".specify" / "specs" / ARCHIVE_PARENT / "archive-manifest.json"
    manifest.write_text("{ not json\n", encoding="utf-8")
    proc, payload = _run_plan(repo, ARCHIVE_PARENT)
    assert proc.returncode == 2
    assert payload["verdict"] == "error"
    assert [condition["code"] for condition in payload["conditions"]] == [
        "archive-manifest-invalid"
    ], "C-112: an unparsable archive record exits 2 as `archive-manifest-invalid`"


def test_c112_manifest_disagreeing_with_the_merge_manifest_is_drift(tmp_path):
    repo = _copy_archive_fixture(tmp_path)
    merge_path = repo / ".specify" / "specs" / ARCHIVE_PARENT / "merge-manifest.json"
    document = json.loads(merge_path.read_text(encoding="utf-8"))
    document["slices"][1]["order"] = 3
    merge_path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    proc, payload = _run_plan(repo, ARCHIVE_PARENT)
    assert proc.returncode == 2
    assert payload["verdict"] == "error"
    assert [condition["code"] for condition in payload["conditions"]] == [
        "archive-drift"
    ], "C-112: an archive record disagreeing with the merge manifest is drift"


def test_c112_manifest_disagreeing_with_the_tree_is_drift(tmp_path):
    repo = _copy_archive_fixture(tmp_path)
    parent = repo / ".specify" / "specs" / ARCHIVE_PARENT
    shutil.move(str(parent / "slices" / ARCHIVE_BETA),
                str(repo / ".specify" / "specs" / ARCHIVE_BETA))
    proc, payload = _run_plan(repo, ARCHIVE_PARENT)
    assert proc.returncode == 2
    assert payload["verdict"] == "error"
    assert [condition["code"] for condition in payload["conditions"]] == [
        "archive-drift"
    ], "C-112: a half-archived tree is drift, never a fallback read"
