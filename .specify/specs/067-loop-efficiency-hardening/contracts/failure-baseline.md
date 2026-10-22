# Contract: Baseline Failure Set & Triage (FB-01…FB-09)

Owner of the SC-008 / FR-018 / SC-009 verification mechanics. Set definition:
`data-model.md` E3; triage records: `data-model.md` E5.

- **FB-01**: The authoritative baseline failure set is the 83-name FAILED list of the
  2026-10-22 full run (`test-evidence/baseline-failures-2026-10-22.txt`). The clarify-era
  cache-derived 109-name record is superseded and is not used for judgments.
- **FB-02**: Green semantics are relative: after slimming, the name-level failure set
  MUST NOT contain any name absent from the baseline set (no NEW failures).
- **FB-03**: Pinned-class contract tests (mirror byte-identity, section-set pins,
  constitution double-landing, gate-criteria SHA pins, fast-fail contract entries and
  their class) MUST be 100% retained in the complete run; intentional updates to a pin
  require a recorded reason; pin literals and strength never decrease (FR-018).
- **FB-04**: The name-level comparison uses the runner's name-list output: baseline-side
  and post-side lists, then `comm -13 baseline-names post-names` (or equivalent) to
  extract NEW failure names; the empty diff is the pass condition for FB-02.
- **FB-05**: Triage of the 83 baseline names is bounded to two classes:
  (1) deterministic repair — mirror/parity/sync/drift/distribution markers are repaired
  by running the sync engine scoped to the drifted pairs (the mechanism owner of mirror
  truth), never by editing tests; pairs whose sources are mid-flight from other features
  are not synced blind. (2) case-level — gate-total pins, exec-quant cases, and the
  remaining named cases are triaged one by one: stale pin updated to the owner fact with
  recorded rationale, real regression fixed at the mechanism, or pre-existing debt
  registered per FB-06.
- **FB-06**: Pre-existing debt form: a dated record under this spec's test-evidence
  directory naming the failing pinned test, stating it predates this scope, and choosing
  fix-before-close or explicit registration — one of the two is mandatory before close
  (SC-008). A debt record never claims green.
- **FB-07**: Deleting or merging away a failing test is never a disposition for a
  baseline failure; FR-015 ledger rows describe reorganizations, not failure disposal.
- **FB-08**: Injection drill (SC-008): during implement verification, inject a single
  artificial failure into one consolidated test; the name-level diff of FB-04 MUST
  surface exactly that injected name; then revert. The drill record (command, diff
  output, date) is committed evidence.
- **FB-09**: Localization drill (SC-009): the injected failure's output MUST identify a
  unique node id (file, case, parametrized row), and a direct re-run by that node id
  MUST reproduce the failure. The drill record includes the re-run command and result.
