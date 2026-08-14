# Quickstart: Deterministic Tool and Skill IDs

## Purpose

Validate that `/speckit.tools` and `/speckit.skills` now produce stable canonical identifiers and that later references can resolve the same artifact deterministically.

## Prerequisites

- Work on branch `005-tool-skill-ids`
- Existing workspace contains `templates/commands/tools.md`, `templates/commands/skills.md`, and their related creation scripts
- At least one sample tool record and one sample skill can be created or refreshed during validation

## Validation Scenarios

### Scenario 1: Tool flow returns a canonical ID

1. Invoke `/speckit.tools` for a resolvable tool candidate.
2. Complete the discovery or record creation flow.
3. Confirm the command output includes:
   - the resolved artifact type (`tool`)
   - a canonical resource ID
   - the matching workspace-relative path
4. Verify the generated or updated tool record persists the same ID.

**Expected Result**: The command returns a single canonical `tool_id`, and the persisted record stores the identical value.

### Scenario 2: Skill flow returns a canonical ID

1. Invoke `/speckit.skills` to create or refresh a skill.
2. Complete the creation or refresh flow.
3. Confirm the command output includes:
   - the resolved artifact type (`skill`)
   - a canonical resource ID
   - the matching workspace-relative path for the skill root or `SKILL.md`
4. Verify the generated or updated skill artifact persists the same ID.

**Expected Result**: The command returns a single canonical `skill_id`, and the persisted artifact stores the identical value.

### Scenario 3: ID-based resolution takes precedence over fuzzy matching

1. Copy a previously returned `tool_id` or `skill_id`.
2. Reuse it in a follow-up document or command context with a vague natural-language hint.
3. Trigger resolution.

**Expected Result**: The system resolves the artifact by ID first and does not ask the user to re-run fuzzy discovery.

### Scenario 4: Historical artifact receives backfilled ID

1. Select an older tool record or skill artifact that does not yet contain a resource ID.
2. Trigger a refresh or update flow.
3. Inspect the resulting persisted artifact.

**Expected Result**: The artifact is updated with a canonical ID without requiring a bulk migration of unrelated artifacts.

### Scenario 5: Conflict between ID and text is blocked

1. Provide a valid `resource_id` for one artifact.
2. Provide natural-language text that clearly refers to a different artifact.
3. Trigger resolution.

**Expected Result**: The system stops with an explicit conflict message and does not silently choose one target.

### Scenario 6: Stale ID is rejected with recovery guidance

1. Generate a valid ID for a persisted artifact.
2. Rename, move, or delete the underlying artifact.
3. Reuse the old ID.

**Expected Result**: The system reports the ID as stale or not found and instructs the user to refresh or rediscover the artifact.

## Regression Expectations

- Existing natural-language-only `/speckit.tools` and `/speckit.skills` flows remain available
- No valid artifact pair shares the same canonical resource ID within the workspace
- Error messages for invalid IDs remain user-readable and actionable
