# Red-First Evidence — 109-prompt-adherence

Purpose: record every red run and every later green capture for this feature as real command output with its exit code, appended as it is measured.
## Red run — declarations guard, before the five facts / owner document / engine exist

- Date: 2026-11-27T07:00:05Z (UTC)
- Command (the only test entry; P1 package baseline tree):

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_prompt_adherence_declarations.py -q
```

- Exit code: `1`
- Real output (runner header, failure names, summary):

```text
# test runner: /usr/local/bin/python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_prompt_adherence_declarations.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
FAILED tests/contract/test_prompt_adherence_declarations.py::test_owner_and_engine_reason_taxonomy_pin
FAILED tests/contract/test_prompt_adherence_declarations.py::test_engine_declaration_read_points_locatable
FAILED tests/contract/test_prompt_adherence_declarations.py::test_owner_catalog_agrees_with_declaration_sets_both_directions
FAILED tests/contract/test_prompt_adherence_declarations.py::test_exactly_five_facts_with_required_keys_and_closed_set_kind
FAILED tests/contract/test_prompt_adherence_declarations.py::test_absent_declaration_layer_degrades_with_exit_2
FAILED tests/contract/test_prompt_adherence_declarations.py::test_membership_equality_per_fr018
FAILED tests/contract/test_prompt_adherence_declarations.py::test_unknown_owner_catalog_token_is_exit_2_with_no_reading
FAILED tests/contract/test_prompt_adherence_declarations.py::test_unknown_declaration_token_is_exit_2_with_no_reading
8 failed, 1 passed in 6.26s
```

- Failure reasons (one line per failing leg's assertion — all are missing-subject asserts, never import
  errors):
  - `test_exactly_five_facts_with_required_keys_and_closed_set_kind`: `AssertionError: exactly the five prompt-adherence facts must exist; found []`
  - `test_membership_equality_per_fr018`: `AssertionError: declaration fact absent: shared/declarations/facts/prompt-adherence-layers.yaml`
  - `test_owner_catalog_agrees_with_declaration_sets_both_directions`: `AssertionError: owner document absent: shared/definitions/prompt-adherence-definitions.md`
  - `test_owner_and_engine_reason_taxonomy_pin`: `AssertionError: owner document absent: shared/definitions/prompt-adherence-definitions.md`
  - `test_engine_declaration_read_points_locatable`: `AssertionError: engine absent: scripts/python/prompt-adherence.py`
  - the three unknown-token / degradation legs: `AssertionError: cannot doctor an absent signals fact` /
    `cannot doctor an absent owner document` / `AssertionError: engine absent: scripts/python/prompt-adherence.py`
    (the scratch-tree precondition hits first because neither the facts, the owner document nor the engine
    exist yet)
- The one passing leg, `test_no_sixth_fact_for_observation_states`, is an absence guard over pre-existing
  subjects: the seven-state fact exists, `run-determination.py` carries `not_evaluated`, and no sixth
  `prompt-adherence-*` fact exists to fail it — its green at red time is honest, not a closure.

## Progression note — declarations guard after the five facts and the owner document land

- Date: 2026-11-27 (P1 package close, before the engine exists)
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_prompt_adherence_declarations.py -q`
- Exit code: `1`
- Real output:

```text
# test runner: /usr/local/bin/python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_prompt_adherence_declarations.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
FAILED tests/contract/test_prompt_adherence_declarations.py::test_owner_and_engine_reason_taxonomy_pin
FAILED tests/contract/test_prompt_adherence_declarations.py::test_absent_declaration_layer_degrades_with_exit_2
FAILED tests/contract/test_prompt_adherence_declarations.py::test_engine_declaration_read_points_locatable
FAILED tests/contract/test_prompt_adherence_declarations.py::test_unknown_declaration_token_is_exit_2_with_no_reading
FAILED tests/contract/test_prompt_adherence_declarations.py::test_unknown_owner_catalog_token_is_exit_2_with_no_reading
5 failed, 4 passed in 6.27s
```

The four passing legs are the fact-set, membership, no-sixth-fact and owner-catalog agreement guards (their
subjects now exist); the five failing legs all fail on `AssertionError: engine absent:
scripts/python/prompt-adherence.py` — the engine is package P2's deliverable, and T016 closes this guard
green there. No leg failed on an import error at any point.

## Red run — engine guard, before the engine exists (T010)

- Date: 2026-11-27 (P2 package, after the fixture family landed)
- Command (the only test entry; fixture family authored in T009):

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_prompt_adherence_engine.py -q
```

- Exit code: `1`
- Real output (runner header, failure names, summary):

```text
# test runner: /usr/local/bin/python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_prompt_adherence_engine.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
FAILED tests/contract/test_prompt_adherence_engine.py::test_engine_imports_no_network_module
FAILED tests/contract/test_prompt_adherence_engine.py::test_engine_reads_through_the_owning_engines_surfaces
FAILED tests/contract/test_prompt_adherence_engine.py::test_undeclared_option_is_rejected_before_any_action
FAILED tests/contract/test_prompt_adherence_engine.py::test_invalid_records_are_disclosed_with_causes_and_counts
FAILED tests/contract/test_prompt_adherence_engine.py::test_source_copy_and_installed_copy_each_read_their_own_owner_document
FAILED tests/contract/test_prompt_adherence_engine.py::test_seeded_default_reading_shape_and_catalog_order
FAILED tests/contract/test_prompt_adherence_engine.py::test_run_with_a_window_is_an_input_error
FAILED tests/contract/test_prompt_adherence_engine.py::test_unmatched_explicit_run_emits_not_found_and_exits_zero
FAILED tests/contract/test_prompt_adherence_engine.py::test_no_adherence_verdict_token_score_or_ranking
FAILED tests/contract/test_prompt_adherence_engine.py::test_gate_family_run_marks_the_gate_row_exercised
FAILED tests/contract/test_prompt_adherence_engine.py::test_version_answers_one_identity_line
FAILED tests/contract/test_prompt_adherence_engine.py::test_no_record_prose_reaches_either_output_form
FAILED tests/contract/test_prompt_adherence_engine.py::test_help_surfaces_are_identical_and_carry_the_four_labels
FAILED tests/contract/test_prompt_adherence_engine.py::test_two_consecutive_runs_are_field_identical
FAILED tests/contract/test_prompt_adherence_engine.py::test_explicit_run_is_partial_where_default_leaves_unobserved
FAILED tests/contract/test_prompt_adherence_engine.py::test_deviant_run_carries_both_run_determination_deviation_classes
FAILED tests/contract/test_prompt_adherence_engine.py::test_deleting_one_rows_records_turns_exactly_that_row_absent
FAILED tests/contract/test_prompt_adherence_engine.py::test_indirect_only_fixture_produces_no_layer_level_verdict
FAILED tests/contract/test_prompt_adherence_engine.py::test_human_form_prints_scope_basis_and_one_line_per_row
FAILED tests/contract/test_prompt_adherence_engine.py::test_recordless_fixture_emits_no_data_with_explicit_absence_lines
FAILED tests/contract/test_prompt_adherence_engine.py::test_project_layer_only_fixture_states_no_host_observation_beyond_unobserved
FAILED tests/contract/test_prompt_adherence_engine.py::test_duplicates_are_disclosed_with_paths
FAILED tests/contract/test_prompt_adherence_engine.py::test_emitted_tokens_are_members_of_declared_domains
23 failed, 1 passed in 6.26s
```

- Failure reason: every failing leg asserts `red-first: scripts/python/prompt-adherence.py is
  absent (built in US1 / T011…T015)` through `_require_engine()` — a named missing-subject
  assertion, never an import error. The one passing leg, `test_fixture_family_paths_exist`,
  guards the fixture family landed in T009 (its subject exists at red time; its green is
  honest, not a closure of any engine behavior).
- The fixture family's seeds were additionally verified at authoring time (T009) by reading
  each of the five variants through the owning engines' read surfaces in process
  (`run-determination.load_determinations`, `exec-quant.load_records`,
  `feedback-utils.scan_entries`, `evidence-utils.load_index`, `probe-utils.load_probe_registry`):
  seeded = 2 determinations / 1 exec-quant record / 2 feedback entries (one gate-family) /
  1 evidence run / probe registry 1 class 1 object 0 errors; project-only and indirect-only
  and recordless and negative each read their declared seeds; the negative variant's broken,
  unknown-version and bad-timestamp seeds are visible to the owning surfaces as dropped or
  out-of-domain records.

## Green capture — Part A closed (T016)

- Date: 2026-11-27 (P2 package; engine delivered in T011…T015)
- Command (the T016 gate, exactly as the task row specifies):

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_prompt_adherence_engine.py \
  tests/contract/test_prompt_adherence_declarations.py -q
```

- Exit code: `0`
- Real output:

```text
# test runner: /usr/local/bin/python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_prompt_adherence_engine.py tests/contract/test_prompt_adherence_declarations.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
bringing up nodes...
bringing up nodes...

.................................                                        [100%]
33 passed in 7.09s
```

- The declarations guard's five engine-dependent legs (owner↔engine reason pin, read-point
  locator, unknown declaration token, unknown owner catalog token, absent declaration layer)
  turned green here, closing the P1 progression note's engine-absent failure set.

### Fixture reading (SC-001) — seeded fixture, human form, exit 0

```text
$ python3 scripts/python/prompt-adherence.py --workspace-root tests/fixtures/prompt-adherence/seeded
prompt-adherence reading
reading-format: 1
engine: scripts/python/prompt-adherence.py 0.0.22
declaration-set: 093e71f226cc7a14f8c5fe83400943305f0e9654a5915a1edd618f7a2d4c5018
facts: shared/declarations/facts/prompt-adherence-deviation-classes.yaml, shared/declarations/facts/prompt-adherence-layers.yaml, shared/declarations/facts/prompt-adherence-reading-status.yaml, shared/declarations/facts/prompt-adherence-signals.yaml, shared/declarations/facts/prompt-adherence-strengths.yaml
scope: run r20261126T000000Z-fixture
scope-resolution: most-recent
scope-basis: store=evidence path=.specify/evidence/ev-20261126-fixture/findings.json timestamp=2026-11-26T00:05:00Z
status: complete
row run-determination-record layer=host-prompt strength=indirect state=Exercised
source run-determination-record store=session path=.specify/session/20261126T000100Z-run-determination-speckit-plan-rfixture.md record=r20261126T000000Z-fixture field=run_id
row exec-quant-record layer=project-rules strength=indirect state=Exercised
source exec-quant-record store=exec-quant path=.specify/exec-quant/records/20261126T000200000000Z-00000001.json record=r20261126T000000Z-fixture field=run_id
row feedback-entry layer=project-rules strength=direct state=Exercised
source feedback-entry store=feedback path=.specify/feedback/20261126T000300Z-fixture-plan.md record=20261126T000300Z-fixture-plan field=run_id
row gate-observation-record layer=project-rules strength=direct state=Unobserved reason=no-matching-records source=.specify/feedback
row evidence-finding layer=project-rules strength=indirect state=Exercised classes=evidence-missing
source evidence-finding store=evidence path=.specify/evidence/ev-20261126-fixture/findings.json record=r20261126T000000Z-fixture field=runId
row probe-registry-declaration layer=project-rules strength=indirect state=Wired
source probe-registry-declaration store=registry path=.specify/shared/definitions/probe-definitions.md record=registry field=objects
coverage-observable: run-determination-record, exec-quant-record, feedback-entry, evidence-finding, probe-registry-declaration
coverage-not-observable: gate-observation-record
coverage-blind-spots: host-prompt-content, host-rule-surfacing, in-turn-rule-behavior, anomaly-line-persistence, gate-breach-and-silent-skip, instruction-drift-between-reconciles
coverage-records-in-scope: 4
coverage-invalid-records: 0
```

- Exactly one observation per catalog row, in catalog order; five positive observations cite
  resolvable repo-relative source references; the gate row's absence carries
  `reason=no-matching-records`; the coverage section lists all six blind-spot classes.

### Field-identical rerun (determinism, L14)

```text
$ python3 scripts/python/prompt-adherence.py --workspace-root tests/fixtures/prompt-adherence/seeded --json > run-a.json   # exit 0
$ python3 scripts/python/prompt-adherence.py --workspace-root tests/fixtures/prompt-adherence/seeded --json > run-b.json   # exit 0
$ sha256sum run-a.json run-b.json
c4e6c56595de4b9d9e0b2ce11df2b95f6eabf8c9eb34d9752c0b08ed279e5f30  run-a.json
c4e6c56595de4b9d9e0b2ce11df2b95f6eabf8c9eb34d9752c0b08ed279e5f30  run-b.json
$ cmp run-a.json run-b.json   # rc 0 (byte-identical)

$ python3 scripts/python/prompt-adherence.py --workspace-root tests/fixtures/prompt-adherence/seeded > run-h1.txt
$ python3 scripts/python/prompt-adherence.py --workspace-root tests/fixtures/prompt-adherence/seeded > run-h2.txt
$ sha256sum run-h1.txt run-h2.txt
c57f9fc9c49e72173295e16f497e311901a4202fd23c609b74e33e6567e90de1  run-h1.txt
c57f9fc9c49e72173295e16f497e311901a4202fd23c609b74e33e6567e90de1  run-h2.txt
$ cmp run-h1.txt run-h2.txt   # rc 0 (byte-identical)
```

Both output forms derive from one computed structure; no `generated_at` or clock field
appears anywhere in the reading.
