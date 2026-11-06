# Checkpoint 04 — tasks

## 1. Artifact verification

- sentinel: `TASKS-DONE`
- U4: **pass** — evidence: `test-evidence/tasks-gates.txt`; independent driver re-runs: `validate-tasks.py` = PASS 0 error(s)/0 warning(s); `decomposition --mode tasks` = proceed (33 FR / 50 tasks vs 60/80); `pre-analyze --stage tasks` = pass (errors=0, advisories=39 future-deliverable paths)
- artifacts:
  - `.specify/specs/086-efficient-test-execution/tasks.md` (50 tasks / 9 phases; 52/52 contract clauses; Tests Mode ON; GATE-086 + GATE-1…8)
  - `.specify/specs/086-efficient-test-execution/coverage-baseline.txt` (575 lines, base `0f4b203e`)
  - `.specify/specs/086-efficient-test-execution/test-evidence/tasks-gates.txt`
  - commit `f3105c98`; branch `086-efficient-test-execution`
- anomaly: `ANOMALY: T041 updates only the 085 verification.md SC-010 live-status lines — the single declared exception authorized by FR-030/A12/A17; must not widen to any other 085 path. The tasks stage's first pre-analyze run had two runtime-stack-row errors (RS-003/RS-004), fixed in-passing. The stage missed the skill-identity feedback/exec-quant records; the driver filled them.`

## 2. Temporary Goal progress

- goal: `.specify/specs/086-efficient-test-execution/goal/086-efficient-test-execution/goal.md` (active)

| criterion | degree | evidence_ptr |
|---|---|---|
| Full-suite parallel wall-clock ≤ 40% of the 1031.48 s serial baseline. | not_evaluated | plan; tasks WP-A; implementation pending |
| Final parallel run has zero new failure names vs the serial baseline, serial exceptions declared. | not_evaluated | tasks T007–T012, T041–T048; implementation pending |
| Principle ships in constitution template/live, instructions template/live, one owner guideline. | not_evaluated | tasks WP-B; implementation pending |
| 085 temporary Goal/Team, concurrency, worktree/integration queue and checkpoints are used and green. | not_evaluated | team file; tasks WP-C; implementation pending |
| Feature reaches Ready for Review with zero blocking review findings. | not_evaluated | tasks U4; review pending |

Unmeasured readings stay `not_evaluated`, never zero.

## 3. Team configuration review

- evidence: team file; tasks stage used the `sdd-task-coordinator`/`sdd-task-executor` seat
- symptom: none
- proposal: none (no configuration change at this checkpoint)
- ratification: n/a
- applied: no

## 4. Next stage concurrency / roster

- stage: `checklist`
- requested: 24; effective: **2**; reason: single ready checklist work package + 1 verifier reserve; host capacity `host-capacity-undeclared`; team `stage_seats.checklist.max_parallel` = 2 is not binding
- stage max_parallel: 2; verifier reserve: 1; executor slots: 1
- roster: `sdd-checklist-worker` (carrier `general-purpose`/`SDD Executor`) + `sdd-stage-verifier`

## Declared exceptions carried forward

- **T041 / 085 live status**: only `.specify/specs/085-sdd-temporary-goal-team/verification.md` SC-010 status lines may change; the 085 goal/team/checkpoints/contracts/history remain untouched. Final verification must show only those SC-010 lines changed. The 085 SC-010 stays `partial` unless the full dogfood evidence is complete.
