"""Contract tests for team-level territory normalization (037-goal-registry, T042).

Contract: .specify/specs/037-goal-registry/contracts/team-territory.contract.md

The overlap machinery is only as good as its normalization. This pins TT-2/TT-3:
brace expansion, relative→canonical, trailing-slash removal, and glob retention —
including the `{a,b,c}` brace form this repo has already been bitten by.
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
    spec = importlib.util.spec_from_file_location("bsi_territory", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules["bsi_territory"] = module
    spec.loader.exec_module(module)
    return module


bsi = _engine()


def test_brace_form_is_expanded():
    """The {a,b,c} form that evaded a prior existence check must expand."""
    out = bsi.expand_scopes(["skills/{a,b,c}/x.md"])
    assert out == {"skills/a/x.md", "skills/b/x.md", "skills/c/x.md"}


def test_nested_and_multiple_braces_expand():
    out = bsi.expand_scopes(["{docs,src}/{a,b}.md"])
    assert out == {"docs/a.md", "docs/b.md", "src/a.md", "src/b.md"}


def test_relative_segments_are_canonicalised():
    assert bsi.normalize_scope("./docs/../skills/x.md") == "skills/x.md"


def test_trailing_slash_removed():
    assert bsi.normalize_scope("docs/reference/") == "docs/reference"


def test_globs_are_retained_not_expanded_against_the_filesystem():
    out = bsi.expand_scopes(["docs/**"])
    assert out == {"docs/**"}, "globs must be kept as patterns, not filesystem-expanded"


def test_leading_dot_slash_removed():
    assert bsi.normalize_scope("./a/b") == "a/b"
