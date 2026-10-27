# Red-First Evidence — Feature 071 (implement stage)

**Opened**: 2026-10-27 at implement part 1 (T001), HEAD `30391ec38ac6de1466254d76febb66cb3ee54710`
**Owner of the obligation**: `contracts/tests-and-docs-sync.md` **C-66** — red-first is a duty of *each of the six groups*, not of the suite as a whole; each group is run before the mechanism it pins exists, and its failing run is recorded with **command line, real output, exit code, failing count**, reviewably rather than asserted. A group that cannot go red when its subject breaks is a fast-fail finding, never coverage.

**Status of this file**: the six group sections below are *scaffolding opened by T001 and filled by their own rows* — T004, T005, T010, T014, T019, T024 write the red run; T009, T013, T018, T023, T028 (plus T027's neighbouring re-run and T030's pin) write the red→green transition. No group may be counted as covered while its section still reads `pending`. Nothing in this file is a claim until it carries a real command, a real exit code, and a real failing count.

## The six new contract test files (C-65 a–f)

| # | Test file | Contract file it pins | C-65 group | Red run written by | Subject that must be able to break |
|---|---|---|---|---|---|
| 1 | `tests/contract/test_review_code_composition.py` | `contracts/command-orchestration.md` | (a) the command template's two segments and their fixed order; (b) the three applicability values | T004 (red) → T009 (green) | the composed surface of `templates/commands/review.md` — segments, order, triage values, two-artifact rule, report subsection content |
| 2 | `tests/contract/test_review_docs_isomorphism.py` | `contracts/tests-and-docs-sync.md` (declared-surface isomorphism) | (f) documentation/template isomorphism | T005 (red) → T034 (green) | the declared surface of `docs/reference/commands/review.md` vs `templates/commands/review.md`; red by construction while the page still describes a process-only review |
| 3 | `tests/contract/test_code_review_skill_contract.py` | `contracts/code-review-skill.md` | (e) the base-resolution rule; (a) triage predicate and empty-delta rule; renderer-mode selection | T010 (red) → T013 (green, base band) and T016/T017 (green, US3 bands) | `skills/internal/code-review/scripts/git-delta-review.sh` `base`/`triage` and the skill's renderer-absence clause |
| 4 | `tests/contract/test_coverage_receipt.py` | `contracts/coverage-receipt.md` | (d) the receipt's exit `1` on a gap and exit `2` on a state it cannot evaluate | T014 (red) → T018 (green) | the `receipt` subcommand — block grammar, closed exit alphabet, gap-vs-skip, three-way count agreement |
| 5 | `tests/contract/test_status_gate_owner.py` | `contracts/status-gate-ownership.md` | (c) the state-machine gate conditions | T019 (red) → T023 (green) | the `Implemented → Ready for Review` owner row and the two initiating rows that reference it |
| 6 | `tests/contract/test_review_feedback_boundary.py` | `contracts/feedback-and-boundaries.md` | (coupled to (a)/(c)) the feedback classification duty and the closing-face invariants | T024 (red) → T028 (green) | the classification duty on both surfaces, the three-unit census, the unchanged closing step set |

**Absence check at T001**: all six files are absent from the tree (they are created by T004/T005/T010/T014/T019/T024), which is the state a red run requires.

## Group 1 — `tests/contract/test_review_code_composition.py`

- Red run (T004): pending
- Command line: pending
- Real output: pending
- Exit code: pending
- Failing count: pending
- Red → green (T009): pending

## Group 2 — `tests/contract/test_review_docs_isomorphism.py`

- Red run (T005): pending
- Command line: pending
- Real output: pending
- Exit code: pending
- Failing count: pending
- Red → green (T034): pending — stays red by design until T031 rewrites the docs page

## Group 3 — `tests/contract/test_code_review_skill_contract.py`

- Red run (T010): pending
- Command line: pending
- Real output: pending
- Exit code: pending
- Failing count: pending
- Red → green (T013 for C-17…C-21; T016/T017 for the US3 bands): pending

## Group 4 — `tests/contract/test_coverage_receipt.py`

- Red run (T014): pending
- Command line: pending
- Real output: pending
- Exit code: pending
- Failing count: pending
- Red → green (T018): pending

## Group 5 — `tests/contract/test_status_gate_owner.py`

- Red run (T019): pending
- Command line: pending
- Real output: pending
- Exit code: pending
- Failing count: pending
- Red → green (T023): pending

## Group 6 — `tests/contract/test_review_feedback_boundary.py`

- Red run (T024): pending
- Command line: pending
- Real output: pending
- Exit code: pending
- Failing count: pending
- Red → green (T028): pending

## Neighbouring-suite re-runs (regression nets, not red-first)

These exercise behaviour that already exists or fully lands before they run, so they carry `[blockedBy:]` instead of a red-first claim (the create-tasks migration/regression exception).

- T027 — `python3 -m pytest -q tests/contract/test_expression_gates_doc.py` against the plan-stage pre-change count of **18 passed** (re-measured at implement start in `notes/pre-change-measurements.md` § PM-6): pending
- T030 — the one intentional pin `tests/contract/test_review_p1_review_loop.py::test_c15_review_owns_the_ready_for_review_transition` under FR-027's single authorization: pending
- T033 / T036 — mirror verification and final closure comparison against the T001 measurements and the T002 baseline: pending

## Fast-fail findings on the red-first obligation (T029 collects these)

None recorded yet. A group whose red run is missing, or that could not be made to go red, is recorded **here** rather than cited as coverage.
