# Quickstart: /speckit.docs 演练路径

> 命令示例的语法均由 `contracts/docs-utils-cli.md`（C-1…C-9）钉住；实现阶段（/speckit.implement）MUST 对每条示例真实执行一次回验（合同 C-11）。`/speckit.docs` 是聊天指令，不是终端命令。

## 场景 1：空白项目 bootstrap（US1 / SC-001）

1. 在无 `docs/`、无根入口文件的项目工作区，聊天中运行 `/speckit.docs`。
2. 引擎判定作用域 = bootstrap，生成骨架：
   - 根目录：`README.md`、`ARCHITECTURE.md`、`CONTRIBUTING.md`、`CHANGELOG.md`（全大写，各按注册语义，≤ 一屏）
   - `docs/`：`concepts/ tutorials/ tasks/ reference/ decisions/（含 README + template）contribute/ notes/（含规则 index.md）`
3. 验收：骨架清单逐项存在；`.specify/docs/audit/` 留有审计记录。

## 场景 2：全量调谐 + 防抖（US1 / SC-002）

1. 在已有杂乱文档的项目运行 `/speckit.docs`（无参 = 全量）。
2. 检查输出顺序：观察快照 → 差异（容忍带过滤）→ 干跑计划（移动/归档项可勾选退出）→ 确认 → 收敛 → 残差报告。
3. 立即再次运行：第二次收敛动作应为零，但审计日志仍新增一条"全维度在容忍带内"。

## 场景 3：notes 生命周期（US2 / SC-003）

```bash
# 状态总览（分组：drafts / expireds / archiveds / invalid）
python3 .specify/scripts/python/docs-utils.py --action scan

# 标记超期（draft 且 expires < today → expired；绝不删除文件）
python3 .specify/scripts/python/docs-utils.py --action expire

# 清理（默认 dry-run 只列候选；--yes 才真删，且仅限 notes 区）
python3 .specify/scripts/python/docs-utils.py --action clean
python3 .specify/scripts/python/docs-utils.py --action clean --yes

# 归档完整性（archived 笔记的 target 必须真实存在）
python3 .specify/scripts/python/docs-utils.py --action archive-check

# 统计
python3 .specify/scripts/python/docs-utils.py --action stats
```

三条退场路径演练：合入（改 status=archived + 填 target + 正文标注归宿）、续期（更新 expires、status 回 draft）、确认删除（clean --yes）。

## 场景 4：命名语义校验（SC-006）

```bash
# 确定性维度校验：大写保留名合规 / 一屏阈值 / 链接可达 / ADR 连续性 / frontmatter 完整性
python3 .specify/scripts/python/docs-utils.py --action validate
```

对含 `readme.md`（小写）或滥用大写名的样例项目，`validate` 输出违规清单；重命名建议进入干跑计划。

## 场景 5：文档同步步骤（US3 / SC-007）

1. 运行任一复杂命令（如 `/speckit.plan`）至收尾。
2. 观察 `## Feedback` 同点的 `## Documentation` 步骤：输出"需记录（目标 + 要点）"或"无需记录"，不阻断收尾。
3. "需记录"时按语义路由完成安全写入；涉及移动/归档级动作时提示改跑 `/speckit.docs`。

## 场景 6：Dogfooding（US4 / SC-004）

1. 在 Spec Kit 仓库聊天中运行 `/speckit.docs`（用户指示：激进重组基调）。
2. 干跑计划逐项确认后收敛：`docs/` 向六类 taxonomy 归位、两份设计笔记退场归档、链接/符号链接/镜像/Documentation Map 同步更新。
3. 验收：`find . -type l` 符号链接完好；`python3 scripts/python/regen-command-copies.py --check` 零漂移；内链零悬空。
