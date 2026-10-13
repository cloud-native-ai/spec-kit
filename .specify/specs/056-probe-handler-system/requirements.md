# Requirements Specification: Probe-Handler 体系（1 probe ⇒ N handler）

**Requirement Branch**: `[056-probe-handler-system]`  
**Created**: 2026-10-13  
**Status**: Draft  
**Input**: User description: 把 probe 概念泛化为全框架可查询、可修改的一等实体，并新增 Handler 层使一个探测点可挂接 N 个已注册反应（完整背景见本文件 § 现状锚点与 § Assumptions；由 2026-10-13 两轮复盘实测得出）。

## Related Feature *(mandatory)*

**Feature ID**: 056  
**Feature Name**: Probe-Handler 体系（伞形：Probe / Handler / HandlerBinding 基础设施）

## Overview

Probe（插点）目前只在 feedback 域完成实体化：`shared/definitions/probe-definitions.md` 以 Probe Class × Probe Object 两层模型登记 6 Class / 72 内部 Object，由 `feedback-utils.py --action probes`（查询/校验/对账/map/probe-inject）消费，契约测试钉死。其余探测→反应机制（触发升级探测、运行判定四轴、证据 lane 探测、满意度识别等）全部硬编码在引擎代码里——无 id、无注册表、无查询面，无法回答"框架现在有哪些 probe"，宿主项目也无法查询；handler 注册面则始终在框架侧（Q6 裁定：宿主只读，见 FR-021）。

同时，wrap-up 收尾点的反应面已经自发演化出多个机制：feedback 记录 + 阈值提示（028/041/047/055）、token 自评（040）、运行判定（S2 引擎）、docs-sync 评估（033/037）、wrap-up 反思（dogfooding 惯例）。它们的接线形态是**手工嵌入段**——每个机制各自往命令模板与技能文件里塞独立小节，行为规则分散在 `feedback-step.md` 与 `docs-step.md` 两个 shared convention 内部组合。实测代价：Feature 040 一次 wrap-up 机制修订的传播足迹为 194 个文件；每个新机制 = 全框架模板手术。

本特性做两件事：

1. **Probe 泛化（实体化）**：把 probe 真源从"反馈插点真源"扩格为全框架 Probe 真源（伞形），散布的探测点（050 升级探测 P1–P5、运行判定四轴与可用性探测、证据引擎 lane 探测）以声明性元数据入册，代码侧以契约测试对账；纯代码微探针（writability/probe-links/git probe 等）按 One Source of Truth 的 code-first 原则**不入册**，仅在真源中以纯指针目录收录。
2. **Handler 层（1 probe ⇒ N handler）**：新增 Handler（跨单元可复用的反应定义）与 HandlerBinding（探测点→处置器的订阅关系）两个实体，配共享引擎 `probe-utils.py` 的 `compile-embeds` 编译动作——从注册表渲染每单元单一收尾段（AUTO-GENERATED），由既有 regen/sync 机制传播。**加一个 wrap-up 反应 = 注册一行 + 重编译**，不再做模板手术。

行为真源文件（`feedback-step.md`、`docs-step.md` 等）保持不动——注册表只接管**接线**，不接管**行为**（One Source Of Truth）。

### 现状锚点（以源码实测为准，2026-10-13）

- Probe 注册表：`feedback-utils.py --action probes --validate` exit 0，**6 classes / 72 internal + 0 external objects**。
- 反馈嵌入面：`## Feedback` 出现在 **23** 个 `templates/commands/*.md`；技能形态嵌入 **46** 个 `SKILL.md`（`skills/internal/` + `skills/external/` 双层布局，S 层重构后）。
- docs-step 嵌入面：**22** 个命令模板引用 `.specify/shared/workflow/docs-step.md`（行为真源在该文件）。
- 运行判定：经 `feedback-step.md` § Run Determination 接线（步骤 1/2/6 消费），非独立嵌入段。
- token 自评（040）：承载于 feedback-step 反思流程内部。
- 确认门控预算：`scan-confirmation-gates.py` 实测 **total 23**（16 destructive + 7 governance_kept）、violations 0；上限 = 044 `baseline.json` total × 25% = **23.25** → **整数余量 0**。本特性生成的一切新措辞 MUST 零 `BLOCKING_PATTERNS` 命中。
- 术语现状：glossary 已注册 Probe Class / Probe Object / Feedback Probe / System Slice（confirmed），「主动触发点」「派发前自检」等同形异义词已消歧；本特性新增三个术语（见 FR-019）。

### Assumptions

- **行为真源不动**：`feedback-step.md`、`docs-step.md`、`proactive-trigger.md` 等保持为各自反应的行为规则 owner；注册表与编译产物只承载接线（谁在哪个点、以什么次序、什么模式被触发）。
- **既有 Feedback Probe 六 Class 语义零回退**：028 建立的行为（threshold 提示永不阻塞、agent 自省 never solicit、外部 probe 本地隔离不上送、技能 runtime-mode gate、简单命令排除集 agents/constitution/feature）全部保持。
- **引擎侧探测点入册的是声明性元数据**（id / 代码锚点 / 归属切片），不是行为本身；行为代码不改写。
- `probe-utils.py` 为 stdlib-only，与 `feedback-utils.py` 同分布（`scripts/python/` + `.specify/scripts/python/` 双镜像）。
- handler_id 使用 `h-` 前缀——已核验与既有 id 命名空间（`gate-`/`speckit-`/`skill-`/`r-`/`M-`）零冲突，全仓无 `handler_id`/`HandlerBinding` 占用。
- `probe-utils.py`、`compile-embeds`、`## Wrap-up` 三个新标识符经全仓 grep 核验无既有占用。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 散布探测点入册，probe 成为可查询的全框架实体 (Priority: P1)

框架维护者要回答"框架现在有哪些探测点"时，运行一次 `probe-utils.py --action probes` 即得到跨域清单：feedback 域 72 个既有 Object 之外，050 的 P1–P5 升级探测、运行判定的四轴与两个可用性探测、证据引擎的三个 lane 探测各以 Probe Class + Object 行入册，每行挂代码锚点（函数/常量名），契约测试 import 代码与注册表对账（零漂移）。纯代码微探针在真源的"非实体 probe 目录"节中以纯指针收录。

**Why this priority**: 实体化是 Handler 层的前提——没有统一的探测点清单，就没有可挂接的订阅对象；这也是用户原始诉求（"可查询可修改的实体"）的直接落点。

**Independent Test**: 单独可测——注册表 `--validate` exit 0 且覆盖新 Class；契约测试对 `trigger-utils.py`/`run-determination.py`/`evidence-utils.py` 的具名函数/常量与注册表行双向对账（变异演练证明能红）。

**Acceptance Scenarios**:

1. **Given** 扩格后的真源，**When** 运行 `--action probes --validate`，**Then** exit 0，清单含全部既有 6 Class（语义不变）与新 Class，新 Object 均解析到所属 Class 且带代码锚点。
2. **Given** 有人在 `trigger-utils.py` 中删除一个已入册的探测函数，**When** 运行对账契约测试，**Then** 测试转红并指名缺失的锚点（不是恒绿盲检）。
3. **Given** 非实体 probe 目录节，**When** 检查任一条目，**Then** 内容是指针（路径 + 一行语义）而非行为规则复述。

---

### User Story 2 - Handler/HandlerBinding 实体与共享引擎上线 (Priority: P1)

框架维护者要给 wrap-up 点加一个新反应（例如未来的"建议采纳率回看"）时，只需在真源注册一个 Handler 行 + 一条 HandlerBinding（selector 订阅 `@point:wrap-up`），再运行 `probe-utils.py --action compile-embeds` 重新编译——**零模板文件编辑**。共享引擎 `probe-utils.py` 承载 probe 族动作（自 `feedback-utils.py` 抽出）与新的 handlers/compile-embeds 动作；`feedback-utils.py` 保留 feedback 领域动作且行为不变。

**Why this priority**: 这是"1 probe ⇒ N handler"的核心增量；没有它，US1 只是清单。

**Independent Test**: 在测试中注册一个临时 handler + binding，运行 compile-embeds，断言目标单元产物包含该 handler 且既有单元产物不受影响；`feedback-utils.py` 全部既有 action 的封闭集契约保持绿。

**Acceptance Scenarios**:

1. **Given** 一个新注册的 agent 型 handler 与 `@point:wrap-up` binding，**When** 运行 `compile-embeds`，**Then** 所有 scope 匹配单元的收尾段按 order 位置出现该 handler 的调用形式，模板源文件零 diff。
2. **Given** kind=engine 的 handler，**When** 其 action 引用一个引擎中不存在的 action，**When** 运行 `--action handlers --validate`，**Then** exit 2 并指名非法引用。
3. **Given** 同一探测点被 N 个 handler 订阅，**When** 查询 `--action handlers --point wrap-up`，**Then** 返回 N 条按 order 排序的记录。

---

### User Story 3 - 手工嵌入段迁移为编译产物 (Priority: P2)

23 个命令模板与 46 个技能文件的收尾面从"`## Feedback` + docs-sync 两个手工段"迁移为"单一编译收尾段"（AUTO-GENERATED 标记，按 order 顶序列出 h-run-determination → h-feedback-record → h-threshold-notice → h-token-reflection → h-docs-sync-eval 等已订阅 handler 的调用形式）。每单元差异（技能 runtime-mode gate、简单命令排除集）由 selector 与 per-unit 覆盖承载。传播走既有 `regen-command-copies.py` / `sync-mirrors.py`，不新建传播器。

**Why this priority**: 价值兑现面——模板手术税的消除发生在迁移完成后；但依赖 US1/US2 的实体与引擎。

**Independent Test**: 迁移后对任一复杂命令运行其收尾流程（含阈值提示、自省、docs-sync 评估、运行判定），行为与迁移前逐项一致（既有契约测试零新增失败）；两次编译 byte-identical。

**Acceptance Scenarios**:

1. **Given** 迁移完成的仓库，**When** 全仓 grep 手工 `## Feedback` 嵌入段，**Then** 命令模板与技能中的命中数为 0（编译产物中的出现由 AUTO-GENERATED 标记声明来源）。
2. **Given** 真源未变，**When** 两次运行 `compile-embeds`，**Then** 产物逐字节一致。
3. **Given** 一个 runtime-mode gate 技能在非 Spec Kit 项目运行，**When** 执行收尾段，**Then** gate 判定保留，反馈链路按既有语义跳过。

---

### User Story 4 - 对账守卫扩展到 handler 面 (Priority: P2)

编译产物 ↔ 注册表双向零缺漏（041 C-5 同型扩展）：孤儿 handler（无 binding 或 action 非法）与缺失 handler（binding 声明了但产物没有）都是可检出错误；kind=engine 的 action 引用与两个引擎真实 action 封闭集 import 对账；生成措辞零 `BLOCKING_PATTERNS` 命中（门控预算 total 保持 23 / violations 0）；order 依赖（h-run-determination 先于 h-feedback-record / h-threshold-notice）由契约测试钉住。

**Why this priority**: 没有对账，编译产物会静默漂移——快速失败纪律对"机器给出的绿"同样适用。

**Independent Test**: 构造五类破损（孤儿 handler/缺失 handler/非法 action/措辞命中/order 颠倒），契约测试逐类转红且指名错误；正向树全绿。

**Acceptance Scenarios**:

1. **Given** 注册表中删除一个已编译进产物的 handler，**When** 运行对账，**Then** exit 2 指名"产物含未注册 handler"。
2. **Given** 生成段措辞被改为含阻塞语气的句子，**When** 运行门控扫描与措辞契约，**Then** 转红。
3. **Given** 两条 binding 的 order 值相同，**When** 运行 validate，**Then** exit 2（确定性要求 order 在 binding 集内唯一）。

---

### User Story 5 - 二期 binding 与词汇表/文档接线 (Priority: P3)

二期订阅点入册并走同一编译/对账规则：050 情境评估的建议与遥测（`@point:situation`）、036 团队阶段边界总结（`@point:phase-boundary`）、044 门控必要性证据（`@point:confirm-gate`，既有 19 个 gate Object 挂 h-gate-evidence）。词汇表新增 Probe（伞形）/Handler/HandlerBinding 三术语，Feedback Probe 降为域实例，「埋点」消歧条目重写；`docs/reference/` 更新 probe 体系文档。

**Why this priority**: 增量价值但非 MVP 路径；探测面在 050/036/044 已各自工作，入册是治理收益。

**Independent Test**: 每类 binding 独立入册后 compile 对账绿、既有领域行为契约不回退。

**Acceptance Scenarios**:

1. **Given** confirm-gate 19 个 Object 挂 h-gate-evidence binding，**When** 编译与对账，**Then** 绿且 044 既有门控证据契约零回退。
2. **Given** glossary 更新，**When** 检索 Feedback Probe 条目，**Then** 表述为 Probe 伞形下的 feedback 域实例且「埋点」消歧指向伞形定义。

---

### Edge Cases

- **engine handler 的 action 引用不存在的 action** → `--validate` exit 2，指名 handler_id 与非法 action。
- **handler 的 behavior_owner 路径不可达（错误/缺失/拼写）** → validate exit 2 指名不可达路径（与非法 action 同级，指针腐化禁止静默）。
- **同一单元同一生命周期点两条 binding 的 order 值相同** → validate exit 2（order 在生效 binding 集内必须唯一；编译期消歧等于引入隐式次序，禁止）。
- **外部 probe（`ext-` 前缀，宿主自定义单元）**：其单元不在框架模板/技能面内 → compile 跳过并在输出中披露 skipped 清单，不报错。
- **用户手工编辑编译产物** → AUTO-GENERATED 横幅 + 既有 regen 先例语义（regen 覆盖，编辑丢失即用户责任）；对账测试对"产物 ≠ 编译重跑结果"转红。
- **单元同时命中 `@point` selector 与逐 object binding** → 合并去重（同一 handler 只出现一次），order 决定位置。
- **`BLOCKING_PATTERNS` 未来扩充命中生成措辞** → 门控扫描/措辞契约转红（编译措辞面被测试钉住，非豁免）。
- **feedback-utils.py 抽出动作后旧调用方**（契约测试、docs 中记载的 CLI 形态）→ 引擎动作封闭集契约同步修订；`feedback-utils.py` 保留的领域动作行为逐字节不变。
- **技能 runtime-mode gate**：编译产物必须保留 gate 判定结构，使非 Spec Kit 项目运行时反馈链路按既有语义跳过。

## Requirements *(mandatory)*

### Functional Requirements

#### 术语与真源扩格（US1）

- **FR-001**: `shared/definitions/probe-definitions.md` MUST 扩格为全框架 Probe 真源（伞形）：既有 Feedback Probe 6 Class / 72 Object 语义与行序不变；Slices 启用 `scripts` 切片；文件头部声明伞形定位与 Feedback Probe 的域实例关系。
- **FR-002**: 050 升级探测（P1–P5）、运行判定（四轴 + session store / evidence lane 两个可用性探测）、证据引擎 lane 探测（probe_node / probe_session_store / probe_platforms）MUST 各以新 Probe Class + Object 行入册，每行携带代码锚点（函数/常量名）；五特征完备性校验沿用 041 C-2。
- **FR-003**: 新增 Object 的代码锚点 MUST 由契约测试与源码双向对账（锚点在源码中存在；源码具名探测在注册表中有行）；对账 MUST 经变异演练证明能红。
- **FR-004**: 真源 MUST 新增「非实体 probe 目录」一节：纯指针形态收录 code-internal 微探针（writability / probe-links / git probe / 会话分析平台预读 / clause mutual-exclusion / read-only probe 等），每条目 = 路径 + 一行语义；目录 MUST NOT 复述行为规则，MUST NOT 参与任何对账计数。

#### Handler 实体与 Binding（US2）

- **FR-005**: Handler schema MUST 为六字段封闭集：`handler_id`（全局唯一，[[STR-004]] 前缀）、`kind`（`engine`/`agent`/`gate`）、`action`、`mode`（`non-blocking`/`blocking`，缺省 `non-blocking`）、`order`、`behavior_owner`（行为真源路径指针）。注册表 MUST NOT 复述 behavior_owner 的行为规则（One Source Of Truth）。
- **FR-006**: HandlerBinding MUST 以 selector 声明订阅：`@point:<lifecycle_point>` + `scope`（`complex-commands`/`skills`/`all`），或逐 `object_id`；per-unit 覆盖（排除/变体）MUST 显式登记。`@point:` 为注册表字面 selector 语法，`lifecycle_point` 值域为封闭集 `wrap-up`/`situation`/`phase-boundary`/`confirm-gate`（Q4 裁定）。一个 Probe Object MUST 可被多个 Binding 订阅（1 ⇒ N）；每个 Binding 恰指一个 Handler。Binding 身份 = (`handler_id`, `selector`, `scope`) 三元组，validate MUST 拒绝完全重复的 Binding；同一 Handler 经多条 selector 命中同一单元同一生命周期点时 MUST 合并为单一编译条目（位于该 Handler 自身的 order 位置），order 冲突错误仅适用于不同 Handler（order 载于 Handler，见 FR-005）。
- **FR-007**: kind=engine 的 action MUST 引用真实引擎 action（封闭集对账）；kind=agent 的 action MUST 是行为真源锚点；kind=gate MUST 对应 confirmation-gates.md 治理条目。任一 Handler 的 behavior_owner 路径 MUST 可达（validate exit 2 指名不可达路径，与非法 action 同级）。
- **FR-008**: MVP 首批 handler MUST 至少含 h-run-determination（engine）、h-feedback-record（engine）、h-threshold-notice（agent）、h-token-reflection（agent）、h-docs-sync-eval（agent），全部绑定 `@point:wrap-up`；生效次序 MUST 保证 h-run-determination 先于 h-feedback-record 与 h-threshold-notice。

#### 共享引擎与编译（US2/US3）

- **FR-009**: 新建共享引擎 [[STR-002]]（stdlib-only，双镜像同 feedback-utils.py 分布），承载自 `feedback-utils.py` 抽出的 probe 族动作——`probes`/`map`/`probe-inject` 三个 action（`--validate`/`--reconcile` 为 `probes` 的 flag；引擎实测修正澄清前的列举口径），行为不变——与新动作（handlers 列表/过滤/validate、[[STR-003]]）；`feedback-utils.py` 保留 feedback 领域动作，其 action 封闭集契约 MUST 同步修订。外部 probe 存储目录（`.specify/memory/feedback/probes/`）仍归 feedback 域，[[STR-002]] 仅读写，零迁移。
- **FR-010**: [[STR-003]] MUST 从真源渲染每单元单一收尾段（[[STR-001]]，AUTO-GENERATED 横幅标记）：按 order 顶序列出该单元生效 handler 的调用形式；调用形式按 kind 固定派生（Q4 裁定）——kind=engine 渲染一行 CLI 调用（引擎文件 + action），kind=agent 渲染一行行为真源锚点引用（behavior_owner 路径 + 锚点名），kind=gate 渲染一行治理条目引用（confirmation-gates.md 条目）；真源未变时两次编译逐字节一致（041 C-6 同型派生不变量）。收尾段标题取新段名 [[STR-001]]（Clarifications Q1 裁定）：041 C-5 对账与既有契约测试的标题钉点 MUST 在同一变更内迁移。
- **FR-011**: 编译写入 templates/ 与 skills/ 源面后，产物传播 MUST 走既有 `regen-command-copies.py` 与 `sync-mirrors.py` 机制，执行次序固定为 compile → regen → sync（contract test 钉住次序）；MUST NOT 新建传播器。
- **FR-012**: [[STR-002]] 的 `--action handlers` MUST 支持列表与按 point/scope/kind/mode 过滤及 `--validate`；其 `--action probes` MUST 覆盖新 Class 的查询。[[STR-003]] MUST 提供 `--check` 漂移预检模式并原子写产物（与 regen-command-copies.py / sync-mirrors.py 姊妹机制同型，drift exit 1）。查询面（probes / handlers 列表）对宿主项目只读可用，注册与编译写面仅框架真源侧（Q6 裁定，见 FR-021）。

#### 语义保持与预算（US3/US4）

- **FR-013**: 迁移 MUST 实现五项语义零回退：threshold 提示永不阻塞、agent 自省 never solicit、外部 probe 本地隔离不上送、技能 runtime-mode gate、简单命令排除集（agents/constitution/feature）——全部由既有契约测试继续钉住，零新增失败。
- **FR-014**: 次序依赖 MUST 由 order 字段声明并经契约测试钉住（h-run-determination 在前，阈值提示消费其判定结果）。
- **FR-015**: 一切生成措辞 MUST 零 `BLOCKING_PATTERNS` 命中；门控扫描 MUST 保持 total 23 / violations 0（预算整数余量 0，不得以改 baseline 换通过）。
- **FR-016**: 迁移完成态：凡存在收尾段的单元，该段必为编译产出（[[STR-001]] 为唯一形态）；手工 `## Feedback` 嵌入段与 docs-sync 手工段在源模板面清零；零生效 handler 的单元不输出收尾段（Q5 裁定，简单命令与外部单元保持现状无段形态）。

#### 对账、二期与词汇表（US4/US5）

- **FR-017**: 编译产物（[[STR-003]] 输出）↔ 真源 MUST 双向零缺漏（孤儿 handler、缺失 handler、非法 action、order 冲突均为 exit 2 错误）；对账复用并扩展 041 C-5 的嵌入点对账机制。
- **FR-018**: 二期 binding（situation / phase-boundary / confirm-gate）入册后 MUST 走与 US3 相同的编译/对账规则；confirm-gate 的 19 个既有 Object 挂 h-gate-evidence，044 门控证据契约零回退。
- **FR-019**: 词汇表 MUST 新增三个术语：Probe（伞形）、Handler、HandlerBinding（origin=auto, status=proposed 起步）；既有 Probe Class 与 Probe Object 条目 MUST 随伞形落定改写（当前表述自定义为 Feedback Probe 的两层，改写为伞形的两层）；Feedback Probe 条目 MUST 改写为伞形下的域实例表述；「埋点」消歧条目 MUST 重写指向伞形定义。
- **FR-020**: 行为真源文件（feedback-step.md / docs-step.md / proactive-trigger.md）的**行为规则** MUST 保持不动；其嵌入位置、段标题等**接线引用类字面量** MUST 随收尾段标题迁移同步更新（Q3 裁定：冻结不适用于接线指针——标题迁移必然触及 feedback-step.md 嵌入参考形态与 docs-step.md 放置行，二者不能同时成立，已裁决接线编辑胜出）。
- **FR-021**: 宿主项目（客户项目）对 probe/handler 体系的访问面为**只读**（Q6 裁定）：MAY 运行 [[STR-002]] 查询面（probes / handlers 列表）回答"本安装面有哪些探测点与 handler"；MUST NOT 获得 Handler/HandlerBinding 注册或编译写面——注册仅框架真源侧，宿主扩展留作 Future Evolution 记入 Feature 详情文件。
- **FR-022**: `docs/reference/` 的 probe 体系文档 MUST 更新（伞形模型、handlers CLI、编译流程）。

### Key Entities *(include if requirement involves data)*

- **Probe Class / Probe Object**（既有）：定义与真源见 `shared/definitions/probe-definitions.md`；本特性扩格其伞形定位并新增 engine 侧 Class，不改动既有行语义。
- **Handler**（新概念，无既有 owner——真源落扩格后真源的新节）：一类可复用反应的定义；六字段 schema 见 FR-005。
- **HandlerBinding**（新概念，同上）：探测点 → Handler 的订阅关系；selector + scope + per-unit 覆盖，见 FR-006。
- **Compiled Wrap-up Section**（派生物，非独立维护实体）：`compile-embeds` 的每单元输出；字节确定、可重建，见 FR-010。
- **Non-entity Probe Catalog entry**：非实体微探针的指针条目，见 FR-004。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 单次 `--action probes` 调用列出跨域 probe 清单（既有 feedback 6 Class/72 Object + 新 engine 侧 Class/Object），`--validate` exit 0。
- **SC-002**: 新增一个 wrap-up 反应的接线成本 = 真源注册行 + 重编译，模板源文件触碰数为 **0**（对比基线：今日同类变更加一个机制需触碰全部 23 命令模板 + 传播副本）。
- **SC-003**: 编译产物字节确定且与真源零漂移：两次重建逐字节一致；五类破损场景（孤儿/缺失/非法 action/措辞命中/order 颠倒）各自使对账转红（变异演练取证）。
- **SC-004**: 语义保持：迁移前后既有契约测试零新增失败，FR-013 五项语义逐项由具名既有测试继续覆盖。
- **SC-005**: 门控预算零扰动：`scan-confirmation-gates.py` total 23 / violations 0 保持不变。
- **SC-006**: engine handler 的 action 引用与两个引擎真实 action 封闭集双向一致（import 对账，053 先例）。
- **SC-007**: Token 中性偏优：迁移后命令模板收尾面的样板行数 ≤ 迁移前（`## Feedback` + docs-sync 两段合计）。
- **SC-008**: 非实体 probe 目录存在、纯指针（零行为复述），且不参与任何对账计数。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 实现后运行 `probe-utils.py --action probes --validate`（对照迁移前 `feedback-utils.py --action probes --validate` 输出 6/72 基线）；频次 = 实现期 + 回归。
- **SC-002 Source**: 测试内演示性注册临时 handler + binding 后运行 compile-embeds，`git diff --stat` 对**模板面全路径集**（templates/ + skills/ 源面及全部镜像/工具副本面）计数为 0；频次 = 契约测试常驻。
- **SC-003 Source**: 契约测试（编译幂等断言 + 五类破损变异用例）；频次 = 每次真源或编译器变更。
- **SC-004 Source**: 迁移前后全量 pytest 名字级 `comm -13` 为空（零新增失败）+ FR-013 五项的具名测试清单核对；频次 = 每个 phase 边界。
- **SC-005 Source**: `scan-confirmation-gates.py` 输出与迁移前实测值（total 23 / violations 0）比对；频次 = 每个 phase 边界。
- **SC-006 Source**: 契约测试 import 两引擎 action 枚举与真源 handler 行双向集合相等；频次 = 每次引擎变更。
- **SC-007 Source**: 计数规则 = 收尾面**非空行数**（`## Feedback` + docs-sync 两段合计 vs [[STR-001]] 单段，源模板面）；迁移前数值冻结于 plan.md 具名小节（格式仿 044 基线先例）；频次 = 一次性（迁移完成时）。
- **SC-008 Source**: 真源目录节检查（条目形态 = 路径 + 一行语义）+ 对账计数排除断言；频次 = 契约测试常驻。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `## Wrap-up` | FR-010, FR-016, contracts（编译产物段标题；命名受 Clarifications Q1 裁定约束） |
| `STR-002` | `probe-utils.py` | FR-009, FR-012, contracts, tasks（共享引擎文件名） |
| `STR-003` | `--action compile-embeds` | FR-009, FR-010, FR-017, contracts, tasks（编译动作 CLI 形态） |
| `STR-004` | `h-` | FR-005, contracts（handler_id 前缀） |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

- Q1: 编译产物收尾段的标题用什么？（现状 wrap-up 反应由 `## Feedback` + docs-sync 两个手工段承载，041 C-5 对账与多个契约测试钉在 `## Feedback` 标题上） → A: 新段名 `## Wrap-up`（[[STR-001]]）——收尾段承载 N 个 handler，语义不只 feedback；标题钉点的迁移在本特性同一变更内完成（用户裁定，2026-10-13）。

### Session 2026-10-13

- Q2: 特性 056 绑定到哪个 Feature（Related Feature 解析）？ → A: **新建 Feature 056**（伞形：Probe / Handler / HandlerBinding 基础设施）——无既有 Feature 以全框架 probe 基础设施为 scope；028 是 feedback 域（其 sibling specs 吸收的均为 feedback 工作），绑定 028 会与 FR-019「Feedback Probe 降为域实例」的归属方向矛盾；050 的 scope 是主动触发本身。注册表义务：新增 Draft 行 + 详情文件 + 028 反向交叉引用。
- Q3: FR-020 行为真源冻结与标题迁移冲突（feedback-step.md 嵌入参考形态、docs-step.md 放置行都钉着 `## Feedback` 字面量，与「MUST 保持不动」不能同时成立）？ → A: 修订 FR-020——行为规则不动，**接线引用类最小编辑允许**；冻结条款改写为行为规则维度的冻结。
- Q4: 编译产物中 handler「调用形式」如何从六字段 schema 派生？ → A: **按 kind 固定形态**——engine→CLI 调用行（引擎文件+action）、agent→行为真源锚点引用行、gate→治理条目引用行；零 schema 变更。同时裁定 `@point:` 为字面 selector 语法，lifecycle_point 值域封闭集 {wrap-up, situation, phase-boundary, confirm-gate}。
- Q5: 零生效 handler 的单元（简单命令 agents/constitution/feature、外部 probe 单元）编译输出空段还是无段？ → A: **不输出段**——与现状一致（这些单元本无嵌入段），041 C-5 嵌入计数语义零变化；FR-016 改写为「凡存在收尾段必为编译产出」。
- Q6: 宿主项目注册 Handler 在本特性范围内吗（Overview 曾把"无法被客户项目扩展"列为痛点）？ → A: **宿主只读**——宿主 MAY 运行查询面（probes / handlers 列表），MUST NOT 获得注册/编译写面；新增 FR-021；宿主 handler 注册留作 Future Evolution 记入 Feature 详情文件。
