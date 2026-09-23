---
id: "20260918T114151Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "051-user-facing-comprehension-implement-20260918-mvp"
scope: "local"
probe: "speckit-implement-wrapup"
kind: "internal"
slice: "commands"
feature: "051-user-facing-comprehension"
disposition: "processed"
partial: false
created: "2026-09-18T11:41:51Z"
summary: "MVP 范围(Phase 1 Setup + Phase 2 US1,13/63 任务)按用户预授权完成并提交(82d95e2d / d6100ef2 / 49f9746e / 8b25e24e)。落地真源文档 + 常驻章节 + 34 个结构契约用例,全量契约回归相对冻结基线零新增(26 == 26,comm -13 空),门控预算 23 不变且扫描器零改动,9 条 Completion Gate"
introspection_ref: "introspection-20260923T120035Z#F-05"
disposition_reason: "introspection:introspection-20260923T120035Z#F-05"
---

## Review
MVP 范围(Phase 1 Setup + Phase 2 US1,13/63 任务)按用户预授权完成并提交(82d95e2d / d6100ef2 / 49f9746e / 8b25e24e)。落地真源文档 + 常驻章节 + 34 个结构契约用例,全量契约回归相对冻结基线零新增(26 == 26,comm -13 空),门控预算 23 不变且扫描器零改动,9 条 Completion Gate 中 6 条通过、3 条失败项全部归因于本轮未开工的 US2–US5(GATE-5 50 条未闭合行、GATE-8 0/8 指针),特性状态如实保持 Planned 未推进。本轮最有价值的产出不是制品而是四次对自身守卫的证伪:三个测试侧缺陷(git diff 未跟踪盲区、C-3 空断言、C-14 与 C-18 按整节而非按列取路径)加一个由 SC-017 演练暴露的 C-11 瞄错树,四者同形——命令有输出,但输出不是关于该命题的。C-3 与 C-11 修好后各自以变异演练实测其能红。

## Optimization Points
- **Red-first 步骤应要求「能红」的演练证据,而不只是「为何绿」的解释。** 本特性 T005 行(经 B-12 订正后)要求执行者为每条改前即绿的条款写明绿因;我照做了,而六条中恰有一条(ambient-section C-11「今天所有指针都能解析」)绿的原因是**断言瞄准了错误的树**——它按框架源树 `shared/guidelines/` 校验指针目标,而指针文本与读者解析的是运行时副本 `.specify/shared/guidelines/`。解释绿因并不能检验该条款**能否**变红。命令的 Evidence-backed closure 门写的是「IDENTIFY 能证明该工作的命令 → RUN → READ → VERIFY 它确实证明了该断言」;对一个**守卫**而言,能证明它的命令是一次**变异**(把被守物弄坏),不是一次通过。建议在 red-first 步骤加一句:凡守卫对象是「投递窗口 / 漂移 / 缺失」这类**负面命题**的条款,取证 MUST 含一次使其变红的演练,否则「绿」与「空断言」不可区分。实测收益:该缺陷由 SC-017 规定的演练在 wrap-up 期暴露,而非在 T005;若在 T005 暴露,可省下一次已提交后的返工与两个补充提交。
- **跨 Phase 的「条款绿点」依赖没有任何机械检查。** discipline-doc C-18(b) 的绿点是 T012(US1),而满足它的工作被排在 T043(US5);在用户选定 MVP 范围(仅 Setup + US1)后,US1 的验收在本轮**结构性不可满足**。`validate-tasks.py` 校验 `blockedBy` 可解析性、ID 唯一性、`[P]` 并行安全与 story 标签位置,但**任务→任务**的依赖图表达不了**条款→任务**的绿点归属,故没有任何东西报警。建议:结构校验器增一条 WARN 级检查——对每个「把条款 X 转绿」的行,解析其契约文档中 X 的归属任务集,若其中任一任务所处 Phase 晚于本行,报「绿点跨阶段」。本例的临时处置是把 T043 的相应半前置执行,并在 T012/T043 两行**写明被推翻的前提**(而非静默改排期),该处置形态本身值得作为先例保留。
- **`git diff <sha>` 看不见未跟踪文件,是「本特性新增了什么」这类中途门禁的通用陷阱。** gate-neutrality C-5/C-6 原以 `git diff --name-only <BASE_SHA>` 取变更集,而本特性自己的制品在 Phase 边界提交前**全是未跟踪的**,于是两条条款在唯一能起作用的窗口内看不见自己要判的文件(一个新增的 `.sh` 会被静默放过)。修法是把 `git ls-files --others --exclude-standard` 并入变更集。命令的 Shell hygiene 小节已收有 `--stat` 行尾形态与 `&&` 链退出码两个陷阱,建议补第三个:**按 SHA 取「新增文件」时 MUST 并入未跟踪集**,否则提交前的窗口内该门禁空转。暴露它的是 C-5 自带的一条反空转哨兵——这条哨兵第一次运行就回本,值得作为「给负面命题配哨兵」的先例推广。
