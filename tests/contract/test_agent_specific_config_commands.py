"""Contract tests for Agent-Specific Configuration in command templates (C-001, C-007)."""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

COMMAND_TEMPLATES = [
    ROOT / "templates" / "commands" / "agents.md",
    ROOT / "templates" / "commands" / "skills.md",
    ROOT / "templates" / "commands" / "tools.md",
]

REQUIRED_HEADINGS = [
    "## Agent-Specific Configuration",
    "### Step 1: Identify Executing Agent",
    "### Step 2: Load Agent-Specific Guidance",
    "### Step 3: Capture Execution Feedback",
]


class TestC001CommandTemplateSectionPresence:
    """C-001: Each targeted command template MUST contain Agent-Specific Configuration section."""

    @pytest.mark.contract
    @pytest.mark.parametrize("template_path", COMMAND_TEMPLATES, ids=lambda p: p.stem)
    def test_section_headings_exist(self, template_path: Path):
        content = template_path.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            assert heading in content, (
                f"{template_path.name} missing required heading: {heading}"
            )


class TestC007AdditiveConstraint:
    """C-007: Agent-Specific Configuration section MUST appear after main workflow sections.

    If a Handoffs section exists, Agent-Specific Configuration MUST appear before it.
    If no Handoffs section exists, Agent-Specific Configuration MUST appear after
    the last main workflow section (## Output Requirements or similar).
    """

    @pytest.mark.contract
    @pytest.mark.parametrize("template_path", COMMAND_TEMPLATES, ids=lambda p: p.stem)
    def test_section_not_at_top(self, template_path: Path):
        content = template_path.read_text(encoding="utf-8")
        agent_config_pos = content.find("## Agent-Specific Configuration")
        assert agent_config_pos != -1, (
            f"{template_path.name} missing ## Agent-Specific Configuration"
        )
        assert agent_config_pos > len(content) // 3, (
            f"{template_path.name}: ## Agent-Specific Configuration should not appear near the top"
        )

    @pytest.mark.contract
    @pytest.mark.parametrize("template_path", COMMAND_TEMPLATES, ids=lambda p: p.stem)
    def test_section_before_handoffs_if_present(self, template_path: Path):
        content = template_path.read_text(encoding="utf-8")
        agent_config_pos = content.find("## Agent-Specific Configuration")
        handoffs_pos = content.find("## Handoffs")
        if handoffs_pos != -1:
            assert agent_config_pos < handoffs_pos, (
                f"{template_path.name}: ## Agent-Specific Configuration must appear before ## Handoffs"
            )
