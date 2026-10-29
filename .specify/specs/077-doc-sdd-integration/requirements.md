# Requirements Specification: 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）

**Requirement Branch**: `077-doc-sdd-integration`
**Created**: 2026-10-30
**Status**: Draft
**Flow Class**: execution
**Input**: User description: "把**项目文档**的开发接入 SDD 阶段链，使 `sdd-loop-driver` 能无人值守驱动文档开发。项目文档与办公文档不同：项目文档应像代码一样有严密的结构和逻辑；接入后应能无人值守开发。"

> **本行的由来（自用声明）**：标题区那一行类别字段（[[STR-001]]）正是本特性要建立的字段，此处先行自用。本特性的交付物是命令模板、驱动技能与确定性检查器，缺陷最先以行为暴露，按 069 的判据属 `execution`（理由见 § Assumptions A6）。接线落地前该字段不被任何阶段读取；落地后即成为本线的生效取值。

## Related Feature *(mandatory)*

**Feature ID**: 077
**Feature Name**: 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）

**绑定结论**：绑定**新建 Feature 077**（`Draft`，2026-10-30 用户裁决立项）；登记行与详情文件随本阶段落盘。**不**把本规格挂到任何既有 Feature 名下。

**与 Feature 069 的关系（直接前序；只引用、不回写）**：Feature 069（执行/表达二元分类与文档型 SDD 同构，`Implemented`）建立了分类判据、唯一所有者、逐流程台账、六面文档型门禁与阶段算子表；其规格的 Out of Scope 明确写着「不新建表达类专用命令集，也不新增 `/speckit.*` 命令」并把阶段命令接线留给后续特性。本特性承接的正是这件被显式推迟的事——**让既有阶段命令与驱动真正按类别运行**，而不是再定义一遍类别。069 的两个切片（`069a` 分类与门禁落地、`069b` 同构映射与度量）也都已 `Implemented`：它们交付的是「类别存在且可查」「映射存在且可核」，本特性交付的是「阶段命令与驱动按类别执行」。因此 069 的状态 MUST NOT 因本特性回退，其正文 MUST NOT 被本特性改写。

**reuse-first 复核（宪法 VII；判据是「该 Feature 是否已拥有本特性要建立的能力」，不是「是否持有交付载体」）**：

| 候选 Feature | 与本特性的关系 | 裁决 |
|---|---|---|
| 069 执行/表达二元分类与文档型 SDD 同构 | 拥有判据、取值、台账、六面门禁与阶段算子表；不拥有阶段命令的接线，其 Out of Scope 显式推迟 | 前序 owner，不是归属 |
| 069a / 069b 切片规格 | 069 的切片，不是独立 Feature；均已 `Implemented` | 不构成归属 |
| 058 无人值守 SDD 循环驱动机制 | 拥有 `sdd-loop-driver` 这一交付载体与阶段编排；不拥有类别判据，也不拥有门禁算子 | 载体 ≠ 归属；本特性对其载体做「类条件」扩展 |
| 067 循环效率加固（规格实存、索引未登记，既有缺口不在本特性范围） | 拥有两槽位测试预算的时点与审计口径；不拥有类别，也不拥有文档门禁 | 不重写其规则；只增加类别分支 |
| 062 Humanize Command | 表达类首个实现；不拥有阶段命令接线 | 无关 |
| 074 Goal/Team/Agent 与 SDD 统一 | 编排与目标层；对象是团队与目标的协同，不是阶段门禁算子 | 无关 |
| 076 决策反题契约 | 计划层的决策记录与证伪四元组；对象不同 | 无关 |

**结论与理由**：069 及其切片都已关闭，且其规格把「阶段命令接线」明确划到后续特性；058/067 持有的是载体与既有规则，不持有「按类别切换门禁」这一能力。把本规格挂到任一既有 Feature 都会让「已关闭」的契约被重新解释；因此新建 077 承接，并在 069 与 058/067 的 owner 文件中只做**类条件追加**，不重写既有条款。

## 现状锚点（2026-10-30 本机实测；dated record，仅作可行性输入，非运行时保证）

- **分类轴已存在，但对象是流程单元，不是特性**：`python3 scripts/python/flow-class-check.py --action check` 报 `79 unit(s) scanned, 0 finding(s)`、`ledger_rows=79 matched=79 inventory_units=79 gaps=0`（27 个命令模板 + 52 个技能）；`--action lookup --unit-id "/speckit.implement"` 返回 `flow_class: execution`、`basis: mixed-oracle`、`source: ledger`。特性索引 `.specify/memory/features.md` 没有类别列，Feature 详情文件也没有该字段。
- **引擎只认两类键**：`--action lookup --unit-id "feature:077"` 返回 `invalid unit id 'feature:077': expected /speckit.<stem> or skill:<dir>`、退出码 2（同时仍打印一条 `source: default` 的降级记录）。特性级类别需要一个自己的键族，且不能被当成「格式非法的单元」。**键族裁决见 § Clarifications 第三条：`spec:<spec 目录名>`，`feature:<ID>` 不予采用**（同 Feature 多切片必然指错线）；本行是 as-of 2026-10-30 的实测记录，保留原样。
- **七个阶段命令模板零接线**：`templates/commands/` 下 `requirements` / `clarify` / `plan` / `tasks` / `checklist` / `analyze` / `implement` 七个模板对 `flow_class` / `flow-class` / `expression` 零命中；已接线的只有 `docs.md`、`review.md`、`humanize.md` 三个。
- **门禁算子表已就绪且自洽**：`shared/workflow/expression-gates.md` 有封闭六面与 16 行阶段算子（八阶段各 2 行）；`--action isomorphism` 报 `8 stage row(s), 6 gate face(s), 0 finding(s)`，`--action faces` 报 `6 face(s) parsed, 0 finding(s)`。
- **驱动侧无类别感知**：`skills/external/sdd-loop-driver/` 的 `SKILL.md` 与 `references/*.md` 对 `flow_class` / `flow-class` / `expression` 零命中；两槽位测试预算的时点是 implement 起点（baseline）与 review 之后（closure），`not-run-docs-only` 只是定向集阶段的一种 `stage-status`，不是槽位语义。
- **069 的推迟是白纸黑字**：`069` 规格 § 显式排除项含「不新建表达类专用命令集，也不新增 `/speckit.*` 命令」，并把项目侧声明面记为「属后续特性」。
- **登记现状**：`features.md` 行数 72（注册本特性**之前**）、最大编号 076（075 未使用，编号不连续）；`.specify/specs/` 最大目录 076。本特性登记后行数为 73。

## Assumptions（对输入中开放点的缺省裁决，clarify 阶段可推翻）

- **A1（编号依据）**：编号 077 由脚手架 `create-new-requirements.sh` 派生——`.specify/specs/` 下最大目录为 `076-decision-tension-contract`，故下一个为 077；`features.md` 的「Total Features」是行数（72），不是最大编号，两者不一致（075 缺号）属既有状态，本特性不借机回填。
- **A2（类别当前按单元、不按特性——实测事实）**：判据与台账的覆盖对象是命令模板与技能（79 个单元，0 缺口）；引擎只解析 `/speckit.<stem>` 与 `skill:<dir>` 两类键，对其他键报 `invalid unit id` 并退出 2。**特性级类别是新增对象族，不是既有能力的别名**，因此必须有可判定、可降级的解析面，不能靠「读 feature 详情里的一句话」。
- **A3（接线改动面的边界，含一处计数纠正）**：派发文本一处写「六个命令模板」、同句又枚举了 `requirements/clarify/plan/tasks/checklist/analyze/implement` **七个**名字。以枚举为准：接线面 = **七个**命令模板 + 驱动技能及其 `references/`。依据：`clarify` 同样是零命中的阶段命令，且门禁 owner 的阶段算子表为 clarify 登记了两行算子；把 clarify 排除会让该阶段成为唯一无类感知的阶段，与「每阶段按类换算子」直接冲突。**clarify（2026-10-30）复核确认：七个，不改判**（复核证据：`for f in requirements clarify plan tasks checklist analyze implement` 逐模板 grep 三类关键词，七个模板命中数全为 0；`expression-gates.md` 阶段算子表中 clarify 有两行）。
- **A4（声明位置裁决：requirements 头部字段）**：三选一中选 **requirements.md 的头部字段**，理由五条——① **时序**：requirements 是链上第一个阶段，也是第一个做门禁判定的阶段；若声明落在 clarify 才创建的 Feature 详情里，第一个阶段必然在错误门禁集下运行，之后才翻转，正是要禁的「静默切换」。② **共址**：七个阶段命令与驱动都以 spec 目录为输入，声明与产物同目录，零额外查找。③ **单一性**：特性索引与详情至多留指针，避免出现第二份分类数据。④ **可判定**：单行定值字段、封闭取值，解析成本最低；而在 76 行宽表上加列会让每行出现空值，把「未声明」变成默认态。⑤ **切片友好**：一条特性线 = 一条 spec 目录，多切片特性各自声明（见 A5）。clarify 若裁定改位，MUST 同步改本文件的 FR 与 Shared Strings。**clarify（2026-10-30）复核确认不改位**，只把行形态、重复/错位判定与非法值处置钉死（FR-001 / FR-005 与 § Clarifications 首条）。
- **A5（声明单位 = 特性线）**：类别按**特性线**（一条 spec 目录）声明，不按 Feature 编号聚合；同一 Feature 的多个切片允许不同类别（例：069a 交付引擎属执行、069b 交付映射文档属表达），注册表不汇总为一个取值。跨线并发时类别按线解析，不得用进程级/环境级全局值跨线复用。
- **A6（本特性自身按判据属 execution）**：本特性交付命令模板、驱动技能、owner 文档与确定性检查器，缺陷最先以「阶段命令不读类别」「驱动放行了缺证据的阶段」这类行为差异暴露，按 069 判据为 `execution`；本特性不替自己主张表达类，也不因此获得任何门禁豁免。
- **A7（脚手架偏差，披露）**：因当前分支已是 `077-doc-sdd-integration` 且派发禁止切换分支，脚手架在**仓库外**调用，使其判定无 git 上下文而跳过分支动作（stderr 留痕 `skipped branch creation for 077-doc-sdd-integration`）；编号与 spec 目录创建能力照用，分支保持 `077-doc-sdd-integration` 不变。若在仓库内调用，脚本会把已存在的 077 分支计入编号源并派生出 078，与你指定的目录冲突。
- **A8（绑定与登记时点偏离默认协议）**：默认把 Feature 绑定推迟到 `/speckit.clarify`；本轮按调用方要求在本阶段完成绑定并落登记行与详情文件，属显式偏离，已在此登记为恢复点。
- **A9（无新增持久编号）**：本阶段未引入 D-/OI-/REC- 等持久编号；若 plan 取号，须按 ID Register 在取号当刻登记 `.specify/memory/register.md`。
- **A10（术语与所有者）**：`flow_class`、`execution`、`expression` 的语义、判据、台账与同义消歧归 069 与 `shared/definitions/flow-class-definitions.md`；六面、算子表、阻断级别、读者声明与证据语法归 `shared/workflow/expression-gates.md`。本文件只引用，不重定义、不复述判据句。
- **A11（形制留待 plan）**：具体命令、退出码、字段子结构、检查器文件名、模板文本（除已钉住的 Shared Strings）属 plan；本文件只固定语义、所有权与可判定验收面。**clarify（2026-10-30）已把四处形制提前钉住**（超出本条原意，属显式偏离）：特性线键形态与三段退出码（FR-003）、四个子节标题与列语义（FR-013，新增 STR-003…STR-006）、`--action structure` 的归属检查器（FR-013 / FR-023）、槽位字段的取值语义（FR-020）——不钉住它们，验收面就无法只读退出码与记录字段判定。其余形制（行内字段子结构、错误文本、测试文件名、plan 模板文本）仍归 plan。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一条特性线声明自己的类别，任何阶段都能在判定前读到它 (Priority: P1)

特性作者在 `requirements.md` 头部写一行类别（`execution` 或 `expression`）。之后无论跑 requirements、clarify、plan、tasks、checklist、analyze 还是 implement，命令都在做门禁判定之前从**同一个**解析入口拿到这个值，并显示它是「已声明」还是「未声明·按默认」。作者不需要维护第二份声明，也不会遇到「索引里写 A、规格里写 B」的自相矛盾。

**Why this priority**: 没有可声明、可解析的载体，后面所有「按类切换」都无从谈起；而如果载体在链上出现得太晚，第一个阶段就已经跑错门禁集。

**Independent Test**: 三个夹具规格——声明 `expression`、不写该字段、写一个非法值——各跑一次解析入口，只读退出码与记录字段即可判定（依次为已声明/未声明带默认标记/阻断错误）。

**Acceptance Scenarios**:

1. **Given** 一条 `requirements.md` 头部写了 `expression` 的特性线，**When** 任一阶段在门禁判定前解析类别，**Then** 得到 `expression` 且来源字段标明「已声明」，退出码 0，无需读取特性索引或详情。
2. **Given** 一条没有该字段的特性线，**When** 解析类别，**Then** 得到 `execution` 且来源字段标明「未声明」并带 069 已登记的默认标记；该结果 MUST NOT 被当作「作者已判定」。
3. **Given** 一条把取值写成封闭集之外文本的特性线，**When** 跑 requirements 阶段门禁，**Then** 门禁阻断并点名该行，MUST NOT 静默按 `execution` 继续。

---

### User Story 2 - 表达类特性走完整八阶段，但每阶段的门禁换成语义上能证伪文档的算子；执行类一点没变 (Priority: P1)

文档型特性的作者仍然走 requirements → clarify → plan → tasks → checklist → analyze → implement → review，一个阶段都不少，但每个阶段的判定换成了读者声明、证据等级与 as-of、结构/链接/构建、事实一致性、评审这些真正能证伪文档的算子；不再被要求拿测试覆盖率证明一段说明文是对的。与此同时，执行类特性跑同一批命令时，看到的阻断项、必填章节和判定结论与改动前逐项一致。

**Why this priority**: 这是用户价值的落点——分类若换不来门禁算子的实际切换，就只是标签；而如果切换让执行类回退，整个框架先受损。

**Independent Test**: 一条表达类夹具线跑七个阶段，检查每阶段都有本阶段登记的 blocking 算子结果、且代码型算子未被继承；同一批命令在一条执行类夹具线上跑，与基线提交的判定集合逐项比对为空差。

**Acceptance Scenarios**:

1. **Given** 一条表达类特性线，**When** 跑任一阶段的门禁，**Then** 执行该阶段在算子表中登记的 blocking 算子；任一 blocking 面为 `not-evaluated` 时该阶段判未通过，而不是记绿。
2. **Given** 一条执行类特性线，**When** 跑同一批阶段命令，**Then** 新增阻断检查 0、新增必填章节 0，门禁判定集合与基线提交逐项相同。
3. **Given** 类别解析入口缺席（owner 文件不可读或引擎不存在），**When** 跑执行类阶段，**Then** 打印 `owner-unavailable` 并保持既有门禁集，流程不被中断，也不新增失败。
4. **Given** 有人试图用「本线属表达类」为由跳过 analyze 或 review，**When** 阶段记录核对，**Then** 该请求被拒，两个阶段的调用率仍为 100%。

---

### User Story 3 - 表达类的 plan 产出可核对的文档结构，implement 按结构落文并过四面门禁 (Priority: P1)

文档作者在 plan 阶段不只写「打算写什么」，而是写出一棵章节树：每节的名称、读者读完要做的决定、父节、明确不覆盖的边界；再加基准读者与阅读场景、每条事实的证据三件套、每条事实的唯一 owner 路径。implement 阶段按这棵树落文：计划里的节必须都在，计划外的顶层章节不许冒出来；每条事实性断言都要在证据清单里有对应行，同一事实只许有一个 owner。这样「文档像代码一样严密」就不是形容词，而是能红能绿的判定。

**Why this priority**: 用户对「项目文档要与代码同等严密」的要求，只有落到 plan 的结构产物与 implement 的四面门禁才成立；否则所谓文档型 SDD 仍只是换了一套口号。

**Independent Test**: 一个合规 plan 夹具通过；四个负向夹具（缺章节树、缺读者行、证据条目缺 source、同一事实两个 owner）各自转红；implement 夹具出现一个计划外顶层章节时转红。

**Acceptance Scenarios**:

1. **Given** 一条表达类特性线的 plan，**When** 检查结构章节，**Then** 章节树、基准读者与阅读场景、证据清单、事实 owner 清单四项齐备，缺任一即判违规。
2. **Given** 一份已批准的文档结构与一次 implement 落文，**When** 只比对章节标题与计划表，**Then** 缺失的计划章节、计划外的顶层章节都被点名，判定不依赖通读正文。
3. **Given** 文档里写了一条事实但证据清单没有对应行，**When** 跑证据面门禁，**Then** 该断言被判违规，而不是因为「句子通顺」放过。
4. **Given** 同一事实在文档与另一处被各写一遍，**When** 跑事实面门禁，**Then** 判违规并指向两处；修复方向是改为引用唯一 owner，不是把措辞改一致。

---

### User Story 4 - sdd-loop-driver 能无人值守驱动表达类特性，而不是按代码型默认放行 (Priority: P2)

驱动者在派发每个阶段时把该线的类别写进子代理提示词；本地原生子代理与远端 CLI 两种拓扑都带同一个值。表达类线到 U4 时，除了哨兵与产物，还要校验该阶段的门禁证据；两槽位测试预算在这类线上装的是两次文档门禁（implement 起点一次、review 后一次），缺槽位就报违规，不会静默跳过、也不会写个 0 冒充跑过。

**Why this priority**: 没有驱动侧接入，无人值守就只能跑执行类；而如果驱动仍然「哨兵在就放行」，表达类会在没有任何门禁证据的情况下被一路推完。

**Independent Test**: 一条表达类线的 implement 记录具备哨兵与产物但缺门禁证据，U4 判未完成；状态脊里两个文档门禁槽位各出现一次且时点正确，缺一个时既有审计报违规。

**Acceptance Scenarios**:

1. **Given** 一条表达类线被派发，**When** 检查阶段提示词，**Then** 其中携带已解析的类别、来源与标注；子代理不自行推断，缺该字段即判派发构造缺陷。
2. **Given** 表达类线的某阶段有哨兵与提交，但门禁证据缺失，**When** U4 校验，**Then** 判未完成，不派发下一阶段。
3. **Given** 表达类线进入 implement 与收尾，**When** 读状态脊的两槽位围栏，**Then** 两个槽位各恰好一次、时点为 implement 起点与 review 之后；未运行不得记 0 或记通过。

---

### Edge Cases

- **同一条特性线两处声明**：requirements 头部与 Feature 详情各写一份 → 判缺陷（第二份是第二真源），由确定性检查报出，而不是靠评审读出来。
- **类别在多切片间不同**：同一 Feature 的切片 A 声明 `execution`、切片 B 声明 `expression` → 合法；每次阶段运行只读本切片，注册表不汇总。
- **声明在 requirements 门禁通过后才写**：判 re-baseline，按新类别重跑 requirements 门禁集并记入阶段记录；不得静默翻转。
- **类别声明为表达、但该线同时产出可执行脚本**：代码型算子按**产物**补回（测试/编译针对那些产物），类别不变、其余阶段不因此改判。
- **引擎/owner 缺席**：打印 `owner-unavailable`，保持执行类门禁集，不中断、不静默切换、不把降级当通过。
- **未刷新的客户项目**：拿到的是旧命令副本与旧驱动技能，没有类别读取，行为与刷新前一致（零行为变化是判定标准，不是缺陷）。
- **远端拓扑**：提示词是类别的唯一载体，环境变量不被远端子代理继承；本地拓扑同样以提示词为准，两边不得各带一个值。
- **两条不同类别的线在同一仓库并发**：类别按线解析；出现跨线泄漏（另一条线拿到别线的类别）即缺陷。
- **站点层不存在**：构建算子记 `not-applicable`（显式），不得记通过。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 类别声明与解析（US1）

- **FR-001**: 每条特性线 MUST 在其 `requirements.md` 的头部区（`## Related Feature` 之前）声明恰好一行类别字段 [[STR-001]]，行形态逐字为 `**Flow Class**: <value>`——[[STR-001]] 后接半角冒号、一个空格、取值，行尾 MUST NOT 有尾随空白，字段名与取值均大小写敏感（全角冒号、大小写变体、行内附加注释一律不合语法）；取值 MUST 为封闭集 `execution` / `expression`；值 MUST 只由作者判定，MUST NOT 由脚本从路径、文件名或内容推断。该行出现第二次（不论两次取值是否相同）MUST 判 `declaration-duplicate`；出现在 `## Related Feature` 之后 MUST 判 `declaration-misplaced`；两个码 MUST 由确定性检查报出，MUST NOT 依赖人工阅读发现。
- **FR-002**: 类别声明 MUST 单一：`.specify/memory/features.md` 与 `.specify/memory/features/<ID>.md` MUST NOT 保存该特性线的类别取值（至多留指向声明行的指针）；同一特性线出现第二处声明 MUST 判为缺陷并由确定性检查报出，MUST NOT 依赖人工阅读发现。
- **FR-003**: 类别解析 MUST 复用既有唯一读取引擎 `scripts/python/flow-class-check.py --action lookup`：该引擎 MUST 能按特性线键解析出与流程单元**同形**的记录（类别、`source`、`marker`、`basis`）；MUST NOT 新增第二份分类数据文件、MUST NOT 新增第二条读取路径、MUST NOT 新建第二个解析函数。特性线键 MUST 取 `spec:<spec 目录名>`（如 `spec:077-doc-sdd-integration`，键族并入同一 `--action lookup`）；MUST NOT 接受裸目录名，MUST NOT 以 `feature:<ID>` 为键——同一 Feature 的多条切片线（`069` / `069a` / `069b`）各自独立声明，Feature 键必然指错线。记录字段集 MUST 与单元键同形：`unit_id` 取键原文、`source` 取 `declaration`（已声明）或 `default`（未声明）、`basis` 为 `null`（判定依据是台账列，声明不携带）、`neutral` 为 `false`。退出码 MUST 分三段：**0** = 已解析（含未声明按默认，此时 `marker` 为 069 登记的默认标记）；**1** = 已声明但取值不在封闭集内（`invalid-class`，阻断，MUST NOT 与 2 合并）；**2** = 键或输入非法、spec 目录不存在、owner 不可解析（`owner-unavailable`，沿用既有前置：owner 先于匹配解析）。特性线声明 MUST NOT 写入逐流程台账——台账行集等于框架单元清单，写入即产生 `unknown` 发现。
- **FR-004**: 未声明类别的特性线 MUST 按 `execution` 运行，`source` MUST 标为 `default`（未声明），并在每个消费点显示 069 登记的默认标记（该标记的语义与字面归 069 § Shared Strings，本文件不复述其文本）；未声明 MUST NOT 被呈现为已判定，也 MUST NOT 被读作表达类。同一解析记录 MUST NOT 同时携带该默认标记与 `source: declaration`——两者互斥，同时出现即第三态缺陷。
- **FR-005**: 已声明但取值不在封闭集内 MUST 按**阻断错误**处理：声明所在阶段的门禁 MUST 失败并点名该行；MUST NOT 静默回落默认类、MUST NOT 继续以 `execution` 运行。解析侧 MUST 以退出码 1 报出该错误（FR-003），门禁侧 MUST 以非零退出阻断并点名文件、行号与越界取值。本条与「owner/引擎不可用」的降级路径（FR-009）是两件事：前者是作者输入错误，后者是外部机制缺席。该阻断与本线类别无关——类别无法判定，不存在「按哪一类继续」这第三种选择；且它只可能出现在显式写了越界值的线上，因此不构成执行类回归。
- **FR-006**: 类别 MUST 在任何阶段作出第一次门禁判定之前可读，**包括 requirements 自身**；在 requirements 阶段写入或修改该行后，下游阶段 MUST 读到新值。读取时点 MUST 是阶段入口，即早于该阶段第一件依赖类别的动作（产物生成或门禁判定，取先发生者）；requirements 阶段的读取 MUST 发生在类别行写入之后、`validate-requirements.py` 之前。类别在 requirements 阶段门禁通过后发生变更的，MUST 记为 re-baseline 事件（写入阶段记录）并按新类别重跑 requirements 门禁集；MUST NOT 静默翻转。
- **FR-007**: 声明单位 MUST 是**特性线**（一条 spec 目录）；同一 Feature 的多个切片各自声明、允许不同类别，注册表 MUST NOT 把它们汇总为一个取值；并发场景下类别 MUST 按线解析，MUST NOT 用进程级、环境级或会话级全局值让一条线的类别泄漏给另一条线。

#### B. 阶段命令按类切换算子（US2）

- **FR-008**: `templates/commands/` 下的 `requirements`、`clarify`、`plan`、`tasks`、`checklist`、`analyze`、`implement` 七个模板 MUST 在其阶段门禁判定之前读取一次类别（时点按 FR-006），并按 `shared/workflow/expression-gates.md` § 阶段算子表执行本阶段的算子行；接线面 MUST 是这七个——`clarify` 在内，因为门禁 owner 的阶段算子表为它登记了两行算子（`G-clarify-clarity` / `G-clarify-reader`），排除它会让该阶段成为唯一无类感知的阶段。同一次阶段运行 MUST 只读取一次，结果复用于本阶段全部算子调用；命令与其委托技能在同一产物变更上重叠时 MUST 复用调用方结果，技能 MUST NOT 再读一次；跨阶段 MUST NOT 缓存（requirements 写入或改判后，下游 MUST 读到新值）；跨线 MUST NOT 复用。模板 MUST NOT 内嵌类别取值、判据句、六面表或算子表副本，只可出现读取调用与 owner 指针。
- **FR-009**: 类别读取失败 MUST 打印 `owner-unavailable` 并保持既有 `execution` 门禁集不变；MUST NOT 中断流程、MUST NOT 静默切换门禁集、MUST NOT 把降级结果读作通过。本路径 MUST 只覆盖三类输入：owner 不可解析、引擎缺席或不可执行、键或输入非法（解析退出码 2）；三者打同一标签、同一行为。MUST NOT 把「已声明但取值越界」（FR-005）并入本路径——把作者输入错误降级成默认类，正是本条与 FR-005 要分开的那件事。
- **FR-010**: 表达类特性线上，本阶段登记的 blocking 算子 MUST 真正阻断——任一面为 `not-evaluated` 时该阶段门禁判未通过；表达类 MUST NOT 继承代码型算子（测试执行、覆盖率、编译），但当该线同时产出代码或站点时，这些产物对应的代码型算子 MUST 按产物补回（按产物、不按类别）。
- **FR-011**: 执行类特性线的可观察行为 MUST 不变：同一输入上 MUST 零新增阻断检查、零新增必填章节，门禁判定集合与基线提交 `c1cd4600` 逐项相同；新增的类别读取对执行类 MUST 非阻断——引擎缺席时执行类阶段照常完成，不新增失败。
- **FR-012**: 切换 MUST 只由类别驱动：模板与技能 MUST NOT 内嵌按特性号、路径、关键词或文件类型的「允许列表」来判定是否走文档门禁；判定面 MUST 是「两条仅类别不同的夹具线跑同一模板，输出差异完全由声明解释」，且模板全文 grep 不出现任何特性号或路径白名单。

#### C. 文档结构与逻辑的硬约束（US3）

- **FR-013**: 表达类特性线的 plan MUST 产出 [[STR-002]] 章节，且 MUST 含四项：① **章节树**（每节：名称、目的＝读者读完要做的决定、父节、边界＝本节不覆盖什么）；② **基准读者与阅读场景**两行，读者定义 MUST 沿用 `shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议，MUST NOT 新建第二套定义；③ **证据清单**（每条拟写入文档的事实性断言 → 证据等级、as-of、source 三件套）；④ **事实 owner 清单**（每条事实 → 唯一 owner 路径与章节锚）。四项 MUST 各落一个固定子节，子节标题逐字取 [[STR-003]]（章节树）/ [[STR-004]]（基准读者）/ [[STR-005]]（证据清单）/ [[STR-006]]（事实 owner 清单）；子节标题缺任一即判违规。每个子节的表头列语义固定——章节树 4 列（节名 / 父节 / 目的 / 边界，`父节` 取顶层标记 `—` 或本表另一行的节名）、证据清单 4 列（断言 / 证据等级 / as-of / source）、事实 owner 清单 3 列（事实 / owner 路径 / 章节锚）；列名由检查器以常量声明（code-first owner），解析 MUST 按列名，MUST NOT 猜列位——与逐流程台账同一纪律，测试 MUST 从该常量读取列名，MUST NOT 手抄。校验器 MUST 是既有 `scripts/python/doc-consistency-check.py` 的新增动作 `--action structure`；本特性 MUST NOT 新增第七个门禁面（该检查器 `--faces` 仍为四面，六面 owner 不变），理由是该检查器已持有读者标记、证据三件套与副本下限三项语法，另置检查器会造出第二套同义解析。四项的校验 MUST 是可重跑的：同一份 plan 上重跑同一命令 MUST 得同一违规集。
- **FR-014**: 章节树（[[STR-003]] 子节）MUST 是实现阶段的唯一结构来源：计划中的每一节 MUST 出现在落文中，落文出现的计划外顶层章节 MUST 判为结构违规；两向判定 MUST 只读章节标题与计划表即可完成，MUST NOT 依赖通读正文或人工印象。判定 MUST 只产出两个具名码：落文缺失计划中的节 → `chapter-missing`；落文出现计划外顶层章节（其父节为顶层标记）→ `chapter-unexpected`；MUST NOT 引入第三个阻断码，非顶层的计划外章节不因本条转红。章节树自身的语法违规 MUST 由 FR-013 的同一动作报出，MUST NOT 另判一处：父节指向不存在的节 → `parent-unknown`，节名重复 → `chapter-duplicate`，目的为空 → `chapter-purpose-missing`，边界为空 → `chapter-boundary-missing`。
- **FR-015**: 证据清单 MUST 覆盖 implement 写入的每条事实性断言：清单外的断言 MUST 判违规；清单条目的等级、as-of、source MUST 成组出现，缺任一 MUST 判违规（语法与判定归 `shared/workflow/expression-gates.md` § 证据分级与 as-of，本文件不复述）。语法 MUST 复用 [[STR-005]] 的四列与既有证据码（`grade-invalid` / `as-of-malformed` / `source-missing` / `grade-asof-unpaired`），MUST NOT 另造同义码；落文中带证据标记、却在清单里找不到对应行的断言 MUST 判 `evidence-unlisted`。
- **FR-016**: 事实 owner 清单（[[STR-006]] 子节）MUST 让每条事实恰有一个 owner；同一事实出现两个 owner、或文档正文把同一事实重复手写 MUST 判违规，修复方向 MUST 是改为指向唯一 owner，MUST NOT 靠对齐措辞。判定 MUST 用三个具名码：同一事实两行 owner → `owner-duplicate`；owner 路径在仓库内不存在 → `owner-path-missing`；章节锚为空 → `owner-anchor-missing`。正文重复手写 MUST 沿用既有 `duplicate` 面的机械下限（归一化后全等且长度 ≥ 24 字符，或相似度 ≥ 0.90 且长度 ≥ 40 字符），MUST NOT 自建第二套阈值，也 MUST NOT 把该下限读作判据放宽（下限之下仍由评审面判定）。
- **FR-017**: 表达类特性线的 implement MUST 按章节树落文，并 MUST 通过四面 blocking 门禁：读者声明（落文前 40 个非空行内的读者与阅读场景）、证据三件套、事实唯一性、结构/链接/构建零新增违规；任一面为 `not-evaluated` MUST NOT 计为通过。章节两向比对（FR-014）属结构面内的第二个算子，MUST NOT 被登记为第五面。结构面通过 MUST NOT 被援引为内容正确性的证据——它只是必要条件，判据归 `shared/workflow/expression-gates.md` § 结构/链接/构建只是必要条件；`## Document Structure` 内 [[STR-004]] 的两行不套用「前 40 个非空行」窗口，该窗口适用于落文文档。四面结果 MUST 落在同一份门禁输出文件，作为本阶段 SC 证据的唯一来源（形态见 FR-020 的槽位与 verification 记录）。

#### D. 驱动接入（US4）

- **FR-018**: `skills/external/sdd-loop-driver/` 的阶段派发载荷 MUST 携带已解析的类别（取值 + `source` + 标注），本地原生子代理与远端 CLI 两种拓扑同规；子代理 MUST NOT 自行推断、补默认或按介质猜测类别；载荷缺该字段 MUST 判为派发构造缺陷，U4 不放行。载荷 MUST 写成 key=value 三元组（`flow_class=<值>`、`source=<declaration|default>`、`marker=<默认标记或空>`）。取值的唯一来源 MUST 是该线 `requirements.md` 的声明行，经同一解析入口取得；类别 MUST 在**每次阶段派发前**解析一次，MUST NOT 从状态脊、环境变量或上一阶段缓存取值。状态脊中的类别行只是带日期的观测记录，MUST NOT 充当取值来源；重入时 MUST 重新解析并与观测比对，不一致即记 re-baseline 事件并更新观测。
- **FR-019**: 表达类特性线的 U4 MUST 在该阶段既有四条件（哨兵、产物、纪律、记账）之外，校验该阶段的表达式门禁证据（算子入口、退出码或摘要）；哨兵与产物具备但门禁证据缺失 MUST 判未完成，MUST NOT 以「产物看起来对」放行。增补项 MUST 是以下四条且全部 blocking：(a) 本阶段登记的 blocking 算子各有一条结果记录，且无 `not-evaluated`；(b) 该记录指向的证据文件存在、非空，且其 SHA-256 与记账值一致（复用既有 `gate-implement-evidence-binding` 口径）；(c) 派发载荷的类别与 U4 当场解析值一致，不一致判派发构造缺陷；(d) 本阶段的 `stage-status` 行在场（定向集义务不因类别免除）。
- **FR-020**: 表达类特性线的两槽位测试预算 MUST 替换为两个**文档门禁槽位**，时点不变（implement 起点 baseline、review 通过后 closure），槽位记录 MUST 落在既有状态脊围栏内并沿用既有行字段；变化只在内容——`selection_basis` 取新值 `docs-gate-full`（与 `full-suite` 同位，只在表达类线出现），`command` 记该次文档门禁命令串（读者 / 证据 / 副本 / 计数四面 + 结构两向比对，站点层存在时加构建算子），`passed` 记 verdict ∈ {pass, not-applicable} 的 blocking 算子数，`failed` 记 verdict ∈ {fail, not-evaluated} 的算子数，closure 的 `baseline_compare` MUST 是算子 id 集合的名称级差集（与 `full-suite` 的失败名单差集同形态）。逐面的 `not-evaluated` 原因 MUST 写在 `evidence_ptr` 指向的门禁输出里，MUST NOT 并入 `passed`、MUST NOT 以 0 表示未运行。槽位 MUST NOT 静默跳过、MUST NOT 在未运行时写槽位行；槽位数、时点、槽位顺序、closure 名称级差集与 `audit-test-budget.py` 的判定 MUST NOT 改变；非槽位阶段的定向集记录义务不因类别免除——仅文档改动亦 MUST 留 `stage-status` 行。
- **FR-021**: 驱动 MUST NOT 因类别改变阶段序列、哨兵字面量、watcher 判定与退出码、卡死处置、快车道判据或 analyze/review 调用率；类别只改变两件事：用哪套算子证明同一不变量、预算槽位里装什么。槽位内容的替换 MUST NOT 构成审计口径变更——两槽位计数、槽位顺序、closure 名称级差集与 `stage-check` 语义逐字不变。

#### E. 不变量、边界与分发

- **FR-022**: 本特性 MUST NOT 新增 `/speckit.*` 命令，MUST NOT 引入运行时调度器、评分器或常驻服务，MUST NOT 新增第三方依赖；新增的确定性检查 MUST 只用标准库并落在既有 `scripts/python/` 下。
- **FR-023**: 接线面 MUST 是封闭集：七个命令模板 + `skills/external/sdd-loop-driver/` 及其 `references/` + 两份 owner 文档（`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`）+ `scripts/python/flow-class-check.py` + `scripts/python/doc-consistency-check.py`（仅新增 `--action structure`，四面与 `--faces` 取值集不变）；扩面 MUST 走契约修订，MUST NOT 由某个模板或技能就地扩面。
- **FR-024**: 改动的唯一编辑面 MUST 是框架源（`templates/`、`shared/`、`skills/`、`scripts/`）；`.specify/` 运行时副本与各工具命令副本 MUST 由既有同步/再生成机制产出，MUST NOT 手改；未刷新的项目 MUST 保持改动前行为（旧副本不含类别读取）。
- **FR-025**: 本特性 MUST NOT 削弱 069 已建立的不变量（八阶段集合不变、门禁数量不降、P0/P1 定义不动、analyze 与 review 调用率 100%），MUST NOT 回退 069 的 `Implemented` 状态、MUST NOT 改写其正文或其切片规格；一条 spec 目录 MUST 只绑一个 Feature，Feature 可拥有多条线（069 拥有 `069-` / `069a-` / `069b-` 三条），因此 077 是**新建 Feature 的承接边**而非 069 的新切片：承接关系记录在新 Feature 侧（`features/077.md` 与本文件 § Related Feature），MUST NOT 反向写入 069 的详情文件。判据 owner 为 069 与 `shared/workflow/expression-gates.md` § 阶段不变量，本文件只引用、不复述。

### 显式排除项（Out of Scope）

- **办公文档**（docx / pptx / xlsx 的内容生产）不在本特性范围；本特性只处理以文档树为载体的项目文档。
- **站点构建与发布**不改判：`skill:create-pages` 仍属 `execution`，其门禁不动；站点构建通过也 MUST NOT 被援引为文档内容正确。
- **不重写 069 的契约**：判据、两取值、`basis`、分类台账、类中立清单、同构映射与不可同构边界一律只引用。
- **不做类别自动推断模型**：不从路径、文件名、扩展名、内容或提交信息猜测类别。
- **不新建命令集、不新建「文档专用阶段」**：阶段集合固定为既有八阶段。
- **不引入运行时调度器、评分系统、报表引擎或常驻服务**（宪法 IX：框架而非运行时）。
- **不重写 058 / 067 的既有规则**：阶段序列、槽位时点、审计口径在 `execution` 分支上逐字不变；本特性只在这些 owner 文件中增加**类别分支**。
- **不规定实现形式**：命令与脚本的内部形制、字段子结构、错误文本、测试与模板文本属 plan；本文件只钉可判定验收面所需的那几项（Shared Strings 表、特性线键形态与三段退出码、四个子节标题与列语义、槽位字段取值语义）。
- **不把客户项目的具体文档当规范对象**：仓库外样本只作动机证据，引用时须带 as-of。

### Key Entities *(include if requirement involves data)*

- **Feature Line（特性线）**：一条 spec 目录；类别的声明单位与解析作用域。
- **Flow Class Declaration（类别声明）**：`requirements.md` 头部的一行字段；取值来自封闭集，携带「已声明 / 未声明」来源语义。
- **Class Resolution Record（类别解析记录）**：解析引擎返回的同形记录——类别、来源、默认标记、判定依据。
- **Document Structure Plan（文档结构产物）**：plan 的四项结构内容（章节树 / 基准读者与阅读场景 / 证据清单 / 事实 owner 清单）。
- **Gate Evidence Record（门禁证据记录）**：某阶段某个 blocking 算子的执行证据（入口、退出码或摘要），是 U4 放行的新前置。
- **Docs Gate Slot（文档门禁槽位）**：表达类线上替代两槽位测试预算的两次门禁运行记录；时点与既有槽位一致，内容换成文档门禁集。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 声明解析三例各跑一次即可判定——声明 `expression` 的特性线解析为 `expression` 且 `source` 标明「已声明」、退出码 0；无该字段的特性线解析为 `execution`、`source` 标明「未声明」并带默认标记；取值非法的一例在 requirements 门禁处阻断（非零退出）且**不**解析为 `execution`。判定只读退出码与记录字段。
- **SC-002**: 执行类零回归——以基线提交 `c1cd4600` 的命令模板为参照，同一执行类夹具上七个阶段的门禁判定集合逐项相同（新增阻断项 0、新增必填章节 0）；把类别引擎移走后重跑，执行类阶段仍完成（打印 `owner-unavailable`，新增失败 0）。
- **SC-003**: 表达类算子覆盖——一条表达类夹具线上，七个阶段各至少产生一条 blocking 算子结果，且该阶段在算子表中登记的面无一遗漏（覆盖率 100%）；删掉 implement 文档的读者声明后该阶段门禁转红（1/1）；站点层不存在的环境里构建算子记 `not-applicable` 而非通过（1/1）。
- **SC-004**: 结构门禁——含四项的 plan 夹具通过；四个负向夹具（缺章节树 / 缺基准读者行 / 证据条目缺 source / 同一事实两个 owner）各转红（4/4）；implement 夹具出现一个计划外顶层章节时转红（1/1）。
- **SC-005**: 驱动门禁——表达类线上「哨兵在 + 产物在 + 门禁证据缺失」的 implement 记录被 U4 判未完成（1/1）；两个文档门禁槽位在状态脊围栏中各出现恰好一次且时点正确，缺槽位时既有审计报违规而非静默通过（1/1）。
- **SC-006**: 零新增机制——`/speckit.*` 命令清单与基线提交 `c1cd4600` 逐字相同（差异集为空）；新增常驻进程/服务/调度器 0；新增第三方依赖 0。
- **SC-007**: 分发等价——重新生成后镜像对零漂移；未刷新副本上渲染出的七个模板不含类别读取（1/1），刷新后含（1/1）；两态各测一次，差异只出现在「是否含类别读取」这一点上。
- **SC-008**: 阶段完整性——一条表达类试点线跑完八阶段，analyze 与 review 各执行一次（2/2，按阶段记录判定），被跳过或缩短的阶段数为 0；判定 MUST NOT 读取类别。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 三个夹具 spec 的 `requirements.md` 与 `flow-class-check.py --action lookup` 的退出码及记录字段；三份输出按「执行时全量捕获」归档到 `test-evidence/`。
- **SC-002 Source**: 基线提交 `c1cd4600` 与实现后的两次阶段运行报告（同一执行类夹具）；门禁判定集合按阶段逐项 diff；引擎移除用例以「把引擎路径指向不存在的位置」构造，留退出码与 stderr。
- **SC-003 Source**: 表达类夹具七阶段的运行记录（算子入口与退出码/摘要）、负向夹具（删读者声明）一次运行、无站点层环境的一次构建算子结果。
- **SC-004 Source**: 五个夹具（1 合规 + 4 负向）与一个 implement 结构夹具的检查器退出码与报告条目；判定只读退出码与条目定位。
- **SC-005 Source**: 状态脊 `<!-- test-budget:begin -->…<!-- test-budget:end -->` 围栏与 `audit-test-budget.py` 的摘要行（`slots=baseline:N closure:N …`）；U4 判定记录与门禁证据缺失用例的校验输出。
- **SC-006 Source**: `/speckit.*` 命令模板清单（`templates/commands/*.md` 与各工具副本目录的并集）、依赖清单与进程清单在基线与实现后的两次采集差异。
- **SC-007 Source**: `sync-mirrors.py`/`regen-command-copies.py` 的漂移检查输出，以及未刷新副本与刷新副本两次渲染结果中「类别读取」行的存在性计数。
- **SC-008 Source**: 试点线的阶段记录（八个阶段各自的哨兵与 U4 记录）与 analyze/review 的运行判定记录；只读记录，不读正文。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "**Flow Class**" | FR-001 |
| `STR-002` | "## Document Structure" | FR-013 |
| `STR-003` | "### Chapter Tree" | FR-013, FR-014 |
| `STR-004` | "### Reader Baseline" | FR-013, FR-017 |
| `STR-005` | "### Evidence List" | FR-013, FR-015 |
| `STR-006` | "### Fact Owners" | FR-013, FR-016 |

**Citation convention**: 下游制品（FR 行、模板、契约、任务、测试）引用本表字面量时 MUST 写 `[[STR-NNN]]`，MUST NOT 重抄字面量；本表是它们的唯一登记处。

**编号范围说明**：本表编号**只在本规格内解析**，新登记的四行接续编为 `STR-003`…`STR-006`。069 已在其 § Shared Strings 占用 `STR-003`（`flow_class`）与 `STR-004`（默认标记字面量），那是 069 的命名空间：本文件正文引用 069 的字面量时只写 owner 路径，不写它的方括号 id，因此本规格的 `[[STR-004]]` 只指「基准读者」子节标题。`STR-001` / `STR-002` 是 requirements 阶段登记的既有行，按 append-only 保留原号不动。

## Clarifications

<!-- Populated by /speckit.clarify: - Q: <question> → A: <answer> -->

### Session 2026-10-30

- Q: 类别声明落在 requirements 头部、Feature 详情，还是两处？行形态如何、非法值怎么处置？ → A: 只落 `requirements.md` 头部区、`## Related Feature` 之前，恰一行 `**Flow Class**: <value>`（半角冒号 + 一个空格 + 取值，行尾无尾随空白，字段名与取值大小写敏感）；索引与详情不存取值。第二次出现判 `declaration-duplicate`，位于 `## Related Feature` 之后判 `declaration-misplaced`。取值越界按阻断处理（解析退出码 1，声明阶段门禁非零退出并点名行号与取值），不回落默认类；无该行 → `execution` + 未声明来源 + 069 登记的默认标记。落 FR-001 / FR-004 / FR-005。
- Q: 接线面是六个还是七个阶段命令？各阶段在什么时点读一次类别、如何避免重复读？ → A: **七个**——`requirements` / `clarify` / `plan` / `tasks` / `checklist` / `analyze` / `implement`；派发文本「六个」与同句枚举七个不一致，以枚举为准。`clarify` 必须在内：门禁 owner 的阶段算子表为它登记了两行算子（`G-clarify-clarity` / `G-clarify-reader`），排除它会让该阶段成为唯一无类感知的阶段。读取时点是阶段入口（早于该阶段第一件依赖类别的动作），同一次阶段运行只读一次并复用于本阶段全部算子；命令与其委托技能在同一次产物变更上重叠时复用调用方结果；跨阶段不缓存，跨线不复用。落 FR-006 / FR-008。
- Q: 特性级类别用扩展既有引擎的第三个键族，还是新建解析函数？键形态、记录形状与退出码如何？ → A: 扩 `flow-class-check.py --action lookup` 的**键族**，不新建解析函数、不新增第二份分类数据。键取 `spec:<spec 目录名>`（如 `spec:077-doc-sdd-integration`），不接受裸目录名，也不接受 `feature:<ID>`——`069` / `069a` / `069b` 三条线同属一个 Feature，按 Feature 键必然指错线。记录沿用同一字段集（`unit_id` 为键原文、`source` 取 `declaration` 或 `default`、`basis` 为 `null`、`neutral` 为 `false`）。退出码分三段：0 = 已解析（含未声明按默认）；**1 = 已声明但取值越界**（阻断）；2 = 键或输入非法、spec 目录不存在、owner 不可解析（`owner-unavailable`）。1 与 2 必须分开，否则「作者写错」会被当成「引擎缺席」静默降级为 `execution`。特性线声明 MUST NOT 写进逐流程台账（台账行集等于框架单元清单，多出行即 `unknown`）。落 FR-003。
- Q: `## Document Structure` 四项的精确语法是什么，由哪个确定性检查器验，零新增违规基线怎么取？ → A: 四项各落一个固定子节，子节标题逐字登记为本规格的四个新字面量（`[[STR-003]]`…`[[STR-006]]`，本规格内的编号，与 069 同号字面量互不相指，见 § Shared Strings 的编号范围说明）；表头列语义固定为——章节树 4 列（节名 / 父节 / 目的 / 边界，`父节` 取顶层标记 `—` 或本表另一行节名）、读者 2 行（沿用既有 `**Readers**:` / `**Reading scenario**:` 标记）、证据 4 列（断言 / 证据等级 / as-of / source）、owner 3 列（事实 / owner 路径 / 章节锚）；表头按列名解析、不猜列位。检查器 = 既有 `scripts/python/doc-consistency-check.py` 的新增动作 `--action structure`（不是第七个门禁面：该检查器 `--faces` 仍为四面，六面 owner 不变），理由是其三项语法（读者标记、证据三件套、副本下限）已在同一检查器内，换一个检查器会造出第二套同义解析。基线取法：主体集合 = 经类别解析为 `expression` 的特性线 spec 目录，首次声明那一次运行实测出的违规集即基线，此后判定「当前违规集 ⊆ 基线集」（按 文件 + 违规码 + 节名 三元组比对，差集为空），不是「总数不增」；新线首次声明时基线为空集，即判绝对。主体集合为空时输出 `not-applicable`，MUST NOT 记 0 违规通过。全仓 `structure-links-build` 面的既有 3 条违规基线归 `docs-utils.py`，本检查不读也不改。落 FR-013 / FR-014 / FR-015 / FR-016 / FR-023。
- Q: 表达类的 implement 证据面如何落——Test-First 怎么判、`verification.md` 写什么、「结构通过只是必要条件」写在哪？ → A: Test-First 按宪法 VII 的 template-only 条款判 `Partial (justified)`，justification 写在 `tasks.md` 的判定行与 `verification.md` 的 `notes=`：该线无运行时代码，替代验证是四项文档门禁输出；`Partial (justified)` 是合法状态，既不记 `pass` 也不记 `fail`。`verification.md` 的 SC 证据改用门禁输出：`SC-NNN_value=` 记门禁摘要（逐面 `面=verdict`），证据记录沿用既有四键（`sample_id` / `evidence_path` / `evidence_sha256` / `verdict`），`evidence_path` 指向 `test-evidence/` 下的该次门禁输出文件；`verdict` 仍取模板既有的五值词表，门禁某面 `not-evaluated` → 该 SC 记 `unknown` 并点名面与原因，MUST NOT 记 `pass`。「结构通过只是必要条件」写进 FR-017 的验收句：结构面绿不得被援引为内容正确性证据；SC-004 的第四个负向夹具（同一事实两个 owner）本身就是「结构绿而内容红」的验收实例，不新增 SC。落 FR-017。
- Q: 驱动侧从哪里取类别、U4 对表达类新增哪些校验、两槽位预算装什么？ → A: 取值的唯一来源是该线 `requirements.md` 的声明行，经同一解析入口在**每次阶段派发前**解析一次；状态脊中的类别行只是带日期的观测，不当取值来源，重入时重新解析并与观测比对，不一致记 re-baseline。派发载荷为 key=value 三元组（取值 + 来源 + 默认标记）。U4 在既有四条件之外增补四项 blocking 校验：算子结果齐备且无 `not-evaluated`、证据文件的 SHA-256 与记账一致（复用既有绑定门）、载荷类别与当场解析值一致、`stage-status` 行在场。两槽位：`slot`、时点、槽位顺序、closure 名称级差集与审计脚本判定全不变，只换内容——`selection_basis=docs-gate-full`、`command` 记文档门禁命令串、`passed` 记 `pass` 与 `not-applicable`、`failed` 记 `fail` 与 `not-evaluated`（逐面原因写进 `evidence_ptr` 指向的输出）、closure 的 `baseline_compare` 为算子 id 集合的名称级差集；未运行不得写槽位行、不得记 0。不改阶段序列与 analyze/review 100%。落 FR-018 / FR-019 / FR-020 / FR-021。
- Q: 077 与 069 是什么关系，一条 spec 到底绑几个 Feature？ → A: 一条 spec 目录绑一个 Feature，Feature 可拥有多个 spec（069 拥有 `069-` / `069a-` / `069b-` 三条线）。077 是新建 Feature，与 069 是一条「承接」边而非归属：069 保持 `Implemented`，其正文与状态 MUST NOT 回退或改写，本特性只在 069 的两个 owner 文件（`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`）做类条件追加；承接关系记录在新 Feature 侧（`features/077.md` 与本节），不在 069 的详情文件里补写。落 § Related Feature 与 FR-025。
- Q: execution 特性如何保证逐字不变，接线失败时回退到哪？ → A: execution 线上新增的只有一次类别读取，判定集合、必填章节、阻断项与基线提交 `c1cd4600` 逐项相同；模板 diff 限于读取调用与 owner 指针。回退路径封闭为四条且都不改判定结果：owner 不可解析 → `owner-unavailable` + 保持既有 `execution` 门禁集；引擎缺席或不可执行 → 同一标签、同一行为；键或输入非法（退出码 2）→ 同一行为；未刷新的旧副本 → 无类别读取，行为与改动前一致。已声明但取值越界不在此列（FR-005 阻断）。任何一条 MUST NOT 静默切换门禁集、MUST NOT 把降级读作通过。落 FR-009 / FR-011 / FR-024。
