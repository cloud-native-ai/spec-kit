---
status: active
created: 2026-10-05
updated: 2026-10-06
---

# Goal: session-driven-self-improvement

## Objective

终态是框架中有一套 improve 流程,具体包含两个方面:主动触发(通过 improve 命令)与被动触发(通过运行判定的结果触发 feedback 流程)。

## Success Criteria

1. 一套新的运行判定,统一「token 消耗」「耗时」「正确性」与「满意度」四个量;其中「正确性」只涵盖**制品正确性**(名字级失败集差集为空,且每条返回绿的检查留有红先行取证或变异演练),语义正确性不在本判据内。
2. 本目标为长期目标,不设算出的终止判据:achieved 是一次刻意的人工判定,而非由度量得出的结论。

## History

- 2026-10-05 — created.
- 2026-10-05 — criteria changed; prior value: None provided.
- 2026-10-05 — criteria changed; prior value: token 消耗与耗时各定一个经验值作为目标,该值可随时调整。
- 2026-10-05 — objective changed; prior value: 目标达成时,使用 speckit 框架的代码项目会充分利用 Session 历史记录、用户输入以及大语言模型调查结论进行自我提升。自我提升分为两种情况:1. 与现有流程一致的被动或预制提升流程;2. 通过命令触发的主动自我提升。主动触发的 improve 流程需要经历三个步骤:1) why:当前的问题是什么(如 token 消耗过多、耗时过长、问题没有解决、用户不满意),即为什么要触发自我提升(通过 session 历史获取);2) what:需要进行哪些提升,分析哪些方面需要提升(被动触发的自我提升不能面面俱到,以免干扰当前流程,可以通过创建新的 spec 或者 todo 来记录,后面通过主动触发进行提升);3) how:该如何进行提升,分析问题、探索思路、实施改造。
- 2026-10-05 — criteria changed; prior value: token 消耗与耗时各定一个经验值作为目标,该值可随时调整。 | 用户满意度有一条判定逻辑(落在 instructions 文档中):用户输入延续之前话题且为否定式,大部分情况即为对结果不满意;用户换了话题或结束了 session,则视为结果被接受。每次判定产出一条改点信息,作为整个自我提升流程的一部分(观察 sensor),不单独作为一条 feedback。
- 2026-10-05 — objective changed; prior value: 终态是框架中有一套 improve 流程,具体包含两个方面:主动触发(通过 improve 命令)与被动触发(通过断言的结果触发 feedback 流程)。
- 2026-10-05 — criteria changed; prior value: 一套新的断言机制统一「token 消耗」「耗时」「正确性」与「满意度」四个量。
- 2026-10-06 — objective changed; prior value: 终态是框架中有一套 improve 流程,具体包含两个方面:主动触发(通过 improve 命令)与被动触发(通过判断逻辑的结果触发 feedback 流程)。
- 2026-10-06 — criteria changed; prior value: 一套新的判断逻辑,统一「token 消耗」「耗时」「正确性」与「满意度」四个量。
