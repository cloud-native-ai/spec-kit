# Verification Log — 101-anchor-goal-realignment

<!--
  Schema owner: shared/workflow/acceptance-hardening.md — § Verification Vocabulary and
  § Closure Verdict. The key=value block below is the record; the tables are a human view
  rendered FROM it. The closure judgement (scripts/python/closure-acceptance-check.py)
  parses `SC-NNN_status=` lines and nothing else. Written by the WP-06 package
  (T078–T081), 2026-11-12.

  This file records readings. It does not flip the feature status: the closure and
  acceptance judgement belong to the review stage, and `Planned → Implemented`
  condition ① (zero open task rows) is closed by the stage integrator's task-sigil
  sweep, outside this package's write territory.
-->

# -- Baseline (recorded once, before implement work changed the tree) --

baseline_commit=ce4fa84ab
baseline_date=2026-11-12
baseline_branch=master
baseline_failed_ids=192
baseline_passed=8900
baseline_skipped=3
baseline_runner=parallel passes=2 tier=full (rc=1, 82s)
baseline_failed_ids_source=.specify/specs/101-anchor-goal-realignment/test-evidence/suite-baseline-entry.txt

# -- /speckit.implement results --

implementation_date=2026-11-12
post_change_commit=85dfebc7f (stage base at WP-06 entry; the WP-06 commit carries this record)

# -- Smoke test record (exactly one per feature) --

smoke_command=bash scripts/bash/run-tests.sh tests/contract/test_anchor_command_surface.py tests/contract/test_goal_command_surface.py tests/contract/test_scope_resolution.py tests/contract/test_cleanup_idempotency.py tests/integration/test_101_convergence.py tests/integration/test_101_protected_paths.py tests/contract/test_live_semantic_residue.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/101-anchor-goal-realignment/test-evidence/final-smoke-2026-11-12.txt

# -- Success Criteria evaluation --
# status ∈ pass | fail | partial | blocked | deferred | unknown

SC-001_status=pass
SC-001_value=C1=0 C2=0 C3=0 C4=0 C5=0 C6=0 C7=0; guard module 7 passed (injection cases red as designed)
SC-001_note=Post-registry scan re-run after the T079 write: `.specify/features.md` is class C7 and stays 0. Evidence `test-evidence/final-residue-scan-2026-11-12.txt`; guard `test-evidence/final-smoke-2026-11-12.txt`.

SC-002_status=pass
SC-002_value=Anchor seven modes / Goal four modes; four Anchor-only modes rejected by `command-mode --command goal` with exit 2 `anchor-only-mode` naming `/speckit.anchor`; zero writes
SC-002_note=Canonical templates + generated copies asserted by `test_anchor_command_surface.py` and `test_goal_command_surface.py`, zero failures in the final suite.

SC-003_status=pass
SC-003_value=14 entries = 9 anchor / 3 action-goal / 2 obsolete; `.specify/anchoring/` action-goal count 0; 3 definitions under `.specify/goals/`; 2 obsolete under `.specify/archive/anchoring/`
SC-003_note=`cleanup --check` verdict `ok`, 4 self-checks — `test-evidence/cleanup-check-wp05-2026-11-12.json`; per-entry classification `test-evidence/classification-2026-11-12.md`.

SC-004_status=pass
SC-004_value=receipt per moved/archived entry; digest before == after; deletes 0; second apply 185 files hash-identical, 0 non-no-op decisions
SC-004_note=`test-evidence/t060-idempotency-wp04b-2026-11-12.json`; protected-path equality asserted by `tests/integration/test_101_protected_paths.py` (green in the smoke).

SC-005_status=pass
SC-005_value=teams 20 = 10 with anchor_slug / 10 without; legacy `goal_slug` 0; dangling anchor_slug 0; dispositions 7 (6×R3 + 1×R2)
SC-005_note=Current tree scan `test-evidence/final-sc005-2026-11-12.txt`; engine reading `test-evidence/run-checks-wp04-2026-11-12.txt` — 6 `ok/false/0`, 4 `goal-terminal/true/5` (087-arch-diagram-docs, draw-two-layer-structure, session-driven-self-improvement, skill-layer-install-separation), 10 `no-goal-definition/false/0`.

SC-006_status=pass
SC-006_value=one definition writer per layer (`goal-utils.py`); two-writer fixture lands distinct paths; injected external definition write turns the audit red
SC-006_note=`test_goal_store_write_boundary.py`, `test_goal_writeset.py`, `tests/integration/test_101_convergence.py` — zero failures in the final suite.

SC-007_status=pass
SC-007_value=second apply 0 non-no-op / 185 hashes identical; digest mismatch → exit 4 `conflict` without rewrite; interruption resume I1–I5 (I5 exit 4 `half-state`)
SC-007_note=`test_evidence/t060-idempotency-wp04b-2026-11-12.json`; `test_cleanup_idempotency.py` + `test_cleanup_resume.py` green in the smoke.

SC-008_status=partial
SC-008_value=3 of 4 limbs pass: both reference pages exist (anchor.md new, goal.md rewritten); flow-class ledger carries both command rows; probe compile 85 units zero drift. Build limb `not-evaluated`.
SC-008_note=Build limb reads Hugo v0.141.0 exit 1 on the pre-existing `.Site.Language.Locale` defect (EP-006), never recorded as a pass; other limbs are not downgraded with it.
SC-008_blocked_at=EP-006 (pre-existing docs-build failure, Hugo v0.141.0 `.Site.Language.Locale` exit 1)
SC-008_reduced_measurement=site build attempted and its failure signature recorded (`test-evidence/docs-build-2026-11-12.txt`); the other three limbs measured live (`test-evidence/final-sc008-2026-11-12.txt`)
SC-008_reduced_measurement_run=yes
SC-008_why_reduced_insufficient=a recorded build failure does not show the delivery pages render in the site; only the file/ledger/probe limbs are proven
SC-008_unblock=repair the Hugo locale configuration in a later feature, then re-run the site build; the supporting path makes this non-blocking today

SC-009_status=pass
SC-009_value=protected roots per-file `git hash-object` equal to `d7c9da7a3`; new `.specify/archive/anchoring/**` and this spec's new evidence listed separately
SC-009_note=`test-evidence/protected-paths-entry.txt` (entry reading) + `tests/integration/test_101_protected_paths.py` green in the smoke; no protected path was touched by WP-06.

SC-010_status=pass
SC-010_value=independent reader restates all four terms (Anchor, anchoring archive, Re-Anchoring, action-level Goal) with object + directory correctly
SC-010_note=`test-evidence/reader-restatement-2026-11-12.md` — all four verdicts `agrees`.

# -- Runtime-stack joint-acceptance rows (RS-003 / RS-004 are Form: in-scope) --

RS-003_joint_acceptance=pass — `goal-utils.py --help`/`--version` still satisfy Constitution XXI; new actions' exit codes and the two-writer audit are pinned by contract tests with zero failures in the final suite; the engine remains the single definition writer.
RS-004_joint_acceptance=pass — `sync-mirrors.py --check` ok (114 files byte-identical); `regen-command-copies.py --check` ok; `flow-class-check.py` resolves both command rows (ledger carries `/speckit.anchor` and `/speckit.goal`).

# -- Final suite gate (T080, single run) --

final_suite_command=bash scripts/bash/run-tests.sh --full --names-out .specify/specs/101-anchor-goal-realignment/test-evidence/final-suite-2026-11-12.txt
final_suite_exit_code=1
final_suite_result=228 failed / 8936 passed / 3 skipped (9167 collected, passes=2 tier=full, 81s)
final_suite_baseline_result=192 failed / 8900 passed / 3 skipped (9095 collected)
final_suite_new_failure_ids=37
final_suite_fixed_ids=1
final_suite_new_failure_ids_source=.specify/specs/101-anchor-goal-realignment/test-evidence/final-suite-2026-11-12.txt
final_suite_full_output=.specify/specs/101-anchor-goal-realignment/test-evidence/final-suite-2026-11-12.output.txt
gate1_verdict=FAIL

# -- Guard and delivery readings (T080, re-run after the registry write) --

mirror_check=ok (shared/ == .specify/shared/, 114 files byte-identical)
mirror_check_evidence=.specify/specs/101-anchor-goal-realignment/test-evidence/final-mirror-check-2026-11-12.txt
copy_check=ok (all per-tool command copies match the source templates)
copy_check_evidence=.specify/specs/101-anchor-goal-realignment/test-evidence/final-copy-check-2026-11-12.txt
residue_after_registry=C1=0 C2=0 C3=0 C4=0 C5=0 C6=0 C7=0
residue_after_registry_evidence=.specify/specs/101-anchor-goal-realignment/test-evidence/final-residue-scan-2026-11-12.txt

# -- Closure judgement (read, not authored) --

closure_check_verdict=accept
closure_check_claimed_status=Planned
closure_check_final_path=pass=6 blocked=0 deferred=0 partial=0 fail=0 unknown=0 total=6
closure_check_command=python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/101-anchor-goal-realignment

# -- Wrap-up engines (unit_id skill:implement-feature, run_id r20261112T064607Z-b101) --

wrapup_determine=.specify/specs/101-anchor-goal-realignment/test-evidence/final-wrapup-determine-2026-11-12.json (duplicate: true)
wrapup_execquant=.specify/specs/101-anchor-goal-realignment/test-evidence/final-wrapup-execquant-2026-11-12.txt (duplicate record; no second row)
wrapup_feedback=.specify/specs/101-anchor-goal-realignment/test-evidence/final-wrapup-feedback-2026-11-12.json (duplicate: true)

## Human view (rendered from the block above)

| SC | Path | Status | Reading |
|----|------|--------|---------|
| SC-001 | final | pass | residue C1–C7 = 0 after the registry write; guard 7/7 |
| SC-002 | final | pass | 7/4 modes; 4 Anchor-only modes named-rejected |
| SC-003 | final | pass | 14 = 9/3/2; goals 3; archive 2 |
| SC-004 | final | pass | receipts + digest equality; 185 files identical; 0 deletes |
| SC-005 | final | pass | 10 bound / 10 unbound / 0 legacy / 0 dangling |
| SC-006 | final | pass | single definition writer; two-writer fixture |
| SC-007 | supporting | pass | idempotent re-apply; conflict exit 4; resume I1–I5 |
| SC-008 | supporting | partial | 3 limbs pass; build limb not-evaluated (EP-006) |
| SC-009 | supporting | pass | protected hashes equal `d7c9da7a3` |
| SC-010 | supporting | pass | reader restates all four terms |

## GATE-1 — final suite vs E2 baseline by failure id: FAIL

Compared by **failure-id names** (not counts, not parallel-mode readings): `comm -13`
gives 37 ids that are red in the final run and absent from the E2 baseline; `comm -23`
gives 1 id that was red at baseline and is green now.

The 37 ids group into three causes (evidence: the per-test tracebacks in
`final-suite-2026-11-12.output.txt`):

1. **Stale-surface test alignment (29 ids)** — pre-existing tests that still assert the
   retired surface; the product change is the intended one, the tests were not re-pointed
   by the package that moved the surface:
   - `tests/contract/test_criterion_subject.py` (11) — the owner fixture still reads
     `shared/definitions/goal-definitions.md`; the `## 判据主体指代形 (Criterion Subject Reference)`
     section now lives in `shared/definitions/anchor-definitions.md`.
   - `tests/contract/test_temp_goal_contract.py` (6), `tests/integration/test_archive_migration_real_data.py` (1) —
     expect `.specify/anchoring/<slug>/goal.md`; the definition file is `anchor.md`.
   - `tests/contract/test_parallel_lines.py` (3) + `tests/integration/test_parallel_lines.py` (1),
     `tests/contract/test_temp_team_schema.py` (2), `tests/contract/test_resident_backfill.py` (2) —
     expect the retired `goal_slug` key; the engine and definitions now emit `anchor_slug`.
   - `tests/contract/test_migrate_distribution_assembly.py` (1) — `COMMAND_BASELINE` is pinned
     at 31 commands; the `anchor` command makes it 32.
   - `tests/contract/test_stage_class_wiring.py` (2: `clarify`, `tasks`) — the compiled Wrap-up
     fingerprint legitimately moved, but the pinned stripped-bytes SHA was not re-pinned.
2. **Live-surface gaps (6 ids)** — product-side omissions this package may not edit:
   - `tests/contract/test_git_workflow_observe.py::test_registry_validation_and_wrap_up_face_stay_green` —
     `probe-utils.py probes --validate` reports `embed without probe object: skill:manage-anchor`.
   - `tests/contract/test_docs_step_injection.py` (2) — `anchor.md`'s compiled Wrap-up carries the
     Docs Sync Eval line, but `COMPLEX_COMMANDS` / `DOCS_STEP_EXCLUDED` were not moved with it.
   - `tests/contract/test_binding_model.py::test_the_three_management_skills_cite_owners_and_restate_no_arguments` —
     the rewritten `manage-goal` SKILL.md no longer states the `.specify/teams/<slug>` landing point.
   - `tests/contract/test_summary_trigger.py` (2) — `run-team` SKILL.md no longer states
     `.specify/anchoring/<goal-slug>/summary/`.
3. **Workspace-residue artifacts (2 ids)** — filesystem state, not product regressions:
   - `tests/contract/test_decision_tension_contract.py::TestScenarioAOwnerAndTemplateAnchor::test_template_is_pointer_not_copy_and_path_resolves` —
     the untracked `.specify/.specify/` directory (dated 2026-11-09, off-limits per this
     dispatch) makes `pointer_base` stop at `.specify` and resolve the repo-root pointer under
     `.specify/.specify/`.
   - `tests/contract/test_isomorphism_map.py::test_no_second_map_or_boundary_table_exists` —
     the scan walks `.specify/.tmp/` and read a parallel worker's `s094` sandbox mid-run.

None of the 37 lies in WP-06's write territory, and none was edited. WP-06 stops here and
reports the set rather than touching tests or sources (fast-fail: this is a decision about
which package owns the repair, not a local correction).

## Named residuals (disclosed, not smoothed over)

- **Feature status held at `Planned`.** `tasks.md` still carries 81 open rows — condition ① of
  `Planned → Implemented` is closed by the stage integrator's task-sigil sweep, outside this
  package's territory. Closure/acceptance judgement belongs to the review stage.
- **GATE-1 fails** with the 37-id set above; the repair split (test re-pointing vs live-surface
  fixes) is a driver decision.
- **T004 never froze `coverage-baseline.txt`** (`account-clause-coverage.py --freeze` was not run at
  SETUP). The FR-071 "no clause-coverage regression" comparison is therefore `not-evaluated`;
  only a same-instant coverage reading exists. The missing baseline is not reconstructed after
  the fact.
- **SC-008 build limb** remains `not-evaluated` (EP-006, pre-existing Hugo failure).
- **12 live `team.md` `forbidden_paths`** still list `.specify/goal/**` — classified as stale
  address in a prohibition field and deliberately not edited.
- `smoke-081.txt` is modified in the working tree (N-8 pre-existing); this package neither
  commits nor reverts it.
