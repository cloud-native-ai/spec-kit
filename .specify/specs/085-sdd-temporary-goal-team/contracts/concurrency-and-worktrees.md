# Contract — Concurrency and Per-Agent Worktrees

Owners: `.specify/specs/064-subagent-concurrency/contracts/` (line registry, workspace isolation, integration queue) and `.specify/specs/070-subagent-task-teams/contracts/` (work packages, scheduler).

- **C-001**: U0 MUST record `agent_concurrency_requested` with a default of 24 and the temporary scope fields.
- **C-002**: The effective concurrency MUST be the minimum of requested, host capacity, stage `max_parallel`, ready executor packages plus verifier reserve, and resource capacity.
- **C-003**: `verifier_reserve` MUST be `max(1, ceil(effective / 4))`; executor slots MUST be `effective - verifier_reserve`.
- **C-004**: A non-declared host capacity MUST be recorded as `host-capacity-undeclared`; a failed dispatch observation MUST halve the effective value with a floor of 1 and a named reason.
- **C-005**: Every dispatch event MUST record requested and effective concurrency; a downgrade MUST never be silent.
- **C-006**: Each SDD run MUST register one coordinator line; each writing agent MUST register a child line with `parent_line_id` and `line_role=agent-write`.
- **C-007**: The parent MUST exist and MUST NOT itself be a child; nesting depth MUST be exactly one.
- **C-008**: A child worktree MUST be under `.specify/.tmp/sdd-loop/worktrees/<child_line_id>` and use branch `line/<child_line_id>`.
- **C-009**: A child line MUST declare `owned_paths` from its package territory and inherit `.specify/goal/**` and `.specify/teams/**` as forbidden paths.
- **C-010**: Child lines MUST be excluded from `SPECIFY_LINE_CONCURRENCY_CAP`; `SPECIFY_AGENT_CONCURRENCY_CAP` MUST default to 24 per parent.
- **C-011**: Integration order MUST be the work-package plan's declared order, never dispatch timing.
- **C-012**: Integration MUST run rebase → targeted quality gate → fast-forward merge → integration record → runtime archive → worktree removal (merged only) → deregistration.
- **C-013**: A failed integration MUST retain the worktree and evidence, record a failed result with a reason, and produce no partial stage deliverable.
- **C-014**: A child line MUST NOT push; merge/push remains the outer layer's decision under its confirmation gates.
- **C-015**: `write_isolation=worktree` MUST be opt-in for temporary-team runs; 070 `shared-tree` remains the default.
- **C-016**: 070's existing write-alone literal, read-only slot cap, and pinned tests MUST remain valid; the new mode appends qualifiers rather than rewriting them.
- **C-017**: 064's root-line behavior, ownership model, and integration queue MUST remain unchanged for entries without the new child fields.
- **C-018**: Disk preflight MUST run before child worktree creation; an out-of-space condition MUST surface as a named anomaly and MUST NOT delete another worktree. (FR-018, FR-019, FR-020, FR-021, FR-022, FR-023, FR-024, FR-031, FR-032, FR-033, FR-034, FR-035, FR-036, FR-043, FR-044, FR-045, FR-046)
