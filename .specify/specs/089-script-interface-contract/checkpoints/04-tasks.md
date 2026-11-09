# Checkpoint 04 — tasks

## 1. Artifact verification

- sentinel: `TASKS-DONE`
- U4: pass — 驱动者独立复跑：`pre-analyze-check --stage tasks` pass（0 errors / 60 advisories 均计划路径或格式说明）、`validate-tasks.py` PASS（0 error / 61 warnings，均在 tasks.md § Notes 裁定）、`decomposition-check --mode tasks` proceed（31 FR / 87 tasks / ceilings 120·160）
- artifacts: `tasks.md`（87 行 T001…T087）、`test-evidence/tasks-{validate,decomposition,stage-status}`
- commits: `56dc6dfd`（tasks 产物）、`b6bb7356`（规模门上限 120/160）、本 checkpoint 提交内的 T025/T032/T063 FR 行级引用修复
- anomaly: `ANOMALY: 首次 tasks 门判 split-required（87>80），经用户裁定提高上限后 proceed`；`ANOMALY: 3 条 runtime-stack-row error 因任务行未引用 FR，驱动者补行级引用`

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| 适用脚本的 -h/--help/--version 全部成功退出、输出非空，执行前后工作树零差异 | not_evaluated | `tasks.md` T055–T066；implement 阶段取证 |
| 契约检查对全部候选给出判定，违规计数为 0，豁免成员逐条带机械判据证据 | not_evaluated | `tasks.md` T030–T054 |
| 干净下游项目经初始化后，宪法含该原则、instructions.md 含对应常驻段落 | not_evaluated | `tasks.md` T027 |

## 3. Team configuration review

- evidence: 无独立 run 报告（首轮运行）；tasks 阶段实际并发 1
- symptom: none
- proposal: none
- ratification: standing
- applied: no

## 4. Next stage concurrency / roster

- requested: 24; effective: 1; reason: checklist 为单产物阶段
- stage max_parallel: 2; verifier reserve: 2
- roster: SDD Checklist Worker ×1
