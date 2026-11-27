# Requirements Specification: Context Management — 上下文的声明、组合与只读审计（Context Management）

**Requirement Branch**: `110-context-management`
**Created**: 2026-11-27
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（修订 `shared/definitions/context-management-definitions.md`、`shared/declarations/facts/context-*.yaml`、`scripts/python/context-audit.py`、`templates/instructions-template.md`、`shared/definitions/framework-map.md`、`tests/**` 的作者，需要判定「每个被声明为上下文的材料由谁拥有、以什么形态进入、缺失时说什么」）与下游项目维护者（在客户项目里运行同一只读审计、需要区分「来源真的缺失」与「审计读不懂」的人）——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` 的全局基准读者判定
**Reading scenario**: 当需要判定「不变/可变两类与系统级/项目级/任务级三层如何划分、类目归属由什么测试判定」「五种物化形态各允许出现在哪些层、越界如何被发现」「十八个上下文事实类各自从哪个 owner 路径物化、cap 指向谁」「组合在哪些触发点发生、由哪个角色执行、证据是什么」「审计引擎的两个动作、九个检查规则、退出码与在场词表是什么」「派发边、记忆召回投影与重入面各由谁的既有通道承载概念指针三元组」「客户项目经 init 得到什么、离线与缺失时如何诚实呈现」「哪些既有 owner 必须保持零改动」时打开本规格，据 FR-001…FR-029 与 SC-001…SC-011 放行 `/speckit.clarify` 与后续规划
**Input**: User description: "对比…本项目与 ai-harness 最近两天的修改，进行查缺补漏。范围裁定：特性级双向同步；spec-kit 以稳定为第一优先级，不引入激进架构变更；决策治理 107/091 各自独立，不互相对齐。"

**输入校正**：①本线把 ai-harness 已关闭的 **093 context-management** 能力**移植**为 spec-kit 的加性面（声明层 + owner 文档 + 只读审计引擎 + 分发/init 接线 + 守卫），不是新造机制；②源能力的注册特性编号（ai-harness Feature 098）**不复用**：本规格绑定 spec-kit **Feature 110**（A-2）；③「稳定第一」落实为**加性约束**：不改变任何既有引擎行为、不迁移任何运行期存储（区别于 105）、不与 107/091 的决策治理对齐，本特性只新增声明、文档、一个只读引擎、守卫与一条 ambient 指令段；④源材料中若干 spec-kit 不存在的传感器（清单见 A-3）按「缺失即降级读数、绝不发明」处理——它们不成为虚构路径，而成为本规格记录的适配裁定。

## Related Feature *(mandatory)*

**Feature ID**: 110
**Feature Name**: Context Management（上下文管理）
**Binding basis**: 独立新特性，无父特性切片。能力语义继承 ai-harness 093（其注册特性 098 Proactive Context Management 的编号在本仓不复用，A-2）；本规格产出的声明模型、owner 文档、只读审计引擎与守卫即该特性的规格面。本阶段不编辑 `.specify/features.md`（**本线约束：不写 registry/spine**）；索引行与详情文件由 `/speckit.clarify` 之后的 Feature Integration Protocol 落位，届时以本规格与现状对账。

## Overview

**目标形态（移植对象）**：spec-kit 的「上下文」今天由若干各自正确的碎片共同提供——指令层的 Documentation Map（`.specify/instructions.md`）、Token 效率纪律（`shared/guidelines/token-efficiency.md`）、重锚定分层 T0/T1/T2（`shared/definitions/re-anchoring-definitions.md`）、记忆召回（`scripts/python/memory-utils.py --action recall`）、声明层（`shared/declarations/contract.yaml` + `declaration_reader.py`）、super↔sub 派发协议（`shared/definitions/superagent-definitions.md` § The super↔sub Protocol）与 agent 文件渲染（`src/specify_cli/__init__.py` 的 render 路径，产出各工具目录下带 `## Project Context` 的 agent 文件）。**没有任何单一 owner 陈述整幅图景**：哪些事实跨任务不变、哪些逐任务可变；每层在哪物化（指针 / 全读 / 有界索引 / 运行期发现 / 内联摘要）；谁在哪个触发点组合；客户项目在来源缺失时如何诚实降级。碎片之间是**沉默的空隙**：没有组合基线的会话与组合过的会话看起来一样，因为没有任何东西点名「本该有什么」。

**本特性交付**：一个 owner 文档（`shared/definitions/context-management-definitions.md`，安装于 `.specify/shared/definitions/`）声明模型与布局；四个机器值域声明事实（`shared/declarations/facts/context-{categories,layers,forms,classes}.yaml`，经 `shared/declarations/contract.yaml` 加性注册、经 `declaration_reader.py` 读取）；一个只读、离线、确定性的审计引擎（`scripts/python/context-audit.py`，`--action check` / `--action manifest --layer <system|project|task>`）；一条 ambient 指令段（`## Context Management(上下文管理)`）；五组守卫测试（4 contract + 1 integration）与逐规则种子违规 fixture；一行框架地图的三个新行。机制**组合一次不变基线、逐任务选择可变层**，按声明触发而非临场发挥；它**替换**上述任何载体中**任何一个都不替换**——每个载体保留其 owner、上限与行为，新模型以指针抵达它们。

**本特性不做什么**：不是新存储、不是 composer、不是 renderer、不是 summarizer、不是上下文窗口优化器、不是调度器，也不是 super↔sub 派发协议的第二套载荷；不迁移任何运行期存储；不改任何既有引擎的语义与退出码；不新增 `/speckit.*` 命令、技能包装、门、红线、watcher 或后台检查；不与决策治理（107）或自动 git closeout（091）做任何对齐。

**实测基线（2026-11-27，本工作树）**：① `.specify/instructions.md` 为 **40,170 B**，生成器 `scripts/bash/generate-instructions.sh` 的预算常量为 **40,960 B** —— ambient 段只有约 **790 B** 余量（A-10）；② 镜像对为 `shared → .specify/shared`、`scripts → .specify/scripts`、`templates → .specify/templates` 等六对（`scripts/python/sync-mirrors.py` 的 MIRROR_PAIRS）；③ 声明层要求事实携带 `fact` / `kind` / `statement` / `consumers` / `former_carriers` 五键，且既有新事实以 `shared/declarations/contract.yaml` 的**追加式注册块**登记（093/105 先例）；④ `shared/definitions/superagent-definitions.md` 的派发载荷是**七个角色字段 + 四项注入 + 上行回传 + 结算**，仓内**不存在** Tier G / Tier T 的七组件包与 per-slot caps（检索 `Tier G` / `Tier T` / `7-component` 零命中）；⑤ 仓内**不存在** `project-context-render.py` / `project_facts.py`，`## Project Context` 由 agent 文件渲染路径产出；⑥ `absent` / `unreachable` / `empty` / `not-evaluated` 四词在仓内没有一个框架 owner（`not-evaluated` 仅作为报告渲染标记出现在 `shared/guidelines/reporting-obligations.md`），证据态七态由 `shared/declarations/facts/evidence-seven-states.yaml#/statement` 拥有。以上⑤⑥是本移植的**缺失传感器**，按 A-3/A-8/A-15 适配，并以「缺失即降级读数、绝不发明」为纪律。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **类别判定 = `execution`**：交付物是 owner 文档、声明事实、只读引擎、守卫与模板段，验收由机器执行与断言；owner 文档另被人类阅读（混合读者面），按 flow-class owner 对混合 oracle 的裁决取 `execution`，`Flow Type` 为 `-`。 | 缺陷只在引擎执行、断言或确定性比对时暴露。 |
| **A-2** | **特性绑定 = Feature 110**：独立新特性 `Context Management（上下文管理）`；**不复用**源能力的注册特性编号（ai-harness Feature 098）；本阶段不编辑 `.specify/features.md`（registry 写入被本线约束禁止），索引行/详情由后续 clarify 按 Feature Integration Protocol 登记。 | brief 明令「Bind Feature 110 (never the source registry ID)」；编号是线身份，不是源身份。 |
| **A-3** | **路径与命名适配（逐目标已核验存在）**：`.ah/` → `.specify/`；`/ah.*` → `/speckit.*`；`ai-harness` → `Spec Kit` / `specify`；源仓的 src/ai_harness → `src/specify_cli`；`.ah/specs/093-context-management/` → 本目录；`.ah/memory/tools/` → `.specify/tools/`；`.ah/state/` → `.specify/state/`。**缺失传感器的适配**：(a) 源 FR-005 的 `project-context-render.py` / `project_facts.py` 在本仓不存在 —— 站位 `## Project Context` 渲染的 owner 改为 agent 文件渲染路径 `src/specify_cli/__init__.py`（`render_agents_for_tool`）；(b) 源 FR-017 的 7 组件包（Tier G/Tier T + caps）在本仓不存在 —— 派发边改为映射到 `superagent-definitions.md` 的真实载荷面（七角色字段、四项注入、上行回传），见 FR-017/A-15；(c) 源 FR-020 的四撤销词 owner 在本仓不存在 —— 见 A-8；(d) 源的 per-slot caps owner 在本仓不存在 —— cap 引用改为 `shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First)，见 FR-019/A-7。每一项都以**降级读数**呈现，不伪造路径。 | 「缺失即降级读数，绝不发明」；适配必须可逐条点名，而不是悄悄换名。 |
| **A-4** | **类别由层派生（承重）**：候选为 (a) 两独立轴、多组合；(b) 一分区、类别只是层的任务相关性标签；(c) 无类别概念。取 (b)：`system`/`project` → `invariant`，`task` → `variable`；每层恰一个类别，类别**永不成为布局表列**。反面度量：独立轴更富表达力，但会把「项目层却随任务变化」这类当前无载体的组合虚构成行。重开条件：出现真实载体——某项目层事实随任务变化——这需要 owner 修订，而不是局部加行。 | 成员测试只说一次：「若只有任务改变、环境与项目不变，该事实会变吗？」 |
| **A-5** | **五形态与合法性矩阵（承重）**：取「五形态 + 每层允许集」而非「指针/内容二元」或「自由形态字段」；合法组合 system ⊂ {runtime-discovery, pointer}、project ⊂ {read-in-full, pointer, bounded-index}、task ⊂ {bounded-index, pointer, inline-digest}。反面度量：矩阵限制了一些技术上可能的组合，但每个限制都对应既有载体的实际行为（全读治理、有界索引、运行期发现、内联兜底、纯指针）。重开条件：出现一个载体其形态必须落在矩阵禁止格——那要修 owner 的矩阵，而不是在引擎里放行。 | 矩阵让「任务层不得复述不变内容」可机械判定。 |
| **A-6** | **布局种子十八类，唯一配对受制裁**：类花名册（成员与次序）由 `context-classes.yaml` 拥有；owner 文档布局表是逐行数据（`class id | layer | form | source | owner | cap reference`）的唯一书写处；两者逐行比对，不匹配即 `check` finding；**不存在第三份布局数据文件**。四事实在 `shared/declarations/contract.yaml` 以**追加式注册块**登记（093/105 先例的平铺式 `<slug>: <path>` 形态），因为四事实不需要 094 `registered_facts` 的额外 `statement_keys`；一个消费者读不到的登记视同不存在。种子十八类沿源清单：system 4（`runtime-environment`、`available-commands`、`operation-permissions`、`reality-constraints`）、project 7（`governance-baseline`、`project-vocabulary`、`concept-definitions`、`concept-explanations`、`capability-inventories`、`project-state-anchors`、`workspace-map`）、task 7（`task-artifacts`、`task-capabilities`、`task-shared-docs`、`task-docs`、`task-memory`、`task-statement`、`task-delta`）；增删类目是 owner 修订。 | 一源真理：表与花名册是唯一受制裁的双表示面，且由守卫钉住。 |
| **A-7** | **cap 只引用、不声明（承重）**：本特性不引入任何数值上限。每个 `bounded-index` 行 MUST 指名 cap owner 的**路径 + 小节**；本仓的 token/cap 经济 owner 是 `shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First)（含其升级阶梯与小文件阈值的例外），`read-in-full` 与 `inline-digest` 行同样指向该小节作为其内容承载的例外 owner。被拒方案：给基线设一个 token 预算——基线是指针形态，其唯一内容是治理文档的全读，而那由既有纪律裁决。 | 源 FR-019 的 per-slot caps owner 在本仓缺失（A-3d）；token 效率纪律是真实存在的 cap owner。 |
| **A-8** | **在场词表在 owner 文档定义一次（适配）**：五个在场词——正向 `present`，缺席 `absent` / `unreachable` / `empty` / `not-evaluated`——在本仓**没有一个既有框架 owner**（A-3c 实测），因此由本特性 owner 文档**一次定义**其语义；其他表面只引用，不复制。证据态读数 `Unobserved` 仍按指针抵达 `shared/declarations/facts/evidence-seven-states.yaml#/statement`。被拒方案：把词表挂到一个不存在的 owner 路径上——那是伪造指针。 | 源 FR-020「只加正向词、其余复用」的前提在本仓不成立；缺口以「一次定义 + 单一 owner」诚实收口，而不是发明 owner。 |
| **A-9** | **引擎形态与退出码**：单文件、stdlib-only、只读；`check` 退 `0` 干净 / `1` findings / `2` 用法、不可读输入或声明事实的未知/缺失成员；`manifest` 只要发出清单即 `0`（缺席行含在内），用法或声明层失败 `2`。探针集封闭为 `platform` / `path-tools` / `fs-access` 三个 id（引擎 schema，不是值域）；**未知探针 id 读 `not-evaluated` 并带原因，属在场读数而非 `check` finding**。 | 与声明层 `exit_codes`（`shared/declarations/contract.yaml` 的 `ok: 0 / finding: 1 / input-error: 2`）一致；不扩检查规则集。 |
| **A-10** | **ambient 段与预算**：源 093 的 `## Context Management(上下文管理)` 段是**能力专属**段落，随本特性移植（改写路径措辞，不导入任何无关 hunk）；落点为 `templates/instructions-template.md`，由 `scripts/bash/generate-instructions.sh` 的**加性 section reconcile** 注入 `.specify/instructions.md`（既有段永不修改或删除，live 文件保持为刷新基线）。实测余量约 **790 B**：最终树的 `BUDGET:` 行 MUST 读 `within`；**不抬高预算常量、不裁剪既有段**；若实测确实装不下，那是必须上送的异常，不是静默提额。 | 源 RU-1 允许提额；本仓「稳定第一」把提额排除在本特性范围外，并要求把冲突显式上送。 |
| **A-11** | **存储登记：无**：机制只读，不创建 `.specify/<store>/`、缓存、索引或渲染产物；`shared/declarations/facts/runtime-store-layout.yaml` 的存储花名册不变。本特性的**唯一持久增量**是：owner 文档、四个声明事实、`contract.yaml` 的四条注册行、审计引擎、守卫与 fixtures、一条 ambient 指令段、框架地图三行。 | 源 FR-011 的等价约束；read-only audit 不需要存储登记。 |
| **A-12** | **分发与隐私**：owner 文档/四事实/注册行/引擎随既有 **publish → install → init** 流走 `shared/` 与 `scripts/` 两棵树（`scripts/python/sync-mirrors.py` 投影到 `.specify/shared`、`.specify/scripts`；`specify init` 复制到客户项目 `.specify/`）；模板编辑经 `templates → .specify/templates` 镜像对落地。机制离线、不传输、不读原始用户文本或会话内容——审计只消费路径、元数据与在场状态。 | 源 FR-023/FR-024 的等价；实测镜像对与 init 复制步骤均存在。 |
| **A-13** | **命名与词汇表**：用户语汇优先——「上下文管理 / 不变 / 可变 / 系统级 / 项目级 / 任务级」；六个双语定义位字面量由 Shared Strings 钉住（[[STR-001]]…[[STR-006]]），机器 token（`invariant`/`variable`、`system`/`project`/`task`、五形态 token）由声明事实拥有。**不编辑 `.specify/glossary.md`**：它是单一所有者的 canonical registry（本线禁止 registry 编辑）；术语提案按 glossary 协议的 wrap-up 检查点在后续阶段提交，机器值域不复制进词汇表。 | Grounded Naming + 一源真理；词汇表编辑不属于本阶段产物。 |
| **A-14** | **环境前提（EP-001，由 plan 定义）**：本机制消费的既有载体——声明层、token 效率纪律、重锚定分层、记忆召回、super↔sub 协议、agent 文件渲染、镜像与 init 流——均已存在且是正确底座；plan 阶段 MUST 逐项记录「在哪找到、如何核验」，MUST NOT 假设本仓没有发布的机制。 | 源 EP-001 的等价；本阶段只保留 `EP-001` 引用。 |
| **A-15** | **概念指针三元组搭既有通道（承重）**：候选为 (a) 在派发载荷新增一个专用字段/注入携带三元组；(b) 三元组由项目层三行在基线中承载，派发边映射到既有通道（`authority_ref` 指针字段 + 子代理 ambient 的 Documentation Map 的 glossary 行 + 派发简报的阅读清单）；(c) 不显式声明，留给 Documentation Map 隐含。取 (b)：它让一致性**可检查**（花名册、manifest 在场、契约守卫），且不给 `superagent-definitions.md` 增加任何字段、注入、上限、标识或自检项。反面度量：(b) 只证明指针在场，不证明语义理解——机制 MUST NOT 声称超出证据的「一致」。重开条件：封闭结构集中某个受治理结构查无既有通道可承载三元组——那要修订该通道的 owner，而不是局部加字段。 | 源 A-16 的等价，落点换成本仓真实通道。 |
| **A-16** | **脚手架偏差（披露）**：`create-new-requirements.sh` 会把当前本地分支 `110-context-management` 计入编号空间而派生 111 并 `git checkout -b`，使工作树偏离本线分支；按 107/108 先例，本阶段**手工**从 `.specify/templates/requirements-template.md` 脚手架到本文件，仅跳过其建分支步骤，偏差记录于 `test-evidence/requirements-stage-2026-11-27.md`。 | 工作树必须停留在 `110-context-management`；脚本把「本线分支」当成了「已用编号」。 |
| **A-17** | **seeded fixture 自带声明层**：`tests/fixtures/context-management/` 的每个 fixture 在自身 workspace root 以框架源形态携带一份最小 owner 文档与四事实（`shared/definitions/` + `shared/declarations/facts/`），因此 `--workspace-root` 选中的树用它自己的声明层驱动 `check`/`manifest`；`tests/fixtures/` 与 `tests/integration/` 的既有 fixture 形态不变。 | 层的根解析规则（FR-021）必须让仓库树、fresh init 树与 seeded fixture 各自读到自己的 owner 文档与事实。 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一条不变基线，组合一次 (Priority: P1)

根会话在一个项目里开始一个工作项。在第一个实质动作之前，它**组合一次不变基线**：系统层（运行环境、可用命令、操作权限、现实约束指针——每项要么在使用时发现，要么指向其 owner）与项目层（以全读 canonical 指针携带治理基线，加上指向项目词汇、能力清单、状态锚与工作区地图的指针/有界索引）。它从 canonical 路径**全读**治理文档，**发现**系统事实而不是凭记忆复述，并且**不把任何不变内容复制**进任何简报。后续任务沿用同一基线，不再重组。

**Why this priority**: 其余一切都压在它上面。没有不变基线的会话会凭猜测的系统事实与陈旧的规则行动；失败是沉默的，因为答案看起来仍然合理。

**Independent Test**: 一个所有来源齐备的 fixture 被组合一次；基线清单（manifest 的 system+project 层读数）逐行列出 form 与 source，治理指针指向 canonical 路径，无任何行携带复制的治理文本；同一会话的第二个任务复用基线而不重组。

**Acceptance Scenarios**:

1. **Given** 一个已初始化且 `.specify/constitution.md`、`.specify/instructions.md` 齐备的项目，**When** 组合基线，**Then** 两者以全读 canonical 指针出现且**零复制字节**，其余项目层行以指针或有界索引出现且 source 路径可解析。
2. **Given** 已组合的基线，**When** 会话进入第二个任务，**Then** 没有任何基线来源因任务变化而被重读或重组，且不变内容不在任务层被复述。
3. **Given** 某个系统事实无法被发现（例如探针不可用），**When** 组合基线，**Then** 该行以显式缺席原因呈现，MUST NOT 填猜值。

---

### User Story 2 - 可变层逐任务选择 (Priority: P1)

会话或 superagent 开始一个具体任务。它只为该任务选择**任务层**：在范围内特性/规格制品、任务相关的技能与命令、任务相关的 shared-docs 与 docs 索引、记忆选择、蒸馏后的 `[task]` 陈述与 delta 事实（上一阶段提交、断点判定、状态脊摘要、territory manifest）。每个选择都受 owner 已声明的上限约束，触及不变层时以指针引用，任务结束即丢弃。

**Why this priority**: 正确的不变基线配一个陈旧或错误的任务层，仍产出错误的工作；任务选择是相关性与新鲜度的裁决处。

**Independent Test**: 同一项目上的两个不同任务关键词产出两份不同的任务清单，均从同一项目清单池中取出，各自在上限内，各自以指针引用同一不变基线且不新增不变内容。

**Acceptance Scenarios**:

1. **Given** 一个有多个规格的项目，**When** 组合一个限定到某特性的任务，**Then** 任务清单含该特性的规格制品并排除无关规格，每个有界行在其 owner 声明的 cap 内。
2. **Given** 同一会话从任务 A 切到任务 B，**When** 组合任务 B，**Then** 只重组任务层行，不变基线原样复用。
3. **Given** 某个任务层行触及一个已由基线承载的治理文档，**When** 组合该行，**Then** 它以指针形态出现且不携带该文档的任何文本。

---

### User Story 3 - 客户项目经 init 获得它：离线且诚实 (Priority: P1)

下游项目通过既有 publish → install → init 流安装 Spec Kit。无需任何额外步骤，它拥有 owner 文档、四个值域与审计引擎；新初始化项目在**无网络**条件下运行文档化调用，得到一份把真实缺失来源按项目既有缺席词表命名的清单，且**不向任何地方传输**。机制从不读取原始用户文本，也从不持久化任何上下文。

**Why this priority**: 只在框架仓里工作、需要网络、或静默填平缺口的机制，服务不了它要服务的客户项目。

**Independent Test**: 一个由 CLI 在 socket 封锁下初始化完成的临时项目运行 `check` 与 `manifest`；输出逐行给出精确缺席原因；fixture 树的哈希清单前后不变，且无新文件出现。

**Acceptance Scenarios**:

1. **Given** 一个刚初始化、无记忆条目且无 Tool 记录的项目，**When** 运行审计，**Then** 这些来源读为 `absent`/`empty` 并带原因，MUST NOT 读成干净默认值，MUST NOT 读成编造内容。
2. **Given** 同一项目在阻断网络的条件下运行审计，**When** 每个审计动作完成，**Then** 未打开任何 socket，未传输任何内容。
3. **Given** 声明事实缺失或不可读的项目，**When** 运行审计，**Then** 不产出任何猜测的判定，并按文档化非零退出码结束。

---

### User Story 4 - 主动触发与具名组合角色 (Priority: P2)

组合不靠偶然。owner 文档声明一个封闭的**触发集**——会话入口、任务入口、任务切换、派发前、阶段边界、来源漂移，外加重入——每个触发点名**组合者**（基线由根会话，派发载荷由 superagent）、它刷新**哪个范围**（基线或任务层）与**组合发生的证据**（派发边是派发简报；其余是 manifest 读数或重锚定陈述）。影响基线的来源变化（宪法修订、指令刷新、特性状态翻转、git 工作流变化）是声明式刷新触发，不是判断题。

**Why this priority**: 没有声明触发与角色，「主动」就变成偶然：有的会话组合、有的不组合，而没有任何东西区分两者。

**Independent Test**: 在一个宪法于两次任务间变化的 fixture 上，声明的来源漂移触发恰好重组基线一次；在一个任务变化而基线来源不变的 fixture 上，只有任务层被重组。

**Acceptance Scenarios**:

1. **Given** 已完成的基线与一份被修订的宪法，**When** 下一个基线刷新触发点到达，**Then** 基线恰好刷新一次，且该刷新在 manifest 的 source reading 中可见。
2. **Given** 一个派发边，**When** superagent 组装派发载荷，**Then** 载荷仍是既有七角色字段 + 四项注入 + 上行回传的形态，机制**不新增**任何角色字段、注入、上限、标识或自检项。
3. **Given** 一次压缩、handoff 或 stall 重读后的续作会话，**When** 它重建上下文，**Then** `reentry` 触发以指针重引基线（仅当同时命中基线刷新触发时才重建）、刷新 `task-delta`、并把重锚定陈述记为证据。

---

### User Story 5 - 一次只读审计读数 (Priority: P3)

维护者想知道机制声称「上下文中应有什么」，以及这些声称是否仍可解析。一次只读调用回答：`check` 对照值域（层、形态、类花名册）校验布局表并确定性地报告完整性 findings；`manifest` 打印一层的行，含 source、form、在场状态与 cap 引用。对不变树连续两次运行逐字节相同。

**Why this priority**: 未被审计的布局会漂移成愿望清单；审计是让声明保持诚实的东西。

**Independent Test**: 四个种子违规 fixture（bad layer token、bad form token、花名册不匹配、层-形态非法）各产出恰好预期的 finding 与退出码；对干净树连续两次运行逐字节相同。

**Acceptance Scenarios**:

1. **Given** 本仓自己的布局，**When** 运行 `check`，**Then** 退出 `0` 且零 findings，第二次运行产出逐字节相同的输出。
2. **Given** 一个声明了任务层 `read-in-full` 行与系统层 `bounded-index` 行的 fixture，**When** 运行 `check`，**Then** 恰好报告两条层-形态 findings 并非零退出。

### Edge Cases

- **项目层来源在 init 时缺席**（例如 `.specify/tools/` 尚无任何 Tool 记录）：行报告 `absent` 或 `empty` 并带原因；基线不带它组合；不得发明占位内容。
- **治理指针不可达**（权限、被删除）：指针报告 `unreachable` 或 `absent`；会话在其余基线上继续并点名缺口；机制从不编造文档文本。
- **运行期发现与已记录的项目事实矛盾**（如指令描述 Python 而解释器缺失）：发现的事实治理当前现实，矛盾必须以披露形态呈现（在场读数的 reason 或复审记录），MUST NOT 静默覆盖任何 owner，也 MUST NOT 以猜测填平。
- **任务变化而基线来源未变**：只重组任务层；重组基线是缺陷。
- **任务层选择会超出 owner 的 cap**：cap owner 的判定治理（token 效率纪律的升级阶梯/例外），机制报告 cap 引用，绝不引入第二个 cap 值。
- **同一来源被两层引用**：只允许 `pointer` 形态；在任务层内容化复用不变来源是缺陷。
- **任务范围什么都没选中**（无匹配制品或记忆）：行报告 `empty` 并带原因；组合仍完成，绝不回落到宽读。
- **两个会话并发组合**：每次组合都是瞬态的、不写盘，因此不共享任何路径、也不可能冲突；审计引擎出于同一原因只读。
- **agent 实例的 `## Project Context` 块陈旧**：它是渲染路径拥有的生成产物；机制报告陈旧（披露），不静默修复。
- **声明层缺失或携带未知成员**：审计不产出判定，按文档化退出码 `2` 结束，绝不猜测值域。
- **运行期探针失败**：该 `runtime-discovery` 行读 `not-evaluated` 并带原因（FR-020），MUST NOT 读 `present`，也 MUST NOT 变成 `check` finding。
- **无法解析 workspace root**（既无 `--workspace-root` 也无祖先 `.specify/`）：`check` 与 `manifest` 均以 `2` 结束并说明；MUST NOT 回落到其它根。
- **完整性违规布局上的 `manifest`**：manifest 仍按花名册行集发出各行（缺失布局行读 `not-evaluated`）；完整性违规是 `check` 的 findings，不改变 `manifest` 的 `0` 退出（声明层失败除外）。
- **不可读来源的 fixture 机制**：`unreachable` 必须能在不依赖运行用户特权（含 root）的条件下构造；实现按 plan 阶段裁定选择只读的注入/受控路径（例如指向一个以文件期望处出现的目录或受控 IO 失败）。
- **来源路径逃逸 workspace root**：审计只消费存在性、可读性、空/非空（大小/条目数）等元数据，不打开任何文件内容，因此无论符号链接或 `..` 逃逸都不可能导出内容；`check` 不因路径形状新增规则。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 框架 MUST 定义一个上下文管理 owner 文档 [[STR-001]]：`shared/definitions/context-management-definitions.md`（安装于 `.specify/shared/definitions/context-management-definitions.md`），承载伞形术语的双语定义位，并拥有：概念本身、两个类别、三个层、五个物化形态与合法性矩阵、层级落点契约、唯一的上下文布局表、组合协议、封闭触发集、组合者角色、概念指针槽位、在场词表（正向词 `present` 在此定义一次）与红线。其他任何表面 MUST 以路径引用抵达这些含义，MUST NOT 复述它们。
- **FR-002**: owner 文档 MUST 以**任务相关性**定义两个类别：`invariant`（[[STR-002]]）——只有任务改变而环境与项目不变时正确性不变的事实，每会话/线组合一次，只在声明触发时刷新；`variable`（[[STR-003]]）——为当前任务选择、逐任务组合的事实。成员测试 MUST 只说一次：「若只有任务改变、环境与项目不变，该事实会变吗？」；每层 MUST 恰声明一个类别；`system`/`project` → `invariant`，`task` → `variable`；类别由层派生，MUST NOT 成为布局表列。机器值域由 `context-categories.yaml` 拥有。
- **FR-003**: owner 文档 MUST 以**事实 owner 居住处**定义三个层：`system`（[[STR-004]]）——执行环境与在其中行动的现实，使用时发现、永不由项目撰写、永不持久化；`project`（[[STR-005]]）——项目 `.specify/` 工作区内撰写或生成的事实，任务周期内不变；`task`（[[STR-006]]）——当前工作项范围内的事实。区序 MUST 为 `system → project → task`（组合序）；机器值域由 `context-layers.yaml` 拥有。
- **FR-004**: owner 文档 MUST 携带唯一的**上下文布局表**，固定六列 `class id | layer | form | source | owner | cap reference`，每行对应一个上下文事实类；该表是逐行数据的唯一书写处，**不存在第二份布局数据文件**——受制裁的双表示面只有「表 + `context-classes.yaml` 花名册」这一对：花名册拥有成员与次序，表的 class-id 列是其投影，二者 MUST 逐行匹配，不匹配即 `check` 的 roster-mismatch finding（退 `1`）。布局表 MUST 无类别列。种子为**十八类**：system 4（`runtime-environment`、`available-commands`、`operation-permissions`、`reality-constraints`）；project 7（`governance-baseline`、`project-vocabulary`、`concept-definitions`、`concept-explanations`、`capability-inventories`、`project-state-anchors`、`workspace-map`）；task 7（`task-artifacts`、`task-capabilities`、`task-shared-docs`、`task-docs`、`task-memory`、`task-statement`、`task-delta`）。类 id MUST 全表唯一；每层 MUST 非空；每层内的行序 MUST 等于花名册声明的次序。
- **FR-005**: 机制 MUST NOT 替换或重定义它所组合的任何既有 owner；边界以指针抵达：派发/相对角色模型与载荷（`shared/definitions/superagent-definitions.md` § The super↔sub Protocol）；agent 文件的 `## Project Context` 渲染（`src/specify_cli/__init__.py` 的 render 路径）；记忆召回（`scripts/python/memory-utils.py --action recall`）；token/cap 经济（`shared/guidelines/token-efficiency.md`）；治理文本（`.specify/constitution.md` / `.specify/instructions.md` 及其生成器）；破坏性动作规则（`shared/guidelines/confirmation-gates.md`）；声明层（`shared/definitions/harness-triple-definitions.md` + `shared/declarations/contract.yaml`）；重锚定分层（`shared/definitions/re-anchoring-definitions.md`）。
- **FR-006**: **系统层** MUST 携带行动所需的环境事实：运行环境（平台、架构、shell、运行时版本）以 `runtime-discovery:platform` 探针发现；可用系统命令以 `runtime-discovery:path-tools` 发现（有 Tool 记录（`.specify/tools/`）时优先复用，按 tool-reuse gate）；操作权限（宿主允许什么：网络可用性、文件系统范围）以 `runtime-discovery:fs-access` 发现；现实约束（能做什么、不能做什么）以 `pointer` 指向既有 owner（`shared/guidelines/confirmation-gates.md`、`shared/guidelines/fast-fail.md`、`shared/guidelines/temp-directory-discipline.md`、`.specify/workflow/git.md`）。环境事实 MUST 在使用时只读观测，永不持久化或复制；约束事实 MUST 以指针呈现，永不复述。探针集是引擎 schema，封闭为三个 id；未被发现的事实 MUST 以缺席读数与原因呈现，永不被猜测或填默认。
- **FR-007**: **项目层** MUST 从 `.specify/` 携带项目事实：治理基线 `governance-baseline`——`.specify/constitution.md` 与 `.specify/instructions.md` 以 `read-in-full` canonical 指针呈现，**零复制字节**；项目词汇 `project-vocabulary`——`.specify/glossary.md`；概念定义 `concept-definitions`——`.specify/shared/definitions/`（有界索引）；概念解释 `concept-explanations`——`.specify/skills.md`、`.specify/tools.md`；能力清单 `capability-inventories`——`.specify/skills/`、`.specify/agents/templates/`、`.specify/agents/instances/`、`.specify/tools/` 与两份指南（有界索引）；项目状态锚 `project-state-anchors`——`.specify/features.md`、`.specify/features/`、`.specify/register.md`、`.specify/workflow/git.md`、`.specify/shared/declarations/facts/runtime-store-layout.yaml`；工作区地图 `workspace-map`——`.specify/shared/definitions/framework-map.md`、`.specify/shared/guidelines/directory-governance.md`。该层 MUST NOT 携带这些来源的内容；只携带指针与有界索引。
- **FR-008**: **任务层** MUST 携带场景事实：`task-artifacts`（在范围内特性详情与规格制品：`.specify/specs/`、`.specify/features/`）、`task-capabilities`（任务相关技能与命令选择：`.specify/skills/`、`.specify/agents/templates/`）、`task-shared-docs`（`.specify/shared/`）、`task-docs`（`docs/`）、`task-memory`（对 `.specify/session/` 与 `.specify/knowledge/` 的记忆召回投影）、`task-statement`（按 `shared/workflow/user-input-protocol.md` 蒸馏的 `[task]` 陈述）、`task-delta`（上一阶段提交、断点判定、状态脊摘要、territory manifest、已记录制品增量）。选择按任务范围与关键词；正文按需打开，绝不整体注入。两条 `inline-digest` 行（`task-statement`、`task-delta`）以**常驻 owner 路径**为其在场见证（分别为 `shared/workflow/user-input-protocol.md` 与 `.specify/register.md` + `.specify/state/`）；瞬态输入不构成常驻来源，也绝不使该行变成缺席。
- **FR-009**: owner 文档 MUST 定义封闭的五形态：`pointer`（按需打开的路径引用，不携带内容）、`read-in-full`（消费者 MUST 完整加载的 canonical 指针，零复制字节）、`bounded-index`（逐条目路径 + 一行相关性，在 owner 的 per-slot cap 内）、`runtime-discovery`（使用时只读观测，永不存储）、`inline-digest`（仅当任务层指针不可达时携带的有界内容）；以及形态×层合法性矩阵：system 允许 `runtime-discovery`、`pointer`；project 允许 `read-in-full`、`pointer`、`bounded-index`；task 允许 `bounded-index`、`pointer`、`inline-digest`。机器值域由 `context-forms.yaml` 拥有；审计引擎 MUST 强制该矩阵（越界即 `layer-form-illegal` finding）。
- **FR-010**: 不变内容 MUST NOT 在可变层被复述：触及不变来源的任务层行 MUST 以 `pointer` 引用它，MUST NOT 携带其文本、其 `read-in-full` 形态或其内联摘要。**可判定的**内容重复由审计报告，恰为两种形状：任务行以 `read-in-full` 覆盖一个不变层行声明的来源；任务行以 `inline-digest` 覆盖一个被不变层行以 `read-in-full` 物化的来源。其余形态（如对仅以指针物化的不变来源做内联摘要）由复审判定。
- **FR-011**: 机制 MUST NOT 持久化上下文：不创建 store、缓存、索引、渲染产物或数据库，也不改变任何既有存储的 schema；一次组合是瞬态的，随工作项消亡。本特性唯一的持久增量是 A-11 枚举的封闭集合；manifest 是打印到 stdout 的读数，永不写盘。
- **FR-012**: owner 文档 MUST 声明**基线组合**：在会话或线的入口（该会话/线的第一个任务），根会话组合不变基线一次——系统层经其使用期发现行、项目层经其 `read-in-full` 治理指针、指针行与有界索引——并从 canonical 路径全读治理文档、执行系统层发现；组合后的基线保持在会话工作状态中，永不持久化。**「会话或线」定义**：session = 一次 agent 会话的上下文窗口生命周期（压缩/重入不产生新 session，重入走 `reentry`）；line = 同一状态脊下的连续阶段系列（跨阶段提交仍是同一 line）。任务变化 MUST NOT 触发基线重组；只有声明的基线刷新触发（`session-entry` 与 `source-drift`）MAY。
- **FR-013**: owner 文档 MUST 声明**任务组合**：在 `task-entry`、`task-switch` 与 `pre-dispatch`，组合者为当前任务选择任务层，在 owner 已声明的 cap 内，以指针引用不变来源；任务切换或阶段边界刷新任务层而不触碰基线；每次组合 MUST NOT 加宽形态（`pointer` 行绝不被整体打开进载荷），MUST NOT 超出 cap，MUST NOT 在任务结束之外保留。
- **FR-014**: owner 文档 MUST 声明**封闭的七触发集**，每项点名其组合者、范围与证据：`session-entry`（根会话；组合基线一次；证据 = manifest 的基线行）、`task-entry`（当前工作的组合者；组合任务层；证据 = manifest 的任务行）、`task-switch`（只重组任务层；证据 = manifest 的任务行）、`pre-dispatch`（superagent；组合派发载荷与基线指针；证据 = 派发简报）、`stage-boundary`（刷新 `task-delta`；证据 = manifest 的任务行）、`source-drift`（根会话；恰好重组基线一次；证据 = manifest 的 source reading）、`reentry`（被恢复的会话；以指针重引基线、刷新 `task-delta`；证据 = 重锚定陈述）。**基线刷新只允许发生在 `session-entry` 与 `source-drift`**；`reentry` 只在同时命中基线刷新触发时重组基线。集合封闭：增删触发是 owner 修订。
- **FR-015**: owner 文档 MUST 以既有相对角色模型（`shared/definitions/superagent-definitions.md`）声明**组合者角色**：根会话在 `session-entry` 组合基线、在 `source-drift` 刷新它、在 `reentry` 以指针重引；superagent 在 `pre-dispatch` 组装每次派发的载荷与基线指针；被派发的执行者只完整加载它收到的指针，MUST NOT 重新收集上下文、MUST NOT 继承兄弟会话的记录、MUST NOT 从会话历史组合。本机制不引入角色值、深度规则或授权。
- **FR-016**: **来源漂移** MUST 是**可观测条件**而非轮询：项目已经记录的基线来源变化——宪法修订、指令刷新、词汇表或特性状态变化、git 工作流变化，或一个与已记录项目事实矛盾的新发现——在下一个基线刷新触发点触发**恰好一次**基线刷新（根会话执行）；证据是项目已保存的变化记录 + manifest 的 source reading（对已声明来源的解析路径、在场 token 与文件元数据的一次确定性摘要，绝不读内容）。机制 MUST NOT 新增 watcher、daemon 或后台检查。
- **FR-017**: 在派发边上，任务层由派发简报承载，经既有载荷通道送达：七个角色字段（其中 `authority_ref` 是指针字段）、四项声明注入（fast-fail 子句、并发义务、汇报义务、重锚定锚摘要）、与上行回传；owner 文档 MUST 以指针陈述该映射（字段与注入引用其 owner，绝不复述），并 MUST 声明该映射**不新增**任何角色字段、注入、上限、标识或自检项，不改变 `superagent-definitions.md` 的载荷规则。非派发场景下，同一组层经同一组声明行组合，不需要任何派发载荷。**适配说明**：源能力的 Tier G/Tier T 七组件包在本仓不存在（A-3b），本映射只落在真实通道上。
- **FR-018**: 四个声明事实 MUST 位于 `shared/declarations/facts/`，各经 `scripts/python/declaration_reader.py` 读取（引擎不得自带第二解析器、不得硬编码域成员）：`context-categories.yaml`（`invariant`、`variable`）、`context-layers.yaml`（`system`、`project`、`task`，按组合序）、`context-forms.yaml`（五个形态 token）、`context-classes.yaml`（每层→有序 class id 的映射，花名册）。四事实 MUST 在 `shared/declarations/contract.yaml` 以追加式注册块**先登记、后消费**（A-6 形态）。**声明事实**的未知或缺失成员（含缺失/不可读事实文件、未知 kind、不在封闭集内的成员）MUST 被拒绝：两个动作均退 `2`、不产出部分判定、不猜默认；迁移前没有声明层的项目是输入错误，不是降级通过。**边界**：owner 文档布局表中的未知层/形态 token 是记录级缺陷，不是输入错误——`check` 以 `unknown-layer` / `unknown-form` finding 报告（退 `1`），引擎绝不把它默认成合法 token。
- **FR-019**: 上限 MUST 引用、绝不重声明：每个 `bounded-index` 行 MUST 指名其 cap owner 的路径 + 小节——`shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First)（含升级阶梯与小文件阈值）；每个内容承载行（`read-in-full` 与 `inline-digest`）MUST 引用同一小节作为其例外/阶梯 owner。机制 MUST NOT 定义任何数值上限，事实与 owner 文档 MUST NOT 携带数值 bound 字段，审计 MUST 原样报告 cap 引用而非发明值；`bounded-index` 行缺少 cap 引用是 `cap-missing` finding。
- **FR-020**: 在场词表 MUST 在 owner 文档定义一次：正向 `present`（该行的每个常驻来源都可解析、可读且非空；`runtime-discovery` 行在其声明的探针成功时读 `present`）与四个缺席词 `absent`（常驻来源路径不存在）、`unreachable`（存在但不可读）、`empty`（可解析但存储为空——0 字节文件或空目录）、`not-evaluated`（没有可读的常驻来源：该行只有瞬态/使用期来源，或花名册类没有布局行因而无声明来源可读——原因点名缺失的布局行；运行期探针失败也读此词并带原因）。多来源行按声明来源次序报告**第一个失败来源**；每次缺席 MUST 带点名来源（或缺失布局行）的原因；静默省略与编造默认都是缺陷。一致性读数 `Unobserved` 按指针抵达 `shared/declarations/facts/evidence-seven-states.yaml#/statement`——MUST NOT 读成 `present`，MUST NOT 读成「一致」。
- **FR-021**: 一个只读审计引擎 `scripts/python/context-audit.py`（安装于 `.specify/scripts/python/context-audit.py`）MUST 是唯一审计入口，并由 framework-map 一行注册。它 MUST：解析 owner 文档的布局表并经 `declaration_reader` 读取四事实；提供 `--action check`（完整性：花名册逐行成员与次序、层与形态 token 对值域、形态×层矩阵、类 id 唯一、层非空、`bounded-index` 行的 cap 引用在场、无类别列——恰为九个规则 `roster-mismatch`、`roster-order`、`unknown-layer`、`unknown-form`、`layer-form-illegal`、`duplicate-class`、`empty-layer`、`cap-missing`、`category-column`；每条 finding 点名文件、行与违反的规则；退 `0` 干净、`1` findings、`2` 用法/不可读输入/声明事实的未知或缺失成员）与 `--action manifest --layer <system|project|task>`（逐行 class、layer、form、解析出的 source(s)、在场 token 与原因、cap 引用；**行集是花名册**——没有布局行的花名册类仍打印，其 form/source/cap 读 `—`、token 读 `not-evaluated` 且原因点名缺失布局行；只要发出清单即退 `0`，缺席行含在内；用法或声明失败退 `2`）。旗标：`--workspace-root PATH`、`--json`（两个动作都接受；`check` 的 JSON 携带 findings 与 summary，`manifest` 携带有序键与按 token 计数）、`-h`/`--help`（同体）、`--version`（运行时派生的单行机器可读身份；无可达 `pyproject.toml` 时读 `unknown` 是允许形态）。用法错误集封闭：未知选项（含裸 `--` 之后）在任何动作前退 `2`；`manifest` 缺 `--layer` 或 `--layer` 不在值域退 `2`；`--layer` 与 `check` 同用退 `2`；无法解析 workspace root 或 owner 文档/事实缺失退 `2`。**层根规则**：workspace root 取 `--workspace-root` 或最近的含 `.specify/` 祖先；层根（owner 文档 + 四事实）是**被审计树自己的声明层**——`<workspace-root>/shared/`（框架源形态存在时）否则 `<workspace-root>/.specify/shared/`（安装形态），一处规则同时服务仓库树、fresh init 树与自带声明层的 fixture。引擎 MUST 遵守 `shared/definitions/script-interface-definitions.md`，写零文件、不开网络连接。
- **FR-022**: 审计 MUST 确定且诚实：对不变树两次运行逐字节相同；每条 finding 点名文件、行与规则；损坏来源以带原因的在场读数出现，绝不成为被跳过的行；引擎 MUST NOT 做语义任务选择或相关性排序（相关性留在组合者），MUST NOT 读取文档内容，MUST NOT 打印发现的宿主值或时间戳（解析出的根只以 workspace 相对路径呈现）；文本清单的末尾 MUST 携带一行 `source-reading: <digest>`（对已声明来源的解析路径、在场 token 与文件元数据的一次确定性摘要），使已记录的基线来源变化可在下次读数中观测——内容字节永不进入它。
- **FR-023**: 机制 MUST 随既有 publish → install → init 流分发：owner 文档、四个声明事实、`contract.yaml` 的四条注册行与审计引擎作为框架源随 `shared/` 与 `scripts/` 两棵树发布（`scripts/python/sync-mirrors.py` 投影 `shared → .specify/shared`、`scripts → .specify/scripts`），`specify init` 把它们装入客户项目的 `.specify/`，无需任何额外步骤；模板编辑经 `templates → .specify/templates` 镜像对落地；镜像 MUST 逐字节等同其源（由既有 mirror 流生成，绝不手改）。`shared/definitions/framework-map.md` MUST 新增三行：owner 文档、四个上下文值域事实的目录条目、审计入口（含文档化调用），每行 MUST 可解析。
- **FR-024**: 机制 MUST 离线且私密：审计路径上无网络访问、无自动传输；任何读数不消费原始用户文本或会话内容——审计只消费路径、存在性/可读性/空与非空的元数据与在场状态，**不打开任何文件内容**（因此符号链接与 `..` 逃逸也不能导出内容）；既有 feedback 红线与 confirmation gates MUST 保持不变，且 MUST NOT 被任何新门引用或加宽。
- **FR-025**: 组合义务 MUST 通过**一条** ambient 指令段抵达每个会话：`## Context Management(上下文管理)`（[[STR-001]]）写入 `templates/instructions-template.md`，并由既有生成器 `scripts/bash/generate-instructions.sh` 的**加性 section reconcile** 注入 `.specify/instructions.md`（live 文件保持为刷新基线；既有段 MUST NOT 被修改或删除）。段落为「摘要 + 指针」形态：指向 owner 文档与审计入口，陈述 baseline-once / task-per-selection、指针而非内容、缺席点名缺口三条规则；MUST NOT 携带布局表、类花名册或 cap 字面量。最终树上生成器的 `BUDGET:` 判决 MUST 为 `within`（在生成器既有声明的预算常量下，A-10）——MUST NOT 抬高预算常量、MUST NOT 裁剪既有段；实测装不下是必须上送的异常。
- **FR-026**: 本版本 MUST NOT 发布新的 `/speckit.*` 命令、技能包装、门、红线、watcher 或后台检查；文档化入口就是 FR-021 的只读审计调用。改/加命令、技能、门或红线超出本特性范围。
- **FR-027**: 机制 MUST 被守卫：contract/integration 守卫 MUST 钉住——布局花名册与四事实逐成员一致（两侧双向）、形态×层矩阵、层级落点契约（三合法格 + 三禁止组合 + 无类别列）、概念指针三元组（作为必需项目层行、作为各结构的声明载体、并在每个结构具名在场面上可读）、在场词表用法（每个缺席带原因、无第五词、`present` 只在一处定义）、`check` 的确定性（逐字节重跑）、只读容器性（前后哈希清单与零新文件）、ambient 段的指针形态（owner 路径在场；无布局表、无花名册、无 cap 字面量）、镜像逐字节等同、super↔sub 协议声明项集未变（边界守卫）、以及七触发/角色/`reentry` 语义的声明；**每条 `check` 规则 MUST 各有自己的 seeded-violation fixture，且变异演练证明该 fixture 的守卫测试在规则被禁用时转红**（观测量是守卫测试的判决，不是引擎的 finding 输出）；全部测试经 `scripts/bash/run-tests.sh` 单入口执行。一个在其主体损坏时不会转红的守卫本身即缺陷。
- **FR-028**: **概念一致性** MUST 是一条声明义务，由**一个不可省略的指针三元组**承载：`glossary` → `.specify/glossary.md`（由 glossary 协议 `shared/workflow/glossary.md` 登记）；`definitions` → `.specify/shared/definitions/` 下的概念定义 owner 文档（有界索引）；`explanations` → `.specify/skills.md`、`.specify/tools.md` 及按 `docs/concepts/documentation-model.md` 的解释型文档。槽位只携带指针——定义的含义留在其 owner，绝不复制进任何上下文。布局中三元组由项目层三行 `project-vocabulary`、`concept-definitions`、`concept-explanations` 承载，花名册与在场读数覆盖三者。槽位 MUST 出现在封闭结构集——root/superagent turn、subagent 派发载荷、记忆召回投影、恢复/重锚定重入面——且 owner 文档 MUST 逐结构声明其载体与指针形态（只映射既有通道：派发边为 `authority_ref` 指针字段 + 子代理 ambient 的 Documentation Map glossary 行 + 派发简报的阅读清单，A-15；本要求 MUST NOT 给 `superagent-definitions.md` 增加字段、注入、上限、标识或自检项）。每个结构的在场 MUST 经机制可读的具名面观测：manifest 的三个项目层行服务 turn、记忆召回投影与恢复/重入面（其载体是组合会话的基线行，一次读数服务三者）；派发载荷经固定通道（Documentation Map 的 glossary 行与简报阅读清单）加协议边界断言读取；仅靠声明而无在场面的结构是缺陷。缺席读数：入口的布局行缺失读 `not-evaluated`（manifest 行集是花名册，行仍打印，原因点名缺失布局行），声明来源缺失/不可读/为空分别读 `absent`/`unreachable`/`empty`；由此结构导出的一致性声称读 `Unobserved`（证据态 owner 按指针）——永不 `present`，永不一致。槽位成员稳定：增删入口是 owner 修订。
- **FR-029**: owner 文档 MUST 声明**层级落点契约**——两类别 × 三层矩阵恰有三个合法格，每格陈述定义、载体、允许形态（**按引用** FR-009，绝不复述第二份值列表）与内容-对-指针规则；其余三个组合（`invariant` × `task`、`variable` × `system`、`variable` × `project`）被点名禁止并出现在任何布局行之外。三格：(a) `invariant` × `system`——环境与现实事实，使用时从环境发现（`runtime-discovery`）或指向其约束 owner（`pointer`），永不由项目撰写、永不持久化；(b) `invariant` × `project`——项目 `.specify/` 内撰写或生成的事实，以 `read-in-full`（治理基线，零复制字节）、`pointer` 或有界索引携带；(c) `variable` × `task`——当前工作项的事实，逐任务选择、以 `bounded-index`、`pointer` 或 `inline-digest` 携带、任务结束即丢弃；派发边由 FR-017 的既有载荷通道承载，非派发时同一组行不用载荷组合。类别由层派生（FR-002），MUST NOT 成为布局列；审计经层与形态值域加花名册强制该矩阵，契约测试钉住三合法格与三禁止组合。

### Key Entities *(include if requirement involves data)*

- **Context category（上下文类别）**：层的任务相关性分类——`invariant` 或 `variable`；携带成员测试与声明成员。
- **Context layer（上下文层级）**：`system`、`project`、`task`；携带其类别、定义判据（事实 owner 的居住处）与其允许形态。
- **Context fact class（上下文事实类）**：一行布局——class id、layer、form、source(s)、owner、cap reference；审计检查与 manifest 打印的单元。
- **Context source（上下文来源）**：事实类物化自的制品路径、canonical 指针或发现形态；解析到一个既有 owner，或读为带原因的缺席。
- **Materialization form（物化形态）**：`pointer`、`read-in-full`、`bounded-index`、`runtime-discovery`、`inline-digest` 之一；携带形态×层矩阵与 cap 链接。
- **Composition trigger（组合触发）**：一个具名时刻——id、组合者角色、范围（基线或任务）、刷新语义与证据；协议声明的封闭触发集。
- **Context manifest（上下文清单）**：一层的审计读数——行含 source、form、在场 token 与原因、cap reference；确定且可重放。
- **Composer role（组合者角色）**：root session、superagent、被派发执行者；经既有相对角色模型解析，谁组合哪个范围。
- **Concept-pointer slot（概念指针槽位）**：不可省略的指针三元组（glossary / definitions / explanations）；缺席入口读一个在场 token，导出的一致性读数读 `Unobserved`，永不一致。
- **Layer landing cell（层级落点格）**：一个合法 (category, layer) 对，含定义、载体、允许形态与内容-对-指针规则。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性**零新增第三方依赖**——它新增一个 Python 标准库只读引擎，消费既有声明层与既有载体，并在既有 pytest 运行器与唯一测试入口下验收。表中 `Premises` 引用的 `EP-NNN` 由 plan 阶段 `## Execution Premises` 定义（本阶段只保留引用）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | 上下文管理运行时面：owner 文档（含布局表）、四个声明事实与注册行、只读审计引擎；宿主为既有 Python 标准库脚本层与共享声明读取器 | in-scope | 本规格：模型、布局花名册、触发协议、审计契约 | Python 标准库；对既有来源只读；无新存储、服务、网络、composer 或数值 cap | 本切片 | 布局完整性 + 确定性 + 只读容器性 + 缺席诚实 + 离线 init 运行 + 镜像等同 | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-018, FR-019, FR-020, FR-021, FR-022, FR-027, FR-028, FR-029 | EP-001 |
| RS-002 | super↔sub 派发协议（七角色字段 + 四项注入 + 上行回传 + 结算） | signed-contract | `shared/definitions/superagent-definitions.md` § The super↔sub Protocol | 既有声明的字段/注入/回传集——无本地 pin、不复述阈值 | `shared/definitions/superagent-definitions.md` | 本特性声明的映射不改变其任何字段、注入或载荷规则，且不新增标识/自检项 | FR-005, FR-017, FR-028 | EP-001 |
| RS-003 | agent 文件的 `## Project Context` 渲染 | signed-contract | `src/specify_cli/__init__.py`（agent render 路径） | 既有渲染行为；本特性不扩展 | `src/specify_cli/__init__.py` | fixture 渲染输出在本特性前后不变 | FR-005 | EP-001 |
| RS-004 | 任务层的记忆召回面 | signed-contract | `scripts/python/memory-utils.py --action recall`；scope 值域 `shared/declarations/facts/memory-types.yaml#/statement` | 既有召回行为与域；只读复用 | `scripts/python/memory-utils.py` | 召回输出在已填充 fixture 上原样消费，零改动 | FR-005, FR-008 | EP-001 |
| RS-005 | 守卫、镜像与分发 | in-scope | 本规格：五组守卫、ambient 指令段、镜像与 init 接线（走既有流） | 既有 pytest 运行器与唯一入口；`sync-mirrors.py`；零新依赖 | 本切片 | 逐规则种子违规守卫 + 镜像逐字节等同 + init fixture 段落在场 + 概念指针与落点守卫 | FR-023, FR-024, FR-025, FR-027, FR-028, FR-029 | EP-001 |

**Contract-cell note**: RS-002/RS-003/RS-004 是既有 owner，按指针消费、零编辑；本规格只交付 RS-001 与 RS-005。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 在本仓树上 `context-audit.py --action check` 退 `0` 且零 findings；四个种子违规 fixture（未知层 token、未知形态 token、花名册不匹配、层-形态非法）各退 `1` 并恰产出预期 finding；对每个不变 fixture 连续两次运行逐字节相同。 **Path**: final
- **SC-002**: 每个审计动作在一个具名 fixture 族与本仓库树上：动作前后同一棵树的内容哈希清单（路径、SHA-256、大小）逐字节相同，允许增量集合为空（解释器字节码缓存按名排除），全树零新文件。 **Path**: final
- **SC-003**: 在「一来源缺失、一记忆根存在但为空、一来源存在但不可读」的 fixture 上，`--action manifest` 逐行恰好读 `absent`、`empty`、`unreachable` 并带原因、不省略任何行；在「全来源在场」fixture 上每行读 `present`，无任何缺席 token 出现。 **Path**: final
- **SC-004**: 形态×层矩阵被强制：一个任务层 `read-in-full` 行加一个系统层 `bounded-index` 行的合并 fixture 恰产出**两条**层-形态 findings（且无其它 finding）；本仓自己的布局零违规。 **Path**: final
- **SC-005**: 在阻断网络的新初始化项目上，`check` 退 `0`、`manifest --layer project` 完成并对真实缺失来源给出显式缺席行；两次运行中 socket 打开数 = 0、传输 = 0。 **Path**: final
- **SC-006**: 本仓布局中每个 `bounded-index` 行指名的 cap owner 路径 + 小节可解析；四个声明事实不含数值 bound 字段；对本特性持久增量（owner 文档、四事实、引擎、模板段与其 live 段）的扫描中「cap 单位旁的数值字面量」命中数为 0。 **Path**: final
- **SC-007**: `context-categories`、`context-layers`、`context-forms` 的每个成员至少被一处测试或引擎动作**实际行使**（行使定义：该成员被变更/缺失时，某条断言或动作输出出现可观测差异），声明与引擎逐成员一致，未知或缺失的**声明**成员以 `2` 被拒。 **Path**: final
- **SC-008**: 一次 `scripts/bash/run-tests.sh` 全量运行报告相对 implement 入口基线零新增失败名；镜像与其源逐字节等同；super↔sub 协议的声明项集、`memory-utils.py --action recall` 在已填充 fixture 上的输出、以及 agent 渲染 fixture 输出均与基线一致（基线：implement 入口提交上的同 fixture 输出）。 **Path**: supporting
- **SC-009**: 新初始化项目生成的指令含 `## Context Management(上下文管理)` 段，且守卫证明其指针形态——owner 路径与审计入口在场；无布局表、无类花名册、无 cap 字面量；最终树上生成器 `BUDGET:` 判决为 `within`。 **Path**: final
- **SC-010**: 在本仓树上 `--action manifest --layer project` 列出三个概念指针行（`project-vocabulary`、`concept-definitions`、`concept-explanations`），各读 `present` 且来源可解析；在「删去一个概念指针布局行 + 一个来源不可读」的种子 fixture 上，manifest 仍打印被删的行（行集是花名册）读 `not-evaluated` 且原因点名缺失布局行、不可读来源行读 `unreachable`、受影响结构的一致性读数读 `Unobserved`，输出中无任何「一致」或对该结构报 `present`；该 fixture 的布局-花名册不匹配另可由 `check` 的 roster-mismatch finding（退 `1`）单独断言（两读数可共现，本判据不要求）；协议边界守卫证明派发边映射未给 super↔sub 协议增加字段、注入、上限、标识或自检项。 **Path**: final
- **SC-011**: owner 文档的层级落点契约恰声明三个合法 (category, layer) 格（含载体、形态与内容-对-指针规则）并点名三个禁止组合；契约测试钉住这些格、布局无类别列、且每个布局行的层与形态落在其合法格内。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 经 `scripts/bash/run-tests.sh` 的 contract/fixture 运行：`check` 的完整命令行、stdout/stderr、退出码与耗时按单次运行证据捕获（每 fixture 一次 + 一次重跑做逐字节比对）；基线是 fixture 的预期 finding 清单。
- **SC-002 Source**: 同一测试运行内、每个审计动作前后对 fixture 树计算 SHA-256 哈希清单（同测试按名排除字节码缓存）；该清单是容器性腿的具名基线参照物；仓库树读数同规。
- **SC-003 Source**: 三个用途构 fixture（缺失来源、空存储、不可读路径）上的 `--action manifest --json` 机器输出，逐行断言预期在场 token。
- **SC-004 Source**: 合并层-形态 fixture 的 `check` 输出与退出码，加本仓 `check` 运行；findings 按规则 id 与条数断言。
- **SC-005 Source**: init fixture 集成测试：CLI 初始化项目、测试壳阻断网络、两个审计动作全量捕获；socket 守卫断言在同一次运行记录。
- **SC-006 Source**: 解析布局表全部 cap 引用的契约测试 + 四事实数值 bound 字段的静态扫描输出；每次运行捕获。
- **SC-007 Source**: 每个声明一个封闭集契约测试 + 未知/缺失声明成员拒绝用例；引擎自身 `check` 输出确认声明一致。
- **SC-008 Source**: `scripts/bash/run-tests.sh` 的全量输出，按名与 implement 入口基线比对；`sync-mirrors.py --check` 输出；协议边界守卫与 `memory-utils.py --action recall` 及渲染 fixture 输出（变更前后各一次）。
- **SC-009 Source**: fresh init fixture 上的指令生成测试 + ambient 段守卫断言 + 生成器 `BUDGET:` 行，同一次运行捕获。
- **SC-010 Source**: 仓库树与「布局行删除 + 来源不可读」种子 fixture 上的 `--action manifest --json` 机器输出逐行断言；同一 fixture 上可选的 `check` roster-mismatch 共现读数；协议边界守卫输出；由 manifest 缺席 token 按证据态 owner 导出的一致性读数。
- **SC-011 Source**: 落点契约测试输出（三合法格、三禁止组合、无类别列）+ 本仓布局的 `check` 运行，同一次运行捕获。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "Context Management(上下文管理)" | FR-001, FR-025, owner-document definition site, ambient-section guard |
| `STR-002` | "Invariant(不变)" | FR-002, owner-document definition site, tests/contract guard |
| `STR-003` | "Variable(可变)" | FR-002, owner-document definition site, tests/contract guard |
| `STR-004` | "System(系统级)" | FR-003, owner-document definition site, tests/contract guard |
| `STR-005` | "Project(项目级)" | FR-003, owner-document definition site, tests/contract guard |
| `STR-006` | "Task(任务级)" | FR-003, owner-document definition site, tests/contract guard |

**Citation convention**: 当契约、任务或测试引用这些字符串之一时，写 `[[STR-NNN]]` 而不是复制字面量，使一次轮换只需编辑本表。

## Clarifications

<!-- 无人值守裁决：本轮不发起阻塞式提问；brief 的歧义清单逐条在 Assumptions 裁决并在此记录。 -->

### Session 2026-11-27

- Q: 规格编号、分支与脚手架如何落地？ → A: **编号 110、分支保持 `110-context-management`**；`create-new-requirements.sh` 会把当前本地分支计入编号空间而派生 111 并新建分支，按 107/108 先例手工从 `.specify/templates/requirements-template.md` 脚手架并记录偏差（A-16）。
- Q: `Related Feature` 绑定谁，是否复用源能力注册编号？ → A: 绑定 **Feature 110 `Context Management（上下文管理）`**，独立新特性；**不复用** ai-harness 的 Feature 098 注册编号；本阶段不编辑 `.specify/features.md`（本线约束），索引/详情登记由 clarify 按 Feature Integration Protocol 完成（A-2）。
- Q: `.ah` / `/ah.*` / `ai-harness` / 源仓的 src/ai_harness 如何适配？ → A: 逐条映射为 `.specify/` / `/speckit.*` / `Spec Kit` / `src/specify_cli`；每个目标路径已核验存在（A-3）；不存在的传感器（渲染器、七组件包、缺席词 owner、per-slot caps）按缺失传感器处理，绝不伪造（A-3、A-8、A-15、FR-019）。
- Q: 源的四缺席词在仓内没有 owner，怎么办？ → A: 在场词表（`present` + 四缺席词）由新 owner 文档**一次定义**；`Unobserved` 仍按指针抵达证据态声明（A-8）。被拒方案是挂一个不存在的 owner 路径。
- Q: 派发边没有 Tier G/Tier T 七组件包，映射到什么？ → A: 映射到本仓真实载荷面：七角色字段（`authority_ref` 为指针字段）、四项注入（重锚定锚摘要承载基线指针）、上行回传；机制不新增任何角色字段、注入、上限、标识或自检项（FR-017、A-15）。
- Q: 上限引用谁？ → A: `shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First)（含升级阶梯与小文件阈值），作为 `bounded-index`、`read-in-full` 与 `inline-digest` 行的唯一 cap/例外 owner；机制零数值上限（FR-019、A-7）。
- Q: 存储如何登记？ → A: **无存储登记**：机制只读，不创建任何运行时存储根；唯一持久增量是 A-11 的封闭集（owner 文档、四事实、四条注册行、引擎、守卫/fixtures、ambient 段、框架地图三行）。
- Q: 分发面与 init 行为？ → A: owner 文档 + 四事实 + 注册行 + 引擎随 `shared/`/`scripts/` 两树经 publish → install → init 落地（镜像 `.specify/shared`、`.specify/scripts`）；ambient 段经 `templates → .specify/templates` 镜像与生成器 reconcile 落地；框架地图新增三行（A-12、FR-023）。
- Q: 源的 ambient 段是否能力专属、是否携带？ → A: 是能力专属段，随本特性携带并改写路径措辞；不导入任何无关 hunk；生成器预算余量约 790 B，最终 `BUDGET:` MUST 读 `within`，不提额不裁旧段（A-10、FR-025）。
- Q: 五个源测试模块如何映射？ → A: `test_context_management_owner.py` / `test_context_management_declarations.py` / `test_context_management_engine.py` / `test_context_management_readonly.py`（contract）与 `test_context_management_init.py`（integration）原样沿用名称，fixture 族置于 `tests/fixtures/context-management/`，全部经 `scripts/bash/run-tests.sh` 执行（FR-027、A-17）。

## Out of Scope

- 上下文窗口的压缩、摘要或截断算法；token 计数或优化引擎；本特性自有的上下文预算数字。
- 持久上下文存储、缓存、索引、快照或渲染产物。
- 由审计引擎执行语义（关键词/嵌入）自动选择；相关性选择始终属于组合者。
- 替换、扩展或重定义任何既有 owner：super↔sub 派发协议、agent 文件渲染、记忆召回、Documentation Map、token 效率纪律、声明层。
- 任何新 `/speckit.*` 命令、技能包装、门、红线、watcher、daemon 或后台检查。
- 网络访问、远程上下文获取、遥测或任何传输。
- 超出既有派发边模型的多 agent 上下文共享：兄弟之间仍然什么都不共享。
- 对概念「语义一致」的验证（理解、翻译准确性、模型信念）；机制只检查指针在场与可解析。
- 通过改变 super↔sub 协议的字段、注入、上限、标识或自检项来承载概念指针槽位。
- 运行期存储迁移（105 的领域）与决策治理对齐（107/091 各自独立，不互相对齐）。
- 抬高 `generate-instructions.sh` 的预算常量或裁剪既有指令段（稳定第一；若 ambient 段装不下，按异常上送）。
- 审计性能目标（除「对花名册与来源列表线性」的设计目标外，不设数值 SLA）。