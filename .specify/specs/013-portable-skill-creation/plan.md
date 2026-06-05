# Implementation Plan: Portable Skill Creation

**Branch**: `013-portable-skill-creation` | **Date**: 2026-06-05 | **Spec**: [requirements.md](./requirements.md)
**Input**: Specification from `.specify/specs/013-portable-skill-creation/requirements.md`

## Summary

Remove environment-specific tool-discovery logic from the skill creation pipeline so that skills created via `/speckit.skills` and `create-skills` are portable across different execution environments. The change touches four file families: the `create-skills` SKILL.md workflow (remove Step 3), the skill template (remove tool boilerplate), the orchestration template (remove tool-manifest modernization step), and the scaffolding script (remove `refresh_tools_for_target()` calls). Existing user-authored `tools/` directories are preserved; only automatic generation is removed.

## Technical Context

**Language/Version**: Python >=3.8 (runtime), Bash (scripts)  
**Primary Dependencies**: Typer, Rich, hatchling (build)  
**Storage**: N/A (file-based template/script changes)  
**Testing**: pytest with markers `contract` and `integration`  
**Target Platform**: Cross-platform (macOS, Linux)  
**Project Type**: Single project — CLI toolkit  
**Performance Goals**: N/A (template/script changes, no runtime performance impact)  
**Constraints**: Changes must be backward-compatible — existing skills with `tools/` directories must not lose content  
**Scale/Scope**: 4 primary files + 2 mirrors + 1 quality checklist + 1 script + contract tests

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Feature-Centric Development**: ✅ This plan is bound to Feature 013 (Skills Command). Feature Index already updated with this spec path.
- **Specification-Driven Development**: ✅ All changes trace directly to FR-001 through FR-011 in the requirements spec.
- **Intent-Driven Development**: ✅ The spec defines "what" (remove tool coupling) and "why" (environment portability). This plan addresses "how".
- **Test-First & Contract-Driven**: ✅ Contract tests will be written/updated before template and script changes. Existing test `test_create_skills_prompt_assets.py` will be updated to assert absence of tool-manifest references.
- **AI Agent Integration**: ✅ No agent-specific changes. The portability improvement benefits all supported agents equally.
- **Continuous Quality & Observability**: ✅ Changes are minimal and targeted. No speculative features added. YAGNI respected — we remove unused coupling rather than adding new abstractions.
- **SDD Workflow Compliance**: ✅ Following spec → plan → tasks → implement pipeline.

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/013-portable-skill-creation/
├── requirements.md      # Feature specification
├── plan.md              # This file
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
├── feature-ref.md       # Phase 1 output
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
# Files to modify
templates/
├── commands/
│   └── skills.md                    # Orchestration template (FR-005, FR-006)
└── skills-template.md               # Skill scaffolding template (FR-003, FR-004)

skills/
└── create-skills/
    ├── SKILL.md                     # Creation workflow (FR-001, FR-002)
    └── references/
        └── skill-creation-quality-checklist.md  # Validation checklist (FR-011)

scripts/
└── bash/
    └── create-new-skill.sh          # Scaffolding script (FR-007, FR-008)

# Mirror files to sync (FR-009)
.specify/skills/
└── create-skills/
    ├── SKILL.md                     # Mirror of skills/create-skills/SKILL.md
    └── references/
        └── skill-creation-quality-checklist.md  # Mirror of checklist

# Tests to add/update
tests/
└── contract/
    ├── test_create_skills_prompt_assets.py   # Update: assert no tool-manifest refs
    └── test_portable_skill_creation.py       # New: FR-specific contract tests
```

**Structure Decision**: Single project layout. All changes are edits to existing files or additions to the existing `tests/contract/` directory. No new directories or structural changes.

## Complexity Tracking

N/A

## Design Details

### Change 1: Remove Step 3 from `create-skills/SKILL.md` (FR-001, FR-002)

**Current state**: Step 3 ("Obtain available tools information") runs `scripts/bash/refresh-tools.sh --system --shell --project --json` and instructs the agent to reference tool manifest categories (`tools/system.json`, `tools/shell.json`, `tools/project.json`), then filter available tools against skill goals.

**Target state**: Remove Step 3 entirely. Renumber subsequent steps (Step 4 → Step 3, Step 5 → Step 4, etc.). Remove any remaining references to tool manifests in the Resource Directory Layout section. The `tools/` entry in the directory layout should be removed. The "Progressive Disclosure" step 3 mention of `tools/` should be updated to remove tool references.

**Files**: `skills/create-skills/SKILL.md`, `.specify/skills/create-skills/SKILL.md` (mirror sync)

### Change 2: Remove tool boilerplate from `templates/skills-template.md` (FR-003, FR-004)

**Current state**: The template includes an "Available Tools & Resources" section with a "Tools" subsection that references `${SKILL_HOME}/tools/` and `refresh-tools.sh`/`create-new-skill.sh` refresh commands.

**Target state**: Remove the entire "Tools" subsection under "Available Tools & Resources". Rename the parent section to "Resources" (since it now only covers scripts, references, and assets). Keep the scripts, references, and assets subsections intact.

**Files**: `templates/skills-template.md`

### Change 3: Update orchestration template (FR-005, FR-006)

**Current state**: `templates/commands/skills.md` has:
- Directory layout (line 68) showing `tools/` as a standard directory
- Step 6 in the Spec-Compliance Modernization Checklist requiring tool manifest regeneration via `create-new-skill.sh --refresh-only`
- Step 4 validation mentioning tool manifest refresh

**Target state**:
- Remove `tools/` from the directory layout example, or add a comment marking it as user-created only (not auto-generated)
- Remove Step 6 ("Tool manifests") from the modernization checklist. Renumber Step 7 → Step 6.
- Remove tool-manifest refresh from validation/report step mentions

**Files**: `templates/commands/skills.md`

### Change 4: Remove `refresh_tools_for_target()` calls from script (FR-007, FR-008)

**Current state**: `scripts/bash/create-new-skill.sh` defines `refresh_tools_for_target()` (lines 105-115) and calls it in three places:
- Line 332: `--refresh-only` mode with specific skill name
- Line 342: `--refresh-only` mode iterating all skills
- Line 379: When skill already exists (reuse path)
- Line 415: New skill creation path

**Target state**:
- Remove the `refresh_tools_for_target()` function definition
- Remove all four call sites
- `--refresh-only` continues to work for `skill_id` frontmatter refresh but no longer generates tool manifests
- Update the "refreshed" JSON message (line 353) to say "Skill metadata refreshed" instead of "Skill tools refreshed"

**Files**: `scripts/bash/create-new-skill.sh`

### Change 5: Update quality checklist (FR-011)

**Current state**: `skills/create-skills/references/skill-creation-quality-checklist.md` includes a "Resource Organization" section that mentions `tools/` as acceptable when containing generated tool manifests.

**Target state**: Remove the mention of `tools/` and generated tool manifests from the checklist. Keep the check for scripts, references, and assets being relevant.

**Files**: `skills/create-skills/references/skill-creation-quality-checklist.md`, `.specify/skills/create-skills/references/skill-creation-quality-checklist.md` (mirror sync)

### Change 6: Update `improve-skills/SKILL.md` tool-manifest references

**Current state**: `skills/improve-skills/SKILL.md` Step 6 (validation) mentions refreshing tool manifests with `create-new-skill.sh --refresh-only` and `refresh-tools.sh`, and discusses generated manifest validation churn.

**Target state**: Remove the tool-manifest refresh instruction from the validation step. Remove the paragraph about distinguishing generated manifests from instruction changes. Keep the rest of the validation step intact.

**Files**: `skills/improve-skills/SKILL.md`, `.specify/skills/improve-skills/SKILL.md` (mirror sync)

### Change 7: Contract tests

**New test file**: `tests/contract/test_portable_skill_creation.py`

Assertions covering:
- FR-001/FR-002: `skills/create-skills/SKILL.md` contains no "refresh-tools" or "tools/system.json" references
- FR-003: `templates/skills-template.md` contains no "Tools" subsection or tool-manifest refresh commands
- FR-005/FR-006: `templates/commands/skills.md` does not require tool manifests in modernization checklist
- FR-007: `scripts/bash/create-new-skill.sh` does not contain `refresh_tools_for_target` calls (function definition or invocations)
- FR-009: Mirror parity between `skills/create-skills/SKILL.md` and `.specify/skills/create-skills/SKILL.md`
- FR-011: Quality checklist does not reference tool manifests

**Existing test updates**: `tests/contract/test_create_skills_prompt_assets.py`
- Update `test_create_skills_uses_relative_resource_paths` to remove `./tools/` from the expected patterns list (line 206)

### Edge Case: Existing `tools/` Directories (FR-010)

The `create_skill_structure()` function in `scripts/bash/common.sh` already does NOT create `tools/`. It only creates `scripts/`, `references/`, and `assets/`. The `tools/` directory was only created by `refresh_tools_for_target()`. By removing `refresh_tools_for_target()` calls, we automatically stop creating `tools/` without affecting existing ones. No explicit migration or deletion logic is needed.

## Implementation Order

1. **Tests first** (TDD): Write `test_portable_skill_creation.py` — tests will fail initially
2. **Script change**: Remove `refresh_tools_for_target()` from `create-new-skill.sh`
3. **Template changes**: Update `skills-template.md` and `templates/commands/skills.md`
4. **Skill changes**: Update `create-skills/SKILL.md` and `improve-skills/SKILL.md`
5. **Checklist update**: Update quality checklist
6. **Mirror sync**: Copy updated files to `.specify/skills/` mirrors
7. **Existing test update**: Update `test_create_skills_prompt_assets.py`
8. **Validation**: Run full test suite, verify all contract tests pass
