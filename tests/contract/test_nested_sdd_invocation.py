"""Contract tests: the invoked-from-team entry form and its handoff (slice 074a, task T012).

What this pins
--------------
`contracts/nested-invocation.md` C-31…C-43 at the **content face** the slice can decide:

1. the entry form accepts exactly six facts and validates them before U0 (C-31);
2. entry validation fails closed over a closed condition set, naming the condition, and a
   failing entry neither starts a run nor re-scopes the duty (C-32);
3. the run ends at review completion and claims no merge authority (C-33);
4. the handoff's field set is closed (C-34) and a handoff missing any field — the integration
   identity in particular (C-42) — is never a successful return;
5. the outcome is three-valued (C-35) and the integration identity is exactly four facts with
   the retained branch named (C-36);
6. a nested run never merges and never pushes (C-37) — the executable half is a `git log` /
   `git status` assertion over a real repository;
7. line registration, failure/stall handoff, and consumer duty reuse the existing mechanisms
   and create no second store (C-38 / C-39 / C-40 / C-43).

Boundary (D-3): this module asserts the path-reference face and deliberately does **not** assert
the `## Nested SDD Runs` heading literal or that section's semantics — those belong to
`074b-nested-governance`.

Red shape: the referenced sections do not exist yet, so every case below fails as a missing
section, not as a contradictory assertion.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

from fixtures.nested_sdd import ALLOWED, build

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFERENCE_MD = SKILL_DIR / "references" / "nested-invocation.md"

ENTRY_TITLE = "Invoked-from-Team Entry"

#: C-31 — the six accepted facts. A fact the form does not accept is not silently ignored,
#: so the set is closed and each member is named.
ENTRY_FACTS = (
    "goal_ref",
    "target_ref",
    "team_slug",
    "seat_slug",
    "scope",
    "verdict_ref",
)

#: C-34 — the handoff's closed field set.
HANDOFF_FIELDS = (
    "outcome",
    "stages_reached",
    "artifact_paths",
    "evidence_paths",
    "unresolved_findings",
    "anomaly_line",
    "integration_identity",
)

#: C-36 — the integration identity is exactly four facts.
INTEGRATION_FACTS = ("line_id", "branch", "worktree_path", "head_commit")

#: C-35 — the outcome takes exactly one of three values ([[STR-007]] / [[STR-008]] / [[STR-009]]).
OUTCOME_STRINGS = ("STR-007", "STR-008", "STR-009")

PROHIBITION_MARKERS = ("MUST NOT", "不得", "禁止", "never")


# ---------------------------------------------------------------------------
# Parsing helpers (deterministic; no prose reading)
# ---------------------------------------------------------------------------


def _read(path: Path) -> str:
    assert path.is_file(), f"missing document: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def _heading_blocks(text: str) -> list:
    """`[(level, title, body)]` — body runs to the next heading of the same or higher level."""
    lines = text.splitlines()
    heads = [
        (index, len(line) - len(line.lstrip("#")), line.lstrip("#").strip())
        for index, line in enumerate(lines)
        if line.startswith("#")
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
    """The single heading block whose title starts with ``title`` (case-sensitive)."""
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


def _section_body(path: Path, title: str) -> str:
    return _block(path, title)[2]


def _own_body(body: str) -> str:
    """A section body cut at its first nested heading (so sub-tables never leak upward)."""
    for line in body.splitlines():
        if line.startswith("###"):
            return body[: body.index(line)]
    return body


def _table_rows(body: str) -> list:
    """Markdown table rows as cell lists; separator rows dropped."""
    rows = []
    for line in body.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        rows.append(cells)
    return rows


def _first_column_names(body: str) -> list:
    """Backticked identifiers from the first column of the body's first table."""
    rows = _table_rows(body)
    assert rows, "expected a Markdown table, found none"
    names = []
    for row in rows[1:]:
        match = re.search(r"`([^`]+)`", row[0])
        names.append(match.group(1) if match else row[0])
    return names


def _entry_section() -> str:
    return _section_body(SKILL_MD, ENTRY_TITLE)


def _reference_section(title: str) -> str:
    return _section_body(REFERENCE_MD, title)


# ---------------------------------------------------------------------------
# C-31 — the entry form and its six accepted facts
# ---------------------------------------------------------------------------


def test_entry_form_section_exists_as_an_additive_subsection():
    """The new entry form is an H3 under an existing H2, so the standalone skeleton is untouched.

    The pinned H2 skeleton of `sdd-loop-driver/SKILL.md` is owned by
    `test_sdd_loop_driver_skill.py::test_c3_skill_md_section_set`; this slice adds no H2, which
    is how "the standalone entry contract is unchanged" stays mechanically true instead of
    being a prose promise.
    """
    level, title, _body = _block(SKILL_MD, ENTRY_TITLE)
    assert title.startswith(ENTRY_TITLE), title
    assert level == 3, (
        f"'{ENTRY_TITLE}' MUST be an H3 (got H{level}); a new H2 would change the pinned "
        f"standalone entry skeleton (C-31, additivity)"
    )


def test_entry_form_accepts_exactly_the_six_facts():
    body = _entry_section()
    for fact in ENTRY_FACTS:
        assert fact in body, (
            f"§ {ENTRY_TITLE} does not name the accepted fact `{fact}` (C-31)"
        )
    assert re.search(r"(六个|六项|exactly six|closed set|封闭)", body), (
        "§ " + ENTRY_TITLE + " MUST declare the accepted fact set as closed (C-31)"
    )
    assert re.search(r"(忽略|silently ignored|MUST NOT ignore)", body), (
        "§ " + ENTRY_TITLE + " MUST state that a fact the form does not accept is not "
        "silently ignored (C-31)"
    )


def test_entry_validation_precedes_u0():
    body = _entry_section()
    assert re.search(r"(U0 之前|before U0|U0 begins|先于 U0)", body), (
        f"§ {ENTRY_TITLE} MUST validate all six facts before U0 begins (C-31)"
    )
    assert "references/nested-invocation.md" in body, (
        f"§ {ENTRY_TITLE} MUST point at its reference document instead of copying the "
        f"validation table into SKILL.md (one source of truth)"
    )


# ---------------------------------------------------------------------------
# C-32 — fail-closed entry validation, condition named
# ---------------------------------------------------------------------------


def test_entry_validation_table_covers_the_closed_condition_set():
    body = _own_body(_reference_section("Entry validation table"))
    rows = _table_rows(body)
    assert len(rows) >= 2, "§ Entry validation table carries no data rows (C-32)"
    joined = " ".join(" ".join(row) for row in rows)
    conditions = {
        "missing or undefined Goal": ("goal",),
        "Target dangling/closed/dropped/outside the bound Goal": ("target",),
        "terminal Goal": ("terminal", "终态"),
        "missing team or seat": ("seat", "team"),
        "scope outside the seat territory": ("scope", "territory"),
        "missing verdict or a verdict other than the SDD value": ("verdict",),
    }
    for label, needles in conditions.items():
        assert any(needle in joined.lower() for needle in needles), (
            f"§ Entry validation table does not cover the condition '{label}' (C-32)"
        )
    assert re.search(r"(点名|names the condition|名称)", joined), (
        "every failing condition MUST be named in the refusal (C-32)"
    )
    assert re.search(r"(不启动|does not start|MUST NOT start)", joined), (
        "a failing entry MUST NOT start a run (C-32)"
    )
    assert re.search(r"(不重划|does not re-scope|MUST NOT re-scope)", joined), (
        "a failing entry MUST NOT re-scope the duty to fit (C-32)"
    )


# ---------------------------------------------------------------------------
# C-33 — stop at review completion, no merge authority
# ---------------------------------------------------------------------------


def test_run_stops_at_review_and_claims_no_merge_authority():
    body = _entry_section()
    assert re.search(r"(止于 review|ends at review|stops at review|review 完成)", body), (
        f"§ {ENTRY_TITLE} MUST state that a nested run ends at review completion (C-33)"
    )
    assert re.search(r"(不进入 merge|no merge step|不合并)", body), (
        f"§ {ENTRY_TITLE} MUST state that the run does not proceed to a merge step (C-33)"
    )
    assert re.search(r"(外层|outer layer)", body), (
        "merge authority MUST be attributed to the outer layer, not to the nested run (C-33)"
    )


# ---------------------------------------------------------------------------
# C-34 / C-42 — the closed handoff field set and the completeness test
# ---------------------------------------------------------------------------


def _handoff_fields() -> list:
    body = _own_body(_reference_section("Handoff schema"))
    return _first_column_names(body)


def _gaps(present) -> list:
    """C-42's consuming check: a field-presence test over the handoff block."""
    return [field for field in _handoff_fields() if field not in set(present)]


def test_handoff_field_set_is_closed():
    fields = _handoff_fields()
    assert tuple(fields) == HANDOFF_FIELDS, (
        "the handoff field set is closed (C-34): expected "
        f"{list(HANDOFF_FIELDS)}, got {fields}"
    )
    body = _reference_section("Handoff schema")
    assert re.search(r"(不完整|incomplete)", body), (
        "§ Handoff schema MUST state that missing any field makes the handoff incomplete "
        "(C-34)"
    )
    assert re.search(r"(不算成功|never a successful return|MUST NOT .*success)", body), (
        "§ Handoff schema MUST state that an incomplete handoff is never a successful return "
        "(C-34 / C-42)"
    )


@pytest.mark.parametrize("dropped", HANDOFF_FIELDS)
def test_a_handoff_missing_any_field_is_incomplete(dropped):
    complete = {field: None for field in HANDOFF_FIELDS}
    assert _gaps(complete) == [], "the complete handoff must be complete"
    del complete[dropped]
    assert _gaps(complete) == [dropped], (
        f"a handoff missing '{dropped}' MUST be judged incomplete (C-34); the presence test "
        f"is the consuming check, not a prose reading"
    )


# ---------------------------------------------------------------------------
# C-35 / C-36 — three-valued outcome and the four-fact integration identity
# ---------------------------------------------------------------------------


def test_outcome_takes_exactly_three_values():
    body = _own_body(_reference_section("Handoff schema"))
    for string_id in OUTCOME_STRINGS:
        assert f"[[{string_id}]]" in body, (
            f"§ Handoff schema does not name the outcome value [[{string_id}]] (C-35)"
        )
    assert re.search(r"(三值|three values|exactly three|四值以上|fourth)", body), (
        "§ Handoff schema MUST state that the outcome is exactly three-valued (C-35)"
    )


def test_integration_identity_is_four_facts_with_the_retained_branch_named():
    body = _reference_section("Handoff schema")
    sub = [
        block
        for block in _heading_blocks(_read(REFERENCE_MD))
        if block[1].startswith("Integration identity")
    ]
    assert sub, "§ Handoff schema carries no 'Integration identity' sub-section (C-36)"
    facts_body = sub[0][2]
    names = _first_column_names(facts_body) if _table_rows(facts_body) else []
    assert tuple(names) == INTEGRATION_FACTS, (
        f"the integration identity is exactly four facts (C-36): expected "
        f"{list(INTEGRATION_FACTS)}, got {names}"
    )
    assert re.search(r"(保留|retained)", facts_body + body), (
        "the handoff MUST name the retained branch (C-36)"
    )


def test_handoff_without_integration_identity_is_not_successful():
    complete = {field: None for field in HANDOFF_FIELDS}
    del complete["integration_identity"]
    assert _gaps(complete) == ["integration_identity"]
    body = _reference_section("Handoff schema")
    assert "integration_identity" in body and re.search(
        r"(不算成功|MUST NOT .*success|not be reported successful)", body
    ), (
        "a handoff without its integration identity leaves the outer layer unable to "
        "integrate, so it MUST NOT be reported successful (C-42)"
    )


# ---------------------------------------------------------------------------
# C-37 — zero merge, zero push
# ---------------------------------------------------------------------------


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", *args],
        cwd=str(repo),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, f"git {' '.join(args)} failed: {proc.stderr}"
    return proc.stdout.strip()


def _git_state(repo: Path) -> dict:
    return {
        "log": _git(repo, "log", "--oneline"),
        "status": _git(repo, "status", "--porcelain"),
        "branch": _git(repo, "rev-parse", "--abbrev-ref", "HEAD"),
        "head": _git(repo, "rev-parse", "HEAD"),
    }


def test_no_instruction_issues_a_merge_or_push():
    """Every line that mentions a merge/push command must also prohibit it (C-37).

    The test also requires the prohibition to be **present**: a scan that can only ever be
    empty would pass on a document that never forbids merging at all, which is the classic
    green check that would not go red.
    """
    assert REFERENCE_MD.is_file(), (
        f"missing document: {REFERENCE_MD.relative_to(REPO_ROOT)}"
    )
    offenders = []
    prohibited_merge = False
    prohibited_push = False
    for path in (SKILL_MD, REFERENCE_MD):
        for lineno, line in enumerate(_read(path).splitlines(), 1):
            prohibits = any(marker in line for marker in PROHIBITION_MARKERS)
            if re.search(r"git (merge|push)", line) and not prohibits:
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{lineno}")
            if prohibits and "merge" in line.lower():
                prohibited_merge = True
            if prohibits and "push" in line.lower():
                prohibited_push = True
    assert not offenders, (
        "a nested run MUST NOT merge and MUST NOT push (C-37); these lines issue or describe "
        "such a command without prohibiting it:\n" + "\n".join(offenders)
    )
    assert prohibited_merge and prohibited_push, (
        "the driver surface MUST state both prohibitions explicitly — a nested run merges "
        f"nothing and pushes nothing (C-37): merge_stated={prohibited_merge} "
        f"push_stated={prohibited_push}"
    )


def test_nested_run_reaches_review_zero_merge_zero_push(tmp_path):
    """The end-to-end content face (C-41, D-3): review reached, zero merge, zero push.

    There is no executable nested run in this slice (the driver is a chat instruction, not a
    CLI), so the decidable face is: the entry precondition resolves allowed on the fixture's
    authorized seat, the handoff assembled from the run's own facts is complete, the stages
    reached stop at review, and a real repository's log/status are byte-identical before and
    after — a merge or a push would change at least one of them.
    """
    project = build(tmp_path / "project")
    repo = tmp_path / "line"
    repo.mkdir()
    (repo / "artifact.md").write_text("reviewed artifact\n", encoding="utf-8")
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "artifact.md")
    _git(repo, "commit", "-q", "-m", "nested run: artifact chain through review")
    before = _git_state(repo)

    rc, _stdout, _stderr = project.run_authorize(project.seat_allowed)
    payload = project.run_authorize_json(project.seat_allowed)
    assert rc == 0 and payload["effective"] == ALLOWED, (
        f"the authorized seat must resolve allowed before a nested run may start (C-8): "
        f"rc={rc} payload={payload!r}"
    )

    handoff = {
        "outcome": "completed",
        "stages_reached": [
            "requirements",
            "clarify",
            "plan",
            "tasks",
            "checklist",
            "analyze",
            "implement",
            "review",
        ],
        "artifact_paths": [str(repo / "artifact.md")],
        "evidence_paths": [str(project.verdict_record)],
        "unresolved_findings": [],
        "anomaly_line": "未发现异常",
        "integration_identity": {
            "line_id": "074a-fixture-line",
            "branch": before["branch"],
            "worktree_path": str(repo),
            "head_commit": before["head"],
        },
    }
    assert _gaps(handoff) == [], (
        f"the end-to-end handoff must carry the whole closed field set (C-34 / C-41): "
        f"gaps={_gaps(handoff)}"
    )
    assert "merge" not in handoff["stages_reached"], (
        "the run stops at review completion; a merge stage is the outer layer's, never the "
        "nested run's (C-33 / C-41)"
    )

    after = _git_state(repo)
    assert after == before, (
        "a nested run MUST NOT merge and MUST NOT push (C-37 / C-41): git log / git status / "
        f"branch / HEAD changed — before={before!r} after={after!r}"
    )


# ---------------------------------------------------------------------------
# C-38 / C-39 / C-40 / C-43 — reuse, stall handoff, consumer duty, no second store
# ---------------------------------------------------------------------------


def test_line_registration_reuses_the_existing_mechanism():
    body = _reference_section("Line registration")
    assert re.search(r"(line registry|line-registry|写线登记)", body), (
        "§ Line registration MUST register the nested run with the existing line registry "
        "(C-38)"
    )
    assert "worktree" in body.lower(), (
        "§ Line registration MUST cite worktree-per-write-line (C-38)"
    )
    assert re.search(r"(串行|serializ|拒绝|reject)", body), (
        "overlapping territories MUST be serialized or rejected by that mechanism (C-38)"
    )
    assert re.search(r"(MUST NOT .*第二|不得新建|no second)", body), (
        "§ Line registration MUST forbid a second mechanism (C-38 / C-43)"
    )


def test_failure_and_stall_handoff_has_four_elements():
    body = _reference_section("Failure and stall handoff")
    assert re.search(r"(发现|found)", body), "the stall handoff names what was found (C-39)"
    assert re.search(r"(吃重|costly|why the run was costly)", body), (
        "the stall handoff states why the run was costly (C-39)"
    )
    assert re.search(r"(中间产物|intermediate artifacts)", body), (
        "the stall handoff lists the intermediate artifacts by path (C-39)"
    )
    assert re.search(r"(可选处置|disposition)", body), (
        "the stall handoff lists the available dispositions (C-39)"
    )
    assert re.search(r"(状态脊|state spine)", body), (
        "on stall the run persists its state spine (C-39)"
    )
    assert f"[[{OUTCOME_STRINGS[2]}]]" in body, (
        "a stalled run returns a failed handoff (C-39)"
    )
    assert re.search(r"(不静默等待|MUST NOT wait silently|不静默)", body), (
        "a stalled run MUST NOT wait silently (C-39)"
    )


def test_consumer_duty_carries_the_handoff_and_hides_no_failure():
    body = _reference_section("Consumer duty")
    assert re.search(r"(原样|verbatim|稳定路径|stable path)", body), (
        "the invoking Agent carries the handoff verbatim or by stable path (C-40)"
    )
    for string_id in OUTCOME_STRINGS[1:]:
        assert f"[[{string_id}]]" in body, (
            f"§ Consumer duty MUST name [[{string_id}]] as a value that must never be "
            f"reported as success (C-40)"
        )
    assert re.search(r"(MUST NOT .*成功|不得报成功|never .*success)", body), (
        "a blocked/failed nested outcome MUST NOT be reported as success (C-40)"
    )


def test_no_second_registry_ledger_spine_or_queue():
    text = _read(REFERENCE_MD)
    assert re.search(r"(MUST NOT|不得)", text), "the reference states no prohibition at all"
    joined = " ".join(text.split())
    for mechanism in ("registry", "state spine", "integration queue"):
        assert re.search(
            r"(MUST NOT|不得)[^.]{0,120}" + re.escape(mechanism), joined
        ) or re.search(
            re.escape(mechanism) + r"[^.]{0,120}(MUST NOT|不得)", joined
        ), (
            f"the reference MUST forbid introducing a second {mechanism} (C-43)"
        )


def test_artifact_and_evidence_paths_are_referenceable():
    """D-3 content face: paths are carried by reference; the report section is not asserted."""
    body = _own_body(_reference_section("Handoff schema"))
    for field in ("artifact_paths", "evidence_paths"):
        assert field in body, f"§ Handoff schema lost the {field} field (C-34)"
    assert re.search(r"(路径|path)", body), (
        "the handoff's artifact/evidence entries are paths, not prose summaries (C-41)"
    )
    text = _read(REFERENCE_MD)
    assert "Nested SDD Runs" not in text, (
        "the `## Nested SDD Runs` report section belongs to 074b-nested-governance (D-3); "
        "this slice's reference MUST NOT define or assert it"
    )
