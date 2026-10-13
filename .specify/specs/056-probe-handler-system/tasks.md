# Tasks: Probe-Handler 体系（1 probe ⇒ N handler）

**Requirement ID**: 056 (from branch name)
**Requirement Key**: 056-probe-handler-system
**Related Feature**: 056 Probe-Handler 体系（伞形：Probe / Handler / HandlerBinding 基础设施）
**Input**: Design documents from `.specify/specs/056-probe-handler-system/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), data-model.md, contracts/ (4 contracts), quickstart.md, feature-ref.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates test-first with contract tests; Principle VII's template-only gate is NOT applicable — this feature ships executable runtime `scripts/python/probe-utils.py`, so structural contract tests supplement rather than replace unit/contract tests. Migration/regression exception applied: guard tests pinning pre-existing behavior (T018, T022, T025, T027) are placed AFTER their implementation tasks with explicit `[blockedBy]`, per create-tasks skill rule.)

**Contract paths** (relative to this file's directory): `contracts/probe-registry.md`, `contracts/handler-registry.md`, `contracts/compile-embeds.md`, `contracts/engine-action-sets.md` — referenced below as [C1]–[C4]:
- [C1] = contracts/probe-registry.md (probe-utils CLI closed set + migration duties)
- [C2] = contracts/handler-registry.md (Handler/HandlerBinding schema + handlers action)
- [C3] = contracts/compile-embeds.md (compile algorithm, --check, refuse conditions, order)
- [C4] = contracts/engine-action-sets.md (two engine action closed sets verbatim)

## Definition of Done (DoD)

- DoD-1: `probe-utils.py` 上线 5 个动作（probes / map / probe-inject / handlers / compile-embeds），probe 族三动作自 feedback-utils.py 迁出且行为不变；feedback-utils.py 收缩为 11 领域动作封闭集（[C4]）且全部既有 action 行为逐项不变（封闭集契约测试绿）
- DoD-2: `shared/definitions/probe-definitions.md` 伞形扩格完成：既有 6 Class / 72 Object 语义零回退，新增散布探测点 Class/Object 带代码锚点，非实体 probe 以纯指针目录收录；`probes --validate` 与 `handlers --validate` exit 0
- DoD-3: 69 个编译单元（23 命令模板 + 35 内部技能 + 11 外部技能）迁移完成态：手工嵌入段清零（命令模板与技能中 `## Feedback` 手工段命中 0），每单元单一 AUTO-GENERATED `## Wrap-up` 收尾段，两次编译 byte-identical
- DoD-4: 五类对账守卫（孤儿 handler / 缺失 handler / 非法 action / order 冲突 / 措辞命中）变异演练逐一转红且指名错误，正向树全绿
- DoD-5: 全部自动化测试通过——相对本运行记录的 failing-test 基线零新增失败（基线 owner：`templates/commands/implement.md` § Test runs）
- DoD-6: 门控预算不变：`scan-confirmation-gates.py` total 23 / violations 0；编译产物行预算 SC-007 ≤ 853 非空行
- DoD-7: 词汇表三新术语（Probe 伞形 / Handler / HandlerBinding，Feedback Probe 降为域实例，「埋点」消歧重写）与 `docs/reference/` probe 体系文档更新完成（FR-019 / FR-022）
- DoD-8: `verification.md` 覆盖 requirements.md 全部 SC-001..008，含诚实 partial（如有）

**DoD Status**: pending

## Completion Gate

- GATE-1: 全量契约+集成测试相对基线零新增失败 — check: `python3 -m pytest tests/ -m contract` 与失败基线对比（基线 owner：`templates/commands/implement.md` § Test runs）
- GATE-2: 镜像面零新增漂移 — check: `python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/regen-command-copies.py --check` 均无 NEW drift
- GATE-3: 无遗留开放任务行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/056-probe-handler-system/tasks.md` 返回 0
- GATE-4: verification.md 逐条列出 SC-001..008 且每条带状态 — check: 对照 requirements.md § Success Criteria 的 SC 编号集合 grep verification.md
- GATE-5: 手工嵌入段清零 — check: 全仓 grep 手工 `## Feedback` 嵌入段于命令模板与技能面命中 0（编译产物内出现由 AUTO-GENERATED 横幅声明来源）
- GATE-6: 门控预算不变 — check: `python3 scripts/python/scan-confirmation-gates.py` 输出 total 23 / violations 0
- GATE-7: 编译漂移预检绿 — check: `python3 scripts/python/probe-utils.py --action compile-embeds --check` exit 0

## Environment Prerequisites

> 本特性无外部环境依赖（无 docker / 集群 / 特殊硬件）。本机环境在生成时实测：`python3` 3.11.11、`pytest` 8.4.2 均可用（`probe: python3 --version && python3 -m pytest --version @ 2026-10-13`）。测试全部为本仓内契约/集成测试。

## Premise Measurements (generation-time, 2026-10-13)

以下全部为本运行实际执行的命令与真实输出，作为任务行内数字型前提的复测锚（implement 启动时按 T002 重新捕获冻结到 `notes/pre-change-measurements.md`）。

### PM-1 编译单元面（SC-007 基线的计数面）

```bash
# units
grep -l '^## Feedback' templates/commands/*.md | wc -l            # → 23
grep -rl '^## Feedback' .specify/skills/internal --include=SKILL.md | wc -l   # → 35
grep -rl '^## Feedback' .specify/skills/external --include=SKILL.md | wc -l   # → 11
# 非空行（计数规则：## Feedback / ## Documentation 两节非空行，截断于下一个 '^## '）
awk '...' → commands=90, internal=575, external=188，合计 853
```

- 实测输出：units commands=23, internal=35, external=11（合计 **69 单元**）；non-blank lines 90+575+188 = **853**（SC-007 冻结基线，见 plan.md § SC-007 基线）。
- **测量陷阱（naive form）**：对命令面直接 `ls templates/commands/*.md | wc -l` 得 **26**，与 23 不一致——差异是 3 个文件（instructions / constitution / feature 相关命令模板）本就没有 `## Feedback` 节。以 `grep -l '^## Feedback'` 的 23 为准。

### PM-2 feedback-utils.py 动作封闭集（迁移前）

```bash
grep -n 'choices=' scripts/python/feedback-utils.py | head -3
```

实测输出（choices 行原文）：`choices=["record", "status", "list", "dispose", "mark-submitted", "reindex", "package", "cleanup", "upstream", "probes", "map", "migrate-legacy", "probe-inject", "introspect-register"]` — 共 **14** 动作。迁移后 probe-utils.py 承载 probes/map/probe-inject + 新增 handlers/compile-embeds；feedback-utils.py 收缩为 11（[C4] 全文）。

### PM-3 门控预算（整数余量 0 的硬约束）

```bash
python3 scripts/python/scan-confirmation-gates.py
```

实测输出：`total 23`（16 destructive + 7 governance_kept）、`violations 0`；测试侧上限 cap 23.25（`tests/contract/test_confirmation_gates_sweep.py`）。本特性一切生成措辞 MUST 零 `BLOCKING_PATTERNS` 命中，否则先做预算 owner 裁定。

### PM-4 probe 注册表现状

```bash
python3 scripts/python/feedback-utils.py --action probes --validate
```

实测输出：`Probe registry valid: 6 classes, 72 internal + 0 external objects`。

### PM-5 镜像对（regen/sync 传播面）

```bash
python3 scripts/python/sync-mirrors.py --check
```

实测输出：6 MIRROR_PAIRS（templates[排除 commands/]、skills/external 363 文件、skills/internal 133、agents 2、scripts 106、shared 46）all ok；memory/ 与 docs/ 无镜像对。regen-command-copies.py 扇出到 `.claude/commands`、`.github/prompts`、`.qoder/commands`、`.opencode/command`。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- **[blockedBy: Txxx]** (optional): explicit dependency tag
- Include exact file paths in descriptions
- Manual QA/verification tasks are listed explicitly where they are separate from automated tests

### Task State Sigil (REQUIRED)

- `- [ ]` Open · `- [>]` Claimed · `- [X]` Closed · `- [~]` Deferred
- A run is complete when zero `[ ]` or `[>]` rows remain.

## Path Conventions

- 框架源面：`templates/`、`shared/`、`scripts/python/`、`skills/`（框架源，编辑在此）
- 运行时镜像面：`.specify/scripts/python/`、`.specify/shared/`、`.specify/templates/`、`.specify/skills/`（由 sync-mirrors.py 传播，不手工编辑）
- 测试面：`tests/contract/`（pytest -m contract）
- 证据面：`.specify/specs/056-probe-handler-system/notes/`

---

## Phase 1: Setup

- [ ] T001 创建运行期证据落点文件 `.specify/specs/056-probe-handler-system/notes/red-first-evidence.md`、`notes/quickstart-run.md`、`notes/pre-change-measurements.md`（三个空骨架，标题行 + 字段占位，按 `.specify/templates/tasks-template.md` 运行期证据约定）
- [ ] T002 改前基线捕获：重跑本文件 § Premise Measurements 的 PM-1..PM-5 全部命令，将真实输出冻结进 `notes/pre-change-measurements.md`（含 failing-test 基线采集：`python3 -m pytest tests/ -m contract` 全量一次，记录失败集；基线 owner：`templates/commands/implement.md` § Test runs；后续所有"零新增失败"对比以此为准）

**Checkpoint**: 基线冻结完成，后续所有对比有据可查。

---

## Phase 2: User Story 1 — 散布探测点入册，probe 成为可查询的全框架实体 (Priority: P1) 🎯 MVP

**Goal**: 050 P1–P5 升级探测、运行判定四轴与两个可用性探测、证据引擎 lane 探测以声明性元数据入册 probe-definitions.md（伞形扩格），每行挂代码锚点，契约测试与代码双向对账（零漂移、变异可红）；纯代码微探针以纯指针目录收录。

**Independent Test**: 注册表 `--validate` exit 0 且覆盖新 Class；对 `trigger-utils.py` / `run-determination.py` / `evidence-utils.py` 的具名函数/常量与注册表行双向对账，变异演练证明能红（删除一个已入册函数 → 测试转红指名锚点）。

### Tests for User Story 1 (MANDATORY) ⚠️

> 写在实现前，先证明其红（对账测试以变异演练证明能红；注册表扩格前对账测试因锚点缺失而红即自然红起点，红证据落 `notes/red-first-evidence.md`）。

- [ ] T003 [P] [US1] 编写契约测试 `tests/contract/test_probe_registry_umbrella.py`（红优先）：注册表伞形结构校验（Class/Object 两层 + 代码锚点列）+ 对 trigger-utils.py（P1–P5 升级探测具名函数）、run-determination.py（四轴 + 可用性探测具名函数/常量）、evidence-utils.py（lane 探测具名行）的双向对账（锚点存在⇔注册行存在），变异可红设计（删锚点/删注册行均须转红）
- [ ] T004 [P] [US1] 编写契约测试 `tests/contract/test_probe_nonentity_catalog.py`（红优先）：非实体 probe 目录节纯指针形态校验（每条目 = 路径 + 一行语义，禁行为规则复述）+ 微探针 exclusion 计数（writability/probe-links/git probe 等按 One Source of Truth code-first 不入册，仅目录化）

### Implementation for User Story 1

- [ ] T005 [US1] [blockedBy: T003,T004] 伞形扩格 `shared/definitions/probe-definitions.md`：头部声明升格为全框架 Probe 真源；既有 feedback 6 Class / 72 Object 行零改动；新增散布探测点 Class 与 Object 行（id / 代码锚点 / 归属切片），锚点以 T003 对账测试实际通过为准；履行 [C1] 迁移义务
- [ ] T006 [US1] [blockedBy: T005] 新增 `shared/definitions/probe-definitions.md` 「非实体 probe 目录」节：纯指针条目（writability / probe-links / git probe 等，路径 + 一行语义），满足 T004 指针形态校验
- [ ] T007 [US1] [blockedBy: T006] `scripts/python/feedback-utils.py` probes 动作适配：validate/reconcile 覆盖非实体目录节（指针可达性校验）与 scripts 切片（`--action probes` 输出含新 Class，行为向后兼容）；`.specify/scripts/python/` 镜像暂不动（T008 统一传播）
- [ ] T008 [US1] [blockedBy: T007] 镜像双写验证：`python3 scripts/python/sync-mirrors.py --write --only registry,scripts`（或等价 --only 选择器）+ `--check` 无 NEW drift；`python3 scripts/python/feedback-utils.py --action probes --validate` exit 0
- [ ] T009 [US1] [blockedBy: T008] US1 故事验证：`pytest tests/contract/test_probe_registry_umbrella.py tests/contract/test_probe_nonentity_catalog.py` 绿；变异演练（删除一个已入册代码锚点 → 对账测试转红指名锚点，恢复后复绿）证据落 `notes/red-first-evidence.md`；`--action probes` 清单含全部新 Class

**Checkpoint**: probe 成为可查询全框架实体——一次 `--action probes` 得到跨域清单，对账零漂移。MVP 完成，STOP 验证。

---

## Phase 3: User Story 2 — Handler/HandlerBinding 实体与共享引擎上线 (Priority: P1)

**Goal**: Handler（六字段封闭集）与 HandlerBinding（selector 订阅）入册；新建共享引擎 `scripts/python/probe-utils.py`：probe 族三动作自 feedback-utils.py 迁出（行为不变）+ handlers 查询动作 + compile-embeds 编译动作；feedback-utils.py 收缩为 11 领域动作（[C4] 封闭集）。

**Independent Test**: 注册临时 handler + binding 运行 compile-embeds，目标单元产物含该 handler 且既有单元产物不受影响；feedback-utils.py 全部既有 action 封闭集契约保持绿。

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T010 [P] [US2] 编写契约测试 `tests/contract/test_handler_registry.py`（红优先）：Handler 六字段封闭集（handler_id `h-` 前缀 / kind∈{engine,agent,gate} / action / mode∈{non-blocking,blocking} / order / behavior_owner 按 kind 派生形态）、HandlerBinding selector 语法（`@point:` 封闭集 + scope 封闭集）、per-unit 覆盖与 identity=(handler_id,selector,scope)、order 在生效 binding 集内唯一（重复 → exit 2）——对 [C2] 六条校验规则逐条
- [ ] T011 [P] [US2] 编写契约测试 `tests/contract/test_probe_engine_action_sets.py`（红优先）：[C4] 两个封闭集全文钉死——probe-utils.py 允许集 {probes,map,probe-inject,handlers,compile-embeds}、feedback-utils.py 允许集 {record,status,list,dispose,mark-submitted,reindex,package,cleanup,upstream,migrate-legacy,introspect-register}，双方超集/缺集均红（对 argparse choices 行解析）

### Implementation for User Story 2

- [ ] T012 [US2] [blockedBy: T009,T010] 注册表新增章节：`shared/definitions/probe-definitions.md` 增加 `## Handler` 与 `## HandlerBinding` 两章 + MVP seed 五行 handler（h-run-determination order 10 / h-feedback-record 20 / h-threshold-notice 30 / h-token-reflection 40 / h-docs-sync-eval 50，data-model.md § MVP Seed Data 为准，behavior_owner 指向 feedback-step.md / docs-step.md / run-determination.py / feedback-utils.py 实锚点）+ wrap-up 点五行 binding（scope 承载 T019 矩阵前的 MVP 骨架：complex-commands + skills 两 selector）
- [ ] T013 [US2] [blockedBy: T011,T012] 新建 `scripts/python/probe-utils.py`（stdlib-only，与 feedback-utils.py 同分布）：自 feedback-utils.py 迁出 probes/map/probe-inject 三 action（行为逐项不变，--validate/--reconcile 为 probes 的 flag）+ 新增 `--action handlers`（list/--point/--scope/--kind/--mode/--validate/--bindings，[C2]）；导出公共代码锚点供对账
- [ ] T014 [P] [US2] [blockedBy: T013] `scripts/python/feedback-utils.py` 收缩：argparse choices 移除 probes/map/probe-inject（PM-2 的 14 → 11），probe 族实现函数随迁（feedback 侧零残留）；既有 11 action 行为不变
- [ ] T015 [US2] [blockedBy: T013] 实现 `--action compile-embeds` 于 probe-utils.py：data-model.md § 7 步编译算法 + [C3]（解析 selector → 匹配单元 → 渲染单一 AUTO-GENERATED `## Wrap-up` 段 → 原子写）；零生效 handler 单元不输出段（Q5）；`--check` exit 1 漂移 / 五类 exit 2 拒写（BLOCKING_PATTERNS 命中拒绝写入——PM-3 硬约束）
- [ ] T016 [US2] [blockedBy: T014,T015] US2 引擎验证：T011 封闭集契约绿；feedback-utils.py 迁移前后对同参数输出逐字节比对（用 T002 捕获的基线输出）；`--action handlers --point wrap-up --validate` 对 seed 五行 exit 0；临时 handler+binding 注册沙箱演练（测试内）目标单元产物含新 handler、既有单元零影响
- [ ] T017 [US2] [blockedBy: T016] 镜像双写验证：sync-mirrors 传播 `scripts/` 对 + `--check` 无 NEW drift；`.specify/scripts/python/probe-utils.py` 就位且可独立调用

**Checkpoint**: "加一个 wrap-up 反应 = 注册一行 + 重编译"的机制面就绪；引擎动作封闭集双方钉死。

---

## Phase 4: User Story 3 — 手工嵌入段迁移为编译产物 (Priority: P2)

**Goal**: 69 个编译单元的收尾面从手工嵌入段迁移为单一 AUTO-GENERATED `## Wrap-up` 编译段；每单元差异（技能 runtime-mode gate、简单命令排除集）由 selector 与 per-unit 覆盖承载；传播走既有 regen/sync。

**Independent Test**: 迁移后任一复杂命令运行收尾流程行为与迁移前逐项一致（既有契约零新增失败）；两次编译 byte-identical。

### Tests for User Story 3 (MANDATORY) ⚠️

> 编译器本体已于 T015 落地，本故事测试为迁移守卫（migration/regression exception：随实现后落位并钉住既有行为语义）。

- [ ] T018 [P] [US3] [blockedBy: T015] 编写契约测试 `tests/contract/test_compile_embeds.py`（守卫，随实现落位）：确定性（两次编译 byte-identical，[C3] 对应 test_compile_embeds_determinism）、零生效单元无段（test_compile_embeds_zero_handler_no_section）、`--check` 语义（干净树 exit 0 / 产物漂移 exit 1）、横幅与标题迁移义务（[C3] title-migration duty）
- [ ] T019 [US3] [blockedBy: T002] 从 69 单元实测推导 per-unit 差异矩阵：逐单元标注 scope 归属（complex-commands / skills / 排除）与 per-unit 覆盖项（技能 runtime-mode gate、简单命令 agents/constitution/feature 排除、23 vs 26 的 3 个无反馈节命令模板），追加至 `notes/pre-change-measurements.md` § per-unit matrix
- [ ] T020 [US3] [blockedBy: T019] 按 per-unit 矩阵完善注册表 binding：scope 行与 per-unit override 行落 `shared/definitions/probe-definitions.md` ## HandlerBinding 章（T012 的 MVP 骨架补全为全量 69 单元覆盖）
- [ ] T021 [US3] [blockedBy: T018,T020] 执行迁移编译：`python3 scripts/python/probe-utils.py --action compile-embeds --write` 对全部生效单元；两次运行 byte-identical；BLOCKING_PATTERNS 命中 → 拒写并修措辞（PM-3）
- [ ] T022 [US3] [blockedBy: T021] 标题迁移义务落地（[C3]）：既有标题 pinning 测试迁移更新——`tests/contract/test_feedback_step_reference_form.py`、`test_docs_step_injection.py`、`test_feedback_command_template.py`、`test_dogfooding_practice.py` 及 041 C-5 同型断言中 `## Feedback` 字面量随标题迁移更新为 `## Wrap-up`（回归例外：随实现后修正，[blockedBy] 已体现）
- [ ] T023 [US3] [blockedBy: T021] 行为真源最小接线编辑（FR-020 裁定）：`shared/workflow/feedback-step.md` § Embedded reference forms 与 `shared/workflow/docs-step.md` 放置行中的接线引用字面量更新（行为规则零改动）
- [ ] T024 [US3] [blockedBy: T022,T023] 传播：`python3 scripts/python/regen-command-copies.py` + `python3 scripts/python/sync-mirrors.py --write`；`--check` 双绿（GATE-2 语义）
- [ ] T025 [P] [US3] [blockedBy: T024] 守卫测试落位：`tests/contract/test_compile_propagation_order.py`（compile → regen → sync 次序钉住）、`tests/contract/test_wrap_up_wording_gate_safe.py`（生成措辞零 BLOCKING_PATTERNS + 门控 total 23/violations 0）、`tests/contract/test_wrap_up_line_budget.py`（SC-007 ≤ 853 非空行预算，PM-1 计数规则）
- [ ] T026 [P] [US3] [blockedBy: T024] US3 故事验证：GATE-5 语义的手工段清零 grep（命令模板 + 技能面命中 0，编译产物内出现由 AUTO-GENERATED 横幅声明）；抽一个复杂命令（含阈值提示/自省/docs-sync 评估/运行判定）按 quickstart.md 路线走收尾流程与 T002 改前证据逐项比对，结论落 `notes/quickstart-run.md`

**Checkpoint**: 模板手术税消除——69 单元收尾面为编译产物，既有行为零回退。

---

## Phase 5: User Story 4 — 对账守卫扩展到 handler 面 (Priority: P2)

**Goal**: 编译产物 ↔ 注册表双向零缺漏 + engine action 封闭集对账 + 措辞/门控预算守卫 + order 次序契约，全部变异可红。

**Independent Test**: 构造五类破损（孤儿 handler / 缺失 handler / 非法 action / order 冲突 / 措辞命中），契约测试逐类转红且指名错误；正向树全绿。

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T027 [P] [US4] 编写契约测试 `tests/contract/test_compile_reconcile_guards.py`（红优先，五类变异矩阵）：孤儿 handler（产物含未注册 handler → exit 2）、缺失 handler（binding 声明但产物没有 → exit 2）、非法 action（engine handler 引用不存在 action → exit 2 指名 handler_id）、order 冲突（同点同生命周期两条 binding 同 order → exit 2）、措辞命中（生成段含阻塞语气句 → 转红）；order 次序契约（h-run-determination 先于 h-feedback-record / h-threshold-notice）钉住

### Implementation for User Story 4

- [ ] T028 [US4] [blockedBy: T027] `scripts/python/probe-utils.py` 补全对账守卫逻辑：reconcile（产物↔注册表双向）、handlers --validate 的 action 封闭集 import 对账（[C4] 消费引擎真实 action 集）、order 唯一性、behavior_owner 可达性校验（错误/缺失/拼写 → exit 2 指名不可达路径）、BLOCKING_PATTERNS 集成；镜像随 T030
- [ ] T029 [US4] [blockedBy: T028] US4 变异演练：五类破损逐一构造 → 对应测试转红且指名错误（证据落 `notes/red-first-evidence.md`）→ 正向树全绿；门控预算不变复测（total 23 / violations 0）
- [ ] T030 [US4] [blockedBy: T029] 镜像双写验证：sync-mirrors 传播 scripts 对 + `--check` 无 NEW drift

**Checkpoint**: 编译产物静默漂移被结构性排除——快速失败纪律对"机器给出的绿"同样成立。

---

## Phase 6: User Story 5 — 二期 binding 与词汇表/文档接线 (Priority: P3)

**Goal**: situation / phase-boundary / confirm-gate 三类二期订阅点入册并走同一编译/对账规则（044 既有 19 个 gate Object 挂 h-gate-evidence）；词汇表三新术语 + Feedback Probe 降级 + 「埋点」消歧重写；docs/reference probe 体系文档更新。

**Independent Test**: 每类 binding 独立入册后 compile 对账绿、既有领域行为契约不回退。

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T031 [P] [US5] [blockedBy: T029] 编写契约测试 `tests/contract/test_phase2_bindings.py`（红优先）：`@point:situation` / `@point:phase-boundary` / `@point:confirm-gate` binding 注册行结构校验 + 044 既有 19 个 gate Object 与 h-gate-evidence binding 对账（零缺漏）

### Implementation for User Story 5

- [ ] T032 [US5] [blockedBy: T031] 注册表二期 binding 落行：`shared/definitions/probe-definitions.md` ## HandlerBinding 章追加三类 binding（situation / phase-boundary / confirm-gate + h-gate-evidence 行，data-model.md 为准）；`--action probes --validate` 覆盖新点
- [ ] T033 [US5] [blockedBy: T032] 二期编译与对账：`compile-embeds --write` + reconcile 绿；044 既有门控证据契约零回退（`pytest tests/ -k gate_evidence` 或对应既有测试文件）；GATE-6 复测
- [ ] T034 [P] [US5] [blockedBy: T009] 词汇表更新 `.specify/memory/glossary.md`（宿主面，无镜像对）：新增 Probe（伞形）/ Handler / HandlerBinding 三术语（origin=auto status=proposed 起步、本轮内由本运行确认），Feedback Probe 条目降为域实例表述，「埋点」消歧条目重写指向伞形定义
- [ ] T035 [P] [US5] [blockedBy: T017] docs/reference 更新：probe 体系文档（probe 五动作 CLI 面、Handler/HandlerBinding 模型、宿主只读边界 Q6）落 `docs/reference/skills/probe.md`（或按 Documentation Map 既有 probe 文档位修正），保持 One Source of Truth 指针形态

**Checkpoint**: 全生命周期点订阅面与词汇/文档接线完成。

---

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T036 [P] 全量契约测试回归：`python3 -m pytest tests/ -m contract` 对比 T002 基线零新增失败（含既有 feedback 域 14→11 动作面、028 六 Class 语义、041/044/050/053/055 交叉特性契约）
- [ ] T037 [P] quickstart.md 四场景全程走查（注册+重编译 / 漂移预检+对账 / 零生效单元 / 动作集对账），结论落 `notes/quickstart-run.md`
- [ ] T038 终检 sweep：GATE-1..GATE-7 逐条执行并记录输出（sync-mirrors --check / regen --check 双绿、compile-embeds --check exit 0、门控 total 23/violations 0、手工段清零、tasks.md 开放行 0）

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 无依赖，先行
- **Phase 2 (US1, P1)**: 依赖 T001/T002（基线）——MVP
- **Phase 3 (US2, P1)**: 依赖 US1（T009）——实体与引擎
- **Phase 4 (US3, P2)**: 依赖 US2（T017）+ T019 矩阵——迁移兑现面
- **Phase 5 (US4, P2)**: 依赖 US3（T024）——对账守卫覆盖迁移后的树
- **Phase 6 (US5, P3)**: 依赖 US4（T029/T030）；T034/T035 可提前（blockedBy 已标注更早锚点）
- **Phase 7 (Polish)**: 依赖全部故事完成

### User Story Dependencies

- US1 → US2 → US3 → US4 → US5 严格串联（实体 → 引擎 → 迁移 → 守卫 → 扩面）
- 故事内：测试行先于实现行（红优先）；迁移/回归例外行（T018/T022/T025）以 [blockedBy] 显式置于实现后

### Parallel Opportunities

- T003+T004（US1 两个测试文件，不同文件）
- T010+T011（US2 两个测试文件）
- T014+T015（feedback 收缩 vs compile-embeds 实现，均只依赖 T013，不同动作面）
- T025+T026、T027（跨故事守卫与验证行）、T034+T035、T036+T037（各自不同文件/面）
并行标记（[P]）已按"写目标不同文件"校准；同文件写行均已串行化。（Parallel Opportunities 与 Notes 小节的说明行均非任务行，任何 `^- \[` 计数工具应排除本节。）

## Implementation Strategy

### MVP First

1. Phase 1 Setup（基线冻结）
2. Phase 2 US1 全绿（probe 可查询实体）——**STOP AND VALIDATE**
3. MVP = US1（requirements.md P1 双故事中 US1 独立可交付：无 Handler 层也有跨域可查询清单）

### Incremental Delivery

US1 → US2（机制面）→ US3（价值兑现面）→ US4（守卫）→ US5（扩面）→ Polish。每故事 Checkpoint 独立可验证。

### Single Developer

按 ID 顺序执行即拓扑序——[blockedBy] 已完整编码依赖，顺序行进即可。

## Notes

[P] 任务 = 不同文件、无依赖
- 每个 US 相位有独立 Checkpoint；验证行（T009/T016/T026/T029/T038）为显式 QA 任务
- 全部数字型前提已在本文件 § Premise Measurements 留复测命令与真实输出；implement 启动时按 T002 重测冻结
- **Deferral discipline**: 无 [~] 行；如 implement 阶段遇外部阻塞，按模板语义转 [~] 并在 verification.md 记 deferred_tasks
