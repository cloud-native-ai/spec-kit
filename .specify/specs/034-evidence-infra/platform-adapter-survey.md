# Platform Adapter Survey(spec 034 US7 / T038)

> 交付边界(Clarify Q3):本 spec 仅交付本探测报告与定序建议;新适配器实现属后续独立迭代。
> 现状判定依据:**源码探测**(引擎子集实际代码)+ doctor 本地落盘探测,不依赖上游 roadmap 文档(FR-012)。

## doctor 探测快照(2026-07-29,本机)

| 工具 | 本地会话落盘 | 探测路径 |
|------|-------------|---------|
| qoder | **detected** | `~/.qoder/projects` |
| claude | **detected** | `~/.claude/projects` |
| codex | not-detected | `~/.codex/sessions` |
| copilot | not-detected | `~/.copilot/session-state` |
| opencode | not-detected | `~/.local/share/opencode` |
| qwen | not-detected | `~/.qwen/tmp` |
| hermes | not-detected | `~/.hermes/sessions` |
| iflow | not-detected | `~/.iflow/tmp` |

注:not-detected 只代表**本机**无落盘,不代表工具不支持;各项目环境应各自跑 doctor 定序。

## 引擎子集适配器现状(源码探测)

| 工具 | 会话适配器 | 资产 provider | 状态 |
|------|-----------|--------------|------|
| qoder | `session-analysis/platforms/qoder.mjs`(完整,内联旧模式) | `agent-customize/providers/qoder.mjs` | 直接可用 |
| codex | `platforms/codex.mjs`(可用,缺模型/Hook 证据) | `providers/codex.mjs` | 直接可用,缺口标 Unobserved |
| claude | `platforms/claude.mjs`(469 行,provider-runner 模式) | `providers/claude.mjs`(531 行,已注册) | **核实补齐**(代码在、上游未背书;时间戳等缺口待 fixture 验证) |
| cursor | `platforms/cursor.mjs`(弱,eventTimestampCoverage partial) | `providers/cursor.mjs` | 不在 spec-kit 支持矩阵,保留不动 |
| copilot/opencode/qwen/hermes/iflow | 无 | 无 | 自研候选(下表) |

## 后续实施定序建议(按本机探测修正的初始候选序)

| 序 | 工具 | 依据 | 工作量注记 |
|----|------|------|-----------|
| 1 | **claude 核实补齐** | 本机已 detected + 双侧源码已存在——最低成本点亮第三个平台 | 小:fixture 测试 + 缺口显式标注即可 |
| 2 | opencode | 会话存储为本地 JSON(`~/.local/share/opencode`),格式公开 | 中:仿 provider-runner 模式新写 |
| 3 | qwen | 存储格式类 Claude JSONL,可低成本仿写 | 中 |
| 4 | iflow | 同 qwen 系(`~/.iflow/tmp`) | 中 |
| 5 | hermes | 落盘格式待核实 | 中~大 |
| 6 | copilot | CLI 会话落盘能力最弱,探测到落盘前不投入 | 待定 |

## 扩展机制约束(引自 FR-012,对后续迭代生效)

- 新会话适配器:继承 `SessionAnalyzer` 五虚方法,**优先 provider-runner 模式**(claude/cursor 已用);同时需在 `analyzer.mjs` 的 `loadPlatform` 分发中登记(勘察确认为显式分支,非自动发现)。
- 新资产 provider:注册进 `agent-customize/providers/index.mjs` 的 `PROVIDER_COLLECTORS` 分发表。
- 每个新适配器:走既有脱敏漏斗(不得绕过 privacy-safe-text/semantic-facets)、能力缺口显式标注(学 cursor 的 `eventTimestampCoverage: "partial"`)、附最小 fixture 测试;doctor 的 `PLATFORM_SESSION_STORES` 表同步更新探测路径。
- 全部修改记入 `scripts/js/better-harness/UPSTREAM.md` 修改日志,并同步双镜像。
