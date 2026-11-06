# Checkpoint 03 — tasks

## 1. Artifact verification

- sentinel: `TASKS-DONE`
- U4: pass — `test-evidence/tasks-gates.txt`
- artifacts: `tasks.md`; `validate-tasks.py` 0 error / 0 warning; `account-clause-coverage.py` status ok
- anomaly: 未发现异常

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| Temporary goal exists only after requirements; criteria traceable, not SC copies | 65% | `goal/085-sdd-temporary-goal-team/goal.md`; `test_temp_goal_contract.py` |
| Checkpoints record concurrency/roster and at most one config change | 60% | `checkpoints/02-plan.md`; `test_checkpoint_protocol.py` |
| Each writing agent has an isolated worktree and deterministic integration | 55% | `contracts/concurrency-and-worktrees.md`; `test_line_registry_child_lines.py` |

## 3. Team configuration review

- evidence: tasks-stage deterministic gates; 26 task rows; 65 clause claims
- symptom: implement stage has more ready write packages than the default shared-tree allows
- proposal: keep `write_isolation: worktree` and set implement `max_parallel: 18` (no new change; already declared at team creation)
- ratification: standing
- applied: no new change

## 4. Next stage concurrency / roster

- requested: 24; effective: 18 (implement executor slots after verifier reserve)
- reason: `verifier-reserve`
- stage max_parallel: implement 18; verifier reserve: 4; integrator after settle
- roster: sdd-implement-coordinator, sdd-implement-executor, sdd-stage-verifier, sdd-stage-integrator
