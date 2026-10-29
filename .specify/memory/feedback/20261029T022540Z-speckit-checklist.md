---
id: "20261029T022540Z-speckit-checklist"
unit_id: "/speckit.checklist"
unit_type: "command"
run_id: "r20261028T132000Z-074d-checklist"
scope: "local"
probe: "speckit-checklist-wrapup"
kind: "internal"
slice: "commands"
feature: "074a-authorized-routing"
feature_id: "074"
partial: false
created: "2026-10-29T02:25:40Z"
summary: "074a checklist 阶段按切片生成新检查单，14 条需求缺口如实记录并交回回环"
---

## Review
074a checklist 阶段按切片生成新检查单，14 条需求缺口如实记录并交回回环

## Optimization Points
- Task: 派发简报要求"检查单聚焦需求质量"但同时期望 pass/fail 判定与缺口清单——两者只有把条目在本趟判完（[x]/fail 行）才同时满足，否则回传无判定可报 | Task: 同作者检测条款要求 gap-finding 派发 fresh-context 子代理，而简报固定 decomposition=single-package 不派子代理；按 gate 的"产物非本会话作者"分支不合规触发条件，但仍需在检查单与证据文件里显式披露证据强度 | Agent: check-prerequisites.sh 再次解析到父 spec 目录（分支=父特性名），切片作用域只能靠简报显式覆盖——同一缺陷在 requirements/clarify/plan/tasks/checklist 五个阶段重复出现，说明"分支名=父特性名"的切片拓扑缺一条脚本级支持 | Env: exec-quant 不接受 --feature/--feature-id，与 run-determination、feedback-utils 的参数面不一致（上一阶段已记录，本阶段复现）
