# Requirements Specification: Unify Command Handoffs

**Requirement Branch**: `001-unify-command-handoffs`  
**Created**: 2026-02-03  
**Status**: Draft  
**Input**: User description: "为spec-kit中的各个命令提供更明确和完善的指引，先在usage文档中记录各个命令直接的相互关系，然后在各个命令的实现文档中（templates/commands/*.md）根据这个相互关系添加前后的指引。比如在implement.md中记录了需要先执行/speckit.tasks命令，在plan.md中记录下一个命令应该是/speckit.tasks命令等等，当前已经有的frontmatter中的handoffs，在文档结尾的”Follow Up“或”Suggestion“等机制需要进行统一。"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - 快速判断下一步该跑什么命令 (Priority: P1)

作为 Spec Kit 的使用者（开发者/维护者），我希望在阅读 usage 指南与任一命令模板时，能够在不“猜流程”的情况下，明确：

- 这个命令通常在什么时候运行（前置条件）
- 运行完之后通常应该运行什么（后续命令）
- 哪些分支是可选的（例如：有歧义时走 clarify、有质量门槛时走 checklist）

**Why this priority**: 这是贯穿全流程的“导航能力”，直接影响使用者是否能顺利走通 spec → plan → tasks → implement。

**Independent Test**: 只通过阅读 docs/usage.md 与任一 templates/commands/*.md，即可明确该命令的典型前置/后续关系，并能给出“下一条命令建议”。

**Acceptance Scenarios**:

1. **Given** 我在 usage 文档中查看命令列表，**When** 我选择任意一个命令（例如 `/speckit.plan`），**Then** 我能看到该命令的前置条件与推荐后续命令（例如“下一步通常是 `/speckit.tasks`”）。
2. **Given** 我打开任一命令模板（例如 templates/commands/implement.md），**When** 我查找“前置/后续指引”区域，**Then** 我能看到清晰的一致格式说明（例如“前置：/speckit.tasks；后续：/speckit.review”）。

---

### User Story 2 - 统一 handoffs 与文末“下一步”机制 (Priority: P2)

作为 Spec Kit 的维护者，我希望命令模板的“交接/下一步”写法是一致的，以便：

- 所有命令模板都有同一种 frontmatter `handoffs` 结构
- 文档正文中不再混用 “Follow Up / Suggestion / Next Steps”等多套机制
- 后续新增/修改命令模板时有明确的写作约束

**Why this priority**: 不一致会造成使用者误解，也会让维护者在迭代模板时反复纠结写法与语义。

**Independent Test**: 仅通过检查 templates/commands/*.md 的 frontmatter 与统一的“下一步”章节标题/结构，即可判断是否一致。

**Acceptance Scenarios**:

1. **Given** 我检查任意命令模板的 YAML frontmatter，**When** 我定位到 `handoffs`，**Then** 我看到的结构、字段命名与缩进是统一且可读的。
2. **Given** 我检查任意命令模板正文末尾，**When** 我寻找后续动作建议，**Then** 我看到的是统一的章节名称与呈现方式，且与 `handoffs` 的意图一致。

---

### User Story 3 - 覆盖全量命令与分支路径 (Priority: P3)

作为 Spec Kit 的使用者，我希望除了核心主路径外，也能清楚知道：

- 可选/并行命令（例如 `/speckit.analyze`、`/speckit.research`）的介入点
- 返工环路（例如 requirements ↔ clarify）应如何表达

**Why this priority**: 实际使用中经常不是“一条直线走到底”，清晰的分支路径能减少卡顿与返工成本。

**Independent Test**: 在 usage 文档中可以找到所有命令的“常见前置/后续”，并能看出可选分支与环路。

**Acceptance Scenarios**:

1. **Given** 我想在任意阶段做一致性检查，**When** 我查阅 usage 或命令模板，**Then** 我能明确 `/speckit.analyze` 可在多个阶段运行，并知道分析后推荐的修复路径。
2. **Given** requirements 中存在歧义标记，**When** 我查阅 usage 或命令模板，**Then** 我能明确应该运行 `/speckit.clarify`，并在澄清完成后回到 requirements 或继续进入 `/speckit.plan`。

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- 某些命令是“严格只读”（例如 analyze），文档仍需要给出后续修复建议但不能暗示自动改文件。
- 命令可能被跳步执行（例如直接 implement），文档需要明确“推荐前置/缺失前置时的建议补救”。
- 某些命令具有可选分支（例如 checklist 为质量门槛；research 为缺信息时的补充），关系说明需要能表达“可选/条件触发”。
- 模板 frontmatter YAML 缩进不一致导致不可读/不可维护；需要建立统一格式以降低后续出错。

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: docs/usage.md MUST 明确记录各命令的直接相互关系，包括：核心主路径（feature → requirements → plan → tasks → implement → review）与可选分支（clarify、checklist、analyze、research 等）。
- **FR-002**: docs/usage.md MUST 提供一个可扫描的关系摘要（例如表格），使使用者能够从任意命令快速定位“常见前置/常见后续”。
- **FR-003**: 每个 templates/commands/*.md MUST 在 YAML frontmatter 中提供 `handoffs` 字段，且结构一致（同一组字段、统一缩进与语义）。
- **FR-004**: 每个 templates/commands/*.md MUST 在正文中以统一机制呈现“下一步/前置”指引（不再混用 Follow Up / Suggestion 等多个机制）。
- **FR-005**: 对于“严格只读”命令模板（例如 analyze），其后续指引 MUST 明确为“建议的下一条命令/人工操作”，而不是暗示自动修改文件。
- **FR-006**: 对于可能被跳步执行的命令模板（例如 implement），其指引 MUST 明确推荐前置命令（例如 tasks、checklist），并在缺失前置时提供补救建议。

### Assumptions

- 文档关系的“默认主路径”以 usage 中现有 Core Lifecycle 为准。
- `handoffs` 主要用于“推荐的下一步命令建议”，不要求它覆盖所有可能分支，但必须覆盖最常见路径与关键质量门槛。
- 本次工作范围只覆盖仓库内 docs/usage.md 与 templates/commands/*.md 的一致性与指引强化，不改变命令实际行为。

### Key Entities *(include if requirement involves data)*

- **Command**: Spec Kit 的一个 AI Agent 命令（例如 `/speckit.plan`），包含用途、前置条件与后续交接。
- **Handoff**: 一个命令在完成后推荐交接到的下一条命令（含简短意图说明）。
- **Usage Guide**: docs/usage.md 中的全局流程与关系摘要。
- **Command Template**: templates/commands/*.md 中每条命令的实现说明模板，包含统一的 `handoffs` 与“下一步”呈现。

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: docs/usage.md 中存在一份覆盖全部命令的关系摘要（每个命令至少包含“常见前置/常见后续”）。
- **SC-002**: templates/commands/*.md 全部文件都包含 `handoffs` frontmatter，且 YAML 结构一致（字段一致、缩进一致、可读）。
- **SC-003**: templates/commands/*.md 全部文件都使用同一种“下一步/交接”呈现机制；仓库内不再存在命令模板中的 `## Follow Up` 章节。
- **SC-004**: 对核心主路径命令（requirements/plan/tasks/implement）而言，文档明确指出的推荐后续命令与 usage 中的关系一致。

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
