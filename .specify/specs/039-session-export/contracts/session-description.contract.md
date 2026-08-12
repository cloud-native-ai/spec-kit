# Contract: session-description(会话描述文档)

**Surface**: 导出目录内 `SESSION.md`(人读)+ `session-meta.json`(机读)
**Implements**: FR-012, FR-013, FR-014
**Authority**: 元信息字段集以 `data-model.md §Entity 2` 为准;本契约规范产出分工与预算纪律。

## 1. 产出分工(两半体)

| 半体 | 产出者 | 约束 |
|------|--------|------|
| 元信息(`session-meta.json` + SESSION.md 元信息节) | 脚本(export.py)确定性提取 | 全部字段来自原始记录,不由模型生成(FR-012) |
| 结构化总结(SESSION.md 总结节) | 执行导出的 agent | 读原始记录后补写;忠实于记录(FR-013/FR-014) |

- 脚本写入 SESSION.md 时 MUST 留下总结占位节(固定 heading),agent 补写时 MUST NOT 改动元信息节。
- `session-meta.json` 为元信息权威;SESSION.md 元信息节与其逐字段一致。

## 2. 元信息字段(STR-003 标识行)

`session-meta.json` 键集:`tool` / `session_id` / `model` / `workspace` / `started_at` / `ended_at` / `snapshot`(bool,运行中会话 true)/ `message_count` / `turn_count` / `exported_at` / `over_summary_budget`(bool)。

- SESSION.md 首节含标识行:`session-export:<tool>/<session-id>`(STR-003)。
- 字段缺失规则:记录中不可得的字段(如模型)置 `null` 并在元信息节标注"记录未含",MUST NOT 猜测填充。

## 3. 结构化总结节

三段固定:**任务脉络**、**关键决策**、**产物清单**。

- 内容边界:仅原始记录可证的事实;MUST NOT 引入记录外新事实来源(FR-014)。
- 运行中会话(`snapshot: true`):总结限定为"截至快照时点"并声明。

## 4. 预算降级(FR-013,clarify 裁决 2026-08-12)

- 双阈值常量:`SUMMARY_LINE_LIMIT = 50000`、`SUMMARY_BYTE_LIMIT = 32 * 1024 * 1024`(以主记录计)。
- 脚本计算并写入 `over_summary_budget`(任一超限即 true),同时 stdout 输出判定供命令面转述。
- 超限 → agent 写**骨架总结**(三段标题 + 各段一句可见范围声明),并显式声明:降级原因、触发的阈值与实际值。
- 未超限 → 全量总结;仍 MUST 忠实于记录。

## 5. Contract / Integration Test Pins

- 夹具驱动:构造已知内容/规模的 jsonl,断言 `session-meta.json` 字段逐值一致(程序提取面 100% 可测)。
- 预算判定:构造超阈值夹具 → `over_summary_budget: true`;未超 → false。
- SESSION.md 结构:标识行、元信息节、总结占位节存在性断言。
- 两形态一致:meta.json 与 SESSION.md 元信息节逐字段对照。
