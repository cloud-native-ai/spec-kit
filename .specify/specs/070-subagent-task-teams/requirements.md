# Requirements Specification: Task Decomposition & Team Coordination for Subagent-Driven SDD

**Requirement Branch**: `070-subagent-task-teams`
**Created**: 2026-10-24
**Status**: Draft
**Input**: Feature 070 brief dated 2026-10-24 — "Task Decomposition & Team Coordination for Subagent-Driven SDD"（驱动子代理的任务拆解与配合机制）: make unattended subagent-driven SDD runs materially faster and more reliable by decomposing each stage into bounded work packages, coordinating them through the existing agent-team substrate, and measuring the result against the measured baseline.

## Related Feature *(mandatory)*

**Feature ID**: 070
**Feature Name**: 驱动子代理的任务拆解与配合机制（Task Decomposition & Team Coordination for Subagent-Driven SDD）

**Binding rationale**: this specification introduces a new capability layer — work decomposition and package coordination inside the driver loop — rather than an evolution of an existing Feature's delivery surface. It is therefore bound to a new Feature, 070, matching the precedent of Features 064 and 068 (each bound to its own new Feature) rather than the 067 precedent (an evolution bound to Feature 058). Status starts at `Draft`. Binding is performed in this requirements stage per the stage brief, which overrides the default deferral to `/speckit.clarify`; the deviation is recorded under Clarifications.

**Reference-only related features (no ownership transferred)**:

- **058 — unattended SDD loop driver**: owns U0–U6, the per-line state spine, stage sentinels, U4 independent verification, watcher verdicts, and stall handling. Feature 070 references these and MUST NOT redefine them.
- **060 — subagent dispatch decomposition**: owns the Agent Template → Instance → Execution taxonomy and the `create-agent` / `run-agent` / `improve-agent` delegation surface. Feature 070 dispatches packages through `run-agent`; it does not re-own those skills.
- **061 — subagent CLI configuration**: owns `CAPABILITY_MATRIX` and dispatch eligibility. Feature 070 does not widen eligibility.
- **063 — SDD loop efficiency**: owns the fast lane, the two-slot test budget, the plan minor-fix constraint, and stream-json / detach behavior. All remain in force.
- **064 — subagent concurrency**: owns the line registry, line/run envelopes, worktree-per-write-line, the Ownership Manifest, the deterministic integration queue, CLI capability profiles, and lifecycle decoupling. Feature 070 reuses those primitives and MUST NOT create a second registry, a second ownership model, or a second integration queue.
- **067 — loop efficiency hardening**: owns the implement-stage part brief, the bounded part size, the dispatch log, test economics, and micro-gap coalescing. Feature 070's Work Package is the general model; the implement projection is the 067 part brief extended with decomposition fields, never a competing format or ledger.
- **068 — exec-quant feedback channel**: owns the execution-quantification feedback path. Feature 070 preserves it and adds no transmission surface.

**Team substrate reference**: `create-team` / `run-team` own the multi-agent Conceptual Model (Role × Stage × Type), the four collaboration patterns, team persistence, the preset contract, and run reports. Feature 070 consumes that vocabulary through a schema-compatible stage-team preset and a thin driver-side adapter; it does not modify either skill.

## Overview

Unattended SDD runs are serial and monolithic at the stage boundary: one subagent executes an entire stage, the driver waits, then verifies the whole result at once. The measured record shows this concentrates cost in the longest stages and, worse, in repair after review. The fix is not another watcher — it is a first-class decomposition and coordination layer that turns each stage into bounded work packages, dispatches the independent ones concurrently where safe, serializes write work deterministically, verifies each package independently, and integrates the result before the stage-level gate.

The layer must be additive. The driver remains the sole coordinator; stage commands remain opaque; stage sentinels, U4 independent verification, and every SDD quality gate remain mandatory. Package-level completion is subordinate to the stage gate, never a substitute. Feature 064's line registry, ownership, worktree, and integration semantics are invariants, and Feature 067's implement-stage part discipline is reused rather than replaced.

## Measured Baseline (2026-10-24, dated record; feasibility input, not a runtime guarantee)

Source: the Feature 070 brief dated 2026-10-24. The brief-derived evidence files it names (driver-side digest under a macOS home directory; historical spines under `/private/tmp/...`; Qoder desktop and qodercli transcripts) were **not reachable from this execution environment**. The values below are reproduced as the brief's dated record; they were not re-measured in this stage, and no value has been inferred or extrapolated.

| Signal | Measured value | Implication |
|---|---|---|
| `plan` stage | 65–70 min; 063 plan commit-to-tasks 23.4 min; 064 plan 23.9 min | longest serial stage |
| `review` + repair | review ~17–37 min; 064 post-review repair 156 min | the tail dominates; repair is monolithic |
| full chain | 064 requirements→review 2h40m, then repair 2h36m; 063 ~20.5 h wall-clock including overnight gaps | the critical path is serial and long |
| stage runs per canonical 8 stages | 063: 21 runs (2.6×); 064: 11 runs (1.4×) | rework and evidence loops are structural cost |
| driver sessions | 114–159 h span; 19–43 MB transcripts (43.4 MB, 23.1 MB, 19.8 MB) | the driver stays online for days under context/state pressure |
| manual interventions | 30 short continue/retry/status messages across 29 sessions; one implement killed (`exit=143`) | "unattended" still needs nudges |
| watcher verdicts | DONE 61 / RUNNING 30 / NO_SIGNAL 4 / FAILED 2 / DEAD 2 / ANOMALY 1 / TIMEOUT 1 / INCOMPLETE 1 | monitoring and retry overhead |
| decomposition today | implement split by Phase (P0–P7, at most 8 tasks per dispatch) done manually by the driver; review parallel verifiers ad hoc | no reusable decomposition or coordination model |
| team mechanism | 12 teams under `.specify/teams/`; `create-team` / `run-team` support parallel / serial / iteration / continuous | existing substrate, unused by the driver |

Interpretation recorded by the brief: the dominant loss is serialization of work that could be parallel or pipelined, plus rework executed as monolithic stages. The improvement target is therefore decomposition and coordination, and its acceptance must be measured against these values rather than asserted from impressions.

## Ownership Boundaries and Non-Duplication

| Concern | Owner | Feature 070's relationship |
|---|---|---|
| Stage chain, sentinels, state spine, U4 verification, watcher, stall handling | Feature 058 | Reference and preserve; no semantic change |
| Agent Template / Instance / Execution; `create-agent` / `run-agent` / `improve-agent` | Feature 060 | Dispatch packages through `run-agent`; no re-owning |
| CLI dispatch eligibility (`CAPABILITY_MATRIX`) | Feature 061 | Read-only reference; no widening |
| Fast lane, two-slot test budget, plan minor-fix, stream-json / detach | Feature 063 | Preserve unchanged |
| Line registry, envelopes, worktree-per-write-line, Ownership Manifest, integration queue, CLI profiles, lifecycle | Feature 064 | Reuse as the only line-level primitives; WP ownership is a finer projection inside one line's manifest — not a second registry |
| Implement part brief, bounded part size, dispatch log, test economics, micro-gap coalescing | Feature 067 | Extend the part brief into the WP model; no second brief format and no second ledger |
| Exec-quant feedback channel | Feature 068 | Preserve; no new transmission surface |
| Team schema, four patterns, presets, run reports | `create-team` / `run-team` | Consume through a schema-compatible preset and a thin adapter; no modification |

## Assumptions (unattended adjudication of the brief's open points; 2026-10-24)

- **A1 — Stage coverage in the first slice**: decomposition is enabled by default for `plan`, `implement`, and `review` when the gate passes. `analyze` and `clarify` may use read-only investigation work packages only when explicitly enabled. `requirements`, `tasks`, and `checklist` remain single-subagent in the first slice. Rationale: the measured longest stages are plan and review, and implement already has a mature part discipline; the remaining stages are either short or produce a single mandatory artifact whose parallelization has poor value-to-risk.
- **A2 — Direct `team.md` reuse versus a stage-team adapter**: a **stage-team preset plus a thin driver-side adapter** is adopted. A persisted `.specify/teams/<slug>/team.md` per stage is rejected because team persistence requires goal establishment and a goal binding, and each run owes a run report and a summary-refresh decision — a per-stage team would add unbounded team state and couple the loop to goal management for a lifetime of one stage. The preset conforms to the existing preset contract; the adapter maps a WP DAG to the existing Role × Stage × Type seats and pattern names. Neither `create-team` nor `run-team` is modified.
- **A3 — Parallel write packages in the first slice**: only **read-only** work packages may run concurrently. Write work packages run serially inside the line worktree. Parallel writes are deferred: they would require a WP-level worktree/ownership extension to Feature 064's one-worktree-per-write-line model, which this feature explicitly does not own. The gate must reject any dispatch set that would create concurrent writes.
- **A4 — Per-WP retry semantics**: each WP receives at most one automatic retry. A retry MUST change the scope (split smaller), the budget (backed by dispatch-level evidence), or the dispatch topology; an identical same-budget rerun is prohibited (the 067 precedent). A WP that fails twice fails the stage gate and enters the existing U5 stage-retry path (default two retries). WP retries are counted separately and do not consume the stage-level retry budget until that escalation.
- **A5 — Metrics thresholds and acceptance basis**: acceptance is **relative** to a comparable measured baseline plus **zero gate regression**. The wall-clock target is a median reduction of at least 20% for a decomposed stage of the same scale; the rework target is at most 1.5 stage executions per canonical stage, strictly below the 2.6× worst measured baseline. No absolute wall-clock promise is made. Any metric without a measurement is recorded as `not_evaluated`, never as zero or an estimate.
- **A6 — Scope slicing**: the artifact defines 30 FR definition rows, which is at the framework's decomposition ceiling but not above it (`split-required` triggers only above 30). The deterministic gate therefore returns `proceed`; no 070a/070b split is required. If later work grows the row count above the ceiling, the split proposal in the Decomposition / Slicing Record applies.
- **A7 — Feature binding timing**: Feature 070 is created and bound in this requirements stage per the stage brief, although the default protocol defers binding to `/speckit.clarify`. This is a recorded deviation, not a silent protocol change.
- **A8 — Scaffolding deviation**: the branch `070-subagent-task-teams` already existed when this stage ran. The scaffolding script's `git checkout -b` was therefore skipped and the spec directory was created with the same template content; no second branch or worktree was created.
- **A9 — Evidence provenance gap**: the brief's original evidence files were unavailable in the execution environment. The baseline is therefore the brief's dated record, and the gap is recorded here rather than filled with invented numbers. A later stage that re-measures must replace this record, not silently mix sources.
- **A10 — Preserved invariants**: the driver remains the sole coordinator; no stage subagent loads or runs the driver; stage commands stay opaque; the stage sentinel plus U4 plus checklist/analyze/review gates remain mandatory; Feature 064's semantics are unchanged; no push is performed.
- **A11 — Relationship to the 067 part discipline**: the WP is the general decomposition unit. For `implement`, the WP brief is the 067 part brief extended with WP identity, dependency, ownership, and parallel-safety fields. The 067 fields, the dispatch log, and the test-economics rules remain authoritative for their scope; Feature 070 adds no competing brief or ledger.
- **A12 — Default decomposition policy**: decomposition is the default for the three first-slice stages only when the gate passes and the stage has more than one genuinely independent or separable unit of work. A one-package stage, an all-serial stage with no independent work, or a stage explicitly disabled by the feature or the entry declaration runs as one package with the same acceptance evidence.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decompose a stage into bounded, gated work packages (Priority: P1)

The driver reaches a stage boundary, derives the stage's work from its own artifacts, and writes a Work Package plan: each package with inputs, outputs, ownership, dependencies, budget, and acceptance evidence. A deterministic gate checks the plan — acyclic graph, complete output coverage, disjoint write ownership for concurrent packages, bounded size — and either admits it or blocks dispatch. When decomposition is not beneficial or is disabled, the stage runs as one package.

**Why this priority**: without a trustworthy package plan and a gate, every later dispatch and verification step inherits an unbounded, unowned scope. This is the prerequisite for all other value.

**Independent Test**: run the decomposition on a fixture stage whose artifacts imply several packages; inspect the plan and gate verdict. Then inject a cycle, an unowned required output, and an overlapping write pair, and confirm each is rejected. Disable decomposition and confirm one package with the same acceptance evidence.

**Acceptance Scenarios**:

1. **Given** a stage whose artifacts imply independent units and disjoint write paths, **When** the driver decomposes it, **Then** every package carries the required schema fields and the gate returns `admit`.
2. **Given** a package plan with a dependency cycle, **When** the gate runs, **Then** dispatch is blocked and the reason is recorded; no package is dispatched.
3. **Given** two packages that would be dispatched concurrently with overlapping owned paths, **When** the gate runs, **Then** the plan is rejected and the driver either serializes the packages or splits the ownership scope.
4. **Given** a stage with one artifact and no separable work, **When** decomposition runs, **Then** the driver records `single-package` with the reason and dispatches exactly one subagent.
5. **Given** a feature or stage with decomposition disabled, **When** the stage is dispatched, **Then** the single-subagent path is used and the full stage gate still applies.

---

### User Story 2 - Coordinate package dispatch with safe parallelism and deterministic writes (Priority: P1)

The driver dispatches packages through the existing single-agent dispatch mechanism, following the dependency graph. Independent read-only packages may run concurrently within the declared slot cap; every write package runs serially inside the line worktree. A failing package does not corrupt or silently block unrelated packages, and each package is retried at most once with a changed scope, budget, or topology.

**Why this priority**: this is where the measured serialization loss is actually removed. Without safe scheduling and failure isolation, decomposition would add overhead without reducing wall-clock.

**Independent Test**: dispatch a fixture DAG with two independent read-only packages and one dependent write package; confirm the read-only intervals overlap, the write package starts only after its dependency is verified, and its writes never overlap another package's paths. Force one package to fail and confirm the dependent is not unlocked while unrelated work completes.

**Acceptance Scenarios**:

1. **Given** two independent read-only packages and a declared slot cap of two, **When** the driver dispatches, **Then** both are dispatched and their execution intervals overlap, recorded in the spine.
2. **Given** a write package and a read-only package whose paths overlap, **When** scheduling runs, **Then** the write package is serialized and the read-only package does not write.
3. **Given** a package that exceeds its budget, **When** the first attempt ends, **Then** the one retry changes the scope, budget, or topology and the change is recorded; an identical rerun is rejected.
4. **Given** a package that fails twice, **When** the driver escalates, **Then** the stage gate fails and the existing U5 stage-retry path is entered; the WP retry history remains visible.
5. **Given** a package whose prompt would name the driver skill or instruct loading a skill, **When** pre-dispatch governance runs, **Then** the dispatch is blocked and recorded.

---

### User Story 3 - Verify each package independently, then integrate before the stage gate (Priority: P1)

Every package is checked by a verifier that is not its executing subagent, with a recorded verdict and evidence pointer. The driver aggregates the outputs, detects missing or contradictory results, integrates them in a deterministic order, and only then runs the unchanged stage-level U4 verification and sentinel check.

**Why this priority**: decomposition without independent package verification converts one large self-report into several smaller self-reports. The stage gate must remain the authority.

**Independent Test**: run a fixture where one package claims success without its output and another produces a conflicting artifact; confirm the aggregation detects both, integration stops, and the stage gate fails. Then run a clean fixture and confirm the stage sentinel and U4 pass only after integration.

**Acceptance Scenarios**:

1. **Given** a package that finishes, **When** verification runs, **Then** a verifier distinct from the executor records pass/fail plus evidence, and a failed package never unlocks its dependents.
2. **Given** all packages pass, **When** aggregation runs, **Then** missing, unowned, or contradictory outputs are detected before stage U4; a clean set is integrated in the declared deterministic order.
3. **Given** an integration conflict, **When** the driver reaches the conflict, **Then** integration stops, the stage gate fails, and no partial commit is presented as a complete stage deliverable.
4. **Given** a clean integrated result, **When** stage U4 runs, **Then** the stage sentinel is necessary, artifact verification and discipline checks are performed, and the stage passes only when all three hold.

---

### User Story 4 - Reuse the team substrate through a stage-team preset and pattern selection (Priority: P2)

The driver maps packages to seats expressed in the existing team vocabulary and selects a pattern from the package graph: parallel for independent read-only work, serial for dependencies and writes, iteration for bounded repair loops. A reusable stage-team preset carries the standard planner/worker/verifier/integrator seats, and a thin adapter binds preset plus graph into a run-scoped plan without creating a persisted team per stage.

**Why this priority**: it keeps the new layer aligned with the framework's existing multi-agent model and avoids inventing a second orchestration abstraction. It is P2 because the decomposition and dispatch value in Stories 1–3 can be delivered without a polished preset.

**Independent Test**: instantiate the preset for a fixture stage and confirm the seats, pattern, and slot cap are derived from the graph; confirm no `.specify/teams/<slug>/` directory is created; confirm the parallel pattern is selected only for independent read-only graphs and the serial pattern for any graph containing a write package.

**Acceptance Scenarios**:

1. **Given** a graph of independent read-only packages, **When** the adapter selects a pattern, **Then** `parallel` is recorded with the seat mapping and the slot cap.
2. **Given** a graph containing a write package, **When** the adapter selects a pattern, **Then** `serial` is recorded and the dispatch order is the topological order with the declared tie-break.
3. **Given** a repair loop over review findings, **When** the adapter selects a pattern, **Then** `iteration` is recorded with an explicit maximum iteration count and a stop condition; `continuous` is never selected.
4. **Given** any decomposed stage, **When** the run completes, **Then** no persisted team definition was created and `create-team` / `run-team` behavior is unchanged.

---

### User Story 5 - Make the improvement measurable without a second ledger (Priority: P2)

The line state spine records each package's dispatch, timestamps, attempts, verdict, and evidence. A run report or digest shows the decomposition, dispatch order, critical path, wall-clock, parallelism efficiency, retries, and verdicts. Acceptance is judged as a relative change against a comparable measured baseline, with zero gate regression, and unmeasured metrics are reported as `not_evaluated`.

**Why this priority**: without measurement the feature cannot distinguish real throughput improvement from reshuffled overhead, and the existing runtime-record discipline forbids a second statistics system.

**Independent Test**: run a fixture stage with two concurrent read-only packages and read the spine plus report; recompute the critical path and parallelism efficiency from the recorded timestamps and compare with the report. Delete a timestamp and confirm the metric becomes `not_evaluated` rather than a zero.

**Acceptance Scenarios**:

1. **Given** a completed decomposed stage, **When** the run report is read, **Then** it carries the pattern, slot cap, dispatch order, critical path, wall-clock, parallelism efficiency, retries, and verdicts, with evidence paths instead of raw transcripts.
2. **Given** a metric whose source records are missing, **When** the report is written, **Then** the metric is `not_evaluated`, not zero and not an estimate.
3. **Given** a claimed parallel speed-up, **When** the spine is audited, **Then** at least two package execution intervals genuinely overlap; otherwise the claim is invalid.
4. **Given** a completed benchmark comparable to the baseline, **When** success is assessed, **Then** the wall-clock and rework criteria are computed from spine timestamps and the gate-regression check from the name-level failure set.

---

### Edge Cases

- **One-package stage**: decomposition must not add dispatch or reporting overhead that exceeds its value; the single-package path records `single-package` and proceeds.
- **Gate rejects the plan**: the driver must split, serialize, or fall back; it MUST NOT dispatch a partially owned or cyclic plan.
- **A package produces no output but reports success**: aggregation detects the missing output; the package is not verified and the stage gate fails.
- **Two packages produce contradictory artifacts**: integration stops before the stage commit; the contradiction is surfaced with both evidence pointers.
- **A package writes outside its owned paths**: the violation is detected during verification/integration, the stage gate fails, and the write is not integrated.
- **A package exceeds its budget**: one retry with a changed scope, budget, or topology; a second failure escalates to the stage gate and U5.
- **The decomposition layer is unavailable or corrupt**: the driver falls back to the single-subagent stage path and records `decomposition-unavailable` with the reason; it never runs a silent partial package set.
- **A package's own sentinel appears in its output**: only the stage-level final output can satisfy the stage sentinel; a package sentinel is never promoted.
- **A package prompt would load the driver or spawn a coordinator**: pre-dispatch governance blocks it; a subagent must never become a second driver.
- **The stage is analyze or clarify without opt-in**: single-subagent path; read-only investigation packages require the explicit enablement declared in A1.
- **Baseline is unavailable for a metric**: record `not_evaluated`; never substitute zero, an estimate, or another stage's number.
- **A package fails while an unrelated read-only package is still running**: the unrelated package completes and is recorded; failure isolation is preserved.

## Requirements *(mandatory)*

### Functional Requirements

#### A. Decomposition model and gate

- **FR-001**: Every Work Package (WP) MUST be a bounded, independently verifiable unit carrying at least: a stable `wp_id`; the owning stage; the objective/scope; required inputs; expected outputs as repository-relative paths or named artifacts; `owned_paths` and `read_only_paths`; `depends_on` (WP ids); `parallel_safe`; a turn/run budget (`max_turns`); acceptance criteria; and the sentinel/evidence that proves completion. A WP missing any required field MUST NOT be dispatched.
- **FR-002**: Decomposition MUST be derived from the stage's own artifacts by a declared, replayable rule: `plan` → design-artifact, research, and verification packages; `tasks` → phase/task-group packages; `implement` → task-group packages bounded by the existing part-size cap; `review` → review-dimension and finding-repair packages; `analyze` / `clarify` → read-only investigation packages. The rule applied and the resulting package list MUST be recorded so the same stage artifacts yield the same decomposition on replay.
- **FR-003**: Before any WP dispatch, the stage MUST pass a decomposition gate requiring all of: (a) the package graph is acyclic; (b) every required stage output is owned by exactly one package, with no orphan or unowned output; (c) no two concurrently dispatched packages have overlapping `owned_paths`, and every owned path is covered by the line's Ownership Manifest; (d) each package is bounded — at most 8 tasks for `implement`, at most 40 contract clauses for a clause-producing package, or an equivalent declared acceptance scope for other stages; (e) the selected pattern is compatible with the graph. A gate failure MUST block dispatch and be resolved by splitting, serializing, or falling back to one package.
- **FR-004**: The stage decomposition record — package list, graph edges, selected pattern, slot cap, gate verdict, and the decomposition rule — MUST be written to the line state spine before the first package dispatch. Package ids MUST remain stable for the life of the stage so retries and evidence remain attributable.
- **FR-005**: Decomposition MUST be individually disablable per stage and per feature. When it is disabled, or the gate finds decomposition not beneficial, the stage MUST run as exactly one single-subagent package with the same acceptance evidence, and the decision plus its reason MUST be recorded.

#### B. Team mapping and pattern selection

- **FR-006**: The package graph MUST be mapped to seats expressed in the existing `create-team` vocabulary — Role × Stage × Type, with each package assigned exactly one accountable seat and a Worker or Meta type. No second multi-agent abstraction and no second team registry may be introduced.
- **FR-007**: The stage pattern MUST be selected from the existing four pattern names by a declared rule: `parallel` when two or more ready packages are independent and read-only; `serial` when packages have dependencies or any package owns write paths; `iteration` for bounded repair or finding-convergence loops with an explicit maximum iteration count and stop condition; `continuous` is excluded from this feature.
- **FR-008**: A reusable stage-team preset compatible with the existing preset contract (preset id, pattern, inputs, roster skeleton, config, provenance) MUST define the standard seats — planner/lead, worker, verifier, and integrator. The driver MUST use a thin adapter that binds the preset and the package graph into a run-scoped coordination plan. A per-stage persisted team definition MUST NOT be created, and `create-team` / `run-team` behavior MUST NOT be modified.
- **FR-009**: Before dispatch, the adapter MUST verify: territory disjointness for concurrently dispatched packages; that every write package's paths are covered by the line Ownership Manifest; that the package slot count does not exceed the line's remaining concurrency allowance; and that each concurrently dispatched package declares isolated ports, temporary directories, and caches, or a read-only shared resource.

#### C. Package dispatch and coordination

- **FR-010**: Each package MUST be dispatched as one bounded subagent execution through the `run-agent` mechanism with a WP brief carrying the fields of FR-001 plus the stage sentinel context. The outgoing prompt MUST NOT name or load `sdd-loop-driver`, MUST NOT instruct the subagent to load any skill, and MUST NOT contain loop logic.
- **FR-011**: Scheduling MUST follow the package graph: a package is dispatchable only when all `depends_on` packages are verified; independent read-only packages MAY run concurrently within the declared slot cap; every write package MUST run serially inside the line worktree in this feature's first slice; no package may write outside its `owned_paths` or into another package's read-only paths.
- **FR-012**: A failed, stalled, or budget-exhausted package MUST NOT block or corrupt unrelated concurrent packages; its outcome MUST be recorded as failed and MUST NOT be counted as verified; the driver MUST NOT unlock a dependent package whose dependency is not verified.
- **FR-013**: Each package MUST receive at most one automatic retry, and the retry MUST change the scope (a smaller package), the budget (with dispatch-level evidence), or the dispatch topology. An identical same-budget rerun is prohibited. A package that fails twice MUST fail the stage gate and enter the existing U5 stage-retry path; package retries do not consume the stage-level retry budget until that escalation.
- **FR-014**: After all dispatchable packages settle, the driver MUST aggregate their outputs and detect missing, unowned, or contradictory outputs before running stage-level U4. Aggregation MUST NOT infer success from package self-reports.
- **FR-015**: The driver MUST remain the sole coordinator. Package executors MUST NOT dispatch other packages, spawn a driver, or modify the stage plan; package completion is subordinate to the stage sentinel and independent U4 verification.

#### D. Verification and integration

- **FR-016**: Every package MUST be verified by a verifier that is not the package's executing subagent, applying contract or adversarial checks where the package's acceptance admits them. The verdict MUST record pass or fail, the acceptance evidence actually checked, and an evidence pointer. A package without an independent verdict MUST NOT unlock its dependents.
- **FR-017**: The stage-level U4 procedure MUST remain mandatory and unchanged: the stage sentinel is necessary, artifact verification is required, and discipline checks are required. Package verdicts are inputs to that procedure and MUST NOT substitute for it.
- **FR-018**: Package outputs MUST be integrated in a deterministic order derived from the graph with a declared tie-break. An integration conflict or a missing output MUST stop integration and fail the stage gate; a partial integration MUST NOT be reported or committed as a complete stage deliverable. The stage commit MUST be made once, by the driver or its integrator seat, after integration.
- **FR-019**: Closure and merge remain driver-owned. This feature MUST NOT push, force-merge, or auto-merge, and MUST preserve the existing confirmation gates.

#### E. Observability and efficiency metrics

- **FR-020**: The line state spine MUST carry a package ledger with, per package: `wp_id`, stage, graph edges, dispatch order, start and end timestamps, attempts, budget, verdict, evidence pointer, and output paths. At stage close the spine MUST also carry the derived critical path, wall-clock, and parallelism efficiency, or the run report MUST derive them from the spine timestamps and point back to the spine. Token or run cost MUST be recorded when available and recorded as `not_evaluated` when unavailable — never as zero.
- **FR-021**: Each decomposed stage MUST produce a run report or digest showing the decomposition, selected pattern and slot cap, dispatch order, critical path, wall-clock, parallelism efficiency, retries, and verdicts. The report MUST reference evidence by path and MUST NOT dump raw transcripts.
- **FR-022**: Efficiency measurements MUST use declared definitions: stage wall-clock (first package dispatch to stage U4 completion); critical path (duration-weighted longest graph path); parallelism efficiency (summed package durations divided by wall-clock times the maximum concurrent package count); stage executions per canonical stage (stage dispatch attempts divided by canonical stages); retry counts (package and stage separately); and manual interventions (user continue/retry/status messages per run).
- **FR-023**: Efficiency acceptance MUST be expressed as a relative change against a comparable measured baseline for the same stage scale. Every metric without a measurement MUST be reported as `not_evaluated`; no absolute wall-clock promise may be substituted, and no stage may claim improvement from impressions or estimates.

#### F. Compatibility and fallback

- **FR-024**: The existing single-subagent stage path MUST remain fully functional. In this feature's first slice, decomposition is enabled by default for `plan`, `implement`, and `review` when the gate passes; `analyze` and `clarify` MAY use read-only investigation packages only when explicitly enabled; `requirements`, `tasks`, and `checklist` remain single-subagent unless a later feature enables them.
- **FR-025**: This feature MUST NOT change stage-command internals, stage sentinel literals, U4 semantics, the checklist/analyze/review gates, the two-slot test budget, the plan minor-fix constraint, the fast lane, Feature 064's line registry/ownership/worktree/integration semantics, Feature 067's part-brief and test-economics rules, or Feature 068's feedback channel.
- **FR-026**: If the decomposition or coordination layer is unavailable, fails its own gate, or loses its evidence, the driver MUST degrade to the single-subagent stage path, record the failure reason and the fallback in the spine, and MUST NOT silently continue with a partial package set.
- **FR-027**: Delivery MUST be confined to the driver skill's source, its references, templates, and scripts, its documentation page, and this feature's specification and evidence. The feature MUST NOT add a runtime service, daemon, external dependency, model API, or a second registry or ledger. Runtime records (feedback, session, knowledge, exec-quant, history, trigger) MUST NOT be stage deliverables.

#### G. Tests and evidence

- **FR-028**: Contract tests MUST pin the package schema, the decomposition gate outcomes, the pattern-selection rule, the preset-to-seat mapping, the ownership and slot preflight, the retry policy, and the single-package fallback.
- **FR-029**: Fixture-based dry runs MUST prove concurrent read-only dispatch, write serialization, ownership-violation rejection, deterministic integration, and fallback. Regression tests MUST prove that existing driver behavior — sentinels, U4, the stage chain, the test budget, the plan constraint, and the 064/067/068 semantics — is unchanged.
- **FR-030**: New behavior MUST have red-first evidence recorded before implementation. Each verification record MUST carry the command, exit code, pass/fail counts, changed paths, and an evidence pointer. A green check that would not turn red when its subject breaks MUST NOT be cited as proof.

### Out of Scope

- A nested driver, a second orchestrator, or any subagent that loads or runs the driver manual.
- Changes to `/speckit.*` stage-command internals, sentinel literals, U4 semantics, or quality-gate criteria.
- A second line registry, ownership model, worktree model, integration queue, or CLI profile store; Feature 064's primitives remain the only line-level ones.
- Parallel write packages in the first slice; WP-level sub-worktrees or a 064 ownership extension.
- A multi-feature or multi-line scheduler beyond what Feature 064 already provides.
- Persisting a `.specify/teams/<slug>/team.md` per stage, or modifying `create-team` / `run-team`.
- `continuous` pattern operation, long-lived team loops, or a new service/daemon.
- Push, remote branch operations, force merge, or bypassing confirmation gates.
- Weakening any quality gate, test-budget slot, or independent-verification requirement to gain speed.

### Key Entities *(include if requirement involves data)*

- **Work Package (WP)**: the bounded unit of stage work; attributes exactly as required by FR-001. One package has one accountable seat and one acceptance evidence set.
- **WP Graph / Stage Decomposition Record**: the package set plus dependency edges, pattern, slot cap, gate verdict, and decomposition rule; written to the line state spine before dispatch (FR-004).
- **Stage Team Preset**: a schema-compatible preset carrying the standard planner/lead, worker, verifier, and integrator seats and the pattern configuration skeleton (FR-008).
- **Seat Mapping**: the derived assignment of each package to one Role × Stage × Type seat, with Worker/Meta type and territory (FR-006).
- **WP Dispatch Record**: per-package dispatch order, start/end timestamps, attempts, budget, verdict, evidence pointer, and output paths (FR-020). It extends, and does not replace, the existing dispatch log and state spine.
- **WP Verdict**: the independent verifier's pass/fail result with the acceptance evidence checked and an evidence pointer (FR-016).
- **Stage Coordination Report**: the per-stage digest of decomposition, pattern, dispatch order, critical path, wall-clock, parallelism efficiency, retries, and verdicts (FR-021).
- **Referenced owners, not redefined**: Line Registry, Line Envelope, Ownership Manifest, and Integration Queue (Feature 064); Part Brief and Dispatch Log (Feature 067); line state spine and sentinel (Feature 058).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On a benchmark run of a feature comparable in stage scale to the 2026-10-24 baseline, decomposed `plan` and `review` stages achieve a median wall-clock reduction of at least 20% versus their baseline medians (plan 65–70 min; review 17–37 min), measured from spine timestamps rather than impressions. When no comparable run exists, the criterion MUST record `not_evaluated` and MUST NOT be claimed as met.
- **SC-002**: On that benchmark, stage executions per canonical stage are at most 1.5×, strictly below the worst measured baseline of 2.6× (Feature 063) — a relative reduction of at least 40% — and no worse than 1.5 absolute.
- **SC-003**: Zero gate regressions: 100% of decomposed stages still produce their stage sentinel and pass U4; the checklist/analyze/review gates, the two-slot test budget, the plan minor-fix constraint, the fast lane, Feature 064's registry/ownership/worktree/integration semantics, Feature 067's part discipline, and Feature 068's channel are unchanged; and the contract/integration suites report zero new name-level failures against the run's baseline failure set.
- **SC-004**: Package coverage and ownership: 100% of required stage outputs are owned by exactly one package; the count of orphan or unowned outputs is zero; the count of cross-package or out-of-territory writes is zero.
- **SC-005**: Every stage records a decomposition decision — `decomposed` or `single-package` — with the gate verdict and reason; silent partial runs are zero.
- **SC-006**: Manual interventions per completed benchmark feature do not exceed the measured baseline rate (30 interventions across 29 sessions, normalized per session), counted from the run record.
- **SC-007**: For every decomposed stage with at least two ready packages, the report records the critical path, wall-clock, parallelism efficiency, and retries; a parallel-execution claim without at least two overlapping package intervals in the spine is invalid, and the number of such invalid claims is zero.
- **SC-008**: Fixture dry runs pass every enumerated scenario — concurrent read-only dispatch, write serialization, ownership-violation rejection, deterministic integration, fallback, and no nested driver — with zero failures, and the existing driver regression suite reports zero new failures.

### Measurement Sources & Collection Methods

- **SC-001 / SC-002 / SC-006 / SC-007 Source**: the line state spine's package ledger and dispatch records, the run report/digest, commit timestamps, and the existing runner status/log artifacts. Baseline values come from the 2026-10-24 dated record in this specification; any re-measurement MUST replace that record rather than mix sources.
- **SC-003 Source**: stage U4 verdict records, gate summaries in the spine, and name-level failure sets produced by the canonical test runner (`--names-out` plus the existing name-level difference method); the baseline failure set is captured at the implement slot.
- **SC-004 / SC-005 Source**: the stage decomposition record, the package ledger, the integration record, and the gate verdict written to the spine.
- **SC-008 Source**: fixture dry-run logs and the canonical test-runner output; each record carries command, exit code, pass/fail counts, changed paths, and an evidence pointer.

## Decomposition / Slicing Record

- **Measured input**: FR definition rows = 30 (counted by the deterministic gate pattern from this file).
- **Gate**: the framework's large-feature gate triggers `split-required` only above the 30-row ceiling; at exactly 30 the measured verdict is `proceed`.
- **Decision**: one feature slice (070). No 070a/070b split is required for the current scope.
- **Contingent split proposal** (only if later growth exceeds the ceiling or the task count exceeds 40): **070a — core package layer**: package schema, decomposition gate, package dispatch/coordination, verification/integration, compatibility/fallback, and their tests. **070b — coordination refinement**: stage-team preset and adapter refinement, bounded iteration pattern, observability/metrics reporting, and any later-approved read-only parallel expansion. Each slice would retain its own spec directory bound to Feature 070 and would remain subject to every quality gate; the split MUST NOT delete, merge, or reorder requirements to evade the ceiling.

## Clarifications

### Session 2026-10-24 — requirements (unattended adjudication)

- Q: Which stages receive decomposition in the first slice? → A: `plan`, `implement`, and `review` by default when the gate passes; `analyze` / `clarify` read-only investigation only on explicit opt-in; the remaining stages stay single-subagent (Assumption A1).
- Q: Direct `team.md` reuse or a stage-team adapter? → A: a schema-compatible stage-team preset plus a thin driver-side adapter; no persisted team per stage and no modification to `create-team` / `run-team` (Assumption A2).
- Q: Are parallel write packages allowed initially? → A: no; read-only packages may parallelize, write packages serialize inside the line worktree; parallel writes require a future Feature 064 extension (Assumption A3).
- Q: Per-package retry versus stage-level retry? → A: one package retry with a changed scope, budget, or topology; a second failure escalates to the stage gate and the existing U5 path; package retries do not consume the stage retry budget until escalation (Assumption A4).
- Q: What counts as "efficiency improved"? → A: a relative median wall-clock reduction of at least 20% for comparable stages, at most 1.5 stage executions per canonical stage, zero gate regression, and `not_evaluated` for anything unmeasured (Assumption A5; SC-001 through SC-008).
- Q: Does the scope exceed the decomposition gate? → A: no; the artifact defines 30 FR definition rows, which is at the ceiling and yields `proceed`; a contingent split proposal is recorded above (Assumption A6).
- Q: Why is Feature binding performed now? → A: the stage brief explicitly directs binding Feature 070 in this stage, overriding the default deferral to `/speckit.clarify`; recorded as a deviation (Assumption A7).
- Q: Why was the scaffolding script's branch creation skipped? → A: the branch `070-subagent-task-teams` already existed; branch creation was skipped and the spec directory was scaffolded from the same template, with no second branch or worktree created (Assumption A8).
- Q: Was the brief's baseline re-measured? → A: no; the named evidence files were unreachable from this environment, so the brief's 2026-10-24 values are carried as a dated record and the provenance gap is disclosed (Assumption A9).
