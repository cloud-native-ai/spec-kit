# Requirements Specification: goal/team 与 spec 的平行关系（重定义 085 的作用域与绑定模型）

**Requirement Branch**: `092-goal-team-parallel`
**Created**: 2026-11-09
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（修订 085 引入的 goal/team 机制、`goal-utils.py`、`create-team` / `run-team`、驱动者 § Temporary Goal/Team 与 checkpoint 协议的作者）、下游项目里同时使用 `/speckit.*` 命令与 SDD 演进流程的项目维护者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 在判定「一次运行能否拥有 goal 与 team」「goal/team 的档案落在哪里」「spec 与 goal+team 谁附属谁、交接发生在哪」时打开本规格，据 FR-001…FR-035 与 SC-001…SC-010 决定 `/speckit.plan` 与后续实现是否放行
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
- **FR-002**: 一个命令运行的 goal/team MUST 通过**[[STR-001]] 记录**声明其归属运行，该记录 MUST 至少承载 `owner`（创建者身份：SDD 运行 / 命令运行 / 人工）与 `lifecycle`（生命周期状态）；缺失绑定记录的定义 MUST 被引擎判为不可解释，而不是被默认为任一归属。
- **FR-003**: 绑定记录的写入 MUST 经 goal 引擎（`resolve-scope` 之外的写动作）与 team 机制完成，MUST NOT 由命令模板、技能或驱动者直接改写 `goal.md` / `team.md` 的绑定字段。
- **FR-004**: 命令运行创建的 goal/team MUST 能在该运行结束后独立成立——即其可读性 MUST NOT 依赖该运行仍在进行；一次运行结束 MUST NOT 使档案失效或消失。
- **FR-005**: 框架 MUST 给出一个**封闭的命令族清单判定方式**：一个命令是否可拥有 goal/team，MUST 由其声明的类决定，MUST NOT 由逐命令硬编码的白名单决定；本特性 MUST 覆盖 `/speckit.feedback` 作为首个取证命令。〔绑定类声明 owner 见 FR-030〕

#### B. 档案统一与迁移

- **FR-006**: goal 与 team 的**唯一**写入落点 MUST 是 `.specify/goal/<slug>/` 与 `.specify/teams/<slug>/`；框架 MUST NOT 在 `.specify/specs/` 下产生任何 goal 或 team 的新写入路径。
- **FR-007**: goal 引擎的 `resolve-scope` MUST 不再返回 spec-local 的 goal/team 根；其作用域取值域 MUST 由本特性重定义（见 FR-024），且既有 `--scope global|spec|auto` 的**字面冲突** MUST 被显式处置——要么保留取值名而改其含义并给出迁移期别名，要么删除取值并让旧调用以可判定的错误失败；两种处置 MUST 在 plan 阶段裁为一种并记录。〔本阶段不预裁，见假设 A1〕
- **FR-008**: 框架 MUST 提供一个**幂等的迁移动作**，把既有 `.specify/specs/<spec>/goal/<slug>/goal.md` 与 `.specify/specs/<spec>/team/<slug>/team.md` 迁入统一档案；迁移 MUST 保留原 slug、原定义内容与 lifecycle 状态，并把「来源 spec」记入 [[STR-001]] 记录。
- **FR-009**: 迁移 MUST 是 archive-not-delete（该事实 MUST 同时写入每一份 [[STR-001]] 记录）：源路径的数据 MUST NOT 被删除，MUST 被移入归档位置并留下指名「来源 spec / slug / 关联目标档案」的回执；迁移失败 MUST 报告失败阶段，MUST NOT 留下无回执的删除。
- **FR-010**: 迁移 MUST 在冲突时停下：目标 slug 已存在且内容不等价时，迁移 MUST 拒绝覆盖并指名两个候选，MUST NOT 择一胜出。
- **FR-011**: 框架 MUST 提供**只读残余探测**：报告仍存在于 `.specify/specs/*/goal|team/` 的未迁移余额，并 MUST NOT 把残余当作当前档案读取或写入。
- **FR-012**: 迁移完成后 MUST 不存在第二条写入路径：本特性 MUST 以契约测试钉住「写 `.specify/specs/<spec>/goal|team/` 的代码路径数量为零」这一条，MUST NOT 只以文档措辞断言。

#### C. 平行关系与交接契约

- **FR-013**: spec（SDD 流程）与 goal+team MUST 是**平行**执行线：任一条线 MUST 能在对方不存在的前提下独立完成一次交付，框架 MUST NOT 设置「必须先有对方」的前置检查。
- **FR-014**: 一个 goal 的归属 MUST 只由绑定记录回答；框架 MUST NOT 从目录位置推断归属，MUST NOT 保留任何「在 spec 下即属于 spec」的推断规则。
- **FR-015**: 本特性 MUST 定义一个**交接契约（handoff contract）**制品：它把 spec 侧的设计结果显式交给 goal+team 施工，MUST 至少承载：目标终态、目标集（Targets）或任务集引用、施工领地（可写路径集）、验收判据引用、以及回写要求。
- **FR-016**: 交接契约的**所有权** MUST 唯一：设计稿由 spec 侧产出与修订，施工队 MUST NOT 改写其设计面；施工队 MUST 只能向 spec 侧提交补丁与状态回写。
- **FR-017**: 复杂工作的判定 MUST 可判定：是否走「spec 设计 + goal+team 执行」MUST 由一条**声明值**决定（例如任务数门槛），MUST NOT 由运行期自由裁量；门槛取值 MUST 有唯一 owner 并在边界值上有确定行为。
- **FR-018**: 在交接模式下，`requirements.md`、`tasks.md`、`verification.md` MUST 仍由 spec 侧唯一持有；施工队 MUST NOT 直接改写这三件制品。
- **FR-019**: 施工完成后 MUST 有**回写路径**：每一条任务的完成状态 MUST 能到达 spec 侧并被判定，回写 MUST 可核验（指名来源运行与证据指针），MUST NOT 以口头/摘要形式替代。
- **FR-020**: 两条线 MAY 同时运行于同一仓库；框架 MUST 在并发形状下保持档案可判定——同一 slug 的第二创建 MUST 被拒绝并指名冲突（见 Edge Cases），MUST NOT 以路径不同（旧落点 vs 新落点）为由允许并存。

#### D. 概念重定义：绑定 / 作用域 / 生命周期

- **FR-021**: 框架 MUST 停止把「临时（temporary）」与「全局（global）」用作 goal/team 的分类判据；这一对词 MUST 只允许出现在历史记录、迁移回执与本特性的规格内，MUST NOT 出现在任何运行时判定面。
- **FR-022**: 替换模型 MUST 至少由三个可判定维度构成：`owner`（谁创建：SDD 运行 / 命令运行 / 人工）、`lifecycle`（`active` / `achieved` / `abandoned`，沿用既有封闭三值）、以及**读写作用域**（谁能写、谁只读）；每个维度 MUST 有封闭取值域与唯一 owner，三者合起来即该定义的 [[STR-001]]。
- **FR-023**: 概念的**唯一 owner** MUST 是既有的定义文档：goal 侧 `.specify/shared/definitions/goal-definitions.md`、team 侧 `.specify/skills/internal/create-team/references/conceptual-model.md`；本特性 MUST 改写这两处而非新建第三处，且其他面 MUST 只引用不复述（宪法 XIV）。
- **FR-024**: 引擎的作用域取值 MUST 由重定义后的模型重新给出；取值名 MUST 表达 owner 与读写权限而不是位置，且 MUST 有单一 owner 文档；取值域内 MUST NOT 出现以目录位置命名的成员，新取值只表达 [[STR-001]] 维度而不再表达位置。
- **FR-025**: 三条既有全局约束 MUST 被显式重述为新模型的推论而不是被删除：(a) 一个 goal 档案的终态保留（不删除）；(b) N teams : 1 goal 的一向身份引用（team 只存 `goal_slug`，不存 goal 内容副本）；(c) 终态 goal 拒绝新绑定。〔这三条各自有既有 owner，本特性 MUST 引用而非复制其规范文本〕
- **FR-026**: 本特性 MUST 更新路由层的 carve-out：`.specify/shared/definitions/sdd-routing-definitions.md` 中「Temporary run-scoped scopes」段落所描述的 spec-local 许可 MUST 被替换为平行模型下的许可，且 MUST NOT 在改后文本里保留「Temporary」作为判据名。
- **FR-027**: 驱动者协议 MUST 同步：`.specify/skills/sdd-loop-driver/SKILL.md` § Temporary Goal/Team 与 `references/checkpoint-protocol.md` 的 goal 相关段落 MUST 改写为新模型下的表述（goal 何时创建、写入何处、以何绑定），且 SDD 阶段链与哨兵 MUST 保持不变。
- **FR-028**: 目录地图 MUST 同步：`.specify/shared/definitions/framework-map.md` 的 Goals / Teams 两行 MUST 表达新的落点与归档语义；`.specify/specs/` 行 MUST NOT 再暗示其下存在 goal/team。
- **FR-029**: `templates/commands/goal.md` 与 `templates/commands/team.md` 的作用域说明 MUST 改为引用新模型 owner，MUST NOT 复述取值域。

#### E. 判定面与取证

- **FR-030**: 可拥有 goal/team 的命令族判定，与交接复杂度门槛，二者 MUST 各有一个**声明层**条目（`shared/declarations/facts/`），且 MUST 由现有声明读取入口消费；MUST NOT 在脚本内硬编码第三处取值。
- **FR-031**: 本特性 MUST 在框架源码侧落地并镜像同步；`templates/` 的框架模板中立性 MUST 保持（MUST NOT 写入本仓专有路径事实）。
- **FR-032**: 本特性 MUST 为 User Story 1–5 中每一个「可判定」断言提供契约级或单元级测试，且每条测试 MUST 在实现缺失时转红；只有文档措辞变化的检查 MUST NOT 被计为取证。
- **FR-033**: SPEC（SDD）侧的 goal/team 创建时机 MUST 在新模型下被重新给出：FR-027 的改写 MUST 明确「一次 SDD 运行何时创建 goal、何时创建 team」，MUST NOT 保留旧目录落点作为时机的依据。
- **FR-034**: 既有 085 的契约测试中钉住 spec-local 落点的用例 MUST 被显式处置（改写为统一落点断言，或标注为历史记录后移除）；本特性 MUST 列出处置清单，MUST NOT 让它们静默失效。
- **FR-035**: 本特性的迁移动作 MUST 在本仓真实数据上干跑一次（只读预演 + 一次实际迁移），并把读数记录为证据；干跑 MUST NOT 删除任何数据。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时——它消费既有的 Python 引擎、既有 pytest 运行器与既有文件系统能力。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库文件系统与路径解析（档案枚举、迁移移动、只读探测） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 中既有的 `requires-python` 声明；本特性零新增第三方依赖 | `pyproject.toml` | 迁移与探测在同一解释器上跑通，路径解析在夹具仓库内可复现 | FR-006, FR-008, FR-009, FR-011 | EP-001 |
| RS-002 | `pytest` 测试运行器（契约测试与夹具仓库断言） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 中既有的 `pytest` 依赖声明；本特性零新增依赖 | `pyproject.toml` | `pytest -m contract` 通过，档案迁移夹具与并发冲突夹具在 `>=3.8` 上执行 | FR-012, FR-032, FR-034 | EP-002 |
| RS-003 | 既有 goal 引擎与声明读取入口的扩展面 | in-scope | 本特性自身修订的 `goal-utils.py` 与 `create-team` 技能 | 不适用（无外部版本面） | `scripts/python/goal-utils.py` | 引擎 `--help` / `--version` 仍满足宪法 XXI，且 `resolve-scope` 的新取值域被契约测试钉住 | FR-001, FR-003, FR-007, FR-024, FR-030 | EP-003 |

### Key Entities *(include if requirement involves data)*

- **绑定记录（Binding record）**: 一个 goal 或 team 定义内声明归属的三维记录——`owner`（创建者身份）、`lifecycle`（生命周期状态）、读写作用域（谁能写、谁只读）。归属的唯一回答者；不新增独立存储，作为 definition 的组成部分。
- **统一档案（Unified archive）**: `.specify/goal/<slug>/` 与 `.specify/teams/<slug>/` 两张既有的框架级档案表——本特性后成为 goal/team 的**唯一**落点。
- **迁移回执（Migration receipt）**: 一次迁移的不可变记录，承载来源 spec、原 slug、目标 slug、时间与结果。archive-not-delete 的承载物；不是当前事实的读取面。
- **残余探测读数（Residual probe reading）**: 只读扫描 `.specify/specs/*/goal|team/` 得到的未迁移余额与逐条路径，用于报告而非写入。
- **交接契约（Handoff contract）**: spec 侧交给施工队的设计稿——目标终态、目标/任务集引用、施工领地、验收判据引用、回写要求。唯一所有权在 spec 侧。
- **设计稿与施工（Design vs construction）**: 两条平行线的能力侧——设计师（spec）负责设计与验收，施工队（goal+team）负责执行与回写；二者各自也能独立完成简单工作。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 一个不含 SDD 规格目录的夹具中，命令运行创建的 goal 与 team 全部落在 `.specify/goal/` 与 `.specify/teams/`，且 `.specify/specs/` 下新增路径数为零；把写入路径改回 spec 子目录时该测试转红。 **Path**: final
- **SC-002**: 框架中「写 `.specify/specs/<spec>/goal|team/` 的代码路径」数量为零：以既有写入面（goal 引擎写动作、`create-team` 落盘、驱动者指令）为对象逐条断言，且该断言在把任一写入改回旧路径时转红。 **Path**: final
- **SC-003**: 迁移在本仓真实数据上的干跑产生可判定读数：迁移前残余 N 条（2026-11-09 只读探测实测为 goal 7 条、team 7 条）、迁移后统一档案对应 slug 全部存在、残余探测余额为零、且没有任何源数据被删除（逐条存在性断言）。本条是比较型封闭清单声明，基线取本特性第一个实现提交之前的只读探测读数；本条 MUST NOT 重新断言该总数常量。 **Path**: final
- **SC-004**: 迁移幂等且冲突安全：对同一棵树连跑两次迁移，第二次零写入且退出码可判定；目标 slug 已存在且内容不等价时拒绝覆盖并指名两个候选。两个夹具各自转绿。 **Path**: final
- **SC-005**: 平行性成立：两个夹具——仅 SDD 无 goal/team、仅 goal+team 无 spec——各自完成一次交付；在任一线上注入「要求对方存在」的前置检查时测试转红。 **Path**: final
- **SC-006**: 交接契约可判定：越过复杂度门槛的 spec 产出一份交接契约并被 goal 与 team 共同引用；未越门槛的 spec 不强制产出。把门槛声明值改成非法值或删除该声明时测试转红。 **Path**: final
- **SC-007**: 交接不变量成立：施工完成后每一条任务状态经回写到达 spec 侧且可核验；施工队直接改写 `tasks.md` / `requirements.md` / `verification.md` 的尝试被拒绝。把「允许施工队直写任务表」注入实现时测试转红。 **Path**: final
- **SC-008**: 概念替换可判定：对运行时面（`.specify/shared/`、`.specify/skills/`、`.specify/scripts/`、`templates/`、`skills/`、`scripts/`）检索「临时/全局」作为分类判据，命中为零；命中只允许出现在历史记录、迁移回执与本特性规格内。该断言在把任一旧措辞写回某个运行时面时转红（合成变异，不改树上文件）。 **Path**: final
- **SC-009**: 绑定模型自足：同一 goal 定义在改变绑定（owner 由命令运行改为被某个 SDD 运行的 team 引用）前后，定义文件字节与路径不变，归属只由绑定记录回答；把归属推断改成「按目录位置」时测试转红。 **Path**: supporting
- **SC-010**: 085 契约测试处置完整：钉住 spec-local 落点的既有用例逐条有处置记录（改写 / 移除 / 标为历史），且处置后全套契约测试在 `>=3.8` 上全绿；存在未处置条目时该测试转红。 **Path**: supporting

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

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"binding"` | FR-002, FR-009, FR-022, FR-024 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

## Assumptions

- **A1（本阶段不裁 scope 取值名，只钉死「必须显式处置」）**: FR-007 要求把 `--scope global|spec|auto` 与新模型的字面冲突显式处置，但两种处置（保留取值名改含义 + 迁移期别名 / 删除取值并让旧调用可判定失败）各自都有一批既有测试与文档要跟着改。本阶段**不替 plan 做这个选择**，只要求 plan 阶段裁为一种并记录依据。理由：这是承重决策（影响既有 7 个档案的读写与全部 scope 测试），由具备完整实现视野的阶段裁定更合适。
- **A2（`/speckit.feedback` 作为首个取证命令，不新增命令）**: 用户点名 `/speckit.feedback`；本特性把它作为命令族扩展的取证实例，但**不新增任何 `/speckit.*` 命令**（状态脊 `non_goals` 已声明）。命令族判定方式由声明层给出（FR-030），取证只覆盖 feedback 一条链。
- **A3（「62 个任务」是用户举的例子，不是门槛常量）**: 用户原文以「前面的 implement 阶段有 62 个任务」为例说明复杂度。本规格把它当**例子**而非门槛：门槛取值不在此写死，由 FR-017 要求的声明层条目给出，本阶段不发明具体数字。
- **A4（不新建引擎、不新建文档 owner）**: 概念 owner 是既有的 `goal-definitions.md` 与 `conceptual-model.md`（FR-023），迁移与探测的确定性部分以扩展既有 Python 引擎的方式落地（宪法 XII / IX）。若实现期证明需要独立可执行体，它必须同时满足宪法 XXI 的 `--help` / `--version` 与未知选项拒绝——这一点与 091 的做法一致。
- **A5（迁移不强制，先探测）**: 迁移是显式动作而非启动时副作用：无人值守运行在未迁移仓库里 MUST NOT 自动搬动档案（那是无人值守的破坏性动作）。因此 FR-008 的迁移动作是**被调用的**，FR-011 的探测是**只读的**；本特性的干跑（FR-035）由本特性的运行自行发起。
- **A6（实测基线读数，取自本阶段）**: 2026-11-09 只读探测：`.specify/specs/*/goal/*/goal.md` 共 7 条、`.specify/specs/*/team/*/team.md` 共 7 条（085–091 各一对，其中 089 的 goal slug 为 `script-interface-contract` 而非目录名）。SC-003 引用该读数作为基线；按 091 的教训，本规格 MUST NOT 把该数字复制为第二处固定值，只在 SC-003 里作为比较基线出现。
- **A7（既有测试的处置是义务，不是可选项）**: FR-034 要求的处置清单必须先列全再动手；`tests/contract/test_scope_resolution.py`、`test_temp_goal_contract.py`、`test_temp_team_schema.py`、`test_team_command_routing.py`、`test_goal_writeset.py`、`test_goal_migration.py`、`test_goal_targets_engine.py`、`test_goal_definition.py` 与 `tests/unit/test_goal_scope_engine.py`、`test_goal_utils.py` 都含 spec-local 断言或 scope 断言，实际处置面以 plan 阶段的检索读数为准。
- **A8（本特性自身的收口受同样约束）**: 本阶段提交只含本特性产物、按显式路径、不 push——迁移机制尚未落地，本特性自己的运行仍按手工步骤完成，并把这件事实记录在此以免被误读为「机制已生效」。
