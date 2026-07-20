# Quickstart: Task Complexity Rubric

**Feature**: 032 Task Complexity Rubric · **Spec**: `031-task-complexity-rubric` · **Date**: 2026-07-20

How to see the rubric appear and how to verify the change.

## See it in a fresh project

1. In a clean workspace with no `.specify/instructions.md`, run the instructions generation flow (`/speckit.instructions`, which invokes `scripts/bash/generate-instructions.sh`).
2. Open the generated `.specify/instructions.md`.
3. Confirm it contains a `## Task Complexity Rubric` section with the tier table, signal list, tie-break rule, default tier, and efficiency-vs-quality statement.

## See it added to an existing project

1. Start from a project whose `.specify/instructions.md` predates this feature (no rubric section).
2. Run `/speckit.instructions`.
3. Confirm the rubric section was inserted after "Fact, Correctness & Logic Checks (Input Sanity)" and that every other section is unchanged.
4. If you had already customized your own rubric, confirm your version was preserved (not overwritten).

## Dogfood in this repository

Run `/speckit.instructions` in spec-kit itself to insert the rubric into this project's own `.specify/instructions.md` (surfaced through the `AGENTS.md` / `QODER.md` symlinks). This is an application of the feature, performed after the template edit lands.

## Verify the change

- Run the rubric test module (added in Phase 2), e.g. `pytest tests/contract/test_task_complexity_rubric.py -q`.
- The test asserts contract checks C-1…C-10 from `contracts/rubric-section.md`: the stable heading, four tiers, five signals, per-tier depth, tie-break rule, default tier, tradeoff statement, project-neutrality, and `templates/` ↔ `.specify/templates/` mirror parity.

## Expected agent behavior once adopted

- A one-line edit to an isolated file → **Trivial** → act directly, minimal ceremony.
- A normal bug fix in one module → **Standard** → read relevant files, run related tests.
- A cross-module refactor with design choices → **Complex** → explore, plan explicitly, verify.
- A data migration / security / public-API change, or an unclear request → **High-stakes / Ambiguous** → exhaustive care, user checkpoints, clarify first.
