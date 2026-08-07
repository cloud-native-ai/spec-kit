# Agent 框架设计（概念模型）

> 本文档是 Spec Kit **Agent 框架的权威概念模型与设计说明**，描述当前**已实现**的机制。
> 阅读顺序建议：先读本文档，再看 [command-and-skills.md](./command-and-skills.md)
> 与 [templates-and-agents.md](./templates-and-agents.md)。

## 一、设计要点

Agent 框架用**一个统一的概念模型**消除 Agent 定义上的几类混乱，让每个 Agent 的属性、
组织方式与生命周期都可被清晰表达：

1. **角色（Role）独立抽象**：Agent 承担的职责与看待问题的视角，被清晰地独立为一个维度。
2. **阶段（Stage）与角色解耦**：同一角色在执行中有执行者、评估者、优化者三种阶段，Stage
   与 Role 是正交维度，各自取值互不牵制。
3. **团队（Team）静态结构显式化**：多个 Agent 组成的静态团队（含一个负责整体评估的
   Supervisor）用一张 Role×Stage 矩阵表达。
4. **循环（Loop）动态结构显式化**：多 Agent 在运行时形成的迭代循环被统一定义，每个循环跨越
   多个阶段。
5. **模板归位**：所有 `agent-*` 模板与 create-agent 技能形成整体，集中在
   `skills/create-agent/templates/`。

下面各节即为这一模型与其落地结构。

## 二、概念模型：三维属性 + 两种结构

一个 **Agent** 由三个正交的属性维度完整描述，再叠加两种组织结构：

### 2.1 三个属性维度

1. **Role（角色）**：定义 Agent 承担的职责以及看问题的视角。共有 **7 个 Worker 角色 + 1 个 Meta 角色**（见下表）。
2. **Stage（阶段）**：同一角色在执行过程中的三种阶段——**执行者（executor）**、**评估者（evaluator）**、**优化者（optimizer）**。
3. **Type（类型）**：区分 **Worker Agent（工作 Agent）** 与 **Meta Agent（元 Agent）**：
   - **Worker Agent**：处理项目中的实际任务；
   - **Meta Agent**：优化和处理其他 Agent（Team Supervisor 就是一种 Meta Agent，负责监控整个团队与其他 Agent 的表现）。

**Type 按操作对象判定（不由 Stage 推导）**：Stage 与 Type 是两个**正交维度**——Stage 回答
"处于协作流程的哪一站"（横向分工），Type 回答"操作对象处于哪个抽象层次"（纵向分层）。
判据：操作对象是**其他 agent / skill / 定义 agent-skill 的配置** → **Meta**；操作对象是
**业务工件与业务信息本身** → **Worker**。Stage 只提供默认倾向，判据优先。

> 历史修订：旧的 "Type-follows-Stage"（evaluator/optimizer 一律 Meta）已被本判据取代。
> 该耦合会把**业务层评估者**系统性误标为 Meta（例：评估各仓库状态的 consistency-checker
> 实为 evaluator 阶段的 Worker）。唯一保留的耦合是 **Team Supervisor 恒为 Meta**——
> 它的操作对象天然是 agent 系统。判据详见 `skills/create-team/references/conceptual-model.md`。

> **Meta 与写权限是单向蕴含,不是充要关系**:只有 `Meta` 类型的 Agent 才能修改**团队自身配置**
> (team.md)、**Agent 定义**(`.specify/agents/{templates,instances}/*.agent.md`、角色/阶段模板)与 **Skill 定义**
> (SKILL.md 及其引用/模板)。因此"需要写这些东西的 Agent ⇒ 必为 Meta"成立(**必要条件**)。
> 但反向不成立:"拥有评估者 / 优化者 / 持续优化角色 ⇏ 就是 Meta"(**非充分**)。这正是旧耦合
> 令人误解之处——复杂团队里做持续优化的 Agent 通常确实会改写 prompt / Agent 定义 / Skill 指南,
> 于是"看起来"优化者必为 Meta;但若某个持续优化 Agent 优化的是**业务工件本身**(收紧一份 spec、
> 重构产品代码、润色文档),无论其循环多么长期迭代,它仍是 **Worker**。判定 Type 要看**它写什么**,
> 而不是它叫什么角色。

### 2.2 两种组织结构

- **Team（团队，静态结构）**：多个 Agent 在静态结构上组成的团队，可用一张 Role×Stage 二维矩阵表达（见 §三），含一个负责整体评估与协调的 Team Supervisor。
- **Loop（循环，动态结构）**：多 Agent 在运行时形成的迭代循环，每个循环跨越多个 Stage；同一角色在不同阶段扮演不同 Type，或由多个 Agent 分别承担不同 Stage。Loop 的运行机制见 [quality-loop.md](./quality-loop.md)。

## 三、Team 的二维矩阵表达

一个 Team 可用一张二维表格描述：**每一行代表一个 Agent（按 Role 划分）**，
**每一列代表工作过程中的一个 Stage**，**整张表格整体代表一个团队**。
行列交叉的单元格用 **Worker** / **Meta** 表示该 Agent 在对应阶段的 Type 属性。

下表的角色与阶段均来自 `skills/create-agent/templates/` 中的能力（Capacity）模板（`agent-capacity-*`）
与阶段模板（`agent-stage-*`）：

| Agent 角色（Role） \ Stage | 执行者（Executor） | 评估者（Evaluator） | 优化者（Optimizer） |
| --- | --- | --- | --- |
| 需求分析师（Requirements Analyst） | Worker | Worker | Worker |
| 用户体验分析师（UX Analyst） | Worker | Worker | Worker |
| 系统架构师（System Designer） | Worker | Worker | Worker |
| 模块设计师（Module Designer） | Worker | Worker | Worker |
| 测试工程师（Test Engineer） | Worker | Worker | Worker |
| 质量保证工程师（QA Engineer） | Worker | Worker | Worker |
| 知识管理员（Knowledge Manager） | Worker | Worker | Worker |
| 团队监督者（Team Supervisor） | Meta | Meta | Meta |

说明：

- **行 = Role**：每个 Agent 占一行。前 7 行为 **Worker 角色**，最后一行 **团队监督者（Team Supervisor）** 为**唯一的 Meta 角色**，统一承担任务协调与团队监督职责。
- **列 = Stage**：对应三个阶段——执行者（executor）、评估者（evaluator）、优化者（optimizer）。
- **单元格 = Type**：按**操作对象**判定。7 个 Worker 角色在三个阶段的操作对象都是**业务工件**（需求、设计、代码、测试、文档），故均为 **Worker**——评估自己领域的业务产物不会使其变成 Meta；Team Supervisor 的操作对象是 agent 及其产出的元属性，各阶段均为 **Meta**。若某 Worker 角色的实例改为评估/优化 **agent 或 skill 本身**，则该实例为 Meta。

> **关于 UX Analyst**：用户体验分析师（UX Analyst）是内置的第 7 个 Worker 角色，负责分析与优化
> **所有用户接口**——不仅是前端 / GUI 页面，也包括命令行（CLI）设计，以及 `/command` 与 skill 等
> 与用户交互的部分。它以需求为输入、并评审既有接口，向 System Designer 与 Module Designer 输出
> 跨全部用户界面（前端、CLI、命令、技能）的 UX 规范与交互契约。模板
> `agent-capacity-ux-analyst-template.md` 与持久化 Agent `.specify/agents/templates/ux-analyst.agent.md` 均已提供。

## 四、Agent 的两种生命周期

> **Class → Instance（类与实例）**：`skills/create-agent/templates/agent-capacity-<X>-template.md` 是一个**抽象的 Agent 类**——带有未填充的 `{{占位符}}`，描述该 Agent **能做什么**（Capacity）。调用 `create-agent` 是**实例化**过程：填充占位符，产出一份**具体的 Agent 定义**写入所属层目录（Template → `.specify/agents/templates/<slug>.agent.md`，Instance → `.specify/agents/instances/<slug>.agent.md`）。运行时 `/speckit.agents run` 再从该定义**派生出活动实例（object）**——同一定义可派生多个互相独立的实例。三层关系：**能力模板（抽象类）→ 落地定义（具体类）→ 运行实例（对象）**，规范术语为 **Agent Template → Agent Instance → Agent Execution**（分类法真源：`shared/definitions/agent-definitions.md`；Execution 层的三种派发模式见 `shared/definitions/subagent-definitions.md`）。`create-agent` / `improve-agent` 只作用于前两层，从不触碰运行实例。

1. **临时 Agent（temporary）**：仅在当前上下文中记录，随会话结束而消失。
2. **持久化 Agent（persistent）**：保存到项目的分层 Agent 目录 `.specify/agents/templates/`（角色模板）或 `.specify/agents/instances/`（实例），可跨会话复用。

持久化 Agent 以 `.specify/agents/templates/` 与 `.specify/agents/instances/` 为**唯一真源**（按层），并通过 `specify init`（或安装流程）为各工具建立**逐文件软链接**。
以 qoder 工具为例，`.qoder/agents/` 是一个**真实目录**，其中每个 `.specify/agents/{templates,instances}/<slug>.agent.md`
都对应一条软链接 `.qoder/agents/<slug>.agent.md -> ../../.specify/agents/templates/<slug>.agent.md`；
`.github/agents`、`.qoder/agents`、`.opencode/agents`、`.hermes/agents` 同理。
逐文件（而非整目录）软链接的好处是：工具目录中可以让框架 Agent 与该工具自建的 Agent（例如
qoder 覆盖内置专家用的同名 `.md`）**并存**。目录与发现细节见 [templates-and-agents.md](./templates-and-agents.md)。

## 五、多 Agent 使用场景（编排与组合）

多个 Agent 的**编排与组合**由**团队域**承载：全部经由 `create-team` 技能（`/speckit.team` 命令）落地，
共有**四种**协作模式，每种编码一种优先取向——

- **parallel（效率优先）**：相互独立、无共享状态的任务，按不相交领域并发拆分；
- **serial（质量优先）**：有严格前序依赖的阶段流水线，每步与前序间做简单验证后才推进；
- **iteration（目标收敛）**：多个 Agent 组成含**唯一 Team Supervisor** 的两层闭环，反复打磨到质量阈值即交付；
- **continuous（长期运营）**：按 cadence 长期运行，每个 cycle 在预算 / 约束 / 独立验证 / 状态脊柱下处理源源不断的工作。

> 概念、四模式语义、目录布局与操作细节均在**团队文档集**：
> [`docs/teams/overview.md`](../teams/overview.md)、[`docs/teams/orchestration.md`](../teams/orchestration.md)、[`docs/teams/continuous-operations.md`](../teams/continuous-operations.md)；
> 单一真相源为 [`skills/create-team/references/conceptual-model.md`](../../../skills/create-team/references/conceptual-model.md) 与 [`operating-loops.md`](../../../skills/create-team/references/operating-loops.md)。
> 本框架文档只保留「团队 = 静态 Team 矩阵 + 动态 Loop」这一**概念**（见 §二、§三），不再复述编排操作。

## 六、实现结构

### 6.1 命令入口（单 Agent 与团队分离）

单 Agent 与团队操作有各自的命令入口：

- `/speckit.agents` 是**单 Agent** 操作的唯一入口——创作或优化**一个** Agent；不新增其他单 Agent 命令，本身不内联渲染模板。
- `/speckit.team` 是**团队**操作的唯一入口——组织或运行多个 Agent（parallel / serial / iteration / continuous）。

单 Agent 命令工作流程：

1. **识别用户意图**：分析用户输入，判断是创作还是优化单个 Agent。
2. **调用 `create-agent` 技能**：按模板创建对应工具的 Agent 配置。
3. **调用 `improve-agent` 技能**：基于反馈优化已有 Agent。
4. **团队意图重定向**：若用户请求组织 / 运行多个 Agent，重定向至 `/speckit.team`，不在此处理。

命令与路由细节见 [command-and-skills.md](./command-and-skills.md)。

### 6.2 技能

单 Agent 域（`/speckit.agents`）：

- **`create-agent`**：创作引擎——按 `Role × Stage × Type` 从模板生成 role / supervisor / custom / project-custom 等**单个** Agent。
- **`improve-agent`**：优化引擎——基于真实使用反馈精炼**单个** Agent 制品（角色模板 / 监督片段 / 自定义 Agent）。

团队域（`/speckit.team`）：

- **`create-team`**：团队引擎——定义并运行团队，实现并行、串行、迭代收敛、长期运营四种协作模式。
- **`improve-team`**：团队优化引擎——基于运行反馈精炼团队结构（阶段 / 编排 / 阈值 / 成熟度）。

### 6.3 模板归位

所有 `agent-*` 模板集中在 **`skills/create-agent/templates/`**，作为 create-agent 技能的一部分；
安装时镜像到 `.specify/skills/create-agent/templates/`。完整模板目录见 [templates-and-agents.md](./templates-and-agents.md)。

### 6.4 技能赋能（Skill Enablement）

技能与 Agent 定义同步安装，因此每个内置 Agent 都可调用任意已安装技能。七个内置角色 Agent 将这一能力**显式化、一致化**：优先使用与角色相关的框架技能，而非手工重复同类操作。每个角色 Agent 及其 `agent-capacity-*`（Capacity）模板都声明两部分：

- **`skills:` 前置字段**：该角色相关的已安装技能规范 slug 列表（如需求分析师 → `draw-plantuml`；模块设计师 → `study-project`）。元 / 框架创作类技能（`create-agent`、`improve-agent`、`create-skills`、`improve-skills`、`create-team`、`improve-team`）为**不可声明**，不出现在任何角色列表中。
- **`## Skill Enablement` 正文小节**：共享的偏好协议（单一事实来源 `skills/create-agent/templates/agent-skill-enablement.md`，各 Agent 组合复用而非各自改写）+ 与 `skills:` 一致的 `| Skill | When to use |` 表格。协议要求：优先选用适用技能；多个适用时选最贴合角色者；无适用技能或技能不可用 / 失败时，直接完成操作并暴露失败。

契约测试 `tests/contract/test_agent_skill_enablement.py` 校验该约定（每个 Agent ≥1 技能、引用均已安装、无不可声明 slug、小节存在、模板与 Agent 保持一致）。约定细节见 [command-and-skills.md](./command-and-skills.md)。

## 七、可追溯性

本文档以仓库中的**活制品**为规范来源，而非任何单份规格文档：

- **模板目录**：`skills/create-agent/templates/`（单 Agent）与 `skills/create-team/templates/agents/`（多 Agent）。
- **持久化 Agent**：`.specify/agents/{templates,instances}/*.agent.md`。
- **守卫测试**：`tests/contract/test_agent_skill_enablement.py`（技能赋能约定）、`tests/unit/test_agent_deprecated_terms.py`（术语规范，持续保证 `Stage` / `optimizer` 等命名在所有 live 制品中成立）。
