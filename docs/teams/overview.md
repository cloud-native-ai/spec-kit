# Teams — 多 Agent 团队（文档中心）

一个 **team** 是有名字、可复用的多 Agent 结构，由 `/speckit.team` 创建 / 修改 / 运行。它由三部分组成：

- **goal** — 团队的**唯一总体最终目标**（北极星）。静态与动态结构**仅为达成 goal 而存在**，都围绕它组织与运行。
- **static structure（静态结构）** — Role × Stage × Type 花名册（*谁*参与）。
- **dynamic structure（动态结构）** — 协作模式 parallel / serial / iteration / continuous（*怎么*协作）。

> `/speckit.agents` 负责**单 Agent**（创作 / 优化一个 Agent）；组织或运行多个 Agent（编排、组合）一律归 `/speckit.team` 与团队技能。单 Agent 框架概念见 [`docs/agents/`](../agents/overview.md)。

## 四种协作模式（动态结构）

每种模式编码一种**优先取向**，由 goal 决定选哪一种。前三种是**有界**（跑一次即止）；`continuous` 是**无界**（按节奏长期运行）。

| 模式 | 优先取向 | 适用 | 生命周期 |
|------|----------|------|----------|
| **parallel** | 效率优先 (throughput) | 相互独立、无共享状态的任务，按不相交领域并发拆分 | 有界 |
| **serial** | 质量优先 (quality) | 有严格前序依赖的阶段流水线，**每步与前序间做简单验证**后才推进 | 有界 |
| **iteration** | 目标收敛 (converge) | 需反复打磨到阈值的单一质量关键交付物 | 有界 |
| **continuous** | 长期运营 (operate) | 源源不断到达的工作（CI/PR/issue）或需长期维持的质量 | 无界 |

- **iteration** 收敛即止；**continuous** 是长期运营形态，其运营纪律见 [continuous-operations.md](./continuous-operations.md)。
- `iteration` 对应**一次性**优化目标；`continuous` 对应**持续型**优化目标。
- **Team Supervisor 约束**：`iteration` / `continuous` 团队**必须且仅含一个** Team Supervisor（Meta 角色）；`parallel` / `serial` 团队**可选**用其作为 Lead / 质量门。

选择哪种模式请用 [orchestration.md](./orchestration.md) 里的**决策树**。

## 团队目录布局

持久化团队各自拥有目录 `.specify/teams/<slug>/`：

```
# parallel / serial / iteration（有界）
.specify/teams/<slug>/
├── team.md            # 定义（Markdown + YAML frontmatter，无逐工具 symlink）
└── runs/              # 每次运行一份报告 runs/<UTC-timestamp>-report.md

# continuous（无界，额外持有运营脊柱文件）
.specify/teams/<slug>/
├── team.md            # 定义（含 continuous config）
├── constraints.md     # 绑定约束（每 cycle 读取）
├── STATE.md           # 跨运行状态脊柱
├── run-log.jsonl      # 结构化运行日志（append-only）
└── runs/              # 每 cycle 一份完整报告
```

运行中间产物一律进 git-ignored 的 `.specify/teams/.work/<slug>/`；交付物只落到其声明的目标路径。

## 本目录文档地图

| 文档 | 内容 |
|------|------|
| [overview.md](./overview.md)（本文） | 团队概念、四模式语义、目录布局、权威来源索引、案例 |
| [orchestration.md](./orchestration.md) | **四模式编排操作指南** — 决策树、parallel/serial/iteration 详解、领域划分、DAG/handshake、模型选择、成本控制、排障 |
| [continuous-operations.md](./continuous-operations.md) | **长期运营纪律** — iteration vs continuous、成熟度 L1→L2→L3+门控、约束文件、预算/断路器/kill-switch、状态脊柱、独立验证者、Post-Run Critique、每 cycle 流程、失败模式 |

## 权威来源索引（单一真相源）

> 本目录做**导航与操作指南**；规范细节以技能 `references/` 为单一真相源，冲突以其为准。

| 主题 | 权威文件 |
|------|----------|
| 概念模型（Role × Stage × Type、Team Supervisor、静/动结构、四模式表） | [`skills/create-team/references/conceptual-model.md`](../../skills/create-team/references/conceptual-model.md) |
| **continuous 运营循环**（成熟度、约束、预算、验证者、状态脊柱、每 cycle 流程） | [`skills/create-team/references/operating-loops.md`](../../skills/create-team/references/operating-loops.md) |
| **Goal 概念**（定义、四条性质、goal-first、持久化 `## Goal`/`goal` 字段） | [`skills/create-team/references/goal.md`](../../skills/create-team/references/goal.md) |
| **「优化」类目标**（一次性→iteration vs 持续→continuous；淘汰 vs 渐进策略） | [`skills/create-team/references/optimization-goals.md`](../../skills/create-team/references/optimization-goals.md) |
| **修改 goal**（modify 一等编辑 + 结构级联重对齐 + 成熟度晋级/降级） | [`skills/improve-team/references/goal-editing.md`](../../skills/improve-team/references/goal-editing.md) |
| 命令入口（create / modify / run 三模式、run 门、continuous 单 cycle 门控） | [`templates/commands/team.md`](../../templates/commands/team.md) |
| 创建 / 运行技能（模式选择、四种模式引擎、持久化 schema） | [`skills/create-team/SKILL.md`](../../skills/create-team/SKILL.md) |
| 修改技能（Refinement Map，含 continuous 项） | [`skills/improve-team/SKILL.md`](../../skills/improve-team/SKILL.md) |
| 数据模型与 `.team.md` schema | [`.specify/specs/.archive/026-agent-team-management/data-model.md`](../../.specify/specs/.archive/026-agent-team-management/data-model.md) |

## 案例

- **淘汰策略范例**（复杂图表下持续优化 draw-plantuml 技能，定义了加权评分规则与淘汰/精英保留策略）：[`.specify/teams/draw-plantuml-optimizer/team.md`](../../.specify/teams/draw-plantuml-optimizer/team.md)。该团队已定义、可直接 re-run；逐轮评分结果需实际执行后累积，届时每轮报告落在同目录 `runs/` 下（运行中间态则落在被忽略的 `.specify/teams/.work/`）。

## 待完善

- `goal` 已作为一等概念落在命令与技能 `references/` 中；数据模型 [`data-model.md`](../../.specify/specs/.archive/026-agent-team-management/data-model.md) 仍把 goal 混入 `description`，需要把 `goal` 分离为独立字段以与技能 schema 一致（建议走 `/speckit.feature`）。
- 数据模型仍以三模式描述动态结构；需补齐 `iteration` 与 `continuous`（含 `config` 运营字段），与本目录及技能 `references/` 对齐（建议走 `/speckit.feature`）。
