from tests.script_api import skills_utils


def test_infer_skill_type_from_specify_primary_path():
    inferred = skills_utils.infer_resource_type_from_path(
        ".specify/skills/demo/SKILL.md"
    )
    assert inferred == "skill"


def test_infer_skill_type_from_legacy_github_path():
    inferred = skills_utils.infer_resource_type_from_path(
        ".github/skills/demo/SKILL.md"
    )
    assert inferred == "skill"


def test_entrypoint_and_outcome_status_enums_are_defined():
    assert "created" in skills_utils.ENTRYPOINT_STATUS
    assert "conflict" in skills_utils.ENTRYPOINT_STATUS
    assert "success" in skills_utils.OUTCOME_STATUS
    assert "partial-success" in skills_utils.OUTCOME_STATUS
