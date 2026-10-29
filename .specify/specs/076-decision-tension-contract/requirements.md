# Requirements Specification: 决策反题与反指标契约（Decision Tension Record）

**Requirement Branch**: `076-decision-tension-contract`
**Created**: 2026-10-29
**Status**: Draft
**Input**: User description: "为计划阶段的承重决策引入可判定的反题契约（Decision Tension Record）：强制记录最强反题、双方不可让渡约束、判别性证据、预期反指标与重开条件；在计划模板中设 `## Decision Tensions` 章节，由 `/speckit.analyze` 增结构检测（缺 DTR / 六字段不全 / expected_sacrifice 无法映射 Measurement Sources → HIGH），ADR 的 Alternatives 引用 tension_id，按复杂度分级门控且确定性校验走既有 scripts/python/；并把改进流程 SI-3C 的证伪尝试升级为机器可读四元组（attempt / exit_code / observation / would_go_red_if），缺失或无法反空真即拒收。不新增命令、存储或运行时。"

## Related Feature *(mandatory)*

**Feature ID**: 076
**Feature Name**: 决策反题与反指标契约（Decision Tension Record）

**绑定结论**：绑定 **Feature 076**（`Draft`，2026-10-29 用户裁决立项）。**不**绑定任何既有 Feature。

**reuse-first 复核（宪法 VII）**：判据是「该 Feature 是否已**拥有**本特性要建立的能力」，而非「是否持有交付载体」。载体相同不构成归属先例——Feature 051 曾对「投递载体完全相同」的 032 / 040 作出各自成 Feature 的判定。

| 候选 Feature | 与 A（DTR）的关系 | 与 B（证伪四元组）的关系 | 裁决 |
|---|---|---|---|
| 009 Plan Command | 持有 `templates/plan-template.md` 这一交付载体，但不拥有「决策反题 / 反指标」的能力与判据 | 无关 | 载体 ≠ 归属 |
| 002 Analyze Command | 持有 `/speckit.analyze` 这一执行载体，既有检测通道只判一致性缺陷，不判「决策是否留下可判定的反面」 | 无关 | 载体 ≠ 归属 |
| 053 Machine-Decidable Artifact Propositions | 拥有「制品结构命题交程序判定」的方法论，不拥有 plan 决策记录这一对象 | 无关（四元组不是制品结构命题） | 方法论相邻，非同一能力 |
| 012 Review Command / 063 Review P1 Governance | 评审流程与 P1 治理，不拥有 plan 决策记录 | 不拥有 SI-3C | 无关 |
| 072 Client-Project Feedback & Self-Improvement | 无关 | 明确**复用** SI-0…SI-9 而不拥有其步骤定义（其 Key Changes 与 Implementation Notes 都把循环当作既有零件） | 消费 ≠ 归属 |
| 058 Unattended SDD Loop Driver | 无关 | 编排层运行效率，不拥有改进循环语义 | 无关 |

**结论与理由**：A 是计划层的新能力（六字段张力记录、可采纳判据、承重门槛、analyze 结构通道），现有 Feature 无 owner；B 是「批评和自我批评」机制的演化，其 owner 是 `shared/guidelines/critique-and-self-critique.md` 与 SI-3C，而该机制**未被任何既有 Feature 收编**——2026-10-29 全仓检索 `memory/features/*.md`，对该 owner 文件与 SI-3C 的引用只出现在 076 自身的立项文档中。因此不构成「必须绑既有 Feature 而非新建」的情形，绑定 076 成立。绑定时点偏离默认协议（默认推迟到 `/speckit.clarify`），见 § Assumptions A4。

## 现状锚点（2026-10-29 以仓库实测为准；dated record，仅作可行性输入，非运行时保证）

- `templates/plan-template.md` 无 `## Decision Tensions` 章节；唯一涉及替代方案的位置是 § Complexity Tracking 的 `Simpler Alternative Rejected Because` 列（第 157 行），且只在宪法违规时填写。
- `docs/decisions/template.md` 有 `## Alternatives` 段，无 `tension_id` 引用位；ADR 事后撰写，不参与任何门禁。
- `.specify/skills/internal/analyze-artifacts/references/detection-and-severity.md` 拥有检测通道与严重度表（既有 7 条通道，A–G），其中无「决策是否留下反题」的通道。
- `shared/guidelines/critique-and-self-critique.md` 的输出形态是「每个提案一条证伪尝试」加 verdict 记在提案已有载体，**无结果字段规格**——「跑过」与「声称跑过」在工件上不可区分；`shared/workflow/self-improvement-workflow.md` SI-3C 只留步骤摘要并指向该 owner。
- `shared/guidelines/` 下不存在 `decision-tension.md`。本特性拟引入的标识符（含 `decision-tension`、`Decision Tensions`、`tension_id`、`expected_sacrifice`、`binding_constraints`、`revision_trigger`、`would_go_red_if`）在框架面上零命中，仅出现在本 Feature 的立项与状态脊文件中（2026-10-29 全仓 grep），无保留标识符冲突。
- `scripts/python/` 已有 `validate-requirements.py`、`validate-tasks.py` 等确定性检查器先例（退出码 0/1/2、只读、标准库），结构校验沿用该目录与形态即可，无需新增运行时。
- `shared/guidelines/task-complexity-rubric.md` 已定义四档复杂度与「冲突取较高一级」的 tie-break，承重门槛与复杂度门控可直接引用它。

## Assumptions（对输入中开放点的缺省裁决，clarify 阶段可推翻）

- **A1（脚手架偏差 / scaffold deviation）**：规格目录与初始文件由项目脚手架 `create-new-requirements.sh` 产出，编号 `076` 与键 `076-decision-tension-contract` 均由脚本派生（未手写）。按阶段约束，本线 MUST NOT 切换或新建分支，故脚本的「创建并切换分支」动作被抑制：在仓库外目录调用该脚本，使其判定无 git 上下文而跳过分支动作（stderr 留痕 `skipped branch creation for 076-decision-tension-contract`）。编号与目录创建能力照用；工作分支保持 `076-decision-tension-contract` 不变。
- **A2（编号由 075 实改为 076 的原因）**：调研报告提出的候选编号是 075，但 `.specify/specs/075-sdd-loop-efficiency/` 已被 Feature 058 的演化 spec 占用（其 Related Feature 绑定 058）。按「编号 = 目录号、不复用」的既有规则顺延为 076。
- **A3（术语裁决）**：对外一律工程词——DTR、反题（antithesis）、反指标（落在 `expected_sacrifice`）、判别性证据（`discriminating_evidence`）、重开条件（`revision_trigger`）。以下五个词仅作**内部理解用别名**，允许出现的白名单只有三处——本节、本规格的术语注记、以及下句点名的 Feature 详情附录——其余位置 MUST NOT 出现，尤其 MUST NOT 进入任何用户可见正文或分发面：矛盾论、主要矛盾、矛盾的主要方面、对抗性矛盾、矛盾转化条件。别名与 DTR 字段的映射不复述，见 `.specify/memory/features/076.md` § 附「内部别名映射（仅供理解，不进用户界面）」；该文件是 Feature 详情，不在 `shared/`、`templates/`、`skills/` 三棵分发面内，因此不参与 SC-007 的零命中计数。
- **A4（特性绑定时点偏离）**：默认协议把 Feature 绑定推迟到 `/speckit.clarify`；本轮按调用方要求在本阶段给出绑定结论，已在 § Related Feature 完成。
- **A5（范围边界）**：本特性只建立规范 owner、模板落点、检测通道、引用关系与确定性校验；不建立回放评测集、效果统计、评分或成熟度报告——效果证据若日后需要，由既有证据层另行采集，本规格不新增载体。
- **A6（载体不变）**：DTR 搭在 plan 工件上；证伪四元组搭在提案已有载体（SI-4 派发载荷、SI-7 intervention 记录）上。两者都不新增存储。
- **A7（门槛判读）**：四类触发（不可逆 / 跨团队 / 高爆炸半径 / 与宪法原则相关）任一成立即承重；复杂度分级与承重判据冲突时，按 `task-complexity-rubric.md` 的 tie-break 取较高一级，并以承重判据为准。
- **A8（调用者是 agent）**：主要消费者是 agent 与维护者，因此所有新增判定 MUST 非交互可完成；人类交互路径保留，但不新增交互能力。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 承重决策留下可判定的反题、代价与重开条件 (Priority: P1)

计划作者写一个承重决策（不可逆、跨团队、高爆炸半径或触及宪法原则）时，不再只写「我们选 A」，而是在计划的 `## Decision Tensions` 章节写一条 `T-NNN` 记录：选了哪一极、最强反题是什么（一个能被独立采纳的具名方案，不是稻草人）、双方各自不可让渡的约束、什么可执行观测能判定哪一极更对、选这一极会让哪个**已声明的**指标变差、变差到什么程度必须重开。读者因此能在一次阅读里看到「没选另一条要付出什么」，而不是事后从 ADR 里猜。

**Why this priority**: 这是本特性唯一的新能力。没有它，analyze 的结构检测与 ADR 的引用都没有对象，B 的四元组也只是另一处孤立字段。

**Independent Test**: 准备一个含 1 条承重决策的计划夹具并按模板填写，运行确定性结构校验器得到退出码 0；随后逐个删字段、置空代价、写入不可判定措辞，校验器逐例变红。

**Acceptance Scenarios**:

1. **Given** 一个含 1 条承重决策的计划，**When** 按模板写 `## Decision Tensions`，**Then** 该章节含一条 `T-001` 记录，六字段齐备，且 `expected_sacrifice` 指向 requirements 中已声明的一条测量来源。
2. **Given** 同一条记录，**When** `expected_sacrifice` 被写成 `none` 或用「要平衡」一类措辞代替取舍，**Then** 校验器判该记录不成立并返回非零退出码，计划 MUST 修正后才能进入下一阶段。
3. **Given** 一个不含任何承重决策的 trivial 计划，**When** 写计划，**Then** 章节写 `N/A` 并逐条说明四类触发均不成立，校验器返回 0，且不产生任何张力记录。

---

### User Story 2 - 分析阶段拦住不成立的张力记录 (Priority: P1)

维护者运行 `/speckit.analyze`。除了既有的检测通道，它还从结构上检查三件事：计划含承重决策却没有张力记录章节（或写了 `N/A` 却没有逐条说明）、某条记录六字段不全（含只有单极的约束）、记录的预期代价指不到已声明的测量来源。三类都判 HIGH，必须回到计划修复并重过门。

**Why this priority**: 没有检测通道，DTR 就只是「建议写」；写了不成立也没人发现，新纪律会立刻退化为仪式。

**Independent Test**: 三个负向夹具各命中一类 HIGH，一个合规夹具三类各 0 条；判定只读报告里的严重度与条目计数。

**Acceptance Scenarios**:

1. **Given** 计划含承重决策但整份计划没有 `## Decision Tensions` 章节，**When** analyze 运行，**Then** 报 1 条 HIGH（缺张力记录），且不因「章节不存在」而跳过检测。
2. **Given** 一条记录缺 `revision_trigger`，或 `binding_constraints` 只有单极，**When** analyze 运行，**Then** 报 1 条 HIGH（六字段不全）。
3. **Given** 记录的 `expected_sacrifice` 指向一个 requirements 中不存在的测量来源，**When** analyze 运行，**Then** 报 1 条 HIGH（无法映射测量来源）。
4. **Given** 一个合规计划（记录齐备且代价可解析），**When** analyze 运行，**Then** 上述三类各 0 条，且既有通道的发现数与判据不变。

---

### User Story 3 - 证伪尝试必须真的跑过，而且能变红 (Priority: P1)

改进提案在派发前要带一条证伪尝试。现在它必须写成四元组：跑了什么（可重放的命令、grep、测试或测量）、退出码、原样观察（不是模型转述），以及「把哪个输入改坏，它必须变红」。缺任何一个字段，或写不出可执行的反空真条件，接收方直接拒收——不再接受「已执行」三个字。

**Why this priority**: 「没有外部信号的自我批评是负收益」是本特性唯一被正面证据支撑的硬约束；四元组是让「跑过」与「声称跑过」在工件上可区分的唯一手段。

**Independent Test**: 一个合规提案被接收；四种字段缺失与一种空真反空真条件的提案全部被拒收，判决由接收方输出而非人工判断。

**Acceptance Scenarios**:

1. **Given** 一个四字段齐备、`would_go_red_if` 以字面 `red:` 分隔两半（前半点名被改坏输入、后半点名具名红色信号）的提案，**When** 派发到 SI-4 接收方，**Then** 提案被接收，四元组记在提案已有载体上。
2. **Given** 同一提案缺 `observation`（或任一其他字段），**When** 派发，**Then** 接收方拒收，并给出「缺哪个字段」的判定。
3. **Given** `would_go_red_if` 只写「若实现有误就会失败」，**When** 派发，**Then** 接收方判为空真条件并拒收，MUST NOT 以附注形式放行。

---

### User Story 4 - 非承重决策不被仪式拖累 (Priority: P2)

改一行文档、修一个错别字、调一个措辞，这类 trivial 任务不触发张力记录。只有不可逆、跨团队、高爆炸半径或触及宪法原则的决策才要求写。门控因此可解释：不是「小改动就不查」，而是「小改动里没有承重决策」。

**Why this priority**: 若门控缺失，新纪律会变成一律填表，成本落在最不需要它的地方，最终被绕过。

**Independent Test**: trivial 夹具零记录、零 HIGH；在同一夹具补入一条不可逆决策并移除其合规 `N/A` 章节后复跑，必须出现 1 条 HIGH；再写入一条合规记录替换 `N/A` 后复跑，HIGH 归 0。

**Acceptance Scenarios**:

1. **Given** 一个 trivial 计划（四类触发均不成立），**When** 写计划并跑 analyze，**Then** 章节为 `N/A` 且逐条说明判据不成立，零记录、零 HIGH。
2. **Given** 同一夹具补入一条不可逆决策（回滚需要迁移）并**移除**该合规 `N/A` 章节，**When** 复跑 analyze，**Then** 恰出现 1 条 HIGH（缺张力记录），说明门控不是「没章节就不查」；**Given** 同一夹具改为写入一条合规 `### T-001` 记录以替换 `N/A`，**When** 再复跑，**Then** HIGH 归 0——「恰 1 条 HIGH」只在删章节这一步可达，补记录这一步证明的是修复路径，两个变体各自独立运行、不对同一次运行同时断言。
3. **Given** 一个被判为 trivial 却触及宪法 MUST 的改动，**When** 判定复杂度，**Then** 按 rubric 的 tie-break 取较高一级，并据此要求张力记录。

---

### User Story 5 - 计划、ADR 与测量来源互相可达 (Priority: P2)

事后写的 ADR 在 `## Alternatives` 段引用计划里的 `tension_id`，不复制内容；读者从 ADR 能回到张力记录，从张力记录的预期代价能回到 requirements 里已声明的测量来源。三处各自只是引用，任何一处改动都不需要同步改写另外两处。

**Why this priority**: 可追溯性；没有它，三处会各自漂移成第二定义点，正是本特性要防的形态。

**Independent Test**: 检查 ADR 模板含引用位；抽查夹具计划中每条记录的预期代价都能解析到一条已声明的测量来源。

**Acceptance Scenarios**:

1. **Given** 一个已写张力记录的计划，**When** 事后写 ADR，**Then** `## Alternatives` 段以 `tension_id` 指向该记录，且不复制其字段内容。
2. **Given** 一条 ADR 引用了一个计划中不存在的 `tension_id`，**When** 做结构检查，**Then** 判为断链并报错，不静默放过。

---

### Edge Cases

- **零承重决策**：章节写 `N/A` 并逐条说明四类触发不成立 → 零记录、零 HIGH；写 `N/A` 但不说明 → 判 HIGH（等同缺章节）。
- **重复或被跳号的记录标识**：计划内 `tension_id` 必须唯一且按出现顺序递增；重复、跳号或非 `T-NNN` 形态由确定性校验器判错。SC-001 的六个反向输入据此含重复、跳号与逐字段删除三类样本（前三者各一例，删除一类逐字段各一例）；非 `T-NNN` 形态由同一 `dtr-tension-id` 标签判错，不单列夹具。
- **预期代价指向不存在的测量来源**：判 HIGH；作者二选一——按澄清或范围变更补建测量来源，或把该决策降级为普通取舍并撤销记录。
- **反题是稻草人**：`antithesis` 写成「什么都不做」、被选方案的弱化版，或只有「但它更差」的陈述 → 不可采纳；两位复核者按同一判据必须得到同一 verdict。
- **双极约束可同时满足**：说明该张力不成立（属可求解冲突），MUST 改写为双赢解或降级，MUST NOT 保留为张力记录。
- **计划在后续阶段新增承重决策**（澄清或任务回环）：计划更新时必须补写记录；analyze 复跑必须仍能检出缺失，不得以「计划已通过一次门」为由跳过。
- **证伪尝试退出码为 0 但观察为空**：视为「跑了但没留下结果」，判不合格并拒收。
- **反空真条件写成条件句**（「如果实现错了就会失败」）：空真，拒收；`would_go_red_if` 必须点名具体输入与被改坏后必红的结果。
- **历史计划没有该章节**：判 HIGH 而非跳过；作者补写，或显式声明 `N/A` 并给出判据结论。范围见 FR-011：只判本轮 `REQUIREMENTS_DIR` 下的 `plan.md`，其他 spec 目录的历史计划不在检查范围、因而不产生发现。
- **术语越界**：分发面出现 A3 列出的内部别名 → 判用户可见面违规，MUST 改为工程词。

## Requirements *(mandatory)*

### Functional Requirements

#### A-1 规范 owner 与判据

- **FR-001**: MUST 新建规范 owner `shared/guidelines/decision-tension.md`，并在其开头声明它拥有什么：六字段 DTR 的输出形态、可采纳判据、拒绝形态、承重决策门槛、相邻 owner 边界、记录标识形态。所有消费者（计划模板、分析检测、ADR 模板、契约测试）MUST 以路径引用该文件，MUST NOT 复述其判据表、拒绝清单或门槛表。
- **FR-002**: DTR MUST 由封闭的六字段加一个记录标识构成，字段名逐字为 `decision`、`antithesis`、`binding_constraints`（含 `pole_a` 与 `pole_b` 两个极点）、`discriminating_evidence`、`expected_sacrifice`、`revision_trigger`；记录标识为 `tension_id`（[[STR-004]]），形态 `T-NNN`（三位数字，计划内唯一且按出现顺序递增）。字段集合封闭：新增、改名或删除 MUST 走 owner 修订，MUST NOT 在消费点就地扩展。
- **FR-003**: 可采纳判据 MUST 是封闭集且四条全满足：(a) `decision` 用一句话点名被选中的一极；(b) `antithesis` 是一个可被独立采纳的具名方案，不是被选方案的弱化版、也不是「什么都不做」，且给出至少一条「在什么条件下它更优」的陈述——只有「但它更差」的陈述判为稻草人；(c) 两个极点约束均非空，且被选方案不同时满足两极（能同时满足时该张力不成立）；(d) `discriminating_evidence` 是一位复核者可执行、结果二值的观测或实验。
- **FR-004**: 拒绝形态 MUST 是封闭清单，命中任一条即判该记录不成立：`expected_sacrifice: none`（[[STR-002]]）；任一极点为空；`discriminating_evidence` 不可执行或结果非二值；`antithesis` 为稻草人；正文以「要平衡」「综合考虑」「视情况而定」一类不可判定措辞代替取舍。清单条目新增 MUST 走 owner 修订。判定者 MUST 一并写明：机械可判的三项（`expected_sacrifice` 恰为 `none`、任一极点为空、命中不可判定措辞清单）由 FR-016 的校验器判定；语义两项（稻草人反题、证据不可执行或结果非二值）由**两位复核者按同一条判据**判定，两人 MUST 得到同一 verdict，分歧即判据待修订，不能两人各自成立。
- **FR-005**: 承重决策门槛 MUST 为四类触发，任一成立即承重：不可逆（回滚需要迁移或重建）、跨团队（改变他人依赖的契约或接口）、高爆炸半径（故障影响面超出本特性边界）、与宪法原则相关（触及任一 MUST 条）。不满足任一触发的决策 MUST NOT 被要求填写记录，缺失记录 MUST NOT 被判为缺陷。
- **FR-006**: 复杂度门控 MUST 引用 `shared/guidelines/task-complexity-rubric.md` 的分级，并声明 Trivial 级任务按定义不含承重决策、因此 MUST NOT 触发记录；当复杂度分级与承重判据冲突时，MUST 按该 rubric 的 tie-break 规则取较高一级，并以承重判据为准判定是否需要记录。
- **FR-007**: owner MUST 声明与四个相邻机制的分工，且各以路径引用不复述：`shared/definitions/derivation-definitions.md` § Contradiction Handling（管两个来源冲突时不取平均）、`/speckit.clarify` 与访谈账本（管需求阶段的分歧与翻供）、`shared/guidelines/fast-fail.md`（管执行中的异常纠正与裁定）、`shared/guidelines/critique-and-self-critique.md`（管改进提案的证伪）。张力记录 MUST 只承接「方向已选定之后的技术取舍」，MUST NOT 承接需求分歧。

#### A-2 计划模板落点

- **FR-008**: `templates/plan-template.md` MUST 新增 `## Decision Tensions`（[[STR-001]]）章节，位置 MUST 是本模板 `##` 级标题序列中 `## Constitution Check` 的**直接后继**，因而也是 `## Project Structure` 的直接前驱。本条是该章节的唯一锚点：原措辞「在 `## Constitution Check` 之后、`## Complexity Tracking` 之前」有两个满足位（紧跟门，或插在 `## Project Structure` 之后），不构成可判定的位置约束。判定方式 MUST 是标题序列检查——抽取全部 `^## ` 行，断言 `## Constitution Check` → `## Decision Tensions` → `## Project Structure` 三者相邻；模板侧由契约测试断言（FR-009），计划实例侧由 FR-016 校验器的 `dtr-anchor` 断言。当计划含至少一条承重决策时该章节必填，每条记录以 `T-NNN` 起头的子节承载；当且仅当无承重决策时，章节 MUST 写 `N/A` 并逐条说明四类触发均不成立，MUST NOT 删除章节或留空。
- **FR-009**: 该章节 MUST 只引用 owner 的字段名与判据（一条指针加字段清单），MUST NOT 复制 owner 的可采纳判据表、拒绝清单或承重门槛表；MUST 由契约测试守卫四件事：章节存在、章节位置（按 FR-008 的标题序列相邻性断言）、指针路径可解析、判据表未被逐行复制。
- **FR-010**: 每条记录的 `expected_sacrifice` MUST 映射到同一特性 `requirements.md` 的 `### Measurement Sources & Collection Methods` 中已声明的一条测量来源（写明测量来源标识与变差方向，可附阈值）。引用形态 MUST 是封闭形式 `<SC-NNN> Source <↓|↑>`：以 `SC-NNN` 标识、空格、字面 `Source` 起头，随后是必填的变差方向记号（`↓` 或 `↑`），其后的阈值或说明自由。`SC-NNN` MUST 解析到该节中以 `**SC-NNN Source**` 起头的条目；一条记录 MUST 只解析到一条来源，值中出现第二个 `SC-NNN` 判解析失败。无该前缀、标识解析不到条目、方向记号缺失或不在 `↓`/`↑` 两值内，一律判「无法解析」并由校验器返回错误（FR-016），MUST NOT 回落为人工阅读判定。无法映射时 MUST 二选一并在计划中留痕：按澄清或范围变更路径补建测量来源，或把该决策降级为普通取舍并撤销该记录。方向记号 MUST 只作**记录性断言**：程序判它落在 `↓`/`↑` 两值内即通过，MUST NOT 断言该方向与所引来源指标的实际语义一致（那是复核者判断）；因此值里不要求写指标名，本特性也不新增方向校验或指标绑定。

#### A-3 分析检测

- **FR-011**: `/speckit.analyze` MUST 新增一个结构通道，判定三类缺陷并各判 HIGH：(a) 计划缺 [[STR-001]] 章节，或该章节写 `N/A` 却未逐条说明四类触发均不成立——两者都按「缺记录」判 HIGH（fail-closed），检测器 MUST NOT 被要求自行判断计划里是否存在承重决策；(b) 任一记录六字段缺失或为空，含 `binding_constraints` 只有单极；(c) `expected_sacrifice` 无法解析到 requirements 中已声明的测量来源。检查范围的被判定对象 MUST 只有一份工件：本轮经前置脚本解析出的 `REQUIREMENTS_DIR` 下的 `plan.md`（该目录内的 `requirements.md` 只是映射比对的参照，不是第二个被判定对象）；其他特性目录下的 `plan.md` MUST NOT 被本通道打开（全仓遍历会把实测 68 份历史计划一次性判 HIGH，且需新增扫描面，违 FR-018）。范围之内的历史计划（契约生效前写下的 `plan.md`）MUST NOT 豁免：缺章节或 `N/A` 未逐条说明照判 HIGH，修复动作是补章节。requirements 无 `### Measurement Sources & Collection Methods` 时按记录数机械分叉：计划含 ≥1 条记录 → 每条 `expected_sacrifice` 解析失败 → 按 (c) 判 HIGH；合规 `N/A`（零记录）→ 映射判定不执行 → 0 条发现。该通道 MUST NOT 设 advisory 或降级档：三类缺陷的取值只有 HIGH 与 0。
- **FR-012**: 该通道的严重度 MUST 采用既有传播面判据（`.specify/shared/workflow/objective-analysis-gate.md`），MUST NOT 新造严重度等级、评分或成熟度结论；每条发现 MUST 写明其传播面（计划 → 任务 / 实现）。
- **FR-013**: 结构判定 MUST 是确定性的（字段存在性、枚举取值、引用解析），MUST NOT 交给模型按语义打分；可机械判定的部分 MUST 由既有 `scripts/python/` 下的程序执行并输出 verdict，模型只消费 verdict。
- **FR-014**: 该通道 MUST 落在 `detection-and-severity.md`（检测通道与严重度的 owner）内并与既有通道并列；对既有内容采用**只增不改**的包含性声明（判据 owner：`shared/guidelines/closed-set-claims.md`）：基线参照物为本特性基线提交 `ac63fe8c` 处的该文件，比较单元为「既有段落 / 新增段落」两类，允许差异集为「本特性新增的通道小节 + 因新增通道而更新的计数行」，集合之内 MUST 通过结构不变量（通道编号唯一、严重度取值落在既有四值域内），集合之外 MUST 与基线逐字节一致（删除或改写行数为 0）；实际差异行 MUST 由契约测试枚举并与声明的允许差异集比对（漂移守卫）。

#### A-4 ADR 引用

- **FR-015**: `docs/decisions/template.md` 的 `## Alternatives` 段 MUST 增加一个 `tension_id`（[[STR-004]]）引用位，以 `T-NNN` 指向同一特性计划中的记录，MUST NOT 复制记录字段内容；引用 MUST 可解析，指向不存在的记录 MUST 判为断链错误。当该决策无张力记录时，MUST 显式写明「无承重张力记录」及判定结论。断链检查的**调用面** MUST 明写：唯一调用面是契约测试 `tests/contract/test_decision_tension_contract.py` 的断链夹具对（一份计划 + 一份含不可解析 `tension_id` 的 ADR 片段），它导入 FR-016 校验器导出的记录索引函数作库调用；本特性 MUST NOT 新增命令，analyze 通道也 MUST NOT 扫描 `docs/decisions/`（那会新增扫描面，违 FR-018）。

#### A-5 确定性校验与机制边界

- **FR-016**: 结构校验 MUST 由 `scripts/python/validate-decision-tensions.py` 执行（既有 `scripts/python/` 下的确定性程序：只用标准库、无第三方依赖、无常驻进程、只读）。调用契约 MUST 是 `python3 scripts/python/validate-decision-tensions.py --spec <spec-dir> [--json]`，读取 `<spec-dir>/plan.md` 与 `<spec-dir>/requirements.md`；选目录而非文件，是因为判定需跨两份工件解析测量来源（单文件位置参数读不到 requirements）。退出码语义 MUST 与既有检查器一致：0 无错误（允许 warning）、1 发现错误、2 输入不可读（任一文件缺失、不可解码或无内容行）。输出 MUST 沿用 `validate-requirements.py` 形态：默认人读（`status` 行 + 每个检查一行 `[label] pass|fail (count)` + findings），`--json` 输出 `{"spec","status","checks":[{"label","status","count"}],"errors","warnings","scanned"}`。检查标签 MUST 是封闭六项，覆盖 FR-008 的锚点断言、FR-011 的三类缺陷与两个记录级形态（记录标识、拒绝形态）——是「四条判据 + 两个记录级形态」的划分，MUST NOT 表述为与四件事的「一一对应」：`dtr-anchor`、`dtr-section-missing`、`dtr-record-incomplete`（六字段齐备、双极非空）、`dtr-tension-id`（唯一、按序、`T-NNN` 形态）、`dtr-rejected-form`（拒绝形态命中，含 [[STR-002]] 与不可判定措辞清单）、`expected-sacrifice-unmapped`（按 FR-010 解析）。同一记录同一标签 MUST 只报一条；跨标签优先级 MUST 明写两条：① 章节缺失 → 只报 `dtr-section-missing`，抑制 `dtr-anchor`（三行相邻断言在章节不存在时必然同红，同一根因不得计两次，否则「缺章节 1 条 HIGH」与退出码计数都会翻倍）；② `expected_sacrifice` 恰为 `none` 时只报 `dtr-rejected-form`，不再叠加 `expected-sacrifice-unmapped`。校验器 MUST 只输出 verdict，MUST NOT 提议改写。
- **FR-017**: 该校验器 MUST 拥有逆样本（快速失败纪律对机器给出的绿同样成立）：删去任一字段（六字段逐一各一例）、置空预期代价、写入不可判定措辞、重复 `tension_id`、`tension_id` 跳号、指向不存在的测量来源——每一例 MUST 在契约测试中产生一次红运行记录；逆样本 MUST NOT 只写在文档描述里。
- **FR-018**: 本特性 MUST NOT 新增 `/speckit.*` 命令、存储、台账、调度器、评分器或模型调用；张力记录搭在计划工件上，判定结果只进既有 analyze 报告与计划文本。

#### B-1 证伪四元组（SI-3C）

- **FR-019**: `shared/guidelines/critique-and-self-critique.md` 的输出形态 MUST 由「一句话加 verdict」升级为封闭四元组：`attempt`、`exit_code`、`observation`、`would_go_red_if`（[[STR-003]]）；四元组 MUST 在派发前产生，字段集合封闭，扩展 MUST 走 owner 修订。
- **FR-020**: 四元组各字段 MUST 有可判定语义：`attempt` 是一位复核者可原样重放的命令、grep、测试或测量；`exit_code` 是整数；`observation` 是原样输出摘要（模型转述判为不合格）；[[STR-003]] 点名「把哪个输入改坏，该尝试必须变红」的具体输入与预期红色结果。`attempt` 的「可重放」是**复核者规则**而不是程序判决：程序只判该字段非空，重放与可重放性归 SI-6 与复核者，封闭拒收原因集因此不含 `attempt-not-replayable`。
- **FR-021**: 拒收规则：四元组任一字段缺失或为空、`observation` 为转述、或 [[STR-003]] 给不出可执行的反空真条件（例如只写「若实现有误就会失败」）时，SI-4 接收方 MUST 拒收该提案；拒收 MUST NOT 折算为「未达成」，MUST NOT 静默接受，也 MUST NOT 以「已执行」字样通过。判定者 MUST 是确定性程序 `scripts/python/validate-falsification-quartet.py` 而不是接收方 agent 的判断：调用契约 `python3 scripts/python/validate-falsification-quartet.py <payload.md> [--json]`，退出码 0 接收 / 1 拒收 / 2 载荷不可读（按拒收处置，原因 `input-unreadable`）。四元组在派发载荷中的形态 MUST 是四个字面键 `attempt:`、`exit_code:`、`observation:`、`would_go_red_if:` 各出现一次（值取键后同行或缩进续行）；`exit_code` MUST 是整数（0 合法）；`observation` MUST 以字面 `raw:` 起头承载原样摘录——这是「非转述」的机械代理，无该标记即判 `observation-not-raw`；[[STR-003]] MUST 同时给出被改坏的具名输入与具名红色信号，两半都 MUST 有机械形状（与 `raw:` 同类：只判形状，不判语义）：**输入半** MUST 是一个反引号跨度，且出现在字面标记 `red:` 之前；**信号半** MUST 是 `red:` 之后至少一个反引号跨度，点名断言名、检查标签或非零退出码之一。缺 `red:` 标记、`red:` 之前无反引号跨度、`red:` 之后无反引号跨度，任一成立即判 `tautology`。该形状管不到「输入真被改坏后是否真会变红」，与「`raw:` 可被伪造」同属已披露限制，由复核者发现、只记非阻断注记、不进判决（owner 的记录点见 T014）。拒收原因 MUST 取自封闭集 `missing-field` / `empty-field` / `exit-code-not-integer` / `observation-not-raw` / `tautology` / `input-unreadable`，并具名指出缺哪个字段或哪半条件。接收方 agent MUST NOT 反向覆盖判决：不得接收脚本退出码非 0 的载荷，MUST NOT 在封闭原因集之外另立拒收理由，额外疑虑只能写成非阻断注记。脚本 MUST NOT 重放 `attempt`，也 MUST NOT 判它「可否重放」——可重放性是复核者规则（SI-6 与复核者按原样执行一次），故封闭原因集不设 `attempt-not-replayable`；重放本身已是既有流程，不引入执行运行时。
- **FR-022**: 载体 MUST 不变：四元组记在提案已有载体（SI-4 派发载荷、SI-7 intervention 记录），MUST NOT 新建台账、存储、probe 或评分。
- **FR-023**: `shared/workflow/self-improvement-workflow.md` 的 SI-3C MUST 只保留步骤摘要与指向 owner 的指针，MUST NOT 复述四元组字段清单或拒收规则；契约测试 MUST 断言「owner 有字段定义」且「workflow 无第二份定义」。

#### C-1 术语与分发

- **FR-024**: 用户可见正文 MUST 只用工程词（DTR、反题、反指标、判别性证据、重开条件）；§ Assumptions A3 列为内部别名的术语 MUST NOT 出现在任何分发面的用户可见文本中（`shared/`、`templates/`、`skills/`）。白名单与 A3 逐处对齐（同一份清单，见 A3）：本规格的 Assumptions A3、owner 的术语注记、以及 A3 点名的 `.specify/memory/features/076.md` § 附「内部别名映射」；最后者是 Feature 详情、不在三棵分发面内，因此不参与 SC-007 的零命中计数，也未在三棵树上开第二个例外。
- **FR-025**: 两顶帽子：唯一编辑面 MUST 是框架源（`shared/`、`templates/`、`skills/internal/analyze-artifacts/`、`scripts/python/`、`docs/decisions/`）；`.specify/` 运行时副本与各工具命令副本 MUST 经既有同步或再生成机制产出，MUST NOT 手改；计划 MUST 列出本次触及的镜像对，并以「相对改动前测量无新增漂移」为判定方式。

**镜像对清单（clarify 阶段钉死；plan 阶段 MUST 原样引用，实现中若发现新增受影响面 MUST 先在本表补行，MUST NOT 静默扩面）**

| # | 框架源（唯一编辑面） | `.specify/` 运行时副本 / 工具副本 | 产出机制 |
|---|---|---|---|
| 1 | `shared/guidelines/decision-tension.md`（新建） | `.specify/shared/guidelines/decision-tension.md` | `sync-mirrors.py`（shared 对） |
| 2 | `shared/guidelines/critique-and-self-critique.md`（改写） | `.specify/shared/guidelines/critique-and-self-critique.md` | 同上 |
| 3 | `shared/workflow/self-improvement-workflow.md`（改写） | `.specify/shared/workflow/self-improvement-workflow.md` | 同上 |
| 4 | `templates/plan-template.md`（改写） | `.specify/templates/plan-template.md` | `sync-mirrors.py`（templates 对；本文件不在被排除的 `commands/` 子树内，故无工具命令副本） |
| 5 | `skills/internal/analyze-artifacts/`（改写 `references/detection-and-severity.md`，若 `SKILL.md` 亦需指针则同对） | `.specify/skills/internal/analyze-artifacts/` 下同名文件 | `sync-mirrors.py`（skills/internal 对） |
| 6 | `scripts/python/validate-decision-tensions.py`（新建） | `.specify/scripts/python/validate-decision-tensions.py` | `sync-mirrors.py`（scripts 对） |
| 7 | `scripts/python/validate-falsification-quartet.py`（新建） | `.specify/scripts/python/validate-falsification-quartet.py` | 同上 |

- **工具命令副本面**：本次 MUST NOT 触及 `templates/commands/**`，因此 `regen-command-copies.py` 的 per-tool 副本集合为空（无新增或修改的命令副本）；若实现阶段确需改命令模板，MUST 先把受影响副本补进本表再改。
- **无镜像面**：`docs/decisions/template.md`（`docs/` 不在 `MIRROR_PAIRS`）与 `tests/**` 契约测试（不入镜像），这两处只做源文件改动。
- **漂移基线（2026-10-29 clarify 阶段实测，dated record）**：`python3 scripts/python/sync-mirrors.py --check` 退出码 0，六对镜像均 `ok`（templates 22 / skills/external 406 / skills/internal 136 / agents 3 / scripts 115 / shared 59 文件）。判定 MUST 是实现后再跑同一命令并与该基线比对：本表所列对 MUST 无新增漂移；MUST NOT 以「命令退出码 0」单独作判据——它同样会被无关面的既有漂移拉红。
- **FR-026**: 既有闭合面 MUST 不回退，按包含性声明（判据 owner：`shared/guidelines/closed-set-claims.md`）表述：基线参照物为基线提交 `ac63fe8c`，比较单元为 `critique-and-self-critique.md` 与 `detection-and-severity.md` 两个文件按段落；允许差异集仅为本特性新增的段落，集合之外 MUST 与基线逐字节一致（删除或改写行数为 0），集合之内 MUST 通过结构不变量（拒绝形态、边界声明、消费者清单、严重度四值域保持可解析）；条目级断言（拒绝形态条数、边界声明条数、消费者清单行数）MUST 不小于基线，由契约测试给出基线与当前的计数比较。

### 显式排除项（Out of Scope）

以下项**不在**本特性范围，且 MUST NOT 以「顺带实现」形式进入：

1. **张力排序算子**（多条记录并存时选出唯一主要张力）——须在记录落地并有回放证据后另立特性。
2. **对抗角色异质性契约**（提案者 ≠ 合成者、批评者异源、先独立后交换）——属团队定义层，本特性不引入。
3. **任何哲学 SOP 技能**（把 A3 的别名概念做成独立技能或命令）。
4. **任何新 `/speckit.*` 命令**。
5. **任何新存储、台账、运行时、调度器或常驻进程**。
6. **任何 LLM 评分器、成熟度报告或效果评分机制**。

### Key Entities *(include if requirement involves data)*

- **决策张力记录（DTR）**：一条承重决策的可判定记录，六字段加一个 `tension_id`；生命周期为「写作 → 结构校验 → 分析检测 → 事后被 ADR 引用」，不新增持久化载体。
- **承重决策**：按四类触发（不可逆 / 跨团队 / 高爆炸半径 / 与宪法原则相关）判定；门槛既是记录的触发条件，也是「不写不算缺陷」的边界。
- **证伪尝试（四元组）**：`attempt` / `exit_code` / `observation` / `would_go_red_if`；载体是提案已有的派发载荷与干预记录。
- **测量来源绑定**：`expected_sacrifice` 与 requirements 中 `### Measurement Sources & Collection Methods` 条目的引用关系；它是「预期代价可测量」的唯一落点。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 在含 1 条承重决策的夹具计划上，[[STR-001]] 章节存在、该记录六字段齐备且 `tension_id` 唯一按序，确定性校验器返回 0；六个反向输入（删去任一字段——六字段逐一各跑一次、置 `expected_sacrifice: none`（[[STR-002]]）、写入不可判定措辞、重复 `tension_id`、`tension_id` 跳号、`expected_sacrifice` 指向不存在的测量来源）各返回 1。判定只读退出码与报告条目，不依赖人工阅读记录正文。
- **SC-002**: analyze 结构通道对三类缺陷各报 1 条 HIGH（缺记录、六字段不全、代价无法映射），对合规计划三类各 0 条，对「章节缺失」的计划报 HIGH 而非跳过；四类夹具各运行一次即可判定。
- **SC-003**: trivial 夹具（无承重决策、`N/A` 且逐条说明判据不成立）零记录、零 HIGH；同一夹具补入一条不可逆决策（回滚需要迁移）并**移除**其合规 `N/A` 章节后复跑，恰出现 1 条 HIGH（章节缺失）；再写入一条合规 `T-001` 记录替换 `N/A` 后复跑，HIGH 归 0。HIGH 计数与记录数即可判定，不需要阅读报告正文。
- **SC-004**: 合规提案（四字段齐备、`observation` 带 `raw:`、`would_go_red_if` 两半具名）被接收；封闭六拒收原因码各有一例（`missing-field` / `empty-field` / `exit-code-not-integer` / `observation-not-raw` / `tautology` / `input-unreadable`）全部被拒收，拒收率 6/6，每条拒收都具名给出缺失字段、失败的那半条件或原因码；四字段各缺一的四例只作 `missing-field` 的**附加**样本（同一原因码，不参与 6/6 计数）。共十一次运行，退出码 0/1/2 三值均被覆盖。
- **SC-005**: 零新增机制：`/speckit.*` 命令清单与基线提交 `ac63fe8c` 处的清单逐字相同（允许差异集为空）；新增常驻进程、服务、调度器、评分器数量为 0；新增第三方依赖为 0；新增校验程序只用标准库。判定以命令清单、依赖清单与进程清单的前后差异完成，差异必须落在空集内。
- **SC-006**: ADR 可追溯：`docs/decisions/template.md` 的 `## Alternatives` 段含 `tension_id` 引用位；夹具计划中每条记录的预期代价都解析到一条已声明的测量来源，解析失败数为 0；指向不存在记录的引用被判为断链错误（判定在契约测试的调用面执行，不在 analyze 通道内扫描 `docs/decisions/`）。
- **SC-007**: 术语合规：在 `shared/`、`templates/`、`skills/` 三棵分发面的用户可见文本中，§ Assumptions A3 列出的内部别名出现次数为 0；改动前后各测一次，计数相同。
- **SC-008**: 既有闭合面不回退：以基线提交 `ac63fe8c` 为参照物，`detection-and-severity.md` 与 `critique-and-self-critique.md` 的实际差异行全部落在声明的允许差异集内（新增段落与新增通道引起的计数行），集合外的删除或改写行数为 0，集合内结构不变量通过；拒绝形态、边界声明、消费者清单的条目数不小于基线。判定由差异行枚举与契约测试计数给出，不靠阅读文件判断。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 夹具计划文件与结构校验器的退出码、报告条目；十二次运行（1 合规 + 删除一类按六字段逐一各一次 + 其余五个反向输入各一次）的完整输出按「执行时全量捕获」纪律归档到本特性证据目录。
- **SC-002 Source**: analyze 报告中的严重度列与条目计数；四类夹具各一次运行的报告快照。
- **SC-003 Source**: 同一 trivial 夹具三次 analyze 报告的 HIGH 计数（合规 `N/A` → 0；补入不可逆决策并移除 `N/A` → 1；写入合规记录替换 `N/A` → 0），与计划中的记录条数；三次运行各留一份报告快照。
- **SC-004 Source**: 接收方的接收 / 拒收判决输出；十一次运行（1 合规 + 6 个原因码各一例 + 4 个附加 `missing-field` 样本），判定只读退出码与判决里的原因码。
- **SC-005 Source**: `/speckit.*` 命令清单（命令模板目录与各工具副本目录的并集）、依赖清单与进程清单在基线提交 `ac63fe8c` 与实现后的两次采集差异；单次比较即可判定。
- **SC-006 Source**: `docs/decisions/template.md` 的文本断言结果、记录到测量来源的解析结果（解析器输出），以及断链夹具对的契约测试输出——它是断链判定的唯一调用面。
- **SC-007 Source**: 三棵分发面的术语 grep 计数，改动前后各一次。
- **SC-008 Source**: 两个 owner 文件与基线提交的逐字 diff，以及契约测试的断言计数。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "## Decision Tensions" | FR-008, FR-011, SC-001 |
| `STR-002` | "expected_sacrifice: none" | FR-004, FR-016, SC-001 |
| `STR-003` | "would_go_red_if" | FR-019, FR-020, FR-021 |
| `STR-004` | "tension_id" | FR-002, FR-015 |

**Citation convention（作用域：仅本文件）**: 本文件内的 FR / SC / Clarifications 引用上表字面量时写 `[[STR-NNN]]`，不复制字面量；`validate-requirements.py` 的 `ref-resolvable` 因此可双向核对（引用未定义即错，定义后无人引用即 warning）。契约与任务文件**不套用**本约定——它们是字面量的消费点，必须逐字书写（`## Decision Tensions`、`expected_sacrifice: none`、`would_go_red_if`、`tension_id`）；把它们改写为 id 会让被消费的字符串在实现期无人可核对。

## Clarifications

### Session 2026-10-29

- 本轮无活动 `[NEEDS CLARIFICATION]` 标记；三处原可发问的开放点按缺省裁决记录，未进入问题队列：编号顺延（A2）、内部别名的对外边界（A3）、载体选择（A6）。
- 特性绑定在本阶段给出而非推迟到 `/speckit.clarify`（A4）；绑定结论与候选核验表见 § Related Feature。
- 显式排除项以 § Requirements 的「显式排除项（Out of Scope）」为准，不在 clarify 阶段重新开启。

### Session 2026-10-29（clarify round 1 · 无人值守）

> 运行模式 A（post-requirements，目标 `requirements.md`；spec 目录内尚无 `plan.md`，模式判定未偏离）。本轮**无用户在环**：六处已知欠指定点由执行代理按项目宪法、仓库实测与规格既有判据自行裁决，每条记录候选读法、代价与被否决理由，供 plan 阶段复核。扫描方式为同作者直读——本阶段无独立子代理派发能力，按 `.specify/shared/workflow/objective-analysis-gate.md` § 7 回退，逐条标注 `(detected: direct read, subagent unavailable)`。未新增或删除 FR / SC / Shared String（仍 26 FR / 8 SC / 4 STR），故 `checklists/requirements.md` 的派生计数无需回改；该清单里 `scanned 255 lines` 是 requirements 阶段那次运行的 `dated record`（指向 `test-evidence/validate-requirements.txt`），本阶段编辑面限本文件、未重盖该戳，因 FR / SC / STR 计数未变而不存在过期派生计数。文中钉入的实测数字（68 份在册计划、镜像文件计数）为本轮 `dated record`，供判定参照，不是长期事实声明。§ Requirements 的「显式排除项」未被重新开启。

- **Q1（模板锚点）→ A：唯一锚点是 `## Constitution Check` 的直接后继。** 实测 `templates/plan-template.md` 的 `##` 级标题序为 Constitution Check → Project Structure（含 Mirror Obligations）→ Complexity Tracking → Phase 1，故原措辞「Constitution Check 之后、Complexity Tracking 之前」有两个满足位（紧跟门，或插在 Project Structure 之后），不可机械判定。取前者：决策记录紧贴它所辩护的门，读者在门与结构方案之间就看见取舍；插在结构方案之后会把「方向取舍」读成「目录布局的注脚」。判定方式是标题序列检查——抽 `^## ` 行，断言 `## Constitution Check` → `## Decision Tensions` → `## Project Structure` 三者相邻；模板侧由契约测试断言，计划实例侧由校验器 `dtr-anchor` 断言。（FR-008、FR-009）`(detected: direct read, subagent unavailable)`

- **Q2（analyze 的适用范围）→ A：只判本轮 spec 目录下的 `plan.md`；范围外的历史计划零发现，范围内不设豁免，缺 Measurement Sources 由记录数机械分叉。** 依据是代码事实（宪法 VIII）：`/speckit.analyze` 的上下文来自 `check-prerequisites.sh` 解析出的 `REQUIREMENTS_DIR`，只加载该目录的 artifacts；在册 `plan.md` 实测 68 份，全仓遍历会一次性把历史特性判成 HIGH，且需新增扫描面（违 FR-018 与宪法 IX）。因此「历史计划一律 HIGH」只在范围内成立：本特性在契约生效前写下的 `plan.md` 缺章节照判 HIGH，修复动作是补章节，不是降级。`requirements.md` 无 `### Measurement Sources & Collection Methods` 时不设 advisory 中间态——计划有 ≥1 条记录则每条解析失败判 HIGH；合规 `N/A`（零记录）则映射判定不执行、0 条发现。被否决读法与代价：给历史计划加 provenance 豁免标记（等于新增逐计划状态位，违 IX）；按 git 首次提交判新旧（rebase 与浅克隆下不可复现）。（FR-011、Edge Cases）`(detected: direct read, subagent unavailable)`

- **Q3（校验器契约）→ A：`scripts/python/validate-decision-tensions.py`，入参是 spec 目录，退出码 0/1/2，人读默认 + `--json`。** 契约钉死为 `python3 scripts/python/validate-decision-tensions.py --spec <spec-dir> [--json]`，读 `<spec-dir>/plan.md` 与 `<spec-dir>/requirements.md`（缺任一或不可解析 → 2）。选目录而非文件：判定要跨两份工件解析测量来源，同仓 `account-clause-coverage.py --spec <spec-dir>` 已是这一形态；`validate-requirements.py` 的单文件位置参数在此读不到 requirements，故不照搬。输出沿用既有检查器：人读模式给 `status` 行、每检查一行 `[label] pass|fail (count)` 与 findings；`--json` 给 `{"spec","status","checks":[{"label","status","count"}],"errors","warnings","scanned"}`。检查标签是封闭六项，覆盖锚点断言、三条 HIGH 与两个记录级形态（不是与三条 HIGH 的「一一对应」）：`dtr-anchor` / `dtr-section-missing` / `dtr-record-incomplete` / `dtr-tension-id` / `dtr-rejected-form` / `expected-sacrifice-unmapped`；同记录同标签只报一条；跨标签优先级两条——章节缺失时只报 `dtr-section-missing` 并抑制 `dtr-anchor`（同一根因不计两次），`expected_sacrifice` 恰为 `none` 时只报 `dtr-rejected-form`，从而避免 SC-001 的反向夹具出现双计数。被否决读法：复用 `validate-tasks.py` 加子命令（把两种工件语义塞进一个入口，退出码与输出形态都会分叉）。（FR-013、FR-016）`(detected: direct read, subagent unavailable)`

- **Q4（`expected_sacrifice` 的映射规则）→ A：封闭引用形态 `<SC-NNN> Source <↓|↑>`，解析失败即判「无法映射」，不回落人工阅读。** 选字面 `Source` 作连接词，是因为 `### Measurement Sources & Collection Methods` 的条目本来就以 `**SC-NNN Source**` 起头，它是唯一可直接对上的连接键；只写 `SC-NNN` 会与同名 Success Criterion 共用一个命名空间，无法区分「引用判据」与「引用它的测量来源」。方向记号取封闭两值 `↓`/`↑`（指标的变差方向），使 FR-010 要求的「变差方向」有一个必填位：机器只判它落在两值内，**不断言**该方向与所引来源指标的实际语义一致——那是记录性断言，由复核者读；阈值与说明放在记号之后自由书写，不参与解析。一条记录只绑定一条来源，值里出现第二个 `SC-NNN` 判解析失败——多条来源会让「代价」失去单值语义，也让 SC-001 的「一条记录一条来源」无法计数。代价：作者必须记住这个前缀形态；收益是映射失败变成退出码而非阅读判断。（FR-010、FR-016）`(detected: direct read, subagent unavailable)`

- **Q5（B 的拒收判定者）→ A：确定性脚本判决，接收方 agent 只消费判决、不得反向覆盖。** 若把拒收留给接收方 agent，同一载荷换一个模型或换一次运行就可能得到不同 verdict，「跑过 vs 声称跑过」重新退化为不可判定，SC-004 的 6/6 也无法复现。故裁决为脚本 `scripts/python/validate-falsification-quartet.py <payload.md> [--json]`（0 接收 / 1 拒收 / 2 载荷不可读按拒收处置），拒收原因取封闭集 `missing-field` / `empty-field` / `exit-code-not-integer` / `observation-not-raw` / `tautology` / `input-unreadable`。两处「语义判据」被换成可判定的形状判据，代价如实记录：① 「`observation` 是转述」——机器判不了语义，改为要求值以字面 `raw:` 起头承载原样摘录，无标记即拒，标记可被伪造（伪造由复核者发现，属非阻断注记，不进判决）；② 「反空真条件」——改为两项都有机械形状：[[STR-003]] 的**输入半**是一个位于字面 `red:` 之前的反引号跨度，**信号半**是 `red:` 之后至少一个反引号跨度（点名断言名 / 检查标签 / 非零退出码）；缺标记或缺任一半即判 `tautology`。它管不到「输入改坏了却不会变红」这层真实性（那属 SI-6 与复核者），与伪造 `raw:` 前缀同属已披露限制。同时钉死两件事：脚本 MUST NOT 重放 `attempt`（重放是复核者与 SI-6 的动作，脚本重放会引入执行运行时，宪法 IX），也 MUST NOT 判它「可否重放」（可重放性是复核者规则），因此封闭原因集不设 `attempt-not-replayable`。被否决读法：agent 判定 + 可复现判据清单（清单本身要执行语义比较，仍不可复现）；脚本判定但保留 agent 否决权（双向覆盖会让判决再次发散）。（FR-019、FR-020、FR-021）`(detected: direct read, subagent unavailable)`

- **Q6（两顶帽子与镜像面）→ A：FR-025 表所列镜像对（行数以该表为准）+ 两个无镜像面，工具命令副本面为空，漂移基线为零。** 清单落在 FR-025 的表里（唯一 owner，plan 阶段原样引用，新增面必须先补行）：`shared/` 三项（含新建 `decision-tension.md`）、`templates/plan-template.md`、`skills/internal/analyze-artifacts/`、`scripts/python/` 两个新脚本，各自经 `sync-mirrors.py` 落到对应 `.specify/` 副本；`docs/decisions/template.md` 与 `tests/**` 不在 `MIRROR_PAIRS`，无镜像。本次不触及 `templates/commands/**`，故 `regen-command-copies.py` 的 per-tool 副本集合为空——这一条必须写明，否则「镜像对清单」会被读成「只列了 `.specify/` 而漏了工具副本」。基线为本轮实测：`sync-mirrors.py --check` 退出码 0、六对均 `ok`，因此判定是「实现后再跑同一命令，相对该基线无新增漂移」，而不是「命令退出码 0」——后者会被无关面的既有漂移拉红，写成绝对判据即不可通过。（FR-025）`(detected: direct read, subagent unavailable)`
