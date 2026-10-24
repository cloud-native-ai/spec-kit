# Implementation Plan: 执行/表达二元分类与文档型门禁（Execution/Expression Classes & Document-Form Gates）— Feature 069 / Slice 069a

**Branch**: `069-execution-expression-sdd` | **Date**: 2026-10-24 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `069a-flow-classification-docs-gates` → Feature 069 执行/表达二元分类与文档型 SDD 同构
**Input**: Specification from `.specify/specs/069a-flow-classification-docs-gates/requirements.md`（父权威：`.specify/specs/069-execution-expression-sdd/requirements.md`）

## Summary

本切片把「执行 / 表达」从散落的形容词变成**可解析、可对账、可读取、可门禁**的一等分类：
一份唯一所有者 `shared/definitions/flow-class-definitions.md`（判据 + 两取值 + 边界例 + 逐流程台账 + 类中立封闭清单 + 命名空间消歧），
一个解析引擎 `scripts/python/flow-class-check.py`（台账 ↔ 流程单元清单机械对账；按单元查类别，未声明返回默认类并带固定标记），
一份门禁算子集 owner `shared/workflow/expression-gates.md`（六面文档型门禁、逐阶段算子表、命令/技能调用点表、证据等级与 as-of 语法、三项基线协议），
一个事实一致性检查器 `scripts/python/doc-consistency-check.py`（读者声明 / 证据标注 / 跨文件手写副本三面；计数比对**委派**给既有 `pre-analyze-check.py`）。

技术路线 = **两个 owner 文档 + 两个 stdlib 引擎 + 最小指定接线**：类别只经 `flow-class-check.py --action lookup` 读取，
接线面**封闭**为 2 个命令模板（`/speckit.docs`、`/speckit.humanize`）与 2 个技能（`create-docs`、`humanize`）。
两入口的接线形态按各自复杂度类别分化：`/speckit.docs`（Complex）在命令模板内 lookup + owner 指针；
`/speckit.humanize`（**Simple**）命令模板只给 owner 指针、**不调用任何脚本**，类别读取与门禁执行落在其委派技能的 Stage 6 执行体（requirements SA-8）。
命令模板与技能 MUST NOT 出现类别字面量，MUST NOT 复制判据或算子表（算子集由门禁 owner 的调用点表拥有）。零新增 `/speckit.*` 命令；未刷新项目拿到的是旧命令副本与旧技能（无 lookup、无 owner、无引擎），
故**没有调用点、行为不变**；刷新后命令副本与 `shared/` + `scripts/` 由同一发行包一次到位，接线随之生效（`contracts/compatibility-distribution.md` § C-4）。
阶段集合、门禁数量与 P0/P1 定义一律不动——分类只换算子集，且阶段完整性判定不读类别。

## Technical Context

**Language/Version**: Python ≥ 3.8（两引擎 stdlib-only：`argparse` / `json` / `re` / `pathlib` / `subprocess` / `difflib` / `datetime`）；owner 文档为 Markdown
**Primary Dependencies**: 无新增第三方依赖；不引入 YAML/JSON 侧车数据文件（台账是 owner 内的 Markdown 表）
**Storage**: 无运行时存储。台账与判据在 owner 文档内；基线记录是**每特性一份**的 `<spec-dir>/notes/expression-baseline.md`（人工填写、随规格入库）；不新增项目侧存储
**Testing**: pytest（本机可用解释器 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest`；本仓 `.venv` **未安装** pytest——实测 `No module named pytest`，实现阶段不得假设 `python3 -m pytest` 可用）；测试基线名字级，见 § Test Strategy
**Target Platform**: Linux / macOS（POSIX；两引擎不依赖 shell 特性，Windows 仅在 git 缺失时降级 as-of 的 commit-date 规则）
**Project Type**: 框架源（`shared/`、`scripts/`）+ 运行时镜像（`.specify/`，由 `sync-mirrors.py` 投影）；无应用运行时
**Performance Goals**: `flow-class-check.py --action check` 在全量 78 个流程单元上单次 < 2 s（纯文本解析）；`doc-consistency-check.py` 在单特性产物集（≤ 30 个文件）上 < 3 s
**Constraints**: 零新增 `/speckit.*` 命令（父 A8）；命令模板与技能 MUST NOT 内嵌类别字面量（FR-015）；接线面封闭为 4 个既有文件、每处只加一个接线小节（W3 为两处同一句），且 `/speckit.humanize` 命令模板 MUST NOT 调用任何脚本（Simple 形态，复杂度判据 owner：`shared/workflow/feedback-step.md` 开篇；见 § Minimal Designated Wiring）；062 / 067 / 068 的 `requirements.md` 字节不变（FR-026 / SC-008）；结构面判据是「零**新增**违规」，因为结构基线已带 3 条既有违规（见 § Test Strategy）
**Scale/Scope**: 流程单元 78（命令 27 + 技能 51，实测）；六面门禁（封闭集，FR-018）；8 个 SDD 阶段的算子映射；4 个接线点；新增文件 = 2 份 owner 文档 + 2 个引擎 + 8 个测试文件（6 契约 + 2 单元）；修改既有文件 = 2 个命令模板 + 2 个技能 + `shared/workflow/feedback-step.md`（+1 行指针），以及由模板重新生成的每工具命令副本（生成物，不手改）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`；本运行无子代理派发工具，同作者评分按 `objective-analysis-gate.md` § 7 降级为直接有界复核——`scored: direct read, subagent unavailable`，见 research.md 抬头):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每个设计决策回指 FR：判据与台账（FR-001/002/005）、读取与降级（FR-009/015/016）、六面门禁（FR-018–FR-024）；contracts 四份逐条编号，feature-ref.md 给 FR→落点映射 |
| II | Feature-Centric Development | ✅ Pass | 复用既有 Feature 069（不新建、不新增注册行）；本阶段只 Draft → Planned；Feature list 复核零新增/零废弃（feature-ref.md § Feature list review） |
| III | Intent-Driven Development | ✅ Pass | requirements 的 what/why 已由 clarify 10 项裁定固定；本 plan 只把「怎么落」写成可解析结构，不重开语义 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 本切片含可执行代码（两个引擎 + 4 个接线点）→ 全量 Test-First（非 template-only Partial）：8 个测试文件先落红，契约四份与测试一一对应（feature-ref.md § Test Mapping） |
| V | AI Agent Integration Standards | ✅ Pass | 零触碰 agent roster / `AGENT_CONFIG`；命令副本不手改——改 2 个模板后由 `regen-command-copies.py` 重生成，`--check` 必须回绿（生成物按源模板单向下发，无手写副本） |
| VI | Continuous Quality & Observability | ✅ Pass | 两引擎输出结构化 JSON + 非零退出码；降级（未声明 / not-run / 缺 git / 引擎缺席）一律显式字段，不静默；接线点的降级同样产出可见标记（不静默切门禁集）；新行为写入 features 详情与 § Test Strategy |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Feature reuse-first 命中 069；状态只进不退（Draft → Planned）；成功判据逐条有测量源（feature-ref.md § SC → Measurement） |
| VIII | Code as the Single Source of Truth | ✅ Pass | 规模与基线全部为本次实跑：命令 27 / 技能 51 / 镜像全绿 / 结构违规 3 / 契约套件 4154 通过 31 失败；推断项均标注 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 零新命令、零守护进程、零数据库、零侧车数据文件；台账复用 owner 内 Markdown 表先例（027）；计数比对委派而非重写；接线面封闭为 4 个既有文件、每处一个接线小节（不做批量接线、不做按类自动分派引擎）；两引擎合计三个动作（`check` / `lookup` / `verify`） |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新文件全部小写 kebab（`flow-class-definitions.md`、`expression-gates.md`、`flow-class-check.py`、`doc-consistency-check.py`）；零新增保留名；`<域>-definitions.md` 沿用同目录惯例 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子已点名：改动落框架源 `shared/` + `scripts/` + `templates/commands/` + `skills/external/`，`.specify/` 只作镜像、每工具命令副本只作生成物；本切片的分类判据对自身适用（069a 自判 `execution`，见 research.md R12） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用既有件：`sync-mirrors.py`（镜像）、`pre-analyze-check.py`（计数比对，委派）、`exec-quant`/`run-determination`/`feedback-utils`（基线三量）、`validate-requirements.py`（需求面）；仅两个新引擎无既有覆盖 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Task Understanding（类别可查、缺口可报）与 Change Validation（文档型算子真正被入口执行，而非仅落文档）与 Reliable Delivery（接线最小、未刷新零变化）；不新增评分/成熟度报告 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 分类判据只在 owner；六面各指一个既有 owner，新增面才写新判据；两个引擎**不复制**门禁表（`lookup` 只返回类别，不回传算子表）；模板/技能只出现 owner 指针与各自被允许的调用形态（W1/W4 lookup、W2/W3 仅指针），不复制判据与算子表；计数规则委派 `pre-analyze-check.py`；`[[STR-NNN]]` 引用惯例沿用（字面量唯一落 requirements 表） |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 两引擎的 text 输出用功能语义 + 可行动路径；`--format json` 面向维护者基线读者；契约与 quickstart 对类别键（[[STR-003]]）与默认标记（[[STR-004]]）首现即释义 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 已执行的 in-passing 修复与前提偏差全部披露（脚手架误落父目录、`CWS_LIB_BASH_HOME` 缺失、`pytest` 不在本仓 `.venv`、契约基线既有 31 红）；每个门禁的降级都产出显式字段而非绿灯 |

**Gates Status**: ✅ 全部 16 原则 Pass，零 Fail / 零 Partial——无 Complexity Tracking 违例项。
过程性披露三件（非违例）：① 同作者评分门降级为直接复核（行上已标注）；② 实现前基线含**既有**红（契约套件 31 失败 / 4154 通过 / 5 跳过），判据是「按名字零新增失败」；③ 结构面基线 3 条既有违规，判据是「零新增」。

**Re-check after Phase 1**: 2026-10-24 复核完成——Phase 1 四类产物（data-model / contracts ×4 / quickstart / feature-ref）落盘后逐行重对照：II（状态推进落 features 两文件）、IV（契约条款 ↔ 测试清单一一对应）、XIV（委派与指针边界在契约 C 条款中固化）、XVI（降级字段在 checker 契约中对齐）证据行按产物实文更新，结论不变（16 Pass）。
**Re-check after wiring revision (2026-10-24)**: 「零改动」改为最小指定接线后重对照——IV（接线点各配契约测试 A1–A7）、V（副本走重生成）、IX（接线封闭 4 文件）、XI（改动面含模板与技能源）、XIII（门禁真正可执行）、XIV（模板只留 owner 指针，不复制判据/算子表；humanize 的读取在技能执行体）、XVI（降级可见），结论不变（16 Pass）。
**Re-check after checklist repair (2026-10-24)**: checklist 待处置项落盘后复核——IV（8 支测试，含分类正确性测试与变异断言）、IX（六面封闭、无扩面）、XIV（`STR-003` 由切片 Shared Strings 声明并标注父来源）、XVI（humanize 保持 Simple：命令模板零脚本调用，读取落技能 Stage 6），结论不变（16 Pass）。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/069a-flow-classification-docs-gates/
├── requirements.md      # 既有（本阶段零改动）
├── notes/
│   ├── parent-fr-mapping.md          # 既有（父/切片编号映射）
│   └── test-baseline-contract.txt    # 新增：契约套件名字级失败基线（实现期「零新增」判据的分母）
├── plan.md              # 本文件
├── research.md          # Phase 0 决策 R1–R14 与实测证据
├── data-model.md        # Phase 1：实体 E1–E10
├── contracts/           # Phase 1：4 份契约（台账 / 阶段算子 / 检查器 / 兼容分发）
├── quickstart.md        # Phase 1：6 个场景（route a/b 逐例标注）
├── feature-ref.md       # Phase 1：FR/SC → 设计落点 → 测试映射
├── tasks.md             # NOT created by /speckit.plan（/speckit.tasks 产出）
└── verification.md      # /speckit.implement 产出
```

### Source Code (repository root)

```text
shared/definitions/flow-class-definitions.md   # 新增：分类 owner（判据/取值/边界例/台账 78 行/类中立清单/命名空间/变更记录）
shared/workflow/expression-gates.md            # 新增：文档型门禁 owner（封闭六面 + 逐阶段算子表 + 调用点表 + 证据语法 + 三项基线协议）
shared/workflow/feedback-step.md               # 修改：+1 行正交声明指针（复杂度轴 ↔ 类别轴，不复述判据）
scripts/python/flow-class-check.py             # 新增：台账对账（check）+ 类别解析（lookup）
scripts/python/doc-consistency-check.py        # 新增：读者/证据/事实一致性三面检查（verify）
templates/commands/docs.md                     # 修改：+1 个接线小节（lookup 调用 + owner 指针；位于 ## Outline 内、分派之前）
templates/commands/humanize.md                 # 修改：+1 个接线小节（仅 owner 指针，不调用脚本；保持 Simple；位于 ## Outline 内、委派之前）
skills/external/create-docs/SKILL.md           # 修改：R6 verify 增补 checker 调用与 owner 指针（不复制规则）
skills/external/humanize/SKILL.md              # 修改：Stage 6 增补 lookup 调用 + 门禁 owner 指针（062 保真细则与默认输出不变）
tests/contract/test_flow_class_ledger.py       # 新增：台账完整性、反空真下限、lookup 语义、模板/技能零类别字面量
tests/contract/test_flow_class_correctness.py  # 新增：分类正确性（≥10 单元 oracle 比对 + 变异断言）
tests/contract/test_expression_gates_doc.py    # 新增：六面齐全、每面单一 owner 指针可解析、逐阶段算子表与调用点表完整
tests/contract/test_doc_consistency_checker.py # 新增：三面规则 + SC-007 注入演练夹具
tests/contract/test_expression_gate_wiring.py  # 新增：4 个接线点、副本重生成、接线封闭集、无类别字面量
tests/contract/test_expression_compatibility.py# 新增：062/067/068 字节不变、零新命令、零项目侧存储、接线面封闭
tests/unit/test_flow_class_check.py            # 新增：解析/归一化/退出码单测
tests/unit/test_doc_consistency_rules.py       # 新增：归一化、排除项、as-of 规则、委派降级单测
```

**Generated copies（不手改）**: 每工具命令副本 `.claude/commands/speckit.{docs,humanize}.md`、`.github/prompts/speckit.{docs,humanize}.prompt.md`、`.opencode/command/speckit.{docs,humanize}.md`、`.qoder/commands/speckit.{docs,humanize}.md` 由 `python3 scripts/python/regen-command-copies.py` 从两个源模板重生成；本切片 MUST NOT 手写这些副本。

**Structure Decision**: 本仓是**框架源 + 自身客户运行时**双身份。改动全部落框架源（`shared/`、`scripts/`、`templates/commands/`、`skills/external/`、`tests/`），
`.specify/` 下的同名文件是 `sync-mirrors.py` 的**受控投影**，不手改。既有表面只允许 4 个接线点（2 模板 + 2 技能）各加一个接线小节
（其中 `humanize.md` 只含 owner 指针、零脚本调用，保持 Simple），
外加 `shared/workflow/feedback-step.md` 的 +1 行指针；**不触碰** `src/specify_cli/`、`AGENTS.md` / `.specify/instructions.md`，
也不触碰其余 25 个命令模板与 49 个技能（接线封闭集，见 § Minimal Designated Wiring）。

### Mirror Obligations *(mandatory — 本切片触碰 `shared/`、`scripts/`、`skills/external/` 与 `templates/commands/`)*

**基线（2026-10-24 实跑，编辑前）**: `python3 scripts/python/sync-mirrors.py --check` → 六对全部 `ok`、命令副本 `OK`、exit 0。
因此本切片的判据是「**零新增漂移**」（不是"绝对全绿"——虽然基线此刻恰好全绿，判据仍按名字级差值写，避免后续无关漂移把判据打成不可通过）。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/flow-class-definitions.md` | `.specify/shared/definitions/flow-class-definitions.md` | `python3 scripts/python/sync-mirrors.py --write --only shared` 后 `--check`，与该对基线比较「零新增差异」 |
| `shared/workflow/expression-gates.md` | `.specify/shared/workflow/expression-gates.md` | 同上（同一对 `shared/`） |
| `shared/workflow/feedback-step.md` | `.specify/shared/workflow/feedback-step.md` | 同上；改的是 +1 行指针，镜像必须同字节 |
| `scripts/python/flow-class-check.py` | `.specify/scripts/python/flow-class-check.py` | `sync-mirrors.py --write --only scripts` 后 `--check`（`scripts` 对是 strict-extras：镜像侧多文件也会报） |
| `scripts/python/doc-consistency-check.py` | `.specify/scripts/python/doc-consistency-check.py` | 同上 |
| `skills/external/create-docs/SKILL.md` | `.specify/skills/create-docs/SKILL.md` | `sync-mirrors.py --write --only skills` 后 `--check`（该对 lenient 只对 extras，差异文件仍报） |
| `skills/external/humanize/SKILL.md` | `.specify/skills/humanize/SKILL.md` | 同上 |

**不产生镜像义务**的文件：`tests/**`（不入镜像）、`.specify/specs/**`（规格产物本身）。
**命令模板无镜像**：`templates` 对的 `commands` 子目录被排除（该镜像已于 2026-08-17 退役），故两个模板的投影目标是每工具命令副本。
**命令副本**: 改完 `templates/commands/docs.md` 与 `templates/commands/humanize.md` 后 MUST 运行 `python3 scripts/python/regen-command-copies.py`，
再以 `--check` 验证 `OK`（判据是「重生成后零漂移」，不是「模板未改动」）；副本属生成物，MUST NOT 手写。

## Complexity Tracking

> 无 Constitution Check 违例。**N/A**。

## Phase 0: Research Review

完整决策与证据见 [research.md](research.md)（R1–R14）。本阶段无需新的外部调研：全部未知项由仓内实测与 clarify 已裁定项解决。
关键结论摘要（**不复述判据**，只记录落点）：

- **所有者与读取路径**：判据/台账在 `shared/definitions/flow-class-definitions.md`；读取只经 `flow-class-check.py --action lookup`。
  台账 = owner 内 Markdown 表，一行一个流程单元；对账 = 与 `templates/commands/*.md` + `skills/{external,internal}/*/SKILL.md` 比对（实测 27 + 51 = 78）。
- **命名空间**：机器键 `[[STR-003]]`；`[[STR-001]]` 与 Agent Execution 同词异义，消歧落 owner § 命名空间 + 既有 glossary 两行。
- **门禁不变量**：阶段集合、门禁数量、P0/P1 定义、analyze/review 调用率 100% 全部**不读类别**；类别只选算子集。
- **六面落点**：四面复用既有 owner（`validate-requirements.py` / `user-facing-comprehension.md` + `create-docs` Authoring Flow / `docs-utils.py` / `one-source-of-truth.md` / 评审流程），两面新增（证据等级与 as-of、事实一致性检查器）；六面为**封闭集**（恰好 6，每面一个 face id，requirements SA-7）。
- **首批成员**：`/speckit.docs` 与 `/speckit.humanize` 登记进台账并做**最小接线**：docs 在命令模板加 lookup + owner 指针，`create-docs` 技能加 owner/checker 指针；humanize 的**命令模板只加 owner 指针**（保持 Simple），lookup 与门禁执行落在 `humanize` 技能的 Stage 6（requirements SA-8）。062 的表面断言与「不削弱既有行为」同时被保住：humanize 只引用门禁 owner，保真细则仍归 062 技能（见 § Minimal Designated Wiring）。
- **兼容与分发**：两份 owner 文档与两个引擎随 `shared/` + `scripts/` 经 `specify init` 到达；不新增项目侧存储。未刷新项目只有旧命令副本与旧技能（无 lookup、无 owner、无引擎）→ **没有调用点、行为不变**；刷新时命令副本与 `shared/` + `scripts/` 由同一发行包一次到位，接线生效；投影/刷新不完整时 lookup 失败即按默认类语义降级并报 `owner-unavailable`（`marker` 为 null，两标签互斥，不中断、不静默切门禁集）。

**No standalone requirement leftovers**: `requirements.md` 无 `[NEEDS CLARIFICATION]`；`pre-analyze-check.py --stage requirements` 实测 `decision=pass`（errors=0 / advisories=0 / fr=27 / sc=8）。advisories 一行是 requirements 阶段（设计产物落盘前）的值；设计产物落盘后同命令复测为 79 条 `missing-path` advisory（全部指向尚待创建的新文件），`decision` 仍为 `pass`（2026-10-24 checklist 阶段复测）。

## Phase 1: Design & Contracts

Phase 1 产物与边界（判据正文在各自 owner，本计划不复述）：

1. **数据模型** [data-model.md](data-model.md) — E1 流程单元、E2 分类登记行、E3 类中立条目、E4 门禁算子、E5 读者声明、E6 证据标注、E7 一致性发现、E8 基线记录、E9 类别解析结果、E10 门禁调用点。
2. **契约** [contracts/](contracts/) — 严格用 `**C-N**` 规范形态（避开 `contract-clause-definitions.md` 的 `md-none` 兜底问题）：
   - `flow-class-ledger.md`：所有者位置、台账行语法、完备性与反空真下限、互斥、默认与标记、类中立封闭、lookup 契约、**指定接线与接线封闭集（lookup 调用 / owner 指针 / 点名的 checker 调用三种形态；禁止类别字面量与判据副本）**、阶段不变量、变更审计。
   - `expression-gate-operators.md`：六面与单一 owner 指针、逐阶段算子表、**命令/技能调用点表（哪个入口、在什么阶段、执行哪些算子）**、阻断级别、读者声明形态、证据等级与 as-of 语法、构建非充分、事实唯一性与修复方向、评审读者基准、三项基线协议、算子去重规则。
   - `doc-consistency-checker.md`：CLI 面、三面规则（R1–R3 + 副本聚类）、排除项、计数委派与 `not-run` 降级、退出码、JSON 输出 schema、**调用点（docs 路径与 create-docs 技能 R6）**。
   - `compatibility-distribution.md`：零新命令、零项目侧存储、分发路径与**单包原子性**、**未刷新 = 旧副本无调用点 / 刷新 = 副本与 owner+引擎同时到位**、指定接线面封闭、镜像与命令副本判据、062/067/068 字节不变、测试基线口径。
3. **最小指定接线** — 见 § Minimal Designated Wiring（4 个接线点 + 封闭集 + 既有表面契约的硬约束）。
4. **Quickstart** [quickstart.md](quickstart.md) — 6 个场景，逐例标注 route (a) 已执行 / (b) 由契约测试钉住，并列出逐例前提；场景 4 覆盖接线的兼容与分发语义。
5. **Feature 绑定** [feature-ref.md](feature-ref.md) — FR/SC → 设计落点 → 契约条款 → 测试面；含接线点表、Feature list 复核与状态推进结论。

### Minimal Designated Wiring（本切片唯一的既有表面改动）

分类与门禁若不被任何入口读取，就只是文档与脚本。本切片因此在**封闭的 4 个接线点**上各加一个接线小节，使「可门禁」成立；**不扩到 069b**（不做同构映射、不做迁移机制、不做度量仪器）。

| # | 接线点（既有文件） | 位置（不得移动既有章节） | 增补内容（封闭清单） | 禁止 |
|---|--------------------|--------------------------|----------------------|------|
| W1 | `templates/commands/docs.md` | `## Outline` 内、`### 技能输入` 及其后的分派之前 | ① `flow-class-check.py --action lookup --unit-id "/speckit.docs"` 调用；② owner 指针（`shared/definitions/flow-class-definitions.md` + `shared/workflow/expression-gates.md`），并按门禁 owner 的 docs 调用点行执行文档型算子（含 `doc-consistency-check.py --action verify`） | 类别字面量；类别归属断言；判据副本；六面算子表的逐行复述；新增 `## ` 顶级章节 |
| W2 | `templates/commands/humanize.md` | `## Outline` 内、委派段之前 | **仅** owner 指针（分类 owner + 门禁 owner 各一条路径），并写明「类别读取与最小算子集执行由委派技能的 Stage 6 承担」（不点名该技能的 `SKILL.md` 路径——C-2 只允许一处技能提及） | lookup 或任何脚本调用（会把 Simple 变 Complex，违反复杂度判据 owner 与 `test_c01_thin_entry_shape`）；类别字面量；类别归属断言；判据/算子表副本；第二处 `SKILL.md` 提及；`## Wrap-up`；改写某条 062 行为 |
| W3 | `skills/external/create-docs/SKILL.md` | `### Reconcile Loop` 的 R6 verify 与 `### Authoring Flow` 的 R6 验证（两处同一句；`### Desired-State Baseline` 是结构/链接/构建面的既有 owner，接线不往该段加内容，以免把门禁规则混进基线） | owner 指针 + 「当调用方已解析为文档型算子集时，对受触文档执行 `doc-consistency-check.py --action verify`」；owner/引擎缺席时显式跳过 | 复制门禁规则；把 checker 变成无条件硬依赖（standalone 会破）；断言类别归属 |
| W4 | `skills/external/humanize/SKILL.md` | `### Stage 6 — 保真自检（交付前）` 段首（读取先于 Stage 6 各项自检） | ① `flow-class-check.py --action lookup --unit-id "/speckit.humanize"`（该流程**唯一**的类别读取，同一次运行只读一次）；② 一句 owner 指针：本技能参与的门禁算子集登记在门禁 owner 的 humanize 调用点，执行细则仍以本文件 Non-negotiables 与 Stage 6 为准；③ owner/引擎缺席时显式降级（`owner-unavailable` 或默认标记），不中断改写 | 复制算子表；断言类别归属；改变 062 的默认输出/报告契约；把 command 模板路径写回技能（C-2 方向）；在 Stage 6 之外新增读取点 |

**接线语义（W1 / W4 的读取形态；W2 只声明归口）**

1. **先读数、后判定**：lookup 在**执行门禁的那个入口**内先于判定执行一次——`/speckit.docs` 在其命令模板分派前，`/speckit.humanize` 在其委派技能的 Stage 6 自检前。类别取值/判据/台账的唯一所有者是分类 owner，门禁算子集的唯一所有者是门禁 owner——模板与技能只给调用与指针。
2. **按 owner 的调用点行执行**：入口不自行列举算子；它加载门禁 owner 的调用点表，执行该入口登记的行（docs = 六面文档型算子；humanize = 最小集）。
3. **降级可见**：lookup 返回 `source: default`（未登记）时原样显示 `marker`（未声明·按默认）；owner 不可解析或脚本缺席（退出码 2）时显示 `owner-unavailable` 且 `marker` 为 null（两标签互斥），**保持既有门禁不变**、不中断流程、不静默切换门禁集（FR-009 / FR-016）。
4. **命令模板不因接线改变复杂度类别**：`/speckit.humanize` 的模板 MUST NOT 出现任何脚本调用；`/speckit.docs` 保持 Complex（已有脚本/产物消费面），lookup 不放宽也不收紧其门禁。

**既有表面契约的硬约束（实现期必须遵守，违反即已有测试转红）**

| 约束 | 来源（既有测试/契约） |
|------|----------------------|
| `docs.md` 的 `## ` 顶级章节序列不得变（接线只能用 `###`） | `tests/contract/test_docs_command_template.py::test_c3_section_order` |
| `humanize.md` 中 `SKILL.md` 只可出现一次（接线文字不得再提技能路径） | `tests/contract/test_humanize_command_surface.py::test_c02_single_skill_delegation` |
| `humanize.md` 非表格行数 ≤ 120（`test_c01` 断言的是**非表格行条数**，当前 40 条）且不得含行为细则关键词（`rubric` / `评审记录` / `评分表` / `盲评`） | 同上 `test_c01_thin_entry_shape` |
| `humanize.md` 不得出现 `## Wrap-up` / `feedback-utils.py` / `probe-utils.py`（Simple 形态） | 同上 `test_c01_thin_entry_shape` |
| `humanize.md` 的接线 MUST NOT 出现任何脚本调用（`flow-class-check.py` / `--action lookup` / 其他引擎名）——命令调用脚本即 Complex，会与其 Simple 形态冲突 | `shared/workflow/feedback-step.md` 开篇（复杂度判据 owner）+ `test_c01_thin_entry_shape` |
| `create-docs`/`humanize` 的技能源与 `.specify/skills/` 镜像必须同字节 | `tests/contract/test_docs_command_template.py::test_c12_skill_source_mirror_byte_identity` |
| `scripts/**` 的 `.py` 不得出现 `humanize` 字样（含注释与示例；`conftest.py` 例外） | `tests/contract/test_humanize_command_surface.py::test_c08_no_runtime_surface` |
| 062 的保真底线、输入解析与默认零写入行为不得改写 | `.specify/specs/062-humanize-command/requirements.md`（字节不变，FR-026 / SC-008） |

**Non-goals（明确不做）**: 不做其余 25 个模板 / 49 个技能的任何接线；不做按类别自动分派引擎；不新增 `/speckit.*` 命令；不改判定阈值、阶段集合或 P0/P1；不引入项目侧注册表或迁移步骤；不把同构映射（069b）预置进调用点表。

## Test Strategy

**Tests Mode**: ON（本切片含可执行运行时脚本，非 template-only）。

**名字级基线（实测，2026-10-24）**

| 层 | 命令 | 基线 |
|----|------|------|
| 采集面 | `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest --collect-only -q tests` | `5361 tests collected`（exit 0） |
| 契约面 | `pytest tests/contract -q --tb=no` | `4154 passed, 31 failed, 5 skipped`（201.9 s）；失败名单冻结在 `notes/test-baseline-contract.txt` |
| 静态交叉核对 | AST 统计 `test_*.py` | 文件 307 / 顶层 `test_*` 函数 2915；`tests/contract/` 189 文件 / 1974 函数（参数化使 collected 大于函数数，两数并存防用错分母） |
| 镜像面 | `python3 scripts/python/sync-mirrors.py --check` | 六对 `ok` + 命令副本 `OK`（exit 0） |
| 结构面 | `python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .` | exit 0，`violations=3`（`broken-link` 2 + `note-frontmatter` 1）——**非零基线** |
| 需求面 | `python3 scripts/python/validate-requirements.py <slice>/requirements.md` | `status: ok`，5 项检查全 pass，0 error / 0 warning |

**判据（全部写成名字级差值，不写绝对绿）**
- 新增测试必须先在既有代码上**红**（引擎/owner/接线尚不存在），再随实现转绿。
- 契约与单元套件：与 `notes/test-baseline-contract.txt` 比对，**零新增失败名字**；既有 31 红不因本切片修复或掩盖（属他特性的登记债）。
- 结构面：`violations` **零新增**（计数与 kind 集合都不得增长）。
- 镜像面：`--check` 零新增差异；命令副本在 `regen-command-copies.py` 重生成后 `--check` 为 `OK`，且副本正文含接线（防「只改模板、未重生成」假绿）。

**接线契约测试（`test_expression_gate_wiring.py` 必须断言的面）**

| # | 断言 | 机械判据 |
|---|------|----------|
| A1 | W1 模板含 lookup 与 owner 指针 | `templates/commands/docs.md` 的接线小节内含 `flow-class-check.py`、`--action lookup`、`"/speckit.docs"`、`flow-class-definitions.md`、`expression-gates.md`、`doc-consistency-check.py`；该小节位于 `## Outline` 之后、`## Wrap-up` 之前 |
| A2 | W2 模板只含 owner 指针、**无脚本调用** | `templates/commands/humanize.md` 的接线小节内含 `flow-class-definitions.md` 与 `expression-gates.md`；**不得**出现 `flow-class-check.py`、`--action lookup`、`--unit-id`、`doc-consistency-check.py`、`feedback-utils.py`、`probe-utils.py` 任一；全文不得出现第二处 `SKILL.md`、不得出现 `## Wrap-up`；非表格行数 ≤ 120（Simple 形态不变） |
| A3 | W3/W4 技能含门禁 owner 引用（W4 另含 lookup） | `skills/external/create-docs/SKILL.md` 含 `expression-gates.md` 与 `doc-consistency-check.py`；`skills/external/humanize/SKILL.md` 含 `expression-gates.md`、`flow-class-check.py`、`--action lookup`、`"/speckit.humanize"`，且 `Stage 6 — 保真自检` 段落与 `diff_protected.py` 引用原样保留 |
| A4 | 无类别字面量与归属断言 | 接线文本（含 owner 指针的最小段落/小节）内，先剔除 `expression-gates` 这一 owner 路径后，不得出现独立词 `expression` / `execution`，也不得出现「本单元属某类」的归属断言（取值字面量与中文类名都算）；全文不得出现类别键赋值形态（正则 `flow_class\s*[:=]`，键名为 `[[STR-003]]` 的固定副本）；不得出现「unit id ‖ 类别取值」的台账样式行 |
| A5 | 接线封闭 | 其余 25 个 `templates/commands/*.md` 与其余 49 个 `skills/{external,internal}/*/SKILL.md` 均不含 `flow-class-check.py` / `expression-gates.md` / `doc-consistency-check.py` 引用 |
| A6 | 生成副本已重生成 | `.claude/commands`、`.github/prompts`、`.opencode/command`、`.qoder/commands` 下共 8 个副本：docs 副本各含 `flow-class-check.py` 与 `expression-gates.md`；humanize 副本各含 `flow-class-definitions.md` 与 `expression-gates.md` 且不含 `flow-class-check.py`（与其源模板一致，证明重生成发生而非手写） |
| A7 | 前序规格字节不变 | 062 / 067 / 068 `requirements.md` 的 sha256 与冻结值一致（与 `test_expression_compatibility.py` 同源断言，不重复定义哈希算法） |

**新增测试清单（8 个文件：6 契约 + 2 单元）**

| 文件 | 断言面 | 对应契约 |
|------|--------|----------|
| `tests/contract/test_flow_class_ledger.py` | 台账行数 ≥ 78、每行取值合法、`/speckit.docs` 与 `/speckit.humanize` 为表达类首成员、未声明单元 lookup 返回默认类 + 标记、模板/技能零类别字面量、类中立清单封闭、接线封闭集 | `flow-class-ledger.md` C-1…C-15 |
| `tests/contract/test_flow_class_correctness.py` | **分类正确性**（不是结构在场）：固定 fixture ≥10 个流程单元（两类 ≥3 / 未声明 ≥1 / 类中立 ≥1 / 混合 oracle ≥1），逐单元断言 lookup 的类别键（[[STR-003]]） / `source` / `basis` / `marker` 与 oracle 相符；变异断言——把 fixture 中一个单元的类别改错后重跑，比对 MUST 转红（证明该测试能证伪） | `flow-class-ledger.md` C-7 + `requirements.md` FR-006 / SC-001 |
| `tests/contract/test_expression_gates_doc.py` | 六面**恰好 6** 且每面恰一个 face id 与一个可解析 `owner_pointer`、逐阶段算子表覆盖 8 阶段、调用点表覆盖 W1–W4、humanize 行为最小集且非六面整套、无"分类可省阶段"表述、证据三值 + `source` 必填 + ISO as-of 语法、三项基线协议在场 | `expression-gate-operators.md` C-1…C-15 |
| `tests/contract/test_doc_consistency_checker.py` | 三面规则在夹具上红/绿、SC-007 三类注入各被报出一次、排除项不误报、计数委派 `not-run` 显式 | `doc-consistency-checker.md` C-1…C-10 |
| `tests/contract/test_expression_gate_wiring.py` | 上表 A1–A7（接线点存在、位置正确、humanize 模板零脚本调用、无类别字面量、接线封闭、副本已重生成、前序规格字节不变） | `flow-class-ledger.md` C-9/C-15 + `expression-gate-operators.md` C-14 + `compatibility-distribution.md` C-4/C-5 |
| `tests/contract/test_expression_compatibility.py` | 062/067/068 `requirements.md` 内容哈希不变、`templates/commands/` 文件集不变（数量与名字集合）、接线面外零改动、无新增项目侧存储路径、`.specify/` 无手写差异 | `compatibility-distribution.md` C-1…C-10 |
| `tests/unit/test_flow_class_check.py` / `tests/unit/test_doc_consistency_rules.py` | 解析、归一化、排除、退出码、降级分支 | 同上两份契约的实现细则 |

## Phase 1: Design Artifacts Summary

（按 create-plan § Summarize after, not before：以下数量在产物落盘后回填。）

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [data-model.md](data-model.md) | 10 实体（E1–E10；E10 = 门禁调用点） |
| Contracts | [contracts/](contracts/) | 4 份：`flow-class-ledger.md`、`expression-gate-operators.md`、`doc-consistency-checker.md`、`compatibility-distribution.md` |
| Quickstart | [quickstart.md](quickstart.md) | 6 场景（逐例标注 route a 已执行 / route b 契约钉住；场景 4 覆盖接线的兼容与分发） |
| Feature reference | [feature-ref.md](feature-ref.md) | FR 27 条 → 落点映射 + 接线点表 + SC 8 条 → 测量源 + Feature list 复核 |
| Research | [research.md](research.md) | 14 项决策（R1–R14；R4/R10 已随接线修订） |
| Baseline record | `notes/test-baseline-contract.txt` | 契约套件失败名单（名字级，逐行一个 nodeid） |
