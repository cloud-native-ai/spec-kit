# Checkpoint 10 — implement wave 3 (A4+B3)

## 1. Artifact verification

- **A4** `f12b554d` — `tests/contract/test_run_tests_runner_contract.py` appended (23 A1 cases preserved; 38 total; 38 passed in the A4 worktree; clean-environment re-run at the driver 38 passed as part of 191).
- **B3** `1d962bfb` — count pins updated, new `tests/contract/test_test_execution_efficiency.py`, owner guideline title/boundary in-passing repair (disclosed, outside B3's owned paths). B3 five files: 153 passed / 1 failed (`test_g9`, T050 baseline).
- **Integration**: A4 ff; B3 rebase+ff; worktree clean; actual concurrency 2.
- **Driver clean-environment combined run**: `191 passed / 1 failed`; the single failure is `test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline`, which is in the T050 baseline (frozen 23 vs live 27; EP-008 disclosed drift), not this feature's.
- **Anomalies**: A4's C-010/C-011 pass against the pre-086 runner (mutation legs carry the red leg); `notes/red-first-evidence.md` was missing and the driver created it; B3 edited the B1 owner guideline outside its owned paths (in-passing, disclosed); A4's test helper `_python()` trusts a caller-supplied relative `SPECKIT_PYTHON` — a caller pitfall only (the clean/full-suite run falls back to `sys.executable`), no suite defect.

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| Full-suite parallel wall-clock ≤ 40% of the 1031.48 s serial baseline. | not_evaluated | T050 687.41s; C1/T047 pending |
| Final parallel run has zero new failure names vs the serial baseline, serial exceptions declared. | not_evaluated | T050 19 names; T047 pending |
| Principle ships in constitution template/live, instructions template/live, one owner guideline. | 100% | B1+B2+B3 integrated; 191/1 clean |
| 085 temporary Goal/Team, concurrency, worktree/integration queue and checkpoints are used and green. | 65% | 2/3/2-way waves; checkpoints 01–10; C1 dogfood/085 tests pending |
| Feature reaches Ready for Review with zero blocking review findings. | not_evaluated | review pending |

## 3. Team configuration review

- evidence: A4/B3 child lines, worktrees, integration; the 2-way wave
- symptom: none
- proposal: no configuration change
- ratification: n/a
- applied: no
- observations: the 081 stale line was released with `--evidence-ref`; the 085 line-registry worktree path must be outside `repo_root`; the A4 runner tests require an absolute `SPECKIT_PYTHON` when the caller sets it.

## 4. Next stage concurrency / roster

- stage: implement (C1 then C2)
- requested: 24; effective: **2** (1 executor + 1 verifier reserve); team cap 18 not binding
- stage max_parallel: 18; verifier reserve: 1; executor slots: 1
- C1 (after A1+A4+B2): parallel-safety marker/nested assertion + 085 dogfood + T014 parallel vs T050 + T016 representative pair
- C2 last: registry/CHANGELOG/085 SC-010 carve-out/verification + T044/T047 closure (final full parallel vs T050)
