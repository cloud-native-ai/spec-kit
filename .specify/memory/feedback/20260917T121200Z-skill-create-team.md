---
id: "20260917T121200Z-skill-create-team"
unit_id: "skill:create-team"
unit_type: "skill"
run_id: "20260917T115453Z-speckit-team-run-draw-two-layer-structure-7"
scope: "local"
probe: "skill-create-team-wrapup"
kind: "internal"
slice: "skills"
feature: "draw-two-layer-structure"
disposition: "processed"
partial: false
created: "2026-09-17T12:12:00Z"
summary: "run 模式第 7 次运行:落地用户五条 UX 要求。新建 skills/draw-diagram/references/delivery-contract.md(91 行)作为交付形态与面向用户文字规则的唯一 owner(D1 自足 HTML/D2 逐引擎源文件与渲染图保留表/D3 without jargon+with context 图内与正文同规/D4 MUST NOT 描述图表本身含图例"
introspection_ref: "introspection-20260923T120035Z#F-17"
disposition_reason: "introspection:introspection-20260923T120035Z#F-17"
---

## Review
run 模式第 7 次运行:落地用户五条 UX 要求。新建 skills/draw-diagram/references/delivery-contract.md(91 行)作为交付形态与面向用户文字规则的唯一 owner(D1 自足 HTML/D2 逐引擎源文件与渲染图保留表/D3 without jargon+with context 图内与正文同规/D4 MUST NOT 描述图表本身含图例式解说与视觉编码解释禁令/D5 用用户原始术语讲系统本身/D6 十项机械自检),补 draw-drawio 的交付形态(七家中唯一真缺口:此前无 HTML 入口),前门五处接线 + 其余五家各一条指针。自查发现并修掉两个自己的缺陷:①接线写成了内容副本(六家把 D4 禁用示例整串抄进去,改 D4 需动 8 个文件,违反 one-source-of-truth 机械判据)→ 七处全部收敛为指针形,四个签名短语在七家 SKILL.md 复测全 0;②我前几轮的零回归结论用了 -k 过滤子集的数字却当作整体基线陈述 → 改做真 A/B(git worktree add --detach HEAD 检出 e67f87c6,对同样 9 个失败文件跑,失败集 comm 求差):HEAD 23 failed / 当前 24 failed,差集仅 test_c10_runtime_copies_exist_for_every_present_tool 一项,归因为 7 月 22 日 git-ignored 试验目录 tmp/e2e-{md,toml}(当时 /speckit.docs 尚不存在故无同名副本;新 worktree 不复制 ignored 文件所以基线侧看不见;grep tests/ 0 命中即无测试创建它们)→ 本轮零回归。未派发 Worker(全部编辑落在 canonical 写入面,Meta 是唯一 canonical 写入者);S2/S3 仍未执行(渲染路径轴②用户裁定在另一流程)。

## Optimization Points
- # Run 7 优化点（skill:create-team — run 模式）
- 1. **run 模式的「零回归」结论缺一条口径纪律**：本轮暴露我把 `-k` 过滤子集的 `14 failed / 298 passed / 1636 deselected` 当作「契约套件」整体基线陈述，而全量跑是 `24 failed / 1924 passed`，两者不可比。建议 `create-team` 的 run 模式在 verification 环节明确要求：**回归结论必须同口径** —— 报告里的套件数字须注明是全量还是过滤子集（含 `-k` 表达式），过滤子集的数字不得当作整体基线陈述。
- 2. **独立验证应以 A/B 基线为默认手段，而不是以「与记忆中的数字相同」为手段**：本轮真正给出结论的是 `git worktree add --detach HEAD` + 失败集 `comm` 求差（23 vs 24，差集 1 项并逐项归因）。建议在 `verification: independent` 的语义里补一条：**当仓库存在长期既存失败时，独立验证的最小充分形式是「同口径 A/B 失败集求差 + 差集逐项归因」**，而非复述历史数字。
- 3. **worktree A/B 有一个必须披露的盲点：新建 worktree 不复制 git-ignored 文件**，因此由 ignored 残留（本例 `tmp/e2e-*`，7 月 22 日）造成的失败在基线侧不可见，会呈现为「只在工作树失败」的假回归。建议把这条写入 run 模式的验证注意事项：**差集项必须先排除 ignored-path 归因，再判定为回归**。
- 4. **「无复写/指针纪律」类检查必须以实际写入的短语为查询集**：本轮我的无复写检查查的是「我以为写了的短语」，产生假阴性并掩盖了一个真缺陷（六家 specialist 把 D4 的禁用示例整串抄成了内容副本）。建议 run 模式在验收 One-Source-Of-Truth 类约束时要求：**先从落盘产物中提取实际短语，再用这些短语做反向计数**，并附机械判据「改一个事实若需编辑多于 owner 一处即为副本」。
