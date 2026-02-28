# Data Model: Speckit Agents Command

## Entity: AgentDefinition

- **Purpose**: Represents a custom agent artifact managed by `/speckit.agents`.
- **Identity**: `agent_name` (kebab-case, unique within `.github/agents/`).
- **Core Fields**:
  - `agent_name` (required)
  - `display_name` (required)
  - `description` (required)
  - `role_scope` (required, single-responsibility)
  - `workflow_steps` (required, ordered list)
  - `output_format` (required)
  - `invocation_mode` (required: direct/subagent/both)
- **Lifecycle States**:
  - `Draft` → `Validated` → `Saved` (initial creation)
  - `Saved` → `Updated` (same-name overwrite path with full replacement)
  - **Update behavior**: Complete file replacement, no partial updates or merges

## Entity: AgentFrontmatter

- **Purpose**: YAML metadata header at top of `.agent.md` file.
- **Core Fields**:
  - `description` (required)
  - `tools` (required, least-privilege by default)
  - `model_hints` (optional)
  - `invocation` (required)
- **Validation Rules**:
  - Must be valid YAML.
  - Tool list must align with workflow purpose.
  - Must not include unsupported provider references.

## Entity: ToolPermissionProfile

- **Purpose**: Defines allowed tools for an agent.
- **Identity**: Derived from `agent_name` + resolved workflow.
- **Core Fields**:
  - `requested_tools` (optional)
  - `effective_tools` (required)
  - `resolution_mode` (explicit/least-privilege)
- **Rules**:
  - If no tools requested: derive least-privilege set.
  - If contradictory constraints: prioritize latest explicit input; unresolved conflicts block save.

## Entity: InferenceDecision

- **Purpose**: Records intent inference outcome when user gives no arguments.
- **Core Fields**:
  - `confidence_level` (high/medium/low)
  - `inferred_intent` (optional)
  - `needs_user_prompt` (boolean)
- **Rules**:
  - `low` confidence must trigger one-sentence intent request and stop generation.

## Relationships

- `AgentDefinition` **contains** one `AgentFrontmatter`.
- `AgentDefinition` **uses** one `ToolPermissionProfile`.
- `AgentDefinition` **may reference** one `InferenceDecision` for no-argument flows.

## Invariants

- Same-name agent update overwrites existing target file.
- Missing `.github/agents/` directory is auto-created before save.
- Only approved providers are allowed in generated guidance.
- Every saved agent must pass YAML and contradiction validation.