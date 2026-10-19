# Tasks: sdd-loop-driver 运行效率优化（SDD Loop Efficiency）

**Requirement ID**: 063 (from branch `063-sdd-loop-efficiency`)
**Requirement Key**: `063-sdd-loop-efficiency`
**Related Feature**: Feature 058 无人值守 SDD 循环驱动机制（演化特性；状态保持 `Implemented`，不回退）
**Input**: Design documents from `.specify/specs/063-sdd-loop-efficiency/` — plan.md, requirements.md, research.md, data-model.md, contracts/ ×5, quickstart.md, feature-ref.md, checklists/requirements.md, notes/source-requirement.md
**Prerequisites**: plan.md (required), requirements.md (required), research.md, data-model.md, contracts/, quickstart.md, feature-ref.md

**Tests Mode**: ON — Constitution Principle IV “Test-First & Contract-Driven Implementation” is test-mandating. This feature is **not** template-only: it ships five executable scripts plus one extended watcher, so unit + integration tests are mandatory; the 49 contract clauses are pinned by structural contract tests; the LLM-orchestrated stage sequence cannot be replayed in CI and is evidenced by the recorded dry-run trace required by plan.md § Complexity Tracking, never disguised as an automated test.

**Tests**: Red-first for every new script and the watcher extension (`notes/red-first-evidence.md` records the command, real output, and exit status of each red run). Mutation drills from plan.md § Verification & Mutation Plan are mandatory; a mutation that does not turn its named test red means that test is not defending the behavior. Tests Mode ON also requires the two full-suite slots of FR-011 to be honored by this feature's own run: exactly one baseline inside implement (T002) and one driver-owned closure after review (not an implement task; see § Notes → Budget closure ownership).

**Organization**: This is a doc+code hybrid (skill manuals + stdlib scripts). Within each user story the order is: red tests → script/manual implementation → mirror parity → green behavior verification → mutation drill → post-mutation re-run. All four optimization stories append to the same owner document (`references/efficiency-model.md`) and the same `dispatch-recipes.md` / `stage-prompts.md`, so their phases serialize on those files; only fixture authoring (Foundational) is parallel. Story phases are numbered in requirement order (US1→US2→US3→US4→US5) to keep the owner-document sections in authoring order; US4 is also P1 and has no behavioral dependency on US2/US3 (see § Notes → Assumptions D-T2).

**Plan constraint**: `plan` U4 has passed (commit 5ab8a5e7). This tasks stage creates only `tasks.md` and does not modify any plan-owned artifact (`plan.md`, `data-model.md`, `contracts/`, `quickstart.md`, `research.md`, `feature-ref.md`), so no `PLAN-EDIT:` declaration is required. Any later implement-stage change to a plan-owned artifact MUST carry a `PLAN-EDIT:` line or halt with `ANOMALY:`.

## Definition of Done (DoD)

- DoD-1: Every task row is `[X]`, or `[~]` with a recorded deferral reason in `verification.md` (`deferred_tasks=`); zero `[ ]` / `[>]` rows remain.
- DoD-2: All 23 deliverables listed in `feature-ref.md` § 交付面清单 exist at their canonical paths and are evidenced in `verification.md`.
- DoD-3: All 49 contract clauses (FL-01…FL-10, TB-01…TB-10, PC-01…PC-10, PD-01…PD-10, DI-01…DI-09) are covered by their named test functions, and the coverage meta-test in `tests/contract/test_sdd_loop_driver_efficiency.py` passes.
- DoD-4: `notes/red-first-evidence.md` records every red-first run, and `verification.md` records all six mutation drills from plan.md with restore confirmation.
- DoD-5: `watch-target.sh --self-test` exits 0 with the four pre-existing failures repaired mechanism-side (portable check or explicit platform skip, never deletion), and the four new stream/detach cases pass.
- DoD-6: The `skills/external/sdd-loop-driver` ↔ `.specify/skills/sdd-loop-driver` pair is byte-identical, zero NEW drift is shown relative to the frozen 68-DIFF baseline, and `probe-utils.py --action compile-embeds --check` reports zero drift.
- DoD-7: The implement run consumed exactly one full-suite slot (`baseline`); no second full suite ran inside implement; targeted test evidence fields are complete; the closure slot is recorded as driver-owned after review.
- DoD-8: `verification.md` lists SC-001…SC-013 with a status and evidence class (automated / recorded trace / driver closure); no SC is claimed as automated when its evidence is only the recorded trace.
- DoD-9: Quickstart S1–S7 are executed; S7 is a recorded dry-run decision trace (no nested driver launch) and its non-CI status is stated.
- DoD-10: Feature 058 detail and index are updated with the 063 implementation record; status remains `Implemented`.

**DoD Status**: pending

## Completion Gate

- GATE-1: Targeted test set green — check: `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py tests/contract/test_sdd_loop_driver_efficiency.py tests/unit/test_admission_check.py tests/unit/test_derive_live_log.py tests/unit/test_audit_test_budget.py tests/unit/test_audit_plan_changes.py tests/integration/test_sdd_loop_efficiency_runner.py tests/integration/test_sdd_loop_efficiency_regression.py -q` exits 0.
- GATE-2: Watcher self-test green — check: `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` exits 0 and reports 0 failed (platform skips, if any, are named).
- GATE-3: Mirror pair byte-identical and zero NEW drift — check: `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` exits 0; `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` exits 0.
- GATE-4: Compile face untouched — check: `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` exits 0 with zero drift.
- GATE-5: Structural validators — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/063-sdd-loop-efficiency/tasks.md` and `python3 .specify/scripts/python/validate-requirements.py .specify/specs/063-sdd-loop-efficiency/requirements.md` both exit 0.
- GATE-6: No open/claimed rows — check: `grep -cE '^- \[[ >]\]' .specify/specs/063-sdd-loop-efficiency/tasks.md` returns 0.
- GATE-7: 23 deliverables present — check: every path in `feature-ref.md` § 交付面清单 passes `test -e`.
- GATE-8: Budget slot discipline — check: `grep -cE '"slot"[[:space:]]*:[[:space:]]*"baseline"' .specify/specs/063-sdd-loop-efficiency/test-evidence/implement.jsonl` returns 1 and `grep -cE '"slot"[[:space:]]*:[[:space:]]*"closure"' .specify/specs/063-sdd-loop-efficiency/test-evidence/implement.jsonl` returns 0 (the closure is executed by the driver after review, not by implement).

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
- No `[green:]` tags in this file: the five contracts use `FL/TB/PC/PD/DI` clause ids, which the repository's machine clause form (`C-<number>`) does not recognize; the tag is optional, and renaming 49 clauses would be a substantive contract change outside this stage. Coverage is instead pinned by one named test function per clause plus the coverage meta-test (T046) and the per-contract traceability tables.

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

**Purpose**: Freeze the pre-change side of every diff premise and record the implement-start full-suite baseline before any artifact is written.

- [ ] T001 记录改前侧测量并保存原始基线输出到 `.specify/specs/063-sdd-loop-efficiency/notes/pre-change-measurements.md`：实跑并粘贴 `python3 scripts/python/sync-mirrors.py --check --only skills/external`（预期 exit 2、68 DIFF、其中 sdd-loop-driver 3 文件）、`bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q`（预期 21 passed / 2 failed）、`bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test`（预期 12 passed / 4 failed）、`python3 --version` / `python --version` / `python3 .specify/scripts/python/validate-requirements.py .specify/specs/063-sdd-loop-efficiency/requirements.md`（0 error / 0 warning），并把三份原始输出分别保存为 `notes/baseline-mirror-check.txt`、`notes/baseline-contract-sdd-loop-driver.txt`、`notes/baseline-watch-selftest.txt`；同时逐项 `test -e` 记录交付面初始状态并把清单写入 `notes/pre-change-measurements.md`：14 个新路径（`references/efficiency-model.md`、5 个新脚本、1 个新契约测试文件、4 个单测、2 个集成测试、夹具目录）应不存在；9 个更新目标（`SKILL.md`、3 份既有 references、`watch-target.sh`、docs 页、既有契约测试、058 详情与索引）应存在；本任务不运行全量测试套件。
- [ ] T002 [blockedBy: T001] 执行本特性运行唯一的 implement 起点全量基线（预算槽位 `baseline`）：`bash scripts/bash/run-tests.sh --names-out .specify/specs/063-sdd-loop-efficiency/notes/baseline-failed-tests.txt`，按 E2 字段把命令、rc、passed/failed 计数、失败名单路径与证据指针完整写入 `.specify/specs/063-sdd-loop-efficiency/test-evidence/implement.jsonl`（目录不存在时先创建；`seq=1`、`slot=baseline`、`stage=implement`、`purpose=implement-start-baseline`、`trigger=scheduled`、`selection_basis=full-suite`、`baseline_compare=na`），并把同一组计数写入 `notes/pre-change-measurements.md`；implement 内不得再运行第二次全量，收口槽位由驱动在 review 后执行（见 § Notes → Budget closure ownership）。

**Checkpoint**: every later “diff against pre-change” premise has a dated baseline; the implement-start full-suite slot is consumed exactly once.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Author the shared fixtures that every story's red-first tests consume.

**⚠️ CRITICAL**: No user-story test can close until these fixtures exist.

- [ ] T003 [P] 创建中型与大型特性夹具 `tests/fixtures/sdd_loop_efficiency/medium/.specify/specs/012-medium/`（`requirements.md` 恰 12 条 `- **FR-NNN**:` 定义行、`tasks.md` 恰 25 条 `- [ ] TNNN` 任务行、`checklists/requirements.md` 全部勾选、`entry.md` 含字面量 `fast-lane=opt-in`、`lines.manifest` 恰一行 `012-medium|012-medium`、`baseline-failed.txt`、`final-failed.txt`）与 `tests/fixtures/sdd_loop_efficiency/large/.specify/specs/013-large/`（`tasks.md` 60 条任务行、其余同构）。
- [ ] T004 [P] 创建 Plan 改动夹具 `tests/fixtures/sdd_loop_efficiency/plan-repo/.specify/specs/012-medium/`：`plan.md`、`data-model.md`、`contracts/fixture-contract.md`、`quickstart.md`、`research.md`、`feature-ref.md` 六件套齐备并可由 quickstart 准备步骤 `git init` + 首次提交。
- [ ] T005 [P] 创建预算台账夹具 `tests/fixtures/sdd_loop_efficiency/state-spine-valid.md`（含 `<!-- test-budget:begin -->` / `<!-- test-budget:end -->` JSONL 围栏，`baseline` 与 `closure` 各一条，closure 的 `baseline_compare` 为 `comm -13` 名称级差集，`exception_reason` 语义完整）与 `tests/fixtures/sdd_loop_efficiency/test-evidence/analyze.jsonl`（一条字段完整的 E3 定向测试证据）。
- [ ] T006 [P] 创建 stream 事件与 stub CLI 夹具：`tests/fixtures/sdd_loop_efficiency/stream/non_terminal_sentinel.jsonl`（非终止事件正文含 `PLAN-DONE` 字样、无终止 result）、`tests/fixtures/sdd_loop_efficiency/stream/result_sentinel.jsonl`（终止 result 的 `result` 文本最后一行恰为 `PLAN-DONE`）、`tests/fixtures/sdd_loop_efficiency/stream/malformed.jsonl`（含不可解析行与无 result 的派生失败形态）、`tests/fixtures/sdd_loop_efficiency/stub-cli.sh`（支持 `--output-format stream-json` 的 `stream` 模式、`--help` 不含该旗标且直接传入时非零退出的 `no-stream` 模式、非零退出的 `fail` 模式、退出 0 但无 result 的 `no-result` 模式，并支持 `--delay N` 控制事件间隔）。
- [ ] T007 [blockedBy: T003,T004,T005,T006] 编写夹具说明 `tests/fixtures/sdd_loop_efficiency/README.md`（逐项映射 fixture → 消费测试 → 契约条款），执行 `chmod +x tests/fixtures/sdd_loop_efficiency/stub-cli.sh`，并实跑 `bash tests/fixtures/sdd_loop_efficiency/stub-cli.sh --output-format stream-json` 与 `--mode no-stream` 冒烟，把输出记入 README 的自检段。

**Checkpoint**: fixtures exist and the stub CLI emits both the stream and the no-stream shapes; all story tests can be authored red.

---

## Phase 3: User Story 1 - 中型特性快车道：显式准入与失败回退 (Priority: P1) 🎯 MVP

**Goal**: Admit a medium feature to the fast lane only on an explicit `fast-lane=opt-in` entry and seven mechanically measured criteria, skip `checklist`, keep `analyze`/`review`, and fail closed with a recorded reversion when a criterion later breaks.

**Independent Test**: Run `admission-check.py` against the medium and large fixtures and boundary variants; inspect the JSON admission record, the downstream prompt blocks, and the reversion procedure.

### Tests for User Story 1 (MANDATORY) ⚠️

- [ ] T008 [US1] Author `tests/unit/test_admission_check.py` red-first：在临时目录复制中型/大型夹具并完成 `git init` + 首次提交 + `012-medium`/`013-large` 分支，覆盖 `test_medium_fixture_admitted`（12 FR / 25 任务、七判据全 pass、`decision=fast-lane`）、`test_large_fixture_denied`（60 任务、criterion a fail、`decision=full-chain`）、`test_task_count_boundary_edges`（8/30 FR 与 10/40 任务含端点通过；7/31、9/41 拒绝）、`test_fr_count_excludes_sc_rows`（SC 行不得计入）、`test_missing_or_unparseable_tasks_fail_closed`、`test_missing_checklist_or_entry_fails_closed`、`test_sensitive_or_engine_path_rejected`、`test_multiline_or_branch_mismatch_lines_manifest_rejected`、`test_open_clarification_marker_rejected`、`test_unresolved_related_feature_rejected`、`test_exit_codes_0_1_2`；把 red 命令、真实输出与退出码记入 `.specify/specs/063-sdd-loop-efficiency/notes/red-first-evidence.md`。
- [ ] T009 [US1] [blockedBy: T008] Author `tests/contract/test_sdd_loop_driver_efficiency.py` 的 FL-01…FL-10 测试函数（`test_fl_01_opt_in_literal_pinned` … `test_fl_10_self_application_exclusion`），钉住 `fast-lane=opt-in` 字面量、七判据表、`checklist=skipped(fast-lane)`、准入记录字段、回退程序、analyze/review 不削弱、`admission-check.py` 的 CLI/退出码与脚本常量（8/30、10/40）、owner 文档落点与 063 自应用排除；在当前树先红，把 red 运行记入 `notes/red-first-evidence.md`。

### Implementation for User Story 1

- [ ] T010 [US1] [blockedBy: T008,T009] 实现 `skills/external/sdd-loop-driver/scripts/admission-check.py`：参数 `--project --base-ref --requirements --tasks --checklists --entry-evidence --lines-manifest --expected-branch [--json-out]`；七判据 (a)–(g) 全部机械判定（FR 只数 `^- **FR-NNN**:` 定义行、任务只数 `^- [state] TNNN` 行、区间常量 8/30 与 10/40 与 FR-003 冻结基线一致、宪法零改动、引擎/模板/技能/依赖清单与安全敏感面保守超集扫描、单线 manifest 恰一行且分支匹配、clarify 完成且活动标记为零、Related Feature 注册可解析、需求质量清单全绿）；任何解析失败或输入缺失 fail-closed；退出码 0=可录取 / 1=拒绝 / 2=输入或解析错误；仅 Python 标准库且 ≥3.8 兼容。
- [ ] T011 [US1] [blockedBy: T010] Author `skills/external/sdd-loop-driver/references/efficiency-model.md` §1（快车道唯一 owner：入口 `fast-lane=opt-in`、裁决点、七判据、E1 准入记录形态、`checklist=skipped(fast-lane)` 下游发布、fail-closed 回退、analyze/review 不变量），并在 `references/dispatch-recipes.md` Recipe 4 写入 `tasks` U4 后、`checklist` 派发前的裁决点与回退序列，在 `references/stage-prompts.md` 写入 implement/review 条件块（跳过标记与准入证据指针，不把缺失 checklist 当缺失必需门）。
- [ ] T012 [US1] [blockedBy: T011] 运行 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 同步 `skills/external/sdd-loop-driver/` → `.specify/skills/sdd-loop-driver/`（含既有 3 文件漂移的机制侧修复），随后运行 `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` 与本对 `sync-mirrors.py --check` 过滤，确认零 DIFF 并把修复前后的 C-12/C-18 结果记入 `verification.md`。
- [ ] T013 [US1] [blockedBy: T010,T011,T012] 运行 `bash scripts/bash/run-tests.sh tests/unit/test_admission_check.py tests/contract/test_sdd_loop_driver_efficiency.py -q` 转绿，并实跑 quickstart S1/S2（含 `--json-out` 内容核对与 S2 的 `full-chain` 拒绝），把命令、输出、退出码记入 `notes/quickstart-run.md` 与 `verification.md`（首次创建）；记录 FR-042(a) 的脚本侧证据（阶段序列部分留给 T051 的录制 trace）与 SC-001/SC-002 的自动证据。
- [ ] T014 [US1] [blockedBy: T013] 执行 admission-check 变异演练：逐一施加「放宽 FR/任务区间端点」「把 SC 行计入 FR」「删去 (c)/(d) 扫描」「接受多行 lines manifest」四个变异，运行 `test_admission_check.py` 确认对应边界/计数/路径/单线用例变红，立即还原；把每个变异的命令、红输出与还原确认记入 `verification.md`。
- [ ] T015 [US1] [blockedBy: T014] 变异还原后复跑 `tests/unit/test_admission_check.py` 与 FL 契约 `tests/contract/test_sdd_loop_driver_efficiency.py`，复跑 quickstart S1/S2 并核对期望值；确认 `git diff` 仅含本特性预期改动后关闭 US1 checkpoint，结果记入 `verification.md`。

**Checkpoint**: US1 is independently functional: the medium fixture is admitted with a complete E1 record, the large fixture is refused fail-closed, and the reversion procedure is documented and pinned.

---

## Phase 4: User Story 2 - 全量测试预算与定向测试证据 (Priority: P1)

**Goal**: Bound each run line to exactly two full-suite slots (implement baseline, post-review closure), require deterministic targeted test sets and complete evidence for every intermediate stage and `review`, and make every out-of-slot full run an explicit exception.

**Independent Test**: Run the budget audit against the valid/invalid ledgers; run the injected-regression integration fixture and confirm the final name-level `comm -13` finds the injected failure.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T016 [US2] Author `tests/unit/test_audit_test_budget.py` red-first：覆盖合法两槽位台账、`test_out_of_slot_without_exception_fails`、槽内重跑只能出现在 closure 之后、第三个槽位拒绝、`environment-failure` 不消耗槽位、缺 `passed/failed` 报 `unknown` 而非 0、closure 缺名称级差集拒绝、`--logs-dir` 命中未入账全量命令拒绝、日志缺失报 `unknown`、摘要 `slots=baseline:1 closure:1 reruns=N exceptions=0 unknown=0`；把 red 运行记入 `notes/red-first-evidence.md`。
- [ ] T017 [US2] Author `tests/integration/test_sdd_loop_efficiency_regression.py` red-first：`test_injected_regression_found_by_name_diff` 在临时目录生成最小 pytest 套件，并用 `bash scripts/bash/run-tests.sh --names-out <临时名单> <临时测试目录> -q` 采集基线（该调用是定向运行，不是全量套件），注入一个已知失败后再次采集，断言 `comm -13 baseline final` 非空且该失败名被报告；同时断言审计脚本拒绝仅比较计数的 closure 记录；把 red 运行记入 `notes/red-first-evidence.md`。
- [ ] T018 [US2] [blockedBy: T009] 扩展 `tests/contract/test_sdd_loop_driver_efficiency.py` 的 TB-01…TB-10 测试函数（`test_tb_01_full_run_definition` … `test_tb_10_orchestration_layer_only`），钉住两槽位定义、baseline/closure 程序、定向集三条并集与选择依据、E3 证据字段、台账 JSONL 围栏、槽外例外与槽内重跑、环境失败边界、`--logs-dir` 扫描、编排层实现；在当前树先红并记入 `notes/red-first-evidence.md`。

### Implementation for User Story 2

- [ ] T019 [US2] [blockedBy: T016,T017] 实现 `skills/external/sdd-loop-driver/scripts/audit-test-budget.py`：解析状态脊 `<!-- test-budget:begin/end -->` JSONL 围栏，校验 `baseline`/`closure`/`in-slot-rerun`/`out-of-slot-exception`/`environment-failure` 语义、每线恰两槽位、例外必须带原因与证据、缺字段报 `unknown`、closure 必须名称级差集；支持 `--spine`、`--spec-dir`、`--logs-dir`；输出可粘贴进收尾汇总的摘要；退出码 0=通过 / 1=审计失败 / 2=输入或解析错误；仅标准库且 ≥3.8 兼容。
- [ ] T020 [US2] [blockedBy: T019] Author `references/efficiency-model.md` §2（两槽位、定向集三条并集与选择命令、E2/E3 证据字段、槽外例外、槽内重跑、环境失败边界），在 `references/stage-prompts.md` 写入 implement 起点 baseline、implement 内禁止第二次全量、中间阶段与 review 定向测试、`baseline_slot=skip(closure-repair)`、收口修复重入块，并在 `references/dispatch-recipes.md` Recipe 4 写入 review 后、合并前的 closure 槽位时序与证据路径。
- [ ] T021 [US2] [blockedBy: T020] 运行 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 并执行 `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` 与本对 `--check` 过滤，确认零 DIFF，把结果记入 `verification.md`。
- [ ] T022 [US2] [blockedBy: T019,T020,T021] 运行 `bash scripts/bash/run-tests.sh tests/unit/test_audit_test_budget.py tests/integration/test_sdd_loop_efficiency_regression.py tests/contract/test_sdd_loop_driver_efficiency.py -q` 转绿，并实跑 quickstart S3；把命令、输出与退出码记入 `notes/quickstart-run.md` 与 `verification.md`；记录 FR-042(b)/(e) 证据，并在 `verification.md` 记录 `baseline_slot=consumed` 与「closure 由驱动在 review 后执行、implement 未运行第二次全量」（不得向 `test-evidence/implement.jsonl` 追加非 JSON 行）。
- [ ] T023 [US2] [blockedBy: T022] 执行 audit-test-budget 变异演练：逐一施加「允许第三个槽位」「缺 `exception_reason` 仍通过」「用计数比较替代名称级差集」「忽略 `--logs-dir` 扫描命中」四个变异，运行 `test_audit_test_budget.py` 确认对应槽位/例外/差集/扫描用例变红，立即还原；把证据记入 `verification.md`。
- [ ] T024 [US2] [blockedBy: T023] 变异还原后复跑预算单测、回归集成测试与 TB 契约，复跑 quickstart S3；确认台账仍报告恰两槽位、0 例外、0 unknown，且 implement 内没有第二次全量执行，结果记入 `verification.md` 并关闭 US2 checkpoint。

**Checkpoint**: US2 is independently functional: the audit accepts the two-slot ledger, refuses out-of-slot runs without an exception, reports missing evidence as `unknown`, and the injected regression is found by name.

---

## Phase 5: User Story 3 - Plan 阶段「只小修、不重审」约束 (Priority: P2)

**Goal**: After `plan` completes, limit downstream changes to plan-owned artifacts to minor fixes, require a `PLAN-EDIT:` declaration for any touch, classify the final diff deterministically, and route substantive changes to the two FR-022 branches without a silent re-review loop.

**Independent Test**: Run `audit-plan-changes.py` against the plan-repo fixture with a declared minor edit, an undeclared edit, an uncommitted edit, and no touch; inspect the classification and disposition.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T025 [US3] Author `tests/unit/test_audit_plan_changes.py` red-first：在临时 git repo 中覆盖 `test_undeclared_plan_change_flagged`（提交区间触碰 `plan.md`、声明为空 → `undeclared=true`、exit 1）、`test_uncommitted_plan_change_included`（`git status --porcelain` 未提交改动进入触碰集合）、`test_declared_minor_change_passes`（声明行解析、exit 0）、`test_no_touch_reports_none`、`test_diff_stats_and_output_shape`、`test_script_is_read_only`（运行前后工作树与 HEAD 不变）；把 red 运行记入 `notes/red-first-evidence.md`。
- [ ] T026 [US3] [blockedBy: T018] 扩展 `tests/contract/test_sdd_loop_driver_efficiency.py` 的 PC-01…PC-10 测试函数（`test_pc_01_activation_point` … `test_pc_10_audit_script_interface`），钉住 plan U4 生效点与六个 plan 拥有路径、小修/实质改动定义、`PLAN-EDIT:` 前缀 token、U4 提交区间加未提交改动检查、两分支分流、analyze 修复路由不变、收口报告、显式排除、脚本只读接口；在当前树先红并记入 `notes/red-first-evidence.md`。

### Implementation for User Story 3

- [ ] T027 [US3] [blockedBy: T025,T026] 实现 `skills/external/sdd-loop-driver/scripts/audit-plan-changes.py`：参数 `--repo --base --head --plan-owned (repeatable) --declarations`；机械输出 `touched_paths[]`（`git diff --name-only <base>..HEAD` 加 `git status --porcelain`）、`declaration_lines[]`、`undeclared` 判定与 diff 统计；退出码 0=无未声明触碰 / 1=存在未声明触碰 / 2=输入或解析错误；只读工作树、仅标准库且 ≥3.8 兼容。
- [ ] T028 [US3] [blockedBy: T027] Author `references/efficiency-model.md` §3（`plan_constraint=active` 生效点、小修/实质改动定义、`PLAN-EDIT:` 声明格式的唯一 owner、U4 分类与 FR-022 两分支、显式排除与设计代价），在 `references/stage-prompts.md` 写入 tasks/analyze/implement/review 的只小修块与 `ANOMALY:` 实质改动回传要求，并在 `references/dispatch-recipes.md` 写入 plan U4 后登记约束、下游 U4 分类与分流程序。
- [ ] T029 [US3] [blockedBy: T028] 运行 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 并执行 `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` 与本对 `--check` 过滤，确认零 DIFF，把结果记入 `verification.md`。
- [ ] T030 [US3] [blockedBy: T027,T028,T029] 运行 `bash scripts/bash/run-tests.sh tests/unit/test_audit_plan_changes.py tests/contract/test_sdd_loop_driver_efficiency.py -q` 转绿，并按 quickstart S6 实跑未声明 plan 改动场景（exit 1、`touched_paths=["plan.md"]`、`undeclared=true`）；把命令、输出与退出码记入 `notes/quickstart-run.md` 与 `verification.md`；记录 FR-042(c) 证据。
- [ ] T031 [US3] [blockedBy: T030] 执行 audit-plan-changes 变异演练：逐一施加「忽略未提交改动」「空声明仍判 declared」两个变异，运行 `test_audit_plan_changes.py` 确认未声明/未提交用例变红，立即还原；把证据记入 `verification.md`。
- [ ] T032 [US3] [blockedBy: T031] 变异还原后复跑 plan 单测、PC 契约与 quickstart S6；确认 `PLAN-EDIT:` 格式 owner、两分支路由与「框架内部硬执行显式排除」均在文档面可见，结果记入 `verification.md` 并关闭 US3 checkpoint。

**Checkpoint**: US3 is independently functional: every plan touch is classified, undeclared/substantive changes fail the stage gate, and no silent re-review loop exists.

---

## Phase 6: User Story 4 - 阶段进度可见与驱动会话解耦 (Priority: P1)

**Goal**: Make every stage run with `--output-format stream-json` by default, preserve the raw event stream, derive an incrementally growing compact live log whose last non-empty line is the sentinel, and run stages detached under `nohup` in both local and remote topologies without changing verdicts, exit codes, or re-entry.

**Independent Test**: Run the runner integration fixture (stream, degraded, detached-survival) and the watcher stream cases; terminate the parent shell mid-stage and confirm the detached runner completes and a `--once` snapshot verifies it.

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T033 [US4] Author `tests/unit/test_derive_live_log.py` red-first：覆盖非终止事件正文含哨兵字样时不产生裸哨兵最后一行、终止 result 文本在 EOF 时逐字追加且最后非空行恰为 `PLAN-DONE`、无事件时不伪造进度行、`--finish` 从 raw 恢复终止 result、不可解析行与无 result 的派生失败不伪完成、管道增量输出在进程结束前即可读取；把 red 运行记入 `notes/red-first-evidence.md`。
- [ ] T034 [US4] Author `tests/integration/test_sdd_loop_efficiency_runner.py` red-first：`test_local_nohup_survives_parent_exit`（父 `bash -c` 启动 nohup runner 后退出，runner 继续并写出 status）、`test_stream_mode_writes_raw_and_live`（raw NDJSON 与 live 最后非空行哨兵）、`test_buffered_degradation_when_cli_lacks_stream`（`no-stream` stub → `progress=degraded` 且不伪完成）、`test_status_fields_and_exit_code_propagation`（`exit/sentinel/progress/detached` 字段与 CLI 退出码）、`test_once_snapshot_does_not_redispatch`（`--once` 快照对已完成阶段只核验）；把 red 运行记入 `notes/red-first-evidence.md`。
- [ ] T035 [US4] [blockedBy: T026] 扩展 `tests/contract/test_sdd_loop_driver_efficiency.py` 的 PD-01…PD-10 测试函数（`test_pd_01_stream_default_and_raw` … `test_pd_10_runner_interface`），钉住 stream-json 默认与 raw 落盘、增量派生、result-only 哨兵、watcher 判定不变、降级标记、双拓扑 nohup、`--once` 重入、`--raw-stream` 证据面与自测、无新等待/服务、runner 接口；在当前树先红并记入 `notes/red-first-evidence.md`。

### Implementation for User Story 4

- [ ] T036 [US4] [blockedBy: T033] 实现 `skills/external/sdd-loop-driver/scripts/derive-live-log.py`：从 stdin/`--events` 增量读取 NDJSON，非终止事件只输出带前缀的单行进度，EOF 时把终止 `result` 事件的 `result` 文本逐字追加；支持一次性 `--finish` 从 raw 恢复；不可解析行容错且不伪造完成；仅标准库且 ≥3.8 兼容。
- [ ] T037 [US4] [blockedBy: T034] 实现 `skills/external/sdd-loop-driver/scripts/stage-runner.sh`：参数 `--cli --cli-args --project-dir --prompt-file --sentinel --line --stage --state-dir --mode auto|stream|buffered --detached yes|no`；auto 探测 `--output-format` 能力；stream 模式 `CLI | tee raw-<line>-<stage>.jsonl | python3 derive-live-log.py --out log-<line>-<stage>.log`；写 pid/status/log/heartbeat 四件套与 runner-log；status 含 `exit/at/sentinel/progress/detached`；派生失败先 `--finish` 恢复、再 buffered fallback、两者皆无判 `sentinel=0`；退出码等于 CLI 退出码；不自行 detach（nohup 由派发配方提供）。
- [ ] T038 [US4] [blockedBy: T036,T037] 扩展 `skills/external/sdd-loop-driver/scripts/watch-target.sh`：新增可选 `--raw-stream PATH`（WATCH 附 `stream=na|absent|growing|idle`、EVIDENCE 附 raw 路径与字节数，不参与任何 verdict）；修复四个既有自测失败（`pid-reuse`、`zombie`、`manifest`、`pgrep-zero-match-trap-reproduced`）为可跨平台运行或显式平台跳过（禁止删除用例）；新增四个自测用例（非终止事件哨兵字样不判 DONE、终止 result 事件判 DONE、派生失败不伪完成、脱离 runner 在驱动退出后存活）；判定表、退出码与窗口/deadline 语义零改动。
- [ ] T039 [US4] [blockedBy: T036,T037,T038] Author `references/efficiency-model.md` §4（stream-json 主路径、派生与降级、raw/live 证据、nohup 双拓扑、重入），更新 `references/dispatch-recipes.md` Recipe 2 为 `stage-runner.sh` 调用形态并把 `sed` 派生旧形态标注为被取代、Recipe 3 与 Recipe 5 写入本地 `nohup … </dev/null >runner-log 2>&1 &` 与远端 `ssh + su + nohup` 等价形态、派发记录 `detached=yes|no`，更新 `references/watch-model.md` §2/§3/§4 的进度、降级与 raw 证据面（判定表不变），并在 `references/stage-prompts.md` 写入重入 `--once`、脱离派发字段与无独立 sleep 回合的等待纪律。
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

- [ ] T044 [US5] [blockedBy: T043] 在 `skills/external/sdd-loop-driver/SKILL.md` 的 `## Discipline Defaults` 与 `## References` 之间新增 H2 `Efficiency Optimizations（运行效率优化）`（四项机制摘要 + 指向 `references/efficiency-model.md` 的单一 owner 指针 + 新脚本清单，不复述细节），并同步更新 `tests/contract/test_sdd_loop_driver_skill.py` 的 `PINNED_H2_SECTIONS`；在测试文件内记录「C-3 有意更新」的理由与日期。
- [ ] T045 [US5] [blockedBy: T044] 更新 `tests/contract/test_sdd_loop_driver_skill.py` 的 C-4 断言：把 runner 派生的 `sed` 断言替换为 `stage-runner.sh` 断言，保留 `nohup`、heartbeat、阶段链与收尾断言；在测试文件内记录「C-4 有意更新」的理由（单点可测试、消除每阶段副本漂移）与日期，禁止静默删除。
- [ ] T046 [US5] [blockedBy: T035,T045] 在 `tests/contract/test_sdd_loop_driver_efficiency.py` 增加 DI-01…DI-09 测试函数（`test_di_01_confirmation_gates_unchanged` … `test_di_09_orchestration_layer_only`）与覆盖 meta-test：逐个读取五份契约的 `FL/TB/PC/PD/DI` 条款 id，断言每个 id 都有对应的 `test_<prefix-lower>_<nn>_...` 测试函数（共 49 条），并钉住确认门、独立校验、卡死处置、质量门、交付面/镜像、自应用、向后兼容与编排层优先；运行该文件转绿并把结果记入 `verification.md`。
- [ ] T047 [US5] [blockedBy: T039] 更新 `docs/reference/skills/sdd-loop-driver.md`：新增四项优化的用户文档段（快车道与准入、两槽位预算与定向证据、plan 只小修约束、stream-json 进度与 nohup 双拓扑），披露日志形态变化（新增 raw stream 与 live log；不支持时降级并记 `progress=degraded`）与「不改变完成判定」，保留既有双拓扑/可移植/投递/目标项目内容，并避免「运行时必读」措辞。
- [ ] T048 [US5] [blockedBy: T044,T045,T046,T047] 运行 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 与 `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` 确认本对字节一致；运行 `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` 确认 exit 0，再运行 `python3 scripts/python/sync-mirrors.py --check --only skills/external`（比本对选择器宽一级）并记录：本对 0 DIFF，其余 11 个目录的既有 65 DIFF 不属本特性面（相对基线为零 NEW drift）；运行 `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` 确认 74 units 零漂移；全部结果记入 `verification.md`。
- [ ] T049 [US5] [blockedBy: T046,T048] 运行 `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py tests/contract/test_sdd_loop_driver_efficiency.py -q`：既有 23 个测试函数全绿（C-12/C-18 的镜像漂移已由 T012/T048 修复，C-3/C-4 为有意更新），新增效率契约与覆盖 meta-test 全绿；把通过输出与两份契约的条款覆盖数（49/49）记入 `verification.md`。
- [ ] T050 [US5] [blockedBy: T049] 按 `.specify/shared/workflow/feature-integration.md` 更新 `.specify/memory/features/058.md` 的 Latest Review/Status Tracking（追加 063 实现记录，状态保持 `Implemented`）与 `.specify/memory/features.md` 的 058 行 Last Updated 注记；确认索引 `Total Features` 不变、未新建 Feature、未回退状态。
- [ ] T051 [US5] [blockedBy: T041,T050] 录制 quickstart S7 的 dry-run 编排决策 trace（不启动嵌套驱动）：用中型夹具逐决策记录「入口携带 `fast-lane=opt-in` → tasks U4 通过 → admission-check 录取 → 跳过 checklist → analyze → implement 基线 → review → 收口 → 合并」与一个未携带字面量的完整链对照，记录每步的实际脚本输出与预期阶段序列；把 trace 路径、要点与「非 CI 录制证据」标注写入 `notes/quickstart-run.md` 与 `verification.md`。
- [ ] T052 [US5] [blockedBy: T048,T049,T050,T051] 收口汇总与最终核验：核对 `notes/red-first-evidence.md` 覆盖全部新脚本与 watcher 扩展、`verification.md` 记录六个变异演练及还原、SC-001…SC-013 逐条状态与证据类别（自动/录制 trace/驱动收口）、23 项交付路径存在；运行 `python3 .specify/scripts/python/validate-requirements.py .specify/specs/063-sdd-loop-efficiency/requirements.md` 与 `python3 .specify/scripts/python/validate-tasks.py .specify/specs/063-sdd-loop-efficiency/tasks.md` 确认 exit 0；复跑 GATE-1 的定向测试集；确认 implement 只消耗 baseline 槽位、closure 仍为驱动在 review 后的职责；确认 063 自身无快车道记录且 checklist/analyze 产物在位（review 由驱动在 implement 后执行）；把全部结论写入 `verification.md`。

**Checkpoint**: US5 is independently verifiable: the skill/docs/mirror/test surfaces are delivered, the two baseline anomalies are repaired mechanism-side, the feature registry remains `Implemented`, and the self-application exclusion is evidenced.

---

## Feature Integration Review

- 2026-10-20, tasks phase: `.specify/memory/features.md` registers 61 features; Feature 058 exists with status `Implemented`; spec 063 is bound to 058 as an evolutionary slice; `.specify/memory/features/058.md` exists. The task breakdown exposes **no new Feature** and invalidates no existing Feature: the five new scripts and the watcher extension are all within 058's existing `skills/external/sdd-loop-driver/` surface. Status stays `Implemented`; T050 appends the implementation-stage record. The tasks-stage record is appended to the feature detail and index by the `/speckit.tasks` lifecycle itself.

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
| `contracts/plan-constraint.md` | PC-01…PC-10 | US3 (T026) | `test_pc_01…test_pc_10` |
| `contracts/progress-decoupling.md` | PD-01…PD-10 | US4 (T035) | `test_pd_01…test_pd_10` |
| `contracts/delivery-and-invariants.md` | DI-01…DI-09 | US5 (T046) | `test_di_01…test_di_09` |

Total: 49 clauses. T046 adds the coverage meta-test that asserts every clause id has a named test function; T009/T018/T026/T035 create and extend the same contract-test file, so those rows serialize.

### Assumptions and decisions

- **D-T1 (no `[green:]` tags)**: the five contracts declare `FL/TB/PC/PD/DI` clause ids, not the repository's machine clause form `C-<number>`. Renaming 49 clauses would be a substantive contract change outside the tasks stage; the optional `[green:]` tag is therefore omitted. Coverage is pinned by one named test per clause plus the T046 meta-test and each contract's traceability table.
- **D-T2 (story order)**: phases follow requirement order US1→US2→US3→US4→US5 rather than strict P1-first. All four optimization stories append to the same owner document and the same stage-prompts/dispatch-recipes files; numeric order keeps the owner sections in authoring order and avoids placeholder markers. US4 is P1 and has no behavioral dependency on US2/US3; a multi-writer team can partition the shared files and run it in parallel.
- **D-T3 (closure ownership)**: the second full-suite slot is owned by the driver after `review`, per FR-011 (`review` 通过之后、合并之前). It is intentionally **not** an implement task: scheduling it inside implement would make it stale before review and would violate the stage order. T002 consumes the only implement-side full-suite slot; T022/T052 record the obligation; the driver executes and ledgers the closure.
- **D-T4 (S7 evidence)**: `quickstart.md` S7 is a recorded dry-run decision trace, not a nested driver launch. The skill's Hard Requirement 6 forbids nested driving, so T051 records the decision sequence and script outputs without launching a driver inside a stage subagent; `verification.md` labels it as non-CI evidence.
- **D-T5 (baseline anomalies)**: the watcher self-test platform/timing failures are repaired mechanism-side in `watch-target.sh` (portable check or explicit platform skip, never deletion); the sdd-loop-driver mirror drift is repaired with `sync-mirrors.py --write --only skills/external/sdd-loop-driver`; the other 11 directories' 65 pre-existing DIFFs are out of this feature's surface and are disclosed under the zero-NEW-drift relative criterion. **Correction (disclosed)**: plan.md phrases the write selector as `--only skills/external`, which is a prefix that would also write the other 11 skills; the task list narrows it to the owned pair (`--only skills/external/sdd-loop-driver`), which is the only reading consistent with the plan's “其余 11 个目录不属本特性面 / 零 NEW drift” criterion. No plan artifact is modified.
- **D-T6 (intentional existing-assertion updates)**: C-3 (`PINNED_H2_SECTIONS`) and C-4 (`sed` → `stage-runner.sh`) are the only existing assertions intentionally changed. Both changes carry an in-file reason and date; no other assertion is weakened.
- **D-T7 (self-application)**: 063's own run is full-chain. No fast-lane admission record is produced for it; checklist/analyze artifacts exist; review is executed by the driver after implement. T052 records that boundary honestly.

### Measured premises (commands actually run at generation time, 2026-10-20)

- FR definitions: `grep -cE '^\- \*\*FR-[0-9]{3}\*\*:' requirements.md` → `43` (trap: counting every `FR-` mention also matches citation rows and SC text; the anchored definition-line pattern is the contract).
- Success criteria: `grep -cE '^\- \*\*SC-[0-9]{3}\*\*:' requirements.md` → `13`.
- Data-model validation rules: `grep -cE '^- V-E[0-9]+-[0-9]+' data-model.md` → `30` (trap: the ASCII-colon form `^- V-E[0-9]+-[0-9]+:` returns `0` because the file uses a full-width `：`).
- Contract clauses: FL `10`, TB `10`, PC `10`, PD `10`, DI `9`; total `49` (`grep -cE '^- \*\*(FL|TB|PC|PD|DI)-[0-9]{2}' contracts/*.md`).
- Deliverables: `awk` over the first fenced block in `feature-ref.md` → `23`.
- Existing contract baseline: `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q` → `2 failed, 21 passed` (C-12/C-18 mirror drift).
- Watcher self-test baseline: `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` → `12 passed, 4 failed` (`pid-reuse`, `zombie`, `manifest`, `pgrep-zero-match-trap-reproduced`).
- Mirror baseline: `python3 scripts/python/sync-mirrors.py --check --only skills/external` → exit `2`, `68 DIFF` across 12 skill directories, of which `3` are in `sdd-loop-driver`.
- Compile face: `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` → `74 units, zero drift`, exit `0`.
- Requirements validator: `python3 .specify/scripts/python/validate-requirements.py .../requirements.md` → `301 lines, 56 definition rows, 6 shared strings, 0 error(s), 0 warning(s)`.
- Interpreter probes: `python3 --version` → `3.9.6`; `python --version` → `3.14.6`; `python -m pytest --version` → `pytest 9.1.1`; direct `python3 -m pytest` is unavailable.
- Task rows at generation: `grep -cE '^- \[[ xX>~]\] T[0-9]{3}' .specify/specs/063-sdd-loop-efficiency/tasks.md` → `52`.
- Deliverable-path initial state: of the 23 paths in `feature-ref.md`, `14` are new and absent (owner doc, 5 new scripts, 7 new test files, fixtures dir), `9` are update targets and present (SKILL.md, 3 existing references, watch-target.sh, docs page, existing contract test, 058 detail and index).

### Runtime-evidence landing points

- `.specify/specs/063-sdd-loop-efficiency/notes/pre-change-measurements.md` — T001/T002 measured values, commands and dates.
- `.specify/specs/063-sdd-loop-efficiency/notes/baseline-failed-tests.txt` — T002 implement-start full-suite name list (the single `baseline` slot).
- `.specify/specs/063-sdd-loop-efficiency/notes/baseline-mirror-check.txt`, `notes/baseline-contract-sdd-loop-driver.txt`, `notes/baseline-watch-selftest.txt` — T001 raw baseline outputs.
- `.specify/specs/063-sdd-loop-efficiency/notes/red-first-evidence.md` — T008/T009/T016/T017/T018/T025/T026/T033/T034/T035 red commands, real output and exit status.
- `.specify/specs/063-sdd-loop-efficiency/notes/quickstart-run.md` — T013/T022/T030/T041/T051 quickstart runs and teardown.
- `.specify/specs/063-sdd-loop-efficiency/verification.md` — T013 onward behavior/structure/SC evidence; T052 final summary.
- `.specify/specs/063-sdd-loop-efficiency/test-evidence/implement.jsonl` — T002 baseline ledger entry; T022's `baseline_slot=consumed` and closure-ownership note live in `verification.md`, not in this JSONL file.

### Budget closure ownership

- This feature's own run has exactly two full-suite slots: `baseline` (T002, inside implement) and `closure` (driver-owned after review, before merge).
- Implement MUST NOT run the closure full suite and MUST NOT run any other full suite. Intermediate stages and `review` use the targeted set selected by the rule in `references/efficiency-model.md` §2.
- If the driver's closure finds new failures and a fix requires rerunning the same suite, the rerun is recorded as `in-slot-rerun` with trigger and evidence; it does not open a third slot.
- Any out-of-slot full run must be an `out-of-slot-exception` with a reason and evidence pointer, and is listed in the final wrap-up summary.

### Pre-existing observations (not repaired by this feature)

- The other 11 skill directories' mirror drift (65 of the 68 baseline DIFFs) is pre-existing and outside this feature's surface; T048 records zero NEW drift rather than claiming a global zero.
- The 2 existing contract failures (C-12/C-18) are repaired by this feature's scoped mirror sync, not waived.
- The 4 watcher self-test failures are repaired mechanism-side in `watch-target.sh`; Linux-only branches may be platform-skipped on macOS, and the skip is named in the self-test output.
