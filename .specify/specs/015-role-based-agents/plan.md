# Implementation Plan: Role-Based Agent Templates

**Branch**: `015-role-based-agents` | **Date**: 2026-06-17 | **Spec**: [requirements.md](./requirements.md)
**Input**: Specification from `.specify/specs/015-role-based-agents/requirements.md`

## Summary

Replace the four capability-based agent templates (common, knowledge, plan, research) with six role-based agent templates that model a software development team: Requirements Analyst, System Designer, Module Designer, Test Engineer, QA Engineer, and Knowledge Manager. Update the `/speckit.agents` command prompt to use role-based templates instead of type-based classification. Each generated agent is dynamically populated with project context at generation time.

Additionally, the `/speckit.agents` command retains its focus on generating agents from templates into the project workspace, while new companion skills (`create-agent`, `improve-agent`) handle the evolution of agent templates and preset logic themselves — mirroring the existing `create-skills` / `improve-skills` pattern.

## Technical Context

**Language/Version**: Python >=3.8  
**Primary Dependencies**: typer, rich, httpx[socks], platformdirs  
**Storage**: File-based (Markdown templates with YAML frontmatter)  
**Testing**: pytest (markers: contract, integration)  
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)  
**Project Type**: Code generator / framework (templates/, scripts/, src/specify_cli/)  
**Performance Goals**: All six agents generated in under 2 minutes per invocation  
**Constraints**: Must maintain symlink compatibility across .github/, .qoder/, .qwen/, .opencode/ directories  
**Scale/Scope**: Six role templates, one command prompt update, two new skills, four template deletions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | This plan is driven by spec 015-role-based-agents/requirements.md; every design decision traces to an FR |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 019 (Agents Command); feature index updated with this spec path |
| III | Intent-Driven Development | ✅ Pass | Role templates focus on "what" each role does and "why" — agent instructions express intent, not implementation |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Contract tests for template rendering and agent generation defined in quickstart.md |
| V | AI Agent Integration Standards | ✅ Pass | Generated agents target approved providers only (Claude Code, Copilot, Qwen, opencode, Qoder); symlink model maintained |
| VI | Continuous Quality & Observability | ✅ Pass | Version-controlled templates; agent generation is idempotent with backup semantics (FR-008a) |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Following full SDD workflow: requirements → clarify → plan → tasks → implement |

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/015-role-based-agents/
├── requirements.md      # Feature specification
├── plan.md              # This file
├── quickstart.md        # Validation scenarios
├── checklists/
│   └── requirements.md  # Quality checklist
└── tasks.md             # Task breakdown (created by /speckit.tasks)
```

No standalone research.md — findings inlined in this plan from project docs and code analysis.

### Source Code (repository root)

```text
templates/                          # Role-based agent templates (6 new, 4 deleted)
├── agent-role-requirements-analyst-template.md
├── agent-role-system-designer-template.md
├── agent-role-module-designer-template.md
├── agent-role-test-engineer-template.md
├── agent-role-qa-engineer-template.md
├── agent-role-knowledge-manager-template.md
templates/commands/agents.md        # Updated command prompt (role-based generation flow)
skills/create-agent/SKILL.md        # New skill: create custom agent templates
skills/improve-agent/SKILL.md       # New skill: improve existing agent templates
agents/                             # Updated bundled agents (installed by specify init)
```

**Structure Decision**: Extends the existing code generator / framework layout. New role templates follow the existing `templates/agent-*-template.md` naming pattern with a `-role-` infix to distinguish them. Two new skills follow the existing `skills/<name>/SKILL.md` structure. No new top-level directories.

## Clarifications

### Session 2026-06-17

- Q: How should the `tools` field be set in role-based agent template frontmatter, given FR-009a requires full read-write access? → A: Omit `tools` entirely — inherits platform defaults, giving full tool access per FR-009a. Simplest and most forward-compatible.

## Phase 0: Research Review

### Key Findings from Code Analysis

1. **Current agent generation flow** (`templates/commands/agents.md`):
   - User provides input or agent is inferred from conversation context
   - Agent is classified into one of four types: Knowledge, Plan, Research, Common
   - Type maps to a template: `templates/agent-{type}-template.md`
   - Template is rendered with placeholder substitution
   - Generated `.agent.md` file is written to `.specify/agents/`

2. **Template structure** (all four current templates):
   - YAML frontmatter with `{{PLACEHOLDER}}` variables: name, description, argument-hint, target, tools, agents, model, handoffs
   - Body with role definition, constraints, workflow, and output sections
   - Each template ~30-40 lines, with type-specific instructions

3. **`specify init` bundling** (`src/specify_cli/__init__.py:991-1005`):
   - Copies `agents/` directory from package resources to `.specify/agents/`
   - Currently contains only `code-reviewer.agent.md` and `references/.gitkeep`
   - This is the mechanism for pre-installing bundled role-based agents

4. **Symlink model** (`ensure_specify_symlink()` at line 762):
   - Creates directory-level symlinks from `.github/agents/`, `.qoder/agents/`, `.qwen/agents/`, `.opencode/agents/` → `.specify/agents/`
   - Already generalized for both skills and agents
   - No changes needed to the symlink infrastructure

5. **Existing skill patterns** (`create-skills/`, `improve-skills/`):
   - `create-skills` creates new skills from user input or conversation history
   - `improve-skills` iteratively improves existing skills from execution feedback
   - Both follow a consistent structure: frontmatter → goal → workflow → constraints
   - New `create-agent` and `improve-agent` skills should mirror this pattern

### Design Decisions

**D1: Template naming convention**: Use `agent-role-<role-slug>-template.md` (e.g., `agent-role-requirements-analyst-template.md`) to clearly distinguish role templates from the old type templates, and to avoid ambiguity with any future template types.

**D2: Command prompt update approach**: Update `templates/commands/agents.md` to replace the four-type classification (Knowledge/Plan/Research/Common) with a role-based selection flow. When invoked without arguments, the command generates all six role-based agents. When invoked with arguments describing a custom agent, it falls back to the existing `agent-common-template.md` pattern (now embedded in the command itself) for ad-hoc agent creation.

**D3: Role templates vs command prompt separation**: Role templates define the static structure and role identity. The `/speckit.agents` command prompt defines the dynamic context injection logic — how to read the project state and resolve placeholders at generation time. This separation means role templates are pure templates (no generation logic), and the command prompt handles orchestration.

**D4: Bundled agents**: The six role-based templates under `templates/` are the source-of-truth for role definitions. The `agents/` directory at package root (installed by `specify init`) will contain the `code-reviewer.agent.md` (existing) but NOT pre-generated role agents — role agents are generated dynamically by `/speckit.agents` because they require project context.

**D5: Skill scope separation**: `/speckit.agents` generates agents from preset templates into `.specify/agents/` (output: project-specific agent files). `create-agent` skill creates/modifies the preset templates in `templates/` (output: reusable template files). `improve-agent` skill refines existing agent templates based on execution feedback (output: improved template files). This mirrors the `skills` vs `create-skills`/`improve-skills` separation.

**D6: Backup detection for FR-008a**: When regenerating role-based agents, compare the existing file content against what would be generated from the template. If they differ (user has customized), create a `.bak` copy before overwriting. This is a simple content-hash comparison.

## Phase 1: Design & Contracts

### Data Model

#### Entity: Role Template

A parameterized Markdown file in `templates/` defining a development workflow role.

| Field | Type | Description |
|-------|------|-------------|
| Template file | Path | `templates/agent-role-<slug>-template.md` |
| Role slug | String | kebab-case identifier (e.g., `requirements-analyst`) |
| Role name | String | Display name (e.g., `Requirements Analyst`) |
| Role identity | Text | First-person professional identity statement |
| Responsibilities | Text | Core duties of this role |
| Upstream | List[String] | Roles/artifacts that provide inputs |
| Downstream | List[String] | Roles/artifacts that consume outputs |
| Workflow | Text | Step-by-step workflow for the role |
| Output format | Text | Expected output structure |
| Context placeholders | List[String] | `{{PLACEHOLDER}}` variables resolved at generation time |

**Context placeholders** used across all role templates:

| Placeholder | Resolved from | Used by roles |
|-------------|---------------|---------------|
| `{{PROJECT_NAME}}` | README.md or pyproject.toml | All |
| `{{TECH_STACK}}` | pyproject.toml dependencies, package.json, etc. | All |
| `{{PROJECT_STRUCTURE}}` | Directory tree analysis | System Designer, Module Designer |
| `{{MODULE_LIST}}` | Source directory scan | Module Designer |
| `{{CONSTITUTION_PRINCIPLES}}` | .specify/memory/constitution.md | QA Engineer, System Designer |
| `{{FEATURE_INDEX}}` | .specify/memory/features.md | System Designer, Knowledge Manager |
| `{{SPECS_DIR}}` | .specify/specs/ listing | Requirements Analyst, System Designer |
| `{{TESTING_FRAMEWORK}}` | pyproject.toml or package.json test config | Test Engineer |
| `{{DOCS_DIR}}` | docs/ listing | Knowledge Manager |

#### Entity: Generated Agent

A concrete `.agent.md` file produced by resolving a Role Template.

| Field | Source | Description |
|-------|--------|-------------|
| File path | Template slug | `.specify/agents/<slug>.agent.md` |
| YAML frontmatter | Template + context | name, description, tools, user-invocable, etc. |
| Body | Template + context | Role instructions with project-specific details |

#### Entity: Workflow Handoff

Defined in each agent's body as upstream/downstream references.

| Handoff | From | To | Artifact |
|---------|------|----|----------|
| Requirements → Design | Requirements Analyst | System Designer | Clarified requirements document |
| Design → Module | System Designer | Module Designer | Design specification, interface contracts |
| Module → Test | Module Designer | Test Engineer | Implementation changes, module boundaries |
| Test → Module (feedback) | Test Engineer | Module Designer | Test results, failure reports |
| Test → QA | Test Engineer | QA Engineer | Test coverage report |
| Design → QA | System Designer | QA Engineer | Architecture design document |
| QA → Requirements (gap) | QA Engineer | Requirements Analyst | Gap analysis, unmet requirements |
| All → Knowledge | All roles | Knowledge Manager | Artifacts, decisions, changes |
| Knowledge → All | Knowledge Manager | All roles | Documentation, knowledge base |

### Template Structure (common across all six roles)

Each role template follows this structure:

```markdown
---
name: {{AGENT_NAME}}
description: {{AGENT_DESCRIPTION}}
user-invocable: true
disable-model-invocation: false
---
You are a **{{ROLE_NAME}}** for the {{PROJECT_NAME}} project.

## Identity & Responsibilities

{{ROLE_IDENTITY}}

## Project Context

{{PROJECT_CONTEXT}}

## Workflow

{{ROLE_WORKFLOW}}

## Upstream (Inputs)

{{UPSTREAM_DESCRIPTION}}

## Downstream (Outputs)

{{DOWNSTREAM_DESCRIPTION}}

## Output Format

{{OUTPUT_FORMAT}}
```

### Command Prompt Update Design

The updated `templates/commands/agents.md` replaces the type-classification flow (steps 5-8) with:

1. **No arguments**: Generate all six role-based agents
   - Read project context (tech stack, directory structure, constitution, features)
   - For each role template, resolve placeholders and write to `.specify/agents/`
   - Before overwriting, check for user modifications → backup if modified (FR-008a)
   - Preserve non-role agents (e.g., `code-reviewer.agent.md`)

2. **With arguments (custom agent)**: Fall back to general-purpose agent creation
   - Use the existing ad-hoc agent creation flow
   - Classify by intent, generate from a generic template structure
   - This preserves the current custom agent creation capability

### Skills Design

#### `create-agent` Skill

Mirrors `create-skills` pattern. Purpose: create new role-based agent templates or customize existing ones in `templates/`.

- **Input**: Role description, responsibilities, workflow constraints
- **Output**: New or updated `templates/agent-role-<name>-template.md`
- **Scope**: Operates on templates (the source-of-truth for roles), not on generated agents in `.specify/agents/`

#### `improve-agent` Skill

Mirrors `improve-skills` pattern. Purpose: iteratively improve agent templates based on execution feedback.

- **Input**: Target agent template identifier + execution evidence (user feedback, failure cases, behavioral drift)
- **Output**: Updated `templates/agent-role-<name>-template.md` with improved instructions
- **Scope**: Same as `create-agent` — operates on templates

## Complexity Tracking

N/A — no constitution violations requiring justification.

## Re-check after Phase 1

**Date**: 2026-06-17

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | All design decisions trace to FRs (001-010); data model entities derive from spec Key Entities |
| II | Feature-Centric Development | ✅ Pass | Feature 019 updated; feature index reflects this spec |
| III | Intent-Driven Development | ✅ Pass | Role templates express intent ("what this role does") not implementation ("how to code it") |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Quickstart validation scenarios defined; template rendering is testable |
| V | AI Agent Integration Standards | ✅ Pass | All agents target approved providers; symlink model preserved |
| VI | Continuous Quality & Observability | ✅ Pass | Backup semantics for regeneration; templates version-controlled |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Full workflow followed |

**Gates Status**: ✅ All gates pass
