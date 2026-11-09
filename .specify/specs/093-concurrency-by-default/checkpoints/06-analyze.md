# Checkpoint 06 — analyze

## 1. Artifact verification
- sentinel target: `notes/analyze-findings.md` (findings report; the analyze stage writes no artifact outside its own notes/ and test-evidence territory).
- live counts (machine-read, `test-evidence/analyze-gates-2026-11-09.txt`): **15 findings** — CRITICAL 1 (`F-093-009`) / HIGH 3 (`F-093-005`, `F-093-006`, `F-093-007`) / MEDIUM 8 (`F-093-008`, `F-093-010`…`F-093-015`, `F-093-018`) / LOW 2 (`F-093-016`, `F-093-017`); `F-093-011` (SC-006 `not_evaluated`) is carried as accepted, not as a defect.
- gates, every command line + complete stdout/stderr + exit status + wall time in `test-evidence/analyze-gates-2026-11-09.txt`:
  - G1 `validate-requirements.py` → `status: ok`, **0 error / 0 warning**, EXIT 0.
  - G2 `account-clause-coverage.py <spec-dir> --corpus-root <worktree>/.specify/specs` → `status: baseline-missing`, EXIT 2; **FR lane 25 / 33** with `UNCOVERED-FR` = FR-011, FR-013, FR-016, FR-017, FR-025, FR-027, FR-028, FR-033; clause lane 35 claimed / 655 uncovered beyond an absent baseline; 108 named-unparseable (0 positive-form). **No `--freeze` was run**, by instruction and by reason: freezing narrows the corpus to everything *but* this spec, so it cannot answer the FR lane and would have converted a red lane into baseline-internal noise.
  - G3 `validate-tasks.py` → **PASS 0 error / 0 warning**, EXIT 0.
  - G4 `validate-decision-tensions.py --spec <spec-dir>` → EXIT 0, 5 records T-001…T-005.
  - G5 `pre-analyze-check.py` requirements 0/0, plan 0/0, tasks 0/101 advisory (every advisory is a creation-target path) — all EXIT 0.
  - G6 `decomposition-check.py --mode tasks` → `proceed`, 33 FR / 137 tasks, ceilings 120 / 160.
- **Anomaly disclosed, not hidden**: two gate readings are red and neither was repaired in-stage — the FR lane (F-093-005, structural: the delivery map's clauses carry no resolvable citation group) and, upstream of it, a CRITICAL requirement-text corruption the validator cannot see because it sits inside a backtick pair (F-093-009). Both are requirement/contract-layer defects with one recorded reading each and are routed to `analyze-repair` with a table, not to the user.

## 2. Temporary Goal progress

> 注（2026-11-09，analyze-repair round 2 · V3-F6）：本节标题沿用已退役的「Temporary Goal」称谓；随框架分发的协议现名「Goal progress」（owner：`skills/external/sdd-loop-driver/references/checkpoint-protocol.md` § 2）。标题保留为 dated record，正文不改写。
| criterion | degree | evidence_ptr |
|---|---|---|
| 各执行体声明 default-concurrent 与具名串行例外 | partial — requirement text judgeable, implementations absent; the one text defect blocking it (FR-006 bijection vs STR-009/STR-010) is F-093-007 | findings § 4 HIGH F-093-007; checklist CHK008 |
| 契约测试可判别 default-concurrent / serial-exception | partial — 12/12 SC mapped to red-first modules, none written | findings § 7 |
| 至少一个真实执行体完成 6 包 worktree 并发与确定性集成 | **not_evaluated** (unchanged, named) | F-093-011; `requirements.md` A4; SC-006 Source |
| 派发能力在位，禁止声明并行而实际串行 | partial — static half delivered by US4 rows; the coordinator verdict is an owner decision, and the recorded host premise was found false (F-093-012) | findings § 3; F-093-003 adjudication |
| 需求文本自身可放行到 implement | **否** — CRITICAL 1 / HIGH 3 | findings § 6 repair brief |

## 3. Team configuration review
- evidence: analyze is a single fresh-context reading of five artifacts; its value is *independent re-derivation*, and a parallel split of one report across executors would produce N verdicts about one artefact with no reconciliation mechanism (checkpoint 05 § 4 reasoned the same and set `max_parallel: 1`).
- symptom: the stage ran serially — one executor — for the fifth consecutive stage. The recorded reason (`mechanism-not-yet-landed`) is the feature's own subject.
- disclosure, measured this run: the executing body **does** hold a dispatch tool (this stage was itself dispatched, and its own tool set includes the subagent-dispatch tool the five earlier stage records say the executor lacks). That contradiction is recorded as F-093-012 rather than used to claim concurrency: dispatching analyze's sub-readers would not have changed the verdict, and SC-006 needs the feature's own mechanism, not a host accident.
- proposal: none — the roster is not the gap.
- ratification: n/a; applied: n/a.

## 4. Next stage concurrency / roster
- requested: 24 (spine `agent_concurrency_requested`); effective: 1; reason: `mechanism-not-yet-landed` ([[STR-010]]) for the mechanism this feature delivers.
- stage max_parallel: 1 for `analyze-repair` — it edits overlapping files (`requirements.md`, `contracts/*.md`, `tasks.md`) and those are integrator-owned single files; a parallel split would put two executors on one file, which FR-012 forbids.
- roster: single repair coordinator in the same worktree/branch (`093-clarify`, head `1770b19a` at stage end). `analyze-repair` re-runs G1 / G2 / G3 and the three `pre-analyze-check` stages, then hands back to the driver.

## 5. Direction audit
- reload tier: T0 (stage start — brief rules read before any write) + T1 (after the gate run, after the findings write, after the spine write) + T2 (at wrap-up, before this checkpoint).
- Q1 rules: unattended; no approval request; U4 → next; spine before action; workspace guard (every write confined to the 093 worktree, verified by `git status` before the commit); fast-fail; gate discipline; budget; report discipline — all in force.
- Q2 process: pass with declared corrections. (a) The evidence file was rewritten once after a shell-redirect mistake truncated its tail — the rewrite re-ran every gate and captured exit codes and wall times the first pass had not; the second pass is the record. (b) The first two `run-determination` attempts (a1 with no declared check, a2 with an unreadable name baseline) were superseded by a3, which is what the spine names — the failures are disclosed in the spine's `wrapup_analyze` line rather than deleted. (c) Two candidate severity assignments were lowered after measuring: the MEDIUM count rose from 7 to 8 when F-093-018 was added mid-pass, and the spine verdict was corrected to match the report rather than left at the first draft's count. (d) One adopted repair was rejected mid-pass: freezing `coverage-baseline.txt` would have made G2 green, and it was refused because it answers a different question; the refusal is written into the evidence file and the findings.
- Q3 next action: pass — `analyze-repair` is the next stage implied by a NOT-READY verdict, and its inputs (5-row repair table, 15 findings with severities) are named in the report.
- Q4 spine freshness: pass — written before the artifact commit, then updated with the wrap-up chain and `next_action: dispatch analyze-repair`; `last_verdict` carries the verdict, the F-093-004 ruling and the F-093-003 adjudication.
- Q5 territory/workspace: pass — no write outside the worktree; no push; no framework source edited (the `[green:]` repair is recorded as an implement row, T138, not applied).
- verdict: **decision-needed** — two items do not have a single recorded reading and were neither repaired nor silently absorbed: the F-093-004 semantics (ruled *with an owner*, by the project's own glossary), and the F-093-003 verdict value (surfaced, because no tool of this stage can measure the host fact it turns on). Everything else with a single reading is in the repair brief.

## 5b. Published-state check
- scope: n/a — no history correction.
- disposition: n/a — nothing to converge.

## 6. Disclosed rulings (in-stage, recorded where they bind)
1. **F-093-004 — the `[green:]` tag is a red-first marker; its owner is `templates/tasks-template.md` L110.** Chosen because `glossary.md` 绿点归属 names that file as the 真源 and Constitution XIV puts an authored definition above a consumer's rule text. The partition invariant survives, scoped to claimed clauses. `validate-tasks.py` is behaviourally consistent and only its description drifts → implement row T138.
2. **F-093-003 — implement-stage work, already carried; the value is an owner decision.** The deliverable (fact + reader + routing + pass-down) is T096/T098/T101/T105 and contract C-072 makes the verdict-absent window fail-closed, so it does not block implement. Choosing `allow` or `forbid` needs a host fact no artifact records — surfaced.
3. **SC-006 stays `not_evaluated`.** Same reason as checkpoints 03/04/05, restated with the F-093-012 disclosure beside it so the next reader does not mistake the host's tool set for the feature's mechanism.
4. **The checklists' three FAIL items are requirement-text defects, not implementation gaps** — CHK002 superseded by F-093-006, CHK008 by F-093-007, CHK009 by F-093-008; none needs new intent to repair.

## 7. Residual risk
- **R-1**: F-093-009's repair is a text substitution in the owner row of a delivery-discipline FR; done carelessly it can turn one definition row into two (the validator's `id-contiguous` / `doc-order` rules would go red). The brief says "re-express, do not append".
- **R-2**: F-093-005's repair edits clause citation groups in `contracts/`, which `feature-ref.md` and `tasks.md` both cite; a re-pointed clause must be re-checked against the delivery map in the same pass or the map drifts again.
- **R-3**: `analyze-repair` adds T138 to a 137-row file that currently validates 0/0; the new row must carry a `blockedBy`/phase placement that keeps `decomposition-check` at `proceed`.
- **R-4**: the coordinator verdict (F-093-003) still blocks the static half of SC-005 at implement time — but only the *value*, not the work.
- **R-5**: the two blind gate faces (duplicate / reader) remain blind; any later stage citing `duplicate=pass` as evidence has read a claim the face never made.
