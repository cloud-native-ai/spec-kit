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

## Red run — owner guard, before the coverage map exists (T017)

- Date: 2026-11-27 (P3 package, after the owner document head and the per-run engine landed)
- Command (the only test entry):

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_prompt_adherence_owner.py -q
```

- Exit code: `1`
- Real output (runner header, failure names, summary):

```text
# test runner: /usr/local/bin/python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_prompt_adherence_owner.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
FAILED tests/contract/test_prompt_adherence_owner.py::test_coverage_map_resolves_targets_and_cites_every_row_and_register_entry
FAILED tests/contract/test_prompt_adherence_owner.py::test_every_assumed_behavior_names_exactly_one_target_kind_and_one_target
FAILED tests/contract/test_prompt_adherence_owner.py::test_coverage_map_names_twelve_dense_assumed_behaviors
3 failed, 7 passed in 6.28s
```

- Failure reason: all three failing legs fail on the named red-first assertion
  `red-first: the owner document carries no assumed-behavior coverage-map section (authored by
  T018 — twelve AB-NN rows mapping each assumed behavior to exactly one catalog row or exactly
  one blind-spot id; FR-003)` — a missing-subject assertion, never an import error. The seven
  passing legs read the delivered owner document's ownership declaration, bilingual layer
  tokens, catalog cells, admission criteria, blind-spot register, framework-map rows and red
  lines; their subjects exist at red time, so their green is honest, not a closure.

## Red run — engine guard's `--check-coverage` legs, before the action exists (T019)

- Date: 2026-11-27 (P3 package, after T018 authored the coverage map)
- Command (the only test entry):

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_prompt_adherence_engine.py -q
```

- Exit code: `1`
- Real output (runner header, failure names, summary):

```text
# test runner: /usr/local/bin/python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_prompt_adherence_engine.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
FAILED tests/contract/test_prompt_adherence_engine.py::test_check_coverage_is_clean_on_the_delivered_owner_document
FAILED tests/contract/test_prompt_adherence_engine.py::test_check_coverage_reports_sorted_findings_on_doctored_copies[dangling-sensor-target]
FAILED tests/contract/test_prompt_adherence_engine.py::test_check_coverage_reports_sorted_findings_on_doctored_copies[dangling-blind-spot-target]
FAILED tests/contract/test_prompt_adherence_engine.py::test_check_coverage_reports_sorted_findings_on_doctored_copies[two-targets-on-one-row]
FAILED tests/contract/test_prompt_adherence_engine.py::test_check_coverage_reports_sorted_findings_on_doctored_copies[duplicate-assumed-behavior]
5 failed, 25 passed in 7.08s
```

- Failure reason: the clean leg reads exit `2` (the staged refusal names the action as not
  delivered) where the contract requires exit `0` with the zero-findings line; the four
  doctored cases read exit `2` where the contract requires exit `1` with the sorted finding
  list (they exercise all five coverage checks: dangling sensor target, dangling blind-spot
  target, two targets on one row, duplicate assumed-behavior id). The remaining new leg
  (`test_check_coverage_exits_2_when_the_owner_document_is_unusable`) passes at red time
  because its subject — the owner-document degradation path — pre-exists this action and fires
  before any action dispatch; its green is honest, not a closure of the new behavior. No leg
  failed on an import error.

## Green capture — the owner guard closes (T021)

- Date: 2026-11-27 (P3 package; `--check-coverage` implemented in T020)
- Command (the T021 gate, exactly as the task row specifies):

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_prompt_adherence_owner.py \
  tests/contract/test_prompt_adherence_engine.py -q
```

- Exit code: `0`
- Real output:

```text
# test runner: /usr/local/bin/python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_prompt_adherence_owner.py tests/contract/test_prompt_adherence_engine.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
40 passed in 7.08s
```

- The three owner-guard coverage-map legs that were red at T017 are green, and the five
  engine-guard `--check-coverage` legs that were red at T019 are green.

## SC-004 reading — the coverage check, clean and doctored (T022)

Clean reading over the delivered owner document:

```text
$ python3 scripts/python/prompt-adherence.py --check-coverage
coverage-map: ok (0 findings)
exit=0

$ python3 scripts/python/prompt-adherence.py --check-coverage --json
coverage-map: ok (0 findings)
exit=0
```

Doctored copy (`.specify/.tmp/prompt-adherence-sc004/`, a sanctioned scratch root; its AB-01
sensor target doctored to `zz-ghost-row`), same engine copy run from the scratch tree:

```text
$ python3 scripts/python/prompt-adherence.py --check-coverage
coverage-map: uncited-catalog-row: no assumed behavior cites run-determination-record
coverage-map: unresolved-target: AB-01 sensor target 'zz-ghost-row' is not a catalog row id
exit=1
```

The findings are sorted; the doctored copy names both the dangling target and the now-uncited
catalog row and exits 1; the scratch tree was removed after the reading. SC-004 is machine-read:
exit 0 with zero findings on the delivered document, exit 1 with the finding list on the
doctored copy.

## T025 — the per-run containment guard closes

Static half (zero write points in the engine source; `rc=1` here is grep's "no match", which is
the wanted reading):

```text
$ grep -nE '\.(write|writelines|write_text|write_bytes|mkdir|makedirs|unlink|rmdir|touch|symlink_to|hardlink_to|chmod|truncate|dump)\(|open\([^)]*["'"'"'][wax+]' scripts/python/prompt-adherence.py; echo "rc=$?"
rc=1
$ grep -nE '^(import|from) (tempfile|sqlite3|shelve|dbm|pickle|shutil|fcntl|filelock|mmap)' scripts/python/prompt-adherence.py; echo "rc=$?"
rc=1
```

The same claim is decided by the guard's AST scan
(`test_engine_source_has_zero_write_points`) and its comparator drill
(`test_manifest_comparison_would_detect_a_store_write`).

Per-run reading measured before/after on a copy of the seeded fixture (14 declared roots, the
same manifest the guard captures):

```text
reading_exit 0
declared_roots 14 populated_before 4 populated_after 4
files_before 7 files_after 7
root_set_identical True
manifest_identical True
```

Guard command (the only test entry) and output:

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_prompt_adherence_readonly.py -q
```

```text
# test runner: /usr/local/bin/python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_prompt_adherence_readonly.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
5 passed in 7.25s
```

Exit code: `0`. Before/after manifest counts are identical (4 populated roots, 7 files, zero
new files; the ten unpopulated declared roots stay absent).

## T026 — the init fixture closes

Guard command (the only test entry) and output:

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/integration/test_prompt_adherence_init.py -q
```

```text
# test runner: /usr/local/bin/python3 -m pytest -n auto --dist load -m "not slow" tests/integration/test_prompt_adherence_init.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
7 passed in 7.45s
```

Exit code: `0`.

Real output from a fresh project initialized from this repository's framework sources
(`copy_local_templates` + `get_resource_path` → repo root; scratch under `.specify/.tmp/`,
removed after the capture):

```text
$ python3 .specify/scripts/python/prompt-adherence.py --version
prompt-adherence.py 0.0.22
exit=0

blocker probe (socket-blocked interpreter): exit=1 blocked=True

$ python3 .specify/scripts/python/prompt-adherence.py        # under the socket-blocked interpreter
prompt-adherence reading
reading-format: 1
engine: .specify/scripts/python/prompt-adherence.py 0.0.22
declaration-set: 2beff0475d4a74de9d3d94259628875f0346b15121e18862dd3a441e44a81c45
facts: shared/declarations/facts/prompt-adherence-deviation-classes.yaml, shared/declarations/facts/prompt-adherence-layers.yaml, shared/declarations/facts/prompt-adherence-reading-status.yaml, shared/declarations/facts/prompt-adherence-signals.yaml, shared/declarations/facts/prompt-adherence-strengths.yaml
scope: run none
scope-resolution: none
status: no-data
row run-determination-record layer=host-prompt strength=indirect state=Unobserved reason=no-matching-records source=.specify/session
row exec-quant-record layer=project-rules strength=indirect state=not_evaluated reason=source-unavailable source=.specify/exec-quant
row feedback-entry layer=project-rules strength=direct state=not_evaluated reason=source-unavailable source=.specify/feedback
row gate-observation-record layer=project-rules strength=direct state=not_evaluated reason=source-unavailable source=.specify/feedback
row evidence-finding layer=project-rules strength=indirect state=not_evaluated reason=source-unavailable source=.specify/evidence
row probe-registry-declaration layer=project-rules strength=indirect state=Wired
source probe-registry-declaration store=registry path=.specify/shared/definitions/probe-definitions.md record=registry field=objects
coverage-observable: probe-registry-declaration
coverage-not-observable: run-determination-record, exec-quant-record, feedback-entry, gate-observation-record, evidence-finding
coverage-blind-spots: host-prompt-content, host-rule-surfacing, in-turn-rule-behavior, anomaly-line-persistence, gate-breach-and-silent-skip, instruction-drift-between-reconciles
coverage-records-in-scope: 0
coverage-invalid-records: 0
exit=0
stderr=''
```

The recordless project reads `no-data` with explicit `not_evaluated` / `Unobserved` lines and
per-store reasons under a socket-blocked interpreter, carries all six blind-spot classes, and
exits 0 — absence is never reported as clean. The probe row reads `Wired` because its registry
declaration ships with init. The fresh project's prompt-adherence-named inventory is exactly
the owner document, the five declaration facts and the engine (C-037 inventory-only scope).
