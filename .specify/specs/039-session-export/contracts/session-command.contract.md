# Contract: session-command(/speckit.session export)

**Surface**: `templates/commands/session.md` + 4 份 per-tool 副本
**Implements**: FR-001, FR-002, FR-003, FR-004, FR-005
**Authority**: 导出机制事实源为 `skills/export-session`(技能契约见 `export-skill-rework.contract.md`);本契约只规范命令面交互与委托。

## 1. CLI Grammar(命令参数面)

```text
/speckit.session export --name <name> [--session <id>] [--tool <name>] [--verify <text>]
```

- `--name` 必填;未提供 → 要求补给,不自动生成(FR-002)。
- `--name` 文法:安全路径段(首字符字母/数字,其余 `[A-Za-z0-9_.-]`);越界即拒。
- `--session` / `--tool` / `--verify` 语义继承 export-session 既有机制(FR-003)。
- 首版仅 `export` 子命令;其他意图 → 报能力清单(仅 export),不猜。

## 2. Preview → Confirm → Execute 门禁(FR-004)

导出前 MUST 披露并经显式确认:

| 披露项 | 内容 |
|--------|------|
| 工具 | 识别/指定的工具(STR-002 规范名) |
| 会话 | session_id + 定位方式(auto / --session / --tool) |
| 目标 | `.session-export/<name>/` 绝对路径 |
| 规模 | 预估(记录行数/字节,可获取时) |

确认后委托 `export-session` 技能执行;命令自身 MUST NOT 重复实现导出逻辑。

## 3. 同名冲突(FR-005)

- 目标目录已存在 → 默认拒绝,preview 门禁内**交互式确认**后方可覆盖。
- 覆盖 = 先清空该目录再写入,不残留旧文件。
- MUST NOT 提供 `--force` 类旁路标志;非交互场景同名重导直接失败并提示换名(clarify 裁决 2026-08-12)。

## 4. 结果回报

- 成功:报导出目录路径 + 描述文档路径(`SESSION.md`)+ 元信息摘要(tool/session_id/model/时间窗)。
- 失败:按技能退出码转述(0/2/3/4/5,见技能契约 §6),不吞错。

## 5. Contract Test Pins

- 命令模板含 export 子命令文法、`--name` 必填纪律、门禁披露四要素、冲突交互确认条款、无 `--force` 旁路断言。
- 4 份 per-tool 副本含上述内容(自既有夹具派生副本集合,不硬编码幻影路径)。
- 委托纪律:命令模板引用 `skills/export-session`,不内联导出实现。
