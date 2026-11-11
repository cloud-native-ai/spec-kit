"""Unit tests for the archive manifest arithmetic and digest (Feature 100, P3).

Contract: ``.specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md``
C-206 (three closure arithmetic families) and C-207 (the 099 C-034 digest:
sha256 over the sorted compact JSON with the ``digest`` field removed).

Constitution Principle IV: pure functions carry their own unit tests.
Red-first: lands before the helpers exist; reading in ``notes/red-first-evidence.md``.
"""

from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"

#: Pinned expected digest for the fixed document below (C-034 algorithm).
PINNED_DIGEST = "sha256:79841272c0d8350792a3026744f2e1db7df3504dc84e81f3f98c7c005eccdb13"


def _load_engine():
    spec = importlib.util.spec_from_file_location("seal_utils_manifest_math", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def eng():
    return _load_engine()


def _document(rows=2, live=1, dated=1, runtime=("runtime-updated", "absent"),
              runtime_carriers=2, file_counts=(2, 1), moved_files=3,
              unclassified=0):
    return {
        "slices": [{"file_count": count} for count in file_counts],
        "references": {
            "rows": [{} for _ in range(rows)],
            "runtime": [{"status": status} for status in runtime],
        },
        "checks": {
            "moved_files": moved_files,
            "live_rewrite": live,
            "dated_preserved": dated,
            "unclassified": unclassified,
            "runtime_carriers": runtime_carriers,
        },
    }


def test_c034_digest_matches_the_pinned_constant(eng):
    document = {"alpha": 1, "beta": [{"x": "值"}], "schema_version": 1}
    assert eng.archive_manifest_digest(document) == PINNED_DIGEST


def test_c034_digest_ignores_the_digest_field_itself(eng):
    document = {"alpha": 1, "beta": [{"x": "值"}], "schema_version": 1}
    with_digest = dict(document, digest=PINNED_DIGEST)
    assert eng.archive_manifest_digest(with_digest) == PINNED_DIGEST


def test_c034_digest_is_key_order_independent(eng):
    first = {"b": 2, "a": {"y": 1, "x": 0}}
    second = {"a": {"x": 0, "y": 1}, "b": 2}
    assert eng.archive_manifest_digest(first) == eng.archive_manifest_digest(second)


def test_c206_a_valid_document_has_no_closure_errors(eng):
    assert eng.archive_closure_errors(_document()) == []


def test_c206_deleting_a_ledger_row_breaks_the_first_family(eng):
    document = _document(rows=3, live=1, dated=1)
    assert document["checks"]["live_rewrite"] + document["checks"]["dated_preserved"] \
        != len(document["references"]["rows"])
    errors = eng.archive_closure_errors(document)
    assert errors and any("live_rewrite" in error for error in errors)


def test_c206_runtime_count_must_match_the_declared_carriers(eng):
    document = _document(runtime=("runtime-updated",), runtime_carriers=2)
    errors = eng.archive_closure_errors(document)
    assert errors and any("runtime" in error for error in errors)


def test_c206_moved_files_must_equal_the_slice_file_counts(eng):
    document = _document(file_counts=(2, 1), moved_files=2)
    errors = eng.archive_closure_errors(document)
    assert errors and any("moved_files" in error or "file_count" in error
                          for error in errors)


def test_c206_bool_is_not_an_acceptable_int_count(eng):
    document = copy.deepcopy(_document())
    document["checks"]["unclassified"] = False
    errors = eng.archive_closure_errors(document)
    assert errors and any("unclassified" in error for error in errors)
