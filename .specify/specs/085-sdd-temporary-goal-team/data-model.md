# Data Model — Feature 085

**Storage**: spec-local files plus the existing environment line registry. No database, daemon, or second ledger.

## Entities

### E1 — Temporary Goal

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `slug` | string | yes | Default = spec basename; unique within the spec scope |
| `objective` | string | yes | End-state outcome, not a task list; engine GD-2 |
| `criteria[]` | string[] | no | Degree-measured; disjoint from `SC-` rows |
| `status` | enum | yes | `active` / `achieved` / `abandoned` |
| `targets[]` | object[] | no | Optional scope slices; unordered; no stage-order semantics |
| `history[]` | string[] | engine-owned | Prior values on deliberate change |
| `spec_dir` | path | yes | `.specify/specs/<NNN-slug>` |
| `scope` | literal | yes | `spec` |

**Rules**: V-1 one goal per spec by default; V-2 engine-only writes; V-3 criteria must not duplicate SC rows; V-4 terminal goals retained; V-5 Targets do not encode dependencies.

### E2 — Temporary Team

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `slug` | string | yes | Team identity; default = spec basename |
| `scope` | literal | yes | `spec` |
| `spec_dir` | path | yes | Parent spec |
| `goal_slug` | string | yes | Must resolve in the spec scope |
| `lifecycle_state` | enum | no | `active` (default) / `archived` |
| `stage_seats` | map | yes | Keys = 8 canonical SDD stages |
| `members[]` | object[] | yes | Each resolves to a framework agent definition |
| `config.agent_concurrency` | object | yes | `{requested, effective, reason}` |
| `config.isolation` | literal | yes | `worktree` for temporary-team runs |
| `config.checkpoint_policy` | object | yes | `{propose, max_config_changes:1, ratification}` |
| `config.summary` | object | no | Temporary teams default `enabled:false`, reason `run-scoped` |
| `territory` | object | yes | `write` / `read` / `forbidden` / `non_path` |

**Rules**: V-6 `stage_seats` keys are canonical stages; V-7 every seat resolves to a member; V-8 `max_parallel` is positive and ≤ effective concurrency; V-9 Team Stage dimension stays `executor|evaluator|optimizer`; V-10 archived teams are refused by `run-team`; V-11 no write to global `.specify/teams/**`.

### E3 — Scope Resolution

| Field | Type | Notes |
|-------|------|-------|
| `scope` | `global` / `spec` | Resolved value |
| `spec_dir` | path/null | Required for spec |
| `goal_root` | path | `.specify/goal` or `<spec-dir>/goal` |
| `team_root` | path | `.specify/teams` or `<spec-dir>/team` |
| `goal_definition` | path | `<goal_root>/<slug>/goal.md` |
| `team_definition` | path | `<team_root>/<slug>/team.md` |

**Rules**: V-12 spec dir must be under `.specify/specs/`; V-13 `auto` resolves only with one candidate; V-14 both candidates → exit 2 `scope-ambiguous`; V-15 wrong scope → exit 3 with a hint; V-16 no fallback.

### E4 — Stage Seat Map

| Field | Type | Notes |
|-------|------|-------|
| `stage` | enum | requirements/clarify/plan/tasks/checklist/analyze/implement/review |
| `seats[]` | string[] | Coordinator/worker/verifier/integrator for the stage |
| `max_parallel` | int | Per-stage cap |

### E5 — Child Line

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `line_id` | string | yes | Environment-unique |
| `parent_line_id` | string | yes | Must exist; parent is not a child; depth 1 |
| `line_role` | literal | yes | `agent-write` |
| `worktree_path` | abs path | yes | `.specify/.tmp/sdd-loop/worktrees/<child_line_id>` |
| `branch` | string | yes | `line/<child_line_id>` |
| `owned_paths` | string[] | yes | Package territory |
| `forbidden_paths` | string[] | yes | Includes `.specify/goal/**`, `.specify/teams/**` |
| `integration_depends_on` | string[] | no | Package dependency mapping |

**Rules**: V-17 child excluded from root-line cap; V-18 `SPECIFY_AGENT_CONCURRENCY_CAP` default 24 per parent; V-19 worktree must be outside repo root/project dir; V-20 removal only after merged.

### E6 — Checkpoint

| Field | Type | Notes |
|-------|------|-------|
| `stage` | enum | The stage just closed |
| `artifact_verification` | object | U4 verdict + evidence pointer |
| `goal_progress[]` | object[] | `{criterion, degree, evidence_ptr}` |
| `config_proposal` | object/null | At most one; includes evidence and exact delta |
| `concurrency_roster` | object | Next stage's requested/effective and roster decision |
| `ratification` | object | `{state, by, at}` |
| `rollback` | object/null | Prior change, trigger, reversal evidence |

### E7 — Concurrency Record

| Field | Type | Notes |
|-------|------|-------|
| `requested` | int | Default 24 |
| `effective` | int | Resolved per stage |
| `reason` | enum | `host-capacity-declared` / `host-capacity-undeclared` / `host-capacity-observed` / `package-limited` / `stage-limited` / `resource-limited` |
| `verifier_reserve` | int | `max(1, ceil(effective/4))` |
| `executor_slots` | int | `effective - verifier_reserve` |

### E8 — Integration Entry

| Field | Type | Notes |
|-------|------|-------|
| `child_line_id` | string | Source |
| `order` | int | From 070 `integration_order` |
| `result` | enum | `merged` / `failed` |
| `commit` | string/null | Merge commit when merged |
| `reason` | string/null | Conflict, missing output, gate failure |

**Rules**: V-21 order is declared, never dispatch timing; V-22 failure retains worktree/evidence; V-23 no partial stage deliverable; V-24 no push.
