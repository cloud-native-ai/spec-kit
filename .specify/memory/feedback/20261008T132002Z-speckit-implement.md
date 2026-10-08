---
id: "20261008T132002Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "implement:20261008-spec054-longrun"
scope: "local"
probe: "speckit-implement-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-10-08T13:20:02Z"
summary: "spec 054 长跑实现全绿:31/31 任务、零 deferred、Completion Gate 5/5、SC-001..004 全 pass;六次阶段提交(3e673e16..d58a600e)均路径限定且 comm -13 空;五守卫文件 35 测试全绿,六个源侧变异演练全部闭环(其中一次演练自身假阴性被识别并按删除式重演——见第 1 条);镜像漂移零新增,quickstart 场景 3"
---

## Review
spec 054 长跑实现全绿:31/31 任务、零 deferred、Completion Gate 5/5、SC-001..004 全 pass;六次阶段提交(3e673e16..d58a600e)均路径限定且 comm -13 空;五守卫文件 35 测试全绿,六个源侧变异演练全部闭环(其中一次演练自身假阴性被识别并按删除式重演——见第 1 条);镜像漂移零新增,quickstart 场景 3 实跑入档。两条机制面发现如下。

## Optimization Points
- 1. [drill-form-blindness] 变异演练的「植错一字」字面执行会在子串断言上假阴性:本轮对 chain guard 的首次演练用了后缀追加式变异(`seat instantiation`→`seat instantiationz`),守卫**不红**——因为子串断言 `"seat instantiation" in text` 对后缀追加天然免疫;删除式变异(`…instantiatio`)才红。教训已写进本特性的 notes/red-first-evidence.md,但它对整个演练纪律成立:植错方向 MUST 选「标记丢失」形态(删除/改写),不能选「标记加长」形态;建议 improve-skills/improve-docs 侧把这条写进守卫演练的取证规范(现属 implement.md 的 Mutation-drill restore 段,该段只讲复原纪律,不讲植错方向的可检性)。
- 2. [substring-false-positive] 标记断言选词时 MUST 先 grep 现仓再定:本轮 T014 守卫的 test_c4 首版用 `"team-scope" in text` 断言 create-team SKILL.md,结果**红前偶然绿**——`team-scoped responsibility`(既有词)子串命中 `team-scope`。修法是换成新步骤专名 `seat instantiation`(现仓零出现)。模式化教训:守卫标记的合格判据 = 「现仓零出现 + 将随主题落地而出现」,断言词在写入守卫前 MUST 过一遍 grep;这比「红先确认」更早一步,能在守卫写歪时当场发现而不是在红先运行时。
