# Verification Log — 109-prompt-adherence

<!--
  Implementation-stage record. The KEY=VALUE block is the record; the closure judgement
  (`scripts/python/closure-acceptance-check.py`) parses `SC-NNN_status=` lines and nothing else.
  Statuses are gate products: every `pass` below was measured by the command named in its note
  on this tree (implementation commits b7661f617 and 1321bb609) before the Pre-Status-Flip Gate
  ran; SC-009's F-1 leg was read on the 1321bb609 tree.
-->

# -- Baseline (recorded before the implement work changed the tree) --

baseline_commit=21cab972e9365f1a3196707af29da400a7265fee
baseline_date=2026-11-27
baseline_branch=109-prompt-adherence
baseline_failed_names=222
baseline_failed_names_path=.specify/specs/109-prompt-adherence/baseline-failed.txt

# -- Implementation results (implement stage, run r20261127T053750Z-109a, packages P1–P4) --

implementation_date=2026-11-27
post_change_commit=1321bb609

# -- Smoke test record (exactly one per feature) --

smoke_command=env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_prompt_adherence_engine.py tests/contract/test_prompt_adherence_owner.py tests/contract/test_prompt_adherence_declarations.py tests/contract/test_prompt_adherence_readonly.py tests/integration/test_prompt_adherence_init.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/109-prompt-adherence/test-evidence/smoke-run.txt

# -- Deferred tasks --

deferred_tasks=

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=seeded fixture reading: exactly one observation per catalog row in catalog order (run-determination Exercised, exec-quant Exercised, feedback Exercised, gate-observation Unobserved + no-matching-records, evidence-finding Exercised + evidence-missing, probe-registry Wired); two consecutive runs are field-identical in both output forms (stdout byte equality)
SC-001_note=final path. tests/contract/test_prompt_adherence_engine.py::test_seeded_default_reading_shape_and_catalog_order / ::test_human_form_prints_scope_basis_and_one_line_per_row / ::test_two_consecutive_runs_are_field_identical / ::test_deleting_one_rows_records_turns_exactly_that_row_absent; command `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_prompt_adherence_engine.py -q` (record-time reading); evidence notes/red-first-evidence.md § T010 red / § T016 green, notes/quickstart-run.md § Scenario 1-2.

SC-002_status=pass
SC-002_value=after a per-run reading and after longitudinal readings (two overlapping windows plus an open-bound window), the hash manifest over the 14 declared roots (one `.specify/<store-name>/` root per store in runtime-store-layout.yaml#/statement) is byte-identical: seeded 4 populated roots / 7 files unchanged, multi-run 14 files unchanged, zero new files; interpreter bytecode caches excluded by name; determinism judged separately by run-A/run-B equality
SC-002_note=final path. tests/contract/test_prompt_adherence_readonly.py::test_per_run_reading_leaves_the_store_roots_byte_identical / ::test_longitudinal_reading_leaves_the_store_roots_byte_identical / ::test_manifest_comparison_would_detect_a_store_write / ::test_engine_source_has_zero_write_points; command `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_prompt_adherence_readonly.py -q`; evidence notes/red-first-evidence.md § T025, § T029 (`manifest_before_files=14 manifest_after_files=14 identical=True`), § T030.

SC-003_status=pass
SC-003_value=project-layer-only fixture: the single host-layer row reads Unobserved (never a host statement); indirect-only fixture: every positive observation declares strength=indirect and no layer-level verdict, score or ranking key appears anywhere in the reading
SC-003_note=final path. tests/contract/test_prompt_adherence_engine.py::test_project_layer_only_fixture_states_no_host_observation_beyond_unobserved / ::test_indirect_only_fixture_produces_no_layer_level_verdict / ::test_no_adherence_verdict_token_score_or_ranking; command `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_prompt_adherence_engine.py -q`; evidence notes/red-first-evidence.md § T016 green.

SC-004_status=pass
SC-004_value=`--check-coverage` on the delivered owner document: exit 0 with exactly `coverage-map: ok (0 findings)`; a doctored copy (AB-01 sensor target → zz-ghost-row) exits 1 naming `unresolved-target: AB-01 sensor target 'zz-ghost-row' is not a catalog row id` and `uncited-catalog-row: no assumed behavior cites run-determination-record`; an unreadable owner document exits 2 with no coverage verdict
SC-004_note=final path. tests/contract/test_prompt_adherence_engine.py::test_check_coverage_is_clean_on_the_delivered_owner_document / ::test_check_coverage_reports_sorted_findings_on_doctored_copies (4 parametrized cases) / ::test_check_coverage_exits_2_when_the_owner_document_is_unusable; command `python3 scripts/python/prompt-adherence.py --check-coverage` (exit 0) plus the doctored scratch-tree run (exit 1); evidence notes/red-first-evidence.md § SC-004 reading, notes/quickstart-run.md § Scenario 5; test-evidence/smoke-run.txt.

SC-005_status=pass
SC-005_value=fresh project initialized from this repository's framework sources (copy_local_templates + get_resource_path, the specify init distribution path) contains the owner document, the five declaration facts and the engine under .specify/; the installed entry answers `--version` (`prompt-adherence.py 0.0.22`); the bare invocation on the recordless project under a socket-blocked interpreter exits 0 with explicit not_evaluated / Unobserved lines, per-store reasons and all six blind-spot classes (JSON: status no-data, 6 observations, 6 blind spots); no network access and no write under any managed store root
SC-005_note=final path. tests/integration/test_prompt_adherence_init.py (7 legs) :: tests/contract/test_prompt_adherence_engine.py::test_engine_imports_no_network_module; command `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_prompt_adherence_init.py -q`; evidence notes/red-first-evidence.md § T026, notes/quickstart-run.md § Scenario 4.

SC-006_status=pass
SC-006_value=every positive observation in the seeded, multi-run, project-only and indirect-only readings reconstructs mechanically from its citation alone (session: the fenced JSON record's run_id; exec-quant/evidence: the record file's declared identity field; feedback: the frontmatter entry id plus the named field; registry: the Objects table's presence); the seeded broken reference surfaces as invalid_sources[.specify/evidence/ev-neg-broken/findings.json]=unparsable, never skipped; the dated baseline entry replays by one engine run: positive rows exact (state + classes), absence rows per the declared explicit-run shift, declaration-set digest and record/invalid counts equal
SC-006_note=final path. tests/contract/test_prompt_adherence_engine.py::test_every_positive_observation_resolves_from_its_citations_alone / ::test_the_seeded_broken_reference_appears_as_an_invalid_source_never_skipped / ::test_the_dated_baseline_entry_replays_against_its_citations; command `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_prompt_adherence_engine.py -q`; evidence notes/red-first-evidence.md § T032.

SC-007_status=pass
SC-007_value=each of the five closed sets' members is exercised by at least one test (layers: 2, strengths: 2, signals/rows: 6 — all six catalog rows observed across fixtures, deviation classes: 3, reading status: all four derivations; observation states compose the seven evidence states plus not_evaluated at read time); an unknown token in any declaration set, owner-document table, undeclared store name or command-line option exits 2 with no reading; the declarations guard pins the five facts to the owner document and the engine member-for-member in both directions
SC-007_note=final path. tests/contract/test_prompt_adherence_declarations.py (20 legs) + tests/contract/test_prompt_adherence_engine.py emitted-token and unknown-token legs; command `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_prompt_adherence_declarations.py tests/contract/test_prompt_adherence_engine.py -q`; evidence notes/red-first-evidence.md § declarations green, § T016.

SC-008_status=pass
SC-008_value=one dated baseline entry exists through the existing feedback channel: .specify/feedback/20261127T074122Z-speckit-implement.md (created 2026-11-27T07:41:22Z, unit /speckit.implement, feature 109-prompt-adherence, feature_id 109), carrying status complete, the six per-row states (3 Exercised, 2 Unobserved with causes, probe Wired), the declaration-set digest 093e71f226cc7a14f8c5fe83400943305f0e9654a5915a1edd618f7a2d4c5018, the six blind spots, record/invalid counts and 4 cited repo-relative source paths; replay re-runs the engine with the recorded --run scope and matches the recorded digest and counts; no aggregate, no new store, no improvement claimed
SC-008_note=final path. The entry itself plus the audit-replay leg ::test_the_dated_baseline_entry_replays_against_its_citations; command `python3 scripts/python/feedback-utils.py --action record ...` (exit 0, duplicate false) and `python3 scripts/python/prompt-adherence.py --run r20261127T053750Z-109a-p3`; evidence notes/red-first-evidence.md § T031, § T032.

SC-009_status=pass
SC-009_value=mirrors and sources byte-identical (`sync-mirrors.py --check` exit 0: scripts/ 134 files, shared/ 123 files; the second --write is a no-op; `regen-command-copies.py --check` exit 0; both engine copies answer `--version`); the fresh init fixture contains the mechanism; the framework-map rows parse; the full suite through `scripts/bash/run-tests.sh --full --names-out .specify/specs/109-prompt-adherence/final-failed.txt` reads 222 failed / 10361 passed / 3 skipped with 222 failed names, and `comm -13 baseline-failed.txt final-failed.txt` is empty — zero NEW failed names against the 222-name implement-entry baseline (highest-precedence reading: the one re-taken after the two guard corrections; the first reading's single NEW name, the bilingual-literal consumer registration, was repaired and the reading replaced, per T039's rule)
SC-009_note=supporting path. tests/integration/test_prompt_adherence_init.py + tests/contract/test_prompt_adherence_owner.py framework-map legs + `sync-mirrors.py --check`; evidence notes/red-first-evidence.md § T033, test-evidence/boundary-readings.txt, test-evidence/implementation-gates.txt § GATE-1

# -- Runtime Stack joint acceptance (one row per in-scope runtime-stack row) --

RS-001_joint_acceptance=verified by behaviour on the delivered tree: fixture consistency (six rows, every allowed state exercised), determinism (run-A/run-B byte equality in both output forms), read-only hash containment over the 14 declared roots for per-run and longitudinal readings, layer honesty (project-only and indirect-only fixtures), offline fresh-init run under a socket-blocked interpreter, mirror parity (`sync-mirrors.py --check` exit 0), and the F-1 full-suite name diff (recorded in test-evidence/implementation-gates.txt)

# -- Documentation evaluation --

The plan changes no docs/ file (PA10): the mechanism's discovery surface is the framework-map
rows plus the owner document § Entry, and it carries no per-session agent obligation, so no docs
page is required by this evaluation; none is added (C-037).