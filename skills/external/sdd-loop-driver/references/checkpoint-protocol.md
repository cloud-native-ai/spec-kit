# Checkpoint Protocol

**When**: after every stage U4 passes and before the next stage is dispatched. A checkpoint is a coordination point, not a stage and not a new gate; the U4 verdict and the stage sentinel remain the completion authority.

**Where**: `.specify/specs/<NNN-slug>/checkpoints/<NN>-<stage>.md`; a final `closure.md` records the terminal goal degree table and the archived team state.

## The four parts (all mandatory)

### 1. Artifact verification

- Consume the stage U4 verdict and a `loop-state.py --action snapshot` record.
- Record the artifact paths, the sentinel, the U4 evidence pointer, and any `ANOMALY:` line.
- Never infer completion from an executor's self-report.

### 2. Temporary Goal progress

- For each criterion of the spec's Temporary Goal, record `criterion / degree / evidence_ptr`.
- `degree` is a progress reading, not a binary checkbox; a missing measurement is `not_evaluated`, never zero.
- Goal content changes only through the goal engine (`/speckit.goal modify --scope spec`); the checkpoint never writes `goal.md`.

### 3. Team configuration review

- Gather evidence from `wp-report.py`, the team's `runs/<run_id>-report.md`, and the ledger.
- Detect one named symptom and propose **at most one** exact delta from the closed candidate space:
  `concurrency`, `stage max_parallel`, `roster add/remove`, `pattern`, `verifier reserve`.
- The proposal names its evidence, the exact before/after values, and the expected effect.
- Ratify according to `checkpoint_policy.ratification` (`standing` for reversible config changes declared at U0, or `human`). Never apply silently.
- Apply through `improve-team` / `/speckit.team modify --scope spec`; territory changes remain explicit modifications and are never optimizer output.

### 4. Concurrency and roster decision for the next stage

- Resolve the next stage's requested/effective concurrency and `stage_seats.<stage>.max_parallel`.
- Record the verifier reserve and the reason for any downgrade.
- The decision is written before the next dispatch; a later change requires another checkpoint.

## Rules

- All four parts are present. An inapplicable part carries `n/a` and a reason; omission is a defect.
- At most one configuration/concurrency/roster change per checkpoint. An explicit human goal edit does not count toward this cap.
- A checkpoint file is committed by the driver immediately after U4 as a driver record, not as a stage deliverable.
- **Rollback**: at the next checkpoint, revert the prior change when U4 fails, new test failures appear versus the stage baseline, `retries_package` increases by at least two, or `parallelism_efficiency` drops by at least 30 percent. A rolled-back change is not re-proposed immediately.
- `coordinate` remains territory-overlap only; with one temporary team it is a recorded no-op.
- The checkpoint carries paths and verdicts, never raw transcripts or fabricated metrics.

## Minimal shape

```markdown
# Checkpoint NN — <stage>

## 1. Artifact verification
- sentinel: <STAGE-DONE>
- U4: <pass|fail> — <evidence path>
- artifacts: <paths>
- anomaly: <未发现异常 | ANOMALY: ...>

## 2. Temporary Goal progress
| criterion | degree | evidence_ptr |
|---|---|---|
| <criterion> | <0-100% or not_evaluated> | <path> |

## 3. Team configuration review
- evidence: <wp-report path | team run report path | ledger>
- symptom: <one named symptom>
- proposal: <none | one exact delta>
- ratification: <standing | human | not-ratified>
- applied: <yes/no + path>

## 4. Next stage concurrency / roster
- requested: <n>; effective: <n>; reason: <reason>
- stage max_parallel: <n>; verifier reserve: <n>
- roster: <seats>
```
