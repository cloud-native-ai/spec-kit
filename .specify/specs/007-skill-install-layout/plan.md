# Implementation Plan: Skill Install Layout

**Branch**: `007-skill-install-layout` | **Date**: 2026-04-21 | **Spec**: [.specify/specs/007-skill-install-layout/requirements.md](.specify/specs/007-skill-install-layout/requirements.md)
**Input**: Specification from `.specify/specs/007-skill-install-layout/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[CN] skills [CN] `.specify/skills/`[CN] `.github/skills/` [CN]“[CN]”[CN]“[CN] + [CN]/[CN]”[CN] `.github/skills/<name>` [CN]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Bash + Python 3.11+[CN] Python >=3.8  
**Primary Dependencies**: Typer[CN]Rich[CN] `scripts/bash/*.sh` [CN] `scripts/python/skills-utils.py` [CN]  
**Storage**: [CN]`.specify/skills/` [CN]  
**Testing**: pytest[CN]`tests/contracts`[CN]`tests/integration`[CN]`tests/unit`[CN]+ [CN]  
**Target Platform**: Linux/macOS/Windows [CN]
**Project Type**: single[CN]CLI + templates + scripts + tests[CN]  
**Performance Goals**: [CN] skill [CN]/[CN]  
**Constraints**: `.specify/skills/` [CN]  
**Scale/Scope**: [CN] skills [CN]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Feature-Centric Development**: [CN] Feature 013[CN]Skills Command[CN] Feature[CN]  
- **Specification-Driven Development**: [CN] FR-001~FR-016 [CN] SC-001~SC-005[CN]  
- **Intent-Driven Development**: [CN]“[CN]”[CN]  
- **Test-First & Contract-Driven**: [CN]/[CN]  
- **AI Agent Integration**: [CN]Copilot/Qwen/opencode/Qoder[CN]  
- **Continuous Quality & Observability**: [CN]  
- **SDD Workflow Compliance**: [CN] plan + data model + contracts + quickstart[CN] `/speckit.tasks`[CN]

**Additional Constraints from Input**:

- [CN] `.github/skills/` [CN] `.specify/skills/` [CN]  
- [CN]“[CN]”[CN]/[CN]  
- [CN]“[CN] + [CN]”[CN]  
- [CN]

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/007-skill-install-layout/
├── plan.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── skill-install-layout.openapi.yaml
├── checklists/
│   └── requirements.md
└── tasks.md
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
  └── __init__.py

scripts/
├── bash/
│   └── create-new-skill.sh
└── python/
  └── skills-utils.py

.specify/
├── scripts/
│   ├── bash/
│   │   └── create-new-skill.sh
│   └── python/
│       └── skills-utils.py
└── skills/
  └── <skill-name>/
      ├── SKILL.md
      └── ...

.github/
└── skills/
  └── <skill-name> -> compatibility entry to .specify/skills/<skill-name>

tests/
├── contracts/
├── integration/
└── unit/
```

**Structure Decision**: [CN] `create-new-skill` [CN] `skills-utils` [CN]/[CN]“[CN]”[CN]“.specify [CN] + [CN]”[CN]

## Complexity Tracking

N/A

## Phase 0: Research Review & Context

- [CN] `research.md`[CN] `requirements.md`[CN]`.specify/memory/constitution.md`[CN]`README.md`[CN]`docs/*.md`[CN]`.specify/memory/features.md` [CN] `.specify/memory/features/*.md` [CN]  
- [CN] Feature 013 [CN] Feature[CN]/[CN] Feature[CN]  
- [CN]
  - `/speckit.*` [CN]
  - [CN]
  - [CN] feature [CN]  
- [CN]

## Phase 1: Design & Contracts

### Design Decisions

1. **[CN]**
  - [CN] skill [CN] `.specify/skills/<skill-name>/`[CN]
  - [CN] `.github/skills/<skill-name>`[CN]

2. **[CN]**
  - [CN]
  - [CN] skill [CN]
  - [CN]“[CN]”[CN]

3. **[CN]**
  - [CN] `.github/skills/<skill-name>` [CN]
  - [CN]“[CN]”[CN]
  - [CN]/[CN]/[CN]

4. **[CN]**
  - [CN]/[CN] skill [CN] + [CN]
  - [CN]/[CN]

### Data Model

- [CN] `.specify/specs/007-skill-install-layout/data-model.md`[CN] `SkillPrimaryCopy`[CN]`CompatibilityEntryPoint`[CN]`ToolSupportProfile`[CN]`MigrationSession`[CN]`BackupArtifact`[CN]`InstallOutcome` [CN]

### Contracts

- [CN] `.specify/specs/007-skill-install-layout/contracts/skill-install-layout.openapi.yaml`[CN]
- [CN]

### Quickstart

- [CN] `.specify/specs/007-skill-install-layout/quickstart.md`[CN]

## Constitution Check (Post-Design Re-check)

- **Feature-Centric Development**: [CN] Feature 013[CN]/[CN]/[CN] Feature[CN]  
- **Specification-Driven Development**: [CN] FR-001~FR-016 [CN]  
- **Intent-Driven Development**: [CN]“[CN] + [CN]”[CN]  
- **Test-First & Contract-Driven**: [CN]  
- **AI Agent Integration**: [CN] provider[CN]  
- **Continuous Quality & Observability**: [CN]  
- **SDD Workflow Compliance**: plan [CN] `/speckit.tasks` [CN]

**Post-Design Gates Status**: ✅ All gates pass

## Phase 2: Implementation Planning

1. [CN] `scripts/bash/create-new-skill.sh` [CN] `.specify/scripts/bash/create-new-skill.sh`[CN] `.specify/skills`[CN]  
2. [CN] `scripts/python/skills-utils.py` [CN] `.specify/scripts/python/skills-utils.py`[CN]skill [CN] `.specify/skills/*/SKILL.md`[CN]  
3. [CN] `.specify/skills` [CN] `.github/skills` [CN]  
4. [CN] `.github/skills` [CN]  
5. [CN]/[CN]/[CN]/[CN]/[CN] contract[CN]integration[CN]unit [CN] Feature 013 [CN]
