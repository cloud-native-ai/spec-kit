"""Contract test: the review loop becomes traceable and owned.

Pins Feature 063 C-11..C-15 (F3, FR-009..FR-013 / SC-005, SC-006):

* C-11 — review Handoffs "After" replaces the ownerless sentence with a named duty:
  every `REC-` is registered in `register.md` in the same commit, using the register's
  pointer-row form.
* C-12 — the ID Register enumeration in `templates/instructions-template.md` adds
  `REC-…`; the live `.specify/instructions.md` receives it through the generator.
* C-13 — `feedback-step.md` § Scope guard keeps `scope: local` and names the existing
  legal intake (manage-feedback Path A digest § A3 自省(Introspection)).
* C-14 — `review-template.md` § 5 and Replacement Rule 3 make the repo-relative path
  the PRIMARY form, absolute only as a parenthetical supplement; external targets are
  marked `external` with a reason.
* C-15 — `feature-integration.md` gains the `/speckit.review` transition row and the
  checklist-row annotation; each command still owns exactly one transition.

Red before the mechanism lands (Tests Mode = ON, Constitution Principle IV).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW_CMD = ROOT / "templates" / "commands" / "review.md"
INSTRUCTIONS_TEMPLATE = ROOT / "templates" / "instructions-template.md"
INSTRUCTIONS_LIVE = ROOT / ".specify" / "instructions.md"
FEEDBACK_STEP = ROOT / "shared" / "workflow" / "feedback-step.md"
REVIEW_TEMPLATE = ROOT / "templates" / "review-template.md"
FEATURE_INTEGRATION = ROOT / "shared" / "workflow" / "feature-integration.md"


def _to_end(text: str, heading: str) -> str:
    m = re.search(rf"(?ms)^{re.escape(heading)}.*\Z", text)
    assert m, f"section {heading!r} not found"
    return m.group(0)


def _section(text: str, start: str, end: str) -> str:
    m = re.search(rf"(?ms)^{start}.*?(?=^{end})", text)
    assert m, f"section {start!r} not found"
    return m.group(0)


# --------------------------------------------------------------------------- #
# C-11 — review handoff owns the REC registration duty
# --------------------------------------------------------------------------- #

def test_c11_handoff_after_names_the_registration_obligation():
    body = REVIEW_CMD.read_text(encoding="utf-8")
    after = _to_end(body, "## Handoffs")
    assert "Apply improvements to spec-kit templates/commands/scripts" not in after, (
        "the ownerless sentence MUST be replaced"
    )
    assert "REC-" in after, "the handoff MUST name the REC- identifier"
    assert "register.md" in after, "the handoff MUST name the register"
    assert re.search(r"same commit|同一提交", after, re.I), (
        "registration MUST be pinned to the same commit"
    )
    assert re.search(r"one-line meaning|一行含义", after, re.I)
    assert re.search(r"report anchor|报告锚点", after, re.I)
    assert re.search(r"status|状态", after, re.I)


# --------------------------------------------------------------------------- #
# C-12 — REC- in the resident instruction layer
# --------------------------------------------------------------------------- #

def test_c12_id_register_enumeration_adds_rec():
    body = INSTRUCTIONS_TEMPLATE.read_text(encoding="utf-8")
    m = re.search(r"(?ms)^## ID Register.*?(?=^## )", body)
    assert m, "ID Register section not found"
    section = m.group(0)
    for prefix in ("D-", "OI-", "S", "T-", "F-", "B-"):
        assert prefix in section, f"the existing enumeration lost {prefix!r}"
    assert "REC-" in section, "the enumeration MUST add the recommendation identifier"


def test_c12_live_instructions_received_rec_through_the_generator():
    assert INSTRUCTIONS_LIVE.is_file()
    live = INSTRUCTIONS_LIVE.read_text(encoding="utf-8")
    m = re.search(r"(?ms)^## ID Register.*?(?=^## )", live)
    assert m, "live instructions have no ID Register section"
    assert "REC-" in m.group(0), (
        "the live .specify/instructions.md MUST carry REC- (generated, never hand-edited)"
    )


# --------------------------------------------------------------------------- #
# C-13 — the legal global-recommendation intake
# --------------------------------------------------------------------------- #

def test_c13_scope_guard_keeps_local_and_names_the_existing_intake():
    body = FEEDBACK_STEP.read_text(encoding="utf-8")
    guard = _section(body, r"3\. \*\*Scope guard\.\*\*", r"4\. \*\*Dedup guard")
    assert "scope: local" in guard, "the local-scope rule MUST be kept"
    assert "/speckit.feedback" in guard, "the legal intake MUST be named"
    assert re.search(r"Path A", guard)
    assert re.search(r"A3 自省|A3 Introspection|Introspection", guard)
    assert re.search(r"no new|MUST NOT.*new|不新建", guard, re.I), (
        "no new intake store/tracking/scoring system may be introduced"
    )


# --------------------------------------------------------------------------- #
# C-14 — repo-relative is the primary REC target form
# --------------------------------------------------------------------------- #

def _recommendations(body: str) -> str:
    return _section(body, r"## 5\.", r"## 6\.")


def _replacement_rule_3(body: str) -> str:
    rules = _section(body, r"## Replacement Rules", r"<!-- End of review template")
    m = re.search(r"(?ms)^3\. .*?(?=^4\. )", rules)
    assert m, "Replacement Rule 3 not found"
    return m.group(0)


def test_c14_section_5_and_rule_3_make_repo_relative_primary():
    body = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    for name, block in (("§ 5", _recommendations(body)),
                        ("Replacement Rule 3", _replacement_rule_3(body))):
        assert re.search(r"repo-relative|repo relative", block, re.I), (
            f"{name} MUST name the repo-relative primary form"
        )
        assert re.search(r"PRIMARY|primary|主形态", block), (
            f"{name} MUST state that repo-relative is the primary form"
        )
        assert re.search(r"absolute|绝对", block, re.I), (
            f"{name} MUST state where the absolute form is allowed"
        )
        assert re.search(r"parenthetical|括号补充", block, re.I), (
            f"{name} MUST demote the absolute form to a parenthetical supplement"
        )


def test_c14_external_targets_are_marked_with_a_reason():
    body = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert re.search(r"\bexternal\b", body), (
        "a target with no repo-relative form MUST be marked `external`"
    )
    assert re.search(r"with (?:its )?reason|并给出理由|给出理由", body, re.I)


def test_c14_absolute_only_instruction_is_not_reintroduced():
    body = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "Every file path is absolute, OR written as" not in body, (
        "the header MUST NOT keep the absolute-only instruction"
    )
    assert "Do not include bare relative paths" not in body, (
        "Replacement Rule 3 MUST NOT keep the absolute-only form"
    )


# --------------------------------------------------------------------------- #
# C-15 — the /speckit.review transition row
# --------------------------------------------------------------------------- #

def _status_table() -> str:
    body = FEATURE_INTEGRATION.read_text(encoding="utf-8")
    return _section(body, r"## Status State Machine", r"## Pre-Status-Flip Gate")


def test_c15_review_owns_the_ready_for_review_transition():
    table = _status_table()
    assert "| `/speckit.review` | `Implemented → Ready for Review` |" in table, (
        "the review transition row MUST be present"
    )
    assert "review.md committed" in table
    assert re.search(r"deferred item resolved or waived", table)


def test_c15_checklist_row_is_annotated_and_keeps_one_transition_per_command():
    table = _status_table()
    checklist_rows = [l for l in table.splitlines() if l.startswith("| `/speckit.checklist`")]
    assert len(checklist_rows) == 1
    assert re.search(r"applies only when|仅在.*之后运行|仅在.*implement", checklist_rows[0]), (
        "the checklist row MUST carry the annotation"
    )
    commands = re.findall(r"(?m)^\|\s*`(/speckit\.[a-z-]+)`\s*\|", table)
    assert len(commands) == len(set(commands)), (
        f"each command MUST own exactly one transition; duplicates: {commands}"
    )
    assert "/speckit.review" in commands


def test_c15_top_command_list_includes_review():
    body = FEATURE_INTEGRATION.read_text(encoding="utf-8")
    first_paragraph = body.split("## Status State Machine")[0]
    assert "/speckit.review" in first_paragraph, (
        "the document's top command list MUST include /speckit.review"
    )
