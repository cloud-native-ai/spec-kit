# Implementation Plan: 同构映射、迁移兼容与度量仪器（Isomorphism Map, Migration Compatibility & Measurement Instruments）— Feature 069 / Slice 069b

**Branch**: `069b-isomorphism-migration-metrics` | **Date**: 2026-10-25 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `069b-isomorphism-migration-metrics` → Feature 069 执行/表达二元分类与文档型 SDD 同构
**Input**: Specification from `.specify/specs/069b-isomorphism-migration-metrics/requirements.md`（父权威：`.specify/specs/069-execution-expression-sdd/requirements.md`；分解门记录：父目录 `notes/decomposition-gate.md`）

## Summary

本切片把 069a 留下的三处交接落成可核对的结构，并且**只增量**：

1. **同构映射与边界进唯一所有者**：在 `shared/definitions/flow-class-definitions.md` 新增
   `## 同构映射（8 阶段 × 3 面）`（6 列表 × 8 行，中间三格即 24 格，每格写成 `代码型：… ↔ 文档型：…`；
   每行带 `强制门禁` + `强制状态` 两列）与 `## 不可同构边界`（a–d 四行，每条必须绑到一个封闭 face id）。
   阶段行集从既有名册 owner（`loop-state.py` 的 `STAGE_ARTIFACTS`）解析，**不新建第二份名册**；判据正文不复制。
2. **一个引擎的三条新动作 + 一次增量扩展**：`scripts/python/flow-class-check.py` 新增 `--action isomorphism` /
   `--action delegation` / `--action faces`，并扩展 `--action check`（解析侧反空真下限、覆盖率断言、`red_kind`
   区分「缺口」与「解析失败」）。`--action lookup` 与既有 8 个 finding kind 零改动。
3. **迁移与度量只声明与冻结，不新增机制**：未刷新项目无调用点（新动作不是调用点）；刷新走既有
   `shared/` + `scripts/` 随包与 `specify init`；三个未刷新客户项目快照事先冻结，判据是失败 nodeid 集合的
   `comm -13` 为空；三项基线只用 exec-quant / feedback / run-determination / git author date，无样本记 `not-evaluated`。

技术路线 = **2 处 owner 文档增量 + 1 个 stdlib 引擎（3 新动作 + 2 个 JSON 字段组）+ 4 份契约 + 8 个测试文件 + 3 份 dated 记录**。
零新增 `/speckit.*` 命令、零新增门禁面、零项目侧存储、零新采集器、零模板/技能改动。

## Technical Context

**Language/Version**: Python ≥ 3.8（引擎 stdlib-only：`argparse` / `json` / `re` / `pathlib` / `datetime`）；owner 文档为 Markdown
**Primary Dependencies**: 无新增第三方依赖；不引入 YAML/JSON 侧车数据（映射与台账都是 owner 内的 Markdown 表）
**Storage**: 无运行时存储。基线记录与迁移样本是本 spec 的 `notes/` dated 记录（每特性一份），不是项目侧存储
**Testing**: pytest（本机解释器 `/Users/liuqiming.lqm/project/profiles/.venv/bin/python`；本仓 `.venv` 未装 pytest——实测），
名字级基线经 `bash scripts/bash/run-tests.sh --names-out <file> ...` 采集
**Target Platform**: Linux / macOS（POSIX；引擎不依赖 shell 特性、不读环境变量决定判定）
**Project Type**: 框架源（`shared/`、`scripts/`、`tests/`）+ 运行时镜像（`.specify/`，由 `sync-mirrors.py` 投影）；无应用运行时
**Performance Goals**: `--action isomorphism` / `faces` / `delegation` 在 78 个流程单元 + 8 行映射 + 6 面绑定上单次 < 2 s（纯文本解析）；
`check` 的增量字段不引入第二次扫描
**Constraints**: 不改 069a 的任何规格与判据正文；不改 `templates/commands/` 与 `skills/`（零调用点、零命令副本改动）；
新动作只在**框架源仓**运行，载荷根给具名 `framework-source-required`；不新增项目侧存储或读取点；不新增采集器
**Scale/Scope**: 修改既有文件 2 个（owner 文档、引擎）；新增文件 = 4 份契约 + 8 个测试 + 3 份 notes；契约条款 4 份；
quickstart 7 个场景；无新增命令、无新增门禁面

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**（rendered from `.specify/memory/constitution.md`，按 `### <numeral>. <name>` 出现顺序；
本运行无子代理派发工具，同作者评分按 `.specify/shared/workflow/objective-analysis-gate.md` § 7 降级为直接有界复核——
`scored: direct read, subagent unavailable`，见 research.md 抬头）：

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每个设计决策回指 FR：映射（FR-001–005）、迁移（FR-006–008）、落地与度量（FR-009–014）；四份契约逐条编号，feature-ref.md 给 FR→落点→测试三段映射 |
| II | Feature-Centric Development | ✅ Pass | 复用 Feature 069（不新建、不新增注册行）；本阶段状态保持 `Planned`（069a Implemented / 069b plan 落盘），不写 `Implemented`；feature-ref.md § Feature list review 零新增/零废弃 |
| III | Intent-Driven Development | ✅ Pass | requirements 的 what/why 已由切片 clarify 记录与父规格固定；本 plan 只把「怎么落」写成可解析结构（表形、kind、`red_kind`、记录字段），不重开语义 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 本切片含可执行代码（引擎扩展）→ 全量 Test-First：8 个测试文件先红（红形态 = 动作/章节缺失），契约四份与测试一一对应（feature-ref.md § 4） |
| V | AI Agent Integration Standards | ✅ Pass | 零触碰 agent roster / `AGENT_CONFIG`；零模板改动 ⇒ 命令副本零重生成；镜像只投影 `shared/` 与 `scripts/` 两对 |
| VI | Continuous Quality & Observability | ✅ Pass | 引擎输出结构化 JSON + 非零退出码；五种 `red_kind` 显式（含 `framework-source-required`），无静默绿；基线记录写明「不可计部分」而不是记 0 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Feature reuse-first 命中 069；状态只进不退（`Planned` 保持）；每条 SC 有测量源（feature-ref.md § 2） |
| VIII | Code as the Single Source of Truth | ✅ Pass | 规模与基线全部为本次实跑：流程单元 78、阶段算子 16 行、六面 6 行、契约套件基线冻结于 `notes/test-baseline-contract.txt`、镜像六对全绿；推断项（如客户快照套件可运行性）标注为待实现期实测 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 零新命令、零新门禁面、零守护进程、零数据库、零侧车数据；映射放既有 owner 而非新文档；复用既有 duplicate 面与既有度量通道；引擎只加三个动作与两个 JSON 字段组 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新文件全部小写 kebab（`test_isomorphism_map.py`、`expression-baseline.md`、`migration-samples.md`）；零新增保留名；`<域>-definitions.md` 与 `notes/` 惯例沿用 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子已点名：改动落框架源（`shared/` + `scripts/` + `tests/`），`.specify/` 只作镜像；切片自判 `execution`（映射有人读面 → mixed-oracle，按 SA-7 仍取 `execution` 并叠加表达类门禁） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 `flow-class-check.py`（扩展而非新引擎）、`doc-consistency-check.py` 的 duplicate 面（判据副本计数）、`sync-mirrors.py`、`run-tests.sh --names-out`、`exec-quant` / `feedback-utils` / `run-determination` / git；仅一个引擎增量无既有覆盖 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Task Understanding（映射可逐行核对、边界可指认）、Change Validation（标注失真与解析失败各自转红）、Reliable Delivery（未刷新零变化、刷新单包原子）；不新增评分/成熟度报告 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 映射与边界进分类 owner；六面绑定仍归门禁 owner；引擎不复制判据/算子表（只读三元组与指针）；计数由制品导出；`[[STR-NNN]]` 引用沿用，字面量唯一表仍在父规格 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 契约与 quickstart 对 `red_kind` / `not-evaluated` / `framework-source-required` 首现即释义；引擎 text 输出给功能语义与可行动路径；`not-evaluated` 与 SC 状态词的差异在两处契约中写明 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 已披露的既有异常：`expression-gates.md § 事实一致性` 的 owner↔owner 重复（REC-069a-11，本切片只把它排除出主体集并写明理由）；owner 文档三处指针偏差（P1–P4）登记为实现期动作；`--action check` 在载荷根必然红的既有缺陷（REC-069a-06）以具名作用域收敛 |

**Gates Status**: ✅ 16 条原则全部 Pass，零 Fail / 零 Partial——无 Complexity Tracking 违例项。

过程性披露（非违例）：① 同作者评分门降级为直接复核；② 本切片对**既有**缺陷只做「作用域/口径」收敛，不修 069a 的判据正文
（REC-069a-11 / REC-069a-14 仍开放，理由见 research R10 / R11）；③ 客户快照的套件可运行性属实现期实测，plan 只冻结样本与判据形态。

**Re-check after Phase 1**: 2026-10-25 复核完成——Phase 1 四类产物（data-model / contracts ×4 / quickstart / feature-ref）落盘后逐行重对照：
II（状态保持 `Planned`，只追加切片记录）、IV（14 条 FR ↔ 契约引用组 ↔ 8 个测试面一一对应）、
IX（2 个源文件 + 8 个测试，无新引擎/新命令）、XIV（判据只在两个 owner、引擎只读结构）、
XVI（既有异常全部披露且划出作用域），结论不变（16 Pass）。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/069b-isomorphism-migration-metrics/
├── requirements.md                 # 既有（本阶段零改动）
├── notes/
│   ├── parent-fr-mapping.md        # 既有（父/切片编号映射）
│   ├── test-baseline-contract.txt  # 新增：框架仓契约套件名字级基线（FR-007 的分母）
│   ├── expression-baseline.md      # 新增：三项基线冻结记录（FR-014）
│   └── migration-samples.md        # 新增：3 个客户快照事先冻结（SA-12 / SC-002）
├── plan.md                         # 本文件
├── research.md                     # Phase 0：R1–R15 与实测证据
├── data-model.md                   # Phase 1：实体 E1–E10
├── contracts/                      # Phase 1：4 份契约
├── quickstart.md                   # Phase 1：7 个场景（逐例标注 route a/b）
├── feature-ref.md                  # Phase 1：FR/SC → 落点 → 契约 → 测试
├── tasks.md                        # NOT created by /speckit.plan（/speckit.tasks 产出）
└── verification.md                 # /speckit.implement 产出
```

### Source Code (repository root)

```text
shared/definitions/flow-class-definitions.md   # 修改：+同构映射 +不可同构边界 +台账版本声明 +P1–P4 指针收敛
scripts/python/flow-class-check.py             # 修改：check 增量（floor/coverage/red_kind）+ isomorphism/delegation/faces 三动作
tests/contract/test_isomorphism_map.py         # 新增：表形/24 格/强制标注真实性/四类边界/口号行/载体唯一
tests/contract/test_ledger_reconciliation.py   # 新增：反空真下限/覆盖率断言/两种红可区分/混合 oracle/版本声明
tests/contract/test_delegation_classes.py      # 新增：模板解析的委托边、类一致、类中立豁免、无人工清单
tests/contract/test_expression_faces.py        # 新增：六面 6/6、指针可解析、第二绑定表、判据副本 0
tests/contract/test_migration_distribution.py  # 新增：零调用点、零模板/技能改动、分发路径、快照记录、零项目侧存储
tests/contract/test_measurement_instruments.py # 新增：基线记录字段、四通道、无新采集器、SC 词表边界
tests/unit/test_isomorphism_checker.py         # 新增：名册解析/格语法/blocking 集合/作用域分支
tests/unit/test_reconciler_extensions.py       # 新增：red_kind 优先级/coverage 数学/委托语法/指针拆分
```

**结构决策**: 本仓是**框架源 + 自身客户运行时**双身份。改动只落框架源；`.specify/` 下同名文件是 `sync-mirrors.py`
的受控投影，不手改。**本切片不改 `templates/commands/` 与 `skills/`**，因此命令副本与技能镜像零改动；
既有表面零接线（新动作不是调用点）。唯一需要人工同步的是 `shared/` 与 `scripts/` 两对镜像。

### Mirror Obligations *(mandatory — 本切片触碰 `shared/` 与 `scripts/`)*

**基线（2026-10-25 实跑，编辑前）**: `python3 scripts/python/sync-mirrors.py --check` → 六对全部 `ok` + 命令副本 `OK`，exit 0。
因此判据写成「**零新增漂移**」（不是"绝对全绿"——虽然此刻恰好全绿，仍按名字级差值写，避免无关漂移把判据打成不可通过）。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/flow-class-definitions.md` | `.specify/shared/definitions/flow-class-definitions.md` | `python3 scripts/python/sync-mirrors.py --write --only shared` 后 `--check`，与该对基线比较「零新增差异」 |
| `scripts/python/flow-class-check.py` | `.specify/scripts/python/flow-class-check.py` | `python3 scripts/python/sync-mirrors.py --write --only scripts` 后 `--check`（`scripts` 对是 strict-extras，镜像侧多文件也会报） |

**不产生镜像义务**：`tests/**`（不入镜像）、`.specify/specs/**`（规格产物本身）。
**命令副本零改动**：`templates/commands/` 未被触碰，故 `regen-command-copies.py --check` 应继续 `OK`；若它变化，说明有人改了模板。

## Complexity Tracking

> 无 Constitution Check 违例。**N/A**。

## Phase 0: Research Review

完整决策与证据见 [research.md](research.md)（R1–R15）。本阶段无需新的外部调研：全部未知项由仓内实测与 requirements 已裁定项解决。
关键结论摘要（**不复述判据**，只记录落点）：

- **载体**：映射 + 边界进 `flow-class-definitions.md`，闭合 069a 第 19 行交接；不新建文档（R1）。
- **表形**：6 列 × 8 行，中间三格即 24 格；阶段集合从 `STAGE_ARTIFACTS` 解析，不建第二份名册（R2）。
- **强制标注**：`已强制` / `已声明未强制` 的**真实性**由 `(阶段, face)` 的 blocking 算子存在性判定（实测 8 个阶段都有 blocking ⇒ 交付表 8 行均 `已强制`；该取值由 fixture 覆盖，不空转）（R4）。
- **边界**：a–d 四行，每条 `门禁处理` 必含封闭 face id（R5）。
- **版本承载**：文档版本 + 既有变更记录，不加行级列、不加 `version` 字段（R6）。
- **对账扩展**：`ledger-truncated` + `coverage` + `red_kind`；既有 8 个 kind 与退出码阶梯不变（R7）。
- **委托核验**：模板路径解析 → `skill:<name>`；类中立豁免取封闭清单（实测 26/27 模板有边、0 类不一致、6 条豁免）（R8）。
- **六面绑定**：一个 `owner_pointer` 格可含主机制 + 执行件（`+` 连接），仍算一个绑定（R9）。
- **判据副本**：复用 duplicate 面，主体集封闭（不含六个 owner），要求 findings = 0（R10）。
- **作用域**：新动作 + `check` 只在框架源仓运行；载荷根给 `framework-source-required`（R11）。
- **基线**：`gate_calls = 0` / `confirmations = 0 + 0` / `wall_clock = null` → 三项 `not-evaluated`（R12）。
- **快照**：三个未刷新客户项目 + archive 临时副本 + `--names-out` 名字集（R13）。
- **既有措辞偏差**：P1–P4 登记为四行指针收敛，实现期随镜像同步（R15）。

**No standalone requirement leftovers**: `requirements.md` 无 `[NEEDS CLARIFICATION]`；`pre-analyze-check.py --stage requirements`
实测 `decision=pass`（errors=0 / advisories=0），`validate-requirements.py` 实测 `status: ok`（五项全 pass，0 error / 0 warning）。

## Phase 1: Design & Contracts

### 1) 同构映射载体（回答「映射写在哪、长什么样、怎么算被强制」）

**载体**：`shared/definitions/flow-class-definitions.md` 的两个二级章节。开篇 owns 列表加两项；`不在本文件` 表删除第 19 行交接项
（由实体章节取代）。MUST NOT 出现第二份映射（契约 C-1）。

**表结构（8 行 × 3 面 = 24 格）**：

| 阶段 | 结构（实体 / 关系 / 边界） | 流程（阶段与门禁角色） | 逻辑（证据 / 契约 / 验收 / 版本 / 所有权） | 强制门禁 | 强制状态 |
| --- | --- | --- | --- | --- | --- |
| requirements / clarify / plan / tasks / checklist / analyze / implement / review（8 行，行首格逐字取自名册） | `代码型：… ↔ 文档型：…` | 同左 | 同左 | 封闭 face id（`已强制` 时 ≥ 1） | `已强制` \| `已声明未强制` |

- **每行强制门禁或标注**：`强制状态` 取封闭两值；`已强制` ⟹ 点名的每个 `(阶段, face)` 在门禁 owner § 阶段算子表里是 `blocking`；
  `已声明未强制` ⟹ 该阶段没有任何 blocking 算子行。失真分别记 `annotation-false-enforced` / `annotation-false-unenforced`；
  既无门禁又无标注 = `slogan-row`（契约 C-4…C-7）。
- **实测基线**：阶段算子表 16 行；8 个阶段各有 ≥1 blocking（`implement` 为 1 blocking + 1 advisory）。因此交付的 8 行都将是 `已强制`；
  `已声明未强制` 是合法取值但不空转——由 fixture（造一个无 blocking 算子的阶段）覆盖。
- **阶段名册引用**：行集等于 `loop-state.py` `STAGE_ARTIFACTS` 的键集；名册变更映射跟走，不另立版本（契约 C-2）。066 的 FR 编号 006 是名册声明的来源。
- **不可同构边界（同文档四行）**：`a` 验收 oracle / `b` 验证算子 / `c` 失败可见性 / `d` 语义 oracle 缺失；
  `门禁处理` 必含封闭 face id（例如 (a) → `review`、(b) → `structure-links-build` + `fact-consistency`、
  (c) → `evidence-asof` + `review`、(d) → `review` + `reader-purpose`）。契约 C-8 / C-9。
- **不复制 069a 判据**：映射只引用 § 判据、两个取值与六面名；引擎只读 `(stage, face, blocking)` 三元组与 face id，
  不复制算子文本（契约 C-14，data-model E6）。

### 2) 迁移与兼容（回答「旧项目为什么不变、刷新为什么原子、零回归怎么测」）

| 状态 | 命令副本 | 技能 | `.specify/shared/` | `.specify/scripts/` | 行为 |
|------|----------|------|--------------------|---------------------|------|
| 未刷新 | 旧 | 旧 | 无映射章节 | 无新动作 | **无调用点**，与分类引入前逐字一致 |
| 已刷新 | 新（内容同旧，因本切片不改模板） | 旧（本切片不改技能） | 有映射 + 边界 + 版本声明 | 有 `check` 增量与三动作 | 映射可逐行核对；`lookup` 不变；新动作只在框架源仓运行 |
| 刷新不完整（异常态） | 新 | — | 缺 owner | — | `lookup` → `owner-unavailable`；新动作 → 不可解析退出 2；MUST NOT 静默切门禁集 |

- **零新调用点**：`check` / `delegation` / `faces` / `isomorphism` 不登记进 `expression-gates.md` § 调用点表，
  不进任何命令模板/技能；调用点表四个 W 行零改动（契约 C-3）。
- **分发**：四类载荷同一个发行包——`pyproject.toml` 第 34 行 `scripts`、第 37 行 `shared` 的 force-include，
  `src/specify_cli/__init__.py` 第 2462 行起的 shared 复制段；不新增机制（契约 C-5）。
- **零回归**：三个未刷新客户快照（`notes/migration-samples.md`）用 `git archive <HEAD>` 建临时副本，
  刷新前后各跑一次套件并采 `--names-out`，`comm -13` MUST 为空；MUST NOT 用条数比对；框架仓基线不替代客户快照（契约 C-6/C-7/C-9）。
- **零项目侧存储/读取点**：无新路径、无缓存、无注册表；项目自建流程按默认类运行，其自身知识空间里的类别记录框架不读（契约 C-4）。

### 3) 度量仪器（回答「三项基线用什么取数、数据长什么样、没有样本怎么记」）

| 量 | 仪器（既有通道） | 可执行命令 | 数据形态 | 本切片冻结值 / 判据 |
|----|------------------|------------|----------|----------------------|
| `gate_calls` | exec-quant 运行记录（068 通道） | `python3 scripts/python/exec-quant.py --action list-records --since 2026-10-24 --format json`，按冻结的 6 个检查类 `unit_id` 过滤，并按 `run_id` 含 `069b` 归属 | 记录对象：`unit_id` / `unit_type` / `run_id` / `collected_at` / `schema_version` | `0` → `not-evaluated`（分母 0） |
| `confirmations` | feedback 条目 frontmatter | `python3 scripts/python/feedback-utils.py --action list --since 2026-10-24 --format json` + 逐条查 `lifecycle_point: gate-*`；clarify 轮次 = 该切片是否有 clarify 运行记录，无则 0 | 条目对象：`id` / `unit_id` / `run_id` / `created`（+ 文件内 `lifecycle_point`） | `0 + 0` → `not-evaluated` |
| `wall_clock` | git author date → 运行判定记录 | `git log -1 --format=%as -- <requirements.md>`；`python3 scripts/python/run-determination.py --action history --target /speckit.analyze --json` | 起点 `YYYY-MM-DD`；终点记录含 `determined_at` / `run_id` | 起点 `2026-10-24`，终点 `null` → `not-evaluated` |

- **无新采集器**：四项命令全部既有；脚本级检查（`pre-analyze-check` / `validate-*` / 测试）不可按次计数——写入「不可计部分」，不记 0（契约 C-2/C-3）。
- **语汇边界**：`not-evaluated` 是判据取值；`verification.md` 的 SC 状态仍取 `pass/fail/partial/deferred/unknown`（契约 C-7）。
- **记录形态**：`notes/expression-baseline.md` 每行 `quantity / frozen_value / frozen_at / frozen_commit / instrument / source_command / verdict`
  （data-model E9）。本切片 5 条 SC 都不是效率降幅判据——基线是给后续同类切片用的可比前值。

### 4) 测试与契约

**契约**（[contracts/](contracts/)，全部用规范形态 `- **C-N**`，块尾一个引用组）：

| 契约 | 条款数 | 覆盖 |
|------|--------|------|
| `isomorphism-map.md` | 14（C-1…C-14） | 载体唯一、表形与行集、24 格格语法、强制状态取值、两种失真、口号行、四类边界、边界绑面、主张落地、禁止整套移植、介质无关、检查器行为、既有判定不改写 |
| `ledger-reconciler.md` | 16（C-1…C-16） | 解析侧下限、覆盖率断言、`red_kind` 与两种红可区分、kind 封闭扩展与 069a 兼容、版本声明、列头沿用、混合 oracle 一致性、委托语法、禁止人工清单、类中立封闭、六面绑定、第二绑定表、判据副本计数、作用域、只读确定性、测试面 |
| `migration-distribution.md` | 11（C-1…C-11） | 未刷新行为、刷新原子、零调用点、零项目侧存储、分发实测、快照冻结、名字级比对、刷新程序与降级、框架基线不替代客户快照、镜像判据、零新命令/零新门禁面 |
| `measurement-instruments.md` | 10（C-1…C-10） | 三项量与冻结点、仪器封闭、过滤集合冻结、确认口径、墙钟口径、`not-evaluated`、SC 词表边界、记录形态、收尾同口径、禁止新统计系统 |

**引用组覆盖**：14 条 FR 全部出现在至少一个条款的块尾引用组内（FR-001–005 → 契约一；FR-006–008 → 契约三；
FR-009–013 → 契约二；FR-014 → 契约四）；5 条 SC 也都在引用组内出现。条款正文只引用 FR/SC 编号，不复述其语义。

**与 069a 测试兼容**（实现期硬约束）：

| 既有断言 | 为什么本切片的扩展不会破它 |
|----------|---------------------------|
| `tests/unit/test_flow_class_check.py` 的「8 个 kind」集合与 `set(kinds) == {"row-malformed"}` | 行级夹具在注入坏行时仍保留 78 条可解析行，`ledger-truncated` 不触发 |
| 同文件 `test_inventory_truncated_below_*` | 这些夹具的 `templates/commands/` **存在但数量不足**，仍走 `inventory-truncated`；`framework-source-required` 只在两棵源树都缺席时触发 |
| `tests/contract/test_flow_class_ledger.py` 的「78 units / 零 findings / 载体唯一」 | 新增章节不产生第二份台账行；表头与列集合不变 |
| `tests/unit/test_flow_class_check.py` 的退出码阶梯（0/1/2） | 新字段是增量；`owner-unavailable` 仍是唯一「无 findings 的退出 2」分支，新增的 `framework-source-required` 只在载荷根触发 |

**新增测试清单（8 个文件：6 契约 + 2 单元）** 见 feature-ref.md § 4。

### 5) 交付物与状态

- `plan.md` / `research.md` / `data-model.md` / `contracts/`（4 份）/ `quickstart.md` / `feature-ref.md` / `notes/`（3 份 dated 记录）落盘。
- **Feature 069 保持 `Planned`**：`069a = Implemented`、`069b = plan 已落盘`；本阶段 MUST NOT 写 `Implemented`。
  登记更新只落 `features/069.md` 的 Related Specifications / Status Tracking 与索引行 Last Updated，不改状态列。
- 不创建 `tasks.md` / `verification.md`（分别归 `/speckit.tasks` 与 `/speckit.implement`）。

## Test Strategy

**Tests Mode**: ON（本切片含可执行代码：引擎扩展）。

**名字级基线（2026-10-25 实跑，编辑前）**

| 层 | 命令 | 基线 |
|----|------|------|
| 采集/契约面 | `SPECKIT_PYTHON=<external venv python> bash scripts/bash/run-tests.sh --names-out <file> tests/contract -q --tb=no -p no:cacheprovider` | 失败 nodeid 名单冻结在 `notes/test-baseline-contract.txt`（**计数与名单的唯一所有者**；本文件不重述数字） |
| 台账面 | `python3 scripts/python/flow-class-check.py --action check --format json` | `units = 78`、`findings = []`、exit 0（实测） |
| 镜像面 | `python3 scripts/python/sync-mirrors.py --check` | 六对 `ok` + 命令副本 `OK`（exit 0，实测） |
| 结构面 | `python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .` | exit 0，`violations = 3`（非零基线，判据为「零新增」） |
| 需求面 | `python3 scripts/python/validate-requirements.py <slice>/requirements.md` | `status: ok`，五项全 pass，0 error / 0 warning（实测） |
| 计划面 | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir <slice> --stage plan --repo .` | 见 § 门禁实跑；判据 = `errors = 0` |

**判据（全部名字级差值，不写绝对绿）**
- 新增测试先红：实现前 `flow-class-check.py` 没有 `isomorphism` / `delegation` / `faces` 三个动作、owner 文档没有两章节；
  红 MUST 表现为「动作/章节缺失」而不是 import/collection error。
- 契约与单元套件：与 `notes/test-baseline-contract.txt` 比对，**零新增失败名字**；既有红不因本切片修复或掩盖。
- 结构面：`violations` 零新增（计数与 kind 集合都不得增长）。
- 镜像面：`--check` 零新增差异；命令副本继续 `OK`（证明模板未被改）。
- 台账面：`check` 在本仓继续 78 units / 零 finding；`lookup` 的四个降级分支行为不变。

**门禁实跑（本阶段）**

```text
python3 scripts/python/validate-requirements.py .specify/specs/069b-isomorphism-migration-metrics/requirements.md
  → status: ok；五项 pass；0 error / 0 warning

python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py \
  --spec-dir .specify/specs/069b-isomorphism-migration-metrics --stage plan --repo .
  → 见「Phase 1 Artifacts Summary」后的实跑记录（errors=0）
```

## Phase 1: Design Artifacts Summary

（按 create-plan § Summarize after, not before：以下数量在产物落盘后回填。）

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [data-model.md](data-model.md) | 10 实体（E1–E10） |
| Contracts | [contracts/](contracts/) | 4 份：`isomorphism-map.md` / `ledger-reconciler.md` / `migration-distribution.md` / `measurement-instruments.md`；条款 51 条（14 + 16 + 11 + 10） |
| Quickstart | [quickstart.md](quickstart.md) | 7 场景（逐例标注 route a / route b） |
| Feature reference | [feature-ref.md](feature-ref.md) | 14 条 FR → 落点 → 契约 → 测试；5 条 SC → 测量源；Feature list 复核 |
| Research | [research.md](research.md) | 15 项决策（R1–R15） |
| Baseline records | `notes/expression-baseline.md` / `notes/migration-samples.md` / `notes/test-baseline-contract.txt` | 三项基线 / 三个快照 / 名字级失败名单 |
