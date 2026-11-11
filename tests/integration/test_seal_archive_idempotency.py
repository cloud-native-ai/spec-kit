"""Integration tests for archive idempotency and determinism (Feature 100, P4).

Contract: ``.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md``
          C-105 (already-archived is idempotent success), C-109 (determinism is
          a hard constraint: byte-identical plans, declared sort keys only,
          zero diff on rerun), ``contracts/archive-manifest.contract.md``
          C-208 (same input, same bytes).

The replay tree is a throwaway copy of ``tests/fixtures/seal-archive/`` under
``tmp_path``; the live repository is never written.
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

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "seal-archive"

PARENT = "100-fixture-parent"
ALPHA = "100a-fixture-alpha"
BETA = "100b-fixture-beta"
SPEC_REL = ".specify/specs/%s" % PARENT
MANIFEST_REL = SPEC_REL + "/archive-manifest.json"

TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _load_engine():
    spec = importlib.util.spec_from_file_location("seal_utils_archive_idem", ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def eng():
    return _load_engine()


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


def _replay(tmp_path: Path, fixture: str = "clean-pair") -> Path:
    repo = tmp_path / "repo"
    shutil.copytree(FIXTURES / fixture, repo)
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    assert _git(repo, "commit", "-qm", "fixture baseline").returncode == 0
    return repo


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


def _status(repo: Path) -> str:
    return _git(repo, "status", "--porcelain").stdout


def _canonical(value) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=True,
                      ensure_ascii=False)


def _codes(payload: dict) -> list:
    return [condition["code"] for condition in payload["conditions"]]


# ---------------------------------------------------------------------------
# C-105 / SC-002 — rerun is idempotent
# ---------------------------------------------------------------------------

def test_second_apply_is_already_archived_with_zero_new_diff(tmp_path):
    repo = _replay(tmp_path)
    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 0, payload.get("conditions")
    assert payload["outcome"] == "archived"
    manifest = (repo / MANIFEST_REL).read_bytes()
    snapshot = _snapshot(repo)
    status = _status(repo)

    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 0, payload.get("conditions")
    assert payload["verdict"] == "ok"
    assert payload["outcome"] == "already-archived"
    assert payload["archive"]["moves"] == []
    assert _snapshot(repo) == snapshot, "C-105: the rerun adds no diff"
    assert _status(repo) == status
    assert (repo / MANIFEST_REL).read_bytes() == manifest, (
        "C-105: no second manifest and no repeated rewrite"
    )


def test_plan_on_the_archived_tree_reports_zero_moves_and_zero_unresolved(tmp_path):
    repo = _replay(tmp_path)
    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 0, payload.get("conditions")

    proc, payload = _run(repo, "archive-plan")
    assert proc.returncode == 0, payload.get("conditions")
    assert payload["outcome"] == "already-archived"
    archive = payload["archive"]
    assert archive["moves"] == []
    assert archive["unresolved_before"] == archive["unresolved_after"] == 0
    assert archive["unclassified"] == 0
    assert archive["manifest"]["checks"]["files_match"] is True


# ---------------------------------------------------------------------------
# SC-002 / FR-004 — an injected content mutation turns the hash check red
# ---------------------------------------------------------------------------

def test_a_content_mutation_is_caught_by_the_hash_check_and_restored(tmp_path, eng,
                                                                    monkeypatch):
    repo = _replay(tmp_path)
    before = _snapshot(repo)
    original_move = eng._archive_move
    calls = {"count": 0}

    def mutating_move(repo_path, source_rel, destination_rel):
        original_move(repo_path, source_rel, destination_rel)
        calls["count"] += 1
        if calls["count"] == 2:
            target = repo_path / destination_rel / "requirements.md"
            target.write_text(target.read_text(encoding="utf-8") + "mutated\n",
                              encoding="utf-8")

    monkeypatch.setattr(eng, "_archive_move", mutating_move)
    spec_dir = (repo / SPEC_REL).resolve()
    payload, code = eng.action_archive_apply(
        types.SimpleNamespace(repo=str(repo)), spec_dir)
    assert code == 2, payload.get("conditions")
    assert "write-failed" in _codes(payload), (
        "SC-002: the zero-loss hash check is the guard that turns red here"
    )
    assert _snapshot(repo) == before, (
        "C-108: the whole batch — moves and rewrites — is restored from the "
        "pinned commit and the recorded original bytes"
    )
    assert _status(repo) == ""
    assert not (repo / MANIFEST_REL).exists()


# ---------------------------------------------------------------------------
# C-109 / C-208 — determinism
# ---------------------------------------------------------------------------

def test_two_plans_are_byte_identical(tmp_path):
    repo = _replay(tmp_path, "reference-matrix")
    first_proc, first_payload = _run(repo, "archive-plan")
    second_proc, second_payload = _run(repo, "archive-plan")
    assert first_proc.returncode == second_proc.returncode == 0
    assert hashlib.sha256(first_proc.stdout.encode("utf-8")).hexdigest() \
        == hashlib.sha256(second_proc.stdout.encode("utf-8")).hexdigest(), (
        "C-208: the same input reproduces the same plan byte for byte"
    )
    assert _canonical(first_payload["archive"]["manifest"]) \
        == _canonical(second_payload["archive"]["manifest"])


def test_sort_keys_use_only_the_declared_fields(tmp_path):
    repo = _replay(tmp_path, "reference-matrix")
    proc, payload = _run(repo, "archive-plan")
    assert proc.returncode == 0, payload.get("conditions")
    manifest = payload["archive"]["manifest"]
    orders = [entry["order"] for entry in manifest["slices"]]
    assert orders == sorted(orders) == list(range(1, len(orders) + 1)), (
        "C-203: slices are ordered by their declared contiguous order value"
    )
    for entry in manifest["slices"]:
        paths = [row["path"] for row in entry["files"]]
        assert paths == sorted(paths), "C-203: files are sorted by path"
    row_keys = [(row["carrier"], row["line"])
                for row in manifest["references"]["rows"]]
    assert row_keys == sorted(row_keys), (
        "C-204: ledger rows are sorted by (carrier, line)"
    )
    serialized = json.dumps(manifest, sort_keys=True, ensure_ascii=False)
    assert not TIMESTAMP_RE.search(serialized), (
        "C-207: no wall-clock field may decide any ordering or value"
    )
    assert '".."' not in serialized and ':\\' not in serialized


def test_reversing_enumeration_order_keeps_the_candidate_identical(tmp_path, eng,
                                                                   monkeypatch):
    repo = _replay(tmp_path, "reference-matrix")
    spec_dir = (repo / SPEC_REL).resolve()
    baseline, code = eng.action_archive_plan(
        types.SimpleNamespace(repo=str(repo)), spec_dir)
    assert code == 0, baseline.get("conditions")
    original = eng._discover_slices

    def reversed_discovery(spec_dir_arg, repo_arg):
        slices, excluded = original(spec_dir_arg, repo_arg)
        return list(reversed(slices)), excluded

    monkeypatch.setattr(eng, "_discover_slices", reversed_discovery)
    mutated, code = eng.action_archive_plan(
        types.SimpleNamespace(repo=str(repo)), spec_dir)
    assert code == 0, mutated.get("conditions")
    assert _canonical(mutated["archive"]["manifest"]) \
        == _canonical(baseline["archive"]["manifest"]), (
        "C-109: if any step sorted by directory enumeration order, reversing "
        "the discovery order would change the plan — the test would go red"
    )


def test_apply_success_leaves_a_clean_rerun_and_no_second_plan(tmp_path):
    repo = _replay(tmp_path)
    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 0, payload.get("conditions")
    status = _status(repo)
    assert status.strip(), (
        "the archive batch is expected to be staged by git mv; the flow commits it"
    )
    _git(repo, "add", "-A")
    assert _git(repo, "commit", "-qm", "archive batch").returncode == 0
    assert _status(repo) == ""
    before = _snapshot(repo)
    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 0 and payload["outcome"] == "already-archived"
    assert _status(repo) == ""
    assert _snapshot(repo) == before
