# Contract: Skill Removal

**ID**: C-REMOVE | **Feature**: 029 | **Maps to**: FR-001, FR-002, SC-002

## Interface

`sdd-workflow` ceases to exist as a skill in every surface.

## Rules

- **MUST** delete the source directory `skills/sdd-workflow/` (its `SKILL.md` and `references/`).
- **MUST** ensure `sdd-workflow` is absent from the installed skills directory `.specify/skills/`.
- **MUST** ensure `sdd-workflow` is absent from every compatibility skills symlink target
  (`.github/skills`, `.<agent>/skills`) — achieved automatically once it is gone from `.specify/skills`.
- **MUST** remove the `sdd-workflow` row from the generated instructions Skills registry table.
- **MUST** decrement the skill count wherever it is stated (e.g. "20 total" → "19 total") in the
  generated instructions and in `docs/` that quote a count.
- After removal, `skills-utils.py` skill enumeration **MUST NOT** list `sdd-workflow`.

## Non-Goals

- No new symlink surface is created for `shared/` — it is reached only via `.specify/shared/...`
  paths and is intentionally NOT skill-discoverable.

## Test Mapping

- Contract test: `skills/sdd-workflow` does not exist in source.
- Integration test: after init, `.specify/skills/sdd-workflow` and `<tool>/skills/sdd-workflow` do not exist.
- Contract test: generated instructions Skills registry has no `sdd-workflow` row and the stated count is decremented.
