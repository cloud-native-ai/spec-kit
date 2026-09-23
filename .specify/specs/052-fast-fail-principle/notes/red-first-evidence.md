# Red-First 证据 (T004) — Feature 052

**Taken at**: 2026-09-23,Phase 2(Foundational),在 T003 建骨架之后、任何实现任务之前。
**Command**:

```bash
python3 -m pytest tests/contract/test_fast_fail_discipline.py -q
```

**实跑输出(末行)**:

```
104 failed, 1 passed in 1.27s
PYTEST_EXIT=1
```

---

## 1. 计数与分类

骨架共 **105** 个测试函数(`--collect-only -q` 实测),对应五份契约的 **105** 条**制品类**条款(107 条总数减去 `dispatch-injection.md` C-24 / C-25 两条行为类——它们无制品可断言,由 T039 的变异演练取证)。

| 前缀 | 契约文件 | 函数数 | `FileNotFoundError`(制品缺失) | `pytest.fail`(断言体未实现) | 改前即绿 |
|---|---|---|---|---|---|
| `c` | `discipline-doc.md` C-1…C-22 | 22 | 21 | 0 | **1**(`test_c20_`) |
| `a` | `ambient-section.md` C-1…C-19 | 19 | 2 | 17 | 0 |
| `x` | `constitution-export.md` C-1…C-23 | 23 | 1 | 22 | 0 |
| `i` | `dispatch-injection.md` C-1…C-23, C-26 | 24 | 16 | 8 | 0 |
| `g` | `gate-neutrality.md` C-1…C-17 | 17 | 6 | 11 | 0 |
| **合计** | | **105** | **46** | **58** | **1** |

### 两类失败原因的区别是**设计出来的**,不是巧合

骨架函数一律是两行:先 `_text(<该条款的主制品>)`,再 `_unimplemented(<条款号>, <落地任务>)`。

- **`FileNotFoundError`(46 条)**:主制品尚不存在,第一行就抛出。全部 46 条读的都是**同一个**缺失制品 —— `shared/guidelines/fast-fail.md`(T006 创建)。故这一类的含义是"制品缺失",执行者在 T006 之后应看到它们**改变失败原因**(从 FileNotFound 变为断言不成立或转绿),而不是继续 FileNotFound。
- **`pytest.fail`(58 条)**:主制品**已存在**(见下表),`_text()` 成功返回,于是第二行的显式失败触发。这一类的含义是"断言体尚未实现",由 T005 / T016 / T025 / T036 / T042 / T050 各自填入。

⇒ **推论(对后续阶段的判据)**:骨架**永不绿**。任何在 T005/T016/T025/T036/T042/T050 之前就已转绿的函数,只有两种可能:要么它是 `test_c20_`(下方第 2 节),要么有人把 `_unimplemented()` 删掉了 —— 后者是一次以错误理由转绿的门禁,MUST 视为缺陷。

已存在的主制品(逐个 `is_file()` 实测为 True):

```
templates/instructions-template.md          .specify/instructions.md
templates/constitution-template.md          templates/commands/constitution.md
.specify/memory/constitution.md             templates/plan-template.md
agents/skill-verifier.agent.md              agents/structure-adjuster.agent.md
skills/create-team/references/patterns.md   skills/create-agent/SKILL.md
templates/commands/agents.md                shared/definitions/subagent-definitions.md
tests/contract/test_constitution_double_landing.py
tests/contract/test_user_facing_comprehension_doc.py
.specify/specs/050-proactive-flow-trigger/baseline-gates.json
scripts/python/scan-confirmation-gates.py   scripts/python/sync-mirrors.py
```

唯一缺失的制品:`shared/guidelines/fast-fail.md`。

---

## 2. 改前即绿的条款:逐条写明为何绿

只有 **1** 条。

### `test_c20_marker_literals_are_mutually_disjoint` — 绿

**为何改前即绿**:C-20 断言的是四个稳定字面量两两互不为子串:

| 字面量 | Shared String | 值 |
|---|---|---|
| 观察标记 | STR-001 | `[fast-fail]` |
| 注入子句标识 | STR-009 | `fast-fail-clause` |
| 回传异常行前缀 | STR-010 | `ANOMALY:` |
| 真源文档相对路径 | STR-002 | `shared/guidelines/fast-fail.md` |

这是**纯字符串运算**,不读任何制品 —— 它的真值只取决于 `requirements.md` 的 Shared Strings 表,而该表在 `/speckit.clarify` 第三轮已定稿。故此条在 red-first 阶段即可断言,且**必然**绿(FR-063 / V1 / `discipline-doc.md` C-20 明文如此规定)。

**它不是空真**:函数内同时断言 `len(C20_LITERALS) == 4` 且四个字面量各自非空(伴生非空断言),故"绿因为互斥成立"与"绿因为集合是空的"可区分。6 对组合全部双向检查(`a not in b` 与 `b not in a`)。

**历史**:STR-001 初版为裸 `fast-fail`,它是 STR-009(`fast-fail-clause`)与 STR-002(路径含 `fast-fail.md`)的**子串**,故 C-20 当时**为红**;clarify 第三轮据 FR-063 把 STR-001 改为带方括号的 `[fast-fail]` 后转绿。这一条因此是本特性自己"发现前提被证伪 ⇒ 停下上送 ⇒ 用户裁定 ⇒ 改字面量"的一次已发生实例。

**⚠️ 执行者注意(Feature 051 的 B-12 教训)**:此条改前即绿是**正确的**,MUST NOT 因为"红的才正常"而去削弱它、删掉它的伴生非空断言、或把四个字面量改成互不相关的值以"制造一次红"。T040 落地 STR-001 的最终形态后,T042 会**重跑**本条复核互斥性仍成立(见 tasks.md 的条款分区表:T043 的 `-k` 含 `c20_`,认领权仍属 T011)。

---

## 3. 骨架阶段顺带查出的两处缺陷(已就地订正)

本阶段的核验命令本身就是被核验对象的一部分 —— 跑它们时查出两处会让后续核验行**假绿或假红**的缺陷:

### 缺陷一:`pytest -k` 按子串匹配,原六行表达式的裸 token 会越界选中后续阶段的条款

原 tasks.md 的六行 `-k` 用裸 token(`c1 or c2 or …`)。实测(5 个桩函数 `test_c1_a` / `test_c2_e` / `test_c10_b` / `test_c18_c` / `test_c22_d`):

```
$ pytest -q -k "c1 or c2"  --collect-only   -> 5 tests collected   (c1, c2, c10, c18, c22)
$ pytest -q -k "c1_ or c2_" --collect-only  -> 2/5 tests collected (c1, c2)
```

后果:T011 明确要求 C-18/C-19/C-22 在该时点**仍为红**,而 `c1` / `c2` 会把它们选进来 ⇒ 核验行自身失败。T018(会拉入 A-13…A-15)、T026(会拉入 X-19…X-23)同病。

订正:六行表达式全部改为带尾下划线的 token(机械替换,复核零残留裸 token),并在 tasks.md 的分区表下新增一条说明,把"编号后紧跟下划线"定为对 T003 的**硬约束**、把"MUST NOT 为整洁去掉尾下划线"定为禁令。

### 缺陷二:`-k` 也匹配 slug,故 slug 里出现条款 token 会跨阶段泄漏

改完 token 后复测,T011 仍收集到 **22** 而非 19。多出的三条是 slug 自身含 token:

```
test_g8_c6_c7_anti_vacuity_sentinels   -> 含 c6_ / c7_
test_i7_c5_c6_anti_vacuity_sentinels   -> 含 c5_ / c6_
test_x20_ufc_c14_pin_raised_to_nine    -> 含 c14_
```

订正:重命名为 `test_g8_stop_semantics_anti_vacuity_sentinels`、`test_i7_clause_size_and_hits_anti_vacuity_sentinels`、`test_x20_ufc_dedup_pin_raised_to_nine`;另把 `test_a15_a14_mutation_drill` 改为 `test_a15_forbidden_sentence_mutation_drill`(它当时不跨阶段,但 A-14 与 A-15 一旦分到不同阶段就会泄漏)。随后对全部 105 个函数名做系统性扫描:**泄漏 0 条**。

### 订正后的分区实测(六行全部相符)

| 核验行 | 认领条款数(分区表) | `-k` 实收集数 | 判定 |
|---|---|---|---|
| T011 | 19 | **19** | MATCH |
| T018 | 16 | **16** | MATCH |
| T026 | 18 | **18** | MATCH |
| T037 | 24 | **24** | MATCH |
| T043 | 3(C-18/C-19 + C-20 附带重跑) | **3** | MATCH |
| T052 | 22 | **22** | MATCH |
| 全文件 | 105 | **105** | MATCH |

> 这两处缺陷是**同一根因**的两种表现:把一个按子串工作的选择器当成按标识符工作的选择器用。它属于本特性要点名的失效形态 —— 检查返回 0(收集成功、退出码正常),但其输出并不关于它被写来判定的命题。故已一并记入 T062 的教训候选。
