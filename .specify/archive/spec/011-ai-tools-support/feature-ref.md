# Feature Reference: AI Tools Support

## Primary Feature

- **Feature ID**: 022
- **Feature Name**: AI Tools Support
- **Status entering plan**: Planned → **Implemented**
- **Specification**: `.specify/specs/011-ai-tools-support/requirements.md`
- **Plan**: `.specify/specs/011-ai-tools-support/plan.md`
- **Implementation Date**: 2026-05-19

## Implementation Summary

### Key Changes

1. **Central assistant support profile** (`src/specify_cli/__init__.py`):
   - Added `InitializationResultSummary` class with created/reused/skipped/preserved/conflict/attention_required categories.
   - Added `get_assistant_profile()`, `get_official_assistants()`, `core_asset_relpaths()`, `is_core_asset_initialized()`, `detect_initialized_core_assets()`, `detect_configured_assistants()`, `compute_command_coverage()`, and related helpers.
   - Added `_ASSISTANT_COMMAND_DIRS`, `_ASSISTANT_EXTENSIONS`, `_ASSISTANT_ARG_FORMATS` mappings for all 5 assistants.
   - Added `_SKILLS_SYMLINK_ASSISTANTS` to cover Qwen and opencode skill symlinks.

2. **Core preservation** (`src/specify_cli/__init__.py`):
   - `copy_local_templates()` now uses `mkdir(parents=True, exist_ok=True)` for idempotent directory creation.
   - Memory files (constitution.md, features.md) are skipped when they already exist.
   - Existing `.specify` core assets are preserved across assistant additions.

3. **Skills symlinks for Qwen Code and opencode**:
   - Qwen (`--ai qwen`) now creates `.qwen/skills → .specify/skills` symlink.
   - opencode (`--ai opencode`) now creates `.opencode/skills → .specify/skills` symlink.

4. **Documentation updates**:
   - `docs/quickstart.md`: Updated to show all 5 assistant options.
   - `docs/usage.md`: Added maintenance workflows for GitHub Copilot, Qwen Code, and opencode.

5. **Tests** (across 17 test files):
   - Unit tests: `test_ai_tools_support_matrix.py`, `test_initialization_result_summary.py`, `test_core_workspace_asset_preservation.py`, `test_ai_tools_cli_help.py`.
   - Integration tests: `test_ai_tools_init_all_assistants.py`, `test_ai_tools_command_coverage.py`, `test_ai_tools_distribution.py`, `test_ai_tools_core_preservation.py`, `test_ai_tools_instruction_preservation.py`, `test_ai_tools_partial_core_repair.py`, `test_ai_tools_custom_asset_conflicts.py`, `test_ai_tools_repeat_run_idempotence.py`, `test_ai_tools_multi_assistant_coexistence.py`, `test_ai_tools_refresh_isolation.py`, `test_ai_tools_validation_summary.py`, `test_ai_tools_quickstart.py`.
   - Contract tests: `test_ai_tools_support_contract.py`, `test_ai_tools_support_surfaces.py`, `test_specify_script_paths.py`.
   - Fixtures: `tests/fixtures/ai_tools_support.py`.

### Feature Relationship Review (Post-Implementation)

- Feature 020 (Qoder Support) and Feature 021 (Claude Code Support) remain intact as historical implementation slices.
- Feature 022 generalizes the cross-assistant initialization and coexistence patterns from Features 020/021.
- No merge/split/deprecation required.

## Feature Relationship Review

### Reused / related features

- **Feature 020 — Qoder Support**: Provides a proven pattern for assistant metadata, command generation, docs, package resources, and tests for one CLI assistant.
- **Feature 021 — Claude Code Support**: Provides a recent pattern for adding one assistant while preserving existing assistant integrations and generating assistant-specific command/ignore assets.
- **Feature 008 — Instructions Command**: Owns generated instruction compatibility surfaces and must remain the source for instruction refresh behavior.
- **Feature 015 — CLI Interface**: Owns CLI initialization, option handling, help text, and user-facing setup flow.
- **Feature 017 — Template Engine**: Owns canonical command/template assets used by assistant-specific generators.
- **Feature 019 — Agents Command**: Establishes custom agent/provider governance boundaries that support-surface audits should not contradict.
- **Feature 013 — Skills Command**: Provides the canonical `.specify/skills/` and compatibility-link model that this feature should preserve.

### No merge / split / deprecation required

This plan does not replace Qoder or Claude Code support. It generalizes cross-assistant initialization and coexistence while keeping assistant-specific features as historical implementation slices and references.

## Notes for `/speckit.tasks`

- Tasks should start with regression tests for assistant matrix parity, core asset preservation, and generated command coverage.
- Existing-project safety is a first-class story, not a polish task.
- Script path helper regression should be included because `/speckit.plan` exposed a `.specify/scripts/bash/common.sh` mismatch during this planning run.
- Documentation, CLI help, package resources, and tests must be audited together to avoid support-surface drift.
- Feature 022 should remain the primary feature for this implementation slice.
