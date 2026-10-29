"""Contract tests for Feature 076 — the Decision Tension Record (DTR) contract.

The feature has one new normative owner (``shared/guidelines/decision-tension.md``) and one new
template anchor (``templates/plan-template.md`` § ``## Decision Tensions``). This file asserts the
contract surface, never the prose quality: section presence and adjacency are pinned on the
``^## `` heading sequence, field names are pinned as literal tokens, and the pointer duty is
pinned by resolving the markdown link to a file on disk.

Scenario groups (declared in ``tasks.md``; each lands in its own class so later segments append
without touching earlier assertions):

* **A** — owner declaration + closed record shape + template anchor (T002)
* B — analyze structural channel (T009)
* C — falsification-quartet owner and SI-3C pointer (T013)
* D — non-load-bearing gating (T017)
* E — ADR reference slot and dangling link (T019)
* F — terminology zero-hit guard (T021, post-implementation guard)
* G — closed-set delta guard (T021, post-implementation guard)

Negative samples live in the tests (FR-017): a fixture that merely *describes* a rejection is not
a test. The owner's rejection-list bullets are extracted mechanically and asserted absent from the
template, so "pointer, not a copy" is decided by a comparison rather than by reading.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

OWNER = ROOT / "shared" / "guidelines" / "decision-tension.md"
TEMPLATE = ROOT / "templates" / "plan-template.md"

RUBRIC = ROOT / "shared" / "guidelines" / "task-complexity-rubric.md"
DERIVATION = ROOT / "shared" / "definitions" / "derivation-definitions.md"
FAST_FAIL = ROOT / "shared" / "guidelines" / "fast-fail.md"
CRITIQUE = ROOT / "shared" / "guidelines" / "critique-and-self-critique.md"

ANALYZE_DETECTION = (
    ROOT / "skills" / "internal" / "analyze-artifacts" / "references"
    / "detection-and-severity.md"
)
ANALYZE_SKILL = ROOT / "skills" / "internal" / "analyze-artifacts" / "SKILL.md"
ANALYSIS_GATE = ROOT / "shared" / "workflow" / "objective-analysis-gate.md"
VALIDATOR = ROOT / "scripts" / "python" / "validate-decision-tensions.py"

WORKFLOW = ROOT / "shared" / "workflow" / "self-improvement-workflow.md"

# The quartet's closed field set (FR-019) and the owner section it refines: the one-line
# 「每个提案一条证伪尝试」 description stays byte-identical, the quartet is added beneath it.
QUARTET_KEYS = ("attempt", "exit_code", "observation", "would_go_red_if")
QUARTET_PARENT_HEADING = "## 输出形态:每个提案一条证伪尝试"
SI3C_HEADING = "### SI-3C — Critique Before Dispatch"

# The structural channel's level-3 heading. ``I`` is the next free letter: ``H`` is taken by the
# checklist pass (``SKILL.md`` step 5), so the numbering cannot be reassigned by taste.
CHANNEL_HEADING = "### I."

# The three repo-resolvable adjacent owners; ``/speckit.clarify`` is a command surface, named in
# prose only (it has no file to resolve, and the owner's clause is a boundary statement, not a path).
ADJACENT_OWNER_PATHS = {
    "derivation definitions": "shared/definitions/derivation-definitions.md",
    "fast fail": "shared/guidelines/fast-fail.md",
    "critique and self-critique": "shared/guidelines/critique-and-self-critique.md",
}

FIELD_NAMES = (
    "decision",
    "antithesis",
    "binding_constraints",
    "pole_a",
    "pole_b",
    "discriminating_evidence",
    "expected_sacrifice",
    "revision_trigger",
)

OWNER_SECTION_ADMISSIBILITY = "## 可采纳判据（封闭集，四条全满足）"
OWNER_SECTION_REJECTION = "## 拒绝形态（封闭清单，命中即拒）与判定者分工"
OWNER_SECTION_THRESHOLD = "## 承重门槛（四类触发）与复杂度门控"
OWNER_SECTION_BOUNDARY = "## 与相邻 owner 的边界"
OWNER_SECTION_CONSUMERS = "## 消费者与引用方式"

TEMPLATE_SECTION = "## Decision Tensions"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def read(path: Path) -> str:
    """Read an artifact, failing as 'missing file' rather than as a wrong assertion."""
    assert path.is_file(), f"missing file: {path}"
    return path.read_text(encoding="utf-8")


def norm(text: str) -> str:
    """Whitespace-normalise an artifact body: the docs hard-wrap prose, the pins are spans."""
    return " ".join(text.split())


def h2_headings(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.startswith("## ")]


def h2_section(text: str, heading: str) -> str:
    """Body of an H2 section, up to the next H2 or EOF."""
    m = re.search(rf"^{re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert m, f"missing H2 section: {heading}"
    return m.group(1)


def owner_admissibility_rows() -> list[str]:
    """The owner's admissibility criteria as written — the rows a copy would reproduce."""
    section = h2_section(read(OWNER), OWNER_SECTION_ADMISSIBILITY)
    return [line.strip() for line in section.splitlines() if line.strip()]


def owner_rejection_bullets() -> list[str]:
    section = h2_section(read(OWNER), OWNER_SECTION_REJECTION)
    return [line.strip() for line in section.splitlines()
            if line.strip().startswith("- ")]


# --------------------------------------------------------------------------- #
# Scenario A — owner and template anchor (T002)
# --------------------------------------------------------------------------- #

class TestScenarioAOwnerAndTemplateAnchor:
    """US1: a load-bearing decision leaves a decidable antithesis, its cost and a re-entry point.

    Contract traceability: ``contracts/decision-tension-owner.md`` C-1…C-8 and
    ``contracts/plan-template-anchor.md`` C-1…C-3.
    """

    # --- owner: C-1 -------------------------------------------------------

    def test_owner_declares_ownership_and_pointer_duty(self):
        opening = norm("\n".join(read(OWNER).splitlines()[:14]))
        assert "唯一真源" in opening, (
            "C-1: the owner must open by declaring itself the single source of truth"
        )
        for owned in ("六字段", "可采纳判据", "拒绝形态", "承重", "相邻", "记录标识"):
            assert owned in opening, (
                f"C-1: the opening declaration does not name what it owns: {owned!r}"
            )
        assert "MUST 以路径引用本文件" in opening, (
            "C-1: consumers must be bound to reference this file by path"
        )
        assert "MUST NOT 复述" in opening, (
            "C-1: the pointer duty must forbid restating the criteria/rejection/threshold tables"
        )

    # --- owner: C-2 -------------------------------------------------------

    def test_record_field_set_is_closed_six_plus_id(self):
        text = read(OWNER)
        for field in FIELD_NAMES:
            assert f"`{field}`" in text, f"C-2: field name {field!r} is not declared verbatim"
        assert "`tension_id`" in text, "C-2: the record identifier is not declared"
        assert "`T-NNN`" in text, "C-2: the T-NNN shape is not declared"
        assert "三位" in text, "C-2: the three-digit shape is not stated"
        joined = norm(text)
        assert "字段集合封闭" in joined, "C-2: the field set is not declared closed"
        assert "MUST 走本文件修订" in joined, (
            "C-2: extending a field must be routed through an owner revision"
        )
        assert "不得跳号" in joined, "C-2: the increasing/gapless rule is missing"

    # --- owner: C-3 -------------------------------------------------------

    def test_admissibility_is_closed_four(self):
        section = h2_section(read(OWNER), OWNER_SECTION_ADMISSIBILITY)
        numbered = re.findall(r"(?m)^\d\.\s", section)
        assert len(numbered) == 4, (
            f"C-3: admissibility must be a closed set of four numbered criteria, found "
            f"{len(numbered)}"
        )
        joined = norm(section)
        for phrase in (
            "点名被选中的一极",
            "可被独立采纳的具名方案",
            "在什么条件下它更优",
            "不同时满足两极",
            "结果二值",
        ):
            assert phrase in joined, f"C-3: criterion phrase missing: {phrase!r}"
        assert "封闭集" in joined, "C-3: the criteria are not declared a closed set"

    # --- owner: C-4 -------------------------------------------------------

    def test_rejection_forms_closed_and_named(self):
        section = h2_section(read(OWNER), OWNER_SECTION_REJECTION)
        bullets = owner_rejection_bullets()
        assert bullets, "C-4: the rejection list is empty"
        assert bullets[0].startswith("- `expected_sacrifice: none`"), (
            "C-4: the FIRST rejection entry must be the literal `expected_sacrifice: none`; "
            f"found {bullets[0]!r}"
        )
        joined = norm(section)
        assert "值留空按同一条判" in joined, (
            "C-4: a blank expected_sacrifice must be judged under the same rejection class"
        )
        for covered in ("任一极点为空", "非二值", "稻草人", "要平衡", "综合考虑", "视情况而定"):
            assert covered in joined, f"C-4: rejection coverage missing: {covered!r}"
        assert "清单条目新增 MUST 走本文件修订" in joined, (
            "C-4: adding a rejection entry must be routed through an owner revision"
        )
        # The judge split is part of the closure: machine three vs reviewer two.
        assert "由确定性校验器判定" in joined, (
            "C-4: the machine-decidable three must be assigned to the validator"
        )
        assert "由两位复核者按同一条判据判定" in joined, (
            "C-4: the two semantic forms must be assigned to two reviewers on one criterion"
        )
        assert "同一 verdict" in joined, (
            "C-4: the two reviewers MUST reach the same verdict"
        )

    # --- owner: C-5 -------------------------------------------------------

    def test_load_bearing_threshold_four_triggers(self):
        joined = norm(h2_section(read(OWNER), OWNER_SECTION_THRESHOLD))
        for trigger in (
            "不可逆（回滚需要迁移或重建）",
            "跨团队（改变他人依赖的契约或接口）",
            "高爆炸半径（故障影响面超出本特性边界）",
            "与宪法原则相关（触及任一 MUST 条）",
        ):
            assert trigger in joined, f"C-5: trigger missing or reworded: {trigger!r}"
        assert "任一成立即承重" in joined, "C-5: the any-one-triggers rule is missing"
        assert "MUST NOT 被要求填写记录" in joined, (
            "C-5: a non-load-bearing decision MUST NOT be asked for a record"
        )
        assert "缺失记录 MUST NOT 被判为缺陷" in joined, (
            "C-5: a missing record MUST NOT be judged a defect outside the threshold"
        )

    # --- owner: C-6 -------------------------------------------------------

    def test_complexity_gating_points_at_rubric(self):
        joined = norm(h2_section(read(OWNER), OWNER_SECTION_THRESHOLD))
        assert "shared/guidelines/task-complexity-rubric.md" in joined, (
            "C-6: the complexity gate must reach the rubric by path"
        )
        assert "Trivial" in joined and "按定义不含" in joined, (
            "C-6: a Trivial task must be declared free of load-bearing decisions by definition"
        )
        assert "tie-break" in joined, "C-6: the conflict resolution must name the rubric tie-break"
        assert "以承重判据为准" in joined, (
            "C-6: the threshold decides whether a record is required"
        )
        assert RUBRIC.is_file(), f"C-6: the referenced rubric does not exist: {RUBRIC}"

    # --- owner: C-7 -------------------------------------------------------

    def test_adjacent_owner_boundaries_by_path(self):
        section = h2_section(read(OWNER), OWNER_SECTION_BOUNDARY)
        for label, rel in ADJACENT_OWNER_PATHS.items():
            assert rel in section, f"C-7: adjacent owner not referenced by path: {label}"
            assert (ROOT / rel).is_file(), f"C-7: referenced adjacent owner is missing: {rel}"
        assert "/speckit.clarify" in section, (
            "C-7: the clarify lane must be named in the division of labour"
        )
        joined = norm(section)
        assert "方向已选定之后的技术取舍" in joined, (
            "C-7: the owner must bound itself to post-direction technical trade-offs"
        )
        assert "MUST NOT 承接需求分歧" in joined, (
            "C-7: requirement-stage disagreement is out of scope"
        )

    # --- owner: C-8 -------------------------------------------------------

    def test_owner_has_no_second_definition_or_carrier(self):
        text = read(OWNER)
        joined = norm(text)
        assert "MUST NOT 引入持久化载体" in joined, (
            "C-8: the owner must forbid introducing a persistence carrier"
        )
        for forbidden in ("台账", "调度器", "评分器", "运行时"):
            assert forbidden in joined, (
                f"C-8: the no-machinery clause must name {forbidden!r}"
            )
        # No second definition of an adjacent owner's enumeration:
        #  - the complexity rubric's tier table must not be reproduced here;
        #  - the falsification quartet's field names belong to the critique owner.
        assert "| **Trivial** |" not in text, (
            "C-8: the owner reproduces the rubric's tier table instead of referencing it"
        )
        assert "would_go_red_if" not in text, (
            "C-8: the quartet field names are defined by critique-and-self-critique.md, "
            "never restated here"
        )
        # The consumer list is pointer-shaped: path + how it references, one row per consumer.
        section = h2_section(text, OWNER_SECTION_CONSUMERS)
        rows = [line for line in section.splitlines()
                if line.strip().startswith("|") and "`" in line and "---" not in line]
        assert len(rows) >= 5, (  # header row + four consumers
            f"C-8: the consumer list is not pointer-shaped (rows with a path: {len(rows)})"
        )

    # --- template: C-1 ----------------------------------------------------

    def test_template_section_adjacent_to_constitution_check(self):
        headings = h2_headings(read(TEMPLATE))
        assert headings.count(TEMPLATE_SECTION) == 1, (
            f"C-1: `{TEMPLATE_SECTION}` must appear exactly once; found "
            f"{headings.count(TEMPLATE_SECTION)}"
        )
        anchor = headings.index("## Constitution Check")
        assert headings[anchor + 1] == TEMPLATE_SECTION, (
            "C-1: `## Decision Tensions` must be the DIRECT successor of `## Constitution Check`; "
            f"found {headings[anchor + 1]!r}"
        )
        assert headings[anchor + 2] == "## Project Structure", (
            "C-1: `## Project Structure` must be the direct successor of the new section; "
            f"found {headings[anchor + 2]!r}"
        )

    # --- template: C-2 ----------------------------------------------------

    def test_template_carrier_and_na_rule(self):
        section = h2_section(read(TEMPLATE), TEMPLATE_SECTION)
        joined = norm(section)
        assert "`T-NNN`" in section, "C-2: the record id shape is not named in the section"
        assert "### T-001" in section or "### T-NNN" in section, (
            "C-2: the section must show a level-3 sub-section heading beginning with T-NNN"
        )
        assert "N/A" in section, "C-2: the N/A rule is missing"
        assert "one line per trigger" in joined, (
            "C-2: N/A must be accompanied by one line per trigger"
        )
        assert "MUST NOT be deleted or left empty" in joined, (
            "C-2: the section must not be deletable or left empty"
        )

    # --- template: C-3 ----------------------------------------------------

    def test_template_is_pointer_not_copy_and_path_resolves(self):
        section = h2_section(read(TEMPLATE), TEMPLATE_SECTION)
        assert "shared/guidelines/decision-tension.md" in section, (
            "C-3: the section must point at the owner by path"
        )
        link = re.search(r"\]\(([^)]*decision-tension\.md)\)", section)
        assert link, "C-3: the pointer is not a resolvable markdown link"
        target = (TEMPLATE.parent / link.group(1)).resolve()
        assert target.is_file(), (
            f"C-3: the pointer path does not resolve to an existing file: {link.group(1)!r}"
        )
        assert target == OWNER.resolve(), (
            "C-3: the pointer resolves somewhere other than the owner document"
        )
        for field in FIELD_NAMES:
            assert field in section, f"C-3: the field-name list is missing {field!r}"
        # The negative half: no owner admissibility row, rejection bullet or threshold
        # definition may be reproduced verbatim in the template.
        reproduced = [row for row in owner_admissibility_rows()
                      if len(row) > 20 and row in section]
        assert reproduced == [], (
            f"C-3: the template reproduces owner admissibility rows: {reproduced!r}"
        )
        copied_bullets = [b for b in owner_rejection_bullets() if b in section]
        assert copied_bullets == [], (
            f"C-3: the template reproduces rejection-list bullets: {copied_bullets!r}"
        )
        for threshold_definition in ("回滚需要迁移或重建", "故障影响面超出本特性边界"):
            assert threshold_definition not in section, (
                f"C-3: the template reproduces the threshold table: {threshold_definition!r}"
            )


# --------------------------------------------------------------------------- #
# Scenario B — analyze structural channel (T009)
# --------------------------------------------------------------------------- #

CHANNEL_PLAN_HEAD = """# Implementation Plan: channel fixture

## Summary

Fixture plan for the analysis channel.

## Constitution Check

*GATE: fixture.*

"""

CHANNEL_PLAN_TAIL = """
## Project Structure

Fixture structure.
"""

CHANNEL_RECORD = """### T-001 — fixture decision

- **decision**: 选择方案 A，因为它在夹具里可判定。
- **antithesis**: 方案 B 是可独立采纳的具名方案；当吞吐需求高于 1k/s 时它更优。
- **binding_constraints**:
  - pole_a: 结果必须逐字节可复现。
  - pole_b: 实现必须能用现有工具链构建。
- **discriminating_evidence**: 运行一次 `pytest -q` 并比较退出码，结果二值。
- **expected_sacrifice**: SC-001 Source ↓ 低于阈值 90% 即重开。
- **revision_trigger**: 连续两次低于阈值 → 重开并复核。
"""

CHANNEL_NA = """N/A — 四类触发逐条不成立：

- 不可逆：改动只替换一处措辞，回滚无需迁移或重建。
- 跨团队：不改变他人依赖的契约或接口。
- 高爆炸半径：故障影响面限于本节文字。
- 与宪法原则相关：不触及任何 MUST 条。
"""

CHANNEL_REQUIREMENTS = """# Requirements: channel fixture

## Success Criteria

- **SC-001**: fixture criterion.

### Measurement Sources & Collection Methods

- **SC-001 Source**: fixture measurement source.
"""

CHANNEL_REQUIREMENTS_NO_SOURCES = """# Requirements: channel fixture

## Success Criteria

- **SC-001**: fixture criterion.
"""


def channel_section_lines() -> list[str]:
    """The channel's own level-3 section, line-for-line (trailing blank line included)."""
    lines = read(ANALYZE_DETECTION).splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith(CHANNEL_HEADING):
            start = index
            break
    assert start is not None, (
        f"the structural channel section ({CHANNEL_HEADING}) is not declared in "
        f"{ANALYZE_DETECTION.relative_to(ROOT)}"
    )
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## ") or lines[index].startswith("### "):
            end = index
            break
    return lines[start:end]


def channel_section() -> str:
    """The channel's own level-3 section — the only region this scenario judges."""
    return "\n".join(channel_section_lines())


def channel_plan(*records: str) -> str:
    body = "## Decision Tensions\n\n" + "\n".join(records) + "\n"
    return CHANNEL_PLAN_HEAD + body + CHANNEL_PLAN_TAIL


def channel_record(field: str = None, value: str = None) -> str:
    """The compliant record, optionally with one field line deleted or its value replaced."""
    if field is None:
        return CHANNEL_RECORD
    if value is None:
        return "\n".join(
            line for line in CHANNEL_RECORD.splitlines()
            if not line.startswith(f"- **{field}**:")
        ) + "\n"
    return "\n".join(
        f"- **{field}**: {value}" if line.startswith(f"- **{field}**:") else line
        for line in CHANNEL_RECORD.splitlines()
    ) + "\n"


def write_channel_spec(root: Path, plan_text: str, requirements_text: str = CHANNEL_REQUIREMENTS) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "plan.md").write_text(plan_text, encoding="utf-8")
    (root / "requirements.md").write_text(requirements_text, encoding="utf-8")
    return root


def run_validator(spec_dir: Path) -> subprocess.CompletedProcess:
    assert VALIDATOR.is_file(), f"missing artifact: {VALIDATOR}"
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--spec", str(spec_dir), "--json"],
        capture_output=True,
        text=True,
    )


def verdict_of(spec_dir: Path) -> tuple[int, dict]:
    """Run the program and return ``(exit_code, label -> count)`` — never a re-derivation."""
    proc = run_validator(spec_dir)
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:  # pragma: no cover - surfaced as a readable failure
        raise AssertionError(
            f"validator --json did not print JSON; exit={proc.returncode} "
            f"stdout={proc.stdout!r} stderr={proc.stderr!r}"
        )
    return proc.returncode, {check["label"]: check["count"] for check in payload["checks"]}


def validator_labels() -> tuple[str, ...]:
    """The validator's closed label set, imported rather than restated."""
    assert VALIDATOR.is_file(), f"missing artifact: {VALIDATOR}"
    spec = importlib.util.spec_from_file_location("_dt_validator_for_channel", VALIDATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return tuple(module.LABELS)


def defect_table(section: str) -> list[list[str]]:
    """The channel's defect-class table rows (data rows only), cells stripped."""
    rows = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        rows.append(cells)
    return rows[1:]  # drop the header row


# The containment baseline named by ``contracts/analyze-channel.md`` C-5 / FR-014. A dated
# referent, never "whatever HEAD says": the allowed delta is measured against this commit.
BASELINE_COMMIT = "ac63fe8c"

SKILL_ENUMERATION_RE = re.compile(r"^(Seven|Eight) passes \(A duplication")


def git_show(rel_path: Path, revision: str = BASELINE_COMMIT) -> str:
    rel = rel_path.relative_to(ROOT).as_posix()
    proc = subprocess.run(
        ["git", "show", f"{revision}:{rel}"], cwd=ROOT, capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"cannot read {rel} at {revision}: {proc.stderr}"
    return proc.stdout


def diff_lines(rel_path: Path, revision: str = BASELINE_COMMIT) -> tuple[list[str], list[str]]:
    """``(removed, added)`` line bodies for one file against the baseline — no hunk chrome."""
    rel = rel_path.relative_to(ROOT).as_posix()
    proc = subprocess.run(
        ["git", "diff", "--no-color", "-U0", revision, "--", rel],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"git diff failed for {rel}: {proc.stderr}"
    removed, added = [], []
    for line in proc.stdout.splitlines():
        if line.startswith("---") or line.startswith("+++"):
            continue
        if line.startswith("-"):
            removed.append(line[1:])
        elif line.startswith("+"):
            added.append(line[1:])
    return removed, added


def pointer_paragraph(text: str) -> list[str]:
    """The pass-enumeration paragraph that points at the detection reference."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if SKILL_ENUMERATION_RE.match(line):
            start = index
            break
    assert start is not None, "the pass-enumeration paragraph is missing from SKILL.md"
    end = start
    while end < len(lines) and "detection-and-severity.md" not in lines[end]:
        end += 1
    assert end < len(lines), "the enumeration paragraph lost its pointer line"
    return lines[start:end + 1]


def h3_section(text: str, heading: str) -> str:
    """Body of an H3 section, up to the next H3 or H2."""
    m = re.search(rf"^{re.escape(heading)}\s*$(.*?)(?=^### |^## |\Z)", text, re.M | re.S)
    assert m, f"missing H3 section: {heading}"
    return m.group(1)


class TestScenarioBAnalyzeStructuralChannel:
    """US2: the analysis stage stops a tension record that does not hold.

    Contract traceability: ``contracts/analyze-channel.md`` C-1…C-4 (C-5 is pinned by the
    allowed-delta enumeration added with the channel registration).
    """

    # --- C-1 --------------------------------------------------------------

    def test_channel_scope_is_one_plan_artifact(self, tmp_path):
        section = norm(channel_section())
        assert "REQUIREMENTS_DIR" in section, (
            "C-1: the judged object must be named as the plan under REQUIREMENTS_DIR"
        )
        assert "exactly one artifact" in section, (
            "C-1: the channel must declare a single judged artifact"
        )
        assert "never a second judged object" in section, (
            "C-1: requirements.md must be declared a mapping reference, not a second object"
        )
        assert "MUST NOT open any other feature directory" in section, (
            "C-1: the channel must forbid opening another feature directory's plan"
        )
        assert "produce no finding at all" in section, (
            "C-1: an out-of-scope plan must produce no finding at all"
        )
        assert "NOT exempt" in section, (
            "C-1: in-scope historical plans must not be exempted"
        )

        # Mechanical half: the checker is directory-scoped. A broken sibling directory never
        # colours the verdict on a compliant spec, and the in-scope plan written before the
        # contract (no section at all) is reported rather than skipped.
        good = write_channel_spec(tmp_path / "in-scope-good", channel_plan(CHANNEL_RECORD))
        write_channel_spec(tmp_path / "out-of-scope-broken", CHANNEL_PLAN_HEAD + CHANNEL_PLAN_TAIL)
        code, counts = verdict_of(good)
        assert code == 0, f"a compliant in-scope plan must exit 0; counts={counts!r}"
        assert set(counts.values()) == {0}, (
            f"a broken sibling directory must not colour this verdict; counts={counts!r}"
        )

        historical = write_channel_spec(
            tmp_path / "in-scope-historical", CHANNEL_PLAN_HEAD + CHANNEL_PLAN_TAIL
        )
        code, counts = verdict_of(historical)
        assert code == 1, "an in-scope plan without the section is a defect, not a skip"
        assert counts["dtr-section-missing"] == 1, (
            f"the missing-section class must be reported once; counts={counts!r}"
        )

    # --- C-2 --------------------------------------------------------------

    def test_three_defect_classes_fail_closed_no_advisory(self, tmp_path):
        section = norm(channel_section())
        assert "HIGH or 0" in section, (
            "C-2: the value domain must be declared as HIGH or 0"
        )
        assert "no advisory or downgrade tier" in section, (
            "C-2: the channel must forbid an advisory or downgrade tier"
        )

        rows = defect_table(channel_section())
        assert len(rows) == 3, (
            f"C-2: exactly three defect classes must be declared, found {len(rows)}"
        )
        closed = set(validator_labels())
        declared = set()
        for row in rows:
            assert len(row) == 3, f"C-2: a defect row must have three cells; got {row!r}"
            assert row[2] == "HIGH", (
                f"C-2: every defect class is HIGH, found severity {row[2]!r} in {row!r}"
            )
            labels = set(re.findall(r"`([a-z-]+)`", row[1]))
            assert labels, f"C-2: the row names no validator label: {row!r}"
            assert labels <= closed, (
                f"C-2: the row names labels outside the validator's closed set: "
                f"{sorted(labels - closed)}"
            )
            declared |= labels
        # The three declared classes cover exactly these four validator labels; the validator's
        # remaining labels (the template anchor, the identifier shape) are not channel classes.
        assert declared == {
            "dtr-section-missing",
            "dtr-record-incomplete",
            "dtr-rejected-form",
            "expected-sacrifice-unmapped",
        }, f"C-2: the declared defect classes cover {sorted(declared)}"

        # One fixture per class; each defect run yields exactly one finding (no double counting).
        compliant = write_channel_spec(tmp_path / "compliant", channel_plan(CHANNEL_RECORD))
        code, counts = verdict_of(compliant)
        assert code == 0 and set(counts.values()) == {0}, (
            f"a compliant plan must be clean; counts={counts!r}"
        )

        cases = [
            ("missing-section", CHANNEL_PLAN_HEAD + CHANNEL_PLAN_TAIL, "dtr-section-missing"),
            ("incomplete-record", channel_plan(channel_record("revision_trigger")),
             "dtr-record-incomplete"),
            ("single-pole", channel_plan(
                channel_record().replace("- pole_b: 实现必须能用现有工具链构建。", "- pole_b:"),
            ), "dtr-rejected-form"),
            ("unmappable-cost", channel_plan(
                channel_record("expected_sacrifice", "SC-099 Source ↓ 未声明的来源"),
            ), "expected-sacrifice-unmapped"),
        ]
        for name, plan_text, label in cases:
            spec = write_channel_spec(tmp_path / name, plan_text)
            code, counts = verdict_of(spec)
            assert code == 1, f"{name}: a defect class must exit 1; counts={counts!r}"
            assert counts[label] == 1, f"{name}: expected one {label}; counts={counts!r}"
            assert sum(counts.values()) == 1, (
                f"{name}: fail-closed means one finding per defect, not a pile; counts={counts!r}"
            )

    def test_requirements_without_measurement_sources_branches_on_record_count(self, tmp_path):
        section = norm(channel_section())
        assert "branch mechanically on the record count" in section, (
            "C-2: the missing-measurement-source branch must be declared mechanical"
        )
        assert "one or more records fail mapping one by one" in section, (
            "C-2: with records present, each one fails mapping"
        )
        assert "zero findings" in section, (
            "C-2: a compliant N/A with zero records produces zero findings"
        )

        with_records = write_channel_spec(
            tmp_path / "records-no-sources",
            channel_plan(CHANNEL_RECORD),
            CHANNEL_REQUIREMENTS_NO_SOURCES,
        )
        code, counts = verdict_of(with_records)
        assert code == 1, "records without a declared source must fail mapping"
        assert counts["expected-sacrifice-unmapped"] == 1, (
            f"the single record must fail mapping once; counts={counts!r}"
        )

        without_records = write_channel_spec(
            tmp_path / "na-no-sources",
            channel_plan(CHANNEL_NA),
            CHANNEL_REQUIREMENTS_NO_SOURCES,
        )
        code, counts = verdict_of(without_records)
        assert code == 0, "a compliant N/A with zero records must not fail mapping"
        assert set(counts.values()) == {0}, (
            f"zero records means the mapping verdict is not executed; counts={counts!r}"
        )

    # --- C-3 --------------------------------------------------------------

    def test_severity_follows_propagation_surface(self):
        assert ANALYSIS_GATE.is_file(), f"missing severity owner: {ANALYSIS_GATE}"
        gate = norm(read(ANALYSIS_GATE))
        assert "propagation-surface" in gate and "FIRST field" in gate, (
            "C-3: the gate owner must still carry the propagation-surface criterion"
        )

        section = norm(channel_section())
        assert "objective-analysis-gate.md" in section, (
            "C-3: the channel must reach the severity owner by path"
        )
        assert "no new severity level" in section, (
            "C-3: the channel must not invent a severity level"
        )
        assert "计划 → 任务 / 实现" in section, (
            "C-3: every finding must name its propagation surface"
        )
        assert "FIRST field" in section, (
            "C-3: the propagation surface must be the finding's first field"
        )

    # --- C-4 --------------------------------------------------------------

    def test_verdicts_come_from_the_program(self, tmp_path):
        section = norm(channel_section())
        assert "scripts/python/validate-decision-tensions.py" in section, (
            "C-4: the channel must name the program that prints the verdict"
        )
        assert "MUST NOT re-score" in section, (
            "C-4: the model must consume the verdict instead of scoring semantically"
        )

        code, counts = verdict_of(
            write_channel_spec(tmp_path / "program-verdict", channel_plan(CHANNEL_RECORD))
        )
        assert code == 0 and set(counts.values()) == {0}, (
            "C-4: the verdict must be the program's exit code plus its label counts"
        )
        assert set(counts) == set(validator_labels()), (
            "C-4: the consumption surface is the program's own closed label set"
        )

    # --- C-5 --------------------------------------------------------------

    def test_channel_only_add_allowed_delta_enumeration(self):
        detection = read(ANALYZE_DETECTION)

        # (1) The count heading changes by exactly one, and the new channel letter is unique.
        count_headings = [line for line in detection.splitlines()
                          if line.startswith("## The ") and line.endswith("passes")]
        assert count_headings == ["## The eight passes"], (
            "C-5: the count heading must carry the new channel; found "
            f"{count_headings!r}"
        )
        subsections = [line for line in detection.splitlines()
                       if re.match(r"^### [A-Z]\. ", line)]
        letters = [re.match(r"^### ([A-Z])\. ", line).group(1) for line in subsections]
        assert letters == ["A", "B", "C", "D", "E", "F", "G", "I"], (
            f"C-5: the channel letters must be A-G plus I (H is the checklist pass); {letters!r}"
        )
        assert len(set(letters)) == len(letters), f"C-5: a channel letter repeats: {letters!r}"

        # (2) The declared allowed delta is exactly 「the new channel section + the count line」.
        removed, added = diff_lines(ANALYZE_DETECTION)
        assert removed == ["## The seven passes"], (
            "C-5: the delta set declares ZERO deleted or rewritten lines outside the count "
            f"line; removed {removed!r}"
        )
        assert added == ["## The eight passes"] + channel_section_lines(), (
            "C-5: every added line must belong to the new channel section or be the count "
            "heading; the comparison unit is 「existing paragraph / new paragraph」"
        )

        # (3) SKILL.md is a pointer update OUTSIDE the containment claim: its only delta is the
        # enumeration paragraph, and that paragraph now names the new channel.
        old_paragraph = pointer_paragraph(git_show(ANALYZE_SKILL))
        new_paragraph = pointer_paragraph(read(ANALYZE_SKILL))
        removed_skill, added_skill = diff_lines(ANALYZE_SKILL)
        assert removed_skill == [line for line in old_paragraph if line not in new_paragraph], (
            "C-5: SKILL.md must change only inside its pass-enumeration paragraph; "
            f"removed {removed_skill!r}"
        )
        assert added_skill == [line for line in new_paragraph if line not in old_paragraph], (
            f"C-5: SKILL.md gained a change outside the enumeration paragraph: {added_skill!r}"
        )
        updated = " ".join(new_paragraph)
        assert "Eight passes" in updated, (
            f"C-5: the two enumerations must not drift; SKILL.md still says: {updated!r}"
        )
        assert "I decision tension records" in updated, (
            f"C-5: the new channel is missing from the SKILL.md enumeration: {updated!r}"
        )


# --------------------------------------------------------------------------- #
# Scenario C — falsification quartet owner and the SI-3C pointer (T013)
# --------------------------------------------------------------------------- #

def quartet_section() -> str:
    """The quartet sub-section inside the owner's output-form section.

    Located by content (all four literal keys), not by its heading wording: the heading is the
    owner's to phrase, the field set is the contract's.
    """
    parent = h2_section(read(CRITIQUE), QUARTET_PARENT_HEADING)
    blocks = re.split(r"(?m)^### ", parent)
    for block in blocks[1:]:
        if all(f"`{key}`" in block for key in QUARTET_KEYS):
            return block
    raise AssertionError(
        "the quartet sub-section is missing: no `### ` block under "
        f"{QUARTET_PARENT_HEADING!r} names all four keys {QUARTET_KEYS!r}"
    )


class TestScenarioCQuartetOwner:
    """US3: a falsification attempt must actually have run, and must be able to go red.

    Contract traceability: ``contracts/falsification-quartet.md`` C-1, C-2, C-4, C-5 (C-3 is
    pinned by ``test_falsification_quartet_validator.py``).
    """

    # --- C-1 --------------------------------------------------------------

    def test_owner_declares_closed_quartet(self):
        section = quartet_section()
        for key in QUARTET_KEYS:
            assert f"`{key}`" in section, (
                f"C-1: the quartet field {key!r} is not declared verbatim in its sub-section"
            )
        joined = norm(section)
        assert "字段集合封闭" in joined, "C-1: the quartet's field set must be declared closed"
        assert "MUST 走本文件修订" in joined, (
            "C-1: extending the quartet must be routed through an owner revision"
        )
        assert "产出形态" in joined, (
            "C-1: the sub-section must declare the quartet to BE the produced form"
        )

        # The earlier one-line description is preserved byte-identical, and the quartet is
        # appended beneath it — the refinement is normative while containment stays true.
        baseline = h2_section(git_show(CRITIQUE), QUARTET_PARENT_HEADING)
        current = h2_section(read(CRITIQUE), QUARTET_PARENT_HEADING)
        assert current.startswith(baseline), (
            "C-1: the existing 「one falsification attempt per proposal」 text must stay "
            "byte-identical; the quartet is an addition, never a rewrite"
        )
        assert len(current) > len(baseline), (
            "C-1: the quartet sub-section is missing from the output-form section"
        )

    # --- C-2 --------------------------------------------------------------

    def test_field_semantics_decidable(self):
        joined = norm(quartet_section())
        # attempt — replayable by a reviewer; replayability is a reviewer rule, not a verdict.
        assert "可原样重放" in joined or "原样重放" in joined, (
            "C-2: `attempt` must be declared replayable verbatim by a reviewer"
        )
        assert "只判非空" in joined, (
            "C-2: the checker may only require `attempt` to be non-empty"
        )
        assert "MUST NOT 判其可否重放" in joined or "MUST NOT 判它「可否重放」" in joined, (
            "C-2: replayability must be declared a reviewer rule, never a program verdict"
        )
        # exit_code — an integer.
        assert "整数" in joined, "C-2: `exit_code` must be declared an integer"
        # observation — the literal marker is the mechanical proxy for 「not a paraphrase」.
        assert "`raw:`" in joined, "C-2: `observation` must carry the literal `raw:` marker"
        assert "转述" in joined, (
            "C-2: `raw:` must be declared the mechanical proxy for 「not a paraphrase」"
        )
        # would_go_red_if — both halves, first-`red:` split, backtick spans.
        assert "第一次出现" in joined, (
            "C-2: the split point is the FIRST occurrence of the literal `red:`"
        )
        assert "`red:`" in joined, "C-2: the literal `red:` marker must be named"
        assert "反引号跨度" in joined, (
            "C-2: both halves are machine-checkable only as backtick spans"
        )
        assert "两半" in joined, "C-2: both halves must be declared"
        for named in ("断言名", "检查标签", "非零退出码"):
            assert named in joined, (
                f"C-2: the signal half must name one of {named!r}"
            )

    # --- C-4 --------------------------------------------------------------

    def test_carrier_unchanged_no_new_store(self):
        joined = norm(quartet_section())
        assert "MUST NOT 新建台账、存储、probe 或评分" in joined, (
            "C-4: the quartet must keep the proposal's existing carrier — no ledger, store, "
            "probe or score"
        )

    # --- disclosed limitations (C-3's non-blocking half) -------------------

    def test_disclosed_limitations_are_non_blocking(self):
        joined = norm(quartet_section())
        assert "可被伪造" in joined, (
            "the `raw:` marker's forgeability must be disclosed, not hidden"
        )
        assert "不可证" in joined, (
            "the truth of the `red:` signal (a broken input that never goes red) must be "
            "disclosed as unprovable by the shape"
        )
        assert "非阻断注记" in joined, (
            "both limitations must be disposed as non-blocking notes"
        )
        assert "不进程序判决" in joined, (
            "neither limitation may enter the program verdict"
        )
        assert "复核者" in joined, (
            "both limitations are found by reviewers, not by the checker"
        )

    # --- C-5 --------------------------------------------------------------

    def test_si3c_pointer_only_both_directions(self):
        workflow = norm(h3_section(read(WORKFLOW), SI3C_HEADING))
        assert "shared/guidelines/critique-and-self-critique.md" in workflow, (
            "C-5: SI-3C must reach the owner by path"
        )
        assert "falsification attempt" in workflow, (
            "C-5: SI-3C must keep its step summary"
        )
        for key in QUARTET_KEYS:
            assert f"{key}:" not in workflow, (
                f"C-5: SI-3C restates the quartet field {key!r} — the owner defines it once"
            )
        for reason in (
            "missing-field", "empty-field", "exit-code-not-integer",
            "observation-not-raw", "tautology", "input-unreadable",
        ):
            assert reason not in workflow, (
                f"C-5: SI-3C restates the rejection reason {reason!r}"
            )
        # The other direction: the owner does define them (a pointer with no target is a dead end).
        owner = norm(quartet_section())
        for key in QUARTET_KEYS:
            assert f"`{key}`" in owner, f"C-5: the owner does not define {key!r}"


# --------------------------------------------------------------------------- #
# Scenario D — non-load-bearing gating (T017)
# --------------------------------------------------------------------------- #

SPEC_DIR = ROOT / ".specify" / "specs" / "076-decision-tension-contract"
ANALYZE_SNAPSHOT_DIR = SPEC_DIR / "notes" / "analyze-sc003"

# The channel's four defect classes are the count surface for SC-003; ``dtr-anchor`` is not one of
# them (it is the template-adjacency assertion, suppressed whenever the section is missing).
SC003_CHANNEL_LABELS = (
    "dtr-section-missing",
    "dtr-record-incomplete",
    "dtr-rejected-form",
    "expected-sacrifice-unmapped",
)

# The four load-bearing triggers, spelled as the owner's threshold section spells them. A compliant
# ``N/A`` must say, trigger by trigger, why that trigger does not hold.
TRIGGERS = ("不可逆", "跨团队", "高爆炸半径", "与宪法原则相关")


def validator_payload(spec_dir: Path) -> tuple[int, dict]:
    """``(exit_code, full --json payload)`` — the record count is read, never re-derived."""
    proc = run_validator(spec_dir)
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:  # pragma: no cover - surfaced as a readable failure
        raise AssertionError(
            f"validator --json did not print JSON; exit={proc.returncode} "
            f"stdout={proc.stdout!r} stderr={proc.stderr!r}"
        )
    return proc.returncode, payload


def label_counts(payload: dict) -> dict:
    return {check["label"]: check["count"] for check in payload["checks"]}


def write_sc003_snapshot(slug: str, fixture: str, spec_dir: Path, exit_code: int, payload: dict) -> Path:
    """Archive one SC-003 analyze-channel snapshot; SC-003's HIGH count reads only these files.

    The channel is a declared detection pass, not a program, so the run that produces its report is
    this test: the snapshot carries the program's verdict verbatim (exit code, per-label counts,
    record count) under the channel's four defect classes. Rendering is deterministic, so a re-run
    refreshes it instead of accumulating near-duplicates.
    """
    counts = label_counts(payload)
    high = sum(counts[label] for label in SC003_CHANNEL_LABELS)
    lines = [
        f"# SC-003 analyze snapshot — {slug}",
        "",
        f"- fixture: {fixture}",
        "- judged artifact: `plan.md` under `REQUIREMENTS_DIR` (the channel's only object; "
        "`requirements.md` is the mapping reference, never a second judged object)",
        f"- validator: `scripts/python/validate-decision-tensions.py --spec <fixture> --json`",
        f"- exit_code: {exit_code}",
        f"- records: {payload['scanned']['records']}",
        f"- HIGH findings: {high}",
        "",
        "| label | status | count |",
        "|---|---|---|",
    ]
    for check in payload["checks"]:
        lines.append(f"| `{check['label']}` | {check['status']} | {check['count']} |")
    lines.append("")
    target = ANALYZE_SNAPSHOT_DIR / f"{slug}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")
    return target


class TestScenarioDNonLoadBearingGating:
    """US4: a trivial plan pays no ceremony, and the gate stays reachable when it stops being trivial.

    SC-003 is read from exactly three snapshots (``notes/analyze-sc003/``): the compliant ``N/A``
    run (0), the section-removed run (1) and the compliant-record run (0). The bare-``N/A`` case is
    an ADDITIONAL assertion on the ``N/A`` criterion: it pins the rule, produces no snapshot and is
    not part of the SC-003 triple.
    """

    # --- D-1 (SC-003 run 1) ------------------------------------------------

    def test_d1_compliant_na_yields_zero_records_and_zero_findings(self, tmp_path):
        plan_text = channel_plan(CHANNEL_NA)
        # The fixture really is the declared shape: one line per trigger, each explaining why it
        # does not hold — the criterion the checker must be able to read.
        na_block = h2_section(plan_text, "## Decision Tensions")
        assert "N/A" in na_block, "the fixture must carry the literal N/A"
        assert "不成立" in norm(na_block), (
            "D-1: a compliant N/A must state that the triggers do not hold"
        )
        for trigger in TRIGGERS:
            assert trigger in na_block, (
                f"D-1: the compliant N/A must justify the {trigger!r} trigger one by one"
            )

        spec = write_channel_spec(tmp_path / "d1-compliant-na", plan_text)
        code, payload = validator_payload(spec)
        counts = label_counts(payload)
        assert payload["scanned"]["records"] == 0, (
            f"D-1: a compliant N/A carries zero records; scanned={payload['scanned']!r}"
        )
        assert code == 0, f"D-1: a compliant N/A must exit 0; counts={counts!r}"
        assert set(counts.values()) == {0}, (
            f"D-1: a compliant N/A must produce zero findings; counts={counts!r}"
        )

        snapshot = write_sc003_snapshot(
            "D-1-compliant-na", "trivial plan: N/A plus one line per trigger", spec, code, payload
        )
        assert snapshot.is_file(), "D-1's SC-003 snapshot must be archived"

    # --- additional assertion (not part of the SC-003 triple) --------------

    def test_bare_na_without_per_trigger_justification_is_a_missing_record(self, tmp_path):
        spec = write_channel_spec(tmp_path / "bare-na", channel_plan("N/A\n"))
        code, payload = validator_payload(spec)
        counts = label_counts(payload)
        assert code == 1, (
            "a bare N/A claims 'no load-bearing decision' without the per-trigger justification, so "
            f"it is treated as a missing record; counts={counts!r}"
        )
        assert counts["dtr-section-missing"] == 1, (
            f"the bare N/A must be counted once as a missing record; counts={counts!r}"
        )
        assert sum(counts.values()) == 1, (
            f"one root cause, one finding; counts={counts!r}"
        )
        assert payload["scanned"]["records"] == 0, (
            f"a bare N/A still carries no record; scanned={payload['scanned']!r}"
        )

    # --- D-2 (SC-003 run 2) ------------------------------------------------

    def test_d2_removing_the_section_reports_exactly_one_missing_section(self, tmp_path):
        # The same fixture, now carrying a load-bearing decision (rollback requires a migration)
        # whose record section is gone: fail-closed, the missing section is the single finding.
        plan_text = CHANNEL_PLAN_HEAD + CHANNEL_PLAN_TAIL
        assert "## Decision Tensions" not in plan_text, (
            "D-2's whole point is the removed section"
        )
        spec = write_channel_spec(tmp_path / "d2-section-removed", plan_text)
        code, payload = validator_payload(spec)
        counts = label_counts(payload)
        assert code == 1, f"D-2: a missing section must exit 1; counts={counts!r}"
        assert counts["dtr-section-missing"] == 1, (
            f"D-2: exactly one dtr-section-missing is reachable here; counts={counts!r}"
        )
        assert counts["dtr-anchor"] == 0, (
            "D-2: the anchor assertion is suppressed when the section is missing — the three-line "
            f"adjacency necessarily reds, and one root cause is counted once; counts={counts!r}"
        )
        assert sum(counts.values()) == 1, (
            f"D-2: 'exactly 1 HIGH' must hold, not 'at least 1'; counts={counts!r}"
        )

        snapshot = write_sc003_snapshot(
            "D-2-section-removed",
            "trivial plan plus one irreversible decision (rollback requires a migration), "
            "compliant N/A section removed",
            spec, code, payload,
        )
        assert snapshot.is_file(), "D-2's SC-003 snapshot must be archived"

    # --- D-3 (SC-003 run 3) ------------------------------------------------

    def test_d3_writing_a_compliant_record_returns_to_zero(self, tmp_path):
        # The repair path: one compliant record written where the N/A block stood.
        plan_text = channel_plan(CHANNEL_RECORD)
        assert "N/A" not in h2_section(plan_text, "## Decision Tensions"), (
            "D-3 replaces the N/A block with a record; the two are mutually exclusive"
        )
        spec = write_channel_spec(tmp_path / "d3-compliant-record", plan_text)
        code, payload = validator_payload(spec)
        counts = label_counts(payload)
        assert payload["scanned"]["records"] == 1, (
            f"D-3: the repair writes exactly one record; scanned={payload['scanned']!r}"
        )
        assert code == 0, f"D-3: a compliant record must exit 0; counts={counts!r}"
        assert set(counts.values()) == {0}, (
            f"D-3: the repair returns to zero HIGH; counts={counts!r}"
        )

        snapshot = write_sc003_snapshot(
            "D-3-compliant-record",
            "same fixture with one compliant T-001 record written in place of the N/A block",
            spec, code, payload,
        )
        assert snapshot.is_file(), "D-3's SC-003 snapshot must be archived"

        # The missing-measurement-source branch is mechanical on the record count: with one record
        # present, that record fails mapping; a compliant N/A (zero records) would not run mapping.
        no_sources = write_channel_spec(
            tmp_path / "d3-no-sources", plan_text, CHANNEL_REQUIREMENTS_NO_SOURCES
        )
        code_ns, payload_ns = validator_payload(no_sources)
        counts_ns = label_counts(payload_ns)
        assert code_ns == 1, "D-3: records without a declared source must fail mapping"
        assert counts_ns["expected-sacrifice-unmapped"] == payload_ns["scanned"]["records"], (
            "D-3: the branch is per record, not per plan; "
            f"counts={counts_ns!r} scanned={payload_ns['scanned']!r}"
        )


# --------------------------------------------------------------------------- #
# Scenario E — ADR reference slot and the dangling link (T019)
# --------------------------------------------------------------------------- #

ADR_TEMPLATE = ROOT / "docs" / "decisions" / "template.md"
ADR_ALTERNATIVES = "## Alternatives"

# The six record fields (plus the two pole lines) that the ADR slot MUST NOT reproduce: the ADR
# points at the record, the record owns its fields.
RECORD_FIELD_LINE_RE = re.compile(
    r"^\s*[-*]\s+\*\*(decision|antithesis|binding_constraints|discriminating_evidence|"
    r"expected_sacrifice|revision_trigger|pole_a|pole_b)\*\*\s*:"
)


def validator_module():
    """The validator imported as a library — the record index is its exported surface (C-2)."""
    spec = importlib.util.spec_from_file_location("_dt_validator_for_adr", VALIDATOR)
    assert spec is not None and spec.loader is not None, f"cannot import {VALIDATOR}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestScenarioEADRReferenceSlot:
    """US5: the plan, the ADR and the measurement source reach each other and copy nothing.

    Contract traceability: ``contracts/adr-reference.md`` C-1 (the slot) and C-2 (a dangling
    reference is an error). C-2's call surface is declared: this class is the ONLY caller, and it
    resolves the reference by importing the validator's ``index_records`` as a library call — the
    feature adds no command and no second parser, and the analyze channel never scans
    ``docs/decisions/``.
    """

    # --- C-1 --------------------------------------------------------------

    def test_adr_alternatives_carries_tension_slot(self):
        template = read(ADR_TEMPLATE)
        section = h2_section(template, ADR_ALTERNATIVES)
        joined = norm(section)

        assert "tension_id" in section, (
            "C-1: `## Alternatives` must carry a `tension_id` reference slot"
        )
        assert "T-NNN" in section, (
            "C-1: the slot must be typed to the `T-NNN` record identifier"
        )
        assert "plan.md" in section, (
            "C-1: the slot must point at the record in the same feature's plan"
        )
        assert "无承重张力记录" in section, (
            "C-1: a decision without a load-bearing record must say so explicitly — "
            "an empty slot is indistinguishable from a slot nobody examined"
        )
        assert ("判定结论" in joined) or ("threshold verdict" in joined), (
            "C-1: the no-record disposition must require the threshold verdict, not just the phrase"
        )

        # No field content is copied: the section may not carry the record's field lines.
        copied = [line for line in section.splitlines() if RECORD_FIELD_LINE_RE.match(line)]
        assert copied == [], (
            f"C-1: the ADR slot must not reproduce any record field; copied lines={copied!r}"
        )

    # --- C-2 --------------------------------------------------------------

    def test_dangling_tension_id_is_an_error(self, tmp_path):
        module = validator_module()
        assert callable(getattr(module, "index_records", None)), (
            "C-2: the validator must export its record-index function for the link check; "
            "a second parser would be a second source of truth"
        )

        # The fixture pair: one plan carrying `T-001`, one ADR fragment pointing at `T-007`.
        fixture = tmp_path / "adr-link"
        fixture.mkdir(parents=True, exist_ok=True)
        plan_text = channel_plan(CHANNEL_RECORD)
        (fixture / "plan.md").write_text(plan_text, encoding="utf-8")
        (fixture / "requirements.md").write_text(CHANNEL_REQUIREMENTS, encoding="utf-8")
        adr_text = (
            "# ADR-0001: fixture\n\n"
            "- **Status:** Proposed\n"
            "- **Date:** 2026-10-29\n\n"
            "## Alternatives\n\n"
            "- **tension_id:** `T-007` — deliberately unresolvable in this fixture plan.\n"
        )
        (fixture / "adr.md").write_text(adr_text, encoding="utf-8")

        index = module.index_records((fixture / "plan.md").read_text(encoding="utf-8"))
        assert "T-001" in index, (
            f"C-2: the fixture plan's record must resolve; index keys={sorted(index)}"
        )
        dangling = re.search(r"`(T-\d{3})`", adr_text).group(1)
        assert dangling not in index, (
            "C-2: the fixture's reference must not resolve, otherwise it cannot discriminate"
        )
        # The broken link is an error, not a hint: the same call answers both directions.
        broken = [identifier for identifier in (dangling,) if identifier not in index]
        assert broken == [dangling], (
            "C-2: an unresolvable `tension_id` must be reported as a broken link, never passed"
        )

        # The record's cost still resolves to a declared measurement source: the pair exercises the
        # link only, not the mapping rule.
        code, counts = verdict_of(fixture)
        assert code == 0, f"C-2: the fixture plan itself is compliant; counts={counts!r}"
        assert counts["expected-sacrifice-unmapped"] == 0, (
            f"C-2: every record's expected_sacrifice must resolve; counts={counts!r}"
        )

        # No new command surface: the validator's CLI stays `--spec` / `--json`.
        proc = subprocess.run(
            [sys.executable, str(VALIDATOR), "--help"], capture_output=True, text=True,
        )
        assert proc.returncode == 0, proc.stderr
        assert "--spec" in proc.stdout and "--json" in proc.stdout, (
            f"C-2: the CLI contract changed: {proc.stdout!r}"
        )
        assert "adr" not in proc.stdout.lower(), (
            "C-2: a link-check command was added; the call surface is the contract test only"
        )


# --------------------------------------------------------------------------- #
# Scenario F — terminology zero-hit guard (T021, post-implementation guard)
# --------------------------------------------------------------------------- #
#
# A post-implementation guard, not a red-first slice: it asserts a before/after property of a
# tree whose sources were finished in US1–US5. The judgement is a count over three trees plus a
# positive control, so an emptied A3 list cannot turn the zero-hit scan vacuously green.

DISTRIBUTION_TREES = ("shared", "templates", "skills")
FEATURE_DETAIL = ROOT / ".specify" / "memory" / "features" / "076.md"
REQUIREMENTS = SPEC_DIR / "requirements.md"

# The alias list is PARSED out of the spec's A3 (the owner). This literal tuple is the drift
# guard a test is allowed to carry: if A3 is renamed, reworded or emptied, the parse or this
# comparison reds instead of the scan silently having nothing to look for.
EXPECTED_ALIASES = ("矛盾论", "主要矛盾", "矛盾的主要方面", "对抗性矛盾", "矛盾转化条件")
A3_MARKER = "**A3（术语裁决）**"
A3_LIST_INTRO = "尤其 MUST NOT 进入任何用户可见正文或分发面："


def a3_line() -> str:
    line = next(
        (raw for raw in read(REQUIREMENTS).splitlines() if A3_MARKER in raw),
        None,
    )
    assert line is not None, "the spec lost its § Assumptions A3 terminology ruling"
    return line


def a3_aliases() -> tuple[str, ...]:
    """The five internal aliases, read from the sentence that enumerates them."""
    line = a3_line()
    index = line.find(A3_LIST_INTRO)
    assert index != -1, (
        "A3 no longer names the alias list with its introducer; the positive control cannot read it"
    )
    tail = line[index + len(A3_LIST_INTRO):].split("。")[0]
    return tuple(item.strip() for item in tail.split("、") if item.strip())


def distribution_files() -> list[Path]:
    """Every file under the three distribution trees (junk dirs excluded, nothing else)."""
    files: list[Path] = []
    for tree in DISTRIBUTION_TREES:
        root = ROOT / tree
        assert root.is_dir(), f"missing distribution tree: {root}"
        files.extend(
            path for path in sorted(root.rglob("*"))
            if path.is_file() and "__pycache__" not in path.parts
        )
    return files


def alias_hits(aliases) -> dict[str, list[str]]:
    """alias -> repo-relative paths that mention it (one pass over the scanned file set)."""
    hits: dict[str, list[str]] = {alias: [] for alias in aliases}
    for path in distribution_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for alias in aliases:
            if alias in text:
                hits[alias].append(path.relative_to(ROOT).as_posix())
    return hits


def inside_distribution_tree(path: Path) -> bool:
    for tree in DISTRIBUTION_TREES:
        try:
            path.relative_to(ROOT / tree)
        except ValueError:
            continue
        return True
    return False


class TestScenarioFTerminologyZeroHit:
    """FR-024 / SC-007: engineering words only on every distribution surface.

    The whitepaper aliases live in exactly two places, both OUTSIDE the three trees
    (``requirements.md`` § Assumptions A3 and the feature detail's § 附 mapping table); the
    owner sits inside ``shared/`` and is therefore NOT whitelisted — it must read in
    engineering words like every other distribution file.
    """

    # --- positive control ---------------------------------------------------

    def test_a3_alias_list_still_exists(self):
        aliases = a3_aliases()
        assert aliases == EXPECTED_ALIASES, (
            "the positive control failed: A3's alias list was renamed, reordered or emptied "
            f"({aliases!r}); the zero-hit scan below would otherwise look for nothing"
        )
        assert len(set(aliases)) == len(aliases) == 5, (
            f"A3 must enumerate five distinct aliases; got {aliases!r}"
        )
        # The ruling still declares the whitelist as exactly two places and names the second.
        line = a3_line()
        assert "白名单只有两处" in line, (
            "A3 must keep declaring a two-place whitelist; a widened whitelist is a contract "
            "change, not a wording tweak"
        )
        assert ".specify/memory/features/076.md" in line, (
            "A3 must keep naming the feature-detail appendix as the second whitelisted place"
        )

    # --- zero hits ----------------------------------------------------------

    def test_distribution_trees_carry_zero_internal_aliases(self):
        aliases = a3_aliases()
        scanned = distribution_files()
        assert len(scanned) > 100, (
            f"the scan is vacuous: only {len(scanned)} files found under the three trees"
        )
        assert OWNER in scanned, (
            "the DTR owner must be inside the scanned surface: it is a distribution file and "
            "is explicitly NOT whitelisted"
        )

        hits = alias_hits(aliases)
        offenders = {alias: paths for alias, paths in hits.items() if paths}
        assert offenders == {}, (
            f"internal aliases leaked onto a distribution surface: {offenders!r}"
        )
        assert sum(len(paths) for paths in hits.values()) == 0, (
            f"SC-007 counts must be zero across shared/ templates/ skills/; got {hits!r}"
        )

    # --- whitelist boundary -------------------------------------------------

    def test_whitelist_is_two_places_outside_the_distribution_trees(self):
        for path in (REQUIREMENTS, FEATURE_DETAIL):
            assert path.is_file(), f"whitelisted place is missing: {path}"
            assert not inside_distribution_tree(path), (
                f"{path.relative_to(ROOT)} is inside a distribution tree, so it cannot be a "
                "whitelisted exception — the trees must be clean without exceptions"
            )

        # The whitelist is genuinely used, not merely allowed: the mapping table still carries
        # the aliases, which is why the two places are named in A3 at all. Four are spelled
        # literally; the fifth (`对抗性矛盾`) is carried as its concept pair 「对抗性 / 非对抗性」,
        # so the assertion is the literal four plus that pair.
        detail = read(FEATURE_DETAIL)
        appendix = detail.split("## 附", 1)
        assert len(appendix) == 2, "the feature detail lost its § 附 alias mapping appendix"
        used = [alias for alias in EXPECTED_ALIASES if alias in appendix[1]]
        assert len(used) >= 4, (
            f"the appendix must still carry the alias mapping (the whitelist's only use); "
            f"found {used!r}"
        )
        assert "对抗性" in appendix[1], (
            "the appendix must still carry the adversarial concept line 「对抗性 / 非对抗性」"
        )


# --------------------------------------------------------------------------- #
# Scenario G — closed-set delta guard (T021, post-implementation guard)
# --------------------------------------------------------------------------- #
#
# FR-014 / FR-026 / SC-008. Both touched closed-set owners are judged as an only-add
# containment claim against commit ``ac63fe8c``: the comparison unit is the paragraph, the
# allowed delta set is 「the new paragraph(s) + the count line the new channel forces」, and
# everything outside it must be byte-identical. Item-level assertions compare counts against
# the baseline, never against prose.

QUARTET_SUBSECTION_HEADING = "### 产出形态:四元组(封闭四字段)"
CRITIQUE_REJECTION_HEADING = "### 拒绝形态(封闭清单,命中即拒)"
CRITIQUE_BOUNDARY_HEADING = "## 边界(本纪律不做什么)"
CRITIQUE_CONSUMER_HEADING = "## 消费者清单"
DETECTION_DO_NOT_FLAG_HEADING = (
    "## DO-NOT-FLAG list (noise control — do not report these at any severity)"
)
SEVERITY_DOMAIN = ("CRITICAL", "HIGH", "MEDIUM", "LOW")


def h3_section_lines(text: str, heading: str) -> list[str]:
    """An H3 section's lines, up to the next H3 or H2 (trailing blank lines trimmed)."""
    lines = text.splitlines()
    assert heading in lines, f"missing section: {heading}"
    start = lines.index(heading)
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## ") or lines[index].startswith("### "):
            end = index
            break
    body = lines[start:end]
    while body and not body[-1].strip():
        body.pop()
    return body


def quartet_section_lines() -> list[str]:
    """The quartet subsection as written in the owner — the declared added paragraph.

    The trailing blank line that separates it from the next H2 is part of the added block, so
    it is kept: the delta is compared verbatim, and trimming it here would hide a real difference.
    """
    lines = read(CRITIQUE).splitlines()
    assert QUARTET_SUBSECTION_HEADING in lines, (
        f"the quartet subsection is missing: {QUARTET_SUBSECTION_HEADING!r}"
    )
    start = lines.index(QUARTET_SUBSECTION_HEADING)
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return lines[start:end]


def bullet_items(text: str, heading: str) -> list[str]:
    """Top-level ``- `` bullets of one H2/H3 section (the item-count surface)."""
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:  # pragma: no cover - reported as a readable failure
        raise AssertionError(f"missing section: {heading}")
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## ") or lines[index].startswith("### "):
            end = index
            break
    return [line for line in lines[start + 1:end] if line.startswith("- ")]


def consumer_rows(text: str, heading: str) -> list[str]:
    """Data rows of the first table inside a section (header and separator dropped)."""
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:  # pragma: no cover - reported as a readable failure
        raise AssertionError(f"missing section: {heading}")
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## ") or lines[index].startswith("### "):
            end = index
            break
    rows = [line for line in lines[start + 1:end] if line.strip().startswith("|")]
    return [row for row in rows if "---" not in row][1:]


def channel_letters(text: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"(?m)^### ([A-Z])\. ", text)]


class TestScenarioGClosedSetDelta:
    """FR-026 / SC-008: the two touched closed-set owners only grew.

    Delta equality (not "no removals") is the criterion: a rewrite shows up as a removed plus
    an added line and would silently pass a removals-only check. The enumerated delta is
    compared to the declared allowed set verbatim, so only the count line and the new
    paragraph(s) can move.
    """

    # --- detection-and-severity.md -----------------------------------------

    def test_detection_and_severity_delta_is_the_declared_allowed_set(self):
        removed, added = diff_lines(ANALYZE_DETECTION)

        # Exactly one rewritten line: the pass count heading the new channel forces to change.
        assert removed == ["## The seven passes"], (
            "the count line is the ONLY deleted or rewritten line this file may carry; "
            f"removed {removed!r}"
        )
        assert added == ["## The eight passes"] + channel_section_lines(), (
            "every added line must belong to the new channel section or be the count heading; "
            f"outside-the-set additions: {[line for line in added if line not in ['## The eight passes'] + channel_section_lines()]!r}"
        )

        # Structural invariants inside the delta, re-read on the current file: the channel
        # letters stay unique and the defect table keeps three HIGH rows.
        current = read(ANALYZE_DETECTION)
        letters = channel_letters(current)
        assert len(set(letters)) == len(letters), f"a channel letter repeats: {letters!r}"
        assert set(channel_letters(git_show(ANALYZE_DETECTION))) <= set(letters), (
            "a baseline pass letter was removed or renamed"
        )
        rows = defect_table(channel_section())
        assert len(rows) == 3 and all(row[2] == "HIGH" for row in rows), (
            f"the three defect classes must stay HIGH; rows={rows!r}"
        )

    # --- critique-and-self-critique.md -------------------------------------

    def test_critique_delta_is_the_declared_allowed_set(self):
        removed, added = diff_lines(CRITIQUE)
        allowed_added = quartet_section_lines()

        assert removed == [], (
            "the quartet rides BELOW the one-line falsification paragraph: zero deleted or "
            f"rewritten lines are allowed in this file; removed {removed!r}"
        )
        assert added == allowed_added, (
            "the only added paragraph must be the quartet subsection; outside-the-set "
            f"additions: {[line for line in added if line not in allowed_added]!r}"
        )

        # Structural invariants inside the delta: the four literal keys are each written once,
        # and the parent paragraph is byte-identical to the baseline (it was never rewritten).
        section = "\n".join(quartet_section_lines())
        for key in QUARTET_KEYS:
            assert section.count(f"`{key}`") == 1, (
                f"the quartet subsection must name `{key}` exactly once; "
                f"count={section.count(f'`{key}`')}"
            )
        baseline_parent = h2_section(git_show(CRITIQUE), QUARTET_PARENT_HEADING)
        live_parent = h2_section(read(CRITIQUE), QUARTET_PARENT_HEADING)
        parent_lines = [line for line in baseline_parent.splitlines()]
        assert all(line in live_parent.splitlines() for line in parent_lines), (
            "the pre-existing 「每个提案一条证伪尝试」 paragraph must survive verbatim"
        )

    # --- item counts never fall below the baseline -------------------------

    def test_item_counts_do_not_fall_below_baseline(self):
        critique_base = git_show(CRITIQUE)
        critique_now = read(CRITIQUE)

        for heading in (CRITIQUE_REJECTION_HEADING, CRITIQUE_BOUNDARY_HEADING):
            base_items = bullet_items(critique_base, heading)
            live_items = bullet_items(critique_now, heading)
            assert len(live_items) >= len(base_items), (
                f"{heading}: item count fell from {len(base_items)} to {len(live_items)}"
            )
            assert live_items[:len(base_items)] == base_items, (
                f"{heading}: an existing item was reworded or reordered; the closed set grows "
                "only by appending"
            )

        base_rows = consumer_rows(critique_base, CRITIQUE_CONSUMER_HEADING)
        live_rows = consumer_rows(critique_now, CRITIQUE_CONSUMER_HEADING)
        assert len(live_rows) >= len(base_rows), (
            f"the consumer list fell from {len(base_rows)} to {len(live_rows)} rows"
        )
        assert live_rows[:len(base_rows)] == base_rows, (
            "the consumer list must grow only by appending; an existing row changed"
        )

        detection_base = git_show(ANALYZE_DETECTION)
        detection_now = read(ANALYZE_DETECTION)
        base_dnf = bullet_items(detection_base, DETECTION_DO_NOT_FLAG_HEADING)
        live_dnf = bullet_items(detection_now, DETECTION_DO_NOT_FLAG_HEADING)
        assert len(live_dnf) >= len(base_dnf), (
            f"the DO-NOT-FLAG list fell from {len(base_dnf)} to {len(live_dnf)} items"
        )
        for value in SEVERITY_DOMAIN:
            assert f"**{value}**" in detection_now, (
                f"the severity value domain lost {value!r}; the four-value domain is a "
                "structural invariant of the closed set"
            )
        assert len(channel_letters(detection_now)) >= len(channel_letters(detection_base)), (
            "a pass section was deleted from the detection owner"
        )
