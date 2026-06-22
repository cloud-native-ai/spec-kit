# Implementation Plan: Tier 2 Agent Support for Hermes-Agent and iFlow

**Branch**: `019-tier2-hermes-iflow` | **Date**: 2026-06-22 | **Spec**: [requirements.md](requirements.md)
**Input**: Specification from `.specify/specs/019-tier2-hermes-iflow/requirements.md`

## Summary

Add Hermes-Agent and iFlow as two new Tier 2 (standard support) AI agents to Spec Kit. This extends the official tool count from 6 to 8, expanding Tier 2 from 1 tool (Qwen Code) to 3 tools. The implementation follows the established assistant onboarding pattern: add entries to all assistant config dicts, add init-flow branches for command generation and symlinks, update the constitution, docs, CLI help text, and add tests. Both new tools use `.hermes/commands/` and `.iflow/commands/` with `md` extension and `$ARGUMENTS` format — matching the majority convention.

## Technical Context

**Language/Version**: Python >=3.8 (per `pyproject.toml`)  
**Primary Dependencies**: `typer` (CLI framework), `rich` (TTY rendering), `shutil` / `pathlib` (file ops)  
**Storage**: Filesystem only (config directories, symlinks, markdown templates)  
**Testing**: `pytest` with markers `contract` and `integration`  
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)  
**Project Type**: Single Python package (`src/specify_cli/`)  
**Performance Goals**: N/A — CLI init operations, no latency sensitivity  
**Constraints**: Must maintain backwards compatibility with existing 6-tool installations; zero disruption to Tier 1 tools  
**Scale/Scope**: 2 new tool entries across ~8 config dicts, ~2 init-flow branches, documentation and constitution updates, test coverage additions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Spec 019 requirements.md drives all implementation; plan traces to FRs |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 022; feature index and detail file updated |
| III | Intent-Driven Development | ✅ Pass | Spec defines WHAT (2 new Tier 2 tools) and WHY (user-requested expansion) before HOW |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Plan includes test tasks before implementation; contracts defined in `contracts/` |
| V | AI Agent Integration Standards | ✅ Pass | Adds hermes-agent and iFlow to official support list; updates Principle V itself; tier classification applied |
| VI | Continuous Quality & Observability | ✅ Pass | Existing test suite extended; semantic versioning maintained; docs updated |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Following full SDD workflow: requirements → clarify → plan → tasks → implement |

**Gates Status**: ✅ All gates pass

**Re-check after Phase 1**: 2026-06-22 — All principles remain Pass after data-model, contracts, and quickstart generation. No new violations introduced.

## Phase 0: Research Review

No standalone research.md — findings inlined below.

**Existing Pattern Analysis**: The codebase uses a centralized assistant configuration model. Adding a new tool requires entries in 8 dictionaries/sets (`AGENT_CONFIG`, `_OFFICIAL_ASSISTANT_KEYS`, `_ASSISTANT_COMMAND_DIRS`, `_ASSISTANT_EXTENSIONS`, `_ASSISTANT_ARG_FORMATS`, `_SKILLS_SYMLINK_ASSISTANTS`, `_ASSISTANT_TIERS`, `_INSTRUCTIONS_FILE_MAP`) plus init-flow branches in `copy_local_templates()` for command generation, skills symlinks, and agents symlinks. The Codex CLI onboarding (Spec 018) is the most recent precedent and confirms this pattern. No architectural changes needed — this is strictly additive.

**Key Technical Decisions**:
- Hermes-Agent key: `"hermes"` (short form, consistent with `"claude"`, `"codex"`, `"qwen"` pattern)
- iFlow key: `"iflow"` (lowercase, consistent with `"opencode"` pattern)
- Both use `.hermes/` and `.iflow/` config dirs, `commands/` subdirectory, `md` extension, `$ARGUMENTS` format
- Instructions files: `HERMES.md` and `IFLOW.md` as symlinks to `.specify/instructions.md`
- No ignore file (`.hermesignore` / `.iflowignore`) needed — only Claude and Codex have ignore files currently; Tier 2 tools follow the Qwen pattern (no ignore file)
- `requires_cli: True` for both — they are CLI-based agents
- Install URLs: TBD — will use placeholder URLs until official URLs confirmed

## Project Structure

### Documentation (this spec)

```text
.specify/specs/019-tier2-hermes-iflow/
├── plan.md              # This file
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
├── checklists/          # Quality checklist
└── requirements.md      # Feature specification
```

### Source Code (repository root)

```text
src/specify_cli/__init__.py   # Config dicts, init flow, CLI args — all changes in single file
tests/contract/               # New: tier2 contract tests for hermes + iflow
tests/integration/            # New: init tests for hermes + iflow
tests/unit/                   # Updates: assistant count assertions
.specify/memory/constitution.md  # Principle V amendment
README.md                     # Tier 2 section update
docs/quickstart.md            # Tool list update
docs/installation.md          # Tool list update
```

**Structure Decision**: Extends the existing single-module CLI (`src/specify_cli/__init__.py`) by adding 2 new tool entries to existing config dictionaries and 2 new init-flow branches. No new top-level directories. Test additions follow established file naming patterns.

## Complexity Tracking

N/A — no constitution violations.

## Detailed Design

### Config Dict Changes (src/specify_cli/__init__.py)

All changes are additive entries in existing dictionaries. No structural changes.

**AGENT_CONFIG** — add 2 entries:
```
"hermes": {"name": "Hermes Agent", "folder": ".hermes/", "install_url": TBD, "requires_cli": True}
"iflow": {"name": "iFlow", "folder": ".iflow/", "install_url": TBD, "requires_cli": True}
```

**_OFFICIAL_ASSISTANT_KEYS** — append `"hermes"`, `"iflow"` after `"qwen"` (Tier 2 section):
```
["claude", "codex", "qoder", "copilot", "opencode", "qwen", "hermes", "iflow"]
```

**_ASSISTANT_COMMAND_DIRS**:
```
"hermes": ".hermes/commands"
"iflow": ".iflow/commands"
```

**_ASSISTANT_EXTENSIONS**:
```
"hermes": "md"
"iflow": "md"
```

**_ASSISTANT_ARG_FORMATS**:
```
"hermes": "$ARGUMENTS"
"iflow": "$ARGUMENTS"
```

**_SKILLS_SYMLINK_ASSISTANTS** — add `"hermes"`, `"iflow"` to the set.

**_ASSISTANT_TIERS**:
```
"hermes": "tier2"
"iflow": "tier2"
```

**_INSTRUCTIONS_FILE_MAP**:
```
"hermes": "HERMES.md"
"iflow": "IFLOW.md"
```

### Init Flow Changes (copy_local_templates)

Add 2 `elif` branches following the existing pattern (after `codex` branch, before `else` fallback):

1. `elif ai_assistant == "hermes"`: call `generate_commands("hermes", "md", "$ARGUMENTS", project_path / ".hermes" / "commands", script_type)`
2. `elif ai_assistant == "iflow"`: call `generate_commands("iflow", "md", "$ARGUMENTS", project_path / ".iflow" / "commands", script_type)`

Add skills symlink blocks:
1. `if ai_assistant == "hermes"`: `ensure_specify_symlink(project_path, ".hermes", "skills")`
2. `if ai_assistant == "iflow"`: `ensure_specify_symlink(project_path, ".iflow", "skills")`

Add agents symlink blocks:
1. `if ai_assistant == "hermes"`: `ensure_specify_symlink(project_path, ".hermes", "agents")`
2. `if ai_assistant == "iflow"`: `ensure_specify_symlink(project_path, ".iflow", "agents")`

### CLI Help Text Update

Update `--ai` option help string in `init()` command:
```
help="AI assistant to use: claude, codex, qoder, copilot, opencode (Tier 1), or qwen, hermes, iflow (Tier 2)"
```

### Constitution Amendment

Update Principle V in `.specify/memory/constitution.md`:
- Add Hermes Agent and iFlow to official agent list
- Update Tier 2 line to: `Tier 2 (standard support) — Qwen Code, Hermes Agent, iFlow`
- Bump version to 1.2.0 (MINOR — expanded Principle V scope)

### Documentation Updates

- **README.md**: Add Hermes Agent and iFlow under "Tier 2 (Standard Support)" section
- **docs/quickstart.md**: Update tool list references
- **docs/installation.md**: Update tool list references
- **CLAUDE.md / instructions.md**: Will be regenerated by `/speckit.instructions` after implementation

### Test Coverage Plan

**Contract tests** (new files):
- `test_hermes_init_contract.py`: Verify AGENT_CONFIG entry, profile fields, tier classification
- `test_iflow_init_contract.py`: Verify AGENT_CONFIG entry, profile fields, tier classification

**Integration tests** (new files):
- `test_hermes_init.py`: End-to-end init with `--ai hermes`, verify directory creation, command templates, symlinks
- `test_iflow_init.py`: End-to-end init with `--ai iflow`, verify directory creation, command templates, symlinks

**Existing test updates**:
- `test_ai_tools_support_contract.py`: Update assistant count from 6 to 8
- `test_ai_tools_init_all_assistants.py`: Add hermes and iflow to all-assistant init loop
- `test_tier_ordering_contract.py`: Verify hermes and iflow appear after Tier 1 tools
- `test_capability_matrix_contract.py`: Verify hermes and iflow are included in audit
- `test_ai_tools_multi_assistant_coexistence.py`: Add hermes/iflow to coexistence tests
