# Tasks Stage Evidence — 109-prompt-adherence

**Run**: `r20261127T053750Z-109a` · **Stage**: `tasks` · **Date**: 2026-11-27
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/prompt-adherence` · **Branch**: `109-prompt-adherence` · **Baseline**: `224fd5a5c`

Every section below is a captured reading from this run; nothing is hand-scored. Test execution for this
stage is `not-run-docs-only` — the stage authors `tasks.md` and its evidence only; the guards it names are
implementation outputs.

## A-1 — Artifacts produced (paths, counts measured after writing)

| Artifact | Path | Count / scope |
|----------|------|---------------|
| Task list | `.specify/specs/109-prompt-adherence/tasks.md` | 39 task rows (T001…T039): Setup 3 / Foundational 5 / US1 8 / US2 6 / US3 4 / US4 3 / US5 3 / Polish 7; 6 `[P]` rows; 39 `[green:]` claims on 6 closure rows |
| Validator capture | `test-evidence/tasks-validator.txt` | `validate-tasks.py` verdict, verbatim |
| Decomposition capture | `test-evidence/decomposition-tasks.txt`, `test-evidence/decomposition-tasks.json` | `decomposition-check.py --mode tasks` verdict |
| Pre-analyze capture | `test-evidence/pre-analyze-tasks.txt`, `test-evidence/pre-analyze-tasks.json` | `pre-analyze-check.py --stage tasks` verdict |
| Workspace signature | `test-evidence/workspace-tasks.json` | snapshot before the artifact writes; check after the gates |

## A-2 — tests-mode decision

**Tests Mode**: ON — Constitution Principle IV「Test-First & Contract-Driven Implementation」is
test-mandating (`grep -nE 'MUST|MANDATORY|NON-NEGOTIABLE|Test-First|TDD|Contract-Driven'
.specify/constitution.md` matches its MUST lines), and this feature ships executable runtime code
(`scripts/python/prompt-adherence.py`), so the template-only exemption does not apply. New-behavior guards
are red-first; two guards over already-delivered behavior (US3 containment/init, US5 advisory-only legs)
are placed after their subjects under the migration/regression exception, declared inline on T023/T024/T030.

## A-3 — validate-tasks.py (verbatim, `test-evidence/tasks-validator.txt`)

```
PASS: .specify/specs/109-prompt-adherence/tasks.md — 0 error(s), 0 warning(s)
EXIT=0
```

The four green-point checks are clean: 39 clauses claimed exactly once, per-contract claim ordinals
monotonic in row order, no clause collision, no test-path green-point divergence (test-authoring rows
carry no claims).

## A-4 — decomposition-check.py --mode tasks (verbatim, `test-evidence/decomposition-tasks.txt`)

```
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 30, "task_count": 39, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": [], "checked_at": "2026-11-27T06:23:41Z"}
EXIT=0
```

## A-5 — pre-analyze-check.py --stage tasks (final run, summary)

```
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=127 waived=0
{"fr": 30, "sc": 9, "tasks": 39, "clauses": 39, "files": 14}
```

All 127 advisories are the single `missing-path` class, naming exactly the 14 deliverable paths this
feature creates (owner document and its installed form, the five fact files, the engine and its installed
form, the five guard files, the fixtures directory): 24 lines in `tasks.md`; the remainder are the same
paths cited by the upstream artifacts (requirements 10 / plan 5 / feature-ref 12 / contracts 54 /
quickstart 9 / research 2 / data-model 1). Zero error-class findings, zero waivers. Full capture:
`test-evidence/pre-analyze-tasks.txt` and `test-evidence/pre-analyze-tasks.json`.

## A-6 — Workspace guard

```
python3 scripts/python/workspace-guard.py --snapshot .specify/specs/109-prompt-adherence/test-evidence/workspace-tasks.json --repo .
recorded .specify/specs/109-prompt-adherence/test-evidence/workspace-tasks.json
EXIT=0

python3 scripts/python/workspace-guard.py --check .specify/specs/109-prompt-adherence/test-evidence/workspace-tasks.json --repo .
clean
EXIT=0
```

## A-7 — Coverage accounting (measured from the written file)

| Axis | Reading |
|------|---------|
| FR coverage | 30/30 — every FR-001…FR-030 named by at least one task row (§ Requirement Coverage Map) |
| SC coverage | 9/9 — every SC-001…SC-009 named; SC-004 and SC-008 have dedicated reading rows |
| Clause coverage | 39/39 — § Clause Coverage & Green Partition claims each clause exactly once across T016 (10), T026 (9), T033 (2), T034 (10), T035 (1), T038 (7) |
| Deliverable families | 11/11 — § Deliverable Coverage Map (engine, owner doc, five facts, five guard families, fixtures, framework-map rows, mirror pairs, distribution/init wiring, quickstart validation, evidence records, dated baseline) |
| Reading slots | targeted sets T-S1…T-S7 (T016/T021/T025/T026/T029/T030/T035) + the single full-suite slot F-1 (T038); implement-entry baseline owned by `/speckit.implement` § Test runs |

## A-8 — Green partition (per contract, measured from the file)

| Contract | Clauses | Row |
|----------|---------|-----|
| owner-and-catalog | C-001…C-007 (7) | T026 |
| declarations-and-vocabularies | C-010…C-016 (7) | T016 |
| engine-and-read | C-030…C-032 (3) | T016 |
| engine-and-read | C-034, C-036 (2) | T026 |
| reading-semantics | C-020…C-029 (10) | T034 |
| distribution | C-033, C-035 (2) | T033 |
| distribution | C-037 (1) | T035 |
| guards-and-boundaries | C-040…C-046 (7) | T038 |

## A-9 — Measured premises (generation-time re-measurement, 2026-11-27)

Recorded in `tasks.md` § Measured Premises with command and real output: FR/SC 30/9; clause definition
lines 7/7/10/5/3/7 = 39 with the naive-reference trap (46) named; 15 deliverable paths ABSENT; mirror and
command-copy baselines rc 0; instruction-section counts 39/40; store roster 14 stores with no `root` key;
probe registry 11 classes / 130 objects; six read-surface functions and their line pointers; interpreter
`/usr/local/bin/python3` 3.11.11 + pytest 8.4.2 with PATH `python3` lacking pytest and no worktree
`.venv`; runner probe with `SPECKIT_PYTHON` overriding → `7 tests collected` exit 0 vs without → exit 1
`no interpreter with pytest found`; Feature 109 index/detail both `Planned`.

## A-10 — Port adaptations from source 092 (disclosed)

The task set follows the source's phase shape with three tree-grounded adaptations, each recorded in the
task text:

1. **Mirror projection is one Polish row (T033), after every framework-source edit.** The source projected
   mirrors in US3 and then edited the engine again in US4/US5, which would leave drift for the final
   `--check`. Here the single projection follows all source edits; the criterion stays "no NEW drift on
   the touched pairs against the measured baseline".
2. **The init fixture asserts inventory only (no mirror-parity leg).** C-037 assigns the init test the
   artifact-inventory scope; mirror parity is carried by T033's `sync-mirrors.py --check`, so the init
   fixture does not depend on projection order.
3. **The readonly guard's longitudinal complement leg lands red-first with T027.** C-041 requires
   complement assertions after both reading forms; US3 closes the per-run leg, US4 adds the longitudinal
   leg before its implementation, and the clause is certified at T038.

The self-location "both copies" leg is proven with a scratch `.specify/scripts/python/` copy plus a
framework-source copy (T010), so it does not depend on the real mirror projection either.

## A-11 — In-passing corrections (disclosed)

1. A one-off probe capture was written to the bare system temp file `/tmp/noenv.out` and deleted in the
   same command (to capture the runner's real exit code through a pipeline). No residue remains; all later
   evidence writes target the spec's `test-evidence/` directory.
2. The source's `tests/integration/test_decision_governance_init.py` pattern does not exist in this tree;
   T024 names the real sibling form `tests/integration/test_init_new_layout.py` (existence-checked), while
   keeping the `copy_local_templates` + `get_resource_path` helpers that do exist in `src/specify_cli/`.

## A-12 — Test execution

`not-run-docs-only` — this stage authors `tasks.md` and its evidence only. The guards it names are
implementation outputs; the implement stage captures the full-suite baseline once through
`scripts/bash/run-tests.sh` (owner: `/speckit.implement` § Test runs) and the single full-suite reading at
T038 (slot F-1).

## A-13 — Concurrency record

`requested=1`; `effective=not_evaluated`; `effective_reason=single-unit`. The representable unit set has
size 1: the executor role forbids dispatching other agents and the driver partitioned the tasks stage as
one serial work package. Reason code `single-unit` read from `shared/declarations/facts/serial-reason.yaml`;
no dispatch intervals were produced.

## Anomaly line

未发现异常（in-passing corrections disclosed in A-11）。