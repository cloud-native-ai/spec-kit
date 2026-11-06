# Checkpoint 09 — implement wave 2 (A2+A3+B2)

## 1. Artifact verification

- **A2** `01cc8da8` — 3 files: audit parser (`VALUE_FLAGS` + attached forms), mirror, unit test. 32 unit passed; 52 targeted integration/contract passed; mutation legs M-8/M-9 red; no full suite.
- **A3** `58d30bde` (rebased) — 3 files: `pyproject.toml` dev extra (`pytest` + `pytest-xdist; python_version >= '3.9'`) + `serial` marker; `docs/contribute/dev-setup.md`; `CONTRIBUTING.md`. Runtime dependencies and `[tool.hatch.build]` unchanged; 346 targeted passed.
- **B2** `dfe27809` (rebased) — 8 files: template `### XIX.` / live `### XX.`, version 1.17.0 + Sync Impact Report, manage-constitution 12th entry, instructions `## Test Execution Efficiency`, mirrors + generator. Counts 19/20/12, watchlist 7, sections 33/34; live instructions 34,685 B < 34,816; gate-scan 27/0 violations.
- **Integration**: A2 ff; A3 rebase+ff; B2 rebase+ff; worktree clean; **actual concurrency 3**.
- **Anomalies carried**: A3 reports T017/T046 both name the two docs; WP-A3 owns them per the plan, so T046's share is already met — WP-C2 must not re-edit them. B2 leaves the six stale count pins (`test_constitution_double_landing` c1/c5/c11; `test_fast_fail_discipline` a7/x5/x13) to B3 by design. A2 notes `--dist=loadfile` under M-8 stays green because the pre-change parser already drops unknown `-x=value`; the separated forms and M-9 are red.

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| Full-suite parallel wall-clock ≤ 40% of the 1031.48 s serial baseline. | not_evaluated | T050 687.41s; parallel pending |
| Final parallel run has zero new failure names vs the serial baseline, serial exceptions declared. | not_evaluated | T050 19 names; T047 closure pending |
| Principle ships in constitution template/live, instructions template/live, one owner guideline. | 80% | B1 + B2 integrated; B3 count pins pending |
| 085 temporary Goal/Team, concurrency, worktree/integration queue and checkpoints are used and green. | 50% | temporary Goal/Team; checkpoints 01–09; 2-way + 3-way waves; 085 tests pending |
| Feature reaches Ready for Review with zero blocking review findings. | not_evaluated | review pending |

## 3. Team configuration review

- evidence: A2/A3/B2 child lines, worktrees, integration; the 3-way wave
- symptom: none
- proposal: no configuration change; keep the plan's dependency waves
- ratification: n/a
- applied: no
- observations: 085 line-registry worktree path must be outside repo_root (C-008 `.specify/.tmp` rejected); the stale 081 line (feature Completed) was released with `--evidence-ref features/081.md` before A2 could register.

## 4. Next wave concurrency / roster

- stage: implement (wave 3)
- requested: 24; effective: **3** (2 executors A4+B3 + 1 verifier reserve); team cap 18 not binding
- stage max_parallel: 18; verifier reserve: 1; executor slots: 2
- roster: `sdd-implement-coordinator` + `sdd-implement-executor` (host-native carriers) + `sdd-stage-verifier`
- wave 3: A4 (append the runner tests to the A1 file; after A2/A3) + B3 (count pins/principle tests; after B2) in parallel
- after: C1 (after A1+A4+B2) → C2 (registry/docs/closure)
