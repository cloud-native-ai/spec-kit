# Feature Specification: Add Instructions and Skills Commands

**Feature Branch**: `1000-add-instr-skills-cmds`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "新建/speckit.instructions和/speckit.skills两个命令，/speckit.instructions命令用来根据当前项目的情况生成对应的instructions文档，具的文档和内容可以参考function copilot_generate_instructions的实现。/speckit.skills命令用来生成skills相关文档。"

## Clarifications

### Session 2026-01-28

- Q: How should `/speckit.instructions` handle updates? → A: **Full Regeneration (Safe Backup)**: Rename existing to `.ai/instructions.md.bak` and generate fresh `.ai/instructions.md` from constitution and templates to ensure full compliance.
- Q: How should `/speckit.skills` use feature context? → A: **Targeted Enrichment**: When creating/updating a specific skill, inject relevant context from active Features/Specs (if matching key concepts) into the generated instructions to tailor the skill to the current project state.
- Q: How should `/speckit.skills` handle existing skills? → A: **Smart Append**: If `SKILL.md` exists, append a new "### Spec Context Updates [Date]" section with the new context; do NOT overwrite existing content.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Project Instructions (Priority: P1)

As a developer using spec-kit, I want to quickly generate a comprehensive `.ai/instructions.md` file and associated symlinks, so that my AI agent is immediately effective with project-specific context.

**Why this priority**: Correct agent onboarding is critical for the effectiveness of the entire spec-kit workflow.

**Independent Test**:
Run `/speckit.instructions` in a clean project (or one without instructions).
Verify `.ai/instructions.md` is created with correct content (Goals, Tech Stack, etc.).
Verify symlinks in `.clinerules`, `.github`, etc., are created.

**Acceptance Scenarios**:

1. **Given** a project without `.ai/instructions.md`, **When** I run `/speckit.instructions`, **Then** the file `.ai/instructions.md` is created with a template reminding me to fill in project details.
2. **Given** the file is created, **When** I check `.clinerules`, `.github`, `.lingma`, `.trae`, `.qoder` directories, **Then** symlinks to `.ai/instructions.md` exist.
3. **Given** an existing `.ai/instructions.md`, **When** I run `/speckit.instructions`, **Then** it should not overwrite it without warning (or should handle it gracefully, though the reference script skips if exists).

---

### User Story 2 - Generate Skill Scaffold (Priority: P1)

As a developer, I want to easily create new Agent Skills using a standard command, so that I can extend Copilot's capabilities without manually setting up the directory structure.

**Why this priority**: Skills are a key extensibility mechanism, and manual creation is error-prone.

**Independent Test**:
Run `/speckit.skills` with a skill name or description.
Verify `.github/skills/<skill-name>/SKILL.md` is created.
Verify the file has correct YAML frontmatter.

**Acceptance Scenarios**:

1. **Given** I want to add a testing skill, **When** I run `/speckit.skills` with arguments describing the skill, **Then** a new directory in `.github/skills/` is created.
2. **Given** the directory is created, **When** I check the content, **Then** a `SKILL.md` file exists with `name` and `description` fields populated.

### Edge Cases

- **EC-001**: **Instruction File Exists**: If `.ai/instructions.md` already exists, the command MUST NOT overwrite it without explicit user confirmation or force flag. It should inform the user content exists.
- **EC-002**: **Missing Tool Directories**: If directories like `.clinerules`, `.lingma` do not exist, the command MUST create them before symlinking.
- **EC-003**: **Skills Command Validity**: If `/speckit.skills` is run without a skill name, the agent MUST ask the user for the skill name and description before proceeding.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a `/speckit.instructions` command template located at `templates/commands/instructions.md`.
- **FR-002**: The `/speckit.instructions` command MUST instruct the agent to create `.ai/instructions.md` if it doesn't exist.
- **FR-003**: The `/speckit.instructions` command MUST instruct the agent to populate `.ai/instructions.md` with sections: Goals, Limitations, Guidance, Steps, Validation, and MCP Tools Usage Guide (referencing `copilot_generate_instructions` logic).
- **FR-004**: The `/speckit.instructions` command MUST instruct the agent to create compatibility symlinks in `.clinerules`, `.github` (as `copilot-instructions.md`), `.lingma`, `.trae`, and `.qoder`.
- **FR-005**: System MUST provide a `/speckit.skills` command template located at `templates/commands/skills.md`.
- **FR-006**: The `/speckit.skills` command MUST instruct the agent to create a new skill directory under `.github/skills/` (or user preference if specified).
- **FR-007**: The `/speckit.skills` command MUST instruct the agent to create a `SKILL.md` file following the schema defined in `skills.md` (YAML frontmatter with name/description, Body with instructions).
- **FR-008**: Identify existing project type and context when running instructions command to tailor the output if possible.
- **FR-009**: **Instruction Update Strategy**: If `.ai/instructions.md` exists, the command MUST rename it to `.ai/instructions.md.bak` (or timestamped) and generate a new file. This ensures the instructions always reflect the current `constitution.md` and `templates` fully.
- **FR-010**: **Skill Context Enrichment**: When running `/speckit.skills` for a specific skill, the command SHOULD search `.specify/memory/feature-index.md` and active specs for relevant context (e.g., if skill is "testing", look for "testing" sections in specs) and include this as context/guidance in the generated `SKILL.md`.
- **FR-011**: **Skill Update Preservation**: If the target skill directory and `SKILL.md` already exist, the command MUST NOT overwrite the file. Instead, it MUST append a new section titled `### Spec Context Updates [YYYY-MM-DD]` containing the newly identified context/requirements, preserving all user customizations.

### Key Entities

- **Instructions Command**: Template file `templates/commands/instructions.md`.
- **Skills Command**: Template file `templates/commands/skills.md`.
- **Reference Logic**: `scripts/bash/generate-copilot.sh` (for instructions) and `skills.md` (for skills).
