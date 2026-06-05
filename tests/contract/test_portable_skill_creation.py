"""Contract tests for portable skill creation (013-portable-skill-creation).

Validates that tool-manifest references have been removed from the skill
creation pipeline: create-skills SKILL.md, skills-template.md, orchestration
template, scaffolding script, quality checklist, and mirror parity.
"""
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CREATE_SKILLS_FILE = ROOT / "skills" / "create-skills" / "SKILL.md"
CREATE_SKILLS_MIRROR = ROOT / ".specify" / "skills" / "create-skills" / "SKILL.md"
SKILLS_TEMPLATE = ROOT / "templates" / "skills-template.md"
ORCHESTRATION_TEMPLATE = ROOT / "templates" / "commands" / "skills.md"
SCAFFOLDING_SCRIPT = ROOT / "scripts" / "bash" / "create-new-skill.sh"
QUALITY_CHECKLIST = ROOT / "skills" / "create-skills" / "references" / "skill-creation-quality-checklist.md"
QUALITY_CHECKLIST_MIRROR = (
    ROOT / ".specify" / "skills" / "create-skills" / "references" / "skill-creation-quality-checklist.md"
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# FR-001: create-skills/SKILL.md has no refresh-tools.sh reference
# ---------------------------------------------------------------------------

@pytest.mark.contract
def test_create_skills_no_refresh_tools_ref():
    text = _text(CREATE_SKILLS_FILE)
    assert "refresh-tools.sh" not in text, (
        "create-skills/SKILL.md still references refresh-tools.sh"
    )


# ---------------------------------------------------------------------------
# FR-002: create-skills/SKILL.md has no tool manifest file references
# ---------------------------------------------------------------------------

@pytest.mark.contract
def test_create_skills_no_tool_manifest_refs():
    text = _text(CREATE_SKILLS_FILE)
    for pattern in ("tools/system.json", "tools/shell.json", "tools/project.json"):
        assert pattern not in text, (
            f"create-skills/SKILL.md still references {pattern}"
        )


# ---------------------------------------------------------------------------
# FR-002, SC-005: create-skills/SKILL.md has no "Obtain available tools" step
# ---------------------------------------------------------------------------

@pytest.mark.contract
def test_create_skills_no_obtain_tools_step():
    text = _text(CREATE_SKILLS_FILE)
    assert "Obtain available tools information" not in text, (
        "create-skills/SKILL.md still contains 'Obtain available tools information' heading"
    )


# ---------------------------------------------------------------------------
# FR-003: skills-template.md has no Tools subsection or refresh-tools
# ---------------------------------------------------------------------------

@pytest.mark.contract
def test_skills_template_no_tools_subsection():
    text = _text(SKILLS_TEMPLATE)
    assert "### Tools" not in text, (
        "skills-template.md still contains '### Tools' heading"
    )
    assert "refresh-tools.sh" not in text, (
        "skills-template.md still references refresh-tools.sh"
    )


# ---------------------------------------------------------------------------
# FR-004: skills-template.md retains scripts, references, assets sections
# ---------------------------------------------------------------------------

@pytest.mark.contract
def test_skills_template_retains_resources():
    text = _text(SKILLS_TEMPLATE)
    for section in ("Scripts", "References", "Assets"):
        assert section in text, (
            f"skills-template.md is missing the '{section}' section"
        )


# ---------------------------------------------------------------------------
# FR-005: orchestration template has no refresh-tools.sh reference
# ---------------------------------------------------------------------------

@pytest.mark.contract
def test_orchestration_no_refresh_tools():
    text = _text(ORCHESTRATION_TEMPLATE)
    assert "refresh-tools.sh" not in text, (
        "templates/commands/skills.md still references refresh-tools.sh"
    )


# ---------------------------------------------------------------------------
# FR-007: script has no refresh_tools_for_target
# ---------------------------------------------------------------------------

@pytest.mark.contract
def test_script_no_refresh_tools_for_target():
    text = _text(SCAFFOLDING_SCRIPT)
    assert "refresh_tools_for_target" not in text, (
        "create-new-skill.sh still contains refresh_tools_for_target"
    )


# ---------------------------------------------------------------------------
# FR-009: mirror parity — create-skills SKILL.md
# ---------------------------------------------------------------------------

@pytest.mark.contract
def test_create_skills_mirror_parity():
    if not CREATE_SKILLS_MIRROR.exists():
        pytest.skip("Mirror file does not exist")
    assert _text(CREATE_SKILLS_FILE) == _text(CREATE_SKILLS_MIRROR), (
        "create-skills SKILL.md mirror differs from source"
    )


# ---------------------------------------------------------------------------
# FR-011: quality checklist has no tool manifest references
# ---------------------------------------------------------------------------

@pytest.mark.contract
def test_checklist_no_tool_manifest_refs():
    text = _text(QUALITY_CHECKLIST)
    assert "tool manifests" not in text.lower(), (
        "Quality checklist still references 'tool manifests'"
    )
    assert "tools/system.json" not in text, (
        "Quality checklist still references tools/system.json"
    )
