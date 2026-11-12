# WP-02b evidence — classification live overlay (decision repair)

- **Line**: `101-anchor-goal-realignment` (unattended SDD, stage `implement`)
- **Package**: WP-02b — decision repair only; T026–T033 were not redone
- **Executor**: SDD Implement Executor (leaf)
- **Run id**: `r20261112T064607Z-b101` · **Unit**: `/speckit.implement` (command)
- **Base commit**: `e77d97e64` · **E2 baseline**: rc=1, 8900 passed, 192 failed, 3 skipped
- **Ruling applied**: `notes/wp02-decision-resolution.md` (027 dated record frozen; live test
  adapts through an additive overlay)

## Change

| Path | Change |
|---|---|
| `tests/contract/test_feedback_command_classification.py` | `_parse_table()` output kept as `BASELINE_TABLE`; new additive `LIVE_OVERLAY = {"anchor": "Complex"}`; `TABLE = {**BASELINE_TABLE, **LIVE_OVERLAY}` so the live expected set is 27 complex / 5 simple; `test_result_line_matches_the_counted_rows` now checks the frozen 027 `**Result**` line against the baseline rows (26 / 5) — the historical check is intact, only its comparison set is the dated table; `test_classification_counts` states the live 27/5 **and** the baseline 26/5, and asserts the overlay never overrides a baseline row. No assertion was deleted or weakened. |
| `tests/contract/test_docs_step_injection.py` | `anchor` added to `DOCS_STEP_EXCLUDED` with reason `no-documentation-section` — anchor is Complex in the classification but its reserved `## Wrap-up` is not compiled yet (T040); `test_c2a_exclusions_are_re_measured` re-measures the reason against the compiled unit, so a Docs Sync Eval line appearing at T040 forces the move into `COMPLEX_COMMANDS` instead of letting the exclusion rot. |

`.specify/specs/027-feedback-mechanism/**` is **not** modified (`git diff --stat` over that path
is empty). No template, skill, mirror, or WP-03 surface was touched.

## Red-first / after readings (all through `scripts/bash/run-tests.sh`)

The 13-module set was reconstructed by reproducing the WP-02 reading: the candidate set
below measured **`15 failed, 525 passed`** with exactly the recorded 15 ids
(`wp02-after-final-names.txt`), which confirms the set.

Command (13 modules):
`bash scripts/bash/run-tests.sh -q --names-out <path> tests/contract/test_compile_propagation_order.py tests/contract/test_expression_compatibility.py tests/contract/test_feedback_command_classification.py tests/contract/test_flow_class_ledger.py tests/contract/test_humanize_command_surface.py tests/contract/test_qoder_command_frontmatter.py tests/contract/test_run_skills_wiring.py tests/contract/test_goal_command_template.py tests/contract/test_goal_targets_engine.py tests/contract/test_migration_distribution.py tests/contract/test_skill_layer_visibility_guards.py tests/contract/test_docs_step_injection.py tests/contract/test_feedback_step_reference_form.py`

| Capture | Scope | Reading |
|---|---|---|
| pre-edit | 13 modules | **rc=1, 15 failed, 525 passed** (reproduces WP-02) |
| post-edit | 13 modules | **rc=1, 16 failed, 525 passed** |
| post-edit | classification module alone | **rc=1, 2 failed, 34 passed** |

Name-level diff against the pre-edit capture:

- closed (1): `test_feedback_command_classification.py::test_table_covers_every_command_template`
  — the decision red.
- new (2): `test_feedback_command_classification.py::test_complex_command_carries_feedback_step[anchor]`
  and `::test_complex_set_equals_measured_feedback_carriers` — the anchor feedback-face
  assertions, now measured rather than absent because `anchor` is in the live expected set.
  They stay red until T040 compiles the AUTO-GENERATED face into `templates/commands/anchor.md`.
- nothing else moved (`comm -23` / `comm -13` above).

## Remaining reds and owners (16)

| Owner | Count | Ids |
|---|---|---|
| E2 baseline (pre-existing) | 9 | `test_expression_compatibility.py::{test_c5_wiring_surface_is_closed, test_c5_non_wiring_files_keep_their_frozen_hashes, test_c6_feedback_step_edit_is_additive_single_line}`; `test_humanize_command_surface.py::{test_c06_registry_rows_resolve, test_wc07_skill_body_budget, test_wc10_feature_062_status_held, test_wc11_feature_row_name_description, test_wc13_stage_class_pin_remeasured}`; `test_qoder_command_frontmatter.py::test_every_template_has_short_description` |
| T039 (flow-class ledger) | 3 | `test_flow_class_ledger.py::{test_check_reports_79_units_and_zero_gaps, test_ledger_has_79_rows_covering_inventory_bidirectionally, test_templates_and_skills_never_assign_class_key}` |
| T040 (probe compile/propagation) | 4 | `test_compile_propagation_order.py::test_propagation_chain_is_green_in_canonical_order`; `test_run_skills_wiring.py::test_c9_compile_embeds_zero_drift_75_units`; `test_feedback_command_classification.py::test_complex_command_carries_feedback_step[anchor]`; `test_feedback_command_classification.py::test_complex_set_equals_measured_feedback_carriers` |

Of the 16, 15 are the WP-02 set minus the decision red; the 2 anchor-face classification
assertions are the T040-owned addition named by the ruling. The two modules adapted here can
only turn fully green when T040 compiles the anchor face (`no-documentation-section` exclusion
is re-measured by `test_c2a`).

## Wrap-up engines (`/speckit.implement`, run `r20261112T064607Z-b101`)

The `(unit_id, run_id)` pair was already recorded by WP-01a's wrap-up, so each engine reports
a duplicate and writes no second row — the duplicate reading is the satisfying evidence.

| Engine | Invocation | Reading |
|---|---|---|
| `run-determination.py` | `--action determine --unit-id /speckit.implement --unit-type command --run-id r20261112T064607Z-b101 --complexity complex --qualification qualified --feature 101-anchor-goal-realignment --json` | rc 0 — `{"duplicate": true, "unit_id": "/speckit.implement", "run_id": "r20261112T064607Z-b101", "note": "this (unit_id, run_id) was already determined"}` |
| `exec-quant.py` | `--action collect --unit-id /speckit.implement --unit-type command --run-id r20261112T064607Z-b101 --format json` | rc 0 — `duplicate record for (/speckit.implement, r20261112T064607z-b101); no second row written -> .specify/memory/exec-quant/records` |
| `feedback-utils.py` | `--action record --unit-id /speckit.implement --unit-type command --run-id r20261112T064607Z-b101 --feature 101-anchor-goal-realignment --points "No significant optimization points identified this run." --review …` | rc 0 — `{"id": "20261112T093549Z-speckit-implement", "path": ".specify/memory/feedback/20261112T093549Z-speckit-implement.md", "duplicate": true, "count_since_submission": 482, "threshold": 10, "should_prompt": true, "migrated": false}` |

In-passing corrections, disclosed: the first two invocations of `run-determination.py` and
`feedback-utils.py` exited 2 with the engine's own missing-argument errors (`--complexity`, then
`--points`); both engines write nothing on an argument error, and the re-invocations above are
the recorded readings.

## Package review (preserved here — the store dedupes this pair and has no force flag)

WP-02b closed the WP-02 decision inside the test layer without rewriting the dated 027 record:
the live expected set now carries `anchor: Complex` through an explicit additive overlay, the
027 `**Result**` line stays a frozen historical check against its own rows, coverage still
requires every `templates/commands/*.md` stem to be classified, and no assertion was removed.
The two remaining anchor assertions are named T040 downstream reds, not weakenings. Targeted
13-module reading: 16 failed / 525 passed, attributed 9 E2 / 3 T039 / 4 T040.

## Anomaly

未发现异常 — the only post-change movement is the intended one (decision red closed, 2 named
T040 reds opened); no unrelated id appeared or disappeared.
