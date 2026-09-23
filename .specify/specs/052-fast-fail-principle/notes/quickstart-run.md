# Quickstart 实跑记录 — Feature 052

本文件由 T012 / T019 / T027 / T038 / T043 / T053 / T054 逐场景追加。每条输出均为**实跑**,不是预期值抄写。

---

## 场景 1 — 真源文档存在且与镜像逐字节相等(T012,改后判据)

```bash
ls -l shared/guidelines/fast-fail.md .specify/shared/guidelines/fast-fail.md
cmp shared/guidelines/fast-fail.md .specify/shared/guidelines/fast-fail.md && echo "BYTE-IDENTICAL"
ls -1 shared/guidelines/*.md | wc -l
```

```
-rw------- 1 agent agent 13452 Sep 23 16:21 shared/guidelines/fast-fail.md
-rw------- 1 agent agent 13452 Sep 23 16:21 .specify/shared/guidelines/fast-fail.md
BYTE-IDENTICAL
count = 13
```

**判定**: 两个文件均存在 ✓(各 13452 字节);`cmp` 静默并输出 `BYTE-IDENTICAL` ✓;份数 = **13**(改前 12 + 1)✓ —— 与场景 1 的改后期望逐项相符。

> *本行曾因生成它的 shell 命令把 `` `BYTE-IDENTICAL` `` 写在双引号内而未转义、被 bash 当作命令替换执行(`BYTE-IDENTICAL: command not found`)而丢失内容,已订正。该形态与 FF-9 同类:命令报告成功、文件也确实写出了,但被写出的内容不是关于命题的那一句 —— 一次落在取证文件自身的盲检。*

---

## 场景 7 — 两份清单的条目语法与 7 项点名覆盖(T012,改后判据)

```bash
grep -cE '^- \*\*(FF|RP)-[0-9]+ ' shared/guidelines/fast-fail.md
grep -cE '^- \*\*(FF|RP)-[0-9]+ .*判据:' shared/guidelines/fast-fail.md
for n in 2 3 4 5 6 7 8; do printf "FF-%s: " "$n"; grep -c "^- \*\*FF-$n " shared/guidelines/fast-fail.md; done
```

```
entries total      = 21
entries with 判据: = 21
FF-2: 1
FF-3: 1
FF-4: 1
FF-5: 1
FF-6: 1
FF-7: 1
FF-8: 1
```

**判定**: 第一条 = **21** ≥ 15 ✓(FF 侧 15 + RP 侧 6);第二条 = **21**,与第一条**相等** ✓(每条都携判据,FR-076 的机械化成立);
`FF-2`…`FF-8` 七项各 **1** ✓(盲检四成因 + `git diff` 三形态逐项可定位)。清单总条数不设钉子(FR-020,可生长)。
---

## 场景 2 — 常驻章节各出现一次且位置合法(T019,改后判据)

```
templates/instructions-template.md:1
.specify/instructions.md:1
--- four anchor line numbers (must strictly increase) ---
66:## Token Efficiency Discipline
74:## User-Facing Comprehension
86:## Fast Fail Discipline
100:## Dogfooding Practice
template H2 = 19   live H2 = 20
pointer lines in template = 1
--- existing position pins test_c7 / test_c8 (real node ids) ---
tests/contract/test_user_facing_comprehension_section.py::test_c7_pinned_position_window_is_undisturbed PASSED
tests/contract/test_user_facing_comprehension_section.py::test_c8_section_sits_after_token_efficiency_and_before_dogfooding PASSED
2 passed in 0.02s        (pytest exit code 0, captured without a pipe)
```

**判定**: 两处各 **1** ✓;四锚点行号 **66 < 74 < 86 < 100** 严格递增,且 `Fast Fail` 落在 `User-Facing Comprehension` 与 `Dogfooding Practice` 之间 ✓;节数 **19 / 20** ✓;指针行 **1** ✓;既有 `test_c7` / `test_c8` 两根位置钉子均 **passed** ✓ —— 与场景 2 的改后期望逐项相符。

> ⚠️ **本场景首次实跑时留下一条盲检,已订正**:初次记录里这一段印的是 `no tests ran in 0.01s`。原因是执行者凭记忆写了 `test_c7_three_sections_stay_contiguous` / `test_c8_new_section_strictly_between` 两个**不存在的** node id,pytest 收集到 0 个用例;而命令尾部接了 `| tail -2`,把 pytest 的非零退出码换成了 `tail` 的 0,于是"零个用例被跑"被写进了取证文件、看起来像一条通过记录。这正是 FF-2(输出形态与后续过滤不匹配)与 FF-4(命令可达范围小于命题范围)的合流形态。订正方式:先 `grep -nE '^def test_c(7|8)'` 取真名,再不带管道实跑以取到真实退出码。教训已记入 T062 的候选:**取证命令 MUST NOT 把 pytest 接在管道之后取退出码**,且 node id MUST 由 grep 取真而非凭记忆书写。
---

## 场景 3 — 宪章双落点与四钉同批上调(T027,改后判据)

```
template principles = 14
live principles     = 16
MUST include entries = 8
304:**Version**: 1.13.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-09-23
--- double-landing title count on both sides (expect 1 / 1) ---
templates/constitution-template.md:1
templates/commands/constitution.md:1
--- four pins ---
66:TEMPLATE_COUNT = 14     # 11 pre-existing + 2 (Feature 051) + 1 landed here (Feature 052)
67:LIVE_COUNT = 16         # 14 pre-existing + 1 (XIV already carries STR-006) + 1 (XVI landed here)
68:COMMAND_COUNT = 8       # 5 pre-existing + 2 (Feature 051) + 1 landed here (Feature 052)
69:MIN_VERSION = (1, 13)   # floor semantics, never an equality pin
--- over-100-char lines in the new template principle block ---
over-100-char lines: 0
--- plan-template.md zero change vs frozen BASE_SHA ---
(empty above = zero change)
--- downstream gate rows rendered by the dynamic enumeration (expect 16, and 15 without XVI) ---
1 passed, 104 deselected in 0.03s
```

```
test_constitution_double_landing.py exit=0 (captured without a pipe)
...................                                                      [100%]
19 passed in 0.03s
```

**判定**: 模板原则 **14** ✓;活动宪章原则 **16** ✓;命令 `MUST include` **8** ✓;版本 **1.13.0** ✓;双落点标题两处各 **1**(逐字一致)✓;新原则块超长行 **0** ✓;`plan-template.md` 对冻结 BASE_SHA 的 `git diff --stat` **为空**(零改动)✓,而 C-18 实测其动态枚举渲染出的门控行数为 **16**、去掉 XVI 后为 **15** ✓;`test_constitution_double_landing.py` **19 passed / exit 0**(退出码不经管道捕获)✓ —— 与场景 3 的改后期望逐项相符。

> ⚠️ 版本行号已由 `:254` 后移,因为 T022 在文件顶部**前置**了一份新的 Sync Impact Report 注释块(051 的原块逐字保留在其下方,含其仍未关闭的 Follow-up TODOs)。场景 3 的期望只钉版本号不钉行号,故不受影响。
---

## 场景 5 — 注入子句:一份拥有者、多份字节相等的副本(T038,改后判据)

```
owner delimiter pairs   = 1
agents/skill-verifier.agent.md:1
agents/structure-adjuster.agent.md:1
owner lines/bytes: 6 801
agents/skill-verifier.agent.md byte-identical: True
agents/structure-adjuster.agent.md byte-identical: True
--- four per-tool trees (implementation-period correction: four, not three) ---
  .claude/agents/skill-verifier.md: exists=True byte-identical=True
  .claude/agents/structure-adjuster.md: exists=True byte-identical=True
  .qoder/agents/skill-verifier.agent.md: exists=True byte-identical=True
  .qoder/agents/structure-adjuster.agent.md: exists=True byte-identical=True
  .github/agents/skill-verifier.agent.md: exists=True byte-identical=True
  .github/agents/structure-adjuster.agent.md: exists=True byte-identical=True
  .opencode/agents/skill-verifier.md: exists=True byte-identical=True
  .opencode/agents/structure-adjuster.md: exists=True byte-identical=True
payload field rows = 6
MIRROR-OK skill-verifier
MIRROR-OK structure-adjuster
```


**判定**: 拥有者定界符 **1** 对;两份出厂预设各 **1** 对;`owner lines/bytes` = **6 / 801**(≤ 10 / ≤ 1200);两份预设与**四棵按工具树的全部 8 个副本**均 `byte-identical: True`;载荷字段行 **6**;两份镜像 `MIRROR-OK` —— 与场景 5 的改后期望逐项相符,且**四棵树**这一实现期订正已并入本场景的实跑输出。

---

## 场景 8 — 观察标记可检索,且真实存据未被污染(T043,改后判据)

```
# 一次性 workspace(/tmp/ffdrill)内 record → list
  "count_since_submission": 1,
  "threshold": 10,
  "should_prompt": false
{
  "count": 1,
  "matches": [
    {
      "id": "20260923T101127Z-speckit-plan",
# 真实存据(按标记过滤)——反空真哨兵
{
  "count": 0,
  "matches": []
}
ls: cannot access '/tmp/ffdrill': No such file or directory
[exit=0]
```

**判定**: 一次性根内 `record` 返回 `id` 与 `path`、`list` 得 `count: 1`(≥1)✓;**真实存据仍为 `{"count": 0, "matches": []}`** ✓ —— 这是本场景的反空真哨兵:它证明"隔离生效"而不是"查询本身读空了";`rm -rf` 后目录不存在 ✓;exit **0** ✓。命令块由 `quickstart.md` 逐字提取执行,未重打。

> ⚠️ 本场景 MUST NOT 用 `--action cleanup` 清理未打包条目(该 action 要求 `--package`,`feedback-utils.py:1389` 会抛 `FeedbackError`),`--action dispose` 亦不适用(只翻元数据、不删文件)。改用 `--workspace-root` 一次性根,已实跑验证。

---

## 场景 4 与场景 9 — 门控预算中立 + 类 ⑪ 跨纪律登记(T053,改后判据)

### 场景 4(命令块由 quickstart.md 逐字提取执行)

```
blocking confirmation gates: 23
  destructive: 13
  governance_kept: 10
violations (reversible gates still blocking): 0
frozen: 23 live: 23 violations: 0
TOTAL-EQUAL
.                                                                        [100%]
1 passed in 0.35s
[exit=0]
```

### 场景 9(命令块由 quickstart.md 逐字提取执行)

```
106:| ⑪ | 失败如实报告 | `shared/guidelines/confirmation-gates.md`, `shared/guidelines/fast-fail.md` | — |
400:    assert len(deduped) == 9, (
1
1
.......................                                                  [100%]
23 passed in 0.36s
[exit=0]
```

**判定(场景 4)**: `total` = **23**(destructive 13 / governance_kept 10)、violations **0**;第二段实跑输出 `frozen: 23 live: 23 violations: 0` 与 **`TOTAL-EQUAL`**;`git diff --stat -- scripts/python/scan-confirmation-gates.py` **为空**;`test_c11_gate_scan_total_unchanged` **1 passed**;exit **0** ✓ —— 与改后期望逐项相符。

**判定(场景 9)**: 类 ⑪ 行的规则真源列**同时含** `shared/guidelines/confirmation-gates.md` 与 `shared/guidelines/fast-fail.md`(`:106`)✓;钉子 `len(deduped) == 9`(`:400`)✓;`fast-fail.md` 在该文件命中 **1** ✓;该行 `reader_baseline_override` 列仍为 `—`(命中 1)✓;`test_user_facing_comprehension_doc.py` **23 passed**(含 `test_c18a` 上限 2 未受影响)、exit **0** ✓。
---

## 场景 6 / 10 / 11 / 12 — 四条变异演练(T054 补记;首次执行见 T039 与 `red-first-evidence.md`)

### 场景 6

**期望**: 步骤 0 输出 `prompt bytes: <非零>`;步骤 1–4 依次为 **≥1 → 0 → `restored` 且 ≥1 → `No such file or directory`**;演练目录计数归零。

```
prompt bytes: 931
3
0
restored
3
ls: cannot access '/tmp/ffdrill': No such file or directory
[exit=0]
```

### 场景 10

**期望**: 四例依次为 **anomaly-halt / clean / incomplete / clean-or-incomplete 中判为 incomplete 者不得为 clean**;末行 `doc carries the rule: True`;`No such file or directory`。

```
有异常: anomaly-halt
无异常: clean
缺异常行: incomplete
行内提及: incomplete
doc carries the rule: True
ls: cannot access '/tmp/ffdrill': No such file or directory
[exit=0]
```

### 场景 11

**期望**: `next action: surface-to-user | allowed: True | forbidden: False`;三条 `doc names …: True`(FR-071 要求排除覆盖既有的**全部**失败规则,故三者都 MUST 被点名)。

```
next action: surface-to-user | allowed: True | forbidden: False
doc names '两振': True
doc names '派发失败': True
doc names '非并行': True
[exit=0]
```

### 场景 12

**期望**: 三行依次为 **True / False / False**(只有干净运行需要该显式陈述);`doc owns the literal: True`。

```
repairs=0 fails=0 -> explicit-statement-present: True
repairs=2 fails=0 -> explicit-statement-present: False
repairs=0 fails=1 -> explicit-statement-present: False
doc owns the literal: True
[exit=0]
```

