# Requirements Specification: Task Complexity Rubric in Generated Instructions

**Requirement Branch**: `031-task-complexity-rubric`  
**Created**: 2026-07-20  
**Status**: Draft  
**Input**: User description: "在instructions命令中最终生成的instructions文档中需要添加一个任务复杂程度评估表,大语言模型需要根据任务的负责程度决定思考的深度,以此来评估效率和质量."

> **Input interpretation note**: 「任务的**负责**程度」 is read as 「任务的**复杂**程度」 (task **complexity**) — a near-homophone dictation fix (fùzé → fùzá), consistent with 「任务复杂程度评估表」 earlier in the same input.

## Related Feature *(mandatory)*

**Feature ID**: 032  
**Feature Name**: Task Complexity Rubric

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Agent calibrates thinking depth from the rubric (Priority: P1)

An AI coding agent starts a new task in a project. It reads the project instructions document, finds the **Task Complexity Rubric**, matches the task against the rubric's signals to place it in a complexity tier, and adopts the thinking depth that tier prescribes — investing little effort in trivial tasks and deep effort in complex, high-stakes ones.

**Why this priority**: This is the core value. Without an agent-consumable rubric in the instructions document, the intended efficiency/quality calibration never happens. This story alone delivers the feature's purpose and is independently demonstrable.

**Independent Test**: Give an agent an instructions document that contains the rubric plus a set of sample tasks; verify that the agent references the rubric, selects a tier per task, and states a thinking-depth level consistent with that tier.

**Acceptance Scenarios**:

1. **Given** an instructions document containing the rubric, **When** the agent receives a trivial task (e.g., a one-line, well-scoped edit), **Then** it selects the lowest complexity tier and applies minimal exploration/planning rather than exhaustive analysis.
2. **Given** the same document, **When** the agent receives a broad, uncertain, multi-file task, **Then** it selects a high complexity tier and applies deeper exploration, explicit planning, and verification.
3. **Given** a task whose signals span two tiers, **When** the agent classifies it, **Then** it follows the rubric's tie-breaking rule and does not stall on the ambiguity.

---

### User Story 2 - Fresh project instructions include the rubric (Priority: P2)

A developer runs `/speckit.instructions` in a project that has no instructions document yet. The generated `.specify/instructions.md` contains a Task Complexity Rubric section, with any template placeholders resolved to concrete content.

**Why this priority**: The rubric must actually appear in newly generated instructions for Story 1 to be possible. It is the primary delivery mechanism for the artifact.

**Independent Test**: In a clean workspace, run the instructions generation flow and confirm the output file contains the rubric section under its stable heading.

**Acceptance Scenarios**:

1. **Given** a project with no `.specify/instructions.md`, **When** `/speckit.instructions` runs, **Then** the generated file contains the rubric section under its stable heading.
2. **Given** the generated file, **When** it is inspected, **Then** the rubric contains distinct tiers, per-tier signals, per-tier thinking-depth prescriptions, a tie-breaking rule, and a default tier — with no unresolved template placeholders.

---

### User Story 3 - Existing instructions gain the rubric non-destructively (Priority: P3)

A developer runs `/speckit.instructions` on a project whose instructions document predates this feature. The refresh inserts the missing rubric section at a structurally appropriate place while leaving all other hand-authored content byte-for-byte unchanged. If the user has already customized their own rubric, it is preserved rather than overwritten.

**Why this priority**: Existing projects must adopt the rubric without losing accumulated, hand-authored knowledge — a core constraint of the instructions refresh model. It is lower priority than P1/P2 only because it targets migration rather than the primary behavior.

**Independent Test**: Take an instructions document that lacks the rubric, run the refresh, and diff before/after to confirm the rubric was added additively and nothing else changed; separately, take a document with a user-customized rubric and confirm the refresh leaves it intact.

**Acceptance Scenarios**:

1. **Given** an existing instructions document with no rubric, **When** the instructions refresh runs, **Then** the rubric section is inserted and every other section is unchanged.
2. **Given** an existing instructions document that already contains a user-customized rubric, **When** the refresh runs, **Then** the user's rubric content is preserved and not overwritten.

---

### Edge Cases

- **Conflicting signals across dimensions** (e.g., a one-line change that nonetheless touches a high-blast-radius shared file): the rubric must give a deterministic tie-breaking rule (default to the higher tier when signals conflict).
- **Unclassifiable or under-specified task** (vague or empty task description): the rubric must define a safe default tier so the agent never lacks guidance.
- **User-authored content precedence**: when a similarly named or customized rubric already exists in the instructions document, regeneration must preserve the user's version (user edits are authoritative).
- **Over-thinking guard**: the rubric must discourage escalating trivial tasks to deep-analysis tiers, since that harms efficiency — the trade-off is symmetric, not "always think more".
- **Stale rubric in backups**: recovery of content from older instructions backups must not resurrect an obsolete rubric that conflicts with the current template-provided one.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The generated project instructions document (`.specify/instructions.md`) MUST include a Task Complexity Rubric presented as a table, discoverable under a single stable heading (see [[STR-001]]).
- **FR-002**: The rubric MUST classify tasks into a small, finite set of clearly labeled complexity tiers that are mutually distinguishable.
- **FR-003**: The rubric MUST enumerate observable signals used to place a task in a tier (for example: scope/size, uncertainty or novelty, blast radius/reversibility, and cross-cutting impact).
- **FR-004**: For each tier, the rubric MUST prescribe a corresponding thinking-depth level expressed as concrete agent behavior (extent of exploration, whether explicit planning is expected, and level of verification), so that "depth" is actionable rather than abstract.
- **FR-005**: The rubric MUST state a tie-breaking rule for tasks whose signals span multiple tiers (default to the higher tier when in doubt).
- **FR-006**: The rubric MUST define a default tier to apply when a task cannot yet be classified or is under-specified.
- **FR-007**: The rubric MUST make the efficiency-versus-quality trade-off explicit — stating that the goal is to avoid both under-thinking complex tasks (quality risk) and over-thinking trivial tasks (efficiency waste).
- **FR-008**: The rubric content MUST be technology-agnostic and project-neutral so it is valid for any project generated by the toolkit, and therefore MUST live in the shared instructions template rather than in project-specific prose.
- **FR-009**: `/speckit.instructions` MUST include the rubric section when generating a fresh instructions document, with no unresolved placeholders remaining.
- **FR-010**: `/speckit.instructions` MUST insert the rubric section into an existing instructions document that lacks it, placing it at a structurally appropriate location without altering unrelated, user-authored content.
- **FR-011**: `/speckit.instructions` MUST NOT overwrite a rubric section that a user has customized; user-authored content takes precedence and is preserved across regenerations.
- **FR-012**: The rubric's heading MUST be stable and consistent across projects so agents and downstream `/speckit.*` steps can reliably locate and reference it.

### Key Entities *(include if requirement involves data)*

- **Task Complexity Rubric**: The artifact embedded in the instructions document that maps complexity signals to tiers and each tier to a thinking-depth prescription; the single reference an agent consults to calibrate effort.
- **Complexity Tier**: A named band of task difficulty (e.g., from trivial to high-stakes) carrying its own signals and thinking-depth prescription.
- **Thinking-Depth Level**: The prescribed effort profile for a tier — how much exploration, planning, and verification the agent should perform.

### Assumptions

- The instructions document remains the canonical, agent-facing context file, so it is the correct home for cross-cutting agent guidance like this rubric.
- Agents that read the instructions document are capable of self-selecting a thinking-depth level when given explicit, behavior-anchored guidance.
- A small number of tiers (roughly 3–5) is sufficient to be useful without being burdensome; the exact count and labels are a design decision for the planning phase.
- The rubric is guidance, not a hard gate: it shapes effort allocation but does not block or fail any task.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After running `/speckit.instructions` in a fresh workspace, the generated instructions document contains the rubric section under its stable heading in 100% of runs.
- **SC-002**: When refreshing an existing instructions document that lacks the rubric, the rubric is added while 100% of previously existing user-authored sections remain byte-for-byte unchanged.
- **SC-003**: In a review of at least 20 diverse sample tasks, independent reviewers agree with the tier the rubric assigns for at least 90% of tasks (the rubric is unambiguous enough to apply consistently).
- **SC-004**: Across a benchmark of at least 20 tasks, an agent's chosen thinking-depth level matches the rubric's prescription for its assigned tier in at least 85% of cases.
- **SC-005**: A first-time reader can locate and read the rubric section within 30 seconds of opening the instructions document (it is a single, self-contained, clearly headed section).

### Measurement Sources & Collection Methods

- **SC-001 Source**: Automated check — run the generation flow in a temporary clean workspace and assert the presence of the rubric heading ([[STR-001]]) in the output file; measured on every change to the instructions command/template.
- **SC-002 Source**: Automated before/after diff — run the refresh on a fixture instructions document lacking the rubric and confirm the change set is a pure additive insertion; measured in CI.
- **SC-003 Source**: Manual review artefact — a reviewer tally (e.g., 3 reviewers × 20 tasks) recorded under the feature directory; measured once at acceptance and on major rubric edits.
- **SC-004 Source**: LLM benchmark harness — present each task together with the rubric, capture the agent's chosen tier/depth versus the rubric-assigned tier; measured at acceptance and on major rubric edits.
- **SC-005 Source**: Timed usability observation recorded alongside the SC-003 review artefact.

## Shared Strings

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "## Task Complexity Rubric" | FR-001, FR-012, SC-001, SC-001 Source |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-07-20

- Q: How should this spec bind to the feature registry (Related Feature was unresolved)? → A: Create a new Feature 032 "Task Complexity Rubric", tracked as a distinct agent-behavior calibration mechanism delivered via the instructions doc (mirroring Glossary/Feedback), rather than binding to the existing Instructions Command feature (008).
