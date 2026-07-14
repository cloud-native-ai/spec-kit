---

description: "Task list: Reclassify sdd-workflow as a Shared Reference Directory"
---

# Tasks: Reclassify sdd-workflow as a Shared Reference Directory

**Requirement ID**: 028
**Requirement Key**: 028-sdd-workflow-refactor
**Related Feature**: 029 Shared Reference Directory
**Input**: Design documents from `.specify/specs/028-sdd-workflow-refactor/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), data-model.md, contracts/

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates writing/updating tests before behavior; contract + unit + integration tasks emitted per story before implementation)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- DoD-1: All ten reference documents live at `shared/workflow/` with content byte-equivalent to their originals (SC-003).
- DoD-2: `sdd-workflow` is absent as a skill from `skills/`, `.specify/skills/`, every tool skills symlink, and the skills registry/count (SC-002).
- DoD-3: `shared/` is packaged and installed to `.specify/shared/`, retained across re-init (SC-004, SC-005).
- DoD-4: All ~38 source references rewritten to the correct per-artefact form; no reference resolves to a dead link (FR-007, FR-008, FR-011).
- DoD-5: Repository-wide `grep sdd-workflow` returns zero live matches outside the excluded set (SC-001).
- DoD-6: Docs describe the shared reference directory, not a skill; `.specify/` mirror regenerated (FR-009).
- DoD-7: Full `pytest` run shows no new failures vs. the pre-refactor baseline (SC-006).

**DoD Status**: met

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

### Task State Sigil

- `- [ ]` — Open. Not yet complete.
- `- [X]` — Closed. Fully executed and verified.
- `- [~]` — Deferred. Handoff with reason recorded in `verification.md`.

## Path Conventions

Code-generator/framework layout: source assets at repo root (`shared/`, `skills/`, `templates/`, `src/specify_cli/`), tests under `tests/{unit,contract,integration}/`, installed mirror under `.specify/`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Capture baselines and scaffold the new source directory.

- [X] T001 [P] Capture pre-refactor baselines: record the current `grep -rn "sdd-workflow"` match count and the current skill count ("20 total"), and run `pytest -q` to snapshot the passing/failing baseline; note results in `.specify/specs/028-sdd-workflow-refactor/verification.md` (create if absent).
- [X] T002 Create the source directory `shared/workflow/` at repo root (empty, git-tracked).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Physically relocate the ten shared documents. Every user story depends on the docs already living at their new home.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T003 Relocate all ten reference docs with history preserved: `git mv skills/sdd-workflow/references/{user-input-protocol,feature-integration,agent-configuration,checklist-methodology,requirements-guidelines,dfx-catalog,clarify-taxonomy,ignore-patterns,tool-definitions,feedback-step}.md shared/workflow/` — verify content parity per `data-model.md` §2 (0 lost, 0 altered).

**Checkpoint**: `shared/workflow/` holds all ten docs; `skills/sdd-workflow/` now contains only `SKILL.md` + an empty `references/`.

---

## Phase 3: User Story 2 - Relocate shared protocols to a dedicated shared reference location (Priority: P1) 🎯 MVP

**Goal**: Make `shared/` a first-class packaged core asset installed to `.specify/shared/` and retained across re-init, with the path-rewrite rule that lets templates reference it root-relative.

**Independent Test**: After a fresh init, `.specify/shared/workflow/` contains all ten docs; a re-init leaves it untouched; `rewrite_paths("shared/workflow/x.md")` yields `.specify/shared/workflow/x.md`.

### Tests for User Story 2 (MANDATORY) ⚠️

> Write these FIRST and ensure they FAIL before implementation.

- [X] T004 [P] [US2] Unit test for the `shared/` path-rewrite rule (root-relative → `.specify/shared/`, idempotent, guarded) in `tests/unit/test_rewrite_paths_shared.py` (contract: `contracts/path-rewrite.contract.md`).
- [X] T005 [P] [US2] Contract test that `pyproject.toml` force-include maps `shared` and that the init copy places `shared/workflow/*` into `.specify/shared/workflow/` in `tests/contract/test_shared_reference_directory.py` (contract: `contracts/install-copy.contract.md`).
- [X] T006 [P] [US2] Integration test: fresh init installs `.specify/shared/workflow/` with 10 docs; re-init preserves it (retained core asset) in `tests/integration/test_shared_dir_install.py` (contract: `contracts/install-copy.contract.md`).

### Implementation for User Story 2

- [X] T007 [US2] Add `"shared" = "specify_cli/shared"` to `[tool.hatch.build.targets.wheel.force-include]` in `pyproject.toml` (after the `agents` entry).
- [X] T008 [US2] Add a `shared/ → .specify/shared/` rule to `rewrite_paths()` in `src/specify_cli/__init__.py` (~L674), matching the existing negative-lookbehind pattern for `memory/`/`scripts/`/`templates/`.
- [X] T009 [US2] Add `".specify/shared"` to `_CORE_SPECIFY_ASSETS` in `src/specify_cli/__init__.py` (~L308) so re-init preserves the directory.
- [X] T010 [US2] Add the init copy block for `shared/` in `src/specify_cli/__init__.py` (near the skills copy ~L1267): guarded `if (resource_path / "shared").exists():` → `shutil.copytree(resource_path / "shared", project_path / ".specify" / "shared", dirs_exist_ok=True)`.

**Checkpoint**: `shared/` is packaged, installed, retained, and reachable via root-relative refs. US2 tests pass.

---

## Phase 4: User Story 1 - Stop treating shared protocols as an invocable skill (Priority: P1)

**Goal**: Remove `sdd-workflow` as a skill from source, the installed skills dir, all symlink surfaces, and the registry/count.

**Independent Test**: `skills/sdd-workflow/` is gone; after init `.specify/skills/sdd-workflow` and `<tool>/skills/sdd-workflow` do not exist; the skills registry/count no longer mentions it.

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T011 [P] [US1] Contract test that `skills/sdd-workflow` does not exist in source, that `skills-utils.py` enumeration excludes it, and that the skills registry/count omit it in `tests/contract/test_sdd_workflow_removed.py` (contract: `contracts/skill-removal.contract.md`).

### Implementation for User Story 1

- [X] T012 [US1] Delete the pseudo-skill directory `skills/sdd-workflow/` (its `SKILL.md` and now-empty `references/`) via `git rm -r`.
- [X] T013 [US1] Remove the `sdd-workflow` mention and decrement the skill count ("20 total" → "19 total") in the skills list — update the generated `.specify/instructions.md` (~L54) and any source that carries the count (e.g. `templates/instructions-template.md` if present); leave the SKILLS registry table free of an `sdd-workflow` row.

**Checkpoint**: `sdd-workflow` no longer exists as a skill anywhere. US1 test passes.

---

## Phase 5: User Story 3 - No dangling references after the move (Priority: P1)

**Goal**: Rewrite every remaining `sdd-workflow` reference to the shared location in the correct per-artefact form, leaving zero dead links.

**Independent Test**: Command templates reference `shared/workflow/…`; skills reference `.specify/shared/workflow/…`; the zero-reference gate returns empty; every rewritten link resolves.

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T014 [P] [US3] Contract test that each command template uses `shared/workflow/…` (no `sdd-workflow`) and each skill uses `.specify/shared/workflow/…`, with no form mixing, in `tests/contract/test_shared_reference_rewrite.py` (contract: `contracts/reference-rewrite.contract.md`).
- [X] T015 [P] [US3] Integration test for the zero-reference gate (empty result outside the excluded set) and link resolution of every `shared/workflow/*` target in `tests/integration/test_zero_sdd_workflow_references.py` (contract: `contracts/zero-reference-gate.contract.md`).

### Implementation for User Story 3

- [X] T016 [P] [US3] Rewrite `skills/sdd-workflow/references/<f>.md` → `shared/workflow/<f>.md` (root-relative form) in all 17 `templates/commands/*.md` (agents, analyze, checklist, clarify, constitution, feature, implement, instructions, plan, requirements, research, review, skills, tasks, team, todo, tools).
- [X] T017 [P] [US3] Rewrite the `sdd-workflow` reference in `templates/skills-template.md` to the installed absolute form `.specify/shared/workflow/<f>.md`.
- [X] T018 [P] [US3] Rewrite the hard-coded `.specify/skills/sdd-workflow/references/<f>.md` → `.specify/shared/workflow/<f>.md` in all 20 sibling `skills/*/SKILL.md` (analysis-project, browser-utils, cli-setup, create-agent, create-skills, create-team, database-utils, document-utils, draw-d3js, draw-echarts, draw-plantuml, extension-e2e-test, git-submodule-edit, git-workflow, improve-agent, improve-skills, improve-team, memory-recall, memory-record, think-skills).

**Checkpoint**: All source references point at the shared location. US3 tests pass (pending mirror regen in Polish).

---

## Phase 6: User Story 4 - Consistent reference form and documentation (Priority: P2)

**Goal**: Ensure docs describe the shared reference directory (not a skill) and the reference forms are consistent.

**Independent Test**: The four docs describe `shared/workflow`; no doc calls `sdd-workflow` a skill; forms are uniform per artefact type.

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T019 [P] [US4] Extend `tests/contract/test_shared_reference_rewrite.py` (or add a focused assertion) verifying the four docs no longer describe `sdd-workflow` as a skill and quote the corrected skill count.

### Implementation for User Story 4

- [X] T020 [P] [US4] Update `docs/agents/command-and-skills.md` and `docs/agents/design.md` to describe the shared reference directory instead of the `sdd-workflow` skill.
- [X] T021 [P] [US4] Update `docs/commands/skills.md` and `docs/skills/feedback.md` (feedback-step now at `shared/workflow/feedback-step.md`) to reference the shared location and remove skill framing.
- [X] T022 [US4] Update the AGENTS.md / instructions Documentation Map and skill-count wording so `sdd-workflow` is described as a shared reference directory (not a skill) and counts are consistent with US1.

**Checkpoint**: Documentation is consistent and free of skill framing for `sdd-workflow`.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Regenerate the mirror and run the final acceptance gates.

- [X] T023 Regenerate the `.specify/` mirror from source so it reflects the move (copy `shared/` → `.specify/shared/`, re-sync `.specify/skills/` without `sdd-workflow`, re-sync `.specify/templates/`, regenerate `.specify/instructions.md`); confirm no `sdd-workflow` remnant survives regeneration.
- [X] T024 Run the zero-reference acceptance gate: `grep -rn "sdd-workflow" .` excluding `.git`, `.venv`, `docs/history`, `docs/summary/03-sdd-workflow-refactor-proposal.md`, and `.specify/specs/028-sdd-workflow-refactor/` → expect empty (SC-001).
- [X] T025 Run `pytest -q` and compare against the T001 baseline; confirm 0 new failures (SC-006). Record the SC-001…SC-006 status rows and any `[~]` deferrals in `.specify/specs/028-sdd-workflow-refactor/verification.md`.
- [X] T026 Run `quickstart.md` steps 1-7 as a final manual verification sweep and update Feature 029 detail (`.specify/memory/features/029.md`) with the implementation outcome.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately.
- **Foundational (Phase 2, T003)**: Depends on Setup — BLOCKS all user stories (docs must be at their new home first).
- **US2 (Phase 3)**: Depends on Foundational. Provides the install pipeline + `rewrite_paths` rule.
- **US1 (Phase 4)**: Depends on Foundational. Independent of US2/US3 (deleting the skill only requires the docs already relocated).
- **US3 (Phase 5)**: Depends on Foundational + US2 (templates need the `shared/` rewrite rule to resolve after install).
- **US4 (Phase 6)**: Depends on US3 (references settled) and US1 (final skill count).
- **Polish (Phase 7)**: Depends on US1 + US2 + US3 + US4 all complete.

### Within Each User Story

- Tests are written FIRST and must FAIL before implementation.
- US2: rewrite rule/packaging (code) before/with the copy block.
- US3: template rewrites and skill rewrites are independent files ([P]).

### Parallel Opportunities

- T004, T005, T006 (US2 tests) run in parallel.
- T016, T017, T018 (US3 rewrites) touch disjoint files → parallel.
- T020, T021 (US4 docs) run in parallel.
- US1 (Phase 4) can proceed in parallel with US2 (Phase 3) once Foundational is done, since they touch disjoint areas (skill deletion vs. CLI/packaging).

---

## Parallel Example: User Story 3

```bash
# Rewrite all reference-bearing source files together (disjoint files):
Task: "Rewrite refs in 17 templates/commands/*.md to shared/workflow/..."
Task: "Rewrite ref in templates/skills-template.md to .specify/shared/workflow/..."
Task: "Rewrite refs in 20 skills/*/SKILL.md to .specify/shared/workflow/..."
```

---

## Implementation Strategy

### MVP First (Foundational + User Story 2)

1. Complete Phase 1 (Setup) and Phase 2 (relocate docs).
2. Complete Phase 3 (US2): packaging + install + retention + rewrite rule.
3. **STOP and VALIDATE**: fresh init installs `.specify/shared/workflow/`; retained on re-init. This is the structural core.

### Incremental Delivery

1. Foundational + US2 → shared directory is installable (MVP).
2. Add US1 → skill removed from registry/symlinks.
3. Add US3 → all references rewritten, zero dead links.
4. Add US4 → docs consistent.
5. Polish → regenerate mirror, run zero-reference gate + pytest.

---

## Notes

- [P] tasks = different files, no dependencies.
- The reference rewrite is mechanical but high-volume; the T024 zero-reference gate is the hard acceptance guard against a missed path.
- Prefer `git mv`/`git rm` to preserve history for the relocation and deletion.
- The `.specify/` mirror is regenerated (T023), never hand-edited file-by-file.
- Commit after each phase or logical group.
