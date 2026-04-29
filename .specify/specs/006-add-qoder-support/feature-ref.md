# Feature References: Add Qoder Support

## Primary Feature

### Feature 020 — Qoder Support

- **Role in this plan**: The sole primary Feature for this requirement.
- **Why primary**: [CN]“[CN] Qoder [CN]”[CN]
- **Plan impact**: Must simultaneously cover initialization, refresh, validation, documentation, distribution, and governance consistency.

## Related Existing Features

### Feature 008 — Instructions Command

- **Relationship**: Qoder [CN]
- **Shared assets**:
  - `scripts/bash/generate-instructions.sh`
  - `templates/instructions-template.md`
  - `.ai/instructions.md`

### Feature 015 — CLI Interface

- **Relationship**: `specify init --ai qoder`[CN] `check()` [CN] CLI [CN]
- **Shared assets**:
  - `src/specify_cli/__init__.py`

### Feature 017 — Template Engine

- **Relationship**: Qoder [CN]
- **Shared assets**:
  - `templates/commands/*.md`
  - `generate_commands()` [CN]

### Feature 019 — Agents Command

- **Relationship**: [CN]Qoder [CN]
- **Shared assets**:
  - `templates/commands/agents.md`
  - `templates/plan-template.md`

## Feature Review Outcome

- **New feature required?** No
- **Feature merge/split required?** No
- **Feature deprecation required?** No
- **Feature classification change required?** No

## Notes for `/speckit.tasks`

1. [CN]/[CN]
2. [CN] CLI [CN]
3. [CN] FR-012/FR-013 [CN]