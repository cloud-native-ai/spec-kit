---
id: "20260922T131753Z-speckit-clarify"
unit_id: "/speckit.clarify"
unit_type: "command"
run_id: "052-fast-fail-principle:clarify:20260922T131753Z"
scope: "local"
probe: "speckit-clarify-wrapup"
kind: "internal"
slice: "commands"
feature: "052-fast-fail-principle"
feature_id: "052"
partial: false
created: "2026-09-22T13:17:53Z"
summary: "Mode A(目标 requirements.md),可写性预探针先跑并通过(目录与文件均可写、touch-test 确认、owner agent:agent)。同作者条件成立——规格由本会话同一 agent 写成——故按 objective-analysis-gate 把覆盖扫描委托给 4 个新鲜上下文只读子代理,分工互不重叠(Feature 绑定与术语 / 功能范围与数据模型 / 交互·非功能"
introspection_ref: "introspection-20260923T120035Z#F-02"
---

## Review
Mode A(目标 requirements.md),可写性预探针先跑并通过(目录与文件均可写、touch-test 确认、owner agent:agent)。同作者条件成立——规格由本会话同一 agent 写成——故按 objective-analysis-gate 把覆盖扫描委托给 4 个新鲜上下文只读子代理,分工互不重叠(Feature 绑定与术语 / 功能范围与数据模型 / 交互·非功能·边界·取舍 / 现状锚点逐条重验),每个简报都点名同作者条件并要求「假定缺陷存在并定位它,不要报告制品是健全的」;四个简报均按本特性自己正在规定的形态注入了 fast-fail 子句并要求显式异常回传行(纪律落地前的自证)。

四路回传约 60 项发现,按「纠正 vs 裁定」分流:4 项经一次批量提问获用户裁定(Feature 绑定 = 新建 052 / Draft;派发前缺子句 = 按发现时点分流;通道二 = 绑定制作者要求而非枚举文件清单;清单 = 改双向并新增过度触发度量),约 30 项为纠正类已就地整合并在 Clarifications 以 C-1..C-22 表逐项披露,其余为非材料项(记录不改);其中 1 项经我复核为**检测方自身错误**(主张把上送件归入门控确认提示类,而该类会与「不新增门控」的裁定及门控预算零命中主张直接矛盾),不予采纳并在案记录理由。四路里有三路按要求回传了显式异常行,一路回传「no anomaly encountered」,无静默缺行。

最有价值的单条发现是**自指的**:规格自己要求真源文档写出相邻纪律的中文名「确认门控治理」,而该词逐字命中扫描器阻塞模式 确认门[禁控];新文档在 shared/ 下、不在豁免集、规格又禁止扩大豁免集,而预算整数余量为 0 且被两个契约测试钉成相等——照原文实现会直接打爆 CI。已改为以路径指称,并补两条约束(不得为躲模式而改语义;规避改写须触发一致性复跑并留痕),另把这份永久代价显式记为已接受。

另证伪一处既有房式措辞:「刷新项目指令即连同镜像副本一并恢复」经实测为假——generate-instructions.sh 全文无镜像同步调用,真实恢复路径是 CLI 的 copy_local_templates()(由 specify init 调用);已改写为真实路径并新增 FR-077 禁止常驻章节沿用该句式。还订正 fail-fast 占用面(初记 5 处、订正为权威源上 9 处且 3 处不指可写性探针)、三处引文的虚构粗体、若干行号与分母。

规格终态 78 FR / 15 SC / 13 STR / 19 key-entity 行 / 30 acceptance / 17 edge cases / 6 stories(4×P1+2×P2),FR 与 SC 均无缺号无悬挂引用,Related Feature 解析完成,注册表义务已履行(索引行、features/052.md、051 反向交叉引用、Total 51→52 且行数与声明总数一致),质量清单全绿。

本轮自查又抓出**两处自己的缺陷**,都是「写完没重算」:① 3 条 Shared Strings 定义而未被任何 [[STR-nnn]] 引用(死钉子),已接入 FR-016/017/054/067 并把引用检查改为双向;② 一个凭记忆写成 20、实为 19 的实体计数,同时污染了规格与 features/052.md 两个文件,已订正。另有一次引擎调用因反思正文含中文双引号被 shell 拆断而失败,经查无残留条目,改走 --review-file 重试成功——该形态问题已作为优化点上送,因其影响所有共享该步的命令。

## Optimization Points
- 命令对「检测回传一大堆发现时如何分流」没有规则。本轮 4 路委托检测回传约 60 项发现,而命令只给了两个约束:问题上限 5 个、以及"fact-vs-decision split——凡仓库能回答的不要问用户"。这两条不足以处理 60 项:我不得不自己发明第三条判据——**只有一种与已记录意图一致的读法的发现属纠正类,就地整合并在收尾逐项披露;只有真正存在多个可行读法的才成为问题**。没有这条,一次针对密集规格的 clarify 要么撑爆 5 问上限、要么静默丢掉发现(而静默丢掉正是本规格 052 要治理的失效)。建议在 `### Question Generation & Interactive Loop` 的约束列表里补一行,把"纠正类就地整合 + 披露、只有分叉才提问"写成命令的显式规则,并要求把纠正类逐项列表记入 Clarifications 会话条目(本轮的 C-1..C-22 表就是这个形态)。
- 命令的 Validation 步(第 5 步)只要求"无残留占位符、结构有效、术语一致",**没有要求重算集成时写进工件的任何计数**。本轮我凭记忆把 Key Entities 写成"13→20",实际是 19,且这个错数同时落进了规格与 `features/052.md` 两个文件;另外我新增了 3 条 Shared Strings 却没有任何 `[[STR-nnn]]` 引用它们(定义而未消费的死钉子)。两处都只因为我在写完后跑了一遍机械复核才发现——而"写完不重算"正是盲检类的成因之一。建议第 5 步增两条:(a) 集成写入的任何计数 MUST 由工件重新导出,不得沿用记忆或上一轮的值;(b) Shared Strings 的引用检查 MUST 双向跑(既查未解析的引用,也查定义而未被引用的行)。
- 两处上游拥有者文档缺陷在本轮被撞到,均不属 clarify 的修复范围,建议单独处置:① `.specify/shared/workflow/feature-integration.md` 的 `:58,68` 指向 `memory/feature-index.md`,该文件**不存在**(真实注册表是 `.specify/memory/features.md`),同文 `:33` 状态机与 `:68` 整合职责对"新建 Feature 应落什么状态"自相矛盾(本轮取更具体的状态机一方 = Draft);② `.specify/shared/definitions/agent-definitions.md:50` 称"seven shipped role agents",实测 `agents/*.agent.md` 只有 **2** 个。
- `## Feedback` 步给出的引擎调用形态是 `--review "<review prose>"`(内联),但**反思正文天然是含引号的散文**——本轮首次调用即因正文里的中文双引号被 shell 拆断而报 `unrecognized arguments`,整条记录未写入(经核实无残留条目)。这不是本命令独有的问题:该步由所有复杂命令共享(`shared/workflow/feedback-step.md` 是拥有者)。建议在拥有者文档里把 `--review-file` 定为散文反思的**默认**形态、内联 `--review` 只用于一句话摘要;引擎已支持 `--review-file`(`feedback-utils.py:150`),零代码改动。附带收益:走文件形态时正文里的引号、反引号、`$` 都不再需要转义,少一类静默截断。
