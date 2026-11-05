# E2 `slot=baseline` — the one full-suite reading of this segment

**Row (the fields the driver records)**

| field | value |
|-------|-------|
| `seq` | 1 |
| `slot` | baseline |
| `stage` | implement |
| `selection_basis` | full-suite |
| `command` | `bash scripts/bash/run-tests.sh --names-out .specify/specs/084-harness-triple-structure/baseline-failed.txt` |
| `rc` | 1 |
| `passed` | 7151 |
| `failed` | 25 |
| `skipped` | 4 |
| `failed_names_path` | `.specify/specs/084-harness-triple-structure/baseline-failed.txt` (25 entries) |
| `evidence_ptr` | `.specify/specs/084-harness-triple-structure/test-evidence/baseline-full-suite-2026-11-05.txt` (complete stdout, 366 s wall clock, `start_epoch=1793877580` `end_epoch=1793877946`) |

Summary line of the run, verbatim:

```text
====== 25 failed, 7151 passed, 4 skipped, 5 warnings in 364.91s (0:06:04) ======
```

This is the **only** full-suite run of this segment. Every later verification in it is a targeted set.

## Attribution — 23 of the 25 entries are pre-change, 2 are in-flight mirror drift

**What happened, stated plainly rather than smoothed**: the run was started at `19:19:40` and finished at
`19:25:46`; the segment's first source edits landed at `19:22:20` (this segment's `notes/`), `19:22:47`
(`shared/declarations/contract.yaml`), `19:23:01` (`shared/definitions/framework-map.md`) and `19:23:53`
(`shared/definitions/harness-triple-definitions.md`). The run therefore **overlapped** the first edits, and
two of its failures are caused by those edits rather than inherited from the branch: the mirror pairs now
carry three unprojected entries (`MISS .specify/shared/declarations/contract.yaml`,
`MISS .specify/shared/definitions/harness-triple-definitions.md`,
`DIFF .specify/shared/definitions/framework-map.md`), and the mirror projection is `tasks.md` T026's job —
this segment MUST NOT hand-copy a mirror (Path Conventions, FF-12).

**How the split was measured, without a second full run.** `git archive HEAD | tar -x -C
.specify/.tmp/084-impl-p1/pristine` materialises the segment's start commit (`9657885f`) as a pristine tree;
the failing tests were then re-run **there**, one targeted invocation per group. A test that fails
identically in the pristine tree is pre-change; a test that passes there is attributable to this segment.

| group | pristine-tree reading | verdict |
|-------|----------------------|---------|
| `tests/contract/test_trigger_engine.py::test_c2_sync_mirrors_check_clean` | passed | **in-flight mirror drift** (T026 owns the projection) |
| `tests/contract/test_scripts_distribution_parity.py::TestScriptsDistributionParity::test_repo_has_no_orphan_or_drifted_scripts` | passed | **in-flight mirror drift** (same cause, same owner) |
| `tests/unit/test_loop_state_engine.py` (10 ids) | 10 failed | pre-change |
| `test_acceptance_premises.py::test_e_a_stale_pin_invalidates_the_comparison_instead_of_failing_it` | failed | pre-change |
| `test_clause_forms.py::test_the_four_md_forms_never_co_occur_in_one_file` | failed | pre-change |
| `test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target` | failed | pre-change |
| `test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline` | failed | pre-change |
| `test_neutrality_budget.py::test_c5_the_cap_leaves_zero_integer_headroom` | failed | pre-change |
| `test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` | failed | pre-change |
| `test_evidence_findings_schema.py::TestCF13FeedbackPackageExclusion::test_package_zip_contains_no_evidence_paths` | failed | pre-change |
| `test_execution_config_engine.py::TestErrorsAndWarnings::test_warning_surface_is_json_and_stderr` | failed | pre-change |
| `test_lifecycle_detach_reattach.py::test_lc_07_identity_mismatch_dead` / `::test_lc_10_11_12_snapshot_branches` | 2 failed | pre-change |
| `test_sdd_loop_driver_skill.py::test_c22_watch_target_hook_selftest` | failed | pre-change |
| `test_shared_reference_rewrite.py::test_skills_use_installed_absolute_shared_form` | failed | pre-change |
| `test_shipped_surface_client_neutrality.py::test_shipped_surface_has_no_framework_runtime_references` | failed | pre-change |
| `test_token_efficiency_discipline.py::test_cd5_headings_only_in_discipline_doc` | failed | pre-change |

**The comparison set for `GATE-2` / T029 is therefore the 23-name list**, written next to this file as
`test-evidence/baseline-pre-existing-failed.txt`; the raw capture at
`.specify/specs/084-harness-triple-structure/baseline-failed.txt` is kept exactly as the command produced it
(25 names) and is **not** rewritten — an evidence file that gets edited to look better stops being evidence.

**Consequence for later rows, recorded rather than absorbed**: on any tree before T026 the two mirror tests
are red **by construction**. T029's `comm -13` therefore compares against the 23-name list, and the two
mirror ids are read as "expected until the projection lands", never as "new failures".

The gate-scan total was re-read after the edits and is unchanged (`blocking confirmation gates: 27`), so
none of the gate-total failures is attributable to this segment's new documents.
