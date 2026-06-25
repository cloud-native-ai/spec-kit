# Implementation Plan: Agent-Specific Configuration for Commands and Skills

**Branch**: `021-agent-specific-config` | **Date**: 2026-06-25 | **Spec**: [requirements.md](./requirements.md)
**Input**: Specification from `.specify/specs/021-agent-specific-config/requirements.md`

## Summary

Add an "Agent-Specific Configuration" section to 7 high-impact files (3 command templates, 4 skills) that implements a three-step agent adaptation workflow: (1) identify the executing AI agent via environmental signals, (2) load agent-specific guidance from inline sections (commands) or `references/` subdocuments (skills), and (3) capture execution feedback to `.specify/memory/feedback/` for continuous optimization. This is a template/document-only change — no Python CLI code changes are required; all modifications are to markdown prompt templates and reference files.

## Technical Context

**Language/Version**: Python >=3.8 (project runtime); Markdown (primary artifact format — all changes are template/document edits)  
**Primary Dependencies**: None new — this spec modifies markdown templates only; existing `typer`, `rich` runtime is unaffected  
**Storage**: File-based — `.specify/memory/feedback/` directory for feedback documents; `${SKILL_HOME}/references/` for skill-level agent guides  
**Testing**: pytest with `contract` and `integration` markers; contract tests validate template structure, integration tests validate end-to-end skill execution  
**Target Platform**: Cross-platform (macOS, Linux) — all artifacts are markdown files  
**Project Type**: Code generator / framework — extends `templates/` and `skills/` directories  
**Performance Goals**: N/A — template content has no runtime performance impact  
**Constraints**: Templates must remain compatible with all supported agents; agent-specific sections must be additive (FR-010); no restructuring of single-file command templates into directories  
**Scale/Scope**: 7 target files, up to 8 agent reference documents per skill (Claude Code + Copilot at launch), centralized feedback directory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | This plan traces directly to requirements.md FR-001 through FR-011; every template change has a corresponding requirement |
| II | Feature-Centric Development | ✅ Pass | Spec bound to Feature 022 (AI Tools Support); feature index and feature detail updated in clarify phase |
| III | Intent-Driven Development | ✅ Pass | Spec focuses on WHAT (agent-specific adaptation) and WHY (different agents have different capabilities); implementation details are minimal |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Contract tests defined for template structure validation (section headings, reference file existence); see contracts/ |
| V | AI Agent Integration Standards | ✅ Pass | All 8 officially supported agents are addressed (FR-003); tier classification from `_ASSISTANT_TIERS` is respected; agent slugs match `AGENT_CONFIG` keys |
| VI | Continuous Quality & Observability | ✅ Pass | Feedback generation (FR-008, FR-009) adds observability for agent-specific execution quality; documents are structured for analysis |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Following full SDD workflow: requirements → clarify → plan → tasks → implement |

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/021-agent-specific-config/
├── plan.md              # This file
├── requirements.md      # Feature specification
├── checklists/          # Quality checklists
│   └── requirements.md
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output
    └── agent-specific-config.contract.md
```

No standalone research.md — findings inlined below from project analysis.

### Source Code (repository root)

```text
templates/commands/agents.md       # Add inline Agent-Specific Configuration section
templates/commands/skills.md       # Add inline Agent-Specific Configuration section
templates/commands/tools.md        # Add inline Agent-Specific Configuration section
skills/browser-utils/SKILL.md      # Add Agent-Specific Configuration section with references/ pointer
skills/browser-utils/references/   # Add claude-code-guide.md, copilot-guide.md
skills/create-agent/SKILL.md       # Add Agent-Specific Configuration section with references/ pointer
skills/create-agent/references/    # Create dir; add claude-code-guide.md, copilot-guide.md
skills/improve-agent/SKILL.md      # Add Agent-Specific Configuration section with references/ pointer
skills/improve-agent/references/   # Create dir; add claude-code-guide.md, copilot-guide.md
skills/improve-skills/SKILL.md     # Add Agent-Specific Configuration section with references/ pointer
skills/improve-skills/references/  # Add claude-code-guide.md, copilot-guide.md (dir exists)
.specify/memory/feedback/          # Create centralized feedback directory
tests/contract/                    # Contract tests for template structure validation
```

**Structure Decision**: Extends the existing code-generator/framework layout by adding content to existing template and skill files, creating `references/` subdirectories where missing (create-agent, improve-agent), adding agent-specific reference documents, and creating the `.specify/memory/feedback/` directory for centralized feedback storage. No new top-level directories.

## Phase 0: Research Review

No standalone `research.md` exists. Findings from project analysis:

### Agent Identification Signals

The existing `AGENT_CONFIG` dict in `src/specify_cli/__init__.py` defines 8 supported agents with their keys: `claude`, `codex`, `qoder`, `copilot`, `opencode`, `qwen`, `hermes`, `iflow`. These keys serve as the canonical agent slugs for reference file naming.

At the template/prompt level (where commands and skills execute), agent identification relies on environmental signals observable by the LLM at runtime:

| Agent | Detection Signal | Slug |
|-------|-----------------|------|
| Claude Code | System prompt mentions "Claude Code", `Agent` tool available, `.claude/` directory exists | `claude-code` |
| GitHub Copilot | VS Code Copilot chat context, `.github/copilot-instructions.md` loaded | `copilot` |
| Qoder CLI | `.qoder/` directory exists, QODER.md instructions loaded | `qoder` |
| opencode | `.opencode/` directory exists | `opencode` |
| Qwen Code | QWEN.md instructions loaded, `.qwen/` directory exists | `qwen` |
| Codex CLI | `.codex/` directory exists | `codex` |
| Hermes Agent | `.hermes/` directory exists | `hermes` |
| iFlow | `.iflow/` directory exists | `iflow` |

Since commands and skills are markdown prompt templates interpreted by the LLM, "detection" means the LLM self-identifies based on its known identity and available tool context. The Agent-Specific Configuration section instructs the LLM to perform this self-identification.

### Existing References Directory State

| Skill | `references/` exists | Current files |
|-------|---------------------|---------------|
| browser-utils | ✅ | `playwright-api.md` |
| create-agent | ❌ | — |
| improve-agent | ❌ | — |
| improve-skills | ✅ | `skill-quality-checklist.md`, `skill-slimming-principles.md` |

### Agent-Specific Capability Differences (Key Examples)

These differences motivate the need for agent-specific guidance:

| Capability | Claude Code | Copilot | Qoder |
|-----------|-------------|---------|-------|
| Subagent delegation | `Agent` tool with typed agents | `@agent` mentions in chat | Not supported |
| File editing | `Edit` (diff-based), `Write` (full replace) | Inline code suggestions, workspace edits | Shell-based editing |
| Shell execution | `Bash` tool with timeout/background | Terminal panel (limited) | Direct shell access |
| Web fetching | `WebFetch`, `WebSearch` tools | Limited | `curl`-based |
| Structured output | JSON schema via tool calls | Markdown-based | Markdown-based |

## Phase 1: Design & Contracts

### Design Decisions

**D1: Agent-Specific Configuration Section Structure**

The section added to each target file follows a consistent three-step structure:

```markdown
## Agent-Specific Configuration

### Step 1: Identify Executing Agent

[Instructions for the LLM to self-identify which agent it is running as,
based on environmental signals — system prompt, available tools, loaded
instructions files, directory markers]

### Step 2: Load Agent-Specific Guidance

[For commands: inline subsections per agent with tool-specific notes]
[For skills: pointer to ${SKILL_HOME}/references/<agent-slug>-guide.md]

### Step 3: Capture Execution Feedback

[Instructions to generate a feedback document at
.specify/memory/feedback/<name>-<agent>-<timestamp>.md when
agent-specific obstacles are encountered]
```

**D2: Reference Document Structure**

Each `<agent-slug>-guide.md` follows a consistent structure:

```markdown
# <Skill Name> — <Agent Name> Guide

## Tool Mapping
[Maps generic skill operations to agent-specific tool calls]

## Best Practices
[Agent-specific patterns that improve execution quality]

## Known Pitfalls
[Agent-specific issues and workarounds]

## Capability Notes
[What this agent can/cannot do relevant to this skill]
```

**D3: Feedback Document Structure**

Each feedback document at `.specify/memory/feedback/` follows:

```markdown
# Agent Execution Feedback

**Source**: <command-or-skill-name>
**Agent**: <agent-slug>
**Timestamp**: <ISO-8601>
**Outcome**: <success-with-workaround | partial-failure | full-failure>

## Obstacle
[Description of the agent-specific issue]

## Workaround Applied
[What was done to work around the issue, if anything]

## Suggested Improvement
[Specific change to the command/skill template or reference document]
```

**D4: Inline vs Reference Split**

- **Command templates** (agents.md, skills.md, tools.md): Inline agent-specific guidance within the template file. Rationale: command templates are single files used as prompt templates; adding a `references/` directory would require restructuring how the CLI processes them.
- **Skills** (browser-utils, create-agent, improve-agent, improve-skills): External reference files at `${SKILL_HOME}/references/<agent-slug>-guide.md`. Rationale: skills already have a directory structure with `references/`; external files keep SKILL.md concise and allow agent guides to be updated independently.

### Re-check after Phase 1

**Re-check date**: 2026-06-25

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Plan traces all design decisions to FR-001–FR-011 |
| II | Feature-Centric Development | ✅ Pass | Feature 022 detail and index updated |
| III | Intent-Driven Development | ✅ Pass | Design focuses on what (section structure) and why (agent differences) |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Contract spec defines structural validation rules; tests precede implementation in task ordering |
| V | AI Agent Integration Standards | ✅ Pass | All 8 agents in `_OFFICIAL_ASSISTANT_KEYS` addressed; tier-1 agents (Claude Code, Copilot) get reference docs at launch |
| VI | Continuous Quality & Observability | ✅ Pass | Feedback document system adds structured observability |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Full workflow followed |

**Gates Status**: ✅ All gates pass (post-design)

## Complexity Tracking

N/A — no constitution violations requiring justification.
