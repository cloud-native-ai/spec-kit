# Data Model: Shared Reference Directory (Feature 029)

**Spec**: `028-sdd-workflow-refactor` | **Date**: 2026-07-14

This is a framework/packaging refactor; the "data model" is the set of build/install-time
entities and their relationships, not a runtime database schema.

## Entities

### 1. Shared Reference Directory

| Attribute | Value |
|-----------|-------|
| Source path | `shared/workflow/` |
| Installed path | `.specify/shared/workflow/` |
| Wheel mapping | `"shared" = "specify_cli/shared"` (force-include) |
| Install mechanism | `shutil.copytree(resource_path / "shared", .specify/shared, dirs_exist_ok=True)` |
| Retention | Listed in `_CORE_SPECIFY_ASSETS` as `.specify/shared` |
| Replaces | `skills/sdd-workflow/` (deleted) |

**Rule**: The `workflow/` subdirectory is a *family*; future shared families may be added as
siblings under `shared/` without changing the install/rewrite machinery.

### 2. Reference Document (×10)

The ten files relocated verbatim (content-preserving move). Exhaustive map:

| # | Old path (`skills/sdd-workflow/references/`) | New path (`shared/workflow/`) |
|---|-----------------------------------------------|-------------------------------|
| 1 | `user-input-protocol.md` | `user-input-protocol.md` |
| 2 | `feature-integration.md` | `feature-integration.md` |
| 3 | `agent-configuration.md` | `agent-configuration.md` |
| 4 | `checklist-methodology.md` | `checklist-methodology.md` |
| 5 | `requirements-guidelines.md` | `requirements-guidelines.md` |
| 6 | `dfx-catalog.md` | `dfx-catalog.md` |
| 7 | `clarify-taxonomy.md` | `clarify-taxonomy.md` |
| 8 | `ignore-patterns.md` | `ignore-patterns.md` |
| 9 | `tool-definitions.md` | `tool-definitions.md` |
| 10 | `feedback-step.md` | `feedback-step.md` |

**Validation**: Content of each new file MUST be byte-equivalent to its origin (0 lost, 0 altered).
`SKILL.md` and `references/` wrapper are NOT carried over (the skill wrapper is discarded).

### 3. Reference Link (two forms — no mixing)

| Form | Used in | Old value | New value |
|------|---------|-----------|-----------|
| Root-relative | command templates (`templates/commands/*.md`, `templates/skills-template.md`) | `skills/sdd-workflow/references/<f>.md` | `shared/workflow/<f>.md` |
| Installed absolute | sibling skills (`skills/*/SKILL.md`) | `.specify/skills/sdd-workflow/references/<f>.md` | `.specify/shared/workflow/<f>.md` |

The root-relative form is upgraded to `.specify/shared/workflow/...` at install time by the
Path-Rewrite Rule. Skills, which are not passed through `rewrite_paths()`, hard-code the
installed absolute form directly.

### 4. Path-Rewrite Rule

| Attribute | Value |
|-----------|-------|
| Location | `rewrite_paths()` in `src/specify_cli/__init__.py` (~L674) |
| New regex | `re.sub(r"(?<!\.specify/)shared/", r".specify/shared/", content)` |
| Guard | Negative lookbehind prevents double-prefixing (same pattern as `memory/`, `scripts/`, `templates/`) |
| Applied at | `generate_commands()` command-body rewrite (~L844) |

### 5. Core Asset Retention Entry

| Attribute | Value |
|-----------|-------|
| Location | `_CORE_SPECIFY_ASSETS` list (~L308) |
| New entry | `".specify/shared"` |
| Effect | `detect_initialized_core_assets` treats it as preserved; re-init does not overwrite |

### 6. Skill Registry Entry (to be removed)

| Attribute | Value |
|-----------|-------|
| Source | `skills/sdd-workflow/` directory (SKILL.md + references/) — DELETED |
| Registry | `sdd-workflow` row removed from the generated instructions Skills registry |
| Count | Skill count decremented by 1 ("20 total" → "19 total" in instructions/docs) |
| Discovery | `skills-utils.py` enumerates `*/SKILL.md`; deletion removes it automatically |
| Symlinks | Absent from `.specify/skills` → absent from every `<tool>/skills` symlink |

## Referring-File Inventory (source)

| Area | Count | Form | Action |
|------|-------|------|--------|
| `templates/commands/*.md` | 17 | root-relative | rewrite → `shared/workflow/...` |
| `templates/skills-template.md` | 1 | absolute | rewrite → `.specify/shared/workflow/...` |
| `skills/*/SKILL.md` (siblings) | 20 | absolute | rewrite → `.specify/shared/workflow/...` |
| `docs/` | 4 | prose | describe shared dir, not a skill; fix skill count |
| `.specify/` mirror | (regenerated) | — | regenerate; no hand-edit |

Excluded from all edits and from the zero-reference gate: `docs/summary/03-sdd-workflow-refactor-proposal.md`,
`.specify/specs/028-sdd-workflow-refactor/**`, `docs/history/**`.

## State Transitions

The refactor itself is a one-shot migration (no runtime state). The relevant lifecycle is the
Feature status: **Draft → Planned** (this command) → Implemented (`/speckit.implement`).
