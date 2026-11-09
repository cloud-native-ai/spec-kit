# Repair wave — 094-goal-team-parallel closure block

**Scope**: wp07 residual list (`notes/closure-readings.md` § 3), under two user rulings
R1 / R2 (2026-11-09) · **Branch**: `094-repairwave` (base master `12dc3e36a`) ·
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/094-repairwave` · **Date**: 2026-11-09.

Raw readings live one file per reading under `test-evidence/repairwave-*`; this note is
the digest.

## 0. Closure verdict — verbatim

```
verdict: accept
spec_dir: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/094-repairwave/.specify/specs/094-goal-team-parallel
flow_class: execution
claimed_status: Planned
final_path: pass=8 blocked=0 deferred=0 partial=0 fail=0 unknown=0 total=8
reason: none
```

Command: `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/094-goal-team-parallel --feature-registry .specify/memory/features.md`
(exit 0; reading `test-evidence/repairwave-closure-acceptance.txt`).

The total fell from 9 to 8 because R2 moved SC-001 from the `final` path to `supporting`;
the eight remaining `final`-path criteria all pass. Supporting rows: SC-001 `partial`
(R2), SC-009 / SC-010 / SC-011 `pass`.

## 1. Per-item disposition

| # | Item | Disposition |
|---|------|-------------|
| 1 | **R1** — `migrate-archive --apply` authorized | executed; 16 definitions migrated, receipts + post-state + idempotence recorded (§ 2) |
| 2 | **R2** — SC-001 re-scoped `final` → `supporting` | recorded in `requirements.md` § Clarifications (new dated subsection) + SC-001 `**Path**` marker; `verification.md` SC-001 = `partial` with the five-field measurement ladder (own guard and T019 write absent; acceptance delegates to SC-004/SC-005). No new guard implemented |
| 3 | **SC-002** — stale action-roster pin | `handoff-ref` added to `EXPECTED_WRITE_ACTIONS` in `tests/contract/test_no_spec_local_writes.py`; module 4 passed (parser set = table set = pinned set = 10 actions; both mutation arms red-on-revert) |
| 4 | **SC-003** — applied migration reading | § 3 below; status `pass` |
| 5 | **SC-010** — disposal wave + exclusion-list repair | rows 1/2/3/6/9/11 rewritten to the archive/binding vocabulary: `test_scope_resolution` (9 passed), `test_temp_goal_contract` (8 passed), `test_temp_team_schema` (9 passed), `test_goal_scope_engine` (9 passed), `test_checkpoint_protocol` (6 passed), `test_checkpoint_rollback` (1 passed); `test_085_disposal_table.py` FEATURE_MODULES admits wp06's `test_framework_map_archive_row.py` + `test_goal_command_template.py` (module 2 passed). Assertions keep their intent: the retired `spec`/`global` value members become "refused with invalid choice", the survive-facts move to their archive locations, no assertion was deleted or hollowed |
| 6 | **one-line repair** — `qoder_command_frontmatter` | `templates/commands/goal.md` short-description 56 → 48 chars (same content, `migrate-archive` kept); `.qoder/commands/speckit.goal.md` regenerated via `regen-command-copies.py`; module 4 passed |
| 7 | **one-line repair** — `summary_trigger` retired path pin | the pinned literal moves to `.specify/anchoring/<goal-slug>/summary/` (the T075 truth); module 35 passed |
| 8 | **VERIFY** — gates, suite diff, mirrors | § 3/§ 4; all targeted gates pass; suite parallel pass 186 failed / 8199 passed / 2 skipped, diff below; `sync-mirrors.py --write` + `--check` OK |

**Discovery during the wave**: the authorized migration moved the live 085 team tree out
of `.specify/specs/085-sdd-temporary-goal-team/team/…`, so the two disposal-table modules
that read that live path (`test_checkpoint_protocol.py` row 6, `test_checkpoint_rollback.py`
row 11) turned red the moment the apply landed — exactly the rewrite their table rows
prescribed. Both were repointed to `.specify/teams/085-sdd-temporary-goal-team/team.md`
in this wave. No test outside the disposal table pinned a moved path (checked by grep over
`tests/` for live `specs/08x|09x/(goal|team)/` references; remaining hits are fixtures or
the two repointed modules).

## 2. SC-003 — applied sequence (R1)

| Step | Reading | Evidence |
|------|---------|----------|
| `probe-residual` before | goal 8 / teams 8 | `repairwave-T079-probe-before.json` |
| `migrate-archive --dry-run` | 16 decisions (8 goal + 8 team), migrate 16, conflict 0, interrupted 0 | `repairwave-T079-dryrun.json` / `.err` |
| `migrate-archive --apply` | migrated 16, conflict 0, interrupted 0, **exit 0** | `repairwave-T079-apply.txt` |
| post `probe-residual` | goal 0 / teams 0 | `repairwave-T079-probe-after.json` |
| per-definition existence | **16/16 PASS**: target present (`.specify/anchoring/<slug>/goal.md` / `.specify/teams/<slug>/team.md`); source tree readable under `.specify/archive/goal-team/trees/`; source moved away; receipt present with `delete_policy: archive-not-delete` and `result: migrated` | `repairwave-T079-existence.txt` |
| idempotent re-run | 16 `noop`, 0 migrated, exit 0; sha256 snapshot of `.specify/anchoring` + `.specify/teams` + `.specify/archive/goal-team` **byte-identical** | `repairwave-T079-idempotent.txt` |

Receipts land one file per definition at `.specify/archive/goal-team/receipts/<kind>-<slug>.yaml`
(16 files); archived trees one directory per source spec at
`.specify/archive/goal-team/trees/<spec-dir-name>/<kind>/<slug>/` (8 directories).
The one-level non-conforming `.specify/specs/088-speckit-visualization/team/team.md` stays
outside the probe and the migration (residual risk 4).

## 3. Failing-set diff (pre-wave → post-wave)

- **Pre-wave set**: `.specify/.tmp/sdd-loop/tmp/gate1-094-failed.txt`, **152 ids** (the
  main-tree GATE-1 reading recorded at `12dc3e36a`).
- **Post-wave reading** (this worktree, canonical runner, parallel pass):
  **186 failed, 8199 passed, 2 skipped, 576 warnings in 41.28 s**; serial mini-pass
  1 passed (not GATE-1). Failed-name set: `repairwave-failed.txt` (186 ids).
- **Fixed = 24**, **New = 58**, arithmetic (152 − 24) + 58 = 128 + 58 = 186 — re-expressed 2026-11-10 (history wave G2): same readings, written so the truncated pair sum no longer hides the starting total
  (`repairwave-fixed-vs-pre.txt` / `repairwave-new-vs-pre.txt`, `LC_ALL=C comm`).

**Fixed (24)** — 23 are the wave's own ids:

- SC-010 family 18: `test_085_disposal_table` 1, `test_scope_resolution` 5,
  `test_temp_goal_contract` 2, `test_temp_team_schema` 2, `test_goal_scope_engine` 8;
- SC-002 2: `test_no_spec_local_writes` both ids;
- one-line repairs 3: `test_qoder_command_frontmatter` 1, `test_summary_trigger` 2.

**1 non-attributable fixed id**: `test_isomorphism_map::test_no_second_document_claims_map_ownership`
was red in the main-tree pre-wave reading and is green here; it passes standalone on this
tree and no wave change touches its subject — a teardown/leak-state difference between the
two readings, **not** claimed as a wave fix.

**New (58)** — every one belongs to one of two environment classes; none is attributable
to a wave change:

| Class | Ids | Cause |
|-------|-----|-------|
| Nested-worktree self-location (trigger engine / promotion / tuning / telemetry + the guard) | 57 (`test_trigger_engine` 25, `test_trigger_promotion` 18, `test_trigger_tuning` 12, `test_trigger_telemetry` 1, `test_ask_record_repeat` 1) | engines resolve the workspace root through the first literal `.specify` path component; from this worktree they land on the MAIN repo. Proof: `repairwave-self-location.txt` — `trigger-utils.py --action status` answers `workspaceRoot: /storage/project/cloud-native-ai/spec-kit` while `git rev-parse --show-toplevel` is this worktree. The family's exact membership varies with the live main-repo trigger state (last mutated by the wp07 runs; mutated again here — § 6 ANOMALY) |
| `REPO_ROOT` itself contains `.specify` | 1 (`test_docs_command_template::test_c10_runtime_copies_exist_for_every_present_tool`) | the test globs `**/speckit.history.*` and filters out any path whose parts contain `.specify`; every hit under this worktree carries that part, so the guard sees zero tool runtime dirs |

The remaining 128 pre-wave ids are unchanged (pre-existing families: goal/summary
integration suites, compile/wording-gate family, gate-count family, loop-state/lifecycle
family, pytest-pin mismatch, neutrality singles). None was touched or newly caused by
this wave.

## 4. Gates (all exit 0)

| Gate | Reading | Evidence |
|------|---------|----------|
| validate-requirements | 0 errors / 0 warnings | `repairwave-validate-requirements.txt` |
| validate-tasks | 0 errors / 1 warning (the disclosed forward edge `T043 → T054`, line 240) | `repairwave-validate-tasks.txt` |
| pre-analyze ×3 (requirements / plan / tasks) | `decision: pass`, errors 0, advisories 20 each | `repairwave-pre-analyze-*.{txt,json}` |
| decomposition plan / tasks | `proceed`, fr 43 / tasks 85 | `repairwave-decomposition-*.{txt,json}` |
| closure acceptance | `verdict: accept` (§ 0) | `repairwave-closure-acceptance.txt` |
| mirrors | `sync-mirrors.py --write` then `--check`: OK | `repairwave-mirror-check.txt` |
| per-tool copies | `regen-command-copies.py --check`: OK | — |

## 5. Residual risks (owned by the driver / next stage)

1. **GATE-1 must still be re-read in the main tree** after every `.specify/.tmp` fixture
   and worktree is removed (execution lesson 2). The worktree reading above is
   environment-degraded with named causes, never a pass.
2. **ANOMALY — main-repo trigger state mutated again**: the suite run (started
   `13:23:32Z`) wrote the MAIN repo's `.specify/memory/trigger/index.json`
   (mtime `2026-11-09 13:23:59 +0800`; `git status` in the main repo shows it modified).
   Same trap as wp07's ANOMALY 1; it cannot be prevented from a nested worktree. The
   driver decides whether to restore the main-repo file.
3. **Pre-existing reds outside the wave's causal surface** stay on the recorded baseline
   (128 unchanged ids). They are not claimed by any criterion of this feature.
4. The one-level `.specify/specs/088-speckit-visualization/team/team.md` remains outside
   the probe glob and the migration; a future ruling must dispose it explicitly.
5. **All 85 task sigils remain `- [ ]`**; the row-state sweep belongs to the driver's
   integration close-out, not to this wave.
6. **SC-010's "contract suite all green" limb** is recorded as its own implementation
   decides it (T065 guard: zero new failing ids against the frozen serial baseline for
   the disposal surface). Literal zero-red across the whole contract suite is not claimed
   because pre-existing families are red on the baseline; the disclosure is in
   `verification.md` SC-010_note.
7. Registry row 094 still reads `Planned`; the claim is consistent with the closure
   verdict and is not raised by this note.

## 6. Commits

- `fix(094-repairwave): close the closure block — SC-003 apply, SC-002 pin, SC-010 disposal, one-line repairs`
  — the six rewritten test modules, the two checkpoint path repoints, the disposal-table
  exclusion repair, the SC-002 pin, `templates/commands/goal.md` + its regenerated `.qoder`
  copy, and the applied migration data (moved spec-local trees, 16 receipts, 16 archive
  definitions).
- `docs(094-repairwave): record R1/R2 rulings, verification statuses and the wave readings`
  — `requirements.md`, `verification.md`, this note and the `repairwave-*` evidence files.
