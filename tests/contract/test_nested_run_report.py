"""Contract tests: the mandatory nested-run section of the team run report (slice 074b, T004).

What this pins
--------------
`contracts/report-and-attribution.md` C-21…C-30 at the decidable face:

1. exactly one mandatory section is added, its heading literal stated verbatim (C-21);
2. the section lists, per invocation, the five fields with a three-valued outcome (C-22);
3. a run with no invocation states that explicitly and never omits the section (C-23);
4. the supervisor is the sole writer and a nested run writes no tracked artifact (C-24);
5. attribution reuses the existing ledger field — exactly one row with a Target, none
   without — and the parsed Goal field set is identical before and after (C-25 / C-26);
6. the section is a peer of `## Verification`, not a replacement (C-27);
7. the routing verdict is consumed by reference and never re-derived (C-28);
8. the handoff's closed field set is read by reference, an incomplete handoff is never a
   successful return, and `blocked` / `failed` are carried through unchanged (C-29);
9. the report contract stays the single owner of the section (C-30).

Measurement rules used below
----------------------------
* The heading literal is judged on a **line-exact** match, so a synonym, a level change or
  an embedded mention in a paragraph cannot satisfy it.
* The "one landing point" audit counts **documents**, not occurrences: the claim is that one
  shipped source document owns the literal, and mirrors under `.specify/` are generated
  projections of those sources rather than additional owners.
* "The existing mandatory sections are unchanged" is judged by extracting the section list
  from the report skeleton and comparing it against the frozen pre-change sequence, plus a
  byte-exact match of the pre-change section-list line.
* The Goal field-set claim is executed, not asserted: `goal-utils.parse_goal` is run over the
  `074a` fixture Goal before and after the supervisor's ledger attribution row.

Red shape (recorded in `notes/red-first-evidence.md`): the section does not exist yet, so every
case below fails as a missing section, not as a contradictory assertion.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

from fixtures.nested_sdd import build

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
CREATE_TEAM = REPO_ROOT / "skills" / "internal" / "create-team" / "SKILL.md"
RUN_TEAM = REPO_ROOT / "skills" / "internal" / "run-team" / "SKILL.md"
RUN_AGENT = REPO_ROOT / "skills" / "internal" / "run-agent" / "SKILL.md"
GOAL_ENGINE = REPO_ROOT / "scripts" / "python" / "goal-utils.py"

#: `[[STR-007]]` — the heading literal, verbatim (`requirements.md` § Shared Strings).
HEADING_LITERAL = "## Nested SDD Runs"
SECTION_TITLE = "Nested SDD Runs"

#: The report-contract subsection that states the obligation. Titled so that the verbatim
#: level-2 literal above keeps exactly one line-exact occurrence in this document.
SUBSECTION_TITLE = "Nested SDD Runs section"

#: The pre-change mandatory section list, in its pre-change order (measured at `241a6082b`).
EXISTING_SECTIONS = (
    "Result Summary",
    "Deliverables",
    "Verification",
    "Execution Detail",
    "Run Workspace",
    "Summary",
)
EXISTING_SECTION_LIST_LINE = "## " + " ## ".join(EXISTING_SECTIONS)

#: `[[STR-004]]` / `[[STR-005]]` / `[[STR-006]]` — the closed outcome set.
OUTCOME_STRINGS = ("STR-004", "STR-005", "STR-006")

#: C-22's five per-invocation fields, as the contract must name them.
PER_INVOCATION_FIELDS = (
    "outcome",
    "artifact paths",
    "evidence paths",
    "routing-verdict reference",
    "anomalies",
)

#: The surfaces whose documents may own a shipped definition point. `.specify/` copies are
#: generated projections (`sync-mirrors.py`) and are therefore not definition points.
SOURCE_SURFACES = ("skills", "shared", "templates", "agents")

#: `parse_goal`'s key set at the pre-change commit — the Goal field set SC-002 compares.
GOAL_FIELD_SET = {
    "slug",
    "title",
    "status",
    "created",
    "updated",
    "objective",
    "criteria",
    "history",
    "criteria_count",
    "boundaries",
    "targets",
    "subjects",
}

#: A ledger attribution row in the existing shape (`summary-mapping.md` § 6), carrying the
#: existing attribution field. Nothing here is a new field: each key is that table's.
ATTRIBUTED_ROW = {
    "item_id": "TI-0001",
    "title": "nested SDD run reached review",
    "phase_ref": "PH-0001",
    "state": "completed",
    "provenance": ".specify/teams/fixture-team/runs/20261029T000000Z-report.md#nested-sdd-runs",
    "ts": "2026-10-29T00:00:00Z",
    "identity": "explicit",
    "target_ref": "T-001",
}


# ---------------------------------------------------------------------------
# Parsing helpers — fence-aware, so the report skeleton's `## ` tokens are read
# as template text and never confused with real document headings.
# ---------------------------------------------------------------------------


def _read(path: Path) -> str:
    assert path.is_file(), f"missing document: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def _fence_aware_lines(text: str) -> list:
    """`[(lineno, line, in_fence)]` — fence markers themselves flagged as inside."""
    rows = []
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            rows.append((lineno, line, True))
            continue
        rows.append((lineno, line, in_fence))
    return rows


def _heading_blocks(text: str) -> list:
    """`[(level, title, body)]` over real headings only (fenced template text skipped)."""
    lines = text.splitlines()
    flags = [inside for _lineno, _line, inside in _fence_aware_lines(text)]
    heads = [
        (index, len(line) - len(line.lstrip("#")), line.lstrip("#").strip())
        for index, line in enumerate(lines)
        if line.startswith("#") and not flags[index]
    ]
    blocks = []
    for position, (index, level, title) in enumerate(heads):
        end = len(lines)
        for later_index, later_level, _later_title in heads[position + 1 :]:
            if later_level <= level:
                end = later_index
                break
        blocks.append((level, title, "\n".join(lines[index + 1 : end])))
    return blocks


def _block(path: Path, title: str):
    hits = [
        block
        for block in _heading_blocks(_read(path))
        if block[1].startswith(title) or block[1].lstrip("§ ").startswith(title)
    ]
    assert len(hits) == 1, (
        f"{path.relative_to(REPO_ROOT)} must carry exactly one '{title}' section, found "
        f"{[hit[1] for hit in hits]}"
    )
    return hits[0]


def _own_body(body: str) -> str:
    """A section body cut at its first nested heading (sub-tables never leak upward)."""
    for line in body.splitlines():
        if line.startswith("#"):
            return body[: body.index(line)]
    return body


def _subsection() -> str:
    """The report-contract subsection that owns the nested-run obligation."""
    return _block(CREATE_TEAM, SUBSECTION_TITLE)[2]


def _report_skeleton() -> str:
    """The fenced report template inside the report contract."""
    body = _block(CREATE_TEAM, "Report contract")[2]
    fences = []
    current = None
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            if current is None:
                current = []
            else:
                fences.append("\n".join(current))
                current = None
            continue
        if current is not None:
            current.append(line)
    hits = [fence for fence in fences if fence.lstrip().startswith("# Team Run Report")]
    assert len(hits) == 1, (
        "the report contract must carry exactly one fenced report skeleton beginning "
        f"'# Team Run Report', found {len(hits)}"
    )
    return hits[0]


def _section_tokens(block: str) -> list:
    """Every `## <name>` token of a template block, in order."""
    tokens = []
    for line in block.splitlines():
        for match in re.finditer(r"##\s+([^#\n]+?)(?=\s*##\s|\s*$)", line):
            tokens.append(match.group(1).strip())
    return tokens


def _documents_carrying(literal: str) -> list:
    """Relative paths of every shipped-source markdown document containing ``literal``."""
    hits = []
    for surface in SOURCE_SURFACES:
        for path in sorted((REPO_ROOT / surface).rglob("*.md")):
            if literal in path.read_text(encoding="utf-8", errors="ignore"):
                hits.append(str(path.relative_to(REPO_ROOT)))
    return hits


def _goal_engine():
    spec = importlib.util.spec_from_file_location("goal_utils_nested_report", GOAL_ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["goal_utils_nested_report"] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# C-21 — exactly one added section, heading literal verbatim, appended not inserted
# ---------------------------------------------------------------------------


def test_heading_literal_is_stated_verbatim_and_line_exact():
    text = _read(CREATE_TEAM)
    exact = [line for line in text.splitlines() if line.strip() == HEADING_LITERAL]
    assert len(exact) == 1, (
        f"the report contract MUST state {HEADING_LITERAL!r} verbatim on its own line "
        f"exactly once (C-21); found {len(exact)} line-exact occurrences"
    )
    for synonym in (
        "## Nested SDD Run\n",
        "### Nested SDD Runs\n",
        "## Nested Sdd Runs\n",
        "## nested sdd runs\n",
    ):
        assert synonym not in text, (
            f"a synonym or level change of the heading literal is a violation (C-21): "
            f"{synonym!r} found"
        )


def test_the_literal_lands_in_exactly_one_shipped_source_document():
    holders = _documents_carrying(HEADING_LITERAL)
    assert holders == ["skills/internal/create-team/SKILL.md"], (
        "the heading literal MUST have exactly one definition point, the report contract "
        f"(C-21 / C-30); documents carrying it: {holders}"
    )
    assert HEADING_LITERAL not in _read(RUN_TEAM), (
        "`run-team` keeps delegating its report duty by path and MUST NOT state the section "
        "a second time (C-30)"
    )


def test_the_section_is_appended_after_an_unchanged_section_list():
    skeleton = _report_skeleton()
    tokens = _section_tokens(skeleton)
    assert tuple(tokens[: len(EXISTING_SECTIONS)]) == EXISTING_SECTIONS, (
        "the existing mandatory sections MUST keep their names and order unchanged (C-21); "
        f"expected the pre-change sequence {list(EXISTING_SECTIONS)}, got {tokens}"
    )
    assert tuple(tokens) == EXISTING_SECTIONS + (SECTION_TITLE,), (
        "the nested section MUST be the one section appended at the end — no rename, no "
        f"merge, no reorder of the existing list (C-21); got {tokens}"
    )
    assert EXISTING_SECTION_LIST_LINE in skeleton, (
        "the pre-change section-list line MUST survive byte-identically (C-21); appending a "
        "section is an addition, not a rewrite of the existing list"
    )
    level, title, _body = _block(CREATE_TEAM, SUBSECTION_TITLE)
    assert title.startswith(SUBSECTION_TITLE) and level == 3, (
        "the obligation MUST be stated inside the report contract as a subsection "
        f"(H3), found H{level} '{title}'"
    )


# ---------------------------------------------------------------------------
# C-21 / C-23 — mandatory for every run; explicit when empty
# ---------------------------------------------------------------------------


def test_section_is_mandatory_for_every_run_in_both_pattern_families():
    body = _subsection()
    assert re.search(r"每次运行|every run", body), (
        "the section MUST be mandatory for every run, not only for runs that nested (C-21)"
    )
    assert re.search(r"有界|bounded", body), (
        "the obligation MUST name the bounded patterns explicitly (C-21)"
    )
    assert "continuous" in body, (
        "the obligation MUST name the continuous pattern explicitly (C-21)"
    )
    assert re.search(r"MUST NOT 省略|不得省略|MUST NOT omit", body), (
        "the obligation MUST forbid omitting the section (C-21 / C-23)"
    )


def test_no_invocation_is_stated_explicitly_and_omission_is_a_violation():
    body = _subsection()
    assert re.search(r"本次无嵌套 SDD 调用|no nested SDD invocation", body), (
        "a run with no nested invocation MUST state that explicitly inside the section "
        "(C-23)"
    )
    assert re.search(r"(省略)[^。.]{0,40}(违约|violation)", body), (
        "an omitted section MUST be a contract violation even when the correct content "
        "would have been 'none' (C-23)"
    )


# ---------------------------------------------------------------------------
# C-22 — the five per-invocation fields and the closed outcome set
# ---------------------------------------------------------------------------


def test_per_invocation_row_carries_five_fields_and_the_closed_outcome_set():
    body = _subsection()
    for field in PER_INVOCATION_FIELDS:
        assert field in body, (
            f"the section MUST list the per-invocation field {field!r} (C-22)"
        )
    for string_id in OUTCOME_STRINGS:
        assert f"[[{string_id}]]" in body, (
            f"the outcome MUST be drawn from the closed three-value set; [[{string_id}]] "
            f"is not named (C-22)"
        )
    assert re.search(r"三值|three values|封闭集|closed set", body), (
        "the outcome set MUST be declared closed (C-22)"
    )
    assert re.search(r"第四值|fourth value", body), (
        "the obligation MUST rule out a fourth value or free text (C-22)"
    )


def test_blocked_and_failed_are_carried_through_never_dressed_as_success():
    body = _subsection()
    for string_id in OUTCOME_STRINGS[1:]:
        assert f"[[{string_id}]]" in body, (
            f"the section MUST name [[{string_id}]] as an outcome it carries through (C-22)"
        )
    assert re.search(r"MUST NOT[^。.]{0,40}改写成成功|不得[^。.]{0,20}改写", body), (
        "a blocked or failed run MUST NOT be rewritten into a successful-sounding sentence "
        "(C-22)"
    )
    assert re.search(r"原样|verbatim", body), (
        "the blocked/failed outcome is carried through unchanged (C-22 / C-29)"
    )


def test_paths_are_carried_as_paths_and_bodies_are_never_inlined():
    body = _subsection()
    assert re.search(r"MUST NOT[^。.]{0,20}内联|never inlines", body), (
        "the section MUST NOT inline artifact bodies — paths are carried as paths (C-22)"
    )
    assert re.search(r"路径", body), (
        "the artifact and evidence entries are paths (C-22)"
    )


# ---------------------------------------------------------------------------
# C-27 — peer of the verification section, not a replacement
# ---------------------------------------------------------------------------


def test_nested_section_is_a_peer_of_verification_not_a_replacement():
    body = _subsection()
    assert "`## Verification`" in body, (
        "the obligation MUST name `## Verification` as the section it sits beside (C-27)"
    )
    assert re.search(r"并列|peer", body), (
        "the nested section MUST be a peer of the verification section (C-27)"
    )
    assert re.search(r"不解除|does not discharge", body), (
        "a nested run's verification evidence MUST NOT discharge the enclosing run's "
        "verification duty (C-27)"
    )
    verification = _own_body(_block(CREATE_TEAM, "Verification")[2])
    assert re.search(r"回归数字注明口径|同口径|One-Source-Of-Truth|One Source Of Truth", verification), (
        "the verification section keeps its existing content obligations (C-27): its "
        "three criteria are still stated"
    )


# ---------------------------------------------------------------------------
# C-28 — the verdict is a reference; a missing record is never re-derived
# ---------------------------------------------------------------------------


def test_routing_verdict_is_a_reference_and_a_missing_record_is_never_rederived():
    body = _subsection()
    assert re.search(r"执行证据|execution evidence", body), (
        "the reference points at the verdict 074a recorded in the Agent execution evidence "
        "(C-28)"
    )
    assert "sdd-route.py" in body, (
        "the producer of that record MUST be cited (C-28)"
    )
    assert re.search(r"MUST NOT[^。.]{0,20}复制|MUST NOT[^。.]{0,30}重算", body), (
        "the section MUST NOT copy the input set / verdict table / reason-code vocabulary "
        "and MUST NOT re-derive the verdict (C-28)"
    )
    assert "missing" in body, (
        "when the recorded verdict cannot be located the reference is recorded as missing "
        "(C-28)"
    )


# ---------------------------------------------------------------------------
# C-29 — handoff field set by reference; an incomplete handoff is never success
# ---------------------------------------------------------------------------


def test_handoff_fields_are_read_by_reference_and_an_incomplete_handoff_is_not_success():
    body = _subsection()
    assert "nested-invocation.md" in body, (
        "the handoff's closed field set is owned by the driver's `nested-invocation.md` and "
        "reached by reference (C-29)"
    )
    assert "incomplete handoff" in body, (
        "a handoff with no integration identity MUST be named an incomplete handoff (C-29)"
    )
    assert re.search(r"MUST NOT[^。.]{0,30}报成功|never a successful return", body), (
        "an incomplete handoff MUST NOT be reported as success, whatever its outcome value "
        "(C-29)"
    )


# ---------------------------------------------------------------------------
# C-24 — sole writer; the nested run writes no tracked artifact
# ---------------------------------------------------------------------------


def test_supervisor_is_the_sole_writer_and_a_nested_run_writes_no_tracked_artifact():
    body = _subsection()
    assert re.search(r"唯一写者|sole writer", body), (
        "the team supervisor is the sole writer of the section (C-24)"
    )
    assert re.search(r"不写任何 tracked 工件|writes no tracked artifact", body), (
        "a nested run MUST NOT write a tracked artifact (C-24)"
    )
    for forbidden_write in ("报告", "goal", "spec 目录"):
        assert forbidden_write in body, (
            f"the prohibition MUST name the {forbidden_write!r} write a nested run never "
            f"performs (C-24)"
        )
    assert "handoff" in body, (
        "the nested run's product is the returned handoff, consumed by the supervisor "
        "(C-24)"
    )


# ---------------------------------------------------------------------------
# C-25 / C-26 / SC-002 — attribution by the existing ledger field, Goal set unchanged
# ---------------------------------------------------------------------------


def test_attribution_reuses_the_existing_ledger_field_and_adds_no_goal_field():
    body = _subsection()
    assert "target_ref" in body, (
        "the attribution row carries the ledger's existing `target_ref` field (C-25)"
    )
    assert "summary-mapping.md" in body, (
        "the field's owner MUST be cited rather than restated (C-25, one source of truth)"
    )
    assert re.search(r"MUST NOT 新增 Goal 字段|no new Goal field", body), (
        "the section MUST NOT introduce a Goal field (C-26)"
    )
    assert re.search(r"结构链接|structural link", body), (
        "no structural link from a Goal to a requirements specification is created (C-26)"
    )
    assert re.search(r"完全一致|identical", body), (
        "the parsed Goal field set MUST be stated identical before and after (C-26)"
    )


def test_attribution_is_observational_so_the_goal_field_set_is_unchanged(tmp_path):
    """SC-002's instrument: append the supervisor's row, re-parse the Goal, compare."""
    project = build(tmp_path / "project")
    engine = _goal_engine()

    before = engine.parse_goal(project.goal_path)
    assert set(before) == GOAL_FIELD_SET, (
        "the pre-run Goal field set differs from the frozen 12-key set; a new Goal field "
        f"would appear here (C-26 / SC-002): {sorted(set(before) ^ GOAL_FIELD_SET)}"
    )

    ledger = project.root / ".specify" / "teams" / project.team_slug / "items.jsonl"
    ledger.write_text(json.dumps(ATTRIBUTED_ROW, ensure_ascii=False) + "\n", encoding="utf-8")

    after = engine.parse_goal(project.goal_path)
    assert set(after) == set(before), (
        "attribution MUST be observational: the parsed Goal field set is identical before "
        f"and after the ledger row (C-26 / SC-002); changed keys "
        f"{sorted(set(after) ^ set(before))}"
    )
    assert after == before, (
        "attribution MUST NOT change any parsed Goal value (C-26 / SC-002)"
    )


def test_attribution_cardinality_is_exactly_one_with_a_target_and_none_without():
    body = _subsection()
    assert re.search(r"至多一条|at most one", body), (
        "the cardinality is at most one attributed ledger row per report (C-25)"
    )
    assert re.search(r"恰一条|exactly one", body), (
        "with a declared Target it is exactly one row (C-25 / V-5)"
    )
    assert re.search(r"零条|none", body), (
        "with no declared Target there is no attributed row (C-25 / V-5)"
    )
    assert re.search(r"MUST NOT 臆造|MUST NOT invent", body), (
        "a run that declared no Target MUST NOT invent a placeholder Target (C-26 / V-6); "
        "its row keeps the existing Goal-wide form"
    )


# ---------------------------------------------------------------------------
# C-30 — one owner across the three skill documents
# ---------------------------------------------------------------------------


def test_single_owner_audit_across_the_three_skill_documents():
    holders = [
        str(path.relative_to(REPO_ROOT))
        for path in (CREATE_TEAM, RUN_TEAM, RUN_AGENT)
        if SECTION_TITLE in path.read_text(encoding="utf-8")
    ]
    assert holders == ["skills/internal/create-team/SKILL.md"], (
        "the section MUST have exactly one owner among the three skill documents (C-30); "
        f"documents naming it: {holders}"
    )
    run_team = _read(RUN_TEAM)
    assert "报告契约" in run_team or "Report contract" in run_team, (
        "`run-team` MUST keep delegating its report duty to the report contract by path "
        "(C-30)"
    )
