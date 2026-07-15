# Team — 多 Agent 团队（导航）

一个 **team** 是有名字、可复用的多 Agent 结构，由 `/speckit.team` 创建 / 修改 / 运行。它由三部分组成：

- **goal** — 团队的**唯一总体最终目标**（北极星）。静态与动态结构**仅为达成 goal 而存在**，都围绕它组织与运行。
- **static structure（静态结构）** — Role × Stage × Type 花名册（*谁*参与）。
- **dynamic structure（动态结构）** — 协作模式 parallel / serial / team-loop（*怎么*协作）。

> 本目录只做**概览与导航**。详细定义以下列**权威来源**为准（技能 `references/` 是单一真相源；本文不再复述细节）。

## 权威来源索引

| 主题 | 权威文件 |
|------|----------|
| 概念模型（Role × Stage × Type、Team Supervisor、静/动结构） | [`skills/create-team/references/conceptual-model.md`](../../skills/create-team/references/conceptual-model.md) |
| **Goal 概念**（定义、四条性质、goal-first、持久化 `## Goal`/`goal` 字段） | [`skills/create-team/references/goal.md`](../../skills/create-team/references/goal.md) |
| **「优化」类目标**（一次性 vs 持续；淘汰 vs 渐进策略及配置） | [`skills/create-team/references/optimization-goals.md`](../../skills/create-team/references/optimization-goals.md) |
| **修改 goal**（modify 一等编辑 + 结构级联重对齐） | [`skills/improve-team/references/goal-editing.md`](../../skills/improve-team/references/goal-editing.md) |
| 命令入口（create / modify / run 三模式、run 门） | [`templates/commands/team.md`](../../templates/commands/team.md) |
| 创建 / 运行技能（模式选择、三种模式引擎、持久化 schema） | [`skills/create-team/SKILL.md`](../../skills/create-team/SKILL.md) |
| 修改技能 | [`skills/improve-team/SKILL.md`](../../skills/improve-team/SKILL.md) |
| 数据模型与 `.team.md` schema | [`.specify/specs/026-agent-team-management/data-model.md`](../../.specify/specs/026-agent-team-management/data-model.md) |

## 案例

- **淘汰策略范例**（复杂图表下持续优化 draw-plantuml 技能，定义了加权评分规则与淘汰/精英保留策略）：[`.specify/teams/draw-plantuml-optimizer/team.md`](../../.specify/teams/draw-plantuml-optimizer/team.md)。该团队已定义、可直接 re-run；逐轮评分结果需实际执行后累积，届时每轮报告落在同目录 `runs/` 下（运行中间态则落在被忽略的 `.specify/teams/.work/`）。

## 待完善

`goal` 已作为一等概念落在命令与技能 `references/` 中；数据模型 [`data-model.md`](../../.specify/specs/026-agent-team-management/data-model.md) 仍把 goal 混入 `description`，需要把 `goal` 分离为独立字段以与技能 schema 一致（建议走 `/speckit.feature`）。
