# Research — Feature 085

**Status**: Phase 0 rulings. Each ruling records the decision, the rejected alternative and the measured anchor. Dates are 2026-11-06.

## R1 — Temporary hierarchy, not a global inversion

**Decision**: Add `SDD run → Temporary Goal → Temporary Team → stage agents` as a spec-local hierarchy. Keep `Global Goal → Global Team → Agent → SDD run` unchanged.

**Rejected alternative**: Let the driver create a Global Goal/Team at U0. This violates 074 FR-001 (`074/requirements.md:219-222`) and `shared/definitions/sdd-routing-definitions.md` § Hierarchy, and creates an authorization chicken-and-egg (the `(team, seat)` predicate needs a team before the run starts).

**Evidence**: The user explicitly distinguished temporary from global and placed goal/team creation after requirements/plan. 074a/074b already implement the global nested invocation and the `## Nested SDD Runs` report section.

## R2 — One scope resolver owned by `goal-utils.py`

**Decision**: `goal-utils.py resolve-scope` owns the global/spec/auto path rule; every consumer (`/speckit.goal`, `/speckit.team`, `run-checks`, `sdd-route authorize`, create/run/improve, evidence) calls it or the same `Scope` object.

**Rejected alternative**: Add a second path resolver in `create-team`/`run-team`. Two resolvers drift and turn one identity into two paths.

**Evidence**: `goal-utils.py` already owns `ARCHIVE_DIRNAME`, `definition_path()`, and the three team-path sites; `create-mode.md` and `run-team` already depend on it.

## R3 — Child lines extend 064, not a second queue

**Decision**: Each writing agent registers a child line with `parent_line_id` and `line_role=agent-write`; child worktrees use the existing `.specify/.tmp` root; integration reuses the existing registry/queue actions.

**Rejected alternative**: A new per-agent queue or a second ownership model. This violates 064's no-second-store rule and FR-031..036.

**Evidence**: `skills/external/sdd-loop-driver/scripts/line-registry.py` already has register/ownership/resources/integration actions; `references/dispatch-recipes.md:276-317` documents worktree-per-write-line and the queue sequence.

## R4 — `write_isolation=worktree` is additive to 070

**Decision**: Keep 070's `shared-tree` default and its write-serial rule byte-identical. Temporary-team runs opt into `write_isolation=worktree`; write packages run concurrently in child worktrees and serialize only at integration.

**Rejected alternative**: Change 070's default to worktree for all runs. That would break the implemented 070 contract and its pinned tests.

**Evidence**: `decomposition-model.md:166-172` owns the write-alone rule; `references/patterns.md:124-131` already documents an optional `isolation: worktree` for team members.

## R5 — Dynamic role grammar, not a fixed roster

**Decision**: Use the role grammar `coordinator / worker / verifier / integrator` and let each stage decide count/type from the work-package benefit test and effective concurrency. User-named examples: `sdd-requirement-analyzer`, `sdd-plan-coordinator`, `sdd-plan-executor`.

**Rejected alternative**: A fixed roster with a fixed number of agents per stage. The user explicitly said count/type are implementation details and should vary.

**Evidence**: Requirements starts with one agent; tasks/implement may use many. Existing capacity templates (requirements-analyst, system-designer, module-designer, test-engineer, qa-engineer) provide role bases.

## R6 — All retained agents use 500

**Decision**: Every retained framework agent definition gets `run-turn-budget: 500`; every rendered copy gets `maxTurns: 500`/`steps: 500`. Synthetic render fixtures are exempt.

**Rejected alternative**: Keep per-role budgets. The user asked for uniform 500 and the current spread (40–400) is a drift source.

**Evidence**: `agents/sdd-executor.agent.md` is currently 400 (not 120); `dispatch-recipes.md:29` records the 2026-11-05 120→400 policy; the unified policy supersedes it with a dated note.

## R7 — Remove the generic `sdd-executor`

**Decision**: Delete the generic template, its mirror, rendered copies, and manifest entries. Replace the requirements instance with `sdd-requirement-analyzer`. Keep `sdd-setup-executor` as a bootstrap path with no `capacity-scope: sdd-executor`.

**Rejected alternative**: Keep the generic agent as a fallback. The user said a generic SDD executor is meaningless; a fallback would keep the drift source.

**Evidence**: `sdd-executor` is referenced by 060 contract tests, fast-fail discipline tests, create-agent/run-agent docs, and the render manifest; all are live references to update. Dated state/evidence records are not rewritten.

## R8 — Checkpoints reuse existing proposal shapes

**Decision**: At each stage boundary, use `wp-report.py` + team run report + ledger, propose at most one configuration change, ratify, and apply via `improve-team`/`/speckit.team modify`. Rollback on named regressions.

**Rejected alternative**: A new optimizer engine or an automatic search loop. That adds a second metric store and bypasses the existing confirmation discipline.

**Evidence**: `improve-team` already does targeted, evidence-based edits; `goal coordinate` already models detect → propose → ratify → write back; 070's ledger is the only metric source.
