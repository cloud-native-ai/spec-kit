# Tasks-stage evidence — 095-superagent-role

Run: `r20261110T065604Z-b095` · Stage: tasks · Template: `.qoder/commands/speckit.tasks.md` · Skill: `create-tasks` · HEAD before this stage: `2c8da54c0`.

## Inputs

- `.specify/specs/095-superagent-role/requirements.md` (38 FR / 10 SC / 10 clarify rulings)
- `plan.md` + `data-model.md` + `contracts/` ×4 + `quickstart.md` + `feature-ref.md`
- Prerequisites run: `bash .specify/scripts/bash/check-prerequisites.sh --json` → `REQUIREMENTS_DIR=.specify/specs/095-superagent-role`, `AVAILABLE_DOCS=[data-model.md, contracts/, quickstart.md, checklists/, feature-ref.md]`, exit 0

## Gate readings

| Gate | Reading |
|---|---|
| Flow-class lookup (once, reused) | `flow_class: execution` / `source: declaration` / exit 0 — `test-evidence/tasks-flow-class.txt` |
| Tests Mode decision | **ON** — constitution grep (`grep -nE 'MUST\|MANDATORY\|NON-NEGOTIABLE\|Test-First\|TDD\|Contract-Driven'`) hits Principle IV (lines 179–184: unit tests / regression coverage / integration-contract tests all MUST) and Principle VII's template-only clause (line 225: template-only features judge Test-First via structural content/path/structure tests). Banner printed in `tasks.md`. |
| Structural validator | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/095-superagent-role/tasks.md` → `PASS: 0 error(s), 0 warning(s)`, exit 0 — `test-evidence/tasks-validate.txt` |
| Green claims | 9 claims, ascending per contract, one row per test module: role-edge-engine C-1/C-11 (T011); role-transition-payload C-2/C-13 (T020); status-digest-role-view C-1/C-7 (T034); harness-landing C-1 (T040), C-3/C-5 (T041). No collision / cross-phase / path-divergence WARN. |
| Premise re-measurement | Recorded with real outputs in `notes/pre-change-measurements.md` (budget 37,454 / 32,975 / 38,400 B; mirror DIFF-class 428 of 437 lines; 14 slices 080–094 with 092 absent; Per-Agent Payload 7 rows; template anchors 266/272) |
| Coverage baseline | Frozen `coverage-baseline.txt` (642 lines, `base-sha: 2c8da54c06e7`) |

## Deliverable shape

- **54 task rows** in 8 phases: Setup 3, Foundational 7, US1 8, US2 10, US3 5, US4 6, US5 6, Polish & Close-out 9.
- **22 `[P]` rows**; **38 `[blockedBy:]`** tags; every row names exact file paths and traces FR/SC.
- **Work Packages** map to plan P1–P6: P1 (7), P2 (13, includes the three forms), P3 (10), P4 (6), P5 (6), P6 (9) — every package ≤16 rows.
- **MVP** = US1 + US2 + US3 (the three P1 stories only together form an independently valuable increment).
- **Test budget registered**: implement start = one full baseline via the runner + per-story red-first targeted runs; closure = full suite after the review round (T001, T051).
- **Environment Prerequisites**: CPython available (3.11.11, lower bound `>=3.8`), runner present, no external environment (no docker / cluster / SSH host / third-party dependency).

## Feature-list review (mandatory at tasks phase)

- Feature 095 exists in `.specify/features.md` with status `Planned`; per `.specify/shared/workflow/feature-integration.md` the tasks phase **maintains `Planned`** — no status change, no new Feature, no invalidated Feature. Detail file `.specify/features/095-superagent-role.md` already carries the plan notes; task breakdown exposed no new feature. **No registry edit made.**

## Concurrency reading (this run)

- `requested` = 1 (the stage's representable unit is the single `tasks.md` authoring unit; probes are sub-steps)
- `effective` = `not_evaluated` (no per-unit dispatched_at / settled_at interval record — no subagent dispatch was used)
- `effective_reason` = `single-unit` (the representable unit set has size 1; nothing to run concurrently)

## Anomalies & in-passing repairs

- No unresolved anomaly. In-passing repairs during authoring: (1) validator WARN `parallel-safe` caused by the literal token `0/1/2` in two fixture rows (false path) → rephrased to prose; (2) WARN `green-clause-collision` (T011 and T015 both claimed C-11) → T015's claim removed, partition re-cut. Final validator: 0 error / 0 warning.
- Disclosed conflict inherited from the plan brief: “`better-harness.md` 增加指针” vs clarify Q6 ruling “不改” → the requirements ruling wins; already disclosed in plan D-1 and recorded in `notes/pre-change-measurements.md` §11.

## Output

`.specify/specs/095-superagent-role/tasks.md` — dependency-ordered, immediately executable, validator-clean.
