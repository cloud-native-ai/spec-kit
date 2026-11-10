# Contract: Session Scan Cache

**Owner of these propositions**: this file. **Implementation surfaces**: `tests/conftest.py` (session
fixtures), `tests/contract/test_coverage_receipt.py`, `tests/contract/test_clause_coverage.py`, and the new
guard `tests/contract/test_scan_cache_contract.py`.

## A. Key and lifetime

- **C-001**: The cache key is `(session, worker, managed surface, root, variant)`. In an xdist session a
  session-scoped fixture is built once **per worker**, so the key's worker component is the xdist worker id
  and the upper bound on builds is the worker count, never the test count (FR-012, FR-025, A8).
- **C-002**: Managed surfaces are exactly two in this slice: `framework-specs-corpus` (the `account()`
  payload over `.specify/specs`) and `framework-root-inputs` (the 071 requirements path and the template
  texts read by `test_coverage_receipt.py`). A new surface requires revising this clause.
- **C-003**: The lifetime is the session. There is no cross-session persistence, no on-disk cache, and no
  mtime or content polling for in-session staleness; a new session (including every new xdist worker)
  rebuilds and therefore sees the current content (FR-025, A15).

## B. Immutability and consumer boundary

- **C-004**: The stored payload is read-only. Consumer access returns a deep copy; no test may mutate the
  stored structure in place. A mutation of the returned copy MUST NOT affect another consumer (FR-013).
- **C-005**: Only read-only assertions against the real framework input may consume the shared payload.
  A test that writes into the tree it scans MUST NOT consume the shared payload and MUST use a per-test
  fixture or a tmp corpus (FR-013, FR-025).
- **C-006**: `test_c20`'s before/after byte-identity check over the real corpus stays a separate
  subprocess test and MUST NOT consume the cache; it is the detector that a scan wrote into the corpus
  (FR-013, FR-014).

## C. Build mechanics

- **C-007**: The corpus surface is built in-process: the fixture loads
  `scripts/python/account-clause-coverage.py` with `importlib.util.spec_from_file_location` (the existing
  house pattern) and wraps `_corpus_files` with a counter. The build is one traversal per worker for the
  surface; the recorded `build_count` and `traversals` fields are exposed on the fixture value for the
  guard (FR-012).
- **C-008**: The five real-corpus callers (`c10`, `c20`, `c26`, `c27`, `form_exit_code_table`) are converted
  to consume the payload only where their subject is the computed result. `form_exit_code_table` keeps its
  subprocess leg because its subject is the process exit-code contract; its computed payload may consume
  the cache (FR-012, FR-018 boundary).

## D. Equivalence and proof

- **C-009**: The same assertion set MUST be green before and after conversion, and assertion strength MUST
  NOT change. Equivalent behaviour is demonstrated by running both files before and after with the same
  selection and comparing pass/fail names (FR-014).
- **C-010**: A cross-session mutation drill MUST turn the corresponding assertion red: build the payload
  over a tmp copy of the corpus in one subprocess session, tamper the copy, build again in a new session,
  and assert the affected field changed. A cache that returned a stale or constant payload fails this
  drill (FR-014, FR-025).
- **C-011**: A build-count probe MUST demonstrate `build_count = 1` per worker with more than one consumer
  and `traversals = 1` for the corpus surface; the probe output is recorded under `test-evidence/`
  (FR-012, SC-007).

## E. Mutation legs

| Leg | Mutation | Must fail |
|-----|----------|-----------|
| CA-M1 | Build the corpus payload per test instead of per session | C-011 |
| CA-M2 | Return the stored payload without a copy and mutate it in one consumer | C-004 |
| CA-M3 | Add mtime-based in-session staleness detection | static assertion in the guard (C-003 forbids it) |
| CA-M4 | Make a mutating test consume the shared payload | C-005 + C-010 drill |
| CA-M5 | Freeze a hardcoded payload in the fixture | C-010 drill |
