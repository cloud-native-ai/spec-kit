# Tasks: Speckit Agents Command

**Input**: Design documents from `/storage/project/cloud-native-ai/spec-kit/.specify/specs/003-speckit-agents-command/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/agents-command.openapi.yaml, quickstart.md

**Tests**: 本次未收到额外 TDD/自动化测试要求；以下以可独立验收的实现与手动验证任务为主。

**Organization**: Tasks are grouped by user story to enable independent implementation and validation.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 对齐 `/speckit.agents` 的命令骨架、提示入口与文档锚点。

- [X] T001 对齐命令模板元信息与执行入口 in templates/commands/agents.md
- [X] T002 对齐命令提示词总入口与参数语义 in .github/prompts/speckit.agents.prompt.md
- [X] T003 [P] 补齐 `/speckit.agents` 的使用说明入口 in docs/usage.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 建立所有用户故事共享的约束与校验规则（必须先完成）。

- [X] T004 定义 agent 文件命名与存储规则（kebab-case + `.github/agents/*.agent.md`） in .github/prompts/speckit.agents.prompt.md
- [X] T005 [P] 定义 approved providers 白名单与拒绝策略 in .github/prompts/speckit.agents.prompt.md
- [X] T006 [P] 定义 least-privilege 默认工具推导规则 in .github/prompts/speckit.agents.prompt.md
- [X] T007 定义冲突约束解析优先级与中止条件 in .github/prompts/speckit.agents.prompt.md
- [X] T008 定义写入前 YAML/frontmatter 校验闸门 in .github/prompts/speckit.agents.prompt.md
- [X] T009 对齐共享契约字段（create/update/infer/validate） in .specify/specs/003-speckit-agents-command/contracts/agents-command.openapi.yaml

**Checkpoint**: Foundation ready - US1/US2/US3 can start.

---

## Phase 3: User Story 1 - Create Custom AI Agent (Priority: P1) 🎯 MVP

**Goal**: 支持创建新的 `.agent.md`，含有参创建与无参推断创建流程。

**Independent Test**: 提供一句明确 intent 或无参高置信上下文，能够在 `.github/agents/` 生成合法 frontmatter 的 agent 文件；低置信无参时会中止并请求一句 intent。

### Implementation for User Story 1

- [X] T010 [US1] 实现“有参创建”步骤（角色、职责、工作流、输出格式） in .github/prompts/speckit.agents.prompt.md
- [X] T011 [US1] 实现“无参推断创建”高置信分支 in .github/prompts/speckit.agents.prompt.md
- [X] T012 [US1] 实现“无参低置信中止并请求一句 intent”分支 in .github/prompts/speckit.agents.prompt.md
- [X] T013 [P] [US1] 生成内容模板中加入 frontmatter 必填项与示例 prompts in templates/commands/agents.md
- [X] T014 [US1] 对齐 Create/Infer 语义与响应约束 in .specify/specs/003-speckit-agents-command/contracts/agents-command.openapi.yaml
- [X] T015 [US1] 增补 US1 验证步骤（创建成功/低置信中止） in .specify/specs/003-speckit-agents-command/quickstart.md
- [X] T016 [US1] 手动验收 US1 场景并记录结果 in .specify/specs/003-speckit-agents-command/quickstart.md

**Checkpoint**: US1 可独立演示并形成 MVP。

---

## Phase 4: User Story 2 - Update Existing AI Agent (Priority: P2)

**Goal**: 支持同名 agent 覆盖更新，并在冲突输入下按规则解析。

**Independent Test**: 对已有同名 agent 执行更新，文件被覆盖；显式输入与推断冲突时以最新显式输入优先，仍冲突则中止并提示修正。

### Implementation for User Story 2

- [X] T017 [P] [US2] 实现同名 agent 覆盖更新语义 in .github/prompts/speckit.agents.prompt.md
- [X] T018 [US2] 实现“显式输入优先于推断”的冲突解析规则 in .github/prompts/speckit.agents.prompt.md
- [X] T019 [US2] 实现“仍冲突则停止并要求修正”的异常分支 in .github/prompts/speckit.agents.prompt.md
- [X] T020 [US2] 对齐 Update/Overwrite 契约细节 in .specify/specs/003-speckit-agents-command/contracts/agents-command.openapi.yaml
- [X] T021 [US2] 更新数据模型生命周期（Saved→Updated 覆盖路径） in .specify/specs/003-speckit-agents-command/data-model.md
- [X] T022 [US2] 增补 US2 验证步骤（覆盖与冲突处理） in .specify/specs/003-speckit-agents-command/quickstart.md

**Checkpoint**: US2 可在不依赖 US3 的情况下独立验收。

---

## Phase 5: User Story 3 - Validate Agent Quality and Consistency (Priority: P3)

**Goal**: 写入前做质量校验，保障 YAML、provider、tools 与约束一致性。

**Independent Test**: 输入非法 YAML、未批准 provider、tools/workflow 不匹配等案例时，系统能阻止保存并返回明确错误。

### Implementation for User Story 3

- [X] T023 [P] [US3] 实现 YAML/frontmatter 语法校验失败即阻止保存 in .github/prompts/speckit.agents.prompt.md
- [X] T024 [P] [US3] 实现 provider 白名单校验失败即阻止保存 in .github/prompts/speckit.agents.prompt.md
- [X] T025 [US3] 实现 tools 与 workflow 一致性校验 in .github/prompts/speckit.agents.prompt.md
- [X] T026 [US3] 实现未指定 tools 时最小权限推导并写入 in .github/prompts/speckit.agents.prompt.md
- [X] T027 [US3] 对齐 Validate 合同错误返回结构 in .specify/specs/003-speckit-agents-command/contracts/agents-command.openapi.yaml
- [X] T028 [US3] 增补 US3 负向验证步骤（invalid YAML/provider/tools） in .specify/specs/003-speckit-agents-command/quickstart.md
- [X] T029 [US3] 手动验收 US3 校验场景并记录结果 in .specify/specs/003-speckit-agents-command/quickstart.md

**Checkpoint**: 三个用户故事均可独立验证，且质量闸门生效。

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 统一文档、feature 追踪与跨产物一致性收尾。

- [X] T030 [P] 同步规范与计划的最终行为描述 in .specify/specs/003-speckit-agents-command/requirements.md
- [X] T031 [P] 记录任务拆分后的关键变化与备注 in .specify/memory/features/019.md
- [X] T032 校验并同步 feature 索引状态与日期 in .specify/memory/features.md
- [X] T033 执行跨产物一致性复核（requirements/plan/data-model/contracts/tasks） in .specify/specs/003-speckit-agents-command/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 无依赖，可立即开始。
- **Phase 2 (Foundational)**: 依赖 Phase 1，且阻塞所有用户故事。
- **Phase 3/4/5 (US1/US2/US3)**: 均依赖 Phase 2 完成；按优先级建议先做 US1。
- **Phase 6 (Polish)**: 依赖所有目标用户故事完成。

### User Story Dependencies

- **US1 (P1)**: 仅依赖 Foundational，可独立交付 MVP。
- **US2 (P2)**: 依赖 Foundational；逻辑上复用 US1 产物，但可独立验收“更新/覆盖”能力。
- **US3 (P3)**: 依赖 Foundational；可独立验收“质量校验闸门”。

### Within Each User Story

- 先实现核心流程，再补齐 quickstart 验证步骤，最后执行手动验收记录。

## Parallel Opportunities

- **Setup**: T003 可与 T001/T002 并行。
- **Foundational**: T005 与 T006 可并行；完成后再做 T007/T008/T009。
- **US1**: T013 可与 T010/T011/T012 并行。
- **US2**: T017 可先并行开展，再串行收敛 T018/T019/T020。
- **US3**: T023 与 T024 可并行，随后执行 T025/T026/T027。
- **Polish**: T030 与 T031 可并行。

## Parallel Example: User Story 1

```bash
Task: "T010 [US1] 实现有参创建流程 in .github/prompts/speckit.agents.prompt.md"
Task: "T013 [P] [US1] 更新生成模板约束 in templates/commands/agents.md"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. 完成 Phase 1 与 Phase 2。
2. 完成 Phase 3（US1）。
3. 按 quickstart 执行 US1 独立验收并确认可演示。

### Incremental Delivery

1. 交付 US1（创建能力）作为 MVP。
2. 增量交付 US2（覆盖更新与冲突解析）。
3. 增量交付 US3（质量校验闸门）。
4. 最后完成 Phase 6 做一致性收尾。

### Team Parallel Strategy

1. 一名成员先完成 Phase 1/2 共享约束。
2. 其后并行分配：A 负责 US1，B 负责 US2，C 负责 US3。
3. 在 Phase 6 合并文档与 feature 跟踪更新。

## Notes

- 所有任务均遵循 `- [ ] Txxx [P] [USx] 描述 + 文件路径` 格式。
- `[P]` 仅用于不同文件或无未完成依赖的任务。
- 每个用户故事都包含独立验收标准，支持分阶段交付。
