# Tasks: Team View Degradation Hardening — 真实团队定义下的诚实呈现与降级语义

**Requirement ID**: 108
**Requirement Key**: `108-team-view-degradation`
**Related Feature**: 108 Team View Degradation（切片）→ 父 Feature 027 Team Management（`.specify/features.md` 行 108 当前 `Planned`；父 027 保持 `Ready for Review`；tasks 阶段不推进生命周期、不改 registry）
**Input**: Design documents from `.specify/specs/108-team-view-degradation/`
**Prerequisites**: plan.md（Technical Context / Mirror Obligations / Execution Premises EP-001…EP-009）、requirements.md（25 FR / 8 SC / 3 STR / A-1…A-17 / US1…US3）、research.md（M1–M8 / R-1…R-15）、data-model.md（C1–C10 实体与 10 条不变式）、contracts/ ×4（35 条款：C-101…C-109 / C-201…C-208 / C-301…C-309 / C-401…C-409）、quickstart.md（S-0…S-7）、feature-ref.md

**Tests Mode**: ON（Constitution Principle IV "Test-First & Contract-Driven Implementation" 是测试强制原则；本特性交付一个读取引擎、技能/文档措辞与三支新测试文件，测试形态为 unit / contract / integration 运行时测试。新行为测试一律红先；两处守既有行为的回归守卫（健康保真、只读快照）按 migration/regression 例外置于实现之后，并在行内声明。）

**Tests**: 红先证据的唯一落点 `.specify/specs/108-team-view-degradation/notes/red-first-evidence.md`（每条：命令、真实输出、退出码）。失败 nodeid 名集的捕获与比较形式归 `/speckit.implement` 的 `**Test runs**` owner，本文件只引用、不复述其路径与 flag。测试唯一入口 `scripts/bash/run-tests.sh`；interpreter 固定在 § Environment Prerequisites。

**Organization**: 按用户故事组织——US1（真实运行历史不被读丢：报告识别、最新选择与残留，P1）、US2（降级团队被诚实呈现并给出受制裁修复路径，P1）、US3（降级语义封闭、可测，健康输出保持不变，P2）。US1 独立构成最小可交付增量；US2 是紧随其后的 P1 增量；US3 的封闭集、三面一致与健康保真依赖前两者落地后转绿。

## Definition of Done (DoD)

- DoD-1: 全部任务行为 `[X]`；若出现 `[~]`，其理由逐条记录在 `.specify/specs/108-team-view-degradation/test-evidence/verification-input.md` 的 `deferred_tasks=`（`verification.md` 由 spec 侧从该输入派生）。
- DoD-2: 交付面齐备——单一读取引擎修订 `scripts/python/team-view.py`、`docs/reference/commands/team.md` 的 View Mode、`skills/internal/view-team/SKILL.md` 的错误导航与增补呈现措辞、三支新测试文件（`tests/unit/test_team_view_report_recognition.py`、`tests/contract/test_team_view_degradation_contract.py`、`tests/integration/test_team_view_degradation.py`）与镜像再生成；零新增第三方依赖、零新增读取器/存储/缓存/快照/索引/registry。
- DoD-3: 覆盖如实记账——FR 25/25、SC 8/8 以 § Requirement Coverage Map 为权威；4 份契约共 35 条款由 § Clause Coverage & Green Partition 逐条恰好认领一次；`validate-tasks.py` 的四项 green 检查零 ERROR，WARN 逐条裁定并记录在 `test-evidence/tasks-validator.txt`。
- DoD-4: 红先证据完整——每条新行为测试在其 subject 落地前经唯一入口执行并失败，命令、真实输出与退出码记录在 `notes/red-first-evidence.md`；两处回归守卫（T020 的健康保真与只读快照）按行内声明的例外置于实现之后。
- DoD-5: 封闭集可测——降级原因 2/2 映射退出码 5、退出码闭集 `0/2/3/4/5` 不变、渲染标签相对 `contracts/view-labels.contract.md` 双向闭包、报告识别/最新选择入口唯一、三面（docs / skill / 程序声明）一致，均由契约测试钉住。
- DoD-6: 健康保真与只读——基线提交 `54c6efa8c` 的程序与变更后程序在同一健康谓词 fixture 上 stdout 逐字节相同、退出码相同（机器 diff 行数 = 0）；healthy / degraded / overview 三个场景调用前后 fixture 工作树内容哈希一致。
- DoD-7: 无形态变更、无迁移——报告命名 owner（`skills/internal/create-team/SKILL.md` § Report contract）与 `team.md` schema 相对基线逐字节未变，既有团队零迁移，紧凑命名报告仍是运行报告。
- DoD-8: `.specify/specs/108-team-view-degradation/test-evidence/verification-input.md`（crew 可写的收口输入）逐条记录 SC-001…SC-008 的状态、命令、值与证据指针；`final` 路径判据 SC-001…SC-004 记 `pass`，且一条 smoke 记录齐备（`smoke_command=`、`smoke_exit_code=0`、存在且非空的 `smoke_evidence_path=`）；`verification.md` 由 spec 侧从该输入派生，crew MUST NOT 直接写（handoff/team 禁止面）。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/108-team-view-degradation/tasks.md` exit 0（0 error；WARN 逐条裁定并记录）。
- GATE-2: 跨产物一致 — check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/108-team-view-degradation --stage tasks --repo .` 输出 `decision=pass` 且 errors=0（advisory 逐条裁定）。
- GATE-3: FR / SC / 条款覆盖 — check: 本文件 § Requirement Coverage Map 为 25/25 与 8/8，§ Clause Coverage & Green Partition 的 35 条款逐条恰认领一次；`validate-tasks.py` 的 `green-dangling` / `green-clause-collision` / `green-cross-phase` / `green-path-divergence` 零 ERROR。
- GATE-4: final 路径成功判据 + smoke 记录 — check: `verification.md`（spec 侧从 `test-evidence/verification-input.md` 派生，crew 不写该文件）中 `**Path**` 为 `final` 的 SC-001…SC-004 全部 `pass`，且 `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`（存在且非空）齐备（条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates）。
- GATE-5: 镜像与副本收敛 — check: `python3 scripts/python/sync-mirrors.py --check` 的漂移成员集相对 `test-evidence/sync-mirrors-baseline.txt` 无新增成员；`python3 scripts/python/regen-command-copies.py --check` exit 0；`scripts/python/team-view.py` ↔ `.specify/scripts/python/team-view.py`、`skills/internal/view-team/SKILL.md` ↔ `.specify/skills/internal/view-team/SKILL.md` 两对字节一致。
- GATE-6: 封闭集与单一引擎 — check: `tests/contract/test_team_view_degradation_contract.py` 全绿（原因集、退出码映射、信封键、单一识别入口、标签闭包、三面一致）；`git diff --stat <baseline_commit>..HEAD` 对 `scripts/python/goal-utils.py` 为空。
- GATE-7: 健康保真与只读 — check: run `tests/integration/test_team_view_degradation.py` 通过，且健康保真测试的 stdout diff 行数 = 0、退出码相同，只读快照测试的新增/修改/删除文件数 = 0。
- GATE-8: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/108-team-view-degradation/tasks.md` 返回 0。

## Environment Prerequisites

- CPython `>=3.8`: **available** — probe: `/usr/local/bin/python3 --version` → `Python 3.11.11` @ 2026-11-26；affected: 全部实现行与测试行。
- pytest: **available** — probe: `/usr/local/bin/python3 -m pytest --version` → `pytest 8.4.2` @ 2026-11-26；约束：PATH 上的 `python3` 解析到 `/storage/project/profiles/.venv/bin/python3` 且 **import no pytest**（probe 输出 `No module named pytest`），因此全部测试行 MUST 经唯一入口 `scripts/bash/run-tests.sh` 并传入 `SPECKIT_PYTHON=/usr/local/bin/python3`；affected: 全部测试行。
- bash / git: **available** — probe: `bash --version` → `4.4.20(1)-release`；`git --version` → `2.43.5` @ 2026-11-26；affected: 唯一测试入口、镜像 / 副本、基线对象与保真行。
- 容器运行时 / 镜像仓库 / 活集群 / 外网: **none** — 本特性全部检查为本地文件、`git`、本地 pytest 与既有只读引擎，无构建、无拉取、无网络、无守护进程 @ 2026-11-26；affected: none。

**A13 boundary**（owner: `shared/workflow/acceptance-hardening.md` § Gates — 本注为指针，不是第二规则）：本节只记录任务生成期的探针结论（探测命令 + ISO 日期）；规划期承重前提归 `plan.md` § Execution Premises，依赖特性继承记录归 `plan.md` § Inherited Blockers。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标逐行不同、无未完成依赖）。本文件的 `[P]` 只出现在测试编写行：T006 / T007、T019 / T020；其余行因共享同一引擎、同一测试文件或同一证据 sink 而按行序串行。
- **[Story]**: 用户故事标签（`[US1]`…`[US3]`），只出现在用户故事阶段的任务行；Setup / Polish 阶段零故事标记。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全 `[X]` 前不得开始本行。仅阶段顺序关系时不写。
- **[green: <contract>#<clause>]**: 绿点认领——本行是该条款在本特性重新转绿的那一行；契约路径相对本文件目录解析。**35 条款分区**：report-recognition C-201…C-207 → T012、C-208 → T018；presentation C-301…C-309 → T018；team-view-program C-101…C-109 → T025；view-labels C-401…C-409 → T025。每条恰一行认领，认领行序与条款序号单调一致；测试编写行不携带 `[green:]`，故无 `green-path-divergence`。
- 每行必须单行完成（含文件路径与全部标签），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `test-evidence/verification-input.md` 的 `deferred_tasks=`、由 spec 侧派生进 `verification.md`，并在行内加 `<!-- deferred: <reason> -->`）。

## Path Conventions

- **框架源（编辑面）**: `scripts/python/team-view.py`、`skills/internal/view-team/SKILL.md`、`docs/reference/commands/team.md`、`tests/**`。
- **生成面（MUST NOT 手改）**: `.specify/scripts/python/team-view.py`、`.specify/skills/internal/view-team/SKILL.md`（由 `sync-mirrors.py` 投影）；每工具命令副本（由 `regen-command-copies.py` 生成）。
- **证据落点（本特性）**: `.specify/specs/108-team-view-degradation/notes/{pre-change-measurements.md,red-first-evidence.md,us1-green.txt,us2-green.txt,us3-green.txt,quickstart-run.md}`、`test-evidence/{implement-entry-readings.txt,us1-red-unit.txt,us1-red-integration.txt,us2-red-degraded.txt,us2-red-states.txt,us3-red-contract.txt,us3-guards.txt,tasks-validator.txt,targeted-set.txt,shape-change-guard.txt}`、`coverage-baseline.txt`、`test-evidence/verification-input.md`（crew 收口输入；`verification.md` 由 spec 侧派生）。
- **只读面（零修改）**: `.specify/specs/108-team-view-degradation/{plan.md,data-model.md,contracts/,research.md,quickstart.md,feature-ref.md}`（plan-owned，仅小修须 `PLAN-EDIT:` 声明）；`.specify/teams/**`（团队档案永不改写）；其它规格的 `.specify/specs/**`（103 的 data-model 与 program contract 作为日期化记录保留）、`.specify/features.md`、`.specify/register.md` 与 state spine（本阶段零编辑）。
- **共享写入面（串行）**: `scripts/python/team-view.py`（每个实现行依次追加）、`tests/integration/test_team_view_degradation.py`（三个故事分段追加）、`notes/red-first-evidence.md`（各验证行汇总）。

## Measured Premises (re-measured at generation time 2026-11-26, HEAD `679301b65`)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 需求条目计数（FR / SC / STR） | `grep -cE '^\- \*\*FR-[0-9]+\*\*:' .specify/specs/108-team-view-degradation/requirements.md`；同法 `SC-`；`grep -cE '^\| \`STR-[0-9]+\`' …/requirements.md` | **25 / 8 / 3** |
| 契约条款数（逐文件） | `grep -cE '^\*\*C-[0-9]+\*\*' .specify/specs/108-team-view-degradation/contracts/*.md` | presentation **9** / report-recognition **8** / team-view-program **9** / view-labels **9**；合计 **35**。**陷阱形**：`grep -ohE '\bC-[0-9]+\b' …/contracts/*.md \| wc -l` → **42**（正文引用混入）；计量单位是行首 `**C-NNN**` 定义行 |
| 实测语料组成 | 一段 Python 扫描 `.specify/teams/*/runs/*` 应用 FR-001 封闭文法与 FR-003 次序 | **46** 文件 = **41** 运行报告（**28** 紧凑合规 + **13** 可解析非合规报告样式）+ **3** 辅助产物 + **2** 残留；三个全非合规团队各 **5 / 7 / 1** 份。**陷阱形**：`ls .specify/teams/*/runs/* \| wc -l` → **46**（把辅助产物与残留都算成报告） |
| 基线对象与 blob 同一性 | `git cat-file -e 54c6efa8c`；`git show 54c6efa8c:scripts/python/team-view.py \| sha256sum`；`sha256sum scripts/python/team-view.py` | 对象在位；两侧 sha256 同为 **`81fad3f9df019319c75d1a73c1ffa27338ac942db6b22c4b90e6b5b61e7bf06b`** |
| 镜像 / 副本基线 | `python3 scripts/python/sync-mirrors.py --check`；`python3 scripts/python/regen-command-copies.py --check` | rc **0**（六对镜像字节一致）；rc **0**（`OK: all per-tool command copies match the source templates.`） |
| 解释器与 pytest | `/usr/local/bin/python3 --version`；`/usr/local/bin/python3 -m pytest --version`；`python3 -m pytest --version` | **3.11.11**；**pytest 8.4.2**；PATH 的 `python3` → `No module named pytest`（`SPECKIT_PYTHON` 覆写是必需项） |
| 新测试文件当前状态 | 逐个 `test -e`（三支新测试文件） | **3/3 ABSENT**（红先前提） |
| 读取 / 编辑目标在位 | 逐个 `test -e`（4 个既有 team-view 测试文件、fixture builder、`goal-utils.py`、`script_interface_cli.py`、docs 页、view-team 技能、`run-tests.sh`） | **10/10 OK** |
| 既有测试面指纹 | `sha256sum tests/unit/test_team_view_parsers.py tests/contract/test_team_view_program_contract.py tests/contract/test_team_view_command.py tests/integration/test_team_view_program.py` | `586d89af…` / `c90700aa…` / `93ca0b23…` / `6cfaca93…`（实现入口复测须相等，否则按差异重新裁定） |
| 证据落点当前状态 | `test -d .specify/specs/108-team-view-degradation/notes`；`test -e .specify/specs/108-team-view-degradation/coverage-baseline.txt` | 两者 **ABSENT** → Setup 行创建 |

## Requirement Coverage Map

| FR | Rows | FR | Rows | FR | Rows |
|----|------|----|------|----|------|
| FR-001 | T006, T008 | FR-010 | T014, T017 | FR-019 | T015, T019 |
| FR-002 | T006, T008 | FR-011 | T013, T015 | FR-020 | T021, T022, T023, T024 |
| FR-003 | T006, T008 | FR-012 | T013, T015, T021 | FR-021 | T008, T019, T023 |
| FR-004 | T006, T009 | FR-013 | T013, T015 | FR-022 | T020 |
| FR-005 | T006, T010 | FR-014 | T013, T015 | FR-023 | T024, T028 |
| FR-006 | T007, T011 | FR-015 | T013, T016 | FR-024 | T019, T025 |
| FR-007 | T014, T017 | FR-016 | T013, T016 | FR-025 | T014, T020, T022 |
| FR-008 | T014, T017 | FR-017 | T010, T019 |  |  |
| FR-009 | T014, T017 | FR-018 | T007, T010, T019 |  |  |

| SC | Rows |
|----|------|
| SC-001 | T007, T012 |
| SC-002 | T007, T012 |
| SC-003 | T013, T018 |
| SC-004 | T020, T025 |
| SC-005 | T019, T025, T027 |
| SC-006 | T007, T019, T025 |
| SC-007 | T020, T025 |
| SC-008 | T027, T029 |

## Clause Coverage & Green Partition

35 条机器可判定条款逐条恰认领一次。测试编写行不携带 `[green:]`；认领落在各故事末尾的验证行（运行测试、写证据），因此无 `green-path-divergence`、无 `green-clause-collision`，每份契约内认领序号随行序单调。

| Contract | Clause | Pinning test | Green point |
|----------|--------|--------------|-------------|
| `contracts/report-recognition.contract.md` | C-201 | `test_team_view_report_recognition.py::test_stamp_grammar_accepts_exactly_the_five_forms` | T012 |
| `contracts/report-recognition.contract.md` | C-202 | `test_team_view_report_recognition.py::test_classification_order_is_fixed` | T012 |
| `contracts/report-recognition.contract.md` | C-203 | `test_team_view_report_recognition.py::test_latest_is_maximum_parsed_timestamp_with_name_tiebreak` | T012 |
| `contracts/report-recognition.contract.md` | C-204 | `test_team_view_report_recognition.py::test_normalized_token_is_the_single_value` | T012 |
| `contracts/report-recognition.contract.md` | C-205 | `test_team_view_report_recognition.py::test_residue_presentation_is_bounded` | T012 |
| `contracts/report-recognition.contract.md` | C-206 | `test_team_view_report_recognition.py::test_uncertainty_predicate_needs_readable_runs_and_residue` | T012 |
| `contracts/report-recognition.contract.md` | C-207 | `test_team_view_degradation.py::test_overview_matches_single_view_and_discloses_uncertainty` | T012 |
| `contracts/report-recognition.contract.md` | C-208 | `test_team_view_degradation.py::test_unreadable_latest_report_is_named_not_unrecorded` | T018 |
| `contracts/presentation.contract.md` | C-301 | `test_team_view_degradation.py::test_binding_unreadable_carries_engine_reason_and_repair_pointers` | T018 |
| `contracts/presentation.contract.md` | C-302 | `test_team_view_degradation.py::test_inline_goal_is_a_named_state_with_repair_pointers` | T018 |
| `contracts/presentation.contract.md` | C-303 | `test_team_view_degradation.py::test_matrix_without_agent_column_is_malformed_and_roster_not_comparable` | T018 |
| `contracts/presentation.contract.md` | C-304 | `test_team_view_degradation.py::test_missing_ledger_carries_its_consequences` | T018 |
| `contracts/presentation.contract.md` | C-305 | `test_team_view_degradation.py::test_spine_applicability_follows_declared_pattern` | T018 |
| `contracts/presentation.contract.md` | C-306 | `test_team_view_degradation.py::test_unreadable_latest_report_is_named_not_unrecorded` | T018 |
| `contracts/presentation.contract.md` | C-307 | `test_team_view_degradation.py::test_four_state_discipline_on_new_surfaces` | T018 |
| `contracts/presentation.contract.md` | C-308 | `test_team_view_degradation.py::test_degraded_definition_names_every_state` | T018 |
| `contracts/presentation.contract.md` | C-309 | `test_team_view_degradation.py::test_degraded_definition_names_every_state` | T018 |
| `contracts/team-view-program.contract.md` | C-101 | `test_team_view_degradation.py::test_view_degradation_leaves_tree_byte_identical` | T025 |
| `contracts/team-view-program.contract.md` | C-102 | `test_team_view_degradation_contract.py::test_single_recognition_entry_source_scan` | T025 |
| `contracts/team-view-program.contract.md` | C-103 | `test_team_view_degradation_contract.py::test_script_interface_stays_closed` | T025 |
| `contracts/team-view-program.contract.md` | C-104 | `test_team_view_degradation_contract.py::test_reason_set_is_closed` | T025 |
| `contracts/team-view-program.contract.md` | C-105 | `test_team_view_degradation_contract.py::test_envelope_keys_unchanged_with_nested_additions` | T025 |
| `contracts/team-view-program.contract.md` | C-106 | `test_team_view_degradation_contract.py::test_script_interface_stays_closed` | T025 |
| `contracts/team-view-program.contract.md` | C-107 | `test_team_view_degradation.py::test_healthy_fixture_is_byte_identical_to_the_baseline_program` | T025 |
| `contracts/team-view-program.contract.md` | C-108 | `test_team_view_degradation_contract.py::test_report_naming_owner_and_schema_unchanged_since_baseline` | T025 |
| `contracts/team-view-program.contract.md` | C-109 | `test_team_view_degradation_contract.py::test_three_surfaces_cite_the_owner` | T025 |
| `contracts/view-labels.contract.md` | C-401 | `test_team_view_degradation_contract.py::test_label_closure_both_directions` | T025 |
| `contracts/view-labels.contract.md` | C-402 | `test_team_view_degradation_contract.py::test_missing_state_subset_members` | T025 |
| `contracts/view-labels.contract.md` | C-403 | `test_team_view_degradation_contract.py::test_declaration_subset_members` | T025 |
| `contracts/view-labels.contract.md` | C-404 | `test_team_view_degradation_contract.py::test_derived_label_members` | T025 |
| `contracts/view-labels.contract.md` | C-405 | `test_team_view_degradation_contract.py::test_new_derived_label_members` | T025 |
| `contracts/view-labels.contract.md` | C-406 | `test_team_view_degradation_contract.py::test_residue_line_form_in_owner` | T025 |
| `contracts/view-labels.contract.md` | C-407 | `test_team_view_degradation_contract.py::test_roster_not_comparable_form_in_owner` | T025 |
| `contracts/view-labels.contract.md` | C-408 | `test_team_view_degradation_contract.py::test_no_substitute_label_or_empty_reason` | T025 |
| `contracts/view-labels.contract.md` | C-409 | `test_team_view_degradation.py::test_healthy_fixture_is_byte_identical_to_the_baseline_program` | T025 |

## Feature Integration Review

- **Review performed at generation (2026-11-26)**: `.specify/features.md` 行 108 已为 `Planned`；任务拆解不暴露新 Feature、不使任何既有 Feature 失效。父 Feature 027 保持 `Ready for Review`（no-status-regression）。tasks 阶段按 stage brief 对 `.specify/features.md` 与 `.specify/features/027-team-management.md` 零编辑；实现 / driver close-out 承担状态推进。
- **Glossary**: 本特性不引入新实体（A-14），不写 `.specify/glossary.md`；`team-view` / `pattern` / `slug` 等既有词条按项目词汇表原样使用。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 先建立证据落点、冻结实现前的可执行基线，并把红先骨架与语料前提固定下来。

- [ ] T001 Create the evidence directory `.specify/specs/108-team-view-degradation/notes/` with a `.gitkeep` so red-first, pre-change and quickstart records have their fixed landing points.
- [ ] T002 [blockedBy: T001] Freeze the contract coverage baseline with `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/108-team-view-degradation --freeze > .specify/specs/108-team-view-degradation/coverage-baseline.txt` and assert the frozen file is non-empty and its `frozen-from` header reads `excluding 108-team-view-degradation`.
- [ ] T003 [blockedBy: T001] Capture the pre-change side of every diff premise in `.specify/specs/108-team-view-degradation/notes/pre-change-measurements.md` with command, reading and date per row: the corpus composition (46 files = 41 reports [28 compact + 13 report-style] + 3 auxiliary + 2 residue; the three all-non-conforming teams hold 5 / 7 / 1), `git cat-file -e 54c6efa8c` plus the baseline-blob vs working-tree sha256 equality `81fad3f9…` for `scripts/python/team-view.py`, the `sync-mirrors.py --check` and `regen-command-copies.py --check` rc-0 readings, the sha256 of the four existing team-view test files, and the two `goal-utils.py binding` messages (`binding-missing: … carries no binding block …`; missing keys `owner_id, origin`).
- [ ] T004 [blockedBy: T001] Create the red-first evidence skeleton `.specify/specs/108-team-view-degradation/notes/red-first-evidence.md` with one slot per planned red-first test (unit grammar/classifier/latest/residue/uncertainty; production replica; corpus replica; residue-only; auxiliary and same-stamp cases; overview reuse; degraded definition; unreadable latest; ledger and spine states; contract closed sets, single entry, label closure and three-surface consistency), each slot recording command, real output and exit status; reference the `/speckit.implement` § Test runs owner for the failing-name baseline instead of restating its path or flag.
- [ ] T005 [blockedBy: T003] Record the implement-entry toolchain readings in `.specify/specs/108-team-view-degradation/test-evidence/implement-entry-readings.txt`: fresh `sync-mirrors.py --check` and `regen-command-copies.py --check` verdicts, `test -e` results for the 10 read/edit surfaces and the 3 absent new test files, and the pytest version under `/usr/local/bin/python3`; this is the environment reading, never a second failing-test baseline.

**Checkpoint**: evidence landing points exist; every pre-change value is frozen before any edit; no executable surface changed yet.

---

## Phase 2: User Story 1 - 真实运行历史不被读丢：报告识别、最新选择与残留 (Priority: P1) 🎯 MVP

**Goal**: 真实团队的运行报告按可解析 UTC 时间戳识别与排序，最新永远是解析时间戳最大者；辅助产物与残留各有显式分类与有界呈现；残留存在时最新判定被披露为不可证明并进入降级。

**Independent Test**: production-replica fixture 上「最近报告」= 解析时间戳最大者、5/5 分类命中、残留行计数 + 有界示例、exit 5；corpus-replica fixture 上 13/13 识别、状态非 `为空`/`缺失`、exit 0；residue-only fixture 上状态为「仅残留，最新不可确定」；概览列与单团队视图的规范化 token 相等。

### Tests for User Story 1 (MANDATORY)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T006 [P] [US1] [blockedBy: T004] Author the US1 red-first unit tests in `tests/unit/test_team_view_report_recognition.py` (importlib load of the hyphenated program, in the style of the existing parser tests): the five accepted stamp forms and rejected samples (date-only prefix, month 13, February 30, hour 24, non-Z zone, stamp not at the name start), the fixed three-way classification order including `-<4hex>-report.md` and `-<4hex>-stage.md`, latest = maximum parsed timestamp with name-ascending tie-break, the single normalized `YYYYMMDDThhmmssZ` token, the residue bound (total count, at most 3 examples, omitted count) and the uncertainty predicate (readable `runs/` plus residue count ≥ 1 only); build fixtures with the existing builder per `tests/fixtures/team_view_fixtures.py`, run the file through the single entry per `scripts/bash/run-tests.sh`, and capture the failing output in `.specify/specs/108-team-view-degradation/test-evidence/us1-red-unit.txt` for the red-first note (FR-001, FR-002, FR-003, FR-004, FR-005).
- [ ] T007 [P] [US1] [blockedBy: T004] Author the US1 red-first integration tests in `tests/integration/test_team_view_degradation.py`: the production replica (old compact report, newer `20261125T121924Z-93cc-stage.md`, newer ISO-dashed report, same-stamp `-seat-result.md`, two date-only residue names) asserting latest = the parsed maximum, 5/5 classification, the bounded residue line and exit 5; the real-corpus replica (5 × `YYYY-MM-DDThh-mm-ssZ-report.md`, 7 × `YYYY-MM-DDThhmmssZ-report.md`, 1 × `YYYYMMDDThhmmZ-report.md`) asserting 13/13 recognition, a state that is neither `为空` nor `缺失`, and exit 0; the residue-only state `未识别（unrecognized）—— 仅残留，最新不可确定`, auxiliary-never-latest, same-stamp tie-break, and overview-vs-single token equality with the inline `（report-recognition-uncertain：残留 N）` marker at exit 0; use the existing builder per `tests/fixtures/team_view_fixtures.py`, run through the single entry per `scripts/bash/run-tests.sh`, and capture the failing output in `.specify/specs/108-team-view-degradation/test-evidence/us1-red-integration.txt` (FR-006, FR-018).

### Implementation for User Story 1

- [ ] T008 [US1] [blockedBy: T006,T007] Implement the closed timestamp grammar and the single classification entry `classify_runs()` in `scripts/python/team-view.py`: five stamp forms with strict UTC calendar validation, the fixed order (no stamp → residue; stamp plus `(?:-[0-9a-f]{4})?-(?:report|stage)\.md` → report; stamp plus any other remainder → auxiliary), latest = maximum parsed timestamp with name-ascending ties, the single normalized token, and the inventory fields (`state` / `reports` / `shown` / `omitted` / `auxiliaries` / `residue` / `latest_path` / `latest_token` / `uncertain` / `unreadable`); replace the `REPORT_NAME_RE` use in `build_persistence()` with this one entry and keep exactly one compiled grammar (FR-001, FR-002, FR-003, FR-021).
- [ ] T009 [US1] [blockedBy: T008] Implement the runs presentation in `_render_persistence()` of `scripts/python/team-view.py`: `已列出` with the carried report cap, the only-residue state `未识别（unrecognized）—— 仅残留，最新不可确定`, the `辅助产物（auxiliary）` line, and the residue line `未识别（unrecognized）: 共 N 份；示例: …（省略 K）` with at most 3 examples and the omitted count; no unbounded name transcription; `缺失` / `为空` / `不可读` keep their meanings (FR-004).
- [ ] T010 [US1] [blockedBy: T008] Implement the uncertainty and degradation carrier in `scripts/python/team-view.py`: a readable `runs/` with residue count ≥ 1 activates `report-recognition-uncertain` in `errors[]` with `degraded = true` and exit 5, and appends the non-group `降级（degraded）` block naming every active reason individually; keep `engine-degraded` unchanged and never let a file-level state alone change the exit code (FR-005, FR-017, FR-018).
- [ ] T011 [US1] [blockedBy: T008] Make the overview reuse the same entry in `scripts/python/team-view.py`: replace `_latest_report_token()` and its narrow `max()` with `classify_runs()` and the normalized token, append `（report-recognition-uncertain：残留 N）` to a residue-bearing row's latest cell, keep the `0/2` exit domain, and never leave an undeterminable row blank or on an older value (FR-006).
- [ ] T012 [US1] [blockedBy: T006,T007,T008,T009,T010,T011] Run the US1 tests through the single entry (run `tests/unit/test_team_view_report_recognition.py` via `scripts/bash/run-tests.sh` and run `tests/integration/test_team_view_degradation.py` via the same entry), record both red-first slots and the green reading in `notes/red-first-evidence.md` and `notes/us1-green.txt` with the SC-001 and SC-002 evidence, and confirm the corpus-replica 13/13 and production-replica 5/5 counts. [green: contracts/report-recognition.contract.md#C-201] [green: contracts/report-recognition.contract.md#C-202] [green: contracts/report-recognition.contract.md#C-203] [green: contracts/report-recognition.contract.md#C-204] [green: contracts/report-recognition.contract.md#C-205] [green: contracts/report-recognition.contract.md#C-206] [green: contracts/report-recognition.contract.md#C-207]

**Checkpoint**: US1 独立可测——真实命名历史被完整识别，最新由解析时间戳决定，残留有界披露并触发 `report-recognition-uncertain`；概览复用同一入口。

---

## Phase 3: User Story 2 - 降级团队被诚实呈现并给出修复路径 (Priority: P1)

**Goal**: 定义不合模板但真实存在的团队被逐项诚实呈现：binding 不可读带引擎原文原因与受制裁修复指针，内联 goal 是命名状态，矩阵缺列是形态异常且名册差异为不可比对，缺失产物带后果，非 continuous 脊柱按 pattern 不适用，frontmatter 成员全量保留。

**Independent Test**: production-shape degraded fixture 上一次 view 退出码 5，六个具名状态全部出现（绑定 `不可读` + 精确原因 + 修复指针、goal 命名状态、矩阵 `形态异常` 点名缺列、`roster_delta` 不可比对、台账 `缺失` 带后果、脊柱按 pattern 不适用），9/9 成员，`/speckit.team modify` ≥ 1，编造零值 = 0；不可读最新报告是命名状态而不是静默 `未记录`。

### Tests for User Story 2 (MANDATORY)

- [ ] T013 [US2] [blockedBy: T012] Author the US2 red-first integration tests appended to `tests/integration/test_team_view_degradation.py` for the production-shape degraded fixture (no `binding` block, a partial-keys variant, an inline `goal` with `anchor_slug`, a matrix without the `agent` column, missing `items.jsonl`, `pattern: iteration` with the three spine files missing, nine frontmatter members): binding `不可读` with the engine's verbatim reason and the `/speckit.team modify` plus `goal-utils.py bind` pointers; the `goal 需归一为 anchor_slug` state with its pointers and an unchanged identity type; matrix `形态异常（缺列: agent）` with parsed rows still listed and `roster_delta` = `不可比对（not comparable）（原因：…）`; ledger `缺失` with its consequences; spine `按声明 pattern 不适用` with the `operating-loops.md` § 8 pointer; 9/9 members and the `seats` / `stage_seats` declared state; exit 5 with every active reason named; at least one `/speckit.team modify` and zero fabricated zero or placeholder values; run through the single entry per `scripts/bash/run-tests.sh` and capture the failing output in `.specify/specs/108-team-view-degradation/test-evidence/us2-red-degraded.txt` (FR-011…FR-016).
- [ ] T014 [US2] [blockedBy: T013] Author the US2 red-first integration tests appended to `tests/integration/test_team_view_degradation.py` for the remaining presentation states: an unreadable latest report (mode 000) renders `不可读` with its path and `不可读` field lines rather than silent `未记录` and does not change the exit code by itself; an undeclared pattern renders spine applicability `适用性不可判定` and discloses the `create-mode.md` § Schema notes owner; a zero-line `items.jsonl` stays `为空`; all six group headings remain present and in order with the new lines additive; run through the single entry per `scripts/bash/run-tests.sh` and capture the failing output in `.specify/specs/108-team-view-degradation/test-evidence/us2-red-states.txt` (FR-007, FR-008, FR-009, FR-010, FR-025).

### Implementation for User Story 2

- [ ] T015 [US2] [blockedBy: T013,T014] Implement the identity-group states in `scripts/python/team-view.py`: binding readability stays engine-only with the verbatim reason plus `/speckit.team modify` and `goal-utils.py bind` pointers (record owner `anchor-definitions.md` § The Binding Record); a declared `goal` renders `goal 需归一为 anchor_slug` in the identity group's degraded cases (non-slug value, or unreadable binding) with `/speckit.team modify` and `goal-utils.py migrate` pointers, while a slug-form `goal` under a readable binding adds no state line (healthy per FR-022); identity resolution keeps `anchor_slug` > `goal_slug` > inferred; never fill a default or infer a value (FR-011…FR-014, FR-019, FR-022).
- [ ] T016 [US2] [blockedBy: T013,T014] Implement the static-group states in `scripts/python/team-view.py`: a missing or duplicated `agent` column → `形态异常` with `缺列: agent` / `重复列: agent` while every parsed matrix row still renders; `roster_delta` → `不可比对（not comparable）（原因：…）` and never `未记录`; frontmatter members render in full; `seats` / `stage_seats` keep their declared/undeclared disclosure (FR-015, FR-016).
- [ ] T017 [US2] [blockedBy: T013,T014] Implement the persistence-group states in `scripts/python/team-view.py`: `items.jsonl` missing → `缺失` with path and consequences (no aggregate counts, no non-terminal signal, no zero-value substitution); spine applicability follows the declared pattern (`continuous` gap vs `按声明 pattern 不适用` with the `operating-loops.md` § 8 pointer; undeclared pattern → `适用性不可判定` plus the `create-mode.md` § Schema notes disclosure); an unreadable latest → `不可读` with path and `不可读` field lines instead of `未记录`; four-state discipline on every new surface (FR-007…FR-010).
- [ ] T018 [US2] [blockedBy: T015,T016,T017] Run the US2 tests through the single entry (run `tests/integration/test_team_view_degradation.py` via `scripts/bash/run-tests.sh`), record the green reading in `notes/us2-green.txt` with the SC-003 six-state evidence, and confirm the named states, the 9/9 member listing and the zero-fabricated-value count. [green: contracts/report-recognition.contract.md#C-208] [green: contracts/presentation.contract.md#C-301] [green: contracts/presentation.contract.md#C-302] [green: contracts/presentation.contract.md#C-303] [green: contracts/presentation.contract.md#C-304] [green: contracts/presentation.contract.md#C-305] [green: contracts/presentation.contract.md#C-306] [green: contracts/presentation.contract.md#C-307] [green: contracts/presentation.contract.md#C-308] [green: contracts/presentation.contract.md#C-309]

**Checkpoint**: US2 独立可测——降级团队的每个不可得事实都带原因与修复路径，名册与矩阵数据不被吞掉，四种文件级状态不互相冒充。

---

## Phase 4: User Story 3 - 降级语义封闭、可测，健康输出保持不变 (Priority: P2)

**Goal**: 降级原因与退出码成为封闭、可测的集合；渲染标签有唯一活所有者且双向闭包；报告识别/最新选择入口唯一；三面（docs / skill / 程序声明）一致；健康团队输出与基线程序逐字节一致，view 零写盘。

**Independent Test**: 基线程序与变更后程序在同一健康 fixture 上 stdout 逐字节相同、退出码相同；原因→退出码逐项命中 2/2、集合外取值 0；源码扫描恰好一个分类入口；标签常量与 `contracts/view-labels.contract.md` 双向一致；三面各点名两个原因 id 与同一 owner 指针；三个场景的前后工作树哈希不变。

### Tests for User Story 3 (MANDATORY)

- [ ] T019 [P] [US3] [blockedBy: T018] Author the US3 red-first contract tests in `tests/contract/test_team_view_degradation_contract.py`: the closed reason set `{engine-degraded, report-recognition-uncertain}` with the 2/2 exit-5 mapping and the unchanged `0/2/3/4/5` set; the exact ten-key `--json` envelope with reasons riding `errors[].code`, nested additions only, and `degraded` true iff a reason is active; exactly one `def classify_runs(` and one compiled timestamp grammar with the overview calling the same entry; reverse samples for a reason outside the set, a label outside the owner table and an extra top-level envelope key; the program label constants ⊆ the tables of `contracts/view-labels.contract.md` in both directions (every member has an emitting site); the closed CLI surface and `-h` / `--help` / `--version` zero-write behaviour; read-only asserts against `docs/reference/commands/team.md`, `skills/internal/view-team/SKILL.md` and the program declaration, each naming both reason ids and citing `contracts/team-view-program.contract.md`; a read-only source scan against `scripts/python/team-view.py` proving only the three declared engine reads and against `scripts/python/goal-utils.py` proving zero modification; and `git show 54c6efa8c:` equality per `git show 54c6efa8c:skills/internal/create-team/SKILL.md` and per `git show 54c6efa8c:skills/internal/create-team/references/create-mode.md`; run through the single entry per `scripts/bash/run-tests.sh` and capture the failing output in `.specify/specs/108-team-view-degradation/test-evidence/us3-red-contract.txt` (FR-017, FR-019, FR-021, FR-024).
- [ ] T020 [P] [US3] [blockedBy: T017] Author the golden-preservation and read-only guards appended to `tests/integration/test_team_view_degradation.py` (regression-guard exception: their green is meaningful only after the engine amendment, so they follow implementation): materialize the baseline program per `git show 54c6efa8c:scripts/python/team-view.py`（只读） beside a read-only base per `scripts/python/script_interface_cli.py` and a read-only base per `scripts/python/goal-utils.py`, assert the git object exists, then on fixtures satisfying the completed FR-022 predicate (three-key binding, compact report names, zero auxiliary artifacts, zero residue, `agent` column, `items.jsonl` present with at least one line, all three continuous-spine files present) in both goal variants (`goal` absent and `goal: <slug>`) run the baseline and working-tree programs and assert byte-identical stdout and equal exit codes; snapshot the fixture tree before and after healthy, degraded and overview invocations and assert zero file additions, modifications or deletions; capture the guard readings in `.specify/specs/108-team-view-degradation/test-evidence/us3-guards.txt` (FR-022, FR-025).

### Implementation for User Story 3

- [ ] T021 [US3] [blockedBy: T019] Update `docs/reference/commands/team.md` View Mode: the closed timestamp grammar and three-way classification, latest = parsed maximum plus the uncertainty rule, the statement that `缺失` / `为空` alone never degrade, the exit-5 meaning, both reason ids (`engine-degraded`, `report-recognition-uncertain`), the repair pointers (`/speckit.team modify`, `goal-utils.py bind` / `migrate`), and the owner pointer `.specify/specs/108-team-view-degradation/contracts/team-view-program.contract.md` with no second definition (FR-012, FR-020).
- [ ] T022 [US3] [blockedBy: T019] Update `skills/internal/view-team/SKILL.md` error-navigation row 5 and the additive-presentation wording: name both reason ids, carry the exit-5 meaning and the owner pointer `.specify/specs/108-team-view-degradation/contracts/team-view-program.contract.md`, state that the new states append rather than replace existing lines, and keep the verbatim re-emission rule unchanged (FR-020, FR-025).
- [ ] T023 [US3] [blockedBy: T019] Update the program declaration in `scripts/python/team-view.py`: the module docstring and the `--help` epilog name both reason ids (`engine-degraded`, `report-recognition-uncertain`), carry the exit-5 meaning and cite the owner pointer `.specify/specs/108-team-view-degradation/contracts/team-view-program.contract.md`; keep `-h` / `--help` / `--version` exit 0 with zero writes (FR-020, FR-021).
- [ ] T024 [US3] [blockedBy: T021,T022,T023] Regenerate and verify the mirror pairs: run `python3 scripts/python/sync-mirrors.py --write` then `--check` with no NEW drift against `test-evidence/sync-mirrors-baseline.txt`; compare byte-for-byte `scripts/python/team-view.py` with `.specify/scripts/python/team-view.py` and `skills/internal/view-team/SKILL.md` with `.specify/skills/internal/view-team/SKILL.md`; run `python3 scripts/python/regen-command-copies.py --check` rc 0 (FR-020, FR-023).
- [ ] T025 [US3] [blockedBy: T019,T020,T021,T022,T023,T024] Run the US3 tests through the single entry (run `tests/contract/test_team_view_degradation_contract.py` via `scripts/bash/run-tests.sh` and run `tests/integration/test_team_view_degradation.py` via the same entry), record the green reading and the SC-004 / SC-005 / SC-006 / SC-007 evidence in `notes/us3-green.txt`, and confirm the baseline-vs-amended stdout diff line count is 0 and the label closure reads both directions. [green: contracts/team-view-program.contract.md#C-101] [green: contracts/team-view-program.contract.md#C-102] [green: contracts/team-view-program.contract.md#C-103] [green: contracts/team-view-program.contract.md#C-104] [green: contracts/team-view-program.contract.md#C-105] [green: contracts/team-view-program.contract.md#C-106] [green: contracts/team-view-program.contract.md#C-107] [green: contracts/team-view-program.contract.md#C-108] [green: contracts/team-view-program.contract.md#C-109] [green: contracts/view-labels.contract.md#C-401] [green: contracts/view-labels.contract.md#C-402] [green: contracts/view-labels.contract.md#C-403] [green: contracts/view-labels.contract.md#C-404] [green: contracts/view-labels.contract.md#C-405] [green: contracts/view-labels.contract.md#C-406] [green: contracts/view-labels.contract.md#C-407] [green: contracts/view-labels.contract.md#C-408] [green: contracts/view-labels.contract.md#C-409]

**Checkpoint**: US3 独立可测——封闭集、单入口、三面一致与健康保真均以机器 diff / 源码扫描 / 行为断言钉住。

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: quickstart 实录、定向测试收口、形态不变守卫与验收证据包。

- [ ] T026 [blockedBy: T025] Execute every scenario in `.specify/specs/108-team-view-degradation/quickstart.md` exactly as written (S-1…S-7, with the S-0 readings re-taken) and record command, output and exit status per scenario in `notes/quickstart-run.md`, teardown included.
- [ ] T027 [blockedBy: T025] Run the targeted set exactly as quickstart.md § Run the targeted set prescribes (the three new test files plus the four inherited team-view test files) through the single entry per `scripts/bash/run-tests.sh`, capture the failing-test name list and compare it against the implement pre-flight baseline under the `/speckit.implement` § Test runs owner (path and flag owned there, not restated), and record the rc, counts and zero-new-failure reading in `test-evidence/targeted-set.txt` (SC-008).
- [ ] T028 [blockedBy: T025] Verify the no-shape-change claim: a read-only `git diff --stat 54c6efa8c..HEAD` against `skills/internal/create-team/SKILL.md` and `skills/internal/create-team/references/create-mode.md` is empty, and the corpus-replica test still recognizes 13/13 while compact `<YYYYMMDD>T<hhmmss>Z-report.md` names stay reports; record the reading in `test-evidence/shape-change-guard.txt` (FR-023).
- [ ] T029 [blockedBy: T025,T026,T027,T028] Assemble the crew-side close-out input `.specify/specs/108-team-view-degradation/test-evidence/verification-input.md`: one `SC-001_status`…`SC-008_status` row each with value, note, command and evidence pointer; the `final`-path criteria SC-001…SC-004 read `pass` and the single smoke record carries `smoke_command=`, `smoke_exit_code=0` and an existing non-empty `smoke_evidence_path=`; the `supporting` criteria SC-005…SC-008 record their evidence (condition set owner: `shared/workflow/acceptance-hardening.md` § Gates). `verification.md` is derived spec-side from this input and MUST NOT be written by the crew (handoff/team forbidden list).

**Checkpoint**: quickstart 全场景有实录；定向集零新增失败；命名 owner 与 schema 未变；`test-evidence/verification-input.md` 可被 spec 侧直接派生为 `verification.md` 供 review 消费。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，可立即开始。
- **Foundational**: 本特性不设独立 Foundational 阶段——三支新测试文件自带本地 helper，既有 `tests/fixtures/team_view_fixtures.py` 已能写任意 `runs/` 文件名与缺失产物，唯一共享实现面（单一读取引擎）按 US1 → US2 → US3 的顺序在行内串行落地。
- **US1 (Phase 2)**: 依赖 Setup；完成后 US2 可开始。
- **US2 (Phase 3)**: 依赖 US1 的验证（同一 integration 文件按段追加）；完成后 US3 可开始。
- **US3 (Phase 4)**: 依赖 US2；封闭集、三面一致与健康保真在此收口。
- **Polish (Phase 5)**: 依赖 US3 完成。

### User Story Dependencies

- **US1（P1）**: Setup 之后即可开始；产出识别/最新/残留/不确定性、新降级原因与概览复用；检查点独立可测（MVP）。
- **US2（P1）**: 依赖 US1 的 integration 文件段落与引擎改动；产出六组内的诚实呈现与修复指针；检查点独立可测。
- **US3（P2）**: 依赖 US1 的新原因与 US2 的呈现面；产出封闭集测试、单入口扫描、标签闭包、三面一致、健康保真与只读守卫。

### Within Each User Story

- 测试先写并按唯一入口执行转红，实现随后使其转绿；验证行汇总红先证据与绿点。
- 同一文件的章节按行序追加（引擎与 integration 文件都不并行写）。
- 每个故事末尾的验证行是 `[green:]` 认领点；测试编写行不认领。
- T020 的两项守卫是回归守卫，按 migration/regression 例外置于实现之后。

### Parallel Opportunities

- Setup 无 `[P]`（同一 notes 目录与同一证据面串行建立）。
- US1 的 T006 与 T007 可并行（unit 文件 vs integration 文件，红先原始输出写入互不相同的 test-evidence sink）。
- US3 的 T019 与 T020 可并行（contract 文件 vs integration 文件，证据 sink 互不相同；两行只以只读指针引用共享 fixture builder 与引擎）。
- 其余行因共享同一引擎或同一 integration 文件而按行序串行。

---

## Parallel Example: User Story 1

```bash
# Launch the two US1 test-authoring rows together (distinct write targets and distinct red sinks):
Task: "Author the US1 unit tests in tests/unit/test_team_view_report_recognition.py (red sink test-evidence/us1-red-unit.txt)"
Task: "Author the US1 integration tests in tests/integration/test_team_view_degradation.py (red sink test-evidence/us1-red-integration.txt)"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 only — it is the smallest same-priority set whose checkpoint is independently testable (production replica + corpus replica + residue-only + overview equality) and it repairs the direct production root cause ("latest is not the real latest"). US2 is the immediate second P1 increment; US3 is the supporting hardening that must not manufacture new distortions.

1. Complete Phase 1: Setup.
2. Complete US1 tests → implementation → verification (T006–T012).
3. **STOP and VALIDATE**: 用 US1 的独立测试标准验证（最新 = 解析最大、13/13、残留有界、概览一致）。
4. Deliver US2, then US3, then Polish.

### Incremental Delivery

1. Setup → 证据落点与冻结基线就绪。
2. US1 → 真实运行历史可读且最新正确（MVP）。
3. US2 → 降级团队诚实呈现并给出修复路径。
4. US3 → 封闭语义、三面一致、健康保真与零写盘。
5. Polish → quickstart 实录、定向集收口与 `test-evidence/verification-input.md`（spec 侧派生 `verification.md`）。

### Parallel Team Strategy

单执行体（本线 `single-unit`）。若后续拆并行：仅 T006/T007 与 T019/T020 两组行可分组并行；引擎、integration 文件与 notes 汇总面永不由两个执行体同时写。

---

## Notes

- **PLAN-EDIT**: 无。本文件未改动任何 plan-owned 路径；contracts、quickstart、data-model、research、feature-ref 只被引用，不被编辑。实现期间如需对 plan-owned 路径做实质变更，按 stage 规则回抛 `ANOMALY`。
- **无迁移**: 本特性不改报告命名 owner（`skills/internal/create-team/SKILL.md` § Report contract）与 `team.md` schema；既有团队零迁移，紧凑命名报告仍是运行报告。FR-023 由 T028 的基线相对 diff 与 C-108 的 `git show` 相等测试共同钉住。
- **单一引擎**: 所有引擎行编辑 `scripts/python/team-view.py`；不新增第二读取器/存储/缓存/快照/索引/registry；`goal-utils.py` 零修改，`goal-utils.py` 的 `bind` / `migrate` 只作为修复路径被点名、不被 view 调用。
- **绿点分区**: 35 条款恰一次认领（T012 / T018 / T025）；测试编写行不携带 `[green:]`；三个验证行只以 `run` 治理词引用测试路径，故 `green-path-divergence` 为 0。integration 文件跨三个故事分段追加，各验证行只负责自己那一段转绿。
- **红先与回归守卫**: T020 的健康保真与只读快照守的是既有行为，其绿只有在引擎修订后才有意义，故按 migration/regression 例外置于实现之后；其余全部新行为测试先于其实现行。
- **测量陷阱**: 条款计数单位是行首 `**C-NNN**` 定义行（正文 `C-` 提及会把 35 读成 42）；语料计数必须按 FR-001 文法分类（直接 `ls` 把 3 个辅助产物与 2 个残留算成报告，46 ≠ 41）。
- **测试预算**: 只跑定向集（三支新文件 + 四个既有 team-view 文件），经唯一入口 `scripts/bash/run-tests.sh`，不跑全量、不直接调用解释器级测试命令；`SPECKIT_PYTHON=/usr/local/bin/python3` 固定在 § Environment Prerequisites。
- **修复路径不执行**: binding / goal 的修复指针只呈现；view 零写盘由 T020 的三场景快照钉住，`/speckit.team modify` 与 `goal-utils.py bind` / `migrate` 从不在 view 内被调用。
