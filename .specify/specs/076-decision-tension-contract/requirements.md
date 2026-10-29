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
- **A3（术语裁决）**：对外一律工程词——DTR、反题（antithesis）、反指标（落在 `expected_sacrifice`）、判别性证据（`discriminating_evidence`）、重开条件（`revision_trigger`）。以下五个词仅作**内部理解用别名**，允许出现在本节与本规格的术语注记中，MUST NOT 进入任何用户可见正文或分发面：矛盾论、主要矛盾、矛盾的主要方面、对抗性矛盾、矛盾转化条件。别名与 DTR 字段的映射不复述，见 `.specify/memory/features/076.md` § 附「内部别名映射（仅供理解，不进用户界面）」。
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

1. **Given** 一个四字段齐备、`would_go_red_if` 点名了可改坏输入与预期红色结果的提案，**When** 派发到 SI-4 接收方，**Then** 提案被接收，四元组记在提案已有载体上。
2. **Given** 同一提案缺 `observation`（或任一其他字段），**When** 派发，**Then** 接收方拒收，并给出「缺哪个字段」的判定。
3. **Given** `would_go_red_if` 只写「若实现有误就会失败」，**When** 派发，**Then** 接收方判为空真条件并拒收，MUST NOT 以附注形式放行。

---

### User Story 4 - 非承重决策不被仪式拖累 (Priority: P2)

改一行文档、修一个错别字、调一个措辞，这类 trivial 任务不触发张力记录。只有不可逆、跨团队、高爆炸半径或触及宪法原则的决策才要求写。门控因此可解释：不是「小改动就不查」，而是「小改动里没有承重决策」。

**Why this priority**: 若门控缺失，新纪律会变成一律填表，成本落在最不需要它的地方，最终被绕过。

**Independent Test**: trivial 夹具零记录、零 HIGH；在同一夹具补入一条不可逆决策后复跑，必须出现 HIGH。

**Acceptance Scenarios**:

1. **Given** 一个 trivial 计划（四类触发均不成立），**When** 写计划并跑 analyze，**Then** 章节为 `N/A` 且逐条说明判据不成立，零记录、零 HIGH。
2. **Given** 同一夹具追加一条不可逆决策（回滚需要迁移），**When** 复跑 analyze，**Then** 恰出现 1 条 HIGH（缺张力记录），说明门控不是「没章节就不查」。
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
- **重复或被跳号的记录标识**：计划内 `tension_id` 必须唯一且按出现顺序递增；重复、跳号或非 `T-NNN` 形态由确定性校验器判错。
- **预期代价指向不存在的测量来源**：判 HIGH；作者二选一——按澄清或范围变更补建测量来源，或把该决策降级为普通取舍并撤销记录。
- **反题是稻草人**：`antithesis` 写成「什么都不做」、被选方案的弱化版，或只有「但它更差」的陈述 → 不可采纳；两位复核者按同一判据必须得到同一 verdict。
- **双极约束可同时满足**：说明该张力不成立（属可求解冲突），MUST 改写为双赢解或降级，MUST NOT 保留为张力记录。
- **计划在后续阶段新增承重决策**（澄清或任务回环）：计划更新时必须补写记录；analyze 复跑必须仍能检出缺失，不得以「计划已通过一次门」为由跳过。
- **证伪尝试退出码为 0 但观察为空**：视为「跑了但没留下结果」，判不合格并拒收。
- **反空真条件写成条件句**（「如果实现错了就会失败」）：空真，拒收；`would_go_red_if` 必须点名具体输入与被改坏后必红的结果。
- **历史计划没有该章节**：判 HIGH 而非跳过；作者补写，或显式声明 `N/A` 并给出判据结论。
- **术语越界**：分发面出现 A3 列出的内部别名 → 判用户可见面违规，MUST 改为工程词。

## Requirements *(mandatory)*

### Functional Requirements

#### A-1 规范 owner 与判据

- **FR-001**: MUST 新建规范 owner `shared/guidelines/decision-tension.md`，并在其开头声明它拥有什么：六字段 DTR 的输出形态、可采纳判据、拒绝形态、承重决策门槛、相邻 owner 边界、记录标识形态。所有消费者（计划模板、分析检测、ADR 模板、契约测试）MUST 以路径引用该文件，MUST NOT 复述其判据表、拒绝清单或门槛表。
- **FR-002**: DTR MUST 由封闭的六字段加一个记录标识构成，字段名逐字为 `decision`、`antithesis`、`binding_constraints`（含 `pole_a` 与 `pole_b` 两个极点）、`discriminating_evidence`、`expected_sacrifice`、`revision_trigger`；记录标识为 `tension_id`（[[STR-004]]），形态 `T-NNN`（三位数字，计划内唯一且按出现顺序递增）。字段集合封闭：新增、改名或删除 MUST 走 owner 修订，MUST NOT 在消费点就地扩展。
- **FR-003**: 可采纳判据 MUST 是封闭集且四条全满足：(a) `decision` 用一句话点名被选中的一极；(b) `antithesis` 是一个可被独立采纳的具名方案，不是被选方案的弱化版、也不是「什么都不做」，且给出至少一条「在什么条件下它更优」的陈述——只有「但它更差」的陈述判为稻草人；(c) 两个极点约束均非空，且被选方案不同时满足两极（能同时满足时该张力不成立）；(d) `discriminating_evidence` 是一位复核者可执行、结果二值的观测或实验。
- **FR-004**: 拒绝形态 MUST 是封闭清单，命中任一条即判该记录不成立：`expected_sacrifice: none`（[[STR-002]]）；任一极点为空；`discriminating_evidence` 不可执行或结果非二值；`antithesis` 为稻草人；正文以「要平衡」「综合考虑」「视情况而定」一类不可判定措辞代替取舍。清单条目新增 MUST 走 owner 修订。
- **FR-005**: 承重决策门槛 MUST 为四类触发，任一成立即承重：不可逆（回滚需要迁移或重建）、跨团队（改变他人依赖的契约或接口）、高爆炸半径（故障影响面超出本特性边界）、与宪法原则相关（触及任一 MUST 条）。不满足任一触发的决策 MUST NOT 被要求填写记录，缺失记录 MUST NOT 被判为缺陷。
- **FR-006**: 复杂度门控 MUST 引用 `shared/guidelines/task-complexity-rubric.md` 的分级，并声明 Trivial 级任务按定义不含承重决策、因此 MUST NOT 触发记录；当复杂度分级与承重判据冲突时，MUST 按该 rubric 的 tie-break 规则取较高一级，并以承重判据为准判定是否需要记录。
- **FR-007**: owner MUST 声明与四个相邻机制的分工，且各以路径引用不复述：`shared/definitions/derivation-definitions.md` § Contradiction Handling（管两个来源冲突时不取平均）、`/speckit.clarify` 与访谈账本（管需求阶段的分歧与翻供）、`shared/guidelines/fast-fail.md`（管执行中的异常纠正与裁定）、`shared/guidelines/critique-and-self-critique.md`（管改进提案的证伪）。张力记录 MUST 只承接「方向已选定之后的技术取舍」，MUST NOT 承接需求分歧。

#### A-2 计划模板落点

- **FR-008**: `templates/plan-template.md` MUST 新增 `## Decision Tensions`（[[STR-001]]）章节，位置 MUST 在 `## Constitution Check` 之后、`## Complexity Tracking` 之前。当计划含至少一条承重决策时该章节必填，每条记录以 `T-NNN` 起头的子节承载；当且仅当无承重决策时，章节 MUST 写 `N/A` 并逐条说明四类触发均不成立，MUST NOT 删除章节或留空。
- **FR-009**: 该章节 MUST 只引用 owner 的字段名与判据（一条指针加字段清单），MUST NOT 复制 owner 的可采纳判据表、拒绝清单或承重门槛表；MUST 由契约测试守卫三件事：章节存在、指针路径可解析、判据表未被逐行复制。
- **FR-010**: 每条记录的 `expected_sacrifice` MUST 映射到同一特性 `requirements.md` 的 `### Measurement Sources & Collection Methods` 中已声明的一条测量来源（写明测量来源标识与变差方向，可附阈值）。无法映射时 MUST 二选一并在计划中留痕：按澄清或范围变更路径补建测量来源，或把该决策降级为普通取舍并撤销该记录。

#### A-3 分析检测

- **FR-011**: `/speckit.analyze` MUST 新增一个结构通道，判定三类缺陷并各判 HIGH：(a) 计划含承重决策但缺 [[STR-001]] 章节，或该章节写 `N/A` 却未逐条说明四类触发不成立；(b) 任一记录六字段缺失或为空，含 `binding_constraints` 只有单极；(c) `expected_sacrifice` 无法解析到 requirements 中已声明的测量来源。
- **FR-012**: 该通道的严重度 MUST 采用既有传播面判据（`.specify/shared/workflow/objective-analysis-gate.md`），MUST NOT 新造严重度等级、评分或成熟度结论；每条发现 MUST 写明其传播面（计划 → 任务 / 实现）。
- **FR-013**: 结构判定 MUST 是确定性的（字段存在性、枚举取值、引用解析），MUST NOT 交给模型按语义打分；可机械判定的部分 MUST 由既有 `scripts/python/` 下的程序执行并输出 verdict，模型只消费 verdict。
- **FR-014**: 该通道 MUST 落在 `detection-and-severity.md`（检测通道与严重度的 owner）内并与既有通道并列；对既有内容采用**只增不改**的包含性声明（判据 owner：`shared/guidelines/closed-set-claims.md`）：基线参照物为本特性基线提交 `ac63fe8c` 处的该文件，比较单元为「既有段落 / 新增段落」两类，允许差异集为「本特性新增的通道小节 + 因新增通道而更新的计数行」，集合之内 MUST 通过结构不变量（通道编号唯一、严重度取值落在既有四值域内），集合之外 MUST 与基线逐字节一致（删除或改写行数为 0）；实际差异行 MUST 由契约测试枚举并与声明的允许差异集比对（漂移守卫）。

#### A-4 ADR 引用

- **FR-015**: `docs/decisions/template.md` 的 `## Alternatives` 段 MUST 增加一个 `tension_id`（[[STR-004]]）引用位，以 `T-NNN` 指向同一特性计划中的记录，MUST NOT 复制记录字段内容；引用 MUST 可解析，指向不存在的记录 MUST 判为断链错误。当该决策无张力记录时，MUST 显式写明「无承重张力记录」及判定结论。

#### A-5 确定性校验与机制边界

- **FR-016**: 结构校验 MUST 由既有 `scripts/python/` 下的确定性程序执行（只用标准库、无第三方依赖、无常驻进程），至少检查：六字段齐备、`binding_constraints` 双极非空、`tension_id` 唯一且按序、`T-NNN` 形态、拒绝形态命中（含 [[STR-002]]）、`expected_sacrifice` 可解析到测量来源。退出码语义 MUST 与既有检查器一致：0 无错误、1 发现错误、2 输入不可读。
- **FR-017**: 该校验器 MUST 拥有逆样本（快速失败纪律对机器给出的绿同样成立）：删任一字段、置空预期代价、写入不可判定措辞、重复 `tension_id`、指向不存在的测量来源——每一例 MUST 在契约测试中产生一次红运行记录；逆样本 MUST NOT 只写在文档描述里。
- **FR-018**: 本特性 MUST NOT 新增 `/speckit.*` 命令、存储、台账、调度器、评分器或模型调用；张力记录搭在计划工件上，判定结果只进既有 analyze 报告与计划文本。

#### B-1 证伪四元组（SI-3C）

- **FR-019**: `shared/guidelines/critique-and-self-critique.md` 的输出形态 MUST 由「一句话加 verdict」升级为封闭四元组：`attempt`、`exit_code`、`observation`、`would_go_red_if`（[[STR-003]]）；四元组 MUST 在派发前产生，字段集合封闭，扩展 MUST 走 owner 修订。
- **FR-020**: 四元组各字段 MUST 有可判定语义：`attempt` 是一位复核者可原样重放的命令、grep、测试或测量；`exit_code` 是整数；`observation` 是原样输出摘要（模型转述判为不合格）；[[STR-003]] 点名「把哪个输入改坏，该尝试必须变红」的具体输入与预期红色结果。
- **FR-021**: 拒收规则：四元组任一字段缺失或为空、`observation` 为转述、或 [[STR-003]] 给不出可执行的反空真条件（例如只写「若实现有误就会失败」）时，SI-4 接收方 MUST 拒收该提案；拒收 MUST NOT 折算为「未达成」，MUST NOT 静默接受，也 MUST NOT 以「已执行」字样通过。
- **FR-022**: 载体 MUST 不变：四元组记在提案已有载体（SI-4 派发载荷、SI-7 intervention 记录），MUST NOT 新建台账、存储、probe 或评分。
- **FR-023**: `shared/workflow/self-improvement-workflow.md` 的 SI-3C MUST 只保留步骤摘要与指向 owner 的指针，MUST NOT 复述四元组字段清单或拒收规则；契约测试 MUST 断言「owner 有字段定义」且「workflow 无第二份定义」。

#### C-1 术语与分发

- **FR-024**: 用户可见正文 MUST 只用工程词（DTR、反题、反指标、判别性证据、重开条件）；§ Assumptions A3 列为内部别名的术语 MUST NOT 出现在任何分发面的用户可见文本中（`shared/`、`templates/`、`skills/`）。内部别名只允许出现在本规格的 Assumptions 与 owner 的术语注记内。
- **FR-025**: 两顶帽子：唯一编辑面 MUST 是框架源（`shared/`、`templates/`、`skills/internal/analyze-artifacts/`、`scripts/python/`、`docs/decisions/`）；`.specify/` 运行时副本与各工具命令副本 MUST 经既有同步或再生成机制产出，MUST NOT 手改；计划 MUST 列出本次触及的镜像对，并以「相对改动前测量无新增漂移」为判定方式。
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

- **SC-001**: 在含 1 条承重决策的夹具计划上，[[STR-001]] 章节存在、该记录六字段齐备且 `tension_id` 唯一按序，确定性校验器返回 0；四个反向输入（删任一字段、置 `expected_sacrifice: none`（[[STR-002]]）、写入不可判定措辞、重复 `tension_id`）各返回 1。判定只读退出码与报告条目，不依赖人工阅读记录正文。
- **SC-002**: analyze 结构通道对三类缺陷各报 1 条 HIGH（缺记录、六字段不全、代价无法映射），对合规计划三类各 0 条，对「章节缺失」的计划报 HIGH 而非跳过；四类夹具各运行一次即可判定。
- **SC-003**: trivial 夹具（无承重决策、`N/A` 且逐条说明判据不成立）零记录、零 HIGH；同一夹具补入一条不可逆决策后复跑恰出现 1 条 HIGH。两次运行的 HIGH 计数与记录数即可判定，不需要阅读报告正文。
- **SC-004**: 合规提案（四字段齐备且反空真条件可执行）被接收；六类不合格（四字段各缺一、`observation` 为转述、反空真条件为空真）全部被拒收，拒收率 6/6，每条拒收都给出缺失字段或空真的具名判定。
- **SC-005**: 零新增机制：`/speckit.*` 命令清单与基线提交 `ac63fe8c` 处的清单逐字相同（允许差异集为空）；新增常驻进程、服务、调度器、评分器数量为 0；新增第三方依赖为 0；新增校验程序只用标准库。判定以命令清单、依赖清单与进程清单的前后差异完成，差异必须落在空集内。
- **SC-006**: ADR 可追溯：`docs/decisions/template.md` 的 `## Alternatives` 段含 `tension_id` 引用位；夹具计划中每条记录的预期代价都解析到一条已声明的测量来源，解析失败数为 0；指向不存在记录的引用被判为断链错误。
- **SC-007**: 术语合规：在 `shared/`、`templates/`、`skills/` 三棵分发面的用户可见文本中，§ Assumptions A3 列出的内部别名出现次数为 0；改动前后各测一次，计数相同。
- **SC-008**: 既有闭合面不回退：以基线提交 `ac63fe8c` 为参照物，`detection-and-severity.md` 与 `critique-and-self-critique.md` 的实际差异行全部落在声明的允许差异集内（新增段落与新增通道引起的计数行），集合外的删除或改写行数为 0，集合内结构不变量通过；拒绝形态、边界声明、消费者清单的条目数不小于基线。判定由差异行枚举与契约测试计数给出，不靠阅读文件判断。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 夹具计划文件与结构校验器的退出码、报告条目；五次运行（1 合规 + 4 反向）的完整输出按「执行时全量捕获」纪律归档到本特性证据目录。
- **SC-002 Source**: analyze 报告中的严重度列与条目计数；四类夹具各一次运行的报告快照。
- **SC-003 Source**: 同一 trivial 夹具前后两次 analyze 报告的 HIGH 计数，与计划中的记录条数；两次运行各留一份报告快照。
- **SC-004 Source**: 接收方的接收 / 拒收判决输出；七个夹具（1 合规 + 6 不合格）各一次运行。
- **SC-005 Source**: `/speckit.*` 命令清单（命令模板目录与各工具副本目录的并集）、依赖清单与进程清单在基线提交 `ac63fe8c` 与实现后的两次采集差异；单次比较即可判定。
- **SC-006 Source**: `docs/decisions/template.md` 的文本断言结果，与记录到测量来源的解析结果（解析器输出）。
- **SC-007 Source**: 三棵分发面的术语 grep 计数，改动前后各一次。
- **SC-008 Source**: 两个 owner 文件与基线提交的逐字 diff，以及契约测试的断言计数。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "## Decision Tensions" | FR-008, FR-011, SC-001 |
| `STR-002` | "expected_sacrifice: none" | FR-004, FR-016, SC-001 |
| `STR-003` | "would_go_red_if" | FR-019, FR-020, FR-021 |
| `STR-004` | "tension_id" | FR-002, FR-015 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-10-29

- 本轮无活动 `[NEEDS CLARIFICATION]` 标记；三处原可发问的开放点按缺省裁决记录，未进入问题队列：编号顺延（A2）、内部别名的对外边界（A3）、载体选择（A6）。
- 特性绑定在本阶段给出而非推迟到 `/speckit.clarify`（A4）；绑定结论与候选核验表见 § Related Feature。
- 显式排除项以 § Requirements 的「显式排除项（Out of Scope）」为准，不在 clarify 阶段重新开启。
