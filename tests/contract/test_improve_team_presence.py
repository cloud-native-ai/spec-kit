"""Contract test: `improve-team` skill presence + non-declarable status (Feature 027).

Enforces the improve-team-skill-contract § Identity and migration contract M5/M6:
  - `skills/improve-team/SKILL.md` resolves as an installed skill with the correct
    frontmatter identity.
  - `improve-team` (and `create-team`) are members of the non-declarable set
    documented in `skills/create-skills/SKILL.md`, and `organize-agents` is gone.
"""

import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"
IMPROVE_TEAM = SKILLS_DIR / "improve-team" / "SKILL.md"
CREATE_SKILLS = SKILLS_DIR / "create-skills" / "SKILL.md"


def _installed_skill_slugs():
    return {p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")}


@pytest.mark.contract
class TestImproveTeamPresence:
    def test_improve_team_resolves(self):
        assert IMPROVE_TEAM.exists(), "skills/improve-team/SKILL.md must exist"
        assert "improve-team" in _installed_skill_slugs()

    def test_improve_team_identity(self):
        content = IMPROVE_TEAM.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        assert len(parts) >= 3, "malformed frontmatter in improve-team/SKILL.md"
        frontmatter = parts[1]
        assert "name: improve-team" in frontmatter
        assert "<SKILL:.specify/skills/improve-team/SKILL.md>" in frontmatter

    def test_non_declarable_list_updated(self):
        content = CREATE_SKILLS.read_text(encoding="utf-8")
        assert "improve-team" in content, "create-skills non-declarable list must include improve-team"
        assert "create-team" in content, "create-skills non-declarable list must include create-team"
        assert "organize-agents" not in content, "organize-agents must be removed from create-skills"
