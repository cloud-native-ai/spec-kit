# Implementation Plan: Speckit Tools Command

**Branch**: `004-speckit-tools-command` | **Date**: 2026-03-02 | **Spec**: [.specify/specs/004-speckit-tools-command/requirements.md](.specify/specs/004-speckit-tools-command/requirements.md)
**Input**: Specification from `.specify/specs/004-speckit-tools-command/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[CN] MCP-only [CN] `/speckit.tools`[CN]“[CN]+[CN]+[CN]”[CN] MCP-only [CN] MCP/System/Shell/Project [CN] `scripts/bash/refresh-tools.sh` [CN] `.specify/memory/tools/`[CN] feature memory [CN] SDD [CN]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+ (project docs recommendation), compatible with project declaration Python >=3.8  
**Primary Dependencies**: Typer, Rich, httpx (with socks), existing project Bash script system  
**Storage**: [CN]`.specify/memory/tools/*.md`[CN]  
**Testing**: pytest[CN]/[CN]  
**Target Platform**: Linux/macOS/Windows [CN] CLI [CN]  
**Project Type**: single[CN]CLI + templates + scripts[CN]  
**Performance Goals**: 95% [CN] 20 [CN]“[CN]→[CN]→[CN]/[CN]”[CN] 5 [CN]  
**Constraints**: [CN] `/speckit.*` [CN] `.specify/memory/tools/` [CN] AI agent [CN]Copilot/Qwen/opencode[CN]  
**Scale/Scope**: [CN]MCP/System/Shell/Project[CN]

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

- [CN] `$ARGUMENTS` [CN] `requirements.md` [CN]
- [CN] `/speckit.tools`[CN] MCP-only [CN]
- [CN] MCP [CN] system/shell/project tools[CN]

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/004-speckit-tools-command/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command, optional)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command, optional)
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
  ├── commands/
  │   └── (tooling command handlers)
  ├── models/
  └── utils/

templates/
├── commands/
│   └── tools.md
└── mcptool-template.md

scripts/
├── bash/
│   └── refresh-tools.sh
└── python/
  └── list_mcp_tools.py

.specify/memory/
├── tools/
│   └── <tool-name>.md
└── features/
  └── 016.md

# Existing generic layout kept unchanged
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

```

**Structure Decision**: [CN] CLI [CN] memory [CN] `src/`[CN]`templates/`[CN]`scripts/` [CN]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**
> If no violations, explicitly write "N/A" and remove the table.

N/A

## Phase 0: Research Review & Context

- `SPECS_DIR/research.md` [CN] `README.md`[CN]`docs/`[CN]`.specify/memory/features.md` [CN] `features/*.md` [CN]
- [CN] `refresh-tools.sh` [CN]
- [CN] NEEDS CLARIFICATION[CN]

## Phase 1: Design & Contracts

### Data Model

- [CN] `.specify/specs/004-speckit-tools-command/data-model.md`[CN] `ToolRecord`[CN]`ToolSourceDescriptor`[CN]`ToolInvocationSession`[CN]`ToolAlias` [CN]

### Contracts

- [CN] `.specify/specs/004-speckit-tools-command/contracts/tools-command.openapi.yaml`[CN]
- [CN] API-style [CN] `/speckit.tools` [CN]

### Quickstart

- [CN] `.specify/specs/004-speckit-tools-command/quickstart.md`[CN] MCP [CN] MCP [CN]

## Constitution Check (Post-Design Re-check)

- **Feature-Centric Development**: [CN] Feature 016[CN] Feature[CN]
- **Specification-Driven Development**: [CN] FR-001~FR-010 [CN] SC-001~SC-005[CN]
- **Intent-Driven Development**: [CN]“[CN]”[CN]
- **Test-First & Contract-Driven**: [CN] tasks [CN] contract/integration [CN]
- **AI Agent Integration**: [CN] agent [CN] provider[CN]
- **Continuous Quality & Observability**: [CN]YAGNI[CN]
- **SDD Workflow Compliance**: [CN] spec → plan [CN] `/speckit.tasks`[CN]

**Post-Design Gates Status**: ✅ All gates pass

## Phase 2: Implementation Planning

1. [CN] `templates/commands/tools.md`[CN]
2. [CN] MCP/System/Shell/Project [CN]
3. [CN] `.specify/memory/tools/<tool-name>.md`[CN]
4. [CN]
5. [CN]
6. [CN]contract → integration → unit[CN]
