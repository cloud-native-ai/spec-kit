# History — spec-kit 项目会话知识库

> 由 `/speckit.history` 从 AI 工具的会话存储增量蒸馏生成。
> 不保存原文转录，只保留长期价值：关键决策、可复用经验、待办、交互流程、用户↔模型分歧点。
>
> - **Claude Code 纪元**（2026-08-15 首次运行）：存储 `~/.claude/projects/-storage-project-cloud-native-ai-spec-kit`；23 个会话中发现 16 个有效会话，7 个琐碎/元会话按启发式跳过。主题 [[00-cross-cutting-lessons]] 至 [[04-history-command-origin]] 来自该轮。
> - **Qoder 纪元**（2026-11-10）：Qoder CLI 会话存储；**125 个会话中蒸馏 108 个，17 个琐碎会话按同一启发式跳过**；五线程聚合为主题 05–09。`.manifest.json` 现记录 Qoder 轮的 108 个 sid；Claude 轮的 manifest 原样保存为 `.manifest.claude-era.json`。

## 主题索引

| 主题文档 | 覆盖会话 | 日期跨度 |
|----------|----------|----------|
| [[00-cross-cutting-lessons]] | 全部 124 个有效会话（16 Claude + 108 Qoder；跨主题复现的教训） | 2026-06-22 → 2026-11-10 |
| [[01-draw-plantuml-optimization]] | 6 个（ee7d6b0a, fe67eaef, 037a7e53, c243363f, eac5d261, c10b41cf） | 2026-07-02 → 2026-07-17 |
| [[02-sdd-feature-lifecycle]] | 4 个（207f8d40, 5878b07d, 5ee06f07, b252f216） | 2026-06-22 → 2026-07-17 |
| [[03-framework-mechanics]] | 5 个（217c6503, 46a705d0, 2a38dcaf, 7d64ad76, cefe2c64） | 2026-06-23 → 2026-07-17 |
| [[04-history-command-origin]] | 1 个（03cf50d0） | 2026-07-14 |
| [[05-agents-skills-tools]] | 41 个（T1；完整 sid 清单见文内） | 2026-10-05 → 2026-11-10 |
| [[06-anchoring-goal-team]] | 33 个（T2；完整 sid 清单见文内） | 2026-10-06 → 2026-11-10 |
| [[07-archive-history-session]] | 41 个（T3；完整 sid 清单见文内） | 2026-10-06 → 2026-11-10 |
| [[08-derive-review-interview]] | 39 个（T4；完整 sid 清单见文内） | 2026-10-05 → 2026-11-10 |
| [[09-memory-state]] | 44 个（T5；完整 sid 清单见文内） | 2026-10-08 → 2026-11-10 |

> 线程计数按"带该标签的会话数"统计（一个会话可进多条线程）；五线程标签合计 198 条，覆盖全部 108 个 Qoder 会话。

## 阅读顺序

1. 先读 [[00-cross-cutting-lessons]] —— 环境坑、镜像/生成器纪律、测试基线、重命名债、真空绿谱系在几乎所有会话中反复出现。
2. 按需进入主题：图表技能优化看 [[01-draw-plantuml-optimization]]；走完整 SDD 流程看 [[02-sdd-feature-lifecycle]]；改框架命令/模板/脚本看 [[03-framework-mechanics]]。
3. [[04-history-command-origin]] 记录了 `/speckit.history` 命令自身的设计决策，是本知识库的"出生证明"。
4. Qoder 轮按线程进入：agent/skill/tool 分层看 [[05-agents-skills-tools]]；目标/团队编排与 anchoring 重命名看 [[06-anchoring-goal-team]]；历史/归档/驾驶证据看 [[07-archive-history-session]]；分析门/独立验证/访谈看 [[08-derive-review-interview]]；存储/registry/状态证据看 [[09-memory-state]]。
5. 跨线程问题按"证据从哪来"读：先 [[09-memory-state]]（状态与基线），再 [[07-archive-history-session]]（记录与波次），最后回 [[00-cross-cutting-lessons]] 对照稳定模式。

## 跨会话元结论

- **双写同步是本项目最高频返工源**：canonical（`templates/` `skills/` `shared/`）→ `.specify/` 镜像 → per-tool 生成副本，三层任何一层漏改都会漂移；`diff -rq` 逐对校验 + 生成器（`generate_commands` / `rewrite_paths`）再生是唯一可靠路径。
- **测试基线纪律贯穿所有特性会话**：动手前记录全量基线，收尾对比失败集而非总数；硬编码数量断言（如 5 个官方工具）在扩容时必然断裂。
- **用户↔模型分歧的稳定模式**：用户反复推动"更深的语义层 / 更严格的验证 / 更彻底的移除"，模型默认偏保守迭代；多轮冲突后落地的用户方案（语义布局规划、default-on supervision、四层产物结构）事后都被证明正确。Qoder 轮延续此模式：fork 模型、G5 拒绝伪造、SC 过声称降级、`slow` 标记优于删除。
- **环境故障是客观存在的工作负载**：root 属主目录、`cp -i` alias、沙箱假象在 ≥5 个会话中独立复现；Qoder 轮又加入 `rm`/`mv` 别名静默 no-op、`.git/objects` 桶属主、原子替换（temp+mv）与 `setfacl` 持久修复。
- **多 Agent 闭环有效但有平台期**：draw-plantuml 优化经 4 种编排形态将 49 分提到 91 分；3 代无提升说明策略池穷尽，须换策略族而非加轮数。
- **"机器绿"是本项目的主要风险形态**（Qoder 轮新增）：重命名债让文档与测试一起陈旧而全绿；`or True`、自指断言、空 fixture 制造真空绿；`[x]` 勾选与 registry `Implemented` 可以无证据存在。判据是"测量优先于声明"——green 是待验证的主张，不是证据。
- **并发安全的根答案是"单一所有者 + 派生即读"**（Qoder 轮新增）：记录类数据一文一件，派生索引即读即建，canonical registries 与少数状态文件保留单文件；任何"共享可变聚合"都会成为合并冲突热点。
- **五线程互相咬合**（Qoder 轮新增）：skill/tool 决定 agent 面，goal/team 决定编排，history/archive 决定记忆，review/derive 决定质量，memory/state 决定证据——任一环失守都会以"无证据的绿色"形式出现在下游。
- **机制不可用时的正确动作是阻断**（Qoder 轮新增）：G1 豁免通道未接线、G5 输入契约缺失导致 0/52，正确结果是 BLOCKED 并交出机制决策，而不是补数据、改状态或静默绕过。

## 运行说明

- `.work/` 为一次性提取草稿（已 git-ignore，可随时删除）；`.manifest.json` 记录已蒸馏会话，重跑只处理新增会话并合并进本目录文档。Claude 纪元的 16 条记录保留在 `.manifest.claude-era.json`（manifest 的 `tool` 字段单值，两轮不能共用一份；Qoder 轮更新未删除旧记录）。
- 跳过未蒸馏的 7 个 Claude 会话（138–1452 字符）：三个 `/exit` 空会话（cedfb1d7, 9e462a2a, 04fca7e6）、三个"如何获取历史 session"元提问（8d42ff83, 9cf6968d, 5eba4259）、一个 18 字符空会话（41a4ae60）——无长期价值，故不在 manifest 中登记。
- Qoder 轮（2026-11-10）：125 个会话、108 个蒸馏、17 个琐碎会话按同一启发式跳过（无长期价值的空/元会话）；六批逐会话五维提取位于 `.specify/specs/090-re-anchoring/test-evidence/history-distill-batch-{1..6}.md`。
