# Tasks: sdd-loop-driver 运行效率优化（SDD Loop Efficiency）

**Requirement ID**: 063 (from branch `063-sdd-loop-efficiency`)
**Requirement Key**: `063-sdd-loop-efficiency`
**Related Feature**: Feature 058 无人值守 SDD 循环驱动机制（演化特性；状态保持 `Implemented`，不回退）
**Input**: Design documents from `.specify/specs/063-sdd-loop-efficiency/` — plan.md, requirements.md, research.md, data-model.md, contracts/ ×5, quickstart.md, feature-ref.md, checklists/requirements.md, notes/source-requirement.md
**Prerequisites**: plan.md (required), requirements.md (required), research.md, data-model.md, contracts/, quickstart.md, feature-ref.md

**Tests Mode**: ON — Constitution Principle IV “Test-First & Contract-Driven Implementation” is test-mandating. This feature is **not** template-only: it ships five executable scripts, one extended watcher and one driver-side stall fixture, so unit + integration tests are mandatory; the 50 contract clauses are pinned by structural contract tests; the LLM-orchestrated stage sequence cannot be replayed in CI and is evidenced by the recorded dry-run trace required by plan.md § Complexity Tracking, never disguised as an automated test.

**Tests**: Red-first for every new script and the watcher extension (`notes/red-first-evidence.md` records the command, real output, and exit status of each red run). Mutation drills from plan.md § Verification & Mutation Plan are mandatory; a mutation that does not turn its named test red means that test is not defending the behavior. Tests Mode ON also requires the two full-suite slots of FR-011 to be honored by this feature's own run: exactly one baseline inside implement (T002) and one driver-owned closure after review (not an implement task; see § Notes → Budget closure ownership). The E2 ledger is the `<!-- test-budget:begin/end -->` JSONL fence **inside the line state spine** established at U0; `<spec-dir>/test-evidence/<stage>.jsonl` carries E3 targeted evidence only and is never the audit authority (I-05).

**Organization**: This is a doc+code hybrid (skill manuals + stdlib scripts). Within each user story the order is: red tests → script/manual implementation → mirror parity → green behavior verification → mutation drill → post-mutation re-run. All four optimization stories append to the same owner document (`references/efficiency-model.md`) and the same `dispatch-recipes.md` / `stage-prompts.md`, so their phases serialize on those files; only fixture authoring (Foundational) is parallel. Story phases are numbered in requirement order (US1→US2→US3→US4→US5) to keep the owner-document sections in authoring order; US4 is also P1 and has no behavioral dependency on US2/US3 (see § Notes → Assumptions D-T2).

**Plan constraint**: `plan` U4 passed at commit 5ab8a5e7; the analyze-loop plan repairs landed at `f0c18e03` and `bcf27c77` with their `PLAN-EDIT:` declarations recorded in plan.md § Plan Repair Record. This tasks-repair-3 modifies `tasks.md` plus the plan-owned pointer/count corrections declared in plan.md § Plan Repair Record 第 4 轮 (N-07/L-01/L-02); any later implement-stage change to a plan-owned artifact MUST carry a `PLAN-EDIT:` line or halt with `ANOMALY:`.

## Definition of Done (DoD)

- DoD-1: Every task row is `[X]`, or `[~]` with a recorded deferral reason in `verification.md` (`deferred_tasks=`); zero `[ ]` / `[>]` rows remain.
- DoD-2: All 24 deliverables listed in `feature-ref.md` § 交付面清单 exist at their canonical paths and are evidenced in `verification.md`.
- DoD-3: All 50 contract clauses (FL-01…FL-10, TB-01…TB-10, PC-01…PC-11, PD-01…PD-10, DI-01…DI-09) are covered by their named test functions, and the coverage meta-test in `tests/contract/test_sdd_loop_driver_efficiency.py` passes.
- DoD-4: `notes/red-first-evidence.md` records every red-first run, and `verification.md` records all seven mutation **target groups / 24 individual mutation applications** from plan.md (admission 5, derive 3, budget 5, plan-changes 3, runner 3, watcher 2, driver-stall 3) with restore confirmation.
- DoD-5: `watch-target.sh --self-test` exits 0 with the historical four failures already green post-merge (28 passed / 0 failed on 2026-10-20; keep them green, never delete), and the four new stream/detach cases pass.
- DoD-6: The `skills/external/sdd-loop-driver` ↔ `.specify/skills/sdd-loop-driver` pair is byte-identical, zero NEW drift is shown relative to the frozen 68-DIFF baseline, and `probe-utils.py --action compile-embeds --check` reports zero drift.
- DoD-7: The implement run consumed exactly one full-suite slot (`baseline`) and recorded it as an E2 row in the line state spine's `test-budget` JSONL fence; no second full suite ran inside implement; targeted test evidence fields are complete; the closure slot is recorded as driver-owned after review and reads the same spine (I-05).
- DoD-8: `verification.md` lists SC-001…SC-013 with a status and evidence class (automated / recorded trace / driver closure); no SC is claimed as automated when its evidence is only the recorded trace; SC-010 cites the [[STR-007]] behavior baseline recorded and replayed by the same `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py` (SB-1…SB-5) with `initial_retries=0` and `exit_code={watcher,runner}`, never substitutes the name-level test-failure baseline (which serves SC-012 only), and never uses decision-table transcription or trace-only evidence.
- DoD-9: Quickstart S1–S7 are executed; S7 is a recorded dry-run decision trace (no nested driver launch) and its non-CI status is stated.
- DoD-10: Feature 058 detail and index are updated with the 063 implementation record **and the missing 063 checklist-stage record** (F-01 governance correction); status remains `Implemented`, never rolled back.

**DoD Status**: pending

## Completion Gate

- GATE-1: Targeted test set green — check: `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py tests/contract/test_sdd_loop_driver_efficiency.py tests/unit/test_admission_check.py tests/unit/test_derive_live_log.py tests/unit/test_audit_test_budget.py tests/unit/test_audit_plan_changes.py tests/integration/test_sdd_loop_efficiency_runner.py tests/integration/test_sdd_loop_efficiency_regression.py -q` exits 0.
- GATE-2: Watcher self-test green — check: `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` exits 0 and reports 0 failed (platform skips, if any, are named).
- GATE-3: Mirror pair byte-identical and zero NEW drift — check: `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` exits 0; `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` exits 0.
- GATE-4: Compile face untouched — check: `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` exits 0 with zero drift.
- GATE-5: Structural validators — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/063-sdd-loop-efficiency/tasks.md` and `python3 .specify/scripts/python/validate-requirements.py .specify/specs/063-sdd-loop-efficiency/requirements.md` both exit 0.
- GATE-6: No open/claimed rows — check: `grep -cE '^- \[[ >]\]' .specify/specs/063-sdd-loop-efficiency/tasks.md` returns 0.
- GATE-7: 24 deliverables present — check: every path in `feature-ref.md` § 交付面清单 passes `test -e`.
- GATE-8: Budget slot discipline — the implement-start baseline is an E2 row in the line state spine's `<!-- test-budget:begin -->` … `<!-- test-budget:end -->` JSONL fence (`$STATE_SPINE` = the state-spine path recorded in the U0 entry declaration), not a spec-dir side file. Check: `python3 skills/external/sdd-loop-driver/scripts/audit-test-budget.py --spine "$STATE_SPINE" --spec-dir .specify/specs/063-sdd-loop-efficiency --stage-check implement` exits 0 and reports `baseline:1 closure:0` while implement is open; the driver appends `closure` to the same spine after review and re-audits with `--stage-check closure` (`baseline:1 closure:1`). `<spec-dir>/test-evidence/implement.jsonl`, if present, is an optional E3 evidence copy only and MUST NOT be treated as the ledger source (I-05).

## Environment Prerequisites

- **bash ≥3.2**: available — probe: `bash --version` @ 2026-10-20 → `5.3.15(1)-release`; affected: all shell scripts, runner integration tests.
- **git**: available — probe: `git rev-parse --abbrev-ref HEAD` @ 2026-10-20 → `063-sdd-loop-efficiency`; affected: admission/coordinator fixture repos, plan-change audits.
- **python3 ≥3.8, stdlib only**: available — probe: `python3 --version` @ 2026-10-20 → `3.9.6`; new scripts MUST stay ≥3.8-compatible and MUST NOT import third-party packages.
- **pytest via the canonical runner**: available — probe: `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q` @ 2026-10-20 → `2 failed, 21 passed`; the runner resolves `python` 3.14.6 + pytest 9.1.1. Direct `python3 -m pytest` is NOT available on this host (python3 has no pytest); always use `scripts/bash/run-tests.sh`.
- **macOS 15.6, no `/proc`**: available with platform caveat — probe: `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` @ 2026-10-20 → `12 passed, 4 failed` (`pid-reuse`, `zombie`, `manifest`, `pgrep-zero-match-trap-reproduced`). T038 repairs these mechanism-side (portable check or explicit platform skip); Linux-only branches are verified structurally, not executed here.
- **Remote SSH/su execution host**: unavailable at generation time — no remote alias/run-user was provided. The remote `ssh + su + nohup` recipe is verified structurally by the PD-06 contract test; local `nohup` detachment is verified behaviorally by the runner integration test. Affected: T035, T039, T041.
- **Network/model API**: not required; no new dependency, service, or API is introduced.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different write targets, no incomplete dependency; only the Foundational fixture rows qualify).
- **[Story]**: `[US1]`..`[US5]` only inside User Story phases; Setup / Foundational rows carry no story label.
- **[blockedBy: Txxx,Tyyy]**: explicit dependency; the task MUST NOT start until every listed row is `[X]`.
- One line per task, including paths and tags; use repository-relative paths.
- No `[green:]` tags in this file: the five contracts use `FL/TB/PC/PD/DI` clause ids, which the repository's machine clause form (`C-<number>`) does not recognize; the tag is optional, and renaming 50 clauses would be a substantive contract change outside this stage. Coverage is instead pinned by one named test function per clause plus the coverage meta-test (T046) and the per-contract traceability tables.

### Task State Sigil (REQUIRED)

- `- [ ]` open; `- [>]` claimed/in-progress; `- [X]` closed; `- [~]` deferred with a recorded reason.

## Path Conventions

- Framework source: `skills/external/sdd-loop-driver/`, `docs/reference/skills/`, `tests/`.
- Runtime mirror: `.specify/skills/sdd-loop-driver/` (generated by `scripts/python/sync-mirrors.py`; never hand-edited).
- Feature evidence: `.specify/specs/063-sdd-loop-efficiency/` (`notes/`, `test-evidence/`, `verification.md`).
- Framework memory: `.specify/memory/features.md`, `.specify/memory/features/058.md`.
- No edits to `templates/`, `src/`, the framework `scripts/` engine tree, `skills/internal/`, or `.specify/templates/commands/`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Author the driver-side stall fixture first, then freeze the pre-change side of every diff premise and record the implement-start full-suite baseline before any behavior-face artifact is written.

- [X] T000 编写驱动侧卡死观测夹具 `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py`（SB-1…SB-5 的唯一执行体）：提供 `--record --worktree <path> --out <json>`、`--replay --worktree <path> --baseline <json> --out <json> [--initial-retries 0]` 与 `--self-test` 三种模式（`--initial-retries` 缺省且唯一允许值为 `0`）；对超时 / 重试上限 / 伪完成三类场景，以自带 stub runner 产生受控 pid/status/heartbeat/runner-log 与 rc，调用真实 `watch-target.sh` 取得 U3 判定，并在夹具内执行文档化的 U4/U5 驱动侧程序（状态脊先写后动、从 `initial_retries=0` 起按实际重试累加、四要素上送件、下一阶段派发决策），从状态脊快照/status/退出记录观测 `watcher_verdict`、`exit_code`（对象 `{"watcher": <int>, "runner": <int>}`，MUST NOT 合并为单值）、`spine_stall_state`、`retries_consumed`、`escalation_package_complete`（或 `not-applicable`）、`next_stage_dispatched`、`spine_write_before_action`、`evidence_ptr`；文件根写 `base_commit`、`recorded_at`、`initial_retries`（固定为 `0`）、`scenarios[]`；`--replay` 负责归一化（时间戳/PID/绝对路径/耗时）与逐字段比较输出；MUST NOT 从 U3/U4/U5 判定表转录、MUST NOT 硬编码期望元组或从基线文件回填，仅允许内部一致性断言（SB-5）；`chmod +x`，先运行 `--self-test` 记录 red（实现前失败）命令、真实输出与退出码到 `.specify/specs/063-sdd-loop-efficiency/notes/red-first-evidence.md`，夹具→消费测试映射由 T007 追加到夹具 README。
- [X] T001 [blockedBy: T000] 记录改前侧测量并保存原始基线输出到 `.specify/specs/063-sdd-loop-efficiency/notes/pre-change-measurements.md`：实跑并粘贴 `python3 scripts/python/sync-mirrors.py --check --only skills/external`（以运行时刻实测为准；2026-10-20 合并 064 后为 exit 2、62 DIFF / 12 目录、本对 0 DIFF；plan 期冻结读数为 68 DIFF / 本对 3 文件）、`bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q`（2026-10-20 合并后实测 23 passed / 0 failed；plan 期基线 21 passed / 2 failed）、`bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test`（2026-10-20 合并后实测 28 passed / 0 failed；plan 期基线 12 passed / 4 failed）、`python3 --version` / `python --version` / `python3 .specify/scripts/python/validate-requirements.py .specify/specs/063-sdd-loop-efficiency/requirements.md`（0 error / 0 warning），并把三份原始输出分别保存为 `notes/baseline-mirror-check.txt`、`notes/baseline-contract-sdd-loop-driver.txt`、`notes/baseline-watch-selftest.txt`；同时逐项 `test -e` 记录交付面初始状态并把清单写入 `notes/pre-change-measurements.md`：15 个新路径（`references/efficiency-model.md`、5 个新脚本、1 个新契约测试文件、4 个单测、2 个集成测试、夹具目录与 `driver-stall-fixture.py`）中 T000 已创建的夹具目录与 `driver-stall-fixture.py` 应存在，其余 13 项应不存在；9 个更新目标（`SKILL.md`、3 份既有 references、`watch-target.sh`、docs 页、既有契约测试、058 详情与索引）应存在（合计 24 项交付）。**同时录制 SC-010 卡死行为基线（[[STR-007]]）**：先执行 N-08 兜底检测——`git log --oneline ba2a18db..HEAD -- skills/external/sdd-loop-driver/SKILL.md skills/external/sdd-loop-driver/references skills/external/sdd-loop-driver/scripts` 必须显示首个行为面提交为 `9e69f3de`，故冻结读数 `ba2a18db` 不适用，实际基线取首个行为面改动前的父提交 `a1aac7e5`，并把该差异写入状态脊 stall baseline 行与 `notes/pre-change-measurements.md`；随后在任何行为面制品落盘之前，用只读 worktree 检出 `a1aac7e5`（`git worktree add --detach <tmp>/063-baseline a1aac7e5`），调用 T000 创建的 `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py --record --worktree <tmp>/063-baseline --out .specify/specs/063-sdd-loop-efficiency/notes/stall-behavior-baseline.json` 录制三类场景处置元组——超时（TIMEOUT）、重试上限（stalled + 四要素上送件）、伪完成（退出 rc=0 且哨兵缺失 → INCOMPLETE，不派发下一阶段）：stub runner 产生受控 pid/status/heartbeat/runner-log 与 rc，真实 `watch-target.sh` 只提供 U3 判定，夹具执行文档化的 U4/U5 驱动侧程序并观测驱动侧字段；watcher 自动夹具不得作为驱动侧字段来源，录制 trace 只作补充、MUST NOT 替代夹具观测（SB-2）；文件根字段 `base_commit`、`recorded_at`、`initial_retries`（固定为 `0`）、`scenarios[]`，每个元组至少含 `watcher_verdict`、`exit_code`（对象 `{"watcher": <int>, "runner": <int>}`，MUST NOT 合并为单值）、`spine_stall_state`、`retries_consumed`、`escalation_package_complete`（或 `not-applicable`）、`next_stage_dispatched`、`spine_write_before_action`、`evidence_ptr`；夹具 MUST NOT 从 U3/U4/U5 判定表转录、MUST NOT 硬编码期望值或从基线文件回填（SB-5）；把路径 + `base_commit` + `initial_retries=0` + `recorded_at` 先写入该线状态脊的 `stall baseline` 行（E8，SB-1）。录制不是全量测试运行，不消耗 FR-011 槽位。本任务不运行全量测试套件；`$STATE_SPINE` 与 T002 同源（驱动 U0 入口声明），缺失即按快速失败以 `ANOMALY:` 回传，不得把基线只留在 notes；若发现 `a1aac7e5` 之后、首个行为面提交之前另有行为面改动，按 FR-038 再向前取首个行为面改动前的提交并在状态脊记录差异。
- [X] T002 [blockedBy: T001] 执行本特性运行唯一的 implement 起点全量基线（预算槽位 `baseline`）：`bash scripts/bash/run-tests.sh --names-out .specify/specs/063-sdd-loop-efficiency/notes/baseline-failed-tests.txt`，把结果写成一条 E2 记录，写入**该线状态脊**的 `<!-- test-budget:begin -->` … `<!-- test-budget:end -->` JSONL 围栏（`$STATE_SPINE` = 驱动 U0 入口声明记录的 `state_spine_path`，`$SPINE_WRITE_MODE=direct|transport` 与 E6/E8 同源；`seq=1`、`slot=baseline`、`stage=implement`、`purpose=implement-start-baseline`、`trigger=scheduled`、`selection_basis=full-suite`、`at`、`command`、`rc`、`passed`/`failed`、`failed_names_path`、`baseline_compare=na`、`evidence_ptr`）。可选：向 `.specify/specs/063-sdd-loop-efficiency/test-evidence/implement.jsonl` 追加一条引用该 E2 记录的 E3 形态证据行（`status=ran`、`selection_basis=full-suite`、`evidence_ptr` 指向状态脊 E2 行与名单文件），但该文件只是传输载体/证据副本，MUST NOT 作为台账或审计来源（I-05）；`SPINE_WRITE_MODE=transport` 时它可承载 E2 形态传输行，驱动 MUST 在 closure 前按 TB-03 合并进状态脊并记 `merge_source`/`merged_at`。写入后用 Python 标准库 `json.loads` 逐行核对围栏内记录可解析且字段齐全（此时 `audit-test-budget.py` 尚未实现，完整审计在 T022 与 GATE-8 以同一 `$STATE_SPINE` 执行）；把同一组计数、状态脊路径与 E2 行位置写入 `notes/pre-change-measurements.md` 与 `verification.md`。implement 内不得再运行第二次全量，收口槽位由驱动在 review 后执行并写入同一状态脊（见 § Notes → Budget closure ownership）。若实现阶段未收到 `STATE_SPINE_PATH`（与 E6/E8 U0 入口同源），按快速失败纪律以 `ANOMALY:` 回传，MUST NOT 另建第二份台账文件；`test-evidence/implement.jsonl` 只是传输载体（`SPINE_WRITE_MODE=transport` 时可承载 E2 形态行），不是台账/审计来源，驱动 MUST 在 closure 前按 TB-03 把它合并进状态脊并记 `merge_source`/`merged_at`。

**Checkpoint**: every later “diff against pre-change” premise has a dated baseline; the implement-start full-suite slot is consumed exactly once.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Author the shared fixtures that every story's red-first tests consume.

**⚠️ CRITICAL**: No user-story test can close until these fixtures exist.

- [X] T003 [P] 创建中型与大型特性夹具 `tests/fixtures/sdd_loop_efficiency/medium/.specify/specs/012-medium/`（`requirements.md` 恰 12 条 `- **FR-NNN**:` 定义行、`tasks.md` 恰 25 条 `- [ ] TNNN` 任务行、`checklists/requirements.md` 全部勾选、`entry.md` 含字面量 `fast-lane=opt-in`、`lines.manifest` 按 E1 §「lines.manifest 行语法」构造恰一行 `012-medium|012-medium`（owner 指针见 T009/T010）、`baseline-failed.txt`、`final-failed.txt`）与 `tests/fixtures/sdd_loop_efficiency/large/.specify/specs/013-large/`（`tasks.md` 60 条任务行、其余同构）。
- [X] T004 [P] 创建 Plan 改动夹具 `tests/fixtures/sdd_loop_efficiency/plan-repo/.specify/specs/012-medium/`：`plan.md`、`data-model.md`、`contracts/fixture-contract.md`、`quickstart.md`、`research.md`、`feature-ref.md` 六件套齐备并可由 quickstart 准备步骤 `git init` + 首次提交。
- [X] T005 [P] 创建预算台账夹具 `tests/fixtures/sdd_loop_efficiency/state-spine-valid.md`（含 `<!-- test-budget:begin -->` / `<!-- test-budget:end -->` JSONL 围栏，`baseline` 与 `closure` 各一条，closure 的 `baseline_compare` 为 `comm -13` 名称级差集，`exception_reason` 语义完整；另含一条 E1 准入记录、`checklist=skipped(fast-lane)` 标记与对应 E3 `status=not-applicable-skipped-stage` 行，用于审计联结用例）与 `tests/fixtures/sdd_loop_efficiency/test-evidence/analyze.jsonl`（一条字段完整的 E3 定向测试证据）；`--spec-dir` 指向的 `test-evidence/` 只承载 E3，E2 台账唯一来源是状态脊围栏。
- [X] T006 [P] 创建 stream 事件与 stub CLI 夹具：`tests/fixtures/sdd_loop_efficiency/stream/non_terminal_sentinel.jsonl`（非终止事件正文含 `PLAN-DONE` 字样、无终止 result）、`tests/fixtures/sdd_loop_efficiency/stream/result_sentinel.jsonl`（终止 result 的 `result` 文本最后一行恰为 `PLAN-DONE`）、`tests/fixtures/sdd_loop_efficiency/stream/malformed.jsonl`（含不可解析行与无 result 的派生失败形态）、`tests/fixtures/sdd_loop_efficiency/stub-cli.sh`（支持 `--output-format stream-json` 的 `stream` 模式、`--help` 不含该旗标且直接传入时非零退出的 `no-stream` 模式、非零退出的 `fail` 模式、退出 0 但无 result 的 `no-result` 模式，并支持 `--delay N` 控制事件间隔）。
- [X] T007 [blockedBy: T000,T003,T004,T005,T006] 编写夹具说明 `tests/fixtures/sdd_loop_efficiency/README.md`（逐项映射 fixture → 消费测试 → 契约条款，含 `driver-stall-fixture.py` → T001/T051 → SB-1…SB-5），执行 `chmod +x tests/fixtures/sdd_loop_efficiency/stub-cli.sh` 并核对 `driver-stall-fixture.py` 可执行位，实跑 `bash tests/fixtures/sdd_loop_efficiency/stub-cli.sh --output-format stream-json` 与 `--mode no-stream` 冒烟，把输出记入 README 的自检段。

**Checkpoint**: fixtures exist and the stub CLI emits both the stream and the no-stream shapes; all story tests can be authored red.

---

## Phase 3: User Story 1 - 中型特性快车道：显式准入与失败回退 (Priority: P1) 🎯 MVP

**Goal**: Admit a medium feature to the fast lane only on an explicit `fast-lane=opt-in` entry and seven mechanically measured criteria, skip `checklist`, keep `analyze`/`review`, and fail closed with a recorded reversion when a criterion later breaks.

**Independent Test**: Run `admission-check.py` against the medium and large fixtures and boundary variants; inspect the JSON admission record, the downstream prompt blocks, and the reversion procedure.

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T008 [US1] Author `tests/unit/test_admission_check.py` red-first：在临时目录复制中型/大型夹具并完成 `git init` + 首次提交 + `012-medium`/`013-large` 分支，覆盖 `test_medium_fixture_admitted`（12 FR / 25 任务、七判据全 pass、`decision=fast-lane`）、`test_large_fixture_denied`（60 任务、criterion a fail、`decision=full-chain`）、`test_task_count_boundary_edges`（8/30 FR 与 10/40 任务含端点通过；7/31、9/41 拒绝）、`test_narrow_task_pattern_only_for_admission`（准入只数 `^- \[[ xX]\] T[0-9]{3}`；宽模式 `^- \[[ xX>~]\] T[0-9]{3}` 仅用于仓库记账，含 `[>]`/`[~]` 的行 MUST NOT 计入准入数）、`test_fr_definition_pattern_pinned`（精确匹配 `^- **FR-[0-9]{3}**:`，owner = requirements.md FR-003(a)；无冒号/说明行不计）、`test_fr_count_excludes_sc_rows`（SC 行不得计入）、`test_missing_or_unparseable_tasks_fail_closed`、`test_missing_checklist_or_entry_fails_closed`、`test_sensitive_or_engine_path_rejected`、`test_lines_manifest_syntax_pinned`（按 data-model.md E1 §「lines.manifest 行语法」：恰一个 ASCII `|`、两字段非空且无空白、`line-label` 匹配 `[A-Za-z0-9._-]+`、注释/空行忽略）、`test_multiline_or_branch_mismatch_lines_manifest_rejected`、`test_open_clarification_marker_rejected`、`test_unresolved_related_feature_rejected`、`test_exit_codes_0_1_2`；把 red 命令、真实输出与退出码记入 `.specify/specs/063-sdd-loop-efficiency/notes/red-first-evidence.md`。
- [X] T009 [US1] [blockedBy: T008] Author `tests/contract/test_sdd_loop_driver_efficiency.py` 的 FL-01…FL-10 测试函数（`test_fl_01_opt_in_literal_pinned` … `test_fl_10_self_application_exclusion`），钉住 `fast-lane=opt-in` 字面量、七判据表、`checklist=skipped(fast-lane)`、准入记录字段、回退程序、analyze/review 不削弱、`admission-check.py` 的 CLI/退出码与脚本常量（8/30、10/40）、owner 文档落点与 063 自应用排除；FL-03(a) 的计数语法只引用 requirements.md FR-003(a)（精确正则 `^- **FR-[0-9]{3}**:`），FL-03(e) 的行语法只引用 data-model.md E1 §「lines.manifest 行语法」，契约测试不得复写或放宽任一 owner；在当前树先红，把 red 运行记入 `notes/red-first-evidence.md`。

### Implementation for User Story 1

- [X] T010 [US1] [blockedBy: T008,T009] 实现 `skills/external/sdd-loop-driver/scripts/admission-check.py`：参数 `--project --base-ref --requirements --tasks --checklists --entry-evidence --lines-manifest --expected-branch [--json-out]`；七判据 (a)–(g) 全部机械判定（FR 只数 `^- **FR-[0-9]{3}**:` 定义行——owner 为 requirements.md FR-003(a)；任务只数 `^- \[[ xX]\] T[0-9]{3}` 行（窄模式；宽模式 `^- \[[ xX>~]\] T[0-9]{3}` 仅用于仓库任务记账，MUST NOT 用于准入，两者不得混用；两者当前恰好同数是巧合，不得写成两者一致），区间常量 8/30 与 10/40 与 FR-003 冻结基线一致且脚本常量是运行时 owner、由契约测试钉住；宪法零改动；引擎/模板/技能/依赖清单与安全敏感面保守超集扫描；`lines.manifest` 严格按 data-model.md E1 §「lines.manifest 行语法」解析——恰一个 ASCII `|`、两字段非空且无空白、label 正则、注释/空行忽略，且恰一行本线记录、分支匹配；clarify 完成且活动标记为零、Related Feature 注册可解析、需求质量清单全绿）；任何解析失败或输入缺失 fail-closed；退出码 0=可录取 / 1=拒绝 / 2=输入或解析错误；仅 Python 标准库且 ≥3.8 兼容。
- [X] T011 [US1] [blockedBy: T010] Author `skills/external/sdd-loop-driver/references/efficiency-model.md` §1（快车道唯一 owner：入口 `fast-lane=opt-in`、裁决点、七判据、E1 准入记录形态、`checklist=skipped(fast-lane)` 下游发布、fail-closed 回退、analyze/review 不变量），并在 `references/dispatch-recipes.md` Recipe 4 写入 `tasks` U4 后、`checklist` 派发前的裁决点与回退序列，在 `references/stage-prompts.md` 写入 implement/review 条件块（跳过标记与准入证据指针，不把缺失 checklist 当缺失必需门）；阶段提示词骨架的 `STATE_SPINE_PATH`/`EVIDENCE_DIR`/`SPINE_WRITE_MODE` 占位符由 T020 统一落地，本节条件块沿用同一骨架，不得另建路径。
- [X] T012 [US1] [blockedBy: T011] 运行 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 同步 `skills/external/sdd-loop-driver/` → `.specify/skills/sdd-loop-driver/`（合并 064 后本对已 0 DIFF；若实现期复测出现漂移则机制侧修复，`references/cli/` 由 064 拥有、只同步不修改内容），随后运行 `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` 与本对 `sync-mirrors.py --check` 过滤，确认零 DIFF 并把修复前后的 C-12/C-18 结果记入 `verification.md`。
- [X] T013 [US1] [blockedBy: T010,T011,T012] 运行 `bash scripts/bash/run-tests.sh tests/unit/test_admission_check.py tests/contract/test_sdd_loop_driver_efficiency.py -q` 转绿，并实跑 quickstart S1/S2（含 `--json-out` 内容核对与 S2 的 `full-chain` 拒绝），把命令、输出、退出码记入 `notes/quickstart-run.md` 与 `verification.md`（`verification.md` 由 T002 创建，T013 追加）；记录 FR-042(a) 的脚本侧证据（阶段序列部分留给 T051 的录制 trace）、准入选址使用窄模式（宽模式仅用于仓库记账）与 SC-001/SC-002 的自动证据。
- [X] T014 [US1] [blockedBy: T013] 执行 admission-check 变异演练：逐一施加「放宽 FR/任务区间端点」「把 SC 行计入 FR」「删去 (c)/(d) 扫描」「接受多行 lines manifest」「把宽任务模式用于准入」五个变异，运行 `test_admission_check.py` 确认对应边界/计数/路径/单线/窄宽模式用例变红（宽模式变异必须让 `test_narrow_task_pattern_only_for_admission` 变红），立即还原；把每个变异的命令、红输出与还原确认记入 `verification.md`。
- [X] T015 [US1] [blockedBy: T014] 变异还原后复跑 `tests/unit/test_admission_check.py` 与 FL 契约 `tests/contract/test_sdd_loop_driver_efficiency.py`，复跑 quickstart S1/S2 并核对期望值；确认 `git diff` 仅含本特性预期改动后关闭 US1 checkpoint，结果记入 `verification.md`。

**Checkpoint**: US1 is independently functional: the medium fixture is admitted with a complete E1 record, the large fixture is refused fail-closed, and the reversion procedure is documented and pinned.

---

## Phase 4: User Story 2 - 全量测试预算与定向测试证据 (Priority: P1)

**Goal**: Bound each run line to exactly two full-suite slots (implement baseline, post-review closure), require deterministic targeted test sets and complete evidence for every intermediate stage and `review`, and make every out-of-slot full run an explicit exception.

**Independent Test**: Run the budget audit against the valid/invalid ledgers; run the injected-regression integration fixture and confirm the final name-level `comm -13` finds the injected failure.

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T016 [US2] Author `tests/unit/test_audit_test_budget.py` red-first：覆盖合法两槽位台账、`test_out_of_slot_without_exception_fails`、槽内重跑只能出现在 closure 之后、第三个槽位拒绝、`environment-failure` 不消耗槽位、缺 `passed/failed` 报 `unknown` 而非 0、closure 缺名称级差集拒绝、`--logs-dir` 命中未入账全量命令拒绝、日志缺失报 `unknown`、摘要 `slots=baseline:1 closure:1 reruns=N exceptions=0 unknown=0`；并补 G-01/I-02 命名用例：`test_ledger_reads_state_spine_fence`（台账唯一来源是状态脊 JSONL 围栏，`test-evidence/implement.jsonl` 不作为台账）、`test_not_applicable_skipped_stage_not_unknown`（E1 准入记录 + [[STR-003]] 联结 → [[STR-008]]，不计入完整性分母）、`test_missing_or_incomplete_admission_record_fails_closed`（收尾时准入记录缺失/字段不全 → 审计判不可信并 exit 1）、`test_empty_selection_escalated_status`（E3 空集升级状态可审计）、`test_multiline_ledger_isolation`（两线台账、槽位、路径互不共享或覆盖）、`test_implement_open_allows_zero_closure`（`--stage-check implement` 只要求 baseline 恰 1、允许 closure 未写入）、`test_closure_requires_two_slots`（`--stage-check closure` 要求 baseline 与 closure 各 1）、`test_docs_only_reduced_field_set`（`not-run-docs-only` 按 `stage`/`row_type=stage-status`/`status`/`selection_basis`/`changed_paths[]`/`evidence_ptr` 六项判完整，运行字段不适用且不报 `unknown`）、`test_stage_status_row_uniqueness`（每个适用阶段恰一条 `row_type=stage-status` 行；整阶段缺行计入完整性分母）、`test_stages_complete_summary`（审计摘要输出 `stages=N complete=N`，授权跳过阶段不计入分母）；把 red 运行记入 `notes/red-first-evidence.md`。
- [X] T017 [US2] Author `tests/integration/test_sdd_loop_efficiency_regression.py` red-first：`test_injected_regression_found_by_name_diff` 在临时目录生成最小 pytest 套件，并用 `bash scripts/bash/run-tests.sh --names-out <临时名单> <临时测试目录> -q` 采集基线（该调用是定向运行，不是全量套件），注入一个已知失败后再次采集，断言 `comm -13 baseline final` 非空且该失败名被报告；同时断言审计脚本拒绝仅比较计数的 closure 记录；把 red 运行记入 `notes/red-first-evidence.md`。
- [X] T018 [US2] [blockedBy: T009] 扩展 `tests/contract/test_sdd_loop_driver_efficiency.py` 的 TB-01…TB-10 测试函数（`test_tb_01_full_run_definition` … `test_tb_10_orchestration_layer_only`），钉住两槽位定义、baseline/closure 程序、定向集固定程序 `targeted-set-v1` 的输入/算法/排序/输出（owner = `contracts/test-budget.md` TB-05）与「同一 `stage_base` + 同一工作树 MUST 复现同一集合」、E3 证据字段（含 `not-applicable-skipped-stage` = [[STR-008]] 及 E1 准入记录 + [[STR-003]] 联结、不计入完整性分母）、台账 JSONL 围栏位于状态脊、槽外例外与槽内重跑、环境失败边界、`--logs-dir` 扫描、编排层实现；在当前树先红并记入 `notes/red-first-evidence.md`。

### Implementation for User Story 2

- [X] T019 [US2] [blockedBy: T016,T017] 实现 `skills/external/sdd-loop-driver/scripts/audit-test-budget.py`：以 `--spine` 指向的线状态脊为台账**唯一来源**，解析 `<!-- test-budget:begin/end -->` JSONL 围栏，校验 `baseline`/`closure`/`in-slot-rerun`/`out-of-slot-exception`/`environment-failure` 语义、每线恰两槽位、例外必须带原因与证据、缺字段报 `unknown`、closure 必须名称级差集；通过 E1 准入记录 + [[STR-003]] 联结识别快车道授权跳过的 `checklist`，把 E3 `not-applicable-skipped-stage`（[[STR-008]]）计为不适用、从完整性分母排除且不得记为 `unknown`；跳过声明缺 E1 或字段不全 → 审计判不可信并 exit 1；E3 空集按 `empty-selection-escalated` 处置（扩大同族或显式例外升级，不得以空集宣称已验证）；多线时逐线隔离台账、槽位与证据路径；每个适用阶段恰一条 `row_type=stage-status` 行（整阶段缺行计入完整性分母）；`not-run-docs-only` 按六项缩减字段集判完整、运行字段不适用且不报 `unknown`；收口审计输出 `stages=N complete=N`；支持 `--spine`、`--spec-dir`（只定位 E3 与名称名单，不作为台账来源）、`--logs-dir`、`--stage-check implement|closure`（implement 只要求 baseline 恰 1 且允许 closure 未写入；closure 要求 baseline 与 closure 各 1）；输出可粘贴进收尾汇总的摘要；退出码 0=通过 / 1=审计失败 / 2=输入或解析错误；仅标准库且 ≥3.8 兼容。
- [X] T020 [US2] [blockedBy: T019] Author `references/efficiency-model.md` §2（两槽位、`targeted-set-v1` 的固定输入/算法/排序/输出并与 TB-05 一致、E2 台账在状态脊围栏与 E3 证据在 `<spec-dir>/test-evidence/` 的分工、空集按 `empty-selection-escalated` 扩大或显式例外升级、快车道授权跳过记 [[STR-008]] 且不入完整性分母、docs-only 六项缩减字段集、每适用阶段唯一 `stage-status` 行与 `stages=N complete=N`、槽外例外、槽内重跑、环境失败边界），在 `references/stage-prompts.md` 写入 implement 起点 baseline（E2 写入状态脊）、implement 内禁止第二次全量、中间阶段与 review 定向测试、`baseline_slot=skip(closure-repair)`、收口修复重入块，并在阶段提示词骨架写入 `STATE_SPINE_PATH`、`EVIDENCE_DIR`、`SPINE_WRITE_MODE=direct|transport` 占位符（与 E6/E8 U0 入口同源；缺失 `STATE_SPINE_PATH` 派发前快速失败；T011/T028/T039 的条件块复用同一骨架，不得另建路径），并在 `references/dispatch-recipes.md` Recipe 4 写入 review 后、合并前的 closure 槽位时序、同一状态脊的追加与审计命令（`audit-test-budget.py --spine "$STATE_SPINE" --spec-dir <spec-dir> --stage-check closure`）及证据路径。
- [X] T021 [US2] [blockedBy: T020] 运行 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 并执行 `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` 与本对 `--check` 过滤，确认零 DIFF，把结果记入 `verification.md`。
- [X] T022 [US2] [blockedBy: T019,T020,T021] 运行 `bash scripts/bash/run-tests.sh tests/unit/test_audit_test_budget.py tests/integration/test_sdd_loop_efficiency_regression.py tests/contract/test_sdd_loop_driver_efficiency.py -q` 转绿，并实跑 quickstart S3；把命令、输出与退出码记入 `notes/quickstart-run.md` 与 `verification.md`；记录 FR-042(b)/(e) 证据，并在 `verification.md` 记录 `baseline_slot=consumed`、`audit-test-budget.py --spine "$STATE_SPINE" --spec-dir .specify/specs/063-sdd-loop-efficiency --stage-check implement` 摘要 `baseline:1 closure:0`、以及「closure 由驱动在 review 后写入同一状态脊、implement 未运行第二次全量」、审计摘要含 `stages=N complete=N` 且每个适用阶段恰一条 `row_type=stage-status` 行（整阶段缺行计入完整性分母）、docs-only 阶段按缩减字段集判完整不报 `unknown`；E2 台账只存在于状态脊围栏，`test-evidence/implement.jsonl` 至多保留一条合法的 E3 引用行（每行合法 JSON，不得承载台账或非 JSON 行，I-05）。
- [X] T023 [US2] [blockedBy: T022] 执行 audit-test-budget 变异演练：逐一施加「允许第三个槽位」「缺 `exception_reason` 仍通过」「用计数比较替代名称级差集」「忽略 `--logs-dir` 扫描命中」「遗漏 docs-only 缩减字段或 `stages=N complete=N`」五个变异，运行 `test_audit_test_budget.py` 确认对应槽位/例外/差集/扫描/完整性用例变红（完整性变异必须让 `test_docs_only_reduced_field_set`、`test_stage_status_row_uniqueness` 或 `test_stages_complete_summary` 变红），立即还原；把证据记入 `verification.md`。
- [X] T024 [US2] [blockedBy: T023] 变异还原后复跑预算单测、回归集成测试与 TB 契约，复跑 quickstart S3；确认台账仍报告恰两槽位、0 例外、0 unknown，且 implement 内没有第二次全量执行，结果记入 `verification.md` 并关闭 US2 checkpoint。

**Checkpoint**: US2 is independently functional: the audit accepts the two-slot ledger, refuses out-of-slot runs without an exception, reports missing evidence as `unknown`, and the injected regression is found by name.

---

## Phase 5: User Story 3 - Plan 阶段「只小修、不重审」约束 (Priority: P2)

**Goal**: After `plan` completes, limit downstream changes to plan-owned artifacts to minor fixes, require a `PLAN-EDIT:` declaration for any touch, classify the final diff deterministically, and route substantive changes to the two FR-022 branches without a silent re-review loop.

**Independent Test**: Run `audit-plan-changes.py` against the plan-repo fixture with a declared minor edit, an undeclared edit, an uncommitted edit, and no touch; inspect the classification and disposition.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T025 [US3] Author `tests/unit/test_audit_plan_changes.py` red-first：在临时 git repo 中覆盖 `test_undeclared_plan_change_flagged`（提交区间触碰 `plan.md`、声明为空 → `undeclared=true`、exit 1）、`test_uncommitted_plan_change_included`（`git status --porcelain` 未提交改动进入触碰集合）、`test_declared_minor_change_passes`（声明行解析、exit 0）、`test_no_touch_reports_none`、`test_diff_stats_and_output_shape`、`test_script_is_read_only`（运行前后工作树与 HEAD 不变），并补 G-01 用例 `test_accumulated_minor_edits_use_final_diff`（多次小修按 `base..HEAD` 的最终 diff 统计汇总，供驱动判 substantive，而不是按单次编辑措辞）与 `test_multi_commit_touch_set`（跨提交触碰集合合并）；把 red 运行记入 `notes/red-first-evidence.md`。
- [ ] T026 [US3] [blockedBy: T018] 扩展 `tests/contract/test_sdd_loop_driver_efficiency.py` 的 PC-01…PC-11 测试函数（`test_pc_01_activation_point` … `test_pc_10_audit_script_interface`、`test_pc_11_reanchoring`），钉住 plan U4 生效点与六个 plan 拥有路径、小修/实质改动定义（按最终 diff 判定，含多处小修累积）、`PLAN-EDIT:` 前缀 token、U4 提交区间加未提交改动检查、两分支分流与 `approved_baseline_commit`（初始 MUST 等于 E4 `plan_commit`；re-baseline 后 MUST 等于 E4 最新 `approved_baseline_commit`，见 PC-11；分支 (a)/(b) 以该提交的 `requirements.md` FR/SC 定义集合与语义为比较对象，不得用工作树文本或其它提交替代）、requirements 门内变更后的 re-anchor（E4 `rebaseline_events[]` 与最新基线；未提交/不可定位不得 re-anchor，受影响 plan 改动按 (b) 上送）、plan 完成后重入必须从状态脊恢复 `active`/`activated_at`（V-E4-2）、analyze 修复路由不变、收口报告、显式排除、脚本只读接口；在当前树先红并记入 `notes/red-first-evidence.md`。

### Implementation for User Story 3

- [ ] T027 [US3] [blockedBy: T025,T026] 实现 `skills/external/sdd-loop-driver/scripts/audit-plan-changes.py`：参数 `--repo --base --head --plan-owned (repeatable) --declarations`；机械输出 `touched_paths[]`（`git diff --name-only <base>..HEAD` 加 `git status --porcelain`）、`declaration_lines[]`、`undeclared` 判定与 diff 统计（按 `base..HEAD` 的**最终累计差异**逐文件输出增删行数，供多处小修累积判定，不得只报最后一笔提交）；退出码 0=无未声明触碰 / 1=存在未声明触碰 / 2=输入或解析错误；只读工作树、仅标准库且 ≥3.8 兼容。
- [ ] T028 [US3] [blockedBy: T027] Author `references/efficiency-model.md` §3（`plan_constraint=active` 生效点与重入恢复、小修/实质改动按最终 diff 的定义、`PLAN-EDIT:` 声明格式的唯一 owner、U4 分类与 FR-022 两分支、`approved_baseline_commit` 初始 = E4 `plan_commit`、re-baseline 后 = E4 最新基线且以该提交的 `requirements.md` 为比较对象、PC-11 re-anchoring（门内 requirements 变更 → 下一个 U4 分类前写 E4 `rebaseline_events[]` 并更新锚点；未提交/不可定位不得 re-anchor，受影响 plan 改动按 (b) 上送；不构成 plan 重审、不移动生效点）、显式排除与设计代价），在 `references/stage-prompts.md` 写入 tasks/analyze/implement/review 的只小修块（复用 T020 的 `STATE_SPINE_PATH`/`EVIDENCE_DIR`/`SPINE_WRITE_MODE` 骨架）与 `ANOMALY:` 实质改动回传要求，并在 `references/dispatch-recipes.md` 写入 plan U4 后登记约束、下游 U4 分类与分流程序、重入时从状态脊恢复 `active`/`activated_at`。
- [ ] T029 [US3] [blockedBy: T028] 运行 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 并执行 `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` 与本对 `--check` 过滤，确认零 DIFF，把结果记入 `verification.md`。
- [ ] T030 [US3] [blockedBy: T027,T028,T029] 运行 `bash scripts/bash/run-tests.sh tests/unit/test_audit_plan_changes.py tests/contract/test_sdd_loop_driver_efficiency.py -q` 转绿，并按 quickstart S6 实跑未声明 plan 改动场景（exit 1、`touched_paths=["plan.md"]`、`undeclared=true`）；把命令、输出与退出码记入 `notes/quickstart-run.md` 与 `verification.md`；记录 FR-042(c) 证据。
- [ ] T031 [US3] [blockedBy: T030] 执行 audit-plan-changes 变异演练：逐一施加「忽略未提交改动」「空声明仍判 declared」「忽略 re-baseline 后的新锚点（按旧 `plan_commit` 比较）」三个变异，运行 `test_audit_plan_changes.py` 与 PC 契约的 `test_pc_11_reanchoring` 确认未声明/未提交/re-anchor 用例变红，立即还原；把证据记入 `verification.md`。
- [ ] T032 [US3] [blockedBy: T031] 变异还原后复跑 plan 单测、PC 契约与 quickstart S6；确认 `PLAN-EDIT:` 格式 owner、两分支路由与「框架内部硬执行显式排除」均在文档面可见，结果记入 `verification.md` 并关闭 US3 checkpoint。

**Checkpoint**: US3 is independently functional: every plan touch is classified, undeclared/substantive changes fail the stage gate, and no silent re-review loop exists.

---

## Phase 6: User Story 4 - 阶段进度可见与驱动会话解耦 (Priority: P1)

**Goal**: Make every stage run with `--output-format stream-json` by default, preserve the raw event stream, derive an incrementally growing compact live log whose last non-empty line is the sentinel, and run stages detached under `nohup` in both local and remote topologies without changing verdicts, exit codes, or re-entry.

**Independent Test**: Run the runner integration fixture (stream, degraded, detached-survival) and the watcher stream cases; terminate the parent shell mid-stage and confirm the detached runner completes and a `--once` snapshot verifies it.

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T033 [US4] Author `tests/unit/test_derive_live_log.py` red-first：覆盖非终止事件正文含哨兵字样时不产生裸哨兵最后一行、终止 result 文本在 EOF 时逐字追加且最后非空行恰为 `PLAN-DONE`、无事件时不伪造进度行、`--finish` 从 raw 恢复终止 result、不可解析行与无 result 的派生失败不伪完成、管道增量输出在进程结束前即可读取；并补 `test_event_to_derived_line_latency_traceable`（每条派生行携带可配对的 raw 事件序号/时间戳，事件→派生行延迟可计算并 ≤120 秒；用 stub `--delay` 夹具验证；无事件区间不产生行、不计入阈值）与 `test_derived_lines_all_have_raw_origin`（伪造行审计：无对应 raw 事件的派生行计数为 0，SC-007）；把 red 运行记入 `notes/red-first-evidence.md`。
- [ ] T034 [US4] Author `tests/integration/test_sdd_loop_efficiency_runner.py` red-first：`test_local_nohup_survives_parent_exit`（父 `bash -c` 启动 nohup runner 后退出，runner 继续并写出 status）、`test_stream_mode_writes_raw_and_live`（raw NDJSON 与 live 最后非空行哨兵）、`test_buffered_degradation_when_cli_lacks_stream`（`no-stream` stub → `progress=degraded` 且不伪完成）、`test_status_fields_and_exit_code_propagation`（`exit/sentinel/progress/detached` 字段与 CLI 退出码）、`test_once_snapshot_does_not_redispatch`（`--once` 快照对已完成阶段只核验）、并补 G-01/SC-007 用例 `test_detached_no_marks_unprotected`（`--detached no` 时 status/派发记录写未脱离风险，不得计为受保护运行）与 `test_raw_receive_timestamps_pair_with_live_lines`（runner 写入 raw 时打点，派生行可按事件配对计算延迟）；把 red 运行记入 `notes/red-first-evidence.md`。
- [ ] T035 [US4] [blockedBy: T026] 扩展 `tests/contract/test_sdd_loop_driver_efficiency.py` 的 PD-01…PD-10 测试函数（`test_pd_01_stream_default_and_raw` … `test_pd_10_runner_interface`），钉住 stream-json 默认与 raw 落盘、增量派生、事件→派生行延迟 ≤120 秒（无事件区间不适用）、每条派生行可追溯到一条 raw 事件且伪造行数为 0、result-only 哨兵、watcher 判定不变、降级标记、双拓扑 nohup、`--once` 重入、`--raw-stream` 证据面与自测、无新等待/服务、runner 接口；在当前树先红并记入 `notes/red-first-evidence.md`。

### Implementation for User Story 4

- [ ] T036 [US4] [blockedBy: T033] 实现 `skills/external/sdd-loop-driver/scripts/derive-live-log.py`：从 stdin/`--events` 增量读取 NDJSON，非终止事件只输出带前缀的单行进度，EOF 时把终止 `result` 事件的 `result` 文本逐字追加；每条派生进度行携带对应 raw 事件的序号与接收时间戳（可配置前缀/字段，供 SC-007 事件→派生行延迟配对），无对应事件不得输出（零伪造行）；支持一次性 `--finish` 从 raw 恢复；不可解析行容错且不伪造完成；仅标准库且 ≥3.8 兼容。
- [ ] T037 [US4] [blockedBy: T034] 实现 `skills/external/sdd-loop-driver/scripts/stage-runner.sh`：参数 `--cli --cli-args --project-dir --prompt-file --sentinel --line --stage --state-dir --mode auto|stream|buffered --detached yes|no`；auto 探测 `--output-format` 能力；stream 模式 `CLI | tee raw-<line>-<stage>.jsonl | python3 derive-live-log.py --out log-<line>-<stage>.log`，并在从 CLI 读取、写入 raw 时逐行打接收时间戳（行内包装或 sidecar，供事件→派生行延迟配对）；写 pid/status/log/heartbeat 四件套与 runner-log；status 含 `exit/at/sentinel/progress/detached`，`detached=no` 时另写 `unprotected=true` 与风险原因，不得计为受保护运行（V-E6-1）；派生失败先 `--finish` 恢复、再 buffered fallback、两者皆无判 `sentinel=0`；退出码等于 CLI 退出码；不自行 detach（nohup 由派发配方提供）。
- [ ] T038 [US4] [blockedBy: T036,T037] 扩展 `skills/external/sdd-loop-driver/scripts/watch-target.sh`：新增可选 `--raw-stream PATH`（WATCH 附 `stream=na|absent|growing|idle`、EVIDENCE 附 raw 路径与字节数，不参与任何 verdict）；修复四个既有自测失败（`pid-reuse`、`zombie`、`manifest`、`pgrep-zero-match-trap-reproduced`）为可跨平台运行或显式平台跳过（禁止删除用例）；新增四个自测用例（非终止事件哨兵字样不判 DONE、终止 result 事件判 DONE、派生失败不伪完成、脱离 runner 在驱动退出后存活）；判定表、退出码与窗口/deadline 语义零改动。
- [ ] T039 [US4] [blockedBy: T036,T037,T038] Author `references/efficiency-model.md` §4（stream-json 主路径、派生与降级、事件→派生行延迟 ≤120 秒与派生行可追溯/零伪造、raw/live 证据、nohup 双拓扑、`detached=no` 的未脱离风险记录、重入），更新 `references/dispatch-recipes.md` Recipe 2 为 `stage-runner.sh` 调用形态并把 `sed` 派生旧形态标注为被取代、Recipe 3 与 Recipe 5 写入本地 `nohup … </dev/null >runner-log 2>&1 &` 与远端 `ssh + su + nohup` 等价形态、派发记录 `detached=yes|no`，更新 `references/watch-model.md` §2/§3/§4 的进度、降级与 raw 证据面（判定表不变），并在 `references/stage-prompts.md` 写入重入 `--once`、脱离派发字段与无独立 sleep 回合的等待纪律，核对阶段提示词骨架仍引用 T020 定义的 `STATE_SPINE_PATH`、`EVIDENCE_DIR`、`SPINE_WRITE_MODE` 占位符（重入与远端 `transport` 不得另建路径）。
- [ ] T040 [US4] [blockedBy: T039] 运行 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver`，确认新增脚本在镜像侧保留可执行位，执行 `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` 与本对 `--check` 过滤，确认零 DIFF，把结果记入 `verification.md`。
- [ ] T041 [US4] [blockedBy: T036,T037,T038,T039,T040] 运行 `bash scripts/bash/run-tests.sh tests/unit/test_derive_live_log.py tests/integration/test_sdd_loop_efficiency_runner.py tests/contract/test_sdd_loop_driver_efficiency.py -q` 与 `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` 转绿，并实跑 quickstart S4/S5；把命令、输出、退出码与 `--once` 重入证据记入 `notes/quickstart-run.md` 与 `verification.md`；记录 FR-042(d) 证据与 SC-008/SC-009/SC-011 的自动证据。
- [ ] T042 [US4] [blockedBy: T041] 执行 derive-live-log、stage-runner、watch-target 变异演练：逐一施加「对非终止事件输出裸哨兵」「在 result 之前追加结果文本」「删除 result 提取」「stream 可用时强选 buffered」「跳过 status 写入」「去掉 detached 记录」「让进度增长产生 DONE」「从 raw 直接读哨兵」八个变异，运行对应单测/集成测试/`--self-test` 确认变红，立即还原；把证据记入 `verification.md`。
- [ ] T043 [US4] [blockedBy: T042] 变异还原后复跑派生单测、runner 集成测试、PD 契约与 `watch-target.sh --self-test`，复跑 quickstart S4/S5；确认判定表、退出码与自测用例集合未因修复而减少，结果记入 `verification.md` 并关闭 US4 checkpoint。

**Checkpoint**: US4 is independently functional: stream progress is visible during the run, the live log ends with the sentinel only from the terminal result, a detached runner survives the parent exit, and the buffered fallback never fabricates completion.

---

## Phase 7: User Story 5 - 安全不变量、自应用与分发 (Priority: P2)

**Goal**: Deliver the four mechanisms through the existing skill, docs page, mirrors, contract tests and fixtures without weakening confirmation gates, independent verification, stall handling, or default full-chain behavior; record the self-application exclusion and repair the two pre-existing baseline anomalies mechanism-side.

**Independent Test**: Inspect SKILL.md, the docs page, the mirror pair, the existing and new contract tests, the feature registry, and the quickstart trace; compare the test failure-name set to the frozen baseline.

### Implementation for User Story 5

- [ ] T044 [US5] [blockedBy: T043] 在 `skills/external/sdd-loop-driver/SKILL.md` 的 `## Discipline Defaults` 与 `## References` 之间新增 H2 `Efficiency Optimizations（运行效率优化）`（四项机制摘要 + 指向 `references/efficiency-model.md` 的单一 owner 指针 + 新脚本清单，不复述细节），并同步更新 `tests/contract/test_sdd_loop_driver_skill.py` 的 `PINNED_H2_SECTIONS`；在测试文件内记录「C-3 有意更新」的理由与日期。`CLI Capability Profiles` 节由 Feature 064 拥有且已在该集合中：MUST NOT 删除、复制、改写或在其内添加 063 内容；C-3 只新增 `Efficiency Optimizations` 一节。
- [ ] T045 [US5] [blockedBy: T044] 更新 `tests/contract/test_sdd_loop_driver_skill.py` 的 C-4 断言：把 runner 派生的 `sed` 断言替换为 `stage-runner.sh` 断言，保留 `nohup`、heartbeat、阶段链与收尾断言；在测试文件内记录「C-4 有意更新」的理由（单点可测试、消除每阶段副本漂移）与日期，禁止静默删除。
- [ ] T046 [US5] [blockedBy: T035,T045] 在 `tests/contract/test_sdd_loop_driver_efficiency.py` 增加 DI-01…DI-09 测试函数（`test_di_01_confirmation_gates_unchanged` … `test_di_09_orchestration_layer_only`）与覆盖 meta-test：逐个读取五份契约的 `FL/TB/PC/PD/DI` 条款 id，断言每个 id 都有对应的 `test_<prefix-lower>_<nn>_...` 测试函数（共 50 条），并钉住确认门、独立校验、卡死处置、质量门、交付面/镜像、自应用、向后兼容与编排层优先；运行该文件转绿并把结果记入 `verification.md`。
- [ ] T047 [US5] [blockedBy: T039] 更新 `docs/reference/skills/sdd-loop-driver.md`：新增四项优化的用户文档段（快车道与准入、两槽位预算与定向证据、plan 只小修约束、stream-json 进度与 nohup 双拓扑），披露日志形态变化（新增 raw stream 与 live log；不支持时降级并记 `progress=degraded`）与「不改变完成判定」，保留既有双拓扑/可移植/投递/目标项目内容，并避免「运行时必读」措辞。
- [ ] T048 [US5] [blockedBy: T044,T045,T046,T047] 运行 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 与 `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` 确认本对字节一致；运行 `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` 确认 exit 0，再运行 `python3 scripts/python/sync-mirrors.py --check --only skills/external`（比本对选择器宽一级）并对照 `research.md` B-2 冻结清单（plan 期 68 DIFF / 12 目录、本对 3；2026-10-20 合并 064 后实测 62 DIFF / 12 目录、本对 0）记录：本对 0 DIFF、全部镜像对零 NEW drift；其余目录的既有 DIFF 作为已披露基线例外保留、不得扩大（不得声称全局零漂移，I-04）；`references/cli/` 由 064 拥有，本任务只验证其字节一致，不得修改内容；运行 `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` 确认 74 units 零漂移；运行 `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_cli_profiles.py -q` 确认 064 的仓库级唯一-owner 守卫 `test_clp_17_no_063_duplicate_owner` 为绿（063 不得保留第二份 CLI-profile 契约/档案测试/README/同 unit Probe Object）；全部结果记入 `verification.md`。
- [ ] T049 [US5] [blockedBy: T046,T048] 运行 `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py tests/contract/test_sdd_loop_driver_efficiency.py -q`：既有 23 个测试函数保持全绿（C-12/C-18 镜像漂移在合并 064 后已关闭，T012/T048 维持零 drift；C-3/C-4 为有意更新），新增效率契约与覆盖 meta-test 全绿；把通过输出与两份契约的条款覆盖数（50/50）记入 `verification.md`。
- [ ] T050 [US5] [blockedBy: T049] 按 `.specify/shared/workflow/feature-integration.md` 更新 `.specify/memory/features/058.md` 的 Latest Review/Status Tracking（追加 063 实现记录，并补记此前缺失的 **063 checklist 阶段记录**——`checklists/efficiency.md` 已落盘（31 pass / 8 not pass，8 项供 analyze 门处置），该记录缺口即 F-01 治理纠正，不改状态）与 `.specify/memory/features.md` 的 058 行 Last Updated 注记；确认索引 `Total Features` 不变、未新建 Feature、未回退状态（保持 `Implemented`）。
- [ ] T051 [US5] [blockedBy: T000,T041,T050] 录制 quickstart S7 的 dry-run 编排决策 trace（不启动嵌套驱动）：用中型夹具逐决策记录「入口携带 `fast-lane=opt-in` → tasks U4 通过 → admission-check 录取 → 跳过 checklist → analyze → implement 基线 → review → 收口 → 合并」与一个未携带字面量的完整链对照，记录每步的实际脚本输出与预期阶段序列；同一收口步骤重放 SC-010 行为基线——确认 T001 的 [[STR-007]] 已在实现首个行为面提交前由 `driver-stall-fixture.py --record` 录制，调用同一夹具 `--replay --baseline .specify/specs/063-sdd-loop-efficiency/notes/stall-behavior-baseline.json --initial-retries 0 --out .specify/specs/063-sdd-loop-efficiency/notes/stall-behavior-baseline-final.json` 在当前树重放三类场景，归一化剔除时间戳、PID、绝对路径与耗时后逐字段比较（含 `exit_code` 的 `watcher`/`runner` 子字段），零差异为通过（SB-1…SB-5；禁止判定表转录/硬编码期望值/基线回填；录制/重放不是全量测试运行、不消耗槽位）；随后执行 driver-stall 变异演练——在夹具副本上逐一施加「把 `initial_retries` 改为非 0」「从场景→期望值表转录字段」「翻转下一阶段派发/先写后动顺序」三个变异，每次以同一 `--replay` 比较必须失败并立即还原，把命令、差异字段与还原确认记入 `verification.md`；把 trace 路径、要点、[[STR-007]] 比较结果与「非 CI 录制证据」标注写入 `notes/quickstart-run.md` 与 `verification.md`。
- [ ] T052 [US5] [blockedBy: T048,T049,T050,T051] 收口汇总与最终核验：核对 `notes/red-first-evidence.md` 覆盖全部新脚本、watcher 扩展与 T000 驱动侧卡死夹具、`verification.md` 记录七个变异**目标组 / 24 个变异应用**（T014 5 + T023 5 + T031 3 + T042 8 + T051 3）及还原、SC-001…SC-013 逐条状态与证据类别（自动/录制 trace/驱动收口）、24 项交付路径存在（含 T000 创建的 `driver-stall-fixture.py`）；核验 SC-010 的 [[STR-007]] 在实现首个行为面提交前由 `driver-stall-fixture.py --record` 录制、收口用同一夹具以 `initial_retries=0` 重放并对 `exit_code={watcher,runner}` 逐字段零差异（SB-1…SB-5），且名称级测试失败基线只用于 SC-012；核验 E4 `rebaseline_events[]` 与最新 `approved_baseline_commit`（若 requirements 在门内变更）且 U4 分类使用最新锚点；确认审计输出 `stages=N complete=N`、docs-only 阶段按缩减字段集判完整且不报 `unknown`、每适用阶段恰一条 `stage-status` 行；确认准入计数只用窄模式、宽模式仅用于仓库记账；在 `verification.md` 记录 G-01 六个 Edge Case 的命名测试/结构化证据——多线隔离（T016）、`detached=no` 未脱离风险（T034/T037）、准入记录缺失收尾审计（T016/T019）、定向集空集升级（T016/T019）、多处小修按最终 diff 判定（T025/T027）、plan 完成后重入恢复 active（T026/T028）；确认 F-01 的 063 checklist 阶段记录已由 T050 补入 058 详情；运行 `python3 .specify/scripts/python/validate-requirements.py .specify/specs/063-sdd-loop-efficiency/requirements.md` 与 `python3 .specify/scripts/python/validate-tasks.py .specify/specs/063-sdd-loop-efficiency/tasks.md` 确认 exit 0；复跑 GATE-1 的定向测试集；确认 E2 台账位于状态脊围栏、baseline 对 closure 审计可见（`audit-test-budget.py --spine "$STATE_SPINE" --stage-check closure` 报 `baseline:1 closure:1`）、implement 只消耗 baseline 槽位、closure 仍为驱动在 review 后的职责；确认 063 自身无快车道记录且 checklist/analyze 产物在位（review 由驱动在 implement 后执行）；确认 064 的唯一-owner 守卫为绿且 063 无 CLI-profile 任务/契约/测试残留；把全部结论写入 `verification.md`。

**Checkpoint**: US5 is independently verifiable: the skill/docs/mirror/test surfaces are delivered, the two baseline anomalies are repaired mechanism-side, the feature registry remains `Implemented`, and the self-application exclusion is evidenced.

---

## Feature Integration Review

- 2026-10-20, tasks phase: `.specify/memory/features.md` registers 61 features; Feature 058 exists with status `Implemented`; spec 063 is bound to 058 as an evolutionary slice; `.specify/memory/features/058.md` exists. The task breakdown exposes **no new Feature** and invalidates no existing Feature: the five new scripts and the watcher extension are all within 058's existing `skills/external/sdd-loop-driver/` surface. Status stays `Implemented`; T050 appends the implementation-stage record. The tasks-stage record is appended to the feature detail and index by the `/speckit.tasks` lifecycle itself.
- 2026-10-20, tasks-repair (analyze gate, round 1): tasks.md was reconciled with the plan-repair `f0c18e03` and the analyze findings (I-05 baseline ledger location, I-07 mutation wording, F-01 058 checklist-stage record routed to T050, G-01 six edge-case mappings, I-01/FL-03(a) regex owner reference). Only `tasks.md` was modified; no plan-owned artifact was touched and no new Feature was created. Status stays `Implemented`. F-01 remains visible as a governance item until T050 executes.
- 2026-10-20, tasks-repair-2 (CLI-profile overlap convergence): 063's provisional CLI-profile scope was adjudicated to Feature 064 per `.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md`. No US6 task is added; CLI-profile contracts, archives, tests and Probe Object stay with 064. `tasks.md` now carries the 064 boundary in T044/T048/T052, the post-merge counts (43 FR / 13 SC / 50 clauses including PC-11 / 24 deliverables / 7 scenarios), and the U-01R/N propagation items. Plan-owned edits carry `PLAN-EDIT:` declarations in plan.md § Plan Repair Record 第 3 轮. Task rows remained T001…T052 (52) at that round; tasks-repair-3 adds T000 — see D-T10. Status stays `Implemented`. F-01 remains visible until T050 executes.
- 2026-10-20, tasks-repair-3 (analyze-rerun-2 focused repair): U-01R closed by making `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py` the single execution body (new T000 author row; T001 record and T051 replay call the same fixture with `initial_retries=0` and `exit_code={watcher,runner}`; decision-table and trace-only wording removed), the mutation plan recomputed to plan.md's seven target groups / 24 applications, and the N-01R/N-02R/N-03R/N-04/N-05 propagation landed in T002/T008/T010/T011/T013/T016/T019/T020/T022/T026/T028/T031/T039/T051/T052. Task rows are T000 + T001…T052 (53); no existing ID was renumbered. Only `tasks.md` plus the plan-owned pointer/count corrections declared in plan.md § Plan Repair Record 第 4 轮 are modified. Status stays `Implemented`. F-01 remains routed to T050/DoD-10.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependency; T002 is the single implement-start full-suite slot.
- **Foundational (Phase 2)**: depends on Setup; blocks every story's red-first tests.
- **US1 (Phase 3)**: depends on Foundational; creates the owner document and the first contract-test file.
- **US2 (Phase 4)**: depends on US1 for the shared owner document and contract-test file; its behavior is independently testable.
- **US3 (Phase 5)**: depends on US2 for the shared owner/contract files; its behavior is independently testable.
- **US4 (Phase 6)**: depends on US3 for the shared owner/contract files; it has no behavioral dependency on US1/US2/US3 and is also P1.
- **US5 (Phase 7)**: depends on US1–US4 final content; distributes, documents and pins the whole feature.
- **Polish**: there is no separate Polish phase; cross-cutting closure is T052 (verification) because the driver-owned closure slot is outside implement.

### User Story Dependencies

- **US1 (P1)**: MVP slice; no dependency on US2–US5 behavior.
- **US2 (P1)**: independent behavior; serialized only by the shared owner/contract files.
- **US3 (P2)**: independent behavior; serialized only by the shared owner/contract files.
- **US4 (P1)**: independent behavior; serialized only by the shared owner/contract files.
- **US5 (P2)**: requires the final SKILL/docs/scripts from US1–US4; its independent test inspects distribution, mirrors and invariants.

### Within Each User Story

- Red tests first; scripts and manual sections next; mirror parity after the skill face is final; behavior verification next; mutation drill after green; post-mutation re-run closes the story.
- Never run a second full suite inside implement; every intermediate verification uses the targeted set selected by the story's changed paths and deliverable contract tests.
- A verification row that writes `verification.md` or `notes/quickstart-run.md` is never `[P]` with another row writing the same sink.

### Parallel Opportunities

- Foundational T003/T004/T005/T006 write disjoint fixture paths and MAY run in parallel.
- All story phases serialize on `references/efficiency-model.md`, `references/dispatch-recipes.md`, `references/stage-prompts.md`, `tests/contract/test_sdd_loop_driver_efficiency.py`, `verification.md`, and `notes/quickstart-run.md`; with multiple writers, partition by file first, then dispatch stories in parallel.
- Inside US5, T047 (docs page) writes only `docs/reference/skills/sdd-loop-driver.md` and could run alongside a test-authoring row, but the phase intentionally keeps the sequence because `verification.md` is the shared sink.

---

## Implementation Strategy

### MVP First

**MVP scope**: **US1 only** (plus Setup and Foundational). US1 is the throughput win that can be admitted and refused on deterministic evidence and is independently testable with the medium/large fixtures. US2 and US4 are also P1 and are required before the feature is complete, but each is a separate independently testable increment; US2 and US4 follow the MVP rather than expanding it.

1. Complete Phase 1 (Setup) and Phase 2 (Foundational).
2. Complete US1 (Phase 3).
3. **STOP and VALIDATE**: run the US1 independent test and record the MVP checkpoint.
4. Continue with US2 → US3 → US4 → US5.

### Incremental Delivery

1. Setup + Foundational → baselines and fixtures ready.
2. US1 → fast lane admitted/refused; demo the MVP.
3. US2 → two-slot budget and name-level regression proof.
4. US3 → plan minor-fix constraint and U4 classification.
5. US4 → stream progress and detached survival.
6. US5 → distribution, docs, mirrors, invariants, registry.

### Parallel Team Strategy

- The shared owner documents and the shared contract-test file are the serialization point; assign one writer per file at a time.
- Foundational fixtures can be split across four writers.
- Distribution work (SKILL.md, docs page, existing-contract updates) can be split after US4 completes.

---

## Notes

### Clause partition and test naming

| Contract | Clauses | Claiming story | Test function prefix |
|----------|---------|----------------|----------------------|
| `contracts/fast-lane.md` | FL-01…FL-10 | US1 (T009) | `test_fl_01…test_fl_10` |
| `contracts/test-budget.md` | TB-01…TB-10 | US2 (T018) | `test_tb_01…test_tb_10` |
| `contracts/plan-constraint.md` | PC-01…PC-11 | US3 (T026) | `test_pc_01…test_pc_11` |
| `contracts/progress-decoupling.md` | PD-01…PD-10 | US4 (T035) | `test_pd_01…test_pd_10` |
| `contracts/delivery-and-invariants.md` | DI-01…DI-09 | US5 (T046) | `test_di_01…test_di_09` |

Total: 50 clauses. T046 adds the coverage meta-test that asserts every clause id has a named test function; T009/T018/T026/T035 create and extend the same contract-test file, so those rows serialize.

### Assumptions and decisions

- **D-T1 (no `[green:]` tags)**: the five contracts declare `FL/TB/PC/PD/DI` clause ids, not the repository's machine clause form `C-<number>`. Renaming 50 clauses would be a substantive contract change outside the tasks stage; the optional `[green:]` tag is therefore omitted. Coverage is pinned by one named test per clause plus the T046 meta-test and each contract's traceability table.
- **D-T2 (story order)**: phases follow requirement order US1→US2→US3→US4→US5 rather than strict P1-first. All four optimization stories append to the same owner document and the same stage-prompts/dispatch-recipes files; numeric order keeps the owner sections in authoring order and avoids placeholder markers. US4 is P1 and has no behavioral dependency on US2/US3; a multi-writer team can partition the shared files and run it in parallel.
- **D-T3 (closure ownership)**: the second full-suite slot is owned by the driver after `review`, per FR-011 (`review` 通过之后、合并之前). It is intentionally **not** an implement task: scheduling it inside implement would make it stale before review and would violate the stage order. T002 consumes the only implement-side full-suite slot and writes it as an E2 row into the line state spine; T022/T052 record the obligation; the driver appends the `closure` row to the **same** spine fence, so the baseline is visible to the closure audit without any cross-file merge (I-05). If an implementation ever leaves the baseline only in `test-evidence/implement.jsonl` (a transport carrier, never the ledger or audit source; remote `SPINE_WRITE_MODE=transport` may carry E2-shaped rows there), the driver MUST merge that row into the spine E2 fence and record `merge_source`/`merged_at` before closure; a closure audit that cannot see a baseline MUST not pass.
- **D-T4 (S7 evidence)**: `quickstart.md` S7 is a recorded dry-run decision trace, not a nested driver launch. The skill's Hard Requirement 6 forbids nested driving, so T051 records the decision sequence and script outputs without launching a driver inside a stage subagent; `verification.md` labels it as non-CI evidence.
- **D-T5 (baseline anomalies)**: the watcher self-test platform/timing failures are repaired mechanism-side in `watch-target.sh` (portable check or explicit platform skip, never deletion); the sdd-loop-driver mirror pair is verified with `sync-mirrors.py --check --only skills/external/sdd-loop-driver`. **Post-merge reading (2026-10-20)**: after 064 was merged, the owned pair is already 0 DIFF and the wider `--only skills/external` check reports 62 DIFF across 12 directories (plan-time frozen reading: 68 DIFF / 12 directories / 3 in the owned pair; see `research.md` B-2). The zero-NEW-drift criterion is unchanged and is evaluated against the frozen path list; `references/cli/` belongs to 064 and is only verified byte-identical, never modified. **Resolved (I-06)**: plan.md originally phrased the write selector as `--only skills/external` (a prefix that would also write the other 11 skills); plan-repair `f0c18e03` corrected it to `--only skills/external/sdd-loop-driver`, matching T012/T021/T029/T040/T048. No plan artifact is modified by this tasks-repair except the CLI-profile convergence carrying its own `PLAN-EDIT:` declarations.
- **D-T6 (intentional existing-assertion updates)**: C-3 (`PINNED_H2_SECTIONS`) adds only `Efficiency Optimizations`; the `CLI Capability Profiles` section is owned by 064 and already pinned — it MUST NOT be deleted, copied or rewritten. C-4 (`sed` → `stage-runner.sh`) is the only other existing assertion intentionally changed. Both changes carry an in-file reason and date; no other assertion is weakened.
- **D-T7 (self-application)**: 063's own run is full-chain. No fast-lane admission record is produced for it; checklist/analyze artifacts exist; review is executed by the driver after implement. T052 records that boundary honestly.
- **D-T8 (tasks-repair round 1)**: this repair addresses the tasks-owned analyze findings — I-05 (baseline E2 into the state-spine fence; GATE-8/T002/T019/T022/T052/Notes realigned), I-07 (mutation plan; corrected to plan's seven target groups / 24 applications in tasks-repair-3 — see D-T10), F-01 (the 063 checklist-stage record is routed to T050/DoD-10 as a governance correction, never a status rollback), G-01 (six edge cases mapped to named tests: T016/T019/T025/T026/T034/T037/T052), and the tasks-side propagation of plan-repair `f0c18e03` (SC-010 [[STR-007]]/SB-1…SB-4 as then recorded — SB-5 added in tasks-repair-3, see D-T10; `approved_baseline_commit`, event→derived-line latency, [[STR-008]] skipped-stage semantics, B-2 zero-NEW-drift, `lines.manifest` syntax owner, `targeted-set-v1`, FL-03(a) exact regex). Only `tasks.md` is modified; no plan-owned artifact is touched. Assumption: `$STATE_SPINE` is the path the driver records in the U0 entry declaration; if implement does not receive it, T002 halts with `ANOMALY:` rather than creating a second ledger.
- **D-T9 (tasks-repair-2, CLI-profile overlap)**: Feature 064 is the sole owner of CLI capability profiles; 063 adds no US6 task, no CLI-profile contract/test/archive/Probe task. T044 only adds `Efficiency Optimizations` and must not touch the 064-owned `CLI Capability Profiles` H2; T048 verifies the 064-owned `references/cli/` by byte equality only and runs the `test_clp_17_no_063_duplicate_owner` guard; T052 confirms no CLI-profile residue in 063. Counts after convergence: 43 FR / 13 SC / 50 clauses (PC-11 included) / 24 deliverables / 7 quickstart scenarios / 41 E rules; task rows remained T001…T052 (52) at that round — tasks-repair-3 adds T000 (fixture author), see D-T10.
- **D-T10 (tasks-repair-3, analyze-rerun-2)**: closes U-01R by making `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py` the single execution body — T000 authors it (record/replay/self-test), T001 records the [[STR-007]] baseline with `--record`, T051 replays with the same fixture at `initial_retries=0` and `exit_code={watcher,runner}`, then runs the three driver-stall mutations; all decision-table-transcription and trace-only wording is removed. The mutation plan is recomputed to plan.md's seven target groups / 24 applications (admission 5 / derive 3 / budget 5 / plan-changes 3 / runner 3 / watcher 2 / driver-stall 3). N-01R lands in T002/T011/T020/T028/T039 (stage-prompt skeleton `STATE_SPINE_PATH`/`EVIDENCE_DIR`/`SPINE_WRITE_MODE`; transport vs ledger wording), N-02R in T026/T028/T052 (initial `approved_baseline_commit`, PC-11 `rebaseline_events[]`, latest anchor), N-03R in T016/T019/T020/T022/T052 (docs-only six-field reduced set, unique `stage-status` row, `stages=N complete=N`), N-04 in T013 (no "first creation" claim; T002 creates `verification.md`), and the N-05 narrow/wide count boundary in T008/T010/T013/T052. Plan-owned corrections N-07/L-01/L-02 are declared in plan.md § Plan Repair Record 第 4 轮. **Assumption**: the new fixture-author row uses ID `T000` (accepted by `validate-tasks.py`) so every existing T001…T052 reference stays stable; the driver-stall mutation drill is folded into T051 rather than adding a second row. `requirements.md` pointer prefixes remain outside this round's allowed edit surface (tasks.md + plan-owned only); F-01 stays routed to T050/DoD-10 and never blocks the gate.

### Measured premises (commands actually run at generation time, 2026-10-20)

- FR definitions: `grep -cE '^\- \*\*FR-[0-9]{3}\*\*:' requirements.md` → `43` (trap: counting every `FR-` mention also matches citation rows and SC text; the anchored definition-line pattern is the contract).
- Success criteria: `grep -cE '^\- \*\*SC-[0-9]{3}\*\*:' requirements.md` → `13`.
- Data-model validation rules: `grep -cE '^- V-E[0-9]+-[0-9]+' data-model.md` → `41` (tasks-repair-2 removed the two CLI-specific E rules; trap: the ASCII-colon form `^- V-E[0-9]+-[0-9]+:` returns `0` because the file uses a full-width `：`).
- Contract clauses: FL `10`, TB `10`, PC `11`, PD `10`, DI `9`; total `50` (`grep -cE '^- \*\*(FL|TB|PC|PD|DI)-[0-9]{2}' contracts/*.md`). CLI-profile clauses are owned by 064 and are not counted here.
- Deliverables: `awk` over the first fenced block in `feature-ref.md` → `24`.
- Existing contract baseline: plan-time `2 failed, 21 passed` (C-12/C-18 mirror drift); post-merge 2026-10-20 `23 passed, 0 failed`.
- Watcher self-test baseline: plan-time `12 passed, 4 failed`; post-merge 2026-10-20 `28 passed, 0 failed`.
- Mirror baseline: plan-time `python3 scripts/python/sync-mirrors.py --check --only skills/external` → exit `2`, `68 DIFF` across 12 skill directories, of which `3` were in `sdd-loop-driver`; post-merge 2026-10-20 → `62 DIFF` across 12 directories, `0` in the owned pair.
- Compile face: `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` → `74 units, zero drift`, exit `0`.
- Requirements validator: `python3 .specify/scripts/python/validate-requirements.py .../requirements.md` → `343 lines, 56 definition rows, 8 shared strings, 0 error(s), 0 warning(s)` (tasks-repair-2 re-measure after the CLI-profile convergence; plan-repair-2's provisional `382 / 65 / 10` is a dated prior reading, not current).
- Interpreter probes: `python3 --version` → `3.9.6`; `python --version` → `3.14.6`; `python -m pytest --version` → `pytest 9.1.1`; direct `python3 -m pytest` is unavailable.
- Task rows: `grep -cE '^- \[[ xX>~]\] T[0-9]{3}' .specify/specs/063-sdd-loop-efficiency/tasks.md` → `53` after tasks-repair-3 (`T000` fixture author plus `T001…T052`; no existing ID was renumbered).
- Deliverable-path initial state: of the 24 paths in `feature-ref.md`, `15` are new and absent (owner doc, 5 new scripts, 7 new test files, fixtures dir, driver-stall-fixture), `9` are update targets and present (SKILL.md, 3 existing references, watch-target.sh, docs page, existing contract test, 058 detail and index).

### Runtime-evidence landing points

- `.specify/specs/063-sdd-loop-efficiency/notes/pre-change-measurements.md` — T001/T002 measured values, commands and dates.
- `.specify/specs/063-sdd-loop-efficiency/notes/baseline-failed-tests.txt` — T002 implement-start full-suite name list (the single `baseline` slot).
- `.specify/specs/063-sdd-loop-efficiency/notes/stall-behavior-baseline.json` — T001 recording of the SC-010 behavior baseline via `driver-stall-fixture.py` (T000) ([[STR-007]], `base_commit`, `initial_retries=0`, `exit_code={watcher,runner}`, three scenario tuples); `notes/stall-behavior-baseline-final.json` — T051 normalized replay for field-by-field comparison (SB-3).
- `.specify/specs/063-sdd-loop-efficiency/notes/baseline-mirror-check.txt`, `notes/baseline-contract-sdd-loop-driver.txt`, `notes/baseline-watch-selftest.txt` — T001 raw baseline outputs.
- `.specify/specs/063-sdd-loop-efficiency/notes/red-first-evidence.md` — T000/T008/T009/T016/T017/T018/T025/T026/T033/T034/T035 red commands, real output and exit status.
- `.specify/specs/063-sdd-loop-efficiency/notes/quickstart-run.md` — T013/T022/T030/T041/T051 quickstart runs, SC-010 replay and teardown.
- `.specify/specs/063-sdd-loop-efficiency/verification.md` — T013 onward behavior/structure/SC evidence; T052 final summary.
- **Line state spine (`$STATE_SPINE`, path recorded in the U0 entry declaration)** — the E2 `<!-- test-budget:begin/end -->` JSONL fence: T002 writes the `baseline` row; the driver appends the `closure` row after review. This spine is the sole ledger authority for `audit-test-budget.py` (I-05).
- `.specify/specs/063-sdd-loop-efficiency/test-evidence/implement.jsonl` — optional E3-shaped reference copy only (at most one legal JSON line per run); it is never the ledger and never the audit source.

### Budget closure ownership

- This feature's own run has exactly two full-suite slots: `baseline` (T002, inside implement, written to the line state spine E2 fence) and `closure` (driver-owned after review, before merge, appended to the same spine).
- Implement MUST NOT run the closure full suite and MUST NOT run any other full suite. Intermediate stages and `review` use the targeted set selected by the fixed `targeted-set-v1` program in `references/efficiency-model.md` §2 (owner: `contracts/test-budget.md` TB-05).
- Driver closure procedure (I-05): (1) before running closure, `audit-test-budget.py --spine "$STATE_SPINE" --spec-dir .specify/specs/063-sdd-loop-efficiency --stage-check implement` MUST show the `baseline` row; if it does not and an E3 copy exists in `test-evidence/implement.jsonl`, merge that row into the spine fence and record the merge source — never audit without a baseline; (2) run the closure full suite with `--names-out final-failed.txt`, compute `comm -13 baseline final`, append the `closure` E2 row to the same spine; (3) re-run the audit with `--stage-check closure` and record `baseline:1 closure:1`, exceptions and unknown in the wrap-up summary.
- If the driver's closure finds new failures and a fix requires rerunning the same suite, the rerun is recorded as `in-slot-rerun` with trigger and evidence; it does not open a third slot.
- Any out-of-slot full run must be an `out-of-slot-exception` with a reason and evidence pointer, and is listed in the final wrap-up summary.

### Pre-existing observations (not repaired by this feature)

- The other 11 skill directories' mirror drift (65 of the 68 DIFFs in the `research.md` B-2 baseline, across 12 directories; the owned pair accounts for 3) is pre-existing and outside this feature's surface; T048 records zero NEW drift rather than claiming a global zero.
- The 2 existing contract failures (C-12/C-18) are repaired by this feature's scoped mirror sync, not waived.
- The 4 watcher self-test failures are repaired mechanism-side in `watch-target.sh`; Linux-only branches may be platform-skipped on macOS, and the skip is named in the self-test output.
