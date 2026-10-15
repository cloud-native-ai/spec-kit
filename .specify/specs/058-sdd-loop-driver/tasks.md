# Tasks: 无人值守 SDD 循环驱动机制（Unattended SDD Loop Driver）

**Requirement ID**: 058 (from branch name)
**Requirement Key**: 058-sdd-loop-driver
**Related Feature**: Feature 058 无人值守 SDD 循环驱动机制（Planned，绑定确认 2026-10-15 clarify）
**Input**: Design documents from `.specify/specs/058-sdd-loop-driver/`（plan.md / requirements.md / data-model.md / contracts/ ×2 / quickstart.md / feature-ref.md）

**Tests Mode**: ON（Constitution Principle IV "Test-First & Contract-Driven Implementation" 存在即为 ON；本特性为 template-only 交付物，宪法 :117 template-only 门适用——测试形态为**结构契约测试**（frontmatter/章节/自包含/镜像断言，先例 `test_run_skills_wiring.py` 逐条款一测），非单元/集成代码测试；plan.md Constitution Check IV ⚠ Partial 已论证）

**Organization**: 本特性为 doc-feature（交付物 = skill 手册 + docs 页 + 契约测试），相位内采用 doc-feature 分类：author-section → mirror-parity → render-verify → refresh-verify；不适用 Models→Services→Endpoints。三个 P2/P1 内容故事向同一对 references 文件追加章节，测试函数追加向同一测试文件——同文件写入任务以 [blockedBy] 串行化，绿点以 [green: <contract>#<clause>] 分区（每条款恰认领一次）。

## Definition of Done (DoD)

- DoD-1: 交付物按规格实现——skills/external/sdd-loop-driver/（SKILL.md + references/dispatch-recipes.md + references/stage-prompts.md）五类内容齐备（C-3…C-9），零硬编码（FR-003/V-6）
- DoD-2: 全部自动化测试通过——tests/contract/test_sdd_loop_driver_skill.py 19 项条款测试全绿（C-1…C-12 + D-1…D-6）、test_run_skills_wiring.py 全绿（roster 更新后仍 12 passed）、全量套件零 NEW failures vs 冻结基线
- DoD-3: 人工验证完成——quickstart.md 场景执行留痕（notes/quickstart-run.md，含 S1 基线复测）；真实/演练驱动验收（D-9）按环境探测结论执行或依 [~] 纪律显式延期
- DoD-4: 文档更新——docs/reference/skills/sdd-loop-driver.md 落位且过 XV 判据（D-1/D-2）；Feature 索引与详情同步
- DoD-5: 评审就绪——镜像逐字节一致（C-11）、外部对无 NEW drift（D-5）、零越界面（D-6：templates/src/scripts 零改动）
- DoD-6: 成功标准核对——SC-001…SC-009 在 verification.md 逐条具状态（可核对的已核、需真实环境的如实 partial/deferred）

**DoD Status**: pending

## Completion Gate

- GATE-1: 全量测试零 NEW failures vs 基线 — check: `bash scripts/bash/run-tests.sh -q` + 与 `<spec-dir>/notes/pre-change-measurements.md` 冻结失败集做名字级 `comm -13`（实现期冻结，模板实现 owner = /speckit.implement step 6 Test runs 条）
- GATE-2: 镜像义务逐字节一致 — check: `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` 为空 且 `python3 scripts/python/sync-mirrors.py --check --only skills/external` 输出相对冻结基线（2 条 git-workspace DIFF）无新增行
- GATE-3: 零开放任务行 — check: `grep -cE '^- \[[ >]\]' tasks.md` 返回 0
- GATE-4: verification.md 逐 SC 具状态 — check: SC-001…SC-009 每条在 verification.md 有状态行
- GATE-5: 结构验证器 — check: `python3 scripts/python/validate-tasks.py <tasks.md>` exit 0（实现期复跑）
- GATE-6: 零越界面 — check: `git diff --stat HEAD -- templates/ src/ scripts/` 为空（D-6）

## Environment Prerequisites

- pytest 解释器: **partial** — 裸 `python3 -m pytest` 不可用（2026-10-15 实测系统 python3 无模块）；必经 `scripts/bash/run-tests.sh`（实测解析成功）。affected: 全部测试行
- qodercli: **available** — `/Users/liuqiming.lqm/.local/bin/qodercli`（2026-10-15 实测 `which qodercli`）。affected: D-9 本地拓扑演练可执行
- 远端工作区别名: **partial** — `~/.ssh/config` 含 94 个 Host 条目（2026-10-15 实测），但目标别名/项目/授权属实现期用户裁定；远端拓扑演练（SC-005 远端段）可执行性由 implement 期与用户确认。affected: T030/T031
- docker/镜像仓库/实集群: 无依赖（D-6 零越界面；交付面全为文件制品）

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1…US6)
- **[blockedBy: T001,T002]**: 显式依赖标签——所列任务未 `[X]` 前不得开始
- **[green: <contract>#<clause>]**: 绿点认领——本行负责使该契约条款转绿；条款全文件恰认领一次
- 含精确文件路径；验证类任务显式列出

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 基线冻结与证据落点就绪（re-freeze 纪律：每次生成/重跑/ implement 开工均重测）

- [ ] T001 冻结改前基线到 .specify/specs/058-sdd-loop-driver/notes/pre-change-measurements.md——逐项实跑并粘贴真实输出：① `bash scripts/bash/run-tests.sh tests/contract/test_run_skills_wiring.py -q`（改前预期 12 passed）；② `python3 scripts/python/sync-mirrors.py --check --only skills/external`（改前预期恰 2 条 git-workspace DIFF + DRIFT 提示）；③ `python3 scripts/python/validate-requirements.py .specify/specs/058-sdd-loop-driver/requirements.md`（预期 exit 0）；④ 全量套件失败集名字级清单（`bash scripts/bash/run-tests.sh -q` 的 failed 节点名，供 GATE-1 comm 比对）；⑤ 陷阱注记：`--only skills/external/sdd-loop-driver`（不存在子域）会命中 placeholder-only 跳过分支，基线测量必须取外层对
- [ ] T002 [P] 创建证据目录 .specify/specs/058-sdd-loop-driver/notes/（含 red-first-evidence.md 空表头与 quickstart-run.md 空表头，供后续行写入）

## Phase 2: User Story 4 — Skill 手册承载机制与执行侧可移植 (Priority: P1) 🎯 MVP

**Goal**: skill 骨架落地——frontmatter 四字段（C-1）、分类张力注解（C-2）、章节集与路由（C-3），结构契约测试先红后绿

**Independent Test**: `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q` 中 C-1/C-2/C-3 测试转绿；skill 文件存在于框架源侧

### Tests for User Story 4 (MANDATORY ⚠ red-first)

- [ ] T003 [US4] Author 结构契约测试 C-1/C-2/C-3（frontmatter 四字段断言、张力注解存在、H2 章节集断言）append 到 tests/contract/test_sdd_loop_driver_skill.py [blockedBy: T002]
- [ ] T004 [US4] Red-first 取证：运行 T003 测试记录 FAIL（3 项）真实输出到 notes/red-first-evidence.md [blockedBy: T003]

### Implementation for User Story 4 (author-section)

- [ ] T005 [US4] Author skills/external/sdd-loop-driver/SKILL.md——frontmatter（name: sdd-loop-driver / description 含触发词「使用SDD开发模式」「无人值守」/ skill_id `<SKILL:.specify/skills/sdd-loop-driver/SKILL.md>` / classification: external）+ 张力注解首行 + H2 章节集（What This Skill Does / When to Load / The Loop (U0–U6) / Hard Requirements / Discipline Defaults / References / Boundary）+ 路由到 references/ 两文件（内容取材 data-model E-1 与 plan Summary）[blockedBy: T004]

### Verification for User Story 4

- [ ] T006 [US4] Verify C-1/C-2/C-3 绿：运行 `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q` 全绿并记录 [green: contracts/skill-structure.md#C-1] [green: contracts/skill-structure.md#C-2] [green: contracts/skill-structure.md#C-3] [blockedBy: T004,T005]

**Checkpoint**: skill 骨架可被宿主按 frontmatter 发现、章节路由成立（US4 独立可测）

## Phase 3: User Story 1 — 一遍性入口驱动远端项目 SDD 全流程闭环（含断点续跑默认）(Priority: P1)

**Goal**: dispatch-recipes.md 内联五大执行机制命令形态 + 阶段链/哨兵字面量 + git 状态判定合并收尾（C-4/C-8/C-9）

**Independent Test**: C-4/C-8/C-9 测试转绿；机制命令形态与简报 §3–§5 已验证形态一致

### Tests for User Story 1 (MANDATORY ⚠ red-first)

- [ ] T007 [US1] Author 派发契约测试 C-4（五机制命令形态：git 断点探测三信号/heredoc 写入/runner 模板+sed 派生/后台执行+tail 轮询+一线一连接/收尾）、C-5（阶段链 STR-002 与 `-DONE` 哨兵字面量内联；`MERGE-DONE` 零出现；git 状态判定文本存在）、C-6（禁止缓冲至退出式派发操作规则 + 观测点映射）append 到 tests/contract/test_sdd_loop_driver_skill.py [blockedBy: T006]
- [ ] T008 [US1] Red-first 取证：C-4/C-5/C-6 FAIL 输出记录到 notes/red-first-evidence.md [blockedBy: T007]

### Implementation for User Story 1 (author-section)

- [ ] T009 [US1] Author skills/external/sdd-loop-driver/references/dispatch-recipes.md——断点探测配方（三信号 + 终态权威文档 + 收尾场景）、阶段提示词文件写入（heredoc）、runner 模板与 sed 派生、后台执行+日志回传+轮询、收尾纪律（合并回 main + 逐线汇总）；阶段链与哨兵字面量；git 状态判定判据文本；可见性契约操作规则内联（内容取材 data-model E-2…E-5/E-8 与 shared 底稿 external-dispatch-recipes.md，标注底稿身份）[blockedBy: T008]

### Verification for User Story 1

- [ ] T010 [US1] Verify C-4/C-8/C-9 绿 [green: contracts/skill-structure.md#C-4] [green: contracts/skill-structure.md#C-5] [green: contracts/skill-structure.md#C-6] [blockedBy: T008,T009]

**Checkpoint**: US4+US1 = MVP——skill 可加载、一遍性入口可按手册驱动（结构可验证；闭环演练在 T030/T031）

## Phase 4: User Story 2 — 独立校验的阶段判定与默认安全纪律 (Priority: P1)

**Goal**: stage-prompts.md 内联三段骨架 + G5 纪律行（C-5/C-6）+ 派发注入回传契约（C-13）+ 校验程序

**Independent Test**: C-6/C-13 测试转绿；骨架三段与 G5 纪律行逐字齐备

### Tests for User Story 2 (MANDATORY ⚠ red-first)

- [ ] T011 [US2] Author 骨架纪律测试 C-7（G5 五纪律行存在）、C-8（派发注入：最后行=哨兵或显式异常行、二者皆无=卡死信号）append 到测试文件 [blockedBy: T010]
- [ ] T012 [US2] Red-first 取证：C-7/C-8 FAIL 输出记录 [blockedBy: T011]

### Implementation for User Story 2 (author-section)

- [ ] T013 [US2] Author skills/external/sdd-loop-driver/references/stage-prompts.md（第一部分）——三段骨架全文（背景与权威文档/执行要求/完成尾标+回传契约）、G5 五纪律行、独立校验程序（尾标必要+产物核验+纪律抽查；校验者≠执行者）、提及已验证变体与卡死处置章节占位路由 [blockedBy: T012]

### Verification for User Story 2

- [ ] T014 [US2] Verify C-7/C-8 绿（C-10 的绿点在 US6——变体章节最后落位）[green: contracts/skill-structure.md#C-7] [green: contracts/skill-structure.md#C-8] [blockedBy: T012,T013]

**Checkpoint**: 校验程序与安全纪律可独立复核（US2 独立可测）

## Phase 5: User Story 3 — 卡死处置与状态落盘上报 (Priority: P1)

**Goal**: 卡死处置程序内联（C-7）——上送件四要素、禁静默规则、状态脊程序

**Independent Test**: C-7 测试转绿；四要素与「先写状态后派发」程序文本齐备

### Tests for User Story 3 (MANDATORY ⚠ red-first)

- [ ] T015 [US3] Author 卡死处置测试 C-9（四要素文本：发现了什么/为何吃重/已产生的中间产物逐项可定位/可选处置；MUST NOT 静默等待/静默修平；状态脊 U2/U4/U5 转移点程序）append [blockedBy: T014]
- [ ] T016 [US3] Red-first 取证：C-9 FAIL 输出记录 [blockedBy: T015]

### Implementation for User Story 3 (author-section)

- [ ] T017 [US3] Author stage-prompts.md（第二部分）——卡死处置与状态脊章节：超时/重试上限/预算/节奏缺省值（90 分钟/2 次，入口可覆盖）、达上限停环程序、上送件四要素、禁静默双规则、状态脊字段与写入时机（内容取材 data-model E-6/E-7 与规格 FR-017…FR-019）[blockedBy: T016]

### Verification for User Story 3

- [ ] T018 [US3] Verify C-7 绿 [green: contracts/skill-structure.md#C-9] [blockedBy: T016,T017]

**Checkpoint**: P1 三硬需求（自迭代 T009/独立校验 T013/卡死处置 T017）内容齐备

## Phase 6: User Story 5 — 多线并行与并发隔离 (Priority: P2)

**Goal**: 并发隔离声明与窄读法授权内容（B-3；无新 C 条款——回归绿 + 内容复核承载）

**Independent Test**: 全测试文件回归绿 + 章节内容与规格 FR-020/FR-021 一致（人工复核）

### Implementation for User Story 5 (author-section)

- [ ] T019 [US5] Author stage-prompts.md（第三部分）——多线并行与并发隔离章节：一线一连接/一线一状态脊、并发隔离显式声明（不读不改不提交清单）、窄读法授权（显式逐项有界、无隐式放行）、任一线失败不阻塞他线 [blockedBy: T018]

### Verification for User Story 5

- [ ] T020 [US5] Verify 回归：全测试文件仍全绿（无回归）+ 隔离章节内容人工复核对照 FR-020/FR-021 [blockedBy: T019]

**Checkpoint**: 并行语义可独立讲解（US5 独立可测）

## Phase 7: User Story 6 — 本地拓扑与已验证变体 (Priority: P2)

**Goal**: 变体内容落位（C-5 的最后构成段——本地简报先行/构建固化分线）

**Independent Test**: C-5 转绿（stage-prompts.md 全构成段齐备）

### Implementation for User Story 6 (author-section)

- [ ] T021 [US6] Author stage-prompts.md（第四部分）——变体章节：本地拓扑（qodercli 直驱 + 简报文件先行 `/tmp/<topic>-sdd-brief.md`）、构建固化变体（同主机按角色分线，参数实例化零机制分支）[blockedBy: T020]

### Verification for User Story 6

- [ ] T022 [US6] Verify C-10 绿（骨架/变体/纪律/卡死/状态脊五段齐备）[green: contracts/skill-structure.md#C-10] [blockedBy: T021]

**Checkpoint**: 全部内容章节落位——skill 内容面完成（author-section 收束）

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: 分发面（mirror-parity）、docs 面、render-verify 与 refresh-verify（US4 的交付义务 D 条款在此收束）

- [ ] T023 Author docs/reference/skills/sdd-loop-driver.md——机制定义+真源指针、双拓扑实例化指引（入口参数清单）、执行侧可移植性（零 .specify 依赖、三投递形态等价）、目标项目侧依赖说明（XV 判据撰写，C-14/C-15）[blockedBy: T022]
- [ ] T024 Verify D-1/D-2 绿（docs 页存在、四内容块齐、无保留名、XV 抽查）[green: contracts/distribution-and-docs.md#C-14] [green: contracts/distribution-and-docs.md#C-15] [blockedBy: T023]
- [ ] T025 [P] Update tests/contract/test_run_skills_wiring.py 的 BASELINE_EXTERNAL 名册加 `sdd-loop-driver`（C-16；名册加行不增测试数，预期仍 12 passed）[blockedBy: T022]
- [ ] T026 Verify C-16：`bash scripts/bash/run-tests.sh tests/contract/test_run_skills_wiring.py -q` 仍 12 passed 且含新名册 [green: contracts/distribution-and-docs.md#C-16] [blockedBy: T025]
- [ ] T027 Mirror write：`python3 scripts/python/sync-mirrors.py --write --only skills/external` 投影 sdd-loop-driver 到 .specify/skills/（C-11；禁手改镜像）[blockedBy: T022]
- [ ] T028 Verify C-11 自包含：`grep -n 'MUST.*\.specify/'` 于 skill 三文件零命中（注意排除底稿注解语境行，判据按 C-11 邻接词）[green: contracts/skill-structure.md#C-11] [blockedBy: T022,T024]
- [ ] T029 Verify C-12 + C-17：`diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` 为空；`sync-mirrors.py --check --only skills/external` 相对 T001 冻结基线无 NEW drift 行 [green: contracts/skill-structure.md#C-12] [green: contracts/distribution-and-docs.md#C-17] [blockedBy: T026,T027]
- [ ] T030 Render-verify：执行 quickstart.md 可执行场景并记录 notes/quickstart-run.md——S1 基线复测（三命令）、S3 前提探测（宿主 cwd 无 .specify 自证 + qodercli 在 PATH）；测试文件 19 函数齐（C-1…C-13 + C-14…C-19，即 C-18）；`git diff --stat HEAD -- templates/ src/ scripts/` 为空（C-19）；C-20 间接判据复跑（宪法门控扫描既有测试全绿）[green: contracts/distribution-and-docs.md#C-18] [green: contracts/distribution-and-docs.md#C-19] [blockedBy: T028,T029]
- [ ] T031 真实/演练驱动验收（D-9/SC-001/SC-002/SC-003/SC-004/SC-005/SC-006/SC-007）：本地拓扑全闭环至少一轮（qodercli available）；远端拓扑轮次经用户确认目标别名后执行（Environment Prerequisites remote 行）；伪完成变异演练（SC-003）；异常注入（SC-004）[blockedBy: T030]
- [ ] T032 SC 状态核对与 Feature 收尾：SC-001…SC-009 逐条对照 T031 证据具状态（可核/如实 partial/deferred）；Feature 索引行与详情文件记录实现期要点（feature-integration 义务）[blockedBy: T031]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，立即可始；T001 冻结的基线被 GATE-1/GATE-2 与 T028 消费
- **US4 (Phase 2)**: 依赖 Setup——skill 骨架是全部后续内容章节的路由宿主
- **US1→US2→US3 (Phase 3–5)**: 依次依赖（同测试文件 append 串行 + 章节同文件依赖）；US3 后 P1 三硬需求齐
- **US5/US6 (Phase 6–7)**: 依赖 US3（stage-prompts.md 顺序追加）
- **Polish (Phase 8)**: 依赖 US6（内容面收束后分发/验证面收束）；T031 远端段需用户确认目标环境

### User Story Dependencies

- US4 是结构宿主（SKILL.md 先行）；US1/US2/US3/US5/US6 的内容章节向 references/ 两文件顺序追加——同文件写入以 blockedBy 串行，绿点按条款分区无冲突
- 各故事 Checkpoint 独立可测（结构测试逐条款转绿即该故事可独立验证）

### Parallel Opportunities

- T002 与 T001 并行（不同文件）
- T023（docs 页）与 T025（名册）并行（不同文件）
- T026/T027 在各自 blockedBy 满足后可并行（测试文件 vs 镜像目录）
- 测试文件 append 任务（T003/T007/T011/T015）因同文件天然串行，无 [P]

---

## Parallel Example: Phase 8

```bash
# T023 与 T025 并行（不同文件）：
Task: "Author docs/reference/skills/sdd-loop-driver.md"
Task: "Update tests/contract/test_run_skills_wiring.py BASELINE_EXTERNAL"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US4 + US1（同为 P1；skill 骨架 + 入口派发内容合起来才构成「可加载、可按手册驱动」的独立增量——US4 单独只是骨架，US1 单独无承载宿主）。

1. Phase 1 Setup → 2. US4（骨架+结构测试绿）→ 3. US1（机制内容+测试绿）→ 4. **STOP and VALIDATE**：skill 三文件结构可验证、路由成立
5. 续 US2/US3（P1 补齐三硬需求）→ US5/US6 → Polish 分发与验收

### Incremental Delivery

每故事 Checkpoint 独立可测；author-section 每段落即测试逐条款转绿；分发面（mirror/roster/docs）在内容面收束后一次性收束（T022 后）。

### 单代理策略

按相位顺序 T001→T032 串行执行即可；[P] 标记仅供多代理并行参考。

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- 红先于绿：每个 author-section 前其契约测试先红（red-first-evidence.md 留痕）
- 底稿引用纪律：references 内容取材 shared 两份底稿时标注底稿身份（C-11 语境判据）
- **契约条款重编号披露（2026-10-15，tasks 首跑 validator 实测）**：D 条款 id 不符条款语法真源（`shared/definitions/contract-clause-definitions.md` §1：id 形态 MUST 为 `C-<数字>`，extractor 实测对 D 文件返回 md-none）——两契约按交付顺序重编号：skill-structure C-1…C-13 重排（旧 C-8→C-5、C-9→C-6、C-6→C-7、C-13→C-8、C-7→C-9、C-5→C-10、C-10→C-11、C-11→C-12、C-12→C-13）、distribution D-1…D-9 → C-14…C-22；引用面（plan/data-model/feature-ref/tasks）已同步，实现未开始零悬空
- Commit after each task or logical group
- **Deferral discipline**: T031 远端段若实现期用户未确认目标环境，按 `[~]` + `<!-- deferred: <reason> -->` 显式延期，不留 `[ ]`
