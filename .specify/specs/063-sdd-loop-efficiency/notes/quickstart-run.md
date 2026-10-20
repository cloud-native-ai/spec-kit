# Quickstart Runs — Feature 063

## S1 — medium fixture admitted

- Preparation: quickstart §准备 (`git init`, base commit, branch `012-medium`).
- Command: `python3 skills/external/sdd-loop-driver/scripts/admission-check.py --project "$FIXTURE" --base-ref "$BASE" --expected-branch 012-medium --requirements ... --tasks ... --checklists ... --entry-evidence ... --lines-manifest ... --json-out /tmp/063-admission.json`
- Exit: `0`
- JSON: `decision=fast-lane`, `measured.fr_count=12`, `measured.task_count=25`, seven criteria all `pass`, `checklist=skipped(fast-lane)`.
- Re-run after the mutation drill: same result (`0`, `fast-lane`, 12/25).

## S2 — large fixture refused fail-closed

- Command: the S1 form with `$FIXTURE_LARGE`, `--expected-branch 013-large`.
- Exit: `1`
- JSON: `decision=full-chain`, `measured.task_count=60`, criterion `a` = `fail`.
- Re-run after the mutation drill: same result (`1`, `full-chain`, 12/60).

## S3 — two-slot ledger and closure audit

- Preparation: quickstart §准备 (medium fixture + `state-spine-valid.md` copied to
  `/tmp/063-line-state.md`; fixture repo initialized and committed).
- Command: `python3 skills/external/sdd-loop-driver/scripts/audit-test-budget.py --spine /tmp/063-line-state.md --spec-dir "$WORK063/medium/.specify/specs/012-medium"`
- Exit: `0`
- Output:

```text
slots=baseline:1 closure:1 reruns=0 exceptions=0 unknown=0 environment_failures=0
stages=0 complete=0
status=ok
```

- The fixture spec dir carries no `test-evidence/` files, so the E3 completeness
  denominator is zero; the E2 fence (baseline + closure with `comm -13`) is the
  audited object. Skip-linkage, docs-only and stage-status cases are exercised
  with `tests/fixtures/sdd_loop_efficiency/test-evidence/` in
  `tests/unit/test_audit_test_budget.py`.
- Re-run after the mutation drill: same output, exit `0`.
- Cleanup: fixture tree and `/tmp/063-line-state.md` removed.

## S4 — derived live log and sentinel verdict

- 4a: derive `stream/non_terminal_sentinel.jsonl` → `/tmp/063-live-a.log`
  (last line is a prefixed progress line); status `exit=0 ... sentinel=0`;
  watcher exit `15` → `verdict=INCOMPLETE` (`reason=exit-record-no-sentinel`).
- 4b: derive `stream/result_sentinel.jsonl` → `/tmp/063-live-b.log`
  (last non-empty line `PLAN-DONE`); watcher with no status exits `0` →
  `verdict=DONE` (`reason=sentinel`).
- WATCH lines carry `stream=na`; with `--raw-stream` they report
  `stream=na|absent|growing|idle` and EVIDENCE adds `raw=`/`bytes=`, never
  changing the verdict.
- Re-run after the mutation drill: same results.

## S5 — local nohup survival and `--once` re-entry

- Command: the quickstart §S5 form (`export TMP063`; parent `bash -c` launches
  `nohup … </dev/null >runner-log 2>&1 &` and exits).
- `status-demo-plan`: `exit=0 at=… sentinel=1 … progress=stream detached=yes`.
- `log-demo-plan.log` last non-empty line: `PLAN-DONE`.
- Raw evidence: `raw-demo-plan.jsonl` 4 lines, receive-timestamp sidecar 4 lines.
- Re-entry snapshot: `watch-target.sh --once` → exit `0`,
  `verdict=DONE pid=dead sentinel=yes rc=0`; the completed stage is verified,
  not redispatched (status/raw unchanged in the integration test).
- Cleanup: temp state dir removed after the status file existed.

## S6 — plan change classification (undeclared → gate failure)

- Preparation: plan-repo fixture initialized and committed; one commit appends a
  marker to `.specify/specs/012-medium/plan.md`; the declarations file is empty.
- Command: `python3 skills/external/sdd-loop-driver/scripts/audit-plan-changes.py --repo "$FIXTURE_REPO" --base "$PLAN_BASE" --head "$PLAN_HEAD" --plan-owned plan.md --plan-owned data-model.md --plan-owned contracts --plan-owned quickstart.md --plan-owned research.md --plan-owned feature-ref.md --declarations /tmp/063-plan-edits.txt`
- Exit: `1`
- Output (relevant fields):

```json
{
  "touched_paths": [".specify/specs/012-medium/plan.md"],
  "declaration_lines": [],
  "undeclared": true,
  "classification": "undeclared",
  "diff_stats": [{"path": ".specify/specs/012-medium/plan.md", "added": 2, "deleted": 0}]
}
```

- The only touched artifact is `plan.md`; `touched_paths[]` carries the
  repo-relative path from `git diff --name-only` (T027). The driver classifies
  the final diff and fails the stage gate before PC-06 routing.
- Re-run after the mutation drill: same result (`1`, `undeclared=true`).
- Cleanup: fixture tree and `/tmp/063-plan-edits.txt` removed.

## S7 — pending (US5, recorded dry-run decision trace; non-CI)
