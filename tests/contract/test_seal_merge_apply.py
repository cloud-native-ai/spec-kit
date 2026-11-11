"""Contract tests for the seal engine's ``merge-apply`` action (Feature 099, work package P4).

Contract: ``.specify/specs/099-speckit-seal/contracts/merge-back.contract.md``
Clauses:  C-013 … C-023 (the apply face) — deterministic parent writes for the
          ``merge`` / ``create`` / ``keep`` actions (directory candidates as
          file-level units, same-name three states), dated-record pointer
          inclusions (never a copy, originals byte-stable), every reference
          rewritten to its merged id, pre-split rows disposed as ``supersede``,
          exactly one ``**Merged into**:`` line per slice, the
          ``merge-manifest.json`` schema (stable key order, self digest,
          ``checks``) and the dated-record hash assertion.

Fixture trees: ``tests/fixtures/seal/split-pair/`` (clean two-slice merge),
``conflict-injections/`` (open conflicts must refuse before any write) and
``factory-doc/`` (a factory document citing a slice-local id).

Red-first: this file landed before the ``merge-apply`` body existed; the red
reading lives in ``.specify/specs/099-speckit-seal/notes/red-first-evidence.md``.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
VALIDATE_REQUIREMENTS = REPO_ROOT / "scripts" / "python" / "validate-requirements.py"
VALIDATE_TASKS = REPO_ROOT / "scripts" / "python" / "validate-tasks.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "seal"

PARENT = "099-fixture-parent"
ALPHA = "099a-fixture-alpha"
BETA = "099b-fixture-beta"

MANIFEST_KEYS = {
    "schema_version", "spec", "merge", "generated_by", "slices", "artifacts",
    "factory_doc_resolutions", "id_maps", "conflicts", "dispositions", "checks",
    "digest",
}
ARTIFACT_ACTIONS = {"merge", "create", "keep", "not-applicable"}
SLICE_MARKER = "**Merged into**: .specify/specs/%s（merge-manifest.json）" % PARENT
ACTIVE_TASK_RE = re.compile(r"^- \[(.)\] (T\d{3})\b")
DATED_DIRS = ("checkpoints", "test-evidence")
DATE_RE = re.compile(r"\d{4}-?\d{2}-?\d{2}")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _copy_fixture(name: str, target: Path) -> Path:
    source = FIXTURES / name
    assert source.is_dir(), (
        f"fixture tree missing: {source} — this is the expected red-first reading "
        "for T021 before the apply work package lands"
    )
    shutil.copytree(source, target)
    return target


def _spec(repo: Path, slug: str = PARENT) -> Path:
    return repo / ".specify" / "specs" / slug


def _run_apply(repo: Path, spec: str = PARENT):
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "merge-apply",
         "--spec-dir", str(_spec(repo, spec)), "--repo", str(repo), "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.stdout.strip(), (
        f"expected a stdout payload; exit={proc.returncode} stderr={proc.stderr[-800:]!r}"
    )
    return proc, json.loads(proc.stdout)


def _manifest(repo: Path) -> dict:
    path = _spec(repo) / "merge-manifest.json"
    assert path.is_file(), (
        "C-019: merge-apply MUST produce merge-manifest.json in the parent spec dir"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def _snapshot(root: Path) -> dict:
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*")) if p.is_file()
    }


def _dated_snapshot(repo: Path) -> dict:
    """C-020: the dated records whose bytes the run must not change."""
    paths = []
    for slug in (ALPHA, BETA):
        base = _spec(repo, slug)
        for name in ("review.md", "code-review.md", "verification.md"):
            if (base / name).is_file():
                paths.append(base / name)
        for dirname in DATED_DIRS:
            if (base / dirname).is_dir():
                paths.extend(p for p in sorted((base / dirname).rglob("*")) if p.is_file())
    return {
        str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in paths
    }


def _run_validator(script: Path, artifact: Path):
    return subprocess.run(
        [sys.executable, str(script), str(artifact), "--json"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, encoding="utf-8", check=False,
    )


def _artifacts(manifest: dict) -> dict:
    return {row["name"]: row for row in manifest["artifacts"]}


# ---------------------------------------------------------------------------
# C-013 / C-019 — the apply run, its actions and the manifest
# ---------------------------------------------------------------------------

def test_clean_split_pair_applies_with_exit_zero(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    proc, payload = _run_apply(repo)
    assert proc.returncode == 0, (
        f"C-018: a clean split pair MUST apply; exit={proc.returncode} "
        f"payload={json.dumps(payload, ensure_ascii=False)[:800]}"
    )
    assert payload["verdict"] == "ok"
    assert payload["conditions"] == []
    apply = payload["apply"]
    assert apply["idempotent"] is False
    assert apply["manifest"] == ".specify/specs/%s/merge-manifest.json" % PARENT
    assert apply["slices"] == [ALPHA, BETA]
    assert apply["writes"], "C-019: a real merge reports the files it wrote"
    assert apply["checks"]["open_rows"] == 0
    assert apply["checks"]["id_continuity"] == "pass"
    assert apply["checks"]["duplicate_ids"] == 0
    assert apply["checks"]["dangling_refs"] == 0
    assert apply["checks"]["dated_record_hashes_stable"] is True


def test_requirements_merge_rewrites_ids_and_keeps_parent_text(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    _run_apply(repo)
    text = (_spec(repo) / "requirements.md").read_text(encoding="utf-8")
    assert "- **FR-001**: Parent alpha requirement, owned by the parent." in text, (
        "C-016: a mapped entry keeps the parent phrasing (localization)"
    )
    assert "- **FR-002**: Parent beta requirement, owned by the parent." in text
    assert "- **FR-003**: Alpha-only requirement, appended by merge order." in text, (
        "C-015: a slice-unique FR appends under the next free parent id (alpha first)"
    )
    assert "- **FR-004**: Beta-only requirement, appended by merge order." in text
    assert text.count("- **FR-001**") == 1, (
        "C-014: the merge MUST NOT duplicate a mapped definition row"
    )
    assert "FR-005" not in text, (
        "C-015: every reference is rewritten to its merged id and no stale id survives"
    )
    assert re.search(r"\|\s*`STR-003`\s*\|\s*`\"alpha-only\"`", text), (
        "C-015: a slice-unique shared string appends to the parent registry"
    )


def test_tasks_merge_supersedes_pre_split_rows(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    _run_apply(repo)
    text = (_spec(repo) / "tasks.md").read_text(encoding="utf-8")
    rows = [(match.group(2), match.group(1))
            for line in text.splitlines()
            if (match := ACTIVE_TASK_RE.match(line))]
    assert [task_id for task_id, _ in rows] == ["T001", "T002", "T003", "T004", "T005"], (
        "C-015/C-022: retained parent rows plus slice rows renumbered in merge order"
    )
    assert all(state == "X" for _, state in rows), (
        "C-022: the merged parent tasks.md carries zero unchecked active rows"
    )
    assert "## Superseded pre-split record" in text, (
        "C-022: the pre-split open rows move into the supersede block"
    )
    assert "> - [ ] T002 Parent open pre-split task, superseded by the split." in text, (
        "C-022: the original row text is retained with a `> ` quote prefix"
    )
    superseded_line = next(
        line for line in text.splitlines() if "Parent open pre-split task" in line)
    assert not ACTIVE_TASK_RE.match(superseded_line), (
        "C-022: a quoted row MUST NOT be counted as an active task row"
    )
    manifest = _manifest(repo)
    assert len(manifest["dispositions"]) == 1
    disposal = manifest["dispositions"][0]
    assert disposal["disposition"] == "supersede"
    assert disposal["superseded"] == {
        "path": ".specify/specs/%s/tasks.md" % PARENT, "line": 4}, (
        "C-022: the superseded position is the original line in the parent tasks.md")
    assert disposal["superseded_by"] == {"path": "merge-manifest.json", "line": 0}, (
        "C-022: superseded_by points at the manifest itself (whole-file fact)"
    )
    assert set(disposal["evidence"]) == {
        ".specify/specs/%s/tasks.md" % ALPHA,
        ".specify/specs/%s/tasks.md" % BETA,
    }
    assert disposal["guard_status"] == "replaced"


def test_contract_merge_appends_clauses_and_creates_slice_only_file(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    _run_apply(repo)
    core = (_spec(repo) / "contracts" / "core.contract.md").read_text(encoding="utf-8")
    assert "**C-001** — Parent core clause one. (FR-001)" in core, (
        "C-016: a mapped contract clause keeps the parent text"
    )
    assert "**C-003** — Alpha-only clause, appended by merge order. (FR-003)" in core, (
        "C-015: a slice-unique clause appends under the parent file's next free C-N"
    )
    assert "**C-005**" not in core, (
        "C-014: no stale slice-local clause id survives the merge"
    )
    assert core.count("**C-001**") == 1, "C-014: no duplicated clause id"
    extra = _spec(repo) / "contracts" / "extra-alpha.md"
    assert extra.is_file(), "C-013: a slice-only contract file is created under the parent"
    extra_text = extra.read_text(encoding="utf-8")
    assert "**C-001** — Alpha-only contract file clause. (FR-003)" in extra_text, (
        "C-015/C-017: a created file's clause ids are rewritten within its own sequence"
    )
    assert "C-007" not in extra_text


def test_one_and_two_digit_clause_ids_merge_instead_of_being_lost(tmp_path):
    """C-015: clause ids are ``C-<digits>``; 1-2 digit ids merge like 3-digit ids.

    The real 074 tree writes ``**C-1** … **C-67**``. An engine anchored to
    ``C-\\d{3}`` recognizes none of them, so every slice clause is silently
    dropped (the P8 round's B4 content loss). This test rewrites the fixture's
    pinned 3-digit ids to the 1-2 digit form and expects the same merge.
    """
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    rewrites = {
        _spec(repo) / "contracts" / "core.contract.md": [
            ("**C-001**", "**C-1**"), ("**C-002**", "**C-2**")],
        _spec(repo, ALPHA) / "contracts" / "core.contract.md": [
            ("**C-001**", "**C-1**"), ("**C-005**", "**C-5**")],
        _spec(repo, ALPHA) / "contracts" / "extra-alpha.md": [
            ("**C-007**", "**C-7**")],
        _spec(repo, BETA) / "contracts" / "core.contract.md": [
            ("**C-002**", "**C-2**")],
        _spec(repo, ALPHA) / "requirements.md": [
            ("| `C-001` | `C-001` |", "| `C-1` | `C-1` |")],
        _spec(repo, BETA) / "requirements.md": [
            ("| `C-002` | `C-002` |", "| `C-2` | `C-2` |")],
    }
    for path, pairs in rewrites.items():
        text = path.read_text(encoding="utf-8")
        for before, after in pairs:
            assert before in text, f"{path} lacks {before!r}"
            text = text.replace(before, after)
        path.write_text(text, encoding="utf-8")
    proc, payload = _run_apply(repo)
    assert proc.returncode == 0, payload.get("conditions")
    core = (_spec(repo) / "contracts" / "core.contract.md").read_text(encoding="utf-8")
    assert "**C-003** — Alpha-only clause, appended by merge order. (FR-003)" in core, (
        "a 1-2 digit slice clause must append under the parent file's next free "
        "C-N instead of being skipped as an unrecognized id form"
    )
    assert "**C-2** — Parent core clause two. (FR-002)" in core, (
        "the parent's own 1-2 digit clause is left untouched"
    )
    extra_text = (_spec(repo) / "contracts" / "extra-alpha.md").read_text(encoding="utf-8")
    assert "**C-001** — Alpha-only contract file clause. (FR-003)" in extra_text
    assert "C-7" not in extra_text
    entries = {(entry["slice"], entry["slice_id"]): entry
               for entry in _manifest(repo)["id_maps"]["C"]}
    assert entries[(ALPHA, "C-1")]["parent_id"] == "C-1", (
        "C-016: the declared 1-2 digit Parent Mapping row must be readable"
    )
    assert entries[(ALPHA, "C-5")]["parent_id"] == "C-003", (
        "C-015: the appended 1-2 digit clause records its merged id in id_maps"
    )


def test_merged_slice_task_rows_keep_their_phase_headings(tmp_path):
    """C-015/C-022: slice rows land under phase headings, so the merged file validates.

    The P8 round's B3: rows appended as one flat block after the last kept parent
    row carry ``[USn]`` labels under ``<no phase>``, and validate-tasks reports
    one story-labels error per row.
    """
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    for slug, label in ((ALPHA, "Alpha"), (BETA, "Beta")):
        (_spec(repo, slug) / "tasks.md").write_text(
            "# Tasks: fixture %s\n\n"
            "## Phase 1: User Story 1 - fixture story\n\n"
            "- [X] T001 [US1] %s first closed task.\n"
            "- [X] T002 [US1] %s second closed task.\n" % (slug, label, label),
            encoding="utf-8")
    proc, payload = _run_apply(repo)
    assert proc.returncode == 0, payload.get("conditions")
    merged = (_spec(repo) / "tasks.md").read_text(encoding="utf-8")
    assert "## Phase 1: User Story 1 - fixture story" in merged, (
        "the slice phase headings must ride along so the rows keep their story phase"
    )
    validator = _run_validator(VALIDATE_TASKS, _spec(repo) / "tasks.md")
    assert validator.returncode == 0, (
        "the merged task list must pass validate-tasks (story-label placement); got:\n"
        + validator.stdout[-1600:]
    )


def test_directory_candidates_merge_and_create_at_file_level(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    _run_apply(repo)
    checklist = (_spec(repo) / "checklists" / "requirements.md").read_text(encoding="utf-8")
    assert "Parent checklist row for requirements." in checklist
    assert "Alpha checklist row for requirements." in checklist, (
        "C-013: a same-name file on both sides merges without losing either side"
    )
    plan_review = _spec(repo) / "checklists" / "plan-review.md"
    assert plan_review.is_file(), "C-013: a slice-only file is created"
    assert "Alpha-only checklist for the merged plan." in plan_review.read_text(
        encoding="utf-8")
    model = (_spec(repo) / "data-model.md").read_text(encoding="utf-8")
    assert "| E1 | Alpha entity | slice-unique entity |" in model, (
        "C-013/C-015: a created data-model carries the slice entity row under its merged id"
    )


def test_prose_artifacts_append_unique_sections_with_source_markers(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    before = (_spec(repo) / "research.md").read_bytes()
    _run_apply(repo)
    plan = (_spec(repo) / "plan.md").read_text(encoding="utf-8")
    assert "Parent execution model, parent text is authoritative." in plan, (
        "C-021: the parent prose stays the authority and is kept unchanged"
    )
    assert "## Merged from slices" in plan, (
        "C-021: slice-unique sections land in the merged appendix"
    )
    assert "<!-- source: %s -->" % ALPHA in plan
    assert "<!-- source: %s -->" % BETA in plan
    assert "Alpha Unique Section" in plan and "Beta Unique Section" in plan
    assert (_spec(repo) / "research.md").read_bytes() == before, (
        "C-021: a keep artifact is not rewritten"
    )


def test_pointer_views_and_dated_record_pointer_inclusions(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    alpha_cp = _spec(repo, ALPHA) / "checkpoints" / "cp-2026-11-01.txt"
    beta_cp = _spec(repo, BETA) / "checkpoints" / "cp-2026-11-05.txt"
    parent_cp = _spec(repo) / "checkpoints" / "cp-2026-11-01.txt"
    alpha_cp_bytes, beta_cp_bytes = alpha_cp.read_bytes(), beta_cp.read_bytes()
    parent_cp_bytes = parent_cp.read_bytes()
    _run_apply(repo)

    verification = (_spec(repo) / "verification.md").read_text(encoding="utf-8")
    assert "SC-001_status=pass" in verification
    assert ".specify/specs/%s/verification.md" % ALPHA in verification
    assert "FR-002_status=pass" in verification
    assert ".specify/specs/%s/verification.md" % BETA in verification, (
        "C-013/C-020: the parent verification view is summary rows plus pointers, "
        "never a second measurement"
    )
    review = (_spec(repo) / "review.md").read_text(encoding="utf-8")
    assert ".specify/specs/%s/review.md" % ALPHA in review
    assert ".specify/specs/%s/review.md" % BETA in review
    code_review = (_spec(repo) / "code-review.md").read_text(encoding="utf-8")
    assert "blocking: 0" in code_review
    assert ".specify/specs/%s/code-review.md" % BETA in code_review

    only_in_beta = _spec(repo) / "checkpoints" / "cp-2026-11-05.txt"
    assert only_in_beta.is_file(), (
        "C-020: a slice-only dated record becomes a parent pointer view"
    )
    pointer_view = only_in_beta.read_text(encoding="utf-8")
    assert "pointer: .specify/specs/%s/checkpoints/cp-2026-11-05.txt" % BETA in pointer_view
    assert "sha256:" in pointer_view
    assert pointer_view != beta_cp.read_text(encoding="utf-8"), (
        "C-020: the parent carries a pointer view, never a copy of the original"
    )
    evidence_view = _spec(repo) / "test-evidence" / "run-2026-11-02.txt"
    assert evidence_view.is_file()
    assert "pointer: .specify/specs/%s/test-evidence/run-2026-11-02.txt" % BETA in \
        evidence_view.read_text(encoding="utf-8")

    assert parent_cp.read_bytes() == parent_cp_bytes, (
        "C-020: a same-name dated record keeps the parent copy byte-identical"
    )
    assert alpha_cp.read_bytes() == alpha_cp_bytes
    assert beta_cp.read_bytes() == beta_cp_bytes, (
        "C-020: slice originals stay byte-identical (never copied over or rewritten)"
    )


def test_dated_records_are_hash_stable_across_the_run(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    before = _dated_snapshot(repo)
    proc, payload = _run_apply(repo)
    assert proc.returncode == 0, (
        "the hash-stability assertion is only meaningful on a completed merge; "
        f"exit={proc.returncode} payload={json.dumps(payload, ensure_ascii=False)[:500]}"
    )
    after = _dated_snapshot(repo)
    assert after == before, (
        "C-020: the engine MUST hash the dated records before and after the run "
        "and assert they are unchanged"
    )


def test_each_slice_carries_exactly_one_merged_into_line(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    _run_apply(repo)
    for slug in (ALPHA, BETA):
        text = (_spec(repo, slug) / "requirements.md").read_text(encoding="utf-8")
        markers = [line for line in text.splitlines()
                   if line.startswith("**Merged into**:")]
        assert len(markers) == 1, (
            "C-019/E14: exactly one `**Merged into**:` line per slice; "
            f"found {markers!r} in {slug}"
        )
        assert markers[0] == SLICE_MARKER, (
            "E14: the marker names the parent spec and the manifest"
        )
        lines = text.splitlines()
        status = next(i for i, line in enumerate(lines) if line.startswith("**Status**:"))
        marker = next(i for i, line in enumerate(lines)
                      if line.startswith("**Merged into**:"))
        assert marker == status + 1, (
            "E14: the marker is appended right after the `**Status**` line"
        )


def test_manifest_schema_is_stable_and_self_digested(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    _run_apply(repo)
    path = _spec(repo) / "merge-manifest.json"
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert set(data) == MANIFEST_KEYS, (
        f"E3: the manifest key set is closed; measured {sorted(data)}"
    )
    assert raw == json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", (
        "E3: the manifest is written with a stable key order (sort_keys), "
        "indent=2 and a trailing newline"
    )
    body = dict(data)
    digest = body.pop("digest")
    canonical = json.dumps(body, separators=(",", ":"), sort_keys=True,
                           ensure_ascii=False)
    expected = "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    assert digest == expected, (
        "V12: the digest is the sha256 of the canonical JSON with `digest` removed"
    )
    assert data["spec"] == PARENT
    assert data["merge"] == {"status": "merged"}
    assert [s["slug"] for s in data["slices"]] == [ALPHA, BETA]
    assert all(s["retention"] == "pending-review" for s in data["slices"]), (
        "V16: retention is explicit, never silently absent"
    )
    assert data["conflicts"] == [], "C-018: a clean merge carries no open conflict"
    assert data["factory_doc_resolutions"] == []

    arts = _artifacts(data)
    roots = {name.split("/")[0] for name in arts}
    assert roots == {
        "requirements.md", "plan.md", "tasks.md", "data-model.md", "contracts",
        "research.md", "quickstart.md", "feature-ref.md", "verification.md",
        "review.md", "code-review.md", "checklists", "checkpoints", "test-evidence",
        "notes",
    }, "V9: the manifest covers the closed fifteen-candidate universe"
    for row in data["artifacts"]:
        assert row["action"] in ARTIFACT_ACTIONS
        assert isinstance(row["checks"], dict), (
            "E5: every artifact row carries its own post-merge checks"
        )
        assert [p["slice"] for p in row["per_slice"]] == [ALPHA, BETA], (
            "V9: per_slice covers every slice for every candidate row"
        )
    assert arts["requirements.md"]["checks"]["id_continuity"] == "pass"
    assert arts["tasks.md"]["checks"]["open_rows"] == 0
    assert arts["checkpoints/cp-2026-11-01.txt"]["action"] == "keep"
    assert arts["checkpoints/cp-2026-11-01.txt"]["pointer"]["kind"] == "slice-original"
    assert arts["checkpoints/cp-2026-11-05.txt"]["pointer_view"] is True
    assert arts["test-evidence/run-2026-11-02.txt"]["pointer_view"] is True
    assert data["checks"]["open_rows"] == 0
    assert data["checks"]["dated_record_hashes_stable"] is True


def test_merged_parent_passes_the_existing_validators(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    proc, payload = _run_apply(repo)
    assert proc.returncode == 0, (
        "the validator proof is only meaningful on a completed merge; "
        f"exit={proc.returncode} payload={json.dumps(payload, ensure_ascii=False)[:500]}"
    )
    requirements = _spec(repo) / "requirements.md"
    tasks = _spec(repo) / "tasks.md"
    req = _run_validator(VALIDATE_REQUIREMENTS, requirements)
    assert req.returncode == 0, (
        "SC-004: the merged requirements.md MUST pass validate-requirements.py; "
        f"output={req.stdout[-1500:]!r} stderr={req.stderr[-500:]!r}"
    )
    task = _run_validator(VALIDATE_TASKS, tasks)
    assert task.returncode == 0, (
        "SC-004: the merged tasks.md MUST pass validate-tasks.py; "
        f"output={task.stdout[-1500:]!r} stderr={task.stderr[-500:]!r}"
    )


# ---------------------------------------------------------------------------
# C-018 / C-022 — refusals write nothing
# ---------------------------------------------------------------------------

def test_open_conflicts_refuse_and_write_nothing(tmp_path):
    repo = _copy_fixture("conflict-injections", tmp_path / "repo")
    before = _snapshot(repo)
    proc, payload = _run_apply(repo)
    assert proc.returncode == 1, (
        "C-018: an open conflict MUST refuse merge-apply with exit 1"
    )
    assert payload["verdict"] == "refused"
    codes = {condition["code"] for condition in payload["conditions"]}
    assert "no-mapping" in codes
    assert "slice-candidate-unconfirmed" in codes
    assert _snapshot(repo) == before, (
        "C-006/C-018: a refused merge-apply MUST NOT create any file (no partial manifest)"
    )


def test_unclosed_slice_tasks_refuse_and_write_nothing(tmp_path):
    repo = _copy_fixture("split-pair", tmp_path / "repo")
    beta_tasks = _spec(repo, BETA) / "tasks.md"
    beta_tasks.write_text(
        beta_tasks.read_text(encoding="utf-8").replace(
            "- [X] T001 Beta first closed task.",
            "- [ ] T001 Beta first closed task."),
        encoding="utf-8",
    )
    before = _snapshot(repo)
    proc, payload = _run_apply(repo)
    assert proc.returncode == 1, (
        "C-022: merging an unclosed slice would make the parent carry unchecked rows"
    )
    assert payload["verdict"] == "refused"
    assert "slice-unclosed" in {c["code"] for c in payload["conditions"]}
    assert _snapshot(repo) == before, (
        "a refused merge-apply MUST NOT fake-check the slice or write anything"
    )


# ---------------------------------------------------------------------------
# C-017 — factory-doc reference resolution
# ---------------------------------------------------------------------------

def test_factory_doc_reference_is_repointed_and_recorded(tmp_path):
    repo = _copy_fixture("factory-doc", tmp_path / "repo")
    doc = repo / "skills" / "internal" / "demo-factory" / "SKILL.md"
    before_line = "- Nested-run outcome is taken from `[[STR-001]]` " \
                  "(slice-local meaning `completed`)."
    assert before_line in doc.read_text(encoding="utf-8")
    proc, payload = _run_apply(repo)
    assert proc.returncode == 0
    after_text = doc.read_text(encoding="utf-8")
    assert "[[STR-007]]" in after_text, (
        "C-017: a recorded factory-doc resolution repoints the reference to the "
        "merged parent id"
    )
    assert "[[STR-001]]" not in after_text
    manifest = _manifest(repo)
    assert manifest["factory_doc_resolutions"] == [{
        "path": "skills/internal/demo-factory/SKILL.md",
        "line": 5,
        "before": before_line,
        "after": "- Nested-run outcome is taken from `[[STR-007]]` "
                 "(slice-local meaning `completed`).",
        "kind": "repoint",
    }], "V15: the resolution row carries {path, line, before, after, kind} verbatim"
    slice_requirements = (_spec(repo, "099a-fixture-fd") / "requirements.md").read_text(
        encoding="utf-8")
    assert slice_requirements.count("**Merged into**:") == 1


# ---------------------------------------------------------------------------
# C-211 (Feature 100) — the parent merge manifest's path-form amendment
# ---------------------------------------------------------------------------

def _load_engine():
    spec = importlib.util.spec_from_file_location("seal_utils_merge_apply_amend", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def eng():
    return _load_engine()


def _pairs():
    return [
        {"slug": ALPHA, "from": ".specify/specs/%s" % ALPHA,
         "to": ".specify/specs/%s/slices/%s" % (PARENT, ALPHA)},
        {"slug": BETA, "from": ".specify/specs/%s" % BETA,
         "to": ".specify/specs/%s/slices/%s" % (PARENT, BETA)},
    ]


def test_c211_whole_path_values_are_amended_everywhere(eng):
    document = {
        "schema_version": 1,
        "spec": PARENT,
        "merge": {"status": "merged"},
        "conflicts": [],
        "slices": [{"slug": ALPHA,
                    "carrier_tasks": ".specify/specs/%s/tasks.md" % ALPHA,
                    "retention": "pending-review"}],
        "dispositions": [{"evidence": [".specify/specs/%s/verification.md" % BETA]}],
        "artifacts": [{"pointer": {"paths": [".specify/specs/%s/plan.md" % ALPHA]}}],
        "id_maps": {"FR": [{"slice": ALPHA, "parent_id": "FR-001"}]},
        "checks": {"open_rows": 0},
    }
    result = eng.amended_merge_document(document, _pairs())
    amended = result["document"]
    assert amended["slices"][0]["carrier_tasks"] == (
        ".specify/specs/%s/slices/%s/tasks.md" % (PARENT, ALPHA))
    assert amended["dispositions"][0]["evidence"] == [
        ".specify/specs/%s/slices/%s/verification.md" % (PARENT, BETA)]
    assert amended["artifacts"][0]["pointer"]["paths"] == [
        ".specify/specs/%s/slices/%s/plan.md" % (PARENT, ALPHA)]
    assert amended["slices"][0]["slug"] == ALPHA, (
        "C-211: bare slug values are identity, never path-form values"
    )
    assert amended["slices"][0]["retention"] == "pending-review"
    assert amended["merge"] == {"status": "merged"}
    assert amended["checks"] == {"open_rows": 0}
    assert amended["id_maps"] == document["id_maps"]
    assert {(row["before"], row["after"]) for row in result["amendments"]} == {
        (".specify/specs/%s/tasks.md" % ALPHA,
         ".specify/specs/%s/slices/%s/tasks.md" % (PARENT, ALPHA)),
        (".specify/specs/%s/verification.md" % BETA,
         ".specify/specs/%s/slices/%s/verification.md" % (PARENT, BETA)),
        (".specify/specs/%s/plan.md" % ALPHA,
         ".specify/specs/%s/slices/%s/plan.md" % (PARENT, ALPHA)),
    }, "C-211: the matching set is the allowed difference set, enumerated in full"


def test_c211_partial_and_longer_values_are_untouched(eng):
    document = {
        "merge": {"status": "merged"},
        "slices": [{
            "slug": ALPHA,
            "carrier_tasks": ".specify/specs/%s/tasks.md" % ALPHA,
            "note": "prefix .specify/specs/%s/tasks.md" % ALPHA,
            "sibling": ".specify/specs/%s-extra/tasks.md" % ALPHA,
            "slug_list": [ALPHA, BETA],
        }],
    }
    result = eng.amended_merge_document(document, _pairs())
    amended = result["document"]
    assert amended["slices"][0]["note"] == "prefix .specify/specs/%s/tasks.md" % ALPHA
    assert amended["slices"][0]["sibling"] == (
        ".specify/specs/%s-extra/tasks.md" % ALPHA), (
        "C-211: matching is a whole-value, path-segment-boundary operation"
    )
    assert amended["slices"][0]["slug_list"] == [ALPHA, BETA]
    assert len(result["amendments"]) == 1


def test_c211_digest_is_recomputed_and_recorded_before_and_after(eng):
    document = {
        "merge": {"status": "merged"},
        "slices": [{"slug": BETA,
                    "carrier_tasks": ".specify/specs/%s/tasks.md" % BETA}],
    }
    result = eng.amended_merge_document(document, _pairs())
    before = eng.archive_manifest_digest(document)
    after = eng.archive_manifest_digest(result["document"])
    assert result["digest_before"] == before
    assert result["digest_after"] == after
    assert result["document"]["digest"] == after, (
        "C-211/C-034: the amended manifest carries its recomputed digest"
    )
    assert after != before
