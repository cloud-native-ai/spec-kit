from pathlib import Path

import pytest

from tests.script_api import skills_utils

ResolutionConflictError = skills_utils.ResolutionConflictError
ResourceIdError = skills_utils.ResourceIdError
resolve_resource = skills_utils.resolve_resource


def test_resolve_by_resource_id_returns_same_artifact(tmp_path: Path):
    workspace = tmp_path
    tool_record = workspace / ".specify" / "memory" / "tools" / "git-status.md"
    tool_record.parent.mkdir(parents=True, exist_ok=True)
    tool_record.write_text("# Tool Record\n", encoding="utf-8")

    result = resolve_resource(
        workspace_root=workspace,
        requested_id="<TOOL:.specify/memory/tools/git-status.md>",
        expected_type="tool",
    )

    assert result.result_type == "resolved"
    assert result.resolved_type == "tool"
    assert result.resolved_id == "<TOOL:.specify/memory/tools/git-status.md>"


def test_resolve_stale_resource_id_returns_stale_error(tmp_path: Path):
    with pytest.raises(ResourceIdError) as exc_info:
        resolve_resource(
            workspace_root=tmp_path,
            requested_id="<TOOL:.specify/memory/tools/missing.md>",
            expected_type="tool",
        )
    assert exc_info.value.code == "stale-id"


def test_id_text_conflict_raises_conflict(tmp_path: Path):
    workspace = tmp_path
    skill_file = workspace / ".github" / "skills" / "writer" / "SKILL.md"
    skill_file.parent.mkdir(parents=True, exist_ok=True)
    skill_file.write_text("---\nname: writer\n---\n", encoding="utf-8")

    with pytest.raises(ResolutionConflictError) as exc_info:
        resolve_resource(
            workspace_root=workspace,
            requested_id="<SKILL:.github/skills/writer/SKILL.md>",
            requested_text="planner",
            expected_type="skill",
        )

    assert exc_info.value.reason == "hint-conflict"
