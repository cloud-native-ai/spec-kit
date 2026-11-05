# Review-stage targeted test evidence — 2026-11-05

stage_base=b2880fa0
review_stage=review (continuation)

## run 1 — the three modules this stage repaired/touches

$ python3 -m pytest tests/contract/test_fast_fail_discipline.py tests/contract/test_constitution_double_landing.py tests/contract/test_instructions_section_propagation.py -q --tb=no
.......................F.................................                [100%]
=========================== short test summary info ============================
FAILED tests/contract/test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline
1 failed, 128 passed in 3.36s

## run 2 — the feature's four guard classes + the budget carrier (smoke set + 1)

$ python3 -m pytest tests/contract/test_self_explanatory_constitution.py tests/contract/test_instructions_section_propagation.py tests/contract/test_self_explanatory_distribution.py tests/contract/test_self_explanatory_glossary.py tests/contract/test_instructions_size_budget.py -q
.......................................................                  [100%]
55 passed in 15.99s

## baseline cross-check

failure name in baseline-failed.txt?
1
test_a7 present in baseline-failed.txt (must be 0 — it was GREEN at base, so its HEAD failure is NEW)?
0
