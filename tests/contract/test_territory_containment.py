"""Contract test for member ⊆ team territory containment (037-goal-registry, T046).

TT-6: a member-level territory whose write scope escapes the team-level write scope
is an out-of-bounds violation and must be reported, not silently allowed.
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
    spec = importlib.util.spec_from_file_location("bsi_contain", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules["bsi_contain"] = module
    spec.loader.exec_module(module)
    return module


bsi = _engine()


def test_member_write_inside_team_write_is_in_bounds():
    out = bsi.containment_violations(team_write=["docs/**"], member_write=["docs/reference/x.md"])
    assert out == [], f"a member write inside the team scope is in bounds; got {out}"


def test_member_write_outside_team_write_is_reported():
    out = bsi.containment_violations(team_write=["docs/**"], member_write=["skills/x.md"])
    assert out, "a member write outside the team scope must be reported"
    assert "skills/x.md" in " ".join(out)


def test_empty_team_write_cannot_contain_anything():
    out = bsi.containment_violations(team_write=[], member_write=["docs/x.md"])
    assert out, "with no team-level write scope, a member write is unbounded and reported"


def test_no_member_scope_is_vacuously_in_bounds():
    out = bsi.containment_violations(team_write=["docs/**"], member_write=[])
    assert out == []
