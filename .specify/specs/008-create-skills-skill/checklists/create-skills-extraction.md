# Extraction Responsibility Checklist: Create Skills Skill

**Purpose**: Track coverage of creation responsibilities moved from `templates/commands/skills.md` into `skills/create-skills/SKILL.md`
**Created**: 2026-05-10
**Feature**: 013 / Skills Command

## Creation Responsibilities Coverage

### Input Parsing & Classification

- [x] Explicit user input parsing (name + description extraction)
- [x] Empty-argument conversation distillation
- [x] Target Skill name validation rules
- [x] Ambiguity handling and one-question-at-a-time clarification

### Skill Structure & Frontmatter

- [x] YAML frontmatter requirements (`name`, `description`)
- [x] SKILL.md body structure (Goal, Workflow, references)
- [x] Resource directory layout (`tools/`, `scripts/`, `references/`, `assets/`)

### Progressive Disclosure & Sizing

- [x] Progressive disclosure guidance (keep SKILL.md < 500 lines)
- [x] When to split details into `references/`
- [x] Relative resource path conventions (`./scripts/`, `./references/`)

### Quality & Anti-Patterns

- [x] Vague description checks
- [x] Invalid Skill name prevention
- [x] Oversized SKILL.md prevention
- [x] Missing executable step checks
- [x] Inconsistent resource path detection

### Registry & Discoverability

- [x] `skill_id` generation and persistence
- [x] `.specify/instructions.md` Skills registry update
- [x] Deduplication and sorting rules

### Completion Reporting

- [x] Path reporting (SKILL.md location, skill_id)
- [x] Example prompts
- [x] Suggested follow-up customizations

### Coverage Summary

- **Total creation responsibilities**: 20
- **Covered in skills/create-skills/SKILL.md**: 20
- **Coverage percentage**: 100%
- **Target**: ≥ 90% (SC-003)