# Tasks Stage Record — 111-general-best-practices

**Date**: 2026-11-27
**Run**: `r20261127T071500Z-111a` · line `general-best-practices` · stage `tasks`
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/general-best-practices` (branch `111-general-best-practices`, base `0419adae5`, stage baseline `1638077e4`)

## Preconditions measured

- Setup: inputs present — requirements (9 FR / 7 SC / 7 STR / 21 assumptions), plan (23-row Constitution Check all pass; 5 Execution Premises all verified; `Dependency set: none`), data-model (11 entities / 12 invariants / 3 transitions), four contracts (24 clauses), quickstart (S-0…S-8), feature-ref. `check-prerequisites`-equivalent inputs were read directly; no setup script re-run (the stage is docs-only and produces no runtime artifact).
- Flow class: reused the once-per-stage reading recorded at plan stage (`flow_class: execution`); no re-read needed — the execution gate set stays unchanged.
- Workspace signature: compared against the plan-stage snapshot `test-evidence/workspace-plan.json` → `clean` (no branch/ref/spec-dir drift; every probe wrote only the sanctioned `.specify/.tmp/` scratch, cleaned after use).
- Containment at stage start: `git diff --name-only 0419adae5..HEAD` = 43 paths (34 spec paths + 3 session + 3 feedback + 3 exec-quant per-entry records), all inside FR-009's declared set.

## Artifacts produced

| Artifact | Path | Reading |
|----------|------|---------|
| Tasks | `tasks.md` | 19 tasks in six phases (Setup 3 / Foundational 1 / US1 4 / US2 2 / US3 5 / Polish 4); Tests Mode ON (doc-feature shape); 24 clauses partitioned T008/T010/T013/T015/T019; FR 9/9, SC 7/7 mapped; targeted + one full-suite slot; no `[~]` deferrals |
| Validator capture | `test-evidence/tasks-validator.txt` | `PASS — 0 error(s), 0 warning(s)` |
| Decomposition capture | `test-evidence/decomposition-tasks.json` / `.txt` | `decision=proceed`, `fr_count=9`, `task_count=19`, ceilings 120/160 |
| Pre-analyze capture | `test-evidence/tasks-pre-analyze.json` / `.txt` | `stage=tasks decision=pass errors=0 advisories=139 waived=0`, summary `fr=9 sc=7 tasks=19 clauses=24 files=12` |
| Accounting captures | `test-evidence/tasks-{run-determination,exec-quant,feedback-record}.txt` | see § Wrap-up accounting |

## Gates

1. **Structural validation** — `validate-tasks.py` on the written file: first pass produced 3 `green-path-divergence` WARNs (the heuristic read the guard path in the verification rows as a write target); resolved by expressing the true relationship — the verification rows run the guard read-only (the template's sanctioned "assign the file to a single phase and reference it read-only" pattern) and by replacing the `<capture path>` placeholder with concrete per-row evidence paths. Final: 0 errors / 0 warnings, rc 0.
2. **Decomposition** — `decomposition-check.py --mode tasks` → `proceed` (9 FR / 19 task rows, under both ceilings).
3. **Pre-analyze `--stage tasks`** — `decision=pass`, `errors=0`, `advisories=139` = 28 `external-clause` tokens (INV-01…INV-12 in data-model / plan / tasks Prerequisites — pre-existing shape from the plan stage) + 111 `missing-path` entries that name the not-yet-created deliverables (`shared/best-practices/**`, the mirror, the guard, the future feature detail).
4. **Workspace guard** — `--check` against `test-evidence/workspace-plan.json` → `clean`.
5. **Test entry** — `not-run-docs-only`: this stage adds Markdown artifacts only and the guard is not implemented yet; the implement stage runs the targeted guard through `scripts/bash/run-tests.sh` (SC-007). The init-drill feasibility probe ran rc 0 and wrote only inside the sanctioned `.specify/.tmp/` root (torn down).

## Corrections and deviations (disclosed)

- **In-passing correction (init-drill premise)**: quickstart S-7 premises that "`specify init` is installed from this checkout". Measured: the globally installed `specify` (`/home/agent/.local/bin/specify`, 0.0.22) reports `framework commit: fed513bcc… (embedded)` and ships its own packaged `shared/` under site-packages, so a drill with it can never see this working tree's module — the SC-004 evidence would be false. Exactly one reading is consistent with the recorded intent ("the drill exercises this checkout's init copy step"): the source-run form `PYTHONPATH=<worktree>/src /usr/local/bin/python3 -c 'import specify_cli; specify_cli.main()' …`, which reports `framework commit: 1638077e4… (git)`. Probe drill rc 0 (shared/ copied; `best-practices/` absent = the correct pre-implementation reading). T014 pins the source-run form; the trap is recorded in § Measured Premises and § Notes of `tasks.md`.
- **Task-row executability fix**: the first draft used a `<capture path>` placeholder inside `--names-out` command lines — a literal space-bearing placeholder would split at the shell. Replaced with concrete per-row evidence paths (`test-evidence/us1-names.txt` … `full-names.txt`); the runner parses `--names-out` anywhere in the line (verified against `scripts/bash/run-tests.sh`).
- **Feature Integration deferred (planned deviation)**: the tasks-phase Feature-list review was performed (no new feature exposed, none invalidated); registry edits stay forbidden by the stage brief and FR-009 names the feature-registration stage as the sole exception. Glossary stays untouched (A-21).
- **Test entry not run**: docs-only stage; see gate 5.
- **Commit ordering**: the stage brief requires the final action to commit all produced artifacts, so the single stage commit includes this record, the checkpoint and the three per-entry accounting records.

## Wrap-up accounting

| Step | Command identity | Record |
|------|------------------|--------|
| Run Determination | `/speckit.tasks` | `.specify/session/20261127T075541Z-run-determination-speckit-tasks-r20261127t071500z-111a.md` (axes `not_evaluated` with source-unavailable reasons; complexity `complex`, qualification `qualified`, feature `111-general-best-practices`) |
| Exec Quant | `/speckit.tasks` | `.specify/exec-quant/records/20261127T075547662238Z-61e5bf4a.json` |
| Feedback Record | `/speckit.tasks` | `.specify/feedback/20261127T075556Z-speckit-tasks.md` (feature key carried; local scope) |

Captures: `test-evidence/tasks-run-determination.txt`, `tasks-exec-quant.txt`, `tasks-feedback-record.txt`.

## Concurrency

- `requested=1`, `effective=not_evaluated`, `effective_reason=single-unit` — the stage is one bounded tasks unit; the interval/parallel carrier reading is not applicable.

## Anomaly line

`未发现异常` — no ANOMALY-class state occurred; the one premise correction above is disclosed as an in-passing correction, not surfaced as an anomaly.