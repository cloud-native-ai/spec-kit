---
id: "20261006T143136Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "speckit-feedback-pathA-introspection-20261006T140432Z"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-10-06T14:31:36Z"
summary: "Path A 一次完整走通,零执行。帽子判定:框架项目(root 实测 templates/skills/shared/scripts/src/specify_cli 五个源目录俱在,且按命令要求以不带尾斜杠的形式测于 root 而非 .specify/ 镜像);入站 feedback/ 实测零包,故 A1/A2 无对象、无 re-delivered/second-copy/orphan 标记可命"
---

## Review
Path A 一次完整走通,零执行。帽子判定:框架项目(root 实测 templates/skills/shared/scripts/src/specify_cli 五个源目录俱在,且按命令要求以不带尾斜杠的形式测于 root 而非 .specify/ 镜像);入站 feedback/ 实测零包,故 A1/A2 无对象、无 re-delivered/second-copy/orphan 标记可命名。路由:external_count 0、17 条全 kind internal,框架帽子下全部指向本项目 ⇒ Path A,Path B 未被选择(该帽子下 Path B 仅经显式 package 请求可达)。A3 自省:范围快照首轮读到 count 5,经与 index.json 交叉核对纠正为 **17**(该 count 为截断后计数,--limit 默认 5,是本轮最高优先发现 M-1/D-01,已单列 backlog 行);核验委派 5 个并行只读子代理按单元亲和度分组,全部对框架源取证、均注入 same-author 条件说明与显式异常行要求,回报 5 条 ANOMALY、0 条静默;其中 5 条 open 条目由本轮编排者自己在同一会话写下,故该子集检测强制委派(/speckit.feedback 不在 objective-analysis-gate 的 BINDING 名册内,按其 Scope limits 主动适用)。报告 introspection-20261006T140432Z 聚 7 个问题恰好覆盖 17 条(Excluded 无,附反空转哨兵说明),引擎 introspect-register 经 4 次 exit 2 修正后 linked 17;经用户 Confirm 后 --confirm 置 confirmed、disposed 17 全 processed、open 归零。A4 分流合计 7(direct-fix 4 / improve-docs 2 / speckit-requirements 1)+ 2 条核验期新发现(D-01 = --limit 截断计数,两半二选一**用户未裁定故未执行**;D-02 = 确认门控上限 owner 误指与字面量双副本),共写 9 条 backlog 行全部 open;另把 2026-09-23 那行 verify-territory-disjoint 语义裁定标注为**跨两轮未动**并并入 F-02。6 处冲突全部朝现行源码解决,含两处对编排者自撰条目的证伪(所引规则错配、行数算术不成立)。A5 零包删除。另报三条审计发现(均只报不修):probes --reconcile 已 zero-gap 使 2026-09-23 的「恒红 6 条」记载失效;outbox 现存包与该日志行所指不符且 package/mark-submitted 无日志行;同一件条目同时存在于已打包 outbox 与活动库、该包在框架帽子下无收件人故为过期副本,是否移除属裁定未动。计数器仍 16/threshold 10、should_prompt 仍 true(dispose 不重置,唯 mark-submitted 会)。

## Optimization Points
- **自省报告 schema 只能靠引擎拒绝反推 —— 而本轮正是「路由该缺陷」的那一轮又踩了它(死信新证)。** 落盘 draft 后 `introspect-register` 连续 **4 次 exit 2** 才通过:C-7 `unknown finding field line`(我写了 `- **问题陈述**:`,该字段不在允许集)→ C-7 再次(把问题陈述降为普通段落后仍被拒,说明 finding 体内**只允许六个字段行**,任何自由散文与缩进子项都算 unknown line)→ C-7 `no parseable members`(`_MEMBER_RE` 要求 `id(成立|部分成立|已过时|不成立)` 紧邻、id 字符类为 `[0-9A-Za-z-]+`,我的反引号与自定义注解括号双双破坏它)→ C-8 `malformed Excluded row`(空集必须写字面量 `无`,散文解释会被当行解析)。四条约束**没有一条**能在写报告前从命令模板或 `templates/` 得知:模板只说「以引擎 V-1 输出为准」,`templates/` 下无报告骨架,四字verdict 词表(`_MEMBER_RE` 于 `scripts/python/feedback-utils.py:313`)与 `无` 这一空集哨兵(`:450`)都只存在于源码。这与条目 `20260923T123804Z-speckit-feedback` 的 P1.2 同根,本轮已被 F-04 收编并分流 improve-docs —— 但**分流它的那一轮自己又完整重犯一次**,是该路由成为死信的新证据(与 backlog 里 2026-09-14 create-skills 那行同类)。建议:在 `templates/` 落一份带六字段与 `无` 哨兵的**报告骨架**,并在命令模板 A3 step 3 明写四字词表与「finding 体内不得有自由散文/子项」这两条最反直觉的约束。
- **`package` 与 `mark-submitted` 不写 consume-log 行,审计链有一个洞(本轮实测取证)。** `consume-log.md` 自述为「processed intake bundles 的审计链」,但 Path B 的两个动作都不在其中留痕。实测:outbox 现存 `feedback-20260923T125538Z.zip`,其 MANIFEST `Generated: 2026-09-23T12:55:38Z` 与 `--action status` 的 `submitted_at` **逐字相等** ⇒ 一次 package + mark-submitted 确实发生过;而 consume-log 无对应行,且 2026-09-23 行记载的待处置包是**另一个**文件(`feedback-20260923T113055Z.zip`,90,947 B、32 文件)并称 cleanup/mark-submitted「停在 dry-run」——该包现已不在。后果:活动库里 `20260923T123804Z-speckit-feedback` 仍为 open 并被本轮 Path A 消化,而它同时是那个已打包、无收件人、无从投递的 zip 的成员之一;没有任何制品能回答「这个包为什么存在、谁批准的、还该不该留」。建议:Path B 的 package 与 mark-submitted 各追加一行 consume-log(或另立一份 outbox 台账),记录 zip 名、Generated、条目集、submitted_at 与批准来源。
- token-efficiency — 为做 A1 的 already-consumed 交叉核对,我用 `tail -8` 整段读入了 `consume-log.md` 的 8 行历史,而该文件的行**极长**(单行可达数千字符,含整批路由明细),实测一次注入约 15 KiB;而本轮入站目录**零包**,A1/A2 无对象,我实际只需要 `Bundles` 一列来确认无待处理包。按摘要优先,应先以程序投影出 `| Date | Bundles |` 两列再读,或直接 `ls feedback/feedback-*.zip` 判空即止(后者已足以得出「零包」结论)。同轮其余读取均为投影式(index.json 只取 disposition 计数、`list --format json` 只取 id/unit/slice 字段、glossary 只取 Canonical/Origin/Status 三列),未发生原文转储;17 条条目的核验**全部委派**给 5 个并行只读子代理而非自读,符合大批次读取纪律。
