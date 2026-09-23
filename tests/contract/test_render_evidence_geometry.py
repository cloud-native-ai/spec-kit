"""Contract test: render-evidence geometry has one owner, and pointers around it.

Failure mode this prevents
--------------------------
Headless Chrome's layout viewport comes out ~87-88px shorter than the
``--window-size`` it was given, so a screenshot window sized to the *content*
height silently clips the bottom of the figure — while the "screenshot exists
and is not blank" check still passes and reports the render as proven. Two
engines measured the same shortfall independently (88px and 87px, same task,
same browser), each with its own inlined copy of the command, and no artifact
owned the cross-skill evidence geometry.

The fix put the rule in exactly one place — the seven-skill delivery contract,
D6 row 「渲染证据几何」 — and turned the engine-side copies into pointers. This
test holds both halves, because each half fails on its own:

* owner side: D6 really carries the row, the margin and the bbox alternative.
  Without this the pointer side is vacuously green — three pointers to a row
  that no longer exists still "agree".
* pointer side: every engine site names the owner row and keeps **no** numeric
  margin and **no** hard-coded window size of its own. A second number is a
  second owner, and the two drift the day the measurement is refined.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"

OWNER = SKILLS / "draw-diagram" / "references" / "delivery-contract.md"
OWNER_SECTION = "## D6"
ROW_NAME = "渲染证据几何"
MARGIN = "≥100px"
OWNER_LINK = "draw-diagram/references/delivery-contract.md"

# The sites the introspection finding named, plus the engine guide that inlined
# the same command with a literal window size.
POINTER_SITES = (
    "draw-echarts/SKILL.md",
    "draw-echarts/references/sds-realization.md",
    "draw-echarts/references/echarts-guide.md",
    "draw-d3js/SKILL.md",
)

VENDOR_DIRS = {"node_modules", "__pycache__", ".git", ".venv", ".migration-backups"}

# A hard-coded window size is the defect itself: it either clips tall content or
# over-pads short content, and it silently replaces the owner's margin rule.
HARD_WINDOW_SIZE = re.compile(r"--window-size=\s*\d+\s*,\s*\d+")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _md_files():
    for path in sorted(SKILLS.rglob("*.md")):
        if VENDOR_DIRS & set(path.relative_to(ROOT).parts):
            continue
        yield path


def _d6_section() -> str:
    """D6 by heading prefix — the heading carries its own title after the id."""
    lines = _text(OWNER).splitlines()
    starts = [k for k, ln in enumerate(lines) if ln.startswith(OWNER_SECTION)]
    assert starts, f"{OWNER.relative_to(ROOT)} lost its {OWNER_SECTION!r} heading"
    assert len(starts) == 1, f"{len(starts)} headings start with {OWNER_SECTION!r}, expected one"
    i = starts[0]
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("## ")), len(lines))
    return "\n".join(lines[i:j])


def _row() -> str:
    rows = [ln for ln in _d6_section().splitlines() if ROW_NAME in ln]
    assert rows, f"D6 carries no {ROW_NAME!r} row — the pointers below would be vacuous"
    assert len(rows) == 1, f"D6 carries {len(rows)} {ROW_NAME!r} rows, expected exactly one"
    return rows[0]


# --- owner side (anti-vacuity) ------------------------------------------------


def test_owner_row_exists_inside_d6():
    assert ROW_NAME in _d6_section(), (
        f"{ROW_NAME!r} must live in the D6 self-check table, not elsewhere in the contract"
    )


def test_owner_row_carries_the_margin_exactly_once():
    row = _row()
    assert row.count(MARGIN) == 1, (
        f"the margin {MARGIN!r} must appear exactly once in the D6 row, found {row.count(MARGIN)}"
    )
    assert _text(OWNER).count(MARGIN) == 1, (
        f"the margin {MARGIN!r} must have exactly one home in the owner document"
    )


def test_owner_row_offers_the_bbox_alternative():
    row = _row()
    assert "bbox" in row, "the row must keep the measure-the-drawn-bbox alternative"
    assert "窗口高" in row and "内容高" in row, "the row must state window height vs content height"


def test_owner_row_rejects_the_weak_evidence_check():
    """The check that let the defect through must be named as insufficient — once, here.

    Pointer sites deliberately do NOT restate this: a restated rule at four sites
    is four copies to drift, and the pointer already sends the reader here.
    """
    assert "不构成" in _row(), "the D6 row must state that a non-blank screenshot is not evidence"


def test_margin_has_no_second_home_in_any_skill_markdown():
    offenders = [
        str(p.relative_to(ROOT)) for p in _md_files() if p != OWNER and MARGIN in _text(p)
    ]
    assert not offenders, (
        f"{MARGIN!r} is owned by the delivery contract D6 row; also found in: {offenders}"
    )


def test_no_skill_markdown_hardcodes_a_window_size():
    hits = []
    for path in _md_files():
        for lineno, line in enumerate(_text(path).splitlines(), 1):
            for m in HARD_WINDOW_SIZE.finditer(line):
                hits.append(f"{path.relative_to(ROOT)}:{lineno}: {m.group(0)}")
    assert not hits, (
        "a literal --window-size=<w>,<h> re-inlines the clipped-screenshot defect; size the "
        "window from the D6 row instead:\n" + "\n".join(hits)
    )


# --- pointer side ------------------------------------------------------------


@pytest.mark.parametrize("rel", POINTER_SITES)
def test_pointer_site_names_the_owner_row(rel):
    text = _text(SKILLS / rel)
    assert ROW_NAME in text, f"{rel} must point at the D6 {ROW_NAME!r} row by name"
    assert OWNER_LINK in text, f"{rel} must reach the owner by path ({OWNER_LINK})"
