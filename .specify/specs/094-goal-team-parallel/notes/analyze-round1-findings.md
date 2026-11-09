# Analyze Round 1 — Findings and Repair Brief (092, 2026-11-09)

Read-only analyze at main workspace `master@0b4f36ab`: 14 findings = 1 CRITICAL / 5 HIGH / 5 MEDIUM / 3 LOW. Checklist 8 fail rows: 7 STILL-VALID / 1 PARTIAL / 0 fixed / 0 NOT-OURS. Verdict: NOT ready to implement.

## Blocking findings
- **C-01 (CRITICAL, command-family predicate wrong)**: FR-006 says "exit 0 + returned registered class = in family", but `flow-class-classes.yaml` is an ordered set whose member 0 is the default for undeclared units, so `/speckit.nonexistentcommand` also exits 0 with `flow_class: execution`. The discriminator is `source: ledger` vs `source: default` (engine L900-918); neither FR-006 nor A9 names it. Fix FR-006 + A9.
- **H-01 (HIGH, untestable GATE-6)**: `account-clause-coverage.py` `fr-uncovered` fails 26/42 under the exact GATE-6 command; the tasks stage deferred the repair to analyze but the spine gate line dropped the disclosure. Either rewrite the 111 clauses' citation groups or make GATE-6 name the lane it actually asserts.
- **H-02 (HIGH, three-way scope set)**: FR-008/plan T-004 say `{global, auto}`; contract C-9 and `features/092.md` say `{goal, teams, auto}`; the live engine uses `("global","spec","auto")`. Reconcile to one answer.
- **H-03 (HIGH, duplicated Assumptions)**: 19 A-lines / 11 distinct; A1-A8 doubled; `validate-requirements.py` `dup-id` only matches FR|SC, so no gate catches it. Merge with two diffs (seg1\seg2, seg2\seg1); never delete.
- **H-04 (HIGH, contradicting A1 + mis-cites)**: seg-1 A1 says scope already ruled; seg-2 A1 defers to plan; FR-008/T-004 took the ruling, so seg-2 A1 is void. Also A2/A4 mis-cite FR-032/FR-025 (should be FR-031/FR-024) in both segments; A3 cites FR-019 instead of FR-031.
- **H-05 (HIGH, T043 forward dependency)**: T043's `[blockedBy: T054]` points to a later task; reorder T043 after T054 or move the handoff-decision implementation earlier.

## Other findings
- M-01 A6 range: seg-1 "085-090" wrong, seg-2 "085-091" correct (live 7+7); keep seg-2, delete seg-1.
- M-02 FR-005 stale pointer to FR-032 (declaration owner is FR-031).
- M-03 A9 "unregistered = not in family" only in Assumptions and factually wrong per C-01; promote with the corrected mechanism.
- M-04 A11 lineage prohibition only in the duplicated block; no FR carries it.
- M-05 FR-041 cites A7 twice; highest-blast-radius instance of H-03 (irreversible 085-test removal).
- L-01 empty B-F FR subsections; L-02 features.md/092 detail stage record stale; L-03 team-side "Temporary" heading vs C-107 scan.

## Implement preconditions (ordered)
1. C-01; 2. H-02; 3. H-03+H-04; 4. M-01..M-05 + L-01; 5. H-05; 6. H-01; 7. L-02.

## Notes
- The validation wave was not independently dispatched (worker has no dispatch tool); every mechanical claim is an engine/shell reading.
- Two blind greens recorded: `doc-consistency-check --faces duplicate` excludes `.specify/` and only reports cross-file duplicates; `validate-requirements dup-id` covers FR|SC only.
