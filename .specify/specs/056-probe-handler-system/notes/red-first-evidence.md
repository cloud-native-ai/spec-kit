# Red-First Evidence — 056-probe-handler-system

> 运行期证据落点（tasks.md T001 创建）。记录每个红优先测试在实现前的失败证据：测试名、失败断言、失败原因归因（制品缺失 vs 断言写错）。

## 格式

每条记录：

```
### <test file>::<test id>
- 时间: <UTC timestamp>
- 命令: <exact command>
- 输出（决定性摘录）: <paste>
- 归因: <subject 缺失 | assertion 缺陷 | 外部在途>
- 恢复: <实现落地后转绿的证据或引用>
```

## 记录（US1 · 2026-10-13）

### 自然红批次（实现前，7 failed / 12 passed）

`python3 -m pytest tests/contract/test_probe_registry_umbrella.py tests/contract/test_probe_nonentity_catalog.py -q`
→ `7 failed, 12 passed`。7 个自然红均为 **subject 缺失**（散布探测点尚未入册、目录章未建、引擎分支未加）；12 个 pass 证明锚点与指针路径真实存在（断言自身健康）。

### 闭合期两处 assertion 缺陷（4 failed → 修复）

首次闭合运行暴露 4 个红，归因均为 **assertion 缺陷**（subject 已落地且正确），修复全部落在测试侧：

1. `test_probe_registry_umbrella.py::test_class_rows_carry_resolvable_code_anchors` 与 `::test_objects_for_new_classes_use_script_units`
   - 输出: `AssertionError: engine anchor scripts/python/evidence-utils.py:LANE_NAMES has no registry class row` + `assert (...) in {}`（declared 为空）
   - 归因: assertion 缺陷 — 测试的 `ANCHOR_RE` 期望 `` `path`:anchor `` 形，而注册表实际著写 `` `path`:`anchor1`,`anchor2` ``（多锚点、锚点带反引号），正则零命中。
   - 修复: 换成 `_parse_anchor_cell` 单元格解析器（路径 + 逗号分隔锚点 token），与注册表著写形对齐。
2. `test_probe_nonentity_catalog.py::test_catalog_entries_are_reachable_pointers` 与 `::test_catalog_entries_match_expected_probe_semantics`
   - 输出: `catalog missing pointer entries: [全部 5 条]`，但 traceback locals 显示 body 明确含 5 条目行、`entries = {}`
   - 归因: assertion 缺陷 — `ENTRY_RE` 缺 `re.MULTILINE`，`^`/`$` 在多行 body 上永不命中。
   - 修复: `re.compile(..., re.MULTILINE)`。

修复后: `19 passed`（exit 0）。

### 变异演练（最终形测试的红能力证明）

两处改形后的测试在最终形下从未见过红态，故各做一次 drill（break → red → 精确逆向恢复 → green）：

- **Drill A**（反向对账路径）: 从 run-determination 类行删去 `` ,`probe_session_store` `` token →
  `AssertionError: engine anchor scripts/python/run-determination.py:probe_session_store has no registry class row`（红，报错含冒犯名）→
  逆向恢复（`count == 1` 断言）→ 该测试 1 passed。
- **Drill B**（目录可达性路径）: 删除 `- \`scripts/python/clause_extract.py\` — ...` 整行 →
  `AssertionError: catalog missing pointer entries: ['scripts/python/clause_extract.py']`（红）→
  逆向恢复（`count == 1` 断言）→ 19 passed + `probes --validate` 复绿（9 classes, 106 internal + 0 external, exit 0）。

恢复后 `sync-mirrors --check` = OK（exit 0），镜像零漂移。
