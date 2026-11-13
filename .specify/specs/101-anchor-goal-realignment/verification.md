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

# -- Final suite gate (T080 WP-06 reading; closure-repair rerun recorded by WP-06b) --

final_suite_command=bash scripts/bash/run-tests.sh --full --names-out .specify/specs/101-anchor-goal-realignment/test-evidence/final-suite-2026-11-12.txt
final_suite_exit_code=1
final_suite_result=193 failed / 8972 passed / 3 skipped (9168 collected + 1 serial, passes=2 tier=full, 56.23s)
final_suite_baseline_result=192 failed / 8900 passed / 3 skipped (9095 collected)
final_suite_new_failure_ids=3
final_suite_fixed_ids=2
final_suite_new_failure_ids_source=.specify/specs/101-anchor-goal-realignment/test-evidence/final-suite-2026-11-12.txt
final_suite_full_output=.specify/specs/101-anchor-goal-realignment/test-evidence/final-suite-2026-11-12.log
final_suite_new_ids_disposition=2 blocked on scripts/python/goal-utils.py:_resident_definitions (anchor.md never enumerated; out of this package's write territory); 1 self-inflicted census mismatch (test_inprocess_conversion_contract.py::test_c001) repaired in tests/** after the run and re-verified by a targeted module pair (16 passed / 1 pre-existing baseline red)
gate1_verdict=FAIL (residual new set: the 2 test_resident_backfill ids)

# -- WP-06b closure repair (2026-11-12) --

closure_repair_closed_ids=35 of 37
closure_repair_blocked_ids=2 (test_resident_backfill.py::test_every_archive_resident_carries_a_binding_after_backfill, ::test_a_second_backfill_writes_nothing_and_refuses_an_incomplete_binding)
closure_repair_blocked_at=scripts/python/goal-utils.py:2528 _resident_definitions globs only */goal.md while every reader resolves anchor.md (sibling _anchor_layer_contains:186 already allows both); live symptom .specify/anchoring/visualization-skill-selection/anchor.md has no binding and backfill-bindings --dry-run plans zero goal rows
closure_repair_evidence=.specify/specs/101-anchor-goal-realignment/test-evidence/implement-wp06b.md

# -- Guard and delivery readings (WP-06 T080; re-read by WP-06b after the repair) --

mirror_check=ok (shared/ == .specify/shared/, 114 files byte-identical)
mirror_check_evidence=.specify/specs/101-anchor-goal-realignment/test-evidence/final-mirror-check-2026-11-12.txt
copy_check=ok (all per-tool command copies match the source templates)
copy_check_evidence=.specify/specs/101-anchor-goal-realignment/test-evidence/final-copy-check-2026-11-12.txt
residue_after_registry=C1=0 C2=0 C3=0 C4=0 C5=0 C6=0 C7=0
residue_after_registry_evidence=.specify/specs/101-anchor-goal-realignment/test-evidence/final-residue-scan-2026-11-12.txt
wp06b_mirror_check=ok (rc 0, shared/ 114 files byte-identical, five projections ok)
wp06b_copy_check=ok (rc 0)
wp06b_residue=C1=0 C2=0 C3=0 C4=0 C5=0 C6=0 C7=0
wp06b_smoke_exit_code=0 (43 passed in 12.85s)
wp06b_smoke_evidence=.specify/specs/101-anchor-goal-realignment/test-evidence/final-smoke-wp06b-2026-11-12.txt
wp06b_targeted_result=11 failed / 274 passed — every red is a baseline id except the 2 blocked resident ids
wp06b_targeted_evidence=.specify/specs/101-anchor-goal-realignment/test-evidence/implement-wp06b-targeted-tests.txt

# -- Coverage baseline (T004, frozen by WP-06b) --

coverage_baseline_command=python scripts/python/account-clause-coverage.py --freeze --spec-dir .specify/specs/101-anchor-goal-realignment --corpus-root .specify/specs
coverage_baseline_file=.specify/specs/101-anchor-goal-realignment/coverage-baseline.txt (673 frozen names, base-sha b9f6a0edb)
coverage_live_reading=722 uncovered clause names: 673 baseline-internal + 49 beyond baseline, all 49 being this feature's own contracts/*.md#C-1…C-49 with no [green:] claim surface; 48 uncovered FRs; no other spec gained an uncovered clause
coverage_live_command=python scripts/python/account-clause-coverage.py --spec-dir .specify/specs/101-anchor-goal-realignment --corpus-root .specify/specs (rc 1, status uncovered)

# -- Closure judgement (read, not authored) --

closure_check_verdict=accept
closure_check_claimed_status=Planned
closure_check_final_path=pass=6 blocked=0 deferred=0 partial=0 fail=0 unknown=0 total=6
closure_check_command=python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/101-anchor-goal-realignment

# -- Wrap-up engines (unit_id skill:implement-feature, run_id r20261112T064607Z-b101) --

wrapup_determine=.specify/specs/101-anchor-goal-realignment/test-evidence/final-wrapup-determine-2026-11-12.json (duplicate: true)
wrapup_execquant=.specify/specs/101-anchor-goal-realignment/test-evidence/final-wrapup-execquant-2026-11-12.txt (duplicate record; no second row)
wrapup_feedback=.specify/specs/101-anchor-goal-realignment/test-evidence/final-wrapup-feedback-2026-11-12.json (duplicate: true)
wp06b_wrapup_determine=.specify/specs/101-anchor-goal-realignment/test-evidence/wrap-up-determine-wp06b-2026-11-12.json (rc 0, duplicate: true)
wp06b_wrapup_execquant=.specify/specs/101-anchor-goal-realignment/test-evidence/wrap-up-execquant-wp06b-2026-11-12.json (rc 0, duplicate record; no second row)
wp06b_wrapup_feedback=.specify/specs/101-anchor-goal-realignment/test-evidence/wrap-up-feedback-wp06b-2026-11-12.json (rc 0, duplicate: true, count_since_submission 485, should_prompt true)

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

## GATE-1 — final suite vs E2 baseline by failure id: FAIL (2 residual ids)

Compared by **failure-id names** (not counts, not parallel-mode readings).

**WP-06 entry reading** (`final-suite-2026-11-12.output.txt`, the pre-repair run): `comm -13`
gave 37 ids red in the final run and absent from the E2 baseline; `comm -23` gave 1 fixed id.

**WP-06b closure-repair reading** (the single rerun; full account in
`test-evidence/implement-wp06b.md`): 193 failed / 8972 passed / 3 skipped; `comm -13`
gives **3** ids, `comm -23` gives 2 fixed ids.

1. **35 of the 37 closed in-territory** by moving live tests / live owners to the new
   Anchor–Goal model, never by weakening an assertion: `test_criterion_subject` (11),
   `test_temp_goal_contract` (6), `test_parallel_lines` (3 contract + 1 integration),
   `test_temp_team_schema` (2), `test_stage_class_wiring` (2 — re-pinned after proving the
   only delta is the machine-owned banner fingerprint), `test_archive_migration_real_data`
   (1), `test_migrate_distribution_assembly` (1 — 31 → 32 with a dated rationale), the
   probe-registry object for `skill:manage-anchor` (1), `test_docs_step_injection` (2),
   `test_binding_model` (1), `test_summary_trigger` (2), and the two workspace-residue
   artifacts: `.specify/.specify/` excluded by skipping `.specify` ancestors (artifact
   never deleted) and `.specify/.tmp` added to the sanctioned skip set.
2. **1 suite-time id was self-inflicted and repaired after the run**: the rewritten
   `test_temp_goal_contract.py` collapsed four classified subprocess sites into a `_run`
   helper, tripping the 098 in-process census (`test_inprocess_conversion_contract.py::test_c001`).
   Calls were inlined into their owning tests and the census-named test restored; verified
   green by a targeted module pair (no second full suite — the closure-repair rerun was
   already spent).
3. **2 ids remain blocked** — `test_resident_backfill.py::test_every_archive_resident_carries_a_binding_after_backfill`
   and `::test_a_second_backfill_writes_nothing_and_refuses_an_incomplete_binding`.
   The aligned subject exposes a real engine gap, not a test defect:
   `scripts/python/goal-utils.py:2528 _resident_definitions` enumerates archive residents
   with `glob("*/goal.md")` (the retired filename) while every reader resolves `anchor.md`
   via `definition_filename("anchor")` (sibling `_anchor_layer_contains:186` already allows
   both names). Live symptom: `.specify/anchoring/visualization-skill-selection/anchor.md`
   carries no `binding:` block and `backfill-bindings --dry-run` plans **zero** goal rows,
   so C-112's exhaustiveness claim is silently violated. The fix is two lines in that
   engine, outside this package's write territory; the run reports the path and evidence
   (`test-evidence/anomaly-resident-backfill-wp06b-2026-11-12.txt`) instead of editing it
   or weakening the guard.

## Named residuals (disclosed, not smoothed over)

- **Feature status held at `Planned`.** `tasks.md` still carries open rows — condition ① of
  `Planned → Implemented` is closed by the stage integrator's task-sigil sweep, outside this
  package's territory. Closure/acceptance judgement belongs to the review stage.
- **GATE-1 fails on exactly the 2 resident ids above**; the engine fix (`_resident_definitions`
  must enumerate `anchor.md` alongside legacy `goal.md`) is a driver decision and is the only
  remaining blocker to a zero-new-id reading.
- **T004 is closed** — `coverage-baseline.txt` was frozen by WP-06b (673 names, base-sha
  `b9f6a0edb`); the live accounting shows 673 baseline-internal uncovered names and 49 beyond
  baseline, all 49 this feature's own unclaimed `contracts/*.md#C-1…C-49`; no other spec
  gained an uncovered clause. FR-071 is now measurable; the 49 are a claim-surface gap in
  `tasks.md` (`[green:]` declarations), not a coverage regression.
- **SC-008 build limb** remains `not-evaluated` (EP-006, pre-existing Hugo failure).
- **12 live `team.md` `forbidden_paths`** still list `.specify/goal/**` — classified as stale
  address in a prohibition field and deliberately not edited.
- `smoke-081.txt` is modified in the working tree (N-8 pre-existing); this package neither
  commits nor reverts it.
