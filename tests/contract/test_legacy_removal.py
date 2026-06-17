"""Contract tests: legacy capability-based agent templates removed."""

import pytest
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"
COMMANDS_DIR = TEMPLATES_DIR / "commands"

LEGACY_TEMPLATES = [
    "agent-common-template.md",
    "agent-knowledge-template.md",
    "agent-plan-template.md",
    "agent-research-template.md",
]

LEGACY_REFERENCES = [
    "agent-common-template",
    "agent-knowledge-template",
    "agent-plan-template",
    "agent-research-template",
]


@pytest.mark.contract
class TestLegacyTemplateRemoval:
    """T015: Verify legacy capability-based templates do not exist."""

    @pytest.mark.parametrize("filename", LEGACY_TEMPLATES)
    def test_legacy_template_removed(self, filename):
        path = TEMPLATES_DIR / filename
        assert not path.exists(), f"Legacy template still exists: {path}"


@pytest.mark.contract
class TestCommandNoLegacyReferences:
    """T016: Verify agents command does not reference legacy templates."""

    @pytest.mark.parametrize("ref", LEGACY_REFERENCES)
    def test_agents_command_no_legacy_reference(self, ref):
        agents_cmd = COMMANDS_DIR / "agents.md"
        assert agents_cmd.exists(), "agents.md command file missing"
        content = agents_cmd.read_text()
        assert ref not in content, f"agents.md still references legacy template: {ref}"
