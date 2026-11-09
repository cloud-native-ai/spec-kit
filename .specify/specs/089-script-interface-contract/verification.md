# Verification — 089-script-interface-contract

| SC | Path | Status | Evidence |
|----|------|--------|----------|
| SC-001 | final | **pass** | `test-evidence/SC-001-zero-side-effect.txt` — contained per-family harness: 749 candidates / 16 families / 0 moved snapshot pairs |
| SC-002 | final | **pass** | `test-evidence/SC-002-incident-script.txt` — `generate-instructions.sh` flags leave `.specify/instructions.md` and `.gitignore` byte-identical; unknown option exits 2 |
| SC-003 | final | **pass** | `test-evidence/closure-check.json` — 751 candidates, **0 violations**, `applicable=367` plus 737 exemptions (453 pytest-module, 140 inherited-from-source, 120 optional-read-only, 9 no-entry-point, 8 historical-record, 4 declared-exception, 3 out-of-scope), 2 declared exceptions recomputed, the only finding is the resolved `ignored-not-probed`; the two counts are NOT disjoint (`exempt` counts `exemptions[]` rows, 353 of which are also `applicable`), so the recomputable partition is `applicable + violations + (candidates − applicable − violations)` and **the identity `applicable + exempt == candidates` is void by construction** — see the re-measurement below <!-- 092 handoff: E4 --> |
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

**Count-identity re-measurement (2026-11-09)** — the identity the DoD/GATE rows used to state is void by construction, not merely unheld on this tree, so it is replaced by a recomputable partition. Measured on `test-evidence/closure-check.json`: `candidates=751`, `applicable=367`, `exempt=737`, `violations=0`. `367 + 737 = 1 104 ≠ 751`. <!-- 092 handoff: E4 -->

The cause is mechanical: `applicable` counts `candidates[]` rows whose `applicable is True` (367) while `exempt` is `len(exemptions[])` (737), and the two sets are **not disjoint** — 353 of the exempted paths are also applicable candidates. Summing them therefore double-counts, and no tree on which any exemption is also applicable can satisfy the identity; the "surplus" is two overlapping classifiers, not a miscount. The recomputable statement is the accounting itself: `applicable` equals the number of `candidates[]` rows with `applicable is True`, `exempt` equals `len(exemptions[])` (every one of those paths a candidate), and no candidate falls outside `applicable` ∪ `exemptions[]` ∪ `violations[]` — on this payload the union covers all 751 with `violations=0`, and 384 candidates are not applicable while all 384 are exempted. That check replaces the identity in DoD-3 / GATE-5; the checker engine's own count semantics are untouched. <!-- 092 handoff: E4 -->

The three viable dispositions, for the user to ratify:

1. **Adopt a `pytest-module` exemption (recommended)** — a Python file that imports `pytest` (or defines `test_*` functions) and whose direct execution cannot act is exempt by run semantics, with a named `basis` and evidence; the 6 files carrying a real `__main__` action plus `conftest.py` are judged individually (T083). This matches C-4's run-semantics criterion and makes SC-003 reachable without absurd edits.
2. **Backfill test modules** — add `--help/--version` to 453 pytest modules; rejected as a semantic absurdity.
3. **Narrow SC-003** — restrict the candidate surface to `scripts/`, `skills/`, `install.sh` and exclude `tests/**` by an explicit scope change; a requirements amendment.

The remaining ~35 non-test violations are separable and mostly corrections: `src/specify_cli/**` is out of scope (requirements Out of Scope) and needs a named exclusion; `.specify/specs/*/notes/**` are dated historical records (A9) and need a `historical-record` basis; mirror duplicates should inherit their source class (C-6); the real gaps are `regen-command-copies.py`, `workspace-guard.py` (pre-parse unknown rejection), `query_mysql.py` (pre-import help), `build-summary-input.py`, `verify-territory-disjoint.py`, `watch-target.sh` (`-h` body), `render-excalidraw.sh`, `render-plantuml.sh`, `install.sh`.

# -- Machine-readable (closure) --
#
# Projection of the two tables above into the key=value carrier that
# `closure-acceptance-check.py` reads (owner: `shared/workflow/acceptance-hardening.md`
# § Verification Vocabulary). Values are copied from the rows above and from the smoke
# record at the top of this file; the tables above stay the authored record.

smoke_command=/usr/bin/python3 -m pytest -q tests/contract/test_script_interface_contract.py tests/contract/test_sdd_loop_driver_efficiency.py tests/contract/test_help_body_preservation.py tests/unit/test_create_new_requirements_separator.py tests/unit/test_workspace_guard.py
smoke_exit_code=0
smoke_evidence_path=.specify/specs/089-script-interface-contract/test-evidence/pkg-p7-stage-status.md

SC-001_status=pass
SC-002_status=pass
SC-003_status=pass
SC-004_status=pass
SC-005_status=pass
SC-006_status=pass
SC-007_status=pass
SC-008_status=pass
SC-009_status=pass
SC-010_status=pass
SC-011_status=pass
SC-012_status=pass

RS-003_joint_acceptance=state consistency is red on an Implemented-but-block copy tree and green when they agree
RS-004_joint_acceptance=the disposition vocabulary bridge is compared once against the sanitize ledger
RS-005_joint_acceptance=one sharded review dispatch stays within the declared concurrency and its union covers the candidates
