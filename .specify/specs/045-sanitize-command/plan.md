# Implementation Plan: 框架资料卫生治理——残留冗余清理与关键资料正确性检查(Sanitize Command)

**Branch**: `045-sanitize-command` | **Date**: 2026-08-20 | **Spec**: [requirements.md](requirements.md)  
**Requirement → Feature**: `045-sanitize-command` → Feature 047 Framework Material Hygiene(框架资料卫生)  
**Input**: Specification from `.specify/specs/045-sanitize-command/requirements.md`

## Summary

新增 `/speckit.sanitize` 命令与 stdlib-only 引擎 `sanitize-utils.py`:检查模式扫描框架自有资料根(运行时动态探测),确定性检查(死引用/索引一致/符号链接/镜像漂移)由引擎直接判定并落盘;时间性声明材料(parked/draft)由引擎采集证据包(提交历史摘要/文件存在性)、agent 仅对证据摘要作过期/冗余语义判定;全部发现以稳定 ID 并入累积台账 `.specify/memory/sanitize/findings.json`(初始 pending)。呈现摘要后提示是否进入清理;删除/归档属破坏性桶,以前置确认的清理计划为执行前提(引擎拒绝无 confirmed 标记的 apply),处置完成后更新发现状态并出具三要素执行报告。复用既有能力:docs 树断链复用 `docs-utils.py`(导入)、镜像漂移复用 `sync-mirrors.py --check`(子进程)、归档落 `.specify/archive/`(既有根)。不触及用户代码/脚本/测试。

## Technical Context

**Language/Version**: Python ≥ 3.8(引擎 stdlib-only,与 feedback-utils.py / evidence-utils.py 同纪律)  
**Primary Dependencies**: 无第三方依赖;复用 `scripts/python/docs-utils.py`(模块导入,docs 树链接校验)与 `scripts/python/sync-mirrors.py`(子进程 `--check`,镜像漂移);git 证据经 `subprocess` 调用本仓 git  
**Storage**: `.specify/memory/sanitize/findings.json` —— 累积发现台账(单一文件,稳定 ID 合并语义);归档处置移入 `.specify/archive/<原相对路径>`(既有 `.specify/archive/spec/` 先例的推广)  
**Testing**: pytest(contract / unit / integration 标记);夹具复刻真实案例(过期 parked todo + 已合入提交)驱动 SC-001;命令模板结构契约测试对齐 046 模式  
**Target Platform**: 跨平台本地 CLI 上下文(Linux/macOS/Windows),与既有 *-utils.py 相同  
**Project Type**: 框架扩展——命令模板 + 引擎脚本,零新顶层目录  
**Performance Goals**: 检查模式在本仓规模秒级完成;证据采集与呈现走摘要/投影(摘要优先),不整读大文件  
**Constraints**: 引擎 stdlib-only;检查模式写入仅限台账文件(被检材料零修改);agent 语义判定只消费引擎产出的证据摘要  
**Scale/Scope**: 资料根运行时动态探测(缺失视为空集);git 证据采集限定声明材料引用的路径/提交

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 需求 045(3 US / 12 FR / 5 SC)→ 本 plan → contracts → tasks 全链 SDD 产物 |
| II | Feature-Centric Development | ✅ Pass | Feature 047 已注册(features.md 索引行 + features/047.md),本 plan 记录 key changes |
| III | Intent-Driven Development | ✅ Pass | Overview 固化动机实例(0801 过期 parked todo vs 1a090c72),验收对照 SC-001 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 4 份契约 + 契约测试先行;夹具复刻真实案例作为 SC-001 度量源 |
| V | AI Agent Integration Standards | ✅ Pass | 命令模板经 regen 传播 4 家工具副本;agent/engine 职责split 由契约钉死(语义判定仅消费证据摘要) |
| VI | Continuous Quality & Observability | ✅ Pass | 发现台账 = 资料卫生可观测面;破坏性门控挂必要性 probe(门控观察协议) |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 遵循 /speckit.plan → /speckit.tasks → /speckit.implement 标准流 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 过期判定以 git 提交/文件存在性为证据源,绝不信材料自述(FR-003) |
| IX | Framework Scope Discipline (No Over-Engineering) | ⚠ Partial — see Complexity Tracking | 新命令面 + 新引擎 + 新台账为 FR-001..012 必需面;能复用面(docs-utils/sync-mirrors/.specify/archive/)全部复用,零投机机制 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 用户文档落 docs/reference/commands/sanitize.md;台账落 .specify/memory/sanitize/ |
| XI | Dogfooding (Self-Application) | ✅ Pass | 实现含本仓真实 dogfood 运行(动机案例即首个清理对象),发现走既有 feedback 通道 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | docs 断链复用 docs-utils、镜像漂移复用 sync-mirrors --check、归档复用 .specify/archive/;新引擎登记 Tool 记录 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 判定纪律对齐 040(程序优先/摘要优先);证据引用可复核 = evidence discipline |

**Gates Status**: ⚠ 一项 Partial(IX),已在 Complexity Tracking 豁免论证;其余 12 项 Pass。

**Re-check after Phase 1**: 2026-08-20 —— data-model.md(5 实体)/ 4 contracts / quickstart.md(3 走查)/ feature-ref.md 落盘后复扫:IX 维持 Partial(设计未新增超出 FR 的机制面);XII 增强(复用面在契约 C-1 钉死);其余不变。

## Phase 0: Research Review

本仓内部探索结论(简短,内联;无独立 research.md):

1. **命令传播链**:`templates/commands/sanitize.md`(源)→ `regen-command-copies.py` 生成 4 份工具副本(`.claude/commands/speckit.sanitize.md`、`.github/prompts/speckit.sanitize.prompt.md`、`.opencode/command/speckit.sanitize.md`、`.qoder/commands/speckit.sanitize.md`);`.specify/templates/` 镜像已排除 commands/(退役),无该镜像义务。
2. **注册点**:probe-definitions.md Objects 表新增 2 行(`speckit-sanitize-wrapup` / `gate-sanitize-destructive-cleanup`);`tests/contract/test_feedback_command_classification.py` 复杂命令计数 17→18;`docs/reference/commands/sanitize.md` 新增;引擎登记 Tool 记录 `.specify/memory/tools/sanitize-utils.py.md`。
3. **存储选型**:feedback(index+条目,追加重写)与 evidence(每运行一目录)均不合"累积发现 + 状态合并"语义 → 单文件台账 findings.json,合并规则入契约 C-2。
4. **复用面**:docs-utils `validate` 的断链检查作用域=根注册文件+docs/**,模块级可导入(sanitize 的 docs 树死引用判定直接复用);sync-mirrors `--check` 输出 MISS/DIFF/ORPHAN(sanitize 镜像漂移 lane 复用,另补孤儿目录 diff 与 obsolete-registry 交叉核对);evidence-utils `doctor` 为引擎三态探测先例。
5. **门控接线**:scan-confirmation-gates.py 对含删除/归档关键词的确认门控自动归类 keep_gate(sanitize 清理门控不构成违例);044 baseline.json 的 total 需 +1 同步;门控单行指针措辞须避开阻塞模式。
6. **归档先例**:`.specify/archive/spec/<NNN-slug>/` 既有;memory 材料归档推广为 `.specify/archive/memory/<原相对路径>`。
7. **引擎 CLI 惯例**:沿用 feedback-utils 的 `--action` 子命令 + `--workspace-root` + JSON 输出 + 退出码 0/2(1=CliError)。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/045-sanitize-command/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

No standalone research.md — findings inlined above.

### Source Code (repository root)

```text
templates/commands/sanitize.md                     # /speckit.sanitize 命令模板(唯一源)
scripts/python/sanitize-utils.py                   # stdlib-only 引擎(collect/record/status/apply)
shared/definitions/probe-definitions.md            # +2 个 probe Objects(wrapup + 清理门控)
docs/reference/commands/sanitize.md                # 用户面命令文档
.specify/memory/tools/sanitize-utils.py.md         # 引擎 Tool 记录(Tool Reuse 纪律)
.specify/memory/sanitize/findings.json             # 运行时发现台账(dogfood 运行产物)
tests/contract/test_sanitize_engine_contract.py    # 引擎 CLI/台账 schema/合并语义契约
tests/contract/test_sanitize_template.py           # 命令模板结构契约(门控/分诊/红线)
tests/unit/test_sanitize_engine.py                 # 夹具驱动引擎测试(含真实案例复刻)
tests/fixtures/sanitize/                           # 夹具:过期 todo/死引用/断链/孤儿镜像/索引缺项
```

**Structure Decision**: 框架既有"命令模板 + 引擎脚本"解剖的常规扩展——不新增顶层目录;新增物全部落入 templates/commands/、scripts/python/、shared/definitions/、docs/、tests/ 既有布局;运行时台账落于 .specify/memory/ 既有存储区。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/sanitize.md` | `.claude/commands/speckit.sanitize.md`; `.github/prompts/speckit.sanitize.prompt.md`; `.opencode/command/speckit.sanitize.md`; `.qoder/commands/speckit.sanitize.md`(经 regen-command-copies.py) | regen 后 4 副本含同一编辑;`regen --check` 零 stale |
| `scripts/python/sanitize-utils.py` | `.specify/scripts/python/sanitize-utils.py`(sync-mirrors strict 对) | `diff -q` 逐字节一致;`sync-mirrors --check` exit 0 |
| `shared/definitions/probe-definitions.md` | `.specify/shared/definitions/probe-definitions.md` | `diff -q`;Objects 表双向零差校验 |

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| IX Partial:新命令面(/speckit.sanitize + 4 工具副本)+ 新引擎(sanitize-utils.py)+ 新台账(.specify/memory/sanitize/) | FR-001..012 要求独立命令、持久化发现状态与确认后清理;规格明确该能力为横向资料卫生,Feature 047 已裁定新建而非绑定既有特性 | 复用 /speckit.docs 被拒:reconcile 语义是"内容收敛",不含时间性证据比对与镜像/链接/索引检查;复用 /speckit.review 被拒:那是 SDD 过程质量评审;台账并入 feedback 存储被拒:发现是机器生成累积台账,生命周期(pending→已处置)与反馈条目语义不同 |
