# Parent FR Mapping — Feature 065 / Slice 066

**Date**: 2026-10-21  
**Parent spec**: `.specify/specs/065-loop-interruption-recovery/requirements.md`  
**Slice spec**: `.specify/specs/066-loop-state-awareness-a/requirements.md`  
**Purpose**: 记录切片局部 FR 与父 FR 的精确对应关系。父引用统一写 `#FR-NNN`；本文件是 dated record，不参与 `pre-analyze-check.py` 的形式化 ID 解析（该检查只扫描 requirements/plan/tasks/data-model/quickstart/research/feature-ref/contracts/checklists）。

## Scope Allocation

| 范围 | 父条目 | 切片映射 |
|------|--------|----------|
| 核心 A 区（状态感知） | `#FR-001`…`#FR-012` | FR-001…FR-012 |
| 边界 D 区（兼容、分发、测试） | `#FR-038`、`#FR-039`、`#FR-040`、`#FR-041`、`#FR-042`、`#FR-043`、`#FR-044`、`#FR-046`、`#FR-047` | FR-013…FR-021 |
| 边界 E 区（非目标） | `#FR-049`、`#FR-050`、`#FR-051`、`#FR-052` | FR-022…FR-025 |
| 核心 B 区（中断检测与生命周期） | `#FR-013`…`#FR-024` | 不在本切片；后续切片承接 |
| 核心 C 区（状态恢复执行） | `#FR-025`…`#FR-037` | 不在本切片；后续切片承接 |
| 边界 D 区第 8 条（跨切片测试矩阵） | `#FR-045` | Out-of-slice；后续末切片汇总 |
| 边界 D 区第 11 条（记录拓扑 + recover 锁） | `#FR-048` | Out-of-slice；恢复执行切片承接 |

切片 FR 定义总数 = 25（核心 12 + 边界 13），低于拆分门上限 30。

## Exact Mapping

| 切片 FR | 父 FR | 切片处理 |
|---------|-------|----------|
| FR-001 | `#FR-001` | 沿用；A 实现 `snapshot` 与 `--self-test` 快照部分 |
| FR-002 | `#FR-002` | 沿用并细化：Registry 对象、载体归属唯一规则、Registry/状态脊缺失路径 |
| FR-003 | `#FR-003` | 沿用并细化：新增 `completion`、`registry`、`salvage`、`recovery_reason`；动作建议为只读投影 |
| FR-004 | `#FR-004` | 沿用并细化：ANOMALY 谓词、形态不覆盖、stalled/retrying 的 `last_verdict` 放宽 |
| FR-005 | `#FR-005` | 沿用；probe 快照作为 watcher 判定来源 |
| FR-006 | `#FR-006` | 沿用；A 只消费产物映射 |
| FR-007 | `#FR-007` | 沿用并细化：`completion` 求值，伪完成与 `loop_state` 分离 |
| FR-008 | `#FR-008` | 沿用；`stage_base_commit` 缺失记 `unknown`，写入义务移交后续切片 |
| FR-009 | `#FR-009` | 沿用并细化：`dead-no-exit-record` 要求无哨兵；形态只注释；活 TIMEOUT 只建议 `watch` |
| FR-010 | `#FR-010` | 沿用；A 只读消费 watchbeat，归属与新鲜度规则见切片 FR-002/FR-010 |
| FR-011 | `#FR-011` | 沿用；正常窗口不误报 |
| FR-012 | `#FR-012` | 沿用；A 的 `--self-test` 覆盖快照适用项，并发锁/拒绝路径由后续切片追加 |
| FR-013 | `#FR-038` | 沿用并细化：新增 watcher SHA-256 锚点 |
| FR-014 | `#FR-039` | 沿用；A 只读 Registry |
| FR-015 | `#FR-040` | 沿用 |
| FR-016 | `#FR-041` | 沿用 |
| FR-017 | `#FR-042` | 沿用；spec 目录不是运行时镜像 |
| FR-018 | `#FR-043` | 沿用；A 的 owner 文档定义状态感知/快照/watchbeat 读取 |
| FR-019 | `#FR-044` | 沿用；A 只更新状态感知相关文档，不声称恢复动作已实现 |
| FR-020 | `#FR-046` | 沿用；A 执行三项变异并覆盖 salvage 只读裁决面 |
| FR-021 | `#FR-047` | 沿用 |
| FR-022 | `#FR-049` | 沿用；A 不产生提交 |
| FR-023 | `#FR-050` | 沿用；A 不执行清理/隔离 |
| FR-024 | `#FR-051` | 沿用；A 输出 `completion=incomplete`，不声称完成 |
| FR-025 | `#FR-052` | 沿用 |

## Out-of-Slice

| 父 FR | 归属 | 理由 |
|-------|------|------|
| `#FR-045` | 后续切片（末切片汇总） | retry/stop/隔离/四要素上送件依赖恢复执行切片；A 只覆盖自身新增检查与逆样本。 |
| `#FR-048` | 后续切片（恢复执行） | A 的快照只读求值，不写状态脊、不持有 `recover --apply` 锁、不产生并发写。 |

## Conflict Note

`pre-analyze-check.py` 的 `dangling-id` 扫描不区分父规格命名空间；若正式 `requirements.md` 直接出现父 FR 编号，会被判为悬空 ID。因此正式文件改用「父 A/D/E 区第 N 条」的章节序号，本文件承载精确 `#FR-NNN` 映射。两份文件合起来满足「父引用写 `#FR-NNN`」与「形式化 ID 可解析」两项约束；父规格仍是语义权威。
