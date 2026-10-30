# Implementation Plan: Coaching Skills（教练技能）

**Branch**: `078-coaching-skills` | **Date**: 2026-10-30 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `078-coaching-skills` → Feature 078 Coaching Skills（教练技能）
**Input**: Specification from `.specify/specs/078-coaching-skills/requirements.md`

## Summary

把外部技能 `think-skills` 重命名并重构为 `coaching-skills`：技能接收「Trainee 目标 + 真实工作」两个位置参数，先在自身上下文里产出双维度执行预期（结果正确性 / 过程效率），再派发**恰好一个**子代理按 Trainee 自身 `SKILL.md` 完成真实工作，教练侧逐步观测并落盘，最后按「预期 vs 实际」产出偏差报告与提升计划，并通过 `improve-skills` 的既有入口应用。

技术路线是**零新增运行时**：技能是一份提示词契约（`skills/external/coaching-skills/`），运行产物是一文一件的 markdown 文件（`.specify/memory/coaching/<run-id>/`），Trainee 解析复用 `run-skills`，子代理派发复用宿主原生能力（降级 `run-agent`），优化复用 `improve-skills`；改名靠既有注册表（flow-class 台账、probe 注册表、`_OBSOLETE_SKILLS`）与既有再生成入口（`sync-mirrors.py`、`regen-command-copies.py`、`probe-utils.py`、`specify render-agents`）落地。

## Technical Context

**Language/Version**: Markdown（技能契约）+ Python 3.8+（既有确定性引擎；本特性不新增脚本）
**Primary Dependencies**: 宿主原生子代理派发（主）/ `run-agent`（降级）/ `run-skills`（Trainee 解析语义）/ `improve-skills`（优化入口）/ `probe-utils.py`、`flow-class-check.py`、`sync-mirrors.py`、`regen-command-copies.py`、`specify render-agents`
**Storage**: 文件即存储——运行产物落 `.specify/memory/coaching/<run-id>/`；注册表真源为 `shared/definitions/flow-class-definitions.md`、`shared/definitions/probe-definitions.md`、`.specify/memory/features.md`
**Testing**: `pytest`（contract 为主）；四个冻结基线测试显式更新；新增教练产物契约测试（夹具 Trainee）；确定性检查 `pre-analyze-check.py`、`flow-class-check.py --action check`、`probe-utils.py --action compile-embeds --check`、`sync-mirrors.py --check`、`regen-command-copies.py --check`、`scan-confirmation-gates.py`
**Target Platform**: 任何支持 Spec Kit 的 agent 宿主；技能是提示词层，不依赖特定运行时
**Project Type**: single（框架源码 + 自举运行时双帽）
**Performance Goals**: 无吞吐目标。可用预算有两条：技能正文过 `skills/external/improve-skills/scripts/skill-shape.py`（基线 ≈1981 tokens / 预算 5000，判定 pass）；单次教练运行的步骤行数与上下文消耗属观测项、不是门禁
**Constraints**: 零新增阻断式确认门（判定单位是 `git diff` 新增行，基线读数见 `test-evidence/stage-plan-baselines.txt`）；旧名在封闭活接线面内至多 1 次（`_OBSOLETE_SKILLS` 条目）；期望必须在派发前落盘；每次运行恰好 1 次派发；派生面只再生成、不手改；历史记录不改写
**Scale/Scope**: 1 个技能包（`SKILL.md` + `references/`）；5 份契约；19 个需手改源文件 + 4 类派生面；4 个冻结基线测试显式更新；台账 79 行（27 命令 + 52 技能，实测）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, 18 principles in file order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | `requirements.md` 的 FR/SC 逐条落进 `contracts/` 条款与 `data-model.md` 校验规则；无需求外设计 |
| II | Feature-Centric Development | ✅ Pass | Feature 078 已登记，本阶段把 `Draft` 推进到 `Planned` 并更新 `.specify/memory/features/078.md` |
| III | Intent-Driven Development | ✅ Pass | Summary 与 `contracts/coaching-run.contract.md` 先给「what/why」，实现细节留到 tasks |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 四个冻结测试与新增契约测试先于技能正文落地；夹具场景对 SC-001…SC-005 |
| V | AI Agent Integration Standards | ✅ Pass | 不改 `AGENT_CONFIG` / `_ASSISTANT_TIERS`；仅用 `specify render-agents --ai qoder` 再生成宿主副本 |
| VI | Continuous Quality & Observability | ✅ Pass | 基线读数存档（`test-evidence/stage-plan-baselines.txt`）；观测记录本身即可审计日志 |
| VII | Specification-Plan-Task-Implementation Workflow (NON-NEGOTIABLE) | ✅ Pass | 本阶段只推进到 `Planned`；不改写需求；历史 run 记录不回填 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 设计前实测活接线面（79 台账行、52 技能、`git grep` 逐文件命中文），不靠记忆 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 技能是提示词；无调度器、无新引擎、无评分系统；并发靠每 run 一目录 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新目录 `skills/external/coaching-skills/`（kebab、语义路径）；运行目录 `coaching/<run-id>/` 路径即语义；无保留名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 改动落在框架源（`skills/`、`shared/`、`src/`），`.specify/` 侧全部再生成；旧目录清理走 `_OBSOLETE_SKILLS` 机制而非实例补丁 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 `run-skills` 解析、`improve-skills` 入口、`probe-utils`/`sync-mirrors`/`regen-command-copies`；不新增脚本 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Controlled Execution（Trainee 按自身流程真实跑通）与 Learning Capture（偏差 → 提升计划）两个维度 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 17 个 STR 字面量 owner 为 `requirements.md`；契约只细化形态；台账/probe 行各有 owner；计数取实测 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 澄清句与运行报告按 owner 写作；内部引擎调用形式不出现在用户面 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 派发载荷注入快速失败条款并要求子代理显式回传异常行；不可见步骤标 `observation-gap` 不编造 |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | 新目录 `.specify/memory/coaching/` 在同一变更内登记进 `shared/definitions/framework-map.md` 的 memory 区（镜像再生成） |
| XVIII | Grounded Naming | ✅ Pass | 用户裁定的 `coaching-skills` 逐处贯穿：目录、frontmatter、skill_id、unit id、台账行、probe 行、路由行、触发词 |

**Gates Status**: ✅ 全部通过，无未证成 Fail/Partial 行。

**Re-check after Phase 1** (2026-10-30, against `data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md`): 同一 18 行逐行复核，结论不变——设计产物只增加「运行目录登记」「契约条款编号」「派生面再生成命令」三类内容，未引入新运行时、新门禁或新事实定义点。

## Decision Tensions

记录形态、可采纳判据、拒绝形态与承重门槛归 `.specify/shared/guidelines/decision-tension.md`（从仓库根读取；本文件不复制判据表）。

### T-001 — 冻结基线用「退役路径登记」承接改名，而不是重写 069a 的哈希清单

- **decision**: 069a 的 `notes/pre-change-file-hashes.txt` 保持原样（dated record），在 `tests/contract/test_expression_compatibility.py` 内新增「退役路径 → 新路径 + 日期 + 理由」登记，清单计数 74/25/49 不变。
- **antithesis**: 按当前树重新生成一份新的哈希清单并替换旧清单；当团队只需要「当前树有无未声明改动」、且不再需要 069a 当时的窗口证据时它更优——测试里没有退役分支，断言更简单。
- **binding_constraints**:
  - pole_a: 历史记录 MUST NOT 被改写（FR-024 / A9），069a 的清单是当时窗口的证据。
  - pole_b: 冻结测试 MUST 保持可判定——旧路径若被静默从清单删除，C-5 的「零新增技能」断言会退化成空断言。
- **discriminating_evidence**: 在实现后的树上运行 `pytest tests/contract/test_expression_compatibility.py -q`，临时移除退役登记并保留清单原样，观察 C-5 是否报 `missing`；结果二值：报出 / 不报出。
- **expected_sacrifice**: SC-009 Source ↓ 冻结测试需多维护一张退役映射（四个测试文件中的一个从「改名」升级为「改名 + 退役语义」），单文件行数增加。
- **revision_trigger**: 退役映射累计超过 3 条（连续三次改名都靠它累积）→ 重开，改为「基线清单 + 按特性分片的增量清单」结构。

### T-002 — 优化在教练会话内联调用 improve-skills，而不是再派发一个子代理

- **decision**: 闭环完成后，教练在自己会话里按 `improve-skills` 既有入口应用提升计划；整次运行只派发一个子代理（Trainee 执行）。
- **antithesis**: 为优化单独派发第二个子代理承载 Trainee 全量文本与偏差证据；当教练会话上下文接近上限、或优化需要大量阅读 Trainee 引用文件时它更优——教练上下文不被优化阅读挤占。
- **binding_constraints**:
  - pole_a: FR-009 规定每次运行恰好一个子代理执行 Trainee，失败也不放宽。
  - pole_b: FR-016 要求 `improve-skills` 拿到偏差证据，而预期与观测都在教练上下文里，只有教练能原样交出。
- **discriminating_evidence**: 在夹具运行里数观测记录 `## Dispatch` 段的派发行数；结果二值：1 / 其他。
- **expected_sacrifice**: SC-005 Source ↓ 教练上下文在优化阶段承担 `improve-skills` 的全文阅读，单次运行的上下文消耗上升（由运行判定的 token 轴观测，非门禁）。
- **revision_trigger**: 出现两次以上「教练上下文在优化阶段耗尽、运行被迫 `run: partial`」→ 重开，改为优化阶段独立派发并在两处之间传递偏差报告路径。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/078-coaching-skills/
├── plan.md              # This file (/speckit.plan command output)
├── requirements.md      # Upstream authority (29 FR / 9 SC / 17 Shared Strings)
├── checklists/          # Requirements-quality checklist (requirements stage)
├── test-evidence/       # Deterministic-check evidence per stage
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (5 contract documents)
├── feature-ref.md       # Phase 1 output (Feature 078 binding)
└── tasks.md             # Phase 2 output (/speckit.tasks command — NOT created here)
```

No standalone `research.md` — Phase 0 findings are inlined below.

### Source Code (repository root)

```text
skills/external/coaching-skills/          # NEW skill package: SKILL.md + references/ (expectation & observation templates)
skills/external/think-skills/             # REMOVED (renamed; its directory and references move under the new name)
skills/internal/run-skills/SKILL.md       # modify-family pointer: think-skills → coaching-skills
skills/internal/create-agent/templates/   # four role templates listing think-skills in their skills: lists
agents/skill-verifier.agent.md            # skills: list (Agent Template source)
agents/structure-adjuster.agent.md        # skills: list (Agent Template source)
templates/commands/skills.md              # /speckit.skills routing row + call form
shared/definitions/flow-class-definitions.md   # ledger row + 台账版本 + change record
shared/definitions/probe-definitions.md        # probe Object row (id + handler unit)
shared/definitions/framework-map.md            # register `.specify/memory/coaching/` in the memory area row
src/specify_cli/__init__.py               # _OBSOLETE_SKILLS entry + historical comment restatement
docs/reference/agents/command-and-skills.md    # live example list
docs/tutorials/quickstart.md              # skill list entry
tests/contract/test_expression_compatibility.py    # frozen baseline (rename + retired-path register)
tests/contract/test_migration_distribution.py      # frozen baseline (skill roster)
tests/contract/test_skill_layer_visibility_guards.py  # frozen baseline (external roster + counts)
tests/contract/test_run_skills_wiring.py           # frozen baseline (roster + route grammar)
tests/contract/                           # NEW coaching contract tests (artifacts, dispatch payload, wiring residues)
```

**Structure Decision**: 本特性在既有「外部技能包 + 共享注册表 + 契约测试」形态内落地，新增唯一顶层目录是三处：`skills/external/coaching-skills/`（技能包，替换同名旧包）、`.specify/memory/coaching/`（运行产物区，须登记进 `framework-map.md` 的 memory 行）、以及 `.specify/specs/078-coaching-skills/contracts/`（本规格的设计产物）。不新增 Python 脚本、不改 `AGENT_CONFIG`、不改 `improve-skills` 契约。

### Mirror Obligations

基线漂移实测（2026-10-30，改动前）：`sync-mirrors.py --check` 退出 0（`templates`/`skills/external`/`skills/internal`/`agents`/`scripts`/`shared` 六对全 ok），`regen-command-copies.py --check` 退出 0，`probe-utils.py --action compile-embeds --check` 报 `75 units, zero drift`。因此本表的判据是「**不新增**漂移」，而不是绝对绿。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/external/coaching-skills/**`（新增） | `.specify/skills/coaching-skills/**`（`skills/external` → `.specify/skills` 对） | `sync-mirrors.py --write --only skills/external` 后 `--check` 无 DIFF/MISS；`git grep -l 'coaching-skills' -- .specify/skills` 命中新目录 |
| `skills/external/think-skills/**`（删除） | `.specify/skills/think-skills/**` 必须显式删除——`sync-mirrors.py` 的 extras 是「archive-not-delete」，不会替我们删 | `test ! -e .specify/skills/think-skills` 成立；`sync-mirrors.py --check` 无旧路径条目 |
| `agents/skill-verifier.agent.md`, `agents/structure-adjuster.agent.md` | `.specify/agents/templates/*.agent.md`（镜像）；`.qoder/agents/*.agent.md`（`specify render-agents --ai qoder`）；`.claude/`/`.github/`/`.opencode/` 的 agents 副本由同一渲染入口按各自字段映射产出 | `sync-mirrors.py --check` 无 DIFF；`.venv/bin/specify render-agents --ai qoder` 后 `grep -rn think-skills .qoder/agents` 为空 |
| `templates/commands/skills.md` | `.claude/commands/speckit.skills.md`；`.github/prompts/speckit.skills.prompt.md`；`.opencode/command/speckit.skills.md`；`.qoder/commands/speckit.skills.md`（`regen-command-copies.py` 单一扇出；`.specify/templates/commands/` 已退役，不产副本） | `regen-command-copies.py --write` 后 `--check` 退出 0 |
| `shared/definitions/flow-class-definitions.md`, `probe-definitions.md`, `framework-map.md` | `.specify/shared/definitions/*.md`（`shared` → `.specify/shared` 对） | `sync-mirrors.py --check` 无 DIFF；`flow-class-check.py --action check` 报 `matched=79 inventory_units=79` |
| `shared/definitions/probe-definitions.md`（probe 行改名） | 技能正文编译块 `## Wrap-up`（`probe-utils.py --action compile-embeds`）；`.specify/memory/feedback/probe-map.md`（`--action map`） | `probe-utils.py --action compile-embeds --check` 退出 0 且仍为 `75 units`（改名删一增一、净变化 0；2026-10-30 实测构成：23 个带 `## Wrap-up` 的命令模板 + 52 个技能）；`--action probes --validate` 退出 0 |
| `src/specify_cli/__init__.py` | 无仓库内镜像；生效路径是 `uv tool install` / `pipx` 后的安装包（本仓库 `.venv/` 是旧版，不做手改） | `python3 -c "import ast,sys; ast.parse(open('src/specify_cli/__init__.py').read())"` 通过；升级清理由 SC-007 夹具 `specify init` 验证 |

## Complexity Tracking

N/A — 无 Constitution Check 违规项，无需要证成的 Fail/Partial 行。

## Phase 0: Research Review

**方法说明**：本阶段的代码探索由单上下文有界探测完成（`git grep` 逐文件命中文 + 定向摘录），未派发 Explore 子代理（本次运行受单上下文约束）。同一约束也适用于 Constitution Check 与质量门的同作者自评分：两份评分均由本上下文完成，未做 fresh-context 委派——这是本阶段的方法局限，记录在此供 `/speckit.analyze` 以独立视角复核，不作为完成信号。

关键实测（2026-10-30，均写入 `test-evidence/stage-plan-baselines.txt`）：

1. **活接线面**：`git grep -l think-skills` 命中 79 个受版本管理文件；其中需手改的源码恰为需求 A10 声明的 19 个（技能本体 2、路由模板 1、agents 2、create-agent 角色模板 4、run-skills 1、shared/definitions 2、src 1、docs 2、contract tests 4），其余为派生面与历史记录。需求正文写的「77 个受版本管理文件」是 requirements 成文时的读数，成文后 `requirements.md` 与 `features*.md` 自身也新增了命中，故当前读数为 79——差异来自计量时点，不是设计分歧；SC-006 的判据以 A10 的**封闭集**为准，不吃全仓计数。
2. **`src/specify_cli/__init__.py` 的两处命中**：`_OBSOLETE_SKILLS` 之外还有一行历史注释 `thought-experiment-verifier→think-skills;`。SC-006 要求旧名在封闭面内恰为 1 次，因此该注释必须以不带旧名字面量的方式重述（保留改名链语义，指向 Feature 078），否则计数就是 2。
3. **镜像不删 extras**：`sync-mirrors.py` 对 `skills/external` 只同步 MISS/DIFF，extras 只提示不删除；改名后 `.specify/skills/think-skills/` 必须显式删除，否则旧名留在安装面。
4. **`_OBSOLETE_SKILLS` 清理语义**：`cleanup_obsolete_framework_assets()` 对 symlink 或不存在者 `continue`，只 `rmtree` 实体目录——与 FR-020 的「删实体、留用户符号链接」天然一致，无需改代码。
5. **probe 与台账**：`probe-utils.py --action compile-embeds --check` 基线 75 单元零漂移；`flow-class-check.py --action check` 基线 `matched=79 inventory_units=79`，台账实际是 27 命令 + 52 技能（文件头写的 78 行是 2026-10-24 读数，已过期）；`lookup skill:think-skills` 解析为 `execution / behavior-oracle`，与 SC-006 期望的新行同值。
6. **门禁预算**：`scan-confirmation-gates.py --summary` 基线 blocking=27（destructive 20 + governance_kept 7），violations 0；扫描面是 `templates/commands`、`skills`、`shared`、`templates/*.md`。新技能正文与路由行必须避开 `BLOCKING_PATTERNS`（例如不得出现「确认门[禁控]」「显式用户确认」「stop and confirm」等），且「external」「删除」这类破坏性关键词只出现在已被治理保留的行上才算合法。
7. **技能形态门**：`skill-shape.py` 对旧技能判 `pass`（≈1981 tokens / 5000 预算，110 行），但已报 `oversized-section`（Workflow 51 行）与 `flags-outside-contract`（Wrap-up 段 23 个 CLI flag）。新正文把逐步骤手册移进 `references/`，Workflow 保持骨架，避免把这两条警示带进新包。
8. **升级兼容机制已在位**：`render_agents_for_tool` 与 `specify render-agents --ai qoder` 存在且可运行（`--help` 退出 0），宿主 agent 副本无需手改。

**决策落点**：`data-model.md` 承载实体与校验规则；`contracts/` 五份契约承载运行契约、三份产物形态、派发载荷、身份接线；`quickstart.md` 承载可执行验收路径；`feature-ref.md` 承载 Feature 078 绑定。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](./data-model.md) | 8 entities（CoachRun / TraineeTarget / ExpectationCriteria / ObservationStep / DispatchRecord / DeviationFinding / ImprovementEntry / RunStatus）+ 4 状态机 |
| Contracts | [`contracts/`](./contracts/) | 5 files: `coaching-run.contract.md`, `expectation.contract.md`, `observation.contract.md`, `dispatch-payload.contract.md`, `identity-and-wiring.contract.md` |
| Quickstart | [`quickstart.md`](./quickstart.md) | 5 scenarios（wiring 验证 / 夹具教练运行 / 升级兼容 / 退化路径 / 清理） |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | Feature 078 绑定与映射表 |

契约条款覆盖核对（FR → 契约）：FR-001…FR-003 → `coaching-run.contract.md` C-1…C-3；FR-004…FR-008 → `expectation.contract.md` C-1…C-5；FR-009…FR-013 → `dispatch-payload.contract.md` C-1…C-5 + `observation.contract.md` C-1…C-6 + `coaching-run.contract.md` C-5/C-6；FR-014…FR-017 → `coaching-run.contract.md` C-7…C-10；FR-018…FR-024 → `identity-and-wiring.contract.md` C-1…C-7；FR-025…FR-029 → `coaching-run.contract.md` C-3/C-9/C-12…C-14。SC-006 / SC-008 的可复核命令面写在 `identity-and-wiring.contract.md` C-8。

与 Phase 0 预期的偏差：无。Phase 0 预计「契约 4–5 份」，实际 5 份——多出的 `identity-and-wiring.contract.md` 把 A10 的 19 文件封闭集与 4 类派生面写成可逐行勾选的接线表，因为改名是本特性的另一半工作。
