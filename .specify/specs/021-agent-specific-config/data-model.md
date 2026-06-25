# Data Model: Agent-Specific Configuration

**Spec**: [requirements.md](./requirements.md)  
**Plan**: [plan.md](./plan.md)  
**Date**: 2026-06-25

## Overview

This feature operates on markdown files (templates, skills, references, feedback documents) rather than database entities. The "data model" describes the structure and relationships of these document types.

## Entities

### 1. Agent Profile

Represents a supported AI agent tool. Derived from the existing `AGENT_CONFIG` dict in `src/specify_cli/__init__.py` — not a new data structure.

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `slug` | string | Canonical agent identifier (e.g., `claude`, `copilot`, `qoder`) | `AGENT_CONFIG` keys |
| `name` | string | Display name (e.g., "Claude Code", "GitHub Copilot") | `AGENT_CONFIG[key]["name"]` |
| `tier` | enum(tier1, tier2) | Support tier classification | `_ASSISTANT_TIERS[key]` |
| `folder` | string | Agent-specific directory marker (e.g., `.claude/`) | `AGENT_CONFIG[key]["folder"]` |

**Identity**: `slug` (unique across all agents)  
**Lifecycle**: Static — managed by `specify init`; not modified by this feature  
**Grounding**: FR-003, FR-004

### 2. Agent Reference Document

A per-agent, per-skill markdown file containing tool-specific guidance.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `skill_name` | string | Name of the parent skill | Must match a skill in `skills/` |
| `agent_slug` | string | Target agent identifier | Must be a valid `AGENT_CONFIG` key or derived slug |
| `path` | string | File path | `${SKILL_HOME}/references/<agent-slug>-guide.md` |
| `tool_mapping` | section | Maps generic operations to agent-specific tool calls | Required |
| `best_practices` | section | Agent-specific patterns | Required |
| `known_pitfalls` | section | Issues and workarounds | Required |
| `capability_notes` | section | Agent capabilities relevant to skill | Required |

**Identity**: Composite of `skill_name` + `agent_slug` (unique pair)  
**Lifecycle**: Created during implementation; updated by `improve-skills` based on feedback  
**Grounding**: FR-005, FR-006, FR-011

### 3. Inline Agent Guidance (Command Templates)

Agent-specific guidance embedded within command template files. Not a separate file entity.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `command_name` | string | Name of the command template | One of: `agents`, `skills`, `tools` |
| `section_heading` | string | Section title | Must be `## Agent-Specific Configuration` |
| `identification_step` | section | LLM self-identification instructions | Required (Step 1) |
| `guidance_subsections` | section[] | Per-agent inline guidance blocks | At least 2 agents (Claude Code, Copilot) |
| `feedback_step` | section | Feedback capture instructions | Required (Step 3) |

**Identity**: `command_name` (unique — one section per command template)  
**Lifecycle**: Created during implementation; updated manually or by feedback-driven improvement  
**Grounding**: FR-001, FR-005

### 4. Execution Feedback Document

A structured markdown file capturing agent-specific execution obstacles.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `source` | string | Command or skill name that generated this feedback | Required |
| `agent_slug` | string | Agent that encountered the obstacle | Required; valid agent slug |
| `timestamp` | ISO-8601 | When the obstacle was encountered | Required |
| `outcome` | enum | `success-with-workaround`, `partial-failure`, `full-failure` | Required |
| `obstacle` | text | Description of the agent-specific issue | Required |
| `workaround` | text | What was done to work around the issue | Optional (may be empty) |
| `suggested_improvement` | text | Proposed change to the template/reference | Required |
| `path` | string | File path | `.specify/memory/feedback/<source>-<agent-slug>-<timestamp>.md` |

**Identity**: Composite of `source` + `agent_slug` + `timestamp` (unique)  
**Lifecycle**: Created on obstacle encounter; consumed by `improve-skills`/`improve-agent`; archived or deleted after incorporation  
**Grounding**: FR-008, FR-009

## Relationships

```
Agent Profile (1) ──── (0..N) Agent Reference Document
    │                          │
    │                          └── belongs to (1) Skill
    │
    └──── (0..N) Execution Feedback Document
                       │
                       └── references (1) Command or Skill
```

- One Agent Profile can have multiple Reference Documents (one per skill it's documented for)
- One Agent Profile can have multiple Feedback Documents (one per obstacle encountered)
- Each Reference Document belongs to exactly one Skill
- Each Feedback Document references exactly one Command or Skill
- Commands use Inline Agent Guidance instead of Reference Documents

## State Transitions

### Feedback Document Lifecycle

```
[Created] → [Active] → [Incorporated] → [Archived]
```

| State | Description | Trigger |
|-------|-------------|---------|
| Created | Feedback generated during execution | Agent-specific obstacle encountered |
| Active | Available for discovery by improvement workflows | File exists in `.specify/memory/feedback/` |
| Incorporated | Feedback applied to template/reference | `improve-skills` or `improve-agent` processes it |
| Archived | No longer active; kept for historical reference | Manual cleanup or retention policy |
