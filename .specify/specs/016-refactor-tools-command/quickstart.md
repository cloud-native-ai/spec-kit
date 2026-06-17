# Quickstart: Refactor Tools Command — Definition-First Model

**Branch**: 016-refactor-tools-command | **Date**: 2026-06-17

## Goal

Validate the definition-first workflow of `/speckit.tools`: tool definition creation, modification, discovery-assisted bootstrapping, invocation preview with behavioral rule enforcement, and confirmation gate.

## Scenarios

### Scenario 1: Define a New Project Script Tool (User Story 1 — P1)

1. User invokes `/speckit.tools` and states: "I want to define a tool called `build-docs` that runs `scripts/bash/build-docs.sh`."
2. System prompts for mandatory fields:
   - **Tool Name**: `build-docs` (provided by user)
   - **Tool Type**: `project-script` (provided by user)
   - **Source Identifier**: `scripts/bash/build-docs.sh` (provided by user)
   - **Description**: "Builds project documentation from markdown sources" (provided by user)
3. System prompts for optional Behavioral Rules. User adds:
   - `MUST run from the repository root directory`
   - `MUST NOT modify source files`
4. System creates `.specify/memory/tools/build-docs.md` with status `Draft`.
5. System validates all mandatory fields are present → transitions status to `Verified`.
6. System registers the tool in the Resource Registry of `.specify/instructions.md`.

**Expected Result**: A complete tool definition record at `.specify/memory/tools/build-docs.md` with all user-provided fields and two behavioral rules. No fields auto-populated from LLM knowledge.

### Scenario 2: Modify an Existing Tool Definition (User Story 2 — P2)

1. User invokes `/speckit.tools` referencing the existing `build-docs` tool.
2. User requests: "Add a new behavioral rule: SHOULD generate a table of contents."
3. System loads the existing record, appends the new behavioral rule.
4. System preserves all existing fields unchanged.
5. System updates `last_updated` date and writes the modified record.

**Expected Result**: The `build-docs.md` record now has three behavioral rules. All other fields (name, type, source, description, parameters) remain identical to their pre-modification values.

### Scenario 3: Discovery-Assisted Definition (User Story 1 + FR-013)

1. User invokes `/speckit.tools` and states: "I want to define a tool called `jq`."
2. System checks `.specify/memory/tools/jq.md` — no record exists.
3. System offers: "No existing definition found. Would you like to scan the system to bootstrap a draft?"
4. User accepts. Discovery runs and proposes a draft:
   - **Proposed Name**: `jq`
   - **Proposed Type**: `system-binary`
   - **Proposed Source**: `/usr/bin/jq`
   - **Draft Label**: "Draft — pending user confirmation"
5. System presents the draft for review. User confirms the name, type, and source but replaces the auto-generated description with: "JSON processor for extracting fields from API responses."
6. User adds behavioral rules:
   - `MUST use --raw-output flag when extracting string values`
   - `MUST NOT use --slurp on unbounded input streams`
7. System persists the confirmed record with `discovery_origin: discovery-assisted`.

**Expected Result**: A verified tool definition at `.specify/memory/tools/jq.md` with user-confirmed fields and user-authored behavioral rules. The description reflects the user's project-specific intent, not a generic LLM-derived description of `jq`.

### Scenario 4: Invocation Preview and Confirmation Gate (User Story 3 — P3)

1. User requests: "Run `build-docs` with `--format html`."
2. System loads the `build-docs` definition record.
3. System displays the invocation preview:
   - **Command**: `scripts/bash/build-docs.sh --format html`
   - **Parameters**: `format = html`
   - **Behavioral Rules**:
     - MUST run from the repository root directory
     - MUST NOT modify source files
     - SHOULD generate a table of contents
   - **Expected Output**: Plain log lines
4. System prompts: "Proceed with execution? (yes/no)"
5. User replies "yes" → system executes the command.
6. System records the invocation session with `result_status: success`.

**Expected Result**: The tool is invoked exactly as previewed. No additional parameters or flags are added by the AI agent. Behavioral rules are shown to the user before execution.

### Scenario 5: View All Registered Tools (User Story 4 — P4)

1. User invokes `/speckit.tools` without specifying a tool name.
2. System lists all registered tool definitions from `.specify/memory/tools/`:
   - `build-docs` | `project-script` | Builds project documentation from markdown sources
   - `jq` | `system-binary` | JSON processor for extracting fields from API responses
3. User selects `jq` to view its full definition.

**Expected Result**: A summary table of all registered tools, followed by the complete definition of the selected tool including behavioral rules.

## Expected Results Summary

- Tool definitions are created from user-provided fields, not LLM-inferred defaults.
- Discovery proposes drafts labeled "Draft — pending user confirmation"; no draft is persisted without user review.
- Behavioral rules are persisted as RFC 2119-prefixed bullets and displayed in invocation previews.
- The confirmation gate blocks execution until the user explicitly approves.
- Field-level modifications preserve unmodified fields with zero data loss.
- All created/modified tools appear in the Resource Registry of `.specify/instructions.md`.
