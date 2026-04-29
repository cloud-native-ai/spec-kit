# Requirements Specification: Deterministic Tool and Skill IDs

**Requirement Branch**: `005-tool-skill-ids`  
**Created**: 2026-03-10  
**Status**: Draft  
**Input**: User description: "为tools和skills增加唯一标识。如docs/skills/problems.md文档中所描述的，当前应用skill和tool的主要问题是”触发“，skill和tool都使用自然语言的模糊匹配方式进行触发，存在大量的不确定性。我希望在/speckit.tools和/speckit.skills命令中能够在调用对应的create-new-*.sh脚本后生成一个唯一标识（建议使用相对File path），这个唯一标识可以在随后的文档或对话中用来定位一个具体的tool或skill。"

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

### User Story 1 - 生成可精确引用的唯一标识 (Priority: P1)

作为使用 `/speckit.tools` 或 `/speckit.skills` 的用户，我希望在命令完成目标对象创建、发现或刷新后立即得到一个稳定且唯一的标识，以便后续不再依赖模糊自然语言来引用具体的 tool 或 skill。

**Why this priority**: 这是解决“该触发时未触发、误触发、选错对象”问题的最小关键能力，没有唯一标识时，后续所有引用仍然存在歧义。

**Independent Test**: 分别执行一次 `/speckit.tools` 与 `/speckit.skills` 创建或解析目标对象，系统在完成脚本调用后返回一个唯一标识，且该标识能唯一对应本次产物。

**Acceptance Scenarios**:

1. **Given** 用户通过 `/speckit.skills` 创建或整理一个 skill，**When** 命令完成目标对象的生成或解析，**Then** 系统返回该 skill 的唯一标识以及其对应的 canonical 路径。
2. **Given** 用户通过 `/speckit.tools` 解析或创建一个工具记录，**When** 命令完成目标对象的生成或解析，**Then** 系统返回该 tool 的唯一标识以及其对应的 canonical 路径。

---

### User Story 2 - 用唯一标识进行后续定位 (Priority: P2)

作为与 Agent 协作的用户，我希望在后续文档、规范或对话中直接引用唯一标识，让系统能够解析到同一个 tool 或 skill，而不是再次依赖模糊匹配。

**Why this priority**: 唯一标识的价值不在于“生成”，而在于“复用”。只有后续可解析，才能真正降低触发不确定性。

**Independent Test**: 在一次创建流程完成后，将生成的标识重新提供给后续命令或对话，系统能够无歧义地定位到相同对象。

**Acceptance Scenarios**:

1. **Given** 用户在文档或对话中提供先前返回的 tool 标识，**When** 系统需要定位目标工具，**Then** 系统应直接解析到同一条工具记录而不要求再次模糊搜索。
2. **Given** 用户在文档或对话中提供先前返回的 skill 标识，**When** 系统需要定位目标 skill，**Then** 系统应直接解析到同一 skill 目录或主文件而不要求再次模糊搜索。

---

### User Story 3 - 在模糊匹配与精确定位之间平滑切换 (Priority: P3)

作为使用 Spec Kit 的用户，我希望系统既保留自然语言发现能力，又在存在唯一标识时优先走精确定位路径，从而兼顾易用性与确定性。

**Why this priority**: 现有工作流已经依赖自然语言发现，新增唯一标识不应破坏旧体验，而应提供更高优先级的确定性入口。

**Independent Test**: 在未提供标识时系统仍可进行发现；在提供标识时系统跳过歧义消解并直接绑定目标对象。

**Acceptance Scenarios**:

1. **Given** 用户只提供自然语言描述而未提供唯一标识，**When** 系统执行 `/speckit.tools` 或 `/speckit.skills`，**Then** 系统仍可沿用现有发现流程。
2. **Given** 用户同时提供自然语言描述和唯一标识，**When** 两者存在冲突，**Then** 系统应优先提示标识与描述不一致，而不是静默选择任一对象。

---

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- 当生成的相对路径因重命名、移动或删除而失效时，系统应明确提示标识已失效，并引导用户重新解析或刷新对象。
- 当用户提供的标识与当前工作区无关、越界或指向非预期类型时，系统应拒绝使用该标识。
- 当历史 tool 或 skill 产物尚未包含唯一标识字段时，系统应在下一次读取或更新该对象时补齐，而不是要求一次性迁移全部历史内容。
- 当自然语言描述与唯一标识指向不同对象时，系统应中止自动继续并提示用户确认实际目标。

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: 系统 MUST 在 `/speckit.tools` 与 `/speckit.skills` 完成目标对象的创建、发现或刷新后，为目标 tool 或 skill 生成一个唯一标识。
- **FR-002**: 系统 MUST 将该唯一标识表示为对当前工作区稳定、可读且可比较的 canonical 字符串，并默认采用工作区相对路径形式。
- **FR-003**: 系统 MUST 在命令输出中同时展示唯一标识与其对应对象类型（tool 或 skill），确保用户可直接复制到后续文档或对话中使用。
- **FR-004**: 系统 MUST 允许后续工作流通过该唯一标识直接定位到同一个 tool 记录或 skill 主目录，而不依赖再次模糊匹配。
- **FR-005**: 系统 MUST 在提供唯一标识时优先使用精确定位流程，并仅在标识缺失、失效或无法解析时回退到现有自然语言发现流程。
- **FR-006**: 系统 MUST 在标识无法解析、类型不匹配、路径越界或指向已不存在对象时返回明确错误，并给出重新发现或刷新对象的引导。
- **FR-007**: 系统 MUST 在自然语言描述与唯一标识解析结果冲突时暂停自动继续，并要求用户确认以避免误绑定。
- **FR-008**: 系统 MUST 为 `/speckit.tools` 生成的工具记录持久化该唯一标识，使其能被后续命令、文档或会话重复使用。
- **FR-009**: 系统 MUST 为 `/speckit.skills` 生成的 skill 产物持久化该唯一标识，使其能被后续命令、文档或会话重复使用。
- **FR-010**: 系统 MUST 保持现有自然语言触发能力可用，确保没有唯一标识的用户仍能完成原有发现流程。
- **FR-011**: 系统 MUST 在读取历史 tool 或 skill 产物时支持补充唯一标识，而不要求用户一次性手动更新所有历史文件。
- **FR-012**: 系统 MUST 确保同一工作区内不存在两个不同对象共享同一个 canonical 唯一标识。

### Key Entities *(include if requirement involves data)*

- **唯一标识（Resource ID）**: 用于唯一定位一个 tool 或 skill 的 canonical 标识字符串，默认以工作区相对路径表达，可在命令输出、文档与对话中复用。
- **Tool 记录（Tool Record）**: 由 `/speckit.tools` 生成或维护的目标对象，包含工具元数据、来源信息以及对应唯一标识。
- **Skill 产物（Skill Artifact）**: 由 `/speckit.skills` 创建或整理的目标对象，至少包含 skill 主目录与 `SKILL.md`，并带有对应唯一标识。
- **定位请求（Resolution Request）**: 后续命令、文档或对话对某个 tool 或 skill 的引用动作，可使用唯一标识或自然语言描述发起。

### Assumptions

- 默认以工作区相对路径作为唯一标识的 canonical 形式，例如指向 tool 记录文件或 skill 主目录/主文件的稳定路径。
- 对历史对象的补齐采取渐进式策略：在对象被再次读取、更新或重写时补充唯一标识，而不是要求仓库立即全量迁移。
- 本次需求聚焦于 `/speckit.tools` 与 `/speckit.skills` 两个命令及其后续引用链路，不要求同时重构所有其他命令的定位方式。
- 若对象被移动或重命名，旧标识可视为失效标识，由系统提示重新解析，而非自动猜测新位置。

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 100% 由 `/speckit.tools` 或 `/speckit.skills` 新生成或更新的目标对象都返回且持久化一个唯一标识。
- **SC-002**: 在提供有效唯一标识的场景下，95% 的后续定位请求可在一次尝试内直接解析到目标对象，无需人工消歧。
- **SC-003**: 在同时存在自然语言描述与唯一标识的场景下，100% 的冲突请求都会在执行前被显式拦截并提示用户确认。
- **SC-004**: 在未提供唯一标识的场景下，现有 `/speckit.tools` 与 `/speckit.skills` 的自然语言发现流程仍保持可用，核心任务完成率不低于变更前基线。
- **SC-005**: 用户在后续文档或会话中复用先前返回标识时，90% 以上的引用无需补充额外上下文即可完成准确定位。

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
