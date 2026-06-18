# Feature Reference: 017-consolidate-draft-skills

**Feature ID**: 013  
**Feature Name**: Skills Command  
**Spec Branch**: `017-consolidate-draft-skills`

## Feature Binding

This specification is bound to Feature 013 (Skills Command), which manages extensible skills and tools in Spec Kit. This spec adds a new iteration to consolidate 9 draft skills into 3 formal skills.

## Related Specifications Under Feature 013

| Spec | Status | Focus |
|------|--------|-------|
| 005-tool-skill-ids | Completed | Deterministic tool/skill ID generation |
| 007-skill-install-layout | Completed | Project-level skill installation layout |
| 008-create-skills-skill | Completed | Dedicated skill creation workflow |
| 012-skill-home-workdir | Completed | Portable path conventions (SKILL_HOME, SKILL_WORKDIR) |
| 013-portable-skill-creation | Completed | Remove environment-specific tool discovery |
| **017-consolidate-draft-skills** | **In Progress** | **Consolidate 9 drafts → 3 formal skills** |

## Feature Index Entry

```
| 013 | Skills Command | Manage extensible skills/tools. | Implemented | .specify/memory/features/013.md | .specify/specs/017-consolidate-draft-skills/requirements.md | 2026-06-18 |
```

## Impact on Feature 013

This spec does NOT introduce new features or deprecate existing ones. It creates 3 new skill packages under the existing Feature 013 umbrella:
- `document-utils` — consolidates 5 document-format draft skills
- `database-utils` — consolidates 2 database-protocol draft skills  
- `browser-utils` — consolidates 2 browser-automation draft skills

No other features are affected by this change.
