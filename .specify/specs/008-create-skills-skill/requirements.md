# Requirements Specification: Create Skills Skill

**Requirement Branch**: `008-create-skills-skill`  
**Created**: 2026-05-10  
**Status**: Draft  
**Input**: User description: "将templates/commands/skills.md中创建skill的逻辑提取出来，独立创建一个名为“create-skills”的skill，放到skills/create-skills目录。"

## Related Feature *(mandatory)*

<!--
  ACTION REQUIRED: Keep the default values as "Need clarification" in the initial draft.
  /speckit.clarify must resolve this section to the final Feature binding before planning.
-->

**Feature ID**: 013  
**Feature Name**: Skills Command

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Create new skills through a dedicated capability (Priority: P1)

As a Spec Kit maintainer, I want skill-creation guidance to live in a dedicated `create-skills` Skill so that command prompts can explicitly delegate skill creation without carrying the full creation workflow inline.

**Why this priority**: This is the core value of the change: it separates reusable Skill-authoring knowledge from the `/speckit.skills` command entrypoint and makes the creation workflow reusable by other commands or agents.

**Independent Test**: Can be tested by requesting creation of a new Skill through the skills command when the target Skill does not exist and verifying that the creation guidance is available from the dedicated `create-skills` Skill rather than only from the command template.

**Acceptance Scenarios**:

1. **Given** the existing skills command contains inline creation guidance, **When** the creation logic is extracted, **Then** a dedicated `create-skills` Skill exists under `skills/create-skills` with clear instructions for creating high-quality Skills.
2. **Given** a user invokes the skills workflow for a Skill that does not exist, **When** the command determines creation is required, **Then** the workflow explicitly routes the creation task to `create-skills`.

---

### User Story 2 - Keep command prompts focused on orchestration (Priority: P2)

As a Spec Kit maintainer, I want `templates/commands/skills.md` to focus on intent parsing, target Skill existence checks, routing, validation, and handoffs so that the command remains concise and easier to maintain.

**Why this priority**: Once creation knowledge is extracted, the command must still remain useful as the explicit entrypoint for `/speckit.skills`; this story protects the command from becoming an oversized prompt again.

**Independent Test**: Can be tested by reviewing the command template and confirming that detailed creation instructions are delegated to `create-skills` while the command still defines creation-vs-improvement routing.

**Acceptance Scenarios**:

1. **Given** the skills command is opened for maintenance, **When** a maintainer reviews its contents, **Then** the command clearly states that missing Skills are created through `create-skills` and existing Skills are improved through `improve-skills`.
2. **Given** a maintainer updates Skill creation methodology, **When** the methodology changes, **Then** the reusable guidance can be updated in `create-skills` without duplicating the same changes in the command prompt.

---

### User Story 3 - Preserve existing skill quality expectations (Priority: P3)

As an AI agent using Spec Kit, I want the extracted `create-skills` Skill to preserve the existing rules for Skill metadata, progressive disclosure, resource directories, registry updates, and validation so that extraction does not reduce output quality.

**Why this priority**: The extraction is only successful if behavior remains equivalent or better for Skill creation while improving separation of concerns.

**Independent Test**: Can be tested by comparing the new `create-skills` Skill against the previous creation guidance and confirming that required creation behaviors remain represented.

**Acceptance Scenarios**:

1. **Given** the extracted Skill is used to create a project-level Skill, **When** the creation is complete, **Then** the resulting Skill has valid frontmatter, clear trigger guidance, appropriate resource organization, and a deterministic registry entry.
2. **Given** the creation request lacks critical metadata, **When** `create-skills` is used, **Then** it asks only the minimum necessary clarification before proceeding.

### Edge Cases

- The requested Skill already exists: the skills command should route to improvement behavior rather than invoking `create-skills` for creation.
- The requested Skill name is invalid or ambiguous: the workflow should ask for clarification instead of creating an incorrectly named Skill.
- The source command contains creation guidance that overlaps with improvement guidance: only creation-specific behavior should move into `create-skills`; improvement behavior remains delegated to `improve-skills`.
- Compatibility entrypoints expose Skills through symlinks or mirrored paths: the canonical Skill content should still be maintained in the intended project Skill directory.
- The creation workflow needs supporting references or scripts: large details should be organized as Skill resources rather than re-expanded inside the command prompt.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a dedicated Skill named `create-skills` for creating new Spec Kit Skills.
- **FR-002**: The `create-skills` Skill MUST be available from the project Skill directory `skills/create-skills`.
- **FR-003**: The `create-skills` Skill MUST preserve the existing creation workflow guidance from the skills command, including metadata extraction, conversation-based workflow distillation, minimal clarification, Skill structure, resource organization, registry updates, validation, and completion reporting.
- **FR-004**: The skills command MUST explicitly route missing target Skills to `create-skills` for creation.
- **FR-005**: The skills command MUST explicitly route existing target Skills to `improve-skills` for refinement or improvement.
- **FR-006**: The skills command MUST retain only orchestration responsibilities needed to parse user intent, determine whether the target Skill exists, select the correct Skill delegation path, and report handoffs or validation expectations.
- **FR-007**: The extracted `create-skills` Skill MUST describe when to create a new Skill from explicit user input and when to derive a new Skill from current conversation history.
- **FR-008**: The extracted `create-skills` Skill MUST instruct agents to keep generated Skill content concise, progressively disclosed, and split into resource directories when details become large.
- **FR-009**: The extracted `create-skills` Skill MUST include quality checks that prevent vague descriptions, invalid Skill names, excessive `SKILL.md` size, missing executable steps, and inconsistent resource paths.
- **FR-010**: The extraction MUST avoid duplicating full creation logic in both the command template and the `create-skills` Skill.
- **FR-011**: Existing improvement guidance MUST continue to be delegated to `improve-skills` rather than merged into `create-skills`.

### Key Entities *(include if requirement involves data)*

- **Skill Creation Capability**: The reusable guidance package that explains how to create a new Skill, including trigger metadata, workflow steps, resource organization, validation, and reporting expectations.
- **Skills Command**: The explicit user-facing command entrypoint that interprets `/speckit.skills` requests and routes to creation or improvement behavior.
- **Target Skill**: The Skill named by the user or inferred from the conversation; its existence determines whether the workflow creates a new Skill or improves an existing one.
- **Skill Resource Registry Entry**: The discoverability metadata recorded for a Skill so future agents can identify and reference it consistently.

### Assumptions

- The existing Skills Command feature is the parent feature for this requirements slice; the initial Related Feature fields remain unresolved until clarification as required by the command workflow.
- `create-skills` is intended for new Skill creation, while `improve-skills` remains responsible for evidence-driven refinement of existing Skills.
- The command remains the explicit `/speckit.skills` entrypoint even after detailed creation guidance is extracted.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Maintainers can identify the creation-vs-improvement routing behavior in the skills command in under 2 minutes.
- **SC-002**: A reviewer can locate all detailed Skill creation guidance in the dedicated `create-skills` Skill without searching through the command template.
- **SC-003**: At least 90% of the previously documented Skill creation responsibilities remain covered after extraction, as verified by a review checklist comparing old guidance to the new Skill.
- **SC-004**: The skills command is reduced to orchestration-focused content while preserving all required user-visible routing outcomes for missing and existing target Skills.
- **SC-005**: A new Skill creation request can be followed end-to-end using `create-skills` without requiring creation-specific instructions from the skills command body.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Manual review of the skills command during implementation review; measure time to identify the routing rule.
- **SC-002 Source**: Manual review of the project Skill directory and generated `SKILL.md`; confirm detailed creation guidance location.
- **SC-003 Source**: Review checklist comparing extracted responsibilities against the pre-extraction skills command content.
- **SC-004 Source**: Diff review of the skills command before and after extraction; confirm detailed creation sections are removed or replaced by delegation language.
- **SC-005 Source**: Dry-run or walkthrough using a representative new Skill request; record whether all required creation decisions are covered by `create-skills`.

## Clarifications

### Session 2026-05-10

- Q: Which Feature should this specification bind to? → A: `013` / `Skills Command`.

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
