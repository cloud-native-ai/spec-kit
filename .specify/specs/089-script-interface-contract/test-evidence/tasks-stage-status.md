# tasks stage — status record for 089-script-interface-contract

Recorded 2026-11-06 on branch `089-script-interface-contract` (base `780652a4`); the gate readings below were
re-measured in the design-repair pass of the same day (parent commit `5c2bb98f`). This file is the tasks-stage
evidence pointer: it names the artifacts, the gates that were actually run, and the current verdict of each.

## Artifacts produced this stage

| Artifact | Path | State |
|----------|------|-------|
| Task list | `.specify/specs/089-script-interface-contract/tasks.md` | written, 87 rows, validator exit 0 |
| Validator output | `test-evidence/tasks-validate.txt` | `PASS (with warnings)` — 0 error(s), 73 warning(s) |
| Decomposition result | `test-evidence/tasks-decomposition.json` | `proceed` (re-measured 2026-11-06 after `b6bb7356`) |
| Coverage baseline | `.specify/specs/089-script-interface-contract/coverage-baseline.txt` | frozen, 573 names; readings in `test-evidence/T004-coverage-freeze.txt` |

## Measured counts

- Task rows: **87** (`grep -cE '^- \[[ x>~]\] T[0-9]{3}' tasks.md`), ids dense `T001`…`T087` in row order.
- FR definitions in `requirements.md`: **31** (`^- \*\*FR-[0-9]{3}\*\*:`), ceiling **120** — passes.
- Contract clauses: **38** (`C-1`…`C-38`), each claimed exactly once by a `[green:]` attribution
  (verified: 38 claim strings, 38 distinct clause ids, zero duplicates).
- Success criteria: **12** (`SC-001`…`SC-012`), each named in the traceability table with at least one row.

Grouping: Phase 1 Setup T001–T005 (5) · Phase 2 Foundational T006–T011 (6) · Phase 3 US4 T012–T029 (18) ·
Phase 4 US5 T030–T066 (37) · Phase 5 US6 T067–T072 (6) · Phase 6 US1 T073–T075 (3) · Phase 7 US2 T076 (1) ·
Phase 8 US3 T077 (1) · Phase 9 Polish T078–T087 (10).

## Gates run

1. `python3 .specify/scripts/python/validate-tasks.py <tasks.md>` → exit **0** (0 errors, 73 warnings).
   Warnings are adjudicated in `tasks.md` § Notes: 66 `green-path-divergence` (12 rows legitimately write the one
   shared contract-test file), 4 `green-cross-phase` (structural: red-first tests, a later-priority phase, and the
   closure-time C-21 guard each own a clause whose ordinal is lower than a row that follows), 1 `parallel-safe` on
   the shared test file (first-writer row T012), 2 forward `blockedBy` (both intentional sequencing).
2. `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements
   requirements.md` → `proceed` (31 FR ≤ 120).
3. `… --mode tasks --requirements requirements.md --tasks tasks.md` → **`proceed`**, exit 0, measured
   `fr_count=31`, `task_count=87`, ceilings `120` / `160` (2026-11-06, `test-evidence/tasks-decomposition.json`).
   *Superseded record, kept for history:* at generation this gate read `split-required` with reason
   `task rows=87 exceeds ceiling 80`, exit 1, because the ceilings were then 60 / 80. Commit `b6bb7356` raised
   them to 120 / 160; the re-measurement above is the current verdict.

## Tests Mode

**ON** — Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating (measured
with `grep -nE 'MUST|MANDATORY|NON-NEGOTIABLE|Test-First|TDD|Contract-Driven' .specify/memory/constitution.md`).
Test rows precede the implementation rows they turn red, with the sanctioned migration exception for rows that
pin a count over surfaces that must exist first (T017, T026, T062, T063) — each carries `[blockedBy:]`.

## Open points handed forward

- No blocking gate: the decomposition verdict is `proceed` and the clause-coverage baseline exists.
- The three measurement discrepancies once recorded as `ANOMALY A-1`…`A-3` in `tasks.md` § Notes were repaired in
  this tree on 2026-11-06 (`plan.md` § Risks 9 and 11, `research.md` R7, `requirements.md` already corrected), so
  what remains in that section is a dated record, not an open item.
