# Quickstart: 072-client-self-improvement

**Requirement → Feature**: `072-client-self-improvement` → Feature 072 客户项目的持续反馈与自我提升

场景 S1–S2 在本仓实跑（输出照抄于 2026-10-27）；S3–S8 依赖的采集/度量行为**本阶段尚未实现**，每条带逐例豁免：前提清单 + 由哪份契约测试钉住（Post-Generation Quality Gate 路线 b）。所有引擎路径以本仓 `.specify/scripts/python/` 为准。

## S1 盘点帽子判定的输入（本仓实跑）

```bash
python3 .specify/scripts/python/probe-utils.py --action probes --format json
```

实测输出摘要（2026-10-27，框架仓）：`available: True`，`external objects: 0`，`classes: 10`。
读法：本仓是框架项目（根级拥有五框架源目录），外部探针对象为零——客户通道处于未武装的输入状态。命令行与输出均被 `tests/contract/test_feedback_probe_cli.py` 等既有套件钉住。

## S2 按外部身份过滤客户条目（本仓实跑）

```bash
python3 .specify/scripts/python/feedback-utils.py --action list --kind external --format json
```

实测输出（2026-10-27，框架仓）：

```json
{
  "count": 0,
  "matches": []
}
```

读法：清单命令的 JSON 形状（`count` + `matches[]`）是 SC-001"按运行标识过滤"的复算面；此命令只读，可在任何项目随时重跑。

## S3 在模拟客户项目里武装客户通道（未实现 — 逐例豁免）

```bash
# 在模拟客户项目根（无 templates/skills/shared/scripts/src/specify_cli 五目录）执行：
python3 .specify/scripts/python/probe-utils.py --action probe-inject \
  --unit custom:myteam/review-loop --workspace-root <fixture-root>
```

**前提清单**：`probe-inject` 动作名与 `--unit` 参数形态以 `probe-utils.py:1355–1381` 实码为准；外部探针文件落 `<fixture-root>/.specify/memory/feedback/probes/`；fixture 需具备 `.specify/shared/definitions/probe-definitions.md`。
**钉住它的测试**：`tests/contract/test_client_armed_state.py`（计划，红先行记录见 SC-006）；注入动作的既有行为由 `tests/contract/test_feedback_probe_registry.py` 钉住。

## S4 一次评审运行自动采集一条指针条目（未实现 — 逐例豁免）

```bash
# 非交互路径第五步（自动发生，无需人工调用）；手工复算：
git-delta-review.sh report --summary --format json --file .specify/specs/<key>/code-review.md
python3 .specify/scripts/python/feedback-utils.py --action list --kind external --format json
```

**前提清单**：`capture` 子命令与 `report --summary --format json` 尚不存在，形态以 `contracts/capture-step.md` C-11/C-17 为准；运行标识 = 记录头日期戳（C-18）；幂等键 `(unit, run)` 为引擎既有行为（`feedback-utils.py` 783–793 行）。
**钉住它的测试**：`tests/contract/test_client_capture.py`（计划；SC-001 的逐项计数相等断言在其中）。

## S5 三种"没采集"的具名披露（未实现 — 逐例豁免）

三种情形各跑一次非交互路径，结论行分别为：

```text
client-capture: client-channel-unarmed …（零外部探针对象 / 显式单元无探针对象 / 注册表不可用）
client-capture: client-unit-ambiguous …（两个以上外部探针对象且无 --client-unit）
client-capture: no-capture-object …（适用性非 run）
```

显式指定的跑法：`/speckit.review --client-unit custom:myteam/review-loop`。
**前提清单**：五值闭集与行形态以 `contracts/capture-step.md` C-22 为准；`--client-unit` 字面量以 C-6 为准；披露与适用性取值同时可见以 C-22 为准。
**钉住它的测试**：`tests/contract/test_client_armed_state.py`（计划；SC-002 只需检查退出码与具名披露）。

## S6 消化：载体指派与打包排除（部分实跑）

打包排除的引擎行为**今天已存在**并可实跑（本仓内无外部条目，排除计数为 0）：

```bash
python3 .specify/scripts/python/feedback-utils.py --action package --format json
```

**逐例豁免**：该命令会写打包产物，故此处不实际执行；排除语义（无条件排除 `kind: external`，只报 `excluded_external` 计数）由实码 `feedback-utils.py:1871–1892` 与 `tests/contract/test_client_package_exclusion.py`（计划）钉住。
载体指派（Park / 新规格 / 改进循环，恰好一个）未实现，形态以 `contracts/digest-and-carriers.md` C-26 为准，由 `test_client_package_exclusion.py` 钉住。

## S7 四条循环度量（未实现 — 逐例豁免）

```bash
python3 .specify/scripts/python/feedback-utils.py --action client-metrics \
  --unit custom:myteam/review-loop --format json
```

**前提清单**：`client-metrics` 动作尚不存在；四指标口径与分子/分母定义以 `contracts/cadence-and-metrics.md` C-43…C-50 与 `data-model.md` E9 为准；`not-evaluated` 字面量 = STR-006。
**钉住它的测试**：`tests/contract/test_client_metrics.py`（计划；SC-005 的两次呈报同读数、存储树无新增文件断言在其中）。

## S8 客户主体的改进循环（未实现 — 逐例豁免）

```bash
/speckit.improve custom:myteam/review-loop
```

**前提清单**：命令模板已承认 `custom:` 目标按解析后实体路由（`templates/commands/improve.md`）；why 段的"运行判定历史未评估"披露与换观察源规则以 `contracts/client-improvement-loop.md` C-34/C-35 为准；引擎对 `custom:` 的 fail-closed 行为已由 `tests/contract/test_run_determination_engine.py:1393` 既有钉住（本特性不重复实现）。
**钉住它的测试**：`tests/contract/test_client_improve_loop.py`（计划；SC-004 的三段产物、台账位置与工作树零变更断言在其中）。
