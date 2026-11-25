# Tasks: Background Dispatch Settlement — 后台派发静默退出结算契约

**Requirement ID**: 106
**Requirement Key**: `106-background-silent-failure`
**Related Feature**: 095 Super Agent Role（`.specify/features.md` 行 106；本阶段维持 `Planned`，无状态迁移权）
**Input**: Design documents from `.specify/specs/106-background-silent-failure/`
**Prerequisites**: plan.md（结构 / Mirror Obligations / Execution Premises / Decision Tensions T-001…T-003）、requirements.md（41 FR / 9 SC / 4 STR / A-1…A-18）、research.md（B-01…B-14 / R-01…R-08）、data-model.md（E1–E9 / INV01…INV12）、contracts/ ×3（34 条款：C-01…C-12 / C-13…C-24 / C-25…C-34）、quickstart.md（S-0…S-7）、feature-ref.md（35 项交付面；单元注册裁决 = 无新单元）

**Tests Mode**: ON（Constitution Principle IV "Test-First & Contract-Driven Implementation" 是测试强制原则；本特性交付 owner 文本、引擎动作、载体证据与契约测试，测试形态为 contract 模块与确定性夹具。新行为测试红先；两处守既有行为的回归守卫按 migration/regression 例外置于实现之后并在行内声明：T023 的保留面守卫在实现完成后转绿，T028 的 version/legacy 守卫在 T029 落地 `legacy` 标注前保持红。）

**Tests**: 红先证据的唯一落点是 `.specify/specs/106-background-silent-failure/notes/red-first-evidence.md`（每条：命令、真实输出、退出码）；失败 nodeid 名集的捕获与比较形式归 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs，本文件只给路径与命令。测试唯一入口是 `scripts/bash/run-tests.sh`；interpreter 固定在 § Environment Prerequisites，任务行不写解释器级测试命令。

**Organization**: 按用户故事组织——US1（可区分的结算值与只读判定面，P1）、US2（全部后台载体证据一致且只有一套契约，P1）、US3（静默结束后的显式反应，P2）、US4（静默终止能让检查转红，P2）、US5（升级加性与旧记录 legacy 标注，P3）。US1 + US2 同为 P1 且互为 MVP 前提：只有结算值而没有载体证据，判定面没有输入；只有载体证据而没有结算值，证据无法收敛为结论——两者检查点各自独立可测，合起来构成可演示的最小增量。Foundational 承载所有故事的唯一前提：结算契约 owner 章节。

## Definition of Done (DoD)

- DoD-1: 全部任务行为 `[X]`；若出现 `[~]`，其理由逐条记录在 `.specify/specs/106-background-silent-failure/verification.md` 的 `deferred_tasks=`。
- DoD-2: 交付面 = 1 处 owner 章节修订（§ Termination，含 § Role Edges 指针句）+ 1 个引擎加性动作（`--action settle`）+ 1 个载体脚本加性证据（`.attempt` / `.end` + trap/pid）+ 5 处技能/报告文本 + 1 处执行模式文本 + 1 处配方文本 + 2 个命令模板与 4 个 coordinator 模板的指针行 + 3 个既有文档页 + 6 个新测试模块 + 1 个夹具树 + 镜像/副本再生成；零新增第三方依赖、零新增调度器/注册表/队列/存储/通知通道/child list。
- DoD-3: 契约覆盖如实记账——3 份契约共 34 条款，每条恰好被一行 `[green:]` 认领一次（C-01…C-07→T002、C-08…C-12→T003、C-13→T007、C-14→T010、C-15→T011、C-16→T012、C-17→T013、C-18→T014、C-19/C-20→T015、C-21→T016、C-22→T017、C-23→T023、C-24→T026、C-25…C-28→T007、C-29→T008、C-30→T025、C-31/C-32→T027、C-33→T029、C-34→T032）；认领行序与条款序号单调一致，零 green-cross-phase / green-clause-collision / green-path-divergence WARN；行为类条款（C-34 列举的集合）只以文本 + 评审/变异演练举证，不冒充机器覆盖；FR 覆盖 41/41 以 § Requirement Coverage Map 为权威，会计器 `fr-uncovered` 车道的 37/41 如实报告（FR-036 / FR-037 / FR-039 / FR-040 不被任何契约条款引用），不作通过判据。
- DoD-4: 6 个测试模块与 `tests/fixtures/settlement/` 全绿并经唯一入口运行；同一夹具两次运行的结算判定差异为 0；新增测试零固定 `sleep`；两槽位预算不变（未新增第三个全量槽位）。
- DoD-5: 镜像与副本 — plan.md § Mirror Obligations 逐行落地；`sync-mirrors.py --check` 的漂移成员集相对基线无新增成员（触及 scope 逐字节一致）；`regen-command-copies.py --check` exit 0；零手改镜像 / 副本。
- DoD-6: 保留面空差异 — watcher 判定 token 集 / 退出码集 / 哨兵字面量集与 `fbab7a45c` 基线逐成员相等；`--self-test` 39 passed / 0 failed；五要素上行与七字段下行文本不变；既有 `.status` 行格式可被基线读取器读回；确认纪律冻结 total 的 `31 != 27` 红是 EP-005 的既有事实，按「触及文件零新增命中」度量，不声称 `== 27` 绿。
- DoD-7: 行为类义务如实分类（C-34 集合）经评审/变异演练举证；四个变异演练各至少一条测试转红并留证在 `test-evidence/mutation-drill.md`；演练未转红即记守卫缺陷，不软化。
- DoD-8: `verification.md` 逐条记录 SC-001…SC-009 的状态、命令与证据指针；`final` 路径的 SC-001 / SC-002 / SC-004 记 `pass` 并带 smoke 记录。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/106-background-silent-failure/tasks.md` exit 0（0 error；WARN 逐条裁定并记录）。
- GATE-2: 跨产物一致 — check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/106-background-silent-failure --stage tasks --repo .` 输出 `decision=pass` 且 errors=0（advisory 逐条裁定；新增测试模块与夹具树的 missing-path advisory 属预期）。
- GATE-3: 条款与 FR 覆盖 — check: `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/106-background-silent-failure` 报 `claimed clauses 34` 且 `clause-uncovered` 的 beyond-baseline 为 0；FR 覆盖的权威判据是本文件 § Requirement Coverage Map（41/41）与 pre-analyze `runtime-stack-row` errors=0；会计器的 `fr-uncovered` 车道如实报告 37/41（FR-036 / FR-037 / FR-039 / FR-040 未被三份契约的任何条款引用——契约集的既有结构事实；plan-owned 契约不改写），不作通过判据。
- GATE-4: final-path 成功判据 + smoke 记录 — check: `verification.md` 中 SC-001 / SC-002 / SC-004 全部 `pass`，且 `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`（存在且非空）齐备（条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates）。
- GATE-5: 全量套件零新增失败 — check: implement 入口既有的全量槽位以 `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh --names-out <failed-list-file>` 运行，失败名集相对 implement 入口基线做 `comm -13` 为空（既有红逐条点名；不新增第三个槽位）。
- GATE-6: 镜像与副本干净 — check: `python3 scripts/python/sync-mirrors.py --check` 的漂移成员集相对基线无新增成员；`python3 scripts/python/regen-command-copies.py --check` exit 0；触及镜像对 `cmp` 空输出。
- GATE-7: 保留面集合相等 — check: `bash scripts/bash/run-tests.sh tests/contract/test_settlement_preservation.py -q` exit 0（watcher 三集合相等、`--self-test` 39/0、gate per-file 命中集）。
- GATE-8: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/106-background-silent-failure/tasks.md` 返回 0。

## Environment Prerequisites

- CPython: **available** — probe: `/usr/local/bin/python3 --version` → `Python 3.11.11` @ 2026-11-25；约束：全部测试行 MUST 以 `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh …` 经唯一入口执行（仓库 `.venv` 不带 pytest）；affected: 全部测试与引擎行。
- pytest / typer: **available** — probe: `/usr/local/bin/python3 -m pytest --version` → `pytest 8.4.2`；`/usr/local/bin/python3 -c "import typer; print(typer.__version__)"` → `0.19.2` @ 2026-11-25；affected: 全部测试行、`regen-command-copies.py`。
- bash / git: **available** — probe: `bash --version` → `4.4.20(1)-release`；`git --version` → `2.43.5` @ 2026-11-25；affected: 测试入口、镜像与证据行。
- 容器运行时 / 镜像仓库 / 活集群 / 外网: **none** — 本特性全部检查为本地文件、`git` 与本地 pytest，无构建、无拉取、无网络、无守护进程 @ 2026-11-25；affected: none。

**A13 boundary**（owner: `shared/workflow/acceptance-hardening.md` § Gates — 本注为指针，不是第二份规则）：本节只记录任务生成时的探针结论（探针命令 + ISO 日期）。计划期承重前提归 plan.md § Execution Premises；来自依赖特性的记录归 plan.md § Inherited Blockers。同一事实写进两个载体即缺陷，第二次出现 MUST 改为指针。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标不同、无未完成依赖）。本文件的 `[P]` 只出现在写目标逐行不同的行：US1 的 T005，US2 的 T012 / T013 / T014。其余行共享 `notes/red-first-evidence.md` 这一追加 sink 或同一文件按行序串行，故零 `[P]`。
- **[Story]**: 用户故事标签（`[US1]`…`[US5]`），只出现在用户故事阶段的任务行；Setup / Foundational / Polish 阶段零 `[US` 标记。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全部 `[X]` 前不得开始本行。仅阶段顺序关系时不写。
- **[green: <contract>#<clause>]**: 绿点认领；一份契约的条款序必须与认领行序单调一致，且每条只被认领一次。本文件 34 条各被认领一次（分区表见 § Contract Clause → Task Map）。
- 每行必须单行完成（含文件路径与全部标签），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `verification.md` 的 `deferred_tasks=`）。

## Path Conventions

- **框架源（编辑面）**: `shared/`、`skills/`、`scripts/`、`templates/`、`agents/`、`docs/`。
- **生成面（MUST NOT 手改）**: `.specify/shared/**`、`.specify/skills/**`、`.specify/scripts/**`、`.specify/agents/templates/**`（由 `sync-mirrors.py` 投影）；`.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/`（由 `regen-command-copies.py` 生成）。
- **证据落点（本特性）**: `.specify/specs/106-background-silent-failure/` 下的 `notes/pre-change-measurements.md`、`notes/red-first-evidence.md`、`notes/quickstart-run.md`、`coverage-baseline.txt`（已冻结）、`test-evidence/mutation-drill.md`、`test-evidence/reaction-drill.md`、`test-evidence/enforcement-honesty.md`、`test-evidence/acceptance-106.md`、`test-evidence/non-goals-audit.md`、`verification.md`。
- **只读面（零修改）**: `skills/external/sdd-loop-driver/scripts/watch-target.sh`、`skills/external/sdd-loop-driver/scripts/stage-runner.sh`、`scripts/python/exec-quant.py`、`scripts/python/sync-mirrors.py`、`scripts/python/regen-command-copies.py`、`scripts/python/scan-confirmation-gates.py`、`docs/reference/history/**`。
- **plan-owned 面（spec 侧所有；crew 不可写）**: `plan.md`、`data-model.md`、`contracts/`、`quickstart.md`、`research.md`、`feature-ref.md` —— 只有 spec 侧（驱动者 / analyze-repair）修订；crew 的 forbidden 领土（`handoff.md` § Territory、`team.md` territory.forbidden）覆盖这些路径，二者冲突时以领土契约为准。

## Measured Premises (re-measured at generation time 2026-11-25, HEAD `1f06dceaf`)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 需求条目计数（FR / SC / STR） | `grep -cE '^\- \*\*FR-[0-9]+\*\*:' .specify/specs/106-background-silent-failure/requirements.md`；同法 `SC-`；`grep -cE '^\| \`STR-[0-9]+\`' …/requirements.md` | FR **41** / SC **9** / STR **4**。**陷阱形**：`grep -c 'FR-'` 得 **54**、`grep -c 'SC-'` 得 **22**（正文引用被一并算入）；计量单位是条目定义行 |
| 契约条款数与形式 | `/usr/local/bin/python3 .specify/scripts/python/clause_extract.py .specify/specs/106-background-silent-failure/contracts/*.md` | 三份均 `form=md-bold-closed`；settlement **12**（C-01…C-12）/ carrier **12**（C-13…C-24）/ enforcement **10**（C-25…C-34），合计 **34**。**陷阱形**：`grep -c 'C-'` 得 13 / 13 / 14（正文引用），定义行 `grep -cE '^\*\*C-[0-9]+'` 才是 12 |
| Plan 集计数 | `grep -c '^## S-' …/quickstart.md`；`grep -cE '^## E[0-9]' …/data-model.md`；`grep -cE '^\- \*\*INV[0-9]+' …/data-model.md`；`grep -cE '^[0-9]+\. \`' …/feature-ref.md` | quickstart 场景 **8**（S-0…S-7）；实体 **9**（E1–E9）；不变量 **12**（INV01…INV12）；交付面 **35** |
| 目标文件在位 | 逐个 `test -e`（18 个编辑目标：3 shared + 1 engine + 5 skills + 2 command templates + 4 coordinator agents + 3 docs） | **18/18 OK** |
| 新测试模块与夹具树当前状态 | 逐个 `test -e`（6 个 `test_settlement_*` 模块 + `tests/fixtures/settlement/`） | **7/7 ABSENT**（红先前件） |
| C2 载体现状 | `grep -c "trap " …/dispatch.sh`；`grep -c "pid_start_ticks\|\.attempt\|\.end" …/dispatch.sh`；`grep -nF 'tee "${LOG_DIR}/${LABEL}.status"' …/dispatch.sh` | trap **0**；attempt/end **0**；`.status` 只在 **150 行**末写一次（无 pid、无心跳） |
| C3 报告现状 | `grep -n 'label\` \| \`role\` \| \`dispatch_duty\` \| \`workspace\` \| \`parent\`' …/create-team/SKILL.md` | **第 85 行** 5 列头（需加性扩为 7 列，5 列仍需可解析） |
| 引擎动作闭集 | `grep -n 'choices=("report", "query")' scripts/python/role-edge-check.py` | **第 961 行** `choices=("report", "query")`；写入 `settle` 前 MUST 保持 `report` / `query` 输出逐字节不变 |
| 保留面基线 | 只读 `skills/external/sdd-loop-driver/scripts/watch-target.sh` 的 `sha256sum` 与 `--self-test` | sha256 `955ddf7820a80cb3afad5af25877f2f8d7093e4fb08c46ec59dfe948ec3f2479`（= `fbab7a45c`）；`SELF-TEST: 39 passed, 0 failed` |
| 镜像 / 副本基线 | `.venv/bin/python scripts/python/sync-mirrors.py --check`；`.venv/bin/python scripts/python/regen-command-copies.py --check` | sync rc **0**（六对 ok，`shared/` 116 files byte-identical）；regen rc **0**（`OK: all per-tool command copies match the source templates.`） |
| 确认门冻结 total | `python3 scripts/python/scan-confirmation-gates.py --root . --json` | **total 31**（EP-005：`== 27` 的相等判定在基线已红，本特性按「触及文件零新增命中」度量） |
| Feature 注册行 | 解析 `.specify/features.md` 行 106 的 Status 单元格 | **Planned**（本阶段无状态迁移权） |
| 环境 | 见 § Environment Prerequisites | Python 3.11.11 / pytest 8.4.2 / typer 0.19.2 / bash 4.4.20 / git 2.43.5 @ 2026-11-25 |

## Requirement Coverage Map

| FR | 承载任务行 | FR | 承载任务行 |
|----|------------|----|------------|
| FR-001 | T002、T006、T007、T008 | FR-022 | T016、T026 |
| FR-002 | T002、T006、T007 | FR-023 | T003、T019、T020、T021 |
| FR-003 | T002、T006、T007 | FR-024 | T003、T019、T020、T021 |
| FR-004 | T002、T006、T007 | FR-025 | T003、T019、T020 |
| FR-005 | T002、T006、T007、T024 | FR-026 | T003、T007、T019、T020 |
| FR-006 | T002、T006、T007、T024、T027 | FR-027 | T002、T019、T020 |
| FR-007 | T002、T006、T007、T028 | FR-028 | T004、T006、T007、T008 |
| FR-008 | T003、T006、T007 | FR-029 | T006、T007、T025 |
| FR-009 | T002、T007、T020 | FR-030 | T025 |
| FR-010 | T002、T007、T010、T013 | FR-031 | T009、T024、T027 |
| FR-011 | T002、T019 | FR-032 | T009、T024、T027 |
| FR-012 | T017、T026 | FR-033 | T023、T027 |
| FR-013 | T004、T017、T026 | FR-034 | T003、T028、T029 |
| FR-014 | T007、T008、T023 | FR-035 | T028、T029 |
| FR-015 | T009、T010 | FR-036 | T031 |
| FR-016 | T007、T009、T011 | FR-037 | T030 |
| FR-017 | T009、T012、T018 | FR-038 | T026、T036 |
| FR-018 | T009、T013 | FR-039 | T023、T036 |
| FR-019 | T009、T014 | FR-040 | T036 |
| FR-020 | T009、T015、T026 | FR-041 | T026、T032、T036 |
| FR-021 | T009、T015 | | |

| SC | 承载任务行 | Path |
|----|------------|------|
| SC-001 | T005、T009、T011、T024、T027 | final |
| SC-002 | T006、T007、T017、T027 | final |
| SC-003 | T023 | supporting |
| SC-004 | T021、T022 | final |
| SC-005 | T009、T024、T027 | supporting |
| SC-006 | T028、T029、T031、T032 | supporting |
| SC-007 | T006、T023、T024、T037 | supporting |
| SC-008 | T024、T027 | supporting |
| SC-009 | T023、T036 | supporting |

## Contract Clause → Task Map (34/34 claimed once)

| Clause | Row | Clause | Row | Clause | Row |
|--------|-----|--------|-----|--------|-----|
| C-01 | T002 | C-13 | T007 | C-25 | T007 |
| C-02 | T002 | C-14 | T010 | C-26 | T007 |
| C-03 | T002 | C-15 | T011 | C-27 | T007 |
| C-04 | T002 | C-16 | T012 | C-28 | T007 |
| C-05 | T002 | C-17 | T013 | C-29 | T008 |
| C-06 | T002 | C-18 | T014 | C-30 | T025 |
| C-07 | T002 | C-19 | T015 | C-31 | T027 |
| C-08 | T003 | C-20 | T015 | C-32 | T027 |
| C-09 | T003 | C-21 | T016 | C-33 | T029 |
| C-10 | T003 | C-22 | T017 | C-34 | T032 |
| C-11 | T003 | C-23 | T023 | | |
| C-12 | T003 | C-24 | T026 | | |

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结后续「零丢失、零新增漂移、未论证成本」判据的对照物——implement 起点的可比较分母与证据落点。

- [ ] T001 捕获 implement 起点基线并建立证据落点：创建 `.specify/specs/106-background-silent-failure/notes/`，为 `notes/red-first-evidence.md`、`notes/quickstart-run.md`、`notes/pre-change-measurements.md` 各写标题占位；把 `git rev-parse --short HEAD`、`git status --short`、只读 `skills/external/sdd-loop-driver/scripts/watch-target.sh` 的 sha256 与 `--self-test` 尾行、调用 `scripts/python/sync-mirrors.py --check` 与 `scripts/python/regen-command-copies.py --check` 的 rc、调用 `scripts/python/scan-confirmation-gates.py --root . --json` 的 total 与触及文件命中集、调用 `scripts/python/role-edge-check.py --action report` 的空夹具输出、只读 `skills/internal/create-team/scripts/dispatch.sh` 现有 `.status` 行形状、六个 settlement 测试模块与 `tests/fixtures/settlement/` 的缺位状态写入 `notes/pre-change-measurements.md`；确认 `coverage-baseline.txt` (只读) 已冻结（787 行）；失败 nodeid 名集的捕获与比较形式归 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs。

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 结算契约的唯一真源——owner 章节。所有故事都只消费它、以指针抵达，任何第二张值表/证据矩阵都是违例。

**⚠️ CRITICAL**: 本阶段完成前，任何用户故事的实现行不得开始。

- [ ] T002 修订结算契约 owner 第一部分：在 `shared/definitions/superagent-definitions.md` § Termination 写入封闭七值集合（`completed` / `failed` / `anomaly` / `cancelled` / `running` / `silent-end` / `unknown`）与三分语义类（终态 / 非终态 / 检测缺陷）、逐值正证据要求表（含明确不构成该值的读数；退出 0 + 显式异常行结算 `anomaly` 且优先于 incomplete 失败分支；独立核验机制为封闭四值 `u4` / `team-verification` / `five-element` / `return-record`）、`silent-end` 的无 pid 分支（等待期限替代消失判定）与边界输入（`--live-window` / `--wait-deadline` / `--start-grace` 的缺省、值域与记录字段优先级按 C-25）、结算时刻的活证据规则、起点记录缺失即 `unknown`（finding 标签 `start-record-missing`，区别于不可读的 `unreadable`）、尝试记录写入既有派发日志目录的加性 `<label>.attempt`（FR-033 允许，非新存储根）、返回通道沉默不等于存活或完成、尝试唯一 label 与旧证据保留、父侧先结算再对外报告；措辞对只读 `scan-confirmation-gates.py` 的阻断模式零新增命中（EP-005 fallback 口径）。 [green: contracts/settlement-contract.contract.md#C-01] [green: contracts/settlement-contract.contract.md#C-02] [green: contracts/settlement-contract.contract.md#C-03] [green: contracts/settlement-contract.contract.md#C-04] [green: contracts/settlement-contract.contract.md#C-05] [green: contracts/settlement-contract.contract.md#C-06] [green: contracts/settlement-contract.contract.md#C-07]
- [ ] T003 修订结算契约 owner 第二部分：在同一章节写入 report / retry / stop 三反应及各自约束、禁止静默修复清单、取消只来自父侧显式记录、`settlement_version` 加性字段与 legacy 三分规则（标注 / 不计合规 / 不改写 / 不产生失败退出码）、virtual 排除与 native 前台终结分支；在 § Role Edges 保留四类封闭边违例并声明三类结算违例（`settlement-unrecorded` / `settlement-out-of-set` / `settlement-unbacked`）由同页拥有。 [green: contracts/settlement-contract.contract.md#C-08] [green: contracts/settlement-contract.contract.md#C-09] [green: contracts/settlement-contract.contract.md#C-10] [green: contracts/settlement-contract.contract.md#C-11] [green: contracts/settlement-contract.contract.md#C-12]

**Checkpoint**: owner 章节是唯一 owner——七值、逐值证据、反应、版本/legacy、边界与违例集合齐备，后续所有行只引用不复制。

---

## Phase 3: User Story 1 - 后台执行体无论怎么结束，父侧都能拿到一个可区分的结果 (Priority: P1) 🎯 MVP

**Goal**: 一个只读、确定性的判定面把既有载体证据收敛为恰好一个封闭结算值；`silent-end` 与 `unknown` 不再被折成成功、失败或仍在运行。

**Independent Test**: `tests/contract/test_settlement_engine.py` 与 `tests/contract/test_settlement_contract_definitions.py` 全绿；六类终局夹具逐类断言值 + 证据指针，静默消失夹具得到 `silent-end`（不可读为 `unknown`）且 `completed` / `failed` / `running` 误判数为 0。

### Tests for User Story 1 (MANDATORY) ⚠️

- [ ] T004 [US1] [blockedBy: T002,T003] 红先新建 `tests/contract/test_settlement_contract_definitions.py`：断言 owner 页面逐字包含 `silent-end` 与 `unknown`、七值与三分语义类、逐值正证据行、四类边违例保持与三类结算违例、`settlement_version` 与 legacy 规则、virtual/native 边界；反向断言 `shared/`、`skills/`、`templates/` 的声明面不存在第二张状态值表或第二份证据矩阵（只以指向 owner 的指针出现，FR-013）；运行 `scripts/bash/run-tests.sh` 记录红并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。
- [ ] T005 [P] [US1] [blockedBy: T002,T003] 新建确定性夹具树 `tests/fixtures/settlement/builders.py` 与静态夹具目录 `tests/fixtures/settlement/c1-state/`、`tests/fixtures/settlement/c3-report/`、`tests/fixtures/settlement/legacy/logs/`、`tests/fixtures/settlement/versioned/logs/`：按参见 `data-model.md` § E2 / § E3 / § E5 的形状生成六类终局（completed / failed / anomaly / cancelled / running / silent-end）、不可读指针、活体与半死（pid 丢失或复用）夹具，全部落在 `tmp_path` 或提交型静态目录，不用固定 `sleep`（FR-031、FR-032）。

### Implementation for User Story 1

- [ ] T006 [US1] [blockedBy: T005] 红先新建 `tests/contract/test_settlement_engine.py`：断言只读 `scripts/python/role-edge-check.py` 的 `--action settle` 存在且输出自有 schema（必需键超集断言，不锁定排他键集）与逐尝试 findings、六类终局夹具的结算值与证据指针、退出码 0/1/2 的三义（含 `silent-end` 判对也是 0、不可读为 2 且 `unknown` 永不为 0）、同输入两次运行逐字节相同、夹具树运行前后逐字节不变（零写入）、C1 判定映射（DONE / FAILED / ANOMALY / INCOMPLETE / DEAD / NO_SIGNAL / TIMEOUT / RUNNING）、C2 记录按证据结算、claim 与推导值不一致即 `settlement-unbacked`；调用唯一入口 `scripts/bash/run-tests.sh` 记录红并写入 `notes/red-first-evidence.md`。
- [ ] T007 [US1] [blockedBy: T002,T003,T006] 在 `scripts/python/role-edge-check.py` 加性实现 `--action settle`（零写入、无临时文件；`report` / `query` 输出逐字节不变）：读取 C1 四件套与 stage sidecar/spine、C2 三件套加 `<label>.attempt` / `<label>.end` / 可选 `<label>.settlement`、C3 报告映射行（5 列 legacy 与 7 列新格式）、C4 native attempt 记录；声明边界输入选项 `--live-window` / `--wait-deadline` / `--start-grace`（缺省、值域与记录字段 `wait_deadline_s` / `start_grace_s` 优先级按 C-25）；输出 E6 findings（value / class / evidence 指针 / consistent / legacy / unknown_cause / violations）与三类封闭违例；退出码沿用 0 判净 / 1 违例 / 2 `unknown`（不可读 / 不可解析或 `start-record-missing`，命名对应指针或起点槽）；`-h` / `--version` 与未声明选项拒绝保持前置（FR-028、FR-029）。 [green: contracts/carrier-conformance.contract.md#C-13] [green: contracts/enforcement-and-migration.contract.md#C-25] [green: contracts/enforcement-and-migration.contract.md#C-26] [green: contracts/enforcement-and-migration.contract.md#C-27] [green: contracts/enforcement-and-migration.contract.md#C-28]
- [ ] T008 [US1] [blockedBy: T006,T007] US1 转绿与取证：运行 `tests/contract/test_settlement_contract_definitions.py`、并运行 `tests/contract/test_settlement_engine.py`、再运行既有的 `tests/contract/test_role_edge_engine.py` 确认 `report` / `query` schema 原样；把同输入两次运行逐字节相同与零写入哈希的读数写入 `notes/red-first-evidence.md`，并对 T001 的 report 基线做逐字节比较（FR-014、FR-028）。 [green: contracts/enforcement-and-migration.contract.md#C-29]

**Checkpoint**: US1 独立可验——六类终局各得一个封闭值且带证据指针；不可读即 `unknown`（exit 2）。

---

## Phase 4: User Story 2 - 每个后台派发载体都产出足以结算的证据，且只有一套契约 (Priority: P1) 🎯 MVP

**Goal**: C1…C6 每个后台可脱离载体都留下足以结算的加性证据；每个派发入口与派发职责定义都引用同一个结算 owner，没有任何第二张表；virtual 与前台同步被写成显式排除。

**Independent Test**: 每个后台可脱离载体各有一个静默消失夹具并经同一判定面得到同一封闭值集合中的结果；`.status` 行被基线读取器原样读回；7 列新报告与 5 列 legacy 报告都可解析；载体清单之外的入口在守卫中判红（由 US4 的 scope 守卫收口）。

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T009 [US2] [blockedBy: T007] 红先新建 `tests/contract/test_settlement_carriers.py`：C2 的 SIGKILL 静默死亡（无 `.end`、pid 消失 → `silent-end`）、TERM/INT/HUP trap 写出终止记录（非零 → `failed`）、活体反向（pid 活 → `running`，不得 `silent-end`）、退出 0 无完成声明 → `failed`（incomplete）、`.status` 行与基线读取器读回一致；C3 的 5 列 legacy 与 7 列新头（缺 `end_state`/`evidence` → `settlement-unrecorded`；`completed` 无证据 → `settlement-unbacked`）；C4 与 C5 的文本钉（尝试记录、前台终结分支、virtual 排除与未完成不得报 `completed`）；C6 的逐值处置措辞；运行 `scripts/bash/run-tests.sh` 记录红并写入 `notes/red-first-evidence.md`（FR-015、FR-016、FR-017、FR-018、FR-019、FR-020、FR-021）。

### Implementation for User Story 2

- [ ] T010 [US2] [blockedBy: T009] 在 `skills/internal/create-team/scripts/dispatch.sh` 加性写入起点与终止证据：启动 CLI 前写 `<label>.attempt`（attempt_id、carrier `c2-subprocess`、parent、started_at、pid、`/proc` 可用时的 pid_start_ticks、`settlement_version: 1`），正常退出与 TERM/INT/HUP trap 写 `<label>.end`（exit / signal / ended_at / settlement_version）；`.status` 行格式、三件套语义、`-h` / `--version` 守卫与未声明选项拒绝逐字不变；不新增心跳文件（FR-015）。 [green: contracts/carrier-conformance.contract.md#C-14]
- [ ] T011 [US2] [blockedBy: T009,T010] C2 转绿与取证：运行 `tests/contract/test_settlement_carriers.py` 的 C2 子集，断言 SIGKILL → `silent-end`（exit 0）、TERM → `failed`、exit 0 无声明 → `failed`（incomplete）、活体 → `running`、不可读 → `unknown`（exit 2），并用只读 `scripts/python/journal-utils.py` 与 `scripts/python/status-digest.py` 的既有解析函数对旧 `.status` 与新 `.status` 得到相同解析结果；把命令与读数写入 `notes/red-first-evidence.md`（FR-016）。 [green: contracts/carrier-conformance.contract.md#C-15]
- [ ] T012 [P] [US2] [blockedBy: T002] 在 `skills/internal/create-team/SKILL.md` § Report 扩展派发映射表：新报告列为 `label` | `role` | `dispatch_duty` | `workspace` | `parent` | `end_state` | `evidence`（7 列），5 列 legacy 头仍被接受并解析为 legacy（其缺列行豁免 `settlement-unrecorded`、只标 legacy）；`## Verification` 必填段声明结算覆盖；7 列新格式行空 `end_state`/`evidence` 记 `settlement-unrecorded`，`completed` 无证据指针记 `settlement-unbacked`；值域与证据矩阵指向结算 owner，不复制第二张表（FR-017）。 [green: contracts/carrier-conformance.contract.md#C-16]
- [ ] T013 [P] [US2] [blockedBy: T002] 在 `skills/internal/run-agent/SKILL.md` 写入 C4 native 义务：native 后台交接前把尝试记录写入既有派发日志目录（carrier `c4-native`，E2 形状）；返回时按五要素结算（缺任一 → `failed`（incomplete）且不消费；宿主报错 → `failed`）；声明的等待期限（C-25 的 `--wait-deadline` 或记录字段 `wait_deadline_s`）已过且无返回、无活信号 → `silent-end`；宿主不提供后台形态时显式声明为前台终结、不产生结算边；virtual 排除以指向结算 owner 的一句话交接，不复制第二张模式表（FR-010、FR-018）。 [green: contracts/carrier-conformance.contract.md#C-17]
- [ ] T014 [P] [US2] [blockedBy: T002] 在 `shared/definitions/subagent-definitions.md` § Three Execution Modes 写入 virtual 排除：不能脱离会话、父侧就是执行者、不存在孤儿边、因此排除在后台结算之外，且未完成的 virtual 工作不得报 `completed`，并附指向结算 owner 的指针（FR-019）。 [green: contracts/carrier-conformance.contract.md#C-18]
- [ ] T015 [US2] [blockedBy: T002] 在 `shared/workflow/external-dispatch-recipes.md` 把 Recipe 4 的单一 stall 句替换为逐值处置（无哨兵且主体消失/无终止记录 → `silent-end`，证据不可读 → `unknown`，无哨兵但主体仍活 → `running`），并限定后台配方只允许合规 runner/wrapper 或显式前台终结两形态；Recipe 7 的结果契约写明每个校验者独立结算、缺失状态/结论即 `failed`（incomplete）并按既有规则重问、不得从波次结果静默消失，结算 owner 以指针引用（FR-020、FR-021）。 [green: contracts/carrier-conformance.contract.md#C-19] [green: contracts/carrier-conformance.contract.md#C-20]
- [ ] T016 [US2] [blockedBy: T003] 在 `shared/definitions/superagent-definitions.md` § Termination 追加 observer 可选句：observer 可记录结算事实但不得成为唯一结算载体，没有 observer 的线仍必须结算；不新增 probe class、handler binding 或 observer 依赖（FR-022）。 [green: contracts/carrier-conformance.contract.md#C-21]
- [ ] T017 [US2] [blockedBy: T002,T003] 为派发入口与派发职责定义各写一行结算 owner 指针：`skills/internal/run-team/SKILL.md`、`skills/external/sdd-loop-driver/SKILL.md`、`templates/commands/agents.md`、`templates/commands/team.md`、`agents/sdd-plan-coordinator.agent.md`、`agents/sdd-task-coordinator.agent.md`、`agents/sdd-implement-coordinator.agent.md`、`agents/sdd-review-coordinator.agent.md`；叶子执行者模板不获得第二套结算逻辑；任何一处都不得出现第二张状态值表或第二份证据矩阵（FR-012、FR-013）。 [green: contracts/carrier-conformance.contract.md#C-22]
- [ ] T018 [US2] [blockedBy: T009,T011,T012,T013,T014,T015,T016,T017] US2 转绿与取证：运行 `tests/contract/test_settlement_carriers.py` 全模块，逐载体记录静默形态的结算值与反应读数（C1/C2/C3/C4/C6；C5 为排除断言），并把 `.status` 旧格式可读、7 列新头解析、指针行使 owner 唯一性写入 `notes/red-first-evidence.md`（FR-017）。

**Checkpoint**: US2 独立可验——每个后台可脱离载体都能被同一判定面结算；virtual 与前台同步的排除有文本与断言；入口指针全部指向同一 owner。

---

## Phase 5: User Story 3 - 检测到静默结束后，反应是显式且不可静默修复的 (Priority: P2)

**Goal**: 父侧在报告前结算每个尝试；`silent-end` / `unknown` 显式上送；重试是新尝试/新 label 且旧证据保留；停止活尝试记 `running` + 活证据 + 停止理由；不代写、不补齐、不改写、不删除证据、不消费旧返回。

**Independent Test**: 双尝试夹具中旧尝试 `silent-end`、重试换新 label、旧证据哈希不变、旧返回不被消费；报告文本逐项覆盖且不用成功语气；自动 kill 计数为 0。

### Implementation for User Story 3

- [ ] T019 [US3] [blockedBy: T002,T003,T013] 在 `skills/internal/run-agent/SKILL.md` 写入反应义务：父侧在对外完成报告之前结算它开过的每个尝试；成功报告逐项携带子尝试结算值与证据指针，未结算者标「未结算」，失败 / 异常 / `silent-end` / `unknown` 逐项上送且不被聚合语气覆盖；重试 = 新尝试 / 新 label 且旧证据保留；对 `silent-end` / `unknown` 的重试必须附具名诊断或用户裁定；停止活尝试记 `running` + 活证据 + 停止理由，不得记 `silent-end`；不代写 / 不补齐 / 不改写 / 不删除证据（FR-011、FR-023、FR-024、FR-025、FR-027）。

### Guard Tests for User Story 3 (migration/regression exception — after implementation)

- [ ] T020 [US3] [blockedBy: T019] 回归守卫（例外声明：守的是 T007 与 T019 已交付的行为）：在 `tests/contract/test_settlement_engine.py` 追加重试 / 晚到返回断言（新 label 是独立 finding、旧尝试保持自身结算值、旧证据文件哈希不变），在 `tests/contract/test_settlement_carriers.py` 追加 run-agent 报告覆盖与禁止静默修复的文本钉；运行 `scripts/bash/run-tests.sh` 记录读数；红能力由 T021 的演练与 T025 的变异证明，不冒充红先（FR-023…FR-027）。

### Reaction Drill and Turn-green

- [ ] T021 [US3] [blockedBy: T020] 反应演练：构造「旧尝试 `silent-end` + 新 label 重试」双尝试夹具，运行 `tests/contract/test_settlement_engine.py` 的相关断言并记录——上送条目存在、重试 label 不同、旧证据哈希前后相等、自动 kill 次数 0、旧返回消费次数 0；读数写入 `test-evidence/reaction-drill.md`（SC-004 的 Source，FR-023、FR-024）。
- [ ] T022 [US3] [blockedBy: T021] US3 转绿与取证：运行 `tests/contract/test_settlement_engine.py`、并运行 `tests/contract/test_settlement_carriers.py`，把反应读数与两条运行结果写入 `notes/red-first-evidence.md`。

**Checkpoint**: US3 独立可验——静默结束的反应可见、可点名、不可被静默修复。

---

## Phase 6: User Story 4 - 静默终止能让一条检查转红，而不是只在文档里被禁止 (Priority: P2)

**Goal**: 四个变异演练各能让至少一条测试转红；每个载体有确定性静默夹具与反向夹具；不可读证据返回 `unknown`（exit 2）而不是绿色；保留面与 `fbab7a45c` 逐成员相等。

**Independent Test**: `test_settlement_preservation.py` / `test_settlement_scope.py` 全绿；四个 drill 的红记录在 `test-evidence/mutation-drill.md`；活体夹具的 `silent-end` 误报数为 0。

### Tests (Guards) for User Story 4

- [ ] T023 [US4] [blockedBy: T008,T018] 保留面守卫（migration/regression 例外，置于实现之后）：新建 `tests/contract/test_settlement_preservation.py`——用 `test-evidence/watch-target-fbab7a45c.sh` 的同一抽取器断言 watcher 判定 token 集、退出码集、哨兵字面量集与 `fbab7a45c` 基线逐成员相等，`--self-test` 39/0，五要素上行与七字段下行文本不变，只读 `scripts/python/role-edge-check.py --action report` 对 T001 基线输出逐字节相同，只读 `scripts/python/scan-confirmation-gates.py` 的触及文件命中数不大于基线（EP-005 fallback），两槽位预算未新增第三槽；运行 `scripts/bash/run-tests.sh` 记录读数（FR-014、FR-033、FR-039）。 [green: contracts/carrier-conformance.contract.md#C-23]
- [ ] T024 [US4] [blockedBy: T005,T009,T020] 活体 / 反向夹具：扩展 `tests/fixtures/settlement/builders.py` 增加 live（短生命周期子进程、pid 存活）与 zombie / pid-reuse 构造，事实型事件轮询而非固定 `sleep`；在 `tests/contract/test_settlement_carriers.py` 追加反向断言——活体在所有后台可脱离载体上不得被判 `silent-end`，长时间无输出但 pid 活保持 `running`（FR-005、FR-031、FR-032、SC-008）。

### Mutation Drill, Scope Guard and Close-out for User Story 4

- [ ] T025 [US4] [blockedBy: T023,T024] 变异演练：逐项执行四个 drill（移除 / 削弱静默终止检测、移除 / 削弱活证据要求、让 `unknown` 返回 0、移除证据指针要求），每项记录至少一条转红的测试（命令 + 输出），逐项复原；未转红即记守卫缺陷，不得软化；读数写入 `test-evidence/mutation-drill.md`（FR-029、FR-030）。 [green: contracts/enforcement-and-migration.contract.md#C-30]
- [ ] T026 [US4] [blockedBy: T018,T024] 新建 `tests/contract/test_settlement_scope.py`：载体清单 C1…C6 为封闭集且每个 C-ID 至少被一个测试引用；全仓声明面无第二张状态值表 / 证据矩阵 / 载体私有判定副本；零新增调度器 / 注册表 / 队列 / 存储 / 通知通道 / child list、零新增 probe class 或 observer 依赖；引擎无 kill / retry / delete / push 权限（AST 扫描）；以一次小型元变异（临时副本注入第二张值表）证明该守卫可转红，读数写入 `test-evidence/mutation-drill.md`（FR-012、FR-013、FR-020、FR-038、FR-041）。 [green: contracts/carrier-conformance.contract.md#C-24]
- [ ] T027 [US4] [blockedBy: T023,T024,T025,T026] US4 转绿与取证：运行 `tests/contract/test_settlement_preservation.py`、并运行 `tests/contract/test_settlement_scope.py`、并运行 `tests/contract/test_settlement_carriers.py`；把载体 × 测试覆盖矩阵（C1…C6 各至少一个确定性测试与一个反向夹具；C5 为排除断言、C4 含前台分支）与全部读数写入 `notes/red-first-evidence.md`；未覆盖载体数为 0 才算通过（FR-031、FR-032、FR-033）。 [green: contracts/enforcement-and-migration.contract.md#C-31] [green: contracts/enforcement-and-migration.contract.md#C-32]

**Checkpoint**: US4 独立可验——规则不再只是散文：删掉任一检测都至少一条转红，活体不被误报。

---

## Phase 7: User Story 5 - 客户项目升级后拿到同一契约，旧记录不被假装成合规 (Priority: P3)

**Goal**: 新字段/新文件一律加性；旧记录被标 legacy 且不计合规、不被改写、不产生失败退出码；不兼容变更清点为空；镜像与逐工具副本由生成器落盘；三个文档页指向同一 owner。

**Independent Test**: legacy 与 versioned 夹具对审计输出满足「有推导值 + 有 legacy 标注 + 退出码非 1」；versioned 记录带 `settlement_version: 1`；不可读证据 exit 2；`sync-mirrors.py --check` 与 `regen-command-copies.py --check` 为 0 且相对基线零新增漂移。

### Tests for User Story 5 (red-first)

- [ ] T028 [US5] [blockedBy: T005,T007] 红先新建 `tests/contract/test_settlement_migration.py`：旧格式夹具标 `legacy: true` 且仍产出推导值、退出码非 1（标注不是拒绝）、文件哈希未被改写；新格式夹具按 `settlement_version: 1` 审计 claim；不可读证据 → exit 2 且 `unknown` 点名指针；断言本特性的不兼容变更清点为 0 且不新增预造拒绝机制；运行 `scripts/bash/run-tests.sh` 记录红（`legacy` 字段尚未出现）并写入 `notes/red-first-evidence.md`（FR-007、FR-034、FR-035）。

### Implementation for User Story 5

- [ ] T029 [US5] [blockedBy: T028] 在 `scripts/python/role-edge-check.py` 的 settle 输出加性落地 version / legacy：无 `settlement_version` 的记录带 `legacy: true` 并仍从原始证据推导；5 列 legacy 报告行豁免 `settlement-unrecorded`（只标注、exit 0）；合规计数只统计带版本的记录；legacy 标注不影响退出码；不新增拒绝分支（拒绝只归 `unknown`，FR-034、FR-035）。 [green: contracts/enforcement-and-migration.contract.md#C-33]
- [ ] T030 [US5] [blockedBy: T029] 更新三个既有文档页：`docs/reference/skills/sdd-loop-driver.md` 增加结算章节（owner 指针 + C1 判定映射指针）、`docs/reference/commands/agents.md` 的 Run Mode 增加结算指针、`docs/reference/teams/orchestration.md` 增加席位 `end_state` 与结算覆盖指针；取值与 owner 一致，不复制第二份集合 / 映射（FR-037）。
- [ ] T031 [US5] [blockedBy: T010,T012,T013,T014,T015,T016,T017,T030] 再生成镜像与逐工具副本（MUST NOT 手改）：依次调用 `python3 scripts/python/sync-mirrors.py --write --only shared`、`--only scripts`、`--only skills/internal`、`--only skills/external`、`--only agents`，再调用 `python3 scripts/python/sync-mirrors.py --check`；调用 `python3 scripts/python/regen-command-copies.py` 后 `--check`；断言触及镜像对逐字节一致、命令副本各含新增指针行、漂移成员集无新增（FR-036）。

### Turn-green and Honesty Boundary

- [ ] T032 [US5] [blockedBy: T028,T029,T031] US5 转绿与诚实边界：运行 `tests/contract/test_settlement_migration.py`；写 `test-evidence/enforcement-honesty.md` 记录行为类条款集合（C-34 列出的八项）逐项由文本 + 评审 / 变异演练举证、未被任何测试行冒充机器覆盖，并附 legacy / versioned 与镜像 / 副本读数（FR-041）。 [green: contracts/enforcement-and-migration.contract.md#C-34]

**Checkpoint**: US5 独立可验——升级加性、旧记录可解释但不合规、镜像与副本一致、诚实边界明示。

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: quickstart 实跑、逐 SC 验收证据、非目标审计与最终门禁——跨故事、不可提前的收尾面。

- [ ] T033 [blockedBy: T022,T027,T032] quickstart 实跑：执行 `quickstart.md` 的 S-0、S-1、S-2、S-3、S-4、S-5、S-6、S-7 可执行部分并贴真实输出（S-1/S-3/S-4/S-5 此时已可执行），teardown 只删除自建的 `.specify/.tmp/settlement-demo`；落盘 `notes/quickstart-run.md`。
- [ ] T034 [blockedBy: T033] 验收证据包：写 `test-evidence/acceptance-106.md` 逐条记录 SC-001…SC-009 的状态、测量命令、真实输出与证据指针（SC-001 / SC-004 / SC-008 的活 / 死 / 半死夹具读数、SC-002 的守卫退出码、SC-003 的三集合相等、SC-005 的覆盖矩阵、SC-006 的 legacy / versioned 与镜像读数、SC-007 的重复运行 diff 与无固定 sleep 扫描、SC-009 的 gate 读数）；final / supporting 路径标注与 `requirements.md` 一致。
- [ ] T035 [blockedBy: T034] 写 `.specify/specs/106-background-silent-failure/verification.md`：逐 SC 状态行（SC-001 / SC-002 / SC-004 为 `final` 且记 `pass`，其余按实测 supporting 读数）、`smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`（指向存在的证据文件）与 `deferred_tasks=`（无 `[~]` 时为空）；不伪造未测读数。
- [ ] T036 [blockedBy: T032,T035] 非目标与零第二机制审计：断言零自动 kill / stop / retry、零推送 / 合并 / 删分支、零证据删除 / 改写 / 历史重写、零新增调度器 / 注册表 / 队列 / 存储 / 通知通道、`.status` 与哨兵字面量不变、只读 `scripts/python/scan-confirmation-gates.py` 的触及文件零新增命中；调用 `scripts/python/scan-confirmation-gates.py --root . --json` 与只读 `scripts/python/account-clause-coverage.py --spec-dir .specify/specs/106-background-silent-failure`，把命令、真实输出与结论写入 `test-evidence/non-goals-audit.md`（FR-038、FR-039、FR-040）。
- [ ] T037 [blockedBy: T036] 最终门禁：调用 `python3 .specify/scripts/python/validate-tasks.py .specify/specs/106-background-silent-failure/tasks.md`（exit 0）、调用 `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/106-background-silent-failure --stage tasks --repo .`（decision=pass errors=0）、再调用 `python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/regen-command-copies.py --check`、并断言 `grep -cE '^- \[[ >]\]' .specify/specs/106-background-silent-failure/tasks.md` 返回 0；命令与读数写入 `test-evidence/final-gate.txt`。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖——T001 先落基线。
- **Foundational (Phase 2)**: 依赖 Setup；T002 / T003 串行写同一 owner 文件，完成后任何故事行才可动。
- **User Stories (Phase 3–7)**: 均依赖 Foundational；US1 交付结算值与判定面，US2 交付载体证据，US3 反应，US4 守卫，US5 迁移 / 镜像；跨故事的显式依赖由 `[blockedBy:]` 承载，不靠阶段顺序猜测。
- **Polish (Phase 8)**: 依赖全部用户故事完成（quickstart 与最终门禁必须在镜像 / 副本再生成之后）。

### User Story Dependencies

- **US1 (P1)**: Foundational 后即可开始；独立可验（六类夹具与引擎模块）。
- **US2 (P1)**: 依赖 US1 的引擎动作（T007）以读取 C2/C3/C4 证据；不依赖 US3 / US4 / US5。
- **US3 (P2)**: 依赖 US1 引擎与 US2 的 run-agent 文本（T013）；只追加测试、演练与证据。
- **US4 (P2)**: 依赖 US1 / US2 的全部行为面与 US3 的反应面；其守卫为回归例外。
- **US5 (P3)**: 依赖 US1 引擎（T007）与 US2 载体文本；文档与镜像必须在全部源编辑之后。

### Within Each User Story

- 新行为测试先写并确认失败 → 实现 → 转绿取证；例外：T023 的保留面守卫与 T028 的 version/legacy 守卫是守既有行为的回归守卫（T028 在 T029 落地 `legacy` 前保持红），红能力由 T021 / T025 / T032 的读数证明。
- 同一文件的多行严格按行序串行：`shared/definitions/superagent-definitions.md`（T002 → T003 → T016）、`skills/internal/run-agent/SKILL.md`（T013 → T019）、`scripts/python/role-edge-check.py`（T007 → T029）、`tests/fixtures/settlement/builders.py`（T005 → T024）、`tests/contract/test_settlement_engine.py`（T006 → T020）、`tests/contract/test_settlement_carriers.py`（T009 → T020 → T024）。
- 每个故事以 `**Checkpoint**` 收口，独立可验后再进入下一故事。

### Parallel Opportunities

- **US1**: T005（夹具树）与 T004（契约定义测试）写目标不同，可并行；其余行共享 `notes/red-first-evidence.md` sink，按行序串行。
- **US2**: T012（create-team SKILL）、T013（run-agent SKILL）、T014（subagent-definitions）写目标逐行不同，可并行；T010 / T011 与 T015 / T016 / T017 按行序串行。
- 其余阶段零 `[P]`：同一文件、共享证据 sink 或同一镜像面按行序串行。

---

## Parallel Example: User Story 2

```text
# T002 完成后，三个文本面可同时开工：
Task: "create-team SKILL 7 列映射表与 Verification 结算覆盖（T012）"
Task: "run-agent SKILL 尝试记录 / 前台终结分支 / virtual 指针（T013）"
Task: "subagent-definitions § Three Execution Modes virtual 排除（T014）"

# 三者完成后，与 C2 证据行汇合：
Task: "T011 C2 转绿 → T015 配方 → T016 observer 句 → T017 入口指针 → T018 全模块转绿"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: **US1 + US2**——两条同为 P1 且互为前提：只有结算值而没有载体证据，判定面没有输入；只有载体证据而没有结算值，证据无法收敛为结论。两者检查点各自独立可测，合起来构成可演示的最小增量。

1. 完成 Phase 1（Setup）与 Phase 2（Foundational）。
2. 完成 US1（owner 文本 → 夹具 → 引擎实测 → 转绿）→ 检查点验证。
3. 完成 US2（C2 证据 → C3 / C4 / C5 / C6 文本 → 入口指针）→ 检查点验证（MVP 到此可演示）。
4. 依次完成 US3（反应）→ US4（守卫 / 变异）→ US5（legacy / 镜像）。
5. Polish：quickstart 实跑 → 验收证据包 → verification → 非目标审计 → 最终门禁。

### Incremental Delivery

每一故事结束时其检查点独立可验、不破坏前序故事；镜像与逐工具副本只在全部源编辑完成后一次性再生成（T031）；`report` / `query` 的字节相等由 T008 与 T023 双重守卫。

---

## Notes

- [P] 任务 = 不同写目标、无未完成依赖；共享 `notes/red-first-evidence.md` sink 不算并行面。
- Story 标签只用于用户故事阶段行；Setup / Foundational / Polish 零 `[US` 标记。
- 契约条款分区：34 条各被一行 `[green:]` 认领一次；认领行序与条款序号单调一致；行为类条款只以文本 + 评审 / 变异演练举证（C-34）。
- 既有失败名字级基线由实现入口 Step 0 重采（owner：`.specify/skills/internal/implement-feature/SKILL.md` § Test runs），本文件不复述比较形式。
- EP-005：冻结 `total == 27` 的相等判定在基线已红（live 31）；本特性的度量是触及文件零新增命中，不声称 `== 27` 绿。
- 会计器 FR 车道：`account-clause-coverage.py` 报 `claimed clauses 34`、`clause-uncovered` beyond-baseline 0；`fr-uncovered` 为 37/41（FR-036 / FR-037 / FR-039 / FR-040 不被任何契约条款引用）。后者是三份契约的既有引用结构事实，按 GATE-3 如实报告；FR 覆盖权威判据是 § Requirement Coverage Map（41/41）与 pre-analyze `runtime-stack-row` errors=0。
- plan-owned 面无任务行主动编辑；crew MUST NOT 写入（forbidden 领土见 `handoff.md` § Territory / `team.md` territory.forbidden）。实现中发现设计面缺陷时停线回抛 spec 侧，由 spec 侧以 PLAN-EDIT 披露纪律修订（本文件不授予 crew 对 plan-owned 路径的编辑权）；实质性改动停线回抛。
- 两槽位测试预算不变；不新增第三全量槽；全部新增测试经唯一入口运行。
