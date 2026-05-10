# Feature Reference: Create Skills Skill

**Parent Feature**: `013` / `Skills Command`  
**Spec**: `.specify/specs/008-create-skills-skill/requirements.md`

## Feature Relationship

This specification is a focused slice of the long-lived `Skills Command` feature. It does not introduce a new top-level feature. It evolves the Skills Command by separating explicit workflow orchestration from reusable Skill-authoring knowledge.

## Feature Memory Updates

- `.specify/memory/features.md` now points Feature `013` to this requirements slice as the latest spec.
- `.specify/memory/features/013.md` records this iteration as the current review focus.

## Integration Notes

- `/speckit.skills` remains the user-facing command entrypoint.
- `create-skills` owns new Skill creation guidance.
- `improve-skills` owns existing Skill refinement guidance.
- Future `/speckit.skills` changes should preserve this separation unless a later spec explicitly changes the command/Skill boundary.
