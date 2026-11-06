# Quickstart — Feature 085

All scenarios assume repo root `/storage/project/cloud-native-ai/spec-kit` and a clean feature branch. Commands are examples; expected results are the invariant, not a promise about a specific host.

## S1 — Read global and temporary scopes

```bash
python3 scripts/python/goal-utils.py resolve-scope --scope global --json
python3 scripts/python/goal-utils.py resolve-scope --scope spec \
  --spec-dir .specify/specs/085-sdd-temporary-goal-team --json
```

Expected: the first returns `.specify/goal` + `.specify/teams`; the second returns the spec-local `goal/` + `team/`; both exit 0. With both candidates and `--scope auto`, expected exit 2 `scope-ambiguous`.

## S2 — Create a temporary goal after requirements

```bash
python3 scripts/python/goal-utils.py create 085-sdd-temporary-goal-team \
  --scope spec --spec-dir .specify/specs/085-sdd-temporary-goal-team \
  --objective "<end-state outcome>" --criterion "<degree criterion>"
```

Expected: `goal/goal.md` under the spec; no `.specify/goal/` write; the objective is an outcome and the criteria do not repeat `SC-` rows.

## S3 — Create a temporary team after clarify + plan

```bash
/speckit.team create --scope spec --spec-dir .specify/specs/085-sdd-temporary-goal-team \
  --goal 085-sdd-temporary-goal-team --pattern parallel --isolation worktree
```

Expected: `team/team.md` with `scope: spec`, `goal_slug`, `stage_seats`, and `config.agent_concurrency`; every `stage_seats` key is a canonical SDD stage.

## S4 — Run a stage with concurrency and record the effective value

```bash
# The driver records U0; a stage dispatch must carry:
# agent_concurrency_requested=24, agent_concurrency_effective=<n>, agent_concurrency_reason=<reason>
python3 skills/external/sdd-loop-driver/scripts/wp-report.py --spine <spine> --stage implement --out-dir <reports>
```

Expected: the report and dispatch events carry requested/effective values; if the host cannot support 24, the reason is named and the effective value is lower.

## S5 — Inspect a child worktree and integration result

```bash
python3 skills/external/sdd-loop-driver/scripts/line-registry.py --action list --format json
git worktree list
```

Expected: each writing agent has a child line with `parent_line_id`, `line_role=agent-write`, its own worktree/branch, and an integration result; a merged child is removed only after `merged`; a failed child retains its worktree and evidence.

## S6 — Inspect a checkpoint and the closure record

```bash
sed -n '1,160p' .specify/specs/085-sdd-temporary-goal-team/checkpoints/01-requirements.md
sed -n '1,160p' .specify/specs/085-sdd-temporary-goal-team/checkpoints/closure.md
```

Expected: every checkpoint carries artifact verification, goal degree rows, at most one config proposal, and the next stage's concurrency/roster decision; `closure.md` carries the terminal goal degree table and the archived team state.

## Verification pointers

- Scope contract: [`contracts/scope-resolution.md`](contracts/scope-resolution.md)
- Temporary Goal/Team contract: [`contracts/temporary-goal-team.md`](contracts/temporary-goal-team.md)
- Concurrency/worktree contract: [`contracts/concurrency-and-worktrees.md`](contracts/concurrency-and-worktrees.md)
- Checkpoint/agent contract: [`contracts/checkpoint-and-agents.md`](contracts/checkpoint-and-agents.md)
- Stage-agent contract: [`contracts/stage-agents.md`](contracts/stage-agents.md)
- Requirement mapping: [`feature-ref.md`](feature-ref.md)
