---
id: "20261110T082855Z-skill-create-requirements"
unit_id: "skill:create-requirements"
unit_type: "skill"
run_id: "r20261110T081104Z-b097"
scope: "local"
probe: "skill-create-requirements-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-10T08:28:55Z"
summary: "create-requirements 执行：脚手架 097-speckit-migrate-command；house 约定对齐 094；验证器首跑 status=ok（0 error / 0 warning）；流程检查清单已盖章。"
---

## Review
create-requirements 执行：脚手架 097-speckit-migrate-command；house 约定对齐 094；验证器首跑 status=ok（0 error / 0 warning）；流程检查清单已盖章。

## Optimization Points
- 1) 寄存需求原文在主仓 .specify/memory/todo（worktree 基线未含），按主仓读取；2) flow-class lookup 于声明写入后返回 source=declaration。
