# Agent 改造方案

当前的 Agent 框架有些混乱，本文档作为当前框架 Agent 的优化方案，按「问题 → 预期结果 → 实现细节」的顺序组织。

## 一、当前 Agent 实现的问题

当前 Agent 实现的主要问题是 **Agent 的定义比较混乱**，具体表现为以下几个概念相互交织、边界不清：

1. **角色（Role）定义不清**：Agent 从角色的角度定义了自身承担的职责，以及在处理问题时看问题的视角，但这一层没有被清晰地抽象出来。
2. **阶段（Stage）与角色混淆**：同一角色的 Agent 在执行过程中存在不同的阶段 Stage，Stage 包含三种情况——执行者、评估者和优化者，对应当前模板目录中的三种 Stage，但 Stage 和 Role 的关系没有理顺。
3. **团队（Team）静态结构缺失**：多个 Agent 在静态结构上组成一个 Team，其中还有一个 Supervisor 角色，负责整体评估 Team 的运行情况；当它判断 Team 当前表现不佳时，需要暂停整个团队的运作并进行整体优化。这一静态组织结构当前没有被清晰表达。
4. **循环（Loop）动态结构缺失**：多 Agent 在动态结构上形成一个 Loop 结构，每一个 Loop 都有多个执行阶段，每一种角色的 Agent 在不同阶段扮演不同角色，或由多个 Agent 扮演不同的 Stage。这一动态运行机制当前也缺乏统一定义。
5. **模板分散**：各式各样的 `templates/agent-*` 模板散落在模板目录，未与 create-agent 技能形成整体。

## 二、预期结果

改造后，Agent 相关能力应满足以下目标：

1. **唯一入口**：`/speckit.agents` 作为所有 Agent 相关操作的唯一命令入口，不新增其他命令。命令的核心是识别用户意图，然后根据分析结果进行 Agent 的创建、编排和执行。
2. **清晰的概念模型**：一个 Agent 应由三个属性维度描述，再叠加两种组织结构——
   - **Role（角色）**：定义 Agent 承担的职责和看问题的视角。
   - **Stage（阶段）**：同一角色在执行中的三种阶段——执行者、评估者、优化者。
   - **Type（类型）**：Role 和 Stage 之外的第三个维度，区分 **Worker Agent（工作 Agent）** 和 **Meta Agent（元 Agent）**。Worker Agent 处理项目中的实际任务；Meta Agent 负责优化和处理其他 Agent（Supervisor 就是一种 Meta Agent）。
   - **Team（团队，静态结构）**：多个 Agent 在静态结构上组成的团队，含负责整体评估的 Supervisor。
   - **Loop（循环，动态结构）**：多 Agent 在动态结构上形成的循环，每个 Loop 含多个执行阶段。
3. **两类 Agent 生命周期**：
   - **临时 Agent**：在上下文中进行记录即可。
   - **持久化 Agent**：持久化到项目对应的 Agent 目录。
4. **支持三类多 Agent 使用场景**：
   - 多个 Agent 并行操作，通过并行度提升效率。
   - 多个 Agent 串行操作，每个 Agent 负责一个阶段性工作，互相配合完成复杂而长期的任务。
   - 多个 Agent 组织成一个团队，构成闭环可自迭代的系统（含实际工作 Agent、元 Agent、Supervisor 三类）。
5. **模板归位**：将各式各样的 `templates/agent-*` 模板迁移到 `skills/create-agent/templates` 目录，作为 create-agent 技能的一部分。
6. **术语统一**：统一 Agent 相关术语——废弃 SubRole 概念，统一使用 **Stage**；将 improver 统一改为 **optimizer**。

### 团队的二维矩阵表达（Team 视图）

一个 Team 可用一张二维表格描述：**每一行代表一个 Agent（按 Role 划分）**，**每一列代表工作过程中的一个 Stage**，**整张表格整体代表一个团队**。行列交叉的单元格用 **Worker** / **Meta** 表示该 Agent 在对应阶段的 Type 属性。

下表的角色及阶段均来自 `skills/create-agent/templates` 中定义的角色模板（`agent-role-*`）与阶段（Stage）模板（历史上曾命名 `agent-subrole-*`，现已重命名为 `agent-stage-*`）：

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

- **行 = Role**：每个 Agent 占一行，对应模板中的一个 `agent-role-*` 角色。前七个为 Worker 角色，最后一个 **团队监督者（Team Supervisor）** 为 Meta 角色——它由原「元协调器（Meta-Coordinator）」与「团队监督者（Team Supervisor）」合并而来，统一承担任务协调与团队监督职责。
- **列 = Stage**：对应模板中的三个 Stage——执行者（executor）、评估者（evaluator）、优化者（optimizer）。
- **单元格 = Type**：Worker 角色在执行者阶段为 **Worker**，在评估者/优化者阶段切换为 **Meta**；Meta 角色（Team Supervisor）不承担实际任务执行，各阶段均为 **Meta**。

## 三、实现细节

### 3.1 核心结构

- `templates/commands/agents.md`：`/speckit.agents` 命令的实现。
- `skills/create-agent` 技能：根据模板创建 agent。
- `skills/improve-agent` 技能：优化 agent。

### 3.2 Agent 的结构化描述（三个属性维度）

定义一个 Agent 时，应从三个正交的属性维度进行描述：

1. **Role（角色）**：定义 Agent 承担的职责以及看问题的视角。
2. **Stage（阶段）**：同一角色在执行过程中的三种 Stage——执行者、评估者、优化者。
3. **Type（类型）**：区分 **Worker Agent（工作 Agent）** 和 **Meta Agent（元 Agent）**：
   - **Worker Agent**：处理项目中的实际任务。
   - **Meta Agent**：优化和处理其他 Agent。Supervisor Agent 就是一种 Meta Agent，其作用是监控整个团队的运作情况和其他 Agent 的表现。

**Type 与 Stage 的关联**：在一个迭代流程中，同一个 Agent 的 type 会随阶段切换——处于**执行者**阶段时它是 Worker Agent，处于**评估者**和**优化者**阶段时它是 Meta Agent。

### 3.3 speckit.agents 命令工作流程

`/speckit.agents` 作为唯一命令入口，工作流程如下：

1. **识别用户意图**：根据用户输入首先进行意图识别。
2. **设计团队结构**：识别到用户意图后，根据分析结果设计整体 Agent 团队的结构。
3. **调用 create-agent 技能**：根据模板创建对应工具的 agent 配置。
4. **调用 organize-agents 技能**：将这些 agent 组织（编排）起来。

命令实现的基本结构可概括为：1）识别用户意图；2）调用 create-agent 技能创建对应工具的 agent 配置；3）调用 organize-agents 技能将 agent 组织起来。

### 3.4 Agent 的两种类型与持久化

Agent 分为两种：

1. **临时 Agent**：在上下文中进行记录即可。
2. **持久化 Agent**：需要在项目对应的 Agent 目录中进行持久化。

持久化的 Agent 需要保存到项目对应的目录 `.specify/agents` 中，然后再根据具体使用的工具情况，通过 `specify init` 命令进行对应工具的配置。针对 qoder 工具（当前使用的工具），是通过 `.qoder/agents -> .specify/agents` 的软链接来实现的。

### 3.5 多 Agent 使用场景

常用的多 Agent 场景有三类：

1. **并行操作**：多个 Agent 并行执行，主要为了通过并行度提高效率。
2. **串行操作**：多个 Agent 串行执行，每个 Agent 负责一个阶段性工作，互相配合完成一个复杂而长期的任务。
3. **团队闭环**：多个 Agent 组织成一个团队，最终构成一个闭环可自迭代的系统。此场景下 agent 分为三类：
   - 实际工作的 Agent；
   - 优化技能和其他 Agent 的「元 Agent」；
   - 负责评估和打分的 Supervisor Agent。

### 3.6 调研任务

针对上述目标，使用多 Agent 进行调研：`/cws_work/` 目录中的各个项目都是和 agent 相关的项目，其中有很多相关的最佳实践。除 `/cws_work/spec-kit` 目录外，需要为每个目录分配一个 agent 进行挖掘。调研结论需要和现有的 agent 相关机制进行融合，**不要创建新的命令**，所有 agent 相关操作都以 `speckit.agents` 命令作为唯一入口。

### 3.7 模板迁移

将各式各样的 `templates/agent-*` 模板，迁移到 `/cws_work/spec-kit/skills/create-agent/templates` 目录中，作为 create-agent 技能的一部分。

### 3.8 名词统一（术语规范化）

名词统一是本改造方案的一个重要步骤，用于消除当前概念混乱。统一规则如下：

1. **废弃 SubRole，统一使用 Stage**：文档与后续实现中不再使用 SubRole / Subrole 这一描述，同一角色在执行过程中的阶段统一称为 **Stage**。
2. **improver 统一为 optimizer**：优化者阶段的英文名统一从 improver 改为 **optimizer**（执行者 executor、评估者 evaluator 保持不变）。
3. **落地记录**（术语统一已在后续实现中完成，历史步骤记录如下）：
   - 模板目录下 `agent-subrole-*.md` 已重命名为 `agent-stage-*.md`；
   - `agent-subrole-improver-template.md` 已重命名为 `agent-stage-optimizer-template.md`，内部 `name`/`description` 中的 improver 同步改为 optimizer；
   - 已完成 `skills/create-agent/SKILL.md`、各编排模板及 `tests/` 中旧术语（subrole / improver）引用的迁移更新。

