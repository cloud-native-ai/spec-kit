# Contract: 文档同步步骤注入（shared/workflow/docs-step.md + 核心命令模板）

约束 FR-011 的落地形态。

- **C-1** 单一事实源 MUST 为 `shared/workflow/docs-step.md`，镜像 `.specify/shared/workflow/docs-step.md` 字节一致；各命令模板 MUST 仅引用该文档，MUST NOT 内联复制其规则正文。
- **C-2** 注入范围 MUST 为 COMPLEX_COMMANDS 全集（既有 13 个 + docs = 14 个）；SIMPLE_COMMANDS（4 个）不注入。范围清单以 `tests/contract/test_feedback_command_classification.py` 为准。
- **C-3** 注入形态 MUST 为 `## Documentation` 章节，位置紧邻 `## Feedback`（同一收尾生命周期点），置于 `## Handoffs` 之前。
- **C-4** 步骤语义 MUST 与 docs-step.md 一致：评估本次运行产生的信息是否需要记录/更新到项目文档空间；结论二选一——`需记录（目标文档 + 要点）` / `无需记录`；结论 MUST NOT 阻断命令收尾。
- **C-5** "需记录"时的写入 MUST 遵循 /speckit.docs 期望态基线与安全写入门禁：语义路由到目标文档；只做安全本地写入（追加/更新，不覆写同名内容）；触及移动/归档级动作时 MUST 降级为"建议运行 /speckit.docs"而非直接执行。
- **C-6** 步骤 MUST 为增量评估：仅判断本次运行触及的信息，MUST NOT 触发全量 R0–R6 调谐；无文档影响时以"无需记录"一行收尾。
- **C-7** 注入 MUST NOT 修改 feedback 引擎、feedback 存储或其动作集（零新增循环机器）；docs-step 不引入新的持久化存储（评估结论体现在会话输出与被更新的文档本身）。
- **C-8** 全部被注入模板的镜像义务 MUST 满足：`.specify/templates/commands/` 镜像 + 各工具运行时副本经 `regen-command-copies.py` 再生成，`--check` 零漂移。
- **C-9** 契约测试 MUST 静态扫描：14 个复杂命令模板均含 `## Documentation` 节且含对 docs-step.md 的引用（源模板根相对 `shared/workflow/docs-step.md`）；4 个简单命令模板均不含。
