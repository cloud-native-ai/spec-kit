"""Unit tests for the ``isomorphism`` action of ``flow-class-check.py`` (069b, T004).

Owns the parser/behaviour details the contract
``.specify/specs/069b-isomorphism-migration-metrics/contracts/isomorphism-map.md``
delegates to an implementation test — the parts a whole-repository contract test
cannot isolate:

* the stage roster is **read from its owner** (``skills/external/sdd-loop-driver/
  scripts/loop-state.py`` → ``STAGE_ARTIFACTS`` top-level keys). A fixture whose
  roster carries four non-canonical stage names must be judged against *those*
  names: an engine with an inlined eight-stage list would either pass a map that
  disagrees with the roster or reject a map that agrees with it;
* the cell grammar boundaries (C-3): a missing ``↔``, two ``↔``, or a side under
  eight characters each report ``cell-malformed``;
* the ``(stage, face)`` blocking set (C-5 / C-6): an advisory row never counts as
  enforcement, and a blocking row at *another* stage never substitutes for the
  row's own stage;
* the payload-root branch (C-13): a tree with neither ``templates/commands/`` nor
  a parseable ``skills/{external,internal}/`` exits 2 with
  ``framework-source-required``, zero findings, and no green verdict.

Fixtures are built from scratch in ``tmp_path``; no test reads or writes the real
owner document. Red-first (Constitution IV): the engine exists (069a) but has no
``isomorphism`` action yet, so every call here fails as "action missing" — never
as an import or collection error. ``_run`` asserts the script path first.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"

OWNER_REL = Path("shared") / "definitions" / "flow-class-definitions.md"
GATES_REL = Path("shared") / "workflow" / "expression-gates.md"
ROSTER_REL = Path("skills") / "external" / "sdd-loop-driver" / "scripts" / "loop-state.py"
COMMANDS_REL = Path("templates") / "commands"

# Contract C-2 / C-4: pinned copies of the exact strings the owner tables carry.
MAP_HEADER = (
    "阶段",
    "结构（实体 / 关系 / 边界）",
    "流程（阶段与门禁角色）",
    "逻辑（证据 / 契约 / 验收 / 版本 / 所有权）",
    "强制门禁",
    "强制状态",
)
BOUNDARY_HEADER = ("边界", "不可互换的判定面", "为什么不能互换", "门禁处理")
ENFORCED = "已强制"
DECLARED_UNENFORCED = "已声明未强制"

FACES = (
    "requirements-clarity",
    "reader-purpose",
    "evidence-asof",
    "structure-links-build",
    "fact-consistency",
    "review",
)
ISO_Z_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run(*args: str) -> subprocess.CompletedProcess:
    assert ENGINE.is_file(), (
        "flow-class engine missing: %s — expected from 069a. "
        "Red is the intended pre-implementation state for 069b T004."
        % ENGINE.relative_to(REPO_ROOT)
    )
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )


def _json(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), (
        "expected a JSON document on stdout, got empty output (stderr: %r)" % proc.stderr
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            "stdout is not JSON (%s); head=%r" % (exc, proc.stdout[:400])
        ) from exc


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _pair(label: str) -> str:
    """A well-formed cell: one ``↔``, both sides >= 8 characters (C-3)."""
    return "代码型：%s 的产物与判定面 ↔ 文档型：%s 的章节与读者面" % (label, label)


def _roster_source(stages: list[str]) -> str:
    entries = "\n".join(
        '    "%s": {"artifacts": [], "owned_paths": [], '
        '"commit_required": True, "no_change_allowed": False},' % stage
        for stage in stages
    )
    return (
        "#!/usr/bin/env python3\n"
        '"""fixture roster — the stage map owner for 069b unit tests."""\n\n'
        "STAGE_ARTIFACTS = {\n%s\n}\n\n"
        "OTHER_TABLE = {\n"
        '    "not-a-stage": {"artifacts": []},\n'
        "}\n" % entries
    )


def _gates_source(stages: list[str], operator_rows: list[tuple[str, str, str]]) -> str:
    lines = [
        "# Expression Gates (unit-test fixture)",
        "",
        "## 六面（封闭集）",
        "",
        "| 面（中文） | face id | owner_pointer |",
        "| --- | --- | --- |",
    ]
    for face in FACES:
        lines.append("| %s | %s | `fixture.md` |" % (face, face))
    lines.extend(
        [
            "",
            "## 阶段算子表",
            "",
            "| 阶段 | 执行算子 | 对应面 | 阻断级别 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for stage, face, level in operator_rows:
        lines.append("| %s | `fixture-check-%s` | %s | %s |" % (stage, stage, face, level))
    lines.extend(["", "## 读者声明", "", "fixture.", ""])
    return "\n".join(lines)


def _map_row(stage: str, faces: list[str] | None, status: str, cells=None) -> str:
    if cells is None:
        cells = [_pair(stage), _pair(stage), _pair(stage)]
    gate_cell = "、".join("`%s`" % face for face in faces) if faces else "—"
    return "| %s | %s | %s | %s | %s | %s |" % (
        stage,
        cells[0],
        cells[1],
        cells[2],
        gate_cell,
        status,
    )


def _owner_source(rows: list[str], boundary_rows=None, extra_sections: str = "") -> str:
    if boundary_rows is None:
        boundary_rows = [
            "| a | 验收 oracle | 执行行为不能替代阅读理解 | `review` 面按读者基准判定 |",
            "| b | 验证算子 | 测试不能替代构建与链接检查 | `structure-links-build` 面按必要条件执行 |",
            "| c | 失败可见性 | 运行期偏差会可见、陈旧事实不会 | `evidence-asof` 面强制三件套 |",
            "| d | 语义 oracle | 文档没有编译器 | `reader-purpose` 面声明读者与场景 |",
        ]
    lines = [
        "# Flow Class Definitions (unit-test fixture)",
        "",
        "**Owner（唯一所有者）**: fixture owns 判据、同构映射、不可同构边界。",
        "",
        "## 同构映射（8 阶段 × 3 面）",
        "",
        "legend：结构 = 实体 / 关系 / 边界；流程 = 阶段与门禁角色；逻辑 = 证据 / 契约 / 验收 / 版本 / 所有权。",
        "",
        "| " + " | ".join(MAP_HEADER) + " |",
        "| " + " | ".join("---" for _ in MAP_HEADER) + " |",
    ]
    lines.extend(rows)
    lines.extend(
        [
            "",
            "## 不可同构边界",
            "",
            "| " + " | ".join(BOUNDARY_HEADER) + " |",
            "| " + " | ".join("---" for _ in BOUNDARY_HEADER) + " |",
        ]
    )
    lines.extend(boundary_rows)
    lines.append("")
    lines.append(extra_sections)
    return "\n".join(lines)


def _build_repo(
    root: Path,
    *,
    stages=("alpha", "beta", "gamma", "delta"),
    operator_rows=None,
    rows=None,
    boundary_rows=None,
    roster_source=None,
    gates_source=None,
    owner_source=None,
) -> Path:
    """Materialise a self-contained framework-source fixture at ``root``."""
    if operator_rows is None:
        operator_rows = [
            ("alpha", "requirements-clarity", "blocking"),
            ("beta", "reader-purpose", "blocking"),
            ("gamma", "fact-consistency", "blocking"),
            ("delta", "structure-links-build", "advisory"),
        ]
    if rows is None:
        rows = [
            _map_row("alpha", ["requirements-clarity"], ENFORCED),
            _map_row("beta", ["reader-purpose"], ENFORCED),
            _map_row("gamma", ["fact-consistency"], ENFORCED),
            _map_row("delta", None, DECLARED_UNENFORCED),
        ]
    _write(root / COMMANDS_REL / "fixture.md", "# /speckit.fixture\n\nfixture template\n")
    _write(root / ROSTER_REL, roster_source if roster_source is not None else _roster_source(list(stages)))
    _write(
        root / GATES_REL,
        gates_source if gates_source is not None else _gates_source(list(stages), operator_rows),
    )
    _write(root / OWNER_REL, owner_source if owner_source is not None else _owner_source(rows, boundary_rows))
    return root


def _iso(root: Path):
    proc = _run("--action", "isomorphism", "--repo", str(root), "--format", "json")
    return proc, _json(proc)


def _kinds(record: dict) -> list[str]:
    return [finding["kind"] for finding in record["findings"]]


def _kinds_for(record: dict, stage: str) -> list[str]:
    return [
        finding["kind"]
        for finding in record["findings"]
        if finding.get("stage") == stage
    ]


# --------------------------------------------------------------------------- #
# the stage roster is read from its owner, never inlined
# --------------------------------------------------------------------------- #
def test_roster_is_parsed_from_loop_state_not_a_builtin_list(tmp_path):
    _build_repo(tmp_path)
    proc, record = _iso(tmp_path)
    assert proc.returncode == 0, (
        "a four-stage roster with a matching map must be clean; findings=%r stderr=%r"
        % (record.get("findings"), proc.stderr)
    )
    assert record.get("action") == "isomorphism"
    assert ISO_Z_RE.match(str(record.get("checked_at", ""))), (
        "checked_at must be ISO-8601 Z; got %r" % record.get("checked_at")
    )
    assert record.get("stages") == 4, (
        "stages is the parsed row count and must follow the fixture roster (4), not a "
        "built-in eight-stage list; got %r" % record.get("stages")
    )
    assert record.get("gates") == 6
    assert record.get("findings") == []


def test_canonical_stage_names_against_a_custom_roster_report_stage_set_mismatch(tmp_path):
    canonical = (
        "requirements",
        "clarify",
        "plan",
        "tasks",
        "checklist",
        "analyze",
        "implement",
        "review",
    )
    rows = [
        _map_row(stage, None, DECLARED_UNENFORCED)
        for stage in canonical
    ]
    _build_repo(tmp_path, rows=rows)
    proc, record = _iso(tmp_path)
    assert proc.returncode == 1
    assert "stage-set-mismatch" in _kinds(record), (
        "a map whose stage set disagrees with the roster must be a finding; got %r"
        % (record["findings"],)
    )


def test_unparsable_roster_exits_2_with_roster_unavailable(tmp_path):
    _build_repo(tmp_path, roster_source="# no STAGE_ARTIFACTS here\n")
    proc, record = _iso(tmp_path)
    assert proc.returncode == 2
    assert record.get("findings") == [], (
        "an unreadable roster is an input error, never a finding set: %r"
        % (record["findings"],)
    )
    assert (record.get("error") or {}).get("label") == "roster-unavailable"
    assert "roster-unavailable" in proc.stderr


# --------------------------------------------------------------------------- #
# cell grammar boundaries (C-3)
# --------------------------------------------------------------------------- #
def _one_bad_cell(tmp_path, bad_cell: str):
    rows = [
        _map_row("alpha", ["requirements-clarity"], ENFORCED),
        _map_row("beta", ["reader-purpose"], ENFORCED),
        _map_row(
            "gamma",
            ["fact-consistency"],
            ENFORCED,
            cells=[_pair("gamma"), bad_cell, _pair("gamma")],
        ),
        _map_row("delta", None, DECLARED_UNENFORCED),
    ]
    _build_repo(tmp_path, rows=rows)
    return _iso(tmp_path)


def test_cell_without_arrow_is_cell_malformed(tmp_path):
    proc, record = _one_bad_cell(tmp_path, "代码型：只有一侧的产物")
    assert proc.returncode == 1
    assert "cell-malformed" in _kinds_for(record, "gamma")


def test_cell_with_two_arrows_is_cell_malformed(tmp_path):
    proc, record = _one_bad_cell(
        tmp_path, "代码型：甲侧的产物面 ↔ 文档型：乙侧的产物面 ↔ 多余的第三侧"
    )
    assert proc.returncode == 1
    assert "cell-malformed" in _kinds_for(record, "gamma")


def test_cell_side_under_eight_characters_is_cell_malformed(tmp_path):
    proc, record = _one_bad_cell(tmp_path, "代码型：x ↔ 文档型：y")
    assert proc.returncode == 1
    assert "cell-malformed" in _kinds_for(record, "gamma")


# --------------------------------------------------------------------------- #
# the (stage, face) blocking set (C-5 / C-6)
# --------------------------------------------------------------------------- #
def test_advisory_only_face_cannot_be_claimed_enforced(tmp_path):
    rows = [
        _map_row("alpha", ["requirements-clarity"], ENFORCED),
        _map_row("beta", ["reader-purpose"], ENFORCED),
        _map_row("gamma", ["fact-consistency"], ENFORCED),
        _map_row("delta", ["structure-links-build"], ENFORCED),
    ]
    _build_repo(tmp_path, rows=rows)
    proc, record = _iso(tmp_path)
    assert proc.returncode == 1
    assert "annotation-false-enforced" in _kinds_for(record, "delta"), (
        "an advisory-only face is not enforcement; got %r" % (record["findings"],)
    )


def test_blocking_at_another_stage_does_not_substitute(tmp_path):
    # fact-consistency is blocking at gamma only; beta carries reader-purpose.
    rows = [
        _map_row("alpha", ["requirements-clarity"], ENFORCED),
        _map_row("beta", ["fact-consistency"], ENFORCED),
        _map_row("gamma", ["fact-consistency"], ENFORCED),
        _map_row("delta", None, DECLARED_UNENFORCED),
    ]
    _build_repo(tmp_path, rows=rows)
    proc, record = _iso(tmp_path)
    assert proc.returncode == 1
    assert "annotation-false-enforced" in _kinds_for(record, "beta"), (
        "another stage's blocking row must not backfill this stage; got %r"
        % (record["findings"],)
    )


def test_advisory_only_stage_may_be_declared_unenforced(tmp_path):
    _build_repo(tmp_path)
    proc, record = _iso(tmp_path)
    assert proc.returncode == 0
    assert "annotation-false-unenforced" not in _kinds_for(record, "delta"), (
        "an advisory-only stage is truthfully '已声明未强制'; got %r"
        % (record["findings"],)
    )


# --------------------------------------------------------------------------- #
# the payload-root branch (C-13)
# --------------------------------------------------------------------------- #
def test_payload_root_exits_2_with_framework_source_required(tmp_path):
    payload = tmp_path / ".specify"
    _write(payload / "shared" / "definitions" / "flow-class-definitions.md", _owner_source([]))
    proc, record = _iso(tmp_path)
    assert proc.returncode == 2, (
        "a payload root is an input error, not a green run; stdout=%r stderr=%r"
        % (proc.stdout, proc.stderr)
    )
    assert record.get("findings") == [], (
        "the payload-root branch must not emit findings: %r" % (record["findings"],)
    )
    assert (record.get("error") or {}).get("label") == "framework-source-required"
    assert "framework-source-required" in proc.stderr


# --------------------------------------------------------------------------- #
# read-only
# --------------------------------------------------------------------------- #
def test_isomorphism_action_writes_nothing(tmp_path):
    _build_repo(tmp_path)

    def snapshot() -> dict[str, str]:
        digests = {}
        for path in sorted(tmp_path.rglob("*")):
            if path.is_file():
                digests[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        return digests

    before = snapshot()
    proc = _run("--action", "isomorphism", "--repo", str(tmp_path), "--format", "json")
    assert proc.returncode == 0
    after = snapshot()
    assert before == after, "the isomorphism action must be read-only (zero writes)"
