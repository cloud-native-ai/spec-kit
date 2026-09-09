---
id: "20260907T115039Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "050-proactive-flow-trigger-requirements-20260907-clarify-pass"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "050-proactive-flow-trigger"
partial: false
created: "2026-09-07T11:50:39Z"
summary: "同一次 requirements 运行的第二阶段(step 7 澄清处理),故与首条记录分 run_id 独立留存。用户在会话内裁定三项 NEEDS CLARIFICATION(Q1=A 仅指令文件通道 / Q2=C 环境信息为主+按需升级探测 / Q3=B 每回合评估),并追加一条设计指示:把触发挂在既有 constitution 每回合合规分析之后。按 Input Sanity 对该指示做源码"
---

## Review
同一次 requirements 运行的第二阶段(step 7 澄清处理),故与首条记录分 run_id 独立留存。用户在会话内裁定三项 NEEDS CLARIFICATION(Q1=A 仅指令文件通道 / Q2=C 环境信息为主+按需升级探测 / Q3=B 每回合评估),并追加一条设计指示:把触发挂在既有 constitution 每回合合规分析之后。按 Input Sanity 对该指示做源码核实,结论为**部分成立**——每回合义务确存在(instructions-template Documentation Map L13 + 常驻指令 L22 + L90),但形式化逐原则 Constitution Check 门控是 plan 期(plan-template.md:31–33 + plan.md:63–66);据此收敛为只挂轻量义务,新增 FR-005b 顺序契约、SC-012、Edge Case 与 Out of Scope 双重设防。三项裁定另经耦合检查后以 FR-005a + Assumptions 显式记录相互依赖(Q3 的可负担性依赖 Q2 的近零默认预算)。落地后残留 marker 0、FR 23、SC 12、Acceptance Scenario 30、Edge Case 14,计数均经程序复核(首轮人工写的 29/12 两处计数有误,已修正为 30/8)。checklist 全项通过,唯一未决为 Related Feature 绑定(按设计移交 clarify)。

## Optimization Points
- **outline step 5.5 只核查"新标识符是否被占用",没有核查"用户断言的框架先例是否属实",而后者更能改变规格形状**:本次用户在澄清阶段追加指示"框架已有类似埋点,如 constitution 要求每个请求都分析处理"。实测结论是**部分成立**——每回合分析义务确实存在,但它是 Documentation Map 表尾的轻量常驻指令(「ALWAYS check the relevant document from the map above first」),而**形式化的逐原则 Constitution Check 门控是 plan 期的**(`plan-template.md:31–33` GATE + `/speckit.plan` 动态枚举)。若照用户表述直接写成"挂在 constitution 清单之后",实现极可能把 plan 期的昂贵枚举门控搬到每回合,直接违反 Principle IX 与 token 效率纪律。建议在 step 5.5 旁增设一条**用户断言先例核实**:当用户以"框架已有 X"为依据提出设计要求时,MUST 先定位 X 的真实实现位置与作用域(每回合 / 命令期 / plan 期),再据此写 FR;断言的部分成立要显式记入 Clarifications,而不是静默按用户措辞落笔。此类断言通常携带正确直觉 + 不精确作用域,直接采信的风险高于直接否定。
- **澄清答案之间的相互依赖需要被显式记录,否则会退化为三条独立约束**:本次 Q1=A(唯一通道)、Q2=C(默认近零证据预算)、Q3=B(每回合评估)单独看都合理,但 Q3 的可负担性**完全依赖** Q2 的默认预算——只做 Q3 而证据预算走探测,就是每回合跑脚本。规格已用 FR-005a 的"二者 MUST 作为一组约束同时落地"和 Assumptions 的相互依赖条目锁定。建议 clarify 落地时增加一步**裁定间的耦合检查**:逐项问"若只实现这一项、其余不变,代价是否失控",并把成立的耦合写成 FR 级约束而非仅 Assumptions 备注。
