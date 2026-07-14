"""Contract test (US1): skill feedback-step conformance.

Enforces ``contracts/feedback-step-convention.md`` §Conformance:
every ``skills/*/SKILL.md`` contains a ``## Feedback`` section AND
``templates/skills-template.md`` contains it. Both the source tree (``skills/``)
and the runtime mirror (``.specify/skills/``) are checked.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FEEDBACK_HEADING = "## Feedback"


def _skill_files(base: Path):
    return sorted(base.glob("*/SKILL.md"))


@pytest.mark.contract
def test_skills_template_carries_feedback_section():
    template = REPO_ROOT / "templates" / "skills-template.md"
    assert FEEDBACK_HEADING in template.read_text(encoding="utf-8")


@pytest.mark.contract
def test_every_source_skill_carries_feedback_section():
    skills_dir = REPO_ROOT / "skills"
    missing = [
        f.parent.name
        for f in _skill_files(skills_dir)
        if FEEDBACK_HEADING not in f.read_text(encoding="utf-8")
    ]
    assert not missing, f"skills/ SKILL.md missing '## Feedback': {missing}"


@pytest.mark.contract
def test_every_runtime_mirror_skill_carries_feedback_section():
    skills_dir = REPO_ROOT / ".specify" / "skills"
    if not skills_dir.exists():
        pytest.skip(".specify/skills mirror not present")
    missing = [
        f.parent.name
        for f in _skill_files(skills_dir)
        if FEEDBACK_HEADING not in f.read_text(encoding="utf-8")
    ]
    assert not missing, f".specify/skills/ SKILL.md missing '## Feedback': {missing}"
