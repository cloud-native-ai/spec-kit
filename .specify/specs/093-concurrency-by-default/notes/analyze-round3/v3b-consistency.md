# V3B — counts, stale-value and internal-consistency verification (analyze round 3)

**Verifier**: fork worker V3B (read-only; this file is the only write)
**Worktree**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/093-clarify`
**Branch / HEAD**: `093-concurrency-by-default` @ `8c90088c` (repair commit `86b9e43c`, base `780dfa82`)
**Objects under test**: `requirements.md`, `plan.md`, `tasks.md`, `feature-ref.md`, `quickstart.md`, `checkpoints/01…06`, `contracts/*`, `register.md`, `.specify/state/093-concurrency-by-default.md`, against the post-repair state (FR 35 / tasks 152 / clauses 94).
**Method**: every count re-measured from the files with independent scripts (not by trusting the artifacts' own totals or the repair ledger); `validate-tasks.py` and `decomposition-check.py` re-run today; no mutation testing (read-only mandate), so each validator check is inspected for a non-empty subject instead.
**Anomaly discipline**: this run made no edit; any anomaly is listed in § 8/§ 9 and closed in the final message. No subagent was dispatched.

---

## 1. Counts table (measured today, from the files)

| Quantity | Expected / claimed | Measured | Status |
|---|---|---|---|
| FR definitions | 35 | **35** — `^- \*\*FR-NNN\*\*:` lines; ids FR-001…FR-035 contiguous, 0 gap, 0 duplicate | ✅ |
| Success criteria | 12 | **12** — SC-001…SC-012; `Path` split 6 `final` (SC-001…SC-006) / 6 `supporting` (SC-007…SC-012), matching DoD-7 and GATE-4 | ✅ |
| Contract clause definitions | (unstated by the brief) | **94** — C-001…C-094 contiguous, each exactly once; per file: declaration-facts 18, judgement-engine 22, executor-obligations 22, high-order-executors 18 (incl. C-093/C-094), existing-semantics-disposal 14; index file claims "94 clauses in total" | ✅ |
| Task rows | T001–T152 | **152** rows, T001…T152 contiguous, ascending, 0 duplicate, 0 missing | ✅ |
| Package-map coverage | each row exactly one package | **152/152** rows assigned exactly once: WP1 16 + WP2 26 + WP3 24 + WP4 37 + WP5 49 = 152; 0 unassigned, 0 multi-assigned | ✅ |
| Green-point claims | no duplicate (contract, clause) | **37 claims / 37 distinct clauses**; 0 duplicate clause, 0 duplicate (path, clause), 0 dangling (every named clause exists in the named contract file); validator records the same 37 | ✅ |
| Row-level `[blockedBy:]` tags | resolvable | **0 tags present** (format documents the tag; no row uses it) → the validator's edge check has no subject; package-level `blockedBy` column (`WP2←WP1`, `WP3←WP1`, `WP4←WP1`, `WP5←WP1/WP2/WP3/WP4`) resolves to declared packages | ✅ (edge check vacuous, not contradicted) |
| Feature-ref maps | 35 FR rows / 12 SC rows | **35 distinct FR ids, contiguous; 12 distinct SC ids, contiguous** | ✅ |
| Shared strings / Runtime Stack | 11 / 5 | **11 STR rows (STR-001…STR-011), 5 RS rows (RS-001…RS-005)** | ✅ |
| `validate-tasks.py` (rerun today) | 0 error / 0 warning | `PASS — 0 error(s), 0 warning(s)`, EXIT 0, 37 green claims emitted | ✅ |
| `decomposition-check.py --mode tasks` (rerun today) | proceed | `{"decision": "proceed", "measured": {"fr_count": 35, "task_count": 152, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": []}`, EXIT 0 | ✅ |

Cross-reference sweep: every `T-NNN` cited in requirements/plan/feature-ref/quickstart/checkpoints resolves inside T001–T152 (0 dangling); max FR ref 35, max SC ref 12, max clause ref C-094 — no out-of-range reference anywhere in `tasks.md`.

---

## 2. Green-point attribution detail

- Claims per contract: declaration-facts C-001/C-002/C-003/C-011/C-013/C-014/C-015/C-016 (8); judgement-engine C-019…C-025, C-028, C-030…C-036 (15); executor-obligations C-042/C-043/C-046/C-061 (4); high-order-executors C-063/C-067/C-068/C-070/C-072/C-093/C-094 (7); existing-semantics-disposal C-079/C-082/C-084/C-092 (4). Sum 37; no clause claimed twice.
- The marker reading (F-093-004 ruling) is the one the file uses: 57 of 94 clauses stay unclaimed and that is admissible (DoD-1: "a feature MAY claim a strict subset"), while every claim resolves.
- The validator's other structural checks have non-vacuous subjects: story-label check runs over 5 story phases; DoD-format over the DoD block; green checks over 37 real claims. Only `blockedBy` is vacuous (no row-level tags). **The 0/0 is earned, not vacuous.**

---

## 3. Package map and decomposition risk

| Package | Rows | Count |
|---|---|---|
| `WP1-facts` | T001–T013, T014, T026, T098 | 16 |
| `WP2-engine` | T021–T025, T030–T033, T051–T056, T074–T077, T095–T097, T109, T113, T119, T138 | 26 |
| `WP3-owners` | T037, T041, T060, T061, T078, T100, T114–T115, T120–T122, T132, T135, T139–T140, T142, T144–T151 | 24 |
| `WP4-tests` | T015–T016, T018, T020, T027, T029, T042, T044, T046–T050, T057, T066–T073, T086–T087, T089, T091, T092, T094, T106–T107, T123, T125, T129, T136, T141, T143, T152 | 37 |
| `WP5-release` | T017, T019, T028, T034–T036, T038–T040, T043, T045, T058–T059, T062–T065, T079–T085, T088, T090, T093, T099, T101–T105, T108, T110–T112, T116–T118, T124, T126–T128, T130–T131, T133–T134, T137 | 49 |

- **Partition exact**: union = {1…152}, no overlap, no gap — matches `tasks.md:358` "Every one of the 152 rows appears in exactly one package".
- **Repair placement**: T144–T151 sit in `WP3-owners`, T152 in `WP4-tests`; no new package was declared and none was needed. Both packages were already above the ~10-row guidance before the repair (WP3 16→24, WP4 36→37), and the deviation is recorded at `tasks.md:370` as deliberate (write-domain boundary, not row count).
- **Slot budget**: the declared concurrency cap is `decomposition_slot_cap: 6` (spine) with `verifier_reserve: 1`; the map presents at most 3 ready-together units (WP2/WP3/WP4 after WP1) → 3 ≤ 5 usable slots. **No package breaches a declared slot budget.**
- **Only split trigger in sight**: the feature-level task ceiling 160 — 152 leaves **8 rows** of headroom; ≥ 9 added rows would flip `decomposition-check` to `split-required`. No package-level hard row budget is declared anywhere.

---

## 4. Stale-value sweep (the four pre-repair families: 33 FR / 137 tasks / 92 clauses / 5 packages)

### 4.1 Surviving LIVE stale value — 1

| # | Location | Claim | Measured today | Class |
|---|---|---|---|---|
| **V3B-F1** | `tasks.md:79` (T006, open row) | "confirm **92** clauses by `grep -c '^- \*\*C-[0-9][0-9][0-9]\*\*'` over the five clause-bearing files" | the row's own command returns **94** (18+22+22+18+14). An implement executor running T006 as written gets a value that contradicts the row's expected value; the freeze step is keyed to this count | **LIVE → finding (MEDIUM)** |

### 4.2 Surviving values classified as dated records — not findings

| Location | Value | Why not a finding |
|---|---|---|
| `plan.md:330` | "the plan stage shipped 92; C-093/C-094 were added by the analyze-repair 2026-11-09 rulings" | explicit dated caveat; live count in the same row is 94 |
| `plan.md:334` | "33 FR was the count at that reading; 35 after the analyze-repair added FR-034/FR-035" | explicit dated caveat |
| `plan.md:339` | "92 clauses against an expected ~70 (94 after the analyze-repair rulings…)" | explicit dated caveat |
| `checkpoints/02-clarify.md:6` | "live counts after integration: 33 FR / 12 SC (6 final / 6 supporting)" | clarify-stage checkpoint = dated stage record (and the file carries the round-2 dated note discipline) |
| `checkpoints/03-plan.md:7,11` | "92 clauses (C-001…C-092)", "33 FR map rows", "proceed, 33 FR" | plan-stage checkpoint = dated stage record |
| `checkpoints/04-tasks.md:7,10,40,51,61` | "137 task rows T001–T137", "5 work packages", "33 FR / 137 tasks", "34 green markers" | tasks-stage checkpoint = dated stage record; V2B § observation 2 reached the same classification |
| `checkpoints/06-analyze.md:12,60` | "33 FR / 137 tasks", "137-row file" | analyze-round-1 checkpoint = dated stage record |
| `checkpoints/01-requirements.md:5` | "36 FR / 12 SC; 8 final / 4 supporting; 7 shared strings" | requirements-stage checkpoint = dated stage record |
| `requirements.md:289` | "FR 由 36 条变为 **33 条**" | Clarifications history; the file itself (`:267`) declares such numbers historical and non-citable as current |
| `register.md:197` (F-093-004) · spine findings line | "093 认领 92 中的 35" / "25/33", "35 of 92", "18 of 92" | dated resolution/narrative records ("resolved（2026-11-09, analyze）"); the current claim reading is 37 of 94 (§ observation 1) |
| `tasks.md:428` | "PASS … over 143 rows" | explicitly dated run record ("Run of 2026-11-09 (analyze-repair)") |

### 4.3 The "5 packages" family

No stale claim exists: the package count is **still 5** after the repair (`tasks.md:370` "152 rows over 5 packages" is current; `checkpoints/04` "5 work packages" is the dated tasks-stage record). Plan's "five independent work packages — P1…P5" is a different partition (planning-run work packages) and is also still five.

No surviving live claim of "137 tasks" or "33 FR" was found outside dated records and explicit caveats.

---

## 5. New rows T144–T152 — structural validity

| Check | Result |
|---|---|
| Existence & contiguity | T144…T152 present, ascending, unique; each is a well-formed `- [ ] TNNN` row | ✅ |
| Phase placement | all nine in `## Phase 8: Polish & Release (Cross-Cutting)` — the non-story phase; matches `plan.md:422` ("Task rows T144–T152 are appended in Phase 8") and `tasks.md:342` | ✅ |
| Story labels | zero `[US` markers — required for a non-story phase (validator's `story-labels` rule agrees) | ✅ |
| `[P]` markers | none — no parallelism claim that would need write-domain proof | ✅ |
| `[green:]` tags | none — consistent with the marker reading: these rows refine the already-marked FR-035/C-094 surface (C-094 is claimed once, by T142); a second claim would trip `green-clause-collision` | ✅ |
| Row-level `blockedBy` | none; phase gating stated in prose at `tasks.md:342` ("gated only on T021–T025 … for the test half"); package-level `blockedBy` (WP3←WP1, WP4←WP1) resolves | ✅ |
| DoD references | DoD-1's marker semantics satisfied (no re-claim); DoD-2 satisfied (validate-tasks PASS); DoD-8 disposition language present in T144/T145 ("dispose the old 'MUST NOT 启动 qodercli' rule in FR-033's list"); no DoD item is contradicted | ✅ |
| Cross-refs | each row cites `(FR-035, C-094)`; T144/T145 also cite F-093-020, which is registered (`register.md:200`, open — the intended state); every task id referenced resolves | ✅ |
| Manifest reachability | the 20-row manifest in `plan.md` § Complete-correction manifest maps every surface to existing rows (T144–T152 for the 15 newly covered ones; pre-existing rows for the 5 baseline ones); that the baseline surfaces' *content* is complete is V1B's finding, not a structural defect here | ✅ |

**`validate-tasks.py` rerun (today, HEAD 8c90088c)**: `PASS — 0 error(s), 0 warning(s)`, EXIT 0; JSON reports 37 green claims and empty error/warning arrays. The 0/0 is earned (§ 2). The round-2 run record at `tasks.md:429` ("PASS … over 152 rows") matches the rerun.

---

## 6. Registry and spine

| Check | Reading | Status |
|---|---|---|
| Grouped verification row `V2/V3@093-analyze-round2` | present at `register.md:201`, status `closed 2026-11-09 (repair round 2 …)`, pointing at `notes/analyze-round2/v2-gates-directive.md` + `v3-trunk-reconciliation.md` + `notes/analyze-repair2.md` § 1–§ 3 | ✅ |
| F-093-019 (duplicate-092 record) | present at `register.md:199` (`recorded`); carried in the spine findings line (`state/093-concurrency-by-default.md:89`); T090 disambiguated in place; suite name kept | ✅ |
| F-093-004 | stays **resolved**: `register.md:197` "resolved（2026-11-09, analyze）" with owner `templates/tasks-template.md` L110 and implement row T138; spine line 89 "RESOLVED" | ✅ |
| F-093-003 | stays **adjudicated**: `register.md:196` open with the analyze adjudication recorded (deliverable carried by T096/T098/T101/T105, C-072 fail-closed; value = owner decision); spine line 89 "ADJUDICATED at analyze 2026-11-09" | ✅ |
| F-093-020 (cited by T144/T145) | registered at `register.md:200`, status `open` (the intended implement-time convergence) | ✅ |
| Spine current state | `next_action` = analyze round 3 dispatch; `last_verdict` states "validate-tasks 0/0 over 152 rows … decomposition proceed 35 FR / 152 tasks"; `breakpoint_verdict` READY-FOR-ANALYZE-ROUND-3 | ✅ |

---

## 7. Decomposition verdict

`decomposition-check.py --mode tasks`: **proceed** — FR 35/120, tasks 152/160, no reason. The eight-row headroom is the only proximity-to-ceiling signal; the package map stays at five packages with no declared slot-budget breach (§ 3). No split-required trigger has fired.

---

## 8. Findings (scored)

| id | severity | finding | anchor |
|---|---|---|---|
| **V3B-F1** | **MEDIUM** | A live, still-open task row states the pre-repair clause count as its expected value. T006 instructs the implement executor to "confirm **92** clauses by `grep -c '^- \*\*C-[0-9][0-9][0-9]\*\*'` over the five clause-bearing files"; the command today returns **94** because repair round 1 added C-093/C-094. Executing the row as written produces an expected-vs-actual contradiction at the very step that freezes the clause-coverage baseline (`coverage-baseline.txt`), and could leave the baseline keyed to a stale clause count. Fix shape: replace 92 with 94 (or, better, drop the restated number and read the count from the contract files in the same command). | `tasks.md:79` (T006) vs `contracts/*.contract.md` (`grep -c` = 18+22+22+18+14 = 94); `plan.md:330` already records the 92→94 movement |
| **V3B-F2** | **LOW** | A live quickstart paragraph points at a scenario id that does not exist: "that is the point of S-1 and S-9" — the page defines S-0…S-6 only (7 scenarios), and `plan.md:331` independently states "7 scenarios (S-0…S-6)". The reference is dangling in every revision of the file (`git log -S 'S-9'` shows it arrived with the original quickstart). Fix shape: name the real scenario(s) (S-1 plus the scenario that actually demonstrates the unregistered-fact red, i.e. S-5/C-039, or S-0), or drop the pair. | `quickstart.md:8` vs `quickstart.md` § S-0…S-6 and `plan.md:331` |

---

## 9. Observations (disclosed, not scored)

1. **Claim-reading drift in dated records**: `register.md:197` and the spine findings line still read "093 认领 92 中的 35". The current measured reading is **37 claimed of 94** (validator: 37 green claims; V2B's G2 rerun: "claimed clauses (this feature): 37"). Both are dated resolutions/narratives, not live counts, so they are not findings under the stated rule — but a future reader must not lift the number.
2. **`plan.md` EP-003 / Technical Context / T005 "23 facts"**: the reader now lists **24** facts (the merged trunk added `shared/declarations/non-disposable-review-surface.yaml` after the plan-stage measurement). Every affected line carries "measured 2026-11-09", so it is a dated reading, not a live claim; the substantive premise (list = 9 contract keys + fact slugs; `--action get --fact concurrency-class` exits 1) still holds verbatim (re-measured today: 9 keys, 24 facts, exit 1).
3. **DoD-1 totality sentence**: "every contract clause C-001…C-094 is owned by at least one row" has no machine owner; measured, 42/94 clauses are named by at least one task row and the cited `feature-ref.md` map covers 69/94 clauses (and is FR→clause, not clause→row, and explicitly "asserts no totality of its own"). The sentence predates both repair rounds (range endpoints only were bumped C-092→C-094) and may be true under a substantive reading of "owned"; flagged as an observation because "owned" is undefined, not because a contradiction was measured.
4. **`plan.md:52` wording**: "10 new contract test modules" aggregates 9 contract modules + 1 unit module (the same 10 files DoD-3 and `feature-ref.md:94` count correctly as 9+1). Count right, label loose.
5. **Enumeration readings re-measured**: 38 `skills/internal` / 16 `skills/external` / 29 command stems / 17 agents / 12 teams / 6 anchoring — all match T003 and quickstart S-1. Note `ls -d .specify/skills/*/` returns 17 directories (16 flat external projections + the `internal/` container); the artifacts' "16 flat external projections" remains correct under its own wording, and the 54 = 38+16 trap arithmetic holds.

---

## Verdict

- Counts: FR 35, SC 12, clauses 94, tasks 152 contiguous/unique, package map an exact 152-row partition, green claims 37/37 resolvable with zero duplicates — all correct.
- Stale-value sweep: exactly **one** live stale value survived (T006's "92 clauses"); every other occurrence of 33/137/92/5 is a dated record or carries an explicit caveat.
- T144–T152: structurally valid (non-story Phase 8, no [US]/[P]/[green] tags by design, no dangling edges, registered F-093-020); `validate-tasks.py` 0/0 re-earned.
- Registry/spine: grouped V2/V3 row, F-093-019, F-093-004 resolved, F-093-003 adjudicated — all as required.
- Decomposition: proceed (35/120 FR, 152/160 tasks); no slot-budget breach; 8-row headroom to the task ceiling.

**V3B: FAIL — V3B-F1 (MEDIUM: tasks.md T006 live "confirm 92 clauses" vs 94 measured), V3B-F2 (LOW: quickstart.md:8 dangling scenario "S-9").**
