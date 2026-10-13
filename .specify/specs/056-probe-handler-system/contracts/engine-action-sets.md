# Contract: 引擎动作封闭集（迁移两侧）

**Spec**: `.specify/specs/056-probe-handler-system/requirements.md` | **Date**: 2026-10-13
**先例**: 053 import 对账（tests/contract/test_run_determination_engine.py L59–61 / L266）
**实测基础**: feedback-utils.py `--action` choices 14 项（scripts/python/feedback-utils.py L1936–1938，2026-10-13 实测）

## 迁移分区（封闭集，契约测试双向钉住）

### probe-utils.py（STR-002）— 5 个 action

```text
probes  map  probe-inject  handlers  compile-embeds
```

- 前三者自 feedback-utils.py 迁入，行为不变；`--validate` / `--reconcile` 是 `probes` 的 flag（非 action）。
- `handlers` / `compile-embeds` 为新增。

### feedback-utils.py（迁移后保留）— 11 个领域 action

```text
record  status  list  dispose  mark-submitted  reindex
package  cleanup  upstream  migrate-legacy  introspect-register
```

- 14（实测）− 3（probe 族迁出）= 11，行为逐字节不变。
- 封闭集契约测试随迁移同步修订（旧调用方：契约测试与 docs 记载的 CLI 形态，requirements 边缘案例 L135）。

## 对账义务

1. **双向钉住**：两个脚本各自的 `--action` choices 被契约测试逐一断言；任一侧多出/缺失 action 即失败。
2. **kind=engine 封闭集**：Handler 行的 engine action 必须命中真实引擎 action 并集（feedback-utils.py 11 项 + run-determination.py ACTIONS L92 + probe-utils.py 5 项 + 其他引擎），validate 拒绝封闭集外引用（exit 2，FR-007）。
3. **迁移行为不变**：三个迁入 action 在迁移前后对相同输入产生相同输出（text/json 双 format）——迁移 diff 审查 + 契约测试锁定。

## 与宿主的关系（Q6 / FR-021）

- 查询面（probes / handlers / map 列表）宿主只读可用；任何写面（probe-inject 的存储写、注册编辑、编译写入）仅框架真源侧。
