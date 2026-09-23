---
id: "20260923T063219Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "052-fast-fail-principle:analyze:20260923T063219Z"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "052-fast-fail-principle"
feature_id: "052"
partial: false
created: "2026-09-23T06:32:19Z"
summary: "本轮 /speckit.analyze 达成其声明目的:只读分析 Mode C 的 8 份制品(requirements / plan / research / data-model / quickstart / feature-ref / contracts×5 / tasks)+ 注册表 + 宪章,产出 54 条发现并完成 CRITICAL/HIGH 的独立验证波。全程零文件写入(唯一例外是本"
introspection_ref: "introspection-20260923T120035Z#F-06"
---

## Review
本轮 /speckit.analyze 达成其声明目的:只读分析 Mode C 的 8 份制品(requirements / plan / research / data-model / quickstart / feature-ref / contracts×5 / tasks)+ 注册表 + 宪章,产出 54 条发现并完成 CRITICAL/HIGH 的独立验证波。全程零文件写入(唯一例外是本反馈条目,命令明文许可)。

同作者条件成立(全部制品由本会话同一 agent 写成),故按 §4 把检测委托给 3 个新鲜上下文只读子代理,分工按命令自己给的三分法:(a) spec↔plan↔research 一致性、(b) plan↔contracts↔data-model↔tasks 覆盖、(c) Feature 链接 + 注册表 + 宪章对齐。三份简报都点名同作者条件、都给了传播面要求与 DO-NOT-FLAG 清单、都注入了本特性正在规定的 fast-fail 子句并要求显式异常回传行。三路共回传 54 条发现:2 CRITICAL / 8 HIGH / 34 MEDIUM / 10 LOW,并回传 5 条 ANOMALY(其中两条证伪了我简报里的前提)。

验证波按 §5.5 用**与检测方互不相交**的 6 个新鲜上下文只读子代理复核全部 10 条 CRITICAL/HIGH,每个验证方只拿到自己那一条(不见检测推理、不见其他发现),并被要求同时回传 evidence_supported 与 evidence_not_supported 两个边界字段。结果:**1 confirm / 8 downgrade / 1 reject,降级率 80%**。唯一维持 HIGH 的是 E-02(FR-013 上送极优先与 FR-014 两振升级被 feature-ref 映射到 discipline-doc C-10,而 C-10 正文五项都不含这两条,该文件自己的条款→FR 映射行也漏了 FR-014 ⇒ 内容会被 T007 写进真源文档但无任何条款断言,守卫对二者的缺失永久失明)。F-04 被 reject(其"缺少程度节"的指控被 FR-009 反证:FR-009 明令 MUST NOT 采用严重程度这类连续量,故 D-10 不设程度节是**要求**而非遗漏),移入 Unvalidated Findings 附录,未静默丢弃。

八次降级同一根因:检测方先定严重度、后补传播面,命令自己的"传播面为 none 则封顶 MEDIUM"规则没有参与定级。这一点已作为优化点上送,并写进报告的补救建议(收紧 §4 的传播面要求),没有把它当作检测准确来呈现。

高价值发现(全部经独立验证或机械复算):E-02(HIGH,守卫盲区);I-01(pytest -k 是子串匹配,三条核验行的表达式跨阶段过选,T011 的命令与它自己"C-18/C-19/C-22 仍红"的期望直接矛盾——验证方用既有 test_user_facing_comprehension_doc.py 实测 -k "c1" 选中 11 个含 c18a/c18b 的函数,-k "c2" 还选中 test_c7_rfc2119_keywords_present,证明匹配连 token 边界都不认);I-02(分区表行数相加为 108 而非 107,constitution-export C-23 被两行重复认领,与表内"唯一交集是 C-20"的自陈矛盾);I-03(T059 的自检只覆盖 3 行,而缺陷在其中 4 行,自检会以错误前提通过);F-13(第三个 Clarifications 会话标题被写成 `- ###` 列表项,对基于标题的计数不可见且时间序错乱,连带把 Session 1 的收尾记录孤立在 Session 3 之后,使一条日期化记录读起来像当前主张);E-05/E-06/E-07(SC-008 无尝试任务、SC-015 无聚合任务、SC-013 编排者侧由自带脚本自证);I-09(8 个文件 vs 14 条规则的单位漂移使 SC-010 在一种读法下构造性不可满足);B-01(comm -13 判据只检新增失败、不检守卫被删,是"过滤后集合为空"却无反空真哨兵,违反 plan.md 自己的要求);G-5(plan.md 声称 6 项上游缺陷已记入 features/052.md,实测该文件只有 5 项,3 项无处可寻);G-6(features/051.md 的反向交叉引用仍写着"MUST NOT 成为类 ⑪ 的第二规则真源",而 D-4 已批准登记,该处在 plan 轮之后从未更新)。

宪章对齐:15 行逐条独立复评,与 plan.md 的自评一致(14 Pass / 1 Partial,Partial 为 Principle IV 且其 Complexity Tracking 条目点名了被破坏的下游制品 tasks.md);Principle XV 的跨纪律改动经核验**未违反**可理解性纪律的封闭集与单一规则真源规则(未新增类、类 ⑤ 有两文件先例、override 上限 2 不受影响、canonical 指针行形态已要求);Principle IX 经核验通过(Out of Scope 拒绝全部机制形态,任务文件面只含文档/契约/测试);plan-template.md 零改动而下游门控自动多一行的主张经读模板 :33-46 核实为真。无宪章 CRITICAL。

Feature 链接:052 绑定高置信,索引行 / 详情文件 / 规格三处 ID·名称·Spec Path 一致,5 个被引用 Feature 全部存在,051 的反向交叉引用在场;状态按状态机正确停在 Planned(索引、详情、Status Tracking 标记三处一致)。发现的是**阶段记录**层面的缺陷(G-1 索引文件头日期陈旧、G-2 索引行无阶段注记、G-3 tasks 期 Feature 列表复审无记录、G-4 四轮产物均未 staged),不是绑定错误。

## Optimization Points
- **本轮验证波降级率 80%(10 送 → 1 confirm / 8 downgrade / 1 reject),八次降级同一个根因:检测方先定严重度、后补传播面,于是命令自己的传播面上限规则没有参与定级。** §4 明写"When the answer is none, severity is capped at MEDIUM",但检测简报的产出形态是"Severity 列 + 单独的 Propagation surface 列",两者并列而非派生——于是 F-01/E-01/I-01/F-02/F-03/F-05/F-06/E-05 全部先被标成 CRITICAL 或 HIGH,再由验证方按上限规则拉回 MEDIUM。建议把 §4 的产出顺序反过来:**先答传播面,再由传播面派生严重度**,并把"传播面为 none 者一律 ≤ MEDIUM"写成检测简报里的硬性第一步,而不是验证波的补救。这不是本轮独有的噪声:它让 8/10 的验证算力花在纠正定级而非发现缺陷上。
- **编排者写进检测简报的前提有两条被检测方证伪,而命令对简报前提没有任何核验要求。** ① 我在简报里写"requirements.md 有 3 个 Clarifications 会话",实测只有 2 个格式正确的 `### Session` 标题(第三个被写成了 `- ###` 列表项,故对任何基于标题的计数不可见);② 我写"分区表声称 107/107 且认领互不相交,请复核",而真实缺陷不在条款集合层(那一层确实 107/107),在**可执行命令层**(pytest `-k` 是子串匹配,印出的表达式跨阶段过选)。两条都被检测方正确地当作 anomaly 上送而没有吸收。命令对 tasks.md 的前提有"Premise verification"整节(每个计数前提都要重测并附命令),对**检测简报的前提**却无同类要求——而简报前提错了会让一整路检测瞄错方向。建议在 §4 的委托段补一句:简报中陈述的一切计数与结构前提 MUST 由编排者在派发前机械导出,MUST NOT 凭记忆写入;凡无法导出的,写成待检测方核实的开放问题而不是断言。
