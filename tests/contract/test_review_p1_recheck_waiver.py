"""Contract test: append-only recheck and the four-part waiver.

Pins Feature 063 C-8, C-9, C-10 (F2, FR-006..FR-008/SC-004):

* C-8 — `create-checklist` § 5 declares the recheck form: one NEW append-only file
  per round (`checklists/recheck-<date>-<topic>.md`), each answer quotes the
  requirement line it answers, and the original checklist is never refreshed in
  place (its unchecked rows are history).
* C-9 — `implement-feature` § Step 2 gains the third branch: an item answered by a
  later stage's recheck is counted as answered, not incomplete, and needs no waiver;
  the gate fires only for genuinely unresolved items.
* C-10 — waivers carry `Scope` / `Basis` / `Disposition` / `Closed`; `Closed` states
  what solved the item; a waiver missing any part is non-compliant.

Red before the mechanism lands (Tests Mode = ON, Constitution Principle IV).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CREATE_CHECKLIST = ROOT / "skills" / "internal" / "create-checklist" / "SKILL.md"
IMPLEMENT_SKILL = ROOT / "skills" / "internal" / "implement-feature" / "SKILL.md"


def _section(text: str, start: str, end: str) -> str:
    m = re.search(rf"(?ms)^{start}.*?(?=^{end})", text)
    assert m, f"section {start!r} not found"
    return m.group(0)


def _create_checklist_generate() -> str:
    return _section(CREATE_CHECKLIST.read_text(encoding="utf-8"),
                    r"### 5\. Generate the checklist", r"### 6\.")


def _implement_step_2() -> str:
    return _section(IMPLEMENT_SKILL.read_text(encoding="utf-8"),
                    r"### Step 2 .*", r"### Step 3")


# --------------------------------------------------------------------------- #
# C-8 — append-only recheck
# --------------------------------------------------------------------------- #

def test_c8_recheck_file_form_is_append_only_per_round():
    section = _create_checklist_generate()
    assert "recheck-<date>-<topic>.md" in section, (
        "the recheck filename form MUST be declared literally"
    )
    assert re.search(r"append-only|追加", section, re.I), (
        "the recheck file MUST be append-only"
    )
    assert re.search(r"NEW file|每轮|per round", section, re.I), (
        "each round MUST create a new file"
    )


def test_c8_answers_quote_the_requirement_line():
    section = _create_checklist_generate()
    assert re.search(r"requirement line|需求行|requirement 行", section, re.I), (
        "every answered entry MUST quote the requirement line it answers"
    )


def test_c8_original_checklist_is_never_refreshed_in_place():
    section = _create_checklist_generate()
    assert re.search(r"MUST NOT|不得", section)
    assert re.search(r"refresh|刷新", section, re.I)
    assert re.search(r"in place|原地", section, re.I)
    assert re.search(r"history|历史", section, re.I), (
        "unchecked rows MUST be preserved as history"
    )


# --------------------------------------------------------------------------- #
# C-9 — the third branch of the exemption gate
# --------------------------------------------------------------------------- #

def test_c9_gate_has_a_third_branch_for_recheck_answered_items():
    step = _implement_step_2()
    assert re.search(r"recheck", step, re.I), (
        "the third branch MUST be driven by the recheck record"
    )
    assert re.search(r"answered|已回答", step, re.I)
    assert re.search(r"not incomplete|不计未完成|不算未完成", step, re.I)
    assert re.search(r"no waiver|无需 waiver|不需要 waiver|无需豁免", step, re.I)


def test_c9_gate_fires_only_for_genuinely_unresolved_items():
    step = _implement_step_2()
    assert re.search(r"only|仅", step, re.I)
    assert re.search(r"unresolved|未解决", step, re.I)


# --------------------------------------------------------------------------- #
# C-10 — four-part waiver
# --------------------------------------------------------------------------- #

def test_c10_waiver_has_all_four_parts():
    step = _implement_step_2()
    for part in ("Scope", "Basis", "Disposition", "Closed"):
        assert re.search(rf"\b{part}\b", step), (
            f"the waiver format MUST carry the `{part}` part"
        )


def test_c10_closed_states_what_solved_it():
    step = _implement_step_2()
    m = re.search(r"(?ms)\bClosed\b.*?(?=\n\s*(?:[-*]|\||$))", step)
    assert m, "the `Closed` part MUST be described"
    assert re.search(r"solved|解决", m.group(0), re.I), (
        "`Closed` MUST state what solved the item"
    )


def test_c10_a_waiver_missing_any_part_is_non_compliant():
    step = _implement_step_2()
    assert re.search(r"missing|缺", step, re.I)
    assert re.search(r"non-compliant|不合规", step, re.I)


def test_c10_waiver_storage_is_the_feature_spec_directory():
    step = _implement_step_2()
    assert "waivers.md" in step, "waivers MUST land in the feature's waivers.md"
    assert re.search(r"REQUIREMENTS_DIR|<spec-dir>", step)
