---
contract: handoff/v1
state: active
goal_slug: 107-decision-governance
team_slug: 107-decision-governance
created: 2026-11-25
updated: 2026-11-25
supersedes: null
---

## Status

State: read from the frontmatter `state` field — `active` → `fulfilled` or `active` → `abandoned`; a terminal handoff is retained, never deleted (C-55).
This contract hands the construction of the referenced task ranges to the referenced crew; design authority stays on the spec side (C-64).

## Goal

Cite by `goal_slug` only: 107-decision-governance.

## Targets

None.

## Task Reference

T001–T056 as defined in `.specify/specs/107-decision-governance/tasks.md`. T056's crew-side deliverable is `.specify/specs/107-decision-governance/test-evidence/verification-input.md`; `verification.md` is derived spec-side from that input and is never a crew write.

## Territory

The paths the crew may write, relative to the repository:

- write: `.specify/specs/107-decision-governance/notes/**`
- write: `.specify/specs/107-decision-governance/writeback/**`
- write: `.specify/specs/107-decision-governance/test-evidence/**`
- write: `.specify/{session,knowledge,feedback,evidence,exec-quant,trigger,retention,renumber,sanitize,housekeeping,coaching,todo,tools,migrate}/**`
- write: `seed/**`, `shared/**`, `skills/**`, `scripts/**`, `src/specify_cli/**`, `templates/**`, `agents/**`, `tests/**`
- write: `docs/reference/**`, `docs/concepts/**`, `docs/tutorials/**`
- write: `.specify/shared/**`, `.specify/scripts/**`, `.specify/templates/**`, `.specify/agents/templates/**`, `.specify/skills/**`
- write: `.github/prompts/**`, `.claude/commands/**`, `.qoder/commands/**`, `.opencode/command/**`
- write: `.specify/instructions.md`, `.specify/glossary.md`, `.specify/.gitignore`, `pyproject.toml`

The following MUST stay forbidden to every seat that carries the expansion (C-62): `requirements.md`, `tasks.md`, `verification.md`, `handoff.md`; plus `plan.md`, `data-model.md`, `contracts/**`, `quickstart.md`, `research.md`, `feature-ref.md`, `checkpoints/**`, `.specify/anchoring/**`, `.specify/teams/**`, `.specify/state/**`, `.specify/features.md`, `.specify/features/107-decision-governance.md`, and dated documentation trees. `verification.md` stays forbidden because it is derived spec-side from the crew's `test-evidence/verification-input.md`, not written by a seat.

## Acceptance Criteria

SC-001…SC-010 from `.specify/specs/107-decision-governance/requirements.md`.

## Writeback

One record per completed task at `.specify/specs/107-decision-governance/writeback/<T-NNN>.yaml` carrying `task`, `outcome`, `run_id`, `evidence`, and `at` (C-65).

## Crew

Cite by `team_slug` only: 107-decision-governance.
