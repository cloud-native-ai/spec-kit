"""Contract test: `/speckit.team` command routing (SC-002, Feature 027).

Enforces the team-command-contract (§ Modes / Routing / MUST-MUST NOT) and the
migration contract M6:
  - `templates/commands/team.md` exists and exposes exactly the three modes
    create / modify / run, routing to create-team / improve-team / create-team.
  - `templates/commands/agents.md` no longer routes any team/orchestration
    operation (no `organize-agents`, no team-loop/parallel/serial orchestration
    routing), i.e. team ops are not served by `/speckit.agents`.
"""

import re
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEAM_CMD = REPO_ROOT / "templates" / "commands" / "team.md"
AGENTS_CMD = REPO_ROOT / "templates" / "commands" / "agents.md"


@pytest.mark.contract
class TestTeamCommandRouting:
    def test_team_command_exists(self):
        assert TEAM_CMD.exists(), "templates/commands/team.md must exist (source of /speckit.team)"

    def test_team_command_exposes_three_modes(self):
        content = TEAM_CMD.read_text(encoding="utf-8").lower()
        for mode in ("create", "modify", "run"):
            assert mode in content, f"team.md must document the '{mode}' mode"

    def test_team_command_routes_to_team_skills(self):
        content = TEAM_CMD.read_text(encoding="utf-8")
        assert "create-team" in content, "team.md must route create/run to create-team"
        assert "improve-team" in content, "team.md must route modify to improve-team"

    def test_team_command_has_preview_confirm_gate(self):
        content = TEAM_CMD.read_text(encoding="utf-8").lower()
        assert "static structure" in content and "dynamic structure" in content, (
            "team.md run mode must render Static + Dynamic structure"
        )
        assert "confirm" in content, "team.md run mode must require explicit confirmation"

    def test_agents_command_does_not_route_team_ops(self):
        content = AGENTS_CMD.read_text(encoding="utf-8")
        assert "organize-agents" not in content, (
            "agents.md must not reference organize-agents after migration"
        )
        # No orchestration/team-execution routing left in the single-agent command.
        assert not re.search(r"team[\s-]?loop", content, flags=re.IGNORECASE), (
            "agents.md must not route team-loop orchestration"
        )
        assert "team-supervisor" not in content.lower(), (
            "agents.md must not offer the team-supervisor authoring mode"
        )
