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

## 五、多 Agent 使用场景

框架支持三类多 Agent 协作拓扑，全部经由 `organize-agents` 技能落地（操作细节见
[multi-agent-orchestration.md](./multi-agent-orchestration.md)）：

1. **并行操作（Parallel Dispatch）**：多个 Agent 并行执行，通过并行度提升效率（领域隔离 → 并行派发 → 结果聚合）。
2. **串行操作（Serial Chain）**：多个 Agent 串行执行，每个 Agent 负责一个阶段性工作，互相配合完成复杂而长期的任务（阶段 N 的产物作为阶段 N+1 的输入）。
3. **团队闭环（Team Loop）**：多个 Agent 组织成一个团队，构成闭环可自迭代的系统。该系统为**两层结构**：
   - **监督 + 协调层**：Team Supervisor（Meta 角色）——质量门禁、收敛决策、任务分解、Agent 派发、进度监控；
   - **执行层**：Worker Agents（7 个预置角色 + 自定义 Agent）——产出交付物。

## 六、实现结构

### 6.1 唯一命令入口

`/speckit.agents` 是所有 Agent 相关操作的**唯一命令入口**，不新增其他命令。其职责是
**识别用户意图 → 委派给对应技能**，本身不内联渲染模板。工作流程：

1. **识别用户意图**：分析用户输入，判断是创作、优化还是编排。
2. **设计/确定团队结构**：根据意图确定所需角色与协作拓扑。
3. **调用 `create-agent` 技能**：按模板创建对应工具的 Agent 配置。
4. **调用 `organize-agents` 技能**：将这些 Agent 按 parallel / serial / team-loop 编排起来。

命令与路由细节见 [command-and-skills.md](./command-and-skills.md)。

### 6.2 三个技能

- **`create-agent`**：创作引擎——按 `Role × Stage × Type` 从模板生成 role / supervisor / triad / custom / team-supervisor 等 Agent。
- **`improve-agent`**：优化引擎——基于真实使用反馈精炼任意 Agent 制品（角色模板 / 阶段模板 / 编排提示 / 监督片段 / 自定义 Agent）。
- **`organize-agents`**：编排引擎——实现并行、串行、团队闭环三种拓扑。

### 6.3 模板归位

所有 `agent-*` 模板已从顶层模板目录迁移至 **`skills/create-agent/templates/`**，作为 create-agent 技能的一部分；
安装时镜像到 `.specify/skills/create-agent/templates/`。完整模板目录见 [templates-and-agents.md](./templates-and-agents.md)。

### 6.4 技能赋能（Skill Enablement）

技能与 Agent 定义同步安装，因此每个内置 Agent 都可调用任意已安装技能。七个内置角色 Agent 将这一能力**显式化、一致化**：优先使用与角色相关的框架技能，而非手工重复同类操作。每个角色 Agent 及其 `agent-role-*` 模板都声明两部分：

- **`skills:` 前置字段**：该角色相关的已安装技能规范 slug 列表（如需求分析师 → `draw-plantuml`；模块设计师 → `analysis-project`）。仅引用类技能（`sdd-workflow`）与元/框架创作类技能（`create-agent`、`improve-agent`、`create-skills`、`improve-skills`、`organize-agents`）为**不可声明**，不出现在任何角色列表中。
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
