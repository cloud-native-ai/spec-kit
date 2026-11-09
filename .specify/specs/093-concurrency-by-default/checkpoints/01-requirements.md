# Checkpoint 01 — requirements

## 1. Artifact verification
- sentinel: REQUIREMENTS-DONE
- U4: pass — `.specify/specs/093-concurrency-by-default/requirements.md` (36 FR / 12 SC; 8 final / 4 supporting; 7 shared strings; 8 clarifications; 6 assumptions; RS-001..RS-005); `validate-requirements.py` status ok 0/0; `pre-analyze-check.py --stage requirements` decision=pass 0/0; commit `a6b571f4` (clean-branch cherry-pick of the original `66e5b8e3`)
- artifacts: requirements.md, `checklists/requirements.md`, `test-evidence/{validate-requirements.txt,pre-analyze-check.txt}`, `goal/093-concurrency-by-default/goal.md`
- anomaly: three framework frictions recorded by the stage: (a) `validate-requirements.py` silently accepted a full-width-colon rewrite as **zero definition rows** while reporting `status: ok` (a green-not-red — exactly SC-001's subject); (b) both checkers are blind to blockquote (`>`) content; (c) the Runtime Stack `Contract` cell rejects a backticked path + `§` anchor combination. Additionally, the parallel dispatch of 092 tasks and 093 requirements in one working tree mixed the branches (092's commits landed on the 093 branch); the driver corrected it by cherry-picking 092 back to `master` and rebuilding the clean 093 branch, and the lesson is recorded for the 092/093 isolation design.

## 2. Temporary Goal progress

> 注（2026-11-09，analyze-repair round 2 · V3-F6）：本节标题沿用已退役的「Temporary Goal」称谓；随框架分发的协议现名「Goal progress」（owner：`skills/external/sdd-loop-driver/references/checkpoint-protocol.md` § 2）。标题保留为 dated record，正文不改写。
| criterion | degree | evidence_ptr |
|---|---|---|
| 各执行体声明 default-concurrent 与具名串行例外 | not_evaluated | requirements FR groups A/E; implementation pending |
| 契约测试可判别 default-concurrent / serial-exception | not_evaluated | requirements FR groups B/F |
| 至少一个真实执行体完成 6 包 worktree 并发与确定性集成 | not_evaluated | 092 implement will be the first proof |
| 派发能力在位，禁止声明并行而实际串行 | not_evaluated | requirements group D |

## 3. Team configuration review
- evidence: none (temporary team is created after plan U4 per 085)
- symptom: the parallel lines shared one working tree and mixed branches
- proposal: per-line worktree isolation (064/084); the driver's multi-line must use worktree-per-write-line
- ratification: standing
- applied: the 093 clarify will run in its own worktree

## 4. Next stage concurrency / roster
- requested: 24; effective: 1; reason: clarify is a single read/write package in the 093 worktree
- stage max_parallel: 1; verifier reserve: 1
- roster: single clarify worker

## 5. Direction audit
- reload tier: T0+T1
- Q1 rules: unattended; no approval request; U4 -> next stage; spine written before acting; workspace-guard; fast-fail; gate discipline; budget; report discipline — all in force
- Q2 process: pass with corrections — the requirements pass; the branch mix and the green-not-red friction are surfaced and corrected/recorded
- Q3 next action: pass — clarify is the next stage, now in an isolated worktree
- Q4 spine freshness: pass — spine updated after U4 (stage=clarify)
- Q5 territory/workspace: correction-applied — 092's commits moved to master; the clean 093 branch rebuilt; the isolation lesson recorded
- verdict: correction-applied
