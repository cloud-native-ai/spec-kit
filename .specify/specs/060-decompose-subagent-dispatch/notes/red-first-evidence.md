# Red-First Evidence — 060-decompose-subagent-dispatch

## T002 — C-1..C-8 真源契约测试（2026-10-17）

```
$ python3.14 -m pytest tests/contract/test_agent_dispatch_mechanism.py -q -p no:cacheprovider
7 failed, 1 passed in 0.05s
FAILED test_c1_delegation_section_in_agent_definitions
FAILED test_c2_responsibility_divide_declared
FAILED test_c4_topology_declaration_section
FAILED test_c5_declaration_vs_recipe_division
FAILED test_c6_anti_nesting_referenced_in_governance
FAILED test_c7_layer_boundary_rules_present
FAILED test_c8_cross_layer_change_ban
```

红因：接线段/拓扑声明段/层界判定在两份真源中尚不存在（subjects not yet authored）——1 passed（C-3 无第三 owner）为稳态即绿，符合预期。

## 后续批次红证据

（各相位 Author 行追加）
