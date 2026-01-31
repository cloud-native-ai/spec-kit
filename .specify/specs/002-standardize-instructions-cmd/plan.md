# Implementation Plan: Standardize Instructions Command

**Branch**: `002-standardize-instructions-cmd` | **Date**: 2026-01-31 | **Spec**: [spec.md](spec.md)
**Input**: Specification from `.specify/specs/002-standardize-instructions-cmd/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The `instructions` command will be refactored to align with the standard `speckit` architecture. This involves:
1. Defining the command in `templates/commands/instructions.md` with proper schema.
2. Standardizing the project instructions content into a customizable template at `templates/instructions-template.md`.
3. Updating the logic script `scripts/bash/generate-instructions.sh` to support "Smart Fusion" (merging existing user content with the new template framework) and safe variable substitution.

## Technical Context

**Language/Version**: Bash (primary logic), Python 3.11+ (CLI interface via Speckit)
**Primary Dependencies**: `typer`, `rich` (Project core), `sed`/`awk`/`grep` (Bash processing)
**Storage**: File system (`.ai/instructions.md`, `.clinerules/`)
**Testing**: Manual verification, Bash unit testing (if applicable)
**Target Platform**: Linux/macOS (Bash environment)
**Project Type**: CLI Tool / Helper Script
**Performance Goals**: N/A (interactive command)
**Constraints**: Must run in standard Bash environment without heavy external dependencies.
**Scale/Scope**: Single command refactoring.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Spec-Driven**: Spec defines requirements for fusion behavior.
- **Agent-First**: Plan creates artifacts for AI context consistency.
- **Library/CLI-First**: Implements a CLI command.
- **Test-First**: Edge cases defined in spec will be tested.
- **Context Preservation**: Feature tracks changes to instructions generation.

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/002-standardize-instructions-cmd/
├── plan.md              # This file
├── data-model.md        # Template variables & Command Schema
├── quickstart.md        # Usage guide
├── contracts/           # Command definition
│   └── instructions.md  # The command contract
├── feature-ref.md       # (Optional)
└── tasks.md             # (To be generated)
```

### Source Code

```text
templates/
├── instructions-template.md       # New: The standard template
└── commands/
    └── instructions.md            # Updated: Command definition

scripts/bash/
└── generate-instructions.sh       # Updated: Logic implementation
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
