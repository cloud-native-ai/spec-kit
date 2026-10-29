# Red-First Evidence — 076-decision-tension-contract

**Owner of this file**: the implement stage's red-first log for Feature 076. Every new behavior
group is run BEFORE its implementation lands, and every run is recorded here as a four-field
observation. A record without all four fields is not evidence: 「已执行」 alone is exactly the
claim this feature (SI-3C 四元组) exists to make distinguishable from a run.

**Test files covered by this log** (the three contract-test files the feature declares):

| # | Test file | Groups it covers |
|---|-----------|------------------|
| 1 | `tests/contract/test_decision_tension_contract.py` | owner + template anchor (scenario A), analyze channel (B), quartet owner / SI-3C pointer (C), non-load-bearing gating (D), ADR slot + dangling link (E), terminology (F), closed-set delta (G) |
| 2 | `tests/contract/test_decision_tension_validator.py` | `validate-decision-tensions.py` CLI, closed six labels, dedup / cross-label precedence, output shape, inverse samples |
| 3 | `tests/contract/test_falsification_quartet_validator.py` | `validate-falsification-quartet.py` accept / reject matrix, exit-code triple, double-`red:` split fixture |

## Recording rule (four fields, mandatory)

Each group appends ONE block with exactly these four fields:

1. **重放命令 / Replay command** — the exact command line, copy-pasteable from the repo root.
2. **真实输出 / Real output** — the observed tail or the decisive excerpt, pasted verbatim
   (never paraphrased, never "expected").
3. **退出码 / Exit code** — the process exit code as observed.
4. **失败计数 / Failure count** — collected / passed / failed as the runner reported them.

Green runs append the same four fields. A group with no red run in this file is not claimed as
red-first (the two post-implementation guard slices F and G are the declared migration exception,
per `tasks.md` § Tests).

**Interpreter**: `SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python`
(the repo's own `.venv` carries no pytest; see `notes/pre-change-measurements.md`).
All commands below are run from the repo root with that interpreter.

---

## Group 1 — `test_decision_tension_contract.py` (scenario A: owner + template anchor)

### R1 — red run before implementation

- **Replay command**: `$SPECKIT_PYTHON -m pytest -q tests/contract/test_decision_tension_contract.py`
- **Real output** (tail; full capture `test-evidence/red-first-contract-scenario-a.txt`):
  ```
  FAILED ...::test_owner_declares_ownership_and_pointer_duty
  FAILED ...::test_record_field_set_is_closed_six_plus_id
  FAILED ...::test_admissibility_is_closed_four
  FAILED ...::test_rejection_forms_closed_and_named
  FAILED ...::test_load_bearing_threshold_four_triggers
  FAILED ...::test_complexity_gating_points_at_rubric
  FAILED ...::test_adjacent_owner_boundaries_by_path
  FAILED ...::test_owner_has_no_second_definition_or_carrier
  FAILED ...::test_template_section_adjacent_to_constitution_check
  FAILED ...::test_template_carrier_and_na_rule
  FAILED ...::test_template_is_pointer_not_copy_and_path_resolves
  11 failed in 0.13s
  ```
  Failure reasons are artifact-missing, not assertion-shape: `missing file:
  .../shared/guidelines/decision-tension.md` and `AssertionError: missing H2 section: ## Decision
  Tensions`.
- **Exit code**: `1`
- **Failure count**: `11 failed / 0 passed` (of 11 collected)

### G1 — green run after T004 / T005 / T006 (owner + template landed)

- **Replay command**: `$SPECKIT_PYTHON -m pytest -q tests/contract/test_decision_tension_contract.py`
- **Real output**: `...........                                                  [100%]` / `11 passed in 0.04s`
- **Exit code**: `0`
- **Failure count**: `0 failed / 11 passed`
- **Evidence**: `test-evidence/green-contract-scenario-a.txt`

---

## Group 2 — `test_decision_tension_validator.py` (CLI + structural checks + inverse samples)

### R2 — red run before implementation

- **Replay command**: `$SPECKIT_PYTHON -m pytest -q tests/contract/test_decision_tension_validator.py`
- **Real output** (tail; full capture `test-evidence/red-first-validator.txt`):
  ```
  E       AssertionError: missing artifact: .../scripts/python/validate-decision-tensions.py
  FAILED ...::test_cli_contract_and_exit_codes
  FAILED ...::test_label_set_closed_and_dedup_precedence
  FAILED ...::test_anchor_requires_three_adjacent_headings
  FAILED ...::test_output_shape_human_and_json
  FAILED ...::test_inverse_samples_turn_red[delete-decision]
  FAILED ...::test_inverse_samples_turn_red[delete-antithesis]
  FAILED ...::test_inverse_samples_turn_red[delete-binding_constraints]
  FAILED ...::test_inverse_samples_turn_red[delete-discriminating_evidence]
  FAILED ...::test_inverse_samples_turn_red[delete-expected_sacrifice]
  FAILED ...::test_inverse_samples_turn_red[delete-revision_trigger]
  FAILED ...::test_inverse_samples_turn_red[sacrifice-none]
  FAILED ...::test_inverse_samples_turn_red[undecidable-wording]
  FAILED ...::test_inverse_samples_turn_red[duplicate-tension-id]
  FAILED ...::test_inverse_samples_turn_red[skipped-tension-id]
  FAILED ...::test_inverse_samples_turn_red[unmapped-measurement-source]
  FAILED ...::test_record_index_exported_for_adr_link_check
  16 failed in 0.93s
  ```
  Failure reason is artifact-missing (`missing artifact:
  .../scripts/python/validate-decision-tensions.py`), not an assertion-shape defect.
- **Exit code**: `1`
- **Failure count**: `16 failed / 0 passed` (of 16 collected: 4 named tests plus the
  11-sample inverse matrix plus the record-index export test)

### G2 — run after T007 (four structural checks landed; two record-level rules belong to T008)

- **Replay command**: `$SPECKIT_PYTHON -m pytest -q tests/contract/test_decision_tension_validator.py`
- **Real output** (tail; full capture `test-evidence/validator-after-t007.txt`):
  ```
  FAILED ...::test_inverse_samples_turn_red[sacrifice-none]
  FAILED ...::test_inverse_samples_turn_red[undecidable-wording]
  FAILED ...::test_inverse_samples_turn_red[unmapped-measurement-source]
  3 failed, 13 passed in 1.65s
  ```
  The three remaining reds are exactly T008's scope (`dtr-rejected-form` for the literal
  `none` and for undecidable wording, `expected-sacrifice-unmapped` for an undeclared
  source). They are NOT masked: the validator declares the six labels, the two rules are
  documented as landing in T008, and every other inverse sample (six field deletions,
  duplicate id, skipped id) is green.
- **Exit code**: `1`
- **Failure count**: `3 failed / 13 passed` (of 16 collected)

### G3 — validator smoke on the feature's own plan (dogfooding)

- **Replay command**:
  `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/076-decision-tension-contract`
- **Real output**: `status: ok` / six `pass (0)` lines / `scanned: 272 lines, 2 record(s)` /
  `0 error(s), 0 warning(s)`
- **Exit code**: `0` (also `0` under system `Python 3.9.6`, which compiles the script: `compile-ok`)
- **Failure count**: not applicable (single run); evidence `test-evidence/validator-smoke-feature-plan.txt`

### G4 — neighbouring guard suites (no regressions)

- **Replay command**: `$SPECKIT_PYTHON -m pytest -q tests/contract/test_validate_tasks_parallel_safety.py
  tests/contract/test_user_facing_comprehension_doc.py tests/contract/test_closed_set_claims.py
  tests/contract/test_validation_carrier_contract.py tests/contract/test_self_improvement_conformance.py
  tests/contract/test_fast_fail_discipline.py::test_x16_plan_template_zero_change`
- **Real output**: `.......................................................................  [100%]` /
  `71 passed in 0.68s`
- **Exit code**: `0`
- **Failure count**: `0 failed / 71 passed`; evidence `test-evidence/neighbor-guards-after-t007.txt`

## Declared transients at the end of this segment (T001–T007)

1. **Mirror drift (closes at T024, the only sync row of this feature).** Adding the owner and
   the validator, and editing the template, leaves three mirror surfaces unsynced by design:
   `DIFF .specify/templates/plan-template.md`, `MISS .specify/scripts/python/validate-decision-tensions.py`,
   `MISS .specify/shared/guidelines/decision-tension.md` (`sync-mirrors.py --check` exit `2`).
   Consequence measured: `tests/contract/test_trigger_engine.py::test_c2_sync_mirrors_check_clean`
   is red until T024 runs `sync-mirrors.py --write`. Evidence:
   `test-evidence/mirror-drift-transient-after-t007.txt`. This is the declared ordering, not a
   subject defect: `tasks.md` § Mirror Obligations names T024 as the single sync-and-verify row.
2. **Two validator rules land in T008.** `dtr-rejected-form` and
   `expected-sacrifice-unmapped` print `pass (0)` until T008; the three red inverse samples above
   keep that gap visible (a vacuous green cannot be mistaken for a finished rule).
3. **No full-suite run in this segment** (the segment is targeted-only by instruction; the
   implementation-start baseline is `6514 passed / 39 failed`, frozen in `baseline-failed.txt`).

---

## Group 3 — `test_falsification_quartet_validator.py` (US3, later phase)

- **Status**: not started in this implementation segment (T012+ belong to a later segment).

---

## Group 4 — instruction-surface pointer (implement P1 adjudication)

- **Trigger**: adding `shared/guidelines/decision-tension.md` turned Feature 051's C-11(b)
  remainder assertion red (`test_user_facing_comprehension_section.py`); the remainder must stay
  within three named structurally-unpointed guidelines and MUST NOT grow a fourth name.
- **Adjudication**: add an instruction-surface pointer; do **not** amend C-11(b) and do **not**
  touch `UNPOINTED_BY_STRUCTURE`. Basis: C-11(b)'s own text forbids a fourth name and predicts
  that adding a pointer only shrinks the remainder; `docs/reference/history/00-cross-cutting-lessons.md:156`
  requires landing the new owner and its pointer as one commit unit rather than committing a
  known-red increment.
- **Landed**: one pointer line in `templates/instructions-template.md` § Task Complexity Rubric
  (plus its `.specify/templates/` mirror); guard re-run = **11 passed**.
- **Generator behaviour (measured)**: `generate-instructions.sh` reconciles at **section** level —
  a section that already exists in the live file is preserved, so `.specify/instructions.md`
  stays byte-identical (`git diff` empty) and does not yet carry the line. New projects rendered
  from the template at `specify init` get it immediately; this repo's live file gets it when that
  section is next reconciled as a whole. Recorded as a disclosed limitation, not a silent gap.
- **Classification**: `PLAN-EDIT: templates/instructions-template.md — one-line instruction-surface
  pointer (required by Feature 051 C-11(b)); 分类=substantive` — the delivery surface gains one
  instruction-surface line; no FR / SC / clause / task additions.
- **Known red kept**: the three validator inverse samples (`sacrifice-none`, `undecidable-wording`,
  `unmapped-measurement-source`) remain red until T008; they are the visible carrier of that
  deferred scope, not masked.
