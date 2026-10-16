# Implementation Plan: 「驱动子代理」机制的技能化分解与公用化（decompose-subagent-dispatch）

**Branch**: `060-decompose-subagent-dispatch` | **Date**: 2026-10-16 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `060-decompose-subagent-dispatch` → Feature 060 「驱动子代理」机制的技能化分解与公用化
**Input**: Specification from `.specify/specs/060-decompose-subagent-dispatch/requirements.md`

## Summary

把 sdd-loop-driver 与 sdd-project-setup 各自内联的「驱动子代理」机制按 057 技能化分解方法上收为公用机制：深化 Agent 三层分类法（Template→Instance→Execution）的层界语义于两份既有真源，增强 create-agent/improve-agent/run-agent 三技能承接面（新增 `agents/sdd-executor.agent.md` 能力模板、多职责实例化、Execution 拓扑声明与冲突拒收、五族前置检查表与失败处置链上收、反嵌套治理上收），两技能机制段坍缩为引用并按义务平价映射逐条对账。交付面全部为 Markdown 制品 + 结构契约测试，无运行时代码。FR-012 真源归属已在 clarify 裁定（见 requirements.md FR-012），本 plan 直接拆解、不重裁。

## Technical Context

**Language/Version**: Markdown 制品（技能体/真源/契约）；契约测试为 Python 3.14 + pytest（仓库既有 tests/contract/ 体系）
**Primary Dependencies**: 既有真源文档（agent-definitions.md、subagent-definitions.md、external-dispatch-recipes.md、fast-fail.md）；sync-mirrors.py（镜像引擎）；probe-utils.py compile-embeds（编译面）；specify render-agents（agents/ 渲染管线，`_AGENT_METADATA_MAPPING`）
**Storage**: 无数据库——制品即文件（技能体、模板、实例、执行配置 yaml 沿用既有 `.specify/agents/execution/configs/` 形态）
**Testing**: pytest contract 标记；新增 `tests/contract/test_agent_dispatch_mechanism.py`（条款一测试，`test_sdd_loop_driver_skill.py` 扁平先例形态）；既有套件 name-level 零新增失败
**Target Platform**: 技能/提示词框架层——宿主 agent 按技能体执行，无运行时进程
**Project Type**: 框架源（两顶帽子：改动全部落框架源 `skills/`、`agents/`、`shared/`，镜像经 sync-mirrors 同步）
**Performance Goals**: N/A（Markdown 制品；可观测性义务由可见性契约与前置检查记录承载）
**Constraints**: FR-012 归属不重裁（Session 2026-10-16 裁定）；编排本体不外移（FR-013）；`/speckit.team` 与 create-team 体系零改动（FR-015）；既有漂移 1 条（instructions-template.md 镜像 DIFF）不属本特性修复面，Verify 用相对判据
**Scale/Scope**: 14 个交付面文件（feature-ref.md 交付清单）；契约条款与平价映射计数由 `contracts/` 制品承载（`clause_extract` 可派生），本文不复写

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**（动态枚举自 `.specify/memory/constitution.md`，16 项；初步自评，同作者门委派复核结果见下文 Re-check 记录）:

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 全部设计决策溯源 requirements.md FR-001..016（feature-ref.md 映射表逐行） |
| II | Feature-Centric Development | ✅ Pass | Feature 060 已注册（features.md + features/060.md），绑定 1:1，plan 不改状态越权 |
| III | Intent-Driven Development | ✅ Pass | 三层语义按"能做什么/为谁做什么/在哪怎么跑"意图分层，未跳到实现细节 |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | 交付面为 Markdown 制品（template-only 形态），依 VII 门判 Partial（正当化）；结构契约测试覆盖契约全条款（计数见 Phase 1 Summary 及其派生命令） |
| V | AI Agent Integration Standards | ✅ Pass | CLI 集不变（qodercli/claude，A3 排除新增）；渲染经既有 `_AGENT_METADATA_MAPPING`，无 provider 变更 |
| VI | Continuous Quality & Observability | ✅ Pass | 反嵌套/可见性三元组/前置检查记录承载可观测性；新行为已反映 spec/plan/contracts |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass (NON-NEGOTIABLE gates) | 特性注册先于 plan；状态 Draft→Planned 由本 plan 推进，不越权 Implemented |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 勘探以源码实测校准（渲染管线/镜像对/先例测试形态均为代码事实，非文档转述） |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 全部交付为提示词/文档/结构测试；无运行时引擎、无调度器、无新存储（退役为状态标记非新子系统） |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新文件走既有命名面（SKILL.md 强制名、references/ 小写、docs/reference/skills/ 惯例路径） |
| XI | Dogfooding (Self-Application) | ✅ Pass | 机制修复落框架源侧（两顶帽子：skills/ 源改、镜像同步）；副本坍缩本身即修复机制侧 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 sync-mirrors/probe-utils/render-agents 既有引擎；前置检查上收是语义搬家非新工具 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Controlled Execution 维度（派发义务公用化）与 Learning Capture 维度（证据回流）；引用 better-harness 锚不另立目标 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 本特性是 XIV 的直接执行：副本坍缩单 owner（SC-003），真源深化只入既有两文档（FR-001），配方引用不复制（R-5） |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 委派说明段面向未读真源的宿主自足（C-34 条款直指）；quickstart 每命令带前提与免责 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 冲突拒收（C-16）、反嵌套派发前拦截（C-20）、前置检查失败处置链（C-17）皆为该纪律的实例化；既有漂移披露不静默修 |

**Gates Status**: ✅ 全部通过——唯一 ⚠（IV）为 VII 门明文允许的 template-only 正当化形态，见 Complexity Tracking。

**Re-check after Phase 1**: 2026-10-16——Phase 1 产物落盘后复核：IV 维持 Partial（契约测试落位方式不变）。同作者门委派 fresh-context 只读评分者对 16 行独立评分：**16/16 判定一致**（IV Partial 正当化成立，IX/XIV 抽查无真源复制），Quality Gate 复核合规（审议标记零命中、quickstart execution-verify 合规、契约全声明性）；回报 2 处纠正级计数漂移已顺手修复并披露：契约条款实数 34 非 31（A/R/I/X 实为 17 非 14，plan 四处）、data-model 校验规则实数 13 非 12（V-E1×3+V-E2×3+V-E3×3+V-E4×2+V-E5×2）。另有论证级 2 项记录：E4 表为实现期 dated record（实现后不得当现状引用）、pytest 基线为实现期复测义务。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/060-decompose-subagent-dispatch/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # 无独立文件——Phase 0 发现内联于本文件 § Phase 0（<50 行且全内部证据）
├── requirements.md      # /speckit.requirements 产物（已澄清）
├── checklists/requirements.md  # 质量清单（clarify 后复绿）
├── data-model.md        # Phase 1 output — 6 实体（E1–E6）+ 校验规则
├── quickstart.md        # Phase 1 output — 5 场景（3 实跑基线 + 2 逐条免责）
├── contracts/           # Phase 1 output — 3 文件 35 条款
│   ├── concept-and-sources.md      # C-1..C-8：真源深化
│   ├── skill-enhancements.md       # C-9..C-25：三技能承接面
│   └── delegation-parity.md        # C-26..C-35 + P-01..P-15：委派化与义务平价
├── feature-ref.md       # Phase 1 output — FR/SC 映射 + 交付清单 + 基线记录
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md     # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
agents/                                    # 新增 sdd-executor.agent.md（SDD 执行者能力模板，框架分发角色集）
skills/internal/create-agent/              # SKILL.md 增强：内容判据 + 多职责实例化 + 退役生命周期
skills/internal/run-agent/                 # SKILL.md 增强：拓扑输入 + 冲突拒收 + 反嵌套义务
skills/internal/run-agent/references/      # 新增 dispatch-preflight.md（五族检查表+处置链上收落点）
skills/internal/improve-agent/             # SKILL.md 增强：执行证据输入形态
skills/external/sdd-loop-driver/           # 委派化：SKILL.md + dispatch-recipes.md + stage-prompts.md 机制段坍缩
skills/external/sdd-project-setup/         # 委派化：setup-recipes.md S4 清零引用 + 远端形态引用
.specify/shared/definitions/               # agent-definitions.md / subagent-definitions.md 扩格
docs/reference/skills/                     # 两技能 docs 页更新（机制归属说明）
tests/contract/                            # 新增 test_agent_dispatch_mechanism.py
```

**Structure Decision**: 本特性落在既有框架源布局内，无新顶层目录——能力模板入既有 `agents/` 角色集（现有 skill-verifier/structure-adjuster 两文件的兄弟位），前置检查以新文件入 run-agent 的 references/ 面，真源深化入既有 shared/definitions/ 两文档。

### Mirror Obligations *(mandatory)*

同步引擎：`scripts/python/sync-mirrors.py`（MIRROR_PAIRS 实测：skills/internal(135)/agents(2)/scripts(108)/shared(49)/skills(external↔flat) 五对）。**基线漂移（2026-10-16 实测）**：`.specify/templates/instructions-template.md` 存在 1 条既有 DIFF——不属本特性触碰对，Verify 全部用相对判据。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `agents/sdd-executor.agent.md`（新增） | `.specify/agents/templates/sdd-executor.agent.md` | `sync-mirrors.py --check` agents 对零 NEW drift；渲染面由 `specify render-agents --ai <tool>` 生成（.qoder/agents/ 等，入 render-manifest） |
| `skills/internal/{create-agent,run-agent,improve-agent}/**` | `.specify/skills/internal/<name>/**` | sync-mirrors internal 对零 NEW drift |
| `skills/external/{sdd-loop-driver,sdd-project-setup}/**` | `.specify/skills/<name>/**` | sync-mirrors skills 对零 NEW drift |
| `.specify/shared/definitions/{agent-definitions,subagent-definitions}.md` | `.specify/shared/definitions/` 同名（shared 对） | sync-mirrors shared 对零 NEW drift |
| 契约测试 `tests/contract/test_agent_dispatch_mechanism.py` | 无镜像（tests/ 不在 MIRROR_PAIRS） | pytest 直跑 |
| 各 SKILL.md 的编译 `## Wrap-up` 面 | 由 probe-utils compile-embeds 维护（unit 认领随 scan） | `compile-embeds --check` 零漂移（新增文件若被 scan 认领则先注册后编译） |

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| IV Test-First 判 ⚠ Partial | 本特性交付面为 Markdown 制品（技能体/真源/模板），无纯函数与运行时行为可单测；按宪法 VII 门"template-only features judge Test-First as Partial (justified)"处理 | 把技能体改写为可执行运行时以换取"完整单测覆盖"——违反 IX（框架非运行时平台），且 058 先例已确立"结构契约测试承载条款验证"的形态（契约全条款测试仍会写，test-first 红绿对 Markdown 结构可行） |

## Phase 0: Research Review

无独立 research.md——发现内联（全内部证据，2026-10-16 勘探实测，Explore 子代理执行、ANOMALY 无）：

- **副本重复精确映射**（Phase 0 核心输入）：loop-driver R0≈STR-006 R1（断点探测）、R1≈R2（提示词文件）、R2≈R3（runner 派生，loop-driver 多心跳机制）、R3≈R4（后台+轮询，loop-driver 独有 nohup 脱离形态与定间隔分级）、R5≈R5+R6（本地+角色分线）；R4 阶段链收尾为 loop-driver 独有。setup-recipes S4 五族表≈loop-driver Preflight；软协同契约与对方 handoff 段互为镜像。
- **前置检查不在配方真源**：external-dispatch-recipes.md 六配方确认无五族检查表——FR-012 裁定（检查表→run-agent）为净新增归属，无既有 owner 冲突；配方文档"只有 how"边界维持不变。
- **渲染管线事实**：agents/ 现有 2 角色文件；`_AGENT_METADATA_MAPPING`（src/specify_cli/__init__.py）按工具渲染 frontmatter（qoder: model-tier→model、capability-tools→tools、run-turn-budget→maxTurns）；渲染产物为实体文件+render-manifest 清单；codex/hermes 仅 annotated。
- **先例形态**：契约测试两种并存（sdd_loop_driver 扁平逐条款 / exec_quant 类分组+fixture）——060 取扁平形态（条款为 Markdown 结构断言，无 fixture 需求）；create-team 席位实例化先例（占位符全解析+专用溯源键）为多职责实例化的直接参照（capacity-scope 对应 team-scope 位）。
- **既有漂移**：sync-mirrors --check 报 `.specify/templates/instructions-template.md` DIFF 1 条——与本特性无关（不触碰该对），披露并采用相对 Verify 判据。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 6 实体（E1 模板 / E2 实例 / E3 拓扑声明 / E4 前置检查记录 / E5 义务集 / E6 平价映射）+ 13 条校验规则（V-E1×3 + V-E2×3 + V-E3×3 + V-E4×2 + V-E5×2） |
| Contracts | [`contracts/`](contracts/) | 3 文件：concept-and-sources.md（C-1..C-8）+ skill-enhancements.md（C-9..C-25）+ delegation-parity.md（C-26..C-35 + P-01..P-15 义务平价映射）。条款计数以 `clause_extract` 派生为准：`python3 -c "import sys; sys.path.insert(0,'.specify/scripts/python'); from clause_extract import extract_clauses; [print(f, len(extract_clauses('.specify/specs/060-decompose-subagent-dispatch/contracts/'+f))) for f in ['concept-and-sources.md','skill-enhancements.md','delegation-parity.md']]"`——2026-10-17 实跑：8 / 17 / 10，合计 35 |
| Quickstart | [`quickstart.md`](quickstart.md) | 5 场景（S1–S3 实跑留痕 / S4–S5 逐条免责+前提清单） |
| Feature ref | [`feature-ref.md`](feature-ref.md) | FR 16/16 映射 + SC 6/6 映射 + 14 项交付清单 + 基线记录 |

Phase 0 预期 vs 实际：实体数 6（预估 5–7 ✓）；契约文件 3（预估 2–3 ✓）；quickstart 场景 5（预估 4–5 ✓）；无漂移需修正项。
