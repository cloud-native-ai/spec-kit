# Implementation Plan: 执行/表达二元分类与文档型门禁（Execution/Expression Classes & Document-Form Gates）— Feature 069 / Slice 069a

**Branch**: `069-execution-expression-sdd` | **Date**: 2026-10-24 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `069a-flow-classification-docs-gates` → Feature 069 执行/表达二元分类与文档型 SDD 同构
**Input**: Specification from `.specify/specs/069a-flow-classification-docs-gates/requirements.md`（父权威：`.specify/specs/069-execution-expression-sdd/requirements.md`）

## Summary

本切片把「执行 / 表达」从散落的形容词变成**可解析、可对账、可读取、可门禁**的一等分类：
一份唯一所有者 `shared/definitions/flow-class-definitions.md`（判据 + 两取值 + 边界例 + 逐流程台账 + 类中立封闭清单 + 命名空间消歧），
一个解析引擎 `scripts/python/flow-class-check.py`（台账 ↔ 流程单元清单机械对账；按单元查类别，未声明返回默认类并带固定标记），
一份门禁算子集 owner `shared/workflow/expression-gates.md`（六面文档型门禁、逐阶段算子表、证据等级与 as-of 语法、三项基线协议），
一个事实一致性检查器 `scripts/python/doc-consistency-check.py`（读者声明 / 证据标注 / 跨文件手写副本三面；计数比对**委派**给既有 `pre-analyze-check.py`）。

技术路线 = **两个 owner 文档 + 两个 stdlib 引擎 + 零命令、零技能、零模板改动**：类别只由引擎读取，命令模板与技能内不得出现类别字面量；
未刷新的客户项目没有任何调用点，行为因此零变化。阶段集合、门禁数量与 P0/P1 定义一律不动——分类只换算子集，且阶段完整性判定不读类别。

## Technical Context

**Language/Version**: Python ≥ 3.8（两引擎 stdlib-only：`argparse` / `json` / `re` / `pathlib` / `subprocess` / `difflib` / `datetime`）；owner 文档为 Markdown
**Primary Dependencies**: 无新增第三方依赖；不引入 YAML/JSON 侧车数据文件（台账是 owner 内的 Markdown 表）
**Storage**: 无运行时存储。台账与判据在 owner 文档内；基线记录是**每特性一份**的 `<spec-dir>/notes/expression-baseline.md`（人工填写、随规格入库）；不新增项目侧存储
**Testing**: pytest（本机可用解释器 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest`；本仓 `.venv` **未安装** pytest——实测 `No module named pytest`，实现阶段不得假设 `python3 -m pytest` 可用）；测试基线名字级，见 § Test Strategy
**Target Platform**: Linux / macOS（POSIX；两引擎不依赖 shell 特性，Windows 仅在 git 缺失时降级 as-of 的 commit-date 规则）
**Project Type**: 框架源（`shared/`、`scripts/`）+ 运行时镜像（`.specify/`，由 `sync-mirrors.py` 投影）；无应用运行时
**Performance Goals**: `flow-class-check.py --action check` 在全量 78 个流程单元上单次 < 2 s（纯文本解析）；`doc-consistency-check.py` 在单特性产物集（≤ 30 个文件）上 < 3 s
**Constraints**: 零新增 `/speckit.*` 命令（父 A8）；命令模板与技能 MUST NOT 内嵌类别字面量（FR-015）；062 / 067 / 068 的 `requirements.md` 字节不变（FR-026 / SC-008）；结构面判据是「零**新增**违规」，因为结构基线已带 3 条既有违规（见 § Test Strategy）
**Scale/Scope**: 流程单元 78（命令 27 + 技能 51，实测）；六面门禁；8 个 SDD 阶段的算子映射；新增文件 = 2 份 owner 文档 + 2 个引擎 + 5 支测试

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`；本运行无子代理派发工具，同作者评分按 `objective-analysis-gate.md` § 7 降级为直接有界复核——`scored: direct read, subagent unavailable`，见 research.md 抬头):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每个设计决策回指 FR：判据与台账（FR-001/002/005）、读取与降级（FR-009/015/016）、六面门禁（FR-018–FR-024）；contracts 四份逐条编号，feature-ref.md 给 FR→落点映射 |
| II | Feature-Centric Development | ✅ Pass | 复用既有 Feature 069（不新建、不新增注册行）；本阶段只 Draft → Planned；Feature list 复核零新增/零废弃（feature-ref.md § Feature list review） |
| III | Intent-Driven Development | ✅ Pass | requirements 的 what/why 已由 clarify 10 项裁定固定；本 plan 只把「怎么落」写成可解析结构，不重开语义 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 本切片含可执行代码（两个引擎）→ 全量 Test-First（非 template-only Partial）：5 支测试先落红，契约四份与测试一一对应（feature-ref.md § Test Mapping） |
| V | AI Agent Integration Standards | ✅ Pass | 零触碰 agent roster / `AGENT_CONFIG` / 每工具命令副本（不改模板 → `regen-command-copies.py --check` 天然绿） |
| VI | Continuous Quality & Observability | ✅ Pass | 两引擎输出结构化 JSON + 非零退出码；降级（未声明 / not-run / 缺 git）一律显式字段，不静默；新行为写入 features 详情与 § Test Strategy |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Feature reuse-first 命中 069；状态只进不退（Draft → Planned）；成功判据逐条有测量源（feature-ref.md § SC → Measurement） |
| VIII | Code as the Single Source of Truth | ✅ Pass | 规模与基线全部为本次实跑：命令 27 / 技能 51 / 镜像全绿 / 结构违规 3 / 契约套件 4154 通过 31 失败；推断项均标注 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 零新命令、零守护进程、零数据库、零侧车数据文件；台账复用 owner 内 Markdown 表先例（027）；计数比对委派而非重写；两引擎合计两个动作面 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新文件全部小写 kebab（`flow-class-definitions.md`、`expression-gates.md`、`flow-class-check.py`、`doc-consistency-check.py`）；零新增保留名；`<域>-definitions.md` 沿用同目录惯例 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子已点名：改动落框架源 `shared/` + `scripts/`，`.specify/` 只作镜像；本切片的分类判据对自身适用（069a 自判 `execution`，见 research.md R12） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用既有件：`sync-mirrors.py`（镜像）、`pre-analyze-check.py`（计数比对，委派）、`exec-quant`/`run-determination`/`feedback-utils`（基线三量）、`validate-requirements.py`（需求面）；仅两个新引擎无既有覆盖 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Task Understanding（类别可查、缺口可报）与 Change Validation（文档型算子）与 Reliable Delivery（零模板改动、未刷新零变化）；不新增评分/成熟度报告 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 分类判据只在 owner；六面各指一个既有 owner，新增面才写新判据；两个引擎**不复制**门禁表（`lookup` 只返回类别，不回传算子表）；计数规则委派 `pre-analyze-check.py`；`[[STR-NNN]]` 引用惯例沿用（字面量唯一落 requirements 表） |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 两引擎的 text 输出用功能语义 + 可行动路径；`--format json` 面向维护者基线读者；契约与 quickstart 对 `flow_class` / `未声明·按默认` 首现即释义 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 已执行的 in-passing 修复与前提偏差全部披露（脚手架误落父目录、`CWS_LIB_BASH_HOME` 缺失、`pytest` 不在本仓 `.venv`、契约基线既有 31 红）；每个门禁的降级都产出显式字段而非绿灯 |

**Gates Status**: ✅ 全部 16 原则 Pass，零 Fail / 零 Partial——无 Complexity Tracking 违例项。
过程性披露三件（非违例）：① 同作者评分门降级为直接复核（行上已标注）；② 实现前基线含**既有**红（契约套件 31 失败 / 4154 通过 / 5 跳过），判据是「按名字零新增失败」；③ 结构面基线 3 条既有违规，判据是「零新增」。

**Re-check after Phase 1**: 2026-10-24 复核完成——Phase 1 四类产物（data-model / contracts ×4 / quickstart / feature-ref）落盘后逐行重对照：II（状态推进落 features 两文件）、IV（契约条款 ↔ 测试清单一一对应）、XIV（委派与指针边界在契约 C 条款中固化）、XVI（降级字段在 checker 契约中对齐）证据行按产物实文更新，结论不变（16 Pass）。

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
├── data-model.md        # Phase 1：实体 E1–E9
├── contracts/           # Phase 1：4 份契约（台账 / 阶段算子 / 检查器 / 兼容分发）
├── quickstart.md        # Phase 1：6 个场景（route a/b 逐例标注）
├── feature-ref.md       # Phase 1：FR/SC → 设计落点 → 测试映射
├── tasks.md             # NOT created by /speckit.plan（/speckit.tasks 产出）
└── verification.md      # /speckit.implement 产出
```

### Source Code (repository root)

```text
shared/definitions/flow-class-definitions.md   # 新增：分类 owner（判据/取值/边界例/台账 78 行/类中立清单/命名空间/变更记录）
shared/workflow/expression-gates.md            # 新增：文档型门禁 owner（六面 + 逐阶段算子表 + 证据语法 + 三项基线协议）
shared/workflow/feedback-step.md               # 修改：+1 行正交声明指针（复杂度轴 ↔ 类别轴，不复述判据）
scripts/python/flow-class-check.py             # 新增：台账对账（check）+ 类别解析（lookup）
scripts/python/doc-consistency-check.py        # 新增：读者/证据/事实一致性三面检查（verify）
tests/contract/test_flow_class_ledger.py       # 新增：台账完整性、反空真下限、lookup 语义、模板零字面量
tests/contract/test_expression_gates_doc.py    # 新增：六面齐全、每面单一 owner 指针可解析、逐阶段算子表完整
tests/contract/test_doc_consistency_checker.py # 新增：三面规则 + SC-007 注入演练夹具
tests/contract/test_expression_compatibility.py# 新增：062/067/068 字节不变、零新命令、零项目侧存储
tests/unit/test_flow_class_check.py            # 新增：解析/归一化/退出码单测
tests/unit/test_doc_consistency_rules.py       # 新增：归一化、排除项、as-of 规则、委派降级单测
```

**Structure Decision**: 本仓是**框架源 + 自身客户运行时**双身份。改动全部落框架源（`shared/`、`scripts/`、`tests/`），
`.specify/` 下的同名文件是 `sync-mirrors.py` 的**受控投影**，不手改。**不触碰** `templates/commands/`、
`skills/`、`src/specify_cli/`、`AGENTS.md` / `.specify/instructions.md`，因此每工具命令副本与指令符号链接零变更。

### Mirror Obligations *(mandatory — 本切片触碰 `shared/` 与 `scripts/`)*

**基线（2026-10-24 实跑，编辑前）**: `python3 scripts/python/sync-mirrors.py --check` → 六对全部 `ok`、命令副本 `OK`、exit 0。
因此本切片的判据是「**零新增漂移**」（不是"绝对全绿"——虽然基线此刻恰好全绿，判据仍按名字级差值写，避免后续无关漂移把判据打成不可通过）。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/flow-class-definitions.md` | `.specify/shared/definitions/flow-class-definitions.md` | `python3 scripts/python/sync-mirrors.py --write --only shared` 后 `--check`，与该对基线比较「零新增差异」 |
| `shared/workflow/expression-gates.md` | `.specify/shared/workflow/expression-gates.md` | 同上（同一对 `shared/`） |
| `shared/workflow/feedback-step.md` | `.specify/shared/workflow/feedback-step.md` | 同上；改的是 +1 行指针，镜像必须同字节 |
| `scripts/python/flow-class-check.py` | `.specify/scripts/python/flow-class-check.py` | `sync-mirrors.py --write --only scripts` 后 `--check`（`scripts` 对是 strict-extras：镜像侧多文件也会报） |
| `scripts/python/doc-consistency-check.py` | `.specify/scripts/python/doc-consistency-check.py` | 同上 |

**不产生镜像义务**的文件：`tests/**`（不入镜像）、`templates/commands/**`（本切片不改）、`.specify/specs/**`（规格产物本身）。
**命令副本**: 因零模板改动，`python3 scripts/python/regen-command-copies.py --check` 必须保持 `OK`（现状实测 `OK`）。

## Complexity Tracking

> 无 Constitution Check 违例。**N/A**。

## Phase 0: Research Review

完整决策与证据见 [research.md](research.md)（R1–R14）。本阶段无需新的外部调研：全部未知项由仓内实测与 clarify 已裁定项解决。
关键结论摘要（**不复述判据**，只记录落点）：

- **所有者与读取路径**：判据/台账在 `shared/definitions/flow-class-definitions.md`；读取只经 `flow-class-check.py --action lookup`。
  台账 = owner 内 Markdown 表，一行一个流程单元；对账 = 与 `templates/commands/*.md` + `skills/{external,internal}/*/SKILL.md` 比对（实测 27 + 51 = 78）。
- **命名空间**：机器键 `flow_class`；`execution` 与 Agent Execution 同词异义，消歧落 owner § 命名空间 + 既有 glossary 两行。
- **门禁不变量**：阶段集合、门禁数量、P0/P1 定义、analyze/review 调用率 100% 全部**不读类别**；类别只选算子集。
- **六面落点**：四面复用既有 owner（`validate-requirements.py` / `user-facing-comprehension.md` + `create-docs` Authoring Flow / `docs-utils.py` / `one-source-of-truth.md` / 评审流程），两面新增（证据等级与 as-of、事实一致性检查器）。
- **首批成员**：`/speckit.docs` 与 `/speckit.humanize` 登记进台账；**不改**两者的模板/技能（062 表面断言与「不削弱既有行为」同时被保住）。
- **兼容与分发**：随 `shared/` + `scripts/` 经 `specify init` 到达；不新增项目侧存储；未刷新项目无调用点 → 行为不变。

**No standalone requirement leftovers**: `requirements.md` 无 `[NEEDS CLARIFICATION]`；`pre-analyze-check.py --stage requirements` 实测 `decision=pass`（errors=0 / advisories=0 / fr=27 / sc=8）。

## Phase 1: Design & Contracts

Phase 1 产物与边界（判据正文在各自 owner，本计划不复述）：

1. **数据模型** [data-model.md](data-model.md) — E1 流程单元、E2 分类登记行、E3 类中立条目、E4 门禁算子、E5 读者声明、E6 证据标注、E7 一致性发现、E8 基线记录、E9 类别解析结果。
2. **契约** [contracts/](contracts/) — 严格用 `**C-N**` 规范形态（避开 `contract-clause-definitions.md` 的 `md-none` 兜底问题）：
   - `flow-class-ledger.md`：所有者位置、台账行语法、完备性与反空真下限、互斥、默认与标记、类中立封闭、lookup 契约、模板零字面量、阶段不变量、变更审计。
   - `expression-gate-operators.md`：六面与单一 owner 指针、逐阶段算子表、阻断级别、读者声明形态、证据等级与 as-of 语法、构建非充分、事实唯一性与修复方向、评审读者基准、三项基线协议、算子去重规则。
   - `doc-consistency-checker.md`：CLI 面、三面规则（R1–R3 + 副本聚类）、排除项、计数委派与 `not-run` 降级、退出码、JSON 输出 schema。
   - `compatibility-distribution.md`：零新命令、零项目侧存储、分发路径、镜像与命令副本判据、062/067/068 字节不变、测试基线口径。
3. **Quickstart** [quickstart.md](quickstart.md) — 6 个场景，逐例标注 route (a) 已执行 / (b) 由契约测试钉住，并列出逐例前提。
4. **Feature 绑定** [feature-ref.md](feature-ref.md) — FR/SC → 设计落点 → 契约条款 → 测试面；含 Feature list 复核与状态推进结论。

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
- 新增测试必须先在既有代码上**红**（引擎/owner 尚不存在），再随实现转绿。
- 契约与单元套件：与 `notes/test-baseline-contract.txt` 比对，**零新增失败名字**；既有 31 红不因本切片修复或掩盖（属他特性的登记债）。
- 结构面：`violations` **零新增**（计数与 kind 集合都不得增长）。
- 镜像面：`--check` 零新增差异；命令副本保持 `OK`。

**新增测试清单（5 支）**

| 文件 | 断言面 | 对应契约 |
|------|--------|----------|
| `tests/contract/test_flow_class_ledger.py` | 台账行数 ≥ 78、每行取值合法、`/speckit.docs` 与 `/speckit.humanize` 为 `expression`、未声明单元 lookup 返回默认类 + 标记、模板/技能零类别字面量、类中立清单封闭 | `flow-class-ledger.md` C-1…C-10 |
| `tests/contract/test_expression_gates_doc.py` | 六面齐全且各指一个可解析 owner 路径、逐阶段表覆盖 8 阶段、无"分类可省阶段"表述、证据三值与 ISO as-of 语法、三项基线协议在场 | `expression-gate-operators.md` C-1…C-11 |
| `tests/contract/test_doc_consistency_checker.py` | 三面规则在夹具上红/绿、SC-007 三类注入各被报出一次、排除项不误报、计数委派 `not-run` 显式 | `doc-consistency-checker.md` C-1…C-9 |
| `tests/contract/test_expression_compatibility.py` | 062/067/068 `requirements.md` 内容哈希不变、`templates/commands/` 文件集不变、无新增项目侧存储路径、`.specify/` 无手写差异 | `compatibility-distribution.md` C-1…C-7 |
| `tests/unit/test_flow_class_check.py` / `tests/unit/test_doc_consistency_rules.py` | 解析、归一化、排除、退出码、降级分支 | 同上两份契约的实现细则 |

## Phase 1: Design Artifacts Summary

（按 create-plan § Summarize after, not before：以下数量在产物落盘后回填。）

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [data-model.md](data-model.md) | 9 实体（E1–E9） |
| Contracts | [contracts/](contracts/) | 4 份：`flow-class-ledger.md`、`expression-gate-operators.md`、`doc-consistency-checker.md`、`compatibility-distribution.md` |
| Quickstart | [quickstart.md](quickstart.md) | 6 场景（route a ×3 / route b ×3） |
| Feature reference | [feature-ref.md](feature-ref.md) | FR 27 条 → 落点映射 + SC 8 条 → 测量源 + Feature list 复核 |
| Research | [research.md](research.md) | 14 项决策（R1–R14） |
| Baseline record | `notes/test-baseline-contract.txt` | 契约套件失败名单（名字级，逐行一个 nodeid） |
