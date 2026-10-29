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

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

OWNER = ROOT / "shared" / "guidelines" / "decision-tension.md"
TEMPLATE = ROOT / "templates" / "plan-template.md"

RUBRIC = ROOT / "shared" / "guidelines" / "task-complexity-rubric.md"
DERIVATION = ROOT / "shared" / "definitions" / "derivation-definitions.md"
FAST_FAIL = ROOT / "shared" / "guidelines" / "fast-fail.md"
CRITIQUE = ROOT / "shared" / "guidelines" / "critique-and-self-critique.md"

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
