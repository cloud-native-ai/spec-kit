---
id: "20260924T032340Z-speckit-clarify"
unit_id: "/speckit.clarify"
unit_type: "command"
run_id: "053-machine-decidable-artifacts-clarify-20260924"
scope: "local"
probe: "speckit-clarify-wrapup"
kind: "internal"
slice: "commands"
feature: "053-machine-decidable-artifacts"
partial: false
created: "2026-09-24T03:23:40Z"
summary: "Mode A run on 053 with same-author detection delegated to 3 fresh-context read-only scanners (12 taxonomy categories split 4/4/4, question budget 2/2/1, each brief carrying the fast-fail dispatch-inje"
---

## Review
Mode A run on 053 with same-author detection delegated to 3 fresh-context read-only scanners (12 taxonomy categories split 4/4/4, question budget 2/2/1, each brief carrying the fast-fail dispatch-injection clause and requiring an explicit anomaly line on return). 4 questions posed, all 4 ratified at the recommended option: create Feature 053 (Draft); reuse goal-utils' existing four EXIT_* meanings and give 'blocked' the measured-free code 5; freeze a name-level baseline for coverage accounting and block only newly-uncovered items; FR-003's form requirements bind new checkers only while FR-005's read-only invariant stays universal. 13 corrections landed in passing, 5 of them the spec's own false measured premises. Structure re-verified mechanically after integration: 48 FR / 12 SC contiguous with 0 document-order breaks, STR forward-dangling 0 and reverse-mismatch 0 (down from 7), 0 active markers, 7 H2 in template order, checklist 16/16 (was 15/16). Full-suite name-level regression against 052's frozen baseline: 65 failed / 2927 passed, comm -13 empty and both name files md5-identical, so zero new failures and the comparison is non-vacuous. Feature 053 registered with a detail file; 052's stale status marker repaired in a separate commit.

## Optimization Points
- 1. **建队列之前先做一次跨扫描器去重(命令未规定)。** 本命令把问题预算按分类组预分给被委托的扫描器(本轮 3 个,预算 2/2/1),却没有任何一步要求在把发现合成队列**之前**先去重。本轮 3 路回传共得 5 个候选问题,其中 2 个是**同一个问题被两个扫描器各自独立查到**(STR-007 与 `goal-utils.py:44-47` 的退出码冲突),队列因此折叠为 4 并空出一个槽位。建议把去重写成显式步骤,并要求把「独立收敛」**作为置信信号呈报**而不是静默合并——同一发现被两路独立命中是它成立的最强证据,应当写进问题的框定语里(本轮即如此措辞,用户据此一次批准)。
- 2. **机械可核的纠正 MUST 先于问题队列落地(命令的步骤序无此槽位)。** 本轮 17 项整合里有 **13 项是纠正而非裁定**,其中 **5 项是规格自身的假前提**。而有两项**对问题本身承重**:FR-027 的分母印「既有 52 个 spec」而实测是 **44** 个 spec 目录(52 是 `features.md` 的 `Total Features`,两个计数被混用),FR-028 的选项 A 建立在「10 份 `.yaml` 可解析其 operations」这一**不存在的形态**上。若先提问后纠正,就会拿一个假前提去消耗一个预算槽位,得到的裁定一落地即为 void。命令现有步骤序是「1 整合用户已给决策 → 2 生成队列」,中间没有「1.5 落地扫描器的纠正」;建议补上,并把判据写成:**任何出现在选项后果预览里的数值,MUST 在提问前已被编排者复跑核对**。
- 3. **子代理回传的实测值在成为选项文本之前 MUST 由编排者重新导出。** 3 个扫描器里有 **2 个**回传了承重的错误实测:① A 路称 10 份 `.yaml` 契约「全部是 OpenAPI」,实测是 **9 份 OpenAPI(39 个 path-operation)+ 1 份 `assertions[].id` 结构化断言(6 条)**,而后者文件名恰恰是 `.openapi.yaml`——A 路的判据是「无字面 `operations:` 键」,那是把 OpenAPI 的 operation 误当成一个键名(它们是 `paths:` 下的 HTTP 方法键);② C 路引用 `scripts/python/build-summary-input.py:41-44`,而该路径下**无此文件**(真身在 `skills/create-team/scripts/`)。两者都即将变成用户据以裁定的选项文本。规则真源 `shared/workflow/objective-analysis-gate.md` 的第 8 条只要求**派发前**把简报里的每个计数机械导出,对**回传后**如何处置只字未提——这是一个单向的规则,缺口在入站方向。
