---

description: "Task list for Feature 028 — Framework Feedback Mechanism"
---

# Tasks: Framework Feedback Mechanism

**Requirement ID**: 027
**Requirement Key**: 027-feedback-mechanism
**Related Feature**: 028 Feedback Mechanism (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/027-feedback-mechanism/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/, quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is MUST/Test-First: contracts define the engine CLI, entry schema, convention, and command classification, so contract + integration + unit tests are authored BEFORE implementation)

**Tests**: Test rows below are MANDATORY and MUST be written first (Red) and fail before the matching implementation tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- DoD-1: `feedback-utils.py` engine implemented (stdlib-only) per `contracts/feedback-utils-cli.md`, mirrored byte-identical to `.specify/scripts/python/`.
- DoD-2: All automated tests pass — unit (`tests/unit/`), contract (`tests/contract/`), integration (`tests/integration/`).
- DoD-3: Every `skills/*/SKILL.md` (and its `.specify/skills/` mirror) plus `templates/skills-template.md` carry a `## Feedback` section (`grep -L "## Feedback" skills/*/SKILL.md` returns nothing).
- DoD-4: All 13 complex command templates carry the feedback step at their wrap-up stage; all 4 simple command templates (`agents`, `constitution`, `feature`, `team`) do NOT.
- DoD-5: Selective triggering, per-run dedup, partial-run labeling, and the single consolidated threshold prompt are demonstrated by passing integration tests.
- DoD-6: Changes validated against Success Criteria SC-001…SC-007 in requirements.md; `.specify/memory/features/028.md` and `features.md` updated.

**DoD Status**: green   <!-- flip to `green` only when every DoD-N row above is satisfied -->

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

### Task State Sigil (REQUIRED)

- `- [ ]` — **Open**. Not yet complete.
- `- [X]` — **Closed**. Fully executed and verified.
- `- [~]` — **Deferred**. Intentionally handed off; record reason in `verification.md`.

## Path Conventions

Single project / code-generator shape (per plan.md). Engine source lives at `scripts/python/` and is mirrored to `.specify/scripts/python/`. Authoring surfaces: `templates/`, `skills/` (mirrored to `.specify/skills/`). Tests under `tests/unit/`, `tests/contract/`, `tests/integration/`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Test scaffolding and store readiness

- [X] T001 [P] Add an isolated-feedback-store pytest fixture (temp workspace containing `.specify/memory/feedback/`) in tests/conftest.py for engine and integration tests
- [X] T002 [P] Confirm the runtime feedback store scaffolding `.specify/memory/feedback/.gitkeep` exists (create if missing) so the store dir is version-tracked

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the shared `feedback-utils.py` engine and the canonical `## Feedback` step text that every skill and complex command embeds. Both US1 and US2 depend on this phase.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

### Tests for Foundational (MANDATORY — write first, ensure they FAIL) ⚠️

- [X] T003 [P] Unit tests for engine pure helpers (unit_id regex validation, `<created-ts>-<unit-slug>` derivation, UTC timestamp formatting, `count_since_submission` computation, `should_prompt` = count >= threshold) in tests/unit/test_feedback_utils.py (mirror the style of tests/unit/test_memory_utils.py)
- [X] T004 [P] Contract test for the engine CLI (actions `record`/`status`/`list`/`mark-submitted`/`reindex`; exit code 2 on bad `--unit-id`, empty `--review`, empty `--points`; JSON output shapes; duplicate `(unit_id,run_id)` returns `duplicate:true` without incrementing count) in tests/contract/test_feedback_utils_cli.py per contracts/feedback-utils-cli.md
- [X] T005 [P] Contract test for the entry file + `index.json` schema (frontmatter fields; body has `## Review` + `## Optimization Points` with ≥1 bullet; `scope: local`; `<YYYYMMDDTHHMMSSZ>-<unit-slug>.md` naming; `entries` sorted `created` desc; `count_since_submission` invariant; `reindex` preserves `submitted_at`) in tests/contract/test_feedback_entry_schema.py per contracts/feedback-entry-schema.md

### Implementation for Foundational

- [X] T006 Implement the stdlib-only engine at scripts/python/feedback-utils.py — all five actions, `(unit_id, run_id)` dedup no-op, `--unit-id` regex `^(?:/speckit\.[a-z0-9._-]+|skill:[a-z0-9._-]+)$`, `--partial` flag, threshold default 10 with `--threshold` / `SPECKIT_FEEDBACK_THRESHOLD`, `reindex` preserving `submitted_at`, exit code 2 on validation errors (patterned on scripts/python/memory-utils.py)
- [X] T007 Mirror the engine byte-identically to .specify/scripts/python/feedback-utils.py (keep in sync with scripts/python/feedback-utils.py)
- [X] T008 Author the canonical `## Feedback` step text (qualification+completion gate, agent self-reflection with no user input, scope guard vs `/speckit.review`, stable-`run_id` dedup guard, `record` invocation, consolidated threshold-prompt behavior, abort/partial rule) as a single embeddable source at skills/sdd-workflow/references/feedback-step.md and mirror it to .specify/skills/sdd-workflow/references/feedback-step.md, derived from contracts/feedback-step-convention.md

**Checkpoint**: Engine + canonical step text ready — user stories can begin.

---

## Phase 3: User Story 1 - Skill self-feedback at end of execution (Priority: P1) 🎯 MVP

**Goal**: Every skill carries a `## Feedback` step by default; at the end of a substantial run a skill self-reflects against its declared purpose and records a local, skill-scoped Feedback Entry.

**Independent Test**: Run any single skill end-to-end and confirm it emits a `scope: local` entry that references the skill's declared purpose, reviews the just-completed run, and lists ≥1 optimization point (or the explicit no-op line).

### Tests for User Story 1 (MANDATORY — write first, ensure they FAIL) ⚠️

- [X] T009 [P] [US1] Conformance contract test in tests/contract/test_feedback_skill_conformance.py: every skills/*/SKILL.md contains a `## Feedback` section AND templates/skills-template.md contains it (i.e. `grep -L "## Feedback" skills/*/SKILL.md` yields nothing)
- [X] T010 [P] [US1] Integration test in tests/integration/test_feedback_skill_record.py: recording a skill feedback step writes a `scope: local`, `unit_type: skill` entry referencing the skill purpose with ≥1 optimization point (or the explicit no-op sentence)

### Implementation for User Story 1

- [X] T011 [US1] Add the canonical `## Feedback` section (from T008) as the final workflow section of templates/skills-template.md so newly authored skills inherit it by default
- [X] T012 [P] [US1] Add the `## Feedback` section to all 21 installed skills at skills/*/SKILL.md using the canonical step text
- [X] T013 [P] [US1] Mirror the `## Feedback` additions into the runtime tree at .specify/skills/*/SKILL.md (keep mirror consistent with skills/)
- [X] T014 [US1] Update skills/create-skills/SKILL.md (and its .specify/skills/ mirror) to VALIDATE that a newly authored skill includes a `## Feedback` section — a skill lacking it is non-conformant (FR-002, FR-010)
- [X] T015 [US1] Update skills/improve-skills/SKILL.md (and its .specify/skills/ mirror) to verify and repair a missing or malformed `## Feedback` section

**Checkpoint**: US1 is independently functional — any skill records a local feedback entry; conformance + integration tests green.

---

## Phase 4: User Story 2 - Complex-command self-feedback at end of execution (Priority: P2)

**Goal**: The 13 complex command templates emit a command-scoped Feedback Entry at their wrap-up / Git-commit-prompt stage; the 4 simple command templates emit none.

**Independent Test**: Run a complex command to its wrap-up stage and confirm it records a `unit_type: command` entry distinct from the global `/speckit.review` report; run a simple command and confirm no entry is written.

### Tests for User Story 2 (MANDATORY — write first, ensure they FAIL) ⚠️

- [X] T016 [P] [US2] Classification contract test in tests/contract/test_feedback_command_classification.py driven by contracts/command-classification.md: each of the 13 complex command templates contains the feedback step; each of the 4 simple templates (`agents`, `constitution`, `feature`, `team`) does NOT
- [X] T017 [P] [US2] Integration test in tests/integration/test_feedback_command_record.py: a complex command records a `unit_type: command`, `scope: local` entry at wrap-up while a simple command records zero entries

### Implementation for User Story 2

- [X] T018 [P] [US2] Embed the feedback step (from T008) at the wrap-up / Git-commit-prompt stage of the SDD-chain complex templates: templates/commands/requirements.md, clarify.md, plan.md, tasks.md, implement.md
- [X] T019 [P] [US2] Embed the feedback step at the wrap-up stage of the analysis/consistency complex templates: templates/commands/analyze.md, checklist.md, review.md (local self-review, kept distinct from its own global report), research.md
- [X] T020 [P] [US2] Embed the feedback step at the wrap-up stage of the tooling/registry complex templates: templates/commands/instructions.md, tools.md, skills.md, todo.md
- [X] T021 [US2] Confirm the simple command templates carry NO feedback step: templates/commands/agents.md, constitution.md, feature.md, team.md (explicit exclusion per FR-006/FR-007)

**Checkpoint**: US2 is independently functional — complex commands record, simple commands do not; classification + integration tests green.

---

## Phase 5: User Story 3 - Selective triggering to protect execution efficiency (Priority: P3)

**Goal**: Feedback attaches only to qualifying long-running flows (all skills; complex commands only), never duplicates per unit+run, labels partial runs, and raises exactly one consolidated submission prompt at threshold.

**Independent Test**: Run a mix of trivial and qualifying flows plus a nested command→skill invocation; confirm trivial/simple flows produce zero entries, each qualifying unit records at most one entry per run, and the consolidated prompt fires exactly once at threshold.

### Tests for User Story 3 (MANDATORY — write first, ensure they FAIL) ⚠️

- [X] T022 [P] [US3] Integration test in tests/integration/test_feedback_dedup.py: a second `record` for the same `(unit_id, run_id)` returns `duplicate:true` and leaves `count_since_submission` unchanged (FR-008, SC-005)
- [X] T023 [P] [US3] Integration test in tests/integration/test_feedback_selective_triggering.py: trivial/short flows and simple commands produce zero entries; a qualifying flow produces exactly one (FR-007, SC-002, SC-004)
- [X] T024 [P] [US3] Integration test in tests/integration/test_feedback_threshold.py: below threshold `should_prompt` is false and no prompt is surfaced; at/over threshold `should_prompt` is true; `mark-submitted` resets `count_since_submission` to 0 and stamps `submitted_at` (FR-011, SC-007)
- [X] T025 [P] [US3] Integration test in tests/integration/test_feedback_partial.py: an aborted/failed run either records nothing or records with `--partial` and a `**Partial run** —` labeled `## Review` (FR-009)

### Implementation for User Story 3

- [X] T026 [US3] Author docs/skills/feedback.md documenting the Feedback Trigger Policy (all skills; 13 complex commands only; trivial/simple excluded), the store layout, the threshold behavior, and its distinction from the global `/speckit.review` — the observable policy source for SC-002/SC-004/SC-006 audits
- [X] T027 [US3] Audit that the canonical step embedded across templates/skills-template.md, all skills/*/SKILL.md, and the 13 complex command templates consistently encodes the qualification+completion gate, stable-`run_id` dedup guard, scope guard, abort/partial rule, and consolidated threshold-prompt behavior; propagate any wording fix from T008 uniformly (and to .specify/ mirrors)

**Checkpoint**: All three user stories independently functional; efficiency, dedup, partial, and threshold guarantees demonstrated.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Feature bookkeeping, docs, and full-suite validation

- [X] T028 [P] Update .specify/memory/features/028.md with implementation notes/status and refresh the Feature 028 row (last-updated) in .specify/memory/features.md (Feature Integration)
- [X] T029 [P] Add the Feedback System to the Documentation Map (docs pointer to docs/skills/feedback.md) alongside the existing Memory System entry
- [X] T030 Run the full test suite (`pytest`, plus `pytest -m contract` and `pytest -m integration`) and confirm unit + contract + integration are green
- [X] T031 Run the quickstart.md conformance checks: `grep -L "## Feedback" skills/*/SKILL.md` (empty), `grep -c "## Feedback" templates/skills-template.md` (≥1), and confirm simple-command exclusion via the classification test

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately.
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories (engine + canonical step text are shared prerequisites).
- **User Stories (Phase 3–5)**: All depend on Foundational completion.
  - US1 (P1), US2 (P2), US3 (P3) are independent of one another and can proceed in parallel once Foundational is done.
  - US3's tests exercise engine behavior built in Foundational plus the convention embedded by US1/US2; run US3 tests after the surfaces they sample exist, or scope US3 tests to the engine directly for isolated verification.
- **Polish (Phase 6)**: Depends on all desired user stories being complete.

### Within Each User Story

- Tests MUST be written and FAIL before implementation.
- Engine before convention (Foundational before US1/US2 surfaces).
- Canonical step text (T008) is the single source; surfaces embed it rather than diverging.

### Parallel Opportunities

- Setup: T001, T002 in parallel.
- Foundational tests: T003, T004, T005 in parallel (different files); implementation T006 → T007 (mirror) sequential; T008 parallel with engine work.
- US1: T009, T010 in parallel; T012 and T013 in parallel (different trees).
- US2: T018, T019, T020 in parallel (disjoint template sets); T016, T017 in parallel.
- US3: T022, T023, T024, T025 in parallel (different test files).

---

## Parallel Example: User Story 2

```bash
# Author the feedback step across the three disjoint complex-template groups together:
Task: "Embed feedback step in SDD-chain templates (requirements, clarify, plan, tasks, implement)"
Task: "Embed feedback step in analysis templates (analyze, checklist, review, research)"
Task: "Embed feedback step in tooling templates (instructions, tools, skills, todo)"

# And run its tests together:
Task: "Classification contract test in tests/contract/test_feedback_command_classification.py"
Task: "Command record integration test in tests/integration/test_feedback_command_record.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational (engine + canonical step — CRITICAL, blocks all stories).
3. Complete Phase 3: User Story 1 (all skills self-feedback).
4. **STOP and VALIDATE**: run any skill, confirm a local entry is recorded; conformance test green.
5. Ship the MVP — the distributed feedback layer's backbone is live.

### Incremental Delivery

1. Setup + Foundational → engine + convention source ready.
2. US1 → every skill records feedback → validate → ship (MVP).
3. US2 → complex commands record, simple excluded → validate → ship.
4. US3 → selective-triggering, dedup, partial, and threshold guarantees → validate → ship.
5. Polish → feature bookkeeping, docs, full-suite green.

---

## Notes

- [P] tasks = different files, no dependencies.
- The engine is built once in Foundational (single file at scripts/python/ + mirror) to avoid cross-story same-file conflicts; US1/US2/US3 edit disjoint authoring/test surfaces.
- Both `skills/` and `.specify/skills/` are real mirror trees (not symlinks): edits must land in both; the same applies to `scripts/python/` ↔ `.specify/scripts/python/`.
- Commit at the wrap-up of each phase; stop at any checkpoint to validate a story independently.
- Prefer `[~]` (deferred, with a recorded reason) over leaving a task `[ ]` if a step is intentionally handed off.
