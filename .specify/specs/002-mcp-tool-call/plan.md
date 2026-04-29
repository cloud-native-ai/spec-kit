# Implementation Plan: MCP Tool Call Command

> Archived Note: This plan is based on historical MCP-only capabilities. The current command entry point has been unified as `/speckit.tools`.

**Branch**: `002-mcp-tool-call` | **Date**: 2026-02-10 | **Spec**: [.specify/specs/002-mcp-tool-call/requirements.md](.specify/specs/002-mcp-tool-call/requirements.md)
**Input**: Specification from `.specify/specs/002-mcp-tool-call/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Provide a complete implementation plan for MCP tool invocation scenarios: add MCP tool record templates and command templates, define tool discovery and interactive completion workflows, form reusable tool records in the local `.specify/memory/tools/` directory, and generate data models, contracts, and quick validation steps (current entry point is `/speckit.tools`).

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python >= 3.8  
**Primary Dependencies**: Typer, Rich, httpx[socks], mcp[cli], platformdirs, readchar  
**Storage**: Local file system (`.specify/memory/tools/`)  
**Testing**: pytest[CN]  
**Target Platform**: [CN] CLI[CN]Linux/macOS/Windows[CN]
**Project Type**: single[CN]CLI [CN]  
**Performance Goals**: [CN] ≤ 2 [CN] ≤ 5 [CN]  
**Constraints**: [CN] CLI [CN]  
**Scale/Scope**: [CN] MCP Server[CN]/[CN] MCP [CN]

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

**Additional Constraints from Input**:

- [CN] `templates/mcptool-template.md` [CN] MCP [CN]
- [CN]/[CN] `templates/commands/tools.md` [CN] `templates/commands/clarify.md` [CN]

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/002-mcp-tool-call/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
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
  ├── __init__.py

templates/
├── mcptool-template.md
└── commands/
  └── tools.md

.specify/memory/
└── tools/
  └── <mcp tool name>.md

tests/
└── contract/
  └── test_mcpcall_contracts.py
```

**Structure Decision**: [CN] CLI [CN] `src/specify_cli/commands/`[CN] `templates/` [CN]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**
> If no violations, explicitly write "N/A" and remove the table.

N/A

## Phase 0: Research Review & Context

- [CN] `research.md`[CN] Feature Memory [CN]
- [CN]

## Phase 1: Design & Contracts

### Data Model

- [CN] `.specify/specs/002-mcp-tool-call/data-model.md`[CN] MCP Tool [CN]Server[CN]

### Contracts

- [CN] `contracts/mcptool-record.schema.json` [CN]
- [CN] `contracts/mcpcall-input.schema.json` [CN]

### Quickstart

- [CN] `.specify/specs/002-mcp-tool-call/quickstart.md`[CN]

### Feature Reference

- [CN] `.specify/specs/002-mcp-tool-call/feature-ref.md`[CN] spec/plan [CN]

### Agent Context Update

- [CN] `.specify/scripts/bash/generate-instructions.sh` [CN] `.ai/instructions.md` [CN]

## Phase 2: Implementation Planning

1. [CN] `templates/mcptool-template.md` [CN] MCP [CN]
2. [CN] `templates/commands/tools.md`[CN] `templates/commands/clarify.md` [CN] MCP [CN]
3. [CN] CLI [CN] `/speckit.tools` [CN]
4. [CN] MCP [CN]`.specify/memory/tools/`[CN]
5. [CN]
