"""Contract tests for Agent-Specific Configuration in skills (C-002, C-003, C-004)."""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

SKILL_DIRS = [
    ROOT / "skills" / "browser-utils",
    ROOT / "skills" / "create-agent",
    ROOT / "skills" / "improve-agent",
    ROOT / "skills" / "improve-skills",
]

REQUIRED_SECTION_HEADINGS = [
    "## Agent-Specific Configuration",
    "### Step 1: Identify Executing Agent",
    "### Step 2: Load Agent-Specific Guidance",
    "### Step 3: Capture Execution Feedback",
]

REQUIRED_AGENT_GUIDES = ["claude-code-guide.md", "copilot-guide.md"]

REQUIRED_GUIDE_HEADINGS = [
    "## Tool Mapping",
    "## Best Practices",
    "## Known Pitfalls",
    "## Capability Notes",
]


class TestC002SkillSectionPresence:
    """C-002: Each targeted skill MUST contain Agent-Specific Configuration section."""

    @pytest.mark.contract
    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda p: p.name)
    def test_section_headings_exist(self, skill_dir: Path):
        skill_md = skill_dir / "SKILL.md"
        assert skill_md.exists(), f"{skill_dir.name}/SKILL.md does not exist"
        content = skill_md.read_text(encoding="utf-8")
        for heading in REQUIRED_SECTION_HEADINGS:
            assert heading in content, (
                f"{skill_dir.name}/SKILL.md missing required heading: {heading}"
            )

    @pytest.mark.contract
    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda p: p.name)
    def test_step2_references_skill_home(self, skill_dir: Path):
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert "${SKILL_HOME}/references/" in content, (
            f"{skill_dir.name}/SKILL.md Step 2 must reference ${{SKILL_HOME}}/references/"
        )


class TestC003ReferenceDocumentNaming:
    """C-003: Each targeted skill MUST have claude-code-guide.md and copilot-guide.md."""

    @pytest.mark.contract
    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda p: p.name)
    @pytest.mark.parametrize("guide_name", REQUIRED_AGENT_GUIDES)
    def test_agent_guide_exists(self, skill_dir: Path, guide_name: str):
        guide_path = skill_dir / "references" / guide_name
        assert guide_path.exists(), (
            f"{skill_dir.name}/references/{guide_name} does not exist"
        )


class TestC004ReferenceDocumentStructure:
    """C-004: Each agent reference document MUST contain required sections."""

    @pytest.mark.contract
    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda p: p.name)
    @pytest.mark.parametrize("guide_name", REQUIRED_AGENT_GUIDES)
    def test_guide_has_required_sections(self, skill_dir: Path, guide_name: str):
        guide_path = skill_dir / "references" / guide_name
        if not guide_path.exists():
            pytest.skip(f"{guide_path} does not exist yet")
        content = guide_path.read_text(encoding="utf-8")
        for heading in REQUIRED_GUIDE_HEADINGS:
            assert heading in content, (
                f"{skill_dir.name}/references/{guide_name} missing: {heading}"
            )
