# Part E2 — Fold Batch 3 Recheck (T022) — 2026-10-22

Dated record for implement part E2 of spec 067 (T022, fold batch 3 = candidate
scan entries 25–36 of `mirror-parity-candidates-2026-10-22.txt`). Every number
below is measured from the command in § Command log; nothing claims an
unexecuted run.

## What folded

- 12 candidate functions in 10 files; 9 pure folds (whole function removed) +
  3 extra-assertion cases where only the redundant byte-compare was removed:
  - `test_summarize_project_prompt_assets.py::test_mirror_is_byte_equivalent`
    (2 params) — tree file-set equality retained (lenient skills pairs keep
    ORPHANs note-only in the suite, so this pin is suite-uncovered).
  - `test_trigger_seed_derivation.py::test_c1_seed_exists_and_mirror_is_byte_identical`
    — seed JSON validity retained (same id).
  - `test_user_facing_comprehension_section.py::test_c2_mirror_carries_the_section_and_is_byte_identical`
    — heading-exactly-once + STR-001 pointer in the mirrored section retained
    (same id).
- The excluded wide hit `test_feedback_probe_cli.py::test_map_is_deterministic_byte_identical`
  (engine-map determinism, no mirror) stays untouched, per the E1 scan ruling.
- Ledger: rows 70–81 appended to `test-evidence/test-consolidation-ledger.md`
  (12 rows = 12 batch-3 candidate functions; every cited suite param id was
  verified present via `--collect-only` before the rows were written). Commit
  column = `pending`, backfilled at part close (E1 pattern).

## Targeted recheck (verbatim)

`bash scripts/bash/run-tests.sh tests/contract/test_mirror_parity_suite.py
<10 batch-3 touched files> -q --durations=0`
→ exit 1, **206 failed / 822 passed** (17.06 s).

- 202 of the failures are the known suite drift params (unchanged from the E1
  run-2 set; owned by T023 sync, not executed in this step).
- 4 non-suite failures, ALL in the in-stage baseline
  (`baseline-failures-2026-10-22-implement-start.txt` lines 60/68/76/78):
  - `test_self_improvement_conformance.py::test_c10_runtime_skill_mirrors_are_current`
  - `test_token_efficiency_discipline.py::test_cd5_headings_only_in_discipline_doc`
  - `test_trigger_engine.py::test_c2_sync_mirrors_check_clean`
  - `test_user_facing_comprehension_doc.py::test_gn_c2_gate_scan_total_unchanged`
- **0 new failures** attributable to the folds (FR-020: every remaining failure
  names its own drift pair or is an in-register baseline name). Suite
  collection total stays 723.

## Command log

1. `bash scripts/bash/run-tests.sh tests/contract/test_mirror_parity_suite.py
   tests/contract/test_self_improvement_conformance.py
   tests/contract/test_summarize_project_prompt_assets.py
   tests/contract/test_token_efficiency_discipline.py
   tests/contract/test_token_efficiency_feedback.py
   tests/contract/test_token_efficiency_gates.py
   tests/contract/test_trigger_engine.py
   tests/contract/test_trigger_seed_derivation.py
   tests/contract/test_user_facing_comprehension_doc.py
   tests/contract/test_user_facing_comprehension_pointers.py
   tests/contract/test_user_facing_comprehension_section.py -q --durations=0`
   → 206 failed / 822 passed (202 suite drift + 4 in-register baseline).
2. `... test_mirror_parity_suite.py --collect-only -q` (param-id verification
   for ledger rows 70–81): all cited params present; total 723 collected;
   summarize-project subtree = 24 params, study-project = 7.

Not run: full suite (slots owned by T007/T034); any `--write` sync (T023);
T024 re-verification.

## Residual risks

- Suite red on 202 params until T023 syncs — expected, in-register.
- `assert_dirs_byte_equivalent` in `tests/contract/helpers_prompt_assets.py`
  is now unused by tests (its caller folded to inline file-set equality);
  left in place as a generic helper — no test surface change.
