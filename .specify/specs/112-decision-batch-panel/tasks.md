# Tasks: Batch Decision Panel（批量决策面板）

**Requirement ID**: 112
**Requirement Key**: `112-decision-batch-panel`
**Related Feature**: 112 Batch Decision Panel（批量决策面板） — `.specify/features.md` 行 112；本阶段维持 `Planned`，不推进生命周期
**Input**: Design documents from `.specify/specs/112-decision-batch-panel/`
**Prerequisites**: plan.md（Technical Context / Project Structure / Mirror Obligations / EP-001…EP-007 / Inherited Blockers）、requirements.md（45 FR / 10 SC / A-1…A-27 / 13 clarification rows / STR-001…STR-015）、research.md（M-1…M-14 / D-1…D-12）、data-model.md（E-1…E-13 / I-1…I-22 / 5 state domains）、contracts/ ×6（C-101…C-110 / C-201…C-208 / C-301…C-307 / C-401…C-409 / C-501…C-512 / C-601…C-608）、quickstart.md（7 scenarios）、feature-ref.md

**Tests Mode**: ON（Constitution Principle IV "Test-First & Contract-Driven Implementation" — “Write or update tests BEFORE implementing new behavior (Red-Green-Refactor)” 以及 unit / regression / contract 三条 MUST；本特性交付可执行引擎、检查器扩展与守卫夹具，测试形态为 unit / contract 两层运行时测试；文档面（所有者页、命令模板、技能、命令文档）由结构契约测试承接，不冒充运行时测试。M-10…M-16 的逆向样本与冻结基线同批更新。）

**Tests**: 红先证据的唯一落点 `.specify/specs/112-decision-batch-panel/notes/red-first-evidence.md`（每支测试一条：命令、真实输出、退出码）。失败测试名集的捕获与比较形式归 `/speckit.implement` 的 `**Test runs**` owner，本文件只给路径与命令。测试执行唯一入口 `bash scripts/bash/run-tests.sh`；解释器解析见 § Environment Prerequisites。

**Organization**: 按用户故事组织——US1（一次集中呈现全部待决策项，P1）、US2（只对异议发声、其余合格项按建议默认值结案，P1）、US3（处置落进既有载体、整批可只凭记录重放，P1）、US4（完备性是诚实的：记账、拒绝、空集明说，P2）、US5（重决不覆盖前例；人工与自主不混淆；零传输，P2）。

## Definition of Done (DoD)

- DoD-1: 全部任务行为 `[X]`；若出现 `[~]`，其理由逐条记录在 `.specify/specs/112-decision-batch-panel/test-evidence/verification-input.md` 的 `deferred_tasks=`（`verification.md` 由 spec 侧从该输入派生）。
- DoD-2: 交付面齐备——所有者页批次扩展（8 个新词使词汇 9 → 17、P-13、3 个批次族条件字段、M-10…M-16、B-08/B-09）、`templates/commands/decide.md`、`skills/internal/decide-batch/SKILL.md`（含编译后的 `## Wrap-up`）、`scripts/python/decision-batch.py`（`scan` / `record` / `replay`）、`scripts/python/validate-decisions.py` 的批次族字段闭包、`docs/reference/commands/decide.md`、`shared/definitions/framework-map.md` 的决策治理行。
- DoD-3: 54 条契约条款逐条恰认领一次并在其绿点行转绿；M-10…M-16 每条都有可转红的逆向样本，B-08/B-09 各有具名评审承接面，文档与测试均不声称机器覆盖行为类判断。
- DoD-4: 完备性、拒绝、`nothing-pending` 与记账恒等式可实测复现；批次记录、register 登记与状态单元格、`resolution` 标注、只凭记录的重放均成立。
- DoD-5: 冻结基线同批移动——命令 33 / 技能 61 / probe 注册面按实测计数更新；镜像与每工具命令副本零新增漂移；fresh `specify init` 夹具收到命令与技能。
- DoD-6: 零新存储根、零 `.specify/.gitignore` 变更、零运行期存储布局变更、`.specify/instructions.md` § Decision Items 段逐字不变（1,276 B）、无第二所有者页或第二记录 schema、零网络访问、零反馈存储写入、零自动传输。
- DoD-7: SC-001…SC-010 在 `test-evidence/verification-input.md` 逐条记录状态、命令与证据指针；`final` 路径判据（SC-001…SC-007、SC-010）记 `pass` 并带 smoke 记录（`smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=` 存在且非空）。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/112-decision-batch-panel/tasks.md` exit 0（0 error；WARN 逐条裁定并记录在 `test-evidence/tasks-validator.txt`）。
- GATE-2: 跨产物一致 — check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/112-decision-batch-panel --stage tasks --repo .` 输出 `decision=pass` 且 errors=0（advisory 逐条裁定）。
- GATE-3: FR / SC / 条款覆盖 — check: 本文件 § Requirement Coverage Map 覆盖 45 条 FR 与 10 条 SC；§ Clause Coverage & Green Partition 的 54 条逐条恰认领一次；`pre-analyze-check.py --stage tasks` 的 `runtime-stack-row` errors=0（in-scope 运行时行的每个 FR 至少被一个任务行行首引用）。
- GATE-4: final 路径成功判据 + smoke 记录 — check: `verification.md` 中 `**Path**` 为 `final` 的 SC-001…SC-007 与 SC-010 全部 `pass`，且 `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`（存在且非空）齐备（条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates）。
- GATE-5: 镜像、副本与指令收敛 — check: `python3 scripts/python/sync-mirrors.py --check` 的漂移成员集相对 `notes/pre-change-measurements.md` 记录的基线无新增成员；`python3 scripts/python/regen-command-copies.py --check` exit 0；`cmp` 抽取的 `## Decision Items` 段为空且段字节 = 1,276 B；`git diff --stat` 对 `.specify/.gitignore` 与运行期存储布局为空。
- GATE-6: 门控中性 — check: `python3 scripts/python/scan-confirmation-gates.py --summary` 相对 `test-evidence/scan-confirmation-gates-baseline.txt`（30 blocking / 0 violations）零新增命中。
- GATE-7: 冻结基线与 probe 注册面 — check: `tests/contract/test_migration_distribution.py` 的命令/技能集合与磁盘实际集合相等（生成时读数 32 → 33、60 → 61）；`tests/contract/test_probe_nonentity_catalog.py` 的字面量等于实测注册对象数（生成时读数 130，新增一个 skill 对象后按实测复测）。
- GATE-8: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/112-decision-batch-panel/tasks.md` 返回 0。

## Environment Prerequisites

- CPython: **available** — probe: `python3 --version` → `Python 3.11.11` @ 2026-11-27；affected: 全部引擎行与测试行。
- pytest（经唯一测试入口）: **unavailable in this worktree** — probe: `bash scripts/bash/run-tests.sh tests/contract/test_migration_distribution.py -q` → `error: no interpreter with pytest found (tried SPECKIT_PYTHON, .venv/bin/python, python3, python)` @ 2026-11-27；affected: 全部测试执行行（T023、T032、T039、T045、T052、T055、T058）。实现阶段 MUST 按 runner 的解释器阶梯解析出带 pytest 的解释器；若仍不可得，测试行保持阻塞并如实上报，MUST NOT 声称绿。
- bash / git: **available** — probe: `bash --version` → `4.4.20(1)-release`；`git --version` → `2.43.5` @ 2026-11-27；affected: 镜像 / 副本 / 证据行。
- 容器运行时 / 镜像仓库 / 活集群 / 外网: **none** — 本特性全部动作是本地文本读写、`git`、CPython 与既有 CLI，无构建、无拉取、无网络、无守护进程 @ 2026-11-27；affected: none。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标逐行不同、无未完成依赖）。本文件的 `[P]` 只出现在测试编写行与彼此独立的文档行。
- **[Story]**: 用户故事标签（`[US1]`…`[US5]`），只出现在用户故事阶段的任务行；Setup / Foundational / Polish 阶段零 `[US` 标记。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全 `[X]` 前不得开始本行。仅阶段顺序关系时不写。
- **[green: <contract>#<clause>]**: 绿点认领——本行是该条款首次转绿的验证行；契约路径相对本文件目录解析。54 条分区：source-roster C-101…C-110、presentation C-201…C-207、default-derivation C-301…C-307 → T023；objection-reply C-401…C-409、record-replay C-501…C-504 → T032；record-replay C-505…C-508 → T039；completeness-refusal C-601…C-608 → T045；presentation C-208、record-replay C-509…C-512 → T052。每条恰一行认领，认领行序与条款序号单调一致；测试编写行不携带 `[green:]`。
- 每行必须单行完成（含文件路径与全部标签），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `test-evidence/verification-input.md` 的 `deferred_tasks=`，spec 侧派生进 `verification.md`）。

## Path Conventions

- **框架源（编辑面）**: `shared/`、`skills/`、`scripts/`、`templates/`、`docs/`、`tests/`。
- **生成面（MUST NOT 手改）**: `.specify/shared/**`、`.specify/skills/**`、`.specify/scripts/**`（由 `sync-mirrors.py` 投影）；每工具命令副本 `.claude/commands/speckit.decide.md`、`.github/prompts/speckit.decide.prompt.md`、`.qoder/commands/speckit.decide.md`、`.opencode/command/speckit.decide.md`（由 `regen-command-copies.py` 生成）。
- **证据落点（本特性）**: `.specify/specs/112-decision-batch-panel/notes/` 下的 `pre-change-measurements.md`、`red-first-evidence.md`、`us1-green.txt`…`us5-green.txt`、`quickstart-run.md`；`test-evidence/` 下的 `scan-confirmation-gates-baseline.txt`、`tasks-validator.txt`、`verification-input.md`；覆盖基线 `coverage-baseline.txt`。
- **只读面（零修改）**: `.specify/specs/112-decision-batch-panel/{plan.md,data-model.md,contracts/,quickstart.md,research.md,feature-ref.md}`（plan-owned；仅在必须时以小修落盘并声明）；`.specify/instructions.md`；`.specify/.gitignore`；`.specify/register.md` 的既有行（本特性只在运行期由批次追加）；其他规格的 `.specify/specs/**` 与 `.specify/features/**`。
- **共享写入面（串行）**: `shared/definitions/decision-definitions.md`（各故事阶段依次追加章节）、`scripts/python/decision-batch.py`（各故事阶段依次加动作腿）、`scripts/python/validate-decisions.py`。

## Requirement Coverage Map

| FR | Rows | FR | Rows | FR | Rows |
|----|------|----|------|----|------|
| FR-001 | T007, T015, T016, T017, T018, T026, T027, T028, T034, T035, T041, T048 | FR-016 | T040, T041, T042, T043 | FR-031 | T024, T027, T029 |
| FR-002 | T007 | FR-017 | T040, T041, T043 | FR-032 | T024, T028, T030 |
| FR-003 | T007, T047, T049 | FR-018 | T040, T041, T043 | FR-033 | T024, T028, T030 |
| FR-004 | T028, T036, T047, T056 | FR-019 | T013, T017, T021 | FR-034 | T033, T034, T036 |
| FR-005 | T047, T056 | FR-020 | T014, T017, T021 | FR-035 | T033, T034, T036 |
| FR-006 | T013, T015, T019 | FR-021 | T013, T018, T020 | FR-036 | T033, T035, T037 |
| FR-007 | T013, T015, T019 | FR-022 | T013, T018, T020 | FR-037 | T024, T028, T030, T033, T036 |
| FR-008 | T013, T015, T016, T019 | FR-023 | T013, T018, T020 | FR-038 | T047 |
| FR-009 | T013, T015, T019 | FR-024 | T024, T027, T029 | FR-039 | T005, T006, T008, T009, T019, T037, T055, T056 |
| FR-010 | T013, T015, T019 | FR-025 | T013, T017, T021 | FR-040 | T024, T026, T029 |
| FR-011 | T013, T017, T019 | FR-026 | T024, T026, T029 | FR-041 | T013, T017, T047 |
| FR-012 | T013, T019, T034 | FR-027 | T024, T026, T027, T029 | FR-042 | T011, T012, T054, T055, T056 |
| FR-013 | T013, T019 | FR-028 | T024, T027, T029 | FR-043 | T053 |
| FR-014 | T013, T017, T021 | FR-029 | T046, T048, T050 | FR-044 | T013, T024, T033, T040, T046, T049, T058 |
| FR-015 | T040, T041, T043 | FR-030 | T025, T027 | FR-045 | T047, T048 |

| SC | Rows |
|----|------|
| SC-001 | T013, T040, T043, T045 |
| SC-002 | T013, T021, T023 |
| SC-003 | T013, T020, T023 |
| SC-004 | T024, T029, T032 |
| SC-005 | T024, T030, T034, T037, T039 |
| SC-006 | T046, T050, T052 |
| SC-007 | T013, T024, T047, T052 |
| SC-008 | T047, T048, T052 |
| SC-009 | T011, T012, T055, T056, T058 |
| SC-010 | T013, T024, T033, T036, T058 |

## Clause Coverage & Green Partition

54 条机器可判定条款逐条恰认领一次。测试编写行不携带 `[green:]`；认领落在各阶段末尾的验证行（运行测试并写证据文件），因此无 `green-path-divergence`、无 `green-clause-collision`，每份契约内认领序号随行序单调。

| Contract | Clause | Pinning test | Green point |
|----------|--------|--------------|-------------|
| `contracts/source-roster.contract.md` | C-101 | `test_decision_batch_engine.py::test_roster_closed_and_predicates` | T023 |
| `contracts/source-roster.contract.md` | C-102 | `test_decision_batch_engine.py::test_incomplete_block_still_candidate` | T023 |
| `contracts/source-roster.contract.md` | C-103 | `test_decision_batch_contract.py::test_block_grammar_owner_extension` | T023 |
| `contracts/source-roster.contract.md` | C-104 | `test_decision_batch_engine.py::test_identity_byte_equal_and_merge` | T023 |
| `contracts/source-roster.contract.md` | C-105 | `test_decision_batch_engine.py::test_origin_linkage_states` | T023 |
| `contracts/source-roster.contract.md` | C-106 | `test_decision_batch_engine.py::test_class_gate_states` | T023 |
| `contracts/source-roster.contract.md` | C-107 | `test_decision_batch_engine.py::test_already_resolved_read_time_join` | T023 |
| `contracts/source-roster.contract.md` | C-108 | `test_decision_batch_engine.py::test_named_exclusions_counted` | T023 |
| `contracts/source-roster.contract.md` | C-109 | `test_decision_batch_engine.py::test_source_presence_levels` | T023 |
| `contracts/source-roster.contract.md` | C-110 | `test_decision_batch_engine.py::test_scan_zero_write` | T023 |
| `contracts/presentation.contract.md` | C-201 | `test_decision_batch_engine.py::test_presentation_order_deterministic` | T023 |
| `contracts/presentation.contract.md` | C-202 | `test_decision_batch_engine.py::test_row_slots_incomplete_named` | T023 |
| `contracts/presentation.contract.md` | C-203 | `test_decision_batch_engine.py::test_batch_context_floor` | T023 |
| `contracts/presentation.contract.md` | C-204 | `test_decision_batch_contract.py::test_presentation_identifier_boundary` | T023 |
| `contracts/presentation.contract.md` | C-205 | `test_decision_batch_engine.py::test_no_truncation_all_rows` | T023 |
| `contracts/presentation.contract.md` | C-206 | `test_decision_batch_engine.py::test_scan_twice_field_identical` | T023 |
| `contracts/presentation.contract.md` | C-207 | `test_decision_batch_engine.py::test_autonomous_presented_zero` | T023 |
| `contracts/presentation.contract.md` | C-208 | `test_decision_batch_contract.py::test_behavior_surfaces_named` | T052 |
| `contracts/default-derivation.contract.md` | C-301 | `test_decision_batch_engine.py::test_default_is_declared_member` | T023 |
| `contracts/default-derivation.contract.md` | C-302 | `test_decision_batch_engine.py::test_no_default_presented_not_settled` | T023 |
| `contracts/default-derivation.contract.md` | C-303 | `test_decision_batch_engine.py::test_grounding_join_closed_inputs` | T023 |
| `contracts/default-derivation.contract.md` | C-304 | `test_decision_batch_engine.py::test_grounded_pointers_all_resolve` | T023 |
| `contracts/default-derivation.contract.md` | C-305 | `test_decision_batch_engine.py::test_no_evidence_explicit` | T023 |
| `contracts/default-derivation.contract.md` | C-306 | `test_decision_batch_engine.py::test_prior_conflict_detected` | T023 |
| `contracts/default-derivation.contract.md` | C-307 | `test_decision_batch_contract.py::test_skill_does_not_recompute` | T023 |
| `contracts/objection-reply.contract.md` | C-401 | `test_decision_batch_engine.py::test_reply_forms_and_abort_zero_records` | T032 |
| `contracts/objection-reply.contract.md` | C-402 | `test_decision_batch_engine.py::test_objection_binds_identity_verbatim` | T032 |
| `contracts/objection-reply.contract.md` | C-403 | `test_decision_batch_engine.py::test_reply_membership_refusals` | T032 |
| `contracts/objection-reply.contract.md` | C-404 | `test_decision_batch_engine.py::test_silence_eligibility_matrix` | T032 |
| `contracts/objection-reply.contract.md` | C-405 | `test_decision_batch_engine.py::test_park_no_record_stays_pending` | T032 |
| `contracts/objection-reply.contract.md` | C-406 | `test_decision_batch_engine.py::test_unattended_and_missing_authorization_refused` | T032 |
| `contracts/objection-reply.contract.md` | C-407 | `test_decision_batch_engine.py::test_ineligible_explicit_settlement` | T032 |
| `contracts/objection-reply.contract.md` | C-408 | `test_decision_batch_contract.py::test_signal_mapping_pointer_only` | T032 |
| `contracts/objection-reply.contract.md` | C-409 | `test_decision_batch_engine.py::test_no_cross_batch_preauthorization` | T032 |
| `contracts/record-replay.contract.md` | C-501 | `test_decision_batch_engine.py::test_record_drift_refused_zero_write` | T032 |
| `contracts/record-replay.contract.md` | C-502 | `test_decision_batch_engine.py::test_batch_id_shape_and_duplicate_refusal` | T032 |
| `contracts/record-replay.contract.md` | C-503 | `test_decision_batch_engine.py::test_batch_record_layout_via_memory_engine` | T032 |
| `contracts/record-replay.contract.md` | C-504 | `test_decision_batch_engine.py::test_decision_record_batch_family` | T032 |
| `contracts/record-replay.contract.md` | C-505 | `test_decision_batch_engine.py::test_register_registration_and_status_update` | T039 |
| `contracts/record-replay.contract.md` | C-506 | `test_decision_batch_engine.py::test_resolution_annotation_and_disclosure` | T039 |
| `contracts/record-replay.contract.md` | C-507 | `test_decision_batch_engine.py::test_two_batches_distinct_paths` | T039 |
| `contracts/record-replay.contract.md` | C-508 | `test_decision_batch_engine.py::test_replay_from_record_only`（含 `::test_replay_broken_pointer_nonzero`） | T039 |
| `contracts/record-replay.contract.md` | C-509 | `test_decision_batch_contract.py::test_transmission_reuses_107_chain` | T052 |
| `contracts/record-replay.contract.md` | C-510 | `test_decision_batch_engine.py::test_supersession_append_only` | T052 |
| `contracts/record-replay.contract.md` | C-511 | `test_decision_batch_contract.py::test_owner_extension_single_owner` | T052 |
| `contracts/record-replay.contract.md` | C-512 | `test_decision_batch_contract.py::test_red_lines_and_boundary` | T052 |
| `contracts/completeness-refusal.contract.md` | C-601 | `test_decision_batch_engine.py::test_completeness_claim_shape` | T045 |
| `contracts/completeness-refusal.contract.md` | C-602 | `test_decision_batch_engine.py::test_bookkeeping_identity_holds` | T045 |
| `contracts/completeness-refusal.contract.md` | C-603 | `test_decision_batch_engine.py::test_unreadable_source_refusal` | T045 |
| `contracts/completeness-refusal.contract.md` | C-604 | `test_decision_batch_engine.py::test_absent_source_named_not_clean` | T045 |
| `contracts/completeness-refusal.contract.md` | C-605 | `test_decision_batch_engine.py::test_nothing_pending_success_no_record` | T045 |
| `contracts/completeness-refusal.contract.md` | C-606 | `test_decision_batch_engine.py::test_unclassifiable_candidate_refused` | T045 |
| `contracts/completeness-refusal.contract.md` | C-607 | `test_decision_batch_engine.py::test_no_partial_complete_claim` | T045 |
| `contracts/completeness-refusal.contract.md` | C-608 | `test_decision_batch_contract.py::test_engine_interface_contract` | T045 |

## Feature Integration Review

- **Review performed at generation (2026-11-27)**: `.specify/features.md` 行 112 已为 `Planned`，其详情文件承载 plan 阶段 Latest Review；tasks 阶段不推进生命周期、不新增 Feature、不使任何既有 Feature 失效。`Total Features` 不变。
- **Glossary**: 本特性的新词（Pending Decision Item、Pending Item Block、Decision Batch、Batch Record、Recommended Default、Recommendation Grounding、Batch Disposition、Acceptance by Silence）按 A-18 只提议不写入 `.specify/glossary.md`；T007 把它们落在所有者页词汇表，T058 验证 glossary 零写入。

## Measured Premises (re-measured at generation time 2026-11-27, HEAD 23b7a68b9)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 需求条目计数（FR / SC / STR） | `grep -cE '^\- \*\*FR-[0-9]{3}\*\*:' .specify/specs/112-decision-batch-panel/requirements.md`；同法 `SC-`；`grep -cE '^\| \`STR-[0-9]+\`' …/requirements.md` | **45 / 10 / 15** |
| 契约条款数（逐文件） | `grep -hcE '^- \*\*C-[0-9]+' .specify/specs/112-decision-batch-panel/contracts/*.md` | source-roster **10** / presentation **8** / default-derivation **7** / objection-reply **9** / record-replay **12** / completeness-refusal **8**；合计 **54**。**陷阱形**：`grep -c 'C-'` 会把正文引用一并算入（实测 114）；计量单位是行首 `- **C-NNN**` 条款定义行 |
| register open 待决策行 | `awk -F'\|' '$2 ~ /^ *(OI-\|D-)/ && $5 ~ /^ *open([[:space:],，（(]\|$)/ {n++} END{print n+0}' .specify/register.md` | **17**。**陷阱形**：只按 id 前缀计数得 27（把已解决行也算入）；判定必须带状态起始词（word boundary `open`） |
| 四个扫描根中的 `### PENDING —` 块 | `for d in .specify/specs .specify/goals .specify/anchoring .specify/teams; do grep -rE '^### PENDING —' --include=*.md "$d" \| wc -l; done` | 四个根均存在、各 **0** 块 → 首轮真实批次呈现 17 行 `incomplete`、零项可结案（A-16、EP-007 fallback） |
| 107 所有者页清单 | `grep -cE '^\| \*\*[A-Z]' shared/definitions/decision-definitions.md`；`grep -cE '^\| P-[0-9]' …`；`grep -cE '^\| M-0[0-9]' …`；`grep -cE '^\| B-0[0-9]' …`；`grep -c '^## ' …` | 词汇 **9** / 生产者 P-01…P-12 **12** / M 规则 **9** / B 规则 **7** / 章节 **9**；`CONDITIONAL_FIELDS` = **6**；检查器 `ADMITTED_FIELD_LINES` = 9 基础行字段 + 6 条件字段 = **15** |
| 冻结命令 / 技能集合 | `ls templates/commands/*.md \| wc -l`；`find skills -name SKILL.md \| wc -l`；`grep -n 'assert len(COMMAND_BASELINE)\|assert len(SKILL_BASELINE)' tests/contract/test_migration_distribution.py` | 磁盘 **32** 命令 / **60** 技能；测试 pin `== 32` / `== 60`；`decide` 与 `decide-batch` 均未在场 |
| probe 注册面 | `python3 scripts/python/probe-utils.py --action probes --validate`；`grep -n 'assert internal ==' tests/contract/test_probe_nonentity_catalog.py` | **11 classes / 130 internal + 0 external objects**；测试字面量仍为 **122**（已落后实测 8 个对象——本任务在新增 skill 对象后按**实测值**更新，见 T011） |
| 门控扫描基线 | `python3 .specify/scripts/python/scan-confirmation-gates.py --summary` | **30** blocking（22 destructive / 7 governance-kept / 1 reversible），**0** violations |
| 命令文档面 | `ls docs/reference/commands \| wc -l` | **30** 个文件，一命令一文档，无 index |
| `## Decision Items` 段字节 | `python3` 段提取后 `len(section.encode('utf-8'))` | **1,276 B**（声明上限 1,500 B），本特性不编辑该段 |
| 既有 knowledge 中的批次条目 | `python3 scripts/python/memory-utils.py --action list --scope knowledge --format json` | `decision-batch-` 前缀条目 **0**（与 quickstart 场景 6 一致） |
| 镜像 / 副本基线 | `python3 .specify/scripts/python/sync-mirrors.py --check`；`python3 scripts/python/regen-command-copies.py --check` | rc **0**（`shared/ == .specify/shared/`，123 files byte-identical）；regen `OK: all per-tool command copies match the source templates.` rc **0** |
| 测试入口与解释器 | `bash scripts/bash/run-tests.sh tests/contract/test_migration_distribution.py -q`；`python3 -m pytest --version` | runner `error: no interpreter with pytest found (tried SPECKIT_PYTHON, .venv/bin/python, python3, python)`；`python3` 报告 `No module named pytest` → 见 § Environment Prerequisites |
| 运行环境 | `python3 --version`；`bash --version`；`git --version` | `Python 3.11.11` / `4.4.20(1)-release` / `2.43.5` |
| 本规格流类别 | `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:112-decision-batch-panel"` | `flow_class: execution` / `flow_type: -` / `source: declaration`，rc 0 |

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 先建立夹具与证据落点，并冻结实现前的可执行读数。

- [X] T001 Create the per-feature fixture tree `tests/fixtures/decision-batch/` with the case directories `two-source`, `incomplete-block`, `autonomous`, `source-conflict`, `class-conflict`, `resolution-join`, `grounding-grounded`, `grounding-none`, `prior-conflict`, `eligibility-matrix`, `unreadable-register`, `absent-root`, `empty-project`, `reply-shapes`, `drift`, `register-updates`, `register-absent`, `concurrency`, `replay-broken`, `batch-family`, `unwritable-old-record`, `m10`, `m11`, `m12`, `m13`, `m14`, `m15`, `m16` (each carrying a `.gitkeep`) and the runtime-evidence directory `.specify/specs/112-decision-batch-panel/notes/` (FR-044).
- [X] T002 [blockedBy: T001] Capture the pre-change side of every diff premise in `.specify/specs/112-decision-batch-panel/notes/pre-change-measurements.md`, with command, reading and ISO date per row: the 17-row register predicate output, 0 `### PENDING —` blocks in the four roots, `scan-confirmation-gates.py --summary` = 30 blocking / 0 violations also captured verbatim into `test-evidence/scan-confirmation-gates-baseline.txt`, `sync-mirrors.py --check` rc 0, `regen-command-copies.py --check` rc 0, the 32-command / 60-skill baselines, the probe registry reading 130 objects against its stale literal 122, 30 command docs, the owner-page inventory (9 vocabulary / 12 producer rows / 9 M rows / 7 B rows / 6 conditional fields), the checker's 15 admitted field lines, 0 `decision-batch-` knowledge entries, and the 1,276 B `## Decision Items` section.
- [X] T003 [blockedBy: T001] Create the red-first evidence skeleton `.specify/specs/112-decision-batch-panel/notes/red-first-evidence.md` with one slot per planned red-first test (the engine scan legs, the record legs, replay, the M-10…M-16 reverse samples, the contract tests); each slot records command, real output and exit status; the failing-test baseline name list is captured by `/speckit.implement`'s `**Test runs**` owner and is referenced, never restated (FR-044).
- [X] T004 [blockedBy: T001] Freeze the clause/FR coverage baseline with `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/112-decision-batch-panel --freeze > .specify/specs/112-decision-batch-panel/coverage-baseline.txt`; record the command and capture date in the file header and never fabricate an empty baseline.

**Checkpoint**: fixture tree and evidence skeleton exist; every pre-change value is frozen before any edit.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 引擎接口、入口面与所有者页骨架是所有故事的共同前置；冻结基线必须随入口面同批移动。

**CRITICAL**: 本阶段完成前，任何用户故事不得开始。

- [X] T005 Author `tests/contract/test_decision_batch_contract.py::test_engine_interface_contract` red-first (C-608): `-h` and `--help` answer the same body, `--version` prints one line on the entry and on each closed action, an undeclared option exits non-zero, the declared action set is exactly `scan` / `record` / `replay`, exit codes `0` / `1` / `2` are stated in the help body, and a scan/replay invocation creates no file inside the repository (before/after snapshot with bytecode writing disabled) (FR-039).
- [X] T006 [blockedBy: T005] Implement the engine CLI skeleton `scripts/python/decision-batch.py`: argparse with the closed positional actions `scan` / `record` / `replay` (the documented invocation form of `quickstart.md`), the declared flags `--workspace-root`, `--format {text,json}`, `--presentation`, `--reply`, `--authorization {interactive,unattended}`, `--batch`, `-h`/`--help`/`--version` resolvable at the entry and on every action, undeclared options rejected non-zero, a declared-but-unimplemented action exiting `2` with an explicit message, and `scan`/`replay` performing no write (FR-039).
- [X] T007 Extend the single owner page `shared/definitions/decision-definitions.md`: the Ownership Declaration names the batch faces; § Closed Vocabulary grows 9 → 17 with the eight bilingual terms (Pending Decision Item（待决策项）、Pending Item Block（待决策项块）、Decision Batch（决策批次）、Batch Record（批次记录）、Recommended Default（建议默认值）、Recommendation Grounding（建议依据）、Batch Disposition（批次处置）、Acceptance by Silence（沉默接受默认）); the producer inventory gains P-13 (producer = 批量决策面板 `/speckit.decide` batch session, carrier = batch record, obligation = `record-when-decision`, class = `human-interactive` only) (FR-001, FR-002, FR-003).
- [X] T008 [blockedBy: T007] Author the thin entry `templates/commands/decide.md` for `/speckit.decide`: User Input Protocol, the closed action set, delegation to the skill and the engine, the exit semantics by pointer, and no criteria table restated from the owner page (FR-039).
- [X] T009 [blockedBy: T008] Author the internal skill `skills/internal/decide-batch/SKILL.md`: presentation relay, reply capture, engine delegation (`scan` / `record` / `replay`), the concurrency-obligation pointer, and the boundaries (never recompute engine verdicts, never invent defaults or options, never record in unattended mode) (FR-039).
- [X] T010 [blockedBy: T009] Register the skill's probe Object and HandlerBinding in `shared/definitions/probe-definitions.md` (object `skill-decide-batch-wrapup`, class `skill-wrapup`, unit `skill:decide-batch`) and compile the skill's `## Wrap-up` with `python3 scripts/python/probe-utils.py --action compile-embeds`; the compiled block is never hand-written and must carry the engine fingerprint (FR-042).
- [X] T011 [blockedBy: T008,T010] Move the frozen inventories in the same change: `tests/contract/test_migration_distribution.py` 32 → 33 commands (`decide`) and 60 → 61 skills (`decide-batch`) with their two length pins, and `tests/contract/test_probe_nonentity_catalog.py` to the re-measured registry object count (generation-time reading 130 + the one new object; the pre-change literal 122 is already 8 behind the measured registry — re-measure at edit time and use the measured value, never 122 + 1) (FR-042, FR-044).
- [X] T012 [blockedBy: T006,T007,T010] Regenerate the four per-tool command copies with `python3 scripts/python/regen-command-copies.py` and project the new engine/skill with `python3 scripts/python/sync-mirrors.py --write`; verify both `--check` modes return rc 0, the four copies contain the edit, and both engine copies answer `--help` / `--version` (FR-042).

**Checkpoint**: engine surface, command, skill, probe wrap-up, owner-page vocabulary/P-13 and the frozen-baseline moves exist; mirrors and copies are clean.

---

## Phase 3: User Story 1 — 一次集中呈现全部待决策项，每项完整、可比较、带建议默认值 (Priority: P1)

**Goal**: 封闭来源清单中的每个待决策项恰好出现一次，按确定顺序排列；每项携带 107 `human-interactive` 模板槽位、来源指针、建议默认值与接地状态、资格状态与原因、异议方式；`ai-autonomous` 不出现但在记账中带理由计数。

**Independent Test**: 覆盖两个来源、重复引用、不完整项与 `ai-autonomous` 项的 fixture 产出预期呈现行；连续两次扫描除时间戳外逐字段一致；篡改一项的默认标记后复核转红。

### Tests for User Story 1 (MANDATORY)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US1] Author the US1 red-first unit tests in `tests/unit/test_decision_batch_engine.py` — `test_roster_closed_and_predicates`, `test_incomplete_block_still_candidate`, `test_identity_byte_equal_and_merge`, `test_origin_linkage_states`, `test_class_gate_states`, `test_already_resolved_read_time_join`, `test_named_exclusions_counted`, `test_source_presence_levels`, `test_scan_zero_write`, `test_presentation_order_deterministic`, `test_row_slots_incomplete_named`, `test_batch_context_floor`, `test_no_truncation_all_rows`, `test_scan_twice_field_identical`, `test_autonomous_presented_zero`, `test_default_is_declared_member`, `test_no_default_presented_not_settled`, `test_grounding_join_closed_inputs`, `test_grounded_pointers_all_resolve`, `test_no_evidence_explicit`, `test_prior_conflict_detected` — each failing on its own missing behaviour, never on an import error; fixtures `tests/fixtures/decision-batch/two-source/`, `incomplete-block/`, `autonomous/`, `source-conflict/`, `class-conflict/`, `resolution-join/`, `grounding-grounded/`, `grounding-none/`, `prior-conflict/` (FR-006, FR-008, FR-009, FR-010, FR-013, FR-014, FR-019, FR-021, FR-022, FR-023, FR-025, FR-041).
- [X] T014 [P] [US1] Author the US1 red-first contract tests in `tests/contract/test_decision_batch_contract.py` — `test_block_grammar_owner_extension` (C-103: the pending-item block grammar is owned by the extended owner page and is not judged as a decision record), `test_presentation_identifier_boundary` (C-204: the user-facing text body carries no field names, script names or status tokens), `test_skill_does_not_recompute` (C-307: the skill delegates the join/pointer/conflict judgements to the engine and performs no semantic retrieval) (FR-020).

### Implementation for User Story 1

- [X] T015 [US1] Author `shared/definitions/decision-definitions.md` § Pending Source Roster（待决策项来源清单）: the two closed sources with their machine-checkable candidate predicates, the four closed scan roots, the candidacy-versus-qualification split, the named exclusion families, the register↔block linkage rule (`origin` token + explicit repository-relative path + exactly one match), the byte-equal identity/dedupe rule, and the presence readings (`read` / `absent` / `unreadable` with the carrier-level versus block-level boundary) (FR-001, FR-006, FR-007, FR-009, FR-010).
- [X] T016 [US1] Author `shared/definitions/decision-definitions.md` § Pending Item Block（待决策项块）: the `### PENDING — <full subject name>` grammar, the closed field set with the same-name and resolution conditional fields, the 107 option-set rules (declared count, five elements, exactly one default, `other` with `path`, `forced`), the block-level grammar defects that yield `incomplete` with named defects, and the "not a decision record" boundary (FR-008).
- [X] T017 [US1] Author `shared/definitions/decision-definitions.md` § Batch States（批次状态） and § Batch Presentation Contract（批次呈现契约）: the closed qualification states with the documented precedence, the named reason set, the exclusion states, the per-item template slots, the batch-level context floor (why now, silence meaning, how to object, pending list, completeness disclosure), the no-truncation rule, the deterministic order, and the identifier boundary for the user-facing body (FR-011, FR-014, FR-019, FR-020, FR-025).
- [X] T018 [US1] Author `shared/definitions/decision-definitions.md` § Recommended Default & Grounding（建议默认值与依据）: the default is the item's single declared default (never invented), the deterministic grounding join over the closed prior-experience carrier set, `grounded` / `no-evidence` with 100% resolvable pointers, `basis` is never evidence, the prior-decision conflict state with its pointer and chosen label, and the engine-judges boundary (FR-021, FR-022, FR-023).
- [X] T019 [US1] [blockedBy: T013] Implement the `scan` core in `scripts/python/decision-batch.py`: register predicate (word-boundary `open`), block parser outside fences, identity merge (byte-equal subject + locator), the register↔block linkage states, class gate (`ai-autonomous` excluded `not-human-held`, unknown class `incomplete` `class-missing`), already-resolved read-time join over prior batch records, named exclusion accounting, presence readings with carrier-level refusal, deterministic ordering, and zero writes (FR-006, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-041).
- [X] T020 [US1] [blockedBy: T018,T019] Implement the grounding join and prior-decision conflict detection in `scan`: the three closed join inputs, the closed prior-experience carrier set, pointer resolution with anchor checking, `no-evidence` emission, and the `prior-decision-conflict` qualification with the prior pointer and chosen label (FR-021, FR-022, FR-023).
- [X] T021 [US1] [blockedBy: T019] Implement the `--format json` payload and the `--format text` renderer as projections of one row set (row-count and identity equality between the two faces), including the batch-level context floor and a text body free of internal identifiers (FR-014, FR-019, FR-020, FR-025).
- [X] T022 [US1] [blockedBy: T015,T016,T017,T018,T019,T020,T021] Regenerate and verify the US1 mirror pairs: `python3 scripts/python/sync-mirrors.py --write` then `--check` with no NEW drift against the baseline in `notes/pre-change-measurements.md`; `cmp` `shared/definitions/decision-definitions.md` with `.specify/shared/definitions/decision-definitions.md` and `scripts/python/decision-batch.py` with `.specify/scripts/python/decision-batch.py`.
- [X] T023 [US1] Run the US1 phase tests through the single entry (see § Environment Prerequisites) against `tests/unit/test_decision_batch_engine.py` and against `tests/contract/test_decision_batch_contract.py`; record the red-first slots and the green run in `notes/red-first-evidence.md` and `notes/us1-green.txt`, with the two-scan comparison and the presentation fixture outputs as SC-002/SC-003 evidence. [green: contracts/source-roster.contract.md#C-101] [green: contracts/source-roster.contract.md#C-102] [green: contracts/source-roster.contract.md#C-103] [green: contracts/source-roster.contract.md#C-104] [green: contracts/source-roster.contract.md#C-105] [green: contracts/source-roster.contract.md#C-106] [green: contracts/source-roster.contract.md#C-107] [green: contracts/source-roster.contract.md#C-108] [green: contracts/source-roster.contract.md#C-109] [green: contracts/source-roster.contract.md#C-110] [green: contracts/presentation.contract.md#C-201] [green: contracts/presentation.contract.md#C-202] [green: contracts/presentation.contract.md#C-203] [green: contracts/presentation.contract.md#C-204] [green: contracts/presentation.contract.md#C-205] [green: contracts/presentation.contract.md#C-206] [green: contracts/presentation.contract.md#C-207] [green: contracts/default-derivation.contract.md#C-301] [green: contracts/default-derivation.contract.md#C-302] [green: contracts/default-derivation.contract.md#C-303] [green: contracts/default-derivation.contract.md#C-304] [green: contracts/default-derivation.contract.md#C-305] [green: contracts/default-derivation.contract.md#C-306] [green: contracts/default-derivation.contract.md#C-307] [blockedBy: T013,T014,T015,T016,T017,T018,T019,T020,T021,T022]

**Checkpoint**: 两个来源的 fixture 各出现一次并带完整槽位；重复引用合并；`ai-autonomous` 呈现数为零；两次扫描除时间戳外逐字段一致；篡改默认标记转红。

---

## Phase 4: User Story 2 — 只对异议发声，其余合格项按建议默认值结案，不合格项不被吞 (Priority: P1)

**Goal**: 用户只回复有异议的项；其余 `eligible` 项按建议默认值结案；不可逆默认、无默认、来源冲突、前例冲突项保持待定并各有原因；「无异议」结案全部合格项；中止会话零记录。

**Independent Test**: 一个含可逆默认、不可逆默认、无默认、前例冲突四项的 fixture，用「仅异议一项」的应答记录批次，断言恰一项 `objected-alternative`、可逆默认项 `accepted-default`、其余三项保持待定且各有具名原因；零异议与中止会话各跑一次。

### Tests for User Story 2 (MANDATORY)

- [X] T024 [P] [US2] Author the US2 red-first unit tests in `tests/unit/test_decision_batch_engine.py` — `test_reply_forms_and_abort_zero_records`, `test_objection_binds_identity_verbatim`, `test_reply_membership_refusals`, `test_silence_eligibility_matrix`, `test_park_no_record_stays_pending`, `test_unattended_and_missing_authorization_refused`, `test_ineligible_explicit_settlement`, `test_no_cross_batch_preauthorization`, `test_record_drift_refused_zero_write`, `test_batch_id_shape_and_duplicate_refusal`, `test_batch_record_layout_via_memory_engine`, `test_decision_record_batch_family` — each failing on its own missing behaviour; fixtures `tests/fixtures/decision-batch/eligibility-matrix/`, `reply-shapes/`, `drift/`, `batch-family/` (FR-024, FR-026, FR-027, FR-028, FR-031, FR-032, FR-033, FR-037, FR-040).
- [X] T025 [P] [US2] Author the US2 red-first contract test in `tests/contract/test_decision_batch_contract.py` — `test_signal_mapping_pointer_only` (C-408: the disposition→choice-signal mapping reaches `shared/guidelines/confirmation-gates.md` by pointer; its value domain is not restated; `objected-parked` emits no signal) (FR-030).

### Implementation for User Story 2

- [X] T026 [US2] Author `shared/definitions/decision-definitions.md` § Decision Batch & Reply（决策批次与应答）: the reply definition (explicit response only; follow-up questions are not replies; abort writes nothing), the caller-declared authorization level with missing = unattended, binding by item identity, member validation before any write, the refusal forms, and the verbatim reply layer versus the `rationale` key points (FR-001, FR-026, FR-027, FR-040).
- [X] T027 [US2] Author `shared/definitions/decision-definitions.md` § Batch Disposition & Acceptance by Silence（批次处置与沉默接受默认）: the closed dispositions, the eligibility conjunction, the silence rule inside a completed interactive batch, explicit settlement of ineligible items with the qualification retained, parked items staying pending with no record, no unhandled settlement, no cross-batch pre-authorization, and the signal mapping by pointer (FR-001, FR-024, FR-027, FR-028, FR-030, FR-031).
- [X] T028 [US2] Author `shared/definitions/decision-definitions.md` § Batch Record Contract（批次记录契约） and extend § Layered Field Closure with the batch-family conditional layer: one dated knowledge entry per batch written through the memory engine, the batch head (id, scan time, tool version, per-source counts, completeness verdict, authorization, verbatim reply block), the item-row table, the decision-record blocks, create-only/never-overwrite, and the three conditional fields `batch_id` / `batch_disposition` / `recommendation_grounding` appearing together on batch-produced records only (FR-001, FR-004, FR-032, FR-033, FR-037).
- [X] T029 [US2] [blockedBy: T024] Implement reply parsing/validation and settlement computation in `scripts/python/decision-batch.py`: reply-file structure, identity binding, full-label membership (including the declared `other` path), duplicate/unknown-identity refusals, zero writes on refusal, the authorization gate, park, explicit settlement of ineligible items, and the eligibility matrix (FR-024, FR-026, FR-027, FR-028, FR-031, FR-040).
- [X] T030 [US2] [blockedBy: T026,T027,T028,T029] Implement the `record` write path: re-scan drift precheck over identity set and per-item fingerprints (refusal with the diff and zero writes, no minted id), late batch-id minting, create-only precheck before the memory-engine call, the batch record head/rows/decision-record blocks via `scripts/python/memory-utils.py --action record --scope knowledge`, the three batch-family fields, and extend `scripts/python/validate-decisions.py`'s admitted-field closure plus one recorded batch-family rule (FR-032, FR-033, FR-037).
- [X] T031 [US2] [blockedBy: T026,T027,T028,T029,T030] Regenerate and verify the US2 mirror pairs: `sync-mirrors.py --write` then `--check` with no NEW drift; `cmp` the owner page, the engine and `scripts/python/validate-decisions.py` against their `.specify/` mirrors; run `validate-decisions.py` over a batch-record fixture and assert exit 0 with the family fields admitted.
- [X] T032 [US2] Run the US2 phase tests through the single entry (see § Environment Prerequisites) against `tests/unit/test_decision_batch_engine.py` and against `tests/contract/test_decision_batch_contract.py`; record the four reply-shape batches, the park row and the family-field outputs in `notes/red-first-evidence.md` and `notes/us2-green.txt` as SC-004 evidence. [green: contracts/objection-reply.contract.md#C-401] [green: contracts/objection-reply.contract.md#C-402] [green: contracts/objection-reply.contract.md#C-403] [green: contracts/objection-reply.contract.md#C-404] [green: contracts/objection-reply.contract.md#C-405] [green: contracts/objection-reply.contract.md#C-406] [green: contracts/objection-reply.contract.md#C-407] [green: contracts/objection-reply.contract.md#C-408] [green: contracts/objection-reply.contract.md#C-409] [green: contracts/record-replay.contract.md#C-501] [green: contracts/record-replay.contract.md#C-502] [green: contracts/record-replay.contract.md#C-503] [green: contracts/record-replay.contract.md#C-504] [blockedBy: T024,T025,T026,T027,T028,T029,T030,T031]

**Checkpoint**: 异议一项 → 恰一项 `objected-alternative`、可逆默认项结案、其余保持待定且原因具名；零异议结案全部 `eligible`；中止零记录；非成员异议被拒且零写入。

---

## Phase 5: User Story 3 — 处置落进既有载体，整批可只凭记录重放 (Priority: P1)

**Goal**: 一次批次结束后，审计者不打开对话历史也能从记录重建项集、完备性、默认值与接地、异议与处置、`D-NNN` 记录、register 登记与来源状态更新；重放只凭记录与可解析指针。

**Independent Test**: 一个 fixture 批次落盘后删除对话上下文，仅凭批次记录与指向的载体重放，断言项集、处置与记录齐全；把一条证据指针改坏，重放转红并点名该指针。

### Tests for User Story 3 (MANDATORY)

- [X] T033 [P] [US3] Author the US3 red-first unit tests in `tests/unit/test_decision_batch_engine.py` — `test_register_registration_and_status_update`, `test_resolution_annotation_and_disclosure`, `test_two_batches_distinct_paths` (distinct paths + mutual write isolation + reads of another batch's settled record only through the declared read-only purposes), `test_replay_from_record_only`, `test_replay_broken_pointer_nonzero` — plus the absent-register creation case; fixtures `tests/fixtures/decision-batch/register-updates/`, `register-absent/`, `concurrency/`, `replay-broken/` (FR-034, FR-035, FR-036, FR-037).

### Implementation for User Story 3

- [X] T034 [US3] Author `shared/definitions/decision-definitions.md` § Register Reflection & Source Updates（批次登记与来源更新）: batch id and decision ids registered at birth (per carrier + range grouping legal), settled register rows' status cells naming batch and decision id without deleting rows, parked rows staying `open`-prefixed and annotated, the block `resolution` conditional field without rewriting block content, failure disclosure, the read-time join preventing re-presentation, and absent-register creation from the existing header form (FR-001, FR-012, FR-034, FR-035).
- [X] T035 [US3] Author `shared/definitions/decision-definitions.md` § Replay Contract（重放契约）: replay is read-only and deterministic over the batch record plus resolvable pointers, reconstructs the item set / completeness / defaults and grounding / objections and dispositions / decision records, reports every unresolvable pointer with a non-zero exit, and never completes from conversation memory (FR-001, FR-036).
- [X] T036 [US3] [blockedBy: T033] Implement register registration and status-cell updates, pending-block `resolution` annotations, post-write failure disclosure, and the absent-register creation path in `record` of `scripts/python/decision-batch.py` (FR-034, FR-035, FR-037).
- [X] T037 [US3] [blockedBy: T033] Implement the `replay` action in `scripts/python/decision-batch.py`: read-only reconstruction from `--batch` plus resolvable pointers, deterministic output, and a non-zero exit naming every unresolvable pointer (FR-036, FR-039).
- [X] T038 [US3] [blockedBy: T034,T035,T036,T037] Regenerate and verify the US3 mirror pairs: `sync-mirrors.py --write` then `--check` with no NEW drift; `cmp` the owner page and the engine against their `.specify/` mirrors.
- [X] T039 [US3] Run the US3 phase tests through the single entry (see § Environment Prerequisites) against `tests/unit/test_decision_batch_engine.py`; record the register diff (status cells and appended rows only), the `resolution` annotations, the two-batch path set, the replay output and the broken-pointer exit in `notes/red-first-evidence.md` and `notes/us3-green.txt` as SC-005 evidence. [green: contracts/record-replay.contract.md#C-505] [green: contracts/record-replay.contract.md#C-506] [green: contracts/record-replay.contract.md#C-507] [green: contracts/record-replay.contract.md#C-508] [blockedBy: T033,T034,T035,T036,T037,T038]

**Checkpoint**: register 追加行与状态单元格更新且行未删除；`resolution` 追加；两个批次路径互异；只凭记录的重放成立，坏指针非零退出。

---

## Phase 6: User Story 4 — 完备性是诚实的：记账、拒绝、空集明说 (Priority: P2)

**Goal**: 每个来源被读取或带原因缺席，每个候选被分类恰好一次，计数恒等；任一载体存在却读不了则整批拒绝；零待决策项显式 `nothing-pending`。

**Independent Test**: 一个不可读 register 触发具名拒绝且零记录；一个缺席的扫描根记为缺席空来源；一个空项目返回 `nothing-pending`；记账恒等式在每个 fixture 上成立。

### Tests for User Story 4 (MANDATORY)

- [X] T040 [P] [US4] Author the US4 red-first unit tests in `tests/unit/test_decision_batch_engine.py` — `test_completeness_claim_shape`, `test_bookkeeping_identity_holds`, `test_absent_source_named_not_clean`, `test_nothing_pending_success_no_record`, `test_unclassifiable_candidate_refused`, `test_no_partial_complete_claim` — with fixtures `tests/fixtures/decision-batch/absent-root/` and `empty-project/` (FR-015, FR-017, FR-018).
- [X] T041 [P] [US4] Author `shared/definitions/decision-definitions.md` § Completeness & Refusal（完备性与拒绝）: the completeness claim as a closed-set claim (referent = this scan, comparison unit = per-candidate classification, allowed delta unconditionally empty), the bookkeeping identity, the presence readings by pointer, carrier-level refusal versus block-level `incomplete`, absent-source naming, `nothing-pending`, the no-silent-drop and no-partial-completeness rules, and the exit-code pointer (FR-001, FR-015, FR-016, FR-017, FR-018).
- [X] T042 [US4] [blockedBy: T019,T030] Author the US4 regression-exception guards in `tests/unit/test_decision_batch_engine.py` — `test_unreadable_source_refusal` over `tests/fixtures/decision-batch/unreadable-register/` and the batch-record-head completeness assertion — placed after their subjects because they guard behaviour already landed by T019 and T030 (migration/regression exception: the subjects predate the guards, so these samples cannot be red-first and are ordered with an explicit dependency instead) (FR-016).

### Implementation for User Story 4

- [X] T043 [US4] [blockedBy: T040] Implement the completeness hardening in `scripts/python/decision-batch.py`: the closed-set claim shape, bookkeeping identity in the payload and the batch-record head, absent sources as named empty sources, explicit `nothing-pending` with exit 0 and no batch record, unclassifiable candidates as refusals, no partial-completeness claim, and the documented exit codes in the help body (FR-015, FR-016, FR-017, FR-018).
- [X] T044 [US4] [blockedBy: T041,T042,T043] Regenerate and verify the US4 mirror pairs: `sync-mirrors.py --write` then `--check` with no NEW drift; `cmp` the owner page and the engine against their `.specify/` mirrors.
- [X] T045 [US4] Run the US4 phase tests through the single entry (see § Environment Prerequisites) against `tests/unit/test_decision_batch_engine.py` and against `tests/contract/test_decision_batch_contract.py`; record the three scan fixtures (two-source / unreadable / empty), the bookkeeping identity, the refusal output and the nothing-pending success in `notes/red-first-evidence.md` and `notes/us4-green.txt` as SC-001 evidence. [green: contracts/completeness-refusal.contract.md#C-601] [green: contracts/completeness-refusal.contract.md#C-602] [green: contracts/completeness-refusal.contract.md#C-603] [green: contracts/completeness-refusal.contract.md#C-604] [green: contracts/completeness-refusal.contract.md#C-605] [green: contracts/completeness-refusal.contract.md#C-606] [green: contracts/completeness-refusal.contract.md#C-607] [green: contracts/completeness-refusal.contract.md#C-608] [blockedBy: T040,T041,T042,T043,T044]

**Checkpoint**: 记账恒等式成立；不可读 register 具名拒绝且零记录；缺席根具名缺席；空项目 `nothing-pending` 且不建批次记录。

---

## Phase 7: User Story 5 — 重决不覆盖前例；人工与自主不混淆；零传输 (Priority: P2)

**Goal**: 与既往决策相反的改选先呈现冲突并要求显式选择；确认后新增记录、旧记录保留并追加 `superseded_by`；`ai-autonomous` 从不进入面板；无人值守不能把「无人应答」记成接受；批次零网络、零反馈写入、零自动传输。

**Independent Test**: 一个主体命中既往记录且默认值不同的 fixture，断言呈现 `prior-decision-conflict` 且不因沉默结案；用户改选后断言新记录 + 旧记录 `superseded_by` 且旧内容零改写；旧载体不可写时拒绝重决；一次批次断言反馈存储与网络零接触。

### Tests for User Story 5 (MANDATORY)

- [ ] T046 [P] [US5] Author the US5 red-first unit tests in `tests/unit/test_decision_batch_engine.py` — `test_supersession_append_only` (new record + old record gains `superseded_by`, old content byte-identical) and the unwritable/unreadable old-carrier refusal — with fixtures `tests/fixtures/decision-batch/prior-conflict/` and `unwritable-old-record/` (FR-029).
- [ ] T047 [P] [US5] Author the US5 red-first contract tests in `tests/contract/test_decision_batch_contract.py` — `test_transmission_reuses_107_chain` (C-509: batch decisions reuse the record → dispatch attempt → implementation receipt chain, no second record or transmission path), `test_owner_extension_single_owner` (C-511: one owner page, all batch faces present, P-13 in the inventory, no second registry/store/schema), `test_red_lines_and_boundary` (C-512: no ai-harness alignment, no network, no feedback-store write, no automatic transmission, no autonomous presentation), `test_behavior_surfaces_named` (C-208: B-08/B-09 review surfaces named, no machine-coverage claim) (FR-003, FR-005, FR-038, FR-041, FR-045).

### Implementation for User Story 5

- [ ] T048 [US5] Author `shared/definitions/decision-definitions.md` § Redecision & Supersession（重决与取代） and extend § Enforcement Boundary: M-10…M-16 rows (each with exactly one deterministic judge action `scan` / `record` / `replay`, one red condition, its coverage statement and its reverse-sample directory under `tests/fixtures/decision-batch/`), B-08（批次呈现可读性与后果真实性） / B-09（建议理由充分性） rows with their named review surfaces, the table–guard parity duty, the gate-neutrality duty and the no-machine-coverage statements (FR-001, FR-029, FR-045).
- [ ] T049 [US5] [blockedBy: T048] Extend `tests/contract/test_decision_governance_guards.py`: `M_RULES` / `B_RULES` to M-01…M-16 / B-01…B-09; `GUARD_ROSTER` covering all sixteen rules with a runner that keeps the nine existing samples byte-identical, dispatches M-01…M-09 to `scripts/python/validate-decisions.py` and M-10…M-16 to `scripts/python/decision-batch.py`'s documented invocations, and asserts each batch reverse sample's exit code plus its named refusal/qualification needle; the parity test keeps the nine `--action` judge rows and judges the batch rows in the batch engine's documented action form; provide the `m10`…`m16` reverse-sample fixtures under `tests/fixtures/decision-batch/` (FR-003, FR-044).
- [ ] T050 [US5] [blockedBy: T046] Implement redecision/supersession in `record` of `scripts/python/decision-batch.py`: a new record plus `superseded_by: <D-NNN> (<carrier path>)` appended to each overturned prior record with its content byte-identical — when the prior record sits inside a prior batch record, the same append is that file's sole sanctioned post-write mutation (every pre-existing byte unchanged; it is not a same-batch-id second batch record) — and a named refusal when the prior carrier is unreadable or unwritable (FR-029, A-27).
- [ ] T051 [US5] [blockedBy: T048,T049,T050] Regenerate and verify the US5 mirror pairs (`sync-mirrors.py --write` then `--check` with no NEW drift; `cmp` the owner page, the engine and the guard fixtures) and run `python3 scripts/python/scan-confirmation-gates.py --summary` against `test-evidence/scan-confirmation-gates-baseline.txt` — zero NEW hits, never an absolute count claim.
- [ ] T052 [US5] Run the US5 phase tests through the single entry (see § Environment Prerequisites) against `tests/unit/test_decision_batch_engine.py`, against `tests/contract/test_decision_batch_contract.py` and against `tests/contract/test_decision_governance_guards.py`, executing every M-10…M-16 reverse sample and recording its red output in `notes/red-first-evidence.md`; record the supersession pair, the zero-touch assertions and the B-08/B-09 surface list in `notes/us5-green.txt` as SC-006/SC-007 evidence. [green: contracts/presentation.contract.md#C-208] [green: contracts/record-replay.contract.md#C-509] [green: contracts/record-replay.contract.md#C-510] [green: contracts/record-replay.contract.md#C-511] [green: contracts/record-replay.contract.md#C-512] [blockedBy: T046,T047,T048,T049,T050,T051]

**Checkpoint**: 重决新增记录、旧记录零改写并带 `superseded_by`；旧载体不可写时拒绝；M-10…M-16 逐条转红演练完成；B-08/B-09 具名；门控读数零新增。

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: 收口命令文档、框架地图、分发闭环、quickstart 实录与验收证据包。

- [ ] T053 [P] Author `docs/reference/commands/decide.md` (FR-043): the entry, the closed actions, the exit semantics copied from the engine's `--help` face, the owner-page pointer, and no restated criteria table.
- [ ] T054 [P] Update the decision-governance row of `shared/definitions/framework-map.md`: P-13, the batch capability and the consumers (`decision-batch.py`, the command, the skill, the guards); keep the row a pointer, not a manual (FR-042).
- [ ] T055 [blockedBy: T012] Add the distribution closure contract test `test_distribution_init_contains_decide` to `tests/contract/test_decision_batch_contract.py`: a throwaway fresh `specify init` workspace receives `/speckit.decide` and `decide-batch` plus the engine, and each of the four per-tool copies contains the edit (precedent: the existing init-layout integration fixture) (FR-039, FR-042).
- [ ] T056 [blockedBy: T012,T053,T054] Verify the delivery closure: `sync-mirrors.py --check` shows no NEW drift against `notes/pre-change-measurements.md`, `regen-command-copies.py --check` exits 0, both engine copies answer `--help` / `--version`, the `.specify/instructions.md` `## Decision Items` section compares byte-identical (1,276 B), and `git diff --stat` over `.specify/.gitignore` and the runtime store layout is empty (FR-004, FR-005, FR-042, FR-043).
- [ ] T057 [blockedBy: T052] Execute every scenario in `.specify/specs/112-decision-batch-panel/quickstart.md` exactly as written (the two already-executed inspections re-run; the five pinned scenarios now run against the landed engine), and record command, output and exit status per scenario plus the teardown in `notes/quickstart-run.md`.
- [ ] T058 [blockedBy: T052,T055,T056,T057] Run the targeted regression set through the single entry (see § Environment Prerequisites): `tests/unit/test_decision_batch_engine.py`, `tests/contract/test_decision_batch_contract.py`, `tests/contract/test_decision_governance_guards.py`, `tests/contract/test_migration_distribution.py`, `tests/contract/test_probe_nonentity_catalog.py`, `tests/unit/test_validate_decisions.py`; record the zero-new-failure reading against the implement baseline, the glossary/instructions/no-register-edit boundary, and assemble `test-evidence/verification-input.md` with SC-001…SC-010 status/command/evidence pointers (the `final` path criteria carry `pass` plus the smoke record; `verification.md` is derived spec-side and MUST NOT be written here) (FR-044).

**Checkpoint**: 命令文档与框架地图就位；分发闭环绿；quickstart 有实录；`test-evidence/verification-input.md` 可直接派生 `verification.md` 进入 review。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，可立即开始。
- **Foundational (Phase 2)**: 依赖 Setup — 阻塞全部用户故事。
- **User Stories (Phase 3–7)**: 依赖 Foundational；五个故事共享同一所有者页与同一引擎，故按顺序推进（US1 → US2 → US3 → US4 → US5），各故事的检查点独立可测。
- **Polish (Phase 8)**: 依赖 US5 完成（T055 另依赖 Phase 2 的入口面）。

### User Story Dependencies

- **US1（P1）**: Foundational 之后即可开始；产出 scan 与呈现面。
- **US2（P1）**: 依赖 US1 的扫描 payload 与资格状态（`record` 的漂移前置比对对象就是 US1 的呈现 payload）；检查点独立。
- **US3（P1）**: 依赖 US2 的批次记录与决策记录（register/`resolution` 与重放的对象）；检查点独立。
- **US4（P2）**: 依赖 US1 的扫描与 US2 的批次头（拒绝与批次头完备性守的是既有行为，经 T042 显式排序）；检查点独立。
- **US5（P2）**: 依赖 US1 的前例冲突呈现与 US2 的记录写入（取代是 `record` 的分支）；检查点独立。

### Within Each User Story

- 测试先写并转红；实现随后使其转绿；验证行记录红先证据与绿点。
- 同一所有者页与同一引擎按行序追加，不并行写同一文件。
- 每个故事末尾的验证行是 `[green:]` 认领点；测试编写行不认领。

### Parallel Opportunities

- Setup / Foundational 无 `[P]`（同一引擎与冻结基线串行）。
- US1 的 T013 与 T014 可并行（单元测试 vs 契约测试）。
- US2 的 T024 与 T025 可并行（单元测试 vs 契约测试）。
- US4 的 T040 与 T041 可并行（单元测试 vs 所有者页章节）。
- US5 的 T046 与 T047 可并行（单元测试 vs 契约测试）。
- Polish 的 T053 与 T054 可并行（命令文档 vs 框架地图）。

---

## Parallel Example: User Story 1

```bash
# Launch the two US1 test-authoring rows together (distinct write targets):
Task: "Author scan/presentation unit tests in tests/unit/test_decision_batch_engine.py"
Task: "Author owner-extension contract tests in tests/contract/test_decision_batch_contract.py"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 + US2（P1）。两者同为 P1，且「呈现完整但不结案」或「结案但不落记录」都不是用户原话的最小闭环；US2 已包含批次记录与决策记录的写入，因此 US1+US2 构成一次可用的决策批次。US3 是审计与重放增量；US4/US5 是诚实性与边界收口。

1. 完成 Phase 1 + Phase 2（地基）。
2. 完成 US1 + US2 并各自通过检查点。
3. **STOP and VALIDATE**: 用 US1/US2 的独立测试标准验证。
4. 依次交付 US3 → US4 → US5 → Polish。

### Incremental Delivery

1. Setup + Foundational → 引擎接口、命令、技能、probe 收尾、所有者页骨架与冻结基线就绪。
2. US1 → 一次完整呈现（MVP 第一半）。
3. US2 → 异议式结案与批次记录（MVP 第二半）。
4. US3 → register/`resolution`/重放。
5. US4 → 完备性与拒绝诚实。
6. US5 → 取代、边界与强制边界表。
7. Polish → 文档、分发、quickstart 与验收证据包。

### Parallel Team Strategy

单执行体（本线 `single-unit`）。若后续拆并行：测试编写行可按上表 `[P]` 分组；所有者页、引擎、验证行永不由两个执行体同时写。

---

## Notes

- **`[green:]` 分区**：54 条全部由五个故事阶段验证行认领，测试编写行不带 `[green:]`；`validate-tasks.py` 的四项 green 检查应零 ERROR，出现的 WARN 逐条裁定并记录在 `test-evidence/tasks-validator.txt`。
- **测量陷阱**：条款计数单位是行首 `- **C-NNN**` 定义行（`grep -c 'C-'` 会误计正文引用，实测 114）；register 待决策行必须按状态起始词判定（只按 id 前缀得 27）。
- **probe 字面量已漂移**：`test_probe_nonentity_catalog.py` 的字面量 122 落后实测注册面 8 个对象；T011 更新前必须复测并把字面量设为**实测值**（生成时读数 130 + 新对象），不得沿用研究阶段的 122 → 123 简写。
- **批次引擎动作形式**：`quickstart.md` 的文档化调用是位置动作（`decision-batch.py scan …`）；M-10…M-16 的判据动作按该形式登记，107 的九条 `--action` 行保持不变，表—守卫对等测试按两种形式分别断言。
- **门控中性**：所有者页与命令/技能均位于 `scan-confirmation-gates.py` 的扫描面；措辞 MUST 避开 `BLOCKING_PATTERNS`（例如不得出现 `confirmation gate` / `确认门控/确认门禁` 字面量）；判定是「相对基线零新增命中」，不是绝对计数。
- **零改写读数**：既有记录（含 107 时代与各特性的既有决策记录）一律零改写；本特性只追加批次记录、决策记录、register 追加行/状态单元格与块内 `resolution`。
- **`[P]` 与写目标**：`[P]` 只用于写目标逐行不同的测试编写行与文档行；所有者页、引擎、镜像 fan-out 与共享证据 sink 一律按行序串行。
- **PLAN-EDIT**: 无。本文件未改动任何 plan-owned 路径；测试文件、所有者页章节、入口面与引擎动作集均取自 plan 的封闭清单。