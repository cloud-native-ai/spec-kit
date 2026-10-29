# Requirements Specification: Unified Goal/Team/Agent Control Hierarchy with SDD Invocation

**Requirement Branch**: `074-goal-team-sdd-unification`
**Created**: 2026-10-28
**Status**: Draft
**Input**: User description: "需要将speckit框架中goal -> team -> agent 和 sdd-loop-driver (SDD开发流程) 这两条实习一个功能的路径进行统一, 其中goal team agent这条线要高于sdd这条线, 当我们run 一个 team的时候 这个team中的某些agent可以通过调用sdd-*技能进一步启动sdd开发流程. 要完成这一点,就需要SDD开发流程和sdd-*技能的理念扩散到整个 goal team agent体系中, 也需要有明确的定义什么时候使用sdd开发,什么时候直接进行修改."

## Related Feature *(mandatory)*

**Feature ID**: 074
**Feature Name**: Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation）

## Overview

The framework currently offers two parallel ways to deliver a change: the top-level
Goal → Team → Agent chain (goal management, team orchestration, single-agent dispatch) and
the standalone SDD development flow (`sdd-loop-driver`, U0–U6). They meet only at one narrow
point — the driver-owned stage-team preset introduced by Feature 070 — and that bridge runs
*inside* the driver; the Goal/Team layer never learns that an SDD flow exists, and an SDD run
never knows which Goal or Target it is advancing.

This feature makes the relationship explicit and hierarchical: **Goal → Team → Agent is the
top-level control chain; an SDD run is a subordinate execution path that an authorized team
member may start.** It adds (a) an agent capability plus team-seat policy that together
authorize an SDD invocation, (b) a deterministic routing decision that settles when a change
runs through SDD and when it is a direct modification, (c) a governed nested-invocation
contract that narrows — without deleting — the existing anti-nesting obligation, and (d) a
reported, auditable handoff that carries the nested run's artifacts and outcome back to the
Goal/Team layer. Concept ownership stays where it already lives: this feature references the
SDD stage roster, the Goal/Target model, the Team model, and the line/ownership primitives;
it does not re-create them.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - An authorized team member starts a nested SDD run (Priority: P1)

A team is running against a bound Goal and Target. One seat's agent definition declares
that it may host an SDD run, and the team roster permits that seat to do so. When the seat
receives a duty whose routing verdict is SDD, it starts an SDD run for the declared scope,
keeps the outer team informed, and returns a handoff when the run reaches review.

**Why this priority**: This is the value the feature exists to deliver — the two delivery
paths become one hierarchy instead of two disconnected workflows.

**Independent Test**: Build a fixture team with one authorized seat and one unauthorized
seat, assign both the same SDD-routed duty, and confirm the authorized seat starts a nested
run while the unauthorized seat is blocked with the failed predicate named.

**Acceptance Scenarios**:

1. **Given** an agent definition with [[STR-001]] set to [[STR-002]] and a roster seat with
   the same policy, **When** an SDD-routed duty is assigned, **Then** the seat starts exactly
   one nested SDD run for the declared Goal/Target and scope.
2. **Given** an agent definition without the capability or a seat policy of [[STR-003]],
   **When** the same duty is assigned, **Then** no SDD run starts and the rejection names
   which half of the authorization failed.
3. **Given** a nested run that reaches review, **When** it returns, **Then** the handoff
   carries its artifact and evidence paths and performs no merge or push.

---

### User Story 2 - A deterministic decision separates SDD from direct modification (Priority: P1)

Before an agent writes, it classifies the proposed change against declared inputs and gets a
verdict: run SDD, modify directly, or adjudicate. The verdict is produced by one deterministic
engine, records the inputs and the matched reason, and cannot return "direct" when the change
is feature-scale, cross-cutting, irreversible, traceability-bound, or Complex/High-stakes.

**Why this priority**: Without an unambiguous rule, every agent invents its own threshold and
the hierarchy produces inconsistent behaviour. This is the "明确的定义" the user asked for.

**Independent Test**: Feed a golden table of representative changes (feature, maintenance,
cross-cutting, irreversible, ambiguous, bounded definition correction) to the routing engine
and assert each documented verdict and reason code; repeat the same inputs and assert
identical verdicts.

**Acceptance Scenarios**:

1. **Given** a feature-scale or irreversible change, **When** routing runs, **Then** the
   verdict is [[STR-004]] with the triggering inputs recorded.
2. **Given** a bounded, reversible maintenance change with no traceability need, **When**
   routing runs, **Then** the verdict is [[STR-005]] and the change proceeds under the
   applicable quality and confirmation gates.
3. **Given** a missing or conflicting input, **When** routing runs, **Then** the verdict is
   [[STR-006]] and never [[STR-005]].
4. **Given** an explicit user instruction that differs from the verdict, **When** the change
   proceeds, **Then** the override is recorded as an adjudication with the user's instruction
   and the overridden verdict.

---

### User Story 3 - Nesting is governed, not escaped (Priority: P2)

The existing anti-nesting obligation forbids any dispatch prompt from naming a driver skill.
This feature narrows that prohibition to a decidable predicate: only an agent that declares
the capability, whose seat policy allows it, and that is receiving an SDD assignment may host
a driver. Stage executors remain leaves and can never start a driver; an SDD run cannot
contain another SDD run; every other dispatch keeps the original prohibition.

**Why this priority**: The previous invariant exists because an ungoverned second driver
escapes the hierarchy. Removing it wholesale would reintroduce that defect; narrowing it to a
checked predicate is what makes the new capability safe.

**Independent Test**: Run the pre-dispatch governance probe against four dispatch shapes —
authorized SDD assignment, unauthorized prompt naming a driver, stage executor attempting to
load a driver, and a nested SDD attempt inside a stage — and confirm only the first is
dispatched.

**Acceptance Scenarios**:

1. **Given** an authorized seat receiving an SDD assignment, **When** the pre-dispatch probe
   runs, **Then** the dispatch is allowed and the authorization basis is recorded.
2. **Given** any dispatch whose recipient lacks either half of the authorization, **When** a
   prompt names an SDD driver, **Then** the dispatch is blocked before it leaves and the
   failed condition is named.
3. **Given** an SDD stage executor, **When** it attempts to start or host an SDD run, **Then**
   the attempt is refused and reported as an anomaly.
4. **Given** two authorized seats whose territories overlap, **When** both attempt an SDD run
   concurrently, **Then** the runs are serialized or one is rejected, and the decision cites
   the existing line/ownership mechanism.

---

### User Story 4 - The outer layer consumes the nested result (Priority: P2)

A nested run ends at review and hands back its outcome, artifacts, evidence, and any
unresolved review findings. The invoking agent and the team run report surface that handoff
verbatim or by stable path; a blocked or failed nested run can never be reported as success;
the Goal layer sees the contribution observationally, attributed through the existing ledger
Target reference, with no new mandatory Goal field.

**Why this priority**: "Goal/Team above SDD" is only real if the upper layer owns the result
and the decision to merge. Without the handoff the hierarchy is nominal.

**Independent Test**: Run a fixture team with one nested SDD run to review; inspect the team
run report and the Goal archives, and assert the nested section, the evidence paths, the
absence of merge/push, and the absence of any new Goal field.

**Acceptance Scenarios**:

1. **Given** a nested run that completes review, **When** the team run report is written,
   **Then** it contains the nested-SDD section with outcome [[STR-007]], artifact paths, and
   evidence paths.
2. **Given** a nested run that is blocked or fails, **When** the invoking agent reports,
   **Then** the report carries [[STR-008]] or [[STR-009]] and the outer run is not marked
   successful.
3. **Given** a nested run attributed to a Target, **When** the goal archive is inspected,
   **Then** attribution appears only through the existing ledger reference and no new
   mandatory Goal field exists.

---

### User Story 5 - SDD concepts are diffused without being duplicated (Priority: P3)

Goal, Team, Agent, and instruction surfaces each gain the minimum vocabulary they need to
reason about SDD: the team report can describe a nested run, agent definitions can declare
the capability, the instructions can point at the routing rule, and the team's own Stage
dimension is explicitly disambiguated from SDD stages. Every fact is referenced from its
existing owner rather than copied.

**Why this priority**: Diffusion is what makes the hierarchy usable day to day, but it
delivers value only after the invocation, routing, and governance slices exist.

**Independent Test**: Run the documentation/contract checks that detect duplicated stage
rosters and unknown keys, and confirm every new surface cites its owner and the team Stage
vocabulary is unchanged.

**Acceptance Scenarios**:

1. **Given** the team conceptual model, **When** SDD stages are discussed, **Then** the model
   states that its Stage dimension is not the SDD stage roster and no value is renamed.
2. **Given** the project instructions, **When** an agent considers a write-bearing change,
   **Then** the instructions point at the routing owner and do not restate its input set or
   verdict table.
3. **Given** an agent definition that hosts SDD, **When** it is validated, **Then** it
   declares the capability and states that it hosts the driver, never executes stage commands
   itself, and ends at review.

---

### Edge Cases

- **Seat allows, agent lacks the capability** (or the reverse): effective authorization is the
  AND of both halves; the run is refused and the report names the failing half.
- **Terminal Goal or terminal/closed Target**: no nested run may start; the invocation is
  refused with the goal-engine verdict, never silently re-scoped.
- **Target project lacks a `.specify/` structure**: route to the setup path; the framework
  MUST NOT degrade an SDD-routed change into a direct modification.
- **Two authorized seats, overlapping territory**: the existing line registry and ownership
  mechanism decide serialization or rejection; no second concurrency mechanism is introduced.
- **Review returns unresolved findings**: the nested run repairs within its own loop; if it
  cannot, it returns a failed handoff carrying the findings, and the outer layer adjudicates.
- **Stall, timeout, or budget exhaustion**: the nested run stops, persists its state spine, and
  returns a failed handoff with the required elements; the outer team's failure isolation and
  reporting apply.
- **The invoking agent is itself a stage executor of another run**: refusal; a stage executor
  is a leaf by definition.
- **A member executed in virtual mode attempts to host SDD**: refused before dispatch; virtual
  execution would merge the orchestrating session with the driver.
- **The seat has no [[STR-011]] entry**: the policy resolves to [[STR-003]]; the run is refused
  even when the Agent declares [[STR-002]].
- **A duty's inputs change after its verdict**: the routing decision is re-applied; the earlier
  verdict is retained in the record and the new verdict supersedes it.
- **The handoff lacks its integration identity**: the outer layer cannot integrate; the handoff
  is incomplete and the run MUST NOT be reported successful.
- **A declared input is knowingly misclassified** (e.g. a feature reported as maintenance):
  the deterministic engine cannot detect a dishonest declaration; the review surface audits
  the classification and records the discrepancy. The engine's determinism is over declared
  inputs, not over the truthfulness of the declaration.
- **User explicitly directs the opposite path**: user authority wins; the override is recorded
  as an adjudication.

## Requirements *(mandatory)*

### Functional Requirements

**Control hierarchy and vocabulary**

- **FR-001**: The framework MUST define one control hierarchy in which the Goal is the highest
  layer, a Team bound to one Goal orchestrates Agent members, an Agent executes a duty, and an
  SDD run is a subordinate execution path an authorized Agent may start. No SDD run may
  create, rebind, re-scope, or terminate a Goal, Target, Team, or roster.
- **FR-002**: The framework MUST define direct modification as executing a change without an
  SDD artifact chain while remaining subject to every applicable quality and confirmation
  gate, and MUST distinguish it from an SDD run in the routing owner document.

**Authorization**

- **FR-003**: An Agent definition MUST be able to declare SDD invocation capability through the
  neutral metadata key [[STR-001]], whose closed values are [[STR-002]] and [[STR-003]]; an
  absent key means [[STR-003]]. The key is framework-level and MUST NOT be rendered to any
  host tool.
- **FR-004**: A Team roster seat MUST be able to declare SDD invocation policy through the same
  key [[STR-001]] with the same closed values, stored as a `team.md` frontmatter map under the
  key [[STR-011]] keyed by seat slug; an absent seat entry or key means [[STR-003]]. The
  dispatch payload MUST carry the team slug, and the authorization probe MUST resolve the
  policy by (team, seat). Effective authorization is the logical AND of the Agent capability
  and the seat policy; an SDD run MUST NOT start unless the effective value is [[STR-002]].
- **FR-005**: The existing anti-nesting obligation MUST be narrowed to a decidable predicate: a
  dispatch prompt may name or assign an SDD driver only when the recipient resolves to an Agent
  definition declaring [[STR-002]], its seat policy declares [[STR-002]], and the assigned
  task is an SDD assignment. Every dispatch that does not satisfy all three conditions keeps
  the original prohibition. The pre-dispatch probe MUST enforce the predicate and fail closed,
  naming the condition that failed.
- **FR-006**: The permitted nesting chain MUST be depth 2: team orchestrator → invoking member
  (driver host) → stage executor (leaf). A member executed in virtual mode MUST NOT host an SDD
  run, because virtual execution occupies the orchestrating session and collapses the outer
  layer into the driver. A stage executor MUST NOT start or host any SDD run; an SDD stage
  executor MUST NOT itself be an SDD invocation host; SDD-within-SDD recursion is prohibited.
  A member MUST host at most one SDD run at a time; no higher per-member cap escape exists.
  The anti-nesting owner document MUST be amended to
  state this depth-2 chain and the virtual prohibition; FR-005 is the closed form of that
  amendment.

**Routing decision**

- **FR-007**: The framework MUST provide one authoritative routing decision that classifies a
  write-bearing change as [[STR-004]] (run the SDD flow), [[STR-005]] (direct modification),
  or [[STR-006]] (adjudicate), implemented by a deterministic engine that returns the same
  verdict for the same inputs.
- **FR-008**: The decision MUST consume declared inputs only: change nature, whether durable
  traceability is required, blast radius, reversibility, and the existing Task Complexity
  Rubric tier. Each input MUST have a closed value domain defined in the routing owner
  document. It MUST NOT use implementation medium, file extension, language, artifact count,
  or author identity. Changes to definition-class surfaces (constitution, instructions,
  Agent/Skill/Team definitions, and templates that generate them) are treated as cross-cutting
  by default.
- **FR-009**: The decision MUST return [[STR-004]] when any of the following holds: the change
  adds or alters a capability or contract; durable traceability is required; the blast radius
  is cross-cutting; the change is irreversible or hard to reverse; or the complexity tier is
  Complex or High-stakes.
- **FR-010**: The decision MUST return [[STR-005]] only when all of the following hold: the
  change preserves every existing capability and contract; no durable traceability is
  required; the blast radius is local; the change is reversible; the complexity tier is
  Trivial or Standard; and, for a definition-class surface, the change is declared a bounded
  correction with a recorded rationale.
- **FR-011**: The decision MUST apply one fixed precedence: [[STR-006]] first, then
  [[STR-004]], then [[STR-005]]. It MUST return [[STR-006]] whenever a required input is
  missing or ambiguous or the inputs conflict; otherwise it MUST return [[STR-004]] if any
  FR-009 condition holds; it MUST return [[STR-005]] only if all FR-010 conditions hold. The
  definition-class cross-cutting default applies only in the non-adjudicate branch. It MUST
  NOT silently default to [[STR-005]]. Every verdict MUST carry its inputs and a reason code
  from a closed vocabulary owned by the routing owner document.
- **FR-012**: An explicit user instruction overrides the verdict; the override MUST be recorded
  as an adjudication containing the user's instruction and the overridden verdict. The engine
  MUST NOT override the user.
- **FR-013**: The decision MUST be applied once per declared member duty before that duty
  performs a write-bearing change; the verdict is reused for that duty until one of its inputs
  changes. The verdict with its inputs and reason code MUST be recorded in the team run report
  or the Agent execution evidence, consumable by the outer layer.
- **FR-014**: The routing rule MUST have exactly one authoritative owner document at
  `shared/definitions/sdd-routing-definitions.md`, which owns the input value domains, the
  verdict table, the precedence, and the reason-code vocabulary. The driver's own entry-routing
  guidance, the project instructions, team and Agent guidance, and tests MUST reach that owner
  by reference and MUST NOT restate its input set, thresholds, or verdict table.

**Nested invocation contract**

- **FR-015**: `sdd-loop-driver` MUST support an invoked-from-team entry form that accepts the
  bound Goal reference, an optional Target, the team slug, the invoking seat, the authorized
  artifact/territory scope, and the routing verdict, and MUST validate them before U0 begins.
- **FR-016**: The nested run MUST end at review completion and return a structured handoff
  carrying an outcome of [[STR-007]], [[STR-008]], or [[STR-009]], the stages reached, the
  artifact paths, the evidence paths, unresolved review findings, an explicit anomaly line,
  and the integration identity: line id, branch, worktree path, and HEAD commit. The retained
  branch MUST be named in the handoff. It MUST NOT merge or push.
- **FR-017**: The invoking Agent MUST include the nested run's handoff in its own result and in
  the team run report, verbatim or by stable path. It MUST NOT report success when the nested
  outcome is [[STR-008]] or [[STR-009]].
- **FR-018**: A nested run MUST register with the existing line registry and the existing
  worktree-per-write-line and ownership mechanism as one write line. Concurrent nested runs
  whose territories overlap MUST be serialized or rejected. No second registry, ownership
  model, integration queue, or state spine may be created.
- **FR-019**: On stall, timeout, or budget exhaustion, the nested run MUST stop, persist its
  state spine, and return a [[STR-009]] handoff carrying what was found, why the run was
  costly, the intermediate artifacts by path, and the available dispositions. The outer
  team's failure isolation and reporting MUST apply; the run MUST NOT wait silently.

**Diffusion into the Goal/Team/Agent system**

- **FR-020**: A Goal MUST NOT gain a mandatory SDD field or a structural link to a
  Requirements spec. A nested run's contribution to a Goal is observational through the team
  run report and summary. At report time, the team supervisor — the sole writer of tracked
  artifacts — MUST append one ledger item carrying the existing Target reference; the nested
  run MUST NOT write tracked artifacts, and no new Goal field is introduced.
- **FR-021**: The team run-report contract, owned by `create-team/SKILL.md` § Report contract,
  MUST gain a mandatory nested-SDD section ([[STR-010]]) that lists every invocation's outcome,
  artifact and evidence paths, routing-verdict reference, and anomalies. A run with no
  invocation MUST state that explicitly rather than omitting the section.
- **FR-022**: The team conceptual model MUST disambiguate its Stage dimension
  (executor/evaluator/optimizer) from the SDD stage roster. No team Stage value may be renamed
  or overloaded with an SDD stage name, and the SDD stage roster remains owned by the driver.
- **FR-023**: An Agent Template or Instance that hosts SDD MUST declare [[STR-002]] and state in
  its responsibilities that it hosts the driver, does not execute stage commands itself, and
  ends at review. The SDD stage-executor capacity remains a leaf and MUST NOT declare
  [[STR-002]].
- **FR-024**: The project instructions MUST carry a pointer-level routing surface: when a
  write-bearing change is proposed, run the decision at the owner's path. The instructions MUST
  NOT restate the input set or verdict table, and the proactive trigger MUST NOT start an SDD
  run without both a routing verdict and effective authorization.
- **FR-025**: `sdd-project-setup` and `sdd-house-keeping` MUST be classified in the same
  routing surface as bootstrap and maintenance paths, distinct from the SDD development flow,
  so an Agent can choose among them. An invocation of either skill MUST satisfy the same
  effective-authorization predicate as an SDD invocation when it dispatches subagents. Only
  `sdd-loop-driver` constitutes an SDD invocation under FR-015.

**Compatibility and safety**

- **FR-026**: An Agent definition or Team seat that carries no [[STR-001]] declaration MUST
  resolve to [[STR-003]], and the pre-dispatch probe MUST reject any dispatch for that
  recipient that names an SDD driver. As a decidable containment claim: relative to the
  baseline case set captured at the pre-change commit named in the verification record, the
  post-change case set of the pre-dispatch governance suite MUST be a superset, and every
  pre-change case MUST return the same verdict.
- **FR-027**: The feature MUST be additive on the four named surfaces: the standalone
  `sdd-loop-driver` entry contract, the Feature 070 stage-team preset contract, the Feature 064
  line/worktree/ownership contract, and the Feature 058 U0–U6 contract. On each surface it
  MUST NOT remove, rename, or change the meaning of an existing key, section, entry form, or
  exit code; additions are permitted. As a decidable containment claim: for each surface, the
  post-change contract-suite case set MUST be a superset of the pre-change case set captured
  at the baseline commit in the verification record, and every pre-change case MUST pass.
- **FR-028**: The framework MUST NOT add automatic merge or push, a scheduler or daemon,
  automatic feedback transmission, or a second confirmation gate.

### Key Entities

- **Control Layer**: One rung of the hierarchy — Goal, Team, Agent, or SDD Invocation. Each
  layer has an owner and a boundary; a lower layer never mutates an upper layer's definition.
- **SDD Invocation**: A bounded nested SDD run started by an authorized seat. Carries the
  invoking team and seat, the Goal/Target, the authorized scope, the routing verdict, the line
  identity, the integration identity, the outcome, and the artifact/evidence paths.
- **Seat Policy**: The `team.md` frontmatter entry under [[STR-011]], keyed by seat slug; it
  resolves together with the Agent capability to the effective authorization.
- **Authorization**: The pair of Agent capability and Team seat policy for the same key,
  resolved by (team, seat); its effective value is their AND, and the record names which half
  supplied which value.
- **Routing Verdict**: The decision record — declared inputs, verdict, reason code from the
  closed vocabulary, actor, and any user override.
- **Direct Modification**: A change executed without an SDD artifact chain, still subject to
  the applicable quality and confirmation gates.
- **Integration Identity**: The line id, branch, worktree path, and HEAD commit that let the
  outer layer locate and integrate a completed nested run.
- **Nested Run Handoff**: The structured return from a nested run — outcome, stages reached,
  artifact and evidence paths, unresolved findings, integration identity, and an anomaly line.
- **Stage Executor**: A leaf execution that runs one assigned stage inside a nested run; it
  cannot drive, dispatch, or start another run.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In a fixture team with one authorized and one unauthorized seat, the same
  SDD-routed duty starts exactly one nested run from the authorized seat and is blocked before
  dispatch for the unauthorized seat, with the failing authorization half named in both
  records.
- **SC-002**: The routing engine returns the documented verdict and reason code for every row
  of a golden case table covering feature, maintenance, cross-cutting, irreversible, ambiguous,
  conflicting, and bounded definition-correction changes; ambiguous and conflicting rows expect
  [[STR-006]], and the bounded definition-correction row expects [[STR-005]] only when all
  FR-010 conditions hold. Repeated evaluation of identical inputs returns identical verdicts.
- **SC-003**: A nested run reaches review, produces the complete SDD artifact chain, performs
  zero merge and zero push, and the team run report's nested section cites every artifact and
  evidence path.
- **SC-004**: Stage executors cannot start an SDD run, and every dispatch prompt that names a
  driver without satisfying all three authorization conditions is blocked before dispatch;
  all pre-existing anti-nesting contract tests remain green for non-authorized paths.
- **SC-005**: Relative to the pre-change case set captured at the baseline commit named in the
  verification record, the post-change team, Agent, and standalone-driver contract suites have
  a superset case set, and every pre-change case returns the same verdict.
- **SC-006**: No second registry, ledger, state spine, ownership model, or integration queue is
  introduced; the nested run's records resolve to the existing line and state artifacts.
- **SC-007**: Every ambiguous or conflicting input set produces [[STR-006]] and never
  [[STR-005]]; the property holds across all cases in the golden table.
- **SC-008**: Relative to the goal fixture captured before the nested run, the post-run parsed
  Goal field set is identical, and any Target attribution resolves only through the existing
  ledger reference.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Fixture-team integration test under `tests/`, plus the generated team run
  report; inspected by the contract test for the authorization predicate.
- **SC-002 Source**: Routing-engine unit tests driven by a checked-in golden table; an
  idempotence test evaluates each row twice and compares verdicts and reason codes.
- **SC-003 Source**: A scripted integration fixture that runs one nested SDD invocation to
  review; assertions read the artifact paths, the team run report, `git log`, and `git status`.
- **SC-004 Source**: The pre-dispatch governance test suite and the existing anti-nesting
  contract tests; each blocked dispatch record is inspected for the named condition.
- **SC-005 Source**: The existing team, Agent, and `sdd-loop-driver` contract suites, run
  unchanged against the pre-change baseline and the post-change tree.
- **SC-006 Source**: A structure/grep contract test over the changed tree plus the line-registry
  contract test; both assert reuse of existing artifacts and absence of new stores.
- **SC-007 Source**: The same golden-table and property test as SC-002, filtered to ambiguous
  and conflicting rows; the expected value is fixed to [[STR-006]].
- **SC-008 Source**: A goal fixture validated with the goal engine before and after a scripted
  nested run; the contract test compares the parsed goal field set.

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"sdd-invocation"` | authorization schema checks (Agent definition + Team seat), pre-dispatch governance tests |
| `STR-002` | `"allowed"` | authorization schema checks, pre-dispatch governance tests, SDD-host Agent responsibility contract |
| `STR-003` | `"forbidden"` | schema-default tests, backward-compatibility tests |
| `STR-004` | `"sdd"` | routing golden table, routing-engine unit tests |
| `STR-005` | `"direct"` | routing golden table, direct-modification gate tests |
| `STR-006` | `"adjudicate"` | routing golden table, ambiguity and conflict property test |
| `STR-007` | `"completed"` | nested-run handoff contract test, team run-report contract test |
| `STR-008` | `"blocked"` | nested-run handoff contract test, authorization-failure tests |
| `STR-009` | `"failed"` | nested-run handoff contract test, stall and timeout tests |
| `STR-010` | `"## Nested SDD Runs"` | team run-report contract test |
| `STR-011` | `"seats"` | team.md seat-policy schema tests, authorization contract tests |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Boundary and Ownership (non-duplication)

| Concern | Existing owner | This feature's relationship |
|---------|----------------|-----------------------------|
| U0–U6, state spine, stage sentinels, U4 verification, watcher, stall handling | Feature 058 / `sdd-loop-driver` | Reference and preserve; the nested entry is additive |
| Agent Template / Instance / Execution; create/dispatch/improve skills | Feature 060 / `agent-definitions.md`; neutral key set in `src/specify_cli/__init__.py` (`NEUTRAL_AGENT_METADATA_KEYS`) | Reuse; the capability key extends the neutral metadata set and its validator allowlist |
| Line registry, worktree-per-write-line, ownership, integration queue | Feature 064 / `sdd-loop-driver/SKILL.md` Hard Requirement 11 and `references/dispatch-recipes.md` | Reuse as the only concurrency primitives; no second model |
| Stage-team preset and work-package decomposition | Feature 070 | Preserve; it is the in-run decomposition mechanism, not a substitute for nested invocation |
| Flow class, fast-fail, confirmation gates, Task Complexity Rubric | Features 069 / 052 and the shared guidelines | Reference by path; no restatement |
| Goal, Target, and Goal–Team binding | `goal-definitions.md` | Reference; no structural link or new mandatory field |
| Team conceptual model, patterns, run report | `create-team` / `run-team`; report contract in `create-team/SKILL.md` § Report contract | Reference; the report contract gains one mandatory section |
| Anti-nesting obligation | `subagent-definitions.md` § Dispatch-Time Governance Obligation | Amend the predicate once to the depth-2 chain and the virtual prohibition; do not duplicate it |

## Assumptions

- **A1**: This is a framework-source change under the two-hats rule; it lands in the sources and
  reaches client projects through the normal publish/install/init flow.
- **A2**: [[STR-001]] is a new neutral framework key registered in the neutral metadata set and
  excluded from host rendering, so host rendering differences do not change authorization.
- **A3**: The team seat policy is a backwards-compatible `team.md` frontmatter extension under
  [[STR-011]], keyed by seat slug; an absent entry means [[STR-003]] for every existing team.
- **A4**: The routing engine is deterministic over declared inputs, whose closed value domains
  and mechanical classification tests are owned by
  `shared/definitions/sdd-routing-definitions.md`. Honest classification remains the caller's
  duty, audited by the review surface; the engine never invents an input.
- **A5**: A nested SDD run is the only sanctioned nesting. Feature 070 work packages remain the
  only in-run decomposition; no third nesting form is introduced.
- **A6**: Of the `sdd-*` skills, only `sdd-loop-driver` constitutes the SDD development flow;
  `sdd-project-setup` and `sdd-house-keeping` are routed bootstrap/maintenance paths.
- **A7**: An explicit user instruction overrides the routing verdict and is recorded as an
  adjudication.
- **A8**: Goal and Requirement remain on different planes with no structural link; observational
  attribution is the only connection.
- **A9**: The concurrency cap is one nested run per member; no higher per-member cap escape
  exists.
- **A10**: The nested run's review stage may include the driver's existing review-repair loop of
  Feature 063; ending "at review" means after that loop settles, not before findings are
  addressed.
- **A11**: The permitted nesting chain is depth 2 (team orchestrator → member driver host →
  stage executor); a virtual-mode member cannot host SDD.
- **A12**: The routing unit is one declared member duty; the verdict is reused until one of its
  inputs changes.
- **A13**: The team supervisor writes the ledger attribution row; the nested run writes no
  tracked artifacts.

## Out of Scope

- Automatic merge or push by a nested run.
- Changing the internal workflow of any individual `/speckit.*` stage command.
- Allowing stage executors to drive, dispatch, or load any driver.
- Multiple levels of SDD nesting (SDD inside SDD).
- Replacing the Feature 070 work-package model or the Feature 064 line/ownership model.
- Automatically making every Agent SDD-capable.
- Adding a scheduler, daemon, second confirmation gate, or automatic feedback transmission.
- Rewriting the anti-nesting rule for dispatches that do not satisfy FR-005.

## Clarifications

### Session 2026-10-28

- Q: 「团队中某些 agent 可以启动 SDD 流程」——这个授权应该声明在哪一层？ → A: Agent 能力 + Team 策略（Agent 定义声明能力，团队席位再按 goal/target 决定本次是否启用）。
- Q: 「什么时候用 SDD、什么时候直接修改」的判据以什么为基础？ → A: 复合确定性判据（变更性质 + 影响面/可逆性 + 既有 Task Complexity Rubric），输出 sdd / direct / adjudicate 三值并记录理由。
- Q: 嵌套的 SDD 子流程应在哪一步收官？ → A: review 后交接——子流程止于 review 完成并交付规格/证据，合并 main 与 push 由外层 goal/team 层按确认门决定。
- Q: 本特性应绑定到哪个 Feature？ → A: 新建 Feature 074（跨层能力层：Goal/Team/Agent 控制层级 + 嵌套 SDD 调用 + 分流判据），与 058（循环驱动）、060（三层 Agent 机制）、070（驱动内工作包分解）的交付面分开。
- Q: 分流判据的输入取值域与理由码应放在哪里？ → A: 新建 `shared/definitions/sdd-routing-definitions.md`，拥有 5 个输入的封闭取值域、三值裁决、优先级与理由码词表；FR-014 指向它。
- Q: 输入同时命中多类条件时，三值裁决如何排优先级？ → A: adjudicate > sdd > direct——缺失/冲突/歧义先判 adjudicate；否则任一 sdd 条件命中即 sdd；仅全部 direct 条件成立才 direct；definition-class 的 cross-cutting 默认只在非 adjudicate 分支生效。
- Q: 合法的嵌套链与执行模态如何限定？ → A: 深度 2（团队编排者 → 成员 driver host → 阶段执行者 leaf）；virtual 成员不得承载 SDD；阶段执行者仍是叶子，SDD-within-SDD 禁止。
- Q: Team 席位的 sdd-invocation 策略应存储并解析在哪里？ → A: `team.md` frontmatter 的 `seats` 映射，按 (team, seat) 解析；与席位实例上的 Agent 能力形成真正的 AND。
- 修正（非用户裁决，同轮边界回修）：routing unit = 每成员职责一次并复用至输入变化；并发上限 = 每成员一（A9 由「每团队」改为「每成员」）；handoff 增补 line id / branch / worktree / HEAD 集成身份；ledger 归因由 team supervisor 写入，嵌套运行不写 tracked 工件。

### Session 2026-10-29

- Q: 074a 的 B-04 修复删除了每成员并发上限的逃逸口；父规格是否跟随？ → A: 跟随——父 FR-006/A9 现为每成员硬上限 1，不再允许团队声明更高 per-member cap（2026-10-29，切片 074a 分析回环）。
