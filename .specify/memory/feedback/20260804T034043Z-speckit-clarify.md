---
id: "20260804T034043Z-speckit-clarify"
unit_id: "/speckit.clarify"
unit_type: "command"
run_id: "036-team-summary-20260804T000000Z"
scope: "local"
feature: "036-team-summary"
partial: false
created: "2026-08-04T03:40:43Z"
summary: "Mode A 运行:目标 .specify/specs/036-team-summary/requirements.md。按 clarify-taxonomy 的 Mode A 分类做覆盖扫描后生成 5 问队列并逐题问答,5 问全部作答(Feature 绑定 / 工作项身份 / 默认启用语义 / 累积上限 / 历史条目降级路径),达到 5 题上限后停止。达成了命令的声明目的:消除了会实质改变下游 "
---

## Review
Mode A 运行:目标 .specify/specs/036-team-summary/requirements.md。按 clarify-taxonomy 的 Mode A 分类做覆盖扫描后生成 5 问队列并逐题问答,5 问全部作答(Feature 绑定 / 工作项身份 / 默认启用语义 / 累积上限 / 历史条目降级路径),达到 5 题上限后停止。达成了命令的声明目的:消除了会实质改变下游 plan 的四类歧义,并把 Feature 绑定从 Need clarification 收敛到 027。集成结果:29 条 FR(FR-001…FR-029 连续)、12 条 SC 各带 Measurement Source、5 条 Shared Strings 全部可解析、无遗留占位符、新增 Work Item Identity 实体。集成过程中自查发现并修复一处跨 FR 矛盾(FR-020 的 STATE.md 字节不变 vs FR-026 要求 STATE.md 扩展携带条目 ID),说明逐题写入后需要跨条款一致性扫描而非只做结构校验。用户在 Q2 覆盖了我的推荐(我建议派生键,用户选择显式发放条目 ID),该选择直接引出第 5 问的存量降级路径,属于问题链设计得当。摩擦主要来自环境与集成边界:memory 目录下多个文件 root 所有导致集成阶段才暴露写权限问题,且上游 checklist 在本次 clarify 后过期需手工回写。

## Optimization Points
- Mode A 的集成规则要求「每答一题即写入目标文件」,但一个答案可能同时改动上游 FR、下游 SC、Key Entities 与 Shared Strings 四处;本次 Q2(工作项身份)一答就新增 FR-026/FR-027、新增 SC-011、新增一条 Key Entity 并修订 FR-018/FR-025。建议命令显式要求:每答一题后做一次**跨 FR 一致性扫描**(尤其是新答案与既有 MUST NOT / 不变量类条款的冲突),而非仅做 markdown 结构校验。本次正是靠这一步才发现 FR-020「STATE.md MUST 保持字节不变」与 FR-026「STATE.md MUST 扩展携带条目 ID」的直接矛盾。
- Feature Binding 落在 `Related Feature` 一节,但命令没有要求把**绑定证据**一并写入。本次绑定 027 而非 013 的判据(027 的 Future Evolution 已预告此项;013 拥有 summarize-project 生命周期但 FR-024 禁止改动该技能,故变更面不匹配)如果不落盘,下一位读者只能看到一个 ID。建议 Feature Linkage 集成规则要求同时写入一到两句可复核的绑定证据。
- 命令的 Feature Integration 只指向 `features.md` 索引,未提到 `features/<ID>.md` 明细文件。本次需要额外手工完成:把 036 提升为 Latest Specification、把归档的 026 降级为 Historical、并在 027 的 Future Evolution 条目上标注「now specified by 036」。建议把明细文件的 Related Specifications 更新写入集成责任清单。
- 上游命令产出的 checklist 在 clarify 之后会**过期**(本次 checklist 的 Notes 仍写着「Feature 绑定 pending by design」,且验证结论只覆盖 clarify 前的 25 条 FR)。命令的 Scope Revision Protocol 有「re-validate 质量清单」一步,但常规 Mode A 路径没有。建议在常规路径也要求:凡本次 clarify 新增/修订了 FR 或 SC,必须回写一次 post-clarify 复验记录并修正已过期的 Notes。
- 写权限探测(Phase 0 步骤 3)只覆盖目标 spec 文件,不覆盖集成阶段真正要写的 `.specify/memory/` 下各文件。本次 `glossary.md`、`features.md`、`feedback/index.json` 均为 root 所有(mode 644),在问答全部结束、集成开始时才暴露,只能逐个用 recreate 补救;`rm`/`mv` 被 alias 成 `-i` 又导致首次写入静默 no-op。建议把探测面扩展到集成阶段的全部写入目标,并在同一时点 fail fast。
- token-efficiency: 本次 5 个问题的候选生成阶段为确认 `summarize-project` 的 R-tier 阻断条件与团队工件字段,读入了技能的 SKILL.md、references 与 schema 全文;其中大部分只为回答「哪些字段是必填、缺失时是否阻断」这一个判定。按 Summary-First,这类结构性判定应先用 grep/字段投影取定向摘录,仅在摘录不足时再升级读全文。集成阶段的校验做得较好(用一次 python 脚本统一输出 FR 计数/ID 连续性/STR 解析/占位符扫描,而非让 LLM 逐节复读),这一模式应固化为命令的默认校验方式。
