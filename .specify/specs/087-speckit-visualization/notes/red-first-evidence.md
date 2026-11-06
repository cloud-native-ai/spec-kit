# Red-first evidence — Feature 087, implement Part 1 (T006, T007)

**Capture date**: 2026-11-06T06:52Z (UTC)
**Discipline**: Constitution IV (Test-First & Contract-Driven Implementation). Each test row precedes its
implementation row; the reading below is the RED state measured **before** T008/T009 existed.

## RED reading — before T008 and T009

**Command (verbatim)**:

```bash
python3 -m pytest -q tests/unit/test_status_digest_unit.py tests/contract/test_reporting_obligations.py
```

**Result**: `34 failed, 1 passed in 0.32s` (`rc=1`)

| File | Red-first row | Failing at RED | Note |
|------|---------------|----------------|------|
| `tests/unit/test_status_digest_unit.py` | T006 | 15 of 16 | the one pass is `test_engine_constants_are_the_authority_not_the_test`, a guard over the imported `STATE_VALUES` / `ACTIVE_STATES` sets and not over the missing script — it stays green by construction |
| `tests/contract/test_reporting_obligations.py` | T007 | 19 of 19 | every test asserts the owner document or a fact carried by it |

**Why this is red for the right reason**: each failing test asserts its subject's existence before its content
(`_require_engine()` / `_read()` raise an assertion naming the missing path), so the failure text is
"artifact missing", never an `ImportError`, `CollectionError` or syntax error. A red produced by a broken test file
would prove nothing about the missing implementation.

## What turns each file green

- `tests/unit/test_status_digest_unit.py` → **T009** (`scripts/python/status-digest.py`): registry resolution order,
  triplet projection, the state vocabulary quoted from the engine, the read-only boundary, the three-action surface.
- `tests/contract/test_reporting_obligations.py` → **T008** (`shared/guidelines/reporting-obligations.md`): the
  single-source-of-truth declaration with exactly eight owned facts, the four non-owned owners by path, the scope
  predicate, the one 30-second definition site, the four element labels by anchor, the three transition classes, the
  nine-term prohibition, the not-a-gate clause.

The GREEN readings are recorded in `test-evidence/implement.jsonl` (E3 rows) after the implementation lands; this
file records the RED half only, so the red→green transition stays auditable from two dated artifacts.

## Scope boundary kept deliberately

This file's tests cover **reader-level** script behaviour and **owner-document** obligations. Not asserted here, and
therefore not attributable to these two rows: the digest's bounding/ordering/`omitted`/exit-status set (T027), the
thirteen guard propositions (T033), the rendered status line (T016), the roster guard (T011), and the coaching
payload amendment (T020). Each of those rows adds its own assertions to the same files.
