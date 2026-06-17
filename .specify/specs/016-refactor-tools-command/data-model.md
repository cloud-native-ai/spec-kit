# Data Model: Refactor Tools Command — Definition-First Model

**Branch**: 016-refactor-tools-command | **Date**: 2026-06-17

## Entities

### ToolDefinitionRecord

- **Description**: The core artifact of the definition-first model. A structured markdown file at `.specify/memory/tools/<tool-name>.md` containing a tool's complete definition including behavioral rules. This replaces the discovery-centric ToolRecord from spec 004 by adding behavioral rules and strengthening the role of user-authored fields over LLM-inferred defaults.
- **Grounding**: FR-001, FR-002, FR-003, FR-004, FR-006, FR-010; User Story 1
- **Fields**:
  - name: string (required) — user-provided tool name; MUST NOT be auto-populated from LLM knowledge (FR-002)
  - tool_type: string (required) — one of `project-script`, `system-binary`, `shell-function` (FR-007)
  - source_identifier: string (required) — script path, binary path, or function name (FR-002)
  - tool_id: string (required) — deterministic identifier derived from canonical file path `.specify/memory/tools/<tool-name>.md` (FR-004)
  - description: string (required) — user-provided purpose statement; MUST NOT be auto-populated from LLM knowledge (FR-002)
  - behavioral_rules: array<BehavioralRule> (optional but recommended) — user-authored constraints (FR-003)
  - parameters: array<ToolParameter> (optional) — input parameters and their constraints
  - returns: array<ToolReturnField> (optional) — expected output fields
  - aliases: array<string> (optional) — alternative names resolving to this record (FR-011)
  - status: string (required) — one of `Draft`, `Verified`, `Deprecated`; transitions to `Verified` only after validation (FR-006)
  - last_updated: date — YYYY-MM-DD format
  - discovery_origin: string (optional) — one of `manual-entry`, `discovery-assisted`, `imported`; tracks whether the record was created from scratch or bootstrapped via discovery (FR-013)
- **State Transitions**:
  - `Draft` → `Verified`: when all mandatory fields are present and non-empty (FR-006)
  - `Verified` → `Draft`: when a mandatory field is cleared during modification
  - `Verified` → `Deprecated`: when the tool is no longer in use
  - `Draft` → `Deprecated`: when a draft tool is abandoned

### BehavioralRule

- **Description**: A single user-authored constraint within a tool definition that prescribes or prohibits a specific invocation pattern. Each rule uses an RFC 2119 keyword prefix to indicate obligation strength.
- **Grounding**: FR-003; Clarification session 2026-06-17 Q3
- **Fields**:
  - keyword: string (required) — one of `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`
  - constraint_text: string (required) — free-form description of the constraint
- **Serialization**: In the markdown tool record, each rule is a bullet: `- {keyword} {constraint_text}`

### ToolParameter

- **Description**: A single input parameter for a tool.
- **Grounding**: FR-002, FR-008
- **Fields**:
  - name: string (required)
  - type: string (required) — data type (e.g., string, integer, boolean, path)
  - required: boolean (required)
  - description: string (required)
  - default: string | null (optional)

### ToolReturnField

- **Description**: A single field in the tool's expected output.
- **Grounding**: FR-008
- **Fields**:
  - name: string (required)
  - type: string (required)
  - description: string (required)

### ToolInvocationSession

- **Description**: A transient record representing one attempt to invoke a tool through `/speckit.tools`. Captures the full lifecycle from parameter resolution through preview, confirmation, execution, and result.
- **Grounding**: FR-008; User Story 3
- **Fields**:
  - tool_name: string — name of the tool being invoked
  - tool_id: string — resolved tool_id from the definition record
  - resolved_command: string — fully resolved command string shown in preview
  - resolved_parameters: object — key-value map of resolved parameter values
  - applicable_behavioral_rules: array<BehavioralRule> — rules active for this invocation
  - expected_output_shape: string — description of expected output format
  - user_confirmed: boolean — whether the user approved execution (FR-008)
  - result_status: string — one of `success`, `failed`, `cancelled`
  - result_summary: string — brief description of the outcome

### DiscoveryDraft

- **Description**: A transient, unverified tool definition proposed by the discovery subsystem when no existing record is found. Requires full user review and confirmation before being persisted as a ToolDefinitionRecord.
- **Grounding**: FR-013, FR-014; Clarification session 2026-06-17 Q2
- **Fields**:
  - proposed_name: string — discovered tool name
  - proposed_type: string — inferred tool type
  - proposed_source: string — discovered source path/name
  - proposed_description: string — auto-generated description (labeled as draft)
  - confidence: string — one of `high`, `medium`, `low` based on discovery match quality
  - draft_label: string — always "Draft — pending user confirmation" (FR-014)

## Relationships

- A **ToolDefinitionRecord** contains zero or more **BehavioralRule** entries (composition).
- A **ToolDefinitionRecord** contains zero or more **ToolParameter** entries (composition).
- A **ToolDefinitionRecord** contains zero or more **ToolReturnField** entries (composition).
- A **ToolInvocationSession** references exactly one **ToolDefinitionRecord** via `tool_id`.
- A **DiscoveryDraft** may be promoted to a **ToolDefinitionRecord** after user confirmation; the draft is discarded after promotion or rejection.

## Validation Rules

- A ToolDefinitionRecord MUST have non-empty `name`, `tool_type`, `source_identifier`, and `description` before transitioning to `Verified` status (FR-006).
- `tool_type` MUST be one of `project-script`, `system-binary`, `shell-function` (FR-007).
- When `status` is `Verified`, the record MUST have at least one of `parameters` or `returns` populated.
- Each BehavioralRule `keyword` MUST be one of `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`.
- Tool aliases MUST be unique across all records — no two records may share the same alias (FR-011).
- When `user_confirmed` is `false` in a ToolInvocationSession, `result_status` MUST be `cancelled` (FR-008).
- A DiscoveryDraft MUST NOT be persisted to `.specify/memory/tools/` without user confirmation (FR-014).
- Mandatory fields in a ToolDefinitionRecord MUST NOT be auto-populated from LLM built-in knowledge (FR-002).

## Changes from Spec 004 Data Model

| Aspect | Spec 004 (Discovery-First) | Spec 016 (Definition-First) |
|--------|---------------------------|----------------------------|
| Primary entity name | ToolRecord | ToolDefinitionRecord |
| Behavioral Rules | Not present | Required section with RFC 2119 keywords |
| Discovery origin tracking | Not present | `discovery_origin` field |
| `tool_type` values | `mcp`, `system`, `shell`, `project` | `project-script`, `system-binary`, `shell-function` (MCP removed) |
| DiscoveryDraft entity | Not present | New — transient draft for discovery-assisted creation |
| LLM knowledge constraint | Not specified | FR-002: mandatory fields MUST NOT be auto-populated from LLM |
