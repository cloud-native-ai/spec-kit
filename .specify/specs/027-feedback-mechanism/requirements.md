# Requirements Specification: Framework Feedback Mechanism

**Requirement Branch**: `027-feedback-mechanism`  
**Created**: 2026-07-13  
**Status**: Draft  
**Input**: User description: "需要在整个框架中引入Feedback机制。所有的操作都不可能一成不变或完美，因此调用的命令、执行的技能、运行的 Agent 都可能存在某种缺陷。因此需要在关键的执行流程中添加可以进行反馈的机制。在大部分执行流程结束后（类似提示用户进行 Git commit 的时机），生成对当前执行流程的 Feedback。整体 review 的 feedback 机制偏向全局视角，而分散在各子模块中的 feedback 仅针对当前操作。例如，执行命令后，需在结尾回顾整个执行过程，并结合命令描述或执行流程，总结针对该命令的优化点。该 feedback 机制不能随机散落在所有执行流程上（会大大降低执行效率），只需放到某些长时间执行的关键流程上。默认情况下，一个技能（skill）必须包含 feedback 反馈机制；针对命令（command），只有很复杂的命令才需要，需根据具体情况进行评估。"

## Related Feature *(mandatory)*

**Feature ID**: 028  
**Feature Name**: Feedback Mechanism

## User Scenarios & Testing *(mandatory)*

<!--
  User stories are prioritized as independently testable journeys.
  P1 is the MVP; each story delivers standalone value.
-->

### User Story 1 - Skill self-feedback at end of execution (Priority: P1)

As a framework maintainer and as an end user running a Spec Kit skill, when a skill finishes a substantial run, I want the skill to look back over what it just did — in light of the skill's own stated purpose — and surface concrete, skill-specific optimization points, so that recurring weaknesses in that skill become visible and can be improved over time.

**Why this priority**: Skills are the most frequently reused, long-running units of behavior in the framework, and the user requires that *every* skill carries a feedback step by default. This is the backbone of the whole capability — without it, there is no distributed feedback layer. It is the minimum viable slice: one skill that reviews itself and reports optimization points already demonstrates the value.

**Independent Test**: Run any single skill end-to-end and confirm that, at the conclusion of its key flow, it produces a local feedback entry that (a) references the skill's declared purpose/description, (b) reviews the actual execution that just happened, and (c) lists actionable optimization points scoped to that skill only.

**Acceptance Scenarios**:

1. **Given** a skill with a defined feedback step, **When** the skill completes its key flow, **Then** it emits a feedback entry containing a review of the just-completed run plus at least one concrete optimization point tied to that skill.
2. **Given** a skill that has just produced feedback, **When** the user inspects the feedback, **Then** the scope is limited to the current operation and does not attempt a whole-project/global assessment.
3. **Given** a newly authored skill, **When** it is created, **Then** it includes the feedback step by default (a skill without a feedback step is treated as non-conformant).

---

### User Story 2 - Complex-command self-feedback at end of execution (Priority: P2)

As an end user running a complex Spec Kit command, when the command reaches the point where it would normally prompt me to perform a Git commit, I want the command to also generate feedback that reviews the entire execution against the command's description/flow and summarizes optimization points for that command, so that friction and defects in complex commands are captured close to where they occurred.

**Why this priority**: Commands are numerous, but only a subset are complex enough to justify feedback. This story delivers the command-side of the mechanism and depends on the same feedback concept established in US1, so it comes second.

**Independent Test**: Run a command that qualifies as complex (per the process-interaction criteria) to completion and confirm that, at the wrap-up stage (alongside the existing Git-commit prompt timing), it emits a command-scoped feedback entry reviewing the run and listing optimization points for that command.

**Acceptance Scenarios**:

1. **Given** a command classified as complex, **When** it finishes and reaches the Git-commit prompt stage, **Then** it also generates a command-level feedback entry summarizing optimization points based on the command description and the actual execution.
2. **Given** a command classified as simple, **When** it finishes, **Then** no feedback entry is generated for that run.
3. **Given** a complex command's feedback, **When** it is reviewed, **Then** its scope is the current command execution only and it is clearly distinct from the global `/speckit.review` report.

---

### User Story 3 - Selective triggering to protect execution efficiency (Priority: P3)

As an end user, I want feedback generation to occur only on long-running key flows and never scattered across every trivial step, so that my day-to-day execution speed is not degraded by constant feedback prompts.

**Why this priority**: This is the guardrail that keeps the mechanism from becoming a productivity tax. It refines US1/US2 rather than standing wholly alone, so it is P3, but it is essential to the user's stated intent ("不能随机散落在所有执行流程上").

**Independent Test**: Execute a mix of short/trivial flows and long-running key flows; confirm feedback is produced only for the long-running key flows and that short flows complete with zero feedback overhead.

**Acceptance Scenarios**:

1. **Given** a trivial or short-lived operation, **When** it completes, **Then** no feedback is generated and no extra prompts appear.
2. **Given** a long-running key flow, **When** it completes, **Then** exactly one feedback entry is generated at the wrap-up stage (not repeatedly during the flow).
3. **Given** the set of framework skills and commands, **When** the triggering policy is applied, **Then** feedback attaches only to flows that meet the qualification (all skills; complex commands per the process-interaction criteria).

---

### Edge Cases

- **Aborted or failed flow**: If a skill/command errors out or is interrupted before reaching its wrap-up stage, feedback generation should be skipped or clearly marked as based on a partial run, rather than fabricating a review of work that did not complete.
- **Nested execution**: When a command invokes a skill (or a skill invokes another skill), feedback must not be duplicated redundantly for the same unit of work; each qualifying unit produces feedback for its own scope only.
- **No optimization points found**: If the execution was clean, the feedback must still be produced but may explicitly state "no significant optimization points identified this run" rather than inventing issues.
- **Overlap with global review**: Local feedback must not restate a whole-project assessment; it must stay within the current operation to avoid duplicating `/speckit.review`.
- **Efficiency regression**: If feedback starts appearing on trivial flows, this is a defect against the selective-triggering requirement.
- **Below-threshold accumulation**: While the Feedback Store holds fewer entries than the threshold, the consolidated submission prompt MUST NOT be raised; entries simply accumulate.
- **Concurrent writes to the store**: Multiple flows writing feedback to `.specify/memory/feedback/` must not corrupt or lose entries.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The framework MUST define a feedback mechanism that, at the wrap-up stage of a qualifying execution flow, reviews the just-completed execution and produces optimization points scoped to the specific unit (skill or command) that ran.
- **FR-002**: Every skill MUST include a feedback step by default; a skill lacking a feedback step is considered non-conformant with the framework standard.
- **FR-003**: Feedback for a unit MUST be derived from BOTH (a) the unit's own declared description/purpose/flow and (b) the actual execution that just occurred, and MUST summarize concrete optimization points for that unit.
- **FR-004**: Feedback MUST be generated at the same lifecycle timing already used to prompt the user for a Git commit (i.e., near the end of the flow), not mid-flow.
- **FR-005**: Local feedback MUST be scoped to the current operation only and MUST remain distinct in scope from the global-perspective `/speckit.review` report.
- **FR-006**: Commands MUST generate feedback only when they involve complex process interaction. A command qualifies if it meets ANY of: (a) it invokes third-party scripts or command-line tools; (b) its output is consumed as input by another flow; or (c) it consumes the output produced by another flow. A command meeting none of these MUST NOT generate feedback.
- **FR-007**: Feedback MUST NOT be triggered on trivial or short-lived flows; it attaches only to long-running key flows so overall execution efficiency is preserved.
- **FR-008**: Feedback MUST NOT be generated more than once per qualifying unit per run, and nested invocations MUST NOT duplicate feedback for the same unit of work.
- **FR-009**: When an execution is aborted, interrupted, or fails before wrap-up, the framework MUST either skip feedback or clearly label it as covering a partial/failed run rather than presenting it as a complete review.
- **FR-010**: The feedback capability MUST be applied uniformly, so that authoring a new skill (and a new complex command) results in the feedback step being present by convention rather than added ad hoc.
- **FR-011**: Generated feedback MUST be recorded and persisted to a dedicated feedback store under `.specify/memory/feedback/`, accumulating entries across runs. When the accumulated feedback reaches a defined threshold, the framework MUST prompt the user in a single consolidated notification to submit the collected feedback to the Spec Kit developers.
- **FR-012**: Feedback content MUST be produced by the executing agent's self-reflection (agent-generated). The mechanism MUST NOT require soliciting feedback content from the human user at wrap-up.

### Key Entities *(include if requirement involves data)*

- **Feedback Entry**: A record produced at the wrap-up of a qualifying flow. Attributes (conceptual): target unit identifier, target type (skill or command), a short review of the just-completed execution, a list of optimization points, scope indicator (`local`/current-operation), and execution context (e.g., which run it refers to). Does not include global/project-wide assessment.
- **Feedback Trigger Policy**: The rule set that decides which flows produce feedback — "all skills by default" plus "complex commands (process-interaction criteria) only" — and explicitly excludes trivial/short flows.
- **Target Unit**: The skill or command being evaluated; the feedback is bound to this unit's declared description/purpose so optimization points are specific to it.
- **Global Review Report**: The existing whole-project, global-perspective feedback artifact (`/speckit.review`), referenced here only to delineate scope — local Feedback Entries complement it and must not duplicate its global scope.
- **Feedback Store**: The accumulating collection of Feedback Entries persisted under `.specify/memory/feedback/`. Attributes (conceptual): the set of recorded entries and an accumulation count used to decide when to raise the consolidated submission prompt.
- **Submission Prompt**: A consolidated, one-time notification raised when the Feedback Store reaches the defined accumulation threshold, inviting the user to submit collected feedback to the Spec Kit developers.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of framework skills include a feedback step by default (no conformant skill ships without one).
- **SC-002**: Feedback appears on 100% of runs of commands classified as complex and on 0% of runs of commands classified as simple.
- **SC-003**: Every generated feedback entry references the target unit's stated purpose and contains at least one actionable, unit-specific optimization point (or an explicit "no significant optimization points this run" statement).
- **SC-004**: Trivial/short flows complete with zero feedback prompts, so users experience no added wrap-up interaction on those flows.
- **SC-005**: Each qualifying flow produces at most one feedback entry per run (no duplication across nested invocations).
- **SC-006**: 100% of local feedback entries stay within current-operation scope (reviewers can distinguish them from the global `/speckit.review` report with no scope overlap flagged).
- **SC-007**: When accumulated feedback in the store reaches the defined threshold, the user is prompted exactly once (consolidated) to submit it to Spec Kit developers; below the threshold, no submission prompt appears.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Inventory scan of all skill definitions checking for the presence of a feedback step; measured whenever skills are added or changed.
- **SC-002 Source**: Sampled execution logs/transcripts of complex vs. simple command runs, comparing presence/absence of feedback against the command classification; measured per release or on a rolling sample.
- **SC-003 Source**: Manual/assisted audit of a sample of generated feedback entries against the two content requirements (purpose reference + actionable optimization point); measured on a rolling sample.
- **SC-004 Source**: Timing/interaction observation of trivial-flow runs confirming zero feedback prompts; measured on a rolling sample of short flows.
- **SC-005 Source**: Review of runs that involve nested skill/command invocation, counting feedback entries per unit per run.
- **SC-006 Source**: Reviewer audit comparing local feedback entries to global review reports for scope overlap; measured on a rolling sample.
- **SC-007 Source**: Inspection of the `.specify/memory/feedback/` store and run transcripts around the threshold boundary, confirming exactly one consolidated submission prompt at/after threshold and none below it.

## Assumptions

- The "wrap-up stage" that already prompts users for a Git commit is the intended anchor point for feedback timing (per the user's "类似提示用户进行 Git commit 的时机").
- The existing `/speckit.review` command remains the owner of global/whole-project feedback; this feature adds only the distributed, local, per-operation layer and does not replace or restructure `/speckit.review`.
- All skills qualify for feedback by default; for commands, the qualifying condition is complex process interaction — invoking third-party scripts/CLI tools, or producing/consuming another flow's I/O (FR-006).
- Feedback is agent-generated self-reflection with no user-input step at wrap-up (FR-012).
- The feedback store lives under `.specify/memory/feedback/`; the exact accumulation threshold value and the store's on-disk format are implementation details to be settled during `/speckit.plan`.
- Agents/roles are governed indirectly through the skills and commands they run; this feature does not, in its MVP, add a separate agent-only feedback surface beyond skills and commands (agents are mentioned as sources of imperfection, addressed via the flows they execute).

## Clarifications

### Session 2026-07-13

- Q: How should this spec be bound to a Feature (no existing match in features.md)? → A: Create new Feature 028 "Feedback Mechanism".
- Q: Where should generated local feedback go, and who consumes it (FR-011)? → A: Record and persist to a dedicated store under `.specify/memory/feedback/`; when accumulated feedback reaches a defined threshold, prompt the user in a consolidated way to submit it to the Spec Kit developers.
- Q: Who produces the feedback content at wrap-up (FR-012)? → A: The executing agent's self-reflection (agent-generated); no user-solicited input.
- Q: What makes a command "complex enough" to require feedback (FR-006)? → A: Complex process-interaction flows — those that (a) invoke third-party scripts/CLI tools, (b) produce output consumed by another flow, or (c) consume another flow's output.
