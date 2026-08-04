# Implementation Plan: Team Summary 信息管理机制

**Branch**: `036-team-summary` | **Date**: 2026-08-04 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `036-team-summary` → Feature 027 Team Management
**Input**: Specification from `.specify/specs/036-team-summary/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command, which **replaces** every `[PLACEHOLDER]` token in place — it MUST NOT append a second copy of this template below the filled content. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

把团队自身当作一个"项目",在四种协作模式各自的**阶段边界**上自动刷新一份**累积式**状态总结。产物按**双索引**落地:`.specify/teams/<team-slug>/` 以 team 为索引只保留运行信息(`runs/` / `STATE.md` / `run-log.jsonl` / `items.jsonl`),`.specify/project/goal/<goal-slug>/` 以 goal 为索引承载**唯一的完整总结**并聚合同一 goal 下的全部团队。

技术路径的核心不是新写一个报告模板,而是**让团队侧扮演"表单作者"**:`summarize-project` 的唯一输入是项目输入表单,技能对表单只读不改、R 档缺失即以退出码 3 阻断。因此本方案由四件事构成——

1. **一份概念映射事实源**(`create-team/references/summary-mapping.md`):团队词汇 → 七个项目管理实体,逐模式定义"阶段/工作项"语义;聚合语义下 `project` 实体上移为 **goal**,里程碑取自 goal 的成功判据(一套,不逐团队重复)。
2. **一支确定性表单生成器**(`create-team/scripts/build-summary-input.py`):从 goal 下**全部**团队的 tracked 工件折叠出 `data/project-input.yaml`,不让大模型通读运行报告转写(FR-008,Program-First)。
3. **一份新增的 tracked 按条目台账**(`.specify/teams/<slug>/items.jsonl`,每团队一份):承载跨运行的显式条目 ID 与可验证出处——因为实测证明 `STATE.md` 没有可确定性解析的结构、`run-log.jsonl` 只有按 cycle 的聚合计数且仅 continuous 模式具备、子代理结果清单位于 git-ignored 目录而不可作出处(见 [research.md](research.md) D-2)。
4. **一层 goal 身份与聚合**:goal 身份由 `team.md` frontmatter 显式声明的 `goal_slug` 承载(存量团队以 team slug 回填并标记推断),阶段按团队命名空间化,工作项归属由其出处路径前缀机器判定,同 goal 并发刷新串行化为一次(见 [research.md](research.md) D-7)。

Phase 0 已**实际执行**被调技能全链路(validate → load → check → engine)验证可行性:R 档三条完全可由团队 tracked 工件满足(exit 0,零人工补填),且引擎自身已兜住"不写 0%""无排期不出甘特"两条降级要求。同一次执行还反证出两条设计约束:条目 ID 受 DDL 字面量约束(中文标题不能当 ID),以及表单必须恒定产出 `coverage` 块否则落盘门禁 CG-COVERAGE 必 FAIL。

## Technical Context

**Language/Version**: Python 3(表单生成器与测试;项目基线 `>=3.8`,与既有 `scripts/python/` 一致)+ Markdown 提示层(技能与命令模板)
**Primary Dependencies**: 被调技能 `summarize-project` 的既有脚本链(`validate-project-input.py` / `project-db.py` / `progress-engine.py` / `check-coherence.py`)、`draw-plantuml`(渲染委托)、`sync-mirrors.py`(镜像同步);标准库 `json` / `hashlib` / `pathlib`,**不新增第三方依赖**
**Storage**: 纯文件。团队侧新增 tracked 的 append-only `.specify/teams/<slug>/items.jsonl`(每团队一份,运行信息);goal 侧交付目录 `.specify/project/goal/<goal-slug>/`(`summary.md` + `assets/` + `data/`,唯一完整总结);派生 SQLite `<goal-dir>/data/project.db` 由被调技能每次重建
**Testing**: `pytest`,markers `contract` / `integration`(见 `pyproject.toml`)。契约测试钉住台账 schema、ID 文法、goal 身份解析、状态行文法、写入面不变性;集成测试以四模式夹具团队跑通表单生成,并以"两团队共享一个 goal"夹具跑通聚合与并发串行化
**Target Platform**: 本地开发机 CLI(Linux / macOS),提示层由受支持的 AI agent CLI 解释执行
**Project Type**: 单体框架仓(code generator / framework 形态:`templates/` + `skills/` + `scripts/` + `src/specify_cli/`)
**Performance Goals**: 非延迟敏感。约束以**消耗**表达:总结步骤注入上下文的团队工件量在运行次数 K → 2K 时不翻倍(SC-005);continuous 默认节奏 MUST NOT 每 cycle 出图(FR-013);goal 侧只渲染一份总结,不因双索引而使出图成本翻倍
**Constraints**: `summarize-project` 零改动(FR-024/SC-003);总结步骤写入面仅限 goal 交付目录 + 反馈存量,`.specify/teams/**`、`.specify/agents/**`、`.specify/project/` 既有历史产物三者字节不变(FR-020 / FR-036 + 预置约束块);出处只指向 tracked 工件(FR-011);预算阶梯优先于节奏(FR-014);同 goal 并发刷新串行化、禁半写产物(FR-035)
**Scale/Scope**: 4 个存量团队(2 continuous + 2 iteration;serial/parallel 需夹具,跨团队聚合亦需夹具)、4 种协作模式 × 7 个项目管理实体的映射矩阵、5 个呈现层面、2 个索引维度;分解图节点阈值 15(CG-6)决定 FR-029 的聚合触发点

### Pre-seeded Constraints — Agent 三层重构对齐 (2026-08-04, authored ahead of /speckit.plan)

> 本块是手工预置的设计输入,非模板占位符:`/speckit.plan` 填充本文件时 MUST 保留并遵守,不得视为待替换内容。分类法真源:`.specify/shared/definitions/agent-definitions.md`;派发模式真源:`.specify/shared/definitions/subagent-definitions.md`。

- **名册解析(People 实体来源)**:团队 `members[]` 引用的 agent 定义位于分层存储 `.specify/agents/templates/<slug>.agent.md`(Agent Template,init 安装)与 `.specify/agents/instances/<slug>.agent.md`(Agent Instance,项目创建),同名时 instance 优先;表单生成器解析人员称名时 MUST 按此顺序取 frontmatter `name`(对应 FR-004)。旧平铺路径 `.specify/agents/<slug>.agent.md` 已废弃,设计中不得出现。
- **子代理 ≡ Agent Execution(第三层)**:团队派发的子代理是运行形态,不是文件;其持久产物(派发配置 `.specify/agents/execution/configs/<slug>.yaml`、包装脚本 `execution/scripts/`)是 tracked 的,**可**作为出处;运行日志 `execution/logs/`(含外部派发可见性三元组 `.live.log`/`.jsonl`/`.status`)已 gitignore,**不得**作为进度出处(对应 FR-011)。
- **触发点与派发的边界**:总结触发点嵌入团队执行流(create-team 执行引擎);若总结步骤本身以外部子代理方式派发,MUST 遵守外部派发可见性契约(stream-json + 过滤器 + 三元组,参考实现 `skills/create-team/scripts/dispatch.sh`),且其日志同样落在 git-ignored 位置。
- **写入面不变性的边界扩展**:总结步骤期间除事实源团队工件外,`.specify/agents/**`(三层全部)亦 MUST 保持字节不变——总结是纯派生步骤,不得触碰 agent 定义与派发配置。
- **术语纪律**:设计文档中提及 agent 时区分层级(Template / Instance / Execution),不用裸词 "agent" 指代文件与运行两种形态。

**本轮 Phase 0 对预置约束的执行结论**:五条全部采纳,无冲突。补充一条实测偏差待实现期收敛——`dispatch.sh` 的 `DISPATCH_LOG_DIR` 默认值是 `${TMPDIR:-/tmp}/spec-kit-dispatch`(仓库之外),与预置块所述 `.specify/agents/execution/logs/` 不一致;二者对 FR-011 的结论相同(均非 tracked、均不得作出处),差异仅在文档与代码的一致性,处置见 [research.md](research.md) § O。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, v1.9.0 — 13 principles):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每项设计决策在 [research.md](research.md) 中回指具体 FR(D-1→FR-018、D-2→FR-008/026、D-3→FR-026/027、D-4→FR-029、D-5→FR-012) |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 027;本轮推进 `features.md` 027 行 Draft→Planned 并在 `features/027.md` 记录计划要点 |
| III | Intent-Driven Development | ✅ Pass | 规格只述 what/why;本 plan 承载 how;多步细化(requirements → clarify ×5 → research → plan) |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 本特性含可执行代码(表单生成器),故按常规判定而非模板豁免:4 份契约先行 + `tests/contract/` 钉住台账 schema/ID 文法/状态行文法/写入面不变性,`tests/integration/` 四模式夹具;Phase 0 已建立执行基线 |
| V | AI Agent Integration Standards | ✅ Pass | 不新增/不改动受支持 agent 清单;`templates/commands/team.md` 的 5 份 per-tool 副本经 `regen-command-copies.py` 统一再生(见 Mirror Obligations) |
| VI | Continuous Quality & Observability | ✅ Pass | FR-015 的运行报告状态行 [[STR-005]] 使"未观测"与"观测到无进展"可区分;台账为结构化 append-only 事件流 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 本轮只推进 Draft→Planned(Implemented 归 `/speckit.implement`);Workflow Gates (NON-NEGOTIABLE) 的 Feature reuse-first 已满足(复用 027,未新建 Feature);未出现状态回退 |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 结论均来自 DDL/源码/**实际执行**;三条文档声明经执行修正或补强(ID 文法、`coverage` 恒产、`STATE.md` 无 schema),见 research.md § E |
| IX | Framework Scope Discipline (No Over-Engineering) | ⚠ Partial — see Complexity Tracking | 新增两类工件(1 支生成器脚本 + 1 份 per-team 台账);二者均由 FR-008/FR-026 强制且有实测反证支撑,但确实超出"纯模板/提示"形态 → 见 Complexity Tracking |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新增路径全为小写(`summary/`、`items.jsonl`、`summary-mapping.md`);未占用保留 ALL-CAPS 名;`.specify/teams/` 不属受管文档空间(项目根 + `docs/`) |
| XI | Dogfooding (Self-Application) | ✅ Pass | 本特性经自身 SDD 流程落地;且其产物正是让本项目 4 个存量团队获得可观测性——用自己的机制观测自己的团队 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 已查 `.specify/memory/tools/`(4 条 Verified:evidence-utils / feedback-utils / refresh-tools / sync-mirrors),无一覆盖"从团队工件派生项目表单" → 按 Principle XII"无 Tool 则写代码是预期结果";实现后 SHOULD 提名晋升为 Tool |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Change Validation(团队状态可被验证而非自述)与 Learning Capture(累积台账供 `improve-team` 取证);未新增评分/成熟度报告系统 |

**Gates Status**: ✅ All gates pass — 唯一非 Pass 行(IX)为 ⚠ Partial 且已在 Complexity Tracking 登记justification,无未经论证的违规。

**Re-check after Phase 1**: 2026-08-04 — Phase 1 产出(data-model.md、4 份契约、quickstart.md、feature-ref.md)落盘后按同表复核,结论不变:13 行中 12 Pass、1 Partial(IX)。契约阶段新增两点强化证据——(a) IV 的契约先行已具体化为 4 份可测契约 + 每条 CLI 示例经真实执行验证;(b) VIII 因 Phase 1 又发现一条文档—代码偏差(`coverage` 恒产要求无对应 FR)并记入 research.md § O,未静默吞掉。IX 的 Partial 判定与理由未变。

**Re-check after the 2026-08-04 scope revision(双索引)**: 逐行重评 13 条,结论仍为 12 Pass / 1 Partial(IX),但两行的证据发生实质变化,故明示而非沿用——
- **II Feature-Centric**:修订新增 FR-030…FR-036 与 US6,改动面仍全部落在 Feature 027 的团队域内(团队配置 schema、执行流触发点、团队产物布局);`.specify/project/goal/` 是产物落位而非新能力域,故**不新建 Feature**,符合 reuse-first 门禁。
- **IX Framework Scope Discipline(仍 Partial)**:修订未新增第三类工件——`goal_slug` 是既有 frontmatter 的一个字段、交付目录是既有 tracked 目录下的子树、聚合与串行化是生成器内的逻辑。Partial 的成因仍只是既有的"1 支脚本 + 1 份台账"两项,理由与 Complexity Tracking 中的论证一致;并发串行化刻意复用既有的"只由团队主管写入"纪律(FR-021)而非引入锁服务或调度器。
- **VIII Code as SSoT**:修订前实测了 `.specify/project/` 的真实内容(10 个 tracked 文件,`manage-project` 时代遗留),据此写成 FR-036 的共存约束,而非假定该目录为空。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/036-team-summary/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — 执行验证 E-1…E-6 + 设计决策 D-1…D-6 + 遗留 § O
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command) — 4 份契约
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── checklists/
│   └── requirements.md  # 规格质量清单(/speckit.requirements + clarify 复验)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

`research.md` 以独立文件产出(Phase 0 含 6 条执行验证与 6 条决策,远超 ~50 行内联阈值,且包含对被调技能脚本链的实测输出)。

### Source Code (repository root)

**镜像说明(2026-08-04 agent 重构,承接上游预置备注)**:agents 的镜像对现为 `agents/` ↔ `.specify/agents/templates/`(由 `sync-mirrors.py` 维护);`instances/` 与 `execution/` 是项目本地产物,**从不镜像**。本规格不改动 agents 任何层,该说明仅用于界定"不得触碰"的范围。

```text
skills/create-team/                 # 团队域主改面:触发点、映射事实源、表单生成器
skills/create-team/references/      # + summary-mapping.md(新增,FR-001 概念映射单一事实源)
skills/create-team/scripts/         # + build-summary-input.py(新增,FR-008 确定性表单生成器)
skills/improve-team/                # config.summary 的调参入口(节奏/开关/交付目录)
templates/commands/team.md          # run 模式:确认门禁披露总结成本 + 触发点收口
skills/create-team/templates/teams/ # 三份预设按模式声明 config.summary 默认节奏
tests/contract/                     # 台账 schema / ID 文法 / 状态行文法 / 写入面不变性
tests/integration/                  # 四模式夹具团队 → 表单生成 → 装载校验全链路
tests/fixtures/                     # serial / parallel 夹具团队 + 共享同一 goal 的双团队聚合夹具
```

运行期数据(非源码,不在上表):每个团队的 `.specify/teams/<team-slug>/items.jsonl`(新增 tracked 台账,team 索引)与每个 goal 的 `.specify/project/goal/<goal-slug>/`(交付目录 [[STR-001]],goal 索引,唯一完整总结)。

**Structure Decision**: 沿用本仓既有的 **code generator / framework** 形态,不新增顶层目录。改动集中在团队域的 `skills/create-team/`(1 份新 reference + 1 支新脚本 + SKILL.md 若干节)与命令模板 `templates/commands/team.md`,并按既有 `tests/{contract,integration,fixtures}/` 布局补测。新增的两个**数据**面分处两个索引:`items.jsonl` 落在 `.specify/teams/<team-slug>/` 之内(需同步修订"团队目录只放 `team.md` + `runs/`"这一既有断言——该断言当前已与 continuous 团队实况不符),交付目录落在既有且 tracked 的 `.specify/project/` 下新增的 `goal/` 子树(与其现存的 `project.md` + wbs/gantt/milestones 历史产物平级共存,不得覆盖,FR-036)。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/team.md` | `.specify/templates/commands/team.md`; `.claude/commands/speckit.team.md`; `.github/prompts/speckit.team.prompt.md`; `.qoder/commands/speckit.team.md`; `.qwen/commands/speckit.team.toml`; `.opencode/command/speckit.team.md` | `sync-mirrors.py --check`(exit 2 = drift);6 份副本均含"总结披露"与新目录断言 |
| `skills/create-team/SKILL.md` | `.specify/skills/create-team/SKILL.md` | `diff -q`;两侧同含 SUMMARIZE 相与修订后的输出纪律 |
| `skills/create-team/references/summary-mapping.md`(新增) | `.specify/skills/create-team/references/summary-mapping.md` | `diff -q`;文件在两侧均存在 |
| `skills/create-team/scripts/build-summary-input.py`(新增) | `.specify/skills/create-team/scripts/build-summary-input.py` | `diff -q`;两侧均可执行且 `--help` 一致 |
| `skills/improve-team/SKILL.md` | `.specify/skills/improve-team/SKILL.md` | `diff -q` |
| `skills/create-team/templates/teams/{artifact-optimizer,process-monitor,workspace-cluster}.md` | `.specify/skills/create-team/templates/teams/*.md` | `diff -q` 三份预设 |

统一入口:改动任一 canonical 源后运行 `python3 scripts/python/sync-mirrors.py --write`,再以 `--check` 验证(Tool 记录 `<TOOL:.specify/memory/tools/sync-mirrors.py.md>`)。**不得**手工编辑任何镜像或 per-tool 副本(生成副本带 `AUTO-GENERATED` 头)。

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 新增可执行脚本 `build-summary-input.py`(超出纯模板/提示形态,Principle IX) | FR-008 明令表单由**确定性程序**派生、禁止大模型通读运行报告转写;SC-005 要求注入量不随运行次数线性增长。二者只能由程序满足 | *让提示层直接读团队工件写表单*:实测 `run-log.jsonl` 与 `runs/` 随运行次数累积,提示层读取即线性增长,直接违反 SC-005;且大模型转写无法保证 ID 文法与出处非空(实测 DDL 会以 exit 3 拒绝) |
| 新增 per-team tracked 数据文件 `items.jsonl`(新数据面,Principle IX) | FR-026 要求条目 ID 落在机器可读工件;FR-010/FR-011 要求每个数值有 tracked 出处 | *复用 `STATE.md`*:实测两个 continuous 团队分节名与形态完全不同(散文 vs 状态桶),无共同 schema 可解析。*复用 `run-log.jsonl`*:仅 continuous 具备,且只有按 cycle 聚合计数、无逐条目身份。*复用子代理结果清单*:位于 git-ignored `.work/`(外部派发三元组更在仓库之外),FR-011 禁止作出处 |
