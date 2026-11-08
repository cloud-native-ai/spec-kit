# Package 3b stage status — 089-script-interface-contract (T042–T049, checker CLI and report faces)

**Scope**: Phase 4 US5 CLI/report band (T042–T049). Eight rows in `scripts/python/script-interface-check.py` plus its pins in `tests/contract/test_script_interface_contract.py`.
**Tree**: `/cws_data/cloud-native-ai/spec-kit`, branch `089-script-interface-contract`, parent `b5585cb4`.
**Run**: 2026-11-07, implement stage, package 3b.

## 1. Per-task completion

| Task | Status | Landing point | Evidence |
|---|---|---|---|
| T042 | done | engine header/tail: shebang, docstring with usage + exit codes, `from __future__ import annotations`, `main(argv=None) -> int`, `sys.exit(main())`, `REPO_ROOT`, sorted `candidates[]`, no write in the measured tree, own `--help`/`--version` green | `test_c14_the_engine_has_the_sibling_engines_shape`, `test_c14_the_engine_answers_its_own_two_flags`, `test_c15_the_engine_writes_nothing_inside_the_repository` |
| T043 | done | `build_parser()`: `--root --json --files --emit-rule --skip-probe --sandbox --budget-seconds --check-projection`; `--emit-rule` + `--files` exit 2 | `test_c16_the_argument_surface_and_its_one_combination_error` |
| T044 | done | `exit_code(report)`: 1 on any violation or unresolved finding, else 0; exit 2 only from the argument/environment branches | `test_c17_the_exit_code_is_derived_from_the_report` |
| T045 | done | `build_report()` / `_base_report()` / `_normalise_rows()`: schema/mode/source/root, four counts, `elapsed_ms`, five arrays with every required row field | `test_c18_*` (two rows) |
| T046 | done | `_emit()`: one `<path>: <missing limbs>` line per violation, one line per unresolved finding, always the `candidates=N applicable=N exempt=N violations=N` summary | `test_c19_the_human_face_prints_violations_and_always_the_summary` |
| T047 | done | determinism pins: two `--json` runs differ only in `elapsed_ms`, no write inside the repository, `REPO_ROOT` resolves the mirror copy to its own root | `test_c20_two_runs_differ_only_in_elapsed_ms`; red-first in `T047-red.txt` |
| T048 | done | `classification_rule()`: eight keys from the same module-level constants table the classifier executes | `test_c21_*` (two rows) |
| T049 | done | `check_projection()` / `projection_rows()` / `project_source()`: mirror == source + declared projection, idempotent, mismatch names the pair and exits 1 | `test_c22_*` (two rows); live reading in `T042-T049-readings.txt` |

T041's `projection-mismatch` leg is green in this package.

## 2. Readings

| Command | Reading |
|---|---|
| `pytest tests/contract/test_script_interface_contract.py -q` | 55 passed in 13.02s (41 at entry, 14 new) |
| `sync-mirrors.py --write` then `--check` | one file synced; every pair `ok`, exit 0 |
| `--json` twice, `--skip-probe` | keys equal, `/elapsed_ms` the only differing path; 743 candidates, 0 exemptions, 0 violations |
| `--json` twice, probed subset on `scripts/python/sync-mirrors.py` | equal minus `elapsed_ms`; both exit 1, `applicable=1 exempt=0 violations=1` |
| `--check-projection --root .` twice | exit 0, `projection []`, byte-identical output |

The empty `projection[]` is the honest C-22 reading now: `PROJECTED_FILES` is T050's landing.

## 3. Corrections repaired in passing

1. Probing runs were not actually deterministic and the C-20 pin could not see it: run 2 captured run 1's leftover sandbox, and the candidate re-projected inside it. `_capture_tree` now omits git-ignored paths (`git check-ignore --stdin`) and symlinks; `_fingerprint` skips symlinks. No verdict changed.
2. `ignored-not-probed` listed the engine's own sandbox leftovers. `_normalise_rows` drops every path under `SANDBOX_ROOTS` from `findings[].paths` and sorts that list and `candidates[]`.
3. The engine's own `--help` lacked `side-effects:`/`exit-codes:`; added via `OWN_HELP_EPILOG`.
4. `--emit-rule` without `--json` crashed on empty stdout; it now prints the same JSON object either way (C-16).

## 4. Anomalies surfaced (decisions taken; no contract edited)

- `ANOMALY C-1` — C-21's shared declaration vs C-22's exit-1-on-mismatch. Implemented as `--emit-rule` → declaration as read, `--check-projection` → verdict; one row type, two faces.
- `ANOMALY C-2` — C-12 names no bucket for an unevaluated candidate; filed as a violation naming the basis limb plus a finding, never an exemption.
- `ANOMALY C-3` — `exceptions[].recomputed` is `false` by construction; the recomputation is T069's.
- `ANOMALY C-4` — C-29 and C-14 touch: the engine's help renders the surface, it does not define the label set.
- `ANOMALY C-5` — the brief's audit invariant has no locatable owner text; implemented as one row shape per candidate with explicit `probe` state.

## 5. Scope discipline

Writes: the engine, its contract test file, the projection of the engine (by `sync-mirrors.py --write`), `tasks.md` (T042–T049) and this evidence folder. Untouched: requirements/plan/contracts/data-model, US4 landing files, other `scripts/python/` scripts, `.specify/scripts/**` by hand, and the dirty `081` smoke file. No push.
