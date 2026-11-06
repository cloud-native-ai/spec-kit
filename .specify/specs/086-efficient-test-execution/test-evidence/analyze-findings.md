# 086 Analyze Findings — read-only cross-artifact analysis

Captured from the analyze stage (`ANALYZE-DONE`) at 2026-11-06T04:56Z. Full report is in the
analyze-stage session/feedback records; this file is the actionable findings digest.

## Metrics

33 FR / 12 SC / 7 STR; 50 tasks; contract claims 52/52 syntactic; FR→contract citation **0/33**;
task FR coverage 32/33; checklist dispositions 44/44; findings **1 CRITICAL / 5 HIGH / 13 MEDIUM / 5 LOW**.
Feature 086 bound; status Planned; 085 diff empty; 085 SC-010 still `partial`.

## CRITICAL

- **C-01** — Four contracts carry no `(FR-…)` reference group; `account-clause-coverage.py` reports
  `status: uncovered`, 33 errors, `fr-uncovered 0/33`. The `[green:]` task rows claim clause IDs only,
  not FRs. Fix: add the clause→FR reference group required by
  `shared/definitions/contract-clause-definitions.md` §4.2 to the four contract files, covering every
  FR-001…FR-033 at least once; rerun `account-clause-coverage.py` to `status: ok`, `fr-uncovered 0`.

## HIGH

- **H-01** — FR-027 (no 085 path modified) vs FR-030 (085 SC-010 MUST be updated); the carve-out lives
  only in tasks T041, and C-041/GATE-5/M-16/team territory/WP-C2/R-8 forbid it literally. T041 cites a
  nonexistent `CLOSURE.md:272`. Fix: add the narrow FR-027 exception (only the 085
  `verification.md` SC-010 status lines), align C-041/GATE-5/M-16/team/WP-C2/R-8, and correct T041's
  citation to FR-030/A12/A17 + 085 plan.
- **H-02** — inherited `PYTHONPATH` is an unstated premise of every run-derived SC; the host `.venv`
  fails with `platformdirs.pytest_plugin` unless `PYTHONPATH` is cleared. Fix: add
  `env -u PYTHONPATH`/`PYTHONPATH=` to quickstart S-0/S-8 and tasks T014/T016/T044/T047, and record
  the environment assumption (A20 / RS-005 joint acceptance).
- **H-03** — Mutation legs M-8…M-15, M-18, M-19 have no tasks; T042 misassigns M-16/M-17. Fix: rewrite
  T042 and add a leg→task→expected-fail table covering all M-1…M-19.
- **H-04** — The implementation-start baseline is taken at T014, after runner/parser/pyproject edits
  (T007/T008), violating TB-03/A9 and absorbing regressions. Fix: move the serial baseline to T001a
  before any source edit; use it as the GATE-1/DoD-4 baseline referent; T014 becomes the parallel
  measurement.
- **H-05** — The task plan implies ≥9 full-suite runs but the two-slot budget allows 2; no
  `out-of-slot-exception` records; the closure names path is `.specify/.tmp/...` instead of TB-04's
  `<spec>/final-failed.txt`. Fix: reuse the closure run, shrink T016 to representative arms, record every
  out-of-slot full run in the state-spine E2 fence, and use the TB-04 names path.

## MEDIUM

| ID | Location | Issue | Fix |
|---|---|---|---|
| M-01 | requirements FR-011 / plan / contracts / tasks | two-pass execution is only an assumption/contract, not an FR | add a sentence to FR-011 (no new FR) |
| M-02 | requirements FR-001/FR-007 / SC-004 / C-002 | `# test runner: mode=…` disclosure has no FR parent | add a sentence to FR-001/FR-007 |
| M-03 | tasks T036/T037/T039/T040/T041/T042/T043/T047 | `[green:]` clause assignments are semantically misaligned | reassign per the report |
| M-04 | runner contract C-014 / STR-002 / data-model E-3 | failed-name template omits pass count | fix the template/consumer |
| M-05 | tasks T010 | inline Python is polluted with `T045` tokens | restore the original expression |
| M-06 | plan Phase 1 / EP-001/EP-006/EP-008 | counts 8 vs 9 research rows, 7 vs 19 mutation legs; EP-001 path missing; gate-cap wording | correct the references/counts |
| M-07 | requirements FR-017 / tasks | FR-017 has zero task carrier | add a guard task/row |
| M-08 | tasks Phase 7 | US5 phase has no verification row | add the ledger verification row |
| M-09 | features.md / features/086.md | registry stage notes stop at plan | record tasks/checklist (status stays Planned) |
| M-10 | tasks T032 / quickstart S-3 | T032 cites the wrong quickstart scenario; duplicated blockedBy | fix the reference/duplicate |
| M-11 | plan WP-C2 / feature-ref / T040 | "additive dogfood assertion" vs "no edit planned" conflict | choose the re-run-only reading |
| M-12 | requirements SC-001 / goal | SC-001 has no 40% lower bound; goal does | add the 40% measurement to SC-001 |
| M-13 | requirements FR-022 / principle contract C-037/C-038 | gate-scan ceiling and budget-raise rule have no FR parent | add the two sentences to FR-022 |

## LOW

- **L-01** research R-4 mode-line form differs from C-002/E-5/T035.
- **L-02** cross-reference/count drift (E-1/E-6, RS-004, state spine effective 24 vs team 18, T021,
  T049 "eight outputs", T002/T005 `[P]`, T001 temp wording, T038 `<stage-base>`, feature-ref baseline
  path, STR-002 consumers).
- **L-03** CHK025: worker death/partial pass list completeness is unspecified.
- **L-04** CHK037: scaffold `087-` branch observation has no owner/parking location.
- **L-05** per-worker `basetemp`/`PYTEST_XDIST_WORKER` lifecycle re-measure has no task.

## Read-only proof

No requirements/plan/tasks/contracts/source/template/test/085 path was modified by the analyze stage.
Only the analyze Wrap-up records (session / feedback / exec-quant) and
`.specify/.tmp/086/analyze-coverage.json` scratch exist. `git diff` over 085 paths is empty.

## Repair order for the driver

1. C-01 contract FR references (deterministic gate).
2. H-01 085 live-status carve-out across FR-027/C-041/GATE-5/M-16/team/WP-C2/R-8/T041.
3. H-04/H-05 baseline timing + two-slot budget in tasks/plan/state spine.
4. H-02 PYTHONPATH precondition in requirements/quickstart/tasks.
5. H-03 mutation-leg tasks/T042.
6. M-01/M-02/M-03/M-04/M-05/M-06/M-07/M-08/M-09/M-10/M-11/M-12/M-13, then L-01…L-05.
7. Re-run validate-requirements, validate-tasks, account-clause-coverage, pre-analyze
   (requirements/plan/tasks) and the decomposition gates; only then dispatch implement.
