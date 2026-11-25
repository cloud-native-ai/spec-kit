---
id: "20261013T170150Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "consume-20261013-batch4"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
disposition: "processed"
partial: false
created: "2026-10-13T17:01:50Z"
summary: "框架帽子(五源目录俱在,batch 3 同)⇒ 全 Path A。14 条物料:本地 2(含 1 条外来污染)+ 孤儿包 12(客户项目 @23617b8a=HEAD~2,框架文件逐字节同 ⇒ 零 ALREADY-FIXED)。1 并行只读核验器对框架源取证(注入 fast-fail 子句,1 ANOMALY/0 静默)+ 编排者直接核验本地 2 条;33 点 = 21 STILL-VALID/2"
introspection_ref: "introspection-20261015T081832Z#F-03"
disposition_reason: "introspection:introspection-20261015T081832Z#F-03"
---

## Review
框架帽子(五源目录俱在,batch 3 同)⇒ 全 Path A。14 条物料:本地 2(含 1 条外来污染)+ 孤儿包 12(客户项目 @23617b8a=HEAD~2,框架文件逐字节同 ⇒ 零 ALREADY-FIXED)。1 并行只读核验器对框架源取证(注入 fast-fail 子句,1 ANOMALY/0 静默)+ 编排者直接核验本地 2 条;33 点 = 21 STILL-VALID/2 PARTIAL/10 NOT-OURS(4 条 confirm-gate 整条 NOT-OURS)。路由 11 新行 + 3 既有行更新(backlog 53→64),最高优先为 feedback 引擎自身 dry-run/破坏性选取卫生(reindex 门前 unlink index.json = 确认门控绕过)。本地 2 条 dispose=processed、孤儿包留底后删、open 归零、入站空。运行判定:qualified;token/耗时/制品正确性均 not_evaluated(本轮无源)、满意度 pending_next_turn;trigger_feedback=false 故不上提交提示(框架帽子下亦不得荐打包)。未出正式 A3 报告(本地仅 2 条且点已本会话对源码核验、包条目按 V-3 不能作成员),如实记录为判断。

## Optimization Points
- 路径解析陷阱在本命令的存储面现身且无守卫:一条客户项目 consume 运行的条目(20261013T162525Z,自述根级无 templates/skills/shared/src/specify_cli、scripts 为 build.sh/generate-mybatis-plus.sh)被误投进框架仓 .specify/memory/feedback/ 并被本仓 probe 注册表正常解析,直到本轮消化读到外来内容才暴露。record 时不盖任何 workspace 身份事实(框架帽子布尔/根路径指纹),consume 侧也无「条目自述仓库 ≠ 本仓」检测 ⇒ 误投在两轮之间不可见。建议:record 落一枚 workspace 身份戳,consume 的 A1/inventory 增一条「外来条目」检测并单独呈报,使 AGENTS.md 所预告的「workspace state written into the framework repo」有机器哨兵而非靠人读出来。
- A3 缺小批量快路,导致纪律被各自即兴绕过:本轮(本地 2 条、点已本会话对源码核验)与外来条目 162525Z 的作者(本地 1 条、同会话已核验)各自独立选择不出正式 introspection 报告、改为直接 dispose + 披露。path-a-digest.md 的 A3 对任意非零 scope 都隐含要报告,却无相称性阈值,于是「2 条已核验」与「32 条跨批」走同一套 ceremony 不合理,agent 只能即兴并自证。建议 A3 明写一条小批量直处置档(N 条低于阈值且点已对现行源核验 ⇒ dispose --reason 路由、不落报告文件),把已被两次独立采用的即兴行为收编为受制裁路径,并要求该档同样在 consume-log 留路由痕迹。
- feedback 引擎自身的 dry-run/破坏性选取缺陷由本命令机器面暴露,应作为本单元自缺陷跟踪而非仅外部发现:--action package 与 --action reindex 均不读 args.dry_run(package 静默落盘 zip、reindex 更在 Stage-5 确认门前 unlink 旧 index.json),action_cleanup 不写 submitted_at 而 mark_submitted 在 submitted_at=null 时全选 ⇒ 未投递条目被记成已投递并多产 zip。三者同根(干跑语义与破坏性动作未对齐确认门),已路由为 backlog 最高优先行;本单元(/speckit.feedback)的 path-b-and-probe.md step5/6 次序文档需随之修正,否则客户项目照文档执行即触发误标。
