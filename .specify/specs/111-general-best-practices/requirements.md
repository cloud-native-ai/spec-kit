# Requirements Specification: General Best Practices — 通用最佳实践模块（四分类封闭集 + 渐进积累）

**Requirement Branch**: `111-general-best-practices`
**Created**: 2026-11-27
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（新增/晋升条目、维护四分类封闭集与守卫、判断「一条经验属于哪个分类、何时可以晋升」的人）与下游项目维护者（`specify init` 后在 `.specify/shared/best-practices/` 消费内容、或在本地按积累机制沉淀经验的人）——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 当需要判定「模块由哪些文档构成、四分类封闭集如何变更」「一条最佳实践必须长什么样」「一条开发观察如何经既有 feedback 引擎记录、按清单晋升程序沉淀为条目、如何可回溯」「模块如何随 `shared/` 分发并在框架地图登记」「本特性的改动边界是什么」时打开本规格，据 FR-001…FR-009 与 SC-001…SC-007 放行 `/speckit.clarify` 与后续规划
**Input**: User description: "Port the closed ai-harness 087 general best-practices capability into spec-kit as new spec 111-general-best-practices: `shared/best-practices/` with the five documents (manifest + four category owner files), distribution through the existing `shared/` shipping/init flow, and any framework-map/instructions wiring the source design requires; additive documentation surfaces only — no engine/runtime change, no store layout, no decision-governance alignment. Bind Feature 111."

**输入校正**：①「五文档」按源交付面读作**清单 README + 四个分类 owner 文件**（共五个文件），不是五个分类；②「closed ai-harness 087 capability」读作源规格 `087-general-best-practices` 的已定稿交付面（`requirements.md` / `plan.md` / `tasks.md` / `contracts/best-practices.contract.md` / `verification.md` 五处所描述的：清单 + 四个分类文件 + 首条 + 积累机制 + 守卫 + 镜像），不是照搬源仓的构建流程；③源规格的 Feature 绑定（ai-harness Feature 040 Knowledge & Session Utilities）**不复用**——spec-kit 注册表没有同名 Feature，本特性按简报绑定为一个新的独立 Feature 111（A-3）；④"verify what the source actually shipped before adding" 是**实测义务**：源仓实测未新增框架地图行、也未新增 instructions 指针（A-6），本特性据目标仓治理判定只补框架地图行。

## Related Feature *(mandatory)*

**Feature ID**: 111
**Feature Name**: General Best Practices（通用最佳实践）

**Binding basis**: 简报固定绑定 Feature 111；本特性是**新的独立 Feature**（无父切片）：它交付随框架分发的**内容模块**，观察记录只按指针复用既有 feedback 引擎（Feature 028 Feedback Mechanism），知识记录义务按指针归既有 `knowledge-promotion` owner；晋升程序与通用判据为模块清单自有规则（A-22），不扩展任何引擎行为。源规格绑定的 ai-harness Feature 040 在 spec-kit 注册表中无对应条目，按"源 registry ID 不复用"的简报约束不迁移该绑定。索引行与详情文件的登记属后续澄清/特性阶段动作，本规格不代行（A-3、A-10）。

## Overview

**问题**：spec-kit 已经拥有机制类文档层——`shared/guidelines/`（纪律）、`shared/definitions/`（概念所有者）、`shared/workflow/`（流程约定）——但没有一个沉淀**日常开发经典最佳实践**的内容层：反复出现的通用工程经验（例如 git clone 的协议口径）没有唯一沉淀点，每次都靠会话记忆或临时口口相传重新发现；即使被记录，也没有"观察 → 复核 → 晋升"的可回溯积累路径。

**源事实（ai-harness 087，2026-11-25 定稿，已实测）**：源仓在 `shared/best-practices/` 建立了**四分类封闭集**模块——清单 `README.md`（声明分类集合、条目形态与积累机制）+ 四个 owner 文件 `programming-languages.md` / `system-interfaces.md` / `programming-frameworks.md` / `programming-tools.md`（其中前三者以"尚无条目"占位）+ 首条种子（`programming-tools.md` § Git clone 的默认协议）+ 源契约 `best-practices.contract.md`（源仓五条条款，其编号不复用） + 守卫 `tests/contract/test_general_best_practices.py` + `.ah/shared/best-practices/` 镜像；verification 记录三条 SC 全部 pass。源仓**未**新增框架地图行、**未**新增 instructions 指针（全仓检索 `best-practices` 在模块与规格之外零命中）；accumulation 复用既有 feedback + memory 引擎，不新建机制。

**目标基线实测（2026-11-27，base `0419adae5`）**：

1. `shared/` 现有 `constants/` / `declarations/` / `definitions/` / `guidelines/` / `patterns/` / `workflow/`，**没有** `best-practices/`；`.specify/shared/` 无同名目录。
2. `specify init` 已把 `shared/` 整目录拷贝到目标项目 `.specify/shared/`（`src/specify_cli/__init__.py` 的 shared 拷贝步骤），新增子目录随既有流程自动分发，无需改代码。
3. `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS` 含 `("shared", ".specify/shared")`，镜像按目录整树比较/写入；`tests/contract/test_mirror_parity_suite.py` 从该引擎派生参数表，新文件自动纳入字节一致检查。
4. `.specify/instructions.md`、`.specify/glossary.md`、`shared/definitions/framework-map.md` 对 `best-practices` 零命中；`shared/definitions/framework-map.md` 是 `.specify/` 布局的单一所有者，`.specify/instructions.md` 的 Framework Map 段只是指向它的指针。
5. `shared/guidelines/directory-governance.md` § 3 规定「新顶层目录或既有树下**首个新种类目录** MUST 在同一变更内登记到其区域地图」；框架布局的区域地图即 `shared/definitions/framework-map.md`。
6. 编号空间：仓内 spec 目录最大为 108，本地分支 `109-prompt-adherence` / `110-context-management` / `111-general-best-practices` 已占用；本线固定编号 111（脚手架脚本会派生 112，见 A-9）。

**本特性交付**：`shared/best-practices/` 模块（清单 + 四个分类 owner 文件 + 首条种子 + 积累机制指针）；`shared/definitions/framework-map.md` 的登记行（同变更落地，镜像再生成）；守卫 `tests/contract/test_general_best_practices.py`；`.specify/shared/best-practices/` 镜像。**全部为增量文档面**，分发复用既有 `shared/` 整目录拷贝与镜像机制。

**不做什么**：不新增引擎、运行时行为、CLI/init 代码、运行时存储或 `.gitignore` 规则；不新建第二积累机制（观察记录按指针复用既有 feedback 引擎；知识记录义务按指针归既有 owner；晋升程序与通用判据由清单自有声明，A-22）；不改 `.specify/instructions.md` 与模板（Framework Map 段已是指针，One Source of Truth）；不改决策治理面（`shared/definitions/decision-definitions.md` 及其检查器零修改；本特性不产出决策项）；不改写任何 dated record；不在本阶段编辑特性注册表或词汇表（A-10）。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **类别判定 = `execution`**：验收 oracle 是机器执行的契约守卫（存在性、封闭集、指针解析、镜像一致、零残留），不是"人读懂内容"的表达类 oracle。 | 按验收 oracle 判定（`shared/definitions/flow-class-definitions.md`）；内容写作质量归评审，不改变类别。 |
| **A-2** | **范围 = 源交付的全部五个文件**：清单 + 四个分类 owner 文件整组移植，含三个"尚无条目"占位与一个首条种子。 | 四分类**封闭集**本身就是能力；只移一部分会破坏封闭集并让守卫失去意义。源设计未声明子集。 |
| **A-3** | **绑定新的独立 Feature 111**；不迁移源 Feature 040 绑定、不设父切片、不复用源 registry ID。特性索引行与详情文件由后续**特性登记阶段**添加（clarify 阶段写面同样不含注册表，A-10、A-21），本阶段不编辑注册表。 | 简报明确"bind spec-kit Feature 111 (source registry ID not reused)"；目标注册表无 Knowledge & Session Utilities 同义条目，硬绑会误导所有权。 |
| **A-4** | **命名/路径适配**（逐项核实）：`ai-harness` → `Spec Kit`；`.ah/` → `.specify/`；`/ah.*` → `/speckit.*`（源五文档中实际无 `/ah.*` 引用）；归属声明 `Feature 040` → `Feature 111`；观察入口指针落到既有 `.specify/scripts/python/feedback-utils.py`（`record` 动作已存在）；知识记录义务指针落到 `.specify/shared/guidelines/knowledge-promotion.md`（存在；该 owner 不定义 feedback → 分类 owner 文件的晋升程序，见 A-22）；晋升程序与通用判据为清单自有规则；镜像目标 `.specify/shared/best-practices/`。 | 源文按产品名与运行时路径书写；目标仓路径实测存在（见 Overview § 目标基线）。 |
| **A-5** | **分发 = 复用既有 `shared/` 通道**：`specify init` 的整目录拷贝 + `sync-mirrors.py` 的 `shared → .specify/shared` 镜像对；**零** CLI/打包/`.gitignore` 改动。 | Overview 实测第 2、3 条：两条通道已覆盖任意新增 `shared/` 子目录；新增改动即为过度工程（宪法 IX）。 |
| **A-6** | **框架地图行 = 目标仓治理要求，MUST 补；instructions 指针 = 不补**。源仓实测两者皆未做；但 `directory-governance.md` § 3 要求新种类目录同变更登记到区域地图（`shared/definitions/framework-map.md`）。`shared/` 是**已分发**目录（source 与 `.specify/shared/` 镜像三副本拓扑），其新子目录种类按框架布局行登记。`.specify/instructions.md` 的 Framework Map 段已是指向地图的指针，补第二段会复制事实（宪法 XIV）。 | 源设计的"未做"是源仓未受该治理约束的证据，不是目标仓可以遗漏登记的理由；登记行满足"文档化含义"义务且不新增第二真源。 |
| **A-7** | **测试 = 一个内容守卫 + 复用既有镜像参数化套件**，Tests Mode 记为 ON（源规格同为 ON）：`tests/contract/test_general_best_practices.py` 以 red-first 钉住 FR-007 的六组断言；镜像字节一致由 `tests/contract/test_mirror_parity_suite.py` 自动覆盖，本守卫不复制第二套比较逻辑。一次全量跑 `scripts/bash/run-tests.sh` 记录基线。 | 源规格 FR-005 的守卫先例；目标仓已有从 `sync-mirrors.py` 派生参数的镜像套件，重复实现违反 One Source of Truth 与测试执行效率纪律。 |
| **A-8** | **内容保真**：五个文档按实质逐字移植（中文正文、双语标题、条目形态 = 标题 + 实践 + 反例/证据），保留三个"尚无条目"占位与首条 `~/.git-credentials` 反例；仅按 A-4 适配产品名与路径。 | 移植的语义对象是源已定稿内容；改写会引入未受源 verification 覆盖的新文本。 |
| **A-9** | **脚手架偏差（披露）**：`create-new-requirements.sh` 从 spec 目录（最大 108）**加**本地分支名派生编号，`109/110/111` 三条并行线分支都在编号空间内，脚本会派生 **112** 并新建分支——与本线"固定编号 111、停留在 `111-general-best-practices` 分支"冲突。按 108 A-16 先例，本阶段从 `.specify/templates/requirements-template.md` **手工**脚手架到 `.specify/specs/111-general-best-practices/requirements.md`，等价复刻模板拷贝、仅跳过建分支步骤，并记录于 `test-evidence/requirements-stage-2026-11-27.md`。 | 工作树必须停留在本线分支；脚本把"本线分支"当成"已用编号"是编号派生的既有陷阱（create-requirements 技能 § 2 已记录同名陷阱）。 |
| **A-10** | **本阶段写面 = 仅本特性产物**：`.specify/specs/111-general-best-practices/**`（requirements、checklists、test-evidence）；不编辑状态脊、特性注册表、词汇表或任何镜像。词汇候选（"best practice / 最佳实践"、"progressive accumulation / 渐进积累"）不在本阶段入表，留待澄清阶段按词汇协议提议——clarify 阶段已按 **A-21** 收敛：提案文本定格，登记时点外置。 | 简报约束"Only this feature's artifacts; no push; no spine/registry edits"；词汇协议允许澄清阶段再提议，避免越界写项目锚点。 |
| **A-11** | **空分类是设计状态，不是缺陷**：三个空分类文件以"尚无条目"占位 + 分类范围说明交付；守卫 MUST NOT 要求非空条目。占位与条目互斥的机器不变式见 **A-16**；"编造条目充数"属积累纪律与评审判定，守卫不声称能判断条目语义真伪。 | 源规格同形态；渐进积累的前提是"干净运行不追加空洞条目"（README 红线）。 |
| **A-12** | **containment 声明的基线与允许增量集由 FR-009 单一拥有**：基线 `0419adae5`；允许变更路径集、以及后续特性登记阶段对注册表的唯一例外都在该条定义；SC-006 只引用，不复述。 | 封闭声明须有基线 referent 与可推导允许增量（owner：`shared/guidelines/closed-set-claims.md`）；同一事实只留一个所有者。 |
| **A-13** | **与决策治理无关**：本特性不产出决策项、不改 `decision-definitions.md`、不触发 `validate-decisions.py` 的任何新规则；内容条目若与既有所有者规则冲突，所有者规则胜出，条目 MUST NOT 作为第二真源落地（Edge Cases）。 | 简报明确"no decision-governance alignment"；One Source of Truth 要求最佳实践不得覆盖机制所有者。 |
| **A-14** | **客户项目再初始化语义沿用现状**：模块随 `shared/` 整目录拷贝；对客户本地修改的保留/覆盖行为与其它 `shared/` 文档一致，本特性不新增保留保证，也不测试该既有语义。 | 不引入新契约；避免为既有分发行为另立承诺（宪法 IX）。 |
| **A-15** | **模块形状的机器可判定形态**：`shared/best-practices/` **顶层文件集恰为五文档**（`README.md` + 四个 owner 文件；多余文件即守卫转红）；清单的封闭集声明 MUST 是模块内**唯一表格**——三列（模块 / 文件 / 内容）、恰四行数据行，四行「模块」单元为 编程语言 / 系统接口 / 编程框架 / 编程工具 且一一对应各自文件，每行恰含一个相对链接、链接目标集合恰为 [[STR-002]]…[[STR-005]]，并含字面量「封闭集」。 | FR-007(a) 的"恰为四类"需要可解析的声明载体；表格是源已定稿形态（A-8），钉成守卫可执行的形状不引入新文本内容。 |
| **A-16** | **条目形态与空分类不变式的机器形态**：条目 = owner 文件中一个 `## ` 标题 + `**实践**` 项目符号 + `**反例 / 证据**` 项目符号（可选 `**延伸**`；晋升条目另须 `**来源**`，A-17）；每个 owner 文件 H1 标题唯一，并携带回指清单的积累机制块引用（README.md 链接 +「积累机制」字样 + 条目形态三元）；**占位 ⇔ 零条目**（恰一行含 [[STR-006]] 的斜体占位、该文件零个 `## ` 条目；首次晋升时同变更移除占位）。守卫 MUST NOT 把占位数量冻结为 3（交付态计数 3 是 SC-001 的测量），也 MUST NOT 宣称能判断条目语义真伪。 | FR-007(b)(c) 的"占位""条目形态"若不钉结构就不可判定；冻结数量会让下一次合法晋升迫使守卫改动，违背渐进积累。 |
| **A-17** | **晋升与回放的追溯形态（可执行字段与身份约定）**：观察 = 既有 feedback 记录，经 `--action record` 写入；[[STR-001]] 标记与四类之一的 **owner 文件 stem**（`programming-languages` / `system-interfaces` / `programming-frameworks` / `programming-tools`）写入该记录的 **`--review` 文本**（记录形态、其余参数与存储处置归引擎 `--help`，不新增字段或动作；AR1-01 裁定）。身份约定：摩擦发生在框架命令/技能运行内时用该运行的 unit id 与类型（`/speckit.<command>`+`command` 或 `skill:<name>`+`skill`）并以该 run id 作 `--run-id`；无此类运行承载的 ad-hoc 观察用 `--unit-id custom:best-practices/observation --unit-type custom-unit --run-id bp-<yyyy-mm-dd>-<slug>`（slug 为 ASCII 稳定短名），装载 probe 注册表的工作区须先按 probe 系统为该 custom 单元建立外部 probe（`probe-utils.py --action probe-inject`，义务归 probe 系统，模块只引用）。晋升条目 MUST 携带 `**来源**` 项目符号，至少含 feedback 条目 ID / 提交号（hex，≥7 位）/ 会话原话引用之一，并写明"通用"判定依据（反复出现或一次明确的用户纠正）。晋升不改写既有观察记录、不新增 feedback 状态；**种子条目豁免来源行**——其来源是促成本特性的用户原始报告（Input），模块文本 MUST NOT 编造 feedback ID。 | 回放路径 = 从条目 `**来源**` 行反向抵达观察；字段与身份约定向引擎实测接口对齐（`--review` 是既有记录中承载自由文本的字段；`custom:` 单元在注册表工作区需要外部 probe，实测记录于 `test-evidence/analyze-repair-round1.md`），反馈存储的处置仍归 feedback 引擎（One Source of Truth）。 |
| **A-18** | **分发与镜像的执行形态**：镜像 MUST 由 `python3 scripts/python/sync-mirrors.py` 的**写模式**在同一变更内再生成，MUST NOT 手改镜像文件；源/镜像字节一致由既有 `tests/contract/test_mirror_parity_suite.py` **唯一**裁决，守卫 MUST NOT 复制比较逻辑；验证记录 MUST 含 `--check` 零漂移输出。init 分发证明 = 代码路径引用（`src/specify_cli/__init__.py` 的 shared 整目录拷贝步骤）+ 既有 init 集成测试（`tests/integration/test_init_new_layout.py`，运行同一拷贝步骤）+ 一次**记录的只读初始化演练**（同一调用形态 `--here --ai qoder --script sh --no-git`，在 `.specify/.tmp/` 临时根内执行，读 `.specify/shared/best-practices/` 恰含五文档）；不新增第二个测试文件。守卫以 `pytest.mark.contract` 标记注册。 | 既有 init 测试运行拷贝步骤但不点名本模块；演练是只读、可复现、零新契约的证据。FR-009 只允许一个新增测试文件，证明不能寄望新测试。 |
| **A-19** | **框架地图行的行形态**：登记行 MUST 位于 `shared/definitions/framework-map.md` 唯一布局表内、与既有 `.specify/shared/` 行相邻，沿用三列形态；Where 单元 = `.specify/shared/best-practices/`；Notes 单元 MUST 同时包含 **Feature 111**、清单 `README.md` 指针与兄弟行的 `(framework source: shared/best-practices/)` 来源指针；表内该目录**恰一行**，源与镜像各恰一行（镜像经 sync-mirrors 再生成）。 | FR-007(e) 需要可判定的登记断言；"含路径字符串"不足以证明所有者在场，路径 + Feature 111 双 token 让登记可判定。 |
| **A-20** | **containment 的残余判定程序**：`git diff --name-only 0419adae5..HEAD` 先减去 FR-009 声明集中的字面路径前缀；残余路径仅当全部落在 `.specify/session/` / `.specify/feedback/` / `.specify/exec-quant/` 三存储、且其**记录体**（frontmatter 或正文）含特性 key `111-general-best-practices` 或 run id `r20261127T071500Z-111a` 时放行，其余残余 = 违规。各阶段 MUST 只写 per-entry 文件；MUST NOT 改写 `.specify/exec-quant/records.jsonl` / `scores.jsonl`、feedback 聚合/索引或任何共享聚合；`.specify/state/`（git-ignored 运行时状态）与 `.specify/trigger/` 不被本特性写。 | 封闭声明须可判定（`closed-set-claims.md`）；记录体谓词是"记账记录"与"共享状态改写"的分界，避免把同目录的任何新文件都当作合法。 |
| **A-21** | **词汇交接（本阶段不写词表）**：词汇候选 "best practice / 最佳实践"（日常开发中反复出现、值得沉淀的经典工程经验）与 "progressive accumulation / 渐进积累"（观察 → 复核 → 晋升的增量沉淀机制）在本规格定格为**提案文本**；本阶段写面仅本特性产物，**不写** `.specify/glossary.md`。词汇协议点名的检查点是 requirements / plan / tasks / implement，而本线 containment（FR-009）不含词表——因此**本线内**登记词表须先修正 FR-009，否则只能在特性封存后另行登记。 | 简报写面"only this feature's artifacts"与 FR-009 的封闭声明都不含 `glossary.md`；A-10 的"留待澄清阶段提议"在此收敛为"提案文本定格 + 登记时点显式外置"。 |
| **A-22** | **晋升程序与通用判据的所有者 = 模块清单**（AR1-02 裁定）：源 087 只把晋升指向 `knowledge-promotion.md`，而该 owner 定义知识记录义务与 2+ 强调升级，不含 feedback → 分类 owner 文件的晋升程序；本特性因此把**晋升程序、"通用"判据（反复出现或一次明确的用户纠正）与 `**来源**` 追溯形态**的所有者定为清单「逐步积累机制」节（随 `shared/` 分发的自有声明面）；`knowledge-promotion.md` 只以指针承担知识记录义务与强调升级；`feedback-utils.py` 仍拥有记录形态、存储与处置。 | 声明了 X 的 owner 必须真拥有 X（宪法 XIV）；源指针只有路径存在证据、没有内容适配证据；把规则放进随模块分发的清单，使 owner 与消费者可达同一文件，且特性保持纯增量（引擎零改动）。 |
| **A-23** | **观察载体 = `--review` 文本 + 身份约定**（AR1-01 裁定）：引擎 `record` 的必填参数为 `--unit-id` / `--run-id` / `--review` / `--points`，无 `notes` 字段且 `--notes` 会被静默丢弃；因此 [[STR-001]] 标记与 owner 文件 stem 写入 `--review` 文本；身份约定与 probe 前提按 A-17 执行。 | 需求必须落在引擎真实存在的字段上；实测 2026-11-27（`--action args-manifest`、legacy 工作区 record 成功读数、带 probe 注册表工作区的 record 失败读数与注册表依赖），记录于 `test-evidence/analyze-repair-round1.md`。 |
| **A-24** | **任务序修复 = US1 末尾先建镜像（T007A）**（AR1-03 裁定）：C-404 的模块读取前导要求断言模块引用的每个仓内路径（含 `.specify/shared/best-practices/`）存在，而镜像原在 T012 才生成；改为在 US1 内容落地后、T008 绿点前插入写模式镜像再生成（T007A），T012 仍作最终再生成收口。 | 保持 C-404 前导断言不削弱（不放宽为"源侧路径"），修复的是任务图而非契约；T009 之后至 T012 之间镜像短暂落后于源，最终态由 T012/T013 收敛并以既有镜像套件唯一裁决。 |

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

框架维护者在一次真实开发摩擦后，用既有 feedback 引擎记下一条带标记的观察；当同一摩擦再次出现或被一次明确的用户纠正证明为**通用**时，他按清单「逐步积累机制」节的晋升程序把它提升进匹配的分类 owner 文件（晋升程序与"通用"判据由清单拥有，知识记录义务按指针归既有 owner），条目带有可回溯的来源（feedback 条目 ID / 提交号 / 会话原话）。全程没有新引擎、新存储或新渲染器。

**Why this priority**: 没有积累路径，模块会停在首条种子；而新建第二机制会与既有 feedback 引擎和知识记录 owner 形成双轨，破坏 One Source of Truth。

**Independent Test**: 从清单与 owner 文件核对积累机制声明：观察入口指向既有 feedback 引擎的动作面、晋升程序与通用判据由清单「逐步积累机制」节唯一拥有、知识记录义务指向既有 `knowledge-promotion` owner、回溯要素在场；全模块检索无第二引擎/存储声明。守卫断言指针可解析且无第二机制。

**Acceptance Scenarios**:

1. **Given** 一次真实开发摩擦，**When** 维护者用 `.specify/scripts/python/feedback-utils.py --action record` 记录观察——[[STR-001]] 标记与所属分类 stem 写入 `--review` 文本，身份约定按 A-17——**Then** 该观察落在既有 feedback 存储，MUST NOT 直接写入模块条目区。
2. **Given** 一条观察被证明通用（反复出现或一次明确的用户纠正），**When** 按清单「逐步积累机制」节的晋升程序（A-22 的规则所有者）晋升，**Then** 条目 MUST 落在匹配的分类 owner 文件并遵守条目形态，且携带观察来源；MUST NOT 编造数值或证据。
3. **Given** 积累机制声明，**When** 维护者检索模块与守卫，**Then** MUST NOT 存在第二引擎、第二存储、第二渲染器或索引的声明；观察与存储按指针复用既有 feedback 引擎，知识记录义务按指针归既有 owner，晋升程序为清单自有规则。

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
- **空分类文件**：保留恰一行 [[STR-006]] 占位与范围句、零个 `## ` 条目；占位与条目互斥——首次晋升时同变更移除占位；MUST NOT 移除文件、MUST NOT 编造条目（A-11、A-16）。
- **交付态计数与积累的张力**：某分类首次晋升后占位数量下降，SC-001 的"= 3"不再成立——该计数只约束交付态，守卫按 A-16 的互斥不变式判定，不冻结数量。
- **镜像手改**：镜像 MUST 由 `sync-mirrors.py` 写模式生成；手改造成的漂移由既有镜像套件转红（FR-006、A-18）。
- **词表登记越界**：本线 containment 不含 `.specify/glossary.md`；在本线内登记词表须先修正 FR-009，否则只能在特性封存后另行登记（A-21）。
- **相对链接断裂**：清单 ↔ 四个 owner 文件的任一链接不可解析即使守卫转红。
- **产品名残留**：模块文本出现 `ai-harness` / `.ah/` / `/ah.` 即使守卫转红（FR-008）。
- **客户项目本地修改后再 init**：沿用既有 `shared/` 刷新语义，本特性不新增保留保证（A-14）。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 在 `shared/best-practices/` 创建模块清单 `README.md`，声明**封闭的四分类集**——编程语言 / 系统接口 / 编程框架 / 编程工具，每类恰一个 owner 文件：[[STR-002]]、[[STR-003]]、[[STR-004]]、[[STR-005]]——以及模块读者与范围（日常开发可复用的经典经验库，渐进积累而非一次性清单）和统一**条目形态**（标题 + 实践 + 反例/证据；结构按 A-16：`## ` 标题 + `**实践**` + `**反例 / 证据**` 项目符号，可选 `**延伸**`）。清单的分类表 MUST 逐行链接到四个 owner 文件；机器形态按 **A-15**：分类表是清单唯一表格（三列、恰四行、每行恰一相对链接、链接目标集合 = 四个 owner 文件），模块顶层文件集恰为五文档，清单含字面量「封闭集」。封闭集变更（新增/删除/改名分类）MUST 在同一变更内同时修订清单、建立或迁移对应 owner 文件并更新守卫（FR-007）；MUST NOT 只新增文件不改清单。
- **FR-002**: 创建四个分类 owner 文件：[[STR-002]]、[[STR-003]]、[[STR-004]]、[[STR-005]]。每个文件 MUST 以唯一 H1 分类标题标识自身，并携带回指清单的积累机制块引用（README 链接 + 条目形态三元，A-16）；分类范围（scope）由清单分类表「内容」列单一拥有，owner 文件不复述（空分类在占位句中复述一句范围说明）。**尚无条目**的分类 MUST 以恰一行含 [[STR-006]] 的斜体占位 + 一句话范围说明交付，且该文件零个 `## ` 条目（占位 ⇔ 零条目的互斥不变式，A-16）；MUST NOT 删除该文件，MUST NOT 以编造条目充数（A-11；语义真伪归评审判定）。
- **FR-003**: 在 [[STR-005]] 中种子首条 [[STR-007]]：git 这个编程工具的 clone 默认口径——**默认用 HTTPS 作 clone URL**；特殊仓库必须走 HTTP（或 SSH）时 MUST 显式提示该仓库的协议与凭据要求，以此达成统一；反例/证据 MUST 记录 `~/.git-credentials` 记录了 HTTP 认证信息而 install 流程用 HTTPS 发起 clone 导致失败的协议错位认知偏差；延伸口径（内网 git 服务在 HTTPS 需认证而 SSH 匿名/key 可用时，install 源 URL 优先给 SSH 或明确提示认证方式）MUST 保留。条目 MUST 遵守 FR-001 的条目形态。种子条目的来源是促成本特性的用户原始报告（本规格 Input）；模块文本 MUST NOT 编造 feedback ID 或来源行（A-17）。
- **FR-004**: 在清单的**逐步积累机制**节声明渐进积累：开发观察经 `.specify/scripts/python/feedback-utils.py --action record` 落为带 [[STR-001]] 标记与所属分类的观察（约定形态按 A-17：标记与四类之一的 owner 文件 stem 写入既有记录的 `--review` 文本，身份与 run id 约定按 A-17，不新增字段、动作或存储）；**晋升程序、"通用"判据（反复出现或一次明确的用户纠正）与 `**来源**` 追溯形态由该节唯一拥有**（A-22）——当观察被证明通用时，按该节程序晋升进匹配的分类 owner 文件，并在条目的 `**来源**` 项目符号中记录观察来源（feedback 条目 ID / 提交号 hex ≥7 位 / 会话原话引用之一）与"通用"判定依据，使条目可回溯；晋升不改写既有观察记录（A-17）。红线：干净运行 MUST NOT 追加空洞条目，MUST NOT 编造数值或证据。机制 MUST 复用既有 feedback 引擎，MUST NOT 新建第二引擎、存储、渲染器或索引；反馈记录的形态与处置按指针归 `feedback-utils.py`，知识记录义务按指针归 `.specify/shared/guidelines/knowledge-promotion.md`——清单只引用这两个所有者、不复述其取值；模块自有的晋升程序与判据由清单声明，不构成复述（A-22）。
- **FR-005**: 在 `shared/definitions/framework-map.md` 新增一行，登记 `.specify/shared/best-practices/` 为随框架分发的通用最佳实践内容模块，指向本模块清单与 Feature 111；行形态按 A-19：位于地图唯一布局表、与既有 `.specify/shared/` 行相邻、三列形态，Where 单元 = `.specify/shared/best-practices/`，Notes 单元同时含 Feature 111、清单 `README.md` 指针与 `(framework source: shared/best-practices/)` 来源指针，该目录在源与镜像表中各恰一行。该登记 MUST 与模块创建**同一变更**落地（`shared/guidelines/directory-governance.md` § 3）。镜像 `.specify/shared/definitions/framework-map.md` 由既有镜像机制再生成，MUST NOT 手改。`.specify/instructions.md` 与指令模板 MUST NOT 新增指针段（现有 Framework Map 段已是指向地图的指针，A-6）。
- **FR-006**: 分发 MUST 复用既有 `shared/` 通道，不新增打包或运行时面：(a) `specify init` 既有的 `shared/` 整目录拷贝使模块落到客户项目 `.specify/shared/best-practices/`；(b) `scripts/python/sync-mirrors.py` 的既有 `shared → .specify/shared` 镜像对 MUST 覆盖本模块并保持源/镜像字节一致；(c) 镜像由 sync-mirrors **写模式**在同一变更内再生成，MUST NOT 手改，字节一致由既有参数化镜像套件唯一裁决，守卫 MUST NOT 复制比较逻辑（A-18）。MUST NOT 新增运行时存储、`.gitignore` 规则、CLI 代码或打包清单改动。
- **FR-007**: 守卫 `tests/contract/test_general_best_practices.py` MUST 以 red-first 方式钉住（结构形态按 A-15 / A-16 / A-17）：(a) 模块顶层文件集恰为五文档；清单唯一分类表恰四行、每行恰一相对链接、链接目标集合恰为 [[STR-002]]、[[STR-003]]、[[STR-004]]、[[STR-005]]，且含「封闭集」字面量；(b) 每个 owner 文件 H1 唯一并携带回指清单的积累机制块引用；空分类 ⇔ 恰一行含 [[STR-006]] 的占位且零个 `## ` 条目；每个条目含 `**实践**` 与 `**反例 / 证据**` 项目符号（可选 `**延伸**`），非种子条目另含 `**来源**`；守卫 MUST NOT 把占位数量冻结为 3，MUST NOT 声称判定条目语义真伪；(c) 首条 [[STR-007]] 在 [[STR-005]] 中的三项内容断言（默认 HTTPS 实践 / 特殊仓库 HTTP 显式提示义务 / `~/.git-credentials` 反例）加延伸 SSH 口径在场；(d) 机制指针可解析——`.specify/scripts/python/feedback-utils.py` 的 `--help` 动作集含 `record`、`.specify/shared/guidelines/knowledge-promotion.md` 存在、清单含 [[STR-001]] 字面量；第二机制检查 = `scripts/python/` 下不存在以 best-practices 命名的引擎文件，文本层的第二机制声明归评审（SC-003）；(e) 框架地图源与镜像各含恰一行同时带 `.specify/shared/best-practices/` 与 `Feature 111` 的表行；(f) 清单 ↔ 四个 owner 文件的相对链接全部可解析。镜像字节一致性由既有 `tests/contract/test_mirror_parity_suite.py` 覆盖，本守卫 MUST NOT 复制第二套镜像比较逻辑。守卫以 `pytest.mark.contract` 标记注册，MUST 经唯一测试入口 `scripts/bash/run-tests.sh` 执行。
- **FR-008**: 适配与零残留：移植内容的产品名与路径 MUST 适配为 spec-kit 口径——`ai-harness` → `Spec Kit`，`.ah/` → `.specify/`，`/ah.*` → `/speckit.*`（源五文档实际无此类引用，出现时一并适配），归属 `Feature 040` → `Feature 111`。模块文本 MUST NOT 含 `ai-harness`、`.ah/`、`/ah.` 残留，MUST NOT 含指向源仓路径的引用；模块引用的每个仓内路径 MUST 在目标仓存在。
- **FR-009**: 边界封闭（可判定）：本特性相对基线 `0419adae5` 的**变更路径集**恰为——`.specify/specs/111-general-best-practices/**`（本规格全过程产物）、`shared/best-practices/**`（五个文档）、`.specify/shared/best-practices/**`（镜像再生成）、`shared/definitions/framework-map.md` 与 `.specify/shared/definitions/framework-map.md`（登记行及其镜像）、`tests/contract/test_general_best_practices.py`（守卫）、以及 **wrap-up 记账记录**——`.specify/session/`、`.specify/feedback/`、`.specify/exec-quant/` 中由本特性各阶段运行经既有三个记账引擎产生的 per-entry 文件（判定谓词：记录体内携带特性 key `111-general-best-practices` 或本线 run id `r20261127T071500Z-111a`）；后续特性登记阶段对 `.specify/features.md` 与 `.specify/features/111-*.md` 的登记行是唯一例外。集合之外的路径 MUST 保持零差异；MUST NOT 改动引擎、模板、技能、代理、命令、宪法/指令、运行时存储布局或决策治理面。残余路径判定程序按 A-20 执行（路径集差 + 三记账存储的记录体谓词）；各阶段 MUST 只写 per-entry 记账文件，MUST NOT 改写既有聚合/索引文件（如 `.specify/exec-quant/records.jsonl` / `scores.jsonl`）；词汇表登记不在本声明集内（A-21）。

### Key Entities *(include if requirement involves data)*

- **Category（分类，封闭集）**: 编程语言 / 系统接口 / 编程框架 / 编程工具；每个分类恰有一个 owner 文件，集合变更须同变更修订清单、文件与守卫。
- **Entry（条目）**: 统一形态 = `## ` 标题 + `**实践**` + `**反例 / 证据**`（可选 `**延伸**`）；晋升条目另带 `**来源**`（A-16、A-17）；种子条目以促成规格的用户原始报告为来源，模块文本不编造 feedback ID。
- **Manifest（清单）**: `README.md` 声明封闭集（唯一三列四行表，A-15）、条目形态、模块读者与范围、积累机制指针。
- **Observation（观察）**: 既有 feedback 存储中的一条记录，其 `--review` 文本携带 [[STR-001]] 标记与四类之一的 owner 文件 stem，身份约定按 A-17；"通用"证明前不进入模块。
- **Guard（守卫）**: `tests/contract/test_general_best_practices.py`，red-first 钉住模块形状、指针、登记与零残留；其可判定边界按 A-16 / SC-003（语义真伪不属守卫断言）。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时依赖、不新增第三方包——它只新增 Markdown 内容、一行框架地图登记与一个 pytest 守卫，消费既有的 Python 解释器、pytest、唯一测试入口与既有镜像引擎。表中 `Premises` 引用的 `EP-NNN` 由 plan 阶段 `## Execution Premises` 定义（本阶段只保留引用）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | 内容模块（清单 + 四个 owner 文件 + 首条） | in-scope | 本特性：`shared/best-practices/` + 镜像 | 四分类封闭集；随 `shared/` 分发 | 本规格 FR-001…FR-003（plan 阶段契约细化） | FR-007 守卫的 (a)(b)(c)(f) 四条断言转绿 | FR-001, FR-002, FR-003 | EP-001 |
| RS-002 | 积累机制声明 + 内容守卫 | in-scope | 本特性：`README.md` + `tests/contract/test_general_best_practices.py` | feedback 观察（指针）→ 按清单自有晋升程序沉淀（A-22）；red-first | 本规格 FR-004、FR-007 | 守卫的 (d) 段断言 + 指针解析；无第二机制声明 | FR-004, FR-007 | EP-002 |
| RS-003 | 分发登记与镜像（框架地图行 + `shared → .specify/shared` 镜像对） | in-scope | 既有：`shared/definitions/framework-map.md` + `scripts/python/sync-mirrors.py`（零修改消费） | 同变更登记；字节一致 | 本规格 FR-005、FR-006 | `sync-mirrors.py --check` 对本模块零漂移；守卫的 (e) 段断言 | FR-005, FR-006 | EP-003 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 模块形状成立：`shared/best-practices/` 顶层文件集恰为清单与四个 owner 文件（5/5，无额外文件）；清单唯一分类表恰四行、声明的封闭集恰为四类（[[STR-002]] / [[STR-003]] / [[STR-004]] / [[STR-005]]）且每类链接到恰一个 owner 文件（4/4，A-15）；清单 ↔ owner 文件相对链接可解析率 = 100%；空分类占位 [[STR-006]] 出现数 = 3 且每个空分类零条目（**交付态**测量；守卫按 A-16 的互斥不变式判定，不冻结该数量）。 **Path**: final
- **SC-002**: 首条种子在场：[[STR-005]] 中 [[STR-007]] 条目同时包含默认 HTTPS 实践、特殊仓库 HTTP 显式提示义务与 `~/.git-credentials` 反例三项（3/3），且延伸口径（HTTPS 需认证而 SSH 可用时优先 SSH 或明示认证方式）在场；守卫对应断言由红转绿。 **Path**: final
- **SC-003**: 积累机制的「引擎指针 + 清单自有规则」成立：指针链可解析（2/2：`feedback-utils.py --action record` 动作、`knowledge-promotion.md` 作为知识记录义务 owner 存在）；晋升程序与通用判据由清单「逐步积累机制」节唯一声明（A-22）；[[STR-001]] 标记在机制声明中在场；第二机制的可判定读数 = 0：`scripts/python/` 下无 `best-practices.py` / `best_practices.py` 引擎文件；文本层的第二机制声明由评审确认，守卫不以模糊文本扫描充数（A-16、FR-007(d)）。 **Path**: final
- **SC-004**: 分发与登记成立：`shared/definitions/framework-map.md` 与 `.specify/shared/definitions/framework-map.md` 各含恰一行同时带 `.specify/shared/best-practices/` 与 `Feature 111` 的登记行（2/2，A-19）；`sync-mirrors.py --check` 对本模块的源/镜像差集 = 空；init 既有 `shared/` 拷贝步骤覆盖新目录的证明记录在场（代码路径引用 + 既有 init 集成测试运行同一拷贝步骤 + 记录的只读初始化演练，按 A-18；不新增第二个测试文件），且 `src/` 改动行数 = 0。 **Path**: final
- **SC-005**: 适配与零残留：模块五文档中 `ai-harness` / `.ah/` / `/ah.` 出现数 = 0；模块引用的仓内路径存在率 = 100%；归属声明为 Feature 111。 **Path**: final
- **SC-006**: containment 成立：`git diff --name-only 0419adae5..HEAD` 的变更路径集 ⊆ FR-009 的声明集（集合外路径出现数 = 0；wrap-up 记账记录按 FR-009 / A-20 的残余判定程序——路径集差后仅三记账存储、记录体含特性 key 或 run id 者放行；后续特性登记阶段的注册表例外按 FR-009 判定）；引擎/模板/技能/代理/命令/宪法/指令/存储布局/决策治理面改动数 = 0。 **Path**: final
- **SC-007**: 测试证据成立：守卫经 `scripts/bash/run-tests.sh tests/contract/test_general_best_practices.py` 执行退出 0，且 red-first 记录（先红后绿）在场；镜像参数化套件相对入口基线零新增红；全量套件失败名集 ⊆ 入口基线（无 NEW）。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 守卫 `tests/contract/test_general_best_practices.py` 的 (a)(b)(f) 断言输出（含清单表格解析读数与顶层文件集读数）；`ls` / 文件树读数；空分类零条目的 (b) 断言输出。
- **SC-002 Source**: 守卫的 (c) 断言输出（对 [[STR-005]] 正文的三项文本断言 + 延伸 SSH 口径）。
- **SC-003 Source**: 守卫的 (d) 断言输出（指针解析 + `scripts/python/` 下的第二引擎文件缺席读数）；`feedback-utils.py --help` 的 `record` 动作在场读数；文本层第二机制声明由评审记录。
- **SC-004 Source**: 守卫的 (e) 断言输出；`python3 scripts/python/sync-mirrors.py --check` 逐字输出；`git diff --numstat 0419adae5..HEAD -- src/` 零行读数；init 证明三件证据（共享拷贝代码路径引用 + 既有 init 集成测试运行同一拷贝步骤 + `.specify/.tmp/` 内只读初始化演练读数，A-18）。
- **SC-005 Source**: 守卫内的残留扫描断言（三组字面量计数 = 0）；被引用路径的存在性断言输出。
- **SC-006 Source**: `git diff --name-only 0419adae5..HEAD` 与 FR-009 声明集的集合差（机器采集）；残余路径按 A-20 的记录体谓词程序判定；review 阶段复核一次。
- **SC-007 Source**: `scripts/bash/run-tests.sh` 的退出码与汇总输出；red-first 记录（`test-evidence/`）；全量套件失败名与入口基线的名字级集合差。

## Shared Strings

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "[best-practice]" | FR-004, FR-007, SC-003 |
| `STR-002` | "programming-languages.md" | FR-001, FR-002, FR-007, SC-001 |
| `STR-003` | "system-interfaces.md" | FR-001, FR-002, FR-007, SC-001 |
| `STR-004` | "programming-frameworks.md" | FR-001, FR-002, FR-007, SC-001 |
| `STR-005` | "programming-tools.md" | FR-001, FR-002, FR-003, FR-007, SC-001, SC-002 |
| `STR-006` | "尚无条目" | FR-002, FR-007, SC-001 |
| `STR-007` | "Git clone 的默认协议" | FR-003, FR-007, SC-002 |

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

### Session 2026-11-27（无人值守 clarify 阶段，自行裁决并记录）

- Q: 五文档范围与四分类封闭集如何变成机器可判定的形状？ → A: 模块顶层文件集恰五文档；清单唯一三列表恰四行、每行恰一相对链接、链接目标集合恰为四个 owner 文件，并含「封闭集」字面量（A-15；FR-001、FR-007(a)、SC-001）。
- Q: 条目形态与"尚无条目"占位如何钉住，守卫的可判定边界在哪？ → A: 条目 = `## ` 标题 + `**实践**` + `**反例 / 证据**`（可选 `**延伸**`；晋升条目另带 `**来源**`）；占位 ⇔ 零条目（互斥不变式）；守卫不冻结占位数量 3、不断言条目语义真伪；"编造条目充数"归积累纪律与评审（A-16；FR-002、FR-007(b)、SC-001、SC-003、Edge Cases）。
- Q: 晋升与回放（追溯）路径的形态是什么？ → A: 观察的 notes 写 [[STR-001]] + owner 文件 stem，不新增字段/动作/存储；晋升条目带 `**来源**`（feedback ID / ≥7 位 hex 提交号 / 会话原话之一）+ 通用判定依据；晋升不改写既有观察记录；种子豁免来源行，模块文本不编造 feedback ID（A-17；FR-003、FR-004、Key Entities）。
- Q: 分发、镜像与 init 证明的执行形态？ → A: 镜像同变更由 `sync-mirrors.py` 写模式再生成、`--check` 零漂移，字节一致唯一由既有镜像套件裁决；init 证明 = 代码路径引用 + 既有 init 集成测试运行同一拷贝步骤 + `.specify/.tmp/` 内只读初始化演练；不新增第二个测试文件（A-18；FR-006、SC-004）。
- Q: 框架地图登记行的可判定形态？ → A: 地图唯一布局表内、与 `.specify/shared/` 行相邻的三列一行；Where = `.specify/shared/best-practices/`，Notes 含 Feature 111、`README.md` 指针与 `(framework source: shared/best-practices/)`；源与镜像各恰一行（A-19；FR-005、FR-007(e)）。
- Q: containment 的残余路径如何判定，记账写入的边界在哪？ → A: 路径集差后，残余仅当落在三记账存储且记录体含特性 key 或 run id 时放行；只写 per-entry 文件，不改写聚合/索引，不触达 trigger/state（A-20；FR-009、SC-006）。
- Q: 词汇候选何时登记？ → A: 本规格定格提案文本（"best practice / 最佳实践"、"progressive accumulation / 渐进积累"）；本阶段不写 `.specify/glossary.md`；本线 containment 不含词表，线内登记须先修正 FR-009，否则线后另行登记（A-21；A-10 收敛）。

### Session 2026-11-27（analyze 轮次三阻断发现的修复裁定）

- Q: 晋升程序与通用判据归谁所有？ → A: 归**清单「逐步积累机制」节**所有；`knowledge-promotion.md` 只以指针承担知识记录义务与强调升级，`feedback-utils.py` 仍拥有记录形态、存储与处置（A-22；FR-004、A-17、C-104、C-302、C-305 同步改写）。
- Q: 观察落在哪个既有字段、ad-hoc 观察的 unit-id/run-id 如何合法？ → A: [[STR-001]] 标记与 owner 文件 stem 写入既有 `--review` 文本；有命令/技能运行时用该运行的 unit id 与 run id，无运行时用 `custom:best-practices/observation` + `--unit-type custom-unit` + `bp-<yyyy-mm-dd>-<slug>`，注册表工作区先经 probe 系统建立外部 probe（A-23、A-17）。
- Q: 守卫前导的镜像路径存在性断言与任务序如何两全？ → A: 在 US1 内容落地后、T008 绿点前插入 T007A（写模式镜像再生成）；C-404 前导断言不放宽，T012 仍作最终再生成收口（A-24）。