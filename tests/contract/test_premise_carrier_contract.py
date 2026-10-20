"""Contract test: environment-premise carrier rules and red-first note shape.

063-review-p1-governance, US6 (C-16/C-17/C-18/C-19, FR-018/FR-024/FR-025/FR-029,
SC-009/SC-011/SC-012).

C-16 — create-tasks SKILL § Environment probe rules item 2 ("Single landing
       point") replaces the CLOSED carrier enumeration ("Per-phase prerequisites
       and `[~]` task notes") with an OPEN list that also covers any
       assumption/decision or free-prose row, so the "MUST reference §
       Environment Prerequisites instead of restating verdicts" duty cannot be
       escaped by sitting in an unlisted carrier.
C-17 — tasks-template § Environment Prerequisites ACTION REQUIRED gains: any row
       restating an environment verdict — in ANY carrier — MUST carry an ISO
       date stamp AND a `(see § Environment Prerequisites)` pointer; both
       together, neither alone.
C-18 — the red-first evidence note's shape rule (owned by create-tasks SKILL §
       Runtime-evidence landing points, where the note's content prescription
       lives) MUST require that when the note binds a claim to a gate, it quotes
       the gate row VERBATIM (id + name + check command); a bare gate id alone
       MUST NOT be used, so a later renumbering produces a visible mismatch.
       Forward-applicable only; 062's note instance is out of scope.
C-19 — create-tasks SKILL § Re-freeze timing MUST point at the implement-side
       consumer step (the pre-flight duty contracted in C-29) instead of
       describing a duty it cannot itself execute; it RETAINS the producer-side
       re-capture obligation.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL = REPO_ROOT / "skills" / "internal" / "create-tasks" / "SKILL.md"
TEMPLATE = REPO_ROOT / "templates" / "tasks-template.md"


def _skill_text() -> str:
    return SKILL.read_text(encoding="utf-8")


def _template_text() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def _item2(skill_text: str) -> str:
    m = re.search(r"(?ms)^\d+\.\s+\*\*Single landing point\*\*.*?(?=^\d+\.|^### |\Z)",
                  skill_text)
    assert m, "create-tasks SKILL lacks the 'Single landing point' item (item 2)"
    return m.group(0)


def _landing_points(skill_text: str) -> str:
    m = re.search(r"(?ms)^\*\*Runtime-evidence landing points.*?(?=^\*\*Re-freeze timing|Create `notes/`|\Z)",
                  skill_text)
    assert m, "create-tasks SKILL lacks the 'Runtime-evidence landing points' block"
    return m.group(0)


def _refreeze(skill_text: str) -> str:
    m = re.search(r"(?ms)\*\*Re-freeze timing\*\*.*?(?=^\*\*Special phase shapes|\Z)",
                  skill_text)
    assert m, "create-tasks SKILL lacks the 'Re-freeze timing' paragraph"
    return m.group(0)


def _action_required(template_text: str) -> str:
    m = re.search(r"(?ms)^## Environment Prerequisites\s*\n(.*?)^## ", template_text)
    assert m, "tasks-template lacks the '## Environment Prerequisites' section"
    return m.group(1)


# --------------------------------------------------------------------------- #
# C-16 — the carrier list is open
# --------------------------------------------------------------------------- #

def test_c16_item2_no_longer_names_only_the_two_closed_carriers():
    item = _item2(_skill_text())
    closed_form = re.search(r"Per-phase prerequisites and `\[\~\]` task notes\s+MUST", item)
    assert not closed_form, (
        "item 2 still carries the closed two-carrier enumeration — the duty must "
        "not be escapable by sitting in an unlisted carrier"
    )


def test_c16_item2_covers_assumption_decision_and_free_prose():
    item = _item2(_skill_text())
    assert re.search(r"assumption", item, re.I), "the open list MUST cover assumptions"
    assert re.search(r"decision", item, re.I), "the open list MUST cover decisions"
    assert re.search(r"free.prose|自由散文|散文", item, re.I), (
        "the open list MUST cover free-prose rows"
    )
    assert re.search(r"per-phase", item, re.I) and re.search(r"\[~\]", item), (
        "the previously listed carriers stay covered (the list opens, it does not shrink)"
    )


def test_c16_item2_keeps_the_reference_instead_of_restate_duty():
    item = _item2(_skill_text())
    assert re.search(r"MUST reference .*Environment Prerequisites|"
                     r"MUST\s+reference that section", item), (
        "the 'reference instead of restating' duty itself MUST survive the opening"
    )


# --------------------------------------------------------------------------- #
# C-17 — restating rows carry date + pointer, both together
# --------------------------------------------------------------------------- #

def test_c17_action_required_declares_date_and_pointer():
    block = _action_required(_template_text())
    assert re.search(r"ISO date", block), "the ISO date stamp MUST be required"
    assert re.search(r"\(see § Environment Prerequisites\)", block), (
        "the `(see § Environment Prerequisites)` pointer MUST be required verbatim"
    )


def test_c17_both_together_neither_alone():
    block = _action_required(_template_text())
    assert re.search(r"both together|两者同时|neither alone|缺一不合规", block), (
        "the rule MUST state both requirements together — either alone is "
        "non-compliant (Edge Cases)"
    )


def test_c17_rule_reaches_any_carrier():
    block = _action_required(_template_text())
    assert re.search(r"any carrier|任何载体|in any carrier", block, re.I), (
        "the date+pointer rule MUST apply to rows in ANY carrier, not only the "
        "two originally listed"
    )


# --------------------------------------------------------------------------- #
# C-18 — red-first note quotes the gate row verbatim
# --------------------------------------------------------------------------- #

def test_c18_note_shape_rule_requires_verbatim_gate_row_quote():
    landing = _landing_points(_skill_text())
    red_first = re.search(r"(?ms)red-first-evidence\.md.*?(?=^- \*\*|^\Z)", landing)
    assert red_first, "the red-first-evidence landing bullet must be locatable"
    rule = red_first.group(0) + landing
    assert re.search(r"quote the gate row verbatim|逐字引用 gate 行", rule, re.I), (
        "a note binding a claim to a gate MUST quote the gate row verbatim"
    )
    for part in (r"id", r"name", r"check command"):
        assert re.search(part, rule, re.I), (
            f"the verbatim quote MUST include the gate row's {part}"
        )


def test_c18_bare_gate_id_alone_is_forbidden():
    landing = _landing_points(_skill_text())
    assert re.search(r"bare gate id.*MUST NOT|裸 gate id.*不可|"
                     r"MUST NOT[^.]*bare gate id|裸 id", landing, re.I | re.S), (
        "a bare gate id alone MUST NOT be usable, so renumbering produces a "
        "visible mismatch"
    )


def test_c18_forward_applicable_only_062_out_of_scope():
    landing = _landing_points(_skill_text())
    assert re.search(r"forward.applicable|前向适用", landing, re.I), (
        "the rule MUST be declared forward-applicable only"
    )
    assert re.search(r"062.*out of scope|062.*不在|out of scope.*062", landing, re.I | re.S), (
        "062's note instance MUST be declared out of scope (never retro-edited)"
    )


# --------------------------------------------------------------------------- #
# C-19 — re-freeze timing points at the implement-side consumer
# --------------------------------------------------------------------------- #

def test_c19_refreeze_points_at_the_implement_preflight():
    para = _refreeze(_skill_text())
    assert re.search(r"implement.*pre-flight|implement 侧.*预检|Step 0|baseline pre-flight",
                     para, re.I), (
        "Re-freeze timing MUST point at the implement-side consumer step (the "
        "C-29 pre-flight) instead of describing a duty this command cannot execute"
    )


def test_c19_producer_side_recapture_obligation_retained():
    para = _refreeze(_skill_text())
    assert re.search(r"re-capture on every generation and every rerun|"
                     r"每次生成与每次重跑.*重捕获|re-capture.*generation.*rerun", para, re.I), (
        "the producer-side re-capture obligation (every generation and every "
        "rerun of this command) MUST be retained"
    )
