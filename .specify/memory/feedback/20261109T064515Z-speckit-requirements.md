---
id: "20261109T064515Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "r20261109T064500Z-092a"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "092"
partial: false
created: "2026-11-09T06:45:15Z"
summary: "neutral"
---

## Review
neutral

## Optimization Points
- 1) validate-requirements.py 与 pre-analyze-check.py 都无 --version 之外的阶段绑定，requirements 产物需同时满足两套判据（id 连续 / Path 标记 / 引用可解 / 运行时表），三处规则来自不同 owner 且无一处汇总清单——写规格时要并行照看，容易只修一侧。2) pre-analyze-check.py 的 --collected 是整数计数、--names-current/--names-baseline/--red-first-refs 是文件路径，而 --declared-check/--green-check 是重复型字符串且要求精确相等匹配：参数形态在 --help 中没有分区说明，run-determination 连续四次以不同理由拒绝，只能靠读源码试错。3) 收尾三步（Run Determination / Exec Quant / Feedback Record）的必需与可选参数集不在同一处：args-manifest 动作已经能自述，但调用方仍要自己拼装。
