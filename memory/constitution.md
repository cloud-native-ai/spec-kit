<!--
Sync Impact Report:
- Version change: Template → 1.0.0
- List of modified principles: Defined all core principles (Spec-Driven, Agent-First, Library/CLI, Test-First, Context).
- Added sections: Technology Guidelines, Development Workflow.
- Removed sections: N/A
- Templates requiring updates:
    - templates/plan-template.md (⚠ updated in this session)
    - templates/tasks-template.md (⚠ updated in this session)
    - templates/spec-template.md (✅ verified)
- Follow-up TODOs: None.
-->

# Spec Kit Constitution

## Core Principles

### I. Spec-Driven Architecture
Development MUST flow from Specification to Implementation.
- **Code is downstream of Specs**: No logic changes without a preceding spec update.
- **Executable Specs**: Specifications should aim to be machine-readable or directly testable where possible.
- **Why over How**: Document the intent and "why" before diving into the implementation details.

Rationale: Prevents "vibe coding" and ensures predictable, aligned outcomes.

### II. Agent-First Design
Artifacts MUST be optimized for both Human and AI consumption.
- **Structured Context**: Use clear directory structures, index files, and consistent naming conventions.
- **Explicit Intent**: Avoid ambiguity; be verbose if it adds clarity for an LLM context window.
- **Self-Documenting**: Code and docs should explain themselves without external knowledge dependency.

Rationale: Enables AI agents (Copilot, etc.) to function as effective pair programmers.

### III. Library-First & CLI-First
Functionality MUST be encapsulated in reusable libraries with CLI interfaces.
- **Library Core**: Core logic resides in isolated, testable Python packages/modules.
- **CLI Exposure**: Every significant library feature MUST be exposed via a CLI (using `typer`) for easy composition and agent testing.
- **Text I/O**: Prefer plain text or JSON inputs/outputs to facilitate piping and automation.

Rationale: Promotes modularity, reusability, and ease of automated testing/invocation.

### IV. Test-First Quality Gates
Quality is non-negotiable and automated.
- **TDD Flow**: Write tests/contracts before implementation.
- **Red-Green-Refactor**: Strictly follow the cycle.
- **Automated Gates**: Linting, type checking, and tests MUST pass before merging.

Rationale: Reduces regressions and enforces the "Quality" aspect of the project goals.

### V. Context Preservation
Maintain the integrity of the project's memory.
- **Update Logs**: Keep `CHANGELOG.md` and feature indices up to date.
- **Decision Records**: Major architectural decisions MUST be recorded in plans or specs.
- **Single Source of Truth**: Identify and respect the authoritative source for any given piece of information.

Rationale: Prevents knowledge loss and context drift over time.

## Technology Guidelines

**Language & Stack**:
- Python 3.8+ (Core)
- Typer (CLI)
- Rich (Terminal UI)
- Hatchling (Build System)

**Dependencies**:
- Keep dependency tree minimal.
- Prefer standard library where reasonable.
- Pin versions to avoid upstream breakages.

## Development Workflow

1.  **Specify**: Define the functionality and success criteria in `.specify/specs/`.
2.  **Plan**: Create a technical plan mapping specs to code structures.
3.  **Task**: Break down the plan into atomic, parallelizable tasks.
4.  **Implement**: Execute tasks with TDD and commit frequently.
5.  **Review**: Verify against the original Specification.

## Governance

**Authority**:
This Constitution supersedes all other loose guidelines. Changes to these principles require a formal amendment and version bump.

**Amendment Process**:
1.  Propose change via PR.
2.  Update version number (Semantic Versioning).
3.  Update `Last Amended` date.

**Compliance**:
All Pull Requests and Agent interactions MUST verify compliance with these Core Principles.

**Version**: 1.0.0 | **Ratified**: 2026-01-18 | **Last Amended**: 2026-01-18
