# Specification Quality Checklist: 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-10-30
**Feature**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/requirements.md`

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

- **Deterministic checker (authority for every count below)**: `python3 scripts/python/validate-requirements.py .specify/specs/077-doc-sdd-integration/requirements.md` → `status: ok`；五项命题全 pass（`id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id`）；scanned 239 lines、33 definition rows（25 FR + 8 SC）、2 shared strings；`0 error(s), 0 warning(s)`；exit 0。逐字输出存于 `.specify/specs/077-doc-sdd-integration/test-evidence/validate-requirements.txt`。上方每一条戳记均派生自该次运行，非手打。
- **Decomposition gate**: `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/077-doc-sdd-integration/requirements.md` → `decision=proceed`、`fr_count=25 ≤ fr_ceiling=30`（`task_count=null` 属 plan 前常态）；exit 0。输出存于 `test-evidence/decomposition-check.json`。FR 预算 25，未触发拆分。
- **Pre-analyze gate (requirements stage)**: `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/077-doc-sdd-integration --stage requirements --repo .` → `decision=pass errors=0 advisories=0 waived=0`（`fr=25 / sc=8`）；exit 0。输出存于 `test-evidence/pre-analyze-check.txt`。零 advisory 的原因：本规格引用的 owner 文件（`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`、`scripts/python/flow-class-check.py`、`skills/external/sdd-loop-driver/`）全部实存。
- **Requirements testable and unambiguous**: 每条 FR 都点名可判定面——解析记录字段与退出码、阶段算子结果的覆盖与阻断、章节标题两向比对、证据三件套的成组性、owner 唯一性、槽位围栏行、命令/依赖/进程清单差异——而不是「更清晰」「更严密」这类形容词。四处需要判断的要求（类别是否由介质推断、表达类是否继承代码算子、结构违规的两向判定、跨线泄漏）各自写明了可复现的判定方式。
- **Containment claims**: 三处「不回退 / 零新增」声明（FR-011 / FR-025 / FR-024）与两处零新增机制声明（FR-022 / SC-006）均点名基线参照物（提交 `c1cd4600`）、比较单位（逐阶段判定集合 / 命令清单 / 依赖与进程清单）、允许差异集（空集，或仅「是否含类别读取」一行）、补集断言（集合外新增 = 0）与集合内不变量，符合 `.specify/shared/guidelines/closed-set-claims.md`。
- **Implementation-specific references** are limited to named existing owners and delivery surfaces（`templates/commands/`、`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`、`scripts/python/flow-class-check.py`、`skills/external/sdd-loop-driver/`、`.specify/memory/features.md`），与既有框架规格（069 / 076）同口径：所有规范性 FR / SC 陈述都是行为性的，未引入语言、框架、运行时或外部 API。
- **Scope boundedness**: 九条显式排除项列于 `## Requirements` → 「显式排除项（Out of Scope）」，逐条可回溯到派发范围的排除清单（办公文档、站点构建与发布、重写 069 契约、类别自动推断、新建命令集、运行时/调度器/评分器、重写 058/067 既有规则、实现形式、客户项目具体文档）。
- **Assumptions / deviations recorded**: A1 编号依据（spec 最大目录 076 → 077；`Total Features` 是行数 72，与最大编号不一致属既有状态）；A2 类别当前按流程单元（79 单元、0 缺口、引擎只认两类键）；A3 接线面计数纠正（派发文本的「六个」与同句枚举的七个命令名不一致，以枚举为准并说明 clarify 不可排除）；A4 声明位置裁决（requirements 头部字段，五条理由；clarify 可推翻）；A5 声明单位 = 特性线（多切片各自声明）；A6 本特性自身类别 = `execution`；A7 脚手架偏差（仓库外调用以抑制切分支，stderr 留痕，分支未变）；A8 绑定时点偏离（按调用方要求在本阶段绑定）；A9 无新增持久编号；A10 术语 owner 归 069 与两份 owner 文档；A11 实现形制留待 plan。
- **Feature binding**: 绑定新建 **Feature 077**（`Draft`，2026-10-30 登记），并对 069 / 069a / 069b / 058 / 067 / 062 / 074 / 076 八项候选做 reuse-first 复核（表内七行，两个切片并作一行；表见 `## Related Feature`）。结论：069 拥有分类轴但不拥有阶段命令接线，且其 Out of Scope 显式推迟；058 / 067 持有驱动载体与既有规则但不持有「按类别切换门禁」这一能力（载体 ≠ 归属）。069 的 `Implemented` 状态 MUST NOT 回退，其正文 MUST NOT 被本特性改写。
- **No clarification markers**: `marker-count` 报 0 个活动标记；本可成为提问的开放点（声明位置、接线面计数、声明单位、自身类别）已按 § Assumptions 逐条裁决并记录，因此不阻塞 `/speckit.clarify` 或 `/speckit.plan`。
- **Known open points handed to clarify**: A4（声明位置）与 A3（接线面是否含 clarify）是**可推翻**的裁决；若 clarify 改判，受影响 FR 为 FR-001 / FR-008 / FR-023 与 Shared Strings 两行，须同批改写并重跑本清单背后的两次确定性检查。
