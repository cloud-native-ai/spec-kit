# Requirements Specification: Prompt Adherence Evaluation — 提示遵从度评价（Prompt Adherence Evaluation）

**Requirement Branch**: `109-prompt-adherence`
**Created**: 2026-11-27
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（需要判定「两个提示层的既有记录究竟证明了什么、证明不了什么、每条结论的来源在哪」的人）与下游客户项目维护者（在本地用一次只读调用判断「发给智能体的规则是否在生效、哪些行为根本没有传感器」的人）；读者基准沿用 `.specify/shared/guidelines/user-facing-comprehension.md` 的全局基准读者，不新建
**Reading scenario**: 当需要判定「宿主提示层与项目规则文件层各自被哪些既有传感器覆盖、覆盖不到的行为叫什么」「一次运行的遵从读取包含哪些字段、依据什么来源、缺席时说什么」「纵向窗口怎样取数、边界如何归属」「封闭词表住在哪里、含义由谁拥有」「只读包含性声明如何判定、如何测试」时打开本规格，据 FR-001…FR-030 与 SC-001…SC-009 放行 `/speckit.clarify` 与后续规划
**Input**: User description: "对比一下最近两天本项目和/storage/project/cloud-native-ai/ai-harness中的修改, 进行查缺补漏（范围裁定）需要进行特性级别的双向同步, speckit以稳定为第一优先级,因此不需要引入过于激进的架构变更。（决策治理裁定）spec-kit 107 与 ai-harness 091 各自独立演进,仅仅互做参考而不是互相对齐。"

**输入校正**：本特性的直接输入是 ai-harness 已关闭能力 `092-prompt-adherence`（其 Feature 097）向 Spec Kit 的**加法式移植**；用户请求中的「双向同步 / 查缺补漏」按「以 ai-harness 为能力拥有方，把该能力完整适配到本树」理解，未列出的其它差异不进入本切片。移植的命名适配规则见 A-3，路径适配逐条实测见 A-4；`092` 的 `Related Feature 097` 是 ai-harness 注册表编号，本规格不复用，绑定本树 Feature 109（A-2）。`spec-kit 107`（decision governance）与 `ai-harness 091` 各自独立，本特性只按引用抵达、不对齐、不改动（A-16）。

## Related Feature *(mandatory)*

**Feature ID**: 109
**Feature Name**: Prompt Adherence Evaluation（提示遵从度评价）
**Binding basis**: 这是一个**新的独立特性**（不是既有 spec-kit 能力的派生切片，也不绑定 092 在 ai-harness 的 Feature 097）。候选复用扫描：069 probe system 拥有 probe 注册表读取与 Wired 状态语义、091/059 exec-quant 拥有执行量化记录、093 feedback 拥有反馈存储与红线、080/run-determination 拥有四轴判定记录、105 runtime store layout 拥有运行期存储根清单、106 evidence lanes 拥有证据通道——它们都是本特性的**传感器所有者**，没有一个是「对两个提示层做遵从读取」的机制；既有 owner 保持不动，本特性只读消费。特性详情文件与 `.specify/features.md` 索引行的登记由 `/speckit.clarify` 按 Feature Integration Protocol 完成；本阶段只在本规格内绑定编号，不编辑注册表（A-2）。

## Overview

本框架的每一项机制——SDD 链、工作流门、fast-fail、证据纪律、确认门、技能与命令——都建立在同一条前提上：智能体**确实遵从**了它收到的提示。该前提有两层：

- **宿主提示层（宿主提示层）**：运行期拥有（runtime-owned）的提示面——智能体 CLI 自身的系统提示加上用户的直接提示。本框架不编写它；它是整个 harness 依赖的环境前提。
- **项目规则文件层（项目规则文件层）**：本框架发布的指令面——`.specify/instructions.md` 及其 `AGENTS.md` / `CLAUDE.md` / `QODER.md` / `.github/copilot-instructions.md` 兼容符号链接；自定义 harness 通过它抵达智能体。

两层中的失败从外面看是同一种现象：「规则从未送达」「规则送达后被忽略」「宿主根本没有呈现规则文件」都表现为「规则没有生效」。本框架此前从未把这条前提作为一个整体审查，因此这些失败模式被静默混同。

本特性构建**提示遵从度评价机制（prompt adherence evaluation mechanism）**：一种确定、可审计、可离线的方式，回答「既有传感器对每一层说了什么、说不了什么、每条结论来自哪里」。它只消费**已经存在**的传感器——feedback 条目（含门控观察）、exec-quant 记录与 measure 报告的读取面、run-determination 四轴记录、evidence findings、probe 注册表声明、以及仅在持久化时才算数的 instructions reconcile 观察——不新增存储、不新增采集点、不修改任何既有记录 schema。每次读取都是**读时重建的投影**：按运行（一次运行的记录能证明什么）与纵向（显式窗口内的状态计数）两种形态，都可仅凭源引用重放。

机制的用途只有一个：帮助 Spec Kit 更好地集成进客户项目——**可分发**（经既有 publish → install → init 流程）、**可离线**（零传输）、**可审计**（来自被引用记录）、**确定性优先**（由程序、而非 LLM，产出读取）。它的第一份产出同时就是完成的前提审查：一张「假定行为 → 传感器或盲区」的覆盖图，使「未被观察的行为」被如实命名，而不是被误当成成立的前提。

机制**不是**什么：不是评分系统、成熟度报告、运行期评价平台或新台账。它只产出封闭状态观察与覆盖计数，绝不产出复合遵从分、排名或跨项目比较；缺席的传感器读作 `not evaluated` / `Unobserved`，绝不读作「干净」。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **类别判定 = `execution`**：主交付物是机制本身（owner 文档、声明值域、只读读取引擎、守卫），验收由机器执行与断言。 | 按验收 oracle 判定；四元组 `flow_class=execution; source=default; marker=; error=owner-unavailable` 记录于本阶段派发。 |
| **A-2** | **特性身份 = 新 Feature 109**：独立特性，不复用 ai-harness 的 Feature 097，也不派生自任何既有 spec-kit 特性；索引/详情登记移交 `/speckit.clarify`，本阶段不编辑 `.specify/features.md` / `.specify/features/`。 | 用户范围裁定要求特性级移植；移植产物在本树是首次出现，既有 owner 只被消费。 |
| **A-3** | **命名与路径适配**：`.ah/` → `.specify/`；`/ah.*` → `/speckit.*`；`ai-harness`（产品）→ Spec Kit / `specify` CLI；`ai-harness init` → `specify init`；记录 kind 令牌 `ah.exec-quant` / `ah.evidence-findings` → `speckit.exec-quant` / `speckit.evidence-findings`；源工具的 Python 包目录映射到本树 `src/specify_cli`（本特性不引用该路径，故不写法字面量）。**逐条实测**：owner 文档、五个声明事实、`scripts/python/prompt-adherence.py`、六个读面（`run-determination.py`、`exec-quant.py`、`feedback-utils.py`、`evidence-utils.py`、`probe-utils.py`、`declaration_reader.py`）、`shared/declarations/facts/runtime-store-layout.yaml`、`shared/workflow/symlink-model.md`、`shared/guidelines/better-harness.md`、`shared/guidelines/confirmation-gates.md`、`shared/definitions/script-interface-definitions.md`、`scripts/bash/run-tests.sh`、`scripts/python/sync-mirrors.py` 在本树全部存在（证据：`test-evidence/requirements-stage-2026-11-27.md` § R-1）。 | 移植不得复制未解析的源命名。 |
| **A-4** | **读面等价已验证**：六个传感器的读取 API 与记录字段在本树逐项核对——`load_determinations`（`run_id` / `determined_at` / `SCHEMA_VERSION=1`）、`load_records`（`kind` / `schema_version=2`（owner `quant-record-schema.yaml`）/ `run_id` / `collected_at`）、`scan_entries`（仅 frontmatter 元数据：`id` / `run_id` / `created` / `file`）、`load_index` + `FINDINGS_KIND` / `SCHEMA_VERSION=1` / `FINDINGS_PROJECTION_FIELDS`（`runId` / manifest `created`）、`load_probe_registry`（`PROBE_DEFS_REL = .specify/shared/definitions/probe-definitions.md`）；门控族前缀在本树 `shared/guidelines/confirmation-gates.md` 第 93 行仍为 `gate:<gate_id>:<UTC ts>`。证据同 A-3。 | 「只消费既有传感器」必须逐面可核对，不能按源文假定。 |
| **A-5** | **存储布局读取面适配（有意偏离源实现）**：源引擎经 `scripts/python/store_layout.py` 读运行时存储布局；**本树没有该模块**，且本树 `runtime-store-layout.yaml` 的 `stores.*` **不含 `root` 键**——根路径是 `.specify/<store-name>/` 投影。本移植改为经 `declaration_reader.py` 直接读该事实（既有先例：`concurrency-check.py`、`sanitize-utils.py`、`seal-utils.py`），由声明的 store 名派生根集合；引擎 MUST NOT 新增第二张根表。语义由 FR-030 承载。 | 保留同一「根集合 = 声明」语义，不引入源模块的镜像副本，符合加法式与 One Source Of Truth。 |
| **A-6** | **不新增运行期存储**：读取全部读时派生，不新增 store root、记录类型、采集点或 schema；`runtime-store-layout.yaml` 不被本特性修改。判定依据：机制的每个输出都由既有记录重算，缓存/索引只会制造第二个事实源。 | FR-005 / FR-006 的显式裁决；并发开发安全要求也不允许新的共享可写聚合。 |
| **A-7** | **分发面**：owner 文档（`shared/`）、五个声明事实（`shared/declarations/facts/`）、引擎（`scripts/`）都随既有镜像对 `scripts → .specify/scripts`、`shared → .specify/shared`（`sync-mirrors.py` `MIRROR_PAIRS`）投影，并由 `specify init` 的 `shared/` + `scripts/` 拷贝进入客户项目；`templates/` 无本特性内容。框架地图新增**两行**：owner 文档行与读取入口行（源 092 先例；本树地图此前不为单个引擎立行，这两行是本能力发现性所需，属本特性专属增量）。测试与 fixtures 是**仓内开发资产**，不分发。 | publish → install → init 是唯一分发路径；镜像生成、不手改。 |
| **A-8** | **tasks-template 改动不随本特性移植**：源提交 `94f77ee` 对 `templates/tasks-template.md` 的改动（`[~]` 行必须带 `<!-- deferred: <reason> -->` 行内标记、GATE-3 覆盖 `[~]`）是其 analyze 轮次发现的**框架根因修复**，属「任务模板/延期纪律」这条独立惯例线，与提示遵从度语义无关。本树模板仍是旧措辞（「ideally」）；该差异作为跨线观察记录，本特性 MUST NOT 导入。 | brief 明示「不导入无关改动」；把无关改动塞进能力移植会破坏归因。 |
| **A-9** | **基线读取 = 必须**：本特性线 MUST 产出一份本仓库的日期化基线读取，经既有渠道（feedback 条目或 evidence 记录）落盘，带显式未观察行、可凭自身引用重放、不声称改进。选择「有基线」而非「基线缺席直到积累记录」：关闭判据（SC-008）与源能力的落地形态都要求首份基线，且它本身是「缺席如实」的首次示范。 | 首份基线同时是机制的首个真实读数与可重放样例。 |
| **A-10** | **观察状态 = 既有七态 + `not_evaluated` 组合**：七态由 `evidence-utils.py` 从 `shared/declarations/facts/evidence-seven-states.yaml#/statement` 读出；`not_evaluated` 取自 run-determination 的判定值域。**不设第六个声明事实**。 | 中文四值域（`adherent`/`deviant`/`unobserved`/`not-evaluated`）被否决：`adherent` 无法在不违反 FR-011/FR-010 的前提下导出，`deviant` 会与 FR-012 冲突。 |
| **A-11** | **不做复合评分（承重决策）**：备选 (a) 每层一个数值分与阈值；(b) 封闭状态观察 + 覆盖 + 状态计数；(c) 不提供读取面。取 (b)。反命题：单一数字更易比较，但没有经过验证的信号-结果联系会让比较指数诱发证据无法支撑的决策（预期反指标：分数被用于跨项目排序）。判别证据：七态证据纪律禁止把 `Unobserved` 折算成值；better-harness 边界禁止新的评分系统与成熟度报告。重开条件：出现日期化前后对照研究证明复合指标改变决策，或用户明确要求排名指标——两者都需新决策与新规格，不是本文件的编辑。 | 记录反命题、判别证据、预期反指标与重开条件（decision-tension 形态）。 |
| **A-12** | **窗口语义**：纵向窗口为显式、半开 `[since, until)`，按每条记录**自身声明的时间戳字段**；省略的边界打印为字面量 `open`（不解析成时钟读数）；默认范围是目录内观测到的**最近运行身份**，不是全时窗。排序与重复处理被声明并被测试（FR-016）。 | 确定性要求：相同输入与相同机制版本必须复现相同输出。 |
| **A-13** | **脚手架偏差（披露）**：当前工作树已处于分支 `109-prompt-adherence`，`create-new-requirements.sh` 会把该分支计入编号空间并派生 110 且新建分支，与本线「停留在既有分支、编号 109」冲突；按 108 A-16 先例，本阶段**手工**从 `.specify/templates/requirements-template.md` 脚手架到 `.specify/specs/109-prompt-adherence/requirements.md`，脚本的模板拷贝步骤等价复刻，仅跳过其编号派生与建分支步骤。 | 工作树拓扑与脚本的编号派生假设不兼容；照抄脚本会制造第二分支并改号。 |
| **A-14** | **词汇表增量延后**：本特性引入的项目域术语——提示遵从度（Prompt Adherence）、宿主提示层（Host Prompt Layer）、项目规则文件层（Project Rule File Layer）——按 glossary 协议应作为 `origin=auto` / `status=proposed` 提案；本阶段按「仅本特性器物」范围只记录提案内容于本表，实际登记交由后续阶段/收尾执行（`glossary-utils.py --action add`）。 | 本阶段不改动项目级词汇表注册面；提案不丢失。 |
| **A-15** | **宿主层观察仅作框架集成输入**：宿主层读数只服务本框架的集成决策，绝不包装成关于宿主产品的反馈；feedback 目标仍是 Spec Kit 框架自身（owner：`shared/workflow/feedback-step.md`，按引用不动）。 | 源 FR-027 的边界，原样保留。 |
| **A-16** | **纯消费者 / 加法式**：不修改任何既有引擎的行为、记录 schema、值域、红线、运行期存储布局（105）或决策治理（107，独立演进，只作参考）；本特性是纯读取方。发现需要新字段时，记为对应 owner 的开放项，不在本特性打补丁。 | 用户稳定性裁定：不引入激进架构变更。 |
| **A-17** | **语言与读者**：正文以中文为主、核心概念带双语定义（与 108 及 `shared/guidelines/bilingual-expression.md` 一致）；所有领域术语要么在 owner 处以指针抵达，要么在本规格定义处带双语形态。 | 最新合并规格的语言惯例 + 用户可理解性纪律。 |
| **A-18** | **单次调用入口**：`python3 .specify/scripts/python/prompt-adherence.py`（框架源 `scripts/python/prompt-adherence.py`）；本版本不发布 `/speckit.*` 命令或 skill 包装器；发现性是框架地图行加 owner 文档 § Entry。 | 源 FR-023/A7 的原样保留；包装器是未来独立决策。 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一次诚实的按运行遵从读取 (Priority: P1)

框架维护者或客户项目所有者完成了一次运行，想知道两层提示的证据究竟说了什么。一次有文档的调用返回一份读取：封闭信号目录中的每一行各一条观察，带证据状态、它来自的源记录，以及——在没有任何可观察内容时——原因。没有任何评分；没有超出被引用记录的推断；再次运行返回同一份读取。

**Why this priority**: 这是机制的核心能力。没有确定、可溯源引用的按运行读取，其余承诺（纵向视图、前提审查、客户采用）都无从组合。

**Independent Test**: 一个覆盖全部目录行的种子 fixture 产出预期读取，连续两次运行逐字段相同；删掉某一行的记录后，恰好该行变成带原因的 `not evaluated` 条目。

**Acceptance Scenarios**:

1. **Given** 一个覆盖每个目录行的 fixture store，**When** 按运行读取运行，**Then** 每个目录行恰好出现一次，带证据状态与可解析源引用。
2. **Given** 同一 fixture，**When** 读取运行两次，**Then** 两份输出逐字段完全相同，包括顺序与窗口算术。
3. **Given** 某目录行没有匹配记录的 fixture，**Then** 该行报告 `not evaluated` / `Unobserved` 与原因、不带裁决，其余行保持已评价。

---

### User Story 2 - 前提被审查、盲区被点名 (Priority: P1)

审查者打开 owner 定义文档，看到前提链被分解为具名假定行为——「宿主呈现项目规则文件」「智能体遵从被呈现的门规则」等等。每条假定行为映射到恰好一个目录行（观察它的传感器）或恰好一个盲区条目（今天没有持久化传感器观察它）。机器检查强制执行该映射，使一个假定无法悄悄算作成立。

**Why this priority**: 本特性存在的理由就是这条前提从未被整体审查。一个从未接上假定的传感器，或一个悄悄借用邻近传感器可信度的假定，会在新机制内部复现原缺陷。

**Independent Test**: 对 owner 文档运行覆盖图检查：每条假定行为都解析到恰好一个传感器或盲区条目，每个传感器条目都解析到目录行 id，且每个目录行都至少被一条假定行为引用。

**Acceptance Scenarios**:

1. **Given** owner 文档，**When** 覆盖图检查运行，**Then** 每条假定行为映射到恰好一个传感器或盲区条目，每个传感器条目解析到既有目录行 id。
2. **Given** 一条没有持久化传感器观察的假定（例如宿主系统提示的原始文本），**Then** 它列于盲区登记，并在每次读取的覆盖节中以不可观察出现。

---

### User Story 3 - 客户项目在本地、离线、无新存储地读取遵从度 (Priority: P1)

一个由本框架初始化出的客户项目想在自己机器上判断：发给它的规则是否在生效。有文档的调用在该项目运行，无需框架维护者参与：它读取项目既有本地存储，不写任何文件、不访问网络、不传输任何内容，也不复现任何原始用户文本。在记录尚不存在的地方，读取明确说明，而不是看起来干净。

**Why this priority**: 向客户项目分发——离线、私有、无需管理新存储——是特性申明的主题与目标；只在框架仓库内可用的机制达不到它。

**Independent Test**: 一个新初始化、无任何记录的项目完成读取并给出显式 `not evaluated` 行；同一离线环境下有数据的 fixture 产出完整读取；覆盖运行期存储布局所辖根集合的哈希清单在两次运行前后不变。

**Acceptance Scenarios**:

1. **Given** 一个刚初始化、无运行期记录的项目，**When** 读取运行，**Then** 它以显式的不可用 / `not evaluated` 行与有文档的退出码完成，且绝不报告干净结果。
2. **Given** 一个有数据的项目与不可用的网络，**When** 读取运行，**Then** 它在无网络访问下成功，且不在受管存储根下写任何内容（允许增量：无）。
3. **Given** 一个在记录字段中嵌入用户散文的存储，**Then** 读取输出只携带结构化字段、封闭令牌与源引用——没有原始用户文本。

---

### User Story 4 - 读时重建的纵向读取 (Priority: P2)

维护者想看跨多次运行、多个单元的视图，因为一次运行无法判定一条前提。一个显式窗口产出每个目录行的状态计数加覆盖行——多少记录可观察、多少缺席、哪些盲区适用——输出有界。不持久化任何内容，也不对项目、智能体或用户排名。

**Why this priority**: 纵向视图是遵从证据变得有意义的地方，但它是按运行路径之上的组合并依赖它；它是 P2 是依赖关系，不是价值关系。

**Independent Test**: 一个多次运行的 fixture 对给定窗口产出预期状态计数；两个相交窗口仅在边界不同处不同；运行后存储树不变。

**Acceptance Scenarios**:

1. **Given** 跨多次运行的记录，**When** 窗口读取运行，**Then** 每行报告各证据状态的计数加覆盖行，且不出现按项目、按智能体或按用户的排名。
2. **Given** 窗口边界恰好落在记录时间戳上，**Then** 半开区间规则按声明适用，且两个边界出现在输出中。

---

### User Story 5 - 负面读数只做咨询、进入既有流程 (Priority: P3)

读取暴露一个负面观察——比如门控观察的决策被反复修改，或某通道从未变得可观察。读取本身不改变任何东西、也不授权任何行动。如果用户或智能体决定采取行动，发现经既有载体流转（feedback 条目、寄存的 TODO 或新规格）；值得保留的读取经既有渠道记为一条日期化记录，源引用原样保留。

**Why this priority**: 闭环重要，但它复用既有改进路径，且不得成为自动变更；它是 P3，因为读取在没有它时依然有价值。

**Independent Test**: 产生负面观察的 fixture 在读取后存储树不变；经既有 feedback 引擎的显式跟进创建一条普通条目；任何地方都不出现新的存储根或聚合。

**Acceptance Scenarios**:

1. **Given** 报告负面状态的读取，**Then** 读取不写任何内容，也不产生自动处置、阈值或变更。
2. **Given** 用户要求保留读取，**Then** 它经既有渠道落为一条日期化记录，源引用完整，且不作为新聚合可查询。

---

### Edge Cases

- **完全没有存储根（全新项目）**：读取按每行自身来源分层完成：源存储缺席的行读 `not_evaluated`，cause `source-unavailable` 并带该 store 的理由；`probe-registry-declaration` 行的来源（`probe-definitions.md`）随 init 分发现场存在且非空，因此在全新项目不会读 `not_evaluated`——它对当前状态评价一次并读其 `Wired` 正上限，或在 scope 未匹配时读 `Unobserved`；该行的 `not_evaluated` 只在显式 `--run` 范围下可达。读取带显式 `not_evaluated` / `Unobserved` 行与每 store 的理由，六个目录行全部在场，六个盲区类全部列出，且退出码区分「跑过但无数据」与错误。
- **一个通道不可用而其它通道存在**：逐行可用性；一个传感器缺席绝不导致整体失败。
- **不可解析或违反 schema 的记录**：该记录贡献一条 `invalid source` 观察并点名其路径；读取不崩溃并报告 invalid-source 计数。
- **记录中的未知值令牌**：该记录作为 invalid source 搁置，cause `schema-violation`，按路径在 invalid-source 披露中具名；读取继续，绝不强制转换或猜测。
- **声明、owner 文档表格或引擎参数中的未知值令牌**：硬错误，非零退出，不产出读取——绝不静默转换或猜测。
- **旧 schema 版本写入的记录**：以 `unknown-schema-version` 搁置并给理由；绝不按当前 schema 解释。
- **同一运行身份的重复记录**：以具名 duplicate 计数暴露，绝不静默合并或未披露地重复计数。
- **窗口边界恰好落在记录时间戳上**：声明所载的半开规则适用并被测试。
- **两次并发读取**：两者都只读并产出相同输出；不存在可争用的锁、缓存或共享可变索引。
- **owner 修订重命名或删除目录行**：早先的日期化记录继续作为日期化记录（凭自身引用可重放）；新读取遵循新声明集并盖其版本。
- **宿主从不呈现指令文件**：layer-B 行在该环境自然不可观察，以带原因的 `Unobserved` 出现——绝不作为不遵从，也绝不作为遵从。
- **请求的运行身份不匹配任何记录**：显式的 not-found 状态，区别于「跑过且干净」。
- **运行身份只出现在部分传感器中**：每行从匹配到的存储评价；未匹配的行以 store 理由报告 `not_evaluated`，读取状态为 `partial`。
- **记录时间戳落在声明格式/时区之外**：视为 invalid source，不强制转换。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 前提、层与 owner

- **FR-001**: 框架 MUST 定义唯一一份提示遵从度评价 owner 文档（框架源 `shared/definitions/prompt-adherence-definitions.md`，安装为 `.specify/shared/definitions/prompt-adherence-definitions.md`），拥有：受评价的前提链、双层模型、信号目录（行与准入判据）、读取契约字段含义、盲区登记、本特性红线。任何其他承载这些事实的表面 MUST 指向它；MUST NOT 复述。
- **FR-002**: owner 文档 MUST 定义两层——宿主提示层（宿主提示层，令牌 [[STR-001]] `host-prompt`）与项目规则文件层（项目规则文件层，令牌 [[STR-002]] `project-rules`）：宿主层 = 运行期拥有的提示面（宿主系统提示加用户直接提示），不由本框架编写；项目层 = 本框架发布的指令面（`.specify/instructions.md` 及其 `AGENTS.md` / `CLAUDE.md` / `QODER.md` / `.github/copilot-instructions.md` 兼容符号链接），其事实 owner 仍是 `.specify/shared/workflow/symlink-model.md`。owner 文档 MUST 以引用抵达 `shared/guidelines/better-harness.md` 中宿主与项目 harness 的既有辨析，以及指令面模型；MUST NOT 另立第二份定义。核心概念行 MUST 带双语形态（owner: `shared/guidelines/bilingual-expression.md`）。
- **FR-003**: owner 文档 MUST 承载完成的前提审查：前提链分解为具名假定行为（`AB-NN`，文档序致密），外加一张覆盖图，其中每条假定行为映射到恰好一个目录行或恰好一个盲区条目。映射 MUST 双向机器可检：每个传感器目标解析到目录行 id，每个盲区目标解析到登记 id，每个目录行至少被一条假定行为引用，每个盲区条目至少被一条假定行为引用。检查 MUST 可经 `python3 .specify/scripts/python/prompt-adherence.py --check-coverage` 触达：退出 `0` 零发现，`1` 给排序后的发现列表，`2` owner 文档不可用。
- **FR-004**: 信号类只有同时满足以下全部条件才可进入目录：(a) 既有机制在既有生命周期点产出它并持久化在既有存储中；(b) 携带机器可读源标识；(c) 其含义可由封闭词表或声明推导判定；(d) 声明层候选（host / project / both）与强度（direct / indirect）；(e) 能在证据纪律下诚实表达「不可观察」。不满足 (a) 的信号 MUST 列为盲区；本特性 MUST NOT 通过新采集点合成它。

#### B. 仅传感器摄取、无新存储

- **FR-005**: 机制 MUST 只消费既有传感器已持久化的记录，且每个读面 MUST 经其所有者引擎的读取函数、进程内读取，绝不另写第二解析器：run-determination 记录（`.specify/session/` 中 tag `run-determination` 的记忆条目，经 `run-determination.py` `load_determinations`）；exec-quant 记录（`.specify/exec-quant/`，`kind: speckit.exec-quant`，schema 版本由 `shared/declarations/facts/quant-record-schema.yaml` 声明，经 `exec-quant.py` `load_records`）；feedback 条目（`.specify/feedback/`，仅经 `feedback-utils.py` `scan_entries` 的 frontmatter 元数据面）；evidence findings（`.specify/evidence/`，经 `evidence-utils.py` `load_index` 加 `run-determination.py` 的 `FINDINGS_PROJECTION_FIELDS` 项投影，字段钉在 `FINDINGS_KIND` / `SCHEMA_VERSION` 上）；probe 注册表声明（`.specify/shared/definitions/probe-definitions.md`，经 `probe-utils.py` `load_probe_registry`）。instructions reconcile 观察只在有持久化时才算数——今天没有存储持久化它们，因此它们不是目录行（FR-029）。机制 MUST NOT 引入新存储根、新记录类型、新采集点，或对任何既有记录做 schema 变更。
- **FR-006**: 每次读取 MUST 是读时派生的只读投影。机制 MUST NOT 向任何受管存储写入，MUST NOT 把派生视图缓存为共享状态，MUST NOT 需要锁或可变索引；并发读取 MUST NOT 相互干扰。
- **FR-007**: 既有 owner 与红线 MUST 保持不变：feedback 红线（仅框架自身为目标、用户数据可选、零自动传输）、run-determination 记录 schema 与值域、evidence 七态值域、probe 注册表、measure 报告契约、运行期存储布局（105）、决策治理（107）。新机制是纯消费者。
- **FR-008**: 当一份读取必须为人保留时，它 MUST 经既有渠道（一条 feedback 条目或一条 evidence 记录）落为**一条日期化记录**并携带源引用；MUST NOT 变成可查询聚合或第二存储。

#### C. 层归因与诚实

- **FR-009**: 每个目录行 MUST 在 owner 文档中声明其层候选与强度。读取 MUST 按声明的归因报告每条观察，MUST NOT 在读时给信号重新指派层。
- **FR-010**: 层级陈述 MUST NOT 仅由 indirect 强度行产出。读取 MAY 并列报告 direct 行与 indirect 行，但 MUST NOT 把它们折叠成对该层的一个裁决。
- **FR-011**: 证据缺席 MUST NOT 报告为遵从：无匹配记录的行、不可用的存储、不可解释的记录 MUST 以 `not evaluated` 或 `Unobserved` 出现，并填充 `reason` 字段（观察上的 `{cause, source}`）——绝不如「干净」「合规」或零。
- **FR-012**: 缺席也 MUST NOT 读成违规：缺失的门记录、缺失的 anomaly 行或任何其他缺席 MUST NOT 被推断为违反。违规式代理只有在既有存储记录了事件本身时才可进入目录。
- **FR-013**: 每次读取 MUST 携带覆盖节，说明本范围内哪些目录行可观察、哪些不可观察、哪些盲区适用；覆盖节 MUST 包含全部六个盲区类、范围内记录数与 invalid 记录数。缺少覆盖节的读取无效。

#### D. 读取契约——确定、可审计、封闭

- **FR-014**: 给定范围（运行身份和/或显式时间边界），读面 MUST 产出一份按运行读取，至少包含：读取格式版本（整数）；引擎身份与版本（版本在运行时从最近的 `pyproject.toml` 重新导出）；声明集版本与事实路径（版本 = 五个事实文件的 SHA-256，按排序后的仓库相对路径加字节计算）；范围与窗口；读取状态（封闭字面量之一）；每个目录行恰好一条观察（证据状态、源引用、状态为 `not evaluated` 或 `Unobserved` 时的 `reason`、仅按该行声明导出的偏差类）；覆盖节；invalid-source 与 duplicate 披露。无显式范围时，读取 MUST 解析目录记录中观测到的最近运行身份，并在范围节打印解析出的身份与依据 `{store, path, timestamp}`；当不存在此类记录时，仍 MUST 产出，读取状态 `no-data`。
- **FR-015**: 给定显式窗口，读面 MUST 产出纵向读取：同一契约加每个目录行的按证据状态计数，输出按 token-efficiency 纪律有界，MUST NOT 对项目、智能体或用户排名或比较。窗口按每条记录自身的时间戳字段取半开 `[since, until)`；省略的边界打印为字面量 `open`（绝不解析成时钟读数），使相同记录与相同机制版本复现同一窗口。边界只接受 `YYYY-MM-DD` 或 `YYYY-MM-DDTHH:MM:SSZ`（UTC），非法值退出 2；`--run` 与任一边界同时出现是输入错误。probe 行对当前状态评价一次并在范围说明中标注 window-exempt。
- **FR-016**: 读取 MUST 确定：相同输入记录与相同机制版本产出相同读取，两种输出形态来自同一份计算结构，JSON 以排序键序列化。计算路径 MUST 是确定性程序，绝不是 LLM 组合。顺序、并列决胜、窗口算术与重复处理 MUST 由 owner 或声明层声明并被测试：行按目录声明顺序；源引用按（路径，记录身份）；invalid sources 按路径；duplicates 按（行，身份）；盲区按登记顺序。重复以每行声明的身份字段（加该行声明的 timestamp）为键，每多一次出现计一次并以路径披露——绝不合并、绝不静默重复计数。输出中 MUST NOT 出现时钟或 `generated_at` 字段。输出上限：每观察源引用 20、invalid sources 50、duplicates 20，每次截断带 shown/total 披露；上限是输出界，绝不是判断阈值。
- **FR-017**: 每条观察 MUST 引用可解析的源引用（store、仓库相对 path、record 身份、field），使第三方仅凭引用即可重建该状态。不可解析或未知引用 MUST 以 invalid sources 暴露，绝不静默跳过。
- **FR-018**: 层令牌、强度令牌、目录行 id、偏差类与读取状态字面量 MUST 是封闭集，其值域经共享声明读取器 `scripts/python/declaration_reader.py` 从 `shared/declarations/facts/` 机器读取，含义由 owner 文档拥有。本特性恰好引入五个声明事实，一事实一集合：`prompt-adherence-layers.yaml`（成员 `host-prompt`、`project-rules`）、`prompt-adherence-strengths.yaml`（`direct`、`indirect`）、`prompt-adherence-signals.yaml`（FR-028 的六个行 id）、`prompt-adherence-deviation-classes.yaml`（`axis-regression`、`green-unproven`、`evidence-missing`）、`prompt-adherence-reading-status.yaml`（`complete`、`partial`、`no-data`、`not-found`）。观察状态 MUST NOT 另设第六事实：按引用复用 `shared/declarations/facts/evidence-seven-states.yaml#/statement` 的七态值域，加 run-determination 值域拥有的 `not_evaluated` 字面量，在读时组合。未知令牌 MUST 为硬错误。任何值域 MUST NOT 在引擎常量或文档中复述。读取 MUST NOT 把遵从裁决令牌（`adherent`、`deviant` 或层级别等价物）作为行值或层值输出——证据状态加声明的偏差类是完整的观察词汇。reason cause 词汇封闭为 `{source-unavailable, no-matching-records, invalid-source}`，invalid-source cause 封闭为 `{unparsable, schema-violation, unknown-schema-version, invalid-timestamp}`；其**含义**由 owner 文档拥有、**令牌**是引擎 schema，双向契约测试钉住两面；它们有意**不是**声明事实。
- **FR-019**: 归属 MUST 单一来源：owner 文档拥有含义，声明事实拥有值域，引擎拥有 schema 与行为，框架地图与任何技能/命令面只携带指针。封闭集变更 MUST 是一次 owner 修订加既有镜像再生成，绝不是第二个编辑位置。

#### E. 分发、离线、隐私与入口

- **FR-020**: 全部器物 MUST 走既有 publish → install → init 流程（框架源、生成的镜像、框架地图行），使新初始化项目无需额外设置就包含该机制：`sync-mirrors.py` 的 `MIRROR_PAIRS` 投影 `shared → .specify/shared` 与 `scripts → .specify/scripts`，`specify init` 拷贝 `shared/` 与 `scripts/` 树。镜像 MUST 生成、绝不手改。测试与 fixtures 是仓内开发资产，不分发。
- **FR-021**: 机制 MUST 不访问网络、不执行自动传输；读数留在项目内。输出 MUST NOT 复现原始用户对话文本——只有结构化字段、封闭令牌与源引用可以进入读取；feedback 条目正文（review 散文、points）、门控决策散文与 finding summary MUST NOT 进入任一输出形态。
- **FR-022**: 缺失的存储、通道或记录 MUST 按 FR-011 降级并有文档化退出码（owner: `shared/definitions/script-interface-definitions.md`）；MUST NOT 编造值、MUST NOT 干净缺省。缺席、不可读或含未知令牌的声明层是同一降级类：读取 MUST NOT 猜值域，MUST 以非零退出并给出有文档的原因。退出码封闭：`0` 已产出读取（含 `no-data` 与 `not-found`）或覆盖检查干净；`1` 覆盖检查报告发现；`2` 无法产出读取（不可用的声明层或 owner 文档、未知令牌、非法参数）。记录级未知值令牌 MUST NOT 成为退出 2 的原因：它进入 `invalid_sources`，读取以退出 0 继续。
- **FR-023**: 一个有文档的单次调用（self-explanatory floor）MUST 产出人类可读读取，且机器可读形态 MUST 可用：`python3 .specify/scripts/python/prompt-adherence.py`（框架源 `scripts/python/prompt-adherence.py`，安装为 `.specify/scripts/python/prompt-adherence.py`），裸调用打印默认范围的按运行读取，`--run <run-id>` 钉住运行身份，`--since` / `--until` 请求纵向读取，`--json` 输出机器可读形态，`--workspace-root PATH` 选择项目，`--check-coverage` 运行 FR-003 覆盖检查；`-h` / `--help` / `--version` 按脚本接口契约。`--version` 版本在运行时从最近 `pyproject.toml` 导出，源码中不写版本字面量。取得确定性读取 MUST NOT 需要 LLM 摘要步骤或手写查询。入口 MUST 在框架地图登记；本版本 MUST NOT 发布 `/speckit.*` 命令或 skill 包装器——包装器是未来的独立决策。

#### F. 守卫、边界与首次采用

- **FR-024**: 契约测试 MUST 至少守卫：owner 文档及其双语形态；五个声明事实 ↔ 引擎封闭集一致性，含未知令牌拒绝（非零退出、无读取）；覆盖 `shared/declarations/facts/runtime-store-layout.yaml#/statement` 所辖受管存储根的只读包含性声明（referent：这些根上的哈希清单；允许增量：无；解释器字节码缓存 `__pycache__/`、`*.pyc` 明确排除；补充断言：按运行与纵向读取后根逐字节不变且零新文件）；重跑确定性（run-A/run-B 相等——与包含性分开判定，互不代证）；镜像一致性（`sync-mirrors.py --check` 对本特性触及的对无新漂移）；框架地图登记可解析；FR-003 覆盖图机器检查。全部守卫经 `scripts/bash/run-tests.sh` 执行。包含性与稳定性声明 MUST 可按 `shared/guidelines/closed-set-claims.md` 判定（基线 referent、比较单元、允许差集来源）。
- **FR-025**: 机制 MUST NOT 产出复合遵从分、成熟度指数、排名或任何跨项目比较；聚合只有按封闭状态的计数加覆盖。任何未来评分都是本特性之外的新决策。
- **FR-026**: 本特性线 MUST 经既有渠道产出一份本仓库的日期化基线读取，带显式未观察行；MUST NOT 在无可比前后证据时声称改进（证据纪律）。
- **FR-027**: 宿主层观察只服务本框架的集成决策。机制 MUST NOT 把它们包装成关于宿主产品的反馈；feedback 目标仍是框架自身。
- **FR-028**: 初始信号目录 MUST 恰好由以下六行组成。每行由一条既有存储上的机器可检记录谓词定义，声明其层候选与强度，并点名它可作证的偏差类（FR-018 集合）；行 id 是由 `prompt-adherence-signals.yaml` 拥有的封闭集，owner 文档通过引用源引擎自身的裁决值域与推导来定义每个偏差类：
  - `run-determination-record` — `.specify/session/` 中 `run-determination.py` 持久化的 run-determination 记忆条目（tag `run-determination`）；身份字段 `run_id`；时间戳 `determined_at`；层 `host-prompt`；强度 `indirect`；正状上限 `Exercised`；可作证 `axis-regression`、`green-unproven`。
  - `exec-quant-record` — `.specify/exec-quant/` 下 `kind: speckit.exec-quant`、schema 版本由 `quant-record-schema.yaml` 声明的记录；身份 `run_id`；时间戳 `collected_at`；层 `project-rules`；强度 `indirect`；正状上限 `Exercised`；仅使用覆盖，无偏差类。
  - `feedback-entry` — `.specify/feedback/` 下 `run_id` 不携带 `gate:` 族前缀的 feedback 条目（仅元数据面）；身份 `run_id`；时间戳 `created`；层 `project-rules`；强度 `direct`；正状上限 `Exercised`；无偏差类——缺席 MUST NOT 读成违规。
  - `gate-observation-record` — 门控观察族的 feedback 条目：`run_id` = `gate:<gate_id>:<UTC ts>`，前缀协议由 `shared/guidelines/confirmation-gates.md` 声明；身份 `run_id`；时间戳 `created`；层 `project-rules`；强度 `direct`；正状上限 `Exercised`；无偏差类——记录中的决策信号是散文，MUST NOT 读取。
  - `evidence-finding` — `.specify/evidence/` 下证据运行的 finding 项（`kind: speckit.evidence-findings`，`schemaVersion: 1`），项投影字段钉在 `FINDINGS_PROJECTION_FIELDS`；身份 `runId`；时间戳为 run manifest 的 `created`；层 `project-rules`；强度 `indirect`；正状上限 `Exercised`；可作证 `evidence-missing`。证据运行以自身 `ev-…` 身份标识，不以 SDD 运行 id 标识，因此在按 SDD 身份取范围的读取中该行诚实未匹配；纵向窗口是跨存储视图。
  - `probe-registry-declaration` — `.specify/shared/definitions/probe-definitions.md` 中的 probe 注册表声明对象；无身份字段、无时间戳（run-identity-exempt、window-exempt）；层 `project-rules`；强度 `indirect`；正状上限 `Wired`（已配置不等于已演练）；无偏差类。
  
  instructions reconcile 观察 MUST NOT 进入目录，直到某 store 持久化它们（今天没有）；它们保持盲区类（FR-029）。每行 MUST 经其所有者引擎的读取面读取，绝不第二解析器。
- **FR-029**: 初始盲区登记 MUST 恰好包含以下六类，每类带「今天为何无持久化传感器观察它」的理由与「owner 许可的采集变更会走的方向」；它们以不可观察进入每次读取的覆盖节：
  - `host-prompt-content` — 宿主系统提示原文与用户直接提示文本从不被读取（隐私红线），因此宿主层规则级遵从没有传感器。
  - `host-rule-surfacing` — 宿主环境是否真的加载并呈现项目规则文件，不留记录。
  - `in-turn-rule-behavior` — 某一规则节是否在本回合被遵守，没有把回合行为与规则绑定的结构化记录。
  - `anomaly-line-persistence` — 派发返回时的 fast-fail anomaly 行不被持久化；被 run-determination 所有者放弃的红状态生产器 MUST NOT 在此重新引入，边界仍归 `shared/guidelines/fast-fail.md`。
  - `gate-breach-and-silent-skip` — 未过必需确认门就行动、或静默跳过必需步骤，都不记录事件；缺席 MUST NOT 读成违规（FR-012）。
  - `instruction-drift-between-reconciles` — 指令节漂移只在 reconcile 运行时可见，且不持久化观察。
- **FR-030**: 目录中非注册表行的源存储 MUST 对 `shared/declarations/facts/runtime-store-layout.yaml#/statement` 的声明集解析：值域经 `declaration_reader.py` 读取；本树的根是声明 store 名的 `.specify/<store-name>/` 投影（该事实不携带逐 store 的 `root` 键），引擎 MUST NOT 另立第二张根表；行点名未声明的 store MUST 是硬错误（退出 2）。probe 行豁免（它是注册表声明，不是存储）。覆盖声明的 referent 是同一事实的声明根集合。

### Key Entities *(include if requirement involves data)*

- **Prompt Layer（提示层）**：两层之一，由令牌（[[STR-001]] 或 [[STR-002]]）标识，带其文本拥有者（宿主运行期 vs 本框架）与可观察性边界。
- **Adherence Signal Class（遵从信号类）**：一个目录行——行 id、描述、源存储与所有者引擎、层候选、强度、允许的观察状态、源引用要求，以及准入失败（FR-004(a)）时的盲区对应。
- **Adherence Observation（遵从观察）**：一个信号类在一个读取范围内的状态，携带证据状态、源引用，以及状态为缺席态（`not evaluated` 或 `Unobserved`）时必有的 reason。
- **Deviation Class（偏差类）**：一个目录行可作证的具名负面观察种类，携带封闭令牌与从源引擎自身值域引用的推导；不声明任何类的行永不产生负面观察。
- **Adherence Reading（遵从读取）**：一份按运行或纵向输出——版本、范围与窗口、观察、覆盖节、invalid-source 与 duplicate 披露。
- **Blind Spot（盲区）**：一个今天没有持久化传感器的假定行为，其理由，以及 owner 许可的采集变更需要观察到什么。
- **Coverage Map（覆盖图）**：从假定行为到传感器行或盲区的机器检查关系。

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|----|----------|
| RS-001 | 提示遵从度评价运行面：owner 定义文档、其声明值域，以及确定性只读读取引擎；承载于既有 Python 标准库脚本层与共享声明读取器 | in-scope | 本规格：owner 文档、信号目录、声明集、读取契约、引擎行为 | 仅 Python 标准库；对既有存储只读（owner: `runtime-store-layout`）；无新存储、采集点、服务、网络或评分 | 本切片 | fixture 一致性 + 确定性 + 只读哈希包含性 + 层诚实 + 离线 init 运行 + 镜像一致性 | FR-001…FR-030, SC-001…SC-009 | EP-001 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 一个覆盖每个目录行与每个允许观察状态的种子 fixture 恰好产出预期读取；连续两次运行逐字段相同、零无法解释的差异 **Path**: final
- **SC-002**: 在有数据 fixture 上运行按运行与纵向读取后，`runtime-store-layout.yaml#/statement` 所辖受管存储根的哈希清单不变（允许增量：无；解释器字节码缓存排除），且零新文件出现 **Path**: final
- **SC-003**: 在只有项目层行可观察的 fixture 中，除 `Unobserved` 外不出现宿主层陈述；在只有 indirect 强度行可观察的 fixture 中，不出现层级裁决 **Path**: final
- **SC-004**: owner 覆盖图中每条假定行为解析到恰好一个传感器或盲区条目，每个传感器条目解析到既有目录行 id，每个目录行至少被一条假定行为引用——机器检查退出 0、零发现；篡改副本退出 1 并点名发现 **Path**: final
- **SC-005**: 由 `specify init` 初始化的无记录项目在文档化调用下以显式 `not evaluated` 行与文档化退出码完成（网络隔离下），有数据 fixture 产出完整读取，且不发生网络访问或传输 **Path**: final
- **SC-006**: fixture 读取中 100% 的观察仅凭其源引用即可解析；故意破坏的引用报告为 invalid source 而非跳过 **Path**: final
- **SC-007**: 每个新封闭集的每个成员至少在一个测试中被演练，未知成员以非零退出被拒绝，声明事实与引擎逐成员一致 **Path**: final
- **SC-008**: 本仓库存在一份日期化基线读取（经既有渠道），含显式覆盖与未观察行，并可凭其自身源引用重放 **Path**: final
- **SC-009**: 镜像与源逐字节一致，fresh init fixture 包含该机制，框架地图行可解析，且经 `scripts/bash/run-tests.sh` 的完整套件无新增失败 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 经 `scripts/bash/run-tests.sh` 的契约/fixture 测试运行；按 single-run evidence 捕获完整命令行、stdout/stderr、退出码与时长，并做一次重跑比对；基线是 fixture 的预期读取清单。
- **SC-002 Source**: 测试自身在每次读取调用前/后对 `runtime-store-layout.yaml#/statement` 声明的根集合计算哈希清单（路径、字节 SHA-256、大小）并比较；字节码缓存按名排除由同一测试断言。
- **SC-003 Source**: 两个专用 fixture（仅项目层；仅 indirect）在层诚实性测试中断言；裁决行对照预期输出。
- **SC-004 Source**: 覆盖图检查器对 owner 文档的机器输出，捕获退出码与发现列表。
- **SC-005 Source**: init-fixture 集成测试：由 CLI 初始化项目、网络隔离、捕获完整调用；同一隔离下的有数据 fixture 为正向用例。
- **SC-006 Source**: audit-replay fixture 测试：逐观察机械解析其引用；种子化坏引用必须作为 invalid source 出现。
- **SC-007 Source**: 每个新封闭集一份契约测试，加未知令牌拒绝用例；每次运行捕获输出。
- **SC-008 Source**: 日期化记录路径本身（feedback 条目或 evidence 记录）及其源引用；以一次 audit-replay 运行演示重放。
- **SC-009 Source**: 镜像一致性检查输出、init-fixture 文件树差异、框架地图解析检查、`scripts/bash/run-tests.sh` 的完整套件输出。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"host-prompt"` | FR-002, layer-token tests |
| `STR-002` | `"project-rules"` | FR-002, layer-token tests |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

<!--
This section is populated by /speckit.clarify with questions and answers.
-->

### Session 2026-11-27（无人值守 requirements 阶段；无提问，裁决记于 Assumptions）

- Q: 本阶段是否留下 `[NEEDS CLARIFICATION]` 标记？→ A: 无。所有开放点由源能力已关闭的裁决（092 的 Clarifications 与其 owner 文档）、本树实测与 brief 的歧义清单就地裁定，见 A-1…A-18。
- Q: 特性绑定？→ A: 新独立 Feature 109「Prompt Adherence Evaluation（提示遵从度评价）」；不复用源 Feature 097；索引/详情登记由 `/speckit.clarify` 完成，本阶段不编辑注册表（A-2）。
- Q: 读面在 spec-kit 是否齐全？→ A: 六个传感器读 API、记录字段、门控族前缀、声明读取器与运行时存储布局事实均已实测存在（A-3、A-4）；唯一偏离是源 `store_layout.py` 在 spec-kit 不存在，改为经 `declaration_reader.py` 直接读布局事实（A-5，FR-030）。
- Q: 是否新增运行期存储？→ A: 否（A-6）。
- Q: 语言与读者？→ A: 中文为主、核心概念双语；读者基准沿用全局基准读者（A-17）。

## Out of Scope

- 复合遵从分、成熟度指数、排名或任何跨项目比较。
- 任何新存储、采集点、记录 schema 变更或数据迁移。
- 读取原始宿主系统提示、原始用户对话文本或用户源码内容。
- 自动传输、遥测上传或任何网络访问。
- 把宿主产品当作产品来评价；读数只服务框架集成。
- 超出既有存储已保留范围的历史回填。
- 改变 feedback、run-determination、evidence、probe 或 measure 报告的语义与红线。
- 仪表盘、UI、计划性评价服务或运行期评价平台。
- 除「框架地图一行」+「owner 文档 § Entry」之外的任何新常驻说明节；本版本不发布任何 `/speckit.*` 命令或 skill 包装器。
- 移植源 092 的 `templates/tasks-template.md` 改动（属另一条惯例线，A-8）。