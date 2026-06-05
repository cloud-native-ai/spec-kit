# Data Model: Portable Skill Creation

**Spec**: [requirements.md](./requirements.md) | **Plan**: [plan.md](./plan.md)

## Overview

This change is a template/script refactoring with no new data entities. The data model documents the existing entities being modified and their relationships.

## Entities

### Skill Directory

The on-disk structure of a Spec Kit skill.

| Attribute | Description |
|-----------|-------------|
| `SKILL.md` | Required. The skill definition file with frontmatter and workflow body |
| `scripts/` | Optional. Executable scripts owned by the skill |
| `references/` | Optional. Reference documentation loaded on demand |
| `assets/` | Optional. Static assets for outputs (templates, images) |
| ~~`tools/`~~ | **Removed from auto-generation**. Was: auto-generated tool manifests. Now: user-created only |

### Skill Template (`templates/skills-template.md`)

The boilerplate used by `create-new-skill.sh` to scaffold new `SKILL.md` files.

| Section | Status |
|---------|--------|
| Frontmatter (name, description, skill_id) | Unchanged |
| Overview | Unchanged |
| Workflow / Instructions | Unchanged |
| Resource ID | Unchanged |
| Path Conventions | Unchanged |
| Resources (scripts, references, assets) | Unchanged (renamed from "Available Tools & Resources") |
| ~~Tools subsection~~ | **Removed** |

### Create-Skills Workflow (`skills/create-skills/SKILL.md`)

The skill that implements skill creation logic.

| Step | Status |
|------|--------|
| 1. Determine creation source | Unchanged |
| 2. Determine SKILL_HOME and metadata | Unchanged |
| ~~3. Obtain available tools information~~ | **Removed** |
| 3. Structure the Skill (was 4) | Updated — no `tools/` in directory layout |
| 4. Incrementally clarify details (was 5) | Renumbered |
| 5. Register the Skill (was 6) | Renumbered |
| 6. Validate the Skill (was 7) | Renumbered |
| 7. Report completion (was 8) | Renumbered |

### Scaffolding Script (`scripts/bash/create-new-skill.sh`)

| Function/Call | Status |
|---------------|--------|
| `refresh_tools_for_target()` definition | **Removed** |
| Calls in `--refresh-only` mode | **Removed** (skill_id refresh preserved) |
| Calls in existing-skill path | **Removed** |
| Call in new-skill creation path | **Removed** |

## Relationships

```
templates/skills-template.md
  └── used by → scripts/bash/create-new-skill.sh (template expansion)
                  └── produces → .specify/skills/<name>/SKILL.md

templates/commands/skills.md
  └── orchestrates → skills/create-skills/SKILL.md (new skill)
  └── orchestrates → skills/improve-skills/SKILL.md (existing skill)

skills/create-skills/SKILL.md
  └── mirrors → .specify/skills/create-skills/SKILL.md
  └── references → skills/create-skills/references/skill-creation-quality-checklist.md
```

## State Transitions

No state transitions — this is a static content change to templates, scripts, and skill definitions.
