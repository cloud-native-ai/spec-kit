# Verification — 070-subagent-task-teams

**Status**: partial (segments S1–S5; T001–T030). The SC-001…SC-008 matrix, the closure full suite, the mirror check, and the final task audit are completed by the final implement segment (T039). This file exists early only to record residual interpretations and in-segment verification facts the dispatch requires.

## US4 verification (impl-s5; T024–T026)

- **Scope**: stage-team preset, seat mapping, graph-derived pattern, run-scoped adapter, and no persisted team (ST-01…ST-12).
- **Command**: `python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_preset.py tests/integration/test_wp_coordination_dry_runs.py` → `27 passed in 0.12s`, rc 0 (14 preset contract + 13 dry runs).
- **Red-to-green**: T024 preset `13 failed, 1 passed` (the pass is the anti-drift ST-10 pin) and the no-team dry run `1 failed` (missing `adapt_stage_team`); T025 implementation → 14 preset cases green; T026 combined run green.
- **Scenario G (no-team half)**: `python3 -m pytest -q tests/integration/test_wp_coordination_dry_runs.py -k "nested_driver or no_team_directory"` → `2 passed`.
- **No-team evidence**: `test_no_team_directory_is_created` compares the repository `.specify/teams/` tree and a temporary project root before and after the adapter projection plus a simulated stage; both are unchanged and no `team.md` appears.
- **Interpretation**: the adapter is a pure projection in the test-only simulator (`stage_team_pattern`, `adapt_stage_team`); the live adapter writes the same fields into the plan fence as driver prompt logic. `parallel` requires at least two independent packages with every package read-only; any `repair_loop` selects `iteration`; `continuous` is unrepresentable.
- **Evidence**: `notes/red-first-evidence.md` §T024–§T026; `test-evidence/implement-stage-status.jsonl` row `impl-s5-us4-preset`.

## US5 verification (impl-s5; T027–T030)

- **Scope**: report derivation, OR-04…OR-13 metrics, `not_evaluated`, stage-close/retry accounting, and the no-raw-transcript rule.
- **Command**: `python3 -m pytest -q tests/unit/test_wp_report.py` → `19 passed in 0.81s`, rc 0.
- **T029 anchor pair**: `python3 -m pytest -q tests/unit/test_wp_report.py tests/contract/test_sdd_loop_driver_wp_model.py` → `76 passed in 2.29s`, rc 0 (19 report + 57 model).
- **Red-to-green**: T027 `19 failed` on the missing script (the first run's accidental rc-2 pass was removed by asserting script existence); T028 implementation → all 19 green.
- **Scenario E (literal run)**: fixture spine `/tmp/wp-demo-e/state.md` (line `line`, two packages) with `--stage-u4-at 1790000300 --manual-interventions 0 --sessions 1` → rc 0; `line-plan-a1-coordination.md/.json` written; `wall_clock_seconds=200`, `critical_path_seconds=130`, `parallelism_efficiency=0.575`, `max_concurrent=2`, `overlap=true`, `stage_executions_per_canonical=0.125`, rate `0.0`.
- **Deleted-timestamp variant**: after removing `plan-wp02`'s settle `ended_at`, `wall_clock_seconds=200` while `critical_path_seconds`, `parallelism_efficiency`, and `max_concurrent` are the literal `"not_evaluated"` (not zero).
- **Missing-session variant**: `manual_interventions=0` is reported while `sessions` and `manual_interventions_per_session` are `"not_evaluated"`.
- **Evidence**: `notes/red-first-evidence.md` §T027–§T030; `test-evidence/implement-stage-status.jsonl` row `impl-s5-us5-report`.

## US5 interpretation notes (flagged for review)

### E11/OR-07 stage-attempt numerator is run-level

- **Interpretation**: `stage_attempts` counts the distinct `(stage, stage_attempt)` pairs that dispatched at least one package **in the run**, per V-CLOSE.3, OR-07's numerator, and SC-002 (which is a run-level rate). The phrase "for the stage in the run" in the E11 field row is read as "in the run's stage chain", not "restricted to the reported stage attempt"; a single-stage fixture therefore reports `1/8 = 0.125`.
- **Where**: `skills/external/sdd-loop-driver/scripts/wp-report.py` (`_stage_attempt_pairs`, `build_report`).
- **Tests**: `tests/unit/test_wp_report.py::test_report_stage_executions_ignore_plan_repairs_and_package_retries`, `test_report_stage_executions_include_a_reentered_stage_attempt`.
- **Review at**: T039 closure (no contract edit; the normative V-CLOSE.3/SC-002 reading wins over the ambiguous projection phrase).

### Settle/verdict pairing when E4 omits the stage attempt

- **Interpretation**: E4's `settle` and `verdict` events carry no `stage_attempt`, so the report pairs each with the oldest unpaired `dispatch` record of the same `wp_id` in ledger order. Because the ledger is append-only, this reconstructs the producing attempt; a split child is a distinct `wp_id`.
- **Where**: `skills/external/sdd-loop-driver/scripts/wp-report.py` (`_attempt_records`).
- **Tests**: `test_report_retry_counts_package_and_stage_separately` and the US5 report suite.
- **Review at**: T039 closure.

### Concurrency sweep vs efficiency numerator

- **Interpretation**: the OR-06 sweep uses every resolved executor interval in the stage attempt (including a failed attempt before its retry), while the efficiency numerator uses each package's verified attempt duration (OR-05's "the verified attempt supplies the duration"). Verifier executions are excluded from both.
- **Where**: `skills/external/sdd-loop-driver/scripts/wp-report.py` (`_max_concurrent`, `_parallelism_efficiency`).
- **Tests**: the US5 report suite (`test_report_parallelism_efficiency_puts_the_product_in_the_denominator`, `test_report_max_concurrent_and_overlap_flag_detect_real_overlap`).
- **Review at**: T039 closure.

### Stage U4 fallback input

- **Interpretation**: `--stage-u4-at` wins; when absent, the report reads the recorded `stage-close` event's `stage_u4_at` for the same stage attempt; otherwise `wall_clock_seconds` is `not_evaluated` (OR-04/OR-11). The report never infers U4 from commit timestamps.
- **Where**: `skills/external/sdd-loop-driver/scripts/wp-report.py` (`build_report`).
- **Tests**: `test_report_stage_close_supplies_the_u4_time_after_close`.
- **Review at**: T039 closure.

## US3 verification (impl-s4; T020–T023)

- **Scope**: independent verification and integration, VI-01…VI-14.
- **Command**: `python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_coordination.py tests/integration/test_wp_coordination_dry_runs.py` → `79 passed in 0.24s`, rc 0.
- **Red-to-green**: T020 `18 failed, 15 passed`; T021 `6 failed`; T022 implementation → all green.
- **Quickstart Scenario D**: `python3 -m pytest -q tests/unit/test_wp_gate.py -k "retry"` → `28 passed`; dry-run dependency/escalation cases → `2 passed`.
- **Quickstart Scenario F — recorded reason**: decision resolution and the single-package/fallback runs are owned by FN-01…FN-08 with green points T034/T035 (US5), outside the T020–T023 scope; no VI clause depends on the decision resolver. Scenario F remains open until T035.
- **Evidence**: `notes/red-first-evidence.md` §T020–§T023; `test-evidence/implement-stage-status.jsonl` row `impl-s4-us3-verification`.

## Analyze residual interpretations (flagged for review)

### R2-04 — OR-14 retry counting for split children

- **Interpretation**: `wp-gate.py --check retry` derives a split child's lineage attempt as `parent_dispatch_count + 1`, per FR-013, A4, WG-17, and OR-15. The stale OR-14 per-`wp_id` event-count sentence is not used for children. A child dispatch numbered 1 is `retry-delta-invalid`; a child's own prior dispatch, a further child attempt, or a proposed split of a child is `retry-exhausted`.
- **Where**: `skills/external/sdd-loop-driver/scripts/wp-gate.py` (`_retry_findings`).
- **Test pins**: `tests/unit/test_wp_gate.py::test_retry_split_parent_admits_the_retry_attempt`, `test_retry_split_child_inherits_the_parent_attempt`, `test_retry_split_child_attempt_one_is_invalid`, `test_retry_split_child_further_attempt_is_exhausted`, `test_retry_split_of_a_child_is_exhausted`.
- **Review at**: T039 closure (R2-04 is non-blocking under the analyze-rerun gate).

No other analyze residual (R2-01, R2-02, R2-03, R2-05, R2-06) is relied on by an implementation path in T014–T023; the normative clauses are followed directly. US3 follows VI-06 and WG-08 for the integrator carve-out, so the stale `V-WP.6` projection (R2-01) is not used.
