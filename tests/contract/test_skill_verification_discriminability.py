"""Contract test: create-skills' verification gates must be discriminating.

Failure mode this prevents
--------------------------
Two gates that read as verification but prove nothing:

* `pressure-testing.md` §0 only declared a run **inconclusive** *after* both
  arms had already produced the same outcome — a post-hoc remedy. For a
  front-door / routing skill there is a pre-hoc topic-selection rule that decides
  whether the scenario can discriminate at all: if every lower layer's
  `description` clue points the same way, both arms route identically whether or
  not the front door was read, so the pair cannot separate "the front door
  routed" from "the host picked a delegate on its own".
* `SKILL.md` §6 said *which* suite to run and what to do when `tests/` is absent,
  but not how to read a red one. When several skills of the same family are
  edited in parallel, an unattributed pass/fail count cannot be routed back to
  its author — the exact shape of a triaged item that was reported dispatched and
  never actually executed.

Pinned here: the front-door rule sits in the **pre-dispatch** section, the two
reference files point at each other (互指 — a one-way link leaves the layering doc
silently unenforced), and §6 carries the attribution step with its command.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
CREATE = ROOT / "skills" / "create-skills"
SKILL = CREATE / "SKILL.md"
PRESSURE = CREATE / "references" / "pressure-testing.md"
LAYERING = CREATE / "references" / "name-collision-and-layering.md"

WRONG_WAY = "lower-layer `description` clues point the wrong way"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, start: str, stop: str) -> str:
    """Window between two headings, so a rule cannot be credited from elsewhere."""
    lines = text.splitlines()
    i = next((k for k, ln in enumerate(lines) if ln.startswith(start)), None)
    assert i is not None, f"heading {start!r} missing"
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith(stop)), len(lines))
    return "\n".join(lines[i:j])


# --- the pre-hoc scenario rule ----------------------------------------------


def test_front_door_rule_lives_in_the_pre_dispatch_section():
    sec = _section(_text(PRESSURE), "### 0.", "### 1.")
    assert "Pre-dispatch" in sec.splitlines()[0], (
        "§0 must stay the pre-dispatch section — the rule is worthless once both arms ran"
    )
    assert "front door" in sec.lower(), "§0 must address front-door / routing-layer skills"
    assert WRONG_WAY in sec, "§0 must require a scenario the lower-layer clues mis-route"
    assert "MUST" in sec, "the scenario rule must be normative, not advice"
    assert "inconclusive" in sec, "a non-discriminating scenario must be recorded inconclusive"


def test_front_door_rule_is_declared_before_the_arms_run():
    """The rule precedes RED/GREEN in the file, not appended after them."""
    text = _text(PRESSURE)
    assert text.index(WRONG_WAY) < text.index("### 1. RED"), (
        "the selection rule must appear before the RED arm, or it reads as post-hoc triage"
    )


# --- 互指: both documents reach each other ----------------------------------


def test_pressure_testing_points_at_the_layering_split():
    sec = _section(_text(PRESSURE), "### 0.", "### 1.")
    assert "name-collision-and-layering.md" in sec, "§0 must name the doc that defines the split"
    assert "§2" in sec, "§0 must point at the layering section, not the whole file"


def test_layering_points_back_at_the_scenario_rule():
    sec = _section(_text(LAYERING), "## 2.", "## 3.")
    assert "pressure-testing.md" in sec, (
        "the layering doc must point back — a one-way link leaves front-door authors "
        "with no route to the scenario rule"
    )
    assert "§0" in sec, "the back-pointer must name the section that owns the rule"
    assert WRONG_WAY in sec, "the back-pointer must carry the short reminder, not just a path"


# --- the attribution step ---------------------------------------------------


def test_step_6_carries_the_attribution_step():
    sec = _section(_text(SKILL), "### 6. Validate", "### 6.5")
    assert "attribute every red" in sec, "§6 must require attribution before reporting"
    assert "--tb=line" in sec, "§6 must give the command that makes each failure name its skill"
    assert "pre-existing debt" in sec and "regression" in sec, (
        "§6 must separate inherited debt from the new skill's own regression"
    )
    assert "completion report" in sec, "the attribution must land in the report, not stay in the run"


def test_attribution_step_is_a_checklist_item_beside_the_suite_item():
    sec = _section(_text(SKILL), "### 6. Validate", "### 6.5")
    items = [ln for ln in sec.splitlines() if ln.startswith("- [ ]")]
    assert any("attribute every red" in ln for ln in items), (
        "the attribution step must be a checkable item, not prose above the checklist"
    )
    assert any("skill-conformance contract suite" in ln for ln in items), (
        "the suite item this step qualifies must still be present in §6"
    )
