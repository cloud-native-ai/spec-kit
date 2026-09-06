---
id: "20260905T095250Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "feedback-package-20260905T095124Z"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-09-05T09:52:50Z"
summary: "完成 Mode 2 package 闭环:状态 10/10,待打包 10 条均为 internal 且无 introspection_ref;生成 20,083-byte zip,MANIFEST 存在且含 10 条 Markdown 记录;cleanup dry-run 精确列出 10 条,实际 cleanup 全部移除,活动 store 归零。未执行网络发送或 mark-submitted,z"
---

## Review
完成 Mode 2 package 闭环:状态 10/10,待打包 10 条均为 internal 且无 introspection_ref;生成 20,083-byte zip,MANIFEST 存在且含 10 条 Markdown 记录;cleanup dry-run 精确列出 10 条,实际 cleanup 全部移除,活动 store 归零。未执行网络发送或 mark-submitted,zip 保留在 outbox。识别 3 个命令/引擎优化点。

## Optimization Points
- Mode 2 的 `list --format json` 顶层 schema 是 `{count,matches}`,但命令说明只描述“Summary view”而未声明结构；本轮调用方按常见 entries/items 投影误判为零条目。建议在命令契约中固定并示例 JSON schema，或给引擎增加一致的 `entries` 键
- token-efficiency: package 流程可用单个 engine action 返回 status + entries summary + introspection refs，避免 status/list 两次调用与一次因 schema 误判产生的额外 Read；程序侧汇总比 agent 猜 JSON 结构更可靠
- package 后 cleanup 会删除已被 git 跟踪的反馈条目，导致工作树出现 10 个 D；这是预期生命周期但用户容易误以为数据丢失。建议 cleanup JSON 增加 `tracked_files_removed` 与推荐的后续 git 处置说明
