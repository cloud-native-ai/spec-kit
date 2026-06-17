"""Integration tests: context injection placeholders in role-based agent templates."""

import re
import pytest
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"
COMMANDS_DIR = TEMPLATES_DIR / "commands"

ROLE_SLUGS = [
    "requirements-analyst",
    "system-designer",
    "module-designer",
    "test-engineer",
    "qa-engineer",
    "knowledge-manager",
]

CONTEXT_PLACEHOLDERS = {
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


@pytest.mark.integration
class TestContextPlaceholderCoverage:
    """T029: Verify templates use context placeholders that will be resolved."""

    @pytest.mark.parametrize("slug", ROLE_SLUGS)
    def test_no_raw_placeholders_left_unresolvable(self, slug):
        path = TEMPLATES_DIR / f"agent-role-{slug}-template.md"
        content = path.read_text()
        found = set(re.findall(r"\{\{[A-Z_]+\}\}", content))
        frontmatter_only = {"{{AGENT_NAME}}", "{{AGENT_DESCRIPTION}}", "{{ROLE_NAME}}"}
        context_vars = found - frontmatter_only
        for var in context_vars:
            assert var in CONTEXT_PLACEHOLDERS, (
                f"{slug}: uses placeholder {var} not in the approved context list"
            )

    def test_all_context_sources_documented_in_command(self):
        agents_cmd = COMMANDS_DIR / "agents.md"
        content = agents_cmd.read_text()
        for placeholder in CONTEXT_PLACEHOLDERS:
            assert placeholder in content, (
                f"agents.md does not document how to resolve {placeholder}"
            )


@pytest.mark.integration
class TestRoleSpecificContext:
    """T030: Verify role-specific context placeholders are assigned correctly."""

    def test_module_designer_has_module_list(self):
        content = (TEMPLATES_DIR / "agent-role-module-designer-template.md").read_text()
        assert "{{MODULE_LIST}}" in content

    def test_module_designer_has_project_structure(self):
        content = (TEMPLATES_DIR / "agent-role-module-designer-template.md").read_text()
        assert "{{PROJECT_STRUCTURE}}" in content

    def test_qa_engineer_has_constitution_principles(self):
        content = (TEMPLATES_DIR / "agent-role-qa-engineer-template.md").read_text()
        assert "{{CONSTITUTION_PRINCIPLES}}" in content

    def test_system_designer_has_feature_index(self):
        content = (TEMPLATES_DIR / "agent-role-system-designer-template.md").read_text()
        assert "{{FEATURE_INDEX}}" in content

    def test_test_engineer_has_testing_framework(self):
        content = (TEMPLATES_DIR / "agent-role-test-engineer-template.md").read_text()
        assert "{{TESTING_FRAMEWORK}}" in content

    def test_knowledge_manager_has_docs_dir(self):
        content = (TEMPLATES_DIR / "agent-role-knowledge-manager-template.md").read_text()
        assert "{{DOCS_DIR}}" in content

    def test_all_templates_have_project_name(self):
        for slug in ROLE_SLUGS:
            content = (TEMPLATES_DIR / f"agent-role-{slug}-template.md").read_text()
            assert "{{PROJECT_NAME}}" in content, f"{slug}: missing {{{{PROJECT_NAME}}}}"

    def test_all_templates_have_tech_stack(self):
        for slug in ROLE_SLUGS:
            content = (TEMPLATES_DIR / f"agent-role-{slug}-template.md").read_text()
            assert "{{TECH_STACK}}" in content, f"{slug}: missing {{{{TECH_STACK}}}}"
