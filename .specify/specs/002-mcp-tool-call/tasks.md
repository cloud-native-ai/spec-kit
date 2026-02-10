---

description: "Task list for MCP Tool Call Command"
---

# Tasks: MCP Tool Call Command

**Input**: Design documents from `.specify/specs/002-mcp-tool-call/`
**Prerequisites**: plan.md, requirements.md, data-model.md, contracts/, quickstart.md

**Tests**: 测试任务按宪章要求纳入（先写测试，确认失败后再实现）。

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 项目结构与基础模板准备

- [x] T001 创建命令代码目录与包占位 `src/specify_cli/commands/__init__.py`
- [x] T002 [P] 确认模板目录结构 `templates/` 与 `templates/commands/` 存在并可写
- [x] T003 [P] 添加模板同步/加载路径说明到 `src/specify_cli/__init__.py` 相关注释

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 所有用户故事共享的核心能力

- [x] T004 在 `templates/commands/mcpcall.md` 描述 MCP 工具记录加载/保存规则
- [x] T005 [P] 在 `templates/commands/mcpcall.md` 描述工具记录 schema 校验规则（使用 `contracts/mcptool-record.schema.json`）
- [x] T006 [P] 在 `templates/commands/mcpcall.md` 描述输入解析与默认值处理规则（使用 `contracts/mcpcall-input.schema.json`）
- [x] T007 在 `templates/commands/mcpcall.md` 描述 MCP 工具发现适配器（调用 refresh-tools.sh 或 MCP 客户端）
- [x] T008 [P] 在 `templates/commands/mcpcall.md` 描述交互式补全流程（server/description/params/returns）
- [x] T009 在 `templates/commands/mcpcall.md` 描述统一错误与提示输出

**Checkpoint**: 基础能力完成后才可进入用户故事实现

---

## Phase 3: User Story 1 - 选择并调用 MCP 工具 (Priority: P1) 🎯 MVP

**Goal**: 首次调用时可自动发现并补全工具信息，生成记录并执行调用

**Independent Test**: 通过 quickstart 场景 1 完成首次调用并生成记录

### Tests for User Story 1 (MANDATORY)

- [x] T010 [P] [US1] 在 `templates/commands/mcpcall.md` 明确 MCP 工具记录 schema 校验示例
- [x] T011 [P] [US1] 在 `templates/commands/mcpcall.md` 明确 mcpcall 输入 schema 校验示例
- [x] T012 [P] [US1] 在 `templates/commands/mcpcall.md` 明确首次调用 + 自动发现 + 记录生成流程验证

### Manual Verification for User Story 1

- [ ] T013 [US1] 手动验证：按 `quickstart.md` 场景 1 执行并记录结果在 `.specify/specs/002-mcp-tool-call/quickstart.md`

### Implementation for User Story 1

- [x] T014 [US1] 生成/更新 MCP 工具记录文件到 `.specify/memory/tools/<mcp tool name>.md`
- [x] T015 [US1] 组装调用参数并执行 MCP 工具调用在 `src/specify_cli/commands/mcpcall.py`
- [x] T016 [US1] 调用前展示工具信息并要求确认在 `src/specify_cli/commands/mcpcall.py`
- [x] T017 [US1] 调用结果输出与错误说明在 `src/specify_cli/commands/mcpcall.py`

**Checkpoint**: US1 可独立完成首次调用流程

---

## Phase 4: User Story 2 - 复用已有工具记录 (Priority: P2)

**Goal**: 已存在记录时跳过发现与补全，直接调用

**Independent Test**: 通过 quickstart 场景 2 完成复用调用

### Tests for User Story 2 (MANDATORY)

- [x] T018 [P] [US2] 在 `templates/commands/mcpcall.md` 明确复用已有记录调用流程验证
- [x] T019 [P] [US2] 在 `templates/commands/mcpcall.md` 明确记录缺失字段触发补全流程验证

### Manual Verification for User Story 2

- [ ] T020 [US2] 手动验证：按 `quickstart.md` 场景 2 和 3 执行并记录结果在 `.specify/specs/002-mcp-tool-call/quickstart.md`

### Implementation for User Story 2

- [x] T021 [US2] 在 `templates/commands/mcpcall.md` 描述读取现有记录并判定完整性规则
- [x] T022 [US2] 在 `templates/commands/mcpcall.md` 描述记录缺失字段触发补全并回写规则

**Checkpoint**: US2 可独立完成复用与修复流程

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: 文档与可维护性完善

- [x] T023 [P] 更新命令文档模板 `templates/commands/mcpcall.md` 与实际流程一致
- [x] T024 [P] 更新 MCP 工具模板示例 `templates/mcptool-template.md`（确保字段齐全）
- [ ] T025 [P] 更新 feature 文档引用 ` .specify/specs/002-mcp-tool-call/feature-ref.md`
- [ ] T026 运行 quickstart 全量验证并记录结果在 `.specify/specs/002-mcp-tool-call/quickstart.md`

---

## Dependencies & Execution Order

- Setup (Phase 1) → Foundational (Phase 2) → US1 → US2 → Polish
- US1 与 US2 均依赖 Foundational 完成

## Parallel Opportunities

- Phase 1 中 T002/T003 可并行
- Phase 2 中 T005/T006/T008 可并行
- US1 合约测试 T010/T011 可并行
- US2 集成测试 T018/T019 可并行

## Implementation Strategy

- MVP：完成 Phase 1 + Phase 2 + US1
- 增量：在 US1 稳定后完成 US2，再进入 Polish
