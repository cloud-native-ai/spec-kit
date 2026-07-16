---
description: "Task list for Glossary Mechanism (spec 029, Feature 031)"
---

# Tasks: Project Glossary Mechanism (项目词汇表机制)

**Requirement ID**: 029
**Requirement Key**: 029-glossary-mechanism
**Related Feature**: 031 Glossary Mechanism (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/029-glossary-mechanism/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/, quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is a MUST/Red-Green-Refactor principle; Principle VII's "template-only features" clause applies to the template/prompt artifacts — their "tests" verify template content, canonical paths, structure, and non-destructive re-init, while the `glossary-utils.py` engine follows classic unit TDD).

**Organization**: Tasks are grouped by the 4 user stories from requirements.md to enable independent implementation and testing.

## Definition of Done (DoD)

- DoD-1: Code/templates/docs implemented per spec (FR-001…FR-015) and contracts/.
- DoD-2: All automated tests pass — `glossary-utils.py` unit tests + `test_glossary_mechanism.py` contract tests (structure/wiring/non-destructive).
- DoD-3: Manual verification completed via quickstart.md steps 1–4.
- DoD-4: All mirror pairs byte-identical (`templates/` ↔ `.specify/templates/`, `shared/workflow/` ↔ `.specify/shared/workflow/`, per-tool command copies) and docs updated.
- DoD-5: No new runtime dependencies; Principle IX (doc/prompt framework) upheld.
- DoD-6: Validated against Success Criteria SC-001…SC-006; no regression vs the recorded pytest baseline.

**DoD Status**: pending

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: US1–US4 for user-story phases only

## Path Conventions

Framework repo (code generator). New/changed paths: `templates/`, `.specify/templates/`, `shared/workflow/`, `.specify/shared/workflow/`, `scripts/python/`, `scripts/bash/`, `templates/commands/` (+ per-tool runtime copies), `tests/`. Runtime artifact: `.specify/memory/glossary.md`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish baseline and target locations before any change.

- [ ] T001 Record current pytest baseline (pass/fail counts, listing pre-existing failures) so regressions are distinguishable per project test-baseline discipline; save note in `.specify/specs/029-glossary-mechanism/verification.md` (create if absent)
- [ ] T002 [P] Confirm target directories exist and are writable: `templates/`, `.specify/templates/`, `shared/workflow/`, `.specify/shared/workflow/`, `scripts/python/`, `tests/contract/`, `tests/unit/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The glossary file-format skeleton and the read/validate engine core that ALL stories build on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T003 [P] Create the glossary file-format template `templates/glossary-template.md` (H1 title, authoring-rule preamble — common words excluded, user-authoritative, conflict-confirm — and the exact `| Canonical | Variants | Meaning | Origin | Status |` table header) per contracts/glossary-file-format.md (C-2, C-4)
- [ ] T004 Mirror to `.specify/templates/glossary-template.md` and verify byte-identical (`diff -q templates/glossary-template.md .specify/templates/glossary-template.md`) (depends: T003)
- [ ] T005 Create engine scaffold `scripts/python/glossary-utils.py` (stdlib-only argparse `--action`; Markdown-table load/parse/serialize helpers matching data-model.md entry fields; JSON stdout / non-zero-on-error convention like feedback-utils.py)
- [ ] T006 [P] Write FAILING unit tests for `validate` and `list` in `tests/unit/test_glossary_utils.py` (valid/invalid structure, empty-but-valid glossary, entry parsing) per contracts/glossary-utils-cli.md C-2, C-6
- [ ] T007 Implement `validate` action in `scripts/python/glossary-utils.py` (enforce C-2/C-3 of glossary-file-format.md) (depends: T005, T006)
- [ ] T008 Implement `list` action in `scripts/python/glossary-utils.py` (return `{count, entries[]}`) (depends: T005, T006)

**Checkpoint**: File format + read/validate engine ready — user stories can begin.

---

## Phase 3: User Story 1 - Initialize glossary at instruction generation (Priority: P1) 🎯 MVP

**Goal**: Running instruction generation seeds a single project-wide `.specify/memory/glossary.md` (non-destructively) and wires it as ambient context.

**Independent Test**: Run `generate-instructions.sh` on a project with domain terms → a valid glossary.md exists with those terms (common words excluded), the Documentation Map lists it, and a re-run preserves existing entries.

### Tests for User Story 1 (MANDATORY) ⚠️

- [ ] T009 [P] [US1] Write FAILING unit test for `init` action (create-if-absent, `--force`, non-destructive when file exists) in `tests/unit/test_glossary_utils.py` per glossary-utils-cli.md C-1
- [ ] T010 [P] [US1] Write FAILING contract test `tests/contract/test_glossary_mechanism.py`: (a) `glossary-template.md` present in both mirrors & byte-identical; (b) `templates/instructions-template.md` Documentation Map contains the Glossary row; (c) `generate-instructions.sh` invokes glossary init; (d) re-running init preserves existing entries — per contracts/instruction-init.md

### Implementation for User Story 1

- [ ] T011 [US1] Implement `init` action in `scripts/python/glossary-utils.py` (create from `--from-template`, default `templates/glossary-template.md`, only if absent; `--force`) per glossary-utils-cli.md C-1 (depends: T005)
- [ ] T012 [US1] Add non-destructive glossary seed hook to `scripts/bash/generate-instructions.sh` (invoke `glossary-utils.py --action init`; never overwrite existing) per instruction-init.md C-1/C-3
- [ ] T013 [US1] Add the Glossary row to the Documentation Map in `templates/instructions-template.md` per instruction-init.md C-4
- [ ] T014 [US1] Mirror the instructions-template change to `.specify/templates/instructions-template.md`; verify `diff -q` (depends: T013)
- [ ] T015 [US1] Add domain-term seeding guidance (propose observed terms as `origin=auto`/`status=proposed`, exclude common words, route collisions through the conflict protocol) to `templates/commands/instructions.md`, then propagate to per-tool runtime copies (`.claude/commands/speckit.instructions.md`, `.github/prompts/instructions.prompt.md`, `.qoder/commands/instructions.md`) per instruction-init.md C-2
- [ ] T016 [US1] Manual QA: run `generate-instructions.sh`; confirm `.specify/memory/glossary.md` created, `--action validate` passes, and the generated `.specify/instructions.md` Documentation Map lists the glossary (quickstart.md step 1)

**Checkpoint**: US1 fully functional and independently testable (MVP).

---

## Phase 4: User Story 2 - Correct & anchor voice/dictated input (Priority: P1)

**Goal**: Every `/speckit.*` command anchors recorded variants → canonical terms when interpreting input, surfacing the correction and deferring on ambiguity.

**Independent Test**: With a seeded variant, a command interprets input using the canonical term, shows the substitution, and asks instead of guessing when a variant is ambiguous.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T017 [P] [US2] Write FAILING contract test in `tests/contract/test_glossary_mechanism.py`: `shared/workflow/glossary.md` exists in both mirrors (byte-identical) and its correction section covers variant→canonical mapping, traceable/visible correction (FR-006), and defer-on-ambiguity (FR-007); and each of `requirements`/`plan`/`tasks`/`implement` command templates contains a `## Glossary` reference to it

### Implementation for User Story 2

- [ ] T018 [US2] Author `shared/workflow/glossary.md` correction/anchoring section per contracts/glossary-protocol.md C-1 (variant→canonical, non-destructive interpretation, traceable correction, ambiguity defer)
- [ ] T019 [US2] Mirror `shared/workflow/glossary.md` to `.specify/shared/workflow/glossary.md`; verify `diff -q` (depends: T018)
- [ ] T020 [US2] Add a lightweight `## Glossary` reference step (modeled on the existing `## Feedback` step) citing `shared/workflow/glossary.md` to `templates/commands/requirements.md`, `templates/commands/plan.md`, `templates/commands/tasks.md`, `templates/commands/implement.md`
- [ ] T021 [US2] Propagate the `## Glossary` step to the per-tool runtime command copies for those four commands (`.claude/commands/speckit.*.md`, `.github/prompts/*.prompt.md`, `.qoder/commands/*.md`) — source minus frontmatter, with `templates/` → `.specify/templates/` path rewrites (depends: T020)
- [ ] T022 [US2] Manual QA: with a seeded variant entry, confirm a command resolves it to the canonical term and surfaces the correction (quickstart.md step 2)

**Checkpoint**: US1 and US2 both independently functional.

---

## Phase 5: User Story 3 - Progressive enrichment with conflict prompts (Priority: P2)

**Goal**: New terms proposed at workflow checkpoints; conflicts (structural + phonetic/meaning) are surfaced and require explicit user confirmation before any write.

**Independent Test**: Introduce a term that collides with an existing entry → conflict is presented and nothing is written until the user resolves it.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T023 [P] [US3] Write FAILING unit test for `detect-conflict` (identical canonical; variant already bound to a different canonical; ambiguous variant) in `tests/unit/test_glossary_utils.py` per glossary-utils-cli.md C-5
- [ ] T024 [US3] Write FAILING unit test that `add` refuses a conflicting write without `--confirmed-resolution` and succeeds with it (single enforcement point for FR-009) in `tests/unit/test_glossary_utils.py` (same file as T023 → sequential)

### Implementation for User Story 3

- [ ] T025 [US3] Implement `detect-conflict` action (structural collisions only; phonetic similarity advisory) in `scripts/python/glossary-utils.py` per glossary-utils-cli.md C-5 (depends: T005)
- [ ] T026 [US3] Implement `add` action with conflict precheck + `--confirmed-resolution` enforcement per glossary-utils-cli.md C-3, C-7 (depends: T025)
- [ ] T027 [US3] Author the progressive-enrichment (checkpoint proposals, FR-004) and conflict-detection/confirmation (FR-008/FR-009) sections in `shared/workflow/glossary.md` and mirror to `.specify/shared/workflow/glossary.md` (verify `diff -q`) per glossary-protocol.md C-2, C-3
- [ ] T028 [US3] Manual QA: use `detect-conflict` on a colliding term and confirm the protocol requires user confirmation before writing (quickstart.md step 3)

**Checkpoint**: US1–US3 independently functional.

---

## Phase 6: User Story 4 - Manual edit with user precedence (Priority: P2)

**Goal**: Users edit the glossary directly; user-authored entries are authoritative and survive regeneration; auto proposals never silently overwrite them.

**Independent Test**: Edit a row (origin=user), re-run generation → the manual value is preserved and not overwritten by an auto proposal.

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T029 [P] [US4] Write FAILING unit test: `add` with `origin=auto` does NOT overwrite an existing `origin=user` entry without confirmation (FR-011) in `tests/unit/test_glossary_utils.py`
- [ ] T030 [P] [US4] Write FAILING contract/round-trip test in `tests/contract/test_glossary_mechanism.py`: edit entries → run `init` again → user-authored rows preserved byte-for-byte (FR-013)

### Implementation for User Story 4

- [ ] T031 [US4] Implement `remove` action (no-op success on missing term) in `scripts/python/glossary-utils.py` per glossary-utils-cli.md C-4 (depends: T005)
- [ ] T032 [US4] Implement the user-precedence rule in `add` (auto never overwrites user without explicit confirmation) per data-model.md precedence rule + glossary-utils-cli.md C-3 (depends: T026)
- [ ] T033 [US4] Author the user-precedence + manual-edit section (FR-010/FR-011) in `shared/workflow/glossary.md` and mirror to `.specify/shared/workflow/glossary.md` (verify `diff -q`) per glossary-protocol.md C-4
- [ ] T034 [US4] Manual QA: edit a row to `origin=user`, re-run generation, confirm preservation and no auto-overwrite (quickstart.md step 4)

**Checkpoint**: All four user stories independently functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T035 [P] Document the glossary mechanism in `docs/` (e.g. `docs/skills/glossary.md` or `docs/memory` area) and add a lean pointer from `README.md`/Documentation Map (one-way reference direction), plus a Documentation Map row for this repo's own instructions
- [ ] T036 [P] Verify ALL mirror pairs byte-identical: `diff -rq` for `templates/glossary-template.md` & `templates/instructions-template.md` vs `.specify/templates/`; `shared/workflow/glossary.md` vs `.specify/shared/workflow/`; and per-tool command copies vs their source templates
- [ ] T037 Run the full `pytest` suite; confirm new contract + unit tests pass and there are no regressions vs the T001 baseline
- [ ] T038 Run quickstart.md end-to-end (all 4 steps) and record results in `verification.md`
- [ ] T039 Feature review: update `.specify/memory/features/031.md` (Implementation Notes / status criteria) and `features.md` if the task breakdown exposed any change; keep status `Planned` until `/speckit.implement`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies.
- **Foundational (Phase 2)**: depends on Setup; BLOCKS all user stories (glossary-template + engine scaffold/validate/list are shared).
- **User Stories (Phase 3–6)**: all depend on Foundational. US1 (MVP) first; US2 is prompt-side and independent; US3/US4 extend the engine (`add`/`detect-conflict`/`remove`/precedence) and the protocol doc.
- **Polish (Phase 7)**: depends on the desired stories being complete.

### User Story Dependencies

- **US1 (P1)**: after Foundational. Independent.
- **US2 (P1)**: after Foundational. Independent of US1 (touches protocol doc + command templates, not the engine beyond `list`).
- **US3 (P2)**: after Foundational. Adds `detect-conflict`/`add`; independently testable.
- **US4 (P2)**: after Foundational. `T032` builds on US3's `add` (T026); otherwise independent.

### Within Each User Story

- Tests (FAIL first) → engine actions / templates → mirrors → manual QA.
- Same-file test tasks (e.g. T023/T024 in `test_glossary_utils.py`) run sequentially, not in parallel.

### Parallel Opportunities

- T003 and T006 (different files) can run in parallel within Foundational.
- US1: T009 (unit) and T010 (contract) are different files → parallel.
- US4: T029 (unit) and T030 (contract) are different files → parallel.
- Polish: T035 and T036 are parallel.
- With capacity, US1 and US2 can proceed in parallel once Foundational is done.

---

## Parallel Example: User Story 1

```bash
# Launch the two US1 test tasks together (different files):
Task: "Unit test for init action in tests/unit/test_glossary_utils.py"        # T009
Task: "Contract test for template/wiring/non-destructive in tests/contract/test_glossary_mechanism.py"  # T010
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Phase 1 Setup → 2. Phase 2 Foundational → 3. Phase 3 US1 → 4. **STOP & VALIDATE**: run quickstart step 1; the glossary is created and ambient. Demo-able MVP.

### Incremental Delivery

Foundational → US1 (init/ambient) → US2 (voice correction) → US3 (enrichment/conflict) → US4 (manual precedence) → Polish. Each story is a self-contained increment that does not break earlier ones.

---

## Notes

- [P] = different files, no incomplete deps. `[Story]` maps each task to a user story for traceability.
- The engine (`glossary-utils.py`) is a single file; its actions are split across stories but edits are sequential per file.
- **Mirror discipline is the top rework risk**: every `templates/`, `shared/workflow/`, and command-template edit MUST be dual-written and verified with `diff` (T004, T014, T019, T021, T027, T033, T036).
- Fuzzy homophone/meaning judgment stays prompt-side (Principle IX) — the engine only does structural detection and enforces "no conflicting write without confirmation".
- Prefer `[~]` (deferred, with a recorded reason) over leaving a task `[ ]`.
