"""Unit tests for the single archive-manifest schema validator (Feature 100, P3).

Contract: ``.specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md``
C-209 (one validator shared by read and write paths; every closed level rejects
unknown or missing fields with exit 2) and C-212 (schema version discipline).

The positive case is the P2 fixture ``archived-pair``: the stricter validator
MUST keep accepting the manifest that manifest-aware discovery already reads.

Red-first: lands before the validator exists; reading in ``notes/red-first-evidence.md``.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
FIXTURE = (REPO_ROOT / "tests" / "fixtures" / "seal-archive" / "archived-pair"
           / ".specify" / "specs" / "100-fixture-parent" / "archive-manifest.json")
SPEC_NAME = "100-fixture-parent"


def _load_engine():
    spec = importlib.util.spec_from_file_location("seal_utils_archive_schema", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def eng():
    return _load_engine()


@pytest.fixture()
def base():
    assert FIXTURE.is_file(), f"fixture manifest missing: {FIXTURE}"
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _rejects(eng, document):
    with pytest.raises(Exception) as caught:
        eng.validate_archive_manifest(document, SPEC_NAME)
    assert getattr(caught.value, "code", None) == "archive-manifest-invalid"
    return str(caught.value)


def test_the_archived_pair_fixture_passes_the_strict_validator(eng, base):
    eng.validate_archive_manifest(base, SPEC_NAME)


def test_top_level_unknown_and_missing_fields_are_rejected(eng, base):
    unknown = copy.deepcopy(base)
    unknown["extra"] = True
    assert "key set" in _rejects(eng, unknown)
    missing = copy.deepcopy(base)
    del missing["checks"]
    assert "key set" in _rejects(eng, missing)


def test_slice_level_unknown_and_missing_fields_are_rejected(eng, base):
    unknown = copy.deepcopy(base)
    unknown["slices"][0]["extra"] = 1
    _rejects(eng, unknown)
    missing = copy.deepcopy(base)
    del missing["slices"][0]["merged_into_pointer"]
    _rejects(eng, missing)
    bad_files = copy.deepcopy(base)
    bad_files["slices"][0]["files"][0]["extra"] = "x"
    _rejects(eng, bad_files)


def test_reference_row_and_runtime_levels_are_closed(eng, base):
    row_unknown = copy.deepcopy(base)
    row_unknown["references"]["rows"] = [{
        "carrier": ".specify/register.md", "line": 1, "before": "x",
        "after": "y", "kind": "live-rewrite", "extra": True}]
    _rejects(eng, row_unknown)
    row_missing = copy.deepcopy(base)
    row_missing["references"]["rows"] = [{
        "carrier": ".specify/register.md", "line": 1, "before": "x",
        "after": "y"}]
    _rejects(eng, row_missing)
    runtime_unknown = copy.deepcopy(base)
    runtime_unknown["references"]["runtime"][0]["extra"] = 1
    _rejects(eng, runtime_unknown)
    runtime_missing = copy.deepcopy(base)
    del runtime_missing["references"]["runtime"][0]["reason"]
    _rejects(eng, runtime_missing)


def test_checks_generated_by_and_merge_levels_are_closed(eng, base):
    for mutate in (
        lambda doc: doc["checks"].__setitem__("extra", 1),
        lambda doc: doc["checks"].pop("files_match"),
        lambda doc: doc["checks"]["preconditions"].__setitem__("extra", 1),
        lambda doc: doc["checks"]["preconditions"].pop("side_presence"),
        lambda doc: doc["generated_by"].__setitem__("extra", 1),
        lambda doc: doc["generated_by"].pop("version"),
        lambda doc: doc["merge_manifest"].__setitem__("extra", 1),
        lambda doc: doc["merge_manifest"].pop("digest_after"),
    ):
        document = copy.deepcopy(base)
        mutate(document)
        _rejects(eng, document)


def test_schema_version_two_is_rejected(eng, base):
    document = copy.deepcopy(base)
    document["schema_version"] = 2
    assert "schema_version" in _rejects(eng, document)


def test_digest_mismatch_is_rejected(eng, base):
    document = copy.deepcopy(base)
    document["digest"] = "sha256:" + "0" * 64
    assert "digest" in _rejects(eng, document)


def test_closure_arithmetic_violation_is_rejected(eng, base):
    document = copy.deepcopy(base)
    document["checks"]["moved_files"] += 1
    assert "moved_files" in _rejects(eng, document) or \
        "arithmetic" in _rejects(eng, document).lower()


def test_row_kind_domain_and_dated_byte_equality_are_enforced(eng, base):
    bad_kind = copy.deepcopy(base)
    bad_kind["references"]["rows"] = [{
        "carrier": ".specify/register.md", "line": 1, "before": "x",
        "after": "y", "kind": "rewritten"}]
    _rejects(eng, bad_kind)
    dated_changed = copy.deepcopy(base)
    dated_changed["references"]["rows"] = [{
        "carrier": ".specify/history/topic.md", "line": 1, "before": "x",
        "after": "y", "kind": "dated-preserved"}]
    _rejects(eng, dated_changed)


def test_runtime_absent_semantics_are_enforced(eng, base):
    no_reason = copy.deepcopy(base)
    no_reason["references"]["runtime"][1]["reason"] = None
    _rejects(eng, no_reason)
    with_updates = copy.deepcopy(base)
    with_updates["references"]["runtime"][1]["updates"] = [
        {"line": 1, "before": "a", "after": "b"}]
    _rejects(eng, with_updates)
    foreign_carrier = copy.deepcopy(base)
    foreign_carrier["references"]["runtime"][1]["carrier"] = (
        ".specify/state/999-foreign.md")
    _rejects(eng, foreign_carrier)


def test_paths_may_not_be_absolute_or_carry_parent_segments(eng, base):
    absolute = copy.deepcopy(base)
    absolute["spec_path"] = "/tmp/spec"
    _rejects(eng, absolute)
    parent = copy.deepcopy(base)
    parent["slices"][0]["from"] = ".specify/../specs/x"
    _rejects(eng, parent)
    backslash = copy.deepcopy(base)
    backslash["slices"][0]["to"] = ".specify\\specs\\x"
    _rejects(eng, backslash)


def test_pinned_commit_must_be_forty_lowercase_hex(eng, base):
    document = copy.deepcopy(base)
    document["pinned_commit"] = "abc123"
    _rejects(eng, document)
