# Requirements Specification: General Best Practices — 通用最佳实践模块（四分类封闭集 + 渐进积累）

**Requirement Branch**: `111-general-best-practices`
**Created**: 2026-11-27
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（新增/晋升条目、维护四分类封闭集与守卫、判断「一条经验属于哪个分类、何时可以晋升」的人）与下游项目维护者（`specify init` 后在 `.specify/shared/best-practices/` 消费内容、或在本地按积累机制沉淀经验的人）——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 当需要判定「模块由哪些文档构成、四分类封闭集如何变更」「一条最佳实践必须长什么样」「一条开发观察如何经既有 feedback + memory 引擎晋升为条目、如何可回溯」「模块如何随 `shared/` 分发并在框架地图登记」「本特性的改动边界是什么」时打开本规格，据 FR-001…FR-009 与 SC-001…SC-007 放行 `/speckit.clarify` 与后续规划
**Input**: User description: "Port the closed ai-harness 087 general best-practices capability into spec-kit as new spec 111-general-best-practices: `shared/best-practices/` with the five documents (manifest + four category owner files), distribution through the existing `shared/` shipping/init flow, and any framework-map/instructions wiring the source design requires; additive documentation surfaces only — no engine/runtime change, no store layout, no decision-governance alignment. Bind Feature 111."

**输入校正**：①「五文档」按源交付面读作**清单 README + 四个分类 owner 文件**（共五个文件），不是五个分类；②「closed ai-harness 087 capability」读作源规格 `087-general-best-practices` 的已定稿交付面（`requirements.md` / `plan.md` / `tasks.md` / `contracts/best-practices.contract.md` / `verification.md` 五处所描述的：清单 + 四个分类文件 + 首条 + 积累机制 + 守卫 + 镜像），不是照搬源仓的构建流程；③源规格的 Feature 绑定（ai-harness Feature 040 Knowledge & Session Utilities）**不复用**——spec-kit 注册表没有同名 Feature，本特性按简报绑定为一个新的独立 Feature 111（A-3）；④"verify what the source actually shipped before adding" 是**实测义务**：源仓实测未新增框架地图行、也未新增 instructions 指针（A-6），本特性据目标仓治理判定只补框架地图行。

## Related Feature *(mandatory)*

**Feature ID**: 111
**Feature Name**: General Best Practices（通用最佳实践）

**Binding basis**: 简报固定绑定 Feature 111；本特性是**新的独立 Feature**（无父切片）：它交付随框架分发的**内容模块**，积累机制只按指针复用既有 feedback（Feature 028 Feedback Mechanism）与 memory / knowledge-promotion 引擎，不扩展其行为。源规格绑定的 ai-harness Feature 040 在 spec-kit 注册表中无对应条目，按"源 registry ID 不复用"的简报约束不迁移该绑定。索引行与详情文件的登记属后续澄清/特性阶段动作，本规格不代行（A-3、A-10）。

## Overview

**问题**：spec-kit 已经拥有机制类文档层——`shared/guidelines/`（纪律）、`shared/definitions/`（概念所有者）、`shared/workflow/`（流程约定）——但没有一个沉淀**日常开发经典最佳实践**的内容层：反复出现的通用工程经验（例如 git clone 的协议口径）没有唯一沉淀点，每次都靠会话记忆或临时口口相传重新发现；即使被记录，也没有"观察 → 复核 → 晋升"的可回溯积累路径。

**源事实（ai-harness 087，2026-11-25 定稿，已实测）**：源仓在 `shared/best-practices/` 建立了**四分类封闭集**模块——清单 `README.md`（声明分类集合、条目形态与积累机制）+ 四个 owner 文件 `programming-languages.md` / `system-interfaces.md` / `programming-frameworks.md` / `programming-tools.md`（其中前三者以"尚无条目"占位）+ 首条种子（`programming-tools.md` § Git clone 的默认协议）+ 契约 `C-001…C-005` + 守卫 `tests/contract/test_general_best_practices.py` + `.ah/shared/best-practices/` 镜像；verification 记录三条 SC 全部 pass。源仓**未**新增框架地图行、**未**新增 instructions 指针（全仓检索 `best-practices` 在模块与规格之外零命中）；accumulation 复用既有 feedback + memory 引擎，不新建机制。

**目标基线实测（2026-11-27，base `0419adae5`）**：

1. `shared/` 现有 `constants/` / `declarations/` / `definitions/` / `guidelines/` / `patterns/` / `workflow/`，**没有** `best-practices/`；`.specify/shared/` 无同名目录。
2. `specify init` 已把 `shared/` 整目录拷贝到目标项目 `.specify/shared/`（`src/specify_cli/__init__.py` 的 shared 拷贝步骤），新增子目录随既有流程自动分发，无需改代码。
3. `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS` 含 `("shared", ".specify/shared")`，镜像按目录整树比较/写入；`tests/contract/test_mirror_parity_suite.py` 从该引擎派生参数表，新文件自动纳入字节一致检查。
4. `.specify/instructions.md`、`.specify/glossary.md`、`shared/definitions/framework-map.md` 对 `best-practices` 零命中；`shared/definitions/framework-map.md` 是 `.specify/` 布局的单一所有者，`.specify/instructions.md` 的 Framework Map 段只是指向它的指针。
5. `shared/guidelines/directory-governance.md` § 3 规定「新顶层目录或既有树下**首个新种类目录** MUST 在同一变更内登记到其区域地图」；框架布局的区域地图即 `shared/definitions/framework-map.md`。
6. 编号空间：仓内 spec 目录最大为 108，本地分支 `109-prompt-adherence` / `110-context-management` / `111-general-best-practices` 已占用；本线固定编号 111（脚手架脚本会派生 112，见 A-9）。

**本特性交付**：`shared/best-practices/` 模块（清单 + 四个分类 owner 文件 + 首条种子 + 积累机制指针）；`shared/definitions/framework-map.md` 的登记行（同变更落地，镜像再生成）；守卫 `tests/contract/test_general_best_practices.py`；`.specify/shared/best-practices/` 镜像。**全部为增量文档面**，分发复用既有 `shared/` 整目录拷贝与镜像机制。

**不做什么**：不新增引擎、运行时行为、CLI/init 代码、运行时存储或 `.gitignore` 规则；不新建第二积累机制（观察记录与晋升复用既有 feedback + memory / knowledge-promotion）；不改 `.specify/instructions.md` 与模板（Framework Map 段已是指针，One Source of Truth）；不改决策治理面（`shared/definitions/decision-definitions.md` 及其检查器零修改；本特性不产出决策项）；不改写任何 dated record；不在本阶段编辑特性注册表或词汇表（A-10）。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **类别判定 = `execution`**：验收 oracle 是机器执行的契约守卫（存在性、封闭集、指针解析、镜像一致、零残留），不是"人读懂内容"的表达类 oracle。 | 按验收 oracle 判定（`shared/definitions/flow-class-definitions.md`）；内容写作质量归评审，不改变类别。 |
| **A-2** | **范围 = 源交付的全部五个文件**：清单 + 四个分类 owner 文件整组移植，含三个"尚无条目"占位与一个首条种子。 | 四分类**封闭集**本身就是能力；只移一部分会破坏封闭集并让守卫失去意义。源设计未声明子集。 |
| **A-3** | **绑定新的独立 Feature 111**；不迁移源 Feature 040 绑定、不设父切片、不复用源 registry ID。特性索引行与详情文件由后续澄清/特性阶段登记，本阶段不编辑注册表。 | 简报明确"bind spec-kit Feature 111 (source registry ID not reused)"；目标注册表无 Knowledge & Session Utilities 同义条目，硬绑会误导所有权。 |
| **A-4** | **命名/路径适配**（逐项核实）：`ai-harness` → `Spec Kit`；`.ah/` → `.specify/`；`/ah.*` → `/speckit.*`（源五文档中实际无 `/ah.*` 引用）；归属声明 `Feature 040` → `Feature 111`；积累机制指针落到目标仓既有路径——`.specify/scripts/python/feedback-utils.py`（`record` 动作已存在）与 `.specify/shared/guidelines/knowledge-promotion.md`（存在）；镜像目标 `.specify/shared/best-practices/`。 | 源文按产品名与运行时路径书写；目标仓路径实测存在（见 Overview § 目标基线）。 |
| **A-5** | **分发 = 复用既有 `shared/` 通道**：`specify init` 的整目录拷贝 + `sync-mirrors.py` 的 `shared → .specify/shared` 镜像对；**零** CLI/打包/`.gitignore` 改动。 | Overview 实测第 2、3 条：两条通道已覆盖任意新增 `shared/` 子目录；新增改动即为过度工程（宪法 IX）。 |
| **A-6** | **框架地图行 = 目标仓治理要求，MUST 补；instructions 指针 = 不补**。源仓实测两者皆未做；但 `directory-governance.md` § 3 要求新种类目录同变更登记到区域地图（`shared/definitions/framework-map.md`）。`shared/` 是**已分发**目录（source 与 `.specify/shared/` 镜像三副本拓扑），其新子目录种类按框架布局行登记。`.specify/instructions.md` 的 Framework Map 段已是指向地图的指针，补第二段会复制事实（宪法 XIV）。 | 源设计的"未做"是源仓未受该治理约束的证据，不是目标仓可以遗漏登记的理由；登记行满足"文档化含义"义务且不新增第二真源。 |
| **A-7** | **测试 = 一个内容守卫 + 复用既有镜像参数化套件**，Tests Mode 记为 ON（源规格同为 ON）：`tests/contract/test_general_best_practices.py` 以 red-first 钉住 FR-007 的六组断言；镜像字节一致由 `tests/contract/test_mirror_parity_suite.py` 自动覆盖，本守卫不复制第二套比较逻辑。一次全量跑 `scripts/bash/run-tests.sh` 记录基线。 | 源规格 FR-005 的守卫先例；目标仓已有从 `sync-mirrors.py` 派生参数的镜像套件，重复实现违反 One Source of Truth 与测试执行效率纪律。 |
| **A-8** | **内容保真**：五个文档按实质逐字移植（中文正文、双语标题、条目形态 = 标题 + 实践 + 反例/证据），保留三个"尚无条目"占位与首条 `~/.git-credentials` 反例；仅按 A-4 适配产品名与路径。 | 移植的语义对象是源已定稿内容；改写会引入未受源 verification 覆盖的新文本。 |
| **A-9** | **脚手架偏差（披露）**：`create-new-requirements.sh` 从 spec 目录（最大 108）**加**本地分支名派生编号，`109/110/111` 三条并行线分支都在编号空间内，脚本会派生 **112** 并新建分支——与本线"固定编号 111、停留在 `111-general-best-practices` 分支"冲突。按 108 A-16 先例，本阶段从 `.specify/templates/requirements-template.md` **手工**脚手架到 `.specify/specs/111-general-best-practices/requirements.md`，等价复刻模板拷贝、仅跳过建分支步骤，并记录于 `test-evidence/requirements-stage-2026-11-27.md`。 | 工作树必须停留在本线分支；脚本把"本线分支"当成"已用编号"是编号派生的既有陷阱（create-requirements 技能 § 2 已记录同名陷阱）。 |
| **A-10** | **本阶段写面 = 仅本特性产物**：`.specify/specs/111-general-best-practices/**`（requirements、checklists、test-evidence）；不编辑状态脊、特性注册表、词汇表或任何镜像。词汇候选（"best practice / 最佳实践"、"progressive accumulation / 渐进积累"）不在本阶段入表，留待澄清阶段按词汇协议提议。 | 简报约束"Only this feature's artifacts; no push; no spine/registry edits"；词汇协议允许澄清阶段再提议，避免越界写项目锚点。 |
| **A-11** | **空分类是设计状态，不是缺陷**：`programming-languages.md` / `system-interfaces.md` / `programming-frameworks.md` 三个文件以"尚无条目"占位 + 分类范围说明交付；守卫 MUST NOT 要求非空条目，MUST NOT 允许编造条目充数。 | 源规格同形态；渐进积累的前提是"干净运行不追加空洞条目"（README 红线）。 |
| **A-12** | **containment 声明的基线与允许增量集由 FR-009 单一拥有**：基线 `0419adae5`；允许变更路径集、以及后续特性登记阶段对注册表的唯一例外都在该条定义；SC-006 只引用，不复述。 | 封闭声明须有基线 referent 与可推导允许增量（owner：`shared/guidelines/closed-set-claims.md`）；同一事实只留一个所有者。 |
| **A-13** | **与决策治理无关**：本特性不产出决策项、不改 `decision-definitions.md`、不触发 `validate-decisions.py` 的任何新规则；内容条目若与既有所有者规则冲突，所有者规则胜出，条目 MUST NOT 作为第二真源落地（Edge Cases）。 | 简报明确"no decision-governance alignment"；One Source of Truth 要求最佳实践不得覆盖机制所有者。 |
| **A-14** | **客户项目再初始化语义沿用现状**：模块随 `shared/` 整目录拷贝；对客户本地修改的保留/覆盖行为与其它 `shared/` 文档一致，本特性不新增保留保证，也不测试该既有语义。 | 不引入新契约；避免为既有分发行为另立承诺（宪法 IX）。 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 遇到开发摩擦时读到规范做法（Priority: P1）

一名维护者（人或 agent）在安装/构建/工具使用中撞上一次反复出现的摩擦——例如内网 git 仓库 clone 因「凭据记的是 HTTP、clone 用的是 HTTPS」而失败。他打开 `.specify/shared/best-practices/`，从清单看到四分类，进入"编程工具"，直接读到默认口径：clone URL 默认用 HTTPS；特殊仓库需要 HTTP 时必须显式提示协议与凭据要求；反例与延伸处置一并给出，而不是靠会话记忆重新推断。

**Why this priority**: 这是模块存在的理由——内容没有正确的默认口径与反例，后面的积累机制只是空转。首条种子就是用户点名的真实教训。

**Independent Test**: 检查 `shared/best-practices/` 五文档：清单声明封闭四分类并逐行链接 owner 文件；`programming-tools.md` 含首条（默认 HTTPS + 特殊仓库提示义务 + `~/.git-credentials` 反例）；三个空分类带"尚无条目"占位与范围说明；所有相对链接可解析。守卫对应断言转绿。

**Acceptance Scenarios**:

1. **Given** 模块已交付，**When** 维护者打开清单 `README.md`，**Then** 他 MUST 看到封闭四分类集合（编程语言 / 系统接口 / 编程框架 / 编程工具）与每类的 owner 文件链接，以及模块读者与范围声明。
2. **Given** 维护者在编程工具分类下查找 git clone 口径，**When** 打开 [[STR-005]]，**Then** [[STR-007]] 条目 MUST 给出默认 HTTPS 实践、特殊仓库 HTTP 的显式提示义务与 `~/.git-credentials` 协议错位反例三项。
3. **Given** 某个分类尚无条目，**When** 打开该 owner 文件，**Then** 它 MUST 呈现 [[STR-006]] 占位并说明该分类范围，MUST NOT 删除文件或以编造条目充数。

---

### User Story 2 - 经既有引擎渐进积累新条目（Priority: P1）

框架维护者在一次真实开发摩擦后，用既有 feedback 引擎记下一条带标记的观察；当同一摩擦再次出现或被一次明确的用户纠正证明为**通用**时，他按知识晋升纪律把它提升进匹配的分类 owner 文件，条目带有可回溯的来源（feedback 条目 ID / 提交号 / 会话原话）。全程没有新引擎、新存储或新渲染器。

**Why this priority**: 没有积累路径，模块会停在首条种子；而新建第二机制会与既有 feedback + memory 引擎形成双轨，破坏 One Source of Truth。

**Independent Test**: 从清单与 owner 文件核对积累机制声明：观察入口指向既有 feedback 引擎的动作面、晋升规则指向既有 knowledge-promotion 所有者、回溯要素在场；全模块检索无第二引擎/存储声明。守卫断言指针可解析且无第二机制。

**Acceptance Scenarios**:

1. **Given** 一次真实开发摩擦，**When** 维护者用 `.specify/scripts/python/feedback-utils.py --action record` 记录带 [[STR-001]] 标记与所属分类的观察，**Then** 该观察落在既有 feedback 存储，MUST NOT 直接写入模块条目区。
2. **Given** 一条观察被证明通用（反复出现或一次明确的用户纠正），**When** 按 `.specify/shared/guidelines/knowledge-promotion.md` 晋升，**Then** 条目 MUST 落在匹配的分类 owner 文件并遵守条目形态，且携带观察来源；MUST NOT 编造数值或证据。
3. **Given** 积累机制声明，**When** 维护者检索模块与守卫，**Then** MUST NOT 存在第二引擎、第二存储、第二渲染器或索引的声明；机制只以指针复用既有 feedback + memory 引擎。

---

### User Story 3 - 下游项目经 init 收到模块并可在框架地图找到（Priority: P2）

下游项目维护者执行 `specify init` 后，`.specify/shared/best-practices/` 随既有 `shared/` 整目录拷贝到位；他（或 agent）浏览框架地图时能在一行内知道这个目录是什么、谁是所有者。框架仓内的 `.specify/shared/best-practices/` 镜像与源目录字节一致，无需任何新命令。

**Why this priority**: 分发与可发现性决定模块是否能被真实使用；但它建立在 US1/US2 的内容与机制之上，价值次序在后。

**Independent Test**: 对既有 `shared/` 拷贝与镜像通道做只读验证——`sync-mirrors.py --check` 对本模块零漂移；框架地图行在源与镜像中都在场；并证明 init 既有拷贝步骤覆盖新目录（代码路径 + 测试）。不需要新增 CLI 代码。

**Acceptance Scenarios**:

1. **Given** 目标项目执行既有 `specify init`，**When** `shared/` 拷贝步骤完成，**Then** 目标 `.specify/shared/best-practices/` MUST 含五个文档，且无需新增任何 CLI/打包改动。
2. **Given** 框架仓中的源目录与镜像目录，**When** 执行 `python3 scripts/python/sync-mirrors.py --check`，**Then** 本模块的源/镜像差集 MUST 为空（字节一致；由既有参数化镜像套件另行钉住）。
3. **Given** 读者浏览 `shared/definitions/framework-map.md`，**When** 查找 shared 内容模块，**Then** MUST 存在一行登记 `.specify/shared/best-practices/` 的含义与所有者；`shared/definitions/framework-map.md` 的镜像 MUST 同步包含该行。

---

### Edge Cases

- **提议第五个分类**：不允许绕过封闭集——MUST 在同一变更内修订清单、建立对应 owner 文件并更新守卫；只新增文件不改清单、或只改清单不建文件，均使守卫转红。
- **观察未证明通用**：留在 feedback 存储，MUST NOT 晋升；"干净运行追加空洞条目"被清单红线明确禁止。
- **同一条经验横跨两个分类**：按**主要主体**选择单一 owner 落条目；其它分类 MUST NOT 复制正文，只允许指针引用（One Source of Truth）。
- **条目与既有所有者规则冲突**：机制所有者规则胜出；该条目 MUST NOT 作为第二真源落地，应按 feedback 通道上送所有者修订（A-13）。
- **空分类文件**：保留占位与范围说明；MUST NOT 移除文件、MUST NOT 编造条目（A-11）。
- **相对链接断裂**：清单 ↔ 四个 owner 文件的任一链接不可解析即使守卫转红。
- **产品名残留**：模块文本出现 `ai-harness` / `.ah/` / `/ah.` 即使守卫转红（FR-008）。
- **客户项目本地修改后再 init**：沿用既有 `shared/` 刷新语义，本特性不新增保留保证（A-14）。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 在 `shared/best-practices/` 创建模块清单 `README.md`，声明**封闭的四分类集**——编程语言 / 系统接口 / 编程框架 / 编程工具，每类恰一个 owner 文件：[[STR-002]]、[[STR-003]]、[[STR-004]]、[[STR-005]]——以及模块读者与范围（日常开发可复用的经典经验库，渐进积累而非一次性清单）和统一**条目形态**（标题 + 实践 + 反例/证据）。清单的分类表 MUST 逐行链接到四个 owner 文件。封闭集变更（新增/删除/改名分类）MUST 在同一变更内同时修订清单、建立或迁移对应 owner 文件并更新守卫（FR-007）；MUST NOT 只新增文件不改清单。
- **FR-002**: 创建四个分类 owner 文件：[[STR-002]]、[[STR-003]]、[[STR-004]]、[[STR-005]]。每个文件 MUST 声明其分类范围（scope）、指回清单的积累机制指针与统一条目形态；**尚无条目**的分类 MUST 保留显式的 [[STR-006]] 占位行并说明该分类范围，MUST NOT 删除该文件，MUST NOT 以编造条目充数（A-11）。
- **FR-003**: 在 [[STR-005]] 中种子首条 [[STR-007]]：git 这个编程工具的 clone 默认口径——**默认用 HTTPS 作 clone URL**；特殊仓库必须走 HTTP（或 SSH）时 MUST 显式提示该仓库的协议与凭据要求，以此达成统一；反例/证据 MUST 记录 `~/.git-credentials` 记录了 HTTP 认证信息而 install 流程用 HTTPS 发起 clone 导致失败的协议错位认知偏差；延伸口径（内网 git 服务在 HTTPS 需认证而 SSH 匿名/key 可用时，install 源 URL 优先给 SSH 或明确提示认证方式）MUST 保留。条目 MUST 遵守 FR-001 的条目形态。
- **FR-004**: 在清单中以**指针形态**声明渐进积累机制：开发观察经 `.specify/scripts/python/feedback-utils.py --action record` 落为带 [[STR-001]] 标记与所属分类的观察；当被证明**通用**（反复出现或一次明确的用户纠正）时，按 `.specify/shared/guidelines/knowledge-promotion.md` 晋升进匹配的分类 owner 文件，并记录观察来源（feedback 条目 ID / 提交号 / 会话原话）使条目可回溯。红线：干净运行 MUST NOT 追加空洞条目，MUST NOT 编造数值或证据。机制 MUST 复用既有 feedback + memory 引擎，MUST NOT 新建第二引擎、存储、渲染器或索引；机制规则按指针抵达所有者，清单不复述其取值。
- **FR-005**: 在 `shared/definitions/framework-map.md` 新增一行，登记 `.specify/shared/best-practices/` 为随框架分发的通用最佳实践内容模块，指向本模块清单与 Feature 111；该登记 MUST 与模块创建**同一变更**落地（`shared/guidelines/directory-governance.md` § 3）。镜像 `.specify/shared/definitions/framework-map.md` 由既有镜像机制再生成，MUST NOT 手改。`.specify/instructions.md` 与指令模板 MUST NOT 新增指针段（现有 Framework Map 段已是指向地图的指针，A-6）。
- **FR-006**: 分发 MUST 复用既有 `shared/` 通道，不新增打包或运行时面：(a) `specify init` 既有的 `shared/` 整目录拷贝使模块落到客户项目 `.specify/shared/best-practices/`；(b) `scripts/python/sync-mirrors.py` 的既有 `shared → .specify/shared` 镜像对 MUST 覆盖本模块并保持源/镜像字节一致。MUST NOT 新增运行时存储、`.gitignore` 规则、CLI 代码或打包清单改动。
- **FR-007**: 守卫 `tests/contract/test_general_best_practices.py` MUST 以 red-first 方式钉住：(a) 清单与四个 owner 文件存在，且清单声明的分类集合恰为四类（第五类出现即红）；(b) 每个 owner 文件携带积累机制指针与条目形态声明，空分类携带 [[STR-006]] 占位；(c) 首条 [[STR-007]] 的实践与反例在 [[STR-005]] 中在场；(d) 积累机制指针引用的 `feedback-utils.py` 动作面与 `knowledge-promotion.md` 路径可解析，且模块内不出现第二引擎/存储的声明；(e) 框架地图在源与镜像中都登记了 `.specify/shared/best-practices/`；(f) 清单 ↔ 四个 owner 文件的相对链接全部可解析。镜像字节一致性由既有 `tests/contract/test_mirror_parity_suite.py` 覆盖，本守卫 MUST NOT 复制第二套镜像比较逻辑。守卫 MUST 经唯一测试入口 `scripts/bash/run-tests.sh` 执行。
- **FR-008**: 适配与零残留：移植内容的产品名与路径 MUST 适配为 spec-kit 口径——`ai-harness` → `Spec Kit`，`.ah/` → `.specify/`，`/ah.*` → `/speckit.*`（源五文档实际无此类引用，出现时一并适配），归属 `Feature 040` → `Feature 111`。模块文本 MUST NOT 含 `ai-harness`、`.ah/`、`/ah.` 残留，MUST NOT 含指向源仓路径的引用；模块引用的每个仓内路径 MUST 在目标仓存在。
- **FR-009**: 边界封闭（可判定）：本特性相对基线 `0419adae5` 的**变更路径集**恰为——`.specify/specs/111-general-best-practices/**`（本规格全过程产物）、`shared/best-practices/**`（五个文档）、`.specify/shared/best-practices/**`（镜像再生成）、`shared/definitions/framework-map.md` 与 `.specify/shared/definitions/framework-map.md`（登记行及其镜像）、`tests/contract/test_general_best_practices.py`（守卫）、以及 **wrap-up 记账记录**——`.specify/session/`、`.specify/feedback/`、`.specify/exec-quant/` 中由本特性各阶段运行经既有三个记账引擎产生的 per-entry 文件（判定谓词：记录体内携带特性 key `111-general-best-practices` 或本线 run id `r20261127T071500Z-111a`）；后续特性登记阶段对 `.specify/features.md` 与 `.specify/features/111-*.md` 的登记行是唯一例外。集合之外的路径 MUST 保持零差异；MUST NOT 改动引擎、模板、技能、代理、命令、宪法/指令、运行时存储布局或决策治理面。

### Key Entities *(include if requirement involves data)*

- **Category（分类，封闭集）**: 编程语言 / 系统接口 / 编程框架 / 编程工具；每个分类恰有一个 owner 文件，集合变更须同变更修订清单、文件与守卫。
- **Entry（条目）**: 统一形态 = 标题 + 实践 + 反例/证据；每条可回溯到一次真实观察来源。
- **Manifest（清单）**: `README.md` 声明封闭集、条目形态、模块读者与范围、积累机制指针。
- **Observation（观察）**: 既有 feedback 存储中的一条记录，带 [[STR-001]] 标记与所属分类；"通用"证明前不进入模块。
- **Guard（守卫）**: `tests/contract/test_general_best_practices.py`，red-first 钉住模块形状、指针与零残留。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时依赖、不新增第三方包——它只新增 Markdown 内容、一行框架地图登记与一个 pytest 守卫，消费既有的 Python 解释器、pytest、唯一测试入口与既有镜像引擎。表中 `Premises` 引用的 `EP-NNN` 由 plan 阶段 `## Execution Premises` 定义（本阶段只保留引用）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | 内容模块（清单 + 四个 owner 文件 + 首条） | in-scope | 本特性：`shared/best-practices/` + 镜像 | 四分类封闭集；随 `shared/` 分发 | 本规格 FR-001…FR-003（plan 阶段契约细化） | FR-007 守卫的 (a)(b)(c)(f) 四条断言转绿 | FR-001, FR-002, FR-003 | EP-001 |
| RS-002 | 积累机制声明 + 内容守卫 | in-scope | 本特性：`README.md` + `tests/contract/test_general_best_practices.py` | feedback 观察 → 按 knowledge-promotion 晋升（指针）；red-first | 本规格 FR-004、FR-007 | 守卫的 (d) 段断言 + 指针解析；无第二机制声明 | FR-004, FR-007 | EP-002 |
| RS-003 | 分发登记与镜像（框架地图行 + `shared → .specify/shared` 镜像对） | in-scope | 既有：`shared/definitions/framework-map.md` + `scripts/python/sync-mirrors.py`（零修改消费） | 同变更登记；字节一致 | 本规格 FR-005、FR-006 | `sync-mirrors.py --check` 对本模块零漂移；守卫的 (e) 段断言 | FR-005, FR-006 | EP-003 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 模块形状成立：`shared/best-practices/` 含清单与四个 owner 文件（5/5）；清单声明的封闭集恰为四类（[[STR-002]] / [[STR-003]] / [[STR-004]] / [[STR-005]]）且每类链接到恰一个 owner 文件（4/4）；清单 ↔ owner 文件相对链接可解析率 = 100%；空分类占位 [[STR-006]] 出现数 = 3（与源设计的三个空分类一致）。 **Path**: final
- **SC-002**: 首条种子在场：[[STR-005]] 中 [[STR-007]] 条目同时包含默认 HTTPS 实践、特殊仓库 HTTP 显式提示义务与 `~/.git-credentials` 反例三项（3/3）；守卫对应断言由红转绿。 **Path**: final
- **SC-003**: 积累机制仅以指针声明：观察入口 → 晋升规则的指针链可解析（2/2：`feedback-utils.py --action record`、`knowledge-promotion.md`）；[[STR-001]] 标记在机制声明中在场；模块内第二引擎/存储/渲染器声明出现数 = 0。 **Path**: final
- **SC-004**: 分发与登记成立：`shared/definitions/framework-map.md` 与 `.specify/shared/definitions/framework-map.md` 都含 `.specify/shared/best-practices/` 登记行（2/2）；`sync-mirrors.py --check` 对本模块的源/镜像差集 = 空；init 既有 `shared/` 拷贝步骤覆盖新目录的证明记录在场（代码路径 + 测试），且 `src/` 改动行数 = 0。 **Path**: final
- **SC-005**: 适配与零残留：模块五文档中 `ai-harness` / `.ah/` / `/ah.` 出现数 = 0；模块引用的仓内路径存在率 = 100%；归属声明为 Feature 111。 **Path**: final
- **SC-006**: containment 成立：`git diff --name-only 0419adae5..HEAD` 的变更路径集 ⊆ FR-009 的声明集（集合外路径出现数 = 0；wrap-up 记账记录按 FR-009 的记录体谓词判定，后续特性登记阶段的注册表例外按 FR-009 判定）；引擎/模板/技能/代理/命令/宪法/指令/存储布局/决策治理面改动数 = 0。 **Path**: final
- **SC-007**: 测试证据成立：守卫经 `scripts/bash/run-tests.sh tests/contract/test_general_best_practices.py` 执行退出 0，且 red-first 记录（先红后绿）在场；镜像参数化套件相对入口基线零新增红；全量套件失败名集 ⊆ 入口基线（无 NEW）。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 守卫 `tests/contract/test_general_best_practices.py` 的 (a)(b)(f) 断言输出；`ls` / 文件树读数。
- **SC-002 Source**: 守卫的 (c) 断言输出（对 [[STR-005]] 正文的三项文本断言）。
- **SC-003 Source**: 守卫的 (d) 断言输出（路径解析 + 无第二机制声明扫描）；`feedback-utils.py --help` 的 `record` 动作在场读数。
- **SC-004 Source**: 守卫的 (e) 断言输出；`python3 scripts/python/sync-mirrors.py --check` 逐字输出；`git diff --numstat 0419adae5..HEAD -- src/` 零行读数；init 共享拷贝代码路径的引用记录。
- **SC-005 Source**: 守卫内的残留扫描断言（三组字面量计数 = 0）；被引用路径的存在性断言输出。
- **SC-006 Source**: `git diff --name-only 0419adae5..HEAD` 与 FR-009 声明集的集合差（机器采集）；review 阶段复核一次。
- **SC-007 Source**: `scripts/bash/run-tests.sh` 的退出码与汇总输出；red-first 记录（`test-evidence/`）；全量套件失败名与入口基线的名字级集合差。

## Shared Strings

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "[best-practice]" | FR-004, SC-003 |
| `STR-002` | "programming-languages.md" | FR-001, FR-002, SC-001 |
| `STR-003` | "system-interfaces.md" | FR-001, FR-002, SC-001 |
| `STR-004` | "programming-frameworks.md" | FR-001, FR-002, SC-001 |
| `STR-005` | "programming-tools.md" | FR-001, FR-002, FR-003, SC-001, SC-002 |
| `STR-006` | "尚无条目" | FR-002, SC-001 |
| `STR-007` | "Git clone 的默认协议" | FR-003, SC-002 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-11-27（无人值守 requirements 阶段，自行裁决并记录）

- Q: Feature 身份如何绑定？ → A: 新建独立 Feature **111 General Best Practices（通用最佳实践）**，不迁移源 Feature 040 绑定、不设父切片；注册表行为后续澄清/特性阶段动作（A-3）。
- Q: 五文档还是子集？ → A: 源交付的全部五个文件（清单 + 四个分类 owner 文件）整组移植，含三个"尚无条目"占位（A-2、A-11）。
- Q: 分发如何接线？ → A: 复用既有 `shared/` 整目录 init 拷贝与 `sync-mirrors.py` 镜像对；零 CLI/打包改动（A-5）。
- Q: 源设计实际交付了框架地图行或 instructions 指针吗？ → A: 实测都没有；目标仓按 `directory-governance.md` § 3 补**框架地图行**（同变更、镜像再生成），**不补** instructions 指针（Framework Map 段已是指针）（A-6）。
- Q: 测试面如何裁定？ → A: 一个内容守卫（red-first，六组断言）+ 复用既有参数化镜像套件；Tests Mode ON（A-7）。
- Q: 命名/路径如何适配？ → A: `ai-harness` → `Spec Kit`、`.ah/` → `.specify/`、`/ah.*` → `/speckit.*`、Feature 040 → Feature 111；所有引用路径经实测存在（A-4）。
- Q: 脚手架如何执行？ → A: 脚本会派生 112（并行分支占用编号空间）；按 108 先例手工从模板脚手架，停留在本线分支，偏差记录于 test-evidence（A-9）。
- Q: 本阶段是否更新词汇表/注册表？ → A: 否；写面限于本特性产物，词汇候选留待澄清阶段（A-10）。
- Q: 条目与既有所有者规则冲突怎么办？ → A: 所有者规则胜出；条目不作为第二真源，按 feedback 通道上送（A-13、Edge Cases）。