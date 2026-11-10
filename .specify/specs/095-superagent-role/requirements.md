# Requirements Specification: super agent 作为相对逻辑角色（定义、协议与 harness 落点）

**Requirement Branch**: `095-superagent-role`
**Created**: 2026-11-10
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（修订 agent / subagent / team / driver 定义与派发面的作者）、下游项目的维护者（在 team、无人值守 SDD 或跨主机驱动中运行、观察与调试 super agent 关系的人）——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 在判定「两个执行体之间是否存在父子边、各自是什么角色、深度多少」「一个 subagent 何时可以在其派发载荷里获得 superagent 职责」「并发、状态同步、状态跟踪与可视化分别归哪个既有 owner」时打开本规格，据 FR-001…FR-038 与 SC-001…SC-010 决定 `/speckit.clarify` 与后续实现是否放行
**Input**: User description: "需要在 Spec Kit 框架中正式引入 super agent 的概念。此前在 team / subagent 的各种特性中，事实上已存在一个 super agent 概念——使用 super agent（当前与用户交互的 session）控制各个 subagent——但没有规范化的定义和架构。通过 sdd-loop-driver 技能进行无人值守开发。在 speckit 中正式引入这个 super agent 的定义，补全明确的结构和流程说明，并在整体 harness 配置中落实。核心约束：super agent 是相对的逻辑概念，不是实体物理概念。三个真实场景（作为定义输入）：1) 桌面端 Qoder 通过 SSH 连接远端服务器执行 qodercli 命令启动 agent 进行开发：桌面端 Qoder = super agent，远端启动的 qodercli = subagent。2) 本地 qodercli 运行一个 team 流程，控制大量 subagent 分工合作：本地 qodercli = super agent，team 中被拉起的 agent = subagent。3) team 中的 agent 需要分析一个大规模代码库，并发启动 10 个 subagent 分工，最后由它自己汇总：该 team agent = super agent（同时它仍是 team 的 subagent）。以这些例子为输入，定义 super agent 与 subagent 之间的协议，以及身份转变时需要注入的上下文或 harness（如一个单纯的 subagent 变成兼具 subagent 和 superagent 两种身份）。需要考虑：并发、状态同步、状态跟踪、可视化显示。本运行同时用于验证 080–094 各 spec 机制的实际效果。"

## Related Feature *(mandatory)*

**Feature ID**: Need clarification
**Feature Name**: Need clarification

## Overview

框架里 super agent 事实上早已存在：当前与用户交互的 session 控制各 subagent，`/speckit.team` 的协调会话、`sdd-loop-driver` 的驱动者、`run-agent` 的派发者都是它。但它只以「主 session / 编排者 / supervisor / driver / 派发方」等分散措辞出现：没有归一化的定义，没有 super↔sub 协议，没有「一个 subagent 转为兼有 superagent 身份时注入什么」的清单，也没有把并发、状态同步、状态跟踪与可视化接到同一张关系模型上。后果是：同一执行体在一条边上是 subagent、在另一条边上是 superagent 的事实只能靠人读对话识别；派发载荷只治理子端（快速失败、并发义务、汇报义务、re-anchoring），不声明父端身份与角色；运行记录能回答「有哪些 agent 在跑」，不能回答「它们谁是谁的上级、深度多少、谁是双重角色」。

本特性把这件事一次定义清楚，并用三个真实形态验收：桌面端 Qoder 经 SSH 驱动远端 qodercli、本地 qodercli 编排一个 team、team 成员再并发扇出 10 个 subagent 并自行汇总。核心约束是**相对性**：super agent 是派发边上的逻辑角色，不是实体类型；同一个执行体在不同边上可以同时是 subagent 与 superagent。

交付物是「定义 + 协议 + 身份转变注入清单 + 既有载体的投影接线」，不是新运行时：并发仍归既有并发义务与事实，状态仍归状态脊 / line registry / artifact triplet / run report，汇报仍归 reporting obligations，授权仍归 `sdd-route.py` 与 team territory，可视化仍归 `status-digest.py`。本特性的运行同时作为 080–094 机制实际效果的观测（收尾附录，FR-038）。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 相对角色与角色边可判定 (Priority: P1)

一个维护者把任意两个执行体交给框架，能得到四个答案：二者之间是否存在派发边；在每条边上谁是 super agent、谁是 subagent；每个执行体的角色集（含同时兼具两者的情形）与深度；以及违例（自派发、悬空父、没有任何边却声称 superagent 角色）。答案只来自既有运行记录，不来自阅读对话或猜测。

**Why this priority**: 相对性是本特性的定义约束。如果角色不能被判定，场景 3 的「同时是两者」就无法验收，「super agent」也会退化为另一个实体类型。

**Independent Test**: 构造 root→A、A→B 两条边的夹具，运行只读判定面，断言角色集、方向与深度；把判定改为按执行体类型分类时该测试转红。

**Acceptance Scenarios**:

1. **Given** root 派发 A，且 A 派发 B，**When** 查询角色与边，**Then** A 在 root→A 上是 subagent、在 A→B 上是 superagent，B 是 subagent，root 不是任何边的 subagent，A 深度为 1、B 深度为 2。
2. **Given** 同一执行体同时处于父边与子边，**When** 输出其角色集，**Then** 同时列出 subagent 与 superagent（[[STR-002]]），而不是二选一或按实体归类。
3. **Given** 自派发边、父身份悬空、或没有任何边却声称 superagent，**When** 判定面运行，**Then** 三类违例各自被点名并返回非零。

---

### User Story 2 - 身份转变：team 成员并发扇出 10 个 subagent 并自行汇总 (Priority: P1)

一个 team 成员先作为 subagent 被父会话派发；在它需要分析大规模代码库时，父派发授予它派发自己子执行体的权利。它随即并发启动 10 个 subagent 分工，自己仍是父边的 subagent，同时成为 10 条子边的 superagent；子项完成后由它汇总成一次向上返回。

**Why this priority**: 这是用户点名的第三个真实场景，也是「身份转变时要注入什么」的唯一入口；缺少它，super agent 只剩与被派发者相同的单层关系。

**Independent Test**: 派发夹具——父派发一个成员并授予派发权；断言载荷携带 [[STR-003]] 的九项内容；成员扇出 10 个独立子项；断言每子一条边、容量预留先于派发、聚合返回逐子归属；删去注入的任一项时派发前自检阻断。

**Acceptance Scenarios**:

1. **Given** 父派发一个 subagent 并授予其派发权，**When** 该 subagent 收到载荷，**Then** 载荷含身份转变注入（[[STR-003]]）：superagent 角色激活与范围、自身身份与父边、必须向下注入的义务清单、并发预算引用、汇报路径、状态载体与写者边界、注意力分类、深度剩余与禁止项、聚合回传契约，全部按指针承载。
2. **Given** 该执行体扇出 10 个互不依赖的子项，**When** 做出派发决策，**Then** 默认并发生效、容量预留先于派发、父记录读数三元组、嵌套不放大容量；只有携带具名理由码时才允许串行。
3. **Given** 子项完成或失败，**When** 该执行体返回父边，**Then** 一次结构化返回逐子归属、携带每子证据路径、不隐藏失败与异常；它作为 subagent 的回传契约（含显式异常行）保持完整。

---

### User Story 3 - 两个既有真实形态：本地 team 编排与跨主机 SSH 驱动 (Priority: P1)

本地 qodercli 运行一个 team 流程时，qodercli 是 super agent、被拉起的 team 成员是 subagent；桌面端 Qoder 通过 SSH 连接远端服务器执行 qodercli 命令时，桌面端是 super agent、远端执行是 subagent。两种形态使用同一套角色、协议与记录，不需要两套解释。

**Why this priority**: 前两个真实场景是本特性的定义输入；只覆盖嵌套扇出而不覆盖这两个形态，定义就只对一种拓扑成立。

**Independent Test**: 两个夹具——本地 team 夹具与远端拓扑夹具（按既有 external-dispatch recipes 形态记录，不要求在测试套件内真实铺设 SSH 主机）；断言边与角色被记录、协议字段齐全、远端产物落在目标项目、桌面侧能消费返回与 liveness。

**Acceptance Scenarios**:

1. **Given** 本地 qodercli 运行一个 team，**When** 各席位被派发，**Then** qodercli 是根（super agent），每个成员是 subagent；逐席位边出现在运行报告的派发映射表与各自 artifact triplet 中，并被状态视图投影。
2. **Given** 桌面端 Qoder 经 SSH 驱动远端 qodercli，**When** 远端执行运行，**Then** root→远端执行这条边按远端拓扑声明记录；远端产物与快照落在目标项目；桌面侧消费结构化返回与 liveness，而不依赖读取远端对话正文。
3. **Given** 某个 team 成员自身又被授予派发权（场景 3 的嵌套），**When** 从根观察，**Then** 深度 2 的边与双重角色同时可见；既有 SDD 治理（深度 2 许可链、每成员一运行、virtual 不得承载）保持不变。

---

### User Story 4 - 状态同步、状态跟踪与可视化 (Priority: P2)

用户随时能看到每条活动执行体的身份、父边、角色、深度、状态、最近活动与距今时长，并知道哪些条目已过期；中断恢复后看到的是真实状态，而不是被静默当作仍在运行或已完成。

**Why this priority**: 用户点名要求考虑状态同步、状态跟踪与可视化；没有这条，角色模型只能写不能看，恢复也只能靠猜。

**Independent Test**: 用既有载体造出活动边与中断边，运行既有 digest 并做恢复；断言字段、截断声明、`nothing-running`、stale 标记与 interrupted/attention 结果。

**Acceptance Scenarios**:

1. **Given** 存在活动边，**When** 运行既有 on-demand digest，**Then** 每条执行体显示身份、父边身份、角色集、深度、状态、最近活动与距今时长、stale 标记；截断时声明被省略条数。
2. **Given** 没有任何活动工作，**When** 运行 digest，**Then** 渲染既有 `nothing-running` 状态，而不是一份空摘要或空集。
3. **Given** 一个父执行体在子项运行中被中断，**When** 执行恢复，**Then** 仍被判定在跑的子项标记为 interrupted/attention；stale attempt 的回传不被消费；恢复动作在动作前重验证授权。

---

### User Story 5 - harness 落点与零第二机制 (Priority: P2)

维护者在定义 owner、既有分类法、项目指令模板与派发面中都能找到同一份模型，全部以指针引用；项目指令体积仍在预算内，且框架里没有多出第二套并发机制、registry、状态存储或报告体系。

**Why this priority**: 用户要求「在整体 harness 配置中落实」，同时简报明确禁止第二套机制；落实与不重复必须同时成立。

**Independent Test**: 生成器预算报告 + owner 指针存在性断言 + 变更集结构审计 + 080–094 观测附录检查。

**Acceptance Scenarios**:

1. **Given** 新增的定义 owner 文档，**When** 读取既有分类法与目录地图，**Then** 它们只含指向 owner 的指针行；指令模板新增段为指针形态，生成的指令文件体积在预算之内。
2. **Given** 本特性的变更集，**When** 做结构审计，**Then** 无新增持久化根、registry 或报告渲染器；判定面只读；并发、汇报与授权的 owner 规则文本未被复制。
3. **Given** 080–094 中本仓实际存在的切片，**When** 收尾产出观测附录，**Then** 每切片逐条记录 `exercised`（带可解析证据路径）或 `not-observed`，不以配置存在推断已行使。

### Edge Cases

- **双重角色执行体在子项仍在运行时收到自己的返回窗口**：MUST NOT 报 completed；未完成子项按 interrupted/attention 处理，不得用「父已完成」掩盖子项状态。
- **同一 label 被重用或重试**：按派发尝试标识区分；stale attempt 的回传 MUST NOT 被当作当前结果消费。
- **子代理声称 superagent 却没有对应边**：判定面 MUST 判违例并点名，不得按提示词措辞采信。
- **根本身是远端执行（桌面会话为根）**：根永不作为 subagent；远端执行是其 subagent，不得因跨主机而反转。
- **人在子项运行中发消息**：可服务、不被排在新工作后、不因等待子项而失效。
- **子回传缺显式异常行**：判 incomplete，不消费结论；MUST NOT 由父代填「无异常」。
- **虚拟模态成员被授予派发权**：按既有「virtual 不得承载」与载体规则拒绝，不得因角色上升而例外。
- **节点在 digest 中被截断**：必须声明被省略条数；过期条目必须带 stale 标记，不得当作当前数据。
- **中断后旧尝试进程仍在**：恢复报告 interrupted/attention；不得重派已完成子项，也不得回放旧消息。
- **SDD 阶段执行体试图充当 driver 或缺三条件**：按既有收窄谓词拒绝；本模型 MUST NOT 放宽任何一条。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 定义与角色判定

- **FR-001**: 本框架 MUST 把 super agent 正式定义为**派发边上的相对逻辑角色**（[[STR-001]]），不是一个实体类型、不是 Agent 三层分类法之外的新层：一条派发边上，创建子执行体的一端是 super agent，被创建的一端是 subagent；分类 MUST 只由边决定，MUST NOT 由执行体类型、模型、工具列表、提示词措辞或个人描述决定。定义与术语边界的唯一 owner MUST 是 [[STR-004]]（框架源 `shared/definitions/superagent-definitions.md`，按 Two Hats 镜像到运行时）；`agent-definitions.md` 与 `subagent-definitions.md` MUST 只新增指向该 owner 的指针行，MUST NOT 复制规则，也 MUST NOT 出现第二个 subagent 定义。
- **FR-002**: 边的判定谓词 MUST 可机器判定且与记录一致：一条有向边 `P → C` 存在，当且仅当 P 的一次派发产生了 C 的一次执行；同一次派发 MUST 恰好对应一条边；角色词表以 [[STR-001]] 为 super agent 的机器标识；在同一执行体上角色是**集合**（[[STR-002]] 表示同时具备 subagent 与 superagent 两种角色），MUST NOT 被压成单一类型；自派发（P = C）MUST 被判为违例。
- **FR-003**: 边 MUST 有唯一机读记录形态（record kind [[STR-005]]）：父执行体身份、子执行体身份、派发尝试标识，以及这些字段所在的既有载体。字段 MUST 解析到既有载体：子身份 MUST 使用既有派发 label（team/dispatch 约定、`run-agent` 的 label，或 stage-runner 的 line+stage 产物命名）；父身份 MUST 是其自身被派发时的 label，根执行体 MUST 使用其既有的运行标识（状态脊 `run_id` 或 line registry `line_id`，无运行标识时使用 owner 文档声明的根标记）。本特性 MUST NOT 新建 registry、状态存储或第二份状态脊。
- **FR-004**: 深度 MUST 可判定：根执行体深度为 0，任一执行体的深度等于从其根沿边计数的最短距离，且 MUST 与派发记录一起可复核。深度规则 MUST 与既有治理相容并只引用不复述：SDD 调用链的深度 2 许可链、每成员至多一个运行、virtual 模态不得承载，均由 `.specify/shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation 拥有；本特性 MUST NOT 放宽其中任何一条，也 MUST NOT 把角色深度当作第二份授权规则。
- **FR-005**: 框架 MUST 提供一个确定性的只读判定面（引擎动作），输入是既有运行记录（边记录形态 [[STR-005]]），输出 MUST 可回答：两个身份之间是否存在边；每个执行体在各边上的角色集；其深度；以及违例（自派发、悬空父、无对应边的角色声明、深度越界）。判定面 MUST 只读（零写点）、MUST 满足宪法 XXI 的脚本接口契约、MUST NOT 引入任何存储；不可读或缺失输入 MUST 以具名错误失败，MUST NOT 静默返回空集或按通过处理。该判定面 MUST 由契约测试守护：注入一条违例时转红。
- **FR-006**: 判定结果 MUST 与既有运行记录逐条可核对：角色查询里的父/子身份 MUST 能在状态脊、line registry 条目、artifact triplet 或 run report 的派发映射表中解析；任一侧无法解析 MUST 报悬空并点名两侧路径，MUST NOT 用对话摘要补建关系。
- **FR-007**: 相对性 MUST 由三个真实形态的验收覆盖，且 MUST NOT 被解释成实体种类：(a) 桌面端 Qoder 经 SSH 启动远端 qodercli——桌面端是 super agent、远端执行是 subagent；(b) 本地 qodercli 运行一个 team——qodercli 是 super agent、team 成员是 subagent；(c) team 成员并发扇出 10 个 subagent 并自行汇总——该成员在父边上是 subagent、在 10 条子边上是 super agent。三个形态 MUST 各有夹具或可复核的实测记录；任一形态的角色方向被反转时对应验收转红。

#### B. super↔sub 协议

- **FR-008**: 下行派发 MUST 在既有派发载荷通道内携带角色与身份字段：父执行体身份、子派发 label、角色声明（本边上是 subagent；是否被授予 superagent 职责）、深度位置、授权依据的引用、结果契约与回传通道；既有四项注入（快速失败子句、并发义务、汇报义务、re-anchoring 锚摘要）MUST 继续按原 owner 注入且只以指针携带，MUST NOT 复制其规则文本；载荷 MUST NOT 指示子代理加载任何技能、MUST NOT 引用驱动技能或包含循环逻辑（反嵌套义务不变）。
- **FR-009**: 上行回传 MUST 携带：结果或交付物路径、证据指针、显式异常行（无异常也须明说）、并发读数三元组、返回执行体的身份；任一必备项缺失即 incomplete return，父 MUST NOT 消费其结论、MUST NOT 代填缺失字段；异常行缺失或为空同判 incomplete。
- **FR-010**: 边内消息 MUST 按目的归入一个封闭分类集（owner 文档单点声明，最少区分 ack、answer、result、attention-escalation 四类）；未被归类的「进度」叙述 MUST NOT 作为消息沿边向上转发，子执行体的活动性 MUST 由既有 liveness 载体现。本特性 MUST NOT 新建注意力机制、通道或通知服务。
- **FR-011**: super agent 对人类的汇报 MUST 继续完全由 `.specify/shared/guidelines/reporting-obligations.md` 拥有（节奏、四要素、非周期触发、reporter 席位、零新增机制）；边内抑制与面向人的汇报是两个流，MUST NOT 互相替代：边内不转发进度 MUST NOT 被读作可以向人少报或缓报。
- **FR-012**: 等待 MUST 有界且可观察：super agent MUST NOT 对子执行体做无界阻塞等待；等待与监听 MUST 复用既有 watch model（`.specify/skills/sdd-loop-driver/references/watch-model.md`）；人类的中止或改向 MUST 始终可服务；子执行体的停滞 MUST 按既有阈值判定并区分 slow 与 stalled，且经既有汇报义务上浮。
- **FR-013**: 每次重试 MUST 是一次新的派发尝试（沿用既有迭代与 label 约定），MUST NOT 覆盖旧尝试的产物；父 MUST NOT 把 stale attempt 的回传当作当前结果——归属 MUST 沿用既有 attribution 取值（own / foreign / stale-run / unattributed / legacy）；旧尝试产物 MUST 保留（non-disposable）。
- **FR-014**: 一条边能做什么 MUST 只由既有声明面裁决：agent 定义的能力键与席位策略（`sdd-route.py --action authorize`）、已记录的路由裁决、以及 team territory；消息内容 MUST NOT 扩大权限；被拒绝的派发 MUST 产出既有具名拒绝记录（失败半边、解析值、两处来源路径、席位）；resume 或 retry 之前 MUST 按同一依据重验证，MUST NOT 继承先前消息里的授权；拒绝 MUST NOT 通过改写措辞修复。
- **FR-015**: 边的结束（completed / failed / cancelled）MUST 写入其既有载体并使父可判定；父 MUST NOT 让子静默成为孤儿；取消与终止 MUST 遵循既有确认门与破坏性动作判据，MUST NOT 因本模型新增确认门。
- **FR-016**: 本协议 MUST NOT 新增传输、通道、队列或调度器：下行、上行、升级与终止都走既有派发载荷与既有运行记录；新增的只是字段与分类，不是第二条通信路径。

#### C. 身份转变注入

- **FR-017**: 当一个 subagent 被授予派发自己子执行体的权利时，派发载荷 MUST 携带身份转变注入（[[STR-003]]），且 MUST 至少包含：(a) 该执行体在本边上的 superagent 角色激活与可派发范围；(b) 它自己的身份与父边；(c) 它必须向自己的每次派发注入的义务清单（按指针）；(d) 可用并发预算与既有 slot/reserve 事实的引用；(e) 汇报路径与 reporter / 主从汇报义务；(f) 它必须读写的既有状态载体与写者边界；(g) 注意力分类与升级规则；(h) 深度剩余与禁止项（承载 SDD 的三条件、virtual 不得承载、每成员一运行，按既有 owner 引用）；(i) 聚合回传契约。注入 MUST 以指针形态承载，MUST NOT 复制任何 owner 的规则文本。
- **FR-018**: 注入 MUST 在派发载荷中物理存在（常驻指令层到不了子代理），并 MUST 由既有派发前自检的形态（载荷子串判定）验证：缺少 [[STR-003]] 的派发 MUST 被判为派发构造缺陷并被阻断；MUST NOT 只在文档里声明注入而不进入载荷。
- **FR-019**: 双重角色执行体 MUST 保留其作为 subagent 的全部上行义务（回传契约、异常行、并发读数、边界与异常停止）；获得 superagent 角色 MUST NOT 减免其中任何一项。
- **FR-020**: 双重角色执行体 MUST 把其子执行体的回传聚合成向父的一次结构化返回（第三个真实场景的自行汇总）：聚合 MUST 逐子归属、携带每子的证据路径，MUST NOT 隐藏失败或异常子项；聚合 MUST NOT 取代子项证据，父 MUST 可按需下钻。
- **FR-021**: 身份转变注入 MUST 有稳定标识（[[STR-003]]），供派发前自检、契约测试与运行记录引用；判定 MUST NOT 依赖自然语言关键词匹配作为唯一判据。

#### D. 并发

- **FR-022**: super agent 的并发 MUST 由既有并发义务与事实拥有：默认并发、声明类别、串行理由码、读数三元组、slot cap 与 verifier reserve（owner：`.specify/shared/definitions/subagent-definitions.md` § The Concurrency Obligation 与 `shared/declarations/facts/` 下的 `concurrency-class.yaml`、`serial-reason.yaml`、`effective-concurrency.yaml`、`concurrency-slot-and-reserve.yaml`）；本特性 MUST NOT 引入第二套并发机制（调度器、信号量、队列、第二份配额表或第二套读数）。
- **FR-023**: 容量预留 MUST 在派发之前完成，且相对其他派发是原子的：不得两个派发同时占用最后一个可用槽，不得先等待再检查；有效可用量 MUST 由既有 slot/reserve 事实计算；有效可用低于 2 时 MUST 按既有预算理由码降级为串行并记录读数，MUST NOT 超发，也 MUST NOT 把降级写成 `effective` 的数字。
- **FR-024**: 嵌套 MUST NOT 放大容量：被授予派发权的执行体不获得新的槽位；在飞执行体总量 MUST 仍受声明的 cap、ceiling 与预算约束；超发 MUST 被判为缺陷并记录，MUST NOT 静默发生。

#### E. 状态同步与恢复

- **FR-025**: 边状态 MUST 有单写者：父拥有边记录与聚合状态，子拥有自己的最新状态（artifact triplet 的 `.status` 与回传）；父 MUST 在下一个外部可见动作（再派发、向上汇报、合并）之前记录边与已收到的返回；MUST NOT 维护共享可变聚合，写入 MUST 按 Concurrent Development Safety 的 per-entry 形态落盘。
- **FR-026**: 父 MUST 只从既有记录派生子状态：三层事实分别是状态层（状态脊 / line registry 条目）、Assignment 事实层（artifact triplet 的 `.status`、回传、run report）、宿主事件层（watch model 的 pid / heartbeat / liveness）；MUST NOT 从对话记忆、子会话正文或进程扫描推断状态。
- **FR-027**: 中断后的恢复 MUST 重建边并报告真实状态：重建自三层事实；仍被判定为在跑的子执行体 MUST 标记为 interrupted / attention，MUST NOT 静默当作 running 或 completed；恢复动作 MUST 沿用既有恢复与重入机制。
- **FR-028**: 恢复与重入 MUST 在动作前按 FR-014 重验证授权，并 MUST NOT 回放旧消息或重派已完成的子项；无法重验证 MUST 以具名失败停下。

#### F. 状态跟踪与可视化

- **FR-029**: 既有 on-demand digest / status 投影 MUST 增加角色-边视图：对每条活动执行体输出身份、父边身份、角色集、深度、状态、最近活动与距今时长、stale 标记；条目 MUST 有界并在截断时声明被省略条数，空集 MUST 渲染既有 `nothing-running` 状态；MUST 与既有 digest 共享同一次状态读取与同一个渲染器，MUST NOT 新建仪表盘、第二 parser 或第二 renderer。
- **FR-030**: 每执行体 liveness MUST 复用既有 artifact triplet；team 与驱动的运行报告 MUST 维护派发映射表（label → 角色 → 工作区），状态行 MUST 携带既有归属（结构 slug + 运行戳）；本特性 MUST NOT 新增观测面或第二份映射。
- **FR-031**: 一个父执行体对 N 个子执行体的扇出形状 MUST 在同一次 digest 读取中呈现（父一行 + 逐子状态），MUST NOT 为角色视图另建 parser 或第二渲染面。

#### G. harness 落点与零重复

- **FR-032**: 定义 owner（[[STR-004]]）MUST 在框架源 `shared/definitions/superagent-definitions.md` 编写并镜像到运行时；文档 MUST 承载完整模型：角色定义、边谓词、深度、协议（下行 / 上行 / 分类 / 等待 / 尝试 / 授权 / 终止）、身份转变注入、状态同步与恢复映射、可视化映射、零第二机制边界、术语边界。`agent-definitions.md`、`subagent-definitions.md`、`framework-map.md` MUST 各新增指向该 owner 的指针行，MUST NOT 复制规则。
- **FR-033**: `templates/instructions-template.md` MUST 新增一个极小指针段（相对角色一句话、owner 路径 [[STR-004]]、身份转变注入存在的声明）；重新生成后 `.specify/instructions.md` MUST 保持在 `scripts/bash/generate-instructions.sh` 的 `INSTRUCTIONS_BUDGET_BYTES` 之下（以生成器的预算报告为判据），且该段 MUST NOT 复制模型或预算数值；余量不足时 MUST 缩减为纯指针，MUST NOT 抬高预算或以超预算交付。
- **FR-034**: 派发面 MUST 接线且只加字段：`run-agent` 的派发注入清单 MUST 增加 [[STR-003]] 项（按指针）；team 派发与驱动阶段派发 MUST 在其既有载荷中携带父身份、子 label 与角色声明；MUST NOT 新增第二套协议、第二个派发器或第二个调度入口。
- **FR-035**: 本特性 MUST NOT 新建第二套并发机制、registry、状态存储或报告体系；新增判定面 MUST 只读；`status-digest.py` MUST 仍是唯一 digest 渲染器；汇报义务、并发事实与授权裁决 MUST 保持其既有 owner。该项 MUST 以结构断言取证（变更集审计 + 只读性断言），MUST NOT 只以措辞声明。
- **FR-036**: 受影响的既有测试与文档 MUST 逐条处置（改写 / 保持 / 移除）；移除仅限「所断言的事实已被本特性删除」；处置后的全套契约测试 MUST 在 `>=3.8` 上全绿；MUST NOT 让任何既有断言静默失效。
- **FR-037**: 实现 MUST 在 Python >= 3.8 上运行、零新增第三方依赖；测试执行唯一入口 MUST 是 `.specify/scripts/bash/run-tests.sh`；新增或修订的可执行脚本 MUST 满足宪法 XXI（`--help`、`--version`、未声明选项拒绝）。

#### H. 本运行对 080–094 的观测

- **FR-038**: 收尾 MUST 产出一份机制观测附录：对 080–094 中本仓 `.specify/specs/` 实际存在的每个切片，逐条记录本运行实际观测到的机制行使证据路径，或显式记录 [[STR-006]]；MUST NOT 以配置存在推断已行使，MUST NOT 声称未被观测的改善；附录 MUST NOT 替代本特性的验收证据。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时——它消费既有 Python 解释器、既有 pytest 运行器、既有派发与状态载体以及既有 digest 投影。`Premises` 指向 plan 阶段将定义的执行前提。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库（角色判定面的读取与判定、digest 投影扩展） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 既有 `requires-python`；本特性零新增第三方依赖 | `pyproject.toml` | 判定面与 digest 扩展在同一解释器上跑通，同输入两次得到相同判定 | FR-005, FR-029, FR-037 | EP-001 |
| RS-002 | `pytest`（契约测试与夹具，唯一入口 `scripts/bash/run-tests.sh`） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 既有 `pytest` 依赖；零新增依赖 | `scripts/bash/run-tests.sh` | 新增与处置后的契约测试在 `>=3.8` 上通过，测试入口为 runner | FR-036, FR-037 | EP-002 |
| RS-003 | 既有派发与状态载体（artifact triplet、run report 映射表、状态脊、line registry 条目） | in-scope | 各载体既有 owner（本特性只扩展字段读取，不新建 store） | 不适用（无外部版本面） | `scripts/python/status-digest.py` | 边记录可从这些载体逐条解析；悬空记录被点名 | FR-003, FR-006, FR-025, FR-030 | EP-003 |
| RS-004 | 本特性新增的只读角色判定引擎 | in-scope | 本特性自身（路径与 CLI 形态由 plan 固定） | 不适用（无外部版本面） | 本特性新增的只读判定引擎（路径由 plan 固定） | `--help` / `--version` 与未声明选项拒绝满足宪法 XXI；零写点由结构断言取证 | FR-005, FR-035 | EP-004 |

### Key Entities *(include if requirement involves data)*

- **角色（Role）**: `superagent` / `subagent` / `dual-role`——派发边端点的相对分类；不是实体属性，不进入 Agent 三层分类法。
- **角色边（Role edge）**: 一次派发产生的有向关系 `P → C`；承载父身份、子身份、派发尝试标识与解析载体；是所有角色、深度与状态视图的坐标系。
- **根执行体（Root execution）**: 直接持有用户会话的执行体；深度 0，永不作为 subagent；根身份取其既有运行标识或 owner 文档声明的根标记。
- **角色深度（Role depth）**: 从根沿边计数到该执行体的最短距离；与既有 SDD 治理的深度限制互相引用而不互相替代。
- **双重角色执行体（Dual-role execution）**: 同时是某条边的 subagent 与另一条边的 superagent 的执行体；第三个真实场景的核心形态。
- **身份转变注入（Role-transition payload）**: 授予派发权时随派发载荷物理携带的有界指针清单（[[STR-003]]）；不是新文件、不是新通道。
- **派发尝试（Dispatch attempt）**: 一次派发及其独有的尝试标识与区间；重试是新尝试，旧尝试产物保留。
- **边记录（Edge record）**: 对既有载体（状态脊 / line registry / artifact triplet / run report 映射表）的投影形态（[[STR-005]]），不是新存储。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 相对角色判定成立：root→A→B 夹具得到 A 的双角色与深度 1、B 的 subagent 与深度 2；同一执行体同时输出 subagent 与 [[STR-002]]，super agent 的机器标识为 [[STR-001]]；自派发、悬空父、无边角色声明三类违例各自判红；把判定改为按执行体类型时测试转红。 **Path**: final
- **SC-002**: 身份转变注入完整且被强制：授予派发权的载荷含 [[STR-003]] 的九项，删去任一项时派发前自检阻断；双重角色执行体的上行回传仍含回传契约、异常行与并发读数；缺项被当作完整成功时测试转红。 **Path**: final
- **SC-003**: 三个真实形态端到端成立：SSH 远端、本地 team、10-child 扇出三个夹具各产出可解析的边记录与角色视图，方向与深度正确；反转任一场景的角色方向或把 team 成员判为仅 subagent 时测试转红。 **Path**: final
- **SC-004**: 并发不变量成立：交错派发夹具中无双重占用最后一槽（预留先于派发）；读数三元组逐 grain 记录；嵌套不放大容量；可用量低于 2 时降级带预算理由码；把预留移到派发之后时测试转红。 **Path**: final
- **SC-005**: 状态同步与恢复成立：父只从既有记录派生状态（第二来源被结构断言判红）；中断夹具恢复后子项标记 interrupted / attention，stale attempt 的回传不被消费，resume 重验证授权；从对话记忆恢复的实现判红。 **Path**: final
- **SC-006**: 可视化单渲染成立：digest 输出含身份、父边、角色、深度、状态、age、stale，截断含 omitted、空集为 `nothing-running`；删去任一字段或新增第二 renderer 时测试转红。 **Path**: final
- **SC-007**: harness 落点成立：instructions 生成文件在预算内（生成器报告 under），模板段为指针形态且 [[STR-004]] 路径存在；把预算数值写入模板或该段复制规则文本时测试转红。 **Path**: final
- **SC-008**: 零第二机制成立：变更集审计显示无新增持久化根、registry 或报告渲染器；新增判定面无写点；并发、汇报与授权的 owner 未被复制规则文本；注入第二 store 时结构断言转红。 **Path**: supporting
- **SC-009**: 既有规则不削弱：反嵌套、深度 2 许可链、每成员一运行、virtual 不得承载的既有契约测试全绿；放宽任一禁令时对应测试转红。 **Path**: supporting
- **SC-010**: 080–094 观测附录成立：每个存在切片的 `exercised` 行都有可解析证据路径，[[STR-006]] 行显式；无证据的行不得标 `exercised`；附录不得取代本特性验收；把未观测行标成 `exercised` 时检查转红。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 角色判定夹具与只读判定面的实测输出（边集、角色集、深度、违例三类），加上「按类型判定」的合成变异实测；记录到 `test-evidence/`。
- **SC-002 Source**: 派发载荷夹具：九项逐项存在性断言、删项后派发前自检的阻断实测、双重角色上行回传的四项断言；记录到 `test-evidence/`。
- **SC-003 Source**: 三个形态夹具的运行记录（边清单、角色方向、深度、远端产物路径），远端形态按既有 external-dispatch recipes 记录；反转方向的合成变异实测。
- **SC-004 Source**: 交错派发夹具的时序与预留记录、读数三元组、嵌套容量读数、低于 2 槽的降级记录；把预留后移的合成变异实测。
- **SC-005 Source**: 中断夹具与恢复输出（interrupted / attention 标记、stale 回传不消费、resume 授权重验证），以及「从对话记忆派生」的结构断言读数。
- **SC-006 Source**: digest 实读输出（字段清单、omitted、`nothing-running`、stale），与第二 renderer 的结构断言。
- **SC-007 Source**: `scripts/bash/generate-instructions.sh` 的预算报告表（live B / tmpl B / status），模板段字节与指针断言；预算数值写入模板的合成变异实测。
- **SC-008 Source**: 变更集结构审计（新增持久化根计数、registry 计数、renderer 计数、判定面写点计数）和对应变异实测，记录到 `test-evidence/`。
- **SC-009 Source**: 既有反嵌套 / 深度 / 成员运行上限 / virtual 承载的契约测试执行读数，加上放宽禁令的合成变异实测。
- **SC-010 Source**: 观测附录逐行检查：切片存在性、`exercised` 行的证据路径可解析、[[STR-006]] 行显式；无证据行标为 `exercised` 的合成变异实测。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"superagent"` | FR-001, FR-002, SC-001 |
| `STR-002` | `"dual-role"` | FR-002, SC-001 |
| `STR-003` | `"role-transition"` | FR-017, FR-018, FR-021, SC-002 |
| `STR-004` | `".specify/shared/definitions/superagent-definitions.md"` | FR-001, FR-032, FR-033, SC-007 |
| `STR-005` | `"role-edge"` | FR-003, FR-005 |
| `STR-006` | `"not-observed"` | FR-038, SC-010 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-11-10（无人值守 requirements 阶段，自行裁决并记录）

- Q: super agent 的定义应放进既有 `subagent-definitions.md`，还是新建一个 owner 文档？ → A: 新建 [[STR-004]]，并让 `agent-definitions.md`、`subagent-definitions.md` 与 `framework-map.md` 只加指针行。理由：`subagent-definitions.md` 已拥有三种执行模态、并发义务、可见性契约与派发治理，是「子端」的 owner；super agent 回答的是父子关系这一不同问题，混入会让两个 owner 都既长又难引用；新建一页不构成第四层分类法，因为角色作用在既有 Agent Execution 层上（FR-001、FR-032）。
- Q: 角色边与 line registry 的 `parent_line_id` 是不是同一张父子关系？ → A: 不是，两条轴必须分开。line registry 的 parent/child 是**写线治理**轴（`line_role=agent-write`、父线不得本身是子线、深度恰为一），角色边是**执行授权与观测**轴（一次派发产生一条边，深度由根计算）。第三个真实场景的扇出子项不是写线，不得为了登记角色而把它们塞进 line registry；反过来本特性 MUST NOT 放宽 line registry 的深度规则。两条轴在一条执行体同时拥有写线时互相引用，不互相改写（FR-003、FR-004、FR-024）。
- Q: 研读材料里的「WorkerSlots 人优先（可超上限一个槽）」是否作为需求采纳？ → A: 不采纳为一个新槽位值。框架里人的请求从根会话进入，不在 worker 槽位上排队；「人优先」落成三条可判定规则：super agent 不得无界阻塞等待、人的中止或改向始终可服务、面向人的汇报继续按既有节奏（FR-011、FR-012）。新增一个超上限槽会改变既有并发事实的调优，超出本特性的证据面。
- Q: 「进度不转发」与框架既有的强制汇报义务冲突吗？ → A: 不冲突，二者是两个流。边内不转发未分类进度；根或监督者面向人的汇报仍完全按 reporting obligations（节奏、四要素、非周期触发、reporter 席位）执行。把「边内抑制」读成「向人少报」是缺陷（FR-010、FR-011）。
- Q: 重试与旧结果如何区分？ → A: 每次重试是新尝试，有新的尝试标识与 label；旧尝试产物保留，父只能消费当前尝试的返回，stale attempt 按既有 attribution 取值识别（FR-013）。
- Q: 080–094 的「验证效果」怎么落成交付，而不是一句口号？ → A: 落成收尾的机制观测附录（FR-038）：只覆盖本仓实际存在的切片，逐条 `exercised`（带可解析证据路径）或 [[STR-006]]；不推断、不把配置存在当作行使，也不替代本特性自己的验收证据。

## Assumptions

- **A1（Flow Class 判定理由）**: 判为 `execution`——验收 oracle 是机器行为：定义文档被 agent 读取、派发载荷被契约测试断言、digest 投影被程序消费、角色判定面被程序执行；缺陷在机器读错或执行错时暴露，而不是只在人读错时暴露。
- **A2（新概念 = 新 owner 页，不是第四层）**: super agent 是框架此前未归一化的新概念，owner 是新增的 [[STR-004]]；角色作用在既有 Agent Template → Instance → Execution 三层之上，不新增层。既有分类法只加指针行。
- **A3（三个场景是定义输入，验收分层）**: 场景 1 的验收以既有 external-dispatch recipes 与记录的远端产物为准，不在测试套件内真实铺设 SSH 主机；场景 2、3 用夹具与真实运行记录共同取证。三个场景的「角色方向」是硬断言。
- **A4（深度与既有 SDD 治理的关系）**: 根 = 用户会话；角色深度按边计数。既有 SDD 深度 2 许可链、每成员一运行、virtual 不得承载仍由 `subagent-definitions.md` 拥有；本模型只解释这些限制在角色图上的位置，不放宽也不新增授权规则。场景 3 的 10 路扇出是通用工作，按既有 fork / subprocess 载体执行，不属于 SDD 链。
- **A5（人优先的落点）**: 见 Clarifications 的第三条裁决——落为「不得无界阻塞等待、人的中止或改向可服务、面向人的汇报照旧」，不新增超上限槽位值。
- **A6（两个汇报流）**: 边内抑制与面向人的汇报互不替代；本特性不新建议汇报通道，也不改变 reporting obligations 的任何数值或席位规则。
- **A7（指令预算）**: 项目指令体积预算由 `scripts/bash/generate-instructions.sh` 的 `INSTRUCTIONS_BUDGET_BYTES` 与其报告拥有；本特性只在剩余余量内增加指针段。余量不足时缩段是唯一合法处置，抬预算属另一项治理变更。
- **A8（零新增持久化）**: 边记录是既有载体的投影；若实现需要新字段，字段加在既有载体的 schema 里并由该载体的 owner 修订，不新建 store。角色判定面必须零写点。
- **A9（080–094 的证据边界）**: 本运行是观测机会，不是机制评审结论；未观测即 [[STR-006]]，不推断、不补写「已改善」。附录不替代本特性的验收证据。
- **A10（工作树纪律）**: 工作树存在本特性开始前遗留的脏文件；本特性只提交自己的产物，不提交、不还原这些文件，也不 push。
- **A11（实现面命名）**: 角色判定引擎的路径、CLI 动作名与根标记字面量由 plan 阶段固定；本规格固定的是查询语义、Shared Strings 与边记录形态，不固定这些实现名。
- **A12（判定方式）**: owner 文档以路径引用既有规则；守护测试断言指针形态、预算行为与结构不变量，不以散文措辞作为唯一证据（盲检查教训：只对措辞的绿不构成证据）。
