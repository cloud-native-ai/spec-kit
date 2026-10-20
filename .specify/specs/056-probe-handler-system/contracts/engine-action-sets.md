# Contract: 引擎动作封闭集（迁移两侧）

**Spec**: `.specify/specs/056-probe-handler-system/requirements.md` | **Date**: 2026-10-13
**先例**: 053 import 对账（tests/contract/test_run_determination_engine.py L59–61 / L266）
**实测基础**: feedback-utils.py `--action` choices 14 项（scripts/python/feedback-utils.py L1936–1938，2026-10-13 实测）
**修订**: 2026-10-20（Feature 063 C-22 同批修订）——三个 wrap-up 引擎（feedback-utils.py / run-determination.py / exec-quant.py）各增 `args-manifest`（机器可读参数 manifest，compile-embeds 渲染器编译期消费，owner 契约 `.specify/specs/063-review-p1-governance/contracts/engine-face-contract.md` C-22）；本文件的封闭集分区按当前生效集合更新，历史迁移算式保留于各行注记。

## 迁移分区（封闭集，契约测试双向钉住）

### probe-utils.py（STR-002）— 5 个 action

```text
probes  map  probe-inject  handlers  compile-embeds
```

- 前三者自 feedback-utils.py 迁入，行为不变；`--validate` / `--reconcile` 是 `probes` 的 flag（非 action）。
- `handlers` / `compile-embeds` 为新增。

### feedback-utils.py（迁移后保留）— 12 个 action（11 领域 + 063 C-22 增 `args-manifest`）

```text
record  status  list  dispose  mark-submitted  reindex
package  cleanup  upstream  migrate-legacy  introspect-register  args-manifest
```

- 历史迁移算式（2026-10-13）：14（实测）− 3（probe 族迁出）= 11，迁移行为逐字节不变；`args-manifest` 为 063 C-22 新增（迁移后的封闭集增长，非迁移面），封闭集契约测试同批修订。
- 旧调用方（契约测试与 docs 记载的 CLI 形态，requirements 边缘案例 L135）不受影响：新增 action 不改变既有 action 行为。

### run-determination.py — 4 个 action（ACTIONS 常量封闭集）

```text
determine  settle  history  args-manifest
```

- 063 C-22 起 exact-pin 双向钉住（此前仅入并集，未单侧钉死）；`args-manifest` 为 063 新增。

### exec-quant.py — 5 个 action（059 落 4 + 063 C-22 增 `args-manifest`）

```text
collect  list-records  score  collect-dispatch  args-manifest
```

- 059 新引擎;动作闭包自引擎 argparse choices 实读(choices 路径,与
  feedback/probe 同);exact-pin 与跨引擎动作名零交集断言钉住
  (test_probe_engine_action_sets.py 扩展)。
- 历史注记:本文件 2026-10-13 版曾记「3 个 action」,059 的 collect-dispatch
  落地时未回写本行——2026-10-20 修订按当前生效闭包(4+args-manifest)订正。

## 对账义务

1. **双向钉住**：各脚本各自的 action 集被契约测试逐一断言；任一侧多出/缺失 action 即失败。
2. **kind=engine 封闭集**：Handler 行的 engine action 必须命中真实引擎 action 并集（feedback-utils.py 12 项 + run-determination.py ACTIONS + probe-utils.py 5 项 + 其他引擎），validate 拒绝封闭集外引用（exit 2，FR-007）。
3. **迁移行为不变**：三个迁入 action 在迁移前后对相同输入产生相同输出（text/json 双 format）——迁移 diff 审查 + 契约测试锁定。
4. **args-manifest 契约**（063 C-22）：manifest 由各引擎自有 parser 派生，`(engine, action)` 缺 manifest 时 compile-embeds 拒绝编译（registry/engine 分歧是 fast-fail 面）。

## 与宿主的关系（Q6 / FR-021）

- 查询面（probes / handlers / map 列表）宿主只读可用；任何写面（probe-inject 的存储写、注册编辑、编译写入）仅框架真源侧。
- `args-manifest` 为纯查询面（stdout JSON，零写面），宿主可用。
