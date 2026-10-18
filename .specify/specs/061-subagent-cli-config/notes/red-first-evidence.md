# Red-first & intentional-extension evidence — Feature 061

Process evidence only. Intentional-extension registration for the Completion Gate lives in
`verification.md` (per SC-004 / C-EQ-11); this file records the observed red→green runs.

## T004 — US1 contract tests, RED before the engine

Command:

```text
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_execution_config_engine.py -q --no-header -p no:cacheprovider
```

Actual output (exit 1):

```text
83 errors in 0.47s
```

Attribution: every test errors on the module-level fixture
`assert ENGINE.is_file(), "execution-config.py missing — engine not implemented"` — the
failure cause is the missing engine, not test syntax. (An earlier draft had 3 vacuous
exit-2 passes for tests that expect a usage error; the autouse fixture was added precisely
so no test can pass while the engine is absent.)

## T010 — US1 contract tests, GREEN after implementation

```text
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_execution_config_engine.py -q --no-header -p no:cacheprovider
........................................................................ [ 86%]
...........                                                              [100%]
83 passed in 6.89s
# exit 0
```

All C-EC-01..C-EC-15 clause groups are green, including the two claude zero-leak paths, the
F-03 precedence cases, external + null `cli`, and `qodercli`/`claude` `auto` positive
resolutions.

## T011 — US2 contract tests, RED before the v2 extension

```text
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_exec_quant_dispatch.py -q --no-header -p no:cacheprovider
38 errors in 0.24s
# exit 1
```

Attribution: the autouse fixture asserts `collect-dispatch` appears in the engine and
`SCHEMA_VERSION = 2`; the extension was absent. An earlier draft had 6 vacuous exit-2 passes
(argparse rejects unknown arguments) and was tightened the same way.

## T012/T013 — Intentional pin extensions (same-nodeid edits)

Actual order: the v2 engine extension landed first, then the pins were extended and
verified green against the v2 contract (these are migration/regression edits, not red-first
tests; tasks.md's "Tests are authored and observed RED before implementation" applies to the
new contract files T004/T011/T018).

| File | Pin | Extension |
|------|-----|-----------|
| `tests/contract/test_exec_quant_engine.py:54` | `ACTIONS_CLOSED_SET` | added `collect-dispatch` |
| same:57 | `PROVENANCE_DOMAIN` | added `configured` |
| same:61 | `MEASURABLE_PATHS` | added `("quality","exit_code")` |
| same:265 | `schema_version == 1` | `== 2` |
| same:549 | full-schema key set | added `config` |
| same | collect record assertions | config group = 11 × `not_evaluated`; `quality.exit_code = not_evaluated` |
| same | unit-id/type fixtures | added `collect` rejecting `agent:`; `--unit-type agent` accepted for listing |
| `tests/contract/test_probe_engine_action_sets.py:91` | exec-quant exact action set | added `collect-dispatch` |

Run after the extension (exit 1 — exactly the 7 pre-existing affected-file nodes; zero new):

```text
7 failed, 86 passed in 15.03s
FAILED tests/contract/test_exec_quant_engine.py::TestAgentCollection::test_resolved_agent_fields_from_wrapper_host
FAILED tests/contract/test_exec_quant_engine.py::TestCredentialDefense::test_engine_masks_credential_shaped_config_values
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_endpoint_candidates_origin_only
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_missing_config_face_degrades_to_marker
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_qoder_adapter_reads_config_face
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_qoder_adapter_reads_per_model_effort_when_set
FAILED tests/contract/test_exec_quant_engine.py::TestSizeCap::test_oversized_record_is_field_truncated_and_capped
```

These 7 are exactly the affected-file baseline set (T028 reconciles them node by node).

## T017 — US2 contract tests, GREEN after implementation

```text
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_exec_quant_dispatch.py -q --no-header -p no:cacheprovider
......................................                                   [100%]
38 passed in 6.71s
# exit 0
```

Plus quickstart S4 (real engine run): one record, idempotent repeat byte-identical,
`method_resolved=qoder-settings`, 11 config fields, measured exit/elapsed/tokens, score
accepted (see `quickstart-run.md` § S4).

## T018 — US3 init-seeding tests, RED before the `defaults_source` parameter

```text
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/integration/test_init_execution_config.py -q --no-header -p no:cacheprovider
6 errors in 0.09s
# exit 1
```

Attribution: the autouse fixture asserts the `defaults_source` parameter exists on
`ensure_agent_layer_dirs`; it did not. (An earlier draft had one vacuous pass where the
current no-seeding behavior already satisfies the "fabricates nothing" case; the fixture
tightened it.)

## T025 — US3 init-seeding tests, GREEN after the seeding implementation

```text
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/integration/test_init_execution_config.py -q --no-header -p no:cacheprovider
......                                                                   [100%]
6 passed in 0.17s
# exit 0
```

Plus quickstart S5 (actual run): `seeded: True True`,
`second_init_byte_identical: True`, `preserved: True`, `explicit_missing_raises: True`
(see `quickstart-run.md` § S5).
