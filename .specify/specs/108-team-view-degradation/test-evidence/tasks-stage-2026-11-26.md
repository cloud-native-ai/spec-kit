# Tasks Stage Evidence — 2026-11-26

Line `team-view-degradation`; run `r20261126T071500Z-108a`; stage `tasks`; attempt 1; stage base commit `679301b65`; branch `108-team-view-degradation` (worktree). Terminal authority: requirements.md + clarifications, plan set + 4 contracts, constitution v1.20.0, `.specify/instructions.md`, and the stage brief `.specify/.tmp/sdd-loop/tmp/team-view-degradation/brief-tasks.md`.

## Setup

- `bash .specify/scripts/bash/check-prerequisites.sh --json` → exit 0; `REQUIREMENTS_DIR` = the spec dir; `AVAILABLE_DOCS` = research.md / data-model.md / contracts/ / quickstart.md / checklists/ / feature-ref.md; `MODE=B`; `WRITABLE=true`.
- `flow-class-check.py --action lookup --unit-id "spec:108-team-view-degradation"` → `flow_class: execution`, `source: declaration`, exit 0. No expression-class gates are added; the stage gate set is the existing one.
- Workflow loaded through `speckit.tasks` → `create-tasks`; structure template `.specify/templates/tasks-template.md`; structural validator `.specify/scripts/python/validate-tasks.py`.

## Generation

- `tasks.md` written at `.specify/specs/108-team-view-degradation/tasks.md`: 29 task rows (T001–T029), organized Setup → US1 (P1) → US2 (P1) → US3 (P2) → Polish. No Foundational phase: no blocking prerequisite exists outside Setup (the three new test files carry their own local helpers; the existing `tests/fixtures/team_view_fixtures.py` already writes arbitrary `runs/` names and missing artifacts; the only shared implementation surface is the single engine, landed sequentially inside US1/US2).
- Tests Mode **ON** (Constitution Principle IV "Test-First & Contract-Driven Implementation"). Red-first evidence lands at `notes/red-first-evidence.md`; raw red outputs land at the per-row `test-evidence/*-red-*.txt` sinks; the failing-name baseline path/flag is referenced to the `/speckit.implement` § Test runs owner, never restated.
- Coverage: § Requirement Coverage Map 25/25 FR and 8/8 SC; § Clause Coverage & Green Partition claims all 35 contract clauses exactly once (report-recognition C-201…C-207 → T012, C-208 → T018; presentation C-301…C-309 → T018; team-view-program C-101…C-109 → T025; view-labels C-401…C-409 → T025), monotonic per contract.
- Parallel markers: T006/T007 (US1) and T019/T020 (US3) only; every other row shares the engine, the integration test file or a notes sink and stays serial by row order.
- Regression-guard exception declared inline on T020 (healthy byte-fidelity + read-only snapshot): their green is meaningful only after the engine amendment, so they follow implementation; all other new-behavior tests precede their implementation rows.
- Plan constraint respected: no plan-owned path edited. `PLAN-EDIT: none`.

## Deterministic gates (verbatim outputs)

- `python3 .specify/scripts/python/validate-tasks.py .specify/specs/108-team-view-degradation/tasks.md` → `PASS: … — 0 error(s), 0 warning(s)`, rc 0 (`test-evidence/tasks-validator.txt`).
- `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/108-team-view-degradation --stage tasks --repo .` → `pre-analyze-check: stage=tasks decision=pass errors=0 advisories=66 waived=0`; summary `fr=25 sc=8 tasks=29 clauses=35 files=12` (`pre-analyze-tasks.txt` / `.json`).
- `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements …/requirements.md --tasks …/tasks.md` → `decision=proceed`, `fr_count=25`, `task_count=29`, ceilings `120 / 160`, rc 0 (`decomposition-tasks.json`).
- `python3 scripts/python/sync-mirrors.py --check` → rc 0, all six mirror families byte-identical; `python3 scripts/python/regen-command-copies.py --check` → rc 0 (`OK: all per-tool command copies match the source templates.`). No executable surface changed in this stage.
- `python3 scripts/python/account-clause-coverage.py --spec-dir …` read-only probe → the accountant resolves and reports the corpus census; freezing is a T002 implement-stage duty (`coverage-baseline.txt` does not exist yet, as measured).

## Advisory adjudication (pre-analyze tasks)

- **36 `external-clause`** — all from `data-model.md` lines 130–165: the `INV-01…INV-10` invariant ids match the legacy clause-id shape `[A-Z]{2,4}-\d{2}`. This is the same known noise the plan stage recorded (36 at plan time; 103's plan recorded the same class). Plan-owned file; not edited. Adjudicated: **benign, pre-existing, framework-improvement candidate** (already a feedback point at plan time).
- **30 `missing-path`** — the three new test files (17 mentions in `tasks.md`, plus quickstart/feature-ref/contract headers), their planned presence being the red-first premise; 1 `.specify/state/u4-...-plan.txt` referenced by the plan-set feature-ref (an out-of-worktree driver path). Adjudicated: **expected** — every missing path is either a surface this feature creates during implement or a driver-owned path outside the worktree.

## Test budget (E3 stage-status row, reduced field set — docs-only stage)

| Field | Value |
|-------|-------|
| stage | `tasks` |
| row_type | `stage-status` |
| status | `not-run-docs-only` |
| selection_basis | this stage changed only Markdown artifacts (tasks.md + evidence); no executable surface changed, so a targeted test selection would be empty — `not-run-docs-only` is the honest reading, never `unknown` |
| changed_paths | `.specify/specs/108-team-view-degradation/tasks.md`, `.specify/specs/108-team-view-degradation/test-evidence/*` (this stage) |
| evidence_ptr | this file; `tasks-validator.txt`; `pre-analyze-tasks.json`; `decomposition-tasks.json` |

## Concurrency

`requested=1`, `effective=not_evaluated`, `effective_reason=single-unit` — one bounded assignment; task-list generation is one indivisible authoring unit with no file-disjoint work package worth a second carrier.

## Workspace guard

- **Before side**: the driver's post-plan signature `.specify/specs/108-team-view-degradation/test-evidence/workspace-plan-poststage-driver.json` (the plan stage's own before/after pair was invalid; the driver took this snapshot at plan close).
- **Check**: `workspace-guard.py --check … --repo .` → `{"status": "clean", "changed": []}`, rc 0 (`workspace-tasks-check-vs-plan.json`). Same branch, same refs, same `.specify/specs` listing (including `108-team-view-degradation`).
- **After side**: `workspace-guard.py --snapshot test-evidence/workspace-tasks.json` then `--check` → `{"status": "clean", "changed": []}`, rc 0 (`workspace-tasks-readings.txt`). No branch created, no spec directory added beyond this feature's own.
- `git status` at stage start: clean (measured before authoring); after authoring only this feature's new artifacts are untracked.

## Feature Integration

- Reviewed `.specify/features.md` and `.specify/features/027-team-management.md` read-only: slice row `108` is `Planned`, parent 027 stays `Ready for Review`; the breakdown exposes no new Feature and invalidates none. Per the stage brief, no registry edit is made; the implement / driver close-out owns any status advance.

## Re-anchoring record

- T0 at setup and before wrap-up: rules reloaded (unattended; no user questions; no push; no spine/registry edits; plan constraint; single engine; closed sets; healthy byte-fidelity; targeted test budget; one-line task rows). Direction questions answered; verdict each time: `on-track`.

## In-passing corrections (disclosed, no claim changed)

1. A malformed DoD row prefix (`DoF-7（笔误更正为 DoD-7）`) was corrected to `DoD-7:` before the validator's first run.
2. The Prerequisites line cited `INV-01…INV-10`, which the pre-analyze gate reads as two external-namespace clause references; reworded to "C1–C10 实体与 10 条不变式" (claims unchanged), reducing the stage's own advisory count by 2.
3. T020's read-only baseline-blob citation was annotated `（只读）` after the structural validator classified it as a write target (a heuristic false positive: the row writes only the integration test file). The parallel-safe warning was cleared without deleting the cited path; the actual write targets were disjoint all along.

## Anomalies

- 未发现异常。No decision-class anomaly occurred; the three in-passing corrections above are local, reversible and claim-preserving. No user question was asked; nothing was pushed; the state spine, `.specify/register.md`, plan-owned paths and all dated records (including the 103 spec artifacts) were left untouched.
