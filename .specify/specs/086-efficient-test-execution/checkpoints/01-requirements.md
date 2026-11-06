# Checkpoint 01 — requirements

## 1. Artifact verification

- sentinel: `REQUIREMENTS-DONE`
- U4: **pass after driver repair** — evidence: `test-evidence/requirements-gates.txt` § U4 independent re-run
- artifacts:
  - `.specify/specs/086-efficient-test-execution/requirements.md`
  - `.specify/specs/086-efficient-test-execution/checklists/requirements.md`
  - `.specify/specs/086-efficient-test-execution/test-evidence/requirements-gates.txt`
  - `.specify/memory/features.md` (row 086; 81 rows / Total Features 81)
  - `.specify/memory/features/086.md`
  - commit `2a88a9e7` (stage); branch `086-efficient-test-execution`
- anomaly: `ANOMALY: stale stage gate evidence (RS-002/RS-005 non-resolving contract cells) repaired; requirements-stage Wrap-up records were missing and were run by the driver; the temporary goal was first created in global scope by an option-order error, removed and recreated spec-local. See §Anomalies and repairs.`

## 2. Temporary Goal progress

- goal: `.specify/specs/086-efficient-test-execution/goal/086-efficient-test-execution/goal.md`
- slug: `086-efficient-test-execution`; status: `active`; engine `validate`: `valid: true`

| criterion | degree | evidence_ptr |
|---|---|---|
| Full-suite parallel wall-clock is at most 40% of the recorded 1031.48 s serial baseline, measured by the canonical runner. | not_evaluated | `.specify/.tmp/086/baseline.log`, `.specify/.tmp/086/parallel.log`; Phase 0 state-spine table |
| The final parallel run has zero new failure names versus the serial baseline, with every serial exception explicitly declared. | not_evaluated | `.specify/.tmp/086/baseline-failed.txt`, `.specify/.tmp/086/parallel-failed.txt`; `comm -13` in state spine |
| The efficient-test-execution principle ships in the constitution template and live file, the instructions template and live file, and a single owner guideline. | not_evaluated | `requirements.md` FR/SC; implementation pending |
| 085's temporary Goal/Team, stage concurrency, worktree/integration queue and checkpoints are used in this run and their test suites remain green. | not_evaluated | this goal file; U0 concurrency declaration; this checkpoint; team/checkpoints pending |
| The feature reaches Ready for Review with zero blocking review findings and honest evidence. | not_evaluated | requirements U4; review pending |

No criterion is marked achieved; unmeasured readings are `not_evaluated`, never zero.

## 3. Team configuration review

- evidence: n/a — the temporary Team is created only after `clarify` + `plan` U4 (085 contract C-008)
- symptom: none
- proposal: none
- ratification: n/a
- applied: no

## 4. Next stage concurrency / roster

- stage: `clarify`
- requested: 24; effective: **2**; reason: single ready clarify package + 1 verifier reserve; host capacity `host-capacity-undeclared`; temporary Team not created until after plan U4 (085 C-008)
- stage max_parallel: 1; verifier reserve: 1; executor slots: 1
- roster: `sdd-clarify-analyzer` (1 executor) + driver U4 verifier

## Anomalies and repairs (disclosed)

1. **Runtime Stack contract cells**: RS-002 (`pyproject.toml` + Chinese annotation) and RS-005 (`运行证据文件`) did not resolve under the repo. The cells were corrected to `pyproject.toml` and `.specify/specs/086-efficient-test-execution/requirements.md`; no FR/SC changed. The stage's original gate evidence claimed `advisories=0`; the U4 re-run is appended to `requirements-gates.txt`.
2. **Missing requirements-stage Wrap-up**: the stage left no session/feedback records despite `REQUIREMENTS-DONE`. The driver ran `run-determination` (session `r20261106T033959Z-086a`), `exec-quant`, and `feedback-utils` for `skill:create-requirements`; records are committed with this checkpoint.
3. **Temporary-goal scope**: the first `goal-utils.py create` call put the goal in global `.specify/goal/086-efficient-test-execution/` because `--scope` was passed before the subcommand. That directory was removed (our own just-created artifact); the goal was recreated at the spec-local path and `validate` returned `valid: true`. No 085 goal/team artifact was touched.
