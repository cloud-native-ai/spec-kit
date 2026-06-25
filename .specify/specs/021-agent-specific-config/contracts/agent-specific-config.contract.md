# Contract: Agent-Specific Configuration

**Spec**: [requirements.md](../requirements.md)  
**Date**: 2026-06-25

## Overview

This contract defines the structural and behavioral rules for the Agent-Specific Configuration feature. Since this feature modifies markdown templates (not code APIs), the contract specifies file structure, section presence, naming conventions, and content requirements that can be validated by contract tests.

## C-001: Command Template Section Presence

Each targeted command template MUST contain a section with the exact heading `## Agent-Specific Configuration`.

**Targets**:
- `templates/commands/agents.md`
- `templates/commands/skills.md`
- `templates/commands/tools.md`

**Validation**:
- MUST contain the heading `## Agent-Specific Configuration`
- MUST contain subsection `### Step 1: Identify Executing Agent`
- MUST contain subsection `### Step 2: Load Agent-Specific Guidance`
- MUST contain subsection `### Step 3: Capture Execution Feedback`
- The section MUST appear after the main workflow sections and before `## Handoffs`

**Grounding**: FR-001

## C-002: Skill SKILL.md Section Presence

Each targeted skill MUST contain a section with the exact heading `## Agent-Specific Configuration` in its SKILL.md.

**Targets**:
- `skills/browser-utils/SKILL.md`
- `skills/create-agent/SKILL.md`
- `skills/improve-agent/SKILL.md`
- `skills/improve-skills/SKILL.md`

**Validation**:
- MUST contain the heading `## Agent-Specific Configuration`
- MUST contain subsections for the three-step workflow (identify, load, capture)
- Step 2 MUST reference `${SKILL_HOME}/references/<agent-slug>-guide.md` path pattern
- The section MUST NOT modify or replace existing workflow sections

**Grounding**: FR-002, FR-010

## C-003: Skill Reference Document Naming

Each targeted skill MUST have per-agent reference documents following the naming convention `<agent-slug>-guide.md`.

**Valid agent slugs** (derived from `AGENT_CONFIG` keys with slug normalization):
- `claude-code` (mapped from config key `claude`)
- `copilot`
- `qoder`
- `opencode`
- `qwen`
- `codex`
- `hermes`
- `iflow`

**Validation**:
- Files MUST be located at `${SKILL_HOME}/references/<agent-slug>-guide.md`
- File names MUST use exactly the slugs listed above
- At launch, at minimum `claude-code-guide.md` and `copilot-guide.md` MUST exist for each targeted skill

**Grounding**: FR-005, SC-002

## C-004: Reference Document Structure

Each agent reference document MUST contain the following sections:

```
# <Skill Name> — <Agent Name> Guide

## Tool Mapping
## Best Practices
## Known Pitfalls
## Capability Notes
```

**Validation**:
- MUST contain all four section headings
- `## Tool Mapping` MUST contain at least one mapping entry
- `## Known Pitfalls` MUST contain at least one pitfall entry (or explicit "None identified")
- Content MUST be specific to the agent-skill combination (not generic boilerplate)

**Grounding**: FR-006

## C-005: Feedback Document Structure

Each execution feedback document MUST conform to the following structure:

**Path pattern**: `.specify/memory/feedback/<source>-<agent-slug>-<timestamp>.md`

Where:
- `<source>` is the command or skill name (e.g., `browser-utils`, `agents`)
- `<agent-slug>` is a valid agent slug from C-003
- `<timestamp>` is ISO-8601 date format (e.g., `2026-06-25T14-30-00`)

**Required fields** (as markdown content):
- `**Source**:` — command or skill name
- `**Agent**:` — agent slug
- `**Timestamp**:` — ISO-8601 timestamp
- `**Outcome**:` — one of `success-with-workaround`, `partial-failure`, `full-failure`
- `## Obstacle` — section describing the issue
- `## Suggested Improvement` — section with proposed fix

**Optional fields**:
- `## Workaround Applied` — section describing the workaround (may be absent if no workaround was possible)

**Grounding**: FR-008, FR-009

## C-006: Graceful Fallback

When the executing agent cannot be identified or has no corresponding reference document, the command or skill MUST:

1. Continue executing the standard workflow without errors
2. NOT produce error messages or warnings that would confuse the user
3. Optionally log a note (non-blocking) suggesting reference creation for the unrecognized agent

**Validation**: Run each targeted command/skill in a context where no agent identification signals are present; verify clean completion.

**Grounding**: FR-007, SC-004

## C-007: Additive Section Constraint

The Agent-Specific Configuration section MUST be additive:

- MUST NOT modify, replace, or conditionally skip any existing workflow step
- MUST NOT introduce new mandatory dependencies for the core workflow
- MUST NOT change the command/skill output format when no agent-specific reference exists
- Removing the entire Agent-Specific Configuration section MUST leave the command/skill fully functional

**Validation**: Diff the command/skill behavior with and without the Agent-Specific Configuration section; core workflow output must be identical.

**Grounding**: FR-010

## C-008: Feedback Directory Existence

The `.specify/memory/feedback/` directory MUST exist after implementation.

**Validation**:
- Directory MUST be present at `.specify/memory/feedback/`
- Directory MAY be empty (feedback documents are generated at runtime, not at build time)
- A `.gitkeep` file SHOULD be present to ensure the empty directory is tracked by git

**Grounding**: FR-009

## Test Matrix

| Contract | Test Type | Automated | Priority |
|----------|-----------|-----------|----------|
| C-001 | Structure (heading grep) | Yes | P1 |
| C-002 | Structure (heading grep) | Yes | P1 |
| C-003 | File existence check | Yes | P1 |
| C-004 | Structure (heading grep) | Yes | P1 |
| C-005 | Structure (field grep) | Yes | P2 |
| C-006 | Behavioral (manual) | No | P1 |
| C-007 | Behavioral (diff) | No | P1 |
| C-008 | File existence check | Yes | P2 |
