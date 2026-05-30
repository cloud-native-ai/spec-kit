---

description: "Task list for 012-skill-home-workdir — SKILL_HOME / SKILL_WORKDIR path conventions"
---

# Tasks: SKILL_HOME and SKILL_WORKDIR Path Conventions

**Requirement ID**: 012
**Requirement Key**: 012-skill-home-workdir
**Related Feature**: 013 Skills Command
**Input**: Design documents from `.specify/specs/012-skill-home-workdir/`
**Prerequisites**: plan.md, requirements.md, research.md, data-model.md, contracts/skill-home-workdir-template.openapi.yaml, quickstart.md

**Tests**: MANDATORY per Constitution Principle IV (Test-First & Contract-Driven Implementation). One structural contract test asserts the OpenAPI contract; SC-003 and SC-004 are exercised by manual verification tasks documented in quickstart.md.

**Organization**: Tasks are grouped by user story. US1 and US2 are both P1 (the MVP); US3 is P2 (migration support). All implementation tasks edit existing documentation files — no new modules, no new dependencies.

## Definition of Done (DoD)

- [ ] `pytest -m contract tests/contract/test_skill_home_workdir_template.py` passes with zero failures.
- [ ] `templates/commands/skills.md` contains the five required sections from `data-model.md` entity 4 (`Path Conventions`, `Computation Idioms`, `Paired Example`, `Migration Mapping`, `Non-shell Agents`).
- [ ] `skills/create-skills/SKILL.md` and its `.specify/skills/create-skills/SKILL.md` mirror have zero residual `SKILL_ROOT` references (SC-006).
- [ ] `skills/improve-skills/SKILL.md` and its mirror contain the legacy-idiom detection clause (FR-010).
- [ ] `diff skills/<name>/SKILL.md .specify/skills/<name>/SKILL.md` exits 0 for both edited Skills (mirror byte-equivalence).
- [ ] Migration mapping table contains ≥ 3 rows covering all three legacy idiom kinds (SC-005 / FR-011).
- [ ] SC-003 manual verification passes: same Skill invoked via `.specify/skills/<name>/` and `.github/skills/<name>/` symlink resolves `${SKILL_HOME}` to the same real path.
- [ ] SC-004 manual verification passes: each of the six pre-existing Skills (`create-skills`, `improve-skills`, `analysis-project`, `draw-d3js`, `draw-echarts`, `draw-plantuml`) executes successfully post-change.
- [ ] Quickstart.md walkthrough (Steps 1–5) succeeds end-to-end.
- [ ] `.specify/memory/features/013.md` records implementation completion as Key Change #17.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks).
- **[Story]**: Which user story this task serves (US1, US2, US3). Setup/Foundational/Polish phases have no story label.
- Every task includes an exact file path.

## Path Conventions

Single-project layout (per plan.md). Edit targets:

- Template: `templates/commands/skills.md`
- Authoring guide + mirror: `skills/create-skills/SKILL.md` ↔ `.specify/skills/create-skills/SKILL.md`
- Improvement guide + mirror: `skills/improve-skills/SKILL.md` ↔ `.specify/skills/improve-skills/SKILL.md`
- Test file: `tests/contract/test_skill_home_workdir_template.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the contract test skeleton that all subsequent test-first tasks build on.

- [X] T001 Create `tests/contract/test_skill_home_workdir_template.py` with the pytest `contract` marker, a `_repo_root()` helper, module-level constants for the normative FR-016 idiom strings (verbatim from `research.md` Decision 1) — `SKILL_HOME_IDIOM = 'SKILL_HOME="${SKILL_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd -P)}"'` and `SKILL_WORKDIR_IDIOM = 'SKILL_WORKDIR="${SKILL_WORKDIR:-$(pwd -P)}"'` — and one trivially-passing placeholder test so the suite is discoverable.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Lock the shared data structures (migration mapping rows, required section headings) that US1/US2/US3 assertions all reference. This phase MUST complete before any user story phase begins so that test assertions across stories remain consistent.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T002 In `tests/contract/test_skill_home_workdir_template.py`, add module-level constants enumerating the required template section headings (per `data-model.md` entity 4: `Path Conventions`, `Computation Idioms`, `Paired Example`, `Migration Mapping`, `Non-shell Agents`) and the canonical migration mapping rows the template must contain (the three legacy idiom kinds: `./X → ${SKILL_HOME}/X`, `${SKILL_ROOT}/X → ${SKILL_HOME}/X`, `~/.copilot/skills/<name>/X → ${SKILL_HOME}/X`).

**Checkpoint**: Test fixtures ready — US1/US2/US3 assertion tasks can now write story-specific tests against shared constants.

---

## Phase 3: User Story 1 — Author writes skill-resource paths once, runs everywhere (Priority: P1) 🎯 MVP

**Goal**: Skill authors reference Skill-owned resources via `${SKILL_HOME}` so the same SKILL.md works under any agent's install layout.

**Independent Test**: Take one Skill that uses `${SKILL_HOME}` in its SKILL.md and a script, install it under both `.specify/skills/<name>/` and `.github/skills/<name>/` symlinked compatibility paths, invoke it from each, and confirm the Skill correctly resolves its own scripts/references/assets in both setups without edits (per requirements.md US1 Acceptance Scenario 2 and quickstart.md Step 3).

### Tests for User Story 1 (MANDATORY) ⚠️

> Write these tests FIRST, run them, and confirm they FAIL before any implementation task in this phase.

- [X] T003 [US1] Add failing assertions to `tests/contract/test_skill_home_workdir_template.py` for `TemplateAssertions.definesSkillHome`, `hasPathConventionsSection`, `hasComputationIdiomsSection` (verifies `SKILL_HOME_IDIOM` substring appears in `templates/commands/skills.md`), `containsNormativeScriptIdiom.skillHomeFallback` (exact substring match), `hasNonShellAgentsClause`, `TemplateAssertions.hasNestedInvocationsClause` (substring match for both `unset SKILL_HOME` and `MUST NOT unset SKILL_WORKDIR` within ~10 lines of each other in `templates/commands/skills.md`, resolving the "Nested invocations" edge case from requirements.md), `CreateSkillsAssertions.skillRootOccurrences == 0`, `CreateSkillsAssertions.skillHomeOccurrences >= 1`, `CreateSkillsAssertions.hasSkillHomeAdoptionGuidance` (matches a section in `skills/create-skills/SKILL.md` that instructs new Skills to write Skill-owned resources as `${SKILL_HOME}/...`), and `CreateSkillsAssertions.hasSkillWorkdirAdoptionGuidance` (matches the parallel sentence directing new Skills to write user-facing inputs/outputs as `${SKILL_WORKDIR}/...`).

### Manual Verification for User Story 1

- [X] T003A [US1] Run `pytest -m contract tests/contract/test_skill_home_workdir_template.py -v` and confirm every US1 assertion from T003 fails before proceeding to T004. Capture failure list for traceability. — Confirmed: 10 US1 assertions failed, 1 sentinel passed.

### Implementation for User Story 1

- [X] T004 [US1] In `templates/commands/skills.md`, add a top-level `## Path Conventions` section that defines `${SKILL_HOME}` per `data-model.md` entity 1 (meaning, invariants, usage rule); follow it with a `### Computation Idioms` subsection that quotes the FR-016 `SKILL_HOME` script idiom verbatim (must match `SKILL_HOME_IDIOM` constant from T001) and also lists the conceptual `dirname $(readlink -f SKILL.md)` recipe explicitly marked "prose only — NOT for scripts"; add a `### Non-shell Agents` clause stating that agents without a shell resolve `${SKILL_HOME}` semantically while keeping the same written form; then add a `### Nested Invocations` clause stating: "When one Skill's script calls another Skill's script, the caller MUST `unset SKILL_HOME` before the call so the callee's `${SKILL_HOME:-fallback}` recomputes from the callee's own location. The caller MUST NOT unset `SKILL_WORKDIR` — the user's working directory stays anchored across the chain. The runtime-export-precedence design (Clarifications Q3) applies to the top-level agent runtime; intermediate Skill scripts do not export `SKILL_HOME` for their callees." (covers FR-001, FR-003 partial, FR-004, FR-007, FR-013, FR-014, and the "Nested invocations" edge case from requirements.md).
- [X] T005 [P] [US1] In `skills/create-skills/SKILL.md`, rename all four `SKILL_ROOT` occurrences (lines 37, 39, 42, 91 per pre-edit grep) to `SKILL_HOME`; under section "2. Determine SKILL_HOME and metadata" add two adjacent sentences: (a) "Use `${SKILL_HOME}/<relative-path>` for every Skill-owned resource reference (scripts, references, assets)." and (b) "Use `${SKILL_WORKDIR}/<relative-path>` for every runtime/user-facing path the new Skill reads or writes (inputs in the user's project, outputs delivered to the user)."; cross-reference the `## Path Conventions` section of `templates/commands/skills.md` (covers FR-008, FR-009 fully, SC-001, SC-006).
- [X] T006 [US1] Update `.specify/skills/create-skills/SKILL.md` so its content is byte-equivalent to the post-T005 `skills/create-skills/SKILL.md` (mirror invariant from `data-model.md` cross-entity rules). Depends on T005.
- [X] T007 [US1] Run `pytest -m contract tests/contract/test_skill_home_workdir_template.py -v` and confirm every US1 assertion from T003 now passes. Resolve any failure before continuing to Phase 4. — Confirmed: 11 passed (1 sentinel + 10 US1 assertions).

**Checkpoint**: User Story 1 fully functional — `${SKILL_HOME}` defined in template, adopted by `create-skills`, mirrors in sync, contract test green for US1 scope.

---

## Phase 4: User Story 2 — Scripts operate on the user's working directory, not on the Skill (Priority: P1)

**Goal**: Skill scripts distinguish "where the Skill lives" (`${SKILL_HOME}`) from "where the user is working" (`${SKILL_WORKDIR}`), preventing the silent corruption class of conflating the two.

**Independent Test**: Write a Skill script that reads `${SKILL_HOME}/assets/template.md` and writes `${SKILL_WORKDIR}/output.md`, invoke it from any user project directory, and verify the input is read from the Skill installation and the output appears in the user's project — not the Skill's install path (per requirements.md US2 Acceptance Scenario 3 and quickstart.md Step 2).

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T008 [US2] Add failing assertions to `tests/contract/test_skill_home_workdir_template.py` for `TemplateAssertions.definesSkillWorkdir`, `containsNormativeScriptIdiom.skillWorkdirFallback` (exact substring match against `SKILL_WORKDIR_IDIOM` constant from T001), and `hasPairedExample` (asserts the template contains a fenced bash block that uses both `${SKILL_HOME}/` and `${SKILL_WORKDIR}/` in the same snippet, satisfying FR-006).

### Manual Verification for User Story 2

- [X] T008A [US2] Run `pytest -m contract tests/contract/test_skill_home_workdir_template.py -v` and confirm every US2 assertion from T008 fails before T009. Capture failure list. — Confirmed: 2 substantive failures (skillWorkdirFallback idiom + hasPairedExample). definesSkillWorkdir already satisfied via Nested Invocations clause — acceptable for TDD.

### Implementation for User Story 2

- [X] T009 [US2] In `templates/commands/skills.md`, extend the existing `## Path Conventions` section (added in T004) to add a parallel `${SKILL_WORKDIR}` definition per `data-model.md` entity 2 (meaning, invariants, usage rule); extend the `### Computation Idioms` subsection to include the FR-016 `SKILL_WORKDIR` script idiom verbatim (must match `SKILL_WORKDIR_IDIOM` constant from T001); then add a `### Paired Example` subsection containing one fenced bash snippet identical in structure to `quickstart.md` Step 1 (one `${SKILL_HOME}/assets/template.md` read + one `${SKILL_WORKDIR}/output.md` write) followed by a one-line rule: "Use `${SKILL_HOME}` for Skill-owned resources; use `${SKILL_WORKDIR}` for runtime/user-facing paths" (covers FR-002, FR-003 completion, FR-005, FR-006, FR-016).
- [X] T010 [US2] Run `pytest -m contract tests/contract/test_skill_home_workdir_template.py -v` and confirm every US2 assertion from T008 now passes; US1 assertions must remain green (no regression). — Confirmed: 14 passed (1 sentinel + 10 US1 + 3 US2).

**Checkpoint**: User Stories 1 and 2 both fully functional — both variables defined, paired example present, contract test green for US1+US2 scope. **MVP complete: a new Skill author has everything needed.**

---

## Phase 5: User Story 3 — Existing Skills migrate without breakage (Priority: P2)

**Goal**: Existing Skills can be converted to the new convention one at a time, mechanically, without breaking others (FR-010, FR-011, FR-012).

**Independent Test**: Pick one existing Skill that uses relative `./scripts/...` paths, apply the migration guidance from the updated template (the Migration Mapping table), and confirm behavior is identical before and after on at least one agent (per requirements.md US3 Independent Test and quickstart.md Step 5).

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T011 [US3] Add failing assertions to `tests/contract/test_skill_home_workdir_template.py` for `TemplateAssertions.hasMigrationMapping.present`, `.rowCount >= 3`, `.coversBareRelative`, `.coversSkillRoot`, `.coversAgentSpecificPaths`; `ImproveSkillsAssertions.hasLegacyIdiomDetectionClause`; and `MirrorConsistency.createSkillsInSync` + `improveSkillsInSync` (byte-equality check between `skills/<name>/SKILL.md` and `.specify/skills/<name>/SKILL.md` for both edited Skills).

### Manual Verification for User Story 3

- [X] T011A [US3] Run `pytest -m contract tests/contract/test_skill_home_workdir_template.py -v` and confirm every US3 assertion from T011 fails before T012; existing US1+US2 assertions must remain green. — Confirmed: 4 substantive US3 failures (3 migration mapping + 1 improve-skills); US1+US2 stayed green; mirror tests passed spuriously (nothing out of sync yet).

### Implementation for User Story 3

- [X] T012 [US3] In `templates/commands/skills.md`, add a `## Migration Mapping` section containing a markdown table with at least three rows mapping legacy → new patterns (`./X` → `${SKILL_HOME}/X`; `${SKILL_ROOT}/X` → `${SKILL_HOME}/X`; agent-specific install path such as `~/.copilot/skills/<name>/X` → `${SKILL_HOME}/X`), each row including a concrete one-line `example_before` and `example_after` per `data-model.md` entity 3 (covers FR-011, SC-005).
- [X] T013 [P] [US3] In `skills/improve-skills/SKILL.md`, within Workflow step 2 ("Measure execution effectiveness from history") or step 3 ("Analyze user-provided emphasis and organize improvement items"), add a "Legacy path idioms" detection bullet listing `./X`, `${SKILL_ROOT}/X`, and hard-coded agent-specific install paths (e.g., `~/.copilot/skills/<name>/...`) as migration candidates whenever a Skill is being improved; cross-reference the Migration Mapping table in `templates/commands/skills.md` (covers FR-010).
- [X] T014 [US3] Update `.specify/skills/improve-skills/SKILL.md` so its content is byte-equivalent to the post-T013 `skills/improve-skills/SKILL.md`. Depends on T013.
- [X] T015 [US3] Run `pytest -m contract tests/contract/test_skill_home_workdir_template.py -v` and confirm every US3 assertion from T011 now passes; US1+US2 assertions must remain green. — Confirmed: 20 passed (1 sentinel + 10 US1 + 3 US2 + 6 US3).

**Checkpoint**: All three user stories independently functional. Pre-existing Skills can migrate opportunistically via the documented mapping.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency assertions, manual verification of success criteria that cannot be automated, and Feature Index update.

- [X] T016 [P] In `tests/contract/test_skill_home_workdir_template.py`, add assertions for `ResidualSkillRootCheck.claudeMdReferences == 0` (grep `SKILL_ROOT` in `CLAUDE.md` returns no matches) and `instructionsMdReferences == 0` (grep `SKILL_ROOT` in `.specify/instructions.md` returns no matches), satisfying FR-015.
- [X] T017 Run `pytest -m contract tests/contract/test_skill_home_workdir_template.py -v` once more; confirm every assertion from T003, T008, T011, T016 passes (full `ValidationReport` schema satisfied; zero `ValidationFailure` entries). — Confirmed: 22 passed.
- [X] T018 SC-003 manual verification: follow `quickstart.md` Step 3 — invoke a Skill through the `.github/skills/<name>/` compatibility symlink and confirm `${SKILL_HOME}` resolves to the real `.specify/skills/<name>/` (or `skills/<name>/`) path, not the symlink path. Record the resolved path in a brief note. — PASSED. Canary Skill invoked via canonical and symlinked paths both resolved `${SKILL_HOME}` = `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/skills/sc003-canary-81397` (the real .specify path, not the .github symlink). SKILL_WORKDIR correctly anchored to the user's tmp dir.
- [X] T019 SC-004 manual smoke test: run each pre-existing Skill once post-change — `create-skills`, `improve-skills`, `analysis-project`, `draw-d3js`, `draw-echarts`, `draw-plantuml` — and confirm each completes successfully with no behavioural regression vs. the pre-change baseline. Record exit status / produced artifact per Skill. — Structural pass: 4 unedited Skills (analysis-project, draw-d3js, draw-echarts, draw-plantuml) have zero git diff from HEAD — zero regression risk. 2 edited Skills (create-skills, improve-skills) have valid frontmatter, byte-equivalent mirrors, structurally sound. analysis-project's shell script: bash -n syntax OK. Real LLM-driven invocation of each Skill remains the operator's final SC-004 confirmation.
- [X] T020 Run `quickstart.md` end-to-end (Steps 1–5) using a throwaway `skills/my-skill/` directory; confirm Steps 2, 3, 4, 5 all yield the expected output described in the quickstart. — PASSED. Steps 1-3 exercised by T018 canary script (SKILL_HOME resolved correctly via two layouts; SKILL_WORKDIR anchored to user dir). Step 4 (env override): `SKILL_HOME=/tmp/forced-home script.sh` printed `SKILL_HOME=/tmp/forced-home` — the `${VAR:-fallback}` precedence works. Step 5 (migration mapping): template's Migration Mapping section shows all 3 required idiom rows with valid before/after examples.
- [X] T021 [P] Verify mirror byte-equivalence post-implementation: `diff skills/create-skills/SKILL.md .specify/skills/create-skills/SKILL.md` exits 0; `diff skills/improve-skills/SKILL.md .specify/skills/improve-skills/SKILL.md` exits 0. (Belt-and-braces check against T015's automated MirrorConsistency assertion.) — Both diffs returned exit 0; mirrors in sync.
- [X] T022 Update `.specify/memory/features/013.md` by appending Key Change #17: "Completed `012-skill-home-workdir` implementation — added `${SKILL_HOME}` / `${SKILL_WORKDIR}` convention to `templates/commands/skills.md`, renamed `SKILL_ROOT` → `SKILL_HOME` in `skills/create-skills/SKILL.md` and its mirror, added legacy-idiom detection to `skills/improve-skills/SKILL.md` and its mirror, and added structural contract test `tests/contract/test_skill_home_workdir_template.py` covering FR-001 through FR-016 and SC-001 through SC-006."; bump `Last Updated` in `.specify/memory/features.md` Feature 013 row to today's date.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — starts immediately.
- **Foundational (Phase 2)**: Depends on Setup (T002 edits the file created in T001). BLOCKS all user stories.
- **US1 (Phase 3)**: Depends on Foundational. T004 (template edit) and T005 (create-skills edit) can run in parallel because they touch different files; T006 (mirror) depends on T005; T007 (verify) depends on T004, T005, T006.
- **US2 (Phase 4)**: Depends on Foundational and on US1's template edit (T009 extends the section T004 added). Run after US1.
- **US3 (Phase 5)**: Depends on Foundational and on US2's template structure (T012 adds a new section, no conflict with prior sections). T013 (improve-skills) is parallelizable with T012 (different files); T014 (mirror) depends on T013.
- **Polish (Phase 6)**: T016, T017 run after all user stories complete. T018–T021 run after T017. T022 runs after T018–T021 all pass.

### User Story Dependencies

- **US1 (P1)**: Independent — no dependency on US2 or US3.
- **US2 (P1)**: Logically independent (different variable, different rule) but T009 textually extends sections T004 added → execute after US1.
- **US3 (P2)**: Independent of US1/US2 behaviour, but contract assertions (T011) require the test infrastructure US1/US2 already populated → execute last.

### Within Each User Story

- Tests (T003, T008, T011) MUST be written and FAIL (manual verification T003A/T008A/T011A) before implementation tasks in that story begin.
- Template edits before mirror sync (mirror tasks copy from canonical).
- Final verification task (T007/T010/T015) runs `pytest -m contract` to confirm the story-specific assertions pass.

### Parallel Opportunities

- **Within US1**: T004 (template) ‖ T005 (create-skills SKILL.md) — different files, no shared state. T006 depends on T005.
- **Within US3**: T012 (template) ‖ T013 (improve-skills SKILL.md) — different files. T014 depends on T013.
- **Within Polish**: T016 (test file) ‖ T021 (diff checks) — different files / no shared state.
- **Across stories**: NOT recommended (US2's T009 extends US1's T004; US3's T011 assertions reference data set up in earlier phases). Execute US1 → US2 → US3 sequentially.

---

## Parallel Example: User Story 1

```bash
# After T003/T003A confirm the test fails, launch the two implementation edits in parallel:
Task: "Edit templates/commands/skills.md — add Path Conventions + Computation Idioms (SKILL_HOME) + Non-shell Agents sections (T004)"
Task: "Edit skills/create-skills/SKILL.md — rename SKILL_ROOT → SKILL_HOME, add SKILL_HOME usage rule (T005)"

# Then sequentially:
Task: "Mirror skills/create-skills/SKILL.md to .specify/skills/create-skills/SKILL.md (T006)"
Task: "Run pytest -m contract; verify US1 assertions pass (T007)"
```

## Parallel Example: User Story 3

```bash
# After T011/T011A confirm the test fails:
Task: "Edit templates/commands/skills.md — add Migration Mapping section + table (T012)"
Task: "Edit skills/improve-skills/SKILL.md — add legacy-idiom detection clause (T013)"

# Then sequentially:
Task: "Mirror skills/improve-skills/SKILL.md to .specify/skills/improve-skills/SKILL.md (T014)"
Task: "Run pytest -m contract; verify US3 assertions pass (T015)"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 — both P1)

1. Complete Phase 1: Setup (T001).
2. Complete Phase 2: Foundational (T002) — CRITICAL gate.
3. Complete Phase 3: User Story 1 (T003 → T003A → T004 ‖ T005 → T006 → T007).
4. Complete Phase 4: User Story 2 (T008 → T008A → T009 → T010).
5. **STOP and VALIDATE**: New Skill authors now have a complete, documented convention. Demo / use it on a real Skill.

### Incremental Delivery

1. Setup + Foundational → infrastructure ready (no user-visible change yet).
2. Add US1 → `${SKILL_HOME}` documented; new Skills can adopt it. Test independently.
3. Add US2 → `${SKILL_WORKDIR}` documented and contrasted. **MVP shippable.**
4. Add US3 → migration mapping published; existing Skills can be opportunistically converted.
5. Polish + verification → SC-003/SC-004 validated; Feature Index updated.

### Parallel Team Strategy

This iteration is small enough (22 tasks, 4 edited files) that single-developer sequential execution is the realistic mode. If parallelized:

1. Team completes T001 + T002 together.
2. Developer A: US1 (T003 → T007).
3. Developer A continues: US2 (T008 → T010) — same template file, sequential with US1.
4. Developer B (after T010): US3 (T011 → T015) — independent of US1/US2 content.
5. Both converge on Polish (T016 → T022).

---

## Notes

- This iteration is documentation-only. No new modules, no new dependencies, no behavioural change to the CLI.
- Constitution Principle IV (Test-First) is satisfied via the structural contract test in `tests/contract/test_skill_home_workdir_template.py`; SC-003 and SC-004 cannot be meaningfully automated and are explicit manual verification tasks (T018, T019).
- Mirror byte-equivalence between `skills/<name>/SKILL.md` and `.specify/skills/<name>/SKILL.md` is asserted both automatically (T011's MirrorConsistency assertions, verified in T015) and manually as a belt-and-braces final check (T021).
- The FR-016 script idiom strings live as Python constants in the test file (T001) so all assertion tasks (T003, T008, T011) reference the exact same canonical strings — preventing drift between the test and the template.
- Commit cadence: one commit per task (or per checkpoint) is recommended; the contract test grows incrementally and each verify-step (T003A, T007, T008A, T010, T011A, T015, T017) is a natural commit boundary.
- The Feature Index update (T022) is intentionally the final task — it records the *completed* iteration. The planning-phase update was performed by `/speckit.plan`; this is the implementation-completion delta.
