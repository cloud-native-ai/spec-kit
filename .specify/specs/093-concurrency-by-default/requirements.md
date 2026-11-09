# Requirements Specification: subagent 并发作为框架基本属性（默认并发）

**Requirement Branch**: `093-concurrency-by-default`
**Created**: 2026-11-09
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（编写/修订 `skills/internal/**`、`skills/external/**`、`templates/commands/**`、`agents/` 与 `.specify/agents/templates/`、以及 SDD 驱动者派发模型的作者）、下游项目里被这些技能与命令编排的维护者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 在判定「一个执行体是否必须并发」「什么理由允许串行」「并发单元怎么切、写域怎么隔离、槽位与校验预算怎么定、失败怎么隔离与重入」「怎样证明并发是真的发生了」时打开本规格，据 FR-001…FR-033 与 SC-001…SC-012 决定 `/speckit.clarify` 与后续实现是否放行
**Input**: User description: "在当前 speckit 框架中的所有技能、命令和更高阶的 goal、team、loop 等，都需要将 subagent 并发作为基本属性；在能用并发的情况下默认都应该是并发的。"

## Related Feature *(mandatory)*

**Feature ID**: 093
**Feature Name**: Concurrency by Default（subagent 并发作为框架基本属性）

## Overview

框架里已经有大量并发能力：064 的写线/worktree 与 integration queue、070 的 Work Package 拆解与 `wp-gate.py`、092 的 goal/team 平行模型。但这些能力是**少数执行体的特权**，不是框架的基本属性：`/speckit.implement` 由 `implement-feature` 技能驱动时仍是单代理逐任务串行（091 实测：62 个任务、一个代理、116 分钟、触达 500 回合上限），`plan` / `implement` / `review` 之外的阶段不自带拆解规则，技能与命令的默认形态是「一个执行体一条线做完」。更糟的是**声明与执行脱节**：092 的 plan 声明「6 包并行」，而执行它的 subagent 没有派发工具（见本 Agent 定义自身的 "Never dispatch another agent"），于是 6 包被单协调器串行完成——形式上「并行」，风险上等于串行，且没有任何检查会发现这件事。

用户诉求把三件事一次纠正到位：

1. **范围是封闭集**——所有技能、命令、goal、team、loop 都必须把 subagent 并发作为基本属性，不是「部分执行体可选增强」；
2. **默认值是并发**——只要依赖、写域、宿主能力与预算允许，默认就并发，串行必须**携带具名理由**且可被机械判别；
3. **声明必须等于执行**——一个声明了多个并发单元的执行体必须真的能并发执行；「声明并行、实际串行」不是可接受的降级，而是一种缺陷，必须被契约测试判红。

本特性不新增 `/speckit.*` 命令、不新增第二套调度引擎或 registry、不改变 SDD 阶段链与哨兵（状态脊 `non_goals` 已声明），它把既有并发机制从「少数执行体的特权」提升为「所有执行体的默认形态」，并把串行变成一次需要举证的例外。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 任何技能、命令、goal、team、loop 都默认并发 (Priority: P1)

一个维护者打开任一执行体（`/speckit.implement`、`/speckit.plan`、`/speckit.docs`、`sdd-house-keeping`、`sdd-project-setup`、`run-team`、`sdd-loop-driver`……），都能读到同一套并发契约：执行体现在由哪一个**声明类别**（见 [[STR-002]]）覆盖，该类别要求的并发单元划分是什么，什么情况下它必须并发、什么情况下允许串行，以及它的串行理由必须落在哪里。

**Why this priority**: 这是用户诉求的第一句。「基本属性」若不能被逐执行体判定，它就只是一句口号；范围不封闭，任何实现都可以指着某一个漏掉的执行体说「它不在范围内」。

**Independent Test**: 对一个由仓库文件系统枚举出的执行体全集（技能目录、命令模板、goal/team 相关技能与模板），逐个断言它能被映射到恰好一个声明类别，并断言该类别在其文件中给出一条可读的并发义务；把一个执行体从清单中移除或把某个声明类别改成「无义务」时测试转红。

**Acceptance Scenarios**:

1. **Given** 仓库中任一技能、命令模板、goal/team/loop 执行体，**When** 执行一次程序化枚举并按决策表判定，**Then** 它落在且只落在一个声明类别的成员集里，且该类别声明的并发义务在它的正文或它按指针引用的 owner 中可寻址。
2. **Given** 一个由决策表判为「零并发单元」的执行体（例如一次单文件只读查询），**When** 它给出串行理由，**Then** 该理由取自定义过的理由码封闭集（[[STR-003]]），并可被程序读取。
3. **Given** 一个既无并发声明、也无具名串行理由的执行体，**When** 运行契约测试，**Then** 测试转红并指名该执行体。

---

### User Story 2 - 默认并发，串行必须携带具名理由 (Priority: P1)

当执行体确实面对两个以上互不依赖的单元、写域互不重叠、宿主能并发、预算允许时，它默认并发执行；任何串行执行都必须声明一个取自封闭词表的理由码，并给出可复核的依据（依赖边、写冲突、宿主无并行能力、验证/预算保留）。

**Why this priority**: 与 User Story 1 同级——没有默认值，「基本属性」会退化为每个执行体自行裁量；没有具名理由，串行就无从判别、也无法在实现期被反向检查。

**Independent Test**: 用两个夹具驱动同一个执行体：一个「两个互不依赖单元 + 不相交写域 + 宿主可并发」，断言它并发派发；一个「存在依赖边」，断言它串行且记录理由码与依据；再把串行理由替换为空或词表外的值，断言门禁判红。

**Acceptance Scenarios**:

1. **Given** 两个以上 ready 且写域不相交的单元，**When** 执行体调度，**Then** 并发执行（并发度受 `<槽位上限>` 与预算约束），且状态记录里 `pattern` 为并发形态、`reason` 为空。
2. **Given** 任一单元依赖另一单元完成，**When** 执行体调度，**Then** 依赖解除前不派发该单元，且串行理由码为 `dependency-edge`。
3. **Given** 两个单元声明了重叠写域，**When** 执行体调度，**Then** 它们不被同时派发，或整体切到写隔离形态（见 FR-013）；理由码为 `write-conflict`；MUST NOT 静默丢弃其中一单元。
4. **Given** 宿主无法发起并行调用，**When** 执行体调度，**Then** 记录 `host-no-parallel` 并串行执行，MUST NOT 声称并行。
5. **Given** 一个串行结果，其理由码为空、词表外或依据缺失，**When** 运行契约测试，**Then** 测试转红并指名该结果。

---

### User Story 3 - 并发单元必须可划分、可隔离、可独立校验、可确定性集成、可失败隔离与重入 (Priority: P1)

对每一类执行体，可并发的单元如何切（package/segment 划分）、写域如何隔离（worktree 或 disjoint territory）、槽位上限与校验者保留如何定、每单元如何独立完成与独立校验、集成顺序如何确定、单单元失败如何不拖垮兄弟单元与如何重入——这些都由规则给出，而不是由执行体临场裁量。

**Why this priority**: 并发若没有这七件事，只是一堆互相踩踏的进程：写冲突、无法复核的完成声明、随机集成顺序、一次失败连带整阶段重做。用户诉求第三条把这几件事列为「每类执行体都需要」。

**Independent Test**: 对一个声明为「多单元」的执行体，喂入一个含两个独立写单元 + 一个依赖单元 + 一个失败单元的夹具，断言：写入隔离生效、并发度不超过槽位上限、校验者独立、集成顺序与声明顺序一致（与派发时刻无关）、失败单元的兄弟单元继续完成、重入不重派已完成单元。

**Acceptance Scenarios**:

1. **Given** 两个写单元同时 ready，**When** 使用共享树隔离形态，**Then** 写单元串行执行（有效并发 1）；**When** 使用 worktree 隔离形态，**Then** 每个单元占独立工作树，集成交给既有串行队列。
2. **Given** 一个已完成的单元，**When** 判定其完成，**Then** 由非该单元执行者的独立校验者给出 verdict；没有 verdict 即未完成。
3. **Given** 单元 A、B 的派发顺序为 B 先返回、A 后返回，**When** 集成，**Then** 集成顺序按声明顺序（而非返回时刻），且在重跑时得到同一顺序。
4. **Given** 一个单元失败或超时，**When** 处置，**Then** 无关的兄弟单元不被取消、其完成状态被记录；依赖该失败单元的单元保持阻塞；失败完成两次即上送。
5. **Given** 一次中断后的重入，**When** 重读状态，**Then** 已完成单元不被重派。

---

### User Story 4 - 具备派发能力的执行体才允许声明并发；禁止「声明并行、实际串行」 (Priority: P1)

框架的 agent 定义、阶段席位、技能与命令执行体，要么自身具备派发能力（能创建兄弟执行体），要么把派发显式交给驱动者/主代理。一个被声明为多单元并发的计划，必须由真的能并发派发的一方执行。

**Why this priority**: 这是 092 实测缺陷的直接纠正——6 包 plan 声明并行，却被一个没有派发工具的协调器单线程执行完。没有这一条，前三条都可以被「形式上满足、执行上落空」地绕过。

**Independent Test**: 对一个声明了多单元的执行体定义做静态检查：若它声明并发单元，则其能力集里必须含派发类工具，或其正文必须显式把派发交给具备该能力的上位执行体；再对 092 形态做复现——给一个「声明 6 包、执行者无派发能力」的夹具，断言门禁判红而不是静默串行。

**Acceptance Scenarios**:

1. **Given** 一个 agent 定义声明「执行 N 个单元」，**When** 静态检查其能力集，**Then** 它含派发能力，或声明了上位派发者；两者都没有时判红并指名。
2. **Given** 一个执行体声明其单元并发，**When** 执行记录显示所有单元由同一执行者顺序完成且无并发证据，**Then** 该结果被判为「声明与执行不一致」并上送，MUST NOT 记为通过。
3. **Given** 一个无派发能力的执行体，**When** 它被指派一项需要多单元的职责，**Then** 框架 MUST 把该职责路由给可派发的一方（驱动者/主代理），而不是让其吞下并串行完成。

---

### User Story 5 - 并发有效性被真实验收：至少一个真实执行体跑出并发与确定性集成 (Priority: P2)

验收不能只靠文档与静态断言：至少一个真实（非夹具）执行体必须留下并发执行的可判定读数——并发的单元数、各自独立校验、确定性集成顺序、总耗时相对串行基线的对照。

**Why this priority**: P2 而不是 P1，因为它依赖前四条落地；但它不可省——没有它，前四条可以是「加了契约测试、但从未在真实运行上发生过」的纸面能力（092 plan 的实测就是先例）。

**Independent Test**: 取本特性自身或紧随其后的真实 SDD 运行，其 implement 阶段按 ≥2 个并发单元执行，产出协调报告与逐单元 verdict，并给出串行基线对照读数（091 的 62 任务/116 分钟）与并发读数。

**Acceptance Scenarios**:

1. **Given** 一次真实运行的 implement 阶段，**When** 阶段完成，**Then** 协调报告给出并发单元数、单元级 verdict、集成顺序与耗时读数；缺失的量化项写作未评估，不写 0 或估计值。
2. **Given** 该运行证据，**When** 与串行基线对照，**Then** 并发形态被明确记录（并发单元数 ≥ 2 且实际重叠），MUST NOT 仅以「声明并发」充当证据。

---

### Edge Cases

- **单单元阶段**：阶段只有一个可表示单元——允许单单元形态，但 MUST 仍然记录决策（`single-unit` 与理由），MUST NOT 把「恰好一个单元」伪装成并发已发生。
- **恰好两个单元但写域相交**：并发不成立，串行理由 MUST 是 `write-conflict` 而非 `dependency-edge`；MUST NOT 为了凑并发把相交的写域声明成不相交。
- **宿主具备并行但预算不足**：预算耗尽的最后一个单元——并发度 MUST 被压到剩余允许额度，理由码 `budget-reserve`；MUST NOT 超出声明的槽位上限。
- **计划 N 个单元、实际只跑 2 个**：并发条件 (a) 只要求 `>= 2`，因此「2 个单元真并发」在形式上合规——**但这不是**「声明 N 个、实际并发」的证明。一次运行的实际生效并发度 `>= 2` 而计划单元数 `N > 实际派发的单元数` 时，未派发的单元 MUST 逐个有记录（已完成并带 verdict、被依赖阻塞、或已失败），**MUST NOT 靠缩小单元集来换取「并发已发生」的结论**（SC-006 的取证因此要求把计划单元数与实际派发单元数一并记录）。
- **校验者保留位被并发单元吃满**：`verifier reserve` MUST 从槽位上限中先扣除；扣完后小于 2 时该执行体退化为串行并记录 `budget-reserve`，MUST NOT 让校验等待全部单元结束。
- **单元失败后兄弟成功**：失败单元依赖者阻塞、无关兄弟继续；重入时已完成兄弟不重派，失败单元按重试规则处理。
- **重试与拆分**：一个单元连续失败两次后拆分，拆分深度为一，拆分后的子单元不再拆分、不再自动重试；子单元失败即阶段失败。
- **串行理由互相矛盾**：同时记录 `host-no-parallel` 与「已并发派发」——MUST 判为不一致并上送，MUST NOT 二者并存。
- **goal/team/loop 层**：一个 goal 的多个 target **在 FR-005 的四条并发条件成立时** MUST 默认并发执行；「互相独立」MUST 由 FR-005 的 (b) 依赖边与 (c) 写域判定回答，MUST NOT 在 FR-005 之外再定义一个「独立性」谓词（否则 goal 层会有一套判据、其他执行体另一套）。team 的席位写领地相交 MUST 在席位绑定阶段被判红，而不是运行时靠席位自觉避让；**实测缺口**：本仓 12 个 team 定义里有 2 个（`demo-seat-dispatch`、`requirement-implement-monitor`）在树内完全不出现 territory 声明——对它们，绑定阶段判定的输入是「未声明」，该情形 MUST 按 FR-012 的「未声明写域即判红」处理，MUST NOT 因「没有领地所以不会相交」而放行。
- **零并发单元的执行体**：如一次只读查询——它 MUST 被明确归为「无可并发单元」并给出决策记录，MUST NOT 因为「没有单元」而从范围清单里消失。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 范围封闭集与判定方式

- **FR-001**: 框架 MUST 把 subagent 并发确立为**所有**执行体的基本属性。范围 MUST 覆盖下列**五个枚举根**（枚举根 = 一个由文件系统派生的目录，其成员即执行体集合，判定见 FR-003）：技能根 `skills/{internal,external}/<name>/`、命令模板根 `templates/commands/<stem>.md`、agent 定义根 `agents/`（其 `.specify/agents/templates/` 投影由 FR-032 的镜像纪律覆盖）、team 定义根 `.specify/teams/<slug>/`、goal 定义根 `.specify/goal/<slug>/`。每个枚举根到其执行体类别的映射 MUST 记录在 [[STR-008]] 的同一条条目内（FR-033），MUST NOT 由逐目录硬编码决定。MUST NOT 把任一执行体类别整体排除在范围外；某个类别的并发义务形态可以不同（例如 goal 的单元是 target），但「有义务、且义务是可判定的」对每一类都成立。
- **FR-002**: 一个执行体是否属范围、以及它的并发义务为何，MUST 由一条**声明层判定**回答，MUST NOT 由逐执行体硬编码的白名单回答；判定面 MUST 由 `shared/declarations/` 中的条目承载并经既有声明读取入口消费（见 FR-033），MUST NOT 新增第二份清单文件或第二套类别表。
- **FR-003**: 执行体的范围 MUST 由**文件系统枚举**派生（技能目录、命令模板目录、agent 定义目录），MUST NOT 由一份手写的执行体清单给出；枚举与其成员集 MUST 有漂移守卫——新增一个技能或命令而未覆盖时，契约测试 MUST 转红（封闭清单声明五要件，owner `.specify/shared/guidelines/closed-set-claims.md`；基线参照物为枚举时刻的目录快照）。
- **FR-004**: 每个执行体 MUST 被映射到**恰好一个**声明类别（[[STR-002]]，其封闭成员集由 [[STR-001]] 承载），映射 MUST 由可判定的判定规则给出（按执行体所属层次与其产出形态），MUST NOT 由作者自行挑选；无法映射的执行体 MUST 被报告为未覆盖并判红，MUST NOT 落进一个「其他」兜底类别。 类别表本身是 [[STR-001]]（`"concurrency-class"`），其语义名是 [[STR-002]]。

#### B. 默认并发与具名串行理由

- **FR-005**: 执行体在**并发条件成立**时 MUST 默认并发执行。并发条件 MUST 同时成立且逐条可判定：(a) 就绪单元数 `>= 2`；(b) 单元之间不存在未满足的依赖边；(c) 写单元的写域两两不相交，或执行体声明了写隔离形态；(d) 宿主具备并行派发能力，或采用外部进程形态；(e) 扣除校验者保留位与预算后的可用槽位 `>= 2`。
- **FR-006**: 任一并发条件（FR-005 (a)…(e)）不成立时允许串行，但**串行 MUST 携带一个取自封闭词表 [[STR-003]] 的理由码与一条可复核依据**（依赖边、写域交集、宿主能力探针结果、槽位与预算读数）；理由码 MUST 是机读字段，MUST NOT 只写在散文里。词表与并发条件 MUST **一一覆盖**：FR-005 的每一条件各有且仅有一个同名理由码，FR-006 的每一理由码各对应且仅对应 FR-005 的一个条件，双向缺口数 MUST 为零——一个条件没有理由码，或一个理由码没有触发条件，都是缺陷。该词表的唯一成员集由 [[STR-003]] 的声明条目拥有（FR-033），本规格 MUST NOT 再列一份副本。一次串行**可以**由多个条件同时不成立造成（例：宿主无并行能力且请求预算不足）。此时记录 MUST 允许**一个有序理由码列表**：成员按上述一一映射的声明次序排列，列表成员 MUST 全部取自词表、MUST NOT 重复；只有没有任何条件不成立时才允许空列表（该形态本身判红，见 FR-007）。MUST NOT 为了迁就单一字段而丢弃次要原因，也 MUST NOT 用列表长度冒充并发度记录（[[STR-005]] 仍是唯一并发度来源）。

- **FR-007**: 一条**无 [[STR-003]] 理由码、理由码列表为空、列表成员落在词表外**的串行结果 MUST 被契约测试判红。依据的**非空或可判定** MUST 落在理由码**所属条件**的取证形态上，而不是任何非空字符串即通过（「有依据」若只判非空，一个 `.` 就能过关）：`dependency-edge` 的依据 MUST 是可解析的依赖边（前置单元 id 与其完成 verdict 指针）；`write-conflict` 的依据 MUST 是可解析的写域交集（相交路径集）；`host-no-parallel` 的依据 MUST 是运行期能力探针读数及其落点；`budget-reserve` 的依据 MUST 是扣保留位前后的槽位与预算读数；[[STR-009]]（`"single-unit"`）与 [[STR-010]]（`"mechanism-not-yet-landed"`）的依据 MUST 是枚举出的可表示单元集（规模为 0 或 1）。依据缺失或形态对不上其理由码时 MUST 判红；反之，一条**并发形态却携带串行理由**或**串行形态却无理由**的记录 MUST 判为不一致（SC-003）。
- **FR-008**: 并发形状下 MUST 记录**[[STR-005]]**：请求的并发度、实际生效的并发度与生效理由三者 MUST 同时记录，MUST NOT 只记录其中之一；实际值以真实同时派发的单元数为准，MUST NOT 以声明值或配置值充数。**「真实同时」的判据** MUST 是逐单元的时间区间：每个单元的派发时刻与返回时刻构成一个区间，实际生效并发度 = 这些区间上**重叠数目的最大值**（同一时刻的重叠计数，不是区间宽度之和除以总时长）；一个单元的时间区间缺失时，该次运行的实际生效并发度 MUST 记为**未评估**，MUST NOT 由声明值、并发度配置或相邻运行推算填补。生效理由 MUST 是「为何实际值 `<` min(槽位上限, 天花板, 剩余预算)」的具名说明（含因失败隔离、提前返回等导致的低于计划值）。
- **FR-009**: 执行体 MUST NOT 因「更简单」「更可控」「历史上就是串行」而选择串行——这类理由不在 [[STR-003]] 的封闭词表内，MUST 被判红；词表扩展 MUST 以修订声明层条目与本规格的形式进行，MUST NOT 由执行体自行扩充。

#### C. 并发单元：划分、隔离、槽位、校验、集成、失败隔离与重入

- **FR-010**: 每类声明的并发形执行体 MUST 给出**单元划分规则**：一条可从权威产物确定性派生的规则（单元由什么派生、单元规模的界、单元的标识与依赖边如何得出），使同样的输入重跑得到同一组单元与同一边集合；MUST NOT 允许按派发时刻或模型裁量临时切包。
- **FR-011**: 单元的**就绪判定** MUST 只由已记录的完成 verdict 与证据指针回答，MUST NOT 由执行者自述、会话记忆或派发先后推断；一个依赖的 verdict 缺失或不可读时，其依赖方保持阻塞并被记录。
- **FR-012**: 每个单元 MUST 具备**写域声明**（可写路径集）；一个既非只读又不声明写域的单元 MUST 被判红，MUST NOT 以「大概是这些文件」代替声明。**写域 MUST 是文件级路径集，MUST NOT 是目录级区域**：一个以目录名（`skills/internal`、`shared/` 这类）为写域的单元 MUST 被判红，因为两个单元各写同一目录下的不同文件在目录级声明上看似相交、在文件级声明上并不相交，而目录级声明又是既有的**声明（declared）与交付（delivered）不一致**的常见来源（本仓 070 的 `sync-mirrors.py`、086 的 `templates/instructions-template.md` 均由不同特性在同一目录下各自修改过）。只读单元 MUST 声明空写域（与 `decomposition-model.md` WP-02 的 `kind=read-only` 不变量同形）。
- **FR-013**: 写隔离 MUST 由**两种已定义的形态**之一给出：共享树形态（写单元独占执行，有效并发 1）或 worktree 形态（每个写单元占独立工作树与独立写线）；一个并发声明 MUST 指名所用形态，MUST NOT 让执行者临场选择。
- **FR-014**: 槽位上限 MUST 由一个**声明值**给出，MUST 有唯一定义点（不出现第三处取值），且 MUST 有一个由既有并发上限机制约束的天花板；实际并发度 MUST NOT 超过 `min(槽位上限, 天花板, 剩余预算)`。**这两个取值面各自 MUST 只引用一个 owner**，且由于现存三处约束会互相收紧，plan MUST 先裁定谁拥有哪一个：实测 2026-11-09，`stage-team-preset.md` 写 `slot_cap_ceiling: "min(6, the line's remaining concurrency allowance owned by Feature 064)"`、`wp-gate.py` 的 `--slot-cap-ceiling` 默认值为 4 且 `WG-16` 校验 `1 <= slot_cap <= ceiling`、`decomposition-model.md` §365 允许临时 team 模式传 `min(effective_concurrency, 24)` 而其余运行保持 `min(4, line remaining)`——四处说法并存时，「唯一定义点」不是通过再添一处来达成，而是通过点名哪一处是 owner、其余为投影。本规格 MUST NOT 自行选定数字；实际并发度的算式（`min` 三者）是本规格唯一新增的合成规则。
- **FR-015**: 每个并发单元 MUST 从槽位预算中**保留至少一个校验位**；扣除保留位后的可用槽位数 `< 2` 时，执行体 MUST 退化为串行并记录理由码 `budget-reserve`，MUST NOT 用「校验与执行同一时刻同一执行者」来绕过保留。
- **FR-016**: 每个单元 MUST 有**独立完成判定**与**独立校验**：完成判定 = 该单元自己的完成信号 + 该单元的证据指针；校验 MUST 由**非该单元执行者**的全新上下文复核者给出，且校验者 MUST NOT 是该单元的派发者本身；单元 verdict MUST NOT 替代阶段级验收。校验者的**独立性结论** MUST 在派发前由记录给出：单元记录携带 `executor_id` 与 `verifier_id` 两个互不相同的标识（一个校验者可复核多个单元，但复核者集合与执行者集合 MUST 无交集），「新上下文」由此判读；只写「独立校验通过」而不落这两个标识的通行记录 MUST 被判为**无法判定独立性**并判红，MUST NOT 计为已校验。
- **FR-017**: 集成的顺序 MUST 是**声明决定的确定性顺序**（依赖分层的展平序），MUST NOT 是派发时刻顺序或返回时刻顺序；同一组单元在重跑时 MUST 得到同一集成顺序（含并列单元的确定性破平规则）。
- **FR-018**: 单元失败 MUST 被**隔离**：一个单元失败、超时或预算耗尽 MUST NOT 取消无关的兄弟单元，MUST NOT 阻塞与它无依赖关系的就绪单元；依赖失败单元的单元 MUST 保持阻塞并记录阻塞原因；失败 MUST 按既有上送规则被显式报告。
- **FR-019**: **重入** MUST 从已记录状态继续：已完成的单元 MUST NOT 被重派，进行中但来源不可达的单元 MUST 被判定并报告，MUST NOT 从会话记忆重建进度；重试计数 MUST 由其记录派生，MUST NOT 依赖独立计数器文件。
- **FR-020**: 每个单元 MUST 有**预算与轮次上界**，一个单元耗尽其预算 MUST NOT 静默延长，也 MUST NOT 把整个阶段的剩余预算挪给单个单元；上界取值 MUST 有唯一定义点。

#### D. 派发能力：声明即执行

- **FR-021**: 一个执行体若声明「并发推进 N（N >= 2）个单元」，它 MUST 满足下列之一：(a) 其定义的能力集含派发类工具（即具备 [[STR-004]]），能自行创建兄弟执行体；(b) 其正文显式把派发交给具备 (a) 的上位执行体（驱动者/主代理），并声明该移交的形态；(c) 它采用外部进程形态的真实并行。三者皆无时，并发声明 MUST 被判红。 本条的判定键是 [[STR-004]]；协调者可派发性的单一裁定处是 [[STR-011]]（`"coordinator-dispatch-verdict"`），两者 MUST NOT 互相替代。
  一台宿主**能**为某个执行体提供派发工具，本身就是一条「该执行体声明并发」的证据来源：一旦宿主在运行期把 N>=2 个单元交给同一执行体，而该执行体的定义不满足 FR-021 (a)/(b)/(c)，该次执行 MUST 判为声明与执行不一致（FR-023），**MUST NOT 因为「执行体定义里没有写并发」而免检**。可见性反例（本仓实测 2026-11-09，登记为 F-093-003）：`agents/` 下的 § Responsibilities 对每个协调者与执行者逐字写着「Never dispatch another agent」，而同文件 frontmatter 的 `capability-tools:` 列出 `Read, Grep, Glob, Bash, Write, Edit`（无派发工具）——静态能力字段与正文禁令**一致**，却与 092 的「6 包并行」声明**矛盾**；框架 MUST 先裁定「协调者是否可派发」，再谈任一协调者声明并发（裁定见 [[STR-011]]（`"coordinator-dispatch-verdict"`）的 owner 条目）。

- **FR-022**: 框架的 agent 定义（`agents/**` 与其 `.specify/agents/templates/` 投影）、阶段席位（阶段团队预设的席位）与各技能/命令执行体，MUST 逐类被判定为「可派发」或「移交派发」，判定结果 MUST 可从定义本身读出（[[STR-004]] 能力键或其指针），MUST NOT 需要运行期探测才知道。
- **FR-023**: 「声明并行、实际串行」MUST 是一种**可判红的缺陷**，不是可接受的降级：一次执行若声明了 N>=2 个单元，而其记录显示所有单元由同一执行者顺序完成、无并发重叠证据，MUST 被判为声明与执行不一致并上送；MUST NOT 把该结果计为并发证据。
- **FR-024**: 一项需要多单元推进的职责，若被指派给不满足 FR-021 的执行体，框架 MUST 把它路由给可派发的一方，MUST NOT 让接收者独吞并逐单元串行完成；路由判定 MUST 由可判定规则给出并留记录。
- **FR-025**: 本特性 MUST NOT 削弱既有的反嵌套纪律：一个阶段执行体仍 MUST NOT 启动或承载 SDD 运行，派发链深度不变；「获得派发能力」不等于「获得承载驱动的资格」。

#### E. 高阶执行体（goal / team / loop）

- **FR-026**: goal 执行体 MUST 把**独立的 target** 默认并发推进：目标之间无依赖且写域不相交时 MUST 并发；有依赖时 MUST 串行并给理由码。并发成立与串行理由 MUST 复用 FR-005 / FR-006 的同一套条件与词表（本规格 MUST NOT 为 goal 另立一套判据，见 FR-032）。goal 的整体完成判定 MUST 仍是「全部 target 达成」，MUST NOT 因为并发而放宽；一个 target 失败时其余 target 的处置 MUST 按 FR-018 的失败隔离规则记录（已完成兄弟不被取消、依赖者保持阻塞）。
- **FR-027**: team 执行体 MUST 在**席位绑定阶段**判定并发可行性：多个席位的写领地相交 MUST 在绑定时被判红（MUST NOT 等到运行时靠席位自觉避让），席位占用的槽位 MUST 计入槽位上限，报告席、校验席 MUST 从槽位预算中扣除。
- **FR-028**: loop 执行体（含 `sdd-loop-driver`、`sdd-house-keeping`、`sdd-project-setup`、任何周期性或长跑循环）MUST：(a) 把并发作为其默认推进形态；(b) 记录**每一个推进单元**的有效并发度与理由码——记录面 MUST 是「单元」而不是「轮」，因为实测三类执行体的推进颗粒互不相同：`sdd-loop-driver` 按阶段与 Work Package 推进、`sdd-house-keeping` 按**条目**推进（保留期清理的对象是记录条目，没有轮次）、`sdd-project-setup` 按**步骤**推进（引导步骤之间有的是依赖边）；把记录面写成「每轮」会使前两类无处落账，从而用「无轮次」掩盖「未记录」；(c) 在多阶段串行的依赖理由上给出理由码而不是静默串行。阶段链本身与哨兵 MUST NOT 改变。
- **FR-029**: 既有拆解规则的**阶段覆盖**（[[STR-007]]）MUST 被重新判定：当前内置缺省只对 `plan` / `implement` / `review` 启用、`requirements` / `tasks` 的规则须显式开启；本特性 MUST 让「有可并发单元」的阶段在不违反 FR-005 条件时默认拆解，未覆盖的阶段 MUST 有具名决策记录，MUST NOT 因为缺省 `off` 而静默串行。**取值面 MUST 与既有状态脊键对齐**：本线的状态脊实测已带 `decomposition` / `decomposition_stages: [plan, implement, review]` / `decomposition_slot_cap` 三个键（见 `.specify/state/093-concurrency-by-default.md` 的 `project_config` 段），因此 [[STR-007]] 的声明条目 MUST 指明它与这三个键的关系（取代 / 投影 / 并列），MUST NOT 产生第四处「哪些阶段拆解」的取值；`decomposition` 的取值域与三种单包决定（`single-package|disabled|fallback`）归 `decomposition-model.md` §9 与 [[STR-007]] 条目，本规格只引用。

- **FR-030**: 本特性 MUST 为 FR-001…FR-033 的每一条「可判定」断言提供契约级或单元级测试，且每条测试 MUST 在实现缺失或回退到串行缺省时转红；只有措辞变化的检查 MUST NOT 被计为取证。
  本特性 MUST 产出**至少一个真实执行体的并发读数**（非夹具）：一份协调报告，含并发单元数、逐单元 verdict、确定性集成顺序、耗时，以及与串行基线（091 的实测：62 任务、单代理、116 分钟）的对照；缺失的量化项 MUST 写为未评估。

- **FR-031**: 本特性 MUST 按 [[STR-006]] 的落点纪律在框架源码侧落地并镜像同步（`skills/`、`agents/`、`shared/`、`scripts/` 的源与其 `.specify/` 投影）；`templates/` 的模板中立性 MUST 保持（MUST NOT 写入本仓专有路径事实）。concurrency-class 五条条目中 `"+'+'+"serial-reason 五条条目中 `"+'+'+"effective-concurrency 五条条目中 `"+'+'+"decomposition-coverage 五条条目中 `"+'+'+"executor-enumeration-roots 由 [[STR-006]] 记录其落点（本条即 [[STR-006]] 的落点纪律本身），并分别以 [[STR-001]] / [[STR-003]] / [[STR-005]] / [[STR-007]] / [[STR-008]] 为语义名。
  本特性引入的判定面 MUST 各有一个**声明层条目**（`shared/declarations/facts/`）或一个已有的唯一 owner。四个判定面与它们的条目 slug 逐条绑定：**并发类别表 [[STR-001]]**（[[STR-002]] 是其语义名）、**串行理由码词表 [[STR-003]]**（含 FR-006 的一一映射与声明次序）、**槽位与保留位取值**（FR-014、FR-015、FR-020 的唯一定义点）、**单元划分规则标识**、以及 [[STR-008]] 载 `"executor-enumeration-roots"`，承载「枚举根 → 执行体类别」映射；[[STR-004]] 与 [[STR-005]] 的语义名各有一个 owner 路径（FR-022 / FR-008），MUST NOT 落在第二处取值上。**登记语义 MUST 以读取入口的实际行为为准，而不是以「条目文件存在」为准**：实测 2026-11-09，`declaration_reader.py --action list` 返回的是 `contract.yaml` **自身的键**（`fact_kinds` / `exit_codes` / …）加 `facts/` 目录里的 slug，二者共用一张清单；因此「登记」MUST 有一个可判定的读取面——要么在 `contract.yaml` 为该 slug 落一个键，要么由读取入口把 `facts/` 的 slug 列为已登记。两处都缺席时该 slug MUST 按 `owner-unavailable` 处理（退出码 2），MUST NOT 取缺省值（实测：`--action get --fact concurrency-class` 现返回 `no declaration for fact 'concurrency-class'`、退出码 1，那正是未登记形态）。登记前的探测 MUST 是本规格的产出一环，MUST NOT 假定条目文件一落地即可读。

- **FR-032**: [[STR-006]] 的概念 owner MUST 复用既有文档：subagent 与执行模式归 `.specify/shared/definitions/subagent-definitions.md`，拆解与调度归 `skills/external/sdd-loop-driver/references/decomposition-model.md`，团队与席位归 `skills/internal/create-team/references/conceptual-model.md`，goal 与 target 归 `.specify/shared/definitions/goal-definitions.md`；本特性 MUST 改写这些 owner 而非新建第二处定义，其余面 MUST 只引用不复述（宪法 XIV）。
  **goal 执行体的落点 MUST 按既有 owner 判定，MUST NOT 由本规格另立一层**。实测 2026-11-09，`goal-definitions.md` 声明 goal 持久化在 `.specify/goal/<goal-slug>/`，而本特性的 spec 树里存在 `.specify/specs/093-concurrency-by-default/goal/<slug>/goal.md`（092 同形）；这一层是由 085 的 spec-local 临时 team/goal 协议产生的**投影**，其所有者与生命周期归该协议。因此 FR-026 的「goal 执行体」MUST 显式区分为：`.specify/goal/` 的**存档目标**与 spec-local 的**临时目标**，两者的 target 并发规则相同，但后者的存在性、删除与迁移 MUST 由 085/092 的 owner 回答，本特性 MUST NOT 假定它长期存在，也 MUST NOT 把它当作第七个枚举根。

- **FR-033**: 既有并发语义的处置清单 MUST 先列全再动手：064 的写线/worktree/integration queue、070 的 Work Package 与 `wp-gate.py` 检查面、092 的 goal/team 平行模型、086 的测试执行效率；凡被本特性改变默认值的，MUST 逐条给出处置（改写 / 保持 / 显式移除）与理由，MUST NOT 让既有契约测试静默失效。 该纪律即 [[STR-006]] 的处置面；本条要求处置记录随同 [[STR-006]] 条目更新。 词表成员中的 [[STR-010]] 本身也是本条登记面的成员。
  本特性的收尾自身 MUST 遵守同一纪律：任何一次由本特性发起的多单元推进 MUST 记录其有效并发度与理由码；本特性 MUST NOT 以「机制尚未落地」为由在自己的运行里声明并发却串行完成（该情形 MUST 记录 [[STR-010]] 事实，而不是伪装成并发）。


### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时——它消费既有的 Python 引擎、既有 pytest 运行器、既有声明读取入口与既有文件系统能力。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库（文件系统枚举、声明读取、JSON 判定） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 既有 `requires-python`；本特性零新增第三方依赖 | `pyproject.toml` | 枚举与判定在同一解释器上跑通 | FR-002, FR-003, FR-033 | EP-001 |
| RS-002 | `pytest`（契约测试与夹具） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 既有 `pytest` 依赖；零新增依赖 | `pyproject.toml` | `pytest -m contract` 在 `>=3.8` 上通过 | FR-030, FR-031 | EP-002 |
| RS-003 | 既有声明读取入口 `scripts/python/declaration_reader.py` 与新声明条目 | in-scope | 本特性自身（新增 `shared/declarations/facts/` 条目并登记 `contract.yaml`） | 不适用（无外部版本面） | `shared/declarations/contract.yaml` | 未登记条目按 `owner-unavailable` 处理，登记后可读 | FR-002, FR-033 | EP-003 |
| RS-004 | 既有 Work Package 门 `skills/external/sdd-loop-driver/scripts/wp-gate.py` 与拆解模型 | in-scope | 本特性自身的修订面（不新增第二个门） | 不适用（无外部版本面） | `references/decomposition-model.md` | 门的 `--help` / `--version` 与未知选项拒绝仍满足宪法 XXI | FR-010, FR-014, FR-017, FR-029 | EP-004 |
| RS-005 | 宿主并行派发能力（原生并行调用或外部进程并行） | signed-contract | 宿主 agent 运行时（框架只消费其能力） | 能力探针结果在运行期记录，MUST NOT 固化在文件里 | `.specify/shared/definitions/subagent-definitions.md` | 探针结果驱动 FR-005(d)，不可用即串行并记理由码 | FR-005, FR-021, FR-023 | EP-005 |

### Key Entities *(include if requirement involves data)*

- **并发单元（Concurrent unit）**: 一次执行体可独立派发、独立完成、独立校验的最小推进单位；承载标识、写域、依赖边、预算上界与证据指针。既有 Work Package 是它的一个实例，本特性 MUST NOT 引入第二个同义记录。
- **执行体（Execution body）**: 一个技能、一个命令执行体、一个 agent 定义、一个 goal/team/loop 推进体；是范围封闭集的成员，通过枚举派生而非手写清单。
- **声明类别（Declaration class）**: 由判定规则把执行体映射到的类别，决定该执行体的并发义务形态；封闭集，新增成员须修订其 owner。
- **串行理由码（Serial reason code）**: 具名说明「为什么这一轮没有并发」的封闭词表成员，携带可复核依据。
- **槽位与保留位（Slot cap and verifier reserve）**: 决定有效并发度的两个上界来源；保留位从槽位中先扣除，是「独立校验」得以成立的预算前提。
- **派发能力（Dispatch capability）**: 一个执行体「能创建兄弟执行体」的能力事实；与「任务声明了并发」配对成立，二者缺一即判红。
- **并发读数（Concurrency reading）**: 一次真实运行产生的并发证据——请求/生效并发度、单元 verdict、集成顺序、耗时与串行基线对照；不可得项写未评估。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 范围封闭且可判定：从文件系统枚举出的执行体全集中，被映射到恰好一个 [[STR-001]] 声明类别的比例为零遗漏——存在任一执行体未被覆盖时该测试转红；把任一执行体从枚举结果中移除后测试仍然转红（双重方向断言）。 本判据的枚举根清单由 [[STR-008]] 承载。 **Path**: final
- **SC-002**: 默认并发成立：对「两个以上就绪、无依赖、写域不相交、宿主可并发、槽位充足」的夹具，执行体必须以并发形态执行并记录 [[STR-005]] 生效并发度 >= 2；把并发判定改为缺省串行时测试转红。 **Path**: final
- **SC-003**: 串行必须有具名理由：夹具中全部串行结果都携带取自 [[STR-003]] 封闭词表的理由码与非空依据；理由码为空、词表外、或与形态矛盾的记录数为零；注入一条无理由串行时测试转红。 **Path**: final
- **SC-004**: 七件事逐项可判定：对一个声明的多单元执行体，单元划分确定性（同输入两次得到同一单元集与依赖边）、写域声明完整性、槽位上限与校验保留位的扣除、独立校验、声明顺序集成、失败隔离、重入不重派——七个断言各自有夹具并在对应实现缺失时转红。 **Path**: final
- **SC-005**: 声明与执行一致：一个声明 N>=2 单元却由单一执行者顺序完成的结果被判为不一致；静态侧对每个声明并发的执行体断言其具备 [[STR-004]] 派发能力或已移交派发，缺失者数为零。092 形态（6 包 plan、执行者无派发能力）作为复现夹具必须在修复前判红、修复后转绿。 **Path**: final
- **SC-006**: 真实执行体并发被取证：至少一次真实（非夹具）运行产出协调报告，含 [[STR-005]] 生效并发度 >= 2、逐单元 verdict、确定性集成顺序与耗时；与串行基线（091：62 任务、单代理、116 分钟）的对照被记录。缺失量化项写作未评估，写成 0 或估计值即判红。 **Path**: final
- **SC-007**: 高阶执行体覆盖：goal 的独立 target、team 的席位领地相交判定、loop 的每轮并发度记录三者各有夹具；把一个高阶执行体的并发判定改回串行缺省时对应测试转红。 **Path**: supporting
- **SC-008**: [[STR-007]] 阶段覆盖可判定：`requirements` / `tasks` 等当前缺省未拆解的阶段，在存在可并发单元时默认拆解并留下决策；未拆解的阶段逐条有具名理由码，理由于缺失时测试转红。 **Path**: supporting
- **SC-009**: 声明层自足：本特性引入的五个判定面（并发类别 [[STR-001]]、串行理由码 [[STR-003]]、槽位与保留位、单元划分规则标识、枚举根映射 [[STR-008]]）各有一个唯一定义点，检索不到第二处取值；把任一条目**从登记面移除**（或使其在读取入口的清单中缺席）时，读取方 MUST 报未登记形态（命令以非零退出码给出具名说明），MUST NOT 回落到缺省值——判据是读取入口的实测行为，不是「注销」这个动作的名字。 **Path**: supporting
- **SC-010**: 既有并发语义处置完整：064 / 070 / 086 / 092 的受影响断言逐条有处置记录（改写 / 保持 / 移除），移除仅限「所断言的事实已被本特性删除」；处置后全套契约测试在 `>=3.8` 上全绿，存在未处置条目时测试转红。 **Path**: supporting
- **SC-011**: 反嵌套未被削弱：派发链深度仍为 2（团队编排 → 调用成员 → 阶段执行体），阶段执行体仍不能启动或承载 SDD 运行；把任一阶段执行体改成可承载驱动时测试转红。 **Path**: supporting
- **SC-012**: 空闲并发的收益可观测：在夹具上，同一任务集以并发形态执行的墙钟耗时低于串行形态，且结果集一致（同样全部完成、同样 verdict）；只有耗时下降而结果集不一致时不计为达成。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 一个枚举型契约测试——程序化枚举技能目录 / 命令模板 / agent 定义目录，按声明类别判定，输出未覆盖清单；空清单为绿。双重方向断言（移除一个执行体仍转红）作为变异证据记录在 `test-evidence/`。
- **SC-002 Source**: 并发夹具（两单元、无依赖、写域不相交）的运行记录：派发时刻表、生效并发度、`pattern` 字段；变异实测（改回串行缺省）记录在 `test-evidence/`。
- **SC-003 Source**: 对全部夹具运行记录的机读扫描——逐条检查理由码是否在封闭词表内、依据是否非空、形态与理由是否互斥；另加一条合成变异记录的实测转红。
- **SC-004 Source**: 七个断言各自的夹具与实测记录（两次运行单元集/依赖边对照、写域声明缺失的拒绝文本、槽位与保留位读数、校验者身份对照、集成顺序对照、失败隔离后的兄弟完成清单、重入后重派计数为 0）。
- **SC-005 Source**: 092 形态复现夹具的判红实测与修复后转绿实测；静态检查对全部声明并发的执行体输出结论清单。
- **SC-006 Source**: 一次真实运行的协调报告（`test-evidence/` 下引用其路径），含并发单元数、逐单元 verdict、集成顺序、耗时；串行基线取自 091 的既有人次记录并注明来源。
- **SC-007 Source**: goal / team / loop 三类夹具的实测记录，与对应变异实测。
- **SC-008 Source**: `requirements` / `tasks` 两个阶段的拆解决策记录与夹具实测；未拆解情形的理由码清单。
- **SC-009 Source**: 声明层条目的登记状态与读取失败实测（注销后 `owner-unavailable`）；第二处取值的检索型断言读数。
- **SC-010 Source**: 064 / 070 / 086 / 092 受影响断言的处置表 + 处置后的 `pytest -m contract` 读数。
- **SC-011 Source**: 反嵌套契约测试（既有测试的保持性断言）与一条注入变异实测。
- **SC-012 Source**: 夹具上的并发/串行两次运行的耗时对照与结果集对照读数，记录在 `test-evidence/`。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"concurrency-class"` | FR-004, FR-031, SC-001 |
| `STR-002` | `"并发类别"` | FR-004（[[STR-001]] 的语义名） |
| `STR-003` | `"serial-reason"` | FR-006, FR-007, FR-009, FR-031, SC-003 |
| `STR-004` | `"dispatch-capability"` | FR-021, FR-022, SC-005 |
| `STR-005` | `"effective-concurrency"` | FR-006, FR-008, SC-002, SC-006 |
| `STR-006` | `"concurrency-contract"` | FR-031, FR-032, FR-033 |
| `STR-007` | `"decomposition-coverage"` | FR-029, SC-008 |
| `STR-008` | `"executor-enumeration-roots"` | FR-001, FR-031, SC-001 |
| `STR-009` | `"single-unit"` | FR-007 |
| `STR-010` | `"mechanism-not-yet-landed"` | FR-033, FR-007 |
| `STR-011` | `"coordinator-dispatch-verdict"` | FR-021 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

**Consumption convention**: a `Consumed by` cell names **definition rows**, and each named row MUST cite the id in its own body as `[[STR-NNN]]`. This specification's verifier enforces both directions: 2026-11-09, a first draft that listed a consumer row which spelled the literal itself reported six such errors in one pass — listing a row is not the same as the row citing.

## Clarifications

### Session 2026-11-09（无人值守 requirements 阶段，自行裁决并记录）

- Q: 用户说的「所有技能、命令、goal、team、loop」范围到底怎么落地——逐条点名，还是给一条判定方式？ → A: 给判定方式。范围由**文件系统枚举**派生（技能目录 + 命令模板 + agent 定义），覆盖性由一条声明层判定回答；逐条点名会立刻与仓库漂移（每加一个技能就漏一个），这正是封闭清单声明纪律要防的失效。（FR-001、FR-002、FR-003）
- Q: 「能用并发」的判据是什么？四种串行理由之后还有别的吗？ → A: 判据是四条件加一条无依赖的槽位条件（FR-005），串行理由取封闭词表 [[STR-003]]：`dependency-edge`（依赖边）、`write-conflict`（写域相交）、`host-no-parallel`（宿主无并行能力）、`budget-reserve`（验证/预算保留）、`single-unit`（可表示单元不足两个）、`mechanism-not-yet-landed`（机制尚未落地，本特性自身运行期的临时事实）。词表封闭，扩展须修订 owner。（FR-006、FR-009）
- Q: 「能力集里没有派发工具」是能力缺失还是要判为缺陷？ → A: 判为缺陷（方案 a 或 b 必须成立）。092 plan 的实测就是这个形态：协调者声明 6 包，自己没有派发工具，于是 6 包被串行完成且无人察觉——这正是用户要纠正的。因此 FR-021 要求能力或显式移交二选一，并在执行记录侧追加一条「声明即执行」的交叉判定。（FR-021、FR-022、FR-023）
- Q: 槽位上限、校验保留位、单元规模界的取值由谁拥有？ → A: 由声明层条目（`shared/declarations/facts/`）+ 既有并发上限机制共同拥有，本规格不发明数字：本规格只要求「有一个唯一定义点 + 不出现第三处取值 + 实际并发度取三者最小值」。具体取值归 plan 阶段的声明条目。（FR-014、FR-015、FR-020、FR-033）
- Q: `requirements` / `tasks` 阶段当前缺省不拆解，是否一律改成拆解？ → A: 不是。改为「存在可并发单元时默认拆解」，未拆解必须留具名理由码。理由：`requirements.md` 与 `tasks.md` 是整体产物（integrator-owned），拆解收益取决于 FR/SC 或任务簇是否真能切分；一刀切会把简单阶段强行拆成一条流水线，收益为负。（FR-029、SC-008）
- Q: 反嵌套纪律会不会被「获得派发能力」意外松掉？ → A: 不会，且必须显式钉住。派发能力只是「创建兄弟执行体」，与「承载驱动」是两件事；本特性在 FR-025 / SC-011 里把既有禁令原样保留并加一条回归断言。（FR-025、SC-011）
- Q: 本特性自己的运行（implement 阶段）还没有机制可用时怎么办？ → A: 记录事实而不是伪装。FR-033 要求以 `mechanism-not-yet-landed` 记录，MUST NOT 用「声明并发」充当并发证据；SC-006 的真实执行体取证因此可能落在本特性之后的一次真实运行上，这一点在本规格中明示。（FR-030、FR-033、SC-006）
- Q: 竞态与并发正确性这里要不要重定义？ → A: 不重定义。并发正确性（隔离、确定性集成、失败隔离）的判据沿用 070 的拆解模型与 064 的写线/worktree 机制；本特性只把它从「三个阶段的可选层」提升为「所有执行体的默认形态」，并补齐缺的默认值与理由码。凡需要改既有语义的，走 FR-033 的处置清单。（FR-013、FR-017、FR-033、FR-032）


### Session 2026-11-09（clarify 阶段 · 访谈式问题自行裁决并记录）

**编号变更通告（append-only 例外：只记事实，不引用已退役的 id）**：本会话把 4 行并入其前一条以保持 id 连续（校验器 `id-contiguous` 拒绝字母后缀），因此 FR 由 36 条变为 **33 条**，SC 维持 12 条，STR 由 7 条增至 **11 条**（新增 `STR-008`…`STR-011`）。并入前后**语义零丢失**：被并入的内容原样保留在其前一条的续行里。旧→新编号的完整映射记录在本阶段的 checkpoint `.specify/specs/093-concurrency-by-default/checkpoints/02-clarify.md` § 6，而不在此处逐条重列——重列会重新引用已退役的 id，使本文件自身的引用解析判红（本轮实测：一致）。

**Mode: A — clarifying `.specify/specs/093-concurrency-by-default/requirements.md`**（`plan.md` 不存在）。同作者条件成立（requirements 与本 clarify 同为无人值守产物）；逐条问题都由**机器读数**驱动（下文每个 → A 都带实测命令结果），未作「读起来像不像有毛病」的猜测。

- Q: 范围封闭集到底枚举什么？原文把 `skills/`（38 internal + 16 external）、`templates/commands/`（29）、goal、team 混在一条里，却没给「枚举什么、按什么归类」的可判定面——「更高级的 goal / team / loop」在文件系统上对应哪些路径？ → A: 给**五个枚举根**并逐条写进 FR-001：`skills/{internal,external}/<name>/`、`templates/commands/<stem>.md`、`agents/`（其 `.specify/` 投影归 FR-031 的镜像纪律）、`.specify/teams/<slug>/`、`.specify/goal/<slug>/`；「枚举根 → 执行体类别」的映射由 [[STR-008]] 的一条声明条目拥有，MUST NOT 逐目录硬编码。实测：`agents/` 17 个定义与 `.specify/agents/templates/` 17 个**逐名相同**；`.specify/teams/` 12 个；`skills/` 两目录各 38 / 16 且每个目录都有 `SKILL.md`。**代价已写进条款**：某一类别（如 goal）的并发单元形态可以不同（单元是 target），但「有义务且义务可判定」对每一类都成立。

- Q: 串行理由码词表与并发条件是否互相覆盖？原文列出 6 个理由码，但 FR-005 的 (d)「宿主具备并行派发能力」在词表里**除了 `host-no-parallel` 还对应哪一条**、以及「一个条件可以同时对应多个理由码」时的记录形态都没定义；清单与条件一旦对不齐，SC-003 的「全部串行结果都有理由」就会在缺口上演成假绿。 → A: 改为**一一覆盖 + 有序列表**：FR-006 要求 FR-005 的每一条件各有且仅有一个同名理由码、每个理由码各对应且仅对应一个条件，双向缺口数为零（词表成员集归 [[STR-003]] 条目，本规格不再列副本）；一次串行可以由多个条件同时不成立造成，故记录面改为**有序理由码列表**（按声明次序、不重复、全取自词表）。**代价已写进条款**：[[STR-009]] 与 [[STR-010]] 不是任何并发条件未成立的结果，它们是「无单元可表示」与「机制未落地」两类事实，故不在「一一映射」约束内——这一点由 [[STR-003]] 条目分 `condition-bound` / `factual` 两组成员表达，SC-003 对两组都要求理由码，只对 `condition-bound` 组要求依据形态。

- Q: 「串行依据非空」能判出什么？原 FR-007 只要求「依据缺失判红」——一个 `.` 就是非空，这条断言于是对任何非空字符串都通过。 → A: 依据 MUST 落在**理由码所属条件**的取证形态上：`dependency-edge` → 可解析的依赖边（前置单元 id + 完成 verdict 指针）；`write-conflict` → 可解析的写域交集（相交路径集）；`host-no-parallel` → 运行期能力探针读数与落点；`budget-reserve` → 扣保留位前后的槽位与预算读数；`single-unit` → 枚举出的可表示单元集（规模 0 或 1）。**代价已写进条款**：这使「依据」从自由文本变成有形状的记录，理由码与依据形态的匹配本身成为一条契约断言（SC-003 的来源同步补上）。

- Q: 「实际生效并发度 >= 2」怎么量？原 FR-008 只说「以真实同时派发的单元数为准」，没给测量面——而 SC-006 的取证正建立在这个数字上；没有定义，一次「6 包里 2 个真并发」也能被读成「并发已发生」。 → A: 判据是**逐单元时间区间的最大重叠数**（派发时刻与返回时刻构成区间，取同一时刻的重叠计数；不是区间宽度之和除以总时长）；任一时间区间缺失时该次运行的实际生效并发度记为**未评估**，MUST NOT 由声明值、配置值或相邻运行推算。并在 Edge Cases 写明「计划 N 个单元、实际只派发 2 个」的情形：并发条件 (a) 只要求 `>= 2`，故 2 个真并发在形式上合规，但未派发单元 MUST 逐个有记录（已完成+verdict / 被依赖阻塞 / 已失败），MUST NOT 靠缩小单元集换「并发已发生」。

- Q: 「独立校验」由谁判、怎么判？原 FR-016 要求「非该单元执行者的全新上下文复核者」，但记录面没有任何字段能证明这一点，一句「独立校验通过」就能过关。 → A: 单元记录 MUST 携带互不相同的 `executor_id` 与 `verifier_id`（一个校验者可复核多个单元，但复核者集合与执行者集合 MUST 无交集）；缺这两个标识的通行记录 MUST 判为**无法判定独立性**并判红，MUST NOT 计为已校验。

- Q: 协调者到底能不能派发？这是本特性的立案缺陷（092 的 6 包声明并行、实际串行），但原文只对「已声明并发」的执行体设了检查——一个**没写并发**的协调者就可以在运行期被宿主喂 6 个单元而免检。 → A: 加两条：(1) 宿主在运行期把 N>=2 个单元交给同一执行体、而该执行体不满足 FR-021 三条之一时，该次执行 MUST 判为声明与执行不一致，MUST NOT 以「定义里没写并发」免检；(2) 把实测矛盾登记为 F-093-003：`agents/` 下 § Responsibilities 对每个协调者与执行者逐字写着「Never dispatch another agent」，同文件 frontmatter `capability-tools:` 为 `Read, Grep, Glob, Bash, Write, Edit`（无派发工具）——**静态能力字段与正文禁令一致，却与 092 的 6 包声明矛盾**。「协调者是否可派发」的裁定登记为 [[STR-011]]（`coordinator-dispatch-verdict`），其 owner 条目 MUST 在一次运行内给出单一裁定；本规格只要求裁定存在且可读，MUST NOT 预设裁定结果（两条读法都与已记录意图相容：禁止派发 ⇒ 派发责任归驱动者/主代理；允许派发 ⇒ 协调者能力集须增派发工具）。

- Q: 声明层（`shared/declarations/`）的「登记」到底是哪个面？SC-009 要求「把任一条目从 `contract.yaml` 注销时读取方按 `owner-unavailable` 失败」，FR-031 又要求「在 `contract.yaml` 登记后才可读」——但 `contract.yaml` 里并没有逐条目的注册表段。 → A: 以读取入口的**实际行为**为准：实测 `declaration_reader.py --action list` 返回 `contract.yaml` **自身的九个键**加 `facts/` 目录里的 slug，二者共用一张清单；`--action get --fact concurrency-class` 返回 `no declaration for fact 'concurrency-class'`、退出码 1（未登记形态）。故「登记」MUST 有一个可判定的读取面——要么在 `contract.yaml` 为该 slug 落一个键，要么由读取入口把 `facts/` 的 slug 列为已登记；两处都缺席即按 `owner-unavailable`（退出码 2）处理，MUST NOT 取缺省值。**登记前的探测是本规格产出的第一环**，MUST NOT 假定条目文件一落地即可读。

- Q: `goal` 在文件系统上有两层——`.specify/goal/<slug>/` 与 spec-local 的 `.specify/specs/<id>/goal/<slug>/goal.md`，哪一层才是「goal 执行体」？ → A: 按既有 owner 判定、本规格不另立一层：`goal-definitions.md` 声明 goal 持久化在 `.specify/goal/<slug>/`；spec-local 那一层是 085 的 spec-local 临时 team/goal 协议的**投影**（092 同形、本特性的 spec 树亦然）。FR-032 因此显式区分「存档目标」与「临时目标」：target 并发规则相同，后者的存在性/删除/迁移归 085/092 的 owner，本特性 MUST NOT 假定其长期存在，也 MUST NOT 把它当第七个枚举根。

- Q: goal / team / loop 三类的「单元」是同一个东西吗？原 FR-028 写「记录每轮/每单元」，但三类执行体的推进颗粒不同。 → A: 记录面改为**每一个推进单元**：`sdd-loop-driver` 按阶段与 Work Package 推进、`sdd-house-keeping` 按**条目**推进（保留期清理的对象是记录条目，没有「轮」）、`sdd-project-setup` 按**步骤**推进（步骤间存在依赖边）。写成「每轮」会让前两类无处落账，从而用「无轮次」掩盖「未记录」。同理，Edge Cases 里 goal 的「互相独立」改为**复用 FR-005 的 (b)+(c)**，不新造一个「独立性」谓词（否则 goal 一套判据、其他执行体另一套）。

- Q: team 席位领地相交在什么输入上判？ → A: 判输入是席位声明的写领地，因此「未声明」的处置必须写明。实测 12 个 team 定义中有 2 个（`demo-seat-dispatch`、`requirement-implement-monitor`）在树内完全不出现 territory 声明；对它们 MUST 按 FR-012 的「未声明写域即判红」处理，MUST NOT 因「没有领地所以不会相交」而放行。同时 FR-012 的写域 MUST 是**文件级路径集而非目录级区域**（目录级声明会把「同目录下不同文件」误判成相交，也是本仓 declared-vs-delivered 不一致的既有来源）。

- Q: 槽位上限「唯一定义点」与现存三处约束是什么关系？ → A: 本规格只拥有**合成算式** `min(槽位上限, 天花板, 剩余预算)`，不拥有数字。实测四处说法并存：`stage-team-preset.md` 的 `slot_cap_ceiling: "min(6, …)"`、`wp-gate.py --slot-cap-ceiling` 默认 4 且 `WG-16` 校验 `1 <= slot_cap <= ceiling`、`decomposition-model.md` §365 的临时 team 模式 `min(effective_concurrency, 24)` 与其余运行的 `min(4, line remaining)`。FR-014 因此要求 plan **先点名哪一处是 owner、其余为投影**，MUST NOT 靠再添一处达成「唯一」。同类对齐也落进 FR-029：本线状态脊 `project_config` 已带 `decomposition` / `decomposition_stages: [plan, implement, review]` / `decomposition_slot_cap`，[[STR-007]] 条目 MUST 说明它与这三个键的关系（取代 / 投影 / 并列），不得出现第四处「哪些阶段拆解」。

- Q: 本特性是否要改写 064 / 070 / 086 / 092 的册来「落地默认值」？ → A: 不改写。FR-033 要求处置清单从四个 owner 册各自读出（「册 × 条目 × 处置」映射），本规格 MUST NOT 复制其内容；任何要求改动四个册正文的处置 MUST 作为一次带 [[STR-006]] 条目的纪律修订记录，并在同一次提交内更新镜像投影。

- Q: 既有受影响的测试面有多大？ → A: 实测 `templates/commands/` 29 个命令模板中只有 1 个（`sanitize.md`）命中 `concurren|并行`；`skills/` 下 `default-concurrent|serial-reason|effective-concurrency` 零命中（7 个新 STR 字面量在仓库内均无既有占用，实测 grep 为空）。该读数写进 FR-033 的处置面：本特性是在**空白面**上新增义务，不是在既有措辞上改判，因此 SC-010 的「逐条有处置记录」不因历史措辞缺席而可省。

## Assumptions

- **A1（范围以本仓文件系统为准）**: 「所有技能/命令/goal/team/loop」按本仓的枚举结果读取，不在规格里固化数量；任何点数在本规格中写作「动态枚举所得」，MUST NOT 固化为常量。（FR-003、SC-001）
- **A2（串行不是失败，无声串行才是）**: 串行本身是合法形态；本特性的判红对象是「无具名理由的串行」与「声明并发实际串行」。这条边界使实现不必为了绿而强行并发。（FR-006、FR-023）
- **A3（宿主能力不可固化）**: 宿主是否支持并行原生调用是运行期事实，写在记录里而不是固化到文件里；把它写死会让同一份配置在不同宿主上给出错误结论。（RS-005、FR-005）
- **A4（真实取证可能后置）**: SC-006 需要一个真实执行体承载，若本特性自身的 implement 阶段跑不出并发，则该证据由紧随其后的一次真实运行补齐并在 `verification.md` 中标注来源；本特性 MUST NOT 用夹具数据冒充真实读数。（FR-033、SC-006）
- **A5（不新增命令、不新增调度引擎）**: 状态脊 `non_goals` 已声明：不新增 `/speckit.*` 命令、不引入第二个派发引擎或 registry、不做无条件并行、不改变 SDD 阶段链与哨兵。本规格的全部要求都在这条边界内。（FR-002、FR-025、FR-028）
- **A6（并发收益不是本特性的唯一判据）**: 本特性在意的首先是**正确性与可判定性**（默认值、理由码、声明与执行一致），其次才是墙钟收益；SC-012 只作为支撑性判据，且必须与结果集一致同时成立。（SC-012）
