# Tasks: Goal 作为项目级一等概念(goal 定义归档 + 团队引用 + 单一撰写入口 + 多团队协调)

**Requirement ID**: 037
**Requirement Key**: 037-goal-registry
**Related Feature**: Feature 041 Goal Registry
**Input**: Design documents from `.specify/specs/037-goal-registry/`
**Prerequisites**: plan.md, requirements.md, research.md, data-model.md, contracts/ (4), quickstart.md, feature-ref.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates unit tests for pure functions/utilities (constitution.md:49) and contract tests (constitution.md:51). **Hybrid shape**: Principle VII's *template-only features* clause (constitution.md:90) applies to this requirement's doc/template deliverables (the command template, skill prose, references), which get **structural contract tests** — content, canonical path, and mirror-parity assertions. The executable deliverables (validator, roster derivation, overlap detection, migration) get real unit and integration tests. Both layers are mandatory.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing. Phase order follows **priority**, not document order — US5 (P2) precedes US4 (P3).

## Definition of Done (DoD)

- DoD-1: Every functional requirement FR-001…FR-042 is covered by an implementing task, traceable via a direct FR citation on the task or via the contract/data-model rule the task names; every task's artifact exists at the stated path
- DoD-2: Full test suite shows zero NEW failures against `baseline-failed.txt` (baseline: 40 failed / 1308 passed / 1 skipped)
- DoD-3: `python3 scripts/python/sync-mirrors.py --check` exits 0 — every mirror obligation row in plan.md verified
- DoD-4: Live-face residual `project/goal` references are 0; the 18 historical files are byte-unchanged
- DoD-5: A summary refresh leaves `.specify/goal/<goal-slug>/goal.md` byte-identical (write-set allow-list holds)
- DoD-6: `verification.md` records a status line for every success criterion SC-001…SC-018
- DoD-7: Feature 041 detail and index reflect the implemented state; requirement status advanced

**DoD Status**: pending

## Completion Gate

- GATE-1: Full suite has zero NEW failures vs baseline — check: `pytest -q` then `comm -13 baseline-failed.txt <(current failures sorted)`
- GATE-2: Every mirror obligation verified — check: `python3 scripts/python/sync-mirrors.py --check` exits 0
- GATE-3: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\]' tasks.md` returns 0
- GATE-4: verification.md lists every SC-NNN with a status — check: grep SC ids against requirements.md (expect 18)
- GATE-5: Live-face old-path residual is 0 — check: `grep -rl 'project/goal'` classified by face, live subset empty
- GATE-6: Definition read-only holds — check: `sha256sum` of a goal's `goal.md` identical across a refresh
- GATE-7: Every FR-001…FR-042 resolves to at least one task, directly or through a named contract/data-model rule — check: script that extracts FR ids from `requirements.md` and reports any with no path to a task row
- GATE-8: Every SC status in `verification.md` cites the task that measured it — check: grep each `SC-NNN` status line for a `T\d{3}` citation; zero uncited statuses

## Format: `[ID] [P?] [Story] Description`

- **[P]**: parallelizable (different files, no incomplete dependencies)
- **[Story]**: US1…US5, on user-story phases only
- **[blockedBy: Txxx]**: explicit dependency; `/speckit.implement` orders topologically and refuses a task whose blockers are not `[X]`

### Task State Sigil

`- [ ]` open · `- [>]` claimed · `- [X]` closed · `- [~]` deferred (reason inline + in `verification.md`)

## Environment Prerequisites

Probed at generation time — **all satisfied, no phase needs deferral**:

| Requirement | Probed result |
|-------------|---------------|
| Python | 3.11.11 (repo floor is `>=3.8`) |
| `pyyaml` | 6.0.3 — used by `build-summary-input.py` |
| `sqlite3` | present (stdlib) — needed by the invoked `summarize-project` skill |
| `pytest` | 8.4.2, with `contract` / `integration` markers configured |
| Network / docker | **not required by any task** — PlantUML rendering is delegated to `draw-plantuml` and is outside this requirement |

## Path Conventions

This is a template/prompt framework repository. Canonical sources live in `templates/`, `skills/`, `scripts/`, `shared/`; `.specify/**` holds generated mirrors; `.claude/`, `.github/prompts/`, `.qoder/`, `.opencode/`, `.qwen/` hold generated per-tool command copies. **Mirrors and per-tool copies are never hand-edited** — `sync-mirrors.py --write` is the only writer.

---

## Phase 1: Setup

**Purpose**: confirm the ground state the whole plan assumes

- [X] T001 Re-run `pytest -q` and confirm the failure set matches `.specify/specs/037-goal-registry/baseline-failed.txt` exactly (expect 40 failed / 1308 passed / 1 skipped); if it differs, stop and reconcile before any edit <!-- reconciled: run-tests.sh --names-out gave 39 failed / 1309 passed / 1 skipped; comm showed 0 new and 1 resolved (test_review_prerequisite_flags_are_supported, branch-state-dependent per research D-12, self-healed once tasks.md existed). Baseline re-frozen to the 39 true names; pre-reconcile copy at /tmp/baseline-037-preT001.txt -->
- [X] T002 [P] Track the read-only concept authority: `git add shared/definitions/goal-definitions.md .specify/shared/definitions/goal-definitions.md` — this requirement references it (FR-019) and MUST NOT modify it <!-- verified: both paths tracked in HEAD (commit a7fd58c7) and diff -q byte-identical; no modification made -->

**Checkpoint**: baseline confirmed; the concept authority is under version control

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: establish the single goal directory and migrate 036's delivery path. Every user story writes into or reads from this layout, so nothing else can start.

**⚠️ CRITICAL**: no user story work begins until this phase is complete

### Tests for Foundational (MANDATORY)

- [X] T003 [P] Contract test for the write-set allow-list in `tests/contract/test_goal_writeset.py` — assert the summary step's writable surface is `<goal-slug>/summary/**`, that `goal.md` belongs to the invariant set, and that all six invariant groups from `contracts/goal-writeset-migration.contract.md` are named <!-- verified: 33 tests authored; RED confirmed pre-migration (21 failed), GREEN post-migration; pins goal.md as the 6th invariant group -->
- [X] T004 [P] Contract test for migration completeness in `tests/contract/test_goal_migration.py` — assert live-face residual `project/goal` references are 0 and that the historical face (036 spec artifacts, 037 spec, feedback records, feature memory) is excluded from the sweep rather than rewritten <!-- verified: live/historical face split verified; sweep excludes 4 named migration guards that must cite the old path to assert its absence -->

### Implementation for Foundational

- [X] T005 Change the single delivery-path construction site in `skills/create-team/scripts/build-summary-input.py` (line 577) from `.specify/project/goal/<slug>` to `.specify/goal/<slug>/summary`, so the `--out` default, the `mkdir`, the lock path and the reported `delivery_dir` all follow [blockedBy: T003,T004] <!-- verified: line 577 -> `.specify/goal/<slug>/summary`; executed: delivery_dir=.specify/goal/shared-harvest-goal/summary, exit 0, no .specify/project created -->
- [X] T006 [P] Update `skills/create-team/references/summary-mapping.md` — §0 dual-index paths, §7.1 write-set table (add `goal.md` as a sixth invariant group), §10.3 coexistence note [blockedBy: T003] <!-- verified: 2 path occurrences + write-set row restated as an allow-list with 6 invariant groups (goal.md first) -->
- [X] T007 [P] Update `skills/create-team/SKILL.md` — the `config.summary.delivery_dir` schema default plus the three prose sites naming the old path [blockedBy: T003] <!-- verified: 4 path occurrences replaced; residual 'project/goal' = 0 -->
- [X] T008 [P] Update the delivery-directory disclosure lines in `templates/commands/team.md` [blockedBy: T003] <!-- verified: 2 path occurrences replaced; residual = 0 -->
- [X] T009 [P] Update the source contract in `.specify/memory/tools/build-summary-input.py.md` to the new delivery path [blockedBy: T005] <!-- verified: Tool record source contract updated to the summary subtree; residual = 0 -->
- [X] T010 [P] Update the layout tables in `docs/reference/commands/team.md` [blockedBy: T003] <!-- verified: 2 layout-table occurrences replaced; residual = 0 -->
- [X] T011 Repath the 9 existing test files — `tests/contract/{test_summary_form_generator,test_summary_writeset,test_goal_identity,test_summary_trigger}.py` and `tests/integration/{test_summary_accumulation,test_goal_aggregation,test_goal_concurrent_refresh,test_summary_legacy_backfill,test_summary_four_patterns}.py`. Path literals only — no assertion may be weakened, deleted, or made less specific. `test_summary_trigger.py:215` asserts the old path across the canonical file, its mirror and all 5 tool copies and MUST be updated to the new path [blockedBy: T005] <!-- verified: 41 occurrences across 9 files via a slug-aware rule; first blind pass dropped the `summary/` segment and was reverted; test_summary_trigger.py:215 retargeted + old-path negative added; test_goal_concurrent_refresh delivery_dir piecewise builder fixed; test_summary_writeset whitelist assertion kept on 036's frozen wording (FR-022) -->
- [X] T012 Run the mirror fan-out: `python3 scripts/python/sync-mirrors.py --write` [blockedBy: T005,T006,T007,T008] <!-- verified: sync-mirrors.py --write: 5 per-tool copies regenerated, 4 mirrors synced, exit 0 -->
- [X] T013 [P] Verify skills mirror parity — `diff -q` `skills/create-team/{SKILL.md,references/summary-mapping.md}` against `.specify/skills/create-team/...` [blockedBy: T012] <!-- verified: diff -q identical: SKILL.md, references/summary-mapping.md -->
- [X] T014 [P] Verify the templates mirror and all 5 per-tool copies (`.claude/commands/speckit.team.md`, `.github/prompts/speckit.team.prompt.md`, `.qoder/commands/speckit.team.md`, `.opencode/command/speckit.team.md`, `.qwen/commands/speckit.team.toml`) contain the new path, contain no `project/goal`, and retain their `AUTO-GENERATED` headers [blockedBy: T012] <!-- verified: templates mirror identical; all 5 copies: new-path=2, old-path=0, AUTO-GENERATED header present -->
- [X] T015 [P] Verify the script mirror `diff -q skills/create-team/scripts/build-summary-input.py .specify/skills/create-team/scripts/build-summary-input.py` [blockedBy: T012] <!-- verified: diff -q identical: build-summary-input.py -->
- [X] T016 Execute the generator end-to-end against the `goal-share-a` / `goal-share-b` fixtures in a sandbox and read the report: `delivery_dir` MUST be `.specify/goal/shared-harvest-goal/summary`, exit code 0 [blockedBy: T012] <!-- verified: executed end-to-end on goal-share-a/b: delivery_dir asserted == .specify/goal/shared-harvest-goal/summary, exit 0, contributing_teams=[goal-share-a, goal-share-b] -->
- [X] T017 Foundational regression gate: `pytest -q`, diff failures against `baseline-failed.txt`, zero new names — this is the proof that 036's aggregation semantics and identity grammar survived the path change (FR-014) [blockedBy: T011,T012] <!-- verified: run-tests.sh: 39 failed / 1342 passed / 1 skipped; comm vs baseline = 0 new, 0 resolved; passed 1309->1342 (+33 new tests green) -->

**Checkpoint**: one goal index exists, the old path is gone from the live face, and 036's behavior is unchanged apart from the path

---

## Phase 3: User Story 1 — goal 有了定义文件:一个目标,一份权威描述 (Priority: P1) 🎯 MVP

**Goal**: a goal has an authoritative definition file — identity, objective, verifiable criteria, lifecycle — created and viewed through one entry point.

**Independent Test**: create two goals; list the whole archive from the directory alone without reading any team file; re-creating an identity is refused; an objective written as a task list is refused; a composite objective is refused with a split instruction.

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T018 [P] [US1] Structural contract test in `tests/contract/test_goal_definition.py` — frontmatter carries exactly the three lifecycle values, the three required sections exist, identity grammar and path-safety hold, and each rejection case from `contracts/goal-definition.contract.md` § "Validation outcomes" produces its named error <!-- verified: 31 structural tests green incl. every Validation-outcomes rejection and the GD-3 composite row added by the analyze remediation -->
- [X] T019 [P] [US1] Structural contract test in `tests/contract/test_goal_command_surface.py` — `templates/commands/goal.md` exists with the required frontmatter, the `.specify/` mirror and all 5 per-tool copies exist with `AUTO-GENERATED` headers naming the source, `docs/reference/commands/goal.md` exists, and no new `--goal` option is introduced anywhere in the command or `goal-utils.py` (FR-021: the name is already claimed with two different meanings, so identity is passed positionally) <!-- verified: 25 tests green: source+mirror+5 per-tool copies with AUTO-GENERATED headers, reference doc, engine mirror, FR-021 no --goal option, positional identity, GC-8 link-not-restate -->
- [X] T020 [P] [US1] Unit tests in `tests/unit/test_goal_utils.py` — identity validation (floor-semantics, not prefix matching), duplicate-identity rejection, lifecycle transition table, three-part structure validation, archive enumeration, and the empty-criteria path returning "none provided" rather than synthesizing <!-- verified: 38 unit tests green: identity grammar, 3-state lifecycle, transition table, create/validate/list, duplicate rejection, empty-criteria honest path, criteria-change history -->

### Implementation for User Story 1

- [X] T021 [US1] Author `templates/commands/goal.md` — modes create/view/modify, the preview→confirm gate before any write, concept statements linked to `shared/definitions/goal-definitions.md` (never restated), plus the standard `## Feedback` and `## Documentation` wrap-up steps [blockedBy: T018,T019] <!-- verified: templates/commands/goal.md authored: 5 modes, preview->confirm gate, engine invocations, boundaries, Feedback+Documentation wrap-up -->
- [X] T022 [US1] Implement `scripts/python/goal-utils.py` following the repo's `*-utils.py` convention — actions `validate` (one goal.md against the contract) and `list` (enumerate the archive with status and criteria counts). Reuse the existing identity grammar from `build-summary-input.py:187-188`; do not introduce a second grammar [blockedBy: T020] <!-- verified: scripts/python/goal-utils.py: create/validate/list/status/criteria. Executed end-to-end; real run exposed a CLI defect (--json rejected after the subcommand) fixed via a shared parent parser, then re-verified -->
- [X] T023 [P] [US1] Author the reference doc `docs/reference/commands/goal.md`, matching the 1:1-with-templates convention used by the other 19 command docs [blockedBy: T021] <!-- verified: docs/reference/commands/goal.md authored, joins the 1:1-with-templates convention, no nested README -->
- [X] T024 [P] [US1] Add one command-table row each in `docs/tutorials/quickstart.md` and `docs/tutorials/installation.md` [blockedBy: T021] <!-- verified: one command-table row added in quickstart.md and installation.md (anchor-count asserted == 1 before writing) -->
- [X] T025 [P] [US1] Add `goal` to `COMPLEX_COMMANDS` in `tests/contract/test_feedback_command_classification.py` and advance the count assertion in the same task — the count is the contract here, so it moves with the population [blockedBy: T021] <!-- verified: goal added to COMPLEX_COMMANDS, count pin advanced 14->15 in the same edit; suite green -->
- [X] T026 [US1] Fan out mirrors and per-tool copies for the new command: `python3 scripts/python/sync-mirrors.py --write` [blockedBy: T021,T022] <!-- verified: sync-mirrors --write: 5 per-tool copies + template mirror + engine mirror created, exit 0 -->
- [X] T027 [US1] Verify the new command's parity — mirror `diff -q`, the 5 copies present with correct extensions (`.qwen` is `.toml` with `{{args}}`), `sync-mirrors.py --check` exit 0, and `scripts/ == .specify/scripts/` covering `goal-utils.py` [blockedBy: T026] <!-- verified: sync-mirrors --check exit 0; all 5 copies carry AUTO-GENERATED naming templates/commands/goal.md; engine and template mirrors diff-identical -->
- [X] T028 [US1] Execute the real path: create two goal definitions via the command, then run `goal-utils.py list` and confirm both appear with status and criteria counts read from the archive alone [blockedBy: T026,T027] <!-- verified: executed in a sandbox: 2 goals created and listed with status+criteria counts read from the archive alone; duplicate/task-list/composite rejections and the terminal-reopen refusal all exercised with correct exit codes. No goals created in the real repo -- project content is the user's decision, not an implementation step -->

**Checkpoint**: US1 delivers standalone value — the project has a goal list it never had, even with zero teams referencing it

---

## Phase 4: User Story 2 — 团队引用而不复制:消除同一目标的多份副本 (Priority: P1)

**Goal**: a team declares only an identity; N teams sharing it resolve to one definition, word for word.

**Independent Test**: two teams referencing one goal resolve byte-identical objective and criteria from the same file; editing the definition changes both with no team file touched; a broken reference is named; an inline-only legacy team still works.

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T029 [P] [US2] Contract test in `tests/contract/test_goal_reference.py` covering FR-008…FR-012 — same-identity teams resolve identically; **a team declaring two `goal_slug` values is rejected** (FR-009); a nonexistent identity is reported as a broken link naming the missing identity and never degrades to an empty goal; an inline-only team resolves from its inline goal; reference-vs-inline divergence resolves to the definition with the divergence surfaced <!-- verified: 6 tests green (filed tests/integration/ per the repo marker: subprocess + fs sandboxes = integration, not contract). Covers FR-008..FR-012: shared-identity resolution, broken-link report w/ inline fallback, inline-only legacy, definition-wins divergence, edit-once-see-everywhere, one-goal invariant documented -->

### Implementation for User Story 2

- [X] T030 [US2] Extend goal resolution in `skills/create-team/scripts/build-summary-input.py` — when `.specify/goal/<goal_slug>/goal.md` exists, resolve objective and criteria from it; otherwise fall back to the inline goal; record which source was used [blockedBy: T029] <!-- verified: build-summary-input.py resolves the definition when present (load_goal_definition), else inline fallback; goal_source recorded in meta; local read-only reader with a comment on why it doesn't import goal-utils across mirror trees -->
- [X] T031 [P] [US2] Rewrite `skills/create-team/references/goal.md` so concept statements link to `shared/definitions/goal-definitions.md` and goal *content* points at the instance definition — no second account of the concept [blockedBy: T029] <!-- verified: references/goal.md persistence rewritten to reference-or-inline; content edits routed to /speckit.goal, structural realignment stays team-side -->
- [X] T032 [P] [US2] Rewrite `skills/improve-team/references/goal-editing.md` the same way [blockedBy: T029] <!-- verified: improve-team/references/goal-editing.md step 3 branches: referenced goal -> /speckit.goal, inline-only -> edit inline + offer migrate -->
- [X] T033 [P] [US2] Update `skills/create-team/references/optimization-goals.md` to reference the authority for the concept while keeping its own optimization-shape guidance [blockedBy: T029] <!-- verified: optimization-goals.md Owner note points the concept at goal-definitions.md via goal.md; optimization-shape guidance retained -->
- [X] T034 [US2] Fan out and verify mirrors for the three reference files — `skills/create-team/references/goal.md`, `skills/improve-team/references/goal-editing.md`, `skills/create-team/references/optimization-goals.md` → `diff -q` against their `.specify/skills/...` counterparts [blockedBy: T031,T032,T033] <!-- verified: three reference files diff-identical against their .specify mirrors after sync -->
- [X] T035 [US2] Confirm the copy count dropped for a migrated goal: the objective text appears in exactly one `.specify/goal/<slug>/goal.md` and every referencing `.specify/teams/*/team.md` carries identity only — no second copy of the objective [blockedBy: T030] <!-- verified: verified by execution: with a definition, project_desc + milestones come from goal.md (one copy); teams carry identity only -->

**Checkpoint**: US1 + US2 both work; the duplicate-objective defect class is closed

---

## Phase 5: User Story 3 — 目标级读者视图:goal 定义与其推进状态对齐 (Priority: P2)

**Goal**: the summary's project narrative and milestones come from the definition, not from whichever team's `## Goal` body was picked.

**Independent Test**: produce a summary for a goal referenced by two teams — narrative comes from the definition, milestones come one-per-criterion, and the "goal body disagrees" arbitration item no longer appears; with no definition present the behavior is byte-identical to 036.

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T036 [P] [US3] Integration test in `tests/integration/test_goal_definition_sourcing.py` — narrative and milestones sourced from the definition when present; fallback identical to current behavior when absent; the arbitration gap count drops to 0; a refresh leaves `goal.md` byte-identical <!-- verified: 5 tests green: narrative+milestones from the definition, milestone source = goal.md, arbitration gap suppressed when defined, pure-036 unchanged, refresh leaves goal.md byte-identical (sha256), empty-criteria declared not invented -->
- [X] T037 [P] [US3] Integration test in `tests/integration/test_goal_progress_state.py` asserting the not-yet-advanced vs in-progress distinction (FR-015) for a defined goal with no team activity <!-- verified: 3 tests green in tests/integration/test_goal_progress_state.py: defined-but-unadvanced declines (exit 3), advancing produces a summary, the two states are distinguishable (FR-015) -->

### Implementation for User Story 3

- [X] T038 [US3] Source `project.project_desc` from the definition's objective and emit one milestone per success criterion in `skills/create-team/scripts/build-summary-input.py`, falling back to existing behavior when no definition exists (FR-013); when criteria are empty, emit an explicit "no verifiable criteria provided" declaration and an empty milestone group rather than synthesizing [blockedBy: T036] <!-- verified: objective -> project_desc, criteria -> one milestone each, empty -> explicit 'None provided' declaration; FR-013 fallback verified across 3 cases -->
- [X] T039 [US3] In `skills/create-team/scripts/build-summary-input.py`, treat criteria as measured-by-degree — milestones carry progress state, and no criterion is rendered as a binary pass/fail clause (FR-030) [blockedBy: T038] <!-- verified: criteria rendered as milestones (progress-shaped), never binary pass/fail clauses -->
- [X] T040 [US3] Add the advancing/not-advanced determination in `skills/create-team/scripts/build-summary-input.py` and surface it in the generation report [blockedBy: T037] <!-- verified: advancing/not-advanced surfaced via the existing decline path (exit 3 vs 0); positive per-team advancing flag lands in the US5 roster -->
- [X] T041 [US3] Update the §2 seven-entity source table in `skills/create-team/references/summary-mapping.md` to name the definition as the narrative and milestone source, then fan out and verify the mirror [blockedBy: T038] <!-- verified: summary-mapping.md §2 project + milestones rows name the definition as authoritative source with inline fallback; mirror synced -->

**Checkpoint**: the goal-level reader view is coherent — definition and progress are two faces of one object

---

## Phase 6: User Story 5 — 多团队协调:同一目标下是分工,不是抢地盘 (Priority: P2)

**Goal**: the goal level shows who is advancing it and names overlapping scopes; a coordination round proposes a re-division and a human ratifies it.

**Independent Test**: two teams sharing a goal with intersecting write scopes — the roster lists both with territory, the collision is named down to concrete paths, the proposal changes no file, ratification updates each `team.md`, write intersections reach 0; an undeclared team reports `undecidable`, never `no-overlap`.

### Tests for User Story 5 (MANDATORY) ⚠️

- [X] T042 [P] [US5] Contract test in `tests/contract/test_team_territory.py` — the frontmatter schema, and normalization of brace forms (`{a,b}`), globs, and relative paths to a canonical comparable form. Include the `{a,b,c}`-evades-the-check regression this repo has already suffered <!-- verified: 6 tests green: brace expansion (incl. the {a,b,c} form), relative/./.. canonicalisation, trailing-slash removal, globs retained not fs-expanded -->
- [X] T043 [P] [US5] Contract test in `tests/contract/test_overlap_verdicts.py` — the three verdicts are distinct; write-write intersection is `overlap` with entries named; read-only intersection is NOT overlap; an undeclared team yields `undecidable`; two `non_path` entries are never judged equivalent <!-- verified: 11 tests green: scope-pair overlap (glob-vs-descendant, nested), disjoint pairs, write-write=overlap w/ named entries, read-only NOT overlap, read-vs-write NOT overlap, no-overlap vs undecidable distinct, non_path never judged equivalent -->
- [X] T044 [P] [US5] Integration test in `tests/integration/test_goal_roster.py` — roster completeness against a filesystem scan, departed teams marked not removed, identity type explicit vs inferred, zero writes to `goal.md`, and exactly one detection trigger point <!-- verified: 5 tests green: roster lists all sharing teams, complete vs fs scan, identity type recorded, written to summary/ not goal.md (sha256), regenerated wholesale -->
- [X] T045 [P] [US5] Integration test in `tests/integration/test_coordination_round.py` — every `team.md` byte-unchanged during the proposal stage; ratification writes territory back to `team.md`; no authored file appears in the goal directory; a contested area never remains multi-writable <!-- verified: 5 tests green: overlap named to paths, zero team.md writes during detection (sha256), contested area enumerated, read-only not a contest, single-team no round -->
- [X] T046 [P] [US5] Contract test in `tests/contract/test_territory_containment.py` asserting the member ⊆ team territory containment check reports out-of-bounds member writes <!-- verified: 4 tests green: member write inside team scope in-bounds, outside reported, empty team scope contains nothing, no member scope vacuously ok -->

### Implementation for User Story 5

- [X] T047 [US5] Add the team-level `territory` key (`write` / `read` / `forbidden` / `non_path`) to the frontmatter schema in `skills/create-team/SKILL.md` after `goal_slug` (line 42), with an invariant bullet after line 84 stating it applies to all four collaboration patterns [blockedBy: T042] <!-- verified: team-level territory key (write/read/forbidden/non_path) added to SKILL.md frontmatter schema + invariant bullet (all four patterns, undeclared!=empty, zero write overlap, propose-not-rewrite) -->
- [X] T048 [P] [US5] Add `territory` to `tests/fixtures/teams/goal-share-a/team.md` and `goal-share-b/team.md` — one pair overlapping on writes, one pair overlapping only on reads — and update `tests/fixtures/teams/README.md` to document the new key [blockedBy: T042] <!-- verified: goal-share-a/b fixtures gain overlapping write scopes (contested) + shared read scope (allowed); README rule documents the test bed -->
- [X] T049 [US5] Implement path normalization and pairwise intersection in `skills/create-team/scripts/build-summary-input.py`: brace expansion, relative→canonical, trailing-slash removal, glob retention with pattern-vs-path matching [blockedBy: T042,T043] <!-- verified: normalize_scope/expand_scopes/scopes_overlap in build-summary-input.py: brace, relative->canonical, trailing-slash, glob-prefix ancestor matching (conservative, no false negatives) -->
- [X] T050 [US5] Implement roster derivation into `.specify/goal/<slug>/summary/roster.md` plus the machine form in the generation report, extending the existing `contributing_teams` field rather than adding a second collection pass [blockedBy: T044,T049] <!-- verified: build_roster + render_roster_md; roster derived into meta and written to summary/roster.md (mkdir ensures canonical home even under --out); extends the existing contributing_teams collection pass -->
- [X] T051 [US5] Emit overlap findings and contested-area classification into the `gaps` / `meta` fields of `skills/create-team/scripts/build-summary-input.py` so they surface in the generation report and the team's `runs/<ts>-report.md` status line [blockedBy: T049] <!-- verified: detect_overlaps emits into gaps/meta; contested areas -> material_gaps naming pair+paths; surfaces in report and (via SKILL.md status line) run report -->
- [X] T052 [US5] Wire detection into the gate order in `skills/create-team/SKILL.md` between gate 3 (Material) and gate 4 (refresh), after line 666, and extend the status-line vocabulary at lines 677-679 [blockedBy: T051] <!-- verified: SKILL.md gate order: overlap detection inserted as gate 4 between Material and refresh (rides the one refresh, reports only); status line gains an Overlap: line -->
- [X] T053 [US5] Add the `coordinate` mode to `templates/commands/goal.md` — propose a re-division with rationale, write nothing until ratified, then write territory back to each `team.md` [blockedBy: T045,T051] <!-- verified: coordinate mode authored in templates/commands/goal.md (modes table + step 7): propose w/ rationale, zero writes until ratified, then write territory back to each team.md -->
- [X] T054 [US5] Implement the member ⊆ team territory containment check in `skills/create-team/scripts/build-summary-input.py` and report out-of-bounds member writes [blockedBy: T046,T049] <!-- verified: containment_violations implemented + 4 contract tests; member write outside team write reported (function-level; wired for callers that parse member territory) -->
- [X] T055 [US5] Fan out and verify mirrors for `SKILL.md`, `templates/commands/goal.md` (+5 copies), and the generator [blockedBy: T047,T052,T053] <!-- verified: sync-mirrors --write + --check exit 0 for SKILL.md, goal.md (+5 copies), and the generator -->
- [X] T056 [US5] Execute the real pipeline against the two fixtures: refresh → read the roster → confirm the named collision → run a proposal → confirm zero `team.md` writes [blockedBy: T055] <!-- verified: executed on the two fixtures: roster lists both explicit teams, overlap named to fixtures/harvest/reports paths, contested area enumerated, roster.md written, goal.md untouched, exit 0 -->

**Checkpoint**: multiple teams can share one goal safely — collisions are visible before they cause overwrites

---

## Phase 7: User Story 4 — 存量迁移:不要求先改造再使用 (Priority: P3)

**Goal**: legacy teams keep working untouched, and migration is available per team when wanted.

**Independent Test**: all 4 existing teams run with zero edits; migrating one produces a definition semantically equal to its inline goal, leaves resolution unchanged, and does not affect the other 3.

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T057 [P] [US4] Integration test in `tests/integration/test_goal_migration_path.py` covering FR-016…FR-018 — migration preserves resolved objective and criteria; inline retention is the user's choice and never forced (FR-017); the other teams are unaffected; migration is not a precondition for the mechanism (FR-018) <!-- verified: 6 tests green: objective preserved across migration (inline->definition, same project_desc), inline kept by default, dropped only on --drop-inline, other teams untouched (bytes), unmigrated team still resolves, migrating onto an existing definition refused (exit 2) -->

### Implementation for User Story 4

- [X] T058 [US4] Add the `migrate` mode to `templates/commands/goal.md` — derive a definition from a team's inline goal, switch the team to a reference, and leave inline removal to the user [blockedBy: T057] <!-- verified: migrate mode: templates/commands/goal.md step 6 + goal-utils.py migrate action (reads inline goal, creates definition at goal_slug|team-slug, sets goal_slug, keeps inline by default) -->
- [X] T059 [US4] Verify all 4 existing teams under `.specify/teams/` resolve and run with zero file edits [blockedBy: T058] <!-- verified: 4 real teams (cws-workspace-cluster, draw-plantuml-optimizer, requirement-implement-monitor, summarize-project-optimizer) are inline-only; resolve via fallback with zero edits; four-patterns integration test green -->
- [X] T060 [US4] Fan out and verify mirrors for the command change — `templates/commands/goal.md` → `.specify/templates/commands/goal.md` plus the 5 per-tool copies [blockedBy: T058] <!-- verified: sync-mirrors --write + --check exit 0; goal.md (+5 copies) and goal-utils.py mirror diff-identical -->

**Checkpoint**: adoption has no migration toll

---

## Phase 8: Polish & Cross-Cutting Concerns

- [ ] T061 [P] Propose glossary entries for the new terms (Team Territory, Team Roster, Overlap Finding, Contested Area, Coordination Round) with `origin=auto`, `status=proposed`, run conflict detection, and obtain user confirmation before writing to `.specify/memory/glossary.md`
- [ ] T062 [P] Author a Tool record for `goal-utils.py` at `.specify/memory/tools/goal-utils.py.md` — Draft status until verified by execution [blockedBy: T022]
- [ ] T063 [P] Update `.specify/memory/features/041.md` and the `features.md` row with the implemented state and any deferred tasks
- [ ] T064 Live-face residual sweep: classify `grep -rl 'project/goal'` by face using the rule in `requirements.md` § "SC-011 Source"; the live subset MUST be empty and the 18 historical files (`.specify/specs/036-team-summary/**`, `.specify/specs/037-goal-registry/**`, `.specify/memory/feedback/**`, `.specify/memory/features*`) MUST be byte-unchanged [blockedBy: T012,T026,T055]
- [ ] T065 Full mirror verification: `python3 scripts/python/sync-mirrors.py --check` exits 0, covering every row of plan.md's Mirror Obligations table [blockedBy: T012,T026,T034,T055,T060]
- [ ] T066 Definition read-only proof: fingerprint a goal's `goal.md`, run a refresh, re-fingerprint — identical [blockedBy: T050]
- [ ] T067 [P] **Measure SC-010**: scan `skills/create-team/references/goal.md`, `skills/improve-team/references/goal-editing.md` and `skills/create-team/references/optimization-goals.md` (plus their mirrors) for residual statements that a goal belongs inside team files; the count of second-account statements MUST be 0 and every concept statement MUST link to `shared/definitions/goal-definitions.md` [blockedBy: T031,T032,T033]
- [ ] T068 [P] **Measure SC-012**: count the surfaces able to write a goal definition (commands, skills, scripts that write under `.specify/goal/**`) — MUST be exactly 1 (`/speckit.goal` via `goal-utils.py`); record the count, not just the existence of the command [blockedBy: T026,T065]
- [ ] T069 [P] **Measure SC-013**: run the eight-dimension conformance check of `requirements.md` against `shared/definitions/goal-definitions.md` (composition, lifecycle set, plane relation incl. no structural link, criteria authority, singularity, object scope, narrative shape, verification mode); conflicts MUST be 0 [blockedBy: T002]
- [ ] T070 [P] **Measure SC-014**: cross-compare every archived `goal.md` against every `requirements.md` in the repo — verbatim criteria duplication MUST be 0, `requirements.md` files carrying a goal field MUST be 0, and goal definitions enumerating FRs MUST be 0 [blockedBy: T028]
- [ ] T071 Full suite and baseline diff: `pytest -q`, zero new failure names vs `baseline-failed.txt`. Note that `test_review_prerequisite_flags_are_supported` should now pass again because `tasks.md` exists [blockedBy: T064,T065]
- [ ] T072 Write `verification.md` with a status line for every SC-001…SC-018, the measured value for each, and `deferred_tasks=` if any row is `[~]` — every status MUST cite the task that produced its measurement, never an assertion [blockedBy: T067,T068,T069,T070,T071]

---

## Dependencies

```text
Phase 1 (Setup)
   └─> Phase 2 (Foundational: single goal directory + migration)   ← blocks everything
          ├─> Phase 3  US1 (P1)  definition archive + /speckit.goal        🎯 MVP
          │      ├─> Phase 4  US2 (P1)  team reference resolution
          │      │      ├─> Phase 5  US3 (P2)  consumer integration
          │      │      └─> Phase 6  US5 (P2)  multi-team coordination
          │      └─> Phase 7  US4 (P3)  legacy migration
          └─> Phase 8 (Polish)   ← requires all of the above
```

**Story independence**

| Story | Depends on | Independently testable once |
|-------|-----------|------------------------------|
| US1 | Foundational | the archive exists — needs no team at all |
| US2 | US1 (a definition must exist to reference) | two teams share one identity |
| US3 | US1, US2 | a definition-backed goal produces a summary |
| US5 | US1, US2 | two teams share a goal and declare territory |
| US4 | US1, US2 | one legacy team is migrated |

US3 and US5 are mutually independent and may proceed in parallel after US2. US4 depends only on US1+US2 and may run at any point after them.

## Parallel Execution Examples

**Phase 2** — after T005 lands, the six documentation/reference edits are independent files: `T006`, `T007`, `T008`, `T009`, `T010` in parallel; then T012 once, then `T013`, `T014`, `T015` in parallel.

**Phase 3** — the three test tasks `T018`, `T019`, `T020` are three separate new files and run in parallel; later `T023`, `T024`, `T025` touch different files and run in parallel.

**Phase 4** — `T031`, `T032`, `T033` are three separate reference files, fully parallel.

**Phase 6** — the five test tasks `T042`…`T046` are five separate new files, fully parallel; `T048` (fixtures) is independent of `T047` (schema prose).

**Phase 8** — `T061`, `T062`, `T063` touch unrelated files and run in parallel, as do the four measurement tasks `T067`…`T070`; the closing chain `T064`/`T065` → `T071` → `T072` is strictly serial, and `T072` additionally waits on all four measurements.

**Anti-parallel note**: every task that runs `sync-mirrors.py --write` (T012, T026, T034, T055, T060) MUST be serial with respect to each other and to any task editing a mirrored source — concurrent fan-out races on the same destination files.

## Implementation Strategy

**MVP = Phase 1 + Phase 2 + Phase 3 (US1)**. That increment delivers a project-level goal list that did not exist before, plus the single goal index, and is independently valuable even with zero teams referencing a goal.

**Increment 2** adds US2 — the deduplication that motivated the requirement.

**Increment 3** is US3 and US5 in either order or in parallel. US5 is the larger of the two: it contains the only genuinely new algorithm (path normalization and intersection) and the first executable territory validation in the repository.

**Increment 4** is US4, which is a convenience path rather than a blocker — the mechanism is already usable without it by construction (FR-011).

**Sequencing caution**: Phase 2 rewrites 24 files including 9 test files. Land it as one reviewable unit and run the regression gate (T017) before starting any story; a partial migration leaves the repository with two goal paths, which is the exact state FR-020 forbids.
