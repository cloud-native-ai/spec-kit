---
id: "20261030T061908Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261030T054502Z-078a"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "078-coaching-skills"
feature_id: "078"
partial: false
created: "2026-10-30T06:19:08Z"
summary: "078-coaching-skills analyze（只读）：跨 requirements/plan/tasks/contracts/data-model/quickstart/checklists/feature 注册表对账。1 CRITICAL + 3 HIGH（经 5 个 fresh-context 只读验证器：4 confirm / 1 downgrade / 0 reject）；三条约"
---

## Review
078-coaching-skills analyze（只读）：跨 requirements/plan/tasks/contracts/data-model/quickstart/checklists/feature 注册表对账。1 CRITICAL + 3 HIGH（经 5 个 fresh-context 只读验证器：4 confirm / 1 downgrade / 0 reject）；三条约定的风险裁决为 CHK013=HIGH、CHK026=MEDIUM、CHK028=MEDIUM（验证器从 HIGH 下调，接受其证据边界）。C-01 为宪法 XIV 冲突（封闭活接线面在 A10 之外被四处复述且已漂移），按规则保持 CRITICAL。H-02 为 SC-008 用总量相等与 FR-027 明令否决的计量单位对撞、且没有任何任务执行新增行判定；H-03 为 SC-006 的封闭面审计漏掉 C-3 的 11 个派生文件。确定性读数：validate-tasks PASS、decision-tensions 0 findings、account-clause-coverage claimed 38 但 FR 车道 0/29 status=uncovered、flow-class 79/79、probe 75 units、mirrors/copies 0 漂移、gates blocking=27。10 条未勾 [Gap] 清单项全部处置（7 covered-by / 3 raised）。结论：需回环上游修复，不得进入 implement。本阶段仅写 test-evidence/analyze-stage-status.txt 与记账；未改任何制品、未提交。

## Optimization Points
- 1) [token-efficiency] 验证波首次派发被后台 shell 退出吞掉（输出为空），白跑一次外部 CLI；技能应要求在把验证器结果计为 verdict 前检查输出非空，空输出计为 incomplete 而非 confirm。2) 固定增加一道「验收面 vs 其 owner 枚举」的成员/单位对账：本轮 4/4 条验证通过的 C/H 中有 3 条是同源枚举在 SC/DoD 与契约/任务间成员或计量单位不一致（C-10 上限、SC-008 总量单位、SC-006 封闭面路径）。3) checklist 问责可交确定性计数（未勾 [Gap] 数 = raised + covered-by），避免手抄 10 条处置标记。4) [token-efficiency] FR 车道 0/29 与条款车道 38/38 的差异应在加载阶段由引擎先打印成一行 verdict，减少为理解同一覆盖率报告反复读取两份摘要。
