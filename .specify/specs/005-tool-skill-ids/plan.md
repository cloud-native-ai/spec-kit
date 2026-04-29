# Implementation Plan: Deterministic Tool and Skill IDs

**Branch**: `005-tool-skill-ids` | **Date**: 2026-03-10 | **Spec**: [.specify/specs/005-tool-skill-ids/requirements.md](.specify/specs/005-tool-skill-ids/requirements.md)
**Input**: Specification from `.specify/specs/005-tool-skill-ids/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[CN] `/speckit.tools` [CN] `/speckit.skills` [CN] canonical ID[CN] ID[CN] tool/skill [CN]

## Technical Context

**Language/Version**: Python 3.11+[CN] Python >=3.8  
**Primary Dependencies**: Typer[CN]Rich[CN] Bash [CN]Markdown [CN]  
**Storage**: [CN]`.specify/memory/tools/`[CN]`.github/skills/` [CN]  
**Testing**: pytest + [CN] contract/integration/unit [CN]  
**Target Platform**: Linux [CN] CLI/AI Agent [CN]
**Project Type**: single[CN]CLI + templates + scripts + tests[CN]  
**Performance Goals**: 95% [CN] ID [CN] ID [CN] 2 [CN]  
**Constraints**: [CN] ID [CN] tool/skill [CN]  
**Scale/Scope**: [CN] tool/skill [CN]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Feature-Centric Development**: [CN] Feature 013[CN] feature[CN] plan [CN]
- **Specification-Driven Development**: [CN] FR-001~FR-012 [CN] SC-001~SC-005[CN]
- **Intent-Driven Development**: [CN]“[CN]”[CN]
- **Test-First & Contract-Driven**: [CN] ID [CN]/[CN]
- **AI Agent Integration**: [CN] GitHub Copilot / Qwen Code / opencode [CN] provider[CN]
- **Continuous Quality & Observability**: [CN] ID [CN]
- **SDD Workflow Compliance**: [CN] spec → plan [CN] `/speckit.tasks`[CN]

**Additional Constraints from Input**:

- [CN]“[CN]”[CN] tool [CN] skill [CN]
- [CN]File path[CN] canonical [CN]
- [CN]

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/005-tool-skill-ids/
├── plan.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── deterministic-resource-ids.openapi.yaml
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
templates/
├── commands/
│   ├── skills.md
│   └── tools.md
├── tool-mcp-call-template.md
├── tool-project-script-template.md
├── tool-shell-function-template.md
└── tool-system-binary-template.md

scripts/
├── bash/
│   ├── create-new-skill.sh
│   ├── create-new-tools.sh
│   └── refresh-tools.sh
└── python/
  ├── list_mcp_tools.py
  ├── list_project_tools.py
  ├── list_shell_tools.py
  └── list_system_tools.py

.github/
└── skills/
  └── <skill-name>/
    ├── SKILL.md
    └── tools/

.specify/
├── memory/
│   └── tools/
│       └── <tool-name>.md
└── specs/
  └── 005-tool-skill-ids/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: [CN] CLI/[CN]/[CN] `templates/commands/`[CN]`scripts/bash/`[CN] Python/[CN] `.specify/memory/tools/` [CN] `.github/skills/` [CN]

## Complexity Tracking

N/A

## Phase 0: Research Review & Context

- `research.md` [CN] `README.md`[CN][docs/usage.md](docs/usage.md)[CN][docs/quickstart.md](docs/quickstart.md)[CN][docs/speckit/spec-driven.md](docs/speckit/spec-driven.md)[CN][docs/skills/problems.md](docs/skills/problems.md)[CN]Feature Index [CN] feature [CN]
- [CN] Python CLI + Bash [CN] + Markdown [CN]
- [CN] Feature[CN] Feature[CN] Feature 013[CN] Feature 016[CN]
- [CN]canonical ID [CN]

## Phase 1: Design & Contracts

### Design Decisions

1. **Canonical ID [CN]**
  - Tool [CN] `tool_id`[CN]
  - Skill [CN] skill [CN] `SKILL.md` [CN] `skill_id`[CN]“skill [CN]”[CN]
  - [CN] canonical [CN]

2. **[CN]**
  - `/speckit.tools` [CN] ID [CN]
  - `/speckit.skills` [CN] `SKILL.md` frontmatter [CN] ID [CN]
  - [CN]

3. **[CN]**
  - [CN] ID [CN] ID [CN]
  - [CN] ID [CN] ID [CN]/[CN]
  - [CN] ID [CN]

4. **[CN]**
  - [CN]
  - [CN] `/speckit.tools` [CN] `/speckit.skills` [CN]

### Data Model

- [CN] `.specify/specs/005-tool-skill-ids/data-model.md`[CN] `ResourceId`[CN]`ToolArtifact`[CN]`SkillArtifact`[CN]`ResolutionRequest`[CN]`ResolutionResult` [CN]

### Contracts

- [CN] `.specify/specs/005-tool-skill-ids/contracts/deterministic-resource-ids.openapi.yaml`[CN]
- [CN]“[CN] ID”“[CN] ID [CN]”“[CN]/[CN]”[CN] tasks [CN]

### Quickstart

- [CN] `.specify/specs/005-tool-skill-ids/quickstart.md`[CN] tool [CN]skill [CN]ID [CN]

## Constitution Check (Post-Design Re-check)

- **Feature-Centric Development**: [CN] Feature 013[CN] feature[CN]
- **Specification-Driven Development**: [CN] requirements [CN] FR/SC [CN]
- **Intent-Driven Development**: [CN]“[CN]”[CN]
- **Test-First & Contract-Driven**: [CN] OpenAPI [CN] contract/integration tests[CN]
- **AI Agent Integration**: [CN] provider [CN]
- **Continuous Quality & Observability**: [CN]
- **SDD Workflow Compliance**: plan [CN] `/speckit.tasks`[CN]

**Post-Design Gates Status**: ✅ All gates pass

## Phase 2: Implementation Planning

1. [CN] `templates/commands/tools.md`[CN]/[CN] ToolRecord [CN] canonical `tool_id`[CN]
2. [CN] `templates/commands/skills.md`[CN]/[CN] skill [CN] canonical `skill_id`[CN]
3. [CN] `create-new-tools.sh` [CN] `create-new-skill.sh` [CN] JSON [CN] ID[CN]
4. [CN] tool [CN] skill [CN] ID [CN]/[CN]
5. [CN] ID[CN]
6. [CN] contract/integration/unit [CN]
