---
id: "20260820T135721Z-speckit-sanitize"
unit_id: "/speckit.sanitize"
unit_type: "command"
run_id: "gate:gate-sanitize-destructive-cleanup:20260820T135721Z"
scope: "local"
probe: "gate-sanitize-destructive-cleanup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-08-20T13:57:21Z"
summary: "confirm-gate 观察事实:gate-sanitize-destructive-cleanup 于 2026-08-20 运行中触发一次,单次批量呈现 2 项 destructive(delete)清理计划,用户批准全部两项;确认前计划文件 confirmed:false、引擎零执行,确认后 agent 清空非空目录内容、引擎完成删除并将两条发现置 resolved,失败项为零。"
---

## Review
confirm-gate 观察事实:gate-sanitize-destructive-cleanup 于 2026-08-20 运行中触发一次,单次批量呈现 2 项 destructive(delete)清理计划,用户批准全部两项;确认前计划文件 confirmed:false、引擎零执行,确认后 agent 清空非空目录内容、引擎完成删除并将两条发现置 resolved,失败项为零。

## Optimization Points
- 破坏性清理门控单次批量触发:2 项 delete 归并一份 cleanup-plan.json(confirmed:false),引擎对未确认 apply 退出码 2 零执行
- 用户经结构化批量确认一次放行两项;放行前零删除零移动,符合确认红线
- 执行机制透明披露:.migration-backups 非空目录需 agent 先清空 58 个桩再由引擎删空目录,用户在知情下批准
