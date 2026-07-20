---
description: "Task list for Task Complexity Rubric in Generated Instructions"
---

# Tasks: Task Complexity Rubric in Generated Instructions

**Requirement ID**: 031
**Requirement Key**: 031-task-complexity-rubric
**Related Feature**: 032 Task Complexity Rubric (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/031-task-complexity-rubric/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), data-model.md, contracts/rubric-section.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates contract/test-first coverage. This is a template-only feature, so "tests" are Layer-1 **structural assertions** on the rendered template content — per plan.md, Principle IV is a justified Partial; no runtime unit exists to drive.)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- DoD-1: The `## Task Complexity Rubric` section is present in BOTH `templates/instructions-template.md` and `.specify/templates/instructions-template.md`, byte-identical for that section (contract C-10).
- DoD-2: `tests/contract/test_task_complexity_rubric.py` passes all contract checks C-1…C-10.
- DoD-3: Fresh generation includes the rubric (SC-001); existing-doc refresh is verified additive and user-preserving (SC-002, FR-010, FR-011).
- DoD-4: Full `pytest` suite shows no new failures versus the Phase 1 baseline (Constitution Principle VI).
- DoD-5: Rubric content is project-neutral — no spec-kit-specific identifiers or paths (FR-008, contract C-9).
- DoD-6: Feature 032 status and notes are consistent across `.specify/memory/features.md` and `.specify/memory/features/032.md`.

**DoD Status**: green

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3); Setup/Foundational/Polish tasks carry no story label
- Include exact file paths in descriptions

### Task State Sigil (REQUIRED)

- `- [ ]` — **Open**. Not yet complete. A run is NOT complete while any `[ ]` remains.
- `- [X]` — **Closed**. Fully executed and verified.
- `- [~]` — **Deferred**. Intentionally handed off; reason recorded in `verification.md` under `deferred_tasks=` plus a `<!-- deferred: <reason> -->` inline comment.

## Path Conventions

This is a documentation/prompt-framework change (no runtime source tree). Relevant paths:

- Template source of truth: `templates/instructions-template.md`
- Mirror (must match source): `.specify/templates/instructions-template.md`
- Structural contract test: `tests/contract/test_task_complexity_rubric.py`
- Generation script (render path): `scripts/bash/generate-instructions.sh`

---

## Phase 1: Setup

**Purpose**: Baseline and edit-site confirmation

- [X] T001 Establish the test baseline: run `pytest -q` from the repo root and record the current pass/fail counts as the regression baseline (a batch of pre-existing, change-unrelated failures is expected — capture it to distinguish regressions later).
- [X] T002 [P] Confirm both mirror targets exist and fix the insertion anchor: the new section goes **after** `## Fact, Correctness & Logic Checks (Input Sanity)` and **before** `## Tech Stack & Resources` in `templates/instructions-template.md` and `.specify/templates/instructions-template.md`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Author the failing structural test that every user story is verified against (TDD Red step)

**⚠️ CRITICAL**: Must complete before user-story implementation begins

- [X] T003 Author the failing structural contract test `tests/contract/test_task_complexity_rubric.py` asserting contract checks C-1…C-10 from `contracts/rubric-section.md` against BOTH template files: stable heading `## Task Complexity Rubric` (STR-001); exactly four tiers labeled `Trivial`, `Standard`, `Complex`, `High-stakes / Ambiguous`; the five signal dimensions (scope/size, uncertainty/novelty, blast radius/reversibility, cross-cutting impact, requirements clarity); a per-tier thinking-depth behavior referencing exploration/planning/verification; the tie-break rule (higher tier on conflict); the default tier + clarify-on-ambiguity; the efficiency-vs-quality statement; project-neutrality (no `spec-kit`/`specify`/feature-id/repo-path strings); and `templates/` ↔ `.specify/templates/` mirror parity for the section. Run it and confirm it FAILS (Red) — the section does not exist yet.

**Checkpoint**: A red structural test pins the acceptance surface.

---

## Phase 3: User Story 1 - Agent calibrates thinking depth from the rubric (Priority: P1) 🎯 MVP

**Goal**: A well-formed, agent-usable rubric exists in the instructions template so an agent can classify a task and adopt the prescribed thinking depth.

**Independent Test**: Structural test C-1…C-10 turns green, and a reviewer can classify the `quickstart.md` sample tasks consistently with the rubric.

### Implementation for User Story 1

- [X] T004 [US1] Insert the `## Task Complexity Rubric` section into `templates/instructions-template.md` at the confirmed anchor, authored verbatim from `data-model.md`: the five signal dimensions, the four-tier table (per-tier signals + thinking-depth behavior), the tie-break rule, the default-tier rule, and the efficiency-vs-quality statement. Keep content project-neutral.
- [X] T005 [US1] Dual-write the identical section into `.specify/templates/instructions-template.md` so the `## Task Complexity Rubric` section is byte-identical to `templates/instructions-template.md` (depends on T004; verify with `diff`).
- [X] T006 [US1] Run `pytest tests/contract/test_task_complexity_rubric.py -q` and confirm C-1…C-10 now PASS (Green) (depends on T004, T005).
- [X] T007 [US1] Manual QA: using the sample tasks in `quickstart.md`, classify the four examples and confirm each maps to the intended tier and prescribed depth (rubric is unambiguous enough to apply).

**Checkpoint**: Rubric content present, mirror-consistent, and structurally verified — MVP delivered.

---

## Phase 4: User Story 2 - Fresh project instructions include the rubric (Priority: P2)

**Goal**: A freshly generated `.specify/instructions.md` contains the rubric section.

**Independent Test**: Generate in a clean workspace → the `## Task Complexity Rubric` heading is present.

### Verification for User Story 2

- [X] T008 [US2] In a temporary clean workspace with no `.specify/instructions.md`, run the fresh-generation path (`scripts/bash/generate-instructions.sh`) and assert the generated `.specify/instructions.md` contains the `## Task Complexity Rubric` heading (SC-001, FR-009). Record the result.

**Checkpoint**: Fresh generation confirmed to include the rubric.

---

## Phase 5: User Story 3 - Existing instructions gain the rubric non-destructively (Priority: P3)

**Goal**: The `/speckit.instructions` refresh inserts the rubric into an existing document without disturbing other content, and never overwrites a user-customized rubric.

**Independent Test**: Before/after diff on a fixture doc shows an additive-only insertion; a user-customized rubric survives the refresh.

### Verification for User Story 3

- [X] T009 [P] [US3] Additive-insert check: create a fixture instructions doc lacking the rubric, run the `/speckit.instructions` refresh (its "add missing scaffolding" step), and diff before/after to confirm the rubric is inserted and every other section is byte-for-byte unchanged (SC-002, FR-010).
- [X] T010 [P] [US3] User-precedence check: with a fixture instructions doc that already contains a user-customized `## Task Complexity Rubric`, run the refresh and confirm the user's version is preserved, not overwritten (FR-011).

**Checkpoint**: Non-destructive refresh behavior verified for both new-insert and user-customized cases.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Regression safety, success-criteria recording, and optional dogfooding

- [X] T011 [P] Run the full `pytest -q` suite and confirm zero new failures versus the T001 baseline (Constitution Principle VI).
- [X] T012 Record success-criteria status in `verification.md` (created by `/speckit.implement`): SC-001, SC-002, SC-005 with pass evidence; mark SC-003 and SC-004 (reviewer/LLM-benchmark agreement) as deferred post-adoption metrics with a recorded reason.
- [~] T013 [P] Dogfood (deferrable): run `/speckit.instructions` in this repository to insert the rubric into spec-kit's own `.specify/instructions.md` (written through the `AGENTS.md`/`QODER.md` symlinks); confirm the change is additive and the symlinks stay intact. If not executed this session, mark `[~]` with a recorded reason. <!-- deferred: live-repo instructions refresh is best performed via an interactive /speckit.instructions run so the full section-by-section refresh + symlink checks apply -->

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately.
- **Foundational (Phase 2)**: Depends on Setup — the red test BLOCKS user-story implementation.
- **User Stories (Phase 3+)**: All depend on Foundational (the failing test). US1 delivers the shared implementation (the template section); US2 and US3 are verifications that depend on US1's edit being in place.
- **Polish (Phase 6)**: Depends on the desired user stories being complete.

### User Story Dependencies

- **US1 (P1)**: Depends only on Phase 2. Delivers the rubric content (the MVP).
- **US2 (P2)**: Depends on US1 (fresh generation renders the template section authored in US1). Independently testable via a clean-workspace generation.
- **US3 (P3)**: Depends on US1 (refresh inserts the same template section). Independently testable via fixture-doc diffs; requires no code change beyond US1 (the command's existing refresh logic handles insertion and user precedence).

### Within Each User Story

- Foundational test (T003) is written and FAILS before US1 implementation (T004–T005).
- Source template (T004) before mirror (T005); both before the green test run (T006).

### Parallel Opportunities

- T002 can run alongside T001.
- T009 and T010 (US3 fixtures) are independent and can run in parallel.
- T011 and T013 (Polish) are independent of each other.

---

## Parallel Example: User Story 3

```bash
# US3 verification fixtures are independent — run together:
Task: "Additive-insert diff check on a rubric-less fixture instructions doc (T009)"
Task: "User-precedence check on a fixture with a customized rubric (T010)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 (baseline + anchor).
2. Complete Phase 2 (failing structural test).
3. Complete Phase 3 (author + mirror the rubric section; test turns green).
4. **STOP and VALIDATE**: rubric is present, mirror-consistent, and structurally verified — this is the shippable MVP.

### Incremental Delivery

1. Setup + Foundational → red test ready.
2. US1 → rubric content in both templates, test green → MVP.
3. US2 → confirm fresh generation includes it.
4. US3 → confirm non-destructive refresh (new-insert + user-customized).
5. Polish → full-suite regression check, record SC status, optional dogfood.

---

## Notes

- [P] tasks = different files, no dependencies.
- This feature intentionally makes **no** change to `templates/commands/instructions.md` or its per-tool runtime copies — FR-009/FR-010/FR-011 are delivered by the command's existing generic "add missing scaffolding" + conflict policy (see plan.md Phase 0).
- Mirror discipline: after editing the section, verify byte-identical parity between `templates/instructions-template.md` and `.specify/templates/instructions-template.md`.
- `cp` may be aliased to `cp -i`; use `\cp`/`cp -f` if copying between mirrors.
- Prefer `[~]` over leaving a task `[ ]` when deliberately handing it off (e.g., T013 dogfood if generation cannot be run this session).
