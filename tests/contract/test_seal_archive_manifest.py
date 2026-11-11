"""Contract tests for the archive manifest candidate (Feature 100, P3).

Contract: ``.specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md``
          C-201…C-212 — fixed name/place, closed key sets at every level,
          serialization, per-field path basis, C-034 digest, closed checks and
          the three closure arithmetic families, determinism, the single shared
          validator, the unique path mapping and schema-version discipline.

Fixture trees: ``tests/fixtures/seal-archive/clean-pair`` and ``reference-matrix``.
The candidate is only ever previewed: ``archive-plan`` writes nothing (C-202).

Red-first: this file lands before the manifest builder exists; the red reading
lives in ``.specify/specs/100-seal-slice-archive/notes/red-first-evidence.md``
(SC-007's first-red host).
"""

from __future__ import annotations

import copy
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

TOP_KEYS = {
    "schema_version", "spec", "spec_path", "generated_by", "pinned_commit",
    "order_basis", "order_source", "slices", "references", "merge_manifest",
    "checks", "digest",
}
GENERATED_KEYS = {"engine", "version", "command"}
SLICE_KEYS = {"slug", "from", "to", "order", "file_count", "files",
              "merged_into_pointer"}
FILE_KEYS = {"path", "sha256"}
POINTER_KEYS = {"path", "line"}
REFERENCES_KEYS = {"rows", "runtime"}
ROW_KEYS = {"carrier", "line", "before", "after", "kind"}
RUNTIME_KEYS = {"carrier", "status", "reason", "updates"}
RUNTIME_UPDATE_KEYS = {"line", "before", "after"}
MERGE_KEYS = {"path", "digest_before", "digest_after"}
CHECKS_KEYS = {"preconditions", "moved_files", "live_rewrite", "dated_preserved",
               "unclassified", "unresolved_before", "unresolved_after",
               "runtime_carriers", "files_match"}
CONDITION_KEYS = {"merge_status", "open_conflicts", "slices_closed",
                  "dirty_spec_tree", "side_presence"}
INT_CHECKS = ("moved_files", "live_rewrite", "dated_preserved", "unclassified",
              "unresolved_before", "unresolved_after", "runtime_carriers")
PATH_FIELDS = ("spec_path", "pinned_commit")
WALLCLOCK_KEYS = {"generated_at", "timestamp", "time", "host", "hostname",
                  "run_id", "started_at", "finished_at"}


def _load_engine():
    spec = importlib.util.spec_from_file_location("seal_utils_archive_manifest", ENGINE)
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
         *args], capture_output=True, text=True, encoding="utf-8", check=False,
        env=env)


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


def _candidate(repo: Path, fixture: str = "clean-pair") -> dict:
    source = FIXTURES / fixture
    tree = repo / "repo"
    tree.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, tree)
    _init_git(tree)
    proc, payload = _run_plan(tree)
    assert proc.returncode == 0, payload.get("conditions")
    manifest = payload["archive"]["manifest"]
    assert isinstance(manifest, dict)
    return manifest


def _walk_keys(value, prefix=""):
    if isinstance(value, dict):
        for key, inner in value.items():
            yield prefix, key
            yield from _walk_keys(inner, prefix + "/" + key)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_keys(item, prefix + "[]")


@pytest.mark.parametrize("fixture", ["clean-pair", "reference-matrix"])
def test_c202_c206_closed_key_sets_at_every_level(tmp_path, fixture):
    manifest = _candidate(tmp_path, fixture)
    assert set(manifest) == TOP_KEYS
    assert set(manifest["generated_by"]) == GENERATED_KEYS
    assert set(manifest["merge_manifest"]) == MERGE_KEYS
    assert set(manifest["references"]) == REFERENCES_KEYS
    assert set(manifest["checks"]) == CHECKS_KEYS
    assert set(manifest["checks"]["preconditions"]) == CONDITION_KEYS
    assert manifest["generated_by"]["command"] == (
        "seal-utils.py --action archive-apply --spec-dir %s" % SPEC_REL)
    assert manifest["schema_version"] == 1
    assert manifest["spec"] == PARENT
    assert manifest["spec_path"] == SPEC_REL
    assert manifest["merge_manifest"]["path"] == "merge-manifest.json"
    for entry in manifest["slices"]:
        assert set(entry) == SLICE_KEYS
        assert set(entry["merged_into_pointer"]) == POINTER_KEYS
        assert entry["from"] == ".specify/specs/%s" % entry["slug"]
        assert entry["to"] == "%s/slices/%s" % (SPEC_REL, entry["slug"])
        assert entry["merged_into_pointer"]["path"] == (
            entry["to"] + "/requirements.md")
        assert entry["file_count"] == len(entry["files"])
        assert [row["path"] for row in entry["files"]] == sorted(
            row["path"] for row in entry["files"])
        assert all(set(row) == FILE_KEYS for row in entry["files"])
    assert [entry["order"] for entry in manifest["slices"]] == list(
        range(1, len(manifest["slices"]) + 1))
    for row in manifest["references"]["rows"]:
        assert set(row) == ROW_KEYS
        assert row["kind"] in ("live-rewrite", "dated-preserved")
        if row["kind"] == "dated-preserved":
            assert row["before"] == row["after"]
    for row in manifest["references"]["runtime"]:
        assert set(row) == RUNTIME_KEYS
        assert row["status"] in ("runtime-updated", "absent")
        if row["status"] == "absent":
            assert row["reason"] and row["updates"] == []
        else:
            assert row["reason"] is None
        for update in row["updates"]:
            assert set(update) == RUNTIME_UPDATE_KEYS


def test_c202_serialization_is_the_declared_form(tmp_path):
    manifest = _candidate(tmp_path)
    text = json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    assert json.loads(text) == manifest
    assert list(json.loads(text)) == sorted(manifest), (
        "C-202: serialization sorts keys at every level"
    )
    assert "\\u" not in text, "ensure_ascii=False keeps CJK text literal"


def test_c207_digest_is_the_c034_algorithm(tmp_path, eng):
    manifest = _candidate(tmp_path)
    assert eng.archive_manifest_digest(manifest) == manifest["digest"]
    stripped = copy.deepcopy(manifest)
    stripped["digest"] = "sha256:" + "0" * 64
    assert eng.archive_manifest_digest(stripped) == manifest["digest"], (
        "C-034/C-207: the digest is computed with the digest field removed"
    )
    assert len(manifest["pinned_commit"]) == 40
    assert all(ch in "0123456789abcdef" for ch in manifest["pinned_commit"])


def test_c207_path_fields_are_repo_relative_and_clean(tmp_path):
    manifest = _candidate(tmp_path, "reference-matrix")
    paths = [manifest["spec_path"]] + [
        entry[field] for entry in manifest["slices"] for field in ("from", "to")
    ] + [entry["merged_into_pointer"]["path"] for entry in manifest["slices"]] + [
        row["path"] for entry in manifest["slices"] for row in entry["files"]
    ] + [row["carrier"] for row in manifest["references"]["rows"]] + [
        row["carrier"] for row in manifest["references"]["runtime"]
    ] + [manifest["merge_manifest"]["path"]]
    for value in paths:
        assert not value.startswith("/"), f"absolute path in the manifest: {value}"
        assert "\\" not in value, f"backslash in the manifest: {value}"
        assert ".." not in value.split("/"), f"parent segment in the manifest: {value}"


def test_manifest_has_no_wallclock_or_environment_fields(tmp_path):
    manifest = _candidate(tmp_path)
    keys = {key for _, key in _walk_keys(manifest)}
    assert not (keys & WALLCLOCK_KEYS), (
        "C-207: the manifest carries no wall-clock, host or run-id field"
    )
    assert not (set(manifest) & WALLCLOCK_KEYS)


def test_c206_three_closure_arithmetic_families_hold(tmp_path, eng):
    manifest = _candidate(tmp_path, "reference-matrix")
    checks = manifest["checks"]
    rows = manifest["references"]["rows"]
    runtime = manifest["references"]["runtime"]
    assert checks["live_rewrite"] + checks["dated_preserved"] == len(rows)
    assert sum(1 for row in runtime if row["status"] == "runtime-updated") \
        + sum(1 for row in runtime if row["status"] == "absent") \
        == checks["runtime_carriers"]
    assert sum(entry["file_count"] for entry in manifest["slices"]) \
        == checks["moved_files"]
    assert checks["files_match"] is True
    for key in INT_CHECKS:
        assert isinstance(checks[key], int) and not isinstance(checks[key], bool)
    assert eng.archive_closure_errors(manifest) == []


def test_sc007_delete_a_ledger_row_turns_the_arithmetic_red(tmp_path, eng):
    manifest = _candidate(tmp_path, "reference-matrix")
    mutated = copy.deepcopy(manifest)
    mutated["references"]["rows"].pop()
    assert eng.archive_closure_errors(mutated), (
        "SC-007: deleting a ledger row breaks live+dated=rows and MUST be caught"
    )
    with pytest.raises(Exception) as caught:
        eng.validate_archive_manifest(mutated, PARENT)
    assert getattr(caught.value, "code", None) == "archive-manifest-invalid"


def test_deleting_a_checks_row_is_rejected(tmp_path, eng):
    manifest = _candidate(tmp_path)
    mutated = copy.deepcopy(manifest)
    del mutated["checks"]["moved_files"]
    with pytest.raises(Exception):
        eng.validate_archive_manifest(mutated, PARENT)


def test_same_input_twice_is_byte_identical(tmp_path):
    tree = tmp_path / "repo"
    shutil.copytree(FIXTURES / "reference-matrix", tree)
    _init_git(tree)
    first_proc, first_payload = _run_plan(tree)
    second_proc, second_payload = _run_plan(tree)
    assert first_proc.returncode == second_proc.returncode == 0
    first = first_payload["archive"]["manifest"]
    second = second_payload["archive"]["manifest"]
    assert json.dumps(first, sort_keys=True, ensure_ascii=False) == \
        json.dumps(second, sort_keys=True, ensure_ascii=False), (
        "C-208: every field, including the digest and ledger order, is reproduced"
    )
    assert first_proc.stdout == second_proc.stdout


def test_c212_schema_version_is_one_and_higher_versions_refuse(tmp_path, eng):
    manifest = _candidate(tmp_path)
    assert manifest["schema_version"] == 1
    for version in (2, 0):
        mutated = copy.deepcopy(manifest)
        mutated["schema_version"] = version
        with pytest.raises(Exception) as caught:
            eng.validate_archive_manifest(mutated, PARENT)
        assert getattr(caught.value, "code", None) == "archive-manifest-invalid"


def test_c209_unknown_or_missing_fields_refuse_at_every_level(tmp_path, eng):
    manifest = _candidate(tmp_path, "reference-matrix")
    mutations = []

    def mutate(path, action):
        mutated = copy.deepcopy(manifest)
        node = mutated
        for key in path[:-1]:
            node = node[key]
        action(node, path[-1])
        mutations.append(mutated)

    mutate(["unknown_top"], lambda node, key: node.__setitem__(key, True))
    mutate(["slices", 0, "unknown_slice"], lambda node, key: node.__setitem__(key, 1))
    mutate(["slices", 0, "files", 0, "unknown_file"],
           lambda node, key: node.__setitem__(key, 1))
    mutate(["references", "rows", 0, "unknown_row"],
           lambda node, key: node.__setitem__(key, 1))
    mutate(["references", "runtime", 0, "unknown_runtime"],
           lambda node, key: node.__setitem__(key, 1))
    mutate(["checks", "unknown_check"], lambda node, key: node.__setitem__(key, 1))
    mutate(["generated_by", "unknown_generated"],
           lambda node, key: node.__setitem__(key, 1))
    mutate(["merge_manifest", "unknown_merge"],
           lambda node, key: node.__setitem__(key, 1))
    mutate(["checks", "files_match"], lambda node, key: node.pop(key))
    mutate(["references", "rows", 0, "kind"], lambda node, key: node.pop(key))
    for mutated in mutations:
        with pytest.raises(Exception) as caught:
            eng.validate_archive_manifest(mutated, PARENT)
        assert getattr(caught.value, "code", None) == "archive-manifest-invalid"
