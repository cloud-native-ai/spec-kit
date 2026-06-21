# Implementation Plan: CLI Priority AI Tool Support

**Branch**: `018-cli-priority-support` | **Date**: 2026-06-21 | **Spec**: [requirements.md](requirements.md)
**Input**: Specification from `.specify/specs/018-cli-priority-support/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This spec establishes a tiered AI tool support model within Spec Kit: five CLI tools (Claude Code, Codex CLI, Qoder CLI, GitHub Copilot, opencode) are designated Tier 1 with deepest integration, while Qwen Code is Tier 2 with standard support. The primary technical work involves: (1) onboarding Codex CLI as a new officially supported tool with full initialization, command template, and documentation coverage; (2) introducing a `tier` field into the assistant profile system and surfacing it in documentation menus, CLI help, and initialization result summaries; (3) generating tool-specific command template variants for all five Tier 1 tools; (4) syncing the constitution's Principle V to include Codex CLI and the tier classification; (5) maintaining a capability matrix auditing 6 support dimensions across all tools. The implementation extends the existing `AGENT_CONFIG`, `_OFFICIAL_ASSISTANT_KEYS`, and assistant profile infrastructure introduced by Feature 022.

## Technical Context

**Language/Version**: Python 3.8+ (per `pyproject.toml` `requires-python = ">=3.8"`)
**Primary Dependencies**: `typer` (CLI framework), `rich` (TTY rendering), `httpx[socks]` (HTTP), `platformdirs`, `readchar`, `truststore` (Python ≥ 3.10)
**Storage**: Filesystem (`.specify/` directory structure, `.codex/`, `.claude/`, `.qoder/`, `.copilot/`, `.opencode/` tool directories)
**Testing**: `pytest` with markers `contract` and `integration` (per `pyproject.toml` → `[tool.pytest.ini_options]`)
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows; terminal-based)
**Project Type**: Single CLI application (`src/specify_cli/` single-module package)
**Performance Goals**: Init completes in <5 min including first `/speckit.*` command availability (SC-001); capability matrix audit completes in <10s per tool
**Constraints**: Must preserve existing `.specify` core content on re-init (Feature 022 preservation rules); must not break existing tool configurations when adding Codex CLI; idempotent re-init behavior
**Scale/Scope**: 6 AI tools (5 Tier 1 + 1 Tier 2); ~15 command templates per tool; ~20 test files expected across contract/integration/unit layers

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

<!--
  ACTION REQUIRED for /speckit.plan:
  Do NOT hard-code principle names here. Instead, read `.specify/memory/constitution.md`,
  enumerate every heading matching `### <roman-or-arabic-numeral>. <name>` (e.g.
  `### I. Template-First Architecture`, `### IV. Test-First Development`), and render
  ONE row in the table below per principle in the exact order they appear in the
  constitution. Include the principle's NON-NEGOTIABLE / MANDATORY annotation verbatim
  when present. This avoids the drift documented in the constitution's Sync Impact Report.

  Each row must contain:
  - Principle (verbatim heading without the leading `### N.`)
  - Compliance ("✅ Pass" / "❌ Fail" / "⚠ Partial — see Complexity Tracking")
  - Evidence (one-line citation pointing at the design artefact that demonstrates compliance)
-->

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | All 17 FRs trace to requirements.md; plan maps each FR to design artifacts in data-model.md and contracts/ |
| II | Feature-Centric Development | ✅ Pass | Spec bound to Feature 022 (AI Tools Support) in feature-index.md; key changes to be recorded in features/022.md |
| III | Intent-Driven Development | ✅ Pass | Requirements focus on what (tool coverage, tier classification) and why (maximize CLI tool capabilities), not how |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Plan includes contract tests for assistant profiles, tier classification, capability matrix audit; TDD ordering in tasks (tests before impl) |
| V | AI Agent Integration Standards | ⚠ Partial — see Complexity Tracking | Current constitution lists 5 official agents without Codex CLI; FR-016 amends Principle V to add Codex CLI and tier classification. Pre-amendment state is a temporary violation with explicit remediation. |
| VI | Continuous Quality & Observability | ✅ Pass | Capability matrix audit provides observability; structured logging via InitializationResultSummary; version tracking for tool adaptation |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Following SDD workflow: requirements → clarify → plan (this document) → tasks → implement |

**Gates Status**: ⚠ One partial gate — Principle V (AI Agent Integration Standards) is currently non-compliant because Codex CLI is not yet in the constitution's official agent list. This is an expected pre-amendment state; FR-016 explicitly resolves it by amending Principle V. See Complexity Tracking row CT-001.

**Re-check after Phase 1**: 2026-06-21 — Post-design re-check confirms Principle V remains ⚠ Partial until implementation executes the constitution amendment (FR-016). All other principles pass against design artifacts (data-model.md, contracts/).

## Project Structure

### Documentation (this spec)

```text
.specify/specs/018-cli-priority-support/
├── requirements.md     # /speckit.requirements output
├── checklists/         # /speckit.requirements quality checklist
│   └── requirements.md
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── cli-priority-support.openapi.yaml
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.log     # Implementation output (/speckit.implement command)
```

No standalone research.md — Phase 0 findings inlined below. All context was resolvable from internal investigation (project docs, constitution, existing source code).

### Source Code (repository root)

```text
src/specify_cli/__init__.py  # Main CLI module: AGENT_CONFIG, assistant profiles, init command, command generation
templates/commands/          # Command template source files (15 .md files, shared across tools)
templates/instructions-template.md  # Instructions generation template (needs codex variant)
templates/constitution-template.md  # Constitution template (needs Principle V update for codex + tiers)
scripts/bash/update-agent-context.sh  # Agent context script (already has partial codex support)
tests/contract/             # Contract tests: assistant profiles, support surfaces, tier classification
tests/integration/          # Integration tests: init, command coverage, multi-tool coexistence
tests/unit/                 # Unit tests: support matrix, tier helpers, profile resolution
docs/                       # User-facing docs: README, quickstart, usage, installation
.specify/memory/constitution.md  # Constitution (needs Principle V amendment)
.specify/memory/features/022.md  # Feature detail for AI Tools Support (needs key changes update)
.specify/memory/features.md      # Feature index (Spec Path → 018-cli-priority-support/requirements.md)
```

**Structure Decision**: Extends existing single-module CLI application (`src/specify_cli/__init__.py`) by adding `codex` to `AGENT_CONFIG`, `_OFFICIAL_ASSISTANT_KEYS`, `_ASSISTANT_COMMAND_DIRS`, `_ASSISTANT_EXTENSIONS`, `_ASSISTANT_ARG_FORMATS`, and introducing a `_ASSISTANT_TIERS` mapping. No new top-level directories; `.codex/commands/` is created dynamically per-project during `specify init`. Test files follow existing naming conventions (`test_codex_init_contract.py`, `test_codex_support_surfaces.py`, `test_tier_classification.py`, etc.).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle V lists only 5 official agents; Codex CLI not yet included (CT-001) | FR-016 requires formal onboarding of Codex CLI; the constitution must reflect the actual supported tool set to maintain governance consistency | Simply adding Codex CLI to code without updating the constitution would create a governance gap where the source of truth disagrees with the implementation |

## Phase 0: Research Review & Context

### Information Gathering

**Project Architecture**: Spec Kit is a Python CLI tool (`specify-cli`) built with Typer/Rich. The core module `src/specify_cli/__init__.py` (~1.8k LOC) contains all CLI commands. The assistant system is driven by:

1. `AGENT_CONFIG` dict — maps tool keys to metadata (name, folder, install_url, requires_cli)
2. `_OFFICIAL_ASSISTANT_KEYS` list — canonical list of officially supported tools
3. `_ASSISTANT_COMMAND_DIRS` — maps tools to command output directories
4. `_ASSISTANT_EXTENSIONS` — file extensions per tool
5. `_ASSISTANT_ARG_FORMATS` — argument format placeholders per tool
6. `_SKILLS_SYMLINK_ASSISTANTS` — set of tools needing skills symlinks

**Current State**: 5 tools are registered (claude, copilot, qwen, opencode, qoder). Codex CLI has partial support in `update-agent-context.sh` (line 580: `codex)` case) and in the `init` command (lines 1797-1807: CODEX_HOME setup step), but is NOT in `AGENT_CONFIG` or `_OFFICIAL_ASSISTANT_KEYS`. This means selecting Codex CLI in `specify init` fails with "Invalid AI assistant".

**Feature 022 Foundation**: Multi-tool coexistence, core asset preservation (`exist_ok=True`), `InitializationResultSummary`, support-surface audit infrastructure, and 17 test files are already in place. Tier 1/Tier 2 is a new layer on top of this.

**No standalone research.md** — all findings are from internal investigation of source code, constitution, and existing test patterns.

### Technical Decisions

1. **Codex CLI entry in AGENT_CONFIG**: Add `"codex"` key with `folder: ".codex/"`, `install_url: "https://..."`, `requires_cli: True`. This follows the exact same pattern as Claude Code and Qoder CLI.

2. **Codex CLI command directory**: `.codex/commands/` (confirmed during `/speckit.clarify`). Add to `_ASSISTANT_COMMAND_DIRS`.
3. **Codex CLI command extension**: `.md` (Markdown format, same as Claude/Qoder/opencode). Add to `_ASSISTANT_EXTENSIONS`.
4. **Codex CLI arg format**: `$ARGUMENTS` (consistent with Claude, Copilot, opencode, Qoder). Add to `_ASSISTANT_ARG_FORMATS`.
5. **Tier classification**: Introduce a new `_ASSISTANT_TIERS` dict mapping tool keys to `"tier1"` or `"tier2"`. Surface in `get_assistant_profile()` as `profile["tier"]`. This is additive and backward-compatible — existing callers that don't check `tier` are unaffected.
6. **Constitution amendment**: Principle V will be updated to list 6 tools (adding Codex CLI) and include tier classification as a sub-bullet. Version bump: PATCH (semantic clarification) or MINOR (new guidance). Recommended: MINOR per constitution amendment procedure.

## Phase 1: Design & Contracts

### Design Overview

The implementation centers on three data structure changes and their downstream effects:

**A. Codex CLI Onboarding (P1, MVP)**
- Add `codex` to: `AGENT_CONFIG`, `_OFFICIAL_ASSISTANT_KEYS`, `_ASSISTANT_COMMAND_DIRS`, `_ASSISTANT_EXTENSIONS`, `_ASSISTANT_ARG_FORMATS`, `_SKILLS_SYMLINK_ASSISTANTS`
- The existing `generate_commands()` function (line 477) already handles arbitrary agents — it reads `templates/commands/*.md` and writes per-extension files. No change needed to the generation logic itself, only to the config dicts that feed it.
- The `init` command already has Codex-specific setup steps (CODEX_HOME, lines 1797-1807) — but only triggers them when `selected_ai == "codex"`, which currently fails before reaching that code because `"codex"` is not in `AGENT_CONFIG`. Adding it to `AGENT_CONFIG` unblocks this existing code path.

**B. Tier Classification (P2)**
- New dict: `_ASSISTANT_TIERS = {"claude": "tier1", "codex": "tier1", "qoder": "tier1", "copilot": "tier1", "opencode": "tier1", "qwen": "tier2"}`
- Updated `get_assistant_profile()` returns `profile["tier"]`
- `--ai` help text updated to reflect tier ordering
- `select_with_arrows()` menu shows Tier 1 tools first (ordered list in `_OFFICIAL_ASSISTANT_KEYS` already controls display order — reorder to put Tier 1 first)
- Documentation (README, installation, quickstart, usage) lists Tier 1 tools first with tier label

**C. Deep Capability Adaptation (P3)**
- Command template variants: The existing `generate_commands()` already produces per-tool variants using `_ASSISTANT_ARG_FORMATS`. For Tier 1 tools, the content quality of command templates is identical (same source templates). "Deep adaptation" means: (1) all 15 commands are generated for each Tier 1 tool (verified by audit), (2) CLI installation verification runs for all Tier 1 tools with `requires_cli: True`, (3) environment variable guidance appears in init summary, (4) skills symlinks established.
- Capability matrix: New function `audit_capability_matrix(project_path)` returns per-tool, per-dimension pass/fail. 6 dimensions: `initialization`, `command_templates`, `instructions`, `ignore_config`, `skills_symlink`, `refresh_protection`.
