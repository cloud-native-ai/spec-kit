# Implementation Plan: 无人值守 SDD 循环驱动机制（Unattended SDD Loop Driver）

**Branch**: `058-sdd-loop-driver` | **Date**: 2026-10-15 | **Spec**: `.specify/specs/058-sdd-loop-driver/requirements.md`
**Requirement → Feature**: `058-sdd-loop-driver` → Feature 058 无人值守 SDD 循环驱动机制
**Input**: Specification from `.specify/specs/058-sdd-loop-driver/requirements.md`

## Summary

以**一个自包含、可移植的 Spec Kit skill（`sdd-loop-driver`，external 分类）**承载无人值守 SDD 循环驱动的全部机制：阶段提示词三段骨架、五大执行机制（断点探测 / 阶段化 prompt 文件 / runner 与派生 / 后台执行+日志轮询 / 收尾纪律）、已验证变体、纪律条款，以及自迭代 / 独立校验 / 卡死处置三硬需求的运行规则（G1 修订裁决：Team 承载被取代，skill 唯一承载，执行侧零 `.specify/` 依赖）。交付面：`skills/external/sdd-loop-driver/`（SKILL.md + references/）＋框架镜像、docs 参考页、结构契约测试；无 preset、无 team、无新引擎脚本（Principle IX 最小面）。技术路径全部继承 2026-10-14 多项目实测形态（简报 §3–§5）与 2026-10-15 已沉淀的 shared 模式/配方文档（`shared/patterns/unattended-loop-pattern.md`、`shared/workflow/external-dispatch-recipes.md`——作为撰写底稿内联进 skill，不作为运行时依赖）。

## Technical Context

**Language/Version**: Markdown（SKILL.md + references/）+ YAML frontmatter（既有外部技能四字段惯例：`name` / `description` / `skill_id` / `classification: external`，实测先例 `skills/external/create-skills/SKILL.md`、`skills/external/git-workspace/SKILL.md`）
**Primary Dependencies**: `sync-mirrors.py`（既有 MIRROR_PAIRS：`skills/external → .specify/skills` 平铺，实测 :82-89）；pytest（契约测试，markers `contract`/`integration`，`pyproject.toml [tool.pytest.ini_options]`）；**无新运行时引擎**（派发/轮询由 skill 指挥宿主 agent 的既有 shell 能力完成，`DISPATCH_CLI`/`dispatch.sh` 为 skill 内容引用的既有参照物，不修改）
**Storage**: N/A（机制无运行时存储；运行期制品——阶段提示词文件、runner、线状态、收尾汇总——由 skill 在目标项目/宿主侧按 data-model 的 schema 落盘，schema 本身是 skill 内容的一部分）
**Testing**: pytest 契约测试（结构钉死：frontmatter 字段、章节集、自包含断言、镜像一致、docs 页面接线——先例 `tests/contract/test_run_skills_wiring.py` 逐条款一测形态）＋真实演练 dogfood（SC-001…SC-009 的验收载体，两态标注：已执行 / 实现后验证）
**Target Platform**: 任意宿主 agent CLI（Claude Code / Qoder CLI / Codex CLI / GitHub Copilot / opencode / Hermes——skill 宿主中立，SC-009 零框架环境）；被驱动子代理所在目标项目需 `.specify/`（执行 `[[STR-002]]` 阶段命令）
**Project Type**: template-only 文档/知识特性（零可执行运行时代码——Principle VII template-only 门适用，Tests Mode 取结构契约形态）
**Performance Goals**: N/A（人工驱动的编排知识，无吞吐量纲；性能相关量纲仅存在于运行期缺省值——阶段超时 90 分钟 / 重试上限 2 次，属 skill 内容参数而非本仓性能指标）
**Constraints**: ① 自包含硬约束（执行侧无法解析框架文档路径——FR-002 内联义务、SC-009 零依赖）；② 投递形态无关（FR-025：三形态等价，无下载/版本化机制）；③ 零新确认门控与零门控预算扰动（`scan-confirmation-gates.py` 仅扫 `templates/`，`SCAN_ROOT_FILES=("templates",)`，skill 文案不在扫描面，total 23 不变）；④ 双顶帽子：改框架源 `skills/external/`，镜像经 sync-mirrors 投影，禁直接手改 `.specify/skills/`（Principle XI）
**Scale/Scope**: 1 个 skill（SKILL.md + 2 个 references）＋ 1 个 docs 参考页 ＋ 1 个契约测试文件（含既有 `test_run_skills_wiring.py` 的 external 名册基线更新）＋ 1 个 docs 页接线；25 FR / 9 SC / 6 US

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**（动态枚举自 `.specify/memory/constitution.md` v1.13.0，16 项；评分为初步判定，同作者条件成立——评分委派 fresh-context 子代理复核，见 Complexity Tracking 前注）:

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 25 FR 逐条映射 Phase 1 契约条款（feature-ref.md）；设计继承 spec 裁决（G1 修订/G3/G4/G5/G6） |
| II | Feature-Centric Development | ✅ Pass | Feature 058 已注册（features.md 行 + features/058.md），plan 推进 Draft→Planned；无新 Feature、无既有失效（US1–US6 全落 058 范围） |
| III | Intent-Driven Development | ✅ Pass | spec 以 6 个 user story 表达 what/why；plan 不引入 spec 外的 how（skill 内容全部溯源简报 §3–§5 与 shared 底稿） |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | template-only 门（零可执行运行时代码，宪法 :117 明文豁免形态）：测试为结构契约（tests/contract/ 逐条款）+ 真实演练 dogfood，非单元/集成代码测试 |
| V | AI Agent Integration Standards | ✅ Pass | 零新增 agent 面/配置解析；qodercli 为 skill 内容参数（`DISPATCH_CLI` 可覆盖），不触 AGENT_CONFIG 名册 |
| VI | Continuous Quality & Observability | ✅ Pass | 状态脊（FR-019）即运行期可观测面；本特性零运行时组件、零版本化面；YAGNI——无 speculative 机制 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 工作流在轨（requirements→clarify→plan）；Workflow Gates：Feature reuse-first ✓（绑定 058）、无状态回退（Draft→Planned）、Pre-Status-Flip 留待 implement |
| VIII | Code as the Single Source of Truth | ✅ Pass | 勘探实测为准：MIRROR_PAIRS :82-89、frontmatter 四字段先例、`.specify/skills.md` 非注册表（自述）、`SCAN_ROOT_FILES=("templates",)` 均以代码/文件实测引用，不引文档记忆 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 交付面 = 文档/提示词制品（skill + docs 页 + 契约测试），零运行时调度器/执行引擎/下载平台；FR-025 显式排除投递机制——本原则是 G1 修订选型的决定性判据 |
| X | Documentation Naming & Location Conventions | ✅ Pass | `skills/external/sdd-loop-driver/SKILL.md` 为工具裁定名（豁免保留名，MUST 按此形态）；docs 页落 `docs/reference/skills/sdd-loop-driver.md`（小写、语义路径）；无新增保留名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子：交付落框架源 `skills/external/`（publish→install→init 抵达下游），`.specify/skills/` 仅经 sync-mirrors 投影；本特性自身经本 SDD 流程演进（自应用在轨） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 镜像同步复用既有 sync-mirrors（不新建传播器，FR-024）；无一次性脚本生成面 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化维度显式记录于 feature-ref.md：Controlled Execution（阶段化派发+独立校验）与 Reliable Delivery（收尾纪律+状态脊） |
| XIV | One Source of Truth (Authority & Reference Discipline) | ⚠ Partial — see Complexity Tracking | skill 内联框架纪律操作要点与 shared 文档内容——物理自包含约束下内联是唯一可行形态（执行侧零依赖）；以契约测试钉死关键操作字面量，shared 文档声明为撰写底稿而非运行时真源 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | docs 参考页面向人类读者（按 XV 判据撰写）；SKILL.md 面向执行 agent（XV 界面类封闭集不含 agent 手册）；一遍性入口话术不变（G4） |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | skill 内联 052 异常分流操作要点（FR-018，C-7）与派发注入义务（宪法 XVI：每派发回传哨兵或显式异常行——C-13 内联操作文本 + E-4 回传契约）；本 plan 自身按门执行（可写性探测已过、示例执行核验在质量门） |

**Gates Status**: ⚠ 两项 Partial（IV、XIV）均带 Complexity Tracking 论证；无 Fail。

**Re-check after Phase 1**: 2026-10-15 — fresh-context 子代理逐行复验完成（明细见 Complexity Tracking 复核结论）：16 行中 15 维持、XVI 缺承载降级后修复恢复 Pass；两行 Partial 论证经受独立复核维持。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/058-sdd-loop-driver/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md     # Implementation output (/speckit.implement command)
```

No standalone research.md — findings inlined below（Phase 0 结果 < 50 行且全部仓库内部实测）。

### Source Code (repository root)

```text
skills/external/sdd-loop-driver/   # 新增：skill 本体（SKILL.md + references/）——框架源侧唯一新目录
├── SKILL.md                       # 入口手册：循环总览（U0–U6）、frontmatter（external）、路由到 references/
└── references/
    ├── dispatch-recipes.md        # 五大执行机制的命令形态（断点探测/prompt 文件/runner 派生/后台轮询/收尾）
    └── stage-prompts.md           # 阶段提示词三段骨架 + 已验证变体 + 纪律条款 + 卡死处置/状态脊程序
docs/reference/skills/sdd-loop-driver.md  # 新增：docs 参考页（双拓扑实例化指引、执行侧可移植性说明——FR-024）
tests/contract/test_sdd_loop_driver_skill.py  # 新增：结构契约测试（逐条款）
tests/contract/test_run_skills_wiring.py      # 修改：BASELINE_EXTERNAL 名册基线加 sdd-loop-driver（勘探实测：该清单钉死 external 技能集）
.specify/skills/sdd-loop-driver/   # 仅经 sync-mirrors 投影（禁手改）
```

**Structure Decision**: 在既有 external 技能家族（11 个先例，`skills/external/<name>/{SKILL.md,references/}` 形态，实测 create-skills 同构）中新增一员并同步既有镜像/测试/文档接线——无新顶层目录、无新引擎、无 preset/团队面；`.specify/skills.md` 无需编辑（自述"非注册表"，发现靠目录扫描，勘探实测确认）。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/external/sdd-loop-driver/SKILL.md` + `references/*.md` | `.specify/skills/sdd-loop-driver/SKILL.md` + `references/*.md`（sync-mirrors external 对平铺投影；实测 MIRROR_PAIRS :82-89） | 改前基线测得（`sync-mirrors.py --check --only skills/external/sdd-loop-driver`，新文件对首跑应报 MISS→写入后 0 DIFF）；判据 = 触及对无 NEW drift，非绝对全绿 |
| `tests/contract/test_run_skills_wiring.py`（名册基线行） | 无镜像（测试文件无副本）；但其 pinned 名册与 `skills/external/` 实际目录强耦合 | 该测试自身转绿即判据（roster 与目录集合相等断言） |
| `docs/reference/skills/sdd-loop-driver.md` | 无镜像（docs/ 无镜像对） | 文件存在 + 契约测试接线断言 |

**BASELINE DRIFT 披露**: 既有全仓镜像基线存在无关漂移（053 特性记录：`sync-mirrors --check` 全树 exit 2 系无关 git-fleet 镜像缺文件）；本表判据一律取"触及对无 NEW drift"，禁止绝对全绿判据。

## Complexity Tracking

> 同作者评分前注：Constitution Check 初判由本会话（同作者）作出，按 objective-analysis-gate 已委派 fresh-context 子代理逐行复核；子代理结论与本表不一致处以下文「复核结论」行为准。

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| IV ⚠ Partial（template-only 门，宪法 :117 明文豁免形态） | 零可执行运行时代码——交付物是 SKILL.md/references/docs 页/契约测试，无单元/集成代码测试对象 | 加一个"可执行内核"换 Pass 正是 Principle IX 禁止的投机基础设施；结构契约 + 真实演练 dogfood 是该门明文豁免形态（051/053 先例） |
| XIV ⚠ Partial（skill 内联框架纪律与 shared 文档内容） | 自包含硬约束（FR-002/FR-011/FR-018；SC-009 零依赖）使执行侧无法解析框架路径——内联是物理唯一可行形态 | 三类合法副本（机器再生/测试钉死/日期化记录）皆不适用此形态，但引用真源在执行侧物理不可达；缓解 = 契约测试钉死关键操作字面量（052 四要素、禁止缓冲至退出式派发、G5 纪律行）+ shared 文档标注为撰写底稿。这是"reference 不可达"约束下的受控例外，非第二真源（框架侧 owner 对框架上下文仍唯一） |

**复核结论**（fresh-context 评分子代理，2026-10-15）：16 行逐行复验——**15 行维持**（子代理实测复核了全部承重代码引用：MIRROR_PAIRS :84、SCAN_ROOT_FILES :36、BASELINE_EXTERNAL :28、宪法 :117/:181 原文）；**1 行降级后修复**：XVI 初判 Pass 的证据含无承载子句（「派发注入义务」全规格零条款钉死、E-4 骨架缺异常回传行）→ 诚实降级 Partial（承载物 = contracts/skill-structure.md）；修复 = 新增 **C-13**（注入义务内联 + 回传契约）与 E-4 骨架回传契约注记，承载具名后恢复 Pass。Gates Status 随之：无 Fail、2 Partial（IV、XIV）。**ANOMALY 顺手修复**：IV 行原引「Principle VII :95」为 051 时代陈旧指针（v1.13.0 实文在 :117），已订正。

**Re-check after Phase 1**: 2026-10-15 — 上述 fresh-context 逐行复验即本次设计后复核；结论 15 维持 + 1 修复后 Pass，两行 Partial 的 Complexity Tracking 论证经受住独立复核（XIV 缓解栏经子代理确认落入"literal pinned in a test"合法副本形态的逐条款应用）。

## Phase 0: Research Review

**Information Gathering**（无独立 research.md——发现内联于此）：

- **D-1 交付落位**：external 技能家族实测 11 个先例（`skills/external/{create-docs,create-pages,create-skills,database-utils,document-utils,draw-diagram,git-workspace,improve-docs,improve-skills,merge-skills,think-skills}`），形态 `SKILL.md + references/`（create-skills 同构）＋可选 scripts/。本特性取 SKILL.md + 2 references（零 scripts——机制无引擎，命令形态全部内联文档化）。镜像：`skills/external → .specify/skills` 平铺（`{"site","internal"}` 排除集，lenient）。
- **D-2 frontmatter 契约**：四字段 `name` / `description`（长描述 + 触发词列表）/ `skill_id: "<SKILL:.specify/skills/sdd-loop-driver/SKILL.md>"`（external 平铺路径）/ `classification: external`——先例 create-skills、git-workspace 逐字实测。词面张力注解（external 分类 vs 内容编排 spec-kit 流程）写进 SKILL.md 正文 frontmatter 后注解行（clarify Q4 裁定的消解义务）。
- **D-3 测试先例与基线义务**：`tests/contract/test_run_skills_wiring.py` 形态 = 逐条款一测（`test_c1_...`）、canonical↔mirror 逐字节断言、frontmatter 子串钉死、**BASELINE_EXTERNAL/BASELINE_INTERNAL 名册 pinned**——新增 external 技能 MUST 同步该名册（否则 roster↔目录集合断言转红）。`baseline-failed.txt` 仓库根不存在，057 于特性目录自持 4 行基线——本特性沿用"tasks 阶段特性目录冻结基线"惯例。
- **D-4 注册面**：`.specify/skills.md` 自述"非注册表"（加技能无需编辑，发现靠目录扫描，实测其原文）；`docs/reference/skills/` 现有 10 个主题文档、057 未触及——FR-024 的 docs 参考页落 `docs/reference/skills/sdd-loop-driver.md` 为该目录首个"按技能名建页"先例（语义路径合规：`<area>/<topic>.md`）。
- **D-5 命名与冲突**：`sdd-loop-driver` 在 skills/、.specify/skills/、templates/ 全仓零命中（reserved identifier check 复核通过）；`-DONE` 哨兵后缀在 tests/scripts/templates 零既有断言（goal-utils 的 `open/done/dropped` Target 状态域为不同概念，无冲突）。
- **D-6 shared 底稿**：`shared/patterns/unattended-loop-pattern.md`（U0–U6 循环、边界口诀、独立校验/卡死处置语义）与 `shared/workflow/external-dispatch-recipes.md`（双拓扑/断点探测/prompt 骨架/runner 派生/后台轮询配方）为本 skill 撰写底稿——**内联其操作要点，标注底稿身份，运行时零依赖**（现状锚点 2026-10-15 内联统一后的口径）。
- **D-7 门控预算零扰动**：`scan-confirmation-gates.py` 的 `SCAN_ROOT_FILES=("templates",)`（051 特性记录 + 本轮实测确认）——skill/docs 文案不在扫描面，total 23 / violations 0 基线不动；本设计无需任何门控措辞规避。
- **D-8 勘探无异常**：8 项勘探全部落证据（子代理回传 "No anomaly found" 行）。

**Refine Technical Context**: 已并入上文 Technical Context（D-1…D-7 逐项落位）。无残留 NEEDS CLARIFICATION。

**Underdetermined design 检查**: 关键设计决策（external 分类、git 状态判定、投递形态无关、内联义务）均已在 clarify 阶段由用户裁定并记录于规格 Clarifications；无新出现的用户偏好级分叉，无需 interview。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`] | 8 实体（E-1 交付物 + E-2…E-8 运行期制品 schema）+ 校验规则 V-1…V-6 |
| Contracts | [`contracts/`] | 2 文件：`skill-structure.md`（C-1…C-12 + B-1…B-4）、`distribution-and-docs.md`（D-1…D-9）；FR 覆盖 25/25（映射见 feature-ref.md） |
| Quickstart | [`quickstart.md`] | 4 场景（S1 已执行基线实测 ×2 命令；S2–S4 实现后验证，逐例前提已列） |
| Feature ref | [`feature-ref.md`] | FR→条款映射 25/25 未覆盖 0；SC→度量 9/9；绑定记录 + Better-Harness 维度 |

**质量门记录**：deliberation 标记扫描 4 文件 + contracts/ 零命中（2026-10-15 实跑 `grep -rn`，exit 1 = clean）；命令示例执行核验——S1 两条命令已实跑（输出粘贴于 quickstart），S2–S4 逐例以「前提 + 契约测试钉死（路由 b，C/D 条款具名）」 discharge，无文件级整体免责。实测计数修正一处前提：pytest 裸 `python3 -m pytest` 不可用（系统 python3 无模块），测试必经 `scripts/bash/run-tests.sh`（已写入 Technical Context 与 quickstart S1）。
