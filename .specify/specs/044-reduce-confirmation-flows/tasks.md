# Tasks: 确认门控精简(Reduce Confirmation Flows)

**Requirement ID**: 044 (from branch name)
**Requirement Key**: 044-reduce-confirmation-flows
**Related Feature**: 046 Confirmation Gate Governance (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/044-reduce-confirmation-flows/`
**Prerequisites**: plan.md ✅, requirements.md ✅, data-model.md ✅, contracts/ ✅(4 份), quickstart.md ✅, feature-ref.md ✅, baseline-gates.md ✅

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates tests;本 spec 为文档/模板特性(唯一可执行代码是扫描脚本),按 constitution.md:93 的 **Template-only features** 门控,"测试"以**结构契约测试**(内容/标题/镜像对等断言)为主,扫描脚本另出真实单元/契约测试。

**Tests**: Tests Mode ON — 每个用户故事阶段先出结构契约测试,再改写模板/技能。

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Environment Prerequisites**: 无外部环境依赖(无 docker/集群/网络拉取);仅需本仓 Python ≥3.8 与既有测试套件。

**Doc-feature taxonomy**: author-section → mirror-parity → render-verify → refresh-verify(plan.md 的 Mirror Obligations 每一行都有显式写入任务与验证任务)。

## Definition of Done (DoD)

- DoD-1: 全部可逆门控按判据改写为自动执行 + 执行报告,破坏性/治理保留/intrinsic 门控零误删
- DoD-2: 全部结构契约测试与扫描脚本测试通过;全套件对比基线零新增失败
- DoD-3: Mirror Obligations 全表验证通过(regen --check 与 sync-mirrors --check 均 exit 0)
- DoD-4: 扫描脚本治理后复扫:总数降幅 ≥75%、violations 为空、残留全部在保留清单内
- DoD-5: quickstart.md 三条走查通过(team 零确认、扫描前后对比、破坏性保留 5/5)
- DoD-6: requirements.md 的 SC-001..SC-005 在 verification.md 逐条有状态行

**DoD Status**: green

## Completion Gate

- GATE-1: Full test suite has zero NEW failures vs recorded baseline — check: `scripts/bash/run-tests.sh` + `comm -13 baseline current`
- GATE-2: Every mirror obligation from plan.md verified — check: `python3 scripts/python/regen-command-copies.py --check` exit 0 且 `python3 scripts/python/sync-mirrors.py --check` exit 0
- GATE-3: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\]' tasks.md` returns 0
- GATE-4: verification.md lists every SC-NNN with a status — check: grep SC ids against requirements.md
- GATE-5: Gate scanner 治理后复扫达标 — check: `python3 scripts/python/scan-confirmation-gates.py --json --baseline baseline.json` 输出 violations=[] 且退出码 0

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结测试与镜像基线,确保治理前后对比可信。

- [X] T001 记录测试基线:运行全套 pytest(`scripts/bash/run-tests.sh` 或 `python3 -m pytest -q`),将失败名单存档到 `.specify/specs/044-reduce-confirmation-flows/baseline-failed.txt`
- [X] T002 验证改动前镜像面干净:`python3 scripts/python/regen-command-copies.py --check` 与 `python3 scripts/python/sync-mirrors.py --check` 均 exit 0;任何既有漂移先归因记录再继续

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 判据真源与扫描脚本——全部用户故事的共同前置。

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests (MANDATORY) ⚠️

- [X] T003 [P] 编写结构契约测试 `tests/contract/test_confirmation_gates_taxonomy.py`:断言 `shared/guidelines/confirmation-gates.md` 存在且含判据文档必备节(两级判据、破坏性清单 ≥4 项、治理保留清单 ≥6 项、存疑从严、回流约束、执行报告节);按标题发现节而非硬编码节数(pin hygiene)[blockedBy: 无]
- [X] T004 [P] 编写扫描脚本契约测试 `tests/contract/test_scan_confirmation_gates.py`:覆盖 gate-scanner-contract C-7 六项(输出 schema 键完整、扫描根排除镜像、判据清单确定性归类、存疑落 destructive、基线 delta 计算、退出码 2 回流违例)[blockedBy: 无]

### Implementation

- [X] T005 撰写判据真源 `shared/guidelines/confirmation-gates.md`:按 confirmation-taxonomy-contract C-1..C-6 与 execution-report-contract C-5(执行报告节含三要素 + 琐碎并入 + 合并呈现 + 失败如实报告),引用 reconcile-pattern.md § Tiered confirmation 为概念基础,不复制其正文 [blockedBy: T003]
- [X] T006 实现 `scripts/python/scan-confirmation-gates.py`(stdlib-only):按 gate-scanner-contract C-1..C-6(CLI 形态、扫描根、检出语义、JSON schema、基线对比、退出码);含 `.specify` 双重路径守卫(参照 regen-command-copies.py) [blockedBy: T004]
- [X] T007 首扫冻结基线:`python3 scripts/python/scan-confirmation-gates.py --json > .specify/specs/044-reduce-confirmation-flows/baseline.json`,并把 `baseline-gates.md` 的概数(≈55–60)更新为实测总数与逐条核对结果 [blockedBy: T006]
- [X] T008 镜像写入与验证:`python3 scripts/python/sync-mirrors.py --write` 同步 T005/T006 新文件;验证 `.specify/shared/guidelines/confirmation-gates.md` 与 `.specify/scripts/python/scan-confirmation-gates.py` 与源侧 `diff -q` 一致(Mirror Obligations 行 3/5) [blockedBy: T005,T006]
- [X] T009 `templates/instructions-template.md` Documentation Map 增一行指向 confirmation-gates.md(D8);同步 `.specify/templates/instructions-template.md` byte-identical(Mirror Obligations 行 2 的模板半体) [blockedBy: T005]

**Checkpoint**: Foundation ready — 判据、扫描器、基线齐备,用户故事可以开始

## Phase 3: User Story 1 - team 全流程自动执行,零确认打断 (Priority: P1) 🎯 MVP

**Goal**: team 创建直接落盘、运行直接启动、收尾自动完成,全程零阻塞确认(SC-001)。

**Independent Test**: 按 quickstart.md §1 走查 team create→run→收尾指令面,断言零阻塞确认指令且 continuous 分支门控仍在。

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T010 [P] 编写结构契约测试 `tests/contract/test_confirmation_gates_team_flow.py`:断言 `templates/commands/team.md` 与 `skills/create-team/SKILL.md` 在一次性模式(parallel/serial/iteration)流程中不含阻塞确认指令("等待用户确认"/"MUST NOT execute before confirmation"族);含落盘后呈现 + 修改途径、执行报告引用、continuous 例外条款、收尾非阻塞提交提示 [blockedBy: T003]

### Implementation for User Story 1

- [X] T011 [US1] 改写 `templates/commands/team.md`:移除创建确认门控(现 :50,83,84,97,102-104)与运行确认门控(现 :52,108-110,125,133-134),改为直接落盘/启动 + 呈现;收尾动作自动化;保留 continuous 分级门控条文;单行引用判据文档(team-flow-contract C-1/C-2/C-4/C-5) [blockedBy: T005,T010]
- [X] T012 [US1] 改写 `skills/create-team/SKILL.md`(现 :32,:38,:44,:236)与 `references/create-mode.md`(:16)、`references/team-presets.md`(:9,52,55)、`references/execution-guide.md`(:31):移除落盘/运行前确认,收尾提交提示改非阻塞一行(附 package 途径),补执行报告三要素;MUST NOT 触碰 `references/operating-loops.md` 与 `workspace-cluster.md` 的分级门控(team-flow-contract C-3/C-4/C-6) [blockedBy: T005,T010]
- [X] T013 [US1] 再生 team 命令 per-tool 副本:`python3 scripts/python/regen-command-copies.py`;grep-for-the-edit 验证 `.claude/commands/speckit.team.md`、`.qoder/commands/speckit.team.md`、`.github/prompts/speckit.team.prompt.md`、`.opencode/command/speckit.team.md` 均含改写(Mirror Obligations 行 1) [blockedBy: T011]
- [X] T014 [US1] `python3 scripts/python/sync-mirrors.py --write` 同步 create-team 技能;`diff -rq skills/create-team .specify/skills/create-team` 验证(Mirror Obligations 行 3) [blockedBy: T012]

### Manual Verification for User Story 1

- [X] T015 [US1] 走查 quickstart.md §1:在改写后的 team 命令/技能指令面确认零阻塞确认、呈现与报告指令齐备、continuous 分支门控保留;结果记入 verification 素材 [blockedBy: T013,T014]

**Checkpoint**: User Story 1 (MVP) 独立可用——team 全流程零确认

## Phase 4: User Story 2 - 全框架门控分类治理:可逆动作不再阻塞 (Priority: P2)

**Goal**: 既有门控按判据逐一治理,残留较基线 ↓≥75% 且全部在保留清单内(SC-002)。

**Independent Test**: 扫描脚本复扫 + 基线对比,按 quickstart.md §2 断言降幅与残留口径。

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T016 [P] 编写结构契约测试 `tests/contract/test_confirmation_gates_sweep.py`:按 baseline-gates.md 治理清单断言 auto_execute 面(goal/agents/skills/todo 批次/样板术语确认/样板提交提示)不再含阻塞样板;keep 面全在( feedback consume、docs 分级、session 同名覆盖、feature 状态回退、analyze 补救批准、interview、constitution 不可撤销、glossary 冲突、git-workflow 远程、tools invoke、commit 批准、implement CONFIRM)[blockedBy: T004]

### Implementation for User Story 2

- [X] T017 [US2] [P] 改写 `templates/commands/goal.md`(现 :28,47):目标定义写入由 preview→confirm 改为直接写入 + 执行报告;单行引用判据文档 [blockedBy: T005,T016]
- [X] T018 [US2] [P] 改写 `templates/commands/agents.md`(现 :43,70):模式选择与派发的阻塞确认改为直接执行 + 报告(破坏性分支除外)[blockedBy: T005,T016]
- [X] T019 [US2] [P] 改写 `templates/commands/skills.md`(现 :61-62):编辑 agent 文件的确认改为直接执行 + 报告 [blockedBy: T005,T016]
- [X] T020 [US2] 改写 `templates/commands/todo.md`:移除各批次执行前确认(现 :143,164-166,206,249),改为自动执行 + 逐批报告——批次是用户明确请求执行的 TODO 计划,git 提供可逆性(执行级决策,理由记入 verification.md);保留 :272 commit 显式批准(governance-kept)与歧义停问 [blockedBy: T005,T016]
- [X] T021 [US2] 收尾术语确认非阻塞化:改写约 10 个命令模板的 Glossary wrap-up 步骤(requirements/plan/tasks/implement/goal/session/interview/docs/feedback/todo 等,以 baseline.json 实测清单为准)为直接写入 + 并入收尾报告;冲突/覆盖用户既有条目仍停等(FR-008 但书);每模板单行引用判据文档 [blockedBy: T005,T016]
- [X] T022 [US2] 反馈提交提示非阻塞化:改写约 20 个命令模板收尾段与 `shared/workflow/feedback-step.md`(现 :80),达阈值时仅在收尾报告附一行非阻塞提示(附 `--action package` 途径);绝不阻塞、绝不自动传输(D5)[blockedBy: T005,T016]
- [X] T023 [US2] 微调 `shared/workflow/glossary.md`:明确非冲突收尾术语直接写入(冲突确认条文不动)[blockedBy: T005,T016]
- [X] T024 [US2] 再生全部受影响命令 per-tool 副本:`python3 scripts/python/regen-command-copies.py`;grep-for-the-edit 验证受影响 stem(goal/agents/skills/todo + 全部样板受影响命令)的 `.claude/.qoder/.github/prompts/.opencode` 副本均含改写(Mirror Obligations 行 1) [blockedBy: T017,T018,T019,T020,T021,T022]
- [X] T025 [US2] `python3 scripts/python/sync-mirrors.py --write` 同步 shared/workflow 改动(feedback-step.md、glossary.md);`diff -q` 验证(Mirror Obligations 行 3) [blockedBy: T022,T023]

### Manual Verification for User Story 2

- [X] T026 [US2] 扫描复扫 + 基线对比:`python3 scripts/python/scan-confirmation-gates.py --json --baseline baseline.json` —— 断言 total 降幅 ≥75%、by_class 残留全部在 keep 清单、violations=[]、退出码 0;实测数记入 verification 素材(quickstart §2) [blockedBy: T024,T025]

**Checkpoint**: User Stories 1 AND 2 独立可用——team 零确认 + 全框架治理达标

## Phase 5: User Story 3 - 先执行后修改:执行报告全覆盖 (Priority: P3)

**Goal**: 全部自动执行动作 100% 覆盖执行报告(三要素或收尾并入),用户事后知情且可改(SC-003)。

**Independent Test**: 枚举改为自动执行的动作面,逐一断言报告指令存在且含修改途径(quickstart 隐含于 §1/§2 的呈现检查)。

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T027 [P] 编写结构契约测试 `tests/contract/test_confirmation_gates_execution_report.py`:断言判据文档执行报告节含三要素 + 琐碎并入 + 合并呈现 + 失败如实报告;断言 US1/US2 改写面(由测试内从 baseline 治理清单动态枚举,勿硬编码文件数)均含执行报告或收尾合并报告指令 [blockedBy: T003]

### Implementation for User Story 3

- [X] T028 [US3] 执行报告指令补齐:逐一检查 US1/US2 改写的每个自动执行流程面,缺失三要素/合并报告指令者补齐(预期为少量补丁;改动文件与理由记入 verification.md) [blockedBy: T015,T026,T027]
- [X] T029 [US3] 传播 T028 改动(如有):regen-command-copies.py / sync-mirrors.py --write 并验证对应副本 [blockedBy: T028]

**Checkpoint**: All user stories independently functional

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 再生 instructions、全量回归与 SC 证据闭环。

- [X] T030 再生本仓 instructions:运行 `/speckit.instructions` 对应脚本路径刷新 `.specify/instructions.md`(AGENTS.md/CLAUDE.md/QODER.md/.github/copilot-instructions.md 符号链接消费面);验证 Documentation Map 新行存在、符号链接完好(Mirror Obligations 行 2) [blockedBy: T009]
- [X] T031 全套件回归:运行全套 pytest,与 T001 基线按名称级 diff,零新增失败 [blockedBy: T029]
- [X] T032 quickstart §2/§3 走查:扫描对比度量(SC-002/SC-005 证据)+ 破坏性门控保留抽查 5/5(SC-004 证据),结果写入 verification.md [blockedBy: T026]
- [X] T033 SC-003 证据:枚举自动执行动作面,逐一确认报告覆盖(三要素或并入收尾),覆盖率 100% 写入 verification.md [blockedBy: T028]
- [X] T034 终验:`python3 scripts/python/regen-command-copies.py --check` 与 `python3 scripts/python/sync-mirrors.py --check` 均 exit 0(GATE-2) [blockedBy: T030,T031]

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 (Setup) → Phase 2 (Foundational):基线先于一切
- Phase 2 → Phase 3/4/5:判据文档(T005)与扫描器(T006/T007)阻塞全部用户故事
- Phase 3/4 → Phase 5:US3 的报告补齐检查 US1/US2 改写面
- Phase 3/4/5 → Phase 6:回归与 SC 证据收尾

### User Story Dependencies

- US1 与 US2 相互独立(都仅依赖 Phase 2),可并行推进;US3 依赖 US1+US2 的改写面存在
- MVP = US1(单独交付 team 零确认价值)

### Within Each User Story

- 结构契约测试(RED) → 模板/技能改写(GREEN) → 副本再生(mirror-parity) → 走查(render-verify)

### Parallel Opportunities

- T003 ∥ T004(两份独立测试文件)
- T017 ∥ T018 ∥ T019(三个独立命令模板)
- T021 与 T022 内部各命令模板之间可并行(不同文件)
- US1 阶段(T010 起)与 US2 阶段(T016 起)整体可并行(不同文件面;T021/T022 的样板模板与 T011 的 team.md 无交集)
- T013 ∥ T014(regen 与 sync 两条传播链)

## Parallel Example: User Story 2

```text
T016 (契约测试) 完成后:
  Agent A: T017 goal.md → T018 agents.md → T019 skills.md
  Agent B: T020 todo.md → T021 术语样板(10 模板)
  Agent C: T022 提交提示样板(20 模板 + feedback-step.md)→ T023 glossary.md
汇合: T024 regen → T025 sync → T026 复扫对比
```

## Implementation Strategy

1. **MVP first**: Phase 1+2+3 交付 team 零确认(SC-001),即可独立验收与展示。
2. **Incremental**: Phase 4 全框架治理(SC-002)→ Phase 5 报告全覆盖(SC-003)→ Phase 6 证据闭环(SC-004/SC-005 + GATE-1..5)。
3. **执行级决策记录**: T020 的 todo 批次自动执行裁定(批次=用户明确请求执行的计划、git 可逆;与 tools invoke 保留门控的区别在于"请求内执行 vs 即兴任意脚本")MUST 记入 verification.md,供 SC 复核引用。
4. **防回流**: 此后任何新增命令/技能在契约测试 + 扫描脚本(退出码 2)双重约束下不得回流非破坏性门控(FR-003/SC-005)。
