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
| SC-001 | a fixture with no SDD spec directory: a command run's goal and team land under `.specify/anchoring/` and `.specify/teams/`, `.specify/specs/` gains zero new paths, and the check turns red when a write path is reverted to a spec subdirectory. R2 (2026-11-09): the criterion is `supporting` — its named module is absent and acceptance delegates to SC-004 / SC-005 | `tests/contract/test_command_run_goal_team.py` (absent on this tree; no new guard under R2 — see `requirements.md` § Clarifications) |
| SC-002 | zero code paths write a goal or team tree under `.specify/specs/<spec>/`, asserted surface-by-surface over the engine's writing actions, `create-team`'s persistence step and the driver instructions; the assertion turns red when any write is reverted to the old path | `tests/contract/test_no_spec_local_writes.py` |
| SC-003 | on this repo's real data: the dry-run readings are decidable, every migrated slug exists in the unified archive, the residual probe balance is zero, and no source data is deleted (per-definition existence assertions) | `tests/integration/test_archive_migration_real_data.py` |
| SC-004 | two consecutive migrations of one tree: the second writes nothing with a decidable exit code; an existing target slug with non-equivalent content is refused, naming both candidates; both fixtures turn green | `tests/contract/test_archive_migration.py` |
| SC-005 | two peer fixtures — SDD-only with no goal/team (a below-threshold handoff decision) and goal+team-only with no spec — each complete one delivery; injecting a "requires the other line" precondition turns the test red; the fixture proves "does not need the other" by decision, never by skipping creation | `tests/integration/test_parallel_lines.py` |
| SC-006 | a spec above the complexity threshold produces a `handoff.md` whose `goal_slug` and `team_slug` resolve three ways against `.specify/anchoring/<slug>/goal.md` and `.specify/teams/<slug>/team.md` (bidirectional key pairs); a spec below the threshold is not required to produce one; an illegal or deleted threshold declaration turns the test red | `tests/contract/test_handoff_contract.py` |
| SC-007 | after construction every task status arrives on the spec side through writeback and is verifiable; a crew attempt to write `tasks.md` / `requirements.md` / `verification.md` directly is refused by the `territory.forbidden` surface, evidenced by exit code and refusal text | `tests/contract/test_handoff_territory.py` |
| SC-008 | no classification use of the retired 临时/全局 vocabulary on the runtime surfaces (`.specify/shared/`, `.specify/skills/`, `.specify/scripts/`, `templates/`, `skills/`, `scripts/`); hits are allowed only in dated records, migration receipts and this spec; a re-injected phrase turns the scan red (synthetic mutation, no tree edit) | `tests/contract/test_criterion_vocabulary_scan.py` |
| SC-009 | the same goal definition keeps its bytes and path when its binding changes (owner from a command run to a team of an SDD run); ownership is answered only by the binding record; a position-inferred ownership mutant turns the test red | `tests/contract/test_binding_model.py` |
| SC-010 | every existing case pinning a spec-local landing point carries a disposal record (rewrite / remove / mark historical; removal only where the asserted fact was deleted), and the whole contract suite is green on `>=3.8` after disposal; an undisposed item turns the test red | `tests/contract/test_085_disposal_table.py` |
| SC-011 | an interrupted migration at "source moved into the archive, target not yet written" reports that step on the second call and completes it, with source data and receipts enumerable and no second move; making the second call re-move or silently succeed turns the test red | `tests/contract/test_migration_interruption.py` |
| SC-012 | after `backfill-bindings`, every `.specify/anchoring/*/goal.md` and `.specify/teams/*/team.md` definition carries a complete `binding` record (`owner` / `owner_id` / `origin`), and a second run writes nothing; restricting the backfill to this feature's new definitions, or deleting one resident's binding line, turns the test red | `tests/contract/test_resident_backfill.py` |

Count: 12 map rows, 12 distinct SC ids. The description cells are projections of `requirements.md` § Success
Criteria — the criteria own the text, this table restates no rule of its own. SC-001's named module does not
exist on this tree: ruling R2 (`requirements.md` § Clarifications, 2026-11-09) records the delegation to
SC-004 / SC-005 and the criterion is `supporting` with status `partial`. Each remaining module is added by
`/speckit.implement` in red-first order and is pinned by `contracts/owner-rewrites-and-tests.md` C-109; the
plan does not restate the names a second time.

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
