"""Contract tests for the isomorphism map and its four boundaries (069b, T005).

Owns the assertions of
``.specify/specs/069b-isomorphism-migration-metrics/contracts/isomorphism-map.md``
that ``tasks.md`` T005 names:

* C-1  the single carrier is ``shared/definitions/flow-class-definitions.md``: it
  declares ownership of both the map and the boundaries up front, no second map
  table exists anywhere in the repository, no second document claims to own the
  map, and the rejected alternative ``shared/definitions/isomorphism-map.md``
  stays absent;
* C-2  the map header is the six declared columns verbatim, exactly eight data
  rows with no blank row, and the stage set equals the roster owner's
  ``STAGE_ARTIFACTS`` keys (parsed here independently of the engine);
* C-3  each of the 24 face cells is ``代码型：… ↔ 文档型：…`` — exactly one ``↔``,
  both sides prefixed and >= 8 characters, and the three-face legend appears once
  in prose before the table;
* C-4…C-7 the enforcement annotation is a closed two-value set and **true**:
  every ``已强制`` (stage, face) pair has a ``blocking`` operator row at that same
  stage, a ``已声明未强制`` stage has no ``blocking`` row, and a row with neither a
  parseable face nor the annotation is a defect. Both false sides and the slogan
  form are injected into a temporary copy and must each turn red;
* C-8/C-9 the boundary table has the declared header, ``a``–``d`` exactly once, a
  non-empty reason, and a gate handling that names at least one closed face id
  *and* says how that face handles the boundary; missing rows, unbound rows and
  malformed rows are injected and must each turn red;
* C-10 the mechanical floors: every map cell names both sides, and no template or
  skill carries a "文档即代码" licence sentence without an owner pointer;
* C-11 the gate owner's operator column carries none of the code-type operators;
* C-12 neither table uses a medium-axis phrase as the classification reason.

Injection fixtures live in ``tmp_path``: the real owner, gate and roster files are
copied, mutated there, and never written back (quickstart route b). Red-first
(Constitution IV): the owner has no map/boundary sections and the engine has no
``isomorphism`` action yet, so the real-tree assertions fail as "artifact
missing" — never as an import or collection error.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER = REPO_ROOT / "shared" / "definitions" / "flow-class-definitions.md"
GATES = REPO_ROOT / "shared" / "workflow" / "expression-gates.md"
ROSTER = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "loop-state.py"
ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"
REJECTED_ALTERNATIVE = REPO_ROOT / "shared" / "definitions" / "isomorphism-map.md"
MIRROR_OWNER = REPO_ROOT / ".specify" / "shared" / "definitions" / "flow-class-definitions.md"

OWNER_REL = Path("shared") / "definitions" / "flow-class-definitions.md"
GATES_REL = Path("shared") / "workflow" / "expression-gates.md"
ROSTER_REL = Path("skills") / "external" / "sdd-loop-driver" / "scripts" / "loop-state.py"
COMMANDS_REL = Path("templates") / "commands"

# Contract C-2 / C-8: pinned copies of the exact header cells.
MAP_HEADER = (
    "阶段",
    "结构（实体 / 关系 / 边界）",
    "流程（阶段与门禁角色）",
    "逻辑（证据 / 契约 / 验收 / 版本 / 所有权）",
    "强制门禁",
    "强制门禁引用",
    "强制状态",
)
FACE_COLUMNS = MAP_HEADER[1:4]
BOUNDARY_HEADER = ("边界", "不可互换的判定面", "为什么不能互换", "门禁处理")

# Contract C-4 / C-5: the closed two-value set and the reference prefix. An
# enforced row must cite concrete gate-operator ids; the citation is what the
# checker can falsify (free-text semantics stay with the review face).
ENFORCED = "已强制"
DECLARED_UNENFORCED = "已声明未强制"
STATUS_VALUES = (ENFORCED, DECLARED_UNENFORCED)
GATE_REF_PREFIX = "gate:"
GATE_ID_COLUMN = "算子 id"

# Contract C-11 / C-12: the closed phrase sets.
CODE_OPERATORS = ("pytest", "--cov", "coverage", "go test", "mvn test", "npm test", "jest")
MEDIUM_PHRASES = ("按扩展名", "by extension", ".md 即", ".yaml 即")

HEADING_RE = re.compile(r"^(#{1,6})\s")
SEPARATOR_CELL_RE = re.compile(r":?-{2,}:?")
FACE_ID_RE = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)+")
ROSTER_KEY_RE = re.compile(r'^ {4}"([a-z][a-z0-9_-]*)"\s*:\s*\{')
LICENCE_RE = re.compile(r"文档即代码|docs?\s+(?:is|are)\s+code", re.IGNORECASE)

# Scan exclusions: generated payload mirrors and an installed wheel are not a
# second authored carrier (``one-source-of-truth`` allows machine-regenerated
# copies). ``docs/public`` is Hugo build output.
SCAN_SKIP_TOP = {".git", ".venv", "node_modules", "public"}
SCAN_SKIP_PATHS = {
    MIRROR_OWNER,
    REPO_ROOT / ".specify" / "skills",
    REPO_ROOT / ".specify" / "templates",
    REPO_ROOT / ".specify" / "agents" / "templates",
}


# --------------------------------------------------------------------------- #
# generic Markdown helpers (independent of the engine)
# --------------------------------------------------------------------------- #
def _read(path: Path, label: str) -> str:
    assert path.is_file(), (
        "%s missing: %s — red is the intended pre-T006/T007/T008 state."
        % (label, path.relative_to(REPO_ROOT))
    )
    return path.read_text(encoding="utf-8")


def _cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _is_separator(row: list[str]) -> bool:
    return bool(row) and all(SEPARATOR_CELL_RE.fullmatch(cell) for cell in row)


def _section_body(lines: list[str], keyword: str):
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match or keyword not in line:
            continue
        level = len(match.group(1))
        body: list[str] = []
        for follow in lines[index + 1:]:
            follow_match = HEADING_RE.match(follow)
            if follow_match and len(follow_match.group(1)) <= level:
                break
            body.append(follow)
        return body
    return None


def _first_table(lines: list[str]):
    for index, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        if index + 1 >= len(lines) or not lines[index + 1].lstrip().startswith("|"):
            continue
        header = _cells(line)
        if not _is_separator(_cells(lines[index + 1])):
            continue
        rows: list[tuple[int, list[str]]] = []
        cursor = index + 2
        while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
            row = _cells(lines[cursor])
            if not _is_separator(row):
                rows.append((cursor + 1, row))
            cursor += 1
        return header, rows
    return None


def _tables(lines: list[str]):
    """Every Markdown table in ``lines`` (header + data rows)."""
    found = []
    index = 0
    while index < len(lines) - 1:
        line = lines[index]
        if (
            line.lstrip().startswith("|")
            and lines[index + 1].lstrip().startswith("|")
            and _is_separator(_cells(lines[index + 1]))
        ):
            header = _cells(line)
            rows = []
            cursor = index + 2
            while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
                row = _cells(lines[cursor])
                if not _is_separator(row):
                    rows.append(row)
                cursor += 1
            found.append((header, rows))
            index = cursor
            continue
        index += 1
    return found


# --------------------------------------------------------------------------- #
# independent readers for the three owners
# --------------------------------------------------------------------------- #
def _roster_stages() -> list[str]:
    text = _read(ROSTER, "stage roster owner")
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not re.match(r"^STAGE_ARTIFACTS\s*=\s*\{", line):
            continue
        stages = []
        for follow in lines[index + 1:]:
            if follow and not follow.startswith(" "):
                break
            match = ROSTER_KEY_RE.match(follow)
            if match:
                stages.append(match.group(1))
        return stages
    return []


def _gate_owner():
    """Return ``(face_ids, operator_rows)``.

    Operator rows are ``(gate_id, stage, face, level, op)``; the gate id is the
    stable citation key the map's ``强制门禁引用`` column must resolve against.
    """
    text = _read(GATES, "gate owner")
    lines = text.splitlines()
    face_body = _section_body(lines, "六面（封闭集）")
    assert face_body is not None, "gate owner has no § 六面（封闭集） section"
    face_table = _first_table(face_body)
    assert face_table is not None, "gate owner § 六面 has no table"
    header, rows = face_table
    assert "face id" in header, "six-face table has no 'face id' column: %r" % (header,)
    face_index = header.index("face id")
    faces = [row[face_index].strip("` ") for _line, row in rows]

    operator_body = _section_body(lines, "阶段算子表")
    assert operator_body is not None, "gate owner has no § 阶段算子表 section"
    operator_table = _first_table(operator_body)
    assert operator_table is not None, "gate owner § 阶段算子表 has no table"
    op_header, op_rows = operator_table
    required = ("阶段", GATE_ID_COLUMN, "执行算子", "对应面", "阻断级别")
    assert all(column in op_header for column in required), (
        "operator table header changed: %r" % (op_header,)
    )
    rows_out = []
    for _line, row in op_rows:
        record = {column: row[op_header.index(column)] for column in required if column in op_header}
        rows_out.append(
            (
                record.get(GATE_ID_COLUMN, "").strip("` "),
                record.get("阶段", "").strip("` "),
                record.get("对应面", "").strip("` "),
                record.get("阻断级别", "").strip("` "),
                record.get("执行算子", ""),
            )
        )
    return faces, rows_out


def _map_rows():
    """Return ``(header, [(line_no, cells), ...])`` for the owner's map table."""
    text = _read(OWNER, "classification owner")
    body = _section_body(text.splitlines(), "同构映射")
    assert body is not None, (
        "owner has no § 同构映射 section — expected `## 同构映射（8 阶段 × 3 面）`"
    )
    table = _first_table(body)
    assert table is not None, "owner § 同构映射 has no parseable table"
    return table


def _boundary_rows():
    text = _read(OWNER, "classification owner")
    body = _section_body(text.splitlines(), "不可同构边界")
    assert body is not None, "owner has no § 不可同构边界 section"
    table = _first_table(body)
    assert table is not None, "owner § 不可同构边界 has no parseable table"
    return table


def _face_ids_in(text: str, faces) -> list[str]:
    found = []
    for face in sorted(faces, key=len, reverse=True):
        if re.search(r"(?<![a-z0-9-])%s(?![a-z0-9-])" % re.escape(face), text):
            found.append(face)
    return found


def _cell_grammar_problem(cell: str):
    """Return None when the cell satisfies C-3, else a prose reason."""
    if cell.count("↔") != 1:
        return "expected exactly one '↔', found %d" % cell.count("↔")
    left, right = [part.strip() for part in cell.split("↔")]
    if not left.startswith("代码型："):
        return "left side does not start with '代码型：'"
    if not right.startswith("文档型："):
        return "right side does not start with '文档型：'"
    if len(left) < 8 or len(right) < 8:
        return "a side is shorter than 8 characters (left=%d, right=%d)" % (len(left), len(right))
    return None


# --------------------------------------------------------------------------- #
# engine invocation (real tree)
# --------------------------------------------------------------------------- #
def _engine(repo: Path):
    assert ENGINE.is_file(), "flow-class engine missing: %s" % ENGINE.relative_to(REPO_ROOT)
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "isomorphism", "--repo", str(repo), "--format", "json"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    try:
        record = json.loads(proc.stdout) if proc.stdout.strip() else None
    except json.JSONDecodeError:
        record = None
    return proc, record


# --------------------------------------------------------------------------- #
# C-1 carrier and declaration
# --------------------------------------------------------------------------- #
def test_owner_declares_the_map_and_the_boundaries():
    text = _read(OWNER, "classification owner")
    opening = "\n".join(text.splitlines()[:8])
    assert "Owner" in opening or "所有者" in opening, (
        "the owner document must declare ownership in its opening lines"
    )
    assert "同构映射" in opening, "the owns list must name the isomorphism map: %r" % opening
    assert "不可同构边界" in opening, "the owns list must name the boundaries: %r" % opening


def test_rejected_alternative_path_stays_absent():
    assert not REJECTED_ALTERNATIVE.exists(), (
        "shared/definitions/isomorphism-map.md is the rejected alternative and MUST stay absent"
    )


def _md_files():
    for path in REPO_ROOT.rglob("*.md"):
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            continue
        if not rel.parts:
            continue
        if rel.parts[0] in SCAN_SKIP_TOP:
            continue
        if "public" in rel.parts:
            continue
        if any(path == skip or skip in path.parents for skip in SCAN_SKIP_PATHS):
            continue
        yield path


def test_no_second_map_or_boundary_table_exists():
    roster = set(_roster_stages())
    assert roster, "the stage roster must parse before carrier uniqueness is judged"
    duplicates = []
    for path in _md_files():
        if path == OWNER:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if "强制状态" not in text and "门禁处理" not in text:
            continue
        for header, rows in _tables(text.splitlines()):
            if "强制状态" in header and "强制门禁" in header:
                for row in rows:
                    if len(row) >= 6 and row[0].strip("` ") in roster:
                        duplicates.append((str(path.relative_to(REPO_ROOT)), row[0]))
                        break
            if "门禁处理" in header and "边界" in header:
                ids = {row[0].strip("` ") for row in rows if row}
                if {"a", "b", "c", "d"} & ids:
                    duplicates.append((str(path.relative_to(REPO_ROOT)), "boundary table"))
                    break
    assert not duplicates, (
        "a second mapping/boundary carrier exists (contract C-1/C-9): %r" % (duplicates,)
    )


def test_no_second_document_claims_map_ownership():
    """A second claimant would be a document declaring itself the owner.

    ``唯一所有者`` as a phrase appears in plans that merely *point at* the owner
    ("put the map into the single owner"), so the detector requires an explicit
    ownership declaration line (``Owner`` + ``唯一所有者``) inside the opening
    block of a document that also names the map.
    """
    claims = []
    for path in _md_files():
        if path == OWNER:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        opening = "\n".join(lines[:30])
        if "同构映射" not in opening:
            continue
        for line in lines[:10]:
            if "Owner" in line and "唯一所有者" in line:
                claims.append(str(path.relative_to(REPO_ROOT)))
                break
    assert not claims, (
        "only the classification owner may claim the map; other claimants: %r" % (claims,)
    )


# --------------------------------------------------------------------------- #
# C-2 table shape and stage set
# --------------------------------------------------------------------------- #
def test_map_header_is_verbatim_and_has_eight_data_rows():
    header, rows = _map_rows()
    assert tuple(header) == MAP_HEADER, (
        "map header must match contract C-2 verbatim; got %r" % (header,)
    )
    assert len(rows) == 8, "the map must have exactly 8 data rows; got %d" % len(rows)
    for line_no, row in rows:
        assert len(row) == len(MAP_HEADER), (
            "map row on line %d has %d cell(s), expected %d (no blank row): %r"
            % (line_no, len(row), len(MAP_HEADER), row)
        )
        assert any(cell for cell in row), "map line %d is a blank row" % line_no


def test_stage_set_equals_the_roster_owner():
    roster = _roster_stages()
    assert len(roster) == 8, "the roster owner must yield 8 stages; got %r" % (roster,)
    _header, rows = _map_rows()
    stages = [row[0].strip("` ") for _line, row in rows]
    assert len(stages) == len(set(stages)), "duplicate stage rows: %r" % (stages,)
    assert set(stages) == set(roster), (
        "map stages must equal STAGE_ARTIFACTS keys; map=%r roster=%r"
        % (sorted(stages), sorted(roster))
    )


# --------------------------------------------------------------------------- #
# C-3 24 cells and the legend
# --------------------------------------------------------------------------- #
def test_all_24_cells_pair_a_code_side_with_a_document_side():
    header, rows = _map_rows()
    problems = []
    cells_seen = 0
    for stage, row in ((row[0].strip("` "), row) for _line, row in rows):
        for column in FACE_COLUMNS:
            cell = row[header.index(column)]
            cells_seen += 1
            problem = _cell_grammar_problem(cell)
            if problem:
                problems.append((stage, column, problem, cell))
    assert cells_seen == 24, "expected 24 face cells, saw %d" % cells_seen
    assert not problems, "cells missing the paired grammar (C-3): %r" % (problems,)


def test_face_legend_is_declared_once_before_the_table():
    text = _read(OWNER, "classification owner")
    lines = text.splitlines()
    body = _section_body(lines, "同构映射")
    assert body is not None
    table_index = next(
        (index for index, line in enumerate(body) if line.lstrip().startswith("|")), len(body)
    )
    prose = "\n".join(body[:table_index])
    for token in ("结构", "流程", "逻辑"):
        assert token in prose, "the pre-table legend must declare the %s face once" % token
    assert "实体" in prose and "关系" in prose and "边界" in prose, (
        "the structure face legend must name 实体 / 关系 / 边界"
    )


# --------------------------------------------------------------------------- #
# C-4 … C-7 enforcement truthfulness on the real tree
# --------------------------------------------------------------------------- #
def test_enforcement_status_is_closed_and_truthful():
    """Independent oracle for C-4…C-7 at reference granularity.

    ``已强制`` is true only when every claimed face has a ``gate:<算子 id>``
    citation that resolves to a ``blocking`` operator row *at that same*
    ``(stage, face)``. The check deliberately stops at the reference: whether the
    free-text cell means what it cites is the review face's call (C-10).
    """
    faces, operators = _gate_owner()
    by_id = {gate_id: (stage, face, level) for gate_id, stage, face, level, _op in operators}
    blocking_pairs = {
        (stage, face) for _gid, stage, face, level, _op in operators if level == "blocking"
    }
    blocking_stages = {stage for _gid, stage, _face, level, _op in operators if level == "blocking"}
    header, rows = _map_rows()
    problems = []
    for line_no, row in rows:
        stage = row[0].strip("` ")
        status = row[header.index("强制状态")].strip("` ")
        gate_cell = row[header.index("强制门禁")]
        ref_cell = row[header.index("强制门禁引用")]
        named = _face_ids_in(gate_cell, faces)
        tokens = [
            token.strip("`")
            for token in re.split(r"[、,，/\s]+", gate_cell.strip("` "))
            if token.strip("`") and token.strip("`") not in ("—", "-")
        ]
        unknown = [token for token in tokens if token not in faces]
        refs = [
            token.strip("`")
            for token in re.split(r"[、,，/\s]+", ref_cell.strip("` "))
            if token.strip("`") and token.strip("`") not in ("—", "-")
        ]
        if status not in STATUS_VALUES:
            problems.append((stage, "status %r outside the closed set" % status))
            continue
        if status == ENFORCED:
            if not named:
                problems.append((stage, "已强制 without a closed face id"))
            for face in named:
                if (stage, face) not in blocking_pairs:
                    problems.append(
                        (stage, "%s has no blocking operator at this stage" % face)
                    )
            if unknown:
                problems.append((stage, "unknown face id(s) %r" % (unknown,)))
            if not refs:
                problems.append((stage, "已强制 without a 强制门禁引用"))
            covered = set()
            for ref in refs:
                if not ref.startswith(GATE_REF_PREFIX):
                    problems.append((stage, "%r lacks the gate: prefix" % ref))
                    continue
                target = by_id.get(ref[len(GATE_REF_PREFIX):])
                if target is None:
                    problems.append((stage, "%r names no declared operator id" % ref))
                    continue
                ref_stage, ref_face, ref_level = target
                if ref_stage != stage:
                    problems.append((stage, "%r resolves to stage %r" % (ref, ref_stage)))
                    continue
                if ref_level != "blocking":
                    problems.append((stage, "%r resolves to a non-blocking row" % ref))
                    continue
                if ref_face not in named:
                    problems.append((stage, "%r resolves to unclaimed face %r" % (ref, ref_face)))
                    continue
                covered.add(ref_face)
            for face in named:
                if face not in covered:
                    problems.append((stage, "%s has no resolving gate: reference" % face))
        else:
            if named or unknown or refs:
                problems.append(
                    (stage, "已声明未强制 must leave 强制门禁 / 强制门禁引用 empty")
                )
            if stage in blocking_stages:
                problems.append((stage, "stage has blocking operators but is declared unenforced"))
    assert not problems, "enforcement annotations are not true (C-4…C-7): %r" % (problems,)


# --------------------------------------------------------------------------- #
# C-8 / C-9 boundary table on the real tree
# --------------------------------------------------------------------------- #
def test_boundary_table_has_the_declared_header_and_ids_a_to_d():
    header, rows = _boundary_rows()
    assert tuple(header) == BOUNDARY_HEADER, (
        "boundary header must match contract C-8 verbatim; got %r" % (header,)
    )
    ids = [row[0].strip("` ") for _line, row in rows if row]
    assert len(rows) == 4, "the boundary table must have exactly 4 data rows; got %d" % len(rows)
    assert sorted(ids) == ["a", "b", "c", "d"], "boundary ids must be a–d once each; got %r" % (ids,)


def test_every_boundary_binds_a_closed_face_and_a_handling():
    faces, _operators = _gate_owner()
    header, rows = _boundary_rows()
    problems = []
    for _line, row in rows:
        boundary = row[0].strip("` ")
        reason = row[header.index("为什么不能互换")].strip()
        handling = row[header.index("门禁处理")].strip()
        if not reason:
            problems.append((boundary, "empty reason"))
        named = _face_ids_in(handling, faces)
        if not named:
            problems.append((boundary, "no closed face id in 门禁处理"))
            continue
        residual = handling
        for face in named:
            residual = residual.replace(face, "")
        residual = re.sub(r"[`\s、,，。；;：:/+—\-（）()\[\]]+", "", residual)
        if len(residual) < 4:
            problems.append((boundary, "face id present but no handling explanation"))
    assert not problems, "boundaries are unbound or malformed (C-9): %r" % (problems,)


# --------------------------------------------------------------------------- #
# C-10 / C-11 / C-12 mechanical floors
# --------------------------------------------------------------------------- #
def test_no_doc_is_code_licence_sentence_without_owner_pointer():
    targets = sorted((REPO_ROOT / "templates" / "commands").glob("*.md"))
    for layer in ("external", "internal"):
        targets.extend(sorted((REPO_ROOT / "skills" / layer).glob("*/SKILL.md")))
    offenders = []
    for path in targets:
        text = path.read_text(encoding="utf-8")
        for match in LICENCE_RE.finditer(text):
            start = text.rfind("\n\n", 0, match.start())
            end = text.find("\n\n", match.end())
            paragraph = text[start if start >= 0 else 0:end if end >= 0 else len(text)]
            if "flow-class-definitions.md" not in paragraph:
                offenders.append(
                    (str(path.relative_to(REPO_ROOT)), paragraph.strip()[:120])
                )
    assert not offenders, (
        "「文档即代码」licence sentence without an owner pointer (C-10): %r" % (offenders,)
    )


def test_gate_operator_column_carries_no_code_type_operator():
    _faces, operators = _gate_owner()
    hits = []
    for _gid, stage, _face, _level, operator in operators:
        lowered = operator.lower()
        for token in CODE_OPERATORS:
            if token in lowered:
                hits.append((stage, token, operator))
    assert not hits, "code-type operators transplanted into the gate owner (C-11): %r" % (hits,)


def _medium_hits(cell: str) -> list[str]:
    normalized = re.sub(r"\s+", "", cell).lower()
    return [
        phrase
        for phrase in MEDIUM_PHRASES
        if re.sub(r"\s+", "", phrase).lower() in normalized
    ]


def test_neither_table_uses_a_medium_axis_phrase():
    map_header, map_rows = _map_rows()
    boundary_header, boundary_rows = _boundary_rows()
    hits = []
    for line_no, row in map_rows:
        for cell in row:
            if _medium_hits(cell):
                hits.append(("map", line_no, cell))
    for line_no, row in boundary_rows:
        for cell in row:
            if _medium_hits(cell):
                hits.append(("boundary", line_no, cell))
    assert not hits, "medium-axis classification phrase in the two tables (C-12): %r" % (hits,)


# --------------------------------------------------------------------------- #
# engine: the real tree is clean
# --------------------------------------------------------------------------- #
def test_engine_reports_eight_stages_six_gates_and_zero_findings():
    proc, record = _engine(REPO_ROOT)
    assert proc.returncode == 0, (
        "the real tree must exit 0; findings=%r stderr=%r"
        % (None if record is None else record.get("findings"), proc.stderr)
    )
    assert record is not None, "the isomorphism action must print a JSON document"
    assert record.get("action") == "isomorphism"
    assert record.get("stages") == 8, "stages must report 8 rows; got %r" % record.get("stages")
    assert record.get("gates") == 6, "gates must report the six closed faces; got %r" % record.get("gates")
    assert record.get("findings") == []


# --------------------------------------------------------------------------- #
# engine: injections on a temporary copy must each turn red
# --------------------------------------------------------------------------- #
def _fixture(tmp_path: Path, mutate_owner=None, mutate_gates=None) -> Path:
    owner_text = _read(OWNER, "classification owner")
    gates_text = _read(GATES, "gate owner")
    if mutate_owner is not None:
        owner_text = mutate_owner(owner_text)
    if mutate_gates is not None:
        gates_text = mutate_gates(gates_text)
    (tmp_path / COMMANDS_REL).mkdir(parents=True, exist_ok=True)
    (tmp_path / COMMANDS_REL / "fixture.md").write_text(
        "# /speckit.fixture\n\nfixture template\n", encoding="utf-8"
    )
    for rel, text in (
        (OWNER_REL, owner_text),
        (GATES_REL, gates_text),
        (ROSTER_REL, ROSTER.read_text(encoding="utf-8")),
    ):
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


def _row_line(lines: list[str], keyword: str, first_cell: str) -> int:
    """Index of the data row whose first cell is ``first_cell`` inside § keyword.

    The line numbers returned by ``_first_table`` are relative to the section
    body; this helper works on the whole document so a rewrite never lands on an
    unrelated line.
    """
    start = next(
        (
            index
            for index, line in enumerate(lines)
            if (HEADING_RE.match(line) and keyword in line)
        ),
        None,
    )
    assert start is not None, "fixture owner lost § %s" % keyword
    level = len(HEADING_RE.match(lines[start]).group(1))
    index = start + 1
    while index < len(lines):
        match = HEADING_RE.match(lines[index])
        if match and len(match.group(1)) <= level:
            break
        line = lines[index]
        if line.lstrip().startswith("|"):
            row = _cells(line)
            if (
                row
                and not _is_separator(row)
                and row[0].strip("` ") == first_cell
                and len(row) >= 2
            ):
                return index
        index += 1
    raise AssertionError("fixture row %r not found in § %s" % (first_cell, keyword))


def _rewrite_rows(text: str, keyword: str, match_first_cell: str, changes: dict[int, str]) -> str:
    lines = text.splitlines()
    index = _row_line(lines, keyword, match_first_cell)
    updated = _cells(lines[index])
    for cell_index, value in changes.items():
        updated[cell_index] = value
    lines[index] = "| " + " | ".join(updated) + " |"
    return "\n".join(lines)


def _delete_row(text: str, keyword: str, first_cell: str) -> str:
    lines = text.splitlines()
    del lines[_row_line(lines, keyword, first_cell)]
    return "\n".join(lines)


def _append_operator_row(text: str, row: str) -> str:
    lines = text.splitlines()
    start = next(
        index for index, line in enumerate(lines) if HEADING_RE.match(line) and "阶段算子表" in line
    )
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if HEADING_RE.match(lines[index])
        ),
        len(lines),
    )
    last_table_line = max(
        index for index in range(start, end) if lines[index].lstrip().startswith("|")
    )
    lines.insert(last_table_line + 1, row)
    return "\n".join(lines)


def _map_index(header, column: str) -> int:
    return header.index(column)


def test_injected_false_enforced_turns_red(tmp_path):
    header, _rows = _map_rows()
    owner_text = _read(OWNER, "classification owner")

    def mutate(text: str) -> str:
        # implement carries reader-purpose as advisory only.
        return _rewrite_rows(
            text,
            "同构映射",
            "implement",
            {
                _map_index(header, "强制门禁"): "`reader-purpose`",
                _map_index(header, "强制状态"): ENFORCED,
            },
        )

    _fixture(tmp_path, mutate_owner=mutate)
    proc, record = _engine(tmp_path)
    assert proc.returncode == 1
    assert "annotation-false-enforced" in [f["kind"] for f in record["findings"]], (
        "an advisory-only face claimed as enforced must be reported: %r" % (record["findings"],)
    )


def test_injected_false_unenforced_turns_red(tmp_path):
    header, _rows = _map_rows()

    def mutate(text: str) -> str:
        # requirements carries blocking operators, so "declared unenforced" is false.
        return _rewrite_rows(
            text,
            "同构映射",
            "requirements",
            {
                _map_index(header, "强制门禁"): "—",
                _map_index(header, "强制状态"): DECLARED_UNENFORCED,
            },
        )

    _fixture(tmp_path, mutate_owner=mutate)
    proc, record = _engine(tmp_path)
    assert proc.returncode == 1
    assert "annotation-false-unenforced" in [f["kind"] for f in record["findings"]], (
        "a stage with blocking operators declared unenforced must be reported: %r"
        % (record["findings"],)
    )


def test_injected_slogan_row_turns_red(tmp_path):
    header, _rows = _map_rows()

    def mutate(text: str) -> str:
        return _rewrite_rows(
            text,
            "同构映射",
            "plan",
            {
                _map_index(header, "强制门禁"): "",
                _map_index(header, "强制状态"): "",
            },
        )

    _fixture(tmp_path, mutate_owner=mutate)
    proc, record = _engine(tmp_path)
    assert proc.returncode == 1
    assert "slogan-row" in [f["kind"] for f in record["findings"]], (
        "a row with neither a face nor the annotation is a slogan row: %r"
        % (record["findings"],)
    )


def test_injected_boundary_missing_turns_red(tmp_path):
    def mutate(text: str) -> str:
        return _delete_row(text, "不可同构边界", "c")

    _fixture(tmp_path, mutate_owner=mutate)
    proc, record = _engine(tmp_path)
    assert proc.returncode == 1
    assert "boundary-missing" in [f["kind"] for f in record["findings"]], (
        "a deleted boundary row must be reported: %r" % (record["findings"],)
    )


def test_injected_boundary_unbound_turns_red(tmp_path):
    header, _rows = _boundary_rows()

    def mutate(text: str) -> str:
        return _rewrite_rows(
            text,
            "不可同构边界",
            "c",
            {header.index("门禁处理"): "由评审面按读者基准复核，不依赖封闭面"},
        )

    _fixture(tmp_path, mutate_owner=mutate)
    proc, record = _engine(tmp_path)
    assert proc.returncode == 1
    assert "boundary-unbound" in [f["kind"] for f in record["findings"]], (
        "a boundary whose handling names no closed face id is unbound: %r"
        % (record["findings"],)
    )


def test_injected_boundary_malformed_turns_red(tmp_path):
    header, _rows = _boundary_rows()

    def mutate(text: str) -> str:
        return _rewrite_rows(
            text,
            "不可同构边界",
            "b",
            {header.index("为什么不能互换"): ""},
        )

    _fixture(tmp_path, mutate_owner=mutate)
    proc, record = _engine(tmp_path)
    assert proc.returncode == 1
    assert "boundary-malformed" in [f["kind"] for f in record["findings"]], (
        "a boundary with an empty reason is malformed: %r" % (record["findings"],)
    )


def test_injected_medium_axis_phrase_turns_red(tmp_path):
    def mutate(text: str) -> str:
        return _rewrite_rows(
            text,
            "同构映射",
            "tasks",
            {1: "代码型：任务清单与覆盖检查 ↔ 文档型：任务叙述与证据标注（按扩展名判定）"},
        )

    _fixture(tmp_path, mutate_owner=mutate)
    proc, record = _engine(tmp_path)
    assert proc.returncode == 1
    assert "medium-axis-in-map" in [f["kind"] for f in record["findings"]], (
        "a medium-axis classification reason must be reported: %r" % (record["findings"],)
    )


def test_injected_code_operator_turns_red(tmp_path):
    def mutate(text: str) -> str:
        return _append_operator_row(
            text,
            "| requirements | `G-injected` | `pytest -q tests/` | requirements-clarity | advisory |"
        )

    _fixture(tmp_path, mutate_gates=mutate)
    proc, record = _engine(tmp_path)
    assert proc.returncode == 1
    assert "code-operator-in-expression-gates" in [f["kind"] for f in record["findings"]], (
        "a code-type operator in the gate owner must be reported: %r" % (record["findings"],)
    )


# --------------------------------------------------------------------------- #
# C-5 at reference granularity: the gate citation itself must be falsifiable
# --------------------------------------------------------------------------- #
def test_injected_missing_gate_reference_turns_red(tmp_path):
    header, _rows = _map_rows()

    def mutate(text: str) -> str:
        return _rewrite_rows(
            text, "同构映射", "tasks", {header.index("强制门禁引用"): ""}
        )

    _fixture(tmp_path, mutate_owner=mutate)
    proc, record = _engine(tmp_path)
    assert proc.returncode == 1
    kinds = [f["kind"] for f in record["findings"]]
    assert "gate-ref-missing" in kinds, (
        "an enforced row with no gate reference must be reported: %r" % record["findings"]
    )


def test_injected_wrong_gate_reference_turns_red(tmp_path):
    header, _rows = _map_rows()

    def mutate(text: str) -> str:
        return _rewrite_rows(
            text,
            "同构映射",
            "requirements",
            {header.index("强制门禁引用"): "`gate:G-clarify-reader`"},
        )

    _fixture(tmp_path, mutate_owner=mutate)
    proc, record = _engine(tmp_path)
    assert proc.returncode == 1
    kinds = [f["kind"] for f in record["findings"]]
    assert "gate-ref-mismatch" in kinds, (
        "a reference resolving to another stage/face must be reported: %r"
        % record["findings"]
    )
    assert "gate-ref-missing" in kinds, (
        "the two claimed faces lose their coverage when the reference moves: %r"
        % record["findings"]
    )


def test_injected_unknown_gate_id_turns_red(tmp_path):
    header, _rows = _map_rows()

    def mutate(text: str) -> str:
        return _rewrite_rows(
            text,
            "同构映射",
            "plan",
            {header.index("强制门禁引用"): "`gate:G-no-such-operator`"},
        )

    _fixture(tmp_path, mutate_owner=mutate)
    proc, record = _engine(tmp_path)
    assert proc.returncode == 1
    assert "gate-ref-unknown" in [f["kind"] for f in record["findings"]], (
        "a reference to an undeclared operator id must be reported: %r"
        % record["findings"]
    )


def test_injected_advisory_gate_reference_turns_red(tmp_path):
    header, _rows = _map_rows()

    def mutate(text: str) -> str:
        # implement's reader-purpose operator is advisory only.
        return _rewrite_rows(
            text,
            "同构映射",
            "implement",
            {header.index("强制门禁引用"): "`gate:G-implement-reader`"},
        )

    _fixture(tmp_path, mutate_owner=mutate)
    proc, record = _engine(tmp_path)
    assert proc.returncode == 1
    assert "gate-ref-not-blocking" in [f["kind"] for f in record["findings"]], (
        "a reference resolving to an advisory operator must be reported: %r"
        % record["findings"]
    )
