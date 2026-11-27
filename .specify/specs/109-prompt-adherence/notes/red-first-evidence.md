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
