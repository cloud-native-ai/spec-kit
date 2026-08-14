# Contract: /speckit.feedback Command(三模式行为)

**Requirement**: `041-refactor-feedback-probe` | **Consumes**: FR-008~FR-010, FR-019, SC-007 | **Pinned by**: `tests/contract/test_feedback_command_template.py`

## C-1 模板与分发

- C-1.1 canonical 模板:`templates/commands/feedback.md`,含 AUTO-GENERATED 兼容头之外的常规命令结构;归类为**复杂命令**(调用引擎脚本)。
- C-1.2 模板 MUST 含 `## Feedback` 步(canonical 块,`--unit-id /speckit.feedback`)与 `## Documentation` 步(docs-step 注入,沿 037 先例)。
- C-1.3 镜像:`.specify/templates/commands/feedback.md` + 仓库现存工具副本面(实测 4:`.claude/commands/speckit.feedback.md`、`.github/prompts/speckit.feedback.prompt.md`、`.qoder/commands/speckit.feedback.md`、`.opencode/command/speckit.feedback.md`;副本清单以 `regen-command-copies.py` 的现存目录探测为准动态派生),经 `sync-mirrors.py --write` 一次落齐,`--check` exit 0;codex/hermes 副本不在本仓生成,由 `specify init` 在下游项目分发。
- C-1.4 `docs/reference/skills/feedback.md` 的命令分类表 MUST 同步:复杂命令清单 +1(feedback),总数 18→19(以实施时实测为准)。

## C-2 模式一(无参数缺省):probe 总览

- C-2.1 无参数调用时,命令 MUST 以 probe 总览为缺省行为:调用 `--action probes` 渲染**图形列表或竖状(树状)结构**——按 Class 分组、组内列 Object,标注内外类别与目标切片。
- C-2.2 总览 MUST 渲染自合并真源(框架 + 项目外部),覆盖度与真源一致;MUST NOT 维护独立清单。
- C-2.3 呈现 MUST 含每个 Object 的:插入位置(unit × lifecycle_point)、收集内容(继承 Class)、处理流程(继承 Class)——即三问的可读投影。
- C-2.4 空态(项目无外部 probe):仅呈现全部内部 Object(交付时 50,含 feedback 命令自身),不报错。

## C-3 模式二:处理已收集反馈

- C-3.1 命令 MUST 引导完成:摘要视图(`list` + `--slice/--kind/--unit-id/--disposition` 过滤)→ 状态视图(`status`)→ 处置(标记 `disposition`、打包 `package`、**打包后的清理 `cleanup`**、阈值/静默调整)。
- C-3.2 打包后清理:仅当用户确认批次已处置(发送或放弃)后执行 `cleanup --package <zip|latest>`;清理范围限定该包实际收录条目(engine-cli C-5)。
- C-3.3 全部动作零网络;`mark-submitted` 语义(archive-then-reset)保留,`cleanup` 是其后的可选收敛步。

## C-4 模式三:注入外部 probe

- C-4.1 命令 MUST 引导声明:目标自定义单元(`custom:<owner>/<name>`)、生命周期点(缺省 wrap-up)、收集意图描述;随后调用 `--action probe-inject` 落文件。
- C-4.2 注入结果 MUST 即刻反映在模式一总览与 `--action map` 重建中。
- C-4.3 注入 MUST 校验 registry C-4 契约(`ext-` 前缀、external 类归属);失败逐条回报,不半写。

## C-5 红线分级(命令侧呈现)

- C-5.1 命令文档段 MUST 声明:内部 probe 反馈面向 Spec Kit 框架上送路径;外部 probe 反馈仅留宿主项目,永不进入上送包。
- C-5.2 独立模式(无 `.specify/`):命令整体不适用(命令仅在 Spec Kit 项目内运行),无需 runtime-mode gate;引擎调用前置探测工作区。

## C-6 用户文档

- C-6.1 `docs/reference/commands/feedback.md` 新增:三模式用法、示例(与 quickstart.md 一致,由契约测试钉住)、退出码表。
