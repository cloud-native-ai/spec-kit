# Requirements Specification: 「驱动子代理」机制的技能化分解与公用化（create-agent / improve-agent / run-agent 增强）

**Requirement Branch**: `060-decompose-subagent-dispatch`  
**Created**: 2026-10-16  
**Status**: Draft  
**Input**: User description: "sdd-loop-driver和sdd-project-setup都涉及到'驱动子代理'去调用speckit命令的流程,需要将驱动子代理这部分按照之前 .specify/specs/057-decompose-command-skills 中定义的方法进行拆分和复用. 当前我们在 .specify/shared/definitions/agent-definitions.md 中为子代理(agent)定义了三个概念:1)Template;2)Instance;3)Execution; 需要针对这一概念进一步深化, 让'驱动子代理'成为一个公用且通用的机制. 另外按照 Template -> Instance -> Execution 这个抽象层次逐步明确具体细节, 以sdd-loop-driver和sdd-project-setup技能为例到了 Agent Execution 这一层就是具体的ssh+su+qodercli了. 总体要求是:在现有的 skills/internal/create-agent/SKILL.md skills/internal/improve-agent/SKILL.md skills/internal/run-agent/SKILL.md体系上做增强,然后让 sdd-loop-driver和sdd-project-setup 技能通过委派这三个技能的方式完成需要'驱动子代理'的任务; 在抽象层次上: '我需要一个能够以项目目录作为工作目录,能加载项目上下文执行SDD流程的代理' -> Agent Template; '我需要一个用来执行setup操作一个用来执行requirement操作' -> Agent Instance( x 2); '我需要使用ssh 登录到开发环境 *.*.*.*(IP地址), 然后以*用户(su或sudo)执行Agent命令(qodercli/claude code)' -> Agent Execution"

## Related Feature *(mandatory)*

**Feature ID**: Need clarification  
**Feature Name**: Need clarification

## User Scenarios & Testing *(mandatory)*

### 现状锚点（2026-10-16 以源码与制品实测为准；dated record，仅作可行性输入，非运行时保证）

- **三层分类法已在册**：Agent Template / Agent Instance / Agent Execution 三词条为 glossary confirmed 条目，真源 [[agent-definitions.md]]；执行三模态（native / virtual / external）、模态选择规则、外部派发可见性契约与派发时治理义务的真源为 [[subagent-definitions.md]]。
- **拓扑配方已有公用落点**：[[STR-006]]（2026-10-15 落盘）已承载六条配方——断点探测、阶段化 prompt 文件、runner 脚本与派生、后台执行+日志回传+轮询、本地直驱变体、构建固化分线变体。
- **run-agent 现边界**：Run Mode 为「单代理单任务」派发，模态选择遵循 subagent-definitions，外部派发强制可见性契约与注入子句；显式声明多代理编排外派 `/speckit.team`。
- **两技能仍各自内联派发机制**：[[STR-004]] 在 `references/dispatch-recipes.md` 内联五族前置检查表 + Recipe 0–3（断点探测/提示词落盘/runner 派生/脱离派发+轮询），在 `references/stage-prompts.md` 内联三段骨架；[[STR-005]] 在 `references/setup-recipes.md` 内联同型五族前置检查表与远端命令形态。两技能之间、以及与外派配方真源之间存在同型副本。
- **反嵌套红线现为本技能专属**：「Driver Topology（驱动拓扑，反嵌套红线）」节 + HR-6 + 两处提示词红线当前落在 [[STR-004]] 内（2026-10-16 缺陷修复产物），尚未上升为公用派发机制的治理义务。

### Assumptions（对输入中开放点的缺省裁决，clarify 阶段可推翻）

- 「SDD 执行者」能力模板进**框架分发角色集**（源码 `agents/` 目录，`specify init` 安装到项目）——「公用且通用」要求跨项目可用，项目侧私有模板不满足；若推翻则退为项目侧容量模板。
- 阶段实例**按需创建**（首次驱动某项目某阶段时实例化），不预建全部阶段的全量实例。
- 拓扑声明的子代理 CLI 集沿用既有两形态（qodercli / claude），本特性不新增 CLI 适配。
- run-agent 的拓扑输入接受**内联参数**与**执行配置文件**（`.specify/agents/execution/configs/` 既有形态）双形态，二者等价。

### User Story 1 - 从能力模板到职责实例的创建面（create-agent 增强） (Priority: P1)

编排者（人或驱动技能）说出能力级需求——"我需要一个能以项目目录为工作目录、加载项目上下文、执行 SDD 流程的代理"——经 create-agent 产出（或定位到）一个 **Agent Template** 层的「SDD 执行者」能力模板；随后说出职责级需求——"一个执行 setup 操作、一个执行 requirements 操作"——从**同一模板**实例化出 ≥2 个 **Agent Instance**，各绑定一个具体职责，实例引用模板而非复述能力。

**Why this priority**: 三层阶梯的上两层是公用机制的骨架——没有可复用的模板与实例，每个驱动方只能继续内联各自的代理描述，公用化无从谈起。

**Independent Test**: 仅实现本故事即可用 create-agent 完整走一遍「模板 → 双实例」创建流程并交付可用制品；不依赖任何执行派发能力。

**Acceptance Scenarios**:

1. **Given** 项目已安装框架角色集, **When** 用户经 create-agent 声明能力级需求（项目工作目录 + 项目上下文 + SDD 流程执行）, **Then** 产出「SDD 执行者」能力模板，能力面与占位符齐备、职责无关，创建过程可复现。
2. **Given** 模板在位, **When** 用户经 create-agent 声明两个职责级需求（setup 操作 / requirements 操作）, **Then** 产出两个 Agent Instance，各自绑定单一职责、引用同一模板，且实例体对模板能力的复述为零。

---

### User Story 2 - 拓扑声明与执行派发面（run-agent 增强） (Priority: P1)

编排者说出运行级需求——"ssh 登录到开发环境某 IP、以某用户（su/sudo）执行 Agent 命令（qodercli / claude）"——作为 **Agent Execution** 层的拓扑声明连同实例引用交给 run-agent；run-agent 解析实例与拓扑、按既有三模态规则选择执行形态、对外部形态执行可见性契约与派发时治理义务，发起真实执行并回传结果。同一实例在本地直驱与远端 ssh 两拓扑下均可发起执行，拓扑差异全部落在 Execution 声明，Template / Instance 制品零改动。

**Why this priority**: Execution 层是抽象阶梯的落地端——拓扑参数化（环境、身份、CLI、工作目录全部入口化）是两技能内联配方得以坍缩的前提。

**Independent Test**: 仅实现本故事即可对任一既有实例分别以本地与远端拓扑声明发起真实执行并审计其命令形态；不依赖两技能的委派化改造。

**Acceptance Scenarios**:

1. **Given** 一个在册实例与本地拓扑声明（项目目录+CLI）, **When** run-agent 发起执行, **Then** 执行在声明的项目目录内以声明的 CLI 运行，结果（或可见性三元组）回传给调用方。
2. **Given** 同一实例与远端拓扑声明（ssh 目标+运行用户+项目目录+CLI）, **When** run-agent 发起执行, **Then** 命令形态符合拓扑声明（ssh → su → CLI），Template / Instance 制品与本地拓扑所用逐字节相同。
3. **Given** 任一拓扑下的派发, **When** 审计 outgoing 提示词, **Then** 提示词不引用任何驱动/循环技能、不指示加载技能（反嵌套红线在公用派发面生效）。

---

### User Story 3 - 两技能的委派化改造（行为平价搬家） (Priority: P1)

sdd-loop-driver 与 sdd-project-setup 把各自内联的「驱动子代理」机制段（前置检查、断点探测、提示词文件、runner 派生、脱离派发+轮询、命令形态）按 057 技能化分解方法委派给三个技能：实例创建走 create-agent、执行派发走 run-agent、证据改进走 improve-agent；两技能体只保留各自编排本体（SDD 六阶段循环 / 调协五步）与对三技能的调用说明，内联副本坍缩为对公用真源的引用。对最终用户，两技能的入口话术与循环/调协行为在平价前提下不变。

**Why this priority**: 这是本特性的核心收益——消除两技能间及与公用配方间的同型副本，让「驱动子代理」从两份私有实现变为一份公用机制；前两个故事是它的承接面。

**Independent Test**: 改造后对任一目标项目（本地拓扑）完整驱动一个 SDD 阶段与一个调协步骤，行为与改造前平价；机制段副本经全仓检索归零。

**Acceptance Scenarios**:

1. **Given** 两技能已完成委派化改造, **When** 逐条比对改造前的派发义务清单（五族前置检查、断点探测、三段骨架、runner 派生、脱离派发+轮询、哨兵与独立校验、状态脊先写后动）, **Then** 每条义务在承接面以同等或更严强度存在、逐条可追溯、零丢失。
2. **Given** 改造后的两技能体, **When** 全仓检索机制段原文（前置检查表行、ssh+su 配方形态、prompt 文件/runner 机制正文）, **Then** 每条派发事实恰有一个权威定义点，技能体内仅存引用。
3. **Given** 两技能的编排本体（六阶段循环/状态脊/卡死处置；调协五步/候选清单）, **When** 审计三技能的承接面, **Then** 编排本体未被搬入——职责切分线保持（框架调协=SDD 执行者 setup 实例职责；SDD 阶段执行=阶段实例职责；循环驱动=驱动技能本体）。

---

### User Story 4 - 执行证据回流（improve-agent 承接） (Priority: P2)

真实执行产生的证据——执行日志、可见性三元组、异常回传行、失败模式（如嵌套驱动、拓扑误配）——经 improve-agent 回流为 Template / Instance 层的定向修正；Agent Execution 本身仍是 own-run 证据而非自改对象（既有 Self-Improvement 边界）。

**Why this priority**: 闭环价值——没有回流，模板与实例会随真实使用漂移失修；但它依赖前三个故事产生的真实执行流，属增强而非骨架。

**Independent Test**: 以一次已知失败的真实执行记录为输入走 improve-agent 流程，产出对模板或实例的定向修正且 Execution 产物未被改动。

**Acceptance Scenarios**:

1. **Given** 一次执行留下的失败证据（如反嵌套违例记录）, **When** 经 improve-agent 发起改进, **Then** 修正落在 Template 或 Instance 层制品，Execution 的日志与产物零改动。
2. **Given** 同一失败模式重复出现, **When** 比对修正前后的实例, **Then** 职责面变更发生在实例层、能力面变更发生在模板层，未发生越层改动。

---

### Edge Cases

- 宿主 agent 无子代理能力 → run-agent 按既有模态选择退化为 virtual（会话内模拟），派发时治理义务同等生效，不因模态放宽。
- 远端环境 CLI 不在执行身份 PATH、运行用户不存在或为 root → 前置检查失败处置链按平价落位（处置归属在 plan 阶段随副本坍缩一并裁定）。
- 把驱动手册整体喂给子代理的嵌套驱动企图 → 公用派发面在派发前拦截（上收后的反嵌套治理义务），MUST NOT 依赖各驱动技能自查。
- 多线并行（如两项目各一线）→ 每线独立实例与拓扑声明，并发隔离纪律随平价保留。
- 实例引用的模板缺失或被删 → run-agent 解析失败按快速失败停机，MUST NOT 静默降级为内联替代。
- push 与破坏性动作 → 既有确认门控分类不变，随平价保留。

## Requirements *(mandatory)*

### Functional Requirements

#### 概念深化与真源（US1 / US2 前置）

- **FR-001**: 三层语义的深化 MUST 落在既有概念真源内完成——[[agent-definitions.md]]（三层判定、变换链、存储布局）与 [[subagent-definitions.md]]（三模态、可见性契约、治理义务）各自增补「驱动子代理作为公用机制」的判定与接线说明；MUST NOT 新建平行的定义文档或第三数据源（One Source Of Truth）。
- **FR-002**: 抽象阶梯的层界语义 MUST 固化为可判定规则——Template 层回答"能做什么"（项目目录为工作目录、加载项目上下文、执行 SDD 流程的能力面）；Instance 层回答"为谁做什么"（职责绑定，×N 实例源自同模板）；Execution 层回答"在哪里怎么跑"（ssh 目标+运行用户+CLI+项目目录的运行拓扑）；每层变更不越层泄漏（改能力不去改拓扑，改拓扑不去改能力）。

#### create-agent 承接面（US1）

- **FR-003**: create-agent MUST 支持创建「SDD 执行者」能力模板并进框架分发角色集（源码 `agents/` 目录，`specify init` 安装），其能力面声明：以项目目录为工作目录、加载项目 `.specify/` 上下文、执行 `/speckit.*` 阶段命令；模板保持职责无关（无 setup/requirements 等具体职责字样）。
- **FR-004**: create-agent MUST 支持从同一模板实例化多个职责实例（setup 操作者、requirements 执行者等），实例 MUST 以引用绑定模板能力、复述为零，并按既有 Instance 层存储与校验规则落位。
- **FR-005**: 实例的职责绑定 MUST 以单职责为最小面：一实例一职责；职责演进走实例层，能力演进走模板层，二者经 improve-agent 分流。

#### run-agent 承接面（US2）

- **FR-006**: [[STR-003]] 的 run-agent MUST 接受 Execution 拓扑声明（本地：项目目录+CLI；远端：ssh 目标+运行用户+项目目录+CLI）连同实例引用，解析为一次具体执行；拓扑要素全部入口参数化，零硬编码（sdd-loop-driver 既有约定上升为公用机制约束）。
- **FR-007**: run-agent 的执行形态 MUST 遵循 subagent-definitions 既有模态选择规则；[[STR-003]] 的外部形态 MUST 满足可见性契约（stream-json + 紧凑化 + 三元组）与派发时治理义务（注入子句 + 异常回传行）——新拓扑形态不构成放宽理由。
- **FR-008**: [[STR-003]] 的具体拓扑配方 MUST 引用 [[STR-006]]（断点探测、阶段提示词文件、runner 派生、后台执行+轮询、本地直驱变体），技能体 MUST NOT 复制配方正文（057 式引用真源）；配方缺失的形态按快速失败报告，MUST NOT 就地发明。
- **FR-009**: 反嵌套治理 MUST 上收为公用派发义务：[[STR-003]] 派发的任何子代理提示词 MUST NOT 引用驱动/循环技能、MUST NOT 指示加载技能、MUST NOT 包含循环逻辑（现 [[STR-004]] 的 Driver Topology 红线上升为机制级）；拦截发生在派发前（派发前自检既有机制），不依赖各驱动技能自查。

#### 两技能委派化（US3）

- **FR-010**: [[STR-004]] 与 [[STR-005]] 两技能的「驱动子代理」机制段 MUST 委派三技能完成——实例创建委派 [[STR-001]]、执行派发委派 [[STR-003]]、证据改进委派 [[STR-002]]；两技能体仅保留各自编排本体（SDD 六阶段循环+状态脊+卡死处置 / 调协五步+候选清单）与对三技能的调用说明（输入/产出），机制段程序性内容按 057 方法清零。
- **FR-011**: 行为平价 MUST 作为改造验收基线：两技能现有全部派发义务（五族前置检查、断点探测、三段骨架、runner 派生、脱离派发+轮询、哨兵与独立校验、状态脊先写后动、push 门控、脏文件纪律）以同等或更严强度落入承接面，逐条可追溯、零丢失。
- **FR-012**: 重复副本 MUST 坍缩为单 owner：五族前置检查表（现两技能各一份）、ssh+su 命令形态（现两技能与 [[external-dispatch-recipes.md]] 三处）、提示词文件与 runner 机制等，改造后每条派发事实在仓内恰一个权威定义点，其余位置一律引用；真源归属逐条在 plan 阶段裁定并登记。
- **FR-013**: 编排本体 MUST NOT 外移：SDD 六阶段循环、状态脊、卡死处置、收尾纪律（归 sdd-loop-driver）与调协五步、候选清单、软协同契约（归 sdd-project-setup）不得被搬入三技能——职责切分线维持（驱动与调协是编排，创建/派发/改进是承接）。

#### improve-agent 承接面（US4）

- **FR-014**: 执行证据（日志、三元组、异常回传行、失败模式）MUST 可经 [[STR-002]] 的 improve-agent 回流为 Template / Instance 层定向修正；Agent Execution 是 own-run 证据而非自改对象（既有 Self-Improvement 边界不变）。

#### 非回归

- **FR-015**: 既有外部行为零变更：三技能既有调用方（`/speckit.agents` 路由、团队流程）的输入输出契约不变；两技能对最终用户的入口话术、循环/调协行为在平价前提下不变；`/speckit.team` 与 create-team 体系零改动（多代理团队编排不在本特性范围）。

### 显式排除项（Out of Scope）

- `/speckit.team`、create-team、improve-team 及团队编排机制零改动——多代理团队是另一条机制线（FR-015）。
- 各 `/speckit.*` 阶段命令（requirements/plan/tasks/...）与治理命令的内部流程零改动——本特性只改变"谁去驱动它们执行"，不改命令本身。
- 子代理 CLI 集不新增适配（qodercli / claude 之外），CLI 层适配属另一维度（Assumption A3）。
- 不新建平行的代理定义文档或第三数据源——深化只在既有两份真源内完成（FR-001）。
- 不迁移 `/speckit.agents` 命令模板本身的路由职责——run-agent 的入口接线维持现状。

### Key Entities *(include if requirement involves data)*

- **Agent Template / Agent Instance / Agent Execution**: 定义与边界以 [[agent-definitions.md]] 为唯一真源，本特性不重定义；新增取值仅「SDD 执行者」模板与各阶段职责实例。
- **Execution 拓扑声明**: 一次执行的环境要素——本地/远端形态、运行身份、项目目录、子代理 CLI、提示词来源；全部为入口参数，持久形态为执行配置文件（`.specify/agents/execution/configs/`）或内联声明。
- **派发义务集**: 模态选择、可见性三元组、注入子句、异常回传行、反嵌套红线——各自真源均在既有文档（subagent-definitions / fast-fail / 外派配方），本特性只做接线与上收，不新设义务定义。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 同一「SDD 执行者」模板成功实例化 ≥2 个不同职责实例，实例体对模板能力的复述为零（引用关系可由制品检索机器判定）。
- **SC-002**: 同一实例以本地与远端两种拓扑声明各完成一次真实执行（远端形态允许以命令形态审计替代实跑），两种形态下 Template / Instance 层制品逐字节相同——拓扑差异全部落在 Execution 声明。
- **SC-003**: 两技能体内派发机制副本归零：五族前置检查表、ssh+su 命令形态、提示词文件/runner 机制各恰有 1 个权威落点（全仓检索计数），且改造前后义务清单逐条比对零丢失。
- **SC-004**: 端到端：经 run-agent 派发一个阶段实例在本地项目完成一个 SDD 阶段，回传满足三条件（完成尾标/产物在位/显式异常行），全程审计子代理输入零驱动技能引用。
- **SC-005**: 既有契约与集成测试套件全部通过，失败名单与实现前基线逐名比对零新增（name-level）。
- **SC-006**: 概念真源增补后，三层词条的 owner 集合不变（仍为 [[agent-definitions.md]] 与 [[subagent-definitions.md]]），全仓无第三处新增定义性正文。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 实例制品检索（模板引用字段 + 能力复述 grep 计数），实现后一次性采集。
- **SC-002 Source**: 本地拓扑实跑一次 + 远端拓扑以派发命令形态审计（ssh/su/CLI 逐要素比对）；Template/Instance 制品 diff 为空判定。
- **SC-003 Source**: 改造前冻结义务清单与机制段原文清单（逐条登记于 tasks 前提测量），改造后全仓 grep 计数 + 逐条追溯表核对。
- **SC-004 Source**: 真实端到端执行的回传记录与子代理输入文件审计（反嵌套检索），实现后一次性采集。
- **SC-005 Source**: `pytest tests/contract/ tests/integration/` 全量运行，与实现前基线失败名单 comm 比对。
- **SC-006 Source**: 三层词条 owner 声明行检索 + 全仓定义性正文定位（每词条恰一 owner 文档）。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `skills/internal/create-agent/SKILL.md` | FR-010, 后续契约测试与任务项 |
| `STR-002` | `skills/internal/improve-agent/SKILL.md` | FR-010, FR-014, 后续契约测试与任务项 |
| `STR-003` | `skills/internal/run-agent/SKILL.md` | FR-006, FR-007, FR-008, FR-009, FR-010, 后续契约测试与任务项 |
| `STR-004` | `skills/external/sdd-loop-driver/SKILL.md` | FR-009, FR-010, 现状锚点, 后续契约测试与任务项 |
| `STR-005` | `skills/external/sdd-project-setup/SKILL.md` | FR-010, 现状锚点, 后续契约测试与任务项 |
| `STR-006` | `.specify/shared/workflow/external-dispatch-recipes.md` | FR-008, 现状锚点, 后续契约测试与任务项 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
