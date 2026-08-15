# History — spec-kit 项目会话知识库

> 由 `/speckit.history` 从 **Claude Code** 会话存储（`~/.claude/projects/-storage-project-cloud-native-ai-spec-kit`）增量蒸馏生成。
> 不保存原文转录，只保留长期价值：关键决策、可复用经验、待办、交互流程、用户↔模型分歧点。
> 生成日期：2026-08-15（首次运行，23 个会话中发现 16 个有效会话；7 个琐碎/元会话按启发式跳过）。

## 主题索引

| 主题文档 | 覆盖会话 | 日期跨度 |
|----------|----------|----------|
| [[00-cross-cutting-lessons]] | 全部（跨主题复现的教训） | 2026-06-22 → 2026-07-17 |
| [[01-draw-plantuml-optimization]] | 6 个（ee7d6b0a, fe67eaef, 037a7e53, c243363f, eac5d261, c10b41cf） | 2026-07-02 → 2026-07-17 |
| [[02-sdd-feature-lifecycle]] | 4 个（207f8d40, 5878b07d, 5ee06f07, b252f216） | 2026-06-22 → 2026-07-17 |
| [[03-framework-mechanics]] | 5 个（217c6503, 46a705d0, 2a38dcaf, 7d64ad76, cefe2c64） | 2026-06-23 → 2026-07-17 |
| [[04-history-command-origin]] | 1 个（03cf50d0） | 2026-07-14 |

## 阅读顺序

1. 先读 [[00-cross-cutting-lessons]] —— 环境坑、镜像双写纪律、测试基线纪律在几乎所有会话中反复出现。
2. 按需进入主题：图表技能优化看 [[01-draw-plantuml-optimization]]；走完整 SDD 流程看 [[02-sdd-feature-lifecycle]]；改框架命令/模板/脚本看 [[03-framework-mechanics]]。
3. [[04-history-command-origin]] 记录了 `/speckit.history` 命令自身的设计决策，是本知识库的"出生证明"。

## 跨会话元结论

- **双写同步是本项目最高频返工源**：canonical（`templates/` `skills/` `shared/`）→ `.specify/` 镜像 → per-tool 生成副本，三层任何一层漏改都会漂移；`diff -rq` 逐对校验 + 生成器（`generate_commands` / `rewrite_paths`）再生是唯一可靠路径。
- **测试基线纪律贯穿所有特性会话**：动手前记录全量基线，收尾对比失败集而非总数；硬编码数量断言（如 5 个官方工具）在扩容时必然断裂。
- **用户↔模型分歧的稳定模式**：用户反复推动"更深的语义层 / 更严格的验证 / 更彻底的移除"，模型默认偏保守迭代；多轮冲突后落地的用户方案（语义布局规划、default-on supervision、四层产物结构）事后都被证明正确。
- **环境故障是客观存在的工作负载**：root 属主目录、`cp -i` alias、沙箱假象在 ≥5 个会话中独立复现，处置手法已模板化（见 [[00-cross-cutting-lessons]]）。
- **多 Agent 闭环有效但有平台期**：draw-plantuml 优化经 4 种编排形态（双角色 / 三角 EEI / 进化 workflow / team-loop 锦标赛）将 49 分提到 91 分；3 代无提升说明策略池穷尽，须换策略族而非加轮数。

## 运行说明

- `.work/` 为一次性提取草稿（已 git-ignore，可随时删除）；`.manifest.json` 记录已蒸馏会话，重跑只处理新增会话并合并进本目录文档。
- 跳过未蒸馏的 7 个会话（138–1452 字符）：三个 `/exit` 空会话（cedfb1d7, 9e462a2a, 04fca7e6）、三个"如何获取历史 session"元提问（8d42ff83, 9cf6968d, 5eba4259）、一个 18 字符空会话（41a4ae60）——无长期价值，故不在 manifest 中登记。
