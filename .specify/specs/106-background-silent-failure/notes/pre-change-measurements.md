# Pre-Change Measurements — implement P1 (T001)

Captured at implement start, before any edit, from the clean tree on branch
`106-background-silent-failure`. Every reading below is a command's real output; the
baseline full-suite log is preserved in full at
`test-evidence/implement-baseline-full.txt` (single-run evidence discipline).

## Tree identity

- `git rev-parse --short HEAD` → `907426e1c`
- `git status --short` → empty at capture time (the only later addition is the
  baseline names list this task itself requires)

## Preserved-surface readings (C1 / watcher)

- `sha256sum skills/external/sdd-loop-driver/scripts/watch-target.sh` →
  `955ddf7820a80cb3afad5af25877f2f8d7093e4fb08c46ec59dfe948ec3f2479`
  (= `fbab7a45c` baseline; the file is not edited by this feature)
- `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test | tail -1` →
  `SELF-TEST: 39 passed, 0 failed` (rc 0)

## Mirror / generated-copy baseline

- `.venv/bin/python scripts/python/sync-mirrors.py --check` → rc **0**;
  `ok shared/ == .specify/shared/ (116 files, byte-identical)`, six pairs ok,
  six projected rows ok
- `.venv/bin/python scripts/python/regen-command-copies.py --check` → rc **0**;
  `OK: all per-tool command copies match the source templates.`

## Confirmation-gate scan (EP-005 fallback basis)

`python3 scripts/python/scan-confirmation-gates.py --root . --json` → rc 0, **total 31**
(the frozen `== 27` equality is a disclosed pre-existing red at this base).

P1 touched declaration-surface file(s) and their per-file hit lines at base:

| Touched file | Hit lines at base |
|--------------|-------------------|
| `shared/definitions/superagent-definitions.md` | `[58]` |
| `scripts/python/role-edge-check.py` | not in scan scope (`shared/`, `skills/`, `templates/` only) |
| `tests/**` | not in scan scope |

## Engine baseline (`report` on an empty carrier set)

```
python3 scripts/python/role-edge-check.py --action report \
  --state-dir tests/fixtures/superagent-role/empty/state \
  --teams-dir tests/fixtures/superagent-role/empty/teams \
  --logs-dir tests/fixtures/superagent-role/empty/logs \
  --registry-dir tests/fixtures/superagent-role/empty/registry
```
→ rc 0, `"summary": {"edges": 0, "executors": 0, "violations": 0, "conflicts": 0}`;
`"action": "report"`, `"schema_version": 1`. This exact output is the byte-comparison
anchor for T008's `report`-unchanged leg.

## C2 carrier `.status` shape at base

`skills/internal/create-team/scripts/dispatch.sh:150`:
`echo "${LABEL} exit=${rc}" | tee "${LOG_DIR}/${LABEL}.status"`
— one line, written only at the end of the pipeline; no trap, no pid, no heartbeat.

## Red-first preconditions (artifacts absent at base)

- `tests/contract/test_settlement_*` → absent (six modules planned)
- `tests/fixtures/settlement/` → absent

## Baseline full-suite reading (implement slot = baseline; the only full run of this stage)

- command:
  `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh --full --names-out .specify/specs/106-background-silent-failure/baseline-failed.txt`
- rc **1**; passes=2 (parallel + 1 declared-serial test)
- parallel pass: `218 failed, 10048 passed, 3 skipped` in 71.62 s
- serial pass: `1 passed`
- failed-name list: `.specify/specs/106-background-silent-failure/baseline-failed.txt`
  (**218** sorted, de-duplicated nodeids) — the tree carries a large pre-existing red
  set that predates this package; GATE-5 is measured as `comm -13` against this list.
- full capture: `test-evidence/implement-baseline-full.txt` (449 KB)

Failed-nodeid capture and comparison form follow the owner
`.specify/skills/internal/implement-feature/SKILL.md` § Test runs (this file records only
paths and readings, never a second rule).

## Frozen coverage baseline

- `wc -l .specify/specs/106-background-silent-failure/coverage-baseline.txt` → **787**
  (read-only; not touched by this package)
