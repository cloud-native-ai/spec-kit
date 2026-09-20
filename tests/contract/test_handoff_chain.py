"""Contract tests: workflow handoff chain between role-based agent templates.

``test_role_templates.py`` pins that the seven role templates *have* a
``## Upstream (Inputs)`` and a ``## Downstream (Outputs)`` section. What this file
pins is the chain itself: those sections are non-empty, and every declared edge
names the role it hands off to. A template edit that drops an edge silently breaks
the workflow, and there is no runtime to exercise — hence the structural test.

Both blocks are table-driven over one slug list and one edge list; adding a role or
an edge is a one-line data change, not a new hand-written test function.
"""

import pytest
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "skills" / "create-agent" / "templates"

ROLE_SLUGS = [
    "requirements-analyst",
    "ux-analyst",
    "system-designer",
    "module-designer",
    "test-engineer",
    "qa-engineer",
    "knowledge-manager",
]

UPSTREAM = "## Upstream (Inputs)"
DOWNSTREAM = "## Downstream (Outputs)"
SECTIONS = {"up": UPSTREAM, "down": DOWNSTREAM}

# The directed edges of the handoff DAG: (source slug, direction, role the section
# must name). Mirrors the bullet lists the templates themselves carry.
HANDOFF_EDGES = [
    ("requirements-analyst", "down", "System Designer"),
    ("system-designer", "up", "Requirements Analyst"),
    ("system-designer", "down", "Module Designer"),
    ("system-designer", "down", "QA Engineer"),
    ("module-designer", "up", "System Designer"),
    ("module-designer", "down", "Test Engineer"),
    ("test-engineer", "up", "Module Designer"),
    # feedback loop: test results flow back to the module designer
    ("test-engineer", "down", "Module Designer"),
    ("test-engineer", "down", "QA Engineer"),
    ("qa-engineer", "up", "System Designer"),
    ("qa-engineer", "up", "Test Engineer"),
    # gap feedback: systemic quality issues flow back to the requirements analyst
    ("qa-engineer", "down", "Requirements Analyst"),
]


def _read_template(slug):
    return (TEMPLATES_DIR / f"agent-capacity-{slug}-template.md").read_text()


def _section(slug, heading):
    """Return ``heading``'s slice, bounded by the next ``## `` heading.

    Bounded on both sides so a renamed heading cannot collapse the slice to the
    whole file (which would make every membership check pass for nothing).
    """
    content = _read_template(slug)
    idx = content.index(heading)
    next_section = content.index("## ", idx + 1)
    return content[idx:next_section]


@pytest.mark.contract
class TestHandoffChain:
    """T025 + T026: each role template declares a non-empty, correctly-wired chain."""

    @pytest.mark.parametrize("heading", [UPSTREAM, DOWNSTREAM])
    @pytest.mark.parametrize("slug", ROLE_SLUGS)
    def test_section_non_empty(self, slug, heading):
        body = _section(slug, heading)
        lines = [line for line in body.split("\n")[1:] if line.strip()]
        assert len(lines) > 0, f"{slug}: {heading} section is empty"

    @pytest.mark.parametrize(
        "slug,direction,role",
        HANDOFF_EDGES,
        ids=[f"{s}-{d}-{r.replace(' ', '')}" for s, d, r in HANDOFF_EDGES],
    )
    def test_edge_names_the_role_it_hands_off_to(self, slug, direction, role):
        heading = SECTIONS[direction]
        assert role in _section(slug, heading), (
            f"{slug}: {heading} no longer names {role} — the handoff chain lost an edge"
        )
