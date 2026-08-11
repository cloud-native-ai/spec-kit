# Tasks: Goal 的 Target 切片(run 级可指定的子成果分解)

**Input**: Design documents from `.specify/specs/038-goal-target/`(plan.md, requirements.md, data-model.md, contracts/×3, quickstart.md, feature-ref.md)
**Prerequisites**: plan.md ✅ | requirements.md ✅ | data-model.md ✅ | contracts/ ✅ | quickstart.md ✅ | feature-ref.md ✅
**Feature**: 041 Goal Registry(扩展切片)| **Branch**: `038-goal-target`

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is NON-NEGOTIABLE; 引擎/折叠为运行时代码 → 单元+契约+集成测试先行;命令模板为模板工件 → 结构性契约测试先行)

**Validation**: 格式校验通过——所有任务均为 `- [ ] [ID] [P?] [US?] 描述+文件路径` 清单行;DoD 仅用 `- DoD-N:` 前缀。

**Environment Prerequisites**: 无外部依赖——仅需本机 `python3`(≥3.8,stdlib-only 引擎)与 `pytest 8.4.2`(已探测可用);无 docker/集群/网络拉取。

---

## Format: `- [ ] [TaskID] [P?] [Story] Description`

## Phase 1: Setup

**Purpose**: 冻结测试基线,区分存量失败与回归(AGENTS.md 测试基线纪律)

- [X] T001 运行全套件冻结基线:`source .venv/bin/activate && python3 -m pytest tests/ -q > /tmp/baseline-038.txt 2>&1` 并记录 pass/fail 计数到 `.specify/specs/038-goal-target/notes/baseline.txt`(实施期每阶段结束对比此文件,零新增失败)

## Phase 2: Foundational(阻塞所有 User Story)

**Purpose**: 引擎数据层——`goal-utils.py` 的 `## Targets` 解析/渲染/校验原语,US1/US2/US3/US4 全部消费

- [X] T002 编写引擎数据层单元测试(测试先行):扩展 `tests/unit/test_goal_utils.py` 新增 Target 数据层用例——节缺省时 `parse_goal` 返回空 `targets` 且既有输出逐字节不变(SC-002 引擎侧);D3 表格渲染往返字节稳定;行正则拒绝手写破坏(错表头/缺列/非法状态);身份文法 `T-\d{3}` 唯一且单调、终态不复用;状态迁移矩阵 9 组(合法 4 组通过,其余拒绝);空表格非法、validate 计 problems(退出码语义);`_reject_bad_objective` 对切片尺度语句复用(GD-2/GD-3 样例集,复用 037 objective 拒绝样例改写)
- [X] T003 实现引擎数据层(满足 T002):在 `scripts/python/goal-utils.py` 新增 `_SECTION_TARGETS = "## Targets"` 常量;`_render()` 按 D3 文法渲染表格(ID 升序);`parse_goal()` 新增 `targets` 键(`{id, statement, status}` 列表,节缺省为空);`validate_goal()` 追加 data-model.md §Entity 1 四条校验规则;抽出可复用的身份发放与状态迁移判定函数(供 T008 CLI 动作调用);MUST 保持无 Target 时 `create`/`validate`/`list`/`status`/`criteria`/`migrate` 输出逐字节不变 [blockedBy: T002]
- [X] T004 运行 T002 测试集确认全绿,并跑 `tests/unit/test_goal_utils.py` 全部既有用例零回归 [blockedBy: T003]

## Phase 3: User Story 1 — 目标可以被切片(P1)🎯 MVP

**Goal**: 项目维护者经 `/speckit.goal`(goal-utils `targets` 动作组)给 goal 添加/列出/迁移 Target,节由引擎渲染、变更进 `## History`
**Independent Test**: quickstart.md §1——添加 3 条、list 输出、GD-2/GD-3/判据复述拒绝、drop 后保留且编号不复用、存量 goal 零迁移

### Tests for User Story 1

- [X] T005 [P] [US1] 编写 targets CLI 契约测试(测试先行):新建 `tests/contract/test_goal_targets_engine.py` pin `contracts/targets-engine.contract.md`——CLI 文法(`--add`/`--list`/`--set`+`--id` 互斥与成对规则);§2 校验表逐行(终态 goal 只读、空语句、GD-2/GD-3、判据归一化等值、`--id` 不存在 → 退出码 3、非法迁移 → 退出码 2);§4 History 记法逐字;`--list` 机器可解析输出与空输出;退出码四值语义 [blockedBy: T003]

### Implementation for User Story 1

- [X] T006 [US1] 实现 `targets` 动作组(满足 T005):在 `scripts/python/goal-utils.py` 新增 `targets` 解析器(位置参数 slug + 互斥标志)与 dispatch 分支;`--add` 身份发放 + `open` 落节 + History 行;`--set --id` 按合法迁移集执行 + History 行(no-op 不写);`--list` 输出 `T-<nnn>\t<status>\t<statement>`;判据归一化等值检查(D5);goal 终态拒绝 [blockedBy: T003,T005]
- [X] T007 [US1] 运行 T005 契约测试 + T002/T004 单元集确认全绿 [blockedBy: T006]
- [X] T008 [US1] 撰写命令模板目标侧(author-section):编辑 `templates/commands/goal.md`——Modes 表新增 targets 行;引擎调用示例块追加 `targets <slug> --add/--list/--set` 三例;Outline 相应步骤(targets 的添加/列出/迁移经由 modify 意图路由,单一撰写入口纪律不变) [blockedBy: T006]
- [X] T009 [US1] 镜像扇出 + 逐行核验(mirror-parity,覆盖 Mirror Obligations 第 1、2 行):运行 `python3 scripts/python/sync-mirrors.py --write`;随后核验——`diff -q scripts/python/goal-utils.py .specify/scripts/python/goal-utils.py`、`diff -q templates/commands/goal.md .specify/templates/commands/goal.md`,并 grep 确认 4 份 per-tool 副本含 targets 内容:`.claude/commands/speckit.goal.md`、`.github/prompts/speckit.goal.prompt.md`、`.qoder/commands/speckit.goal.md`、`.opencode/command/speckit.goal.md` [blockedBy: T008]
- [X] T010 [US1] 更新命令面结构性契约测试:扩展 `tests/contract/test_goal_command_surface.py`——goal.md 含 targets 模式行与引擎示例的内容断言;per-tool 副本集合从既有测试夹具派生(pin hygiene:不新增硬编码计数) [blockedBy: T009]
- [X] T011 [US1] 端到端验证(render-verify):按 quickstart.md §1 + §5 对真实引擎执行——3 条添加、list、GD-2/GD-3 拒绝样例、drop/编号不复用、存量 goal `view`/`validate` 输出与基线 diff 为空;结果回写 quickstart.md 走查记录 [blockedBy: T009]

**Checkpoint**: US1 完成即可独立交付——`/speckit.goal` 可完成 Target 全生命周期授权(MVP)

## Phase 4: User Story 2 — run 指定 Target(P1)

**Goal**: `/speckit.team run <team> --target T-<nnn>` 在 preview 校验(悬空/终态/跨 goal)、门禁披露、run report 记录;未指定时逐字节等价
**Independent Test**: quickstart.md §2——合法指派披露行与 report 行格式;三类非法引用 preview 停止零痕迹;无参数回归

### Tests for User Story 2

- [X] T012 [P] [US2] 编写 run 指派结构性契约测试(测试先行):新建 `tests/contract/test_run_target_assignment.py` pin `contracts/run-target-assignment.contract.md`——`templates/commands/team.md` 含:run 模式 `--target` 参数文法行、preview 五步校验(解析绑定 goal 用既有两级解析、悬空报错、终态复核二分、跨 goal 拒绝、终态 goal 只读)、门禁披露行格式 `本次 Target: T-002 — <语句>(open)` / `本次 Target: 无(对 goal 整体运行)`、report 指派行 `**Target 指派**:` 格式、"MUST NOT 提供终态执行旁路"约束句 [blockedBy: T003]
- [X] T013 [P] [US2] 编写 preview 校验逻辑集成测试(测试先行):新建 `tests/integration/test_run_target_validation.py`——构造绑定 goal 定义 + 团队夹具,经 `goal-utils.py` 解析路径断言:合法 open 引用通过;悬空 `T-999` 判定悬空;`done`/`dropped` 判定终态并给出复核二分指引文本;限定形 `other-goal.T-001` 判定跨 goal;goal 终态拒指派(校验规则以引擎 `parse_goal` 为唯一事实源,与 T003 数据层一致) [blockedBy: T003]

### Implementation for User Story 2

- [X] T014 [US2] 撰写命令模板团队侧(author-section,满足 T012):编辑 `templates/commands/team.md`——Run Mode 节 preview 步骤插入 `--target` 解析与五步校验(引用 goal-utils 解析为事实源);确认门禁披露清单追加本次 Target 行;run report 步骤追加 `**Target 指派**:` 字段;Routing 表 run 行注记可选 target;显式写入"不改变绑定/身份解析/交付目录"与"无终态执行旁路" [blockedBy: T012,T013]
- [X] T015 [US2] 镜像扇出 + 逐行核验(mirror-parity,覆盖 Mirror Obligations 第 3 行):`python3 scripts/python/sync-mirrors.py --write`;`diff -q templates/commands/team.md .specify/templates/commands/team.md`;grep 确认 4 份 per-tool 副本含 `--target` 校验内容:`.claude/commands/speckit.team.md`、`.github/prompts/speckit.team.prompt.md`、`.qoder/commands/speckit.team.md`、`.opencode/command/speckit.team.md` [blockedBy: T014]
- [X] T016 [US2] 运行 T012/T013 测试全绿 + 既有 team 命令面测试(`tests/contract/test_team_command_routing.py` 等)零回归 [blockedBy: T015]

**Checkpoint**: US1+US2 = 完整 MVP(可切片 + 可指派)

## Phase 5: User Story 3 — 台账归属与切片轴总结(P2)

**Goal**: `items.jsonl` 可选 `target_ref` 被折叠引擎消费,产出切片轴卷积(n/m,与判据轴分列),不一致列为待批准项
**Independent Test**: quickstart.md §3——归属计数正确、无 target_ref 条目归整体、轴分列、待批准项两侧触发、无效引用降级声明

### Tests for User Story 3

- [X] T017 [P] [US3] 编写折叠契约/集成测试(测试先行):新建 `tests/integration/test_target_fold.py` pin `contracts/target-ref-ledger.contract.md`——携带合法 `target_ref` 行归入对应 Target(末行定态语义不变);无字段行归 goal 整体;非法引用(不存在身份)降级计入整体 + `invalid_refs` 计数 + 声明;goal 无 `## Targets` 节时表单不含 `targets:` 块(既有输出逐字节不变,SC-002);`targets:` 块结构与 data-model.md §派生结构一致;`pending_approval` 两侧触发(open/全完成、done/未完成);负向扫描——产物无 "targets done ⇒ achieved" 推导(SC-005);IL-1…IL-5 保持(叠加 `tests/contract/test_team_item_ledger.py` 零回归) [blockedBy: T003]

### Implementation for User Story 3

- [X] T018 [US3] 实现折叠扩展(满足 T017):编辑 `skills/create-team/scripts/build-summary-input.py`——`fold_ledger()` 单遍扫描增加 `target_ref` 分组与无效引用降级;`load_goal_definition()` 读取 `## Targets` 节(经 goal-utils 解析语义);表单装配新增 `targets:` 块(authored_status/attributed_items/completed_items/pending_approval/coverage/unattributed_to_target/invalid_refs);切片轴与判据轴分列,不得出现 achieved 推导 [blockedBy: T003,T017]
- [X] T019 [US3] 更新台账契约文档:编辑 `.specify/specs/036-team-summary/contracts/items-ledger.contract.md`——字段表追加 `target_ref`(可选、局部形文法、缺省语义、IL-1…IL-5 保持声明);先读现行结构按既有格式追加,不改既有条款 [blockedBy: T018]
- [X] T020 [P] [US3] 更新 create-team 参考文档(author-section):编辑 `skills/create-team/references/summary-mapping.md`——items.jsonl 字段表加 `target_ref` 行、折叠规则加归属/降级条款、表单 `targets:` 块说明 [blockedBy: T018]
- [X] T021 [P] [US3] 编辑 `skills/create-team/references/goal.md`——Target 的提议形流程(团队/run 提议新 Target 或完成,propose → ratify 经 `/speckit.goal`,派生流程不写 `goal.md`)与 [[STR-004]] 概念锚链接 [blockedBy: T018]
- [X] T022 [P] [US3] 编辑 `skills/create-team/references/execution-guide.md`——run 执行时目标聚焦 Target 的操作纪律、新台账条目携带 `target_ref` 的主管写入职责 [blockedBy: T018]
- [X] T023 [US3] 镜像扇出 + 逐行核验(mirror-parity,覆盖 Mirror Obligations 第 4、5、6、7 行):`python3 scripts/python/sync-mirrors.py --write`;`diff -q` 核验 `build-summary-input.py`、`summary-mapping.md`、`goal.md`、`execution-guide.md` 各自的 `.specify/skills/create-team/` 镜像 [blockedBy: T020,T021,T022]
- [X] T024 [US3] 运行 T017 测试全绿 + 既有总结折叠族(`tests/integration/test_goal_aggregation.py`、`test_summary_four_patterns.py` 等)零回归 [blockedBy: T023]

## Phase 6: User Story 4 — done Target 喂给里程碑视图(P3)

**Goal**: `done` Target 以来源标记进入既有里程碑组,与判据投影天然区分;summarize-project 零代码改动
**Independent Test**: quickstart.md §4——判据行与 Target 行共存且 source 区分;判据为空时 Target 来源填充并声明

### Tests for User Story 4

- [X] T025 [P] [US4] 编写里程碑吸收集成测试(测试先行):新建 `tests/integration/test_target_milestones.py`——`done` Target 产出 `milestones` 行且 `source: goal-target:<slug>/goal.md#T-<nnn>`;判据投影行语义原样(036 FR-013 保持);判据为空 + 存在 done Target → 里程碑组由 Target 来源填充并声明来源;`open`/`dropped` Target 不进入里程碑组 [blockedBy: T018]

### Implementation for User Story 4

- [X] T026 [US4] 实现里程碑吸收(满足 T025):编辑 `skills/create-team/scripts/build-summary-input.py`——表单 milestones 组追加 Target 来源行(title 取语句、status 映射 achieved 语义、source 值按契约 §5);`skills/summarize-project/` 代码与 DDL MUST 不改(D7) [blockedBy: T025]
- [X] T027 [US4] 运行 T025 全绿 + 既有里程碑相关断言零回归;`diff -q` 复核 summarize-project 未被触碰 [blockedBy: T026]

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T028 [P] 词汇表消歧条目(FR-017):编辑 `.specify/memory/glossary.md`——新增行 `Goal Target | 目标切片, target 切片 | …(链接概念锚)`(origin/status 按词汇表协议);同表追加 "target" 消歧行,指明 `optimization_target`/`co_targets`、territory `target` 字段、evidence/interview-utils `--target` 与本概念无关,均不改名 [blockedBy: T006]
- [X] T029 [P] 用户文档(FR-018):编辑 `docs/reference/commands/goal.md`——targets 动作组小节(链接概念锚,不复述);编辑 `docs/reference/commands/team.md`——run 模式 `--target` 参数与复核二分小节 [blockedBy: T014]
- [X] T030 全仓镜像一致性终检:`python3 scripts/python/sync-mirrors.py --check`(exit 0)+ `find` 抽查无手工双写残留 [blockedBy: T009,T015,T023,T027,T028,T029]
- [X] T031 全套件终验:对比 T001 基线——零新增失败;既有测试若因合法表面扩展需同任务更新计数,遵循 pin hygiene(计数即契约者在同一任务更新,否则 `len(...)` 派生) [blockedBy: T030]
- [X] T032 quickstart 全走查复跑(refresh-verify):按 quickstart.md §1–§5 对真实引擎与折叠链端到端执行一遍,结果回写;SC-001…SC-006 逐项对照取证来源 [blockedBy: T031]

---

## Dependencies

```text
T001 (Setup 基线)
 └─▶ T002 → T003 → T004   (Foundational: 引擎数据层,阻塞一切)
      ├─▶ US1: T005 → T006 → T007 → T008 → T009 → T010/T011
      ├─▶ US2: T012,T013 ─▶ T014 → T015 → T016      (依赖 T003 数据层)
      ├─▶ US3: T017 ─▶ T018 → T019/T020/T021/T022 → T023 → T024
      └─▶ US4: T025 ─▶ T026 → T027                   (依赖 T018 折叠)
Polish: T028/T029 随 US1/US2 落定即可并行 → T030 → T031 → T032
```

- US1 ⊥ US2 ⊥ US3(仅共享 T003 数据层;测试文件各自独立,`[P]` 有效)
- US4 依赖 US3 的折叠实现(T018)
- US1、US2 同为 P1,构成 MVP;US3(P2)、US4(P3)可独立延后

## Parallel Execution Examples

```text
# Foundational 完成后,三个 Story 的测试编写可同时发起:
Task: "T005 targets CLI 契约测试"     (tests/contract/test_goal_targets_engine.py)
Task: "T012 run 指派结构性契约测试"    (tests/contract/test_run_target_assignment.py)
Task: "T017 折叠集成测试"             (tests/integration/test_target_fold.py)

# US3 参考文档三件互不依赖:
Task: "T020 summary-mapping.md 更新"
Task: "T021 references/goal.md 更新"
Task: "T022 execution-guide.md 更新"

# Polish 期文档两件并行:
Task: "T028 词汇表条目"  |  Task: "T029 用户文档"
```

## Implementation Strategy

### MVP First(User Story 1 + 2)

1. Phase 1 Setup → Phase 2 Foundational(阻塞项,最先完成)
2. US1(切片授权)→ 独立测试:quickstart §1/§5
3. US2(run 指派)→ 独立测试:quickstart §2
4. **MVP 就绪**:目标可切片、run 可指派、拦截与披露生效

### Incremental Delivery

- US1+US2 后可先交付评审;US3(归属与切片轴总结)再交付;US4(里程碑吸收)最后
- 每阶段结束对比基线(T001)确认零新增失败;每镜像批次结束跑 `sync-mirrors.py --check`
- 实施纪律:契约测试先行于实现;镜像只走 `sync-mirrors.py`;终态复核二分不提供执行旁路

## Notes

- `[blockedBy:]` 标记由 `/speckit.implement` 拓扑排序消费;无标记任务仅受阶段顺序约束
- Pin hygiene:本任务集新增测试的 per-tool 副本清单、表面文件列表一律从既有夹具/目录树派生,不硬编码幻影路径;版本断言用 floor 语义
- 模板工件(命令模板/参考文档)的测试为结构性契约测试(内容/镜像一致性断言),无运行时对象——符合模板特性门
- `[P]` 仅标于不同文件且无未完成依赖的任务;共享同一文件(如 `build-summary-input.py` 的 T018/T026)串行

## Definition of Done

- DoD-1: SC-001…SC-006 逐项有取证来源且通过(SC-002 以 diff 为空取证)
- DoD-2: 全套件对比基线零新增失败;三份契约的 Test Pins 全部落实为测试并绿
- DoD-3: `sync-mirrors.py --check` exit 0;Mirror Obligations 9 行逐行核验留痕
- DoD-4: quickstart.md §1–§5 全走查通过并回写结果
- DoD-5: 词汇表含「Goal Target」消歧条目;docs/reference/commands/{goal,team}.md 已更新;全文档对概念表述链接 [[STR-004]] 不复述
- DoD-6: 终态复核二分无执行旁路;派生流程零写入 `goal.md`;切片轴与判据轴无互推
