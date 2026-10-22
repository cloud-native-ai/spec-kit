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
| 1 | tests/unit/test_admission_check.py::test_medium_fixture_admitted | retained | (same id) | id and assertion set unchanged (decision/measured/criteria ids a–g/checklist skip); mechanism rewritten: engine importlib-loaded in-process via main(argv), repo from module template clone instead of init+2 commits | 2026-10-22 | f14c4f49 |
| 2 | tests/unit/test_admission_check.py::test_large_fixture_denied | retained | (same id) | id and assertion set unchanged (exit 1/full-chain/task_count 60/criterion a fail); same mechanism rewrite as row 1; large fixture now a module-scoped template repo | 2026-10-22 | f14c4f49 |
| 3 | tests/unit/test_admission_check.py::test_task_count_boundary_edges[8-10-True] | retained | (same id) | param id and assertions unchanged (exit/decision/measured fr+task); mechanism rewritten (in-process call, template clone+variant commit) | 2026-10-22 | f14c4f49 |
| 4 | tests/unit/test_admission_check.py::test_task_count_boundary_edges[30-40-True] | retained | (same id) | as row 3 | 2026-10-22 | f14c4f49 |
| 5 | tests/unit/test_admission_check.py::test_task_count_boundary_edges[7-40-False] | retained | (same id) | as row 3 | 2026-10-22 | f14c4f49 |
| 6 | tests/unit/test_admission_check.py::test_task_count_boundary_edges[31-40-False] | retained | (same id) | as row 3 | 2026-10-22 | f14c4f49 |
| 7 | tests/unit/test_admission_check.py::test_task_count_boundary_edges[12-9-False] | retained | (same id) | as row 3 | 2026-10-22 | f14c4f49 |
| 8 | tests/unit/test_admission_check.py::test_task_count_boundary_edges[12-41-False] | retained | (same id) | as row 3 | 2026-10-22 | f14c4f49 |
| 9 | tests/unit/test_admission_check.py::test_narrow_task_pattern_only_for_admission | retained | (same id) | both variants' assertions unchanged (narrow-9 rejected with wide-mode message; narrow-10 admitted, task_count 9/10); mechanism rewritten (two template clones) | 2026-10-22 | f14c4f49 |
| 10 | tests/unit/test_admission_check.py::test_fr_definition_pattern_pinned | retained | (same id) | FR-pattern pin literal and both variants' assertions unchanged (fr_count 7 rejected / 8 admitted); mechanism rewritten | 2026-10-22 | f14c4f49 |
| 11 | tests/unit/test_admission_check.py::test_fr_count_excludes_sc_rows | retained | (same id) | assertions unchanged (exit 0, fr_count 8 with 19 SC rows present); mechanism rewritten | 2026-10-22 | f14c4f49 |
| 12 | tests/unit/test_admission_check.py::test_missing_or_unparseable_tasks_fail_closed | retained | (same id) | fail-closed assertions unchanged (exit 2 missing tasks; exit 1 empty task list, task_count 0); mechanism rewritten | 2026-10-22 | f14c4f49 |
| 13 | tests/unit/test_admission_check.py::test_missing_checklist_or_entry_fails_closed | retained | (same id) | fail-closed assertions unchanged (exit 2 missing checklist; exit 1 non-opt-in entry, decision full-chain); mechanism rewritten | 2026-10-22 | f14c4f49 |
| 14 | tests/unit/test_admission_check.py::test_sensitive_or_engine_path_rejected | retained | (same id) | all three variant assertions unchanged (criteria c fail engine path; d fail sensitive path; d fail sensitive content); mechanism rewritten (three template clones) | 2026-10-22 | f14c4f49 |
| 15 | tests/unit/test_admission_check.py::test_lines_manifest_syntax_pinned[# comment\n\n012-medium\|012-medium\n] | retained | (same id) | manifest syntax pin literals unchanged; per-row pass/fail assertions unchanged; mechanism rewritten | 2026-10-22 | f14c4f49 |
| 16 | tests/unit/test_admission_check.py::test_lines_manifest_syntax_pinned[012-medium\|012-medium\|extra\n] | retained | (same id) | as row 15 | 2026-10-22 | f14c4f49 |
| 17 | tests/unit/test_admission_check.py::test_lines_manifest_syntax_pinned[012-medium \| 012-medium\n] | retained | (same id) | as row 15 | 2026-10-22 | f14c4f49 |
| 18 | tests/unit/test_admission_check.py::test_lines_manifest_syntax_pinned[012/medium\|012-medium\n] | retained | (same id) | as row 15 | 2026-10-22 | f14c4f49 |
| 19 | tests/unit/test_admission_check.py::test_lines_manifest_syntax_pinned[012-medium\|012-medium\nother\|other\n] | retained | (same id) | as row 15 | 2026-10-22 | f14c4f49 |
| 20 | tests/unit/test_admission_check.py::test_multiline_or_branch_mismatch_lines_manifest_rejected | retained | (same id) | both variant assertions unchanged (manifest-branch mismatch; expected-branch mismatch, criterion e fail); mechanism rewritten | 2026-10-22 | f14c4f49 |
| 21 | tests/unit/test_admission_check.py::test_open_clarification_marker_rejected | retained | (same id) | assertion unchanged ([NEEDS CLARIFICATION: marker → criterion f fail); mechanism rewritten | 2026-10-22 | f14c4f49 |
| 22 | tests/unit/test_admission_check.py::test_unresolved_related_feature_rejected | retained | (same id) | both variant assertions unchanged (related 099 not in registry; missing feature detail → criterion f fail); mechanism rewritten | 2026-10-22 | f14c4f49 |
| 23 | tests/unit/test_admission_check.py::test_exit_codes_0_1_2 | retained | (same id) | kept as THE CLI subprocess pin (T004): 3 true sys.executable invocations asserting exit 0/1/2 verbatim; exit-0 case additionally pins --json-out payload file (strengthened, LED-07-compliant); repos from template clones | 2026-10-22 | f14c4f49 |

LED-08 note (reportive, no rows): two same-shape sibling rows ADDED to
`test_task_count_boundary_edges` at f14c4f49 — `[30-10-True]` (fr upper × task lower, inside
window) and `[7-9-False]` (both below lower bounds). New coverage, post-only ids.
