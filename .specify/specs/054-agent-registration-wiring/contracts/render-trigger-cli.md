# Contract: Render Trigger CLI(渲染触发命令)— 054

**Scope**: FR-004(触发半)、FR-005(容量承载的上游机制)。实现主体:`src/specify_cli/__init__.py` 新增子命令。从句形态:`md-bold-closed`(语法真源 `shared/definitions/contract-clause-definitions.md`)。

## § 命令形

**C-1**: 子命令名 `render-agents`,注册于既有 typer app(与 `init`(:2653)、`check`(:2993)并列);`--ai <tool>` 必填;项目路径解析与 `init` 相同规则,项目路径不得为 `.specify` 运行时目录本身(既有防嵌套守卫沿用)。

**C-2**: `<tool>` 值域 = `_AGENT_METADATA_MAPPING` 中 `mode == "render"` 的键集(qoder/claude/copilot/opencode);annotated 模式工具(codex/hermes)或未知名 → 参数错误,退出非 0,报合法值列表。(FR-004)

## § 行为

**C-3**: MUST 委派既有 `render_agents_for_tool(project_path, tool)`——真文件渲染、manifest 漂移检测(改过的产物先备份)、陈旧产物修剪(仅 manifest 记录集)、legacy 符号链接替换迁移、用户资产不动,全部沿用,不复制渲染逻辑。

**C-4**: 单次调用渲染一个工具;对同一项目重复调用幂等(产物稳定、manifest 增量、备份仅在真实漂移时发生);rendered = 0 是合法成功(空中性层 → 空注册面,退出 0)。

## § 输出与退出码

**C-5**: 成功:人读摘要一行(rendered/backups/unmapped 计数取自 stats)+ 退出 0;元数据校验失败:`AgentMetadataError` 的既有点名输出(文件 + 键)+ 退出非 0;参数错误:报错并列出合法值 + 退出非 0。

## § 容量承载(FR-005 的机制面)

**C-6**: 渲染产物 MUST 按既有字段映射携带中性键(`model-tier→model`、`capability-tools→tools`、`run-turn-budget→maxTurns` 等,`_AGENT_METADATA_MAPPING[tool]["fields"]`);`team-scope` 属 framework-only 键,不渲染。由此派发侧可达:宿主注册类型携带 capacity-tools/model-tier/run-turn-budget 与 system prompt,`templates/commands/agents.md` 既有派发要求在席位场景下成立。

## § 教学与守卫(指针,不属本契约)

本命令的教学面(agents 命令模板与 create-agent 技能教授触发真相)与守卫(契约测试钉命令存在性、值域、stats 投影)由 `teaching-and-guards.md` 拥有(其 C-3 触发真相、C-4/C-9 守卫);本文不重复。

**验收示例前提**(供 /speckit.implement 复测):`specify render-agents --ai qoder` 退出 0 依赖——子命令已实现且目标项目 `.specify/agents/{templates,instances}/` 定义通过校验;stats 数值以实跑为准,本文不预写数值。
