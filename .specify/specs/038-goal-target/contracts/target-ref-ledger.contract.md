# Contract: target-ref-ledger(items.jsonl `target_ref` 与切片轴折叠)

**Surface**: `items.jsonl` 行契约扩展 + `build-summary-input.py` 折叠行为
**Implements**: FR-013, FR-014, FR-015, FR-016;SC-001, SC-005
**Upstream contract**: 036 `contracts/items-ledger.contract.md`(LC-1…LC-10)——本契约**叠加**,不改动其任何条款。

## 1. 字段契约(FR-013)

| 规则 | 约定 |
|------|------|
| 字段名 | [[STR-003]],可选 |
| 取值文法 | 局部形 `T-\d{3}`;goal 由团队绑定隐含;限定形/其他形态非法 |
| 缺省语义 | 归属 goal 整体;存量行语义 MUST 不变 |
| IL-1…IL-5 | 全部保持——append-only、末行定态、tracked provenance、身份文法、supersedes 折叠均不因本字段改变 |
| 写入者 | 仅团队主管(036 FR-021);子代理 MUST NOT 写入 |

## 2. 折叠规则(build-summary-input.py)

`fold_ledger` 扩展为单遍扫描中同时分组:

1. 行携带合法 [[STR-003]] 且该身份存在于绑定 goal 的 [[STR-001]] 节 → 计入该 Target 的归属集合(末行定态语义不变:同一 `item_id` 以最后事件为准)。
2. [[STR-003]] 指向不存在身份 → 记为无效归属行:按 goal 整体降级计入,并在表单 `targets.invalid_refs` 计数 + 报告声明;MUST NOT 臆造 Target(FR-014)。
3. 无 [[STR-003]] → goal 整体(既有行为)。
4. 归属与团队命名空间前缀(`<team-slug>.TI-nnnn`,036 §6.2)正交:前缀照常加,[[STR-003]] 仍为局部形。

## 3. 表单输出(D4)

- goal 存在 [[STR-001]] 节 → 表单产出 `targets:` 块(结构见 data-model.md §派生结构),含每 Target 的 `authored_status` / `attributed_items` / `completed_items` / `pending_approval`、`coverage`(按 authored 终态计 n/m)、`unattributed_to_target`、`invalid_refs`。
- goal 无该节 → 表单 MUST 不含 `targets:` 块(既有输出逐字节不变,SC-002)。
- 切片轴 MUST 与判据轴分列;表单与报告 MUST NOT 出现由 Target 完成度推导 goal `achieved` 的字段或表述(SC-005;037 FR-030/FR-031 权威不变)。

## 4. 待批准项(FR-015)

`authored_status` 为 `open` 而归属条目全部 `completed`(且归属条目数 ≥ 1)→ `pending_approval: true`,报告侧显式列为"待批准完成"条目;两侧(authored 状态与台账证据)MUST NOT 被折叠流程自动翻转。反向(authored `done` 而归属条目未完成)同样列出,提示复核。

## 5. 里程碑吸收(FR-016, P3)

- `authored_status: done` 的 Target 追加为 `milestones` 组行:`title` 取语句,`status` 映射 achieved 语义,`source` 取 `goal-target:<goal-slug>/goal.md#T-<nnn>`。
- 判据投影行(036 FR-013)语义原样保留,来源标记两类天然区分;判据为空而存在 done Target → 里程碑组由 Target 来源条目填充并声明来源(US4 场景 2)。
- `skills/summarize-project/` 代码与 DDL 不改——区分仅靠既有 `source` 列(D7)。

## 6. Contract / Integration Test Pins

- 携带/缺失/非法 [[STR-003]] 三类行的折叠归属断言(SC-001 归属 100% 无歧义)。
- 无节 goal 的表单 diff 为空(SC-002)。
- 轴分列与负向扫描:产物中不存在 "targets done ⇒ achieved" 推导句式(SC-005)。
- `pending_approval` 两侧触发(open/全完成;done/未完成)各一例。
- 里程碑组:判据行 + Target 行共存、来源标记区分、判据为空时的填充。
