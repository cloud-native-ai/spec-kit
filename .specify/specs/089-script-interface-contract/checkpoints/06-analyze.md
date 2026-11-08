# Checkpoint 06 — analyze

## 1. Artifact verification

- sentinel: `ANALYZE-DONE` / `ANALYZE2-DONE` / `ANALYZE3-DONE`（三轮）
- U4: pass — round 3 **GATE GREEN**：CRITICAL 0 / HIGH 0 / MEDIUM 8 / LOW 10；上一轮 4 条 HIGH 全部关闭
- 独立复跑：`account-clause-coverage.py` ok（31/31 FR cited，claimed clauses 38，0 beyond baseline）；`validate-tasks.py` 0 error / 62 warning；`pre-analyze-check --stage tasks` pass（0 error）；`decomposition-check --mode tasks` proceed（31/87，ceiling 120/160）
- artifacts: 全部 spec 产物 + `coverage-baseline.txt`；提交链 `5c2bb98f` → `8e410a88` → `754f3d3b` → 本轮 MEDIUM 收口提交
- anomaly: 修复期由驱动者披露并更正的项：requirements 事实更正、data-model 条款重映射、SC-012 取证改注入式、sandbox exit code、版本解析有界上溯、墓碑引用诚实化、FR 映射重写、计数漂移

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| 适用脚本的 -h/--help/--version 全部成功退出、输出非空，执行前后工作树零差异 | not_evaluated | analyze 三轮均未实现代码；implement 阶段取证 |
| 契约检查对全部候选给出判定，违规计数为 0，豁免成员逐条带机械判据证据 | not_evaluated | 契约 C-1…C-22 已定稿；实现待做 |
| 干净下游项目经初始化后，宪法含该原则、instructions.md 含对应常驻段落 | not_evaluated | 契约 C-23…C-32 已定稿；实现待做 |

## 3. Team configuration review

- evidence: 三轮 analyze 的实际并发均为 1；无 run report
- symptom: none
- proposal: none
- ratification: standing
- applied: no

## 4. Next stage concurrency / roster

- requested: 24; effective: 6; reason: implement 包按 plan S0–S8 切分，写包独占、只读包可并行
- stage max_parallel: 6; verifier reserve: 2
- roster: SDD Implement Coordinator ×1 + SDD Implement Executor ×N（按 ≤16 任务/段派发）+ verifier/integrator reserve
