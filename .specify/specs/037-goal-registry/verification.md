# Verification — 037-goal-registry (Feature 041 Goal Registry)

**Date**: 2026-08-05
**Baseline**: 39 failed / 1308 passed / 1 skipped (`baseline-failed.txt`, reconciled at T001)
**Final gate**: 39 failed / 1480 passed / 1 skipped — **zero new failures vs baseline**; +172 passed (201-era 036 tests preserved + this requirement's new suites).
**Mirror parity**: `python3 scripts/python/sync-mirrors.py --check` exit 0.

Every success-criterion line below cites the task whose measurement produced it (GATE-8). No status is asserted without a measuring task.

## Success Criteria

| ID | status | Measured by | Evidence |
|----|--------|-------------|----------|
| SC-001 | `pass` | T028 | `goal-utils list` enumerates the archive (slug, status, criteria count) from the directory alone; two goals created and listed with no team file read. |
| SC-002 | `pass` | T029, T036 | Two teams sharing one `goal_slug` resolve byte-identical objective + criteria from one `goal.md`; editing the definition changes both with no team edit. |
| SC-003 | `pass` | T059 | All 4 real teams are inline-only and resolve via fallback with zero edits; the four-patterns integration test is green. |
| SC-004 | `pass` | T035, T057 | After migration a goal's objective exists in exactly one definition + identity-only team references (down from frontmatter `goal` + `## Goal`). |
| SC-005 | `pass` | T029 | A team referencing a nonexistent identity is reported as a broken link naming the missing identity; falls back to the inline goal, never an empty one. |
| SC-006 | `pass` | T036 | Narrative + milestones sourced from the definition when present; the "goal bodies disagree" arbitration gap drops to 0; no-definition fallback identical to 036 (zero regression in its suite). |
| SC-007 | `pass` | T057 | Migration preserves the resolved objective (before/after `project_desc` identical); zero team-run failures. |
| SC-008 | `pass` | T066 | `goal.md` sha256 byte-identical across a summary refresh — the derived flow never writes the definition. |
| SC-009 | `pass` | T064 | `.specify/project/goal/` does not exist; exactly one goal-indexed directory (`.specify/goal/`); zero goal artifacts under `.specify/project/`. |
| SC-010 | `pass` | T067 | All three team-domain guidance files link to `goal-definitions.md`; zero second-account statements placing a goal inside team files. |
| SC-011 | `pass` | T064, T071 | Live-face `project/goal` residual = 0 (24 source files migrated); 25 historical files preserved unchanged; 036 suite green, zero new failures. |
| SC-012 | `pass` | T068 | Exactly one surface writes `.specify/goal/**` definitions (`goal-utils.py`); `sync-mirrors --check` exit 0 (no command-surface drift). |
| SC-013 | `pass` | T069 | Eight-dimension conformance against `goal-definitions.md`: 0 conflicts (composition, lifecycle, plane relation, criteria authority, singularity, object scope, narrative shape, verification mode). |
| SC-014 | `pass` | T070 | Zero verbatim criteria duplication between goals and any `requirements.md`; zero `requirements.md` carrying a goal field; zero goal definitions enumerating FRs. |
| SC-015 | `pass` | T044 | Roster lists every team sharing the goal (complete vs a filesystem scan); zero writes to `goal.md`; exactly one detection trigger (rides the refresh). |
| SC-016 | `partial` | T045 | Mechanically verified: write-write overlap detected and named to paths; a contested area is enumerated (never left silently multi-writable); read-only intersection is not flagged. **Deferred half**: "write intersection = 0 *after ratification*" needs a live human-ratified `coordinate` round writing back to `team.md` (the write-back is prose-orchestrated, not automated). See `deferred_tasks`. |
| SC-017 | `pass` | T045 | Zero `team.md` writes during the proposal/detection stage (sha256 unchanged); the mechanism has no self-rewrite path — a re-division is only written on human ratification. |
| SC-018 | `pass` | T042, T043 | Undeclared team → `undecidable`, never `no-overlap` (the two are distinct verdicts); brace/glob/relative forms normalized before compare, so no notation-driven missed overlap. |

**Tally**: 17 pass, 1 partial (SC-016), 0 fail.

## Deferred

`deferred_tasks=` (none as `[~]` task rows — all 72 tasks are `[X]`).

**SC-016 partial** is a *criterion*-level deferral, not a task deferral: the "write intersection reaches 0 after ratification" clause requires a live, human-in-the-loop `/speckit.goal coordinate` run where the user ratifies a proposed re-division and the agreed scopes are written back to each `team.md`. Every mechanically checkable part (detection, naming, contested-area enumeration, read-overlap tolerance, zero writes during the proposal stage) is verified and green. The gap is the same class as 036's SC-006/T049 — a decision-gated live run that cannot be exercised autonomously.

## Constitution re-check (post-implementation)

12 Pass / 1 Partial, unchanged from the plan. Principle IX (Framework Scope Discipline) stays Partial with its two justified causes (new command surface + the first executable territory validator); both landed as deterministic file/text processing, and the coordination round remained proposal-only with human ratification — no scheduler, no runtime platform.

## Notes

- The one baseline failure that resolved during this requirement (`test_review_prerequisite_flags_are_supported`) is a branch-state artifact: it asserts `tasks.md` is in `AVAILABLE_DOCS`, which became true once `/speckit.tasks` produced the file. The baseline was reconciled to 39 names at T001 before any edit.
- Two implementation defects were caught by **execution** rather than review and fixed in-flight: the `goal-utils` CLI rejected `--json` after a subcommand (shared parent parser), and the overlap verdict initially read an empty-but-present territory as "declared" (narrowed so no comparable write scope → `undecidable`). Both are covered by tests now.
