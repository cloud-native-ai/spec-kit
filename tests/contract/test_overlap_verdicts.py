"""Contract tests for overlap verdicts (037-goal-registry, T043).

Contract: .specify/specs/037-goal-registry/contracts/team-territory.contract.md

Three verdicts, kept distinct: `overlap` (write-write intersection, entries named),
`no-overlap` (both declared, no write intersection), `undecidable` (either team
undeclared, or the only intersection is between non-path entries). Read overlap is
allowed. Two non-path declarations are never judged equivalent.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"

pytestmark = pytest.mark.contract


def _engine():
    spec = importlib.util.spec_from_file_location("bsi_overlap", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules["bsi_overlap"] = module
    spec.loader.exec_module(module)
    return module


bsi = _engine()


def T(write=None, read=None, forbidden=None, non_path=None):
    return {
        "write": list(write or []),
        "read": list(read or []),
        "forbidden": list(forbidden or []),
        "non_path": list(non_path or []),
    }


# --------------------------------------------------------------------------
# scope-pair overlap (TT-4)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("a,b", [
    ("docs/**", "docs/reference/team.md"),   # glob covers a concrete descendant
    ("docs/**", "docs/**"),                  # identical
    ("docs/reference/**", "docs/**"),        # nested globs
    ("a/b", "a/b"),                          # identical concrete
])
def test_overlapping_scope_pairs(a, b):
    assert bsi.scopes_overlap(a, b), f"{a!r} and {b!r} should overlap"


@pytest.mark.parametrize("a,b", [
    ("docs/**", "skills/**"),
    ("docs/a.md", "docs/b.md"),
    ("src/x", "tests/x"),
])
def test_disjoint_scope_pairs(a, b):
    assert not bsi.scopes_overlap(a, b), f"{a!r} and {b!r} should be disjoint"


# --------------------------------------------------------------------------
# verdicts (TT-5, OV-1..OV-5)
# --------------------------------------------------------------------------

def test_write_write_intersection_is_overlap_and_names_entries():
    finding = bsi.overlap_verdict("A", T(write=["docs/**"]), "B", T(write=["docs/reference/x.md"]))
    assert finding["verdict"] == "overlap"
    assert finding["kind"] == "write-write"
    assert finding["entries"], "an overlap finding must name the intersecting entries"


def test_read_only_intersection_is_not_overlap():
    finding = bsi.overlap_verdict("A", T(read=["skills/**"]), "B", T(read=["skills/x.md"]))
    assert finding["verdict"] != "overlap"


def test_read_vs_write_intersection_is_not_overlap():
    finding = bsi.overlap_verdict("A", T(read=["docs/**"]), "B", T(write=["docs/x.md"]))
    assert finding["verdict"] != "overlap", "read-vs-write is not a write-write overlap"


def test_both_declared_no_write_intersection_is_no_overlap():
    finding = bsi.overlap_verdict("A", T(write=["docs/**"]), "B", T(write=["skills/**"]))
    assert finding["verdict"] == "no-overlap"


def test_undeclared_team_is_undecidable_not_no_overlap():
    finding = bsi.overlap_verdict("A", T(write=["docs/**"]), "B", T())
    assert finding["verdict"] == "undecidable"
    assert finding["verdict"] != "no-overlap"


def test_only_non_path_intersection_is_undecidable():
    a = T(non_path=[{"type": "framework", "target": "spec-kit"}])
    b = T(non_path=[{"type": "framework", "target": "spec-kit"}])
    finding = bsi.overlap_verdict("A", a, "B", b)
    assert finding["verdict"] == "undecidable"


def test_two_non_path_declarations_are_never_judged_equivalent():
    a = T(non_path=[{"type": "framework", "target": "spec-kit"}])
    b = T(non_path=[{"type": "framework", "target": "spec-kit"}])
    finding = bsi.overlap_verdict("A", a, "B", b)
    # listed side by side for arbitration, not auto-merged
    assert finding["verdict"] == "undecidable"
    assert "non_path" in finding.get("note", "").lower() or finding.get("non_path_pairs")


def test_no_overlap_and_undecidable_are_distinct():
    declared = bsi.overlap_verdict("A", T(write=["docs/**"]), "B", T(write=["skills/**"]))
    undeclared = bsi.overlap_verdict("A", T(write=["docs/**"]), "B", T())
    assert declared["verdict"] == "no-overlap"
    assert undeclared["verdict"] == "undecidable"
    assert declared["verdict"] != undeclared["verdict"]
