# Implementation Plan: 确认门控精简(Reduce Confirmation Flows)

**Branch**: `044-reduce-confirmation-flows` | **Date**: 2026-08-18 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `044-reduce-confirmation-flows` → Feature 046 Confirmation Gate Governance
**Input**: Specification from `.specify/specs/044-reduce-confirmation-flows/requirements.md`

## Summary

框架内约 55–60 处"阻塞等待用户确认"门控中,多数保护的是可逆动作,已显著拖慢日常使用(典型:team 创建/运行/收尾三次打断)。本计划落地 Feature 046 的两级确认分类判据——**破坏性/不可撤销动作保留前置确认,可逆动作自动执行并附事后执行报告**——交付物为:一份框架级共享约定文档(分类判据真源)、一个确定性门控扫描脚本(度量与防回流)、对 team 命令/技能与全框架可逆门控的源侧改写(经 regen-command-copies.py + sync-mirrors.py 传播到全部运行时副本)。纯 prompt/文档 + 一个 stdlib 脚本,零运行时引擎、零新存储。

## Technical Context

**Language/Version**: Python >= 3.8(仅新增扫描脚本,stdlib-only);其余交付物为 Markdown(prompt/模板/约定)
**Primary Dependencies**: 无新增;复用既有 `scripts/python/regen-command-copies.py`(命令副本扇出)与 `scripts/python/sync-mirrors.py`(镜像同步)
**Storage**: Markdown 文件(模板/技能/共享约定)+ 扫描结果 JSON(stdout,不落盘存储);治理基线快照作为规格工件存档于本目录
**Testing**: pytest(`tests/contract/` 契约测试,markers: contract/integration)
**Target Platform**: 全部 6 家受支持 AI agent CLI 的命令运行时(Claude Code / Codex CLI / Qoder CLI / GitHub Copilot / opencode / Hermes Agent)
**Project Type**: 代码生成器/框架(templates/, scripts/, skills/, shared/, src/specify_cli/)
**Performance Goals**: 门控扫描全仓 <10s(一次性批处理,非热路径);零确认打断为交互性能目标(SC-001)
**Constraints**: 不新增存储/引擎/依赖(Constitution IX);破坏性门控保留率 100%(SC-004);镜像与生成副本零漂移
**Scale/Scope**: 治理面 ≈55–60 处门控(约 20 个命令模板 + create-team 技能 + 4 份共享文档);新增 2 个源文件(约定文档 + 扫描脚本)+ 4 份契约

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.9.x, 13 principles):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 本计划由 requirements.md(3 US / 11 FR / 5 SC,澄清完毕)驱动,走 spec→plan→tasks→implement 全程 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 046 Confirmation Gate Governance,单一 Feature 范围,feature-ref.md 记录映射 |
| III | Intent-Driven Development | ✅ Pass | 交付物为 prompt/约定层改写,表达"可逆即自动执行"的意图判据,不硬编码执行细节 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 4 份契约(taxonomy / team-flow / gate-scanner / execution-report)+ 每契约配套 contract 测试,TDD 顺序见 tasks |
| V | AI Agent Integration Standards | ✅ Pass | 命令模板改写经 regen-command-copies.py 单一源扇出到 6 家 CLI 副本,无手工分叉 |
| VI | Continuous Quality & Observability | ✅ Pass | 扫描脚本提供 SC-002/SC-005 的可重复度量;执行报告契约保证自动执行动作可观察 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 本文件即工作流第 2 步产物,后续 tasks/implement 依序进行 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 分类判据唯一真源 shared/guidelines/confirmation-gates.md;镜像与副本全部由生成器再生,禁手写 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 纯 prompt/文档 + 一个确定性 stdlib 扫描脚本;无运行时调度、无新存储、无新依赖 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新文档落 shared/guidelines/(与 token-efficiency、task-complexity-rubric 同类),小写路径语义名,不触碰保留文件名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 本仓以框架作者帽编辑 templates/、skills/、shared/ 源侧(机制侧修复,传播到全部客户项目);本计划自身走本框架 SDD 流程(自举);Loop A 反馈链不变仅非阻塞化 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 门控扫描能力经查 `.specify/memory/tools/` 与 scripts/python/ 无既有 Tool(gate-check.py 为写入门禁判定,非门控盘点),新脚本为预期产出;镜像/副本传播复用 sync-mirrors.py / regen-command-copies.py |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 本需求即 harness 改进:削减 Agent Work Loop 中的无效停等(确认打断),feedforward 侧以判据文档约束未来流程 |

**Gates Status**: ✅ All gates pass(无 Fail / Partial,无需 Complexity Tracking)

**Re-check after Phase 1**: 2026-08-18 — Phase 1 工件(data-model.md + 4 contracts + quickstart.md + feature-ref.md)落盘后复核:13 项结论不变,契约面使 IV 证据更实(契约文件见 contracts/),其余同上表。

## Phase 0: Research Review

无独立 research.md——Phase 0 发现简短且全部可由仓内调查解决,按模板指引内联于此。

**P0-1 门控盘点(需求阶段已完成,作为基线)**:经全框架扫描确认 ≈55–60 处阻塞确认指令,分布:约 20 处样板化反馈提交提示、约 10 处收尾术语确认、约 8 处可逆 preview→confirm 写入门控(goal/tools/agents/skills/team 等)、约 8 处破坏性/不可撤销门控(删除/移动/推送/覆盖,保留)、约 5 处固有交互(interview/constitution)、4 处 team 流程门控。基线快照存档为 `baseline-gates.md`(本目录)。

**P0-2 既有概念基础**:`shared/patterns/reconcile-pattern.md` § Tiered confirmation 已有三级表(safe local writes 自动 / external authoritative 停等 / destructive-move-archive 停等)——Feature 046 的分类判据是其推广,不另造概念。

**P0-3 传播机制**:命令模板真源 `templates/commands/*.md`,经 `regen-command-copies.py` 扇出到 .claude/.qoder/.github/prompts/.opencode 各工具副本;skills/↔.specify/skills/、shared/↔.specify/shared/、scripts/python/↔.specify/scripts/python/ 经 `sync-mirrors.py` 同步。所有改写只落源侧。

**设计决策(Decisions)**:

- **D1 判据真源位置**:`shared/guidelines/confirmation-gates.md`(guidelines 类,与 token-efficiency.md、task-complexity-rubric.md 并列);commands/skills 模板以单行引用接入,不复制判据正文(对齐 Token Efficiency 纪律的"引用不复制"模式)。
- **D2 治理三分类**:判据在两级(破坏性 vs 可逆)之上显式设第三桶"治理保留清单"(governance-kept)——固有交互(interview 退出门、constitution 不可撤销确认)与安全规范对齐门控(git commit 显式批准、implement gate.yaml CONFIRM 判定、git-workflow 远程操作)凭清单保留,不依赖可逆性推断。存疑从严规则仅作用于两级之间。
- **D3 扫描脚本**:`scripts/python/scan-confirmation-gates.py`(stdlib-only,Program-First):按阻塞确认语义模式扫描 templates/commands/、skills/、shared/、templates/*.md,输出 JSON(逐条 gate 记录 + 汇总),支持 `--baseline` 对比;度量 SC-002/SC-005 并防回流。不建 UI、不落存储。
- **D4 team 例外**:持续循环类(continuous)运行保留 `create-team` references 中既有分级门控(operating-loops.md / workspace-cluster.md),一次性模式(parallel/serial/iteration)全自动——来自澄清会话 2026-08-18。
- **D5 反馈提交提示**:`shared/workflow/feedback-step.md` 改为"达阈值在收尾报告附一行非阻塞提示(附提交命令)",绝不阻塞、绝不自动传输——来自澄清会话 2026-08-18。
- **D6 术语确认非阻塞化**:收尾术语写入改为直接写入 + 报告;**冲突/覆盖用户既有权威条目时仍停等**(glossary 协议的冲突确认属破坏性桶:覆盖用户数据)——FR-008 但书。
- **D7 执行报告契约**:三要素(执行内容/产出工件/修改途径);琐碎动作并入所属流程收尾报告逐项列明(FR-009 粒度豁免,澄清会话 2026-08-18);失败如实报告中间产物(FR-010)。
- **D8 instructions 接线**:`templates/instructions-template.md` Documentation Map 增一行指向 confirmation-gates.md,使判据对所有命令 ambient;实现期以 `/speckit.instructions` 再生本仓 AGENTS.md 等符号链接消费面。
- **D9 保留清单(不改)**:feedback.md consume 报告确认(前置原子删除)、docs.md 移动/归档/删除分级、session.md 同名覆盖、feature.md 状态回退、analyze.md 补救批准、tools invoke 预览门控(任意脚本执行,存疑从严)、constitution-template 不可撤销确认、git-workflow push/force 门控、interview 全部交互。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/044-reduce-confirmation-flows/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── baseline-gates.md    # 治理前门控基线快照(SC-002 度量基准)
├── checklists/requirements.md  # /speckit.requirements 产物
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md     # Implementation output (/speckit.implement command)
```

No standalone research.md — findings inlined under `## Phase 0: Research Review` above.

### Source Code (repository root)

```text
shared/guidelines/              # 新增 confirmation-gates.md——分类判据真源(FR-001/002/003)
templates/commands/             # team/goal/tools/agents/skills/todo/implement 等门控改写 + 样板确认非阻塞化(FR-004..008)
templates/instructions-template.md  # Documentation Map 增判据文档引用(D8)
skills/create-team/             # SKILL.md + references 门控改写(创建/运行/收尾零确认,continuous 例外)(FR-004..006)
scripts/python/                 # 新增 scan-confirmation-gates.py——门控扫描与基线对比(D3)
tests/contract/                 # 4 份契约对应的契约测试
.specify/                       # 上述各面的运行时镜像(全部由 sync-mirrors.py / regen-command-copies.py / speckit.instructions 再生,禁手写)
```

**Structure Decision**: 落在既有"代码生成器/框架"形态内:新增恰好 2 个源文件(shared/guidelines/confirmation-gates.md、scripts/python/scan-confirmation-gates.py),其余为对既有模板/技能/共享文档的源侧改写;无新顶级目录。所有运行时副本经既有生成器再生(见 Mirror Obligations)。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/*.md`(受影响 stem:team, goal, tools, agents, skills, todo, implement, requirements, plan, tasks, clarify, research, review, analyze, checklist, docs, feature, feedback, session, interview, history, constitution, instructions) | `.specify/templates/commands/*.md`(sync-mirrors);per-tool 副本:`.claude/commands/speckit.<stem>.md`、`.qoder/commands/speckit.<stem>.md`、`.github/prompts/speckit.<stem>.prompt.md`、`.opencode/command/speckit.<stem>.md`(regen-command-copies) | `python3 scripts/python/regen-command-copies.py --check` exit 0;`python3 scripts/python/sync-mirrors.py --check` exit 0 |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md`(byte-identical);`.specify/instructions.md` 再生(AGENTS.md/CLAUDE.md/QODER.md/.github/copilot-instructions.md 符号链接消费) | `/speckit.instructions` 再生后 diff 核对;符号链接完好 |
| `skills/create-team/SKILL.md` + `references/*` | `.specify/skills/create-team/**`(sync-mirrors;`.github/skills` 为符号链接,无副本) | `sync-mirrors.py --check` exit 0 |
| `shared/workflow/feedback-step.md`、`shared/workflow/glossary.md`(微调)、新增 `shared/guidelines/confirmation-gates.md` | `.specify/shared/**`(sync-mirrors) | `sync-mirrors.py --check` exit 0 |
| 新增 `scripts/python/scan-confirmation-gates.py` | `.specify/scripts/python/scan-confirmation-gates.py`(sync-mirrors) | `sync-mirrors.py --check` exit 0 |

## Complexity Tracking

N/A — Constitution Check 全 Pass,无违规需辩护。

## Phase 1: Design & Contracts

工件已落盘(见 Summary after-fill):

- **data-model.md** — 4 个实体:Confirmation Gate(门控扫描记录)、Confirmation Taxonomy(判据)、Execution Report(执行报告)、Gate Scan Report(扫描汇总)。本 Feature 的"数据"是扫描输出 schema 与报告结构,无持久化存储。
- **contracts/** — 4 份契约:
  1. `confirmation-taxonomy-contract.md` — 判据规则、破坏性清单、治理保留清单、存疑从严、判据文档的结构约束
  2. `team-flow-contract.md` — team 命令/create-team 技能的零确认行为(创建落盘、运行启动、收尾自动化、continuous 例外)
  3. `gate-scanner-contract.md` — 扫描脚本 CLI 契约:参数、JSON 输出 schema、基线对比语义、退出码
  4. `execution-report-contract.md` — 三要素报告 + 琐碎并入规则 + 失败如实报告
- **quickstart.md** — 3 条走查:team 零确认全流程、扫描脚本治理前后对比、破坏性门控保留抽查。
- **feature-ref.md** — Feature 046 绑定与本计划映射。
