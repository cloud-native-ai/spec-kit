# Implementation Plan: Add Instructions and Skills Commands

**Branch**: `1000-add-instr-skills-cmds` | **Date**: 2026-01-28 | **Spec**: [.specify/specs/1000-add-instr-skills-cmds/spec.md](spec.md)
**Input**: Specification from `.specify/specs/1000-add-instr-skills-cmds/spec.md`

## Summary

Implement two new Agent Commands, `/speckit.instructions` and `/speckit.skills`, by adding prompt templates to the `templates/commands/` directory. These commands will empower the Agent to generate and maintain critical onboarding documentation (`.ai/instructions.md`) and extensibility scaffolds (`.github/skills/`) while respecting existing content and project constitution.

## Technical Context

**Language/Version**: Python 3.8+ (CLI), Markdown (Prompts)
**Primary Dependencies**: None (Pure prompt engineering + CLI file generation)
**Storage**: File system (Markdown templates)
**Testing**: Manual validation (Agent interaction testing), CLI integration testing
**Target Platform**: VS Code Copilot / Generic Agent
**Project Type**: CLI Tool / Specification standard
**Performance Goals**: N/A
**Constraints**: Must work across different Operating Systems (path handling). Must be idempotent or safe-update.
**Scale/Scope**: 2 new command files.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Spec-Driven**: Spec flow is Spec -> Plan -> Task -> Implement (We are in Plan phase).
- **Agent-First**: The feature itself is about enhancing Agent capabilities. Artifacts are prompts.
- **Library/CLI-First**: Implemented as standard CLI command templates.
- **Test-First**: Requirements define clear Acceptance Criteria.
- **Context Preservation**: Updates document rationale in spec.

**Gates Status**: [✅ All gates pass]

## Project Structure

### Documentation (this spec)

```text
.specify/specs/1000-add-instr-skills-cmds/
├── plan.md              # This file
├── spec.md              # Feature specification
```

### New Components

```text
templates/commands/
├── instructions.md      # Template for /speckit.instructions
├── skills.md            # Template for /speckit.skills
```

## Phase 0: Research Review & Context

**Goal**: Validate that no Python code changes are required and prompt templates are sufficient.

1.  **Analyze `src/specify_cli/__init__.py`**: Confirmed `generate_commands` automatically scans `templates/commands/*.md`. Adding files is sufficient.
2.  **Analyze `scripts/bash/generate-copilot.sh`**: logic confirms `.ai/instructions.md` content structure.
3.  **Analyze `skills.md`**: logic confirms `SKILL.md` structure.

**Decision**: No `scripts/bash/` changes needed for runtime. Pure prompt implementation.

## Phase 1: Design & Contracts

**Goal**: Define the exact content of the prompt templates.

### Data Model Entitites (Prompt Structures)

#### 1. Instructions Command (`templates/commands/instructions.md`)
- **Frontmatter**:
  - `description`: Generate or update project instructions and compatibility symlinks.
  - `scripts`: (Optional) `check-prerequisites.sh` if needed.
- **Body**:
  - **Context Loading**: Read `README.md`, `.specify/memory/constitution.md`, `pyproject.toml`.
  - **Exist Check**: Check for `.ai/instructions.md`.
  - **Strategy**:
    - If missing: Create from scratch using standard sections (Goals, Tech Stack, Guidelines).
    - If exists: Rename to `.bak` and regenerate, merging `constitution.md` content into "Guidance".
  - **Symlinks**: Create relative symlinks in `.clinerules`, `.github`, `.lingma`, etc.

#### 2. Skills Command (`templates/commands/skills.md`)
- **Frontmatter**:
  - `description`: Create or update an Agent Skill.
- **Body**:
  - **Input Parsing**: `$ARGUMENTS` -> Skill Name + Description.
  - **Context Loading**: Read `.specify/memory/feature-index.md` + active specs (if applicable).
  - **Strategy**:
    - If directory missing: Create `.github/skills/<name>/SKILL.md`.
    - If exists: Append "### Spec Context Updates" section.
  - **Content**: Populate `SKILL.md` YAML frontmatter + Body instructions.

### API Contracts
- **CLI Interface**: Standard slash commands.
- **Output Artifacts**:
  - `.ai/instructions.md`
  - `.github/skills/<name>/SKILL.md`
  - Symlinks

### Agent Context Update
- Run agent update script (if standard procedure requires).

## Phase 2: Implementation Steps

1.  **Implement `templates/commands/instructions.md`**: Write the prompt template.
2.  **Implement `templates/commands/skills.md`**: Write the prompt template.
3.  **Verify**: Run `specify init` in a test directory to verify commands appear (manual test).
