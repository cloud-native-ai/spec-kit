"""Contract test: single-agent skills contain no team/orchestration content (SC-003).

Enforces migration contract M4:
  - `skills/create-agent/SKILL.md` retains only single-agent authoring modes
    (`role`, `supervisor`, `custom`, `project-custom`) and no `triad` /
    `team-supervisor` modes or orchestration content.
  - `skills/improve-agent/SKILL.md` contains no Triad/orchestration refinement
    content (those move to `improve-team`).
"""

import re
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CREATE_AGENT = REPO_ROOT / "skills" / "create-agent" / "SKILL.md"
IMPROVE_AGENT = REPO_ROOT / "skills" / "improve-agent" / "SKILL.md"

# Multi-agent / orchestration tokens that must not appear in the single-agent skills.
FORBIDDEN_TOKENS = [
    "team-supervisor",
    "Team Supervisor",
    "Triad Mode",
    "Team Supervisor Mode",
    "EEI triad",
    "orchestration template",
    "parallel dispatch",
    "serial chain",
    "team loop",
    "team-loop",
]


@pytest.mark.contract
class TestSingleAgentPurity:
    def test_create_agent_has_no_team_content(self):
        content = CREATE_AGENT.read_text(encoding="utf-8")
        offending = [t for t in FORBIDDEN_TOKENS if t.lower() in content.lower()]
        assert not offending, (
            f"create-agent/SKILL.md must not contain team/orchestration tokens: {offending}"
        )

    def test_create_agent_retains_single_agent_modes(self):
        content = CREATE_AGENT.read_text(encoding="utf-8")
        for kind in ("role", "supervisor", "custom", "project-custom"):
            assert kind in content, f"create-agent must retain the '{kind}' authoring mode"

    def test_create_agent_no_triad_mode(self):
        content = CREATE_AGENT.read_text(encoding="utf-8")
        assert not re.search(r"^\|\s*`?triad`?\s*\|", content, flags=re.MULTILINE), (
            "create-agent capability matrix must not list a 'triad' mode"
        )

    def test_improve_agent_has_no_team_content(self):
        content = IMPROVE_AGENT.read_text(encoding="utf-8")
        offending = [t for t in FORBIDDEN_TOKENS if t.lower() in content.lower()]
        assert not offending, (
            f"improve-agent/SKILL.md must not contain team/orchestration tokens: {offending}"
        )
        assert "triad refinement" not in content.lower(), (
            "improve-agent must not contain a Triad Refinement section"
        )
