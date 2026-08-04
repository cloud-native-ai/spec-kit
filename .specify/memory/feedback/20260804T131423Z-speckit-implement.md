---
id: "20260804T131423Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "036-team-summary-implement-phases5to9-20260804T211500Z"
scope: "local"
feature: "036-team-summary"
partial: false
created: "2026-08-04T13:14:23Z"
summary: "完成 036-team-summary 的 Phase 5-9(US3 累积 / US4 只读与出处 / US5 存量回填 / US6 goal 聚合 / Polish),119/120 任务闭环、1 项 deferred(T049),Feature 027 推进至 Implemented。达成命令声明目的:逐相推进、测试先行、每次闭环都以真实执行输出为证据,并以基线名单差集证明零回归。"
---

## Review
完成 036-team-summary 的 Phase 5-9(US3 累积 / US4 只读与出处 / US5 存量回填 / US6 goal 聚合 / Polish),119/120 任务闭环、1 项 deferred(T049),Feature 027 推进至 Implemented。达成命令声明目的:逐相推进、测试先行、每次闭环都以真实执行输出为证据,并以基线名单差集证明零回归。

证据规模:新增 201 个测试(5 个契约文件 + 5 个集成文件)全绿;每个相边界都做全量回归,`comm -13` 恒为空,失败名单始终 39 → 39,passed 1108 → 1309(+201,恰为新增数)。真实数据证据:4 个存量团队全部 `status=ready` / `missing_required=0`(基线 0/4);一次真实字节不变性审计对 5 组共 776 个文件取指纹,0 变更;三次连续真实刷新 md5 完全一致;真实 WBS 渲染出 SVG+PNG,深度≥2 节点 12 个,在 CG-6 阈值 15 之内。8 项 Completion Gate 全部按其自述命令对当前树重跑复核,而非采信任务勾选态。

两条只有真跑才会暴露的事实:(1) 两个团队各自发放的 `TI-0001` 会因 `entity_ids` 全局主键撞号(实测 exit 3),故聚合层必须按团队命名空间化 ID,该前缀顺带承载 FR-033 归属——纯推理几乎必然踩中;(2) continuous 团队的运行报告**不遵循**已文档化的 Report contract(实为 `# Cycle Report` + `**UTC**:`,无 Outcome),首次集成运行即因此失败;按 FR-025 不改写历史,改为兼容两种形态并回退到被强制的文件名时间戳,同时把不合规形态记为材料缺口。

三次"断言机制自身有缺陷"值得单独记:字符窗口邻近性启发式、按 `## ` 切分而 fenced 块内含同名标题、以及改错了文件位置(改 `## Goal` 正文而非 frontmatter `goal:`)。三次都判定为断言侧缺陷并改断言,未迁就坏断言去改正确的被测物——这一判定分叉如果做错,会主动破坏已正确的文档与实现。

T049 明确 deferred 而非硬闭:它需要在 report-only 档位真实跑一次 continuous 团队,preview→confirm 门禁按设计把该动作交给用户;门禁逻辑本身已落地并由 48 条断言钉住,故 SC-006 记 partial。SC-010 同理(程序化半边通过,人工读者核查未做)。13/15 SC pass,2 partial,0 unknown。

## Optimization Points
- 第 7 步的证据闭环规则很强,但缺一条"失败归属判定"分叉:测试转红时可能是被测物错,也可能是**断言自身写错**。本次三次红全部属后者(±900 字符邻近性窗口、按 `## ` 切分而 fenced 报告模板内含 `## Result Summary`、以及改了 `## Goal` 正文而非权威的 frontmatter `goal:`)。若机械照"红了就改被测物"执行,会把正确的文档结构和正确的实现改坏来迁就坏断言。建议补一句:测试转红 MUST 先判定失败归属(被测物 vs 断言),并在进度报告中说明改了哪一侧及理由。这条对 doc-feature 类特性尤其关键,因为结构性断言极易写成脆弱的文本启发式。
- 第 8 步的 Completion Gate 复核要求"按其自述 check 重跑",但没要求**门禁项本身要覆盖本次真实新增的风险面**。本次 tasks.md 初版只有 4 条 GATE,实施中我按发现补到 8 条(新增:被调技能零改动、既有 .specify/project 产物零改动、每个 goal 目录恒一份总结)。建议命令提示:实施期若发现新的不可回归属性,MUST 追加 GATE 行,而不是只在 verification.md 里叙述。
- 命令要求"phase-by-phase; complete each before next",但对**前置相已顺带落地后续相实质**(front-loading)只给了闭环方式,没给识别方式。本次 US3/US4 的多数断言在 US1 的生成器落地时就已满足,US6 的 T110-T112 亦然。我按"重新校验断言集 + 记录证据"闭环,但这是靠人判断的。建议补一句:进入新相时先跑该相测试,全绿即说明其实质已前置落地,按 front-loading 规则闭环并在报告中标注,不要重做。
- Long-Run Mode 只在用户显式要求时激活,但本次用户说"finish all left Phase"(一次性交付多相),既非单次也非显式 long-run。命令没有覆盖这个中间档,导致我自行决定"连续推进多相并在每相边界做回归+提交"。建议明确第三档:**多相连续模式**——每相边界强制回归 + 提交 + 进度报告,但不需要 long-run 的状态文件与停滞计数器。
- `.git/objects` 的 root 所有 bucket 阻塞提交这一坑已在 AGENTS.md 记载,但 `/speckit.implement` 的第 8 步"Commit gate"未提示它。本次在提交 US2 时撞上(4 个 bucket:5d/0a/75/9c),按记载的 remedy 修复(移开、以当前用户重建、拷回、`git fsck` 验证、blob 计数比对)。建议 Commit gate 补一句:提交失败且报 `insufficient permission for adding an object` 时,按 AGENTS.md 的 bucket remedy 处理,并以 `git fsck` 验证,不要改文件内容去规避哈希。
- token-efficiency: 全程未重读自己刚写的工件;所有验证走批量脚本一次性输出(FR/SC 覆盖、blockedBy 完整性、路径存在性、五组指纹、名单差集);勾选态每次从磁盘重读并回打计数,避免用过期上下文。可改进点:全量回归约 15-20s,本次跑了 8 次(每相边界 + 最终),其中 Phase 5/6 两次相邻边界之间没有跨相风险,可合并为一次;另外 US4 的测试直接 `cat >>` 追加到既有文件,虽省了一次全文重写,但也意味着我无法用 Edit 的精确匹配保护——追加式写入对"文件已被外部修改"的检测更弱,应权衡。
