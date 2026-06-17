# Implementation Plan: Refactor Tools Command — Definition-First Model

**Branch**: `016-refactor-tools-command` | **Date**: 2026-06-17 | **Spec**: [requirements.md](requirements.md)
**Input**: Specification from `.specify/specs/016-refactor-tools-command/requirements.md`

## Summary

Refactor the `/speckit.tools` command from a discovery-first model (where the system scans for tools and then optionally persists records) to a definition-first model (where users explicitly author tool definitions with behavioral rules, and discovery serves only as a draft-bootstrapping assistant). The core change is that tool definition records — including a new RFC 2119-style "Behavioral Rules" section — become the authoritative source for tool invocation, overriding LLM built-in knowledge. This affects the command template (`templates/commands/tools.md`), tool record templates (`templates/tool-*-template.md`), and the supporting scripts (`create-new-tools.sh`, `refresh-tools.sh`).

## Technical Context

**Language/Version**: Python >=3.8 (per `pyproject.toml`), Bash scripts for automation  
**Primary Dependencies**: Typer (CLI), Rich (rendering), existing Bash/Python script infrastructure  
**Storage**: `.specify/memory/tools/<tool-name>.md` — structured markdown files (existing pattern)  
**Testing**: pytest with markers `contract`, `integration`, `unit` (existing infrastructure)  
**Target Platform**: Linux/macOS/Windows CLI environments, AI chat instruction context  
**Project Type**: Single — CLI toolkit with templates, scripts, and prompt templates  
**Performance Goals**: Tool definition creation completes in under 3 minutes (SC-002); no runtime performance targets (this is a prompt template system, not a server)  
**Constraints**: `/speckit.tools` is an AI chat instruction, not a terminal command; tool records are markdown files, not database entries; must remain compatible with Claude Code, GitHub Copilot, Qwen Code, opencode, and Qoder  
**Scale/Scope**: Three tool types (`project-script`, `system-binary`, `shell-function`); tool registry expected to contain 10–50 tools per project

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Spec 016 requirements.md drives all changes; 14 FRs and 5 SCs trace to user stories |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 016 (Tools Command); feature index updated 2026-06-17 |
| III | Intent-Driven Development | ✅ Pass | Spec focuses on WHAT (definition-first model) and WHY (LLM knowledge interference); HOW deferred to this plan |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Contract artifacts generated in Phase 1; TDD order enforced in tasks phase |
| V | AI Agent Integration Standards | ✅ Pass | Only approved agents supported; tool definitions are agent-agnostic prompt artifacts consumed by all five approved agents |
| VI | Continuous Quality & Observability | ✅ Pass | YAGNI: no speculative features; behavioral rules are minimal addition to existing template structure |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Full SDD workflow: requirements (done) → plan (this) → tasks → implement |

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/016-refactor-tools-command/
├── plan.md              # This file
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── tools-command.openapi.yaml
├── checklists/
│   └── requirements.md  # Quality checklist (created during requirements)
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created by /speckit.plan)
```

No standalone research.md — findings inlined below in Phase 0.

### Source Code (repository root)

```text
templates/
├── commands/
│   └── tools.md                      # Command template — PRIMARY CHANGE TARGET
├── tool-project-script-template.md   # Add Behavioral Rules section
├── tool-system-binary-template.md    # Add Behavioral Rules section
└── tool-shell-function-template.md   # Add Behavioral Rules section

scripts/bash/
├── create-new-tools.sh               # Refactor: definition-first flow
└── refresh-tools.sh                  # Refactor: discovery as draft assistant

.specify/memory/tools/                # Tool definition records (existing directory)
```

**Structure Decision**: Extends the existing CLI toolkit structure. No new top-level directories. Changes are concentrated in `templates/` (command template + 3 tool record templates) and `scripts/bash/` (2 scripts). The `.specify/memory/tools/` storage location is unchanged.

## Complexity Tracking

N/A — no constitution violations.

## Phase 0: Research Review & Context

No `research.md` exists. Findings derived from analysis of existing artifacts:

1. **Current architecture**: The existing `templates/commands/tools.md` follows a 10-step flow: identify → discover → resolve naming → reuse/create record → ID-first resolution → validate → collect parameters → confirmation gate → execute → report. Discovery (step 2, via `create-new-tools.sh`) is the primary entry point.

2. **Key gap**: Tool record templates (`tool-*-template.md`) have no "Behavioral Rules" section. The AI agent currently relies on Description, Parameters, Returns, and Usage Notes to understand tool behavior — all of which can be overridden by LLM built-in knowledge for well-known tools.

3. **Backward compatibility**: Existing tool records lack a Behavioral Rules section but otherwise match the refactored structure. Adding the section is additive — no migration needed.

4. **Discovery scripts**: `create-new-tools.sh` supports `--action find` for discovery. `refresh-tools.sh` scans system/shell/project sources via `tools-utils.py`. Both produce JSON output. Under the refactored model, these scripts support "discovery-assists-definition" (FR-013) rather than serving as the primary flow.

5. **Command template rewrite scope**: The `templates/commands/tools.md` Outline section needs restructuring to make definition (create/modify) the primary action (step 1), with discovery repositioned as a draft-bootstrapping helper when no record exists. The confirmation gate (step 8) and registration (step 10) are preserved.

## Phase 1: Design & Contracts

### Data Model

Generated as `data-model.md` — see below.

### Contracts

Generated as `contracts/tools-command.openapi.yaml` — see below.

### Quickstart

Generated as `quickstart.md` — see below.

## Constitution Check (Post-Design Re-check)

**Re-check**: 2026-06-17 — All design artifacts verified against constitution principles.

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Data model entities trace to FRs (FR-001–FR-014); contract endpoints map to user stories |
| II | Feature-Centric Development | ✅ Pass | Feature 016 updated; no new features needed; no features deprecated |
| III | Intent-Driven Development | ✅ Pass | Behavioral Rules entity captures user intent explicitly; definition-first flow prioritizes WHAT over HOW |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | OpenAPI contract covers all command operations; validation rules defined for all entities |
| V | AI Agent Integration Standards | ✅ Pass | Tool definitions are agent-agnostic markdown consumed by all five approved agents |
| VI | Continuous Quality & Observability | ✅ Pass | Status field tracks record lifecycle; no speculative features added |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Plan complete with data model, contracts, quickstart; ready for /speckit.tasks |

**Post-Design Gates Status**: ✅ All gates pass
