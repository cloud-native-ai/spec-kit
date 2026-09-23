# Requirements Specification: 机器可判定的制品命题(Machine-Decidable Artifact Propositions)

**Requirement Branch**: `053-machine-decidable-artifacts`  
**Created**: 2026-09-23  
**Status**: Draft  
**Input**: User description: "让制品的结构性命题由机器判定,而不是由 LLM 目测。本轮 /speckit.feedback consume 的自省报告把 5 个「需要新能力而非小编辑」的项路由到了本命令,它们是同一个主题的五处缺口:一处制品对自身结构做断言(编号连续、引用可解析、计数正确),或一处制品对兄弟制品做断言(某条款由哪一行任务转绿、某判据的主体是否被覆盖),而这个断言当前只能靠代理阅读后声明,于是错前提会静默进入下游。五项:① requirements.md 没有确定性校验器(FR/SC 编号连续性与文档出现序、每个 FR-/SC-/[[STR-]] 引用可解析、活动标记计数只应数「带冒号且未被反引号包裹」的实例);同型先例已存在:validate-tasks.py 之于 tasks.md。② 「条款由哪个任务转绿」这一归属关系对结构校验器不可见,需要先在 tasks 模板定义行内归属声明面,再给校验器增 WARN 级「绿点跨阶段」检查。③ 机器覆盖核算(contracts 每条条款与每条 FR 恰被一行任务认领,由脚本印出未覆盖集),其前置缺口是 contracts 的条款语法当前没有 owner。④ goal 判据主体的「目录指代形」——当前靠成员枚举,脆弱且不可程序指代。⑤ goal-utils.py 增 run-checks action,一次输出团队 run 前置五项检查的 JSON verdict。跨切面约束:(a) 校验器给出的绿同样受快速失败纪律约束,每个新检查都 MUST 有逆样本;(b) 门控预算余量为零,任何新增措辞须零命中;(c) templates/ 保持项目中立;(d) 新增检查器 MUST 走 Program-First 的既有归属声明形态;(e) validate-tasks.py 在改动前没有任何契约测试钉住其检查项计数与退出码表,新校验器不要重蹈。"

## Related Feature *(mandatory)*

<!--
  ACTION REQUIRED: Keep the default values as "Need clarification" in the initial draft.
  /speckit.clarify must resolve this section to the final Feature binding before planning.
-->

**Feature ID**: Need clarification  
**Feature Name**: Need clarification

## Overview

框架的每一份制品都在对自己或兄弟制品做**结构性命题**:`requirements.md` 声称自己的 FR 编号连续、声称每个交叉引用都能解析、声称活动标记还剩几处;`tasks.md` 声称某条契约条款会由某一行任务转绿;goal 判据声称它约束的主体是某一组东西。今天这些命题**全部由阅读者(代理)在目测之后声明**,而声明一旦写进制品,下游就把它当事实引用。

后果不是"偶尔看错",而是**错前提静默扩散**:一份声称「107/107 条款已覆盖」的 tasks.md 会把一个结构性不可满足的验收条件送进 implement;一份声称「零残留旧计数」的 clarify 回写会在编号已经变了的情况下通过。本仓最贵的一类缺陷正是这个形态——检查跑完给出了绿,但那个绿不是关于它被写来判定的那个命题的(见 `.specify/shared/guidelines/fast-fail.md` 的机器绿条款与 `docs/reference/history/00-cross-cutting-lessons.md` § 十二)。

本特性把这类命题**从散文搬进程序**:每个命题获得一个确定性判定者(检查器),命题的真假由退出码与机读 verdict 表达,而不是由某一行自陈的数字表达。已有同型先例可循——`scripts/python/validate-tasks.py` 之于 `tasks.md`;本特性沿用它的形态,把它扩展到 `requirements.md`、把「条款→任务」的归属关系变成可解析的声明面、并给 goal 侧两个当前只能靠内部函数或成员枚举表达的命题装上 CLI 入口。

**本特性不做什么**(边界,避免与相邻纪律混淆):

- 不引入任何新的门控停等点。检查器输出的是**判定**,授权语义仍归 `.specify/shared/guidelines/confirmation-gates.md`。
- 不改变 `/speckit.*` 命令的阶段划分或状态机。检查器接进既有步骤,不新增步骤。
- 不做语义正确性判断(某条 FR 写得好不好、某个故事是否真的独立可测)。程序只判**可机械判定的结构命题**;语义判断仍归 `/speckit.analyze` 与 `/speckit.clarify`。
- 不回溯改造既有 spec 的契约文件(见 FR-027 与下方 Clarification 标记)。

### 现状锚点(以源码实测为准,2026-09-23)

| 事实 | 实测值 | 对本特性的意义 |
|---|---|---|
| `scripts/python/validate-tasks.py` 的检查面 | 5 项,全部基于**任务→任务**图(行形态、ID 唯一、blockedBy 可解析、`[P]` 并行安全、story 标签位置) | 条款→任务归属**结构性不可见**,这是 US2 的缺口本体 |
| 该脚本改动前的契约钉子 | **0 个**(全仓无任何测试钉住其检查项集合或退出码表) | 零漂移守卫状态;本特性 MUST NOT 重蹈(FR-046) |
| 契约文件总数 | **110**(`.specify/specs/*/contracts/` 下 100 个 `.md` + 10 个 `.yaml`) | 覆盖核算的分母;也说明条款语法不统一 |
| 采用 `**C-N**` 条款形态的契约文件 | **21 / 110** | 条款语法**无 owner**,故 US3 必须先解决归属再谈核算(FR-022…FR-026) |
| `goal-utils.py` 现有 action | `create` / `validate` / `check-statement` / `list` / `status` / `objective` / `criteria` / `migrate` / `targets` | `run-checks` **未被占用**;`preview_target_check` 与 `resolve_effective_target` 无 CLI 入口(US4 缺口本体) |
| 门控扫描器预算 | total **23**,cap = 93 × 0.25 = **23.25**,整数余量 **0**,由**三处不同形态**的断言钉住 | 任何新增措辞须零命中(FR-045) |
| 标识符冲突检查 | `validate-requirements` / `run-checks` / `[green:` / `clause-ref` / `validate_requirements` 在非 spec、非 memory 的跟踪文件里**零命中** | 本特性引入的新标识符均无碰撞 |
| `shared/constants/clarify-taxonomy.md` 的文档序不变量 | 本轮(2026-09-23)刚加入,含一段**过渡期** awk 抽取式与一句「Until that validator ships」的接线声明 | US1 MUST 接管它并**移除该过渡副本**(FR-014)——这是本特性对既有制品的一笔明确债务 |
| `shared/guidelines/requirements-guidelines.md` § Validation Process | 只有勾选项清单,**无检查器**;计数与引用解析留给目测 | US1 的落点 |

### Assumptions

- **A-1 制品形态稳定**:被校验制品是 Markdown 文本,其结构由 `.specify/templates/` 下的模板定义。检查器判的是「制品是否符合其模板声明的结构」,不是「制品写得好不好」。
- **A-2 单一消费通道**:检查器由 `/speckit.*` 命令在自己的既有步骤里调用,并由契约测试直接调用;不提供守护进程、不做文件监听、不接入 CI 之外的任何自动触发面。
- **A-3 零写入**:所有检查器 MUST 是只读的。判定结果只经 stdout / 退出码表达,MUST NOT 修改被校验制品(与 `validate-tasks.py` 现状一致)。
- **A-4 增量生效**:新检查器对**本特性之后**产出的制品强制;对既有制品的适用性见 FR-027 与下方标记。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - `requirements.md` 的结构性命题由校验器判定,而不是由作者自陈 (Priority: P1)

写规格的人(或代理)在 `requirements.md` 里印出「38 条 FR、12 条 SC、零残留活动标记」这类数字时,今天没有任何程序核对过它们。本故事给 `requirements.md` 装一个与 `validate-tasks.py` 同形的确定性校验器:编号连续且按**文档出现序**、每个 `FR-\d+` / `SC-\d+` / `[[STR-\d+]]` 引用都能解析到本文件内的一处定义、活动标记的计数只数**带冒号且未被反引号包裹**的实例。命令在写完规格后跑它,按退出码决定是否继续。

**Why this priority**: 这是五项里唯一**已有同型先例、已有明确落点、且被另一处制品显式等待**的一项——`shared/constants/clarify-taxonomy.md` 本轮刚写入的文档序不变量明写「Until that validator ships」,并临时携带一段 awk 抽取式作为过渡副本。不落地 US1,那段过渡副本就长期留在 owner 文档里成为第二份真相。同时 `requirements.md` 是整条链的最上游,它的错前提传播距离最远。

**Independent Test**: 对一份真实的 `requirements.md`(例如 `.specify/specs/052-fast-fail-principle/requirements.md`)只读地跑一次校验器,确认 exit 0;再对四份人为破坏的副本(编号跳号、FR 换序、引用指向不存在的 STR、把一个活动标记反引号包裹后期望计数不变)各跑一次,确认每份都被点名且 exit 非 0。四份破坏样本各自只触发预期的那一项检查,即证明检查项之间不互相遮蔽。

**Acceptance Scenarios**:

1. **Given** 一份 FR 编号连续、引用全部可解析、活动标记为零的 `requirements.md`,**When** 跑校验器,**Then** exit 0,人读输出逐项列出已执行的检查与 `0 error(s)`,机读输出的 error 计数为 0。
2. **Given** 一份把 `FR-007` 插到 `FR-012` 之后的规格(ID **集合**仍连续),**When** 跑校验器,**Then** 报出文档序违例并按 [[STR-002]] 的形态点名是哪一条排在哪一条之后,exit 非 0。
3. **Given** 一份规格,其正文含一个**被反引号包裹**的 STR 引用形态(属提及)与一个**裸写**的 STR 引用形态(属真实引用),且二者指向的编号都超出 Shared Strings 表的定义范围,**When** 跑校验器,**Then** 只对裸写的那一个报出引用不可解析并给出其行号,对被反引号包裹的那一个不报,exit 非 0。
4. **Given** 一份讨论澄清机制、因而正文里大量出现被反引号包裹的标记名的规格,**When** 跑校验器,**Then** 活动标记计数**只**统计带冒号且未被反引号包裹的实例;被反引号包裹的标记名一律不计入。
5. **Given** 校验器已在命令流程里接好,**When** 它报出任一 ERROR,**Then** 命令 MUST NOT 继续进入下一阶段,并 MUST 把校验器的输出原样呈现(而不是复述或概括)。
6. **Given** US1 已落地,**When** 复核 `shared/constants/clarify-taxonomy.md`,**Then** 那段过渡期 awk 抽取式已被移除,该处的文档序不变量改为指向校验器,且「Until that validator ships」一句已删除。

---

### User Story 2 - 「哪条条款由哪一行任务转绿」成为可声明、可解析、可校验的面 (Priority: P1)

今天 `tasks.md` 的每一行只声明它写哪些文件;一条契约条款会不会被转绿、由哪一行负责,只存在于契约散文里。于是当 MVP 截断到前两个故事时,**没有任何东西**能发现「第三个故事的验收条件依赖一个排在它之后的阶段」这种结构性不可满足。本故事在 tasks 模板定义一个行内归属声明面,并给 `validate-tasks.py` 增一项 WARN 级检查:归属任务集中任一任务所处阶段晚于本行,即报「绿点跨阶段」。

**Why this priority**: 与 US1 同为 P1,因为它俩合起来才闭合「制品对自身结构的命题」这一类:US1 管一份制品内部的自洽,US2 管两份制品之间的归属。而且 US3 的覆盖核算**依赖**本故事的声明面——没有可解析的归属,核算无从谈起。先例证据:本轮消化的一条 implement 反馈正是「条款由哪个任务转绿对结构校验器不可见」,已由自省报告 F-05 定级为需新能力。

**Independent Test**: 构造两份最小 tasks.md + 一份最小契约:甲的两行任务分别认领条款 C-1、C-2 且阶段序与认领序一致;乙把认领 C-2 的行放在认领 C-1 的行**之前**的阶段。对甲跑校验器应 exit 0 且零 WARN;对乙应报出跨阶段绿点 WARN 并点名涉及的行与阶段。再对丙(归属标记指向一份不存在的契约文件)跑,应报不可解析——三向合起来证明该检查既能发现真问题,又不误报正常排布。

**Acceptance Scenarios**:

1. **Given** 一行任务按 [[STR-001]] 的形态声明它认领某契约的某条款,**When** 跑校验器,**Then** 该声明被解析为 `(契约文件, 条款 id, 任务 id, 所处阶段)` 四元组。
2. **Given** 某条款的归属任务集中存在一个所处阶段**晚于**声明行的任务,**When** 跑校验器,**Then** 报 WARN 级「绿点跨阶段」,点名条款、涉及的行与阶段序,exit 码为「有 WARN 无 ERROR」对应的那一档。
3. **Given** 一条归属声明指向不存在的契约文件或不存在的条款 id,**When** 跑校验器,**Then** 报 ERROR(不可解析),而不是 WARN——悬空归属比跨阶段归属更严重。
4. **Given** 一行任务声明了归属但**未**声明文件路径,**When** 跑校验器,**Then** 既有的行形态检查 MUST NOT 因此误报;归属声明与路径声明是两个正交的面。
5. **Given** 两份任务行认领**同一条款的同一区间**,**When** 跑校验器,**Then** 报 WARN 并点名两行——这与 `.specify/memory/glossary.md` 已登记的「条款分区 (Clause Partition)」是同一失效模式的两面:该术语讲的是「同一契约测试文件被多阶段核验行认领」,本检查把它机械化。

---

### User Story 3 - 覆盖核算:每条条款与每条 FR 恰被一行认领,未覆盖集由脚本印出 (Priority: P2)

`tasks.md` 今天可以自陈「107/107 条款已覆盖」而无人核对。本故事让覆盖成为一个**印出来的集合差**而不是一个声明的数字:脚本读契约与 tasks,把「每条条款、每条 FR」的全集减去「被某一行认领」的子集,印出未覆盖集;为空才算覆盖完整。前置条件是给契约的条款语法指定 owner——实测 110 份契约里只有 21 份用 `**C-N**` 形态,其余各异,没有 owner 就没有全集。

**Why this priority**: P2 而非 P1,因为它依赖 US2 的声明面,且必须先解决条款语法的归属问题;而归属问题触及 110 份既有文件,是本特性里唯一可能引发大范围返工的一项。它的价值最高(直接消灭「自陈覆盖率」这一类假绿),但落地顺序必须在 US1/US2 之后。

**Independent Test**: 在一个临时目录里搭一份最小 spec(一份 3 条款的契约 + 一份 tasks.md,其中 2 条被认领、1 条未被认领),跑核算脚本,确认它印出的未覆盖集恰为那 1 条、exit 非 0;再把第 3 条补上认领,确认未覆盖集为空、exit 0。两次运行的差集必须**按名字**比对,而不是按计数——计数相等会掩盖成员变化。

**Acceptance Scenarios**:

1. **Given** 条款语法已有 owner 文档,**When** 核算脚本读一份契约,**Then** 它按 owner 定义的形态抽出条款全集,并对无法按该形态解析的文件**逐个点名**而不是静默跳过。
2. **Given** 一份 tasks.md 漏认领了某条款,**When** 跑核算,**Then** 未覆盖集按 [[STR-009]] 的前缀形态印出该条款,exit 非 0。
3. **Given** 覆盖完整,**When** 跑核算,**Then** 未覆盖集为空,且脚本 MUST 同时印出一个**必须非空**的伴生量(已认领条款数、被扫描契约文件数),使「空因为对」与「空因为盲」可区分。
4. **Given** 某条款被**两行**任务认领,**When** 跑核算,**Then** 报出重复认领并点名两行——「恰被一行认领」中的「恰」是双向的:漏认领与重复认领都是违例。
5. **Given** 一份 FR 未被任何任务行提及,**When** 跑核算,**Then** 它出现在未覆盖集里,与条款未覆盖分列(两者的全集来源不同,不可混为一个计数)。

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

- **制品为空或只有模板骨架**:校验器 MUST 报「无可校验内容」而不是 exit 0。一个只有占位符的 `requirements.md` 通过校验,等于给下游发了假通行证。
- **编号带字母后缀或补零不一致**(`FR-7` vs `FR-007`):MUST 判为形态违例并点名两种写法,而不是自行归一化后放行——归一化会掩盖作者的编号意图。
- **同一 ID 被定义两次**:MUST 报重复定义(ERROR),且与「引用不可解析」分列,因为二者的修法相反(一个要删,一个要补)。
- **归属声明出现在被围栏代码块包裹的示例里**:MUST NOT 被当作真实声明解析。先例:本轮消化的一条反馈正是「指针落进了围栏示例块内」,靠一次围栏感知扫描才发现。
- **契约文件是 `.yaml` 而非 `.md`**(实测 110 份里有 10 份):条款全集的抽取 MUST 覆盖两种形态,或对无法覆盖的形态**逐个点名跳过**并计入一个非零的伴生量,MUST NOT 静默忽略。
- **`run-checks` 的五项检查里有一项自身抛异常**:MUST 把该条记为 [[STR-004]] 并继续评估其余四项,MUST NOT 让一项异常吞掉整份 verdict。
- **指代形导出空集合**(目录存在但为空):MUST 报「主体集合为空」而不是让判据空真通过。
- **门控预算**:本特性新增的任何措辞若使扫描器 total 从 23 变为 24,即为违例——整数余量为 0,没有「加一条再调 cap」的余地。

## Requirements *(mandatory)*

### Functional Requirements

#### 校验器形态与 Program-First 归属

- **FR-001**: 每个新增的确定性检查器 MUST 是单一入口的可执行脚本,以被校验制品的路径为参数,以退出码表达判定;MUST NOT 要求调用方先读入制品内容再自行判断。
- **FR-002**: 每个检查器的模块 docstring MUST 按 [[STR-008]] 的形态声明其 Program-First 归属(点名规则 owner 文档),并逐项列出它执行的检查及各自判据,与 `scripts/python/validate-tasks.py` 的既有体例同形。
- **FR-003**: 每个检查器 MUST 同时提供人读输出与 `--json` 机读输出,且二者判定一致;机读输出 MUST 含被校验制品路径、逐项检查的 verdict、error 计数与 warning 计数,人读输出的计数尾行形态为 [[STR-003]]。
- **FR-004**: 检查器 MUST 对「被校验文件不存在」「被校验文件不可解析」「被校验文件为空或仅含模板骨架」三种情形给出**互相可区分**的退出码或 verdict,MUST NOT 混为同一失败形态。
- **FR-005**: 所有检查器 MUST 是只读的:判定只经 stdout 与退出码表达,MUST NOT 修改被校验制品或任何仓内文件。

#### requirements 侧的可判定命题(US1)

- **FR-006**: 系统 MUST 提供一个校验 `requirements.md` 的确定性检查器,其检查面至少覆盖:FR/SC 编号连续、编号按**文档出现序**、交叉引用可解析、活动标记计数。
- **FR-007**: 编号连续性检查 MUST 按前缀分序列独立进行(`FR-` 与 `SC-` 各自成序),MUST NOT 跨前缀比较序号。
- **FR-008**: 文档序检查 MUST 锚定在**定义行**上,而不是在 ID 的每次出现上;`## Clarifications` 一节 MUST 被排除。依据:本轮实测,按「每次出现」比对会在一份干净的既有规格上报出 5 条假违例,而按定义行锚定并排除该节后为 0——两个锚点都是承重的,不是装饰。
- **FR-009**: 引用可解析检查 MUST 覆盖 `FR-\d+`、`SC-\d+` 与 `[[STR-\d+]]` 三种形态,每条不可解析的引用 MUST 报出引用出现的行号与被引用的 ID。**被反引号包裹的引用形态属「提及」而非「引用」,MUST NOT 计入**;该区分与 FR-010 对活动标记的区分同构且同样承重——一份讨论引用机制的规格必然大量提及引用形态本身。本规格的撰写过程实测到该失效:为描述「不可解析引用」而裸写的示例本身成了一个不可解析引用。
- **FR-010**: 活动标记计数 MUST 只统计**带冒号且未被反引号包裹**的实例。依据:一份讨论澄清机制的规格必然大量出现被反引号包裹的标记名,字面匹配对它 grep-敌对——本轮实测该形态在既有规格上会给出虚高计数。
- **FR-011**: 检查器 MUST 对同一 ID 被定义两次报 ERROR,且与「引用不可解析」分列(二者修法相反:一个要删,一个要补)。
- **FR-012**: `/speckit.requirements` MUST 在写完规格后调用该检查器,并在其报出任一 ERROR 时**停止**,MUST NOT 进入下一阶段;停止时 MUST 原样呈现检查器输出,不得复述或概括。
- **FR-013**: `shared/guidelines/requirements-guidelines.md` § Validation Process MUST 写明「计数与引用解析由该检查器派生,MUST NOT 手打」,并 MUST 把清单更新的时机明确置于澄清回写**之后**。
- **FR-014**: US1 落地后,`shared/constants/clarify-taxonomy.md` 里本轮加入的过渡期 awk 抽取式 MUST 被移除,该处的文档序不变量改为指向检查器,且「Until that validator ships」一句 MUST 删除。依据:该文件是 owner,留一份过渡副本就是留第二份真相。

#### 绿点归属声明面(US2)

- **FR-015**: tasks 模板 MUST 定义一个行内归属声明面,其字面形态为 [[STR-001]];一行任务 MAY 声明零到多条归属。
- **FR-016**: `validate-tasks.py` MUST 解析该声明面为 `(契约文件, 条款 id, 任务 id, 所处阶段)` 四元组,并对指向不存在契约文件或不存在条款 id 的声明报 **ERROR**(悬空归属比跨阶段归属更严重)。
- **FR-017**: `validate-tasks.py` MUST 增一项 **WARN** 级检查:某条款的归属任务集中存在所处阶段晚于声明行的任务时,报「绿点跨阶段」并点名条款、涉及行与阶段序。
- **FR-018**: 两行任务认领同一条款的同一区间时 MUST 报 WARN 并点名两行;该检查与 `.specify/memory/glossary.md` 已登记的「条款分区 (Clause Partition)」是同一失效模式的两面,MUST 在实现处引用该术语而不是另造名词。
- **FR-019**: 归属声明 MUST 与既有的行形态检查正交:一行只声明归属而不声明文件路径时,既有检查 MUST NOT 误报。
- **FR-020**: 出现在**围栏代码块内**的归属声明 MUST NOT 被当作真实声明解析。
- **FR-021**: 归属声明面 MUST 项目中立:MUST NOT 含本仓专有名词,其形态说明 MUST 落在 tasks 模板而非某个 spec 的散文里。

#### 覆盖核算与条款语法的 owner(US3)

- **FR-022**: 系统 MUST 为契约的**条款语法**指定唯一 owner:要么指定一份既有文档为 owner 并声明其覆盖的形态,要么定义一个**最小可解析子集**并新建 owner 文档。实测依据:110 份契约文件里只有 21 份采用 `**C-N**` 形态,其余各异,当前无任何 owner(全仓 `templates/` 下无 contracts-template,`shared/definitions/` 下无定义文档)。
- **FR-023**: 核算脚本 MUST 按 owner 定义的形态抽出条款全集;对无法按该形态解析的文件 MUST **逐个点名**,并把点名数计入一个非零伴生量,MUST NOT 静默跳过。
- **FR-024**: 核算 MUST 以**集合差**表达结果:全集减去被认领子集,印出未覆盖集,前缀形态为 [[STR-009]];未覆盖集为空时 exit 0,否则 exit 非 0。
- **FR-025**: 未覆盖集为空时,脚本 MUST 同时印出至少一个**必须非空**的伴生量(已认领条款数、被扫描契约文件数),使「空因为对」与「空因为盲」可区分。
- **FR-026**: 条款未覆盖与 FR 未覆盖 MUST 分列,二者的全集来源不同,MUST NOT 合并为一个计数。
- **FR-027**: 覆盖核算 MUST NOT 要求改造既有 spec 的契约文件。[NEEDS CLARIFICATION: 核算对既有 52 个 spec 的适用性——是仅对本特性之后新建的 spec 强制、还是对既有 spec 提供只读的「不合规清单」而不阻断?前者范围可控但留下一个长期双标准,后者一次性暴露 110 份文件的真实分布但可能产出大量无法立即修的行。两种读法都成立,工件无记录。]
- **FR-028**: `.yaml` 形态的契约(实测 10 份)MUST 被覆盖核算显式处置:要么解析其 operations 作为条款全集,要么逐个点名跳过并计入 FR-023 的伴生量;MUST NOT 静默忽略。

#### run-checks 的调用契约(US4)

- **FR-029**: `goal-utils.py` MUST 增一个名为 [[STR-005]] 的 action,一次调用输出团队 run 前置五项检查的 verdict;五项为 goal-binding / dangling / target-terminal / cross-goal / goal-terminal。
- **FR-030**: 该 action MUST 复用既有的内部解析函数而**不重写第二套文法**;无 `--target` 时 MUST 先解析有效 target 再执行五项检查,并把解析结果(有效值、来源、声明的 focus)写进输出。
- **FR-031**: 机读输出的每条 check MUST 含 `id`(1..5)、`name`(上述五个名字之一)、`verdict`、`message`;顶层 MUST 含 `team_slug`、`goal_slug`、`identity_kind`、`resolution`、`checks`、`verdict`、`blocked`。
- **FR-032**: 单项检查的 verdict MUST 沿用既有词表 [[STR-006]];因前置条件不成立而被短路的检查 MUST 记为 [[STR-004]],MUST NOT 记为 `ok`。
- **FR-033**: 退出码 MUST 按 [[STR-007]] 分档,且「检查判为阻塞」与「输入不合法」与「定义不可解析」三档互相可区分。
- **FR-034**: 该 action MUST 零写入:任何一次调用都 MUST NOT 修改 `.specify/goal/` 或 `.specify/teams/` 下的任何文件。

#### goal 判据主体的指代形(US5)

- **FR-035**: `shared/definitions/goal-definitions.md` MUST 定义一个可由程序解析的**判据主体指代形**,使主体集合在解析那一刻被导出,而不是取自判据文本里的成员枚举。
- **FR-036**: 指代形指向不存在的路径时 MUST 报可区分的错误,MUST NOT 退化为空集合;导出集合为空(路径存在但无成员)时同样 MUST 报错,前缀为 [[STR-010]]——空集合会让「零个主体全部满足」空真。
- **FR-037**: 一条判据同时使用指代形与成员枚举时 MUST 报冲突,MUST NOT 静默择一。
- **FR-038**: 既有的纯枚举判据 MUST 保持完全一致的解析行为;本特性 MUST NOT 使任何既有 goal 失效或需要迁移才能继续解析。

#### 机器绿的证据纪律

- **FR-039**: 本特性新增的**每一项**检查 MUST 有逆样本取证:证明被守物真的坏掉时该检查会变红。只展示正常路径的取证不被接受——这是 `.specify/shared/guidelines/fast-fail.md` 机器绿条款的直接适用,不是本特性的额外要求。
- **FR-040**: 凡断言「某集合为空」的检查(未覆盖集、不可解析集、冲突集),MUST 在同处配一条**反空真哨兵**:断言一个必须非空的伴生量,使「空因为对」与「空因为盲」可区分。
- **FR-041**: 凡守卫**负面命题**的检查(某物不存在 / 未变化 / 未泄漏),其取证 MUST 含一次变异演练:弄坏被守物 → 确认变红 → 精确反向替换复原 → 确认恢复绿,并复核复原后该文件的差异回到预期形态。演练用的临时产物 MUST 删净并复核计数归零。
- **FR-042**: 检查项集合的钉子 MUST 以**标签集**表达,而不是以计数表达;退出码表 MUST 单独被钉。依据:本轮实测 `validate-tasks.py` 在改动前**零钉子**,而计数形态的钉子会在新增一项检查时打破一个与语义无关的数字。
- **FR-043**: 每个检查器 MUST 至少对一份**真实存在**的仓内制品只读地跑通一次并留下真实输出,作为它可运行的证据;「能编译」不构成「能启动」的证据。

#### 中立性、预算中立与漂移守卫

- **FR-044**: `templates/` 下新增的一切内容 MUST 项目中立:MUST NOT 含 `spec-kit` / `specify-cli` / `specify_cli` / `cloud-native-ai` 一类本仓专名。
- **FR-045**: 本特性落地后,`scripts/python/scan-confirmation-gates.py` 的 total MUST 仍为 **23**、violations MUST 为 **0**。整数余量为 0 且该上限由三处不同形态的断言钉住,故 MUST 以措辞设计回避命中,MUST NOT 放宽被扫描文档集、调高上限或修改任何基线数据。
- **FR-046**: 本特性触及的每个检查器(含既有的 `validate-tasks.py`)MUST 在落地时**同时**获得钉住其检查项标签集与退出码表的契约测试;MUST NOT 留下任何一个零守卫的检查器。
- **FR-047**: 检查器 MUST 随包安装到运行时镜像,并被镜像同步的一致性检查覆盖(与 `validate-tasks.py` 同待遇)。
- **FR-048**: 本特性 MUST NOT 新增任何门控停等点、MUST NOT 改变 `/speckit.*` 的阶段划分或状态机、MUST NOT 引入守护进程或文件监听;检查器只由命令在其既有步骤内调用,或由测试直接调用。

### Key Entities *(include if requirement involves data)*

- **检查器 (Checker)**: 一个单一入口的可执行判定者。属性:被校验制品类别、检查项标签集、退出码表、是否只读、Program-First 归属声明。关系:被一个 `/speckit.*` 命令在其既有步骤调用;被契约测试钉住。
- **命题 (Proposition)**: 制品对自己或兄弟制品做出的一个结构性断言。属性:命题文本、判定者(检查器 + 检查项标签)、当前 verdict。关系:一个命题恰有一个判定者;一个检查器可判定多个命题。
- **归属声明 (Green-Point Claim)**: 一行任务对「我负责让某条款转绿」的机器可解析陈述。属性:契约文件、条款 id、任务 id、所处阶段。关系:多条归属声明构成覆盖核算的「被认领子集」。
- **条款 (Clause)**: 一份契约里的一个可独立判定的规范单元。属性:所属契约文件、条款 id、抽取形态、是否可被 owner 定义的语法解析。关系:条款全集是覆盖核算的分母。
- **未覆盖集 (Uncovered Set)**: 条款全集(或 FR 全集)减去被认领子集的差。属性:成员名单、伴生的非空量。关系:为空是覆盖完整的判据,但**只在伴生量非空时**才有意义。
- **逆样本 (Counter-Sample)**: 一份人为破坏了被守命题的最小制品。属性:破坏了哪一项检查、期望的 verdict 与退出码。关系:每个检查项恰有至少一个逆样本;缺逆样本的检查项视为未取证。
- **判据主体 (Criterion Subject)**: 一条 goal 判据所约束的对象集合。属性:表达形态(指代形 / 成员枚举)、解析时刻导出的成员集。关系:指代形使该集合可被程序导出;两种形态并存即冲突。
- **run 前置 verdict**: 团队 run 前五项检查的一次性机读结论。属性:五条 check 各自的 verdict、顶层 verdict、blocked、target 解析来源。关系:短路项记 `not-evaluated`,MUST NOT 记 `ok`。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `requirements.md` 的四类结构命题(编号连续、文档序、引用可解析、活动标记计数)全部由程序判定;对一份真实既有规格只读跑通且 exit 0,对四份各自只破坏一类命题的副本各报出对应的那一类且 exit 非 0——四次命中率 4/4,零交叉遮蔽。
- **SC-002**: `shared/constants/clarify-taxonomy.md` 里本轮加入的过渡期 awk 抽取式**已不存在**,该处改为指向检查器;全文对「Until that validator ships」的命中数为 0,且对检查器路径的命中数 ≥ 1。
- **SC-003**: 「条款由哪一行任务转绿」成为可解析面:对一份归属序与阶段序一致的最小 tasks.md 跑校验器得 0 WARN,对一份把归属行放到更早阶段的副本得 ≥1 WARN 且点名条款与阶段——两个方向都被实测。
- **SC-004**: 悬空归属(指向不存在的契约文件或条款 id)被判为 ERROR 而非 WARN,且与跨阶段 WARN 在退出码上可区分。
- **SC-005**: 覆盖核算以集合差表达:对一份 3 条款契约、2 条被认领的最小 spec,印出的未覆盖集恰为那 1 条;补上认领后未覆盖集为空且伴生量非零。两次运行按**名字**比对而非按计数。
- **SC-006**: 条款语法有唯一 owner:owner 文档存在、声明其覆盖的形态、并被核算脚本引用;对 110 份既有契约跑一次只读扫描,输出「可按 owner 语法解析的文件数 / 逐个点名跳过的文件数」,两者之和等于 110(反空真哨兵)。
- **SC-007**: `run-checks` 一次调用输出五条 check 且字段齐备;对一个 goal 已终态的真实团队跑,对应 check 的 verdict 属既有词表、顶层 blocked 为真、退出码为阻塞档;对不存在的 slug 跑,退出码为输入错误档且 `.specify/goal/` 与 `.specify/teams/` 的字节校验和前后不变。
- **SC-008**: 短路项不报绿:构造一个使某项检查前置条件不成立的团队,该条 verdict 为 `not-evaluated` 而非 `ok`,且其余四条仍被评估(不被异常吞掉)。
- **SC-009**: 指代形的价值可被直接看见:对同一主体集合分别用指代形与成员枚举写两条判据,在目录里增删一个成员后,指代形导出的集合随之变化而枚举形不变——该差异在输出里可见。
- **SC-010**: 向后兼容:本特性落地前后,对仓内**全部**既有 goal 定义跑一次解析,失败集合按名字比对为空(不是按计数比对)。
- **SC-011**: 机器绿的证据纪律被执行:本特性新增的检查项**逐项**都有逆样本,逆样本数 ≥ 检查项数;守卫负面命题的检查项逐项都有一次变异演练记录(弄坏→变红→复原→恢复绿),且演练临时产物的残留计数为 0。
- **SC-012**: 预算与中立性保持:落地后 `scan-confirmation-gates.py` 的 total 仍为 23、violations 为 0;`templates/` 下新增内容对本仓专名的命中数为 0;全量测试相对开工时冻结的**名字级**基线的新增失败集为空。

### Measurement Sources & Collection Methods

- **SC-001 / SC-003 / SC-004 / SC-005 Source**: 检查器的实跑输出与退出码。取证形态:对真实制品只读跑一次贴出完整输出;对每份人为破坏的副本各跑一次贴出被点名的检查项与退出码。破坏副本 MUST 建在临时目录,MUST NOT 落在 `.specify/specs/` 下。采集时机:实现该故事的阶段收尾各一次。
- **SC-002 Source**: `grep -c` 对 `shared/constants/clarify-taxonomy.md` 的两次计数(过渡式命中数应为 0、检查器路径命中数应 ≥1),配一条反空真哨兵(该文件非空且文档序不变量小节仍在场),使「0 因为已移除」与「0 因为整节丢失」可区分。
- **SC-006 Source**: 核算脚本对 `.specify/specs/*/contracts/` 的一次只读全量扫描输出。基线值:改前实测 110 份文件、其中 21 份采用 `**C-N**` 形态(2026-09-23 实测,命令与输出记入本特性的 notes)。采集时机:owner 文档落地后一次、核算脚本落地后一次。
- **SC-007 / SC-008 Source**: `run-checks --json` 的实跑输出与退出码,加 `.specify/goal/` 与 `.specify/teams/` 在调用前后的字节校验和对比。实验 MUST 在临时仓库副本里做,真实 goal 与团队定义 MUST NOT 被改动;若只能在真实树上验证,则 MUST 只跑只读路径并记录校验和不变作为证据。
- **SC-009 / SC-010 Source**: 解析器对两条判据的导出集合输出(增删成员前后各一次),以及对仓内全部既有 goal 定义的批量解析结果;SC-010 的比对 MUST 按失败**名字**集合(`comm -13` 形态),MUST NOT 按计数。
- **SC-011 Source**: 本特性 `verification.md` 里的逆样本清单与变异演练记录,每项含:植入什么、哪条变红、如何复原、复原后的差异复核结果。演练临时产物的残留计数由一次 `find` 实测。
- **SC-012 Source**: `scan-confirmation-gates.py --summary` 的 total 与 violations 真实数字;对 `templates/` 新增内容的专名 grep 计数;以及全量测试相对**开工时冻结的名字级基线**的 `comm -13` 差集(基线用 `run-tests.sh --names-out` 采集,记入本特性目录)。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `[green: <contract>#<clause>]` | FR-015, FR-016, FR-020, US2 验收场景 1, contracts/green-point-claim.md, tasks 模板的形态说明 |
| `STR-002` | `ORDER BREAK: <ID> after <ID>` | FR-008, US1 验收场景 2, requirements 检查器的文档序检查输出 |
| `STR-003` | `0 error(s), 0 warning(s)` | FR-003, US1 验收场景 1, 人读输出的计数尾行形态 |
| `STR-004` | `not-evaluated` | FR-032, SC-008, US4 验收场景 2, run-checks 的短路项 verdict |
| `STR-005` | `run-checks` | FR-029, SC-007, goal-utils 的 action 名与 `--help` 行 |
| `STR-006` | `ok\|no-goal-definition\|dangling\|target-terminal\|cross-goal\|goal-terminal\|input-error` | FR-032, US4 验收场景 1, run-checks 的单项 verdict 词表(沿用既有,不新造) |
| `STR-007` | `0=ok / 4=blocked / 2=input-error / 3=unparsable` | FR-033, SC-007, run-checks 的退出码表 |
| `STR-008` | `Program-First discipline (shared/guidelines/token-efficiency.md)` | FR-002, 每个新检查器 docstring 的归属声明首句 |
| `STR-009` | `UNCOVERED:` | FR-024, SC-005, 未覆盖集每行的前缀 |
| `STR-010` | `SUBJECT EMPTY:` | FR-036, US5 Edge Case, 指代形导出空集合时的报错前缀 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
