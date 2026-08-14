---
id: "20260813T151845Z-speckit-clarify"
unit_id: "/speckit.clarify"
unit_type: "command"
run_id: "040-agent-metadata-portability-clarify-2026-08-13"
scope: "local"
feature: "040-agent-metadata-portability"
feature_id: "044"
partial: false
created: "2026-08-13T15:18:45Z"
summary: "Mode A 对 requirements.md 的澄清完整收敛:提问前先用子代理对六家 AI agent CLI 的 agent 格式做官方文档核实(fact-vs-decision 的外部延伸),据此重写 Q3 选项空间;5 个发现型问题(Feature 绑定、元信息载体、目标目录矩阵、手改产物再渲染行为、三目录消歧)逐一裁定并回写,另加 1 个由用户自由文本回答派生的显式超上限确认(三维度模"
---

## Review
Mode A 对 requirements.md 的澄清完整收敛:提问前先用子代理对六家 AI agent CLI 的 agent 格式做官方文档核实(fact-vs-decision 的外部延伸),据此重写 Q3 选项空间;5 个发现型问题(Feature 绑定、元信息载体、目标目录矩阵、手改产物再渲染行为、三目录消歧)逐一裁定并回写,另加 1 个由用户自由文本回答派生的显式超上限确认(三维度模型 vs Worker/Meta 判型的读法)。集成纪律全程保持:Clarifications 行数严格递增(1→5)、FR-002/FR-012/FR-021/FR-023/FR-024 标记全部消除、SC-002/SC-003/FR-014 随矩阵裁定同步调整、两处边界情形标注'已裁定'、Feature 044 完整注册(index 行 + features/044.md + 033 反向交叉引用)、checklist 全绿。规格现 0 标记、27 FR、8 SC,可直接进入 /speckit.plan。

## Optimization Points
- **问题预算应为"用户回答派生的确认"单列一档**:本轮在 5 问上限处收到了用户的自由文本回答(Q5),该回答引入了与既有概念模型冲突的新框架(三维度划分 vs Worker/Meta 判型),必须再问一次确认才能安全集成 —— 这次确认既不是发现型提问,也不该静默超上限。现行 clarify 模板只说 "max 5 questions / never exceed",没有为"用户回答本身派生的确认"留位置,执行者只能在静默超上限、猜测集成、升级 /speckit.interview 三者间硬选。建议模板明确:由用户回答直接派生的澄清确认不计入发现型 5 问预算,但必须显式编号并声明派生来源(本轮第 6 问即按此自律执行)。
- **外部事实核实应成为 Mode A 的前置显式步骤**:本轮最大的收益来自提问前派子代理对六家 AI agent CLI 的 agent 格式做官方文档核实 —— 它直接改写了 Q3 的选项空间(claude 的规范位置是 `.claude/agents/` 而非现状的 `.github`;codex 是 TOML 且落点在用户级 config 层),避免把猜测的字段名写进需求。现行 clarify 的"事实-决策分离"只覆盖"仓库内可回答的事实",不覆盖"外部系统格式/协议类事实"。建议在 taxonomy 的 Mode A 清单里加一条:当需求引用外部工具的格式、字段或协议时,先做外部依据探测(可并行子代理),探测结果作为选项表的证据注入,未核实项显式降级为"待核实"选项。
- **token-efficiency**:集成全部走小锚点 Edit(features.md 846 字符长行先用 `sed tail -c` 取唯一尾锚再编辑,避免整行注入);每轮集成后用 `grep -c '^- Q:'` 程序化验证 append-only 行数严格递增(1→2→3→4→5),未做整文件重读。可避免的开销一处:Feature 索引全量行(`grep -E '^\| [0-9]{3}'`)一次性拉回 20+ 行超长行,其中多数与本需求无关 —— 更省的做法是先只取 ID+Name+Status 三列投影,命中候选后再取全行。
