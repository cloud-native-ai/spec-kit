---
id: "20260923T113303Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "052-fast-fail-principle:feedback-package:20260923T113055Z"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
feature: "052-fast-fail-principle"
partial: false
created: "2026-09-23T11:33:03Z"
summary: "本轮 /speckit.feedback 以显式 `package` 参数进入,按 Routing flow 第 1 步短路至 Path B(跳过步骤 2–5 的帽子/清单判定作为路由依据,但仍执行了帽子取证:根级 templates/skills/shared/scripts/src-specify_cli 五个目录实测存在,`src/specify_cli` 仅在根级——框架项目成立)。清单实"
---

## Review
本轮 /speckit.feedback 以显式 `package` 参数进入,按 Routing flow 第 1 步短路至 Path B(跳过步骤 2–5 的帽子/清单判定作为路由依据,但仍执行了帽子取证:根级 templates/skills/shared/scripts/src-specify_cli 五个目录实测存在,`src/specify_cli` 仅在根级——框架项目成立)。清单实跑:31 条条目全部 `kind: internal`、全部 `disposition` 为空(OPEN)、slice 为 commands 22 + skills 9、`introspection_ref` 命中 0、`partial` 1 条;`external_count: 0`,故引擎的 excluded_external 排除面为空。入站目录 `feedback/feedback-*.zip` 零包,Path A 无待消化物料。阈值 31/10、should_prompt=true。打包实跑成功:zip 落在 `.specify/memory/feedback/packages/feedback-20260923T113055Z.zip`,90,947 字节,`unzip -t` 全部 OK、零错误,包内 32 个文件(31 条目 + MANIFEST),MANIFEST 的 Entries=31、时间跨度 2026-09-14T02:27:57Z → 2026-09-23T11:05:28Z、spec-kit 0.0.22、install source 与 `--action upstream` 回报一致。因零条目携 `introspection_ref`,第 4 步的 `--include-introspection` 提议不适用,未触发。打包后复核 `--action status`:31/31 条目仍在库(引擎声明 sources untouched,实测相符)。零网络行为,zip 未由代理发送。收尾的第 5、6 步(清理与 mark-submitted)按快速失败纪律判为**裁定**而非纠正,已停在 dry-run 预览并上送用户,详见 Optimization Points 第 1 条。制品提交步:本轮唯一制品即该 zip,实测被 `.gitignore:45 *.zip` 忽略,`git status --porcelain` 对 `.specify/memory/feedback/` 与 `feedback/` 均为空——无可提交面,按约定跳过而非造空提交。

## Optimization Points
- Path B 第 5 步的收尾清理在文本上无条件,但在框架帽子下不可判定:技能已声明框架项目的 Path B「是应请求而非依判断而进入」,第 5 步却没有对应的帽子条件。本仓上游解析为自身(`--action upstream` 回报 install-source 即本仓),打出的包没有收件人;若照默认执行 `--action cleanup`,会把 31 条从未被 Path A 就地消化的条目从活动库移除,使其唯一可操作形态只存在于一个无法送达的 zip 内。建议:第 5 步改为帽子感知——框架项目里仅当用户同时要求 `mark-submitted`(即该批确已了结)时才清理,否则保留并在报告中列为待定;客户项目维持现默认。本轮据此停在 dry-run 预览,未执行清理,也未执行 `mark-submitted`(后者断言「批次已处置」,本地不可观测,属裁定而非纠正)。
- `--action cleanup --dry-run` 的输出是裸 id 数组(31 行)+ `removed: []` + `remaining_entries`,没有待移除条数的头部字段;消费方必须自己数数组长度才能形成判断,违背摘要优先。建议引擎在该 JSON 顶层补 `would_remove_count`(以及 `remaining_after`),使预览可作摘要消费而不必先吞下整个 id 列表。
