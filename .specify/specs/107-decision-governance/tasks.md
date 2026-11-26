# Tasks: Decision Governance（AI Agent 决策项治理）

**Requirement ID**: 107
**Requirement Key**: `107-decision-governance`
**Related Feature**: 107 Decision Governance（AI Agent 决策项治理） — `.specify/features.md` 行 107；本阶段维持 `Planned`，不推进生命周期
**Input**: Design documents from `.specify/specs/107-decision-governance/`
**Prerequisites**: plan.md（技术路线 / Project Structure / Mirror Obligations / BC-01…BC-06 / EP-001…EP-007 / T-001…T-003）、requirements.md（30 FR / 10 SC / 9 STR / A-1…A-14 / P-01…P-12 / M-01…M-09 / B-01…B-07）、research.md（M-1…M-16 / R-1…R-8）、data-model.md（E1…E9 / I-01…I-14）、contracts/ ×5（C-101…C-109 / C-201…C-208 / C-301…C-308 / C-401…C-407 / C-501…C-506）、quickstart.md（6 scenarios）、feature-ref.md

**Tests Mode**: ON（Constitution Principle IV "Test-First & Contract-Driven Implementation" 为测试强制原则；本特性交付可执行检查器 `scripts/python/validate-decisions.py` 与守卫夹具，测试形态为 unit / contract / integration 运行时测试。文档面（owner page、instruction 段、指针行）按宪法 VII 的 template-only 条款由结构契约测试承接，不冒充运行时测试。migration/regression 例外两处：C-502 的零改写读数与 BC 行映射守的是既有语料与已落地迁移面，其红能力由实现后语料与变异演练证明；其余新行为测试一律红先。）

**Tests**: 红先证据的唯一落点 `.specify/specs/107-decision-governance/notes/red-first-evidence.md`（每支测试一条：命令、真实输出、退出码）。失败 nodeid 名集的捕获与比较形式归 `/speckit.implement` 的 `**Test runs**` owner，本文件只给路径与命令。测试执行唯一入口 `bash scripts/bash/run-tests.sh`；interpreter 固定在 § Environment Prerequisites。

**Organization**: 按用户故事组织——US1（两条生产规则与两类强调，P1）、US2（封闭选项集，P1）、US3（既有载体归档与可重建，P1）、US4（superagent→subagent 传递与实施回执，P1）、US5（M/B 强制诚实，P2）、US6（落地、镜像、客户接收、旧记录零改写，P2）。

## Definition of Done (DoD)

- DoD-1: 全部任务行为 `[X]`；若出现 `[~]`，其理由逐条记录在 `.specify/specs/107-decision-governance/test-evidence/verification-input.md` 的 `deferred_tasks=`（`verification.md` 由 spec 侧从该输入派生）。
- DoD-2: 交付面齐备——新所有者页 `shared/definitions/decision-definitions.md`、只读检查器 `scripts/python/validate-decisions.py`、五支测试模块、instruction 新段（≤1,500 B）与总预算 40,960、相邻所有者指针行、`docs/concepts/spec-driven.md` 与框架地图行、镜像与副本再生成。
- DoD-3: M-01…M-09 每条都有能转红的守卫与逆向样本，并逐条经唯一测试入口执行；B-01…B-07 每条都有具名评审承接面，文档与测试均不声称机器覆盖。
- DoD-4: FR-014 分层文法（基础层 + 条件层）、`D-NNN` 编号与 register 登记语义、四类载体重建、旧记录 `legacy` 报告与零改写均可实测复现。
- DoD-5: 传递面完整——决策块五字段、确认、`implementation_receipt` 四字段、缺席拒绝、静默重决上送、三段审计链与多跳同号规则均有夹具与守卫。
- DoD-6: 镜像 / 副本 / instruction 收敛——`sync-mirrors.py --check` 相对基线无新增漂移成员、`regen-command-copies.py --check` rc 0、模板与活副本段逐字一致且在字节上限内、空客户项目 init 收到该段、`scan-confirmation-gates.py` 相对基线 `test-evidence/scan-confirmation-gates-baseline.txt` 零新增命中。
- DoD-7: BC-01…BC-06 每行都映射到一条被测试的迁移或确定性拒绝行为与证据；无只依赖运行时双路径回退或人工说明的行。
- DoD-8: `.specify/specs/107-decision-governance/test-evidence/verification-input.md`（crew 可写的收口输入）逐条记录 SC-001…SC-010 的状态、命令与证据指针；`final` 路径判据记 `pass` 并带 smoke 记录；`verification.md` 由 spec 侧从该输入派生，crew MUST NOT 直接写（handoff/team 禁止面）。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/107-decision-governance/tasks.md` exit 0（0 error；WARN 逐条裁定并记录）。
- GATE-2: 跨产物一致 — check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/107-decision-governance --stage tasks --repo .` 输出 `decision=pass` 且 errors=0（advisory 逐条裁定）。
- GATE-3: FR / SC / 条款覆盖 — check: 本文件 § Requirement Coverage Map 为 30/30 与 10/10，§ Clause Coverage & Green Partition 的 38 条逐条恰认领一次；`pre-analyze-check.py --stage tasks` 的 `runtime-stack-row` errors=0（RS-004/RS-005/RS-006 的每个 FR 至少被一个任务行引用）。
- GATE-4: final 路径成功判据 + smoke 记录 — check: `verification.md` 中 `**Path**` 为 `final` 的 SC-001…SC-006 与 SC-010 全部 `pass`，且 `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`（存在且非空）齐备（条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates）。
- GATE-5: 镜像、副本与指令收敛 — check: `python3 scripts/python/sync-mirrors.py --check` 的漂移成员集相对 `test-evidence/sync-mirrors-baseline.txt` 无新增成员；`python3 scripts/python/regen-command-copies.py --check` exit 0；`cmp` 抽取段为空且段字节 ≤1,500 B、总量 <40,960 B。
- GATE-6: 门控中性 — check: `python3 scripts/python/scan-confirmation-gates.py --summary` 相对 `test-evidence/scan-confirmation-gates-baseline.txt`（31 blocking / 0 violations）零新增命中。
- GATE-7: 旧记录零改写 — check: `git diff --numstat 08b59695c..HEAD -- <既有记录路径>` 对既有文件删除列 = 0、`--diff-filter=D` 为空；追加与新增文件允许（行级包含读数，见 § Notes）。
- GATE-8: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/107-decision-governance/tasks.md` 返回 0。

## Environment Prerequisites

- CPython: **available** — probe: `/usr/local/bin/python3 --version` → `Python 3.11.11` @ 2026-11-25；约束：`python3` 可能解析到无 pytest 的 profile venv，全部测试行 MUST 以 `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh …` 经唯一入口执行；affected: 全部测试行与检查器行。
- pytest: **available** — probe: `/usr/local/bin/python3 -m pytest --version` → `pytest 8.4.2` @ 2026-11-25；affected: 全部测试行。
- bash / git: **available** — probe: `bash --version` → `4.4.20(1)-release`；`git --version` → `2.43.5` @ 2026-11-25；affected: 测试入口、镜像 / 副本与证据行。
- 容器运行时 / 镜像仓库 / 活集群 / 外网: **none** — 本特性全部检查为本地文件、`git`、本地 pytest 与既有 CLI（`specify init` / `specify migrate`），无构建、无拉取、无网络、无守护进程 @ 2026-11-25；affected: none。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标逐行不同、无未完成依赖）。本文件的 `[P]` 只出现在测试编写行：T009 / T010、T023 / T024 / T025、T046 / T047；其余行因共享同一所有者页、同一检查器或同一镜像 fan-out 而按行序串行。
- **[Story]**: 用户故事标签（`[US1]`…`[US6]`），只出现在用户故事阶段的任务行；Setup / Foundational / Polish 阶段零 `[US` 标记。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全 `[X]` 前不得开始本行。仅阶段顺序关系时不写。
- **[green: <contract>#<clause>]**: 绿点认领——本行是该条款在本特性重新转绿的那一行；契约路径相对本文件目录解析。**38 条款分区**：text C-101…C-105 → T017、C-106…C-108 → T022、C-109 → T045；archive C-201…C-208 → T031；transmission C-301…C-308 → T038；enforcement C-401…C-407 → T045；migration C-501…C-506 → T052。每条恰一行认领，认领行序与条款序号单调一致；测试编写行不携带 `[green:]`，故无 `green-path-divergence`。四项 green 检查由 `validate-tasks.py` 判定。
- 每行必须单行完成（含文件路径与全部标签），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `test-evidence/verification-input.md` 的 `deferred_tasks=`，spec 侧派生进 `verification.md`）。

## Path Conventions

- **框架源（编辑面）**: `shared/`、`skills/`、`scripts/`、`templates/`、`docs/`。
- **生成面（MUST NOT 手改）**: `.specify/shared/**`、`.specify/skills/**`、`.specify/scripts/**`、`.specify/templates/**`（由 `sync-mirrors.py` 投影）；每工具命令副本（由 `regen-command-copies.py` 生成）；`.specify/instructions.md`（由 `generate-instructions.sh` 产出）。
- **证据落点（本特性）**: `.specify/specs/107-decision-governance/` 下的 `notes/pre-change-measurements.md`、`notes/red-first-evidence.md`、`notes/us1-green.txt`…`notes/us6-green.txt`、`notes/quickstart-run.md`、`test-evidence/mutation-drill.md`、`test-evidence/migration-closure.md`、`test-evidence/gate-neutrality.txt`、`test-evidence/preservation-sweep.txt`、`test-evidence/verification-input.md`（crew 收口输入；`verification.md` 由 spec 侧派生）。
- **只读面（零修改）**: `.specify/specs/107-decision-governance/{plan.md,data-model.md,contracts/,quickstart.md,research.md,feature-ref.md}`（plan-owned，仅小修须 `PLAN-EDIT:` 声明）；`docs/reference/history/**`、`docs/decisions/**`、`.specify/archive/**`、其他规格的 `.specify/specs/**` 与 `.specify/register.md` 的既有行。
- **共享写入面（串行）**: `shared/definitions/decision-definitions.md`（六个故事阶段依次追加章节）、`scripts/python/validate-decisions.py`（四个 action 依次加入）。

## Measured Premises (re-measured at generation time 2026-11-25, HEAD `d05c3a350`)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 需求条目计数（FR / SC / STR） | `grep -cE '^\- \*\*FR-[0-9]+\*\*:' .specify/specs/107-decision-governance/requirements.md`；同法 `SC-`；`grep -cE '^\| \`STR-[0-9]+\`' …/requirements.md` | **30 / 10 / 9** |
| 契约条款数（逐文件） | `grep -cE '^\- \*\*C-[0-9]+\*\*' .specify/specs/107-decision-governance/contracts/*.md` | text **9** / archive **8** / transmission **8** / enforcement **7** / migration **6**；合计 **38**。**陷阱形**：`grep -c 'C-'` 会把正文引用一并算入；计量单位是行首 `- **C-NNN**` 条款定义行 |
| 生产者 / M / B / BC 行 | `grep -c '^| P-' …/requirements.md`；`grep -cE '^\| M-[0-9]+' …`；`grep -cE '^\| B-[0-9]+' …`；`grep -cE '^\| BC-[0-9]+' .specify/specs/107-decision-governance/plan.md` | **12 / 9 / 6 / 6** |
| 新交付物当前状态 | 逐个 `test -e`（owner page ×2 含镜像、checker ×2 含镜像、fixture 根、五支测试模块） | **10/10 ABSENT**（红先的前提） |
| 编辑 / 读取目标在位 | 逐个 `test -e`（15 个指针 / 生产者面 + 模板、生成器、框架地图、docs、register、glossary、既有测试与入口共 40 个路径） | **40/40 OK** |
| 指令活副本与预算 | `wc -c .specify/instructions.md`；`grep -n INSTRUCTIONS_BUDGET_BYTES scripts/bash/generate-instructions.sh`；`grep -c '^## ' templates/instructions-template.md` | live **38,894 B**；budget **38,912**（line 107）；top-level sections **38**；段上限先例 `**本节字节上限：2,000 B**`（line 57，唯一一处段上限字面量） |
| 旧式 `D-` 标题判别 | `grep -rn '^### D-' .specify/specs --include='*.md' \| wc -l`；`grep -rnE '^### D-[0-9]{3}' .specify/specs --include='*.md' \| wc -l` | **39** 条一/两位数标题；三位数记录形态 **0** 条 → 判别式安全。**陷阱形**：register 行不是标题行，本命令不计量它们 |
| `T-NNN` 标题计数 | `grep -cE '^### T-[0-9]{3}' .specify/specs/*/plan.md` 求和 | **104** = 既有 **101** + 本特性 plan 新增 T-001…T-003（plan 阶段读数 101 是当时快照，属 dated 读数） |
| 镜像 / 副本 / 门控基线 | `python3 scripts/python/sync-mirrors.py --check`；`python3 scripts/python/regen-command-copies.py --check`；`python3 scripts/python/scan-confirmation-gates.py --summary` | sync-mirrors rc **0**（6 对字节一致）；regen rc **0**（`OK: all per-tool command copies match the source templates.`）；门控 **31 blocking / 0 violations**（基线文件 `test-evidence/{sync-mirrors-baseline,regen-copies-baseline,scan-confirmation-gates-baseline}.txt`） |
| 受保护面既有测试在位 | 逐个 `test -e`（driver skill / efficiency / watch-iteration / role-transition payload / fast-fail discipline / decision-tension contract） | **6/6 OK** |

## Requirement Coverage Map

| FR | Rows | FR | Rows | FR | Rows |
|----|------|----|------|----|------|
| FR-001 | T004, T011, T012, T019, T026, T027, T033, T040 | FR-011 | T009, T011, T039, T041 | FR-021 | T032, T033, T036, T038 |
| FR-002 | T028, T034, T041, T049 | FR-012 | T018, T019, T022 | FR-022 | T039, T040, T045 |
| FR-003 | T027, T042, T045 | FR-013 | T018, T019, T022 | FR-023 | T039, T041, T045 |
| FR-004 | T025, T027 | FR-014 | T023, T026, T029, T031 | FR-024 | T039, T045 |
| FR-005 | T053 | FR-015 | T023, T026, T029 | FR-025 | T043, T045 |
| FR-006 | T011, T017 | FR-016 | T024, T026, T031 | FR-026 | T014, T015, T016, T048, T050 |
| FR-007 | T012, T013, T017 | FR-017 | T024, T027, T031 | FR-027 | T008, T016, T030, T037, T044, T050 |
| FR-008 | T011, T017 | FR-018 | T032, T033, T034, T035, T036, T038 | FR-028 | T024, T029, T031, T047, T052 |
| FR-009 | T011, T017 | FR-019 | T032, T033, T035, T036, T038 | FR-029 | T046, T047, T051, T052 |
| FR-010 | T011, T012, T014, T017 | FR-020 | T032, T033, T035, T038 | FR-030 | T049, T053 |

| SC | Rows |
|----|------|
| SC-001 | T042, T045 |
| SC-002 | T010, T013, T017 |
| SC-003 | T009, T011, T017, T039 |
| SC-004 | T018, T020, T022 |
| SC-005 | T023, T024, T029, T031 |
| SC-006 | T032, T036, T038 |
| SC-007 | T039, T045 |
| SC-008 | T048, T050 |
| SC-009 | T046, T047, T051, T052 |
| SC-010 | T015, T016, T048, T050 |

## Clause Coverage & Green Partition

38 条机器可判定条款逐条恰认领一次。测试编写行不携带 `[green:]`；认领落在各阶段末尾的验证行（写证据文件、运行测试），因此无 `green-path-divergence`、无 `green-clause-collision`，每份契约内认领序号随行序单调。

| Contract | Clause | Pinning test | Green point |
|----------|--------|--------------|-------------|
| `contracts/text-and-options.contract.md` | C-101 | `test_decision_governance_contracts.py::test_class_declaration_closed` | T017 |
| `contracts/text-and-options.contract.md` | C-102 | `test_decision_governance_contracts.py::test_full_name_minimum_bar_four_surfaces` | T017 |
| `contracts/text-and-options.contract.md` | C-103 | `test_decision_governance_guards.py::test_m02_locator_red_then_green` | T017 |
| `contracts/text-and-options.contract.md` | C-104 | `test_decision_governance_contracts.py::test_human_template_elements` | T017 |
| `contracts/text-and-options.contract.md` | C-105 | `test_decision_governance_contracts.py::test_ai_template_elements` | T017 |
| `contracts/text-and-options.contract.md` | C-106 | `test_validate_decisions.py::test_m03_option_set_reverse_samples` | T022 |
| `contracts/text-and-options.contract.md` | C-107 | `test_validate_decisions.py::test_ai_replay_deterministic` | T022 |
| `contracts/text-and-options.contract.md` | C-108 | `test_decision_governance_contracts.py::test_human_signal_pointer_only` | T022 |
| `contracts/text-and-options.contract.md` | C-109 | `test_decision_governance_contracts.py::test_review_surfaces_named` | T045 |
| `contracts/archive-and-audit.contract.md` | C-201 | `test_decision_governance_contracts.py::test_record_line_grammar` | T031 |
| `contracts/archive-and-audit.contract.md` | C-202 | `test_validate_decisions.py::test_m01_field_closure_reverse_samples` | T031 |
| `contracts/archive-and-audit.contract.md` | C-203 | `test_validate_decisions.py::test_m04_id_density_register` | T031 |
| `contracts/archive-and-audit.contract.md` | C-204 | `test_decision_governance_guards.py::test_broken_pointer_red` | T031 |
| `contracts/archive-and-audit.contract.md` | C-205 | `test_decision_governance_guards.py::test_no_tension_field_copy` | T031 |
| `contracts/archive-and-audit.contract.md` | C-206 | `test_decision_governance_guards.py::test_legacy_two_digit_reported_legacy` | T031 |
| `contracts/archive-and-audit.contract.md` | C-207 | `test_decision_governance_contracts.py::test_no_second_store` | T031 |
| `contracts/archive-and-audit.contract.md` | C-208 | `test_decision_governance_contracts.py::test_read_only_disposition_carrier` | T031 |
| `contracts/transmission-and-implementation.contract.md` | C-301 | `test_decision_governance_guards.py::test_m06_block_completeness` | T038 |
| `contracts/transmission-and-implementation.contract.md` | C-302 | `test_decision_governance_guards.py::test_m06_dispatch_without_block_refused` | T038 |
| `contracts/transmission-and-implementation.contract.md` | C-303 | `test_decision_governance_guards.py::test_acknowledgement_present` | T038 |
| `contracts/transmission-and-implementation.contract.md` | C-304 | `test_decision_governance_guards.py::test_m05_receipt_reverse_samples` | T038 |
| `contracts/transmission-and-implementation.contract.md` | C-305 | `test_decision_governance_guards.py::test_silent_redecision_is_anomaly` | T038 |
| `contracts/transmission-and-implementation.contract.md` | C-306 | `test_decision_governance_guards.py::test_m07_chain_three_segments` | T038 |
| `contracts/transmission-and-implementation.contract.md` | C-307 | `test_decision_governance_guards.py::test_multi_hop_same_id` | T038 |
| `contracts/transmission-and-implementation.contract.md` | C-308 | `test_decision_governance_guards.py::test_supersession_preserves_old` | T038 |
| `contracts/enforcement-boundary.contract.md` | C-401 | `test_decision_governance_guards.py`（逐 M 行） | T045 |
| `contracts/enforcement-boundary.contract.md` | C-402 | `test_decision_governance_contracts.py::test_behavior_surfaces_named` | T045 |
| `contracts/enforcement-boundary.contract.md` | C-403 | `test_decision_governance_guards.py::test_every_guard_has_reverse_sample` | T045 |
| `contracts/enforcement-boundary.contract.md` | C-404 | `test_validate_decisions.py::test_cli_surface` | T045 |
| `contracts/enforcement-boundary.contract.md` | C-405 | `test_decision_governance_contracts.py::test_gate_neutrality` | T045 |
| `contracts/enforcement-boundary.contract.md` | C-406 | `test_decision_governance_guards.py::test_inventory_closure` | T045 |
| `contracts/enforcement-boundary.contract.md` | C-407 | `test_decision_governance_guards.py::test_table_guard_parity` | T045 |
| `contracts/migration-and-compat.contract.md` | C-501 | `test_decision_governance_migration_map.py::test_bc_row_set_closed_and_mapped` | T052 |
| `contracts/migration-and-compat.contract.md` | C-502 | `test_decision_governance_migrate_dryrun.py::test_base_corpus_zero_rewrite` | T052 |
| `contracts/migration-and-compat.contract.md` | C-503 | `test_decision_governance_migrate_dryrun.py::test_instructions_generated_dimension` | T052 |
| `contracts/migration-and-compat.contract.md` | C-504 | `test_decision_governance_guards.py::test_m06_dispatch_without_block_refused` | T052 |
| `contracts/migration-and-compat.contract.md` | C-505 | `test_decision_governance_migration_map.py::test_no_fallback_only_row` | T052 |
| `contracts/migration-and-compat.contract.md` | C-506 | `test_decision_governance_contracts.py::test_mirror_and_copy_closure` | T052 |

## Feature Integration Review

- **Review performed at generation (2026-11-25)**: `.specify/features.md` 行 107 已为 `Planned`，其详情文件已承载 plan 阶段 Latest Review；tasks 阶段不推进生命周期、不新增 Feature、不使任何既有 Feature 失效。`Total Features` 不变。
- **Glossary**: `Decision` 类新词仍以 `origin=auto`、`status=proposed` 留在 run 证据（`test-evidence/glossary-proposal.md`、`test-evidence/glossary-proposal-plan-2026-11-25.md`），本特性不写 `.specify/glossary.md`（FR-005；T053 验证）。

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 先建立夹具与证据落点，并冻结实现前的可执行基线。

- [X] T001 Create the fixture tree `tests/fixtures/decision-governance/` with `m01`, `m02`, `m03`, `m04`, `m05`, `m06`, `m07`, `m08`, `m09`, `reconstruct`, `legacy`, `payload`, `chain` subdirectories (each with `.gitkeep`) and the evidence directory `.specify/specs/107-decision-governance/notes/`.
- [X] T002 [blockedBy: T001] Capture the pre-change side of every diff premise in `.specify/specs/107-decision-governance/notes/pre-change-measurements.md`: `wc -c .specify/instructions.md` (38894), `grep -n INSTRUCTIONS_BUDGET_BYTES scripts/bash/generate-instructions.sh` (line 107, 38912), `grep -rn '^### D-' .specify/specs --include='*.md' | wc -l` (39; three-digit form 0), plus the readings of `python3 scripts/python/sync-mirrors.py --check`, `python3 scripts/python/regen-command-copies.py --check`, `python3 scripts/python/scan-confirmation-gates.py --summary` and `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/107-decision-governance` — command, reading and capture date per row.
- [X] T003 [blockedBy: T001] Create the red-first evidence skeleton `.specify/specs/107-decision-governance/notes/red-first-evidence.md` with one slot per planned red-first test (M-01…M-09 reverse samples, C-102 four-surface, C-107 replay, C-204/C-205/C-206 guards, the payload/chain fixtures); each slot records command, real output and exit status; the failing-test baseline name list is captured by `/speckit.implement`'s `**Test runs**` owner and is referenced, never restated.

**Checkpoint**: fixture tree and evidence skeleton exist; every pre-change value is frozen before any edit.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 单一所有者页的骨架与检查器入口是所有故事的共同前置；两者必须先把「谁拥有什么」和「只读、可拒绝未声明选项」钉住。

**CRITICAL**: 本阶段完成前，任何用户故事不得开始。

- [X] T004 Author `shared/definitions/decision-definitions.md` § Ownership declaration and § Closed vocabulary: state up front that the page owns the vocabulary, class presentation, option-set contract, record field closure, transmission obligations, M/B boundary and legacy rules; list the nine closed terms (Decision Item, Decision Record, Option, Decision Block, Acknowledgement, Implementation Receipt, Decision Producer, Archive Projection, Decision Class) with one-line meanings; state the pointer-only duty to adjacent owners; wording MUST stay gate-neutral against `scripts/python/scan-confirmation-gates.py` `BLOCKING_PATTERNS`.
- [X] T005 [blockedBy: T004] Extend `tests/contract/test_decision_governance_contracts.py` with the foundational owner-page guards: the page exists at `shared/definitions/decision-definitions.md`; § Ownership declaration names every owned surface; § Closed vocabulary carries exactly the nine terms; no adjacent owner's criteria-table heading is restated in the page.
- [X] T006 [blockedBy: T001] Author `tests/unit/test_validate_decisions.py::test_cli_surface` red-first: `-h` and `--help` answer the same body, `--version` prints one line, an undeclared option exits non-zero, declared actions are exactly `records|payload|chain|inventory`, a run creates no file inside the repository (before/after snapshot), and exit codes are 0 = pass, 1 = documented check failed, 2 = input or argument error.
- [X] T007 [blockedBy: T006] Implement the read-only CLI skeleton `scripts/python/validate-decisions.py`: argparse surfaces `--action {records,payload,chain,inventory}`, `--spec PATH`, `--carrier PATH` (repeatable), `--fixture PATH`, `--register PATH`, `--glossary PATH`, `--json`, `--help`, `--version`; unrecognized options exit 2; a declared action not yet implemented exits 2 with an explicit message; the module resolves its root from its own path and satisfies `shared/definitions/script-interface-definitions.md`.
- [X] T008 [blockedBy: T004,T007] Regenerate and verify the Foundational mirror pairs: `python3 scripts/python/sync-mirrors.py --write`, then `python3 scripts/python/sync-mirrors.py --check` with no NEW drift against `test-evidence/sync-mirrors-baseline.txt`; `cmp` `shared/definitions/decision-definitions.md` with `.specify/shared/definitions/decision-definitions.md` and `scripts/python/validate-decisions.py` with `.specify/scripts/python/validate-decisions.py`.

**Checkpoint**: owner-page skeleton and checker CLI exist, are mirrored, and reject undeclared options.

---

## Phase 3: User Story 1 — 决策文本与两类强调 (Priority: P1)

**Goal**: 两条生产事故（简称、同名无定位）在决策文本层被挡住，两类决策各按自己的强调呈现并声明类别。

**Independent Test**: M-02 夹具（`same_name_conflict: true` 无 `resource_locator`）与 M-08 夹具（已登记 variant）分别转红、补全后转绿；同一决策按两类模板呈现时类别声明、必需要素与评审承接面差异成立；instruction 段含两条生产规则且 ≤1,500 B。

### Tests for User Story 1 (MANDATORY)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T009 [P] [US1] Author the US1 red-first contract tests in `tests/contract/test_decision_governance_contracts.py`: `test_class_declaration_closed` (C-101), `test_full_name_minimum_bar_four_surfaces` (C-102), `test_human_template_elements` (C-104), `test_ai_template_elements` (C-105); each fails on its own missing-surface assertion, never on an import error.
- [X] T010 [P] [US1] Author the US1 red-first guard tests and fixtures: `tests/contract/test_decision_governance_guards.py::test_m02_locator_red_then_green` and `::test_m08_registered_variant_red`, with `tests/fixtures/decision-governance/m02/` (record with `same_name_conflict: true` and empty `resource_locator` → red; business resource group + region id → green) and `tests/fixtures/decision-governance/m08/` (subject hits a stubbed glossary variant whose canonical exists → red; full name → green).

### Implementation for User Story 1

- [X] T011 [US1] [blockedBy: T004] Author `shared/definitions/decision-definitions.md` § Decision Classes and per-class presentation templates: class judged by holder (A-4); `human-interactive` template = plain-language question, context, per-option consequences/reversibility/default, full names and locator, wording per `shared/guidelines/user-facing-comprehension.md`; `ai-autonomous` template = closed options, explicit decision predicate/rule, explicit assumptions, machine-checkable evidence pointers, deterministic conclusion and reopening condition; class-mismatch routing to the B-03/B-04/B-06 review surfaces without any machine-coverage claim.
- [X] T012 [US1] [blockedBy: T011] Author `shared/definitions/decision-definitions.md` § Decision Text Contract: the two production rules as the minimum bar (full names, never an abbreviation alone; `same_name_conflict: true` plus machine-parseable `resource_locator` with the named-dimension floor business resource group + region id); the ban on presenting a same-name object without a locator; the per-class emphasis duties (FR-008/FR-009); name the B-01/B-02 review surfaces for completeness and locator adequacy.
- [X] T013 [US1] [blockedBy: T007,T010] Implement the `--action records` legs M-02 (`same_name_conflict: true` with empty `resource_locator` or fewer than two named dimensions → red) and M-08 (structured subject matches a registered glossary variant whose canonical exists → red; only registered words are covered) in `scripts/python/validate-decisions.py`; verdicts carry rule id, carrier path, line and message; the run mutates nothing.
- [X] T014 [US1] [blockedBy: T012] Add the whole section `## Decision Items（决策项）` to `templates/instructions-template.md` immediately after `## ID Register (编号登记)`: pointer form (owner-page pointer), the two production rules as the minimum bar, one line per class emphasis, and the literal `**本节字节上限：1,500 B**`; no copied table, no copied criteria, no gate-trigger wording.
- [X] T015 [US1] [blockedBy: T014] Raise `INSTRUCTIONS_BUDGET_BYTES` from 38,912 to 40,960 in `scripts/bash/generate-instructions.sh` (T-001 ruling) and regenerate `.specify/instructions.md` with `bash scripts/bash/generate-instructions.sh`; assert the `Decision Items` section is ≤1,500 B and the live total is <40,960 B; `cmp` the extracted section between template and live.
- [X] T016 [US1] [blockedBy: T012,T013,T014,T015] Regenerate and verify the US1 mirror pairs: `python3 scripts/python/sync-mirrors.py --write` then `--check` with no NEW drift; `cmp` `templates/instructions-template.md` with `.specify/templates/instructions-template.md` and `scripts/bash/generate-instructions.sh` with `.specify/scripts/bash/generate-instructions.sh`; `python3 scripts/python/regen-command-copies.py --check` rc 0.
- [X] T017 [US1] Run the US1 phase tests through the single entry `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh` against `tests/contract/test_decision_governance_contracts.py` (read-only) and `tests/contract/test_decision_governance_guards.py` (read-only); record the red-first slots and the green run in `notes/red-first-evidence.md` and `notes/us1-green.txt`, including the M-02 red→green and M-08 red→green outputs as SC-002 evidence; full-name rule presence is asserted on the four surfaces (owner page, instruction section, decision-item templates, guard fixtures + the named B-01/B-02 review surface). [green: contracts/text-and-options.contract.md#C-101] [green: contracts/text-and-options.contract.md#C-102] [green: contracts/text-and-options.contract.md#C-103] [green: contracts/text-and-options.contract.md#C-104] [green: contracts/text-and-options.contract.md#C-105] [blockedBy: T009,T010,T011,T012,T013,T014,T015,T016]

**Checkpoint**: 两条生产事故夹具红→绿；instruction 段与所有者页同时承载两条规则；类别模板差异由契约测试固定。

---

## Phase 4: User Story 2 — 封闭选项集 (Priority: P1)

**Goal**: 选项集封闭、可枚举、可比较，没有「其他」黑洞；AI 决策的选中项可由记录输入与谓词确定性重放。

**Independent Test**: 空选项集、重复标签、`other` 无 `path`、单选项未声明 `forced`、五要素缺失分别令 M-03 转红；补齐后转绿；重放测试对同一记录输入给出同一选中项。

### Tests for User Story 2 (MANDATORY)

- [X] T018 [P] [US2] Author the US2 red-first unit tests and fixtures: `tests/unit/test_validate_decisions.py::test_m03_option_set_reverse_samples` (empty set, duplicate label, `other` without `path`, and one missing element each → red; completed set → green) and `::test_ai_replay_deterministic` (recorded inputs plus the decision predicate re-derive the chosen option), with forward and reverse samples under `tests/fixtures/decision-governance/m03/`.

### Implementation for User Story 2

- [X] T019 [US2] [blockedBy: T012] Author `shared/definitions/decision-definitions.md` § Option-Set Contract: closed enumerable set with a declared count (0/1 degenerate cases included), the five elements per option (label, consequences, reversibility, default, evidence), unique labels, `other` legal only with a `path` (who/when/how adds options and writes back), a single viable option requires `forced` plus a reason, zero viable options is not a decision item; the chosen option is a named member; AI replayability duty; the human choice signal is reached by pointer to `shared/guidelines/confirmation-gates.md` without restating its value domain.
- [X] T020 [US2] [blockedBy: T013,T018] Implement the `--action records` M-03 leg and the chosen-member membership check in `scripts/python/validate-decisions.py`; verdicts carry rule id, carrier path, line and message; the run stays read-only.
- [X] T021 [US2] [blockedBy: T019] Extend `tests/contract/test_decision_governance_contracts.py` with `test_human_signal_pointer_only`: the owner page reaches the gate-observation signal vocabulary by pointer and does not restate its value domain.
- [X] T022 [US2] Run the US2 phase tests through the single entry `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh` against `tests/unit/test_validate_decisions.py` (read-only) and `tests/contract/test_decision_governance_contracts.py` (read-only); record green output and the M-03 reverse-sample outputs in `notes/red-first-evidence.md` and `notes/us2-green.txt`. [green: contracts/text-and-options.contract.md#C-106] [green: contracts/text-and-options.contract.md#C-107] [green: contracts/text-and-options.contract.md#C-108] [blockedBy: T018,T019,T020,T021]

**Checkpoint**: M-03 的每个退化形态可转红；重放一致；`other` 与 `forced` 规则由测试固定。

---

## Phase 5: User Story 3 — 既有载体归档与可重建 (Priority: P1)

**Goal**: 每个清单内生产者的决策落在其既有载体，只凭 register 与载体即可重建每条记录的适用层字段（基础层 + 触发成立的条件族）；旧记录报告 `legacy`、零改写。

**Independent Test**: 四类载体（requirements / plan / checkpoint / run report）夹具仅用 register + 载体重建每条记录的适用层全部字段（基础层 + 触发成立的条件族）；删除适用层必填字段或改坏指针令 M-01/M-04 转红；承重决策只交叉引用 `T-NNN`、不含六字段副本。

### Tests for User Story 3 (MANDATORY)

- [X] T023 [P] [US3] Author the US3 red-first unit tests and fixtures: `tests/unit/test_validate_decisions.py::test_m01_field_closure_reverse_samples` (missing base-layer field, a conditional field missing while its trigger holds, class outside the closed set, a malformed timepoint, a timepoint contradicting the `transmission_status` phase) and `::test_m04_id_density_register` (bad `D-NNN` form, non-dense per carrier, id unresolvable in the register stub), with `tests/fixtures/decision-governance/m01/` and `tests/fixtures/decision-governance/m04/` including a register stub.
- [X] T024 [P] [US3] Author the US3 red-first guard tests and fixtures: `tests/contract/test_decision_governance_guards.py::test_broken_pointer_red` (C-204, M-09: an unresolvable evidence pointer turns red, a resolvable one stays green), `::test_no_tension_field_copy` (C-205), `::test_legacy_two_digit_reported_legacy` (C-206) and `::test_reconstruct_from_register_and_carriers` over the four-carrier fixture set `tests/fixtures/decision-governance/reconstruct/` (requirements, plan, checkpoint, run report), with `tests/fixtures/decision-governance/legacy/` carrying one/two-digit legacy headings, a three-digit heading with zero field lines (legacy, not judged), an incomplete new-form block with exactly one C-201 field line (new-form → M-01 red) and legacy register rows (including `D-001`) — the pair pins C-206's minimal qualifying form in both directions — and `tests/fixtures/decision-governance/m09/` carrying a resolvable and a broken-pointer record pair (M-09 reverse sample).
- [X] T025 [P] [US3] Author the US3 red-first contract tests in `tests/contract/test_decision_governance_contracts.py`: `test_record_line_grammar` (C-201), `test_no_second_store` (C-207), `test_read_only_disposition_carrier` (C-208).

### Implementation for User Story 3

- [X] T026 [US3] [blockedBy: T019] Author `shared/definitions/decision-definitions.md` § Decision Record: the serialization grammar (`### D-NNN — <title>`, one `- **<field>**: <value>` line per field, indented option sub-lines, ≥2-space continuations, fenced blocks excluded), FR-014's layered grammar (the ten base-layer fields on every record; the conditional same-name family `same_name_conflict` + `resource_locator`; supersession via `superseded_by`; the phase-driven transmission timepoints `dispatched_at` / `acknowledged_at` / `implemented_at`, appended as `transmission_status` advances — no `not-yet` placeholder), supersession (old record retained, marked by `superseded_by`), id rules (`D-NNN`, dense per carrier, never reused, registered at birth, cross-carrier references carry the carrier pointer) and the reconstruction duty (no conversation-memory backfill).
- [X] T027 [US3] [blockedBy: T026] Author `shared/definitions/decision-definitions.md` § Archive as Projection and the normative Decision Producer Inventory (P-01…P-12 with obligation `record` / `record-when-decision` / `exempt`, carrier, class posture and owner); state archive-as-projection (union of producer × carrier plus the register index; no second registry, queue, store or scheduler), the read-only-disposition rule (a read-only command's disposition lands in its own report, never by editing the analyzed artifact) and the inventory-revision duty.
- [X] T028 [US3] [blockedBy: T027] Add one pointer line each to the record-side adjacent owners (pointer-only, no criteria table copied): `shared/guidelines/confirmation-gates.md` (P-01), `shared/guidelines/decision-tension.md` (P-03: a load-bearing decision appends a decision record cross-referencing its `T-NNN`, six fields not copied), `shared/guidelines/fast-fail.md` (P-07: after an adjudication the record and transmission obligations apply), `shared/definitions/goal-definitions.md`, `shared/definitions/anchor-definitions.md`, `shared/definitions/agent-definitions.md` (P-08) and `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` (P-04).
- [X] T029 [US3] [blockedBy: T020,T023] Implement the `--action records` legs M-01 (base-layer fields present, conditional fields present exactly when their trigger holds, class inside the closed set, timepoints well-formed and matching the `transmission_status` phase), M-04 (`D-NNN` form, dense and unique per carrier, id resolvable in the register) and M-09 (every evidence pointer resolves to an existing carrier path/anchor; only resolvability is judged, not sufficiency) plus the legacy discriminator (the minimal qualifying form: a `^### D-\d{3}` heading whose block carries at least one C-201 field line — a block at or above it is new-form even when incomplete and its missing fields are M-01's red, while every heading below it and every register row — including the id-shaped `D-001` row — is reported `legacy`, never judged or rewritten) in `scripts/python/validate-decisions.py`.
- [X] T030 [US3] [blockedBy: T027,T028,T029] Regenerate and verify the US3 mirror pairs: `python3 scripts/python/sync-mirrors.py --write` then `--check` with no NEW drift; `cmp` the owner page and every pointer-file pair (`shared/guidelines/{confirmation-gates,decision-tension,fast-fail}.md`, `shared/definitions/{goal,anchor,agent}-definitions.md`, `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` against their `.specify/` mirrors).
- [X] T031 [US3] Run the US3 phase tests through the single entry `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh` against `tests/unit/test_validate_decisions.py` (read-only), `tests/contract/test_decision_governance_guards.py` (read-only) and `tests/contract/test_decision_governance_contracts.py` (read-only); record the four-carrier reconstruction output, the `legacy` report, the broken-pointer red and the M-01/M-04 reverse outputs in `notes/red-first-evidence.md` and `notes/us3-green.txt`. [green: contracts/archive-and-audit.contract.md#C-201] [green: contracts/archive-and-audit.contract.md#C-202] [green: contracts/archive-and-audit.contract.md#C-203] [green: contracts/archive-and-audit.contract.md#C-204] [green: contracts/archive-and-audit.contract.md#C-205] [green: contracts/archive-and-audit.contract.md#C-206] [green: contracts/archive-and-audit.contract.md#C-207] [green: contracts/archive-and-audit.contract.md#C-208] [blockedBy: T023,T024,T025,T026,T027,T028,T029,T030]

**Checkpoint**: 四类载体可重建；旧记录报告 `legacy` 且未被判错；编号与分层字段闭包由守卫固定。

---

## Phase 6: User Story 4 — 决策完整跨过 superagent→subagent 边 (Priority: P1)

**Goal**: 派发载荷携带完整决策块，子代理回传确认与实施回执，结果钉回 `decision_id`；静默重决成为显式异常。

**Independent Test**: 一次夹具派发含完整决策块、回传含确认与 `implementation_receipt`；缺块派发被拒绝；上下文变化成为 fast-fail 上送；自行改选成为显式异常；记录 → 派发 → 回执三段链可解析。

### Tests for User Story 4 (MANDATORY)

- [X] T032 [US4] Author the US4 red-first guard tests and fixtures: `tests/contract/test_decision_governance_guards.py::test_m06_block_completeness` (FR-018), `::test_m06_dispatch_without_block_refused` (FR-018), `::test_acknowledgement_present` (FR-019), `::test_m05_receipt_reverse_samples` (FR-019), `::test_silent_redecision_is_anomaly` (FR-020), `::test_m07_chain_three_segments` (FR-021), `::test_multi_hop_same_id` (FR-021) and `::test_supersession_preserves_old` (FR-020), with payload/return snapshots under `tests/fixtures/decision-governance/{payload,chain,m05,m06,m07}/`.

### Implementation for User Story 4

- [X] T033 [US4] [blockedBy: T027] Author `shared/definitions/decision-definitions.md` § Transmission and Implementation: the `decision_block` five fields (`decision_id`, `decision_class`, chosen option full label, implementation constraints, archive pointer) riding the existing dispatch payload with the seven role fields and four injections unchanged; the acknowledgement; the `implementation_receipt` four fields (`decision_id`, implementation summary, evidence pointers, `divergence: none|diverged` plus reason) and the `transmission_status` update; no silent re-decision (fast-fail escalation at the anomaly point); the audit chain record → dispatch attempt → receipt; multi-hop same-id rule; re-decision supersession.
- [X] T034 [US4] [blockedBy: T033] Add the superagent pointer line in `shared/definitions/superagent-definitions.md` (the decision block travels in the existing payload as task-authority content, never an eighth role field) and the dispatch-side pointer in `skills/external/sdd-loop-driver/references/dispatch-recipes.md` and `skills/external/sdd-loop-driver/references/stage-prompts.md`.
- [X] T035 [US4] [blockedBy: T033] Add the producer duties to `skills/internal/run-agent/SKILL.md` and `skills/internal/run-team/SKILL.md`: build and validate the decision block before dispatch (FR-018), refuse a decision-backed dispatch without a complete block, require the acknowledgement and `implementation_receipt` on return (FR-019; an incomplete return is not consumed or backfilled), and route an invalidated decision to the fast-fail surface report (FR-020); owner-page pointers only.
- [X] T036 [US4] [blockedBy: T029,T032] Implement `--action payload` (M-06: decision-backed dispatch missing the block or any block field → red; non-decision dispatch without a block stays legal) and `--action chain` (M-05: receipt missing, or `decision_id` missing/unresolvable; M-07: any of record, dispatch attempt or receipt missing, or ids inconsistent) in `scripts/python/validate-decisions.py`; read-only, JSON verdicts.
- [X] T037 [US4] [blockedBy: T033,T034,T035,T036] Regenerate and verify the US4 mirror pairs: `python3 scripts/python/sync-mirrors.py --write` then `--check` with no NEW drift; `cmp` `shared/definitions/superagent-definitions.md`, the two driver references and the two skill files against their `.specify/` mirrors.
- [X] T038 [US4] Run the US4 phase tests through the single entry `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh` against `tests/contract/test_decision_governance_guards.py` (read-only); record the dispatch round-trip snapshots, the refusal output, the silent-redecision anomaly and the chain readings in `notes/red-first-evidence.md` and `notes/us4-green.txt`. [green: contracts/transmission-and-implementation.contract.md#C-301] [green: contracts/transmission-and-implementation.contract.md#C-302] [green: contracts/transmission-and-implementation.contract.md#C-303] [green: contracts/transmission-and-implementation.contract.md#C-304] [green: contracts/transmission-and-implementation.contract.md#C-305] [green: contracts/transmission-and-implementation.contract.md#C-306] [green: contracts/transmission-and-implementation.contract.md#C-307] [green: contracts/transmission-and-implementation.contract.md#C-308] [blockedBy: T032,T033,T034,T035,T036,T037]

**Checkpoint**: 决策块完整性与拒绝、确认与回执、三段链、多跳同号、取代保留全部可测。

---

## Phase 7: User Story 5 — 强制是诚实的 (Priority: P2)

**Goal**: 每条 M 规则有可转红守卫与逆向样本，每条 B 规则有具名评审承接面；不加阻塞门控，哨兵 / watcher / 两槽预算按 FR-025 的具名基线零漂移。

**Independent Test**: 逐守卫做变异/逆向演练，全部转红且定位到规则；B-01…B-07 各有具名承接面；`scan-confirmation-gates.py` 相对基线 `test-evidence/scan-confirmation-gates-baseline.txt` 零新增命中。

### Tests for User Story 5 (MANDATORY)

- [X] T039 [US5] [blockedBy: T036] Author the US5 enforcement tests in `tests/contract/test_decision_governance_guards.py` and `tests/contract/test_decision_governance_contracts.py`: `::test_every_guard_has_reverse_sample` (C-403), `::test_inventory_closure` (C-406: declared producer set from the owner page against the documented code-face scan output, verdict `observed == declared ± exempt`, FR-022/FR-024/FR-025), `::test_table_guard_parity` (C-407), `test_behavior_surfaces_named` (C-402, B-01…B-07), `test_gate_neutrality` (C-405, FR-025) and `test_review_surfaces_named` (C-109).
- [X] T040 [US5] [blockedBy: T033] Author `shared/definitions/decision-definitions.md` § Enforcement Boundary: the M table (M-01…M-09 each with exactly one deterministic judge action and one red condition) and the B table (B-01…B-07 each with its named review surface and the explicit no-machine-coverage statement), plus the table–guard parity duty and the gate-neutrality duty (no new blocking gate; FR-022).
- [X] T041 [US5] [blockedBy: T040] Add the B-rule review-surface pointers: `skills/internal/analyze-artifacts/SKILL.md` (B-04/B-05/B-07), `skills/internal/review-feature-quality/SKILL.md` and `skills/internal/review-sdd-process/SKILL.md` (B-01…B-07); pointer-only, no rule text copied (FR-023).
- [X] T042 [US5] [blockedBy: T027,T036] Implement `--action inventory` in `scripts/python/validate-decisions.py`: parse the declared producer set from the owner page's inventory table, accept the observation set from the documented code-face scan output supplied by the caller, and emit `observed == declared ± exempt` with a red verdict on any unregistered producer that yields a decision item (FR-022, SC-001).
- [X] T043 [US5] [blockedBy: T041,T042] Run the gate-neutrality scan and record it: `python3 scripts/python/scan-confirmation-gates.py --summary` compared to `test-evidence/scan-confirmation-gates-baseline.txt` (31 blocking / 0 violations, zero NEW hits) into `test-evidence/gate-neutrality.txt`; assert the FR-025 preservation reading against the effective baseline (default `fbab7a45c`; replaced only by a recorded re-baseline ruling) by read-only `git diff --quiet <effective baseline>..HEAD -- shared/declarations/facts/driver-completion-sentinels.yaml skills/external/sdd-loop-driver/references/watch-model.md skills/external/sdd-loop-driver/references/efficiency-model.md` (rc 0, zero `--numstat` rows; the allowed-delta set is unconditionally empty and any three-path change must land with its FR-025 re-baseline ruling in the same commit) and assert the payload field counts (seven role fields + four injections + five-item uplink) are unchanged per EP-002 (FR-025).
- [X] T044 [US5] [blockedBy: T041,T042] Regenerate and verify the US5 mirror pairs: `python3 scripts/python/sync-mirrors.py --write` then `--check` with no NEW drift; `cmp` the analyze/review skill pairs; `python3 scripts/python/regen-command-copies.py --check` rc 0.
- [X] T045 [US5] Run the US5 phase tests through the single entry `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh` against `tests/contract/test_decision_governance_guards.py` (read-only) and `tests/contract/test_decision_governance_contracts.py` (read-only); execute each M guard's reverse sample and record its red output in `notes/red-first-evidence.md`; write the per-guard drill summary to `test-evidence/mutation-drill.md`; record the enforcement tables versus guard-roster parity and the B-surface list. [green: contracts/enforcement-boundary.contract.md#C-401] [green: contracts/enforcement-boundary.contract.md#C-402] [green: contracts/enforcement-boundary.contract.md#C-403] [green: contracts/enforcement-boundary.contract.md#C-404] [green: contracts/enforcement-boundary.contract.md#C-405] [green: contracts/enforcement-boundary.contract.md#C-406] [green: contracts/enforcement-boundary.contract.md#C-407] [green: contracts/text-and-options.contract.md#C-109] [blockedBy: T039,T040,T041,T042,T043,T044]

**Checkpoint**: 变异演练逐条转红；B 面全部具名；门控读数不变。

---

## Phase 8: User Story 6 — 落地、镜像、客户接收与旧记录零改写 (Priority: P2)

**Goal**: 能力随框架源分发；镜像与副本同批再生成；下游项目经 init 收到 instruction 段；旧记录原样保留；不兼容变更闭合。

**Independent Test**: 镜像检查与副本检查；空客户项目 init 夹具收到该段；旧记录经 diff 行级比较零改写；BC 行逐条跑 dry-run 与拒绝/迁移证据。

### Tests for User Story 6 (MANDATORY)

- [X] T046 [P] [US6] Author the BC closure guard `tests/contract/test_decision_governance_migration_map.py`: `test_bc_row_set_closed_and_mapped` (the plan's inventory rows equal `{BC-01…BC-06}`; every row names a resolution and an existing test path; an unmapped row turns it red) and `test_no_fallback_only_row` (no row is resolved solely by a runtime dual-path fallback or a manual instruction).
- [X] T047 [P] [US6] Author the migrate/legacy integration test `tests/integration/test_decision_governance_migrate_dryrun.py`: `test_instructions_generated_dimension` (a `specify migrate --dry-run --format json` plan lists the `.specify/instructions.md` convergence item under the existing `templates-generated` dimension; the dimension set gains no seventh member) and `test_base_corpus_zero_rewrite` (line-level containment over the base-corpus paths at `08b59695c`: no pre-existing line removed or changed; appended rows allowed; old-form records reported `legacy`).

### Implementation for User Story 6

- [X] T048 [US6] [blockedBy: T015] Extend `tests/contract/test_decision_governance_contracts.py` with the landing closures: `test_mirror_and_copy_closure` (sync-mirrors no NEW drift against the baseline, `regen-command-copies.py --check` rc 0, template/live extracted section `cmp`, section ≤1,500 B, total <40,960 B; FR-026/FR-027) and `test_client_init_receives_section` (a throwaway `specify init --here --ai qoder --script sh --no-git` workspace receives the `Decision Items` section and both production rules; SC-010).
- [X] T049 [US6] [blockedBy: T027] Add the framework documentation pointers: one row in `shared/definitions/framework-map.md` for the owner page (what/where/owner/lifecycle/content class, framework source `shared/definitions/`) and one pointer line in `docs/concepts/spec-driven.md`; no rule text copied (FR-030).
- [X] T050 [US6] [blockedBy: T016,T030,T037,T044,T048,T049] Regenerate and verify the full landing surface: `python3 scripts/python/sync-mirrors.py --write` then `--check` with no NEW drift against the baseline; `cmp` every touched pair from plan § Mirror Obligations; `python3 scripts/python/regen-command-copies.py --check` rc 0; `bash scripts/bash/generate-instructions.sh` then `cmp` the extracted section and re-check the two byte budgets (FR-026/FR-027, SC-008).
- [X] T051 [US6] [blockedBy: T046,T047,T050] Produce the migration closure evidence `test-evidence/migration-closure.md`: for each BC-01…BC-06 row run its named behavior and record the command, output and pinning test; run the `specify migrate --dry-run --format json` fixture and record the `templates-generated` convergence item; assert no seventh migrate dimension (dimension set read from `src/specify_cli/__init__.py`).
- [X] T052 [US6] Run the US6 phase tests through the single entry `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh` against `tests/contract/test_decision_governance_migration_map.py` (read-only), `tests/integration/test_decision_governance_migrate_dryrun.py` (read-only) and `tests/contract/test_decision_governance_contracts.py` (read-only); record the mirror/copy/instruction readings, the client-init tree and the zero-rewrite line-level reading in `notes/us6-green.txt` and `test-evidence/migration-closure.md`. [green: contracts/migration-and-compat.contract.md#C-501] [green: contracts/migration-and-compat.contract.md#C-502] [green: contracts/migration-and-compat.contract.md#C-503] [green: contracts/migration-and-compat.contract.md#C-504] [green: contracts/migration-and-compat.contract.md#C-505] [green: contracts/migration-and-compat.contract.md#C-506] [blockedBy: T046,T047,T048,T049,T050,T051]

**Checkpoint**: 镜像与副本干净；客户项目收到 instruction 段；旧记录零改写；BC 行逐条有执行证据。

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: 收口词汇表纪律、受保护面回归、quickstart 实录与验收证据包。

- [X] T053 Verify the glossary proposal-only discipline: `.specify/glossary.md` carries no new Decision term (read-only `git diff d05c3a350..HEAD -- .specify/glossary.md` empty) and the proposal evidence (`test-evidence/glossary-proposal.md`, `test-evidence/glossary-proposal-plan-2026-11-25.md`) remains the only glossary deliverable; no write without user confirmation (FR-005).
- [X] T054 [blockedBy: T052] Run the preservation regression sweep through the single entry: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py tests/contract/test_sdd_loop_driver_watch_iteration.py tests/contract/test_sdd_loop_driver_efficiency.py tests/contract/test_role_transition_payload.py tests/contract/test_fast_fail_discipline.py tests/contract/test_decision_tension_contract.py -q`; record the zero-new-failure reading and the FR-025 preservation reading (the three-path `git diff --quiet <effective baseline>..HEAD` rc 0 / zero `--numstat` rows against the effective baseline — default `fbab7a45c`, replaced only by a recorded re-baseline ruling) plus the EP-002 payload field-count statement in `test-evidence/preservation-sweep.txt`.
- [X] T055 [blockedBy: T052] Execute every scenario in `.specify/specs/107-decision-governance/quickstart.md` exactly as written (the executed-today commands re-run; the planned-surface commands run after landing) and record command, output and exit status per scenario in `notes/quickstart-run.md`, teardown included.
- [X] T056 [blockedBy: T052,T053,T054,T055] Assemble the crew-side close-out input `.specify/specs/107-decision-governance/test-evidence/verification-input.md`: record SC-001…SC-010 each with status, command and evidence pointer; the `final`-path criteria (SC-001…SC-006, SC-010) carry `pass` plus the smoke record (`smoke_command=`, `smoke_exit_code=0`, `smoke_evidence_path=` existing and non-empty); the supporting criteria (SC-007…SC-009) record their drill/mirror/migration evidence. `verification.md` is derived spec-side from this input and MUST NOT be written by the crew (handoff/team forbidden list).

**Checkpoint**: 词汇表未变；受保护面零新增失败；quickstart 有实录；`test-evidence/verification-input.md` 可直接派生 `verification.md` 进入 review。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，可立即开始。
- **Foundational (Phase 2)**: 依赖 Setup — 阻塞全部用户故事。
- **User Stories (Phase 3–8)**: 依赖 Foundational；六个故事共享同一所有者页与同一检查器，故按顺序推进（US1 → US2 → US3 → US4 → US5 → US6），各故事的检查点独立可测。
- **Polish (Phase 9)**: 依赖 US6 完成。

### User Story Dependencies

- **US1（P1）**: Foundational 之后即可开始；产出所有者页 §3/§4、instruction 段与 M-02/M-08。
- **US2（P1）**: 依赖 US1 的 §4 位置（同一文件续写）与 `--action records` 骨架；检查点独立。
- **US3（P1）**: 依赖 US2 的选项契约（记录字段引用选项闭集）；检查点独立。
- **US4（P1）**: 依赖 US3 的记录与档案指针（决策块引用档案与编号）；检查点独立。
- **US5（P2）**: 依赖 US4 的检查器 action 全集；负责强制面审计与变异演练。
- **US6（P2）**: 依赖 US1 的 instruction 段与全部前序镜像面；负责分发、客户接收与迁移收口。

### Within Each User Story

- 测试先写并转红；实现随后使其转绿；验证行记录红先证据与绿点。
- 同一文件的章节按行序追加，不并行写同一所有者页。
- 每个故事末尾的验证行是 `[green:]` 认领点；测试编写行不认领。

### Parallel Opportunities

- Setup / Foundational 无 `[P]`（同一所有者页与检查器串行）。
- US1 的 T009 与 T010 可并行（契约测试文件 vs 守卫测试与夹具）。
- US3 的 T023、T024、T025 可并行（单元测试、守卫测试与夹具、契约测试三组写目标互不相同）。
- US6 的 T046 与 T047 可并行（迁移映射守卫 vs migrate dry-run 集成测试）。

---

## Parallel Example: User Story 3

```bash
# Launch the three US3 test-authoring rows together (distinct write targets):
Task: "Author m01/m04 unit tests in tests/unit/test_validate_decisions.py"
Task: "Author guard tests and four-carrier fixtures in tests/contract/test_decision_governance_guards.py + tests/fixtures/decision-governance/reconstruct/"
Task: "Author grammar/no-second-store/read-only contract tests in tests/contract/test_decision_governance_contracts.py"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 + US2（决策文本与选项集）。两者同为 P1，且「文本规则落地但选项不封闭」会把无法比较的选项带进后续归档与传递；两者合并构成决策项质量的最小可交付增量。US3（归档）、US4（传递）各自是独立可测的增量；US5 与 US6 是强制诚实与分发收口。

1. 完成 Phase 1 + Phase 2（地基）。
2. 完成 US1 + US2 并各自通过检查点。
3. **STOP and VALIDATE**: 用 US1/US2 的独立测试标准验证。
4. 依次交付 US3 → US4 → US5 → US6。

### Incremental Delivery

1. Setup + Foundational → 所有者页骨架与检查器入口就绪。
2. US1 → 两条生产事故被挡住（MVP 第一半）。
3. US2 → 选项集封闭（MVP 第二半）。
4. US3 → 归档可重建。
5. US4 → 传递与回执可审计。
6. US5 → 强制审计诚实。
7. US6 → 分发、镜像、客户接收与迁移收口。

### Parallel Team Strategy

单执行体（本线 `single-unit`）。若后续拆并行：测试编写行可按上表 `[P]` 分组；所有者页与检查器永不由两个执行体同时写。

---

## Notes

- **FR-002 的 `register.md` 读法**：plan § Project Structure 的落地面是封闭清单，其中不含 `register.md`；`.specify/register.md` 保持编号登记事实，由所有者页与测试以指针抵达，本特性不向 register 添加指针行（也不改写既有行）。新增 `D-NNN` 行只会在将来真实决策记录诞生时按 FR-015 追加。
- **C-102 的四面对读法**：四面对 = 所有者页、instruction 段、决策项模板（所有者页 §3）、守卫/评审面；其中评审面在 US1 由所有者页点名的 B-01/B-02 承接，US5 把它接进 `analyze-artifacts` / `review-*` 技能（C-402），因此 C-102 的绿点可诚实落在 T017。
- **client-init 测试的落点**：为保持 plan 的封闭测试文件清单，`test_client_init_receives_section` 落在 `tests/contract/test_decision_governance_contracts.py`，复用既有 `specify init --here … --no-git` 夹具形态（`tests/integration/test_init_new_layout.py` 为先例）。
- **零改写读数**：`08b59695c` 以来 `.specify/register.md` 已由 plan 阶段追加 T-019…T-021 三行；因此 C-502 的判定是**行级包含**（既有无一行被删除或改写，允许追加；`git diff --numstat` 删除列 = 0 且无删除文件），不是文件级空 diff。文件级空 diff 只适用于本特性未触碰的记录路径。
- **绿点分区**：38 条全部由六个阶段验证行认领，测试编写行不带 `[green:]`；`validate-tasks.py` 的四项 green 检查应零 ERROR，出现的 WARN 逐条裁定并记录在 `test-evidence/tasks-validator.txt`。
- **测量陷阱**：条款计数单位是行首 `- **C-NNN**` 定义行（`grep -c 'C-'` 会误计正文引用）；`T-NNN` 标题现值 104 = 既有 101 + 本特性 plan 新增 3；旧式 `D-` 判别只对标题行计数，register 行另由 legacy 夹具覆盖。
- **门控中性**：所有者页与 instruction 段都位于 `scan-confirmation-gates.py` 的扫描面（`shared`、`templates/*.md`），措辞 MUST 避开 `BLOCKING_PATTERNS`（例如不得出现 `confirmation gate` / `确认门控/确认门禁` 字面量）。
- **`[P]` 与写目标**：`[P]` 只用于写目标逐行不同的测试编写行；所有者页、检查器、镜像 fan-out 与共享证据 sink 一律按行序串行。
- **PLAN-EDIT**: 无。本文件未改动任何 plan-owned 路径；测试文件、owner page、instruction 段位置与检查器 action 集均取自 plan 的封闭清单。
