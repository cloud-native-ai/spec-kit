# Data Model: SKILL_HOME / SKILL_WORKDIR Conventions

**Branch**: `012-skill-home-workdir` | **Date**: 2026-05-30 | **Plan**: [plan.md](plan.md)

This iteration is documentation-only — there is no persisted data, no API request/response model, no schema migration. The "data model" here describes the **first-class concepts** the updated `templates/commands/skills.md` defines and the **structural shape** of each affected document. These are the entities a contract test (and a human reader) will assert against.

## Entities

### 1. `SKILL_HOME` (named path variable)

| Field | Value |
|-------|-------|
| `name` | `SKILL_HOME` |
| `canonical_written_form` | `${SKILL_HOME}` |
| `meaning` | The Skill's real on-disk directory containing `SKILL.md`, after symlink resolution. |
| `script_resolution_recipe` | `${SKILL_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd -P)}` |
| `conceptual_resolution_recipe` | `dirname $(readlink -f SKILL.md)` (prose contexts only) |
| `invariants` | Absolute; post-symlink (physical); identical across compatibility entrypoints; agent-engine-independent. |
| `usage_rule` | Every Skill-owned resource reference (`scripts/`, `references/`, `assets/`, sub-directory files) is written as `${SKILL_HOME}/<relative-path>`. |
| `relationship_to_SKILL_WORKDIR` | Distinct concept: `SKILL_HOME` is where the Skill lives; `SKILL_WORKDIR` is where the user is. They are equal only by coincidence. |
| `relationship_to_SKILL_ROOT` | Supersedes. `SKILL_ROOT` references in in-scope Skill-authoring guidance are renamed to `SKILL_HOME`. |
| `requirements_traceability` | FR-001, FR-003, FR-004, FR-006, FR-007, FR-008, FR-013, FR-014, FR-016 |

### 2. `SKILL_WORKDIR` (named path variable)

| Field | Value |
|-------|-------|
| `name` | `SKILL_WORKDIR` |
| `canonical_written_form` | `${SKILL_WORKDIR}` |
| `meaning` | The runtime working directory of a Skill-invoked process — typically the user's project root. |
| `script_resolution_recipe` | `${SKILL_WORKDIR:-$(pwd -P)}` |
| `conceptual_resolution_recipe` | `bash -c 'pwd \|\| echo ${PWD}'` (prose contexts only) |
| `invariants` | Runtime-bound; absolute; symlink-resolved; equal to the directory the agent invoked the Skill from; stable across nested Skill calls. |
| `usage_rule` | Every user-facing path (inputs to read from the user's project, outputs to write into the user's project) is written as `${SKILL_WORKDIR}/<relative-path>`. |
| `relationship_to_SKILL_HOME` | Distinct concept (see above). |
| `requirements_traceability` | FR-002, FR-003, FR-005, FR-006, FR-007, FR-013, FR-016 |

### 3. `MigrationMappingEntry` (table row in the migration mapping)

| Field | Type | Description |
|-------|------|-------------|
| `legacy_pattern` | string | Pre-convention path idiom (e.g., `./scripts/init.sh`, `${SKILL_ROOT}/references/x.md`, `~/.copilot/skills/foo/assets/y.md`). |
| `new_pattern` | string | Equivalent `${SKILL_HOME}/...` form. |
| `example_before` | string | One concrete line of the legacy form, copy-pasteable. |
| `example_after` | string | The corresponding rewritten line. |
| `requirements_traceability` | constant | FR-011, SC-005 |

**Cardinality constraint**: ≥ 3 rows total — at minimum one each for bare relative paths, `SKILL_ROOT`, and agent-specific install paths embedded in prose.

### 4. `TemplateSection` (structural assertion target)

Each of the four edited documents must contain the named sections below. The contract test asserts presence by heading match.

| Document | Required Sections |
|----------|-------------------|
| `templates/commands/skills.md` | `Path Conventions`, `Computation Idioms`, `Paired Example`, `Migration Mapping`, `Non-shell Agents` |
| `skills/create-skills/SKILL.md` | Renamed `SKILL_ROOT` → `SKILL_HOME` (zero residual `SKILL_ROOT` occurrences); guidance to write new Skill resources as `${SKILL_HOME}/...` |
| `skills/improve-skills/SKILL.md` | A "Legacy path idioms" detection clause listing `./X`, `${SKILL_ROOT}/X`, agent-specific install paths as migration candidates |
| Mirrored `.specify/skills/<name>/SKILL.md` files | Byte-equivalent to their `skills/<name>/SKILL.md` counterparts |

## Cross-Entity Invariants

- **Variable distinctness**: `SKILL_HOME ≠ SKILL_WORKDIR` is a *contract*, not a coincidence. The Paired Example section in the template must demonstrate both used in the same script for different purposes.
- **Migration safety**: For every `MigrationMappingEntry`, applying the mapping to a legacy Skill must produce a behaviorally identical Skill (per FR-012). The mapping is mechanical, not semantic.
- **Mirror consistency**: For each edited `skills/<name>/SKILL.md`, the `.specify/skills/<name>/SKILL.md` mirror must be updated in the same commit. Drift between mirrors is a contract violation.
- **Scope containment**: No file outside the four-document edit set is modified by this iteration (verified by `git diff --name-only` review against the listed paths plus `tests/contract/test_skill_home_workdir_template.py`).
