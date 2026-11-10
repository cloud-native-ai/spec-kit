# Tasks: Speckit Seal（/speckit.seal：按 review 封装 spec 与分片合并回写）

**Requirement ID**: 099
**Requirement Key**: 099-speckit-seal
**Related Feature**: 099 Speckit Seal（/speckit.seal：按 review 封装 spec 与分片合并回写）
**Input**: Design documents from `.specify/specs/099-speckit-seal/`
**Prerequisites**: requirements.md (28 FR / 9 SC / 3 STR + Clarifications + Assumptions A1–A7), plan.md (9 个工作包 P1–P9、6 条 decision-tension T-001…T-006、12 条 Execution Premise EP-001…EP-012、Mirror Obligations), research.md (R-01…R-21), data-model.md (E1–E14, V1–V16), contracts/ (4 文件 C-001…C-045), quickstart.md (S-1…S-9), feature-ref.md（FR 28/28、SC 9/9 映射）

**Tests Mode**: ON — 宪法 Principle IV "Test-First & Contract-Driven Implementation" 是 test-mandating 原则（"Critical flows MUST have automated regression coverage" / "Integration/contract tests MUST cover cross-service communication and external APIs"），且 plan.md § Constitution Check 第 IV 行与 `contracts/records-and-boundaries.contract.md` C-045 已把 9 条 SC 逐条映射到红先模块。交付面是混合形态：Python 引擎与契约/集成测试走运行时断言；prose/protocol 载体（状态 owner、模板、技能、命令模板）走**结构契约测试**（文件与夹具树断言），不写服务型单测——即 template-only gate 叠加在运行时行之上，而不是替代它们。flow_class = `execution`（`flow-class-check.py --action lookup --unit-id spec:099-speckit-seal` → `flow_class: execution`，source: declaration），无表达类门禁增量。

**Tests**: MANDATORY。红先读数落 `.specify/specs/099-speckit-seal/notes/red-first-evidence.md`；实测读数落 `.specify/specs/099-speckit-seal/test-evidence/`。守护行先于把它转绿的实现行；迁移/回归例外行（守卫既有行为的断言）落在其消费对象之后并带显式 `[blockedBy:]`。

**Organization**: 按 requirements.md 的 4 条用户故事分组（US1/US2/US3 均为 P1，US4 为 P2），前置 Setup（基线冻结）与 Foundational（状态域扩展 + 引擎骨架，阻塞全部故事），尾置 Polish。三条 P1 故事同优先级；阶段顺序服从 plan.md § Execution Model 的工作包依赖链 `P1 ∥ P2 → P3 → P4 → P5 → P6 → P7 → P8 → P9`（P3–P5 共用同一引擎文件 `scripts/python/seal-utils.py`，写域相交串行链），US3（074 回合）按定义是全系统验收、天然最后执行。

## Phase Map

| Phase | Purpose | Rows | Stories / criteria |
|-------|---------|------|--------------------|
| 1 Setup | 冻结覆盖基线、创建证据落点、记录前置实测 | T001–T002 | all |
| 2 Foundational | 状态值域 `Sealed` 与全部消费面同步；引擎骨架与 CLI 契约 | T003–T017 | blocks US1–US4；FR-001…FR-003、FR-021 |
| 3 用户故事 2（P1） | 分片识别、`merge-plan`、`merge-apply` 确定性合并回写 | T018–T024 | US2、SC-003 / SC-004 / SC-005 |
| 4 用户故事 1（P1） | `seal` 判定（只读阶段）与两阶段原子写入 | T025–T029 | US1、SC-001 / SC-002 |
| 5 用户故事 4（P2） | `archive-gate` 单 owner、归档 lane 接线、命令面三件套、边界审计 | T030–T038 | US4、SC-007 / SC-008 |
| 6 用户故事 3（P1） | 074 真实回合：split → merge-back → seal，五项输入逐条处置 | T039–T044 | US3、SC-006 |
| 7 Polish | 全量测试对照、镜像复核、quickstart、`verification.md`、注册表收尾 | T045–T051 | SC-001…SC-009 的 Measurement Sources |

**MVP scope**: US1、US2、US3 均为 P1 且缺一不可独立成值——只合并不封装则 spec 永无终态（US1 缺失），只封装不合并则 074 这类分片父级无法通过前置条件（US2 缺失），两者齐备却无真实回合则验收停在夹具上（US3 缺失）。按模板 MVP 规则，MVP 覆盖**全部三条 P1 故事**（Phase 3–4 与 Phase 6）。US4（P2）约束实现形态而非新增用户能力，与 MVP 同批交付但排在其边界被引用之后（Phase 5）。

### Work-package map（plan.md § Execution Model 的行级投影，每包 ≤16 行）

| 包 | 主题 | 行 | 行数 |
|----|------|----|------|
| P1 | 状态值域扩展与消费面同步 | T003–T015 | 13 |
| P2 | 引擎骨架与 CLI 契约 | T016–T017 | 2 |
| P3 | 分片识别与 `merge-plan` | T018–T020 | 3 |
| P4 | `merge-apply` 确定性写面 | T021–T024 | 4 |
| P5 | `seal` 判定与两阶段写入 | T025–T029 | 5 |
| P6 | `archive-gate` 与既有 lane 接线 | T030–T034 | 5 |
| P7 | 命令面与名册装配 | T035–T038, T051 | 5 |
| P8 | 074 真实回合 | T039–T044 | 6 |
| P9 | 收尾验证与记录 | T045–T050 | 6 |

包定义与依赖边归 plan.md § Execution Model 所有；本表只记行号投影，不复制其依赖规则。

## Definition of Done (DoD)

- DoD-1: **FR/SC 车** — FR-001…FR-028 与 SC-001…SC-009 每条至少被一个任务行在行内逐字引用（§ FR → row trace / § SC → row trace 记录映射）；Check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/099-speckit-seal --stage tasks --repo .` 报 `decision=pass` 且无点名本文件的 unquoted-FR 发现。
- DoD-2: **状态域唯一** — `Sealed` 在 schema owner 与全部 carrier/消费面（模板转移表、`[FEATURE_STATUS]` 行、索引模板词汇、feature-integration 协议、manage-features 词表、non-disposable 表、closure completion-claim 家族）同批识别；任一面移除时 `tests/contract/test_sealed_status_domain.py` 转红并点名该面（FR-001、SC-008、C-025、C-029）。Check: `bash scripts/bash/run-tests.sh tests/contract/test_sealed_status_domain.py tests/contract/test_status_gate_owner.py tests/contract/test_acceptance_state_machine.py tests/contract/test_acceptance_schema_ownership.py -q` 全绿。
- DoD-3: **引擎契约** — `seal-utils.py` 动作封闭集恰四值、退出码封闭集恰三值、`--help`/`--version` 零副作用、未声明选项非零拒绝（FR-021、C-001…C-004）。Check: `bash scripts/bash/run-tests.sh tests/contract/test_seal_engine_contract.py -q` 全绿。
- DoD-4: **确定性与幂等** — `merge-apply` 两次运行逐字节一致、成功重跑零 diff；`seal` 重跑 `already-sealed`；阻断态重跑拒绝清单一致（FR-013、FR-028、C-014、C-007、C-038）。Check: `bash scripts/bash/run-tests.sh tests/integration/test_seal_merge_determinism.py tests/contract/test_seal_seal.py -q` 全绿。
- DoD-5: **拒绝零持久化且逐条点名** — 八类拒绝各以封闭码具名、状态不变、报告含全部未满足条件与修复路径；`state-drift`/`closure-input-defect` 走 exit 2 且不读作通过（FR-009、C-006、C-042）。Check: `bash scripts/bash/run-tests.sh tests/contract/test_seal_seal.py -q` 全绿。
- DoD-6: **074 回合二值终态** — `.specify/specs/074-goal-team-sdd-unification/` 回合产出完整合并清单与父级汇总视图；父 `tasks.md` 未勾选行为 0；seal 终态为 `Sealed` 或至少逐条覆盖 FR-027 五项实测输入（额外具名阻断逐条点名）的拒绝清单；重跑清单一致（SC-006、FR-027、FR-028）。Check: `test-evidence/074-round-20261110.txt` 存在且五个 FR-027 项各有 resolved/blocked 记录。
- DoD-7: **零新增重复机制** — 引擎动作表无 move/delete/archive/push/scheduler；状态值域单 owner；无第二注册表/台账/并行 spec 树（FR-024、SC-008、C-008、C-036）。Check: `bash scripts/bash/run-tests.sh tests/contract/test_seal_boundaries.py tests/contract/test_seal_archive_gate.py -q` 全绿。
- DoD-8: **镜像与副本生成** — `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 零新增漂移（相对 T001 冻结基线）（FR-021、plan § Mirror Obligations）。Check: GATE-2。
- DoD-9: **final 判据全 pass 且有 smoke 记录** — `verification.md` 每条 SC 一行状态，`**Path**: final` 判据均为 `pass`，smoke 三键齐备（GATE-4）。Check: GATE-4。
- DoD-10: **命令参考页落地** — `docs/reference/commands/seal.md` 存在，四个动作与退出码只按指针指向引擎 `--help` 与 `contracts/seal-engine.contract.md`，不复制封闭集（FR-021、plan § Project Structure）。Check: `test -s docs/reference/commands/seal.md`。

**DoD Status**: pending

## Completion Gate

- GATE-1: 全量套件相对实现入口基线零**新增**失败 — 基线名单由 `/speckit.implement` step 6 `**Test runs**` 拥有（`--names-out` 捕获，`comm -13` 比对）；本流程只消费该基线、不另立路径。Check: `bash scripts/bash/run-tests.sh --names-out .specify/specs/099-speckit-seal/test-evidence/final-failed.txt` 后对实现入口基线名单做 `comm -13`，新增名单为空。
- GATE-2: plan.md § Mirror Obligations 的每一对源/镜像零新增漂移。Check: `python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/regen-command-copies.py --check` 均 exit 0。
- GATE-3: 无遗留 `[ ]` / `[>]` 任务行。Check: `grep -cE '^- \[[ >]\] T[0-9]{3} ' .specify/specs/099-speckit-seal/tasks.md` 返回 0。
- GATE-4: 每条 `final` 路径成功判据为 `pass` **且** smoke 记录存在。Check: `.specify/specs/099-speckit-seal/verification.md` 中每条 `**Path**` 读 `final` 的判据有 `SC-NNN_status=pass`，且 `smoke_command=`、`smoke_exit_code=0`、`smoke_evidence_path=`（存在且非空的路径）三键齐备；`blocked`/`deferred`/`fail` 的 final 判据除非有具名用户豁免否则不通过。条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates —— 本行只承载检查，不复制 schema。
- GATE-5: 结构校验器干净。Check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/099-speckit-seal/tasks.md` exit 0 且 0 error。

## Environment Prerequisites

Probed 2026-11-10 in `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal` (branch `099-speckit-seal`). 每个依赖这些裁决的任务行引用本节、不复述结论；implement 入口须重新探测，不跨运行缓存。

- CPython 解释器（引擎与全部测试）：**available** — probe: `python3 --version` @ 2026-11-10 → `Python 3.11.11`；`pyproject.toml` 声明 `requires-python >=3.8`；受影响：全部引擎与守卫行。
- `pytest`：**available** — probe: `python3 -c "import pytest; print(pytest.__version__)"` @ 2026-11-10 → `8.4.2`；受影响：全部测试行与 GATE-1。
- 唯一测试入口 `scripts/bash/run-tests.sh`：**available** — probe: `bash scripts/bash/run-tests.sh tests/contract/test_status_gate_owner.py -q` @ 2026-11-10 → `32 passed in 6.52s`；受影响：全部 `bash scripts/bash/run-tests.sh` 行。
- `git`：**available** — probe: `git --version` @ 2026-11-10 → `git version 2.43.5`；受影响：T043 的钉住提交与 `dirty-spec-tree` 判定、T001 的基线留痕。
- 外部服务 / 网络 / 容器运行时 / 守护进程：**not required** — 引擎 stdlib-only，全部夹具树在 sanctioned 临时根 `.specify/.tmp/` 下本地构建（quickstart S-3/S-7）；受影响：无。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行 —— 不同**写**目标、且不依赖同阶段未完成行。
- **[Story]**: `US1`…`US4`，仅用户故事阶段携带；Setup / Foundational / Polish 阶段零 `[US` 标记。
- **[blockedBy: Txxx,Tyyy]**: 显式依赖；被列出的任务未 `[X]` 前本行不得开始。无标签的行只服从阶段顺序。
- 一行一条任务，精确路径，禁止换行续写。

### Task State Sigil

`- [ ]` open · `- [>]` claimed（多代理专用）· `- [X]` closed · `- [~]` deferred，原因记入 `verification.md` 的 `deferred_tasks=`。

## Path Conventions

两顶帽子（plan.md § Structure Decision、§ Mirror Obligations）：`scripts/`、`shared/`、`skills/`、`templates/`、`tests/` 是**框架源**；`.specify/scripts/`、`.specify/shared/`、`.specify/skills/` 是 `scripts/python/sync-mirrors.py` 生成的运行时投影，绝不手改。`.specify/templates/commands/` 已退役 —— 命令模板经 `scripts/python/regen-command-copies.py` 投影到四个 per-tool 副本。全部路径为仓库根相对路径。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结可比较的基线、建立全部运行时证据落点。

运行时证据的固定落点（owner：`create-tasks` 技能 § Runtime-evidence landing points）：`notes/red-first-evidence.md`、`notes/quickstart-run.md`、`notes/pre-change-measurements.md`、`coverage-baseline.txt`；失败测试基线名单路径由 `/speckit.implement` step 6 `**Test runs**` 拥有，本文件不另立第二路径。

- [X] T001 [P] 创建 `.specify/specs/099-speckit-seal/notes/` 并把前置实测冻结进 `notes/pre-change-measurements.md`：`python3 scripts/python/sync-mirrors.py --check`（实测 2026-11-10：exit 0，`shared/ == .specify/shared/ (111 files, byte-identical)`）、`python3 scripts/python/regen-command-copies.py --check`（exit 0）；失败测试基线名单按 `/speckit.implement` step 6 `**Test runs**` 所有者的形式在实现入口捕获。
- [X] T002 [P] 冻结条款覆盖基线：`python3 scripts/python/account-clause-coverage.py .specify/specs/099-speckit-seal --freeze > .specify/specs/099-speckit-seal/coverage-baseline.txt`（本 spec 有契约集 C-001…C-045，MUST 冻结而非伪造空基线）（FR-025、SC-008）。

**Checkpoint**: 基线可比较、证据落点就绪。

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 状态值域 `Sealed` 的单 owner 扩展与全部消费面同步（plan P1）；引擎骨架与 CLI 契约（plan P2）。二者阻塞全部用户故事。

**⚠️ CRITICAL**: 本阶段完成前不得进入任何用户故事阶段。

### Tests for Foundational

- [X] T003 写红先漂移守卫 `tests/contract/test_sealed_status_domain.py`，覆盖 C-029 的七面（模板转移表状态集、模板 `[FEATURE_STATUS]` 行、索引模板词汇行、feature-integration 协议行、manage-features 词表、non-disposable 状态表、closure completion-claim 家族），运行 `bash scripts/bash/run-tests.sh tests/contract/test_sealed_status_domain.py -q` 并把红输出与退出码记入 `.specify/specs/099-speckit-seal/notes/red-first-evidence.md`（FR-001、SC-008、[blockedBy: T001]）。
- [X] T004 [P] 把 `tests/contract/test_status_gate_owner.py` 的六状态 pin（415–426 行处的 stale-pin 约定）更新为含 `Sealed` 的七状态封闭集（FR-001、C-029）。
- [X] T005 [P] 把 `tests/contract/test_acceptance_state_machine.py` 的六值 pin（`FEATURE_STATUS_VALUES`，92 行与 513 行）更新为七值集；保持 `tests/contract/test_acceptance_schema_ownership.py` 中「每个投影落在域内」的断言原样不变并在七值域下转绿（FR-001、C-029）。

### Implementation for Foundational

- [X] T006 [P] 扩展状态 schema owner `shared/workflow/acceptance-hardening.md` § Feature Status：`Sealed`（[[STR-001]]）的值定义、术语表行，以及唯一转移 `Ready for Review → Sealed` 及其条件；不新增第二个值或第二条转移（FR-001、FR-002、C-024、C-025）。
- [X] T007 [P] 在 `shared/workflow/feature-integration.md` § Status State Machine 增加 `/speckit.seal` 协议行（`Ready for Review → Sealed`，owner 命令 `/speckit.seal`），并把 `Ready for Review → Completed` 标注为对新工作关闭（FR-001、FR-002、FR-003、C-025、C-027）。
- [X] T008 [P] 扩展 `shared/definitions/non-disposable-definitions.md`：注册表状态值域行（196 行）加入 `Sealed`，并在其后的 status×verdict 表补 `Sealed` 行（FR-001、C-025、C-029）。
- [X] T009 [P] 更新 `templates/feature-details-template.md`：§ Canonical Status State Machine 的转移行、`**Status**` 词汇 bullet、`[FEATURE_STATUS]` 占位词汇行同批识别 `Sealed`（FR-001、C-025）。
- [X] T010 [P] 更新 `templates/feature-index-template.md`：状态封闭词汇行加入 `Sealed`（FR-001、C-025）。
- [X] T011 [P] 更新 `skills/internal/manage-features/SKILL.md` 的状态词表，使 reconcile 流程把 `Sealed` 识别为受治理状态（FR-001、C-025）。
- [X] T012 [P] 更新 `scripts/python/closure-acceptance-check.py`：`CLAIMED_IMPLEMENTED`（258 行）加入 `Sealed`，使 completion-claim 家族与 `AUDIT_FAMILY`（1508 行）随动覆盖（FR-001、plan § Disclosed Rulings 3）。
- [X] T013 [P] 更新 `scripts/python/non-disposable-check.py` 的状态×裁决表，使 `Sealed` 行被判定而不是落到范围之外（FR-001、C-025）。
- [X] T014 按 `manage-constitution` 流程收敛宪法生命周期叙述：`templates/constitution-template.md` 与 `.specify/constitution.md` 的终态表述同批改说 `Sealed`（schema owner 为准），版本号与 amend 日期同步（FR-002、FR-003、C-027、[blockedBy: T006]）。
- [X] T015 投影并核对镜像：`python3 scripts/python/sync-mirrors.py --write` 后 `python3 scripts/python/sync-mirrors.py --check`，确认相对 T001 基线在 `shared/`、`templates/`、`skills/internal/`、`scripts/` 零新增漂移（FR-021、plan § Mirror Obligations、[blockedBy: T006,T007,T008,T009,T010,T011,T012,T013,T014]）。
- [X] T016 写红先引擎契约测试 `tests/contract/test_seal_engine_contract.py`，覆盖 C-001…C-010（四动作封闭集、三值退出码、`--help`/`--version` 零副作用、未声明选项非零拒绝、选项面封闭、两阶段声明、stdout-only 拒绝、写路径白名单），红输出记入 `notes/red-first-evidence.md`（FR-021、FR-025、[blockedBy: T001]）。
- [X] T017 实现 `scripts/python/seal-utils.py` 骨架：argparse + `script_interface_cli` 守卫（`--help`/`--version` 零副作用、未声明选项 exit 2）、四动作派发封闭集、三值退出码域、`--json` 稳定负载、写路径白名单常量、C-009 的字面 `.specify` 组件守卫（禁止向上找最近 `.specify` 的启发式）；随后 `python3 scripts/python/sync-mirrors.py --write` 并确认 `--check` exit 0（FR-021、C-001…C-010、[blockedBy: T016]）。

**Checkpoint**: 状态域七面同批识别且漂移守卫可红；引擎骨架满足接口契约。

---

## Phase 3: User Story 2 - 把分片交付的同名输出件确定性合并回父级 (Priority: P1)

**Goal**: `merge-plan`（只读预览：分片集合、15 项输出件动作、ID 映射与冲突）与 `merge-apply`（确定性写父级合并产物、`merge-manifest.json`、分片 `**Merged into**` 标注、拆前行 supersede 处置）。

**Independent Test**: 对 `tests/fixtures/seal/split-pair/` 连跑两次 `merge-apply`——断言两次产物与清单逐字节一致、重跑零 diff；注入「同号不同义」与「无映射条目」冲突——断言 `merge-plan` 以冲突清单返回且无内容被静默丢弃；合并后对夹具父级运行 `validate-requirements.py` 与 `validate-tasks.py` 均 exit 0。

### Tests for User Story 2 (plan face, MANDATORY) ⚠️

- [X] T018 [P] [US2] 构建夹具树 `tests/fixtures/seal/`：`split-pair/`（父 `099-fixture-parent` + 两片各带 `## Parent Mapping` 与 `.specify/state/<parent>.md` 拆分记录）、`conflict-injections/`（同号不同义 `[[STR-NNN]]`、未声明登记处的 `[[STR-NNN]]`（跨登记处歧义）、无映射条目、只命中一半条件的分片候选、同一锚点双端编辑、目录同名文件三态）、`factory-doc/`（出厂文档引用分片本地 ID）（FR-011、FR-013、FR-017）。
- [X] T019 [US2] 写红先契约测试 `tests/contract/test_seal_merge_plan.py`：两条件分片集合、声明顺序与 `order_basis`、15 项封闭候选的动作分类（`merge|create|keep|not-applicable` 且 `not-applicable` 带 `basis`）、目录型候选的文件级单元与同名三态、dated-record 文件的指针纳入（不复制原件）、token→注册表绑定（未声明登记处的引用检出与歧义冲突）、`id_maps` 家族、同号不同义与无映射冲突、出厂文档分片本地 ID 检出，红输出记入 `notes/red-first-evidence.md`（FR-011、FR-012、FR-014、FR-015、FR-016、FR-017、SC-005、[blockedBy: T018]）。

### Implementation for User Story 2 (merge-plan)

- [X] T020 [US2] 在 `scripts/python/seal-utils.py` 实现 `merge-plan` 只读动作：分片发现（C-011 双条件）、顺序派生与依据留痕、15 项候选逐件动作（目录型候选按文件级单位、dated-record 文件指针纳入）、token→注册表绑定检查、ID 家族映射与冲突收集、稳定 JSON，零写盘（FR-011、FR-012、FR-014、FR-015、FR-016、FR-017、C-011…C-018、[blockedBy: T019]）。

### Tests for User Story 2 (apply face, MANDATORY) ⚠️

- [X] T021 [US2] 写红先契约测试 `tests/contract/test_seal_merge_apply.py`：`merge/create/keep` 动作结果（含目录型候选的文件级单位与同名三态）、dated-record 指针纳入（无父级副本、原件字节不变）、全部引用改写为合并后 ID、拆前行 `supersede` 处置、恰一行 `**Merged into**:` 分片标注、`merge-manifest.json` schema（稳定键序、自摘要、`checks`）、dated-record 哈希稳定、合并后 fixture 父级的 `validate-requirements.py` / `validate-tasks.py` exit 0，红输出记入 `notes/red-first-evidence.md`（FR-018、FR-019、SC-004、[blockedBy: T020]）。
- [X] T022 [US2] 写红先集成测试 `tests/integration/test_seal_merge_determinism.py`：两次运行 sha256 名单逐字节一致、`merge-apply` 重跑零 diff、把任一排序键改为「返回时刻」的变异转红，红输出记入 `notes/red-first-evidence.md`（FR-013、SC-003、[blockedBy: T020]）。

### Implementation for User Story 2 (merge-apply)

- [X] T023 [US2] 在 `scripts/python/seal-utils.py` 实现 `merge-apply` 动作：确定性写父级合并产物（目录型候选按文件级单位；dated-record 文件只写指针视图、不复制原件）、`merge-manifest.json`、分片 `**Merged into**:` 标注、C-017 记录过解决方式的出厂文档引用修正（含未声明登记处的引用检出）、C-022 的 supersede 处置、dated-record 哈希断言；随后 `python3 scripts/python/sync-mirrors.py --write` 并确认 `--check` exit 0（FR-012、FR-013、FR-018、FR-019、FR-020、C-014、C-019…C-023、[blockedBy: T021,T022]）。
- [X] T024 [US2] 用既有验证器证成合并产物：对合并后的 fixture 父级运行 `python3 scripts/python/validate-requirements.py` 与 `python3 scripts/python/validate-tasks.py`（均 exit 0），并扫描 ID 连续、重复 ID、悬空引用与未勾选行计数，读数记入 `test-evidence/merge-apply-checks.txt`（FR-014、SC-004、[blockedBy: T023]）。

**Checkpoint**: 合并回写在夹具上确定性成立，冲突显式且阻断。

---

## Phase 4: User Story 1 - 把一条 review 完成的 spec 封装为终态 Sealed (Priority: P1)

**Goal**: `seal` 动作——只读阶段算齐全部前置条件，全成立才进入两阶段原子写入（`seal.md` + 注册表行 + 特性详情）；已封装幂等返回 `already-sealed`；任一不成立逐条点名拒绝。

**Independent Test**: 对 `tests/fixtures/seal/single-spec/`（review 干净、验收齐备、无分片）运行 `seal`——断言状态变为 `Sealed`、`seal.md` 存在且与注册表/详情一致、重跑幂等；对八类失败夹具各断言具名拒绝且状态不变；「三缺一」夹具 MUST 拒绝。

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T025 [US1] 构建封装修剪夹具：`tests/fixtures/seal/single-spec/`（review 干净、`code-review.md` 零 `blocking`、`verification.md` 每条 SC 有状态行、SC 行带行尾 `**Path**` 标记、注册表+详情同处 `Ready for Review`）与 `tests/fixtures/seal/seal-refusals/` 八类失败夹具（from 状态错误、P0 未处置含仅驱动者豁免、验收状态行缺失、闭包 exit 2、分片存在未决冲突、分片未闭合、脏 spec 树、`state-drift`）及「三缺一」变异夹具（FR-005、FR-006、FR-007、FR-008、FR-009、SC-001、SC-002、[blockedBy: T024]）。
- [X] T026 [US1] 写红先契约测试 `tests/contract/test_seal_seal.py`：主路径（exit 0、`seal.md` 落盘、注册表行与详情同批 `Sealed`）、幂等重跑（`already-sealed`、无第二份回执、状态面不动）、八类拒绝逐夹具点名封闭码（含分片未闭合报 `slice-unclosed`）且状态不变、「三缺一」变异转红、074 形态的闭包 exit 2 报 `closure-input-defect` 且不读作通过，红输出记入 `notes/red-first-evidence.md`（FR-005、FR-006、FR-007、FR-008、FR-009、FR-010、SC-001、SC-002、[blockedBy: T025]）。
- [X] T027 [US1] 写红先契约测试 `tests/contract/test_seal_concurrency_and_readonly.py`：两条并行写者对不同 spec 写出不同路径（无共享可变聚合）、`seal` 运行前后 review 与分片测量文件哈希一致、`dirty-spec-tree` 拒绝并指名路径，红输出记入 `notes/red-first-evidence.md`（FR-019、FR-020、SC-009、C-037、C-039、C-040、[blockedBy: T026]）。

### Implementation for User Story 1

- [X] T028 [US1] 在 `scripts/python/seal-utils.py` 实现 `seal` 只读判定段：状态对读取（与闭包引擎 `resolve_claimed_status` 同源；不一致/缺失 → `state-drift` exit 2）、review/P0 判定（C-044 两载体 `- **User waiver**:` 字面形式才计豁免）、`code-review.md` 的 `blocking` 扫描与 `review.md`/`code-review.md` 缺失判定（`review-missing`）、闭包子进程与七键回执逐字复制（exit 2 → `closure-input-defect`）、`merge-manifest.json` 完成度检查（`not-applicable` 须带 `basis`）与分片闭合判据（`slice-unclosed`：未勾选行计数 + `[~]` 的 `deferred_tasks=` 记录）、`git status --porcelain -- <parent-spec-dir>` 脏树探测、以及 stdout-only 且顺序稳定的拒绝报告（FR-004、FR-005、FR-006、FR-007、FR-008、FR-009、C-031、C-042、[blockedBy: T026,T027]）。
- [X] T029 [US1] 实现 `seal` 写入段：同批原子写 `seal.md`（data-model § 3 封闭字段集，重封装写 `supersedes`）、注册表行（`Status` 与 `Last Updated`）与特性详情（`Status` 与 `## Latest Review` 追加），任一写入失败按原字节恢复本批已写文件并 exit 2；随后 `python3 scripts/python/sync-mirrors.py --write` 并确认 `--check` exit 0（FR-002、FR-004、FR-009、FR-010、C-005、C-032、C-033、C-034、[blockedBy: T028]）。

**Checkpoint**: 干净单体 spec 可封装；八类拒绝具名且零持久化；重跑幂等。

---

## Phase 5: User Story 4 - 边界清晰且零新增重复机制 (Priority: P2)

**Goal**: `archive-gate` 单 owner 准入查询、归档 lane 与注册表归档指针的接线、命令面三件套（模板 / 技能 / 副本）、边界与零重复机制的可静态核验。

**Independent Test**: 非 `Sealed` 的 spec 在归档入口被具名拒绝并指向 `/speckit.seal`，`Sealed` 通过；把准入判据复制到第二处时守卫转红；引擎动作表静态审计不含移动/删除/push/调度；双写夹具路径互异。

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T030 [US4] 写红先契约测试 `tests/contract/test_seal_archive_gate.py`：`Sealed` → exit 0；非 `Sealed` → exit 1 且 `pointer` 指向 `/speckit.seal`；遗留 `Completed` 无 C-044 用户裁定 → exit 1 具名；`state-drift` → exit 2；把准入判据复制到第二个实现处时守卫转红，红输出记入 `notes/red-first-evidence.md`（FR-023、SC-007、C-030、[blockedBy: T029]）。

### Implementation for User Story 4

- [X] T031 [US4] 在 `scripts/python/seal-utils.py` 实现 `archive-gate` 只读动作（data-model E11 的裁决负载、准入判据唯一实现、引擎不可用时的读取错误透传）；随后 `python3 scripts/python/sync-mirrors.py --write` 并确认 `--check` exit 0（FR-023、C-030、[blockedBy: T030]）。
- [X] T032 [P] [US4] 接线归档 lane：`skills/internal/sanitize-materials/SKILL.md` 在退休/归档 spec 或标归档指针前查询 `seal-utils.py --action archive-gate`；拒绝 `1`/`2` 时具名拒绝并指回 `/speckit.seal`，绝不退化为「未查询即允许」（FR-022、FR-023、C-030、C-035、[blockedBy: T031]）。
- [X] T033 [P] [US4] 接线注册表归档指针：`skills/internal/manage-features/SKILL.md` 的 `Relocated` 形态归档指针动作先查询 `archive-gate`；注册表 reconcile 本身仍归 manage-features（FR-022、FR-023、C-030、C-035、[blockedBy: T031]）。
- [X] T034 [US4] 写边界审计测试 `tests/contract/test_seal_boundaries.py`：引擎动作表无 move/delete/archive/push/scheduler、状态值域单 owner、无第二套状态机/第二份注册表/第二份台账/并行 spec 树，目录与注册表差异审计干净；审计读数记入 `test-evidence/boundaries-audit.txt`（FR-020、FR-022、FR-024、SC-008、C-008、C-036、[blockedBy: T031]）。
- [X] T035 [US4] 写命令模板 `templates/commands/seal.md`：薄入口（User Input、Delegation 到 `seal-artifact`、Glossary、Wrap-up 探针嵌入、Handoffs），全部判定委派引擎，owner 按路径引用不复述（FR-021、C-041、[blockedBy: T031]）。
- [X] T036 [US4] 写 internal 技能 `skills/internal/seal-artifact/SKILL.md`（只做编排与报告、不复算判定，命名先例 `clarify-artifact`），并在 `shared/definitions/flow-class-definitions.md` 登记 `/speckit.seal` 与 `skill:seal-artifact` 两行（`flow_class: execution`）、在 `shared/definitions/probe-definitions.md` 登记 wrap-up 探针条目（FR-021、C-041、[blockedBy: T035]）。
- [X] T037 [US4] 更新名册/台账 pin：`tests/contract/test_flow_class_ledger.py` 的普查 pin —— 实测 2026-11-10 `flow-class-check.py --action check` 报告 85 units（29 个命令模板 + 56 个技能）；本特性落地后台账须报告 87（30 + 57），按文件内既有的 dated stale-pin 约定更新（FR-021、[blockedBy: T036]）。
- [X] T038 [US4] 生成四个 per-tool 命令副本 `python3 scripts/python/regen-command-copies.py`（绝不手抄），技能经 `python3 scripts/python/sync-mirrors.py --write` 投影，并确认两条 `--check` 均 exit 0、零新增漂移（FR-021、C-041、[blockedBy: T037]）。

**Checkpoint**: 归档准入单 owner 可查询且被消费；命令三件套与副本齐备；边界静态可核验。

---

## Phase 6: User Story 3 - 为 074 的回合提供可执行流程并留下可复现裁决 (Priority: P1)

**Goal**: 以 `.specify/specs/074-goal-team-sdd-unification/` 为目标执行真实 split → merge-back → seal 回合，五项实测输入缺陷逐条显式处置，终态二值（`Sealed` 或具名阻断清单）。

**Independent Test**: 在 074 当前树（074a 32/32、074b 26/26 闭合；父 `tasks.md` 57 个 `[ ]` 行；父级无 `review.md`/`code-review.md`；父 `verification.md` 为聚合指针集）运行完整回合——断言合并清单覆盖两片全部实际输出件、父 `tasks.md` 未勾选行为 0、父 `verification.md` 每条 SC 有状态行、seal 裁决至少逐条覆盖 FR-027 五项（额外阻断逐条点名）、阻断态重跑清单一致。

- [X] T039 [US3] 对 074 运行 `merge-plan` 并逐条处置其报告的冲突（C-018 的 `recheck-clean`；含两组 STR 同号不同义的声明映射核验：074a 本地 `STR-010` → 父 `STR-011`，074b 本地 `STR-004`–`STR-007` → 父 `STR-007`–`STR-010`）:（a）出厂文档 `skills/internal/create-team/SKILL.md:99,101` 的 `[[STR-004]]`/`[[STR-005]]`/`[[STR-006]]` 是 074b 本地语义（`completed`/`blocked`/`failed`），存在性判定成立但合并后须重指向父级 `[[STR-007]]`/`[[STR-008]]`/`[[STR-009]]`（值同，实测 2026-11-10）或改用逐字字面量并记录；（b）为 074 父 `requirements.md` 每条 SC 行补恰一个行尾 `**Path**: final`（严格默认、逐条记录）——实测 2026-11-10 `grep -c '\*\*Path\*\*' .specify/specs/074-goal-team-sdd-unification/requirements.md` = 0（FR-016、FR-027(a)、FR-027(b)、FR-027(c)、SC-006、[blockedBy: T038]）。
- [X] T040 [US3] 对 `.specify/specs/074-goal-team-sdd-unification/` 运行 `merge-apply`：产出父级合并 `tasks.md`（拆前未勾选行按 C-022 以 `> ` 引用前缀保留进「Superseded pre-split record」块——实测 2026-11-10 父 `tasks.md` 未勾选行 57）、父 `verification.md` 聚合指针视图补齐（每条 SC 有状态行）、父 `review.md` 汇总指针视图（两片 review 记录的汇总，缺席新建）、父 `code-review.md` 汇总指针视图（两片 code-review 记录的汇总，缺席新建）、`merge-manifest.json`（逐输出件动作、目录候选文件级单元、dated-record 指针、`id_maps`、`dispositions`、`factory_doc_resolutions`、`checks`）与两片 `requirements.md` 的 `**Merged into**:` 标注（FR-012、FR-018、FR-019、FR-026、SC-006、[blockedBy: T039]）。
- [~] T041 [US3] `[~]` 理由（2026-11-11）：校验已执行并留证；`validate-requirements.py` exit 0、dated-record 哈希一致，但 `validate-tasks.py` 对合并后父 tasks.md 报 43 errors——分片任务行落在无阶段标题区（33 story-labels）与 1–2 位条款未被引擎识别导致 10 green-dangling（见 `test-evidence/074-merge-checks.txt`、`test-evidence/074-round-20261110.txt` B3/B4）；根因在 merge 引擎输出面（P3/P4 写域），按 T-005 以具名阻断收口，不伪造 exit 0。 回合后置校验：`python3 scripts/python/validate-tasks.py .specify/specs/074-goal-team-sdd-unification/tasks.md` exit 0 且未勾选行为 0、`python3 scripts/python/validate-requirements.py .specify/specs/074-goal-team-sdd-unification/requirements.md` exit 0、两片 dated record（`review.md`/`code-review.md`/`verification.md`/`test-evidence/`）运行前后哈希一致，读数记入 `test-evidence/074-merge-checks.txt`（FR-019、SC-004、SC-009、[blockedBy: T040]）。
- [X] T042 [US3] 写集成测试 `tests/integration/test_seal_074_round.py`：真实树只读 `merge-plan` 面断言（两片以 `order_basis: split-record` 被识别、冲突类别具名）与阻断态重跑一致性；测试 MUST NOT 改写 074 树（FR-026、FR-028、SC-006、[blockedBy: T041]）。
- [X] T043 [US3] 先提交回合产物（074 父目录 + 两片标注 + 出厂文档修正），再对 `.specify/specs/074-goal-team-sdd-unification/` 运行 `seal`，把完整 stdout 裁决捕获到 `test-evidence/074-round-20261110.txt`；终态 MUST 二值——`Sealed`（exit 0）或至少逐条覆盖 FR-027 五项实测输入、并逐条点名额外阻断的拒绝清单（exit 1；`state-drift` 为 exit 2）；重跑一次证明清单一致（FR-026、FR-027、FR-028、SC-006、plan § Decision Tensions T-005、[blockedBy: T042]）。
- [X] T044 [US3] 把回合裁决写入既有承载（不建第三份台账）：`merge-manifest.json` 的 `conflicts[]`/`dispositions[]`、仅 `Sealed` 时的 `seal.md` `waivers[]`、被阻断时的 `test-evidence/074-round-20261110.txt`；FR-027 五项（缺 `Path` 标记、STR 同号不同义、出厂文档引用分片本地 ID、074b P0 仅驱动者豁免、57 行拆前记录）逐项呈 `resolved`（证据指针）或 `blocked`（理由），五项之外阻断同样逐条落承载，无第三态、无静默默认（FR-027、C-043、[blockedBy: T043]）。

**Checkpoint**: 074 回合可执行、可复现、裁决完整（`Sealed` 或具名阻断）。

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 全量对照、镜像复核、走查取证与验收记录收尾。

- [ ] T045 [P] 跑全量套件并证明零新增失败：`bash scripts/bash/run-tests.sh --names-out .specify/specs/099-speckit-seal/test-evidence/final-failed.txt`，相对实现入口基线名单做 `comm -13` 比对，读数记入 `test-evidence/final-suite.txt`（FR-025、GATE-1、[blockedBy: T044]）。
- [ ] T046 [P] 终局镜像复核：`python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/regen-command-copies.py --check` 均 exit 0 且相对 T001 基线零新增漂移，读数记入 `test-evidence/final-mirror-checks.txt`（plan § Mirror Obligations、GATE-2、[blockedBy: T044]）。
- [ ] T047 按 quickstart S-1…S-9 走查交付树（含 S-3/S-7 的重跑形态与 S-9 清理），把真实命令、输出与退出码记入 `.specify/specs/099-speckit-seal/notes/quickstart-run.md`——该文件是 GATE-4 的 smoke 证据（FR-026、SC-001…SC-006、[blockedBy: T044]）。
- [ ] T048 写 `.specify/specs/099-speckit-seal/verification.md`：SC-001…SC-009 每条一行 `SC-NNN_status=`（词汇 owner：`shared/workflow/acceptance-hardening.md` § Verification Vocabulary），并给出 smoke 记录三键（`smoke_command=`、`smoke_exit_code=0`、`smoke_evidence_path=` 指向 `notes/quickstart-run.md`）；任一 `final` 判据非 `pass` 即 GATE-4 不通过（SC-001…SC-009、GATE-4、[blockedBy: T045,T046,T047]）。
- [ ] T049 对 Feature 099 执行 Feature Integration reconcile（`manage-features` 流程）：`.specify/features/099-speckit-seal.md` 与 `.specify/features.md` 行同步为实现阶段状态并追加实现/评审记录；确认 tasks 阶段的特性清单复核未暴露新增或失效 Feature（plan § Phase 1 summary：已有 099 行，无合并/废弃/改名）（FR-024、SC-008、[blockedBy: T048]）。
- [ ] T050 覆盖基线终局对照：`python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/099-speckit-seal` 确认相对 T002 冻结的 `coverage-baseline.txt` 零新增未覆盖名，读数记入 `test-evidence/coverage-final.txt`（FR-025、SC-008、[blockedBy: T049]）。
- [X] T051 [P] 写命令参考页 `docs/reference/commands/seal.md`（执行流、产物与用法；四个动作与退出码按指针指向引擎 `--help` 与 `contracts/seal-engine.contract.md`，不复述封闭集），属项目文档面、不扩张 `templates/commands/seal.md` + `skills/internal/seal-artifact/SKILL.md` + `scripts/python/seal-utils.py` 的三件套边界（FR-021、plan § Project Structure、[blockedBy: T038]）。

**Checkpoint**: 全部 SC 有落点，门禁全绿，验收记录齐备。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，立即开始。
- **Foundational (Phase 2)**: 依赖 Setup；阻塞全部用户故事。
- **US2 (Phase 3)**: 依赖 Foundational；对应 plan P3 → P4。
- **US1 (Phase 4)**: 依赖 US2（plan 声明 P2 → P3 → P4 → P5 的同一引擎文件串行链：`seal` 实现段在 `merge-apply` 之后落地）。
- **US4 (Phase 5)**: 依赖 US1（P5 → P6）；命令面 P7 的测试依赖 P6（P6 → P7-tests），故整阶段置于 US1 之后。
- **US3 (Phase 6)**: 依赖 US4（plan：`P2…P7 → P8`）；回合是全系统验收，天然最后。
- **Polish (Phase 7)**: 依赖全部故事完成。

### User Story Dependencies

- **US1 / US2 / US3（均 P1）**: 同优先级；执行顺序由 plan § Execution Model 的包链固定（共享引擎文件的写域串行），不是优先级降级。US2 的合并引擎对 US1 的分片场景前置条件是语义前置；US3 消费前两者。
- **US4（P2）**: 约束实现形态；其 `archive-gate` 与命令面在 US3 回合之前装配完成（plan 的 `P2…P7 → P8`）。

### Within Each User Story

- 测试先写并确认失败，再写实现；迁移/回归例外行落在其消费对象之后并带 `[blockedBy:]`（本文件：T024/T034/T042）。
- 同一文件（`scripts/python/seal-utils.py`）的实现行严格串行：T017 → T020 → T023 → T028 → T029 → T031。

### Parallel Opportunities

- Phase 1：T001 与 T002 并行（不同写目标）。
- Phase 2：T004、T005（不同测试文件）与 T006–T013（各自不同 carrier 文件）并行；T003（红先守卫 + 共享证据文件）、T014、T015、T016、T017 按序。
- Phase 3：T018 夹具构建可先行；其余按 `blockedBy` 串行。
- Phase 5：T032 与 T033 在 T031 之后并行（不同技能文件）。
- Phase 7：T045 与 T046 在 T044 之后并行（不同证据文件）。

---

## Parallel Example: Foundational carrier sync

```bash
# After T003–T005 landed (guard red), the seven carrier surfaces are independent
# files and can be edited concurrently by parallel workers:
Task: "T006 shared/workflow/acceptance-hardening.md — Sealed + transition"
Task: "T007 shared/workflow/feature-integration.md — protocol row"
Task: "T008 shared/definitions/non-disposable-definitions.md — domain line + table"
Task: "T009 templates/feature-details-template.md — transition + status + glossary row"
Task: "T010 templates/feature-index-template.md — vocabulary line"
Task: "T011 skills/internal/manage-features/SKILL.md — status vocabulary"
Task: "T012 scripts/python/closure-acceptance-check.py — completion-claim family"
Task: "T013 scripts/python/non-disposable-check.py — status×verdict rows"
```

---

## Implementation Strategy

### MVP First

1. 完成 Phase 1 Setup + Phase 2 Foundational。
2. 完成三条 P1 故事：US2（Phase 3）→ US1（Phase 4）→ US4 装配（Phase 5 的 P6/P7 是 US3 的前置装配）→ US3（Phase 6）。
3. **STOP and VALIDATE**: 按每条故事的 Checkpoint 独立验证；074 回合给出二值终态。
4. Phase 7 Polish 收尾并产出验收记录。

### Incremental Delivery

1. Phase 2 后：状态域七面可漂移取证，引擎接口契约绿。
2. Phase 3 后：合并回写在夹具上确定性成立（SC-003/004/005 取证）。
3. Phase 4 后：单体 spec 可封装与拒绝语义完备（SC-001/002/009 取证）。
4. Phase 5 后：归档准入单 owner、命令面可运行（SC-007/008 取证）。
5. Phase 6 后：074 真实回合裁决（SC-006 取证）。
6. Phase 7 后：全部门禁与验收记录齐备。

---

## FR → row trace

Generated from this file's own task rows (each FR appears inline in at least one row above).

| FR | Rows |
|----|------|
| FR-001 | T004, T005, T006, T007, T008, T009, T010, T011, T012, T013 |
| FR-002 | T006, T014, T029 |
| FR-003 | T007, T014 |
| FR-004 | T028, T029 |
| FR-005 | T025, T026, T028 |
| FR-006 | T025, T026, T028 |
| FR-007 | T026, T028 |
| FR-008 | T026, T028 |
| FR-009 | T026, T028, T029 |
| FR-010 | T026, T028, T029 |
| FR-011 | T019, T020 |
| FR-012 | T019, T020, T023 |
| FR-013 | T018, T022, T023 |
| FR-014 | T019, T020, T023, T024 |
| FR-015 | T019, T020 |
| FR-016 | T019, T020, T039 |
| FR-017 | T018, T019, T020 |
| FR-018 | T021, T023, T040 |
| FR-019 | T021, T023, T027, T040, T041 |
| FR-020 | T023, T034 |
| FR-021 | T016, T017, T035, T036, T037, T038, T051 |
| FR-022 | T032, T033, T034 |
| FR-023 | T030, T031, T032, T033 |
| FR-024 | T034, T049 |
| FR-025 | T002, T016, T019, T026, T045, T050 |
| FR-026 | T039, T040, T042, T043, T047 |
| FR-027 | T039, T043, T044 |
| FR-028 | T042, T043, T044 |

## SC → row trace

| SC | Rows | 首红/取证模块 |
|----|------|----------------|
| SC-001 | T025, T026, T028, T029 | `tests/contract/test_seal_seal.py` + `tests/contract/test_sealed_status_domain.py` |
| SC-002 | T025, T026, T028 | `tests/contract/test_seal_seal.py`（八类拒绝 + 三缺一变异） |
| SC-003 | T022, T023 | `tests/integration/test_seal_merge_determinism.py` |
| SC-004 | T021, T023, T024 | `tests/contract/test_seal_merge_apply.py` |
| SC-005 | T018, T019, T039 | `tests/contract/test_seal_merge_plan.py` |
| SC-006 | T039, T040, T041, T042, T043, T044, T047 | `tests/integration/test_seal_074_round.py` + `test-evidence/074-round-20261110.txt` |
| SC-007 | T030, T031, T032, T033 | `tests/contract/test_seal_archive_gate.py` |
| SC-008 | T003, T004, T005, T012, T034 | `tests/contract/test_sealed_status_domain.py` + `tests/contract/test_seal_boundaries.py` |
| SC-009 | T027, T040, T041 | `tests/contract/test_seal_concurrency_and_readonly.py` |

---

## Notes

- 前提复测（2026-11-10，本阶段实测并逐字引用）：074 父 `tasks.md` 未勾选行 `grep -cE '^- \[ \]'` = **57**；`074a` 闭合 `grep -cE '^- \[X\]'` = **32**；`074b` = **26**；父 `requirements.md` 的 `**Path**` 标记数 = **0**（`grep -c` 零匹配时退出码为 1 —— 链式命令须用 `;` 或 `|| true`，否则静默中断）；父级无 `review.md`/`code-review.md`（`ls` 实测）；父 `verification.md` 为聚合指针集（提交 `91726a641`）。两片 `## Parent Mapping` 均存在；拆分记录位于 `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（顺序 074a → 074b）。
- 名册普查的陷阱形态：`flow-class-check.py --action check` 实测 **85 units（29 命令 + 56 技能）**；用 `grep -cE '^\| \`'` 数台账行会得到 **0**（行形态为 `| skill:… |` / `| /speckit.… |`，不以反引号开头）——T037 以引擎读数为准。
- 出厂文档引用实测：`skills/internal/create-team/SKILL.md:99` 与 `:101` 以 `[[STR-004]]`/`[[STR-005]]`/`[[STR-006]]` 引用 outcome；074b 本地值 `completed`/`blocked`/`failed` 与父级 `STR-007`/`STR-008`/`STR-009` 同值不同号（两份 STR 表实测）。
- 074 回合终态允许是具名阻断（plan T-005 / A4）：P0 的修复证据或用户显式裁定是回合外输入，本流程 MUST NOT 以自判豁免替代。
- 失败测试基线名单的所有权在 `/speckit.implement` step 6 `**Test runs**`；本文件不复制其路径或比较形式。
- `[P]` 行写目标互异、不共享可变聚合；写 `notes/red-first-evidence.md` 的行故意不标 `[P]`（共享追加槽）。
