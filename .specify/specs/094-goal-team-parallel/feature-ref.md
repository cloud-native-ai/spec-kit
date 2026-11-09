# Feature Reference — 094-goal-team-parallel

**Feature**: goal/team binding × spec parallelism (临时/全局概念重定义 + 归档统一 + 施工队并行)
**Spec directory**: `.specify/specs/094-goal-team-parallel/`
**Binding**: `spec:094-goal-team-parallel`; `flow_class=execution` (registered declaration, not inferred)
**Delivery surface**: engine `scripts/python/goal-utils.py` (extended), declaration facts under
`.specify/shared/declarations/facts/`, the sdd-loop driver skill, the `/speckit.goal` `/speckit.team` `/speckit.feedback`
command templates, the framework map, and the 085 test set.
**Authority**: `requirements.md` (43 FR, 12 SC, Clarifications Q1–Q14, Assumptions A1–A11) is the intent owner; the
contracts below are the conformance owner; `plan.md` is the design owner. This page restates no rule — it maps.

## Delivery map — FR → contract clause

| FR | Clause | FR | Clause |
|---|---|---|---|
| FR-001 | C-1, C-2, C-3, C-4 | FR-023 | C-18 |
| FR-002 | C-1, C-2, C-3, C-4, C-30 | FR-024 | C-88, C-89, C-90, C-92 |
| FR-003 | C-1, C-2, C-3, C-4, C-5, C-6, C-59 | FR-025 | C-9, C-10, C-11, C-13, C-29 |
| FR-004 | C-1, C-2, C-3, C-4 | FR-026 | C-7, C-17, C-18, C-19, C-20, C-28 |
| FR-005 | C-71, C-72, C-75 | FR-027 | C-16, C-91, C-92 |
| FR-006 | C-71, C-72, C-74 | FR-028 | C-21, C-22, C-23, C-24, C-93, C-94, C-95, C-96 |
| FR-007 | C-13, C-31, C-44, C-46, C-47 | FR-029 | C-48, C-100, C-101 |
| FR-008 | C-9, C-10, C-11, C-12, C-13, C-29 | FR-030 | C-45, C-50, C-97, C-98, C-101 |
| FR-009 | C-32, C-33, C-35, C-36, C-38, C-39, C-40, C-50 | FR-031 | C-74, C-76, C-77, C-78, C-79, C-80, C-81, C-82, C-83, C-84, C-85, C-86, C-87 |
| FR-010 | C-32, C-33, C-34, C-35, C-37, C-39 | FR-032 | C-108 |
| FR-011 | C-40, C-41 | FR-033 | C-104, C-108, C-109, C-110, C-111 |
| FR-012 | C-43, C-44, C-45 | FR-034 | C-58, C-59, C-60 |
| FR-013 | C-46, C-47, C-106, C-108 | FR-035 | handoff-contract#C-53, handoff-contract#C-54, C-55, C-56, C-57, C-68, C-69, C-70 |
| FR-014 | C-25 | FR-036 | C-15, C-61, C-62, C-63, C-64 |
| FR-015 | C-8, C-26 | FR-037 | C-49, C-107 |
| FR-016 | handoff-contract#C-53, handoff-contract#C-54, C-55, C-56, C-57, C-58, C-59, C-60, C-61 | FR-038 | C-14, C-15, C-16, C-26 |
| FR-017 | C-64 | FR-039 | C-68, C-69, C-70, C-80, C-81 |
| FR-018 | C-79, C-80, C-81 | FR-040 | C-73, C-99 |
| FR-019 | C-62, C-67 | FR-041 | C-102, C-103, C-104, C-105 |
| FR-020 | C-65, C-66, C-67 | FR-042 | C-42, C-51, C-52 |
| FR-021 | C-27 | FR-043 | unified-archive-and-migration#C-112, unified-archive-and-migration#C-113 |
| FR-022 | C-107, C-108 | | |

Count: 43 FR entries across 22 physical table rows (two FR cells per row), 43 distinct FR ids — every
requirement reaches at least one clause. `page#id` cells anchor the four clause ids that were page-ambiguous
before the D1 renumber (`handoff-contract#C-53` / `#C-54` on FR-016 and FR-035; the archive-page backfill
clauses are `unified-archive-and-migration#C-112` / `#C-113` on FR-043).

**This table is generated, not authored.** It is the deterministic export of the contracts' own citation
groups; regenerate it (never hand-edit a cell) with:

```
python3 - <<'EOF'   # run from the repo root; same 22-row/two-column layout
import sys; sys.path.insert(0, '.specify/scripts/python')
import clause_extract as ce, glob
files = sorted(glob.glob('.specify/specs/094-goal-team-parallel/contracts/*.md'))
ANCHOR = {('handoff-contract', 'C-53'), ('handoff-contract', 'C-54'),
          ('unified-archive-and-migration', 'C-112'), ('unified-archive-and-migration', 'C-113')}
fr = {}
for f in files:
    page = f.rsplit('/', 1)[-1][:-3]
    for cid, frs in ce.clause_citations(f).items():
        for x in frs:
            fr.setdefault(x, []).append((page, cid))
for x in sorted(fr):
    cells = [f'{p}#{c}' if (p, c) in ANCHOR else c
             for p, c in sorted(fr[x], key=lambda pc: int(pc[1].split('-')[1]))]
    print(x, cells)
EOF
```

The snippet sorts each FR's clause list by clause number, so regeneration reproduces both membership and
column order on all 22 rows; the four `page#id` cells are emitted through the `ANCHOR` set. An earlier
revision printed in contract-file order and therefore differed on five rows in order only (FR-013, FR-029,
FR-030, FR-037, FR-039); membership was identical on both sides — membership is the invariant, order is not.

`clause_extract.py` is the executable counterpart of
`.specify/shared/definitions/contract-clause-definitions.md` § 4: a clause cites FRs through the **last
FR/SC-bearing parenthetical in its block**, inline code spans stripped. The map therefore changes only when a
clause's citation group changes — which is exactly when a reader needs to see it change.

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
| SC-012 | every `.specify/goal/*/goal.md` and `.specify/teams/*/team.md` resident carries a complete `binding` record after `backfill-bindings`, and a second run writes nothing | `tests/contract/test_resident_backfill.py` |

Count: 12 map rows, 12 distinct SC ids. Each module is added by `/speckit.implement` in red-first order; the module names
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
