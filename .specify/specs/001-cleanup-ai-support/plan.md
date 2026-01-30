# Implementation Plan: Cleanup Legacy AI Tools Support

**Branch**: `001-cleanup-ai-support` | **Date**: 2026-01-30 | **Spec**: [.specify/specs/001-cleanup-ai-support/spec.md](../spec.md)
**Input**: Specification from `.specify/specs/001-cleanup-ai-support/spec.md`

## Summary

This plan covers the removal of all legacy AI tool integrations from the Spec Kit CLI, retaining only **GitHub Copilot**, **Qwen Code**, and **opencode**. This involves stripping implementation code, configuration logic, and templates for unsupported tools, and updating documentation to reflect the new independent evolution state.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Typer (CLI), Rich (UI), httpx (Network)
**Storage**: N/A (CLI tool, file-based)
**Testing**: pytest
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: CLI Tool
**Constraints**: strictly limit support to the 3 specified tools.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Spec-Driven**: ✅ Started with spec 001.
- **Agent-First**: ✅ Documentation and templates are agent-friendly.
- **Library/CLI-First**: ✅ Modifying existing CLI.
- **Test-First**: ✅ Tests will be updated/added for supported providers.
- **Context Preservation**: ✅ Feature index and changelogs will be updated.

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/001-cleanup-ai-support/
├── plan.md              # This file
├── data-model.md        # Phase 1 output (Config schema)
├── quickstart.md        # Phase 1 output (Updated usage)
└── feature-ref.md       # Phase 1 output
```

### Source Code (repository root)

```text
src/
└── specify_cli/
    └── __init__.py      # Main CLI entry point to refactor

templates/
└── commands/            # Templates to prune
    ├── analyze.md       # Generic template (keep)
    ├── specify.md       # Generic template (keep)
    ├── ...              # Other generic templates (keep)
    └── [agent-specific] # Remove unsupported agent templates (if separate)

docs/                    # Documentation to update
```

## Phase 1: Design & Contracts

### Data Model Changes

The `AGENT_CONFIG` dictionary in `src/specify_cli/__init__.py` will be reduced to:

```python
AGENT_CONFIG = {
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github/",
        "install_url": None,
        "requires_cli": False,
    },
    "qwen": {
        "name": "Qwen Code",
        "folder": ".qwen/",
        "install_url": "https://github.com/QwenLM/qwen-code",
        "requires_cli": True,
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode/",
        "install_url": "https://opencode.ai",
        "requires_cli": True,
    },
}
```

### Template Cleanup Strategy

Scan `src/specify_cli/__init__.py`'s `generate_commands` function to identify hardcoded logic for removed agents. Provide logic only for the 3 supported agents.

Verify which templates in `templates/commands` are generic vs agent-specific. The current implementation uses generic templates (e.g. `specify.md`) and injects agent-specific logic via `generate_commands`. We need to ensure `generate_commands` doesn't support other keys.

## Phase 2: Implementation Tasks

See `/speckit.tasks` output.
