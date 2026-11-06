# Verification Log — 087-arch-diagram-docs

<!--
  Schema owner: shared/workflow/acceptance-hardening.md § Verification Vocabulary and § Closure Verdict.
  This file is the declared carrier (templates/verification-log-template.md); where it and the owner
  disagree the owner wins.

  Round: review-repair round 1 (2026-11-06). The review gate returned `blocked` on 1 P0 / 6 P1 / 17 P2;
  this file is the P0 finding F1. It is written HONESTLY: a `final`-path criterion reads `pass` only
  where the evidence pointer exists and reproduces; where the evidence is a unit/integration assertion
  on a local fixture the note says exactly that, and no criterion is promoted by a model judgement.

  Round 2 (same date): review F2/F13/F17/F26/F27/F28 were closed as a documentation-and-guard repair — no
  engine behaviour, fixture composition or criterion semantics changed. `post_change_commit` therefore keeps
  naming `b06c93a7`, the commit whose run produced these readings; the round-2 repair commit rides in the
  run's own commit log rather than overwriting where the measurements came from.
-->

# -- Repair rounds on this log (one line per round) --

round2_repair_scope=documentation-only (review F2/F13/F17/F26/F27/F28); no engine, fixture or test-semantics change
round2_repair_reading=the five 087 files re-run at the repair head: 124 passed, 0 failed; the SC rows above carry over unchanged

# -- Baseline (recorded before this round's repairs) --

baseline_commit=24cb4edc
baseline_date=2026-11-06
baseline_branch=line/087-arch-diagram-docs

baseline_failed_tests=26
baseline_passed_tests=7471
baseline_skipped_tests=4
baseline_record=.specify/specs/087-arch-diagram-docs/test-evidence/baseline-full-suite.log
baseline_failed_names=.specify/specs/087-arch-diagram-docs/baseline-failed.txt

# -- /speckit.implement results --

implementation_date=2026-11-06
post_change_commit=b06c93a7

post_change_087_files_passed=124
post_change_087_files_failed=0
post_change_fixture_check=pass
post_change_mirror_check=pass
post_change_command_copy_check=pass

# -- Smoke test record (exactly one per feature) --

smoke_command=/usr/bin/python3 -m pytest tests/unit/test_docs_obligation_reuse.py tests/unit/test_docs_utils_carriers.py tests/unit/test_docs_utils_obligation.py tests/integration/test_docs_obligation_scenarios.py tests/integration/test_docs_command_scenarios.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/087-arch-diagram-docs/test-evidence/smoke.txt

# -- Success Criteria evaluation --
# SC-001 … SC-006 are the `final` path; SC-007 … SC-010 are `supporting` (requirements.md).

SC-001_status=pass
SC-001_value=4/4 artifacts resolved from the record; reference target ∈ rendered[].path
SC-001_note=integration assertion on the `clean/` fixture copy — tests/integration/test_docs_obligation_scenarios.py::test_sc001_four_artifacts_present (document, source, rendered face, resolving reference); this round tightened the assertion from "any `../assets/` link" to "the link target is one of the record's rendered[].path" (review F24)

SC-002_status=pass
SC-002_value=2/2 faces named: orphan-rendered and orphan-source, distinct verdict/reason pairs
SC-002_note=test_sc002_removing_either_face_turns_red over `tmp_path` copies of orphan-rendered/ and orphan-source/; the two values are distinct per C-005, and the source-only case is additionally pinned by U::test_c007_source_only_reference_is_not_satisfied (review F4)

SC-003_status=pass
SC-003_value=reconcile reports missing>0 then 0 new findings; no cosmetic change
SC-003_note=test_sc003_reconcile_reports_then_converges plus test_c008a_second_reconcile_zero_findings — the second-run reading is on the same fixture copy, not a second space

SC-004_status=pass
SC-004_value=rename fixture: document and diagram in step, or a named staleness finding
SC-004_note=test_sc004_rename_keeps_document_and_diagram_in_step; the named-finding branch is test_c015_named_staleness_keeps_source in the command scenarios

SC-005_status=pass
SC-005_value=0 new engines, 0 new routing tables, 0 new delivery contracts; every surface reaches draw-diagram by path
SC-005_note=test_sc005_no_second_engine (changed-file scan for ≥2 engine names plus router vocabulary), test_sc005_surfaces_reach_by_reference and test_sc005_engine_domain_is_single_owner in tests/unit/test_docs_obligation_reuse.py; this round's own engine comment tripped the scan once and was rewritten in delivery-contract terms — the guard was not weakened

SC-006_status=pass
SC-006_value=2 runs byte-identical; every document keyed by path with a reason from the closed set; clean space zero findings; unrecorded space not-evaluated
SC-006_note=test_c002_two_runs_identical_json plus test_sc006_two_runs_identical_and_keyed_by_path, test_c012_no_record_not_evaluated, test_c012_trace_incomplete_end_to_end; the clean-space zero-finding reading is the `--only`-scoped `clean/` verdict (the whole-space reading carries the six typed index.md files the fixture registers, which is E6's composition, not a finding about the flow)

SC-007_status=partial
SC-007_value=record schema complete for 8/11 spaces; no unaccepted-diagram negative case
SC-007_note=supporting path. The record's required-field set is pinned by U::test_c010_record_schema (each required field dropped on its own copy must land not-evaluated / trace-incomplete) and end to end by I::test_c012_trace_incomplete_end_to_end, but the criterion's second half — "a produced diagram missing any of these is reported as unaccepted" — has no fixture asserting an UNACCEPTED delivery (`delivery.accepted=false`) rather than an incomplete RECORD
SC-007_blocked_at=2026-11-06 — no fixture yet separates "record present but delivery.accepted=false" from "record incomplete"
SC-007_reduced_measurement=the record schema's required-field set is asserted (trace-incomplete/ lands not-evaluated / trace-incomplete, and the builder's --check pins the eleven records' bytes)
SC-007_reduced_measurement_run=yes
SC-007_why_reduced_insufficient=an incomplete record and an unaccepted delivery are two different facts; the reduced measurement proves the first and says nothing about the second, so the criterion's "reported as unaccepted" half remains unmeasured
SC-007_unblock=add a twelfth fixture space whose record carries delivery.accepted=false with a non-empty unmet list, and assert the reading names it

SC-008_status=pass
SC-008_value=exempt-ok / exempt-bad / exempt-superseded: 3/3 readings as registered
SC-008_note=test_sc008_exemption_visible_and_superseded plus test_c011_exempt_ok / test_c011_exempt_bad / test_c011_superseded; exempt-ok reads converged=true + clean=false (C-013), superseded reads not-evaluated / exemption-invalid

SC-009_status=pass
SC-009_value=read-only zone, anchor zone, archive-not-delete and the confirmation tiers observably unchanged
SC-009_note=test_sc009_confirm_tiers_and_zones_unchanged; a move/archive fixture still stops for confirmation, and `assets/` is out of the carrier set so no diagram is triaged as prose

SC-010_status=partial
SC-010_value=unrefreshed-runtime degradation has no end-to-end fixture run
SC-010_note=supporting path. The degraded reading is asserted at the text/wiring level — the flows must carry the `not-evaluated` label instead of a green, which test_sc010_unrefreshed_runtime_degrades_visibly and test_c004_refusal_carried_through check — but no fixture project with an unrefreshed `.specify/` runtime was actually run end to end in this round
SC-010_blocked_at=2026-11-06 — deferred: not attempted this round (supporting path admits `deferred`)
SC-010_reduced_measurement=the flow text and dispatch wiring are asserted to carry the degraded label and to forbid a silent green
SC-010_reduced_measurement_run=yes
SC-010_why_reduced_insufficient=carrying the label is not the same as the label firing on an unrefreshed runtime; a project that never runs the flow cannot be shown to read it
SC-010_unblock=stand up a fixture project whose `.specify/skills/` lacks the `obligation` action and record its flow output
SC-010_deferred_reason=supporting-path criterion, not attempted this round; the feature's acceptance does not depend on it

# -- Joint acceptance (one row per `in-scope` runtime-stack row in requirements.md) --
# RS-005 / RS-006 / RS-007 are the three `in-scope` rows; RS-001 … RS-004 are `signed-contract`.

RS-005_joint_acceptance=pass
RS-006_joint_acceptance=pass
RS-007_joint_acceptance=pass
RS-001_joint_acceptance=pass
RS-002_joint_acceptance=pass
RS-003_joint_acceptance=pass
RS-004_joint_acceptance=partial

# -- Deferred tasks --

deferred_tasks=
deferred_reason_summary=none — every one of the 76 rows is closed; T076's own row records the stage status

# -- Free-form notes --

notes=SC-007 and SC-010 are `supporting` rows held at `partial`: neither refuses the closure verdict (only a `final`-path criterion can), and both carry a named unblock. RS-004 is `partial` for the same reason the SC-010 row is — the shared render backend was never exercised from this checkout (no `healthz` reading was taken in this round); RS-004 is `signed-contract`, so the row is recorded rather than claimed. Feature 087 stays `Planned`: this round does not flip the status, and the `Planned → Implemented` transition belongs to a run whose closure verdict is `accept` and whose `final_path.pass = 6/6` — which the payload below reports.
