# Feature Reference — Feature 085

## 1. Binding

| Field | Value |
|-------|-------|
| Feature ID | 085 |
| Feature name | SDD 临时 Goal / 临时 Team 与多 Agent 并发 |
| Requirement branch | `085-sdd-temporary-goal-team` |
| Requirements | [`requirements.md`](requirements.md) |
| Feature detail | `.specify/memory/features/085.md` |
| Feature index row | `.specify/memory/features.md` (Draft) |
| Flow class | execution |
| FR / SC | 50 / 10 |

## 2. Delivery Surface

| # | Surface | Change |
|---|---------|--------|
| 1 | `scripts/python/goal-utils.py` | Scope value object, `resolve-scope`, spec-local goal/team paths, scoped actions |
| 2 | `scripts/python/sdd-route.py` | `authorize` accepts scope/spec-dir and records them |
| 3 | `templates/commands/goal.md`, `templates/commands/team.md` | `--scope` / `--spec-dir` entry |
| 4 | `skills/internal/manage-goal/` | Temporary Goal workflow and scope-aware modes |
| 5 | `skills/internal/create-team/` | Spec-local team creation, `stage_seats`, scoped paths, `improve-team` scope |
| 6 | `skills/internal/run-team/` | Scoped team load, run report, `run-checks` |
| 7 | `skills/internal/improve-team/` | Scoped team edits and checkpoint proposals |
| 8 | `skills/external/sdd-loop-driver/SKILL.md` | U0 fields, requirements/plan goal/team creation, concurrency declaration |
| 9 | `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` | NEW four-part checkpoint protocol |
| 10 | `skills/external/sdd-loop-driver/references/decomposition-model.md` | `write_isolation=worktree`, new requirements/tasks rules |
| 11 | `skills/external/sdd-loop-driver/scripts/wp-gate.py` | Stages/rules/WG-15a/SD-04b/WG-17 |
| 12 | `skills/external/sdd-loop-driver/scripts/line-registry.py` | Child lines, `SPECIFY_AGENT_CONCURRENCY_CAP`, integration reuse |
| 13 | `shared/definitions/goal-definitions.md` | Temporary Goal concept |
| 14 | `shared/definitions/sdd-routing-definitions.md` | Spec-local carve-out |
| 15 | `shared/definitions/subagent-definitions.md` | Child-line/agent nesting boundary |
| 16 | `agents/*.agent.md` + `.specify/agents/**` + rendered copies | Remove generic executor; add stage roles; unify 500 |
| 17 | `skills/internal/create-agent/templates/` + `skills/internal/create-team/templates/agents/` | Role bases and budgets |
| 18 | `tests/contract/`, `tests/unit/`, `tests/integration/` | Scope/temp goal/temp team/checkpoint/worktree/budget guards |
| 19 | `docs/reference/` | Command, skill, agent documentation |
| 20 | `.specify/memory/features.md`, `.specify/memory/features/085.md` | Registry binding and status |

## 3. FR → Contract / Slice Map

| FR group | FRs | Contract / slice |
|----------|-----|------------------|
| Temporary Goal | FR-001…FR-005 | `temporary-goal-team.md` C-001…C-006; S2 |
| Temporary Team | FR-006…FR-011 | `temporary-goal-team.md` C-007…C-015; S3 |
| Scope-aware commands | FR-012…FR-017 | `scope-resolution.md` C-001…C-014; S1 |
| SDD flow and concurrency | FR-018…FR-024 | `concurrency-and-worktrees.md` C-001…C-005; S2/S3/S5 |
| Stage agents and budgets | FR-025…FR-030 | `stage-agents.md` C-001…C-005; S6 |
| Per-agent worktree/queue | FR-031…FR-036 | `concurrency-and-worktrees.md` C-006…C-018; S4 |
| Checkpoints/config | FR-037…FR-042 | `checkpoint-and-agents.md` C-001…C-013; S7 |
| Compatibility/safety | FR-043…FR-050 | plan § Constitution Check, mirrors, S0/S8 |

## 4. SC → Measurement

| SC | Path | Measurement source |
|----|------|--------------------|
| SC-001 | final | `test_scope_resolution.py` exit codes and JSON |
| SC-002 | final | fixture goal creation + parsed criteria vs SC rows |
| SC-003 | final | parsed `team.md` + `stage_seats` closure test |
| SC-004 | final | spine/dispatch requested/effective + concurrency evidence |
| SC-005 | final | child worktrees, queue report, git history |
| SC-006 | final | checkpoint files + next-stage dispatch + rollback drill |
| SC-007 | final | source/mirror/render/manifest scans + budget test |
| SC-008 | supporting | before/after hashes of global stores |
| SC-009 | supporting | pre/post 070/064 contract suites |
| SC-010 | supporting | dogfood run report and evidence |

## 5. Disclosed Rulings

- The generic `sdd-executor` is removed, not kept as a fallback; dated historical records are not rewritten.
- The default concurrency is a target, not a guarantee; requested/effective must be recorded.
- Temporary Goal/Team are spec-local and do not enter global stores.
- The 070 shared-tree mode and 064 root-line behavior remain the compatibility baseline.
- The temporary hierarchy is a spec-local carve-out, not an inversion of 074's global hierarchy.
