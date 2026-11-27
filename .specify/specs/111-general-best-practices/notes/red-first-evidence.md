# Red-first evidence — tests/contract/test_general_best_practices.py (T004)

Captured before any module document existed (module, mirror and map row all absent).

- **Guard**: `tests/contract/test_general_best_practices.py` — shared module-read prelude
  plus six stable legs (`test_module_document_set_and_closed_category_table`,
  `test_owner_files_placeholders_and_entry_shape`,
  `test_seed_entry_three_facts_and_ssh_extension`,
  `test_accumulation_pointer_chain_and_no_second_engine`,
  `test_framework_map_registration_rows_source_and_mirror`,
  `test_relative_links_resolve`), `pytestmark = pytest.mark.contract`.
- **Command** (single entry, interpreter per § Environment Prerequisites):
  `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_general_best_practices.py -q`
- **Date**: 2026-11-27T08:38Z
- **Exit code**: `1`

**Real output** (decisive excerpt; the raw full capture lives at
`test-evidence/guard-red-first.log`, a git-ignored local `*.log` file):

```text
# test runner: /usr/local/bin/python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_general_best_practices.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
bringing up nodes...
EEEEEE                                                                   [100%]
==================================== ERRORS ====================================
___ ERROR at setup of test_module_document_set_and_closed_category_table ___
...
>       assert MODULE_DIR.is_dir(), "missing module directory: shared/best-practices/"
E       AssertionError: missing module directory: shared/best-practices/
...
ERROR tests/contract/test_general_best_practices.py::test_framework_map_registration_rows_source_and_mirror
ERROR tests/contract/test_general_best_practices.py::test_relative_links_resolve
ERROR tests/contract/test_general_best_practices.py::test_owner_files_placeholders_and_entry_shape
ERROR tests/contract/test_general_best_practices.py::test_accumulation_pointer_chain_and_no_second_engine
ERROR tests/contract/test_general_best_practices.py::test_module_document_set_and_closed_category_table
ERROR tests/contract/test_general_best_practices.py::test_seed_entry_three_facts_and_ssh_extension
6 errors in 6.25s
```

**Why this is the right red**: all six legs halt in the shared prelude on the absent
module directory — the guard is red because the subject does not exist yet, not because
an assertion is mis-written. The prelude additionally carries the zero-residue scan,
the `Feature 111` attribution and the cited-path existence assertions (C-404, FR-008).