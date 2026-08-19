# Contract: Gate Scanner(门控扫描脚本)

**交付物**: `scripts/python/scan-confirmation-gates.py`(stdlib-only,Python >= 3.8)
**溯源**: FR-003(回流约束执行面)、SC-002、SC-005;data-model.md Entity 1 / Entity 4;Token Efficiency 纪律 Program-First

## C-1 命令形态

```text
python3 scripts/python/scan-confirmation-gates.py [--baseline <baseline.json>] [--root <repo-root>] [--json | --summary]
```

- 默认输出人类可读汇总(`--summary`),`--json` 输出机器可读全量。
- `--root` 缺省为脚本所在仓根。
- 退出码:0 = 扫描完成(无论检出多少);1 = 参数/环境错误;2 = 提供 `--baseline` 且存在 verdict=auto_execute 仍以阻塞形态存在的门控(回流违例)。

## C-2 扫描根

MUST 且仅扫描:`templates/commands/`、`templates/*.md`、`skills/`、`shared/`。MUST NOT 扫描镜像副本(`.specify/`、`.claude/`、`.qoder/`、`.github/prompts/`、`.opencode/`)以避免重复计数;生成副本的一致性由 regen-command-copies/sync-mirrors 的 `--check` 独立保证。

## C-3 检出语义

以阻塞确认语义模式匹配(示例模式族,非穷举):"等待用户确认"、"before … confirm"、"MUST NOT execute before confirmation"、"Proceed … yes/no"、"stop and confirm"、"after user confirmation"。每条检出 MUST 输出 data-model.md Entity 1 全字段;`action_class` 与 `verdict` 由判据文档的清单(破坏性清单 + 治理保留清单)确定性判定,判据无法命中时 MUST 落 `destructive`(存疑从严)。

## C-4 输出 schema

`--json` 输出顶层键 MUST 为:`total`、`gates`(Entity 1 数组)、`by_class`、`by_verdict`、`baseline_delta`(无基线为 null)、`violations`。字段语义与 data-model.md Entity 4 一致。

## C-5 基线对比

`--baseline` 指向治理前基线 JSON(由本规格实现期首扫生成并存档)。`baseline_delta` MUST 给出 total 差值与 by_class 差值。SC-002 的度量口径 = 基线 total 与治理后 total 之比,残留口径 = `violations` 为空且 by_class 中非 `reversible` 项全部在判据清单内。

## C-6 镜像

脚本 MUST 有 `.specify/scripts/python/` 镜像(sync-mirrors.py 管理);镜像副本运行时 MUST 正确解析仓根(参照 regen-command-copies.py 的 `.specify` 双重路径守卫)。

## C-7 契约测试

`tests/contract/test_scan_confirmation_gates.py` MUST 覆盖:输出 schema 键完整、扫描根排除镜像、判据清单确定性归类、存疑落 destructive、基线对比 delta 计算、退出码 2 的回流违例触发。
