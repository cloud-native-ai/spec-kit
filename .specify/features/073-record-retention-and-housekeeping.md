# Feature Detail: 记录消费回收与 SDD 项目管家（Record Retention & SDD House-Keeping）

**Feature ID**: 073
**Name**: 记录消费回收与 SDD 项目管家（Record Retention & SDD House-Keeping）
**Description**: 为 exec-quant / feedback / session 三套按 run 累积的原始记录建立「消费 → 回执 → 回收」生命周期，挂在 `/speckit.sanitize --lane retention`；并新增外部技能 `sdd-house-keeping`，把 `sdd-project-setup` 中反复执行的维护步骤抽出，作为周期性维护入口调用目标项目的 sanitize retention lane。
**Status**: Implemented
**Created**: 2026-10-27
**Last Updated**: 2026-10-27 (boundary hardening: setup = S0–S2 + HANDOFF; house-keeping = H1 gaps OR owner drift; shared target-resolution; loop-driver three-skill handoff; target dependency classes — setup has no `.specify/` dependency, house-keeping/loop-driver upward-search the nearest valid `.specify/` root and refuse/handoff when absent; 18 pre-existing failures unchanged)

## Overview

三套记录都是 append-only 的 per-run 证据，但既有引擎只走到「标记/打包」：框架仓走 feedback Path A 不打包，条目被标记后永久保留；session 的 `prune` 直接删除、没有蒸馏门；exec-quant 只有入站聚合、本地记录无回收（059/068 明确留待后续）。本特性补的是可审计的消费链路：先写持久载体与 per-entry 回执，再凭回执和 30 天宽限删除原始记录；没有回执不删除。

同时把 `sdd-project-setup` 的周期性维护步骤（S1 盘点、S3 调协、S3+ 强化、S4 验证、S5 报告）抽到新的外部技能 `sdd-house-keeping`（H0–H5），setup 只保留 bootstrap 与 handoff。新技能在 `cleanup` 模式下调用目标项目的 `/speckit.sanitize --lane retention`，不直接调用 apply、不新增第二道确认门。

## Key Changes

1. **`record-retention.py`**：独立协调引擎，动作 `scan / distill / plan / apply / status / args-manifest`；通过 importlib 复用 exec-quant / feedback / memory / run-determination 的 schema 解析，不复制字段规则。
2. **新存储 `.specify/memory/retention/`**：`summaries/<store>/`（月度计数/投影，append-only）、`receipts/`（每消费一条一张）、`plans/`（`confirmed: false`）、`ledger/`（每批回收审计 + 计数守恒）。
3. **回收门槛**：exec-quant 可解析 + 被摘要覆盖；feedback processed/ignored + 载体；run-determination settled + 被摘要覆盖；session 笔记有 promotion/ephemeral 回执；统一 30 天宽限；open/unsettled/unreadable/unclassified 永不回收。
4. **apply 安全门**：`confirmed: true`、回执复核、宽限复核、git 干净（非 git 需 `--allow-unversioned`）、计数守恒 `remaining + retired = original`、失败不回滚并如实报告。
5. **sanitize retention lane**：`--lane materials|retention|all`；materials 七阶段与确认门不变；retention lane R1–R5 使用独立计划/回执/ledger，不写 findings 台账。
6. **`sdd-house-keeping` 外部技能**：H0 入口 → H1 双盘点 → H2 调协（含 sanitize retention）→ H3 强化 → H4 验证 → H5 报告；自带只读盘点脚本；setup 保留 bootstrap 并 handoff，loop-driver 仍负责 SDD 阶段。
7. **注册与派生面**：probe 对象、flow-class 台账、docs 页、external roster、frozen inventory、mirrors 同批更新。

## Implementation Notes

- 当前 staged 的原始记录必须先提交，首次 apply 才能通过 git-clean 门；删除后由 git 历史兜底。
- `exec-quant/scores/` 暂不回收（体量小、可与记录 join）；`scores.jsonl` 是 legacy 只读回退。
- `sdd-house-keeping` 的盘点脚本与 setup 的副本保持字节一致（provenance 三行除外），保证外部技能独立可运行。
- 不新增调度器；周期由用户或宿主循环触发。`check` 是默认模式，`cleanup` 必须显式请求。
- 已知 pre-existing 债务：`test_shared_reference_rewrite` 对 create-docs/humanize/memory-recall/memory-record 的裸 `shared/` 引用报红，与本次改动无关。
