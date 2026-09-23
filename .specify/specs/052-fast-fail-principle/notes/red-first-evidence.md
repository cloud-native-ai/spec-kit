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

---

# 变异演练取证(T039 / T051 — 行为类条款 C-24 / C-25)

`dispatch-injection.md` C-24 / C-25 是**行为类**条款:编排者与子代理在运行期的动作无落盘制品可断言,故 MUST 由实跑演练取证,且形态 MUST 为「把被守物弄坏 → 确认变红 → 复原 → 确认恢复绿」,而不是"当前树上通过"。

**取证方式(可复现)**:四个场景的命令块由 `quickstart.md` **逐字提取后执行**,不重打——
`re.search(r'^## 场景 N .+?(?=^## 场景 |\Z)')` 取节,再取 `**改后期望**` 之后最后一个 ```bash 块,写入 `/tmp/scenN.sh` 后 `bash` 执行。这样"我跑的就是制品印的那条命令"是可核验的,而不是靠记忆重写一遍。

| 场景 | 被演练的命题 | 实跑输出 | 期望 | 判定 |
|---|---|---|---|---|
| 6 | 派发前自检确实在派发**之前**发生(FR-053) | `prompt bytes: 931`;子句命中数 **3 → 0 → restored 且 3**;`ls: cannot access '/tmp/ffdrill': No such file or directory` | ≥1 → 0 → `restored` 且 ≥1 → 目录不存在 | ✓ |
| 10 | 缺异常行的回传被判为**不完整**(FR-066) | `有异常: anomaly-halt` / `无异常: clean` / `缺异常行: incomplete` / `行内提及: incomplete`;`doc carries the rule: True` | 第四例(行内提及 `ANOMALY:`)**不得**判为 clean | ✓ |
| 11 | 异常停 MUST NOT 被原样重派(FR-055) | `next action: surface-to-user \| allowed: True \| forbidden: False`;`doc names '两振': True` / `'派发失败': True` / `'非并行': True` | 同左;三条既有失败规则都 MUST 被点名 | ✓ |
| 12 | 干净运行也显式说一句(FR-067) | `repairs=0 fails=0 -> True` / `repairs=2 fails=0 -> False` / `repairs=0 fails=1 -> False`;`doc owns the literal: True` | **True / False / False**(只有干净运行需要该陈述) | ✓ |

四个场景 exit code 均为 **0**。

**C-25 的删净复核**:场景 6 与场景 10 各自 `rm -rf /tmp/ffdrill` 后再 `ls`,输出均为 `No such file or directory`,即演练制品计数归零;本文件与仓库内均无残留(`git status` 于 Phase 6 提交前为空)。

**场景 10 第四例的实质**:回传里**行内提及** `ANOMALY:`(例如复述自己被要求怎么做)MUST NOT 被读作一次异常停——这正是 C-20 把判据定为**行首**前缀而非"含该子串"的理由。若按子串判定,这一例会误报为 anomaly-halt;演练证明按行首判定它落到 `incomplete`(既不是干净、也不是异常停),分类正确。

---

# 实现期新查出的自身缺陷(T039 同批,附变异演练)

## 缺陷三:自指哨兵被自己的诊断文本触发

`test_i12_channel_two_bounded_set`(C-12 有界性)的形态是"读取本测试模块自身的源码,断言其中不含对 `.specify/agents/instances/` 的枚举"。初版把该路径**逐字写进了断言的失败消息**,于是哨兵在自己的诊断文本上命中,恒红。

- 根因:一个"扫描自身源码"的检查,其**探针字符串与被禁字符串是同一个字面量**。
- 订正:把 needle 由片段拼出(`"agents" + "/" + "instances"`),并把诊断消息改写为不含该路径的散文("the project-local agent-instance directory");再为该哨兵配一条伴生断言(模块源码长度 > 1000 且 `FACTORY_PRESETS` 仍在场),使"没命中因为对"与"没命中因为读空了"可区分。
- 变异演练:把该守卫改成真的去 `glob` 那个无界目录 → `test_i12` **变红**并印出 C-12 的理由 → 从备份复原 → **恢复绿** → 重新编译通过、收集数仍为 **105**。演练备份用 `\cp -f` 复原(alias-proof),复核方式为重跑该用例而非只看 `cp` 的退出码。

> 这一条形态与首轮查出的 `-k` 子串泄漏同源:**把一个按文本工作的机制当作按标识符工作的机制用**。扫描自身源码时,扫描器读到的包括它自己的报错文案。已记入 T062 的教训候选。

---

# C-15 / A-14 变异演练取证(T051)

**被演练的命题**:`ambient-section.md` C-14 —— 常驻章节 MUST NOT 含"刷新项目指令即连同其镜像副本一并恢复"一类句式。这是**负面命题**,故 MUST 配变异演练,不能只看它在当前树上通过。

**四步实跑**(对象:`templates/instructions-template.md` 的 `## Fast Fail Discipline` 节;断言:`test_a14_no_refresh_instructions_restores_mirror`)

| 步 | 动作 | 实跑结果 |
|---|---|---|
| 0 | 演练前基线 | `pytest -k "a14_"` → `1 passed`,exit **0** |
| 1 | 把房式假承诺句 `refresh the project instructions to restore it together with its mirror copy` 插入本章节 | `pytest -k "a14_"` → exit **1**,`AssertionError: C-14: templates/instructions-template.md carries the false restore promise ...` ⇒ **变红** |
| 2 | 移除该句(以精确字符串反向替换,并 `assert count == 1` 确认只命中一处) | — |
| 3 | 复核恢复 | `pytest -k "a14_"` → `1 passed`,exit **0** ⇒ **恢复绿**;`git diff --stat -- templates/instructions-template.md` 输出 **0 行**;`git diff --quiet` 退出 0 ⇒ 文件与 HEAD **逐字节相同**,演练零残留 |

**为何 C-14 成立(机制侧实测,不靠断言自证)**:`scripts/bash/generate-instructions.sh` 全文不含 `shared/guidelines`,`test_a14` 把这一点作为断言的一部分——若日后该脚本真的开始复制 guideline 文件,这条断言会变红并提示"假承诺禁令需要重新推导",而不是继续守一条已经过时的禁令。

**顺带查明的上游缺陷(按 FR-077 上报,不改写)**:活动指令文件 `.specify/instructions.md` 中该假承诺句式**仍存在 1 处**,归属 **Feature 051 的 `## User-Facing Comprehension` 节**(实测:命中行所属的最近 `## ` 标题即该节;本特性的 `## Fast Fail Discipline` 节区间内命中数为 **0**)。FR-077 明文规定该同类问题属上游缺陷、MUST 单独上报、MUST NOT 由本特性顺手改写(那会是一次未获授权的爆炸半径越界),故本特性只保证**自己那一节**不含该句式。

> 复原动作一律用精确字符串替换并以 `assert count == 1` 自证只命中一处,不用 `cp` 回填——本轮早先一次演练正因 `cp` 被 alias 成交互模式且后接 `&& rm -f` 而删掉备份、留下残留(见上文"实现期新查出的自身缺陷"一节之后的记录)。
