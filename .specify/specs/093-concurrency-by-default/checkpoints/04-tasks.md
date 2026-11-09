# Checkpoint 04 — tasks

## 1. Artifact verification
- sentinel target: `tasks.md`
- live counts: **137** task rows `T001`–`T137` (`grep -c '^- \[ \] T'`), contiguous and unique; **8** phases (Setup 7 / Foundational 19 / US1 15 / US2 24 / US3 20 / US4 20 / US5 6 / Polish 26); **5** work packages covering every row exactly once (checked by set union = `{1..137}`, no duplicate membership); **34** `[green: <contract>#<clause>]` red-first markers.
- gates, all evidence retained under `test-evidence/`:
  - `validate-tasks.py` → **PASS — 0 error / 0 warning** (`validate-tasks.txt`). The first run of this stage measured 2 errors / 277 warnings; the convergence to zero is recorded in the artifact's `## Notes` § Validator adjudication.
  - `decomposition-check.py --mode tasks` → **proceed**, 33 FR / 137 tasks, ceilings 120 FR / 160 tasks (`decomposition-tasks.json`).
  - `pre-analyze-check.py --stage tasks` → **decision=pass**, 0 error / 101 advisory (`pre-analyze-tasks.json`). Two genuine in-stage fixes and one inherited one: a stale task-count claim in `quickstart.md` (62 → the 091 baseline record, cited instead of restated); `RS-003` / `RS-004` FR ownership resolved by line-level FR references on T002/T014/T016/T084; and `plan.md` § Inherited Blockers row 1 re-carriered from a gate id that did not exist to `gate:GATE-7`, which this stage added.
- **Anomaly disclosed, not hidden**: `validate-tasks.py` and the `create-tasks` skill disagree on the semantics of `[green: …]`. The validator enforces a one-row-per-clause partition; the skill describes the tag as a red-first marker. The two contracts cannot both be satisfied by one artefact — satisfying the validator forces untagging rows whose red-first work is real. This stage adopted the marker reading, restored the red-first rows, kept the partition discipline that the validator can still check, and recorded the divergence below as a decision that must be ratified.

## 2. Temporary Goal progress
| criterion | degree | evidence_ptr |
|---|---|---|
| 各执行体声明 default-concurrent 与具名串行例外 | partial (rows allocated) | US1 rows T027–T041 and US2 rows T042–T065; owner surfaces T037/T056/T060; verification T065 |
| 契约测试可判别 default-concurrent / serial-exception | partial (modules allocated) | the ten module rows T015–T020, T027/T029, T042–T050, T066–T073, T086–T094, T106/T107, T123/T125/T129/T136; each SC has a named module row |
| 至少一个真实执行体完成 6 包 worktree 并发与确定性集成 | **not_evaluated** (unchanged, and named as a gap) | § Work Packages § SC-006 evidence plan: the partition is ready (WP2/WP3/WP4 disjoint, ready together after WP1) but this stage's executor has no dispatch tool; T106 is the row that records it as `not_evaluated` |
| 派发能力在位，禁止声明并行而实际串行 | partial (rows allocated) | US4 rows T086–T105 (capability action, 092 reproduction fixture T090, anti-nesting T091) plus T098 which registers the verdict without answering it |

## 3. Team configuration review
- evidence: the partition is genuinely parallel — three packages (WP2 engine, WP3 owners, WP4 tests) with **pairwise-disjoint file-level write domains**, ready together once WP1 closes; the cap is measured at dispatch, never copied
- symptom: **the executing agent still has no dispatch tool**, so this stage ran serially, one executor, exactly as the plan stage did
- proposal: none — changing the roster does not create a dispatch tool; the mechanism is this feature's own delivery
- ratification: n/a; applied: n/a
- **disclosure**: "partition ready but execution serial" is stated in the artifact (§ Work Packages), here, and in the return; SC-006 is `not_evaluated`, never `0` and never an estimate

## 4. Next stage concurrency / roster
- requested: the spine's `agent_concurrency_requested`; effective: **1**; reason: `mechanism-not-yet-landed` ([[STR-010]])
- stage max_parallel: 1 for the remaining planning stages (checklist, analyze); the implement stage is the first that may genuinely dispatch, carrying WP2/WP3/WP4 in one round
- roster: single tasks coordinator; next stage = **checklist** in the same worktree/branch

## 5. Direction audit
- reload tier: T0 (stage start) + T1 (after each of the three artefact rewrites) + T2 (at wrap-up)
- Q1 rules: unattended; no approval request; U4 → next stage; spine before action; workspace guard (writes confined to the worktree); fast-fail; gate discipline; budget; report discipline — all in force
- Q2 process: pass with corrections applied in-passing and disclosed — (a) a dangling clause id (`C-023` on an executor-obligations row that has no such clause) re-pointed to `C-060`; (b) 26 duplicated clause claims collapsed, each duplicate being a second view of work already marked; (c) the US2 implementation block, which had been left with three duplicate rows and duplicate ids, rewritten end to end; (d) the § Dependencies and § Work Packages row references re-derived from the final numbering rather than carried over; (e) a framework-observation id invented in T060 replaced by a path reference; (f) a stale `62 tasks` claim in `quickstart.md` replaced by a citation of the baseline record; (g) `plan.md`'s inherited-blocker carrier re-pointed to the gate this stage actually defines
- Q3 next action: pass — checklist is the next stage and its inputs (137 rows, 5 packages, 10 modules, GATE-7) are named in the artefact
- Q4 spine freshness: pass — updated after this checkpoint with the tasks verdict, the gate readings, `wrapup_tasks` and `next_action: checklist`
- Q5 territory/workspace: pass — no write outside the worktree; the main worktree untouched; no push
- verdict: **correction-applied** — every item above had exactly one reading consistent with the recorded intent and was repaired locally; the one item that does **not** have a single reading is the `[green:]` semantics disagreement, and it is escalated below rather than settled here

## 5b. Published-state check
- scope: n/a — no history correction (part 5's `correction-applied` covers in-stage artifact corrections, not a branch correction)
- disposition: n/a — nothing to converge

## 6. Disclosed rulings (in-stage, recorded where they bind)
1. **[green: …] is a red-first marker, not a clause-registration table.** Adopted because `create-tasks` defines it that way and because the alternative (one row per clause) forced untagging rows whose tests are genuinely red-first. Consequence: DoD-1 was rewritten from "every clause claimed by exactly one row" to "every FR row resolves to an implementation row; the tag appears at most once per (module path, clause)". **This needs ratification**: `validate-tasks.py`'s rule text says otherwise, and the two cannot both be true. Recorded as the stage's headline anomaly.
2. **Package boundary = write domain, not row count.** 137 rows over 5 packages is far above the ~10-row guidance; splitting further would put two packages on one file, which FR-012 forbids. Recorded as a deliberate deviation.
3. **SC-006 is `not_evaluated`.** The partition and the evidence plan are complete; the executing body cannot dispatch. The honest value is `not_evaluated`, with the gap named as the missing capability rather than missing work.
4. **The coordinator verdict stays unadjudicated.** T098 authors the fact; the question is not answered in this artefact (F-093-003 stays open).
5. **US1–US4 form the MVP.** Splitting them would deliver half a mechanism (a closed set with no judgement, or a judgement with no set).

## 7. Residual risk
- **R-1**: the ten test modules and `concurrency-check.py` do not exist, so every path they name is a creation target — the 101 `missing-path` advisories are this fact, not a defect, but they will mask a genuine typo until the modules land.
- **R-2**: the `[green:]` semantics disagreement (ruling 1) means a later stage re-running `validate-tasks.py` after adding tags could see warnings reappear; the rule needs one owner before implement starts.
- **R-3**: SC-006 cannot close from any stage whose executor lacks a dispatch tool; if the implement executor is the same, the feature ships with SC-006 `not_evaluated` and the gap named.
- **R-4**: the coordinator verdict (F-093-003) blocks the static half of SC-005 until an owner rules.
- **R-5**: 137 rows is a large artefact; a later stage that edits row content without re-running the two gates will not notice a re-broken sequence.
