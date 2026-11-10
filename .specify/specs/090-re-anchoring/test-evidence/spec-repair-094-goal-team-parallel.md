# Spec repair — 094-goal-team-parallel

- **Date**: 2026-11-10
- **Spec**: `.specify/specs/094-goal-team-parallel/` (live, not archived)
- **Inputs**: prior audit `.specify/specs/090-re-anchoring/test-evidence/spec-audit-live-batch-6.md`, `spec-audit-live-batch-7.md` § `094-goal-team-parallel` (:212–245), `spec-audit-summary.md`; deterministic settled scan `spec-audit-settled.json` → `.specify/specs/094-goal-team-parallel` (`refs 262 / alive 210 / moved 210 / dead 52`, 19-entry `dead_list`).
- **Counting unit**: one occurrence per `(file, line, longest matching stale path)` — nested tokens (e.g. `.specify/goal` inside `.specify/goal/demo-command-goal/goal.md`) are counted once against the most specific path. The settled `dead: 52` is a distinct-path count; the occurrence census below is larger because the `.specify/goal` family alone has 442 line-occurrences in dated records.

## Counts

| Bucket | Count |
|---|---:|
| Dead references reviewed (line-occurrences, 28 path entries) | **1007** |
| Live-fixed | **3 lines / 4 path instances** |
| Dated-kept | **981** |
| Non-reference | **23** (15 substring matches of a live path + 8 examples/retirement statements) |

Entry-set derivation: 18 distinct entries from the settled `dead_list` (the `094-repairwave`/`094-repairwave/` pair is one path) + 9 audit-named extras (`shared/workflows/feedback-step.md`, `.specify/teams/team.md`, `.specify/specs/091-auto-git-closeout/team`, `.specify/anchoring/demo-command-goal/goal.md`, `.specify/goal/demo-command-goal/goal.md`, `.specify/specs/900-fixture/goal`, `.specify/.tmp/sdd-loop/tmp/gate1-094-failed.txt`, `.specify/specs/092-goal-team-parallel`) plus the anchor-rename family `.specify/memory/`, with the s094 scratch prefix shown as two rows = 28 rows.

## Live-fixed (before → after)

| # | Location | Before | After | Basis |
|---|---|---|---|---|
| 1 | `plan.md:59` | `.specify/memory/constitution.md` | `.specify/constitution.md` | Live normative pointer (Constitution Check source); target exists |
| 2 | `plan.md:64` | `.specify/memory/features.md` | `.specify/features.md` | Live normative pointer (feature registry); target exists |
| 3 | `plan.md:64` | `.specify/memory/features/094.md` | `.specify/features/094-goal-team-parallel.md` | Live normative pointer (feature detail); target exists, slug confirmed `# 094 — Goal/Team Parallel` |
| 4 | `notes/red-first-evidence.md:6` | `shared/workflows/feedback-step.md` | `shared/workflow/feedback-step.md` | Standing owner citation in the file's format preamble; the singular path is the only live owner (`shared/workflow/feedback-step.md`), the plural never existed |

No validator exists for `plan.md` or `notes/red-first-evidence.md`; the spec-level validators were re-run (below).

## Per-entry disposition

`D` = dated-kept (dated record: `notes/**`, `test-evidence/**`, `verification.md`, `checkpoints/**`, or a dated passage — never rewritten). `N` = non-reference (example / placeholder / retirement statement). `F` = live-fixed.

| # | Dead entry | Occ | Disposition | Evidence locations / note |
|---|---|---:|---|---|
| 1 | `.specify/.tmp/s094-*` | 2 | D | `notes/closure-readings.md:185`; `test-evidence/wp02-T083-mutation.txt:6` — sanctioned scratch, removed by teardown |
| 2 | `.specify/.tmp/s094/*` | 95 | D | `quickstart.md:35,36,124`; `tasks.md:143,493`; `notes/**`; `test-evidence/**` — transient `.specify/.tmp/` paths |
| 3 | `…/test-evidence/migration-applied.json` | 1 | D | `quickstart.md:59` — runtime redirect target of walk S-3; absent because the walk was not run in the real tree |
| 4 | `…/test-evidence/residual-before.json` | 1 | D | `quickstart.md:49` — same, S-2 runtime output |
| 5 | `.specify/.tmp/s092*` | 10 | D | `notes/analyze-round1-repair.md:11`; `notes/analyze-round3/repair-r2.md:69`; `notes/analyze-round4/fix-w1.md:69,70`; gate readings under `test-evidence/` |
| 6 | `.specify/.tmp/sdd-loop/worktrees/094-repairwave` | 13 | D | `notes/repairwave.md:5,14`; `notes/review-arc.md:25`; `test-evidence/repairwave-*` |
| 7 | `.specify/.tmp/sdd-loop/forks/094-wp0` | 2 | D | `notes/review-process-artifacts.md:82`; `test-evidence/wp05-T044-mutation.txt:7` |
| 8 | `.specify/.tmp/sdd-loop/tmp/gate1-094-failed.txt` | 6 | D | `verification.md:21`; notes/test-evidence gate records |
| 9 | `.specify/specs/092-non-disposable/team/team.md` | 1 | D | `notes/implement-wp02.md:130` — pre-change measurement record |
| 10 | `.specify/specs/088-speckit-visualization/team/088-reporting-dogfood/team.md` | 9 | D | `notes/pre-change-measurements.md:45`; `test-evidence/migration-dryrun.json`, `repairwave-T079-*`, `wp02-T083-probe-before.json`, `wp07-T079-*` |
| 11 | `.specify/specs/092-non-disposable/notes/refactor-anchoring-merge.md` | 1 | D | `notes/analyze-round3/w3-trunk-reconciliation.md:266` |
| 12 | `.specify/specs/094-goal-team-parallel/team/094-goal-team-parallel/team.md` | 8 | D | `notes/pre-change-measurements.md:49`; `test-evidence/migration-dryrun.json`, `repairwave-T079-*`, `wp02-T083-probe-before.json`, `wp07-T079-*` — old spec-local team slot in pre-migration readings |
| 13 | `.specify/specs/085-sdd-temporary-goal-team/goal/085-sdd-temporary-goal-team/goal.md` | 16 | D | `notes/pre-change-measurements.md:28`; `test-evidence/checklist-readings-2026-11-09.txt`, `migration-dryrun.json`, `repairwave-*`, `requirements-baseline-probe.txt`, `wp02-T083-probe-before.json`, `wp07-T079-*` |
| 14 | `.specify/specs/069b-isomorphism-migration-metrics/contracts/ledger-reconciler.md` | 1 | D | `notes/review-implementation-code.md:90` (D-I1 finding quotes the pre-archive path) |
| 15 | `.specify/specs/088-speckit-visualization/goal/088-speckit-visualization/goal.md` | 10 | D | `notes/pre-change-measurements.md:31`; `test-evidence/checklist-readings-2026-11-09.txt`, `migration-dryrun.json`, `repairwave-*`, `requirements-baseline-probe.txt`, `wp02-T083-probe-before.json`, `wp07-T079-*` |
| 16 | `.specify/specs/069b-isomorphism-migration-metrics` (dir) | 38 | D | `notes/closure-readings.md:91`, `implement-wp06.md:27,78`, `review-consolidated.md:37`, `review-implementation-code.md:90`; `test-evidence/wp06-neighbourhood.txt`, `wp07-closure-suite.out` — archived source paths recorded before/after consolidation |
| 17 | `.specify/specs/092-goal-team-parallel` (old number) | 98 | D | `notes/analyze-round4/vc-anchoring.md:110` explicitly rules "dated evidence, must keep"; all other hits are `test-evidence/` gate readings |
| 18 | `.specify/specs/091-auto-git-closeout/team` | 11 | D | `requirements.md:10` is the verbatim user `Input` quote (kept by the spec's own D5 decision); `notes/pre-change-measurements.md:48`; `test-evidence/` probe readings |
| 19 | `.specify/specs/900-fixture/goal` | 2 | D | `notes/implement-wp06.md:17`; `test-evidence/wp01-T005-red.txt:293` — fixture example recorded inside dated records |
| 20 | `.specify/anchoring/demo-command-goal/goal.md` | 15 | D 12 / N 3 | N: `quickstart.md:42,80,82` — demo walk S-1/S-5 example path, never created in the real tree; D: `test-evidence/` gate readings |
| 21 | `.specify/goal/demo-command-goal/goal.md` | 19 | D | `notes/analyze-round4/fix-w2.md:21`; `test-evidence/` pre-analyze/precheck readings |
| 22 | `.specify/teams/demo-crew/team.md` | 1 | N | `quickstart.md:103` — S-7 illustrative fixture (`demo-crew` team never created) |
| 23 | `.specify/teams/team.md` | 1 | D | `notes/review-implementation-code.md:92` — old global-team path in a review record |
| 24 | `.specify/templates/commands/` | 35 | D 32 / N 3 | N: `plan.md:248`, `tasks.md:79`, `feature-ref.md:117` — retirement statements ("NO mirror (retired)" / "is retired" / quoted advisory), not live pointers; D: `test-evidence/` pre-analyze advisory readings |
| 25 | `shared/workflows/feedback-step.md` | 1 | **F** | `notes/red-first-evidence.md:6` → `shared/workflow/feedback-step.md` |
| 26 | `.specify/memory/` (anchor-rename family) | 153 | D 151 / **F** 2 lines | F: `plan.md:59`, `plan.md:64` (3 path instances, see table above); D: `requirements.md:262` (dated clarification), `verification.md:108`, `notes/**`, `test-evidence/**` (longest-match census) |
| 27 | `.specify/goal` (strict, excl. `goal-team`) | 442 | D 441 / N 1 | Historical statements with explicit rename disclosure (`plan.md:11,16,47,110,111,134,163`; `requirements.md:10,19,153,251,304,309`; `research.md:19,35,88,132`), dated `checkpoints/**`, `notes/**`, `test-evidence/**`; N: `plan.md:141` — hypothetical downstream mapping example (`--scope goal` → `.specify/goal/`) |
| 28 | `scripts/territory-check.py` | 15 | N | Every occurrence is a substring or tree-relative mention of the live `skills/internal/create-team/scripts/territory-check.py` (`quickstart.md:102`; `notes/implement-wp04.md:79,104`, `implement-wp04b.md:71`, `implement-wp06.md:7`, `review-implementation-code.md:82`; `test-evidence/wp04-*`, `wp06-*`) |

## Registry

Row `094` at `.specify/features.md:101` resolves: Feature Details `.specify/features/094-goal-team-parallel.md` (content matches), Spec Path `.specify/specs/094-goal-team-parallel/requirements.md` (exists). **No registry edit.**

## Validator readings (after the fixes)

```text
$ python3 .specify/scripts/python/validate-requirements.py .specify/specs/094-goal-team-parallel/requirements.md
file: .specify/specs/094-goal-team-parallel/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
  [path-marker] pass (0)
scanned: 331 lines, 55 definition rows, 6 shared strings
0 error(s), 0 warning(s)
exit 0

$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/094-goal-team-parallel/tasks.md
WARN  240: blockedBy: T043 references later task T054 (forward dependency — verify this is intentional)
PASS (with warnings): .specify/specs/094-goal-team-parallel/tasks.md — 0 error(s), 1 warning(s)
exit 0
```

The single warning is the already-adjudicated declared cross-package edge `T043 → T054` recorded in `tasks.md` § Green Partition — unchanged, not silenced.

## Out-of-scope observations (no edit)

- The audit's "Guards" section names `test_residual_probe.py` (`plan.md:354`) and `tests/contract/test_command_run_goal_team.py` (`contracts/owner-rewrites-and-tests.md:128`); neither exists anywhere in the tree and the latter is disclosed in `tasks.md:180-181` as never authored (closed by delegation under ruling R2). No target exists and none was invented; neither is in the settled `dead_list`.
- `notes/review-implementation-code.md:90` (D-I1) records live normative pointers dangling in **other** documents (`shared/definitions/non-disposable-definitions.md`, `shared/definitions/flow-class-definitions.md`, `.specify/skills/internal/manage-history/SKILL.md`, `.specify/memory/features/090.md`). They are outside this spec's directory and were not touched; that note itself is a dated record.
- `plan.md:16,47,110,111,134,163` and `requirements.md:19,304,309` mention `.specify/goal/` only as the pre-rename literal with an explicit 2026-11-09 rename disclosure; rewording them would rewrite a dated reading, so they are kept.

Anomaly: the settled scan's `scripts/territory-check.py` entry is a substring false positive — all 15 occurrences are the live `skills/internal/create-team/scripts/territory-check.py` (or a tree-relative mention inside it); recorded as non-reference and nothing was changed.

Files changed: `.specify/specs/094-goal-team-parallel/plan.md`, `.specify/specs/094-goal-team-parallel/notes/red-first-evidence.md`. No commit, no push, no subagents.
