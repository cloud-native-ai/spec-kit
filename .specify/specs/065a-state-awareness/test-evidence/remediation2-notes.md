# Remediation Round 2 Notes — 065a-state-awareness

**Date**: 2026-10-22
**Scope**: analyze round-2 findings C-01, N-01, I-04, I-05, N-03, N-04.

## N-02 — pre-analyze `clauses` field divergence

`pre-analyze-check.py` reports `"clauses": 0` for the canonical `C-N` contract form, while `account-clause-coverage.py` reports `claimed clauses 60`. The accountant is authoritative for clause coverage; the pre-analyze `clauses` field MUST NOT be used as coverage evidence. No framework script was modified in this remediation.

## Applied changes

- **C-01**: slice FR-043 now excludes the derived mapping table (FR-004) from the owner reference's ownership scope and allows mirror/pointer only; parent FR-004 now states "本表由本条拥有" and treats the reference and code as mirrors; `research.md` R-13 now says "镜像 derived 映射（owner 为 FR-004）"; `plan.md` source tree wording no longer implies table ownership; T003 adds a parse-based owner-claim assertion across slice requirements, parent requirements, research, plan, reference and code.
- **N-01**: action-matrix row 6 narrowed to `loop_state=DONE ∧ commits.value_state=unknown`; C-46/C-57/research/plan wording aligned; rows 8–10 explicitly excluded for `STALLED`/`REENTRY_REQUIRED` so those states reach row 11; T007/T015 add terminal-state + complete-artifacts + unknown-baseline tests.
- **I-04**: Edge Case at `requirements.md:126` now limits parent C-area priority to non-stale forms; stale forms follow SA-1/C-43 (`stale-unisolated → stop` belongs to 065c).
- **I-05**: parent FR-004 flat `spine_consistent` replaced with nested `spine.consistent`.
- **N-03**: `data-model.md:265` marked "summary only; owner C-46"; `snapshot-envelope.md` C-23 marks the consistency criterion as summary only with owner C-39.
- **N-04**: C-54 now defines `artifacts.complete=null` + `artifacts.value_state=unknown` for an unknown `stage_base_commit` and excludes it from `false_completion`.

## Post-remediation validation

- `account-clause-coverage.py`: claimed clauses 60; FR claimed 25 / uncovered 0; status ok.
- `validate-tasks.py`: PASS, 0 errors, 0 warnings.
- `pre-analyze-check.py --stage tasks`: decision=pass, errors=0, advisories=42 (all expected missing implementation paths).
- `validate-requirements.py` (slice): 27 errors, all `id-contiguous` (documented waiver); other categories pass.
- `validate-requirements.py` (parent): status ok, 0 errors.
- SC-001…SC-006 all cited in contract citation groups.
