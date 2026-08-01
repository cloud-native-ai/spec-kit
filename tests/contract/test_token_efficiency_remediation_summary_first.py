"""Contract tests pinning summary-first remediation of audit top-5 (spec 035).

Frozen audit rows V-001 (plan.md), V-002 (clarify.md), V-003 (implement.md),
V-005 (requirements.md): whole-file / whole-corpus context loading replaced
by summary-level instructions. Pins: old phrase gone, replacement present,
mirror parity, fan-out copies carry the edit.
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
CMD = ROOT / "templates" / "commands"

# (audit-id, template, old phrase that must be gone, new phrase that must exist)
PINS = [
    (
        "V-001",
        "plan.md",
        "and all files in `.specify/memory/features/`",
        "read ONLY the detail file(s) of the bound/related Feature",
    ),
    (
        "V-002",
        "clarify.md",
        "**Load common context**: `.specify/memory/constitution.md`, `README.md`, relevant `docs/`",
        "only as targeted excerpts",
    ),
    (
        "V-003",
        "implement.md",
        "**Load context**: tasks.md (REQUIRED), plan.md (REQUIRED), data-model.md, contracts/, research.md, quickstart.md (IF EXISTS)",
        "preload ONLY tasks.md (REQUIRED) and plan.md (REQUIRED)",
    ),
    (
        "V-005",
        "requirements.md",
        "skim the highest-numbered existing spec under `.specify/specs/` before drafting",
        "targeted excerpts — heading structure",
    ),
]


@pytest.mark.parametrize("vid,name,old,new", PINS, ids=[p[0] for p in PINS])
def test_old_whole_read_instruction_gone(vid, name, old, new):
    text = (CMD / name).read_text(encoding="utf-8")
    assert old not in text, f"{vid}: whole-read instruction still present in {name}"


@pytest.mark.parametrize("vid,name,old,new", PINS, ids=[p[0] for p in PINS])
def test_summary_first_replacement_present(vid, name, old, new):
    text = (CMD / name).read_text(encoding="utf-8")
    assert new in text, f"{vid}: summary-first replacement missing in {name}"
    assert "token-efficiency.md" in text, f"{vid}: discipline reference missing in {name}"


@pytest.mark.parametrize("vid,name,old,new", PINS, ids=[p[0] for p in PINS])
def test_mirror_identical(vid, name, old, new):
    src = CMD / name
    mirror = ROOT / ".specify" / "templates" / "commands" / name
    assert src.read_bytes() == mirror.read_bytes(), f"{vid}: template mirror drift for {name}"


@pytest.mark.parametrize("vid,name,old,new", PINS, ids=[p[0] for p in PINS])
def test_fanout_copy_carries_edit(vid, name, old, new):
    copy = ROOT / ".qoder" / "commands" / f"speckit.{name}"
    text = copy.read_text(encoding="utf-8")
    assert old not in text, f"{vid}: per-tool copy still has old phrase (regen missed)"
    assert new in text, f"{vid}: per-tool copy missing remediated phrase (regen missed)"
