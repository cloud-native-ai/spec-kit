# Requirements Specification: Review P1 Governance（评审 P1 治理）

**Requirement Branch**: `063-review-p1-governance`  
**Created**: 2026-10-19  
**Status**: Draft  
**Input**: User description: "把 062-humanize-command SDD 过程评审报告中的 P1 findings（以及同批 P2）收敛为一个框架级治理特性，修复产生这些缺陷的机制，而不是只修 062 的实例。" 权威评审报告：`.specify/specs/062-humanize-command/review.md`（528 行；P0=0 / P1=6 / P2=2）；本轮治理范围与终态说明：`/tmp/sdd-review-p1/brief.md`（运行输入，未在本阶段归档）。

## Related Feature *(mandatory)*

**Feature ID**: Need clarification  
**Feature Name**: Need clarification

## 现状锚点（2026-10-19 以源码与评审报告实测为准；dated record，仅作治理输入，非运行时保证）

- 权威评审报告为 `.specify/specs/062-humanize-command/review.md`：P0=0、P1=6、P2=2，共 15 条改进建议；本特性治理的 finding 编号与严重度为 F1（P1）、F2（P1）、F3（P1）、F4（P1）、F5（P2）、F6（P1）、F7（P1）、F8（P2）。
- 评审报告 §0 明确本仓同时是框架源与客户运行时（Two Hats）：本特性的机制修复 MUST 落在框架源侧（`shared/`、`templates/`、`skills/`、`scripts/`、`tests/`、`docs/`）；`.specify/` 运行时副本是生成/同步面。
- 评审报告记录的两条决策类异常与本特性相交：E1 = `run-determination.py` 的 `(unit_id, run_id)` 幂等锁使已落定的欠测量记录无法重跑补齐；E2 = Feature 062 的 `Implemented → Ready for Review` 转换归属冲突（`features/062.md` 的状态判据已满足 vs `shared/workflow/feature-integration.md` 只把该转换授予 `/speckit.checklist`）。
- 当前编号断点：仓库既有规格最大为 062；本规格为 063；master 在 `060320e5` 之后为续作基线。
- 评审报告 §7 明确：F3 的“review 转换表缺行”是 post-validation addendum（未经独立验证波次），但它是 F3 证据的一部分；本特性按 brief 要求将其纳入 F3 治理面。

## Assumptions（对输入中开放点的缺省裁决；clarify 阶段可推翻，推翻时 MUST 记录）

- **Related Feature 暂不绑定**：本阶段保留 `Need clarification`；由 `/speckit.clarify` 按 Feature Binding Rules 绑定。brief 称本特性为“新框架治理特性”，但未指定 Feature ID，故不在此发明。
- **治理范围是 F1–F8 的机制修复**，不是重做 062，也不是逐条复述评审建议。F5/F8 虽为 P2，仍在 brief 的 F1–F8 范围内。
- **机制修复优先于实例修复**（宪法 XI）：每条 finding 的验收落在“产生该缺陷的模板/技能/命令/脚本/契约”上；`.specify/` 运行时副本经既有 sync/init 流程落位，MUST NOT 以手改运行时副本作为主要交付。
- **062 的制品是证据，不是编辑对象**：本特性 MUST NOT 修改 `.specify/specs/062-humanize-command/` 下的 `requirements.md`、`plan.md`、`tasks.md` 或 `review.md` 来“消除” finding。`notes/red-first-evidence.md` 的 GATE 编号实例修复不在本特性范围内（F8 只要求机制侧不再产生裸 id 引用）。
- **E1 裁决（run-determination 幂等锁）**：保留 `(unit_id, run_id)` 幂等语义，不自动另铸 run-id；机制修复是让编译 face 首次调用即完整（必填参数全集 + 源参数），并把“已落定欠测量记录的人工补测”留给调用者显式决定、在运行证据中记录。理由：每轮一条记录是既有设计；自动另铸会制造平行记录并证伪“one run, one record”。
- **E2 裁决（Ready for Review 归属）**：在 `shared/workflow/feature-integration.md` 转换表中新增 `/speckit.review` 行，转换条件为“review 证据已提交且每个延期项已解决或豁免”；`/speckit.checklist` 行保留，但注明其转换仅在 checklist 于 implement 之后运行时适用。理由：`features/062.md` 的状态判据把该状态定义为本阶段产出，且转换表本身声明“每个命令恰好拥有一个转换”。
- **REC 登记形态**：`register.md` 采用既有指针行形态（编号 → 一行含义 → 权威路径 → 状态），MUST NOT 复述建议正文；不为 REC 新建存储/引擎/评分系统（宪法 IX/XIII）。
- **REC 的合法入口**：`shared/workflow/feedback-step.md` § Scope guard 保持本地 scope 规则不变，同时点名既有的 Mode 5 自省豁免路径为全局 review 建议的合法入口；不新建 intake 存储。
- **历史回填不是机制修复的前置条件**：本特性前向强制“评审产生 REC 时同批登记”；对十份历史 review 的回填 MAY 作为有界迁移执行，但不构成验收前置，且 MUST NOT 演化为新的跟踪系统。
- **checklist 关闭形态**：采用 append-only recheck 文件（061 的 REC-C5），不原地刷新原 checklist；waiver 采用 `Scope` / `Basis` / `Disposition` / `Closed` 四段（061 的 REC-C6）。原始未勾选项保留为历史记录。
- **引用组花括号字符集**（F1）：`(` 与 `（` 是开组定界符，`)` 与 `）` 是对应闭组定界符；嵌套只要求同宽度匹配。跨宽度嵌套/不配对视为畸形组，MUST 由检查器报告，MUST NOT 被静默计为引用或静默计为 mention（缺省裁定，见 Clarifications）。
- **基线差异分类**（F7）：允许 `upstream repair` / `inherited` / `attributable to this feature` 三类之外增加 `undecidable`；无法归因时 MUST 报告 undecidable，MUST NOT 猜测。
- **证据哈希算法**（F6）：requirements 层只要求“确定性内容哈希 + 模板记录算法”；具体算法（如 SHA-256）由 plan 选择，避免在需求层锁定实现。
- **计数与枚举**：编译单元集合、baseline 文件集合、recognition 参数集合等易变集合 MUST 由引擎/目录派生或引用其 owner（宪法 XIV），MUST NOT 在需求或下游制品中手写固定条数。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 分析阶段看见已写下的质量信号 (Priority: P1)

框架维护者在检查单里写下一个 `Gap`，或在契约集中使用全角括号引用 FR。下一次 `/speckit.analyze` 必须读到这份检查单、把未回答的 `Gap` 升格为 finding 或显式处置；条款覆盖核算必须识别两种括号宽度并作为 analyze 的固定步骤运行，而不是等评审者事后手工发现。

**Why this priority**: F1 与 F2 是同一类失效——证据已经写在树里，却没有阶段消费它，导致同一缺陷被重复诊断并付出多轮修复提交。两者都直接削弱 analyze 门作为“实现前最后一道机械一致性检查”的可信度。

**Independent Test**: 在临时 fixture 中放入一个带 `Gap` 未勾选项的 checklist 与一份混用全角/半角括号的契约集，运行 analyze 与覆盖核算；检查 `Gap` 是否被升格/处置、覆盖总数是否不再随括号宽度分叉。

**Acceptance Scenarios**:

1. **Given** 一个 feature 的 `checklists/*.md` 中存在 `[覆盖/安全, Gap]` 的未勾选项，**When** 运行 `/speckit.analyze`，**Then** 该条要么作为 finding 出现在门报告中，要么带有明确的 disposition 与理由；不存在“未勾选且未处置”的 `Gap`。
2. **Given** 一份契约集同时包含 `(FR-001)` 与 `（FR-002）` 两种引用组，**When** 用 owner 规则与 `clause_extract.py` 抽取，**Then** 两种宽度都被识别，同一语料只得到一个覆盖率总数；仅用 ASCII 与同时用两种宽度不再产生两个都自称“实测”的总数。
3. **Given** 一个 feature 尚未冻结 `coverage-baseline.txt`，**When** `/speckit.analyze` 运行覆盖核算，**Then** `baseline-missing` 作为阶段可见问题出现并给出 remedy，而不是被静默跳过；`/speckit.tasks` 已按既有冻结时机产出该基线。
4. **Given** 一个已解析的 checklist 条目（其问题主题后来被 requirements/plan 修复），**When** 进入 implement 前的 checklist 门，**Then** 该条目由 append-only recheck 记录回答，不计为未完成，也不需要 waiver。

---

### User Story 2 - 评审建议成为可追踪的持久编号 (Priority: P1)

框架维护者运行一次完整评审后，每条 `REC-` 建议在同一个提交里登记进 ID Register；下游 feature 能按编号找回归档、目标路径与状态，而不必重新诊断同一个缺陷。评审的 Handoffs 不再是一句没有所有者的“Apply improvements”。

**Why this priority**: F3 让生命周期中最昂贵的产物（完整过程评审）变成死信；十份历史 review 与 061 的 22 条 REC 都未进入任何可检索入口，同类缺陷因此反复以新编号重新出现。

**Independent Test**: 在 fixture 中生成一份含 2–3 条 `REC-` 的 review，执行收尾；检查 `register.md` 是否在同一提交出现对应指针行，目标路径能否在干净 checkout 上解析，backlog 是否有合法入口。

**Acceptance Scenarios**:

1. **Given** 一份新评审报告，**When** 评审阶段收尾，**Then** 报告中每条 `REC-` 都在 `.specify/memory/register.md` 有一行指针登记（编号 → 一行含义 → 报告锚点 → 状态），且提交包含该登记。
2. **Given** 一份把目标写成机器本地绝对路径的 review，**When** 按新模板起草，**Then** 每条 REC 首先给出 repo-relative 路径，绝对路径只作括号补充；没有 repo-relative 形态的外部目标必须标记为 external 并给出理由。
3. **Given** 一条全局 review 建议，**When** 走 feedback 入口，**Then** `feedback-step.md` § Scope guard 明确指向既有的合法 framework-scope 入口（Mode 5 自省豁免），而不是把它挡在 `scope: local` 之外且无路可走。
4. **Given** 一个 feature 已满足自身状态判据且 review 证据已提交，**When** `/speckit.review` 收尾，**Then** 转换表明确由 review 拥有 `Implemented → Ready for Review`，registry 落位；`/speckit.checklist` 的同一转换仅在其于 implement 之后运行时适用。

---

### User Story 3 - 编译后的 Wrap-up face 可按原文执行 (Priority: P1)

任意 `/speckit.*` 命令的收尾面是 AUTO-GENERATED 文本；执行者照抄即可完成运行判定与 feedback 记录，而不是先经历四轮“缺一个参数”错误、再得到一个无法补测的欠测量记录。

**Why this priority**: F4 在本轮 10 个 command-unit wrap-up 中全部命中，且把运行判定传感器静默退化为三个 `not_evaluated` 轴并锁死；它直接破坏“AUTO-GENERATED 文本可信”这一前提。

**Independent Test**: 对每个编译单元逐字执行其 `## Wrap-up` 的引擎调用（隔离工作区），断言一次成功、无缺参、无因 face 缺参导致的 `not_evaluated`；同时用缺 2 个以上必填参数的 fixture 验证一次列全。

**Acceptance Scenarios**:

1. **Given** 一个编译后的 command-unit face，**When** 逐字执行其第 1、3 步，**Then** 引擎一次调用成功，不出现 `--run-id is required` / `--complexity is required` / `--review is required` 的逐参单错。
2. **Given** 一个 handler 的引擎 action 接受源参数（如 `--session-file`、`--declared-check`），**When** 渲染该单元的 face，**Then** face 同时给出该 action 接受的必填参数与源参数；action 不接受的参数不得被渲染。
3. **Given** 一次调用缺少两个以上必填参数，**When** 引擎报错，**Then** 一个错误/结构化列表列出全部缺失参数，而不是每修一个再暴露下一个。
4. **Given** 全部单元重编译后，**When** 运行 `probe-utils.py --action compile-embeds --check`，**Then** 零漂移；`backlog.md` 中 2026-10-15 的该条状态翻转为 closed 并附证据。

---

### User Story 4 - “声称 PASS”必须绑定到归档证据 (Priority: P1)

验证记录中的每个 `pass` 都有结构化证据行：样本 id、归档路径、内容哈希、verdict。一个声称“已运行 s11”但实际没有归档证据的记录，会被机械门判红，而不是靠执行者自 disclosure 才发现。

**Why this priority**: F6 是“绿是声明而非证据”的直接实例；059-F4 已经报告过同型缺陷，062 再次复发。行为类条款的验收如果只剩自我披露，整个验证记录的可信度就不成立。

**Independent Test**: 在 fixture 中制造一个 `pass` 但证据文件缺失/为空/哈希不匹配的样本，运行 evidence-binding gate；断言三种情形都判红；补上正确证据后判绿。

**Acceptance Scenarios**:

1. **Given** 一份验证记录，**When** 某样本标记 `pass` 且其归档文件存在、非空、哈希匹配，**Then** `gate-implement-evidence-binding` 通过。
2. **Given** 同一记录中某 `pass` 的归档文件缺失、为空或哈希不匹配，**When** 运行该 gate，**Then** gate 判红并指出样本 id 与失败原因；不得降级为“自披露后继续”。
3. **Given** 一个 evaluation sample 有证据行但 verdict 不是 `pass`（如 `fail`/`deferred`），**When** 运行 gate，**Then** 不要求其证据绑定（只有 `pass` 声明承担该义务）。
4. **Given** `verification-log-template.md`，**When** 作者填写验证记录，**Then** 模板在 implement results 与 SC evaluation 之间提供逐样本证据槽，而不是让每个 feature 自创证据表。

---

### User Story 5 - 冻结基线在消费侧被重新读懂 (Priority: P1)

`/speckit.implement` 开工前重新捕获每个冻结基线；若数值变化，先写回引用行，再用 `git log` 归因（上游修复 / 继承 / 本特性 / 不可判定），之后才允许给出漂移结论。

**Why this priority**: F7 让 implement 面对一个无法解释的冻结数字（209 vs 113）并临场发明对账流程。冻结值在消费侧没有被重新读懂，任何漂移 verdict 都建立在过期测量上。

**Independent Test**: 在 fixture 中让基线在 tasks 代与 implement 之间发生漂移，运行 implement 预检；断言数值被重捕获并写回、差异被分类、无可解释数字。

**Acceptance Scenarios**:

1. **Given** `notes/baseline-*` 中的冻结值与当前树不一致，**When** 开始 `/speckit.implement`，**Then** 预检步骤重新捕获、把新值写入引用它的行，并在任何漂移 verdict 之前给出差异分类。
2. **Given** 一处差异无法通过 `git log` 归因，**When** 分类，**Then** 报告 `undecidable`，不得猜测为 upstream/inherited，也不得据此发红或发绿。
3. **Given** 一个基线文件缺失，**When** 预检运行，**Then** 按“首次捕获”处理并记录 provenance，不得把缺失当作零漂移。
4. **Given** `create-tasks` 的 re-freeze timing 文本，**When** 阅读它，**Then** 它指向 implement 侧的消费步骤，而不是描述一个自己无法执行的职责。

---

### User Story 6 - 陈旧前提与 gate 引用不再静默漂移 (Priority: P2)

`tasks.md` 的 assumption/decision 行复述环境判据时带日期与指针；red-first evidence note 引用 gate 时逐字引用 gate 行。一个被推翻的前提或一个重编号的 gate 会产生可见不匹配，而不是让读者落到错误的位置。

**Why this priority**: F5/F8 是 P2 审计摩擦，不阻塞正确使用；但它们与 P1 机制共享同一根因——封闭枚举/裸引用让事实在载体之外漂移。作为独立切片交付，不拖累 P1 的机制修复。

**Independent Test**: 放入一条无日期/无指针的环境复述行，断言 create-tasks 的载体规则能捕获它；放入一条裸 gate id 引用的 note，重编号 gate 后断言出现可见不匹配。

**Acceptance Scenarios**:

1. **Given** `tasks.md` 的 assumption/decision 或自由散文行复述了环境判据，**When** `/speckit.tasks` 生成或修订，**Then** 该行带 ISO 日期与 `(see § Environment Prerequisites)` 指针；封闭载体清单之外不存在可逃逸的复述。
2. **Given** 一条 red-first 证据 note 引用某个 GATE，**When** 作者写入 note，**Then** note 逐字引用 gate id + name + check command；tasks 重编号后会产生可见不匹配，而不是静默指向错误的 gate。

---

### Edge Cases

- 同一引用组混用全角开括号与半角闭括号（或反向）→ 视为畸形组，检查器报告；不得静默计为引用，也不得静默计为 mention。
- 引用组同宽度嵌套（如 `（FR-001（a））`）→ 按 owner 的“一层嵌套”规则解析；超过一层或跨宽度嵌套 → 畸形组报告。
- 一份契约集只使用半角括号 → 结果与同时支持两种宽度的实现一致；不得因新增宽度支持而改变既有语料的总数。
- feature 没有 `checklists/` 目录 → analyze 正常继续，不产生虚假的 checklist finding。
- checklist 中存在未勾选项但没有任何 `Gap` 标签 → 仍按既有语义加载；只有 `Gap` 项承担“必须升格或处置”的强义务。
- checklist 条目在 analyze 之后被下游阶段解决 → 由 append-only recheck 记录回答；原始 checklist 不原地刷新，原始未勾选行保留。
- 一份 waiver 缺少 `Scope` / `Basis` / `Disposition` / `Closed` 任一段 → 视为不合规 waiver，MUST NOT 被当作已关闭证据。
- 一份 review 没有任何 `REC-` → 不要求在 register 中新增行；不得为满足检查而编造编号。
- REC 的目标在仓库外（如外部依赖）→ 标记 external，给出绝对路径与理由；不得伪造 repo-relative 形式。
- REC 的目标行号在后续编辑中失效 → 以路径 + 章节锚点为主，行号只作辅助；登记行不因行号漂移而失效。
- 编译 face 对应的 handler 没有源参数 → 只渲染必填参数；不得为不存在的参数生成占位值。
- 一个已存在的 `(unit_id, run_id)` 记录在 face 修复前就已落定且欠测量 → 重跑返回 duplicate；引擎不得自动另铸 run-id。调用者若显式补测，MUST 在运行证据中记录该决定与新 run-id。
- 运行环境中的引擎版本比 face 生成时旧 → 缺参错误应一次列全；若参数本身不存在，错误必须指出该参数不被该版本接受，而不是静默忽略。
- `notes/baseline-*` 中某个基线文件缺失 → 预检按“首次捕获”处理并记录 provenance；MUST NOT 把缺失当作零漂移。
- 基线差异分类为 `undecidable` → 必须显式报告并保留原始数值；不得以“看起来像上游修复”代替证据。
- 证据归档文件存在但为空 → 判红（`test -e` 不足以证明执行）。
- 证据哈希算法未在模板中声明 → 视为模板不合规；不得由执行者临场选择算法后声称可复现。
- red-first note 引用一个不存在的 gate id → 逐字引用使不匹配可见；检查器/评审 MUST 报告，而不是接受裸 id。
- 环境判据行只有日期没有指针，或只有指针没有日期 → 均不合规。
- 历史 review 没有 `REC-` 编号 → 不强制回填；前向机制只要求新评审按新规则登记。
- 一个 command-unit face 的 handler 清单在重编译后变化 → 以引擎的当前 unit 集合为准；不得在需求或模板中手写固定单元数。

## Requirements *(mandatory)*

### Functional Requirements

#### F1 — 条款覆盖核算通道（引用组字符集与接线）

- **FR-001**: 引用组语法的 owner `shared/definitions/contract-clause-definitions.md` § 4 rule 2 MUST 明确声明引用组的定界字符集：开组定界符为 `(` 或 `（`，对应闭组定界符为 `)` 或 `）`；嵌套 MUST 在同一宽度内匹配。该声明 MUST 是规范性的（owner 正文），不能只存在于抽取器实现中。
- **FR-002**: `scripts/python/clause_extract.py` 的 `parentheticals()` MUST 实现 FR-001 的字符集：接受两种宽度、同宽度嵌套匹配；同一语料 MUST NOT 因是否识别全角括号而得出两个都自称“实测”的总数。抽取器 MUST 增加确定性自测样本，至少包含一个全角引用组与一个同宽度嵌套组。
- **FR-003**: 条款覆盖核算 MUST 接入 `/speckit.analyze`：`templates/commands/analyze.md` 与 `skills/internal/analyze-artifacts/SKILL.md` 的装载/检查流程 MUST 调用 `scripts/python/account-clause-coverage.py`，使覆盖核算成为 analyze 的固定步骤而非评审者可选的旁路工具。基线缺失时 MUST 把 `baseline-missing` 作为阶段可见问题与 remedy 呈现，MUST NOT 静默跳过。
- **FR-004**: 对含契约集的 feature，`/speckit.tasks` MUST 把 `coverage-baseline.txt`（[[STR-002]]）纳入冻结基线集合，使用覆盖引擎的冻结路径（`--freeze`）产出；冻结时机 MUST 与该命令既有的 re-freeze timing 一致（每个 feature 的第一次全树核算，而非第一次全绿）。analyze 的消费步骤 MUST 指向同一基线文件。无契约集的 feature MUST 显式 skip 并说明理由，MUST NOT 伪造空基线。

#### F2 — checklist 的责任阶段与关闭形态

- **FR-005**: `/speckit.analyze` MUST 装载 feature 的 `checklists/*.md`；每个未勾选且带 `Gap` 标签的条目 MUST 被升格为 finding，或在门报告中给出明确 disposition 与理由。MUST NOT 出现“未勾选、未升格、未处置”的 `Gap`；disposition 形态 MUST 由 analyze 技能定义为确定性可检查的标记，而不是自由散文。
- **FR-006**: checklist 的回答 MUST 采用 append-only recheck 记录（每轮一个 recheck 文件）：每个已回答条目 MUST 引用它所回答的 requirement 行；MUST NOT 原地刷新原 checklist。原 checklist 的未勾选行 MUST 保留为历史记录（lands 061 REC-C5）。
- **FR-007**: `skills/internal/implement-feature/SKILL.md` § Step 2 — Checklist exemption gate MUST 增加第三分支：当后续阶段已经解决某条目的主题并按 FR-006 记录回答时，该条目 MUST 被视为已回答、不计入未完成；门只对真正未解决的条目触发。MUST NOT 继续让每个 feature 因“无阶段负责翻勾”而必然 waiver。
- **FR-008**: waiver 记录 MUST 采用 `Scope` / `Basis` / `Disposition` / `Closed` 四段格式，并列出关闭该条目的上游制品编辑（lands 061 REC-C6）。缺少任一段的 waiver MUST 被视为不合规；`Closed` 必须说明是什么解决了它，而不是永远 open-ended。

#### F3 — 评审建议的持久化与所有权

- **FR-009**: `templates/commands/review.md` § Handoffs “After” MUST 具名所有者与可机械检查的义务：报告中每条 `REC-` 编号（[[STR-003]]）MUST 在同一个提交中登记到 `.specify/memory/register.md`，采用既有指针行形态（编号 → 一行含义 → 报告锚点 → 状态）。MUST NOT 保留“Apply improvements to spec-kit templates/commands/scripts”这类无所有者指令。
- **FR-010**: `templates/instructions-template.md` § ID Register MUST 把 `REC-`（[[STR-003]]）加入持久编号枚举，使该义务可从常驻指令层发现；活动 `.specify/instructions.md` MUST 经既有 refresh/sync 流程获得该行，MUST NOT 以手改运行时副本作为主要落点。
- **FR-011**: `shared/workflow/feedback-step.md` § Scope guard MUST 保留 wrap-up 条目的 `scope: local` 规则，同时点名全局 review 建议的合法入口（既有的 Mode 5 自省豁免路径）。MUST NOT 新建独立 intake 存储、跟踪引擎或评分系统（宪法 IX/XIII）；“那是 `/speckit.review` 的职责”MUST NOT 再等同于“没有任何机制跟踪它”。
- **FR-012**: `templates/review-template.md` § 5 与 Replacement Rule 3 MUST 把 repo-relative 路径作为 REC 目标的主形态，绝对路径只作括号补充；该方向与 061 报告的做法相反，因为相对路径在任意 checkout 可解析。确实没有 repo-relative 形态的外部目标 MUST 标记 external 并给出理由。
- **FR-013**: `shared/workflow/feature-integration.md` 的状态转换表 MUST 增加 `/speckit.review` 行：`Implemented → Ready for Review`，条件为“`review.md` 已提交且每个延期项已解决或豁免”；`/speckit.checklist` 行 MUST 注明其同一转换仅在 checklist 于 implement 之后运行时适用。“每个命令恰好拥有一个转换”的规则 MUST 保持成立。

#### F4 — 编译 Wrap-up face 的可执行性

- **FR-014**: `scripts/python/probe-utils.py` 的 `--action compile-embeds` 渲染器 MUST 支持 handler 行的完整参数占位约定：为每个单元渲染其引擎 action 接受的必填参数全集（包含 run-scoped 值如 `--run-id`）以及源参数（该 action 当前接受的 `--session-file`、`--session-rows`、`--tool`、`--declared-check`、`--green-check` 等；权威集合以引擎 parser 为准）。action 不接受的参数 MUST NOT 被渲染。占位约定 MUST 声明在 registry/渲染契约中，而非逐命令手写。
- **FR-015**: `scripts/python/run-determination.py` 与 `scripts/python/feedback-utils.py` MUST 在一次调用中报告全部缺失的必填参数（单个错误或结构化列表），MUST NOT 逐参单错；输入错误的退出码保持既有约定。
- **FR-016**: 修复落地后，所有编译单元 MUST 经 `compile-embeds` 重编译，`--check` MUST 零漂移，适用时以 `--reconcile` 收口；`backlog.md` 中 2026-10-15 的该条 MUST 在同一提交翻转为 closed 并附证据。
- **FR-017**: `run-determination.py` 的 `(unit_id, run_id)` 幂等语义 MUST 保持不变；框架 MUST NOT 自动另铸 run-id 来为既有欠测量记录补测。机制修复是首次调用即完整（FR-014/FR-015）；若调用者显式决定补测，该决定 MUST 在运行证据中记录，MUST NOT 成为引擎默认行为。

#### F5 — 环境判据载体的开放

- **FR-018**: `skills/internal/create-tasks/SKILL.md` § Environment probe rules item 2 的封闭载体清单 MUST 打开：`MUST reference § Environment Prerequisites instead of restating verdicts` 的义务 MUST 覆盖 per-phase prerequisites、`[~]` task notes，以及**任何 assumption/decision 或自由散文行**。`templates/tasks-template.md` § Environment Prerequisites 的 ACTION REQUIRED MUST 同步扩展，并要求任何复述环境判据的行携带 ISO 日期与 `(see § Environment Prerequisites)` 指针。

#### F6 — 声称到证据的绑定

- **FR-019**: `templates/verification-log-template.md` MUST 在 `# -- /speckit.implement results --` 与 `# -- Success Criteria evaluation --` 之间增加结构化证据记录段：每个 evaluation sample 一行，承载 sample id → 归档工件路径 → 内容哈希 → verdict。模板 MUST 声明确定性哈希算法与“`pass` verdict 必须有完整证据行”的规则。
- **FR-020**: `shared/definitions/probe-definitions.md` MUST 在既有 command-gate 行旁注册 `gate-implement-evidence-binding`（[[STR-001]]），object 为 `/speckit.implement`，class 为 `command-gate`；`skills/internal/implement-feature/SKILL.md` MUST 在 GATE-8 旁引用该 gate。检查内容：对每个记录为 `pass` 的样本，归档工件 MUST 存在、非空，且其计算哈希 MUST 等于记录哈希；缺失/为空/不匹配 MUST 判红。该 gate MUST 复用既有 gate-probe 机制，MUST NOT 新建子系统。
- **FR-021**: 验证记录中的 `pass` 声明 MUST 由 FR-019 的结构化证据行支撑；没有证据行的 `pass` MUST 被视为 unverified，MUST NOT 作为通过证据引用。

#### F7 — 冻结基线的消费侧义务

- **FR-022**: `skills/internal/implement-feature/SKILL.md` MUST 在 Step 1 之前增加预检步骤：重新捕获 `<spec-dir>/notes/baseline-*` 的每个冻结基线（集合从目录派生，不手写条数）；重捕获值不同时，MUST 把新值写入引用它的行，并在任何漂移 verdict 之前用 `git log` provenance 把每处差异分类为 `upstream repair` / `inherited` / `attributable to this feature` / `undecidable`。`undecidable` MUST 显式报告，MUST NOT 猜测。
- **FR-023**: `templates/commands/implement.md` MUST 陈述与 FR-022 相同的预检职责，使该义务到达命令面，而不只存在于技能内部。
- **FR-024**: `skills/internal/create-tasks/SKILL.md` § Re-freeze timing MUST 指向 implement 侧的消费步骤；它保留生产侧的 re-capture 义务，但 MUST NOT 继续描述一个自己无法执行的“在 implement 开始时重捕获”职责而不给出消费者落点。

#### F8 — gate 引用形态

- **FR-025**: 在 `skills/internal/implement-feature/SKILL.md` 规定 red-first evidence note 的形态处，note MUST 逐字引用 gate 行（id + name + check command），MUST NOT 只引用裸 gate id。这样 tasks 重编号会产生可见不匹配，而不是静默指向错误的 gate。该义务前向适用；062 的 note 实例不在本特性编辑范围内。

#### 跨切面约束

- **FR-026**: 所有修复 MUST 落在框架源侧（`shared/`、`templates/`、`skills/`、`scripts/`、`tests/`、`docs/`）；`.specify/` 运行时副本 MUST 经既有 sync/init 流程更新，MUST NOT 以手改副本作为主交付（宪法 XI 两顶帽子）。
- **FR-027**: 本特性 MUST 为每个机制变更增加或更新确定性契约测试；对否定命题（“X 不得发生”）MUST 配变异演练，证明守卫在对象被破坏时会转红。测试 MUST 以冻结的失败节点名单为基线，改动后零新增失败。
- **FR-028**: 本特性 MUST NOT 新增外部服务、网络调用、模型 API、第三方依赖或后台常驻进程（宪法 IX）。
- **FR-029**: 本特性 MUST NOT 修改 `.specify/specs/062-humanize-command/` 下的 `requirements.md`、`plan.md`、`tasks.md` 或 `review.md` 来消除 finding；062 制品是证据。任何 062 notes 实例修复 MUST 另案处理，不并入本特性。
- **FR-030**: 本特性引入的计数与枚举 MUST 由程序派生或引用 owner（宪法 XIV）：编译单元集合由 `probe-utils.py` 派生，baseline 集合由目录派生，参数集合由引擎 parser 派生；MUST NOT 手写固定条数或重复枚举。

### 显式排除项（Out of Scope）

- 重新实现 `/speckit.humanize`、回滚 062 或重做 062 的实现。
- 修改 062 的 `requirements.md` / `plan.md` / `tasks.md` / `review.md`，或把 062 notes 的实例错误当作本特性的验收对象。
- 改变已合入的 sdd-loop-driver 监控改进，除非某条 P1 机制修复明确需要。
- 新增运行时平台、调度器、检测器、评分系统、成熟度报告或跟踪引擎（宪法 IX/XIII）。
- 新建反馈存储、REC 数据库或第二套注册表；REC 只使用既有 `register.md` 指针行。
- 历史 review 建议的全量回填（可有界迁移，但不是验收前置）。
- 自动提交、自动推送或在工作树之外发起任何写入。
- 修复与本治理范围无关的既有漂移（镜像、测试、文档）。
- 在 requirements 层锁定具体哈希算法、占位符语法或测试实现细节（由 plan 决定）。

### Key Entities *(include if requirement involves data)*

- **Finding（F-N）**: 评审报告中的缺陷单元，携带严重度、证据、目标机制与来源报告锚点；本特性消费 F1–F8，不重新评级。
- **Mechanism Fix Record（机制修复记录）**: 一条 finding 到“owner 文档/机制 → 契约测试 → 验收场景”的映射；它是本特性的执行单元，不是新的持久编号体系。
- **Checklist Item Disposition（检查单条目处置）**: 条目 id、状态（升格/已回答/延后）、回答所引用的 requirement 行、recheck 文件路径与处置阶段。
- **Recommendation（REC-）**: 评审建议的持久编号，携带一行含义、报告锚点与状态；登记在 `register.md`，不在此复述正文。
- **Compiled Wrap-up Face（编译收尾面）**: 由 registry + renderer 生成的单一 `## Wrap-up` 段，携带引擎 action 接受的完整参数集。
- **Frozen Baseline（冻结基线）**: 一个名字级或覆盖级测量，携带捕获命令、日期与引用行；消费侧负责重捕获与归因。
- **Evidence Record（证据记录）**: sample id → 归档工件路径 → 内容哈希 → verdict；`pass` 声明的机械对应物。
- **Gate Row（门控行）**: `probe-definitions.md` 中的 command-gate 注册项，绑定 object、class 与检查语义。
- **Transition Row（转换行）**: `feature-integration.md` 中“命令 → 状态转换 → 条件”的所有权行；每个命令恰好一行。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 引用组字符集不再是一个未声明轴：对同一份同时含半角/全角引用组及同宽度嵌套的 fixture，ASCII-only 与双宽度实现的覆盖率总数差异为 0；owner 正文对定界符与嵌套规则的字面声明存在且可被契约测试断言；畸形跨宽度组被报告数为 100%。
- **SC-002**: 条款覆盖核算成为 analyze 的固定步骤：带契约集的 fixture feature 在 analyze 运行中产生覆盖 verdict 的比例为 100%；`baseline-missing` 不再静默通过；每个含 `contracts/` 且经 `/speckit.tasks` 生成的 feature 都存在 `coverage-baseline.txt`（`find` 检查），缺失数为 0；无契约集 feature 的伪造基线数为 0。
- **SC-003**: 对至少含一条未勾选 `Gap` 的 seed checklist，analyze 门报告中“升格为 finding 或显式 disposition”的覆盖率为 100%；“未勾选、未升格、未处置”的条目数为 0；以一个复刻 062 CHK005/CHK011 形态的 fixture 验证，同一 Gap 在首轮 analyze 即被消费，不再需要后续三提交修复环。seed 的 `Gap` 条目数 MUST 非零，使该断言不是空真。
- **SC-004**: 已被下游解决的 checklist 条目由 append-only recheck 记录回答的比例为 100%；因此被迫 waiver 的条目数为 0；原始 checklist 被原地刷新的次数为 0；缺少 `Scope`/`Basis`/`Disposition`/`Closed` 任一段的 waiver 数为 0。
- **SC-005**: 在至少含一条 `REC-` 的 seed 评审中，`REC-` 编号在 `register.md` 的同提交登记率为 100%（0 条未登记）；登记行可解析到报告锚点与状态；repo-relative 目标路径在干净 checkout 上可解析率为 100%；只有机器本地绝对路径的目标数为 0；全局建议有合法 feedback 入口的比例为 100%。seed 的 `REC-` 条数 MUST 非零，使该断言不是空真。
- **SC-006**: 满足自身状态判据且 review 证据已提交的 feature 在同一运行中进入 `Ready for Review` 的比例为 100%；不满足条件的 feature 被误转的比例为 0%；转换表仍满足“每个命令恰好一个转换”。
- **SC-007**: 逐字执行每个 command-unit 的 `## Wrap-up` 引擎调用，首次调用成功率 100%；缺参错误数为 0；因 face 未给出参数而落为 `not_evaluated` 的轴数为 0；`compile-embeds --check` 漂移为 0；2026-10-15 backlog 行状态为 closed。
- **SC-008**: 对缺 2 个以上必填参数的调用，单次错误列出全部缺失参数的比例为 100%；逐参单错轮次为 0；已存在的 `(unit_id, run_id)` 记录不产生自动另铸 run-id 的次数为 0 例外（即自动另铸次数为 0）。
- **SC-009**: 任何复述环境判据的 tasks 行（含 assumption/decision 与自由散文）携带 ISO 日期与 `(see § Environment Prerequisites)` 指针的比例为 100%；封闭载体清单之外的可逃逸复述数为 0（以 seed fixture 验证）。
- **SC-010**: 每个记录为 `pass` 的样本都有存在、非空、哈希匹配的归档证据的比例为 100%；缺失/为空/不匹配三种反向 fixture 触发红门的比例为 100%；反向 fixture 中由 gate（而非执行者自披露）发现问题的比例为 100%，false-green 数为 0。
- **SC-011**: 冻结基线与当前树不一致时，implement 预检重捕获并写回引用行的比例为 100%；每处差异被分类（upstream repair / inherited / attributable / undecidable）的比例为 100%；未分类差异数为 0；因无流程而临场发明对账写法的次数为 0。
- **SC-012**: red-first evidence note 逐字引用 gate 行（id + name + check command）的比例为 100%；裸 gate id 引用数为 0；在 fixture 中重编号 gate 后产生可见不匹配的比例为 100%。
- **SC-013**: 与冻结的失败节点名单相比，排序后新增失败节点数为 0；镜像/生成面新增漂移数为 0；新增外部服务、网络调用、模型 API、第三方依赖与后台常驻进程数均为 0。
- **SC-014**: 062 的 `requirements.md` / `plan.md` / `tasks.md` / `review.md` 在本特性提交窗口内变更数为 0；所有机制编辑位于框架源侧，运行时副本由生成/同步产生（手改运行时副本数为 0）；新增计数/枚举中手写固定条数或重复 owner 枚举的数量为 0。

### Measurement Sources & Collection Methods

- **SC-001 / SC-002 Source**: `clause_extract.py` 自测与双宽度 fixture；`account-clause-coverage.py --spec <fixture>` 在临时目录中的输出；owner 正文的契约测试断言；`find <specs> -name coverage-baseline.txt`；analyze 门报告。
- **SC-003 / SC-004 Source**: 含 `Gap` 未勾选项的 seed checklist 加 analyze 运行记录；append-only recheck 文件与 `[x]`/回答条目引用的 requirement 行；implement Step 2 的 exit 记录；waiver 文本审计。
- **SC-005 / SC-006 Source**: 含 2–3 条 `REC-` 的 seed review；`register.md` 检索；干净 checkout / 临时 clone 上的路径解析；`feedback-step.md` 入口审计；`features.md` 与 feature detail 的状态；`feature-integration.md` 转换表的契约测试。
- **SC-007 / SC-008 Source**: 在隔离工作区逐字执行每个编译单元的 wrap-up 引擎调用，记录 exit code 与 stderr；`probe-utils.py --action compile-embeds --check`；`backlog.md` 行状态；缺多参 fixture 的单次错误输出。
- **SC-009 Source**: seed `tasks.md`（含 assumption/decision 与自由散文复述）+ create-tasks 生成结果；grep 日期与指针；载体清单契约测试。
- **SC-010 Source**: seed `verification.md` + `notes/e8-run` 风格证据文件；`gate-implement-evidence-binding` 运行记录；缺失/为空/哈希不匹配三种变异 fixture。
- **SC-011 Source**: 在 tasks 代与 implement 之间制造漂移的 fixture；implement 预检输出；`git log` provenance 记录；引用行写回前后的 diff。
- **SC-012 Source**: seed red-first note；gate 行重编号后的 fixture；逐字引用断言。
- **SC-013 Source**: 改动前用 `scripts/bash/run-tests.sh --names-out <file>` 冻结的排序失败节点名单，改动后 `comm -13 baseline current` 为空；`sync-mirrors.py --check`；依赖清单差异与源码网络调用检索。
- **SC-014 Source**: `git diff -- .specify/specs/062-humanize-command/` 为空；框架源与 `.specify/` 运行时的路径审计；生成/同步命令的 `--check` 输出；计数/枚举的 owner 引用审计。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"gate-implement-evidence-binding"` | FR-020 |
| `STR-002` | `"coverage-baseline.txt"` | FR-004 |
| `STR-003` | `"REC-"` | FR-009, FR-010 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-10-19（requirements 阶段的访谈式裁决；无活动 `[NEEDS CLARIFICATION` 标记）

> 本会话记录 brief 要求自行裁决并在 Assumptions/Clarifications 留痕的开放点。裁决不改变 F1–F8 的范围；clarify 阶段若推翻，MUST 在此追加新会话并保留旧记录。

- Q: `run-determination.py` 的 `(unit_id, run_id)` 幂等锁把欠测量记录定格后，接受欠测量还是另铸 run-id？ → A: **保留幂等锁，接受该条记录为已落定证据；不自动另铸 run-id。** 机制修复改为让编译 face 首次调用即完整（FR-014/FR-015），从源头避免欠测量；若调用者事后显式补测，新 run-id 与理由 MUST 写入运行证据，引擎不提供默认补救（FR-017）。
- Q: Feature 062 的 `Ready for Review` 转换归 `/speckit.checklist` 还是 `/speckit.review`？ → A: **归 `/speckit.review`。** 在 `shared/workflow/feature-integration.md` 转换表新增 review 行，条件为 review 证据已提交且延期项已解决/豁免；checklist 行保留但注明仅在其于 implement 之后运行时适用（FR-013）。依据是 `features/062.md` 的状态判据已把该状态定义为 review 证据产出，且转换表自身要求“每个命令恰好一个转换”。
- Q: REC 的登记形态与合法入口？ → A: **`register.md` 指针行 + 既有 Mode 5 自省豁免入口。** 不新建存储/引擎；`feedback-step.md` 只点名既有合法入口，保持 wrap-up 条目的 local scope 不变（FR-009/FR-011）。历史回填是可选的 bounded migration，不是验收前置。
- Q: checklist 的关闭形态由哪个阶段负责、是否原地刷新？ → A: **由解决该条目主题的阶段负责记录回答，写入 append-only recheck 文件；不原地刷新原 checklist。** implement 的豁免门增加“已回答”第三分支；waiver 采用 `Scope`/`Basis`/`Disposition`/`Closed`（FR-006/FR-007/FR-008）。该裁决同时落地 061 的 REC-C5/C6。
- Q: 引用组遇到跨宽度嵌套或宽度不配对时怎么计？ → A: **视为畸形组并由检查器报告**，不静默计为引用，也不静默计为 mention。合法嵌套只要求同宽度匹配；这是 owner 未明说的边界，作为缺省裁定记录，clarify 可修订（FR-001/FR-002）。
- Q: F8 是否要顺带修正 062 的 `notes/red-first-evidence.md` 中的 GATE 编号？ → A: **不修。** 本特性只落机制侧（逐字引用 gate 行，前向适用）；062 的 notes 属于证据，修改它会模糊“机制是否已修复”的判定（FR-025/FR-029）。
