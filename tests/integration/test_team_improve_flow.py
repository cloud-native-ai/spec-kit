"""Integration test: team improve flow artifacts (quickstart §2, Feature 027).

Validates the artifacts that drive the improve flow (see test_team_create_flow for
the rationale on artifact-based checks):
  - `skills/improve-team/SKILL.md` documents structure-preserving, evidence-based
    edits (e.g. add a member) that bump the `updated` date while leaving unaffected
    fields unchanged (SC-005).
  - The negative "team not found" path offers to create the team (FR-010).
"""

import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
IMPROVE_TEAM = REPO_ROOT / "skills" / "improve-team" / "SKILL.md"


@pytest.mark.integration
class TestTeamImproveFlow:
    @pytest.fixture
    def content(self):
        return IMPROVE_TEAM.read_text(encoding="utf-8")

    def test_operates_on_existing_team(self, content):
        assert ".specify/teams/" in content, "improve-team must load the persisted .team.md"

    def test_targeted_structure_preserving(self, content):
        lower = content.lower()
        assert "targeted" in lower or "structure-preserving" in lower or "preserve" in lower, (
            "improve-team must make targeted, structure-preserving edits"
        )
        assert "evidence" in lower, "improve-team must be evidence-based"

    def test_bumps_updated_date(self, content):
        assert "updated" in content, "improve-team must bump the 'updated' date after editing"

    def test_team_not_found_offers_create(self, content):
        lower = content.lower()
        assert "team not found" in lower, "improve-team must handle the missing-team case"
        assert "create" in lower, "improve-team must offer to create a missing team (FR-010)"
