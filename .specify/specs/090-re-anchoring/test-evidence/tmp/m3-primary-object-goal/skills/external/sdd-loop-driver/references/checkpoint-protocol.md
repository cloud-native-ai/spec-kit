# Checkpoint Protocol

**When**: after every stage U4 passes and before the next stage is dispatched. A checkpoint is a coordination point, not a stage and not a new gate; the U4 verdict and the stage sentinel remain the completion authority.

**Where**: `.specify/specs/<NNN-slug>/checkpoints/<NN>-<stage>.md`; a final `closure.md` records the terminal goal degree table and the archived team state.

## The five parts (all mandatory)

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

### 5. Direction audit

- Reload the loop anchor before answering: **T0** the state spine's `driver_contract` + `direction_contract` +
  `next_action` at every checkpoint; **T1** the driver `SKILL.md` Hard Requirements block plus this protocol at
  every stage boundary, after any subagent turn-limit stall, and after a detected context compaction; **T2** the
  full manual plus a reference only when a dispatch form is unclear or a stall is being handled. A full reload of
  every reference at every step is forbidden: it is ceremony and it buries the anchor in noise.
- **The audit's primary object is the goal.** The current action and the next one already carry
  the goal; a dropped rule leaves no trace in them (the canonical failure: "unattended" was ignored — package
  boundaries asked for permission and the spine lagged — while the work itself kept advancing step by step).
- Answer five binary questions, each with a path or a reading as evidence:
  1. Which rules govern this step, and is each still in force (`unattended` / no approval request / U4 -> next
     stage / spine written before acting / `workspace-guard --check` / fast-fail / the gate discipline / budget)?
  2. Was the last action completed under those rules — no report substituting for execution, no subagent
     turn-limit treated as a reason to hand back?
  3. Is the next action the one the plan or assignment names? (The goal is implicit in it; do not ask the goal
     as a separate question.)
  4. Is the state spine fresher than the last checkpoint/commit (HR4)?
  5. Did the last package stay inside its territory and leave `workspace-guard --check` clean?
- The verdict is exactly one of `on-track`, `correction-applied`, `decision-needed`. Only `decision-needed` is
  surfaced (fast-fail); the other two are recorded and the loop continues.
- The audit is a statement, never an approval request: it MUST NOT end with a question to the user.
- Two consecutive audits flagging the same drift escalate as a recurring anomaly (fast-fail growth rule).

## Rules

- All five parts are present. An inapplicable part carries `n/a` and a reason; omission is a defect.
- At most one configuration/concurrency/roster change per checkpoint. An explicit human goal edit does not count toward this cap.
- A checkpoint file is committed by the driver immediately after U4 as a driver record, not as a stage deliverable.
- **Rollback**: at the next checkpoint, revert the prior change when U4 fails, new test failures appear versus the stage baseline, `retries_package` increases by at least two, or `parallelism_efficiency` drops by at least 30 percent. A rolled-back change is not re-proposed immediately.
- `coordinate` remains territory-overlap only; with one temporary team it is a recorded no-op.
- The checkpoint carries paths and verdicts, never raw transcripts or fabricated metrics.
- **Direction audit is mandatory**: every checkpoint carries part 5; a checkpoint without it is a defect. Its reload tier and verdict are recorded in the checkpoint, not only in the conversation.
- **No approval request**: a checkpoint's outcome is a statement; asking the user to continue violates HR1 and is itself a drift signal.
- **Workspace signature (2026-11-08 RCA)**: a stage that runs probes, tests or subagents MUST record the measured repository's signature before them and compare it after: `python3 scripts/python/workspace-guard.py --snapshot <spec-dir>/test-evidence/workspace-<stage>.json --repo <repo>` then `--check`. A difference in branch, refs or `.specify/specs` fails the checkpoint — it means a probe or agent resolved its repository root outside its sandbox (the 2026-11-07 incident created 40 branches and spec dirs).

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

## 5. Direction audit
- reload tier: <T0 | T0+T1 | T2>
- Q1 rules: <which rules, each in force?> — <evidence>
- Q2 process: <verdict> — <evidence>
- Q3 next action: <verdict> — <evidence>
- Q4 spine freshness: <verdict> — <evidence>
- Q5 territory/workspace: <verdict> — <evidence>
- verdict: <on-track | correction-applied | decision-needed>
```
