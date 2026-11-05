# Specification Quality Checklist: Harness 三重结构（markdown + yaml + script）

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-11-05
**Feature**: `.specify/specs/084-harness-triple-structure/requirements.md`

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

- **Deterministic checker（本清单所有计数的唯一权威）**：`python3 .specify/scripts/python/validate-requirements.py .specify/specs/084-harness-triple-structure/requirements.md` → `status: ok`；`id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id` / `path-marker` 六项全 pass；`scanned: 282 lines, 25 definition rows, 14 shared strings`；`0 error(s), 0 warning(s)`；exit 0。逐字输出存于 `test-evidence/validate-requirements.txt`（clarify 复跑刷新；行数 250 → 282 是本轮写回，定义行与 STR 计数不变）。本清单不手抄计数——上面这串数字是从该文件抄来的唯一处，改规格即重跑。25 个定义行 = 19 条 FR + 6 条 SC。
- **类别读取（一次，复用于全阶段判定）**：`python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:084-harness-triple-structure"` → `flow_class: execution` / `flow_type: -` / `source: declaration` / `marker: null` / exit 0；逐字输出存于 `test-evidence/flow-class-lookup.txt`。`source=declaration` 证明类别由本文件头部声明行解析，不依赖任何注册表行。
- **`Path` 标注（081 FR-001 的格式契约）**：6 条 SC 各在一行内、作为该行最后一个 token 携带 `**Path**: …`；两条 `final`（SC-001、SC-002）覆盖本特性的主旅程——「一条事实只有一个机器读得到的定义点」与「三层完整性达标」；其余四条为 supporting。`execution` 类特性至少一条 `final` 的下限由 `path-marker` 判项机械确认。
- **三处「实现细节」判项的判定依据（disclosed，非同义反复）**：本特性的**主体就是载体的分层本身**，因此目录路径、脚本名、声明键名与原因字面量是用户指令「markdown + yaml + script 三重结构」逐字给定的**验收面**，不是作者擅自选定的 HOW；规格里没有固定数据结构、算法或第三方库选择（唯一的实现约束 `stdlib-only`／「不新增 YAML 库」来自仓内既有先例与该特性要防的失效，见 A5）。据此 `No implementation details` 与 `No implementation details leak` 判通过，判据与理由同处可见，复核者可在这两句上反驳。
- **读者基准（`Written for non-technical stakeholders`）的判定依据**：本工件属 `.specify/shared/guidelines/user-facing-comprehension.md` § 面向用户界面类 的第 ⑦ 类，基准读者是「未在本会话打开过本仓、但具备本领域知识的人」。工件中的 `FR-NNN` / `SC-NNN`、`[[STR-NNN]]`、路径与命令均属该 owner 白名单（读者需逐字键入或复制的标识符）；产物指向一律以路径引用而非复述其内容。据此判通过。
- **包含性声明（closed-set claims）的五要件对位**：本特性的三条 JSON「封闭集」主张分别落在 SC-001（候选处置覆盖）、SC-002（三层完整性）、SC-006（非目标未越界）。共同要件按 owner 逐条落位——**基线参照物**：候选屏幕 S 在实现树上重算（不是上一轮自己），SC-006 的基线是实现起始提交；**比较单元**：流程单元（身份 = markdown 载体路径）与「事实声明条数」，明示不使用「其余流程」「未受影响的文件」这类未定义聚合词；**允许差异集来源**：机械派生（S 的重算结果与 `facts/` 反投影），不手写清单；**补集断言与结构不变量**：候选集外 MUST 无孤立声明文件（补集侧），候选集内 MUST 恰一条处置记录且通过 schema 与子集校验（结构侧）；**未定义聚合词清零**：全文未出现「其余」「等等」「相关流程」承载验收语义。SC-001 另附确定性（两次运行逐字节一致）与包含性分开声明，符合 owner「两类断言必须分开」。
- **范围边界为什么是可判定的（本特性的核心裁决）**：范围不用流程清单定义，而用两条合取判据（FR-002 的 D1 资产面 ∧ D2 机器面）加一条机械候选屏幕（FR-004 的 S）。因此「哪些流程涉及 harness」不靠枚举权威，而靠「跑一遍 S、看每个候选单元的处置」——`§ Initial Scope Adjudication` 的 18 行是**日期基线**（每一行都指到仓内证据：`feedback-utils.py` 的阈值常量与 `feedback-step.md` 的同一数值、`evidence-utils.py` 的七态与 `better-harness.md` 的重列、`flow-class-check.py` 的取值元组与 `flow-class-definitions.md` 的取值域），不是范围 owner。该表存在的意义是证明判据能判，不是替代判据。
- **clarify 已收口的三项（2026-11-05，本清单只记结论，判据与证据在规格内）**：① `Related Feature` 已绑定 **Feature 084**（`create-requirements` 保留 `Need clarification`、由 `/speckit.clarify` 按 `.specify/shared/workflow/feature-integration.md` § Feature Binding Rules 落定；候选复核表在规格 § Related Feature）；② A8 已裁定并**拆成两条相反结论**——`Path` 取值域不越界（保留 in-scope，FR-018 增补 `acceptance-hardening.md` 并附「081 测试断言零改动」）、六个检查项标签集越界（不迁，N7 + 三个树内锚点）；③ A9 与 FR-011 的移交已收口成可判定形态：分发／证据／归属三条义务在 FR-013、SC-005、`RS-003` 内可判，留给 plan 的只剩两份**清单产物**本身（首批迁移名单、`specify init` 资产名册与升级动作），判定点是它们出现在 plan 交付物里。规格内已无不可判定的「待定」。
- **零澄清标记**：`marker-count` pass（0）。10 条裁决记在 `## Assumptions`（A1–A10）；其中 A2（归 yaml 的判据）、A3（范围判据与候选屏幕）、A5（既有解析器不重构）、A7（目标锚点自身也要分层）是四个真正做了选择的点，clarify 可推翻并触发重判。
- **本清单不是门禁输入**：它记录的是 clarify / plan **之前**的规格状态；后续任一阶段的写回都可能移动行号与计数，此后的权威是该次运行的 checker 输出，不是本文件。
