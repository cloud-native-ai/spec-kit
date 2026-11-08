# Verification — 089-script-interface-contract

| SC | Path | Status | Evidence |
|----|------|--------|----------|
| SC-001 | final | **pass** | `test-evidence/SC-001-zero-side-effect.txt` — contained per-family harness: 749 candidates / 16 families / 0 moved snapshot pairs |
| SC-002 | final | **pass** | `test-evidence/SC-002-incident-script.txt` — `generate-instructions.sh` flags leave `.specify/instructions.md` and `.gitignore` byte-identical; unknown option exits 2 |
| SC-003 | final | **pass** | `test-evidence/closure-check.json` — 751 candidates, **0 violations**, 737 exemptions (453 pytest-module, 140 inherited-from-source, 120 optional-read-only, 9 no-entry-point, 8 historical-record, 4 declared-exception, 3 out-of-scope), 2 declared exceptions recomputed, the only finding is the resolved `ignored-not-probed` |
| SC-004 | final | **pass** | `test-evidence/SC-004-downstream.txt` |
| SC-005 | supporting | **pass** | `test-evidence/SC-005-constitution-diff.txt` |
| SC-006 | final | **pass** | `test_constitution_double_landing.py` (19/20/12 + watchlist 7) and `test_fast_fail_discipline.py` pins |
| SC-007 | supporting | **pass** | `test-evidence/SC-007-zero-regression.txt` + the `common.sh` publication fix (`22d5e84b`, paths-only output restored) |
| SC-008 | final | **pass** | `test-evidence/SC-008-mutation.txt` — mutant exits 1 naming the path; control green |
| SC-009 | final | **pass** | `test-evidence/SC-009-candidate-coverage.txt` |
| SC-010 | final | **pass** | `test-evidence/SC-010-classification-mutants.txt` |
| SC-011 | supporting | **pass** | `test-evidence/SC-011-version-source.txt` |
| SC-012 | final | **pass** | `test-evidence/SC-012-declared-exceptions.txt` |

deferred_tasks: T081 (registry/status flip) and T086 (closure full-suite comparison) remain; T080/T083/T087 are done

smoke_command: `/usr/bin/python3 -m pytest -q tests/contract/test_script_interface_contract.py tests/contract/test_sdd_loop_driver_efficiency.py tests/contract/test_help_body_preservation.py tests/unit/test_create_new_requirements_separator.py tests/unit/test_workspace_guard.py`
smoke_exit_code: 0
smoke_evidence_path: `.specify/specs/089-script-interface-contract/test-evidence/pkg-p7-stage-status.md`

## SC-003 blocker (one decision, not a correction)

`tests/**` candidates cannot reach `violations=0` under the current spec:

- The clarification (Q3) says test modules are **applicable** and must be backfilled or registered as exemptions. Backfilling pytest modules with `--help/--version` is meaningless; the declared-exception register only accepts `skills/external/<skill>/` scripts, so `tests/**` cannot be registered there either.
- Measured: 453 of the 488 violations are under `tests/**`; 361 are `probe-inconclusive` (importing a pytest module without pytest context), 92 are missing help/version limbs.

The three viable dispositions, for the user to ratify:

1. **Adopt a `pytest-module` exemption (recommended)** — a Python file that imports `pytest` (or defines `test_*` functions) and whose direct execution cannot act is exempt by run semantics, with a named `basis` and evidence; the 6 files carrying a real `__main__` action plus `conftest.py` are judged individually (T083). This matches C-4's run-semantics criterion and makes SC-003 reachable without absurd edits.
2. **Backfill test modules** — add `--help/--version` to 453 pytest modules; rejected as a semantic absurdity.
3. **Narrow SC-003** — restrict the candidate surface to `scripts/`, `skills/`, `install.sh` and exclude `tests/**` by an explicit scope change; a requirements amendment.

The remaining ~35 non-test violations are separable and mostly corrections: `src/specify_cli/**` is out of scope (requirements Out of Scope) and needs a named exclusion; `.specify/specs/*/notes/**` are dated historical records (A9) and need a `historical-record` basis; mirror duplicates should inherit their source class (C-6); the real gaps are `regen-command-copies.py`, `workspace-guard.py` (pre-parse unknown rejection), `query_mysql.py` (pre-import help), `build-summary-input.py`, `verify-territory-disjoint.py`, `watch-target.sh` (`-h` body), `render-excalidraw.sh`, `render-plantuml.sh`, `install.sh`.
