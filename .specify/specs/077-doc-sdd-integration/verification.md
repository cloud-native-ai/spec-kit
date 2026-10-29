# Verification Log — 077-doc-sdd-integration

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=c1cd4600
baseline_date=2026-10-30
baseline_branch=077-doc-sdd-integration

# Full-suite baseline captured at implement start (E2 slot 1): 6593 passed / 39 failed / 7 skipped.
baseline_suite_failed=39
baseline_suite_failed_names=.specify/specs/077-doc-sdd-integration/baseline-failed.txt

# -- /speckit.implement results --

implementation_date=2026-10-30
# Tree this segment (part 4/4) builds on: the P3 commit. This segment's own commit hash is
# reported in the implement wrap-up; verification.md is written before that commit exists,
# so no self-referential hash is invented here.
segment_base_commit=f5835e0e

# P4 (T023–T028) measured targeted sets only; the closure full run belongs after review and is
# NOT pre-spent here (Constitution: one full-suite reading per slot).
post_change_targeted_set_passed=174
post_change_targeted_set_failed=0
post_change_remaining_open_tasks=0

# -- Evidence records (bind every claim to archived evidence) --

sample_id=SC-001_three_declaration_states
evidence_path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-quickstart-s1-s7.txt
evidence_sha256=336a2f2d875a8f009bb49c06bee86cd28c06e07364b656423c60f230f2944c9e
verdict=pass

sample_id=SC-002_two_state_strip_equality
evidence_path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-distribution-two-state.txt
evidence_sha256=a477bce127b42e79a83c54745a83bf1c90d5668e0b0ab022ecbe3d08f768c5b4
verdict=partial

sample_id=SC-003_structure_faces_and_build_subrow
evidence_path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-closing-suites.txt
evidence_sha256=525131a6c2da54697e9a2d998105bde515d4edfc80f70ec0bb01c7232d942a16
verdict=partial

sample_id=SC-004_structure_gate_fixtures_and_producer
evidence_path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-plan-template-skeleton.txt
evidence_sha256=57e04e217208d92ad7d150b9fdf43f1e3776b8c23bd4dd1afabadaa87180a56a
verdict=pass

sample_id=SC-005_slots_live_and_u4_contract
evidence_path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-quickstart-s1-s7.txt
evidence_sha256=336a2f2d875a8f009bb49c06bee86cd28c06e07364b656423c60f230f2944c9e
verdict=partial

sample_id=SC-006_zero_new_mechanism
evidence_path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-scope-set-difference.txt
evidence_sha256=61dee41b0f679edee97e37fd0b6330813d7d4ab21c0a6211e69c4affd9e0eeb7
verdict=pass

sample_id=SC-007_distribution_equivalence
evidence_path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-distribution-two-state.txt
evidence_sha256=a477bce127b42e79a83c54745a83bf1c90d5668e0b0ab022ecbe3d08f768c5b4
verdict=pass

sample_id=SC-008_stage_integrity_and_069_invariants
evidence_path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-stage-integrity.txt
evidence_sha256=2ab40493e899f6ee0d61d85ced05ac4f10eebb24e11ac6772682d7c629ecb7dd
verdict=partial

# -- Success Criteria evaluation --
# Vocabulary is the one owned by .specify/templates/verification-log-template.md
# (pass | fail | partial | deferred | unknown).

SC-001_status=pass
SC-001_value=3/3 fixtures answer distinctly: `expression` / `source: declaration` / exit 0; `execution` / `source: default` / marker + `error.label: declaration-absent` / exit 0; `flow_class: null` / `source: declaration` / stderr `invalid-class: …:3 carries 'expressive'` / exit 1
SC-001_note=test-evidence/tasks-quickstart-s1-s7.txt § S2b (text + json records for all three fixtures). **Disclosed deviation**: the quickstart's S2 snippet points `--repo` at a bare temp tree, and the engine resolves its class owner under that root — the snippet as written therefore degrades all three to `owner-unavailable`/exit 2 (recorded unchanged in the same file, § S2). S2b adds the owner document exactly the way the pinned unit test's fixture does; `quickstart.md` was not rewritten (plan-owned). Closing set `tests/unit/test_flow_class_spec_key.py` + `tests/contract/test_flow_class_spec_declaration.py` = green (tasks-closing-suites.txt, 174 passed).

SC-002_status=partial
SC-002_value=leg 1 (gate-set identity for an execution-class line): **pass** — 35/35 template files restore the baseline byte for byte after stripping the wiring card, and the base→refresh diff contains only `insert` opcodes (0 deleted or rewritten lines; engine/owner hits 0/0/0 → 1/1/1). leg 2 ("remove the class engine and re-run: the execution-class stage still completes, printing `owner-unavailable`, 0 new failures"): **not executed end-to-end**
SC-002_note=test-evidence/tasks-distribution-two-state.txt. Leg 2 is evidenced only at its two observable ends: the engine prints `owner-unavailable` and exits 2 on an owner-less root (tasks-quickstart-s1-s7.txt § S2), and the card's degradation sentence (`退出码 2` + `不中断`) is asserted by tests/contract/test_stage_class_wiring.py (in tasks-closing-suites.txt). No seven-stage replay was run — the seven templates are byte-identical to the baseline outside the card, so a replay would measure baseline behaviour, not this feature. FR-011's exemption set is exactly the two declared places (plan template section + the card), no third.

SC-003_status=partial
SC-003_value=structure / evidence / reader faces and the `build` sub-row are fixture-verified (reader face turns red on a missing reader declaration; `build` sub-row `not-applicable` is listed face-level and does not move `passed`/`failed`; a `fail` sub-row turns the operator verdict `fail`). "Seven stages each emit ≥1 blocking operator row on one expression fixture line": **not produced by a live line**
SC-003_note=test-evidence/tasks-closing-suites.txt (test_document_structure_gate.py: 1 compliant + 4 negative + 2 delivered-document fixtures) and test-evidence/p3-t016-t020-green.txt (test_docs_gate_driver.py: operator counting is taken from the owner's stage-operator table, not from the CLI faces). The 100% per-stage coverage claim is judged from the operator table (U4's denominator), which is byte-identical to the baseline (tasks-owner-append-delta.txt).

SC-004_status=pass
SC-004_value=1 compliant fixture green; 4 negative fixtures red 4/4 (missing Chapter Tree + missing reader lines + evidence row missing `source` + one fact with two owners); 2 delivered-document fixtures red 2/2 (`chapter-unexpected`; structure/links/build clean while the evidence face fails → the gate still fails); producer skeleton present with two mutation probes that turn its own leg red
SC-004_note=test-evidence/tasks-closing-suites.txt (the checker legs) + test-evidence/tasks-plan-template-skeleton.txt (the producer leg, its two probes, and acceptance ② = the T009 strip guard and the T013 suite green on the same tree: 98 passed).

SC-005_status=partial
SC-005_value=slots: **pass** — `slots=baseline:1 closure:1 reruns=0 exceptions=0 unknown=6 environment_failures=0` with the two docs-gate-full rows accepted, and the negative control (a second `baseline` row) turns the audit red. U4 judging an expression line's implement record as incomplete: **specified and contract-asserted, not executed on a live line**
SC-005_note=test-evidence/tasks-quickstart-s1-s7.txt § S6/S6b for the slot half (the `status=fail` there is the fixture's missing six-stage E3 evidence, not a slot violation); test-evidence/p3-t016-t020-green.txt for the U4 half (`U4` carries the four blocking checks, the gate-evidence-missing case is incomplete and blocks the next dispatch, and `not-applicable` is not a cross-level equation). U4 is a driver prompt rule — its execution needs a driven line, which this segment did not run.

SC-006_status=pass
SC-006_value=`/speckit.*` inventory 27 = 27 with difference `[]`; dependencies 6 = 6 (pyproject blob identical); process carriers 19 = 19; service/daemon declarations `[]` = `[]`; blocking confirmation gates 27 = 27; `doc-consistency-check.py --faces` still four and the parser not widened
SC-006_note=test-evidence/tasks-scope-set-difference.txt (T021, baseline `c1cd4600` vs tree). Re-checked after this segment's plan-template edit: the template adds no command, no dependency and no gate (tasks-owner-append-delta.txt re-measures the ledger, tasks-069-invariants.txt re-measures the faces).

SC-007_status=pass
SC-007_value=unrefreshed 0/0/0 vs refreshed 1/1/1 for (engine, class owner pointer, gate owner pointer) across 35 files (7 templates × 1 source + 4 per-tool copies); stripping the card restores the baseline byte for byte in 35/35; mirrors six pairs `ok` and per-tool copies `OK`
SC-007_note=test-evidence/tasks-distribution-two-state.txt (§ per-file table + summary) and test-evidence/tasks-quickstart-s1-s7.txt § S5 (the live `--check` runs).

SC-008_status=partial
SC-008_value=eight-stage set 8 → 8 and the 100% analyze/review rule: unchanged and asserted; the "expression pilot line ran all eight stages, analyze and review once each (2/2), 0 skipped or shortened stages" measurement: **not run** (this repository has no expression-class line to pilot)
SC-008_note=test-evidence/tasks-069-invariants.txt (stage table identical to `c1cd4600`, `isomorphism` 8 stage rows / 6 gate faces / 0 findings, `## 阶段不变量` byte-identical, 069/069a/069b untouched) + test-evidence/tasks-stage-integrity.txt (the guard that the stage-integrity judge reads stage records and never the class). The 2/2 pilot count needs a driven expression line; it is a review/closure-time observation, not something this segment could fabricate.

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=

# -- Free-form notes --

notes=T023 measured the two distribution states with the strip algorithm imported from its owning test module (no second implementation): 35/35 identical after strip, insert-only diffs. T024 re-read the 069 invariants without rewriting the owner (eight stages 8→8, six faces byte-identical, four CLI faces unchanged, P0/P1 owner files with an empty diff, analyze/review still 100%, 069/069a/069b zero change). T025 proved the two owner documents are append-only (28 added lines, 0 deleted or rewritten; eleven sections byte-identical; ledger 79 rows, gaps=0, `spec:` never enters it). T026 ran S1–S7 for real; S2 needed the owner-document fixture the pinned unit test uses (disclosed above, quickstart.md not rewritten). T027 ran the four closing gates on the final tree (validate-tasks PASS 0/0; decomposition proceed 28 ≤ 40; pre-analyze pass errors=0 advisories=3 — all three are `.specify/.tmp/` paths the quickstart creates at run time; clause coverage `status: ok` with claimed 77 / FR 25/25). T028 landed the plan-template skeleton and its own static leg, proven non-vacuous by two mutation probes; the template's mirror copy was regenerated by `sync-mirrors.py --write` (the templates pair is the only pair that moved). Known red kept untouched: tests/contract/test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline is one of the 39 baseline failures (baseline-failed.txt line 12) — it belongs to Feature 069's confirmation-gate budget and is not this feature's to fix or mask.
