# Checkpoint 08 — implement wave 1 (A1+B1)

## 1. Artifact verification

- **A1** `bd241323` — 3 files: `scripts/bash/run-tests.sh` + `.specify` mirror + `tests/contract/test_run_tests_runner_contract.py` (23 cases). 23 runner tests passed; guard set 213 passed / 1 failed (the pre-existing `test_c5_the_cap_leaves_zero_integer_headroom` in the T050 baseline). **Anomaly:** A1 created the A4-owned runner test file; A4 MUST append, not overwrite.
- **B1** `3540c7f5` — 2 files: `shared/guidelines/test-execution-efficiency.md` + `.specify` mirror (16.7 KB). 79 targeted tests passed / 1 deselected (the same pre-existing `test_c5`); `scan-confirmation-gates` **total 27 / destructive 20 / keep_gate 7 / violations 0**; bilingual/doc checks 0 findings. **Anomalies:** guideline body is Chinese while the constitution/instructions titles are English (B2/B3 must carry the shared English title); the earlier "34" gate reading was wrong — the executed scan is 27.
- **Integration**: A1 fast-forward `bd241323`; B1 rebase + fast-forward `3540c7f5`; worktree clean; A1/B1 worktrees removed; child lines `086-wp-a1`/`086-wp-b1` closed; branches deleted.
- **Actual concurrency**: **2** (A1 + B1). 085 child lines registered/closed; worktrees under `~/tmp/spec-kit/086/worktrees/` (the C-008 `.specify/.tmp` path is rejected by the line-registry's "outside repo_root" check; recorded as a 085 dogfood observation).

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| Full-suite parallel wall-clock ≤ 40% of the 1031.48 s serial baseline. | not_evaluated | T050 687.41s; parallel pending |
| Final parallel run has zero new failure names vs the serial baseline, serial exceptions declared. | not_evaluated | T050 19 names; T047 closure pending |
| Principle ships in constitution template/live, instructions template/live, one owner guideline. | 35% | B1 owner guideline + mirror integrated; B2/B3 pending |
| 085 temporary Goal/Team, concurrency, worktree/integration queue and checkpoints are used and green. | 30% | temporary Goal/Team; checkpoints 01–08; 2-way wave; 085 tests pending |
| Feature reaches Ready for Review with zero blocking review findings. | not_evaluated | review pending |

## 3. Team configuration review

- evidence: A1/B1 child lines, worktrees, integration record; the 2-way wave
- symptom: none
- proposal: no configuration change; keep the plan's dependency waves
- ratification: n/a
- applied: no
- observation: the 085 line-registry's "worktree outside repo_root" check contradicts C-008's `.specify/.tmp` path; the driver used `~/tmp/spec-kit/086/worktrees/` and records the inconsistency as a 085 dogfood observation (no 085 edit).

## 4. Next wave concurrency / roster

- stage: `implement` (wave 2)
- requested: 24; effective: **4** (3 executors A2/A3/B2 + 1 verifier reserve); team cap 18 not binding
- stage max_parallel: 18 (team implement cap); verifier reserve: 1; executor slots: 3
- roster: `sdd-implement-coordinator` + `sdd-implement-executor` (host-native carriers) + `sdd-stage-verifier`
- wave 2: A2 (audit parser) + A3 (pyproject/dev docs/serial marker) + B2 (constitution/instructions landing) in parallel; A2/A3 depend on A1; B2 depends on B1
- wave 3: A4 after A2/A3 (append the runner tests); B3 after B2; C1 after A1+A4+B2; C2 last
