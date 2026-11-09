# Contract — Goal and Team (scope: spec)

Owners: `shared/definitions/goal-definitions.md` (Goal concept and its two scopes), `skills/internal/create-team/references/conceptual-model.md` (Team concept), `skills/internal/create-team/references/create-mode.md` (schema).

- **C-001**: A Goal (scope: spec) MUST be a spec-attached authored definition stored at `.specify/specs/<NNN-slug>/goal/<goal-slug>/goal.md`.
  <!-- superseded (092: scope-not-temporary) -->
  <!-- prior text, retained (2026-11-09): "A Temporary Goal MUST be a spec-attached, run-scoped authored definition stored at `.specify/specs/<NNN-slug>/goal/goal.md`." -->
- **C-002**: It MUST be authorable only after the `requirements` stage passes U4; before that, no spec-scoped goal file may exist.
  <!-- superseded (092: scope-not-temporary) -->
  <!-- prior text, retained (2026-11-09): "before that, no temporary goal file may exist." -->
- **C-003**: Its objective MUST be an end-state outcome, not a task list; engine GD-2/GD-3 checks apply.
- **C-004**: Its criteria MUST be degree-measured and MUST NOT duplicate any `SC-` row in the same spec.
- **C-005**: It MUST use the `active`/`achieved`/`abandoned` lifecycle; terminal goals are retained.
- **C-006**: One spec MUST have at most one goal by default; identity defaults to the spec basename and is unique in the spec scope.
  <!-- superseded (092: scope-not-temporary) -->
  <!-- prior text, retained (2026-11-09): "One spec MUST have at most one temporary goal by default; identity defaults to the spec basename and is unique in the spec scope." -->
- **C-007**: A Team (scope: spec) MUST be a spec-attached persisted roster stored at `.specify/specs/<NNN-slug>/team/team.md` for the spec's single default team; an ADDITIONAL named team nests as `.specify/specs/<NNN-slug>/team/<team-slug>/team.md` (the default team never nests under its own spec slug — that duplicates the slug in the path).
  <!-- superseded (092: scope-not-temporary) -->
  <!-- prior text, retained (2026-11-09): "A Temporary Team MUST be a spec-attached persisted roster stored at `.specify/specs/<NNN-slug>/team/team.md` for the spec's single default team; an ADDITIONAL named team nests as `.specify/specs/<NNN-slug>/team/<team-slug>/team.md` (the default team never nests under its own spec slug — that duplicates the slug in the path); the `<slug>` directory collapses to `team/team.md` only when the team slug equals the spec basename." The trailing collapse clause was already retired by the 092 default-team ruling (`a1549dc7`); the sentence above is that text with the rename applied. -->
- **C-008**: It MUST be created only after both `clarify` and `plan` pass U4, and MUST bind `goal_slug` to the spec-scoped goal.
  <!-- superseded (092: scope-not-temporary) -->
  <!-- prior text, retained (2026-11-09): "…and MUST bind `goal_slug` to the temporary goal." -->
- **C-009**: Its frontmatter MUST carry `scope: spec`, `spec_dir`, `goal_slug`, optional `lifecycle_state`, `stage_seats`, and `config.agent_concurrency`.
- **C-010**: `stage_seats` keys MUST be exactly the eight canonical SDD stages; every seat MUST resolve to a roster member; `max_parallel` MUST be positive and ≤ effective concurrency.
- **C-011**: The Team `Stage` dimension MUST remain `executor`/`evaluator`/`optimizer`; no SDD stage name may be used there.
- **C-012**: A spec-scoped team MUST write a run report for each stage under `team/runs/` using the existing report contract.
  <!-- superseded (092: scope-not-temporary) -->
  <!-- prior text, retained (2026-11-09): "A temporary team MUST write a run report for each stage under `team/runs/` using the existing report contract." -->
- **C-013**: A spec-scoped team MUST be adjustable at any time through the team modification path and MUST be archived in place at completion.
  <!-- superseded (092: scope-not-temporary) -->
  <!-- prior text, retained (2026-11-09): "A temporary team MUST be adjustable at any time through the team modification path and MUST be archived in place at completion." -->
- **C-014**: A spec-scoped team MUST NOT write `.specify/anchoring/**` or `.specify/teams/**`.
  <!-- superseded (092: scope-not-temporary) -->
  <!-- prior text, retained (2026-11-09): "A temporary team MUST NOT write `.specify/goal/**` or `.specify/teams/**`." The two halves are one substitution: the retired "temporary" attribute goes, and the global archive moved `.specify/goal/` → `.specify/anchoring/` under the same 092 ruling. -->
- **C-015**: A spec-scoped goal MUST NOT be copied into a requirements spec; no structural Goal field is added to `requirements.md`. (FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011)
  <!-- superseded (092: scope-not-temporary) -->
  <!-- prior text, retained (2026-11-09): "A temporary goal MUST NOT be copied into a requirements spec; …" -->
