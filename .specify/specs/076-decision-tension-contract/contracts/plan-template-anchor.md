# Contract: 计划模板锚点（plan-template-anchor）

**Feature**: 076-decision-tension-contract → Feature 076 决策反题与反指标契约（Decision Tension Record）
**FR 覆盖**: FR-008、FR-009
**载体**: `templates/plan-template.md`、`.specify/templates/plan-template.md`（镜像）

本契约钉住章节的存在、位置与内容形态。三条一起才构成「可判定的位置约束」：只有存在性没有
位置，章节可以漂到任何地方；只有位置没有内容边界，模板会变成 owner 的第二份副本。

## 条款

- **C-1** (section exists at the anchor): the template MUST contain a `## Decision Tensions` section whose position is asserted on the `^## ` heading sequence — extracting every level-2 heading and requiring the three consecutive entries `## Constitution Check` → `## Decision Tensions` → `## Project Structure`; the phrase-level reading «after Constitution Check and before Complexity Tracking» MUST NOT be used as the anchor because it admits two satisfying positions. (FR-008)
- **C-2** (record carrier and N/A rule): each record MUST be carried by a sub-section whose heading begins with `T-NNN`; when and only when the plan has no load-bearing decision the section MUST contain the literal `N/A` plus one line per trigger explaining why that trigger does not hold, and the section MUST NOT be deleted or left empty. (FR-008)
- **C-3** (pointer, not a copy): the section MUST consist of one pointer to `shared/guidelines/decision-tension.md` plus the field-name list, and MUST NOT reproduce the owner's admissibility table, rejection list or threshold table; the guarding contract test MUST assert four things — section presence, the heading-sequence adjacency of C-1, that the pointer path resolves to an existing file, and that no owner table row is reproduced verbatim in the template. (FR-009)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-1 | FR-008 | test_template_section_adjacent_to_constitution_check |
| C-2 | FR-008 | test_template_carrier_and_na_rule |
| C-3 | FR-009 | test_template_is_pointer_not_copy_and_path_resolves |

## FR 覆盖核对

- FR-008、FR-009 由本文件 C-1…C-3 承接。
- 计划**实例**侧的同名断言由 `validator.md` 的 `dtr-anchor` 标签负责，两处断言同一形态、不同工件。
