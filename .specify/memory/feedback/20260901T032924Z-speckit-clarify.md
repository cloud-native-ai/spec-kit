---
id: "20260901T032924Z-speckit-clarify"
unit_id: "/speckit.clarify"
unit_type: "command"
run_id: "048-docs-reconcile-clarify-20260901"
scope: "local"
probe: "speckit-clarify-wrapup"
kind: "internal"
slice: "commands"
feature: "048-docs-reconcile"
partial: false
created: "2026-09-01T03:29:24Z"
summary: "Mode A 运行,目标 requirements.md。分类扫描后 3 类需澄清(Feature Linkage 缺失、目标声明归属面 Partial、内容动作量无界 Partial),9 类 Clear;三问彼此独立故合并一批提问,均带 Recommended 与落地后果预览。三项决策全部集成并逐次落盘:Related Feature 解析为 037(附证据链)、FR-001 补归属面 + 新"
---

## Review
Mode A 运行,目标 requirements.md。分类扫描后 3 类需澄清(Feature Linkage 缺失、目标声明归属面 Partial、内容动作量无界 Partial),9 类 Clear;三问彼此独立故合并一批提问,均带 Recommended 与落地后果预览。三项决策全部集成并逐次落盘:Related Feature 解析为 037(附证据链)、FR-001 补归属面 + 新增 FR-002a、FR-008 明确无上限 + 新增大规模扇出边界情况;同步收窄 Out of Scope/Assumptions,履行既有 Feature 的注册义务(features.md 行追加 + features/037.md 交叉引用)。提问前完成可写性探针,提问后完成占位符/追加式不变量/标题结构/FR 计数/Total Features 五项校验。用户在两处选择了带已识别代价的选项,均已补相应约束性条款。

## Optimization Points
- Mode A 集成规则要求"Feature linkage → 更新 Related Feature",但对绑定到既有 Feature 的情形未说明注册义务(新 Feature 才有明确的分配ID/建索引行/加反向引用清单);本轮据 041 先例自行补了 features.md 行追加与 features/037.md 交叉引用,建议在 clarify-taxonomy.md Mode A 规则中把"绑定既有 Feature"的义务显式写出(至少:详情文件 Related Specifications 追加 + 索引行 follow-up 注记),避免不同运行做法不一致
- 本轮三问经 AskUserQuestion 的 preview 字段呈现"选项落地后果",用户据此在有语义张力的选项(运行工作区承载跨运行契约)上做出知情选择;命令模板当前只规定 Markdown 表格 + Recommended 标注,未提示可呈现"该选项将产生的规格改动"这一维度,建议把"每个选项附落地后果预览"纳入提问格式建议
- 用户选择了带已知语义张力的选项(声明落按次运行痕迹目录)与无上限扇出;两者都需在规格侧补约束才不致埋雷(FR-002a、扇出前告知+中止+pending 结转)。建议在 Mode A 集成规则中加一条:当用户选择的选项存在已识别的张力或代价时,集成 MUST 连带写入相应的约束性 FR/边界情况,而不是只记录 Q→A
