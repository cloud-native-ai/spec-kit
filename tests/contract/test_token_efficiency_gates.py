"""Contract tests for Feature 040 authoring gates (C-A3, spec 035).

Every creation/improvement flow that authors framework units must carry a
token-efficiency check item referencing the discipline doc, with skill
mirrors kept identical; the skill scaffold template must NOT grow a
checklist section.
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]

GATE_FILES = [
    "skills/create-skills/references/skill-creation-quality-checklist.md",
    "skills/improve-skills/references/skill-quality-checklist.md",
    "skills/create-agent/SKILL.md",
    "skills/create-team/SKILL.md",
    "skills/create-tools/SKILL.md",
]


@pytest.mark.parametrize("rel", GATE_FILES)
def test_ca3_gate_file_carries_marker(rel):
    path = ROOT / rel
    assert path.is_file(), f"missing gate file: {rel}"
    text = path.read_text(encoding="utf-8")
    assert "token-efficiency" in text, f"token-efficiency check item missing in {rel}"


@pytest.mark.parametrize("rel", GATE_FILES)
def test_ca3_gate_file_references_discipline_doc_not_copies(rel):
    text = (ROOT / rel).read_text(encoding="utf-8")
    assert "token-efficiency.md" in text, f"discipline doc reference missing in {rel}"
    assert "## 程序优先(Program-First)" not in text, f"discipline section copied into {rel}"


@pytest.mark.parametrize("rel", GATE_FILES)
def test_ca3_skill_mirror_identical(rel):
    src = ROOT / rel
    mirror = ROOT / ".specify" / rel
    assert mirror.is_file(), f"missing mirror: {mirror}"
    assert src.read_bytes() == mirror.read_bytes(), f"mirror drift: {rel}"


def test_ca3_skills_template_not_bloated():
    text = (ROOT / "templates" / "skills-template.md").read_text(encoding="utf-8")
    assert "token-efficiency" not in text, (
        "skills-template.md must not grow a token-efficiency checklist section "
        "(gate items belong to creation flows, not the artifact scaffold)"
    )
