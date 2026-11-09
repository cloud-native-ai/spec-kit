# Checkpoint 03 — plan

> **Correction (2026-11-09, analyze-repair · F-093-012)**: the claim in §3 that "the executing agent has no dispatch tool" is false — the executing body holds a host dispatch tool (measured by the analyze stage itself), and a tool set is a per-run probe, not a constant. The body of this dated checkpoint is left as written; the corrected premise lives in `plan.md` § Concurrency plan and the ledger `notes/analyze-repair.md` § F-093-012.

## 1. Artifact verification
- sentinel target: `plan.md` + the Phase 1 set (`research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `feature-ref.md`)
- live counts, taken from each file: `plan.md` 385 lines and exactly **one** `# Implementation Plan:` heading (no residual placeholder); `research.md` **14** sections (R-1…R-14); `data-model.md` **11** entities / **26** validation rules / **5** state machines; `contracts/` **6** files carrying **92** clauses (C-001…C-092, counted by `grep -c '^- \*\*C-[0-9][0-9][0-9]\*\*'` over the five clause-bearing files); `quickstart.md` **7** scenarios (S-0…S-6); `feature-ref.md` **33** FR map rows + **12** SC map rows, verified against the requirement ids by a set differ (no gap, no alias)
- gates, all evidence retained under `test-evidence/`:
  - `pre-analyze-check.py --stage plan` → **decision=pass**, 0 error / 44 advisory (`pre-analyze-plan.json`). Every advisory is a `missing-path` on a path this feature *creates* (the eight facts, the ten test modules, `.specify/templates/commands/`, 092's `verification.md`), plus two dated citations in `research.md`. None is a silent break.
  - `validate-decision-tensions.py` → **status ok**, 0 errors, 5 records (`decision-tensions-plan.json`). Two `expected-sacrifice-unmapped` findings were raised and fixed in-stage (T-002 and T-004 each re-named an SC id in prose, so one source read as two).
  - `decomposition-check.py --mode plan` → **proceed**, 33 FR, no reason (`decomposition-plan.json`).
  - `overlap-check.py` → **reading=overlap**, 84 specs / 195 hits / 113 nested-path (`overlap-plan.json`). The verdict is **not** taken from this reading: F-093-002 is live in this worktree (the engine's declared-surface extraction is coarser than the delivery surface and pairs directories against files inside them). The adjudication is file-level, in `feature-ref.md` § Overlap adjudication.
- anomaly disclosed above rather than hidden: the overlap engine's green-or-red is not usable as-is here; the recorded reading plus the by-hand file-level table is the evidence, and F-093-002 stays open as a framework finding.

## 2. Temporary Goal progress

> 注（2026-11-09，analyze-repair round 2 · V3-F6）：本节标题沿用已退役的「Temporary Goal」称谓；随框架分发的协议现名「Goal progress」（owner：`skills/external/sdd-loop-driver/references/checkpoint-protocol.md` § 2）。标题保留为 dated record，正文不改写。
| criterion | degree | evidence_ptr |
|---|---|---|
| 各执行体声明 default-concurrent 与具名串行例外 | partial (design complete) | `contracts/executor-obligations.contract.md` C-041…C-062 (three-part obligation, class text, closed reason set); `contracts/declaration-facts.contract.md` C-004/C-005; implementation pending |
| 契约测试可判别 default-concurrent / serial-exception | partial (allocation complete) | executor-obligations C-060 + `feature-ref.md` § Measurement map: 12 SC → 10 modules, each named; the modules land red-first at implement |
| 至少一个真实执行体完成 6 包 worktree 并发与确定性集成 | not_evaluated (unchanged) | `plan.md` § Concurrency plan for this run: this stage ran serial, one agent, `mechanism-not-yet-landed`; SC-006 recorded as `not_evaluated`, not as zero and not as an estimate |
| 派发能力在 agent/阶段席位/执行体中在位，禁止声明并行而实际串行 | partial (design complete) | judgement-engine C-037…C-040 (existing `capability-tools` is judged, no new key), `test_concurrency_reproduction_092.py` as the red-first reproduction, T-004 registering the coordinator verdict without self-adjudicating it |

## 3. Team configuration review
- evidence: five work packages were designed and ready (`P1` facts, `P2` engine, `P3` owners/agents, `P4` contracts/tests, `P5` evidence/adjudication), with `P1 → P2` and `P1/P2 → P4` as the only edges — a genuinely parallel partition
- symptom: **the executing agent has no dispatch tool** (`Read, Grep, Glob, Bash, Write, Edit`; no Agent/Task tool), so the partition ran serially in one context. This is exactly the 092 shape this feature exists to make red.
- proposal: none this stage — changing the roster does not change the toolset; the fix is the mechanism, and the mechanism is this feature's own delivery.
- ratification: n/a
- applied: n/a
- **disclosure (092 lesson)**: "partition ready but execution was serial" is stated here, in `plan.md` § Concurrency plan for this run, and in the return; it is never presented as concurrency.

## 4. Next stage concurrency / roster
- requested: 24 (spine `agent_concurrency_requested`); effective: **1**; reason: `mechanism-not-yet-landed` ([[STR-010]]) — no dispatch capability in the executor's toolset
- stage max_parallel: 1; verifier reserve: 1 (the independent verifier has not run for this stage)
- roster: single plan coordinator; next stage = **tasks** in the same worktree/branch, which produces the WP set the implement stage can then dispatch

## 5. Direction audit
- reload tier: T0+T1+T2 (stage start, after each artifact landed, and at wrap-up)
- Q1 rules: unattended; no approval request; U4 → next stage; spine before action; workspace guard (wrote only inside the worktree, plus `.specify/memory/features*.md`, `.specify/state/`, and the spec directory); fast-fail; gate discipline; budget; report discipline — all in force
- Q2 process: pass with corrections — corrections applied in-passing and disclosed: (a) the fact count was reconciled six→**eight** across `plan.md` (Summary, Technical Context, Storage, Constitution IX row, Scale/Scope, the T-005 判据 line) and `declaration-facts.contract.md` C-001/C-003; (b) two `expected_sacrifice` rows bound two SC ids and were rewritten to one; (c) two Fact Owners anchors pointed at headings that do not exist (`## Goal 与 Target`, `## Territory`) and were re-pointed to the real anchors; (d) one typo (`effectice-concurrency`); (e) a `--record` flag declared in judgement-engine C-021 so the quickstart commands are interface-conformant; (f) `feature-ref.md` ownership rows corrected where the overlap reading had attributed `sync-mirrors.py`/`instructions-template.md` to the wrong feature
- Q3 next action: pass — tasks is the next stage; the WP set, the ten red-first modules and the T-004 blocking item are its inputs
- Q4 spine freshness: pass — spine carries `stage: plan`, the new verdict, the four gate readings, the resolved/pending finding states and `next_action: … dispatch tasks`
- Q5 territory/workspace: pass — no write outside the worktree; the main worktree's 092 line untouched; no push
- verdict: correction-applied (the six→eight reconciliation was a real contradiction inside the artifact, not a wording preference; the alternative readings would each have changed a deliverable)

## 6. Disclosed rulings (in-stage, recorded where they bind)
1. T-001 — the slot cap value moves to a fact; the ceiling stays owned by `wp-gate.py`; the three prose sites become projections. Alternative kept in the record: keep all four and call the tightest one the owner (rejected: "unique definition point" is not reached by adding a fifth).
2. T-002 — `effective` = maximum interval overlap; auxiliary aggregates refused. Alternative: interval-width sum ÷ total duration (rejected: it counts idle units as concurrency).
3. T-003 — write domains are file-level path sets. Alternative: directory-level regions + scheduler prefix check (rejected on the measured `skills/internal` case).
4. T-004 — the coordinator verdict is registered but **not** decided here. Alternative: declare "coordinator may dispatch" and add the tool to 13 agents (refused: it would invent intent no artifact records — F-093-003).
5. T-005 — the judgement surfaces ride the existing declaration layer; no concurrency-specific registry. Alternative: a standalone `concurrency.yaml` (rejected: second source of truth, Constitution XIV).

## 7. Residual risk
- **R-1 (highest)**: `concurrency-check.py` does not exist yet, so every quickstart command except S-0 is unrunnable today; S-1…S-6 are pinned by clause ids, not by execution. Mitigation: the allocation names one module per SC, and implement lands them red-first.
- **R-2**: the coordinator verdict (T-004) blocks the static half of SC-005; until an owner rules, `capability` correctly reports `owner-unavailable` (exit 2) and the static assertion cannot close.
- **R-3**: F-093-002 means a later stage cannot use `overlap-check.py` from inside a worktree as a verdict; the file-level adjudication must be refreshed by reading if the surface moves.
- **R-4**: SC-006's real-run evidence cannot be produced by this stage and must come from a run whose executor actually dispatches; until then the honest value is `not_evaluated`.
