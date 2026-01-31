# Feature Specification: Standardize Instructions Command

**Feature Branch**: `002-standardize-instructions-cmd`  
**Created**: 2026-01-31  
**Status**: Draft  
**Input**: User description: "--number 1

将instructions命令改成一个标准的speckit命令（可以参考其他命令的实现）。需要包含templates/commands/instructions.md命令自身定义，scripts/bash/generate-instructions.sh用来处理复杂逻辑的shell脚本，templates/instructions-template.md包含大部分文本内容的模版文件。"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Standardized Instructions (Priority: P1)

As a developer, I want the `instructions` command to generate project instructions using a customizable template, so that I can maintain consistent context for AI tools.

**Why this priority**: Core functionality required to ensure the command behaves predictably and is maintainable.

**Independent Test**: Can be tested by running the updated command and verifying the output file structure against the template.

**Acceptance Scenarios**:

1. **Given** a valid `templates/instructions-template.md` exists, **When** I run the `instructions` command, **Then** the output instructions file is generated using the template content.
2. **Given** the script is executed, **When** it runs, **Then** it correctly substitutes dynamic variables into the template.
3. **Given** the command definition, **When** inspected, **Then** it points to the correct script and has standard metadata.

---

### Edge Cases

- What happens when `templates/instructions-template.md` is missing? (Script should error or use built-in default)
- What happens when the output file is locked or unwritable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The command definition MUST be located at `templates/commands/instructions.md` and follow the standard `speckit` command schema.
- **FR-002**: The implementation logic MUST be encapsulated in `scripts/bash/generate-instructions.sh`.
- **FR-003**: The script MUST use `templates/instructions-template.md` as the source of truth for the instructions text content.
- **FR-004**: The system MUST support variable substitution within the template, limited to basic project metadata (e.g., Project Name, Root Path, Date). It SHOULD NOT attempt complex auto-detection of tech stacks.
- **FR-005**: If `templates/instructions-template.md` is empty or missing, the command MUST fail with an error message indicating the missing file. It MUST NOT use an embedded default.
- **FR-006**: If the target instructions file already exists, the system MUST Perform a **content fusion**: use the generated template as the structural framework and rewrite the existing content to fit into this new structure, ensuring no custom context is lost (as opposed to simple backup-and-replace).
- **FR-007**: The system MUST create relative symlinks for AI tool integration (e.g., linking `.clinerules/project_rules.md` to `../.ai/instructions.md`) to ensure portability.

### Key Entities

- **Command Definition**: `templates/commands/instructions.md`
- **Logic Script**: `scripts/bash/generate-instructions.sh`
- **Content Template**: `templates/instructions-template.md`

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]

## Clarifications

### Session 2026-01-31

- Q: What level of dynamic content injection is expected for FR-004? → A: **Basic Metadata**: Script substitutes only standard ENV vars available to it (Project Name, Root Path, Date) and leaves content placeholders.
- Q: How should the command handle an existing `.ai/instructions.md` file? → A: **Smart Fusion**: Use the new template as a structural framework and incorporate/rewrite the existing content into it, ensuring custom context is preserved (not just simple replacement).
- Q: FR-005 states "fail or provide default" if the template file is missing. Which behavior do you prefer? → A: **Hard Fail**: Exit with error "Template not found". Forces user to fix environment.
- Q: The current script creates symlinks for `.clinerules`. Should the standardized command preserve this behavior? → A: **Yes, Relative Symlinks**: Maintain relative symlinks (portable across machines).

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
