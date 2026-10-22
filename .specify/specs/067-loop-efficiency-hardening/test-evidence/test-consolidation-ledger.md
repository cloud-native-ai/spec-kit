# Test Consolidation Ledger — 067-loop-efficiency-hardening

**Owner of record rows**: this file (schema: `data-model.md` E2; mechanics: `contracts/consolidation-ledger.md` LED-01…LED-08).

**Discipline (LED-01…LED-03)**:

- Every test id present in `test-evidence/baseline-test-ids.txt` and absent from the closure
  post list MUST have a row here (LED-05 join at T035). Case rows carry the full node id;
  file rows carry the file plus a declared node-id prefix.
- Disposition vocabulary is CLOSED: `deleted` / `case-merge` / `file-merge` / `retained`.
  A `deleted` row without `retained_equivalent_id` is invalid (V-E2-3).
- Append-only (LED-03): rows are never rewritten; corrections are new rows. Every row
  carries date + commit for attribution.
- Equivalence rationale MUST state the assertion set preserved (LED-04). Byte-identity
  consolidations cite the shared parametrized suite. Pin strength never decreases (LED-07 / FR-018).
- `retained` rows are optional bookkeeping for ids that survive reorganization unchanged in
  coverage; only MISSING ids are audited (LED-05). This file also records `retained` rows when
  a test's mechanism was rewritten (e.g., subprocess → in-process) so the rewrite is traceable.

## Rows

<!-- append rows below; one row per line-group, never rewrite above -->

| # | original_id | disposition | retained_equivalent_id | equivalence_rationale | date | commit |
|---|---|---|---|---|---|---|
