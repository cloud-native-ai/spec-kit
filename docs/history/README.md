# 项目历史会话知识库(docs/history)

本目录从 Claude Code 针对本项目的 **25 个历史对话 session**(约 28MB / 98 万字符)中提炼而成。不保存原文,只沉淀有长期价值的信息,按**主题聚合**组织。

提炼侧重五个维度:**① 关键决策与理由 ② 可复用经验/踩坑 ③ 未完成/待办 ④ 关键交互流程 ⑤ 用户与模型之间的冲突/分歧点**。

> 生成于 2026-07-14。源 session 位于 `~/.claude/projects/-storage-project-cloud-native-ai-spec-kit/*.jsonl`。此知识库可由 `/speckit.history` 命令增量重建(见 [docs/commands/history.md](../commands/history.md))。

## 阅读顺序

**先读 [[00-cross-cutting-lessons]]** —— 跨所有会话反复出现的坑与约定(镜像同步、脚本名、权限、测试基线、SDD 关卡…),是本项目最该先看的一页。

## 主题文档

| 文档 | 主题 | 覆盖 session | 时间跨度 |
|------|------|-------------|----------|
| [00-cross-cutting-lessons.md](00-cross-cutting-lessons.md) | 跨会话通用经验与踩坑 | (全部) | — |
| [01-agent-system-evolution.md](01-agent-system-evolution.md) | Agent 机制与角色体系演进(014→015→264→022) | 46696883, 5e7f0ff3, 26d59af9, 264ad40c, 5ee06f07, 12df2298 | 06-15 → 07-07 |
| [02-commands-and-cli-tools.md](02-commands-and-cli-tools.md) | 命令与 CLI 工具体系(/speckit.tools 016、CLI 分层 018、移除废弃工具) | 101d217a, 207f8d40, 12df2298 | 06-17 → 06-22 |
| [03-skills-system.md](03-skills-system.md) | Skills 体系建设(017 合并、git-workflow 三模式、021 Agent 特定配置) | 031835d1, 46a705d0, 5878b07d | 06-18 → 06-25 |
| [04-draw-plantuml-optimization.md](04-draw-plantuml-optimization.md) | draw-plantuml 长期优化(打分迭代、专项图、离线渲染、PlantUML 技巧) | ee7d6b0a, 037a7e53, eac5d261, c243363f, fe67eaef | 07-02 → 07-14 |
| [05-docs-and-governance.md](05-docs-and-governance.md) | 文档、依赖与项目治理(命令文档、上游同步、依赖清理、team goal/sdd-workflow) | f265adf7, 40cdddea, 217c6503, eac5d261 | 06-18 → 07-14 |

## 贯穿全程的几条"元结论"

1. **本项目定位 = 文档/prompt 框架,不是运行时平台。** 这是所有"是否采纳/同步/新增"决策的最高标尺(上游 3 个月改动整批不同步;supervisor 只是 prompt 指令不做运行时调度)。参见 [[feedback_no-dfx-overdesign]]。
2. **单一权威源 + 镜像/symlink 桥接**是本项目的核心架构模式(`.specify/` 为权威,各工具目录桥接)。改一处必须同步所有镜像——这也是最高频的返工来源。
3. **模型倾向"差不多就收尾",用户坚持更高标准并要求定位根因**——这是冲突点里反复出现的模式,且多数情况用户判断更准(如小图根因是脚本 bug、Integration 架构对本项目无意义)。
4. **SDD 流程有硬关卡**:Feature 复用优先、状态不倒退、Pre-Status-Flip Gate、Deferred 用 `[~]` 显式登记、纯模板 feature 的 Test-First 判 Partial。

## 未纳入主题的会话(元问题/琐碎,一句带过)

- `8d42ff83` / `5eba4259` / `9cf6968d` / `41a4ae60` — "如何获取 Claude Code 历史 session/对话记录" 等元问题,无项目产出。
- `cedfb1d7` — 仅一条 local-command caveat,无内容。
- `03cf50d0` — 本次"整理历史 session"任务的早期分身。

---

_相关记忆:[[feedback_no-dfx-overdesign]] · [[feedback_plantuml-layout-techniques]] · [[reference_plantuml-offline-render]]_
