# Checkpoint 06 — implement

## 1. Artifact verification

- sentinel: IMPLEMENT-DONE
- U4: pass — commit `95b7d071` (ordering test + rule-anchor member closure + verification.md) plus driver corrections `9df034a3`; feature guard modules: 2 failed / 130 passed, the two failures are the baseline pair (`test_i11…`, `test_g9…`)
- artifacts: `tests/contract/test_sdd_loop_driver_reanchor.py` (ordering assertion + three mutants), `checkpoint-protocol.md`, `re-anchoring-definitions.md` §1.1 closed eight, both instruction surfaces, `verification.md`, `test-evidence/contract-baseline-comparison.txt`
- wrap-up: `exec-quant` + `feedback` recorded by the implement executor under `/speckit.implement`; session record present
- anomaly: n-1 (guard-tests C-3 claims "no subprocess" but test_goal_migration spawns one), n-4 (`generate-instructions.sh` refuses to overwrite; budget 38400 set by hand), n-5 (090 evidence lane tripped the migration guard — closed by `9df034a3`); the one new baseline failure recorded by the executor is also closed by `9df034a3`

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| SC-001 | 100% | `verification.md` SC-001; guard modules green |
| SC-002 | 100% — ordering assertion landed, three mutants proven red first | `test-evidence/ordering-red-control.txt`, `red-first-090-c7.txt` |
| SC-003 | 100% under the re-based criterion (zero new vs the 49-name baseline; the 1 new failure is closed) | `test-evidence/contract-baseline-comparison.txt` + `9df034a3` |
| SC-004 | 100% | `verification.md` SC-004; owner §2 vs protocol §5 |

## 3. Team configuration review

- evidence: implement ran as one coordinator + sequential executor; no parallelism symptom
- symptom: none (single package)
- proposal: none
- ratification: n/a
- applied: no

## 4. Next stage concurrency / roster

- requested: 24; effective: 24; reason: local native subagents, shared-tree
- stage max_parallel: 1 (review is read-only over the four segments), verifier reserve: 1
- roster: review coordinator + four segment reviewers

## 5. Direction audit

- reload tier: T0+T1
- Q1 rules: in force; the stage landed tests red-first, disclosed the budget-by-hand correction, and did not push
- Q2 process: the executor's two anomalies were acted on by the driver (both closed) rather than left to review
- Q3 next action: the review stage (mandatory; four segments + ARC), then closure
- Q4 spine freshness: rewritten for implement before dispatch; rewritten now for review
- Q5 territory/workspace: only feature artifacts + the two guard corrections; mirrors `--check` ok; dirty `smoke-081.txt` untouched
- verdict: on-track
