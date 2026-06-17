"""Contract tests: role-based agent template structure and validity."""

import re
import pytest
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"

ROLE_SLUGS = [
    "requirements-analyst",
    "system-designer",
    "module-designer",
    "test-engineer",
    "qa-engineer",
    "knowledge-manager",
]

MANDATORY_SECTIONS = [
    "## Identity & Responsibilities",
    "## Project Context",
    "## Workflow",
    "## Upstream (Inputs)",
    "## Downstream (Outputs)",
    "## Output Format",
]

APPROVED_PLACEHOLDERS = {
    "{{AGENT_NAME}}",
    "{{AGENT_DESCRIPTION}}",
    "{{ROLE_NAME}}",
    "{{PROJECT_NAME}}",
    "{{TECH_STACK}}",
    "{{PROJECT_STRUCTURE}}",
    "{{MODULE_LIST}}",
    "{{CONSTITUTION_PRINCIPLES}}",
    "{{FEATURE_INDEX}}",
    "{{SPECS_DIR}}",
    "{{TESTING_FRAMEWORK}}",
    "{{DOCS_DIR}}",
}


@pytest.mark.contract
class TestRoleTemplateExistence:
    """T005: Verify each role template file exists with valid YAML frontmatter."""

    @pytest.mark.parametrize("slug", ROLE_SLUGS)
    def test_template_file_exists(self, slug):
        path = TEMPLATES_DIR / f"agent-role-{slug}-template.md"
        assert path.exists(), f"Role template missing: {path}"

    @pytest.mark.parametrize("slug", ROLE_SLUGS)
    def test_template_has_yaml_frontmatter(self, slug):
        path = TEMPLATES_DIR / f"agent-role-{slug}-template.md"
        content = path.read_text()
        assert content.startswith("---"), f"{slug}: must start with YAML frontmatter"
        parts = content.split("---", 2)
        assert len(parts) >= 3, f"{slug}: malformed frontmatter (needs opening and closing ---)"
        frontmatter = parts[1]
        assert "name:" in frontmatter or "{{AGENT_NAME}}" in frontmatter
        assert "description:" in frontmatter or "{{AGENT_DESCRIPTION}}" in frontmatter
        assert "user-invocable:" in frontmatter

    @pytest.mark.parametrize("slug", ROLE_SLUGS)
    def test_template_omits_tools_field(self, slug):
        path = TEMPLATES_DIR / f"agent-role-{slug}-template.md"
        content = path.read_text()
        parts = content.split("---", 2)
        frontmatter = parts[1]
        assert "tools:" not in frontmatter, f"{slug}: tools field must be omitted (FR-009a)"


@pytest.mark.contract
class TestRoleTemplateSections:
    """T006: Verify each role template contains mandatory sections."""

    @pytest.mark.parametrize("slug", ROLE_SLUGS)
    def test_mandatory_sections_present(self, slug):
        path = TEMPLATES_DIR / f"agent-role-{slug}-template.md"
        content = path.read_text()
        for section in MANDATORY_SECTIONS:
            assert section in content, f"{slug}: missing mandatory section '{section}'"


@pytest.mark.contract
class TestRoleTemplatePlaceholders:
    """T007: Verify templates use only approved placeholder variables."""

    @pytest.mark.parametrize("slug", ROLE_SLUGS)
    def test_only_approved_placeholders(self, slug):
        path = TEMPLATES_DIR / f"agent-role-{slug}-template.md"
        content = path.read_text()
        found = set(re.findall(r"\{\{[A-Z_]+\}\}", content))
        unapproved = found - APPROVED_PLACEHOLDERS
        assert not unapproved, f"{slug}: unapproved placeholders found: {unapproved}"
