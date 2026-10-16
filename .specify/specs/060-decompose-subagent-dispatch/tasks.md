# Tasks: 「驱动子代理」机制的技能化分解与公用化

**Branch**: `060-decompose-subagent-dispatch` | **Date**: 2026-10-16
**Feature**: Feature 060（Requirement `060-decompose-subagent-dispatch` 绑定，1:1）
**Input**: plan.md + requirements.md + data-model.md + contracts/ ×3 + quickstart.md + feature-ref.md

**Tests Mode**: ON（Constitution Principle IV "Test-First & Contract-Driven Implementation" 命中测试强制关键词；交付面为 Markdown 制品——依 Principle VII template-only 门以**结构契约测试**承载：34 条款 C-1..C-34 逐条先红后绿 + C-35 平价底册锚点，全部落在 `tests/contract/test_agent_dispatch_mechanism.py`）

**Organization**: 本特性为 doc-feature（交付物 = 技能体 + 真源文档 + 模板 + docs 页 + 契约测试），相位内采用 doc-feature 分类：author-section → mirror-parity → render-verify → refresh-verify；不适用 Models→Services→Endpoints。测试函数分四批 append 到同一测试文件——Author 行以 [blockedBy] 串行化（同文件写入），绿点由 Verify 行与完成行认领（T022 认领 C-35，其余 Verify 行认领；每条款恰认领一次）。

## Definition of Done (DoD)

- DoD-1: 全部任务行 `[X]`（或 `[~]` 带 deferred 理由），零 `[ ]`/`[>]` 残留
- DoD-2: 契约测试 C-1..C-35 全绿（`tests/contract/test_agent_dispatch_mechanism.py`）
- DoD-3: 既有套件 name-level 零新增失败（对比 T001 冻结名单）
- DoD-4: 镜像义务全落位——sync-mirrors 触碰对零 NEW drift、compile-embeds 零漂移
- DoD-5: 副本归零检索达标（quickstart S2 三组判据：成组共现恰 1 落点等）
- DoD-6: SC-001..006 逐条在 verification.md 记录状态

**DoD Status**: pending

## Completion Gate

- GATE-1: 全量套件零 NEW 失败 — check: `python3.14 -m pytest tests/contract/ tests/integration/ -q` 与 T001 冻结名单 `comm -13` 为空
- GATE-2: 镜像义务逐对验证 — check: `python3 scripts/python/sync-mirrors.py --check`（触碰对零 NEW drift；既有 instructions-template DIFF 不计）
- GATE-3: 无 `[ ]`/`[>]` 任务行残留 — check: `grep -cE '^- \[[ >]\]' tasks.md` 返回 0
- GATE-4: verification.md 逐 SC 记录 — check: grep SC-001..SC-006 对照 requirements.md
- GATE-5: 契约测试全绿 — check: `python3.14 -m pytest tests/contract/test_agent_dispatch_mechanism.py -q` 0 failed

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行（不同文件、无未完成依赖）
- **[Story]**: 所属用户故事（US1..US4）；Setup/Foundational/Polish 相位无标签
- **[blockedBy: Txxx]**: 显式依赖——被列任务未 `[X]` 前本任务 MUST NOT 开始
- **[green: <contract>#<clause>]**: 绿点认领——本行负责使该契约条款转绿；每条款全仓恰认领一次（重复=collision，回退=backwards，同名测试文件双行=divergence）
- 每任务单行（含路径与标签）；路径用仓库相对路径

---

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 冻结改前基线到 `.specify/specs/060-decompose-subagent-dispatch/notes/pre-change-measurements.md`——逐项实跑并粘贴真实输出：① quickstart S2 三组副本检索（ConnectTimeout 成组共现/nohup su -/反嵌套字面——基线含 2 个 git-utils 误中样本注记）；② 条款计数再派生（contracts 三文件 C-1..C-35 = 8+17+10、P 表 15 行、data-model V-E 13 条——`grep -cE` 实跑）；③ 全量契约套件失败名单（`python3.14 -m pytest tests/contract/ -q` 的 FAILED 名单，供 GATE-1 comm 比对；消费义务属 /speckit.implement `**Test runs**` bullet）；④ 三引擎基线（sync-mirrors --check 既有 DIFF 1 条 / compile-embeds --check 73 units 零漂移 / regen-command-copies --check OK）

## Phase 2: Foundational (Blocking Prerequisites — 真源深化 C-1..C-8)

- [X] T002 Author 真源契约测试 C-1..C-8（agent-definitions 接线段存在+职责切分线+无第三 owner、拓扑声明段+分工不变+反嵌套引用、层界三行判定+越层禁令）append 到 `tests/contract/test_agent_dispatch_mechanism.py`——先红，红证据记录 `.specify/specs/060-decompose-subagent-dispatch/notes/red-first-evidence.md` [blockedBy: T001]
- [X] T003 [P] Author `shared/definitions/agent-definitions.md` 驱动子代理接线段（Transformation Chain 后：创建经 create-agent/派发经 run-agent/修正经 improve-agent）+ 职责切分线 + 层界三行判定 + 越层禁令（C-1/C-2/C-7/C-8）[blockedBy: T002]
- [X] T004 [P] Author `shared/definitions/subagent-definitions.md` Execution 拓扑声明段（本地/远端要素表+内联/配置双形态+冲突拒收）+ 分工不变声明 + Dispatch-Time Governance 反嵌套引用行（C-4/C-5/C-6）[blockedBy: T002]
- [X] T005 Verify C-1..C-8 绿：`python3.14 -m pytest tests/contract/test_agent_dispatch_mechanism.py -q` 全绿并记录 + shared 镜像同步（`python3 scripts/python/sync-mirrors.py --write`）+ shared 对零 NEW drift [green: contracts/concept-and-sources.md#C-1] [green: contracts/concept-and-sources.md#C-2] [green: contracts/concept-and-sources.md#C-3] [green: contracts/concept-and-sources.md#C-4] [green: contracts/concept-and-sources.md#C-5] [green: contracts/concept-and-sources.md#C-6] [green: contracts/concept-and-sources.md#C-7] [green: contracts/concept-and-sources.md#C-8] [blockedBy: T002,T003,T004]

## Phase 3: User Story 1 - 从能力模板到职责实例的创建面（Priority: P1） 🎯

**Story Goal**: 「SDD 执行者」能力模板进框架分发角色集 + 多职责实例化 + 退役生命周期，经 create-agent 完整可复现。

**Independent Test**: 仅凭本故事即可创建模板与 ≥2 实例并审计引用关系（SC-001 判据），不依赖派发面。

- [X] T006 [US1] Author create-agent 契约测试 C-9..C-14（模板合法性与职责零命中、内容判据机械面、判据入 SKILL.md、多职责实例化、退役生命周期、agents 镜像对）append 到 `tests/contract/test_agent_dispatch_mechanism.py`——先红 [blockedBy: T002]
- [X] T007 [P] [US1] Author `agents/sdd-executor.agent.md`——中性词表 frontmatter（name/description/user-invocable: false/model-tier/capability-tools/skills/run-turn-budget）+ 三要素能力面 + 职责字样与专用信息字面量零命中（C-9/C-10）[blockedBy: T002]
- [X] T008 [P] [US1] Enhance `skills/internal/create-agent/SKILL.md`——模板分发层内容判据（C-11）+ 多职责实例化与 team-scope 互斥说明（C-12）+ Agent Lifecycle 节退役规则扩格（C-13）[blockedBy: T002]
- [X] T009 [US1] render-verify：`specify render-agents --ai qoder` 实跑 + `.qoder/agents/sdd-executor.agent.md` 生成入 render-manifest 检查 [blockedBy: T007]
- [X] T010 [US1] Verify C-9..C-14 绿 + 镜像同步（agents 对 + internal 对）[green: contracts/skill-enhancements.md#C-9] [green: contracts/skill-enhancements.md#C-10] [green: contracts/skill-enhancements.md#C-11] [green: contracts/skill-enhancements.md#C-12] [green: contracts/skill-enhancements.md#C-13] [green: contracts/skill-enhancements.md#C-14] [blockedBy: T006,T007,T008,T009]

## Phase 4: User Story 2 - 拓扑声明与执行派发面（Priority: P1） 🎯

**Story Goal**: run-agent 接受拓扑声明（本地/远端、内联/配置、冲突拒收）、承载五族前置检查+处置链、反嵌套义务入派发治理、配方引用不复制。

**Independent Test**: 对任一既有实例以本地拓扑发起真实执行并以命令形态审计远端形态（SC-002 判据），不依赖两技能改造。

- [X] T011 [US2] Author run-agent 契约测试 C-15..C-21（拓扑输入形态、冲突拒收、preflight 文件与 SKILL 接线、配方引用不复制、反嵌套义务、既有规则零改写）append 到 `tests/contract/test_agent_dispatch_mechanism.py`——先红 [blockedBy: T006]
- [X] T012 [P] [US2] Author `skills/internal/run-agent/references/dispatch-preflight.md`——五族前置检查表+失败处置链上收（内容取材 loop-driver Preflight 现行正文，行为平价搬家；本地拓扑跳过注记保留）（C-17）[blockedBy: T001]
- [X] T013 [P] [US2] Enhance `skills/internal/run-agent/SKILL.md`——Run Mode 增拓扑声明输入（C-15）+ 冲突拒收（C-16）+ preflight 接线（C-18）+ 配方引用 [[STR-006]]（C-19）+ 派发治理增反嵌套义务（C-20）+ 既有边界条文零改写自审（C-21）[blockedBy: T002]
- [X] T014 [US2] Verify C-15..C-21 绿 + 镜像同步（internal 对）[green: contracts/skill-enhancements.md#C-15] [green: contracts/skill-enhancements.md#C-16] [green: contracts/skill-enhancements.md#C-17] [green: contracts/skill-enhancements.md#C-18] [green: contracts/skill-enhancements.md#C-19] [green: contracts/skill-enhancements.md#C-20] [green: contracts/skill-enhancements.md#C-21] [blockedBy: T011,T012,T013]

## Phase 5: User Story 3 - 两技能的委派化改造（Priority: P1） 🎯

**Story Goal**: sdd-loop-driver 与 sdd-project-setup 机制段坍缩为引用、委派说明段落位、P 表逐行对账、docs 页更新——行为平价零丢失。

**Independent Test**: 对任一目标项目（本地拓扑）驱动一个 SDD 阶段与一个调协步骤，行为平价；副本归零检索达标（SC-003/SC-004）。

- [X] T015 [US3] Author 委派化契约测试 C-26..C-35（拓扑改引用、Preflight/配方坍缩、骨架保留+机制引用、编排本体保留、setup 两侧坍缩、委派说明段、外部行为零变更、自足可加载、P 表逐行填实）append 到 `tests/contract/test_agent_dispatch_mechanism.py`——先红（对当前树副本仍在，天然红）[blockedBy: T011]
- [X] T016 [US3] Rewrite `skills/external/sdd-loop-driver/SKILL.md`——Driver Topology 节改引用+循环视角自检行、HR-6 同步改写（C-26）[blockedBy: T014]
- [X] T017 [P] [US3] Rewrite `skills/external/sdd-loop-driver/references/dispatch-recipes.md`——Preflight 节清零引用 run-agent dispatch-preflight.md、Recipe 0/1/2/3/5 同型机制段坍缩引用 [[STR-006]]、保留差异面（心跳/定间隔分级/多线批查/双线隔离）并注明（C-27）[blockedBy: T014]
- [X] T018 [P] [US3] Rewrite `skills/external/sdd-loop-driver/references/stage-prompts.md`——三段骨架内容保留、机制红线段改引用 run-agent 反嵌套义务（C-28）[blockedBy: T014]
- [X] T019 [US3] Enhance `skills/external/sdd-loop-driver/SKILL.md`——增补「子代理创建与派发委派」说明段（实例创建→create-agent、阶段派发→run-agent，输入/产出说明）（C-29）[blockedBy: T010,T014,T016]
- [X] T020 [P] [US3] Rewrite `skills/external/sdd-project-setup/references/setup-recipes.md`——S4 五族检查表清零引用、软协同 handoff 段收敛单侧引用、远端命令形态坍缩引用（C-30/C-31）[blockedBy: T014]
- [X] T021 [US3] Enhance `skills/external/sdd-project-setup/SKILL.md`——增补委派说明段（盘点脚本执行主体、S2/S3 治理命令派发经 run-agent 可选形态）（C-32）[blockedBy: T010,T014,T020]
- [X] T022 [US3] 义务平价对账：`contracts/delegation-parity.md` § P 表 P-01..P-15 逐行填实（新落点/强度/追溯三列以实存证据填齐，更严处注明），发现额外义务按同格式追加（C-35，绿点由 T023 认领）[blockedBy: T016,T017,T018,T019,T020,T021]
- [X] T023 [US3] Verify C-26..C-34 绿 + 镜像同步（skills 对）[green: contracts/delegation-parity.md#C-26] [green: contracts/delegation-parity.md#C-27] [green: contracts/delegation-parity.md#C-28] [green: contracts/delegation-parity.md#C-29] [green: contracts/delegation-parity.md#C-30] [green: contracts/delegation-parity.md#C-31] [green: contracts/delegation-parity.md#C-32] [green: contracts/delegation-parity.md#C-33] [green: contracts/delegation-parity.md#C-34] [green: contracts/delegation-parity.md#C-35] [blockedBy: T015,T016,T017,T018,T019,T020,T021]
- [X] T024 [US3] Update `docs/reference/skills/sdd-loop-driver.md` 与 `docs/reference/skills/sdd-project-setup.md`——机制归属说明（派发机制真源已迁 run-agent/配方真源；软协同契约不变）[blockedBy: T019,T021,T023]

## Phase 6: User Story 4 - 执行证据回流（Priority: P2）

**Story Goal**: 执行证据（三元组/日志/异常回传行/失败模式）可经 improve-agent 回流为 Template/Instance 层修正，Execution 不自改边界保持。

**Independent Test**: 以一次已知失败执行记录走 improve-agent 流程产出定向修正且 Execution 产物零改动。

- [X] T025 [US4] Author improve-agent 契约测试 C-22..C-23（证据输入形态、Self-Improvement 边界保持）append 到 `tests/contract/test_agent_dispatch_mechanism.py`——先红 [blockedBy: T011,T015]
- [X] T026 [US4] Enhance `skills/internal/improve-agent/SKILL.md`——Input Contract 增执行证据输入形态（C-22）+ Self-Improvement 边界不动自审（C-23）[blockedBy: T002]
- [X] T027 [US4] Verify C-22..C-23 绿 + 镜像同步（internal 对）[green: contracts/skill-enhancements.md#C-22] [green: contracts/skill-enhancements.md#C-23] [blockedBy: T025,T026]

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T028 全量镜像验证：`python3 scripts/python/sync-mirrors.py --check` 触碰对（agents/internal/skills/shared）零 NEW drift——既有 instructions-template DIFF 1 条不计入（C-24）[blockedBy: T005,T010,T014,T024,T027]
- [X] T029 编译面复核：`python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` 零漂移 + unit 认领面复核（73 units 基线对照）（C-25）[blockedBy: T028]
- [X] T030 Verify C-24/C-25 绿并记录 [green: contracts/skill-enhancements.md#C-24] [green: contracts/skill-enhancements.md#C-25] [blockedBy: T028,T029]
- [X] T031 quickstart 复跑留痕到 `.specify/specs/060-decompose-subagent-dispatch/notes/quickstart-run.md`——S1 内容判据（对 sdd-executor 复跑预期空输出）、S2 三组检索复测（恰 1 落点判定，scope=框架源侧 skills/ shared/ 排除镜像）、S3 引擎复跑；S4/S5 段由 T034–T036 回填 [blockedBy: T030]
- [X] T032 全套件 name-level 对比：`python3.14 -m pytest tests/contract/ tests/integration/ -q` 与 T001 冻结名单 comm 零新增（消费义务见 /speckit.implement `**Test runs**` bullet）[blockedBy: T030]
- [X] T033 feature-ref 交付清单对账（14 项逐项存在性检查）+ Feature 列表复审（无新 Feature、无既有失效，状态维持 Planned 不越权）[blockedBy: T023,T024]

---

## Phase 8: User Story Acceptance Evidence（SC-001/002/004 实跑承载——analyze H-02 修复）

> SC-001/002/004 的验收证据此前零任务承载（analyze H-02）：三行落在对应故事的 Verify 之后，产出直接供 verification.md 逐 SC 记录（DoD-6/GATE-4 的证据来源）。

- [X] T034 [US1] SC-001 实跑：经 create-agent 从 sdd-executor 实例化 ≥2 个职责实例（sdd-setup-executor / sdd-requirements-executor），并按 SC-001 判据审计——实例体对模板能力的复述零命中（grep capacity-scope 引用计数 + 能力描述句检索），证据落 `verification.md` [blockedBy: T010]
- [X] T035 [US2] SC-002 实跑：同一实例以本地拓扑完成一次真实执行 + 远端拓扑以派发命令形态逐要素审计（ssh/su/CLI/目录）；两形态下 Template/Instance 制品 diff 为空判定，证据落 `verification.md` [blockedBy: T014]
- [X] T036 [US3] SC-004 端到端：经 run-agent 派发一个阶段实例在本地项目完成一个 SDD 阶段，回传三条件核验（完成尾标/产物在位/显式异常行）+ 子代理输入文件反嵌套审计（驱动技能引用零命中），证据落 `verification.md`；末次执行后回填 quickstart S4/S5 免责段为实跑留痕（M-06 同批：S2 判定 scope=框架源侧）[blockedBy: T014,T024]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，立即开始
- **Foundational (Phase 2)**: 依赖 T001——BLOCKS 全部用户故事（真源深化是三技能承接面的语义底座）
- **US1/US2 (Phase 3/4)**: 依赖 Foundational；US1 与 US2 相互独立可并行（不同文件面）
- **US3 (Phase 5)**: 依赖 US1（T010）与 US2（T014）——委派化的引用目标必须先落位；相位内 T016→T019 串行（同文件）
- **US4 (Phase 6)**: 依赖 Foundational；与 US1/US2/US3 无文件冲突可并行
- **Polish (Phase 7)**: 依赖全部用户故事 Verify 完成

### User Story Dependencies

- **US1 (P1)**: Foundational 后即可开工——产出模板与实例（SC-001）
- **US2 (P1)**: Foundational 后即可开工——preflight 上收与派发面（SC-002 前置）
- **US3 (P1)**: blockedBy US1+US2——委派化把机制段指向新落点（SC-003/SC-004）
- **US4 (P2)**: Foundational 后即可开工——证据回流形态（FR-014）

### Parallel Opportunities

- T003/T004（两真源文件互不相交）
- T007/T008（模板与 create-agent SKILL.md）
- T012/T013（preflight 新文件与 run-agent SKILL.md）
- T016/T017/T018/T020（四处不同文件的委派化改写——注意 T019 与 T016 同文件须串行）
- 各相位 Author 行与实现行的测试文件写入以 [blockedBy] 串行，不做 [P]

## Implementation Strategy

- **MVP scope**: US1 + US2 + US3（三个 P1 故事合在一起才构成可独立验证的机制闭环——US1 无消费面、US3 无承接面则各为半机制）；US4（P2）为独立增强，可后置
- **先红后绿**: 每相位 Author 行先落测试并记录红证据（notes/red-first-evidence.md），实现行转绿，Verify 行认领绿点
- **平价优先**: US3 每处删改前对照 T001 冻结的改前原文清单——义务零丢失（P 表逐行可追溯）优先于文字优美
- **镜像纪律**: 每相位结束即同步镜像（doc-feature mirror-parity 行），Polish 相位全量复核——不留跨相位漂移
