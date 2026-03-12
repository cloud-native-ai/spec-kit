from pathlib import Path

from tests.script_api import skills_utils

generate_resource_id = skills_utils.generate_resource_id


def test_generate_tool_resource_id_uses_workspace_relative_path(tmp_path: Path):
    workspace = tmp_path
    tool_record = workspace / ".specify" / "memory" / "tools" / "demo.md"
    tool_record.parent.mkdir(parents=True, exist_ok=True)
    tool_record.write_text("# demo\n", encoding="utf-8")

    resource_id = generate_resource_id("tool", tool_record, workspace)

    assert resource_id == "<TOOL:.specify/memory/tools/demo.md>"


def test_generate_skill_resource_id_uses_skill_md_path(tmp_path: Path):
    workspace = tmp_path
    skill_file = workspace / ".github" / "skills" / "demo" / "SKILL.md"
    skill_file.parent.mkdir(parents=True, exist_ok=True)
    skill_file.write_text("---\nname: demo\n---\n", encoding="utf-8")

    resource_id = generate_resource_id("skill", skill_file, workspace)

    assert resource_id == "<SKILL:.github/skills/demo/SKILL.md>"
