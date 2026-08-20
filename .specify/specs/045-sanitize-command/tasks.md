# Tasks: 框架资料卫生治理——残留冗余清理与关键资料正确性检查(Sanitize Command)

**Requirement ID**: 045  
**Requirement Key**: 045-sanitize-command  
**Related Feature**: 047 Framework Material Hygiene(框架资料卫生)  
**Input**: Design documents from `.specify/specs/045-sanitize-command/`  
**Prerequisites**: plan.md(required), requirements.md(required), data-model.md, contracts/(4), quickstart.md, feature-ref.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation"(NON-NEGOTIABLE:tests BEFORE implementation,pure functions MUST have unit tests);本需求为混合形态——引擎(runtime code)走 unit/integration/contract 三层,命令模板(template-only artifact)按宪法 §IV "Template-only features" 条款走结构契约测试(content/heading/mirror-parity 断言)。

**Environment Prerequisites**: 无外部环境依赖——python3(≥3.8)与本仓 git 均已在生成时确认可用;全部夹具为本地文件系统 + 本地 git 迷你仓,无需 docker/网络/集群。

## Definition of Done (DoD)

- DoD-1: 引擎 `scripts/python/sanitize-utils.py` 按 contracts/sanitize-engine.md 实现:恰 4 个 action(collect/record/status/apply)、退出码 0/1/2、写入仅限台账/计划/处置目标、范围红线(越界 target 拒绝)全部生效
- DoD-2: 全部自动化测试通过(unit/integration/contract),全套件相对 recorded baseline 零新增失败
- DoD-3: plan.md Mirror Obligations 三行全部核验:引擎镜像 diff -q 一致、probe-definitions 镜像 diff -q 一致、4 份工具副本经 regen 传播且 `regen --check` 零 stale;`sync-mirrors --check` exit 0
- DoD-4: 登记面同步:复杂命令分类 17→18、044 门控 baseline total +1、`.specify/memory/tools/sanitize-utils.py.md` Tool 记录、`docs/reference/commands/sanitize.md` 用户文档
- DoD-5: 本仓 dogfood 检查运行已执行并如实报告发现(含真实过期 parked todo 的提交级证据)
- DoD-6: requirements.md 的 SC-001..SC-005 逐条在 verification.md 有状态与证据记录

**DoD Status**: pending

## Completion Gate

- GATE-1: 全套件零新增失败 — check: `python3 -m pytest tests/ -q` 后与 `.specify/specs/045-sanitize-command/baseline-failed.txt` 做名字级失败集合 diff(comm -13 baseline current 为空)
- GATE-2: 镜像义务逐行核验 — check: `diff -q scripts/python/sanitize-utils.py .specify/scripts/python/sanitize-utils.py`;`diff -q shared/definitions/probe-definitions.md .specify/shared/definitions/probe-definitions.md`;`python3 scripts/python/sync-mirrors.py --check` exit 0
- GATE-3: 无未决任务行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/045-sanitize-command/tasks.md` 返回 0
- GATE-4: verification.md 覆盖全部 SC — check: 对 requirements.md 的 SC-001..005 逐一 grep verification.md
- GATE-5: 门控治理无回流 — check: `python3 scripts/python/scan-confirmation-gates.py` violations 为空,total = baseline+1(新破坏性清理门控计入 keep_gate)
- GATE-6: 命令副本零 stale — check: `python3 scripts/python/regen-command-copies.py --check` 零 "stale, no source template",4 份 speckit.sanitize 副本存在

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 / US2 / US3(mapping to requirements.md user stories)
- **[blockedBy: Txxx]**: explicit dependency tag;task MUST NOT start until every listed task is `[X]`
- 每条任务含精确文件路径

### Task State Sigil (REQUIRED)

- `- [ ]` Open / `- [>]` Claimed / `- [X]` Closed / `- [~]` Deferred(reason recorded in verification.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结测试基线,区分既有失败与本需求回归

- [X] T001 冻结全套件测试基线:运行 `python3 -m pytest tests/ -q`,把名字级失败清单写入 `.specify/specs/045-sanitize-command/baseline-failed.txt`(既有失败不构成本需求回归)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 引擎骨架 + 台账/Schema/合并语义 + 资料根枚举——全部用户故事的公共地基

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 [P] 契约测试(RED):引擎 CLI 面——恰 4 个 action、未知 action 退出 1(JSON error)、退出码表 0/1/2、JSON 输出信封,写入 `tests/contract/test_sanitize_engine_contract.py`(锚 contracts/sanitize-engine.md §1/§3/§6)
- [X] T003 [P] 单元测试(RED):台账原语与合并语义——原子写(.part+os.replace)、损坏重建+note、稳定 ID=sha1(category|target)[:12]、schema 校验 C-1..C-7、合并规则 C-8..C-13、部分扫描防误销账 C-14、资料根枚举与白名单,写入 `tests/unit/test_sanitize_store.py`(锚 contracts/sanitize-findings.md)
- [X] T004 引擎骨架 `scripts/python/sanitize-utils.py`:argparse(--action/--workspace-root/--format/--file/--plan/--roots)、动作分发、CliError→退出 1 + JSON error 信封(GREEN for T002)[blockedBy: T002]
- [X] T005 台账/Schema/合并/资料根实现 `scripts/python/sanitize-utils.py`:findings.json 读写原子化、schema 校验全有或全无、六类合并语义、资料根表(data-model §4)与自检豁免、用户代码排除模式(GREEN for T003)[blockedBy: T003, T004]

**Checkpoint**: 引擎可运行四个动作的空实现;store 契约测试转绿

---

## Phase 3: User Story 1 - 过期残留检测:报告持久化先行,被检材料零修改 (Priority: P1) 🎯 MVP

**Goal**: 检查模式扫描时间性声明材料,采集证据包,语义判定入账(pending),台账/摘要/status 可用

**Independent Test**: 在复刻真实案例的夹具上走 collect → 判定 → record → status,断言过期残留发现携带提交级证据引用、被检材料零变更(quickstart 走查 1)

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE**: Write these tests FIRST, ensure they FAIL before implementation

- [X] T006 [P] [US1] 夹具 `tests/fixtures/sanitize/stale-todo/`:本地迷你 git 仓 + parked todo(声明"未落地"五项,引用具体路径)+ 已合入提交(触碰所引路径)——真实案例(20260812 todo vs 1a090c72)的复刻,SC-001 度量源
- [X] T007 [P] [US1] 单元测试(RED):语义候选采集——claims 机械抽取(frontmatter 日期 + 状态声明短语)、证据包(gitLog 截断 20 行、pathExistence 映射)、git 不可用降级 note,写入 `tests/unit/test_sanitize_semantic.py`(锚 contracts/sanitize-detection-rules.md §5 C-14..C-16)

### Implementation for User Story 1

- [X] T008 [US1] 实现 collect 的语义候选采集 `scripts/python/sanitize-utils.py`:memory-todo/draft 根扫描、claims/evidencePack 组装、git 子进程(超时/失败→证据不足)[blockedBy: T005, T006, T007]
- [X] T009 [US1] 实现 collect 的确定性发现合并与 status 动作 `scripts/python/sanitize-utils.py`:台账摘要信封、零写入 status[blockedBy: T008]
- [X] T010 [US1] 实现 record 动作 `scripts/python/sanitize-utils.py`:--file schema 校验(违例退出 2 且全有或全无)、语义发现按合并语义入账、"证据不足"候选拒绝[blockedBy: T009]
- [X] T011 [US1] 集成测试 `tests/integration/test_sanitize_us1.py`:US1 全流程断言——发现含 commit 证据引用(SC-001)、被检材料快照零变更且写入仅落台账(SC-002)、证据不足候选不入账[blockedBy: T010]

### Manual Verification for User Story 1

- [X] T012 [US1] 手工走查:按 quickstart.md 走查 1 在临时目录副本上执行引擎三命令,核对输出信封与台账状态[blockedBy: T011]

**Checkpoint**: US1 独立可测——过期残留检出 + 台账持久化 + 零材料修改全部成立(MVP 达成)

---

## Phase 4: User Story 2 - 关键资料正确性检查:死引用、索引一致性与镜像漂移 (Priority: P2)

**Goal**: 四类确定性检查器接入 collect,全部判定程序化,发现并入同一台账

**Independent Test**: correctness 夹具上运行 collect,断言四类发现全部检出、detection=programmatic、修复后重跑自动收敛(quickstart 走查 3)

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T013 [P] [US2] 夹具 `tests/fixtures/sanitize/correctness/`:死引用材料(链接/路径/命令/技能四形态 + 围栏豁免 + 占位符豁免)、features 索引双向缺项、断链+被替换为普通文件的链接、孤儿镜像目录(已注册/未注册两态)
- [X] T014 [P] [US2] 单元测试(RED):死引用抽取语法,写入 `tests/unit/test_sanitize_checks_refs.py`(锚 contracts/sanitize-detection-rules.md §1 C-1..C-5)
- [X] T015 [P] [US2] 单元测试(RED):索引一致性与符号链接检查器,写入 `tests/unit/test_sanitize_checks_index.py`(锚 §2/§3 C-6..C-10)
- [X] T016 [P] [US2] 单元测试(RED):镜像漂移检查器(sync-mirrors --check 解析 + 孤儿目录 + obsolete 交叉核对),写入 `tests/unit/test_sanitize_checks_mirror.py`(锚 §4 C-11..C-13)

### Implementation for User Story 2

- [X] T017 [US2] 实现死引用检查器 `scripts/python/sanitize-utils.py`:自有语法(材料根)+ docs 树 lane 复用 docs_utils 导入(C-4)[blockedBy: T013, T014]
- [X] T018 [US2] 实现索引一致性与符号链接检查器 `scripts/python/sanitize-utils.py`:features/feedback/evidence 三族双向 + 固定链接集三态判定 + delegate 处置[blockedBy: T013, T015]
- [X] T019 [US2] 实现镜像漂移检查器 `scripts/python/sanitize-utils.py`:sync-mirrors --check 子进程解析、孤儿目录补检、未注册改名残留 severity=high[blockedBy: T013, T016]
- [X] T020 [US2] 集成测试 `tests/integration/test_sanitize_us2.py`:四类发现全检出且 detection=programmatic(SC-004)、severity 默认映射、修复一项后重跑自动收敛(C-10)、--roots 子集不误销账(C-14)[blockedBy: T017, T018, T019]

**Checkpoint**: US1+US2 独立成立——确定性检查零 LLM 参与,台账自动收敛闭环

---

## Phase 5: User Story 3 - 确认后清理:前置确认 + 状态更新 + 执行报告 (Priority: P3)

**Goal**: 清理计划 + apply 引擎侧 + 命令模板(门控/probe/移交分诊)+ 全部登记面

**Independent Test**: 夹具上走"未确认 apply 被拒(零删除零移动)→ 确认 → 执行 → 状态 resolved → 执行报告三要素"(quickstart 走查 2)

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T021 [P] [US3] 契约测试(RED,append):apply 门与红线——未 confirmed 计划退出 2 零执行、越界 target(src//tests//.git/)退出 2、disposition 不一致退出 2、repair/dismiss 仅状态更新,追加至 `tests/contract/test_sanitize_engine_contract.py`(锚 contracts/sanitize-engine.md §2/§4)[blockedBy: T002]
- [X] T022 [P] [US3] 结构契约测试(RED):命令模板——流程锚文本(C-4..C-10)、红线声明(C-11..C-14)、门控指针行存在且不命中扫描器阻塞模式、## Feedback 步骤存在、4 副本一致性,写入 `tests/contract/test_sanitize_template.py`(锚 contracts/sanitize-command-template.md)

### Implementation for User Story 3

- [X] T023 [US3] 实现 cleanup-plan + apply `scripts/python/sanitize-utils.py`:计划校验、delete/archive(至 `.specify/archive/<原相对路径>`)机械执行、状态更新(resolved)、执行报告信封(三要素+失败如实)、executed 标记[blockedBy: T021, T005]
- [X] T024 [US3] 撰写命令模板 `templates/commands/sanitize.md`:frontmatter(script 指向引擎)、执行流 Preflight/Collect/Judge/Present/Confirm/Apply/Wrap-up、单行门控指针 `> Gate probe: gate-sanitize-destructive-cleanup — ...`、红线四条、## Feedback 与 ## Documentation 步骤(GREEN for T022)[blockedBy: T022, T023]
- [X] T025 [US3] 登记面同步:`shared/definitions/probe-definitions.md` Objects 表 +2 行(speckit-sanitize-wrapup / gate-sanitize-destructive-cleanup);`tests/contract/test_feedback_command_classification.py` 复杂命令计数 17→18;`.specify/specs/044-reduce-confirmation-flows/baseline.json` total +1;运行 `scan-confirmation-gates.py` 验证新门控归类 keep_gate 且 violations 为空[blockedBy: T024]
- [X] T026 [US3] 传播命令副本:运行 `python3 scripts/python/regen-command-copies.py`;核验 `.claude/commands/speckit.sanitize.md`、`.github/prompts/speckit.sanitize.prompt.md`、`.opencode/command/speckit.sanitize.md`、`.qoder/commands/speckit.sanitize.md` 四副本含同一编辑且 `--check` 零 stale[blockedBy: T024]
- [X] T027 [US3] 集成测试 `tests/integration/test_sanitize_us3.py`:未确认 apply 拒绝且零删除零移动 → confirmed 后 delete/archive 执行 → 状态 pending→resolved → 执行报告三要素 + 失败如实报告路径(SC-003)[blockedBy: T023, T013]
- [X] T028 [US3] 用户文档与 Tool 记录:`docs/reference/commands/sanitize.md`(既有命令文档格式:标题/模式/bash 示例/Exit Codes/See Also;CLI 示例与契约测试钉死的语法一致)+ `.specify/memory/tools/sanitize-utils.py.md`(Tool Reuse 纪律:行为规则+环境适用性)[blockedBy: T024, T023]

**Checkpoint**: 三个故事全部独立成立——完整命令可用,门控治理零回流

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 镜像终验、全量回归、dogfood、SC 台账

- [X] T029 镜像义务终验:运行 `python3 scripts/python/sync-mirrors.py --write`;`diff -q` 核验引擎与 probe-definitions 两对镜像逐字节一致;`--check` exit 0[blockedBy: T023, T025]
- [X] T030 全量回归与 pin 卫生:全套件 vs baseline-failed.txt 名字级零新增失败;复核硬编码计数仅限"计数即契约"处(复杂命令 18、门控 total 23),其余以 len()/glob 派生[blockedBy: T011, T020, T027, T029]
- [X] T031 dogfood 检查运行(本仓真实工作区):执行 collect + 对 `.specify/memory/todo/20260812-evidence-session-backlog.md` 作语义判定并入台账,断言发现携带 1a090c72 证据引用;清理执行留给用户确认(非阻塞),如实报告发现清单[blockedBy: T029]
- [X] T032 撰写 `verification.md`:SC-001..005 逐条状态与证据(SC-001 夹具+dogfood 双源;SC-002 快照;SC-003 集成;SC-004 集成;SC-005 夹具+抽检记录),含 deferred_tasks 记录区[blockedBy: T030, T031]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 立即可执行
- **Foundational (Phase 2)**: 依赖 Phase 1;**阻塞全部用户故事**
- **US1 (Phase 3)**: 依赖 Phase 2;无跨故事依赖(MVP)
- **US2 (Phase 4)**: 依赖 Phase 2(复用 T005 台账/根);与 US1 仅共享台账语义,可并行推进
- **US3 (Phase 5)**: 依赖 Phase 2;模板(T024)依赖引擎 apply 语义(T023);与 US1/US2 可并行推进
- **Polish (Phase 6)**: 依赖全部实现任务

### User Story Dependencies

- **US1 (P1)**: Foundational 后即可开始,零外部依赖
- **US2 (P2)**: Foundational 后即可开始;独立可测(确定性检查器不依赖语义 lane)
- **US3 (P3)**: Foundational 后即可开始;集成测试 T027 复用 US2 的 correctness 夹具(T013)

### Parallel Opportunities

- Phase 2 内:T002 ∥ T003(不同测试文件)
- US1 内:T006 ∥ T007(夹具 ∥ 测试)
- US2 内:T013 ∥ T014 ∥ T015 ∥ T016(夹具 ∥ 三个测试文件);实现侧 T017/T018/T019 同文件(sanitize-utils.py)串行
- US3 内:T021 ∥ T022(不同测试文件);T025 ∥ T026 ∥ T028(登记面/副本/文档不同文件)于 T024 后并行
- 跨故事:US2 与 US3 的测试/夹具任务可由不同 worker 并行(不同文件)

---

## Parallel Example: User Story 2

```bash
# Launch all US2 test/fixture tasks together:
Task: T013 correctness 夹具 tests/fixtures/sanitize/correctness/
Task: T014 死引用语法测试 tests/unit/test_sanitize_checks_refs.py
Task: T015 索引/链接测试 tests/unit/test_sanitize_checks_index.py
Task: T016 镜像漂移测试 tests/unit/test_sanitize_checks_mirror.py
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 单故事——过期残留检出 + 台账持久化 + 零材料修改,独立可测即交付核心价值(需求的直接动因)。US1 无同优先级伴生故事。

1. Complete Phase 1: Setup(基线冻结)
2. Complete Phase 2: Foundational(引擎骨架 + 台账)
3. Complete US1(MVP!)
4. **STOP and VALIDATE**: quickstart 走查 1 + T011 集成断言
5. US2 → US3 依次增量,每故事独立验证后再进

### Incremental Delivery

1. Setup + Foundational → 引擎地基
2. +US1 → 检出与台账(MVP)
3. +US2 → 确定性正确性检查 + 自动收敛
4. +US3 → 命令面/门控/登记面 → 完整 `/speckit.sanitize`
5. Polish → 镜像终验/全量回归/dogfood/SC 台账

---

## Notes

- [P] 任务 = 不同文件、无依赖;引擎实现任务(T004/T005/T008..T010/T017..T019/T023)同文件必须串行
- 测试先行的 RED-GREEN 顺序由 blockedBy 编码(T002/T003 → T004/T005 等)
- T025 的三个计数/登记变更是"计数即契约"例外:与引入变更同任务同步更新(pin 卫生规则 3)
- T031 dogfood 的清理执行须经用户确认——引擎红线(C-11)优先于任务完成性;发现如实报告即可关闭任务
- Commit after each task or logical group;stop at any checkpoint to validate story independently
