# Requirements Specification: Re-Anchoring（不忘初心 · 温故而知新）

**Requirement Branch**: `090-re-anchoring`
**Created**: 2026-11-08
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

**Input**: 用户裁定（逐字要点）：「将『开局加载一次』的动作，变成『每执行完一个核心步骤就再加载一次』，使用 session compact + reload + evaluation 来明确和最开始的方向是否存在偏差；在核心概念中针对 agent 加入『不忘初心：一直记得最开始的任务和规则』和『温故而知新：通过不断复习来强化记忆和回顾目标』」。后续纠正（逐字要点）：「回顾的重点应该是规则而不是目标，因为当前正在做和下一步要做就已经隐含了目标在内，经常会被遗漏的是规则；以『无人值守』被忽略而工作仍一步步推进为例。」

## Related Feature

**Feature ID**: 090
**Feature Name**: Re-Anchoring（不忘初心 · 温故而知新）

## Overview

长会话中规则会静默丢失：目标由当前/下一步隐含，而「无人值守」「不征求继续」「U4→下一阶段」「先写脊后行动」等规则一旦被丢弃，不再在任何动作里显形。本特性把「开局加载一次」改为**按核心步骤重载**：agent 在入口固化**任务锚 + 规则锚**，每完成一个核心步骤执行 compact → reload → evaluate，先问规则、后问任务，给出 `on-track` / `correction-applied` / `decision-needed` 三值判定。

## Functional Requirements

- **FR-001**: 框架 MUST 提供 Re-Anchoring 的唯一 owner 文档 `shared/definitions/re-anchoring-definitions.md`，拥有两个概念、重载分层与 agent 义务。
- **FR-002**: 宪法模板与本仓宪法 MUST 各新增一条 Re-Anchoring 原则，标题一致，正文以指针引用 owner 文档。
- **FR-003**: 指令模板与 `instructions.md` MUST 各新增一条常驻段（摘要 + owner 指针）。
- **FR-004**: 方向锚 MUST 同时包含任务锚（目标逐字、非目标、验收权威、阶段计划、裁定门）与**规则锚**（无人值守/不征求继续/U4→下一阶段/先写脊后行动/workspace guard/fast-fail/确认门/预算）。
- **FR-005**: 每个核心步骤后的五问 MUST **规则优先**：本步受哪些规则约束且是否仍生效 → 上一动作是否在规则下完成 → 下一步是否为计划命名的那一步 → 状态载体是否更新 → 领地/工作区签名是否干净。
- **FR-006**: 重载 MUST 分层：T0（方向锚摘要，每核心步骤）、T1（规则摘要，阶段边界/压缩后/子代理轮次上限后）、T2（全文，仅在派发形态不清或处置卡死时）；MUST NOT 每工具调用重载全文。
- **FR-007**: 审计结论是陈述，MUST NOT 以征求用户「继续」收尾；只有 `decision-needed` 上送。
- **FR-008**: `agent-definitions.md` MUST 声明 agent 侧义务：入口复述方向锚，核心步骤后先重读规则并记录五问判定；派发简报携带锚摘要。
- **FR-009**: `manage-constitution` 的 MUST include 清单 MUST 新增该原则条目。
- **FR-010**: 既有双落地/快失败计数 pin MUST 与新增原则同批移动，并有契约测试守护。

## Success Criteria

- **SC-001**: owner 文档、两侧宪法、两侧指令面、agent 条款五处同时存在且以指针互引（契约测试）。
- **SC-002**: 五问顺序在 checkpoint 协议中明确为「规则优先」，并有契约测试钉住。
- **SC-003**: 双落地计数与 watchlist 同批移动；`test_constitution_double_landing` 与 `test_fast_fail_discipline` 绿。
- **SC-004**: 方向审计的 T0/T1/T2 分层在 owner 文档与 checkpoint 协议中一致。

## Note

本特性的实现在本分支上**预先落地**（提交 `5a1041e4`、`55776937`（原 087 线，已重放到 090）），需求规格在 2026-11-08 从 086 中拆出（原编号 087，因远端占用重编号为 090）后建立；后续按 SDD 链补齐 clarify/plan/tasks 与 review。
