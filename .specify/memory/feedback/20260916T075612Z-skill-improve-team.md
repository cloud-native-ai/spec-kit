---
id: "20260916T075612Z-skill-improve-team"
unit_id: "skill:improve-team"
unit_type: "skill"
run_id: "20260916T062500Z-improve-team-draw-two-layer-structure-s1-split"
scope: "local"
probe: "skill-improve-team-wrapup"
kind: "internal"
slice: "skills"
feature: "draw-two-layer-structure"
partial: false
created: "2026-09-16T07:56:12Z"
summary: "证据驱动的结构编辑:依据 run 2026-09-16T060815Z 的量化根因,把单 stage S1-refactor 拆为 S1a-S1e 五个 stage,并把交付粒度从逐文件改为目录级归属+例外清单。DAG 用程序校验(抽 workflow JSON → 悬空引用检查 → 拓扑排序判环 → write∩forbidden 求交),四项全过;拓扑序暴露 S1a 与 S1c 是并发根,原设"
introspection_ref: "introspection-20260923T120035Z#F-16"
---

## Review
证据驱动的结构编辑:依据 run 2026-09-16T060815Z 的量化根因,把单 stage S1-refactor 拆为 S1a-S1e 五个 stage,并把交付粒度从逐文件改为目录级归属+例外清单。DAG 用程序校验(抽 workflow JSON → 悬空引用检查 → 拓扑排序判环 → write∩forbidden 求交),四项全过;拓扑序暴露 S1a 与 S1c 是并发根,原设计误以为全链线性。仅改必要字段,goal.md/roster/pattern/config.summary 逐字节未动,旧产物保留不删并注明「不等于 S1a 已完成」。两点机制缺口:Refinement Map 无「stage 装不进单次派发预算」这一行(现有「Serial stage stalls」会把诊断误引向 blockedBy 边或 handoff 路径);归因量化必须可复算——我自己先把「产物条目数」当成「覆盖文件数」算错了 5-6 vs 12-14 次派发,靠确定性复核才纠正,已在 run report 留订正节未静默改数。

## Optimization Points
- # improve-team 运行优化点（draw-two-layer-structure 结构编辑，2026-09-16）
- **[Refinement Map 缺一行] 「stage 工作量超出单次派发预算」这个症状在 improve-team 的 Refinement Map 里没有对应条目。**
- 本次证据驱动的结构编辑处理的正是这个症状：run `2026-09-16T060815Z` 实测两次派发均撞 15 轮上限、
- 产物只覆盖目标的 13/162 文件，gate 判 FAIL。Refinement Map 现有 15 行覆盖的是「迭代不收敛」
- 「分数震荡」「并行文件冲突」「serial 阶段停滞（broken/missing handoff dependency）」「成员失效」
- 「缺角色」等，**没有一行**指向「stage 太大装不进一次派发」。而「Serial stage stalls」那一行会把
- 诊断引向 `blockedBy` 边或 handoff 文件路径——本次的真正根因既不是边错也不是路径错，
- 是 stage 粒度与派发预算不匹配。建议补一行：
- 症状「stage 反复撞派发轮次上限、产物只覆盖目标的一小部分」→ 原因「stage 交付粒度超出单次派发预算」
- → 编辑「按受影响文件/目录规模拆 stage，或把交付粒度从逐文件降为目录级 + 例外清单」。
- **[诊断陷阱] 「产物条目数」不等于「覆盖目标数」，本次我自己先踩了再纠正。**
- 首次归因时我把子代理产出的 80 条归属当成「覆盖了 mermaid 60 个文件」，据此算出「S1 需 5–6 次派发」；
- 确定性复核（`find` 出实际文件清单后逐个精确串匹配产物）显示只覆盖 13 个文件，真实需求是 12–14 次。
- 差因：那些条目多数是 `SKILL.md` 的**章节**标题而非文件路径。
- 这条教训对 improve-team 通用：**结构编辑的量化依据必须用确定性复核（实际清单 × 精确匹配）取得，
- 不能采信产物的条目计数**。本次已在 run report 里留了订正节与复核方法，未静默改数。
- 建议 Refinement Map 或 Behavior 步骤 3（attribute root cause）加一句提示：
- 归因所用的量化必须可复算，产物条目数不是覆盖度。
- ## 本次编辑做对的部分（非问题）
- 拆分后 DAG 用程序校验而非目测：抽出 workflow JSON → 悬空引用检查 → 拓扑排序判环 →
- `write ∩ forbidden` 求交，四项全过；拓扑序暴露出 `S1a` 与 `S1c` 是并发根（原设计误以为全链线性）。
- 未连带改动 goal.md、roster 的 role 级 blockedBy、pattern、config.summary —— 符合
- 「仅做必要的结构改动；未受影响的成员/字段保持逐字节不变」。
- 旧产物 `ownership-map.md` 保留不删，并在 progress 里写明「可作 S1a 输入素材，但不等于 S1a 已完成」，
- 避免下一次 run 把旧产物误当成 stage 已完成。
