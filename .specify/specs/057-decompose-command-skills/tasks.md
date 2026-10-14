# Tasks: 057-decompose-command-skills(命令技能化分解补全)

**Requirement ID**: 057
**Requirement Key**: 057-decompose-command-skills
**Related Feature**: 057 命令技能化分解补全(from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/057-decompose-command-skills/`(plan.md、requirements.md、data-model.md、contracts/run-skills-wiring.md + contracts/run-team-parity.md、quickstart.md、feature-ref.md)
**Prerequisites**: plan.md(required)、requirements.md(required)、research.md(无——内联于 plan Phase 0)、data-model.md、contracts/

**Tests Mode**: ON(Constitution Principle IV "Test-First & Contract-Driven Implementation" 强制测试;Feature 057 为 template-only——Constitution VII Workflow Gates "Template-only features" 门裁定:测试形态为**结构契约测试**(内容/规范路径/镜像字节一致断言),非单元/集成测试,plan.md Constitution Check IV 行已证成)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. Within-story order follows the **doc-feature taxonomy**(author-section → mirror-parity → render-verify → refresh-verify,per create-tasks § Phase Shapes)——本特性交付物为技能/模板/注册表内容,无 Models/Services/Endpoints。

## Definition of Done (DoD)

- DoD-1: 制品按规格落地——两新 internal 技能(run-skills/run-team)、team.md 与 skills.md 命令模板改动、指南例外条目、probe 注册表 2 行,全部落规范层
- DoD-2: 全部结构契约测试通过——tests/contract/test_run_skills_wiring.py 覆盖 C-1…C-12 且全绿
- DoD-3: quickstart.md 三场景实跑并留痕(notes/quickstart-run.md,含场景 B 的变更前后平价对照与全部 teardown 步骤)
- DoD-4: 行为类条款评审完成(B-1…B-5;含 SC-003 平价对映逐条核对与 fresh-context 自足运行记录)
- DoD-5: 相对判据收尾复测无新增漂移(镜像仍恰 1 条既有 DIFF;门控 total 仍 23;compile 71 单元零漂移;regen 全 OK)
- DoD-6: verification.md 对 SC-001…SC-005 逐条记录状态

**DoD Status**: pending

## Completion Gate

- GATE-1: 结构契约测试全绿 — check: `python3 -m pytest tests/contract/test_run_skills_wiring.py -q` EXIT=0
- GATE-2: 镜像义务相对判据 — check: `python3 scripts/python/sync-mirrors.py --check` DIFF 计数仍 = 1 且为既有 `.specify/skills/git-workspace/scripts/git_fleet.py`
- GATE-3: 无残留开放任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/057-decompose-command-skills/tasks.md` 返回 0
- GATE-4: verification.md 逐 SC 状态 — check: `grep -cE 'SC-00[1-5]' .specify/specs/057-decompose-command-skills/verification.md` ≥ 5
- GATE-5: 门控预算不变(设计规避验证) — check: `python3 .specify/scripts/python/scan-confirmation-gates.py` total 仍 = 23、violations = 0
- GATE-6: 编译产物零漂移 — check: `python3 scripts/python/probe-utils.py --action compile-embeds --check` 报告 71 units、zero drift
- GATE-7: per-tool 副本一致 — check: `python3 scripts/python/regen-command-copies.py --check` 报告 OK

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1=run-skills / US2=run-team / US3=接线核查)
- **[blockedBy: T001,T002]**: 显式依赖标签——被列任务全部 `[X]` 前不得开始
- **[green: <contract>#<clause>]**: green-point 归属——本行是把该契约条款转绿的那一行;C-1…C-12 每条恰被一行认领,编号即认领顺序(分区:Foundational=C-1,US1=C-2/C-3/C-4,US2=C-5/C-6/C-7/C-8/C-9,US3=C-10/C-11/C-12)
- Include exact file paths in descriptions

### Task State Sigil

`- [ ]` Open / `- [>]` Claimed(多代理)/ `- [X]` Closed / `- [~]` Deferred(理由入 verification.md deferred_tasks= 与行内注释)。完成 = 零 `[ ]`/`[>]`。

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 为后续阶段准备证据落点

- [ ] T001 Create spec notes directory and red-first evidence placeholder at .specify/specs/057-decompose-command-skills/notes/red-first-evidence.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 测试先行与两故事共用的注册基础设施;完成前不得开始任何用户故事

**Generation-time premise measurements(2026-10-14 实跑,生成期复测与 plan 阶段一致)**:
`python3 scripts/python/sync-mirrors.py --check` → EXIT=2,恰 1 条既有 DIFF(`.specify/skills/git-workspace/scripts/git_fleet.py`);`python3 .specify/scripts/python/scan-confirmation-gates.py` → total 23(16 destructive + 7 governance_kept),violations 0;`python3 scripts/python/probe-utils.py --action compile-embeds --check` → 69 units, zero drift;`python3 scripts/python/regen-command-copies.py --check` → OK。

- [ ] T002 [P] Write structural contract test tests/contract/test_run_skills_wiring.py covering clauses C-1…C-12 of contracts/run-skills-wiring.md (red-first: both skills and edits absent) and record each clause's failing evidence (command, real output, exit status) in .specify/specs/057-decompose-command-skills/notes/red-first-evidence.md
- [ ] T003 [P] Capture pre-change baselines into .specify/specs/057-decompose-command-skills/notes/pre-change-measurements.md by running the four engine checks listed in this phase preamble and pasting real outputs (re-freeze: re-run, never inherit)
- [ ] T004 [P] Add two skill-wrapup Object rows (units skill:run-skills and skill:run-team, lifecycle_point wrap-up) to the Object table in shared/definitions/probe-definitions.md, then mirror-sync via `python3 scripts/python/sync-mirrors.py --write --only shared` [green: contracts/run-skills-wiring.md#C-1]

**Checkpoint**: 契约测试红(制品缺失态)已取证;注册基础设施就绪——用户故事可开始

---

## Phase 3: User Story 1 - run-skills:运行未注册技能的统一入口 (Priority: P1) 🎯 MVP

**Goal**: 一个宿主未发现的技能,仅凭 run-skills 一次调用完成解析(canonical 优先)、加载、执行并转述产出;run-skills 自身注册到 agent(具名例外)

**Independent Test**: 新上下文中对已知位置集内的未注册技能调用 run-skills(quickstart 场景 A premises)→ 解析披露所选路径 + 按其 SKILL.md 执行;pytest -k "c1 or c2 or c8" 绿

### Implementation for User Story 1

- [ ] T005 [US1] Author skills/internal/run-skills/SKILL.md per plan.md: frontmatter (name run-skills, classification internal, skill_id "<SKILL:.specify/skills/internal/run-skills/SKILL.md>"); body Goal/Input Contract/Workflow (location search order per data-model.md § Skill Location Search Order — canonical before installed; trust boundary FR-003; execution per FR-005; best-effort registration hint FR-007; runtime-mode gate FR-008 incl. internal-target refusal)/Boundaries; zero BLOCKING_PATTERNS wording (gate-scan constraint, plan.md Constraints ①)
- [ ] T006 [US1] [blockedBy: T005] Mirror-sync the new skill via `python3 scripts/python/sync-mirrors.py --write --only skills/internal/run-skills` and verify byte-identity with `diff -q skills/internal/run-skills/SKILL.md .specify/skills/internal/run-skills/SKILL.md`
- [ ] T007 [US1] [blockedBy: T006] Render the compiled Wrap-up via `python3 scripts/python/probe-utils.py --action compile-embeds` and re-sync mirrors (plan Mirror Obligations row 7)
- [ ] T008 [US1] [blockedBy: T005] Update internal-skill guidance in templates/skills.md AND .specify/skills.md (dual write, byte-identical): run-skills named exception to "internal not agent-visible" + multi-host fallback via /speckit.skills run route; zero BLOCKING_PATTERNS wording
- [ ] T009 [US1] [blockedBy: T006,T007,T008] Verify US1: `python3 -m pytest tests/contract/test_run_skills_wiring.py -k "c2 or c3 or c4" -q` green; `diff -q templates/skills.md .specify/skills.md` identical [green: contracts/run-skills-wiring.md#C-2] [green: contracts/run-skills-wiring.md#C-3] [green: contracts/run-skills-wiring.md#C-4]

**Checkpoint**: US1 独立可测——MVP 交付(运行未注册技能的入口可用)

---

## Phase 4: User Story 2 - run-team:/speckit.team run 流程提取 (Priority: P1)

**Goal**: /speckit.team run 委派给 run-team,行为平价(P-1…P-10 零丢失);命令模板程序性内容清零

**Independent Test**: team.md 结构断言(C-4/C-5)+ 对同一团队变更前后各跑一次 run 比对义务面(quickstart 场景 B 平价对照法);pytest -k "c4 or c5 or c10 or c11 or c12" 绿

### Implementation for User Story 2

- [ ] T010 [US2] Author skills/internal/run-team/SKILL.md carrying obligations P-1…P-10 from contracts/run-team-parity.md (Workflow: Load/Preview via goal-utils run-checks engine as sole judge/Restate/Render/Present & Execute/Orchestrate/Report; Constraints: --target invariants, .work/ output discipline, continuous loop gates; Boundaries: no create/modify semantics, dispatch governance per subagent-definitions with fast-fail injection clause); zero BLOCKING_PATTERNS wording
- [ ] T011 [US2] Slim templates/commands/team.md per C-4/C-5: routing-table run row, routing-flow run step, and Ambiguous-Intent run listing all point to run-team (runtime path skills/internal/run-team/SKILL.md); Run Mode section reduced to routing pointer + inputs/outputs note; create/modify rows unchanged
- [ ] T012 [US2] [blockedBy: T010] Mirror-sync via `python3 scripts/python/sync-mirrors.py --write --only skills/internal/run-team` and verify `diff -q` byte-identity
- [ ] T013 [US2] [blockedBy: T011] Fan out team.md per-tool copies via `python3 scripts/python/regen-command-copies.py` and verify `--check` OK plus copies contain the run-team routing
- [ ] T014 [US2] [blockedBy: T012] Render Wrap-up via `python3 scripts/python/probe-utils.py --action compile-embeds` and re-sync mirrors
- [ ] T015 [US2] [blockedBy: T011,T012,T013,T014] Verify US2: `python3 -m pytest tests/contract/test_run_skills_wiring.py -k "c5 or c6 or c7 or c8 or c9" -q` green; `python3 scripts/python/probe-utils.py --action compile-embeds --check` reports 71 units zero drift [green: contracts/run-skills-wiring.md#C-5] [green: contracts/run-skills-wiring.md#C-6] [green: contracts/run-skills-wiring.md#C-7] [green: contracts/run-skills-wiring.md#C-8] [green: contracts/run-skills-wiring.md#C-9]

**Checkpoint**: US1 + US2 均独立可用;run 义务真源已单点化到 run-team

---

## Phase 5: User Story 3 - 接线核查与 modify 语义封口 (Priority: P2)

**Goal**: 三个命令模板路由逐行指向既有技能,零重复语义新技能

**Independent Test**: pytest -k "c3 or c6 or c9" 绿;agents.md 三行路径实存;目录清单无重复语义

### Implementation for User Story 3

- [ ] T016 [US3] Extend templates/commands/skills.md Delegation routing table from 2 to 5 rows per C-3 (create / improve / merge / think / run — run row runtime path skills/internal/run-skills/SKILL.md with input note pinning grammar `run-skills <名称|路径>`)
- [ ] T017 [US3] [blockedBy: T016] Fan out skills.md per-tool copies via `python3 scripts/python/regen-command-copies.py` and verify `--check` OK plus copies contain the 5-row table
- [ ] T018 [P] [US3] Audit templates/commands/agents.md 3-row intent table against existing skills run-agent/create-agent/improve-agent (fix routing line only if drift found; expected no change) and confirm referenced runtime paths exist
- [ ] T019 [US3] [blockedBy: T016,T017,T018] Verify US3: `python3 -m pytest tests/contract/test_run_skills_wiring.py -k "c10 or c11 or c12" -q` green [green: contracts/run-skills-wiring.md#C-10] [green: contracts/run-skills-wiring.md#C-11] [green: contracts/run-skills-wiring.md#C-12]

**Checkpoint**: 三个命令面路由全族指向既有技能;无重复语义技能目录

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 全量绿、实跑留痕、相对判据收尾

- [ ] T020 [P] Run the full structural contract suite `python3 -m pytest tests/contract/test_run_skills_wiring.py -q` — all C-1…C-12 green
- [ ] T021 [P] Execute quickstart.md scenarios A/B/C with real outputs (including scenario B pre/post parity comparison and every teardown step) into .specify/specs/057-decompose-command-skills/notes/quickstart-run.md
- [ ] T022 Fresh-context self-containment record for SC-001/SC-002: dispatch a new-context agent to run one unregistered fixture skill via run-skills alone (no ambient instructions) and record resolution/executon/disclosure evidence in .specify/specs/057-decompose-command-skills/notes/quickstart-run.md appendix
- [ ] T023 Re-run relative-criteria baselines (GATE-2/5/6/7 commands) and record per-SC status rows (SC-001…SC-005) in .specify/specs/057-decompose-command-skills/verification.md
- [ ] T024 [blockedBy: T020,T021,T022,T023] Sweep Definition of Done + Completion Gate, flip DoD Status, confirm zero open `[ ]`/`[>]` rows in tasks.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖,立即开始
- **Foundational (Phase 2)**: 依赖 Setup;T002/T003/T004 可并行
- **US1 (Phase 3)**: 依赖 Foundational;MVP
- **US2 (Phase 4)**: 依赖 Foundational;与 US1 无相互依赖(T010 不依赖 T005-T009),可并行
- **US3 (Phase 5)**: T016 不依赖 US1/US2 产物本身,但 run 路由行指向的 [[STR-001]] 由 US1 落地——C-3 的完整绿判定在 T019,自然满足
- **Polish (Phase 6)**: 依赖全部故事完成

### User Story Dependencies

- **US1**: Foundational 后即可开始;不依赖其他故事
- **US2**: Foundational 后即可开始;不依赖 US1(P-1…P-10 义务源自 team.md 现行文本,非 run-skills)
- **US3**: 依赖 US1 的 [[STR-001]] 存在(run 路由行指向它);C-3/C-6/C-9 的绿判定在 T019

### Parallel Opportunities

- Phase 2: T002 / T003 / T004 互不同文件,可并行
- US2 与 US3 的 authoring 行(T010 与 T016/T018)不同文件,可并行
- T020 / T021 可并行(只读运行 + 独立留痕文件)

---

## Parallel Example: Phase 2

```bash
# 三行互不写同文件,可并行派发:
Task: "Write structural contract test tests/contract/test_run_skills_wiring.py (T002)"
Task: "Capture pre-change baselines into notes/pre-change-measurements.md (T003)"
Task: "Add probe registry rows in shared/definitions/probe-definitions.md (T004)"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 单独构成独立可测增量(运行未注册技能的入口),MVP = Phase 1 + Phase 2 + Phase 3。US2 为同优先级但独立可交付的第二个增量(非 MVP 必需)。

1. Complete Phase 1: Setup → 2. Phase 2: Foundational(红先行取证落地)→ 3. Phase 3: US1 → 4. **STOP and VALIDATE**: T009 绿 + quickstart 场景 A premises 复核 → 5. 继续增量

### Incremental Delivery

1. Setup + Foundational → 2. US1(MVP)→ 3. US2(平价提取)→ 4. US3(封口核查)→ 5. Polish(全量绿 + 实跑留痕)

---

## Notes

- 本特性为 template-only:全部"测试"为结构契约(内容/路径/镜像字节);行为类义务(B-1…B-5)由 quickstart 实跑、fresh-context 记录与评审承担,不声称测试覆盖
- 镜像义务:plan.md Mirror Obligations 表 7 行全部有显式 write+verify 任务覆盖(T004/T006/T007/T008/T012/T013/T014/T017)
- 收尾相对判据:无新增漂移(基线见 Phase 2 preamble 与 notes/pre-change-measurements.md)
- Commit after each task or logical group; Stop at any checkpoint to validate story independently
