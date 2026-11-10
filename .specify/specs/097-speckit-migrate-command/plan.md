# Implementation Plan: /speckit.migrate 一次性迁移收尾命令

**Branch**: `097-speckit-migrate-command` | **Date**: 2026-11-10 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `097-speckit-migrate-command` → Feature 024 Specification Workspace Versioning
**Input**: Specification from `.specify/specs/097-speckit-migrate-command/requirements.md`

## Summary

新增 `specify migrate` 子命令与 `/speckit.migrate` 运行期模板，把「install → init → migrate」第三步做成一次性收尾：以**当前已安装版本**的声明与资产为期望态，对 `.specify/` 工作区做只读五维探测（维度 token 与语义 owner：`data-model.md` E-8 / requirements FR-007，本计划不复述清单），产出逐项差异计划（默认零写入干跑），经双键确认后按 FR-014 六值处置收敛，凡移动/替换/移除一律 archive-not-delete 并留下逐运行回执。跨版本为一次直达（N→N+k，无中间版本步骤）；失败语义按 FR-017 为前向续跑 + 逐项归档找回，不提供全局回滚。

技术路线是**组合既有引擎，不做第二套迁移逻辑**：客户端工作区的期望态由 init 的同一复制机制投影到临时参照树（`copy_local_templates` + `rewrite_paths` + `generate_commands`）；五维探测分别消费 `sanitize-utils.py` 的只读检查器（链接/残留/平铺重复）、`anchor-layout-migrate.py` 的 check/apply（锚点布局）、`sync-mirrors.py --check` 与 `regen-command-copies.py --check`（框架源工作区的镜像与生成副本）、init 的 `cleanup_obsolete_framework_assets` / `migrate_flat_internal_skills` 决策（退役与平铺收敛）。`/speckit.sanitize` 保持周期性治理定位，其 Migration lane 声明在同一变更内改为「周期复检兜底」。

关键取舍见 § Decision Tensions（T-001 参照树投影、T-002 框架源双模式）；复用边界与不可复制清单见 `contracts/migrate-engine.md`；完整调查读数见 `research.md`。

## Technical Context

**Language/Version**: Python `>=3.8`（沿用 `pyproject.toml` 的 `requires-python`）；本特性零新增第三方依赖。
**Primary Dependencies**: `typer`（既有 CLI 框架）；引擎侧为标准库 + 仓库内既有脚本（`sanitize-utils.py`、`anchor-layout-migrate.py`、`sync-mirrors.py`、`regen-command-copies.py`）。
**Storage**: 纯文件系统——回执 `.specify/memory/migrate/receipts/<run-id>.json`（逐运行一文一件）；归档 `.specify/archive/migrate/<run-id>/<相对路径>`；无数据库、无索引文件。
**Testing**: `pytest`，唯一入口 `bash scripts/bash/run-tests.sh`（默认并行 `-n <effective> --dist load`）；新增 contract / integration / unit 三组测试，夹具在 `tmp_path` 内现场生成。
**Target Platform**: 支持符号链接的 Linux/macOS CLI 环境为主；无符号链接平台按降级事实报告（`refuse`），不崩溃。命令不依赖 git。
**Project Type**: 单包框架 CLI + 命令模板/技能分发（`src/specify_cli/`、`templates/commands/`、`skills/`）。
**Performance Goals**: 干跑全程零网络、零目标写入；参照树复制与工作区资产同量级，单次干跑在既有测试夹具（< 1000 文件）上 < 30 s；应用阶段每项处置最多一次归档写 + 一次目标写。
**Constraints**: 干跑绝对零写入（回执只走 stdout / `--format json`）；archive-not-delete；双键确认且**不提供**非交互确认旗标；未确认破坏项 `blocked`；不依赖 git；Python 3.8 语法兼容。
**Scale/Scope**: 1 个子命令（4 个选项）、1 个模板 + 4 份再生副本、1 个命令文档页、5 个探测维度、6 值处置域（引用 requirements FR-014）、1 个回执存储、14 个工作包。

## Constitution Check

**Core Principles Compliance** (rendered from `.specify/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每个 WP 与契约条款可回溯到 requirements FR-001…FR-025（`feature-ref.md` 的 FR→WP 矩阵） |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 024；本阶段同步 `features.md` 行与 `.specify/features/024-*.md`（Draft → Planned） |
| III | Intent-Driven Development | ✅ Pass | 不扩张范围：install/init 职责留在原入口（FR-004）、goal/team 迁移只留静止指针（FR-013） |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | `contracts/` 3 份契约 + WP 顺序把契约/夹具测试排在实现前（tasks 将逐行标 Red-first） |
| V | AI Agent Integration Standards | ✅ Pass | 不新增 agent；模板仅经既有 regen 分发到现行工具副本树，无新工具分支 |
| VI | Continuous Quality & Observability | ✅ Pass | 逐运行回执 + `test-evidence/` 实测记录 + Run Determination 读数 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 本工件集即 plan 阶段产物；tasks 由 `/speckit.tasks` 从本计划切分 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 期望态从已安装代码/资产读取（`research.md` R-2/R-6），不从文档或版本号猜测 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 1 个子命令 + 组合既有引擎；无新运行时、无新依赖、无新评分/登记系统 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 命令参考页落 `docs/reference/commands/migrate.md`；运行时落点全部在已登记 `.specify/` 根下 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 框架源编辑 → 镜像再生成（Mirror Obligations）；两个 hat 在结构与计划中显式区分 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用边界表（`contracts/migrate-engine.md` § C-5）逐项钉名 owner，禁止复制检查实现 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Controlled Execution / Reliable Delivery：blocked/refuse 可判定、归档可找回、回执可枚举 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 处置域引用 FR-014、期望态 owner 引用 FR-005 路径；契约不复述其清单 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 计划面/命令 help/回执文案按全局基准读者书写，术语走 `.specify/glossary.md` |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 冲突 `refuse` 指名双方、未确认 `blocked`、无静默跳过（契约不变量 I-4） |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | `.specify/memory/migrate/receipts/` 与 `.specify/archive/migrate/` 在同一变更登记（WP10） |
| XVIII | Grounded Naming | ✅ Pass | `specify migrate` / `/speckit.migrate` 名称来自 requirements STR-001/STR-002，贯穿全部落点 |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | 命令面只投影四类结局 + 六值处置，不增额外面；回执字段即用户审阅所需最小集 |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | 测试只经 `run-tests.sh` 运行；夹具用 `tmp_path` 隔离，可并行；不新增 runner 或慢速全局夹具 |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | `specify migrate --help` 零副作用、未声明选项拒绝（Typer exit 2）；引擎为进程内库，不属于必答 `--version` 的脚本集 |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | 阶段检查点记录方向审计与并发读数；命令面在 help 与模板中保留规则指针，不新增机制 |

**Gates Status**: ✅ All gates pass（无 Fail / Partial 行，Complexity Tracking 为 N/A）。

**Re-check after Phase 1**: 2026-11-10 — Phase 1 工件（data-model / 3 契约 / quickstart / feature-ref）落盘后复核：22 行维持 Pass；唯一变化是 XIV/XXI 的证据由「计划意图」升级为「契约条款 + 命令 help 契约」，无新增违规。

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md` — this section carries records in that shape and does not restate its rules.*

### T-001 — 期望态用「init 参照树」整体投影，而不是逐文件重写比较

- **decision**: 期望态由「把当前安装版本的资产经 init 的同一复制机制投影到临时参照树」得到，差异对照只做文件集合与字节比较。
- **antithesis**: 逐文件期望内容计算——直接调用 `rewrite_paths` 与 `generate_commands` 在内存中逐文件生成期望内容再比较；当工作区资产规模大、干跑频繁、且每个投影面都能被稳定地单文件调用时它更优——干跑无需整树复制，冷启动延迟更低。
- **binding_constraints**:
  - pole_a: 正确性——投影语义（路径改写、命令生成）必须只有一份实现，任何比较器都不得复制它。
  - pole_b: 成本——干跑应避免与资产规模成正比的整树复制，最好保持纯读取。
- **discriminating_evidence**: 在同一旧版夹具上，用一次性脚本按 `rewrite_paths(source)` 逐文件生成期望内容，与参照树中的同名文件逐字节比对；结果二值：全等 / 存在不等。存在不等即证明参照树漏掉了某个投影面（或逐文件方案多引入了第二语义）。
- **expected_sacrifice**: SC-001 Source ↓ 每次干跑付出一次与工作区资产同量级的临时树复制，冷启动延迟高于内存内逐文件比较。
- **revision_trigger**: 干跑在典型夹具上连续两次超过 30 s，或参照树复制成为测试预算的主要开销 → 重开，改为逐文件期望内容计算并补投影面清单测试。

### T-002 — 框架源工作区把镜像/副本维度委托给既有检查器，而不是统一走参照树

- **decision**: 检测到框架源树（`skills/external/` 存在，与 sanitize 既有 guard 同源）时，镜像与生成副本维度直接消费 `sync-mirrors.py --check` 与 `regen-command-copies.py --check`；客户端工作区才用 init 参照树比较。
- **antithesis**: 单一参照树比较器用于所有工作区；当仓库自身 `.specify/` 也以 init 投影形态维护（而非 sync-mirrors 字节形态）时它更优——一份比较语义、无模式分支。
- **binding_constraints**:
  - pole_a: 正确性——本仓 `.specify/` 的字节形态（含投影块）由 sync-mirrors 拥有，参考物不得把它判成漂移。
  - pole_b: 证据面——收敛路径应尽量单一，使每个模式都享有同等的逐维度变异实测覆盖。
- **discriminating_evidence**: 取本仓一对已同步镜像（`shared/definitions/framework-map.md` 与 `.specify/shared/definitions/framework-map.md`），判定 `mirror == rewrite_paths(source)`；结果二值：相等 / 不等。实测（2026-11-10，`test-evidence/plan-gates.txt`）：`mirror == source` 为真而 `mirror == rewrite_paths(source)` 为假——落在「不等」分支，即统一参照树会在本仓误报漂移，委托模式是该事实下唯一不自相矛盾的选择。
- **expected_sacrifice**: SC-003 Source ↓ 三类验收夹具均为客户端形态，框架源模式的收敛正确性交由 sync-mirrors/regen 既有契约测试兜底，migrate 侧不为该模式新增逐维度变异实测。
- **revision_trigger**: 若出现一次「委托检查器判 clean 而参照树比较判漂移」且参照树一侧被证明正确 → 重开，评估把本仓 `.specify/` 迁移为 init 投影形态。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/097-speckit-migrate-command/
├── requirements.md      # 上游规格（已完成，含 clarify 裁定）
├── research.md          # Phase 0 调查读数（本阶段产出）
├── plan.md              # 本文件（/speckit.plan 产出）
├── data-model.md        # Phase 1：差异项/计划/回执/归档/结局实体与状态
├── contracts/           # Phase 1：3 份契约
│   ├── migrate-cli.md       # 命令面、选项、结局与退出码、stdout 包络
│   ├── migrate-engine.md    # 五维、处置映射、复用边界、安全/幂等/续跑、回执与并发
│   └── migrate-template.md  # /speckit.migrate 薄投影、装配面与等价性
├── quickstart.md        # Phase 1：4 个用户旅程场景
├── feature-ref.md       # Phase 1：Feature 024 绑定与 FR→WP 矩阵
├── tasks.md             # 下一阶段（/speckit.tasks）产出
└── verification.log     # 实现阶段产出
```

### Source Code (repository root)

```text
src/specify_cli/__init__.py                     # + specify migrate 子命令、参照树构建、五维规划器、执行器、回执
templates/commands/migrate.md                   # 运行期模板唯一来源
.github/prompts/speckit.migrate.prompt.md       # regen-command-copies 生成（copilot）
.claude/commands/speckit.migrate.md             # regen-command-copies 生成（claude）
.qoder/commands/speckit.migrate.md              # regen-command-copies 生成（qoder）
.opencode/command/speckit.migrate.md            # regen-command-copies 生成（opencode）
docs/reference/commands/migrate.md              # 命令参考页（执行流、选项、结局、边界）
skills/internal/sanitize-materials/SKILL.md     # Migration wrap-up lane 定位声明收敛
.specify/skills/internal/sanitize-materials/SKILL.md  # 镜像（sync-mirrors --write 再生成）
shared/definitions/framework-map.md             # 登记 .specify/memory/migrate/ 与 .specify/archive/migrate/
.specify/shared/definitions/framework-map.md    # 镜像（sync-mirrors --write 再生成）
tests/contract/test_migrate_cli_surface.py      # 命令面/退出码/help/未声明选项
tests/contract/test_migrate_engine_contract.py  # 五维/处置域映射/无第二实现的结构守卫
tests/contract/test_migrate_template.py         # 模板薄投影 + Qoder frontmatter
tests/contract/test_migrate_distribution_assembly.py  # 源模板/四副本/文档页/基线冻结
tests/unit/test_migrate_planner.py              # 维度映射、稳定排序、去重、变异注入拒绝
tests/unit/test_migrate_receipts.py             # 逐运行一文一件、两写者不同路径
tests/integration/test_migrate_us1_converge.py  # 纯旧版：干跑零写入 → 应用收敛 → 再跑 clean
tests/integration/test_migrate_us2_safety.py    # 无 tty blocked、归档找回、冲突 refuse、用户内容保护
tests/integration/test_migrate_us3_crossversion.py  # N→N+k 一次直达、中断续跑不二次搬移
tests/integration/test_migrate_us4_equivalence.py   # 两入口同计划、模板不复制逻辑
tests/fixtures/migrate-097/builders.py          # 由声明生成的旧版/混杂/最新夹具构建器
tests/contract/test_migration_distribution.py   # COMMAND_BASELINE 29 → 30
.specify/memory/migrate/receipts/               # 运行时回执（apply 时创建；逐运行一文一件）
.specify/archive/migrate/                       # 运行时归档（apply 时创建；<run-id>/ 下保相对布局）
```

**Structure Decision**: 扩展现有单模块 Typer CLI（`src/specify_cli/__init__.py`）与既有命令装配面；不新建顶层目录。两个新运行时目录挂在已登记根下（`.specify/memory/`、`.specify/archive/`），登记随本变更落地（WP10）。

### Mirror Obligations

基线（测量于 2026-11-10，本 worktree，见 `research.md` R-8）：`regen-command-copies.py --check` exit 0；`sync-mirrors.py --check` exit 0。判据统一为「本特性触及的镜像对 **no NEW drift**」，不是全绿断言。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/migrate.md` | `.github/prompts/speckit.migrate.prompt.md`; `.claude/commands/speckit.migrate.md`; `.qoder/commands/speckit.migrate.md`; `.opencode/command/speckit.migrate.md`（`regen-command-copies.py` 生成；无 `.specify/templates/commands/` 镜像——该面已退役） | 再生成后 `regen-command-copies.py --check` 相对 R-8 基线无 NEW drift；引用模板名的 `AUTO-GENERATED` 标记存在 |
| `skills/internal/sanitize-materials/SKILL.md` | `.specify/skills/internal/sanitize-materials/SKILL.md` | `sync-mirrors.py --write --only skills/internal/sanitize-materials` 后 `--check` 无 NEW drift；`diff -q` 两文件一致 |
| `shared/definitions/framework-map.md` | `.specify/shared/definitions/framework-map.md` | 同上（`--only shared/definitions/framework-map.md`）；两文件字节一致 |
| `src/specify_cli/__init__.py`、`docs/reference/commands/migrate.md` | 无镜像（前者入 wheel，后者是项目开发文档、不分发） | 不适用；由 WP08/WP14 的装配面测试覆盖 |

### Work Packages (≤16，供 `/speckit.tasks` 切分)

| WP | 内容 | FR |
|----|------|-----|
| WP01 | `specify migrate` 子命令面：4 个选项、前置条件、结局→退出码、`--help` 零副作用、未声明选项拒绝、stdout text/json 包络 | FR-001, FR-003, FR-019, FR-022 |
| WP02 | 工作区形态识别与客户端参照树：`framework-source` 判定（`skills/external/`，与 sanitize guard 同源）、按已安装资产运行 init 复制机制到临时树（仅客户端模式）、工具/脚本变体探测、失败清理 | FR-005, FR-006, FR-007 |
| WP03 | 五维规划器：模板与生成物、锚点布局、兼容链接、镜像一致性、迁移残留；稳定排序、按 target 去重、逐项「维度/当前态/期望态/拟处置/依据路径」 | FR-006, FR-007, FR-008 |
| WP04 | 处置分类与安全门：六值域映射（引用 FR-014）、破坏桶分类（判据与清单 owner = `.specify/shared/guidelines/confirmation-gates.md`）、双键确认、非交互 blocked、冲突 refuse、平台降级 refuse | FR-014, FR-015, FR-016 |
| WP05 | 执行器：write/replace/archive 逐项执行、归档布局、锚点引擎 apply 委托、平铺移动、链接与副本写、幂等与中断续跑、引擎写模式委托 | FR-009, FR-010, FR-011, FR-016, FR-017 |
| WP06 | 回执：apply 落盘 `.specify/memory/migrate/receipts/<run-id>.json`、干跑只走 stdout、逐项状态、恢复路径、并发两写者不同路径 | FR-018 |
| WP07 | init 决策/执行拆分：从 `cleanup_obsolete_framework_assets` / `migrate_flat_internal_skills` 提出纯决策函数，两入口共享；等价性测试 | FR-009 |
| WP08 | 模板与装配：`templates/commands/migrate.md`、四副本再生、Qoder frontmatter、`docs/reference/commands/migrate.md`、`COMMAND_BASELINE` 29→30 | FR-002, FR-021, FR-022 |
| WP09 | sanitize lane 定位声明收敛：Migration wrap-up lane 改为「周期复检兜底，一次性收尾主入口是 migrate」，镜像同步 | FR-012 |
| WP10 | 目录治理：`shared/definitions/framework-map.md` 登记 `.specify/memory/migrate/` 与 `.specify/archive/migrate/`，镜像同步 | FR-018（目录治理约束） |
| WP11 | 夹具构建器：由声明生成的纯旧版 / 新旧混杂 / 已最新三类夹具（退役清单、旧代状态文件、平铺残留、旧锚点布局） | FR-023 |
| WP12 | 集成验收 US1+US3：干跑零写入、应用收敛、再跑 clean、N→N+k 一次直达、中断续跑不二次搬移 | FR-008, FR-017, FR-020, FR-023, FR-025 |
| WP13 | 安全与用户内容验收 US2：无 tty blocked、归档逐条找回、冲突指名双方、用户内容逐字节不变、变异注入转红（含逐维度移除收敛处置后对应检查转红的断言，FR-008/FR-024） | FR-008, FR-015, FR-016, FR-024 |
| WP14 | 等价与分发验收 US4：两入口同计划、模板薄投影结构守卫、装配面齐全、`regen --check` 无 NEW drift、镜像无 NEW drift | FR-002, FR-021, FR-022, FR-025 |

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | CPython `>=3.8` 的文件系统/路径语义足以完成差异枚举、归档移动、回执写入与只读探测 | `pyproject.toml` `requires-python` 声明 + 本阶段读数在同一解释器实测（本环境 CPython 3.11；3.8 运行时兼容由项目既有支持契约承担，本阶段未在该版本实测，`research.md` R-8） | verified | — |
| EP-002 | Typer 的模块级 `@app.command()` 注册形态可直接新增子命令，且未声明选项由框架拒绝（exit 2） | `src/specify_cli/__init__.py:2785-2791,3330-3380`；`specify --help` 实测仅 init/check/render-agents | verified | — |
| EP-003 | pytest 运行器（`scripts/bash/run-tests.sh`）可执行本特性的 contract/integration/unit 子集 | 实测 `bash scripts/bash/run-tests.sh tests/contract/test_anchor_layout_migrate.py -q` → 3 passed（2026-11-10，默认并行形态）；`test-evidence/plan-gates.txt` | verified | — |
| EP-004 | 既有引擎可进程内导入或按 CLI 动作只读消费，且继续满足接口契约 | `research.md` R-2；`anchor-layout-migrate.py --help`、`regen --check`、`sync-mirrors --check` 实测 exit 0 | verified | — |
| EP-005 | `.specify/source.json` 只存在于 043 之后初始化的项目；旧项目缺席是正常事实 | `write_source_stamp`（`__init__.py:606-631`，调用点 :3257）；043 契约 `source-stamp-write` | verified | — |
| EP-006 | 测试平台支持符号链接创建；不支持时命令以 `refuse` 报告降级事实而非崩溃 | 本环境 Linux 创建符号链接成功（init 夹具路径 `ensure_specify_symlink`）；降级映射见 `contracts/migrate-engine.md` § 平台降级 | verified | — |

## Inherited Blockers

Dependency set: none

本特性不依赖任何携带未结记录的依赖特性；被消费的 init / sanitize / anchor-layout / sync-mirrors / regen 面均为已落地的框架能力（`research.md` R-2/R-3/R-8），不以 feature 依赖身份进入本表。

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | — | not-applicable | — | — | 声明依赖集为空；无被提取的 blocked/deferred/partial 记录可处置 |

## Complexity Tracking

N/A — Constitution Check 无 Fail / Partial 行，无需豁免。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | `data-model.md` | 9 entities（E-1 DiffItem、E-2 Plan、E-3 Receipt、E-4 ArchiveEntry、E-5 RunOutcome、E-6 WorkspaceKind、E-7 ReferenceTree、E-8 维度映射、E-9 Pointer）+ 5 条不变量 |
| Contracts | `contracts/` | 3 files：`migrate-cli.md`（C-1…C-7）、`migrate-engine.md`（C-1…C-8）、`migrate-template.md`（T-1…T-6） |
| Quickstart | `quickstart.md` | 6 个场景（0 前置已实测 / 1 已最新 / 2 旧版收敛 / 3 非交互 blocked / 4 冲突与中断 / 5 代理会话）；未实现示例逐例列前提并由契约测试钉住，清理步骤已实测 |
| Feature ref | `feature-ref.md` | Feature 024 绑定 + FR→WP 矩阵（25/25 FR 覆盖，14 个 WP） |

与 Phase 0 预期的漂移：无。研究阶段预计 `research.md` 独立成文（> 50 行且含外部既有引擎评估），实际按此落地；契约数量按 3 份（命令面 / 引擎 / 模板）落地，与 WP01/WP02–WP07/WP08 的边界一致。
