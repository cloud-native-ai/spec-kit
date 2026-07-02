# Feature Specification: EEI Agent Triad (Executor-Evaluator-Improver)

**Feature Branch**: `022-eei-agent-triad`  
**Created**: 2026-07-02  
**Status**: Draft  
**Input**: User description: "在 Role-Based Agent 架构上增加 Executor-Evaluator-Improver 三角色协作维度"

## Related Feature *(mandatory)*

**Feature ID**: 019  
**Feature Name**: Agents Command

## Context & Motivation

This specification codifies the multi-subagent collaboration pattern discovered during a successful goal-driven optimization session. In that session, a K8s infrastructure diagram was iteratively improved from a quality score of 49/100 to 91/100 over 17 rounds using three specialized subagent roles:

- **Drawing Agent (Executor)**: Read skill references, produced PlantUML diagrams, rendered to PNG
- **Scoring Agent (Evaluator)**: Read rendered image, evaluated on correctness (60%) + aesthetics (40%), gave numeric score + specific improvement suggestions
- **Skill Optimizer Agent (Improver)**: Received evaluator feedback, modified skill reference files (howto guides, best practices) to improve the executor's next run

The pattern proved highly effective: each round produced measurable improvement, the agents operated independently (no shared context pollution), and the orchestrator managed context passing between them.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Quality-Gated Iterative Task Execution (Priority: P1)

A user sets a quality goal (e.g., "draw a diagram scoring >90 on correctness and aesthetics") and the system automatically orchestrates an executor-evaluator-improver loop until the goal is met.

**Why this priority**: This is the core value proposition — the user gets progressively higher-quality output without manually coordinating multiple agents.

**Independent Test**: Can be fully tested by invoking a goal-driven task (e.g., "draw a K8s architecture diagram and optimize until score >80") and verifying that (1) the executor produces output, (2) the evaluator scores it, (3) the improver modifies the environment if the score is below threshold, and (4) the loop terminates when the score exceeds the threshold.

**Acceptance Scenarios**:

1. **Given** a user has set a quality goal with a numeric threshold, **When** the executor produces output that scores below the threshold, **Then** the system automatically invokes the improver and re-runs the executor with the updated environment, repeating until the threshold is met or a maximum iteration count is reached.
2. **Given** the executor produces output that scores above the threshold on the first attempt, **Then** the system stops immediately and reports success without invoking the improver.
3. **Given** the maximum iteration count is reached without meeting the threshold, **Then** the system stops, reports the best score achieved across all iterations, and presents the best-scoring output.

---

### User Story 2 - Independent Agent Context Isolation (Priority: P1)

Each agent in the triad operates with its own context, without inheriting or leaking state from the other agents. The orchestrator is responsible for selecting WHAT context to pass between them.

**Why this priority**: Context isolation is what makes the pattern work — the evaluator must assess output independently, and the executor must re-read the environment fresh each iteration.

**Independent Test**: Verify that (1) the evaluator receives only the executor's output (not the executor's prompt or reasoning), (2) the executor re-reads its skill/reference files each iteration (not cached from a previous run), and (3) the improver receives only the evaluator's feedback (not the executor's internal state).

**Acceptance Scenarios**:

1. **Given** the executor has completed its work, **When** the evaluator is invoked, **Then** the evaluator receives only the executor's output artifacts (files, images) and scoring criteria — never the executor's original prompt, internal reasoning, or conversation history.
2. **Given** the improver has modified the executor's environment (skill files, instructions), **When** the executor runs again, **Then** the executor reads the latest version of all reference files as specified in its prompt, not from any cache or prior context.
3. **Given** any agent fails during execution, **Then** the failure is reported to the orchestrator without propagating to the other agents' next invocations.

---

### User Story 3 - Dual-Target Improvement (Priority: P2)

The improver can modify both the executor's environment (external resources) and the executor itself (prompt, context, instructions).

**Why this priority**: The session proved that improving the executor's environment (skill files, best practices docs) was more impactful than just re-running with the same instructions. The improver's dual target — environment AND executor — is what drives convergent improvement.

**Independent Test**: Verify that the improver can (1) edit files in the executor's reference path (environment improvement), and (2) suggest prompt modifications for the next executor invocation (executor improvement). Both improvement types should be traceable in the iteration log.

**Acceptance Scenarios**:

1. **Given** the evaluator reports "arrow congestion due to ortho line routing," **When** the improver acts, **Then** the improver modifies the executor's skill reference files (e.g., adding layout guidance to best practices) — this is environment improvement.
2. **Given** the evaluator reports "missing Ingress component," **When** the improver acts, **Then** the improver adds "include Ingress" to the executor's prompt or context for the next iteration — this is executor improvement.
3. **Given** the improver has made changes, **When** the next iteration begins, **Then** the changes are traceable: modified files are logged, prompt adjustments are recorded, and the iteration report shows what was changed and why.

---

### User Story 4 - Configurable Scoring Dimensions (Priority: P2)

The evaluator's scoring criteria and weights are configurable per task, allowing the user to define what "quality" means for their specific goal.

**Why this priority**: Different tasks require different quality definitions. The K8s session used correctness (60%) + aesthetics (40%), but a code review task might use correctness (70%) + maintainability (30%).

**Independent Test**: Verify that the evaluator accepts scoring dimension definitions (name + weight) and produces a weighted total score.

**Acceptance Scenarios**:

1. **Given** the user defines dimensions `{correctness: 60%, aesthetics: 40%}`, **When** the evaluator scores, **Then** the output includes per-dimension scores and a weighted total.
2. **Given** the user defines dimensions `{correctness: 70%, performance: 30%}`, **When** the evaluator scores a different type of output, **Then** the evaluator adapts its criteria to the new dimensions.
3. **Given** no dimensions are specified, **Then** the system uses a default scoring configuration appropriate to the task type.

---

### User Story 5 - Iteration History and Convergence Tracking (Priority: P3)

The system maintains a history of all iterations, enabling the user to see the improvement trajectory and identify which changes had the most impact.

**Why this priority**: Understanding which improvements drove the biggest score gains helps refine future optimization strategies.

**Independent Test**: Verify that after N iterations, the system can produce a summary showing: iteration number, score per dimension, weighted total, key changes made, and score delta from previous iteration.

**Acceptance Scenarios**:

1. **Given** 5 iterations have completed, **When** the user requests the iteration history, **Then** the system displays a table showing round number, scores, delta, and key changes per round.
2. **Given** an iteration produces a score regression (lower than previous), **Then** the iteration history flags the regression and the improver's changes that caused it.

---

### Edge Cases

- What happens when the evaluator and improver disagree (improver's changes cause score regression)?
  → The system tracks the best-scoring iteration. If 3 consecutive regressions occur, the system reverts to the best-known state and tries a different improvement strategy.
- What happens when the executor cannot read the improved environment?
  → The system validates that all file paths referenced in the executor's prompt exist before each iteration.
- What happens when the maximum iteration count is very high (e.g., 100)?
  → The system enforces a configurable hard limit (default: 20) and warns the user at 50% of the limit.
- What happens when the evaluator scores 100/100?
  → Perfect score stops the loop immediately. The result is flagged as "optimal" in the iteration history.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST support defining a triad of three sub-agent roles (Executor, Evaluator, Improver) within a single Role-Based Agent scope
- **FR-002**: The system MUST orchestrate the triad in a loop: Executor → Evaluator → (if below threshold) Improver → Executor, until the score exceeds the configured threshold or the maximum iteration count is reached
- **FR-003**: Each sub-agent MUST be invoked as an independent subagent with its own prompt and context — no shared conversation state between triad members
- **FR-004**: The Executor MUST re-read all referenced environment files (skills, instructions, templates) at the start of each iteration, ensuring it always uses the latest version modified by the Improver
- **FR-005**: The Evaluator MUST produce a structured output containing: per-dimension scores, weighted total, and specific improvement suggestions
- **FR-006**: The Improver MUST receive the Evaluator's structured feedback and produce two categories of changes: (a) environment modifications (files, configs) and (b) executor prompt/context modifications
- **FR-007**: The system MUST track iteration history including: round number, scores, changes made, and score deltas
- **FR-008**: The system MUST support configurable scoring dimensions with user-defined weights (e.g., `{correctness: 0.6, aesthetics: 0.4}`)
- **FR-009**: The system MUST enforce a configurable maximum iteration limit (default: 20) to prevent infinite loops
- **FR-010**: The system MUST preserve the best-scoring output across all iterations and return it if the threshold is never met
- **FR-011**: The Improver's environment modifications MUST be limited to files within the agent's designated workspace (skill directories, template directories, instruction files) — never system files or user code outside the workspace
- **FR-012**: The triad pattern MUST be composable with the existing Role-Based Agent architecture — any role (Requirements Analyst, System Designer, etc.) can optionally adopt the EEI triad pattern

### Key Entities

- **Triad**: A configured set of three sub-agent definitions (Executor, Evaluator, Improver) bound to a single Role-Based Agent
- **Iteration**: One complete cycle of Executor → Evaluator (→ optional Improver), including all inputs, outputs, scores, and changes
- **Scoring Dimensions**: Named quality criteria with weights that define "quality" for a specific task
- **Environment**: The set of files, configurations, and instructions that the Executor reads to perform its work
- **Iteration History**: Ordered log of all iterations with scores, deltas, changes, and convergence metrics

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can set up a goal-driven EEI loop that converges to a score above the configured threshold within the configured iteration limit, in at least 80% of attempts
- **SC-002**: Each iteration in the loop completes within 3 minutes for typical tasks (diagram generation, code review, document generation)
- **SC-003**: The iteration history clearly shows score progression, enabling the user to identify which improvements had the most impact
- **SC-004**: The triad pattern can be applied to at least 3 different Role-Based Agent types (e.g., diagram drawing, code review, document writing) without modification to the core loop logic
- **SC-005**: Environment modifications made by the Improver are traceable — the user can review exactly what changed between iterations
- **SC-006**: No context leakage between triad members — verified by the evaluator never referencing the executor's internal prompt or reasoning in its feedback

### Measurement Sources & Collection Methods

- **SC-001 Source**: Goal completion rate tracked across EEI loop invocations; measured by threshold-met vs max-iteration outcomes
- **SC-002 Source**: Iteration duration measured from executor invocation to evaluator output completion; median across 10+ iterations
- **SC-003 Source**: User review of iteration history table; qualitative assessment of score trajectory visibility
- **SC-004 Source**: Successful application of EEI pattern across 3 distinct domain tasks; documented in test cases
- **SC-005 Source**: Diff logs generated per iteration showing file changes and prompt modifications
- **SC-006 Source**: Audit of evaluator prompts and outputs to confirm no executor context leakage

## Assumptions

- The existing Role-Based Agent architecture supports spawning independent subagents (confirmed by current implementation using the Agent tool)
- The reference session (K8s diagram optimization, 49→91 score) is representative of real-world EEI loop effectiveness
- Scoring is done by an LLM-based evaluator (not a deterministic metric), so scores have natural variability of ±3 points between runs
- The orchestrator runs in the main agent's context and manages context passing between triad members
- File system access for environment modification follows the existing skill/template file structure

## Clarifications

### Session 2026-07-02

- Q: Which existing Feature should this spec belong to? → A: Feature 019 (Agents Command) — the EEI triad extends the role-based agent system
