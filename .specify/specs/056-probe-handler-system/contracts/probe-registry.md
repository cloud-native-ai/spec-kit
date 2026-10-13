# Contract: 共享引擎 probe-utils.py（STR-002）CLI 面

**Spec**: `.specify/specs/056-probe-handler-system/requirements.md` | **Date**: 2026-10-13
**Engine file**: `scripts/python/probe-utils.py`（NEW；镜像 `.specify/scripts/python/probe-utils.py`，scripts 严格对）

## 定位

stdlib-only 共享引擎（依赖面与 feedback-utils.py 同分布）。承载自 feedback-utils.py 抽出的 probe 族动作（行为不变）与新动作；feedback 域动作留在 feedback-utils.py（封闭集见 contracts/engine-action-sets.md）。

## Action 封闭集（5 个，机器对账）

| action | 来源 | 行为契约 |
|--------|------|----------|
| `probes` | 自 feedback-utils.py 迁入，行为不变 | 注册表查询/校验/对账；`--validate` 与 `--reconcile` 为本 action 的 **flag**（非独立 action，L1986–1992 现状语义保持）；MUST 覆盖新 Class（050 / 运行判定 / 证据 lane）的查询；`--action probes --validate` 计数排除「非实体 probe 目录」节（FR-004） |
| `map` | 自 feedback-utils.py 迁入，行为不变 | 探测面地图合成（现 compose_probe_map L1416 语义）；纯只读 |
| `probe-inject` | 自 feedback-utils.py 迁入，行为不变 | 外部 probe 注入（现 L1695–1755 语义）；写面仅 `.specify/memory/feedback/probes/`（零迁移，FR-009） |
| `handlers` | NEW | Handler/Binding 注册表查询：列表 + 按 `--point` / `--scope` / `--kind` / `--mode` 过滤 + `--validate`（FR-012）；纯只读 |
| `compile-embeds` | NEW | 编译收尾段，契约见 contracts/compile-embeds.md |

## 公共旗标（沿用 feedback-utils.py 惯例）

- `--format text|json`（缺省 text；与 feedback-utils.py L2023 同型）。
- 查询面（probes / handlers / map）对宿主项目**只读**可用；注册与编译写面仅框架真源侧（Q6 / FR-021）。

## 退出码契约（封闭集）

| 退出码 | 语义 | 触发例 |
|--------|------|--------|
| 0 | 成功 / 校验通过 / 无漂移 | — |
| 1 | 漂移预检命中 | compile-embeds --check 检出产物与注册表不一致 |
| 2 | 校验/对账错误 | 非法 action、behavior_owner 不可达、重复 Binding 三元组、order 冲突、孤儿/缺失 handler、生成措辞命中 BLOCKING_PATTERNS（拒写） |

## 迁移义务

- 三个迁入 action 的行为**逐字节不变**：同输入同输出（含 text/json 两种 format）。
- feedback-utils.py 移除三 action 与 probe 注册表加载后，其 `--action` choices 收缩为 11 个领域动作（清单与对账义务见 contracts/engine-action-sets.md）；其帮助文本/文档记载的 CLI 形态同步修订（requirements 边缘案例 L135）。
- 契约测试钉住两侧封闭集（053 import 对账先例：tests/contract/test_run_determination_engine.py L59–61/L266 同型）。
