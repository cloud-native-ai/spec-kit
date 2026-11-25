# Requirements Specification: Decision Governance — AI Agent 决策项的文本、选项、归档、传递与两类强调（Decision Governance）

**Requirement Branch**: `107-decision-governance`
**Created**: 2026-11-25
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（修订 `shared/`、`templates/`、`skills/`、`agents/`、`scripts/`、`src/` 的作者，需要判定每条决策规则由谁拥有、哪个检查器判它、改了要迁移什么）与下游项目维护者（使用生成后的 `.specify/instructions.md` 与既有决策面的人，需要判定「一次决策该写什么、写去哪里、如何被审计」）
**Reading scenario**: 当需要判定「一个决策项的文本在各决策类别下必须包含什么」「一个选项集必须长什么样」「每个决策归档到哪个既有载体、由哪个单一所有者拥有每个字段」「一个决策如何从 superagent 完整传到 subagent 并让实施回执可追溯」「哪些规则是机器可判、哪些只能由评审承接」「如何落地、镜像与客户项目如何收到、哪些不兼容变更必须由迁移或确定性拒绝收口」时打开本规格，据 FR-001…FR-030 与 SC-001…SC-010 放行 `/speckit.clarify` 与后续规划
**Input**: User description: "前面中途插入的两个决策相关的instruction都来自于真实的生产环境, 决策对于AI agent使用过程中至关重要, 需要使用sdd-loop-driver技能专门针对 AI Agent的决策进行系统性优化,包括单不限于 决策文本规范, 选项规范, 每个决策都必须归档并可审计, 决策项的传递和实施(尤其是针对superagent-subagent架构, superagent决策+subgent实施), 另外需要注意的是: 决策包括人工交互式决策和AI自主决策, 这两类决策的核心考量不同,侧重点不同, 人工交互式决策注重可读性, AI自主决策注重严谨性."

**输入校正**：①「单不限于」按上下文读作「包括但不限于」；「subgent」读作 `subagent`；②「决策文本规范」读作**决策项（decision item）的描述文本契约**，不是只改 instruction 模板的一段话——instruction 中的两条生产规则只是最低门槛（A-8）；③「每个决策都必须归档并可审计」以 **Decision Producer Inventory（封闭清单）** 界定「决策」的外延：清单内的生产者在产出决策项时 MUST 留下可重建的决策记录，in-passing correction 不属于决策（按 `shared/guidelines/fast-fail.md` 的纠正/裁定判据），清单外的生产者若产出决策项即缺陷（A-5）；④「传递和实施」复用既有派发载荷通道与角色边契约（owner：`shared/definitions/superagent-definitions.md`），不新建传输机制（A-7）；⑤「人工交互式决策」= 由人持有的决策（交互式决策门、人工评审处置、人对选项的选择），「AI 自主决策」= 由 agent 在无用户在场时持有的决策（无人值守裁决、委派实施中的取舍）——分类看**持有者**而非表面介质（A-4）；⑥用户点名使用 sdd-loop-driver 技能，是该优化的**执行方式**（由本次 SDD 运行承担），不是产品需求；本规格交付的是框架能力。

## Related Feature *(mandatory)*

**Feature ID**: 107
**Feature Name**: Decision Governance（AI Agent 决策项治理）

## Overview

**问题**：决策在 AI agent 工作流中承重，但本仓的决策处理分散在多个互不引用的所有者上，没有任何一处契约回答同一组问题：

- `shared/guidelines/confirmation-gates.md`（149 行）管「是否向用户提问」与两轴分类（授权级别 × 影响范围），不规定决策项文本、选项集、归档形态或传递；
- `shared/guidelines/decision-tension.md`（116 行，Feature 076）管**承重技术取舍**的反题六字段（`T-NNN`），只承接「方向已选定之后的技术取舍」，不承接一般决策项；
- `.specify/register.md`（253 行）管持久编号的登记，不规定决策记录的字段；
- `shared/guidelines/fast-fail.md`（308 行）管运行中异常的纠正/裁定分流，不规定裁定之后的归档与传递；
- `shared/definitions/superagent-definitions.md`（126 行）管角色边、七字段下行与五要素上行，不含决策块；
- 检查点（`<spec-dir>/checkpoints/<NN>-<stage>.md`，仓内已有 125 个文件）、analyze 处置、review 发现处置、goal/anchor/team 决策、probe/feedback 处置、run determination 各自产出「像决策的东西」，但形态各异、无共同记录契约。作为真实语料：各 spec 的 `plan.md` 中已有 101 条 `T-NNN` 张力记录、仓内已有 43 份 run report、register 中已有决策类编号行（`D1–D9`、`D-A`、`D-B`、`D-001` 等）。

**后果**：决策文本可以只写简称、可以在同名资源前不给出定位信息；选项可以不是封闭集；决策可以只活在对话或某份工件正文里，事后无法只凭档案重建「谁、何时、基于什么、选了哪个、是否被传递与实施」；superagent 的决策传到 subagent 时可能被静默改写；人工交互式决策与 AI 自主决策用同一种呈现，前者牺牲可读性、后者牺牲严谨性。两条生产事件（简称导致的错误决策、同名资源导致的错误决策）已经证明这不是理论风险。

**实测基线（2026-11-25，base `fbab7a45c`）**：`templates/instructions-template.md` 与生成的 `.specify/instructions.md` 均**不含**这两条生产规则（全仓 grep「完整名称 / 同名冲突 / region id」在模板与活指令面零命中，命中仅在无关技能与文档）；`.specify/glossary.md` **没有** Decision 词条；本仓**没有**决策项契约、决策记录形态或决策传递契约的所有者页。上述所有者文件与计数由本次测量取得，实现期可复测。

**本特性交付**：一个**决策治理单一所有者页**（新概念，A-2），拥有决策词汇闭集、两类决策的强调与呈现模板要求、选项集契约、决策记录字段闭集与字段→所有者映射、传递与实施回执义务、机器可判/行为类边界；一个**封闭的决策生产者清单**把既有生产者逐一映射到既有归档载体（不新建登记/存储）；在既有派发载荷通道中增加**决策块**并规定确认与实施回执；为机器可判子集提供可转红的守卫（含逆向样本），为行为类规则指定评审承接面；把两条生产规则作为最低门槛落到 instruction 模板与所有者页；并完成镜像、每工具副本、客户项目接收与兼容/迁移收口。

**不做什么**：不新建第二套决策登记、队列、存储或调度器；不替换 `decision-tension.md` 的承重取舍契约（承重决策**追加**一条决策记录并以 `T-NNN` 交叉引用，不复制六字段）；不新增阻塞式确认门控；不改写任何 dated record（历史规格、历史评审、既有记录正文）；不追求对「名字是否足够完整」「理由是否充分」等语义命题的机器判定——它们归评审（A-9）；不把决策记录做成运行时服务。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **Flow Class = `execution`**：交付物是规则所有者页、模板段、载荷契约、守卫与契约测试；缺陷只在解析、断言或执行时暴露。`Flow Type` 写 `-`。 | 按验收 oracle 判定（`shared/declarations/facts/flow-class-basis.yaml` 的既有判据），而非按文本介质。 |
| **A-2** | **单一所有者页 = `shared/definitions/decision-definitions.md`（新概念）**：本仓不存在「决策项一般契约」的所有者，因此按 `create-requirements` 的概念-所有者检查如实声明为**新概念**，由本特性创建；既有相邻所有者（`confirmation-gates.md`、`decision-tension.md`、`fast-fail.md`、`register.md`、`superagent-definitions.md`、`goal-definitions.md`、`anchor-definitions.md`、checkpoint 协议、analyze/review 技能）保留各自事实，只新增**指针行**指向新页；新页 MUST NOT 复述它们的判据表。命名按最近同型兄弟（`superagent-definitions.md`、`goal-definitions.md`、`anchor-definitions.md`）取 `decision-definitions.md`。 | Grounded Naming + One Source Of Truth：新概念必须有所有者；已有事实不搬家，避免第二定义点。 |
| **A-3** | **归档即投影（archive-as-projection）**：决策档案不是新存储，而是「封闭生产者清单 × 既有载体」的投影；`.specify/register.md` 仍是持久编号的唯一索引。每个决策记录的载体由其生产者决定（如 requirements 裁决 → `requirements.md` § Clarifications；承重取舍 → `plan.md` § Decision Tensions；阶段裁决 → 检查点文件；传递 → run report/派发载荷）。没有载体的生产者 MUST 走清单修订，MUST NOT 静默丢弃记录。 | 简报明令「No second registry: reuse/extend the register, decision-tension, goal/anchor/checkpoint and execution-record surfaces」。 |
| **A-4** | **两类决策的判定看持有者**：`human-interactive` = 决策由人持有（交互式决策门的用户选择、人工评审处置、人对选项的选择）；`ai-autonomous` = 决策由 agent 在无用户在场时持有（无人值守裁决、被委派的实施取舍、运行内自裁）。同一个生产者可产出两类（如确认门在交互运行是前者、无人值守运行是后者）。类缺失、类混合或类与持有者不符是缺陷（类不符的**判定**属行为类，B-06）。**传递不改变类别**：被交办实施的决策在其决策块中沿用其记录的类别——人持有的决策被交办仍为 `human-interactive`，父侧无人值守自主交办才是 `ai-autonomous`（P-09、FR-018）。 | 简报的两类区分是「核心考量不同」；用持有者定义可判定且与 `confirmation-gates.md` 的授权级别轴正交，不复制其取值域。 |
| **A-5** | **「每个决策」的外延 = 封闭生产者清单**：清单内生产者产出的**决策项**必须留记录；`fast-fail` 意义上的 in-passing correction 不是决策；未显式呈现、未被传递、未被评审的普通设计细节不是决策项；清单外生产者若产出决策项即缺陷（应补入清单）。清单扩展 MUST 以修订所有者页/本规格清单的形式进行。 | 把「每个决策」变成可判定命题，同时不把一切思考都变成记录负担；纠正/裁定判据归 `fast-fail.md`，不复述。 |
| **A-6** | **决策编号 = `D-NNN`（三位、按载体密集），登记于 register**：沿用 ID Register 已列出的 `D-…` 编号族（先例：087 的 `D-001`），不发明新前缀；同一载体内的 `D-NNN` 唯一且连续，跨载体允许重复出现但引用 MUST 同时给出**载体指针**；编号不复用，被取代的决策保留原记录并标 `superseded`。register 行可逐条或按「载体 + 区间」分组登记（先例：`D1–D9` 分组行）。 | Grounded Naming + ID Register 纪律：编号在诞生时登记；一处编号只有一个定义点。 |
| **A-7** | **传递复用既有载荷通道**：决策块搭乘 `superagent-definitions.md` 已拥有的派发载荷通道下行；七角色字段与四项既有注入**保持不变**，决策块是任务权威内容而不是第八个角色字段；若实现需要改变字段数或注入清单，MUST 有记录在案的裁定（brief 约束）。 | 简报要求「transmission（role_edge + payload）」；既有契约的改动面应最小、可审计。 |
| **A-8** | **两条生产规则 = 最低门槛，不是全部**：①决策项文本使用完整名称，不得只用简称；②可能存在同名冲突时，每个决策项给出资源的完整定位信息（如业务资源组 + region id）。两条 MUST 同时落在**所有者页**与 **instruction 模板**，并进入决策项模板与守卫/评审；特性范围不限于 instruction。 | 两条规则来自真实生产事故；用户明言「NOT limited to the instruction template; the two examples are the minimum bar」。 |
| **A-9** | **机器可判/行为类边界沿用既有分野**：机器可判 = 在场性、形态、闭集取值、引用可解析、集合封闭、id 可解析；行为类 = 名称是否真的足够完整、定位维度是否真的足够区分、可读性、严谨性、后果与理由是否真实充分、类别是否选对。机器类 MUST 有能转红的守卫（含逆向样本）；行为类 MUST 有具名评审承接面，MUST NOT 声称被机器覆盖。 | 与 `053-machine-decidable-artifacts` 的判据一脉相承：程序只判可机械判定的结构命题，语义仍归 analyze/clarify/review。 |
| **A-10** | **兼容策略 = 新记录新形态、旧记录只读**：新契约只约束本特性落地后创建的决策记录；旧记录保持可解析并报告为 `legacy`，不被判为无效、不被改写。任何使既有载体或载荷不再成立的变更 MUST 在 `/speckit.migrate` 中有迁移或确定性拒绝，plan MUST 维护封闭的不兼容变更清单（先例：105 的 § Backward-Incompatible Change Inventory）。 | 简报约束「Preserve existing sentinel literals … unless a recorded ruling justifies a change」与「no retroactive rewrite」。 |
| **A-11** | **词汇表提案只提议不写入**：`Decision Item`、`Decision Class`、`Human-Interactive Decision`、`AI-Autonomous Decision`、`Decision Record`、`Implementation Receipt` 等新词以 `origin=auto`、`status=proposed` 形态记录在 run 证据中；未获用户确认前不写 `.specify/glossary.md`（先例：105 A-16）。无验收标准依赖写入动作。 | `shared/workflow/glossary.md` § 冲突与用户优先；无人值守运行不因等待确认而阻塞。 |
| **A-12** | **Related Feature 保持 `Need clarification`**，绑定推迟到 `/speckit.clarify`（Feature Integration Protocol）。本仓的 `101` 条张力记录、`125` 个检查点、`43` 份 run report 与 register 决策行仅作**基线语料**，不构成绑定。（已结清：2026-11-25 的 `/speckit.clarify` 绑定为 **Feature 107**，见 § Clarifications；本条保留为 requirements 阶段的时点裁定。） | `create-requirements` 步骤 5.3/6 明令；binding 不是本次运行的职责。 |
| **A-13** | **instruction 段为指针形并声明字节上限**：新段「Decision Items（决策项）」在 `templates/instructions-template.md` 中以「两三条最低规则 + 指向所有者页」的形态存在，声明 `**本节字节上限：1,500 B**`（判据 = 声明上限 + 生成后实测增量）；MUST NOT 复制所有者页的判据表或模板全文。 | 同 `templates/instructions-template.md` 既有段落的形态与字节预算纪律；避免指令膨胀与第二定义点。 |
| **A-14** | **守卫程序优先、复用既有检查器**：优先扩展既有 `validate-*`/契约测试面；若需新引擎，MUST 遵守 `shared/definitions/script-interface-definitions.md`（`--help`/`--version`、拒绝未声明选项、只读/写入面声明）。守卫经唯一测试入口 `scripts/bash/run-tests.sh` 执行；本特性不新增第三方依赖。 | Program-First + Script Interface Contract + 单一测试入口。 |

## Decision Producer Inventory (closed)

清单外的生产者若产出决策项即缺陷（A-5）。`Obligation` 取值域：`record` = 该生产者产出的每个决策项 MUST 有决策记录；`record-when-decision` = 其输出只有在构成决策时才需要记录（须给出判据）；`exempt` = 不产出决策项（必须给理由）。扩展 MUST 修订本表或所有者页同名表。

| ID | Producer | 既有面 / 归档载体 | Obligation | Class（按持有者） | Owner（事实与载体） |
|----|----------|------------------|------------|-------------------|---------------------|
| P-01 | 确认门 / 用户决策 | 门控执行报告 + 门控观察 probe 条目（`feedback-utils.py --action record --lifecycle-point gate:<id>`） | record-when-decision（门控触发即是决策；可逆动作的自动执行不是决策门） | 交互运行 `human-interactive`；无人值守 `ai-autonomous` | `shared/guidelines/confirmation-gates.md`（是否问）；本页所有者（记录形态） |
| P-02 | requirements 阶段裁决（无人值守自裁） | `requirements.md` § Clarifications（Session 行）+ 本规格 A 表 | record | `ai-autonomous` | `skills/internal/create-requirements/SKILL.md` |
| P-03 | plan 阶段取舍与承重决策 | `plan.md`（含 § Decision Tensions 的 `T-NNN`） | record（显式呈现的取舍）；承重决策另加 `T-NNN` 并交叉引用 | 通常 `ai-autonomous` | `shared/guidelines/decision-tension.md`（六字段）；本页所有者（决策记录） |
| P-04 | 阶段检查点裁决 | `<spec-dir>/checkpoints/<NN>-<stage>.md` | record-when-decision（检查点内的并发/名册/方向裁决是决策；纯事实核验不是） | `ai-autonomous` | `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` |
| P-05 | analyze 处置 | analyze findings report（`/speckit.analyze` 的 compact findings report） | record（每个 carried finding 的 `fixed`/`deferred`/`rejected` + reason 是决策项） | `ai-autonomous` | `skills/internal/analyze-artifacts/SKILL.md` |
| P-06 | review 发现处置 | review report（`review.md` 与分段报告） | record-when-decision（处置的接受/修复/拒绝是决策；纯观察不是） | 由持有者定（人工评审 = `human-interactive`；自动分段 = `ai-autonomous`） | `skills/internal/review-feature-quality/SKILL.md`、`skills/internal/review-sdd-process/SKILL.md`、`shared/workflow/acceptance-hardening.md` § Review Composition |
| P-07 | fast-fail 裁定 | fast-fail 上送件 + 处置回执（执行报告） | record-when-decision（裁定是决策；异常报告本身不是） | 由持有者定（用户裁定 = `human-interactive`；无人值守按矩阵自裁 = `ai-autonomous`） | `shared/guidelines/fast-fail.md` |
| P-08 | goal / anchor / team 决策 | `.specify/goals/<slug>/goal.md`、`.specify/anchoring/<slug>/anchor.md`、`.specify/teams/<slug>/team.md` 的既有决策/History 面 | record | 由持有者定（用户裁定 = `human-interactive`；团队/引擎裁决 = `ai-autonomous`） | `shared/definitions/goal-definitions.md`、`anchor-definitions.md`、`agent-definitions.md` |
| P-09 | superagent → subagent 传递决策 | 派发载荷（决策块）+ run report / 角色边载体 | record（被传递的决策项 MUST 有记录——即该决策在产出载体的那条唯一记录；传递动作与实施回执 MUST NOT 生成第二条决策记录，只更新该记录的 [[STR-007]] 与审计链三段）+ 传递 + 实施回执 | 随被传递决策记录的类别（A-4）：父侧无人值守自主交办 = `ai-autonomous`；人持有的决策被交办实施仍为 `human-interactive`（`decision_class` MUST 与其记录一致，FR-018） | `shared/definitions/superagent-definitions.md`、`skills/internal/run-agent/SKILL.md`、`skills/internal/run-team/SKILL.md` |
| P-10 | probe / feedback 处置 | `.specify/feedback/` 条目 + probe 注册面 | record-when-decision（阈值提示不是决策；接受/延后/拒绝处置是决策） | 通常 `ai-autonomous` | `shared/definitions/probe-definitions.md`、`shared/workflow/feedback-step.md` |
| P-11 | run determination（运行判定） | session 记忆中的判定记录（`run-determination.py`） | exempt —— 它是对已完成运行的**测量/评估**，不是「在选项间选择」的决策项 | n/a | `shared/workflow/feedback-step.md` § Run Determination |
| P-12 | 确定性检查器/门的 verdict（pass/fail、split-required、校验退出码） | 检查器输出 / 检查点引用 | exempt —— 结果由规则唯一决定，没有选项集；围绕它的处置归 P-04/P-05 | n/a | 各检查器与 `shared/workflow/acceptance-hardening.md` § Gates |

**清单封闭性**：实现期 MUST 以代码面扫描（模板、技能、agents、scripts、src 中会写决策/裁决/处置/记名册的入口）对照本表；表中之外的决策入口 MUST 触发清单修订，MUST NOT 静默放行（FR-003）。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 两条生产事故在决策文本层被挡住，且两类决策各按自己的强调呈现 (Priority: P1)

一个维护者在无人值守运行里裁决「把某资源迁到哪个资源组」。决策文本自动给出资源的完整名称；当同一业务资源组下存在两个同名资源时，决策项在提问/记录之前就带上业务资源组与 region id 的完整定位，而不是让简称和同名把选择带偏。一个交互式决策门给用户看的是平实语言、上下文、后果与可逆性；一个 AI 自主决策留下的是封闭选项、明确的决策谓词、显式假设与可机器核查的证据。两类决策都**声明自己的类别**，类别缺失或呈现与类别不符都会被报出。

**Why this priority**: 这是用户请求的语义核心与两条真实生产事故的直接修复；文本层挡不住，后面所有归档与传递都在传播错误决策。

**Independent Test**: 两个夹具分别复现「只用简称」与「同名资源无定位信息」，断言守卫/评审在缺完整名称或缺定位维度时转红、补全后转绿；再以同一决策分别按两类模板呈现，断言类别声明、必需要素与评审承接面的差异。

**Acceptance Scenarios**:

1. **Given** 一个结构化决策记录声明 `same_name_conflict: true`，**When** 其 `resource_locator` 为空或不足两个具名维度，**Then** 机器守卫转红；补齐业务资源组 + region id 后转绿。
2. **Given** 决策项主体用了一个已在 `.specify/glossary.md` 登记为 variant 的简称（canonical 存在），**When** 记录被守卫检查，**Then** 机器守卫转红（M-08）；未登记简称由行为类评审 B-01 承接，不声称机器覆盖。
3. **Given** 一个 `human-interactive` 决策项，**When** 呈现给用户，**Then** 它包含平实语言的问题、上下文、每个选项的后果/可逆性/默认项，以及完整名称与定位信息；若只有形式化谓词而无解释，评审按 B-03 报缺陷。
4. **Given** 一个 `ai-autonomous` 决策项，**When** 记录落盘，**Then** 它包含封闭选项集、决策谓词/规则、显式假设、可机器核查的证据指针与确定性结论；若只有散文而无判定规则，评审按 B-04 报缺陷。
5. **Given** 任何决策项缺少类别或类别值不在闭集 `human-interactive` / `ai-autonomous` 内，**When** 守卫检查，**Then** 转红。

---

### User Story 2 - 选项集是封闭、可枚举、可比较的，没有「其他」黑洞 (Priority: P1)

一个决策项的选项构成封闭集合：每个选项有名有姓（遵循与决策主体相同的完整名称/定位规则），带后果、可逆性、默认项与选择所需证据。只有在给出「新增选项的路径」时，名为 `other` 的选项才合法；否则「其他」不是选项。只有一个可行选项时，决策项自带 `forced` 声明与理由，而不是伪装成多选。

**Why this priority**: 选项不规范会让决策看起来有选择、实际无法比较；同名与简称同样会污染选项标签。

**Independent Test**: 夹具分别构造空选项集、重复标签、`other` 无路径、单选项未声明 forced，断言守卫转红；补齐五要素后转绿。

**Acceptance Scenarios**:

1. **Given** 一个选项集，**When** 任一选项缺少 label / consequences / reversibility / default / evidence 五要素之一，**Then** 机器守卫按形态转红。
2. **Given** 名为 `other` 的选项且无 `path` 定义，**When** 守卫检查，**Then** 转红；给出「谁在何时可新增选项、如何回写记录」的路径后转绿。
3. **Given** 只有一个可行选项，**When** 记录落盘，**Then** 决策项声明 `forced` 与理由；未声明即缺陷。
4. **Given** 一个 `ai-autonomous` 决策，**When** 用记录的输入与决策谓词重放，**Then** 选中项可被确定性地重新推出；重放结果与记录不符即缺陷（M-01 + SC-004）。

---

### User Story 3 - 每个决策都归档在既有档案中，且只凭档案就能重建 (Priority: P1)

审计者拿到 `.specify/register.md` 与各既有载体，不打开任何对话历史，就能为每个清单内生产者产出的决策重建：决策编号、类别、上下文、选项集、选中项、理由、证据指针、持有者/执行者身份、时间戳，以及传递与实施状态。承重决策的理据只存在 `T-NNN` 六字段里，决策记录只交叉引用它，不复制。没有新台账、没有第二个真相。

**Why this priority**: 「必须归档并可审计」是用户原话；不约束载体就会长出第二套登记。

**Independent Test**: 取一组夹具决策（分别落在 requirements、plan、checkpoint、run report），只用 register + 载体重建全部字段；删掉任一必填字段或改坏任一指针，断言守卫转红。

**Acceptance Scenarios**:

1. **Given** 一个清单内生产者产出决策项，**When** 决策完成，**Then** 其记录落在该生产者对应的既有载体中，含 FR-014 的封闭字段集，且 `D-NNN` 已登记于 register。
2. **Given** 一份承重决策，**When** 检查记录，**Then** 决策记录引用对应的 `T-NNN`，且不重复六个张力字段；重复即缺陷（FR-017）。
3. **Given** 任一记录的 evidence 指针，**When** 审计者解析，**Then** 指针全部可解析；任一不可解析即缺陷。
4. **Given** 一条本特性落地前创建的旧形态记录，**When** 审计者读取，**Then** 它被报告为 `legacy` 并可解析，不被判无效、不被改写（FR-028）。

---

### User Story 4 - 决策完整跨过 superagent→subagent 边，实施回执把结果钉回决策编号 (Priority: P1)

一个 superagent 决定「按方案 B 实施」，把决策交给 subagent。派发载荷携带决策块（编号、类别、选中项、实施约束、档案指针），子代理回传确认；实施完成后，回执写明 `decision_id`、做了什么、证据指针，以及「与决策一致 / 发生偏离（附理由）」的声明。子代理不得静默重决；上下文已使决策失效时，它停在异常点快速失败上送，而不是自行改选。审计链从决策记录 → 派发尝试（角色边/run report）→ 实施回执全部可追溯。

**Why this priority**: 用户明确点名 superagent 决策 + subagent 实施；传递处静默改写会让归档与实施脱节，审计归零。

**Independent Test**: 一次夹具派发：载荷含完整决策块、回传含确认与实施回执；再注入「上下文变化」与「子代理自行改选」两种形态，断言前者成为 fast-fail 上送、后者成为显式异常；无决策块的实施派发被拒绝。

**Acceptance Scenarios**:

1. **Given** 一个决策 backed 的实施派发，**When** 构建载荷，**Then** 决策块含 `decision_id`、`decision_class`、选中项、实施约束与档案指针；缺项即拒绝派发（M-06）。
2. **Given** 子代理的回传，**When** 父侧消费，**Then** 回传含决策确认与 `implementation_receipt`（含 `decision_id`、实施摘要、证据指针、偏离声明）；缺任一项即回传不完整，父侧 MUST NOT 消费或补齐（沿用 `superagent-definitions.md` 上行规则）。
3. **Given** 子代理发现决策已失效，**When** 它停止，**Then** 以上送件形态报告「证伪了什么预期」，父侧重决并留下新记录；旧记录与回执保留。
4. **Given** 一个没有决策记录/编号的实施决策，**When** 尝试派发，**Then** 拒绝；一个子代理无法解析的 `decision_id`，**When** 尝试实施，**Then** 停止并报告（M-04/M-05）。
5. **Given** 一条传递决策，**When** 审计，**Then** 决策记录 → 派发尝试 → 实施回执三段链路可解析；断链是可上报的显式异常，不是沉默（M-07）。

---

### User Story 5 - 强制是诚实的：机器判可判的，评审承接不可判的 (Priority: P2)

维护者检查这套治理的强制面：每条机器可判规则都有一个能转红的守卫，并配一个逆向样本（把被检查对象改坏，守卫必须红）；每条行为类规则都点名评审承接面，不被冒充为机器覆盖。守卫沿用既有测试入口与脚本接口契约，不新增阻塞门控。

**Why this priority**: 没有可转红的守卫，「治理」只是文档；把不可判的命题冒充机器判，会制造假绿。

**Independent Test**: 逐守卫做 mutation/逆向演练；对照 § Enforcement Boundary 的机器/行为两表核对守卫清单与评审义务，缺一即红。

**Acceptance Scenarios**:

1. **Given** 任一机器可判规则，**When** 移除其守卫或让被检查对象违反它，**Then** 测试转红且定位到该规则。
2. **Given** 任一行为类规则，**When** 查评审承接面，**Then** 存在具名承接面（analyze / review 段 / 人工评审）；文档或测试不得声称它被机器覆盖。
3. **Given** 新增守卫，**When** 运行既有测试入口，**Then** 经 `scripts/bash/run-tests.sh` 执行；新脚本若存在，`--help`/`--version` 可用且拒绝未声明选项。
4. **Given** 治理落地，**When** 运行 `scan-confirmation-gates.py`，**Then** 无新增阻塞门控命中；既有哨兵字面量、watcher verdict/退出码与测试预算不变（除非记录在案的裁定）。

---

### User Story 6 - 落地可交付、镜像一致、客户项目收得到，旧记录不被改写 (Priority: P2)

框架维护者发布该能力：所有者在 `shared/`、instruction 模板段、生产者面、载荷契约与守卫中都落地；`.specify/` 镜像与每工具副本在同一变更内再生成；下游项目经 init/refresh 收到 instruction 段与规则；旧记录原样保留、报告为 legacy；任何不兼容的记录形态变更都有迁移或确定性拒绝路径，而不是运行时双路径回退或人工说明。

**Why this priority**: 只在源树写文档、不发到客户项目等于没做；改写旧记录或靠双路径回退会制造静默漂移。

**Independent Test**: 镜像检查 + 命令副本再生成检查；空客户项目 init 夹具断言 instruction 段与规则存在；旧规格记录零改写（行级零删除读数，允许追加）；不兼容变更逐行跑 migrate dry-run/refusal。

**Acceptance Scenarios**:

1. **Given** 特性落地后的源树，**When** 运行镜像与副本检查，**Then** `regen-command-copies.py --check` rc 0，`sync-mirrors.py --check` 的漂移成员集相对基线无新增成员（绝对读数如实报告）。
2. **Given** 一个空客户项目夹具，**When** 执行 `specify init` 刷新，**Then** `.specify/instructions.md` 含「Decision Items」指针段与两条生产规则，且在声明字节上限内。
3. **Given** base `fbab7a45c` 的既有决策记录（`T-NNN`、检查点、run report、register 行、Clarifications），**When** 与实现后的工作树比较，**Then** 记录正文零改写；只有新记录使用新形态。
4. **Given** plan § Backward-Incompatible Change Inventory 的每一行，**When** 执行 `/speckit.migrate` 的 dry-run 与 apply/refuse，**Then** 每行产出具名迁移或确定性拒绝与证据；任一依赖运行时双路径回退或人工说明的行使守卫转红。

### Edge Cases

- **同一 `D-NNN` 出现在两个载体**：编号按载体密集，引用 MUST 同时给载体指针；同一载体内重复即缺陷（dup-id 类守卫）；register 行以「载体 + 区间」分组消歧（A-6）。
- **决策被推翻/取代**：保留两条记录（原件 + 取代件），原件标 `superseded` 并指向新编号；MUST NOT 删除或改写原件；推翻本身也是一条决策记录。
- **决策在传递后失效**：子代理停在异常点快速失败上送（`shared/guidelines/fast-fail.md`），父侧重决并新增记录；旧记录与旧回执保留，审计链不断。
- **只有一个可行选项**：决策项声明 `forced` 与理由；伪装成多选是缺陷；没有选项的「决策」不是决策项。
- **`other` 选项**：仅在定义 `path`（谁、何时、如何新增选项并回写记录）时合法；否则守卫转红。
- **同名冲突未声明但实际存在**：行为类评审（B-02）承接；把 `same_name_conflict` 标 false 以绕过定位是缺陷，不是豁免。
- **无人值守运行中出现 `human-interactive` 决策**：不得静默转成 AI 自主决策；以 blocked 报告携带问题与选项停等（沿用 `confirmation-gates.md` 的无人值守轴），类别保持 `human-interactive`、状态标 `blocked`。
- **生产者没有归档载体**：清单修订，MUST NOT 丢弃记录；一个生产者只有在给出 `exempt` 理由时才可移出记录义务。
- **只读命令产生处置**（如 analyze 只读）：处置写入它自己的报告载体，MUST NOT 通过修改被分析工件来「归档」。
- **决策跨多跳子代理链**：每一跳载荷都携带决策块、每跳回执都引用同一 `decision_id`；最终实施回执与原始记录可连成一条链。
- **两个并行分支同时记录决策**：记录落在各载体（逐文件/逐条目），不写共享可变聚合；register 为手工唯一写入者，编号冲突按 `/speckit.sanitize --lane renumber` 的既有机制修复，MUST NOT 静默改号。

## Requirements *(mandatory)*

### Functional Requirements

**所有者与边界**

- **FR-001**: MUST 创建单一所有者页 [[STR-001]]，拥有本特性的封闭词汇表（decision item / decision class / human-interactive decision / ai-autonomous decision / decision record / decision archive / decision transmission / implementation receipt / decision producer）、两类决策的强调与呈现要求、选项集契约、决策记录字段闭集、传递与实施回执义务、机器可判/行为类边界、以及字段→所有者映射。其他面（instruct、模板、技能、agents、文档）MUST 以指针抵达，MUST NOT 复述其判据表。
- **FR-002**: 相邻所有者保留各自事实并只新增指针行：`confirmation-gates.md`（是否问、授权级别轴）、`decision-tension.md`（承重取舍六字段 `T-NNN`）、`fast-fail.md`（纠正/裁定）、`register.md`（编号登记）、`superagent-definitions.md`（角色边/载荷/上行）、goal/anchor/team/checkpoint/analyze/review/probe 的既有所有者。每个决策记录字段 MUST 在本规格 § Decision Record Field Ownership 表中恰有一个定义所有者。
- **FR-003**: MUST 维护**封闭的 Decision Producer Inventory**（本规格 § Decision Producer Inventory）；每个生产者 MUST 取 `record` / `record-when-decision` / `exempt` 之一并给出载体与所有者；实现期 MUST 以代码面扫描核对「表中之外无决策入口」；清单外入口产出决策项即缺陷；扩展 MUST 以修订所有者页/清单的形式进行。
- **FR-004**: MUST NOT 新建第二套决策登记、队列、存储或调度器；决策档案 MUST 是既有载体的投影，`.specify/register.md` MUST 是持久编号的唯一索引；载体保留各自格式与 owner。
- **FR-005**: MUST 产出新决策词汇的 glossary 提案（`origin=auto`、`status=proposed`）并留在 run 证据中；未获用户确认前 MUST NOT 写入 `.specify/glossary.md`；写入时必须走 `glossary-utils.py` 的冲突检测。

**决策文本（按类）**

- **FR-006**: 每个决策项 MUST 声明恰一个 [[STR-002]] 取值，闭集为 [[STR-003]] / [[STR-004]]；类缺失、类混合或值域外是缺陷；类决定适用的模板与检查集。
- **FR-007**: 决策项描述 MUST 无歧义地标识对象：主体与选项标签 MUST 使用完整名称，MUST NOT 只用简称；当可能存在同名冲突时，决策项 MUST 给出机器可解析的 [[STR-005]]，其中 MUST 包含能区分同名资源的具名维度（下限：业务资源组 + region id 这一对；具体维度集由所有者页声明）；同名冲突 MUST 以 [[STR-006]] 显式声明；决策项 MUST NOT 在没有定位信息时呈现同名对象。
- **FR-008**: [[STR-003]] 决策项 MUST 以可读性为先：平实语言、上下文、每个选项的后果与可逆性、默认项、完整名称与定位信息；措辞与上下文规则 MUST 遵循 `shared/guidelines/user-facing-comprehension.md`，MUST NOT 只给形式化谓词而无解释。
- **FR-009**: [[STR-004]] 决策项 MUST 以严谨性为先：封闭选项集、明确的决策谓词/规则、显式假设、可机器核查的证据指针、确定性结论与重开条件；MUST NOT 只有散文而没有判定规则。
- **FR-010**: 两条生产规则 MUST 作为最低门槛落到**所有者页与 instruction 模板**：①完整名称；②同名冲突时的完整定位信息；两条 MUST 同时进入决策项模板与守卫/评审（不是只改 instruction 一段话）。
- **FR-011**: 呈现与类别不符 MUST 被判为缺陷：`human-interactive` 只有形式化谓词无解释、或 `ai-autonomous` 只有散文无判定规则，任一面 MUST 被具名评审承接（B-03/B-04）；类别的**选错**由 B-06 承接，MUST NOT 声称机器可判。

**选项**

- **FR-012**: 选项 MUST 构成封闭、可枚举的集合；每题 MUST 有声明的选项数（含 0/1 的退化情形）；每个选项 MUST 携带 label、consequences、reversibility、default 标记、evidence（选择所需证据）五要素；`other` 只有在定义 `path`（谁/何时/如何新增选项并回写记录）时才合法；空选项集不能构成决策项。
- **FR-013**: 选中项 MUST 被记录为选项集中的一个具名成员；`ai-autonomous` 决策的选中项 MUST 能由记录的输入与决策谓词确定性重放推出；`human-interactive` 决策 MUST 记录人作出的选择信号（信号词汇沿用 `confirmation-gates.md` 门控观察协议的既有取值域，不复述）。

**归档与审计**

- **FR-014**: 每个决策项 MUST 在决策完成时恰产生一条决策记录，落在其生产者在清单中对应的既有载体；记录字段闭集：[[STR-009]]、[[STR-002]]、context、options、chosen option、rationale、evidence pointers、actor、timestamps（创建/传递/确认/实施）、[[STR-007]]；缺任一字段即缺陷。字段名以所有者页与本规格 Shared Strings 为准，生产面 MUST NOT 改名。传递动作与实施回执 MUST NOT 生成第二条决策记录——一条决策项恰一条记录；回执只更新该记录的 [[STR-007]] 与审计链（FR-019、FR-021）。
- **FR-015**: 决策编号 MUST 取 `D-NNN`（三位、按载体密集、不复用），并 MUST 在编号诞生时登记于 `.specify/register.md`（可逐条或按载体+区间分组）；跨载体引用 MUST 同时携带载体指针；被取代的编号保留并标 `superseded`，MUST NOT 重用或删除。
- **FR-016**: 决策记录 MUST 可只凭既有载体 + register 重建；evidence 指针 MUST 全部可解析（可由机器判定解析性的是 M-09：指针指向的载体路径/锚必须存在且可读；证据是否充分属评审）；无法重建（缺字段、断指针、无记录）即缺陷，MUST NOT 以对话记忆补足。
- **FR-017**: 承重决策 MUST 同时满足 `decision-tension.md` 的六字段，并由决策记录交叉引用对应 `T-NNN`；决策记录 MUST NOT 复制 `antithesis`/`binding_constraints`/`discriminating_evidence`/`expected_sacrifice`/`revision_trigger` 的内容（单一定义点）。

**传递与实施（superagent → subagent）**

- **FR-018**: 交办实施的决策 MUST 以**决策块**搭乘既有派发载荷通道下行：块内 MUST 含 `decision_id`、`decision_class`、选中项（完整标签）、实施约束、档案指针；缺项 MUST 拒绝派发；`decision_class` MUST 与被传递决策记录的 `decision_class` 一致（传递不改变类别；人持有的决策被交办实施仍为 `human-interactive`）；七角色字段与四项既有注入保持不变（A-7）。
- **FR-019**: 子代理回传 MUST 含决策确认与 [[STR-008]]：[[STR-009]]、实施摘要、证据指针、偏离声明（`none` 或 `diverged` + 理由）；回执 MUST 更新记录的 [[STR-007]] 实施状态；缺任一项即回传不完整，父侧 MUST NOT 消费或补齐（沿用 `superagent-definitions.md` 上行规则）。
- **FR-020**: 子代理 MUST NOT 静默重决：上下文变化导致决策失效时 MUST 停在异常点并以 fast-fail 上送；无决策记录/编号的决策 MUST NOT 被派发实施；无法解析的 `decision_id` MUST NOT 被实施。
- **FR-021**: 每条传递决策 MUST 留下可审计链：决策记录 → 派发尝试（角色边 identity / run report）→ 实施回执；断链 MUST 是可上报的显式异常，MUST NOT 沉默。

**强制**

- **FR-022**: MUST 为机器可判子集提供守卫，且每个守卫 MUST 能转红：M-01 记录字段/类取值/时间戳形态；M-02 [[STR-006]] 为 true 时 [[STR-005]] 存在且具名维度数达下限；M-03 选项闭集（空集/重复标签/`other` 无 `path`/五要素缺失）；M-04 新式记录（`^### D-\d{3}` 标题且携带记录字段文法）的 `D-NNN` 形态、同载体密集性与 register 可解析（legacy 标题与 register 行不判）；M-05 [[STR-008]] 存在且 [[STR-009]] 可解析；M-06 决策 backed 派发的决策块完整性；M-07 审计链三段在场；M-08 结构化决策主体命中 glossary 已登记 variant（canonical 存在）时转红（只覆盖已登记词）；M-09 evidence 指针可解析（指向的载体路径/锚不存在或不可读即转红；只判解析不判充分性）。
- **FR-023**: 行为类规则 MUST 点名评审承接面并 MUST NOT 冒充机器覆盖：B-01 完整名称是否足够完整；B-02 定位维度是否足够区分；B-03 人工可读性与后果/可逆陈述的真实性；B-04 AI 决策谓词/假设/确定性是否成立；B-05 理由是否充分；B-06 类别是否选对。承接面至少覆盖 `/speckit.analyze`（产物一致性）、`/speckit.review`（产物/实现/代码段）与人工决策评审。
- **FR-024**: 每个守卫 MUST 配一个逆向/变异样本（把被检查对象改坏后守卫转红），无逆向样本的守卫视为缺陷；守卫 MUST 经唯一测试入口执行；新增脚本若存在 MUST 满足 `script-interface-definitions.md`。
- **FR-025**: 本特性 MUST NOT 新增阻塞式确认门控；`scan-confirmation-gates.py` 的治理后复扫 MUST 零新增命中；既有哨兵字面量、watcher verdict/退出码与两槽测试预算 MUST 保持不变，除非有记录在案的裁定。

**落地与兼容**

- **FR-026**: MUST 在框架源落地：所有者页、instruction 模板新段（指针形、含两条生产规则、声明字节上限）、各生产者面、载荷契约、决策项模板与守卫；instruction 段 MUST 同时出现在 `templates/instructions-template.md` 与生成的 `.specify/instructions.md`（含每工具兼容副本/符号链接）。
- **FR-027**: MUST 在同一变更内再生成 `.specify/` 镜像与每工具命令副本：`regen-command-copies.py --check` MUST rc 0；`sync-mirrors.py --check` 的漂移成员集 MUST 相对基线无新增成员（绝对读数如实报告）；MUST NOT 手改镜像面。
- **FR-028**: 新契约只约束本特性落地后创建的决策记录；base `fbab7a45c` 的既有记录（`T-NNN`、检查点、run report、register 行、Clarifications、review/analyze 报告正文）MUST NOT 被改写；旧形态记录 MUST 保持可解析并报告为 `legacy`，MUST NOT 被判无效。
- **FR-029**: 任何**向后不兼容的记录形态变更**（使既有载体/载荷/编号/instruction 面在新版本下不再成立的变更）MUST 在 `/speckit.migrate` 中有可执行迁移逻辑或确定性拒绝；plan MUST 维护封闭的 § Backward-Incompatible Change Inventory，每行具名迁移/拒绝行为与证据指针；MUST NOT 只依赖运行时双路径回退或人工操作说明。
- **FR-030**: MUST 更新框架文档与登记面：框架地图为所有者页 [[STR-001]] 新增一行（owner/生命周期/内容）；docs 以指针抵达所有者页、MUST NOT 复述规则；glossary 提案按 FR-005 留证；`Related Feature` 绑定已由 2026-11-25 的 `/speckit.clarify` 完成（Feature 107，见 § Clarifications）。

### Key Entities

- **Decision Item（决策项）**：一个被呈现给人或由 agent 持有的选择；属性：类别、完整名称与定位、上下文、选项集、选中项、理由、证据、持有者。
- **Decision Record（决策记录）**：决策项在既有载体中的归档投影；字段闭集见 FR-014；以 `D-NNN` 标识。
- **Option（选项）**：label、consequences、reversibility、default 标记、evidence，以及可选的 `other` path。
- **Decision Class（决策类别）**：`human-interactive` / `ai-autonomous` 闭集。
- **Decision Producer（决策生产者）**：封闭清单内的一个会产生决策项的既有面；携带 obligation、载体与 owner。
- **Decision Archive（决策档案）**：清单 × 既有载体的并集 + register 索引；不是新存储。
- **Decision Transmission（决策传递）**：派发载荷中的决策块 + 子代理确认。
- **Implementation Receipt（实施回执）**：回传中的 `implementation_receipt`，把实施结果钉回 `decision_id`。

### Decision Record Field Ownership (closed)

每字段恰有一个定义所有者；载体保留自己的排版，MUST NOT 改名或另立取值域。

| Field | 定义所有者（取值域/形态） | 载体/登记所有者 | 说明 |
|-------|--------------------------|------------------|------|
| `decision_id` | `decision-definitions.md`（`D-NNN` 形态） | `.specify/register.md`（登记） | 编号在诞生时登记；引用同时给载体指针 |
| `decision_class` | 同上（闭集 `human-interactive` / `ai-autonomous`） | 同上 | 类决定模板与检查集 |
| context | 同上（内容下限） | 各载体 | 决策所处情境与约束 |
| options / chosen option | 同上（五要素与闭集） | 各载体 | 承重决策的理据由 `T-NNN` 承载 |
| rationale | 同上（一般）；承重时指向 `T-NNN` | `decision-tension.md`（承重六字段） | 一处事实一个定义点 |
| evidence pointers | 同上（必须可解析） | 各证据载体（feedback/evidence/artifact） | 指针解析义务归本契约 |
| actor | `superagent-definitions.md`（边身份）/ run 身份 | 各载体 | 谁持有/实施了该决策 |
| timestamps | `decision-definitions.md`（创建/传递/确认/实施四个时点） | 各载体自己的时间格式 | 四个时点必须齐全 |
| `transmission_status` | `decision-definitions.md`（值域在其页声明） | run report / 角色边载体 | 传递与确认状态 |
| implementation status | `decision-definitions.md`（值域在其页声明） | 实施回执 + 产物 | 由回执驱动；是 [[STR-007]] 状态面承载的实施结果维度，不是第 11 个记录字段（FR-014 封闭集不变；见 § Clarifications 2026-11-25） |

### Enforcement Boundary (closed)

| Rule ID | Rule | Judge（承接面） | 转红条件 | 覆盖声明 |
|---------|------|----------------|----------|----------|
| M-01 | 决策记录字段/类取值/时间戳形态 | 确定性守卫 | 缺字段、类值域外、四个时点缺失或形态错 | 机器覆盖 |
| M-02 | 同名冲突的定位信息 | 确定性守卫 | `same_name_conflict: true` 且 `resource_locator` 空或具名维度数低于下限 | 机器覆盖（只判在场与维度数） |
| M-03 | 选项闭集 | 确定性守卫 | 空集、重复标签、`other` 无 `path`、五要素缺失 | 机器覆盖 |
| M-04 | 决策编号（只判新式记录） | 确定性守卫 | 新式记录（`^### D-\d{3}` 标题且携带记录字段文法）的 `D-NNN` 形态错、同载体不密集、register 不可解析；legacy 标题与 register 行不判 | 机器覆盖 |
| M-05 | 实施回执 | 确定性守卫 | 回执缺失、`decision_id` 缺失或不可解析 | 机器覆盖 |
| M-06 | 派发决策块 | 确定性守卫 | 决策 backed 派发缺决策块或块缺字段 | 机器覆盖 |
| M-07 | 审计链 | 确定性守卫 | 记录/派发/回执三段任一缺失或编号不一致 | 机器覆盖 |
| M-08 | 已登记简称 | 确定性守卫 | 主体命中 glossary variant 且 canonical 存在 | 机器覆盖（只覆盖已登记词） |
| M-09 | evidence 指针可解析 | 确定性守卫 | 任一 evidence 指针不可解析（指向的载体路径/锚不存在或不可读） | 机器覆盖（只判可解析，不判证据是否充分） |
| B-01 | 名称完整性 | `/speckit.review` 产物段 + 人工决策评审 | 未登记简称或名称不足以指认 | 行为类，不声称机器覆盖 |
| B-02 | 定位充分性 | `/speckit.review` 产物段 + 人工决策评审 | 维度不足以区分同名对象 | 行为类 |
| B-03 | 人工可读性/后果真实性 | 人工决策评审 + `/speckit.review` 产物段 | 行话无解释、后果/可逆性陈述失真 | 行为类 |
| B-04 | AI 严谨性 | `/speckit.analyze` + `/speckit.review` | 谓词不可执行、假设缺失、结论不可重放 | 行为类 |
| B-05 | 理由充分性 | `/speckit.analyze` + `/speckit.review` | 理由未支撑选中项或与证据矛盾 | 行为类 |
| B-06 | 类别正确性 | `/speckit.review` 产物段 | 类别与持有者不符（如无人值守却标 human-interactive 且未停等） | 行为类 |

### Landing & Compatibility Inventory (candidates; plan owns the closed list)

以下为已知候选，plan MUST 将其细化为封闭的 § Backward-Incompatible Change Inventory 并逐行给出迁移/拒绝行为与证据；任一未映射行使守卫转红（FR-029）。

| BC ID | Change | 兼容影响 | 预置结局（闭集） |
|-------|--------|----------|------------------|
| BC-01 | 既有载体新增决策记录块 | 旧记录无块 | `compatibility-bridge`（无块 = legacy，可读不判错） |
| BC-02 | 派发载荷新增决策块 | 非决策派发无块 | `compatibility-bridge`（无块合法）；决策 backed 无块 `migrate:refuse` |
| BC-03 | 新增 `D-NNN` 编号族行 | 与既有 `D1–D9`/`D-001` 并存 | `compatibility-bridge`（分组登记；冲突走 renumber 修复） |
| BC-04 | instruction 模板新增段 | 生成指令变化 | `compatibility-bridge`（managed-section 保留自定义内容；client refresh 收到） |
| BC-05 | 新守卫面对旧记录 | 旧记录可能不满足新形态 | `compatibility-bridge`（只判新块；旧记录报告 legacy） |
| BC-06 | 两条生产规则生效 | 既有决策文本可能含简称/缺定位 | `compatibility-bridge`（只约束新决策；评审报告 legacy） |

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时依赖、不新增第三方包——它交付规则所有者页、模板段、载荷契约、守卫与契约测试，并消费既有 Python 解释器、pytest 运行器、唯一测试入口、既有派发载体与既有检查器。表中 `Premises` 引用的 `EP-NNN` 由 plan 阶段 `## Execution Premises` 定义（本阶段不建 premises 表）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库（守卫与契约测试的文本解析、fixture 构造） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 既有 `requires-python`；本特性零新增第三方依赖 | `pyproject.toml` | 新增测试在 `>=3.8` 解释器上经唯一入口通过；新增第三方 import 为零 | FR-022, FR-024 | EP-001 |
| RS-002 | `pytest` 测试运行器（契约 / 单元测试） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 既有 pytest 声明；零新增依赖 | `pyproject.toml` | 经 `scripts/bash/run-tests.sh` 运行新增测试，相对入口基线零新增名字级失败 | FR-024 | EP-001 |
| RS-003 | POSIX `bash` 运行时（唯一测试入口） | signed-contract | bash 上游 / 运行环境（本仓只消费） | 不新增显式版本下限；本特性不改该入口 | `scripts/bash/run-tests.sh` | 新增测试全部经该入口执行且一次退出 0 | FR-024 | EP-001 |
| RS-004 | 既有派发载体与角色边契约（run-agent / run-team / driver 载荷与回传） | in-scope | 本特性修改的 framework 源技能与定义页 | 不适用（仓内实现，无外部版本面） | `shared/definitions/superagent-definitions.md` | 派发夹具含决策块与实施回执；缺块拒绝；回传缺项不被消费 | FR-018, FR-019, FR-020, FR-021 | EP-002 |
| RS-005 | 既有确定性检查器面（`validate-*`、`scan-confirmation-gates.py`、contract 测试） | in-scope | 本特性扩展的 framework 源脚本与测试 | 不适用（仓内实现） | `scripts/python/validate-requirements.py` | 每个守卫的逆向样本转红；`scan-confirmation-gates.py` 零新增命中 | FR-022, FR-024, FR-025 | EP-003 |
| RS-006 | 既有 instruction 生成与镜像/副本工具（managed-section 生成、镜像同步、命令副本再生成） | in-scope | 本特性修改的框架源与工具链 | 不适用（仓内实现） | `scripts/python/sync-mirrors.py` | instruction 模板与活副本一致且字节上限内；`regen-command-copies.py --check` rc 0；`sync-mirrors` 漂移无新增成员 | FR-026, FR-027 | EP-004 |

**Contract-cell note**: 每个 `Contract` 单元格只放一个仓内可解析路径；`RS-004`–`RS-006` 指向本特性修改的既有代表文件，不是第二契约。既有载荷与镜像机制在本次扩展中保持其既有协议，义务只在新增的决策块与记录形态上。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 决策生产者清单封闭：以本规格 § Decision Producer Inventory 为声明集、以实现期代码面扫描为观测集，按生产者身份比较，观测集 MUST 等于声明集（允许差异 = 清单明确登记的 `exempt` 行）；任一未登记的生产者产出决策项 MUST 使守卫转红。**Path**: final
- **SC-002**: 两条生产事故被挡住：夹具 A（同名资源，[[STR-006]] 为 true 但无 [[STR-005]]）触发 M-02 转红，补业务资源组 + region id 后转绿；夹具 B（主体命中已登记 glossary variant）触发 M-08 转红，改完整名称后转绿；两条规则同时出现在生成的 instruction 与所有者页。**Path**: final
- **SC-003**: 两类决策分离：类缺失/值域外触发 M-01 转红；`human-interactive` 夹具含 FR-008 的全部要素并通过 B-03 评审；`ai-autonomous` 夹具含 FR-009 的全部要素并通过 B-04 评审；类别与持有者不符触发 B-06 评审发现。**Path**: final
- **SC-004**: 选项闭集：空选项集、重复标签、`other` 无 `path`、五要素缺失分别触发 M-03 转红；补齐后转绿；`ai-autonomous` 的选中项经记录输入 + 谓词重放一致。**Path**: final
- **SC-005**: 归档可重建：对夹具决策集（覆盖 requirements/plan/checkpoint/run report 四类载体），仅用 register + 载体即可重建 FR-014 的全部字段；删任一字段触发 M-01（`decision_id` 不可解析时另由 M-04 判）转红，改坏任一 evidence 指针触发 M-09 转红；承重决策的记录不含六字段副本且 `T-NNN` 可解析。**Path**: final
- **SC-006**: 传递与实施可审计：决策 backed 派发含完整决策块（M-06 绿），回传含确认与 [[STR-008]]（M-05 绿），三段链可解析（M-07 绿）；静默改选夹具产生显式异常；无记录决策派发被拒绝；缺 [[STR-009]] 的回执使 M-05 转红。**Path**: final
- **SC-007**: 强制诚实：§ Enforcement Boundary 的每条 M 规则都有对应守卫与一个逆向样本，逐条 mutation 演练全部转红且定位到规则；每条 B 规则都有具名承接面；守卫清单与两表逐行一致，缺一即红。**Path**: supporting
- **SC-008**: 落地与镜像干净：`regen-command-copies.py --check` rc 0；`sync-mirrors.py --check` 的漂移成员集相对基线无新增成员（绝对读数如实报告）；instruction 模板与活副本的「Decision Items」段逐字一致且在声明的字节上限内；`scan-confirmation-gates.py` 零新增门控命中；空客户项目 init 夹具收到该段。**Path**: supporting
- **SC-009**: 兼容与迁移闭包：base `fbab7a45c` 的既有决策记录正文零改写（行级零删除读数：既有记录行零删除、零改写，追加与新增文件允许）；旧形态记录被报告为 `legacy` 且可解析；plan § Backward-Incompatible Change Inventory 的每一行都映射到一条被测试的迁移或确定性拒绝行为，未映射行使守卫转红。**Path**: supporting
- **SC-010**: instruction 最低门槛生效：生成的 `.specify/instructions.md`（含每工具兼容副本）包含「Decision Items」指针段、两条生产规则与两类强调，且在 A-13 声明的字节上限内。**Path**: final

### Measurement Sources & Collection Methods

- **SC-001 Source**: 本规格清单的声明集 + 实现期对 `templates/`、`skills/`、`agents/`、`scripts/`、`src/` 的决策入口扫描输出；守卫测试断言「观测 = 声明」并附扫描命令与输出。实现与 review 各一次。
- **SC-002 Source**: 两个生产事故夹具（结构化记录 + 生成的 instruction 文本）；M-02/M-08 的退出码与消息；`grep` 指令面命中；评审 B-01 的发现记录。实现与 review 各一次。
- **SC-003 Source**: 两类模板夹具与评审记录（B-03/B-04/B-06）；M-01 的退出码。实现与 review 各一次。
- **SC-004 Source**: 选项集夹具（空/重复/`other`/缺要素）与 M-03 输出；AI 决策重放脚本输出。实现一次。
- **SC-005 Source**: 四类载体夹具 + register 夹具；重建脚本/runbook 输出；M-01/M-04/M-09 输出；`T-NNN` 交叉引用检查结果。实现与 review 各一次。
- **SC-006 Source**: 派发载荷快照、回传快照、run report；M-05/M-06/M-07 输出；fast-fail 上送件样例。实现与 review 各一次。
- **SC-007 Source**: mutation 演练记录（逐守卫的逆向样本执行输出）；§ Enforcement Boundary 与守卫清单的对照表；评审承接面清单。实现与 review 各一次。
- **SC-008 Source**: `regen-command-copies.py --check` 的 rc 与输出；`sync-mirrors.py --check` 的 rc、输出与相对基线 `test-evidence/sync-mirrors-baseline.txt` 的成员集差值；instruction 模板/活副本 `cmp` 与字节计数；`scan-confirmation-gates.py` 的 `violations` 输出；空项目 init 的树与指令片段。实现与 review 各一次。
- **SC-009 Source**: `git diff --numstat <base>..HEAD -- <既有记录路径集>` 的零删除读数（既有文件删除列 = 0、无删除文件；追加与新增文件允许）；旧记录解析夹具与 `legacy` 报告；plan § Backward-Incompatible Change Inventory + `/speckit.migrate` dry-run/apply/refuse 读数。实现与 review 各一次。
- **SC-010 Source**: `.specify/instructions.md` 与每工具副本的段抽取；字节计数（`wc -c`）；模板与活副本的 `cmp`。实现一次。

## Shared Strings

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "shared/definitions/decision-definitions.md" | FR-001, FR-030 |
| `STR-002` | "decision_class" | FR-006, FR-014 |
| `STR-003` | "human-interactive" | FR-006, FR-008 |
| `STR-004` | "ai-autonomous" | FR-006, FR-009 |
| `STR-005` | "resource_locator" | FR-007, SC-002 |
| `STR-006` | "same_name_conflict" | FR-007, FR-022 |
| `STR-007` | "transmission_status" | FR-014, FR-019 |
| `STR-008` | "implementation_receipt" | FR-019, SC-006 |
| `STR-009` | "decision_id" | FR-014, FR-019, FR-022, SC-006 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-11-25（无人值守 requirements 阶段，自行裁决并记录）

- Q: 用户原文「单不限于」「subgent」如何处置？ → A: 按输入校正读作「包括但不限于」「subagent」；不改变需求语义，见头部输入校正。
- Q: 是否为决策新建一个登记册/存储？ → A: 否（A-3、FR-004）。决策档案是「封闭生产者清单 × 既有载体」的投影；`.specify/register.md` 仍是编号唯一索引；没有第二台账。
- Q: 「每个决策都要归档」的边界是什么？ → A: 由封闭生产者清单界定（A-5、FR-003）：清单内生产者产出的决策项必须留记录；in-passing correction 与普通设计细节不是决策项；清单外入口产出决策项即缺陷。
- Q: 两类决策如何判定，是否与既有授权级别轴冲突？ → A: 按持有者判定（A-4）：`human-interactive` = 人持有；`ai-autonomous` = agent 在无用户在场时持有。与 `confirmation-gates.md` 的授权级别轴正交，不复述其取值域。
- Q: 决策编号用什么形态？ → A: `D-NNN`（沿用 register 已列的 `D-…` 编号族；先例 087 `D-001`），按载体密集、不复用，register 登记（A-6、FR-015）。
- Q: 传递是否要改派发载荷的七字段？ → A: 不改变七角色字段与四项既有注入；决策块搭乘既有载荷通道，作为任务权威内容（A-7、FR-018）。若实现需要改变字段数/注入清单，须有记录在案的裁定。
- Q: 承重决策与 `decision-tension.md` 的关系？ → A: 承重决策**追加**一条决策记录并交叉引用 `T-NNN`；六字段内容只在张力记录中定义，决策记录不复制（FR-017）。
- Q: 哪些规则必须能转红、哪些只能评审？ → A: 按 A-9 与 § Enforcement Boundary：M 规则有守卫与逆向样本；B 规则有具名评审承接面，不得声称机器覆盖（FR-022、FR-023、FR-024）。
- Q: 存量记录怎么办？ → A: 新契约只约束落地后新建的记录；旧记录零改写、报告 `legacy`、可解析（FR-028）；不兼容形态由 `/speckit.migrate` 迁移或确定性拒绝（FR-029）。
- Q: 两只生产 instruction 是否只加在模板？ → A: 否。它们是**最低门槛**：所有者页、instruction 段、决策项模板、守卫/评审四处都落（A-8、FR-010、FR-026）。
- Q: 词汇表新词是否直接写入？ → A: 只提议（`origin=auto`、`status=proposed`），未确认不写（A-11、FR-005）。
- Q: `Related Feature` 绑定？ → A: 保持 `Need clarification`，由 `/speckit.clarify` 绑定（A-12）；本规格的基线语料不构成绑定。
- Q: 本阶段脚手架若脚本会派生新编号分支怎么办？ → A: 本规格必须使用编号 107；因当前已在 `107-decision-governance` 分支且脚本的编号推导会把当前分支计入而派生 108，按简报「不得创建第二个分支、在当前分支继续并记录偏差」的裁定，采用等价的手工脚手架（复制 `.specify/templates/requirements-template.md` 并替换输入描述），偏差记录于 `test-evidence/requirements-stage-2026-11-25.md`。

### Session 2026-11-25（无人值守 clarify 阶段，自行裁决并记录）

- Q: `Related Feature` 绑定到哪个既有 Feature，还是新建？ → A: 新建 **Feature 107 Decision Governance**。候选 046 / 076 / 053 / 095 / 090 逐一核对：均只拥有相邻窄面（门控分类、承重取舍六字段、机器可判边界、角色边载荷、重载与处置），无既有 Feature 承担一般决策项契约；本规格 A-2 声明新概念与新所有者页 `shared/definitions/decision-definitions.md`；各候选的 sibling 规格集均仅 1 份，绑定先例指向 create。编号 107 与分支名、`REQUIREMENT_ID` 一致，106 已被并行线 `106-background-silent-failure` 占用。
- Q: 本规格与上述候选是什么父子/切片关系？ → A: **独立特性，不是任何候选的切片**；五处相邻所有者只新增指针行与交叉引用（FR-002），不承担父级归属。归属裁决与交叉引用记录于 `.specify/features/107-decision-governance.md` § Overview / § Related Files；索引行与 `Total Features` 同批更新，邻接 Feature 076 详情新增反向交叉引用。
- Q: `implementation status` 是否属于决策记录封闭字段集？（FR-014 闭集未列；§ Decision Record Field Ownership 列出该行；FR-019 要求回执更新记录的 `transmission_status` 实施状态） → A: 不新增第 11 个记录字段。FR-014 的封闭集是成员资格权威（「缺任一字段即缺陷」）；`implementation status` 是记录 `transmission_status` 状态面承载的实施结果维度（值域由所有者页声明、由实施回执驱动、由 M-05 回执守卫覆盖），不单独成为记录字段；已在 § Decision Record Field Ownership 该行 说明 中写明，排除第 11 字段读法。
- Q: FR-030 末句「`ready-for-clarify` 的 Feature 绑定仍由 `/speckit.clarify` 完成」在本次绑定后如何收口？ → A: 按实际结果更新为「`Related Feature` 绑定已由 2026-11-25 的 `/speckit.clarify` 完成（Feature 107）」；不保留悬而未决的绑定义务，避免 plan/tasks 派生幻影任务。

### Session 2026-11-26（无人值守 analyze 修复，自行裁决并记录）

- Q: A-9 把「引用可解析」划入机器可判集、FR-016 把不可解析 evidence 指针定为缺陷，但封闭 M 表（M-01…M-08）没有承接行，SC-005 却把「改坏指针」映射到 M-01/M-04——怎么办？ → A: 新增 **M-09**（evidence 指针可解析：确定性守卫，只判解析不判充分性），封闭 M 表扩为 M-01…M-09；M-01/M-04 的转红条件不变，SC-005 的指针破坏读数改映射到 M-09。折叠进 M-01 的读法被拒：那会改变 M-01 已声明的转红条件（字段在场/类取值/时间戳形态），且仍无具名规则承接 A-9 的「引用可解析」。
- Q: P-09 把 superagent→subagent 传递的类别固定为 `ai-autonomous` 且义务写作 `record`，与 A-4（类别看持有者）和 FR-014（一条决策项恰一条记录）如何一致？ → A: 传递不产生新决策项——被传递决策的**唯一**记录是其在产出载体的记录；决策块的 `decision_class` MUST 与该记录一致（人持有的决策被交办实施仍为 `human-interactive`）；传递与实施回执 MUST NOT 生成第二条记录，只更新该记录的 `transmission_status` 与审计链（FR-014、FR-018、FR-019、FR-021）。
- Q: C-502 的零改写验收读数（`08b59695c..HEAD` 文件级空 diff）在 plan 落地后已不可满足，如何重述？ → A: 改为**行级包含**读数：既有记录路径上 `git diff --numstat` 的删除列为 0、无删除文件，追加与新增文件（如 register 的 `T-019…T-021` 行、新 `plan.md`）允许且属预期；文件级空 diff 只适用于本特性未触碰的记录路径（与 tasks § Notes「零改写读数」一致）。
