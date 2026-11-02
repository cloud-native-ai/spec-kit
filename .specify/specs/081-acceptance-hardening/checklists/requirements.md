# Specification Quality Checklist: Stricter Acceptance & Artifact Review（更严格的验收与产物审查）

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-11-01
**Feature**: `.specify/specs/081-acceptance-hardening/requirements.md`

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Stability / containment claims name a baseline referent and a derivable allowed-delta set (owner: `.specify/shared/guidelines/closed-set-claims.md`)
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

- **Deterministic checker（所有计数的唯一权威）**：`python3 .specify/scripts/python/validate-requirements.py .specify/specs/081-acceptance-hardening/requirements.md` → `status: ok`；`id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id` 全 pass；`scanned: 232 lines, 34 definition rows, 17 shared strings`；`0 error(s), 0 warning(s)`；exit 0。逐字输出存于 `test-evidence/validate-requirements.txt`。本清单不手抄计数。34 个定义行 = 25 条 FR + 9 条 SC；两个分项由下面两条门的程序输出交叉确认，不是人工拆分。
- **Decomposition gate（FR 上限）**：`decomposition-check.py --mode plan` → `decision=proceed`，`fr_count=25 ≤ fr_ceiling=30`；exit 0。输出存于 `test-evidence/decomposition-check.json`。故 § Decomposition & Ceiling 断言「不需要切成 081a–081d」有程序读数支撑，081a–081d 只作为 plan 阶段可选边界保留。
- **Pre-analyze gate（requirements 阶段）**：`pre-analyze-check.py --stage requirements` → `decision=pass errors=0 advisories=0 waived=0`，`fr=25 sc=9 clauses=0`；exit 0。输出存于 `test-evidence/pre-analyze-check.{txt,json}`。
- **三处「实现细节」判项的判定依据（disclosed，非同义反复）**：本特性的**主体就是框架自身的门禁机制**，因此脚本名、模板路径、状态值与原因标签是用户指令逐字给定的**验收面**，不是作者擅自选定的 HOW；规格里没有固定数据结构、算法或第三方库选择（唯一的实现约束 `stdlib-only` 与「不含模型判断」来自既有的 Program-First 纪律与该特性要防的失效）。据此 `No implementation details` 与 `No implementation details leak` 判通过，判据与理由同处可见，复核者可在此一句上反驳。
- **读者基准（`Written for non-technical stakeholders`）的判定依据**：本工件属 `.specify/shared/guidelines/user-facing-comprehension.md` § 面向用户界面类 的第 ⑦ 类，基准读者是「未在本会话打开过本仓、但具备本领域知识的人」。工件中的 `FR-NNN` / `SC-NNN` 与路径、命令均属该 owner 白名单第 3 条（读者需逐字键入或复制的标识符）与第 5 条（同处具名的短形式）；产物指向一律以路径引用而非复述。据此判通过。
- **包含性声明（closed-set claims）**：SC-009 ② 现按 owner 五要件写足——基线参照物（实现起始提交上采集的失败用例 id 集合，存 `<spec-dir>/baseline-failed.txt`）、比较单元（失败用例 id 集合，明示不用「全仓测试」这类未定义聚合词）、允许差异集来源（空集，机械可得）、补集与不变量（`head − baseline` 必须为空，`baseline − head` 必须逐条列为已修复）、未定义聚合词清零。SC-009 ④ 的 schema 唯一性由「Shared Strings 表 + owner 章节目录机械导出字面量 × `templates/` 与 `shared/` 两类路径」派生，并用守卫测试把真实命中枚举为与豁免清单相等。
- **待 clarify 落定的一项**：`Related Feature` 保持 `Need clarification`（`create-requirements` 不自行绑定，见 `.specify/shared/workflow/feature-integration.md` § Feature Binding Rules）。这不构成规格缺陷；`/speckit.clarify` 须在 plan 之前完成绑定。
- **零澄清标记**：`marker-count` pass（0）。10 条缺省裁决记在 `## Assumptions`（A1–A10），其中 A3（review 组合改三段）、A4（`Path` 行内标注）、A6（线状态集扩张）是三个真正做了选择的点，clarify 阶段可推翻。
