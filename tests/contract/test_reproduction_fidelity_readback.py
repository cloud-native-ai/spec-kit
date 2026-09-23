"""Contract test: reproduction fidelity is verified by read-back diff, not by eye.

Failure mode this prevents
--------------------------
The draw-d3js reproduction pipeline fixed the *input* side (measure the source
image into the SDS) and the *internal* side (validate coordinates against the
SDS), but nothing ever connected the rendered pixels back to the source image.
Fidelity could therefore only be *asserted* — "looks like the original" — and
the delivery checklist made it worse: every item was unconditional, so under
`fidelity_intent=reproduction` an item the source image does not have (a legend
swatch, an always-on edge-label toggle) pressured the author to deviate from the
source in order to tick a box.

Pinned here: §4's third gate (render read-back ↔ source diff) exists with its
quantified-tolerance and convergence requirements, it reaches the render-evidence
geometry owner by pointer instead of sizing its own window, the two Cycle-4 R1
todos are absorbed rather than left dangling as "still to do", and the checklist
carries the N/A general rule.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
D3JS = ROOT / "skills" / "draw-d3js"
SDS = D3JS / "references" / "sds-realization.md"
SKILL = D3JS / "SKILL.md"
CYCLE4 = D3JS / "references" / "cycle4-improvements.md"

GATE_NAME = "关三：渲染读回 ↔ 源图差量"
OWNER_ROW = "渲染证据几何"
OWNER_LINK = "draw-diagram/references/delivery-contract.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str, next_prefix: str = "## ") -> str:
    lines = text.splitlines()
    starts = [k for k, ln in enumerate(lines) if ln.startswith(heading)]
    assert starts, f"{heading!r} heading missing"
    i = starts[0]
    j = next(
        (k for k in range(i + 1, len(lines)) if lines[k].startswith(next_prefix)),
        len(lines),
    )
    return "\n".join(lines[i:j])


def _gate() -> str:
    sec = _section(_text(SDS), "## 4.")
    assert GATE_NAME in sec, f"§4 lost {GATE_NAME!r} — fidelity falls back to eyeballing"
    return sec[sec.index(GATE_NAME):]


# --- the third gate ----------------------------------------------------------


def test_section_4_declares_three_gates():
    text = _text(SDS)
    assert "三道关" in _section(text, "## 4."), "§4 must declare three gates"
    assert "两道关" not in text, "a stale '两道关' count survived somewhere in the file"


def test_gate_three_compares_against_the_source_image():
    gate = _gate()
    for needle in ("连通域", "像素", "源图"):
        assert needle in gate, f"gate three must carry the {needle!r} comparison"


def test_gate_three_requires_a_quantified_tolerance():
    gate = _gate()
    assert "容差" in gate and "MUST 给数" in gate, "the tolerance must be quantified, not vibes"
    assert "没有可继承的默认值" in gate, (
        "the gate must say the tolerance has no inheritable default, so a run cannot "
        "silently pass on somebody else's number"
    )
    assert "MUST NOT 充当实测值" in gate, "visual judgement must not stand in for a measurement"


def test_gate_three_requires_convergence_not_a_single_pass():
    gate = _gate()
    assert "迭代收敛" in gate, "the gate must iterate to convergence"
    assert "单次通过不算收敛" in gate, "one green pass must not be recorded as convergence"


def test_gate_three_reaches_the_evidence_geometry_owner_by_pointer():
    gate = _gate()
    assert OWNER_ROW in gate, f"gate three must name the owner's {OWNER_ROW!r} row"
    assert OWNER_LINK in gate, "gate three must reach the owner by path"
    assert "≥100px" not in _text(SDS), "the margin value is owned by the contract, not copied here"


# --- the two Cycle-4 R1 todos are absorbed, not dangling ---------------------


def test_cycle4_todos_are_marked_absorbed():
    text = _text(CYCLE4)
    assert "dated record" in text.lower(), "cycle4 must declare itself a dated record"
    assert text.count("已收编") == 2, (
        f"exactly two R1 todos were absorbed into gate three, found {text.count('已收编')}"
    )
    assert "sds-realization.md" in text, "the absorbed todos must point at the gate that owns them"
    assert "§4 关三第 7 条" in text and "§4 关三第 6 条" in text, (
        "each absorbed todo must name the gate item that replaced it"
    )


# --- the checklist's N/A general rule ---------------------------------------


def _checklist_lead() -> str:
    text = _text(SKILL)
    sec = _section(text, "## Quality Checklist")
    first_item = sec.index("- [ ]")
    return sec[:first_item]


def test_checklist_carries_the_reproduction_general_rule():
    lead = _checklist_lead()
    assert "总则" in lead, "the general rule must precede the checklist items, not hide among them"
    assert "fidelity_intent=reproduction" in lead, "the rule must name its firing condition"
    assert "**N/A**" in lead, "a non-applicable item must be marked N/A explicitly"
    assert "MUST NOT 为了凑满清单而偏离源图" in lead, (
        "ticking a box must never justify deviating from the source image"
    )
    assert "承载" in lead, "the rule must say who carries the semantics the source image lacks"
