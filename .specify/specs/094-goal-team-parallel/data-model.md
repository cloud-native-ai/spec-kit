# Data Model — Feature 092

Entities the feature designs. Field names are the ones the contracts use verbatim; a field that the contracts do
not name is marked `annotation` and is not required. Validation rules point at the contract clause that owns them.

## E-1 Binding record ([[STR-001]] `binding`)

Carried inside E-2 / E-3 frontmatter. Not a store of its own (FR-002).

| Field | Type | Domain | Rule |
|-------|------|--------|------|
| `owner` | closed set | `sdd-run` / `command-run` / `human` | C-2 |
| `owner_id` | token | state-spine `run_id` shape, or `human` | C-3 (name only, grammar owned by the driver's state model) |
| `origin` | nullable token | `null` or an existing `.specify/specs/<dir>` basename | C-4 |

Validation: exactly these three keys; a missing key is `binding-missing`; a hand edit is `binding-hand-edited`
(C-5); rewrites preserve every other byte (C-6).

## E-2 Goal definition

Path `.specify/goal/<slug>/goal.md` (C-31). Existing shape (objective, criteria, lifecycle status, created/updated
dates, change history, optional targets, boundaries) is preserved; the following are added or constrained:

| Field | Type | Rule |
|-------|------|------|
| `binding` | E-1 | required |
| `handoff_ref` | nullable path | spec-dir-relative path of the `handoff.md` that names this goal (C-59) |
| `status` | closed set | `active` / `achieved` / `abandoned` (C-17) |
| `targets[].id` | `T-NNN` | existing engine rule, unchanged |
| `origin` (inside binding) | see E-1 | set by migration (C-36) or creation |

## E-3 Team definition

Path `.specify/teams/<slug>/team.md` (C-31).

| Field | Type | Rule |
|-------|------|------|
| `binding` | E-1 | required |
| `goal_slug` | identity | one-way, N teams : 1 goal, no goal content copy (C-28) |
| `handoff_ref` | nullable path | same contract as E-2 (C-59) |
| `lifecycle_state` | closed set | `active` / `archived` (C-18) |
| `territory.write[]` | path list | must not include `.specify/goal/**` or `.specify/teams/**` (C-15) |
| `territory.forbidden[]` | path list | the three spec artifacts plus `handoff.md` when a contract is active (C-62) |

## E-4 Archive layer ([[STR-002]] `archive-scope`)

Not a file: the closed coordinate system that answers "which tree". Members: `goal`, `teams`, `auto` (C-9, C-10).
`auto` is a read-only resolver, never a write target (C-11, C-13).

## E-5 Migration receipt

One file per entry: `.specify/archive/goal-team/receipts/<kind>-<slug>.yaml` (C-32, C-33).

| Field | Type | Rule |
|-------|------|------|
| `kind` | `goal` / `teams` | |
| `source_spec` | spec-dir name | recorded as `origin` too (C-36) |
| `source_slug` / `target_slug` | identity | equal unless a deliberate rename, which this feature does not perform |
| `target_path` / `archived_path` | path | both must exist after a completed migration (C-37) |
| `concept_digest` | digest | over the concept payload only (C-41) |
| `result` | closed set | `migrated` / `noop` / `conflict` / `interrupted` / `archived` |
| `delete_policy` | literal | `archive-not-delete` (FR-010) |
| `at` | timestamp | UTC ISO-8601 |

## E-6 Residual probe reading

Read-only output (C-43). Rows: `kind`, `path`, plus per-kind counts. No state, never written to disk by the engine.

## E-7 Archive receipt

Same directory family as E-5 with `result: archived`; written when a definition retires in place (C-34). Not a
read surface for current facts.

## E-8 Handoff contract ([[STR-004]] `handoff.md`)

Path `<spec-dir>/handoff.md` (C-53). Frontmatter:

| Field | Type | Rule |
|-------|------|------|
| `contract` | literal | `handoff/v1` (C-55) |
| `state` | closed set | `active` → `fulfilled` / `abandoned` (C-55) |
| `goal_slug` | identity | resolves to E-2 (C-58) |
| `team_slug` ([[STR-005]]) | identity | resolves to E-3 (C-58) |
| `created` / `updated` | dates | |
| `supersedes` | nullable path | |

Body sections: `## Status`, `## Goal`, `## Targets`, `## Task Reference`, `## Territory`, `## Acceptance Criteria`,
`## Writeback`, `## Crew` (C-54). `## Task Reference` holds id ranges, never task rows (C-57).

## E-9 Command-family fact

`shared/declarations/facts/goal-team-command-family.yaml` (C-76). `kind: closed-set`; `statement` is the explicit
addition list on top of the class predicate; mandatory declaration keys `fact`, `kind`, `statement`, `consumers`,
`former_carriers`.

## E-10 Handoff threshold fact

`shared/declarations/facts/goal-team-handoff-threshold.yaml` (C-79). `kind: threshold`; statement keys `metric:
task-count`, `threshold: <int>`, `boundary: exclusive`, `on_direct: none`, `on_handoff: after-tasks-u4`.

## E-11 Legacy key alias

Not a new field: a read-only mapping of `temp_goal_slug` / `temp_team_slug` / `temp_scope_spec_dir` onto
`goal_slug` / `team_slug` / `origin_spec_dir` (C-21…C-24). Removal point recorded in the concept owner (C-23).

## E-12 Territory set

The pair (`territory.write`, `territory.forbidden`) on E-3 after a handoff activation expands E-8's `## Territory`
(C-61). Derived, not stored separately.

## E-13 Writability decision

A pure function result: `(kind, binding, bound_teams) → allowed | refused(reason)` (C-14). Reasons:
`bound-by:<team-slug>` (a goal bound by a team, written by a non-`human` owner), `archived` (a team),
`cross-layer-write` (C-16). Never a stored field.

## State transitions

| Subject | From | To | Trigger | Rule |
|---------|------|----|---------|------|
| E-2 goal | `active` | `achieved` / `abandoned` | explicit `/speckit.goal` action | C-17 |
| E-2 goal | terminal | `active` | explicit `reopen`, `owner: human` only | C-19 |
| E-3 team | `active` | `archived` | explicit action; `run-team` then refuses | C-18 |
| E-8 handoff | `active` | `fulfilled` / `abandoned` | spec-side action after writeback verification | C-55, C-64 |
| E-2 / E-3 (migrated) | spec-local (residual) | unified archive | `migrate-archive` | C-35…C-40 |
| migration run | — | `interrupted` | process stops mid-definition | C-39 (resumable) |

## Validation rules (drawn from requirements)

1. A definition without a complete E-1 is uninterpretable (FR-002).
2. Two definitions with the same slug cannot coexist in the archive, whatever their `owner` differs (FR-021).
3. A terminal goal refuses a new binding (FR-026c).
4. A bound goal is writable only by `human` (FR-038).
5. A handoff names only resolving keys and never copies task rows (FR-034, C-57).
6. The complexity fact is the only input to "complex / direct" and to goal/team creation timing (FR-018, FR-039).
7. The declaration facts cannot take effect before registration (C-83).
8. A residual directory is reported, never read as current (C-44).
