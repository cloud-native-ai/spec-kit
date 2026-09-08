---
id: "20260907T093812Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "050-proactive-flow-trigger-requirements-20260907"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "050-proactive-flow-trigger"
partial: false
created: "2026-09-07T09:38:12Z"
summary: "本次运行完整走通 outline 全步骤并到达 wrap-up:分支编号推导正确(排除 slash-namespaced 远端分支,取 .specify/specs/ 最高 049 → 050);create-new-requirements.sh 一次成功且按提示先 Read 预创建文件再 Write;现状锚点 8 条全部经源码/脚本实测(含发现 _INSTRUCTIONS_FILE_MAP 声"
---

## Review
本次运行完整走通 outline 全步骤并到达 wrap-up:分支编号推导正确(排除 slash-namespaced 远端分支,取 .specify/specs/ 最高 049 → 050);create-new-requirements.sh 一次成功且按提示先 Read 预创建文件再 Write;现状锚点 8 条全部经源码/脚本实测(含发现 _INSTRUCTIONS_FILE_MAP 声明 6 条路径但 generate-instructions.sh 只生成 4 条的真实覆盖缺口,已落为 FR-003);house convention 对齐最近合入的 049(中文、Overview + 现状锚点 + 缺口表、Clarifications→Out of Scope→Assumptions 顺序);安全边界(破坏性永不晋升)在 FR-011 + SC-005 + Out of Scope 三处交叉锁定;glossary 富化 5 条经引擎 detect-conflict 全部无冲突后直写,validate 通过。3 个 NEEDS CLARIFICATION 均为高影响分叉(触发通道范围 / 评估证据预算 / 评估触发时机),已按上限收敛并转入 clarify。

## Optimization Points
- **Glossary 步骤只处理"变体→规范词"的同音修复,未处理"同词异义分化"(same-word-different-sense),而后者风险更高**:本次用户输入中的「埋点」「自省」都是项目词汇表里**已 confirmed 条目的语义词**——「埋点/插点」锚定 Feedback Probe(wrap-up 事实捕获点)、「自省」锚定 Feedback Introspection(需求 047,对已积累 feedback 条目的深加工)。但用户本次指的是**不同概念**(必经路径上的触发落点 / 对当前项目状态的判断)。命令的 `## Glossary` 步骤只指示"把记录的变体映射到规范词",若照做会把「自省」静默校正为 Feedback Introspection,从而把整份规格的语义锚定到一个既有特性上(误绑 Feature、误写现状锚点、误设 Out of Scope)。本次是靠主动通读词汇表发现的,不是靠步骤提示。建议在 `## Glossary` 步骤补一条**反向检查**:当用户输入中的词命中既有 canonical/variant 但**上下文语义与既有条目不符**时,MUST 视为分化而非变体——显式提交冲突、另立新规范词,MUST NOT 静默套用既有条目。此类分化的代价(整份规格语义错位)远高于同音错字。
- **step 5.5 的"Reserved identifier check"只查新标识符是否被占用,未查新标识符是否**语义误占**既有域**:本次核查确认 `PROACTIVE`/`AUTO_TRIGGER`/`SUGGEST*` 零占用可直接用,但同时发现 `should_prompt`/`resolve_threshold`/`SPECKIT_FEEDBACK_THRESHOLD` 属 feedback 域的既有阈值机制——本特性的"N 次晋升"与之同构。建议在该步骤补一句:发现**同构既有机制**时,MUST 在规格中显式声明复用还是新建(本次落为 FR-021 单引擎坍缩约束),否则 plan 阶段容易平行造第二套计数-阈值引擎。
