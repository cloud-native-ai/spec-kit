# Tasks: Feedback 机制的 Probe 化重构(反馈插点 + 切片定向 + 三模式管理命令 + 外部 probe)

**Requirement ID**: 041
**Requirement Key**: 041-refactor-feedback-probe
**Related Feature**: 028 Feedback Mechanism
**Input**: Design documents from `.specify/specs/041-refactor-feedback-probe/`
**Prerequisites**: plan.md ✅, requirements.md ✅, data-model.md ✅, contracts/ ✅(×4), quickstart.md ✅, feature-ref.md ✅

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation"(integration/contract tests MUST cover cross-service communication)强制测试先行;模板/命令面适用宪法 template-only 门(结构契约测试:内容/标题/镜像 parity 断言),引擎面适用运行时契约测试。两类测试均已按 story 置顶。

**Organization**: Tasks are grouped by user story to enable independent implementation and testing. 本 spec 为「引擎代码 + 模板/定义」混合形态:引擎任务走 Tests→Implementation,模板任务走 doc-feature taxonomy(author-section / mirror-parity / render-verify)。

## Definition of Done (DoD)

- DoD-1: 引擎与模板实现符合 requirements.md 21 FR 与 contracts/×4 的每条 MUST 断言
- DoD-2: 全部新增契约测试通过(4 个测试文件),全量 suite 相对基线零新增失败
- DoD-3: plan.md Mirror Obligations 五行全部 `sync-mirrors.py --check` exit 0 覆盖
- DoD-4: SC-001~008 逐条在 verification.md 记录状态与证据命令输出
- DoD-5: docs/reference/commands/feedback.md 新增、docs/reference/skills/feedback.md 分类表更新(18→19)
- DoD-6: 本仓库旧格式反馈条目迁移完成(legacy_remaining=0)且 migration-log.md 留痕

**DoD Status**: pending

## Completion Gate

- GATE-1: 零新增测试失败 — check: `python3 -m pytest tests/ -q 2>&1 | tail -5` 与 `.specify/specs/041-refactor-feedback-probe/baseline-failed.txt` 按名比对,新增失败为 0
- GATE-2: 全部镜像一致 — check: `python3 scripts/python/sync-mirrors.py --check; echo $?`(期望 0)
- GATE-3: 无开放任务行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/041-refactor-feedback-probe/tasks.md`(期望 0)
- GATE-4: SC 全覆盖 — check: `grep -oE 'SC-[0-9]{3}' .specify/specs/041-refactor-feedback-probe/verification.md | sort -u`(期望 SC-001..SC-008)
- GATE-5: probe 对账守恒 — check: `python3 .specify/scripts/python/feedback-utils.py --action probes --reconcile; echo $?`(期望 0;50 Object = 49 既有 + feedback 自身,与嵌入清单 19 commands + 31 skills 双向零缺漏)
- GATE-6: 外部隔离 — check: 测试工作区 package 后 `unzip -p <zip> '*.md' | grep -c '^kind: external'`(期望 0;`-p` 流式读取包内文件**内容**而非文件名清单)且 `unzip -p <zip> MANIFEST.md | grep -ci external`(期望 0)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: US1~US6 per requirements.md;Setup/Foundational/Polish 无标签
- **[blockedBy: Txxx]**: 显式依赖;`/speckit.implement` 按此拓扑排序并拒绝阻塞未闭合的任务
- 路径均为仓库根相对路径

### Task State Sigil (REQUIRED)

- `- [ ]` Open · `- [>]` Claimed(多 agent)· `- [X]` Closed · `- [~]` Deferred(理由记入 verification.md `deferred_tasks=`)

## Path Conventions

- 引擎:`scripts/python/feedback-utils.py`(canonical)→ `.specify/scripts/python/` 镜像
- 定义/模板:`shared/`、`templates/`(canonical)→ `.specify/` 镜像 + 6 工具命令副本
- 测试:`tests/contract/`(沿 `test_feedback_*.py` 命名)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 基线与迁移面快照(全任务的参照系)

**Environment Prerequisites**: 无外部依赖 — 仅需 `python3`(>=3.8)与 `pytest`(仓库 venv)。

- [X] T001 运行全量测试套件并按名记录失败基线到 `.specify/specs/041-refactor-feedback-probe/baseline-failed.txt`(`python3 -m pytest tests/ -q`;只记失败测试名,后续 GATE-1 以此比对)
- [X] T002 [P] 快照隐式反馈点清单到 `.specify/specs/041-refactor-feedback-probe/embed-inventory.txt`:grep `## Feedback` 于 `templates/commands/*.md` 与 `skills/*/SKILL.md`,产出 49 行(18 command + 31 skill,计数用 `grep -c` 实测,不硬编码);此清单是 T006 的 Object 映射输入与 GATE-5 的对账基准(快照时点 49;T018 落地后基准更新为 50,以实施时实测为准)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 引擎的 probe 注册表解析核心(全部 story 的依赖)

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 编写失败的注册表契约测试 `tests/contract/test_feedback_probe_registry.py`:按 `contracts/probe-registry.md` C-2/C-3/C-4(schema、五特征非空、kind 枚举、object 唯一、unit 语法、`ext-` 前缀)用 tmp 工作区夹具断言 `--action probes --validate` 的通过/违规(exit 2)两态
- [X] T004 [blockedBy: T003] 在 `scripts/python/feedback-utils.py` 实现注册表加载器(框架真源 `shared/definitions/probe-definitions.md` + 项目外部 `.specify/memory/feedback/probes/*.md` 合并)与 `--action probes --format json` / `--validate`(engine-cli C-3.1/C-3.2)
- [X] T005 [blockedBy: T004] 实现 `--action probes --reconcile`:对运行仓库实况 grep 嵌入点,输出双向缺漏清单,零缺漏 exit 0(engine-cli C-3.3;registry C-5)

**Checkpoint**: `probes --validate/--reconcile` 可对夹具运行;story 实现可并行开始

---

## Phase 3: User Story 1 - 反馈点成为显式建模的 Feedback Probe(Class/Object 两层) (Priority: P1) 🎯 MVP

**Goal**: probe 真源落盘——3 Class + 49 Object 全部归类,对账守恒(SC-001)
**Independent Test**: `--action probes --reconcile` exit 0,且 `--validate` 五特征完备

### Implementation for User Story 1

- [X] T006 [US1] [blockedBy: T002, T004] 撰写真源 `shared/definitions/probe-definitions.md`:按 `contracts/probe-registry.md` C-2/C-3 与 data-model §1/§2 —— `## Classes` 3 行(command-wrapup / skill-wrapup / external-custom)、`## Objects` 49 行(object_id 自 unit 派生,逐行映射 T002 清单)、`## Slices` 枚举、外部登记契约节(C-4 规则文本)
- [X] T007 [US1] [blockedBy: T005, T006] 运行 `probes --validate` 与 `--reconcile` 至全绿;将输出(49 对 49 双向零缺漏、无未归类 Object)存为 SC-001 证据到 `.specify/specs/041-refactor-feedback-probe/verification-scratch/sc-001.txt`
- [X] T008 [US1] [blockedBy: T006] mirror-parity:`python3 scripts/python/sync-mirrors.py --write` 后 `--check` exit 0;`diff -q shared/definitions/probe-definitions.md .specify/shared/definitions/probe-definitions.md` 零差异

**Checkpoint**: US1 独立可测——真源即机制本体;49 点显式化完成

---

## Phase 4: User Story 2 - 项目级 Feedback Probe 结构图 (Priority: P1) 🎯 MVP

**Goal**: `--action map` 派生结构图,重建零漂移(SC-003)
**Independent Test**: 同真源两次 `--action map` 产出逐字节一致;受控修改后差异仅在对应条目

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T009 [US2] [blockedBy: T004] 创建引擎契约测试 `tests/contract/test_feedback_probe_cli.py` 首批用例(map 幂等零差异、覆盖度=合并真源、Class→Object 分组与内外标注,engine-cli C-7);先失败后实现

### Implementation for User Story 2

- [X] T010 [US2] [blockedBy: T009] 在 `scripts/python/feedback-utils.py` 实现 `--action map`:整体重建 `.specify/memory/feedback/probe-map.md`(竖状树 + Mermaid 源码块 + 明细表,见 data-model §6);不读旧文件、无合并语义
- [X] T011 [US2] [blockedBy: T010] render-verify:生成 probe-map.md,Mermaid 块结构校验(节点数=Class+Object 数),连续两次执行 `diff` 零差异;证据存 `verification-scratch/sc-003.txt`

**Checkpoint**: US2 独立可测——图 = 真源函数,SC-003 可判

---

## Phase 5: User Story 3 - 反馈按系统切片定向 (Priority: P1) 🎯 MVP

**Goal**: 条目经 Object→Class 继承 probe/kind/slice,过滤程序化(SC-002/004)
**Independent Test**: 夹具库含 ≥3 切片段落,`list --slice X` 一步命中且不含其它切片

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T012 [US3] [P] [blockedBy: T004] 编写失败测试:扩展 `tests/contract/test_feedback_probe_entry_schema.py`(probe/kind/slice frontmatter、无对应 Object 时 exit 2、disposition 只经处置动作,entry-schema C-1)并在 `tests/contract/test_feedback_probe_cli.py` 追加 `--slice/--kind/--disposition` 过滤用例(engine-cli C-2)

### Implementation for User Story 3

- [X] T013 [US3] [blockedBy: T012] 在 `scripts/python/feedback-utils.py` 实现 record 的 probe 自动解析(unit_id→Object;失败 exit 2 报 `no probe object for unit`)与 frontmatter/index 新键(probe/kind/slice/disposition,entry-schema C-1/C-4;不接受手工 kind/slice 覆盖)
- [X] T014 [US3] [blockedBy: T013] 实现 `list --slice/--kind/--disposition` 过滤(引擎端程序判定,输出保持摘要级)
- [X] T015 [US3] [blockedBy: T013] mirror-parity:引擎镜像 `sync-mirrors.py --write` + `--check` exit 0;`diff -q scripts/python/feedback-utils.py .specify/scripts/python/feedback-utils.py` 零差异

**Checkpoint**: US3 独立可测——切片消费闭环成立;MVP(US1+US2+US3)齐备,STOP 验证

---

## Phase 6: User Story 4 - /speckit.feedback 三种执行模式 (Priority: P2)

**Goal**: 新复杂命令(总览/处理含打包后清理/注入入口)+ 分发镜像 + 文档(doc-feature 形态)
**Independent Test**: 无参数渲染出与真源一致的 probe 竖状总览;模式二完成 查看→过滤→处置→打包→清理 闭环

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T016 [US4] [blockedBy: T014] 编写失败测试:`tests/contract/test_feedback_command_template.py`(模板存在、三模式章节、`## Feedback`+`## Documentation` 步、现存工具副本面——清单由 regen 现存目录探测动态派生,本仓实测 4——存在且含 AUTO-GENERATED 头,feedback-command C-1)+ 在 `test_feedback_probe_cli.py` 追加 cleanup 用例(engine-cli C-5);同步更新 `tests/contract/test_feedback_command_classification.py` 分类计数(复杂命令 +feedback,计数改动与命令落地同任务,沿 Pin Hygiene 规则 3)

### Implementation for User Story 4

- [X] T017 [US4] [blockedBy: T016] 在 `scripts/python/feedback-utils.py` 实现 `--action cleanup --package <zip|latest> [--dry-run]`(仅删包内实际收录条目,先校验 zip+MANIFEST,追加 `cleanup-log.md`,计数重算;engine-cli C-5)
- [X] T018 [US4] [blockedBy: T005, T014, T017] 撰写 `templates/commands/feedback.md`(canonical,复杂命令):三模式执行流程(模式一调 `probes` 渲染竖状总览;模式二 status/list 过滤→处置→package→cleanup;模式三引导 `probe-inject`)+ canonical `## Feedback` 步 + docs-step,依 `contracts/feedback-command.md`;**同任务**在 `shared/definitions/probe-definitions.md` 的 `## Objects` 增行 `speckit-feedback-wrapup | command-wrapup | /speckit.feedback | wrap-up` 并重跑 `--action probes --reconcile`(19+31=50 双向零缺漏,registry C-3.4)
- [X] T019 [US4] [blockedBy: T018] mirror-parity:`sync-mirrors.py --write` 生成 `.specify/templates/commands/feedback.md` 与现存工具副本面(本仓实测 4:`.claude/commands/speckit.feedback.md`、`.github/prompts/speckit.feedback.prompt.md`、`.qoder/commands/speckit.feedback.md`、`.opencode/command/speckit.feedback.md`;codex/hermes 由 `specify init` 下游分发);逐副本 grep 三模式关键节 + AUTO-GENERATED 头
- [X] T020 [US4] [P] [blockedBy: T018] 文档:新增 `docs/reference/commands/feedback.md`(三模式用法/退出码,与 quickstart 一致);更新 `docs/reference/skills/feedback.md` 分类表(复杂命令 +feedback)与 probe 化机制段
- [X] T021 [US4] [blockedBy: T017, T019] 手动 QA(quickstart §1~2):scratch 项目内无参数总览 ↔ `probes --format json` 一致;记录一条真实反馈→package→`cleanup --dry-run` 预览→执行清理,对账活跃库清空与包内留档;证据存 `verification-scratch/sc-007-mode12.txt`

**Checkpoint**: US4 独立可测——用户无需手工调引擎即可完成三类诉求

---

## Phase 7: User Story 5 - 旧格式条目收敛处置,红线不破 (Priority: P2)

**Goal**: migrate-legacy 一次性收敛本仓库旧条目,处置留痕(SC-005/006)
**Independent Test**: 迁移后 `status` 报 `legacy_remaining: 0`,migration-log.md 逐条可审计

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T022 [US5] [blockedBy: T013] 编写失败测试:在 `test_feedback_probe_cli.py` 追加 migrate-legacy 用例(计划执行 delete/re-register、`legacy_remaining` 计数、重登记条目 `migrated_from` 保留;engine-cli C-8、entry-schema C-2)

### Implementation & Migration for User Story 5

- [ ] T023 [US5] [blockedBy: T022] 实现 `--action migrate-legacy --plan-file <plan>` 与 `status` 的 `legacy_remaining`/`external_count` 输出;migration-log.md 逐条记录(id|delete|re-register|rationale|date)
- [ ] T024 [US5] [blockedBy: T023] agent 整体 review 本仓库 `.specify/memory/feedback/` 旧格式条目(逐条核对优化点是否已合入或已过时),产出处置计划 `.specify/memory/feedback/migration-plan.md`,**停点:向用户确认计划后**方可执行
- [ ] T025 [US5] [blockedBy: T024] 执行迁移(`migrate-legacy --plan-file`)并验证 `legacy_remaining: 0`、重登记条目可按新格式检索、计数重算不重复触发提示;证据存 `verification-scratch/sc-005.txt`

**Checkpoint**: US5 独立可测——旧格式归零且全程留痕

---

## Phase 8: User Story 6 - 外部 probe:宿主项目自定义单元的本地反馈环 (Priority: P2)

**Goal**: probe-inject + 外部条目隔离(不上送、可单独过滤)(SC-008)
**Independent Test**: 注入外部 probe → 产出 `kind=external` 条目 → package 包内该条目出现 0 次

### Tests for User Story 6 (MANDATORY) ⚠️

- [ ] T026 [US6] [blockedBy: T004] 编写失败测试:在 `test_feedback_probe_cli.py` 追加 probe-inject 用例(`ext-` 前缀派生、冲突 exit 2、`custom:` unit 语法;engine-cli C-6)与 package 排除用例(外部条目 0 入包、`excluded_external` 计数、MANIFEST probe/slice 列;engine-cli C-4)

### Implementation for User Story 6

- [ ] T027 [US6] [blockedBy: T026] 实现 `--action probe-inject --unit custom:<owner>/<name> [--lifecycle-point] --notes-file`:写 `.specify/memory/feedback/probes/ext-<slug>.md`(registry C-4 schema),注入即入合并真源
- [ ] T028 [US6] [blockedBy: T027] 实现 package 外部排除 + MANIFEST 增列(probe/slice)+ JSON 输出 `excluded_external` 计数(engine-cli C-4);record 支持 `custom:` unit(`unit_type=custom-unit`,entry-schema C-3)
- [ ] T029 [US6] [blockedBy: T013] 更新 canonical 步骤 `shared/workflow/feedback-step.md`:record 经 probe 自动解析的说明、外部自定义单元的记录指引;**同步受牵连的内嵌副本**(canonical 块要求逐字内嵌——覆盖 plan.md Mirror Obligations 行 5):受措辞改动影响的 18 个 `templates/commands/*.md` 内嵌 `## Feedback` 节与 31 个 `skills/*/SKILL.md` 内嵌节同批更新,经 `python3 scripts/python/sync-mirrors.py --write` 再生 `.specify/` 镜像与各工具命令副本,逐副本 grep 新措辞核对(与 T019/T031 的镜像写操作串行执行,避免 `--write` 竞争)
- [ ] T030 [US6] [blockedBy: T028, T011] 手动 QA(quickstart §3~4):scratch 项目注入样例外部 probe → 模式一总览与 `--action map` 均含 `ext-*` 对象 → 记录一条外部条目 → package 后 `unzip -p <zip> '*.md' | grep -c '^kind: external'` 断言 0 并核 MANIFEST 无 external 行(与 GATE-6 同口径);证据存 `verification-scratch/sc-008.txt`

**Checkpoint**: US6 独立可测——Loop B 本地反馈环闭合

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: 跨 story 收敛与全仓一致性

- [ ] T031 [blockedBy: T008, T015, T019, T029] 全仓镜像终检:`python3 scripts/python/sync-mirrors.py --check` exit 0(覆盖 plan.md Mirror Obligations 已触发的各行;行 5 的「再生副本含编辑」由 T029 的逐副本 grep 核验承担,`--check` 不提供该证明)
- [ ] T032 [blockedBy: T021, T025, T030] 全量 suite 复跑并与 T001 基线按名比对,零新增失败;记录到 verification-scratch
- [ ] T033 [P] 刷新工具记录 `.specify/memory/tools/feedback-utils.py.md`:新增 5 动作与新旗标入 Parameters/Behavioral Rules,Discovery Notes 记复验日期
- [ ] T034 [blockedBy: T031, T032] 撰写 `.specify/specs/041-refactor-feedback-probe/verification.md`(SC-001~008 逐条状态+证据路径);更新 `features/028.md`(Implemented 描述扩展)与 `features.md` 行 Notes(交付记录)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 立即开始;T002 是 T006 的输入
- **Foundational (Phase 2)**: 依赖 Setup;**阻塞全部 story**
- **US1 (Phase 3)**: 依赖 T002+T004;产出真源后 US2/US3/US6 的运行时验证才有数据
- **US2 (Phase 4)** / **US3 (Phase 5)**: 依赖 T004(解析核心);彼此独立,可并行
- **US4 (Phase 6)**: 依赖 T005+T014+T017(命令是引擎动作的编排面)
- **US5 (Phase 7)**: 依赖 T013(新条目 schema 先行)
- **US6 (Phase 8)**: 依赖 T004;T030 另依赖 T011(map 呈现外部对象)
- **Polish (Phase 9)**: 依赖全部 story

### User Story Dependencies

- US1(真源)→ US2/US3/US6 的运行时验证;US3(schema)→ US5;US4 编排 US1/US2/US3/US6 的既有能力
- 均保持独立可测:每 story 的 Independent Test 不要求其它 story 先绿

### Within Each User Story

- 引擎任务:Tests(先失败)→ Implementation → mirror-parity
- 模板任务:author-section → mirror-parity → render-verify / manual QA
- 共享测试文件串行化:`test_feedback_probe_cli.py` 由 US2 创建,US3/US4/US5/US6 追加 — 这些追加任务不可跨 story 并行标 [P](同文件),已按 phase 顺序串行

### Parallel Opportunities

- T002 与 T001 并行(不同文件)
- T009(US2 建 cli 测试)与 T012(US3 建 schema 测试)并行(不同文件)
- T020(docs)与 T017(cleanup 引擎)并行(不同文件,在 T016 后)
- T027/T028(引擎)与 T020/T029 可交错;凡执行 `sync-mirrors.py --write` 的任务(T008/T015/T019/T029/T031)彼此串行,避免镜像写竞争

---

## Parallel Example: User Story 3

```bash
# T015(engine mirror)完成后,US6 的 T029 可交错推进(镜像写与其它 --write 串行):
Task T029: 更新 shared/workflow/feedback-step.md + 内嵌副本同步 + 再生核对
# 同时另一 worker 处理 US5:
Task T023: 实现 migrate-legacy(test_feedback_probe_cli.py 由其独占追加)
```

---

## Implementation Strategy

### MVP First

**MVP scope rule**: 三个 P1 story(US1 真源建模 + US2 结构图 + US3 切片定向)共同构成最小独立可用增量——建模(US1)若无消费面(US3)是半个机制,故 MVP 覆盖全部 P1。

1. Complete Phase 1: Setup(基线 + 49 点快照)
2. Complete Phase 2: Foundational(解析核心)
3. Complete US1 → US2 → US3(或 US2 ∥ US3)
4. **STOP and VALIDATE**: 逐 story 跑 Independent Test(reconcile 全绿 / map 零漂移 / 切片一步过滤)
5. 其后按 P2 顺序 US4(命令面)→ US5(迁移)→ US6(外部 probe)→ Polish

### Incremental Delivery

1. Foundation → US1(机制本体,可独立演示 `probes --validate/--reconcile`)
2. +US2(结构图,SC-003 可判)→ +US3(切片消费,SC-002/004 可判)= MVP
3. +US4(用户入口)→ +US5(旧库收敛)→ +US6(Loop B 扩展)
4. Polish:镜像终检/基线复跑/工具记录/verification

### Parallel Team Strategy

1. 共同完成 Setup + Foundational
2. Developer A: US1→US2;Developer B: US3→US5;Developer C: US4 文档面(T020/T021 前置阅读)
3. US6 在 T004 后任意 worker 接手(注意 cli 测试文件串行)

---

## Notes

- [P] 任务 = 不同文件且无未闭合依赖
- 契约测试文件与 contracts/ 一一对应:probe-registry→test_feedback_probe_registry.py、engine-cli→test_feedback_probe_cli.py、entry-schema→test_feedback_probe_entry_schema.py、feedback-command→test_feedback_command_template.py
- Pin Hygiene:49 与 18→19 均为「计数即契约」(SC-001/分类表),改动人口的任务同任务更新;其余计数一律 `len(glob)` 派生
- T024 是唯一用户停点(迁移计划确认);其余任务均可自动推进
- Commit 节奏:每 story Checkpoint 后提交一次
