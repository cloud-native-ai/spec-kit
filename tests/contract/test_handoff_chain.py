"""Contract tests: workflow handoff chain between role-based agent templates."""

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


def _read_template(slug):
    return (TEMPLATES_DIR / f"agent-role-{slug}-template.md").read_text()


@pytest.mark.contract
class TestUpstreamDownstreamSections:
    """T025: Verify each role template has non-empty upstream/downstream sections."""

    @pytest.mark.parametrize("slug", ROLE_SLUGS)
    def test_upstream_section_non_empty(self, slug):
        content = _read_template(slug)
        idx = content.index("## Upstream (Inputs)")
        next_section = content.index("## ", idx + 1)
        section_body = content[idx:next_section].strip()
        lines = [l for l in section_body.split("\n")[1:] if l.strip()]
        assert len(lines) > 0, f"{slug}: Upstream section is empty"

    @pytest.mark.parametrize("slug", ROLE_SLUGS)
    def test_downstream_section_non_empty(self, slug):
        content = _read_template(slug)
        idx = content.index("## Downstream (Outputs)")
        next_section = content.index("## ", idx + 1)
        section_body = content[idx:next_section].strip()
        lines = [l for l in section_body.split("\n")[1:] if l.strip()]
        assert len(lines) > 0, f"{slug}: Downstream section is empty"


@pytest.mark.contract
class TestHandoffChainCompleteness:
    """T026: Verify the handoff chain references are complete and correct."""

    def test_requirements_analyst_downstream_mentions_system_designer(self):
        content = _read_template("requirements-analyst")
        downstream = content[content.index("## Downstream (Outputs)"):]
        assert "System Designer" in downstream

    def test_system_designer_upstream_mentions_requirements_analyst(self):
        content = _read_template("system-designer")
        upstream = content[content.index("## Upstream (Inputs)"):content.index("## Downstream (Outputs)")]
        assert "Requirements Analyst" in upstream

    def test_system_designer_downstream_mentions_module_designer(self):
        content = _read_template("system-designer")
        downstream = content[content.index("## Downstream (Outputs)"):]
        assert "Module Designer" in downstream

    def test_system_designer_downstream_mentions_qa_engineer(self):
        content = _read_template("system-designer")
        downstream = content[content.index("## Downstream (Outputs)"):]
        assert "QA Engineer" in downstream

    def test_module_designer_upstream_mentions_system_designer(self):
        content = _read_template("module-designer")
        upstream = content[content.index("## Upstream (Inputs)"):content.index("## Downstream (Outputs)")]
        assert "System Designer" in upstream

    def test_module_designer_downstream_mentions_test_engineer(self):
        content = _read_template("module-designer")
        downstream = content[content.index("## Downstream (Outputs)"):]
        assert "Test Engineer" in downstream

    def test_test_engineer_upstream_mentions_module_designer(self):
        content = _read_template("test-engineer")
        upstream = content[content.index("## Upstream (Inputs)"):content.index("## Downstream (Outputs)")]
        assert "Module Designer" in upstream

    def test_test_engineer_downstream_mentions_module_designer_feedback(self):
        content = _read_template("test-engineer")
        downstream = content[content.index("## Downstream (Outputs)"):]
        assert "Module Designer" in downstream

    def test_test_engineer_downstream_mentions_qa_engineer(self):
        content = _read_template("test-engineer")
        downstream = content[content.index("## Downstream (Outputs)"):]
        assert "QA Engineer" in downstream

    def test_qa_engineer_upstream_mentions_system_designer(self):
        content = _read_template("qa-engineer")
        upstream = content[content.index("## Upstream (Inputs)"):content.index("## Downstream (Outputs)")]
        assert "System Designer" in upstream

    def test_qa_engineer_upstream_mentions_test_engineer(self):
        content = _read_template("qa-engineer")
        upstream = content[content.index("## Upstream (Inputs)"):content.index("## Downstream (Outputs)")]
        assert "Test Engineer" in upstream

    def test_qa_engineer_downstream_mentions_requirements_analyst(self):
        content = _read_template("qa-engineer")
        downstream = content[content.index("## Downstream (Outputs)"):]
        assert "Requirements Analyst" in downstream

    def test_knowledge_manager_references_all_roles(self):
        content = _read_template("knowledge-manager")
        assert "All roles" in content or "all roles" in content
