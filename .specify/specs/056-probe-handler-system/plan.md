# Implementation Plan: Probe-Handler 体系（1 probe ⇒ N handler）

**Branch**: `056-probe-handler-system` | **Date**: 2026-10-13 | **Spec**: `.specify/specs/056-probe-handler-system/requirements.md`
**Requirement → Feature**: `056-probe-handler-system` → Feature 056 Probe-Handler 体系
**Input**: Specification from `.specify/specs/056-probe-handler-system/requirements.md`

## Summary

把 probe 从 feedback 域实体升格为全框架伞形一等实体，并新增 Handler / HandlerBinding 两层，使一个探测点（`@point:<lifecycle_point>` 选择器）可挂接 N 个已注册反应：按 scope（complex-commands / skills / all 或逐 object_id）与 order 编排，mode 区分 non-blocking（默认，fail-open）/ blocking。派发采用**编译期生成**——新共享引擎 `probe-utils.py --action compile-embeds` 从注册表为每个单元渲染单一 AUTO-GENERATED `## Wrap-up` 段，经既有 `regen-command-copies.py` / `sync-mirrors.py` 传播；"加一个机制 = 注册一行 + 重编译"。MVP 将 wrap-up 收尾点现有 5 个 handler（feedback 记录+阈值提示、token 自评、run-determination 四轴、docs-sync 评估、wrap-up 反思）合并编译，行为规则冻结（FR-020 仅允许接线引用类最小编辑），每单元差异以单元级参数保留，确认门控零命中（FR-015，预算整数余量为 0）。

## Technical Context

**Language/Version**: Python ≥3.8（stdlib-only，无新增运行时依赖）
**Primary Dependencies**: 既有引擎族（feedback-utils.py / trigger-utils.py / run-determination.py / evidence-utils.py）；新增共享引擎 probe-utils.py；Markdown 模板/技能面（纯文档投影，无运行时框架 — Constitution IX）
**Storage**: 文件注册表 — Probe Class×Object 真源 `shared/definitions/probe-definitions.md`（既有，升格伞形）；Handler / HandlerBinding 注册表新增于同一文件（章节定位见 data-model.md）；外部 probe 存储 `.specify/memory/feedback/probes/`（既有约定，零迁移，FR-009）
**Testing**: pytest（markers: contract / integration），契约测试落 `tests/contract/`
**Target Platform**: 本仓库框架源（templates/ + skills/ + shared/ + scripts/）及其全部镜像/工具副本投影（4 个命令副本树 + 6 对镜像，见 Mirror Obligations）
**Project Type**: 文档/提示词框架 + Python 脚本引擎（编译期代码生成，非运行时平台）
**Performance Goals**: N/A — compile-embeds 为一次性构建动作；对账/校验动作为秒级文件扫描
**Constraints**: ① 确认门控预算整数余量为 0（改前实测 total 23 / cap 23.25；cap 由测试侧 `tests/contract/test_confirmation_gates_sweep.py` 持有，脚本本身无 cap）→ 编译生成段措辞必须零 BLOCKING_PATTERNS（17 个正则）命中，否则先做预算 owner 裁定；② SC-007 Token 中性：迁移后收尾面非空行总数 ≤ 改前基线 853（具名冻结于 § SC-007 基线）；③ 次序依赖：run-determination 先于 feedback record，阈值提示消费其结果；④ 每单元差异必须保留（feedback 技能 runtime-mode gate 形态；简单命令排除 agents/constitution/feature 相关行）；⑤ 零生效 handler 的单元不输出任何段（clarify Q5）
**Scale/Scope**: 编译单元集 = 69 个（templates/commands 23 + skills/internal 35 + skills/external 11，实测口径见 § SC-007 基线）；probe-utils.py 5 个引擎动作（probes / map / probe-inject / handlers / compile-embeds）；MVP 绑定 5 个 handler 于 wrap-up 点；situation / phase-boundary / confirm-gate binding 显式留二期

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 22 FR / 8 SC 全部映射进本计划与 Phase 1 产物（feature-ref.md 给出映射）；生成段措辞冻结自既有各节（FR-020） |
| II | Feature-Centric Development | ✅ Pass | Feature 056 伞形绑定 + Feature 028 降为域实例（requirements.md § Clarifications Q2）；索引/详情同步义务落 feature-ref.md § 本规划对 Feature 记录的更新义务 |
| III | Intent-Driven Development | ✅ Pass | spec 只述 what/why（22 FR）；how（编译期派发）由 data-model.md / contracts/ 承载并逐条回指 FR |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 注册表 schema / 编译零漂移 / 引擎动作封闭集 / SC-007 预算 / 门控零命中先落契约测试再实现；先例 test_feedback_probe_registry.py C-2..C-5 |
| V | AI Agent Integration Standards | ✅ Pass | kind=agent 的调用形态按 clarify Q4 固定为 behavior_owner 锚行（FR-010）；AGENT_CONFIG / agent roster 不动 |
| VI | Continuous Quality & Observability | ✅ Pass | 生成段带 AUTO-GENERATED 头（机器可对账，FR-010）；situation/phase-boundary/confirm-gate 二期显式排除出 MVP，无 speculative 基建 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 工作流门裁决已记录：Feature 复用判定 = 新建伞形（requirements.md § Clarifications Q2）；本阶段只推进 Draft→Planned，Implemented 属 /speckit.implement |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 全部事实以代码实测行号取证（findings 1–7）；编译单元集经实测钉为 69（23 命令 + 35 内部技能 + 11 外部技能，scan_embed_units 同语义） |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 派发 = 编译期模板渲染 + 运行期 agent 顶序执行，无 runtime 调度器；散布探测点（P1–P5 等）显式留二期（finding 3） |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新段名 `## Wrap-up` 为框架语义段名而非文档命名面；docs/reference 更新沿用现有路径（FR-022）；无新保留名注册 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 机制修复落生成侧：wrap-up 五节并一节由 compile-embeds 渲染，加机制 = 注册一行 + 重编译（消除 040/033/S2 式全框架模板手术） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 scan_embed_units 单元枚举（feedback-utils.py L1342–1364）与 regen-command-copies / sync-mirrors 传播链；唯一新引擎文件 probe-utils.py |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 加机制成本从全框架模板手术降为注册+重编译 = Better Harness feedforward 维度改善（.specify/shared/guidelines/better-harness.md）；FR-011 固定 compile→regen→sync 次序契约 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 行为真源留在 shared/workflow/*.md（FR-020 冻结）；嵌入段 = 机器再生成副本；注册表 = 结构唯一真源 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 生成段词汇冻结自既有各节文案（FR-020），词汇面不变；新增措辞受 BLOCKING_PATTERNS 零命中约束（FR-015） |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 产物↔注册表零漂移对账 + engine action↔封闭集对账（FR-012 / FR-017）；异常显式失败不静默；--check 预检先行 |

**Gates Status**: ✅ All gates pass — 16/16 Pass，无 Fail/Partial 行，Complexity Tracking 为 N/A。

**Re-check after Phase 1**: 2026-10-13 —— 16 行全表经 fresh-context 只读子代理对照落盘产物复核：12 Pass；4 项证据指针缺陷（行 II 死指针、行 VI 引用错位 FR-012→FR-010、行 VII 误指 FR-019、行 XIII 缺 better-harness owner 锚）已就地修正为 Pass；行 VIII 措辞校正（69 = 23+35+11 为实测确认口径）；quickstart 免责面扩展覆盖迁移态非引擎命令。无 Fail/Partial 残留，Complexity Tracking 维持 N/A。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/056-probe-handler-system/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

No standalone research.md — Phase 0 findings inlined below（全部为内部代码取证，无外部源评估）。

### Source Code (repository root)

```text
shared/definitions/probe-definitions.md   # Probe Class×Object 注册表真源（既有）：升格伞形 + 新增 Handler/HandlerBinding 章
scripts/python/probe-utils.py             # NEW 共享引擎：probes/map/probe-inject（自 feedback-utils.py 迁入）+ handlers + compile-embeds
scripts/python/feedback-utils.py          # 移除 probe 族动作与注册表加载，保留 11 个领域动作
templates/commands/*.md                   # 23 个命令模板（编译单元）：手工 `## Feedback` 段 → 编译 AUTO-GENERATED `## Wrap-up` 段
skills/internal/*/SKILL.md                # 35 个内部技能单元：同上（runtime-mode gate 差异以单元级参数保留）
skills/external/*/SKILL.md                # 11 个外部技能单元：同上
shared/workflow/feedback-step.md          # 行为真源（冻结）——仅允许接线引用类最小编辑（FR-020）
shared/workflow/docs-step.md              # 行为真源（冻结）——同上
tests/contract/                           # 新契约：注册表 schema、编译零漂移、引擎动作封闭集、SC-007 预算、门控零命中
docs/reference/skills/                    # 引擎/机制参考更新（FR-022）；词汇表义务见 FR-019（两者无镜像对，host-side 编辑）
.specify/                                 # 上述源面文件的镜像投影（sync-mirrors.py 传播，不手改；命令模板另经 regen-command-copies.py 扇出 4 工具树）
```

**Structure Decision**: 文档/提示词框架形态（代码生成器形：templates/ + scripts/ + shared/），不新建任何顶层目录。共享引擎落既有 `scripts/python/`，注册表真源扩既有 `shared/definitions/probe-definitions.md`，编译目标为既有 `templates/commands/` 与 `skills/{internal,external}/` 单元面。唯一新文件级产物是 `scripts/python/probe-utils.py`（及镜像副本）；`memory/` 与 `docs/` 无镜像对（finding 5），其更新为纯 host-side 编辑。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/probe-definitions.md` | `.specify/shared/definitions/probe-definitions.md`（shared↔.specify/shared 对） | `python3 scripts/python/sync-mirrors.py --check` — 改前基线已实测 exit 0（2026-10-13，见 Phase 0 基线记录）；判据 = 无 NEW drift（仅本 spec 所触文件出现新差异）+ 副本含编辑 |
| `scripts/python/probe-utils.py`（NEW） | `.specify/scripts/python/probe-utils.py`（scripts 严格对，双向新建） | 同上：sync-mirrors --check 无 NEW drift；副本文件存在且 byte-identical |
| `scripts/python/feedback-utils.py` | `.specify/scripts/python/feedback-utils.py` | 同上：sync-mirrors --check 无 NEW drift |
| `templates/commands/*.md`（23 个编译单元） | `.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/` —— regen-command-copies.py 扇出；NO `.specify/templates/commands/` 镜像（已退役） | `python3 scripts/python/regen-command-copies.py --check` — 改前基线实测 exit 0；判据 = 无 NEW drift + 再生成副本含 `## Wrap-up` 编辑 |
| `skills/internal/*/SKILL.md`（35 单元） | `.specify/skills/internal/*`（internal 对，133 文件面） | sync-mirrors --check 无 NEW drift |
| `skills/external/*/SKILL.md`（11 单元） | `.specify/skills/external/*`（external 对，363 文件面） | sync-mirrors --check 无 NEW drift |
| `shared/workflow/feedback-step.md`、`shared/workflow/docs-step.md` | `.specify/shared/workflow/` 对应副本 | sync-mirrors --check 无 NEW drift |
| `docs/reference/**`、`.specify/memory/glossary.md` | 无镜像对（memory/ 与 docs/ 不在 MIRROR_PAIRS，finding 5） | N/A — 仅 host-side 编辑，无对账义务 |

## Complexity Tracking

N/A — Constitution Check 16 项全部 Pass，无需要 justified 的 violation。

## Phase 0: Research Review

**Information Gathering**: 项目文档按 token-efficiency 纪律取目标摘录（AGENTS.md Documentation Map + feedback/run-determination 参考）；Feature 记忆投影读取（features.md 行 + 056.md 详情）；代码取证以 Explore 子代理 + 定向 grep 完成。无外部源评估，不产出独立 research.md。

**Findings（全部实测取证）**:

1. **引擎动作分区（实测）**：feedback-utils.py 现有 14 个 action（choices 定义 L1933–1939）；probe 族动作 = probes / map / probe-inject 三个，`--validate` / `--reconcile` 是 probes 动作的旗标而非动作（L1986–1992）→ 迁移后 probe-utils.py 承接 3 个既有动作 + 新增 handlers / compile-embeds = 5 个动作；feedback-utils.py 保留 11 个领域动作。外部 probe 存储维持 `.specify/memory/feedback/probes/`（EXTERNAL_PROBES_DIRNAME，L1172），零迁移（FR-009）。
2. **单元枚举可复用（实测）**：scan_embed_units（feedback-utils.py L1342–1364）双向扫描 templates/commands/*.md + skills/{,external/,internal/}*/SKILL.md 中字面 `## Feedback` 段，与注册表互为对账（零缺口）——compile-embeds 复用同一单元枚举，天然覆盖两源面，不引入新扫描器（Constitution XII）。
3. **散布探测点不入 MVP（实测）**：P1–P5 升级探测硬编码于 trigger-utils.py run_probes（L565–639）；满意度表为 run-determination.py 代码常量（_build_satisfaction_table L625）；证据引擎 lane 探测于 evidence-utils.py（L41/194/220/241）——均按 spec 增量策略留二期 binding，本次不动。
4. **前提修正①（门控预算归属）**：预算 cap 由契约测试持有（test_confirmation_gates_sweep.py L161–168 断言 total ≤ 23.25），scan-confirmation-gates.py 脚本本身无 cap；BLOCKING_PATTERNS 共 17 个正则（L46–64），SCAN_DIRS 覆盖 templates/commands + skills + shared + 根 templates/*.md。编译段措辞的零命中义务由此约束；若需预算裁定，owner 在测试侧基线，不在脚本。
5. **前提修正②（镜像拓扑）**：sync-mirrors.py MIRROR_PAIRS 实测 6 对（templates[排除 commands/]、skills/external、skills/internal、agents、scripts、shared）；memory/ 与 docs/ **无镜像对**——glossary 与 docs/reference 更新无 mirror 义务。
6. **前提修正③（命令副本扇出）**：templates 镜像对排除 commands/（已退役）；23 个命令模板的副本仅由 regen-command-copies.py 经 src/specify_cli.generate_commands 扇出到 .claude/commands、.github/prompts、.qoder/commands、.opencode/command 四树。
7. **现状收尾段形态（实测）**：现嵌段标题为 `## Feedback`（例：templates/commands/implement.md L47–53），其后依次 `## Documentation`、`## Handoffs`；全仓不存在 `## Wrap-up` 字面（已 grep 验证）——clarify Q1 选定的新段名无存量冲突。每单元差异落点已确认：feedback 技能形态为 runtime-mode gate 段落，简单命令排除 agents/constitution/feature 相关行——编译模板必须以单元级参数（scope 判定）承载，不得全框架同文。

**无未知项**：requirements.md 无遗留 `[NEEDS CLARIFICATION]`（clarify 已清空）；Technical Context 全项可定；无 NEEDS CLARIFICATION 需要在本阶段解决。

### 改前基线记录（2026-10-13 实测，Mirror Obligations 与 FR-015/SC-007 判据对照值）

确认门控扫描（预算整数余量 0）：

```text
$ python3 scripts/python/scan-confirmation-gates.py
blocking confirmation gates: 23
  destructive: 16
  governance_kept: 7
violations (reversible gates still blocking): 0
```

镜像漂移（6 对全 ok，文件数 21/363/133/2/106/46）：

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (21 files)
ok    skills/external/ == .specify/skills/ (363 files)
ok    skills/internal/ == .specify/skills/internal/ (133 files)
ok    agents/ == .specify/agents/templates/ (2 files)
ok    scripts/ == .specify/scripts/ (106 files)
ok    shared/ == .specify/shared/ (46 files)
sync-mirrors exit=0
```

命令副本漂移：

```text
$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
regen exit=0
```

### SC-007 基线（具名冻结小节）

- **判据**：收尾面非空行数 = `## Feedback` 与 `## Documentation` 两个 `##` 级节体内的非空行合计（切节规则：遇到下一 `## ` 行即止节），面集 = `templates/commands/*.md` + `skills/internal/*/SKILL.md` + `skills/external/*/SKILL.md`（源面，不含任何镜像/工具副本）。
- **编译单元集**（含字面 `## Feedback` 的单元，与 scan_embed_units 同语义，实测）：

```text
$ grep -l '^## Feedback' templates/commands/*.md | wc -l
23
$ grep -l '^## Feedback' skills/internal/*/SKILL.md | wc -l
35
$ grep -l '^## Feedback' skills/external/*/SKILL.md | wc -l
11
```

  合计 **69 个编译单元**（23 + 35 + 11）。
- **改前非空行实测**（2026-10-13，命令与真实输出）：

```text
$ awk 'FNR==1{u++} /^## /{sec=($0~/^## (Feedback|Documentation)( |$)/)} sec&&NF{n++} END{printf "units=%d non-blank_lines=%d\n",u,n}' templates/commands/*.md
units=26 non-blank_lines=90
$ awk 'FNR==1{u++} /^## /{sec=($0~/^## (Feedback|Documentation)( |$)/)} sec&&NF{n++} END{printf "units=%d non-blank_lines=%d\n",u,n}' skills/internal/*/SKILL.md
units=35 non-blank_lines=575
$ awk 'FNR==1{u++} /^## /{sec=($0~/^## (Feedback|Documentation)( |$)/)} sec&&NF{n++} END{printf "units=%d non-blank_lines=%d\n",u,n}' skills/external/*/SKILL.md
units=11 non-blank_lines=188
```

  合计 **853 非空行**（commands 90 + internal 575 + external 188）。
- **迁移后判据**：同面集同规则实测总数 **≤ 853**（对照 STR-001 单段形态；SC-007 只设不回归上限，未设下限）。
- **口径注**：commands 面 awk 扫到 26 个文件，其中 3 个不含 `## Feedback`（贡献 0 行）；单元计数一律以 69 编译集口径为准，行数不受影响。

## Phase 1: Design Artifacts Summary

产物落盘后实测计数（2026-10-13，命令真实输出）：

```text
$ ls -1 .specify/specs/056-probe-handler-system/contracts/
compile-embeds.md
engine-action-sets.md
handler-registry.md
probe-registry.md
$ grep -c '^### [0-9]' .specify/specs/056-probe-handler-system/data-model.md
7
$ grep -c '^## Scenario' .specify/specs/056-probe-handler-system/quickstart.md
4
$ grep -c '^- FR-\|^| FR-' .specify/specs/056-probe-handler-system/feature-ref.md
22
```

计数口径注：`^### [0-9]` 仅匹配 data-model.md 的实体定义节（### 1…### 7），不触及其他三级标题；`^## Scenario` 仅匹配 quickstart.md 的场景节；feature-ref 的匹配模式命中 22 个 FR 映射行（该文件内无其他 `- FR-`/`| FR-` 形态行）。

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | `data-model.md` | 7 实体（ProbeClass / ProbeObject / 非实体目录条目 / Handler / HandlerBinding / CompiledEmbed / ExternalProbe）+ 漂移错误类封闭集 8 项 + MVP 种子 5 Handler / 5 Binding |
| Contracts | `contracts/` | 4 files: probe-registry.md / handler-registry.md / compile-embeds.md / engine-action-sets.md |
| Quickstart | `quickstart.md` | 4 scenarios（注册重编译 / 漂移预检对账 / 零段语义 / 封闭集对账）；全部 probe-utils.py 示例为 route (b) 免责 + 契约测试预登记 |
| Feature ref | `feature-ref.md` | 22 FR 映射行（22/22 全覆盖）+ SC 测量源回指 |

与 Phase 0 预期的偏差：无（预登记 4 份契约，实际落盘 4 份；实体 7 个与预期一致）。
