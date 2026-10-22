# SC-008 Drift-Protection Audit (name-level diff + W-1 roster join) — 2026-10-22 · T036

**Owner of this record**: T036 (Phase 9 closure slot). **Diff-set artifact**: `name-diff-2026-10-22.txt` (generated from the actual `comm` outputs of the committed lists; regeneration command in that file's header). **Ruling authority**: W-1 = `review.md` §4 P1-1 + `pinned-roster-addendum-2026-10-22.md`. **Failure-set semantics**: `data-model.md` §E3 (baseline failure set), contracts FB-02/FB-04/FB-06.
**No full suite was re-run for this audit** — the closure slot (T034) is the only post-change full run; per FB-04 the `--names-out` list of that run is the approved equivalent of log extraction.

## 1. Name-level diff (GATE-1)

Post names = `closure-failures-2026-10-22.txt` (T034 closure run; 14 names, sorted, one per line).

| comparison | baseline | comm -13 (NEW) | comm -23 (fixed) |
|---|---|---|---|
| **T007 in-stage baseline** (`baseline-failures-2026-10-22-implement-start.txt`, 83 — M-1 authority) | 83 | **0** | 69 |
| pre-stage list (`baseline-failures-2026-10-22.txt`, 83 — scope copy; set-identical to the T007 list, verified `comm` both directions empty) | 83 | **0** | 69 |

- **0 NEW name-level failures** against both baselines (GATE-1 bar: empty output — met).
- 69 baseline names fixed (mirror sync + triage + suite consolidation).
- The 14 remaining names are a subset of the T007 in-stage baseline (mechanically: `comm -13` empty ⇔ subset) and of the pre-stage set — **all pre-existing debt**, each carried by a dated FB-06 record (`debt-*.md`, each marked "not introduced by this scope"). i11 (`test_i11_channel_two_mirrors_and_per_tool_copies`) was fixed in `bc5c443a` and does not appear.
- **No debt name was modified during closure** (scope discipline): closure names == the triage table's 14 `pre-existing-debt` rows exactly (§3).

## 2. W-1 pinned-roster ledger join (FR-018 / FB-03)

Roster = `pinned-roster-2026-10-22.txt` (302 unique ids; the file carries 610 lines with section repeats — deduped for the set join). Validity precheck: roster ⊆ baseline id list (302/302).

Deterministic join (roster id → ledger row → suite param → post list/green), per the addendum's accepted paths:

| path | ids | result |
|---|---|---|
| 1 — id present in post list | **264** | OK |
| 2 — case-merge row → retained equivalent suite param(s) in post list **and green** | **38** | OK (all mapped) |
| gap (neither path) | **0** | — |

Path-2 details (join executed mechanically against the post list; green = not among the 14 closure failed names; the suite contributes 0 names to that list, so all referenced params are green):

- 30 exact full-id case-merge rows (including the 8 LED-03 correction rows 82–89 from the T035 audit, which resolve the base-id form defect of rows 54/76 — see `coverage-audit-2026-10-22.md` §3).
- Wildcard-form rows resolved by subtree prefix against the post list's suite params: row 58 `skills/external/git-utils/*` → **29/29 params** present and green; row 67 `skills/external/sdd-loop-driver/*` → **28/28 params** present and green (annotation counts matched exactly).
- Note: the addendum's review-time estimate "44 roster ids covered by the fold" is superseded by this recomputation (38 path-2 + the addendum's own clause that the exact join is recomputed at T036, not trusted from the summary).
- Roster coverage of the fold set: the 38 missing ids of the T035 audit are all roster members — 0 roster id vanished without mapping.

**Roster preservation verdict: 302/302 mapped to surviving coverage; pin literals and strength unchanged (LED-07 upheld; 0 `deleted` rows in the ledger).**

## 3. Triage closure recheck (V-E5-1…V-E5-3 / T029)

Fresh mechanical extraction of `failure-triage-2026-10-22.md` table rows:

- Data rows **83** / unique original ids **83** / duplicates 0 — set-equal to the FB-01 83-name baseline (0 missing, 0 extra).
- class: mirror-sync 53 / stale-pin 11 / regression 5 / pre-existing-debt 14 (= 83).
- disposition: synced 53 / pin-updated+rationale 10 / mechanism-fixed 5 / debt-registered 15 (= 83).
- **closure 14 failed names == the 14 `pre-existing-debt` class rows, exact set equality**; all 15 debt-registered rows carry dated `debt-*.md` records (the 15th = the i11 stale-pin row, fixed at `bc5c443a`).
- Pinned-class injection drill (`injection-drill-2026-10-22.md`, T028): hit / localize / reproduce / restore all confirmed — unchanged evidence base for SC-009.
- Zero NEW pinned failures in this range (§1: NEW = 0).

## 4. Verdict

**SC-008 / GATE-1: PASS** — 0 NEW name-level failures; roster 302/302 preserved under W-1; triage 83/83 closed; 14 known debt reds remain deliberately unmodified (FB-06 registered, pre-existing, not introduced by this scope). Waiver W-1 is a criterion-shape ruling (ledger-join instead of literal subset), not a test waiver.
