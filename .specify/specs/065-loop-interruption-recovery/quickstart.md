# Quickstart — Feature 065 Loop Interruption Awareness & Recovery

**Date**: 2026-10-21 | **Engine**: `skills/external/sdd-loop-driver/scripts/loop-state.py` (not implemented at plan time) | **Owner reference**: `skills/external/sdd-loop-driver/references/state-awareness.md`

The scenarios below are the acceptance walkthrough for the new layer. Each `loop-state.py` example carries a **per-example status line** naming its premises; none of those examples is executable until `/speckit.implement` lands the engine, and implementation MUST execute every one (including teardown) and paste the real output into `verification.md`. The baseline commands in § Baseline were executed now.

## S1 — Accident replay: one call reconstructs the incident (US1, P1)

**Fixture**: a line whose stage ran with `exit=1`, no sentinel, complete but uncommitted plan artifacts, and no watchbeat. This is the measured xuanji-doc 015 shape.

```bash
TMP=$(mktemp -d)
mkdir -p "$TMP/state" "$TMP/repo/.specify/specs/065-demo"
cd "$TMP/repo" && git init -q && git config user.email t@example.com && git config user.name t
printf '# plan\n' > .specify/specs/065-demo/plan.md
# ... research.md, data-model.md/contracts/, quickstart.md, feature-ref.md written here ...
printf 'exit=1 at=1700000000 sentinel=0 line=line-demo stage=plan event=status\n' > "$TMP/state/status-line-demo-plan"
printf 'ANOMALY: plan stopped after writing artifacts\n' > "$TMP/state/log-line-demo-plan.log"

python3 skills/external/sdd-loop-driver/scripts/loop-state.py --action snapshot \
  --line-id line-demo --run-id r20261021T000000Z-abcd --stage plan \
  --spine "$TMP/state/spine-line-demo.md" --state-dir "$TMP/state" \
  --spec-dir "$TMP/repo/.specify/specs/065-demo" --repo "$TMP/repo"

rm -rf "$TMP"
```

**Status: not executable at plan time.** Premises: the engine and its flags from contract LS; the artifact map from data-model E-09; the status/log formats from `stage-runner.sh`/`run-stage.sh`; git present; the fixture's plan artifact set complete. **Expected (contractual, to be measured)**: one JSON snapshot with `interruptions` containing `artifacts-without-completion` (and possibly `stale-signal` only if a conflicting carrier exists), `loop_state` derived from the `exit=1` record, `recovery_action=retry` because the last line is an `ANOMALY:` line, and exit 0. The operator makes no per-file manual inspection (SC-001).

## S2 — Dispatched but unwatched vs a normal window (US1/US2, P1)

**Fixture**: a live PID and a fresh heartbeat, no watchbeat. A second fixture has a fresh watchbeat written by the driver.

```bash
# fixture setup omitted: pid/status/heartbeat files per stage-runner.sh
python3 skills/external/sdd-loop-driver/scripts/loop-state.py --action snapshot \
  --line-id line-demo --run-id r20261021T000000Z-abcd --stage plan \
  --state-dir "$TMP/state" --spec-dir "$TMP/repo/.specify/specs/065-demo" --repo "$TMP/repo"

python3 skills/external/sdd-loop-driver/scripts/loop-state.py --action recover \
  --line-id line-demo --run-id r20261021T000000Z-abcd --stage plan \
  --state-dir "$TMP/state" --spec-dir "$TMP/repo/.specify/specs/065-demo" --repo "$TMP/repo" --apply
```

**Status: not executable at plan time.** Premises: the watchbeat filename/fields (SP-23–SP-26); the freshness threshold resolved from `watch-target.sh --help`; PID identity via `kill -0` + start token. **Expected**: the no-marker fixture reports `unwatched`, `recovery_action=watch`, and `recover --apply` writes only the marker (`event=watch-return`), no spine and no commit; the fresh-marker fixture reports `RUNNING` with no `unwatched` finding. A second immediate `recover --apply` returns `already-applied`.

## S3 — Retry isolates an old attempt's signals (US3, P1)

**Fixture**: a status file from an old `run_id`, a pid file from the old attempt, and a current spine whose `stage_started_at` is later than both.

```bash
python3 skills/external/sdd-loop-driver/scripts/loop-state.py --action recover \
  --line-id line-demo --run-id r20261021T000000Z-abcd --stage plan \
  --state-dir "$TMP/state" --spec-dir "$TMP/repo/.specify/specs/065-demo" --repo "$TMP/repo" --apply

ls "$TMP/state/attempts/"
```

**Status: not executable at plan time.** Premises: the old carriers' formats and mtimes; the isolation directory sequence (RC-19–RC-21); the attempt ceiling owner in `stage-prompts.md`. **Expected**: `recovery_action=retry`, `result=applied`, old files under `attempts/<attempt>-<run-id>-<epoch>/`, zero deletions, `spine_attempt` incremented exactly once, and the next dispatch sees a clean signal surface. A repeat returns `already-applied` and does not increment again.

## S4 — Resume commits only stage paths; salvage is explicit (US3, P1)

**Fixture**: complete plan artifacts, no sentinel, `exit=1`, no `ANOMALY:` line, an unrelated dirty file in the repo, and a spine with `spine_stage_base_commit`.

```bash
# First, without salvage: the decision must stay retry.
python3 skills/external/sdd-loop-driver/scripts/loop-state.py --action recover \
  --line-id line-demo --run-id r20261021T000000Z-abcd --stage plan \
  --state-dir "$TMP/state" --spec-dir "$TMP/repo/.specify/specs/065-demo" --repo "$TMP/repo"

# Then record the U4 salvage decision and apply.
python3 skills/external/sdd-loop-driver/scripts/loop-state.py --action recover --apply \
  --line-id line-demo --run-id r20261021T000000Z-abcd --stage plan \
  --state-dir "$TMP/state" --spec-dir "$TMP/repo/.specify/specs/065-demo" --repo "$TMP/repo" \
  --salvage --evidence "$TMP/state/log-line-demo-plan.log"

git -C "$TMP/repo" status --porcelain
git -C "$TMP/repo" log --oneline -1
```

**Status: not executable at plan time.** Premises: the six plan-owned paths; `spine_stage_base_commit`; the commit-message form (RC-13); the dirty unrelated file. **Expected**: the first call is `retry`; the second is `resume`, commits only the six plan-owned paths (the unrelated dirty file remains dirty and uncommitted), records `spine_salvage: accepted` with evidence and time before committing, and never starts a subagent. A repeat returns `already-applied`.

## S5 — Stop at the ceiling: four-element handoff, no kill (US3, P1)

**Fixture**: a line at the retry ceiling, with a dead process and a complete evidence set.

```bash
python3 skills/external/sdd-loop-driver/scripts/loop-state.py --action recover --apply \
  --line-id line-demo --run-id r20261021T000000Z-abcd --stage plan \
  --state-dir "$TMP/state" --spec-dir "$TMP/repo/.specify/specs/065-demo" --repo "$TMP/repo"

sed -n '1,80p' "$TMP/state"/handoff-line-demo-plan-*.md
```

**Status: not executable at plan time.** Premises: the retry ceiling from `stage-prompts.md`; the handoff filename (E-11); the watcher snapshot fields available from the last `--once`. **Expected**: `recovery_action=stop`, `result=applied`, exit 0; the spine is `stalled` with reason/evidence; the handoff contains the four elements and `process_action=none`; no process is signalled and no worktree is removed. A live-process fixture additionally carries `requires_explicit_decision=true`.

## S6 — `check-spine`: valid, invalid and legacy (US4, P2)

```bash
python3 skills/external/sdd-loop-driver/scripts/loop-state.py --action check-spine --spine "$TMP/state/spine-line-demo.md"
echo "exit=$?"
```

**Status: not executable at plan time.** Premises: the fenced schema (SP-01–SP-16); the legacy-degradation rule (SP-21). **Expected**: a valid `running` spine exits 0 with `ok=true`; a spine missing `spine_stage_deadline_epoch` or a carrier path exits 1 with a `violations[]` naming each field; a `stalled` spine without `spine_stall_reason`/`spine_evidence` exits 1; a legacy spine (no fence) exits 1 with `machine-segment-missing` while a snapshot of the same spine still evaluates with `schema=legacy` and `unknown` fields.

## S7 — Probe: remote unreachable is STALLED, never DEAD (US2, P1)

```bash
printf '%s\n' '{"schema_version":1,"reachable":false,"reason":"ssh-255"}' > "$TMP/probe.json"
python3 skills/external/sdd-loop-driver/scripts/loop-state.py --action snapshot \
  --line-id line-demo --run-id r20261021T000000Z-abcd --stage plan \
  --probe "$TMP/probe.json" --state-dir "$TMP/state" \
  --spec-dir "$TMP/repo/.specify/specs/065-demo" --repo "$TMP/repo"
```

**Status: not executable at plan time.** Premises: the probe envelope (E-10); the remote-unreachable finding (SN-35). **Expected**: `evidence_source=probe`, `loop_state=STALLED`, `interruptions=[remote-unreachable]`, `recovery_action=stop`, exit 0; no local watcher is invoked and `DEAD` never appears.

## Baseline — executed now

These two commands were run at plan time and are the regression floor for implementation.

```bash
$ bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test
SELF-TEST: 38 passed, 0 failed

$ python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver
DIFF  .specify/skills/sdd-loop-driver/SKILL.md
... (11 differing files, listed in research.md § 0.4) ...
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
EXIT=2
```

After implementation the expected mirror result is zero drift for the pair (the write resolves the disclosed baseline drift), and the watcher self-test remains 38/0 with identical verdict/exit pairs.
