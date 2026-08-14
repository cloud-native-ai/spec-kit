# Quickstart: Validate AI Tools Support

## Prerequisites

- Work from the repository root.
- Implementation tasks for Feature 022 have been completed.
- Use disposable fixture workspaces for initialization and refresh checks.
- To validate missing-tool paths, run with at least one CLI assistant command unavailable or simulate command absence in tests.

## Scenario 1: New project initialization for every official assistant

1. For each official assistant key (`copilot`, `claude`, `qwen`, `opencode`, `qoder`), initialize a new project with that assistant selected.
2. Inspect the generated project for `.specify` core assets.
3. Inspect the assistant-specific command/guidance directory for generated Spec Kit workflow entry points.
4. Read the initialization summary.

**Expected Result**:

- Each assistant can initialize a usable Spec Kit workspace.
- Every assistant has discoverable core workflow commands or documented exclusions.
- `.specify` assets are created once as the canonical workspace core.
- The summary lists created core and assistant-specific assets.

## Scenario 2: Existing project adds a second assistant

1. Initialize a workspace with one assistant.
2. Modify a core `.specify` file to represent user-maintained content.
3. Add a second official assistant to the same workspace.
4. Compare the modified core file before and after the second initialization.

**Expected Result**:

- The modified core file is unchanged.
- The second assistant’s assets are created.
- The first assistant’s assets remain present and usable.
- The summary marks core files as reused or preserved, not overwritten.

## Scenario 3: Multiple assistants coexist

1. Configure at least three official assistants in one workspace.
2. Verify each assistant root and command surface exists.
3. Refresh one assistant.
4. Compare all other assistant roots before and after refresh.

**Expected Result**:

- All configured assistants remain available.
- Refreshing one assistant does not remove or rewrite another assistant root.
- The summary identifies configured assistants and any missing coverage.

## Scenario 4: Incomplete `.specify` core is repaired safely

1. Create a workspace with a partial `.specify` directory and missing required core files.
2. Add an official assistant.
3. Inspect which core files were created and which existing files were reused.

**Expected Result**:

- Missing required core files are created from templates.
- Existing initialized core files are preserved.
- The summary clearly distinguishes created assets from reused/preserved assets.

## Scenario 5: Customized tool-specific assets are protected

1. Create or modify an assistant-specific command/guidance file with user content.
2. Refresh that assistant.
3. Inspect the file and the result summary.

**Expected Result**:

- User customization is preserved or a conflict is reported.
- No customized assistant-specific file is silently overwritten.
- The summary identifies the asset and required user action when conflict exists.

## Scenario 6: Repeat-run idempotence

1. Initialize a workspace with one assistant.
2. Run initialization or refresh again with the same assistant.
3. Compare core `.specify` content and assistant-specific content before and after.

**Expected Result**:

- No duplicate core content is created.
- Existing user-maintained content remains unchanged.
- The summary reports reused/skipped/preserved assets rather than repeated creation.

## Scenario 7: Project configuration vs local tool availability

1. Attempt initialization with a CLI assistant whose local command is unavailable.
2. Repeat with validation intentionally skipped.
3. Compare generated assets and messages.

**Expected Result**:

- Without skip validation, the user receives install guidance and a clear blocked or warning state.
- With skip validation, project assets are generated and the summary states that local tool availability was not verified.
- The summary distinguishes “project configured” from “local tool available.”

## Scenario 8: Support-surface release audit

1. Audit official assistant references in CLI help, README, docs, templates, scripts, package resources, generated assets, and tests.
2. Compare each surface to the assistant support matrix.
3. Audit command coverage for every official assistant against canonical command templates.

**Expected Result**:

- All release-blocking surfaces list the same official assistants.
- 100% of canonical workflow commands are generated for each assistant or have explicit exclusions.
- Audit failures name the mismatched surface and block release readiness.

## Scenario 9: SDD script path consistency

1. Run current feature workflow helpers from a branch with a `.specify/specs/<requirements-key>/requirements.md` artifact.
2. Confirm planning and prerequisite scripts resolve the current requirements directory and file.
3. Repeat after adding another assistant to ensure generated commands invoke the same script paths.

**Expected Result**:

- Scripts resolve `.specify/specs/<requirements-key>/requirements.md` consistently.
- No helper attempts to use legacy `specs/<branch>/spec.md` paths.
- Assistant command assets invoke the same working script flow.
