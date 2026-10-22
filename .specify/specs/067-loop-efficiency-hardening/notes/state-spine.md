# Loop State Spine — 067-loop-efficiency-hardening

<!-- loop-state:begin -->
spine_state: running
stage_started_at: 1792653477
stage_deadline_epoch: 1792658877
stage_base_commit: ae215d74
attempt: 0
retry_limit: 2
run_id: r20261022T061700Z-067a
last_verdict: none
salvage: none
<!-- loop-state:end -->

## U0 Entry Declaration

- **line_id**: 067-loop-efficiency-hardening
- **target_project**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
- **topology**: local (host-native subagent; qodercli MUST NOT be started)
- **authority**: `.specify/specs/067-loop-efficiency-hardening/requirements.md`, `.specify/specs/063-sdd-loop-efficiency/`, `scripts/bash/run-tests.sh`, `pyproject.toml`, `.specify/memory/constitution.md`
- **slice**: 067-loop-efficiency-hardening; this run's focus = drastically slim the spec-kit framework's own test workflow so one complete run finishes within 10 minutes
- **breakpoint (U1)**: requirements — 067 has Draft `requirements.md` only; no plan/tasks/checklist/analyze; feature binding = Feature 058
- **branch**: 067-loop-efficiency-hardening (short-lived feature branch off master `7f9033ec`; U6 merges locally, push requires explicit authorization)
- **working tree at dispatch**: clean except this spine and the running baseline log (both driver-owned)

## Stage Plan

requirements (update scope with test-suite optimization) → U4 verify + deterministic gates → clarify → plan → tasks → checklist → analyze → implement → review → U6 local merge (push requires explicit authorization).

## Split Plan (067 parts)

1. Requirements update: add framework test-suite slimming scope (new US + FRs/SCs, baseline facts).
2. Clarify: resolve open choices (dev-only test deps, tiering policy, pruning evidence rules).
3. Plan: test-economics design (tiering, table-driven consolidation, fixture sharing, parallel execution, runner contract).
4. Tasks: bounded ≤8-task parts.
5. Checklist → analyze (mandatory gates).
6. Implement in bounded parts; full-suite budget only at implement start and post-review slots.
7. Review → local merge.

## Current Part Brief (implement A · T001–T006)

- **part_id**: P7-implement-A-baseline-rc07-admission
- **allowed files**: `tests/conftest.py`, `tests/unit/test_admission_check.py`, `test-evidence/` new/updated evidence files, `tasks.md` task-state checkboxes only
- **must not modify**: `src/`, `scripts/`, `pyproject.toml`, mirrors, registry, requirements.md, plan.md, other tests
- **tasks**: T001 baseline id list (three-number reconciliation), T002 evidence skeletons (ledger/triage/pinned roster), T003 RC-07 autouse git-config neutralization fixture, T004 admission in-process direct call with CLI pin, T005 admission fixture reuse + table-driven expansion, T006 targeted retest + timing evidence
- **excluded**: T007 (implement-start full run) is **driver-executed after this part** with `--names-out` and the MP-02 cold-cache protocol; the executor MUST NOT run the full suite
- **target commands**: `bash scripts/bash/run-tests.sh --collect-only -q` (T001); `bash scripts/bash/run-tests.sh tests/unit/test_admission_check.py -q --durations=0` (T003/T006)
- **expected red→green**: admission family baseline 87.45 s (red) → family ≤25 s design band, or over-band recorded with attribution (green); all 18 admission behaviors and the CLI exit-code pin preserved
- **run-turn-budget**: 120
- **acceptance**: T001–T006 `[X]`; RC-07 scoped and reversible; ledger rows for merged/rewritten cases; no full-suite run; no test claimed pass unless actually run; report residual risks
- **test-budget ruling**: pre-stage 750 s run is diagnostic and consumes no slot; T007 is the implement-start slot; T034 is the closure slot; exactly two in-stage full runs

## Dispatch Log

| part | stage | task_ids | turns | tests delta | commit | outcome |
|------|-------|----------|-------|-------------|--------|---------|
| P1-requirements-test-scope | requirements | — | not_evaluated | none run | 982a0503 | DONE — US5 + FR-011…FR-021 + SC-006…SC-010 land; no test claimed |
| P2-clarify-test-economics | clarify | — | not_evaluated | none run (baseline in flight; only lastfailed cache read) | f086e36d | DONE — 7 open items ratified; Assumptions de-opened; FR-012/FR-018/SC-007src/SC-008 minimal revisions; pre-analyze 0/0 fr=21 sc=10; validate-requirements 0e/0w |
| P3-plan-test-slimming | plan | — | not_evaluated | none run (2-node timing probe only, per plan-probes dated record) | bca3bc99 | DONE — plan.md + research/data-model/contracts×4/quickstart + plan-probes evidence; pre-analyze --stage plan pass 0e/0a (clauses=35); decomposition-check --mode plan proceed (FR 21/30); no full-suite run; no test claimed as passing |
| P4-tasks-test-slimming | tasks | T001–T038 | not_evaluated | none run | 78954beb | DONE — 38 tasks / 9 phases (≤8 per part); validate-tasks 0e/0w; pre-analyze tasks pass 0e/1a (expected missing new test path); decomposition proceed 38/40; no test run |
| P5-checklist-test-slimming | checklist | CHK001–CHK041 | not_evaluated | none run | 3db048e4 | DONE — 41 items, 40 PASS / 1 FAIL (CHK012 E2 symbol ambiguity); FAIL remediated by `b9d23cc2` (tasks.md disambiguation; validate-tasks 0/0); no test run |
| P6-analyze-test-slimming | analyze | — | not_evaluated | none run | ae215d74 (report + remediation) | DONE — VERDICT GREEN; 0 CRITICAL / 0 HIGH / 3 MEDIUM / 8 LOW; M-1 slot ruling, M-2 count reconciliation, M-3 feature registry sync applied; no test run |
| P7-implement-A-baseline-rc07-admission | implement | T001–T006 (T007 driver) | — | targeted only | — | dispatched |

## Gates

- requirements U4 (2026-10-22T06:23:47Z): `pre-analyze-check --stage requirements` → pass, 0 errors / 0 advisories, fr=21 sc=10; `decomposition-check --mode plan` → proceed (21/30, no split-required).
- requirements validator (subagent report): validate-requirements status=ok, 0 error / 0 warning.
- U4 artifact check: commit `982a0503` contains only `requirements.md` + `notes/test-slimming-scope-2026-10-22.md`; no push; no false test-pass claim found.
- clarify U4 (2026-10-22T06:30:08Z): `pre-analyze-check --stage requirements` → pass, 0 errors / 0 advisories, fr=21 sc=10; `decomposition-check --mode plan` → proceed (21/30); commit `f086e36d` contains only requirements.md + two dated evidence/notes files; no pytest run claimed.
- baseline evidence commit: `137abc67` (`test-evidence/baseline-full-2026-10-22.md`, failure list, top-50 durations).

## Baseline Full-Run Measurement (driver)

- Command `bash scripts/bash/run-tests.sh -q --durations=50`; exit 1; wrapper wall clock **750 s**; pytest **748.56 s**.
- Counts: **83 failed, 4467 passed, 1 skipped, 4 warnings**; 4553 collected.
- Failure set: 83 names in `test-evidence/baseline-failures-2026-10-22.txt`; 50 contain a mirror/parity/sync/drift/distribution marker; remaining 33 are gate-total pins, exec-quant cases, and 3 `tests/unit/test_loop_state_engine.py` cases.
- Slowest 50 = 298.2 s; admission_check 18, worktree queue 6, proactive trigger 4, trigger telemetry 3, workspace isolation 3.
- Full stdout: machine-local `notes/baseline-full-2026-10-22.log` (`*.log` gitignored); dated record committed at `137abc67`.
- This is the pre-change baseline for SC-006/SC-008, not a passing run.

## Test-Budget Ruling (M-1)

- Pre-stage full run `2026-10-22` (750 s, 83 failed) = diagnostic baseline outside implement; consumes no 063 slot.
- Implement-start slot = T007: full run with `--names-out` (`test-evidence/baseline-failures-<date>-implement-start.txt`) and MP-02 cold-cache protocol; booked in this spine's `<!-- test-budget -->` fence by T007.
- Closure slot = T034: full run after review, before merge; booked as `slot=closure`.
- In-stage full runs = exactly two; any third run requires an explicit out-of-slot exception record.
- Closure name-level diff authority = the T007 in-stage baseline list; the pre-stage 83-name list is the scope baseline.

## Checkpoint

- requirements DONE (`982a0503`); clarify DONE (`f086e36d`); baseline measured (`137abc67`); plan DONE (`bca3bc99`); tasks DONE (`78954beb`); checklist DONE (`3db048e4`, CHK012 fixed by `b9d23cc2`); analyze GREEN (`ae215d74`, 0 CRITICAL/HIGH, M-1…M-3 remediated).
- implement: part A dispatched (T001–T006); T007 driver-run next; then parts B–F, Phase 8 wrap-up, review, Phase 9 closure, U6 local merge (push requires explicit authorization).

## Framework Observations

- (U4/U6) none recorded yet.
