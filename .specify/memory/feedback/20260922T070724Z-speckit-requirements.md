---
id: "20260922T070724Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "052-fast-fail-principle:requirements:20260922T070724Z"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "052-fast-fail-principle"
disposition: "processed"
partial: false
created: "2026-09-22T07:07:24Z"
summary: "本轮 /speckit.requirements 达成其声明目的:把一份理念级用户输入(在全框架增加 fast fail 原则)蒸馏为两个可落地层(框架自身 / 下游项目)与 5 个独立可测的用户故事,产出 46 条 FR、10 条 SC(各带测量源)、8 条 Shared Strings、11 条边界情形,零 [NEEDS CLARIFICATION],质量检查清单除 Related Featu"
introspection_ref: "introspection-20260923T120035Z#F-10"
disposition_reason: "introspection:introspection-20260923T120035Z#F-10"
---

## Review
本轮 /speckit.requirements 达成其声明目的:把一份理念级用户输入(在全框架增加 fast fail 原则)蒸馏为两个可落地层(框架自身 / 下游项目)与 5 个独立可测的用户故事,产出 46 条 FR、10 条 SC(各带测量源)、8 条 Shared Strings、11 条边界情形,零 [NEEDS CLARIFICATION],质量检查清单除 Related Feature 按设计留待 clarify 外全绿。Overview 的现状锚点全部经源码逐条实测复核(十余处停止/上报点位、门控扫描器实跑 total、宪章双落点四个钉子、命名占用实测),一处引文行号偏差(one-source-of-truth.md 的 remove-the-copy 句实为 :51 而非 :49)在写入后即被自查订正。最关键的一次避免踩坑来自词汇表:门控预算整数余量为 0 使「设计规避」成为唯一可行处置,否则 FR-037 会写成扩大扫描器豁免集。

## Optimization Points
- Glossary 步只指向「入向变体校正」与「收尾术语增补」,从未指向把词汇表当作**约束事实源**来读。本轮两条决定性事实——门控预算整数余量为 0、以及房子对该约束的既定处置是「设计规避」而非扩大 POLICY_DOCS 豁免集——都来自词汇表既有条目(`门控预算整数余量`、`设计规避`),而我只因为顺带 grep 了 `门控` 才撞上它们。若漏掉,FR-037 会被写成「把新真源文档登记进 POLICY_DOCS」,与本仓两个已把余量用尽的契约测试直接冲突,而该错误要到 plan/implement 期才暴露。建议:`## Glossary` 步增一行,要求按本特性主题域对词汇表做一次**约束侧**读取(有哪些已登记的机械上限、既定处置、已命名的反模式),而不只是变体校正侧读取。
- Outline 步骤 5.4 写「sample the highest-numbered existing spec under `.specify/specs/`」,但未点名工件文件名。上游 spec-kit 约定是 `spec.md`,本仓工件是 `requirements.md`;我按 `spec.md` 探了一次,得到 ENOENT,多花一个来回。建议:在 5.4 中直接点名 `requirements.md`(或令其从模板名派生),使这次「房子约定窥探」本身不必先猜路径——按本特性自己的判据,这正是「命名路径上的 ENOENT = 前提被证伪」类。
