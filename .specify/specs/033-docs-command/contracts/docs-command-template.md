# Contract: `/speckit.docs` 命令模板结构（templates/commands/docs.md）

本契约约束新增命令模板的结构与分发。全部条款为规范性声明；由契约测试钉住。

- **C-1** 源模板 MUST 位于 `templates/commands/docs.md`，并在 `.specify/templates/commands/docs.md` 存在字节一致镜像（`regen-command-copies.py --check` 零漂移）。
- **C-2** frontmatter MUST 含 `description`（一行）与 `handoffs`；引用共享文档 MUST 使用根相对形式（`shared/workflow/...`、`shared/patterns/reconcile-pattern.md`），由再生成器重写为 `.specify/shared/...`（test_shared_reference_rewrite 约定）。
- **C-3** 模板 body MUST 含以下章节（顺序固定）：`## User Input`（含 `$ARGUMENTS` 与 User Input Protocol 引用）、`## Glossary`、`## Outline`、`## Reconcile Loop`（或 Outline 内等价小节）、`## Feedback`、`## Documentation`、`## Handoffs`。
- **C-4** `## Outline` MUST 含作用域判定表（无参全量 / 单目标 / 原始材料扇出 / bootstrap 四行，FR-003）与分级确认门禁表（安全写入自动 / 移动归档须计划确认，FR-004）。
- **C-5** 模板 MUST 声明四件强制产物及其落点：观察快照（内联）、干跑计划（`.specify/docs/plans/`）、审计日志（`.specify/docs/audit/`，零收敛也落盘）、残差报告（内联）。
- **C-6** 模板 MUST 声明归档区为 `docs/archive/`，且正式区动作词汇中不出现"删除"（notes 区确认删除除外，须引用 FR-006c 语义）。
- **C-7** 模板 MUST 保持薄调度层：引擎细节引用 `shared/patterns/reconcile-pattern.md` 与 `docs/commands/docs.md`，不内联重复完整 R0–R6 规程（reconcile-pattern §Applying-6）。
- **C-8** `## Feedback` 节 MUST 符合 `shared/workflow/feedback-step.md` 约定（unit-id `/speckit.docs`、unit-type command）；`docs` MUST 加入 `tests/contract/test_feedback_command_classification.py` 的 `COMPLEX_COMMANDS` 清单，计数 13→14，SIMPLE 保持 4。
- **C-9** 期望态基线内容 MUST 与 requirements.md FR-002/FR-010 一致：六类目录 + notes；特殊名注册表四条种子（README/ARCHITECTURE/CONTRIBUTING/CHANGELOG 及各自语义）。
- **C-10** 运行时副本 MUST 覆盖仓库中已存在的全部工具命令目录（.claude/.github/.qoder/.qwen/.opencode/.codex/.hermes/.iflow 等），由 `regen-command-copies.py` 生成，禁止手改。
- **C-11** 命令参考文档 MUST 新增 `docs/reference/commands/docs.md`（结构对齐既有命令参考文档；dogfooding 重组前路径为 `docs/commands/docs.md`），并在 `docs/tutorials/quickstart.md` 命令表加行。
