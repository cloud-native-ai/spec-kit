# Agent 框架设计（概念模型）

> 本文档是 Spec Kit **Agent 框架的权威概念模型与设计说明**，描述的是当前**已实现**的机制
> （spec `023-agent-framework-redesign`，Feature 019 *Agents Command*）。
> 它由早期的《Agent 改造方案》重写而来：早期文档以「问题 → 预期结果 → 实现细节」的提案形式
> 组织，本文档则以实现结果为准，保留必要的迁移背景以供追溯。阅读顺序建议：先读本文档，再看
> [command-and-skills.md](./command-and-skills.md) 与 [templates-and-agents.md](./templates-and-agents.md)。

## 一、设计动机

早期 Agent 实现的核心问题是 **Agent 的定义混乱**——若干概念相互交织、边界不清：

1. **角色（Role）未抽象**：Agent 承担的职责与看待问题的视角没有被清晰地独立出来。
2. **阶段（Stage）与角色混淆**：同一角色在执行中存在执行者、评估者、优化者三种阶段，但 Stage 与 Role 的关系没有理顺。
3. **团队（Team）静态结构缺失**：多个 Agent 在静态结构上组成团队（含一个负责整体评估的 Supervisor），这一组织结构未被表达。
4. **循环（Loop）动态结构缺失**：多 Agent 在运行时形成迭代循环，每个循环含多个阶段，缺乏统一定义。
5. **模板分散**：`templates/agent-*` 模板散落在顶层模板目录，未与 create-agent 技能形成整体。

当前实现针对以上问题给出了统一的概念模型与落地结构，下面各节即为**最终结果**。

## 二、概念模型：三维属性 + 两种结构

一个 **Agent** 由三个正交的属性维度完整描述，再叠加两种组织结构：

### 2.1 三个属性维度

1. **Role（角色）**：定义 Agent 承担的职责以及看问题的视角。共有 **7 个 Worker 角色 + 1 个 Meta 角色**（见下表）。
2. **Stage（阶段）**：同一角色在执行过程中的三种阶段——**执行者（executor）**、**评估者（evaluator）**、**优化者（optimizer）**。
3. **Type（类型）**：区分 **Worker Agent（工作 Agent）** 与 **Meta Agent（元 Agent）**：
   - **Worker Agent**：处理项目中的实际任务；
   - **Meta Agent**：优化和处理其他 Agent（Team Supervisor 就是一种 Meta Agent，负责监控整个团队与其他 Agent 的表现）。

**Type-follows-Stage（类型由阶段决定）**：Type 不是独立选择的，而是由 Stage 推导——
Worker 角色处于 **执行者** 阶段时为 Worker，处于 **评估者 / 优化者** 阶段时切换为 Meta；
Meta 角色（Team Supervisor）不承担实际任务，各阶段恒为 Meta。

### 2.2 两种组织结构

- **Team（团队，静态结构）**：多个 Agent 在静态结构上组成的团队，可用一张 Role×Stage 二维矩阵表达（见 §三），含一个负责整体评估与协调的 Team Supervisor。
- **Loop（循环，动态结构）**：多 Agent 在运行时形成的迭代循环，每个循环跨越多个 Stage；同一角色在不同阶段扮演不同 Type，或由多个 Agent 分别承担不同 Stage。Loop 的运行机制见 [eei-triad-pattern.md](./eei-triad-pattern.md)。

## 三、Team 的二维矩阵表达

一个 Team 可用一张二维表格描述：**每一行代表一个 Agent（按 Role 划分）**，
**每一列代表工作过程中的一个 Stage**，**整张表格整体代表一个团队**。
行列交叉的单元格用 **Worker** / **Meta** 表示该 Agent 在对应阶段的 Type 属性。

下表的角色与阶段均来自 `skills/create-agent/templates/` 中的角色模板（`agent-role-*`）
与阶段模板（`agent-stage-*`）：

| Agent 角色（Role） \ Stage | 执行者（Executor） | 评估者（Evaluator） | 优化者（Optimizer） |
| --- | --- | --- | --- |
| 需求分析师（Requirements Analyst） | Worker | Meta | Meta |
| 用户体验分析师（UX Analyst） | Worker | Meta | Meta |
| 系统架构师（System Designer） | Worker | Meta | Meta |
| 模块设计师（Module Designer） | Worker | Meta | Meta |
| 测试工程师（Test Engineer） | Worker | Meta | Meta |
| 质量保证工程师（QA Engineer） | Worker | Meta | Meta |
| 知识管理员（Knowledge Manager） | Worker | Meta | Meta |
| 团队监督者（Team Supervisor） | Meta | Meta | Meta |

说明：

- **行 = Role**：每个 Agent 占一行。前 7 行为 **Worker 角色**，最后一行 **团队监督者（Team Supervisor）** 为**唯一的 Meta 角色**——它由原「元协调器（Meta-Coordinator）」与「团队监督者（Team Supervisor）」**合并**而来，统一承担任务协调与团队监督职责；框架中不再存在独立的 Meta-Coordinator。
- **列 = Stage**：对应三个阶段——执行者（executor）、评估者（evaluator）、优化者（optimizer）。
- **单元格 = Type**：遵循 Type-follows-Stage——Worker 角色在执行者阶段为 **Worker**，在评估者/优化者阶段为 **Meta**；Team Supervisor 各阶段均为 **Meta**。

> **关于 UX Analyst**：用户体验分析师（UX Analyst）是内置的第 7 个 Worker 角色，负责分析与优化
> **所有用户接口**——不仅是前端 / GUI 页面，也包括命令行（CLI）设计，以及 `/command` 与 skill 等
> 与用户交互的部分。它以需求为输入、并评审既有接口，向 System Designer 与 Module Designer 输出
> 跨全部用户界面（前端、CLI、命令、技能）的 UX 规范与交互契约。
>
> 早期重设计 spec（023）曾依据决策 **D1** 将其暂缓（deferred）；该决策现已被本次实现取代——
> UX Analyst 已作为内置角色落地：模板 `agent-role-ux-analyst-template.md` 与持久化 Agent
> `.specify/agents/ux-analyst.agent.md` 均已提供。

## 四、Agent 的两种生命周期

1. **临时 Agent（temporary）**：仅在当前上下文中记录，随会话结束而消失。
2. **持久化 Agent（persistent）**：保存到项目的 Agent 目录 `.specify/agents/`，可跨会话复用。

持久化 Agent 以 `.specify/agents/` 为**唯一真源**，并通过 `specify init`（或安装流程）为各工具建立**逐文件软链接**。
以 qoder 工具为例，`.qoder/agents/` 是一个**真实目录**，其中每个 `.specify/agents/<slug>.agent.md`
都对应一条软链接 `.qoder/agents/<slug>.agent.md -> ../../.specify/agents/<slug>.agent.md`；
`.github/agents`、`.qwen/agents`、`.opencode/agents`、`.hermes/agents`、`.iflow/agents` 同理。
逐文件（而非整目录）软链接的好处是：工具目录中可以让框架 Agent 与该工具自建的 Agent（例如
qoder 覆盖内置专家用的同名 `.md`）**并存**。目录与发现细节见 [templates-and-agents.md](./templates-and-agents.md)。

## 五、多 Agent 使用场景（编排与组合）

多个 Agent 的**编排与组合**由**团队域**承载：全部经由 `create-team` 技能（`/speckit.team` 命令）落地，
共有**四种**协作模式，每种编码一种优先取向——

- **parallel（效率优先）**：相互独立、无共享状态的任务，按不相交领域并发拆分；
- **serial（质量优先）**：有严格前序依赖的阶段流水线，每步与前序间做简单验证后才推进；
- **iteration（目标收敛）**：多个 Agent 组成含**唯一 Team Supervisor** 的两层闭环，反复打磨到质量阈值即交付；
- **continuous（长期运营）**：按 cadence 长期运行，每个 cycle 在预算/约束/独立验证/状态脊柱下处理源源不断的工作。

> 概念、四模式语义、目录布局与操作细节均在**团队文档集**：
> [`docs/teams/overview.md`](../teams/overview.md)、[`docs/teams/orchestration.md`](../teams/orchestration.md)、[`docs/teams/continuous-operations.md`](../teams/continuous-operations.md)；
> 单一真相源为 [`skills/create-team/references/conceptual-model.md`](../../skills/create-team/references/conceptual-model.md) 与 [`operating-loops.md`](../../skills/create-team/references/operating-loops.md)。
> 本框架文档只保留「团队 = 静态 Team 矩阵 + 动态 Loop」这一**概念**（见 §二、§三），不再复述编排操作。

## 六、实现结构

### 6.1 命令入口（单 Agent 与团队分离）

单 Agent 与团队操作有各自的命令入口（Feature 027 团队管理引入的分离）：

- `/speckit.agents` 是**单 Agent** 操作的唯一入口——创作或优化**一个** Agent；不新增其他单 Agent 命令，本身不内联渲染模板。
- `/speckit.team` 是**团队**操作的唯一入口——组织或运行多个 Agent（parallel / serial / iteration / continuous）。

单 Agent 命令工作流程：

1. **识别用户意图**：分析用户输入，判断是创作还是优化单个 Agent。
2. **调用 `create-agent` 技能**：按模板创建对应工具的 Agent 配置。
3. **调用 `improve-agent` 技能**：基于反馈优化已有 Agent。
4. **团队意图重定向**：若用户请求组织/运行多个 Agent，重定向至 `/speckit.team`，不在此处理。

命令与路由细节见 [command-and-skills.md](./command-and-skills.md)。

### 6.2 技能

单 Agent 域（`/speckit.agents`）：

- **`create-agent`**：创作引擎——按 `Role × Stage × Type` 从模板生成 role / supervisor / custom / project-custom 等**单个** Agent。
- **`improve-agent`**：优化引擎——基于真实使用反馈精炼**单个** Agent 制品（角色模板 / 监督片段 / 自定义 Agent）。

团队域（`/speckit.team`）：

- **`create-team`**：团队引擎——定义并运行团队，实现并行、串行、迭代收敛、长期运营四种协作模式。
- **`improve-team`**：团队优化引擎——基于运行反馈精炼团队结构（阶段 / 编排 / 阈值）。

### 6.3 模板归位

所有 `agent-*` 模板已从顶层模板目录迁移至 **`skills/create-agent/templates/`**，作为 create-agent 技能的一部分；
安装时镜像到 `.specify/skills/create-agent/templates/`。完整模板目录见 [templates-and-agents.md](./templates-and-agents.md)。

### 6.4 技能赋能（Skill Enablement）

技能与 Agent 定义同步安装，因此每个内置 Agent 都可调用任意已安装技能。七个内置角色 Agent 将这一能力**显式化、一致化**：优先使用与角色相关的框架技能，而非手工重复同类操作。每个角色 Agent 及其 `agent-role-*` 模板都声明两部分：

- **`skills:` 前置字段**：该角色相关的已安装技能规范 slug 列表（如需求分析师 → `draw-plantuml`；模块设计师 → `analysis-project`）。元/框架创作类技能（`create-agent`、`improve-agent`、`create-skills`、`improve-skills`、`create-team`、`improve-team`）为**不可声明**，不出现在任何角色列表中。
- **`## Skill Enablement` 正文小节**：共享的偏好协议（单一事实来源 `skills/create-agent/templates/agent-skill-enablement.md`，各 Agent 组合复用而非各自改写）+ 与 `skills:` 一致的 `| Skill | When to use |` 表格。协议要求：优先选用适用技能；多个适用时选最贴合角色者；无适用技能或技能不可用/失败时，直接完成操作并暴露失败。

契约测试 `tests/contract/test_agent_skill_enablement.py` 校验该约定（每个 Agent ≥1 技能、引用均已安装、无不可声明 slug、小节存在、模板与 Agent 保持一致）。约定细节见 [command-and-skills.md](./command-and-skills.md)。

## 七、术语统一（规范化）

术语统一是本框架消除概念混乱的关键步骤。**当前唯一被接受的术语**如下（旧术语仅在迁移说明中作为历史上下文出现）：

1. **废弃 SubRole，统一使用 Stage**：同一角色在执行中的阶段统一称为 **Stage**，不再使用 SubRole / Subrole。
2. **improver 统一为 optimizer**：优化者阶段的英文名统一为 **optimizer**（执行者 executor、评估者 evaluator 不变）。
3. **Meta-Coordinator 合并入 Team Supervisor**：不再存在独立的 Meta-Coordinator，其协调职责并入唯一的 Meta 角色 Team Supervisor。

历史迁移落地记录（供追溯）：

- `agent-subrole-*.md` 已重命名为 `agent-stage-*.md`；
- `agent-subrole-improver-template.md` 已重命名为 `agent-stage-optimizer-template.md`，内部 `name`/`description` 中的 improver 同步改为 optimizer；
- `skills/create-agent/SKILL.md`、各编排模板及 `tests/` 中的旧术语（subrole / improver）引用均已迁移。

> 守卫测试 `tests/unit/test_agent_deprecated_terms.py` 会持续扫描废弃术语，确保上述规范在所有 live 制品中长期成立。

## 八、可追溯性

本文档的规范来源为重设计 spec：`.specify/specs/023-agent-framework-redesign/`——
参见 `requirements.md`、`data-model.md` 及
`contracts/{conceptual-model,agents-command,template-migration}-contract.md`。
决策记录见该 spec 的相关文档；其中 UX Analyst 暂缓的决策 **D1** 已被本次实现取代（UX Analyst 现为内置 Worker 角色）。
