# Tasks: 授权席位的有界嵌套 SDD 调用与确定性分流（Authorized Routing & Nested SDD Invocation）— Feature 074 / Slice 074a

**Requirement ID**: 074a（Feature 074 的第一个切片；不新建 Feature ID、不新增注册行）
**Requirement Key**: `074a-authorized-routing`
**Branch**: `074-goal-team-sdd-unification`
**Related Feature**: 074 Goal/Team/Agent 与 SDD 开发流程统一（切片复用同一注册行；本阶段状态天花板 `Planned`）
**Input**: Design documents from `.specify/specs/074a-authorized-routing/`
**Prerequisites**: plan.md（技术路线、Mirror Obligations、Structure Decision）、requirements.md（20 FR / 6 SC / 10 STR；Clarifications D-1/D-2/D-3）、research.md（RA1–RA9）、data-model.md（E1–E9 / V-1…V-29 / 3 状态机）、contracts/ ×4（47 条款：`hierarchy-and-authorization.md` 16 / `routing-decision.md` 14 / `nested-invocation.md` 13 / `bootstrap-and-maintenance.md` 4）、quickstart.md（S1–S7）、feature-ref.md（交付面 15 行、FR/SC 映射、7 条裁示）

**Tests Mode**: ON（Constitution Principle IV "Test-First & Contract-Driven Implementation" 为测试强制原则——纯函数/工具 MUST 有单测、关键流程 MUST 有自动化回归覆盖；本切片交付可执行的只读引擎、框架源码编辑与四份契约，非 template-only，故不适用结构性契约测试替代运行时测试的豁免。5 个新测试文件（1 个夹具模块旁挂）一律红先：先跑出失败并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`，再进入对应实现行。）

**Tests**: 红先证据的唯一落点是 `.specify/specs/074a-authorized-routing/notes/red-first-evidence.md`（每支测试一条：命令、真实输出、退出码）。失败 nodeid 名集的捕获与比较形式归 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs，本文件只给路径与命令，不复述比较形式。

**Organization**: 按用户故事组织——US1（授权席位启动一次有界嵌套 SDD 运行并拿回 handoff）、US2（确定性三值分流把 SDD 与直接修改分开）、US3（嵌套被治理而非被逃脱）。US1 与 US2 同为 **Priority P1**（沿用 requirements 标签，不重排），两者共同构成 MVP——只有「分流裁决」而无「授权席位启动嵌套运行」时，本切片不可独立演示，反之亦然。两者在行序上按**交付依赖**排列而非按故事号：US1 的入口校验消费「一条已记录的裁决」（data-model E4 字段面，夹具自带），因此不依赖 US2 的引擎，先落 US1 使两个 P1 故事各自独立可测。Foundational 只承载词汇 owner 文档的地基三节，三条用户故事的全部其他面都按路径引用它。Polish 收口镜像、单一 owner 审计、结构面、回归、SC 证据与登记。

## Definition of Done (DoD)

- DoD-1: 全部 32 行任务为 `[X]`；若出现 `[~]`，其理由逐条记录在 `.specify/specs/074a-authorized-routing/verification.md` 的 `deferred_tasks=`。
- DoD-2: 交付面按 `feature-ref.md` § 2 的 **15 行 = 9 新 + 6 改**落地——9 新 = 3 个新框架文件（`shared/definitions/sdd-routing-definitions.md`、`scripts/python/sdd-route.py`、`skills/external/sdd-loop-driver/references/nested-invocation.md`）+ 5 个新测试文件 + 1 个新夹具；6 改 = 5 个被编辑的框架源文件（`shared/definitions/subagent-definitions.md`、`src/specify_cli/__init__.py`、`skills/internal/run-agent/SKILL.md`、`skills/internal/create-team/references/create-mode.md`、`skills/external/sdd-loop-driver/SKILL.md`）+ 1 个既有测试文件（`tests/contract/test_neutral_metadata_schema.py`，声明的 pin 变更）；零新增 `/speckit.*` 命令、零新增技能。
- DoD-3: 4 份契约共 47 条款（16 + 14 + 13 + 4）每条恰被一个任务行 `[green:]` 认领一次；`account-clause-coverage.py` 报告 `claimed clauses = 47`、`FR 20 / 20`、`uncovered beyond baseline = 0`；每个契约内认领顺序单调递增。
- DoD-4: 5 支新测试全绿；相对 T002 重采的名字级基线零**新增**失败 nodeid（既有红不修、不掩盖；名单与计数以 `test-evidence/targeted-set-v1-baseline.txt` 为唯一所有者，本文件不复述数字）。
- DoD-5: plan.md § Mirror Obligations 逐行落地——7 个源文件的 `.specify/` 投影 `cmp` 同字节；`sync-mirrors.py --check` 相对 T001 基线零新增差异；`regen-command-copies.py --check` 继续 `OK`（证明 `templates/commands/` 零改动）；零手改镜像。
- DoD-6: 路由四项事实（五项输入取值域 / 三值裁决表 / 固定优先级 / 理由码词表）只在 `shared/definitions/sdd-routing-definitions.md` 落盘一次，其余新增面按路径抵达；本切片零新增 registry、ledger、状态脊、ownership 模型、集成队列、确认门、调度器、守护进程或自动传输。
- DoD-7: `verification.md` 逐条列 `- **SC-001**` … `- **SC-006**` 的状态（只从 `.specify/templates/verification-log-template.md` 的封闭词表取值）、命令、输出摘要与证据指针；无来源的量记 `not-evaluated` + reason，不记 0、不记达成。
- DoD-8: plan_constraint 全趟遵守——`plan.md` / `data-model.md` / `contracts/` / `quickstart.md` / `research.md` / `feature-ref.md` 的任一改动只能是行级小修（错字 / 措辞 / 断链 / 格式 / 行级一致），逐项在 `verification.md` 声明 `PLAN-EDIT: <path> — <理由>；分类=minor`；任何实质性改动停线回抛，不静默重写。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/074a-authorized-routing/tasks.md` exit 0（0 error / 0 warning）。
- GATE-2: 跨产物一致 — check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/074a-authorized-routing --stage tasks --repo .` 输出 `decision=pass` 且 errors=0（advisory 逐条裁定并记录）。
- GATE-3: 分解规模合法 — check: `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/074a-authorized-routing/requirements.md --tasks .specify/specs/074a-authorized-routing/tasks.md` 结论为 `proceed`（task rows ≤ 40）。
- GATE-4: 条款覆盖完整 — check: `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/074a-authorized-routing` 输出 `claimed clauses = 47`、`FR uncovered: 0`、beyond-baseline = 0。
- GATE-5: 测试零新增失败 — check: `test-evidence/targeted-set-v1-baseline.txt` 记录的 13 文件定向套件重跑后，失败 nodeid 排序与 T002 重采名单做 `comm -13` 为空（名字级，非计数级）。
- GATE-6: 镜像与副本零漂移 — check: `python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/regen-command-copies.py --check` 均 exit 0，且与 `notes/pre-change-measurements.md` 的改前基线比较零新增差异。
- GATE-7: 零新增存储面 — check: `.specify/state/`、既有 line registry 目录与 `.specify/memory/` 的文件名集合，相对 `notes/pre-change-measurements.md` 的改前基线做 `comm -13` 为空。
- GATE-8: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/074a-authorized-routing/tasks.md` 返回 0。
- GATE-9: SC 证据齐备 — check: `grep -cE '^- \*\*SC-00[1-6]\*\*' .specify/specs/074a-authorized-routing/verification.md` 返回 6。

## Environment Prerequisites

<!-- 本节是环境判定的单一落点：任何任务行只引用本节，不复述结论。 -->

- pytest（`python3 -m pytest`）: **available** — probe: `python3 -m pytest --version` → `pytest 8.4.2` @ 2026-10-29；affected: T005、T007、T012、T016、T018、T021、T022、T025、T029。
- git（`log` / `status` / `cmp` 所需的 HEAD 读取）: **available** — probe: `git rev-parse HEAD` → `907d21fbe`；`git status --short` 可读 @ 2026-10-29；affected: T001、T012、T029。
- 容器运行时 / 镜像仓库 / 活集群 / 外网: **none** — 本切片全部检查为本地文件、`git` 与本地 pytest，无构建、无拉取、无网络 @ 2026-10-29；affected: none。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标不同、无未完成依赖）。本文件只有 Setup 的 T002/T003 满足该条件（写目标分别是 `test-evidence/targeted-set-v1-baseline.txt` 与 `coverage-baseline.txt`）；用户故事内的红先行共用 `notes/red-first-evidence.md` 这一追加落点，Polish 的 T027 / T028 共用 `notes/quickstart-run.md` 这一追加落点，T026 逐对核对时点名全部源文件——共享 sink 或共享点名面即同写目标，故这两段零 `[P]`（按行序串行，不靠删路径消警）。
- **[Story]**: 用户故事标签（`[US1]`…`[US3]`），只出现在用户故事阶段的任务行；Setup / Foundational / Polish 阶段零 `[US` 标记。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全部 `[X]` 前不得开始本行。仅阶段顺序关系时不写。
- **[green: <contract>#<clause>]**：绿点认领——本行是使该条款转绿的那一行；契约路径相对本文件目录解析。47 条款分区：`hierarchy-and-authorization.md` C-1…C-2→T004、C-3→T008、C-4→T009、C-5→T010、C-6…C-8→T011、C-9…C-10→T023、C-11…C-14→T024、C-15…C-16→T025；`routing-decision.md` C-17→T004、C-18…C-27→T017、C-28→T019、C-29→T020、C-30→T027；`nested-invocation.md` C-31…C-33→T013、C-34…C-37→T014、C-38…C-40→T015、C-41…C-42→T016、C-43→T028；`bootstrap-and-maintenance.md` C-44…C-46→T004、C-47→T028。每条恰一行认领，`validate-tasks.py` 四项 green 检查 + `account-clause-coverage.py` 核对。
- 每行必须单行完成（含文件路径与全部标签），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `verification.md` 的 `deferred_tasks=`）。

## Path Conventions

- **框架源（编辑面）**: `shared/definitions/`、`src/specify_cli/__init__.py`、`scripts/python/`、`skills/internal/`、`skills/external/sdd-loop-driver/`、`tests/contract/`、`tests/fixtures/`。
- **生成面（MUST NOT 手改）**: `.specify/shared/`、`.specify/skills/`、`.specify/scripts/`（`sync-mirrors.py` 投影）；每工具命令副本（`regen-command-copies.py` 生成）。
- **证据落点（本切片）**: `.specify/specs/074a-authorized-routing/` 下的 `notes/pre-change-measurements.md`、`notes/red-first-evidence.md`、`notes/quickstart-run.md`、`coverage-baseline.txt`、`test-evidence/targeted-set-v1-baseline.txt`、`verification.md`。
- **禁改面**: `.specify/specs/074-goal-team-sdd-unification/**`（父 spec 与父设计，含其 `tasks.md`，只读）；`.specify/specs/074b-nested-governance`（兄弟切片，尚未开始）；`templates/commands/**`（本切片零改动）；`.specify/memory/constitution.md`（本切片不改宪法）。
- **plan-owned 面（仅小修）**: `plan.md`、`data-model.md`、`contracts/**`、`quickstart.md`、`research.md`、`feature-ref.md`。
- **074b 承接、本切片 MUST NOT 实现**: 父 `US4`/`US5`、父 `FR 020`–`FR 024`、父 `FR 026`–`FR 028`、team report 的 `## Nested SDD Runs` 段标题与段语义、父 `STR 010` 字面量。

## Measured Premises (re-measured at generation time 2026-10-29, HEAD `907d21fbe`)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 需求条目计数（FR / SC / STR） | `grep -cE '^\- \*\*FR-[0-9]+\*\*:' …/requirements.md`；同法 `SC-`；`grep -cE '^\| \`STR-[0-9]+\`' …/requirements.md` | 20 / 6 / 10 |
| 契约条款数（逐文件 + 合计） | `grep -cE '^\*\*C-[0-9]+\*\*' .specify/specs/074a-authorized-routing/contracts/*.md`；合计 `grep -ohE '^\*\*C-[0-9]+\*\*' …/contracts/*.md \| wc -l` | 16（hierarchy）/ 14（routing）/ 13（nested）/ 4（bootstrap）；合计 **47** |
| 9 个新文件当前状态 | 逐个 `test -e`（3 个框架文件 + 5 个测试文件 + 1 个夹具） | 9/9 ABSENT（红先的前提） |
| `sdd-invocation` 在代码 owner 的已落盘处数 | `grep -c 'sdd-invocation' src/specify_cli/__init__.py` | `0`。**陷阱形**：`grep -rn 'sdd-invocation' .` 会命中本切片设计文档的说明文字（requirements / plan / data-model / contracts），那是引用不是定义；计量单位是代码 owner 文件，不是全仓 |
| 中性键 owner 位置 | `grep -n 'NEUTRAL_AGENT_METADATA_KEYS\s*=\|NEUTRAL_AGENT_FRAMEWORK_KEYS\s*=' src/specify_cli/__init__.py` | `119`（metadata 映射）/ `149`（framework frozenset）；pin 面在 `tests/contract/test_neutral_metadata_schema.py:130`（frozenset 等值）与 `:137`（成员交叉核对） |
| 反嵌套义务 owner 位点 | `grep -n 'Dispatch-Time Governance Obligation' shared/definitions/subagent-definitions.md`；`grep -n 'loop depth' …` | 章节 `:98`；待改句 `:104`（`loop depth is always 1: driver → stage executor`） |
| `team.md` schema owner 位点 | `grep -n 'Persisted \`team.md\` schema' skills/internal/create-team/references/create-mode.md` | `:51`（`seats` 块映射的落点） |
| 驱动参考目录在位、新参考文件缺失 | `ls skills/external/sdd-loop-driver/references/` | 目录在位（cli/ 与 6 个 .md）；`nested-invocation.md` ABSENT |
| 镜像基线 | `python3 scripts/python/sync-mirrors.py --check` | exit 0；六对 `ok`：templates 22 / skills-external 405 / skills-internal 136 / agents 3 / scripts 113 / shared 58 |
| 命令副本基线 | `python3 scripts/python/regen-command-copies.py --check` | `OK: all per-tool command copies match the source templates.`，exit 0 |
| targeted-set-v1 基线 | `sed -n '1,20p' test-evidence/targeted-set-v1-baseline.txt` | 13 个契约文件；`stage_base=939766891`；`191 passed`；选择理由与「无超集声明」声明在同文件 |
| 前置门禁（plan 之后） | `pre-analyze-check.py --stage plan`；`decomposition-check.py --mode plan` | plan 阶段 pass（0 error / 47 advisory）、`proceed`（fr_count=20） |

## Requirement Coverage Map

| FR | 承载任务行 | SC | 承载任务行 |
|----|------------|----|------------|
| FR-001 | T004 | SC-001 | T007、T016 |
| FR-002 | T004 | SC-002 | T018、T020、T021 |
| FR-003 | T008、T009 | SC-003 | T016 |
| FR-004 | T010、T011 | SC-004 | T022、T025 |
| FR-005 | T011、T023 | SC-005 | T028 |
| FR-006 | T022、T024、T025 | SC-006 | T018、T021 |
| FR-007 | T019、T020 | — | — |
| FR-008 | T017 | — | — |
| FR-009 | T017、T020 | — | — |
| FR-010 | T017、T020 | — | — |
| FR-011 | T017、T020 | — | — |
| FR-012 | T017 | — | — |
| FR-013 | T017 | — | — |
| FR-014 | T004、T017、T027 | — | — |
| FR-015 | T012、T013 | — | — |
| FR-016 | T013、T014 | — | — |
| FR-017 | T015、T016 | — | — |
| FR-018 | T011、T015、T028 | — | — |
| FR-019 | T012、T015 | — | — |
| FR-020 | T004、T028 | — | — |

**FR-020 implement waiver（不新增 SC）**：FR-020 在本切片无 SC 承接（`## Success Criteria` 只有 SC-001…SC-006，全部先于 FR-020 的加入而定义）。按 implement waiver 处置：**不新增 SC、不重编号**。其可判定面由承载行给出——T004（`## Invocation kinds` 四类分类，C-44 / C-45 / C-46）与 T028（零新增命令与技能，C-47）；C-46 的「setup / house-keeping 子代理派发适用同一有效授权谓词」由 T023 的派发前探针实际执行。waiver 的记账面是 `verification.md`（implement 阶段）：该行记 `FR-020 → waived (no SC)`，MUST NOT 记为空缺。

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结四类对照物（改前测量、名字级测试基线、条款覆盖基线），使后续「零新增」判据全部有对照物。

- [ ] T001 捕获改前基线：创建 `.specify/specs/074a-authorized-routing/notes/pre-change-measurements.md`，逐项贴真实输出与捕获日期——`python3 scripts/python/sync-mirrors.py --check`（六对逐对）、`python3 scripts/python/regen-command-copies.py --check`、`grep -c 'sdd-invocation' src/specify_cli/__init__.py`、`grep -n 'loop depth' shared/definitions/subagent-definitions.md`、`git rev-parse HEAD`、`git status --short`，外加 `.specify/state/` 与 `.specify/memory/` 的当前文件名清单（GATE-7 的对照物）；本行不写任何源文件。
- [ ] T002 [P] 在实现起点按 never-cache 规则重采名字级测试基线：重跑 `.specify/specs/074a-authorized-routing/test-evidence/targeted-set-v1-baseline.txt` 内记录的 13 个契约文件命令，把该文件的 HEAD / 日期 / 命令 / 结果四行更新为本次真实值（该文件是这条 targeted-set-v1 基线的唯一所有者）；失败 nodeid 名单的捕获与比较形式归 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs，本行不复述比较形式，也不改选择理由行。
- [ ] T003 [P] 在实现起点按 never-cache 规则重采条款覆盖基线：`python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/074a-authorized-routing --freeze > .specify/specs/074a-authorized-routing/coverage-baseline.txt`（脚本只打印、不写文件），核对头部含 `frozen-from:` 与 `excluding 074a-authorized-routing`，并确认基线正文**不含**本切片 47 条 `C-N` 名——`--freeze` 排除被核算 spec 本身，本切片条款只能被任务行认领、不能被自己的基线豁免。

**Checkpoint**: 四类分母落盘（镜像/副本、新增存储面、名字级失败名单、条款覆盖）；后续「零新增」判据均有冻结对照物。

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 落词汇 owner 文档的地基三节——控制层级、直接修改定义、四种调用类型。三条用户故事的每一个面都按路径抵达这份文档，因此它先于任何用户故事。

**⚠️ CRITICAL**: 本阶段完成前，任何用户故事行不得开始。

- [ ] T004 落 `shared/definitions/sdd-routing-definitions.md` 的地基三节：开篇声明它是路由规则的唯一 owner 并列出它拥有的四项事实（五项输入的封闭取值域、三值裁决表、固定优先级、理由码词表），`## Hierarchy`（Goal 最高 / Team 编排 Agent 成员 / Agent 执行职责 / SDD 运行是从属执行路径；SDD 运行 MUST NOT 创建、重绑、改范围或终止 Goal、Target、Team、roster），`## Direct modification`（无 SDD 工件链但仍受全部适用质量门与确认门；门禁集合按路径引用 `.specify/shared/guidelines/confirmation-gates.md` 与宪法质量原则，不复述），`## Invocation kinds`（驱动 = SDD 开发流程 / setup 技能 = 框架引导 / house-keeping 技能 = 周期性维护 / 直接修改；无 `.specify/` 结构的目标项目走 setup 路径且 MUST NOT 把 SDD 分流降级为直接修改；setup 与 house-keeping 派发子代理时适用同一有效授权谓词；只有 `sdd-loop-driver` 构成 SDD 调用）。 [green: contracts/hierarchy-and-authorization.md#C-1] [green: contracts/hierarchy-and-authorization.md#C-2] [green: contracts/routing-decision.md#C-17] [green: contracts/bootstrap-and-maintenance.md#C-44] [green: contracts/bootstrap-and-maintenance.md#C-45] [green: contracts/bootstrap-and-maintenance.md#C-46]
- [ ] T005 [blockedBy: T004] 红先编写契约测试到 `tests/contract/test_sdd_routing_definitions.py`：owner 文档开篇声明它拥有四项事实；四项事实在仓库内只有一处落盘（对其余新增面按落盘短语反向计数，命中即 finding）；五项输入各自封闭取值域在场且禁用输入（实现介质 / 扩展名 / 语言 / 工件数 / 作者身份）被写成规则；`## Invocation kinds` 恰四类且 setup / house-keeping 与开发流程区分；每个 `[[STR-NNN]]` 引用解析到 `requirements.md` § Shared Strings 的一行；运行红跑（红形态 = 章节缺失），把命令、真实输出、退出码写入 `.specify/specs/074a-authorized-routing/notes/red-first-evidence.md`。

**Checkpoint**: 词汇 owner 在位，后续三条故事的全部新增面只能按路径抵达它。

---

## Phase 3: User Story 1 - 授权席位启动一次有界嵌套 SDD 运行 (Priority: P1) 🎯 MVP

**Goal**: 定义声明 `sdd-invocation: allowed` 且席位策略允许的成员，在收到一条分流为 SDD 的职责时启动恰好一次嵌套运行，运行止于 review 并交回结构化的 handoff；未满足任一半的成员在派发前被阻断且点名失败的一半。

**Independent Test**: 用夹具团队（一席允许、一席禁止、一席无 `seats` 条目）对两席指派同一条已裁决为 SDD 的职责：允许席启动一次嵌套运行、禁止席在派发前被阻断并点名失败的一半；再由 `test_nested_sdd_invocation.py` 断言入口校验 fail-closed、handoff 字段集封闭、零 merge 零 push。

- [ ] T006 [US1] 建夹具 `tests/fixtures/nested_sdd.py`：在受认可临时根（`.specify/shared/guidelines/temp-directory-discipline.md`）下生成最小 `.specify/` 目标项目——`team.md` frontmatter 含 `seats` 块映射（一席 `[[STR-002]]`、一席 `[[STR-003]]`、一席无条目）、两份 `.agent.md`（一份声明 `[[STR-001]]: [[STR-002]]`、一份缺键）、一个 Goal 带 `open` Target、一条已记录的裁决记录（`data-model.md` E4 字段面，verdict 为 `[[STR-004]]`，使 US1 不依赖 US2 的引擎）。
- [ ] T007 [US1] [blockedBy: T006] 红先编写契约测试到 `tests/contract/test_sdd_authorization.py`：两半 AND 的四种组合；缺键 / 缺 `seats` 映射 / 缺席条目一律解析为 `[[STR-003]]`；流式 `seats` 映射与悬空席条目被拒并点名席位（不回退为 `[[STR-002]]`）；`(team, seat)` 两坐标缺一即拒；拒绝记录点名失败的一半（`agent` / `seat` / `both`）并携带两个来源路径与 seat slug；`--action authorize` 只读零写入、退出码 0（任何裁决，含拒绝；拒绝由 JSON verdict / reason 表达）/ 2（输入错误）分层；运行红跑并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。
- [ ] T008 [US1] [blockedBy: T007] 在 `src/specify_cli/__init__.py` 把 `sdd-invocation` 加入 `NEUTRAL_AGENT_METADATA_KEYS`（封闭值 `[[STR-002]]` / `[[STR-003]]`、缺省 `[[STR-003]]`、`renders_to_tools = False`）与 `NEUTRAL_AGENT_FRAMEWORK_KEYS`，并在同一次改动里把 `tests/contract/test_neutral_metadata_schema.py` 的框架键 frozenset 字面量加恰好一个成员（`feature-ref.md` § 5 ruling 5 声明的唯一 pin 变更）；该键 MUST NOT 出现在任何宿主工具的渲染字段里。 [green: contracts/hierarchy-and-authorization.md#C-3]
- [ ] T009 [US1] [blockedBy: T008] 在 `skills/internal/run-agent/SKILL.md` 的 agent 编写基线里列出新键，值域 / 缺省 / 不渲染三项只作指针指向 `src/specify_cli/__init__.py` 的键集 owner，不复述取值。 [green: contracts/hierarchy-and-authorization.md#C-4]
- [ ] T010 [US1] [blockedBy: T008] 在 `skills/internal/create-team/references/create-mode.md` § Persisted `team.md` schema 增加 `[[STR-010]]` 块映射（按 seat slug 键控、条目内为同一键；块式唯一、流式判畸形、悬空席条目标 dangling、缺省 `[[STR-003]]`、既有团队零回填）。 [green: contracts/hierarchy-and-authorization.md#C-5]
- [ ] T011 [US1] [blockedBy: T008,T010] 新建只读 stdlib 引擎 `scripts/python/sdd-route.py` 并落第一个动作 `--action authorize`：按 `(team, seat)` 解析两半、AND 求值、块式唯一解析、拒绝点名失败的一半并附两个来源路径与 seat slug；零写入、`route` / `golden` 两个动作由 US2 的后续行加入同一文件；本行不手写 `.specify/scripts/python/` 镜像（归 T026）。 [green: contracts/hierarchy-and-authorization.md#C-6] [green: contracts/hierarchy-and-authorization.md#C-7] [green: contracts/hierarchy-and-authorization.md#C-8]
- [ ] T012 [US1] [blockedBy: T011] 红先编写契约测试到 `tests/contract/test_nested_sdd_invocation.py`：六项事实缺一即拒且点名条件（缺 Goal / Target 悬空或关闭或越出绑定 Goal / 终态 Goal / 缺 team 或 seat / scope 越出 territory / 缺裁决或裁决非 `[[STR-004]]`）；运行止于 review 且不进入 merge 步；handoff 字段集封闭（outcome / stages reached / artifact paths / evidence paths / 未决 findings / 异常行 / 集成身份）；三值 outcome；集成身份四事实与被点名的保留 branch；零 merge 零 push（`git log` / `git status` 断言）；卡死 / 超时 / 预算触顶产出 `[[STR-009]]` handoff；缺集成身份的 handoff 不算成功；D-3 的路径引用面（不断言 `## Nested SDD Runs` 标题字面量）；运行红跑并记录。
- [ ] T013 [US1] [blockedBy: T012] 在 `skills/external/sdd-loop-driver/SKILL.md` 增加 § Invoked-from-Team Entry（六项事实、U0 前校验、止于 review）与一条 Hard Requirement（作为一条写线注册到既有 line registry；不 merge、不 push）；独立入口契约逐字不变。 [green: contracts/nested-invocation.md#C-31] [green: contracts/nested-invocation.md#C-32] [green: contracts/nested-invocation.md#C-33]
- [ ] T014 [US1] [blockedBy: T013] 新建 `skills/external/sdd-loop-driver/references/nested-invocation.md` 的 § Entry validation table 与 § Handoff schema：字段集封闭、三值 outcome、集成身份四事实与被点名的保留 branch、零 merge 零 push 的越权判据。 [green: contracts/nested-invocation.md#C-34] [green: contracts/nested-invocation.md#C-35] [green: contracts/nested-invocation.md#C-36] [green: contracts/nested-invocation.md#C-37]
- [ ] T015 [US1] [blockedBy: T014] 同一参考文档补 § Line registration（复用 Feature 064 的 line registry 与 worktree-per-write-line，领域重叠串行或拒绝，MUST NOT 新建第二套机制）、§ Failure and stall handoff（停止、持久化既有状态脊、`[[STR-009]]` handoff 四要素、外层失败隔离与上报）、§ Consumer duty（调用方结果原样或按稳定路径携带 handoff；`[[STR-008]]` / `[[STR-009]]` MUST NOT 报成功）。 [green: contracts/nested-invocation.md#C-38] [green: contracts/nested-invocation.md#C-39] [green: contracts/nested-invocation.md#C-40]
- [ ] T016 [US1] [blockedBy: T015] US1 转绿与取证：`python3 -m pytest -q tests/contract/test_sdd_authorization.py tests/contract/test_nested_sdd_invocation.py` 跑到全绿并把绿证据追加 `notes/red-first-evidence.md`；把两席夹具结果（允许席启动一次嵌套运行 / 禁止席派发前被阻断且点名失败的一半）、止于 review、零 merge 零 push 的真实输出贴入 `notes/quickstart-run.md` 的 S4 / S5 小节。 [green: contracts/nested-invocation.md#C-41] [green: contracts/nested-invocation.md#C-42]

**Checkpoint**: US1 独立可验收——两半授权可复算、拒绝点名失败的一半、入口校验 fail-closed、handoff 字段集封闭且止于 review；MVP 第一半就位。

---

## Phase 4: User Story 2 - 确定性分流把 SDD 与直接修改分开 (Priority: P1) 🎯 MVP

**Goal**: 写入前按声明输入得到 sdd / direct / adjudicate 三值裁决，由同一个确定性引擎产生，携带输入与理由码，且在变更属功能规模、跨切面、不可逆、需可追溯或 Complex/High-stakes 时绝不返回 direct。

**Independent Test**: 把黄金表（feature / maintenance / cross-cutting / irreversible / ambiguous / conflicting / 有界定义修正）喂给 `--action golden`，逐行断言文档化裁决与理由码；同一输入求值两次返回逐字节相同的输出。

- [ ] T017 [US2] [blockedBy: T005] 在 `shared/definitions/sdd-routing-definitions.md` 落路由正文：五项声明输入的封闭取值域与禁用输入（`change_nature` 的域含 `definition-class`，其成员资格由目标路径谓词派生，谓词清单归 `requirements.md` FR-008 且不新增第六输入）、复杂度层级引用 `.specify/shared/guidelines/task-complexity-rubric.md` 作 owner 且不复述其信号与表、definition-class 默认 cross-cutting 与「有界修正」独立取值 + 非空理由、`[[STR-004]]` 的命中条件、`[[STR-005]]` 的全部条件、固定优先级 `[[STR-006]] > [[STR-004]] > [[STR-005]]`、冲突集的封闭枚举与多条件命中的取码次序、用户显式指示覆盖并记为裁定（含被覆盖的裁决与 FR-011 理由码）、每成员职责一次并复用至输入变化（输入变化即重判、旧裁决保留）、裁决记录载体（本切片 = Agent 执行证据；handoff 与调用方结果按稳定路径引用同一条记录，不复算）。 [green: contracts/routing-decision.md#C-18] [green: contracts/routing-decision.md#C-19] [green: contracts/routing-decision.md#C-20] [green: contracts/routing-decision.md#C-21] [green: contracts/routing-decision.md#C-22] [green: contracts/routing-decision.md#C-23] [green: contracts/routing-decision.md#C-24] [green: contracts/routing-decision.md#C-25] [green: contracts/routing-decision.md#C-26] [green: contracts/routing-decision.md#C-27]
- [ ] T018 [US2] [blockedBy: T017] 红先编写契约测试到 `tests/contract/test_sdd_routing_engine.py`：同输入同输出（确定性）、优先级次序、理由码取码次序（多条件命中时按 owner 声明次序取首条且携带全部命中条件）、退出码阶梯（产出裁决即 exit 0，含 `[[STR-006]]`；输入错误 exit 2）、零写入与 stdlib-only、引擎不自带第二份取值域 / 裁决表 / 优先级 / 理由码；运行红跑并记录。
- [ ] T019 [US2] [blockedBy: T018] 在 `scripts/python/sdd-route.py` 加入 `--action route` 与 `--action golden`：运行时解析 owner 文档取值（MUST NOT 自带第二份四项事实）、`route` 产出裁决即 exit 0（含 `[[STR-006]]`）、输入错误 exit 2、`golden` 解析并判定表内每一行；`--action authorize` 的既有行为零改动。 [green: contracts/routing-decision.md#C-28]
- [ ] T020 [US2] [blockedBy: T019] 在 owner 文档落 § Golden case table（Markdown 表：case id / 五项输入 / 期望裁决 / 期望理由码 / 覆盖的需求面；至少覆盖 feature-scale、bounded maintenance、cross-cutting、irreversible、ambiguous、conflicting 与满足其余全部条件的有界定义修正七类），并连跑两次 `--action golden` 证明逐行裁决与理由码一致；行集唯一落点在该表，测试代码与独立数据文件 MUST NOT 复制行。 [green: contracts/routing-decision.md#C-29]
- [ ] T021 [US2] [blockedBy: T020] US2 转绿与取证：`python3 -m pytest -q tests/contract/test_sdd_routing_definitions.py tests/contract/test_sdd_routing_engine.py` 跑到全绿；`python3 scripts/python/sdd-route.py --action golden --format json` 两次输出逐字节一致，并把两段真实输出与逐行核对贴入 `notes/quickstart-run.md` 的 S1 / S2 / S3 小节；同时复核 ambiguous 与 conflicting 行返回 `[[STR-006]]` 而非 `[[STR-005]]`。

**Checkpoint**: US2 独立可验收——三值裁决可复算、黄金表逐行可判定、重复求值一致、绝不静默默认 direct；MVP 第二半就位。

---

## Phase 5: User Story 3 - 嵌套被治理，而不是被逃脱 (Priority: P2)

**Goal**: 把既有反嵌套义务收窄为一个可判定谓词——只有同时满足三条件的派发才能点名驱动；阶段执行者仍是叶子、SDD 之内不得再有 SDD、virtual 成员不得承载；其余一切派发保持原禁令。

**Independent Test**: 对四种派发形态跑派发前治理探针（授权 SDD 指派 / 未授权提示词点名驱动 / 阶段执行者尝试加载驱动 / 阶段内的嵌套 SDD 尝试），只有第一种被派发，其余三种在离开前被阻断并点名失败条件。

- [ ] T022 [US3] [blockedBy: T016] 红先编写契约测试到 `tests/contract/test_sdd_invocation_governance.py`：四种派发形态（授权 SDD 指派放行并记录授权依据 / 未满足两半的提示词点名驱动 → 派发前阻断并点名条件 / 阶段执行者尝试加载驱动 → 拒绝并报异常 / 阶段内的嵌套 SDD 尝试 → 拒绝）；virtual 模态承载被拒；深度 2 链（团队编排者 → 成员 driver host → 阶段执行者叶子）；既有反嵌套契约用例在非授权路径上保持绿；运行红跑并记录。
- [ ] T023 [US3] [blockedBy: T022] 就地把反嵌套义务收窄为可判定谓词：在 `shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation 把 `:104` 的「loop depth 恒为 1」句改写为三条件谓词（收件 Agent 定义声明 `[[STR-002]]` ∧ 其席位策略声明 `[[STR-002]]` ∧ 指派任务是 SDD 指派，其中 SDD 指派按 `requirements.md` FR-005 的定义 = 已记录裁决为 `[[STR-004]]` 的成员职责；不满足三者的一切派发保持原禁令逐字不变），并让 `skills/internal/run-agent/SKILL.md` 的派发前探针改调 `python3 scripts/python/sdd-route.py --action authorize` 后 fail-closed（改写提示词无法修好一次拒绝）。 [green: contracts/hierarchy-and-authorization.md#C-9] [green: contracts/hierarchy-and-authorization.md#C-10]
- [ ] T024 [US3] [blockedBy: T023] 在同一 owner 位点同一趟声明深度 2 链、virtual 模态禁令与每成员一运行的硬上限（无可声明的更高上限；第二个并发职责由既有 line 机制串行化或拒绝，不新增并发原语），并把拒绝记录收紧为「点名失败条件 + 收件方解析值 + 两个来源路径 + seat slug」，MUST NOT 只写「未授权」。 [green: contracts/hierarchy-and-authorization.md#C-11] [green: contracts/hierarchy-and-authorization.md#C-12] [green: contracts/hierarchy-and-authorization.md#C-13] [green: contracts/hierarchy-and-authorization.md#C-14]
- [ ] T025 [US3] [blockedBy: T024] US3 转绿与取证：`python3 -m pytest -q tests/contract/test_sdd_invocation_governance.py` 全绿；既有反嵌套用例逐条仍绿（按 T002 基线名集核对）；结构面复核授权面未新增确认门 / 调度器 / 第二 registry；把阶段执行者与未合格提示词的阻断记录（含点名条件）贴入 `notes/quickstart-run.md` 的 governance 小节（quickstart 无该场景，不复用 S6）。 [green: contracts/hierarchy-and-authorization.md#C-15] [green: contracts/hierarchy-and-authorization.md#C-16]

**Checkpoint**: US3 独立可验收——四种派发形态只有授权 SDD 指派被放行，其余路径的原禁令逐字保留且可点名失败条件。

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 收口镜像、单一 owner、结构面、回归与登记。

- [ ] T026 镜像同步与逐对核验：`python3 scripts/python/sync-mirrors.py --write --only shared --only skills --only scripts` 后 `python3 scripts/python/sync-mirrors.py --check`（相对 T001 基线零新增差异），并用 `cmp` 逐对核对 7 个源文件与各自 `.specify/` 投影同字节——`shared/definitions/sdd-routing-definitions.md`、`shared/definitions/subagent-definitions.md`、`skills/internal/run-agent/SKILL.md`、`skills/internal/create-team/references/create-mode.md`、`skills/external/sdd-loop-driver/SKILL.md`、`skills/external/sdd-loop-driver/references/nested-invocation.md`、`scripts/python/sdd-route.py`；`python3 scripts/python/regen-command-copies.py --check` 仍 `OK`（证明命令模板零改动）；禁止手改镜像。
- [ ] T027 单一 owner 审计：按落盘短语反向计数，确认五项输入取值域、三值裁决表、固定优先级与理由码词表在 `shared/definitions/sdd-routing-definitions.md` 之外零副本（探针、驱动入口、执行证据记录形状一律按路径抵达）；把命令与真实输出写入 `notes/quickstart-run.md` 的 single-owner 小节。 [green: contracts/routing-decision.md#C-30]
- [ ] T028 结构面复核（与 T027 共用同一证据落点，故按行序串行）：(a) 零新增 `/speckit.*` 命令与零新增技能——`ls templates/commands/*.md | wc -l` 与 `ls -d skills/external/*/ | wc -l`、`ls -d skills/internal/*/ | wc -l` 相对 T001 基线不变；(b) 零新增 registry / ledger / 状态脊 / ownership 模型 / 集成队列——`.specify/state/`、既有 line registry 目录与 `.specify/memory/` 的文件名集合相对 T001 基线 `comm -13` 为空，嵌套运行的记录解析到既有 line 条目与既有状态脊；把命令与输出贴入 `notes/quickstart-run.md` 的 structure 小节。 [green: contracts/nested-invocation.md#C-43] [green: contracts/bootstrap-and-maintenance.md#C-47]
- [ ] T029 [blockedBy: T026] 定向回归与分类诚实性审计面：重跑 `test-evidence/targeted-set-v1-baseline.txt` 的 13 个既有契约文件 + 5 个新测试文件（`python3 -m pytest -q …`），把既有 13 文件的失败 nodeid 排序后与 T002 重采名单做 `comm -13`（MUST 为空，判据是名字级不是条数级），5 个新文件 MUST 全绿；同趟落审计职责——`/speckit.review` 是本切片的分类诚实性审计面（复核每条已声明输入的分类、记录不一致；嵌套运行另加驱动 U4 独立校验），引擎的确定性只覆盖声明输入，故审计结论记入 review 证据而不回写裁决；结果与命令追加 `notes/pre-change-measurements.md` 的回归小节。
- [ ] T030 [blockedBy: T029] 快速走查取证：按 `quickstart.md` 的 S1–S7 逐条执行（S1 route feature-scale / S2 bounded maintenance / S3 missing input / S4 effective authorization / S5 nested run + handoff / S6 acceptance evidence / S7 三项基线在实现起点重测），把每条命令、真实输出、退出码写入 `notes/quickstart-run.md`；无法执行的场景记 `not-evaluated` + reason，不记达成。
- [ ] T031 [blockedBy: T030] SC 证据与登记收口：把 SC-001…SC-006 的状态（只从 `.specify/templates/verification-log-template.md` 的封闭词表取值）、命令、输出摘要与证据指针逐条写入 `.specify/specs/074a-authorized-routing/verification.md`，并逐条声明本趟的 `PLAN-EDIT:`（若有）；同步 `.specify/memory/features/074.md` 的切片行与 `.specify/memory/features.md` 的 074 行 Last Updated（状态列保持 `Planned`；`Implemented` 转移按 `.specify/shared/workflow/feature-integration.md` 判定，不在本行擅自推进）。
- [ ] T032 [blockedBy: T031] 终局门禁复跑：依次跑 `python3 .specify/scripts/python/validate-tasks.py .specify/specs/074a-authorized-routing/tasks.md`（0 error / 0 warning）、`python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/074a-authorized-routing --stage tasks --repo .`（errors=0，advisory 逐条裁定）、`python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/074a-authorized-routing/requirements.md --tasks .specify/specs/074a-authorized-routing/tasks.md`（`proceed`）、`python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/074a-authorized-routing`（claimed = 47 / FR 20 / uncovered beyond baseline = 0），把四段真实输出贴入 `verification.md` 的 gates 小节；若发现与冻结清单的结构漂移，按 rerun 契约追加新行而不重编号。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，可立即开始；T002 / T003 互为 `[P]`。
- **Foundational (Phase 2)**: 依赖 Setup（T001 的落点目录就位）；**阻塞三条用户故事**——T004 是词汇 owner，T005 是它的红先形状测试。
- **User Stories (Phase 3–5)**: US1 依赖 T005；US2 依赖 T005；US3 依赖 T016（治理谓词调用 US1 落下的 `--action authorize`）。
- **Polish (Phase 6)**: 依赖全部用户故事完成。

### User Story Dependencies

- **US1 (P1)**: 依赖 Foundational；不依赖 US2——入口校验消费「一条已记录的裁决」（夹具按 `data-model.md` E4 字段面自带），故两个 P1 故事各自独立可测。
- **US2 (P1)**: 依赖 Foundational；不与 US1 共享写目标（唯一同文件面是 `scripts/python/sdd-route.py` 的三个动作，按 `--action` 分区，T011 → T019 串行）。
- **US3 (P2)**: 依赖 US1 的 `--action authorize`（T011）与 US1 绿点（T016）；与 US2 无写目标重叠。

### Within Each User Story

- 红先测试先写并跑红（命令 + 真实输出 + 退出码入 `notes/red-first-evidence.md`）→ 再实现 → 再转绿取证。
- 一个条款只由一个行认领；同一契约内认领顺序单调递增（T004 起，逐行只前进不后退）。
- 同一文件的多行（`shared/definitions/sdd-routing-definitions.md`：T004 / T017 / T020；`scripts/python/sdd-route.py`：T011 / T019；`skills/internal/run-agent/SKILL.md`：T009 / T023；`skills/external/sdd-loop-driver/references/nested-invocation.md`：T014 / T015）按行序串行，不加 `[P]`。

### Parallel Opportunities

- Phase 1：T002 与 T003 可并行（写目标不同：`test-evidence/targeted-set-v1-baseline.txt` 与 `coverage-baseline.txt`）。
- 其余阶段零 `[P]`：红先行共用 `notes/red-first-evidence.md` 这一追加落点，T027 与 T028 共用 `notes/quickstart-run.md` 这一追加落点，T026 逐对核对时点名全部源文件——同一文件即同写目标，按行序串行。

## Parallel Example: Phase 1

```bash
# 两条互不写同一文件的基线重采行可同时启动：
Task: "名字级测试基线重采（T002）"
Task: "条款覆盖基线重采（T003）"
```

---

## Implementation Strategy

### MVP First

**MVP scope rule**: MVP = 全部同为 P1 的用户故事，即 **US1 + US2**。只有分流裁决而无「授权席位启动嵌套运行」时无法独立演示层级统一（另一半是两条互不相连的流程）；只有嵌套运行而无确定性裁决时无法判定何时该走 SDD。US3 是使该能力**安全**的收窄，独立于 MVP 交付但必须在收口前完成。

1. Phase 1 Setup（冻结四类分母）
2. Phase 2 Foundational（词汇 owner，阻塞全部故事）
3. US1 → 按 Checkpoint 独立验收
4. US2 → 按 Checkpoint 独立验收（MVP 完成，可演示）
5. US3 → 按 Checkpoint 独立验收
6. Phase 6 Polish（镜像、单一 owner、结构面、回归、SC 证据、登记）

### Incremental Delivery

1. Setup + Foundational → 词汇口径统一，后续每个新增面都只按路径抵达它
2. US1 → 授权席位可启动并交回一次有界嵌套运行
3. US2 → 何时走 SDD 变成可判定、可复算的裁决
4. US3 → 嵌套被收窄到可判定谓词，其余路径的原禁令逐字保留
5. Polish → 零漂移、零新增存储面、SC 证据齐备

---

## Notes

- **plan_constraint（active since 2026-10-29T02:44Z，plan_commit = 8f991f375）**: 本切片的 plan-owned 面（`plan.md` / `data-model.md` / `contracts/**` / `quickstart.md` / `research.md` / `feature-ref.md`）只接受行级小修，逐项在 `verification.md` 声明 `PLAN-EDIT: <path> — <理由>；分类=minor`；实质性改动停线回抛，不静默重写。父设计 `.specify/specs/074-goal-team-sdd-unification/**` 全程只读。
- **测试预算**: 本切片使用 targeted-set-v1（`stage_base=tasks`）；全量 baseline / closure 两个槽位归 implement 与 review 阶段，本文件不预占。
- **陷阱形复核**: 「新增存储面为零」的计量单位是**文件名集合**（`comm -13`），不是行数或目录数；「`sdd-invocation` 已落盘处数」的计量单位是代码 owner 文件，不是全仓 grep 命中（设计文档里的说明文字是引用，不是定义）。
- **不复述面**: 五项输入取值域 / 三值裁决表 / 固定优先级 / 理由码词表 / 复杂度层级信号 / 门禁集合 / 阶段名册 一律按路径抵达各自 owner，本文件与任何实现面 MUST NOT 复述。
- **零越界面**: 本切片不实现 074b 承接的父 `FR 020`–`FR 024`、`FR 026`–`FR 028` 面，不断言 `## Nested SDD Runs` 标题字面量（D-3），不新增 `templates/commands/**` 改动。
