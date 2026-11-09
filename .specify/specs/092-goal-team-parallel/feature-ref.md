# Feature Reference — 092-goal-team-parallel

**Feature**: goal/team binding × spec parallelism (临时/全局概念重定义 + 归档统一 + 施工队并行)
**Spec directory**: `.specify/specs/092-goal-team-parallel/`
**Binding**: `spec:092-goal-team-parallel`; `flow_class=execution` (registered declaration, not inferred)
**Delivery surface**: engine `scripts/python/goal-utils.py` (extended), declaration facts under
`.specify/shared/declarations/facts/`, the sdd-loop driver skill, the `/speckit.goal` `/speckit.team` `/speckit.feedback`
command templates, the framework map, and the 085 test set.
**Authority**: `requirements.md` (42 FR, 11 SC, Clarifications Q1–Q12, Assumptions A1–A11) is the intent owner; the
contracts below are the conformance owner; `plan.md` is the design owner. This page restates no rule — it maps.

## Delivery map — FR → contract clause

| FR | Clause | FR | Clause |
|---|---|---|---|
| FR-001 | binding-and-lifecycle C-1, C-2 | FR-022 | command-family-and-declarations C-77…C-80 |
| FR-002 | binding-and-lifecycle C-3 | FR-023 | binding-and-lifecycle C-26 |
| FR-003 | binding-and-lifecycle C-4 | FR-024 | handoff-contract C-53, C-58 |
| FR-004 | binding-and-lifecycle C-5 | FR-025 | binding-and-lifecycle C-25 |
| FR-005 | binding-and-lifecycle C-18, C-19 | FR-026 | binding-and-lifecycle C-27 |
| FR-006 | owner-rewrites-and-tests C-91 | FR-027 | binding-and-lifecycle C-28 |
| FR-007 | unified-archive-and-migration C-32, C-33 | FR-028 | binding-and-lifecycle C-29 |
| FR-008 | binding-and-lifecycle C-11 | FR-029 | handoff-contract C-56, C-57 |
| FR-009 | unified-archive-and-migration C-34 | FR-030 | handoff-contract C-59 |
| FR-010 | unified-archive-and-migration C-35 | FR-031 | command-family-and-declarations C-81, C-88 |
| FR-011 | unified-archive-and-migration C-36 | FR-032 | command-family-and-declarations C-71 |
| FR-012 | unified-archive-and-migration C-37, C-38 | FR-033 | command-family-and-declarations C-71, C-72 |
| FR-013 | unified-archive-and-migration C-39, C-40 | FR-034 | command-family-and-declarations C-84 |
| FR-014 | binding-and-lifecycle C-11, C-12 | FR-035 | command-family-and-declarations C-86, C-87 |
| FR-015 | binding-and-lifecycle C-13, C-16 | FR-036 | command-family-and-declarations C-73, C-74 |
| FR-016 | unified-archive-and-migration C-41, C-42 | FR-037 | command-family-and-declarations C-75, C-76 |
| FR-017 | unified-archive-and-migration C-43, C-44 | FR-038 | binding-and-lifecycle C-30 |
| FR-018 | unified-archive-and-migration C-45, C-46 | FR-039 | owner-rewrites-and-tests C-92, C-93 |
| FR-019 | unified-archive-and-migration C-47, C-48 | FR-040 | owner-rewrites-and-tests C-94, C-95 |
| FR-020 | command-family-and-declarations C-89 | FR-041 | owner-rewrites-and-tests C-96 |
| FR-021 | binding-and-lifecycle C-17 | FR-042 | owner-rewrites-and-tests C-97 |

Count: 42 map rows, 42 distinct FR ids — every requirement reaches at least one clause.

## Measurement map — SC → red-first module

| SC | Measurement surface | Primary test module (red first) |
|---|---|---|
| SC-001 | a write to any `.specify/specs/*/goal` or `team` path is refused by the engine | `tests/contract/test_command_run_goal_team.py` |
| SC-002 | every engine write path reports its binding record | `tests/contract/test_no_spec_local_writes.py` |
| SC-003 | after migration the residual count is 0 while every source tree stays readable under `trees/` | `tests/integration/test_archive_migration_real_data.py` |
| SC-004 | a second migration run performs no write and never overwrites on conflict | `tests/contract/test_archive_migration.py` |
| SC-005 | the writability function returns an explicit verdict; neither line requires the other | `tests/integration/test_parallel_lines.py` |
| SC-006 | the three-way keys resolve in both directions across `handoff.md` and the definitions | `tests/contract/test_handoff_contract.py` |
| SC-007 | a crew write onto a spec artifact is refused; a writeback record is accepted | `tests/contract/test_handoff_territory.py` |
| SC-008 | the command family is a closed set and an unregistered carrier is refused | `tests/contract/test_criterion_vocabulary_scan.py` |
| SC-009 | a rebind changes ownership only; the file-minus-binding hash is unchanged | `tests/contract/test_binding_model.py` |
| SC-010 | the 085 temporary hierarchy and vocabulary are gone; the disposal table is measured | `tests/contract/test_085_disposal_table.py` |
| SC-011 | an interrupted migration resumes; no new failing id appears against the serial baseline | `tests/contract/test_migration_interruption.py` |

Count: 11 map rows, 11 distinct SC ids. Each module is added by `/speckit.implement` in red-first order; the module names
above are the plan's allocation and are pinned by `contracts/owner-rewrites-and-tests.md` C-109; the plan does not
restate them a second time.

## 085 disposal

The 085 temporary goal/team concept is superseded, not deprecated: the 11 affected test modules are disposed per
`contracts/owner-rewrites-and-tests.md` C-98…C-104 — each is either *rewritten* to the binding model, *removed* because
its subject no longer exists, or *retained as historical* with a pointer to this feature. No module is kept green by
weakening its assertion; the measured disposal list (11 modules, one with none of the affected surfaces) is recorded in
that clause range and must be re-measured, not re-derived, by `/speckit.implement`.

## Disclosed rulings made in this stage

Each was adjudicated in place rather than escalated, per the unattended-run instruction; each is recorded where it
binds, not only here.

1. `spec` leaves the archive-scope value domain — recorded in plan.md T-004 and C-9.
2. Handoff creation timing is derived from one declared fact, not from two independent settings — plan.md T-006.
3. Migration is an explicit command, never implicit on read — plan.md T-007 and C-45.
4. Pre-analyze advisory "`.specify/templates/commands/` retired" is a known landing-point fact, ruled non-blocking in
   plan.md § Complexity Tracking.
5. The `binding` read action and the `command-family` read action are new; neither rewrites `flow-class-check.py` — C-10,
   C-85.
