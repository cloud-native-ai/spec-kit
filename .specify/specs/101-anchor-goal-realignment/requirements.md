# Requirements Specification: Anchor / Goal Semantic Realignment + Command-Surface Cleanup

**Requirement Branch**: `101-anchor-goal-realignment`
**Created**: 2026-11-12
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（编写/修订 `templates/commands/**`、`skills/internal/**`、`shared/definitions/**`、`scripts/python/goal-utils.py`、`.specify/anchoring/**`、`.specify/teams/**` 与 `.specify/specs/**` 的维护者）与下游项目中使用 `/speckit.anchor`、`/speckit.goal`、`/speckit.team`、需要判定「项目级远期目标与行动级指导各是什么、各自存在哪里、由哪个入口撰写、档案里为什么只剩该留的条目」的维护者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 当需要判定「Anchor 与 Goal 各指什么、谁拥有该定义」「`/speckit.anchor` 与 `/speckit.goal` 各承载哪些模式、调用错误模式时发生什么」「`.specify/anchoring` 里哪些条目保留、哪些迁走、哪些归档、依据什么规则、回执长什么样」「迁移为什么不会丢数据、能否重跑与中断续做」「团队绑定的字段为何从 `goal_slug` 变成 `anchor_slug`、悬空绑定怎么修」「哪些活文档、词表、台账、探针、测试必须同步改，哪些日期化记录必须保持原字节」时打开本规格，据 FR-001…FR-071 与 SC-001…SC-010 决定 `/speckit.clarify` 与后续实现是否放行
**Input**: User description: "按照方案B执行无人值守的sdd流程... 按照新的定义goal已经降级为实际行动方面的指导, 而anchor应该是整个项目级别的远期目标." —— 即：**Anchor = 项目级远期目标；Goal = 行动级实际指导**；`/speckit.anchor` 接管旧 `/speckit.goal` 的全部七模式（`create` / `view` / `modify` / `targets` / `migrate` / `migrate-archive` / `coordinate`）；`/speckit.goal` 改为承载新的行动级 Goal；随后清理 `.specify/anchoring`，只保留真正的项目级锚点，把行动级目标迁入新的 Goal 存档，过期条目留下回执后归档（archive-not-delete）。本规格不重写任何日期化历史记录，不推送远端。

## Related Feature *(mandatory)*

**Feature ID**: 101
**Feature Name**: Anchor / Goal Realignment

**Binding note**: 本特性是 **041 Goal Registry** 所建立概念与命令面的**语义反转**（不是其增量扩展），作为独立 Feature 登记（2026-11-12 `/speckit.clarify` 裁定 D-1）：041 保持 `Implemented` 与其日期化记录，只增加一条反向交叉引用。041 把"项目级 Goal"定为一等概念；本特性把它改名为 Anchor，并把 Goal 降为行动级指导。041 的单一入口规则（其 FR-025 / FR-026）以**入口唯一性**为不变量，改名后由 `/speckit.anchor` 继承；其"不得有第二个撰写入口"的约束在本规格以 FR-011 / FR-021 原样保留。094 的"不引入第二套引擎/第二份 schema"（其 FR-001）在本规格以 FR-028 / FR-008 保留。

## Overview

当前活语义与用户裁定相反：`shared/definitions/goal-definitions.md` 把 **Goal** 定义为项目级、`outcome, not steps` 的一等概念，`.specify/anchoring/` 是它的档案；`/speckit.goal` 是它唯一的撰写入口，承载七模式。094 只把目录 `.specify/goal/` 改名为 `.specify/anchoring/`，文件名 `goal.md`、字段 `goal_slug` 与命令面都没有改名。`sdd-routing-definitions.md` 因此把 Goal 画成控制层级最高层。

本特性执行 **Plan B 语义反转**：**Anchor（锚点）**成为项目级、长周期、跨交付物持续追求的远期目标；**Goal（目标）**降为行动级、短周期、可执行的实际指导。命令面对调：`/speckit.anchor`（canonical `templates/commands/anchor.md`）接管旧 `/speckit.goal` 的全部七模式，成为锚点档案的唯一撰写入口；`/speckit.goal` 被改写成四模式（`create` / `view` / `modify` / `status`），只服务行动级 Goal。存储面随之分离：锚点定义文件由 `goal.md` 改名为 `anchor.md`（[[STR-001]]），行动级 Goal 落到新的 `.specify/goals/<goal-slug>/goal.md`（[[STR-002]]），团队绑定字段由 `goal_slug` 改为 `anchor_slug`（[[STR-003]]）。

最后执行**档案清理**：对 `.specify/anchoring/` 现存 14 个条目逐条按规则分类，保留真锚点、把行动级条目迁入 Goal 存档、把过期条目连同回执归档（archive-not-delete）。迁移不改概念载荷、不删数据、可重跑、可中断续做；每个动作留下逐条回执（[[STR-005]]）。所有活文档、词表、台账、探针、团队引用与契约测试同步收敛；037 / 038 / 042 / 074 / 085 / 094、`.specify/archive/**`、`.specify/history/**` 等日期化记录保持原字节。

**不做什么**：不新建第二套定义引擎或第二份 schema（094 FR-001）；不新建第二套归档目录体系（复用 `.specify/archive/` 下新增 `anchoring/` 子目录）；不让 `/speckit.goal` 成为锚点档案的第二个撰写入口；不把行动级 Goal 放进控制层级或团队绑定；不重写日期化历史；不推送远端。

## Assumptions & Decisions *(design choices the user ruling left open; adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **Anchor store**：`.specify/anchoring/<anchor-slug>/anchor.md`；**Goal store**：`.specify/goals/<goal-slug>/goal.md`。 | 概念名必须投影到存储名（Self-Explanatory Structure / Grounded Naming）。Goal 用**复数** `.specify/goals/` 而非历史路径 `.specify/goal/`：后者在 094 已被改名为 `anchoring`，复用会让日期化记录里的旧路径"静默解析到不同数据"——悬空是响亮的，静默错配不是。 |
| **A-2** | **Goal 模式集 = 四模式**：`create` / `view` / `modify` / `status`；`view` 无 slug 时列存档；`status` 报告并转换生命周期状态（`active` / `achieved` / `abandoned`，终态保留，`reopen` 仅限 `owner: human` 且追加历史行），`modify` 编辑指导叙述与完成条件。不含 `targets` / `migrate` / `migrate-archive` / `coordinate`。 | 行动级指导不需要切片授权、团队协调或档案迁移；这四项正是 Plan B 划给 `/speckit.anchor` 的。`status` 语义复用既有生命周期 owner 与引擎 `status` 动作，不新增状态机（D-3）。对旧调用显式拒绝并给指针（FR-020），而不是静默降级。 |
| **A-3** | **`--scope` 成员改为 `anchor` / `teams` / `goals` / `auto`；旧成员 `goal` 直接判非法取值（exit 2），不做别名。** | 094 对 `global` / `spec` 的退役先例就是"直接失败、不静默换值"。别名期会让"哪个 `goal` 才是锚点"长期不可判定。 |
| **A-4** | **团队绑定到 Anchor**，字段 `goal_slug` → `anchor_slug`。 | Plan B 把 `targets` 与 `coordinate`（团队面机械）归 `/speckit.anchor`，因此团队服务的对象就是 Anchor。保留 `goal_slug` 会让 team.md 里的 "goal" 指 Anchor，而 `/speckit.goal` 指行动级 Goal——正是禁止的静默重载。 |
| **A-5** | **最终分类由 plan 依规则裁定并落成分类表**，implement 只执行该表；本规格的 14 条清单是**暂定基线**（见下表），任何偏离必须在分类表中记录规则 id 与证据。 | 用户裁定只给概念，不给条目级判决；但实现者必须有可判定规则，且不能悄悄改判。决策者收敛为 plan 一处，避免同一判决在 plan 与 implement 各答一次。 |
| **A-6** | **过期锚点的归档目的地 = `.specify/archive/anchoring/<slug>/`**（复用既有 `.specify/archive/` 根，不新增回顾面根）。 | archive-not-delete 且不新增目录体系；`.specify/archive/` 已是既有历史根。 |
| **A-7** | **行动级 Goal 不进控制层级、不带 Targets、不被团队绑定**；它可带行动/步骤形文本，不适用 Anchor 的 GD-2 `outcome, not steps` 校验。 | "实际行动方面的指导"本就允许多步骤；把 GD-2 施加于它会自相矛盾。控制层级仍为 Anchor → Team → Agent → SDD run。 |
| **A-8** | **不修订宪法**。 | 宪法没有任何原则以 Goal / Anchor 命名；唯一相关的 XXII Re-Anchoring 讲的是"方向锚 + 规则锚"的运行内纪律，与本实体不冲突。 |
| **A-9** | **非一次性处置回顾面成员更新**：`.specify/anchoring` 与 `.specify/goals` 加入回顾面成员；历史成员 `.specify/goal` 退役，并在 owner 声明中记录退役理由。 | 新存储是持久定义面；回顾面 owner 是封闭集，静默缺席会让"新目录不进回顾"成为默认（D-4）。 |
| **A-10** | **技能拆分**：七模式技能移到 `skills/internal/manage-anchor/`；`skills/internal/manage-goal/` 重写为四模式。 | 技能名与命令名同构；保留"manage-goal 跑七模式"会让技能描述与命令语义互相打脸。 |
| **A-11** | **Feature 绑定**：已由本阶段裁定为新 Feature **101 "Anchor / Goal Realignment"**（见 `Related Feature` 与 D-1）。 | 语义反转是概念反转而非增量扩展；绑定到 041 会让同一 Feature 同时声称两套相反语义。 |
| **A-12** | **引擎就地扩展**：`goal-utils.py` 加一个清晰命名的行动级 Goal 动作组，以及一个清理/迁移动作组（`--check` / `--apply`），不新建可执行体或并行迁移工具。 | brief §3.4 的首选路径；同一数据不设第二个写者（D-4）。 |

### Provisional anchoring inventory (measured 2026-11-12; final call per A-5)

| # | Slug | Provisional classification | Note |
|---|------|---------------------------|------|
| 1 | `086-efficient-test-execution` | anchor | 持续质量属性，按度衡量 |
| 2 | `087-arch-diagram-docs` | anchor | 持续文档架构目标 |
| 3 | `090-re-anchoring` | anchor | 持续纪律目标 |
| 4 | `094-goal-team-parallel` | anchor | 持续模型目标 |
| 5 | `command-logic-as-classified-skills` | anchor | 持续架构目标（带 `summary/`） |
| 6 | `draw-two-layer-structure` | anchor | 持续架构目标 |
| 7 | `script-interface-contract` | anchor | 持续契约目标 |
| 8 | `session-driven-self-improvement` | anchor | 持续机制目标（带 `summary/`） |
| 9 | `skill-layer-install-separation` | anchor | 持续架构目标（带 `summary/`） |
| 10 | `088-speckit-visualization` | action-goal | 单一交付物；带 T-001/T-002 与团队 `088-reporting-dogfood` |
| 11 | `091-auto-git-closeout` | action-goal | 单一机制交付；团队已 archived |
| 12 | `draw-diagram-interactive` | action-goal | 单一能力交付（带 `summary/` 与团队） |
| 13 | `085-sdd-temporary-goal-team` | obsolete | 被后续模型取代 |
| 14 | `post-refactor-mechanism-integrity` | obsolete | 已完成的one-off检查（带 `summary/`） |

Measurement basis: directory listing of `.specify/anchoring/*/`, `goal.md` presence, five `summary/` trees, and the team→slug map; full readings in `test-evidence/requirements-anchor-inventory-2026-11-12.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 项目级远期目标由 Anchor 承载，七模式入口是 `/speckit.anchor` (Priority: P1)

维护者想创建/查看/修改一个项目级远期目标、给它加一个可指派的切片、把某个团队的内联目标迁成定义、协调共享同一目标的两个团队。她使用 `/speckit.anchor`，七种模式与旧 `/speckit.goal` 完全一致；写入仍只经 `goal-utils.py` 落到 `.specify/anchoring/<slug>/anchor.md`；`sdd-routing-definitions.md` 的控制层级以 Anchor 为最高层。

**Why this priority**: 这是用户裁定的第一句——anchor 是项目级远期目标。没有这一步，语义反转只剩文档措辞，命令面仍在说旧话。

**Independent Test**: 在夹具仓库中运行 `/speckit.anchor` 的七模式各一次：定义落在锚点档案、引擎拒绝第二条写路径、旧的 `/speckit.goal targets` 被拒并指向 `/speckit.anchor`；删除 canonical `anchor.md` 模板时契约测试转红。

**Acceptance Scenarios**:

1. **Given** 干净的夹具仓库，**When** 运行 `/speckit.anchor create demo-anchor --objective "…"`，**Then** 定义落到 `.specify/anchoring/demo-anchor/anchor.md`（[[STR-001]]），绑定记录完整，`summary/` 未被创建，且 `goal-utils.py` 是唯一写入者。
2. **Given** 一个已存在的锚点，**When** 运行 `/speckit.anchor targets <slug> --add "…"`，**Then** `## Targets` 由引擎渲染到 `anchor.md`；同一操作经 `/speckit.goal` 调用时被具名拒绝（[[STR-007]]）并给出 `/speckit.anchor` 指针，零写入。
3. **Given** 团队域文档要求声明所服务的对象，**When** 阅读任一活团队页面，**Then** 它说的是绑定 Anchor（`anchor_slug`），不是绑定项目级 Goal。

---

### User Story 2 - 行动级 Goal 有自己的存档、四模式入口与轻量校验 (Priority: P1)

维护者需要写一条短期、可执行的实际指导："这周把 X 能力补上，完成条件是 Y"。她用 `/speckit.goal create`，得到 `.specify/goals/<slug>/goal.md`（[[STR-002]]）；文本可以是步骤形的，不会被 GD-2 以"task list"拒绝；它没有 Targets、不绑定团队、不在控制层级里。

**Why this priority**: 用户裁定的第二句——goal 降为行动级指导。若 Goal 仍复用锚点存储与七模式，语义反转不成立。

**Independent Test**: 用步骤形文本创建 Goal，断言写入 Goal 存档且通过；用同一步骤形文本创建 Anchor，断言仍被 GD-2 拒绝；用 `/speckit.goal targets` 断言具名拒绝与指针。

**Acceptance Scenarios**:

1. **Given** 干净仓库，**When** 运行 `/speckit.goal create sprint-guidance --guidance "1. … 2. …" --done "…"`，**Then** 文件落在 `.specify/goals/sprint-guidance/goal.md`，含绑定记录与 `status: active`，且 `.specify/anchoring/` 零新增。
2. **Given** 同一段步骤形文本，**When** 用于 `/speckit.anchor create`，**Then** 被 GD-2 拒绝（行动级指导与锚点叙述的形状校验不同）。
3. **Given** 一个 Goal 存在，**When** 任何团队尝试以 `anchor_slug: sprint-guidance` 绑定，**Then** 解析失败并具名报告——Goal 不参与 Anchor 身份解析。

---

### User Story 3 - 档案清理：只留真锚点，迁移与归档零丢失、可重跑 (Priority: P1)

维护者运行清理。每个 `.specify/anchoring/` 条目得到 `anchor` / `action-goal` / `obsolete` 三种判决之一，并记录规则 id 与证据；保留项改名为 `anchor.md` 并重生成派生 summary；行动级项迁入 `.specify/goals/`（叙述、判据、生命周期、历史保留；Targets 要么随条目保留为 Anchor，要么逐条原样保留在迁移后的 Goal 正文并记入回执）；过期项移入 `.specify/archive/anchoring/<slug>/`（[[STR-006]]）。每个动作留下逐条回执，重复运行零新增 diff。

**Why this priority**: 用户裁定的第三句——清理。语义模型不落到数据上就只是改名；而清理最容易丢数据，所以必须与迁移安全同优先级。

**Independent Test**: 对真实 14 条目执行分类 → 迁移 → 归档 → 重跑：断言前后概念摘要逐条相等、无删除、无孤立 `summary/`、第二遍输出 `already-migrated` / `already-archived` 且零 diff；在"源已归档、目标未落盘"处中断再续做，断言从报告阶段续做且无无回执删除。

**Acceptance Scenarios**:

1. **Given** 14 个锚点条目与暂定分类基线，**When** 执行分类与清理，**Then** 每个条目有一条带规则 id 的分类记录；`.specify/anchoring/` 下不再有行动级条目，`.specify/goals/` 下出现每条被迁移定义，过期条目位于 `.specify/archive/anchoring/` 且带回执。
2. **Given** 一次已成功完成的迁移，**When** 再次运行，**Then** 退出 0，报告 `already-migrated` / `already-archived`，不产生第二份回执，相对重跑前零新增 diff。
3. **Given** 迁移在"源已归档、目标尚未写入"之间被中断，**When** 再次调用，**Then** 报告中断阶段与实际状态并从该阶段续做，不重复搬迁，不产生无回执删除。
4. **Given** 目标 slug 已存在且概念载荷不等价，**When** 执行迁移，**Then** 拒绝覆盖、指名两个候选、零写入。

---

### User Story 4 - 团队绑定改为 Anchor，零悬空 (Priority: P2)

所有 `team.md` 的 `goal_slug` 经引擎改名为 `anchor_slug`（[[STR-003]]），其余字节不变；每个团队解析到的 Anchor 必须存在。绑在被迁移/归档条目上的团队被逐条处置：改绑到既有 Anchor 并记录理由，或连同回执归档；无法判定的处置停下并具名报告，绝不猜测。两处现存悬空绑定（`viz-skill-arena` → `visualization-skill-selection`、`demo-seat-dispatch` → 自身）被修复或连同回执归档。

**Why this priority**: 绑定是团队运行的五查前提；字段与目标层不同步会让所有团队运行在解析处失败，但它是清理的后果，排在语义与数据之后。

**Independent Test**: 用 20 个真实团队定义（16 个带 `goal_slug`、4 个无绑定）运行改名字段：断言带绑定文件逐文件只改一个键、`goal_slug`（[[STR-008]]）零残留、`anchor_slug` 全部可解析、无绑定文件逐字节不变；注入一个悬空 slug，断言五查与契约测试转红。

**Acceptance Scenarios**:

1. **Given** 20 个团队定义（16 带 `goal_slug`、4 无绑定），**When** 执行结构性字段迁移，**Then** 每个带绑定 `team.md` 的该步 diff 只含 `goal_slug` → `anchor_slug` 一行、其余字节逐字节相同、无绑定文件不变；随后术语归一化步骤对正文中的绑定字段与 `.specify/goal/<slug>/summary/` 引用逐行改写并记入回执，日期化 `runs/**` 保持原字节（D-2）。
2. **Given** `viz-skill-arena` 声明了缺失的 `visualization-skill-selection`，**When** 运行清理，**Then** 该锚点经引擎从团队内联目标落盘（或改绑到既有锚点并记录理由），该团队的 `run-checks` 通过。
3. **Given** 一个团队绑在被迁移的行动级条目上且没有明确归属锚点，**When** 运行清理，**Then** 处置停下并具名报告该团队与两个可选路径，MUST NOT 自动归档或自动改绑。

---

### User Story 5 - 所有活面说同一种话：文档、词表、台账、探针、技能 (Priority: P2)

维护者读到的每个活页面都指向正确的概念：framework-map 有锚点与 Goal 两行；glossary 不再把项目级档案写成 `.specify/goal/`，并明确 Anchor / anchoring archive / Re-Anchoring 三词不同；routing 层级以 Anchor 为顶；flow-class 台账有 `/speckit.anchor` 行；探针登记有 `/speckit.anchor` 的 wrap-up；setup / house-keeping 检查锚点档案而不是历史 `.specify/goal/`；团队域参考使用 `anchor_slug` 与 `.specify/anchoring/<slug>/summary/`。

**Why this priority**: 语义反转的价值取决于下一位读者能否沿名字找到对象；活面不同步会把旧语义悄悄传播下去。

**Independent Test**: 对声明的活根跑一次残留扫描：断言零处把 Goal 定义为项目级、零处以 `/speckit.goal` 作为锚点档案入口、零处使用 `.specify/goal/<slug>/summary/`；注入一句旧语义断言扫描转红；文档站构建通过。

**Acceptance Scenarios**:

1. **Given** 收敛后的仓库，**When** 运行残留扫描，**Then** 三类旧表述在活根中计数为 0；历史根（日期化 specs / archive / history / docs-notes）不计入且保持原字节。
2. **Given** `flow-class-check.py --action check` 与探针编译，**When** 运行，**Then** `/speckit.anchor` 的台账行与 wrap-up 面存在，计数与漂移守卫期望一致。
3. **Given** `sdd-project-setup` 在无锚点的项目上运行，**When** 检查 goals，**Then** 它读 `.specify/anchoring/*/anchor.md` 并报 GAP，而不是读永远不存在的 `.specify/goal/`。

---

### User Story 6 - 维护者能一眼分辨 Anchor 与 Re-Anchoring (Priority: P3)

新读者打开 glossary 或任一 owner 页面，能分清：`Anchor`（项目级持久实体）、`anchoring archive`（存放它的目录）、`Re-Anchoring`（agent 每核心步骤重载方向锚与规则的纪律）。没有任何位置用裸词 "anchoring" 指代行动级 Goal。

**Why this priority**: 术语消歧是长期可维护性的成本项，不阻塞主线，但漏掉会让下一次语义讨论从混乱开始。

**Independent Test**: 按 glossary 与两份 owner 页面判断三词；删除消歧行后，提交前检查转红。

**Acceptance Scenarios**:

1. **Given** glossary 与 `re-anchoring-definitions.md`，**When** 阅读三个词条，**Then** 三者的对象、生命周期与所在目录各不相同且互相引用，读者无需读代码即可复述差异。

---

### Edge Cases

- **同一 slug 同时存在于两个存档**：`--scope auto` MUST 以 exit 2 报 `scope-ambiguous`，不择一胜出。
- **旧调用 `--scope goal`**：MUST 以 argparse `invalid choice` 退出 2；不得被读作 `anchor`。
- **被迁移条目带 `## Targets`**：MUST 要么保留为 Anchor，要么把这些 Target 逐条原样保留在 Goal 正文并写入回执；静默丢弃是阻断缺陷。
- **被归档条目带 `summary/`**：summary MUST 随定义处置或连同回执归档；定义已不存在的孤立 `summary/` MUST NOT 留在锚点档案里。
- **`/speckit.goal targets|migrate|migrate-archive|coordinate`**：MUST 具名拒绝（[[STR-007]]）并指向 `/speckit.anchor`，零写入；不得回退到 `view`。
- **团队绑在被迁移条目上且无明确锚点**：处置 MUST 停下并具名报告；自动归档或自动改绑都不允许。
- **迁移在"源已归档、目标未写"之间中断**：重新调用 MUST 从报告阶段续做，不二次搬运、不留无回执删除。
- **两个分支同时写新存档**：新 Goal 存档 MUST 一文一件（每 slug 一个目录），两分支写不同 slug 时路径不同；共享单一 `.jsonl` 或聚合索引是布局缺陷。
- **日期化记录引用旧路径 `.specify/goal/…` 或 `goal.md`**：保持原字节；其旧路径解析为悬空即正确——不得因"看起来像坏链"而回写历史。
- **`viz-skill-arena` 只有内联目标、没有定义文件**：修复路径 MUST 经引擎 `migrate` 生成 Anchor，而不是手写 `anchor.md`。

## Requirements *(mandatory)*

### Functional Requirements

#### A. Concept ownership and semantics

- **FR-001**: 框架 MUST 把 **Anchor（锚点）** 定义为**项目级、长周期、跨交付物持续追求**的远期目标（authored end state），并在 `.specify/shared/definitions/anchor-definitions.md` 建立其唯一 owner。
- **FR-002**: Anchor owner MUST 在同一处承载 Anchor 的构成（目标叙述 + 可验证成功判据 + 生命周期）、它的档案层与定义文件 [[STR-001]]、**共享绑定记录与生命周期表的唯一 owner**、Target 分解与 Anchor–Team 绑定；其他面（含 Goal owner）MUST 只按路径引用，MUST NOT 复述这些事实。
- **FR-003**: 框架 MUST 把 **Goal（目标）** 重新定义为**行动级、短周期、可执行的实际指导**，并把 `.specify/shared/definitions/goal-definitions.md` 重写为它的唯一 owner。
- **FR-004**: Goal owner MUST 定义 Goal 的构成（指导叙述——MAY 是步骤形；至少一条可验证的完成条件；生命周期）、存档 [[STR-002]] 与身份文法，并按路径引用 FR-002 的绑定记录与生命周期 owner；它 MUST NOT 复述三键或生命周期表，MUST NOT 定义 Targets、团队绑定、coordinate 或任何控制层级位置。
- **FR-005**: 任何活文档 MUST NOT 保留与本规格 FR-001 / FR-003 相反的定义；"a Goal is a project-level end state"及其等价中文表述 MUST 从全部活面消失。
- **FR-006**: 现有 `goal-definitions.md` 中描述项目级概念的内容 MUST 以**保留 git 历史的方式**移入 Anchor owner；该文件随后 MUST 被重写为 Goal owner；两个概念的正文 MUST NOT 在仓内留下第二份副本。
- **FR-007**: Anchor 身份 MUST 为 `.specify/anchoring/` 下的目录 slug（`anchor-slug`），其定义文件 MUST 为 `anchor.md`（由 `goal.md` 改名，[[STR-001]]）；Goal 身份 MUST 为 `.specify/goals/` 下的目录 slug（`goal-slug`），其定义文件 MUST 为 `goal.md`（[[STR-002]]）。
- **FR-008**: 两个概念 MUST 复用同一套生命周期取值 `active` / `achieved` / `abandoned` 与同一条三键绑定记录（`owner` / `owner_id` / `origin`）；MUST NOT 引入第二套生命周期或第二份 schema。
- **FR-009**: **术语消歧**：`Anchor` / `anchoring archive`（持久实体与其目录）与 `Re-Anchoring` / `direction anchor`（运行内规则重载纪律）MUST 在 glossary 与两份 owner 中被明确区分；裸词 "anchoring" MUST NOT 被用来指代行动级 Goal。

#### B. Anchor command surface

- **FR-010**: `/speckit.anchor` MUST 由 canonical `templates/commands/anchor.md` 交付，并 MUST 恰好暴露从旧 `/speckit.goal` 继承的七模式：`create` / `view` / `modify` / `targets` / `migrate` / `migrate-archive` / `coordinate`。
- **FR-011**: `/speckit.anchor` MUST 是锚点档案的唯一撰写入口；除引擎外，任何命令、技能、脚本或运行 MUST NOT 写入 `.specify/anchoring/**`。
- **FR-012**: 命令 MUST 把七模式语义委派给名字与 Anchor 概念一致的技能（`manage-anchor`）；模板 MUST 只保留入口、用户输入处理、glossary 前置与 wrap-up，MUST NOT 复述技能的模式表。
- **FR-013**: 命令 MUST 经既有镜像模型交付（canonical 模板 → `.specify/` 镜像 → 各受支持工具的命令副本），其参考页 MUST 为 `docs/reference/commands/anchor.md`；MUST NOT 手写任何副本。
- **FR-014**: `/speckit.anchor` MUST 在探针登记处拥有一个 wrap-up 探针对象与绑定，并以 `/speckit.anchor` 为 unit-id 把 run determination / exec quant / feedback / docs-sync 编译进模板。
- **FR-015**: `targets` 与 `coordinate` MUST 作用于 Anchor 的 Targets 与绑定该 Anchor 的团队；`migrate` MUST 从团队内联目标派生 Anchor；`migrate-archive` MUST 继续作为 spec-local 遗留定义树的唯一显式迁移入口，archive-not-delete。
- **FR-016**: 所有描述项目级概念的活面 MUST 指向 `/speckit.anchor`：团队创建、团队执行、团队改进、SDD 驱动检查点、项目 setup、house-keeping、interview pattern、命令参考与教程。
- **FR-017**: "团队绑定一个项目级 Goal"这一退役读法 MUST NOT 留在活面；团队侧 MUST 表述为绑定 Anchor。
- **FR-018**: 以旧语义引用 `/speckit.goal` 的**日期化记录** MUST 保持原字节，并按其日期解读；MUST NOT 被本特性回写。

#### C. Goal command surface

- **FR-019**: `/speckit.goal` MUST 只服务行动级 Goal，由重写后的 canonical `templates/commands/goal.md` 交付，并 MUST 恰好暴露四模式 `create` / `view` / `modify` / `status`；`view` 无 slug 时 MUST 列出 Goal 存档且 MUST 只读；`status` MUST 报告并转换生命周期状态（`active` / `achieved` / `abandoned`，终态保留，`reopen` 仅限 `owner: human` 且追加历史行）；`modify` MUST 编辑指导叙述与完成条件。
- **FR-020**: 命名 Anchor-only 模式（`targets` / `migrate` / `migrate-archive` / `coordinate`）的调用 MUST 以具名拒绝（[[STR-007]]）失败、指向 `/speckit.anchor`、非零退出且零写入；MUST NOT 静默回退到 `view`。
- **FR-021**: `/speckit.goal` MUST 只经引擎写 `.specify/goals/<goal-slug>/goal.md`（[[STR-002]]），MUST NOT 写锚点档案或任何团队定义。
- **FR-022**: `/speckit.goal` MUST 委派给四模式的 `manage-goal` 技能；该技能 MUST NOT 暴露 Targets、迁移、coordinate 或团队操作。
- **FR-023**: Goal MUST NOT 被解析为 Anchor 身份：只存在于 Goal 存档的 slug MUST 无法通过 `anchor_slug`（[[STR-003]]）解析，且任何团队 MUST NOT 绑定它。
- **FR-024**: Goal 撰写 MUST 接受行动/步骤形文本，MUST NOT 对其施加 Anchor 的 `outcome, not steps`（GD-2）形状校验；Anchor 撰写 MUST 继续拒绝任务清单形目标。
- **FR-025**: Goal 生命周期迁移 MUST 使用共享三值；终态 Goal MUST 保留在存档中，MUST NOT 被删除。
- **FR-026**: `docs/reference/commands/goal.md` MUST 被重写为新概念与四模式；其任何活段落 MUST NOT 再把 `/speckit.goal` 描述为项目级目标或锚点档案的撰写入口。
- **FR-027**: 两个命令 MUST 仍通过类别台账进入声明的命令族（不得手维护白名单）；命令族判定 MUST 按定义层（anchor / goal / team）分别作答，而不是单一布尔值。

#### D. Engine boundary

- **FR-028**: `scripts/python/goal-utils.py` MUST 继续作为锚点档案与 Goal 存档的**唯一引擎与唯一写者**；本特性 MUST NOT 新增第二套引擎、第二份 schema 或并行的迁移工具。
- **FR-029**: 引擎 MUST 按层解析定义文件名（`anchor.md` / `goal.md` / `team.md`）；引擎及其消费者 MUST NOT 假定单一全局文件名常量。
- **FR-030**: `--scope` 取值 MUST 变为封闭四成员 [[STR-004]]（`anchor` / `teams` / `goals` / `auto`）；该取值集的唯一 owner MUST 为 `anchor-definitions.md` § Archive Layers，其他面（含引擎 `--help`）MUST 只按路径引用；退役成员 `goal` MUST 以非法取值失败（exit 2），MUST NOT 被静默别名。
- **FR-031**: `--scope auto` MUST 在三个层之间解析，并在 slug 不存在于任何层、或在多于一层存在时以 exit 2 报错，MUST NOT 猜测。
- **FR-032**: 行动级 Goal 操作 MUST 是同一可执行体内一个独立、清晰命名的动作组；分类、迁移与归档清理 MUST 是同一可执行体内另一个独立命名的动作组，并 MUST 提供 `--check` 与 `--apply`；任一组动作 MUST NOT 写入另一组的存储层。
- **FR-033**: 既有动作（`list` / `validate` / `binding` / `targets` / `run-checks` / `command-family` / `handoff-decision` / `handoff-ref` / `probe-residual`）MUST 在其所服务的层上保持原语义，只按新名称、文件名与绑定字段（`anchor_slug`）适配。
- **FR-034**: 引擎 MUST 继续在不动作的情况下回答 `-h` / `--help` 与 `--version`，并拒绝未声明选项，符合 script-interface 契约。

#### E. Classification, cleanup, migration

- **FR-035**: `.specify/anchoring/` 下每个条目 MUST 得到 `anchor` / `action-goal` / `obsolete` 之一的最终分类，并记录规则 id 与所用证据。
- **FR-036**: 分类规则 MUST 为：目标绑定单一交付物、有有限完成事件且验证为有限通过/不通过集 → `action-goal`；主题被后续模型取代或记录的是已完成的一次性检查 → `obsolete`；其余 → `anchor`。判不准的条目 MUST 只有在记录理由后才可取 `anchor`。
- **FR-037**: § Assumptions 的暂定清单 MUST 作为期望基线；与之不同的最终判决 MUST 记录规则 id 与证据，MUST NOT 静默改判。
- **FR-038**: 判为 `anchor` 的条目 MUST 留在 `.specify/anchoring/<slug>/` 并持有 `anchor.md`（[[STR-001]]）；其派生 `summary/` MUST 被重生成，MUST NOT 手改。
- **FR-039**: 判为 `action-goal` 的条目 MUST 迁入 `.specify/goals/<slug>/goal.md`（[[STR-002]]），保留目标叙述、成功判据（作为完成条件）、生命周期状态、时间戳与 History；字段映射 MUST 限于：文件位置、`## Objective` → `## Guidance`、`## Success Criteria` → `## Completion Conditions`，其余 frontmatter（`status` / `created` / `updated` / `binding`）与 `## Boundaries` / `## History` 正文逐字节不变；`## Targets` 按 FR-040 处置。
- **FR-040**: Target MUST NOT 丢失：带 `## Targets` 的条目 MUST 要么保留为 Anchor，要么把每个 Target 语句原样保留在迁移后的 Goal 正文中，并在回执中记录其身份。
- **FR-041**: 判为 `obsolete` 的条目 MUST 经引擎的归档动作连同回执归档到 `.specify/archive/anchoring/<slug>/`（[[STR-006]]），MUST NOT 被删除，MUST NOT 用手工 `git mv` 替代引擎动作。
- **FR-042**: 每个被迁移或归档的条目 MUST 有一条回执，记录源路径、目标路径、概念摘要（概念载荷哈希）、时间戳、引擎标识、结果身份与 `delete_policy: archive-not-delete`（[[STR-005]]）；回执 MUST 为逐条、机器可读的 JSON，并落在动作目标内（迁移 → `.specify/goals/<slug>/migration-receipt.json`，归档 → `.specify/archive/anchoring/<slug>/migration-receipt.json`），MUST NOT 写入任何共享聚合文件。
- **FR-043**: 概念摘要 MUST 为声明映射后归一化投影的 `sha256`（投影 = FR-039 映射后的正文 + `status` / `created` / `updated` / `binding` frontmatter；`## Targets` 由 FR-040 单独记账）；回执 MUST 同时记录源摘要、目标摘要与映射版本，动作前后按同一映射计算的摘要 MUST 相等。迁移与归档 MUST 幂等：第二次运行 MUST 报 `already-migrated` / `already-archived`（判据：目标存在且回执存在），不写第二份回执，且零新增 diff。
- **FR-044**: 迁移与归档 MUST 可中断续做：中断 MUST 报告所处阶段与实际状态，重新调用 MUST 从该阶段续做；MUST NOT 存在无回执的删除。
- **FR-045**: 冲突（目标 slug 已存在且概念载荷不等价）MUST 停下、指名两个候选、MUST NOT 覆盖或择一胜出。
- **FR-046**: 被迁移或归档条目所绑定的团队 MUST 逐条处置，处置顺序 MUST 为：R1 改绑到覆盖其主题的既有 Anchor（记录证据与理由）→ R2 主题通过 FR-036 的 `anchor` 判据时经引擎 `migrate` 落成 Anchor → R3 否则连同回执归档该团队；R1–R3 均无法由团队定义与档案证据判定时 MUST 停下并具名报告。
- **FR-047**: `team.md` 的 frontmatter 绑定键 `goal_slug` MUST 经引擎改名为 `anchor_slug`（[[STR-003]]），该结构性步骤 MUST 只改这一行、其余字节逐字节保持；活团队定义正文中对绑定字段与 `.specify/goal/<slug>/summary/` 交付路径的引用 MUST 在随后的术语归一化步骤中更新（FR-058），该步骤逐行记入回执。『活团队定义』= `.specify/teams/**/team.md`（不因 `lifecycle_state: archived` 豁免）；日期化 `runs/**` 不是定义，不在此列（FR-061）。退役键 `goal_slug`（[[STR-008]]）MUST NOT 留在任何活团队定义的 frontmatter 或正文中。
- **FR-048**: 本特性完成后，任何团队的 `anchor_slug`（[[STR-003]]）MUST 能解析到既有 Anchor；现存两处悬空绑定——`viz-skill-arena` → 缺失的 `visualization-skill-selection`、`demo-seat-dispatch` → 缺失的 `demo-seat-dispatch`——MUST 按 FR-046 的 R1–R3 顺序处置（D-5：前者持续按度优化的主题按 R2 经引擎 `migrate` 落成 Anchor，后者一次性演示主题按 R3 连同回执归档团队），MUST NOT 留下无法解析的绑定。4 个无绑定字段的团队（`cws-workspace-cluster`、`draw-plantuml-optimizer`、`requirement-implement-monitor`、`summarize-project-optimizer`）MUST 保持字节不变，并在证据中登记为「无绑定」。
- **FR-049**: 被迁移/归档条目的派生 `summary/` MUST 随定义处置（目标层支持时）或连同回执归档；定义已不存在的孤立 `summary/` MUST NOT 留在锚点档案中。

#### F. Live-surface delivery

- **FR-050**: `shared/definitions/framework-map.md` MUST 分别列出锚点存档、Goal 存档、锚点归档目的地与团队存档四行，每行点名其 owner。
- **FR-051**: `.specify/glossary.md` MUST 删除把项目级档案写成 `.specify/goal/` 的过期描述，并 MUST 定义 Anchor、Anchor Archive、Anchor–Team Binding、Goal（行动级）、Goal 存档与 Re-Anchoring 消歧；任何活 glossary 行引用 `.specify/goal/` 或 `goal_slug` 的 MUST 一并更新为新路径或新字段，MUST NOT 只改被点名的词条。
- **FR-052**: `shared/definitions/sdd-routing-definitions.md` MUST 把 Anchor 放在控制层级最高层、把 Goal 移出控制层级，并把**锚点侧**共享定义的改写路由到 `/speckit.anchor`（团队侧保持 `/speckit.team`，行动级 Goal 由 `/speckit.goal` 管理且不进入该层级）。
- **FR-053**: `shared/definitions/re-anchoring-definitions.md` § Anchoring archive MUST 把实体定义引用到 Anchor owner，保留它自己拥有的三条边，MUST NOT 重新定义实体。
- **FR-054**: `shared/definitions/flow-class-definitions.md` MUST 新增 `/speckit.anchor` 行并更新 `/speckit.goal` 行；技能行 MUST 反映七模式与四模式两个技能；台账自身的计数声明与漂移守卫期望 MUST 在同一变更内重新测量。
- **FR-055**: `shared/definitions/probe-definitions.md` MUST 新增 `/speckit.anchor` 的 wrap-up 探针对象、绑定与 docs 面；`/speckit.goal` 探针 MUST 保留；编译嵌入 MUST 从登记处重生成，MUST NOT 手改。
- **FR-056**: `sdd-project-setup` 与 `sdd-house-keeping` MUST 检查锚点存档（而非历史 `.specify/goal/` 路径），并在 bootstrap / 维护指引中点名 `/speckit.anchor`。
- **FR-057**: `docs/reference/commands/anchor.md` MUST 存在，`docs/reference/commands/goal.md` MUST 被重写；教程命令表、quickstart 前置表与任何命令索引 MUST 按新语义列出两个命令。
- **FR-058**: 团队域参考（`create-team` / `improve-team` / `run-team` / `summarize-project` 及其脚本）MUST 使用 Anchor 术语、`anchor_slug` 与 `.specify/anchoring/<slug>/summary/` 作为交付目录；任何活页面 MUST NOT 继续把 `.specify/goal/<slug>/summary/` 当交付路径。
- **FR-059**: `shared/patterns/interview-pattern.md` 及其他引用旧入口的活 pattern / 定义页 MUST 把锚点撰写指向 `/speckit.anchor`，只把行动级指导指向 `/speckit.goal`。
- **FR-060**: 非一次性处置回顾面成员 MUST 被更新：`.specify/anchoring` 与 `.specify/goals` 成为成员，历史成员 `.specify/goal` 退役并在 owner 声明（`shared/declarations/facts/non-disposable-review-surface.yaml#/statement`，含镜像副本）中记录退役理由。
- **FR-061**: 日期化记录 MUST NOT 被重写：037、038、042、074、085、094、全部日期化 spec 目录、`.specify/teams/**/runs/**`、`.specify/archive/**`、`.specify/history/**`、`docs/notes/**` 与日期化 test-evidence MUST 保持逐字节不变。

#### G. Verification and guard obligations

- **FR-062**: 契约测试 MUST 在 `templates/commands/anchor.md` 缺失、未暴露恰好七模式、或复述 `--scope` 取值集而非引用 owner 时转红。
- **FR-063**: 契约测试 MUST 在 `goal` 模板把 Anchor-only 模式当作可接受模式、或 Anchor-only 调用未被具名拒绝（[[STR-007]]）时转红。
- **FR-064**: 契约测试 MUST 在任一 `.specify/anchoring/*/` 缺 `anchor.md`（[[STR-001]]）、或分类记录标为 `action-goal` 的条目仍留在那里时转红。
- **FR-065**: 契约测试 MUST 在引擎之外的任何代码路径写入锚点存档或 Goal 存档时转红；两写者模拟 MUST 证明不同 slug 落到不同路径。
- **FR-066**: 契约测试 MUST 在任一活团队定义（frontmatter 或正文，含 `lifecycle_state: archived` 的 `team.md`；`runs/**` 除外）仍含 `goal_slug`（[[STR-008]]）、或任一 `anchor_slug`（[[STR-003]]）无法解析时转红。
- **FR-067**: 契约测试 MUST 在活面仍把 Goal 定义为项目级、仍把 `/speckit.goal` 当锚点档案入口、或仍使用 `.specify/goal/<slug>/summary/` 交付路径时转红。
- **FR-068**: 迁移测试 MUST 断言幂等、中断续做、回执完整、概念摘要相等与零删除；注入重复回执或丢弃一个 Target MUST 使套件转红。
- **FR-069**: 日期化记录不可改写守卫 MUST 以特性前提交 `d7c9da7a3` 为基线比较受保护路径（FR-061 的集合），任何字节变化 MUST 转红；实现入口与收尾各采集一次，两次读数 MUST 与基线相等。
- **FR-070**: 命令面漂移守卫（flow-class 台账计数、参考页覆盖、命令族判定）MUST 在同一变更内更新，使缺失 `/speckit.anchor` 行或页面成为红色而非被容忍。
- **FR-071**: 本特性 MUST 把自身验证读数写入 `.specify/specs/101-anchor-goal-realignment/test-evidence/`；没有读数的结论 MUST 报 `not-evaluated`，MUST NOT 报通过。

### Key Entities *(include if requirement involves data)*

- **Anchor（锚点）**: 项目级远期目标定义；目录身份 `anchor-slug`，定义文件 `anchor.md`；由目标叙述、成功判据、生命周期、绑定记录与可选 Targets 构成；被团队绑定；由 `/speckit.anchor` 经引擎撰写。
- **Goal（行动级目标）**: 短期实际指导；目录身份 `goal-slug`，定义文件 `goal.md`，存于 `.specify/goals/`；由指导叙述（可为步骤形）、完成条件、生命周期与绑定记录构成；不带 Targets、不被团队绑定、不在控制层级。
- **Anchor–Team binding**: 团队 frontmatter 的 `anchor_slug` 单向引用（N 团队 : 1 Anchor）；只存身份，不复制内容。
- **Goal store**: `.specify/goals/` 本身；一文一件、每 slug 一个目录，派生索引就地重建而非共享可变文件。
- **Migration / archive receipt**: 逐条动作回执；记录源、目标、概念摘要、时间戳、引擎身份、结果身份与 `delete_policy: archive-not-delete`。
- **Classification record**: 每个条目一条的判决记录；字段至少含 slug、`classification`、规则 id、证据指针与日期。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时依赖——它消费既有的 Python 解释器、pytest 运行器、既有 goal 引擎与既有镜像/分类引擎。表中每一行可机械判；零散文声明。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库文件系统与路径解析（命令脚手架、档案扫描、迁移与回执写入） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 中既有的 `requires-python` 声明；本特性零新增第三方依赖 | `pyproject.toml` | 新增命令/迁移/守卫脚本在 `>=3.8` 解释器上通过定向测试与 `--help`/`--version` 契约；静态 import 清单为零 | FR-062, FR-071 | EP-001 |
| RS-002 | `pytest` 测试运行器（契约测试、双写者夹具、迁移夹具） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 中既有的 pytest 声明；本特性零新增依赖 | `pyproject.toml` | `bash scripts/bash/run-tests.sh` 通过；新增 `tests/contract/` 守卫在 `>=3.8` 上执行 | FR-062, FR-063, FR-064, FR-065, FR-066, FR-067, FR-068 | EP-002 |
| RS-003 | 既有 `goal-utils.py` 引擎的扩展面（anchor/goal 双档案、`anchor_slug`、迁移动作） | in-scope | 本特性自身修订的 `scripts/python/goal-utils.py` | 不适用（无外部版本面） | `scripts/python/goal-utils.py` | 引擎 `--help`/`--version` 仍满足宪法 XXI；新动作的退出码与两写者审计被契约测试钉住 | FR-047, FR-048, FR-049 | EP-003 |
| RS-004 | 既有镜像/命令副本/流程分类引擎（`sync-mirrors.py`、`regen-command-copies.py`、`flow-class-check.py`） | in-scope | 本特性自身修订的台账与模板；引擎只消费 | 不适用（无外部版本面） | `scripts/python/sync-mirrors.py` | `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 均 exit 0；`flow-class-check.py` 对新旧两命令行均可解析 | FR-054, FR-057, FR-070 | EP-004 |
| RS-005 | `git`（受保护日期化路径的 `hash-object` 基线比较与工作树状态读取） | signed-contract | git 上游（本仓只消费） | 本仓无版本声明；pin 由 `git --version` 在 test-evidence 的首次采集记录提供 | `scripts/bash/common.sh` | 受保护路径哈希集合与特性前提交 `d7c9da7a3` 相等；迁移前后 `git status --porcelain` 增量为空 | FR-061, FR-069 | EP-005 |

**Contract-cell note**: 每个 `Contract` 单元格只放一个仓内可解析路径；其余引用是证据，不是第二契约。RS-003/RS-004 的 in-scope 义务在 tasks 阶段由任务行引用其 FR，在 closure 阶段由 `verification.md` 的点名联合验收行闭合。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 语义一致性可判定——对声明的活根执行残留扫描，"Goal = 项目级"与"Anchor 从属于 Goal"两类表述计数为 0；向任一活面注入一句旧语义后扫描转红；日期化根不计入且保持原字节。 **Path**: final
- **SC-002**: 命令面分割完整——`/speckit.anchor` 恰好暴露七模式、`/speckit.goal` 恰好暴露四模式，四个 Anchor-only 模式（`targets` / `migrate` / `migrate-archive` / `coordinate`）经 `/speckit.goal` 调用时全部具名拒绝并指向 `/speckit.anchor`；删除任一 canonical 模板或模式行时契约测试转红。 **Path**: final
- **SC-003**: 档案纯度可测量——14 个条目逐条有分类记录；`.specify/anchoring/` 中 `action-goal` 条目数为 0；每个被判 `action-goal` 的条目在 `.specify/goals/` 中恰有一份定义；过期条目全部位于 `.specify/archive/anchoring/`；读数写入 test-evidence，不以暂定数字充当实测。 **Path**: final
- **SC-004**: 零丢失可复核——每条被迁移/归档条目有回执；概念摘要在动作前后相等；删除数为 0；受保护日期化路径的逐文件哈希与特性前提交一致。 **Path**: final
- **SC-005**: 绑定完整性——活团队定义中 `goal_slug` 计数为 0；每个 `anchor_slug` 可解析；每个受影响团队有一条处置记录；`viz-skill-arena` 与 `demo-seat-dispatch` 的五查通过。 **Path**: final
- **SC-006**: 单写者成立——静态审计显示锚点档案与 Goal 存档各只有引擎一个写者；两写者模拟在同一层写不同 slug 时落到不同路径；在引擎外注入一次写入后审计转红。 **Path**: final
- **SC-007**: 幂等与可续做——迁移成功后重跑零新增 diff、零重复回执；在"源已归档、目标未写"处中断后重入，从报告阶段续做且完成状态可判定。 **Path**: supporting
- **SC-008**: 交付面齐备——`anchor.md` 参考页存在、`goal.md` 参考页已重写、flow-class 台账含两命令行、探针编译含 `/speckit.anchor` 面、文档站构建通过；任一缺失使守卫转红。 **Path**: supporting
- **SC-009**: 历史不可改写——037 / 038 / 042 / 074 / 085 / 094、全部日期化 spec 目录、`.specify/teams/**/runs/**`、`.specify/archive/**`、`.specify/history/**`、`docs/notes/**` 的哈希集合与基线 `d7c9da7a3` 相等。 **Path**: supporting
- **SC-010**: 读者可分辨——按 glossary 与两份 owner，未参与本轮的读者能正确复述 Anchor、anchoring archive、Re-Anchoring 与行动级 Goal 的对象与所在目录；复述失败即判定不通过。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 残留扫描脚本对本规格 § Live-surface roots 声明的活根做正则计数，输出每类命中路径；注入用例在测试夹具中执行。活根集合在 plan 的 `research.md` 中声明，测试读取该声明而非各自硬编码。
- **SC-002 Source**: 契约测试解析 canonical 模板的 `argument-hint` 与模式表，并对 `/speckit.goal <anchor-only-mode>` 做子进程调用，采集退出码、stderr 与零写入断言。
- **SC-003 Source**: 分类记录（逐条 markdown/JSON）与两次目录枚举读数（清理前、清理后）；`find`/`glob` 计数与 `goal-utils.py list --scope anchor|goals` 输出交叉核对。
- **SC-004 Source**: 回执文件逐条读取；概念摘要由引擎在动作前后各计算一次并写入回执；受保护路径哈希由 `git hash-object` 或 `sha256sum` 在特性前提交与实现后各采集一次。
- **SC-005 Source**: 对 `.specify/teams/*/team.md` 的 frontmatter 扫描；`goal-utils.py run-checks <team>` 逐团队退出码；处置记录清单。
- **SC-006 Source**: 静态审计（对仓储代码路径的写入面扫描，含镜像树）加两分支夹具模拟；审计在 `tests/contract/` 中执行。
- **SC-007 Source**: 迁移夹具上的两次 apply 与一次中断注入；diff 与回执计数。
- **SC-008 Source**: 文件存在性 + `flow-class-check.py --action check` 退出码 + 探针编译命令 + docs 构建命令的退出码。
- **SC-009 Source**: 受保护路径的 `git hash-object` 集合对比（基线 = 特性前提交 `d7c9da7a3`）。
- **SC-010 Source**: 一次基准读者复述记录，落在 `test-evidence/`；复述文本与三词条的对照由评审者判定。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `".specify/anchoring/<anchor-slug>/anchor.md"` | FR-002, FR-007, FR-038, FR-064 |
| `STR-002` | `".specify/goals/<goal-slug>/goal.md"` | FR-004, FR-007, FR-021, FR-039 |
| `STR-003` | `"anchor_slug"` | FR-023, FR-047, FR-048, FR-066 |
| `STR-004` | `anchor` / `teams` / `goals` / `auto` | FR-030 |
| `STR-005` | `"delete_policy: archive-not-delete"` | FR-042 |
| `STR-006` | `".specify/archive/anchoring/<slug>/"` | FR-041 |
| `STR-007` | `"anchor-only-mode"` | FR-020, FR-063 |
| `STR-008` | `"goal_slug"` | FR-047, FR-066 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

<!-- Populated by /speckit.clarify. Initial draft carries none. -->

### Session 2026-11-12

- Q: Which Feature owns this specification — a new Feature or an extension of 041 Goal Registry? → A: 新 Feature **101 "Anchor / Goal Realignment"**；041 保持 `Implemented` 与其日期化记录，只增加一条反向交叉引用。D-1
- Q: `goal_slug` 退役与"其余字节逐字节相同"如何同时成立？ → A: 分两步——结构性迁移只改 frontmatter 绑定键一行，逐字节断言只作用于该步；正文中的 `goal_slug` 与 `.specify/goal/<slug>/summary/` 引用由随后的术语归一化步骤逐行改写并记入回执；日期化 `runs/**` 不属于活团队定义，保持原字节。D-2
- Q: 新 `/speckit.goal` 的 `status` 模式做什么？ → A: 报告并转换生命周期状态（`active` / `achieved` / `abandoned`，终态保留，`reopen` 仅限 `owner: human` 且追加历史行），复用既有生命周期 owner 与引擎 `status` 动作；`view` 只读，`modify` 编辑指导与完成条件。D-3
- Q: 清理/迁移以什么形态执行，回执与概念摘要如何判定？ → A: 作为 `goal-utils.py` 内独立命名的清理动作组（`--check` / `--apply`），不新增 `/speckit.anchor` 模式（七模式上限不变）；回执为逐条 JSON 落在动作目标内（`migration-receipt.json`），不写共享聚合；概念摘要为声明映射后归一化投影的 `sha256`，回执记录源/目标摘要与映射版本；幂等判据为"目标存在且回执存在"。D-4
- Q: 两个悬空团队绑定如何处置，哪些日期化路径需要保护？ → A: 处置顺序 R1 改绑到覆盖其主题的既有 Anchor（记录证据）→ R2 主题通过 `anchor` 判据则经引擎 `migrate` 落成 Anchor → R3 否则连同回执归档团队；无法判定即停并具名报告。`viz-skill-arena` 的持续按度优化主题按 R2 落成 `visualization-skill-selection`；`demo-seat-dispatch` 的一次性演示主题按 R3 归档。受保护日期化路径增加 `.specify/teams/**/runs/**` 与全部日期化 spec 目录，基线为 `d7c9da7a3`。D-5

**In-pass corrections（本轮就地纠正，均与已记录意图一致）**：

- `SC-002` 原写"三个 Anchor-only 模式"，与 `FR-020` 列出的四个（`targets` / `migrate` / `migrate-archive` / `coordinate`）矛盾 → 改为"四个"。
- `FR-052` 原写"把**一切**共享定义的改写路由到 `/speckit.anchor`"，与团队侧既有边界（`/speckit.team`）冲突 → 收敛为锚点侧改路由到 `/speckit.anchor`、团队侧保持 `/speckit.team`。
- `FR-002` / `FR-004` 原各自"定义绑定记录与生命周期"会形成第二份 schema → 唯一 owner 归 `anchor-definitions.md`，Goal owner 只按路径引用。
- `FR-033` 的既有动作清单遗漏了同样读取绑定字段的写动作 `handoff-ref` → 补入并按 `anchor_slug` 适配。
- `A-5` 原写"plan / implement 裁定"两个决策者 → 收敛为 plan 落分类表、implement 只执行；`A-9` / `A-11` 由 D-4 / D-1 一并定案。

## Non-Goals & Boundaries *(informative)*

- **不新增命令**：`/speckit.anchor` 是既有 `/speckit.goal` 命令面的**改名与接管**，不是第 32 个新能力面；净增命令数为 1（`anchor`）且旧面同时收缩，命令总数由台账 owner 重测。
- **不改宪法**：Re-Anchoring 原则（XXII）与其 owner 的运行内纪律保持不变；本特性只消歧术语。
- **不做 Goal 的团队绑定或 Targets**：行动级 Goal 是指导，不是施工对象；需要切片与协调的工作继续由 Anchor + Team 承载。
- **不重写日期化记录**，也不把 git 历史纳入改写范围。
- **不推送远端**：本线无人值守，推送需显式授权。
