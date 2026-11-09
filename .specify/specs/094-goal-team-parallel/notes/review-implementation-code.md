# Review — segments C (implementation) and D (code) — 094-goal-team-parallel

**Date**: 2026-11-09 · **Reviewer**: Qoder agent (segment C+D seat of a split `/speckit.review` run)
**Tree**: main repo `/storage/project/cloud-native-ai/spec-kit` · **Base**: `4420076ca` (caller-supplied,
resolved via `skills/internal/code-review/scripts/git-delta-review.sh base --since 4420076c --head HEAD
--json` → `base_source: explicit`) · **Head**: `19003b6131efab4ecdc451f7df8f3e199270a792` (run-start HEAD,
`19003b613`).

**Method**: `.specify/skills/internal/review-feature-quality/SKILL.md` § Segment B for the implementation
segment, `.specify/skills/internal/code-review/` six-level vocabulary for the code segment, composed per
`templates/commands/review.md`. **Writes**: this file only.

**Uncommitted scope (disclosed, never concluded over)**: the working tree carries changes outside the
094 delta — `.specify/memory/trigger/index.json` (mutated by the repair-wave full-suite run; the
repairwave ANOMALY), the study-code restructure (`skills/external/study-code/**`,
`tests/**` helper renames) and small coaching edits. The code judgment is made against HEAD `19003b613`;
none of the uncommitted scope is attributed to, or excused by, this review.

---

## 1. Segment C — Implementation Review

### C.1 Base / head / smoke triple

| Field | Value |
|-------|-------|
| Base commit | `4420076ca` (`base_source: explicit`) |
| Head commit | `19003b613` |
| Smoke command (verbatim) | `python3 -m pytest tests/contract/test_archive_migration.py tests/contract/test_handoff_contract.py tests/contract/test_handoff_territory.py tests/contract/test_parallel_lines.py tests/integration/test_parallel_lines.py tests/contract/test_criterion_vocabulary_scan.py tests/contract/test_binding_model.py tests/contract/test_resident_backfill.py tests/contract/test_migration_interruption.py tests/contract/test_declaration_facts.py -q` |
| Smoke exit code | `0` |
| Smoke evidence path | this file, § C.2 row S-1 (output embedded verbatim below; the recorded run at HEAD reproduces the claimed `wp07-smoke.out` reading) |

### C.2 Closure evidence, file by file

Every row below was re-executed or re-derived on this tree; the "reproduced" column is the reading this
run obtained, not a restatement of the feature's claim.

| # | Claim (owner) | Retained artifact | Reproduced this run |
|---|---------------|-------------------|---------------------|
| S-1 | Smoke: 54 passed, exit 0 (`verification.md:30-32`, T079 smoke record) | `test-evidence/wp07-smoke.out` (54 passed) | **54 passed in 7.11s, exit 0** (command verbatim above) |
| S-2 | Closure verdict `accept`, `final_path: pass=8 blocked=0 deferred=0 partial=0 fail=0 unknown=0 total=8` (`notes/repairwave.md` § 0) | `test-evidence/repairwave-closure-acceptance.txt` | `closure-acceptance-check.py --json` → `accept`; final_path identical; all four `completion_conditions` true (smoke record pass included) |
| S-3 | Apply: 16 migrated (8 goal + 8 team), conflict 0, interrupted 0, exit 0 (`repairwave.md` § 2) | `repairwave-T079-apply.txt`, `repairwave-T079-existence.txt` (16/16 PASS) | Independent verifier over the 16 receipts: every `target_path` is a file, every `archived_path` a directory, every receipt carries `delete_policy: archive-not-delete`, `result: migrated`, and the target's `origin` equals `source_spec` — **0 problems** |
| S-4 | Idempotent second apply: 16 noop, zero bytes written (`repairwave.md` § 2) | `repairwave-T079-idempotent.txt` | `goal-utils.py migrate-archive --dry-run --json` → `{"migrated": 0, "noop": 16, "conflict": 0, "interrupted": 0}`, exit 0 |
| S-5 | Residual surface empty (C-43 / GATE-3) | `repairwave-T079-probe-after.json` | `goal-utils.py probe-residual --json` → goal `[]`, teams `[]`, counts 0/0; on-disk `specs/*/goal/*/goal.md` and `specs/*/team/*/team.md` both 0 (the one-level `088-speckit-visualization/team/team.md` remains, disclosed residual risk 4) |
| S-6 | archive-not-delete: source trees readable under `trees/` (`repairwave.md` § 2) | `test-evidence/repairwave-T079-existence.txt` | 18 `.md` files under `.specify/archive/goal-team/trees/`; diff of migrated 085 goal **and** team against their archived copies = **identical minus the `binding` block** |
| S-7 | Binding exhaustive: 18 residents backfilled (6 goal + 12 team), second run zero writes; 34/34 archive definitions carry binding (`verification.md:88`) | `resident-backfill-applied.json`, `resident-backfill-second-run.txt`, `repairwave-binding-coverage.txt` | Recount on disk: **14 goals + 20 teams = 34/34 complete bindings**; second-run file: 18 `already-bound`, `EXIT=0` |
| S-8 | Disposal-family modules green (`repairwave.md` § 1 items 5–7; `verification.md` SC-002/SC-010) | per-module readings cited in `repairwave.md` | Targeted run: **87 passed, exit 0** — `test_scope_resolution` 9, `test_temp_goal_contract` 8, `test_temp_team_schema` 9, `test_goal_scope_engine` 9, `test_checkpoint_protocol` 6, `test_checkpoint_rollback` 1, `test_085_disposal_table` 2, `test_no_spec_local_writes` 4, `test_qoder_command_frontmatter` 4, `test_summary_trigger` 35 |
| S-9 | Supplementary guards (`wp03`/`wp04`/`wp06` guard modules not in the smoke list) | — | **39 passed, exit 0** — `test_command_family`, `test_feedback_command_template`, `test_sdd_loop_driver_skill`, `test_framework_map_archive_row`, `test_goal_command_template`; plus `tests/integration/test_archive_migration_real_data.py` **1 passed, exit 0** |
| S-10 | Failing-set diff 152 − 24 + 58 = 186 (`repairwave.md` § 3) | pre set `.specify/.tmp/sdd-loop/tmp/gate1-094-failed.txt` (152 lines, still present), `repairwave-failed.txt` (186), `-fixed-vs-pre.txt` (24), `-new-vs-pre.txt` (58), `repairwave-suite.out` (`186 failed, 8199 passed, 2 skipped`) | Arithmetic re-derived: 152 − 24 + 58 = 186 ✓. Environment classes as disclosed (worktree self-location 57 + REPO_ROOT 1); the non-attributable fixed id is explicitly not claimed |
| S-11 | Gates: validate-requirements 0/0; validate-tasks 0 errors/1 warning; pre-analyze ×3 pass (fr 43 / sc 12 / tasks 85); decomposition proceed; mirrors OK; GATE-7 interface (`repairwave.md` § 4) | `repairwave-validate-*.txt`, `repairwave-pre-analyze-*`, `repairwave-decomposition-*`, `repairwave-mirror-check.txt` | `validate-tasks.py` → `PASS (with warnings) — 0 error(s), 1 warning(s)` (line 240, the disclosed T043→T054 forward edge); `sync-mirrors.py --check` → exit 0 on the current tree; `goal-utils.py --version` → `0.0.22` exit 0, `migrate-archive --bogus-option` → exit 2; pre-analyze/decomposition readings match the artifacts (20 advisories each; fr 43 / tasks 85) |
| S-12 | SC statuses match the `Path` markers (8 final, 4 supporting) | `verification.md:38-89`, `requirements.md` **Path** markers | 8 × `final` all `pass`; 4 × `supporting` (SC-001 `partial`, SC-009/010/011 `pass`) — matches the closure `total=8` |
| S-13 | Row-state sweep: zero open rows (GATE-4) | `tasks.md` | `0` rows matching `^- \[[ >]\] T`; `85` rows `[x]`; `validate-tasks` 0 errors |

**SC-001 (partial) is honest**: `verification.md:39-45` states its own guard is absent and that no pass is
claimed; ruling R2 (`requirements.md:271-274`) re-scopes the criterion. The criterion reads exactly what
its evidence supports. The related **row-state** problem is F-C1 below.

### C.3 Findings (P0 / P1 / P2 — owner: `review-sdd-process`)

| Severity | Artifact / path | Line | Finding |
|----------|-----------------|------|---------|
| **P1** | `.specify/specs/094-goal-team-parallel/tasks.md` | 180–186 | **F-C1 — T016–T019 read `[x]` while their named deliverables are absent.** T016/T017 cite `tests/contract/test_command_run_goal_team.py` (the file does not exist on this tree); T019 claims "the engine's `create` action write[s] owner, owner_id and origin" with "evidence: scripts/python/goal-utils.py (create binding write)" — `create_goal` (`scripts/python/goal-utils.py:1074-1101`) writes no binding block, and `verification.md:39` says so verbatim. Ruling R2 re-scopes SC-001 but says nothing that makes a nonexistent module an evidence target; the sigil sweep (commit `19003b613`) closed rows whose text still asserts closed deliverables. Repair: re-word T016–T019 to the R2 disposition (closed-by-delegation, named owners SC-004/SC-005) or reopen them; either way remove the two falsified evidence pointers. |
| **P2** | `.specify/specs/094-goal-team-parallel/tasks.md` | 40 | **F-C2 — DoD-7 keeps a stale final-path list.** It still enumerates "SC-001, SC-002, SC-003, SC-004, SC-005, SC-006, SC-007, SC-008, SC-012 are `final`", but `requirements.md:198` re-scoped SC-001 to `supporting` by ruling R2. The authoritative checker reads `requirements.md` (and returns total=8), so this is a second, stale statement of the set `shared/workflow/acceptance-hardening.md` owns. Repair: replace the enumeration with a pointer, or align it to `requirements.md`. |
| **P2** | `.specify/specs/094-goal-team-parallel/tasks.md` | 37, 329 | **F-C3 — T079/DoD-4 evidence pointers name two files that do not exist.** Both rows cite `test-evidence/migration-applied.json` and `test-evidence/residual-after.txt`; the retained artifacts are `repairwave-T079-apply.txt` and `repairwave-T079-probe-after.json` (`repairwave.md` § 2 records the supersession). SC-003's pass itself is fully backed; the row's pointer is dangling, so a reader following T079 lands on nothing. Repair: re-point the two rows at the repairwave names (or at `notes/repairwave.md` § 2). |
| **P2** | `.specify/specs/094-goal-team-parallel/notes/red-first-evidence.md` | 125 | **F-C4 — the T044 mutation record says the command is "recorded verbatim in the evidence file", but no command exists there.** `test-evidence/wp05-T044-mutation.txt` holds only three lines (`clean exit: 0 | verdict: ok` / `mutated exit: 2 | error: injected-requires-spec-line` / `MUTATION TURNS THE PEER-B PATH RED: yes`) — no command, no date, no fixture. The discriminating outcome is recorded; the reproduction path is not. Same class in `verification.md:64`: SC-006's "threshold-illegal/absent red reading" is attributed to `wp03-T051-red.txt`, but that file's failure is `error: unrecognized option: --tasks` — a pre-implementation red-first, not a declaration-mutation reading. Repair: add command + fixture identity to the T044 file; re-describe SC-006's pointer (the declaration-refusal arms live in `test_declaration_facts.py::test_handoff_decision_refuses_when_the_fact_is_unavailable` and `::test_a_fact_in_another_grammar_is_refused_at_load`). |
| **P2** | `.specify/specs/094-goal-team-parallel/requirements.md` | 327 (A8), `tasks.md` 30 | **F-C5 — the feature's own run is `handoff` under its own threshold but carries no handoff artifact.** `handoff-decision --tasks .specify/specs/094-goal-team-parallel/tasks.md` → `handoff, task_count 85, threshold 10`; no `<spec>/handoff.md` and no `writeback/` exist. A8 discloses that the feature's own run follows the pre-094 protocol, so this is not a criterion violation — but it means the real-tree creation-timing + handoff path is proven only on fixtures, never dogfooded. Repair: when the next slice runs on this spec, drive it through the new path (or record a dated rationale in `verification.md`). |

**Segment C verdict**: `pass` — every `final`-path criterion's pass is reproducible from a retained
artifact (S-1…S-13), the one non-pass criterion is honestly reported, and no P0 exists. The P1 is a
bookkeeping/acceptance-honesty defect in `tasks.md`, not a falsified SC reading.

---

## 2. Segment D — Code Review

### D.1 Delta judged

`git diff 4420076c..HEAD`, scoped as directed: `scripts/python/goal-utils.py` (+1477/−61),
`shared/declarations/**` (the two 094 facts + `contract.yaml` registration), `shared/definitions/**`
(goal-definitions, sdd-routing, framework-map — 094 hunks), `templates/commands/{goal,team,feedback}.md`,
`skills/internal/create-team/**` (+427/−22 incl. `references/handoff-contract-template.md` and
`scripts/territory-check.py`), `skills/external/sdd-loop-driver/**`, `tests/**` (094 modules). The range
also carries sibling-line changes (090/092 non-disposable merge, 069 consolidation, study-code); only
094-attributable hunks are judged, plus the cross-line consistency items the brief names.

### D.2 Findings (six-level — owner: `code-review`)

| Severity | File:line | Finding |
|----------|-----------|---------|
| **important** | `shared/definitions/non-disposable-definitions.md:39,48,134,490,637`; `shared/definitions/flow-class-definitions.md:36,135,141,149,157,159,160,203,208,213,221`; `.specify/skills/internal/manage-history/SKILL.md:200`; `.specify/memory/features/090.md:45` | **D-I1 — the consolidation archive left live normative pointers dangling.** These owner/registry docs cite `.specify/specs/092-non-disposable/{data-model,plan,requirements}.md` and `.specify/specs/069b-isomorphism-migration-metrics/contracts/ledger-reconciler.md` as live paths. Both directories were moved to `.specify/archive/specs/` by `c5b17a9fc`; neither cited path exists (`ls .specify/specs/069b-isomorphism-migration-metrics` → No such file), while the archived copies do. Unlike the dated feature-detail bodies (which carry an appended consolidation note and are historical records), these are normative owner documents whose authority chain now fails at the cited path. Repair: re-point the five 092 refs to `.specify/archive/specs/092-non-disposable/...`, the eleven 069b refs likewise, and re-sync mirrors. |
| **important** | `scripts/python/goal-utils.py:599` (+ `1074-1101`, `2814-2817`) | **D-I2 — the engine cannot bring a freshly created definition into the binding model.** `create_goal` writes no binding block, and `bind_definition` begins with `current = read_binding(path)`, which raises `binding-missing` before any rewrite. Reproduced on a scratch fixture under `.specify/.tmp/` (cleaned): `create` exit 0 → `binding` exit 2 `binding-missing` → `bind --owner command-run --owner-id r…` exit 2 `binding-missing`; only `backfill-bindings --apply` repairs it, and it stamps `owner: human / owner_id: human / origin: null` regardless of the true creator. This is the code-level root of F-C1/SC-001: the "only legal ownership-write path" (FR-003) has no entry point for new definitions. The R2 ruling accepts the missing T019 write, but the *engine's* documented bind path remains unreachable-by-construction for `create` output; a probe is already written (`verification.md:45` `SC-001_unblock`). |
| **suggestion** | `scripts/python/goal-utils.py:117-120`, `549-551`, `579-582`, `1476-1478` | **D-S1 — the retired "default team at `<team-root>/team.md`" branch survives in four places.** `Scope.team_definition`, `bound_team_slugs`, `_path_for_kind` and `run_checks` all prefer `<team-root>/team.md` over `<team-root>/<slug>/team.md` when the former exists. In the new model team definitions live only at `.specify/teams/<slug>/team.md`; a stray `.specify/teams/team.md` would be read (and, via `bind teams <slug>`, **written**) as the definition for *any* slug. Recommend deleting the branch or refusing the path with a named error. |
| **suggestion** | `scripts/python/goal-utils.py:2045` | **D-S2 — the receipt-write step is labelled `"source-move"`.** `step(lambda: _write_receipt(...), "source-move")` means an `OSError` while writing the receipt produces `_Interrupted("source-move", …)`, so C-39's "reports its reached step" reports the wrong step (recovery still succeeds via the orphan path). Also `FAULT_STEPS` (`:1678`) has no `receipt-write`, so the seam cannot inject at the third step. Fix the label and add the step to the closed fault set, or state why the third step is not injectable. |
| **suggestion** | `scripts/python/goal-utils.py:1983-2003` | **D-S3 — `_noop_decisions` trusts the receipt without re-reading its target.** A second `migrate-archive` reports `noop` for every migrated receipt even if the target definition has since been deleted or overwritten, so the idempotency reading can stay green while the archive has lost the definition. A one-line `target.is_file()` + digest check would make the noop claim measured, not remembered. |
| **nitpick** | `scripts/python/goal-utils.py:348-353` | **D-N1 — `archive_root`'s docstring describes a deleted concept**: "or the active spec's `goal/` subtree when a spec scope is resolved". There is no spec scope any more; `_ACTIVE_SCOPE.goal_root` is always `.specify/anchoring`. The same wording invites a future writer to reintroduce the retired branch. |
| **question** | `scripts/python/goal-utils.py:2331-2333` | **D-Q1 — confirm the intended failure mode of `command-family` on a degraded declaration layer.** When the family fact is absent/unregistered the action refuses with exit 2 (`owner-unavailable`), while an absent *carrier* answers `in_family: false` without failing. Tests pin both (`test_declaration_facts.py:241-260`, `test_command_family.py`), so this is likely deliberate; the question is whether a read that only needs the class predicate should be blocked by a declaration-layer outage. |

**Praise**: the mutation arms are genuine (in-memory reverted copies over the real checker, not prose
claims); the migration module drives the real CLI over fixture repositories and proves interruption
through a declared, closed fault seam; the canonical-binding-form check makes hand edits a named refusal;
the vocabulary guard is predicate-based (classification-use) instead of a word ban; and the two declaration
facts carry their consumers and registration together, with the engine reading them through the one
declaration reader.

### D.3 Test intent preservation (rewritten 085 modules)

| Module (disposal row) | Intent before → after | Weakened? |
|---|---|---|
| `test_scope_resolution.py` (row 1) | "global scope roots" → "goal/teams scope roots"; "spec scope requires spec-dir" → parametrized "retired scopes refused with invalid choice"; "spec write leaves global stores byte-identical" → "goal write leaves team store byte-identical **and adds no `.specify/specs/` path**" (stronger) | No |
| `test_temp_goal_contract.py` (row 2) | "temporary goal under the spec, absent from global" → "goal in the unified archive, spec-local tree absent, archived source readable"; adds the binding-record assertion | No |
| `test_temp_team_schema.py` (row 3) | spec-scoped schema `scope: spec` → archive binding (`binding:`, `owner: human`, `origin: …`), lifecycle and stage-seat assertions unchanged | No |
| `test_goal_scope_engine.py` (row 9) | `global/spec` path pairs → `goal/teams` pairs; the two "spec-scope" cases become a parametrized refusal for both retired values | No |
| `test_checkpoint_protocol.py` (row 6) | part 2 retitled "Goal progress"; adds the new-key/stage-chain/retired-syntax guard; the four-part and sentinel assertions stay | No |
| `test_checkpoint_rollback.py` (row 11) | path repoint only | No |

No `pytest.skip`, `xfail` or `skipif` exists in any of the twelve 094-authored modules; assertion bodies
drive the engine as a subprocess. The six rewritten modules plus the two line-repair targets are green
(S-8), and their old facts are not silently dropped.

### D.4 Cross-line consistency

- **092→094 rename**: no runtime surface references `092-goal-team-parallel`; the remaining hits are the
  dated session/feedback records and the historical note in `features/094.md:67-71` — legitimate under the
  non-disposable discipline. `features.md` row 092 reads `Relocated` with the archive pointer; the
  consolidation ledger (`.specify/archive/specs/CONSOLIDATION-LEDGER.md`) matches the moved directories.
- **Consolidation archives**: feature-detail bodies keep historical paths + an appended consolidation
  note (073/090/092 pattern) — accepted as the dated-record form; the *normative* owner docs are the
  exception and are D-I1.
- **Owners cross-cite**: `goal-definitions.md` → `conceptual-model.md` and back; neither restates the
  other's value domain (guarded by `test_binding_model.py::test_the_two_owners_cite_each_other_and_restate_no_value_domain`, green).
- **Framework-map / templates / driver**: Goals/Teams/archive rows, both command templates and the driver
  `Goal/Team（binding model）` sentence all name `.specify/anchoring/` + `.specify/teams/` and no spec
  subdirectory; `test_no_spec_local_writes.py` (4 passed) pins the write set and both mutation arms.

**Segment D verdict**: `pass` — no `blocking` finding. Two `important`, three `suggestion`, one
`nitpick`, one `question`; the delta is correct where every final-path behavior is exercised, and the
test rewrites preserve intent.

---

## 3. Residual risks carried forward (owned by the driver / next stage)

1. **GATE-1 is still not a main-tree reading.** The repair wave ran in a nested worktree; its 186-id
   reading is environment-degraded with named causes (worktree self-location 57 + `REPO_ROOT`-contains-
   `.specify` 1). The valid GATE-1 (main tree, serial, after `.specify/.tmp` teardown) is outstanding
   (`repairwave.md` § 5.1; `verification.md:103`).
2. **The 092/069b pointer drift (D-I1)** touches documents outside the 094 write domain; fixing it is a
   small follow-up, but it should not be lost — the owner pages are the reachable authority chain.
3. **The one-level `.specify/specs/088-speckit-visualization/team/team.md`** stays outside the probe glob
   and the migration; a future ruling must dispose it explicitly (`repairwave.md` § 5.4).
4. **Uncommitted tree state** (trigger index mutation + study-code/coaching edits) is disclosed in the
   header; the repairwave ANOMALY (main-repo trigger state mutated by the nested-worktree suite) stands
   until the driver decides to restore `.specify/memory/trigger/index.json`.

**ANOMALY**: the main-tree working copy carries uncommitted changes outside the 094 delta — the
repair-wave suite mutated `.specify/memory/trigger/index.json` (the disclosed nested-worktree
self-location trap) and concurrent study-code/coaching edits are present — so the code judgment was made
at committed HEAD `19003b613` and no conclusion is issued over the uncommitted scope. In-passing repairs
made by this review: none (read-only seat; only this notes file was written).
