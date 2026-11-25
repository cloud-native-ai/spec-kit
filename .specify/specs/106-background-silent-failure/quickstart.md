# Quickstart — Background Dispatch Settlement（106-background-silent-failure）

**Readers**: framework maintainers verifying the settlement contract after `/speckit.implement`; downstream maintainers checking what an upgrade changes.
**Reading scenario**: someone who has the repository checked out and wants to (a) see one silent-death attempt settle correctly, (b) see the preserved watcher surface stay unchanged, and (c) know exactly which scenarios are executable now versus after implementation.

**Reader baseline**: `shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 (the framework maintainer baseline; no stricter override declared here).

## Execution status of this page

Every executable example below is marked either **run-now** (executed while authoring this plan; the observed result is quoted and stored under `test-evidence/`) or **not-implemented-yet** (the `settle` action / additive records do not exist at plan time). A **not-implemented-yet** example lists its premises and the exact pinning test that makes it valid; it is never implicitly covered by a file-level disclaimer. Examples are bash blocks; run them from the repository root.

The `settle` action and the C2/C4 records are delivered by `/speckit.implement`; the commands in S-1…S-5 are therefore validated by the named contract tests, not by a plan-stage execution.

---

## S-0 — Read the single owner — run-now (reading, no command)

Read `shared/definitions/superagent-definitions.md` § Termination. It owns the closed seven-value set, the per-value evidence requirement and the three settlement violation kinds. Every other document on this page points at it; none restates the table.

**Premises**: the file exists at that path; the section heading is verbatim `**Termination.**` (the amendment lands there).

---

## S-1 — C2 subprocess silent death — not-implemented-yet

```bash
# 1. dispatch a fake CLI that blocks, then SIGKILL the wrapper from another shell
DISPATCH_CLI=/bin/sh DISPATCH_CLI_FLAGS="-c 'sleep 300'" \
DISPATCH_LOG_DIR=.specify/.tmp/settlement-demo/logs \
  bash skills/internal/create-team/scripts/dispatch.sh demo-kill . .specify/.tmp/settlement-demo/prompt.txt

# 2. after the wrapper is killed, judge the attempt
python3 scripts/python/role-edge-check.py --action settle \
  --logs-dir .specify/.tmp/settlement-demo/logs
```

**Expected after implementation**: the attempt row settles `silent-end`, carries `start` evidence (`.attempt`), `lack` evidence (no `.end`, no terminal record) and the pid-goes-away check; exit 0 because a correctly derived `silent-end` is a judged attempt, not a violation.

**Premises** (re-measure at implement time): (1) `dispatch.sh` accepts `DISPATCH_CLI` / `DISPATCH_CLI_FLAGS` and writes `<label>.attempt` before launching; (2) the wrapper pid is recorded and is killable; (3) `.specify/.tmp/` is git-ignored (measured: it is); (4) the `settle` action accepts `--logs-dir` and derives C2 attempts from it.
**Pinning tests**: `tests/contract/test_settlement_carriers.py::test_c2_silent_death`, `tests/contract/test_settlement_engine.py::test_settle_derives_silent_end`.

---

## S-2 — C1 verdict mapping — mixed

Run-now part (the watcher surface the mapping consumes):

```bash
bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test | tail -1
# observed: SELF-TEST: 39 passed, 0 failed
```

Extract the three preserved sets from the baseline copy (run-now; the same extractor is pinned in the test):

```bash
grep -oE '"(DONE|RUNNING|ANOMALY|FAILED|DEAD|TIMEOUT|INCOMPLETE|NO_SIGNAL)"' \
  .specify/specs/106-background-silent-failure/test-evidence/watch-target-fbab7a45c.sh | tr -d '"' | sort -u
grep -oE '^EXIT_[A-Z_]+=[0-9]+' \
  .specify/specs/106-background-silent-failure/test-evidence/watch-target-fbab7a45c.sh | cut -d= -f2 | sort -n -u
grep -oE '[A-Z][A-Z0-9_]*-DONE' .specify/specs/106-background-silent-failure/test-evidence/watch-help-baseline.txt | sort -u
# observed verdicts: ANOMALY DEAD DONE FAILED INCOMPLETE NO_SIGNAL RUNNING TIMEOUT
# observed exit codes: 0 2 10 11 12 13 14 15 16
# observed sentinel literal: STAGE-DONE
```

Not-implemented-yet part: `python3 scripts/python/role-edge-check.py --action settle --state-dir <state> --logs-dir <logs>` judges a stage fixture and maps `DONE → completed`, `FAILED → failed`, `ANOMALY → anomaly`, `INCOMPLETE → failed (incomplete)`, `DEAD`/`NO_SIGNAL → silent-end`, `RUNNING`/`TIMEOUT → running` only with a fresh live check.

**Premises**: the four-piece names are as measured (`pid-`, `status-`, `log-`, `heartbeat-<line>-<stage>`); the baseline copy in `test-evidence/` is byte-identical to `fbab7a45c` (sha `955ddf78…`); the `settle` action reads the stage sidecar/spine for role/attempt identity.
**Pinning tests**: `tests/contract/test_settlement_preservation.py::test_watcher_sets_equal_baseline`, `tests/contract/test_settlement_engine.py::test_c1_verdict_mapping`.

---

## S-3 — Team seat settlement — not-implemented-yet

```bash
python3 scripts/python/role-edge-check.py --action settle \
  --teams-dir .specify/teams --logs-dir .specify/agents/execution/logs
```

**Expected after implementation**: each mapping row carries `end_state` + `evidence`; a versioned row missing either is `settlement-unrecorded` (exit 1); a `completed` row with no evidence pointer is `settlement-unbacked`; a 5-column legacy report still parses, is annotated `legacy`, and is exempt from `settlement-unrecorded` (exit 0 — its absent cells are absent columns, not an unrecorded claim).

**Premises**: new reports use the 7-column header `label | role | dispatch_duty | workspace | parent | end_state | evidence`; legacy 5-column headers remain accepted; `## Verification` carries the settlement-coverage declaration; each seat has an E2 start record (`<label>.attempt`, carrier `c3-team-seat`) or the same label's C1/C2 start evidence — a seat with a start record but no report row settles `silent-end`, and a seat with neither start record nor row is `unknown` (`start-record-missing`).
**Pinning test**: `tests/contract/test_settlement_carriers.py::test_team_report_5_and_7_columns`.

---

## S-4 — Legacy vs versioned audit — not-implemented-yet

```bash
python3 scripts/python/role-edge-check.py --action settle \
  --logs-dir tests/fixtures/settlement/legacy/logs --format json
```

**Expected after implementation**: the legacy fixture's findings carry `legacy: true`, a derived verdict is still produced, the exit code is 0 (annotation is not a refusal); the versioned fixture's findings carry `settlement_version: 1` and are audited as claims. Unreadable evidence in either fixture exits 2 with `unknown` findings naming the pointer.

**Premises**: the fixture pair exists under `tests/fixtures/settlement/{legacy,versioned}/logs`; `--format json` is the engine's default output.
**Pinning test**: `tests/contract/test_settlement_migration.py::test_legacy_annotated_not_compliant`.

---

## S-5 — Mutation drill — not-implemented-yet (implement-stage evidence)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_settlement_engine.py tests/contract/test_settlement_carriers.py -q
```

**Expected after implementation**: green on the unmodified tree; for each of the four drills (remove silent-end detection; remove the liveness requirement; make `unknown` exit 0; remove the evidence-pointer requirement) at least one test red, recorded with its command and output under `test-evidence/mutation-drill.md`.

**Premises**: the settlement engine and carriers exist; the host needs `SPECKIT_PYTHON=/usr/local/bin/python3` because the repo `.venv` carries no pytest (measured); the drill edits are reversed after each run (history keeps nothing).
**Pinning tests**: the drill matrix rows in `test_settlement_engine.py` / `test_settlement_carriers.py`; evidence duty in `contracts/enforcement-and-migration.contract.md` C-30.

---

## S-6 — Preserved surfaces — run-now

```bash
bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test | tail -1
# observed: SELF-TEST: 39 passed, 0 failed

sha256sum skills/external/sdd-loop-driver/scripts/watch-target.sh \
  .specify/specs/106-background-silent-failure/test-evidence/watch-target-fbab7a45c.sh
# observed: both 955ddf7820a80cb3afad5af25877f2f8d7093e4fb08c46ec59dfe948ec3f2479

python3 scripts/python/scan-confirmation-gates.py --root . --json | head -3
# observed: "total": 31 — pre-existing at the stage base; the pinned == 27 test is red at base (EP-005 fallback:
# this feature is measured by zero NEW hits on the files it touches)

python3 scripts/python/role-edge-check.py --action report \
  --state-dir .specify/.tmp/sdd-loop/tmp/background-silent-failure/qs-probe/state \
  --teams-dir .specify/.tmp/sdd-loop/tmp/background-silent-failure/qs-probe/teams \
  --logs-dir .specify/.tmp/sdd-loop/tmp/background-silent-failure/qs-probe/logs \
  --registry-dir .specify/.tmp/sdd-loop/tmp/background-silent-failure/qs-probe/none
# observed: rc 0, summary {"edges":0,"executors":0,"violations":0,"conflicts":0}
```

**Teardown (verified)**: `rm -rf .specify/.tmp/sdd-loop/tmp/background-silent-failure/qs-probe` — the scratch tree lives under the sanctioned, git-ignored `.specify/.tmp/`; the observed output is preserved in `test-evidence/quickstart-role-edge-empty-report.json`.

**Premises**: the watcher file is unchanged since `fbab7a45c` (measured by sha); the scanner's scan scope is `templates/commands`, `templates/*.md`, `skills`, `shared`; the engine `report` action accepts the four roots and exits 0 on an empty edge set (observed).
**Pinning tests**: `tests/contract/test_settlement_preservation.py` (sets + self-test + per-file gate hit-set), `tests/contract/test_role_edge_engine.py` (report schema unchanged).

---

## S-7 — Mirrors and the unique test entry — mixed

Run-now:

```bash
.venv/bin/python scripts/python/sync-mirrors.py --check
# observed: rc 0 — six pairs ok, six projected rows ok (baseline for "no NEW drift")

.venv/bin/python scripts/python/regen-command-copies.py --check
# observed: OK: all per-tool command copies match the source templates.
```

Not-implemented-yet:

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_settlement_contract_definitions.py \
  tests/contract/test_settlement_engine.py \
  tests/contract/test_settlement_carriers.py \
  tests/contract/test_settlement_migration.py \
  tests/contract/test_settlement_preservation.py \
  tests/contract/test_settlement_scope.py -q
```

**Expected after implementation**: all six modules green; the mirror pair this feature touches reports no NEW drift; no third full-suite slot is consumed.

**Premises**: the six modules and `tests/fixtures/settlement/` exist; the mirrors are regenerated with `.venv/bin/python` (the generator needs `typer`); the runner override is the measured interpreter premise.
**Pinning tests**: the six modules themselves; mirror parity is already guarded by the existing mirror suite.
