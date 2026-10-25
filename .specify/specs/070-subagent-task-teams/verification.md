# Verification — 070-subagent-task-teams

**Status**: implementation complete (T001–T039); a **user waiver for SC-001/SC-002 is recorded** (`notes/waiver-070.md`, 2026-10-25), so the closure gate is no longer blocked. The post-review closure full suite reports **18 failed / 5674 passed / 1 skipped with 0 new name-level failures** against the 19-failure / 5341-passed baseline, and the test-budget audit reports `status=ok`. The feature is merged at `ca8040f5` (fast-forward; no push; worktree retained). SC-001 and SC-002 remain `not_evaluated` and are waived, not met; SC-006 remains `not_evaluated`. See § Closure outcome (post-review).

## Entry surface and opt-out/fallback verification (impl-s6; T031–T035)

- **Scope**: the intentional SKILL H2 pin update and entry section, the pointer-only docs section, the 058/063/064/067/068 non-regression net, the FN-01…FN-16 opt-out/fallback cases, and the runtime-owner §20/§21 sections plus the simulator decision procedure.
- **Commands and results**:
  - `python3 -m pytest -q tests/contract/test_sdd_loop_driver_skill.py -k "not c18"` → `24 passed, 1 deselected in 14.97s`, rc 0.
  - `python3 -m pytest -q tests/contract/test_non_regression_070.py` → `10 passed in 0.04s`, rc 0.
  - `python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_coordination.py tests/integration/test_wp_coordination_dry_runs.py` → `130 passed in 0.34s`, rc 0 (44 FN + 34 SD + 33 VI contract cases, 19 dry runs).
  - Full 070-targeted audit (eight files) → `324 passed in 5.98s`, rc 0.
- **Red-to-green**: T031 `1 failed, 24 deselected` (missing H2); T034 `34 failed, 19 passed, 77 deselected` (missing decision procedure and §20/§21; the 16 clause pins and 3 pre-existing fallback cases are disclosed anti-drift passes); T035 → all green.
- **Non-regression evidence**: `test-evidence/non-regression-070.txt` records the 10-case green run and the owner-agreement result (5 mirror rows only in plan.md, 4 inventory rows only in data-model.md, additive-only section sets).
- **Pre-T037 disposition**: `SKILL.md` was edited in T032, so `test_c18_mirror_pair_no_drift` fails on the source/mirror byte pair until T037 runs `sync-mirrors.py --write`. No mirror file was hand-edited. This is the only deselected/failing pre-existing surface in this segment and is not a name-level regression against the E2 baseline.

### Interpretations (flagged for review)

- **Explicit `on` versus `auto` benefit**: FN-04's benefit test is scoped to `auto` by WG-13. An explicit stage `on` bypasses that test but still requires a gate `admit` and at least two packages (V-PLAN.2); a one-package `on` stage resolves to `single-package` with `reason=not-beneficial`. The simulator encodes this in `decide_stage_decomposition`.
- **Unrepresentable contract reason**: FN-06 names three fallback causes and the model (§8, E13) forces the single-package fallback when a required inventory item cannot be represented. That path records `decision=fallback` with `reason=not-beneficial` and the finding `unrepresentable-contract`; it is not a gate reject.
- **No-partial representation**: a non-decomposed decision keeps `attempted_packages` for evidence and `dispatched_packages=[]`. WP-13's sole package is the stage execution itself, so the standard path reports `packages_dispatched=[]` (no *package* dispatch) while running one unchanged stage execution.
- **Declaration validation**: the test-only resolver rejects unknown stages, modes outside `auto|on|off`, and a non-positive/non-integer slot cap rather than coercing them. This is boundary validation inside the simulator, not a new command argument; the live driver records the same fields in the spine.
- **R2-03 residual**: the `disabled` resolution follows V-DEC.5 / FN-03 / FN-08 (feature-level `off`), not the narrower state-table trigger projection; no plan-owned artifact was changed.

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

## T036–T038 verification (impl-s7)

- **T036 mutation drills**: `python3 -m pytest -q -s tests/contract/test_wp_mutation_drills.py` → `4 passed in 4.09s`, rc 0. Each drill runs a control (unmutated copy, `1 passed`) and a mutant (cycle check removed, write-alone removed, missing verdict treated as pass, `not_evaluated` replaced by zero), each of which turns the selected contract/unit test red on an assertion. Details: `notes/red-first-evidence.md` §T036.
- **T037 mirror sync**: `sync-mirrors.py --write` synced five files; `--check` → `ok skills/external/ == .specify/skills/ (32 files)`, rc 0; all five `cmp` pairs identical. `32 = 28-file baseline + 4 planned new files`, zero NEW drift. `test_sdd_loop_driver_skill.py -k c18` → `1 passed`. Details: `notes/pre-change-measurements.md` §T037.
- **T038 quickstart**: Scenarios A–G all ran with the recorded rc; A `admit` rc 0, B `reject` rc 1 with `cycle`/`orphan-output`/`path-overlap`, C `2 passed`, D `retry-unchanged` rc 1 → split `admit` rc 0 → `retry-exhausted` rc 1, E metrics and both `not_evaluated` variants rc 0, F `19 passed`, G `3 passed`; fixture workspace removed (`TEARDOWN_OK`). Details: `notes/quickstart-run.md`.
- **T038 benchmark**: `not_evaluated` — zero comparable samples, no run record for driver sessions or manual interventions. SC-001/SC-002 must not be marked met. Details: `notes/benchmark-070.md`.

## Closure verification (T039)

- **Segment**: impl-s7, 2026-10-25T07:57Z.
- **Budget disposition**: the impl-s7 mandatory test budget authorises all new
  unit/contract/integration suites plus `validate-tasks`, and explicitly defers
  the full-suite closure slot to the driver after review. The E2 baseline
  (`baseline-failed.txt`, T002) is unchanged and is not re-run here.

### Checks run

| Check | Command | Real output | rc |
|---|---|---|---|
| All new 070 suites | `python3 -m pytest -q tests/unit/test_wp_gate.py tests/unit/test_wp_report.py tests/contract/test_sdd_loop_driver_wp_model.py tests/contract/test_sdd_loop_driver_wp_gate.py tests/contract/test_sdd_loop_driver_wp_coordination.py tests/contract/test_sdd_loop_driver_wp_preset.py tests/contract/test_non_regression_070.py tests/contract/test_wp_mutation_drills.py tests/integration/test_wp_coordination_dry_runs.py` | `328 passed in 10.04s` | 0 |
| Skill contract incl. the 070 H2 pin and mirror pair | `python3 -m pytest -q tests/contract/test_sdd_loop_driver_skill.py` | `25 passed in 15.98s` | 0 |
| Existing driver targeted regression (same set as the T001 baseline) | `python3 -m pytest -q tests/unit/test_decomposition_check.py tests/unit/test_pre_analyze_check.py tests/unit/test_overlap_check.py tests/contract/test_sdd_loop_driver_gates.py tests/contract/test_sdd_loop_driver_skill.py` | `65 passed in 18.04s` (identical to the T001 `65 passed`) | 0 |
| Task file validity | `python3 scripts/python/validate-tasks.py .specify/specs/070-subagent-task-teams/tasks.md` | `PASS — 0 error(s), 0 warning(s)` | 0 |
| Clause coverage (110 ids) | corrected loop over non-comment inventory lines against the four contract test files (`test-evidence/final-clause-coverage.txt`) | `checked=110 missing=0` | 0 |
| Mirror pair | `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` | `ok skills/external/ == .specify/skills/ (32 files)` | 0 |
| Cross-artifact consistency | `python3 /home/agent/sdd-070/tools/pre-analyze-check.py --spec-dir .specify/specs/070-subagent-task-teams --stage tasks --repo .` | `decision=pass errors=0 advisories=0 waived=0`; fr 30 / sc 8 / tasks 39 / clauses 110 | 0 |
| Decomposition size gate | `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/070-subagent-task-teams/requirements.md --tasks .specify/specs/070-subagent-task-teams/tasks.md` | `decision=proceed`, `task_count=39` (ceiling 40) | 0 |
| Unfinished rows | `grep -cE '^- \[[ >]\]' .specify/specs/070-subagent-task-teams/tasks.md` | `0` after T039 is marked | 0 |

**Clause-coverage repair (in-scope, test-documentation only)**: the first
corrected T039 loop found seven ids whose literals were absent from the four
contract test files (`WG-02`, `WG-03`, `WG-04`, `WG-14`, `WG-15`, `WG-17`,
`WG-18`). Their behavioural pins already existed in
`tests/unit/test_wp_gate.py` and `tests/contract/test_sdd_loop_driver_wp_coordination.py`;
T039 added a clause-to-test mapping block to the
`tests/contract/test_sdd_loop_driver_wp_gate.py` docstring (the same pattern
used for WG-06…WG-13 at T011). No assertion, behaviour, or contract text
changed. After the repair the loop reports `checked=110 missing=0`.

**Inventory-form disclosure**: the literal `for id in $(cat ...)` form in the
T039 row still fails on the inventory's `#` header (it stops at the header word
`frozen`). The T001/T003 disclosure already requires T039 to read non-comment
lines, which the command above does; the 110 id rows themselves are unchanged.

### Deferred closure slot (driver, after review)

Not run in impl-s7 by the mandatory test-budget instruction:

```sh
bash scripts/bash/run-tests.sh --names-out .specify/specs/070-subagent-task-teams/final-failed.txt
comm -13 .specify/specs/070-subagent-task-teams/baseline-failed.txt \
  .specify/specs/070-subagent-task-teams/final-failed.txt
```

The closure gate requires the second command to return empty (zero NEW
name-level failures) before any closure handoff. Until it runs, DoD-7 remains
open.

### SC-001…SC-008 evidence matrix

- **SC-001**: **Status = `waived` (user, 2026-10-25).** Criterion: stage
  wall-clock ≤ 80% of the dated anchor, median over at least three comparable
  samples. Metric/command: `notes/benchmark-070.md` (no comparable driver run
  exists, so no median is computable). Output: 0 samples,
  `median=not_evaluated`. Waived by the user via `notes/waiver-070.md` because
  the mechanism, functional behaviour, and all quality gates are verified
  while a comparable benchmark is deferred; the criterion is **not** claimed
  met.
- **SC-002**: **Status = `waived` (user, 2026-10-25).** Criterion: stage
  executions per canonical stage ≤ 1.5 and ≥40% below 2.6×. Metric/command:
  `notes/benchmark-070.md` (no run-level `(stage, stage_attempt)` chain exists).
  Output: `not_evaluated`; Scenario E's fixture `0.125` is a derivation test,
  not a benchmark. Waived by the user via `notes/waiver-070.md` (same reason);
  the criterion is **not** claimed met.
- **SC-003**: **Status = `met` (closure 18 failed / 0 new; gate suites green).**
  All targeted new and existing-driver suites are green, and the post-review
  closure full suite reports `18 failed / 5674 passed / 1 skipped` against the
  19-failure / 5341-passed baseline with zero name-level additions
  (`comm -13` empty). Command: the 070 suite (`328 passed`), the existing
  driver targeted suite (`65 passed`, identical to T001), the skill contract
  (`25 passed`), the mirror check (`ok`, 32 files), the non-regression net
  (`10 passed`), and the closure full suite. Output: zero new failures.
- **SC-004**: **Status = `met` (targeted).** Criterion: every required output
  is owned; zero orphan or cross-territory outputs/writes. Command:
  `python3 -m pytest -q tests/unit/test_wp_gate.py -k "orphan or duplicate_output or integrator_output or write_write or read_write"`.
  Output: `7 passed, 76 deselected`; also covered by the 328-test run.
- **SC-005**: **Status = `met` (targeted).** Criterion: every stage records a
  decision with its gate verdict and reason. Command:
  `python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_coordination.py tests/integration/test_wp_coordination_dry_runs.py -k "fn_05 or fn_08 or single_package or disabled_stage"`;
  Scenario F. Output: `4 passed, 126 deselected`; Scenario F `19 passed`.
- **SC-006**: **Status = `not_evaluated`.** Criterion: manual interventions per
  session ≤ 30/29. Metric/command: `notes/benchmark-070.md` (no run record
  supplies either input). Output: `manual_interventions=not_evaluated`,
  `sessions=not_evaluated`.
- **SC-007**: **Status = `met` (targeted).** Criterion: the report records
  critical path, wall-clock, efficiency, and retries; a parallel claim needs
  overlapping intervals. Command:
  `python3 -m pytest -q tests/unit/test_wp_report.py -k "critical_path or parallelism_efficiency or max_concurrent or overlap or retry"`;
  Scenario E. Output: `4 passed, 15 deselected`; Scenario E
  `critical_path=130`, `wall=200`, `efficiency=0.575`, `max_concurrent=2`,
  `overlap=true`.
- **SC-008**: **Status = `met` (targeted).** Criterion: fixture dry runs pass
  every enumerated scenario and the driver suite reports zero new failures.
  Command: Scenario C (`2 passed`), Scenario G (`3 passed`), Scenario F
  (`19 passed`), existing driver targeted suite (`65 passed`). Output: zero
  failures in the enumerated fixture scenarios and the driver's own suite.

### Closure gate disposition

- `SC-001` and `SC-002` are `not_evaluated`, and **no written user waiver**
  naming either criterion exists in the workspace at 2026-10-25T07:52Z.
- FR-023 and T039 are explicit: an all-`not_evaluated` benchmark MUST NOT
  close the feature, and the closure gate fails (no handoff) when neither met
  evidence nor a recorded waiver exists. **The closure gate is blocked; no
  handoff is issued; the feature remains Planned.**
- To close, the user must either (a) record an explicit waiver naming SC-001
  and/or SC-002 with its reason, or (b) run a comparable benchmark (at least
  three samples per measured stage, same host class and topology, FR-022
  interval). Then run the deferred full-suite slot and the name-level
  comparison above and re-evaluate.
- T039 is marked `[x]` because the closure gate was executed and its blocking
  outcome is recorded here. That mark does not assert feature closure and does
  not promote SC-001 or SC-002.

### Plan constraint

**PLAN-EDIT: none.** No plan-owned artifact (`plan.md`, `data-model.md`,
`contracts/`, `quickstart.md`, `research.md`, `feature-ref.md`) was touched in
impl-s7. The six analyze residuals remain non-blocking and none is used by a
new code path in T036–T039.

## Closure outcome (post-review)

- **User waiver**: SC-001 and SC-002 are waived by the user on 2026-10-25
  (`notes/waiver-070.md`) because the mechanism, functional behaviour, and all
  quality gates are verified while a comparable benchmark is deferred. Both
  remain `not_evaluated` and are **not** claimed met; SC-003…SC-008 remain in
  force, and SC-006 remains `not_evaluated`.
- **User ratification**: the analyze-repair semantic plan revision is approved
  under the 063 §3.5(b) branch-(b) user decision
  (`notes/plan-revision-ratification-070.md`);
  `approved_baseline_commit = 0df504b9`.
- **Closure full suite**: `bash scripts/bash/run-tests.sh tests --names-out
  .specify/specs/070-subagent-task-teams/final-failed.txt` → `18 failed, 5674
  passed, 1 skipped in 256.75s`, rc 1;
  `comm -13 baseline-failed.txt final-failed.txt` → 0 lines, i.e. zero new
  name-level failures against the baseline (`19 failed / 5341 passed`).
  Evidence: `final-failed.txt` and the driver log
  `/home/agent/sdd-070/closure-full.log`.
- **Test-budget audit**: `audit-test-budget.py --stage-check closure` →
  `slots=baseline:1 closure:1 reruns=3 exceptions=0 unknown=0
  environment_failures=0`, `stages=6 complete=6`, `status=ok`, rc 0.
- **Review disposition**: P0 = 0; P1 F1 (semantic plan revision) resolved by
  the user ratification above, P1 F2 (analyze-rerun evidence) resolved by
  commit `c9fef843`; P2 F3 backfilled, P2 F4/F5 recorded as framework
  follow-ups.
- **Merge**: master `ca8040f5`, fast-forward from `4f73c21d` after rebasing
  the four post-review commits (`c947c029`, `ff3fbdec`, `c35d83d6`,
  `ca8040f5`); no push (`gitlab/master` remains 4 commits behind); the
  worktree is retained.
