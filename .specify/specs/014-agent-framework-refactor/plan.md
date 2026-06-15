# Implementation Plan: Agent Framework Refactor

**Branch**: `014-agent-framework-refactor` | **Date**: 2026-06-15 | **Spec**: [requirements.md](requirements.md)
**Input**: Specification from `.specify/specs/014-agent-framework-refactor/requirements.md`

## Summary

Refactor the Spec Kit agent system to use `.specify/agents/` as the canonical agent directory (paralleling `.specify/skills/`), with directory-level symlinks for tool-specific discovery, bundled agent installation during `specify init`, and a shared `references/` subdirectory for cross-agent materials. The primary changes span: (1) the `/speckit.agents` command template, (2) the CLI init flow in `__init__.py`, (3) the package's `agents/` directory with pre-built agents, and (4) packaging configuration.

## Technical Context

**Language/Version**: Python >=3.8 (per `pyproject.toml`)
**Primary Dependencies**: `typer` (CLI), `rich` (rendering), `shutil` / `os` / `pathlib` (filesystem ops)
**Storage**: Filesystem — `.agent.md` files, directories, symlinks
**Testing**: `pytest` with `contract` and `integration` markers
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows — note: symlinks on Windows require elevated permissions or developer mode)
**Project Type**: Single CLI package (`src/specify_cli/`)
**Performance Goals**: File I/O operations; sub-second for agent creation, <5s for init with agents
**Constraints**: Must preserve backward compatibility with existing `.github/agents/` layouts; must not break existing skills symlink behavior
**Scale/Scope**: ~5 supported AI tools, ~3-5 bundled agents initially, unlimited user-created agents

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Feature-Centric Development**: ✅ Bound to Feature 019 (Agents Command). Feature index updated. This spec extends the existing feature, not a new one.
- **Specification-Driven Development**: ✅ Implementation directly traces to the 12 functional requirements in `requirements.md`. Every code change maps to a specific FR.
- **Intent-Driven Development**: ✅ Spec defines "what" (canonical directory, symlinks, init bundling, shared references) and "why" (tool discoverability, no content duplication). "How" is determined here in planning.
- **Test-First & Contract-Driven**: ✅ Plan includes contract tests for symlink behavior, integration tests for init flow, and unit tests for the generalized symlink helper.
- **AI Agent Integration**: ✅ Only approved agents are supported: Claude Code, GitHub Copilot, Qwen Code, opencode, Qoder. Tool-specific directory mapping is explicit.
- **Continuous Quality & Observability**: ✅ No speculative features. Changes follow YAGNI. Structured progress tracking via `StepTracker`.
- **SDD Workflow Compliance**: ✅ Following spec → plan → tasks → implement workflow.

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/014-agent-framework-refactor/
├── requirements.md      # Feature specification
├── plan.md              # This file
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── agents-directory.yaml
└── checklists/
    └── requirements.md  # Quality checklist
```

### Source Code (repository root)

```text
src/specify_cli/
└── __init__.py          # CLI implementation (~1.8k LOC)
                         # - Modify: ensure_agent_symlink() (new, generalized from ensure_agent_skills_symlink)
                         # - Modify: copy_local_templates() — add agents copy + symlink block
                         # - Modify: _CORE_SPECIFY_ASSETS — add ".specify/agents"

agents/                  # Pre-built agents (new, bundled in wheel)
├── .gitkeep
├── references/          # Shared reference materials
│   └── coding-standards.md
└── code-reviewer.agent.md  # Example bundled agent

templates/
├── agent-common-template.md      # Existing — no changes needed
├── agent-knowledge-template.md   # Existing — no changes needed
├── agent-plan-template.md        # Existing — no changes needed
├── agent-research-template.md    # Existing — no changes needed
└── commands/
    └── agents.md                 # Modify: update target from .github/agents/ to .specify/agents/

tests/
├── contract/
│   └── test_agents_symlink.py   # New: contract tests for agent symlink behavior
├── integration/
│   └── test_init_agents.py      # New: integration tests for init with agents
└── unit/
    └── test_ensure_symlink.py   # New: unit tests for generalized symlink helper

pyproject.toml           # Modify: add "agents" to force-include
```

**Structure Decision**: Single-project structure. All changes are within the existing `src/specify_cli/__init__.py` module and surrounding packaging/template files. No new modules needed — the symlink helper is a function within `__init__.py`, consistent with the existing `ensure_agent_skills_symlink` pattern.

## Complexity Tracking

N/A — no Constitution violations.

## Design Decisions

### D1: Generalize `ensure_agent_skills_symlink` into a reusable function

The existing `ensure_agent_skills_symlink` is a nested function inside `copy_local_templates` that handles `.specify/skills` symlinks. Rather than duplicating it for agents, extract it into a module-level function `ensure_specify_symlink(root_path, agent_dir_name, specify_subdir)` that works for both skills and agents.

**Parameters**:
- `root_path: Path` — project root
- `agent_dir_name: str` — tool directory prefix (e.g., `.github`, `.qoder`)
- `specify_subdir: str` — subdirectory name under `.specify/` and the tool directory (e.g., `"skills"` or `"agents"`)

This replaces `ensure_agent_skills_symlink` calls with `ensure_specify_symlink(project_path, ".github", "skills")` and adds `ensure_specify_symlink(project_path, ".github", "agents")`.

### D2: Agent directory symlink mapping

Each tool gets a directory-level symlink:

| Tool | Symlink Path | Target |
|------|-------------|--------|
| Claude Code | `.github/agents/` | → `.specify/agents/` |
| VS Code Copilot | `.github/agents/` | → `.specify/agents/` |
| Qoder | `.qoder/agents/` | → `.specify/agents/` |
| Qwen | `.qwen/agents/` | → `.specify/agents/` |
| opencode | `.opencode/agents/` | → `.specify/agents/` |

Note: Claude Code and Copilot both share `.github/agents/` — same symlink serves both. The `.claude/agents/` path is not needed since Claude Code reads from `.github/agents/`.

### D3: `/speckit.agents` command template update

The `templates/commands/agents.md` template currently targets `.github/agents/<name>.agent.md` directly. Update it to:
1. Target `.specify/agents/<name>.agent.md` as the canonical write location
2. Generate workspace files (AGENTS.md, MEMORY.md, SOUL.md, USER.md) on first run
3. Place reference materials in `.specify/agents/references/`
4. Trigger symlink creation after agent write (via instruction in the command template, since `/speckit.agents` is a prompt, not code)

### D4: Init flow additions

In `copy_local_templates()`, after the existing skills block:
1. Copy `agents/` from package resource to `.specify/agents/` (same as skills copy)
2. For each supported tool, call `ensure_specify_symlink(project_path, tool_dir, "agents")`

### D5: Workspace files purpose

| File | Purpose |
|------|---------|
| `AGENTS.md` | Index of all agents in the project — names, descriptions, invocation hints |
| `MEMORY.md` | Persistent context shared across agent invocations (project conventions, past decisions) |
| `SOUL.md` | Project identity and principles that all agents should internalize |
| `USER.md` | Current user context, preferences, and working style for agent personalization |

These are created by the `/speckit.agents` command template (prompt-time), not by the CLI init code. The CLI only copies bundled agents.

### D6: Package data inclusion

Add to `pyproject.toml` `[tool.hatch.build.targets.wheel.force-include]`:
```
"agents" = "specify_cli/agents"
```

### D7: Core assets update

Add `".specify/agents"` to `_CORE_SPECIFY_ASSETS` list so existing agent directories are preserved during re-initialization.
