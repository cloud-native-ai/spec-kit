# Loop State Spine — 067-loop-efficiency-hardening

<!-- loop-state:begin -->
spine_state: running
stage_started_at: 1792655452
stage_deadline_epoch: 1792660852
stage_base_commit: e95a5920
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

## Current Part Brief (implement B · T008–T012)

- **part_id**: P8-implement-B-slow-families
- **allowed files**: `tests/integration/test_worktree_integration_queue.py`, `tests/contract/test_workspace_isolation_contract.py`, `tests/contract/test_store_state_protocol.py`, `tests/unit/test_audit_plan_changes.py`, `tests/unit/test_loop_state_engine.py`, `test-evidence/` evidence, `tasks.md` T008–T012 checkboxes only
- **must not modify**: `src/`, `scripts/`, `pyproject.toml`, mirrors, registry, requirements.md, plan.md, other tests
- **measure-first rule**: run each family targeted BEFORE editing. RC-07 already cut the global hook tax; if a family is already within the plan §W2 band, record the measurement as a no-op ("already in band after RC-07") and do NOT edit that file. Only edit families still above band.
- **families**: worktree queue (T008), workspace isolation (T009), store-state two-branch merge (T010), audit_plan_changes + loop_state fixtures (T011), then T012 consolidated targeted retest + ledger rows
- **loop_state constraint**: T011 may only touch fixtures; the 3 baseline-failing loop_state tests must not be fixed or weakened here (triage owns them), and fixture changes must not become their failure cause
- **target commands**: `bash scripts/bash/run-tests.sh <family files> -q --durations=0`
- **expected red→green**: each family measured post-RC-07; above-band families reduced into plan band; all assertions and isolation semantics preserved; no full-suite run
- **run-turn-budget**: 120
- **acceptance**: T008–T012 `[X]` (no-op with measurement evidence allowed); ledger rows for any merged/rewritten tests; before/after table in `test-evidence/w2-partb-timing-<date>.md`; no test claimed pass unless actually run

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
| P8-implement-B-slow-families | implement | T008–T012 | — | targeted only | — | dispatched (measure-first; no-op if already in band) |

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
