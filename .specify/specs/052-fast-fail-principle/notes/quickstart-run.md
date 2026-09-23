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
