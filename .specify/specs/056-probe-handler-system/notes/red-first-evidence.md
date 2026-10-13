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

## 记录（US2 · 2026-10-13）

### 自然红批次（实现前，8 failed / 5 passed）

`python3 -m pytest tests/contract/test_handler_registry.py tests/contract/test_probe_engine_action_sets.py -q`
→ `8 failed, 5 passed`。归因全部 **subject 缺失/未迁移**：

- 5 个为 Handler/HandlerBinding 章未建（chapter missing / no rows / seed handlers missing）；
- 3 个为 `probe-utils.py` 未建（engine 缺失：validate FileNotFoundError / sandbox FileNotFoundError / action set missing）；
- 1 个为 feedback-utils 仍 14 action（迁移未做，`got != FEEDBACK_ALLOWED`）。
- 5 个 pass 为空集上的形态守卫（vacuous），红能力由 T016 沙箱演练证明。

### T012 后中间态（9 passed / 4 failed）

注册表侧全部转绿（章结构 / 六字段封闭集 / 三元组唯一 / 点内 order 唯一 / 种子次序约束 / selector+scope 封闭集 / owner 可达 + agent 锚点即标题原文）；余 4 红均为引擎侧（probe-utils.py 缺失 ×3、feedback choices 尚未收缩 14→11）——与 T013/T014 的 subject 对应。

## 记录（T015–T017 · 2026-10-13）

### T015 compile-embeds 实现（scripts/python/probe-utils.py）

7 步算法落地：`scan_compile_units`（义务扫描 = `## Feedback` 字面 / 手工 `## Documentation` / H2 `## Wrap-up` 三类标记，迁移后再扫描稳定）→ `_effective_handlers`（selector 命中 → scope 匹配 all / complex-commands / skills / 逐 object_id **加法**订阅，多 selector 同 handler 合并）→ `render_wrap_up_section`（单 AUTO-GENERATED `## Wrap-up` 段：横幅含真源路径 + 指纹 sha256(Handler+Binding rows)[:12]；技能面保留 runtime-mode gate 判定结构；kind 派生一行调用形式：engine → `python3 .specify/scripts/python/<engine> --action <action> --unit-id "<unit_id>" --unit-type <command|skill>`，agent/gate → `.specify/<owner>` § "<action 标题>"）→ `_replace_sections`（删手工 Feedback/Documentation/编译 Wrap-up 段，编译段落位于既有 `## Feedback` 段位）→ 原子写（tmp + os.replace）。

**实现期裁定**（记录于 contracts 之上）：
- **scope 语义 = 加法**。逐 object_id 行仅命中该单元（data-model L108"仅命中该 ProbeObject 所属单元"）；"扣减覆盖"的排除编码在本期实测矩阵中**无需求**——简单命令排除集由义务扫描自然实现（agents/constitution/feature 无 `## Feedback` → 不在单元宇宙）。若未来矩阵需要排除行，届时随其契约测试一起加编码（YAGNI）。
- **运行时面路径映射**：注册表 owner 为框架源面（`scripts/…`/`shared/…`），编译段引用运行时面 `.specify/…`——下游项目只有 `.specify/` 树（两顶帽：发布→init 拓扑），contracts/compile-embeds.md 的 `python3 scripts/python/…` 示例形按此修正理解（引擎文件 + action 的形不变，路径面取运行时面）。
- **拒写封闭集落地**：validate_handlers 全集（缺失 handler 引用 / 非法 engine action / order 冲突 / owner 不可达 / 重复三元组）+ **孤儿 handler**（注册无 binding）+ **BLOCKING_PATTERNS**（按路径 import scan-confirmation-gates.py 的 BLOCKING_RE，命中整体拒写并逐单元指名）。`--check` 漂移 = 全文件重算比对，exit 1 逐单元指名、零写入。

**沙箱演练（/tmp/t015-sandbox，全绿）**：
1. 迁移前 `--check` → exit 1，单元逐名（3/3）；2. compile → plan 段落位于 `## Feedback` 位、Documentation 段移除、接缝干净；技能面含 runtime gate；3. 重编译 → `0 written, 3 unchanged` + plan.md 逐字节一致（确定性）；4. 迁移后 `--check` → exit 0；5. json format payload 正确；6. 全 scope 翻离 zero.md → 手工段移除且**零段输出**（Q5），`--check` 计数降为 2（zero.md 退出宇宙）；7. 孤儿 handler → exit 2 `orphan handler: 'h-orphan' has no HandlerBinding row`；8. 措辞门控 → exit 2 逐单元指名命中模式（`'stop and confirm'`）。

**实现中发现并修复的缺陷**（归因 = subject）：
- `validate_handlers` order 冲突误报：同 handler 多 selector/scope 订阅被计为冲突——data-model 合并规则明确"order 冲突错误仅适用于不同 Handler"；改为 (point, order) 桶内**distinct handler 集合**判定。
- `_replace_sections` 接缝缺陷：`splitlines()` 吞掉编译段尾空行导致下一段标题与末条目粘连；改 `split("\n")` 保尾空行。

### 迁移收尾修订（T013/T014 旧调用方）

- `tests/contract/test_feedback_probe_registry.py`：整体 re-point 至 `probe_utils.main`（17 用例，全 probe 族）。
- `tests/contract/test_feedback_probe_cli.py`：TestMapAction×5 / TestProbeInjectAndExclusion 的 probe-inject·probes·map 调用 / TestSmokeRemediationContracts F2 → `probe_utils.main`；feedback 域用例（list/dispose/package/cleanup/migrate-legacy）不动。
- feedback-utils.py 缺陷修复：`action_record` 的 `custom:` 校验仍引用已迁走的 `_CUSTOM_UNIT_RE`（NameError）→ 从 probe_utils re-export 补回（单一真源不变）。

### T016 引擎验证

- 六套 probe/handler 契约套件 `72 passed`（handler_registry 9 + engine_action_sets 5 + probe_registry 17 + probe_cli 全量 + nonentity + umbrella）。
- **基线重放（本日新增 5/5 IDENTICAL）**：probes --format json / probes --validate / probes --reconcile（真仓只读）+ map --format json / probe-inject（scratch 播种真注册表 + 非实体目录指针目标）——新旧引擎同参逐字节一致；其余 7 对基线已在 T013/T014 当轮证明。
- seed 五行 `--action handlers --point wrap-up --validate` → exit 0（5 handlers, 5 bindings）。
- 沙箱演练（测试内永久化）：随 T018 `test_compile_embeds.py` 落位（本轮沙箱证据见上节 1–8）。

### T017 镜像双写

`sync-mirrors --write`（probe-utils.py + feedback-utils.py 两文件）→ `.specify/scripts/python/probe-utils.py` 就位且独立调用复现同结果（mirror `handlers --validate` exit 0；mirror `compile-embeds --check` exit 1 / 69 units）；`sync-mirrors --check` 全 OK（agents/scripts/shared 三面零漂移）。

### 实测树 --check（迁移前真值）

`compile-embeds --check` 于真仓 → exit 1，**69/69 单元漂移**（23 命令 + 46 技能），逐名清单与实测单元集一致；简单命令（agents/constitution/feature）不在宇宙；`--format json` 漂移计数 69/69；工作树零写入。

### 全仓契约套件清扫（Phase 3 收尾）

`pytest tests/contract -q` → **2718 passed, 0 failed**。清扫发现并修复 2 个旧调用方（均归因 = 迁移波及，非 subject 缺陷）：

- `test_dogfooding_practice.py` C4：`ENGINE_ACTIONS` 字面钉的是迁移前 14-action 集 → 拆分 `FEEDBACK_ENGINE_ACTIONS`（11）+ `PROBE_ENGINE_ACTIONS`（5），choices 钉住改指 feedback 11 集，doc-real 检查改用并集（doc 可引用两引擎的 action）。
- `test_store_state_protocol.py` TestTwoBranchMerge：fixture 仓只拷 feedback-utils.py 单文件 → feedback-utils 现于模块加载期 import 兄弟 probe-utils.py（056 引擎拆分）→ fixture 补拷成对文件。
