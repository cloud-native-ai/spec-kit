# Checkpoint 05 — checklist

> **Correction (2026-11-09, analyze-repair · F-093-012)**: the claims in §2 / §3 that the executing body holds "no dispatch tool" are false — it holds a host dispatch tool (measured by the analyze stage itself), and a tool set is a per-run probe, not a constant. The dated body is left as written; the corrected premise lives in `tasks.md` § Environment Prerequisites and the ledger `notes/analyze-repair.md` § F-093-012.

## 1. Artifact verification
- sentinel target: `checklists/2026-11-09-requirements-quality.md`
- live counts (all machine-read, `test-evidence/checklist-readings-2026-11-09.txt` §1): **44** items `CHK001`–`CHK044`, ids contiguous and unique, 0 duplicate id, 0 duplicate normalised body; **44/44** items carry a resolvable `[Req §…]` / `[Gap]` traceability anchor (methodology floor 80 %); **44/44** carry a quality-dimension bracket; **0** items open with `Verify / Test / Confirm / Check` + implementation behaviour.
- verdict distribution: **pass 37 / fail 3 (CHK002, CHK008, CHK009) / 观察 2 (CHK040, CHK041) / not_evaluated 1 (CHK043, SC-006) / blocked-by F-093-004 1 (CHK042)** = 44.
- gates, evidence retained in `test-evidence/checklist-gates-2026-11-09.txt`:
  - **G-checklist-reader (real file)**: `reader=pass`, 15 files, 0 findings, EXIT=0.
  - **G-checklist-reader (red-first probe 1)**: the `**Readers**:` line removed from a scratch copy under `.specify/.tmp/` → `reader=fail`, `reader-declaration-missing`, findings 1, EXIT=1 — **the gate does go red on its own subject**.
  - **G-checklist-duplicate (real file)**: `duplicate=pass`, 15 files, 0 findings, EXIT=0.
  - **workspace-guard**: `--snapshot` before any write (`test-evidence/workspace-checklist.json`), `--check` after the probes → `clean`, EXIT=0. Every write of this stage landed inside the 093 worktree; no write to the main worktree, no push.
- **Anomaly disclosed, not hidden — two of the three gate readings are weaker than their label:**
  1. **G-checklist-reader judges only the declaration.** Probes 2 and 2b broke the traceability anchors on three items (reduced to an unresolvable `Req ;`) and the face still returned `reader=pass`, 0 findings. The face has exactly two markers (`doc-consistency-check.py` `READER_MARKERS` :44-47); it never reads CHK items. So `reader=pass` means "the file declares its readers", **not** "the items are good". The property the gate was meant to establish (44/44 anchors, contiguous ids) is established by the machine check in readings §1, not by the gate.
  2. **G-checklist-duplicate is a blind check in this topology.** Probes 3 and 3b cloned CHK010 verbatim as CHK045 (and again with one extra full stop); both returned `duplicate=pass`, EXIT=0. Cause, measured not inferred: `is_excluded_path` (:279-290) rejects any path carrying a `.specify` component *before* the explicit `--path` is honoured, so `collect_records()` emits **0** records and the face compares an empty set with itself. The reading is kept verbatim and labelled; it is **not** reported as evidence of absence of duplicates. The 092 checklist recorded the same face as a green for the same reason.
  Consequently the duplicate property is established by the item-level machine check (44 distinct ids, 0 duplicate bodies under the engine's own normalisation rule :318-324), and a recurrence note is added below. Both defects are routed as framework observations (readings §4 O-1 / O-2 / O-3), not repaired in-stage: repairing them means editing a framework script outside this stage's territory.

## 2. Temporary Goal progress

> 注（2026-11-09，analyze-repair round 2 · V3-F6）：本节标题沿用已退役的「Temporary Goal」称谓；随框架分发的协议现名「Goal progress」（owner：`skills/external/sdd-loop-driver/references/checkpoint-protocol.md` § 2）。标题保留为 dated record，正文不改写。
| criterion | degree | evidence_ptr |
|---|---|---|
| 各执行体声明 default-concurrent 与具名串行例外 | **partial — requirement text is judgeable, implementations absent** | CHK006/CHK007/CHK010/CHK012 pass on FR-005…FR-007; CHK008 fail (FR-006's bijection contradicts its own `factual` members); CHK009 fail (the "6 reason codes" count has no owner in the requirements body) |
| 契约测试可判别 default-concurrent / serial-exception | **partial — acceptance judged, modules not yet written** | CHK035 pass (every SC carries a reading + mutation arm), CHK036 pass (`final` = SC-001…SC-006, aligned with `tasks.md` DoD-7 / GATE-4), CHK037 pass (closed disposition set) |
| 至少一个真实执行体完成 6 包 worktree 并发与确定性集成 | **not_evaluated** (unchanged, and named) | CHK043, by design; reasons: this stage's executor holds `Read, Grep, Glob, Bash, Write, Edit` — no dispatch tool; `tasks.md` § Environment Prerequisites and § SC-006 evidence plan carry the same probe; the mechanism is this feature's own deliverable |
| 派发能力在位，禁止声明并行而实际串行 | **partial — judged statically, runtime half open** | CHK020–CHK025 pass on the requirement side (declaration-imply-execution, no exemption, anti-nesting); the runtime verdict stays F-093-003, deliberately unadjudicated by T098 |
| 需求文本自身可放行到 analyze | **partial — 3 fails, 2 观察, 1 blocked row** | this file § 1; none of the three fails needs new intent to repair (see § 5 Q2) |

## 3. Team configuration review
- evidence: the checklist stage is a single-reader artefact — every item's verdict must be re-derivable by one reader along its `[Req §…]` anchor. There is no file-level write domain to split: one file, append-only recheck convention (`create-checklist` SKILL § Recheck), so partition into packages would put two executors on one file, which FR-012 forbids at directory level.
- symptom: the executing agent still has no dispatch tool, so this stage ran serially, exactly as plan and tasks did — fifth consecutive stage to do so.
- proposal: **none**. A roster change does not create a dispatch tool, and splitting one checklist file across executors would manufacture the exact write conflict this feature is about. The one measurable cost — five serial stages in a row — is already the subject of the feature itself, so proposing a workaround here would mask the gap it exists to close.
- ratification: n/a; applied: n/a.
- **disclosure**: the stage's own run is an instance of its subject ("declared 24, executed 1"). Recorded here and in the return, not presented as concurrency.

## 4. Next stage concurrency / roster
- requested: **24** (spine `agent_concurrency_requested`); effective: **1**; reason: `mechanism-not-yet-landed` ([[STR-010]]) — the dispatch mechanism is this feature's own delivery and has not landed.
- stage max_parallel: **1** for analyze. analyze is itself a fresh-context verification stage whose value is a second reading of the same artefacts; running it in parallel with itself would produce two verdicts about one artefact and no mechanism to reconcile them.
- roster: single analyze coordinator in the same worktree / branch (`093-clarify`, head `dbe172a4` at stage entry). First ruling owed to analyze: **F-093-004** (`[green:]` semantics), then F-093-003 (coordinator dispatch verdict).

## 5. Direction audit
- reload tier: **T0** (stage start — the brief's rules read before any write) + **T1** (after each artefact write: checklist draft, gate run, readings) + **T2** (at wrap-up, before this checkpoint).
- Q1 rules: unattended; no approval request; U4 → next; spine before action; workspace guard (all writes confined to the 093 worktree, verified `clean`); fast-fail; gate discipline; budget; report discipline — all in force. Objective-analysis rule 7 fallback declared once at the top of the checklist (single-context read-only; no dispatch tool).
- Q2 process: pass, with declared corrections. (a) A first-draft count claim ("pass 32") did not match the grepped distribution (37) — recomputed by grep and corrected, not re-estimated. (b) CHK009 carried an overstated observation ("five named members plus a trailing question") that the requirements text does not literally contain; replaced by the measured fact (one member named, the other five absent from the body) — the verdict `fail` is unchanged because it rests on the missing owner, not on the count of named members. (c) `validate-tasks.py` / `decomposition-check.py` were **not** re-run in this stage: they are outside its gate set and their tasks-stage readings stand in `test-evidence/validate-tasks.txt` and `decomposition-tasks.json` — the readings file says so explicitly rather than implying a rerun. Nothing else needed repair.
- Q3 next action: pass — analyze is the next stage in the declared `stage_plan`; its inputs are named (44 items with 3 fails, F-093-004 first, F-093-003 second, the two gate-scope defects above).
- Q4 spine freshness: pass — updated immediately after this checkpoint with the checklist verdict, the gate readings (including their scope limits), `wrapup_checklist` and `next_action: dispatch analyze with F-093-004 as the first ruling`; `stage_base_commit` = `dbe172a4`.
- Q5 territory / workspace: pass — no write outside the worktree; the main worktree untouched; no push; `workspace-guard --check` = `clean`.
- verdict: **on-track** — the stage delivered its assigned artefact, its item-level properties are machine-verified, the three fails are requirement-text defects with a single reading each (repair is an edit to `requirements.md` text in analyze, not an invention of intent), and the two weak gate readings are surfaced rather than converted into green evidence.

## 5b. Published-state check
- scope: n/a — no history correction.
- disposition: n/a — nothing to converge.
