# Agents — 单 Agent 框架（文档中心）

本目录记录 Spec Kit 的**单 Agent 框架**。所有陈述均以仓库中实际的代码、技能、模板与持久化
Agent 为准——这里描述的是当前**已实现**的机制，而非提案。

> `/speckit.agents` 负责**单 Agent**（创作 / 优化一个 Agent）；组织或运行多个 Agent
> （编排、组合）一律归 `/speckit.team` 与团队技能，见 [`docs/teams/`](../teams/overview.md)。

## 框架是什么

一个 **Agent** 由三个正交属性维度完整描述，由两种结构组织，由一个命令驱动，由两个技能产出：

- **模型（Model）**：每个 Agent 都是 `Role × Stage × Type`；静态排布为 **Team**（Role×Stage
  矩阵），动态展开为 **Loop**（跨阶段迭代）。
- **命令（Command）**：`/speckit.agents` 是单 Agent 工作的**唯一**入口——它识别意图并委派，
  从不内联渲染模板；多 Agent 团队（组织 / 运行多个 Agent）归 `/speckit.team`。
- **技能（Skills）**：`create-agent`（创作单个 Agent）、`improve-agent`（优化单个 Agent）；
  团队编排（parallel / serial / iteration / continuous）由团队域的 `create-team` /
  `improve-team` 承载。
- **制品（Artifacts）**：可复用模板位于 `skills/create-agent/templates/`，持久化 Agent 位于
  `.specify/agents/`，经逐文件软链接暴露给每个受支持工具。

```
         /speckit.agents  (single-agent entry)        /speckit.team  (team entry)
                 │                                            │
        ┌────────┴────────┐                          ┌────────┴────────┐
        ▼                 ▼                          ▼                 ▼
   create-agent      improve-agent               create-team      improve-team
   (author)          (refine)                    (define|run:              (refine team: stages/
        │                 │                        parallel|serial|          thresholds/maturity)
        ▼                 ▼                        iteration|continuous)
   skills/create-agent/templates/*        .specify/agents/*.agent.md  ──(per-file symlink)──▶ .qoder/agents/, .github/agents/, …
   (Role × Stage × Type source)           (persisted Team members)
```

## 文档导航

| 文档 | 覆盖内容 |
|------|----------|
| [design.md](./design.md) | **权威概念模型与设计**——Role / Stage / Type、Type 由 Stage 决定、Team 矩阵、Loop，以及唯一的 Team Supervisor。**从这里开始。** |
| [command-and-skills.md](./command-and-skills.md) | `/speckit.agents` 单一入口、意图→能力路由、两个单 Agent 技能、临时 / 持久生命周期与工具集成。 |
| [templates-and-agents.md](./templates-and-agents.md) | 规范模板目录与命名、七个预置角色 Agent + Team Supervisor、`.specify/agents/` 布局与发现机制。 |
| [quality-loop.md](./quality-loop.md) | Executor-Evaluator-Optimizer（EEI）质量闭环与角色域监督者（单 Agent）。 |

> **多 Agent 编排在别处**：组织 / 运行多个 Agent（parallel · serial · iteration · continuous）
> 归团队域，见 [`docs/teams/`](../teams/overview.md)——[orchestration.md](../teams/orchestration.md)
> （四模式操作指南）与 [continuous-operations.md](../teams/continuous-operations.md)（长期运营纪律）。

## 核心术语（速查）

| 术语 | 含义 | 规范取值 |
|------|------|----------|
| **Role（角色）** | 职责 + 看待问题的视角 | 7 个 Worker 角色 + 1 个 Meta 角色（Team Supervisor） |
| **Stage（阶段）** | 角色的执行阶段 | `executor`、`evaluator`、`optimizer` |
| **Type（类型）** | 由 Stage 推导的分类 | `Worker`（实际任务）· `Meta`（管理 / 优化 Agent） |
| **Team（团队）** | 静态结构 | Role×Stage 矩阵，单元格存 Type |
| **Loop（循环）** | 动态结构 | 运行时跨阶段迭代 |
| **Lifecycle（生命周期）** | Agent 存放位置 | `temporary`（仅上下文）· `persistent`（`.specify/agents/`） |

## 规范来源

本文档以仓库中的活制品为准：模板 `skills/create-agent/templates/`、持久化 Agent
`.specify/agents/`，以及守卫测试 `tests/contract/test_agent_skill_enablement.py` 与
`tests/unit/test_agent_deprecated_terms.py`。概念细节见 [design.md](./design.md)。
