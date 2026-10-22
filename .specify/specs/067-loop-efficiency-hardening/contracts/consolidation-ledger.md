# Contract: Consolidation Ledger (LED-01…LED-08)

Owner of the ledger mechanics for FR-014 / FR-015 / SC-007. Ledger file and row schema:
`.specify/specs/067-loop-efficiency-hardening/test-evidence/test-consolidation-ledger.md`
(fields in `data-model.md` E2). Baseline/post id lists: `data-model.md` E4.

- **LED-01**: Every test id present in the baseline id list and absent from the post id
  list MUST have a ledger row. Case-level merge rows carry the full original node id;
  file-level merge rows carry the original test file plus a declared node-id prefix.
- **LED-02**: Disposition vocabulary is closed: deleted / case-merge / file-merge /
  retained. A `deleted` row without a retained equivalent coverage id is invalid.
- **LED-03**: The ledger is append-only; rows carry date and commit for attribution.
  Earlier rows are never rewritten; corrections are new rows.
- **LED-04**: Equivalence rationale is mandatory and must state what assertion set is
  preserved. For byte-identity consolidations the rationale cites the shared parametrized
  suite (table derived from the sync engine's pair inventory) and notes that per-pair
  byte comparison strength is unchanged or stronger (FR-018).
- **LED-05**: Closure audit is a deterministic inline join, not new machinery:
  regenerate the post list with the same collect method, then for the missing set
  (`comm -23 baseline-ids post-ids`) join each id against the ledger — case rows by
  full node id, file rows by mechanical expansion of the declared prefix. The join is
  performed by the small inline procedure recorded here at closure time:
  ```sh
  comm -23 test-evidence/baseline-test-ids.txt <post-ids> > /tmp/missing-ids.txt
  # then per id: match case rows on full id; file rows on prefix; report unmatched
  ```
  (implementation may inline the per-id join in a throwaway python/shell snippet run
  once; the snippet text and its output land in the audit evidence record).
- **LED-06**: Any missing id with no matching ledger row is a silent deletion; the
  closure audit fails (SC-007: zero such ids is the bar).
- **LED-07**: Pin-strength guard: consolidation MUST NOT remove pin literals, weaken
  pinned assertions, or lower the strength of drift protection (FR-018). A merged pin
  keeps its literal subject; if a pinned test also asserted extra conditions, those
  extra assertions stay with a surviving test.
- **LED-08**: Tests ADDED after the baseline (new coverage, drill fixtures) need no
  ledger rows; the audit compares baseline ids only, in the direction baseline → post.
  Post-only ids are reported informationally, not audited.
