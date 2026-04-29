# Implementation Plan: Add Qoder Support

**Branch**: `006-add-qoder-support` | **Date**: 2026-03-29 | **Spec**: [.specify/specs/006-add-qoder-support/requirements.md](.specify/specs/006-add-qoder-support/requirements.md)
**Input**: Specification from `.specify/specs/006-add-qoder-support/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[CN] Spec Kit [CN] Qoder [CN] `specify init`[CN] `tmp/patches/qoder-main/` [CN] Feature [CN]“[CN]/[CN]”[CN]

## Technical Context

**Language/Version**: Python >=3.8[CN] Python 3.11+  
**Primary Dependencies**: Typer[CN]Rich[CN]httpx[socks][CN]readchar[CN] Bash [CN] Markdown [CN]  
**Storage**: [CN]`.specify/`[CN]`.github/`[CN]`.qoder/` [CN]  
**Testing**: pytest[CN]`tests/contract`[CN]`tests/integration`[CN]`tests/unit`[CN]+ [CN]/[CN]  
**Target Platform**: Linux/macOS/Windows [CN] CLI [CN] Linux [CN]
**Project Type**: single[CN] Python CLI + [CN] + [CN] + [CN]  
**Performance Goals**: [CN] Qoder [CN] Qoder [CN]/[CN]/[CN]  
**Constraints**: [CN] Copilot/Qwen/opencode [CN]Qoder [CN] `--ignore-agent-tools`[CN] Qoder [CN]  
**Scale/Scope**: [CN] 1 [CN] CLI [CN]1 [CN]/[CN]/[CN]/[CN] Feature 020 [CN]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Feature-Centric Development**: [CN] Feature 020[CN] Feature[CN] Feature 008[CN]015[CN]017[CN]019 [CN]
- **Specification-Driven Development**: [CN] FR-001~FR-013 [CN] SC-001~SC-005[CN] patch [CN]
- **Intent-Driven Development**: [CN]“Qoder [CN]”[CN] CLI[CN]
- **Test-First & Contract-Driven**: [CN]/[CN]/[CN]/[CN] tasks/implement [CN]
- **AI Agent Integration**: [CN] Qoder[CN] feature [CN]
- **Continuous Quality & Observability**: [CN]README[CN]
- **SDD Workflow Compliance**: [CN] requirements [CN] checklist[CN] plan [CN] feature [CN]

**Additional Constraints from Specification Context**:

- [CN] `tmp/patches/qoder-main/` [CN]
- [CN]Qoder [CN]
- [CN] FR-012 [CN]

**Gates Status**: ✅ All gates pass[CN]/[CN]/[CN]

## Project Structure

### Documentation (this spec)

```text
.specify/specs/006-add-qoder-support/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── qoder-support.openapi.yaml
├── feature-ref.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── specify_cli/
  └── __init__.py

templates/
├── plan-template.md
├── instructions-template.md
└── commands/
  ├── agents.md
  ├── instructions.md
  └── *.md

scripts/
└── bash/
  ├── generate-instructions.sh
  └── *.sh

docs/
├── installation.md
├── quickstart.md
├── usage.md
├── upstream.md
├── skills/
└── speckit/

.specify/
├── memory/
│   ├── constitution.md
│   ├── features.md
│   └── features/020.md
└── specs/
  └── 006-add-qoder-support/

tmp/
└── patches/
  └── qoder-main/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: [CN] CLI [CN] `src/specify_cli/__init__.py` [CN]`templates/` [CN]/[CN]`scripts/bash/generate-instructions.sh` [CN]`docs/` [CN]`.specify/memory/` [CN]

## Complexity Tracking

N/A

## Phase 0: Research Review & Context

- [CN] spec [CN] `research.md`[CN] `README.md`[CN]`docs/**`[CN]`.specify/memory/features.md`[CN]`.specify/memory/features/*.md`[CN]`.specify/memory/constitution.md` [CN] `tmp/patches/qoder-main/` [CN]
- [CN] `src/specify_cli/__init__.py` [CN] Python CLI[CN] `AGENT_CONFIG`[CN]`copy_local_templates()` [CN] `generate_commands()` [CN]
- [CN] `.qoder/project_rules.md` [CN]CLI [CN] Qoder[CN]
- [CN]CLI [CN] `qoder`[CN] `https://qoder.com/cli`[CN] `.qoder/commands/`[CN] Markdown[CN] `$ARGUMENTS`[CN]
- Feature [CN]/[CN]/[CN] Feature[CN] Feature 020[CN] Feature 008[CN]Instructions[CN]015[CN]CLI Interface[CN]017[CN]Template Engine[CN]019[CN]Agents Command[CN]
- [CN] `/speckit.research`[CN]

**Phase 0 Output**: [CN] `research.md`[CN]

## Phase 1: Design & Contracts

### Design Decisions

1. **[CN]**
   - [CN] `AGENT_CONFIG` [CN] `qoder` [CN]
   - Qoder [CN] Qwen/opencode [CN] CLI [CN] CLI [CN] `--ignore-agent-tools` [CN]

2. **Qoder [CN]**
   - [CN]Qoder [CN]`.qoder/commands/*` [CN]`.qoder/project_rules.md` [CN]/[CN]
   - [CN]“[CN]/[CN] Qoder [CN]”[CN]

3. **[CN]**
   - [CN]README[CN] Qoder[CN]
   - [CN] CLI [CN]/[CN]/[CN] FR-012/FR-013[CN]

4. **[CN]**
   - [CN]“[CN]”“[CN]”“[CN]”[CN] tasks/implement [CN]
   - [CN] CLI [CN] wheel/[CN]

### Planned Design Artifacts

- `data-model.md`: [CN] `SupportedAssistant`[CN]`AssistantAssetSet`[CN]`AssistantValidationRule`[CN]`SupportSurface`[CN]`DistributionVariant` [CN]
- `contracts/qoder-support.openapi.yaml`: [CN] OpenAPI [CN]
- `quickstart.md`: [CN] CLI[CN]
- `feature-ref.md`: [CN] Feature 020 [CN] Feature/[CN] `/speckit.tasks` [CN]

## Constitution Check (Post-Design Re-check)

- **Feature-Centric Development**: [CN] Feature 020[CN] Feature [CN]
- **Specification-Driven Development**: [CN]
- **Intent-Driven Development**: [CN]“[CN] Qoder [CN]”[CN]
- **Test-First & Contract-Driven**: [CN]OpenAPI [CN]/[CN]
- **AI Agent Integration**: [CN] feature [CN]“[CN]”[CN]
- **Continuous Quality & Observability**: [CN]/[CN]/[CN]
- **SDD Workflow Compliance**: plan [CN] `/speckit.tasks`[CN]

**Post-Design Gates Status**: ✅ All gates pass

## Phase 2: Implementation Planning

1. [CN] `.specify/memory/constitution.md`[CN] Qoder [CN]
2. [CN] `src/specify_cli/__init__.py` [CN] `AGENT_CONFIG`[CN]`--ai` [CN]CLI [CN] `check()` [CN] Qoder [CN] CLI [CN]
3. [CN] Qoder [CN] `.qoder/project_rules.md` [CN]
4. [CN] `templates/commands/*.md`[CN]`templates/plan-template.md`[CN]`templates/instructions-template.md` [CN]
5. [CN] `README.md`[CN]`docs/installation.md`[CN]`docs/usage.md` [CN]
6. [CN]/[CN] CLI [CN] Qoder[CN]
7. [CN]CLI [CN] contract/integration/unit [CN]
8. [CN] Feature 020 [CN] Feature Memory [CN]
