# Requirements Specification: /speckit.agents run — 显式 run 子命令与 superagent/subagent 架构自动应用（Agents Run）

**Requirement Branch**: `104-agents-run`
**Created**: 2026-11-24
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（修订 `templates/commands/agents.md`、`skills/internal/run-agent/**`、`docs/reference/commands/agents.md`、`docs/reference/agents/**`、`docs/tutorials/**` 与 `tests/**` 的作者）与下游项目中通过 `/speckit.agents run` 派发子代理、需要判定「语法、角色自动性、多子代身份与可见性、错误路径」的维护者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 当需要判定「run 子命令是否显式受支持、语法如何」「一次 run 如何自动构成 superagent→subagent 边、当前 session 如何被声明为 superagent」「同一 superagent 下多次 run 如何区分、从哪里可见」「与既有 run-agent 技能、095 角色定义、/speckit.team 如何划界」「哪些文档面必须同步」「如何确定性验收」时打开本规格，据 FR-001…FR-024 与 SC-001…SC-007 决定 `/speckit.clarify` 与后续实现是否放行
**Input**: User description: "需要在agents命令中,创建一个run子命令, 当用户执行/speckit.agents run xxx 命令时自动应用superagent和subagent架构将任务派发到子代理中, 当前session自动成为superagent. 一个superagent下可以多次执行 /speckit.agents run命令来启动多个子代理."

**输入校正**：①「xxx」读作 agent 名，其后可接任务文本，即 `run <agent-name> [task]`；②「创建一个 run 子命令」读作**把既有 run 意图显式化为受模板、文档与检查器固定的子命令语法**——`run-agent` 技能已交付派发内核，superagent/subagent 角色模型已由 095 定义；本特性消除的是「已交付定义」与「用户可见的自动应用」之间的缺口，不是从零新建派发机制。

## Related Feature *(mandatory)*

**Feature ID**: 019
**Feature Name**: Agents Command
**Binding basis**: 019 owns the `/speckit.agents` command surface and the agent definition/execution layer（索引描述：Create, refine, and run layered agents with rendered host registrations）；019 的详情文件 Related Specifications 显示其已连续吸收同主题 spec（003 / 014 / 022 / 023）。候选扫描（2026-11-24）：019 `Implemented`（直接匹配）；095 `Ready for Review`（superagent 角色定义 owner——本特性按 A-2 只引用、不重定义，故不绑定）；057 `Implemented`（仅做命令路由核查，非命令面 owner）。按 Feature Binding Rules 的 bind 分支「匹配即绑定、不新建」：绑定 019，不创建新 Feature；019 状态保持 `Implemented`（no-status-regression gate），索引行与 019 详情文件的绑定义务同批履行。

## Overview

`/speckit.agents` 当前已是单代理操作的单一入口，`run` 意图在命令模板的意图表中存在并委派给 `run-agent` 技能；该技能已能解析定义、解析配置、以 native / virtual / external 三种模式派发**活的独立 Agent Execution**，注入快速失败子句，并在授予派发职责时注入 `role-transition`。superagent/subagent 的相对角色、七字段下行、五要素上行、深度与状态投影已由 095 在 `.specify/shared/definitions/superagent-definitions.md` 定义。也就是说，**派发内核与角色定义都已交付**。

但「用户执行 `/speckit.agents run xxx` 时自动应用该架构」仍有缺口：

1. **显式语法未固定**：命令模板没有 `argument-hint`，`run <agent-name> [task]` 只存在于意图表的一格文字里；命令参考文档没有 run 行，也没有语法块；无参行为在文档中仍被描述为「生成七个角色代理」，与当前模板（委派 run-agent 的列举/建议行为）矛盾。
2. **角色自动性未接线到派发面**：run-agent 的派发说明只要求快速失败注入与（授职时的）`role-transition`，没有要求携带 095 owner 已规定的**七字段下行**，也没有要求回传满足**五要素上行**；派发前的呈现只披露 agent 名与任务，不披露「本 session 是 superagent、子代 label、回传通道」。定义存在，运行面没有自动应用它。
3. **多次 run 的身份面缺失**：同一 Instance 可被执行多次，但 run-agent 没有规定每次派发的唯一子代 label、重试即新尝试、旧尝试产物保留；多子代的可见性没有指向既有载体（artifact triplet、状态摘要角色视图、运行记录）。
4. **边界条件含混**：SDD 授权探针（`sdd-route.py --action authorize`）的适用条件在技能文本中未写明「仅当载荷指派 SDD 驱动时」，普通 run 是否会被缺 team/seat 阻断不可判定。
5. **文档漂移**：`docs/reference/commands/agents.md` 实为三份全文串接的副本（三个一级标题），首份仍写「create and refine one agent」与「capabilities (create / refine)」；`docs/reference/agents/command-and-skills.md` 写「creates or refines one agent」与「two skills」；教程与总览面重复「无参生成七个角色代理」的陈旧陈述。

本特性把这五类缺口收敛为一次交付：显式 `run` 子命令 + 角色自动接线 + 多子代身份/可见性 + 边界澄清 + 文档同源校正。**不做什么**：不新建第二套派发机制、调度器、registry、存储或渲染器；不重定义 superagent（引用 095 owner）；不把 run 变成团队编排入口（那是 `/speckit.team`）；不改动 create / refine 的语义；不新增 glossary 词条。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **类别判定 = `execution`**：交付物是命令模板、技能文本、参考文档与契约测试，验收时由机器执行/解析/断言。 | 按验收 oracle 判定：缺陷只在契约测试、结构检查或派发演练中暴露，而非读者读错。 |
| **A-2** | **只补缺口，不重建**：以「已交付 vs 缺口」审计为前提（Overview 五条），FR 只覆盖缺口；既有派发内核、配置解析、可视化契约、角色定义保持原位，本特性对它们零修改或仅按指针引用。 | 095 / 064 / 060 已交付的能力不得被第二套实现覆盖；重复建造是 One Source of Truth 违约。 |
| **A-3** | **显式语法与自然语言意图并存**：`run <agent-name> [task]` 为受支持的显式子命令（模板 frontmatter `argument-hint` 固定其形态）；既有自然语言意图路由（含中文「运行代理」）保持不变；不新增 `run` 以外的动词别名。 | 与 `/speckit.team`、`/speckit.goal` 等多模式命令的 argument-hint 先例一致；显式化不牺牲既有可用性。 |
| **A-4** | **`run <name>` 缺任务时停止并征询**：呈现解析后的 agent（名、层、描述）并请求任务，**不派发空任务简报**，也不得落入无参列举行为。 | subagent 的定义属性是「有界任务简报」（`subagent-definitions.md` § What a Subagent Is）；空简报不是有界任务。 |
| **A-5** | **当前 session = superagent 是定义性的，不是开关**：095 owner 规定角色只由派发边决定；本特性不引入激活开关、角色实体或配置。自动应用 = 派发载荷携带 owner 的七字段与既有注入 + 回传满足五要素 + 呈现披露角色关系。 | 相对角色模型不得被实体化或第二次定义；把「自动」实现成开关会造出第二语义。 |
| **A-6** | **一次 run = 一条边 = 一个子代**：同一 superagent 下多次 run 产生多条独立边与多个子代，每次派发使用唯一 child label（派发尝试标识），重试是新尝试、旧产物保留；多次 run 的可见性只经既有载体（artifact triplet、状态摘要角色视图、运行记录），不新增清单/registry。 | 095 § Role Edges / § State Synchronization；重复调用天然支持，缺的是身份与可见性接线。 |
| **A-7** | **SDD 授权探针只在 SDD 指派时适用**：`sdd-route.py --action authorize` 的派发前探针只在载荷指派/点名 SDD 驱动时执行（收窄谓词的三条件，owner：`subagent-definitions.md` § Dispatch-Time Governance Obligation）；普通 run 指派不因缺 team/seat 被阻断。技能文本 MUST 写清该条件。 | 现状技能文本的「Dispatch only when…」未限定适用范围，普通 run 的可判定性因此受损；这是文本精度修复，不放宽任何 SDD 禁令。 |
| **A-8** | **文档同步面（含两处前提纠正）**：必须更新 `docs/reference/commands/agents.md` 与 `docs/reference/agents/command-and-skills.md`；同批校正 `docs/reference/agents/overview.md` / `design.md` 的能力单行、`docs/tutorials/installation.md` / `quickstart.md` 的命令表行与陈旧无参陈述。**P-1**：`docs/reference/commands/agents.md` 当前为三份副本串接（`^# /speckit.agents` 计数 = 3），MUST 合并为单副本。**P-2**：多处文档仍称无参执行「生成七个角色代理」，与当前模板（无参 → run-agent 列举/建议）矛盾，MUST 校正。`docs/reference/history/` 的 dated record 不改写。 | 根因修复纪律：编辑已知漂移所在文件时不把漂移留在原地；但 dated record 是历史，不属现役事实。 |
| **A-9** | **委派载体不变**：不新增技能；命令模板保持「只路由」；本特性编辑既有 `run-agent` 技能（及其 `references/` 如需）以完成接线。 | 单一职责拆分已成立（run-agent 持有 run 模式与无参行为）；新建技能会造出第二派发面。 |
| **A-10** | **不新增 glossary 词条**：`run` 是通用词；`Super Agent`（superagent）与 `Agent Execution`（子代理）均已登记；`role-transition` 等术语按 owner 引用。 | 词汇表只登记项目域术语；遵循 103 的 A-11 先例。 |
| **A-11** | **两顶帽子**：源面为 `templates/commands/agents.md`、`skills/internal/run-agent/**`、`docs/**`、`tests/**`；`.specify/**` 镜像与各工具命令副本由 `scripts/python/sync-mirrors.py` / `scripts/python/regen-command-copies.py` 再生成，不手改。 | 本仓为 framework source；手改镜像会在同步时丢失。 |
| **A-12** | **Feature 绑定留待 `/speckit.clarify`**（**已履行 2026-11-24**：绑定 Feature 019，见 `Related Feature` 与 clarify 会话）：`create-requirements` 不建 Feature。 | Feature Binding Rules 的 bind 分支在 clarify 执行；019 为候选，本阶段按 bind 分支裁决绑定并履行 registry 义务。 |
| **A-13** | **并发读数**：一次 run 只有一个可表示单元，按 `single-unit` 记录读数三元组（`requested` / `effective` / `effective_reason`）；用户多次调用 run 是多次独立命令运行，不是单一执行体内扇出；一次 run MUST NOT 扇出多个 agent。 | owner：`subagent-definitions.md` § The Concurrency Obligation、`serial-reason.yaml`；单次委派允许 native，单单元是具名事实。 |
| **A-14** | **行为类条款须自陈**：呈现披露、载荷内容、回传完整性、运行期 label 唯一性属行为类（无独立制品可观测面），MUST 声明为行为类并以真源文本 + 评审 + 变异演练取证；MUST NOT 声称被契约测试「覆盖」。制品类条款（模板字段、文档字面量、计数）由契约测试机械断言。 | 052 的制品类/行为类二分；把行为类当制品类断言是盲检。 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一条显式 run 命令把任务派发给子代理，当前 session 自动是 superagent (Priority: P1)

维护者手头有一个已定义的 agent（如 `sdd-debt-governor`），想让它在隔离上下文里完成一件有界任务。他输入 `/speckit.agents run sdd-debt-governor 审计 src/ 下的技术债并输出清单`。命令识别出显式 `run` 意图，委派 `run-agent`；技能解析到 instance（不存在则回退 template），先呈现：agent 名与层、任务、**「本 session 是该边的 superagent（根），子代 label 为 X，结果经回传通道 Y 返回」**，以及生效配置；随后派发一个独立执行。执行返回后，维护者看到结果或交付物路径、证据指针、显式异常行、并发读数与执行体身份。他不需要打开任何开关、写任何配置或声明「我是 superagent」——架构随派发边自动成立。

**Why this priority**: 这是用户原话的核心——显式 run 与架构的自动应用；没有它，其余都是附属。

**Independent Test**: 契约测试断言模板 `argument-hint`、意图表 run 行与技能输入契约三处语法一致；结构断言检查技能文本含七字段下行、五要素上行、呈现三要素与快速失败注入的指针；一次 run 演练（可执行路径存在时）检查返回含五要素且无缺项消费。

**Acceptance Scenarios**:

1. **Given** 一个存在于 `.specify/agents/instances/` 的 agent 定义，**When** 执行 `run <agent-name> <task>`，**Then** 命令路由到 run-agent，呈现包含 agent 名/层、任务、角色关系（本 session = superagent/根、child label、回传通道）与生效配置，随后派发一个独立执行；返回含五要素。
2. **Given** 同名定义同时存在于 instances 与 templates，**When** 执行 run，**Then** instance 胜出并被派发，呈现披露被遮蔽的 template 身份；不静默择一。
3. **Given** 用户未给出任务，**When** 执行 `run <agent-name>`，**Then** 呈现解析后的 agent 并请求任务，不派发空简报。
4. **Given** 用户只输入 `run` 而未给出 agent 名，**When** 命令处理输入，**Then** 输出 [[STR-003]]、能力清单与用法，不派发。

---

### User Story 2 - 同一 superagent 下多次 run 启动多个子代理，彼此可区分 (Priority: P1)

维护者先派发一个调研 agent，随后在同一个会话里再派发一个实现 agent。两次 run 各自产生独立执行与独立边；他能在既有状态面看到两个子代各自的 label、父边、角色、深度与状态，重试某一次不会覆盖上一次的产物，也不会把旧尝试的返回当成当前结果。

**Why this priority**: 用户明确要求「一个 superagent 下可以多次执行 run 来启动多个子代理」；没有唯一身份与可见性，多次 run 只能靠对话记忆。

**Independent Test**: 以同一 parent 身份与两个不同 child label 构造边记录夹具，运行只读角色判定引擎，断言两行子代、深度 1、无违例；以 label 重用/重试形态断言按新尝试处理且旧产物保留。

**Acceptance Scenarios**:

1. **Given** 同一 session 已派发过一个子代，**When** 再次执行 `run <另一个 agent> <task>`，**Then** 产生第二条独立边与新的 child label；两次派发的标签不相同。
2. **Given** 两个已完成的子代，**When** 读取既有状态摘要的角色视图，**Then** 父行加两行子代可见，各含父边、角色、深度与状态；截断时声明省略条数。
3. **Given** 对同一任务重试派发，**When** 新尝试开始，**Then** 使用新 label，旧尝试产物保留；旧尝试的迟到返回不被当作当前结果消费。

---

### User Story 3 - 边界与治理不越线：单代理、SDD 条件、零第二机制 (Priority: P2)

维护者需要确认 `/speckit.agents run` 仍然是**单代理**操作：它不会变成团队编排入口，不会新建第二套派发机制，也不会在普通派发时被 SDD 授权探针误伤；与 `/speckit.team` 的分工稳定可预期。

**Why this priority**: 安全边界与治理边界决定 run 能否被放心用于日常；越线会让两个命令的职责含混。

**Independent Test**: 路由样例集断言 run 不承接多代理/团队意图；结构审计断言无新增持久化根/registry/渲染器/调度器；文本契约断言 SDD 探针条件被限定，且反嵌套红线仍按指针存在。

**Acceptance Scenarios**:

1. **Given** 要求「并行运行三个 agent 并汇总」的输入，**When** 命令识别意图，**Then** 不被 run 承接，转 `/speckit.team` 或明确报告越界；run 一次只执行一个 agent 的一个任务。
2. **Given** 一个普通 run 指派（未点名任何 SDD 驱动），**When** 执行派发前检查，**Then** 不调用 SDD 授权探针、不因缺 team/seat 被阻断；SDD 指派仍按收窄谓词的既有禁令执行。
3. **Given** 本特性的变更集，**When** 做结构审计，**Then** 无新增持久化根、registry、第二渲染器、调度器或队列；派发复用既有 `run-agent`、`execution-config.py`、`dispatch.sh`、`exec-quant.py`。
4. **Given** 一次 run 运行，**When** 记录并发读数，**Then** 三元组齐全，单派发以 `single-unit` 具名；MUST NOT 以一个进程内的多次调用冒充并发。

---

### User Story 4 - 一个语法、一处真源：文档与发现性同步 (Priority: P2)

维护者从命令参考、agents 参考或教程学习 `/speckit.agents`。三处都给出同一套能力与语法：create / refine / run，显式 run 语法一致；`docs/reference/commands/agents.md` 只有一份正文，不再有三份串接副本，也不再声称「无参执行生成七个角色代理」或「capabilities (create / refine)」。

**Why this priority**: 发现性决定特性是否被用起来；文档矛盾会让用户对语法和默认行为失去信任。

**Independent Test**: 对命名文档做固定断言：顶层标题计数、run 语法出现、陈旧字面量计数为 0、三份参考面能力集一致；变异演练删除 run 行或复制出第二份正文时检查转红。

**Acceptance Scenarios**:

1. **Given** `docs/reference/commands/agents.md`，**When** 运行文档契约检查，**Then** `^# /speckit.agents` 计数为 1，Syntax 块含显式 run，意图表含 run 行，技能清单含三个技能，陈旧字面量出现数为 0。
2. **Given** `docs/reference/agents/command-and-skills.md` 与 `docs/reference/agents/overview.md`，**When** 检查能力枚举，**Then** 均包含 run（三能力），且 `run-agent` 作为第三技能被列出并指向其输出契约。
3. **Given** 教程命令表与无参说明，**When** 检查陈旧陈述，**Then** 「无参生成七个角色代理」一类陈述不再出现；命令表行包含 run。
4. **Given** 用户阅读命令参考的 Syntax 块，**When** 依样执行，**Then** 语法与模板 `argument-hint`、技能输入契约逐字一致。

---

### User Story 5 - 失败与半成品被诚实报告，不被当作成功 (Priority: P3)

维护者遇到各种失败：agent 不存在、定义损坏、配置解析失败、子代理失败或回传缺项。他要看到可行动的错误与部分结果，而不是静默成功、编造结果或用对话补全缺失字段。

**Why this priority**: 错误路径决定日常可用性与信任；价值低于主派发路径，但不可省略。

**Independent Test**: 逐条断言错误路径字面量与「不消费不完整返回」的结构/文本契约；对缺异常行的返回夹具断言判 incomplete。

**Acceptance Scenarios**:

1. **Given** 一个不存在的 agent 名，**When** 执行 run，**Then** 输出 [[STR-002]]、可用 agent 提示（有界，设上限须报省略数）与 create 建议，不派发。
2. **Given** 定义目录存在但 `.agent.md` 缺失或不可读，**When** 执行 run，**Then** 报告「定义损坏/不可读」并点名路径，不与「不存在」混同。
3. **Given** 配置解析失败，**When** 派发前检查运行，**Then** 停止派发并报告引擎的字段/支持集消息；不绕过解析器手工拼参数。
4. **Given** 子代理失败、超时或触达轮次上限，**When** 返回，**Then** 报告部分结果与失败原因，不隐藏失败。
5. **Given** 回传缺少五要素中的任一项（含显式异常行），**When** 父侧收到，**Then** 判 incomplete，不消费结论、不代填缺失字段。

### Edge Cases

- **`run` 携带团队参数**（如 `--target`）：报告「该参数属于 /speckit.team」并请求澄清，不静默丢弃、不把 run 改写成团队运行。
- **同一 agent 被连续 run 且前一个仍在运行**：允许；各自独立执行与 label；旧尝试的迟到返回按既有归因规则不消费。
- **双角色执行体调用 run**：它在父边仍是 subagent、在新边成为 superagent；上行职责不减，返回父边时仍须五要素回传。
- **virtual 模式（宿主无子代理能力）**：单次委派可 virtual 执行，但仍须呈现角色关系与完整回传；virtual MUST NOT 被当作并发载体，MUST NOT 承载 SDD 运行。
- **external 模式**：必须遵守既有可见性契约（stream-json + compact filter + `.live.log` / `.jsonl` / `.status` 三件套），不得把 print 输出重定向进静默日志。
- **无参 `/speckit.agents`**：保持既有列举 + 上下文建议 + 能力摘要（非破坏性），不得被显式 run 语法替换。
- **歧义输入**（既像 run 又像 create/refine）：报告三能力并请求意图，不静默执行任何模式。
- **根身份解析**：当前 session 在状态脊/line registry 下运行时取既有 `run_id` / `line_id`，否则取 owner 声明的根标记；不得发明第二套根身份。
- **回传缺并发读数三元组**：判 report-incomplete 并由父侧报告，父侧不得代填。
- **agent 名与任务文本中的引号/空格**：按 User Input / shell quoting 既有规则处理，不把任务文本当命令选项。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 显式子命令与路由

- **FR-001**: `/speckit.agents` MUST 支持显式 `run` 子命令，语法为 [[STR-001]]（`run <agent-name> [task]`）；命令模板 `templates/commands/agents.md` MUST 在 frontmatter 增加 `argument-hint` 固定该语法，MUST 保留意图表中的 run 行与三技能路径（run / create / refine），MUST 保持自然语言意图路由可用；MUST NOT 新增 `run` 之外的动词别名，MUST NOT 把团队能力并入本命令。
- **FR-002**: 路由 MUST 以显式动词优先于上下文推断：显式 `run` 意图 MUST 落到 `run-agent`；create / refine 意图 MUST NOT 落到 run；团队多代理意图 MUST NOT 落到 run（指向 `/speckit.team`）；空参数 MUST 保持既有「列举 + 上下文建议 + 能力摘要」无参行为；歧义的非空输入 MUST 报告三能力并请求意图，MUST NOT 静默选择任何模式。
- **FR-003**: 显式 `run` 未给出 agent 名时 MUST 输出 [[STR-003]]、三能力清单与用法，MUST NOT 从上下文推断 agent、MUST NOT 派发。
- **FR-004**: `run <agent-name>` 未给出任务时 MUST 呈现解析后的 agent（名、层、描述）并请求任务，输出 [[STR-004]]；MUST NOT 派发空任务简报，MUST NOT 落入无参列举行为。
- **FR-005**: agent 解析 MUST 按既有规则：`.specify/agents/instances/<name>.agent.md` 优先、回退 `.specify/agents/templates/<name>.agent.md`（instance 胜出），存在 `.specify/agents/execution/configs/<name>.yaml` 时应用；呈现 MUST 披露解析层与被遮蔽的同胞定义。未找到 MUST 输出 [[STR-002]]、有界的可用项提示与 create 建议；定义目录存在而 `.agent.md` 缺失/不可读 MUST 报告「定义损坏/不可读」并点名路径，MUST NOT 与「不存在」混同。

#### B. superagent/subagent 架构的自动应用

- **FR-006**: 每次 run 派发 MUST 按 095 owner 的相对角色模型构成一条 `superagent → subagent` 边：当前持有用户会话的执行体是根（深度 0）即该边的 superagent，被派发执行是 subagent；角色 MUST 只由边决定，MUST NOT 由执行体类型、提示词、模型或自述分类。本特性 MUST NOT 引入激活开关、角色实体、第四层分类或第二份角色定义。
- **FR-007**: 派发前呈现 MUST 为**披露而非阻断门禁**，且至少含：① 解析后的 agent 身份（名、层、描述）与任务简报；② 角色关系——本 session 为该边 superagent（根），子代 child label，结果回传通道；③ 生效配置的既有披露项（`config_id`、`mode`、`cli`、有效 `model` / `reasoning_effort` / `context_window`、`source_chain`、`skipped_layers`、`quantification`、`requires_external`）。呈现 MUST 以指针指向角色与协议 owner，MUST NOT 复述其规则文本。用户可在派发前叫停。
- **FR-008**: 派发载荷 MUST 物理携带：① 七字段下行（字段集与语义 owner：`.specify/shared/definitions/superagent-definitions.md` § The super↔sub Protocol，本规格不复述字段表）；② 既有四项注入（快速失败子句、并发义务、汇报义务、re-anchoring 锚摘要）按各自 owner 以指针携带；③ 当派发授予派发职责（`dispatch_duty: granted`）时，`role-transition` 稳定标识与九项指针清单。载荷 MUST NOT 指示子代加载任何技能、MUST NOT 点名任何驱动技能、MUST NOT 含循环逻辑（反嵌套，owner 按 `subagent-definitions.md` § Dispatch-Time Governance Obligation）。
- **FR-009**: 派发前自检 MUST 在既有形态上扩展为逐项判定：`role-transition` 标识与九个 item-id slug 逐项在场（授职派发时），以及七字段下行逐项在场；缺标识或缺任一 slug/字段 MUST 作为载荷构造缺陷在派发前阻断，MUST NOT 进入派发。
- **FR-010**: 每个回传 MUST 满足 owner 的五要素上行（结果或交付物路径、证据指针、显式异常行、并发读数三元组、返回执行体身份）；缺任一项即 incomplete，父侧 MUST NOT 消费其结论、MUST NOT 代填缺失字段；无异常时 MUST 显式写「未发现异常」。
- **FR-011**: 每次 run 派发 MUST 使用唯一 child label（派发尝试标识）；同一 superagent 下多次 run MUST 产生互不相同的 label；重试 MUST 是新尝试并保留旧尝试产物；旧尝试的迟到返回 MUST NOT 被当作当前结果消费（归因规则按既有 watch model owner）。child label MUST 复用既有 dispatch label 约定——`dispatch.sh <label>` 的 label 原样作为该次派发的 `run_id` 交给 `exec-quant.py --action collect-dispatch --run-id <label>`，external artifact triplet 以 `<label>.live.log` / `.jsonl` / `.status` 命名；MUST NOT 新增 label 生成器、子代清单或 registry。
- **FR-012**: 多子代 MUST 仅经既有载体可见：external 派发的 artifact triplet（`.live.log` / `.jsonl` / `.status`）与 `exec-quant` 记录、状态摘要的角色视图（`parent` / `roles` / `role_set_marker` / `depth`）与运行记录；本特性 MUST NOT 新增子代清单、registry、第二渲染器或第二状态存储。
- **FR-013**: 同一 Instance 可被多次执行（顺序或并发），每次执行 MUST 与定义及其它执行隔离；run MUST NOT 修改 agent 定义、MUST NOT 跨执行共享可变状态。

#### C. 边界与治理

- **FR-014**: run MUST 保持**单代理**语义：一次 run 执行一个 agent 的一个有界任务；多代理编排（并行 / 串行链 / 迭代 / 持续循环）MUST NOT 由 run 承接，MUST 指向 `/speckit.team`；create / refine 的语义与写权 MUST 保持不变。
- **FR-015**: 本特性 MUST 复用既有机制：`run-agent` 技能、`execution-config.py` 配置解析、`dispatch.sh` 外部派发载体、`exec-quant.py` 量化收集、`role-edge-check.py` 角色判定、`status-digest.py` 角色视图；MUST NOT 新增调度器、队列、传输、通知通道、持久化根或第二派发机制。
- **FR-016**: SDD 授权探针（`sdd-route.py --action authorize`）MUST 只在派发载荷指派/点名 SDD 驱动时执行，条件按 `subagent-definitions.md` § Dispatch-Time Governance Obligation 的收窄谓词；普通 run 指派 MUST NOT 因缺 team/seat 被阻断。run-agent 技能文本 MUST 显式写出该适用条件；拒绝时 MUST 点名失败的一半（agent / seat / both）、来源路径与 seat slug（既有形态）。
- **FR-017**: 每次 run 运行 MUST 记录并发读数三元组（`requested` / `effective` / `effective_reason`）；单派发 MUST 以 `single-unit` 具名；无区间时 `effective` 取 `not_evaluated` 字面量，MUST NOT 记 0 或估算值。用户多次调用 run 是多次独立命令运行，MUST NOT 被宣称为单执行体内并发；一次 run MUST NOT 扇出多个 agent。

#### D. 文档与发现性

- **FR-018**: `docs/reference/commands/agents.md` MUST 合并为**单份正文**（前提纠正 P-1：当前 `^# /speckit.agents` 计数为 3），并同步：描述行从 [[STR-006]] 更正为三能力；Syntax 块加入显式 run；意图表加入 run 行；技能清单列出 run / create / refine 三技能；无参行为更正为列举 + 建议（删除 [[STR-008]] 一类「无参生成七个角色代理」的陈述）；`capabilities (create / refine)`（[[STR-005]]）不再出现。
- **FR-019**: `docs/reference/agents/command-and-skills.md` MUST 同步为三能力：描述句不再写「creates or refines one agent」一类只含两能力的陈述；意图路由表加入 run 行；路由流覆盖 run；单代理技能清单由两个扩为三个，并为 `run-agent` 增加一节（解析 → 呈现 → 派发 → external 收集 → 报告，按指针引用其输出契约，不复制规则）。
- **FR-020**: 同批同步其余能力枚举面（2026-11-24 扫描固定的封闭清单：`docs/reference/agents/overview.md`、`docs/reference/agents/design.md`、`docs/tutorials/installation.md`、`docs/tutorials/quickstart.md`）：overview / design 的能力陈述 MUST 含 run，且技能计数陈述（如 overview 的「两个单 Agent 技能」）MUST 更新为三技能；installation / quickstart 的命令表行 MUST 含 run，且其中的陈旧无参陈述（[[STR-007]] 及同句式变体）MUST 被更正为与当前模板一致；`docs/reference/history/` 的 dated record MUST NOT 被改写。README 当前无 `/speckit.agents` 能力枚举行（2026-11-24 扫描 0 命中），不在本清单；若 plan 阶段扫描发现新增枚举面，MUST 先把其路径并入本 FR 的清单并同步 SC-005 允许集，再编辑。
- **FR-021**: 本特性 MUST NOT 新增 glossary 词条；`Super Agent`、`Agent Execution`、`role-transition` 等术语 MUST 按既有词条与 owner 引用，MUST NOT 新造同义词或为 `run` 建立项目域定义。

#### E. 质量与测试

- **FR-022**: 契约测试 MUST 机械固定：① 模板 frontmatter `argument-hint`、意图表 run 行与三技能路径；② 技能文本含七字段下行、五要素上行、呈现三要素、label 唯一性、SDD 探针适用条件与快速失败注入的**指针**（不得复制 owner 规则文本）；③ 命名文档的单副本计数、run 出现与陈旧字面量计数为 0；④ 无新增持久化根/registry/渲染器；⑤ 变更源面与其运行时镜像字节一致（重生成后）。既有守卫（`test_run_skills_wiring.py` C-11、`test_team_command_routing.py` M6、`test_role_transition_payload.py`、`test_fast_fail_discipline.py` 的 agents 面）MUST 相对 implement 入口的名字级失败基线不得新增失败；基线既有红 MUST 逐条点名（相对判据，不要求「全绿」）。
- **FR-023**: 行为类条款（FR-007 呈现披露、FR-008 载荷内容、FR-010 回传完整性、FR-011 运行期 label 唯一性、FR-016 探针条件的执行、FR-017 读数记录）MUST 在 plan / contracts 中被逐条标注为行为类，并以真源文本 + 评审 + 变异演练取证；MUST NOT 声称其由契约测试「覆盖」。制品类条款（FR-001 / FR-003 / FR-004 / FR-018 / FR-019 / FR-020 / FR-022）由契约测试机械断言。
- **FR-024**: 新增测试 MUST 经唯一入口 `scripts/bash/run-tests.sh` 一次执行并退出 0；既有相关测试 MUST 相对 implement 入口的名字级失败基线零新增失败（基线既有红逐条点名，不声称全绿）；MUST NOT 直接调用解释器级测试命令。

### Key Entities *(include if requirement involves data)*

- **Agent Definition（Agent Template / Agent Instance）**: 被解析并派发的定义，位于 `.specify/agents/{instances,templates}/<name>.agent.md`；三层分类法与字段语义 owner 是 `shared/definitions/agent-definitions.md`，本特性只消费。
- **Agent Execution**: 一次 run 产生的运行形态；三种执行模式与可见性契约 owner 是 `shared/definitions/subagent-definitions.md`，本特性不新增执行层实体。
- **Role Edge**: 一次派发产生的 `parent → child` 关系；是既有载体的投影（owner：`superagent-definitions.md` § Role Edges），不是新存储；本特性只为 run 派发补齐七字段下行与身份解析。
- **Child Label（派发尝试标识）**: 子代在既有派发 label 约定下的身份，用于区分同一 superagent 的多个子代与重试；具体形态 = `dispatch.sh <label>` 的 label（原样作为派发 `run_id` 与 artifact triplet 前缀；owner：`skills/internal/run-agent/SKILL.md` / `exec-quant.py --action collect-dispatch`），不是新实体，不新增生成器或清单。
- **Return Record**: 子代回传，承载五要素上行；owner 是 `superagent-definitions.md` § The super↔sub Protocol。
- 本特性不新增数据实体、持久化根或 registry；以上实体均为既有载体的读取或投影。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时依赖、不新增第三方包——它交付命令模板、技能文本、参考文档与测试，并消费既有 Python 解释器、pytest 运行器、唯一测试入口、既有派发运行时与只读角色判定引擎。每行可机械判定。表中 `Premises` 引用的 `EP-NNN` 由 plan 阶段 `## Execution Premises` 定义（本阶段不建 premises 表）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库（契约测试的文本解析、fixture 构造与文件计数） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 既有 `requires-python`；本特性零新增第三方依赖 | `pyproject.toml` | 新增测试在 `>=3.8` 解释器上经唯一入口通过；本特性新增第三方 import 为零 | FR-022, FR-024 | EP-001 |
| RS-002 | `pytest` 测试运行器（契约 / 结构 / 文档测试） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 既有 pytest 声明；零新增依赖 | `pyproject.toml` | `scripts/bash/run-tests.sh` 运行新增测试，相对入口基线零新增名字级失败 | FR-022, FR-024 | EP-001 |
| RS-003 | POSIX `bash` 运行时（唯一测试入口 `scripts/bash/run-tests.sh`） | signed-contract | bash 上游 / 运行环境（本仓只消费） | 不新增显式版本下限；本特性不改动该入口 | `scripts/bash/run-tests.sh` | 新增测试全部经该入口执行且一次退出 0 | FR-024 | EP-001 |
| RS-004 | 既有只读角色判定引擎（边、角色集、深度与四类违例） | signed-contract | 既有 095 交付引擎（本特性只读消费，零修改） | 仓内既有实现；pin 由 `--help` 声明的动作集固定 | `scripts/python/role-edge-check.py` | 以同一 parent + 两个 child label 的夹具运行，报告两条边、深度 1、无违例 | FR-012, FR-022 | EP-002 |
| RS-005 | 既有配置解析引擎（`resolve` / 快照 / `config_id`） | signed-contract | 既有 061 交付引擎（只读消费，零修改） | 仓内既有实现；字段与能力矩阵 owner 在引擎内 | `scripts/python/execution-config.py` | run 前置解析成功时呈现 `config_id` 与有效配置；失败停止派发 | FR-007 | EP-002 |
| RS-006 | 既有外部派发载体（可见性契约与 artifact triplet） | signed-contract | 既有 create-team 交付脚本（只读消费，零修改） | 仓内既有实现；契约 owner 在 `subagent-definitions.md` § External Dispatch Visibility Contract | `skills/internal/create-team/scripts/dispatch.sh` | external 派发产出三件套；静默重定向形态被拒绝 | FR-012 | EP-002 |
| RS-007 | 既有派发量化收集（`collect-dispatch`） | signed-contract | 既有 059 / 061 交付引擎（只读消费，零修改） | 仓内既有实现；记录 schema owner 在引擎内 | `scripts/python/exec-quant.py` | external 派发后收集成功；失败仅报告、不改变派发结果 | FR-012 | EP-002 |
| RS-008 | 本特性的派发编排面（run-agent 技能的 run 模式增量：语法、呈现、载荷、回传、label、边界） | in-scope | 本特性自身修改的 framework 源技能 | 不适用（无外部版本面） | `skills/internal/run-agent/SKILL.md` | 结构契约断言所需指针与条款在位；变异演练删项时检查转红 | FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-016, FR-017 | EP-003 |

**Contract-cell note**: 每个 `Contract` 单元格只放一个仓内可解析路径；`RS-008` 指向本特性修改的交付面 `skills/internal/run-agent/SKILL.md`，不是第二契约。`RS-004`–`RS-007` 的既有引擎与脚本在本特性中零修改，义务只在其既有契约上被消费与断言。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 显式 run 语法在三个面（模板 `argument-hint` [[STR-001]]、run-agent 输入契约、命令参考 Syntax）逐字一致；路由样例集（显式 run ≥2 条、create、refine、团队、空参数、歧义）逐条命中预期，错误路由数为 0；不存在 agent（[[STR-002]]）、缺 agent 名（[[STR-003]]）、缺任务（[[STR-004]]）三条路径各按契约停止且派发数为 0 **Path**: final
- **SC-002**: 同一 parent 下两次 run 产生两条独立边：以同一父身份与两个不同 child label 的夹具运行只读角色判定引擎，报告 2 条子代边、深度 1、无违例；label 重用/重试按新尝试处理、旧产物保留、迟到返回不被消费；把两次派发压成同一 label 或消费旧返回时测试转红 **Path**: final
- **SC-003**: 派发面接线契约在位：技能文本含七字段下行、五要素上行、呈现三要素、label 唯一性、SDD 探针适用条件、快速失败注入与反嵌套红线的指针；删除任一项时对应契约检查转红；既有守卫 `test_run_skills_wiring.py` C-11、`test_team_command_routing.py` M6、`test_role_transition_payload.py`、`test_fast_fail_discipline.py` 的 agents 面相对 implement 入口基线零新增名字级失败（基线既有红逐条点名） **Path**: supporting
- **SC-004**: 文档同源：`docs/reference/commands/agents.md` 的 `^# /speckit.agents` 计数 = 1（改前 3）；run 语法与 run 意图行在该文件出现；[[STR-005]] / [[STR-006]] / [[STR-007]] / [[STR-008]] 在命名文件中的实时出现数为 0；`docs/reference/agents/command-and-skills.md` 的能力集为三项且含 `run-agent` 小节；overview / design 的能力单行与教程命令表行含 run **Path**: supporting
- **SC-005**: 零第二机制与变更集包含性：基线参照物 = implement 阶段提交的父提交；比较单元 = `git diff <base>..HEAD --name-status` 的路径集，按产物类分组（命令模板 / 技能 / 文档 / 测试 / 再生成的镜像与工具命令副本）；允许差异集由被编辑源面的扇出闭包机械导出并由测试逐类断言（`templates/commands/agents.md`、`skills/internal/run-agent/**`、FR-018 / FR-019 / FR-020 点名的文档、`tests/**`，以及 `sync-mirrors.py` / `regen-command-copies.py` 的再生成产物）；补集侧断言该区间不出现上列之外的路径；集合内断言无新增持久化根 / registry / 渲染器 / 调度器；镜像与源逐字节一致 **Path**: supporting
- **SC-006**: 变异演练 4/4：删除 `argument-hint` → 模板契约转红；删除 run 意图行 → 模板契约转红；删除七字段下行指针 → 技能契约转红；复制出第二份命令参考正文 → 文档契约转红；逐项复原后转绿；演练读数记录到 `test-evidence/` **Path**: supporting
- **SC-007**: 新增测试经 `scripts/bash/run-tests.sh` 一次执行退出 0；既有相关测试相对 implement 入口的名字级失败基线零新增失败；基线既有红逐条点名、不声称全绿 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 路由样例集契约测试的逐条通过计数与失败明细，加上三面语法断言（模板 frontmatter 解析、技能文本匹配、命令参考 Syntax 块）的断言输出。
- **SC-002 Source**: 边记录夹具上 `role-edge-check.py` 的报告输出（边数、深度、违例集），加上 label 重用/重试变异实测；读数记录到 `test-evidence/`。
- **SC-003 Source**: 契约测试的逐项断言输出与删项后的转红实测；既有守卫的同一批次执行结果。
- **SC-004 Source**: 文档契约测试的计数输出（标题计数、字面量计数、能力集断言）。
- **SC-005 Source**: 变更集结构审计（新增持久化根/registry/渲染器/调度器计数）、被编辑源面的扇出闭包逐类枚举断言与 `sync-mirrors.py --check` 读数。
- **SC-006 Source**: 变异演练逐项的红/绿实测记录，落在 `test-evidence/`。
- **SC-007 Source**: `scripts/bash/run-tests.sh` 的退出码、测试汇总与名字级失败基线差分。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"[create|refine|run] [agent-name] [task]"` | FR-001, SC-001 |
| `STR-002` | `"agent not found"` | FR-005, SC-001 |
| `STR-003` | `"missing agent name"` | FR-003, SC-001 |
| `STR-004` | `"missing task"` | FR-004, SC-001 |
| `STR-005` | `"capabilities (create / refine)"` | FR-018, SC-004 |
| `STR-006` | `"create and refine one agent"` | FR-018, SC-004 |
| `STR-007` | `"Generate role-based agents or create custom agents"` | FR-020, SC-004 |
| `STR-008` | `"generates the seven role-based workflow agents"` | FR-018, SC-004 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-11-24（无人值守 requirements 阶段，自行裁决并记录）

- 本阶段不发起阻塞式提问；候选问题按「Recommended」自裁决并逐条写回对应节（A-3 / A-4 / A-5 / A-6 / A-7 / A-8 / FR-016 / FR-020 / Edge Cases），无遗留 `[NEEDS CLARIFICATION]`。
- Q: `run xxx` 是新建派发能力，还是显式化既有 run 意图？ → A: **显式化并接线**。`run-agent` 已交付派发内核，095 已定义角色模型；本特性只补显式语法、七字段下行/五要素上行的运行面接线、多子代身份、文档同源与检查器（概览五缺口）。
- Q: `run <name>` 缺任务时怎么办？ → A: 呈现解析后的 agent 并请求任务（输出 [[STR-004]]），不派发空简报（A-4）。
- Q: 文档三副本与陈旧无参陈述如何处理？ → A: 同一变更合并为单副本并校正（P-1 / P-2，FR-018 / FR-020）；`docs/reference/history/` 的 dated record 不改写。
- Q: SDD 授权探针是否阻断普通 run？ → A: 否；探针只在载荷指派/点名 SDD 驱动时适用，普通 run 不因缺 team/seat 被阻断（A-7 / FR-016）。
- Q: 是否新增 glossary 词条？ → A: 否；`Super Agent` / `Agent Execution` 已登记，按既有词条与 owner 引用（A-10 / FR-021）。
- 同作者检测门：本 `requirements.md` 由本阶段单一执行体自撰；后续 `/speckit.analyze` / 评审若在同一会话内分析本文件，须按 `.specify/shared/workflow/objective-analysis-gate.md` 委派 fresh-context 只读子代理。

### Session 2026-11-24（无人值守 clarify 阶段，自行裁决并记录）

- Q: 本特性绑定哪个 Feature？ → A: 绑定既有 **Feature 019（Agents Command）**。候选证据：019 `Implemented`（"Create, refine, and run layered agents with rendered host registrations"，直接拥有 `/speckit.agents` 命令面）；095 `Ready for Review` 是 superagent 角色定义 owner，本特性按 A-2 只引用不重定义，不绑定；057 `Implemented` 仅做路由核查。019 详情显示其已吸收 003 / 014 / 022 / 023 等同主题 spec（binding-precedent heuristic 成立）。按 bind 分支「匹配即绑定、不新建」，不创建新 Feature。
- Q: 「child label（派发尝试标识）」采用什么既有约定？ → A: 复用既有 dispatch label 约定：`dispatch.sh <label>` 的 label 原样作为该次派发的 `run_id`（owner：`skills/internal/run-agent/SKILL.md`），并交给 `exec-quant.py --action collect-dispatch --run-id <label>`；external artifact triplet 以 `<label>.live.log` / `.jsonl` / `.status` 命名。唯一性由「每次 run 生成新 label、重试即新 label」保证；MUST NOT 新增 label 生成器、子代清单或 registry。写回 FR-011 与 Key Entities 的 Child Label 行。
- Q: FR-020 的「实现若发现其它能力枚举面」条件句如何可判定？ → A: 以 2026-11-24 仓库扫描固定封闭清单：`docs/reference/agents/overview.md`、`docs/reference/agents/design.md`、`docs/tutorials/installation.md`、`docs/tutorials/quickstart.md`（均在 FR-018 / FR-019 之外）；README 扫描 0 命中，不列入。overview / design 的**技能计数陈述**（如「两个单 Agent 技能」）一并纳入 MUST 更新为三技能。若 plan 阶段扫描发现新增枚举面，MUST 先把路径并入 FR-020 清单并同步 SC-005 允许集再编辑（closed-set-claims：封闭集须可判定）。写回 FR-020。
- Q: Feature Registry 的绑定机械义务如何履行？ → A: 019 状态保持 `Implemented` 不回退（clarify 无状态迁移权；no-status-regression）；同批更新索引行：Spec Path → `.specify/specs/104-agents-run/requirements.md`、Last Updated 跟随绑定注记；019 详情文件 Related Specifications 增列本 spec 并记录绑定理由、Last Updated 改为 2026-11-24；`Total Features` 与行数不变（不新增行）。A-12 标记为已履行。
- 同作者检测门：本阶段执行体与 requirements 作者不是同一会话（requirements 由上一阶段独立执行体自撰），门未触发，未委派 fresh-context 检测子代理；本次覆盖扫描由本执行体直接完成，关键前提（H1 计数 = 3、陈旧字面量命中文件、README 0 命中、argument-hint 现状）均以仓库检索当场取证。
