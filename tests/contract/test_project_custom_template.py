"""Contract tests: project-custom agent scaffold template and skill docs.

The `project-custom` authoring capability produces a project-bound agent from a
single reusable scaffold. This guards two invariants:

1. The scaffold `agent-project-custom-template.md` exists with valid YAML
   frontmatter, carries the `project:` binding marker + Qoder-compatible fields,
   and contains the mandatory `## Project Scope Guard` section.
2. `skills/create-agent/SKILL.md` documents the `project-custom` capability and
   its scope-guard behavior so the command can route to it.
"""

import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = ROOT / "skills" / "create-agent" / "templates"
SKILL = ROOT / "skills" / "create-agent" / "SKILL.md"
SCAFFOLD = TEMPLATES_DIR / "agent-project-custom-template.md"


@pytest.mark.contract
class TestProjectCustomTemplate:
    def test_scaffold_exists(self):
        assert SCAFFOLD.exists(), f"project-custom scaffold missing: {SCAFFOLD}"

    def test_valid_frontmatter(self):
        content = SCAFFOLD.read_text(encoding="utf-8")
        assert content.startswith("---"), "must start with YAML frontmatter"
        parts = content.split("---", 2)
        assert len(parts) >= 3, "malformed frontmatter (needs opening and closing ---)"
        frontmatter = parts[1]
        assert "name:" in frontmatter or "{{AGENT_NAME}}" in frontmatter
        assert "description:" in frontmatter or "{{AGENT_DESCRIPTION}}" in frontmatter
        assert "user-invocable:" in frontmatter

    def test_qoder_frontmatter_fields(self):
        frontmatter = SCAFFOLD.read_text(encoding="utf-8").split("---", 2)[1]
        for field in ("model:", "tools:", "maxTurns:"):
            assert field in frontmatter, f"missing Qoder frontmatter field '{field}'"

    def test_project_binding_marker(self):
        frontmatter = SCAFFOLD.read_text(encoding="utf-8").split("---", 2)[1]
        assert "project:" in frontmatter, "scaffold must carry a 'project:' binding marker"

    def test_project_scope_guard_section(self):
        content = SCAFFOLD.read_text(encoding="utf-8")
        assert "## Project Scope Guard" in content, "missing mandatory Project Scope Guard section"


@pytest.mark.contract
class TestProjectCustomSkillDocs:
    def test_skill_documents_project_custom_capability(self):
        content = SKILL.read_text(encoding="utf-8")
        assert "project-custom" in content, "SKILL.md must document the project-custom capability"

    def test_skill_documents_scope_guard(self):
        content = SKILL.read_text(encoding="utf-8")
        assert "Project Scope Guard" in content, "SKILL.md must document the scope-guard behavior"
