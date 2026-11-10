# Tasks: Super Agent Role（相对逻辑角色：定义、协议与 harness 落点）

**Requirement ID**: 095
**Requirement Key**: 095-superagent-role
**Related Feature**: Feature 095 Super Agent Role（相对逻辑角色：定义、协议与 harness 落点）— `.specify/features.md` row `Planned`（tasks 阶段只维护 `Planned`，不改状态）
**Input**: Design documents from `.specify/specs/095-superagent-role/`
**Prerequisites**: `plan.md`（required）、`requirements.md`（required，US1–US5）、`data-model.md`、`contracts/`（4 files）、`quickstart.md`、`feature-ref.md` — 全部在盘并已通过 plan 门禁（HEAD `2c8da54c0`）

**Tests Mode**: ON — `constitution.md` Principle IV “Test-First & Contract-Driven Implementation” is NON-NEGOTIABLE（“Pure functions/utilities MUST have unit tests”“Critical flows MUST have automated regression coverage”“Integration/contract tests MUST cover cross-service communication”）；Principle VII 的 **template-only** 条款另要求文档/模板类交付以结构契约测试（内容、标题、镜像一致性断言）取证，而非运行时测试。两层都 emit：引擎与 digest 走运行时契约测试，定义/模板/派发面走结构契约测试。

**Tests**: MANDATORY。每个用户故事的测试行先写、先跑红（粘贴进 `notes/red-first-evidence.md`），随后才是实现行；既有行为守护测试（迁移/回归类）可在其被测面更新后转绿，但不得静默失效。

**Organization**: 按 `requirements.md` 的 US1–US5 组织，外加 Setup、Foundational（定义 owner，阻塞全部故事）与 Polish & Close-out 三个阶段。本特性一半是 doc-feature（定义页、模板、派发面文档）、一半是引擎（一个只读判定引擎 + digest 扩展 + 六个契约测试模块）：文档面按 `create-tasks/references/phase-shapes.md` 的 doc-feature 分类法（author-section → mirror-parity → render-verify → refresh-verify）执行，引擎面保持 tests → fixtures → implementation → mirror → green 的次序。

## Definition of Done (DoD)

- DoD-1: 六个新契约测试模块全部通过唯一入口 `bash scripts/bash/run-tests.sh`；每个模块的红先行有命令、真实输出与退出码记录在 `notes/red-first-evidence.md`（FR-036, FR-037）
- DoD-2: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/095-superagent-role/tasks.md` 以 0 退出、零 ERROR；每条 WARN 在 `test-evidence/validate-tasks.txt` 中被裁决（不许以删路径的方式消音）
- DoD-3: `plan.md` § Mirror Obligations 的每一行都有显式 write 行与 verify 行（该表是行数与逐行映射的唯一 owner：10 个 source 行覆盖 12 个文件）；被触及的镜像对相对 428 行 DIFF-class 基线无 NEW drift（FR-032, FR-036）
- DoD-4: `scripts/python/role-edge-check.py` 满足宪法 XXI（`--help` / `--version`、未声明选项非零拒绝、读取前不动作），且零写点由结构扫描与夹具字节不变双重取证（FR-005, FR-035）
- DoD-5: `scripts/bash/generate-instructions.sh` 的预算报告 `BUDGET:` 行以 `within` 结尾、日志行显示正余量、分段表含 `## Super Agent (相对逻辑角色)` 行；live 文件携带该段（FR-033, SC-007）
- DoD-6: `verification.md` 中 SC-001…SC-010 均有状态行；`final` 路径准则全部 `pass` 且有 smoke 记录（`smoke_command` / `smoke_exit_code=0` / `smoke_evidence_path` 指向存在且非空文件），`supporting` 路径准则各有自身证据（SC-001…SC-010）
- DoD-7: `observation-appendix.md` 对 080–094 中实际存在的 14 个切片各有一行：`exercised`（可解析证据路径 + 可复现机器记录）或显式 `not-observed` + 理由；配置存在、对话叙述、本特性自身产物均未作为机制行使证据（FR-038, SC-010）
- DoD-8: 受影响的既有测试逐条处置为 `rewrite` / `keep` / `remove` 并记入 `verification.md`；`test_i13` 的 7→8 行数更新与其触发行同一次提交；无断言静默失效（FR-036）
- DoD-9: 无 `[ ]` / `[>]` 行残留；`[~]` 行带理由并列入 `verification.md` 的 `deferred_tasks=`；本特性不 push

**DoD Status**: pending

## Completion Gate

- GATE-1: Full suite has zero NEW failures vs the implement-start baseline — check: `bash scripts/bash/run-tests.sh --names-out <current-names>`（baseline 的路径/旗标/比较形式归 `.specify/templates/commands/implement.md` § **Test runs**，不在此复述）后 `comm -13 <baseline-names> <current-names>` 在本次特性范围内为空
- GATE-2: Every mirror obligation from `plan.md` § Mirror Obligations verified — check: `python3 scripts/python/sync-mirrors.py --check` 与 `notes/pre-change-measurements.md` §2 记录的 428 行 DIFF-class 基线比对，被触及的镜像对无 NEW drift
- GATE-3: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\]' .specify/specs/095-superagent-role/tasks.md` 返回 0
- GATE-4: Every `final`-path success criterion is `pass` **and** the feature's smoke record is present — check: `verification.md` 中每个 `**Path**` 为 `final` 的 SC 行有 `SC-NNN_status=pass`，且 `smoke_command=`、`smoke_exit_code=0`、`smoke_evidence_path=`（路径存在且非空）俱在；条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates
- GATE-5: The new engine obeys the script interface contract — check: `python3 .specify/scripts/python/script-interface-check.py --files scripts/python/role-edge-check.py` 退出 0（该 checker 是仓库级入口，positional 文件会被拒绝）
- GATE-6: This artifact keeps its structural guarantee — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/095-superagent-role/tasks.md` 退出 0

## Environment Prerequisites

- CPython 解释器: **available** — probe: `python3 --version` @ 2026-11-10 → `Python 3.11.11`（下界由 `pyproject.toml` 的 `requires-python = ">=3.8"` 拥有）; affected phases/tasks: 全部引擎与测试行（US1 / US4 / 全部 test 模块）
- 测试运行器: **available** — probe: `ls scripts/bash/run-tests.sh` @ 2026-11-10 → 存在（唯一测试入口）; affected phases/tasks: 全部测试执行行
- 外部环境（容器运行时 / 镜像仓库 / 活集群 / 真实 SSH 主机 / 特殊硬件）: **not required** — probe: `ls tests/fixtures/` @ 2026-11-10 仅见声明式夹具集，本特性的远端形态按既有 external-dispatch recipes 以夹具记录（plan A3，不在套件内铺设 SSH）; affected phases/tasks: none
- 新增第三方依赖 / 包索引: **not required** — probe: `grep -n 'requires-python' pyproject.toml` @ 2026-11-10 → `>=3.8`，零新增依赖（FR-037）; affected phases/tasks: none

**A13 boundary**（owner: `shared/workflow/acceptance-hardening.md` § Gates — 本行是指针，不是第二条规则）：本节只记录 task-generation 的探针结论，每条带探针命令与 ISO 日期。规划期前提归 `plan.md` § Execution Premises；来自依赖特性的记录归 `plan.md` § Inherited Blockers；同一事实写进两个载体是缺陷。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行 —— 与同阶段其他 `[P]` 行不写同一文件，且不依赖未完成行
- **[Story]**: `US1`…`US5`；故事阶段每行恰好一个，非故事阶段（Setup / Foundational / Polish）零个
- **[blockedBy: <行ID>,<行ID>]**: 所列行全部 `[X]` 前本行不得开始；无该标签时只服从阶段顺序
- **[green: <contract>#<clause>]**: 该行首次把该契约子句变绿的红先行标记。本文件只声明**严格子集**：每个契约内被声明的子句序号随行号单调递增（防 `green-cross-phase`），每个测试模块路径最多由一行携带（防 `green-path-divergence`），一个子句最多一行（防 `green-clause-collision`）；未声明的子句是可接受的留白
- 契约路径相对**本文件所在目录**解析（`contracts/…`）
- 每行含精确文件路径；每行必须单行完整（换行会把路径藏出闸门视野）
- 执行性任务一律可追溯 FR/SC，行尾以括号标注

### Task State Sigil (REQUIRED)

`- [ ]` 未开始 · `- [>]` 已认领 / 进行中（多代理运行认领时翻转）· `- [X]` 已关闭且已核实 · `- [~]` 显式延后（`verification.md` 的 `deferred_tasks=` 记录理由）。存在任何 `[ ]` 或 `[>]` 时本次运行未完成。

## Path Conventions

- 单一项目、框架源 + 运行时镜像（Two Hats）：框架源在 `shared/`、`scripts/python/`、`templates/`、`skills/`；运行时镜像在 `.specify/shared/`、`.specify/scripts/`、`.specify/templates/`、`.specify/skills/`（`skills/external/sdd-loop-driver` → `.specify/skills/sdd-loop-driver`）
- 本特性唯一的新目录集是 `tests/fixtures/superagent-role/`（按特性的夹具惯例）；不新建其他目录
- 证据落点：`test-evidence/`（本 spec 目录下）、`notes/`（同上）

## Premise Readings (task generation, 2026-11-10)

本阶段重新测量并落盘于 `notes/pre-change-measurements.md`（实现起点按 implement 预检再测，永不缓存）：

- 指令预算：live **37,454 B** / 模板 **32,975 B** / `INSTRUCTIONS_BUDGET_BYTES=38400`（`generate-instructions.sh:107`）→ 算术余量 **946 B**；trap：`over` 在 `size >= budget` 触发，故可用最后一字节是 `budget-1`，实际余量读数 945 B
- 镜像基线：`sync-mirrors.py --check` 共 **437** 行，其中 **DIFF-class 428** 行（422 `DIFF` + 6 `DIFF[projected]`，与 plan 基线一致）；trap：naive `wc -l` = 437
- 切片清单：`ls .specify/specs/ | grep -E '^0(8|9)[0-9]'` → 080–091、093、094、095；**080–094 实际存在 14 个**，**092 不存在**；trap：“080..094 = 15”与“含 095 的 15”都为假读法
- Per-Agent Payload 表当前 **7** 行（`task_brief` / `territory` / `forbidden_files` / `output_convention` / `incremental_landing` / `model_hint` / `fast_fail_clause`），`test_i13` 硬编码 7 → 加 `role_fields` 后同任务改为 8
- `status-digest.py`：`--action {digest,guard,report}`、`--format {table,json}`、`nothing-running` 退出 3；`--format text` 已退役（既有测试断言退出 2）；trap：新引擎契约的 `--format json|text` 是另一个脚本
- 模板锚点：Framework Map / Runtime & Symlink Model 在模板 **266 / 272** 行，在 live 文件 **283 / 289** 行
- 路径：`scripts/python/role-edge-check.py` 与 `tests/fixtures/superagent-role/` **不存在**；`run-tests.sh`、`validate-tasks.py`、`script-interface-check.py`、`account-clause-coverage.py` 全部存在
- 既有测试约束：`test_i13`（7 行）、digest 表六列、section propagation（live 必须携带模板全部段）、nested run report（顶层段列表不变）、`test_c3_no_third_owner_of_three_layers`（新 owner 页不得重复三层箭头字面量）
- 契约形式：四个契约均为 `md-heading` 子句形式（`## C-N.`），由 `clause_extract.py` 解析；覆盖率基线已冻结（642 行，`base-sha: 2c8da54c06e7`）
- `better-harness.md` 不改（clarify Q6 裁定，覆盖简报字面）；glossary `Super Agent` 行已存在（`auto` / `proposed`）

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 建立证据落点并冻结后续行要读的基线，不改任何行为。

- [ ] T001 Capture the implement-start full-suite baseline by failure name through the runner (`bash scripts/bash/run-tests.sh --names-out <path>`) — the baseline's landing path, capture flag and name-level comparison form are owned by `.specify/templates/commands/implement.md` § **Test runs**（指针，不复述）; the targeted red-first set is each story's own contract module; the closure full-suite run is T051 (FR-036, FR-037)
- [ ] T002 [P] Refresh the task-generation measurements into `.specify/specs/095-superagent-role/notes/pre-change-measurements.md` — re-run every command in that file (instruction sizes, mirror baseline, digest output, payload row count, slice inventory) and carry any changed value forward; the file was seeded by this tasks run on 2026-11-10 with real outputs (FR-033, FR-036)
- [ ] T003 [P] Re-freeze the clause-coverage baseline — `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/095-superagent-role --freeze > .specify/specs/095-superagent-role/coverage-baseline.txt`; this tasks run froze it on 2026-11-10 (642 lines, `base-sha: 2c8da54c06e7`), and the implement pre-flight re-captures it (never cached) (FR-036)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 定义 owner 页与三条指针行 —— 五个用户故事都读这份模型；此阶段不关闭，任何故事行不得开始。

**⚠️ CRITICAL**: 本阶段关闭前不得开始任何用户故事行。

- [X] T004 [P] Author the definitions contract test `tests/contract/test_superagent_definitions.py` — owner page present on both sides after sync; ownership declared up front; required sections (role / edge / depth / protocol / injection / state / visualization / zero-mechanism / terminology); the nine-item closed list slugs; the four message-class tokens; pointer-only discipline (no copied concurrency / reporting / authorization rule text, no budget literal); the role-depth-vs-license-chain sentence; `agent-definitions.md` carries no second subagent definition; the three sibling pointer lines exist; the owner page does not repeat the three-layer marker literal guarded by `tests/contract/test_agent_dispatch_mechanism.py::test_c3_no_third_owner_of_three_layers` — run it red through the runner and paste into `notes/red-first-evidence.md`（FR-001, FR-010, FR-032; SC-001 definition half）
- [X] T005 Author `shared/definitions/superagent-definitions.md` — the single owner: relative role definition (set semantics; `dual-role` as the role-set output marker, never a carrier declaration value; carrier declarations use `subagent` / `superagent`, with the grant carried independently by `dispatch_duty`), edge predicate, role depth (unbounded; one sentence stating the orthogonality with the SDD license-chain depth 2 owned by `subagent-definitions.md` § Dispatch-Time Governance Obligation), the super↔sub protocol (downlink / uplink / message classes / waiting / attempts / authorization / termination), the closed nine-item `role-transition` injection with its item-id slugs, state-sync & recovery mapping over the three fact layers, visualization mapping, zero-second-mechanism boundary, and terminology boundary (`super agent` / `superagent` / `super-agent` alias; not a fourth layer — phrase it without the exact three-layer arrow literal); every rule cited by pointer, never copied [blockedBy: T004] (FR-001, FR-004, FR-008, FR-010, FR-017, FR-025, FR-026, FR-032)
- [X] T006 [P] Add the pointer line to `shared/definitions/agent-definitions.md` — one line naming `shared/definitions/superagent-definitions.md` as the owner of the role concept, and explicitly not a fourth layer; no rule text, no second subagent definition [blockedBy: T005] (FR-001, FR-032)
- [X] T007 [P] Add the pointer line and one boundary sentence to `shared/definitions/subagent-definitions.md` — “the parent-side role is owned there; this page owns the child side”; no rule text [blockedBy: T005] (FR-001, FR-004, FR-032)
- [X] T008 [P] Add the pointer row for the new owner page to `shared/definitions/framework-map.md` — one row naming the file and what it owns; no rule text [blockedBy: T005] (FR-032)
- [X] T009 Sync the four definition sources to their runtime mirrors file-scoped — `python3 scripts/python/sync-mirrors.py --write --only shared/definitions/<file>` for `superagent-definitions.md`, `agent-definitions.md`, `subagent-definitions.md`, `framework-map.md`; disclose that the sync normalizes the pre-existing path-prefix drift on the three pre-existing dirty mirrors (plan § Mirror Obligations), and commit no other dirty file [blockedBy: T006,T007,T008] (FR-032, FR-036)
- [X] T010 Verify the definitions layer — run `tests/contract/test_superagent_definitions.py` green through the runner; `python3 scripts/python/sync-mirrors.py --check` shows no NEW drift on the four pairs against the §2 baseline; paste both readings into `test-evidence/definitions-readings.txt` [blockedBy: T009] (FR-032, SC-001 definition half)

**Checkpoint**: 定义 owner 与三条指针行在源与镜像两侧成立；所有故事读同一份模型。

---

## Phase 3: User Story 1 - 相对角色与角色边可判定 (Priority: P1) 🎯 MVP

**Goal**: 任意两个执行体交给只读判定面，能得到边存在性、每条边上的角色、每个执行体的角色集与深度、以及四类违例 —— 答案只来自既有运行记录。

**Independent Test**: 在 `root-a-b/` 夹具上运行 `--action report`，断言 `summary.edges == 2`、A `roles: ["subagent","superagent"]` / `depth: 1`、B `roles: ["subagent"]` / `depth: 2`；四类违例夹具各自非零；把判定改为按执行体类型时测试转红。

### Tests for User Story 1 (MANDATORY) ⚠️

> 先写测试，实现行落地前必须失败；红跑记录进 `notes/red-first-evidence.md`。

- [X] T011 [P] [US1] Author the engine contract test `tests/contract/test_role_edge_engine.py` — CLI `--help` / `--version` / undeclared-option rejection, exit codes 0/1/2 (named error on unreadable input, explicit empty-set summary, required-vs-optional root split), report & query schemas (incl. `executors[].role_set_marker` = `"dual-role"` on A, `null` elsewhere), the closed four violation kinds, conflict rows naming both paths and the edge identity, determinism (two runs byte-identical), strict input (unknown row → 2; `superagent` is a known declared-role value, never malformed), read-only structural scan + fixture byte-identity, and the three mutation drills (type-based classification red; injected violation red; an explicit `superagent` assertion with no edge where it is the parent red — while a `dispatch_duty: granted` declaration with no children stays green) — run red and paste [green: contracts/role-edge-engine.contract.md#C-1] [green: contracts/role-edge-engine.contract.md#C-11] (FR-005, FR-006, SC-001)
- [X] T012 [P] [US1] Create the clean chain fixture `tests/fixtures/superagent-role/root-a-b/` — root→A and A→B expressed in the three carrier forms of `data-model.md` § 2.1 (team run-report mapping rows under `teams/<slug>/runs/`, driver spine + stage envelope sidecar under `state/`, artifact triplets under `logs/`, registry cross-check entries under `registry/`); A's mapping row declares `role = superagent` with `dispatch_duty = granted` (driving the `role_set_marker` = `"dual-role"` assertion for A), with depths 0, 1 and 2 for root, A and B (FR-002, FR-003, SC-001)
- [X] T013 [P] [US1] Create the violation fixtures `tests/fixtures/superagent-role/violations/self-dispatch/`, `.../dangling-parent/`, `.../unbacked-claim/`, `.../depth-cycle/` — one minimal carrier set each, so each violation kind is judged in isolation (FR-002, FR-005, SC-001)
- [X] T014 [P] [US1] Create the edge-case fixtures `tests/fixtures/superagent-role/conflict/` (one field disagreeing between two carriers → a `conflicts` row naming both paths), `tests/fixtures/superagent-role/malformed/` (unknown row inside a known table → exit 2 naming path and field), `tests/fixtures/superagent-role/empty/` (clean empty set → exit 0 with `summary.edges = 0`) (FR-003, FR-005; contract C-2/C-8/C-9)

### Implementation for User Story 1

- [X] T015 [US1] Implement `scripts/python/role-edge-check.py` — argparse interface per contract C-1 (`--action report|query`, `--state-dir`, `--teams-dir`, `--logs-dir`, `--registry-dir`, `--format json|text`, `--help`, `--version`, undeclared-option rejection), exit codes C-2 with the required/optional root split, report/query schemas C-3/C-4, the closed violation set C-5 (`self-dispatch`, `dangling-parent`, `unbacked-role-claim` — an explicit `superagent` assertion with no edge where it is the parent, never a `dispatch_duty` grant — `depth-inconsistent`; a fifth kind MUST NOT be emitted), zero write points C-6, deterministic ordering C-7 (`(parent, child, attempt)` / `id` / `(kind, subjects)`), conflicts C-8 (field + both paths + owning edge identity), strict input C-9, identity resolution in the exact order of `data-model.md` § 3 (label → line id → spine `run_id` → literal `root` → dangling), depth = shortest edge distance from a root (cycle → `null` + `depth-inconsistent`), executor `state` derivation from the existing carriers per `data-model.md` § 4/§ 9 (completed / failed / cancelled), and parent-side carriers as the primary source with the rest cross-checked [blockedBy: T011,T012,T013,T014] (FR-002, FR-003, FR-004, FR-005, FR-006, FR-013, FR-015)
- [X] T016 [US1] Expose the pure evaluation interface inside `scripts/python/role-edge-check.py` — module-level `read_carrier_inputs(*, state_dir, teams_dir, logs_dir, registry_dir)` and `evaluate_role_model(inputs)` returning the same model as `--action report` (contract C-1's importable-interface row; `--action report` ≡ `evaluate_role_model(read_carrier_inputs(...))`), so the digest calls both exactly once per run; zero write points preserved at module scope [blockedBy: T015] (FR-029, FR-035)
- [X] T017 [US1] Sync the engine to its runtime mirror — `python3 scripts/python/sync-mirrors.py --write --only scripts/python/role-edge-check.py`; verify the pair and the mirror's `--help` / `--version` behaviour is pinned by the contract test [blockedBy: T015,T016] (FR-032, FR-036)
- [X] T018 [US1] Turn the engine contract green — run `tests/contract/test_role_edge_engine.py` through the runner; run the three C-10 command examples against `tests/fixtures/superagent-role/root-a-b/` and paste their real outputs and exit codes into `test-evidence/role-edge-engine-readings.txt` [blockedBy: T017] (FR-005, SC-001)

**Checkpoint**: US1 独立可验 —— 边、角色集（含 `dual-role`）、深度与四类违例都由只读引擎一次回答；把分类改按实体类型时测试转红。

---

## Phase 4: User Story 2 - 身份转变：team 成员并发扇出 10 个 subagent 并自行汇总 (Priority: P1)

**Goal**: 派发载荷在授予派发权时物理携带 `role-transition` 九项指针清单与七个下行角色字段；上行回传与聚合契约不变；并发不变量仍归既有 owner。

**Independent Test**: 载荷夹具逐项删除九项之一 → 既有派发前自检形态（子串判定）阻断；加入「加载 superagent-definitions.md」指令 → 反嵌套契约测试转红；七字段在每个接线面出现；双角色上行回传五要素完整。

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T019 [P] [US2] Create the payload fixtures `tests/fixtures/superagent-role/payload/role-transition-complete.md` (literal `role-transition` + the nine item-id slugs), `.../role-transition-missing-item.md` (one item deleted), `.../role-transition-skill-load.md` (a skill-load instruction — the anti-nesting violation), and the seven downlink role fields block (FR-017, FR-018, SC-002)
- [X] T020 [US2] Author `tests/contract/test_role_transition_payload.py` — nine-item presence by item-id slug on every wired surface; delete any one of the nine item-id slugs → the pre-dispatch self-check's substring form blocks (identifier alone is insufficient); anti-nesting red (skill-load instruction, driver-skill reference, loop logic, full manual); the seven downlink fields on each wired surface; the return contract's five items; per-child aggregate attribution; the dual-role duties-intact mutation (grant superagent and drop an upload duty → red); team mapping-row shape; driver envelope seven fields — run red and paste [blockedBy: T019] [green: contracts/role-transition-payload.contract.md#C-2] [green: contracts/role-transition-payload.contract.md#C-13] (FR-008, FR-009, FR-017, FR-018, FR-019, FR-020, FR-021, SC-002)

### Implementation for User Story 2

- [X] T021 [US2] Edit the dispatch-injection block in `skills/internal/run-agent/SKILL.md` — add the `role-transition` pointer item (when dispatch duty is granted, the payload carries the closed nine-item list) and extend the existing pre-dispatch self-check's substring requirement to the identifier plus its item ids; one bullet each, no new gate, no skill-load instruction [blockedBy: T020] (FR-008, FR-018, FR-021, FR-034, SC-002)
- [X] T022 [P] [US2] Edit `skills/internal/create-team/references/patterns.md` — add the `role_fields` row (seven fields by reference) to the Per-Agent Payload table, and in the SAME task update `tests/contract/test_fast_fail_discipline.py::test_i13_channel_three_payload_sixth_field_row` expected row count 7 → 8 (measured 2026-11-10: 7 rows) [blockedBy: T020] (FR-008, FR-034, FR-036)
- [X] T023 [P] [US2] Edit the Report contract in `skills/internal/create-team/SKILL.md` — make the dispatch mapping table `label | role | dispatch_duty | workspace | parent` mandatory inside `## Execution Detail`; no new top-level section (the existing section list stays byte-identical for `tests/contract/test_nested_run_report.py`) [blockedBy: T020] (FR-030, FR-034)
- [X] T024 [P] [US2] Edit `skills/external/sdd-loop-driver/SKILL.md` — one pointer line in Driver Topology / U0.5: the driver is the root super agent, stage dispatch payloads carry the role fields, execution stays with the existing pre-dispatch self-check and U4 — no new gate, no stage-sequence or sentinel change [blockedBy: T020] (FR-034)
- [X] T025 [P] [US2] Edit `skills/external/sdd-loop-driver/references/stage-prompts.md` — add the `role_edge` object (the seven downlink fields) to the `prompt-<line_id>-<stage>.md.meta.json` envelope sidecar contract [blockedBy: T020] (FR-008, FR-030, FR-034)
- [X] T026 [US2] Sync the three skill surfaces to their runtime mirrors file-scoped — `skills/internal/run-agent/SKILL.md`, `skills/internal/create-team/SKILL.md` + `references/patterns.md`, `skills/external/sdd-loop-driver/SKILL.md` + `references/stage-prompts.md` (the external tree mirrors to `.specify/skills/sdd-loop-driver/…`); verify pair parity [blockedBy: T021,T022,T023,T024,T025] (FR-032, FR-034, FR-036)
- [X] T027 [US2] Turn the payload contract green — run `tests/contract/test_role_transition_payload.py` and `tests/contract/test_fast_fail_discipline.py -k 'i13 or i14'` through the runner; record the delete-one-block and anti-nesting mutation readings in `test-evidence/role-transition-readings.txt` [blockedBy: T026] (FR-018, FR-021, SC-002, SC-009)
- [X] T028 [US2] Register the concurrency-invariant evidence (SC-004) with no second mechanism — run the existing concurrency contract selection `tests/contract/test_concurrency_units.py tests/contract/test_concurrency_serial_reason.py tests/contract/test_concurrency_dispatch_capability.py` green through the runner (the slot+reserve arithmetic and the degradation rules stay with their existing owners); confirm the owner page's concurrency section is pointer-only (T004's discipline) and that this feature moved no reservation and added no capacity mechanism; record in `test-evidence/concurrency-invariants.txt` — the whole change-set audit is T041's job [blockedBy: T005,T027] (FR-022, FR-023, FR-024, SC-004)

**Checkpoint**: US2 独立可验 —— 授职载荷九项封闭、缺项被阻断、红线不可越、双角色回传义务不减、聚合逐子归属、并发仍归既有 owner。

---

## Phase 5: User Story 3 - 两个既有真实形态：本地 team 编排与跨主机 SSH 驱动 (Priority: P1)

**Goal**: 桌面端 SSH 驱动远端 qodercli、本地 qodercli 编排 team、team 成员再扇出 10 个 subagent —— 三个形态用同一套角色、协议与记录，方向与深度可判定。

**Independent Test**: 三个夹具各自的引擎报告给出可解析的边清单、角色方向与深度（root 0 / 成员 1 / 扇出子项 2）；反转任一形态的角色方向时测试转红；远端形态按既有 external-dispatch recipes 以声明式记录，不铺设真实 SSH。

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T029 [US3] Append the three-form cases to `tests/contract/test_role_edge_engine.py` — local-team, remote-topology and fanout-10 direction/depth assertions, the 10-child count, and the direction-reversal mutation; no `[green:]` tag (this row refines the module already marked by T011); run red (fixtures absent) and paste [blockedBy: T011] (FR-007, SC-003)

### Implementation for User Story 3

- [X] T030 [P] [US3] Create `tests/fixtures/superagent-role/local-team/` — local qodercli as root, team members as children (mapping rows + artifact triplets), direction root→members (FR-007(b), SC-003)
- [X] T031 [P] [US3] Create `tests/fixtures/superagent-role/remote-topology/` — desktop session as root, remote qodercli execution as its subagent, recorded per the existing external-dispatch recipes form (declarative; remote artifacts and liveness under the target-project convention) (FR-007(a), SC-003)
- [X] T032 [P] [US3] Create `tests/fixtures/superagent-role/fanout-10/` — root→A (A's row: `role = superagent` + `dispatch_duty = granted`; driving the `role_set_marker` = `"dual-role"` assertion for A) and A→10 children; 10 mapping rows; root depth 0, A depth 1, children depth 2 (FR-007(c), FR-020, FR-024, SC-003)
- [X] T033 [US3] Turn the three-form cases green and record readings — per fixture the engine report (edge list, roles, `role_set_marker`, depths, child count) plus the direction-reversal mutation reading into `test-evidence/three-forms-readings.txt` [blockedBy: T029,T030,T031,T032] (FR-007, SC-003)

**Checkpoint**: 三个真实形态在同一模型下成立；任一方向被反转即转红。

---

## Phase 6: User Story 4 - 状态同步、状态跟踪与可视化 (Priority: P2)

**Goal**: 既有 digest 一次读取就呈现每条执行体的身份、父边、角色集、深度、状态、最近活动与距今时长、stale 标记；截断声明被省略条数；空集渲染 `nothing-running`；恢复后的状态来自既有记录而非对话。

**Independent Test**: 用既有载体造出活动边与中断边，运行 `status-digest.py --action digest`（table + json）；断言字段、`omitted`、`nothing-running`、stale 与 interrupted 结果；删任一字段或加第二 renderer 时测试转红。

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T034 [P] [US4] Author `tests/contract/test_status_digest_roles.py` — `parent` / `roles` / `role_set_marker` / `depth` beside the existing fields in table and JSON; merged-set schema by source type (line rows keep `line_id` / `last_activity_at`; non-line executor rows use `id` / `last_activity`); `omitted` on truncation; `nothing-running` unchanged (exit 3); fan-out shape (one parent row + 10 child rows in one read); single-reader structural assertion (imports the engine's `read_carrier_inputs` + `evaluate_role_model`, one materialization per run, no carrier root read twice); single-renderer structural assertion; provenance (no conversation-memory or process-scan derivation); the interrupted fixture renders stale/interrupted and never silently completed; drop-field / add-renderer mutation red — run red and paste [green: contracts/status-digest-role-view.contract.md#C-1] [green: contracts/status-digest-role-view.contract.md#C-7] (FR-025, FR-026, FR-027, FR-029, FR-030, FR-031, SC-005, SC-006)
- [X] T035 [P] [US4] Create `tests/fixtures/superagent-role/interrupted/` — a parent interrupted while a child still appears running/stale (spine verdict + triplet mtimes), driving the interrupted/attention and stale assertions (FR-027, SC-005)

### Implementation for User Story 4

- [X] T036 [US4] Extend `scripts/python/status-digest.py` — `project_entry` gains `parent`, `roles`, `role_set_marker` (the `dual-role` marker passed through from the engine model) and `depth`; both formats carry them; the role model is computed once per run through the engine's importable interface (one `read_carrier_inputs` + one `evaluate_role_model`; every carrier root read at most once, shared with the legacy entry construction); `nothing-running` / `omitted` / `stale` semantics unchanged; no second parser, renderer or dashboard [blockedBy: T034,T035] (FR-029, FR-030, FR-031, FR-035)
- [X] T037 [US4] Sync the digest to `.specify/scripts/python/status-digest.py` and record its live render — file-scoped sync, pair parity, then run quickstart scenario 2 (table + json) and paste into `test-evidence/status-digest-roles-readings.txt` [blockedBy: T036] (FR-029, SC-006)
- [X] T038 [US4] Turn the digest role test green and keep the existing digest contract green — run `tests/contract/test_status_digest_roles.py` and `tests/contract/test_status_digest.py` through the runner; append the runner readings to `test-evidence/status-digest-roles-readings.txt` [blockedBy: T037] (FR-029, SC-006)
- [X] T039 [US4] Register the state-sync / recovery evidence (SC-005) — assert the interrupted fixture never reads as completed, the stale attempt's return is not consumable (existing attribution values, referenced not restated), resume re-validation stays with the existing authorization owner, and bounded wait / slow-vs-stalled thresholds stay with `watch-model.md`: run `tests/contract/test_sdd_invocation_governance.py` and `tests/contract/test_loop_state_contract.py` green; record in `test-evidence/state-sync-recovery.txt` [blockedBy: T038] (FR-012, FR-014, FR-025, FR-026, FR-027, FR-028, SC-005)

**Checkpoint**: US4 独立可验 —— 角色视图在唯一 digest 中一次读取呈现；空集、截断、stale 与中断语义都按既有行为；无第二 renderer。

---

## Phase 7: User Story 5 - harness 落点与零第二机制 (Priority: P2)

**Goal**: 定义 owner、既有分类法、项目指令模板与派发面引用同一份模型且全为指针；指令体积仍在预算内；框架里没有多出第二套并发机制、registry、状态存储或报告体系。

**Independent Test**: 生成器预算报告 `within` + owner 指针存在性断言 + 变更集结构审计（六个 C-3 断言）；注入第二 store 路径或第二 renderer 时结构断言转红。

### Tests for User Story 5 (MANDATORY) ⚠️

- [X] T040 [P] [US5] Author `tests/contract/test_instructions_budget_superagent_section.py` — the section exists between `## Spec Kit Framework Map` and `## Spec Kit Runtime & Symlink Model`; pointer form (owner path present; no budget literal; no copied rule text; no table; ≤600 B target); the live file carries the section; the budget verdict is `within` (reusing the existing live-size check pattern from `tests/contract/test_instructions_size_budget.py`) — run red and paste [green: contracts/harness-landing.contract.md#C-1] (FR-033, SC-007)
- [X] T041 [P] [US5] Author `tests/contract/test_superagent_zero_mechanism.py` — the six C-3 assertions over the change-set file list and the new/changed sources: no new persistence root, no new registry, no second renderer, no second dispatcher/scheduler/queue or transport/channel, the judgement face is read-only (source scan), owner rules not copied (concurrency, reporting, authorization) — mutation (a second store path or a second renderer) turns red — run red and paste [green: contracts/harness-landing.contract.md#C-3] [green: contracts/harness-landing.contract.md#C-5] (FR-011, FR-016, FR-035, SC-008)

### Implementation for User Story 5

- [X] T042 [US5] Add the `## Super Agent (相对逻辑角色)` section to `templates/instructions-template.md` between `## Spec Kit Framework Map` (line 266) and `## Spec Kit Runtime & Symlink Model` (line 272) — one sentence stating the relative logical role, the owner path `.specify/shared/definitions/superagent-definitions.md`, and one sentence declaring the `role-transition` injection's physical presence; ≤600 B target; no budget literal, no copied rules, no table; in the SAME commit raise the section-count pins in `tests/contract/test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22` (`TPL_EXPECTED` 35 → 36, `LIVE_EXPECTED` 36 → 37) [blockedBy: T040] (FR-033, FR-036, SC-007)
- [X] T043 [US5] Sync the template mirror and run the generator — `python3 scripts/python/sync-mirrors.py --write --only templates/instructions-template.md` then `bash scripts/bash/generate-instructions.sh`; capture the full budget report (BUDGET line `within`, positive headroom, one per-section row for the new section) into `test-evidence/instructions-budget.txt`; the live `.specify/instructions.md` is generator-produced and never hand-edited [blockedBy: T042] (FR-033, SC-007)
- [X] T044 [US5] Verify the harness landing green — run the section test plus `tests/contract/test_instructions_size_budget.py`, `tests/contract/test_instructions_section_propagation.py` and `tests/contract/test_fast_fail_discipline.py -k 'a7_section_counts'` through the runner; append readings to `test-evidence/instructions-budget.txt` [blockedBy: T043] (FR-033, SC-007)
- [X] T045 [US5] Verify zero-second-mechanism and that existing rules are not weakened — run `tests/contract/test_superagent_zero_mechanism.py` and the targeted selection `tests/contract/test_fast_fail_discipline.py -k 'i14' tests/contract/test_sdd_invocation_governance.py tests/contract/test_nested_run_report.py` through the runner, comparing FAILED names against the implement-start baseline (zero NEW failures in this selection; any pre-existing baseline red is named and exempted, never claimed green); record in `test-evidence/zero-mechanism-readings.txt` [blockedBy: T041] (FR-035, SC-008, SC-009)

**Checkpoint**: US5 独立可验 —— 指针段在预算内、live 文件由生成器收敛、零第二机制由结构断言取证、既有禁令相对基线零新增失败（与 FR-036 同一判据）。

---

## Phase 8: Polish & Close-out (Cross-Cutting)

**Purpose**: 收尾附录、既有测试处置台账、quickstart 实跑、镜像总核验与 closure 全量 —— 让特性可交付且可复核。

- [ ] T046 Produce `.specify/specs/095-superagent-role/observation-appendix.md` — one row per 080–094 slice actually present (measured 2026-11-10: 14 slices — 080–091, 093, 094; **092 absent**): each row carries the slice's mechanism claim plus `exercised` with a resolvable evidence path and a reproducible machine record (run record / feedback entry / trigger index entry / digest output / flow-class reading), or the literal `not-observed` with a reason; configuration existence, conversation narrative, “the run went smoothly” and this feature's own artifacts are not evidence; the appendix does not replace this feature's acceptance evidence [blockedBy: T045] (FR-038, SC-010)
- [ ] T047 Verify the appendix mechanically — a deterministic check that every existing slice has exactly one row and every `exercised` row's cited path resolves; the mutation drill marks one `not-observed` row `exercised` **in a copy under `notes/`** (never editing the tracked appendix) and shows the check exits non-zero; record both readings in `test-evidence/observation-appendix-check.txt` [blockedBy: T046] (FR-038, SC-010)
- [ ] T048 Write the existing-test disposition ledger into `.specify/specs/095-superagent-role/verification.md` — `rewrite`: `tests/contract/test_fast_fail_discipline.py::test_i13_channel_three_payload_sixth_field_row` (count 7 → 8, in T022's commit); `keep`: `test_status_digest.py`, `test_instructions_size_budget.py`, `test_instructions_section_propagation.py`, `test_nested_run_report.py` (verified green, no edit); `remove`: none (no asserted fact is deleted); docs disposition: `better-harness.md` unchanged (clarify Q6), three definition pages pointer-only; set `deferred_tasks=` [blockedBy: T045] (FR-036)
- [ ] T049 Run the quickstart end-to-end and write `.specify/specs/095-superagent-role/notes/quickstart-run.md` — scenarios 1 (engine query), 2 (digest table + json), 3 (payload obligation: no command — assert the payload fixture and the SKILL declaration instead), 4 (mirror sync + generator budget report), with real output and teardown [blockedBy: T018,T027,T038,T043] (FR-005, FR-029, FR-033, SC-001, SC-006, SC-007)
- [ ] T050 Verify the complete Mirror Obligations table — every row of `plan.md` § Mirror Obligations (the table is the count owner: 10 source rows covering 12 files — definitions ×4: T009/T010; template ×1: T043; engine ×1: T017; digest ×1: T037; skills ×5 files via 3 rows: T026; the mirror-parity pin `tests/contract/test_mirror_parity_suite.py` covers the pairs) carries both a write task and a verify task; run `sync-mirrors.py --check` against the §2 baseline and confirm no NEW drift; confirm no per-tool command copies were regenerated (no `/speckit.*` command file changed; `regen-command-copies.py` not invoked); record in `test-evidence/mirror-obligations.txt` [blockedBy: T026,T037,T043] (FR-032, FR-036)
- [ ] T051 Run the closure full suite (scheduled after the review round's fixes land) — `bash scripts/bash/run-tests.sh --names-out <current-names>`; compare FAILED names against the implement-start baseline (T001) with `comm -13`; zero NEW failures caused by this feature; record in `test-evidence/closure-suite.txt` [blockedBy: T027,T033,T038,T044,T045] (FR-036, FR-037, SC-009)
- [ ] T052 Re-run the structural validator until exit 0 — `python3 .specify/scripts/python/validate-tasks.py .specify/specs/095-superagent-role/tasks.md`; record the verdict (exit code, ERROR/WARN counts, WARN adjudication) in `test-evidence/validate-tasks.txt` (FR-036)
- [ ] T053 Finalize `.specify/specs/095-superagent-role/verification.md` — SC-001…SC-010 status rows with source pointers; **produce** the smoke record in this task: run `bash scripts/bash/run-tests.sh tests/contract/test_role_edge_engine.py tests/contract/test_role_transition_payload.py tests/contract/test_status_digest_roles.py tests/contract/test_superagent_definitions.py tests/contract/test_instructions_budget_superagent_section.py tests/contract/test_superagent_zero_mechanism.py -q`, capture its stdout/stderr and exit code into `test-evidence/smoke-six-modules.txt` (the file MUST be produced by this task, never assumed), then record `smoke_command` (verbatim), `smoke_exit_code=<measured>`, `smoke_evidence_path=test-evidence/smoke-six-modules.txt`, and the GATE-4 self-check [blockedBy: T047,T048,T050,T051] (SC-001…SC-010, GATE-4)
- [ ] T054 Record the Feature-list review — confirm Feature 095 stays `Planned` (feature-integration table: `/speckit.tasks` maintains `Planned`; implement advances) and that the task breakdown exposed no new or invalidated Feature; write the one-line record into `verification.md`; no `.specify/features.md` edit [blockedBy: T051] (requirements.md § Related Feature; constitution Principle II)

**Checkpoint**: 所有 `[ ]` 关闭或 `[~]` 延后；附录、台账、quickstart、镜像与 closure 读数齐备。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无前置；T001 的基线是 GATE-1 与 T051 的比较对象
- **Foundational (Phase 2)**: 无前置；关闭前阻塞全部用户故事
- **US1 (Phase 3)**: 依赖 Foundational；引擎与夹具是 US3、US4 的前置
- **US2 (Phase 4)**: 依赖 Foundational（T005 的 owner 页是载荷字段的规则源）；与 US1 无硬依赖
- **US3 (Phase 5)**: 依赖 US1（同一个测试模块与引擎）
- **US4 (Phase 6)**: 依赖 Foundational + US1（T016 的纯函数是 digest 的单读接缝）
- **US5 (Phase 7)**: 依赖 Foundational；与 US1–US4 无硬依赖（预算段与结构审计独立）
- **Polish (Phase 8)**: 依赖全部实现阶段；T051 在 review 轮修复落地后执行

### User Story Dependencies

- **US1 (P1)**: Foundational 后可独立开始，无故事内前置
- **US2 (P1)**: Foundational 后可独立开始；与 US1 无硬依赖（T028 只读引用 T005 的 owner 页与既有并发契约测试，不依赖 US1 产物）
- **US3 (P1)**: 依赖 US1 的测试模块与引擎（T011/T015）
- **US4 (P2)**: 依赖 US1 的纯函数接缝（T016）
- **US5 (P2)**: Foundational 后可独立开始

### Within Each User Story

- 测试行先写并跑红（`notes/red-first-evidence.md`），实现行后落地
- 夹具先于引擎/渲染实现（判定面没有输入就无法判定）
- 实现 → 镜像同步 → 转绿与读数
- 每个故事在进入下一故事前完成 Checkpoint

### Parallel Opportunities

- Setup：T002 与 T003 并行（不同文件）
- Foundational：T004 先写（红），T005 随后；T006 / T007 / T008 三条指针行互不冲突可并行
- US1：T011 测试、T012 / T013 / T014 三组夹具互不冲突可并行；实现与镜像串行
- US2：T019 夹具先行；T021–T025 五个接线面写不同文件，可并行；镜像与转绿串行
- US3：T030 / T031 / T032 三组夹具可并行；测试延展（T029）先写
- US4：T034 测试与 T035 夹具可并行；实现与镜像串行
- US5：T040 与 T041 两个测试模块可并行；模板、生成器、验证串行
- Polish：T046 → T047 串行；T049 / T050 可与 T046 并行（不同文件）

---

## Parallel Example: User Story 2 的接线面

```bash
# 五个接线面（T021–T025）互不写同一文件，可同批派出：
Task: "run-agent SKILL 增加 role-transition 指针项与自检子串要求 — skills/internal/run-agent/SKILL.md"
Task: "Per-Agent Payload 增加 role_fields 行并同步改 test_i13 计数 — skills/internal/create-team/references/patterns.md + tests/contract/test_fast_fail_discipline.py"
Task: "Report contract 增加派发映射表 — skills/internal/create-team/SKILL.md"
Task: "Driver Topology / U0.5 增加一行指针 — skills/external/sdd-loop-driver/SKILL.md"
Task: "Stage envelope 增加 role_edge 七字段 — skills/external/sdd-loop-driver/references/stage-prompts.md"
```

## Work Packages (implement plan)

按 `plan.md` § Work Packages 的 P1–P6 切包；每包 ≤16 行。包内可并行的行按上节 Parallel Opportunities 派出，包间按依赖顺序。

| Package (plan) | Rows | Count | Write domain |
|---|---|---|---|
| P1 — Definition owner + pointer lines | T004–T010 | 7 | `shared/definitions/` ×4 + mirrors |
| P2 — Read-only role-edge engine + fixtures (incl. three forms) | T011–T018, T029–T033 | 13 | `scripts/python/role-edge-check.py`, `tests/fixtures/superagent-role/`, engine test module |
| P3 — Protocol & transition-injection wiring | T019–T028 | 10 | three skill surfaces + payload fixtures + payload test + `test_i13` |
| P4 — Digest role view | T034–T039 | 6 | `scripts/python/status-digest.py` + digest test + interrupted fixture |
| P5 — Harness landing | T040–T045 | 6 | `templates/instructions-template.md` + budget / zero-mechanism tests |
| P6 — Close-out | T046–T054 | 9 | appendix, verification.md, notes/quickstart-run.md, evidence |

## Implementation Strategy

### MVP First

**MVP scope rule**: MVP 是同优先级的用户故事集合中各自可独立验收的最小集。本特性的三个 P1 故事（US1 相对角色判定、US2 身份转变注入、US3 三个真实形态）只有合起来才构成一个有价值的增量 —— 有判定无注入则身份转变不可执行，有注入无形态验收则方向不可证 —— 因此 **MVP = US1 + US2 + US3**；US4、US5 与 Polish 为增量交付。

1. 完成 Setup + Foundational
2. 完成 US1 → 独立验收（引擎与四类违例）
3. 完成 US2 → 独立验收（九项注入、缺项阻断、回传义务）
4. 完成 US3 → 独立验收（三形态方向与深度）
5. **STOP and VALIDATE**：逐个故事按 Checkpoint 验收，再进入 US4 / US5 / Polish

### Incremental Delivery

1. Setup + Foundational → 定义层就绪
2. US1 → 角色判定可查（MVP 第一块）
3. US2 → 授职载荷可携带、可阻断
4. US3 → 三形态验收（MVP 完成）
5. US4 → 可视化与恢复可看
6. US5 → harness 落点与零机制取证
7. Polish → 附录、台账、quickstart、closure

## Notes

- `[P]` 行 = 不同文件、无未完成依赖；同一阶段内两个 `[P]` 行写同一文件是缺陷，须改为串行或拆分
- 测试执行唯一入口是 `bash scripts/bash/run-tests.sh`；裸测试 CLI 或 `-m` 模块入口不得出现在任何行的命令里
- 优先 `[~]` 而非把行留成 `[ ]`「以后再补」—— `[~]` 是有理由的显式交接，`[ ]` 阻断完成
- 本文件出现的两处「不改」：`better-harness.md`（clarify Q6）与 `/speckit.*` 命令文件（本特性不新增命令）；二者都是设计裁决，不是遗漏
- 陷阱提醒：镜像基线引用 **428**（DIFF-class）而非 437（`wc -l`）；切片清单是 **14**（092 不存在）；`test_i13` 计数必须与 `role_fields` 同任务更新；digest 的 `--format table|json` 与新引擎的 `--format json|text` 是两个脚本
- 提交纪律：只提交本特性产物；既有脏文件不提交不还原；不 push
