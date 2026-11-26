---
contract: handoff/v1
state: active
goal_slug: 108-team-view-degradation
team_slug: 108-team-view-degradation
created: 2026-11-26
updated: 2026-11-26
supersedes: null
---

## Status

State: read from the frontmatter `state` field — `active` → `fulfilled` or `active` → `abandoned`; a terminal handoff is retained, never deleted (C-55).
This contract hands the construction of the referenced task ranges to the referenced crew; design authority stays on the spec side (C-64).

## Goal

Cite by `goal_slug` only: 108-team-view-degradation.

## Targets

None.

## Task Reference

T001–T029 as defined in `.specify/specs/108-team-view-degradation/tasks.md`. T029's crew-side deliverable is `.specify/specs/108-team-view-degradation/test-evidence/verification-input.md`; `verification.md` is derived spec-side from that input and is never a crew write.

## Territory

- write: `.specify/specs/108-team-view-degradation/{notes,writeback,test-evidence}/**`
- write: `.specify/{session,knowledge,feedback,evidence,exec-quant,trigger,retention,renumber,sanitize,housekeeping,coaching,todo,tools,migrate}/**`
- write: `shared/**`, `skills/**`, `scripts/**`, `src/specify_cli/**`, `templates/**`, `agents/**`, `tests/**`, `docs/reference/**`, `docs/concepts/**`, `docs/tutorials/**`
- write: `.specify/{shared,scripts,templates,agents/templates,skills}/**`, `.github/prompts/**`, `.claude/commands/**`, `.qoder/commands/**`, `.opencode/command/**`, `.specify/instructions.md`, `.specify/glossary.md`, `.specify/.gitignore`, `pyproject.toml`

Forbidden to every seat carrying the expansion (C-62): `requirements.md`, `tasks.md`, `verification.md`, `handoff.md`, `plan.md`, `data-model.md`, `contracts/**`, `quickstart.md`, `research.md`, `feature-ref.md`, `checkpoints/**`, `.specify/anchoring/**`, `.specify/teams/**`, `.specify/state/**`, `.specify/features.md`, `.specify/features/027-team-management.md`, dated documentation trees. `verification.md` stays forbidden because it is derived spec-side from the crew's `test-evidence/verification-input.md`, not written by a seat.

## Acceptance Criteria

SC-001…SC-008 from `.specify/specs/108-team-view-degradation/requirements.md`.

## Writeback

One record per completed task at `.specify/specs/108-team-view-degradation/writeback/<T-NNN>.yaml` carrying `task`, `outcome`, `run_id`, `evidence`, and `at` (C-65).

## Crew

Cite by `team_slug` only: 108-team-view-degradation.
