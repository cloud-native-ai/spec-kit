# Quickstart Run Record — Feature 078 (T028, T029)

**Date**: 2026-10-30
**Scope**: quickstart scenarios 1, 2, 3, 4, 5 — every block below is the real output of the
command shown, run against this tree. Scenario 5's teardown targets the run directory that
scenario 2 actually produced (run-id back-filled from that run, never hard-coded).

**Transport note (read first).** Scenario 2's single dispatch was executed by a one-shot
runner that loads `tests/fixtures/coaching/fixture-trainee/SKILL.md` by explicit path and
follows its Workflow literally, emitting one event per step. No host-native subagent was
offered to this stage, so the run records `mode: run-skills-explicit-path`,
`self-report` rows from the runner's event log, and the substitution is stated verbatim in
the DispatchRecord `anomaly-line` instead of being presented as host telemetry. Nothing in
the four artifacts claims a `host-event` channel.

---

## Scenario 1 / 3 — shell-level verification (T028)

### 1.1 Coach's own class binding

```text
$ python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "skill:coaching-skills"
unit_id: skill:coaching-skills
flow_class: execution
flow_type: null
source: ledger
marker: null
basis: behavior-oracle
neutral: false
rc=0
```

`source: ledger` / `execution` / `behavior-oracle`, exit 0 — the T025 reading the task
names.

### 1.2 Ledger and probe registry are internally consistent

```text
$ python3 .specify/scripts/python/flow-class-check.py --action check
flow-class check: 79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]
coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39
rc=0

$ python3 scripts/python/probe-utils.py --action probes --validate
Probe registry valid: 10 classes, 117 internal + 0 external objects
rc=0

$ python3 scripts/python/probe-utils.py --action compile-embeds --check
compile-embeds --check: 75 units, zero drift
rc=0
```

`matched=79` as the task requires; the unit count stays 75 because a rename removes one
unit and adds one.

### 1.3 Derived faces carry no drift and no stale copy

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (406 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (117 files)
ok    shared/ == .specify/shared/ (60 files)
rc=0

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
rc=0

$ test ! -e .specify/skills/think-skills
rc=0
```

### Gate summary (SC-008 companion reading)

```text
$ python3 scripts/python/scan-confirmation-gates.py --summary
blocking confirmation gates: 27
  destructive: 20
  governance_kept: 7
violations (reversible gates still blocking): 0
rc=0
```

Same total as the pre-change baseline (`blocking=27` = destructive 20 + governance_kept 7,
`violations=0` — `test-evidence/gate-newline-baseline.txt`). The judged unit for SC-008 is
the **added line**, not the total; that reading is in `verification.md` § SC-008.

### Scenario 3 — the upgrade path on a disposable fixture

Two throwaway projects under `.specify/.tmp/coaching-078/fixture-cleanup/` (deleted by the
run), calling the real `specify_cli.cleanup_obsolete_framework_assets`:

```text
entity: old dir exists before = True
entity: removed entries = ['.specify/skills/think-skills']
entity: old dir exists after  = False (expected False)
linked: symlink exists before = True
linked: removed entries = []
linked: symlink kept after    = True (expected True)
linked: target untouched      = True (expected True)
scenario3 verdict: pass
rc=0
```

An entity directory is deleted; a user-authored symlink of the same name survives and its
target is untouched — SC-007's two halves. `specify init` itself was not run here: the
cleanup function is the unit the upgrade path adds, and `test_coaching_wiring_contract.py`
C-4 pins the same two behaviours as contract tests.

---

## Scenario 2 — one real coaching loop (T029)

**Run**: `coaching-skills tests/fixtures/coaching/fixture-trainee "<the brief in
tests/fixtures/coaching/work.md>"`, optimization set to `skipped`, Trainee files untouched
(the brief is a byte copy at `.specify/.tmp/coaching-078/run1-work/work.md`, which is where
the Trainee wrote `checklist.md`).

**Ordering evidence** — expectation on disk before the first dispatch action:

```text
expectation.md mtime : 1793349175.2307684  (= 2026-10-30T08:32:55.230768Z)
dispatched-at        : 2026-10-30T08:32:58.017522+00:00
```

**Runner return** (the dispatched side):

```text
$ python3 .specify/.tmp/coaching-078/trainee-runner/run_fixture_trainee.py \
    --trainee tests/fixtures/coaching/fixture-trainee \
    --work-dir .specify/.tmp/coaching-078/run1-work \
    --events .specify/.tmp/coaching-078/run1-events.jsonl
trainee=fixture-trainee steps=7 rows=4/5
anomaly-line: none; transport=scripted-one-shot-runner (no host-native subagent was offered to this stage) - every step row is self-report from this runner's event log
```

**The Trainee's primary artifact** (exists, and carries both planted defects):

```text
$ cat .specify/.tmp/coaching-078/run1-work/checklist.md
| # | item | status |
|---|---|---|
| 1 | Build passes. | PENDING |
| 2 | Unit tests pass. | PENDING |
| 3 | Migration dry-run succeeds. | PENDING |
| 5 | On-call owner is named. | PENDING |
```

Item 4 (`Rollback plan is written`) is missing — the planted correctness defect; the step
table records 5 brief reads for 4 rows — the planted efficiency regression.

**Four artifacts, run-shape validator** (the validator the run contract owns, imported from
`tests/contract/test_coaching_run_contract.py`):

```text
run_dir: .specify/memory/coaching/20261030T083250Z-fixture-trainee
artifacts: ['deviations.md', 'expectation.md', 'improvement-plan.md', 'observation.md']
expectation mtime: 1793349175.2307684
validator errors: []
verdict: pass
```

`validate_run(run_dir, primary_artifact_exists=True, oc1_met=False)` returned no error: four
artifacts and no fifth, both expectation dimensions present, exactly one dispatch, the
expectation older than the dispatch, closed status domains, and `run: partial` +
`optimization: skipped` consistent with the FR-017 boundary.

**What the four records say**

| Artifact | Content highlights |
|---|---|
| `expectation.md` | `## Outcome Correctness` (`OC-1` = the checklist itself, `OC-2` = header/PENDING) and `## Process Efficiency` (`PE-1` = 1 read + 1 write, `PE-2` = validation-gap); assumptions, unknowns, forbidden side effects, Trainee failure semantics |
| `observation.md` | one `## Dispatch`, seven step rows, every row `source: self-report`, `gap-count: 0`, `## Result` = `completed` |
| `deviations.md` | `D-1` result-deviation (4 of 5 rows, evidence S6 + checklist.md, high); `D-2` process-deviation (5 brief reads, evidence S1-S5, medium); `## Readings` separates the two readings |
| `improvement-plan.md` | `I-1` → `Workflow` step 3 (drop the item-4 exemption), `I-2` → `Workflow` step 2 (reuse the collected list); `## Run Status`: `run: partial`, `optimization: skipped` |

---

## Scenario 4 — degraded path: `improve-skills` unavailable (T029)

A one-shot copy at `.specify/.tmp/coaching-degraded/` with `improve-skills` removed from
**both** layers:

```text
absent: skills/external/improve-skills/SKILL.md
absent: skills/internal/improve-skills/SKILL.md
absent: .specify/skills/improve-skills/SKILL.md
absent: .specify/skills/internal/improve-skills/SKILL.md
```

The same loop was driven again (new run-id, its own run directory inside the copy):

```text
run_dir: .specify/.tmp/coaching-degraded/.specify/memory/coaching/20261030T083352Z-fixture-trainee
expectation mtime: 1793349232.678042   (dispatched-at 2026-10-30T08:33:52.678078+00:00)
artifacts: ['deviations.md', 'expectation.md', 'improvement-plan.md', 'observation.md']
validator errors: []
run-not-failed: True
```

`improvement-plan.md` § Run Status reads `run: partial` + `optimization: unavailable`: the
Trainee's output is still delivered, the unavailable optimization does not cap the
execution, and the run never degrades to `failed` for lack of `improve-skills`.

---

## Scenario 5 — teardown on the run that actually ran (T029)

`RUN_ID` was back-filled by cross-checking the run report (`expectation.md` § Run header)
with the directory name — never hard-coded:

```text
$ ls -1 .specify/memory/coaching
20261030T083250Z-fixture-trainee
reported-run-id=20261030T083250Z-fixture-trainee
dir-name=20261030T083250Z-fixture-trainee
backfill-agrees=yes
backfilled RUN_ID=20261030T083250Z-fixture-trainee

$ test -d ".specify/memory/coaching/$RUN_ID"; echo "test -d rc=$?"
test -d rc=0

slug=fixture-trainee
claim-path=.specify/memory/coaching/.optimization-claims/fixture-trainee
claim-state=absent (optimization: skipped -> owner mandates no claim)

$ rm -rf ".specify/memory/coaching/$RUN_ID"; echo "rm -rf rc=$?"
rm -rf rc=0

$ rm -f "$CLAIM"; echo "rm -f rc=$?"
rm -f rc=0

$ test ! -e ".specify/memory/coaching/$RUN_ID"; echo "test ! -e run-dir rc=$?"
test ! -e run-dir rc=0
$ test ! -e "$CLAIM"; echo "test ! -e claim rc=$?"
test ! -e claim rc=0

$ find .specify/memory/coaching -maxdepth 2 -print
.specify/memory/coaching
```

The `test -d` came **before** the removal, so the later `test ! -e` proves a real deletion
rather than a name that never existed. The Trainee slug derived from `RUN_ID` is
`fixture-trainee`; because scenario 2 recorded `optimization: skipped`, `data-model.md`
§ Optimization claim mandates no claim, and none was present — there was therefore no
crash leftover to attribute and report. The `rm -f` is still executed as the owner's
clearing step (a no-op here) and the final assertion covers both paths.

The degraded copy (`.specify/.tmp/coaching-degraded/`) is scratch under the sanctioned temp
root and was removed with it at wrap-up; the run record above is its evidence.
