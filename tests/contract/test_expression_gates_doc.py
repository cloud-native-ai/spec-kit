"""Contract tests for the expression-gate owner document (069a, T013).

Owns the owner-document assertions of
``.specify/specs/069a-flow-classification-docs-gates/contracts/expression-gate-operators.md``
that ``tasks.md`` T013 names:

* C-1  the owner exists, declares its ownership up front, and carries a **closed
       set of exactly six faces** — each with exactly one face id, one Chinese
       name, and exactly one ``owner_pointer`` whose path and ``§`` section
       anchor resolve in this repository;
* C-2  a per-stage operator table covers all eight SDD stages (rows >= 8, no
       empty operator cell);
* C-3  every face owns at least one ``blocking`` operator; requirements clarity /
       fact consistency / review each carry one; a missing reader declaration is
       blocking; the P0/P1 downgrade and "looser channel" negatives are present;
* C-4  the reader declaration is the two-line form inside the first 40 non-empty
       lines, reusing the baseline reader (no second reader definition);
* C-5  the evidence grade is the closed three-value set, ``as-of`` is
       ``YYYY-MM-DD``, ``source`` is mandatory (``source-missing``), the three
       pieces are grouped, and the object boundary against
       ``evidence-step.md`` / ``single-run-evidence.md`` is stated;
* C-6  structure / links / build are necessary-but-not-sufficient, the judge is
       "zero **new** violations", and an absent site layer is ``not-applicable``;
* C-7  one owner per fact, >= 2 hand-written copies is a defect, the fix
       direction is "reference the owner", derived counts come from artifacts,
       and the mechanical detection floor is acknowledged;
* C-8  review keeps the declared reader baseline (not compile/test/coverage) and
       is present at both ``analyze`` and ``review``;
* C-9  the three baselines name their existing source commands, the freeze point
       is the first ``requirements`` commit, and "no source" is ``null`` + reason;
* C-11 stage completeness never reads the class, analyze/review stay at 100%,
       and skip/shorten/re-classify requests are rejected without exception;
* C-13 the document is orthogonal to the complexity axis and only points at
       ``shared/workflow/feedback-step.md``;
* C-14 the call-site table registers W1…W4, the docs row runs the checker, the
       ``/speckit.humanize`` row declares "no class read", the ``skill:humanize``
       row is the flow's only ``--action lookup`` and is never the six-face set.

Red-first discipline (Constitution IV): the owner document does not exist yet.
``_read_owner`` asserts the path first, so a red is "artifact missing", never an
import or collection error.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER = REPO_ROOT / "shared" / "workflow" / "expression-gates.md"
OWNER_REL = "shared/workflow/expression-gates.md"
CLASS_LEDGER = REPO_ROOT / "shared" / "definitions" / "flow-class-definitions.md"

# requirements.md § Shared Strings (pinned copies).
STR_003 = "flow_class"

# The closed six-face set (contract C-1). Order is the contract's table order.
FACE_NAMES = (
    "需求清晰度",
    "读者/目的/边界",
    "证据分级与 as-of",
    "结构/链接/构建",
    "事实一致性",
    "评审",
)
FACE_IDS = (
    "requirements-clarity",
    "reader-purpose",
    "evidence-asof",
    "structure-links-build",
    "fact-consistency",
    "review",
)
FACES_WITH_MANDATORY_BLOCKING = (
    "requirements-clarity",
    "fact-consistency",
    "review",
)
STAGES = (
    "requirements",
    "clarify",
    "plan",
    "tasks",
    "checklist",
    "analyze",
    "implement",
    "review",
)
BLOCKING_LEVELS = ("blocking", "advisory")

PATH_TOKEN_RE = re.compile(
    r"(?:shared|scripts|skills|templates|tests|docs)/[A-Za-z0-9._/-]+"
)
# An affirmative "expression class may skip/shorten/re-classify" phrasing.
SKIP_PERMISSION_RE = re.compile(
    r"(?:表达类|expression)[^。\n]{0,24}"
    r"(?:可以|允许|无需|可不|可)[^。\n]{0,12}"
    r"(?:跳过|省略|缩短|改判)"
)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _read_owner() -> str:
    assert OWNER.is_file(), (
        "expression-gate owner missing: %s — expected at T016/T017/T018/T019 "
        "(069a). Red is the intended pre-implementation state for T013." % OWNER_REL
    )
    return OWNER.read_text(encoding="utf-8")


def _cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _is_separator(line: str) -> bool:
    cells = _cells(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def _tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    """Return ``(header, rows)`` for every Markdown table in *text*."""
    tables: list[tuple[list[str], list[list[str]]]] = []
    block: list[str] = []
    for line in text.splitlines() + [""]:
        if line.lstrip().startswith("|"):
            block.append(line)
            continue
        if len(block) >= 2:
            header = _cells(block[0])
            rows = [
                _cells(row)
                for row in block[1:]
                if not _is_separator(row)
            ]
            tables.append((header, rows))
        block = []
    return tables


def _table(text: str, *header_needles: str) -> tuple[list[str], list[list[str]]]:
    for header, rows in _tables(text):
        joined = " ".join(header)
        if all(needle in joined for needle in header_needles):
            return header, rows
    raise AssertionError(
        "owner lacks a table whose header contains all of %r; headers seen: %r"
        % (header_needles, [h for h, _ in _tables(text)])
    )


def _column(header: list[str], needle: str) -> int:
    for index, cell in enumerate(header):
        if needle in cell:
            return index
    raise AssertionError("table header %r has no column containing %r" % (header, needle))


def _paths(text: str) -> list[str]:
    found = []
    for raw in PATH_TOKEN_RE.findall(text):
        token = raw.rstrip(".,;:，。；：)）】]")
        if token and token not in found:
            found.append(token)
    return found


def _section_span(text: str, heading: str) -> tuple[int, int]:
    """Return (start, end) line indexes of a ``## heading`` section."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index
            continue
        if start is not None and line.startswith("## "):
            return start, index
    assert start is not None, "owner lacks the section %r" % heading
    return start, len(lines)


def _section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start, end = _section_span(text, heading)
    return "\n".join(lines[start:end])


def _pointer_problems(cell: str) -> list[str]:
    problems: list[str] = []
    paths = _paths(cell)
    if not paths:
        problems.append("owner_pointer carries no repo-relative path: %r" % cell)
    for rel in paths:
        if not (REPO_ROOT / rel).exists():
            problems.append("owner_pointer path does not exist: %s" % rel)
    if "§" in cell:
        anchor = cell.split("§", 1)[1]
        anchor = re.split(r"[（(；;+，,]", anchor, maxsplit=1)[0].strip()
        if not anchor:
            problems.append("owner_pointer carries an empty section anchor: %r" % cell)
        else:
            resolved = False
            for rel in paths:
                target = REPO_ROOT / rel
                if not target.is_file():
                    continue
                for line in target.read_text(encoding="utf-8").splitlines():
                    if line.lstrip().startswith("#") and anchor in line:
                        resolved = True
                        break
                if resolved:
                    break
            if not resolved:
                problems.append(
                    "section anchor %r is not a heading under any pointer path %r"
                    % (anchor, paths)
                )
    return problems


# --------------------------------------------------------------------------- #
# C-1 — closed six-face set, one id and one resolvable pointer per face
# --------------------------------------------------------------------------- #
def test_c01_owner_declares_scope_and_closed_face_count():
    text = _read_owner()
    head = "\n".join(text.splitlines()[:20])
    assert "expression-gates.md" in head, "owner must name itself in its opening lines"
    assert "Owner" in head or "所有者" in head, (
        "owner must declare its ownership in the opening lines"
    )
    assert "面数 = 6" in text, "owner must state the closed face count verbatim (面数 = 6)"
    assert re.search(r"新增面[^。\n]{0,20}(?:后续特性|后续)[^。\n]{0,10}修订", text), (
        "owner must state that adding a face requires a later feature revising this owner"
    )
    assert "MUST NOT 复述" in text or "不复述" in text, (
        "owner must declare that it does not restate the pointed-to owners' criteria"
    )


def test_c01_face_table_has_exactly_six_faces():
    text = _read_owner()
    header, rows = _table(text, "face id", "owner_pointer")
    assert len(header) == 3, "face table must have exactly three columns: 面 | face id | owner_pointer"
    data = [row for row in rows if row and row[0]]
    assert len(data) == 6, (
        "face table must list exactly 6 faces (closed set), found %d rows" % len(data)
    )
    ids = [row[_column(header, "face id")] for row in data]
    names = [row[0] for row in data]
    assert len(set(ids)) == 6, "face ids must be unique (one id per face), got %r" % ids
    assert set(ids) == set(FACE_IDS), (
        "face ids must be exactly the closed set %r, got %r" % (list(FACE_IDS), ids)
    )
    for name, face_id in zip(names, ids):
        matched = [known for known in FACE_NAMES if name.startswith(known)]
        assert matched, "unknown Chinese face name %r (expected one of %r)" % (name, FACE_NAMES)
        expected_id = FACE_IDS[FACE_NAMES.index(matched[0])]
        assert face_id == expected_id, (
            "face %r must map to face id %r, got %r" % (matched[0], expected_id, face_id)
        )
    assert {known for known in FACE_NAMES} == {
        next(k for k in FACE_NAMES if name.startswith(k)) for name in names
    }, "each of the six Chinese face names must appear exactly once"


def test_c01_every_face_declares_exactly_one_resolvable_owner_pointer():
    text = _read_owner()
    header, rows = _table(text, "face id", "owner_pointer")
    index = _column(header, "owner_pointer")
    problems: list[str] = []
    for row in rows:
        if not row or not row[0]:
            continue
        pointer = row[index] if index < len(row) else ""
        if not pointer:
            problems.append("face %r has an empty owner_pointer cell" % row[0])
            continue
        problems.extend("%s: %s" % (row[0], item) for item in _pointer_problems(pointer))
    assert not problems, "unresolvable owner pointers:\n- " + "\n- ".join(problems)


# --------------------------------------------------------------------------- #
# C-2 — per-stage operator table
# --------------------------------------------------------------------------- #
def test_c02_stage_operator_table_covers_all_eight_stages():
    text = _read_owner()
    header, rows = _table(text, "阶段", "执行算子", "对应面", "阻断级别")
    stage_col = _column(header, "阶段")
    operator_col = _column(header, "执行算子")
    face_col = _column(header, "对应面")
    blocking_col = _column(header, "阻断级别")
    data = [row for row in rows if row and row[0]]
    assert len(data) >= 8, (
        "stage operator table must have at least 8 data rows (one per stage), got %d" % len(data)
    )
    seen_stages = set()
    problems: list[str] = []
    for row in data:
        if len(row) != len(header):
            problems.append("row has %d cells, header has %d: %r" % (len(row), len(header), row))
            continue
        stage = row[stage_col].strip("` ")
        seen_stages.add(stage)
        if not row[operator_col].strip("` "):
            problems.append("stage %r has an empty operator cell" % stage)
        face = row[face_col].strip("` ")
        if face not in FACE_IDS:
            problems.append("stage %r names %r, which is not a face id" % (stage, face))
        level = row[blocking_col].strip("` ")
        if level not in BLOCKING_LEVELS:
            problems.append("stage %r has blocking level %r" % (stage, level))
    assert not problems, "stage operator table defects:\n- " + "\n- ".join(problems)
    assert set(STAGES) <= seen_stages, (
        "the operator table must cover all 8 stages; missing %r" % (set(STAGES) - seen_stages)
    )


# --------------------------------------------------------------------------- #
# C-3 — blocking floor per face, no downgrade
# --------------------------------------------------------------------------- #
def test_c03_blocking_floor_holds_for_every_face():
    text = _read_owner()
    header, rows = _table(text, "阶段", "执行算子", "对应面", "阻断级别")
    face_col = _column(header, "对应面")
    blocking_col = _column(header, "阻断级别")
    blocking_faces = set()
    for row in rows:
        if len(row) != len(header):
            continue
        if row[blocking_col].strip("` ") == "blocking":
            blocking_faces.add(row[face_col].strip("` "))
    for face in FACE_IDS:
        assert face in blocking_faces, "face %r has no blocking operator in the stage table" % face
    for face in FACES_WITH_MANDATORY_BLOCKING:
        assert face in blocking_faces, "face %r MUST carry at least one blocking operator" % face

    reader_lines = [line for line in text.splitlines() if "reader-declaration-missing" in line]
    assert reader_lines, "owner must name the reader-declaration-missing finding"
    assert any("阻断" in line for line in reader_lines), (
        "a missing reader declaration must be declared 阻断 (blocking), not a warning"
    )
    assert re.search(r"不得[^。\n]{0,20}(?:P0/P1|P0|P1)[^。\n]{0,20}(?:降为|降级)[^。\n]{0,10}advisory", text), (
        "owner must forbid downgrading existing P0/P1 judgements to advisory"
    )
    assert re.search(r"不得[^。\n]{0,24}表达类[^。\n]{0,16}更宽松", text), (
        "owner must refuse to read the expression class as a looser channel"
    )


# --------------------------------------------------------------------------- #
# C-4 — reader declaration
# --------------------------------------------------------------------------- #
def test_c04_reader_declaration_is_two_lines_in_first_40():
    text = _read_owner()
    assert "**Readers**:" in text, "owner must pin the `**Readers**:` line form"
    assert "**Reading scenario**:" in text, "owner must pin the `**Reading scenario**:` line form"
    assert re.search(r"前\s*40\s*个非空行", text), (
        "owner must scope the declaration to the first 40 non-empty lines"
    )
    assert "reader-declaration-missing" in text, "owner must name the missing-declaration finding"
    assert "基准读者" in text, "owner must reuse the baseline reader instead of inventing a second"
    assert "user-facing-comprehension.md" in text, (
        "owner must point at the baseline reader's owner"
    )
    assert re.search(r"MUST NOT[^。\n]{0,20}第二套", text) or "不新建第二套" in text, (
        "owner must forbid a second reader definition"
    )


# --------------------------------------------------------------------------- #
# C-5 — evidence grades, as-of, source
# --------------------------------------------------------------------------- #
def test_c05_evidence_grade_asof_and_source_syntax():
    text = _read_owner()
    for grade in ("实测", "推断", "引用"):
        assert grade in text, "evidence grade %r missing from the closed three-value set" % grade
    assert "YYYY-MM-DD" in text, "owner must pin the as-of form YYYY-MM-DD"
    assert re.search(r"封闭三值|三值封闭", text), "owner must state the grade set is closed"
    assert "source" in text and re.search(r"来源[^。\n]{0,10}必填|MUST[^。\n]{0,10}source", text), (
        "owner must make `source` mandatory"
    )
    assert "source-missing" in text, "owner must name the source-missing blocking rule"
    assert re.search(r"三件套", text), (
        "owner must state the grade / as-of / source three-piece grouping rule"
    )
    assert "evidence-step.md" in text, (
        "owner must carry the object boundary against the seven-state evidence step"
    )
    assert "single-run-evidence.md" in text, (
        "owner must carry the object boundary against single-run evidence"
    )


# --------------------------------------------------------------------------- #
# C-6 — structure / links / build are necessary, not sufficient
# --------------------------------------------------------------------------- #
def test_c06_structure_links_build_is_necessary_not_sufficient():
    text = _read_owner()
    assert re.search(r"零\s*\*\*新增\*\*|零新增", text), (
        "structure face must be judged as zero **new** violations"
    )
    assert "not-applicable" in text, "an absent site layer must be recorded not-applicable"
    assert re.search(r"必要条件", text), (
        "owner must state that structure/links/build are necessary but not sufficient"
    )
    assert re.search(r"MUST NOT[^。\n]{0,30}(?:援引|当作|作为)[^。\n]{0,20}(?:正确性|内容)", text) or (
        re.search(r"不得[^。\n]{0,30}(?:援引|当作|作为)[^。\n]{0,20}(?:正确性|内容)", text)
    ), "owner must forbid citing a green build as proof of content correctness"
    assert "broken-link" in text and "note-frontmatter" in text, (
        "owner must carry the measured structure baseline kinds (broken-link / note-frontmatter)"
    )
    assert re.search(r"violations\s*=\s*3", text), (
        "owner must carry the measured structure baseline (violations = 3)"
    )


# --------------------------------------------------------------------------- #
# C-7 — fact uniqueness and the fix direction
# --------------------------------------------------------------------------- #
def test_c07_fact_uniqueness_fix_direction():
    text = _read_owner()
    assert "one-source-of-truth.md" in text, "fact consistency must point at its single owner"
    assert re.search(r"≥\s*2\s*处|>\s*=\s*2\s*处|两处|2 处", text), (
        "owner must state that two or more hand-written copies are a defect"
    )
    assert re.search(r"修复方向[^。\n]{0,40}引用|改为[^。\n]{0,20}引用", text), (
        "the fix direction must be 'turn it into a reference to the owner'"
    )
    assert re.search(r"MUST NOT[^。\n]{0,30}(?:改措辞|措辞改到一致)|不是[^。\n]{0,20}改措辞", text), (
        "owner must forbid 'rewording until the copies agree' as a fix"
    )
    assert "pre-analyze-check.py" in text, (
        "hand-written counts must be reported by the existing count judge, not a second rule"
    )
    assert "24" in text and "0.90" in text and "40" in text, (
        "owner must acknowledge the mechanical detection floor (24 chars / 0.90 ratio / 40 chars)"
    )


# --------------------------------------------------------------------------- #
# C-8 — review keeps the reader baseline and sits at analyze + review
# --------------------------------------------------------------------------- #
def test_c08_review_judges_reader_baseline_in_analyze_and_review():
    text = _read_owner()
    header, rows = _table(text, "阶段", "执行算子", "对应面", "阻断级别")
    stage_col = _column(header, "阶段")
    face_col = _column(header, "对应面")
    review_stages = {
        row[stage_col].strip("` ")
        for row in rows
        if len(row) == len(header) and row[face_col].strip("` ") == "review"
    }
    assert {"analyze", "review"} <= review_stages, (
        "the review face must be present at both analyze and review, got %r" % review_stages
    )
    assert "review-sdd-process" in text, "review face must point at its owning skill"
    assert "review-template.md" in text, "review face must point at the report template"
    assert re.search(r"读者[^。\n]{0,10}基准", text), (
        "review must judge against the declared reader baseline"
    )
    assert re.search(r"MUST NOT[^。\n]{0,40}(?:编译|测试|覆盖率)", text) or (
        re.search(r"不得[^。\n]{0,40}(?:编译|测试|覆盖率)", text)
    ), "review must not reuse the code-review object (compile / test / coverage)"
    assert re.search(r"MUST NOT[^。\n]{0,20}分类[^。\n]{0,10}免除", text) or (
        "不得由分类免除" in text
    ), "the class must never exempt an artifact from review"


# --------------------------------------------------------------------------- #
# C-9 — the three baselines
# --------------------------------------------------------------------------- #
def test_c09_three_baselines_have_sources_and_null_rule():
    text = _read_owner()
    header, rows = _table(text, "量", "既有通道")
    joined = "\n".join(" ".join(row) for row in rows)
    assert len(rows) >= 3, "the baseline table must register the three quantities"
    assert "门禁调用次数" in joined, "baseline quantity 'gate calls' missing"
    assert "人工确认次数" in joined, "baseline quantity 'human confirmations' missing"
    assert "墙钟" in joined, "baseline quantity 'requirements→analyze wall clock' missing"
    assert "exec-quant.py" in joined, "gate-call baseline must name its existing source command"
    assert "feedback-utils.py" in joined, "confirmation baseline must name its existing source"
    assert "git log -1 --format=%cs" in joined, (
        "wall-clock baseline must derive from the requirements first-commit date"
    )
    assert re.search(r"首个提交|首次提交", text), (
        "owner must pin the freeze point as the first requirements commit"
    )
    assert re.search(r"null", text) and re.search(r"reason", text), (
        "a quantity without a source must be null + reason (never 0, never met)"
    )
    assert re.search(r"≤\s*3", text), "owner must cap confirmations per stage at <= 3"


# --------------------------------------------------------------------------- #
# C-11 — stage integrity never reads the class
# --------------------------------------------------------------------------- #
def test_c11_stage_integrity_never_reads_class():
    text = _read_owner()
    assert re.search(r"阶段完整性", text), "owner must name the stage-integrity invariant"
    assert re.search(r"类别\s*MUST NOT\s*参与|MUST NOT\s*参与[^。\n]{0,10}类别", text), (
        "owner must state the class never participates in the stage-integrity judgement"
    )
    assert re.search(r"100\s*%", text), "owner must pin the 100% analyze/review call rate"
    assert re.search(r"跳过|缩短|改判", text), "owner must name the forbidden class-based shortcuts"
    assert re.search(r"拒绝", text), "owner must state those requests are rejected"
    assert re.search(r"无例外|MUST NOT[^。\n]{0,10}例外", text), (
        "the rejection rule must carry no exception"
    )


# --------------------------------------------------------------------------- #
# C-12 / C-13 — additive first batch; orthogonal to the complexity axis
# --------------------------------------------------------------------------- #
def test_c12_negative_clause_keeps_first_batch_additive():
    text = _read_owner()
    assert re.search(r"只补强|不削弱", text), (
        "the first-batch members must be additive only (never weaken existing gates)"
    )
    assert "feedback-step.md" in text, "the complexity axis must be reached by pointer"
    assert re.search(r"正交", text), "owner must state orthogonality with the complexity axis"
    assert "feedback-step.md" in text and re.search(r"MUST NOT[^。\n]{0,20}复制", text), (
        "owner must forbid copying the complexity axis' criteria into itself"
    )


def test_c13_owner_points_at_the_complexity_axis_instead_of_restating_it():
    text = _read_owner()
    axis = [line for line in text.splitlines() if "feedback-step.md" in line]
    assert axis, "owner must point at shared/workflow/feedback-step.md for the complexity axis"
    assert all("MUST NOT" in line or "只" in line or "指针" in line for line in axis), (
        "every complexity-axis mention must be a pointer, not a restatement: %r" % axis
    )


# --------------------------------------------------------------------------- #
# C-14 — call-site registry
# --------------------------------------------------------------------------- #
def _call_site_table() -> tuple[list[str], list[list[str]]]:
    return _table(_read_owner(), "调用点", "类别读取", "执行算子", "阻断")


def test_c14_call_site_table_covers_w1_to_w4():
    header, rows = _call_site_table()
    data = [row for row in rows if row and row[0]]
    assert len(data) == 4, (
        "the call-site table must register exactly four entries (W1…W4), got %d" % len(data)
    )
    entries = [row[0] for row in data]
    for needle in ("/speckit.docs", "skill:create-docs", "/speckit.humanize", "skill:humanize"):
        assert any(needle in entry for entry in entries), (
            "call-site table lacks the %r entry; entries: %r" % (needle, entries)
        )
    docs_row = next(row for row in data if "/speckit.docs" in row[0] and "humanize" not in row[0])
    assert "doc-consistency-check.py --action verify" in " ".join(docs_row), (
        "the /speckit.docs row must run `doc-consistency-check.py --action verify`"
    )
    docs_join = " ".join(docs_row)
    for face in FACE_IDS:
        assert face in docs_join or face.replace("-", " ") in docs_join.lower() or (
            (face == "requirements-clarity" and "需求清晰度" in docs_join)
            or (face == "reader-purpose" and "读者" in docs_join)
            or (face == "evidence-asof" and "证据" in docs_join)
            or (face == "structure-links-build" and "结构" in docs_join)
            or (face == "fact-consistency" and "事实" in docs_join)
            or (face == "review" and "评审" in docs_join)
        ), "the /speckit.docs row must cover all six faces; face %r missing" % face


def test_c14_humanize_rows_are_a_separate_row_set():
    header, rows = _call_site_table()
    data = [row for row in rows if row and row[0]]
    w2 = next(row for row in data if "/speckit.humanize" in row[0])
    w4 = next(row for row in data if "skill:humanize" in row[0])
    w2_join = " ".join(w2)
    assert "不读取" in w2_join, "the /speckit.humanize row must declare that it never reads the class"
    for forbidden in ("flow-class-check.py", "--action lookup", "--unit-id",
                      "doc-consistency-check.py"):
        assert forbidden not in w2_join, (
            "the /speckit.humanize row must not carry %r (Simple form, no script call)" % forbidden
        )
    humanize_rows = "\n".join(" ".join(row) for row in (w2, w4))
    assert humanize_rows.count("--action lookup") == 1, (
        "only the skill:humanize row may carry the flow's single --action lookup"
    )
    w4_join = " ".join(w4)
    assert "flow-class-check.py --action lookup" in w4_join, (
        "the skill:humanize row must carry the flow's lookup call"
    )
    assert "/speckit.humanize" in w4_join, (
        "the skill:humanize row must name the unit id it looks up"
    )
    assert "structure-links-build" not in w4_join, (
        "the humanize operator row must not absorb the structure face"
    )
    assert "requirements-clarity" not in w4_join and "需求清晰度" not in w4_join, (
        "the humanize operator row must not absorb the requirements-clarity face"
    )
    assert "062-" in w4_join, "the skill:humanize row must register the 062-* minimal operator set"
    text = _read_owner()
    for line in text.splitlines():
        if "humanize" not in line:
            continue
        assert not re.search(r"(?:是|属于)[^。\n]{0,10}(?:六面|门禁集)[^。\n]{0,10}(?:子集|精简版)", line), (
            "the humanize row must never be described as a subset / trimmed six-face set: %r" % line
        )


# --------------------------------------------------------------------------- #
# Cross-cutting negatives
# --------------------------------------------------------------------------- #
def test_no_expression_class_skip_or_shorten_permission():
    targets = [("expression-gates.md", _read_owner())]
    if CLASS_LEDGER.is_file():
        targets.append(("flow-class-definitions.md", CLASS_LEDGER.read_text(encoding="utf-8")))
    for name, text in targets:
        for line in text.splitlines():
            assert not SKIP_PERMISSION_RE.search(line), (
                "%s permits a class-based stage shortcut: %r" % (name, line)
            )


def test_call_site_table_is_the_only_operator_registry():
    text = _read_owner()
    for line in text.splitlines():
        if "调用点表" in line and "唯一" not in line and "MUST NOT" not in line:
            continue
    assert re.search(r"调用点表", text), "owner must name the call-site table"
    assert re.search(r"MUST NOT\s*复制|不得复制|不复述", text), (
        "owner must forbid templates / skills from copying the operator registry"
    )
