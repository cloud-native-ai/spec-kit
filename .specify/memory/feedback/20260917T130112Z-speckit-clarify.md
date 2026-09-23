---
id: "20260917T130112Z-speckit-clarify"
unit_id: "/speckit.clarify"
unit_type: "command"
run_id: "051-user-facing-comprehension:2026-09-17:clarify-modeA"
scope: "local"
probe: "speckit-clarify-wrapup"
kind: "internal"
slice: "commands"
feature: "051-user-facing-comprehension"
disposition: "processed"
partial: false
created: "2026-09-17T13:01:12Z"
summary: "Mode A on requirements.md. 11 类 taxonomy 扫描:Feature Linkage = Missing(高优先),3 类 Partial、7 类 Clear。提问 4 个(5 上限内),因四者互不为对方选项集设前提,按 batching rule 合并为一次提示;四项均获批准推荐项。集成按「target artifact first, Feature regis"
introspection_ref: "introspection-20260923T120035Z#F-07"
disposition_reason: "introspection:introspection-20260923T120035Z#F-07"
---

## Review
Mode A on requirements.md. 11 类 taxonomy 扫描:Feature Linkage = Missing(高优先),3 类 Partial、7 类 Clear。提问 4 个(5 上限内),因四者互不为对方选项集设前提,按 batching rule 合并为一次提示;四项均获批准推荐项。集成按「target artifact first, Feature registry second」落地。两处先核实再当作提问前提的事实最有价值:① generate-instructions.sh 全文确实不同步 shared/(grep 无拷贝逻辑),把「指针可能悬空」的推测变成实测结构性发现,并据此把 Q4 的选项空间从「要不要修」改写为「修 vs 只加提示义务」;② update-feature-index.sh:150 确实是 cat > 整体重写、:164 表头只 6 列(缺活动索引实际使用的 Spec Path 列),与 AGENTS.md 声称的「计数由此脚本维护」矛盾 —— 按 One Source of Truth 的代码优先权威序与 Feature 049/050 既有记录改为手工编辑索引。Q3 是一个本该在 /speckit.requirements 就问却没问的问题:规格把「程度用定性上限还是裸数值」写成 Assumption 并用「若 /speckit.plan 判定…」把决策推迟给后续阶段而未标记为开放;本轮提交裁定,使其已知代价(门控提示与收尾报告无长度界)按集成规则绑定成文进 FR-011(知情接受 + 接受条件 + 升级路径),未停留在一行答案。机械核验三项:append-only 不变量(- Q: 行 2 → 6 严格递增)、FR/SC/STR 引用零悬空、FR 文档序连续性 —— 第三项抓到前两项放过的缺陷(新组插在既有组前使文档序成 035,037,038,036,ID 却完整)。产物已提交 777c1525,删除面审计干净。全量契约套件 24 failed / 1924 passed,经核验全部为既有基线或分支状态所致(23 条命中 049 冻结基线 47 条;第 24 条 test_review_prerequisite_flags_are_supported 仅因本分支尚无 plan.md 而失败,/speckit.plan 后自愈),9 个失败测试文件无一引用本轮改动的 4 个路径 ⇒ 零回归。

## Optimization Points
- # `/speckit.clarify` run optimization points — 051-user-facing-comprehension (2026-09-17, Mode A)
- ## Review
- Mode A,target `requirements.md`。11 个 taxonomy 类别扫描结果:Feature Linkage = Missing(高优先),其余 10 类中 3 类 Partial、7 类 Clear。提问 4 个(在 5 个上限内),因四者互不为对方的选项集设前提,按 batching rule 合并为一次提示而非逐问循环。四项均获用户批准推荐项。集成按「target artifact first, Feature registry second」的顺序落地并各自保存。
- 两处**先核实再当作提问前提**的事实,是本轮最有价值的动作:
- 1. `generate-instructions.sh` 全文**确实不同步 `shared/`**(grep 无任何 `shared` 拷贝逻辑)。这把"指针可能会悬空"的推测变成了实测的结构性发现,并因此把 Q4 的选项从"要不要修"改写成"修 vs 只加提示义务"——后者才是真实的决策空间。
- 2. `scripts/bash/update-feature-index.sh:150` **确实是 `cat > "$FEATURE_INDEX"` 整体重写**,且 `:164` 输出的表头只有 **6 列**(缺活动索引实际使用的 `Spec Path` 列)。这与 `AGENTS.md` 声称的"该计数由此脚本维护"直接矛盾。按 One Source of Truth 的权威顺序(**代码优先于文档**)与 Feature 049/050 的既有记录,改为手工编辑索引行与表头计数。
- Q3 是一个**本该在 `/speckit.requirements` 就问、却没问**的问题:规格把"程度用定性上限还是裸数值"写成了 Assumption,还用"若 `/speckit.plan` 判定某界面类确需数值上限…"的措辞把决策**推迟**给了后续阶段。本轮把它提交给用户,使一个未经批准的推断转为裁定,且其已知代价(门控提示与收尾报告无长度界)按集成规则**绑定成文**进 FR-011(知情接受 + 接受条件 + 升级路径),没有停留在"记了一行答案"。
- 机械核验做了三项而非靠眼看:append-only 不变量(`- Q:` 行 2 → 6,严格递增)、FR/SC/STR 引用零悬空(循环解析每个引用)、FR **文档序**连续性。第三项抓到了一个前两项都放过的缺陷:新 FR 组插在既有组之前,使文档序变成 035, 037, 038, 036——ID 完整、引用无悬空,但阅读序错乱。
- ## 优化点
- ### 1. Mode A 的 taxonomy 缺一个类别:「被上一阶段当作假设推迟的决策」
- 本轮 4 个问题**全部**来自 `/speckit.requirements` 写成 Assumption 的推断,而不是来自规格文本的显式空缺。其中 Q3 的 Assumption 甚至明写"若 `/speckit.plan` 判定…",即它把决策推给了后续阶段却**没有标记为开放**。
- 后果是:Mode A 的 `Misc / Placeholders` 类别扫描结果为 **Clear**(0 个 TODO 标记、无未量化形容词),因为一条写得好的 Assumption **看起来就像一个已解决项**。11 个类别里没有任何一个会去读 Assumptions 并问"这是裁定还是推断"。
- 建议 Mode A 增一个类别 **Deferred-by-assumption**:枚举 target artifact 的 Assumptions,标出满足以下任一条的条目——(a) 记录了在**具名替代方案之间**的选择;(b) 指名某个后续阶段为决策者;(c) 含"若…则升级路径是…"形态的推迟子句。这些是**穿着已决问题外衣的开放问题**。本轮 16 条 Assumption 中命中 1 条(Q3);假设更多的规格会产出更多。
- ### 2. FR 校验需要「文档序连续性」而不只是「ID 完整性」
- 集成规则要求新增/删除 FR 后保持编号连续,但**只查 ID 集合会漏掉插入位置错误**:本轮 ID 001–038 齐全、引用零悬空,文档序却是 035, 037, 038, 036,因为新组被插在既有组之前。
- 抓到它的是 `awk 'NR!=$1+0{print "ORDER BREAK"}'` 这类**按出现顺序**的断言。建议把它与 append-only 计数并列进 validation 步骤的机械检查——Mode A 集成经常新增 FR,而"ID 都在"给人一种已经校验过的错觉。
- 顺带:本轮据此把新 FR **追加到列表末尾**(FR-037/FR-038)而非插入中部,并在 FR-003/FR-005/FR-009/FR-014 加前向引用。这避免了上一轮遇到的整批重编号,代价是主题分组不再严格相邻——用组标题 `#### 读者基准与投递(clarify 第二轮裁定)` 标明来源作为补偿。
- ### 3. `AGENTS.md` 与代码在"谁维护 Total Features"上矛盾,且只能靠读邻行才发现
- `AGENTS.md` 的 Documentation Map 写着 Feature Index 的权威计数"由 `scripts/bash/update-feature-index.sh` 维护";实测该脚本是破坏性整体重写且会丢掉 `Spec Path` 列。Feature 049 与 050 都在**索引行的散文里**记录了这个 workaround。
- 本轮之所以没有踩坑,只因为我为了学格式读了 050 那一行。一次没有读邻行的 clarify 会直接运行脚本并摧毁索引——**这是活的危险,不是风格问题**。已在报告的 Documentation 步骤记为「需记录」并给出目标文件与要点,但**未在本轮修改**:它属框架源(`templates/instructions-template.md`,影响全部下游项目),与 Feature 051 无关,且 clarify 的 Behavior Rules 禁止改动 target 之外的工件。
- ## Token 消耗观察 (token-efficiency)
- 一处可避免的重复支出:为提取失败测试的**文件清单**,我在已跑过一次全量契约套件(1948 项 / 38s)之后又跑了一次全量,只为了 `grep '^FAILED'`。第一次运行时同趟管道接 `grep` 即可留存,第二次全量重跑是纯浪费。
- 上下文注入侧本轮是有界的:features.md 索引扫描用 `cut -c1-190` 截断、050 索引行只在需要学格式与查 workaround 时整读一次(该行约 10 KB,是格式与破坏性脚本警告的唯一载体,属"编辑目标/唯一来源"例外)、040.md 因需追加反向交叉引用而整读(52 行,编辑目标例外)。taxonomy 与 binding rules 两份文档为规则真源、整读属必要。
