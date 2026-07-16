"""Contract test: `organize-agents` is renamed to `create-team` (M1, Feature 027).

Enforces the Team Migration contract
(``.specify/specs/.archive/026-agent-team-management/contracts/team-migration-contract.md`` § M1)
and the create-team skill contract § Identity.

Assertions:
  - ``skills/create-team/SKILL.md`` resolves as an installed skill.
  - ``skills/organize-agents/`` no longer resolves.
  - The create-team skill declares ``name: create-team`` and the new ``skill_id``,
    with no lingering ``organize-agents`` string in its body/frontmatter.
"""

import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"


def _installed_skill_slugs():
    return {p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")}


@pytest.mark.contract
class TestCreateTeamRename:
    def test_create_team_resolves(self):
        """`create-team` installs and resolves under its new name."""
        assert (SKILLS_DIR / "create-team" / "SKILL.md").exists(), (
            "skills/create-team/SKILL.md must exist (renamed from organize-agents)"
        )
        assert "create-team" in _installed_skill_slugs()

    def test_organize_agents_no_longer_resolves(self):
        """`organize-agents` is gone after the rename."""
        assert not (SKILLS_DIR / "organize-agents").exists(), (
            "skills/organize-agents/ must not exist after rename to create-team"
        )
        assert "organize-agents" not in _installed_skill_slugs()

    def test_create_team_frontmatter_identity(self):
        """Frontmatter carries the new name + skill_id and no organize-agents string."""
        content = (SKILLS_DIR / "create-team" / "SKILL.md").read_text(encoding="utf-8")
        parts = content.split("---", 2)
        assert len(parts) >= 3, "malformed frontmatter in create-team/SKILL.md"
        frontmatter = parts[1]
        assert "name: create-team" in frontmatter, (
            "create-team frontmatter must declare 'name: create-team'"
        )
        assert "<SKILL:.specify/skills/create-team/SKILL.md>" in frontmatter, (
            "create-team frontmatter must declare the new skill_id"
        )
        assert "organize-agents" not in content, (
            "no 'organize-agents' string may remain in create-team/SKILL.md"
        )
