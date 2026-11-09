# Closure readings — 094-goal-team-parallel (wp07, T079–T080)

**Package**: `wp07-closure` (read-only + evidence) · **Rows**: T079–T080 ·
**Branch**: `094-wp07` (base `03efbb1f6`, master @ wp01–wp06 + wp04b) · **Date**: 2026-11-09 ·
**Tree**: this worktree, `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/094-wp07`
(henceforth "the worktree").

Raw outputs live one file per reading under
`.specify/specs/094-goal-team-parallel/test-evidence/` (`wp07-*`, `closure-failed.txt`,
`migration-dryrun.json`, `wp07-closure-acceptance.*`). This note is the digest; it never
replaces the raw records.

## 1. T079 — real-data sequence

| Step | Reading | Evidence |
|------|---------|----------|
| `probe-residual` before | **goal 8 / teams 8** (085–091, 089/088 slugs renamed post-baseline, plus 094's own pair) | `wp07-T079-probe-before.txt` |
| Baseline comparison | programmatic diff against `requirements-baseline-probe.txt` (goal 7 / team 7): goal +094; team +088 (rename), +089 (rename), +094. Two renames are commit `76b4ec60e` (092 repair wave); 094's pair is the run's own subject (tasks.md N-4 / A8) | `wp07-T079-baseline-comparison.txt` |
| `migrate-archive --dry-run` | **16 decisions** = 8 goal + 8 team, **0 conflict, 0 interrupted**, each `action: migrate` with a receipt body (`delete_policy: archive-not-delete`) | `migration-dryrun.json`, `wp07-T079-dryrun.txt` |
| `migrate-archive --apply` | **REFUSED before execution** by the host action classifier: the dispatch declares wp07 "read-only + evidence" and the apply permanently relocates pre-existing spec trees; it clears only on explicit user authorization naming the action | `wp07-T079-apply-blocked.txt` |
| `probe-residual` after / existence assertions | **not run** — nothing was applied, so no after-reading exists | — |

Adjudication: the dry-run plan is complete and conflict-free; the applied reading the
criterion needs (residual zero, every source tree readable under
`.specify/archive/goal-team/trees/`, per-definition existence assertions) is outstanding
and is recorded as SC-003 `blocked` in `verification.md`, never as a pass.

Also measured while censusing the subject: the probe form sees 8 goal / 8 team, the full
census sees 8 goal / 9 team — the ninth is the one-level non-conforming
`.specify/specs/088-speckit-visualization/team/team.md`, which neither the probe glob nor
the migration addresses. Plan EP-002's round-4 census (9 goal / 10 team = 19) predates the
consolidation archive of the 092 tree; the premise itself is written as "the probe's
reading, not a frozen constant", so it stays verified, but the drift is recorded here.

## 2. T080 — closure sequence

### 2.1 Teardown precondition

No fixture or worktree exists **inside the worktree** (`.specify/.tmp` absent at entry;
the command/exit metadata of the suite run is `wp07-closure-suite-meta.txt`). The wp07 worker itself is a worktree of the
main repo's `.specify/.tmp/sdd-loop/`, which is the contamination source named in § 2.4
and ANOMALY 1.

### 2.2 Projection verdicts (GATE-2)

- `python3 scripts/python/sync-mirrors.py --check` → **OK**, exit 0: templates 22,
  skills/external 419, skills/internal 141, agents 17, scripts 123, shared 102 — all
  byte-identical; every projected pair listed ok. **The wp06 mirror anomaly is closed**
  (wp04b's two files are projected at HEAD). Reading: `wp07-mirror-check.txt`.
- `python3 scripts/python/regen-command-copies.py --check` → **OK**, exit 0. Reading:
  `wp07-copy-check.txt`.

### 2.3 Stage gates

| Gate | Reading | Evidence |
|------|---------|----------|
| validate-requirements | 0 errors / 0 warnings, exit 0 (326 lines, 55 definition rows, 6 shared strings) | `wp07-validate-requirements.txt` |
| validate-tasks | 0 errors, **1 warning** — the disclosed forward edge `T043 → T054` (line 240); exit 0 | `wp07-validate-tasks.txt` |
| validate-decision-tensions | 7 records, 0 findings, exit 0 | `wp07-validate-decision-tensions.txt` |
| pre-analyze ×3 (requirements / plan / tasks) | `decision: pass`, **errors 0**, fr 43 / sc 12 / tasks 85, 40 advisories each (all `missing-path` on intentionally absent or retired paths), exit 0 | `wp07-pre-analyze-*.txt` / `.json` |
| decomposition | plan **proceed** (fr 43); tasks **proceed** (fr 43 / tasks 85), exit 0 | `wp07-decomposition-*.txt` / `.json` |
| GATE-7 script interface | `--help` 0, `--version` 0 (`goal-utils.py 0.0.22`), `migrate-archive --bogus-option` rejected with exit 2 | `wp07-script-interface.txt` |
| GATE-3 residual probe | ran (8 goal / 8 team) — but see T079: the residual surface cannot be emptied while the apply is unauthorized | `wp07-T079-probe-before.txt` |

### 2.4 Full-suite reading (GATE-1 input)

Command (canonical runner, xdist defaults):
`bash scripts/bash/run-tests.sh --names-out .specify/specs/094-goal-team-parallel/test-evidence/closure-failed.txt -q`

- **Parallel pass: 205 failed, 8174 passed, 2 skipped, 576 warnings in 42.20 s.**
- Serial pass (1 declared `serial` test): 1 passed, exit contribution 0. Combined exit: **1**.
- Failed-name list: **205 ids** (`closure-failed.txt`), the serial-comparable comparison
  surface (086 runner contract; plan § baseline-stability).

Deltas (name-level, `LC_ALL=C comm`):

- vs **plan baseline** (46 ids): **161 new** — this surface is stale (see ANOMALY 1 and
  T002's implement-entry finding that already measured 113).
- vs **implement-entry baseline** (`implementation-baseline-ids.txt`, 113 ids): **94 new**,
  **2 fixed** (`test_checkpoint_protocol::test_protocol_has_the_four_parts`,
  `test_isomorphism_map::test_no_second_document_claims_map_ownership`).
  113 − 2 + 94 = 205. Files: `wp07-closure-new-vs-implementation.txt`,
  `wp07-closure-fixed-vs-implementation.txt`, `wp07-closure-new-vs-plan.txt`.

Attribution of the 94 new ids (representative causes in `wp07-closure-attribution.txt`,
one line per failing module):

| Group | Ids | Cause |
|-------|-----|-------|
| trigger engine / promotion / tuning / telemetry | 52 | **worktree self-location**: engines resolve the workspace root through the literal `.specify` component in this worktree's absolute path and land on the MAIN repo; the guard `test_ask_record_repeat::test_canonical_engine_does_not_self_resolve_to_the_framework_repo` fails on exactly this. Verified: a fixture `trigger-utils.py --action init` answers `workspaceRoot: /storage/project/cloud-native-ai/spec-kit`. The 63-id serial probe reproduced the parallel ids exactly, so this is not a scheduling artifact |
| measurement_instruments | 9 | `.specify/specs/069b-isomorphism-migration-metrics/` was archived by the 2026-11-09 consolidation; the module pins `notes/expression-baseline.md` under the old live path (post-baseline tree state, not 094) |
| summary_trigger | 2 | `run-team` SKILL.md now names `.specify/anchoring/<goal-slug>/summary/` (T075); the test pins the retired `.specify/goal/<goal-slug>/summary/` path — a test pin the disposal table does not cover |
| 085 disposal family (`test_goal_scope_engine` 8, `test_scope_resolution` 5, `test_temp_goal_contract` 2, `test_temp_team_schema` 2) | 17 | wp01's scope narrowing (T013); all marked `rewrite` in the tasks.md § 085 disposal table and owned by **no package** (wp05 ANOMALY, still open) |
| wp06 guard pins | 4 | `test_no_spec_local_writes` 2 — `EXPECTED_WRITE_ACTIONS` predates wp04b's `handoff-ref`; `test_085_disposal_table` 1 — two wp06-authored modules fall outside `FEATURE_MODULES`; `test_qoder_command_frontmatter` 1 — `goal.md` short-description is 56 chars (limit 50) after wp06's T074 edit |
| singles | 9 | `spec_feature_binding_integrity` 1 (archived 046/092 spec paths), `run_checks` 1 (the known wp01/wp02 roster pin, roster now 19 vs pinned 11), `expression_faces` 2, `nested_run_report` 1, `expression_compatibility` 1 (a `historical` disposal row), `docs_command_template` 1, `coaching_wiring_contract` 1, `clause_coverage` 1, `ask_record_repeat` 1 (self-location, counted here by module but explained above) |

Pre-existing families **unchanged** by this package (present in the implement-entry
baseline, readings only): the goal/summary/target integration suites
(`test_summary_accumulation` 10, `test_summary_legacy_backfill` 10, `test_goal_aggregation`
10, `test_target_fold` 7, `test_goal_reference` 5, `test_goal_concurrent_refresh` 5,
`test_target_milestones` 4, `test_goal_definition_sourcing` 4, `test_goal_roster` 1,
`test_goal_migration_path` 1), the compile/wording-gate family (`test_compile_*` 11,
`test_engine_face_contract` 5), the gate-count family (28 vs 27/23 across
`test_neutrality_budget`, `test_confirmation_gates_sweep`, `test_criterion_subject`,
`test_fast_fail_discipline`, `test_proactive_trigger_section`, `test_sdd_diffusion`,
`test_wrap_up_wording_gate_safe`, `test_user_facing_comprehension_doc`,
`test_clause_coverage` 1), the loop-state/lifecycle family (`test_loop_state_engine` 9,
`test_lifecycle_detach_reattach` 2), the pytest-pin mismatch
(`test_acceptance_premises`: env pytest 8.4.2 vs recorded 9.0.3), and the neutrality /
shared-reference / token-efficiency singles.

**GATE-1 verdict: not achievable from this worktree.** The only valid GATE-1 reading is
the serial failed-id diff run in the MAIN tree after every fixture and worktree under
`.specify/.tmp/` is removed (execution lesson 2) — i.e. after this worker is torn down and
its changes integrated. The worktree reading above is recorded as an environment-degraded
reading with named causes, never as a pass.

### 2.5 Per-criterion status block (mirror of `verification.md`)

`SC-001_status=fail` · `SC-002_status=partial` · `SC-003_status=blocked` ·
`SC-004_status=pass` · `SC-005_status=pass` · `SC-006_status=pass` ·
`SC-007_status=pass` · `SC-008_status=pass` · `SC-009_status=pass` ·
`SC-010_status=fail` · `SC-011_status=pass` · `SC-012_status=pass`

(The record lives in `verification.md`; this line is a view. Final-path: pass 6 /
partial 1 / blocked 1 / fail 1 / total 9.)

### 2.6 Closure verdict (GATE-5 input) — verbatim

```
verdict: block
spec_dir: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/094-wp07/.specify/specs/094-goal-team-parallel
flow_class: execution
claimed_status: Planned
final_path: pass=6 blocked=1 deferred=0 partial=1 fail=1 unknown=0 total=9
reason: final-path-not-pass: SC-001
reason: final-path-not-pass: SC-002
reason: final-path-not-pass: SC-003
```

Command: `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/094-goal-team-parallel --feature-registry .specify/memory/features.md`
(exit 1; JSON payload `wp07-closure-acceptance.json`, human output
`wp07-closure-acceptance.txt`).

## 3. Residual risks — owned by the driver / next stage

1. **T079 apply is unauthorized** — SC-003 `blocked`: run `migrate-archive --apply`, the
   after-probe and the existence assertions with explicit authorization; the dry-run plan
   is ready (`migration-dryrun.json`, 16 decisions / 0 conflicts).
2. **SC-001 has no guard and no implementation** — `tests/contract/test_command_run_goal_team.py`
   is absent and `create_goal` writes no binding block (T016–T019 blocked in wp03, module
   unowned in the § Package Map). Needs an owner or a re-scope ruling.
3. **SC-002 is red on a stale pin** — add `handoff-ref` to `EXPECTED_WRITE_ACTIONS` in
   `tests/contract/test_no_spec_local_writes.py` (wp06's module) and re-run.
4. **SC-010 is red** — the 085 disposal rewrites remain unowned (17 ids), and
   `test_085_disposal_table.py`'s exclusion list must admit wp06's two modules or the
   table must grow a row; the "contract suite all green" limb cannot hold until the
   disposal wave lands.
5. **Feature-introduced reds outside the disposal table** — `test_qoder_command_frontmatter`
   (goal.md description 56 > 50) and `test_summary_trigger` (retired summary path pinned);
   both are one-line repairs in the owning surfaces.
6. **ANOMALY 1 — worktree self-location contamination**: engines self-resolve to the main
   repo from this nested worktree (guard test red by design of the trap). Consequences:
   (a) the trigger family (52 ids) is red for environmental reasons; (b) the runs mutated
   the MAIN repo's live `.specify/memory/trigger/index.json` (measured: `updated`
   12:30:05Z → 13:04:27Z, stats/promotion counters moved; worktree-side files untouched).
   The main repo file was NOT restored by wp07 (a shared working-tree write outside the
   worktree guard); the driver decides — `git checkout -- .specify/memory/trigger/index.json`
   in the main repo if the prior state is wanted.
7. **GATE-1 must be re-read in the main tree** after teardown; the plan baseline (46) is
   stale and the implement-entry baseline (113) is itself worktree-contaminated per T002.
8. **All 85 task sigils are still `- [ ]`** at HEAD; no package updated them and wp07 does
   not batch-close other packages' rows. GATE-4 is therefore red and the row-state sweep
   belongs to the driver's integration close-out.
9. **The one-level `088-speckit-visualization/team/team.md`** is outside the probe glob and
   the migration subject; a future ruling must dispose it explicitly.
10. **Registry row 094 still reads `Planned`**; the claim is correct given the closure
    verdict `block` and is not raised by this note.

## 4. Anomaly summary (for the close-out message)

- ANOMALY 1: worktree self-location — engines resolve the main repo; trigger family (52 ids)
  red; main-repo trigger index mutated; final GATE-1 must run in the main tree after teardown.
- (no second anomaly: every in-passing repair this package made is listed above; the
  probe scratch under `.specify/.tmp/s094-*` and the suite-leaked `.specify/.tmp/s094`
  fixtures were removed in-passing.)
