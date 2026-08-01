"""Contract tests pinning program-first remediation of audit top-5 (spec 035).

Frozen audit row V-004 (templates/commands/tasks.md): the constitution
keyword detection must be a deterministic grep step, not a whole-file
LLM parse. Pins: old phrase gone, program-first replacement present,
fan-out copies carry the edit.
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]

CANONICAL = ROOT / "templates" / "commands" / "tasks.md"
MIRROR = ROOT / ".specify" / "templates" / "commands" / "tasks.md"
QODER_COPY = ROOT / ".qoder" / "commands" / "speckit.tasks.md"

OLD_PHRASE = "parse `.specify/memory/constitution.md` and detect any principle"
NEW_PHRASE = "grep -nE 'MUST|MANDATORY|NON-NEGOTIABLE|Test-First|TDD|Contract-Driven'"


def test_v004_old_whole_file_parse_gone():
    text = CANONICAL.read_text(encoding="utf-8")
    assert OLD_PHRASE not in text, "V-004: whole-constitution LLM parse instruction still present"


def test_v004_program_first_replacement_present():
    text = CANONICAL.read_text(encoding="utf-8")
    assert NEW_PHRASE in text, "V-004: deterministic grep detection step missing"
    assert "token-efficiency.md" in text, "V-004: discipline reference missing in tasks.md template"


def test_v004_mirror_identical():
    assert CANONICAL.read_bytes() == MIRROR.read_bytes(), "tasks.md template mirror drift"


def test_v004_fanout_copies_carry_edit():
    text = QODER_COPY.read_text(encoding="utf-8")
    assert OLD_PHRASE not in text, "per-tool copy still has old phrase (regen missed)"
    assert NEW_PHRASE in text, "per-tool copy missing remediated phrase (regen missed)"
    assert "AUTO-GENERATED" in text.splitlines()[0], "per-tool copy lost AUTO-GENERATED header"
