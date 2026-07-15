"""Integration test: team create flow artifacts (quickstart §1, Feature 027).

Because teams are authored/executed by an interactive agent, this integration
test validates the *artifacts* that drive the create flow rather than spawning a
live agent:
  - `templates/commands/team.md` documents the create mode and the persisted
    store path `.specify/teams/<slug>/team.md`.
  - `skills/create-team/SKILL.md` describes producing a persisted team with the
    data-model schema: YAML frontmatter (slug / pattern / members / config), a
    `## Static Structure` matrix, and a `## Dynamic Structure`.
  - The runtime store directory `.specify/teams/` is tracked.
"""

import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEAM_CMD = REPO_ROOT / "templates" / "commands" / "team.md"
CREATE_TEAM_SKILL = REPO_ROOT / "skills" / "create-team" / "SKILL.md"
TEAMS_STORE = REPO_ROOT / ".specify" / "teams"


@pytest.mark.integration
class TestTeamCreateFlow:
    def test_command_documents_persistence_store(self):
        content = TEAM_CMD.read_text(encoding="utf-8")
        assert ".specify/teams/" in content, (
            "team.md must reference the persisted team store .specify/teams/"
        )

    def test_command_documents_create_mode(self):
        content = TEAM_CMD.read_text(encoding="utf-8").lower()
        assert "create" in content

    def test_skill_describes_team_file_schema(self):
        content = CREATE_TEAM_SKILL.read_text(encoding="utf-8")
        assert ".specify/teams/" in content, "create-team must document the team.md store"
        assert "## Static Structure" in content, "create-team must define the Static Structure"
        assert "## Dynamic Structure" in content, "create-team must define the Dynamic Structure"
        for key in ("pattern", "members", "config", "slug"):
            assert key in content, f"create-team must document the '{key}' frontmatter field"

    def test_teams_store_tracked(self):
        assert (TEAMS_STORE / ".gitkeep").exists(), (
            ".specify/teams/.gitkeep must exist so the store is tracked"
        )
