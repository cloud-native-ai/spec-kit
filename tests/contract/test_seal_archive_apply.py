"""Contract tests for the seal engine's ``archive-apply`` action (Feature 100, P4).

Contract: ``.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md``
          C-105 (already-archived is idempotent success), C-106 (pure move: one
          rename pair per file, zero deletions, never a plain ``mv``),
          C-108 (two-phase execution, batch write, byte-for-byte restore on
          failure), ``contracts/reference-classification.contract.md`` C-308…
          C-311 (live rewrites, dated byte stability, runtime carriers,
          source/mirror pairing, test-construction lines).

Fixture trees: ``tests/fixtures/seal-archive/`` — ``clean-pair`` (two slices at
source, no external live carriers), ``reference-matrix`` (live + dated
carriers), ``runtime-present`` (state records present).

Red-first: this file lands before the ``archive-apply`` body exists; the red
reading lives in ``.specify/specs/100-seal-slice-archive/notes/red-first-evidence.md``.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import types
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
MANIFEST_REL = SPEC_REL + "/archive-manifest.json"
MERGE_REL = SPEC_REL + "/merge-manifest.json"

TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _load_engine():
    assert ENGINE.is_file(), "engine missing: scripts/python/seal-utils.py"
    spec = importlib.util.spec_from_file_location("seal_utils_archive_apply", ENGINE)
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
    assert source.is_dir(), f"fixture tree missing: {source}"
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


def _run(repo: Path, action: str) -> tuple[subprocess.CompletedProcess, dict]:
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", action,
         "--spec-dir", str(repo / SPEC_REL), "--repo", str(repo), "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.stdout.strip(), (
        f"expected a stdout payload for {action}; exit={proc.returncode} "
        f"stderr={proc.stderr[-800:]!r}"
    )
    return proc, json.loads(proc.stdout)


def _snapshot(root: Path) -> dict:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }


def _file_rows(directory: Path) -> list:
    return [
        {"path": path.relative_to(directory).as_posix(),
         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in sorted(directory.rglob("*")) if path.is_file()
    ]


def _status(repo: Path) -> str:
    proc = _git(repo, "status", "--porcelain")
    assert proc.returncode == 0, proc.stderr[-400:]
    return proc.stdout


def _codes(payload: dict) -> list:
    return [condition["code"] for condition in payload["conditions"]]


def _canonical(value) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=True,
                      ensure_ascii=False)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _name_status(repo: Path, commit: str) -> list:
    proc = _git(repo, "diff", "--name-status", "-M", commit)
    assert proc.returncode == 0, proc.stderr[-400:]
    rows = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if parts[0].startswith("R") and len(parts) == 3:
            rows.append(("R", parts[1], parts[2]))
        elif len(parts) == 2:
            rows.append((parts[0], parts[1], None))
    return rows


def _apply_in_process(eng, repo: Path):
    spec_dir = (repo / SPEC_REL).resolve()
    return eng.action_archive_apply(types.SimpleNamespace(repo=str(repo)), spec_dir)


# ---------------------------------------------------------------------------
# C-105 / C-106 / C-108 — the successful apply batch
# ---------------------------------------------------------------------------

def test_apply_moves_every_slice_and_lands_the_manifest(tmp_path):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    _init_git(repo)
    before = {slug: _file_rows(repo / ".specify/specs" / slug)
              for slug in (ALPHA, BETA)}

    plan_proc, plan_payload = _run(repo, "archive-plan")
    assert plan_proc.returncode == 0, plan_payload.get("conditions")
    candidate = plan_payload["archive"]["manifest"]
    pinned = candidate["pinned_commit"]

    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 0, payload.get("conditions")
    assert payload["verdict"] == "ok"
    assert payload["outcome"] == "archived"
    assert [(m["from"], m["to"]) for m in payload["archive"]["moves"]] == [
        (ALPHA_FROM, ALPHA_TO), (BETA_FROM, BETA_TO)]

    assert plan_payload["archive"]["manifest"] == payload["archive"]["manifest"], (
        "C-108: the apply read-only stage recomputes exactly the plan's candidate"
    )
    assert _sha256(_canonical(plan_payload["archive"]["manifest"])) == \
        _sha256(_canonical(payload["archive"]["manifest"]))

    manifest_path = repo / MANIFEST_REL
    assert manifest_path.is_file()
    assert manifest_path.read_text(encoding="utf-8") == json.dumps(
        payload["archive"]["manifest"], indent=2, sort_keys=True,
        ensure_ascii=False) + "\n", "C-202: the record lands in its canonical form"
    assert payload["archive"]["manifest"]["checks"]["files_match"] is True

    for slug in (ALPHA, BETA):
        destination = repo / (SPEC_REL + "/slices/" + slug)
        assert _file_rows(destination) == before[slug], (
            "FR-004: file count, per-file sha256 and relative paths are unchanged"
        )
        assert not (repo / ".specify/specs" / slug).exists()

    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == pinned, (
        "C-207: apply MUST NOT commit the batch"
    )
    _git(repo, "add", "-A")
    rows = _name_status(repo, pinned)
    assert not [row for row in rows if row[0] == "D"], (
        "C-106: the archive batch never shows a plain deletion"
    )
    expected_renames = {
        (".specify/specs/%s/%s" % (slug, item["path"]),
         "%s/slices/%s/%s" % (SPEC_REL, slug, item["path"]))
        for slug, files in before.items() for item in files
    }
    assert {(row[1], row[2]) for row in rows if row[0] == "R"} == expected_renames
    assert {row[1] for row in rows if row[0] == "A"} == {MANIFEST_REL}
    assert {row[1] for row in rows if row[0] == "M"} == {MERGE_REL}


def test_apply_rewrites_live_carriers_and_preserves_dated_bytes(tmp_path):
    repo = _copy_fixture("reference-matrix", tmp_path / "repo")
    _init_git(repo)
    before = _snapshot(repo)
    plan_proc, plan_payload = _run(repo, "archive-plan")
    assert plan_proc.returncode == 0, plan_payload.get("conditions")
    manifest = plan_payload["archive"]["manifest"]
    rows = manifest["references"]["rows"]
    live = [row for row in rows if row["kind"] == "live-rewrite"]
    dated = [row for row in rows if row["kind"] == "dated-preserved"]
    live_carriers = {row["carrier"] for row in live}
    dated_carriers = {row["carrier"] for row in dated} - live_carriers
    assert live_carriers and dated_carriers, "fixture must exercise both kinds"

    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 0, payload.get("conditions")
    assert payload["outcome"] == "archived"

    for row in live:
        lines = (repo / row["carrier"]).read_text(encoding="utf-8").splitlines()
        assert lines[row["line"] - 1] == row["after"], (
            "C-308: the live line is rewritten to its recorded after text"
        )
    for carrier in dated_carriers:
        located = repo / carrier
        for entry in manifest["slices"]:
            if carrier.startswith(entry["from"] + "/"):
                located = repo / (entry["to"] + carrier[len(entry["from"]):])
        assert hashlib.sha256(located.read_bytes()).hexdigest() == before[carrier], (
            "C-308: dated carriers keep their original bytes, at their archived "
            "path when they live inside a moved slice"
        )
    assert (repo / SPEC_REL / "seal.md").read_bytes() == \
        (FIXTURES / "reference-matrix" / SPEC_REL / "seal.md").read_bytes(), (
        "C-301/C-304: the parent seal.md is not a live carrier and is never rewritten"
    )

    pinned = manifest["pinned_commit"]
    _git(repo, "add", "-A")
    rows_diff = _name_status(repo, pinned)
    modified = {row[1] for row in rows_diff if row[0] == "M"}
    assert modified == live_carriers | {MERGE_REL}, (
        "C-106: the M set is exactly the declared live carriers plus the merge manifest"
    )
    assert {row[1] for row in rows_diff if row[0] == "A"} == {MANIFEST_REL}
    assert not [row for row in rows_diff if row[0] == "D"]


def test_a_source_mirror_mismatch_ends_with_mirror_copy_and_restores(tmp_path):
    repo = _copy_fixture("reference-matrix", tmp_path / "repo")
    mirror = repo / ".specify/shared/definitions/example.md"
    mirror.write_text(mirror.read_text(encoding="utf-8") + "\nmirror-only line\n",
                      encoding="utf-8")
    _init_git(repo)
    before = _snapshot(repo)

    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 2, payload.get("conditions")
    assert "mirror-copy" in _codes(payload), (
        "C-310: a source/mirror pair that no longer agrees is an input error, "
        "not a generic write failure"
    )
    assert _snapshot(repo) == before, (
        "C-310: the batch is restored byte for byte before the error is reported"
    )
    assert _status(repo) == ""
    assert not (repo / MANIFEST_REL).exists()


# ---------------------------------------------------------------------------
# C-105 — already-archived, manifest invalid, non-git
# ---------------------------------------------------------------------------

def test_second_apply_reports_already_archived_with_zero_diff(tmp_path):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    _init_git(repo)
    first_proc, first_payload = _run(repo, "archive-apply")
    assert first_proc.returncode == 0, first_payload.get("conditions")
    manifest_bytes = (repo / MANIFEST_REL).read_bytes()
    snapshot = _snapshot(repo)
    status = _status(repo)

    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 0, payload.get("conditions")
    assert payload["verdict"] == "ok"
    assert payload["outcome"] == "already-archived"
    assert payload["archive"]["moves"] == []
    assert _snapshot(repo) == snapshot, (
        "C-105: a rerun moves nothing, rewrites nothing and writes no second manifest"
    )
    assert _status(repo) == status
    assert (repo / MANIFEST_REL).read_bytes() == manifest_bytes


def test_unparsable_record_is_an_input_error_not_already_archived(tmp_path):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    _init_git(repo)
    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 0, payload.get("conditions")
    (repo / MANIFEST_REL).write_text("{not json\n", encoding="utf-8")
    before = _snapshot(repo)

    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 2, payload.get("conditions")
    assert payload["verdict"] == "error"
    assert "archive-manifest-invalid" in _codes(payload)
    assert _snapshot(repo) == before, (
        "C-105: an unreadable record is never read as already-archived and "
        "MUST leave the tree untouched"
    )


def test_apply_outside_a_git_tree_refuses_with_exit_two(tmp_path):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    before = _snapshot(repo)

    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 2, payload.get("conditions")
    assert payload["verdict"] == "error"
    assert "not-a-git-tree" in _codes(payload), (
        "C-106: the engine never degrades to a plain mv outside a work tree"
    )
    assert _snapshot(repo) == before


def test_refused_apply_persists_nothing(tmp_path):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    _init_git(repo)
    (repo / SPEC_REL / "requirements.md").write_text(
        "# Requirements: fixture parent\n\n- **FR-009**: uncommitted edit.\n",
        encoding="utf-8")
    before = _snapshot(repo)

    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 1, payload.get("conditions")
    assert payload["verdict"] == "refused"
    assert payload["outcome"] is None
    assert "dirty-spec-tree" in _codes(payload)
    assert _snapshot(repo) == before, (
        "C-103: a refusal writes no record, no empty manifest and no ledger"
    )


# ---------------------------------------------------------------------------
# C-309 — runtime carriers: present is updated, absent never blocks
# ---------------------------------------------------------------------------

def test_runtime_carriers_are_updated_and_absence_does_not_block(tmp_path):
    repo = _copy_fixture("runtime-present", tmp_path / "repo")
    _init_git(repo)
    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 0, payload.get("conditions")
    assert payload["outcome"] == "archived"
    runtime = payload["archive"]["manifest"]["references"]["runtime"]
    assert [row["status"] for row in runtime] == [
        "runtime-updated", "runtime-updated", "absent"]
    parent_state = (repo / (".specify/state/%s.md" % PARENT)).read_text(
        encoding="utf-8")
    assert "%s/slices/%s/plan.md" % (SPEC_REL, ALPHA) in parent_state, (
        "C-309: a present runtime record is rewritten in the same batch"
    )
    alpha_state = (repo / (".specify/state/%s.md" % ALPHA)).read_text(
        encoding="utf-8")
    assert "%s/slices/%s/tasks.md" % (SPEC_REL, ALPHA) in alpha_state
    assert not (repo / (".specify/state/%s.md" % BETA)).exists()
    assert payload["archive"]["manifest"]["checks"]["runtime_carriers"] == 3


# ---------------------------------------------------------------------------
# C-108 — a failed batch restores every original byte
# ---------------------------------------------------------------------------

def test_a_corrupted_move_is_detected_and_the_batch_is_restored(tmp_path, eng,
                                                                monkeypatch):
    repo = _copy_fixture("clean-pair", tmp_path / "repo")
    _init_git(repo)
    before = _snapshot(repo)
    original_move = eng._archive_move
    calls = {"count": 0}

    def corrupting_move(repo_path, source_rel, destination_rel):
        original_move(repo_path, source_rel, destination_rel)
        calls["count"] += 1
        if calls["count"] == 1:
            target = repo_path / destination_rel / "tasks.md"
            target.write_text(target.read_text(encoding="utf-8") + "mutated\n",
                              encoding="utf-8")

    monkeypatch.setattr(eng, "_archive_move", corrupting_move)
    payload, code = _apply_in_process(eng, repo)
    assert code == 2, payload.get("conditions")
    assert payload["verdict"] == "error"
    assert "write-failed" in _codes(payload), (
        "FR-004: a content mutation turns the zero-loss hash check red and the "
        "batch ends with write-failed"
    )
    assert _snapshot(repo) == before, (
        "C-108: the moved directories are restored by their original bytes"
    )
    assert _status(repo) == "", "the restored index is clean again"
    assert not (repo / MANIFEST_REL).exists()
    assert not (repo / SPEC_REL / "slices").exists()


def test_a_carrier_write_failure_restores_moves_and_rewrites(tmp_path, eng,
                                                             monkeypatch):
    repo = _copy_fixture("reference-matrix", tmp_path / "repo")
    _init_git(repo)
    before = _snapshot(repo)
    original_write = eng._archive_write_text

    def failing_write(path, text):
        if Path(path).name == "register.md":
            raise OSError("injected: register.md is unwritable")
        return original_write(path, text)

    monkeypatch.setattr(eng, "_archive_write_text", failing_write)
    payload, code = _apply_in_process(eng, repo)
    assert code == 2, payload.get("conditions")
    assert "write-failed" in _codes(payload)
    assert _snapshot(repo) == before, (
        "C-108: every rewritten carrier, the merge manifest and the moved "
        "directories are restored byte for byte"
    )
    assert _status(repo) == ""
    assert not (repo / MANIFEST_REL).exists()
    assert not (repo / SPEC_REL / "slices").exists()
