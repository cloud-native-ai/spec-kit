# Implement part 2 — T007-T012 (US1 tests + constitution principle)

- **stage**: implement
- **part**: 2/10
- **part_scope**: T007-T012
- **stage_base**: `1cec4933`
- **test_budget**: targeted-set-v1
- **command**: `python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q`
- **selected_paths**: `tests/contract/test_self_explanatory_constitution.py`
- **rc**: 1
- **passed / failed**: 12 passed / 1 failed
- **new_failures**: `test_c21_instructions_summary_is_at_most_two_sentences` — **expected-red until T022** lands the instructions section. C-7's mandate-side half is expected-red until T013 lands the generator skill entry. Neither is a regression against `baseline-failed.txt`.
- **baseline**: 26 inherited failures in `baseline-failed.txt`; no new failure outside the two declared expected-reds.
- **sufficiency**: the US1 surface is green — C-1/C-2/C-3/C-4/C-6/C-7 template side/C-8/C-20 pass; C-21's green is deferred to T022 (instructions phase), and C-7's mandate side to T013.
- **evidence_ptr**: this file; `notes/pre-change-measurements.md` (T012 `hits: []`, block 22 lines); `notes/red-first-evidence.md` (T006 red + T015 pairing).
