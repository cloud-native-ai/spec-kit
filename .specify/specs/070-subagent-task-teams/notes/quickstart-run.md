# Quickstart Run — Feature 070 (T038)

**Run date**: 2026-10-25T07:52Z (segment impl-s7)
**Workspace**: `/tmp/wp-demo-070-s7` (fixture-only; removed at teardown)
**Driver mirror under test**: `.specify/skills/sdd-loop-driver/`
**Host/toolchain**: Linux `5.10.134-15.2.al8.x86_64`; `Python 3.11.11`; `pytest 8.4.2`

All fixtures were built with the test-only builders in `tests/fixtures/wp_fixtures.py`
(`make_two_package_plan`, `make_write_package`, `make_plan`, `make_spine`,
`make_manifest`, `plan_event`, `dispatch_event`, `settle_event`, `verdict_event`).
No fixture wrote the repository, a line registry, or a real state spine.

**Mirror-path scope**: Scenarios A, B, D, and E invoke the CLI scripts through
`.specify/skills/sdd-loop-driver/scripts/` exactly as the quickstart shows.
Scenarios C, F, and G are the quickstart's own pytest selectors over the
test-only simulator and the contract pins; `tests/` has no mirror, and those
tests execute the fixture algorithm they pin. The mirror scripts are exercised
by A, B, D, and E.

## Scenario A — Gate a decomposed plan

Command:

```sh
cd /tmp/sdd-worktrees/spec-kit/070-subagent-task-teams
python3 .specify/skills/sdd-loop-driver/scripts/wp-gate.py \
  --spine /tmp/wp-demo-070-s7/a/state.md --stage plan --stage-attempt 1 \
  --check plan --plan-json /tmp/wp-demo-070-s7/a/plan.json \
  --json-out /tmp/wp-demo-070-s7/a/wp/line-plan-a1-gate-plan.json
```

Real output (rc 0):

```json
{"schema_version": 1, "check": "plan", "stage": "plan", "verdict": "admit", "findings": [], "plan_hash": "sha256:356656864e1dbb18b9c0cd084afc361ce9d95ec7f289df78a920cd9bb66f32b0", "checked_at": "2026-10-25T07:52:17Z", "evidence_ptr": "/tmp/wp-demo-070-s7/a/wp/line-plan-a1-gate-plan.json", "dispatch_layers": [["plan-wp01", "plan-wp02"]], "integration_order": ["plan-wp01", "plan-wp02"]}
```

`--json-out` was written and carries the same verdict, findings, layers, and
integration order. Fixture: two independent read-only packages, `pattern=parallel`,
`slot_cap=2`.

## Scenario B — Reject a cyclic, orphaned, or overlapping plan

Command:

```sh
python3 .specify/skills/sdd-loop-driver/scripts/wp-gate.py \
  --spine /tmp/wp-demo-070-s7/b/state.md --stage plan --stage-attempt 1 \
  --check preflight --manifest /tmp/wp-demo-070-s7/b/manifest.json \
  --json-out /tmp/wp-demo-070-s7/b/wp/line-plan-a1-gate-preflight.json
```

Real output (rc 1):

```json
{"schema_version": 1, "check": "preflight", "stage": "plan", "verdict": "reject", "findings": [{"code": "cycle", "wp_id": null, "detail": "dependency cycle among: plan-wp02, plan-wp03"}, {"code": "orphan-output", "wp_id": null, "detail": "required output owned by no package: ghost.md"}, {"code": "path-overlap", "wp_id": "plan-wp01", "detail": "unordered write territories overlap: plan-wp01 / plan-wp02"}, {"code": "write-write-unordered", "wp_id": "plan-wp01", "detail": "unordered write territories overlap: plan-wp01 / plan-wp02"}], "plan_hash": "sha256:4f43feb8211e3c3a241c1156a54206ade58de7c87c8bb44901397d10b5655e22", "checked_at": "2026-10-25T07:52:29Z", "evidence_ptr": "/tmp/wp-demo-070-s7/b/wp/line-plan-a1-gate-preflight.json", "dispatch_layers": [], "integration_order": []}
```

Fixture note (disclosed): the first construction appended `ghost.md` to
`required_outputs` after `make_plan` had computed the canonical hash, so the
run also reported a fixture-construction `plan-hash-mismatch`. The fixture was
rehashed with `canonical_hash_of` and rerun; the output above is the corrected
run. No product code changed.

## Scenario C — Concurrent read-only dispatch and write serialization

Command:

```sh
python3 -m pytest -q tests/integration/test_wp_coordination_dry_runs.py \
  -k "concurrent_read_only or write_serialization"
```

Real output (rc 0): `2 passed, 17 deselected in 0.03s`.

## Scenario D — Verifier failure, retry delta, and escalation

Commands and real outputs:

```sh
GATE=.specify/skills/sdd-loop-driver/scripts/wp-gate.py

python3 "$GATE" --spine /tmp/wp-demo-070-s7/d/no-delta.md --stage plan \
  --stage-attempt 1 --check retry --wp-id plan-wp02 --wp-attempt 2
```

rc 1, `verdict=reject`, finding `retry-unchanged` (`"a second attempt without a
material delta"`), `dispatch_count=1`.

```sh
python3 "$GATE" --spine /tmp/wp-demo-070-s7/d/split.md --stage plan \
  --stage-attempt 1 --check retry --wp-id plan-wp02 --wp-attempt 2
```

rc 0, `verdict=admit`, `findings=[]`, `dispatch_count=1`. The spine carries one
`plan-wp02` dispatch and one amendment whose `retry_delta.scope.split_into`
names `plan-wp02-a` and `plan-wp02-b`.

```sh
python3 "$GATE" --spine /tmp/wp-demo-070-s7/d/no-delta.md --stage plan \
  --stage-attempt 1 --check retry --wp-id plan-wp02 --wp-attempt 3
```

rc 1, `verdict=reject`, finding `retry-exhausted` (`"attempt 3 is rejected"`),
`dispatch_count=1`.

## Scenario E — Stage close, report, and `not_evaluated`

Happy path:

```sh
python3 .specify/skills/sdd-loop-driver/scripts/wp-report.py \
  --spine /tmp/wp-demo-070-s7/e/state.md --stage plan --stage-attempt 1 \
  --stage-u4-at 1790000300 --manual-interventions 0 --sessions 1 \
  --out-dir /tmp/wp-demo-070-s7/e/reports
```

Real output (rc 0), metric projection of the printed JSON:

```json
{
  "line_id": "line-demo", "stage": "plan", "stage_attempt": 1,
  "decision": "decomposed", "pattern": "parallel", "slot_cap": 2,
  "wall_clock_seconds": 200,
  "critical_path_seconds": 130,
  "parallelism_efficiency": 0.575,
  "max_concurrent": 2,
  "overlap": true,
  "retries_package": 0, "retries_stage": 0,
  "stage_attempts": 1, "canonical_stages": 8,
  "stage_executions_per_canonical": 0.125,
  "manual_interventions": 0, "sessions": 1,
  "manual_interventions_per_session": 0.0,
  "token_cost": "not_evaluated"
}
```

The full stdout also carries the two `pass` verdict records and the four
evidence references. Both `line-demo-plan-a1-coordination.md` and
`line-demo-plan-a1-coordination.json` were written under
`/tmp/wp-demo-070-s7/e/reports/`; stdout equals the JSON report.

Deleted timestamp variant (`ended_at` removed from the `plan-wp02` settle
event; same CLI inputs, out-dir `reports-missing`), rc 0:

```json
{"wall_clock_seconds": 200, "critical_path_seconds": "not_evaluated", "parallelism_efficiency": "not_evaluated", "max_concurrent": "not_evaluated", "overlap": false}
```

`wall_clock_seconds` stays computable from the first dispatch and the supplied
U4 time; the three duration-derived metrics are the literal `not_evaluated`,
not zero.

Missing `--sessions` variant (out-dir `reports-no-sessions`), rc 0:

```json
{"manual_interventions": 0, "sessions": "not_evaluated", "manual_interventions_per_session": "not_evaluated"}
```

The intervention count stays reported; the per-session rate is
`not_evaluated`.

## Scenario F — Opt out and single-package fallback

Command:

```sh
python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_coordination.py \
  tests/integration/test_wp_coordination_dry_runs.py \
  -k "precedence or auto_requires or non_decomposed or fallback or every_stage_records or single_package or disabled_stage"
```

Real output (rc 0): `19 passed, 111 deselected in 0.07s`.

Covered walkthrough steps: feature-level `off` beats every override; the
stage override beats the stage map, which beats the built-in default; `auto`
requires `admit`, at least two packages, and the WG-13 benefit test; a
non-decomposed decision (`single-package`/`disabled`/`fallback`) runs the
unchanged standard stage path, records its decision in the plan fence, and
dispatches no partial package set.

## Scenario G — No nested driver, no persisted team

Command:

```sh
python3 -m pytest -q tests/integration/test_wp_coordination_dry_runs.py \
  -k "nested_driver or no_team_directory"
```

Real output (rc 0): `3 passed, 16 deselected in 0.04s`.

The cases assert that a prompt naming the driver, loading a skill, or carrying
loop logic is blocked and recorded; that a clean prompt is dispatched; and
that a decomposed stage creates no `.specify/teams/<slug>/` directory and no
`team.md`.

## Teardown

```sh
rm -rf /tmp/wp-demo-070-s7
test ! -e /tmp/wp-demo-070-s7 && echo "TEARDOWN_OK"
```

Real output: `TEARDOWN_OK` (rc 0).

## Claims

- Every scenario above exited with the recorded code; no scenario was skipped.
- This note makes no absolute wall-clock or efficiency claim. The Scenario E
  numbers come from a synthetic fixture spine and a caller-supplied U4 epoch;
  they prove the report derivation, not a benchmark result. The benchmark
  record is `notes/benchmark-070.md`.
