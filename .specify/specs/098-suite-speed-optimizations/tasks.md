# Tasks: 测试套件提速五项优化（xdist 验证 / slow 分档 / 会话缓存 / 去固定 sleep / 进程内直调）

**Requirement ID**: 098
**Requirement Key**: 098-suite-speed-optimizations
**Related Feature**: 086 Efficient Test Execution (Concurrent by Default) — status stays `Ready for Review`
**Input**: Design documents from `.specify/specs/098-suite-speed-optimizations/`
**Prerequisites**: plan.md (required), requirements.md (required), research.md, data-model.md, contracts/ (6 files, 68 clauses), quickstart.md, feature-ref.md

**Tests Mode**: ON — `.specify/constitution.md` Principle IV "Test-First & Contract-Driven Implementation" carries MUST rows ("Pure functions/utilities MUST have unit tests", "Critical flows MUST have automated regression coverage", "Integration/contract tests MUST cover cross-service communication and external APIs"); this feature's own six contract files (`contracts/*.contract.md` § Test obligations) additionally require their cases before the behavior change. Layers emitted: contract (5 new guard files + the tier contract file), integration conversions (event-wait/runner), and the existing 086 runner contract suite (measured 40 collected cases) as the compatibility baseline.

**Organization**: Tasks are grouped by user story (requirements.md § User Scenarios & Testing) so each story is independently implementable and testable. `plan.md` § Work Packages maps onto the phases: WP-1/WP-2 → US1; WP-3/WP-4 → US2; WP-5 → US3; WP-6 → US4; WP-7/WP-8 → US5; WP-9 → Polish and the closure-stage row. Each phase stays ≤16 rows so `/speckit.implement` can package it at ~10 tasks per package (≤16).

## Definition of Done (DoD)

- DoD-1: Every task row is `[X]` or an explicitly deferred `[~]` with its reason recorded in `verification.md` under `deferred_tasks=`
- DoD-2: The five new contract files (`test_suite_tier_contract.py`, `test_parallel_consistency_contract.py`, `test_scan_cache_contract.py`, `test_event_wait_contract.py`, `test_inprocess_conversion_contract.py`) are green under `scripts/bash/run-tests.sh`
- DoD-3: The existing 086 runner contract suite (`tests/contract/test_run_tests_runner_contract.py`, 40 collected cases) is green and C-001…C-016 text is untouched
- DoD-4: The four mirror obligations regenerate cleanly — `python3 scripts/python/sync-mirrors.py --check` shows no NEW drift on the runner pair, the `feedback-utils.py` pair and the two driver reference pairs
- DoD-5: Every `final`-path success criterion (SC-001…SC-009) is `pass` with a named evidence path; SC-010/SC-011 are recorded as `supporting`
- DoD-6: Quickstart S-1…S-13 are executed and their real output (with teardown) is recorded in `notes/quickstart-run.md`
- DoD-7: The two-slot test budget stays exactly two budget slots: slot 1 `baseline` at implement start, slot 2 `closure` after review; no third full run is added for measurement. The closure stage additionally runs its same-tree `--full --serial` validation run (T061): it consumes no budget slot, is not a measurement, and is required by the parallel-consistency comparison (requirements A14, parallel-consistency C-007)

**DoD Status**: pending

## Completion Gate

- GATE-1: Closure-slot full run has zero NEW failures vs the recorded baseline — **evaluated at the closure stage** (the post-change full runs are the closure slot plus its same-tree serial validation run; implement runs no full suite, and the validation run is neither a budget slot nor a measurement — requirements A14): check: `bash scripts/bash/run-tests.sh --full --names-out .specify/specs/098-suite-speed-optimizations/final-failed.txt` then `comm -13 .specify/specs/098-suite-speed-optimizations/baseline-failed.txt .specify/specs/098-suite-speed-optimizations/final-failed.txt` is empty (the two pre-existing names `test_c5_gate_budget_is_unchanged_by_the_owner_document` and `test_c10_openapi_clauses_are_method_keys_and_the_total_matches_the_census` appear on both sides and compare equal by name)
- GATE-2: Every mirror obligation from plan.md verified with no NEW drift — check: `python3 scripts/python/sync-mirrors.py --check` exits 0 on the runner, `feedback-utils.py` and two `skills/external` reference pairs (generation-time baseline 2026-11-10: exit 0, all pairs `ok`)
- GATE-3: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\]' .specify/specs/098-suite-speed-optimizations/tasks.md` returns 0
- GATE-4: Every `final`-path success criterion is `pass` **and** the feature's smoke record is present — check: in `verification.md`, every criterion whose `**Path**` marker reads `final` has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` (a path that exists and is non-empty) are all present; the closure-stage rows supply the SC-003/SC-005 readings before this gate is re-read
- GATE-5: Every new or changed test file passes a targeted run under the canonical runner, and every red-first record exists — check: `bash scripts/bash/run-tests.sh tests/contract/test_suite_tier_contract.py tests/contract/test_parallel_consistency_contract.py tests/contract/test_scan_cache_contract.py tests/contract/test_event_wait_contract.py tests/contract/test_inprocess_conversion_contract.py -q` exits 0 and `.specify/specs/098-suite-speed-optimizations/notes/red-first-evidence.md` is non-empty

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (`[US1]`…`[US5]`), required on user-story rows only
- **[blockedBy: T001,T002]** (optional): the listed tasks MUST be `[X]` before this row starts
- **[green: <contract>#<clause>]** (optional, repeatable): the row that turns that contract clause green; contract paths resolve relative to this file's directory. Every clause of the six contract files is claimed by exactly one row (partition in § Clause Attribution)
- Every row keeps its checkbox, ID, labels, description, path and tags on ONE line

## Path Conventions

Single repository: tests under `tests/`, engines under `scripts/python/`, the runner under `scripts/bash/`, the driver references under `skills/external/sdd-loop-driver/references/` (mirrored to `.specify/skills/sdd-loop-driver/references/`), feature records under `.specify/specs/098-suite-speed-optimizations/`.

## Measured Premises (re-derived at tasks generation, 2026-11-10)

Every count below was produced by the command shown, run in this worktree on 2026-11-10; implement MUST re-derive the baseline readings at its own start instead of inheriting these numbers.

| # | Premise | Re-derivation command | Measured output |
|---|---------|----------------------|-----------------|
| P-1 | Full collection size | `bash scripts/bash/run-tests.sh --serial --collect-only -q 2>/dev/null \| grep -c '::'` | `8543` |
| P-2 | Existing runner contract suite cases | `bash scripts/bash/run-tests.sh --workers 1 tests/contract/test_run_tests_runner_contract.py --collect-only -q` | `40 tests collected in 0.03s` (trap: naive `grep -c 'def test_'` returns `49` because fixture-source strings also match; the collected count is 40) |
| P-3 | `time.sleep` census under `tests/` | `grep -rn --include='*.py' 'time\.sleep' tests/ \| wc -l` | `20` occurrences in 10 files; scope files: `test_client_metrics.py` 8, `test_feedback_probe_cli.py` 1, `test_line_envelope_contract.py` 2, `test_store_state_protocol.py` 2, `test_sdd_loop_efficiency_runner.py` 1, `test_session_kill_reattach.py` 2 |
| P-4 | `subprocess.run` census under `tests/` | `grep -rn --include='*.py' 'subprocess\.run' tests/ \| wc -l` and `grep -rln … \| wc -l` | `499` source lines / `229` files (research B-9 recorded 498/228; the AST scan at T043 owns the final denominator — source lines are not call sites) |
| P-5 | Session-scoped pytest fixtures today | `grep -rn --include='*.py' 'fixture(scope="session"' tests/ \| wc -l` | `0` |
| P-6 | Registered pytest markers | `grep -n 'markers' -A 8 pyproject.toml` | lines 53–57: `contract`, `integration`, `serial` only; no `slow` registration |
| P-7 | Shared wait helper | `grep -n 'def wait_until' tests/fixtures/line_fixtures.py` | `396:def wait_until(predicate, timeout: float = 5.0, interval: float = 0.05) -> bool:` |
| P-8 | Engine clock reads | `grep -n 'def now_iso\|def timestamp_id' scripts/python/feedback-utils.py` | `125:def now_iso()` / `129:def timestamp_id()` |
| P-9 | Two-slot budget surfaces | `grep -n 'run-tests.sh' skills/external/sdd-loop-driver/references/efficiency-model.md` and `…/stage-prompts.md` | `efficiency-model.md:91` baseline row, `:92` closure row; `stage-prompts.md:165` baseline restatement, `:206` closure restatement; `audit-test-budget.py` treats `--full` as a flag (research B-10) |
| P-10 | Toolchain | `python3 -V`; `python3 -c 'import pytest, xdist; print(pytest.__version__, xdist.__version__)'`; `git --version` | `Python 3.11.11`; `pytest 8.4.2 xdist 3.8.0`; `git version 2.43.5` — no docker/network/cluster dependency exists for any task |

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the runtime-evidence landing points and freeze the two generation-time baselines that later rows diff against.

- [X] T001 Create the spec runtime-evidence directory `.specify/specs/098-suite-speed-optimizations/notes/` for red-first evidence, the quickstart run record and the pre-change measurements (directory meaning: `create-tasks` § runtime-evidence landing points).
- [X] T002 [P] Freeze the clause-coverage baseline with `python3 scripts/python/account-clause-coverage.py .specify/specs/098-suite-speed-optimizations --freeze > .specify/specs/098-suite-speed-optimizations/coverage-baseline.txt` and confirm the printed header records the freeze context (68 clauses over the six contract files are the claim universe).
- [ ] T003 [blockedBy: T001] Record two-slot budget slot 1 of 2 (implement-start baseline, pre-change runner = full selection by construction) plus the pre-change measurements in `.specify/specs/098-suite-speed-optimizations/notes/pre-change-measurements.md`: full-suite wall and `--names-out` reading, full-tier `--collect-only -q` id set, `test_client_metrics.py` wall (S-0.4), corpus-pair pass/fail names (S-0.5), the scope sleep census (P-3) and the subprocess census (P-4) — command, exit code and duration for each; land run-time output outside `.specify/specs` and copy it afterwards (corpus-write hazard, `test-evidence/corpus-write-hazard.txt`).

## Phase 2: User Story 1 - 缺省反馈循环只跑快档，且排除被明示 (Priority: P1) 🎯 MVP

**Goal**: The canonical runner's default tier excludes `slow`-marked tests and discloses the excluded count on the mode line; a caller `-m` owns its selection; `--full` restores the full selection; marker registration and membership evidence are machine-checked.

**Independent Test**: On the same tree, `bash scripts/bash/run-tests.sh --collect-only -q` versus `--full --collect-only -q` differ exactly by the `-m slow` set (S-1); the mode line reads `tier=fast excluded_slow=<measured>`; adding one slow test to a fixture tree increments `excluded_slow` (S-2/S-3).

**Checkpoint**: US1 alone is a working fast default with disclosure; coverage is never silently shrunk because `--full` and the disclosed count are both runner-native.

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T004 [US1] Author the red tier-behavior contract cases in `tests/contract/test_suite_tier_contract.py` (tier-selection §E obligations 1–10: default exclusion, no-slow tree, caller `-m` in both spellings, path/`-k`, `--full`+`-m`, `--serial` × {fast, full, caller}, `serial`+`slow` intersection, empty-after-exclusion, `--help`/undeclared option, header expression) on throwaway fixture trees whose `pytest.ini` registers `slow`; record the red run in `notes/red-first-evidence.md`.

### Implementation for User Story 1

- [X] T005 [US1] [blockedBy: T004] Implement `--full` flag parsing, the extended script-interface usage/`--help` text, and caller `-m` detection in both spellings (`-m <expr>`, `-m=<expr>`) in `scripts/bash/run-tests.sh`.
- [X] T006 [US1] [blockedBy: T005] Implement the default fast-tier exclusion and its serial two-pass composition (`-m "not serial and not slow"` then `-n0 -m "serial and not slow"`), path/`-k` narrowing inside the tier, and `--serial` orthogonality in `scripts/bash/run-tests.sh`.
- [X] T007 [US1] [blockedBy: T006] Implement the `slow` marker enumeration (`excluded_slow` via `--collect-only -q -m slow` with `-q`/`--quiet` normalised away and exit 5 treated as zero), the appended `tier=`/`excluded_slow=` mode-line fields, the truthful header, and the empty-after-exclusion named error (exit 2) in `scripts/bash/run-tests.sh`. [green: contracts/tier-selection.contract.md#C-001] [green: contracts/tier-selection.contract.md#C-002] [green: contracts/tier-selection.contract.md#C-003] [green: contracts/tier-selection.contract.md#C-004] [green: contracts/tier-selection.contract.md#C-005] [green: contracts/tier-selection.contract.md#C-006] [green: contracts/tier-selection.contract.md#C-007] [green: contracts/tier-selection.contract.md#C-008] [green: contracts/tier-selection.contract.md#C-009] [green: contracts/tier-selection.contract.md#C-010] [green: contracts/tier-selection.contract.md#C-011]
- [ ] T008 [US1] [P] Register the `slow` marker with its semantic description and default-tier exclusion statement in `pyproject.toml` (markers block, lines 53–57) (FR-005). [green: contracts/slow-membership.contract.md#C-001]
- [ ] T009 [US1] [blockedBy: T008] Measure the candidate durations, write the membership registry `test-evidence/slow-members.md` (columns `test_id | category | reason | date`; categories `process-boundary` / `corpus-scan`) and `test-evidence/slow-members-measurement.txt`, then apply `@pytest.mark.slow` to exactly the measured members only (FR-006). [green: contracts/slow-membership.contract.md#C-002] [green: contracts/slow-membership.contract.md#C-003] [green: contracts/slow-membership.contract.md#C-004]
- [ ] T010 [US1] [blockedBy: T007, T009] Append the registry↔collect identity, real-tree collection-equality, disclosure-arithmetic and guard-not-a-member cases (slow-membership C-005…C-009) to `tests/contract/test_suite_tier_contract.py`, deriving both sides at guard time and embedding no member count.
- [X] T011 [US1] [blockedBy: T007] Regenerate the projected runner mirror with `python3 scripts/python/sync-mirrors.py --write --only scripts` and verify `python3 scripts/python/sync-mirrors.py --check` reports no NEW drift on the `run-tests.sh` pair.
- [ ] T012 [US1] [blockedBy: T010, T011] Run `tests/contract/test_suite_tier_contract.py` (obligations 1–11) and the existing 086 runner contract suite (40 collected cases, P-2) under the canonical runner green; record commands, exits and durations in `test-evidence/tier-contract-green.txt`. [green: contracts/tier-selection.contract.md#C-012] [green: contracts/tier-selection.contract.md#C-013] [green: contracts/tier-selection.contract.md#C-014] [green: contracts/slow-membership.contract.md#C-005] [green: contracts/slow-membership.contract.md#C-006] [green: contracts/slow-membership.contract.md#C-007] [green: contracts/slow-membership.contract.md#C-008] [green: contracts/slow-membership.contract.md#C-009]
- [ ] T013 [US1] [blockedBy: T012] Execute mutation drills TS-M1…TS-M8 and SL-M1…SL-M5 on throwaway copies and record each red output in `test-evidence/tier-mutations.txt`.

**Checkpoint**: US1 is independently testable: the fast default, the disclosure count, the caller-priority matrix and the registry guard all run without US2–US5.

---

## Phase 3: User Story 2 - 全量档与两槽位预算仍然完整 (Priority: P1) 🎯 MVP

**Goal**: `--full` covers every collected test; both budget slots (baseline at implement start, closure after review) run the full tier with `--names-out`; the full selection does not regress; parallel safety is verified by same-tree bidirectional name comparison starting at `tests/contract`.

**Independent Test**: `bash scripts/bash/run-tests.sh --full --collect-only -q` equals the implement-start id set plus this feature's tests (S-12); both driver rows carry `--full` (S-9); the contract-subset parallel-vs-serial `comm` is empty in both directions (S-4).

**Checkpoint**: US1+US2 together form the completeness increment (MVP): faster default without a silently shrunk full path.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T014 [US2] Author the parallel-consistency contract cases in `tests/contract/test_parallel_consistency_contract.py`: same-tree bidirectional `--names-out` comparison discipline, no wall-clock assertions, and the non-parallel-safe fixture drill (two tests writing one shared path behind a barrier) whose comparison MUST be non-empty; record the drill output in `notes/red-first-evidence.md`.

### Implementation for User Story 2

- [ ] T015 [US2] [blockedBy: T007, T009] Run the contract-subset comparison (S-4, targeted run — no budget slot): default-parallel `--workers 4 tests/contract --names-out` versus `--serial tests/contract --names-out`, both `comm -13` and `comm -23` empty; record commands, exits, durations and complete lists in `test-evidence/parallel-consistency-contract.txt`.
- [ ] T016 [US2] [blockedBy: T007] Run the no-xdist PYTHONPATH shim over `tests/contract` (the 086 C-006 construction) and record the `reason=no-xdist` mode line plus a valid `--names-out` list in `test-evidence/parallel-consistency-noxdist.txt`.
- [ ] T017 [US2] [blockedBy: T014, T015, T016] Run `tests/contract/test_parallel_consistency_contract.py` green and record the run in `test-evidence/parallel-consistency-contract.txt`. [green: contracts/parallel-consistency.contract.md#C-001] [green: contracts/parallel-consistency.contract.md#C-002] [green: contracts/parallel-consistency.contract.md#C-003] [green: contracts/parallel-consistency.contract.md#C-004] [green: contracts/parallel-consistency.contract.md#C-005] [green: contracts/parallel-consistency.contract.md#C-006] [green: contracts/parallel-consistency.contract.md#C-009] [green: contracts/parallel-consistency.contract.md#C-010] [green: contracts/parallel-consistency.contract.md#C-011] [green: contracts/parallel-consistency.contract.md#C-012]
- [ ] T018 [US2] [P] [blockedBy: T005] Add `--full` to the two slot command rows in `skills/external/sdd-loop-driver/references/efficiency-model.md` §2 (baseline `:91`, closure `:92`) so neither slot can silently run the default tier (FR-010).
- [ ] T019 [US2] [P] [blockedBy: T005] Add `--full` to the baseline (`:165`) and closure (`:206`) restatements in `skills/external/sdd-loop-driver/references/stage-prompts.md`.
- [ ] T020 [US2] [blockedBy: T018, T019] Regenerate the skill mirrors with `python3 scripts/python/sync-mirrors.py --write --only skills/external` and verify `--check` reports no NEW drift on the two driver reference pairs.
- [ ] T021 [US2] [blockedBy: T020] Append the two-slot `--full` doc-assertion case and the full-collection equality case (tier-selection §E obligation 11) to `tests/contract/test_suite_tier_contract.py`.
- [ ] T022 [US2] [blockedBy: T003, T021] Produce the full-tier collection diff (S-12) against the implement-start id set in `notes/pre-change-measurements.md` and record `test-evidence/full-collection-diff.txt` (FR-011). [green: contracts/tier-selection.contract.md#C-015]
- [ ] T023 [US2] [blockedBy: T017] Execute mutation drills PC-M1…PC-M5 on throwaway copies and record each red output in `test-evidence/parallel-mutations.txt`.

**Checkpoint**: US2 independently proves the full path is intact and the budget surfaces request it; US1 is not required for the parallel-consistency drill itself.

---

## Phase 4: User Story 3 - 全语料扫描每个会话只算一次 (Priority: P2)

**Goal**: The two corpus contract files consume a per-session (per-worker), read-only scan payload built once; mutable fixtures never share it; a tampered corpus still reddens.

**Independent Test**: A counted probe shows `build_count = 1` per worker and `traversals = 1` for `framework-specs-corpus`; both files' pass/fail names are equal before and after; the tmp-corpus cross-session drill reddens (S-5).

**Checkpoint**: US3 is independent of the tier and of US4/US5 — it touches only `tests/conftest.py` and the two corpus test files.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T024 [US3] Author the scan-cache contract cases in `tests/contract/test_scan_cache_contract.py` (`build_count`/`traversals` counters on the fixture value, deep-copy immutability, the static no-mtime-staleness assertion, and the tmp-corpus cross-session mutation drill); record the red run in `notes/red-first-evidence.md`.

### Implementation for User Story 3

- [ ] T025 [US3] [blockedBy: T024] Add the session scan-cache fixture factory to `tests/conftest.py` for surfaces `framework-specs-corpus` and `framework-root-inputs`, keyed by (worker, surface, root, variant), with a build counter and `copy.deepcopy` consumer access (scan-cache C-007 house pattern: `importlib.util.spec_from_file_location` over `scripts/python/account-clause-coverage.py`). [green: contracts/scan-cache.contract.md#C-001] [green: contracts/scan-cache.contract.md#C-002] [green: contracts/scan-cache.contract.md#C-003] [green: contracts/scan-cache.contract.md#C-004] [green: contracts/scan-cache.contract.md#C-007]
- [ ] T026 [US3] [blockedBy: T025] Convert the real-repository reads in `tests/contract/test_coverage_receipt.py` to the session `framework-root-inputs` surface.
- [ ] T027 [US3] [blockedBy: T025] Convert the real-corpus consumers whose subject is the computed result (c10, c26, c27 and the `form_exit_code_table` payload leg) in `tests/contract/test_clause_coverage.py` to the session payload; keep `test_c20`'s byte-identity check cache-free (scan-cache C-006) and the `form_exit_code_table` subprocess exit-code leg (scan-cache C-008). [green: contracts/scan-cache.contract.md#C-005] [green: contracts/scan-cache.contract.md#C-006] [green: contracts/scan-cache.contract.md#C-008]
- [ ] T028 [US3] [blockedBy: T003, T026, T027] Run both corpus files before/after with `--full` and compare pass/fail names, then run the build-count/traversal probe; record `test-evidence/cache-counts.txt` and the equivalence names (land probe output outside `.specify/specs` during the run and copy afterwards — corpus-write hazard). [green: contracts/scan-cache.contract.md#C-009]
- [ ] T029 [US3] [blockedBy: T028] Run `tests/contract/test_scan_cache_contract.py` plus both converted files green and record the run. [green: contracts/scan-cache.contract.md#C-010] [green: contracts/scan-cache.contract.md#C-011]
- [ ] T030 [US3] [blockedBy: T029] Execute mutation drills CA-M1…CA-M5 on throwaway copies and record each red output in `test-evidence/cache-mutations.txt`.

**Checkpoint**: US3's independent criterion is the per-worker build count plus the equivalence pair; nothing in US1/US2/US4/US5 needs to be present.

---

## Phase 5: User Story 4 - 等待与顺序不再靠固定 sleep (Priority: P2)

**Goal**: Ordering determinism comes from the injected clock and explicit mtimes; completion waits observe events with an explicit deadline; the scope files carry zero synchronization `time.sleep`.

**Independent Test**: `bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_event_wait_contract.py -q` (S-6) proves the zero scan; `test_client_metrics.py` (S-7) is green with a smaller wall than its S-0.4 pre-change reading at equal worker count.

**Checkpoint**: US4 is independent — its only shared surface with other stories is `scripts/python/feedback-utils.py`, which nothing else in this feature edits.

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T031 [US4] Author the event-wait contract cases in `tests/contract/test_event_wait_contract.py`: the AST zero-synchronization-sleep scan over the event-wait C-001 scope files (naming file and line), the `wait_until` default assertions (`timeout == 30` — the enacted default, red against the measured pre-change 5.0 — `interval <= 0.2`), and the per-line exemption registry; record the red run in `notes/red-first-evidence.md`. [green: contracts/event-wait.contract.md#C-001] [green: contracts/event-wait.contract.md#C-003]

### Implementation for User Story 4

- [ ] T032 [US4] [blockedBy: T031] Add the optional `--now <YYYY-MM-DDTHH:MM:SSZ>` injected clock to `scripts/python/feedback-utils.py`, read by `now_iso()` (`:125`) and `timestamp_id()` (`:129`), documented in `--help`, default-off byte-identical, an unparsable value exits non-zero with a named error.
- [ ] T033 [US4] [blockedBy: T032] Regenerate the `scripts/` mirror pair with `python3 scripts/python/sync-mirrors.py --write --only scripts` and verify `--check` reports no NEW drift on `feedback-utils.py`.
- [ ] T034 [US4] [blockedBy: T032] Convert the eight ordering sleeps in `tests/contract/test_client_metrics.py` (lines 338, 391, 394, 400, 432, 458, 463, 671) to `--now`-injected timestamps plus explicit `os.utime` owner-file mtimes, keeping the assertion set unchanged (event-wait C-005). [green: contracts/event-wait.contract.md#C-004] [green: contracts/event-wait.contract.md#C-005]
- [ ] T035 [US4] [P] [blockedBy: T032] Replace the ordering sleep in `tests/contract/test_feedback_probe_cli.py` with the injected clock.
- [ ] T036 [US4] [P] [blockedBy: T032] Replace the two ordering sleeps in `tests/contract/test_store_state_protocol.py` with the injected clock.
- [ ] T037 [US4] Align the `wait_until` defaults in `tests/fixtures/line_fixtures.py:396` to `timeout=30` and `interval<=0.2`. [green: contracts/event-wait.contract.md#C-006] [green: contracts/event-wait.contract.md#C-007]
- [ ] T038 [US4] [blockedBy: T037] Replace the inline poll in `tests/integration/test_sdd_loop_efficiency_runner.py` with the shared `wait_until` (explicit 30 s deadline, 0.2 s interval, named failure on timeout).
- [ ] T039 [US4] [P] [blockedBy: T037] Replace the SIGHUP grace and post-exit residue waits in `tests/integration/test_session_kill_reattach.py` with event predicates over the observable file state.
- [ ] T040 [US4] [P] [blockedBy: T037] Replace the heartbeat first-write and advance waits in `tests/contract/test_line_envelope_contract.py` with event predicates. [green: contracts/event-wait.contract.md#C-008]
- [ ] T041 [US4] [blockedBy: T033, T034, T035, T036, T038, T039, T040] Run the guard and the six scope files green; record the `test_client_metrics.py` before/after wall pair (event-wait C-010) against `notes/pre-change-measurements.md` in `test-evidence/event-wait-green.txt`. [green: contracts/event-wait.contract.md#C-002] [green: contracts/event-wait.contract.md#C-009] [green: contracts/event-wait.contract.md#C-010]
- [ ] T042 [US4] [blockedBy: T041] Execute mutation drills EW-M1…EW-M5 on throwaway copies and record each red output in `test-evidence/event-wait-mutations.txt`.

**Checkpoint**: US4's independent criterion is the scan plus the green six-file run; the wall pair is directional evidence, never an assertion.

---

## Phase 6: User Story 5 - 非边界的引擎调用改为进程内直调 (Priority: P2)

**Goal**: Every `subprocess.run` site under `tests/` is classified; non-boundary engine/CLI calls run in-process with equivalent assertions; boundary subjects keep their subprocess; the manifest guard reddens on an unclassified site or a reverted conversion.

**Independent Test**: `bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_inprocess_conversion_contract.py -q` (S-8) green over the complete manifest; converting one point back to `subprocess.run` reddens and names it.

**Checkpoint**: US5 is independent — conversions touch test files only; its guard is the discriminating surface.

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T043 [US5] Author the in-process conversion contract cases in `tests/contract/test_inprocess_conversion_contract.py`: the AST census over `tests/**/*.py` and the read-only `tests/conftest.py`, manifest completeness against that denominator, the closed keep-class set, and the revert-red leg; record the red run in `notes/red-first-evidence.md`. [green: contracts/inprocess-conversion.contract.md#C-001] [green: contracts/inprocess-conversion.contract.md#C-002]

### Implementation for User Story 5

- [ ] T044 [US5] [blockedBy: T043] Add the generic in-process invocation helper to `tests/script_api.py` (importlib load, stdout/stderr capture, `main(argv)` exit code; `typer.testing.CliRunner` equivalent for the Typer CLI).
- [ ] T045 [US5] [blockedBy: T044] Generate `test-evidence/inprocess-conversion.md` from the AST census (one row per site: `file | call_site | verdict | boundary_class | reason`) and pilot-convert one contract file with local `_run` wrappers, recording before/after equivalence (FR-019). [green: contracts/inprocess-conversion.contract.md#C-003] [green: contracts/inprocess-conversion.contract.md#C-004] [green: contracts/inprocess-conversion.contract.md#C-005] [green: contracts/inprocess-conversion.contract.md#C-006]
- [ ] T046 [US5] [blockedBy: T045] Convert the contract-area engine group A (goal/flow/concurrency/confirmation engines) to in-process calls and fill their manifest rows.
- [ ] T047 [US5] [blockedBy: T045] Convert the contract-area engine group B (docs/probe/trigger/summary engines) and fill their manifest rows.
- [ ] T048 [US5] [blockedBy: T045] Convert the contract-area engine group C (mirror/measure/state engines) where non-boundary and fill their manifest rows.
- [ ] T049 [US5] [blockedBy: T046, T047, T048] Record the contract-area keep rows with boundary classes (fixture-layer `cwd=`/`env=` helpers, `copy-topology` cases) in `test-evidence/inprocess-conversion.md` (FR-027).
- [ ] T050 [US5] [blockedBy: T045] Convert the integration-area groups (docs-scenario and evidence-lane) non-boundary engine calls and fill their manifest rows.
- [ ] T051 [US5] [blockedBy: T045] Convert the unit-area engine-call group and fill their manifest rows.
- [ ] T052 [US5] [blockedBy: T049, T050, T051] Record the integration/unit keep rows, run the guard over the full manifest, fix every unclassified site and update the manifest evidence pointers. [green: contracts/inprocess-conversion.contract.md#C-007] [green: contracts/inprocess-conversion.contract.md#C-008]
- [ ] T053 [US5] [blockedBy: T052] Run the guard and the converted files green with equivalence evidence in `test-evidence/inprocess-equivalence.txt`. [green: contracts/inprocess-conversion.contract.md#C-009] [green: contracts/inprocess-conversion.contract.md#C-010]
- [ ] T054 [US5] [blockedBy: T053] Execute mutation drills IC-M1…IC-M5 on throwaway copies (including revert-one-converted-point red then restore) and record each output in `test-evidence/inprocess-mutations.txt`.

**Checkpoint**: US5's independent criterion is the closed manifest plus the equivalence pair; group file sets are proven disjoint by the manifest scan before any concurrent dispatch of T046–T048/T050/T051.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Measurement records, forbidden-shortcut and interface evidence, quickstart execution and the closure-stage handoff.

- [ ] T055 [P] Record the scope-disclosure reading from the slot-1 baseline (the pre-change default had the marked set merged, so its wall is a full-selection reading) in `test-evidence/tier-measurements.txt` — the default-vs-full wall difference is a selection difference, not an efficiency claim; no additional full run (FR-020).
- [ ] T056 [blockedBy: T003, T012] Measure the default tier's same-selection wall pair on the same host and day (S-13 legs 2–3: parallel vs `--serial`, tier unchanged; selection equality proven by the two `--collect-only` readings; targeted measurement per A9 — not a budget slot) and record both walls, their ratio, the excluded count and the default-vs-full raw walls as disclosure readings in `test-evidence/tier-measurements.txt`. [green: contracts/tier-selection.contract.md#C-016]
- [ ] T057 Run the SC-010 forbidden-shortcut diff scan (decorator and in-function `skip`/`xfail` forms, conditional skips, retry-until-green loops, parametrize removals) and record `test-evidence/forbidden-shortcuts.txt` (FR-021).
- [ ] T058 [P] Run the SC-011 interface evidence (S-11: `--help` lists `--full`, `--version` answers one line, an undeclared option exits non-zero) and record `test-evidence/interface-evidence.txt`.
- [ ] T059 [P] Write the `test-evidence/` index linking every SC-001…SC-011 to its evidence path(s), including this feature's coverage baseline and the closure records.
- [ ] T060 Run quickstart scenarios S-1…S-13 and record the real output (with teardown) in `notes/quickstart-run.md`; land run-time output outside `.specify/specs` and copy afterwards (corpus-write hazard).
- [~] T061 [blockedBy: T054, T060] Closure-stage row, executed by the driver after review (slot 2 of 2; handoff to the `closure` stage): run `bash scripts/bash/run-tests.sh --full --names-out .specify/specs/098-suite-speed-optimizations/final-failed.txt`, compare by name with `comm -13` against `baseline-failed.txt`, run the same-tree `--full --serial` validation run with the bidirectional name comparison, and record the full-tier wall ratio against the slot-1 baseline in `test-evidence/closure.txt` [green: contracts/parallel-consistency.contract.md#C-007] [green: contracts/parallel-consistency.contract.md#C-008] <!-- deferred: driver closure stage after review; slot 2 of 2 — not an implement-stage run -->

**Checkpoint**: All evidence lands; the closure-stage row remains `[~]` until the driver's closure stage executes it.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: starts immediately; T003 records slot 1 and every pre-change reading later rows diff against.
- **US1 (Phase 2)**: depends on T003 (red-first baseline context); blocks US2's tier-dependent runs.
- **US2 (Phase 3)**: T015/T016 read the post-US1 runner; T018–T020 are doc surfaces that only need `--full` to exist (T005).
- **US3 (Phase 4)**: independent of US1/US2; needs T003's pre-change names for its equivalence pair.
- **US4 (Phase 5)**: independent; its only engine edit is `feedback-utils.py` (T032).
- **US5 (Phase 6)**: independent; the manifest scan (T045) defines the group file lists before conversion rows.
- **Polish (Phase 7)**: T055–T059 after the mechanism stories; T060 after all stories; T061 last, executed by the driver at the closure stage.

### User Story Dependencies

- **US1 (P1)**: no dependency on other stories — MVP part 1.
- **US2 (P1)**: T015/T016/T022 run on the post-US1 runner; the parallel-consistency drill (T014/T017) has no US1 dependency — MVP part 2 alongside US1.
- **US3 / US4 / US5 (P2)**: each independent of the others and of US1/US2's implementation, sharing only the runner entry and the pre-change measurements.

### Within Each User Story

- Tests are authored and red before the behavior change (T004→T005, T024→T025, T031→T032, T043→T044); guards over existing behavior prove their discriminating power through the mutation rows.
- Every contract file's clauses are claimed by exactly one row (`[green:]`); a claim may sit out of clause order when the completing row is later (the guard-green row or the deferred closure row T061).

### Parallel Opportunities

- T002 can run beside T001/T003's recording work.
- T008 (pyproject) is independent of the runner edits.
- T018 and T019 edit disjoint reference files.
- T035, T036, T039, T040 touch four disjoint test files after T032/T037.
- T055, T058, T059 write disjoint evidence records.
- US3, US4 and US5 can be worked concurrently by different executors after Phase 2's runner mechanism lands; the conversion groups (T046–T048, T050, T051) become parallel-safe only once the manifest scan proves their file sets disjoint (decomposition §13).

---

## Parallel Example: User Story 4

```bash
# After T032 (injected clock) and T037 (helper defaults):
Task: "Replace the ordering sleep in tests/contract/test_feedback_probe_cli.py with the injected clock"
Task: "Replace the two ordering sleeps in tests/contract/test_store_state_protocol.py with the injected clock"
Task: "Replace the SIGHUP grace and post-exit residue waits in tests/integration/test_session_kill_reattach.py with event predicates"
Task: "Replace the heartbeat first-write and advance waits in tests/contract/test_line_envelope_contract.py with event predicates"
```

## Parallel Example: User Story 2

```bash
# Two disjoint budget surfaces, same change:
Task: "Add --full to the slot rows in skills/external/sdd-loop-driver/references/efficiency-model.md §2"
Task: "Add --full to the baseline/closure restatements in skills/external/sdd-loop-driver/references/stage-prompts.md"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 + US2 — the two same-priority (P1) stories together form the independently valuable increment: a faster default is only admissible when the full tier, the disclosed exclusion count and the two budget slots stay intact (Constitution XX: no speed bought by shrinking the selection). US1 alone delivers the fast default; US2 alone delivers the full-path integrity; each has its own checkpoint.

1. Complete Phase 1 (Setup) — slot 1 and the pre-change readings.
2. Complete US1 (T004–T013) → checkpoint: fast default + disclosure + registry guard.
3. Complete US2 (T014–T023) → checkpoint: full path + budget surfaces + parallel consistency.
4. **STOP and VALIDATE**: run S-1, S-2, S-3, S-4, S-9, S-12 for the MVP.
5. Then US3 → US4 → US5 (or concurrently by write domain), then Polish.

### Incremental Delivery

- US1 and US2 ship together as the MVP; US3, US4, US5 each add a measured saving with its own guard and can land in any order.
- No story ever changes the selection of another; the full tier and the two slots are the invariant.

### Work Package Mapping (plan.md § Work Packages → rows)

| Package | Rows | Package size |
|---------|------|--------------|
| WP-1 Runner tier mechanism | T004–T007, T011–T013 | 7 |
| WP-2 Slow registry and guard | T008–T010 | 3 |
| WP-3 Two-slot commands request the full tier | T018–T021 | 4 |
| WP-4 Parallel consistency verification | T014–T017, T023 | 5 |
| WP-5 Session scan cache | T024–T030 | 7 |
| WP-6 Clock injection and event waits | T031–T042 | 12 |
| WP-7 In-process infrastructure + contract-area groups | T043–T049 | 7 |
| WP-8 In-process integration/unit areas and evidence | T050–T054 | 5 |
| WP-9 Measurement, forbidden shortcuts, interface evidence | T003, T022, T055–T060 | 8 |
| Setup / closure handoff | T001–T002, T061 | 3 |

---

## Requirement Traceability

### Functional Requirements → Tasks

| FR | Tasks |
|----|-------|
| FR-001 | T004–T007, T012, T017 |
| FR-002 | T014–T017, T023, T061 |
| FR-003 | T015, T017, T061 |
| FR-004 | T016, T017 |
| FR-005 | T008, T010, T012 |
| FR-006 | T009, T013 |
| FR-007 | T004–T007, T012 |
| FR-008 | T005, T012 |
| FR-009 | T005, T012 |
| FR-010 | T018–T022, T061 |
| FR-011 | T003, T021, T022 |
| FR-012 | T024–T029 |
| FR-013 | T024, T025, T027, T029 |
| FR-014 | T024, T028–T030 |
| FR-015 | T031, T034–T036, T041 |
| FR-016 | T031, T037–T041 |
| FR-017 | T031, T041, T042 |
| FR-018 | T043–T053 |
| FR-019 | T043, T045, T049, T052–T054 |
| FR-020 | T003, T055, T056, T061 |
| FR-021 | T057 |
| FR-022 | T012, T017, T058 |
| FR-023 | T012, T021 |
| FR-024 | T009, T010, T012 |
| FR-025 | T025, T028, T029 |
| FR-026 | T031, T037–T041 |
| FR-027 | T043, T049, T052–T054 |

### Success Criteria → Tasks / Evidence

| SC | Tasks | Evidence path |
|----|-------|---------------|
| SC-001 | T003, T021, T022 | `test-evidence/full-collection-diff.txt` |
| SC-002 | T014–T017 | `test-evidence/parallel-consistency-contract.txt` |
| SC-003 | T061 | `test-evidence/closure.txt` |
| SC-004 | T055, T056 | `test-evidence/tier-measurements.txt` |
| SC-005 | T018–T020, T061 | `test-evidence/closure.txt` |
| SC-006 | T004, T009, T010, T012 | `test-evidence/tier-contract-green.txt`, `test-evidence/slow-members.md` |
| SC-007 | T028, T029 | `test-evidence/cache-counts.txt` |
| SC-008 | T041, T042 | `test-evidence/event-wait-green.txt` |
| SC-009 | T053, T054 | `test-evidence/inprocess-equivalence.txt`, `test-evidence/inprocess-mutations.txt` |
| SC-010 | T057 | `test-evidence/forbidden-shortcuts.txt` |
| SC-011 | T012, T058 | `test-evidence/interface-evidence.txt` |

---

## Mutation Leg Carriers

Each leg is exercised against a throwaway copy; the recorded red output is the proof the guard is a discriminator (never a green label).

| Leg | Guard row | Drill row |
|-----|-----------|-----------|
| TS-M1…TS-M8 | T004 / T010 / T021 | T013 |
| SL-M1…SL-M5 | T010 | T013 |
| PC-M1…PC-M5 | T014 | T023 |
| CA-M1…CA-M5 | T024 | T030 |
| EW-M1…EW-M5 | T031 | T042 |
| IC-M1…IC-M5 | T043 | T054 |

---

## Clause Attribution (renumbered 2026-11-10, analyze repair round)

This section replaces the former "Clause Attribution Deviation" record. At tasks generation the six `contracts/*.contract.md` files declared two-letter-prefixed clause ids that the framework's clause-syntax owner (`.specify/shared/definitions/contract-clause-definitions.md` § 1, form `C-<number>`) and its executable `scripts/python/clause_extract.py` could not parse (`md-none`). The analyze stage's Round-1 gate confirmed the defect (`clause-unparsable`, `fr-uncovered` 0/27) as W3-01.

The repair round executed the plan-owned remedy: every clause id in the six contract files was renumbered to the canonical `C-<three-digit>` form, every citation was updated (contracts, plan.md, quickstart.md, feature-ref.md and this file), and this file now emits one `[green:]` claim per clause (68 clauses, 68 claims; partition by row is in the table below). Machine readings after the repair:

- `python3 scripts/python/clause_extract.py`-based extraction reads all six files as `md-bold-closed` with 68 clauses (16/9/12/11/10/10).
- All 27 FRs are cited from clause citation groups (`fr-uncovered` 0/27).
- `validate-tasks.py` resolves every `[green:]` claim; the only warnings are out-of-order claims on rows whose completing moment is later (parallel-consistency C-007/C-008 at the closure row T061; scan-cache C-007 at the fixture row T025 before T027's C-005/C-006; event-wait C-002 at the guard-green row T041).

| Contract | Clause range | Claiming rows |
|----------|--------------|---------------|
| `tier-selection.contract.md` | C-001…C-016 | C-001…C-011 → T007; C-012…C-014 → T012; C-015 → T022; C-016 → T056 |
| `slow-membership.contract.md` | C-001…C-009 | C-001 → T008; C-002…C-004 → T009; C-005…C-009 → T010 |
| `parallel-consistency.contract.md` | C-001…C-012 | C-001…C-005 and C-009 → T014; C-006 → T015; C-010/C-011 → T016; C-012 → T017; C-007/C-008 → T061 |
| `scan-cache.contract.md` | C-001…C-011 | C-001…C-004 and C-007 → T025; C-005/C-006/C-008 → T027; C-009 → T028; C-010/C-011 → T029 |
| `event-wait.contract.md` | C-001…C-010 | C-001/C-003 → T031; C-004/C-005 → T034; C-006/C-007 → T037; C-008 → T040; C-002/C-009/C-010 → T041 |
| `inprocess-conversion.contract.md` | C-001…C-010 | C-001/C-002 → T043; C-003…C-006 → T045; C-007/C-008 → T052; C-009/C-010 → T053 |

## Notes

- Runtime evidence rule: while a corpus-scanning test is running, never write under `.specify/specs` (research B-5 / `test-evidence/corpus-write-hazard.txt`); run-time output lands outside the corpus and is copied afterwards.
- Two-slot budget: exactly two budget-slot full runs — slot 1 `baseline` at implement start (T003), slot 2 `closure` after review (T061). The closure stage adds one same-tree `--full --serial` validation run (T061) as validation evidence: it consumes no slot and no SC-004/SC-005 wall-clock reading (requirements A14); every other run in this file is a targeted run or a collection.
- Pre-existing failures are compared by name, never by count: `test_c5_gate_budget_is_unchanged_by_the_owner_document` and `test_c10_openapi_clauses_are_method_keys_and_the_total_matches_the_census` appear on both sides of every full-run comparison (research B-4).
- `[P]` means different write targets and no incomplete dependency; when in doubt, sequence with `[blockedBy:]` rather than assume disjointness.
- Prefer `[~]` over leaving a row `[ ]`: T061 is the only `[~]` row and it is a deliberate handoff to the driver's closure stage.
