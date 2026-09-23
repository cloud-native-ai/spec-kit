"""Contract test: a hidden edge must never be stacked on an existing visible edge.

Failure mode this prevents
--------------------------
`skills/draw-plantuml/references/sds-realization.md` §2.1 organises hidden
scaffolding as "intent → means → measured boundary", one hidden edge at a time.
A property of the *graph* — a visible `A --> B` plus a reverse `B -[hidden]- A`
forming a 2-cycle, whose reversal dot leaves undecided — is not expressible in
that table, so it was never recorded. Meanwhile the layout guide actively
invited the combination: its back-edge row recommends `-[hidden]-` for feedback
edges, and its hidden-edge section says to write the hidden skeleton before the
real relations. The result is a layout that silently flips between renders with
no rule to appeal to.

Pinned here: the hard rule lives in §2.1 (the geometry owner) and states why the
table could not hold it; the three inviting surfaces in the guides carry a short
reminder plus the owner path rather than a second copy of the reasoning.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
PUML = ROOT / "skills" / "draw-plantuml" / "references"
OWNER = PUML / "sds-realization.md"
LAYOUT = PUML / "guide" / "layout.md"
PLAYBOOK = PUML / "guide" / "large-diagram-playbook.md"

OWNER_LINK = "../sds-realization.md"
CYCLE = "2-环"
WHY_NOT_IN_TABLE = "图结构性质"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section_21() -> str:
    lines = _text(OWNER).splitlines()
    starts = [k for k, ln in enumerate(lines) if ln.startswith("### 2.1")]
    assert starts, "§2.1 heading missing from the plantuml SDS realization manual"
    i = starts[0]
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("### ")), len(lines))
    return "\n".join(lines[i:j])


# --- the owner rule ---------------------------------------------------------


def test_hard_rule_lives_in_section_21():
    sec = _section_21()
    assert "硬规则" in sec, "§2.1 must carry the hard rule next to the table it qualifies"
    assert "MUST NOT" in sec and "反向" in sec and "hidden" in sec, (
        "the rule must forbid stacking a reverse hidden edge on an existing visible one"
    )
    assert CYCLE in sec and "不确定" in sec, "the rule must name the 2-cycle and dot's undecided reversal"


def test_hard_rule_gives_the_replacement():
    sec = _section_21()
    assert "不可见锚点列" in sec and "hidden down 链" in sec, (
        "a bare prohibition with no alternative invites the author back to the hidden edge"
    )


def test_hard_rule_says_why_the_table_could_not_hold_it():
    sec = _section_21()
    assert WHY_NOT_IN_TABLE in sec, (
        "the rule must record that it is a graph-structure property, outside the "
        "table's one-edge-per-row reach — otherwise it gets folded back in and lost"
    )
    offenders = [
        str(p.relative_to(ROOT))
        for p in sorted((ROOT / "skills").rglob("*.md"))
        if "node_modules" not in p.parts and p != OWNER and WHY_NOT_IN_TABLE in _text(p)
    ]
    assert not offenders, f"the rationale is owned by §2.1; also found in: {offenders}"


# --- the inviting surfaces point at the owner -------------------------------


def _window(path: Path, anchor: str, mode: str) -> str:
    """Narrow window around an anchor: one table row, or one whole section.

    Deliberately narrow so a pointer sitting elsewhere in the same file cannot
    make the pin pass.
    """
    lines = _text(path).splitlines()
    hits = [k for k, ln in enumerate(lines) if anchor in ln]
    assert hits, f"{path.name} lost the anchor {anchor!r} this pin hangs on"
    i = hits[0]
    if mode == "line":
        return lines[i]
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("#")), len(lines))
    return "\n".join(lines[i:j])


@pytest.mark.parametrize(
    "path,anchor,mode",
    [
        (LAYOUT, "**回边 / 反馈边**", "line"),
        (LAYOUT, "### 2.6 隐藏连线强制布局", "section"),
        (PLAYBOOK, "#### 4c.", "section"),
    ],
    ids=["layout-back-edge-row", "layout-hidden-edge-section", "playbook-4c"],
)
def test_inviting_surface_points_at_the_owner(path: Path, anchor: str, mode: str):
    window = _window(path, anchor, mode)
    assert CYCLE in window, f"{path.name}: the {anchor!r} surface must name the 2-cycle hazard"
    assert OWNER_LINK in window, f"{path.name}: the {anchor!r} surface must reach the owner by path"
