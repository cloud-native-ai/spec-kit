# Plan-stage checks (071) — what was run, what it means, what is expected to be red

**Date**: 2026-10-27 | **Base commit**: `884e7a86` | **Stage**: plan
**Purpose**: a dated record of every deterministic check this stage ran, the exact verdict, and — for the checks that cannot pass at plan time — the reason they cannot, so a later stage does not read an expected red as a defect or an expected advisory as a clean run.

## 1. `pre-analyze-check.py --stage plan` — decision `pass`

```text
pre-analyze-check: stage=plan decision=pass errors=0 advisories=20 waived=0
summary: fr=28 sc=7 tasks=0 clauses=0 files=13
```

Files: `test-evidence/pre-analyze-check-plan.{json,stdout,stderr,exit}`.

Two things about that line need stating rather than inferring:

- **`advisories=20` is expected at plan stage.** Every advisory is the same check (`missing-path`) against a deliverable this plan designs but has not built: the six new contract test files, referenced from `quickstart.md`, `feature-ref.md`, and each contract's `Pinned by` line. They are not waivers and they are not silence: they are the pre-implementation state, and the implementation stage closes them by creating those files. A `--strict` run is meant to be red here.
- **`clauses=0` does not mean "no clauses".** The pre-analyze checker registers clause ids through a two-to-four-letter prefix pattern (`WP-01`, `FN-16`), which the canonical clause form declared by `shared/definitions/contract-clause-definitions.md` § 3 (`**C-N**`, `md-bold-closed`) deliberately does not use. The clause lane for this spec is therefore accounted by `clause_extract.py` / `account-clause-coverage.py`, both of which read the canonical form. The zero is a property of the legacy pattern, not of the contract set.

## 2. Clause extraction — 73 clauses, all canonical, all cited

```text
command-orchestration.md   form=md-bold-closed 16  C-1..C-16    no_citation=[]
code-review-skill.md       form=md-bold-closed 14  C-17..C-30   no_citation=[]
coverage-receipt.md        form=md-bold-closed 14  C-31..C-44   no_citation=[]
status-gate-ownership.md   form=md-bold-closed 10  C-45..C-54   no_citation=[]
feedback-and-boundaries.md form=md-bold-closed 10  C-55..C-64   no_citation=[]
tests-and-docs-sync.md     form=md-bold-closed  9  C-65..C-73   no_citation=[]
total_clauses=73  distinct_FRs_cited=28  missing_FRs=[]
```

Files: `test-evidence/clause-extraction.txt`. Every clause block ends with its citation group, so the FR lane has no orphan clause and no clause cites nothing.

## 3. Clause / FR coverage accounting — FR lane green, clause lane red by design at plan stage

```text
FR universe: 28   FR claimed: 28   FR uncovered: 0
[clause-uncovered] fail (568) — 568 uncovered, 73 beyond the frozen baseline
[coverage-baseline-delta] fail (73) — baseline holds 495 names
status: uncovered   exit=1
```

Files: `test-evidence/clause-coverage.txt`.

The clause lane's *claimed* set is the `[green: <contract>#<clause>]` declarations on `tasks.md` rows — a tasks-stage artifact that does not exist yet, so all 73 new clauses read as unclaimed and the `comm -13` delta against the frozen baseline is exactly those 73. This is the engine telling the truth about the stage, not a defect in the contract set: the tasks stage creates the claiming rows and the same command then has a chance to go green.

The frozen baseline used for this measurement was written to `tmp/sdd-loop-071/coverage-baseline-071.txt` (the sanctioned scratch root) rather than committed, because a baseline frozen before the claiming rows exist would be regenerated anyway. The tasks stage owns that decision.

## 4. Regression and mirror baselines — measured before any edit

```text
test_expression_gates_doc.py                                   18 passed
expression_compatibility + run_skills_wiring + migration_distribution
  + flat_internal_skill_migration + review_p1_review_loop      60 passed (5 files)
sync-mirrors --only templates      ok (22 files)
sync-mirrors --only skills/internal ok (136 files)
sync-mirrors --only shared         ok (55 files)
regen-command-copies --check       OK: all per-tool command copies match
```

Files: `test-evidence/regression-baseline.txt`. The criterion for the implementation stage is **no NEW failure and no NEW drift** against these numbers, not a green run: a bare "all green" criterion is unpassable the moment unrelated drift predates the change.

## 5. Checks deliberately not run

- `account-clause-coverage.py` without the temp baseline: it exits `2` with `baseline-missing`, which would say nothing about the contract set. The measurement above uses a frozen baseline so the FR lane is real rather than absent.
- `probe-utils.py --action compile-embeds`: the probe registry is not edited by this feature (the `/speckit.review` and `skill:code-review` closing faces are already registered), so there is nothing to recompile and a run would prove nothing about this design.
- Any full test suite: this stage changes specification documents only; running a suite here would be a cost with no matching claim (the closure slot belongs to a later stage).
