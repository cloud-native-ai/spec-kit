"""Contract tests for the driver-side class branch (077, T016).

Owns ``.specify/specs/077-doc-sdd-integration/contracts/driver-integration.md``
C-001 … C-010 — the only contract file this feature writes into the driver
skill. The stage sequence, sentinels, watcher verdicts, stall handling and the
fast-lane rule are owned elsewhere and are asserted here only as **unchanged**.

What this file pins, and why each assertion is decidable from the text alone:

* **C-001 / C-002 — the dispatch payload quartet.** Every stage dispatch must
  carry ``flow_class=`` / ``source=`` / ``marker=`` / ``error=`` in segment ①,
  identically for the local native subagent and the remote CLI (the prompt is
  the only carrier). A missing key is a *dispatch construction defect* and U4
  does not pass; the subagent may not infer, default or guess the class.
* **C-004 / C-005 — U4's four additional blocking checks.** The denominator is
  the gate owner's operator table (implement registers exactly one blocking
  row, ``G-implement-structure``); the four CLI faces are never counted as
  operators; the site build check rides that operator as a ``face=build``
  sub-row; the evidence file is judged ``exists and non-empty`` with **no** hash
  comparison; the payload class must equal the on-the-spot parse; a payload
  whose ``error`` slot is not ``-`` takes the ``owner-unavailable`` branch; the
  ``stage-status`` row must be present. Sentinel plus artifact without gate
  evidence is *incomplete*.
* **C-006 / C-007 / C-008 — the two slots swap their content, not their
  skeleton.** Two slots, same points (implement start / after review), same
  order, same closure name-level diff, same audit judgement; only the content
  becomes ``selection_basis=docs-gate-full`` with the docs-gate command string,
  an aggregated exit code, operator-level ``passed``/``failed`` and a
  name-level ``baseline_compare``. ``not-applicable`` appears only on the
  ``build`` sub-row and is listed separately — no cross-level equation.
* **C-009 / C-010 — the class branch moves exactly two things.** The skill's
  ``## Hard Requirements`` states the branch and points at both references,
  and states that the stage sequence, sentinel literals, watcher verdicts and
  exit codes, stall handling, fast-lane criteria and the analyze/review call
  rate (100%) do not move.

Red-first (Constitution IV): today the driver skill and its references carry
**zero** hits for ``flow_class|flow-class`` (the red-first token set is
deliberately narrowed to that pair — ``expression`` alone would match an
unrelated ``integer expression expected`` in ``references/watch-model.md`` and
produce a false positive). Every class-branch assertion below is therefore the
intended pre-implementation red, while the "unchanged" legs are regression
guards that must stay green both before and after.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
SKILL_MD = SKILL_DIR / "SKILL.md"
STAGE_PROMPTS = SKILL_DIR / "references" / "stage-prompts.md"
EFFICIENCY = SKILL_DIR / "references" / "efficiency-model.md"

# E9 — the dispatch payload is a key=value list, so each key is matched with
# its `=`; `flow_class` without `=` is not a payload key.
QUARTET_KEYS = ("flow_class=", "source=", "marker=", "error=")

# The class branch may live only in these three files: FR-023's closed wiring
# surface names the driver skill and its references, and the three-file split is
# the one T017/T019/T020 assigns (skeleton / slots / hard requirements). Each
# file is judged by its own marker — the slot owner names the new
# `selection_basis` value instead of restating the class key.
CLASS_BRANCH_MARKERS = {
    SKILL_MD: ("flow_class",),
    STAGE_PROMPTS: ("flow_class",),
    EFFICIENCY: ("docs-gate-full",),
}
CLASS_BRANCH_FILES = tuple(CLASS_BRANCH_MARKERS)

# FR-019(a): implement registers exactly one blocking operator row.
IMPLEMENT_OPERATOR = "G-implement-structure"
OPERATOR_ID_RE = re.compile(r"\bG-[a-z][a-z0-9-]+")
CLASS_TOKEN_RE = re.compile(r"flow_class|flow-class")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _read(path: Path) -> str:
    assert path.is_file(), "driver file missing: %s" % path.relative_to(REPO_ROOT)
    return path.read_text(encoding="utf-8")


def _section(text: str, heading_prefix: str) -> str:
    """Return one section: from the heading line to the next same-or-higher one."""
    lines = text.split("\n")
    starts = [i for i, line in enumerate(lines) if line.startswith(heading_prefix)]
    assert len(starts) == 1, (
        "expected exactly one heading starting %r, found %d"
        % (heading_prefix, len(starts))
    )
    start = starts[0]
    level = len(heading_prefix) - len(heading_prefix.lstrip("#"))
    stop = re.compile(r"^#{1,%d} " % level)
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if stop.match(lines[index]):
            end = index
            break
    return "\n".join(lines[start:end])


def _blocks(text: str) -> list[str]:
    """Paragraphs: blank-line separated blocks (table rows stay inside one)."""
    return [block for block in re.split(r"\n\s*\n", text) if block.strip()]


def _mentions(text: str, tokens: tuple[str, ...], context: str) -> str:
    """Assert some paragraph carries every token; return that paragraph."""
    for block in _blocks(text):
        if all(token in block for token in tokens):
            return block
    raise AssertionError(
        "%s: no paragraph carries all of %r — the rule is not stated as one "
        "judgeable unit" % (context, tokens)
    )


def _code_block(section: str) -> str:
    match = re.search(r"```(?:text)?\n(.*?)```", section, re.DOTALL)
    assert match is not None, (
        "expected a fenced code block in the section headed %r" % section.split("\n")[0]
    )
    return match.group(1)


def _prompts() -> str:
    return _read(STAGE_PROMPTS)


def _u4() -> str:
    return _section(_prompts(), "## Independent Verification")


def _slots() -> str:
    return _section(_read(EFFICIENCY), "## 2. ")


def _hard_requirements() -> str:
    return _section(_read(SKILL_MD), "## Hard Requirements")


# --------------------------------------------------------------------------- #
# C-001 / C-002 — the dispatch payload quartet
# --------------------------------------------------------------------------- #
def test_the_stage_prompt_skeleton_carries_the_class_quartet():
    skeleton = _code_block(_section(_prompts(), "### 第①段"))
    missing = [key for key in QUARTET_KEYS if key not in skeleton]
    assert not missing, (
        "segment ① must carry the class quartet %r (C-001); missing %r in the "
        "skeleton" % (QUARTET_KEYS, missing)
    )


def test_the_payload_value_domains_are_closed():
    skeleton = _code_block(_section(_prompts(), "### 第①段"))
    assert "declaration|default" in skeleton, (
        "`source` must state its closed domain `<declaration|default>` (C-001)"
    )
    assert "owner-unavailable|-" in skeleton, (
        "`error` must state its closed domain `<owner-unavailable|->` (C-001): "
        "anything else (e.g. `declaration-absent`) would read an advisory as an "
        "error"
    )


def test_the_quartet_is_one_rule_for_both_topologies():
    _mentions(
        _prompts(),
        ("本地", "远端", "同规"),
        "stage-prompts.md",
    )
    _mentions(
        _prompts(),
        ("提示词", "唯一载体"),
        "stage-prompts.md",
    )


def test_a_missing_quartet_key_is_a_dispatch_construction_defect():
    _mentions(
        _prompts(),
        ("派发构造缺陷", "U4", "不放行"),
        "stage-prompts.md",
    )


def test_the_stage_subagent_may_not_infer_or_default_the_class():
    _mentions(
        _prompts(),
        ("子代理", "MUST NOT", "推断"),
        "stage-prompts.md",
    )
    _mentions(
        _prompts(),
        ("补默认",),
        "stage-prompts.md",
    )


def test_the_error_slot_domain_excludes_the_advisory_code():
    _mentions(
        _prompts(),
        ("error", "值域", "owner-unavailable"),
        "stage-prompts.md",
    )
    _mentions(
        _prompts(),
        ("declaration-absent", "MUST NOT", "载荷"),
        "stage-prompts.md",
    )


def test_an_empty_marker_is_missing_only_outside_the_degraded_shape():
    _mentions(
        _prompts(),
        ("marker", "空", "缺字段"),
        "stage-prompts.md",
    )


def test_the_class_value_comes_from_the_requirements_declaration_each_time():
    _mentions(
        _prompts(),
        ("requirements.md", "声明行", "每次阶段派发前"),
        "stage-prompts.md",
    )
    _mentions(
        _prompts(),
        ("状态脊", "MUST NOT", "取值来源"),
        "stage-prompts.md",
    )
    _mentions(
        _prompts(),
        ("re-baseline",),
        "stage-prompts.md",
    )


# --------------------------------------------------------------------------- #
# C-004 / C-005 — U4's four additional blocking checks
# --------------------------------------------------------------------------- #
def test_u4_keeps_the_existing_four_conditions():
    u4 = _u4()
    for token in ("哨兵", "产物", "纪律", "记账"):
        assert token in u4, "U4 lost its existing condition %r" % token
    assert "四条件" in u4, (
        "the existing four conditions must stay the base U4 verdict (C-004)"
    )


def test_u4_adds_four_blocking_checks_for_expression_lines():
    u4 = _u4()
    assert "表达类" in u4, "U4 must scope the additions to the expression class"
    assert "四项" in u4 and "blocking" in u4, (
        "the four additions must be all-blocking (C-004)"
    )
    for marker in ("(a)", "(b)", "(c)", "(d)"):
        assert marker in u4, "U4 check %s missing (C-004)" % marker


def test_u4_counts_operators_from_the_operator_table_only():
    u4 = _u4()
    _mentions(u4, ("计数分母", "算子表"), "U4")
    _mentions(u4, (IMPLEMENT_OPERATOR, "1 行"), "U4")
    _mentions(u4, ("四个 CLI", "MUST NOT", "算子"), "U4")
    _mentions(u4, ("face=build", "子行", "不另立算子"), "U4")


def test_u4_evidence_is_existence_and_non_empty_without_hash_comparison():
    u4 = _u4()
    _mentions(u4, ("存在且非空", "不做哈希比对"), "U4")
    _mentions(u4, ("MUST NOT", "哈希", "记账字段"), "U4")


def test_u4_compares_the_payload_class_with_the_on_the_spot_parse():
    _mentions(_u4(), ("当场解析", "一致", "派发构造缺陷"), "U4")


def test_u4_routes_the_owner_unavailable_payload_away_from_the_expression_checks():
    u4 = _u4()
    _mentions(u4, ("owner-unavailable", "降级观测", "保持既有"), "U4")
    _mentions(u4, ("MUST NOT", "表达类", "四项校验"), "U4")
    _mentions(u4, ("作者未声明", "MUST NOT"), "U4")


def test_u4_requires_the_stage_status_row():
    _mentions(_u4(), ("stage-status", "在场"), "U4")


def test_gate_evidence_missing_is_incomplete_and_blocks_the_next_dispatch():
    u4 = _u4()
    _mentions(u4, ("门禁证据", "未完成"), "U4")
    _mentions(u4, ("MUST NOT 派发下一阶段",), "U4")


def test_a_build_sub_row_failure_turns_the_operator_verdict_fail():
    u4 = _u4()
    _mentions(u4, ("子行", "算子级", "fail"), "U4")
    _mentions(u4, ("不允许", "子行红、算子绿"), "U4")


def test_a_not_applicable_build_sub_row_is_listed_separately():
    u4 = _u4()
    _mentions(u4, ("not-applicable", "子行", "单列"), "U4")
    _mentions(u4, ("MUST NOT 计入", "passed"), "U4")


# --------------------------------------------------------------------------- #
# C-006 / C-007 / C-008 — the two slots: same skeleton, new content
# --------------------------------------------------------------------------- #
def test_the_slot_skeleton_is_unchanged():
    slots = _slots()
    assert "恰好两个槽位" in slots, (
        "the run line keeps exactly two slots (C-008; owner 067's skeleton)"
    )
    assert "baseline" in slots and "closure" in slots
    assert "implement 起点" in slots, "the baseline point must not move"
    assert "review" in slots and "通过之后" in slots, (
        "the closure point must not move"
    )
    assert "audit-test-budget.py" in slots, (
        "the audit entry must stay named in the slot owner section"
    )


def test_expression_lines_use_the_docs_gate_selection_basis():
    slots = _slots()
    assert "docs-gate-full" in slots, (
        "the expression-class slot takes the new `selection_basis` value (C-006)"
    )
    _mentions(slots, ("selection_basis", "docs-gate-full"), "efficiency §2")
    assert "--action verify --faces reader,evidence,duplicate,count" in slots, (
        "the four-face call must be verbatim in the slot command string (C-006)"
    )
    assert "--action structure" in slots, (
        "the structure sub-step must be part of the same command string (C-006)"
    )
    assert "docs-utils.py --action validate" in slots, (
        "the operator's registered entry still runs; it is the operator-level row "
        "(C-006 / document-structure C-017)"
    )
    _mentions(slots, ("站点层", "face=build", "子行"), "efficiency §2")
    _mentions(slots, ("MUST NOT", "新增聚合脚本"), "efficiency §2")


def test_the_rc_column_is_the_aggregated_exit_code():
    slots = _slots()
    _mentions(slots, ("聚合", "逐命令", "非零优先"), "efficiency §2")
    _mentions(slots, ("evidence_ptr", "rc"), "efficiency §2")


def test_passed_and_failed_count_operator_level_rows_only():
    slots = _slots()
    _mentions(slots, ("passed", "算子级", "pass"), "efficiency §2")
    _mentions(slots, ("failed", "not-evaluated", "算子级"), "efficiency §2")
    _mentions(slots, ("之和", "算子级", "行数"), "efficiency §2")


def test_not_applicable_is_not_a_cross_level_equation():
    slots = _slots()
    _mentions(slots, ("MUST NOT", "跨级", "算子总数"), "efficiency §2")
    _mentions(slots, ("not-applicable", "面级"), "efficiency §2")


def test_closure_baseline_compare_is_a_name_level_operator_id_diff():
    _mentions(
        _slots(),
        ("baseline_compare", "名称级", "算子 id"),
        "efficiency §2",
    )


def test_an_unrun_slot_writes_no_row_and_records_no_zero():
    slots = _slots()
    _mentions(slots, ("未运行", "槽位行"), "efficiency §2")
    _mentions(slots, ("不记 0",), "efficiency §2")


def test_the_audit_and_the_slot_semantics_are_unchanged():
    slots = _slots()
    _mentions(slots, ("audit-test-budget.py", "不变"), "efficiency §2")
    _mentions(slots, ("槽位顺序", "不变"), "efficiency §2")
    assert "stage-check" in slots, (
        "the stage-check semantics must remain named in the slot owner section"
    )


# --------------------------------------------------------------------------- #
# C-009 / C-010 — the class branch moves exactly two things
# --------------------------------------------------------------------------- #
def test_the_class_branch_moves_nothing_but_operators_and_slots():
    text = _prompts()
    _mentions(
        text,
        ("MUST NOT 因类别改变", "阶段序列"),
        "stage-prompts.md",
    )
    protocol = _mentions(
        text,
        ("哨兵字面量", "watcher", "卡死处置", "快车道"),
        "stage-prompts.md",
    )
    assert "退出码" in protocol, (
        "the invariant sentence must keep the watcher exit codes in its scope"
    )
    _mentions(text, ("analyze", "review", "100%"), "stage-prompts.md")


def test_the_skill_hard_requirements_carry_the_class_branch():
    hard = _hard_requirements()
    for key in ("flow_class", "source", "marker", "error"):
        assert key in hard, (
            "the Hard Requirements branch must name the quartet key %r (C-009)"
            % key
        )
    _mentions(hard, ("派发构造缺陷",), "SKILL.md § Hard Requirements")
    _mentions(hard, ("U4", "门禁证据"), "SKILL.md § Hard Requirements")
    _mentions(hard, ("owner-unavailable",), "SKILL.md § Hard Requirements")
    for pointer in ("references/stage-prompts.md", "references/efficiency-model.md"):
        assert pointer in hard, (
            "the branch must point at %s instead of copying its content (C-009)"
            % pointer
        )


def test_the_skill_declares_the_invariants_the_class_may_not_move():
    hard = _hard_requirements()
    _mentions(
        hard,
        ("阶段序列", "哨兵字面量", "watcher", "快车道"),
        "SKILL.md § Hard Requirements",
    )
    _mentions(hard, ("100%",), "SKILL.md § Hard Requirements")
    assert "MUST NOT 因类别改变" in hard, (
        "the branch must state the invariant clause verbatim enough to be judged"
    )
    assert "跳过" in hard or "缩短" in hard, (
        "the clause must refuse requests to skip or shorten a stage (C-010)"
    )


def test_the_stage_chain_and_sentinel_literals_are_untouched():
    skill = _read(SKILL_MD)
    assert (
        "requirements → clarify → plan → tasks → checklist → analyze → implement "
        "→ review" in skill
    ), "the eight-stage chain literal must not move (C-009)"
    assert "大写阶段名 + -DONE" in _prompts(), (
        "the sentinel rule must not move (C-009)"
    )


# --------------------------------------------------------------------------- #
# carrier hygiene — one branch, three files, one operator id
# --------------------------------------------------------------------------- #
def test_the_class_branch_lives_in_the_three_declared_files():
    for path, markers in CLASS_BRANCH_MARKERS.items():
        text = _read(path)
        for marker in markers:
            assert marker in text, (
                "%s must carry the class branch (%s; T017/T019/T020)"
                % (path.relative_to(REPO_ROOT), marker)
            )
    stray = []
    for path in sorted(SKILL_DIR.rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".py", ".sh"}:
            continue
        if path in CLASS_BRANCH_FILES:
            continue
        if CLASS_TOKEN_RE.search(path.read_text(encoding="utf-8", errors="ignore")):
            stray.append(path.relative_to(REPO_ROOT).as_posix())
    assert not stray, (
        "the class branch must not scatter beyond its three carriers (FR-023's "
        "closed wiring surface): %r" % stray
    )


@pytest.mark.parametrize("path", [STAGE_PROMPTS, EFFICIENCY])
def test_the_driver_names_the_implement_operator_and_copies_no_other(path):
    ids = set(OPERATOR_ID_RE.findall(_read(path)))
    assert IMPLEMENT_OPERATOR in ids, (
        "%s must name %s — U4(a)'s denominator is that single registered row, so "
        "the operator must be cited somewhere for the count to exist (C-004)"
        % (path.relative_to(REPO_ROOT), IMPLEMENT_OPERATOR)
    )
    assert ids <= {IMPLEMENT_OPERATOR}, (
        "%s must cite the implement operator only — the operator table has one "
        "owner, the driver does not copy it (C-004): %r"
        % (path.relative_to(REPO_ROOT), sorted(ids))
    )
