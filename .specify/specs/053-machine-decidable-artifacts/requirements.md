# Requirements Specification: 机器可判定的制品命题(Machine-Decidable Artifact Propositions)

**Requirement Branch**: `053-machine-decidable-artifacts`  
**Created**: 2026-09-23  
**Status**: Draft  
**Input**: User description: "让制品的结构性命题由机器判定,而不是由 LLM 目测。本轮 /speckit.feedback consume 的自省报告把 5 个「需要新能力而非小编辑」的项路由到了本命令,它们是同一个主题的五处缺口:一处制品对自身结构做断言(编号连续、引用可解析、计数正确),或一处制品对兄弟制品做断言(某条款由哪一行任务转绿、某判据的主体是否被覆盖),而这个断言当前只能靠代理阅读后声明,于是错前提会静默进入下游。五项:① requirements.md 没有确定性校验器(FR/SC 编号连续性与文档出现序、每个 FR-/SC-/[[STR-]] 引用可解析、活动标记计数只应数「带冒号且未被反引号包裹」的实例);同型先例已存在:validate-tasks.py 之于 tasks.md。② 「条款由哪个任务转绿」这一归属关系对结构校验器不可见,需要先在 tasks 模板定义行内归属声明面,再给校验器增 WARN 级「绿点跨阶段」检查。③ 机器覆盖核算(contracts 每条条款与每条 FR 恰被一行任务认领,由脚本印出未覆盖集),其前置缺口是 contracts 的条款语法当前没有 owner。④ goal 判据主体的「目录指代形」——当前靠成员枚举,脆弱且不可程序指代。⑤ goal-utils.py 增 run-checks action,一次输出团队 run 前置五项检查的 JSON verdict。跨切面约束:(a) 校验器给出的绿同样受快速失败纪律约束,每个新检查都 MUST 有逆样本;(b) 门控预算余量为零,任何新增措辞须零命中;(c) templates/ 保持项目中立;(d) 新增检查器 MUST 走 Program-First 的既有归属声明形态;(e) validate-tasks.py 在改动前没有任何契约测试钉住其检查项计数与退出码表,新校验器不要重蹈。"

## Related Feature *(mandatory)*

**Feature ID**: 053  
**Feature Name**: 机器可判定的制品命题(Machine-Decidable Artifact Propositions)

**绑定判定**:新建而非绑定(2026-09-24 `/speckit.clarify` 经用户裁定)。决定性先例是 `features/040.md:57-63`——051 依同一形状判为新 Feature,确立「以指令段/脚本形式嵌入是**投递事实,不是归属事实**」(052 沿用同句)。逐个核验的候选与排除理由:041 Goal Registry 只覆盖 US4/US5 两个故事,且 `features/041.md:57` 声明 `shared/definitions/goal-definitions.md` 非其所拥有,而 US5 正是要改该文件;023 / 035 是零同胞的 Draft 且主题不相干;040 / 052 的 owner 文档已被本规格明令处置(FR-014 要求移除 052 期间加入 `clarify-taxonomy.md` 的过渡副本),绑上去与本规格自身义务相反。

## Overview

框架的每一份制品都在对自己或兄弟制品做**结构性命题**:`requirements.md` 声称自己的 FR 编号连续、声称每个交叉引用都能解析、声称活动标记还剩几处;`tasks.md` 声称某条契约条款会由某一行任务转绿;goal 判据声称它约束的主体是某一组东西。今天这些命题**全部由阅读者(代理)在目测之后声明**,而声明一旦写进制品,下游就把它当事实引用。

后果不是"偶尔看错",而是**错前提静默扩散**:一份声称「107/107 条款已覆盖」的 tasks.md 会把一个结构性不可满足的验收条件送进 implement;一份声称「零残留旧计数」的 clarify 回写会在编号已经变了的情况下通过。本仓最贵的一类缺陷正是这个形态——检查跑完给出了绿,但那个绿不是关于它被写来判定的那个命题的(见 `.specify/shared/guidelines/fast-fail.md` § 判据同样覆盖机器给出的绿 与 `docs/reference/history/00-cross-cutting-lessons.md` § 十二)。

本特性把这类命题**从散文搬进程序**:每个命题获得一个确定性判定者(检查器),命题的真假由退出码与机读 verdict 表达,而不是由某一行自陈的数字表达。已有同型先例可循——`scripts/python/validate-tasks.py` 之于 `tasks.md`;本特性沿用它的形态,把它扩展到 `requirements.md`、把「条款→任务」的归属关系变成可解析的声明面、并给 goal 侧两个当前只能靠内部函数或成员枚举表达的命题装上 CLI 入口。

**本特性不做什么**(边界,避免与相邻纪律混淆):

- 不引入任何新的门控停等点。检查器输出的是**判定**,授权语义仍归 `.specify/shared/guidelines/confirmation-gates.md`。
- 不改变 `/speckit.*` 命令的阶段划分或状态机。检查器接进既有步骤,不新增步骤。
- 不做语义正确性判断(某条 FR 写得好不好、某个故事是否真的独立可测)。程序只判**可机械判定的结构命题**;语义判断仍归 `/speckit.analyze` 与 `/speckit.clarify`。
- 不回溯改造既有 spec 的契约文件(见 FR-027 与下方 Clarification 标记)。

### 现状锚点(以源码实测为准,2026-09-23)

| 事实 | 实测值 | 对本特性的意义 |
|---|---|---|
| `scripts/python/validate-tasks.py` 的检查面 | **6** 项,全部基于**任务→任务**图(行形态、ID 唯一、blockedBy 可解析、`[P]` 并行安全、story 标签位置、**DoD 格式**) | 条款→任务归属**结构性不可见**,这是 US2 的缺口本体 |
| 该脚本**现有**的契约钉子 | **2 处**,均在 `tests/contract/test_validate_tasks_parallel_safety.py`:标签集钉 `EXPECTED_CHECKS`(:75-82,由 :314 的 `labels == EXPECTED_CHECKS` 断言到脚本实际发出的标签集)+ 退出码表钉 `test_c5_exit_code_table`(:346) | 二者落在提交 `46760e37`,而该提交是本 spec 提交 `7c5598c0` 的**祖先**⇒ FR-046 对既有脚本的义务是「新增检查项时同步扩充既有钉子」,不是「从零补钉」 |
| 契约文件总数 | `.specify/specs/*/contracts/` 下的全部文件;**该总数是一个会变动的量**(本特性自己的 7 份契约落盘即改变它),故其当前值与 as-of 由 `notes/clause-form-census.md` 唯一拥有,本行不复写字面量 | 覆盖核算的分母;也说明条款语法不统一。**因此 SC-006 的分母哨兵 MUST 是关系式**(可解析数 + 点名数 == 本次实扫总数),MUST NOT 是一个写死的整数 |
| 条款语法的实测分布 | **至少 6 种机器可辨形态**(闭合粗体 / 括注后闭合的粗体 / `## C-N` 标题形 / OpenAPI `.yaml` / 结构化 `assertions[].id` `.yaml` / 皆无);逐形态的文件数与条款 id 数由 `notes/clause-form-census.md` **唯一拥有**,本行不复写——该量随本特性自己的契约落盘与每次编辑而变;唯一可安全引用的字面量是**改前基线**(110 文件 / 508 id),落盘后的值 MUST 现场跑该文件内的命令 | 条款语法**无 owner**;**残余数是 owner 所声明覆盖面的函数,不是一个定值**。故 US3 必须先解决归属再谈核算(FR-022…FR-026),且一切总量哨兵 MUST 取关系式(见 SC-006) |
| `goal-utils.py` 现有 action | `create` / `validate` / `check-statement` / `list` / `status` / `objective` / `criteria` / `migrate` / `targets` | `run-checks` **未被占用**;`preview_target_check` 与 `resolve_effective_target` 无 CLI 入口(US4 缺口本体) |
| 门控扫描器预算 | total **23**,cap = 93 × 0.25 = **23.25**,整数余量 **0**,由**三处不同形态**的断言钉住 | 任何新增措辞须零命中(FR-045) |
| 标识符冲突检查 | `validate-requirements` / `run-checks` / `[green:` / `clause-ref` / `validate_requirements` 在非 spec、非 memory 的跟踪文件里**零命中** | 本特性引入的新标识符均无碰撞 |
| `shared/constants/clarify-taxonomy.md` 的文档序不变量 | 本轮(2026-09-23)刚加入,含一段**过渡期** awk 抽取式与一句「Until that validator ships」的接线声明 | US1 MUST 接管它并**移除该过渡副本**(FR-014)——这是本特性对既有制品的一笔明确债务 |
| `shared/guidelines/requirements-guidelines.md` § Validation Process | 只有勾选项清单,**无检查器**;计数与引用解析留给目测 | US1 的落点 |

### Assumptions

- **A-1 制品形态稳定**:被校验制品是 Markdown 文本,其结构由 `.specify/templates/` 下的模板定义。检查器判的是「制品是否符合其模板声明的结构」,不是「制品写得好不好」。
- **A-2 单一消费通道**:检查器只经**两条**通道被触发——由 `/speckit.*` 命令在自己的既有步骤里调用,或由契约测试直接调用(与 FR-048 的封闭集同一枚举);不提供守护进程、不做文件监听、不接入 CI 或任何其它自动触发面。实测本仓当前无任何 CI 配置(`.github/workflows/` 不存在),故 CI 不是一个可用通道,MUST NOT 在措辞上被暗示为许可。
- **A-3 零写入**:所有检查器 MUST 是只读的。判定结果只经 stdout / 退出码表达,MUST NOT 修改被校验制品(与 `validate-tasks.py` 现状一致)。
- **A-4 增量生效**:新检查器对**本特性之后**产出的制品强制;对既有制品的适用性见 FR-027 与下方标记。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - `requirements.md` 的结构性命题由检查器判定,而不是由作者自陈 (Priority: P1)

写规格的人(或代理)在 `requirements.md` 里印出「38 条 FR、12 条 SC、零残留活动标记」这类数字时,今天没有任何程序核对过它们。本故事给 `requirements.md` 装一个与 `validate-tasks.py` 同形的确定性检查器:编号连续且按**文档出现序**、每个 `FR-\d+` / `SC-\d+` / `[[STR-\d+]]` 引用都能解析到本文件内的一处定义、活动标记的计数只数**带冒号且未被反引号包裹**的实例。命令在写完规格后跑它,按退出码决定是否继续。

**Why this priority**: 这是五项里唯一**已有同型先例、已有明确落点、且被另一处制品显式等待**的一项——`shared/constants/clarify-taxonomy.md` 本轮刚写入的文档序不变量明写「Until that validator ships」,并临时携带一段 awk 抽取式作为过渡副本。不落地 US1,那段过渡副本就长期留在 owner 文档里成为第二份真相。同时 `requirements.md` 是整条链的最上游,它的错前提传播距离最远。

**Independent Test**: 对一份真实的 `requirements.md`(例如 `.specify/specs/052-fast-fail-principle/requirements.md`)只读地跑一次检查器,确认 exit 0;再对四份人为破坏的副本(编号跳号、FR 换序、引用指向不存在的 STR、把一个活动标记反引号包裹后期望计数不变)各跑一次,确认每份都被点名且 exit 非 0。四份破坏样本各自只触发预期的那一项检查,即证明检查项之间不互相遮蔽。

**Acceptance Scenarios**:

1. **Given** 一份 FR 编号连续、引用全部可解析、活动标记为零的 `requirements.md`,**When** 跑检查器,**Then** exit 0,人读输出逐项列出已执行的检查与 `0 error(s)`,机读输出的 error 计数为 0。
2. **Given** 一份把 `FR-007` 插到 `FR-012` 之后的规格(ID **集合**仍连续),**When** 跑检查器,**Then** 报出文档序违例并按 [[STR-002]] 的形态点名是哪一条排在哪一条之后,exit 非 0。
3. **Given** 一份规格,其正文含一个**被反引号包裹**的 STR 引用形态(属提及)与一个**裸写**的 STR 引用形态(属真实引用),且二者指向的编号都超出 Shared Strings 表的定义范围,**When** 跑检查器,**Then** 只对裸写的那一个报出引用不可解析并给出其行号,对被反引号包裹的那一个不报,exit 非 0。
4. **Given** 一份讨论澄清机制、因而正文里大量出现被反引号包裹的标记名的规格,**When** 跑检查器,**Then** 活动标记计数**只**统计带冒号且未被反引号包裹的实例;被反引号包裹的标记名一律不计入。
5. **Given** 检查器已在命令流程里接好,**When** 它报出任一 ERROR,**Then** 命令 MUST NOT 继续进入下一阶段,并 MUST 把检查器的输出原样呈现(而不是复述或概括)。
6. **Given** US1 已落地,**When** 复核 `shared/constants/clarify-taxonomy.md`,**Then** 那段过渡期 awk 抽取式已被移除,该处的文档序不变量改为指向检查器,且「Until that validator ships」一句已删除。

---

### User Story 2 - 「哪条条款由哪一行任务转绿」成为可声明、可解析、可校验的面 (Priority: P1)

今天 `tasks.md` 的每一行只声明它写哪些文件;一条契约条款会不会被转绿、由哪一行负责,只存在于契约散文里。于是当 MVP 截断到前两个故事时,**没有任何东西**能发现「第三个故事的验收条件依赖一个排在它之后的阶段」这种结构性不可满足。本故事在 tasks 模板定义一个行内归属声明面,并给 `validate-tasks.py` 增一项 WARN 级检查:归属任务集中任一任务所处阶段晚于本行,即报「绿点跨阶段」。

**Why this priority**: 与 US1 同为 P1,因为它俩合起来才闭合「制品对自身结构的命题」这一类:US1 管一份制品内部的自洽,US2 管两份制品之间的归属。而且 US3 的覆盖核算**依赖**本故事的声明面——没有可解析的归属,核算无从谈起。先例证据:本轮消化的一条 implement 反馈正是「条款由哪个任务转绿对结构检查器不可见」,已由自省报告 F-05 定级为需新能力。

**Independent Test**: 构造两份最小 tasks.md + 一份最小契约:甲的两行任务分别认领条款 C-1、C-2 且阶段序与认领序一致;乙把认领 C-2 的行放在认领 C-1 的行**之前**的阶段。对甲跑检查器应 exit 0 且零 WARN;对乙应报出跨阶段绿点 WARN 并点名涉及的行与阶段。再对丙(归属标记指向一份不存在的契约文件)跑,应报不可解析——三向合起来证明该检查既能发现真问题,又不误报正常排布。

**Acceptance Scenarios**:

1. **Given** 一行任务按 [[STR-001]] 的形态声明它认领某契约的某条款,**When** 跑检查器,**Then** 该声明被解析为 `(契约文件, 条款 id, 任务 id, 所处阶段)` 四元组。
2. **Given** 某条款的归属任务集中存在一个所处阶段**晚于**声明行的任务,**When** 跑检查器,**Then** 报 WARN 级「绿点跨阶段」,点名条款、涉及的行与阶段序,且 exit 码仍为 **0**——`validate-tasks.py` 的既有退出码表只有「无 ERROR → 0」「有 ERROR → 1」两档,警告不单独成档(该事实被 `tests/contract/test_validate_tasks_parallel_safety.py:353,356` 钉住)。
3. **Given** 一条归属声明指向不存在的契约文件或不存在的条款 id,**When** 跑检查器,**Then** 报 ERROR(不可解析),exit 码 **1**,而不是 WARN 的 exit 0——悬空归属比跨阶段归属更严重,二者在退出码上即 1 vs 0 之别。
4. **Given** 一行任务声明了归属但**未**声明文件路径,**When** 跑检查器,**Then** 既有的行形态检查 MUST NOT 因此误报;归属声明与路径声明是两个正交的面。
5. **Given** 两份任务行认领**同一条款的同一区间**,**When** 跑检查器,**Then** 报 WARN 并点名两行——这与 `.specify/memory/glossary.md` 已登记的「条款分区 (Clause Partition)」是同一失效模式的两面:该术语讲的是「同一契约测试文件被多阶段核验行认领」,本检查把它机械化。
6. **Given** 两个核验行指向**同一份测试文件路径**、而各自的归属声明指向**不同的绿点**,**When** 跑检查器,**Then** 报 WARN 并点名两行与该路径;再对一份「同一路径、两行绿点相同」的副本跑,**Then** 零 WARN——正反两向都实测,证明该检查认的是**绿点分歧**而不是**路径共用**。本场景与场景 5 MUST 分列:场景 5 的判据是条款区间重叠,本场景的判据是测试路径共用且绿点不同,两者可以在同一份 tasks.md 上各自独立触发。

---

### User Story 3 - 覆盖核算:每条条款恰被一行认领、每条 FR 至少被一条条款引用,未覆盖集由脚本印出 (Priority: P2)

`tasks.md` 今天可以自陈「107/107 条款已覆盖」而无人核对。本故事让覆盖成为一个**印出来的集合差**而不是一个声明的数字:脚本读契约与 tasks,把「每条条款、每条 FR」的全集减去**各自来源的**被认领子集(条款侧 = 某一行任务的 `[green:]`;FR 侧 = 某条条款的引用组,FR-026),印出未覆盖集;为空才算覆盖完整。前置条件是给契约的条款语法指定 owner——实测 110 份契约里只有 21 份用 `**C-N**` 形态,其余各异,没有 owner 就没有全集。

**Why this priority**: P2 而非 P1,因为它依赖 US2 的声明面,且必须先解决条款语法的归属问题;而归属问题触及全仓每一份既有契约文件(总数由 `notes/clause-form-census.md` 拥有),是本特性里唯一可能引发大范围返工的一项。它的价值最高(直接消灭「自陈覆盖率」这一类**盲检**,见 `.specify/memory/glossary.md` 已登记的「盲检 (Blind Check)」),但落地顺序必须在 US1/US2 之后。

**Independent Test**: 在一个临时目录里搭一份最小 spec(一份 3 条款的契约 + 一份 tasks.md,其中 2 条被认领、1 条未被认领),跑核算脚本,确认它印出的未覆盖集恰为那 1 条、exit 非 0;再把第 3 条补上认领,确认未覆盖集为空、exit 0。两次运行的差集必须**按名字**比对,而不是按计数——计数相等会掩盖成员变化。

**Acceptance Scenarios**:

1. **Given** 条款语法已有 owner 文档,**When** 核算脚本读一份契约,**Then** 它按 owner 定义的形态抽出条款全集,并对无法按该形态解析的文件**逐个点名**而不是静默跳过。
2. **Given** 一份 tasks.md 漏认领了某条款,**When** 跑核算,**Then** 未覆盖集按 [[STR-009]] 的前缀形态印出该条款,exit 非 0。
3. **Given** 覆盖完整,**When** 跑核算,**Then** 未覆盖集为空,且脚本 MUST 同时印出一个**必须非空**的伴生量(已认领条款数、被扫描契约文件数),使「空因为对」与「空因为盲」可区分。
4. **Given** 某条款被**两行**任务认领,**When** 跑核算,**Then** 报出重复认领并点名两行——「恰被一行认领」中的「恰」是双向的:漏认领与重复认领都是违例。
5. **Given** 一份 FR 未被任何条款的引用组认领,**When** 跑核算,**Then** 它出现在未覆盖集里,与条款未覆盖分列(两者的全集来源不同,不可混为一个计数)。

---

### User Story 4 - 团队 run 前置的五项检查一次调用即出机读 verdict (Priority: P2)

`/speckit.team` 的 run 前置要做五项检查(goal 绑定、悬空、target 终态、跨 goal、goal 终态),但它们依赖 `goal-utils.py` 里两个**没有 CLI 入口**的内部函数,于是每一轮 run 都要由代理自己拼装调用顺序、自己解读结果。本故事增一个 `run-checks` action,一次输出五项检查的机读 verdict。

**Why this priority**: P2。它不涉及制品间的命题,但它是「一个判定必须可一次调用取得」这一原则的实例:当五项检查要由调用方拼装时,拼装顺序错了不会报错,只会给出一个看似合理的绿。它自包含、风险低、收益明确,适合作为本特性的第二个 P2。

**Independent Test**: 对一个真实的团队 slug 跑 `run-checks --json`,确认输出含五个 check 条目、每条带 id 与 name、顶层 verdict 与 blocked 字段齐备、退出码符合 [[STR-007]];再对一个 goal 已终态的团队跑,确认对应 check 的 verdict 为既有词表里的值、顶层 blocked 为真、退出码为阻塞档;最后对不存在的 slug 跑,确认退出码为输入错误档且**零写入**(前后 `.specify/goal/` 与 `.specify/teams/` 的字节校验和不变)。

**Acceptance Scenarios**:

1. **Given** 一个合法团队 slug,**When** 跑 `run-checks`,**Then** 五项检查全部被评估,每条带 [[STR-004]] 之外的真实 verdict,顶层 verdict 与 blocked 由五条派生。
2. **Given** 某项检查因前置条件不成立而被短路,**When** 跑 `run-checks`,**Then** 该条的 verdict MUST 是 [[STR-004]],MUST NOT 是 `ok`——一个未被评估的检查报绿,正是本特性要消灭的形态。
3. **Given** 未传 `--target`,**When** 跑 `run-checks`,**Then** 输出的 resolution 字段说明有效 target 是怎么解析出来的(来源与声明的 focus),使调用方不必自己重推。
4. **Given** 团队定义文件不可解析或仓库根无法确定,**When** 跑 `run-checks`,**Then** 退出码为 [[STR-007]] 里对应的那一档,且与「检查判为阻塞」的档位可区分。
5. **Given** 任何一次调用,**When** 它返回,**Then** `.specify/goal/` 与 `.specify/teams/` 下的文件字节未变(零写入是硬约束,不是惯例)。

---

### User Story 5 - goal 判据的主体可由程序指代,不再靠成员枚举 (Priority: P3)

`shared/definitions/goal-definitions.md` 里一条判据若要说「这七个绘图技能都要满足 X」,今天只能把七个名字逐个列出。名字一变、一增、一删,判据就静默失实,而且没有任何程序能核对「判据声称的主体集合」与「实际存在的集合」是否一致。本故事给判据主体引入一个**可由程序解析的指代形**,使主体集合能被机械导出而非人工维护。

**Why this priority**: P3。它是五项里唯一不产生新检查器的一项(它改变的是**数据的表达形态**),价值要让位于 US1–US4;但它是 US3 那类「全集减去子集」核算能推广到 goal 侧的前提,故仍在本特性范围内而不是另立。

**Independent Test**: 写两条判据:甲用指代形声明主体为一个目录,乙用成员枚举声明同样七个名字。对二者各跑一次解析,确认甲导出的主体集合与目录实际内容一致;然后在目录里增删一个成员,确认甲的导出集随之变化而乙的不变——这一对差异就是本故事的全部价值,必须能在输出里直接看见。

**Acceptance Scenarios**:

1. **Given** 一条判据以指代形声明主体,**When** 引擎解析它,**Then** 主体集合由指代形**在解析那一刻**导出,而不是取自判据文本里的枚举。
2. **Given** 指代形指向一个不存在的路径,**When** 引擎解析,**Then** 报可区分的错误(不是空集合)——空集合会让「零个主体全部满足」空真。
3. **Given** 一条判据同时使用指代形与成员枚举,**When** 引擎解析,**Then** MUST 报冲突而不是静默择一。
4. **Given** 既有的纯枚举判据,**When** 引擎解析,**Then** 行为与本特性之前完全一致(向后兼容是硬约束:既有 goal 不因本特性失效)。

---

### Edge Cases

- **制品为空或只有模板骨架**:检查器 MUST 报「无可校验内容」而不是 exit 0。一个只有占位符的 `requirements.md` 通过校验,等于给下游发了假通行证。
- **编号带字母后缀或补零不一致**(`FR-7` vs `FR-007`):MUST 判为形态违例并点名两种写法,而不是自行归一化后放行——归一化会掩盖作者的编号意图。
- **同一 ID 被定义两次**:MUST 报重复定义(ERROR),且与「引用不可解析」分列,因为二者的修法相反(一个要删,一个要补)。
- **归属声明出现在被围栏代码块包裹的示例里**:MUST NOT 被当作真实声明解析。先例:本轮消化的一条反馈正是「指针落进了围栏示例块内」,靠一次围栏感知扫描才发现。
- **契约文件是 `.yaml` 而非 `.md`**(实测该形态存在且分属**两种**语法:OpenAPI 与结构化断言;逐形态计数由 `notes/clause-form-census.md` 拥有):条款全集的抽取 MUST 覆盖这两种形态,或对无法覆盖的形态**逐个点名跳过**并计入一个非零的伴生量,MUST NOT 静默忽略。
- **`run-checks` 的五项检查里有一项自身抛异常**:MUST 把该条记为 [[STR-004]] 并继续评估其余四项,MUST NOT 让一项异常吞掉整份 verdict。
- **指代形导出空集合**(目录存在但为空):MUST 报「主体集合为空」而不是让判据空真通过。
- **检查器从镜像副本被调用**:本仓同时是框架源与自己的客户运行时,故任何「向上找最近的含 `.specify/` 的祖先」式自定位在本仓**自匹配**,会把每次调用都解析到框架仓而非调用方工作区(该缺陷形态见 `AGENTS.md` § Two Hats 的 Path-resolution trap)。新增检查器 MUST 只在自身已解析路径含字面 `.specify` 组件时才允许自定位,且 MUST 为该规则的**否定情形**配一条断言;失效表现是工作区状态被写进框架仓,而不是一个失败的测试。
- **契约文件可被解析但抽出零条款**:MUST 报「该文件贡献 0 条款」并计入一个非零伴生量,MUST NOT 静默把它算作已覆盖。这正是 FR-025 要区分的「空因为盲」在**单文件**粒度上的形态——一份分母悄悄少了 1 的核算,其未覆盖集为空同样是假绿。
- **门控预算**:本特性新增的任何措辞若使扫描器 total 从 23 变为 24,即为违例——整数余量为 0,没有「加一条再调 cap」的余地。

## Requirements *(mandatory)*

### Functional Requirements

#### 检查器形态与 Program-First 归属

- **FR-001**: 每个新增的确定性检查器 MUST 是单一入口的可执行脚本,以被校验制品的路径为参数,以退出码表达判定;MUST NOT 要求调用方先读入制品内容再自行判断。
- **FR-002**: 每个**新增**检查器的模块 docstring MUST 按 [[STR-008]] 的形态声明其 Program-First 归属(点名规则 owner 文档),并逐项列出它执行的检查及各自判据,与 `scripts/python/validate-tasks.py` 的既有体例同形。
- **FR-003**: 每个**新增**检查器 MUST 同时提供人读输出与 `--json` 机读输出,且二者判定一致;机读输出 MUST 含被校验制品路径、**逐项检查的 verdict**、error 计数与 warning 计数,人读输出的计数尾行形态为 [[STR-003]]。实测:先例 `validate-tasks.py --json` 只发 `file` / `errors` / `warnings` / `status` 四键,**无逐项 verdict 数组**,故本条要求的形态是**新造**而非沿用;其实测风险较低——全仓无任何调用方传 `--json`(`templates/commands/tasks.md` 只以人读形态调用)。**量化词辖域(本条与 FR-002 共用一个固定读法,用以消除 FR-001…FR-005 之间的不一致)**:**形态类**要求(FR-002 的 docstring 体例、本条的机读输出键集)只辖本特性**新增**的检查器,既有的 `validate-tasks.py` MUST NOT 因本特性被要求迁移其 JSON 形态——它只受 FR-046 的钉子扩充义务与 FR-017/FR-018 的新增检查项约束;而**安全类**要求(FR-005 的只读性)**普遍适用于全部**检查器含既有的。这一不对称是刻意的:只读性是安全不变量,不是形态约定。
- **FR-004**: 检查器 MUST 对「被校验文件不存在」「被校验文件不可解析」「被校验文件为空或仅含模板骨架」三种情形给出**互相可区分**的退出码或 verdict,MUST NOT 混为同一失败形态。
- **FR-005**: 所有检查器 MUST 是只读的:判定只经 stdout 与退出码表达,MUST NOT 修改被校验制品或任何仓内文件。

#### requirements 侧的可判定命题(US1)

- **FR-006**: 系统 MUST 提供一个校验 `requirements.md` 的确定性检查器,其检查面至少覆盖:FR/SC 编号连续、编号按**文档出现序**、交叉引用可解析、活动标记计数。
- **FR-007**: 编号连续性检查 MUST 按前缀分序列独立进行(`FR-` 与 `SC-` 各自成序),MUST NOT 跨前缀比较序号。
- **FR-008**: 文档序检查 MUST 锚定在**定义行**上,而不是在 ID 的每次出现上;其违例输出形态为 [[STR-002]];`## Clarifications` 一节 MUST 被排除。依据:本轮实测,按「每次出现」比对会在一份干净的既有规格上报出 5 条假违例,而按定义行锚定并排除该节后为 0——两个锚点都是承重的,不是装饰。
- **FR-009**: 引用可解析检查 MUST 覆盖 `FR-\d+`、`SC-\d+` 与 `[[STR-\d+]]` 三种形态,每条不可解析的引用 MUST 报出引用出现的行号与被引用的 ID。**被反引号包裹的引用形态属「提及」而非「引用」,MUST NOT 计入**;该区分与 FR-010 对活动标记的区分同构且同样承重——一份讨论引用机制的规格必然大量提及引用形态本身。本规格的撰写过程实测到该失效:为描述「不可解析引用」而裸写的示例本身成了一个不可解析引用。
- **FR-010**: 活动标记计数 MUST 只统计**带冒号且未被反引号包裹**的实例。依据:一份讨论澄清机制的规格必然大量出现被反引号包裹的标记名,字面匹配对它 grep-敌对——本轮实测该形态在既有规格上会给出虚高计数。
- **FR-011**: 检查器 MUST 对同一 ID 被定义两次报 ERROR,且与「引用不可解析」分列(二者修法相反:一个要删,一个要补)。
- **FR-012**: `/speckit.requirements` MUST 在写完规格后调用该检查器,并在其报出任一 ERROR 时**停止**,MUST NOT 进入下一阶段;停止时 MUST 原样呈现检查器输出,不得复述或概括。
- **FR-013**: `shared/guidelines/requirements-guidelines.md` § Validation Process MUST 写明「计数与引用解析由该检查器派生,MUST NOT 手打」,并 MUST 把清单更新的时机明确置于澄清回写**之后**。
- **FR-014**: US1 落地后,`shared/constants/clarify-taxonomy.md` 里本轮加入的过渡期 awk 抽取式 MUST 被移除,该处的文档序不变量改为指向检查器,且「Until that validator ships」一句 MUST 删除。依据:该文件是 owner,留一份过渡副本就是留第二份真相。

#### 绿点归属声明面(US2)

- **FR-015**: tasks 模板 MUST 定义一个行内归属声明面,其字面形态为 [[STR-001]];一行任务 MAY 声明零到多条归属。
- **FR-016**: `validate-tasks.py` MUST 把 [[STR-001]] 形态的声明解析为 `(契约文件, 条款 id, 任务 id, 所处阶段)` 四元组,并对指向不存在契约文件或不存在条款 id 的声明报 **ERROR**(悬空归属比跨阶段归属更严重)。
- **FR-017**: `validate-tasks.py` MUST 增一项 **WARN** 级检查:某条款的归属任务集中存在所处阶段晚于声明行的任务时,报「绿点跨阶段」并点名条款、涉及行与阶段序。
- **FR-018**: 归属声明的冲突检查 MUST 覆盖**两个**命题;二者相关但不是同一个检查,故 MUST **分列**报出,MUST NOT 合并为一条计数:(a) 两行任务认领**同一条款的同一区间**时报 WARN 并点名两行;(b) 同一**测试路径**出现在两个核验行、且两行的绿点不同时报 WARN 并点名两行与该路径。(b) 是把 `templates/commands/tasks.md:197` 已声明却仍靠散文执行的自检机械化——该处原文为「Add a self-check that flags any test path appearing in two verification rows with different green points」,而 `.specify/memory/glossary.md` 已登记的「条款分区 (Clause Partition)」条目本身即写明「生成期 MUST 机械核算分区的并集覆盖全部条款且无幻影记号」。本检查与该术语是同一失效模式的两面,MUST 在实现处引用该术语而不是另造名词。
- **FR-019**: 归属声明 MUST 与既有的行形态检查正交:一行只声明归属而不声明文件路径时,既有检查 MUST NOT 误报。
- **FR-020**: 出现在**围栏代码块内**的 [[STR-001]] 形态 MUST NOT 被当作真实归属声明解析。
- **FR-021**: 归属声明面 MUST 项目中立:MUST NOT 含本仓专有名词,其形态说明 MUST 落在 tasks 模板而非某个 spec 的散文里。

#### 覆盖核算与条款语法的 owner(US3)

- **FR-022**: 系统 MUST 为契约的**条款语法**指定唯一 owner:要么指定一份既有文档为 owner 并声明其覆盖的形态,要么定义一个**最小可解析子集**并新建 owner 文档。owner MUST 同时声明**一条条款的正文边界**(一个条款块从其标记行起,到下一个条款标记**或下一个章节标题**为止——以先到者为准;围栏块与行内代码跨度内的文本不算正文):不声明边界,则「条款引用了哪条 FR」取决于抽取器按行还是按块读,同一份语料会得出两个都能自圆其说的总数(2026-10-03 实测:本特性自己的 182 条里恰有 2 条的 `(FR-nnn)` 落在标记行之后的行上,按行读会静默丢失)。实测依据(2026-10-02 `/speckit.plan` Phase 0 重新分类):契约文件里至少存在 **6** 种机器可辨形态,逐形态计数由 `notes/clause-form-census.md` 唯一拥有(本条不复写,因为该量随本特性自己的契约落盘而变);当前无任何 owner(全仓 `templates/` 下无 contracts-template,`shared/definitions/` 下无定义文档)。**落点约束(实测)**:`scan-confirmation-gates.py:35` 的 `SCAN_DIRS = ("templates/commands", "skills", "shared")` 已含 `shared`,故新建在 `shared/definitions/` 下的 owner 文档从**第一稿起**就落在 FR-045 的预算内(total 23、整数余量 0);其措辞 MUST 零命中 `BLOCKING_PATTERNS`,MUST NOT 靠事后调整 cap 或放宽被扫描集来解决。
- **FR-023**: 核算脚本 MUST 按 owner 定义的形态抽出条款全集;对无法按该形态解析的文件 MUST **逐个点名**,并把点名数计入一个非零伴生量,MUST NOT 静默跳过。实测代价:被点名的文件数随 owner 声明的覆盖面而变(两个端值的当前实测见 `notes/clause-form-census.md`),且两种取值都远超可逐行铺满的量,故「点名清单」MUST 可被折叠为计数 + 可选展开,MUST NOT 强制逐行铺满每次输出。
- **FR-024**: 核算 MUST 以**集合差**表达结果:全集减去被认领子集,印出未覆盖集,前缀形态为 [[STR-009]];未覆盖集为空时 exit 0,否则 exit 非 0。
- **FR-025**: 未覆盖集为空时,脚本 MUST 同时印出至少一个**必须非空**的伴生量(已认领条款数、被扫描契约文件数),使「空因为对」与「空因为盲」可区分。
- **FR-026**: 条款未覆盖与 FR 未覆盖 MUST 分列,二者的全集来源不同,MUST NOT 合并为一个计数。**两个子集各自的来源**(2026-10-03 定,来源 `/speckit.analyze` F-05/F-19 的裁定):条款全集 = 契约文件按 FR-022 边界切出的条款块,其**被认领子集** = `tasks.md` 行上的 `[green:]` 归属声明;FR 全集 = `requirements.md` 的 FR 定义行(代码跨度之外),其**被认领子集** = **条款引用组**(C-2 三条规则:块边界 = 标记或标题先到;引用组 = 块内最后一个含 FR/SC id 的括号,容忍一层嵌套、`FR-a…FR-b` 区间展开;组外同形字样按「提及」处理,FR-009)里的 `(FR-nnn)`。FR MUST NOT 作为 `[green:]` 的认领目标——该声明面的目标只有契约文件与条款 id(FR-015、FR-016),所以 FR 侧的覆盖判定与任务行无关,只随契约条款的引用而变。两侧的抽取 MUST 共用同一个抽取器(FR-022 的 owner 定义形态、FR-023 按形态解析),MUST NOT 各写一套解析。本条是「哪个计算点拥有哪一半事实」的唯一声明:核算脚本据此判定 verdict,`feature-ref.md` 的映射表是该脚本同一规则的**发布视图**,不是第二个独立结论。
- **FR-027**: 覆盖核算 MUST NOT 要求改造既有 spec 的契约文件。对既有 **44** 个 spec 目录(其中 **43** 个含 `contracts/`;两个数同基——44 与 43 都**含**本特性自己的目录,初版曾把含 053 的 44 与不含 053 的 42 混在一句里)的适用性取**冻结名字级基线**判据:开工时把当时的未覆盖项**名字集**冻结成一份基线文件(落在本特性目录),此后只对相对该基线**新增**的未覆盖项阻断;基线内的既有项不阻断,但每轮 MUST 仍印出其计数,使欠账可见而非消失。比对 MUST 按名字集合(`comm -13` 形态)、MUST NOT 按计数——与本 spec SC-010 / SC-012 已采用的判据同形,故不产生永久豁免清单,也不留下「同一检查器对两类 spec 给不同判定」的双标准。**基线面**(2026-10-03 增,来源 `/speckit.analyze`):被冻结成基线的那份未覆盖项名字集 MUST 在**排除本特性自己的 spec 目录**的语料上采集(即普查 owner 的 excl-`<ID>` 稳定基;其两端值由 `notes/clause-form-census.md` 拥有,本条不复写),使本特性自己的条款与 FR 恒在基线**之外**——只能被认领,不能被豁免。理由:认领落地晚于基线冻结(本 spec 的 tasks 阶段即如此排),若冻结面含本特性自身项,则自身项先进了基线、后又被认领,`comm -13` 对**任何**认领结果都报空——那是一个永不变红的检查。**配套的正向完备量**:同一核算 MUST 另印一个 MUST **非空**的「本特性已认领条款数」(与 FR-025 同形),否则「基线外集合为空」与「认领从未发生」两种状态不可区分。**基线缺失 MUST NOT 报绿**(2026-10-03 增,来源 `/speckit.analyze` F-18):基线文件不存在时核算 MUST 以非零码退出并点名缺失路径——「无基线」MUST NOT 被读成「无豁免项」而使差集平凡为空。该条同时封掉一个循环定义:若把冻结触发写成「首次全树**变绿**时」,则 green 依赖基线、基线依赖先跑,二者互相为前置,任何一轮都成立不了。
- **FR-028**: `.yaml` 形态的契约(实测 **10** 份)MUST 被覆盖核算显式处置:MUST NOT 静默忽略。实测这 10 份分属**两种**语法而非一种——**9** 份 OpenAPI(条款全集 = 其 **39** 个 path-operation,即 `paths:` 下的 HTTP 方法键;文件内无字面 `operations:` 键,MUST NOT 以该键名作为探测条件)与 **1** 份结构化断言(条款全集 = 其 `assertions[].id`,**6** 条)。故可选处置为:(a) 两种语法各写一个抽取器,(b) 逐个点名跳过并计入 FR-023 的伴生量。

#### run-checks 的调用契约(US4)

- **FR-029**: `goal-utils.py` MUST 增一个名为 [[STR-005]] 的 action,一次调用输出团队 run 前置五项检查的 verdict;五项为 goal-binding / dangling / target-terminal / cross-goal / goal-terminal。
- **FR-030**: 该 action MUST 复用既有的内部解析函数而**不重写第二套文法**;无 `--target` 时 MUST 先解析有效 target 再执行五项检查,并把解析结果(有效值、来源、声明的 focus)写进输出。
- **FR-031**: 机读输出的每条 check MUST 含 `id`(1..5)、`name`(上述五个名字之一)、`verdict`、`message`;顶层 MUST 含 `team_slug`、`goal_slug`、`identity_kind`、`resolution`、`checks`、`verdict`、`blocked`。
- **FR-032**: 单项检查的 verdict MUST 沿用既有词表 [[STR-006]];因前置条件不成立而被短路的检查 MUST 记为 [[STR-004]],MUST NOT 记为 `ok`。
- **FR-033**: 退出码 MUST 按 [[STR-007]] 分档,且「检查判为阻塞」与「输入不合法」与「定义不可解析」三档互相可区分。`run-checks` 落在既有二进制内,故 MUST 复用该二进制已定义的 `EXIT_*` 常量原义,MUST NOT 让同一个码在同一脚本里按 action 而有两种含义;`blocked` 因此取 **5**(实测空闲)。既有调用方 `templates/commands/team.md:96,98` 按 0/2 分支,不受影响。
- **FR-034**: 该 action MUST 零写入:任何一次调用都 MUST NOT 修改 `.specify/goal/` 或 `.specify/teams/` 下的任何文件。

#### goal 判据主体的指代形(US5)

- **FR-035**: `shared/definitions/goal-definitions.md` MUST 定义一个可由程序解析的**判据主体指代形**,使主体集合在解析那一刻被导出,而不是取自判据文本里的成员枚举。
- **FR-036**: 指代形指向不存在的路径时 MUST 报可区分的错误,MUST NOT 退化为空集合;导出集合为空(路径存在但无成员)时同样 MUST 报错,前缀为 [[STR-010]]——空集合会让「零个主体全部满足」空真。
- **FR-037**: 一条判据同时使用指代形与成员枚举时 MUST 报冲突,MUST NOT 静默择一。
- **FR-038**: 既有的纯枚举判据 MUST 保持完全一致的解析行为;本特性 MUST NOT 使任何既有 goal 失效或需要迁移才能继续解析。

#### 机器给出的绿:证据纪律

- **FR-039**: 本特性新增的**每一项**检查 MUST 有逆样本取证:证明被守物真的坏掉时该检查会变红。只展示正常路径的取证不被接受——这是 `.specify/shared/guidelines/fast-fail.md` § 判据同样覆盖机器给出的绿 的直接适用,不是本特性的额外要求。
- **FR-040**: 凡断言「某集合为空」的检查(未覆盖集、不可解析集、冲突集),MUST 在同处配一条**反空真哨兵**:断言一个必须非空的伴生量,使「空因为对」与「空因为盲」可区分。
- **FR-041**: 凡守卫**负面命题**的检查(某物不存在 / 未变化 / 未泄漏),其取证 MUST 含一次变异演练:弄坏被守物 → 确认变红 → 精确反向替换复原 → 确认恢复绿,并复核复原后该文件的差异回到预期形态。演练用的临时产物 MUST 删净并复核计数归零。
- **FR-042**: 检查项集合的钉子 MUST 以**标签集**表达,而不是以计数表达;退出码表 MUST 单独被钉。依据:仓内既有的唯一先例 `EXPECTED_CHECKS`(`tests/contract/test_validate_tasks_parallel_safety.py:75-82`)正是标签集形态并被断言等于脚本实际发出的标签集,而计数形态的钉子会在新增一项检查时打破一个与语义无关的数字。
- **FR-043**: 每个检查器 MUST 至少对一份**真实存在**的仓内制品只读地跑通一次并留下真实输出,作为它可运行的证据;「能编译」不构成「能启动」的证据。

#### 中立性、预算中立与漂移守卫

- **FR-044**: `templates/` 下新增的一切内容 MUST 项目中立:MUST NOT 含 `spec-kit` / `specify-cli` / `specify_cli` / `cloud-native-ai` 一类本仓专名。
- **FR-045**: 本特性落地后,`scripts/python/scan-confirmation-gates.py` 的 total MUST 仍为 **23**、violations MUST 为 **0**。整数余量为 0 且该上限由三处不同形态的断言钉住,故 MUST 以措辞设计回避命中,MUST NOT 放宽被扫描文档集、调高上限或修改任何基线数据。
- **FR-046**: 本特性触及的每个检查器 MUST 在落地时**同时**具备钉住其检查项标签集与退出码表的契约测试;MUST NOT 留下任何一个零守卫的检查器。既有的 `validate-tasks.py` 两处钉子均已存在(见现状锚点),故对它的义务是「新增检查项的同一提交内扩充这两个钉子」;对本特性新建的检查器则是「落地即建钉」。
- **FR-047**: 检查器 MUST 随包安装到运行时镜像,并被镜像同步的一致性检查覆盖(与 `validate-tasks.py` 同待遇)。
- **FR-048**: 本特性 MUST NOT 新增任何门控停等点、MUST NOT 改变 `/speckit.*` 的阶段划分或状态机、MUST NOT 引入守护进程或文件监听;检查器只由命令在其既有步骤内调用,或由测试直接调用。

### Key Entities *(include if requirement involves data)*

- **检查器 (Checker)**: 一个单一入口的可执行判定者。属性:被校验制品类别、检查项标签集、退出码表、是否只读、Program-First 归属声明。关系:被一个 `/speckit.*` 命令在其既有步骤调用;被契约测试钉住。
- **命题 (Proposition)**: 制品对自己或兄弟制品做出的一个结构性断言。属性:命题文本、判定者(检查器 + 检查项标签)、当前 verdict。关系:一个命题恰有一个判定者;一个检查器可判定多个命题。
- **归属声明 (Green-Point Claim)**: 一行任务对「我负责让某条款转绿」的机器可解析陈述。属性:契约文件、条款 id、任务 id、所处阶段。关系:多条归属声明构成覆盖核算**条款侧**的「被认领子集」;FR 侧的被认领子集**不**来自归属声明,而来自条款**引用组**里的 `(FR-nnn)`(定义见 FR-026 与 C-2;FR 不是该声明面的目标)。
- **条款 (Clause)**: 一份契约里的一个可独立判定的规范单元。属性:所属契约文件、条款 id、抽取形态、是否可被 owner 定义的语法解析、**正文边界**(由 owner 声明:标记行起,至下一个条款标记或下一个章节标题先到者止,FR-022)。关系:条款全集是覆盖核算的分母。
- **未覆盖集 (Uncovered Set)**: 全集减去**对应来源的**被认领子集的差——条款侧与 FR 侧两侧各一套,分母与子集来源都不同(FR-026),MUST NOT 合并。属性:成员名单、伴生的非空量。关系:为空是覆盖完整的判据,但**只在伴生量非空时**才有意义;基线缺失时本实体不成立,MUST 以非零码退出(FR-027 § 基线面)。
- **逆样本 (Counter-Sample)**: 一份人为破坏了被守命题的最小制品。属性:破坏了哪个**检查单位**、期望的 verdict 与退出码、它键到哪个主语(SC-011 的键规则:检查标签 / 退出档 / verdict 词汇项三种同格形态)。关系:每个检查单位至少有一个逆样本;缺逆样本的单位视为未取证。
- **判据主体 (Criterion Subject)**: 一条 goal 判据所约束的对象集合。属性:表达形态(指代形 / 成员枚举)、解析时刻导出的成员集。关系:指代形使该集合可被程序导出;两种形态并存即冲突。
- **run 前置 verdict**: 团队 run 前五项检查的一次性机读结论。属性:五条 check 各自的 verdict、顶层 verdict、blocked、target 解析来源。关系:短路项记 `not-evaluated`,MUST NOT 记 `ok`。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `requirements.md` 的四类结构命题(编号连续、文档序、引用可解析、活动标记计数)全部由程序判定;对一份真实既有规格只读跑通且 exit 0,对四份各自只破坏一类命题的副本各报出对应的那一类且 exit 非 0——四次命中率 4/4,零交叉遮蔽。
- **SC-002**: `shared/constants/clarify-taxonomy.md` 里本轮加入的过渡期 awk 抽取式**已不存在**,该处改为指向检查器;全文对「Until that validator ships」的命中数为 0,且对检查器路径的命中数 ≥ 1。
- **SC-003**: 「条款由哪一行任务转绿」成为可解析面:对一份归属序与阶段序一致的最小 tasks.md 跑检查器得 0 WARN,对一份把归属行放到更早阶段的副本得 ≥1 WARN 且点名条款与阶段——两个方向都被实测。
- **SC-004**: 悬空归属(指向不存在的契约文件或条款 id)被判为 ERROR 而非 WARN,且在退出码上可区分:悬空归属 exit **1**、仅跨阶段 WARN exit **0**(不新设第三档)。
- **SC-005**: 覆盖核算以集合差表达:对一份 3 条款契约、2 条被认领的最小 spec,印出的未覆盖集恰为那 1 条且每行以 [[STR-009]] 起首;补上认领后未覆盖集为空且伴生量非零。两次运行按**名字**比对而非按计数。
- **SC-006**: 条款语法有唯一 owner:owner 文档存在、声明其覆盖的形态、并被核算脚本引用;对全仓 `.specify/specs/*/contracts/` 跑一次只读扫描,输出「可按 owner 语法解析的文件数 / 逐个点名跳过的文件数 / **本次实扫总数**」三个数,且前两者之和**等于第三者**(反空真哨兵)。该哨兵 MUST 是**关系式**而不是一个字面总数——本特性自己的契约就在被扫描面内,任何写死的总数都会在其落盘那一刻自我证伪(实测:改前 110、本特性 7 份契约落盘后 117,差值恰为 +7)。
- **SC-007**: [[STR-005]] 一次调用输出五条 check 且字段齐备;对一个 goal 已终态的真实团队跑,对应 check 的 verdict 属既有词表、顶层 blocked 为真;对不存在的 slug 跑,`.specify/goal/` 与 `.specify/teams/` 的字节校验和前后不变;两次的退出码按 [[STR-007]] 分别落在阻塞档与输入错误档。
- **SC-008**: 短路项不报绿:构造一个使某项检查前置条件不成立的团队,该条 verdict 为 [[STR-004]] 而非 `ok`,且其余四条仍被评估(不被异常吞掉)。
- **SC-009**: 指代形的价值可被直接看见:对同一主体集合分别用指代形与成员枚举写两条判据,在目录里增删一个成员后,指代形导出的集合随之变化而枚举形不变——该差异在输出里可见。
- **SC-010**: 向后兼容:本特性落地前后,对仓内**全部**既有 goal 定义跑一次解析,失败集合按名字比对为空(不是按计数比对)。
- **SC-011**: 「机器给出的绿」的证据纪律被执行:本特性新增的检查项**逐项**都有逆样本,逆样本数 ≥ 检查项数;守卫负面命题的检查项逐项都有一次变异演练记录(弄坏→变红→复原→恢复绿),且演练临时产物的残留计数为 0。**主语、键与分母**(2026-10-03 定,来源 `/speckit.analyze` E-02:原判据无法由命令计算——它没有说逆样本按什么归到主语,也没说分母取哪个集合):「检查项」= 一个检查器可被**单独点名**的一个 verdict 单位,三种同格形态之一——一个检查标签、一个退出档、一个 verdict 词汇项;每条逆样本 MUST 记它键到哪个单位(既有字段「哪条变红」就是这个键),对没有标签集的主语(既有脚本里新增的 action)MUST 以「action + 期望档」为键;分母 MUST 取**本特性新增**的单位数——一个既有脚本被扩了 4 项,分母就是 4,而不是它 docstring 里现有的 10 项。
- **SC-012**: 预算与中立性保持:落地后 `scan-confirmation-gates.py` 的 total 仍为 23、violations 为 0;`templates/` 下新增内容对本仓专名的命中数为 0;全量测试相对开工时冻结的**名字级**基线的新增失败集为空。

### Measurement Sources & Collection Methods

- **SC-001 / SC-003 / SC-004 / SC-005 Source**: 检查器的实跑输出与退出码。取证形态:对真实制品只读跑一次贴出完整输出;对每份人为破坏的副本各跑一次贴出被点名的检查项与退出码。破坏副本 MUST 建在临时目录,MUST NOT 落在 `.specify/specs/` 下。采集时机:实现该故事的阶段收尾各一次。
- **SC-002 Source**: `grep -c` 对 `shared/constants/clarify-taxonomy.md` 的两次计数(过渡式命中数应为 0、检查器路径命中数应 ≥1),配一条反空真哨兵(该文件非空且文档序不变量小节仍在场),使「0 因为已移除」与「0 因为整节丢失」可区分。
- **SC-006 Source**: 核算脚本对 `.specify/specs/*/contracts/` 的一次只读全量扫描输出。基线值:逐形态的文件数与条款 id 数由 `notes/clause-form-census.md` **唯一拥有**(含分类命令、两个 as-of 值与自指修正说明),本节不复写。该基线 MUST 连同**当轮 owner 声明覆盖哪些形态**与 **as-of 提交**一起记录,否则「可解析文件数」在两个 owner 定义之间、以及两个时点之间都不可比。采集时机:owner 文档落地后一次、核算脚本落地后一次。
- **SC-007 / SC-008 Source**: `run-checks --json` 的实跑输出与退出码,加 `.specify/goal/` 与 `.specify/teams/` 在调用前后的字节校验和对比。实验 MUST 在临时仓库副本里做,真实 goal 与团队定义 MUST NOT 被改动;若只能在真实树上验证,则 MUST 只跑只读路径并记录校验和不变作为证据。
- **SC-009 / SC-010 Source**: 解析器对两条判据的导出集合输出(增删成员前后各一次),以及对仓内全部既有 goal 定义的批量解析结果;SC-010 的比对 MUST 按失败**名字**集合(`comm -13` 形态),MUST NOT 按计数。
- **SC-011 Source**: 本特性 `verification.md` 里的逆样本清单与变异演练记录,每项含:植入什么、哪条变红、如何复原、复原后的差异复核结果。演练临时产物的残留计数由一次 `find` 实测。
- **FR-027 基线 Source**: 采集面与采集时机 MUST NOT 在此复写——采集面由 **FR-027 § 基线面** 唯一拥有(那份排除本特性自己 spec 目录的 excl-`<ID>` 语料,其两端值由 `notes/clause-form-census.md` 拥有),落盘与可读性约束由 `data-model.md` V-13 拥有,时机字段由 `data-model.md` E-3c 的 `frozen_at` 拥有。本节只留**方法**:一次只读扫描产出未覆盖项**名字集** → 冻结进本特性目录的一份基线文件 → 此后每轮 `comm -13 <baseline> <current>` 比对;基线缺失即非零退出(FR-027 § 基线面)。(2026-10-03 订正,来源 `/speckit.analyze` F-17:此行原复写「全仓 `.specify/specs/*/contracts/`」这一**修订前**采集面、并写「实现 US3 的阶段开工时一次」,而 `data-model.md` E-3c 说 `frozen_at` = 实现开工时刻、`tasks.md` T026 说首次全树运行时——三处三种时机,采集面与修订后的 FR-027 直接冲突。它不是旁注:`checklists/requirements.md` 的检查项把读者明确指向本行取采集方法。修法是依 one-source-of-truth 改为引用,而不是在这里再印一个值。)
- **SC-012 Source**: `scan-confirmation-gates.py --summary` 的 total 与 violations 真实数字;对 `templates/` 新增内容的专名 grep 计数;以及全量测试相对**开工时冻结的名字级基线**的 `comm -13` 差集(基线用 `run-tests.sh --names-out` 采集,记入本特性目录)。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `[green: <contract>#<clause>]` | FR-015, FR-016, FR-020, US2 验收场景 1, contracts/green-point-claim.md, tasks 模板的形态说明 |
| `STR-002` | `ORDER BREAK: <ID> after <ID>` | FR-008, US1 验收场景 2, requirements 检查器的文档序检查输出 |
| `STR-003` | `0 error(s), 0 warning(s)` | FR-003, US1 验收场景 1, 人读输出的计数尾行形态 |
| `STR-004` | `not-evaluated` | FR-032, SC-008, US4 验收场景 2, run-checks 的短路项 verdict。**本条是新造字面量**(实测在 `scripts/python/goal-utils.py` 零命中),故该脚本的有效 verdict 词表是 STR-006 ∪ {本条} |
| `STR-005` | `run-checks` | FR-029, SC-007, goal-utils 的 action 名与 `--help` 行 |
| `STR-006` | `ok\|no-goal-definition\|dangling\|target-terminal\|cross-goal\|goal-terminal\|input-error` | FR-032, US4 验收场景 1, run-checks 的单项 verdict 词表(沿用既有,不新造;7 个字面量已逐个实测命中 `scripts/python/goal-utils.py`)。**这 7 个是 `run-checks` 的词表,不是该二进制的全词表**:实测该脚本另发第 8 个字面量 `rejected`(`:935` `check-statement`、`:968` `targets --check`,均配 `EXIT_INPUT_ERROR`),二者与五项检查无关,故 MUST NOT 因本条被删改 |
| `STR-007` | `0=ok / 2=input-error / 3=not-found / 4=invalid / 5=blocked` | FR-033, SC-007, run-checks 的退出码表。**沿用 `scripts/python/goal-utils.py:44-47` 既有的 `EXIT_OK=0 / EXIT_INPUT_ERROR=2 / EXIT_NOT_FOUND=3 / EXIT_INVALID=4` 四码原义**,只为 `blocked` 取下一个空闲码 **5**(实测 `scripts/python/` 全目录零占用) |
| `STR-008` | `Program-First discipline (shared/guidelines/token-efficiency.md)` | FR-002, 每个新检查器 docstring 的归属声明首句 |
| `STR-009` | `UNCOVERED:` | FR-024, SC-005, 未覆盖集每行的前缀 |
| `STR-010` | `SUBJECT EMPTY:` | FR-036, US5 Edge Case, 指代形导出空集合时的报错前缀 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

### Session 2026-09-24

- Q: 053 该绑到哪个 Feature?五个故事横跨 requirements 检查器、tasks 归属声明面、覆盖核算、goal-utils 新 action 与 goal 判据主体,无任何既有 Feature 覆盖这五者。 → A: **新建 Feature 053(Draft)**。判定与逐候选排除理由写进 `## Related Feature`;决定性先例 `features/040.md:57-63`(051 判新建),沿用 052 的「投递载体 ≠ 归属事实」。
- Q: STR-007 的退出码表与 `goal-utils.py:44-47` 既有的 `EXIT_*` 常量在码 3 与码 4 上冲突(同一二进制内一码两义),怎么对齐? → A: **沿用既有四码原义,`blocked` 取下一个空闲码 5**。STR-007 改为 `0=ok / 2=input-error / 3=not-found / 4=invalid / 5=blocked`;FR-033 增「MUST NOT 让同一个码按 action 而有两种含义」。实测 5 在 `scripts/python/` 全目录零占用,既有调用方 `team.md:96,98` 只按 0/2 分支故不受影响。
- Q: 覆盖核算对既有 44 个 spec 目录(42 个含 `contracts/`)怎么适用?实测 110 份契约里只有 31 份有机器可抽取的条款形态,其余 79 份 `.md` 一份都没有。 → A: **冻结名字级基线,只对新增未覆盖项阻断**。 **(2026-10-02 订正,原提问在 2026-09-24:提问时所给的两个数均为假——`/speckit.plan` 的探查轮重新分类后实测为可解析 **57 / 110**、残余 **53** 份(as-of 本特性自己的契约落盘**之前**;该量会变动,当前值由 `notes/clause-form-census.md` 唯一拥有),因为 `## C-N` 标题形(25 份)与 `**C-N (标签)**` 括注形(1 份)同样机器可抽取,原测量只认闭合粗体。裁定本身不受影响:残余量级从 79 降到 53 不改变「不产生永久豁免清单」这一取舍理由,故 A 项照旧成立;此处按追加而非替换的方式记下,决定原文不动。)**FR-027 的活动标记据此移除并改写为该判据;比对按名字集合(`comm -13` 形态)而非计数,与本 spec SC-010 / SC-012 同形;基线内既有项不阻断但每轮仍印出计数。
- Q: FR-003 要求的「逐项检查的 verdict」数组在既有 `validate-tasks.py --json` 里并不存在,既有脚本要不要补? → A: **只辖新增检查器**。既有 `validate-tasks.py` 保留其四键 JSON,MUST NOT 因本特性被要求迁移;它只受 FR-046 的钉子扩充义务与 FR-017/FR-018 的新增检查项约束。该读法已写进 FR-003 尾部,并显式声明 FR-005 的只读性**普遍**适用于全部检查器——形态类辖新增、安全类辖全部,这一不对称是刻意的。

### Session 2026-10-02

- Q: (来自 `/speckit.plan` Phase 0)FR-018 的第二个 WARN 该检哪个命题——规格字面的「同条款同区间」,还是 `templates/commands/tasks.md:197` 已声明的「同一测试路径出现在两个核验行且绿点不同」? → A: **两者都机械化**。FR-018 据此改写为覆盖 (a)(b) 两个命题且 MUST 分列报出;US2 增验收场景 6(正反两向)。理由:该处散文自检与 `.specify/memory/glossary.md`「条款分区 (Clause Partition)」条目里的「生成期 MUST 机械核算」是同一义务,而 US2 恰好在建它所需的全部解析数据(行级测试路径由既有 `_classify_paths` 抽出、绿点由新 `[green:]` 声明抽出),边际成本仅一个检查标签 + 一个逆样本 + 一个钉子条目。**该裁定扩大了 FR-018 的范围,故按 `/speckit.plan` 的上游优先规则先改本文件再填计划模板;FR/SC 编号未变(仍 48 / 12),故无需重编号。**

### Session 2026-10-03

用户指令原文(逐字,`/speckit.analyze` 之后的整改授权):`Generate concrete remediation edits for the top 3 corrections and 3 spec amendments`

- Q: (来自 `/speckit.analyze` F-07,HIGH)基线在 US3 阶段冻结、认领在 Polish 阶段落地,顺序不可调换;而 FR-027 的冻结面按原文**含**本特性自己的目录。这样 GATE-8/T046/DoD-7 的自举判据对任何认领结果都报空——它该永不变红吗? → A: **冻结面排除本特性自己的 spec 目录**,FR-027 据此增「基线面」+「配套正向完备量」两句。这不是新裁定:plan § XI 与 `notes/clause-form-census.md` 都写明 053 自己的条款 MUST NOT 被基线豁免,而 `comm -13` 的单调性使该义务与「冻结面含自身」互斥——恰有一种与已记录意图一致的读法,故属纠正;独立校验子代理已实测冻结时刻自身项 100% 未覆盖(认领只在 T045 落地)并确认无任务在 T045 之后重冻。
- Q: (来自 `/speckit.analyze` F-05,HIGH)T045 要给 48 个 `requirements.md#FR-NNN` 认领,但 owner 声明的六种形态全部以 `C-\d+` 为键、C-11 又要求「对该文件不可解析的形态 MUST 报 `green-dangling`」——GATE-7 因此不可满足。是给 owner 加第七种形态,还是让 C-11 豁免非契约文件? → A: **两者都不做:FR 不是认领目标**。契约条款才是 `[green:]` 的唯一目标面;FR 的覆盖由核算器按 FR-026 的**第二个全集**独立判定——全集 = `requirements.md` 的 FR 定义行,被认领子集 = 各契约条款行尾的 `(FR-nnn)` 反向引用。依据是已记录的三条而非新意向:FR-015/FR-016 把声明面定义为指向**契约文件与条款 id**、FR-021 禁止把形态说明落在某个 spec 的散文里(T025 那句「本行 DESIGNATES that convention」正是它禁止的东西)、FR-026 明写两个全集来源不同 MUST NOT 合并。→ T025/T045/GATE-7/DoD-7 据此改写。**(2026-10-03 第二轮订正**:该轮只收回了认领面,没给替代规则找 owner——「FR 侧被认领子集 = 条款行尾反向引用」当时仍只活在 `tasks.md` 的散文里。现由 **FR-026** 声明、`contracts/clause-coverage.md` C-18 承判据、§ Key Entities「归属声明/未覆盖集」两条按两侧来源改写、`data-model.md` E-4/E-5b 同步;并按 F-20 的裁定把 `feature-ref.md` 定位为同一规则的**发布视图**而非第二个独立结论。**)
- Q: (来自 `/speckit.analyze` E-02,HIGH)GATE-9 写 `≥14`,同一行自己给出的分解 `5+4+3+2+3` 却是 17,且逐故事计数与其来源工件不一致。该钉哪个数? → A: **一个都不钉**。GATE-9 改为关系式判据:每个新检查器的逆样本数 ≥ **该检查器自己的**已钉标签数(owner = 模块 docstring,per D-5)+ 其契约额外要求的成对/逐档样本;计数由命令导出。理由:把总量抄进门里就是本特性要消灭的那类「多处出现的一个数」(XIV),而 `data-model.md:69-71` 已是标签集的拥有者。**(2026-10-03 第二轮订正**:本行当时称 data-model 为标签集的拥有者,而 D-5 与 GATE-9 称 owner = 模块 docstring——同一事实被登记了两个 owner。现行分工:**全量标签集 → 该检查器自己的模块 docstring(D-5)**,**本特性新增子集 + 主语键 → SC-011**,门取后者作分母;该轮把关系式判据写出来却仍未使其可由命令计算(五个主语里三个落在「每个新检查器」这个量化域之外、`goal-utils.py` 的 docstring 是 action 名而非检查标签),据 SC-011 的新键规则改写 GATE-9。**)
- 三项整改的落点(同一轮):`contracts/clause-coverage.md` C-21、`tasks.md` T025/T026/T045/T046/T040/GATE-2/GATE-7/GATE-8/GATE-9/DoD-7/Environment 段、`plan.md` § Mirror Obligations、`quickstart.md` 场景 3 与场景 11 的实测表。三项纯纠正(E-01 漏跑的 `b2.md`、F-06 缺失的 `T031` 依赖边、E-04 漏列的 `skills` 镜像对)与一处必须同行的连带订正(F-03 全树 DIFF 计数 3 → 实测 33,新镜像行的改前值依赖它)一并落地;FR/SC/STR 编号未变(仍 48 / 12 / 10),无需重编号。**(2026-10-03 第二轮订正**:该清单漏了三处真实落点——`features/053.md`、§ Key Entities、本文件 SC 的 FR-027 Source 行——并把 C-21 配对判据的 quickstart 落点写成场景 11(实为场景 7);漏记的后果由第二轮检测代理实测出:登记说「已全部落地」而采集面仍写着修订前的值。**)

- Q: (第二轮 `/speckit.analyze` 的三条 裁定,用户授权「按照建议修复掉所有的阻塞问题」)GATE-9 的分母取哪个集合、FR 覆盖规则由谁拥有、一条条款的正文到哪里结束——三处工件都没有记过选择,怎么定? → A: 三条都按「与最多已记录意图一致」落定,并在此留下裁定痕:① **分母 = 本特性新增的检查单位数**,主语键与三种同格形态(标签 / 退出档 / verdict 词汇项)由 SC-011 声明——FR-039、`checker-form.md` C-16、SC-011 三处早已一致说「新增」,只有本轮的 GATE-9 草稿说全量;② **FR-026 拥有两个子集的来源**,`feature-ref.md` 是核算器同一规则的发布视图——它自己已声明拥有映射事实、`plan.md` 也这么说,缺的只是把「谁计算、谁发布」分开;③ **条款正文边界 = 标记行到下一个标记或下一个章节标题先到者**,由 FR-022 交给 owner 文档声明——本特性 182 条里恰有 2 条的 `(FR-nnn)` 在标记行之后的行上,按行读会静默丢引用,而按块读到标题为止能同时解释 feature-ref 现有的 192/166/16 三个数(实测脚本按此规则重导:182 块、48/48 覆盖、192 含重复、166 唯一对、16 条不引用 FR——全部复现,唯二变化是 FR-014 少一条 `requirements-checker` C-21、FR-025 多一条 `clause-coverage` C-21)。②③ 是可覆盖的:若更希望 `feature-ref.md` 自己算而不是引用抽取器,或希望边界「只到下一个标记」(则总数 193),说一声即可回退。
