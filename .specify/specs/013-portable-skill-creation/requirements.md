# Feature Specification: Portable Skill Creation

**Feature Branch**: `013-portable-skill-creation`  
**Created**: 2026-06-05  
**Status**: Draft  
**Input**: User description: "优化templates/commands/skills.md相关的命令和skills/create-skills中的skill实现,需要让通过这个命令和skill创建的skill更加通用,比如移除tools的逻辑(创建tools的环境也就是创建skill的环境和执行skill的环境可能存在差异,tools有可能不可用)."

## Related Feature *(mandatory)*

**Feature ID**: 013  
**Feature Name**: Skills Command

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Environment-Portable Skill Creation (Priority: P1)

A skill author uses `/speckit.skills` (backed by the `create-skills` skill) to create a new skill on their development machine. The newly created skill does not contain any environment-specific tool manifest references or tool-discovery steps. When a different user later invokes this skill on a machine with a different set of available tools (or no tool manifests at all), the skill executes successfully without errors related to missing tools.

**Why this priority**: This is the core problem. Skills currently embed tool-discovery logic (`refresh-tools.sh`) and reference auto-generated tool manifest files (`tools/system.json`, `tools/shell.json`, `tools/project.json`). When the skill is used in an environment where these scripts or manifests are unavailable, the skill fails or produces misleading instructions. Removing this coupling is the primary deliverable.

**Independent Test**: Create a skill using the updated `create-skills` workflow, then verify the resulting `SKILL.md` contains zero references to `refresh-tools.sh`, `tools/system.json`, `tools/shell.json`, `tools/project.json`, or the "Obtain available tools information" step.

**Acceptance Scenarios**:

1. **Given** a user invokes `create-skills` to create a new skill, **When** the skill is scaffolded, **Then** the resulting `SKILL.md` contains no tool-manifest references or tool-discovery steps.
2. **Given** a newly created skill, **When** it is executed on a machine that does not have `refresh-tools.sh` or tool manifest files, **Then** the skill executes its workflow without errors or missing-resource warnings related to tools.
3. **Given** the `create-skills/SKILL.md` workflow definition, **When** a user reads the workflow steps, **Then** there is no "Obtain available tools information" step.

---

### User Story 2 - Portable Skill Template (Priority: P1)

A skill author creates a new skill and receives a scaffolded `SKILL.md` from the skill template (`templates/skills-template.md`). The template no longer includes an "Available Tools & Resources" section with tool manifest references. Instead, the template focuses on Skill-owned resources (scripts, references, assets) that travel with the skill directory.

**Why this priority**: The template is the source for every new skill. If the template includes tool-specific boilerplate, every created skill inherits that portability problem. Fixing the template fixes all future skills at once.

**Independent Test**: Read `templates/skills-template.md` and verify it does not contain a "Tools" subsection referencing `tools/system.json`, `tools/shell.json`, `tools/project.json`, or `refresh-tools.sh`.

**Acceptance Scenarios**:

1. **Given** the current skill template, **When** it is used to scaffold a new skill, **Then** the generated `SKILL.md` omits the "Available Tools & Resources" > "Tools" subsection and its tool-manifest refresh instructions.
2. **Given** a skill directory created from the updated template, **When** the directory contents are listed, **Then** no `tools/` subdirectory is auto-created during scaffolding.

---

### User Story 3 - Simplified Orchestration Template (Priority: P2)

The `/speckit.skills` orchestration template (`templates/commands/skills.md`) references tool manifests in the modernization checklist and skill directory layout. These references are updated to remove the assumption that tool manifests are always present or needed.

**Why this priority**: The orchestration template governs how both new and existing skills are validated. Removing tool-manifest requirements from validation prevents false negatives when a skill directory intentionally omits tool manifests.

**Independent Test**: Read `templates/commands/skills.md` and verify the directory layout example, the modernization checklist, and the validation/report steps no longer treat `tools/` as a required or expected directory for new skills.

**Acceptance Scenarios**:

1. **Given** the orchestration template's directory layout example, **When** a user reads it, **Then** the `tools/` directory is either removed or explicitly marked as legacy/optional with a note that it is no longer auto-generated.
2. **Given** the modernization checklist in the orchestration template, **When** Step 6 ("Tool manifests") is evaluated, **Then** it no longer requires running `refresh-tools.sh` or checking for `tools/*.json` files as a mandatory modernization step.

---

### User Story 4 - Script Behavior Update (Priority: P3)

The `scripts/bash/create-new-skill.sh` script currently calls `refresh_tools_for_target()` to auto-generate tool manifest files into every new skill's `tools/` directory. After the update, the script no longer generates tool manifests during skill creation or refresh.

**Why this priority**: The script is the final enforcement point. Even if templates and SKILL.md are updated, the script would re-introduce tool manifests on every `--refresh-only` or creation run unless also updated.

**Independent Test**: Run `create-new-skill.sh` for a new skill and verify no `tools/` directory or `*.json` manifest files are created in the skill directory.

**Acceptance Scenarios**:

1. **Given** a user runs `create-new-skill.sh --json <name>` to create a new skill, **When** the script completes, **Then** the skill directory does not contain a `tools/` subdirectory.
2. **Given** a user runs `create-new-skill.sh --refresh-only --name <name> --json`, **When** the script completes, **Then** no tool manifest files are written to the skill directory (the `--refresh-only` flag still refreshes `skill_id` in frontmatter but skips tool manifests).

---

### Edge Cases

- What happens when an existing skill already has a `tools/` directory with custom (non-auto-generated) content? The update must not delete user-authored files inside `tools/`; it only stops *auto-generating* manifests.
- What happens when `improve-skills` references tool manifests as part of its modernization checklist? The modernization checklist step for tool manifests should be removed or made a no-op so existing skills are not flagged for missing tool manifests.
- What happens if a skill author explicitly wants to reference tools in their skill? They can still manually create a `tools/` directory and add content; the change only removes the automatic generation and template boilerplate.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `create-skills/SKILL.md` workflow MUST NOT include a step that runs `refresh-tools.sh` or any tool-discovery script during skill creation.
- **FR-002**: The `create-skills/SKILL.md` workflow MUST NOT reference tool manifest files (`tools/system.json`, `tools/shell.json`, `tools/project.json`) as part of the skill creation process.
- **FR-003**: The `templates/skills-template.md` MUST NOT include an "Available Tools & Resources" > "Tools" subsection that references auto-generated tool manifests.
- **FR-004**: The `templates/skills-template.md` MUST retain sections for scripts, references, and assets as portable, Skill-owned resources.
- **FR-005**: The `templates/commands/skills.md` orchestration template MUST remove or make optional the "Tool manifests" step (current Step 6) in the Spec-Compliance Modernization Checklist.
- **FR-006**: The `templates/commands/skills.md` orchestration template MUST update the directory layout example to remove or mark `tools/` as optional/legacy.
- **FR-007**: The `scripts/bash/create-new-skill.sh` script MUST NOT call `refresh_tools_for_target()` or generate tool manifest JSON files when creating or refreshing a skill.
- **FR-008**: The `scripts/bash/create-new-skill.sh` script MUST continue to support `--refresh-only` for refreshing `skill_id` frontmatter, but without tool manifest generation.
- **FR-009**: The `.specify/skills/create-skills/SKILL.md` mirror MUST be updated to match the canonical `skills/create-skills/SKILL.md` after changes are applied.
- **FR-010**: Existing skills that already contain a `tools/` directory MUST NOT have their `tools/` directory or contents deleted by any automated process introduced by this change.
- **FR-011**: The `skills/create-skills/references/skill-creation-quality-checklist.md` MUST be updated to remove validation items that check for tool manifest presence or tool manifest refresh commands.

### Key Entities

- **Skill Template** (`templates/skills-template.md`): The source-of-truth boilerplate used to scaffold every new `SKILL.md`. Determines the default structure of all created skills.
- **Orchestration Template** (`templates/commands/skills.md`): The `/speckit.skills` command definition that routes creation and improvement, including the modernization checklist.
- **Create-Skills Skill** (`skills/create-skills/SKILL.md`): The skill that implements the creation workflow, currently containing a tool-discovery step.
- **Skill Scaffolding Script** (`scripts/bash/create-new-skill.sh`): The shell script that creates skill directories and generates boilerplate, currently including tool manifest generation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of newly created skills (via `create-skills` or `create-new-skill.sh`) contain zero references to `refresh-tools.sh`, `tools/system.json`, `tools/shell.json`, or `tools/project.json` in their `SKILL.md`.
- **SC-002**: A skill created on one machine executes its documented workflow without errors when transferred to a machine that does not have `refresh-tools.sh` or tool manifests available.
- **SC-003**: The `templates/skills-template.md` contains no tool-manifest boilerplate; the "Available Tools & Resources" section, if present, only covers scripts, references, and assets.
- **SC-004**: Existing skills with manually authored `tools/` directories retain their content unchanged after running any updated scripts.
- **SC-005**: The `create-skills/SKILL.md` workflow has no "Obtain available tools information" step or equivalent.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Structural contract test asserting absence of tool-manifest keywords in newly scaffolded `SKILL.md` files. Run via `pytest -m contract`.
- **SC-002 Source**: Manual or integration test: create a skill, copy the skill directory to an isolated environment without `scripts/bash/`, confirm the `SKILL.md` workflow is self-contained.
- **SC-003 Source**: Static inspection of `templates/skills-template.md` content; can be verified by a contract test.
- **SC-004 Source**: Integration test: create a skill with a pre-existing `tools/` directory containing custom content, run `--refresh-only`, verify `tools/` contents are unchanged.
- **SC-005 Source**: Static inspection of `skills/create-skills/SKILL.md` step list; contract test on step headings.

## Assumptions

- Tool manifests (`tools/*.json`) were originally introduced to help AI agents understand available tools at skill authoring time. This specification assumes that tool awareness is better handled at the *agent runtime* level rather than baked into each skill's static files.
- The `tools/` directory convention is retained as a valid user-authored directory but is no longer auto-generated or required by the validation checklist.
- The `scripts/bash/refresh-tools.sh` script itself is NOT removed or modified — it remains available for other purposes (e.g., `/speckit.tools`). Only its invocation from skill creation flows is removed.

## Clarifications

### Session 2026-06-05

- Q: Which Feature should this spec be bound to? → A: Feature 013 — Skills Command (existing feature covering skill creation, installation, and orchestration).
