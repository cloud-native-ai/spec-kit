# Contract: Render Trigger CLI(渲染触发命令)— 054

**Scope**: FR-004(触发半)、FR-005(容量承载的上游机制)。实现主体:`src/specify_cli/__init__.py` 新增子命令。

## C-1 命令形

- C-1.1: 子命令名 `render-agents`,注册于既有 typer app(与 `init`、`check` 并列)。
- C-1.2: 参数:`--ai <tool>`(必填)。`<tool>` 值域 = `_AGENT_METADATA_MAPPING` 中 `mode == "render"` 的键集(qoder/claude/copilot/opencode);annotated 工具(codex/hermes)或未知名 → 参数错误,退出非 0,报合法值列表。
- C-1.3: 项目路径解析与 `init` 相同规则(当前目录或 `--here` 语义对齐既有实现);项目路径不得为 `.specify` 运行时目录本身(既有 `AgentMetadataError` 防嵌套守卫沿用)。

## C-2 行为

- C-2.1: MUST 委派既有 `render_agents_for_tool(project_path, tool)`——真文件渲染、manifest 漂移检测(改过的产物先备份)、陈旧产物修剪(仅 manifest 记录集)、legacy 符号链接替换迁移、用户资产不动,全部沿用,不复制渲染逻辑。
- C-2.2: 单次调用渲染一个工具;对同一项目重复调用幂等(产物稳定、manifest 增量、备份仅在真实漂移时发生)。
- C-2.3: rendered = 0 是合法成功(空中性层 → 空注册面,退出 0)。

## C-3 输出与退出码

- C-3.1: 成功:人读摘要一行(如 `rendered N agent(s) for <tool>`,N 与 backups/unmapped 计数取自 stats)+ 退出 0。
- C-3.2: 元数据校验失败:`AgentMetadataError` 的既有点名输出(文件 + 键)+ 退出非 0。
- C-3.3: 参数错误(非渲染模式工具/未知名):报错并列出合法值 + 退出非 0。

## C-4 容量承载(FR-005 的机制面)

- C-4.1: 渲染产物 MUST 按既有字段映射携带中性键(`model-tier→model`、`capability-tools→tools`、`run-turn-budget→maxTurns` 等,`_AGENT_METADATA_MAPPING[tool]["fields"]`);`team-scope` 属 framework-only 键,不渲染。
- C-4.2: 由此派发侧可达:宿主注册类型携带 capacity-tools/model-tier/run-turn-budget 与 system prompt——`templates/commands/agents.md` 既有派发要求(「with its configured …」)在席位场景下成立。

## C-5 触达面与守卫

- C-5.1: `templates/commands/agents.md` 与 `skills/create-agent/SKILL.md` 的触发真相段 MUST 教授本命令为上宿主面的正道(取代「或建议跑 `specify init`」的旧措辞;init 仍是首次安装入口,不删其文档)。
- C-5.2: 契约测试 MUST 钉:子命令存在性与参数值域(对 annotated 工具报错)、成功路径 stats 投影、校验失败路径退出码(见 `teaching-and-guards.md` C-8)。

**验收示例前提**(供 /speckit.tasks 与 /speckit.implement 复测):`specify render-agents --ai qoder` 退出 0 依赖——子命令已实现且本项目 `.specify/agents/{templates,instances}/` 定义通过校验;stats 数值以实跑为准,本文不预写数值。
