# Tasks: Prompt Adherence Evaluation（提示遵从度评价）— Spec Kit 移植

**Requirement ID**: 109
**Requirement Key**: `109-prompt-adherence`
**Related Feature**: 109 Prompt Adherence Evaluation（提示遵从度评价）— `.specify/features.md` 行 109 当前 `Planned`；本阶段只复核特性清单（见 § Feature Integration Review），不推进生命周期、不编辑 registry
**Input**: Design documents from `.specify/specs/109-prompt-adherence/`: requirements.md（30 FR / 9 SC / 14 条澄清 / A-1…A-18 / US1…US5）、plan.md（23 行宪法检查 / PA1–PA16 / EP-001…EP-008 / Mirror Obligations）、research.md（R-1…R-11 + RU-1…RU-3）、data-model.md（E-1…E-11 + I-1…I-14）、contracts/ ×6（39 条款：owner-and-catalog 7 / declarations-and-vocabularies 7 / reading-semantics 10 / engine-and-read 5 / distribution 3 / guards-and-boundaries 7）、quickstart.md（6 场景 + 传感器读取块 + 分发/套件检查块）、feature-ref.md
**Prerequisites**: plan.md（必需）、requirements.md（必需）、data-model.md、contracts/、research.md、quickstart.md、feature-ref.md

**Tests Mode**: ON — 宪法 Principle IV「Test-First & Contract-Driven Implementation」为测试强制原则（其 MUST 行要求 unit / regression / integration+contract 覆盖）；本特性交付可执行运行时引擎 `scripts/python/prompt-adherence.py`，宪法 §IV 的 template-only（Partial justified）豁免不适用。新行为守卫一律红先；两处守既有交付行为的守卫（US3 的包含性/初始化守卫、US5 的 advisory-only 腿）按 migration/regression 例外置于其实现之后，并在行内声明。

**Tests**: 红先证据的唯一落点 `.specify/specs/109-prompt-adherence/notes/red-first-evidence.md`（每条：命令、真实输出、退出码）。测试唯一入口 `scripts/bash/run-tests.sh`；解释器前置约束固定在 § Environment Prerequisites。失败 nodeid 名集的捕获与比较形式归 `/speckit.implement` 的 `**Test runs**` owner，本文件只引用、不复述其路径与 flag。

**Green-point tags**: 本文件使用可选 `[green: <contract>#<clause>]` 认领；39 条款的分区在 § Clause Coverage & Green Partition 一次性声明（每条恰一次、每契约内认领序号随行序单调）。测试编写行不携带认领，`validate-tasks.py` 的四项 green 检查零 ERROR。

**Organization**: 按 `requirements.md` 的五个用户故事组织——US1、US2、US3 为 P1，US4 为 P2，US5 为 P3——外加 Setup、Foundational 与 Polish 三个阶段。owner 文档、五个声明事实与框架地图行是所有故事共同消费的阻塞前置；引擎在 US1 建成，US2/US4 在其上扩写、绝不重写。

**任务行数**: 39 条任务（T001…T039）。

## Definition of Done (DoD)

- DoD-1: `shared/definitions/prompt-adherence-definitions.md` 是前提链、双层模型、六行信号目录与声明归因、盲区登记、机器可检覆盖图、读取契约字段含义与本特性红线的唯一 owner；其他表面只按路径指向它（FR-001, FR-002, FR-003, FR-004, FR-028, FR-029）。
- DoD-2: `shared/declarations/facts/` 下恰好五个声明事实，具备声明层 required keys 与既有 `closed-set` kind；观察状态不设第六事实，读时组合既有七态域与 `not_evaluated` 字面量（FR-018, SC-007）。
- DoD-3: `scripts/python/prompt-adherence.py` 是单一 stdlib 只读脚本，其文档化调用、flags、help/version 内容、未声明选项拒绝与退出码语义（0/1/2）与脚本接口契约及 FR-023 完全一致；`--version` 在运行时从最近 `pyproject.toml` 重导出（FR-022, FR-023）。
- DoD-4: 每份读取确定、重跑逐字节相同，引用可解析源，披露 invalid sources 与 duplicates，携带强制覆盖节，且绝不输出遵从裁决令牌、复合评分或排名（FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-025）。
- DoD-5: 只读包含性声明成立——在按运行与纵向两种读取前后，对 `shared/declarations/facts/runtime-store-layout.yaml#/statement` 所辖受管存储根计算的哈希清单逐字节不变、零新文件，解释器字节码缓存按名排除；确定性与包含性分开判定（FR-006, SC-002）。
- DoD-6: 分发走既有 publish → install → init——镜像对源逐字节一致且相对基线无 NEW drift，fresh init fixture 含该机制，并在网络隔离下以显式 `not_evaluated` / `Unobserved` 行完成读取（FR-020, FR-021, SC-005, SC-009）。
- DoD-7: 契约 C-040 点名的五个守卫文件存在，在所属行声明的位置红先（或按 migration/regression 例外声明），演练每个新封闭集的每个成员，拒绝未知令牌，覆盖图机器检查可触达（FR-024, SC-004, SC-007）。
- DoD-8: 一份本仓库的日期化基线读取经既有 feedback 渠道落盘，凭其源引用可重放，含显式未观察行，且不声称改进（FR-008, FR-026, SC-008）。
- DoD-9: 每个非注册表行的存储根派生自布局事实——经 `declaration_reader.py` 读取 `runtime-store-layout.yaml#/statement`，根是 `.specify/<store-name>/` 投影；引擎不持第二张根表，行点名未声明 store 为硬错误（退出 2）（FR-005, FR-030）。
- DoD-10: `verification.md` 每条 SC 一行状态，`final` 路径判据为 `pass` 且 smoke 记录齐备；Feature 109 在 Pre-Status-Flip Gate 下 `Planned → Implemented`；不新增 instructions 节、不发布 `/speckit.*` 命令或 skill 包装器（FR-023, FR-024, SC-009）。

**DoD Status**: pending

## Completion Gate

- GATE-1: 全量套件相对实现入口基线零 NEW 失败名 — check: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh --names-out .specify/specs/109-prompt-adherence/final-failed.txt` 后做名称级对照（基线捕获与比较形式归 `/speckit.implement` § Test runs，本文件不复述）。
- GATE-2: plan.md § Mirror Obligations 的每一行逐字节一致 — check: `python3 scripts/python/sync-mirrors.py --check` 对本特性触及的对相对 `notes/pre-change-measurements.md` 无 NEW drift；`python3 scripts/python/regen-command-copies.py --check` exit 0。
- GATE-3: 无 `[ ]` 或 `[>]` 任务行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/109-prompt-adherence/tasks.md` 返回 0。
- GATE-4: 每条 `final` 路径成功判据为 `pass` 且 smoke 记录齐备 — check: `verification.md` 中 `**Path**` 为 `final` 的 SC-001…SC-008 全部 `SC-NNN_status=pass`，且 `smoke_command=`、`smoke_exit_code=0`、`smoke_evidence_path=`（路径存在且非空）齐备（条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates）。
- GATE-5: 结构校验器静默 — check: `python3 scripts/python/validate-tasks.py .specify/specs/109-prompt-adherence/tasks.md` exit 0；`python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/109-prompt-adherence --stage tasks --repo .` 输出 `decision=pass` errors=0（advisory 逐条裁定）。
- GATE-6: 引擎与声明层干净 — check: `python3 scripts/python/script-interface-check.py --files scripts/python/prompt-adherence.py,.specify/scripts/python/prompt-adherence.py --json` 零违规；`python3 scripts/python/harness-triple-check.py --action verify` 对五个 `prompt-adherence-*` slug 干净。
- GATE-7: 布局事实派生守卫 — check: 引擎源码的 `declaration_reader` + `runtime-store-layout` 读点可定位（triple-check 条件 c）；引擎无第二根表（只读源码扫描）；`tests/contract/test_prompt_adherence_engine.py` 的未声明 store 用例以退出 2 拒绝。
- GATE-8: 覆盖图机器检查干净 — check: `python3 scripts/python/prompt-adherence.py --check-coverage` 退出 0 零发现；篡改副本退出 1 并点名发现；不可读 owner 文档退出 2。

## Environment Prerequisites

- CPython `>=3.8`: **available** — probe: `/usr/local/bin/python3 --version` → `Python 3.11.11` @ 2026-11-27；PATH 的 `python3` 解析到 `/storage/project/profiles/.venv/bin/python3`（同为 3.11.11）；affected: 全部实现行与测试行。
- pytest: **available** — probe: `/usr/local/bin/python3 -m pytest --version` → `pytest 8.4.2` @ 2026-11-27；约束：PATH 的 `python3` **import no pytest**（`python3 -m pytest --version` → `No module named pytest`），且本工作树无 `.venv/bin/python`，因此全部测试行 MUST 经唯一入口并传入 `SPECKIT_PYTHON=/usr/local/bin/python3`；探针：带覆写 `bash scripts/bash/run-tests.sh tests/contract/test_runtime_store_layout.py --collect-only -q` → `7 tests collected` exit 0；不带覆写 → `error: no interpreter with pytest found` exit 1；affected: 全部测试行。
- bash / git: **available** — probe: `bash --version` → `4.4.20(1)-release`；`git --version` → `2.43.5` @ 2026-11-27；affected: 唯一测试入口、镜像/副本、基线对象与证据行。
- 容器运行时 / 镜像仓库 / 活集群 / 外网: **none** — 本特性全部检查为本地文件、`git`、本地 pytest 与既有只读引擎，无构建、无拉取、无网络、无守护进程 @ 2026-11-27；affected: none。

**A13 boundary**（owner: `shared/workflow/acceptance-hardening.md` § Gates — 本注为指针，不是第二规则）：本节只记录任务生成期的探针结论（探测命令 + ISO 日期）；规划期承重前提归 `plan.md` § Execution Premises，依赖特性继承记录归 `plan.md` § Inherited Blockers。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标逐行不同、无未完成依赖）。本文件的 `[P]` 只出现在 T007 / T008（owner 文档 vs 框架地图）与 T023 / T024（readonly 守卫 vs init 守卫，红先证据落不同 sink）；其余行因共享同一引擎、同一测试文件或同一证据 sink 而按行序串行。
- **[Story]**: 用户故事标签（`[US1]`…`[US5]`），只出现在用户故事阶段的任务行；Setup / Foundational / Polish 阶段零故事标记。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全 `[X]` 前不得开始本行。仅阶段顺序关系时不写。
- **[green: <contract>#<clause>]**: 绿点认领——本行是该条款在全 carrier 集合上转绿的那一行；契约路径相对本文件目录解析。分区见 § Clause Coverage & Green Partition，每条恰一次。
- 每行必须单行完成（含文件路径与全部标签），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `verification.md` 的 `deferred_tasks=`，并在行内加 `<!-- deferred: <reason> -->`）。

## Path Conventions

- **框架源（编辑面）**: `shared/definitions/prompt-adherence-definitions.md`、`shared/definitions/framework-map.md`、`shared/declarations/facts/prompt-adherence-*.yaml`、`scripts/python/prompt-adherence.py`、`tests/contract/test_prompt_adherence_*.py`、`tests/integration/test_prompt_adherence_init.py`、`tests/fixtures/prompt-adherence/`。
- **生成面（MUST NOT 手改）**: `.specify/shared/**` 与 `.specify/scripts/**`（`sync-mirrors.py` 投影）；每工具命令副本（本特性零改动）。
- **证据落点（本特性）**: `.specify/specs/109-prompt-adherence/` 下的 `notes/{pre-change-measurements.md,red-first-evidence.md,quickstart-run.md}`、`test-evidence/{us3-red-readonly.txt,us3-red-init.txt,tasks-validator.txt,boundary-readings.txt,implementation-gates.txt}`、`coverage-baseline.txt`、`baseline-failed.txt`（实现入口基线的捕获形式归 `/speckit.implement` § Test runs）。
- **只读面（零修改）**: `.specify/specs/109-prompt-adherence/{plan.md,requirements.md,data-model.md,contracts/,research.md,quickstart.md,feature-ref.md}`（plan-owned；实现期间如需实质变更按 stage 规则回抛 `ANOMALY`）；`.specify/register.md` 与 driver state spine（本阶段零编辑）。

## Deliverable Coverage Map

十一个交付家族与任务行的对应（brief 清单 + FR-026 的日期化基线）：

| # | 交付家族 | 任务行 | 说明 |
|---|----------|--------|------|
| 1 | 只读引擎 `scripts/python/prompt-adherence.py` | T011, T012, T013, T014, T015, T020, T028 | 接口 → 声明/布局/owner 读取 → 六传感器 → 观察推导 → 读取装配 → `--check-coverage` → 纵向读取 |
| 2 | owner 文档 `shared/definitions/prompt-adherence-definitions.md` | T006, T007, T018 | 头部/目录/盲区/红线 → 读取契约节与 § Entry → 前提链与覆盖图 |
| 3 | 五个声明事实 `shared/declarations/facts/prompt-adherence-*.yaml` | T005 | 恰好五个，无第六事实 |
| 4 | 五个守卫家族（4 contract + 1 integration） | T004, T010, T019, T027, T030, T017, T023, T024 | declarations / engine（含后续扩写腿）/ owner / readonly / init |
| 5 | fixtures `tests/fixtures/prompt-adherence/` | T009 | 六行种子 + 层/强度变体 + 负种子 |
| 6 | 框架地图行 `shared/definitions/framework-map.md` | T008 | owner 文档行 + 读取入口行 |
| 7 | 镜像对（shared / scripts 投影） | T033 | 单次投影 + 无 NEW drift + 二次写入无变化 |
| 8 | 分发/init 接线（`specify init` 拷贝） | T024, T026 | fresh init 含机制、离线诚实读取 |
| 9 | quickstart 校验 | T034 | 六场景 + 传感器读取块 + 检查块（全量套件腿归 T038） |
| 10 | 证据记录 | T001, T002, T003, T016, T021, T022, T025, T026, T029, T031, T032, T035, T036, T037, T038, T039 | notes/ + test-evidence/ 的实测落盘 |
| 11 | 日期化基线读取（FR-026） | T031, T032 | feedback 条目 + 可重放读证 |

## Measured Premises (generation-time re-measurement, 2026-11-27)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 需求条目计数（FR / SC） | `grep -cE '^- \*\*FR-[0-9]+\*\*:' .specify/specs/109-prompt-adherence/requirements.md`；同法 `SC-` | **30 / 9** |
| 契约条款数（逐文件） | `grep -cE '^## C-[0-9]+' .specify/specs/109-prompt-adherence/contracts/*.contract.md` | owner-and-catalog **7** / declarations-and-vocabularies **7** / reading-semantics **10** / engine-and-read **5** / distribution **3** / guards-and-boundaries **7**；合计 **39**。**陷阱形**：`grep -ohE '\bC-[0-9]+\b' …/contracts/*.contract.md \| wc -l` → **46**（正文引用混入）；计量单位是行首 `## C-NNN` 定义行 |
| 交付路径当前状态 | 逐个 `test -e`（owner 文档、五个事实、引擎、五个守卫文件、fixtures 目录、两份 `.specify/` 镜像） | **15/15 ABSENT**（机制为新；红先前提） |
| 镜像 / 副本基线 | `python3 scripts/python/sync-mirrors.py --check`；`python3 scripts/python/regen-command-copies.py --check` | rc **0**（六对镜像字节一致，六投影 `ok`）；rc **0**（`OK: all per-tool command copies match the source templates.`） |
| 指令节计数基线 | `grep -c '^## ' templates/instructions-template.md`；同法 `.specify/instructions.md` | **39 / 40** |
| 存储根集合 | 经 `declaration_reader.load_fact(…, "runtime-store-layout")` 读 `statement.stores` | **14** 个 store；`any(root key)` = **False**；根为 `.specify/<store-name>/` 投影 |
| probe 注册表计数 | `python3 .specify/scripts/python/probe-utils.py --action probes --format json` | `available: true`；classes **11**；objects **130**（错误键缺席 = 0 error） |
| 六个读面在位 | 逐个 `grep -n` 函数定义 | `run-determination.py::load_determinations` :1170、`FINDINGS_PROJECTION_FIELDS` :210、`GREEN_UNPROVEN_VERDICT` :243；`exec-quant.py::load_records` :1124、`KIND` :147；`feedback-utils.py::scan_entries` :420、`entry_meta` :538；`evidence-utils.py::load_index` :138、`FINDINGS_KIND` :48、`SCHEMA_VERSION` :47；`probe-utils.py::load_probe_registry` :283；`declaration_reader.py::find_repo` :120 / `load_fact` :400；`confirmation-gates.md` :93 |
| 解释器与 pytest 解析 | `/usr/local/bin/python3 --version`；`/usr/local/bin/python3 -m pytest --version`；`python3 -m pytest --version` | **3.11.11**；**pytest 8.4.2**；PATH 的 `python3` → `No module named pytest`（`SPECKIT_PYTHON` 覆写是必需项） |
| 唯一入口可用性 | 带覆写与不带覆写各一次 `--collect-only -q` | 带 `SPECKIT_PYTHON` → `7 tests collected` exit 0；不带 → `error: no interpreter with pytest found` exit 1 |
| 既有守卫文件在位 | 逐个 `test -e`（runtime store layout / script interface / exec-quant / feedback / evidence / probe）与 init 模式文件 | **7/7 OK** |
| 框架地图与登记面在位 | `test -e`（`shared/definitions/framework-map.md`、`.specify/shared/definitions/framework-map.md`） | 两者 **OK** |
| Feature 109 注册状态 | `grep -n '\| 109 \|' .specify/features.md`；`grep -n '^\*\*Status\*\*' .specify/features/109-prompt-adherence.md` | 索引行 **Planned**；详情 **Planned** |

## Requirement Coverage Map

| FR | Rows | FR | Rows | FR | Rows |
|----|------|----|------|----|------|
| FR-001 | T006, T007, T021, T026 | FR-011 | T014, T015, T016 | FR-021 | T015, T024, T034 |
| FR-002 | T006, T021, T026 | FR-012 | T014, T015 | FR-022 | T011, T020, T022, T024 |
| FR-003 | T018, T019, T020, T021, T022 | FR-013 | T015, T016 | FR-023 | T011, T024, T034, T035 |
| FR-004 | T006, T017, T018 | FR-014 | T011, T015, T016 | FR-024 | T001, T004, T010, T017, T019, T023, T024, T025, T027, T030, T038 |
| FR-005 | T012, T013, T016 | FR-015 | T027, T028, T029 | FR-025 | T015, T030, T034 |
| FR-006 | T015, T023, T025, T027, T029, T030 | FR-016 | T014, T015, T016, T028 | FR-026 | T031, T032, T037 |
| FR-007 | T012, T013, T035 | FR-017 | T014, T015, T032 | FR-027 | T015, T031 |
| FR-008 | T031, T032 | FR-018 | T004, T005, T012, T016 | FR-028 | T006, T009, T013, T014, T021 |
| FR-009 | T014, T015, T021 | FR-019 | T006, T008, T012 | FR-029 | T006, T015, T021 |
| FR-010 | T010, T015 | FR-020 | T026, T033, T039 | FR-030 | T012, T016, T038 |

**SC coverage**: SC-001 → T010, T016, T034；SC-002 → T023, T025, T027, T029, T030；SC-003 → T009, T010；SC-004 → T018, T019, T020, T021, T022；SC-005 → T024, T026, T034；SC-006 → T010, T032；SC-007 → T004, T005, T016, T021；SC-008 → T031, T032, T037；SC-009 → T021, T026, T033, T038, T039。

**Coverage statement**: 每个功能需求 FR-001…FR-030 与每条成功判据 SC-001…SC-009 至少被一个任务行点名；SC-002 由多个行分面承担（创作、包含性收口、窗口运行、advisory 运行），无一行凭单面认领它；SC-004 与 SC-008 各有专用读数行，判据由一次运行取证、不由摘要取证。本表是 FR/SC 覆盖的唯一声明处；§ Clause Coverage & Green Partition 是条款分区的唯一声明处——两份分区互不复述。

## Clause Coverage & Green Partition

39 条款逐条恰认领一次；测试编写行不携带 `[green:]`，因此 `green-path-divergence` 为 0；每份契约内认领序号随行序单调，因此 `green-cross-phase` 为 0。

| Contract file | Clauses | Green row | Carrier |
|---------------|---------|-----------|---------|
| `contracts/owner-and-catalog.contract.md` | C-001…C-007（7） | T026 | owner 守卫在 T021 全绿；fresh-init 库存腿在 T026 补齐 C-001 的 init 面 |
| `contracts/declarations-and-vocabularies.contract.md` | C-010…C-016（7） | T016 | declarations 守卫的 read-point 与 emitted-token 腿 + engine 守卫 |
| `contracts/engine-and-read.contract.md` | C-030…C-032（3） | T016 | 引擎接口与六读面腿 |
| `contracts/engine-and-read.contract.md` | C-034, C-036（2） | T026 | init 的 socket-blocked 腿 + 双副本自定位腿 |
| `contracts/reading-semantics.contract.md` | C-020…C-029（10） | T034 | quickstart 场景 1–5 端到端实证 |
| `contracts/distribution.contract.md` | C-033, C-035（2） | T033 | 镜像投影 + 无 NEW drift + init 库存 + 基线条目 |
| `contracts/distribution.contract.md` | C-037（1） | T035 | 指令节计数不变读数 + 无命令/skill 面 |
| `contracts/guards-and-boundaries.contract.md` | C-040…C-046（7） | T038 | 终态树上的 GATE 复核 |

## Feature Integration Review

任务拆解复核（2026-11-27）：本拆解未暴露新 Feature，也未使既有 Feature 失效——11 个交付家族全部落在 Feature 109 的已登记范围内，存储根读取适配（A-5）是 109 自身的引擎行为而非独立能力。Feature 109 保持 `Planned`；本阶段不编辑 `.specify/features.md`、`.specify/features/109-prompt-adherence.md`、`.specify/register.md` 与 state spine。`Planned → Implemented` 是实现阶段的职责（T037，Pre-Status-Flip Gate）。

## Test Reading Slots

效率模型（`shared/guidelines/test-execution-efficiency.md`；098 的 tier 选择）要求读取槽被显式命名，且全量套件只读一次：

- **实现入口基线**（全量，1 次）：由 `/speckit.implement` 的 Step 0 捕获（`--names-out .specify/specs/109-prompt-adherence/baseline-failed.txt`；路径与 flag 归该 owner，本文件不复述）。本任务列表不重复该捕获。
- **定向集槽 T-S1**（T016）：declarations + engine 两个新文件。
- **定向集槽 T-S2**（T021）：owner + engine 两个文件。
- **定向集槽 T-S3**（T025）：readonly 守卫（按运行腿）。
- **定向集槽 T-S4**（T026）：init 守卫。
- **定向集槽 T-S5**（T029）：engine + readonly（纵向腿）。
- **定向集槽 T-S6**（T030）：engine + readonly（advisory-only 腿）。
- **定向集槽 T-S7**（T035）：既有 owner 顶守卫六文件。
- **全量读取槽 F-1**（T038，1 次）：唯一一次全量套件读取，在全部代码/测试/登记编辑之后；名称级对照基线。T039 不重跑全量（无 test-affecting 编辑）；若出现此类编辑，重取 T038 读数并替换记录。

## Phase 1: Setup（共享基础设施）

**Purpose**: 打开本特性的证据落点，并冻结后续每一行据以判断的测量值——先于任何源文件被触碰。

- [X] T001 Create the runtime-evidence landing points — `.specify/specs/109-prompt-adherence/notes/red-first-evidence.md`, `notes/quickstart-run.md`, `notes/pre-change-measurements.md` — each with a one-line purpose header; later rows append real output only, never summaries.
- [X] T002 [blockedBy: T001] Capture the pre-change measurements into `notes/pre-change-measurements.md`, each with its command and the ISO date 2026-11-27: (a) `python3 scripts/python/sync-mirrors.py --check` and `python3 scripts/python/regen-command-copies.py --check` exit codes — the no-NEW-drift baseline every later mirror claim is relative to; (b) existence checks over the 15 deliverable paths (owner document, five facts, engine, five guard files, fixtures directory, two installed mirrors) reporting ABSENT — the mechanism is new; (c) the clause count from `grep -cE '^## C-[0-9]+'` over `contracts/*.contract.md` (7/7/10/5/3/7 = 39), with the naive-reference trap recorded; (d) `grep -c '^## ' templates/instructions-template.md` and the same count on `.specify/instructions.md` — the section-count baseline for the no-new-section reading; (e) the store roster re-read through `declaration_reader.py` (14 stores, no per-store `root` key) and the probe-registry counts.
- [X] T003 [blockedBy: T002] Freeze the clause-coverage baseline: `python3 scripts/python/account-clause-coverage.py .specify/specs/109-prompt-adherence --freeze > .specify/specs/109-prompt-adherence/coverage-baseline.txt` (the accountant only prints; the redirect is the freeze), then record the frozen line count and the `files:` / `base-sha:` header fields in `notes/pre-change-measurements.md`.

**Checkpoint**: 后续每个「无 NEW drift」与「计数不变」声明都有编号在案的实测值，红先证据文件在第一次红运行之前已存在。

## Phase 2: Foundational（阻塞前置）

**Purpose**: 落 owner 文档、五个声明事实与框架地图登记——所有读取、覆盖检查与分发共同消费的那一层。任何用户故事都不在此之前开始。

**⚠️ CRITICAL**: T004 先写声明断言；T005 收口事实侧，T012 收口引擎读点侧。晚于其 subject 写就的绿色断言无法证明 subject 曾经缺席。

- [X] T004 Author `tests/contract/test_prompt_adherence_declarations.py` red-first: the five fact files exist with `shared/declarations/contract.yaml`'s required keys and `kind: closed-set`; membership equality per FR-018; cross-agreement between the owner document's catalog cells and the five sets in BOTH directions; the owner↔engine reason-taxonomy pin (three row-reason causes, four invalid-source causes); unknown-token rejection and the degradation exits; the declarations read-point locator (the engine references `declaration_reader` and each slug); and the no-sixth-fact leg for observation states (FR-018, FR-019, FR-024, SC-007). Every leg must fail on the missing facts, owner document or engine — never on an import error; record the red run in `notes/red-first-evidence.md`.
- [X] T005 [blockedBy: T004] Write the five declaration facts — `shared/declarations/facts/prompt-adherence-layers.yaml` (`host-prompt`, `project-rules`), `shared/declarations/facts/prompt-adherence-strengths.yaml` (`direct`, `indirect`), `shared/declarations/facts/prompt-adherence-signals.yaml` (the six row ids of FR-028), `shared/declarations/facts/prompt-adherence-deviation-classes.yaml` (`axis-regression`, `green-unproven`, `evidence-missing`), `shared/declarations/facts/prompt-adherence-reading-status.yaml` (`complete`, `partial`, `no-data`, `not-found`) — each carrying `fact`, `kind: closed-set`, `statement`, `consumers` naming `scripts/python/prompt-adherence.py`, and `former_carriers`, in the subset the declaration reader parses (FR-018).
- [X] T006 [blockedBy: T005] Author the owner-document head in `shared/definitions/prompt-adherence-definitions.md`: the self-declared single ownership (premise chain, two-layer model, catalog, reading-contract meanings, blind-spot register, red lines); the two-layer model with the `host-prompt` / `project-rules` bilingual definition sites and by-reference reaches to the harness disambiguation and the instructions-surface owner (FR-002); the machine-parsed catalog table carrying the six rows of FR-028 with every cell (record predicate, store and owning read surface, identity fields, timestamp field, layer, strength, allowed states, deviation classes) plus the admission-criteria section (FR-004, FR-028); the blind-spot register with the six classes of FR-029, each with its reason and capture direction, the `host-prompt-content` privacy red line and the `anomaly-line-persistence` boundary (FR-029).
- [X] T007 [P] [blockedBy: T006] Author the owner document's reading-contract and boundary sections in `shared/definitions/prompt-adherence-definitions.md`: per-run and longitudinal field meanings, the four-way state derivation, the three reason causes and four invalid-source causes with their meanings (the owner face of the pin), the status derivation, ordering / tie-break / duplicate / window semantics, the privacy rule, the red lines (feedback red lines referenced from their owner, never restated), and § Entry naming the one documented invocation (FR-014, FR-015, FR-016, FR-017, FR-021, FR-023, FR-025, FR-027).
- [X] T008 [P] [blockedBy: T006] Register two rows in `shared/definitions/framework-map.md`: one owner-document row and one reading-entry row naming `scripts/python/prompt-adherence.py` with its documented invocation — owner path, installed path and a one-line scope per row, imitating the existing rows' shape (FR-020).

**Checkpoint**: 该层已存在（owner 文档 + 五个事实 + 框架地图行），声明守卫已红先落地，所有故事都可读取目录与值域而非重新声明它们。

## Phase 3: User Story 1 - 一次诚实的按运行遵从读取 (Priority: P1) 🎯 MVP 之一

**Goal**: 一次文档化调用返回按运行读取——每个目录行一条观察，带证据状态、可解析源引用，以及在无可观察内容时的原因；不评分、不越证据推断、重跑相同。

**Independent Test**: 覆盖全部目录行的种子 fixture 产出预期读取；连续两次运行逐字段相同；删掉某行的记录后，恰好该行变成带原因的 `not_evaluated` 条目。

**Checkpoint**: 引擎在 fixtures 与本仓库上满足完整按运行契约，声明守卫的读点腿也转绿。

- [X] T009 [US1] Build the fixture store family under `tests/fixtures/prompt-adherence/`: a workspace-shaped fixture seeding at least one record for every one of the six catalog rows (a run-determination memory entry, exec-quant records, one non-gate feedback entry and one `gate:`-family entry, an evidence findings run, and a probe-registry declaration readable through `probe-utils.py`), plus the project-layer-only and indirect-only variants and the negative seeds (a broken source reference, a duplicate pair, an unparsable record, an unknown-schema-version record); every listed path existence-checked at authoring time (FR-028, SC-003).
- [X] T010 [US1] [blockedBy: T009] Author `tests/contract/test_prompt_adherence_engine.py` red-first — per-run legs: the bare invocation prints the reading with the resolved run identity and its basis and exactly one observation per catalog row in catalog order with resolvable source references; two consecutive runs are field-identical in both output forms; deleting one row's records turns exactly that row into `not_evaluated` with a reason; the recordless fixture emits `no-data` and an unmatched `--run` emits `not-found`, both exiting 0, while `--run` combined with a window exits 2; seeded invalid records and the broken reference surface in `invalid_sources` with counts and no crash; duplicates are disclosed; a prose-marker scan finds no raw user text; the project-layer-only fixture yields no host statement beyond `Unobserved` and the indirect-only fixture yields no layer-level verdict; no adherence verdict token, score or ranking appears; help/version answer and an undeclared option is rejected; a scratch `.specify/scripts/python/` copy and a framework-source copy each locate themselves correctly with the negative case asserted; no network module is imported (FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-016, FR-017, FR-021, FR-022, FR-024, FR-028). Record the red run in `notes/red-first-evidence.md`.
- [X] T011 [US1] [blockedBy: T010] Implement the engine skeleton and interface in `scripts/python/prompt-adherence.py`: one stdlib-only file; `-h` and `--help` with identical bodies (usage, options, side effects `none`, exit-code meanings); `--version` printing `<script-name> <framework-version>` re-derived from the nearest `pyproject.toml`; undeclared options rejected with exit 2 before any action, including after a bare `--`; the flags `--run`, `--since`, `--until`, `--json`, `--workspace-root`, `--check-coverage`; workspace resolution from `--workspace-root` else walking upward to the nearest ancestor holding `.specify/`; copy-level self-location firing only on a literal `.specify` component of its own resolved path (FR-022, FR-023).
- [X] T012 [US1] [blockedBy: T011] Implement the declaration, owner-document and store-layout reads in `scripts/python/prompt-adherence.py`: the five facts through `scripts/python/declaration_reader.py` (`find_repo` framework-source form first, `.specify/` mirror second); parse the owner document's catalog and blind-spot tables and validate every cell against the declaration sets — an unknown token aborts with exit 2 and no reading; read `shared/declarations/facts/runtime-store-layout.yaml#/statement` through `declaration_reader.py` and derive each non-registry row's root as the `.specify/<store-name>/` projection of its declared store name (no ported `store_layout.py`, no second root table; a row naming an undeclared store is a hard error, exit 2); stamp the declaration-set version as the SHA-256 over the five fact files (sorted repo-relative path plus bytes) computed at read time (FR-018, FR-019, FR-022, FR-030).
- [X] T013 [US1] [blockedBy: T012] Implement the six sensor reads in `scripts/python/prompt-adherence.py`, each through its owning engine's read surface in process (the `scripts/python/measure.py` importlib precedent), never a second parser: `run-determination.py` `load_determinations`, `exec-quant.py` `load_records`, `feedback-utils.py` `scan_entries` (frontmatter metadata only, both the ordinary and the `gate:` family), `evidence-utils.py` `load_index` plus the finding-item fields pinned against `FINDINGS_KIND` / `SCHEMA_VERSION` / `FINDINGS_PROJECTION_FIELDS`, and `probe-utils.py` `load_probe_registry` (FR-005, FR-028).
- [X] T014 [US1] [blockedBy: T013] Implement the observation derivation in `scripts/python/prompt-adherence.py`: each row's record predicate and identity joins on its declared fields; the positive-state caps (`Exercised`; `Wired` for the probe row); the three deviation-class derivations cited from the source engines' own verdict domains; the four-way absence derivation with the three reason causes; the four invalid-source causes; duplicate counting per the declared key; and source-reference ordering (FR-009, FR-011, FR-012, FR-017, FR-028).
- [X] T015 [US1] [blockedBy: T014] Implement the reading assembly in `scripts/python/prompt-adherence.py`: per-run scope (`--run` pinned; default = the most recent run identity observed across the catalog, selected by timestamp then store name then source path, with the basis printed; `no-data` / `not-found`), the status derivation, exactly one observation per row in catalog order, the mandatory coverage section (observable / not-observable / all six blind-spot classes / record and invalid counts), the `invalid_sources` and `duplicates` disclosures, privacy (structured fields only), the human-readable form and the `--json` form serialized with sorted keys from the same computed structure, no clock field anywhere, and no adherence verdict (FR-009, FR-010, FR-013, FR-014, FR-016, FR-021).
- [X] T016 [US1] [blockedBy: T015] Close Part A through the project runner: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_prompt_adherence_engine.py tests/contract/test_prompt_adherence_declarations.py -q` green (the declarations guard's read-point and emitted-token legs included); capture the fixture reading and the field-identical rerun in `notes/red-first-evidence.md` (SC-001, SC-007) [green: contracts/declarations-and-vocabularies.contract.md#C-010] [green: contracts/declarations-and-vocabularies.contract.md#C-011] [green: contracts/declarations-and-vocabularies.contract.md#C-012] [green: contracts/declarations-and-vocabularies.contract.md#C-013] [green: contracts/declarations-and-vocabularies.contract.md#C-014] [green: contracts/declarations-and-vocabularies.contract.md#C-015] [green: contracts/declarations-and-vocabularies.contract.md#C-016] [green: contracts/engine-and-read.contract.md#C-030] [green: contracts/engine-and-read.contract.md#C-031] [green: contracts/engine-and-read.contract.md#C-032].

## Phase 4: User Story 2 - 前提被审查、盲区被点名 (Priority: P1) 🎯 MVP 之二

**Goal**: owner 文档把前提链分解为具名假定行为，每条映射到恰好一个目录行或恰好一个盲区条目；机器检查双向执行该映射，使一个假定无法悄悄算作成立。

**Independent Test**: `--check-coverage` 对 owner 文档退出 0 零发现；篡改副本点名悬空目标并退出 1；不可读的 owner 文档退出 2。

**Checkpoint**: 前提审查机器可检，且每个盲区在每次读取的覆盖节中以不可观察出现。

- [X] T017 [US2] [blockedBy: T008] Author `tests/contract/test_prompt_adherence_owner.py` red-first: owner existence and self-declared ownership; the bilingual layer tokens; the catalog table cells resolvable against the declaration sets; the blind-spot register entries carrying reason and capture direction; the coverage-map two-way legs (every assumed behavior to exactly one target kind and one target; every sensor target to a catalog row id; every catalog row cited; every register id cited); the framework-map rows; and the red-line legs (FR-001, FR-002, FR-003, FR-004, FR-028, FR-029, SC-004). Fails on the missing coverage map, never on an import error; record the red run in `notes/red-first-evidence.md`.
- [X] T018 [US2] [blockedBy: T017] Author the premise chain and the coverage map in `shared/definitions/prompt-adherence-definitions.md`: twelve named assumed behaviors, dense in document order, each mapping to exactly one catalog row (sensor side) or exactly one blind-spot id, as the machine-parsed coverage-map table (FR-003).
- [X] T019 [US2] [blockedBy: T018] Extend `tests/contract/test_prompt_adherence_engine.py` red-first with the `--check-coverage` legs: clean exit 0 with zero findings on the delivered owner document; a doctored copy in a sanctioned scratch root (a dangling row id, an unresolved target) exiting 1 with the finding named; an unreadable owner document exiting 2 (FR-003, FR-022). Record the red run in `notes/red-first-evidence.md`.
- [X] T020 [US2] [blockedBy: T019] Implement the `--check-coverage` action in `scripts/python/prompt-adherence.py`: parse the coverage map and enforce assumed-behavior uniqueness, single target kind plus single target, target resolution against the catalog rows and the register, full row coverage and full register coverage; exit 0 with zero findings, 1 with the sorted finding list, 2 on an unreadable owner document (FR-003, FR-022).
- [X] T021 [US2] [blockedBy: T017,T020] Close the owner guard through the project runner: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_prompt_adherence_owner.py tests/contract/test_prompt_adherence_engine.py -q` green; record the output in `notes/red-first-evidence.md` (FR-001, FR-002, FR-003, FR-004, FR-028, FR-029).
- [X] T022 [US2] [blockedBy: T021] Take SC-004's reading: run `python3 scripts/python/prompt-adherence.py --check-coverage` on the delivered owner document and capture exit 0 with zero findings, then the doctored copy's exit 1 with its sorted findings, in `notes/red-first-evidence.md` (SC-004).

## Phase 5: User Story 3 - 客户项目在本地、离线、无新存储地读取遵从度 (Priority: P1) 🎯 MVP 之三

**Goal**: 文档化调用在刚初始化的项目里工作——读取本地存储、不写文件、不访问网络、不复现原始用户文本，并在记录尚不存在处明确说明。

**Independent Test**: 刚初始化且无记录的项目在 socket-blocked 解释器下以显式 `not_evaluated` 行完成；有数据的 fixture 产出完整读取；受管存储根的哈希清单在读取前后不变。

**Checkpoint**: 分发（fresh init）与包含性/隐私由 fixture 经项目 runner 证明，而非断言。

- [X] T023 [P] [US3] [blockedBy: T016] Author `tests/contract/test_prompt_adherence_readonly.py` against the delivered engine — a declared regression guard over behavior already delivered: the baseline hash manifest is captured by the test itself immediately before each reading invocation in the same working tree (path, SHA-256 of bytes, size per file); the comparison unit is every file under the roots derived from `shared/declarations/facts/runtime-store-layout.yaml#/statement` through `declaration_reader.py` (one `.specify/<store-name>/` root per declared store) plus the root path sets themselves; the allowed diff set is none, and the complement assertions run after a per-run reading (the longitudinal leg lands red-first with T027); interpreter bytecode caches are excluded by name; determinism is judged separately by run-A/run-B equality and never cited as containment evidence (FR-006, FR-024, SC-002). Record the authored run in `test-evidence/us3-red-readonly.txt`.
- [X] T024 [P] [US3] [blockedBy: T016] Author `tests/integration/test_prompt_adherence_init.py` — a declared regression guard with its mirror-independent initial form: a fresh project initialized from this repository's framework sources (the `copy_local_templates` + `get_resource_path` monkeypatch pattern, with the fresh-init subprocess form of `tests/integration/test_init_new_layout.py`) contains the owner document, the five facts and the engine under `.specify/`; the installed entry answers `--version`; the bare invocation on the recordless project emits explicit `not_evaluated` / `Unobserved` lines with exit 0 under a socket-blocked interpreter; no instructions section and no `/speckit.*` command or skill surface exists for this feature; the inventory-only scope of C-037 is asserted (FR-020, FR-021, FR-022, FR-023, SC-005, SC-009). Record the authored run in `test-evidence/us3-red-init.txt`.
- [X] T025 [US3] [blockedBy: T023] Close the per-run containment guard: confirm the engine has zero write points (no file opened for writing, no directory created, no cache or lock), run the per-run reading inside the guard, `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_prompt_adherence_readonly.py -q` green, and record the before/after manifest counts in `notes/red-first-evidence.md` (FR-006, SC-002).
- [X] T026 [US3] [blockedBy: T024] Close the init fixture through the project runner and record its real output in `notes/red-first-evidence.md`: the fresh-project absence lines, the offline socket-blocked run, and the installed copy's `--version` (FR-020, FR-021, SC-005) [green: contracts/owner-and-catalog.contract.md#C-001] [green: contracts/owner-and-catalog.contract.md#C-002] [green: contracts/owner-and-catalog.contract.md#C-003] [green: contracts/owner-and-catalog.contract.md#C-004] [green: contracts/owner-and-catalog.contract.md#C-005] [green: contracts/owner-and-catalog.contract.md#C-006] [green: contracts/owner-and-catalog.contract.md#C-007] [green: contracts/engine-and-read.contract.md#C-034] [green: contracts/engine-and-read.contract.md#C-036].

## Phase 6: User Story 4 - 读时重建的纵向读取 (Priority: P2)

**Goal**: 显式窗口产出每个目录行的状态计数加覆盖行——每条记录自身时间戳上的半开边界、省略边界打印为 `open`、输出有界、零持久化。

**Independent Test**: 多次运行的 fixture 对给定窗口产出预期计数；两个相交窗口仅在边界不同处不同；两次运行后存储树不变。

**Checkpoint**: 窗口读取在按运行路径之上组合、不新增存储，其边界算术机器可检。

- [ ] T027 [US4] [blockedBy: T016] Extend `tests/contract/test_prompt_adherence_engine.py` and `tests/contract/test_prompt_adherence_readonly.py` with the longitudinal legs, red-first: a multi-run fixture yields per-row counts by evidence state; a window boundary falling exactly on a record timestamp follows the half-open rule; an omitted bound prints as the literal `open` and both bounds appear; the probe row evaluates once and is marked window-exempt; `--since` / `--until` accept `YYYY-MM-DD` and `YYYY-MM-DDTHH:MM:SSZ` while an invalid value exits 2; no per-project, per-agent or per-user ranking appears; the containment complement assertions run after the longitudinal reading too (FR-006, FR-015, FR-016). Record the red run in `notes/red-first-evidence.md`.
- [ ] T028 [US4] [blockedBy: T027] Implement the longitudinal reading in `scripts/python/prompt-adherence.py`: window parsing and validation, half-open `[since, until)` comparison against each record's own declared timestamp field, the `open` literal, per-row state counts in catalog order, the window-exempt declaration-row note, and the output caps (per-observation sources 20, invalid sources 50, duplicates 20, each with a truncation disclosure and a total count) (FR-015, FR-016).
- [ ] T029 [US4] [blockedBy: T028] Capture the window readings in `notes/red-first-evidence.md`: the multi-run fixture's counts; two overlapping windows differing only where their bounds differ; the store tree unchanged after both runs (FR-015, SC-002).

## Phase 7: User Story 5 - 负面读数只做咨询、进入既有流程 (Priority: P3)

**Goal**: 报告负面观察的读取不改变任何东西、也不授权任何行动；值得保留的读取经既有 feedback 渠道落为一条日期化记录，可凭其源引用重放。

**Independent Test**: 产生负面观察的 fixture 在读取后存储树不变；经既有 feedback 引擎的显式跟进创建一条普通条目，源引用完整；任何地方都不出现新的存储根或聚合。

**Checkpoint**: advisory 边界机器可检，日期化基线经既有渠道存在，audit replay 解析每条引用。

- [ ] T030 [US5] [blockedBy: T029] Extend the engine and read-only guards with the advisory-only legs — a declared regression exception over behavior delivered in US1 through US4, whose red-capability is the seeded negative observation: a fixture yielding a deviation-class observation leaves the store tree unchanged and produces no automatic disposition, threshold or mutation; no new aggregate or store root appears; the complete negative vocabulary is exactly the three deviation classes plus the absence states, with no verdict token anywhere (FR-008, FR-025, SC-002). Record the run in `notes/red-first-evidence.md`.
- [ ] T031 [US5] [blockedBy: T030] Produce the dated baseline reading through the existing channel: run the default-scope reading and its `--json` form on this repository, then record exactly one feedback entry via `python3 scripts/python/feedback-utils.py --action record --unit-id /speckit.implement --unit-type command --run-id <implement-run-id> --feature 109-prompt-adherence --feature-id 109` carrying the reading's status, per-row states, declaration-set digest and source references; the entry stays replayable by one engine run against its citations, creates no aggregate, and its target is the framework itself (FR-008, FR-026, FR-027, SC-008).
- [ ] T032 [US5] [blockedBy: T031] Take SC-006's audit-replay reading: mechanically resolve every observation's source references from the fixture reading and from the baseline entry — every positive observation resolves from its citations alone, and the seeded broken reference appears as an invalid source, never skipped; record both in `notes/red-first-evidence.md` (FR-017, SC-006).

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: 取特性级读数、证明边界未移动、闭合运行——不在此落地新机制。

- [ ] T033 [blockedBy: T032] Execute and verify the plan's Mirror Obligations table: run `python3 scripts/python/sync-mirrors.py --write` (the single projection, after every framework-source edit has landed), then `--check` — every pair this spec touches is byte-identical with no NEW drift against `notes/pre-change-measurements.md` (the owner document, `framework-map.md`, the five facts, the engine); run the second write and confirm it changes nothing; confirm both engine copies answer `--version` and that no `.specify/` mirror was hand-edited (FR-020, SC-009) [green: contracts/distribution.contract.md#C-033] [green: contracts/distribution.contract.md#C-035].
- [ ] T034 [P] [blockedBy: T033] Execute every scenario in `.specify/specs/109-prompt-adherence/quickstart.md` exactly as written (Scenarios 1–6 plus the sensor-read block and the check block's mirror/copy legs), and record each real output with its teardown steps in `notes/quickstart-run.md`; the check block's full-suite line is executed once at T038 (slot F-1), not re-run here; a premise that no longer holds is recorded as a reading against that premise and reported to the plan owner — the quickstart is plan-owned and is never rewritten from this stage (SC-001, SC-005, SC-009) [green: contracts/reading-semantics.contract.md#C-020] [green: contracts/reading-semantics.contract.md#C-021] [green: contracts/reading-semantics.contract.md#C-022] [green: contracts/reading-semantics.contract.md#C-023] [green: contracts/reading-semantics.contract.md#C-024] [green: contracts/reading-semantics.contract.md#C-025] [green: contracts/reading-semantics.contract.md#C-026] [green: contracts/reading-semantics.contract.md#C-027] [green: contracts/reading-semantics.contract.md#C-028] [green: contracts/reading-semantics.contract.md#C-029].
- [ ] T035 [P] [blockedBy: T033] Take the boundary readings: `python3 scripts/python/harness-triple-check.py --action verify` is clean for the five `prompt-adherence-*` slugs; `python3 scripts/python/script-interface-check.py --files scripts/python/prompt-adherence.py,.specify/scripts/python/prompt-adherence.py --json` reports zero violations; the section count in `templates/instructions-template.md` and `.specify/instructions.md` is unchanged against `notes/pre-change-measurements.md`; no `/speckit.*` command or skill directory ships; and the existing owner guards stay green — `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_runtime_store_layout.py tests/contract/test_script_interface_contract.py tests/contract/test_exec_quant_engine.py tests/contract/test_feedback_utils_cli.py tests/contract/test_evidence_findings_schema.py tests/contract/test_probe_registry_umbrella.py -q` — record the outputs in `test-evidence/boundary-readings.txt` (FR-007, FR-019, FR-023, SC-009) [green: contracts/distribution.contract.md#C-037].
- [ ] T036 [blockedBy: T006] Register the three proposed glossary terms — 提示遵从度（Prompt Adherence）、宿主提示层（Host Prompt Layer）、项目规则文件层（Project Rule File Layer） — as `origin=auto` / `status=proposed` through `python3 scripts/python/glossary-utils.py --action add`, and record the engine's verdict in `notes/red-first-evidence.md` (requirements A-14; no new store, no schema change).
- [ ] T037 [blockedBy: T034,T035,T036] Write `.specify/specs/109-prompt-adherence/verification.md`: one `SC-NNN_status=` line per success criterion, `deferred_tasks=`, the smoke record fields, the SC-004 / SC-008 evidence pointers, and the documentation evaluation's outcome (the plan changes no `docs/` file, so a page lands only if the evaluation names one); flip Feature 109 `Planned` → `Implemented` under the Pre-Status-Flip Gate with the `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/109-prompt-adherence` verdict recorded (FR-026, SC-008).
- [ ] T038 [blockedBy: T037] Re-validate GATE-1…GATE-8 against the current tree and record each check's command and real output in `.specify/specs/109-prompt-adherence/test-evidence/implementation-gates.txt`; this row carries the single full-suite reading slot F-1: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh --names-out .specify/specs/109-prompt-adherence/final-failed.txt` followed by `comm -13 .specify/specs/109-prompt-adherence/baseline-failed.txt .specify/specs/109-prompt-adherence/final-failed.txt` printing nothing (zero NEW failed names; the baseline's capture and comparison form are owned by the implement skill's Test runs rule) (FR-024, SC-009) [green: contracts/guards-and-boundaries.contract.md#C-040] [green: contracts/guards-and-boundaries.contract.md#C-041] [green: contracts/guards-and-boundaries.contract.md#C-042] [green: contracts/guards-and-boundaries.contract.md#C-043] [green: contracts/guards-and-boundaries.contract.md#C-044] [green: contracts/guards-and-boundaries.contract.md#C-045] [green: contracts/guards-and-boundaries.contract.md#C-046].
- [ ] T039 [blockedBy: T038] Final structural re-run after the closure edits: `python3 scripts/python/sync-mirrors.py --check`, `python3 scripts/python/validate-tasks.py .specify/specs/109-prompt-adherence/tasks.md`, and `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/109-prompt-adherence --stage tasks --repo .`; record the outputs in `test-evidence/implementation-gates.txt`; the full suite is not re-run here because no test-affecting path changed after T038 — if one did, the T038 reading is re-taken and replaces its record (FR-024, SC-009).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，可立即开始。
- **Foundational (Phase 2)**: 依赖 Setup，阻塞所有用户故事。五个事实先于 owner 文档落地（目录单元按它校验），owner 文档先于任何读取其表格的行。
- **User Stories (Phases 3–7)**: 全部依赖 Foundational。US1 建引擎；US2 在同一文件上加 `--check-coverage`；US3 证明分发、包含性与隐私；US4 加纵向读取；US5 闭合 advisory 回路并落基线。
- **Polish (Phase 8)**: 依赖全部源编辑落地——T033 投影镜像，T034–T039 度量整个特性。

### User Story Dependencies

- **US1（P1，MVP 之一）**: Foundational 之后，不依赖其它故事。
- **US2（P1，MVP 之二）**: 依赖 US1 的引擎骨架（`--check-coverage` 动作在同一文件）；覆盖图是 owner 文档的新节，不是第二份文档。
- **US3（P1，MVP 之三）**: 其守卫在 US1 之后创作；其绿依赖引擎（US1）与 owner 文档（fresh-project 缺席行不依赖 US2 的覆盖图）。
- **US4（P2）**: 依赖 US1 的读取装配——窗口路径在其上组合、不新增存储。
- **US5（P3）**: 依赖 US4，因为 advisory-only 腿与基线运行要演练两种读取形态。

### Within Each User Story

- 测试先于使其转绿的实现行；两处既有行为守卫（T023/T024、T030）按 migration/regression 例外置于实现之后，并在行内声明。
- US1：fixtures 先于测试文件；测试文件先于引擎行（接口 → 声明/布局读取 → 六传感器 → 观察推导 → 装配 → 收口）。
- US2：owner 守卫先于覆盖图；覆盖图先于 `--check-coverage` 腿；腿先于动作实现；动作先于 SC-004 读数。
- US3：两个守卫文件并行创作（写目标不同），随后各自收口。
- US4/US5：测试腿先于其引擎行；每个证据行在其所记录的运行之后。
- 每个 `[blockedBy:]` 只指向更早的任务；无标签时按阶段顺序执行。

### Parallel Opportunities

- T007 ∥ T008：owner 文档的契约节与框架地图行写不同文件。
- T023 ∥ T024：两个 US3 守卫文件互斥，红先证据落不同 sink。
- T034 ∥ T035：quickstart 实录与边界读数写不同文件。
- 无 US1 行带 `[P]`：它们或写同一引擎文件、或写同一测试文件，按行序串行。

---

## Parallel Example: Phase 2 and Phase 5

```bash
# Phase 2 — owner 文档契约节与框架地图登记（不同文件）：
Task: "Author the owner document's reading-contract and boundary sections in shared/definitions/prompt-adherence-definitions.md"
Task: "Register two rows in shared/definitions/framework-map.md"

# Phase 5 — 两个 US3 守卫（不同文件、不同红先 sink）：
Task: "Author tests/contract/test_prompt_adherence_readonly.py"
Task: "Author tests/integration/test_prompt_adherence_init.py"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 + US2 + US3——三个 P1 故事只有合在一起才构成一个独立有价值的增量：没有前提审查的读取无法完成本特性的核心目的（未被观察的行为必须被点名，而不是被误当成成立的前提）；没有分发，机制永远到不了客户项目，而那正是特性的申明目标。三个检查点各自可独立测试。

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational（CRITICAL — 阻塞所有故事）.
3. Complete US1 → US2 → US3 in order; stop at each checkpoint and validate it independently.
4. Then US4（纵向）→ US5（advisory 回路与基线）.
5. Polish: 特性级读数、镜像投影、收口记录与终态门复核.

### Incremental Delivery

1. Setup + Foundational → 该层存在；后续故事读取它而非重新声明。
2. US1 → 按运行读取在 fixtures 与本仓库上工作（MVP 核心）。
3. US2 → 前提审查机器可检。
4. US3 → 机制可分发、可包含、可离线。
5. US4 → 纵向视图在按运行路径上组合。
6. US5 → 基线经既有渠道落盘、可凭引用重放。
7. Polish → quickstart 实录、镜像收敛、`verification.md` 与 GATE 终态复核。

### Parallel Team Strategy

单执行体（本线 `single-unit`）。若后续拆并行：仅 T007/T008、T023/T024、T034/T035 三组行可分组并行；引擎、各测试文件与 notes 汇总面永不由两个执行体同时写。

---

## Notes

- **PLAN-EDIT**: 无。本文件未改动任何 plan-owned 路径；contracts、quickstart、data-model、research、feature-ref、requirements 只被引用，不被编辑。实现期间如需对 plan-owned 路径做实质变更，按 stage 规则回抛 `ANOMALY`。
- **无新机制**: 零新 store、采集点、记录 schema、评分、命令、skill 或 instructions 节；feedback / run-determination / evidence / probe / measure 的所有者被读取、不被编辑（T035 证明）。
- **Two Hats**: 每一处编辑落在框架源（`shared/`、`scripts/`、`tests/`）；`.specify/shared/` 与 `.specify/scripts/` 副本只经 T033 的投影到达——手改镜像即使让树看起来更绿也是缺陷。
- **绿点分区**: 39 条款恰一次认领（T016 / T026 / T033 / T034 / T035 / T038）；测试编写行不携带 `[green:]`；各契约内认领序号随行序单调，故四项 green 检查零 WARN。
- **红先与回归例外**: 新行为守卫（T004、T010、T017、T019、T027）先于其实现；T023/T024（包含性与 init）与 T030（advisory-only）守的是既有交付行为，按 migration/regression 例外置于实现之后，行内已声明。
- **测量陷阱**: 条款计数单位是行首 `## C-NNN` 定义行（正文引用会把 39 读成 46）；解释器解析必须带 `SPECKIT_PYTHON=/usr/local/bin/python3`（PATH 的 `python3` 无 pytest、本工作树无 `.venv`）。
- **测试预算**: 定向集槽 T-S1…T-S7 按阶段收口，全量套件只走槽 F-1（T038）一次；不缩小选择、不跳过、不以重跑到绿。
- **Deferrals**: 无 `[~]` 行——本拆解中每个交付家族都有认领行；requirements A-14 的三条词汇提案由 T036 经既有 glossary 引擎登记，不推迟。
- **前提重测而非继承**: 本文件引用的每个计数与文件存在性前提都在 § Measured Premises 带命令与 2026-11-27 的实测输出；未被执行的再推导命令只是声明，不是测量。