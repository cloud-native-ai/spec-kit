from pathlib import Path

import pytest

from tests.script_api import skills_utils

ResolutionConflictError = skills_utils.ResolutionConflictError
ResourceIdError = skills_utils.ResourceIdError
backfill_resource_id = skills_utils.backfill_resource_id
resolve_resource = skills_utils.resolve_resource


def test_resolution_prefers_id_over_fuzzy_text(tmp_path: Path):
    workspace = tmp_path
    tool_file = workspace / ".specify" / "memory" / "tools" / "lint.md"
    tool_file.parent.mkdir(parents=True, exist_ok=True)
    tool_file.write_text("# lint\n", encoding="utf-8")

    result = resolve_resource(
        workspace_root=workspace,
        requested_id="<TOOL:.specify/memory/tools/lint.md>",
        requested_text="lint",
        expected_type="tool",
    )

    assert result.result_type == "resolved"
    assert result.fallback_used is False


def test_resolution_fallback_when_id_missing(tmp_path: Path):
    workspace = tmp_path
    tool_file = workspace / ".specify" / "memory" / "tools" / "format.md"
    tool_file.parent.mkdir(parents=True, exist_ok=True)
    tool_file.write_text("# format\n", encoding="utf-8")

    result = resolve_resource(workspace_root=workspace, requested_text="format", expected_type="tool")

    assert result.result_type == "fallback"
    assert result.resolved_id == "<TOOL:.specify/memory/tools/format.md>"


def test_backfill_tool_record_id_for_historical_artifact(tmp_path: Path):
    workspace = tmp_path
    tool_file = workspace / ".specify" / "memory" / "tools" / "legacy.md"
    tool_file.parent.mkdir(parents=True, exist_ok=True)
    tool_file.write_text(
        "# Tool Record: legacy\n\n**Tool Name**: legacy\n**Tool Type**: `system-binary`\n**Source Identifier**: /usr/bin/legacy\n",
        encoding="utf-8",
    )

    resolved_id = backfill_resource_id(workspace, "tool", tool_file)
    content = tool_file.read_text(encoding="utf-8")

    assert resolved_id == "<TOOL:.specify/memory/tools/legacy.md>"
    assert "**Tool ID**: <TOOL:.specify/memory/tools/legacy.md>" in content


def test_invalid_id_type_mismatch_errors(tmp_path: Path):
    workspace = tmp_path
    skill_file = workspace / ".github" / "skills" / "ops" / "SKILL.md"
    skill_file.parent.mkdir(parents=True, exist_ok=True)
    skill_file.write_text("---\nname: ops\n---\n", encoding="utf-8")

    with pytest.raises(ResolutionConflictError) as exc_info:
        resolve_resource(
            workspace_root=workspace,
            requested_id="<SKILL:.github/skills/ops/SKILL.md>",
            expected_type="tool",
        )

    assert exc_info.value.reason == "type-mismatch"


def test_stale_id_reports_resource_error(tmp_path: Path):
    with pytest.raises(ResourceIdError) as exc_info:
        resolve_resource(
            workspace_root=tmp_path,
            requested_id="<SKILL:.github/skills/missing/SKILL.md>",
            expected_type="skill",
        )

    assert exc_info.value.code == "stale-id"
