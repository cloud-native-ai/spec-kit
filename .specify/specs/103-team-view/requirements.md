# Requirements Specification: /speckit.team view — 团队结构与状态只读呈现（Team View）

**Requirement Branch**: `103-team-view`
**Created**: 2026-11-24
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（编写/修订 `templates/commands/**`、`skills/internal/**`、`shared/definitions/**`、`scripts/python/**` 与 `.specify/specs/**` 的维护者）与下游项目中使用 `/speckit.team` 查看团队结构与运行状态、需要判定「view 呈现什么、依据哪份定义、缺失数据如何标注」的维护者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 当需要判定「view 是什么、不做什么」「一次完整呈现包含哪些信息组、每个字段的真源在哪」「无 slug / 未知 slug / 空档案 / 损坏定义时行为如何」「view 与 modify、run 的路由冲突如何裁决」「view 是否写盘、是否调用引擎、是否运行五查预检」「文档与发现性需要哪些同步」「如何确定性验收」时打开本规格，据 FR-001…FR-021 与 SC-001…SC-007 决定 `/speckit.clarify` 与后续实现是否放行
**Input**: User description: "需要 /speckit.team 命令中，在 create/modify/run 结构之外再增加一个 view 子命令，用来完整详细地呈现 team 的结构和状态（只读呈现：不创建、不修改、不运行、不写 team 定义或 run 记录）。"

**输入校正**：「子team命令」按「/speckit.team 命令」理解（明显笔误，不改变语义）。

## Related Feature *(mandatory)*

**Feature ID**: Need clarification
**Feature Name**: Need clarification

## Overview

`/speckit.team` 当前是团队操作的单一入口，恰好三个模式——create、modify、run。三者都带写权或执行权：create / modify 改写团队定义，run 登记 run line、派发席位并产出运行报告。于是「只是想看清楚这个团队长什么样、现在处于什么状态」没有任何只读入口：读者要么手工打开 `.specify/teams/<slug>/team.md`、`runs/`、`items.jsonl` 逐处拼读，要么走 run 模式——而 run 会登记 line、派发席位、产生运行报告，代价与副作用都远超「查看」。

本特性在既有三模式之外新增第四个模式 **view**，把「团队的结构与状态」收敛为一次**只读呈现**：

1. **职责边界**——view 只读：不创建、不修改、不运行；不写 team 定义、run 报告、台账、summary、锚点/目标档案、registry、状态文件或 run line；不派发席位。一次 view 运行后工作树零变更。
2. **「完整详细」的对象**——一个团队的六组信息：身份与绑定（含 binding 记录、绑定锚点身份）、静态结构（Role × Stage × Type 名册与领地）、动态结构（pattern 与全部声明的配置）、持久化位置与产物清单（定义、运行报告、台账、持续运营脊柱、summary 送达位置）、最近运行状态（报告清单、最新报告的有界摘要、台账聚合、遗留异常信号）、其他归档层引用（`handoff_ref`、绑定锚点状态与 Target 列表——按身份引用，不复制内容）。
3. **输入形态**——`view <slug>` 呈现单个团队；无 slug 呈现全部团队概览；团队不存在报「team not found」并建议 create；档案为空显式声明；定义损坏（目录在而 `team.md` 缺失/不可读）与「不存在」区分报告。
4. **输出契约**——面向人的聊天渲染；字段真源是概念模型、`team.md` schema 与 `goal-utils.py` 引擎，view 引用而不复制；固定规则的提取（定义解析、档案枚举、报告清单、台账聚合、最新报告摘要）由确定性只读程序完成，不经散文重推。
5. **入口接线**——`templates/commands/team.md` 的模式表、路由流、默认行为、歧义能力清单与 frontmatter 声明加入 view；委派给新的只读内部技能 `view-team`。
6. **文档与发现性**——`docs/reference/commands/team.md` 同步四模式并在同一变更中校正两处既有 run 模式陈述漂移；feature registry 绑定归 `/speckit.clarify`，README 不承载模式枚举。
7. **质量与测试**——契约测试钉住模板/技能/文档接线，单元/集成测试用 fixture 覆盖字段渲染、缺失三态、错误路径与只读性；唯一测试入口 `scripts/bash/run-tests.sh`。

**不做什么**：不新建第二套团队存储、状态缓存或快照；不把 view 变成 run 的预检面（五查预检与 `blocked` 判定仍归 run 预览）；不新增面向用户的机器可读输出格式；不改动既有 create / modify / run 的语义与写权；不写镜像 `.specify/**`（由 `scripts/python/sync-mirrors.py` 再生成）。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **类别判定 = `execution`**：交付物是命令模板、技能、确定性读取程序与测试，验收时被机器执行/解析。 | 按验收 oracle 判定：缺陷只在机器执行/断言时暴露，而非读者读错。 |
| **A-2** | **委派载体 = 新的只读内部技能 `view-team`**（源 `skills/internal/view-team/SKILL.md`）。不并入 create-team / improve-team / run-team。 | 团队模式已按单一职责拆分（run-team 先例）；把只读呈现塞进持写权/执行权的技能会让边界含混。命令模板保持「只路由」。 |
| **A-3** | **路由裁决**：显式查看意图（查看/展示/呈现/结构/状态/详情/概览/overview/status/inspect/show）→ view；create/modify/run 意图 MUST NOT 落到 view；**歧义的非空输入不自动选 view**——保持命令既有「不猜」契约，报告四项能力并请求意图。 | 只读回退是可选项而非义务；/speckit.team 既有契约禁止静默猜测。`--target` 是 run 的参数，view 携带时报模式/参数冲突，不静默丢弃。 |
| **A-4** | **「完整详细」的边界**：定义的全部字段与成员行、全部运行报告文件名（逆时序、附总数；如设显示上限须报省略数）、最新报告的有界摘要（Outcome、Target 指派行、Result Summary 摘录、Verification 摘录、Nested SDD Runs 的 anomalies 值）；旧报告只列名不展开。 | 「完整」覆盖当前结构与状态；报告正文无界，全量转写违反 token 效率纪律。 |
| **A-5** | **不新增面向用户的机器可读输出格式**。机器问题由引擎既有读动作（`--json`）回答；确定性读取程序的中间数据不是对外契约。 | 避免第二份格式与第二套语义；既有引擎已提供机器读面。 |
| **A-6** | **绑定/锚点事实只来自引擎读动作**（`goal-utils.py binding`、`list`、`targets --list`），不重解析、不另立解析规则。**团队枚举无引擎动作**（`list --scope teams` 被引擎声明为 scope-not-applicable），按命令既有约定扫描 `.specify/teams/*/team.md`；若引擎将来提供团队枚举动作，view 应切换（未来修订点）。 | One Source Of Truth：引擎是定义语义的唯一判定点；目录扫描是既有的公开约定。 |
| **A-7** | **view 不渲染五查预检与 `blocked` 判定**：那是 run 预览的职责。view 只呈现已持久化状态与绑定事实（含「绑定悬空」这一事实），不冒充运行前置判定。 | 防止 view 被读成 run 的替代预览面；两种模式的职责不混。 |
| **A-8** | **状态诚实**：未记录 ≠ 无异常；缺失 / 为空 / 不可读三态必须区分，禁止静默省略或编造零值。 | 与反馈/证据纪律一致：沉默不得被读作干净。 |
| **A-9** | **既有文档漂移在同一变更中校正（前提纠正 P-1）**：`docs/reference/commands/team.md` 把 run 委派写成 `create-team`（执行路径）且把预览描述为阻断确认门；而模板自 057 起路由到 `run-team` 技能、预览是披露而非门禁。以模板/技能为唯一记录意图，同步更正。 | 唯一读法与记录意图一致（run-team 技能存在）；编辑同一文档时保留已知漂移违反根因修复纪律。 |
| **A-10** | **Feature 绑定留待 `/speckit.clarify`**：`Related Feature` 保持默认 `Need clarification`。 | `create-requirements` 技能约定：本阶段不查表、不建 Feature。 |
| **A-11** | **不新增 glossary 词条**：`view` 是通用词，且 anchor/goal 的 view 模式均未登记词条；「Team View」不是新实体，只是既有 `/speckit.team` 的第四模式。 | 词汇表只登记项目域术语；遵循既有先例，避免为模式名单列实体。 |
| **A-12** | **view 无自身状态**：不写缓存、快照、索引或运行记录；每次运行从定义与引擎实时读取。 | 零新增 store/registry 的合规底线。 |
| **A-13** | **渲染语言**：沿用项目双语表述——字段标识（slug、pattern、lifecycle 取值、路径、模式名）保留原样，说明用中文；受 user-facing comprehension 的行话与上下文规则约束。 | 用户可读性与双语表述纪律。 |
| **A-14** | **输入校正**：「子team命令」→「/speckit.team 命令」（笔误，语义不变）。 | 事实与逻辑检查；不改变需求含义。 |
| **A-15** | **两顶帽子**：源面为 `templates/commands/team.md`、`skills/internal/view-team/**`、确定性读取程序（路径由 plan 定稿）、`docs/reference/commands/team.md`、`tests/**`；`.specify/**` 镜像由 `scripts/python/sync-mirrors.py` 再生成，不手改。 | 本仓为 framework source；手改镜像会在同步时丢失且破坏单一来源。 |
| **A-16** | **确定性读取程序**：候选路径 `scripts/python/team-view.py`（只读、组合引擎读动作）；名称/路径由 plan 定稿。若实现选择扩展 `goal-utils.py` 的只读动作，同样满足 FR-014，但 MUST NOT 改变既有动作语义。 | 固定规则提取归程序（Program-First）；路径留给 plan 以免 requirements 硬编码猜测。 |
| **A-17** | **最新报告摘要按报表契约读取**（owner：`skills/internal/create-team/SKILL.md` § Report contract），旧报告缺段按「未记录」标注，不推断。 | 报表段名与字段有唯一 owner；view 只消费不定义。 |
| **A-18** | **Type 维度取自定义文件的 `## Static Structure` 授权矩阵**：frontmatter `members` 不含 type，view 不推断；正文矩阵与 frontmatter 名册不一致时，view 呈现差异而不裁决。 | 概念模型定义 Type 由矩阵表达；view 是呈现面，不是校正面。 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一次查看看懂一个团队的全部结构与状态 (Priority: P1)

维护者在协作中需要判断「这个团队由哪些席位组成、绑定了哪个锚点、用什么协作模式、上次运行结果如何、还有没有遗留问题」。他输入 `/speckit.team view <slug>`，在一次输出中看到团队的六组信息——身份与绑定、静态结构（Role × Stage × Type 名册与领地）、动态结构（pattern 与全部声明配置）、持久化位置与产物清单、最近运行状态（报告清单、最新报告摘要、台账聚合、遗留异常信号）、其他归档层引用（`handoff_ref`、绑定锚点状态与 Target 列表）；每处缺失都显式标注「未记录 / 为空 / 不可读」，并且这次查看没有改动仓库的任何文件。

**Why this priority**: 这是本特性的核心价值——「完整详细地呈现团队的结构和状态」；没有它，view 模式没有存在意义。

**Independent Test**: 在含一份完整团队定义、至少一份运行报告与一份台账的 fixture 团队上执行一次 view，断言六组信息各自出现且缺失标注正确；同一 fixture 在查看前后的内容哈希一致。

**Acceptance Scenarios**:

1. **Given** 一个含完整定义、运行报告与台账的团队，**When** 执行 `view <slug>`，**Then** 输出包含六组信息，且静态结构的每一名成员、运行报告清单的每一份报告都被覆盖。
2. **Given** 一个只有定义、没有 `runs/` 与 `items.jsonl` 的团队，**When** 执行 `view <slug>`，**Then** 输出成功完成，且「运行报告」「台账」两处显式标注缺失，不出现编造的数字。
3. **Given** 一个绑定锚点已不存在的团队，**When** 执行 `view <slug>`，**Then** 绑定处标注「悬空（dangling）」并给出绑定记录，不静默略过、不自动迁移。

---

### User Story 2 - 不记得 slug 时先看全部团队 (Priority: P1)

维护者只记得「项目里有一批团队」，但记不清某个团队的准确 slug。他输入 `/speckit.team view`（不带 slug），得到按 slug 排序的全部团队概览——每行含 slug、名称、pattern、lifecycle、绑定锚点身份、更新日期与最近运行日期；档案为空时输出「未找到团队」（[[STR-002]]）而不是空白。

**Why this priority**: 无参数的概览是 view 的第二条主路径，直接决定发现性；空档案行为决定首次使用体验。

**Independent Test**: 在含两个团队的 fixture 上执行无参数 view，断言两行且排序确定；在空档案 fixture 上执行，断言显式声明。

**Acceptance Scenarios**:

1. **Given** 档案含多个团队，**When** 执行不带 slug 的 view，**Then** 输出按 slug 升序排列的概览，行数等于团队数。
2. **Given** 团队档案为空，**When** 执行不带 slug 的 view，**Then** 输出 [[STR-002]]，并列出四项能力提示。

---

### User Story 3 - 查看就是查看：只读边界与路由不串线 (Priority: P2)

维护者担心「查看」会顺手改东西或触发运行：他需要确认 view 不写盘、不派发席位、不登记 run line；同时希望「查看结构 / 看看状态」这类意图稳定落到 view，而不是被误路由到 modify 或 run。

**Why this priority**: 只读保证与路由裁决是安全边界；没有它，用户不敢在关键路径上使用 view。

**Independent Test**: 对一组标注了意图的样例输入断言路由结果；在一次 view 前后对 fixture 工作树做内容哈希对比并统计新增/修改/删除文件数。

**Acceptance Scenarios**:

1. **Given** 查看类意图的输入样例，**When** 命令识别意图，**Then** 全部路由到 view，0 条落到 create / modify / run。
2. **Given** create / modify / run 意图的输入样例，**When** 命令识别意图，**Then** 0 条落到 view。
3. **Given** 一个含完整团队的 fixture 仓库，**When** 执行一次 view，**Then** 工作树内容零变更，无新增 run 报告、台账行或 team.md 修改。
4. **Given** 意图歧义的非空输入，**When** 命令无法判定模式，**Then** 报告四项能力并请求意图，不静默执行任何模式（包括 view）。

---

### User Story 4 - 团队不存在时给出可行动的导航 (Priority: P3)

维护者输入了错误或过时的 slug。他需要明确的「找不到」结论、当前可用的 slug 清单，以及下一步该做什么（create），而不是一个模糊错误或静默的空输出。

**Why this priority**: 错误路径决定日常可用性，但价值低于主呈现路径。

**Independent Test**: 对不存在的 slug 执行 view，断言错误字面量与建议；对「目录存在但 team.md 缺失」的损坏定义执行 view，断言报告的是损坏而非不存在。

**Acceptance Scenarios**:

1. **Given** slug 不存在且档案非空，**When** 执行 `view <slug>`，**Then** 输出 [[STR-001]]、可用 slug 清单（有界，若设上限须报省略数）与 create 建议。
2. **Given** slug 不存在且档案为空，**When** 执行 `view <slug>`，**Then** 输出 [[STR-001]]、[[STR-002]] 与 create 建议。
3. **Given** 团队目录存在但 `team.md` 缺失或不可读，**When** 执行 `view <slug>`，**Then** 输出「定义损坏」并点名路径，不把它报告为「不存在」，也不把它渲染成完整团队。

### Edge Cases

- **view 携带 run 专用参数**（如 `--target T-001`）：报告模式/参数冲突并请求澄清，不静默丢弃参数、不自动改走 run。
- **归档团队（`lifecycle_state: archived`）**：正常呈现并标注 archived；view 不拒绝归档团队（拒绝执行为 run 的职责）。
- **旧拼写 `goal_slug` 或缺失 `anchor_slug` 的遗留团队**：按既有推断规则呈现并披露「遗留 / 推断」身份，不迁移、不修复。
- **`runs/` 存在但报告不可读、`items.jsonl` 含无法解析的行**：按「不可读」计数并披露，不中断整次查看。
- **运行报告数量超过显示上限**：报出总数与被省略条数，不静默截断。
- **最新报告缺少报表契约中的必填段**（如 Verification）：按「未记录」标注该段，不以其它段内容代替。
- **团队正文矩阵与 frontmatter 名册不一致**：并列呈现差异，view 不裁决哪一方正确。
- **锚点目录存在、绑定锚点终态（achieved/abandoned）**：呈现锚点状态；view 只报事实，不做运行许可判定。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `/speckit.team` MUST 在 create / modify / run 之外暴露第四个模式 `view`；命令模板 `templates/commands/team.md` 的 frontmatter（`description`、`short-description`、`argument-hint` = [[STR-003]]）、模式表、路由流、无参数默认行为的能力清单与歧义意图的能力清单 MUST 全部包含 view，且 MUST NOT 再声明「恰好三个模式」。
- **FR-002**: 意图路由 MUST 把查看类意图（查看 / 展示 / 呈现 / 结构 / 状态 / 详情 / 概览 / overview / status / inspect / show）识别为 view；create / modify / run 意图 MUST NOT 路由到 view；歧义的非空输入 MUST 报告四项能力并请求意图，MUST NOT 静默执行任何模式（含 view）；`--target` 是 run 专用参数，view 携带它时 MUST 报告模式/参数冲突并请求澄清，MUST NOT 静默丢弃。
- **FR-003**: view MUST 委派给一个专职的只读内部技能（新技能 `view-team`，运行时路径 `.specify/skills/internal/view-team/SKILL.md`）；命令模板 MUST 只保留入口、输入接线与生命周期，MUST NOT 内联呈现逻辑；该技能 MUST NOT 承接 create / modify / run 语义，也 MUST NOT 成为单代理操作入口。
- **FR-004**: view MUST 严格只读：一次 view 运行 MUST NOT 写入或改动任何团队定义、运行报告、台账、持续运营脊柱、summary、锚点/目标档案、feature registry、状态脊、run line 或任何其它文件；MUST NOT 派发席位、执行工作或登记 run line。该约束是可判定的封闭声明：基线 = 运行开始时的工作树内容快照，允许增量 = 空（运行结束后逐路径一致）。
- **FR-005**: `view <slug>` MUST 以精确 slug 匹配解析 `.specify/teams/<slug>/team.md`；MUST NOT 用前缀/模糊匹配静默选中另一个团队。`--scope` 与 `--spec-dir` 按命令既有 Scope 段落透传；view 只在团队档案层解析团队，无法适用的取值 MUST 明确报告，MUST NOT 静默忽略。
- **FR-006**: slug 不存在时，view MUST 输出既有字面量 [[STR-001]]、列出当前可用 slug（有界；若设上限 MUST 报省略条数）或声明档案为空，并指向 create；MUST NOT 自动创建、自动运行或回退到其它模式。团队目录存在但 `team.md` 缺失或不可读时，view MUST 报告「定义损坏」并点名路径，MUST NOT 把它报告为「不存在」，也 MUST NOT 把它渲染成完整团队。
- **FR-007**: 不带 slug 的 view MUST 呈现全部团队概览：每个团队至少含 slug、名称、pattern、lifecycle、绑定锚点身份（含遗留/推断披露）、更新日期与最近运行日期（无运行则标注未记录）；顺序 MUST 按 slug 升序确定；档案为空时 MUST 输出 [[STR-002]]。
- **FR-008**: 单团队 view MUST 呈现身份与绑定组：名称、slug、描述、lifecycle（缺省按 owner 读作 active）、binding 记录（owner / owner_id / origin）与绑定锚点身份；遗留 `goal_slug` 拼写与「未声明 `anchor_slug` 时以自身 slug 推断锚点身份」的既有规则 MUST 被引用并披露，MUST NOT 被静默归一；绑定锚点不可解析时 MUST 标注悬空（dangling）。绑定与锚点答案 MUST 来自引擎的声明读动作（`goal-utils.py` 的 `binding`、`list`、`targets --list`），MUST NOT 由散文重新解析或另立规则。
- **FR-009**: 单团队 view MUST 呈现静态结构：授权矩阵（`## Static Structure` 的 Role × Stage × Type 名册）与 frontmatter 名册事实（每个成员的 role、lifecycle、已声明领地，`seats`、`stage_seats`），成员覆盖 MUST 完整；正文矩阵与 frontmatter 名册不一致时 MUST 并列呈现差异，MUST NOT 自行裁决或修复。
- **FR-010**: 单团队 view MUST 呈现动态结构：pattern 与定义中声明的全部配置（并行度 / DAG / 迭代设置 / 持续运营 cadence / summary 配置 / 优化目标）以及 `focus_target`（若声明）；未声明的可选键 MUST 标注「未声明」，其默认值 MUST 按 owner 指针抵达，MUST NOT 由 view 发明默认。
- **FR-011**: 单团队 view MUST 呈现持久化位置与产物清单：团队目录、`runs/` 报告清单（全部报告文件名，逆时序，附总数；若设显示上限 MUST 报省略条数）、`items.jsonl` 的存在性、行数、按状态的计数与非终态行（状态值域读自台账 owner）、持续运营脊柱文件（`constraints.md` / `STATE.md` / `run-log.jsonl`）的存在性、以及 summary 送达位置（按声明呈现；缺省语义按 owner 指针抵达）。
- **FR-012**: 单团队 view MUST 呈现最近运行状态的有界摘要：最新报告的 Outcome 字段、`**Target 指派**` 行、Result Summary 摘录、Verification 的存在性与摘录、Nested SDD Runs 段的 anomalies 值；各段按报表契约读取，缺失段 MUST 显式标注「未记录」；「未记录异常」MUST NOT 被渲染成「无异常」。
- **FR-013**: 单团队 view MUST 呈现归档层引用：存在 `handoff_ref` 时呈现其路径；绑定锚点可解析时呈现其 lifecycle、判据数量与 Target 列表（经引擎读动作），不可解析时呈现原因；MUST NOT 复制锚点的 objective 或判据正文（身份而非内容），需要时指向 `/speckit.anchor view`。
- **FR-014**: view 依赖的固定规则提取（定义解析、团队档案枚举、运行报告清单、台账聚合、最新报告摘要）MUST 由一个确定性只读程序完成，该程序 MUST 组合引擎的声明读动作、MUST NOT 重新实现定义/生命周期/Target 语义；若以脚本交付，MUST 遵守 Script Interface Contract（`-h` / `--version` 无副作用、拒绝未声明选项）；具体路径与名称由 plan 定稿。
- **FR-015**: 每个必需信息组在无数据时 MUST 区分「缺失（文件/目录不存在）」「为空（存在但无条目）」「不可读（存在但解析失败）」三态并显式标注；MUST NOT 静默省略、MUST NOT 以零值或占位值冒充数据；台账坏行与不可读报告 MUST 计数披露且不中断整次查看。
- **FR-016**: view MUST 声明其数据的 as-of 参照（所用文件时间戳与最新报告时间戳）；MUST NOT 声称实时探测或实时状态。
- **FR-017**: `docs/reference/commands/team.md` MUST 同步为四模式：描述行、When to Use、Syntax、模式表与 view 小节；同一变更中 MUST 校正两处既有 run 模式陈述漂移——run 委派对象改为 `run-team` 技能、预览改为「披露而非阻断门禁」，与命令模板和 run-team 技能一致。
- **FR-018**: Feature 绑定归 `/speckit.clarify`（Feature Integration Protocol）；绑定落地后，实现 MUST 按各自协议同步 `.specify/features.md` 与特性详情文件。README 当前不承载团队模式枚举，故本特性不要求 README 变更；若实现发现任何模式枚举面，MUST 同步。
- **FR-019**: 本特性 MUST NOT 新增第二套团队/运行状态存储、缓存、快照、索引或 registry，也 MUST NOT 复制概念模型、锚点定义或引擎已拥有的枚举与判据；所有对外分发变更 MUST 落在 framework 源面（`templates/`、`skills/`、`scripts/`、`docs/`、`tests/`），`.specify/**` 镜像 MUST 由 `scripts/python/sync-mirrors.py` 再生成而非手改。
- **FR-020**: 遗留形态与生命周期容错：`goal_slug` 旧拼写、缺失 `anchor_slug` 的推断身份、缺失 `runs/` 或 `items.jsonl`、缺失持续运营脊柱文件、`archived` 团队 MUST 都能被呈现并披露状态；view MUST NOT 因这些形态失败，MUST NOT 迁移或修复它们；归档团队 MUST 被标注 archived（view 不拒绝归档团队）。
- **FR-021**: 测试 MUST 覆盖：模板/技能/文档接线的契约测试；确定性读取程序在 fixture 上的单元/集成测试——完整团队、最小团队、未知 slug、空档案、缺失可选产物、遗留拼写、归档生命周期、台账坏行；只读性断言（运行前后工作树不变）；全部测试 MUST 经唯一入口 `scripts/bash/run-tests.sh` 执行并退出 0。

### Key Entities *(include if requirement involves data)*

- **Team Definition**: 团队定义文件 `.specify/teams/<slug>/team.md`（frontmatter + `## Goal` + `## Static Structure` + `## Dynamic Structure` + `## Self-Improvement Contract`）；schema owner 是 `skills/internal/create-team/references/create-mode.md`，view 只读取。
- **Binding Record**: 每个团队携带的三键所有权记录（owner / owner_id / origin）；含义与取值域 owner 是 `shared/definitions/anchor-definitions.md` § The Binding Record。
- **Bound Anchor / Target**: 团队通过 `anchor_slug` 单向引用的锚点及其 Target 清单；view 只按身份引用与引擎读动作呈现，不复制其内容。
- **Run Report**: 每次运行落盘的 `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md`；段名与字段 owner 是 `skills/internal/create-team/SKILL.md` § Report contract。
- **Item Ledger**: 团队目录下的 `items.jsonl`（追加式台账）；字段与状态值域 owner 是 `skills/internal/create-team/references/execution-guide.md` 与 `summary-mapping.md` § 6.5。
- **Continuous Operating Spine**: `continuous` 团队的三件持续运营文件（`constraints.md` / `STATE.md` / `run-log.jsonl`）；owner 是 `skills/internal/create-team/references/operating-loops.md`。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 在含完整定义、至少一份运行报告与一份台账的 fixture 团队上，一次 view 输出覆盖六组必需信息（身份与绑定、静态结构、动态结构、持久化清单、最近运行状态、归档层引用），每组至少出现一个字段，且该 fixture 的全部成员行与全部报告文件名均被覆盖（覆盖数 = fixture 实际数） **Path**: final
- **SC-002**: 一次 view 运行前后，fixture 工作树的内容哈希完全一致，新增 / 修改 / 删除文件数为 0，新增 run 报告、台账行与 team 定义改动数均为 0 **Path**: final
- **SC-003**: 路由样例集（≥1 条查看类意图、≥1 条 create、≥1 条 modify、≥1 条 run、≥1 条歧义）经命令识别后，查看类意图命中 view 的比例为 100%，非查看意图落到 view 的条数为 0，歧义输入执行模式的条数为 0 **Path**: supporting
- **SC-004**: 错误路径 3/3 命中：未知 slug 输出 [[STR-001]] 与 create 建议；空档案输出 [[STR-002]]；损坏定义输出点名路径的「定义损坏」报告 **Path**: supporting
- **SC-005**: 两个具名文件（`templates/commands/team.md`、`docs/reference/commands/team.md`）的模式表各列出 4 个模式，陈旧字面量 [[STR-004]] 在两文件中的实时出现数为 0（固定模式、允许增量为空），且 run 委派对象与预览语义两处漂移已按模板/技能校正 **Path**: supporting
- **SC-006**: 在 fixture 中删除 `runs/`、`items.jsonl` 与最新报告的 Verification 段后，一次 view 成功完成（退出正常、无异常中断）且 3 处缺失全部显式标注，输出中不出现「无异常」式断言 **Path**: supporting
- **SC-007**: 新增与既有相关测试经 `scripts/bash/run-tests.sh` 一次执行退出码为 0，且新增测试覆盖 FR-021 列出的全部 fixture 形态 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: fixture 集成测试的断言结果（六组信息与成员/报告覆盖计数），由 `scripts/bash/run-tests.sh` 执行。
- **SC-002 Source**: 只读性测试对 fixture 工作树做内容哈希快照（测试开始前 / 结束后各一次）并求差。
- **SC-003 Source**: 路由样例集契约测试的逐条通过计数与失败明细。
- **SC-004 Source**: 错误路径测试的断言输出（三场景逐一断言）。
- **SC-005 Source**: 对两个具名文件运行固定模式的计数检查（测试内以程序统计，不靠人读）。
- **SC-006 Source**: 缺失三态 fixture 测试的断言输出。
- **SC-007 Source**: `scripts/bash/run-tests.sh` 的退出码与测试汇总。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"team not found"` | FR-006, SC-004, tests asserting the unknown-slug path |
| `STR-002` | `"No teams found"` | FR-007, SC-004, tests asserting the empty-archive path |
| `STR-003` | `"[create|modify|run|view] [team-slug] [--target <T-<nnn>>]"` | FR-001, command-template contract tests |
| `STR-004` | `"exactly three modes"` | SC-005, doc-sync count test (stale literal that MUST disappear) |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

<!--
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
