"""Contract test: checklist loading and `[Gap]` consumption in `/speckit.analyze`.

Pins Feature 063 C-3 and C-4 (F2, FR-005/SC-003):

* C-3 — the analyze load table gains a `checklists/*.md` row carrying item text,
  checked state, and tags (`[Gap]` in particular); the command face's Delegation
  Inputs name the checklist surface.
* C-4 — the detection passes include one checklist pass: every unchecked `[Gap]`
  item is raised as a finding or carries an explicit disposition marker. Free prose
  MUST NOT satisfy it, and the report makes "unchecked + unraised + undispositioned"
  observable as zero.

Red before the mechanism lands (Tests Mode = ON, Constitution Principle IV).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANALYZE_SKILL = ROOT / "skills" / "internal" / "analyze-artifacts" / "SKILL.md"
ANALYZE_REFS = ROOT / "skills" / "internal" / "analyze-artifacts" / "references"
ANALYZE_CMD = ROOT / "templates" / "commands" / "analyze.md"


def _load_table() -> str:
    text = ANALYZE_SKILL.read_text(encoding="utf-8")
    m = re.search(r"(?ms)^### 2\. Load artifacts.*?(?=^### 3\.)", text)
    assert m, "analyze skill § 2 artifact load table not found"
    return m.group(0)


def _detection_surface() -> str:
    """The skill body plus its references: the checklist pass may land in either."""
    parts = [ANALYZE_SKILL.read_text(encoding="utf-8")]
    if ANALYZE_REFS.is_dir():
        parts.extend(p.read_text(encoding="utf-8") for p in sorted(ANALYZE_REFS.glob("*.md")))
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# C-3 — loading the checklist surface
# --------------------------------------------------------------------------- #

def test_c3_load_table_has_a_checklists_row():
    table = _load_table()
    rows = [l for l in table.splitlines() if l.strip().startswith("|")]
    checklist_rows = [l for l in rows if "checklists/" in l]
    assert len(checklist_rows) == 1, (
        f"the load table MUST gain exactly one `checklists/*.md` row; got {checklist_rows}"
    )
    row = checklist_rows[0]
    assert re.search(r"item text|条目文本|item 文本", row, re.I), (
        "the row MUST load item text"
    )
    assert re.search(r"checked|勾选", row, re.I), "the row MUST load checked state"
    assert re.search(r"tags?|标签", row, re.I), "the row MUST load tags"
    assert "[Gap]" in row, "the row MUST name [Gap] in particular"


def test_c3_command_face_names_the_checklist_surface():
    body = ANALYZE_CMD.read_text(encoding="utf-8")
    m = re.search(r"(?ms)^## Delegation.*?(?=^## )", body)
    assert m, "analyze command § Delegation not found"
    assert "checklists/" in m.group(0), (
        "Delegation Inputs MUST name the checklist surface (C-3)"
    )


# --------------------------------------------------------------------------- #
# C-4 — deterministic Gap disposition
# --------------------------------------------------------------------------- #

def test_c4_every_unchecked_gap_is_raised_or_dispositioned():
    surface = _detection_surface()
    assert re.search(r"\[Gap\]", surface), "the pass MUST name the [Gap] tag"
    assert re.search(r"unchecked|未勾选", surface, re.I)
    assert re.search(r"finding|finding", surface, re.I) and re.search(
        r"disposition|处置", surface, re.I
    ), "the pass MUST offer raise-as-finding or an explicit disposition"


def test_c4_marker_form_is_deterministic_and_free_prose_does_not_satisfy():
    surface = _detection_surface()
    assert "disposition:" in surface, "the marker MUST carry a machine-readable key"
    assert "raised-as-finding" in surface
    assert "covered-by" in surface
    assert re.search(r"CHK\d{3}\s+disposition:", surface), (
        "the marker MUST pin the item id immediately before `disposition:`"
    )
    assert re.search(r"free prose|自由散文", surface, re.I)
    assert re.search(r"MUST NOT|不得", surface)

    # the declared grammar is decidable: this parser is the executable reading of it
    marker = re.compile(
        r"^CHK\d{3} disposition: (?:raised-as-finding (?:H-\d+|H-?[A-Z]+-\d+)"
        r"|covered-by \S.*)$"
    )
    assert marker.match("CHK005 disposition: raised-as-finding H-01")
    assert marker.match("CHK005 disposition: covered-by plan.md § Rollout")
    assert not marker.match("CHK005 looks fine to me")
    assert not marker.match("CHK005 raised")


def test_c4_undispositioned_count_is_observable_as_zero():
    surface = _detection_surface()
    assert re.search(
        r"unchecked\s*\+\s*unraised\s*\+\s*undispositioned|未勾选.{0,8}未升格.{0,8}未处置",
        surface,
        re.I,
    ), "the report MUST make the undispositioned count observable"
    assert re.search(r"(?:==|=|为)\s*0", surface), (
        "the count MUST be reported against a zero verdict"
    )
