# Verification — Feature 063

Evidence class labels: **automated** (CI test), **recorded trace** (non-CI
recording), **driver closure** (owned by the driver after review).

## T002 — implement-start full-suite baseline (only slot consumed in implement)

- State spine: `/tmp/sdd-loop-efficiency/state.md` (`spine_write_mode=direct`)
- E2 ledger fence position: `<!-- test-budget:begin -->` line 1 (`seq=1`, `slot=baseline`)
- Command: `bash scripts/bash/run-tests.sh --names-out .specify/specs/063-sdd-loop-efficiency/notes/baseline-failed-tests.txt`
- Result: `68 failed, 4115 passed, 1 skipped, 4 warnings in 397.21s`; exit `1`
- Failed-name list: `notes/baseline-failed-tests.txt` (68 entries)
- Full log: `/tmp/t002-full-suite.log`
- Failure surface: all 68 are pre-existing mirror-drift / frozen-count contract
  failures; none is in `test_sdd_loop_driver_skill.py` or
  `test_sdd_loop_driver_cli_profiles.py`.
- `baseline_slot=consumed`; closure is driver-owned after review; implement ran
  no second full suite.
- E3 reference copy: `test-evidence/implement.jsonl` carries one legal row that
  references the E2 row; it is a transport/evidence copy, never the ledger.

## T001 — pre-change measurements and SC-010 baseline

- Measurements: `notes/pre-change-measurements.md` (+ raw outputs `notes/baseline-*.txt`)
- SC-010 baseline: `notes/stall-behavior-baseline.json`, `base_commit=a1aac7e5`,
  `initial_retries=0`, recorded before the first behavior-face commit; replay
  pre-check on the current tree: zero differences.

## US1 — fast lane (T008–T015)

### T008/T010 — admission-check unit suite (automated)

- Red: `notes/red-first-evidence.md` § T008 (23 failed, script absent).
- Green: `bash scripts/bash/run-tests.sh tests/unit/test_admission_check.py -q` → `23 passed`.
- Script: `skills/external/sdd-loop-driver/scripts/admission-check.py`; constants
  `FR_MIN=8 / FR_MAX=30 / TASK_MIN=10 / TASK_MAX=40`; exit codes 0/1/2; stdlib only.

### T009/T011 — FL clauses and owner document (automated)

- Red: `notes/red-first-evidence.md` § T009 (10 failed).
- Green (T013 combined run): `tests/unit/test_admission_check.py tests/contract/test_sdd_loop_driver_efficiency.py -q` → `33 passed`.
- Owner document: `skills/external/sdd-loop-driver/references/efficiency-model.md` §1.
- Downstream: `references/dispatch-recipes.md` Recipe 4 admission point + reversion;
  `references/stage-prompts.md` § Fast Lane Conditional Blocks.
- FR-042(a) script-side: S1/S2 show admission and refusal; the stage-sequence part
  is recorded in the S7 dry-run trace (T051).

### T012 — mirror parity (automated)

- `sync-mirrors.py --write --only skills/external/sdd-loop-driver` → 2 new + 2 updated.
- `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` → exit 0.
- `sync-mirrors.py --check --only skills/external/sdd-loop-driver` → `ok (17 files)`, exit 0.
- Existing C-12/C-18 (mirror drift) remain green; `test_sdd_loop_driver_skill.py` was
  23/23 green at T001.

### T013 — targeted green + quickstart S1/S2

- `bash scripts/bash/run-tests.sh tests/unit/test_admission_check.py tests/contract/test_sdd_loop_driver_efficiency.py -q` → `33 passed in 85.74s`, exit 0.
- Quickstart S1: exit 0, `fast-lane`, 12/25, seven pass. S2: exit 1, `full-chain`, 60 tasks, criterion a fail. Details in `notes/quickstart-run.md`.
- Narrow-mode admission: S1/S2 and `test_narrow_task_pattern_only_for_admission`; wide mode is repository bookkeeping only.
- SC-001/SC-002 automated evidence: unit + FL tests + S1/S2.

### T014 — mutation drill (5 applications, all restored)

| Mutation | Red test | Restore |
|----------|----------|---------|
| FR_MAX 30→31 | `test_task_count_boundary_edges[31-40-False]` | checksum equal |
| count SC rows as FR | `test_fr_count_excludes_sc_rows` | checksum equal |
| remove (c)/(d) scans | `test_sensitive_or_engine_path_rejected` | checksum equal |
| accept multi-record manifest | `test_lines_manifest_syntax_pinned[two records]` | checksum equal |
| use wide task mode for admission | `test_narrow_task_pattern_only_for_admission` | checksum equal |

### T015 — post-mutation re-run

- Mirror re-sync + `diff -rq` exit 0 + `--check` exit 0.
- `33 passed in 121.09s`, exit 0; quickstart S1/S2 re-run with the same expectations.
- `git diff` contains only the feature's expected paths (implementation + mirrors + tests + spec notes).

## US2 — two-slot budget and targeted evidence (T016–T024)

### T016/T017/T018 — red-first (automated)

- Red: `notes/red-first-evidence.md` § T016/T017/T018 (script absent; 22 unit
  failures, 1 integration failure, 10 TB contract failures).
- Green (T022 combined run): `tests/unit/test_audit_test_budget.py
  tests/integration/test_sdd_loop_efficiency_regression.py
  tests/contract/test_sdd_loop_driver_efficiency.py -q` → `43 passed in 4.50s`.
- Script: `skills/external/sdd-loop-driver/scripts/audit-test-budget.py`;
  ledger authority = the `<!-- test-budget:begin/end -->` fence in the state
  spine; `test-evidence/` is E3 only (`test_ledger_reads_state_spine_fence`).

### T020/T021 — owner document, prompts, recipes, mirror (automated)

- `references/efficiency-model.md` §2 (two slots, targeted-set-v1, E3 fields,
  audit/exceptions, completeness `stages=N complete=N`, orchestration layer).
- `references/stage-prompts.md` budget blocks (implement baseline, intermediate
  and review targeted runs, driver closure, `baseline_slot=skip(closure-repair)`,
  `STATE_SPINE_PATH`/`EVIDENCE_DIR`/`SPINE_WRITE_MODE` placeholders).
- `references/dispatch-recipes.md` Recipe 4 closure timing + audit command.
- Mirror: `sync-mirrors.py --write --only skills/external/sdd-loop-driver` →
  1 new + 3 updated; `diff -rq` exit 0; `--check --only ...` → `ok (18 files)`.

### T022 — live ledger and quickstart S3 (automated + recorded)

- Quickstart S3: exit `0`, `slots=baseline:1 closure:1 reruns=0 exceptions=0
  unknown=0`, `stages=0 complete=0`, `status=ok` (details in
  `notes/quickstart-run.md`).
- Live 063 spine (`/tmp/sdd-loop-efficiency/state.md`):
  `audit-test-budget.py --spine ... --spec-dir .specify/specs/063-sdd-loop-efficiency
  --stage-check implement` → exit `0`, `slots=baseline:1 closure:0 ...`,
  `stages=0 complete=0`. `baseline_slot=consumed`; closure remains driver-owned
  after review. Implement ran no second full suite.
- E2 fence is the only ledger; `test-evidence/implement.jsonl` carries one E3
  reference row and is never audited as a ledger (I-05).

### T023 — mutation drill (5 applications, all restored)

| Mutation | Red test | Restore |
|----------|----------|---------|
| allow a third slot | `test_third_slot_rejected` | checksum equal |
| missing `exception_reason` passes | `test_out_of_slot_without_exception_fails` | checksum equal |
| count comparison replaces name-level diff | `test_closure_requires_name_level_diff` | checksum equal |
| ignore `--logs-dir` scan hits | `test_unaccounted_log_full_run_rejected` (+ `test_missing_logs_reports_unknown`) | checksum equal |
| drop docs-only reduced-field / completeness checks | `test_docs_only_reduced_field_set` | checksum equal |

### T024 — post-mutation re-run (automated)

- `43 passed in 4.50s`, exit 0; quickstart S3 re-run identical.
- Ledger still reports exactly two slots, 0 exceptions, 0 unknown; no second
  full suite ran inside implement.
- US2 checkpoint closed.

## US3 — plan minor-fix constraint (T025–T032)

### T025/T026 — red-first (automated)

- Red: `notes/red-first-evidence.md` § T025 (8 failed, script absent) and § T026
  (9 PC failures).
- Green (T030 combined run): `tests/unit/test_audit_plan_changes.py
  tests/contract/test_sdd_loop_driver_efficiency.py -q` → `39 passed`.
- Script: `skills/external/sdd-loop-driver/scripts/audit-plan-changes.py`;
  bare artifact names (`plan.md`, `contracts`) resolve to any matching
  repo-relative path; final `diff_stats` uses `git diff --numstat <base>` so
  accumulated edits are judged on the cumulative diff; the script is read-only.

### T028/T029 — owner document, prompts, recipes, mirror (automated)

- `references/efficiency-model.md` §3 (activation state, minor/substantive
  definitions, `PLAN-EDIT:` format owner, U4 diff check, two branches with the
  latest `approved_baseline_commit`, re-anchoring, re-entry restore, exclusion).
- `references/stage-prompts.md` plan-constraint block (tasks/analyze/implement/
  review; `PLAN-EDIT:` + `ANOMALY:`); `references/dispatch-recipes.md` Recipe 4
  registration, U4 classification/routing and re-entry restore.
- Mirror: 1 new + 3 updated; `diff -rq` exit 0; `--check --only ...` →
  `ok (19 files)`.

### T030 — quickstart S6 (automated + recorded)

- Exit `1`, `touched_paths=[".specify/specs/012-medium/plan.md"]` (the sole
  artifact is `plan.md`), `undeclared=true`, `classification=undeclared`,
  `diff_stats` added 2. The driver fails the gate before PC-06 routing.
  Details in `notes/quickstart-run.md`.

### T031 — mutation drill (3 applications, all restored)

| Mutation | Red test | Restore |
|----------|----------|---------|
| ignore uncommitted changes | `test_uncommitted_plan_change_included` | checksum equal |
| empty declarations still declared | `test_undeclared_plan_change_flagged` | checksum equal |
| ignore the new anchor after re-baseline | `test_pc_11_reanchoring` | checksum equal |

- The PC-11 pin was strengthened to the exact latest-anchor sentence
  (`此后一律使用**最新**锚点`) after the first attempt did not turn red.

### T032 — post-mutation re-run (automated)

- `39 passed in 20.46s`, exit 0; quickstart S6 re-run identical.
- `PLAN-EDIT:` format owner, two-branch routing and the framework-internal
  explicit exclusion are visible in the owner document and prompts.
- US3 checkpoint closed.

## US4 — stream progress and detached runner (T033–T043)

### T033/T034/T035 — red-first (automated)

- Red: `notes/red-first-evidence.md` § T033 (8 failed), § T034 (7 failed,
  runner absent), § T035 (10 PD failures).
- Green (T041): `tests/unit/test_derive_live_log.py
  tests/integration/test_sdd_loop_efficiency_runner.py
  tests/contract/test_sdd_loop_driver_efficiency.py -q` → `57 passed in 13.48s`.

### T036/T037/T038 — derivation, runner, watcher (automated)

- `derive-live-log.py`: incremental prefixed progress lines with `evt=`/`at=`,
  terminal `result` text appended verbatim at EOF, `--finish` recovery,
  malformed input tolerated without fabricated completion.
- `stage-runner.sh`: auto probe and `--output-format stream-json` pipeline,
  raw + receive-timestamp sidecar, derived live log, four-piece set + runner
  log, `exit/sentinel/progress/detached` status (with `unprotected=true` and
  risk reason for `--detached no`), exit code = CLI rc, degradation chain
  (`cli-lacks-stream` → `derivation-recovered` → `buffered-fallback` →
  `sentinel=0`).
- `watch-target.sh`: `--raw-stream` visibility (`stream=na|absent|growing|idle`,
  `raw=`/`bytes=` on EVIDENCE, never a verdict input); four stream self-tests
  plus a `stream-progress-not-done` sub-check. Self-test: `33 passed, 0 failed`
  (28 historical + 4 stream cases + the progress sub-check; no case deleted).

### T039/T040 — owner document, recipes, prompts, mirror (automated)

- `references/efficiency-model.md` §4; `watch-model.md` §2/§3/§4/§10 progress,
  degradation and raw evidence (verdict table unchanged); Recipe 2 switched to
  `stage-runner.sh` (old `sed` form explicitly superseded); Recipe 3/5 nohup
  forms and `detached` recording; stage-prompts progress/detach/re-entry blocks.
- Mirror: 7 changed (2 new scripts); `diff -rq` exit 0; `--check --only ...` →
  `ok (21 files)`; new scripts keep the executable bit in the mirror.

### T041 — live runs and quickstart S4/S5 (automated + recorded)

- S4a: INCOMPLETE (15), last line is a prefixed progress line; S4b: DONE (0)
  from the terminal result. S5: `status` has `exit=0 sentinel=1 progress=stream
  detached=yes`, live log ends `PLAN-DONE`, raw/sidecar 4/4 lines; `--once`
  re-entry returns DONE without redispatch. Details in `notes/quickstart-run.md`.
- SC-008/009/011 automated evidence: runner integration + derive unit +
  watcher self-tests; `--once` re-entry in
  `test_once_snapshot_does_not_redispatch`.

### T042 — mutation drill (8 applications, all restored)

| Mutation | Red test | Restore |
|----------|----------|---------|
| non-terminal events emit a bare sentinel | `test_non_terminal_sentinel_not_bare_last_line` | checksum equal |
| result text written before progress lines | `test_terminal_result_appended_verbatim` (+ incremental pipe) | checksum equal |
| delete result extraction | `test_terminal_result_appended_verbatim` | checksum equal |
| force buffered even when stream is available | `test_auto_selects_stream_when_cli_advertises_capability` | checksum equal |
| skip status write | `test_stream_mode_writes_raw_and_live` | checksum equal |
| drop the detached record | `test_status_fields_and_exit_code_propagation` | checksum equal |
| progress growth produces DONE | `stream-progress-not-done` (self-test) | checksum equal |
| read the sentinel from raw | `stream-progress-not-done` + `stream-nonterminal-sentinel` | checksum equal |

### T043 — post-mutation re-run (automated)

- `57 passed in 13.48s`, exit 0; watcher self-test `33 passed, 0 failed`;
  quickstart S4/S5 re-run identical. No self-test case was removed by the
  repairs. US4 checkpoint closed.
