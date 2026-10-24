# Pre-change Measurements — Feature 070

**Captured**: 2026-10-24T17:04:08Z (before the first implementation edit)
**Captured by**: implement segment impl-s1 (T001)
**Purpose**: freeze the dated control values that T037 (mirror sync) and T039 (closure) compare against.

## Host and toolchain

| Probe | Real output |
|-------|-------------|
| Host | `Linux 5.10.134-15.2.al8.x86_64 x86_64` |
| `python3 --version` | `Python 3.11.11` |
| `python3 -m pytest --version` | `pytest 8.4.2` |

## Git state at capture

| Probe | Real output |
|-------|-------------|
| `git rev-parse HEAD` | `0df504b989649ec4e7509a35789e0504631a0475` |
| `git status --short` | `?? .specify/specs/070-subagent-task-teams/test-evidence/analyze-rerun-report.md` and `?? .specify/specs/070-subagent-task-teams/test-evidence/analyze-rerun.jsonl` (pre-existing untracked analyze-rerun evidence; not created or modified by this segment) |

## Mirror baseline

Command:

```sh
python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver
```

Real output (rc 0):

```text
scope --only: skills/external/sdd-loop-driver
ok    skills/external/ == .specify/skills/ (28 files)
```

This is the clean **28-file** source/mirror pair baseline T037 and T039 compare against. `.specify/skills/sdd-loop-driver/` is generated and must never be hand-edited.

## Targeted driver baseline (not the E2 baseline)

Command:

```sh
python3 -m pytest -q tests/unit/test_decomposition_check.py tests/unit/test_pre_analyze_check.py \
  tests/unit/test_overlap_check.py tests/contract/test_sdd_loop_driver_gates.py \
  tests/contract/test_sdd_loop_driver_skill.py
```

Real output: rc 0, `65 passed in 15.98s`.

This is a targeted baseline for the existing driver suite. It is deliberately **not** the E2 full-suite baseline; that slot is captured once, separately, at implement start (T002) and recorded in the transport spine's test-budget fence.

## Clause-form probe (disclosed tooling limitation)

Command:

```sh
python3 .specify/scripts/python/clause_extract.py .specify/specs/070-subagent-task-teams/contracts/*.md
```

Real output (rc 0): every contract file is classified `form=md-none`, `clauses=0`, and is tagged `UNPARSABLE-NAMED`:

```text
fallback-and-nonregression.md	form=md-none	clauses=0
observability-and-retry.md	form=md-none	clauses=0
scheduler-and-dispatch.md	form=md-none	clauses=0
stage-team-adapter.md	form=md-none	clauses=0
verification-and-integration.md	form=md-none	clauses=0
work-package-model.md	form=md-none	clauses=0
wp-gate.md	form=md-none	clauses=0
```

Cause: the extractor recognizes only the closed `C-\d+` clause form; Feature 070's contracts use domain-prefixed ids (WP/WG/SD/VI/ST/OR/FN). This is a tooling limitation, not a coverage drop: clause coverage is fixed by `tasks.md` § Clause Coverage Model and will be checked mechanically by T039 against the frozen inventory in `notes/contract-clause-inventory.txt`.

## Clause counts re-measured for the inventory control

| Contract file | Domain clauses |
|---------------|----------------|
| `work-package-model.md` | 18 |
| `wp-gate.md` | 18 |
| `scheduler-and-dispatch.md` | 16 |
| `verification-and-integration.md` | 14 |
| `stage-team-adapter.md` | 12 |
| `observability-and-retry.md` | 16 |
| `fallback-and-nonregression.md` | 16 |
| **Total** | **110** |

## Consumption

- **T037** compares `sync-mirrors.py --check` against the 28-file baseline above.
- **T039** compares closure drift against the same 28-file baseline and the full-suite name list captured at T002 (`baseline-failed.txt`).
- No value in this note was inferred; each row is the recorded output of the command shown.
