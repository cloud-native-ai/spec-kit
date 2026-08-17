# Implementation Plan: 基于已定义 Goal 的团队创建流程(Goal→Target 分解提议 + 每 Target 一队)

**Branch**: `042-goal-team-creation` | **Date**: 2026-08-17 | **Spec**: [requirements.md](requirements.md)  
**Requirement → Feature**: `042-goal-team-creation` → Feature 027 Team Management  
**Input**: Specification from `.specify/specs/042-goal-team-creation/requirements.md`

## Summary

`/speckit.team` 的 create 流程增加 **goal-based 分支**:入参 token 与 `.specify/goal/` 下现存 `<goal-slug>` 精确匹配(经 `goal-utils.py list` 确定性枚举)并经用户确认后,用 `parse_goal` 加载定义(叙事/判据/生命周期/既有 Targets),呈现四要素 goal 分析(维度、判据覆盖、既有 Target、短期可达成性——建议非门禁);用户裁决单团队或分解路径。分解路径起草 Target 提议集(每条先经引擎 `targets --check` 干跑校验,复用既有 GD-2/GD-3/判据复述检测文法),**一次合并确认**后逐条经既有 `targets --add` 落盘(单一撰写入口不变,team 侧零直写 `goal.md`);既有 open Targets 一律复用为基线。随后**每个 open Target 创建一个团队**:同一 `goal_slug`(N teams : 1 Goal),roster/pattern 以 Target 语句复用 preset 匹配与 pattern 决策树,team.md 新增可选 frontmatter 字段 `focus_target`(局部形 `T-<nnn>`),territory 提议经新的薄校验脚本(复用既有 overlap 文法)验证两两不相交后落盘。run 侧:`--target` 解析顺序变为 **显式 > focus_target > 无**,解析值走既有五项 preview 校验,披露以 "(团队默认)" 标记来源;未声明 focus_target 的团队行为与引入前逐字节等价。

技术路线:**零新依赖、单引擎扩展、薄 I/O 包装**。`goal-utils.py` 新增两个确定性面(`targets --check` 干跑、`resolve_effective_target` 解析函数);`skills/create-team/scripts/verify-territory-disjoint.py` 仅做 JSON 进/verdict 出,内部 import 既有 `expand_scopes`/`scopes_overlap`/`overlap_verdict`(不另立第二套重叠文法);其余全部是模板/技能文档面(`templates/commands/team.md`、`skills/create-team/**`、`docs/reference/commands/`)经 `regen-command-copies.py` + `sync-mirrors.py` 扇出。

## Technical Context

**Language/Version**: Python ≥ 3.8(引擎/脚本,stdlib-only);模板/文档为 Markdown  
**Primary Dependencies**: 无新增——typer/rich 等运行时依赖不触及;`goal-utils.py`、`match-team-preset.py`、`build-summary-input.py` 均既有 stdlib 脚本  
**Storage**: 文件系统事实源——`.specify/goal/<slug>/goal.md`(定义,只经引擎写)、`.specify/teams/<slug>/team.md`(团队定义,新增 `focus_target` 字段)、run 报告与 `items.jsonl`(既有)  
**Testing**: pytest,`tests/contract/`(新 3 个契约测试文件,沿用 `test_goal_targets_engine.py` 的 importlib 进程内 `main()` 断言风格与 `test_run_target_assignment.py` 的模板子串 + per-tool 副本一致性风格);实现前冻结基线(存量失败 vs 回归二分)  
**Target Platform**: 跨平台 CLI 工具链(Linux/macOS/Windows bash);六家 AI agent CLI 的命令副本经再生脚本扇出  
**Project Type**: CLI 工具 + 模板框架(single,framework/code-generator 形态)  
**Performance Goals**: 引擎调用 O(archive 规模);一次成组创建 ≤ 小几十团队,顺序执行;无性能敏感面  
**Constraints**: ① 单一撰写入口——`goal.md`/`## Targets` 只经 `goal-utils.py` 渲染,team 侧流程零直写;② 未声明 `focus_target` 且无显式 `--target` 的 run 全流程与引入前**逐字节等价**(038 SC-002 不回退);③ 判据权威——Target 语句不得复述判据/SC-xxx;④ 镜像零手工双写  
**Scale/Scope**: 分解规模个位到十位级 Target;改动面 = 1 个引擎文件(+镜像)、1 个新薄脚本(+镜像)、2 个模板命令文件源、4 个技能参考文档、1 个用户文档、3 个新测试文件、若干既有测试更新

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, v1.10.0):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 本计划直接由 requirements.md(15 FR/6 SC/3 US)推导;设计工件 data-model/contracts 逐 FR 对应 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 027 Team Management(2026-08-17 clarify 裁定);feature-ref.md 记录映射 |
| III | Intent-Driven Development | ✅ Pass | 用户意图(传入已定义 goal → 分析 → 按需分解 → 每 Target 一队)编码为分支识别与分析披露,不要求用户学新语法 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 4 份 contracts 先行;3 个新契约测试在实现前定稿断言(含逐字节等价回归钉) |
| V | AI Agent Integration Standards | ✅ Pass | 确定性判断全部下沉引擎(check/resolve/overlap),agent 只承担语义提议并附理由;命令面 6 工具副本再生 |
| VI | Continuous Quality & Observability | ✅ Pass | run 报告与台账携带指派落痕(既有面);提议-批准全程 verdict 可溯源 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 本文件为 plan 阶段产物;tasks 阶段按 9 相分解 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 概念不复述——链接 `shared/definitions/goal-definitions.md`;行为真源在引擎函数,模板只编排不判定 |
| IX | Framework Scope Discipline (No Over-Engineering) | ⚠ Partial — see Complexity Tracking | 引擎新增 2 个确定性面 + 1 个薄校验脚本;均为 FR-006/FR-011/FR-012 的程序优先落点,无投机面 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 产物落 `.specify/specs/042-*/`;用户文档落 `docs/reference/commands/`;词汇表经引擎写入 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 分解提议流程可在本仓 goal(如 harness 改进类)上自用;反馈步骤照常嵌入 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | overlap 文法 import 复用不重写;preset 匹配/决策树复用;`--check` 复用与 `--add` 同源校验器,零第二文法 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 补齐 Agent Work Loop "goal→编队" 缺口:大目标到可执行团队的转化获得受纪律流程 |

**Gates Status**: ⚠ 唯一 Partial 为原则 IX,属"新增最小确定性引擎面"的既定例外类别(同 036/041 先例),已列 Complexity Tracking 并给出拒绝的更简替代;其余 12 项 Pass。

**Re-check after Phase 1**: 2026-08-17 — Phase 1 设计工件(data-model.md、4 contracts、quickstart.md、feature-ref.md)落地后复核:IX 维持 Partial(薄脚本与 `--check` 均为契约钉死的必要面),其余不变;见表格同上,无新增 Fail/Partial。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/042-goal-team-creation/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── goal-based-create.contract.md
│   ├── decomposition-proposal.contract.md
│   ├── focus-target-resolution.contract.md
│   └── creation-territory-disjoint.contract.md
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── checklists/          # requirements 校验清单(已存在)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md     # Implementation output (/speckit.implement command)
```

No standalone research.md — Phase 0 findings inlined below (internal investigation only, < 50 lines).

### Source Code (repository root)

```text
scripts/python/goal-utils.py            # +targets --check 干跑校验;+resolve_effective_target 解析函数(复用既有校验器/五查,零第二文法)
skills/create-team/scripts/verify-territory-disjoint.py   # 新薄脚本:territory 提议 JSON 进 → 两两 verdict 出(import 既有 overlap 文法)
templates/commands/team.md              # create 路由 +goal-based 分支;run 模式 +focus_target 解析与披露
skills/create-team/SKILL.md             # create 流程骨架 +goal-based 分支条目
skills/create-team/references/create-mode.md   # goal-based 创建过程规范 +focus_target 字段入 schema
skills/create-team/references/goal.md   # 团队侧 focus_target/提议纪律(扩 §Target)
skills/create-team/references/execution-guide.md  # run 解析顺序 +披露标记 +台账归属
docs/reference/commands/team.md         # 用户文档:goal-based 创建与 focus_target 语义
tests/contract/test_targets_check.py    # --check 干跑契约(退码/零写入/终态拒绝)
tests/contract/test_focus_target_resolution.py  # 解析顺序/披露标记/无字段逐字节等价
tests/contract/test_goal_team_creation.py      # 命令模板分支文本 + per-tool 副本一致性 + 成组建队纪律
```

**Structure Decision**: 扩展现有"模板框架 + 确定性引擎"形态:不新增顶层目录;引擎改动收敛在既有单文件 `goal-utils.py`(+1 镜像),新脚本挂 `skills/create-team/scripts/`(随 skills 镜像对自动扇出),命令面经既有再生链扇出 6 份 per-tool 副本。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/python/goal-utils.py` | `.specify/scripts/python/goal-utils.py` | `cmp` 逐字节;`sync-mirrors.py --write` 后 `--check` exit 0 |
| `templates/commands/team.md` | `.github/prompts/`、`.claude/commands/`、`.hermes/commands/`、`.opencode/command/`、`.qoder/commands/`、`.codex/commands/` 下的 speckit.team 副本(仅已存在目录) | `python3 scripts/python/regen-command-copies.py` 再生;契约测试 `PER_TOOL_COPIES` 逐一 `diff -q` |
| `skills/create-team/SKILL.md` | `.specify/skills/create-team/SKILL.md` | `sync-mirrors.py --check` |
| `skills/create-team/references/create-mode.md` | `.specify/skills/create-team/references/create-mode.md` | 同上 |
| `skills/create-team/references/goal.md` | `.specify/skills/create-team/references/goal.md` | 同上 |
| `skills/create-team/references/execution-guide.md` | `.specify/skills/create-team/references/execution-guide.md` | 同上 |
| `skills/create-team/scripts/verify-territory-disjoint.py`(新) | `.specify/skills/create-team/scripts/verify-territory-disjoint.py` | 同上(新增文件随对同步) |
| `docs/reference/commands/team.md` | 无镜像(docs 单份) | — |

## Phase 0: Research Review

无 standalone research.md——以下勘察结论全部来自仓内实测(Explore 子代理,2026-08-17),供 Phase 1 直接引用:

- **引擎可复用面**(`scripts/python/goal-utils.py`,镜像逐字节相同):`parse_goal(path)` 一次返回 `{slug,status,objective,criteria,history,targets,…}`;`list_goals(root)` 枚举 archive slug;`_reject_bad_target_statement`/`_bad_shape`/判据归一化比对构成 GD-2/GD-3/判据复述**同源检测文法**;`preview_target_check` 七值 verdict(`ok/no-goal-definition/cross-goal/input-error/goal-terminal/dangling/target-terminal`)为五查唯一权威;`resolve_team_goal_identity` 已读 team.md(两级身份解析),扩展读 `focus_target` 语义一致。
- **create 面**(`skills/create-team/references/create-mode.md`):六步过程;frontmatter 字段序 `slug, name, description, goal, goal_slug, territory, pattern, members, config, created, updated`——`focus_target` 插在 `goal_slug` 之后;preset 匹配 `match-team-preset.py --goal "<text>" [--top N]` 输出 `confidence/high|medium|low|none + matches[]`,以 Target 语句为输入即复用。
- **run 面**(`templates/commands/team.md` L79–113):五查在 preview 前依序执行,任何失败零执行痕迹;披露行 `本次 Target: T-002 — <statement>(open)` / `本次 Target: 无(对 goal 整体运行)`;报告行 `**Target 指派**: …`;台账 `target_ref` 仅由 Team Supervisor 写入——`focus_target` 解析的插入点为 Run Mode 第 2 步,且必须保住"未声明且未指定 → 逐字节等价"。
- **territory 面**:`build-summary-input.py` 的 `expand_scopes`/`scopes_overlap`/`overlap_verdict`(`overlap/no-overlap/undecidable`)/`detect_overlaps` 为唯一重叠文法;新脚本 import 复用,不重写。
- **扇出面**:`regen-command-copies.py` → 6 个 `_ASSISTANT_COMMAND_DIRS`;`sync-mirrors.py` 对 `templates→.specify/templates`(不含 commands)、`skills→.specify/skills`。
- **测试先例**:`test_goal_targets_engine.py`(importlib 进程内跑 `main()` 断退码)、`test_run_target_assignment.py`(模板子串 + `PER_TOOL_COPIES` 一致性)、`test_team_command_routing.py`/`test_overlap_verdicts.py`(分类断言)。
- **裁决**:无 /speckit.interview 必要——剩余设计决策(字段插入位、slug 派生模式、`--check` 语义)均可由规格 + 仓内约束推导,已在 contracts 中定约。

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 原则 IX(新增确定性引擎面):`goal-utils.py` +`targets --check`、+`resolve_effective_target`;+`verify-territory-disjoint.py` 薄脚本 | FR-006 要求提议集在呈现前经确定性形态校验(程序优先),FR-011 要求 run 侧解析顺序成为引擎裁决而非模板散文,FR-012 要求两两不相交判定可执行——三者都需要可测试的确定性落点 | (a) 模板散文描述校验规则 → agent 各自复述文法,必然漂移,违背 038 FR-003/FR-007"零第二套检测文法";(b) 由 agent 即兴调用私有函数 → 无契约、无退码、不可测;(c) territory 校验重写一份重叠判断 → 与 036/037 已落地文法双轨,重叠判定结果可分叉。薄脚本仅做 I/O 包装,判定函数全部 import 既有实现 |
