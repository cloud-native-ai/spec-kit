# Requirements Specification: SDD 临时 Goal / 临时 Team 与多 Agent 并发

**Requirement Branch**: `085-sdd-temporary-goal-team`
**Created**: 2026-11-06
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "SDD 临时 Goal / 临时 Team 与多 Agent 并发：SDD 启动后先执行 requirements，再据其产出创建附着在 spec 上的临时 Goal；clarify+plan 后创建临时 Team。临时 Goal/Team 存放在 .specify/specs/<NNN-slug>/goal 与 team 下，可随时调整，完成后归档。每个 SDD 阶段使用阶段专用 agent 角色（如 sdd-requirement-analyzer、sdd-plan-coordinator、sdd-plan-executor），按阶段负载和并发度动态决定数量与类型。SDD 启动时设置并发度（默认 24），写 agent 使用独立 worktree 与集成队列。每阶段设置 checkpoint 协同并优化 team 配置。删除泛化 sdd-executor，所有框架 agent 的 run-turn-budget 统一为 500。"

## Related Feature *(mandatory)*

**Feature ID**: 085
**Feature Name**: SDD 临时 Goal / 临时 Team 与多 Agent 并发（SDD Temporary Goal/Team and Multi-Agent Concurrency）

## Overview

This feature integrates the Goal and Team mechanisms into the SDD development flow in the direction the user specified: **the SDD flow is the outer container, and the temporary Goal/Team are attached to its spec**. After the `requirements` stage produces the requirement set, the SDD orchestrator authors a **Temporary Goal** under `.specify/specs/<NNN-slug>/goal/`. After `clarify` and `plan` settle the design, it creates a **Temporary Team** under `.specify/specs/<NNN-slug>/team/`, whose roster and concurrency drive the remaining stages. Both are adjustable at any time and are retained in place when the run completes.

The temporary hierarchy is deliberately separate from the global hierarchy established by Feature 074:

```text
Global hierarchy (unchanged):  Global Goal → Global Team → Agent → SDD run
Temporary hierarchy (new):     SDD run → Temporary Goal → Temporary Team → stage agents
```

The global rules stay intact: no SDD run may create, rebind, re-scope, or terminate a **Global** Goal/Target/Team/roster. The temporary carve-out is spec-local and run-scoped; global stores (`.specify/goal/**`, `.specify/teams/**`) remain read-only to the run and are declared forbidden paths in its Ownership Manifest.

The core efficiency objective is **more concurrent, stage-specific agents doing useful SDD work**, not a fixed roster. Every SDD startup declares a concurrency degree (default 24). The driver resolves an effective concurrency per stage from the declared value, host capability, ready work packages, verifier reserve, and resource isolation; requested and effective values are always recorded, and downgrades are explicit. Writing agents get one git worktree each; their commits are serialized through the existing line registry and integration queue. At every stage boundary a checkpoint records artifact verification, temporary-goal progress, one proposed team-configuration change, and the next stage's concurrency/roster decision.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Temporary Goal is authored after requirements (Priority: P1)

An SDD run starts with a concurrency declaration but no Goal or Team. It executes `requirements` with one stage-specific analyzer. When the requirements stage passes U4, the orchestrator authors a Temporary Goal whose objective is the run's end state (not a task list and not a copy of the specification's success criteria), writes it through the goal engine under the spec directory, and records the goal slug in the run's state spine.

**Why this priority**: Without the temporary goal there is no run-scoped north star for later checkpoints and no way to measure goal progress by degree.

**Independent Test**: Run a fixture SDD flow through `requirements` with no goal present; assert that no `.specify/goal/` path is created, a `goal/goal.md` appears under the spec only after U4, and the authored criteria do not duplicate any `SC-` row.

**Acceptance Scenarios**:

1. **Given** an SDD run whose spec directory has no temporary goal, **When** the requirements stage passes U4, **Then** the orchestrator authors `goal/goal.md` through the goal engine and records the temporary goal slug in the state spine.
2. **Given** an authored temporary goal, **When** its criteria are inspected, **Then** they are degree-measured end-state criteria and are not verbatim or mechanical copies of the requirements specification's success criteria.
3. **Given** a resumed run whose temporary goal already exists, **When** the run re-enters at a later stage, **Then** it validates and reuses the existing goal and does not recreate it.

---

### User Story 2 - Temporary Team is created after clarify and plan (Priority: P1)

After `clarify` and `plan` pass U4, the orchestrator creates a Temporary Team bound to the temporary goal. The team declares a `stage_seats` map for the eight canonical SDD stages, a concurrency target, and an isolation mode. The team's own Stage dimension remains executor/evaluator/optimizer; the SDD stage axis exists only in `stage_seats`.

**Why this priority**: The team is the execution structure that turns the remaining stages into coordinated multi-agent work.

**Independent Test**: Run a fixture through `clarify` and `plan`; assert that no team exists before plan U4, a `team/team.md` appears after plan U4, its `goal_slug` resolves to the temporary goal, and every `stage_seats` key is a canonical SDD stage.

**Acceptance Scenarios**:

1. **Given** a run that has passed `clarify` and `plan`, **When** plan U4 passes, **Then** `team/team.md` is created under the spec directory and bound to the temporary goal.
2. **Given** a persisted temporary team, **When** its frontmatter is parsed, **Then** `scope: spec`, `spec_dir`, `goal_slug`, `lifecycle_state`, `stage_seats`, and `config.agent_concurrency` are present and internally consistent.
3. **Given** a stage key outside the eight canonical stages, **When** `stage_seats` is validated, **Then** the team write is rejected and the offending key is named.

---

### User Story 3 - Stage-specific agents and the declared concurrency drive execution (Priority: P1)

Each SDD stage uses stage-specific agents rather than one generic executor. The number and type of agents are implementation details chosen per stage: `requirements` starts with one analyzer; `plan` may use a coordinator plus several plan executors; `tasks`, `implement`, and `review` may run up to the effective concurrency. The run records the requested concurrency (default 24), the effective concurrency, and the reason for any downgrade on every dispatch.

**Why this priority**: This is the core value: more concurrent, focused agents shorten the SDD wall-clock while preserving independent verification.

**Independent Test**: Run a fixture with a declared concurrency of 24 and enough independent packages; assert that at least one stage dispatches more than one agent concurrently, the requested/effective values are recorded, and a host that cannot support 24 records a named downgrade rather than silently running serially.

**Acceptance Scenarios**:

1. **Given** a new SDD run with no explicit concurrency, **When** U0 records the entry declaration, **Then** the requested concurrency is 24 and the effective value is resolved per stage.
2. **Given** a stage with more ready packages than the effective concurrency, **When** dispatch runs, **Then** at most the effective number of executors run concurrently and the rest wait.
3. **Given** a host that cannot issue the requested concurrency, **When** the driver resolves the effective value, **Then** it records a named downgrade reason and never claims the requested concurrency was achieved.

---

### User Story 4 - Writing agents use independent worktrees and the integration queue (Priority: P1)

A writing agent executes in its own git worktree and branch, writes only its declared territory, and never commits into another agent's worktree. When its output is verified, the integration queue rebases it onto the run target and merges it in the deterministic order declared by the work-package plan. A conflict, a missing output, or a failed gate preserves the worktree and evidence and stops that entry without producing a partial deliverable.

**Why this priority**: Concurrent writes are the risky half of concurrency; worktree isolation and a single integration queue are what make 24-way execution safe.

**Independent Test**: Run a fixture with two or more writing agents in separate worktrees; assert distinct branches and worktrees, deterministic merge order, zero lost commits, zero Git index corruption, and no push.

**Acceptance Scenarios**:

1. **Given** two writing agents with disjoint territories, **When** both are dispatched, **Then** each runs in its own worktree and branch and their commits are integrated in the declared order.
2. **Given** a rebase conflict during integration, **When** the queue processes that entry, **Then** it records a failed integration result, preserves the worktree and evidence, and does not produce a partial stage deliverable.
3. **Given** a completed child line, **When** integration succeeds, **Then** the runtime records are archived, the worktree is removed only after a merged result, and the child line is deregistered.

---

### User Story 5 - Stage checkpoints coordinate verification, goal progress, and team configuration (Priority: P2)

At every stage boundary the driver runs a four-part checkpoint: artifact verification, temporary-goal progress by degree, at most one team-configuration proposal with ratification, and the next stage's concurrency/roster decision. The checkpoint is written under the spec and is committed by the driver.

**Why this priority**: Without checkpoints, concurrency has no coordination point and team configuration cannot improve across stages.

**Independent Test**: Run a fixture through two stage boundaries; assert each checkpoint file carries all four sections, contains at most one configuration change, and the next stage's dispatch reflects the recorded concurrency/roster decision.

**Acceptance Scenarios**:

1. **Given** a stage U4 pass, **When** the checkpoint runs, **Then** it writes artifact verification, a criterion/degree/evidence table, one proposal decision, and the next stage's concurrency/roster decision.
2. **Given** a checkpoint whose proposal is not ratified, **When** the next stage starts, **Then** the team configuration is unchanged and the checkpoint records the non-ratification.
3. **Given** a checkpoint where a prior configuration change caused a U4 failure or a large efficiency drop, **When** the next checkpoint runs, **Then** it records the rollback and does not re-propose the same change immediately.

---

### User Story 6 - Existing goal/team commands operate on both scopes; the generic executor is removed (Priority: P2)

`/speckit.goal` and `/speckit.team` can operate on Global and Temporary scopes through one deterministic resolver. The generic `sdd-executor` agent is removed from sources, mirrors, rendered copies, and the render manifest; stage-specific agents replace it. Every retained framework agent carries a turn budget of 500, and every rendered host copy carries the corresponding `maxTurns`/`steps` value.

**Why this priority**: Scope-aware commands make the temporary hierarchy usable day to day; removing the generic agent and unifying budgets removes the two sources of drift the user identified.

**Independent Test**: Invoke read and write operations on global and spec scopes; assert path resolution and ambiguity errors. Assert that no `sdd-executor` definition remains and every retained definition and rendered copy carries 500.

**Acceptance Scenarios**:

1. **Given** both a global and a temporary goal with the same identity, **When** a read command runs without an explicit scope, **Then** it reports scope ambiguity and names both candidates.
2. **Given** an explicit `--scope spec --spec-dir <path>`, **When** `/speckit.goal` or `/speckit.team` writes, **Then** only the spec-local store is touched.
3. **Given** the cleaned tree, **When** sources, mirrors, render manifest, and rendered agent copies are scanned, **Then** no `sdd-executor` remains and every retained agent carries the unified budget.

---

### User Story 7 - Team configuration improves across stages (Priority: P3)

The checkpoint proposals use the work-package reports, team run reports, and ledger to detect a symptom and propose at most one change: raise or lower concurrency, add or remove a seat, adjust a stage's maximum parallelism, or change the pattern. A ratified change is applied through the existing team-modification path; a regression triggers rollback.

**Why this priority**: It turns concurrency from a static startup number into an evidence-driven configuration search.

**Independent Test**: Run a fixture where a stage shows low parallelism efficiency; assert a proposal is produced, ratified, applied, and the next stage's dispatch reflects the change; then inject a regression and assert rollback.

**Acceptance Scenarios**:

1. **Given** low parallelism efficiency and idle ready packages, **When** the checkpoint proposes a change, **Then** the proposal names the evidence and the exact configuration delta.
2. **Given** a ratified change that causes a U4 failure or a large efficiency drop, **When** the next checkpoint runs, **Then** the change is rolled back and recorded.

---

### Edge Cases

- The spec directory is absent or outside `.specify/specs/`: a `spec`-scope operation fails with a named error and does not fall back to global.
- Both global and temporary identities exist and no scope is given: the read command reports ambiguity; a write command refuses until a scope is chosen.
- A resumed run already has a temporary goal or team: the run validates and reuses it; it never recreates or overwrites it.
- A temporary team is archived: `run-team` refuses it; an explicit modify-and-reactivate path exists.
- The host supports fewer concurrent agents than requested: the effective value is downgraded and recorded; the run never claims the requested value.
- The disk cannot support another worktree: worktree creation fails fast with a named anomaly; it does not silently reuse or delete another worktree.
- Two writing agents declare overlapping territories: the plan gate rejects the overlap or routes it to the integration order; overlapping writes are never dispatched as if independent.
- A child integration fails: the worktree and evidence are retained; the stage gate fails; no partial deliverable is produced.
- A global Goal/Team would be touched by a temporary-scope write: the write is refused and the global store remains byte-identical.
- The generic `sdd-executor` is still referenced by a test, doc, or render manifest: the cleanup is incomplete and the change is not accepted.

## Requirements *(mandatory)*

### Functional Requirements

**A. Temporary Goal**

- **FR-001**: The framework MUST define a **Temporary Goal** as a spec-attached, run-scoped authored end-state definition that uses the same three-part composition, identity grammar, lifecycle, and engine as a Global Goal, and MUST persist it at `.specify/specs/<NNN-slug>/goal/goal.md`. The concept MUST be owned in `shared/definitions/goal-definitions.md`; this feature cites that owner and does not restate its composition rules.
- **FR-002**: The SDD orchestrator MUST author the Temporary Goal only after the `requirements` stage passes U4, and MUST write it through the goal engine with the `spec` scope. It MUST NOT create the goal before requirements, and it MUST NOT mechanically copy any `SC-` row into the goal criteria.
- **FR-003**: A Temporary Goal MUST carry the lifecycle states `active`, `achieved`, and `abandoned`; a terminal goal MUST be retained under the spec and MUST NOT be deleted as a lifecycle transition.
- **FR-004**: One spec MUST have at most one Temporary Goal by default; its identity MUST default to the spec directory basename and MUST be unique within the spec scope. A deliberate re-scope MAY use a suffixed identity, but the engine MUST refuse a duplicate.
- **FR-005**: A Temporary Goal MAY carry optional Targets as scope slices; Targets MUST NOT be used to express stage order or dependency edges. A goal without Targets MUST behave exactly as a goal with an empty Target set.

**B. Temporary Team**

- **FR-006**: The framework MUST define a **Temporary Team** as a spec-attached, run-scoped persisted roster and configuration that uses the same team schema, create/run/improve machinery, and report contract as a Global Team, and MUST persist it at `.specify/specs/<NNN-slug>/team/team.md`. The concept MUST be owned in `skills/internal/create-team/references/conceptual-model.md`.
- **FR-007**: The SDD orchestrator MUST create the Temporary Team only after both `clarify` and `plan` pass U4, and MUST bind it to the Temporary Goal.
- **FR-008**: A Temporary Team `team.md` MUST carry `scope: spec`, `spec_dir`, `goal_slug`, an optional `lifecycle_state` (absent means active), a `stage_seats` block map, and a `config.agent_concurrency` record. These keys MUST be additive to the existing team schema and MUST NOT change the meaning of existing keys.
- **FR-009**: `stage_seats` MUST be keyed only by the eight canonical SDD stages, and every seat listed MUST resolve to a roster member. Each stage entry MUST carry a positive `max_parallel` that does not exceed the run's effective concurrency.
- **FR-010**: The Team's own `Stage` dimension MUST remain `executor` / `evaluator` / `optimizer`; no SDD stage name may be used as a Team Stage value. The SDD stage axis MUST exist only in `stage_seats`.
- **FR-011**: A Temporary Team MUST be adjustable at any time through the team modification path, MUST write a run report for each stage run under `team/runs/`, and MUST be archived in place at completion.

**C. Scope-aware Goal and Team commands**

- **FR-012**: `goal-utils.py` MUST expose a read-only `resolve-scope` action that returns the resolved scope, spec directory, goal root, team root, team definition path, and goal definition path for `global`, `spec`, or `auto`.
- **FR-013**: The path rule MUST be: global uses `.specify/goal` and `.specify/teams`; spec uses `<spec-dir>/goal` and `<spec-dir>/team`. A spec directory MUST be under `.specify/specs/`; an absent or invalid spec directory MUST fail with exit 2 and a named reason.
- **FR-014**: `/speckit.goal` and `/speckit.team` MUST accept `--scope` and `--spec-dir` and MUST route their read and write operations through the same resolver. Existing global behavior without these flags MUST remain byte-identical.
- **FR-015**: Read operations MUST default to `auto`; write operations MUST require an explicit scope. `auto` MUST resolve only when exactly one candidate exists; when both exist, it MUST fail with a named ambiguity error instead of preferring one.
- **FR-016**: `goal-utils.py run-checks`, `sdd-route.py authorize`, `create-team`, `run-team`, `improve-team`, and the evidence runs lane MUST use the same scope resolution and MUST NOT implement a second path rule.
- **FR-017**: A wrong-scope identity MUST fail with exit 3 and a hint naming the other scope; no operation may silently fall back from spec to global or from global to spec.

**D. SDD flow integration and concurrency**

- **FR-018**: The SDD U0 entry declaration and state spine MUST carry `temp_scope_spec_dir`, `temp_goal_slug`, `temp_team_slug`, `agent_concurrency_requested` (default 24), `agent_concurrency_effective`, `agent_concurrency_reason`, `verifier_reserve`, `write_isolation`, `checkpoint_last`, and `checkpoint_pending_proposal`.
- **FR-019**: The effective concurrency MUST be resolved per stage as the minimum of the requested value, the declared or observed host parallel capacity, the stage's `max_parallel`, the ready executor package count plus verifier reserve, and the available resource capacity. A non-declared host capacity MUST be recorded as `host-capacity-undeclared`; an observed failure MUST halve the effective value with a recorded reason and a floor of 1.
- **FR-020**: The `requirements` stage MUST default to one stage-specific analyzer; after U4 the orchestrator MUST author the Temporary Goal and record its slug.
- **FR-021**: The `clarify` and `plan` stages MAY use one to several stage-specific agents; after plan U4 the orchestrator MUST create the Temporary Team and record its slug.
- **FR-022**: The `tasks`, `implement`, and `review` stages MUST scale their stage agents according to the effective concurrency and the ready work packages; `implement` MUST use the per-agent worktree mode when it dispatches more than one writing agent.
- **FR-023**: Temporary-team mode MAY enable decomposition for `requirements` and `tasks` through the run-scoped spine declaration; the Feature 070 built-in defaults MUST remain unchanged, and the benefit test MUST still decide whether a stage is decomposed.
- **FR-024**: The SDD run's Ownership Manifest MUST declare `.specify/goal/**` and `.specify/teams/**` as forbidden paths, and every child manifest MUST inherit them. A temporary-scope write MUST NOT modify either global store.

**E. Stage-specific agents and turn budgets**

- **FR-025**: The generic `agents/sdd-executor.agent.md` MUST be removed from the source tree, the `.specify/agents/templates/` mirror, every rendered host copy, and `.specify/agents/.render-manifest.json`. The `sdd-requirements-executor` instance MUST be replaced by a stage-specific requirements agent.
- **FR-026**: The framework MUST use a role grammar rather than a fixed roster: an optional stage coordinator, one or more stage workers (analyzer, executor, or reviewer), one or more independent stage verifiers, and one stage integrator. The grammar MUST apply to all eight canonical stages.
- **FR-027**: The role names for the stages the user named MUST be `sdd-requirement-analyzer` for requirements, `sdd-plan-coordinator` for plan coordination, and `sdd-plan-executor` for plan work packages; the remaining stages MUST follow the same `<stage>-<role>` grammar.
- **FR-028**: The number and type of agents per stage MUST be an implementation detail decided by the work-package benefit test, the effective concurrency, the ready package count, and the checkpoint evidence; no fixed per-stage count may be asserted as a contract.
- **FR-029**: Every retained framework agent definition MUST carry `run-turn-budget: 500`, and every rendered host copy MUST carry the corresponding `maxTurns: 500` or `steps: 500`. Synthetic fixtures that test rendering are exempt.
- **FR-030**: The live references to the removed generic agent in `create-agent`, `run-agent`, the SDD driver, `dispatch-recipes`, and the affected contract tests MUST be updated; dated records under `.specify/state/` and `.specify/memory/evidence/` MUST NOT be rewritten.

**F. Per-agent worktree and integration queue**

- **FR-031**: Each SDD run MUST register one coordinator line, and each writing agent MUST register a child line with its own worktree and branch.
- **FR-032**: A child line MUST carry `parent_line_id` and `line_role=agent-write`; the parent MUST exist, MUST NOT itself be a child, and the nesting depth MUST be exactly one.
- **FR-033**: A child worktree MUST be created under `.specify/.tmp/sdd-loop/worktrees/<child_line_id>`, MUST use branch `line/<child_line_id>`, MUST declare the package's `owned_paths`, and MUST inherit the run's `forbidden_paths`.
- **FR-034**: Child lines MUST be excluded from the root-line `SPECIFY_LINE_CONCURRENCY_CAP` count and MUST be governed by a separate `SPECIFY_AGENT_CONCURRENCY_CAP` with a default of 24 per parent.
- **FR-035**: Child integration MUST use the existing line registry and integration queue: rebase, targeted quality gate, fast-forward merge, integration record, runtime archive, worktree removal only after a merged result, and deregistration. The order MUST be the work-package plan's declared integration order, never dispatch timing.
- **FR-036**: A failed integration MUST retain the worktree and evidence, MUST record a failed result with a reason, MUST NOT produce a partial stage deliverable, and MUST NOT push.

**G. Checkpoints and configuration optimization**

- **FR-037**: After every stage U4 and before the next dispatch, the driver MUST run a four-part checkpoint: artifact verification, temporary-goal progress by degree, at most one team-configuration proposal with ratification, and the next stage's concurrency/roster decision.
- **FR-038**: The checkpoint MUST be written as `.specify/specs/<NNN-slug>/checkpoints/<NN>-<stage>.md`; a final `closure.md` MUST record the terminal goal degree table and the team's archived state.
- **FR-039**: Goal progress MUST be recorded as `criterion / degree / evidence_ptr`; goal content MUST change only through the goal engine, never through a checkpoint write.
- **FR-040**: A checkpoint MUST apply at most one configuration, concurrency, or roster change. The change MUST be ratified according to `checkpoint_policy.ratification` and applied through the existing team-modification path; an explicit human goal edit does not count toward the one-change cap.
- **FR-041**: The proposal MUST consume existing evidence only: the work-package report, the team run report, and the ledger. It MUST detect one named symptom and propose one exact delta from the closed candidate space in the plan.
- **FR-042**: A ratification-triggered change MUST be rolled back at the next checkpoint if U4 fails, new test failures appear, package retries increase by at least two, or parallelism efficiency drops by at least 30 percent; a rolled-back change MUST NOT be re-proposed immediately.

**H. Compatibility, safety, and verification**

- **FR-043**: The global hierarchy MUST remain unchanged. The only hierarchy amendment is an explicit spec-local Temporary Goal/Team carve-out in `shared/definitions/sdd-routing-definitions.md`; no global Goal/Target/Team/roster write may be authorized by it.
- **FR-044**: Feature 070's `shared-tree` write mode and every pinned literal MUST remain the default and unchanged; the worktree isolation mode MUST be additive and opt-in for temporary-team runs.
- **FR-045**: Feature 064's root-line behavior, ownership model, and integration queue MUST remain unchanged for entries without the new child fields; all child-line fields MUST be optional and additive.
- **FR-046**: The implementation MUST run a disk-space preflight before creating worktrees and MUST surface an out-of-space condition as a named fast-fail anomaly rather than a silent retry or a deletion of another worktree.
- **FR-047**: The implementation MUST add contract, unit, and integration coverage for scope resolution, temporary-goal lifecycle, temporary-team schema and `stage_seats`, checkpoint protocol, global-store containment, child-line worktrees and integration queue, and the unified turn budget.
- **FR-048**: The implementation MUST pass an end-to-end dogfood run that exercises a temporary goal, a temporary team, more than one concurrent stage agent, at least one writing agent in a child worktree, all stage checkpoints, one ratified configuration change, one rollback drill, and terminal goal/team archival.
- **FR-049**: The implementation MUST regenerate every mirror and command copy and MUST pass `sync-mirrors.py --check`, `regen-command-copies.py --check`, and the render-manifest checks.
- **FR-050**: The implementation MUST update the feature registry, the command/skill documentation, and the SDD driver documentation; it MUST NOT rewrite dated historical records.

### Key Entities

- **Temporary Goal**: A spec-attached, run-scoped authored end-state definition with degree-measured criteria and an `active`/`achieved`/`abandoned` lifecycle.
- **Temporary Team**: A spec-attached persisted roster and configuration bound to one Temporary Goal, carrying `stage_seats`, a concurrency target, and an isolation mode.
- **Scope Resolution**: The deterministic mapping from `global`/`spec`/`auto` to goal and team roots, owned by `goal-utils.py`.
- **Stage Seat Map**: The `stage_seats` block map from each canonical SDD stage to its seats and maximum parallelism.
- **Agent Concurrency**: The requested and effective number of concurrently running stage agents, with a verifier reserve and named downgrade reasons.
- **Child Line**: A write agent's line registry entry with a parent line, own worktree and branch, owned paths, and an integration dependency set.
- **Checkpoint**: The per-stage record of artifact verification, goal degree, one configuration proposal, and the next stage's concurrency/roster decision.

### Runtime Stack & Dependency Ownership

本特性交付的运行时能力是临时 Goal/Team 的 scope 解析、SDD 并发调度、child line 工作树/集成队列，以及阶段 agent 的渲染与统一预算；其余项由外部供给、本仓只消费，按 `signed-contract` 记。该表是 SC-004、SC-005、SC-007、SC-010 的运行时前提。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | Python 3 解释器（运行契约/单元/集成测试与确定性检查） | signed-contract | CPython 上游（本仓只消费） | `requires-python >= "3.8"`（`pyproject.toml` 已声明，不新增 pin） | `pyproject.toml` | 新增与改动的测试在 `>=3.8` 解释器上通过；新增脚本 stdlib-only | FR-047 | EP-001 |
| RS-002 | pytest（守卫测试运行器） | signed-contract | pytest 上游（本仓只消费） | 无声明 pin；执行时以 `pytest --version` 原文记录进 test-evidence | `scripts/bash/run-tests.sh` | 基线差集为空且新增守卫测试全绿 | FR-047 | EP-001 |
| RS-003 | 环境级 line registry 与集成队列（含 child line、worktree、agent 并发上限） | in-scope | 本仓 `skills/external/sdd-loop-driver/scripts/line-registry.py` | 同一提交 | `skills/external/sdd-loop-driver/scripts/line-registry.py` | SC-005 | FR-031, FR-032, FR-033, FR-034, FR-035, FR-036 | EP-001 |
| RS-004 | 阶段 agent 渲染与 `run-turn-budget` → `maxTurns`/`steps` 映射 | in-scope | 本仓 `src/specify_cli/__init__.py` | 同一提交 | `src/specify_cli/__init__.py` | SC-007 | FR-025, FR-029, FR-030 | EP-001 |
| RS-005 | 受支持的 agent 宿主（加载并执行阶段 agent） | signed-contract | 各受支持 agent 工具上游（本仓只消费） | 无声明 pin；执行时以宿主名 + 版本原文记录进 test-evidence | `docs/reference/cli/supported-agent-tools.md` | SC-010 | FR-022, FR-029 | EP-002 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A global/spec/auto scope fixture resolves every documented case; ambiguous and wrong-scope cases return the documented named errors and never fall back across scopes. **Path**: final
- **SC-002**: A fixture SDD run creates no temporary goal before requirements U4, creates exactly one after U4, and its criteria do not duplicate any `SC-` row. **Path**: final
- **SC-003**: A fixture SDD run creates no temporary team before plan U4 and creates exactly one bound team after plan U4; every `stage_seats` key is a canonical stage and every seat resolves to a roster member. **Path**: final
- **SC-004**: A fixture run declares concurrency 24 and records a requested/effective pair and a named reason on every dispatch; at least one stage dispatches more than one agent concurrently, and a constrained host records a downgrade instead of claiming 24. **Path**: final
- **SC-005**: A two-or-more writing-agent fixture produces distinct child worktrees and branches, integrates in the declared order, loses zero commits, corrupts zero Git indexes, and performs zero pushes. **Path**: final
- **SC-006**: Every stage checkpoint carries all four sections, contains at most one configuration change, and the next stage's dispatch reflects the recorded concurrency/roster decision; a regression drill records a rollback. **Path**: final
- **SC-007**: After cleanup, no `sdd-executor` definition remains in sources, mirrors, rendered copies, or the render manifest; every retained framework agent carries 500, and every rendered copy carries the corresponding budget value. **Path**: final
- **SC-008**: A temporary-scope write leaves `.specify/goal/**` and `.specify/teams/**` byte-identical. **Path**: supporting
- **SC-009**: Feature 070's legacy shared-tree mode and Feature 064's root-line behavior produce no new failures against the pre-change baseline. **Path**: supporting
- **SC-010**: The dogfood run completes the full stage chain with a temporary goal, a temporary team, concurrent stage agents, child worktrees, checkpoints, one ratified change, one rollback, and terminal archival. **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: Contract tests under `tests/contract/` driving `goal-utils.py resolve-scope`, `/speckit.goal`, `/speckit.team`, and `sdd-route.py authorize`; store the command, exit code, and JSON output in the feature's `test-evidence/`.
- **SC-002 Source**: Fixture run and `goal-utils.py parse_goal` output before and after requirements U4; compare criterion rows against the requirements `SC-` rows.
- **SC-003 Source**: Fixture run and parsed `team.md` frontmatter; `stage_seats` closure test.
- **SC-004 Source**: State-spine fields and dispatch events from the fixture run; `wp-report.py` output.
- **SC-005 Source**: Child line registry entries, `git worktree list`, `git log`/`git status` before and after integration, and the integration queue report.
- **SC-006 Source**: Checkpoint files and the following stage's dispatch records; rollback drill record.
- **SC-007 Source**: Source/mirror/render scans, `.render-manifest.json` sha checks, and the unified-budget contract test.
- **SC-008 Source**: Before/after hashes of `.specify/goal/**` and `.specify/teams/**` in a temporary-scope fixture.
- **SC-009 Source**: Pre-change baseline node-id set and the post-change run of the 070/064 contract suites.
- **SC-010 Source**: The dogfood run report, checkpoint files, integration records, and terminal goal/team state.

## Boundary and Ownership (non-duplication)

| Concern | Existing owner | This feature's relationship |
|---------|----------------|-----------------------------|
| Goal composition, identity, lifecycle, Targets | `shared/definitions/goal-definitions.md` | Adds the Temporary Goal variant by reference; does not restate the composition rules |
| Goal engine and path | `scripts/python/goal-utils.py` | Adds scope resolution and spec-local roots; keeps global behavior |
| Team conceptual model, schema, patterns, run reports | `skills/internal/create-team/` | Adds `stage_seats` and spec-local persistence; keeps the Stage dimension and global schema |
| Goal/Team command entry | `templates/commands/goal.md`, `templates/commands/team.md` | Adds `--scope`/`--spec-dir`; keeps existing modes |
| SDD hierarchy and routing | `shared/definitions/sdd-routing-definitions.md` | Adds the spec-local temporary carve-out; keeps the global prohibition |
| Work packages, stage-team preset, ledger | Feature 070 (`skills/external/sdd-loop-driver/`) | Adds worktree isolation mode and requirements/tasks rules; keeps shared-tree default |
| Lines, worktrees, ownership, integration queue | Feature 064 (`line-registry.py`, contracts) | Adds optional child-line fields; keeps root-line behavior |
| Agent definitions and rendering | `agents/`, `.specify/agents/`, `src/specify_cli/__init__.py` | Removes the generic executor, adds stage agents, unifies the budget |
| Checkpoints, goal summary, config proposals | `improve-team`, `manage-goal coordinate`, `wp-report.py` | Reuses their proposal/ratification and metrics shapes; adds no optimizer engine |

## Assumptions

- **A1**: The user's explicit design decisions are authoritative: Temporary Goal/Team are spec-attached and created after requirements/plan; the global hierarchy stays unchanged; the default concurrency is 24; the per-agent worktree + integration queue model is chosen; all retained agent budgets are 500.
- **A2**: The host may not support 24 concurrent agents. The requested value is a target; the effective value is resolved and recorded, and a downgrade is a legitimate outcome rather than a failure.
- **A3**: The existing 070 shared-tree mode and 064 root-line behavior are the compatibility baseline; the new mode is additive and opt-in for temporary-team runs.
- **A4**: A temporary goal is authored by the orchestrator from the requirements and design context; it is not mechanically derived from `SC-` rows and does not create a structural link from `requirements.md`.
- **A5**: A temporary team has exactly one team per spec in the default flow; multiple runs append reports and checkpoints rather than creating new team directories.
- **A6**: The disk preflight is a hard gate; a worktree allocation that cannot fit is surfaced, not worked around by deleting another agent's worktree.
- **A7**: Historical records (`.specify/state/`, `.specify/memory/evidence/`, dated review/feedback entries) are immutable inputs to this feature; only live references and live definitions are edited.

## Out of Scope

- Changing the global Goal/Team lifecycle, ownership, or store layout beyond the additive scope resolver.
- Authorizing an SDD run to create or rebind a Global Goal/Target/Team/roster.
- A guaranteed 24-way concurrency on every host; the effective value is resolved and may be lower.
- Automatic merge or push by the driver, a child line, or a checkpoint.
- A new scheduler, daemon, evaluation service, or second registry/ledger/state spine.
- Rewriting dated historical records, evidence archives, or prior feature specs.
- Making every stage use a fixed number or type of agents; the roster is dynamic by design.

## Clarifications

### Session 2026-11-06

- Q: Where should the Goal and Team be created? → A: They are attached to the SDD flow, not the global hierarchy. The Temporary Goal is authored after requirements; the Temporary Team is created after clarify + plan. Both live under `.specify/specs/<NNN-slug>/goal/` and `team/`, and both can be adjusted at any time. Existing `/speckit.goal` and `/speckit.team` operate on both global and temporary scopes.
- Q: What is the lifecycle granularity? → A: One Temporary Goal/Team per SDD feature/run, archived and retained at completion.
- Q: How many agents per stage? → A: Eight stages each have stage-specific agents; the number and type vary with the flow and concurrency. Requirements starts with one; tasks/implement may launch many concurrent agents.
- Q: What is the turn-budget policy? → A: All retained framework agent definitions and rendered copies are unified to 500.
- Q: What is the write-concurrency model? → A: Each writing agent gets an independent worktree and branch; integration is serialized through the existing line registry and integration queue.
- Q: What happens to the generic `sdd-executor`? → A: It is removed. Stage-specific roles replace it, following the coordinator/worker/verifier/integrator grammar.
- Q: What is the default concurrency? → A: 24 at SDD startup, with a requested/effective record and honest downgrade.
