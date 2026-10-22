# SC-007 Coverage Audit (LED-05 inline join) — 2026-10-22 · T035

**Owner of this record**: T035 (Phase 9 closure slot). **Method authority**: `contracts/consolidation-ledger.md` LED-05/LED-06; E4 dual lists (`data-model.md` §E4); W-1 roster join ruling = `pinned-roster-addendum-2026-10-22.md` (executed in the T036 record, cross-referenced here).
**Inputs**: `test-evidence/baseline-test-ids.txt` (E4 baseline, 4551 ids) × `test-evidence/post-test-ids-2026-10-22.txt` (E4 post, T033, 5239 ids) × `test-evidence/test-consolidation-ledger.md` (89 rows after LED-03 corrections, see §3).
**Join procedure**: deterministic inline python (throwaway, run once; logic transcribed below), same collection-method lists per V-E4-1.

## 1. List reconciliation (comm)

```text
baseline body ids = 4551 (unique)     post body ids = 5239 (unique)
comm -23 baseline post (missing)  = 38
comm -13 baseline post (post-only)= 726
arithmetic: 4551 − 38 + 726 = 5239  ✓ (post total matches E1 closure collect)
```

## 2. Layer cross-check (E1 closure layer_counts × E4 head note)

| layer | baseline (E4 head note anchor) | computed from baseline ids | post (E1 closure record) | computed from post ids | delta |
|---|---|---|---|---|---|
| contract | 3426 | 3426 ✓ | 4097P + 14F = 4111 | 4111 ✓ | +685 |
| unit | 734 | 734 ✓ | 736P + 0F | 736 ✓ | +2 |
| integration | 391 | 391 ✓ | 391P + 1S = 392 | 392 ✓ | +1 |
| total | 4551 | 4551 ✓ | 5239 (= 14F+5224P+1S) | 5239 ✓ | +688 |

Delta explanation (exact, id-level): contract +685 = 723 new suite params − 38 folded contract ids; unit +2 = the two LED-08 sibling params `test_task_count_boundary_edges[30-10-True]` / `[7-9-False]`; integration +1 = the LED-08 CLI smoke test. No unexplained delta.

## 3. LED-05 join — missing set → ledger (38/38)

**Missing set = exactly 38 ids, all `tests/contract/` layer.** Coverage mapping by disposition:

- 30 ids match case-merge rows literally (full node id = row `original_id`).
- 8 ids are members of two parametrized loops whose ledger rows (54, 76) recorded the **base-id form** (`...::test_mirror_identical`, `...::test_ca3_skill_mirror_identical` — no `[param]` suffix), deviating from the E2 rule "original_id = full node id (case-level)". The strict full-id join initially reported these 8 as unmatched.
- **In-passing repair (LED-03 correction, disclosed)**: coverage was verifiably intact — both rows' `retained_equivalent_id` enumerate exactly the 3 + 5 covering suite params, and all 8 params are present and green in the post list. The strict-literal reading (8 silent deletions) is contradicted by the artifacts themselves, so per the fast-fail correction criterion the defect was repaired by the ledger's own sanctioned mechanism (LED-03: corrections are new rows): rows 82–89 appended to `test-consolidation-ledger.md` recording the 8 full node ids. No earlier row rewritten; append-time HEAD `373f4b32`; rows land in the P16 closure commit.
- **Post-correction strict join: unmatched = 0** (LED-06 bar met, no tolerance logic needed).
- Missing ⊆ folded: yes — the folded set (44 distinct case-merge original ids) = 38 missing full ids + the 2 base-id forms of rows 54/76 + 4 ids whose case-merge rows record an assertion-level fold while the id itself survives in post (row 71 ×2 `test_mirror_is_byte_equivalent[summarize-project|study-project]`, row 78 `test_c1_seed_exists_and_mirror_is_byte_identical`, row 81 `test_c2_mirror_carries_the_section_and_is_byte_identical`; each verified present in the post list, extra assertions retained in file per LED-07).
- Retained-row sanity: 46 retained rows, all with `original_id` present in the post list (0 gone).
- Green-coverage check: every missing id maps to ≥1 suite param present in the post list and absent from the 14-name closure failure list → **0 missing ids without green coverage**.

## 4. Post-only ids (LED-08, reportive — not audited)

726 post-only = **723** new `tests/contract/test_mirror_parity_suite.py::` ids (717 `test_mirror_file_byte_identical` params + 6 sibling pin functions of the new suite file) + **3** same-shape additions recorded in the ledger's LED-08 notes:

- `tests/integration/test_trigger_telemetry.py::test_cli_subprocess_smoke_pins_payload_and_exit_semantics` (T013/FR-020)
- `tests/unit/test_admission_check.py::test_task_count_boundary_edges[30-10-True]` (T005)
- `tests/unit/test_admission_check.py::test_task_count_boundary_edges[7-9-False]` (T005)

723 + 3 = 726 (exact; no unclassified post-only id).

## 5. Verdict

- **SC-007 / GATE-2: PASS** — zero silent deletion (unmatched = 0 post-correction); E4 dual lists reconciled; three layers all executed in the closure run; missing set fully ledger-mapped to green coverage.
- Ledger form-defect repair disclosed: rows 82–89 (this audit; LED-03).
- Note: post list header records tree `00287a38` (T033/T034 executed at that tree; their evidence committed as `e6c3e655`). No test file changed between `00287a38` and current HEAD (diff touches only spec evidence + spine), so the post list is valid at HEAD.
