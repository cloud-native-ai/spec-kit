# Implementation Plan: Claude Code Support

**Branch**: `009-claude-code-support` | **Date**: 2026-05-14 | **Spec**: [.specify/specs/009-claude-code-support/requirements.md](.specify/specs/009-claude-code-support/requirements.md)
**Input**: Specification from `.specify/specs/009-claude-code-support/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add Claude Code as a first-class Spec Kit assistant integration. The implementation will extend assistant selection and validation, generate Claude Code custom commands and special configuration files such as `.claudeignore`, refresh Claude Code compatibility surfaces from canonical Spec Kit instructions, and update governance/documentation so Claude Code support is consistent with existing assistant integrations.

## Technical Context

**Language/Version**: Python >=3.8 for CLI code; Bash for project scripts; Markdown/YAML for generated command, instruction, and contract assets.  
**Primary Dependencies**: Typer, Rich, httpx[socks], platformdirs, readchar, mcp[cli], packaged templates under `templates/`, and shell scripts under `scripts/bash/`.  
**Storage**: File-based project assets under `.specify/`, `.github/`, `.qwen/`, `.opencode/`, `.qoder/`, and new `.claude/` / root Claude Code compatibility files; no database storage.  
**Testing**: pytest with existing `tests/contract`, `tests/integration`, and `tests/unit` structure; shell-script behavior validated through script/API helpers where possible.  
**Target Platform**: Cross-platform CLI distribution with primary validation on Linux/macOS and generated project compatibility for common Spec Kit workspaces.  
**Project Type**: Single Python CLI package with bundled templates, scripts, docs, and SDD artifacts.  
**Performance Goals**: Claude Code asset generation and refresh complete within normal initialization time; users can confirm required Claude Code assets in under 3 minutes after setup begins.  
**Constraints**: Claude Code must become an officially approved assistant in governance before release readiness; new assets must not break Copilot, Qwen Code, opencode, or Qoder support; Claude Code files must remain compatibility surfaces derived from canonical Spec Kit instructions.  
**Scale/Scope**: One new assistant integration covering CLI selection, generated commands, `.claudeignore`, instruction refresh, docs, tests, packaging, and Feature 021 tracking.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Feature-Centric Development**: Feature 021 is registered and linked to this specification. Planning reuses patterns from Feature 020 (Qoder Support) without merging or splitting existing features.
- **Specification-Driven Development**: FR-001 through FR-011, user stories, edge cases, and success criteria drive all planned code, docs, templates, and tests.
- **Intent-Driven Development**: The plan preserves the user intent: Claude Code support with custom commands and `.claudeignore`-style configuration, while deferring implementation mechanics to tasks.
- **Test-First & Contract-Driven**: Contract, integration, and unit tests will be authored before implementation tasks for assistant selection, command generation, ignore policy, refresh, governance, and distribution behavior.
- **AI Agent Integration**: Current constitution lists approved assistants as GitHub Copilot, Qwen Code, opencode, and Qoder. This feature requires a governance update to add Claude Code before release readiness is claimed; until that update lands, Claude Code implementation is blocked from being considered complete.
- **Continuous Quality & Observability**: The implementation must keep CLI/help output, docs, generated assets, and packaged resources auditable with clear validation messages and no speculative assistant surfaces.
- **SDD Workflow Compliance**: Requirements and clarification are complete; this plan produces design artifacts and hands off to `/speckit.tasks`.

**Gates Status**: ✅ All gates pass for planning with one explicit release blocker: update constitutional and documentation governance so Claude Code is officially approved before implementation can be marked ready for review.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/009-claude-code-support/
├── requirements.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── claude-code-support.openapi.yaml
├── feature-ref.md
├── checklists/
│   └── requirements.md
└── tasks.md             # Created later by /speckit.tasks
```

### Source Code (repository root)

```text
src/
└── specify_cli/
   └── __init__.py

scripts/
└── bash/
   ├── generate-instructions.sh
   └── *.sh

templates/
├── commands/
│   └── *.md
├── instructions-template.md
├── plan-template.md
├── agent-*.md
└── vscode-settings.json

docs/
├── installation.md
├── quickstart.md
├── usage.md
└── skills/

.specify/
├── memory/
│   ├── constitution.md
│   ├── features.md
│   └── features/021.md
└── specs/
   └── 009-claude-code-support/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Use the existing single Python CLI structure. Assistant support belongs in `src/specify_cli/__init__.py`, generated workflow command templates under `templates/commands/`, instruction refresh in `scripts/bash/generate-instructions.sh`, docs in `README.md` and `docs/`, governance in `.specify/memory/constitution.md`, and tests in the existing contract/integration/unit hierarchy.

## Complexity Tracking

N/A

## Phase 0: Research Review & Context

- Reviewed `README.md`, `docs/installation.md`, `docs/usage.md`, `docs/quickstart.md`, `docs/spec-driven.md`, and `docs/upstream.md` for assistant support, SDD workflow, initialization, and command expectations.
- Reviewed `.specify/memory/constitution.md`, `.specify/memory/features.md`, Feature 020 (Qoder Support), Feature 019 (Agents Command), Feature 017 (Template Engine), Feature 015 (CLI Interface), and Feature 008 (Instructions Command) for integration boundaries.
- Inspected `pyproject.toml`, `src/specify_cli/__init__.py`, `scripts/bash/generate-instructions.sh`, `templates/commands/`, and existing Qoder tests/artifacts to identify reusable assistant-support patterns.
- No separate `research.md` existed at plan start; Phase 0 decisions are captured in the generated `research.md` artifact.

**Phase 0 Output**: `research.md`

## Phase 1: Design & Contracts

### Design Decisions

1. **Assistant metadata and validation**
  - Add Claude Code to the assistant support matrix with a stable key, display name, folder, install guidance, and CLI validation expectation.
  - Keep unsupported assistant rejection behavior; only expand the approved list once governance is updated.

2. **Claude Code asset generation**
  - Generate custom command files from the canonical `templates/commands/*.md` inventory into a Claude Code-discoverable command location.
  - Generate or refresh Claude Code-specific guidance and `.claudeignore` defaults as compatibility assets derived from canonical Spec Kit instructions.
  - Preserve user custom content or report conflicts rather than silently overwriting customized Claude Code files.

3. **Instruction refresh and coexistence**
  - Extend instruction refresh to maintain Claude Code compatibility links/files while keeping `.specify/instructions.md` as the source of truth.
  - Ensure Copilot, Qwen Code, opencode, and Qoder assets remain unchanged unless their canonical shared source changes.

4. **Governance, docs, and release audit**
  - Update constitution and user-facing support surfaces to include Claude Code as officially approved.
  - Add release/blocking audits that verify docs, CLI help, templates, generated assets, and package resources all agree on Claude Code support.

### Planned Design Artifacts

- `data-model.md`: Defines `SupportedAssistant`, `ClaudeCodeAssetSet`, `ClaudeCodeCommandSurface`, `ClaudeCodeIgnorePolicy`, `AssistantRefreshRule`, and `SupportSurfaceAudit`.
- `contracts/claude-code-support.openapi.yaml`: Contract for listing assistants, initializing Claude Code projects, validating Claude Code availability, refreshing assets, and auditing support surfaces.
- `quickstart.md`: Validation walkthrough for new-project setup, existing-project refresh, missing CLI, ignore policy, command coverage, and release audit.
- `feature-ref.md`: Feature relationship review and notes for `/speckit.tasks`.

## Constitution Check (Post-Design Re-check)

- **Feature-Centric Development**: Pass. Feature 021 remains the sole primary feature; related features are integration dependencies only.
- **Specification-Driven Development**: Pass. Design artifacts trace to FR-001 through FR-011 and SC-001 through SC-005.
- **Intent-Driven Development**: Pass. The plan preserves user value and separates Claude Code compatibility from implementation mechanics.
- **Test-First & Contract-Driven**: Pass. The OpenAPI-style contract and quickstart scenarios define acceptance before task generation.
- **AI Agent Integration**: Pass for planning with release blocker. The implementation must update official governance to include Claude Code before the feature can be marked ready for review.
- **Continuous Quality & Observability**: Pass. Audit and validation surfaces are planned explicitly.
- **SDD Workflow Compliance**: Pass. Requirements, clarification, plan, research, data model, contract, and quickstart artifacts are present for task generation.

**Post-Design Gates Status**: ✅ All gates pass for planning; Claude Code governance update is a required implementation task and release blocker.

## Phase 2: Implementation Planning

1. Update governance and support surfaces so Claude Code is officially approved across `.specify/memory/constitution.md`, README, docs, templates, and CLI help.
2. Extend assistant metadata and CLI validation in `src/specify_cli/__init__.py` for Claude Code selection, missing-tool guidance, and `--ignore-agent-tools` behavior.
3. Generate Claude Code command assets from `templates/commands/*.md` into the chosen Claude Code command location with `$ARGUMENTS` handoff semantics.
4. Add `.claudeignore` and Claude Code-specific compatibility files while preserving `.specify/instructions.md` as the canonical source.
5. Extend instruction refresh scripts to create/update Claude Code compatibility surfaces without duplicating canonical content.
6. Add contract, integration, and unit tests for initialization, refresh, command coverage, ignore policy, governance, and release distribution.
7. Update Feature 021 memory and index after tasks/implementation outcomes are validated.
