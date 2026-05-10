# Data Model: Create Skills Skill

**Branch**: `008-create-skills-skill`  
**Date**: 2026-05-10

## Entities

### Skill Creation Capability

Represents the reusable knowledge package that guides agents through creating new Spec Kit Skills.

**Fields**:

- `name`: Always `create-skills`.
- `canonical_source_path`: Repository source path for the Skill, expected to be `skills/create-skills/SKILL.md`.
- `workspace_compatibility_path`: Current-workspace Skill path when mirrored or installed, typically `.specify/skills/create-skills/SKILL.md`.
- `description`: Trigger description that clearly identifies new Skill creation and workflow distillation scenarios.
- `workflow_sections`: Ordered guidance sections covering input parsing, conversation distillation, Skill structure, resources, registry, validation, and reporting.
- `resource_directories`: Optional relative directories such as `./references/`, `./scripts/`, and `./assets/`.

**Validation rules**:

- `name` must match the directory name.
- `description` must describe both capability and trigger scenarios.
- `SKILL.md` must contain YAML frontmatter followed by actionable Markdown instructions.
- Resource paths must be relative to the Skill root.
- Creation guidance must not include `/speckit.skills` command routing logic except as contextual relationship notes.

**Relationships**:

- Used by `Skills Command` when a target Skill does not exist.
- Complements `improve-skills`, which handles existing Skill refinement.

### Skills Command

Represents the `/speckit.skills` command prompt that remains the explicit orchestration entrypoint.

**Fields**:

- `template_path`: `templates/commands/skills.md`.
- `input_arguments`: Raw user command arguments.
- `target_skill_name`: Parsed or inferred Skill name.
- `target_exists`: Boolean determination of whether the target Skill already has a `SKILL.md`.
- `delegation_target`: Either `create-skills` or `improve-skills`.
- `handoffs`: Follow-up actions such as updating project instructions or registries.

**Validation rules**:

- If `target_exists` is false, `delegation_target` must be `create-skills`.
- If `target_exists` is true, `delegation_target` must be `improve-skills`.
- The command template must not duplicate detailed creation methodology that belongs in `create-skills`.
- The command must preserve enough routing context for predictable `/speckit.skills` behavior.

**Relationships**:

- Invokes `create-skills` for missing target Skills.
- Invokes `improve-skills` for existing target Skills.
- May request `/speckit.instructions` after changes so Skills remain discoverable.

### Target Skill

Represents the Skill being created or improved through the command workflow.

**Fields**:

- `name`: Lowercase Skill identifier using alphanumeric characters and hyphens.
- `description`: Capability and trigger description.
- `skill_root`: Chosen Skill directory.
- `skill_file`: `SKILL.md` under `skill_root`.
- `skill_id`: Deterministic identifier when managed in the current workspace.
- `creation_source`: Either explicit user input or conversation-derived workflow.

**Validation rules**:

- `name` must be valid and must match the target directory.
- Missing critical metadata should trigger one targeted clarification question.
- Existing target Skills must not be overwritten by creation flow.
- Created Skills should use progressive disclosure and avoid unrelated documentation files.

### Skill Resource Registry Entry

Represents discoverability metadata recorded for reusable Skills.

**Fields**:

- `skill_name`: Human-readable Skill name.
- `skill_id`: Deterministic Skill identifier when available.
- `description`: Trigger description.
- `canonical_path`: Workspace-relative `SKILL.md` path.

**Validation rules**:

- Registry rows must be deduplicated by Skill ID or canonical path.
- Registry rows must use the existing table schema in `.specify/instructions.md`.
- Registry updates should not disturb unrelated Agent or Tool registry entries.

## State Transitions

### Target Skill Lifecycle

1. `requested`: User requests a Skill creation or refresh action.
2. `classified`: `/speckit.skills` determines whether the target exists.
3. `delegated-to-create`: Missing targets are routed to `create-skills`.
4. `drafted`: `create-skills` produces or updates initial Skill content.
5. `validated`: Frontmatter, structure, resource links, and registry expectations are checked.
6. `reported`: The agent reports paths, IDs, examples, and follow-up actions.

### Command Template Refactor Lifecycle

1. `inline-creation-guidance`: Current command contains detailed creation methodology.
2. `extracted-guidance`: Creation methodology lives in `create-skills`.
3. `orchestration-only`: Command retains routing, validation expectations, and handoffs.
4. `verified`: Review confirms no creation logic drift or duplication.
