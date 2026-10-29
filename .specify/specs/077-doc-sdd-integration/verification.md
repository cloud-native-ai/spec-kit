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
evidence_path=.specify/specs/077-doc-sdd-integration/test-evidence/pilot-expression-line.txt
evidence_sha256=e50f000997af1799650cd70ff06794afe56cc094ec346c03027814e9282e6c40
verdict=pass

sample_id=SC-004_structure_gate_fixtures_and_producer
evidence_path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-plan-template-skeleton.txt
evidence_sha256=57e04e217208d92ad7d150b9fdf43f1e3776b8c23bd4dd1afabadaa87180a56a
verdict=pass

sample_id=SC-005_slots_live_and_u4_contract
evidence_path=.specify/specs/077-doc-sdd-integration/test-evidence/pilot-expression-line.txt
evidence_sha256=e50f000997af1799650cd70ff06794afe56cc094ec346c03027814e9282e6c40
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
evidence_path=.specify/specs/077-doc-sdd-integration/test-evidence/pilot-expression-line.txt
evidence_sha256=e50f000997af1799650cd70ff06794afe56cc094ec346c03027814e9282e6c40
verdict=partial

# -- Success Criteria evaluation --
# Vocabulary is the one owned by .specify/templates/verification-log-template.md
# (pass | fail | partial | deferred | unknown).

SC-001_status=pass
SC-001_value=3/3 fixtures answer distinctly: `expression` / `source: declaration` / exit 0; `execution` / `source: default` / marker + `error.label: declaration-absent` / exit 0; `flow_class: null` / `source: declaration` / stderr `invalid-class: …:3 carries 'expressive'` / exit 1
SC-001_note=test-evidence/tasks-quickstart-s1-s7.txt § S2b (text + json records for all three fixtures). **The disclosed deviation is closed in this round**: `quickstart.md` § S2 now builds the temp root with the owner document (`cp shared/definitions/flow-class-definitions.md "$TMP/shared/definitions/"`) and states the premise; the snippet was re-run verbatim and the three answers are reproduced in test-evidence/pilot-expression-line.txt § 3 (it supersedes § S2 of the older transcript, whose bytes are left untouched and whose sha is the one recorded above). The bare-tree form still degrades — `flow_class: execution` / `error.label: owner-unavailable` / exit 2 — and is kept as a contrast case in § 4. Closing set `tests/unit/test_flow_class_spec_key.py` + `tests/contract/test_flow_class_spec_declaration.py` = green (tasks-closing-suites.txt, 174 passed).

SC-002_status=partial
SC-002_value=leg 1 (gate-set identity for an execution-class line): **pass** — 35/35 template files restore the baseline byte for byte after stripping the wiring card, and the base→refresh diff contains only `insert` opcodes (0 deleted or rewritten lines; engine/owner hits 0/0/0 → 1/1/1). leg 2 ("remove the class engine and re-run: the execution-class stage still completes, printing `owner-unavailable`, 0 new failures"): **not executed end-to-end**
SC-002_note=test-evidence/tasks-distribution-two-state.txt. Leg 2 is evidenced only at its two observable ends: the engine prints `owner-unavailable` and exits 2 on an owner-less root (tasks-quickstart-s1-s7.txt § S2; re-measured for this round in test-evidence/pilot-expression-line.txt § 4), and the card's degradation sentence (`退出码 2` + `不中断`) is asserted by tests/contract/test_stage_class_wiring.py (in tasks-closing-suites.txt). **The expression-line pilot cannot close this leg**: it is an expression-class line, and leg 2 asks what an *execution*-class stage does when the class mechanism disappears. Remaining gap, stated as a gap: no seven-stage replay on an execution-class line was run. The reason it was not run is unchanged and deliberate — the seven templates are byte-identical to the baseline outside the card, so a replay would measure baseline behaviour, not this feature. FR-011's exemption set is exactly the two declared places (plan template section + the card), no third.

SC-003_status=pass
SC-003_value=structure / evidence / reader faces and the `build` sub-row are fixture-verified (reader face turns red on a missing reader declaration; `build` sub-row `not-applicable` is listed face-level and does not move `passed`/`failed`; a `fail` sub-row turns the operator verdict `fail`). "Seven stages each emit ≥1 blocking operator row on one expression fixture line": **8/8 operator rows now run on one declared-`expression` fixture line** — S1 entry read (`expression` / `declaration` / rc 0), S2 `validate-requirements` (5/5 labels), S3 `--action structure` (`status: ok`, `two-way: run`, 0 findings, 4/4 subsections), S4 `--action verify` (reader / evidence / duplicate / count all `pass`), S5 `validate-decision-tensions` (6/6 labels), S6 seven templates each carry exactly one wiring card and one lookup, S7 `docs-utils.py --action validate` (0 violations), S8 the two `docs-gate-full` slots accepted (`slots=baseline:1 closure:1`); 0 rows `not-evaluated`
SC-003_note=test-evidence/pilot-expression-line.txt § 1–2 (the eight-row transcript) and § 6 (three mutation controls that turn their own row red: delivered reader declaration removed ⇒ `faces.reader = fail`; plan chapter tree renamed ⇒ `subsection-missing`; a slot field removed ⇒ `reason=row 2: missing selection_basis`). **Scope of the claim**: a *synthetic fixture pilot with gate-level real execution* — the fixture line is `tests/fixtures/expression_line/`, the repository is built in `tmp_path` and discarded; it is not a customer line and is not recorded as one. The per-stage coverage denominator is still read from the gate owner's operator table (byte-identical to `c1cd4600`, tasks-owner-append-delta.txt), never from the pilot's own row count. S8's audit exits 1 because the six per-stage E3 evidence files are outside the eight rows (`unknown=6`); the slot half — which is what S8 measures — is clean.

SC-004_status=pass
SC-004_value=1 compliant fixture green; 4 negative fixtures red 4/4 (missing Chapter Tree + missing reader lines + evidence row missing `source` + one fact with two owners); 2 delivered-document fixtures red 2/2 (`chapter-unexpected`; structure/links/build clean while the evidence face fails → the gate still fails); producer skeleton present with two mutation probes that turn its own leg red
SC-004_note=test-evidence/tasks-closing-suites.txt (the checker legs) + test-evidence/tasks-plan-template-skeleton.txt (the producer leg, its two probes, and acceptance ② = the T009 strip guard and the T013 suite green on the same tree: 98 passed).

SC-005_status=partial
SC-005_value=slots: **pass, and re-measured on the pilot line** — `slots=baseline:1 closure:1 reruns=0 exceptions=0 environment_failures=0` with two `selection_basis=docs-gate-full` rows (one `baseline`, one `closure`), no slot-level violation; the field set is pinned by a mutation (dropping `selection_basis` from the closure row ⇒ `reason=row 2: missing selection_basis`), and the older negative control (a second `baseline` row) still turns the audit red. U4 judging an expression line's implement record as incomplete: **specified and contract-asserted, not executed on a live line**
SC-005_note=test-evidence/pilot-expression-line.txt § 2 (row S8 + its "detail") and § 6 (the slot-field mutation). U4 is a driver prompt rule — running it needs a driven line, and the pilot is a test, not a driver run; that half therefore stays unobserved and the SC stays `partial`. The U4 half's assertion lives in test-evidence/p3-t016-t020-green.txt (`U4` carries the four blocking checks, the gate-evidence-missing case is incomplete and blocks the next dispatch, and `not-applicable` is not a cross-level equation). The slot half's older evidence (tasks-quickstart-s1-s7.txt § S6/S6b, whose `status=fail` was the fixture's missing six-stage E3 evidence, not a slot violation) is unchanged; test-evidence/pilot-expression-line.txt supersedes it as the SC's sample.

SC-006_status=pass
SC-006_value=`/speckit.*` inventory 27 = 27 with difference `[]`; dependencies 6 = 6 (pyproject blob identical); process carriers 19 = 19; service/daemon declarations `[]` = `[]`; blocking confirmation gates 27 = 27; `doc-consistency-check.py --faces` still four and the parser not widened
SC-006_note=test-evidence/tasks-scope-set-difference.txt (T021, baseline `c1cd4600` vs tree). Re-checked after this segment's plan-template edit: the template adds no command, no dependency and no gate (tasks-owner-append-delta.txt re-measures the ledger, tasks-069-invariants.txt re-measures the faces).

SC-007_status=pass
SC-007_value=unrefreshed 0/0/0 vs refreshed 1/1/1 for (engine, class owner pointer, gate owner pointer) across 35 files (7 templates × 1 source + 4 per-tool copies); stripping the card restores the baseline byte for byte in 35/35; mirrors six pairs `ok` and per-tool copies `OK`
SC-007_note=test-evidence/tasks-distribution-two-state.txt (§ per-file table + summary) and test-evidence/tasks-quickstart-s1-s7.txt § S5 (the live `--check` runs).

SC-008_status=partial
SC-008_value=eight-stage set 8 → 8 and the 100% analyze/review rule: unchanged and asserted. The "expression pilot line ran all eight stages, analyze and review once each (2/2), 0 skipped or shortened stages" measurement: **partly run**. Part that ran: an expression-class fixture line executed **eight operator rows with 0 skipped or shortened rows** (S1–S8, all `pass`, transcript in the evidence file). Part that did not: `analyze` and `review` were **not invoked** on that line (2/2 unobserved), so the "analyze/review once each" half of this SC is still unmeasured
SC-008_note=test-evidence/pilot-expression-line.txt § 1–2 and § 7 (the reading notes state the gap in the same file). The eight rows are *gate* rows (entry read, requirements, structure, four faces, decision tensions, wiring presence, docs-space validate, slot audit), not the eight SDD stage commands; a fixture driven by a test does not call `/speckit.analyze` or `/speckit.review`, and calling them would require a driven line, not a test. Stage-set invariance itself stays proven by test-evidence/tasks-069-invariants.txt (stage table identical to `c1cd4600`, `isomorphism` 8 stage rows / 6 gate faces / 0 findings, `## 阶段不变量` byte-identical) and by the guard in test-evidence/tasks-stage-integrity.txt that the stage-integrity judge reads stage records and never the class.

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=

# -- Free-form notes --

notes=T023 measured the two distribution states with the strip algorithm imported from its owning test module (no second implementation): 35/35 identical after strip, insert-only diffs. T024 re-read the 069 invariants without rewriting the owner (eight stages 8→8, six faces byte-identical, four CLI faces unchanged, P0/P1 owner files with an empty diff, analyze/review still 100%, 069/069a/069b zero change). T025 proved the two owner documents are append-only (28 added lines, 0 deleted or rewritten; eleven sections byte-identical; ledger 79 rows, gaps=0, `spec:` never enters it). T026 ran S1–S7 for real; S2 needed the owner-document fixture the pinned unit test uses (that gap is now closed in `quickstart.md` itself — see SC-001). T027 ran the four closing gates on the final tree (validate-tasks PASS 0/0; decomposition proceed 28 ≤ 40; pre-analyze pass errors=0 advisories=3 — all three are `.specify/.tmp/` paths the quickstart creates at run time; clause coverage `status: ok` with claimed 77 / FR 25/25). T028 landed the plan-template skeleton and its own static leg, proven non-vacuous by two mutation probes; the template's mirror copy was regenerated by `sync-mirrors.py --write` (the templates pair is the only pair that moved).

# -- Review fix round (2026-10-30) -- the P1 evidence line and the three important replies --

review_fix_round=2026-10-30
# P1-a: one declared-expression fixture line now runs eight gate-level operator rows.
pilot_fixture=tests/fixtures/expression_line/{requirements,plan,doc}.md
pilot_test=tests/integration/test_expression_line_pilot.py
pilot_rows=8 (S1 lookup / S2 validate-requirements / S3 structure / S4 four faces / S5 decision tensions / S6 wiring presence / S7 docs-space validate / S8 docs-gate-full slots) — 8/8 pass, 0 not-evaluated
pilot_mutations=3 (delivered reader removed -> reader face fail; plan chapter tree renamed -> subsection-missing; slot field removed -> "row 2: missing selection_basis")
pilot_scope=synthetic fixture pilot (gate-level real execution); NOT a customer line — recorded as such in the evidence file's header and § 7
# P1-b: quickstart.md § S2 rewritten to the runnable form (owner document copied into the temp root) and re-run; the plan registers it as PLAN-EDIT … 分类=minor.
# important-1 / important-2: the exit-2 spec-input path now reports `owner-unavailable` with `flow_class: null` (was `invalid-unit-id` with a decided `execution`). Chosen branch: one label, two shapes — input missing -> null; owner/engine unavailable -> the pre-existing default record. This keeps the dispatch payload's `error` domain at `{owner-unavailable, -}`, so U4(c) needs no third branch. Registered in requirements FR-003/FR-004/FR-018/FR-019(c), data-model E2/E3/E9, contracts class-resolution C-003/C-005/C-006/C-012 and driver-integration C-001/C-004(c), stage-prompts.md.
# important-3: `templates/plan-template.md` no longer points a downstream project at `[[STR-002]]…[[STR-006]]`; it states the five headings verbatim and names the checker constants as the code-first owner (mirror synced).

# Known red kept untouched: tests/contract/test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline is one of the 39 baseline failures (baseline-failed.txt line 12) — it belongs to Feature 069's confirmation-gate budget and is not this feature's to fix or mask.
