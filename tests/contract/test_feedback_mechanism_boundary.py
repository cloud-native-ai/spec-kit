"""Contract test: keep the feedback / SDD-flow mechanism boundary explicit.

Owner: ``shared/workflow/feedback-step.md`` § *Mechanism boundary — SDD-flow
mechanisms vs framework feedback*.

The failure this guard prevents is calling ``/speckit.review`` a "global, whole-project"
report — inherited wording from feature 027 — which made the feature-scoped SDD review
look like the home for whole-framework diagnosis. The correct model is:

- ``/speckit.analyze`` and ``/speckit.review`` are SDD-flow mechanisms whose input is
  the current feature;
- feedback is not an SDD stage; it targets the framework and aggregates across units;
- each entry stays ``scope: local``; the framework-wide view is the introspection
  aggregation over recorded entries, never a zero-input audit.

Only current owners/surfaces are scanned. Dated feature specs (``.specify/specs``) are
historical records and are deliberately excluded.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER = REPO_ROOT / "shared" / "workflow" / "feedback-step.md"
DOCS_REF = REPO_ROOT / "docs" / "reference" / "skills" / "feedback.md"
ENGINE = REPO_ROOT / "scripts" / "python" / "feedback-utils.py"
SKILLS = {
    "manage-feedback": REPO_ROOT / "skills" / "internal" / "manage-feedback" / "SKILL.md",
    "review-sdd-process": REPO_ROOT / "skills" / "internal" / "review-sdd-process" / "SKILL.md",
    "analyze-artifacts": REPO_ROOT / "skills" / "internal" / "analyze-artifacts" / "SKILL.md",
}

BOUNDARY_HEADING = "### Mechanism boundary — SDD-flow mechanisms vs framework feedback"

# The misleading wording that must not survive in current surfaces. The specs under
# .specify/specs/ that introduced it are dated records, not live doctrine.
OBSOLETE = (
    "sole **global**, whole-project process report",
    "global/whole-project assessment",
    "the global ``/speckit.review`` report",
    "The global `/speckit.review`",
)


def _flat(text: str) -> str:
    """Collapse whitespace so a hard-wrapped phrase still matches the literal."""
    return re.sub(r"\s+", " ", text)


def test_owner_declares_the_boundary():
    text = OWNER.read_text(encoding="utf-8")
    assert BOUNDARY_HEADING in text, "owner lost its mechanism-boundary subsection"
    flat = _flat(text)
    for literal in (
        "belong to the SDD flow",
        "Feedback is not an SDD stage",
        "framework-wide view exists only as the **aggregation**",
        "never as an independent, zero-input audit",
    ):
        assert literal in flat, f"owner boundary lost substance: {literal!r}"


def test_current_surfaces_drop_the_global_review_wording():
    for path in (OWNER, DOCS_REF, ENGINE, *SKILLS.values()):
        assert path.is_file(), f"missing current surface: {path.relative_to(REPO_ROOT)}"
        flat = _flat(path.read_text(encoding="utf-8"))
        for obsolete in OBSOLETE:
            assert obsolete not in flat, (
                f"{path.relative_to(REPO_ROOT)} still describes review as a "
                f"whole-framework report: {obsolete!r}"
            )


def test_each_mechanism_surface_points_at_the_owner():
    for name, path in SKILLS.items():
        flat = _flat(path.read_text(encoding="utf-8"))
        assert "feedback-step.md" in flat, f"{name} lost its pointer to the boundary owner"
        assert "Mechanism boundary" in flat, (
            f"{name} points at feedback-step.md without naming the section"
        )


def test_docs_reference_states_the_correct_relationship():
    flat = _flat(DOCS_REF.read_text(encoding="utf-8"))
    for literal in (
        "SDD-flow mechanisms",
        "feature-scoped",
        "not an SDD stage",
        "aggregation",
    ):
        assert literal in flat, f"docs reference lost boundary fact: {literal!r}"
