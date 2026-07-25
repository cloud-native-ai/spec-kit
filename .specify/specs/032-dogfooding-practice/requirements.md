# Requirements Specification: Dogfooding Practice Adoption

**Requirement Branch**: `032-dogfooding-practice`  
**Created**: 2026-07-25  
**Status**: Draft (revised 2026-07-25: refocus on existing loops, no new machinery)  
**Input**: User description: "需要为 Spec Kit 框架和所有使用 Spec 框架的项目引入 Dogfooding 的理念…（Dogfooding 定义、三特征、反误区、典型场景）" + 修订指示："Dogfooding 的核心理念在于工具开发者与使用者联系紧密，甚至可能是同一人或团队，从而可以构建顺畅的反馈循环。当前框架中已包含多种类似的反馈循环，涵盖 Feedback 机制与任务记录。当前理念应聚焦于框架本身。Spec Kit 框架本身已具备这样的循环机制：任何使用 Spec Kit 框架的项目，都能帮助 Spec Kit 框架进行循环反馈和持续提升；同时，这些项目也可以基于 Spec Kit 框架提供的功能，构建自身项目的反馈循环。"

## Related Feature *(mandatory)*

**Feature ID**: 036  
**Feature Name**: Dogfooding Practice

## Overview

Dogfooding（吃自己的狗粮）的核心在于**工具开发者与使用者联系紧密（甚至同一人/团队），从而形成顺畅的"使用 → 反馈 → 迭代"循环**。Spec Kit 已经具备承载这一理念的全部循环机制（Feedback 机制、任务记录/verification、memory、history、review）——本需求**不新建任何循环机器**，而是把既存的两级循环显名化、打通并交付为可操作指引：

- **Loop A（框架级，已存在）**：Spec Kit 用 Spec Kit 开发自己；任何使用 Spec Kit 的项目在真实使用中产生的反馈，经既有 Feedback 机制（record → 阈值提示 → package → 手动提交安装源仓库）回流，帮助框架持续提升。
- **Loop B（项目级，能力已就绪）**：使用 Spec Kit 的项目可以复用框架提供的能力（feedback 引擎、memory、history、review、任务记录），为**自己的产品**构建同构的反馈循环。

交付物限于：治理原则显名（constitution）+ 下游可操作指引（instructions 模板节）。成功标准是两条循环真实可走通，而非新增系统。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 框架自用闭环（Spec Kit 用 Spec Kit 开发自己） (Priority: P1)

作为 Spec Kit 维护者，我在开发 Spec Kit 的每个新能力时，都使用 Spec Kit 自己的规格驱动工作流完成；真实使用中的摩擦点经**既有** Feedback 机制记录并回流迭代。治理原则将这一实践显名化，并要求偏离留档。

**Why this priority**: 框架若不自用，就无权要求下游采用；且这是唯一不依赖外部项目、可立即验证的切片。

**Independent Test**: constitution 含命名的 Dogfooding 原则（含自用与偏离留档条款）；抽查最近一个框架功能的规格产物齐全，且反馈存储中存在来源于真实使用的条目。

**Acceptance Scenarios**:

1. **Given** 治理原则已含 Dogfooding 条款, **When** 维护者启动新框架功能, **Then** 该功能经框架自身工作流推进，产物留存于规格目录。
2. **Given** 维护者真实使用框架遇到摩擦点, **When** 经既有 Feedback 机制记录, **Then** 条目落盘 `.specify/memory/feedback/` 且计入既有阈值提示循环。
3. **Given** 某功能确需绕过自用工作流, **When** 例外发生, **Then** 偏离原因被留档（spec 目录或 memory 治理文档）。

---

### User Story 2 - 下游项目反馈回流框架（Loop A 显名化） (Priority: P2)

作为使用 Spec Kit 的下游项目团队成员，我从项目内的指引中清楚知道：我在真实使用框架时产生的反馈（各命令/技能自动记录的优化点 + 我主动记录的摩擦点），会经既有链路（record → 阈值提示 → package → 手动提交）回流给框架开发者——我知道这条路径存在、如何触发、以及提交是手动且可选的。

**Why this priority**: 这是"所有使用 Spec 框架的项目帮助框架提升"的直接落点；机制已存在（Feature 028），缺的只是让使用者看见并走通。

**Independent Test**: 指引节含 Loop A 路径说明；按指引步骤在任一工作区完成一次 record → status → package 演练即走通全链路。

**Acceptance Scenarios**:

1. **Given** 项目经框架初始化或指令刷新, **When** 成员阅读指引, **Then** 能看到回流路径的触发方式与手动提交说明（含"零自动传输"红线）。
2. **Given** 成员按指引操作, **When** 执行 record 与 package 动作, **Then** 全链路走通且不需要任何本需求新增的机器。

---

### User Story 3 - 下游项目构建自身反馈循环（Loop B 指引） (Priority: P3)

作为下游项目负责人，我从指引中获得"用框架既有能力为自己的产品构建反馈循环"的做法：用 feedback 引擎记录本产品真实使用中的发现、用 memory/history 沉淀经验、在 review 节点复盘，从而把 Dogfooding 落到自己的产品上；指引同时给出反误区提示（形式化、回音室、反馈失效、过度理想化）与分阶段/场景裁剪建议。

**Why this priority**: 价值最大但依赖 Loop A 指引先立（同一指引节的进阶部分），且完全复用既有能力、无新机制。

**Independent Test**: 指引节含 Loop B 能力映射（能力 → 用途）与反误区清单；按指引可用 `--unit-id` 自定义来源为本产品记录一条发现。

**Acceptance Scenarios**:

1. **Given** 指引已送达, **When** 团队为自己的产品记录一条真实使用发现, **Then** 复用既有 feedback 引擎即可完成（自定义 unit-id 标识产品场景），无需新工具。
2. **Given** 产品形态不适合团队日常自用, **When** 团队应用指引, **Then** 指引提供场景裁剪建议（定期真实环境演练、代理用户群等）而非强制自用。

---

### Edge Cases

- **早期不成熟产品 / 不适合自用的产品形态**：指引须支持分阶段推进与场景裁剪，不得一刀切。
- **反馈只记不提**：Loop A 提交是手动可选的；指引须说明阈值提示的含义，避免"记录了以为已回流"的误解。
- **既有项目刷新冲突**：指引节并入既有项目时不得覆盖用户自定义内容。
- **例外豁免**：紧急修复等确需绕过自用工作流时，记录偏离而非伪造合规。
- **重复造轮子倾向**：任何"为 Dogfooding 新建记录/统计系统"的提议都违反本需求边界（见 FR-004）。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 框架 MUST 将 Dogfooding 确立为一条命名的治理原则，内容至少涵盖：核心理念（开发者与使用者紧密联系形成顺畅反馈循环）、两级循环（Loop A 框架级回流 / Loop B 项目级自建）、以及对既有循环机制的指认（Feedback 机制、任务记录等）。
- **FR-002**: Spec Kit 框架自身 MUST 践行该原则：功能演进经自有 SDD 工作流完成；确需偏离时 MUST 留档原因（spec 目录或 memory 治理文档，原则正文指明落点）。
- **FR-003**: 通过框架初始化的新项目和执行指令刷新的既有项目 MUST 获得 Dogfooding 指引节，内容 MUST 包含：(a) Loop A 回流路径的可操作说明（记录 → 阈值提示 → package → 手动提交，含零自动传输说明）；(b) Loop B 能力映射（feedback 引擎 / memory / history / review / 任务记录 → 各自在自建循环中的用途）；(c) 反误区清单与分阶段/场景裁剪建议。并入既有项目时 MUST 保留用户自定义内容。
- **FR-004**: 本需求 MUST 完全复用既有循环机制，MUST NOT 新建平行的记录、统计或提醒系统（不新增引擎动作、不新增命令步骤、不新增存储）；指引与原则只做显名化与路径指认。
- **FR-005**: Dogfooding 对下游项目 MUST 以建议性原则 + 指引的强度生效：不设阻断性门禁，不强制使用频次。

### Key Entities

- **Dogfooding 原则（Principle）**: 治理层文本（constitution 命名原则）：核心理念、两级循环、自用与偏离留档条款、建议性声明。
- **实践指引（Practice Guidance）**: instructions 模板中的指引节：Loop A 路径、Loop B 能力映射、反误区、分阶段/场景裁剪。
- **既有循环机制（referenced，不新建）**: Feedback 机制（Feature 028：条目/阈值/package/手动提交）、任务记录与 verification、memory（session/knowledge）、history、review——作为被指认的载体出现在原则与指引中。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 原则确立后，Spec Kit 框架自身启动的新功能开发中，100% 经自有规格驱动工作流完成或留有显式偏离记录。
- **SC-002**: 100% 的新初始化项目包含 Dogfooding 指引节；既有项目一次指令刷新即获得，且用户自定义内容零丢失。
- **SC-003**: Loop A 可走通：在任一工作区按指引步骤完成 record → status → package 全链路演练，一次通过、零新增工具。
- **SC-004**: 本需求交付零新增循环机器：feedback 引擎动作集、命令模板步骤集、存储布局相对实现前不变（仅新增治理/指引文本与测试）。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 框架仓库规格目录审计 + memory 偏离记录；按发布周期核对。
- **SC-002 Source**: 初始化/刷新产物抽检 + 刷新前后差异比对；每次框架发布回归时执行。
- **SC-003 Source**: quickstart.md 演练脚本步骤的手工执行记录（verification.md）。
- **SC-004 Source**: 实现前后 `feedback-utils.py --help` 动作清单、命令模板 diff、`.specify/memory/` 目录布局比对（verification.md 记录）。

## Assumptions

- **复用既有反馈机制**：Loop A 即 Feature 028 的既有链路；本需求不改动其行为，只在指引中显名。
- **"所有使用 Spec 框架的项目"** 解释为：新初始化项目 + 执行指令刷新的既有项目。
- **术语规范**：正式名词为 "Dogfooding"（"Dogfooded"、"Dogfoodding" 为常见误写变体）；"Spec Key" 为 "Spec Kit" 的听写变体。

## Clarifications

- Q: Dogfooding 对下游项目的约束强度（建议性 / 节点提醒 / 阻断门禁）？ → A: 建议性原则 + 评审节点提醒；不设阻断性门禁。（修订后进一步收敛为：建议性原则 + 指引，不新增任何节点步骤）

### Session 2026-07-25

- Q: Feature 绑定——新建 Feature 还是绑定既有 028 Feedback Mechanism？ → A: 新建 Feature 036 "Dogfooding Practice"，与 028 建立复用关联（028 作为发现记录与统计载体）。
- Q: SC-003/004 的"活跃开发周期"如何界定？ → A: 以相邻两次评审节点（/speckit.review）为界。（修订后该口径随 loop-health 移除而不再使用）
- 用户修订指示（2026-07-25）：理念聚焦框架本身；框架已具备两级循环（下游项目回流框架 + 下游项目自建循环），MUST 复用既有机制、不新建循环机器 → 移除原 FR-005/006 的引擎扩展与 review 步骤需求，改为 FR-003 指引显名 + FR-004 复用红线。
