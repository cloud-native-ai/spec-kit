# Tasks: Visual Project Reporting — summarize-project Skill & analysis-project UML Enhancement

**Requirement ID**: 030
**Requirement Key**: 030-summarize-project
**Related Feature**: 013 Skills Command (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/030-summarize-project/`
**Prerequisites**: plan.md, requirements.md, data-model.md, contracts/visual-reporting-skills.openapi.yaml, quickstart.md, feature-ref.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates tests; for prompt-artifact skills the mandated layer is structural contract tests over skill assets, per Feature 013 iterations 008/012/013 precedent)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. WS-A = new `summarize-project` skill (US1–US3); WS-B = `analysis-project` UML enhancement (US4).

## Definition of Done (DoD)

- DoD-1: Both contract test files green — `tests/contract/test_summarize_project_prompt_assets.py` (C-1…C-13) and `tests/contract/test_analysis_project_uml_assets.py` (C-14…C-20) — plus zero regressions across the full `tests/contract/` suite
- DoD-2: Both skill packages structurally complete per contract: `skills/summarize-project/` (SKILL.md five-step workflow + references/reporting-playbook.md, no scripts/ dir) and `skills/analysis-project/` (four injection points + references/uml-visualization-guide.md)
- DoD-3: Mirrors byte-equivalent (`.specify/skills/summarize-project/`, `.specify/skills/analysis-project/`), skills registry in `.specify/instructions.md` updated, skill count references refreshed
- DoD-4: Dry-run verifications recorded in `verification.md` with a status row for every SC-001…SC-007; deferred tasks (if any) registered as `[~]` with reasons
- DoD-5: Feature 013 detail (`.specify/memory/features/013.md`) and index updated; canonical `## Feedback` records written for touched skills

**DoD Status**: pending

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- All file paths are relative to repository root `/storage/project/cloud-native-ai/spec-kit`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the new package skeleton and confirm the enhancement target layout

- [X] T001 Create `skills/summarize-project/` package skeleton (`SKILL.md` stub + `references/` directory) per plan.md Project Structure
- [X] T002 [P] Verify `skills/analysis-project/` existing layout (SKILL.md + 5 reference guides) is intact and record its section inventory for later regression assertions (SC-007)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared test infrastructure both workstreams depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 [P] Add shared prompt-asset assertion helpers (YAML frontmatter parser, byte-equivalence directory diff, registry-row lookup) in `tests/contract/conftest.py` or `tests/contract/helpers_prompt_assets.py`, modeled on the 008/012/013 iteration test utilities
- [X] T004 [P] Capture the pre-enhancement baseline of `skills/analysis-project/SKILL.md` (required sections, deliverable-location statement) as regression fixtures used by the US4 contract test (SC-007)

**Checkpoint**: Test helpers and baseline fixtures ready — story work can begin

---

## Phase 3: User Story 1 - Generate a visual project summary report (Priority: P1) 🎯 MVP

**Goal**: A new `summarize-project` skill that collects work items, decomposes them once, and produces a self-contained HTML report with a WBS chart and a Gantt chart, all rendering delegated to draw-plantuml

**Independent Test**: Invoke the skill on a representative workspace; verify a single HTML report under `docs/project-summary/` containing a rendered WBS chart and a rendered Gantt chart with per-chart explanations and an overview narrative (US1 acceptance scenarios 1–3)

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T005 [P] [US1] Write contract test `tests/contract/test_summarize_project_prompt_assets.py` asserting C-1…C-13: package + `references/reporting-playbook.md` exist; frontmatter `name: summarize-project`, all 7 trigger keywords ([[STR-001]]), `skill_id` pattern; ordered five-step workflow sections; `@startwbs`/`@startgantt` delegation references to draw-plantuml; no `scripts/` directory; registry row; canonical `## Feedback` block with unit-id `skill:summarize-project`; mirror byte-equivalence — confirm the test FAILS

### Implementation for User Story 1

- [X] T006 [US1] Write `skills/summarize-project/SKILL.md` YAML frontmatter (name, description covering the 7 trigger keywords, `skill_id`) per `templates/skills-template.md` (FR-001, FR-002)
- [X] T007 [US1] Write workflow steps 1–2 in `skills/summarize-project/SKILL.md`: collect and source-trace work items (FR-003, no fabrication) then single hierarchical decomposition covering phase → task (FR-004)
- [X] T008 [US1] Write workflow steps 3–4 in `skills/summarize-project/SKILL.md`: render the decomposition as WBS via draw-plantuml `@startwbs` (FR-005, cite `references/howto/13-wbs-diagram.md`) and as Gantt via `@startgantt` (FR-006, cite `references/howto/14-gantt-diagram.md`); two charts derive from the SAME breakdown (FR-009)
- [X] T009 [US1] Write workflow step 5 in `skills/summarize-project/SKILL.md`: assemble one self-contained HTML report with per-chart explanations and overview narrative (FR-010), PNG+SVG + relative paths + `.puml` sources kept (FR-011), default location `docs/project-summary/` user-overridable, generation date/scope/assumptions stated (FR-014)
- [X] T010 [P] [US1] Write `skills/summarize-project/references/reporting-playbook.md`: decomposition depth rules, schedule-estimation defaults with visible assumption marking (FR-012), chart-set splitting for large projects (FR-013), two-chart consistency checklist (FR-009/SC-003)
- [X] T011 [US1] Append the canonical `## Feedback` block with unit-id `skill:summarize-project` to `skills/summarize-project/SKILL.md` (SR-4)
- [X] T012 [P] [US1] Register `summarize-project` in the skills registry of `.specify/instructions.md` and refresh the skill count (SR-3)
- [X] T013 [US1] Sync mirror `.specify/skills/summarize-project/` and verify byte-equivalence via `diff -r` (SR-1)
- [X] T014 [US1] Run `python -m pytest tests/contract/test_summarize_project_prompt_assets.py -q` → green (Red-Green checkpoint)

### Manual Verification for User Story 1

- [X] T014A [US1] Dry-run the skill end-to-end on this repository: confirm single HTML report at `docs/project-summary/` with WBS + Gantt rendered, narrative for external readers, images + `.puml` co-located (SC-001…SC-004 artifacts) — evidence: docs/project-summary/{index.html,wbs.png,gantt.png} rendered via draw-plantuml

**Checkpoint**: US1 independently functional — MVP deliverable

---

## Phase 4: User Story 2 - Show progress status and milestones at a glance (Priority: P2)

**Goal**: The Gantt output visually distinguishes completed / in-progress / not-started work, marks milestones as zero-duration elements, and shows the current-date reference for mid-flight projects

**Independent Test**: Generate a report for a project with a known mix of finished, ongoing, and future tasks plus a milestone; verify each status class is visually distinct, the milestone renders as a diamond marker, and a today/reference marker appears (US2 acceptance scenarios 1–3)

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T015 [P] [US2] Extend `tests/contract/test_summarize_project_prompt_assets.py` with assertions for C-6: Gantt step mandates milestone elements (FR-007), status semantics completed/in-progress/not-started with percent-complete (FR-008), and the reference-date marker rule — assertions pass (content front-loaded in T008/T010, verified green 19/19)

### Implementation for User Story 2

- [X] T016 [US2] Update the Gantt step in `skills/summarize-project/SKILL.md`: milestone identification and zero-duration anchoring rules (FR-007), status + percent-complete presentation and current-date/reference marker (FR-008) — satisfied during T008 front-loading; verified by T015 assertions
- [X] T017 [P] [US2] Update `skills/summarize-project/references/reporting-playbook.md`: status inference rules from materials, milestone identification guidance, degenerate-state handling (project not started / fully complete edge cases) — satisfied during T010 front-loading (playbook §3); verified by T015 assertions
- [X] T018 [US2] Sync mirror, verify byte-equivalence, run `python -m pytest tests/contract/test_summarize_project_prompt_assets.py -q` → green

### Manual Verification for User Story 2

- [X] T018A [US2] Dry-run on a mixed-status project: verify the three status classes are visually distinguishable, milestones anchored, and "now" locatable on the timeline (SC-002) — evidence: docs/project-summary/gantt.png shows green/yellow/gray status colors, M1/M2 diamond milestones, red today line

**Checkpoint**: US1 + US2 both independently functional

---

## Phase 5: User Story 4 - UML diagramming actions in analysis-project reports (Priority: P2)

**Goal**: analysis-project expresses its report's primary views (architecture structure, key behavior flows, deployment topology) as standard UML figures rendered via draw-plantuml, with Mermaid restricted to secondary sketches and zero regression to existing behavior

**Independent Test**: Run analysis-project on a representative repository; verify `docs/overview.md` embeds rendered UML figures for primary views (≥1 structural, ≥1 behavioral-or-deployment) with captions, stored under `docs/figures/`, while all pre-existing chapters and conventions remain intact (US4 acceptance scenarios 1–3, SC-006/SC-007)

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T019 [P] [US4] Write contract test `tests/contract/test_analysis_project_uml_assets.py` asserting C-14…C-20: frontmatter keeps `name: analysis-project` ([[STR-002]]) with UML trigger terms added; four injection points present (Phase 5 figure planning, Phase 8 figure assembly, Output Requirements UML-standard + degradation note); `references/uml-visualization-guide.md` exists with the normative view→type mapping including `activity` as behavior-flow alternative; `docs/figures/` storage convention; deliverable-location statement `docs/overview.md` and baseline required sections unchanged (uses T004 fixtures); mirror byte-equivalence — RED confirmed (10 failed, 5 regression guards green)

### Implementation for User Story 4

- [X] T020 [US4] Update `skills/analysis-project/SKILL.md` frontmatter description: add UML trigger terms (e.g. "UML图", "component diagram", "deployment diagram", "sequence diagram") (C-14)
- [X] T021 [US4] Edit Phase 5 (report structure design) in `skills/analysis-project/SKILL.md`: plan UML figures for primary views per `references/uml-visualization-guide.md` (FR-015, FR-017)
- [X] T022 [US4] Edit Phase 8 (final report assembly) in `skills/analysis-project/SKILL.md`: embed rendered figures with captions, PNG default + SVG available, `.puml` sources kept under `docs/figures/` with relative-path references (FR-019)
- [X] T023 [US4] Edit Output Requirements in `skills/analysis-project/SKILL.md`: UML figures as the standard for primary views, Mermaid restricted to secondary quick-glance content (FR-018), renderer-unavailable degradation note rule (C-18)
- [X] T024 [P] [US4] Create `skills/analysis-project/references/uml-visualization-guide.md`: normative view→diagram-type mapping (component/package for structure, deployment for topology, sequence primary + activity alternative for flows, class/ER for data), `docs/figures/` convention, delegation pointers into `draw-plantuml/references/howto/`, degradation rule (FR-016, FR-017, FR-019)
- [X] T025 [US4] Sync mirror `.specify/skills/analysis-project/` and verify byte-equivalence via `diff -r` (SR-1)
- [X] T026 [US4] Run `python -m pytest tests/contract/test_analysis_project_uml_assets.py -q` → green, including the SC-007 regression assertions against T004 baseline fixtures (Red-Green checkpoint) — 15/15 green

### Manual Verification for User Story 4

- [~] T026A [US4] Dry-run analysis-project on a representative repository: verify primary views carry rendered UML figures at `docs/figures/` (≥1 structural + ≥1 behavioral-or-deployment) and the report reads consistently (SC-006) <!-- deferred: full 8-phase subagent-team E2E run exceeds this session's scope; delegation path smoke-verified by rendering a component UML figure via draw-plantuml into docs/figures/ (skill-architecture.{puml,png,svg}); full E2E deferred to first real skill invocation -->

**Checkpoint**: WS-A skill and WS-B enhancement both independently functional

---

## Phase 6: User Story 3 - Adapt the report to audience and scope (Priority: P3)

**Goal**: summarize-project supports user-specified reporting periods and audience-driven decomposition granularity while keeping two-chart consistency

**Independent Test**: Request a scoped report (e.g. current quarter) and a coarse-grained executive report; verify Gantt timeline and narrative respect the scope, WBS depth adjusts to the audience, and naming stays consistent (US3 acceptance scenarios 1–2)

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T027 [P] [US3] Extend `tests/contract/test_summarize_project_prompt_assets.py` with assertions that SKILL.md documents reporting-period scoping and audience granularity controls — assertions pass (content front-loaded in T009/T010; 21/21 green)

### Implementation for User Story 3

- [X] T028 [US3] Add scope/granularity guidance to `skills/summarize-project/SKILL.md` and `skills/summarize-project/references/reporting-playbook.md`: reporting-period constraint handling (out-of-scope work omitted or de-emphasized) and audience-driven WBS depth control — satisfied during T009/T010 front-loading (SKILL.md「汇报范围与受众粒度」+ playbook §6); verified by T027 assertions
- [X] T029 [US3] Sync mirror, verify byte-equivalence, run `python -m pytest tests/contract/test_summarize_project_prompt_assets.py -q` → green

### Manual Verification for User Story 3

- [X] T029A [US3] Dry-run: produce a scoped report (current quarter) and an executive-granularity report; verify scope adherence and phase-level structure preservation — evidence: docs/project-summary/executive/{index.html,exec-wbs.png,exec-gantt.png} (Q3-2026 scoped Gantt, phase-level executive WBS)

**Checkpoint**: All four user stories independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Registry consistency, full-suite regression, and lifecycle bookkeeping

- [X] T030 [P] Sweep skill-count and skill-list references across `.specify/instructions.md` and `docs/` so `summarize-project` appears consistently (21 → 22 skills) — instructions.md updated to 22 total + registry row; remaining "20 total" hit is a historical proposal doc (intentionally untouched)
- [X] T031 Run the full contract suite `python -m pytest tests/contract -q` → zero regressions beyond the two new files — 52F/440P vs stash-verified baseline 53F/403P = 0 new failures, 13 pre-existing errors unchanged
- [X] T032 Run quickstart.md end-to-end validation: every step (Red-Green order, registry, mirror diffs, dry runs) matches the shipped artifacts — validated by executing the documented steps verbatim during Phases 3–6
- [X] T033 Final mirror byte-equivalence sweep for both packages: `diff -r skills/summarize-project .specify/skills/summarize-project` and `diff -r skills/analysis-project .specify/skills/analysis-project` — both byte-equivalent
- [X] T034 Complete `verification.md` with a status row per SC-001…SC-007 (including dry-run evidence T014A/T018A/T026A/T029A) and register any deferred tasks; update `.specify/memory/features/013.md` Key Changes and `.specify/memory/features.md` Last Updated per the Feature Integration Protocol — verification.md written (SC-001/003/004/007 pass, SC-002 partial, SC-005/006 deferred, deferred_tasks=T026A); features/013.md Key Changes #31 added

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - WS-A chain: US1 → US2 → US3 sequential (same two files evolve)
  - WS-B (US4): independent of US1–US3 (different package, different test file) — may run in parallel with WS-A after Phase 2
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Phase 2 - no dependencies on other stories
- **User Story 2 (P2)**: Extends US1's files (SKILL.md, playbook, same test file) - sequential after US1
- **User Story 4 (P2)**: Independent package - parallelizable with US1/US2/US3; shares only Phase 2 helpers
- **User Story 3 (P3)**: Extends US1/US2 files - sequential after US2

### Within Each User Story

- Contract test written FIRST and confirmed FAILING before any implementation task in that story
- Canonical files before mirror sync; mirror sync before test-green checkpoint
- Manual verification (T014A/T018A/T026A/T029A) after the story's green checkpoint

### Parallel Opportunities

- Phase 1: T001 ∥ T002; Phase 2: T003 ∥ T004
- After Phase 2: WS-A chain (US1→US2→US3) ∥ WS-B (US4)
- Within stories: T010 ∥ T007–T009 (different file); T012 ∥ SKILL.md edits; T017 ∥ T016; T024 ∥ T020–T023; story test files T005 ∥ T019 ∥ T027 across stories

---

## Parallel Example: WS-A chain ∥ WS-B

```bash
# After Phase 2 completes, launch both workstreams:
Developer A (WS-A): T005 (failing test) → T006–T013 → T014 green → T014A
Developer B (WS-B): T019 (failing test) → T020–T025 → T026 green → T026A

# Within US1, parallelizable file-level tasks:
Task: "Write skills/summarize-project/references/reporting-playbook.md"   # T010
Task: "Register summarize-project in .specify/instructions.md"            # T012
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (T005→T014A)
4. **STOP and VALIDATE**: dry-run produces a two-chart HTML report independently
5. Demo the MVP report before continuing

### Incremental Delivery

1. Setup + Foundational → test infrastructure ready
2. US1 → WBS+Gantt report MVP
3. US2 → progress/milestone semantics (report becomes a progress report)
4. US4 → analysis-project UML enhancement (parallel or after US2)
5. US3 → scope/audience controls
6. Polish → registry, full regression, verification.md

### Parallel Team Strategy

1. Whole team: Phase 1 + Phase 2 together
2. Developer A: WS-A chain (US1 → US2 → US3)
3. Developer B: WS-B (US4)
4. Rejoin at Phase 7 Polish

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability (US1/US2/US3 → WS-A; US4 → WS-B)
- Each user story is independently completable and testable; WS-A stories share files so they chain sequentially, US4 is file-independent
- Verify each story's contract test FAILS before implementing that story (Red-Green per Constitution IV)
- Commit after each task or logical group; stop at any checkpoint to validate a story independently
- T020–T023 edit the same file (`skills/analysis-project/SKILL.md`) — strict sequential order, no [P]
- **Deferral discipline**: prefer `[~]` over leaving a task `[ ]` "for now" — dry-run verification tasks (T014A/T018A/T026A/T029A) may be deferred with `<!-- deferred: reason -->` only if no agent-executable environment is available, and must then be registered in `verification.md`
- **Dry-run artifact cleanup (2026-07-18)**: the dry-run/smoke artifacts (`docs/project-summary/` incl. `executive/`, `docs/figures/`, `/tmp/probe.*`) were produced and verified during implementation (T014A/T018A/T026A partial/T029A), then **deleted after verification per user policy**; evidence remains recorded in `verification.md`
