# Plan-stage deterministic checks — Feature 074

Recorded 2026-10-28 during `/speckit.plan` for
`.specify/specs/074-goal-team-sdd-unification`. Every line below is a command that was actually
run in this repository, followed by its real output. Nothing here is a pre-written expectation.

Test budget for this stage: **targeted-set-v1**, plus `status=not-run-docs-only` for the full
suite (no source file was edited by this stage, so the full suite has no new subject).

## 1. Contract clause extraction

```bash
python3 scripts/python/clause_extract.py .specify/specs/074-goal-team-sdd-unification/contracts/*.md
```

```text
authorization-and-probe.md	form=md-bold-closed	clauses=16
diffusion-and-compat.md	form=md-bold-closed	clauses=13
nested-invocation.md	form=md-bold-closed	clauses=16
report-and-attribution.md	form=md-bold-closed	clauses=8
route-decision.md	form=md-bold-closed	clauses=14
```

Total 67 clauses, all canonical `md-bold-closed`, ids contiguous C-1…C-67 across the five files
(file order above is alphabetical, not clause order). FR/SC citation-group coverage, measured with
`grep -oE 'FR-0[0-9]{2}'` / `'SC-0[0-9]{2}'` per file and unioned: 28/28 FR, 8/8 SC.

## 2. Clause and FR coverage accounting

```bash
python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074-goal-team-sdd-unification
```

```text
FR universe: 28
FR claimed: 28
FR uncovered: 0

ERROR frozen baseline not found: .specify/specs/074-goal-team-sdd-unification/coverage-baseline.txt
companion (must be non-empty on a green run): claimed clauses 0, scanned files 208, clause universe 1238, FR universe 28
  [clause-uncovered] fail (562) — 562 uncovered, 562 beyond the frozen baseline
  [fr-uncovered] pass (0) — 28 of 28 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id under the owner's forms
  [coverage-baseline-delta] fail (562) — baseline holds 0 names
status: baseline-missing
rc=2
```

**Reading (no suppression)**: the FR lane is green (28/28). The clause lane is red **by design at
this stage** and is not claimed as green: clause claims are `[green:]` rows in `tasks.md`, which
does not exist yet, and the frozen baseline belongs to the tasks stage. Freezing a baseline now
would record zero claimed clauses and make the tasks stage trivially green — the failure mode the
`[coverage-baseline-delta]` line exists to prevent. The `clause-unparsable` advisory covers 94
pre-existing files across the repository corpus, unrelated to this spec.

## 3. Cross-artifact pre-analyze gate (plan stage)

```bash
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py \
  --spec-dir .specify/specs/074-goal-team-sdd-unification --stage plan
```

```text
pre-analyze-check: stage=plan decision=pass errors=0 advisories=0 waived=0
{"stage": "plan", "decision": "pass", "findings": [], "summary": {"errors": 0, "advisories": 0,
 "waived": 0, "fr": 28, "sc": 8, "tasks": 0, "clauses": 0, "files": 12},
 "checked_at": "2026-10-28T13:41:01Z"}
rc=0
```

`clauses=0` is a known reading of this checker, not an absence of clauses: its legacy prefix
pattern does not match the canonical `**C-N**` form (recorded the same way by Features 071 and
072). The clause count is taken from § 1 instead.

## 4. Mirror and per-tool copy baseline

```bash
python3 scripts/python/sync-mirrors.py --check       # rc=0
python3 scripts/python/regen-command-copies.py --check  # rc=0
```

```text
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (405 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (113 files)
ok    shared/ == .specify/shared/ (58 files)
```

Zero pre-existing drift. The plan's mirror criterion is therefore both "no NEW drift" and
measurably "clean".

## 5. Flow-class ledger unchanged

```bash
python3 scripts/python/flow-class-check.py --action check
```

```text
flow-class check: 79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]
coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39
rc=0
```

Confirms this feature adds no flow unit (no new command, no new skill) — the ledger stays at 79
units with zero findings, which is the FR-028 / C-67 negative check.

## 6. Targeted contract suite baseline

See `targeted-set-v1-baseline.txt`: 13 files, `191 passed`, `rc=0`, `duration_ms=23138`.
Selection basis: the suites that pin every surface this feature will touch — the anti-nesting and
dispatch-governance cases, the neutral metadata schema and tool mapping, the driver skill, the team
command routing, goal definition, the instructions section propagation and size budget, and the
flow-class ledger. Sufficiency: the same set is the pre-change case set for the FR-026/FR-027
containment claims (frozen as collected node ids at implementation start, per contract C-62).

## 7. Instructions size baseline

```bash
grep -n '^INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh
wc -c .specify/instructions.md templates/instructions-template.md
```

```text
38:INSTRUCTIONS_BUDGET_BYTES=32768
 41948 .specify/instructions.md
 34666 templates/instructions-template.md
```

Both files are over the budget before this feature. The new ambient section's acceptance is a
declared per-section byte ceiling plus a measured delta, never an absolute "fits the budget" pass.
