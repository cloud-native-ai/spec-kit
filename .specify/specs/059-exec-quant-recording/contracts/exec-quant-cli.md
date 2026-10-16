# Contract: exec-quant.py 引擎 CLI(Feature 059)

**Spec**: `.specify/specs/059-exec-quant-recording/requirements.md` | **Date**: 2026-10-16
**Behavior owner**: `scripts/python/exec-quant.py`(实现期落地;本文是目标契约,由 `tests/contract/test_exec_quant_engine.py` 钉住)

引擎动作封闭集(D1):`collect` / `list-records` / `score`(与既有四引擎动作名零交集)。运行形态与相邻引擎一致(`python3 .specify/scripts/python/exec-quant.py …`);wrap-up 编译面呈现最小调用行,调用方按需补参(既有约定,同 run-determination)。

## 通用参数

| 参数 | 必填 | 语义 |
|------|------|------|
| `--action` | 是 | `collect` \| `list-records` \| `score` |
| `--unit-id` | collect/score 必填;list 可选过滤 | `/speckit.<cmd>` \| `skill:<name>` \| `custom:<owner>/<name>` |
| `--unit-type` | 否(与 unit-id 形态不符时用法错误) | `command` \| `skill` \| `custom-unit` |
| `--run-id` | 否 | collect:显式 run_id(缺省走 D2 解析);list:过滤到单 run |
| `--workspace-root` | 否 | 工作区根(缺省自定位,同相邻引擎) |

## 动作一:`collect`(FR-001/002/005–010/012)

```bash
python3 .specify/scripts/python/exec-quant.py --action collect \
  --unit-id "/speckit.plan" --unit-type command [--run-id "<stable-run-id>"]
```

行为:采集三字段组 → 按 D2 解析 run_id → 写一行 JSON 到 `records.jsonl`。判定记录存在则携带其四轴/qualification/failed_set_diff 并标注 `carried`;不存在则对应字段 `not_evaluated`。

- 退出码:`0` 成功(含降级采集——字段降 not_evaluated 但记录照落);`1` 采集/写盘失败(stderr 消息可见,非阻塞);`2` 用法错误(如 unit-id 形态非法)。
- 幂等:同 `(unit_id, run_id)` 重复 collect 输出 duplicate 提示并不追加第二行(同运行判定 L1411 先例)。
- 输出(text):一行摘要含 run_id、run_id_resolution、落库路径。

## 动作二:`list-records`(FR-013)

```bash
python3 .specify/scripts/python/exec-quant.py --action list-records \
  [--unit-id "..."] [--unit-type command|skill|custom-unit] [--since "2026-10-16"] \
  [--run-id "..."] [--format text|json]
```

行为:读 `records.jsonl` + `scores.jsonl`,按过滤条件枚举,join 打分(最新 `scored_at` 胜),每条呈现身份三元组与三字段组要点。

- `--format json`:机器可读形态(FR-013 的 machine-readable 形态),逐记录完整 schema(含逐字段 provenance 与 not_evaluated 标记);`--format text`(缺省):人类可读摘要行。
- 退出码:`0`(含零命中——零命中是结果非错误)。

## 动作三:`score`(FR-014)

```bash
python3 .specify/scripts/python/exec-quant.py --action score \
  --unit-id "/speckit.plan" --run-id "<existing-run-id>" --score <1-5> [--note "..."]
```

行为:对既有记录追加一条打分行到 `scores.jsonl`(append-only,D3);不触碰 records.jsonl。

- 前置:目标 `(unit_id, run_id)` 在 records.jsonl 必须存在(打分是「对既有记录补录」,无记录可打 → 退出码 `2` 用法错误)。
- `--score` 接受 1–5 数值(通道约定,非打分模型);越界 → 退出码 `2`。
- 退出码:`0` 成功;`1` 写盘失败;`2` 用法错误(记录不存在/分值越界/缺参)。

## 交叉约束

- **action 封闭集对账**:动作经 argparse `choices=["collect", "list-records", "score"]` 声明——`_engine_action_union()` 对 choices 分支实读(与 feedback/probe 引擎同路径;`ACTIONS` 元组分支仅 name-gated 于 run-determination/trigger-utils,见 `contracts/probe-registration.md` §2);`_ENGINE_SIBLINGS` 追加后,Handler 行 `action=collect` 命中 union。
- **跨引擎动作名零交集**:与既有四引擎动作名零同名(各引擎动作清单以各自源码为真源,不在此复述);由测试扩展钉死——跨引擎动作名交集断言 = ∅ + choices exact-pin。
- **存储边界**:引擎只写 `.specify/memory/exec-quant/`;不触 feedback store、session store、任何上送路径(FR-009/FR-011)。
- **新引擎 exact-pin**:`test_exec_quant_action_set_exact`(新增于 test_probe_engine_action_sets.py 扩展)断言 `--action` choices 恰为这三项。
