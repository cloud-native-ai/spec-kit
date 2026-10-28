"""Cross-skill contract for the three SDD-driving external skills.

Pins the split introduced by the setup/house-keeping extraction:
setup = bootstrap, house-keeping = periodic maintenance, loop-driver = stages.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SETUP = ROOT / "skills" / "external" / "sdd-project-setup" / "SKILL.md"
HOUSE = ROOT / "skills" / "external" / "sdd-house-keeping" / "SKILL.md"
LOOP = ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
PREFLIGHT = ROOT / "skills" / "internal" / "run-agent" / "references" / "dispatch-preflight.md"
TARGET = ROOT / "shared" / "workflow" / "target-resolution.md"


def _read(path: Path) -> str:
    assert path.is_file(), f"missing: {path}"
    return path.read_text(encoding="utf-8")


def test_target_resolution_splits_dependency_classes():
    owner = _read(TARGET)
    assert "Skill dependency classes" in owner
    assert "no `.specify/` dependency" in owner
    assert "strong `.specify/` dependency" in owner
    assert "Walk **upward**" in owner
    assert "refuse to execute" in owner
    assert "sdd-project-setup" in owner
    assert "git rev-parse --show-toplevel" in owner
    assert "Reject a root whose basename is `.specify`" in owner
    for skill in (SETUP, HOUSE, LOOP):
        assert "target-resolution.md" in _read(skill), (
            f"{skill.name} must reference the shared target-resolution owner")


def test_setup_has_no_specify_dependency_and_two_skills_do():
    setup = _read(SETUP)
    assert "不依赖 `.specify/`" in setup
    assert "不向上搜索 `.specify/`" in setup
    for path in (HOUSE, LOOP):
        text = _read(path)
        assert "向上搜索" in text
        assert "拒绝执行" in text or "handoff `sdd-project-setup`" in text
        assert "不向上搜索 `.specify/`" not in text


def test_setup_is_bootstrap_only_and_hands_off():
    text = _read(SETUP)
    assert "The Loop (S0–S2 + HANDOFF)" in text
    assert "S2.5 BOOTSTRAP" in text
    assert "sdd-house-keeping" in text
    assert "bootstrap-complete / maintenance-pending" in text
    assert "MUST NOT 执行 `/speckit.sanitize`" in text
    assert "S3 RECONCILE" not in text
    assert "S3+ STRENGTHEN" not in text


def test_house_keeping_owns_maintenance_and_record_retention():
    text = _read(HOUSE)
    assert "H1 缺口 OR owner 自检报告的漂移" in text
    assert "/speckit.sanitize check" in text
    assert "/speckit.sanitize --lane all" in text
    assert "bootstrap-gap" in text
    assert "record-retention.py" in text
    assert "sdd-project-setup" in text
    assert "sdd-loop-driver" in text


def test_loop_driver_names_both_handoff_targets():
    text = _read(LOOP)
    assert "sdd-project-setup" in text
    assert "sdd-house-keeping" in text
    assert "bootstrap" in text
    preflight = _read(PREFLIGHT)
    assert "sdd-project-setup" in preflight
    assert "sdd-house-keeping H1–H4" in preflight
    assert "bootstrap-complete / maintenance-pending" in preflight


def test_docs_pages_carry_the_three_loop_map():
    for name in ("sdd-project-setup.md", "sdd-house-keeping.md"):
        text = _read(ROOT / "docs" / "reference" / "skills" / name)
        assert "S0–S2" in text or "S0–S2 + HANDOFF" in text
        assert "H0–H5" in text or "S0–S2" in text
    loop_doc = _read(ROOT / "docs" / "reference" / "skills" / "sdd-loop-driver.md")
    assert "house-keeping" in loop_doc
