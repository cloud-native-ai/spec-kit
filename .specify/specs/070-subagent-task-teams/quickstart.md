# Quickstart: 070-subagent-task-teams

**Feature**: 070 — Task Decomposition & Team Coordination for Subagent-Driven SDD
**Created**: 2026-10-24

This quickstart shows the intended operator experience for the new layer. The scripts and fixtures it names do not exist yet; they are created during implementation. Every command below therefore carries an **Execution status** note and a **Premises** list, and names the test that will pin it. Nothing in this file was executed during the plan stage except where a command is marked as already run.

## Scenario A — Gate a decomposed plan

**Purpose**: prove that a plan with bounded, owned, acyclic packages is admitted before dispatch.

```sh
python3 skills/external/sdd-loop-driver/scripts/wp-gate.py \
  --spine /tmp/wp-demo/state.md --stage plan --stage-attempt 1 \
  --check plan --plan-json /tmp/wp-demo/plan.json \
  --json-out /tmp/wp-demo/wp/line-plan-a1-gate-plan.json
```

Expected: JSON with `"verdict":"admit"` and exit code 0.

- **Execution status**: not run (script and fixture are implementation deliverables).
- **Premises**: `wp-gate.py` exists at that path; `--stage-attempt` is accepted (WG-02 / DR2); the plan fixture follows `data-model.md` E2; the JSON shape and exit code follow WG-04/WG-05; the state directory is writable.
- **Pinned by**: `tests/contract/test_sdd_loop_driver_wp_gate.py` and `tests/unit/test_wp_gate.py` (planned).

## Scenario B — Reject a cyclic, orphaned, or overlapping plan

**Purpose**: prove that dispatch is blocked and the driver records the reason, then falls back without a partial run.

```sh
python3 skills/external/sdd-loop-driver/scripts/wp-gate.py \
  --spine /tmp/wp-demo/state.md --stage plan --stage-attempt 1 \
  --check preflight --manifest /tmp/wp-demo/manifest.json \
  --json-out /tmp/wp-demo/wp/line-plan-a1-gate-preflight.json
```

Expected on the broken fixture: `"verdict":"reject"` with `cycle`, `orphan-output`, and `path-overlap` findings, exit code 1. The driver makes at most one repair amendment; a second reject records `decision=fallback`, `reason=gate-reject`, and runs the single-package path.

- **Execution status**: not run.
- **Premises**: the fixture plan contains a cycle, an unowned required output, and two unordered write packages with overlapping `owned_paths`; the manifest follows the 064 schema (`owned_paths`, `read_only_paths`, `forbidden_paths`); the gate emits the WG-06…WG-16 codes.
- **Pinned by**: `tests/unit/test_wp_gate.py` (cycle/orphan/overlap cases) and `tests/integration/test_wp_coordination_dry_runs.py` (fallback case).

## Scenario C — Concurrent read-only dispatch and write serialization

**Purpose**: prove that independent read-only packages overlap, a write package starts only after them, and no write interval overlaps another package's interval.

```sh
python3 -m pytest -q tests/integration/test_wp_coordination_dry_runs.py \
  -k "concurrent_read_only or write_serialization"
```

Expected: both tests pass. The simulator fixture records intervals; the test asserts at least two read-only intervals overlap and that the write interval begins after every read-only interval ends.

- **Execution status**: not run.
- **Premises**: `tests/fixtures/wp_driver_sim.py` implements the SD-01…SD-06 algorithm; the plan has two independent read-only packages and one dependent write package; `slot_cap=2`; the test asserts intervals, not wall-clock durations.
- **Pinned by**: `tests/integration/test_wp_coordination_dry_runs.py`; the algorithm text is pinned by `tests/contract/test_sdd_loop_driver_wp_coordination.py`.

## Scenario D — Verifier failure, retry delta, and escalation

**Purpose**: prove that a failed or unverified package blocks dependents, a retry requires a material delta, and a second failure escalates to U5.

```sh
python3 skills/external/sdd-loop-driver/scripts/wp-gate.py \
  --spine /tmp/wp-demo/state.md --stage plan --stage-attempt 1 \
  --check retry --wp-id plan-wp02 --wp-attempt 2 \
  --json-out /tmp/wp-demo/wp/line-plan-a1-gate-retry.json
```

Expected: the first fixture (no delta) returns `retry-unchanged`, exit 1. The second fixture (scope split into `plan-wp02-a` and `plan-wp02-b`) returns `admit`, exit 0. A third attempt returns `retry-exhausted`, exit 1, and the stage gate fails into U5.

- **Execution status**: not run.
- **Premises**: the ledger contains one `dispatch` for `plan-wp02` before the retry check; the amendment carries `wp_id`, `wp_attempt=2`, and a `retry_delta`; the split children have distinct outputs; the stage-attempt counter starts fresh after a U5 retry.
- **Pinned by**: `tests/unit/test_wp_gate.py` (retry cases) and `tests/integration/test_wp_coordination_dry_runs.py` (dependency-block and escalation cases).

## Scenario E — Stage close, report, and `not_evaluated`

**Purpose**: prove that the report is derived from the spine, that the metrics are recomputable, and that a missing timestamp becomes `not_evaluated` rather than zero.

```sh
python3 skills/external/sdd-loop-driver/scripts/wp-report.py \
  --spine /tmp/wp-demo/state.md --stage plan --stage-attempt 1 \
  --stage-u4-at 1790000000 --manual-interventions 0 \
  --out-dir /tmp/wp-demo/reports
```

Expected: the command prints the metrics JSON and writes `line-plan-a1-coordination.md` and `.json`. Deleting a package `ended_at` from a copied spine makes `critical_path_seconds` and `parallelism_efficiency` equal to the literal `not_evaluated`; `wall_clock_seconds` remains computable if the first `started_at` and `stage_u4_at` exist.

- **Execution status**: not run.
- **Premises**: the fixture spine contains `plan`, `dispatch`, `settle`, `verdict`, and `integrate` events with epoch timestamps; `--stage-u4-at` and `--manual-interventions` are accepted (OR-11 / DR6); the report paths follow WP-11.
- **Pinned by**: `tests/unit/test_wp_report.py` and `tests/contract/test_sdd_loop_driver_wp_model.py`.

## Scenario F — Opt out and single-package fallback

**Purpose**: prove that the declared precedence is honored and that a non-decomposed stage still records a decision.

1. In the U0 entry declaration write `decomposition: off`. No stage override can re-enable decomposition in that run.
2. Otherwise write `decomposition_stages: plan=auto` and, for one attempt, `decomposition_override: off`. That attempt records `decision=disabled`; the next attempt returns to `auto`.
3. Run the standard stage prompt, runner/native dispatch, sentinel, and U4 unchanged. The plan fence carries `decision=single-package` (or `disabled`/`fallback`), one synthetic package, and the gate verdict.

- **Execution status**: design walkthrough; no command is executed in the plan stage.
- **Premises**: the spine carries the FN-01 fields; the driver resolves the decision once (FN-02); the single-package package is `<stage>-wp01` with the stage sentinel (WP-13); for `implement`, the 067 part discipline remains in force (FN-05).
- **Pinned by**: `tests/contract/test_sdd_loop_driver_wp_coordination.py` (resolution/precedence) and `tests/integration/test_wp_coordination_dry_runs.py` (single-package and fallback runs).

## Scenario G — No nested driver, no persisted team

**Purpose**: prove that a package prompt cannot become a second driver and that a decomposed stage creates no team directory.

```sh
python3 -m pytest -q tests/integration/test_wp_coordination_dry_runs.py \
  -k "nested_driver or no_team_directory"
```

Expected: a prompt naming `sdd-loop-driver` is blocked and recorded; a clean prompt is dispatched. After a simulated decomposed stage, no `.specify/teams/<slug>/` directory exists and no `team.md` was written.

- **Execution status**: not run.
- **Premises**: the prompt check implements SD-13's three prohibitions; the simulator writes only under a temp state directory; the team-directory assertion checks the temp project root.
- **Pinned by**: `tests/integration/test_wp_coordination_dry_runs.py` and `tests/contract/test_sdd_loop_driver_wp_preset.py`.

## Regression and evidence commands

These run the existing behavior and the new tests at implementation time. They are not executed in the plan stage.

```sh
python3 -m pytest -q tests/contract/test_non_regression_070.py
bash scripts/bash/run-tests.sh --names-out .specify/specs/070-subagent-task-teams/baseline-failed.txt
python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver
python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver
```

- **Premises**: `test_non_regression_070.py` is created in the implementation phase; the full suite runs only in the two 063 slots (implement baseline and closure); the mirror command is the existing pair `skills/external` → `.specify/skills` and the baseline is the clean 28-file state measured in `research.md` § 0.
- **Pinned by**: `tests/contract/test_non_regression_070.py`, the existing mirror parity suite, and the 063 test-budget audit.
