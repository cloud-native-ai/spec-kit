# Loop State Spine — 067-loop-efficiency-hardening

<!-- loop-state:begin -->
spine_state: running
stage_started_at: 1792658279
stage_deadline_epoch: 1792663679
stage_base_commit: 58dd4f79
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

## Current Part Brief (implement F · T025–T029)

- **part_id**: P12-implement-F-triage-drills
- **allowed files**: triage-relevant contract/unit test files (gate-total pins, exec-quant, loop_state), `test-evidence/` triage/debt/evidence, `tasks.md` T025–T029 checkboxes only
- **must not modify**: source `shared/`, `skills/`, `scripts/`, `templates/`, `src/`, `pyproject.toml`, mirrors, registry, requirements.md, plan.md, tests unrelated to triage; never delete a test to hide a failure
- **T025**: gate-total pins — for each remaining Class 2 gate-total failure, identify the owner fact; update the expected literal with a recorded rationale (stale-pin) or register a dated debt; do not weaken pin strength.
- **T026**: exec-quant failures — triage each name; environment-specific/pre-existing → debt with evidence; do not fake a pass.
- **T027**: loop_state 3 failures — triage; two pass in isolation and fail in full context (order/state dependence); register debt or fix test-local isolation without weakening assertions.
- **T028**: injection + localization drill — inject one failing assertion into a merged suite parameter, run with `--names-out`, confirm the name-level diff contains exactly the injected name, re-run by node id to reproduce, then restore; evidence `injection-drill-<date>.md`.
- **T029**: triage closure — verify all 83 baseline names have exactly one row (50 mirror + 33 Class 2), debt rows point to dated records, pinned-roster intersection resolved, no test deleted to hide a failure.
- **no full suite**; no test claimed pass unless actually run.
- **run-turn-budget**: 120
- **acceptance**: T025–T029 `[X]`; triage table 83 rows; drills recorded with restoration; residual debt explicit; no new failures introduced

## Dispatch Log

| part | stage | task_ids | turns | tests delta | commit | outcome |
|------|-------|----------|-------|-------------|--------|---------|
| P1-requirements-test-scope | requirements | — | not_evaluated | none run | 982a0503 | DONE — US5 + FR-011…FR-021 + SC-006…SC-010 land; no test claimed |
| P2-clarify-test-economics | clarify | — | not_evaluated | none run (baseline in flight; only lastfailed cache read) | f086e36d | DONE — 7 open items ratified; Assumptions de-opened; FR-012/FR-018/SC-007src/SC-008 minimal revisions; pre-analyze 0/0 fr=21 sc=10; validate-requirements 0e/0w |
| P3-plan-test-slimming | plan | — | not_evaluated | none run (2-node timing probe only, per plan-probes dated record) | bca3bc99 | DONE — plan.md + research/data-model/contracts×4/quickstart + plan-probes evidence; pre-analyze --stage plan pass 0e/0a (clauses=35); decomposition-check --mode plan proceed (FR 21/30); no full-suite run; no test claimed as passing |
| P4-tasks-test-slimming | tasks | T001–T038 | not_evaluated | none run | 78954beb | DONE — 38 tasks / 9 phases (≤8 per part); validate-tasks 0e/0w; pre-analyze tasks pass 0e/1a (expected missing new test path); decomposition proceed 38/40; no test run |
| P5-checklist-test-slimming | checklist | CHK001–CHK041 | not_evaluated | none run | 3db048e4 | DONE — 41 items, 40 PASS / 1 FAIL (CHK012 E2 symbol ambiguity); FAIL remediated by `b9d23cc2` (tasks.md disambiguation; validate-tasks 0/0); no test run |
| P6-analyze-test-slimming | analyze | — | not_evaluated | none run | ae215d74 (report + remediation) | DONE — VERDICT GREEN; 0 CRITICAL / 0 HIGH / 3 MEDIUM / 8 LOW; M-1 slot ruling, M-2 count reconciliation, M-3 feature registry sync applied; no test run |
| P7-implement-A-baseline-rc07-admission | implement | T001–T006 (T007 driver) | not_evaluated | targeted: admission 23→25 passed; full slot 83F/4469P/1S | 47a52cc9, f14c4f49, fe5f1e62, e95a5920 | DONE — RC-07 fixture + admission in-process/clone; call sum 121.06→23.03 s; T007 wall **534 s**, name diff 0 NEW / 0 FIXED |
| P8-implement-B-slow-families | implement | T008–T012 | not_evaluated | targeted only; 9 runs | 3cf366b6 | DONE — all four families already in band after RC-07; zero code changes; no ledger changes |
| P9-implement-CD-telemetry-clone | implement | T013–T018 | not_evaluated | targeted only | e30ea169, 5b2521c9 | DONE — telemetry 23.36→1.14 s (CLI smoke kept); proactive+instructions 32.70→31.0 s, still over band, attributed to generator subprocesses in the forbidden `scripts/` surface; clone fixture wired and verified |
| P10-implement-E1-mirror-suite-fold | implement | T019–T021 | not_evaluated | suite 202F/521P (drift, expected); 23 functions folded | 54cf98e4, 0c674638, 00b654a1 | DONE — suite covers 723 params; ledger 23 case-merge rows; no sync yet |
| P11-implement-E2-fold3-sync-recheck | implement | T022–T024 | not_evaluated | targeted: fold recheck 206F/822P (0 new); suite 202F/521P → 0F/723P; combined rerun 9F/1214P (all in-register) | 3059f4f0, 1d40ebeb, a6098885, 58dd4f79 | DONE — batch 3: 12 functions folded (9 pure + 3 byte-only, ledger 70–81); sync: 5 pairs, 202 engine-written mirrors, --check 0 DIFF; triage 50 rows (49 synced / 1 debt: test_i11 stale-pin, FB-06 debt-i11-per-tool-clause-render-2026-10-22.md) |
| P12-implement-F-triage-drills | implement | T025–T029 | — | targeted only | — | dispatched |

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

<!-- test-budget:begin -->
{"seq":1,"slot":"baseline","stage":"implement","purpose":"implement-start-baseline","trigger":"scheduled","at":"2026-10-22T07:39:30Z","command":"bash scripts/bash/run-tests.sh -q --durations=50 --names-out .specify/specs/067-loop-efficiency-hardening/test-evidence/baseline-failures-2026-10-22-implement-start.txt","selection_basis":"full-suite","rc":1,"passed":4469,"failed":83,"failed_names_path":".specify/specs/067-loop-efficiency-hardening/test-evidence/baseline-failures-2026-10-22-implement-start.txt","baseline_compare":"na","wall_seconds":534,"evidence_ptr":".specify/specs/067-loop-efficiency-hardening/test-evidence/full-run-2026-10-22-implement-start.md"}
<!-- test-budget:end -->

## Checkpoint

- requirements DONE (`982a0503`); clarify DONE (`f086e36d`); baseline measured (`137abc67`); plan DONE (`bca3bc99`); tasks DONE (`78954beb`); checklist DONE (`3db048e4`, CHK012 fixed by `b9d23cc2`); analyze GREEN (`ae215d74`, 0 CRITICAL/HIGH, M-1…M-3 remediated).
- implement: part A DONE (T001–T006 + T007 implement-start slot). T007 result: 534 s wall (≤600 s process check), 83 failed / 4469 passed / 1 skipped, name diff 0 NEW / 0 FIXED; E1 record `full-run-2026-10-22-implement-start.md`; budget fence baseline:1/closure:0. Next: part B (T008–T012), then C/D/E/F, Phase 8 wrap-up, review, Phase 9 closure, U6 local merge (push requires explicit authorization).
- E3 stage evidence for clarify/plan/tasks/checklist/analyze added; review row pending the review stage.

## Framework Observations

- (U4/U6) none recorded yet.
