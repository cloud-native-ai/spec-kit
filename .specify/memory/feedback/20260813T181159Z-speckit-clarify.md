---
id: "20260813T181159Z-speckit-clarify"
unit_id: "/speckit.clarify"
unit_type: "command"
run_id: "040-agent-metadata-portability-clarify2-2026-08-13"
scope: "local"
feature: "040-agent-metadata-portability"
feature_id: "044"
partial: false
created: "2026-08-13T18:11:59Z"
summary: "第二轮澄清处理了一条用户修订指示(目录级 Worker/Meta 划分)并按 Scope Revision Protocol 完成级联:先做事实核对(conceptual-model.md 判据与用户指示一致)+ 术语表语音更正surface(2 处,用户确认),集成用户指示进 FR-023/023a/024/025 与 US5 后,就'7 个现有预置角色的归属'这一真实冲突提出双选项,用户选 B"
---

## Review
第二轮澄清处理了一条用户修订指示(目录级 Worker/Meta 划分)并按 Scope Revision Protocol 完成级联:先做事实核对(conceptual-model.md 判据与用户指示一致)+ 术语表语音更正surface(2 处,用户确认),集成用户指示进 FR-023/023a/024/025 与 US5 后,就'7 个现有预置角色的归属'这一真实冲突提出双选项,用户选 B(严格判据迁移)。随后联动改写 FR-023/023a/SC-001/Out of Scope/Key Entities/现状锚点,残留引用扫描通过(旧设计词仅存于 append-only 历史),Feature 044 详情与 checklist 同步。Clarifications 保持 append-only(累计 8 行,两轮各一节)。规格现 28 条 FR(含 023a)、8 SC、0 标记,可进入 /speckit.plan。

## Optimization Points
- **用户修订指示的级联改写应有机械核对清单**:第二轮是 scope 修订(7 角色定义从预置集迁往 Worker 模板),触发了 FR-023/023a/024/025、SC-001、Out of Scope、Key Entities、现状锚点、Feature 详情的多点联动。本次靠人工枚举完成,残留扫描(grep 旧设计词)兜住了底线,但"哪些小节必须联动"仍靠临场判断 —— 例如 SC-001 的"7 个预置"措辞若漏改会与迁移后的目录形态矛盾。建议 clarify 的 Scope Revision 流程里固化一张联动清单模板(FR/SC/Out of Scope/Key Entities/现状锚点/Feature 详情/checklist 七处),修订类会话逐项打勾,避免漏改依赖记忆。
- **术语表协议的语音更正闭环有效但缺登记**:本轮两处语音误写("Process/原 Agent"→预置/Meta Agent、"Server Agent"→笔误)经用户确认后更正,但更正结论只落在 Clarifications 里,没有进 glossary(glossary 协议要求写入需用户显式确认,本轮未单独问)。结果是同类误写下轮仍要重新推断。建议:语音更正被确认后,clarify 收尾时把"是否写入 glossary"并入最后一个确认问题一次问完,而不是留到下一轮重新发现。
- **token-efficiency**:FR 级联改写全部用唯一锚点小 Edit(一次 old_string 拼写失误被 Edit 工具当场拒绝,反而避免了错误写入 —— 说明精确匹配机制对长中文段落的防错价值);残留扫描用三个 grep 程序化完成,未整文件重读。可避免开销:读 conceptual-model.md 时 grep -E 'Worker|Meta' 带回 20 行,实际只需判据两行(:19-20)与写权限门(:34-44),先取行号再取片段会更省。
