"""Unit tests for the 069b reconciler extensions (T018).

Owns the boundary behaviour that the contract tests
(``test_ledger_reconciliation.py`` / ``test_delegation_classes.py`` /
``test_expression_faces.py``) only touch at their outer edges:

* the ``LEDGER_FLOOR`` derivation — ``⌊(27 + 51) / 2⌋ = 39``, taken from the
  inventory-side floor constants, never from the inspected ledger and never a
  third hand-written unit count. The 38 / 39 / 40 boundary is exercised, and a
  100-row ledger must not move the floor;
* the coverage arithmetic combinations and the necessary-but-not-sufficient
  relation between the four conditions and ``clean``;
* the ``red_kind`` priority ladder
  (``owner-unavailable`` > ``framework-source-required`` > ``parse-failure`` >
  ``gap`` > ``clean``) with one fixture per rung;
* the delegation grammar (optional ``.specify/`` prefix, optional layer, the
  canonical name class, placeholder rejection) and per-template de-duplication;
* the ``owner_pointer`` grammar (``+`` joins paths into one binding, ``§``
  anchor must match a heading).

Fixtures are minimal framework-source trees; nothing here reads the real owner.
Red-first (Constitution IV): every assertion reads a field or an action 069a's
engine does not have yet, so red is "action / field missing" — never an import
or collection error. ``_run`` asserts the script path first.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"
OWNER_REL = Path("shared") / "definitions" / "flow-class-definitions.md"
GATES_REL = Path("shared") / "workflow" / "expression-gates.md"
COMMANDS_REL = Path("templates") / "commands"

EXECUTION = "execution"
EXPRESSION = "expression"
FLOOR_COMMANDS = 27
FLOOR_SKILLS = 51
LEDGER_FLOOR = (FLOOR_COMMANDS + FLOOR_SKILLS) // 2  # 39
VERSION_LINE = "**台账版本**: 1（2026-10-25）"
LEDGER_COLUMNS = ("unit_id", "flow_class", "basis", "neutral", "notes")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run(*args: str) -> subprocess.CompletedProcess:
    assert ENGINE.is_file(), (
        "flow-class engine missing: %s — expected from 069a. "
        "Red is the intended pre-implementation state for 069b T018."
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


def _render_owner(rows, *, version=VERSION_LINE, extra=()):
    lines = [
        "# Flow Class Definitions (069b unit fixture)",
        "",
        "## 逐流程台账",
        "",
    ]
    if version is not None:
        lines.extend([version, ""])
    lines.append("| " + " | ".join(LEDGER_COLUMNS) + " |")
    lines.append("| " + " | ".join("---" for _ in LEDGER_COLUMNS) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(c, "")) for c in LEDGER_COLUMNS) + " |")
    lines.extend(extra)
    lines.extend(
        [
            "",
            "## 类中立清单",
            "",
            "| unit_id | category | rationale |",
            "| --- | --- | --- |",
            "",
        ]
    )
    return "\n".join(lines)


def _rows(commands=FLOOR_COMMANDS, skills=FLOOR_SKILLS):
    stems = ["cmd-%02d" % n for n in range(1, commands + 1)]
    names = ["skill-%02d" % n for n in range(1, skills + 1)]
    out = []
    for index, stem in enumerate(stems):
        out.append(
            {
                "unit_id": "/speckit.%s" % stem,
                "flow_class": EXECUTION if index % 2 == 0 else EXPRESSION,
                "basis": "behavior-oracle",
                "neutral": "",
                "notes": "",
            }
        )
    for index, name in enumerate(names):
        out.append(
            {
                "unit_id": "skill:%s" % name,
                "flow_class": EXECUTION if index % 2 == 0 else EXPRESSION,
                "basis": "reader-oracle",
                "neutral": "",
                "notes": "",
            }
        )
    return out


def _build(root: Path, *, commands=FLOOR_COMMANDS, skills=FLOOR_SKILLS, rows=None, owner_text=None):
    for stem in ["cmd-%02d" % n for n in range(1, commands + 1)]:
        _write(root / COMMANDS_REL / ("%s.md" % stem), "# /speckit.%s\n" % stem)
    for index, name in enumerate(["skill-%02d" % n for n in range(1, skills + 1)]):
        layer = "external" if index < 14 else "internal"
        _write(
            root / "skills" / layer / name / "SKILL.md",
            "---\nname: %s\ndescription: fixture\n---\n" % name,
        )
    used = rows if rows is not None else _rows(commands, skills)
    _write(root / OWNER_REL, owner_text if owner_text is not None else _render_owner(used))
    return used


def _check(root: Path):
    proc = _run("--action", "check", "--repo", str(root), "--format", "json")
    record = _json(proc) if proc.stdout.strip() else None
    return proc, record


def _coverage(record: dict) -> dict:
    assert record is not None, "check must print JSON"
    assert isinstance(record.get("coverage"), dict), (
        "check JSON must carry `coverage` (C-2); got %r" % (record.get("coverage"),)
    )
    return record["coverage"]


def _red_kind(record: dict) -> str:
    assert record is not None, "check must print JSON"
    assert "red_kind" in record, (
        "check JSON must carry `red_kind` (C-3); keys=%r" % sorted(record)
    )
    return record["red_kind"]


def _kinds(record: dict) -> list[str]:
    return [finding.get("kind") for finding in record.get("findings", [])]


def _edge_records(record: dict) -> list[dict]:
    keys = ("command", "skill", "command_class", "skill_class", "verdict", "source_line")
    found: list[dict] = []

    def walk(node):
        if isinstance(node, dict):
            if all(key in node for key in keys):
                found.append(node)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(record)
    return found


# --------------------------------------------------------------------------- #
# LEDGER_FLOOR: derived, not counted, not read from the ledger
# --------------------------------------------------------------------------- #
def test_floor_is_half_the_inventory_floors(tmp_path):
    _build(tmp_path)
    proc, record = _check(tmp_path)
    coverage = _coverage(record)
    assert coverage["floor"] == LEDGER_FLOOR == 39, (
        "LEDGER_FLOOR MUST be ⌊(27 + 51) / 2⌋ = 39 (C-1); got %r" % coverage.get("floor")
    )
    assert proc.returncode == 0


def test_floor_boundary_is_39_not_the_expected_row_count(tmp_path):
    full = _rows()
    _build(tmp_path, rows=full[:38])
    _proc, record = _check(tmp_path)
    assert _coverage(record)["ledger_rows"] == 38
    assert "ledger-truncated" in _kinds(record), "38 < 39 must truncate (C-1)"

    _build(tmp_path, rows=full[:39])
    _proc, record = _check(tmp_path)
    assert _coverage(record)["ledger_rows"] == 39
    assert "ledger-truncated" not in _kinds(record), (
        "39 == the floor must not truncate (C-1) — the floor is not 78"
    )

    _build(tmp_path, rows=full[:40])
    _proc, record = _check(tmp_path)
    assert _coverage(record)["ledger_rows"] == 40
    assert "ledger-truncated" not in _kinds(record)


def test_floor_does_not_move_with_the_inspected_ledger(tmp_path):
    rows = _rows()
    inflated = rows + [
        {
            "unit_id": "skill:ghost-%02d" % n,
            "flow_class": EXECUTION,
            "basis": "behavior-oracle",
            "neutral": "",
            "notes": "",
        }
        for n in range(22)
    ]
    _build(tmp_path, rows=inflated)
    _proc, record = _check(tmp_path)
    coverage = _coverage(record)
    assert coverage["ledger_rows"] == 100
    assert coverage["floor"] == 39, (
        "a 100-row ledger MUST NOT move the floor — it is inventory-derived (C-1); "
        "got %r" % coverage.get("floor")
    )
    assert "ledger-truncated" not in _kinds(record)


# --------------------------------------------------------------------------- #
# coverage arithmetic and the clean relation
# --------------------------------------------------------------------------- #
def test_clean_requires_zero_findings_on_top_of_the_four_coverage_conditions(tmp_path):
    rows = _rows(26, 50)
    _build(tmp_path, commands=26, skills=50, rows=rows)
    proc, record = _check(tmp_path)
    coverage = _coverage(record)
    assert coverage["matched"] == coverage["inventory_units"] == 76
    assert coverage["gaps"] == 0
    assert coverage["parse_errors"] == 0
    assert coverage["ledger_rows"] >= coverage["floor"]
    assert record.get("findings"), "inventory-truncated must still be a finding"
    assert _red_kind(record) == "parse-failure", (
        "the four coverage conditions are necessary, not sufficient; an inventory-side "
        "defect outside the gap bucket is a parse failure (C-2 / C-3)"
    )
    assert proc.returncode == 1


def test_gaps_and_parse_errors_are_independent_sums(tmp_path):
    rows = _rows()
    # One valid row removed (missing) + one unknown row + one malformed row.
    injected_rows = rows[1:] + [
        {
            "unit_id": "skill:ghost",
            "flow_class": EXECUTION,
            "basis": "behavior-oracle",
            "neutral": "",
            "notes": "",
        }
    ]
    owner_text = _render_owner(
        injected_rows,
        extra=("| not-a-unit-id | execution |",),
    )
    _build(tmp_path, owner_text=owner_text)
    _proc, record = _check(tmp_path)
    kinds = _kinds(record)
    coverage = _coverage(record)
    assert kinds.count("missing") == 1
    assert kinds.count("unknown") == 1
    assert kinds.count("row-malformed") == 1
    assert coverage["gaps"] == 2 == kinds.count("missing") + kinds.count("unknown")
    assert coverage["parse_errors"] == 1 == kinds.count("row-malformed") + kinds.count(
        "ledger-truncated"
    )
    assert coverage["ledger_rows"] == 78
    assert coverage["matched"] == 77


# --------------------------------------------------------------------------- #
# red_kind priority ladder, one fixture per rung
# --------------------------------------------------------------------------- #
def test_priority_owner_unavailable_outranks_framework_source_required(tmp_path):
    payload = tmp_path / "payload"
    (payload / ".specify").mkdir(parents=True)
    proc, record = _check(payload)
    assert proc.returncode == 2
    assert _red_kind(record) == "owner-unavailable"
    assert record.get("findings") == []


def test_priority_framework_source_required_outranks_parse_failure(tmp_path):
    payload = tmp_path / "payload"
    _write(
        payload / ".specify" / OWNER_REL,
        _render_owner(_rows(2, 2)),
    )
    proc, record = _check(payload)
    assert proc.returncode == 2
    assert _red_kind(record) == "framework-source-required", (
        "a parseable owner on a payload root is still framework-source-required, "
        "not a gap / parse failure (C-3 / C-14)"
    )
    assert record.get("findings") == []


def test_priority_parse_failure_outranks_gap(tmp_path):
    rows = _rows()
    owner_text = _render_owner(rows[:-1], extra=("| not-a-unit-id | execution |",))
    _build(tmp_path, owner_text=owner_text)
    _proc, record = _check(tmp_path)
    kinds = _kinds(record)
    assert "missing" in kinds and "row-malformed" in kinds
    assert _red_kind(record) == "parse-failure", (
        "parse-failure outranks gap (C-3); kinds=%r" % kinds
    )


def test_priority_gap_outranks_clean(tmp_path):
    rows = _rows()
    _build(tmp_path, rows=rows[:-1])
    _proc, record = _check(tmp_path)
    assert _red_kind(record) == "gap"


def test_priority_clean_is_zero_findings(tmp_path):
    _build(tmp_path)
    proc, record = _check(tmp_path)
    assert record.get("findings") == []
    assert _red_kind(record) == "clean"
    assert proc.returncode == 0


def test_every_observed_kind_falls_into_one_bucket(tmp_path):
    gap_bucket = {
        "missing",
        "unknown",
        "duplicate",
        "dual-class",
        "invalid-class",
        "neutral-unlisted",
        "mixed-oracle-class",
        "ledger-version-missing",
    }
    rows = _rows()
    fixtures = {
        "missing": (_render_owner(rows[:-1]), "gap"),
        "unknown": (
            _render_owner(
                rows
                + [
                    {
                        "unit_id": "skill:ghost",
                        "flow_class": EXECUTION,
                        "basis": "behavior-oracle",
                        "neutral": "",
                        "notes": "",
                    }
                ]
            ),
            "gap",
        ),
        "row-malformed": (
            _render_owner(rows, extra=("| not-a-unit-id | execution |",)),
            "parse-failure",
        ),
        "ledger-truncated": (_render_owner(rows[:10]), "parse-failure"),
        "ledger-version-missing": (_render_owner(rows, version=None), "gap"),
        "inventory-truncated": (None, "parse-failure"),
    }
    for label, (owner_text, expected) in fixtures.items():
        root = tmp_path / label
        kwargs = {"owner_text": owner_text} if owner_text is not None else {}
        if label == "inventory-truncated":
            _build(root, commands=26, skills=50)
        else:
            _build(root, **kwargs)
        _proc, record = _check(root)
        kinds = set(_kinds(record))
        assert kinds, "fixture %r produced no findings" % label
        outside = kinds - (gap_bucket | {"row-malformed", "ledger-truncated", "inventory-truncated"})
        assert not outside, "fixture %r produced unclassified kinds %r" % (label, outside)
        assert _red_kind(record) == expected, (
            "fixture %r must be %r; kinds=%r" % (label, expected, sorted(kinds))
        )


# --------------------------------------------------------------------------- #
# delegation grammar and de-duplication
# --------------------------------------------------------------------------- #
def _delegation_fixture(root: Path, lines: list[str], *, skill_names=("alpha",)):
    _write(root / COMMANDS_REL / "demo.md", "# /speckit.demo\n\n" + "\n".join(lines) + "\n")
    rows = [
        {
            "unit_id": "/speckit.demo",
            "flow_class": EXECUTION,
            "basis": "behavior-oracle",
            "neutral": "",
            "notes": "",
        }
    ]
    for name in skill_names:
        _write(
            root / "skills" / "internal" / name / "SKILL.md",
            "---\nname: %s\ndescription: fixture\n---\n" % name,
        )
        rows.append(
            {
                "unit_id": "skill:%s" % name,
                "flow_class": EXECUTION,
                "basis": "behavior-oracle",
                "neutral": "",
                "notes": "",
            }
        )
    _write(root / OWNER_REL, _render_owner(rows))


def _delegation(root: Path):
    proc = _run("--action", "delegation", "--repo", str(root), "--format", "json")
    record = _json(proc) if proc.stdout.strip() else None
    return proc, record


def test_grammar_accepts_prefix_and_layer_variants(tmp_path):
    lines = [
        "a `skills/alpha/SKILL.md`",
        "b `.specify/skills/alpha/SKILL.md`",
        "c `skills/external/alpha/SKILL.md`",
        "d `skills/internal/alpha/SKILL.md`",
    ]
    _delegation_fixture(tmp_path, lines)
    proc, record = _delegation(tmp_path)
    assert proc.returncode == 0, "all four spellings name the same skill; stderr=%r" % proc.stderr
    edges = _edge_records(record)
    assert len(edges) == 1, (
        "one template + one skill name = one edge after de-duplication (C-8); got %r"
        % edges
    )
    assert edges[0]["skill"] == "skill:alpha"


def test_grammar_rejects_placeholder_and_non_canonical_names(tmp_path):
    lines = [
        "placeholder `skills/<name>/SKILL.md`",
        "placeholder `.specify/skills/<name>/SKILL.md`",
        "uppercase `skills/Alpha/SKILL.md`",
        "underscore `skills/al_pha/SKILL.md`",
        "space `skills/al pha/SKILL.md`",
    ]
    _delegation_fixture(tmp_path, lines, skill_names=("alpha",))
    proc, record = _delegation(tmp_path)
    assert proc.returncode == 0, (
        "non-canonical names are not edges and not findings (C-8); findings=%r"
        % (None if record is None else record.get("findings"))
    )
    assert record is not None
    assert _edge_records(record) == []
    assert record.get("findings") == []


def test_same_skill_twice_is_one_edge(tmp_path):
    lines = [
        "first `skills/internal/alpha/SKILL.md`",
        "second `.specify/skills/internal/alpha/SKILL.md`",
    ]
    _delegation_fixture(tmp_path, lines)
    _proc, record = _delegation(tmp_path)
    assert len(_edge_records(record)) == 1, (
        "same-template same-skill MUST de-duplicate (C-8); got %r"
        % _edge_records(record)
    )


# --------------------------------------------------------------------------- #
# owner_pointer grammar
# --------------------------------------------------------------------------- #
def _faces_fixture(root: Path, pointer_cell: str):
    rows = [
        ("需求清晰度", "requirements-clarity", pointer_cell),
        ("读者/目的/边界", "reader-purpose", "`shared/guidelines/b.md` § Section B"),
        ("证据分级与 as-of", "evidence-asof", "`shared/guidelines/b.md` § Section B"),
        ("结构/链接/构建", "structure-links-build", "`shared/guidelines/b.md`"),
        ("事实一致性", "fact-consistency", "`shared/guidelines/b.md`"),
        ("评审", "review", "`shared/guidelines/b.md`"),
    ]
    lines = [
        "# Expression Gates (069b unit fixture)",
        "",
        "## 六面（封闭集）",
        "",
        "| 面（中文） | face id | owner_pointer |",
        "| --- | --- | --- |",
    ]
    for label, face_id, pointer in rows:
        lines.append("| %s | %s | %s |" % (label, face_id, pointer))
    lines.append("")
    _write(root / GATES_REL, "\n".join(lines))
    _write(root / COMMANDS_REL / "docs.md", "# /speckit.docs\n")
    _write(root / "shared" / "guidelines" / "a.md", "# A\n\n## Section A\n")
    _write(root / "shared" / "guidelines" / "b.md", "# B\n\n## Section B\n")


def _faces(root: Path):
    proc = _run("--action", "faces", "--repo", str(root), "--format", "json")
    record = _json(proc) if proc.stdout.strip() else None
    return proc, record


def test_plus_joined_pointer_is_one_binding(tmp_path):
    _faces_fixture(
        tmp_path,
        "`shared/guidelines/a.md` § Section A + `shared/guidelines/b.md` § Section B",
    )
    proc, record = _faces(tmp_path)
    assert proc.returncode == 0, (
        "a `+`-joined cell is one binding, not a second pointer (C-11); findings=%r"
        % (None if record is None else record.get("findings"))
    )
    assert record is not None
    assert record.get("faces") == 6
    assert record.get("findings") == []


def test_anchor_must_match_a_heading_text(tmp_path):
    _faces_fixture(tmp_path, "`shared/guidelines/a.md` § Section A")
    proc, record = _faces(tmp_path)
    assert proc.returncode == 0, "a matching anchor must stay green; findings=%r" % (
        None if record is None else record.get("findings")
    )

    _faces_fixture(tmp_path, "`shared/guidelines/a.md` § Section B")
    proc, record = _faces(tmp_path)
    assert proc.returncode == 1, "a mismatched anchor must turn red (C-11)"
    assert record is not None
    kinds = _kinds(record)
    assert "faces-unresolvable" in kinds, (
        "a mismatched anchor is `faces-unresolvable` (C-11); got %r" % kinds
    )


def test_plus_joined_pointer_with_one_missing_path_is_unresolvable(tmp_path):
    _faces_fixture(
        tmp_path,
        "`shared/guidelines/a.md` + `shared/guidelines/missing.md`",
    )
    proc, record = _faces(tmp_path)
    assert proc.returncode == 1
    assert record is not None
    assert "faces-unresolvable" in _kinds(record)
