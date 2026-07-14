"""Contract tests: sdd-workflow no longer exists as a skill (Feature 029, contract C-REMOVE)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_sdd_workflow_skill_dir_absent_in_source():
    assert not (ROOT / "skills" / "sdd-workflow").exists()


def test_sdd_workflow_skill_dir_absent_in_installed_mirror():
    assert not (ROOT / ".specify" / "skills" / "sdd-workflow").exists()


def test_instructions_skill_list_omits_sdd_workflow():
    instructions = ROOT / ".specify" / "instructions.md"
    if not instructions.exists():
        return
    text = instructions.read_text(encoding="utf-8")
    # The skills inventory line must not advertise sdd-workflow as an installed skill.
    assert "sdd-workflow" not in text


def test_skill_count_no_longer_twenty():
    instructions = ROOT / ".specify" / "instructions.md"
    if not instructions.exists():
        return
    text = instructions.read_text(encoding="utf-8")
    assert "20 total" not in text
