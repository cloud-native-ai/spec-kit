---
id: "20260818T021842Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "feedback-cleanup-loop-template-20260818T021842Z"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-08-18T02:18:42Z"
summary: "用户直提改进落地:feedback 命令模板补两条默认清理闭环(Mode 2 package 后 dry-run→cleanup 删包内条目、mark-submitted 后删 zip;Mode 4 consume 末尾强制删批次 zip+consume-log 记录),行为规则与用户文档同步,4 副本再生;并按新策略补执行本会话遗留两处清理(intake 清空、store 13 条归零)。"
---

## Review
用户直提改进落地:feedback 命令模板补两条默认清理闭环(Mode 2 package 后 dry-run→cleanup 删包内条目、mark-submitted 后删 zip;Mode 4 consume 末尾强制删批次 zip+consume-log 记录),行为规则与用户文档同步,4 副本再生;并按新策略补执行本会话遗留两处清理(intake 清空、store 13 条归零)。

## Optimization Points
- ## Points
- 旧模板把 package 清理门在"用户确认批次已处置"、consume 清理门在"全部发现已路由"——两道确认在实践中都不会自然发生,导致 zip/条目无限期滞留(本会话实证:consume 留 2 zip、package 留 13 条,由用户人工提出才闭环)。教训已落模板:清理必须是运行的默认收尾步,确认对象降为"路由报告/打包完成"这一必然发生的时点;今后给任何命令设计清理步时,门条件应绑定在流程自身的事件上,而非外部 downstream 完成。
