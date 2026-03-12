from pathlib import Path

import pytest

from tests.script_api import skills_utils

ResourceIdError = skills_utils.ResourceIdError
generate_resource_id = skills_utils.generate_resource_id
infer_resource_type = skills_utils.infer_resource_type
normalize_workspace_path = skills_utils.normalize_workspace_path
validate_resource_id = skills_utils.validate_resource_id


def test_normalize_workspace_path_returns_posix_relative(tmp_path: Path):
    workspace = tmp_path
    target = workspace / ".specify" / "memory" / "tools" / "demo.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("# demo\n", encoding="utf-8")

    normalized = normalize_workspace_path(target, workspace)

    assert normalized == ".specify/memory/tools/demo.md"


def test_normalize_workspace_path_rejects_outside_workspace(tmp_path: Path):
    outside = tmp_path.parent / "outside.md"
    outside.write_text("x\n", encoding="utf-8")

    with pytest.raises(ResourceIdError) as exc_info:
        normalize_workspace_path(outside, tmp_path)

    assert exc_info.value.code == "out-of-workspace"


def test_validate_resource_id_and_type_inference():
    ok, code = validate_resource_id("<SKILL:.github/skills/demo/SKILL.md>", expected_type="skill")
    assert ok is True
    assert code is None
    assert infer_resource_type("<SKILL:.github/skills/demo/SKILL.md>") == "skill"


def test_generate_resource_id_rejects_type_mismatch(tmp_path: Path):
    workspace = tmp_path
    skill_file = workspace / ".github" / "skills" / "demo" / "SKILL.md"
    skill_file.parent.mkdir(parents=True, exist_ok=True)
    skill_file.write_text("---\nname: demo\n---\n", encoding="utf-8")

    with pytest.raises(ResourceIdError) as exc_info:
        generate_resource_id("tool", skill_file, workspace)

    assert exc_info.value.code == "invalid-type"
