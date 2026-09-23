---
id: "20260922T101630Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "052-fast-fail-principle:requirements:addendum-1:20260922T101630Z"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "052-fast-fail-principle"
partial: false
created: "2026-09-22T10:16:30Z"
summary: "追加输入轮(收尾后到达的 scope addendum):用户要求重点关注子代理面,理由是子代理启动后不受控、须在启动时注入规则。按 user-input-protocol § Mid-Run Addendum Input 处理——落在上游工件 requirements.md 并重跑验证门一次,不新起调用。补一轮定向调研后核实用户判断成立且理由更硬:子代理提示派生自其 Agent 定义与派发载荷而"
introspection_ref: "introspection-20260923T120035Z#F-10"
---

## Review
追加输入轮(收尾后到达的 scope addendum):用户要求重点关注子代理面,理由是子代理启动后不受控、须在启动时注入规则。按 user-input-protocol § Mid-Run Addendum Input 处理——落在上游工件 requirements.md 并重跑验证门一次,不新起调用。补一轮定向调研后核实用户判断成立且理由更硬:子代理提示派生自其 Agent 定义与派发载荷而非编排者对话(subagent-definitions.md:13),团队上下文隔离规则另将「不传对话历史」定为有意屏障,故常驻层结构性到不了子代理;且六条既有纪律对「自己如何抵达子代理」全部零表述,派发期唯一的框架级 MUST 是可见性契约(管观测不管行为)。据此新增 User Story 4(P1)、FR-047–FR-062 一组、6 条边界情形、4 条 Key Entities、SC-011–SC-014 及测量源、STR-009/STR-010,并同步更新 Overview/现状锚点(新增一组 8 条)/差异表/FR-028 边界/Out of Scope/Assumptions;原 US4/US5 顺延为 US5/US6,交叉引用无残留。规格自 46 FR/10 SC/8 STR/5 故事 增至 62 FR/14 SC/10 STR/6 故事,仍零 [NEEDS CLARIFICATION]。词汇表增补 3 条(注入子句/派发前自检/异常回传行),冲突检测全过。

## Optimization Points
- 命令对「**收尾已完成之后**才到达的 scope addendum」没有明确规定。`.specify/shared/workflow/user-input-protocol.md` § Mid-Run Addendum Input 覆盖的是"步骤之间"到达的追加输入,处置是"在下一个工件写入点合并、验证门重跑一次";但当追加输入到达时收尾三件事(工件提交提示、词汇表增补、反馈记录)**都已经跑完**,流程里就不存在"下一个工件写入点"了。本轮我按类比裁定:重开上游工件 → 重跑验证门 → 重跑词汇表增补 → 反馈按新一轮记一条(独立 run_id),并在规格的 Clarifications 里留下可审计的结构变更清单。这套裁定是合理的,但它是**我推出来的,不是命令说的**——下一次换一个会话可能推出别的(比如重跑一次完整收尾、或干脆当作新调用)。建议:在 `## Feedback` 步或 Outline 末尾补一行,明确"收尾后到达的追加输入按 addendum 处理:重开上游工件、验证门重跑一次、收尾的三个副作用各按增量重跑一次而非整套重来,且不新起一次调用"。
- 追加输入触及了一个本命令**没有要求核查**的面:子代理派发。本轮之所以能写出真实的注入落点(三条派发通道)而不是我编的注册点,靠的是临时补了一轮定向调研;而 Outline 步骤 5.5 的"保留标识符检查"与 5.6 的"移植/集成输入卫生"都只覆盖标识符冲突与外部代码库,没有一条要求"当需求触及某个既有概念时,先找到那个概念的**拥有者文档**再落笔"。本例的拥有者文档是 `shared/definitions/subagent-definitions.md`,它的一句话(子代理提示"not from the orchestrator's conversation")直接决定了这条需求的形状——若没读到它,我会把注入写成"常驻层自动继承",而这在本框架里是**结构性错误**。建议:在步骤 5 增一条"概念拥有者核查"——需求若引入或约束某个已有框架概念(Subagent / Agent / Tool / Team / Feature / Probe 等),MUST 先定位 `shared/definitions/` 下的拥有者文档并据其定义落笔,MUST NOT 按训练知识中的通用含义写。
