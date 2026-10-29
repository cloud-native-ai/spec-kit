# Tasks: Unified Goal/Team/Agent Control Hierarchy with SDD Invocation

> **SUPERSEDED (2026-10-29)**: This 57-row task list was split at tasks U4 (`split-required`, 57 > 40) into `074a-authorized-routing` (32 tasks) and `074b-nested-governance` (26 tasks). The open rows below are the **pre-split state**, not outstanding work; see `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录. Retained as the split record.

**Requirement ID**: 074
**Requirement Key**: `074-goal-team-sdd-unification`
**Related Feature**: 074 Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation）
**Input**: Design documents from `.specify/specs/074-goal-team-sdd-unification/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md, feature-ref.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is
MANDATORY ("Pure functions/utilities MUST have unit tests", "Integration/contract tests MUST cover
… external APIs"), and the plan's Constitution Check row IV declares six red-first behaviour groups.
No template-only gate applies: the deliverable includes an executable engine
(`scripts/python/sdd-route.py`), so unit and contract layers both have a subject.

**Tests**: When Tests Mode is ON the test rows below are MANDATORY. Every test row is red-first
except the two declared exceptions marked `[blockedBy:]` on their implementation dependency (the
R12 pin change, and the containment/regression cases that can only go green after the consumer code
they exercise has landed — `create-tasks` § Task Generation Rules, migration/regression exception).

**Organization**: Tasks are grouped by user story (requirements.md US1–US5) so each story is
independently implementable and testable. Phase order follows story priority (P1 → P1 → P2 → P2 → P3).

## Definition of Done (DoD)

- DoD-1: All 67 contract clauses (C-1…C-67) are discharged by the row that carries their `[green:]` tag, and `python3 .specify/scripts/python/validate-tasks.py .specify/specs/074-goal-team-sdd-unification/tasks.md` exits 0 on the finished document
- DoD-2: Every new or edited source artifact is a framework-source edit, and every `.specify/` projection is produced by `scripts/python/sync-mirrors.py` or `scripts/bash/generate-instructions.sh`, never hand-edited
- DoD-3: All eight success criteria (SC-001…SC-008) carry a status and a measurement source in `.specify/specs/074-goal-team-sdd-unification/verification.md`
- DoD-4: The 13-file targeted set stays green (pre-change record: 191 passed, `test-evidence/targeted-set-v1-baseline.txt`) and the containment claims are discharged as node-id set containment, never as counts
- DoD-5: The runtime-evidence landing points exist and carry real pasted output: `notes/red-first-evidence.md`, `notes/quickstart-run.md`, `notes/pre-change-measurements.md`, `coverage-baseline.txt`
- DoD-6: No new `/speckit.*` command, skill, registry, ledger, state spine, ownership model, integration queue, scheduler, daemon, confirmation gate, or automatic feedback transmission exists (FR-028, C-63, C-64, C-67)

**DoD Status**: pending

## Completion Gate

- GATE-1: Targeted set plus the six new and one edited contract files has zero NEW failures vs the frozen baseline — check: `python3 -m pytest -q <the 13 baseline files> tests/contract/test_sdd_routing_definitions.py tests/contract/test_sdd_routing_engine.py tests/contract/test_sdd_authorization.py tests/contract/test_sdd_invocation_governance.py tests/contract/test_nested_sdd_invocation.py tests/contract/test_nested_run_report.py tests/contract/test_neutral_metadata_schema.py`
- GATE-2: Every mirror obligation from plan.md is verified byte-identical — check: `python3 scripts/python/sync-mirrors.py --check` exits 0
- GATE-3: No open or claimed task rows remain — check: `grep -cE '^- \[[ >]\]' .specify/specs/074-goal-team-sdd-unification/tasks.md` returns 0
- GATE-4: The task document is structurally valid — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/074-goal-team-sdd-unification/tasks.md` exits 0
- GATE-5: `verification.md` lists every SC-NNN with a status — check: `grep -oE 'SC-00[1-8]' .specify/specs/074-goal-team-sdd-unification/verification.md | sort -u | wc -l` returns 8
- GATE-6: FR coverage stays complete and the clause lane is clean against the frozen baseline — check: `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074-goal-team-sdd-unification` reports `FR uncovered: 0`

## Environment Prerequisites

- Local Python + pytest toolchain: available — probe: `python3 --version && python3 -m pytest --version` → `Python 3.11.11` / `pytest 8.4.2` @ 2026-10-28; affected phases/tasks: every test row (T006, T007, T012, T015, T016, T022, T026, T027, T031, T043, T046, T049, T055), no network, container runtime, cluster, or special hardware dependency exists for this feature

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`[US1]`…`[US5]`); Setup, Foundational and Polish rows carry none
- **[blockedBy: T001,T002]**: this row MUST NOT start until every listed task is `[X]`
- **[green: <contract>#<clause>]**: this row is the one that turns that contract clause green; contracts resolve relative to this file's directory. The 67 clauses are partitioned so each clause is claimed exactly once, in ascending clause order per contract file
- Include exact file paths in descriptions; one task row stays on one line

### Task State Sigil

`- [ ]` open · `- [>]` claimed · `- [X]` closed · `- [~]` deferred (reason recorded in `verification.md` under `deferred_tasks=`)

## Path Conventions

Single project: sources at the repository root (`shared/`, `scripts/`, `skills/`, `templates/`,
`src/`, `tests/`, `agents/`); this feature's design artifacts and runtime evidence under
`.specify/specs/074-goal-team-sdd-unification/`. Every `.specify/` path except the spec directory
is a generated projection and MUST NOT be hand-edited.

---

## Phase 1: Setup

**Purpose**: Create the runtime-evidence landing points and freeze the pre-change baselines that
the later phases measure against.

- [ ] T001 Create the runtime-evidence landing points under `.specify/specs/074-goal-team-sdd-unification/notes/` — `red-first-evidence.md`, `quickstart-run.md`, `pre-change-measurements.md` — each header naming the capture command that fills it
- [ ] T002 Freeze the pre-change test-node-id case set of the 13-file targeted set at baseline commit `6297c14f6` into `.specify/specs/074-goal-team-sdd-unification/notes/pre-change-measurements.md` with `python3 -m pytest --collect-only -q` over those 13 files (contract C-62: a count comparison is non-conforming)
- [ ] T003 Re-measure the committed `.specify/specs/074-goal-team-sdd-unification/coverage-baseline.txt` with `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074-goal-team-sdd-unification` and record both lanes plus the delta in `notes/pre-change-measurements.md`; re-freeze only if the corpus uncovered set moved

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The two artifacts every user story extends — the shared engine shell and the shared
fixture. Neither carries a `[green:]` tag: an engine shell with no action and a fixture with no
assertion turn nothing green.

**⚠️ CRITICAL**: No user story task may start until this phase is complete.

- [ ] T004 Create `scripts/python/sdd-route.py`: a stdlib-only, read-only engine exposing `--action route|authorize|golden` with the exit alphabet `0` (a verdict or a judged finding was produced) / `2` (input error) / `3` (authorization refused), one constant naming the owner document `.specify/shared/definitions/sdd-routing-definitions.md`, no file writes, and no copy of any value domain
- [ ] T005 [P] Create `tests/fixtures/nested_sdd.py`: a temporary repository fixture holding a minimal `.specify/`, one `team.md` with a block-style `seats:` map declaring one `allowed` and one `forbidden` seat, two agent definitions, and one goal with an open Target

**Checkpoint**: engine shell and fixture exist; US1–US5 can now extend them.

---

## Phase 3: User Story 1 — An authorized team member starts a nested SDD run (Priority: P1) 🎯 MVP

**Goal**: An Agent definition capability plus a team seat policy together authorize one bounded
nested SDD run, and the run validates its entry facts before U0 and returns a structured handoff at
review.

**Independent Test**: Build the fixture team (one authorized seat, one unauthorized seat), assign
both the same SDD-routed duty, and confirm the authorized seat resolves to `allowed` and starts
exactly one nested run while the unauthorized seat is refused with the failing half named — then
confirm the returned handoff carries the closed field set and performs no merge or push.

### Tests for User Story 1 (MANDATORY) ⚠️

- [ ] T006 [P] [US1] Author the red-first contract cases in `tests/contract/test_sdd_authorization.py`: agent-half and seat-half resolution, the AND matrix, absent key / absent `seats` / absent entry defaulting to `forbidden`, a flow-style map refused with the seat named, a dangling seat reported, and the refusal naming the failed half with both source paths plus the seat slug
- [ ] T007 [P] [US1] Author the red-first contract cases in `tests/contract/test_nested_sdd_invocation.py`: the six-fact entry form, the six fail-closed conditions, handoff field presence, the three-value outcome alphabet, the four-fact integration identity, zero merge and zero push read from `git log` / `git status`, and the failure/stall handoff

### Implementation for User Story 1

- [ ] T008 [US1] Add `sdd-invocation` to `NEUTRAL_AGENT_METADATA_KEYS` (closed domain `allowed`/`forbidden`, default `forbidden`, `renders_to_tools = False`) and to `NEUTRAL_AGENT_FRAMEWORK_KEYS` in `src/specify_cli/__init__.py` [green: contracts/authorization-and-probe.md#C-15]
- [ ] T009 [P] [US1] Add the `seats:` block map to the persisted `team.md` schema in `skills/internal/create-team/references/create-mode.md`: block style only, flow style refused as malformed input with the seat named, a dangling seat reported rather than ignored, an absent entry resolving to `forbidden`, and no back-fill for existing teams [green: contracts/authorization-and-probe.md#C-16] [green: contracts/authorization-and-probe.md#C-17]
- [ ] T010 [P] [US1] Add `team_slug` and `seat_slug` to the dispatch payload declaration in `shared/definitions/subagent-definitions.md` § Execution Topology Declaration, so the seat policy resolves by (team, seat) instead of by seat alone [green: contracts/authorization-and-probe.md#C-18]
- [ ] T011 [US1] Implement `--action authorize` in `scripts/python/sdd-route.py`: resolve both halves, return `effective` as their AND, name the failing half (`agent` / `seat` / `both`), record both source paths plus the seat slug, exit `3` on refusal and `2` on malformed input [green: contracts/authorization-and-probe.md#C-19] [blockedBy: T004]
- [ ] T012 [US1] Update the declared pin in `tests/contract/test_neutral_metadata_schema.py` so `NEUTRAL_AGENT_FRAMEWORK_KEYS` gains exactly one member, `sdd-invocation`, in the same change as the key (R12; this is the feature's only intentional change to an existing assertion) [blockedBy: T008]
- [ ] T013 [US1] Add § Invoked-from-Team Entry to `skills/external/sdd-loop-driver/SKILL.md`: the six accepted facts (Goal reference, optional Target, team slug, invoking seat, authorized scope, routing verdict reference), the validation table, the stop-at-review boundary, and one Hard Requirement line; the standalone entry contract stays unchanged [green: contracts/nested-invocation.md#C-31] [green: contracts/nested-invocation.md#C-32] [green: contracts/nested-invocation.md#C-33]
- [ ] T014 [US1] Create `skills/external/sdd-loop-driver/references/nested-invocation.md`: the handoff's closed field set, the entry-validation table, the three-value outcome, the four-fact integration identity with the retained branch named, the zero-merge/zero-push rule, registration as one write line in the existing registry, and the failure/stall handoff [green: contracts/nested-invocation.md#C-34] [green: contracts/nested-invocation.md#C-35] [green: contracts/nested-invocation.md#C-36] [green: contracts/nested-invocation.md#C-37] [green: contracts/nested-invocation.md#C-38] [green: contracts/nested-invocation.md#C-39] [green: contracts/nested-invocation.md#C-40] [blockedBy: T013]

**Checkpoint**: US1 is independently testable — the fixture's authorized seat resolves to `allowed`, the unauthorized seat is refused with the failed half named, and the entry form accepts or refuses all six facts.

---

## Phase 4: User Story 2 — A deterministic decision separates SDD from direct modification (Priority: P1)

**Goal**: One owner document plus one deterministic engine settle *whether* a change runs SDD,
with the five declared inputs, one fixed precedence, a closed reason-code vocabulary, and a golden
table every caller can re-judge.

**Independent Test**: Feed the golden table's seven rows to `--action golden` and assert each
documented verdict and reason code; re-run the same inputs and assert byte-identical output; assert
a missing or conflicting input set returns `adjudicate` and never `direct`.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T015 [P] [US2] Author the red-first contract cases in `tests/contract/test_sdd_routing_definitions.py`: the owner declaration and the four facts it owns, the five closed value domains, the Task Complexity Rubric cited rather than copied, the definition-class cross-cutting default with its bounded-correction escape, and the single-declaration-point scan for a second table
- [ ] T016 [P] [US2] Author the red-first contract cases in `tests/contract/test_sdd_routing_engine.py`: determinism, the precedence `adjudicate > sdd > direct`, reason codes, ambiguity and conflict never returning `direct`, identical repeated evaluations, every golden row judged twice, and exit codes `0` (a verdict, including `adjudicate`) / `2` (input error)

### Implementation for User Story 2

- [ ] T017 [US2] Author `shared/definitions/sdd-routing-definitions.md` § Owner declaration, § Hierarchy and boundary, § Direct modification, and § Input domains: the five inputs' closed domains, the prohibition on medium/extension/language/count/author-identity inputs, and the definition-class cross-cutting default [green: contracts/route-decision.md#C-1] [green: contracts/route-decision.md#C-2] [green: contracts/route-decision.md#C-3] [green: contracts/route-decision.md#C-4] [green: contracts/route-decision.md#C-5] [green: contracts/route-decision.md#C-6]
- [ ] T018 [US2] Author § Verdict table, § Precedence, § Conflict set, and § Reason-code vocabulary in `shared/definitions/sdd-routing-definitions.md`: the SDD conditions, the direct conditions, the single fixed precedence with the conflict closed set, and the reason codes in their declared order [green: contracts/route-decision.md#C-7] [green: contracts/route-decision.md#C-8] [green: contracts/route-decision.md#C-9] [green: contracts/route-decision.md#C-10]
- [ ] T019 [US2] Author § Override record and § Per-duty application in `shared/definitions/sdd-routing-definitions.md`: the user instruction verbatim with the overridden verdict retained, and one application per declared member duty reused until an input changes [green: contracts/route-decision.md#C-11] [green: contracts/route-decision.md#C-12]
- [ ] T020 [US2] Implement `--action route` in `scripts/python/sdd-route.py`, reading the domains, verdict table, precedence and reason codes out of `shared/definitions/sdd-routing-definitions.md` at run time and writing no file [green: contracts/route-decision.md#C-13] [blockedBy: T004,T018]
- [ ] T021 [US2] Author § Golden case table in `shared/definitions/sdd-routing-definitions.md` covering the seven required faces and implement `--action golden` judging every row from that table with no second copy in test code or a data file [green: contracts/route-decision.md#C-14] [blockedBy: T020]

**Checkpoint**: US2 is independently testable — every golden row returns its documented verdict and reason code twice identically, and no ambiguous or conflicting input set reaches `direct`.

---

## Phase 5: User Story 3 — Nesting is governed, not escaped (Priority: P2)

**Goal**: The anti-nesting obligation is narrowed once, in place, to a three-condition predicate
enforced fail-closed before dispatch, with the depth-2 chain and the three prohibitions stated
where the obligation lives.

**Independent Test**: Run the pre-dispatch governance probe against four dispatch shapes —
authorized SDD assignment, unauthorized prompt naming a driver, stage executor attempting to load a
driver, and a nested SDD attempt inside a stage — and confirm only the first is dispatched, each
refusal naming the failed condition, while every pre-change case keeps its recorded verdict.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T022 [US3] Author the red-first contract cases in `tests/contract/test_sdd_invocation_governance.py`: the three-condition predicate matrix, the depth-2 chain, the virtual-mode prohibition, the stage-executor refusal, and the per-member cap

### Implementation for User Story 3

- [ ] T023 [US3] Narrow § Dispatch-Time Governance Obligation in `shared/definitions/subagent-definitions.md` to the three-condition predicate (capability `allowed` ∧ seat policy `allowed` ∧ an SDD assignment), keeping the original prohibition unchanged for every dispatch that fails it [green: contracts/authorization-and-probe.md#C-20]
- [ ] T024 [US3] Enforce the predicate fail-closed in the `skills/internal/run-agent/SKILL.md` pre-dispatch probe by calling `scripts/python/sdd-route.py --action authorize` instead of re-reading the definitions in prose, with the refusal naming the condition that failed [green: contracts/authorization-and-probe.md#C-21] [blockedBy: T011,T023]
- [ ] T025 [US3] State the depth-2 chain, the three prohibitions (a stage executor starts nothing, no SDD-inside-SDD, no virtual-mode host) and the per-member cap in the same § Dispatch-Time Governance Obligation, replacing the unqualified "loop depth is always 1" claim [green: contracts/authorization-and-probe.md#C-22] [green: contracts/authorization-and-probe.md#C-23] [green: contracts/authorization-and-probe.md#C-24] [blockedBy: T023]
- [ ] T026 [US3] Extend `tests/contract/test_sdd_invocation_governance.py` with the leaf assertion over `agents/sdd-executor.agent.md`, the hosting-declaration conformance case (three responsibility statements read together with the declaration), the pre-change case-set containment comparison, and the refused-dispatch record assertions [green: contracts/authorization-and-probe.md#C-25] [green: contracts/authorization-and-probe.md#C-26] [green: contracts/authorization-and-probe.md#C-27] [green: contracts/authorization-and-probe.md#C-28] [green: contracts/authorization-and-probe.md#C-29] [blockedBy: T022,T025]

**Checkpoint**: US3 is independently testable — only an authorized SDD assignment is dispatched, every other shape keeps the original prohibition, and the narrowing is provably an addition, not an escape.

---

## Phase 6: User Story 4 — The outer layer consumes the nested result (Priority: P2)

**Goal**: The team run report gains one mandatory nested-SDD section; the invoking Agent carries the
handoff; attribution to a Goal happens only through the existing ledger Target reference; and the
predecessor contracts stay additive.

**Independent Test**: Run the fixture team with one nested SDD run to review, then assert the report's
`## Nested SDD Runs` section exists with every artifact and evidence path, that a blocked/failed run
is never reported as success, that no merge or push happened, and that the parsed Goal field set is
identical before and after.

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T027 [P] [US4] Author the red-first contract cases in `tests/contract/test_nested_run_report.py`: the `## Nested SDD Runs` heading literal, explicit-when-empty, the per-invocation field list, the peer relationship to `## Verification`, supervisor-only writes, exactly one ledger item carrying the existing Target reference, and the parsed Goal field set identical before and after

### Implementation for User Story 4

- [ ] T028 [US4] Add `## Nested SDD Runs` to § Report contract in `skills/internal/create-team/SKILL.md` as a mandatory section listing per invocation the outcome, artifact paths, evidence paths, routing-verdict reference and anomalies, plus the explicit "no nested SDD invocation this run" line [green: contracts/report-and-attribution.md#C-47] [green: contracts/report-and-attribution.md#C-48] [green: contracts/report-and-attribution.md#C-49]
- [ ] T029 [US4] Add the writer, attribution, peer and verdict-reference duties to the same § Report contract: the supervisor is the sole writer, exactly one ledger item carrying the existing Target reference is appended at report time with no new Goal field and no `goal.md` write, the nested section stays a peer of `## Verification` rather than a replacement, and the routing verdict is consumed by reference [green: contracts/report-and-attribution.md#C-50] [green: contracts/report-and-attribution.md#C-51] [green: contracts/report-and-attribution.md#C-52] [green: contracts/report-and-attribution.md#C-53] [green: contracts/report-and-attribution.md#C-54] [blockedBy: T028]
- [ ] T030 [US4] Add the invoking-Agent consumption duty to `skills/internal/create-team/SKILL.md` § Execution (run mode): the handoff is included in the Agent's own result and in the run report verbatim or by stable path, and success is never reported on a `blocked` or `failed` outcome [green: contracts/nested-invocation.md#C-41]
- [ ] T031 [US4] Extend `tests/contract/test_nested_sdd_invocation.py` with the end-to-end acceptance case: one nested run to review, the complete artifact chain, zero merge and zero push, and every artifact and evidence path present in the report section [green: contracts/nested-invocation.md#C-42] [blockedBy: T007,T028]
- [ ] T032 [US4] Verify the Feature 070 stage-team preset contract is additive-unchanged: run its suite and assert no preset key, section, entry form, or exit code was removed, renamed, or re-meant, recording the output in `.specify/specs/074-goal-team-sdd-unification/verification.md` [green: contracts/nested-invocation.md#C-43]
- [ ] T033 [US4] Verify the Feature 058 U0–U6 contract is additive-unchanged: run the driver's stage, sentinel, independent-verification, watcher and stall cases and assert no semantics moved, recording the output in `verification.md` [green: contracts/nested-invocation.md#C-44] [blockedBy: T032]
- [ ] T034 [US4] Add the setup-path entry to the invocation-kind classification in `shared/definitions/sdd-routing-definitions.md`: a target project carrying no `.specify/` structure routes to the setup skill and is never degraded into a direct modification [green: contracts/nested-invocation.md#C-45] [blockedBy: T017]
- [ ] T035 [US4] Add the incomplete-handoff obligation to `skills/external/sdd-loop-driver/references/nested-invocation.md`: a handoff missing its integration identity is incomplete by definition, and the consuming check is a field-presence test over the handoff block, not a prose reading [green: contracts/nested-invocation.md#C-46] [blockedBy: T014]

**Checkpoint**: US4 is independently testable — a completed, a blocked and a failed nested run each produce the required report content, and the Goal layer shows attribution only through the ledger row.

---

## Phase 7: User Story 5 — SDD concepts are diffused without being duplicated (Priority: P3)

**Goal**: Team, Agent and instruction surfaces each gain the minimum vocabulary they need, every
fact reaching its owner by reference, and the team Stage dimension is explicitly disambiguated from
the SDD stage roster.

**Independent Test**: Run the diffusion and contract checks that detect duplicated stage rosters and
unknown keys, and confirm every new surface cites its owner while the team Stage vocabulary is
unchanged.

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T036 [US5] Extend `tests/contract/test_sdd_routing_definitions.py` and `tests/contract/test_sdd_invocation_governance.py` with the diffusion assertions: each new surface cites its owner by path, the team Stage vocabulary is unchanged, and no second copy of the input set, verdict table, or precedence exists

### Implementation for User Story 5

- [ ] T037 [US5] Disambiguate the Stage dimension in `skills/internal/create-team/references/conceptual-model.md`: executor/evaluator/optimizer is not the SDD stage roster, the roster stays owned by the driver, and no team Stage value is renamed or overloaded [green: contracts/diffusion-and-compat.md#C-55]
- [ ] T038 [US5] Add exactly one pointer-level routing ambient section to `templates/instructions-template.md`: when a write-bearing change is proposed, run the decision at `.specify/shared/definitions/sdd-routing-definitions.md`, with no input set, no verdict table, and no second copy of the precedence [green: contracts/diffusion-and-compat.md#C-56] [blockedBy: T017]
- [ ] T039 [P] [US5] Add the promotion-conjunction pointer sentence to `shared/guidelines/proactive-trigger.md`: promotion to an SDD run requires both a routing verdict of the SDD kind and an effective authorization of `allowed`, stated once in the routing owner and reached from here [green: contracts/diffusion-and-compat.md#C-57]
- [ ] T040 [US5] Add § Invocation kinds to `shared/definitions/sdd-routing-definitions.md`: the driver, framework bootstrap, periodic maintenance and direct modification as four distinct kinds, with the same effective-authorization predicate applying when the setup or house-keeping skill dispatches subagents [green: contracts/diffusion-and-compat.md#C-58] [green: contracts/diffusion-and-compat.md#C-59] [blockedBy: T017]
- [ ] T041 [P] [US5] Add `sdd-invocation` to the § Authoring Baseline supported-field list in `skills/internal/run-agent/SKILL.md` as a pointer to the key set's owner, so an authored instance can declare it and a validator rejects a value outside the closed set [green: contracts/diffusion-and-compat.md#C-60]

**Checkpoint**: US5 is independently testable — every diffused surface cites its owner and no surface duplicates a table, a threshold, or the stage roster.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Mirror and generator projections, the containment discharge, the negative structural
checks, and the evidence sweeps that close the feature.

- [ ] T042 [P] Sync every edited source to its projection with `python3 scripts/python/sync-mirrors.py --write --only <source prefix>` for plan.md § Mirror Obligations rows 1–5 (`shared/`, `skills/internal/`, `skills/external/`, `scripts/`, `templates/`), never hand-editing a `.specify/` copy
- [ ] T043 Verify the mirror obligations byte-identically with `python3 scripts/python/sync-mirrors.py --check`, enumerating rows 1–5 of plan.md § Mirror Obligations and requiring zero drift against the measured-clean baseline
- [ ] T044 Regenerate `.specify/instructions.md` with `bash scripts/bash/generate-instructions.sh`, then assert the new routing section heading is present, no existing section was rewritten, and record the byte delta against the declared per-section ceiling (the file was already 41,948 B over the 32,768 B budget before this feature) [blockedBy: T038,T042]
- [ ] T045 Assert the CLI neutral-key single definition point with `grep -c 'sdd-invocation' src/specify_cli/__init__.py`, and keep `tests/contract/test_tool_mapping.py` and `tests/contract/test_neutral_metadata_schema.py` green (plan.md § Mirror Obligations row 7) [blockedBy: T008]
- [ ] T046 Discharge both containment claims by comparing the frozen pre-change node-id set in `notes/pre-change-measurements.md` with the post-change collected set: superset relation plus identical verdicts for the shared ids, never a count comparison [green: contracts/diffusion-and-compat.md#C-61] [green: contracts/diffusion-and-compat.md#C-62]
- [ ] T047 Negative check over the changed tree: no automatic merge or push, no scheduler or daemon, no automatic feedback transmission, no second confirmation gate, and no scheduler or second registry behind the authorization surface — its only stored state stays the two declared values [green: contracts/authorization-and-probe.md#C-30] [green: contracts/diffusion-and-compat.md#C-63]
- [ ] T048 Structure check over the changed tree: no second registry, ledger, state spine, ownership model, or integration queue, and the nested run's records resolve to the existing line entry and state spine [green: contracts/diffusion-and-compat.md#C-64]
- [ ] T049 Run the pre-dispatch governance suite and assert every pre-change case returns its recorded verdict, so an undeclared Agent definition or Team seat still resolves to `forbidden` [green: contracts/diffusion-and-compat.md#C-65]
- [ ] T050 Roster check over the added text: no SDD stage-name enumeration, no duplicated roster, and no second team Stage vocabulary [green: contracts/diffusion-and-compat.md#C-66]
- [ ] T051 Delivered-file-set check: no new `/speckit.*` command and no new skill — `python3 scripts/python/flow-class-check.py --action check` stays at 79 units with zero findings [green: contracts/diffusion-and-compat.md#C-67]
- [ ] T052 Execute quickstart scenarios S1–S6 against the delivered artifacts and paste each real command output and exit code into `.specify/specs/074-goal-team-sdd-unification/notes/quickstart-run.md` with its teardown [blockedBy: T021,T024]
- [ ] T053 Collect the red-first evidence for every new test file into `.specify/specs/074-goal-team-sdd-unification/notes/red-first-evidence.md`: the command, the real output, and the exit status of each pre-implementation run [blockedBy: T006]
- [ ] T054 Run the clause-coverage accounting against the frozen baseline and record both lanes (FR and clause) with the measured delta in `notes/pre-change-measurements.md` [blockedBy: T003]
- [ ] T055 Run the 13-file targeted set plus the six new and one edited contract file, and record command, selection basis, selected paths, pass/fail counts, and any new failure against the frozen baseline in `verification.md` [blockedBy: T026,T031]
- [ ] T056 Review the Feature list per the Feature Integration Protocol: confirm `.specify/memory/features.md` and `.specify/memory/features/074.md` still describe Feature 074 accurately, and update them synchronously only if the breakdown exposed a new or invalidated feature
- [ ] T057 Confirm the plan's "no `templates/commands/**` change" claim and that `python3 scripts/python/regen-command-copies.py --check` stays clean [blockedBy: T042]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies — starts immediately
- **Foundational (Phase 2)**: depends on Setup; BLOCKS every user story (US1 extends the engine shell from T004 and the fixture from T005)
- **User Stories (Phases 3–7)**: each depends on Foundational; each is independently testable
- **Polish (Phase 8)**: depends on every story it verifies; T042–T045 need the story edits landed, T046–T051 need the tests landed

### User Story Dependencies

- **US1 (P1)**: after Foundational; no dependency on another story
- **US2 (P1)**: after Foundational; independent of US1, but US1's entry form validates a verdict reference that only US2 produces — this is why the MVP covers both P1 stories
- **US3 (P2)**: after Foundational; consumes US1's `--action authorize` (T011), so T024 is blocked on it
- **US4 (P2)**: after Foundational; consumes US1's entry form and handoff (T013, T014) and US2's owner document (T017)
- **US5 (P3)**: after Foundational; diffuses US1's key and US2's owner document into the team, Agent and instruction surfaces

### Within Each User Story

- Tests first and red before implementation (T006/T007, T015/T016, T022, T027, T036)
- The two declared exceptions run after their dependency: T012 after T008 (pin change), T026/T031 after the code they exercise (containment and regression cases)
- Documents before the engine action that reads them: T017–T019 before T020, T020 before T021
- Story complete before the next priority

### Parallel Opportunities

- T004 ∥ T005 (engine shell vs fixture)
- T006 ∥ T007 (two different test files)
- T008 ∥ T009 ∥ T010 (CLI key set, team schema, payload declaration — three different files)
- T015 ∥ T016 (two different test files)
- T039 ∥ T041 (trigger discipline vs authoring baseline)
- T042 alone in its step; T043–T051 each read the tree, so they serialize only on their recorded evidence file

---

## Parallel Example: User Story 1

```text
# Launch both red-first test files together:
Task: "Author tests/contract/test_sdd_authorization.py (agent half, seat half, AND matrix, defaults)"
Task: "Author tests/contract/test_nested_sdd_invocation.py (six facts, entry validation, handoff)"

# Then the three independent single-file edits:
Task: "Add sdd-invocation to src/specify_cli/__init__.py"
Task: "Add the seats: block map to skills/internal/create-team/references/create-mode.md"
Task: "Add team_slug/seat_slug to shared/definitions/subagent-definitions.md § Execution Topology Declaration"
```

## Parallel Example: User Story 2

```text
Task: "Author tests/contract/test_sdd_routing_definitions.py (owner shape, closed domains, one declaration point)"
Task: "Author tests/contract/test_sdd_routing_engine.py (determinism, precedence, golden rows, exit codes)"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: **US1 + US2** — both are P1, and neither is independently valuable in the delivered
sense: US1's entry form validates a routing verdict reference (`verdict_ref`, contract C-31/C-32)
that only US2's decision can produce, so authorization without routing would be a mechanism with no
input, and routing without authorization would decide a path nobody may start. Every other story is
P2/P3 and is independently testable on top of this pair.

1. Complete Phase 1: Setup (evidence landing points and frozen baselines)
2. Complete Phase 2: Foundational (engine shell + fixture) — BLOCKS all stories
3. Complete US1 then US2
4. **STOP and VALIDATE**: run each story's checkpoint independently against the fixture
5. Continue with US3 → US4 → US5, then Polish

### Incremental Delivery

1. US1 → the hierarchy gains an authorized nested path with a structured handoff
2. US2 → the "when is it SDD" question becomes one deterministic verdict
3. US3 → the narrowing is governed and provably additive
4. US4 → the outer layer owns the result and the integration decision
5. US5 → the vocabulary diffuses without a second copy
6. Polish → mirrors, generated instructions, containment, and structural negatives

### Parallel Team Strategy

Two workers can take US1 and US2 concurrently after Foundational (different files, one shared engine
file sequenced by `[blockedBy:]`); US3–US5 then run concurrently except where the table above records
a dependency.

---

## Assumptions & Clarifications

- **A1 (stage scope)**: This stage produces `tasks.md` only. No implementation row is executed here; `/speckit.checklist`, `/speckit.analyze` and `/speckit.implement` are dispatched by the orchestrator, not by this stage.
- **A2 (input classification)**: The dispatch brief arrived as background context plus the stage command — no task outline and no additional task entries — so the breakdown follows requirements.md's user stories as the primary structure.
- **A3 (test-file population)**: Six new contract test files plus one declared pin edit. `plan.md` § Scale/Scope and § Structure Decision used to say "7 new test files" / "seven test files are new", which contradicts the enumerated delivery surface (`plan.md` § Source Code lists six `NEW` files, `feature-ref.md` § 2 rows 13–18 list six, `research.md` R14 states "six new … test files", and every contract's "Pinned by" line resolves to that same six). The count phrases were corrected to six as a line-level consistency fix; the enumeration and the contract pins govern.
- **A4 (clause partition)**: The 67 clauses are partitioned across rows so that each clause is claimed exactly once and, within one contract file, the claimed ordinals ascend with row order. Where the contract's "Pinned by" line names two test files, the green point is the row that lands the artifact or the test group the clause describes, not the row that merely runs the suite.
- **A5 (coverage baseline timing)**: `.specify/specs/074-goal-team-sdd-unification/coverage-baseline.txt` was frozen during this stage, after the `[green:]` claims existed (plan.md § Phase 1 records that it must not freeze before any claim exists). T003 re-measures it rather than freezing a second time.
- **A6 (no environment dependency)**: This feature needs only the local Python/pytest toolchain, recorded once in § Environment Prerequisites; no docker daemon, network image, cluster, or special hardware is involved, so no task is `[~]`-eligible on environment grounds.
- **A7 (pre-change baseline commit)**: The containment claims' pre-change case sets are captured at `6297c14f6` (the plan-stage commit, which equals `approved_baseline_commit`); the plan's `feature-ref.md` § 6 names `7831bb4bb` as the freeze point, and the verification record names whichever commit the implementation actually freezes at — the two are reconciled in `verification.md` rather than silently.
- **A8 (no shipped preset)**: R9 governs — FR-023 is implemented as a conditional conformance rule plus a negative assertion over `agents/sdd-executor.agent.md`; no new shipped Agent preset is created.
