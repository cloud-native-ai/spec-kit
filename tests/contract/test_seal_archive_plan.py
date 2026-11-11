"""Contract tests for the seal engine's ``archive-plan`` action (Feature 100, P3).

Contract: ``.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md``
          C-102 (precondition conjunction, every unsatisfied item named),
          C-103 (closed verdict/outcome/reason vocabulary and 0/1/2 exits),
          C-104 (named ``not-applicable``).
          ``contracts/reference-classification.contract.md`` C-301…C-307
          (scan roots, F1/F2/F3 forms, carrier roster, fail-closed
          ``unclassified-reference`` and the resolved = 0 definition).

Fixture trees: ``tests/fixtures/seal-archive/`` — ``clean-pair`` (two slices at
source, clean merge record), ``empty`` (named not-applicable), ``reference-matrix``
(live + dated carriers), ``reference-matrix-unclassified`` (one out-of-roster
carrier), ``partial-pair`` (one slice per side) and ``runtime-present`` (state
records present).

Red-first: this file lands before the ``archive-plan`` body exists; the red
reading lives in ``.specify/specs/100-seal-slice-archive/notes/red-first-evidence.md``.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "seal-archive"

PARENT = "100-fixture-parent"
ALPHA = "100a-fixture-alpha"
BETA = "100b-fixture-beta"
SPEC_REL = ".specify/specs/%s" % PARENT
ALPHA_FROM = ".specify/specs/%s" % ALPHA
BETA_FROM = ".specify/specs/%s" % BETA
ALPHA_TO = "%s/slices/%s" % (SPEC_REL, ALPHA)
BETA_TO = "%s/slices/%s" % (SPEC_REL, BETA)

OUTCOMES = {"would-archive", "archived", "already-archived", "not-applicable"}
ROW_KEYS = {"carrier", "line", "before", "after", "kind"}
RUNTIME_KEYS = {"carrier", "status", "reason", "updates"}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _load_engine():
    assert ENGINE.is_file(), "engine missing: scripts/python/seal-utils.py"
    spec = importlib.util.spec_from_file_location("seal_utils_archive_plan", ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def eng():
    return _load_engine()


def _copy_fixture(name: str, target: Path) -> Path:
    source = FIXTURES / name
    assert source.is_dir(), (
        f"fixture tree missing: {source} — T011/T022 create it before the red run"
    )
    shutil.copytree(source, target)
    return target


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
        "GIT_COMMITTER_NAME": "fixture",
        "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
    })
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=fixture",
         "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
         *args],
        capture_output=True, text=True, encoding="utf-8", check=False, env=env,
    )


def _init_git(repo: Path) -> None:
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    assert _git(repo, "commit", "-qm", "fixture baseline").returncode == 0


def _run_plan(repo: Path, spec: str = PARENT):
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "archive-plan",
         "--spec-dir", str(repo / ".specify" / "specs" / spec),
         "--repo", str(repo), "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.stdout.strip(), (
        f"expected a stdout payload; exit={proc.returncode} stderr={proc.stderr[-800:]!r}"
    )
    return proc, json.loads(proc.stdout)


def _snapshot(root: Path) -> dict:
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*")) if p.is_file()
    }


def _codes(payload: dict) -> list:
    return [c["code"] for c in payload["conditions"]]


def _rows(manifest: dict) -> list:
    return manifest["references"]["rows"]


def _row(manifest: dict, carrier: str, line: int):
    found = [r for r in _rows(manifest)
             if r["carrier"] == carrier and r["line"] == line]
    assert len(found) == 1, f"expected one ledger row for {carrier}:{line}; got {found!r}"
    return found[0]


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# C-102 / C-103 / C-104 — preconditions, verdict vocabulary and exits
# ---------------------------------------------------------------------------

def test_plan_clean_pair_is_would_archive_with_zero_unresolved(tmp_path):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    _init_git(repo)
    proc, payload = _run_plan(repo)
    assert proc.returncode == 0, payload.get("conditions")
    assert payload["verdict"] == "ok"
    assert payload["outcome"] == "would-archive"
    assert payload["outcome"] in OUTCOMES
    archive = payload["archive"]
    assert [m["slug"] for m in archive["moves"]] == [ALPHA, BETA]
    assert [(m["from"], m["to"]) for m in archive["moves"]] == [
        (ALPHA_FROM, ALPHA_TO), (BETA_FROM, BETA_TO)]
    manifest = archive["manifest"]
    checks = manifest["checks"]
    assert checks["preconditions"]["side_presence"] == {
        ALPHA: "source", BETA: "source"}
    assert checks["preconditions"]["merge_status"] == "merged"
    assert checks["preconditions"]["open_conflicts"] == 0
    assert checks["preconditions"]["slices_closed"] is True
    assert checks["preconditions"]["dirty_spec_tree"] is False
    assert checks["unresolved_before"] == 0
    assert checks["unresolved_after"] == 0
    assert checks["unclassified"] == 0
    assert archive["unresolved_before"] == archive["unresolved_after"] == 0
    assert manifest["slices"][0]["merged_into_pointer"]["line"] > 0


def test_plan_is_read_only_and_never_writes_the_manifest(tmp_path):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    _init_git(repo)
    before = _snapshot(repo)
    _run_plan(repo)
    assert _snapshot(repo) == before, (
        "C-103: archive-plan is read-only — no manifest, no ledger, no reject record"
    )
    assert not (repo / SPEC_REL / "archive-manifest.json").exists()


def test_plan_empty_slice_set_is_named_not_applicable(tmp_path):
    repo = _copy_fixture("empty", tmp_path / "repo")
    _init_git(repo)
    proc, payload = _run_plan(repo, "100-fixture-empty")
    assert proc.returncode == 0, payload.get("conditions")
    assert payload["verdict"] == "ok"
    assert payload["outcome"] == "not-applicable"
    assert "empty by construction" in payload["archive"]["basis"], (
        "C-104: the basis MUST come from the merge manifest, not a bare 'no slices'"
    )
    assert payload["archive"]["manifest"] is None
    assert not (repo / ".specify" / "specs" / "100-fixture-empty"
                / "archive-manifest.json").exists()


def _mutate_manifest(repo: Path, mutate) -> None:
    path = repo / SPEC_REL / "merge-manifest.json"
    document = _read_json(path)
    mutate(document)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")


def test_plan_names_every_unsatisfied_precondition(tmp_path):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    _init_git(repo)
    _mutate_manifest(repo, lambda d: d["conflicts"].append(
        {"id": "fixture-conflict", "status": "open"}))
    (repo / ".specify/specs" / ALPHA / "tasks.md").write_text(
        "# Tasks: fixture alpha\n\n- [ ] T001 Alpha open task.\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "inject conflict and open row")
    (repo / SPEC_REL / "requirements.md").write_text(
        "# Requirements: fixture parent\n\n- **FR-002**: uncommitted edit.\n",
        encoding="utf-8")
    proc, payload = _run_plan(repo)
    assert proc.returncode == 1, payload.get("conditions")
    assert payload["verdict"] == "refused"
    assert payload["outcome"] is None
    codes = set(_codes(payload))
    assert {"conflict-open", "slice-unclosed", "dirty-spec-tree"} <= codes, (
        "C-102: all unsatisfied conditions are named in one report, never only the first"
    )
    for condition in payload["conditions"]:
        assert set(condition) == {"code", "evidence", "fix_path", "rerun"}


def test_plan_same_slice_on_both_sides_refuses_destination_exists(tmp_path):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    _init_git(repo)
    target = repo / SPEC_REL / "slices" / BETA
    target.parent.mkdir(parents=True)
    shutil.copytree(repo / ".specify/specs" / BETA, target)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "duplicate beta on both sides")
    before = _snapshot(repo)
    proc, payload = _run_plan(repo)
    assert proc.returncode == 1, payload.get("conditions")
    assert payload["verdict"] == "refused"
    assert _codes(payload) == ["destination-exists"]
    assert BETA in json.dumps(payload["conditions"], ensure_ascii=False)
    assert _snapshot(repo) == before, "C-103: a refusal writes nothing"


def test_plan_missing_slice_is_an_input_error(tmp_path):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    _init_git(repo)
    shutil.rmtree(repo / ".specify/specs" / BETA)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "drop beta")
    proc, payload = _run_plan(repo)
    assert proc.returncode == 2, payload.get("conditions")
    assert payload["verdict"] == "error"
    assert "slice-missing" in _codes(payload)


def test_plan_partial_pair_is_an_input_error(tmp_path):
    repo = _copy_fixture("partial-pair", tmp_path / "repo")
    _init_git(repo)
    before = _snapshot(repo)
    proc, payload = _run_plan(repo)
    assert proc.returncode == 2, payload.get("conditions")
    assert payload["verdict"] == "error"
    assert "partial-archive" in _codes(payload), (
        "C-102 ⑤: a slice split across the two sides is an input defect, never a guess"
    )
    assert _snapshot(repo) == before


def test_plan_reports_input_defects_and_refusals_together_with_exit_two(tmp_path):
    repo = _copy_fixture("partial-pair", tmp_path / "repo")
    _init_git(repo)
    _mutate_manifest(repo, lambda d: d["conflicts"].append(
        {"id": "fixture-conflict", "status": "open"}))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "inject conflict")
    proc, payload = _run_plan(repo)
    assert proc.returncode == 2, payload.get("conditions")
    codes = set(_codes(payload))
    assert {"conflict-open", "partial-archive"} <= codes, (
        "C-102: an input defect wins the single exit code while every item stays named"
    )


def test_plan_runs_on_a_spec_whose_seal_judgment_is_blocked(tmp_path):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    _init_git(repo)
    seal = repo / SPEC_REL / "seal.md"
    assert "blocked" in seal.read_text(encoding="utf-8")
    proc, payload = _run_plan(repo)
    assert proc.returncode == 0, payload.get("conditions")
    assert payload["outcome"] == "would-archive", (
        "C-107/FR-001: archive is available at Sealed or at any named blocking state"
    )


def test_plan_verdict_outcome_and_reason_domains_are_closed(eng):
    assert tuple(eng.ARCHIVE_OUTCOMES) == (
        "would-archive", "archived", "already-archived", "not-applicable")
    assert set(eng.ARCHIVE_REFUSAL_REASONS) == {
        "destination-exists", "dirty-spec-tree", "conflict-open", "slice-unclosed",
        "unresolved-references", "unclassified-reference"}
    assert set(eng.ARCHIVE_ERROR_REASONS) == {
        "merge-manifest-missing", "merge-manifest-invalid", "slice-missing",
        "partial-archive", "archive-drift", "archive-manifest-invalid",
        "not-a-git-tree", "mirror-copy", "write-failed"}


def test_plan_refuses_outside_a_git_work_tree(tmp_path):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    proc, payload = _run_plan(repo)
    assert proc.returncode == 2
    assert "not-a-git-tree" in _codes(payload)


# ---------------------------------------------------------------------------
# C-301 … C-307 — carrier roster, classification and fail-closed resolution
# ---------------------------------------------------------------------------

def test_reference_matrix_classifies_live_and_dated_carriers(tmp_path):
    repo = _copy_fixture("reference-matrix", tmp_path / "repo")
    _init_git(repo)
    proc, payload = _run_plan(repo)
    assert proc.returncode == 0, payload.get("conditions")
    manifest = payload["archive"]["manifest"]
    rows = _rows(manifest)
    assert all(set(row) == ROW_KEYS for row in rows)
    assert all(row["kind"] in ("live-rewrite", "dated-preserved") for row in rows)
    by_carrier = {}
    for row in rows:
        by_carrier.setdefault(row["carrier"], []).append(row)

    register = ".specify/register.md"
    assert [r["kind"] for r in by_carrier[register]] == ["live-rewrite"]
    assert ALPHA_TO in by_carrier[register][0]["after"]

    plan = by_carrier[SPEC_REL + "/plan.md"]
    assert [r["kind"] for r in plan] == ["live-rewrite", "live-rewrite"]
    assert plan[1]["before"].startswith("The sibling shorthand is ")
    assert "slices/%s/" % BETA in plan[1]["after"]

    detail = ".specify/features/100-fixture-parent.md"
    sections = {r["line"]: r["kind"] for r in by_carrier[detail]}
    assert sections[5] == "dated-preserved"
    assert sections[9] == "live-rewrite"
    assert sections[10] == "live-rewrite"
    assert sections[14] == "dated-preserved", (
        "C-304: only `## Related Specifications/Requirements` is live"
    )

    dated_carriers = {
        SPEC_REL + "/notes/note.md", SPEC_REL + "/test-evidence/evidence.txt",
        SPEC_REL + "/checklists/checklist.md", ".specify/features.md",
        ".specify/memory/session/entry.md", ".specify/history/topic.md",
        ".specify/specs/%s/notes.md" % ALPHA, ".specify/specs/%s/notes.md" % BETA,
    }
    for carrier in dated_carriers:
        assert carrier in by_carrier, f"declared dated carrier missing: {carrier}"
        for row in by_carrier[carrier]:
            assert row["kind"] == "dated-preserved"
            assert row["before"] == row["after"], (
                "C-306/C-308: dated records keep their bytes"
            )

    assert SPEC_REL + "/seal.md" not in by_carrier, (
        "C-303: the parent seal.md is owned by seal and MUST NOT be rewritten"
    )

    shared = by_carrier["shared/definitions/example.md"][0]
    mirror = by_carrier[".specify/shared/definitions/example.md"][0]
    assert shared["kind"] == mirror["kind"] == "live-rewrite"
    assert shared["after"] == mirror["after"], (
        "C-310: source and mirror are rewritten to the same text in one batch"
    )

    tests_rows = by_carrier["tests/contract/test_fixture_refs.py"]
    f3 = [r for r in tests_rows if "SLICE_DIR" in r["before"]][0]
    assert f3["kind"] == "live-rewrite"
    assert "%s/slices/%s" % (PARENT, ALPHA) in f3["after"]
    identity = [r for r in tests_rows if "assert make(" in r["before"]][0]
    assert identity["after"].endswith('== "100b-fixture-beta"'), (
        "C-302/C-311: an identity literal on the right of `==` is not a path reference"
    )

    manifest_rows = by_carrier[SPEC_REL + "/merge-manifest.json"]
    assert len(manifest_rows) == 2, (
        "C-301: only the merge manifest's path-form string values are live hits"
    )
    assert all(r["kind"] == "live-rewrite" for r in manifest_rows)
    assert all("/slices/" in r["after"] for r in manifest_rows)

    checks = manifest["checks"]
    assert checks["live_rewrite"] + checks["dated_preserved"] == len(rows)
    assert checks["unresolved_before"] == 0
    assert checks["unresolved_after"] == 0
    assert checks["unclassified"] == 0


def test_unclassified_carrier_refuses_before_any_write(tmp_path):
    repo = _copy_fixture("reference-matrix-unclassified", tmp_path / "repo")
    _init_git(repo)
    before = _snapshot(repo)
    proc, payload = _run_plan(repo)
    assert proc.returncode == 1, payload.get("conditions")
    assert payload["verdict"] == "refused"
    assert payload["outcome"] is None
    assert "unclassified-reference" in _codes(payload)
    evidence = json.dumps(payload["conditions"], ensure_ascii=False)
    assert "unsorted/random.md" in evidence, (
        "C-305: the out-of-roster carrier is named with its line"
    )
    assert _snapshot(repo) == before


def test_injected_dangling_live_reference_refuses_unresolved(tmp_path):
    repo = _copy_fixture("reference-matrix", tmp_path / "repo")
    _init_git(repo)
    register = repo / ".specify" / "register.md"
    register.write_text(
        register.read_text(encoding="utf-8")
        + "- Dangling: `.specify/specs/%s/missing.md`\n" % ALPHA,
        encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "inject dangling live reference")
    proc, payload = _run_plan(repo)
    assert proc.returncode == 1, payload.get("conditions")
    assert "unresolved-references" in _codes(payload), (
        "C-307: a live reference whose target will not exist fails closed"
    )


def test_removing_one_mapping_leaves_dated_references_unresolved(eng):
    path = ".specify/specs/%s/tasks.md" % BETA
    both = [{"from": ALPHA_FROM, "to": ALPHA_TO},
            {"from": BETA_FROM, "to": BETA_TO}]
    assert eng.map_archived_reference(path, both) == (BETA_TO + "/tasks.md", BETA)
    assert eng.map_archived_reference(path, both[:1]) == (None, None), (
        "C-210/C-306(d): removing a `from -> to` mapping turns the dated hit "
        "unresolved; no second mapping table exists"
    )


def test_runtime_carriers_present_and_absent_are_both_named(tmp_path):
    repo = _copy_fixture("runtime-present", tmp_path / "repo")
    _init_git(repo)
    proc, payload = _run_plan(repo)
    assert proc.returncode == 0, payload.get("conditions")
    manifest = payload["archive"]["manifest"]
    runtime = manifest["references"]["runtime"]
    assert all(set(row) == RUNTIME_KEYS for row in runtime)
    assert [row["carrier"] for row in runtime] == [
        ".specify/state/%s.md" % PARENT,
        ".specify/state/%s.md" % ALPHA,
        ".specify/state/%s.md" % BETA,
    ]
    assert [row["status"] for row in runtime] == [
        "runtime-updated", "runtime-updated", "absent"]
    parent, alpha, beta = runtime
    assert parent["reason"] is None and parent["updates"], (
        "C-309: an existing record with a hit records its line update"
    )
    assert alpha["updates"] and alpha["updates"][0]["line"] > 0
    assert beta["status"] == "absent" and beta["reason"] and beta["updates"] == []
    checks = manifest["checks"]
    assert checks["runtime_carriers"] == 3
    assert sum(1 for row in runtime if row["status"] == "runtime-updated") \
        + sum(1 for row in runtime if row["status"] == "absent") \
        == checks["runtime_carriers"]
    assert ALPHA_TO in parent["updates"][0]["after"]


def test_reference_matrix_without_state_records_reports_three_absent(tmp_path):
    repo = _copy_fixture("reference-matrix", tmp_path / "repo")
    _init_git(repo)
    proc, payload = _run_plan(repo)
    assert proc.returncode == 0, payload.get("conditions")
    runtime = payload["archive"]["manifest"]["references"]["runtime"]
    assert [row["status"] for row in runtime] == ["runtime-updated", "absent", "absent"]
    assert runtime[0]["updates"] == [], (
        "C-205: an existing record with zero hits is still `runtime-updated`"
    )


def test_plan_is_byte_stable_across_two_runs(tmp_path):
    repo = _copy_fixture("reference-matrix", tmp_path / "repo")
    _init_git(repo)
    first, _ = _run_plan(repo)
    second, _ = _run_plan(repo)
    assert first.stdout == second.stdout, (
        "C-208/SC-006: the same input reproduces the same plan byte for byte"
    )


def test_plan_previews_the_merge_manifest_path_amendments(tmp_path, eng):
    repo = _copy_fixture("reference-matrix", tmp_path / "repo")
    _init_git(repo)
    merge_path = repo / SPEC_REL / "merge-manifest.json"
    original = _read_json(merge_path)
    proc, payload = _run_plan(repo)
    assert proc.returncode == 0, payload.get("conditions")
    archive = payload["archive"]
    amendments = archive["merge_amendments"]
    assert {(a["before"], a["after"]) for a in amendments} == {
        (ALPHA_FROM + "/tasks.md", ALPHA_TO + "/tasks.md"),
        (BETA_FROM + "/tasks.md", BETA_TO + "/tasks.md"),
    }
    recorded = archive["manifest"]["merge_manifest"]
    assert recorded["path"] == "merge-manifest.json"
    assert recorded["digest_before"] == eng.archive_manifest_digest(original)
    amended = eng.amended_merge_document(
        original,
        [{"slug": ALPHA, "from": ALPHA_FROM, "to": ALPHA_TO},
         {"slug": BETA, "from": BETA_FROM, "to": BETA_TO}])["document"]
    assert recorded["digest_after"] == eng.archive_manifest_digest(amended)
