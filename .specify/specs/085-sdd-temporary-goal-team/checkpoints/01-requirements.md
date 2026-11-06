# Checkpoint 01 — requirements

## 1. Artifact verification

- sentinel: `REQUIREMENTS-DONE`
- U4: pass — `test-evidence/requirements-gates.txt`
- artifacts: `.specify/specs/085-sdd-temporary-goal-team/requirements.md`
- anomaly: 未发现异常

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| Temporary goal exists only after requirements; criteria traceable, not SC copies | 50% | `goal/085-sdd-temporary-goal-team/goal.md`; `tests/contract/test_temp_goal_contract.py` |
| Checkpoints record concurrency/roster and at most one config change | 30% | `checkpoints/`; `tests/contract/test_checkpoint_protocol.py` |
| Each writing agent has an isolated worktree and deterministic integration | 20% | `contracts/concurrency-and-worktrees.md`; `tests/contract/test_line_registry_child_lines.py` |

## 3. Team configuration review

- evidence: requirements-stage gates; no work-package report yet
- symptom: none
- proposal: none
- ratification: n/a
- applied: no

## 4. Next stage concurrency / roster

- requested: 24; effective: 4 (clarify is read-mostly; stage max_parallel 2)
- reason: `stage-limited`
- stage max_parallel: clarify 2; verifier reserve: 1
- roster: sdd-clarify-analyzer + sdd-stage-verifier
