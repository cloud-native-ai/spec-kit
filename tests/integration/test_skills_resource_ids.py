from pathlib import Path

from tests.script_api import skills_utils

backfill_skill_id = skills_utils.backfill_skill_id
generate_skill_id = skills_utils.generate_skill_id
read_skill_id = skills_utils.read_skill_id


def test_skill_id_persisted_for_new_skill(tmp_path: Path):
    workspace = tmp_path
    skill_root = workspace / ".github" / "skills" / "testing"
    skill_file = skill_root / "SKILL.md"
    skill_root.mkdir(parents=True, exist_ok=True)
    skill_file.write_text("---\nname: testing\ndescription: test\n---\n", encoding="utf-8")

    skill_id = generate_skill_id(skill_root, workspace)
    backfill_skill_id(skill_file, workspace)

    assert read_skill_id(skill_file) == skill_id


def test_backfill_skill_id_is_idempotent(tmp_path: Path):
    workspace = tmp_path
    skill_root = workspace / ".github" / "skills" / "ops"
    skill_file = skill_root / "SKILL.md"
    skill_root.mkdir(parents=True, exist_ok=True)
    skill_file.write_text(
        "---\nname: ops\ndescription: ops\nskill_id: \"<SKILL:.github/skills/ops/SKILL.md>\"\n---\n",
        encoding="utf-8",
    )

    result = backfill_skill_id(skill_file, workspace)

    assert result is None
