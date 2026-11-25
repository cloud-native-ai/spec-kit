# Requirements Specification: Background Dispatch Settlement — 后台派发静默退出结算契约（Background Dispatch Settlement）

**Requirement Branch**: `106-background-silent-failure`
**Created**: 2026-11-25
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（`shared/definitions/`、`skills/internal/run-agent`、`skills/internal/run-team`、`skills/internal/create-team`、`skills/external/sdd-loop-driver`、契约测试与文档的作者）与下游项目维护者（升级后需要判定「我的后台派发何时才算有结论、静默结束时谁负责上送、旧记录还算不算数」）
**Reading scenario**: 当需要判定「一次后台派发结束状态的封闭集合是什么」「每个状态分别需要什么正证据」「哪些派发载体已有静默退出契约、哪些缺失」「检测到静默结束后必须上报、重试还是停止」「哪条守卫能让静默终止转红」「既有哨兵、判定、退出码与确认纪律是否被改动」「客户项目如何升级且不丢证据」时打开本规格，据 FR-001…FR-041 与 SC-001…SC-009 放行 `/speckit.clarify` 与后续规划
**Input**: User description: "目前后台任务静默退出(成功或失败)依然是个大问题, 需要开发一个特性,在superagent-subagent进行后台任务派发的时候需要能够处理后台任务的静默失败场景"

**输入校正（写在规格最前，供后续阶段沿用）**：

1. **「后台任务」**读作**可脱离派发回合继续执行的后台派发**——外部进程载体（fork / subprocess）、远端 detached 运行、宿主提供的后台子代理任务；不读作占用当前会话的 virtual 模式（它不产生可脱离的边，见 A-5）。
2. **「静默退出(成功或失败)」是两个都要处理的形态**：**静默成功**＝后台工作结束（或进程消失）却没有完成证据，没人能把它与「仍在运行」区分；**静默失败**＝后台工作失败或终止却没有失败证据，没人能把它与「仍卡着」或「成功」区分。用户句末的「静默失败场景」按整句语义读作包含两者，而不是只修失败一侧。
3. **「superagent-subagent」**指既有相对角色与派发边（owner：`.specify/shared/definitions/superagent-definitions.md`），不是新的实体、层级或第二套角色定义。
4. **「需要能够处理」**读作：**结算（settle）+ 上送（report）+ 按既有纪律反应（retry / stop）**，不是静默自动修复、不是自动杀进程、不是新调度器。
5. **「大问题」**是真实摩擦的陈述；本规格的现状以源码实测为准（见 § Overview），不把散文当作机制权威。

## Related Feature *(mandatory)*

**Feature ID**: 095
**Feature Name**: Super Agent Role（相对逻辑角色：定义、协议与 harness 落点）

## Overview

**实测基线（commit `fbab7a45c`）**：后台派发的当前形态分散在四条入口与三类证据面中，各自的「结束可判定性」并不相同。

- **C-1 fork 载体（SDD 驱动阶段派发）**：`skills/external/sdd-loop-driver/scripts/stage-runner.sh` 写四件套（pid / status / log / heartbeat）与 runner log；`scripts/watch-target.sh` 拥有判定状态机与退出码；`references/watch-model.md` §2–§3 规定「完成需正证据」。`NO_SIGNAL` / `DEAD` / `INCOMPLETE` 已覆盖该载体的部分静默形态，065a 的状态快照另检测 `dead-no-exit-record`、`unwatched`、`artifacts-without-completion` 等中断形态。这是**已有静默退出契约**的一侧。
- **C-2 subprocess 载体（`skills/internal/create-team/scripts/dispatch.sh`）**：产出 `.live.log` / `.jsonl` / `.status` 三件套；`.status` 只在管线正常走到末尾时写一次 `<label> exit=<code>`，脚本自身**没有 trap、没有 pid 记录、没有心跳**。若包装脚本被 SIGKILL、宿主被杀或机器中断，目录里只剩停止增长的日志：**没有终止记录，也没有可判活的 pid**。这是**缺失静默退出契约**的一侧。
- **C-3 团队席位**：`skills/internal/run-team/SKILL.md` 经 C-1/C-2 派发席位；`skills/internal/create-team/SKILL.md` 的运行报告有 `## Execution Detail` 派发映射表与必填 `## Verification`，但映射表没有「该席位以什么状态结束」这一列——一个席位静默死亡时，报告仍可能以成功语气收尾。
- **C-4 native / C-5 virtual**：`skills/internal/run-agent/SKILL.md` 要求回传携带五要素，缺一即不完整、不得消费；但**尝试记录只在父侧记忆中**，回归载体里没有一个「这个尝试已开始、至今没有返回」的持久事实。native 后台任务若被宿主丢失，父侧无法凭既有载体证明它消失过；virtual 不脱离会话，不存在孤儿边，但当前也没有把这一排除写成显式规则。
- **C-6 直接外部配方**：`.specify/shared/workflow/external-dispatch-recipes.md` 的后台配方只承诺阶段粒度观测，且把「超过超时仍无哨兵」写成 stall；在「进程已死且无终止记录」与「进程仍活」两种情形下，这同一句话给出的处置方向相反。
- **契约层的既有半句**：`.specify/shared/definitions/superagent-definitions.md` § The super↔sub Protocol § Termination 已声明边的结束值 `completed` / `failed` / `cancelled` 且「silent orphaning is a defect」；但**没有把静默终止命名为一个可观测状态，没有给出每个状态的正证据，也没有任何守卫让它转红**。本特性修订这一 owner 章节，而不是另立一套平行定义。

**问题（为什么现在必须做）**：父侧今天对「子执行体还活着吗」只有两种回答——读一个可能不存在的返回，或凭印象。静默成功会让已完成的工作被当成仍在运行而重复派发；静默失败会让一个死掉的执行体被当成仍卡着而永远等下去。两者都不是「偶发故障」，而是**判定面缺一个状态**：没有正证据的终止必须被识别为终止，而不是落入 `completed`、`failed` 或 `running` 中的任何一个。

**本特性交付**：一条**派发结算契约**——封闭的结算值集合与每值的正证据要求、全部后台派发载体的证据一致性、静默结束后的反应义务，以及一个**能让静默终止转红的确定性判定面**。它复用既有 watcher 判定、065a 状态快照、role-edge 判定引擎、三件套/四件套与运行报告，不新建调度器、注册表或第二个状态机（A-6、FR-038）。

**不做什么**：不改变 watcher 的判定、退出码与哨兵字面量；不改变五要素上行与七字段下行；不改变 SDD 阶段语义、授权、确认纪律与两槽位测试预算；不自动杀进程、不自动重试、不自动推送/合并、不删除证据、不改写历史记录；不把 observer、报告或父侧记忆当作唯一结算载体。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **类别判定 = `execution`**：交付物是定义、技能/命令文本、报告字段、判定引擎行为与契约测试；缺陷只在机器执行、解析或断言时暴露。 | 按验收 oracle 判定，而非按介质（owner：`.specify/shared/definitions/flow-class-definitions.md`）。 |
| **A-2** | **静默成功与静默失败同属范围**：结束但没有完成证据的工作不得算 `completed`；结束但没有失败证据的工作不得算 `failed`；两者都不得被报成 `running`。 | 用户原话已点名「成功或失败」；brief 的语义读法与此一致。只修失败一侧会留下「做完了没人知道」的更大浪费。 |
| **A-3** | **结算值封闭集**：`completed` / `failed` / `anomaly` / `cancelled` / `running` / `silent-end` / `unknown`。前四者为终态语义（其中 `anomaly` 为异常终态），`running` 为非终态且只在活证据下成立，`silent-end` 为「终止但无结论」的显式异常终态，`unknown` 为证据不可读的检测缺陷态、不是结束。`cancelled` 复用既有 owner 的结束值；`silent-end` 为本特性命名的新值；`unknown` 复用 065a 的既有词汇。集合与证据要求的唯一 owner 是修订后的 superagent 定义章节（A-6）。 | 既有 owner 已有 `completed` / `failed` / `cancelled`；watch 侧已有 `RUNNING` 与各类无信号判定。需要新增的恰恰只是「静默终止」这一个可观测状态，而不是一套新词表。 |
| **A-4** | **载体范围 = 后台可脱离者**：C-1 fork、C-2 subprocess、C-3 团队席位、C-4 native（仅在宿主提供后台形态时）、C-6 直接外部配方在范围内；C-5 virtual 显式排除（不能脱离会话，父侧就是执行者，不存在孤儿边），但父侧仍不得把未完成的 virtual 工作报成 `completed`。 | 不静默缩小请求：把 virtual 排除的理由写明并留下「未完成不得报成功」的义务，而不是假装它不存在。native 是否后台由宿主决定，故按「宿主提供则适用、否则前台终结」双分支写明。 |
| **A-5** | **后台派发 = 可脱离派发回合的执行**；前台 native/virtual 的工具返回本身就是终止事件，不产生持久边。 | 与 `.specify/shared/definitions/subagent-definitions.md` § Three Execution Modes 的承载分类一致；避免把前台同步调用也纳入异步结算。 |
| **A-6** | **零第二机制**：不新建存储、注册表、调度器、队列、守护进程、通知通道或 child list；结算是对**既有载体**的只读分类。契约的单一 owner 是 `.specify/shared/definitions/superagent-definitions.md` § Termination（本特性修订），载体判定仍归 `references/watch-model.md` 与 065a，边判定优先复用 `scripts/python/role-edge-check.py`；新引擎只有在 plan 记录「既有 owner 不覆盖」的裁定后才允许。 | 宪法 IX / 政策 One Source Of Truth；简报明确要求「不要建造第二套机制」。 |
| **A-7** | **正证据原则延伸**：`completed` / `failed` / `anomaly` / `cancelled` / `silent-end` 都必须有**正向记录**；「没看到输出」「进程不在了但没查」不构成任何终态证据。`silent-end` 需要「尝试已开始」+「执行主体已消失」+「四类终态证据均缺席」三件同时成立。 | 延续 watch-model 的「完成需正证据」；否则静默终止会被读成「未知」，而未知又会被读成「还行」。 |
| **A-8** | **反应三选一**：report / retry / stop；禁止静默修复。`silent-end` 与 `unknown` 按 fast-fail 的异常停纪律上送，不得当作普通失败原样重派。重试永远是**新尝试、新 label**，旧证据保留。 | owner：`.specify/shared/guidelines/fast-fail.md`、`superagent-definitions.md` § Attempts。新增计数器或自动重试器会造出第二套处置。 |
| **A-9** | **既有契约的包含性保持**：哨兵字面量、watcher 判定/退出码/`--self-test`、五要素上行、七字段下行、确认纪律与其冻结预算、两槽位测试预算的允许差异集为**空集**；新字段/新文件一律加性；不改变既有 `.status` 行格式。 | 简报的 preserve 要求；同时满足 `closed-set-claims.md` 的五要件（基线、比较单元、允许集来源、补集断言、无未定义聚合词）。 |
| **A-10** | **迁移 = 前向加性 + 旧记录显式标注**：新格式记录以**加性字段**声明结算契约版本（随结算承载记录声明，不改既有行格式）；无版本的历史记录/报告按 dated record 不改写，但在**结算判定/审计输出**中标注 legacy，**不得**被报成「符合新契约」，且 legacy 标注本身**不构成失败退出码**。不新增预造拒绝机制：证据不可读由 [[STR-002]] 承担确定性拒绝语义；不兼容的活面变更按 FR-035 自带迁移/拒绝并附测试（本特性的允许差异集为空集，即不发生）。 | 历史记录是当时事实，不是待修缺陷；「legacy 沉默通过」才是盲检类失效。标注、拒绝、禁止三分闭合，避免第二套拒绝机制。 |
| **A-11** | **两顶帽子**：契约与文本落框架源（`shared/`、`skills/`、`templates/`、`scripts/`、`src/`）；本仓 `.specify/` 的镜像由既有同步/安装流程再生，不手改；客户项目经 init/refresh 获得。 | 直接改运行时副本不传播，且会被下一次刷新覆盖。 |
| **A-12** | **确认纪律预算零新增**：在扫描面上新增/改写的规范文本 MUST 对 `scan-confirmation-gates.py` 的阻断模式零新增命中；冻结的 total 与相等判定必须保持绿色。采用**设计规避**（换措辞/按路径引用），不得扩大豁免集。 | 预算余量为 0 是已实测约束（`.specify/shared/guidelines/confirmation-gates.md` 与对应契约测试）；放宽门禁等于把「响亮失败」换回「静默分歧」。 |
| **A-13** | **不动的面**：不自动 kill/stop 活进程；不推送、不合并、不删除分支、不改写远端；不删除/覆盖证据；不改 SDD 阶段链、授权与两槽位预算。 | 简报的 non-goals 与破坏性动作纪律；watcher 只读、处置归驱动者（watch-model §0/§3）。 |
| **A-14** | **测试经济**：新增测试经唯一入口 `scripts/bash/run-tests.sh` 运行，不新增第三个全量槽位；用确定性夹具/假 CLI/事件文件，不用固定 `sleep`。 | owner：`.specify/shared/guidelines/test-execution-efficiency.md`、sdd-loop-driver 的两槽位预算。 |
| **A-15** | **命名**：`silent-end` 是新概念名；**plan 阶段 wrap-up 经 `glossary-utils.py --action add`（先 `detect-conflict`；`origin=auto`、`status=proposed`）提议**，结构冲突即停并交用户裁定，不在本规格内直接写入 `.specify/glossary.md` 的确认态；implement 阶段 wrap-up 为后备检查点。本规格的定义在该词条被确认前对本特性有效，确认后由词汇表条目接管语义引用。 | 词汇表「提议 ≠ 落地」；`status=proposed` 即既有用户确认通道形态；无人值守流程不得被确认门卡死。 |
| **A-16** | **Feature 绑定在 `/speckit.clarify` 完成**：requirements 阶段保持 `Need clarification`；clarify 阶段绑定 Feature 095（切片行 106，`Draft`），不新建 Feature。 | Feature Integration Protocol 的绑定时点在 clarify；绑定依据见 `## Clarifications` Session 2026-11-25。 |
| **A-17** | **并发读数**：本阶段是一个执行体、单叶、无派发，按 `single-unit` 记录 `requested=1` / `effective=not_evaluated` / `effective_reason=single-unit`。 | owner：`subagent-definitions.md` § The Concurrency Obligation。 |
| **A-18** | **无人值守**：不向用户提问；所有取舍记录在本表；实现阶段遇到需要裁定的歧义按 fast-fail 停在异常点上报，不得就地发明意图。 | 简报的 unattended 约束。 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 后台执行体无论怎么结束，父侧都能拿到一个可区分的结果 (Priority: P1)

父代理派发一个后台执行体后继续自己的工作。执行体可能正常完成、失败、显式报异常、被取消、还在跑，也可能**消失得无影无踪**——被杀、宿主丢失、包装脚本崩溃、返回通道断掉。父代理在汇报前逐个结算自己开过的尝试：每种结束都有对应的值；「还在跑」必须带着当下可复核的活证据；「消失了但没有任何结论」必须显示为静默终止，而不是成功、失败或仍在运行。

**Why this priority**: 这是用户请求的语义核心。没有这一步，后面的报告、重试与守卫都建立在「我们能区分状态」这个未验证前提上。

**Independent Test**: 用同一载体构造完成、失败、异常、取消、存活、静默消失六类夹具，逐类断言结算值与证据指针；其中静默消失夹具必须得到 `silent-end`（证据不可读时为 `unknown`），且 `completed`/`failed`/`running` 计数为 0。

**Acceptance Scenarios**:

1. **Given** 一个后台尝试已结束且留下终止成功记录与可核验交付物，**When** 父侧结算，**Then** 得到 `completed`，并携带终端记录与独立核验的指针。
2. **Given** 一个后台尝试的进程已消失、没有任何终止/失败/异常/取消记录，**When** 父侧结算，**Then** 得到 `silent-end`（或证据不可读时 `unknown`），并携带「尝试已开始」「执行主体已消失」「无终态证据」三类指针。
3. **Given** 一个后台尝试仍在运行且 pid 存活、心跳或活日志新鲜，**When** 父侧结算，**Then** 得到 `running` 且携带当下活证据；**同时** 一个只有旧读数、没有再验证的尝试不得被报成 `running`。

---

### User Story 2 - 每个后台派发载体都产出足以结算的证据，且只有一套契约 (Priority: P1)

维护者检查所有派发入口：SDD 驱动的 fork 载体、外部 CLI 的 subprocess 载体、团队席位、宿主后台 native 任务、直接外部配方。每个载体要么已经产出四件套/三件套，要么补齐加性的起点与终止证据；每个入口都引用同一个结算 owner，没有哪个技能或命令私藏第二张判定表。virtual 与前台同步调用被显式排除并写明理由。

**Why this priority**: 只在一条载体上修静默退出，等于把问题挪到另一条路径；而每个入口各修一套，等于制造若干会漂移的第二真源。

**Independent Test**: 每个后台可脱离载体各有一个静默消失夹具；全部夹具经同一判定面得到同一封闭值集合中的结果；载体清单之外的入口被守卫判红。

**Acceptance Scenarios**:

1. **Given** 一个包装脚本被 SIGKILL、只留下停止增长的日志且没有终止记录，**When** 检查其起点/存活/终止证据，**Then** 能从既有或新增的加性记录证明「执行主体已消失」，并结算为 `silent-end`。
2. **Given** 任一派遣入口的文本，**When** 静态检查其引用的结算 owner，**Then** 全部指向同一处，且不存在第二份状态值表或第二份证据矩阵。
3. **Given** virtual 模式的派发，**When** 检查是否创建后台结算边，**Then** 不创建，且文本明确写出排除理由与此模式下「未完成不得报成功」的义务。

---

### User Story 3 - 检测到静默结束后，反应是显式且不可静默修复的 (Priority: P2)

操作者看到父代理的报告：每一个子尝试都有结算；还在跑的子尝试被标为「未结算」，死掉但无结论的被标为静默终止并附证据指针；失败、异常、未知同样显式。父代理可以选择重试，但重试是新尝试、新 label，旧证据保留；也可以停止，但停止遵守既有破坏性动作纪律；它不会偷偷补一个「成功」、不会把旧尝试的晚到返回当成本次结果、不会为了让报告好看而删证据。

**Why this priority**: 检测到静默终止却静默处理，只是把不可见性从执行期挪到报告期。

**Independent Test**: 在一次包含静默终止的模拟运行中，检查报告是否逐项列出结算与证据；检查重试是否产生新 label 且旧证据仍在；检查是否发生自动 kill、证据覆盖或旧返回消费（均应为 0）。

**Acceptance Scenarios**:

1. **Given** 一个子尝试结算为 `silent-end`，**When** 父代理汇报，**Then** 报告显式上送该尝试、证据指针与可选处置，且不使用成功语气。
2. **Given** 父代理决定重试，**When** 新尝试启动，**Then** 使用新 label，旧尝试的结算与证据保留，且重试理由被记录。
3. **Given** 一个旧尝试在新尝试启动后才返回，**When** 父代理收集结果，**Then** 旧返回不被当成本次结果消费，旧尝试保持自己的结算值。

---

### User Story 4 - 静默终止能让一条检查转红，而不是只在文档里被禁止 (Priority: P2)

维护者运行契约测试：删掉「静默终止检测」、删掉「活证据要求」、或让 `unknown` 冒充通过，至少一条测试转红；每个载体都有对应的确定性夹具与反向夹具（活着的尝试不得被误报为静默终止）。守卫不能因为读不到证据就返回绿色。

**Why this priority**: 一条无法转红的规则只是散文；本特性存在的意义之一就是把「silent orphaning is a defect」从声明变成可执行判定。

**Independent Test**: 执行变异演练：逐项移除检测行为并运行测试，记录转红项；对每个载体运行活/死两组夹具，确认无误报与漏报。

**Acceptance Scenarios**:

1. **Given** 一个声明 `completed` 却没有完成证据的尝试行，**When** 运行判定守卫，**Then** 退出非零并点名缺失的证据。
2. **Given** 判定面无法读取某个证据路径，**When** 运行判定守卫，**Then** 得到 `unknown` 类发现而不是通过。
3. **Given** 移除「静默终止检测」实现，**When** 运行契约测试，**Then** 至少一条转红，且转红项被记录为演练证据。

---

### User Story 5 - 客户项目升级后拿到同一契约，旧记录不被假装成合规 (Priority: P3)

下游维护者升级框架后：新增的字段/文件是按加性方式出现的；旧报告与旧尝试没有被改写，但在审计中被明确标为 legacy；任何不兼容的路径/字段/状态行变化都有迁移路径或确定性拒绝；框架源、模板与本仓运行副本一致，镜像不靠手改。

**Why this priority**: 没有迁移与旧记录处置，升级会把「以前看不出来」变成「以前假装看得出来」，反而更危险。

**Independent Test**: 用一份旧格式夹具与一份新格式夹具运行审计，断言旧记录被标 legacy、新记录按契约判定；对每个不兼容变更执行其迁移/拒绝夹具。

**Acceptance Scenarios**:

1. **Given** 一份无结算契约版本的历史运行报告，**When** 审计，**Then** 被标 legacy，且不被计为符合新契约，也不被改写。
2. **Given** 一份不兼容的字段变更未附迁移/拒绝行为，**When** 运行变更闭包检查，**Then** 检查转红并点名该变更。

---

### Edge Cases

- **退出码 0 但无哨兵/无完成声明**：属「结束了但没有完成证据」，结算为 `failed`（incomplete），不是 `completed`，也不是 `silent-end`（结束被观测到了，缺的是交付）。
- **哨兵在但产物缺失**：伪完成候选；独立核验失败即不得算 `completed`。
- **进程被 SIGKILL**：无终止记录、pid 已消失 → `silent-end`；若启动宽限期内 pid 从未出现，同样按 `silent-end`，而不是「仍在启动」。
- **包装脚本捕获到 SIGTERM 并写出终止记录**：按记录结算（非零 → `failed`）；只有父侧经既有破坏性纪律显式取消时才可记 `cancelled`。
- **pid 被复用或已僵尸**：不算存活；没有终止记录时按 `silent-end`，不得因 `kill -0` 成功就报 `running`。
- **期限之后的晚完成**：在既有 deadline grace 内出现终止/哨兵证据时按新证据重判；宽限耗尽仍无终态才判静默终止类结果，不得提前宣布消失。
- **进程活着但长时间无输出**：pid/心跳新鲜即 `running`；日志静默本身不产生 `silent-end`，也不单独产生超时。
- **证据不可读（权限/解析失败）**：`unknown` + 上送；不得回退成 `completed`、`failed` 或 `running`，也不得返回绿色。
- **父代理自身死亡**：后续会话必须能凭既有持久载体重建尝试并结算；缺起点记录的尝试被标 legacy/`unknown`，不得补写成 `completed`。
- **多子执行体聚合**：任一子尝试的 `silent-end`/`unknown` 不得被聚合成功语气覆盖；每个子尝试独立结算、独立留证。
- **派发前失败（前置检查拒绝、配置解析失败）**：不是一次「已开始的尝试」，应产出派发前失败记录，不产生 `silent-end`，也不进入重试计数。
- **observer 不在场**：观察者只记录事实，不是结算前提；没有 observer 的线仍必须结算。
- **宿主不提供后台 native 形态**：该模式声明为前台终结，工具返回即终止事件；不得伪造一个「后台结算边」。
- **同一次运行的并发重试**：两个尝试并存时各自独立结算；旧尝试的晚到返回永不覆盖新尝试。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 结算契约（Settlement Contract）

- **FR-001**: 每一次后台派发尝试 MUST 在父侧得到**恰好一个**结算值，取值来自封闭集 {`completed`, `failed`, `anomaly`, `cancelled`, `running`, [[STR-001]], [[STR-002]]}；集合之外的值 MUST 被拒绝；`running` 为非终态，`unknown` 为检测缺陷态而非结束。
- **FR-002**: `completed` MUST 只在存在**正完成证据**时成立：终端成功记录 **且** 对所需交付物/返回的独立核验通过（例如驱动 U4 的产物校验、团队 `## Verification`、五要素上行齐备）；仅有退出码 0 MUST NOT 构成完成。
- **FR-003**: `failed` MUST 只在存在**正失败证据**时成立：非零终端记录、带具名原因的失败返回，或退出码 0 但缺少所需完成证据（incomplete 类）；日志缺失、无输出或沉默 MUST NOT 被读作失败。
- **FR-004**: `anomaly` MUST 只在存在**显式异常信号**且有终端证据时成立（如最后非空行以 `ANOMALY:` 开头、或显式异常返回）；进程仍活时出现的异常行只表示 `anomaly=observed`，该尝试仍为 `running`，不得提前终态化。
- **FR-005**: `running` MUST 只在**结算时刻复核过的活证据**下成立（pid 存活且非僵尸/未复用、心跳新鲜、活日志在声明阈值内增长、返回通道仍开放之一）；陈旧读数或未复核 MUST NOT 被报成 `running`。
- **FR-006**: [[STR-001]] 是「执行主体已消失且完成/失败/异常/取消证据全部缺席」的显式异常终态；对没有 pid 的载体，它是「声明等待期限已过、无返回且无活信号」。它 MUST NOT 被折算成 `completed` 或 `failed`，也 MUST NOT 被报成「仍在运行」。
- **FR-007**: [[STR-002]] MUST 在证据不可读/不可解析时产出，点名不可读的证据指针；它不是一个结束，且 MUST 携带与 [[STR-001]] 相同的「不得声称成功」反应。
- **FR-008**: `cancelled` MUST 只来自父侧经既有破坏性动作纪律产生的显式取消记录；进程死亡、提前退出或连接断开 MUST NOT 被推断为取消。
- **FR-009**: 每次尝试 MUST 有唯一 label；一次重试 MUST 是**新尝试、新 label**；旧尝试的证据 MUST 保留；旧尝试的晚到返回 MUST NOT 被当作当前尝试的结果消费。
- **FR-010**: 父侧 MUST 在派发前或派发时把尝试身份、载体、父身份、开始时间与（进程载体的）pid 记入**既有父侧载体**；缺起点记录的尝试无法证明「曾经存在」，其结算 MUST 为 [[STR-002]] 而不是 `completed`。返回通道（含七字段角色的 `return_channel`）是**子侧发起**的上行，其沉默 MUST NOT 被读作存活或完成；父侧结算的依据是尝试记录 + 活证据/期限 + 载体终止记录，而不是「等一个可能永远不来的返回」。
- **FR-011**: 父侧在自身对外可见的完成报告之前 MUST 结算它开过的每个尝试；任一尝试无结算即使父侧报告不完整，其成功结论 MUST NOT 成立。

#### B. 载体一致性（Carrier Conformance）

- **FR-012**: § Dispatch Carrier Inventory 是**封闭清单**；后台派发 MUST 落在某个已列载体上；新增/移除载体 MUST 修订本规格，临时发现的第五类载体不得静默加入。
- **FR-013**: 每个派发入口（`/speckit.agents`、`/speckit.team`、SDD 驱动阶段派发、直接外部配方）与每个有派发职责的定义（技能、命令、coordinator/supervisor 类 agent 模板）MUST 引用同一个结算 owner；任何技能/命令/模板/文档/测试 MUST NOT 携带第二张状态值表、第二份证据矩阵或载体私有的判定副本；叶子执行者模板 MUST NOT 因此获得第二套结算逻辑。
- **FR-014**: C-1 fork 载体 MUST 继续以四件套与 watcher 判定作为载体证据源；本特性 MUST 消费它们，且 MUST NOT 改变 `watch-target.sh` 的判定、退出码、哨兵字面量或 `--self-test`；U4/U5 与 065a 的恢复动作仍归驱动者。
- **FR-015**: C-2 subprocess 载体 MUST 产出**加性**的起点/存活/终止证据，使结算可导出：至少包含尝试身份、pid、开始时间的起点记录，以及正常退出与可捕获信号下的终止记录保证；既有 `.status` 行格式与三件套语义 MUST 对旧消费者保持可读，新证据不得改变旧格式。
- **FR-016**: C-2 的结算 MUST 按证据成立：成功终止记录 + 已核验返回 → `completed`；非零终止记录 → `failed`；退出 0 但无完成声明 → `failed`（incomplete），不得 `completed`；无终止记录 + 已记录 pid 消失（或启动宽限内从未出现）→ [[STR-001]]；证据不可读 → [[STR-002]]。
- **FR-017**: C-3 团队运行 MUST 在运行报告的 `## Execution Detail` 映射表中为**每个被派发席位**记录结算值 [[STR-003]] 与证据指针（加性列/加性行），并在 `## Verification` 声明结算覆盖；缺少席位行或结算的运行报告 MUST 被判不完整，不得以成功语气收尾。
- **FR-018**: C-4 native MUST 在派发时留下尝试记录，并在返回时结算：五要素缺任一 → `failed`（incomplete）且不得消费；宿主报错 → `failed`；超过声明的等待期限仍无返回且无活信号 → [[STR-001]]；宿主不提供后台形态时，该模式 MUST 显式声明为前台终结，工具返回即终止事件。
- **FR-019**: C-5 virtual MUST 被显式排除在后台结算之外并写明理由：它不能脱离会话、父侧就是执行者、不存在孤儿边；同时父侧 MUST NOT 把未完成的 virtual 工作报成 `completed`。
- **FR-020**: C-6 直接外部配方 MUST 只提供两种形态：使用合规 runner/wrapper 产出终止证据的后台形态，或把配方显式限制为「前台返回即终止」；后台配方 MUST 修正「超时无哨兵＝stall」的含混表述——无哨兵且执行主体已消失/无终止记录 → [[STR-001]]（不可读为 [[STR-002]]），无哨兵但进程仍活 → `running`。
- **FR-021**: 只读验证波（分析 fan-out 等）MUST 对每个校验者结算；缺失状态或结果 → `failed`（incomplete）并按既有规则重问，MUST NOT 从波次结果中静默消失。
- **FR-022**: observer（096）MAY 记录结算事实，但 MUST NOT 成为唯一结算载体；没有 observer 的线仍必须结算；本特性不新增 probe class 或 handler binding。

#### C. 反应义务（Reaction Obligations）

- **FR-023**: 结算为 [[STR-001]] 或 [[STR-002]] 时，父侧 MUST 显式上送异常类报告（发现什么、为何吃重、已产生的中间产物、可选处置），MUST NOT 声称成功，MUST NOT 未加诊断就按普通失败原样重派。
- **FR-024**: 重试 MUST 只以新尝试/新 label 发生；旧证据保留；既有重试上限不变；对 [[STR-001]]/[[STR-002]] 的重试 MUST 附带具名诊断或用户裁定（fast-fail：异常停不是普通失败）。
- **FR-025**: 停止/终止/取消 MUST 遵守既有破坏性动作纪律；watcher MUST NOT 杀进程；对活尝试选择「不再等待」时 MUST 记录 `running` + 活证据 + 停止理由，MUST NOT 记成 [[STR-001]]。
- **FR-026**: 禁止静默修复：不得代写他人终止记录、不得补齐缺失返回字段、不得改写 `.status`/报告/证据、不得删除证据、不得把 [[STR-001]]/[[STR-002]] 改写成 `failed`/`completed`、不得消费过期返回。
- **FR-027**: 父侧成功报告 MUST 携带子尝试的结算覆盖（逐项值与证据指针）；仍在跑的必须标为「未结算」；失败、异常、[[STR-001]]、[[STR-002]] 必须逐项上送，不得被聚合语气覆盖。

#### D. 可执行判定与证据（Enforcement）

- **FR-028**: MUST 有一个确定性、只读的结算判定面，从既有载体为每个尝试给出结算与证据发现；它 MUST 零写入、零新存储，分类表 MUST 只有一个 owner 并被测试钉住。
- **FR-029**: 判定面 MUST 接入至少一条能转红的守卫，覆盖：集合外值；无完成证据却声称 `completed`；无活证据却声称 `running`；无「消失+缺席」证据却声称 [[STR-001]]；被派发却无结算行；[[STR-002]] 被当成通过。判定面 MUST 是 `scripts/python/role-edge-check.py` 的**加性扩展**（其 owner 页即本特性修订的 superagent 定义页；违规种类由封闭四类扩为「四类边违规 + 结算违规集合」）；引擎今天不读的载体证据（C-2 加性起点/终止记录、C-4 尝试记录、C-6 runner 记录）在 plan 中要么加性接入同一引擎的输入集，要么在 plan 记录「既有 owner 不覆盖」裁定；该裁定落盘之前 MUST NOT 引入第二判定引擎。
- **FR-030**: MUST 有变异演练：移除/削弱「静默终止检测」「活证据要求」「unknown 不得通过」「证据指针要求」中任一项，至少一条测试 MUST 转红；演练 MUST 留证。
- **FR-031**: 每个清单内的后台载体 MUST 有至少一个确定性测试模拟其静默终止形态并断言结算与反应；缺测试的载体 MUST 被判缺陷。
- **FR-032**: 测试 MUST 经 `scripts/bash/run-tests.sh` 运行、使用确定性夹具/假 CLI/事件文件而非固定等待，并 MUST 同时断言正向与反向（活着的尝试不得被误报为静默终止）。

#### E. 兼容、迁移、文档与范围（Compatibility & Scope）

- **FR-033**: 既有哨兵字面量、watcher 判定/退出码/`--self-test`、五要素上行、七字段下行、破坏性动作纪律与其冻结预算、两槽位测试预算 MUST 保持不变（允许差异集为空集）；所有新增字段/文件 MUST 为加性。
- **FR-034**: 新格式记录 MUST 以**加性字段**声明结算契约版本 [[STR-004]]（随结算承载记录声明，MUST NOT 改动既有行格式）；无该版本的旧尝试/旧报告 MUST 在结算判定/审计输出中被标为 legacy 且 MUST NOT 被报成符合新契约；dated record MUST NOT 被改写；legacy 标注本身 MUST NOT 产生失败退出码（它不是拒绝）。
- **FR-035**: 任何对既有路径/文件/字段/状态行契约的不兼容变更 MUST 附带迁移路径或确定性拒绝，并 MUST 有测试；MUST NOT 出现静默混合态。
- **FR-036**: 两顶帽子：改动 MUST 落框架源与模板；本仓 `.specify/` 镜像经既有同步/安装流程再生，不手改；客户项目经 init/refresh 获得同一契约。
- **FR-037**: 文档 MUST 更新唯一 owner 章节、引用它的技能/命令与 `docs/reference/` 页面；取值与代码一致；MUST NOT 复制第二份集合/映射。
- **FR-038**: 零新增机制：不新增调度器、守护进程、队列、注册表、通知通道、存储或 child list；复用既有载体、判定引擎与报告面；observer 保持可选。
- **FR-039**: 扫描面上新增/改写的规范文本 MUST 对 `scan-confirmation-gates.py` 的阻断模式零新增命中；冻结 total 与相等判定 MUST 保持绿色；只允许设计规避，不得扩大豁免集。
- **FR-040**: 非目标 MUST 保持：不自动 kill/stop 活尝试，不推送/合并/删除分支/改写远端，不删除证据，不改 SDD 阶段语义与授权，不回溯改写历史报告/规格。
- **FR-041**: 范围封闭与诚实：载体清单与结算值集合在本规格内封闭；新发现的载体或判定 MUST 走规格修订；无法机械断言的义务 MUST 标为行为类并指定评审/变异演练义务，MUST NOT 声称已被守卫覆盖。

### Key Entities *(include if requirement involves data)*

- **Dispatch Attempt（派发尝试）**：一次有唯一 label 的后台派发；属性含父身份、载体、起点证据、终止证据、结算值、证据指针、契约版本。重试产生新的 Attempt，旧 Attempt 保留。
- **Settlement Verdict（结算判定）**：A-3 的封闭值之一；区分「终态」「非终态」「检测缺陷」三类语义，任何输出都不得省略。
- **Evidence Bundle（证据束）**：载体特定的证据集合——C-1 的四件套 + 日志 + watcher 判定，C-2 的三件套 + 加性起点/终止记录，C-3 的报告行 + 席位返回，C-4 的返回与尝试记录，C-6 的 runner 记录；每个结算值必须指名其证据来源。
- **Reaction Record（反应记录）**：对非 `completed` 结算的上送/重试/停止动作及理由；重试必须指向新的 Attempt，停止必须指向既有纪律。

### Dispatch Carrier Inventory (closed)

| ID | 载体 / 入口 | 可后台脱离 | 现有证据 | 本特性处置 |
|----|-------------|-----------|----------|-----------|
| **C-1** | SDD 驱动阶段派发（fork；`skills/external/sdd-loop-driver/scripts/stage-runner.sh` + `watch-target.sh`） | 是 | 四件套 + 哨兵 + watcher 判定 + 065a 中断形态 | 保持载体契约不变；补齐结算消费与测试 |
| **C-2** | 外部 CLI subprocess（`skills/internal/create-team/scripts/dispatch.sh`；run-agent 外部派发、团队席位、验证波共用） | 是 | `.live.log` / `.jsonl` / `.status`；无 pid/起点/心跳；status 只在正常走到末尾时写 | 加性起点/存活/终止证据 + 结算判定 |
| **C-3** | 团队运行（`/speckit.team`；席位经 C-1/C-2） | 是 | 运行报告 `## Execution Detail` 映射表、`## Verification` | 每席位结算列 + 覆盖声明 |
| **C-4** | native 子代理（`/speckit.agents`，宿主管理） | 宿主提供后台形态时是，否则否 | 工具返回；无持久尝试记录 | 父侧尝试记录 + 期限/无返回结算；前台终结显式声明 |
| **C-5** | virtual 子代理（会话内模拟） | 否 | 内联返回 | **显式排除**；保留「未完成不得报成功」义务 |
| **C-6** | 直接外部配方（`external-dispatch-recipes.md` Recipe 3/4/7 与同类直驱） | 是 | runner 哨兵/日志；后台轮询 | 只允许「合规 runner 后台形态」或「前台返回即终止」；修正 stall 表述 |

### Settlement Evidence Matrix

| Settlement | 必须存在的正证据 | 明确不能作为该判定证据的读法 |
|------------|------------------|------------------------------|
| `completed` | 终端成功记录 **且** 独立核验通过的交付物/返回（五要素齐备 / U4 / 团队 Verification） | 仅 exit 0；仅日志末尾好看；仅父侧期望 |
| `failed` | 非零终端记录；或具名失败返回；或 exit 0 但缺完成证据 | 无输出；日志停止增长；父侧等待超时 |
| `anomaly` | 显式异常信号 + 终端证据 | 仍存活时的中间异常行（只记 observed） |
| `cancelled` | 父侧经既有纪律写下的取消记录 | 进程死亡；连接断开；提前退出 |
| `running` | 结算时刻复核的活证据（pid + 僵尸/复用检查、fresh heartbeat、活日志增长、开放返回通道） | 陈旧读数；上次看到还活着；未检查 |
| `silent-end`（[[STR-001]]） | 起点记录 + 执行主体消失 + 完成/失败/异常/取消证据全部缺席；或无 pid 载体的等待期限已过且无返回无活信号 | 「没看到输出」；「进程不在」但未核对起点/证据；未到期限 |
| `unknown`（[[STR-002]]） | 证据不可读/不可解析的指针集合 | 任何成功、失败或仍在运行的推断 |

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增第三方运行时依赖，交付定义、技能/命令文本、报告字段、判定行为与契约测试，并消费既有 shell/Python 标准库、唯一测试入口、既有 watcher/状态引擎与既有判定引擎。表中 `Premises` 引用的 `EP-NNN` 由 plan 阶段 `## Execution Premises` 定义（本阶段不建 premises 表）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|----|----------|
| RS-001 | 既有 SDD 驱动 watch/判定证据面（四件套、哨兵、判定与退出码） | in-scope | 既有驱动技能源（本特性只消费判定，不改语义） | 不适用（仓内实现） | `skills/external/sdd-loop-driver/scripts/watch-target.sh` | watcher `--self-test` 100%；判定 token/退出码/哨兵集合与基线相等；结算映射零语义改动 | FR-014, FR-028, FR-029 | EP-001 |
| RS-002 | 既有 subprocess 派发包装（三件套与加性起点/终止记录） | in-scope | 本特性修改的框架源包装脚本 | 不适用（仓内实现） | `skills/internal/create-team/scripts/dispatch.sh` | 旧消费者读到的 `.status` 行格式不变；SIGKILL 夹具得到 [[STR-001]]；起点记录在场 | FR-015, FR-016, FR-021 | EP-002 |
| RS-003 | 既有父侧报告/返回载体与边判定引擎（团队报告、run-agent 返回、role-edge 判定） | in-scope | 本特性修改的框架源技能与判定引擎 | 不适用（仓内实现） | `scripts/python/role-edge-check.py` | 每个尝试有结算与证据指针；缺证据行转红；legacy 行被标注而非通过 | FR-010, FR-017, FR-018, FR-028, FR-029 | EP-003 |
| RS-004 | 唯一测试入口与既有测试套件 | in-scope | 既有测试基础设施（本特性只新增测试） | 不适用（仓内实现） | `scripts/bash/run-tests.sh` | 新增测试经该入口运行；两槽位预算不变；同夹具重复运行结算一致 | FR-031, FR-032 | EP-004 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 对清单内每个后台可脱离载体的「执行主体消失且无终态证据」夹具，结算结果为 [[STR-001]]（证据不可读时为 [[STR-002]]），`completed` 与 `running` 误判数均为 0。**Path**: final
- **SC-002**: 在合规运行夹具中，每个被派发尝试恰有一个封闭集结算值与证据指针 [[STR-003]]；任一尝试缺值、缺证据或声称 `completed` 而无完成证据时，守卫退出非零；零个无证据行通过。**Path**: final
- **SC-003**: 以基线提交 `fbab7a45c` 为参照物，用同一抽取器从实现后的文件抽取 watcher 判定 token 集合、退出码集合与哨兵字面量集合，三个集合均逐成员等于基线集合（允许差异集为空集，补集断言即「成员差集为空」）；`watch-target.sh --self-test` 通过率 100%；抽取器读取的输入恰为 `skills/external/sdd-loop-driver/scripts/watch-target.sh` 及其 `--help` / `--self-test` 输出。**Path**: supporting
- **SC-004**: 反应演练中，100% 的 [[STR-001]]/[[STR-002]] 夹具产生显式上送；自动 kill 次数为 0；重试均使用新 label 且旧证据保留；旧尝试晚到返回被消费的次数为 0。**Path**: final
- **SC-005**: 清单内每个后台可脱离载体都有确定性一致性测试与结算映射（覆盖率 100%），未分类载体数为 0；native 的前台终结分支与 virtual 的排除理由各有断言。**Path**: supporting
- **SC-006**: 新格式记录声明 [[STR-004]]；旧格式记录被标 legacy 且被计为符合新契约的行数为 0；源/模板/已安装副本一致；每个不兼容变更都映射到一条被测试的迁移/拒绝行为。**Path**: supporting
- **SC-007**: 新增测试全部经 `scripts/bash/run-tests.sh` 运行，且不新增第三个全量槽位；同一夹具重复运行的结算判定差异数为 0；固定等待型新增测试数为 0。**Path**: supporting
- **SC-008**: 活体夹具（pid 存活、心跳/活日志新鲜）在所有后台可脱离载体上被误报为 [[STR-001]] 的次数为 0；长时间静默但存活的尝试保持 `running`。**Path**: supporting
- **SC-009**: `scan-confirmation-gates.py` 的 total 保持冻结基线值且相等判定测试保持绿色；本特性新增的阻断模式命中数为 0。**Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 / SC-008 Source**: 每个载体一套「活 / 死 / 半死（pid 丢失或复用）」夹具，写入 `test-evidence/`；断言结算值与证据指针；对活体夹具断言不出现 [[STR-001]]。实现阶段与 review 阶段各运行一次。
- **SC-002 Source**: 判定守卫的夹具运行输出（JSON：每个 attempt 的结算、证据指针、findings）；含一个「声称成功但无证据」的反向夹具与一个「无结算行」夹具，断言退出非零。读数写入 `test-evidence/`。
- **SC-003 Source**: 以 `fbab7a45c` 为基线的抽取脚本输出（判定 token 集合、退出码集合、哨兵字面量集合）与实现后抽取结果的集合比较；`watch-target.sh --self-test` 输出。一次实现、一次 review。
- **SC-004 Source**: 反应演练脚本输出：上送条目、重试 label 列表、旧证据文件哈希、自动 kill 审计（应为空）、旧返回消费记录（应为空）。一次实现、一次 review。
- **SC-005 Source**: 载体清单 × 测试文件的覆盖矩阵（人工核对 + 静态检查断言每个载体 ID 至少被一个测试引用）；native 前台分支与 virtual 排除的断言。实现一次。
- **SC-006 Source**: 旧/新格式夹具的审计输出；`sync-mirrors.py --check` 与安装流程的既有读数（如实报告绝对漂移，断言本特性触及面零新增）；不兼容变更清单 × 迁移/拒绝测试的映射表。实现与 review 各一次。
- **SC-007 Source**: `scripts/bash/run-tests.sh` 的运行报告（选择集、耗时、失败名单）；同一夹具两次运行的判定 diff；新增测试的静态扫描（无固定 `sleep`）。实现与 review 各一次。
- **SC-009 Source**: `scripts/python/scan-confirmation-gates.py` 的输出与冻结基线比较；对应契约测试的退出码。实现与 review 各一次。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "silent-end" | FR-006, FR-023, FR-024, FR-029, SC-001, SC-004, SC-008 |
| `STR-002` | "unknown" | FR-007, FR-023, FR-024, FR-029, SC-001, SC-004 |
| `STR-003` | "end_state" | FR-017, SC-002 |
| `STR-004` | "settlement_version" | FR-034, SC-006 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-11-25（无人值守 clarify 阶段，Feature 绑定与残留歧义裁决）

- Q: `Related Feature` 绑定到哪个既有 Feature，是否新建？ → A: 绑定 Feature 095（Super Agent Role），以索引切片行 106 登记 `Draft`（先例：097/100/105 的 slice-row 形态）；不新建 Feature，父行状态保持 `Ready for Review` 不回退。依据：095 拥有本特性修订的 `superagent-definitions.md` § Termination 与拟扩展的 `role-edge-check.py`；058 只拥有 C-1 载体与 watcher 判定（本特性明令不改），064 拥有生命周期/归属，065 拥有中断恢复，均非结算契约 owner。095 无既往切片 → 本规格为其首个切片；直接 scope-match 优先于「无同主题兄弟」的 create 信号。
- Q: A-15 的 `silent-end` 词条如何在「用户确认通道」中提议、何时落地？ → A: 不在本阶段写 `.specify/glossary.md` 的确认态；plan 阶段 wrap-up 经 `glossary-utils.py --action add`（先 `detect-conflict`，`--origin auto --status proposed`）提议，结构冲突即停并交用户裁定（glossary protocol §3）；implement 阶段 wrap-up 为后备检查点；确认前本规格定义有效（A-15 已记录）。
- Q: FR-028/FR-029 的确定性结算判定面复用哪个既有引擎？ → A: 复用 `scripts/python/role-edge-check.py` 作为唯一判定引擎（零写入只读、已读团队报告映射表/驱动 sidecar 与四件套/run-agent dispatch record/registry 交叉校验、退出码 0/1/2 天然承载「干净 / 违例 / 不可读→[[STR-002]]」），违规种类在其 owner 页由封闭四类扩为「四类边违规 + 结算违规集合」；对引擎今天不读的载体证据（C-2 加性记录、C-4 尝试记录、C-6 runner 记录），plan 只能加性接入同一引擎，或先记录「既有 owner 不覆盖」裁定才可引入第二引擎（A-6 保持成立）。
- Q: A-10/FR-034 的 legacy 标注落在哪个面，客户项目是否需要显式拒绝路径？ → A: 三分闭合：版本声明 = 加性字段随结算承载记录声明（不改既有行格式）；legacy = 只在结算判定/审计输出中标注，旧记录不改写、不计合规、**不产生失败退出码**；拒绝 = 证据不可读由 [[STR-002]] 承担唯一确定性拒绝语义，不新增预造拒绝机制——不兼容活面变更被 FR-033 的允许差异集（空集）禁止，未来若发生则由 FR-035 强制自带迁移/拒绝与被测行为。
