# Requirements Specification: goal/team 与 spec 的平行关系（重定义 085 的作用域与绑定模型）

**Requirement Branch**: `092-goal-team-parallel`
**Created**: 2026-11-09
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（修订 085 引入的 goal/team 机制、`goal-utils.py`、`create-team` / `run-team`、驱动者 § Temporary Goal/Team 与 checkpoint 协议的作者）、下游项目里同时使用 `/speckit.*` 命令与 SDD 演进流程的项目维护者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 在判定「一次运行能否拥有 goal 与 team」「goal/team 的档案落在哪里」「spec 与 goal+team 谁附属谁、交接发生在哪」时打开本规格，据 FR-001…FR-042 与 SC-001…SC-010 决定 `/speckit.plan` 与后续实现是否放行
**Input**: User description: "需要将085扩展到 /speckit.feedback 这类命令, 临时goal和临时team不仅仅是作用于SDD流程,也作用于speckit*命令, 在这点上需要将临时goal和临时team的归档目录挪到原本的.specify/goal和.specify/teams中,而不是.specify/specs/091-auto-git-closeout/goal和.specify/specs/091-auto-git-closeout/team这类spec子目录,  spec的SDD和goal+team应该是平行关系而不是从属关系. "临时"和"全局"也不是一个标准概念, 需要进行重定义. spec和goal+team的关系应该类似于 "设计师"和"施工队",  动手能力强的"设计师"可以自己动手完成一些简单的工作(在spec的sdd流程中直接执行), 有一定设计能力的"施工队"也可以自己完成一些简单的方案设计(goal直接进行设计然后执行), 但是比较复杂的工作就应该是"设计师将设计稿交给施工队去执行"(如前面的 implement阶段有 62 个任务)."

## Related Feature *(mandatory)*

**Feature ID**: 092
**Feature Name**: goal/team 与 spec 的平行关系（Goal/Team × Spec Parallelism）

## Overview

085 把 goal/team 机制整体挂在 SDD 流程**之下**：goal/team 只在 SDD 运行中存在，存放于 `.specify/specs/<NNN-slug>/goal|team/`，`/speckit.goal` 与 `/speckit.team` 的唯一读写面就是这两个 spec 子目录，全局档案 `.specify/goal/**` 与 `.specify/teams/**` 对 SDD 运行是 forbidden path。三个后果与用户诉求直接冲突：

1. **只有 SDD 能用**：`/speckit.feedback`、`/speckit.docs`、`/speckit.sanitize` 这类命令运行既没有 goal，也没有 team，机制价值被限制在一条流程里。
2. **档案分裂**：同一概念（一个 goal、一个 team）因为「谁创建了它」而落在两种互不相同的路径上，`.specify/goal/` 与 `.specify/teams/` 这两张既有的框架级档案表反而只登记了一半。
3. **从属关系被写进了路径**：路径选择本身就在声明「goal/team 属于 spec」。用户要的是**平行**。

本特性把这三件事一次改到位，并**删除「临时 / 全局」这一对非标准概念**：不再靠目录位置区分两条线，改由一张可判定的**绑定（binding）、作用域（scope）与生命周期（lifecycle）模型**决定每个 goal/team 属于谁、活多久、能被谁读写。spec（设计师）与 goal+team（施工队）成为两条**平行执行线**：简单工作各自直接做，复杂工作由 spec 出「设计稿」、goal+team 按「交接契约」施工。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 命令运行也能拥有 goal 与 team (Priority: P1)

用户运行 `/speckit.feedback`（或 `/speckit.docs`、`/speckit.sanitize` 等）时，命令可以声明并维护属于自己的 goal 与 team：goal 记录这次处理的终态，team 记录座席与并发，二者与 SDD 运行用的是同一套引擎、同一套结构、同一张档案表。

**Why this priority**: 这是整条诉求的入口。没有它，goal/team 机制的适用范围仍然只有 SDD 一条线，「扩展到 `/speckit.*` 命令族」不可能被验收。

**Independent Test**: 在一个没有 SDD 规格目录的夹具里发起一次命令运行，创建一个 goal 与一个 team，断言二者落在 `.specify/goal/<slug>/` 与 `.specify/teams/<slug>/`，且其上记录的 binding 指向该命令运行，不指向任何 spec。

**Acceptance Scenarios**:

1. **Given** 一个不含任何 `goal/` 或 `team/` 子目录的规格目录，**When** 一次命令运行创建 goal 与 team，**Then** 创建成功，档案位于 `.specify/goal/<slug>/goal.md` 与 `.specify/teams/<slug>/team.md`，且 `.specify/specs/` 下不新增任何路径。
2. **Given** 一次命令运行已创建 goal 与 team，**When** 该运行写 run report 与运行记录，**Then** 记录落在 `.specify/teams/<slug>/runs/` 下，不落在任何 spec 子目录。
3. **Given** 一次 SDD 运行同样创建 goal 与 team，**When** 比对两次创建的存储形态，**Then** 引擎、目录形态、definition schema 与校验规则完全一致，唯一差异在 binding 行记录的创建者身份。

---

### User Story 2 - 档案统一落 `.specify/goal/` 与 `.specify/teams/`，旧数据归档不删除 (Priority: P1)

goal 与 team 只有一处落点：`.specify/goal/<slug>/` 与 `.specify/teams/<slug>/`。SaaS 化的旧落点 `.specify/specs/<spec>/goal|team/` 不再产生新写入；仓库里已经存在的 7 个 spec-local goal 与 7 个 spec-local team 经迁移命令搬入统一档案，原位置留下归档回执而非被删除。

**Why this priority**: 与 User Story 1 同一级——两者缺一，档案仍然分裂。这条也是唯一带**破坏性风险**的诉求，必须由可判定规则钉死「archive-not-delete」。

**Independent Test**: 在一个复刻现状的夹具里放入若干 `.specify/specs/<spec>/goal/<slug>/goal.md` 与 `.specify/specs/<spec>/team/<slug>/team.md`，运行迁移，断言统一档案出现同 slug 的定义、原路径的数据未被删除（内容仍在归档回执所指处可读）、且迁移可重跑幂等。

**Acceptance Scenarios**:

1. **Given** 一个 spec-local goal 历史目录，**When** 迁移运行，**Then** `.specify/goal/<slug>/goal.md` 出现且内容与源定义等价，源目录被移入归档位置并留下一条指名来源 spec 与 slug 的回执，源文件未被删除。
2. **Given** 迁移已完成的仓库，**When** 再次运行迁移，**Then** 不产生第二个副本、不覆盖已有定义，退出码可判定（幂等）。
3. **Given** 迁移后的仓库，**When** 检索新写入路径，**Then** 不存在任何写 `.specify/specs/<spec>/goal|team/` 的代码路径或文档指令；仅保留只读探测以报告未迁移残余。

---

### User Story 3 - spec 与 goal+team 是两条平行线，简单工作各自直接做 (Priority: P1)

`.specify/specs/` 下的 goal/team 落点消失之后，两条线的地位由「路径从属」变成「档案并列 + 显式绑定」。简单工作可以只走一条线：设计师自己动手（SDD 流程里直接执行），或施工队自己出小方案再做（一个 goal 直接设计并执行）。两条线都不需要对方存在。

**Why this priority**: 这是用户诉求的核心命题，也是判断「平行」与「从属」的分水岭；它必须在**没有任何交接**的情形下也成立。

**Independent Test**: 两个夹具各跑一次——其一只有 SDD 流程、无任何 goal/team；其二只有一个 goal+team、无任何 spec 目录。两次都成功完成交付，且不存在「必须有对方」的前置检查。

**Acceptance Scenarios**:

1. **Given** 一次只有 SDD 流程的运行，**When** 全程不创建任何 goal 或 team，**Then** 流程正常完成，没有一处报错或警告要求 goal/team 存在。
2. **Given** 一个只有 goal+team 的运行，**When** 全仓库不存在对应 spec 目录，**Then** goal 可被创建、team 可被创建与运行，且 binding 行不出现 `spec` 取值。
3. **Given** 两条线都在运行的仓库，**When** 查询某个 goal 的归属，**Then** 归属只由其 binding 行回答，不由它所在的目录回答。

---

### User Story 4 - 复杂工作：设计师出设计稿，施工队按交接契约施工 (Priority: P1)

当一个 SDD 流程的判断落在「复杂」侧（例如一次 implement 阶段有 62 个任务），spec 侧不自己逐个执行，而是产出一份**交接契约**（handoff contract）：把要达成的终态、目标集、领地与验收判据显式交给一个 goal+team 施工队；施工队按契约执行并把进度回写。设计稿的归属、施工的归属、回写的方向都有可判定的形态与不变量。

**Why this priority**: 与 User Story 3 配对——只证明「平行」而不定义「如何协作」，平行就退化为互不相干。这是用户明确点名的「设计师将设计稿交给施工队」。

**Independent Test**: 用一个含 62 个任务的夹具 spec 触发复杂度判定，断言：生成的 handoff contract 存在且被 goal 与 team 共同引用；施工队执行后每个任务的完成状态都经回写到达 spec 侧，且 spec 侧对任务行的唯一所有权未被打破。

**Acceptance Scenarios**:

1. **Given** 一个任务数越过复杂度门槛的 spec，**When** 判定运行方式，**Then** 产出 handoff contract 并交给 goal+team，而不是在 spec 线内串行执行。
2. **Given** 一个任务数在门槛以下的 spec，**When** 判定运行方式，**Then** 允许 spec 直接执行，且不强制产出 handoff contract。
3. **Given** 一份已交付的 handoff contract，**When** 施工队完成全部目标，**Then** spec 侧的每一条任务状态都反映施工结果，而 `tasks.md` 与 `verification.md` 仍由 spec 侧唯一持有，施工队只能交付补丁与回写，不能直接改写任务表。

---

### User Story 5 - 「临时 / 全局」被绑定模型取代 (Priority: P1)

框架里不再使用「临时 goal」「全局 team」这类说法。取而代之的是三条可判定的**绑定维度**——owner（谁发起）、scope（写入与读取的作用域）、lifecycle（何时结束、结束后留什么）——以及一条显式规则：档案位置由 binding 决定，不由概念分类决定。

**Why this priority**: 这一条是前四条能被稳定实现与验收的前提；只要「临时/全局」仍作为判据存在，路径从属关系就会以另一种名字回流。

**Independent Test**: 对框架源码与文档全量检索「临时 goal / 全局 goal」作为**判据**（而非历史记录）的出现，断言运行时面为零；同一个 goal 定义只要改变 binding 就改变其归属与读写权限，而定义文件本身与路径不变。

**Acceptance Scenarios**:

1. **Given** 一个由命令运行创建的 goal，**When** 同一个 goal 被一次 SDD 运行的 team 绑定，**Then** 绑定关系记录在 team 侧（N teams : 1 goal），goal 档案位置与内容不变。
2. **Given** 一个 goal 已完成，**When** 它进入终态，**Then** 其生命周期状态（`achieved` / `abandoned`）在定义文件中表达，档案保留，不被删除、不被移到第二处。
3. **Given** 任一框架运行时面，**When** 检索「临时」「全局」作为分类判据，**Then** 命中为零，命中仅允许出现在历史记录、迁移回执与本特性的规格内。

---

### Edge Cases

- **命令运行在搬运旧档案的中途被中断**：迁移是 [[STR-002]] 上的一次受控档案搬移，运行被中断于「源已移入归档位置、目标定义尚未落盘」之间——迁移 MUST 可判定地报告其阶段与实际状态（源归档目录名 + 目标是否已存在），再次调用 MUST 从该阶段续做而不是重新搬一次；MUST NOT 留下无回执的删除（FR-011 的中断分支）。
- **同一 slug 在两条线都出现**：命令运行与 SDD 运行各建一个同名 goal——引擎 MUST 拒绝第二个创建并指名冲突，MUST NOT 以路径不同为由允许并存。
- **未迁移的旧目录仍在**：迁移不是强制的第一步；未迁移的 spec-local 目录被**只读探测**报告为残余，MUST NOT 被静默当作当前档案写入。
- **迁移中途失败**：源目录已被移动、目标定义尚未落盘——迁移 MUST 可判定地报告失败阶段与实际状态，MUST NOT 留下无回执的删除。
- **handoff 反向污染**：施工队试图直接改写 `tasks.md` / `requirements.md`——MUST 被拒绝，并要求以补丁 + 回写的方式提交。
- **复杂度门槛恰好落在边界**：任务数等于门槛时——MUST 由一条声明值决定，不允许运行时自由裁量。
- **goal 终态后仍被指派新 team**：终态 goal MUST 拒绝新绑定，并指名终态；重新打开须经显式生命周期动作，不是隐式副作用。
- **一个 team 绑定一个 goal，多个 team 共享一个 goal**：N teams : 1 goal 是合法形态；领地重叠 MUST 被侦测并报告，MUST NOT 被静默允许。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 作用域扩展：命令运行可拥有 goal 与 team

- **FR-001**: 框架 MUST 允许任一 `/speckit.*` 命令运行创建并拥有 goal 与 team，且 MUST 与 SDD 运行使用同一套引擎、同一套 definition schema 与同一套生命周期状态；本特性 MUST NOT 引入第二套 goal/team 引擎或第二份 schema。
- **FR-002**: 一个命令运行的 goal/team MUST 通过**[[STR-001]] 记录**声明其归属的运行，该记录 MUST 同时承载两个维度：**身份**——`owner`（封闭三值：`sdd-run` / `command-run` / `human`）与 `owner_id`（该次运行的标识，MUST 与状态脊 `run_id` 同名同义）；**来源**——`origin`（封闭取值 `null` 或一个 spec 目录名）。缺失绑定记录的定义 MUST 被引擎判为不可解释，而不是被默认为任一归属。〔`origin` 与 `owner_id` 的引入理由见 Clarifications 的 Q1〕
- **FR-003**: 绑定记录的写入 MUST 经 goal 引擎（`resolve-scope` 之外的写动作）与 team 机制完成，MUST NOT 由命令模板、技能或驱动者直接改写 `goal.md` / `team.md` 的绑定字段。引擎 MUST 提供**绑定重写动作**：改变 `owner` / `owner_id` / `origin` 时定义文件的其余字节保持不变（SC-009），且这是「同一档案被另一条线接管」的唯一合法路径。
- **FR-004**: 命令运行创建的 goal/team MUST 能在该运行结束后独立成立——即其可读性 MUST NOT 依赖该运行仍在进行；一次运行结束 MUST NOT 使档案失效或消失。
- **FR-005**: 框架 MUST 给出一个**封闭的命令族清单判定方式**：一个命令是否可拥有 goal/team，MUST 由其声明的类决定，MUST NOT 由逐命令硬编码的白名单决定；本特性 MUST 覆盖 `/speckit.feedback` 作为首个取证命令。〔绑定类声明 owner 见 FR-031〕
- **FR-006**: 命令族判定 MUST 消费**既有类别声明**：`flow-class-classes.yaml` 中已登记类别的载体文件 `templates/commands/<command>.md` 构成命令族；判定 MUST 复用既有的类别读取入口 `.specify/scripts/python/flow-class-check.py --action lookup`，并以该入口输出中的 **`source` 字段**为判别子——只有 `source: ledger`（该单元在登记表里有自己的条目）才算入族，`source: default`（未声明的单元按有序清单的第 0 个成员兜底）**MUST NOT** 算入族。理由（实测，2026-11-09）：该清单是有序集合，成员 0 是未声明单元的默认值，因此 `/speckit.nonexistentcommand` 同样输出 `flow_class: execution` 且退出 0，「退出 0 + 返回某个登记类别」不再是族内族外的判别子；对照实测 `/speckit.feedback`、`/speckit.plan` 均为 `source: ledger`，`/speckit.nonexistentcommand` 为 `source: default`、`marker: 未声明·按默认`。判定 MUST NOT 新增类别声明表或第二份命令清单，也 MUST NOT 把 `flow_class` 取值本身当作族判据。〔未声明类别的命令不入族见假设 A9〕
- **FR-007**: goal 与 team 的**唯一**写入落点 MUST 是 [[STR-002]] 的两个档案行 `.specify/goal/<slug>/` 与 `.specify/teams/<slug>/`；框架 MUST NOT 在 `.specify/specs/` 下产生任何 goal 或 team 的新写入路径。
- **FR-008**: goal 引擎的 `resolve-scope` MUST 不再返回 spec-local 的 goal/team 根，其取值域 MUST 被 [[STR-002]] 重写；`spec` 这一取值名 MUST 被删除并让旧调用以可判定的错误失败（`{{SCRIPT-ROOT}}/goal-utils.py` 现有 `invalid choice: <value>` 退出码 2 形态）；其余成员的完整封闭取值集与 `global` 的处置由 FR-025 单一给出，本条不复述；`--spec-dir` MUST 继续为引擎接受，用于解析 `origin` 与判定 `--scope auto` 的输入有效性，但 MUST NOT 再决定定义落点。〔原「两选一、由 plan 裁定」的处置已由 clarify 裁定，见 Clarifications 的 Q2；取值集的唯一 owner 是 FR-025，见 Clarifications 的 Q13〕
- **FR-009**: 框架 MUST 提供一个**幂等的迁移动作**（进入 [[STR-002]]）：把既有 `.specify/specs/<spec>/goal/<slug>/goal.md` 与 `.specify/specs/<spec>/team/<slug>/team.md` 迁入统一档案；迁移 MUST 保留原 slug、原定义内容与 lifecycle 状态，并把「来源 spec」记入 [[STR-001]] 记录的 `origin` 维度。
- **FR-010**: 迁移 MUST 是 archive-not-delete（该事实 MUST 同时写入每一份 [[STR-001]] 记录）：源路径的数据 MUST NOT 被删除，MUST 被移入归档位置 [[STR-003]] 并留下指名「来源 spec / 原 slug / 目标 slug / 关联目标档案 / 结果」的回执；迁移失败 MUST 报告失败阶段，MUST NOT 留下无回执的删除；中断的迁移 MUST 可从其报告阶段续做（见 Edge Cases）。
- **FR-011**: 迁移 MUST 在冲突时停下：目标 slug 已存在且内容不等价时，迁移 MUST 拒绝覆盖并指名两个候选，MUST NOT 择一胜出。冲突识别的判据 MUST 只来自定义文件的**概念载荷**（Objective、Success Criteria、Lifecycle status、Targets 的文本），MUST NOT 包含后来新增的绑定行——否则旧档案一经迁移就必然与自身「不等价」而永久报冲突。〔判据见 Clarifications 的 Q3〕
- **FR-012**: 框架 MUST 提供**只读残余探测**：报告仍存在于 `.specify/specs/*/goal|team/` 的未迁移余额，并 MUST NOT 把残余当作当前档案读取或写入。探测的执行体归 FR-010 的迁移引擎（同一个可执行体的只读动作），MUST NOT 新增第二个可执行体。
- **FR-013**: 迁移完成后 MUST 不存在第二条写入路径：本特性 MUST 以契约测试钉住「写 `.specify/specs/<spec>/goal|team/` 的代码路径数量为零」这一条，MUST NOT 只以文档措辞断言。
- **FR-014**: spec（SDD 流程）与 goal+team MUST 是**平行**执行线：任一条线 MUST 能在对方不存在的前提下独立完成一次交付，框架 MUST NOT 设置「必须先有对方」的前置检查。
- **FR-015**: 一个 goal 的归属 MUST 只由绑定记录回答；框架 MUST NOT 从目录位置推断归属，MUST NOT 保留任何「在 spec 下即属于 spec」的推断规则。
- **FR-016**: 本特性 MUST 定义一个**交接契约（handoff contract）**制品：它把 spec 侧的设计结果显式交给 goal+team 施工，MUST 至少承载：目标终态、目标集（Targets）或任务集引用、施工领地（可写路径集）、验收判据引用、回写要求，以及对施工队的 [[STR-005]] 引用。其落点、契约引用的双向键与生命周期 MUST 由本特性钉死（见 FR-035、FR-034），否则「被 goal 与 team 共同引用」（SC-006）不可判定。
- **FR-017**: 交接契约的**所有权** MUST 唯一：设计稿由 spec 侧产出与修订，施工队 MUST NOT 改写其设计面；施工队 MUST 只能向 spec 侧提交补丁与状态回写。
- **FR-018**: 复杂工作的判定 MUST 可判定：是否走「spec 设计 + goal+team 执行」MUST 由一条**声明值**决定（例如任务数门槛），MUST NOT 由运行期自由裁量；门槛取值 MUST 有唯一 owner 并在边界值上有确定行为。〔取值面与边界语义见 Clarifications 的 Q5〕
- **FR-019**: 在交接模式下，`requirements.md`、`tasks.md`、`verification.md` MUST 仍由 spec 侧唯一持有；施工队 MUST NOT 直接改写这三件制品。
- **FR-020**: 施工完成后 MUST 有**回写路径**：每一条任务的完成状态 MUST 能到达 spec 侧并被判定，回写 MUST 可核验（指名来源运行与证据指针），MUST NOT 以口头/摘要形式替代。
- **FR-021**: 两条线 MAY 同时运行于同一仓库；框架 MUST 在并发形状下保持档案可判定——同一 slug 的第二创建 MUST 被拒绝并指名冲突（见 Edge Cases），MUST NOT 以路径不同（旧落点 vs 新落点）为由允许并存。
- **FR-022**: 框架 MUST 停止把「临时（temporary）」与「全局（global）」用作 goal/team 的分类判据；这一对词 MUST 只允许出现在历史记录、迁移回执与本特性的规格内，MUST NOT 出现在任何运行时判定面。
- **FR-023**: 替换模型 MUST 至少由四个可判定维度构成：`owner`（谁创建：`sdd-run` / `command-run` / `human`，见 FR-002）、`owner_id`（哪个运行，见 FR-002）、`origin`（来源 spec 或无，见 FR-002）、`lifecycle`（goal 侧 `active` / `achieved` / `abandoned`，沿用既有封闭三值；team 侧沿用既有 `lifecycle_state: active | archived`，MUST NOT 把 goal 的三值强加给 team）；每个维度 MUST 有封闭取值域与唯一 owner，它们合起来即该定义的 [[STR-001]]。**读写作用域** MUST NOT 作为声明维度单独存在：它能且只能由 `owner` + [[STR-002]] 机械导出（见下一条）。
- **FR-024**: 概念的**唯一 owner** MUST 是既有的定义文档：goal 侧 `.specify/shared/definitions/goal-definitions.md`、team 侧 `.specify/skills/internal/create-team/references/conceptual-model.md`；本特性 MUST 改写这两处而非新建第三处，且其他面 MUST 只引用不复述（宪法 XIV）。
- **FR-025**: 引擎的作用域取值 MUST 由重定义后的模型重新给出：**封闭三成员** `goal` / `teams` / `auto`——前两个直接命名 [[STR-002]] 的两条档案行，`auto` 表示「由引擎在两条档案行之间唯一解析」，不含任何以 spec 位置命名的成员；`global` 与 `spec` 两个旧取值名 MUST 一并出域（`global` 随档案行改名为 `goal` / `teams` 而不再有对应成员，`spec` 按 FR-008 删除），旧调用 MUST 以 argparse 的 `invalid choice` 退出 2 失败。取值域 MUST 有单一 owner 文档（概念 owner 见 FR-024），`goal-utils.py` 的 `--scope` `choices=` 是该 owner 的执行投影，其他面 MUST 只引用不复述；新取值只表达 [[STR-002]] 与 [[STR-001]] 维度而不再表达位置。〔本条的三个成员与 plan T-004 / 契约 C-9 是同一份取值集；Clarifications 的 Q2 记「保留 `global` / `auto`」的措辞在本阶段被判为「保留两**行**档案语义、改名后为 `goal` / `teams`」，见 Clarifications 的 Q13〕
- **FR-026**: 三条既有全局约束 MUST 被显式重述为新模型的推论而不是被删除：(a) 一个 goal 档案的终态保留（不删除）；(b) N teams : 1 goal 的一向身份引用（team 只存 `goal_slug`，不存 goal 内容副本）；(c) 终态 goal 拒绝新绑定。〔这三条各自有既有 owner，本特性 MUST 引用而非复制其规范文本〕
- **FR-027**: 本特性 MUST 更新路由层的 carve-out：`.specify/shared/definitions/sdd-routing-definitions.md` 中「Temporary run-scoped scopes」段落所描述的 spec-local 许可 MUST 被替换为平行模型下的许可，且 MUST NOT 在改后文本里保留「Temporary」作为判据名。改后许可 MUST 保持**一次 SDD 运行 MUST NOT 创建/重绑/改范围/终止共享档案（`goal` 档案与 team 档案）中的既有定义**这一条禁令不变，只把「运行可以创建设定于其 spec 之下」改为「运行可以创建 `owner: sdd-run` 的定义，档案落 [[STR-002]]」——层级禁令本身 MUST NOT 因作用域迁移而松弛。〔不变量的措辞见 Clarifications 的 Q7〕
- **FR-028**: 驱动者协议 MUST 同步：`.specify/skills/sdd-loop-driver/SKILL.md` § Temporary Goal/Team 与 `references/checkpoint-protocol.md` 的 goal 相关段落 MUST 改写为新模型下的表述（goal 何时创建、写入何处、以何绑定），且 SDD 阶段链与哨兵 MUST 保持不变。同步面 MUST 同时覆盖 `temp_goal_slug` / `temp_team_slug` / `temp_scope_spec_dir` 这组状态脊键：goal 引擎 MUST 为这组旧键提供**一次性迁移别名**（读取时接受旧键、写入新键，别名在 plan 声明的版本点移除），状态脊写入 MUST 跟随 SKILL 正文改写；让旧键在任何一处以可判定方式失效（而不是被悄悄丢弃）是这条 FR 的验收面。
- **FR-029**: 目录地图 MUST 同步：`.specify/shared/definitions/framework-map.md` 的 Goals / Teams 两行 MUST 表达新的落点与归档语义（含 [[STR-003]] 行）；`.specify/specs/` 行 MUST NOT 再暗示其下存在 goal/team。
- **FR-030**: `templates/commands/goal.md` 与 `templates/commands/team.md` 的作用域说明 MUST 改为引用新模型 owner，MUST NOT 复述取值域。迁移与残余探测的**命令入口** MUST 明确唯一所有者：goal 侧归 `/speckit.goal` 的 `migrate-archive` 模式（该命令已是 goal 档案的唯一写入口，MUST NOT 需要第二个人工介入），team 侧由同一动作按 [[STR-002]] 一并处理；`/speckit.sanitize` 只提供只读残余探测并列示读数。〔为何不归 sanitize 见 Clarifications 的 Q8〕
- **FR-031**: 可拥有 goal/team 的命令族判定，与交接复杂度门槛，二者 MUST 各有一个**声明层**条目（`shared/declarations/facts/`），且 MUST 由现有声明读取入口消费；MUST NOT 在脚本内硬编码第三处取值。条目 MUST 在 `shared/declarations/contract.yaml` 完成登记后才可被读取（该契约是值域与 subset id 的 owner，未登记条目按 `owner-unavailable` 处理，不得当作默认值），且两处消费点 MUST 落在**本特性新增或修改的引擎内**，MUST NOT 要求修改既有 `flow-class-check.py` 或驱动脚本。〔登记义务见 Clarifications 的 Q9〕
- **FR-032**: 本特性 MUST 在框架源码侧落地并镜像同步；`templates/` 的框架模板中立性 MUST 保持（MUST NOT 写入本仓专有路径事实）。
- **FR-033**: 本特性 MUST 为 User Story 1–5 中每一个「可判定」断言提供契约级或单元级测试，且每条测试 MUST 在实现缺失时转红；只有文档措辞变化的检查 MUST NOT 被计为取证。
- **FR-034**: 契约与 goal/team 的引用 MUST 是**双向可解析的键对**：契约侧以 `goal_slug` + [[STR-005]] 引用其施工队，goal 定义与 `team.md` 侧以 `handoff_ref`（指向 [[STR-004]] 的 spec 相对路径）反向引用；双向键的写入同受 FR-003 的绑定写纪律约束，MUST NOT 由契约文件单方面声明一个不存在的 team。
- **FR-035**: 交接契约 MUST 落在 spec 目录内的固定相对路径 `<spec-dir>/` + [[STR-004]]，一个 spec 一份（`tasks.md` 为任务表的唯一所有者，契约是它的施工侧视图，MUST NOT 复制任务行，只引用任务 ID 区间或清单）；契约 MUST 由 `tasks` 阶段在判定为「复杂」之后产出，`implement` 阶段消费，生命周期 `active` → `fulfilled` / `abandoned` 两态终局，终局契约保留不删除。〔为何由 tasks 而非 plan 产出见 Clarifications 的 Q4〕
- **FR-036**: 施工队的越权写 MUST 由 `team.md` 既有 `territory` 封闭清单机械拒绝，MUST NOT 依赖施工队的自觉：契约中声明的施工领地在生效时 MUST 被展开为绑定该 goal 的每个 team 的 `territory.write`，spec 侧三件制品（`requirements.md` / `tasks.md` / `verification.md`）与契约文件本身 MUST 落在 `territory.forbidden`。SC-007 的「直写被拒绝」以 `create-team` 的领地判定面取证，不以「施工队被要求不要写」取证。
- **FR-037**: 一次运行的**临时作业区**（[[STR-002]] 的第三行，即 `.specify/` + [[STR-006]] 目录，git-ignored、工作项结束即清理）MUST NOT 被纳入本特性任何迁移、残余探测或档案统一动作：它是既有的既定时点（`shared/guidelines/temp-directory-discipline.md`）而非本特性引入的概念，本特性 MUST 只在其概念 owner 中用一行「不是 goal/team 档案层级」把两者划清；`scan-temp-usage.py` 的既有 `temporary` 词面 MUST NOT 被 FR-022 的字面替换波及。〔理由见 Clarifications 的 Q12〕
- **FR-038**: 可写性与可读性 MUST 由绑定与档案层级的**确定性函数**回答，不由任何声明字段或目录位置回答：team 档案（[[STR-002]]）由该 team 的 `owner` 身份独立可写，其绑定运行的标志 MUST 被记录，但 MUST 不是该档案可写性的条件；goal 档案只有在「没有任何 team（任何档案层）以 `goal_slug` 绑定它」时才对非 `human` 的 `owner` 可写——一旦被绑定，goal 只能经 `/speckit.goal`（`owner: human`）改写，被取代的写入方 MUST 收到可判定的拒绝而非静默成功；team `archived` 后由 `run-team` 拒绝执行；读到 [[STR-002]] 之外的行，写入 MUST 以可判定错误拒绝（`goal-utils.py` 现有 `scope-ambiguous` 退出 2 是这一类的既有先例）。〔该规则替代「读写作用域」维度与旧「全局边界 / forbidden paths」禁令，见 Clarifications 的 Q6〕
- **FR-039**: SPEC（SDD）侧的 goal/team 创建时机 MUST 由本特性的声明层条目给出（FR-031 的第二个条目同源：与任务集大小绑定的两种运行形态就是创建时机的唯一依据），FR-028 的驱动者改写 MUST 引用该条目而不自行复述：判定为**直接执行**（任务数在门槛以下）的运行 MUST NOT 创建 goal 或 team；判定为**交接**的运行 MUST 在 `tasks` U4 之后创建 goal 与 team 并产出交接契约。〔时机的可判定形态见 Clarifications 的 Q5 与 Q10〕
- **FR-040**: 命令运行的创建时机 MUST 同样可判定：命令运行 MAY 在其运行内创建 goal/team，创建时刻 MUST 由命令模板在其自身声明中给出（本特性 MUST 至少为 `/speckit.feedback` 给出该声明），MUST NOT 依赖引擎的隐式副作用，MUST NOT 要求命令运行拥有 spec 目录。
- **FR-041**: 既有 085 的契约测试中钉住 spec-local 落点的用例 MUST 被显式处置（改写为统一落点断言，或标注为历史记录后移除）；本特性 MUST 列出处置清单，MUST NOT 让它们静默失效。处置面 MUST 至少覆盖 A7 已点名的文件清单（以 plan 阶段的检索读数为准，不得只按 A7 抄录），且处置后的全套契约测试必须在 `>=3.8` 上全绿——**移除**只能用于「该用例断言的事实已被本特性删除」的情形，断言仍成立而只是落点变化的用例 MUST 改写而非移除。〔判据见 Clarifications 的 Q11〕
- **FR-042**: 本特性的迁移动作 MUST 在本仓真实数据上干跑一次（只读预演 + 一次实际迁移），并把读数记录为证据；干跑 MUST NOT 删除任何数据。

本节的 `A`–`F` 六个分组是标题，不承载要求条目：分组标题在 clarify 阶段随条目增删保留下来，而**全部 42 条 FR 按执行顺序连续登记在 `A` 之下**，编号 `FR-001`…`FR-042` 未按分组重新切分。重切分组会让编号在不同位置改变含义，代价大于收益，因此本阶段把这一事实写明，而不是留下六个空标题让读者以为分组与编号对应。分组的语义对应（供检索用，不构成第二份清单）：`A` 作用域扩展（FR-001…FR-006、FR-040）、`B` 档案统一与迁移（FR-007、FR-009…FR-013、FR-042）、`C` 平行关系与交接契约（FR-014、FR-016…FR-021、FR-034…FR-036、FR-039）、`D` 概念重定义（FR-002、FR-003、FR-015、FR-022…FR-027、FR-038）、`E` 判定面与取证（FR-005、FR-031…FR-033、FR-041）、`F` 档案层级与运行时豁免（FR-037）。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时——它消费既有的 Python 引擎、既有 pytest 运行器与既有文件系统能力。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库文件系统与路径解析（档案枚举、迁移移动、只读探测） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 中既有的 `requires-python` 声明；本特性零新增第三方依赖 | `pyproject.toml` | 迁移与探测在同一解释器上跑通，路径解析在夹具仓库内可复现 | FR-008, FR-010, FR-011, FR-013 | EP-001 |
| RS-002 | `pytest` 测试运行器（契约测试与夹具仓库断言） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 中既有的 `pytest` 依赖声明；本特性零新增依赖 | `pyproject.toml` | `pytest -m contract` 通过，档案迁移夹具与并发冲突夹具在 `>=3.8` 上执行 | FR-014, FR-039, FR-041 | EP-002 |
| RS-003 | 既有 goal 引擎与声明读取入口的扩展面 | in-scope | 本特性自身修订的 `goal-utils.py` 与 `create-team` 技能 | 不适用（无外部版本面） | `scripts/python/goal-utils.py` | 引擎 `--help` / `--version` 仍满足宪法 XXI，且 `resolve-scope` 的新取值域被契约测试钉住 | FR-001, FR-003, FR-009, FR-026, FR-031 | EP-003 |
| RS-004 | 档案迁移与残余探测的可执行形（一次档案搬移 + 只读扫描） | in-scope | 本特性自身修订的 `goal-utils.py`（复用 RS-003 的文件，不新增可执行体） | 不适用（无外部版本面） | `scripts/python/goal-utils.py` | 迁移与探测的 `--help` / `--version` 与未知选项拒绝满足宪法 XXI；干跑与幂等读数记录在 `test-evidence/` | FR-010, FR-011, FR-012, FR-013, FR-042 | EP-004 |

### Key Entities *(include if requirement involves data)*

- **绑定记录（Binding record）**: 一个 goal 或 team 定义内声明归属的四维记录——`owner`（创建者身份，封闭三值）、`owner_id`（哪个运行）、`origin`（来源 spec 或无）、`lifecycle`（生命周期状态）。归属的唯一回答者；不新增独立存储，作为 definition 的组成部分。读写作用域不是它的字段，而是由它与档案层级按 FR-038 导出。
- **统一档案（Unified archive）**: `.specify/goal/<slug>/` 与 `.specify/teams/<slug>/` 两张既有的框架级档案表——本特性后成为 goal/team 的**唯一**落点。
- **迁移回执（Migration receipt）**: 一次迁移的不可变记录，承载来源 spec、原 slug、目标 slug、时间与结果。archive-not-delete 的承载物；不是当前事实的读取面。
- **残余探测读数（Residual probe reading）**: 只读扫描 `.specify/specs/*/goal|team/` 得到的未迁移余额与逐条路径，用于报告而非写入。
- **档案层级（Archive layer）**: [[STR-002]] 的封闭三行（goal 档案 / team 档案 / 运行临时区）——本特性后所有 definition 归属关系的唯一坐标系；[[STR-006]] 行不是 definition 的落点。
- **归档回执（Archive receipt）**: 一个退役定义迁离原位后留下的不可变记录，落 [[STR-003]]，承载原路径、原 slug、目标 slug、时间与结果；与**迁移回执**的区别在于它按定义一件一份、在档案内可枚举。
- **交接契约（Handoff contract）**: spec 侧交给施工队的设计稿——目标终态、目标/任务集引用、施工领地、验收判据引用、回写要求；落 [[STR-004]]，以 `goal_slug` + [[STR-005]] 引用施工队并被反向引用。唯一所有权在 spec 侧。
- **设计稿与施工（Design vs construction）**: 两条平行线的能力侧——设计师（spec）负责设计与验收，施工队（goal+team）负责执行与回写；二者各自也能独立完成简单工作。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 一个不含 SDD 规格目录的夹具中，命令运行创建的 goal 与 team 全部落在 `.specify/goal/` 与 `.specify/teams/`，且 `.specify/specs/` 下新增路径数为零；把写入路径改回 spec 子目录时该测试转红。 **Path**: final
- **SC-002**: 框架中「写 `.specify/specs/<spec>/goal|team/` 的代码路径」数量为零：以既有写入面（goal 引擎写动作、`create-team` 落盘、驱动者指令）为对象逐条断言，且该断言在把任一写入改回旧路径时转红。 **Path**: final
- **SC-003**: 迁移在本仓真实数据上的干跑产生可判定读数：迁移前残余 N 条（2026-11-09 只读探测实测为 goal 7 条、team 7 条）、迁移后统一档案对应 slug 全部存在、残余探测余额为零、且没有任何源数据被删除（逐条存在性断言）。本条是比较型封闭清单声明，基线取本特性第一个实现提交之前的只读探测读数；本条 MUST NOT 重新断言该总数常量。 **Path**: final
- **SC-004**: 迁移幂等且冲突安全：对同一棵树连跑两次迁移，第二次零写入且退出码可判定；目标 slug 已存在且内容不等价时拒绝覆盖并指名两个候选。两个夹具各自转绿。 **Path**: final
- **SC-005**: 平行性成立：两个夹具——仅 SDD 无 goal/team（以任务数在门槛以下、因而正式不创建 goal/team 的交接判定为形态，见 FR-039）、仅 goal+team 无 spec——各自完成一次交付；在任一线上注入「要求对方存在」的前置检查时测试转红。夹具 MUST NOT 以「跳过创建」伪造平行性，MUST 以判定结果证明「不需要对方」。 **Path**: final
- **SC-006**: 交接契约可判定：越过复杂度门槛的 spec 产出一份 [[STR-004]]，其中 `goal_slug` 与 [[STR-005]] 与 `.specify/goal/<slug>/goal.md`、`.specify/teams/<slug>/team.md` 三向可解析（双向键对，见 FR-034）；未越门槛的 spec 不强制产出。把门槛声明值改成非法值或删除该声明时测试转红。 **Path**: final
- **SC-007**: 交接不变量成立：施工完成后每一条任务状态经回写到达 spec 侧且可核验；施工队直接改写 `tasks.md` / `requirements.md` / `verification.md` 的尝试被 `territory.forbidden` 判定面拒绝（FR-036），拒绝以退出码与拒绝文本取证。把「允许施工队直写任务表」注入实现时测试转红。 **Path**: final
- **SC-008**: 概念替换可判定：对运行时面（`.specify/shared/`、`.specify/skills/`、`.specify/scripts/`、`templates/`、`skills/`、`scripts/`）检索「临时/全局」作为分类判据，命中为零；命中只允许出现在历史记录、迁移回执与本特性规格内。该断言在把任一旧措辞写回某个运行时面时转红（合成变异，不改树上文件）。 **Path**: final
- **SC-009**: 绑定模型自足：同一 goal 定义在改变绑定（owner 由命令运行改为被某个 SDD 运行的 team 引用）前后，定义文件字节与路径不变，归属只由绑定记录回答；把归属推断改成「按目录位置」时测试转红。 **Path**: supporting
- **SC-010**: 085 契约测试处置完整：钉住 spec-local 落点的既有用例逐条有处置记录（改写 / 移除 / 标为历史，移除仅限「所断言的事实已被删除」的用例，见 FR-041），且处置后全套契约测试在 `>=3.8` 上全绿；存在未处置条目时该测试转红。 **Path**: supporting
- **SC-011**: 中断迁移可续做：在「源已移入归档位置、目标尚未落盘」处中断一次迁移，第二次调用 MUST 报告该阶段并完成收尾，且源数据与回执均可枚举——不得二次搬移。把第二次调用改成重新搬移或静默成功时测试转红。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: `tests/contract/` 下新增的命令运行 goal/team 夹具测试，记录夹具树、创建命令、产物路径清单到 `test-evidence/`；变异实测（改回 spec 子目录）一并记录。
- **SC-002 Source**: 对 `scripts/python/goal-utils.py`、`skills/internal/create-team/`、`.specify/skills/sdd-loop-driver/SKILL.md` 与 `references/checkpoint-protocol.md` 的写入面清单 + 一个结构不变量断言（旧路径写入点为 0）；变异实测记录在 `test-evidence/`。
- **SC-003 Source**: 迁移前后各一次只读探测读数（`test-evidence/` 下的探测输出）与迁移回执清单；数据未被删除以逐条存在性断言取证。
- **SC-004 Source**: 幂等夹具与冲突夹具的实测记录：两次运行的退出码、写入计数（第二次为零）、冲突时打印的两个候选。
- **SC-005 Source**: 两个平行性夹具的实测记录（运行命令、退出码、交付物清单）。
- **SC-006 Source**: 门槛两侧各一个夹具 + 声明层取值域的契约测试；变异实测（非法值 / 删除声明行）记录在 `test-evidence/`。
- **SC-007 Source**: 交接夹具中施工队的越权写尝试被拒绝的实测记录（退出码与拒绝文本），以及回写到达 spec 侧的逐条断言。
- **SC-008 Source**: 一个检索型契约测试（程序化扫描，不是人工阅读）；合成变异实测记录在 `test-evidence/`，依据 `docs/reference/history/00-cross-cutting-lessons.md` §「盲检查」——只看措辞的绿不构成证据。
- **SC-009 Source**: 绑定变更前后同一定义的哈希对照与归属查询输出，记录在 `test-evidence/`。
- **SC-010 Source**: 085 契约测试文件清单与逐条处置表（写入 `feature-ref.md` 或本规格的处置节），加上处置后的 `pytest -m contract` 读数。
- **SC-011 Source**: `test-evidence/` 下的中断迁移夹具复现记录（中断点、第二次调用的退出码、回执路径与源数据存在性断言）。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"binding"` | FR-002, FR-010, FR-023, FR-025 |
| `STR-002` | `"archive-scope"` | FR-007, FR-009, FR-025, FR-037, FR-038 |
| `STR-003` | `".specify/archive/goal-team/"` | FR-010, FR-029 |
| `STR-004` | `"handoff.md"` | FR-034, FR-035, SC-006 |
| `STR-005` | `"team_slug"` | FR-034, FR-016, SC-006 |
| `STR-006` | `".tmp"` | FR-037 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

### Session 2026-11-09（无人值守 clarify，自行裁决并记录）

- **编号重排（本会话）**: 本会话新增 5 条要求与 1 条成功判据，为消除 letter-suffix 形态，尾部编号整体后移。旧→新映射（`FR`，逐条列出，未列出者编号不变）: FR-005a→FR-006, FR-006→FR-007, FR-007→FR-008, FR-008→FR-009, FR-009→FR-010, FR-010→FR-011, FR-011→FR-012, FR-012→FR-013, FR-013→FR-014, FR-014→FR-015, FR-015→FR-016, FR-016→FR-017, FR-017→FR-018, FR-018→FR-019, FR-019→FR-020, FR-020→FR-021, FR-021→FR-022, FR-022→FR-023, FR-023→FR-024, FR-024→FR-025, FR-025→FR-026, FR-026→FR-027, FR-027→FR-028, FR-028→FR-029, FR-029→FR-030, FR-030→FR-031, FR-031→FR-032, FR-032→FR-033, FR-033→FR-034, FR-034→FR-035, FR-035→FR-036, FR-036→FR-037, FR-037→FR-038, FR-038→FR-039, FR-039→FR-040, FR-040→FR-041, FR-041→FR-042, FR-042（新增，无旧号）；`SC-001`…`SC-011` 编号不变。映射之后的 live 引用已按此表机械改写，`## Clarifications` 内的历史行不改写。
> **本节两处编号的判读规则**: 上面这一行是全量的 `FR` 旧→新映射；其余各 Q/A 行末尾括号里的编号是**本会话结束时**的 live 编号（已按该映射改写），不是重排前的编号。`FR-005a` 等 letter-suffix 形态已不存在。

- Q: 一个 goal 同时属于一条 spec、又在某个 team 里被调用，归属应由哪一维回答？ → A: 归属拆成两维：`owner` + `owner_id` 回答「谁发起的哪个运行」，`origin` 回答「源自哪个 spec 目录（或 null）」；旧的单一 `owner` 无法同时表达这两件事，会把「被 spec 派生」误读成「属于 spec」，这正是用户要消除的从属关系。（FR-002、FR-023、Key Entities）
- Q: `--scope global|spec|auto` 与新模型的字面冲突怎么处置——保留取值名改含义，还是删取值让旧调用失败？ → A: 删除 `spec` 取值（旧调用以引擎既有的 `invalid choice` 退出 2 失败），保留 `global` / `auto` 并收窄其含义；`--spec-dir` 保留为 `origin` 与 `auto` 有效性的输入，不再决定落点。理由：本特性的核心命题就是「位置不再决定归属」，保留一个与位置同名的取值会让从属关系以另一种名字回流；一次性可判定失败比长期别名更省后续梳理成本。（FR-008）
- Q: 迁移时「内容不等价」按什么判？绑定行是不是要在比较里？ → A: 只比概念载荷（Objective / Success Criteria / Lifecycle status / Targets 文本），绑定行（[[STR-001]]）排除在外。理由：迁移自己就要往目标文件写入绑定行，若绑定行参与比较，迁移完的档案与其自身来源永远「不等价」，幂等（SC-004）随之不可达。（FR-011）
- Q: 交接契约在哪个阶段产出——plan 还是 tasks？ → A: tasks 阶段，在复杂度判定之后、`implement` 之前产出。理由：契约要承载「任务集引用」，而任务集在 tasks 之前根本不存在；放在 plan 会迫使契约复制一份任务清单，直接违反 FR-020 的唯一所有权。（FR-016、FR-035、FR-039）
- Q: 复杂度门槛落在哪个声明面、边界值怎么算、哪些运行形态会创建 goal/team？ → A: 落 `shared/declarations/facts/` 的一个条目，取「任务数」阈值，边界按「任务数 > 阈值」为复杂（等于阈值仍是简单，见 Edge Cases）；交接判定同时是 goal/team 的创建时机：直接执行的运行不创建，交接的运行在 tasks U4 后创建，命令运行由命令模板声明其创建时刻。（FR-018、FR-031、FR-039、FR-040）
- Q: 「读写作用域」原为第三维度、且旧规则用「团队不得写 `.specify/goal/**` / `.specify/teams/**`」的禁令表达——这条禁令在新模型下还成立吗？ → A: 不成立，必须替换。旧禁令的作用是防止一次运行污染共享档案；机制换成一条可判定的函数：team 档案由该 team 的 owner 身份独立可写；goal 档案只要被任意档案层的某个 team 绑定，就只有 `human`（`/speckit.goal`）能改写。引擎取值面随之改为档案层级（[[STR-002]]）+ 绑定维度，`spec` 成员消失。（FR-023、FR-038、FR-025）
- Q: 路由层 carve-out 改写时，原有的层级禁令保留哪一条？ → A: 保留「一次 SDD 运行 MUST NOT 创建/重绑/改范围/终止共享档案中的既有定义」，只把「运行可在自己 spec 下创建设定」改为「运行可创建 `owner: sdd-run` 的定义，档案落 [[STR-002]]」。理由：作用域迁移不得顺手放松层级治理，否则任何运行都能改写别人的 goal。（FR-028）
- Q: 迁移与残余探测的命令入口归谁——`/speckit.goal` 还是 `/speckit.sanitize`？ → A: 归 `/speckit.goal` 的新 `migrate-archive` 模式（goal 与 team 一并处理，因为 goal 引擎已是 goal 档案的唯一写入口），`/speckit.sanitize` 只做只读探测。理由：sanitize 的职责是材料整理，不持有 goal 档案写权限，让它搬档案会制造第二个写入口（违反 FR-008 的单一落点纪律）。（FR-030、FR-012）
- Q: 两个新声明条目除了新增文件还要做什么？ → A: 必须在 `shared/declarations/contract.yaml` 登记 subset id 与值域，且消费点落在本特性新增/修改的引擎里，不得要求改既有 `flow-class-check.py` 或驱动脚本。理由：未登记条目在读入口处按 `owner-unavailable` 处理，等于声明写了个不生效的条目——这会被「绿了但不生效」的检查掩盖。（FR-031）
- Q: goal 的创建时机在「只有 goal 无 team」和「有 team」两种形态下怎么定？ → A: 时机由复杂度判定统一决定（FR-039）：直接执行的 SDD 运行不创建 goal/team；交接的运行在 tasks U4 后创建两者；「有 team 没 goal」不是合法形态（team MUST 绑定一个 goal，N teams : 1 goal）。命令运行的创建时刻由命令模板声明。（FR-039、FR-040）
- Q: 既有 085 测试哪些可以移除？ → A: 只有「断言的事实已被本特性删除」的用例可移除（例如 `--scope spec` 仍写入 spec 子目录），断言仍成立而只是落点变化的用例必须改写为 [[STR-002]] 断言，并逐条留处置记录。理由：移除一个仍成立的事实等价于让 085 的守卫静默消失。（FR-041、SC-010）
- Q: 框架里还有一处 `temporary`（`.specify/.tmp/` 运行临时区）——它算不算本特性要清理的「临时」概念？ → A: 不算，且不得被波及。运行临时区是既有的既定时点（`shared/guidelines/temp-directory-discipline.md`），与 goal/team 的归属分类无关；本特性只在其概念 owner 处加一行「不是档案层级」，MUST NOT 对 `scan-temp-usage.py` 的既有词面做字面替换。（FR-037）
- Q: 状态脊上的 `temp_goal_slug` / `temp_team_slug` / `temp_scope_spec_dir` 与驱动者正文的 `Temporary Goal/Team` 怎么迁移？ → A: 正文改写为新模型表述，旧键由 goal 引擎提供一次性迁移别名（读旧写新，移除点在 plan 声明），并让旧键在任何一处失效都是可判定的，而不是被静默丢弃。（FR-028）

### Session 2026-11-09（analyze-repair，自行裁决并记录）

- Q（H-02）：同一份取值集在三处出现三种写法——FR-008 + plan T-004 写 `{global, auto}`，契约 C-9 + `.specify/memory/features/092.md` 写 `{goal, teams, auto}`，live 引擎 `goal-utils.py:1312` 写 `("global", "spec", "auto")`。哪一个是对的，其余怎么处置？ → A: 以 **`goal` / `teams` / `auto`** 为唯一答案，唯一 owner 是 FR-025（本条新增为封闭三成员并以 `choices=` 为实现投影）；`global` 与 `spec` 一并出域。判据不是投票而是**语义**：`global` 是 085 的「全局档案」单数概念，本特性把它拆成两条并列档案行（[[STR-002]]），一个叫 `global` 的成员会同时指向两行、每回调用都要再猜一层；而 `{global, auto}` 两成员集根本表达不出「写 goal 档案」与「写 team 档案」两条写目标（C-13 要求写入必须点名档案行）。因此 Q2 里「保留 `global` / `auto`」的措辞应读作「保留两**行档案**语义」，改名后即 `goal` / `teams`；契约 C-9、`features/092.md`、plan T-004 与 quickstart 的 `--scope goal` 均已一致，本阶段只改 FR-008 / FR-025 / 假设 A1 三处正文。（FR-008、FR-025、A1）
- Q（H-01）：GATE-6 的命令写作 `account-clause-coverage.py --spec-dir …`，而该命令实测 `fr-uncovered` fail 26/42 且退出 1；是把 111 条条款的引注组改写，还是让 GATE-6 只声明它真正判定的车道？ → A: **改写引注组**，不改判据语义。判据 owner（`shared/definitions/contract-clause-definitions.md` § 引用组）把「条款引用了哪条 FR」定义为条款块内**最后一个**含编号的括号组，而本特性把 FR 写在块首括注里、块尾不再有引用组，于是每条条款都被记为「未引用」——这是引注形式缺陷，不是覆盖缺失（`pre-analyze-check --stage tasks` 的 FR 车道 42/42、`feature-ref.md` § FR → clause map 42/42 均可证）。取真判据的代价是 111 条各加/移一个括号组；降判据的代价是让一条真检查从此只看它想看的部分。同族 spec 090（10/10）与 091（28/28）在该判据下都满覆盖，证明判据可实现。（FR-033、SC-006、SC-010）

## Notes

### Assumptions 双段合并（H-03 / H-04，2026-11-09 analyze-repair）

本文件的 `## Assumptions` 曾有两个并列段（clarify 段与 requirements 段各写一份 A1–A8，共 19 行 / 11 个不同 id）。
`validate-requirements.py` 的 `dup-id` 只匹配 `FR|SC`，因此重复了整轮 checklist 与 analyze 都没被门禁抓到。
本阶段按**差集**合并，逐条保留、绝不删除：

- **seg1 \ seg2（只在 clarify 段出现的内容，已并入合并段）**: A1 的「已由 clarify 裁定」形态；A2 的 `FR-006`/`FR-031` 双引；A3 的 `FR-018 / FR-031`；A4 的 `RS-003、RS-004` 与 `FR-024`；A5 的 `FR-009` / `FR-030` / `FR-012`；A6 的探测文件路径与「088 / 089 的 team slug 偏离目录名」；A7 的「plan R-28 实测 11 个模块」；A9 / A10 / A11 三条（段 2 完全没有）。
- **seg2 \ seg1（只在 requirements 段出现的内容，已并入合并段）**: A6 的枚举范围「085–091」（段 1 误写 085–090，差 091 一条）；A6 的「089 的 goal slug 为 `script-interface-contract`」措辞。
- **两段一致、合并后只留一份**: A2 / A3 / A5 / A7 / A8 的正文主体。

处置同时修掉三处误引与一处矛盾：A2 误引 `FR-007、FR-032` → `FR-006、FR-031`；A3 误引 `FR-019 / FR-032` → `FR-018 / FR-031`；A4 误引 `FR-025` → `FR-024`、`RS-004` → `RS-003、RS-004`；A5 误引 `FR-010` / `FR-031` / `FR-013` → `FR-009` / `FR-030` / `FR-012`。
矛盾项（段 2 的 A1 写「本阶段不裁 scope 取值名，只钉死必须显式处置」，与已裁决的 FR-008 及段 1 的 A1 直接冲突）以 clarify 裁决为准保留一份，段 2 的 A1 文本作为**已被取代读法**记录在本节而不保留在正文——这是唯一一处内容不并入合并段落的位置，理由是它断言的事实已被判决删除，保留会让读者看到两条互斥的现行规则。

本阶段同时补齐两处 analyze 指出的口径缺口：A11 的「迁移 MUST NOT 重建谱系」原先只在假设里出现、无 FR 承载，现由 FR-009 正文承载（A11 只留理由）；A6 的枚举范围统一为「085–091」。

### 同批处置的其余发现（2026-11-09 analyze-repair）

- **M-01 / H-04（A6 范围与误引）**: 见上节，合并段取 `085–091`（7 + 7，实测）。
- **M-02（FR-005 的过期指针）**: `见 FR-032` → `见 FR-031`（声明层条目的 owner 是 FR-031）。
- **M-03 / C-01（命令族判别子）**: FR-006 与 A9 一并改为 `source: ledger` vs `source: default`；FR-006 载实测对照（`/speckit.feedback`、`/speckit.plan` = `ledger`；`/speckit.nonexistentcommand` = `default`），A9 只留理由与「未声明 = 不入族」的裁定。
- **M-04（A11 无 FR 承载）**: 已由 FR-009 承载，见上节。
- **M-05（FR-041 双引 A7）**: 原 FR-041 在正文里两次点名 A7（「至少覆盖 A7 已点名的文件清单…不得只按 A7 抄录」），是 H-03 中**爆炸半径最大**的一处——一旦按重复块整段处置掉其一，这条不可逆的 085 测试移除就失去它唯一的清单锚点。合并后 A7 只剩一条，FR-041 的两次点名指向同一目标，语义不变；本阶段不改写 FR-041 正文，只把这件事记录在此。
- **L-01（B–F 空分组）**: 六个分组标题保留，`A` 段末补一句「全部 42 条 FR 连续登记在 A 之下、分组只是标题」的事实，避免读者以为编号与分组对应。


## Assumptions

`A1`–`A8` only; `A9`–`A11` are the clarify-stage additions that follow. Two blocks had accumulated here (a
clarify-written block and an older requirements-written block); the merge rule and the two diffs it consumed are
recorded in § Notes → 「Assumptions 双段合并」 so the consolidation is auditable rather than silent.

- **A1（scope 取值名已由 clarify 裁定，不再是待选项）**: 原 A1 把 `--scope` 的两种处置推给 plan。clarify 已裁为「删除 `spec` 取值」，并在本阶段把保留行的取值名钉为 `goal` / `teams`（连同 `auto` 共三成员，唯一 owner 是 FR-025，见 Clarifications 的 Q13）；依据见 Clarifications 的 Q2。实现面（既有 scope 测试的改写清单）仍归 plan/implement 排布。
- **A2（`/speckit.feedback` 作为首个取证命令，不新增命令）**: 用户点名 `/speckit.feedback`；本特性把它作为命令族扩展的取证实例，但**不新增任何 `/speckit.*` 命令**（状态脊 `non_goals` 已声明）。命令族判定方式由声明层条目 + 既有类别读取入口给出（FR-006、FR-031），取证只覆盖 feedback 一条链。
- **A3（「62 个任务」是用户举的例子，不是门槛常量）**: 用户原文以「前面的 implement 阶段有 62 个任务」为例说明复杂度。本规格把它当**例子**而非门槛：门槛取值由 FR-018 / FR-031 的声明层条目给出，本阶段不发明具体数字。
- **A4（不新建引擎、不新建文档 owner）**: 概念 owner 是既有的 `goal-definitions.md` 与 `conceptual-model.md`（FR-024），迁移与探测以扩展既有 `goal-utils.py` 的方式落地（RS-003、RS-004、宪法 XII / IX）。若实现期证明需要独立可执行体，它必须同时满足宪法 XXI 的 `--help` / `--version` 与未知选项拒绝——这一点与 091 的做法一致。
- **A5（迁移不强制，先探测）**: 迁移是显式动作而非启动时副作用：无人值守运行在未迁移仓库里 MUST NOT 自动搬动档案（那是无人值守的破坏性动作）。因此 FR-009 的迁移动作是**被调用的**（入口见 FR-030），FR-012 的探测是**只读的**；本特性的干跑（FR-042）由本特性的运行自行发起。
- **A6（实测基线读数，取自 requirements 阶段）**: 2026-11-09 只读探测（`.specify/specs/092-goal-team-parallel/test-evidence/requirements-baseline-probe.txt`）：`.specify/specs/*/goal/*/goal.md` 共 7 条、`.specify/specs/*/team/*/team.md` 共 7 条（085–091 各一对；089 的 goal slug 为 `script-interface-contract` 而非目录名，088 / 089 的 team slug 亦偏离目录名；092 自身的 spec-local goal 在本特性落地后计入残余）。SC-003 引用该读数作为**比较基线**；按 091 的教训，本规格 MUST NOT 把该数字复制为第二处固定值——计数与枚举只在本条与 SC-003 的基线引用处出现。
- **A7（既有测试的处置是义务，不是可选项）**: FR-041 要求的处置清单必须先列全再动手；`tests/contract/test_scope_resolution.py`、`test_temp_goal_contract.py`、`test_temp_team_schema.py`、`test_team_command_routing.py`、`test_goal_writeset.py`、`test_goal_migration.py`、`test_goal_targets_engine.py`、`test_goal_definition.py` 与 `tests/unit/test_goal_scope_engine.py`、`test_goal_utils.py` 都含 spec-local 断言或 scope 断言，实际处置面以 plan 阶段的检索读数为准（A7 是起点，不是清单；plan-phase R-28 实测为 11 个模块，其中 `test_goal_writeset.py` 只有一处非断言命中）。
- **A8（本特性自身的收口受同样约束）**: 本阶段提交只含本特性产物、按显式路径、不 push——迁移机制尚未落地，本特性自己的运行仍按手工步骤完成，并把这件事实记录在此以免被误读为「机制已生效」。
- **A9（未声明类别的命令按「不入族」处理）**: FR-006 用「载体文件是否在 `flow-class-classes.yaml` 中登记了类别」判定命令族，判别子是类别读取入口输出里的 `source` 字段——`source: ledger`（登记表里有自己的条目）入族，`source: default`（有序清单第 0 个成员的兜底）不入族；`flow_class` 取值与退出 0 都不是判别子（`/speckit.nonexistentcommand` 同样退出 0 并返回 `flow_class: execution`，见 FR-006 的实测）。本阶段裁为「未声明 = 不入族」，理由是判定必须可由既有读入口回答，猜一个白名单会重新引入逐命令硬编码。若后续确需让某个入口层命令入族，正确做法是给它登记类别，而不是改本判据。
- **A10（绑定改成可写性的确定性函数，不靠禁令）**: 旧规则用「forbidden paths」表达「运行不得写共享档案」。本阶段裁为可判定函数（FR-038）：被任意 team 绑定的 goal 只能由 `human` 改写。边界情形——同一个 goal 被另一条线的 team 绑定时，原 `owner` 失去写权——是**有意接受**的代价：它把「谁的档案」变成可枚举的事实，而不是依赖禁令文本。
- **A11（`origin` 只记直接来源，不建谱系）**: 迁移后的定义 `origin` 记录**直接来源 spec**；一条被迁移的 team 若其 `goal_slug` 指向也被迁移的 goal，迁移 MUST NOT 试图重建跨定义的历史谱系。理由：谱系不是本特性的诉求，且它会让「重跑迁移是否等价」变得不可判定。该禁令的规范面由 FR-009 承载（迁移 MUST NOT 重建谱系），本条只记理由。
