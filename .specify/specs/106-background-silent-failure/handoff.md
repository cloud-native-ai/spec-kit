---
contract: handoff/v1
state: active
goal_slug: 106-background-silent-failure
team_slug: 106-background-silent-failure
created: 2026-11-25
updated: 2026-11-25
supersedes: null
---

## Status

State: read from the frontmatter `state` field — `active` → `fulfilled` or `active` → `abandoned`; a terminal handoff is retained, never deleted (C-55).
This contract hands the construction of the referenced task ranges to the referenced crew; design authority stays on the spec side (C-64).

## Goal

Cite by `goal_slug` only: 106-background-silent-failure.

## Targets

None.

## Task Reference

T001–T037 as defined in `.specify/specs/106-background-silent-failure/tasks.md`.

## Territory

The paths the crew may write, relative to the repository:

- write: `.specify/specs/106-background-silent-failure/notes/**`
- write: `.specify/specs/106-background-silent-failure/writeback/**`
- write: `.specify/specs/106-background-silent-failure/test-evidence/**`
- write: `.specify/{session,knowledge,feedback,evidence,exec-quant,trigger,retention,renumber,sanitize,housekeeping,coaching,todo,tools,migrate}/**`
- write: `seed/**`, `shared/**`, `skills/**`, `scripts/**`, `src/specify_cli/**`, `templates/**`, `agents/**`, `tests/**`
- write: `docs/reference/**`, `docs/concepts/**`, `docs/tutorials/**`
- write: `.specify/shared/**`, `.specify/scripts/**`, `.specify/templates/**`, `.specify/agents/templates/**`, `.specify/skills/**`
- write: `.github/prompts/**`, `.claude/commands/**`, `.qoder/commands/**`, `.opencode/command/**`
- write: `.specify/instructions.md`, `.specify/glossary.md`, `.specify/.gitignore`, `pyproject.toml`

The following MUST stay forbidden to every seat that carries the expansion (C-62): `requirements.md`, `tasks.md`, `verification.md`, `handoff.md`; this contract additionally forbids `plan.md`, `data-model.md`, `contracts/**`, `quickstart.md`, `research.md`, `feature-ref.md`, `checkpoints/**`, `.specify/anchoring/**`, `.specify/teams/**`, `.specify/state/**`, `.specify/features.md`, `.specify/features/095-superagent-role.md`, and dated documentation trees (`docs/reference/history/**`, `docs/decisions/**`, `docs/archive/**`).

## Acceptance Criteria

SC-001…SC-009 from `.specify/specs/106-background-silent-failure/requirements.md`.

## Writeback

One record per completed task at `.specify/specs/106-background-silent-failure/writeback/<T-NNN>.yaml` carrying `task`, `outcome` (`done` | `blocked` | `deferred`), `run_id`, `evidence` (path or command plus exit code), and `at` (C-65).

## Crew

Cite by `team_slug` only: 106-background-silent-failure.
