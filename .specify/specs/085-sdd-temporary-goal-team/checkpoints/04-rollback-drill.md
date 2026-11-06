# Checkpoint 04 — rollback drill (implement)

## 1. Artifact verification

- sentinel: `IMPLEMENT-PART-DONE`
- U4: pass — `test-evidence/tasks-gates.txt`; targeted implementation tests `test-evidence/smoke.txt`
- artifacts: `scripts/python/goal-utils.py`, `scripts/python/sdd-route.py`, `skills/external/sdd-loop-driver/scripts/line-registry.py`, `wp-gate.py`, `agents/sdd-*.agent.md`, `tests/`
- anomaly: 未发现异常

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| Temporary goal exists only after requirements; criteria traceable, not SC copies | 80% | `test_temp_goal_contract.py` |
| Checkpoints record concurrency/roster and at most one config change | 80% | `test_checkpoint_protocol.py`; this drill |
| Each writing agent has an isolated worktree and deterministic integration | 80% | `test_temp_team_worktree_queue.py`; `test_line_registry_child_lines.py` |

## 3. Team configuration review — rollback drill

- evidence: `test_temp_team_worktree_queue.py`; team `config.agent_concurrency`
- proposed change: raise implement `max_parallel` 18 → 24
- simulated regression: parallelism efficiency drop > 30% and one package retry increase
- rollback trigger: `parallelism_efficiency` drop ≥ 30% (owner: `checkpoint-protocol.md`)
- action: restore the prior `team.md` bytes; no second proposal in the same checkpoint
- result: `rollback=yes`; bytes restored; the change is not re-proposed immediately

## 4. Next stage concurrency / roster

- requested: 24; effective: 18; reason: `verifier-reserve` (unchanged after rollback)
- stage max_parallel: implement 18; verifier reserve: 4
- roster: unchanged
