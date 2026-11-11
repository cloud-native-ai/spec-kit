# Contract — `/speckit.migrate` 运行期模板（薄投影）

**Spec**: `requirements.md` FR-002、FR-021、FR-022 · **Plan**: `plan.md` WP08、WP14 · **Date**: 2026-11-10

## T-1 frontmatter 与形态

`templates/commands/migrate.md` 的 frontmatter 只有两个键（与既有命令模板一致）：

```yaml
---
description: <一句话完整描述：旧版 specify 项目的一次性迁移收尾——只读探测、逐项计划、归档式自动收敛>
short-description: <短标签供 Qoder 副本生成 description>
---
```

正文 MUST 以 `## User Input`（`$ARGUMENTS`）、`## Glossary` 指针、`## Delegation`、`## Handoffs` 构成，风格与既有命令模板一致。

## T-2 薄投影（核心约束）

模板是本特性唯一的**非确定性**载体，但 MUST NOT 承载任何检查或处置实现：

1. 探测与计划 MUST 只经 `specify migrate`（默认干跑；机器可读时 `--format json`）获得。
2. 处置 MUST 只经 `specify migrate --apply` 执行；干跑之后自动运行，不等待对话确认（`--apply` 是唯一写入授权，archive-first 回执是可恢复性契约）。
3. 模板 MUST NOT 内联任何维度的检查逻辑、残留清单、路径改写规则或处置判断；MUST NOT 自带第二份「计划」。
4. 模板 MUST NOT 传递任何确认类旗标（命令面不存在该旗标，见 `contracts/migrate-cli.md` C-5）。
5. 模板 MUST 把命令的结局词与退出码原样转述给用户：`clean` / `planned` / `applied` / `blocked`；`blocked` 时 MUST 说明哪些项未执行与原因（结构性冲突、无归档路径或执行失败），MUST NOT 宣称成功。

**结构测试断言**（WP14）：
- `templates/commands/migrate.md` 含字面量 `specify migrate` 与 `specify migrate --apply`；
- 不含 `check_`、`sanitize-utils`、`anchor-layout-migrate`、`sync-mirrors`、`regen-command-copies`、`_OBSOLETE_` 等实现级符号（只允许经 `--help`/计划输出间接引用）；
- 不含 Python/bash 代码围栏中的检查实现。

## T-3 等价性（FR-002）

测试从模板中提取所声明的命令（`specify migrate [--format json]`），在夹具上执行，与直接执行 CLI 的输出比较：
- `items` 与 `summary` 逐项相同（确定性部分，见 `contracts/migrate-cli.md` C-4）；
- apply 时回执 `outcome` 与 `items[].disposition/status` 相同；
- 两入口都不产生额外文件。

## T-4 装配面（FR-021、SC-009）

| 面 | 路径 | 检查 |
|----|------|------|
| 源模板 | `templates/commands/migrate.md` | 存在；frontmatter 契约通过 |
| 四份再生副本 | `.github/prompts/speckit.migrate.prompt.md`、`.claude/commands/speckit.migrate.md`、`.qoder/commands/speckit.migrate.md`、`.opencode/command/speckit.migrate.md` | 均由 `regen-command-copies.py` 生成（含 `AUTO-GENERATED` 标记并指向源模板）；`--check` 退出 0 |
| Qoder frontmatter | `.qoder/commands/speckit.migrate.md` | `description` 来自 `short-description`（既有 `test_qoder_command_frontmatter.py` 覆盖） |
| 命令文档 | `docs/reference/commands/migrate.md` | 存在；含执行流、选项、结局/退出码、回执与归档落点、与 init/sanitize 的边界 |
| 冻结基线 | `tests/contract/test_migration_distribution.py` | `COMMAND_BASELINE` 加 `migrate`，长度 29 → 30 |
| 退役面 | `.specify/templates/commands/` | MUST NOT 出现 `migrate.md`（该镜像面已退役） |

## T-5 代理会话中的自动执行与披露

- 模板 MUST 在干跑后自动调用 `--apply`；不要求对话同意，也不存在第二把钥匙或确认旗标。
- 模板 MUST 在收尾披露：哪些 anchor 被合并（占位替换或真实内容合并）、两个原件的归档位置、回执 `recover` 路径，并建议用对应 owner 命令复核合并结果。
- 模板 MUST NOT 编造「已确认」「已人工审阅」状态；合并与归档是自动执行的事实，按回执如实转述。

## T-6 回执指向

apply 后模板 MUST 报告回执路径（`.specify/memory/migrate/receipts/<run-id>.json`）与归档根（`.specify/archive/migrate/<run-id>/`），并说明恢复途径以回执 `recover` 字段为准。
