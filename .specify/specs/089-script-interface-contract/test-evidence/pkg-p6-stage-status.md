# P6 stage status (T092–T094, 2026-11-08)

- T092: SC-001 re-measured with the contained harness — 749 candidates over 16 families, 0 moved snapshot pairs, VERDICT PASS (`SC-001-zero-side-effect.txt`).
- T093: `create-new-requirements.sh` no longer re-enters `main` (removed the nested entry at line ~388); `--` is a terminator, a token after it is an operand, and no-input exits 1 with usage without reading stdin. Regression tests: `tests/unit/test_create_new_requirements_separator.py` (2 passed).
- T094: five scripts with an original `usage()` now print it (watch-target, stage-runner, run-stage, render-excalidraw, git-delta-review); labels are appended only when absent, so no doubling. Guard test: `tests/contract/test_help_body_preservation.py` (7 passed).
- Verification: driver efficiency 51 + T093/T094 9 = 60 passed; mirrors `--check` exit 0.
