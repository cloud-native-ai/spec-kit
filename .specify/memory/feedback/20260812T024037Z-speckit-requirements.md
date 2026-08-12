---
id: "20260812T024037Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "039-session-export-20260812-requirements"
scope: "local"
feature: "039-session-export"
partial: false
created: "2026-08-12T02:40:37Z"
summary: "039-session-export 规格一次成稿:4 user stories(US1/US2 P1 MVP、US3 P2 描述文档、US4 P3 团队追溯)、16 FR、6 SC、3 Shared Strings;背景承接前序会话命名 todo 的降级路线裁定清晰落规格;现状锚点全部源码实测(export.py 2093 行、10 产品矩阵、zip 形态、aone-open 上报段),port"
---

## Review
039-session-export 规格一次成稿:4 user stories(US1/US2 P1 MVP、US3 P2 描述文档、US4 P3 团队追溯)、16 FR、6 SC、3 Shared Strings;背景承接前序会话命名 todo 的降级路线裁定清晰落规格;现状锚点全部源码实测(export.py 2093 行、10 产品矩阵、zip 形态、aone-open 上报段),port-input 卫生执行到位;校验清单 16/16。

## Optimization Points
- ## Optimization Points
- 移植/改造型需求的规格阶段应程序化预探支持矩阵:本次「现状锚点」靠手工 grep 得出(10 产品 → 保留 4 / 新增 2 / 移除 6),若模板指引把「按适配器函数名/产品标识逐行枚举」作为 port-input 卫生的标准动作(输出小表),FR 的移除清单会更不易漏。
