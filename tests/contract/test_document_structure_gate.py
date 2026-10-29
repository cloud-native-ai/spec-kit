"""Contract tests for ``doc-consistency-check.py --action structure`` (077, T013).

Both legs of ``.specify/specs/077-doc-sdd-integration/contracts/document-structure.md``
are written here in one pass (C-001 … C-016); the following task rows only turn
parts of them green:

* **CLI contract** — ``--action structure`` exists (``--action`` choices widened
  from ``("verify",)`` to ``("verify", "structure")``), the subject is the
  ``plan.md`` under ``--spec-dir``, and ``--faces`` / ``parse_faces`` are
  untouched (still four faces — no seventh gate face).
* **Four subsections + four code families** — the four ``###`` literals are held
  by the checker as constants (code-first owner) and the test reads them from
  there instead of copying them; the finding code set is exactly the four
  families of ``data-model.md`` E6.
* **Whole-chapter-missing precedence** — one root cause yields one code: the
  absent chapter reports ``document-structure-missing`` and suppresses the four
  ``subsection-missing`` it would otherwise imply.
* **Two-way comparison only with ``--path``** — without ``--path`` the run is
  plan-side only and says ``two-way: not-run`` (never readable as "two-way
  passed"); ``chapter-missing`` / ``chapter-unexpected`` can only appear when a
  delivered document is named.
* **SC-004's second delivered-document fixture** — structure / links / build add
  no violation while the evidence face fails on one assertion missing ``source``:
  the same action, the same delivered document, and the gate still fails
  ("structure green, content red").
* **Baseline** — ``当前违规集 ⊆ 基线集`` judged on ``file + code + section``
  triples; a missing baseline file reads as the empty set; ``--freeze`` prints
  and never writes.
* **Degradation and author errors** — an unparsable owner is
  ``not-applicable`` with the ``owner-unavailable`` label (never "0 violations
  passed"); an exit-1 declaration error stops the gate (FR-005).

Fixtures live in ``tmp_path`` and mirror the real layout
(``<repo>/.specify/specs/<name>/``), because the class is resolved through the
same ``flow-class-check.py --action lookup --unit-id "spec:<name>"`` entry the
stage commands use — a fixture outside that layout would resolve no line at all.

Red-first (Constitution IV): today ``--action structure`` is rejected by
argparse with ``invalid choice`` and exit 2, so every assertion below is the
intended pre-implementation red.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "python" / "doc-consistency-check.py"
PLAN_TEMPLATE = REPO_ROOT / "templates" / "plan-template.md"
REQUIREMENTS = (
    REPO_ROOT / ".specify" / "specs" / "077-doc-sdd-integration" / "requirements.md"
)

SPEC_NAME = "777-fixture-line"

OWNER_TEXT = """# Flow Class Definitions (fixture)

本文件是 077 契约测试的临时夹具，不是仓库所有者。

## 逐流程台账

**台账版本**: 1（2026-10-30）

| unit_id | flow_class | basis | neutral |
|---------|------------|-------|---------|
| /speckit.implement | execution | mixed-oracle | |
"""

DECLARED_EXPRESSION = (
    "# Requirements: fixture\n\n"
    "**Flow Class**: expression\n\n"
    "## Related Feature *(mandatory)*\n\n"
    "**Feature ID**: 777\n"
)
DECLARED_EXECUTION = DECLARED_EXPRESSION.replace("expression", "execution")
UNDECLARED = (
    "# Requirements: fixture\n\n"
    "## Related Feature *(mandatory)*\n\n"
    "**Feature ID**: 777\n"
)
DECLARED_INVALID = DECLARED_EXPRESSION.replace("expression", "expressive")

CHAPTER_TREE_ROWS = (
    "| 概览 | — | 读者读完决定是否继续读第二节 | 本节不覆盖实现细节 |\n"
    "| 实现 | 概览 | 读者读完决定本次改动点 | 本节不覆盖运维 |\n"
)
EVIDENCE_ROWS = (
    "| 引擎存在 | 实测 | 2026-10-30 | `python3 scripts/python/flow-class-check.py --action check` |\n"
)
OWNER_ROWS = "| 引擎存在 | `docs/fact-owner.md` | § 概览 |\n"
READER_LINES = (
    "**Readers**: 迁移评审者，需要在合并前判断这份文档是否可用。\n"
    "**Reading scenario**: 合并前核对章节结构与事实标注。\n"
)

DELIVERED_OK = """# Delivered

**Readers**: 迁移评审者，需要在合并前判断这份文档是否可用。
**Reading scenario**: 合并前核对章节结构与事实标注。

## 概览

引擎存在（证据：实测，as-of 2026-10-30，source: `python3 scripts/python/flow-class-check.py --action check`）。

## 实现

改动点落在既有文件的扩展点上，不新增门禁面。
"""


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _load_checker():
    assert CHECKER.is_file(), "structure checker missing: %s" % CHECKER
    spec = importlib.util.spec_from_file_location("_doc_consistency_under_test", CHECKER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_plan(*, chapter_tree=CHAPTER_TREE_ROWS, reader=READER_LINES,
               evidence=EVIDENCE_ROWS, owners=OWNER_ROWS, heading=True,
               omit=(), extra=""):
    """Assemble a ``plan.md``; ``omit`` drops a whole subsection by its key."""
    parts = ["# Plan: fixture\n\n", "## Summary\n\nfixture plan.\n\n"]
    if heading:
        parts.append("## Document Structure\n\n")
        if "chapter_tree" not in omit:
            parts.append("### Chapter Tree\n\n")
            parts.append("| 节名 | 父节 | 目的 | 边界 |\n")
            parts.append("| --- | --- | --- | --- |\n")
            parts.append(chapter_tree)
            parts.append("\n")
        if "reader" not in omit:
            parts.append("### Reader Baseline\n\n")
            parts.append(reader)
            parts.append("\n")
        if "evidence" not in omit:
            parts.append("### Evidence List\n\n")
            parts.append("| 断言 | 证据等级 | as-of | source |\n")
            parts.append("| --- | --- | --- | --- |\n")
            parts.append(evidence)
            parts.append("\n")
        if "owners" not in omit:
            parts.append("### Fact Owners\n\n")
            parts.append("| 事实 | owner 路径 | 章节锚 |\n")
            parts.append("| --- | --- | --- |\n")
            parts.append(owners)
            parts.append("\n")
        parts.append(extra)
    return "".join(parts)


def make_repo(tmp_path, *, requirements=DECLARED_EXPRESSION, plan=None,
              with_owner=True, delivered=None, owner_files=("docs/fact-owner.md",)):
    """A fixture repo laid out like the real one (``.specify/specs/<name>/``)."""
    repo = tmp_path / "repo"
    spec_dir = repo / ".specify" / "specs" / SPEC_NAME
    _write(spec_dir / "requirements.md", requirements)
    _write(spec_dir / "plan.md", build_plan() if plan is None else plan)
    if with_owner:
        _write(repo / "shared" / "definitions" / "flow-class-definitions.md", OWNER_TEXT)
    for rel in owner_files:
        _write(repo / rel, "# owner fixture\n")
    if delivered is not None:
        _write(spec_dir / "delivered.md", delivered)
    return repo, spec_dir


def _run(*args):
    assert CHECKER.is_file(), "structure checker missing: %s" % CHECKER
    return subprocess.run(
        [sys.executable, str(CHECKER), *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )


def run_structure(spec_dir, *extra, fmt="json"):
    return _run("--action", "structure", "--spec-dir", str(spec_dir), "--format", fmt, *extra)


def payload_of(proc):
    assert proc.stdout.strip(), (
        "expected a JSON payload on stdout; stderr=%r" % proc.stderr
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            "stdout is not JSON (%s); head=%r; stderr=%r"
            % (exc, proc.stdout[:400], proc.stderr[:400])
        ) from exc


def rules_of(payload):
    return [item["rule"] for item in payload["findings"]]


# --------------------------------------------------------------------------- #
# CLI contract
# --------------------------------------------------------------------------- #
def test_structure_action_exists_and_needs_a_spec_dir(tmp_path):
    _repo, spec_dir = make_repo(tmp_path)
    proc = run_structure(spec_dir)
    assert proc.returncode in (0, 1), (
        "`--action structure` must be an accepted action; exit=%d stderr=%r"
        % (proc.returncode, proc.stderr)
    )
    assert payload_of(proc)["action"] == "structure"

    missing = _run("--action", "structure", "--format", "json")
    assert missing.returncode == 2, (
        "structure needs --spec-dir; a scope-less run must be an input error, got %d"
        % missing.returncode
    )


def test_default_run_is_plan_side_only_and_says_two_way_not_run(tmp_path):
    _repo, spec_dir = make_repo(tmp_path)
    proc = run_structure(spec_dir, fmt="text")
    assert proc.returncode in (0, 1), proc.stderr
    assert "two-way: not-run" in proc.stdout, (
        "without --path the run is plan-side only and MUST say so — it must never "
        "read as 'two-way passed'; stdout=%r" % proc.stdout
    )


def test_faces_and_parse_faces_are_unchanged():
    module = _load_checker()
    assert tuple(module.FACES) == ("reader", "evidence", "duplicate", "count"), (
        "this feature adds an action, not a fifth/sixth/seventh face; FACES=%r"
        % (module.FACES,)
    )
    assert module.parse_faces("reader") == ["reader"]
    assert module.parse_faces("") == list(module.FACES)
    try:
        module.parse_faces("structure")
    except Exception as exc:  # InputError, by whatever name the module uses
        assert "structure" in str(exc), (
            "`structure` is an action, not a face; the rejection must name it: %r" % exc
        )
    else:  # pragma: no cover — the branch above must fire
        raise AssertionError("parse_faces accepted `structure` as a face")


def test_the_cli_rejects_structure_as_a_face(tmp_path):
    _repo, spec_dir = make_repo(tmp_path)
    control = _run("--action", "structure", "--spec-dir", str(spec_dir), "--faces", "reader")
    assert control.returncode in (0, 1), (
        "control: the same action with a registered face must run, so the rejection "
        "below is about the value and not about the action; exit=%d stderr=%r"
        % (control.returncode, control.stderr)
    )
    proc = _run("--action", "structure", "--spec-dir", str(spec_dir), "--faces", "structure")
    assert proc.returncode == 2, (
        "--faces must keep the four-face value set; `structure` is not a face"
    )


# --------------------------------------------------------------------------- #
# Constants: subsections and column names are the checker's (code-first owner)
# --------------------------------------------------------------------------- #
def test_subsections_and_columns_are_checker_constants():
    module = _load_checker()
    subsections = tuple(module.STRUCTURE_SUBSECTIONS)
    assert subsections == (
        "### Chapter Tree",
        "### Reader Baseline",
        "### Evidence List",
        "### Fact Owners",
    ), "the four subsection literals must be the registered ones, got %r" % (subsections,)
    assert tuple(module.CHAPTER_TREE_COLUMNS) == ("节名", "父节", "目的", "边界")
    assert tuple(module.EVIDENCE_LIST_COLUMNS) == ("断言", "证据等级", "as-of", "source")
    assert tuple(module.FACT_OWNERS_COLUMNS) == ("事实", "owner 路径", "章节锚")
    assert module.STRUCTURE_HEADING == "## Document Structure"


def test_the_code_set_is_exactly_the_four_families():
    module = _load_checker()
    families = module.STRUCTURE_CODE_FAMILIES
    assert set(families) == {"structure-syntax", "two-way", "evidence", "owner"}, (
        "the finding code set is four families — no fifth; got %r" % sorted(families)
    )
    syntax = set(families["structure-syntax"])
    assert {"document-structure-missing", "subsection-missing", "parent-unknown",
            "chapter-duplicate", "chapter-purpose-missing",
            "chapter-boundary-missing"} <= syntax, syntax
    assert set(families["two-way"]) == {"chapter-missing", "chapter-unexpected"}
    evidence = set(families["evidence"])
    assert {"evidence-unlisted", "grade-invalid", "as-of-malformed", "source-missing",
            "grade-asof-unpaired"} <= evidence, evidence
    owner = set(families["owner"])
    assert {"owner-duplicate", "owner-path-missing", "owner-anchor-missing"} <= owner, owner


# --------------------------------------------------------------------------- #
# Happy path
# --------------------------------------------------------------------------- #
def test_expression_line_with_a_complete_plan_passes(tmp_path):
    _repo, spec_dir = make_repo(tmp_path)
    proc = run_structure(spec_dir)
    assert proc.returncode == 0, "a complete structure must pass; stderr=%r" % proc.stderr
    payload = payload_of(proc)
    assert payload["status"] == "ok", payload
    assert payload["findings"] == [], payload["findings"]
    assert payload["class"] == "expression" and payload["source"] == "declaration"
    assert payload["scope"]["files_scanned"] >= 1


# --------------------------------------------------------------------------- #
# Structure syntax: missing chapter / subsection precedence
# --------------------------------------------------------------------------- #
def test_whole_chapter_missing_reports_one_code_and_suppresses_subsection_codes(tmp_path):
    _repo, spec_dir = make_repo(tmp_path, plan=build_plan(heading=False))
    proc = run_structure(spec_dir)
    assert proc.returncode == 1, "a missing `## Document Structure` must fail the gate"
    rules = rules_of(payload_of(proc))
    assert rules == ["document-structure-missing"], (
        "one root cause, one code: the missing chapter MUST suppress the four "
        "`subsection-missing` it implies; got %r" % rules
    )


def test_missing_chapter_tree_reports_subsection_missing(tmp_path):
    _repo, spec_dir = make_repo(tmp_path, plan=build_plan(omit=("chapter_tree",)))
    proc = run_structure(spec_dir)
    assert proc.returncode == 1
    findings = payload_of(proc)["findings"]
    tree = [item for item in findings if item["rule"] == "subsection-missing"]
    assert tree and tree[0]["section"] == "### Chapter Tree", (
        "the missing subsection must be named by its registered literal; got %r"
        % findings
    )


def test_missing_reader_lines_report_subsection_missing(tmp_path):
    _repo, spec_dir = make_repo(tmp_path, plan=build_plan(reader=""))
    proc = run_structure(spec_dir)
    assert proc.returncode == 1, (
        "a Reader Baseline subsection without the two marker lines must go red"
    )
    findings = payload_of(proc)["findings"]
    assert [item["rule"] for item in findings] == ["subsection-missing"], findings
    assert findings[0]["section"] == "### Reader Baseline", findings


def test_chapter_tree_syntax_codes(tmp_path):
    cases = {
        "parent-unknown": ("| 概览 | — | 决定是否继续 | 不覆盖细节 |\n"
                           "| 实现 | 不存在的节 | 决定改动点 | 不覆盖运维 |\n"),
        "chapter-duplicate": ("| 概览 | — | 决定是否继续 | 不覆盖细节 |\n"
                              "| 概览 | — | 决定改动点 | 不覆盖运维 |\n"),
        "chapter-purpose-missing": ("| 概览 | — |  | 不覆盖细节 |\n"),
        "chapter-boundary-missing": ("| 概览 | — | 决定是否继续 |  |\n"),
    }
    for rule, rows in cases.items():
        case_dir = tmp_path / rule
        _repo, spec_dir = make_repo(case_dir, plan=build_plan(chapter_tree=rows))
        proc = run_structure(spec_dir)
        assert proc.returncode == 1, "%s must fail the gate" % rule
        assert rule in rules_of(payload_of(proc)), (
            "expected %r from chapter-tree rows %r, got %r"
            % (rule, rows, rules_of(payload_of(proc)))
        )


# --------------------------------------------------------------------------- #
# Evidence face: the four reused codes + evidence-unlisted
# --------------------------------------------------------------------------- #
def test_evidence_codes_are_reused_not_reinvented(tmp_path):
    cases = {
        "grade-invalid": "| 引擎存在 | 也许 | 2026-10-30 | source-x |\n",
        "as-of-malformed": "| 引擎存在 | 实测 | 2026/10/30 | source-x |\n",
        "source-missing": "| 引擎存在 | 实测 | 2026-10-30 |  |\n",
        "grade-asof-unpaired": "| 引擎存在 | 实测 |  | source-x |\n",
    }
    for rule, rows in cases.items():
        case_dir = tmp_path / rule
        _repo, spec_dir = make_repo(case_dir, plan=build_plan(evidence=rows))
        proc = run_structure(spec_dir)
        assert proc.returncode == 1, "%s must fail the gate" % rule
        assert rule in rules_of(payload_of(proc)), (
            "expected %r, got %r" % (rule, rules_of(payload_of(proc)))
        )


def test_evidence_unlisted_requires_a_delivered_document(tmp_path):
    doc = DELIVERED_OK + (
        "\n## 附录\n\n另一条断言（证据：实测，as-of 2026-10-30，source: 未登记）。\n"
    )
    _repo, spec_dir = make_repo(tmp_path, delivered=doc)
    proc = run_structure(spec_dir, "--path", str(spec_dir / "delivered.md"))
    assert proc.returncode == 1
    assert "evidence-unlisted" in rules_of(payload_of(proc)), rules_of(payload_of(proc))

    plan_only = run_structure(spec_dir)
    assert "evidence-unlisted" not in rules_of(payload_of(plan_only)), (
        "an unlisted assertion is a delivered-document property; the plan-side run "
        "must not claim it"
    )


# --------------------------------------------------------------------------- #
# Owner face
# --------------------------------------------------------------------------- #
def test_owner_codes(tmp_path):
    cases = {
        "owner-duplicate": ("| 引擎存在 | `docs/fact-owner.md` | § 概览 |\n"
                            "| 引擎存在 | `docs/other-owner.md` | § 实现 |\n"),
        "owner-path-missing": "| 引擎存在 | `docs/not-there.md` | § 概览 |\n",
        "owner-anchor-missing": "| 引擎存在 | `docs/fact-owner.md` |  |\n",
    }
    for rule, rows in cases.items():
        case_dir = tmp_path / rule
        _repo, spec_dir = make_repo(case_dir, plan=build_plan(owners=rows))
        proc = run_structure(spec_dir)
        assert proc.returncode == 1, "%s must fail the gate" % rule
        assert rule in rules_of(payload_of(proc)), (
            "expected %r, got %r" % (rule, rules_of(payload_of(proc)))
        )


def test_verbatim_hand_copy_uses_the_existing_duplicate_floor(tmp_path):
    copied = "这一行在计划与落文里逐字重复，长度远超机械下限，必须被既有阈值判出。"
    plan = build_plan(extra="\n" + copied + "\n")
    doc = DELIVERED_OK + "\n" + copied + "\n"
    _repo, spec_dir = make_repo(tmp_path, plan=plan, delivered=doc)
    proc = run_structure(spec_dir, "--path", str(spec_dir / "delivered.md"))
    assert proc.returncode == 1
    assert "duplicate-fact" in rules_of(payload_of(proc)), (
        "a verbatim hand copy above the existing floor must be reported with the "
        "existing code; got %r" % rules_of(payload_of(proc))
    )


# --------------------------------------------------------------------------- #
# Two-way comparison
# --------------------------------------------------------------------------- #
def test_delivered_document_chapter_codes(tmp_path):
    unexpected = DELIVERED_OK + "\n## 附录\n\n计划外的顶层章节。\n"
    _repo, spec_dir = make_repo(tmp_path / "unexpected", delivered=unexpected)
    proc = run_structure(spec_dir, "--path", str(spec_dir / "delivered.md"))
    assert proc.returncode == 1
    payload = payload_of(proc)
    assert "chapter-unexpected" in rules_of(payload), rules_of(payload)
    assert "chapter-missing" not in rules_of(payload), rules_of(payload)

    missing = DELIVERED_OK.split("## 实现")[0]
    _repo, spec_dir = make_repo(tmp_path / "missing", delivered=missing)
    proc = run_structure(spec_dir, "--path", str(spec_dir / "delivered.md"))
    assert proc.returncode == 1
    payload = payload_of(proc)
    assert "chapter-missing" in rules_of(payload), rules_of(payload)
    assert "chapter-unexpected" not in rules_of(payload), rules_of(payload)


def test_a_non_top_level_extra_section_does_not_turn_red(tmp_path):
    doc = DELIVERED_OK.replace(
        "改动点落在既有文件的扩展点上，不新增门禁面。",
        "改动点落在既有文件的扩展点上。\n\n### 细节\n\n非顶层小节不因本条转红。",
    )
    _repo, spec_dir = make_repo(tmp_path, delivered=doc)
    proc = run_structure(spec_dir, "--path", str(spec_dir / "delivered.md"))
    assert proc.returncode == 0, (
        "an unexpected NON-top-level section must not turn the gate red; findings=%r"
        % payload_of(proc)["findings"]
    )


def test_structure_green_content_red_is_still_a_failure(tmp_path):
    """SC-004's second delivered-document fixture: structure green, content red."""
    plan = build_plan(evidence="| 引擎存在 | 实测 | 2026-10-30 |  |\n")
    _repo, spec_dir = make_repo(tmp_path, plan=plan, delivered=DELIVERED_OK)
    proc = run_structure(spec_dir, "--path", str(spec_dir / "delivered.md"))
    assert proc.returncode == 1, (
        "one assertion without `source` must fail the gate even when the chapter "
        "structure is clean — structure is necessary, never sufficient"
    )
    payload = payload_of(proc)
    rules = rules_of(payload)
    assert "source-missing" in rules, rules
    assert not {"chapter-missing", "chapter-unexpected"} & set(rules), (
        "the structural half must be clean in this fixture — otherwise the leg does "
        "not prove 'structure green, content red'; got %r" % rules
    )


# --------------------------------------------------------------------------- #
# Subject classes: execution / undeclared / degraded / author error
# --------------------------------------------------------------------------- #
def test_execution_class_is_not_applicable_and_never_a_pass(tmp_path):
    _repo, spec_dir = make_repo(tmp_path, requirements=DECLARED_EXECUTION)
    proc = run_structure(spec_dir, fmt="text")
    assert proc.returncode == 0, proc.stderr
    assert "status: not-applicable" in proc.stdout, proc.stdout
    assert "status: ok" not in proc.stdout, (
        "not-applicable must never be rendered as a pass; stdout=%r" % proc.stdout
    )
    assert "class=execution" in proc.stdout and "source=declaration" in proc.stdout
    assert "files_scanned: " in proc.stdout, (
        "the companion quantity (files checked) must be non-empty; stdout=%r" % proc.stdout
    )


def test_undeclared_class_is_not_applicable_and_carries_the_default_source(tmp_path):
    _repo, spec_dir = make_repo(tmp_path, requirements=UNDECLARED)
    proc = run_structure(spec_dir)
    assert proc.returncode == 0
    payload = payload_of(proc)
    assert payload["status"] == "not-applicable", payload
    assert payload["source"] == "default", payload
    assert payload["class"] == "execution", payload


def test_degraded_owner_is_not_applicable_with_the_visible_label(tmp_path):
    _repo, spec_dir = make_repo(tmp_path, with_owner=False)
    proc = run_structure(spec_dir)
    assert proc.returncode == 0, (
        "an absent owner degrades visibly, it does not fail the stage; stderr=%r"
        % proc.stderr
    )
    payload = payload_of(proc)
    assert payload["status"] == "not-applicable", payload
    assert payload["error"] and payload["error"]["label"] == "owner-unavailable", payload


def test_author_error_stops_the_gate(tmp_path):
    _repo, spec_dir = make_repo(tmp_path, requirements=DECLARED_INVALID)
    proc = run_structure(spec_dir)
    assert proc.returncode == 1, (
        "an out-of-set declaration must stop the gate (FR-005), got exit %d"
        % proc.returncode
    )
    payload = payload_of(proc)
    assert payload["status"] == "fail", payload
    assert payload["error"]["label"] == "invalid-class", payload


# --------------------------------------------------------------------------- #
# Baseline
# --------------------------------------------------------------------------- #
def test_baseline_subset_is_the_criterion(tmp_path):
    _repo, spec_dir = make_repo(
        tmp_path, plan=build_plan(owners="| 引擎存在 | `docs/not-there.md` |  |\n")
    )
    first = run_structure(spec_dir)
    assert first.returncode == 1
    triples = ["%s\t%s\t%s" % (item["path"], item["rule"], item["section"] or "-")
               for item in payload_of(first)["findings"]]
    assert triples, "fixture precondition: the run must produce findings"
    _write(spec_dir / "structure-baseline.txt", "\n".join(triples) + "\n")

    second = run_structure(spec_dir)
    assert second.returncode == 0, (
        "findings inside the frozen baseline are tolerated (当前违规集 ⊆ 基线集); "
        "got findings=%r" % payload_of(second)["findings"]
    )
    payload = payload_of(second)
    assert payload["baseline"]["new"] == 0, payload["baseline"]
    assert payload["status"] == "ok", payload


def test_a_missing_baseline_reads_as_the_empty_set(tmp_path):
    _repo, spec_dir = make_repo(tmp_path, plan=build_plan(owners="| 引擎存在 | `docs/not-there.md` | § |\n"))
    assert not (spec_dir / "structure-baseline.txt").exists()
    proc = run_structure(spec_dir)
    assert proc.returncode == 1, "no baseline file means no tolerance — an absolute judge"
    assert payload_of(proc)["baseline"]["entries"] == 0


def test_freeze_prints_and_never_writes(tmp_path):
    _repo, spec_dir = make_repo(tmp_path, plan=build_plan(owners="| 引擎存在 | `docs/not-there.md` | § |\n"))
    proc = run_structure(spec_dir, "--freeze")
    assert proc.returncode == 0, proc.stderr
    assert "\t" in proc.stdout, (
        "`--freeze` prints the triples (file, code, section); stdout=%r" % proc.stdout
    )
    assert not (spec_dir / "structure-baseline.txt").exists(), (
        "the checker never writes the baseline file itself"
    )


# --------------------------------------------------------------------------- #
# Determinism
# --------------------------------------------------------------------------- #
def test_same_plan_yields_the_same_violation_set(tmp_path):
    plan = build_plan(
        chapter_tree="| 概览 | — |  |  |\n| 概览 | — | 决定 |  |\n",
        evidence="| 引擎存在 | 也许 | 2026/10/30 |  |\n",
    )
    _repo, spec_dir = make_repo(tmp_path, plan=plan)
    first = payload_of(run_structure(spec_dir))
    second = payload_of(run_structure(spec_dir))
    assert first["findings"] == second["findings"], (
        "the same plan must yield the same violation set, in a stable order"
    )


# --------------------------------------------------------------------------- #
# Producer side — the plan template carries the skeleton (T028 / FR-013)
# --------------------------------------------------------------------------- #
# This leg is deliberately independent of the stage-wiring guard (T009) and of the
# runner legs above (T013): it reads `templates/plan-template.md` directly, takes the
# five literals from the feature's `requirements.md` § Shared Strings and the three
# column sets from the checker's constants, and never hand-copies either. Without it
# the producer side would only be covered by "someone else's green".
CLASS_CONDITION_SENTENCE = "表达类 MUST 产出该章节、执行类 MUST NOT 被要求产出"


def _shared_strings() -> dict:
    """``STR-NNN -> literal`` from the feature's requirements § Shared Strings table."""
    assert REQUIREMENTS.is_file(), "requirements owner missing: %s" % REQUIREMENTS
    text = REQUIREMENTS.read_text(encoding="utf-8")
    start = text.index("## Shared Strings")
    tail = text[start:]
    following = re.search(r"^## ", tail[3:], re.MULTILINE)
    block = tail[: following.start() + 3] if following else tail
    rows = re.findall(r"^\|\s*`(STR-\d{3})`\s*\|\s*\"([^\"]*)\"\s*\|", block, re.MULTILINE)
    assert rows, "the Shared Strings table yielded no `STR-NNN` rows"
    return dict(rows)


def _table_header_after(lines: list, heading: str) -> list:
    """The first markdown table's header cells under ``heading`` (stops at the next `## `)."""
    assert heading in lines, "plan template lacks %r" % heading
    start = lines.index(heading)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            break
        if lines[index].startswith("|"):
            return [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
    return []


def test_plan_template_carries_the_document_structure_skeleton():
    """The template is the producer of `## Document Structure` and the four subsections.

    Two owners meet here and are asserted to agree: the feature's requirements
    (the literal register) and the checker's constants (the code-first column owner).
    """
    facts = _shared_strings()
    for key in ("STR-002", "STR-003", "STR-004", "STR-005", "STR-006"):
        assert key in facts, "requirements § Shared Strings lost %s" % key

    module = _load_checker()
    # Register and code agree before either is compared with the template.
    assert facts["STR-002"] == module.STRUCTURE_HEADING, (
        "requirements and the checker disagree on the chapter heading: %r vs %r"
        % (facts["STR-002"], module.STRUCTURE_HEADING)
    )
    assert tuple(facts["STR-00%d" % i] for i in range(3, 7)) == tuple(
        module.STRUCTURE_SUBSECTIONS
    ), "requirements and the checker disagree on the four subsection literals"

    text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    lines = text.split("\n")

    heading = facts["STR-002"]
    assert heading in lines, (
        "plan template lacks %r — expression-class plans would have no reachable producer"
        % heading
    )
    assert text.count("\n" + heading + "\n") == 1, (
        "%r must appear exactly once in the template" % heading
    )

    subsections = [facts["STR-00%d" % i] for i in range(3, 7)]
    positions = []
    for literal in subsections:
        assert literal in lines, "plan template lacks the subsection %r" % literal
        assert text.count("\n" + literal + "\n") == 1, (
            "%r must appear exactly once in the template" % literal
        )
        positions.append(lines.index(literal))
    assert positions == sorted(positions), (
        "the four subsections must appear in the registered order %r, got %r"
        % (subsections, [lines[p] for p in positions])
    )
    assert positions[0] > lines.index(heading), "subsections must sit under the chapter"

    chapter_tree, reader_baseline, evidence_list, fact_owners = subsections
    assert _table_header_after(lines, chapter_tree) == list(module.CHAPTER_TREE_COLUMNS), (
        "the Chapter Tree table header must be the checker's CHAPTER_TREE_COLUMNS"
    )
    assert _table_header_after(lines, evidence_list) == list(module.EVIDENCE_LIST_COLUMNS), (
        "the Evidence List table header must be the checker's EVIDENCE_LIST_COLUMNS"
    )
    assert _table_header_after(lines, fact_owners) == list(module.FACT_OWNERS_COLUMNS), (
        "the Fact Owners table header must be the checker's FACT_OWNERS_COLUMNS"
    )

    start = lines.index(reader_baseline) + 1
    end = next(
        (i for i in range(start, len(lines)) if lines[i].startswith("### ") or lines[i].startswith("## ")),
        len(lines),
    )
    reader_block = "\n".join(lines[start:end])
    for marker in module.READER_BASELINE_MARKERS:
        assert reader_block.count(marker) == 1, (
            "the Reader Baseline subsection must carry %r exactly once (two lines, as the "
            "checker parses them); block=%r" % (marker, reader_block)
        )

    assert CLASS_CONDITION_SENTENCE in text, (
        "the template must state %r — without the second half an execution-class line would "
        "gain a new mandatory section (FR-011)" % CLASS_CONDITION_SENTENCE
    )
