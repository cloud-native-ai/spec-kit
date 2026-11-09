---
id: "20261109T030015Z-skill-create-tasks"
unit_id: "skill:create-tasks"
unit_type: "skill"
run_id: "r20261109T030000Z-auto-git-closeout"
scope: "local"
probe: "skill-create-tasks-wrapup"
kind: "internal"
slice: "skills"
feature: "091-auto-git-closeout"
feature_id: "091"
partial: false
created: "2026-11-09T03:00:15Z"
summary: "Tasks stage on the 28-FR / 8-SC / 26-clause 091 spec produced `.specify/specs/091-auto-git-closeout/tasks.md` — 60 dependency-ordered rows across 8 phases (Setup 7, Foundational 8, US1 9, US2 9, US3 6"
---

## Review
Tasks stage on the 28-FR / 8-SC / 26-clause 091 spec produced `.specify/specs/091-auto-git-closeout/tasks.md` — 60 dependency-ordered rows across 8 phases (Setup 7, Foundational 8, US1 9, US2 9, US3 6, US4 6, US5 8, Polish 8 until recount), every row carrying `blockedBy` and a file-level verification surface, a 26-claim green partition, and a 28-row FR trace. Driven to `decomposition-check --mode tasks decision=proceed (fr 28 / tasks 60, both under ceiling)` and `pre-analyze-check --stage tasks decision=pass errors=0`, with `validate-tasks.py` at 0 errors and 46 warnings adjudicated rather than silenced. Three rulings recorded at generation (receipt directory, probe handler order 60, new reference filename) plus two gate readings retained in `test-evidence/`.

## Optimization Points
- `validate-tasks.py green-path-divergence` encodes "one green path per row", which is unsatisfiable for any feature whose clauses outnumber its test modules: 26 clauses all land in one contract module, so the check fires 45 times on a partition that is in fact exact. A green point is a (clause, first-green commit) pair, not a file; the check has no way to read "these rows assert different clauses of the same file" as legitimate.
- `pre-analyze-check.py` extracts task ids with `^- \[[ xX>~]\] (T\d{3})`, so a sub-row id such as `T010b` (accepted by `validate-tasks.py`, which is the tasks-file owner) is read as a duplicate of `T010` and fails the gate with 4 errors. Two scripts disagree on the same file's row grammar, and only one of them is the owner.
- Inserting a row mid-file is impossible without renumbering the whole tail, because ids are positional (`TNNN` dense) while `blockedBy` cites ids. The only escape is appending ids above the last row (T057…T060 here), which breaks the "rows ascend through phases" reading the Phase Map depends on.
- `account-clause-coverage.py` treats a missing `coverage-baseline.txt` as 603 errors with `status: baseline-missing`, and the freeze is a tasks-stage duty — so any consumer running the accountant *at* the tasks stage, rather than after implement, sees a hard fail that no tasks.md edit can clear. The gate and its own evidence row disagree about when the baseline is owed.
- Three-wrap-up-script interface friction: `run-determination.py --action determine` rejects `--user-turn-class` (a flag listed for the action), and `--names-current` silently means "a file of failed node ids", not the name list printed in the sibling stages' evidence, so the correctness axis stays `no_baseline` unless a pytest run produced a failed-nodeid file.

## Optimization Points
- validate-tasks.py green-path-divergence is unsatisfiable when clauses outnumber test modules; pre-analyze-check.py T\d{3} id grammar contradicts validate-tasks.py on sub-row ids; positional task ids make mid-file insertion impossible; account-clause-coverage.py hard-fails at the tasks stage over a baseline it says implement owes; run-determination.py --action determine rejects a flag it lists and --names-current means a file, not the printed name list
