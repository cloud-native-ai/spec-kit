# Feature Reference: 065a-state-awareness

**Bound Feature**: **Feature 065** — SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery）
**Slice**: `065a-state-awareness`（Feature 065 的第一个切片）
**Requirements**: [`requirements.md`](./requirements.md) · **Plan**: [`plan.md`](./plan.md)
**Feature Registry**: `.specify/memory/features.md`（ID 065）· **Feature Detail**: `.specify/memory/features/065.md`

## 1. 绑定关系

- 本切片 MUST 复用 Feature 065，MUST NOT 新建 Feature ID 或注册行（`requirements.md` A-15）。
- Feature 065 的权威需求仍是父规格 `.specify/specs/065-loop-interruption-recovery/requirements.md`；本切片是其在分解门下的第一个执行单元，保留父 FR 编号空间（SA-2）。
- 本 plan 只把 Feature 065 的注册状态从 `Draft` 推进到 `Planned`，并更新详情文件的 Latest Review / Related Specifications；MUST NOT 推进到 `Implemented`。

## 2. 本切片在 Feature 065 中的位置

| 切片 | 主题 | 本 plan 的关系 |
|------|------|----------------|
| `065a-state-awareness`（本切片） | US1 + 快照引擎 | 实现只读 `snapshot`、六类形态基础检测、`--probe`、信封与退出码、`--self-test` |
| `065b-interruption-lifecycle` | US2 + US4 + `check-spine` | 追加 `heartbeat-stalled`、`lifecycle-spine-violation`、六类形态的权威细化谓词、脊写侧与校验器 |
| `065c-recovery` | US3 + `recover` | 追加 `resume/retry/stop` 执行、salvage 记录、旧信号隔离、并发锁与上送件 |

本 plan 为下游切片保留的扩展点：

- CLI 动作面已含 `recover` / `check-spine` 的拒绝分支（`LS-02`），下游只需替换实现，不改参数面。
- 八类中断词表与字段已冻结（`IA-01`），065b 只需追加检测器。
- 动作建议的封闭集与优先级已冻结（`IA-13`–`IA-17`），065c 只需执行建议。
- 状态脊机读段的读取键已定义（`data-model.md` §3.2），写侧由 065b/065c 实现。

## 3. 本切片覆盖的父 FR

| 区域 | 父编号 | 本 plan 落点 |
|------|--------|--------------|
| A 核心 | FR-001–FR-012 | `plan.md` §Summary/Technical Context；`contracts/loop-state-cli.md`、`snapshot-envelope.md`、`interruption-and-action.md`、`stage-artifact-map.md` |
| D 边界 | FR-038–FR-044、FR-046、FR-047 | 兼容（不触碰 watcher/Registry/命令）；双帽子与镜像；单一 owner reference；变异演练 |
| E 边界 | FR-049–FR-052 | 只读、不 kill/删除/push；不替代 058/064 |

显式 out-of-slice：父编号 045（跨切片测试矩阵，065c 汇总）与 048（记录拓扑 + recover 锁，065c 承接）。

跨切片落点注记：FR-010 的驱动者写入侧归 065b（本切片只交付读取契约与消费）；FR-044 的恢复动作与 watchbeat 写侧章节由 065b/065c 补齐；FR-012/FR-046 的自测与变异演练按切片累计。详见 `plan.md` §Slice Landing Notes。

## 4. 与相邻特性/工具的边界

- **Feature 058**：U0–U6、状态脊文件语义、哨兵、U4/U5、watcher 判定与其退出码保持 owner；本切片只读消费，不改 `watch-model.md` 或 `watch-target.sh`。
- **Feature 063**：plan-owned 集合（`efficiency-model.md` §3.1）与阶段基线提交被引用；fast lane/测试预算/只小修规则不改。
- **Feature 064**：Registry/lease/reservation/ownership 语义不变；本切片只读 Registry 条目。
- **feedback/probe**：不新增记录引擎；如后续需要记录，走既有 `feedback-utils.py` / probe 注册表。

## 5. 分发与文档面

| 资产 | 源（改动落点） | 镜像/发布 |
|------|----------------|-----------|
| 引擎 | `skills/external/sdd-loop-driver/scripts/loop-state.py` | `.specify/skills/sdd-loop-driver/scripts/loop-state.py`（`sync-mirrors.py`） |
| Owner reference | `skills/external/sdd-loop-driver/references/state-awareness.md` | `.specify/skills/sdd-loop-driver/references/state-awareness.md` |
| 技能入口 | `skills/external/sdd-loop-driver/SKILL.md` | `.specify/skills/sdd-loop-driver/SKILL.md` |
| 文档入口 | `docs/reference/skills/sdd-loop-driver.md` | 直接发布，无镜像 |
| 测试 | `tests/unit/test_loop_state_engine.py`、`tests/contract/test_loop_state_contract.py`、`tests/contract/test_sdd_loop_driver_skill.py` | 仓库内，无镜像 |

## 6. 注册表变更（本阶段唯一允许的注册表改动）

- `.specify/memory/features.md`：Feature 065 行 `Status: Draft → Planned`；`Last Updated` 追加本切片 plan 的事实与产物指针。
- `.specify/memory/features/065.md`：`Status: Planned`；`Last Updated`；Latest Review 追加 065a plan 摘要；Related Specifications 增加切片规格与 plan 指针。
- `Total Features` 不变（本次不新增 Feature 行）。

**披露**：切片 `requirements.md` §Related Feature 写有“MUST NOT 改写注册状态或索引行”；本阶段指令与 `/speckit.plan` 的 Feature Integration 要求把绑定特性推进到 `Planned`。本阶段执行后者并在此显式记录差异；不新建 Feature ID、不新增注册行（另见 `plan.md` §Disclosed Deviations）。
