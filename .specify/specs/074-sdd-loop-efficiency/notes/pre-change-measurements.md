# Pre-Change Measurements — Feature 063

- Date: 2026-10-20
- Branch: `074-sdd-loop-efficiency`
- HEAD at measurement: `ed96d5c8` (spec corrections only; no behavior-face change)
- State spine: `/tmp/sdd-loop-efficiency/state.md` (`spine_write_mode=direct`)

## N-08 — SC-010 baseline commit correction

Command:

```text
git log --oneline ba2a18db..HEAD -- skills/external/sdd-loop-driver/SKILL.md skills/external/sdd-loop-driver/references skills/external/sdd-loop-driver/scripts
```

Real output:

```text
4f75a98f fix(sdd-loop-driver): add deadline grace and late-completion guard
1610e3b4 fix(064-subagent-concurrency): close ownership fail-open and land behavior evidence
26b19104 test(064-subagent-concurrency): finalize 3.8-compatible stdlib guard and rerun
30439f53 test(064-subagent-concurrency): close non-regression gates and verification
c37d7614 feat(064-subagent-concurrency): add CLI capability profiles and observation program
a100d560 feat(064-subagent-concurrency): implement lifecycle detach, lease and reattach
ba785b0a feat(064-subagent-concurrency): implement workspace isolation and integration queue
9e69f3de feat(064-subagent-concurrency): implement line registry and attribution envelope
```

- First behavior-face commit: `9e69f3de`.
- Parent = actual behavior baseline: `a1aac7e5f8a6174d8cf26b0c1665c539dad3383d`.
- The spec's frozen reading `ba2a18db` **does not apply** (behavior already changed at `9e69f3de`).
- Recorded in the state spine (`Line Notes`, `Stall Baseline`), here, and in `plan.md` § Plan Repair Record 第 5 轮.

## SC-010 behavior baseline recording

- Command: `python3 tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py --record --worktree /tmp/063-baseline-a1aac7e5 --out .specify/specs/074-sdd-loop-efficiency/notes/stall-behavior-baseline.json`
- Read-only worktree: `git worktree add --detach /tmp/063-baseline-a1aac7e5 a1aac7e5`
- Exit status: `0`
- File root: `base_commit=a1aac7e5f8a6174d8cf26b0c1665c539dad3383d`, `recorded_at=1792494509`, `initial_retries=0`, three scenarios.

Observed tuples (fixture observation, not transcribed):

| Scenario | watcher_verdict | exit_code {watcher, runner} | spine_stall_state | retries | escalation | next_stage | write_before_action |
|----------|-----------------|-----------------------------|-------------------|---------|------------|------------|---------------------|
| timeout | TIMEOUT | {14, 124} | stalled-timeout | 0 | true | no | yes |
| retry-limit | FAILED | {12, 1} | stalled-retry-limit | 2 | true | no | yes |
| fake-done | INCOMPLETE | {15, 0} | incomplete-fake-done | 0 | not-applicable | no | yes |

- Replay pre-check on the current tree (before any behavior-face edit): `--replay --worktree . --baseline … --initial-retries 0` → `PASS: replay matches baseline`, `differences=[]`.
- Recording/replay is not a full-suite run and consumed no FR-011 slot.

## Mirror check (`sync-mirrors.py --check --only skills/external`)

- Exit status: `2`
- `62` DIFF lines across `10` unique `.specify/skills/<name>` directories; `0` in the owned `sdd-loop-driver` pair.
- Raw output: `notes/baseline-mirror-check.txt`; frozen path list: `notes/baseline-mirror-diff-paths.txt` (62 paths) for the zero-NEW-drift comparison.
- **Measured discrepancy**: plan/tasks recorded "12 directories"; this run measures 10 unique mirror directories. The path list is the comparison authority; the count wording is a dated reading and is not silently normalized.

## Existing contract test (`tests/contract/test_sdd_loop_driver_skill.py`)

- Command: `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q`
- Result: `23 passed`, exit `0`.
- Raw output: `notes/baseline-contract-sdd-loop-driver.txt`.

## Watcher self-test

- Command: `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test`
- Result: `28 passed, 0 failed`, exit `0`.
- Raw output: `notes/baseline-watch-selftest.txt`.

## Interpreters and validators

- `python3 --version` → `Python 3.9.6`
- `python --version` → `Python 3.14.6`
- `python3 .specify/scripts/python/validate-requirements.py .specify/specs/074-sdd-loop-efficiency/requirements.md` → `348 lines, 56 definition rows, 8 shared strings, 0 error(s), 0 warning(s)`

## Deliverable initial state (24 paths in `feature-ref.md`)

New paths (15) — `driver-stall-fixture.py` and the fixture directory exist after T000; the other 13 are absent:

- absent: `references/efficiency-model.md`
- absent: `scripts/stage-runner.sh`
- absent: `scripts/derive-live-log.py`
- absent: `scripts/admission-check.py`
- absent: `scripts/audit-test-budget.py`
- absent: `scripts/audit-plan-changes.py`
- absent: `tests/contract/test_sdd_loop_driver_efficiency.py`
- absent: `tests/unit/test_admission_check.py`
- absent: `tests/unit/test_derive_live_log.py`
- absent: `tests/unit/test_audit_test_budget.py`
- absent: `tests/unit/test_audit_plan_changes.py`
- absent: `tests/integration/test_sdd_loop_efficiency_runner.py`
- absent: `tests/integration/test_sdd_loop_efficiency_regression.py`
- present (T000): `tests/fixtures/sdd_loop_efficiency/`
- present (T000): `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py`

Update targets (9) — all present:

- `skills/external/sdd-loop-driver/SKILL.md`
- `skills/external/sdd-loop-driver/references/dispatch-recipes.md`
- `skills/external/sdd-loop-driver/references/stage-prompts.md`
- `skills/external/sdd-loop-driver/references/watch-model.md`
- `skills/external/sdd-loop-driver/scripts/watch-target.sh`
- `docs/reference/skills/sdd-loop-driver.md`
- `tests/contract/test_sdd_loop_driver_skill.py`
- `.specify/memory/features/058.md`
- `.specify/memory/features.md`
