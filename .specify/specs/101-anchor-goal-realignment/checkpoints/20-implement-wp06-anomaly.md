# Checkpoint 20 — implement WP-06 (GATE-1 anomaly and ruling)

## 1. Artifact verification

- sentinel: **none** — WP-06 delivered the registry/detail/verification but ended with `ANOMALY: GATE-1 FAIL — final suite has 37 failure ids absent from the E2 baseline (29 stale-surface assertions, 6 live-surface gaps, 2 workspace-residue artifacts), all outside WP-06's write territory; no test or source edited.`
- delivered: commit `5c89f9ca6` (T078–T081: registry row 101, 101 detail, 041/094 successor notes, `verification.md`, final evidence). The registry status is honestly held at `Planned`; `closure-acceptance-check.py` returns `accept` for the claimed `Planned` (final path 6/6 pass).
- final full suite (T080, one slot): **228 failed / 8936 passed / 3 skipped** (9167) vs E2 `192 / 8900 / 3` (9095); 37 new failure ids by name; 1 fixed. GATE-1 = **FAIL**. `sync-mirrors --check` ok (114 byte-identical); `regen --check` ok; residue after the registry write C1–C7 = 0; residue guard 7/7; feature smoke 43 passed.
- 37 new ids:
  - **29 stale-surface assertions**: `test_criterion_subject` 11, `test_temp_goal_contract` 6, `test_parallel_lines` 4, `test_temp_team_schema` 2, `test_resident_backfill` 2, `test_stage_class_wiring` 2, `test_archive_migration_real_data` 1, `test_migrate_distribution_assembly` 1.
  - **6 live-surface gaps**: `test_git_workflow_observe` (missing probe object `skill:manage-anchor`), `test_docs_step_injection` 2, `test_binding_model` (lost teams landing point), `test_summary_trigger` 2 (lost summary literal).
  - **2 workspace-residue artifacts**: `test_decision_tension_contract` (pre-existing untracked `.specify/.specify/`), `test_isomorphism_map` (mid-run `.specify/.tmp` sandbox).
- SC evidence: SC-005 20 teams 6 ok + 4 goal-terminal + 10 no-goal-definition, legacy `goal_slug` 0, dangling 0; SC-008 reference pages/ledger/probe 85 zero drift, build limb `not-evaluated` (EP-006) → partial; SC-009 protected roots equal `d7c9da7a3`; SC-010 reader restatement agrees.
- residuals: T004 never froze `coverage-baseline.txt` → FR-071 clause coverage `not-evaluated`; 12 `team.md` forbidden paths still name `.specify/goal/**` (classified prohibition-field residual); `smoke-081.txt` left modified/uncommitted.

## 2. Ruling

1. **29 stale-surface assertions** are live tests still asserting the retired Goal model; update their expectations to the new Anchor/Goal model without weakening the subject check (live tests, not dated records).
2. **6 live-surface gaps** are live owners/tests: add the `skill:manage-anchor` probe object and compile (live probe registry); fix the docs-step injection faces, the binding-model teams landing point and the summary-trigger literal in their live owners or tests.
3. **2 workspace-residue tests** must ignore the sanctioned `.specify/.tmp` root and the pre-existing untracked `.specify/.specify/` (record the latter as a known baseline artifact; never delete it).
4. **T004 coverage baseline**: freeze it via the task’s engine now and record the reading; FR-071 clause coverage is then measurable.
5. Re-run the **final full suite** after the fixes (closure-repair rerun, recorded as `in-slot-rerun`); GATE-1 must be zero new vs E2; update `verification.md`, the feature detail/registry honestly; keep the lifecycle status governed by the review stage.

## 3. Next stage concurrency / roster

- requested: 24; effective: 1; effective_reason: `dependency-edge` — WP-06b is the GATE-1 closure repair; verifier reserve: 1.
- next package: **WP-06b** (test/live-surface alignment + coverage baseline + final suite + verification), then the review stage.

## 4. Direction audit

- reload tier: T0 + T1.
- Q1 rules: unattended / no approval request / U4 → next stage / spine written before acting / workspace guard / fast-fail / gate discipline / budget / report discipline — all in force.
- Q2 process: `correction-applied` — WP-06 surfaced the GATE-1 failure instead of weakening the comparison or editing out-of-territory tests/source; the driver ruled the test/live-surface closure.
- Q3 next action: pass — WP-06b closes GATE-1; review follows.
- Q4 spine freshness: pass — spine will record attempt 2 before the repair dispatch.
- Q5 territory/workspace: pass — WP-06 wrote only registry/detail/verification/final evidence; the pre-existing `smoke-081.txt`/`.specify/.specify/` remain untouched.
- verdict: `correction-applied`.
- 5b published-state: `n/a — no history correction`.
