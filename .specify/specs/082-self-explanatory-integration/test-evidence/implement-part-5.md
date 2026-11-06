# Implement part 5 — T024-T028 (US2 live reconcile + mutation legs)

- **stage**: implement
- **part**: 5/10
- **part_scope**: T024-T028
- **stage_base**: `5f267f22`
- **test_budget**: targeted-set-v1
- **command**: `python3 -m pytest tests/contract/test_instructions_section_propagation.py tests/contract/test_self_explanatory_constitution.py tests/contract/test_instructions_size_budget.py -q`
- **rc**: 0
- **passed / failed**: 32 passed / 0 failed
- **new_failures**: none; baseline 26 inherited failures in `baseline-failed.txt` unchanged.
- **live instructions**: `.specify/instructions.md` = 33357 B; `INSTRUCTIONS_BUDGET_BYTES` = 34816; headroom 1459 B; section `## Self-Explanatory Structure (不言自明)` at line 89; second generator run rc 0 and printed `Section reconcile: live instructions already carry all template sections.` (idempotent).
- **mirrors**: `.specify/templates/instructions-template.md` and `.specify/scripts/bash/generate-instructions.sh` byte-identical to their sources; symlinks `CLAUDE.md` / `QODER.md` / `AGENTS.md` still point to `.specify/instructions.md`.
- **mutation legs**: M-3/M-4 passed on temp copies; real template untouched.
- **C-21 pair**: closed — the template-side green arrived at T022; T024 re-ran the C-21 test after the live reconcile and recorded the pair in `notes/red-first-evidence.md`.
- **T028 C-19**: Documentation Map decision recorded in `test-evidence/tasks-stage-premises.md` (no row added; owner reachable through the section pointer).
- **discipline**: no plan-owned edits; no Completion Gate, no Feature status flip, no implement Feedback/Wrap-up; not pushed.
