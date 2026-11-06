# Tasks: SDD 临时 Goal / 临时 Team 与多 Agent 并发

**Requirement ID**: 085
**Requirement Key**: 085-sdd-temporary-goal-team
**Related Feature**: 085 SDD 临时 Goal / 临时 Team 与多 Agent 并发
**Input**: Design documents from `.specify/specs/085-sdd-temporary-goal-team/`
**Prerequisites**: plan.md, requirements.md, research.md, data-model.md, contracts/

**Tests Mode**: ON — Constitution Principle IV (Test-First & Contract-Driven Implementation) requires red-first behavior groups for every new predicate.

**Organization**: Tasks are grouped by user story so each slice can be implemented and tested independently.

## Definition of Done (DoD)

- DoD-1: Every FR in `requirements.md` has an implementation or an explicit rejection recorded in `verification.md`.
- DoD-2: Every contract clause is claimed by exactly one task row and is closed by its `[green:]` evidence.
- DoD-3: All new and changed tests pass; the pre-change baseline has zero new failed node ids.
- DoD-4: Mirrors, command copies, rendered agents, and the render manifest are regenerated and `--check` clean.
- DoD-5: The dogfood run records a temporary goal, a temporary team, concurrent stage agents, child worktrees, checkpoints, one ratified config change, and one rollback.
- DoD-6: Documentation and the feature registry reflect the final state; dated historical records are unchanged.

**DoD Status**: pending

## Completion Gate

- GATE-1: Full suite has zero NEW failures vs the S0 baseline — check: `scripts/bash/run-tests.sh --names-out .specify/specs/085-sdd-temporary-goal-team/test-evidence/final-failed.txt` and `comm -13 test-evidence/baseline-failed.txt test-evidence/final-failed.txt`.
- GATE-2: Mirror and command copies are clean — check: `python3 scripts/python/sync-mirrors.py --check` and `python3 scripts/python/regen-command-copies.py --check` both exit 0.
- GATE-3: Render manifest and agent cleanup are complete — check: `grep -R "sdd-executor" agents .specify/agents .qoder .claude .github .opencode` returns no live definition; `test_unified_turn_budget.py` passes.
- GATE-4: No open task rows — check: `grep -cE '^- \[[ >]\]' .specify/specs/085-sdd-temporary-goal-team/tasks.md` returns 0; every `final`-path SC has `SC-NNN_status=pass` and the smoke record is present in `verification.md`.

## Environment Prerequisites

- Python 3.8+: available — probe: `python3 --version` @ 2026-11-06; affected phases: all.
- pytest: available — probe: `python3 -m pytest --version` @ 2026-11-06; affected phases: all test phases.
- git: available — probe: `git --version` @ 2026-11-06; affected phases: S4/S8, all integration tests.
- supported host agent: partial — probe: `specify render-agents --help` @ 2026-11-06; affected phases: S6/S8; an unavailable host records `not-evaluated`, never a silent pass.

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 Run S0 preflight: disk, git writability, ignore check, baseline test run and node-id set in `test-evidence/`.
- [X] T002 Create and validate the 085 requirements, plan, research, data-model, contracts, quickstart, and feature-ref artifacts.
- [X] T003 Create the test fixtures and temporary-repo helper used by the scope, temp-goal, temp-team, and child-line tests in `tests/fixtures/temp_sdd_team.py`.

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T004 Add the `Scope` value object and `resolve-scope` action skeleton to `scripts/python/goal-utils.py`, with a unit-test stub for path resolution. [green: contracts/scope-resolution.md#C-001] [green: contracts/scope-resolution.md#C-002] [green: contracts/scope-resolution.md#C-003] [green: contracts/scope-resolution.md#C-004] [green: contracts/scope-resolution.md#C-005] [green: contracts/scope-resolution.md#C-006]

## Phase 3: User Story 6 - Scope-aware Goal and Team commands (Priority: P2)

**Goal**: one deterministic resolver; both commands and all consumers use it.

- [X] T010 [US6] Finish scope resolution: spec-dir validation, auto ambiguity, wrong-scope errors, returned object keys, and legacy global parity in `scripts/python/goal-utils.py`. [green: contracts/scope-resolution.md#C-007] [green: contracts/scope-resolution.md#C-008] [green: contracts/scope-resolution.md#C-009] [green: contracts/scope-resolution.md#C-010] [green: contracts/scope-resolution.md#C-011] [green: contracts/scope-resolution.md#C-012]
- [X] T011 [US6] Wire `--scope`/`--spec-dir` through `templates/commands/goal.md`, `templates/commands/team.md`, `sdd-route.py authorize`, `run-checks`, `create-team`, `run-team`, `improve-team`, and the evidence runs lane; regenerate per-tool copies. [green: contracts/scope-resolution.md#C-013] [green: contracts/scope-resolution.md#C-014]
- [X] T012 [US6] Add `tests/contract/test_scope_resolution.py` and `tests/unit/test_goal_scope_engine.py`, including global/spec/auto, ambiguity, wrong scope, and legacy byte-identical cases.

## Phase 4: User Story 1 - Temporary Goal is authored after requirements (Priority: P1)

**Goal**: a spec-local authored goal, created only after requirements U4.

- [X] T020 [US1] Add the Temporary Goal concept and spec-local storage to `shared/definitions/goal-definitions.md` and `skills/internal/manage-goal/SKILL.md`; default identity = spec basename; lifecycle `active`/`achieved`/`abandoned`; one goal per spec. [green: contracts/temporary-goal-team.md#C-001] [green: contracts/temporary-goal-team.md#C-002] [green: contracts/temporary-goal-team.md#C-003]
- [X] T021 [US1] Implement authored objective/criteria, criteria-disjointness check against `SC-` rows, engine-only writes, and terminal retention in `manage-goal` and `goal-utils.py`. [green: contracts/temporary-goal-team.md#C-004] [green: contracts/temporary-goal-team.md#C-005] [green: contracts/temporary-goal-team.md#C-006]
- [X] T022 [US1] Add `tests/contract/test_temp_goal_contract.py` and the fixture assertions for no-goal-before-requirements, criteria disjointness, resume-reuse, and terminal retention.

## Phase 5: User Story 2 - Temporary Team is created after clarify and plan (Priority: P1)

**Goal**: a spec-local team bound to the temporary goal, with `stage_seats`.

- [X] T030 [US2] Extend `skills/internal/create-team/references/create-mode.md` and `conceptual-model.md` with `scope`, `spec_dir`, `goal_slug`, `lifecycle_state`, `stage_seats`, and the Team Stage disambiguation; add schema validation in `create-team`. [green: contracts/temporary-goal-team.md#C-007] [green: contracts/temporary-goal-team.md#C-008] [green: contracts/temporary-goal-team.md#C-009] [green: contracts/temporary-goal-team.md#C-010] [green: contracts/temporary-goal-team.md#C-011]
- [X] T031 [US2] Add per-stage run reports, in-place archive, global-store containment (`.specify/goal/**`, `.specify/teams/**`), and resume/archived-team behavior in `run-team` and `create-team`. [green: contracts/temporary-goal-team.md#C-012] [green: contracts/temporary-goal-team.md#C-013] [green: contracts/temporary-goal-team.md#C-014] [green: contracts/temporary-goal-team.md#C-015]
- [X] T032 [US2] Add `tests/contract/test_temp_team_schema.py` and `tests/contract/test_stage_seat_map.py`, including seat closure, max_parallel bounds, Stage-dimension non-overload, and archived refusal.

## Phase 6: User Story 3 - Stage-specific agents and declared concurrency (Priority: P1)

**Goal**: more concurrent, focused agents; no generic executor; uniform 500.

- [X] T040 [US3] Add U0 concurrency fields, effective-concurrency resolution, verifier reserve, downgrade reasons, and per-dispatch records to `skills/external/sdd-loop-driver/SKILL.md` and the state spine. [green: contracts/concurrency-and-worktrees.md#C-001] [green: contracts/concurrency-and-worktrees.md#C-002] [green: contracts/concurrency-and-worktrees.md#C-003] [green: contracts/concurrency-and-worktrees.md#C-004] [green: contracts/concurrency-and-worktrees.md#C-005]
- [X] T041 [US3] Remove the generic `sdd-executor` from sources, mirrors, rendered copies, and the render manifest; add the stage role grammar and the user-named roles; set every retained definition and rendered copy to 500 — covers FR-025, FR-029, FR-030. [green: contracts/stage-agents.md#C-001] [green: contracts/stage-agents.md#C-002] [green: contracts/stage-agents.md#C-003] [green: contracts/stage-agents.md#C-004] [green: contracts/stage-agents.md#C-005]
- [X] T042 [US3] Add `tests/contract/test_unified_turn_budget.py`, the agent-cleanup scan, and the concurrency-field tests; update live references in `create-agent`, `run-agent`, `dispatch-recipes`, and the render tests.

## Phase 7: User Story 4 - Per-agent worktrees and the integration queue (Priority: P1)

**Goal**: safe concurrent writes through 064 child lines.

- [X] T050 [US4] Add `parent_line_id`, `line_role`, child worktree/branch, owned/forbidden paths, and depth-1 validation to `skills/external/sdd-loop-driver/scripts/line-registry.py` and the 064 contracts/data-model — covers FR-031, FR-032, FR-033. [green: contracts/concurrency-and-worktrees.md#C-006] [green: contracts/concurrency-and-worktrees.md#C-007] [green: contracts/concurrency-and-worktrees.md#C-008] [green: contracts/concurrency-and-worktrees.md#C-009] [green: contracts/concurrency-and-worktrees.md#C-010]
- [X] T051 [US4] Add `SPECIFY_AGENT_CONCURRENCY_CAP`, child-line exclusion from the root cap, queue reuse, failure/conflict retention, archive/remove/deregister sequence, and no-push behavior — covers FR-034, FR-035, FR-036. [green: contracts/concurrency-and-worktrees.md#C-011] [green: contracts/concurrency-and-worktrees.md#C-012] [green: contracts/concurrency-and-worktrees.md#C-013] [green: contracts/concurrency-and-worktrees.md#C-014] [green: contracts/concurrency-and-worktrees.md#C-015] [green: contracts/concurrency-and-worktrees.md#C-016] [green: contracts/concurrency-and-worktrees.md#C-017] [green: contracts/concurrency-and-worktrees.md#C-018]
- [X] T052 [US4] Add `tests/contract/test_line_registry_child_lines.py` and `tests/integration/test_temp_team_worktree_queue.py`, including deterministic replay, conflict retention, and zero lost commits.

## Phase 8: User Story 5 - Stage checkpoints coordinate verification, goal progress, and team configuration (Priority: P2)

**Goal**: four-part checkpoints at every stage boundary.

- [X] T060 [US5] Add `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` and wire the four-part checkpoint into the driver after U4 and before the next dispatch. [green: contracts/checkpoint-and-agents.md#C-001] [green: contracts/checkpoint-and-agents.md#C-002] [green: contracts/checkpoint-and-agents.md#C-003] [green: contracts/checkpoint-and-agents.md#C-004] [green: contracts/checkpoint-and-agents.md#C-005] [green: contracts/checkpoint-and-agents.md#C-006] [green: contracts/checkpoint-and-agents.md#C-007] [green: contracts/checkpoint-and-agents.md#C-008]
- [X] T061 [US5] Add `tests/contract/test_checkpoint_protocol.py`, including the four mandatory sections, `n/a` discipline, goal degree table, and next-stage concurrency/roster decision.

## Phase 9: User Story 7 - Team configuration improves across stages (Priority: P3)

**Goal**: at most one evidence-driven change per checkpoint, with rollback.

- [X] T070 [US7] Connect the checkpoint proposal to `improve-team`/`/speckit.team modify`, including one-change cap, ratification states, evidence sources, and territory-vs-config separation. [green: contracts/checkpoint-and-agents.md#C-009] [green: contracts/checkpoint-and-agents.md#C-010] [green: contracts/checkpoint-and-agents.md#C-011] [green: contracts/checkpoint-and-agents.md#C-012] [green: contracts/checkpoint-and-agents.md#C-013]
- [X] T071 [US7] Add the rollback drill and the checkpoint proposal/rollback tests in `tests/contract/test_checkpoint_protocol.py` and `tests/integration/test_checkpoint_rollback.py`.

## Phase 10: Polish & Cross-Cutting Concerns

- [X] T080 [P] Regenerate mirrors, command copies, and rendered agents; update docs, the feature registry, and the feature detail; run `sync-mirrors.py --check`, `regen-command-copies.py --check`, and the manifest sha check.
- [X] T081 Run the full suite, the targeted stage checks, and the dogfood run (temporary goal/team, concurrency >1, child worktrees, checkpoints, one ratified change, one rollback); record `verification.md`.
- [X] T082 Run `/speckit.review`: four segments + ARC; land `review.md` and `code-review.md`; register `REC-` ids if any; do not flip status before the code segment completes.

## Dependencies & Execution Order

- Phase 1 → Phase 2 → Phase 3 (scope) → Phases 4–9. Within a story, tests may be written before implementation; the `[P]` markers are on rows that write different files.
- T041 depends on T040 only for the U0 fields; the agent cleanup can proceed in parallel with the concurrency resolver.
- T051 depends on T050; T070 depends on T060; T081 depends on all implementation phases; T082 depends on T081.

## Parallel Opportunities

- T003 and T004 can run in parallel.
- T020/T030/T040/T060 touch different files and can be prepared concurrently once scope is stable.
- T042/T052/T061/T071 are independent test suites and can run in parallel after their implementation rows.

## Implementation Strategy

MVP is Phase 3 + Phase 4 (scope + temporary goal). The next increment is Phase 5 + Phase 6 (temporary team + stage agents). The concurrency increment is Phase 7 (worktrees + queue). Checkpoints and configuration optimization follow. The dogfood and review are the final gate.
