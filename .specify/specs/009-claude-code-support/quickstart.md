# Quickstart: Validate Claude Code Support

## Prerequisites

- Work from the repository root.
- Implementation tasks for Feature 021 have been completed.
- To validate the normal tool-check path, Claude Code is available in the local environment.
- To validate the failure path, run in an environment where the Claude Code command is not available.

## Scenario 1: New project initialization with Claude Code

1. Initialize a new project with Claude Code selected.
2. Inspect the generated project for Claude Code compatibility assets:
   - Claude Code custom command directory
   - Claude Code guidance or compatibility file
   - `.claudeignore`
   - `.specify/` workflow assets
3. Confirm standard Spec Kit workflow commands are discoverable from the Claude Code command surface.

**Expected Result**:

- The project is initialized successfully.
- Claude Code-specific assets are present.
- Required `.specify/` workflow files remain available to Claude Code.
- Command coverage matches the canonical `templates/commands/*.md` inventory or documents explicit exclusions.

## Scenario 2: Existing workspace refresh

1. Start with a Spec Kit workspace that already contains another assistant integration such as Copilot, Qwen Code, opencode, or Qoder.
2. Add or refresh Claude Code support.
3. Compare assistant-specific directories before and after refresh.

**Expected Result**:

- Claude Code assets are created or updated.
- Existing assistant integrations remain intact.
- Canonical instruction links still point to `.specify/instructions.md` where appropriate.

## Scenario 3: Customized Claude Code files

1. Create a workspace with existing Claude Code files containing user-authored content.
2. Refresh Claude Code support.
3. Inspect changed files and refresh messages.

**Expected Result**:

- User custom content is preserved when safe.
- Any conflict is reported clearly.
- No customized file is silently overwritten.

## Scenario 4: Missing Claude Code validation

1. Ensure the Claude Code command is not available in the environment.
2. Attempt initialization with Claude Code selected and without the ignore flag.

**Expected Result**:

- Setup reports that Claude Code could not be validated.
- The message includes install/setup guidance.
- The message explains how to continue with the tool check intentionally skipped.

## Scenario 5: Skip validation intentionally

1. Run initialization with Claude Code selected and tool validation skipped.
2. Inspect generated assets.

**Expected Result**:

- Setup proceeds without local Claude Code validation.
- Generated assets are identical in required structure to the normal path.
- The user receives clear guidance that local Claude Code availability was not verified.

## Scenario 6: `.claudeignore` safety audit

1. Inspect `.claudeignore` generated in a Claude Code-ready project.
2. Confirm it excludes local environment, dependency, cache, build, temporary, and secret-like content.
3. Confirm it does not exclude required `.specify/` workflow artifacts or Claude Code command assets.

**Expected Result**:

- Privacy-sensitive and high-noise paths are excluded.
- Requirements, plan, tasks, instructions, and generated command assets remain accessible for the workflow.

## Scenario 7: Support-surface and release audit

1. Audit supported assistant references across governance, README, docs, CLI help, templates, generated assets, and release/package resources.
2. Compare each surface to the assistant support matrix.

**Expected Result**:

- Claude Code appears consistently wherever supported assistants are listed.
- No support surface contradicts another surface.
- Governance includes Claude Code as an officially approved assistant before release readiness is claimed.

## Scenario 8: Command coverage audit

1. Count canonical command templates under `templates/commands/`.
2. Generate Claude Code command assets.
3. Compare generated command names against canonical template names.

**Expected Result**:

- 100% of standard Spec Kit workflow commands are generated for Claude Code or have documented exclusions.
- Generated command descriptions preserve canonical workflow intent.
