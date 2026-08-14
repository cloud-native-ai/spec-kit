# Contract: Tool Metadata Mapping

契约对象:`src/specify_cli/__init__.py` 常量 `_AGENT_METADATA_MAPPING`(D4)。

## M-1 完备性

映射 MUST 覆盖 `AGENT_CONFIG` 全部 6 个工具键;每工具恰为一行,`mode ∈ {render, annotated}`(SC-003)。契约测试以 `AGENT_CONFIG` 键域动态对照,不得硬编码 6。

## M-2 出处与待核实

每行 MUST 携带 `provenance`:官方文档 URL,或"源码核实 + <ref>"。交付时 MUST 无 `待核实` 标志(SC-003)。当前状态:

| 工具 | mode | provenance | 备注 |
|------|------|-----------|------|
| qoder | render | https://docs.qoder.com/cli/subagent | `name`/`description` 必填;支持 `tools`/`skills`/`maxTurns`/`model`/`color`/`timeoutMins` 等;未知字段被忽略 |
| claude | render | https://code.claude.com/docs/en/sub-agents | 目标目录 `.claude/agents/`;字段清单在实现期对照官方文档二次核实后方可去掉"待核实";未能核实的字段按 D3 处理 |
| copilot | render | https://code.visualstudio.com/docs/copilot/customization/custom-agents;https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-custom-agents | 目标目录 `.github/agents/`;文件名 `<name>.agent.md`;支持 `description`(必填)/`tools`/`model`/`user-invocable`/`disable-model-invocation` |
| opencode | render | https://opencode.ai/docs/agents/ | 目标目录 `.opencode/agents/`(复数);`description` 必填;**文件名即 agent 名**;`mode: subagent` 表达非用户直接调用;`steps` 承载规模上限 |
| codex | annotated | openai/codex `codex-rs/core/src/config/agent_roles.rs` | 格式 TOML、落点 `$CODEX_HOME/agents/`(用户级 config 层,越出项目作用域)→ 本轮不渲染(FR-012) |
| hermes | annotated | 官方文档检索无成文约定 | 按 FR-014 静默跳过 |

## M-3 目标目录矩阵

| 工具 | 目标目录 | 文件名规则 |
|------|----------|-----------|
| qoder | `.qoder/agents/` | `<slug>.agent.md` |
| claude | `.claude/agents/` | `<slug>.md` |
| copilot | `.github/agents/` | `<slug>.agent.md` |
| opencode | `.opencode/agents/` | `<slug>.md`(文件名 = agent 名) |

矩阵变更 MUST 经 `_AGENT_METADATA_MAPPING` 单点修改(FR-012),MUST NOT 在渲染函数内硬编码目录。

## M-4 字段转换

每个 render 行的 `fields` MUST 为每个可渲染中立键给出:目标字段名、取值映射(含枚举转换,如 `model-tier` → 工具枚举)、或 `None`(该工具无对应物)。`supervisor`/`capacity-scope` 在所有工具均为 `None`(C-6)。

## M-5 无对应物统一策略(D3)

无对应物的中立字段 MUST **跳过不落盘**,并计入该次渲染的"未承载意图"汇总,在 init 反馈中按 agent 列出。策略文本 MUST 记录在映射常量头部注释,对所有工具一致适用(FR-013)。

## M-6 取值越界

中立取值不在目标工具枚举内(如未知 `display-color`)时,渲染 MUST 按 M-5 跳过该字段并计入汇总;MUST NOT 产出工具无法解析的取值。

## M-7 单点真源

渲染函数 MUST 只从 `_AGENT_METADATA_MAPPING` 读取目标目录、文件名规则与字段转换;代码其他位置 MUST NOT 出现并行的工具格式知识。
