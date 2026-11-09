# Contract — Temporary Goal and Temporary Team

Owners: `shared/definitions/goal-definitions.md` (Goal concept), `skills/internal/create-team/references/conceptual-model.md` (Team concept), `skills/internal/create-team/references/create-mode.md` (schema).

- **C-001**: A Temporary Goal MUST be a spec-attached, run-scoped authored definition stored at `.specify/specs/<NNN-slug>/goal/goal.md`.
- **C-002**: It MUST be authorable only after the `requirements` stage passes U4; before that, no temporary goal file may exist.
- **C-003**: Its objective MUST be an end-state outcome, not a task list; engine GD-2/GD-3 checks apply.
- **C-004**: Its criteria MUST be degree-measured and MUST NOT duplicate any `SC-` row in the same spec.
- **C-005**: It MUST use the `active`/`achieved`/`abandoned` lifecycle; terminal goals are retained.
- **C-006**: One spec MUST have at most one temporary goal by default; identity defaults to the spec basename and is unique in the spec scope.
- **C-007**: A Temporary Team MUST be a spec-attached persisted roster stored at `.specify/specs/<NNN-slug>/team/<slug>/team.md`; the `<slug>` directory collapses to `team/team.md` only when the team slug equals the spec basename.
  <!-- superseded by: skills/internal/create-team/references/create-mode.md (team root layout) -->
  <!-- prior text, retained (2026-11-09): "stored at `.specify/specs/<NNN-slug>/team/team.md`." -->
- **C-008**: It MUST be created only after both `clarify` and `plan` pass U4, and MUST bind `goal_slug` to the temporary goal.
- **C-009**: Its frontmatter MUST carry `scope: spec`, `spec_dir`, `goal_slug`, optional `lifecycle_state`, `stage_seats`, and `config.agent_concurrency`.
- **C-010**: `stage_seats` keys MUST be exactly the eight canonical SDD stages; every seat MUST resolve to a roster member; `max_parallel` MUST be positive and ≤ effective concurrency.
- **C-011**: The Team `Stage` dimension MUST remain `executor`/`evaluator`/`optimizer`; no SDD stage name may be used there.
- **C-012**: A temporary team MUST write a run report for each stage under `team/runs/` using the existing report contract.
- **C-013**: A temporary team MUST be adjustable at any time through the team modification path and MUST be archived in place at completion.
- **C-014**: A temporary team MUST NOT write `.specify/goal/**` or `.specify/teams/**`.
- **C-015**: A temporary goal MUST NOT be copied into a requirements spec; no structural Goal field is added to `requirements.md`. (FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011)
