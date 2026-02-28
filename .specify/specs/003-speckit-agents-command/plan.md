# Implementation Plan: Speckit Agents Command

**Branch**: `003-speckit-agents-command` | **Date**: 2026-02-28 | **Spec**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/003-speckit-agents-command/requirements.md`
**Input**: Specification from `/storage/project/cloud-native-ai/spec-kit/.specify/specs/003-speckit-agents-command/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement `/speckit.agents` as a deterministic planning/authoring command that creates or updates workspace-scoped `.agent.md` files in `.github/agents/`, with strict least-privilege defaults, conflict handling, and approved-provider constraints. The implementation will extend existing prompt-command assets (not terminal runtime commands), add contract/design artifacts for agent lifecycle flows, and align feature memory tracking with SDD governance.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python >=3.8 (project baseline), optimized for Python 3.11+ runtime in docs  
**Primary Dependencies**: Typer, Rich, httpx[socks], platformdirs, readchar, mcp[cli]  
**Storage**: File-based Markdown artifacts (`.github/agents/*.agent.md`, `.specify/specs/**`, `.specify/memory/**`)  
**Testing**: pytest for Python modules; spec/plan acceptance via artifact validation and command-flow checks  
**Target Platform**: Linux/macOS/Windows environments running VS Code-compatible AI chat workflows  
**Project Type**: Single CLI toolkit with template-driven prompt-command assets  
**Performance Goals**: Agent artifact generation/update completes within 2 minutes for normal repository sizes  
**Constraints**: Approved providers only (GitHub Copilot/Qwen Code/opencode), least-privilege default tools, overwrite behavior for same-name agent, low-confidence inference requires user intent prompt  
**Scale/Scope**: Tens to low hundreds of agent files per repository; single-feature planning scope for `003-speckit-agents-command`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Feature-Centric Development**: Feature Index is single source of truth; all phases re-evaluate Feature changes.
- **Specification-Driven Development**: Code serves specifications; specifications are executable and generate working systems
- **Intent-Driven Development**: Focus on "what" and "why" before "how"; use rich specifications with guardrails
- **Test-First & Contract-Driven**: TDD flow followed; pure functions have unit tests; critical flows have regression coverage
- **AI Agent Integration**: Only approved agents (GitHub Copilot, Qwen Code, opencode); configuration rejects unsupported providers
- **Continuous Quality & Observability**: Structured logging; semantic versioning; CI quality gates; simple designs (YAGNI)
- **SDD Workflow Compliance**: Follow spec → plan → tasks → implement workflow with proper validation at each phase

**Gates Status**: ✅ All gates pass

**Additional Constitution Alignment Notes**:
- Feature-Centric: feature index and detail updates are included in this plan output.
- AI Agent Integration: contract/design explicitly reject unsupported providers.
- Continuous Quality: validation rules include YAML correctness, contradiction handling, and least-privilege defaults.

## Phase 0: Research & Context Decisions

- `research.md` is not present for this spec directory; plan context was resolved by reading `README.md`, `docs/**`, `.specify/memory/constitution.md`, `.specify/memory/features.md`, and `.specify/memory/features/001..019.md`.
- Technical unknowns resolved without blocking clarifications.
- No unresolved `NEEDS CLARIFICATION` remain in requirements.

**Phase 0 Output**: Technical Context finalized in this file.

## Phase 1: Design & Contracts

Planned design artifacts:
- `data-model.md`: define AgentDefinition, AgentFrontmatter, ToolPermissionProfile, and lifecycle constraints.
- `contracts/agents-command.openapi.yaml`: define create/update/list/validate flows as API-style contracts mapped from requirements.
- `quickstart.md`: executable validation flow for authoring and updating agents.

**Post-Design Constitution Re-check**: ✅ Pass (no additional gate violations introduced).

## Phase 2: Implementation Planning (for `/speckit.tasks` input)

1. Add/align command prompt behavior for `/speckit.agents` to enforce resolved clarifications.
2. Ensure overwrite semantics, low-confidence intent halt, conflict-resolution precedence, and least-privilege defaults are encoded consistently.
3. Add/refresh validation checks for YAML frontmatter correctness and provider restrictions.
4. Update documentation references where command behavior is surfaced.
5. Validate artifact consistency across requirements/plan/contracts/data model/feature memory.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/003-speckit-agents-command/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Optional Phase 0 output (/speckit.research)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this spec. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
└── specify_cli/

templates/
└── commands/
  └── agents.md

.github/
└── prompts/
  └── speckit.agents.prompt.md

.specify/
├── memory/
│  ├── features.md
│  └── features/019.md
└── specs/003-speckit-agents-command/
  ├── requirements.md
  ├── plan.md
  ├── data-model.md
  ├── quickstart.md
  └── contracts/

tests/
└── [existing or future command-level validation tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

**Structure Decision**: Single CLI toolkit structure is retained. This feature primarily updates prompt-command assets and spec artifacts, with optional Python test coverage under existing test conventions.

## Complexity Tracking

N/A
