---
id: "20261030T060843Z-speckit-checklist"
unit_id: "/speckit.checklist"
unit_type: "command"
run_id: "r20261030T054502Z-078a"
scope: "local"
probe: "speckit-checklist-wrapup"
kind: "internal"
slice: "commands"
feature: "078-coaching-skills"
feature_id: "078"
partial: false
created: "2026-10-30T06:08:43Z"
summary: "checklist 阶段新增 36 项需求质量清单 checklists/coaching-loop-2026-10-30.md（CHK001–CHK036，七组：运行输入与解析、执行预期、运行状态与报告、派发/观测/失败、重命名身份与封闭面、依赖与非功能），全部为题问句、36/36 带 Req 锚点（100%），Verify/Test/Confirm/Check 开头 0 条，编号连续无重复，软"
---

## Review
checklist 阶段新增 36 项需求质量清单 checklists/coaching-loop-2026-10-30.md（CHK001–CHK036，七组：运行输入与解析、执行预期、运行状态与报告、派发/观测/失败、重命名身份与封闭面、依赖与非功能），全部为题问句、36/36 带 Req 锚点（100%），Verify/Test/Confirm/Check 开头 0 条，编号连续无重复，软上限 40 未触；确定性自检输出存 test-evidence/checklist-self-check.txt，本阶段 docs-only 预算记 test-evidence/checklist-stage-status.txt（status=not-run-docs-only）。未覆盖 checklists/requirements.md，未改 requirements.md / plan 属主制品（PLAN-EDIT: 0）。清单暴露三条高价值跨制品冲突：US1-AS3/FR-017 与 contracts C-10 对 success/partial 判定不一致（CHK013）、FR-018 的八个身份坐标与 SC-006 的五个计数坐标不对齐（CHK026）、FR-024 字面冻结 .specify/specs/** 会连本特性自身产物一并冻结（CHK028）。方法局限如实记录：技能要求 fresh-context 子代理做工差扫描，本线驱动约束禁止派发子代理，故为单上下文扫描，已写入清单 Notes 交 /speckit.analyze 复核。

## Optimization Points
- 1) create-checklist 的 same-author 检测要求派发 fresh-context 子代理，而无人值守驱动可能禁止子代理；技能可声明一条受认可的单上下文降级路径并要求显式记录局限，而不是让两个约束在运行时相互冲突。2) 清单最高价值的条目来自「状态值域 / 坐标枚举 / 路径边界」这类跨制品对账，建议技能在加载 plan 与 contracts 后固定跑一遍封闭值域与枚举对账，把这类冲突从偶然发现变为必跑步骤。3) 条目数、编号连续性、≥80% 可追溯目前靠人眼或临时内联脚本判定；技能可内置一个小型确定性检查器，让这三条判据可复现。\n
