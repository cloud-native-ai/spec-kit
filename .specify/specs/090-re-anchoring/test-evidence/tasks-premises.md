# Implement-stage premises re-measured on the implement tree — 2026-11-09T23:45Z

T001. Section title as the implement stage's landing point for the task-generation premises
(table in `tasks.md` § Premises measured at generation time). Every row below was re-run on the
implement tree (HEAD `1a274860`, worktree clean apart from files outside this feature); the
generation-time reading is quoted beside it so a divergence is visible rather than averaged.

| Quantity | Implement-tree reading | Re-derivation actually executed | Generation-time reading |
|---|---|---|---|
| FR definitions | **10** | `account-clause-coverage.py --spec-dir .specify/specs/090-re-anchoring --json` → `fr.universe 10` | 10 |
| FR coverage from contract citation groups | **10 of 10**, `uncovered []` | same run → `fr.claimed 10`, `fr.uncovered []` | 10 of 10 (0 of 10 before the analyze repair) |
| Contract clauses in the four pages | **31** (8 / 9 / 6 / 8) | same run → `clause.claimed 31`; per-page id sets recorded in `sc002-ordering.txt` | 31 |
| Clause universe (whole corpus) | **1908** names, 288 files (`scanned` in the same JSON) | same run | 1908 |
| Guard modules this feature names | **4** | `ls tests/contract/test_{reanchoring_contract,sdd_loop_driver_reanchor,constitution_double_landing,fast_fail_discipline}.py` | 4 |
| Guard assertions today | **4 / 4 / 19 / 104 passed, 2 failed** → `2 failed, 129 passed` | `/usr/bin/python3 -m pytest <four modules> -q --tb=no -rA` @ 2026-11-09 | 2 failed, 129 passed |
| Ordering assertions in the tree today | **0** | `test_sdd_loop_driver_reanchor.py` holds 4 tests, none of them ordering (captured in `red-first-090-c7.txt`) | 0 |
| Constitution principles | template **21** (`XXI`), live **22** (`XXII`) | `grep -cE '^### [IVXLC]+\. ' templates/constitution-template.md` → 21; `.specify/memory/constitution.md` → 22 | 21 / 22 |
| Count pins | `TEMPLATE_COUNT = 21`, `LIVE_COUNT = 22`, `COMMAND_COUNT = 14`, watchlist **9** | `grep -nE '^(TEMPLATE_COUNT|LIVE_COUNT|COMMAND_COUNT) = ' tests/contract/test_constitution_double_landing.py`; watchlist last entry `"Re-Anchoring (不忘初心 · 温故而知新)"` | same |
| Instructions size vs budget | live **35 790 B** vs `INSTRUCTIONS_BUDGET_BYTES=37888` → **2 098 B** headroom | `wc -c .specify/instructions.md`; `grep -n INSTRUCTIONS_BUDGET_BYTES scripts/bash/generate-instructions.sh` → line 100 | same |
| Owner page size | **63** lines at entry to this stage | `wc -l shared/definitions/re-anchoring-definitions.md` | 63 |
| Mirror pairs this feature owns | **6** identity pairs, all byte-equal | `/usr/bin/python3 scripts/python/sync-mirrors.py --check` → exit 0 | same |
| Sibling coverage baselines | **26** spec dirs carry `coverage-baseline.txt` | `ls .specify/specs/*/coverage-baseline.txt \| wc -l` | 26 |
| Tasks rows | **39** lines carry a `- [ ]`/`[>]`/`[X]` sigil | see `derive-utils`-free reading in `closure-guards.txt` (39 rows, 31 claims, 4 pages) | 38 rows at generation, 39 after the analyze repair added T039 |

## Divergences recorded, not averaged

- **Owner page line count** — read 63 at stage entry, identical to the generation-time figure. The
  F-08 row then added the budget rule to § 3 and a quick re-read line to § 1.2, so a re-measurement
  after that edit reads 65; the growth is this stage's disclosed change, and `tasks.md` § Premises
  keeps the entry reading it was produced with.
- **Rows 39 vs 38** — the analyze repair added T039; `tasks.md` line 132 already states 39.
- Everything else is identical to the generation-time table, including the two pre-existing red
  guard tests (`test_fast_fail_discipline.py::test_i11_…`, `::test_g9_…`).
