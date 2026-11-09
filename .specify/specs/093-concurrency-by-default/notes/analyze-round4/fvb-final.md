# FVB — final consistency verification after repair round 3 (analyze round 4, 2026-11-09)

**Worker**: FVB (read-only final consistency verification). Worktree `.specify/.tmp/sdd-loop/worktrees/093-clarify`, branch `093-concurrency-by-default`, HEAD `132bedba` (repair commit `03d19361`, spine commit `132bedba`, base `c7a8ac4f`). No edits, no commits, no push, no subagents; the only file written is this note.
**Domain**: counts, stale-value sweep, DoD/premise sentences, SC-006 status, registry/spine, decomposition headroom — after tasks 152 → 155.
**Method**: every quantity re-measured from the files with independent scripts and greps (not lifted from any artifact's own total); `validate-tasks.py` and `decomposition-check.py` re-run on today's tree; read-only throughout.

---

## 1. Counts (measured from the files today)

| Quantity | Claimed / expected | Measured | Verdict |
|---|---|---|---|
| FR definitions | 35 | **35** — `^- \*\*FR-[0-9]{3}\*\*:` count = 35, FR-001…FR-035 contiguous, 0 duplicate | ✅ |
| Success criteria | 12 | **12** — SC-001…SC-012; `Path` split 6 `final` (SC-001…SC-006) / 6 `supporting` (SC-007…SC-012) | ✅ |
| Contract clauses | 94 | **94** — per file: declaration-facts 18 + judgement-engine 22 + executor-obligations 22 + high-order-executors 18 (C-063…C-078, C-093…C-094) + existing-semantics-disposal 14 = **94**; id set equals {1…94} exactly, 0 duplicate. The 6th file (`concurrency-contracts.md`) is index-only and states "94 clauses in total" | ✅ |
| Task rows | T001–T155 | **155** — `^- \[ \] T[0-9]{3}` count = 155; scripted check: T001…T155 ascending, each +1, 0 gap, 0 duplicate | ✅ |
| Package partition | 16+26+27+37+49 = 155 | **exact partition**: `WP1-facts` 16, `WP2-engine` 26, `WP3-owners` 27, `WP4-tests` 37, `WP5-release` 49; sum 155; 0 missing from packages, 0 extra, 0 multi-assigned — every row exactly one package | ✅ |
| Green-tag claims per clause | no duplicate (page, clause) | **37 claims / 37 distinct (contract file, clause) pairs**; 0 duplicate, 0 dangling (every named clause is defined in the named file); 36 rows carry tags (T122 carries two distinct clauses). `validate-tasks.py --json`: `status PASS`, 37 green claims, 37 distinct pairs | ✅ |
| feature-ref maps | 35 FR / 12 SC | **35** distinct FR ids (contiguous 1…35) in § Delivery map; **12** distinct SC ids in § Measurement map | ✅ |
| `validate-tasks.py` (rerun today) | 0 error / 0 warning | `PASS — 0 error(s), 0 warning(s)`, EXIT 0 | ✅ |
| `decomposition-check.py --mode tasks` (rerun today) | proceed | `{"decision": "proceed", "measured": {"fr_count": 35, "task_count": 155, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": []}`, EXIT 0 | ✅ |

---

## 2. Stale-value sweep (152 rows / 92 clauses / 24-row WP3)

**Live claims found: none.** Every occurrence of the three pre-repair values sits inside a dated record, a dated caveat, or a task id (`T152`). "24-row WP3" occurs **nowhere** in the tree; the live WP3 count is **27**.

| Location | Value | Class (why not a finding) |
|---|---|---|
| `tasks.md:432` | "over **152** rows" | dated run record ("Run of 2026-11-09 (analyze-repair round 2)"); the same bullet set states it is annotated forward, and `tasks.md:433` carries the round-3 "over 155 rows" record beside it |
| `plan.md:330` | "the plan stage shipped **92**; C-093/C-094 were added by the analyze-repair 2026-11-09 rulings" | explicit dated caveat; live count 94 in the same row |
| `plan.md:339` | "**92** clauses against an expected ~70 (**94** after …)" | explicit dated caveat |
| `register.md:197` (F-093-004) | "093 认领 **92** 中的 35" | dated resolution narrative ("resolved（2026-11-09, analyze）"); live reading is 37 of 94 — disclosed residual (V3B § 9 obs 1, repair3 § 6), not a live count |
| `state/093-concurrency-by-default.md:51` | "plan U4: pass — **92** clauses … SC-006 not_evaluated" | dated plan-stage gate record |
| `state/093-concurrency-by-default.md:93` | "093 claims **35 of 92**" | dated findings narrative (analyze era); same drift disclosure as register:197 |
| `checkpoints/02,03,04,06` | 33 FR / 137 tasks / 92 clauses (C-001…C-092) | dated stage records (clarify / plan / tasks / analyze-round-1) |
| `checklists/2026-11-09-requirements-quality.md:7,74` | "137 行 T001–T137", "5 页 / **92** 条款", "T006 定 **92** 条 clause" | dated checklist review record (filename date; observations of the corpus at review time); T006 itself now reads 94 |
| `checklists/requirements.md:38` | "live counts **33 FR** / 12 SC" | clarify-stage gate-evidence record (scoped "Gate evidence (clarify stage …)") |
| `notes/*`, `test-evidence/*` | 152 / 92 / 143 / 137 readings | dated round records and captured run evidence |

The two "35 of 92" strings (`register.md:197`, spine line 93) are the known claim-reading drift already disclosed in round 3 and deliberately retained as dated narrative; the live reading is 37 claimed of 94 (measured above). No update required under the stated rule, but a future reader must re-measure rather than lift the number.

---

## 3. DoD / premise sentences that enumerate counts

| Surface | Check | Reading |
|---|---|---|
| DoD-1 endpoints | FR-001…FR-035 = 35; C-001…C-094 = 94 | **agree** |
| DoD-1 totality sentence | "every contract clause C-001…C-094 is owned by at least one row" | **FAIL — D1** (see § 7). Measured ownership: **39/94** clauses cited inside task rows; **69/94** named in the feature-ref delivery map; **72/94** anywhere in `feature-ref.md`. The only way to reach 94 in `tasks.md` is the self-referential range "C-001…C-094" inside DoD-1/Format themselves. The same DoD-1 sentence calls the FR→clause map a "complete clause→row delivery map", while that section is titled "FR → contract clause" and states "it asserts no totality of its own" (the F-093-013 closure line) |
| Environment Prerequisites (`tasks.md` § Environment Prerequisites) | no count enumerations; every referenced task id resolves (T101 / T103 / T105 / T106 / T110); FR-005(d) correction consistent with register / spine / quickstart (F-093-012) | **agree** (Python 3.11.11 ≥ 3.8 confirmed; no CI / dependency / container claims are stale) |
| Package tables | `tasks.md`: "Every one of the 155 rows appears in exactly one package", "155 rows over 5 packages"; `plan.md` P1…P5 = five planning work packages | **agree** (both statements true; plan's P1…P5 is a different, still-five partition) |

---

## 4. SC-006 and finding statuses

- **SC-006 `not_evaluated` on every surface, no pass claim anywhere**: `requirements.md` SC-006 + A4 + Clarifications 283/299; `plan.md:357,440`; `tasks.md` DoD-6, T110, § Work Packages "SC-006 MUST be recorded `not_evaluated`"; `quickstart.md:115`; `checkpoints/02:18, 03:22, 04:21, 05:8,26, 06:22`; `register.md:198` (F-093-011 accepted); spine lines 51 and 93. `verification.md` does not exist yet — correct, it is the implement-stage artifact owned by DoD-7 / GATE-4. ✅
- **F-093-004**: stays `resolved（2026-11-09, analyze）` (`register.md:197`), owner `templates/tasks-template.md` L110, implement row **T138** present and carrying the marker-reading repair. ✅
- **F-093-003**: stays `open` with the analyze 2026-11-09 adjudication recorded (`register.md:196`); spine line 93 "ADJUDICATED"; deliverable anchors T096 / T098 / T101 / T105 all exist. ✅

---

## 5. Registry and spine

- Register rows for 093 intact: F-093-001…F-093-020 (`register.md:194–200`), plus grouped verification rows `V2/V3@093-analyze-round2` (`:201`) and `V1B/V3B@093-analyze-round3` (`:202`, added by repair round 3 — the +1 line in `03d19361`).
- F-093-020 stays `open`; cited by T144, T145, T153; plan manifest rows 4 / 6 / 16 now read `T140, T153` / `T116, T133, T154` / `T037, T060, T099, T132, T155` with severity "MEDIUM (round-3 re-measure)". ✅
- Spine: `last_verdict` = repair round 3 REPAIR-DONE with the 155-row readings; `next_action` = analyze round 4 (final); `breakpoint_verdict` READY-FOR-ANALYZE-ROUND-4. Gates block carries the round-3 readings (validate 0/0 over 155, decomposition 35/155, partition 16+26+27+37+49=155). ✅
- **No artifact contradicts the spine findings list.** The one asymmetry is narrative completeness, not contradiction: the F-093-020 entry names convergence rows T140/T142 (the analyze-era set) while the plan manifest now also carries T144–T155; both are true and the later rows are recorded separately in `wrapup_analyze_repair3` and the round-3 manifest rows.

---

## 6. Decomposition headroom

| Budget | Declared | Used | Headroom |
|---|---|---|---|
| Task ceiling (feature) | 160 | **155** | **5 rows** — adding a 6th row (→161) flips `decomposition-check` to `split-required`; this is the closest split trigger |
| FR ceiling | 120 | 35 | 85 |
| Slot cap / verifier reserve | 6 / 1 (spine) | max 3 ready-together (WP2/WP3/WP4 after WP1) | 3 ≤ 5 usable — no breach |
| Per-package row budget | **none declared** (only the ~10 rows/package *guidance*) | WP1 16 / WP2 26 / WP3 27 / WP4 37 / WP5 49 | All five packages exceed the ~10-row guidance; the deviation is recorded as deliberate at `tasks.md:373` (write-domain boundary, not row count). No package can "exceed" a budget that is not declared — but if the ~10-row guidance were adopted as a budget, every package would breach, WP5 (49) worst |

---

## 7. Findings

| id | severity | surface | finding |
|----|----------|---------|---------|
| **D1** | **MEDIUM** | `tasks.md` DoD-1 | The totality sentence "every contract clause C-001…C-094 is owned by at least one row" does not agree with the measured artifacts: task rows cite **39/94** clauses, the feature-ref delivery map names **69/94**, the whole of `feature-ref.md` names **72/94** (the apparent 94 in `tasks.md` comes only from DoD-1/Format restating the C-001…C-094 range itself). The same sentence calls the FR→clause map a "complete clause→row delivery map" although that section is FR→clause and explicitly "asserts no totality of its own" (F-093-013). DoD-1's own machine form (`validate-tasks.py` 0/0, the marker reading) passes and is unaffected. Fix shape (text-level): reword to the F-093-004 marker reading — every FR resolves to a row; every `[green:]`-claimed clause is owned by exactly one row; unclaimed clauses are admissible; the FR→clause map is a human index that asserts no totality. Deferred to this round by repair round 3 (§ 6), so this is the round-4 re-judgment |

No other finding. All count, stale-value, SC-006, registry and decomposition checks are green; no gate was weakened; no live stale 152/92/24 claim survives.

---

## Verdict

**FVB: FAIL — D1 (MEDIUM): `tasks.md` DoD-1's totality sentence ("every contract clause C-001…C-094 is owned by at least one row") is contradicted by measurement (39/94 task-row citations, 69/94 delivery-map clauses, 72/94 anywhere in feature-ref) and mislabels the FR→clause map as a "complete clause→row delivery map" that "asserts no totality of its own". Everything else — FR 35 / SC 12 / clauses 94 / 155 contiguous rows / exact 16+26+27+37+49 partition / 37 distinct green claims / no live stale counts / SC-006 not_evaluated everywhere / F-093-004 resolved + F-093-003 adjudicated / 155 ≤ 160 — is green.**
