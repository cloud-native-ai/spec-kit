# Requirements Specification: sdd-observer agent（SDD 专用第三方观察者与 journal 记录）

**Requirement Branch**: `096-sdd-observer-agent`
**Created**: 2026-11-10
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（新增 `sdd-observer` 角色、修订 `sdd-loop-driver` 启动/收束逻辑、维护 journal 引擎与校验器的作者）、下游项目里被驱动式 SDD 流程编排的项目维护者，以及在一条线结束后复盘「发生了什么、证据在哪」的评审者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 在判定「观察者何时启动、活多久」「journal 记什么、不记什么、怎么证明客观」「观察者与状态脊 / 汇报义务 / 执行证据面 / line registry 的边界」「观察者掉线是否影响开发线」「与 095 superagent 角色模型怎么接口」时打开本规格，据 FR-001…FR-023 与 SC-001…SC-007 决定 `/speckit.clarify` 与后续实现是否放行
**Input**: User description: "定义一个 sdd-observer agent 定义：专门观察一个 SDD 执行流程。在确认启动 SDD 流程之后（例如创建完 SDD git 分支之后），为该 spec 的开发流程启动一个专用的 sdd-observer agent 实例。sdd-observer 可以使用内部 subagent 作为 agent execution。它以第三方视角观察并记录整个 SDD 开发流程，最终写入对应 .specify/specs/NNN-<spec slug>/journal.md。记录必须客观，只记事件与证据指针（时间、阶段、命令、产物路径、退出码），不提供任何主动的评价或建议。"

## Related Feature *(mandatory)*

**Feature ID**: 096
**Feature Name**: SDD 专用观察者与线级观察记录（sdd-observer）

## Overview

本特性新增一个 `sdd-observer` 角色及其专用实例机制：每条由 `sdd-loop-driver` 驱动的 SDD 线在确认启动之后获得一个只观察、不参与的第三方观察者；它把整条线的可观测事件以封闭结构追加写入该 spec 目录的 `journal.md`，且只记事件与证据指针。它一次回答四个立项问题：

1. **启动与生命周期**：观察者在线已登记且状态脊已建立之后、首个阶段的 U2 派发之前启动（FR-005），以有界执行窗口运行（FR-007），允许同一专用实例在阶段边界重启（FR-008），随线终态收束（FR-009）。它不是写线、不占工作树、不进集成队列（FR-004），掉线不阻塞任何阶段（FR-020）。
2. **客观性构造**：journal 的每个条目是既有载体事实的确定性投影（状态脊、阶段日志与完成哨兵、checkpoint 文件、git 历史、driver 正证据四件套），结构封闭、不存在承载评价 / 建议 / 因果推断 / 严重级的字段（FR-013），每条条目携带可解析的证据指针（FR-014），由唯一的确定性引擎写入与校验（FR-015）。
3. **载体边界**：不新造观测面——状态脊仍是唯一持久状态（FR-017），周期性面向用户的汇报仍归既有汇报义务（FR-018），外部执行的可见性仍走既有 artifact triplet 契约（FR-019），`/speckit.status` 摘要的字段集不变（FR-017）。
4. **与 095 的接口**：095（superagent 相对角色）不在本基线；本特性按现有三层 agent 模型定义 observer 角色面（FR-002），不依赖任何未合并产物；将来角色模型落地时经引用绑定，不重定义 journal 格式与启动点。

非目标：observer 不做评审、不产出建议、不参与决策，也不重复 driver 的汇报或状态摘要；不新增命令、不改任何 stage 命令内部流程、不引入调度器 / 守护进程 / 第二注册表 / 第二状态脊（FR-006、FR-018）。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一条 SDD 线从启动到 review，journal 留下完整轨迹 (Priority: P1)

一条 driver 驱动的 SDD 线从确认启动推进到 review 收束，spec 目录下出现一份 `journal.md`：按时间顺序记录阶段开始与结束、阶段校验结论、checkpoint、提交与异常。读者打开这一份文件即可复盘整条线发生了什么，并为每件事找到对应的证据位置。

**Why this priority**: 这是用户诉求的本体——第三方视角的观察必须落到一条线一份、可追溯的记录上；没有它，其余边界都是空谈。

**Independent Test**: 用一条夹具 SDD 线（stub 阶段执行 + 真实 driver 记账）启用 observer，断言 journal 存在、覆盖声明层阶段序列中的每个阶段（阶段序列读 `shared/declarations/facts/driver-stage-sequence.yaml#/statement`，夹具不重述阶段清单），且每条条目字段齐备、序号连续。

**Acceptance Scenarios**:

1. **Given** 一条已登记且状态脊已存在的 SDD 线，**When** 首个阶段被派发，**Then** journal 头部出现，且第一个 journal 条目的观测时间早于首个阶段完成条目。
2. **Given** 线推进到 review 收束且 observer 全程在线，**When** 打开 journal，**Then** 声明层阶段序列中的每个阶段都至少有阶段开始与阶段结束条目，每条条目带观测时间、阶段、事件类、证据指针，命令与退出码缺失时以 `-` 占位。
3. **Given** 线在阻塞 / 停滞处置下停线，**When** observer 结算，**Then** journal 以线终态条目收尾，或由状态脊记录 observer 未能收尾的原因（FR-009、FR-013）。

---

### User Story 2 - 记录只有事实与证据指针，评价与建议无处可写 (Priority: P1)

读者检查 journal 时，任何条目都能回到一个载体事实（状态脊字段、哨兵行、checkpoint、提交、退出记录）；条目结构里没有一个字段可以写「做得好」「应该改成什么」「因为什么导致」——第三方视角不会退化成第二个评审者。

**Why this priority**: 用户明确要求客观记录、不提供主动评价或建议；若允许自由文本，观察记录会与 review / analyze 的职责混淆，且无法被机器判定。

**Independent Test**: 确定性 checker 对结构与指针逐项判定：正常 journal 退出 0；构造三种反例——条目携带字段集之外的键（如 recommendation）、事件类落在封闭集合之外、自由叙述条目——三种反例各自转红。

**Acceptance Scenarios**:

1. **Given** 一份由引擎生成、只含封闭字段与封闭事件类的 journal，**When** checker 运行，**Then** 退出码为 0，且逐条持久证据指针可解析。
2. **Given** 在一条条目里加入字段集之外的键（如 recommendation）或写入集合之外的事件类，**When** checker 运行，**Then** 退出码非零并点名文件、行与条目。
3. **Given** 一个没有被观测到的窗口，**When** 下一次 observer 执行或线收束写入，**Then** 出现 `observer-gap` 条目点名窗口起止，而不是以推断的事件填充。

---

### User Story 3 - 观察者掉线不阻塞开发线，缺口仍被点名 (Priority: P1)

observer 进程被杀、启动报错或窗口意外结束，SDD 线照常推进并收束；状态脊记录 observer 状态，journal 或收束报告披露观察缺口。没有任何阶段因为 observer 缺席而卡住。

**Why this priority**: 观察者若成为门，开发线就被一个非交付角色挟持；用户明确要求观察者掉线不得阻塞。

**Independent Test**: 夹具中分别强制 observer 启动失败、在运行中杀死 observer，断言线仍到达终态且状态脊记录 observer 状态；再注入一个「阶段门依赖 observer 存活」的反例，断言该反例转红。

**Acceptance Scenarios**:

1. **Given** observer 启动失败，**When** 线推进到终态，**Then** 每个阶段照常完成，状态脊记录 observer 状态为失败 / 不可用，收束报告点名原因。
2. **Given** observer 执行中途被终止，**When** 线跨过下一个阶段边界，**Then** driver 不因此改判任何阶段结果，并允许同一专用实例重启，把缺口记为 `observer-gap`。
3. **Given** 某个阶段门被改为「observer 必须存活」，**When** 测试运行，**Then** 该反例转红——证明非阻塞性不是巧合。

---

### User Story 4 - 只读且边界一致：不新造状态面、汇报面或可见性通道 (Priority: P2)

想知道「现在跑到哪」，读者仍然看状态脊与 `/speckit.status`；想知道「发生过什么」，才看 journal。observer 不写开发产物，不产生第三条面向用户的通道。

**Why this priority**: 与 reporting-obligations、artifact triplet、state spine 的边界是立项要求之一；第二状态面或第二汇报面会让既有纪律互相矛盾。

**Independent Test**: 对 observer 的写面声明与状态摘要契约做结构断言：写面恰为 journal 与自身运行产物；`/speckit.status` 的字段集在本特性前后不变，observer 只以既有「已派发 agent」语义出现。

**Acceptance Scenarios**:

1. **Given** 任一 observer 执行，**When** 审计其实际写面，**Then** 只触及 journal 与自身执行运行产物，状态脊与阶段产物的写入数为零。
2. **Given** 本特性落地后，**When** 对比 `/speckit.status` 摘要契约与输出字段集，**Then** 无新增字段、行或小节；observer 仅以既有已派发 agent 语义出现。

---

### User Story 5 - 一 spec 一专用实例，可选内部 subagent (Priority: P2)

每条线拥有恰好一个专用 observer 实例；两条并行线得到两个实例身份与两份 journal。observer 可以用内部 subagent 承担自己的观察职责，但只读边界与客观性结构同样约束这些 subagent。

**Why this priority**: 用户点名「专用 sdd-observer agent 实例」与「可使用内部 subagent 作为 agent execution」；不约束实例基数会把两条线的记录写进同一文件。

**Independent Test**: 两条并行线各得独立实例身份与独立 journal；同线第二个并发 observer 执行被拒绝或串行化；observer 定义文本允许 subagent，同时载明禁止宿主内建 in-process 并发承载、禁止加载 driver 技能、禁止承载 SDD 运行。

**Acceptance Scenarios**:

1. **Given** 两条并行 SDD 线，**When** 两者各自启动 observer，**Then** 产生两个不同实例身份与两份不同 journal，不出现共享记录文件。
2. **Given** 同一线上一个 observer 执行尚未结算，**When** driver 尝试再派发，**Then** 新派发被拒绝或串行化，journal 不出现并发写。
3. **Given** `sdd-observer` 的定义文本，**When** 审计其能力面，**Then** 允许使用内部 subagent，但禁止宿主内建 in-process 路径作为并发承载、禁止引用或加载 driver 技能、禁止承载或启动 SDD 运行。

---

### Edge Cases

- **线在 observer 启动前就失败**：允许没有 journal；状态脊记录 `observer` 未启动的原因，收束报告披露，不视为静默缺失（FR-009、FR-023）。
- **journal 写入失败（权限 / 磁盘）**：observer 执行按失败结算，取证落该执行的 `.status` 退出记录与状态脊观察者记录节（journal 不作为自身失败的记录面），不影响阶段推进；下一次执行继续追加，缺口按 `observer-gap` 披露。
- **同一秒内产生多条条目**：条目顺序取追加写顺序（文件行序），checker 以文件序判定非递减，不依赖秒级时间戳排序（FR-011、FR-015）。
- **证据指针指向已被清理的运行期文件**：指针按其留存类别接受判定；持久指针在收束时必须可解析，运行期指针必须被标记（FR-014）。
- **线收束后工作树被清理**：journal 已随收束提交进入版本历史，指针中的持久载体保持可解析（FR-010）。
- **团队内调用的嵌套 SDD 运行**：内层运行拥有自己的 observer 与 journal；内层 observer 不观察外层团队运行（FR-021）。
- **observer 尝试写状态脊或阶段产物**：按越界写判定为缺陷，以声明的写面与实际差异取证（FR-016）。
- **入口声明关闭 observer**：与掉线同属「已记录的未观测」，必须在状态脊与收束报告中披露（FR-023）。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 角色定义与专用实例

- **FR-001**: 框架 MUST 交付一个 [[STR-002]] 角色定义（Agent Template 层，源位于 `agents/sdd-observer.agent.md`，经既有 `agents/` → `.specify/agents/templates/` 镜像流安装），声明 `observer` 角色面：只观察一条 SDD 线，不参与执行、评价、评审或决策。它 MUST NOT 是 stage executor、reviewer 或 reporter 席位，对开发线不持有任何写权限。
- **FR-002**: `sdd-observer` 的职责绑定 MUST 用当前基线已有的三层 agent 模型表达（Agent Template → Agent Instance → Agent Execution，owner：`.specify/shared/definitions/agent-definitions.md`）；MUST NOT 引用或依赖任何未合并特性的产物（包括 095 的 superagent 角色定义与 `superagent-definitions.md`）。`observer` 角色面 MUST 在模板与实例定义文本中显式声明，使将来出现更上位的角色模型时可经引用绑定，而不必重定义 journal 格式或启动点。
- **FR-003**: 每条 driver 驱动的 SDD 线 MUST 拥有恰好一个专用 observer Agent Instance（实例层，一条线一个实例，身份由 line / spec key 派生）；该实例 MAY 被该线的多次 observer Execution 复用；不同线 MUST NOT 共享实例或 journal。任一 stage 命令 MUST NOT 自行创建 observer 实例——实例创建属于 driver 的启动职责。
- **FR-004**: observer 的实例身份 MUST 由 `line_id` 与 spec key 派生（一条线一个实例、跨线不共享）；`run_id` 是线级 run id，不区分实例；每次 observer 执行的身份走既有派发 label 约定。身份（`line_id`、`run_id`、spec key、执行 label）MUST 记录在状态脊的观察者记录节与 journal 头部；该节由 driver 以追加式小节写入（键名与形状 owner：`skills/external/sdd-loop-driver/SKILL.md` §状态脊，plan 阶段随启动步骤修订），observer 自身 MUST NOT 写状态脊（FR-016）。observer MUST NOT 注册为写线——不占用 line registry 的封闭写线角色集（`root` / `coordinator` / `agent-write`）、不占用工作树、不进入集成队列，因为它不写任何开发产物。

#### B. 启动与生命周期

- **FR-005**: 启动时点：driver MUST 在 line 已登记且状态脊已建立之后、首个阶段的 U2 派发之前（即首个阶段提示词发出前）发起 observer 启动；启动尝试及其结果（已启动 / 失败 / 已关闭）MUST 由 driver 写入状态脊的观察者记录节（FR-004）。该时点是「确认启动」的唯一机械判据（状态脊存在 + line 已登记 + U2 尚未派发）。启动点 MUST 属于 driver；MUST NOT 下放到任一 stage 命令内部。
- **FR-006**: observer Execution MUST 经既有派发机制落地（`run-agent` 派发治理 + 既有执行拓扑声明与可见性契约），承载 MUST 是 external 执行模态的两条合法进程承载之一——fork（同族 `qodercli` 子进程经 `stage-runner.sh`）或 subprocess（异构 agent 自身 CLI 的子进程）；native 与 virtual 模态 MUST NOT 承载 observer Execution 本身。本特性 MUST NOT 引入调度器、定时器服务、守护进程、常驻服务、第二注册表或第二状态脊。
- **FR-007**: 生命周期 MUST 是有界执行窗口：observer 随线启动或阶段边界启动，随执行结算或线终态结束。同一条线在同一时刻 MUST 至多存在一个活的 observer Execution；前一个执行的 `.status` 未结算时 driver MUST NOT 派发下一个，且 journal 引擎 MUST 以单写者协议拒绝第二个并发 writer——journal 的并发写 MUST NOT 发生。
- **FR-008**: 当 observer Execution 在线终止之前结束（失败、停滞、窗口到期），driver MAY 在下一阶段边界从同一专用实例再次启动；窗口边界取既有派发的 turn budget 与阶段 deadline，不引入新定时器；重启 MUST 追加到同一 journal，并按 FR-013 记录缺口。observer 的重启 MUST NOT 改变任何阶段的重试次数、超时判定或完成哨兵判定。
- **FR-009**: 线到达终态时 observer 生命周期随之收束：driver MUST 启动一次终态收束执行，由该执行经 journal 引擎（FR-015）追加线终态条目；若收束时仍存在未闭合的观测窗口，该执行 MUST 同时追加点名窗口起止的 `observer-gap`（[[STR-003]]）条目（窗口终点取该执行首条条目的观测时间，FR-013）。仅当终态收束执行无法启动或失败（含线在 observer 启动前即失败、按 Edge Cases 允许无 journal 的情形）时，journal MUST NOT 被改写，driver MUST 在状态脊观察者记录节记录 observer 未能收尾的原因，且既有 U6 收束报告 MUST 披露未闭合窗口的起止。observer 的结算 MUST NOT 改变线终态，也不阻塞 U4 校验或 U6 收尾。

#### C. journal 制品与客观性

- **FR-010**: journal 的落点 MUST 是 `.specify/specs/<NNN-slug>/journal.md`（[[STR-001]]），一条线一份；写入 MUST 为追加式，已写入条目 MUST NOT 被改写或删除；journal 头部 MUST 承载 `line_id`、`run_id`、spec key、实例 label 与 `created_at`（UTC），由 checker 校验。journal 可被中间阶段提交扫入且不要求单独提交，线收束提交 MUST 包含最终条目，使工作树清理后记录仍从版本历史可读；journal 写入失败时，失败取证落 observer 执行自身的 `.status` 退出记录与状态脊观察者记录节（journal 不作为自身失败的记录面）。本特性 MUST NOT 引入第二份记录文件或第二个记录存储。
- **FR-011**: 条目结构 MUST 封闭：每个条目恰好承载九类信息——序号（引擎赋值、单调递增且与文件序一致）、观测时间（引擎时钟，UTC ISO-8601 秒级）、事件时间（载体提供时，否则 `-`）、阶段（线级与 observer 自身事件取 `-`）、事件类、命令（原文或 `-`）、产物路径（仓库相对或 `-`）、退出码（整数或 `-`）、证据指针（至少一个，并带留存类别）。同一秒内的多条条目以文件序为权威顺序。键名拼写与事件类字面量由 journal 格式 owner（`shared/declarations/facts/journal-format.yaml`）唯一拥有；本规格拥有信息面与封闭性要求，owner 拥有拼写面。
- **FR-012**: 事件类 MUST 取一个封闭集合，覆盖可观测的 SDD 里程碑：线启动与线终态、阶段启动与阶段结束、阶段校验结论、checkpoint、提交、异常、停滞、重试、派发、产物写入，以及 observer 自身的启动、结算、缺口与错误。集合的增删 MUST 经 journal 格式 owner 修订；执行体 MUST NOT 就地发明条目或事件类。
- **FR-013**: 客观性 MUST 由构造保证：条目是既有载体事实的确定性投影——观测输入限定为磁盘载体与仓库事实（状态脊、阶段日志与完成哨兵、checkpoint 文件、git 历史、driver 正证据四件套（`pid-*` / `status-*` / `log-*.log` / `heartbeat-*.log`）、exec 记录），MUST NOT 以 driver 的会话上下文或阶段提示词作为观测输入；observer MUST NOT 手工编写自由叙述条目；journal MUST NOT 存在承载评价、建议、因果推断、严重级或推荐的字段，字段集之外的键与集合之外的事件 MUST 被判红。未被观测的窗口 MUST 记为 `observer-gap`（[[STR-003]]），MUST NOT 以推断的事件填充；缺口窗口起点取上一条已写入条目的观测时间（无条目时取状态脊观察者记录节的启动时间），终点取下一次执行首条条目的观测时间（线终态时即 FR-009 的终态收束执行）。
- **FR-014**: 证据纪律：每条条目 MUST 至少携带一个证据指针；指向持久载体的指针 MUST 在线收束时可解析，不可解析即缺陷；只存在于运行期的指针 MUST 被标记为运行期留存，且当同一事实存在持久载体时 MUST NOT 成为唯一条目证据。没有载体证据的事件 MUST NOT 被记录。
- **FR-015**: MUST 存在一个确定性 journal 引擎（单一可执行面）：它把载体事实投影为封闭结构、校验结构 / 序号 / 文件序 / 指针可解析性，并拒绝未声明的键与事件；observer Execution MUST 经该引擎写入，而非手写条目。该引擎 MUST 遵守脚本接口契约（`-h` / `--help` / `--version` 零副作用应答，未声明选项非零拒绝）。

#### D. 载体边界

- **FR-016**: 只读边界：observer 的写面恰为 journal 与自身执行运行产物（既有 `.specify/agents/execution/logs/` 布局）；MUST NOT 写状态脊、阶段产物、feature 注册表、glossary 或任何其他载体。越界写 MUST 按缺陷判定，以实例 / 模板声明的写面与实际写入差异取证。
- **FR-017**: 状态面边界：状态脊仍是 driver 的唯一持久状态；observer MUST NOT 创建第二状态存储、第二注册表、第二状态面或第二汇报通道。observer 的存活与状态 MUST 经既有主从汇报义务（master 每 tick 报告已派发 sub-flow）与 `/speckit.status` 的既有 supervision 投影（driver 以既有 `--sub-flow <label>=<triplet-dir>` 语义传入）作为普通已派发 agent 呈现，MUST NOT 新增字段、行或小节。
- **FR-018**: 汇报边界：journal 是持久记录，不是周期性面向用户的汇报；observer MUST NOT 发出用户可见的汇报、提问、审批请求、建议或评价。driver 的汇报义务与 observer 的 journal 互不替代，范围内流程的汇报义务 MUST NOT 因本特性改变。
- **FR-019**: 可见性边界：外部承载的 observer Execution MUST 遵守既有 External Dispatch Visibility Contract 的 artifact triplet（`<label>.live.log` / `<label>.jsonl` / `<label>.status`，三件）；journal 以指针引用这些运行产物，MUST NOT 复制其内容，MUST NOT 新造可见性通道。

#### E. 非干涉、范围与内部子代理

- **FR-020**: 非干涉：observer 的存在、缺失、健康、结论与 journal 内容 MUST NOT 成为任何阶段推进（U4）、checkpoint、review 或合并的门；observer 异常 MUST 由 driver 记录进状态脊观察者记录节并在既有 U6 收束报告中披露，但 MUST NOT 阻塞开发线；observer 自身 MUST NOT 发出用户可见的汇报、提问或审批请求（FR-018）。唯一的收束义务是披露（FR-009、FR-013、FR-023），且披露 MUST 由一条记录的原因满足；当 FR-009 的终态收束执行可用时，journal 侧的终态与缺口写入照常执行，披露与该写入互不替代。
- **FR-021**: 适用范围内：本特性适用于 driver 驱动的 SDD 线（含团队内调用的嵌套运行），一条线一份 journal。非 SDD 的 `/speckit.*` 命令运行与不承载 SDD 线的 team 运行 MUST NOT 产生 observer 或 journal；嵌套运行拥有自己的 observer，内层 observer MUST NOT 观察外层团队运行。
- **FR-022**: observer MAY 使用内部 subagent 承担自己的观察职责，但内部 subagent MUST 在 observer Execution 内串行执行、MUST NOT 作为并发承载（宿主内建 in-process 并发路径 BANNED），且继承 observer 的只读边界（FR-016）、读域（FR-013）与客观性结构（FR-011、FR-013）。observer MUST NOT 引用或加载 driver / 循环技能，MUST NOT 承载或启动 SDD 运行。
- **FR-023**: 入口声明 MAY 关闭 observer，键为 `observer: on|off`（缺省 `on`）；关闭 MUST 由 driver 记录在状态脊观察者记录节（state=`disabled`）并在收束时披露。关闭的 observer 与掉线的 observer 同属「已记录的未观测」，MUST NOT 表现为静默缺失。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增外部运行时——它消费既有的 Python 解释器、既有测试运行器、既有驱动 / agent / 派发面与宿主 `git`。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库文件系统、JSON 与时间能力（journal 引擎与校验器的运行面） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 中既有的 `requires-python` 声明；本特性零新增第三方依赖 | `pyproject.toml` | `bash scripts/bash/run-tests.sh` 在 `>=3.8` 解释器上通过 | FR-011, FR-015 | EP-001 |
| RS-002 | `pytest` 测试运行器（契约测试与夹具执行） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 中既有的 `pytest` 依赖声明；本特性零新增依赖 | `pyproject.toml` | `bash scripts/bash/run-tests.sh -m contract` 通过 | FR-012, FR-013, FR-014 | EP-002 |
| RS-003 | 既有 SDD 驱动、agent 定义与派发面（启动点、专用实例、进程承载、可见性契约） | in-scope | 本特性自身修订的 `sdd-loop-driver` 技能与 `agents/` 角色模板 | 不适用（无外部版本面） | `skills/external/sdd-loop-driver/SKILL.md` | 驱动的定义断言与契约测试通过：启动步骤在场、写面无越界、未引入新机制术语 | FR-002, FR-003, FR-005, FR-006, FR-016, FR-017 | EP-003 |
| RS-004 | `git` 命令行的只读提交 / 分支事实观测（journal 的提交类事件） | signed-contract | 宿主环境提供（本仓只消费，不打包） | 不计版本字符串；本特性实现期实测 `git log --format` 与 `git rev-parse` 形态在宿主各跑通一次，任一不可用即判 `fail` | `pyproject.toml` | 收束时 journal 的提交类条目可在宿主 `git` 上逐条复现 | FR-012, FR-014 | EP-004 |

> RS-004 的 `Contract` 列只声明本仓 Python 依赖面；`git` 由宿主环境提供，不列为 Python 依赖（沿 091 的同一处置）。`Premises` 列的 `EP-NNN` 由 plan 阶段的 § Execution Premises 定义并对齐本表；若 plan 需要改号，两侧同批更新，MUST NOT 只改一侧。

### Key Entities *(include if requirement involves data)*

- **sdd-observer 角色模板（Observer Template）**: Agent Template 层的角色定义，声明只看不做的角色面、只读边界与客观性禁令；一条线不拥有模板，只拥有实例。
- **专用观察实例（Observer Instance）**: 绑定到一条 SDD 线的 Agent Instance，承载该线的观察职责与身份（`line_id` / `run_id` / spec key）；可被多次执行复用，跨线不共享。
- **观察执行（Observer Execution）**: 一次有界的 live run — 启动于线启动或阶段边界，结算于窗口结束或线终态；其运行产物遵循既有 artifact triplet 与存储布局。
- **观察记录（journal）**: 线级、单文件、追加式的持久制品，落在 `.specify/specs/<NNN-slug>/journal.md`；由引擎写入，随线收束提交。
- **记录条目（Journal Entry）**: 封闭结构的单条事实投影，承载九类信息（类别见 FR-011）；不存在评价 / 建议 / 因果推断字段。
- **事件类（Event Class）**: 条目所表示的可观测里程碑的封闭取值；字面量由 journal 格式 owner 唯一拥有。
- **载体事实（Carrier Fact）**: 状态脊字段、完成哨兵行、checkpoint、提交、driver 正证据四件套状态与 exec 记录等可复核事实；是条目的唯一来源。
- **观察缺口（Observer Gap）**: 一段没有被任何 observer 执行覆盖的时间窗口的显式记录；不是推断出来的事件。
- **专用实例身份（Line-scoped Observer Identity）**: 由 line / spec key 派生的实例与记录身份；保证一条线一个实例、一份 journal。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 一条由 driver 夹具驱动、observer 启用且全程零 observer 失败的完整 SDD 线，在 `.specify/specs/<NNN-slug>/journal.md`（[[STR-001]]）产生记录，覆盖声明层阶段序列中的每一个阶段（阶段序列读声明层，不重述阶段清单）；对含 observer 失败或缺口的线，覆盖判据为「每个阶段至少有阶段开始条目，或被 `observer-gap`（[[STR-003]]）点名」（收束侧缺口条目的写入义务：FR-009；缺口窗口定义：FR-013）；删除 journal、或删掉零失败夹具中任一阶段的阶段结束条目，使验收测试转红。 **Path**: final
- **SC-002**: journal 中每条条目的持久证据指针在线收束时可解析；注入一条伪造或指向不存在路径的条目，使 checker 转红（变异实测记录在 `test-evidence/`）。 **Path**: final
- **SC-003**: 非阻塞性成立：强制 observer 启动失败、以及在运行中杀死 observer，夹具中的开发线仍到达其终态，状态脊记录 observer 状态（失败 / 不可用）；把一个阶段门改为依赖 observer 存活时，该反例测试转红。 **Path**: final
- **SC-004**: 客观性构造可判定：checker 拒绝 (a) 携带字段集之外键（如 recommendation）的条目、(b) 落在封闭集合之外的事件类、(c) 自由叙述条目——三份反例夹具各自转红；且 `sdd-observer`（[[STR-002]]）的定义文本逐字携带「不评价、不建议、不推断」禁令。 **Path**: final
- **SC-005**: 启动时序与实例不变量：首个 journal 条目早于首个阶段完成条目；两条并行线产生两份不同 journal 与两个不同实例身份；同线第二个并发 observer 执行被拒绝或串行化。 **Path**: supporting
- **SC-006**: 边界一致：observer 声明的写面恰为 journal 与自身运行产物，状态脊 / 阶段产物的写入数为零；`/speckit.status` 摘要契约与输出字段集以本特性第一个实现提交之前的一次实测采集为基线，允许的 delta 集合为空（零新增字段、行与小节），observer 仅以既有已派发 agent 语义出现。 **Path**: supporting
- **SC-007**: 缺口披露：人为跳过一段观测窗口后，下一次 observer 执行或线终态收束执行 MUST 输出 `observer-gap`（[[STR-003]]）条目并点名窗口起止（写入义务：FR-009；窗口定义：FR-013）；移除缺口披露机制使该测试转红。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: `tests/fixtures/sdd-observer/` 下的驱动夹具（stub 阶段 + 真实 driver 记账）与 `tests/contract/` 下的 journal 覆盖断言；夹具运行输出与 `test-evidence/requirements-*.txt` 一并留痕。
- **SC-002 Source**: 契约测试中的伪造指针反例（变异实测：正常夹具绿、伪造指针红），证据落在本特性 `test-evidence/`。
- **SC-003 Source**: 两个非阻塞夹具（启动失败、中途终止）的退出码与状态脊读取记录；「observer 成为门」的反例转红记录。
- **SC-004 Source**: 三份客观性反例夹具（额外字段 / 集合外事件 / 自由叙述）的 checker 退出码与点名行，以及定义文本的逐字断言。
- **SC-005 Source**: 双线并行夹具的 journal 路径与实例身份清单；同线重复派发的拒绝或串行记录。
- **SC-006 Source**: 写面声明的结构断言（journal 与运行产物之外为零）；`/speckit.status` 契约字段集的前后对比记录（零新增），observer 行经既有 supervision `--sub-flow` 投影出现。
- **SC-007 Source**: 缺口夹具的 `observer-gap` 条目摘录与窗口起止；移除披露机制后的红测记录。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"journal.md"` | FR-010, SC-001 |
| `STR-002` | `"sdd-observer"` | FR-001, SC-004 |
| `STR-003` | `"observer-gap"` | FR-013, SC-007 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

### Session 2026-11-10（无人值守 requirements，自行裁决并记录）

- Q: 观察者实例的启动时机定在哪一步，才算「确认启动 SDD 流程」？ → A: 用户原话「如创建完 SDD git branch 之后」是示例而非严格事件；本阶段裁为「线已登记、状态脊已建立之后，首个阶段的完成被接受之前」（FR-005）。这是 driver 可判定、且与阶段内部流程解耦的唯一时点，避免把启动点塞进任一 stage 命令。
- Q: 观察者实例的生命周期怎么定，与 line registry / 状态脊 / 阶段派发是什么关系？ → A: observer 不是写线，不注册写线角色、不占工作树、不进集成队列（FR-004）；身份只写状态脊与 journal 头部。执行是有界窗口、同线至多一个活执行、允许阶段边界同实例重启（FR-007、FR-008）；线终态收束（FR-009）。重启不改变阶段重试与超时判定（FR-008）。
- Q: journal 的客观性怎么构造才可判定？ → A: 结构 + 投影 + 证据三件事：封闭字段集与封闭事件类（FR-011、FR-012）；条目是载体事实的确定性投影，没有承载评价 / 建议 / 因果推断的字段（FR-013）；每条条目带可解析证据指针（FR-014），由唯一确定性引擎写入与校验（FR-015）。不建自然语言评价检测器——那会引入第二判断面与误报。
- Q: 与 reporting-obligations、artifact triplet、state spine 的边界怎么划？ → A: 状态脊仍是唯一持久状态，observer 只读；周期汇报仍归既有汇报义务，journal 不是汇报；外部可见性仍走既有四件套，journal 只引用不复制；`/speckit.status` 摘要字段集不变，observer 以既有已派发 agent 语义出现（FR-016…FR-019）。
- Q: 与 095（superagent 相对角色）怎么接口？ → A: 095 不在本基线；本阶段按当前三层 agent 模型定义 observer 角色面（FR-002），不引用任何未合并产物。sdd-observer 先作为一个持 `observer` 角色面的 Agent Instance 落地；将来若 095 合并，只做角色模型的引用绑定，不重定义 journal 格式与启动点。
- Q: 观察者掉线怎么办？ → A: 不阻塞——observer 的任何失败只被记录与披露，不成为阶段门（FR-020）；缺口以 `observer-gap` 显式记录（FR-013），收束必须披露「未观测」的原因（FR-009、FR-023）。

### Session 2026-11-10（clarify pre-plan，无人值守自行裁决）

- Feature binding（机械应用 Feature Binding Rules）: `.specify/features.md` 与 `.specify/features/` 无同主题 Feature（候选 064 / 074 / 085 的范围分别为 subagent 并发归属、Goal/Team/Agent 与 SDD 统一、临时 Goal/Team 并发；均不覆盖「观察者角色 + 线级 journal」），按 create 分支绑定新 Feature `096`（095 预留给未合并的 superagent 特性，见 A2）；索引行与详情文件的落册义务本轮不执行（本阶段写面仅 requirements.md），记为 pending，恢复点为本会话条目与 clarify 报告。
- Q: 观察者的启动时点与实例身份 / 状态脊登记如何裁定，才与 line registry、状态脊和首个阶段派发一致？ → A: 启动时点收敛为 driver 在 line 已登记且状态脊已建立之后、首个阶段 U2 派发之前执行一次启动步骤（FR-005 与 A3 同步改写；US1 AS1 的「首个阶段被派发时 journal 头部已存在」即该判据）；实例身份 = `line_id` + spec key，`run_id` 为线级、不区分实例，每次执行走既有派发 label；状态脊观察者记录节由 driver 以追加式小节写入（字段：state ∈ `started`|`failed`|`disabled`|`closed`、instance、execution label、reason），键名与形状 owner 为 `skills/external/sdd-loop-driver/SKILL.md` §状态脊，observer 自身不写状态脊；关闭开关为 U0 入口声明的 `observer: on|off`（缺省 `on`），投影到同一记录节（FR-004、FR-005、FR-016、FR-023）。
- Q: journal 的条目结构、时间基准与缺口窗口如何补全才可机械校验？ → A: 条目为九类信息（在八类之外增加单调递增的 `序号`；`阶段` 对线级与 observer 自身事件取 `-`）；观测时间取引擎时钟 UTC ISO-8601 秒级、同一秒内以文件序为权威；事件时间仅在载体提供时填写；journal 头部承载身份四元组（`line_id` / `run_id` / spec key / 实例 label）与 `created_at`，由 checker 校验；格式 owner 预绑定为 `shared/declarations/facts/journal-format.yaml`（A8 改写）；`observer-gap` 窗口起点取上一条已写入条目的观测时间（无条目时取状态脊观察者记录节的启动时间）、终点取下一执行首条条目的观测时间（FR-010、FR-011、FR-013、FR-015）。
- Q: 观察者 Execution 用哪种执行模态承载，内部 subagent 的并发与读域如何约束？ → A: observer Execution MUST 用 external 模态的进程承载（fork `stage-runner.sh` 或 subprocess 异构 CLI 子进程）；native / virtual MUST NOT 承载 observer Execution 本身；内部 subagent 只在 observer Execution 内串行承担观察职责、不作为并发承载（宿主 in-process 并发 BANNED），并继承同一只读边界与读域（磁盘载体与仓库事实，禁读 driver 会话上下文 / 阶段提示词）；同线单活执行由 driver 串行派发（上一执行 `.status` 未结算不派发）+ journal 引擎单写者拒绝共同保证；窗口边界取既有派发 turn budget / 阶段 deadline，不新增定时器（FR-006、FR-007、FR-008、FR-013、FR-022）。
- Q: 与 reporting-obligations / artifact triplet / status-digest 的边界如何落到既有面而非新造？ → A: 术语分流——visibility contract 统一称 artifact triplet（`<label>.live.log` / `<label>.jsonl` / `<label>.status`，三件），driver 自身 watch 证据称正证据四件套（pid / status / log / heartbeat，四件）；observer 作为已派发 sub-flow 由既有主从汇报义务（master 每 tick 报告已派发 sub-flow）与 `/speckit.status` 的既有 supervision 投影（driver 以既有 `--sub-flow <label>=<triplet-dir>` 语义传入）呈现，digest 字段集零新增（SC-006 不变）；observer 自身不发用户可见汇报或审批请求（FR-017、FR-018、FR-019、A9）。
- Q: 观察者自身的失败语义（启动失败、掉线、journal 未写成）如何裁定？ → A: 三者都归「已记录的未观测」，不成为阶段门——启动失败与 journal 写入失败由 driver 记入状态脊观察者记录节（state=`failed` + reason），并由 observer 执行自身的 `.status` 退出记录取证；中途终止允许下一阶段边界从同一实例重启并写 `observer-gap`；journal 不作为自身失败的记录面；线在 observer 收尾前失败时，状态脊记原因、既有 U6 收束报告披露；SC-001 的完整覆盖断言限定于零 observer 失败夹具，失败线覆盖判据为「每阶段有阶段开始条目或被 `observer-gap` 点名」（FR-009、FR-013、FR-020、FR-023、SC-001）。

## Assumptions

- **A1（类别判定：execution）**: 按验收 oracle 判定——交付物（agent 定义、driver 启动逻辑、journal 引擎与 checker）在验收时被机器执行与解析，缺陷在运行与解析时暴露，而不是只在读者读错时暴露；故 `Flow Class` 为 `execution`，`Flow Type` 为 `-`。
- **A2（095 接口按 master 现状定义）**: 基线（master@b3da3a26d）不含 `superagent-definitions.md`、不含 095 spec；本规格不假设其存在。`sdd-observer` 按现有三层 agent 模型落地，`observer` 角色面写入定义文本，供将来的 superagent 角色模型引用绑定。若 095 先合并，plan 只做映射复核，MUST NOT 引入第二套角色系统。
- **A3（启动点裁为 driver 的 U2 之前）**: 启动发生在 line 登记与状态脊建立之后、首个阶段的 U2 派发之前（首个阶段提示词发出前）；这是「确认启动」在本框架里唯一可机械判定的形态（状态脊存在 + line 已登记 + U2 尚未派发）。用户举例的「创建完分支」在既有流程中早于此判定，故不作为判据。
- **A4（有界执行而非常驻进程）**: observer 的执行形态裁为「有界窗口 + 阶段边界重启」，而非单一长跑进程。理由：框架的执行层是有 turn budget 的 Agent Execution，且 reporting-obligations § 十一 明令禁止调度器、定时器服务与守护进程；重启由 driver 的阶段边界触发，窗口边界取既有派发的 turn budget 与阶段 deadline，不需要新机制。
- **A5（journal 单文件覆盖「一文一件」缺省）**: `journal.md` 是用户点名的单文件制品，优先于 Concurrent Development Safety 的「记录类数据一文一件」缺省（用户指令优先于项目惯例）；并发安全由「同线至多一个活 writer + 追加写」承担（FR-007、FR-010），并由双线夹具验证路径隔离。
- **A6（客观性用构造而非语义检测）**: 客观性通过封闭结构、载体投影与指针可解析实现；本规格明确不建自然语言的情感 / 建议检测器——那是一个新的判断面，判定不可复现且会误报。评价与建议在结构上无处可写，即为达标的判定形态。
- **A7（observer 不是写线）**: observer 不注册 line registry 的封闭写线角色集（`root` / `coordinator` / `agent-write`）、不占工作树、不进集成队列；身份（`line_id` / `run_id` / spec key / 执行 label）由 driver 写入状态脊观察者记录节并同步进 journal 头部，observer 自身不写状态脊。此裁定避免改动 line registry 的封闭角色集与 worktree 语义。
- **A8（格式 owner 预绑定）**: 字段键名、事件类字面量与 journal 头部形状由 `shared/declarations/facts/journal-format.yaml` 唯一拥有（本规格预绑定该路径，plan 阶段创建该声明并由 `declaration_reader.py` 读取）；本规格只拥有信息面与封闭性。测试钉住 `STR-001`…`STR-003` 三个字面量，其余拼写不在本规格重复。
- **A9（运行期产物用既有布局）**: observer 自身的执行日志与 artifact triplet 落既有 `.specify/agents/execution/logs/`（已被 `.specify/.gitignore` 忽略）；journal 对这些产物使用「运行期留存」指针（FR-014），持久事实优先引用状态脊、spec 产物、checkpoint 与提交。
- **A10（可测性分层）**: 确定性面（journal 引擎、checker、driver 启动 / 收束文本、定义断言）走契约测试；observer 的 LLM 行为本身以定义文本与结构断言为准，按模板类特性先例判 Test-First Partial（宪法 VII 的 justified 形态），不伪称对 LLM 行为做了确定性回归。
- **A11（框架源侧落地）**: 变更是框架源侧的（`agents/`、`skills/external/sdd-loop-driver/`、`shared/`、`scripts/`、`templates/` 及其 `.specify/` 镜像），经既有镜像与 init 流到达下游；不改任何 stage 命令内部流程，不新增 `/speckit.*` 命令。
- **A12（journal 不进阶段产物表）**: journal MUST NOT 被加入任何阶段的 required artifact 集或 `STAGE_ARTIFACTS` 映射，也不成为 U4 完成条件；它由线收束提交携带，阶段完成判定与 observer 状态完全解耦（FR-009、FR-020）。
- **A13（关闭开关是可记录状态）**: 入口声明可以关闭 observer（默认启用）；关闭、启动失败、中途终止三者都是「已记录的未观测」，收束必须披露，禁止静默缺失（FR-023）。本阶段不发明第二个开关或配置层。
