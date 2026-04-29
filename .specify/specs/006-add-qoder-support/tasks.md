# Tasks: Add Qoder Support

**Requirement ID**: 006
**Requirement Key**: 006-add-qoder-support
**Related Feature**: 020 Qoder Support
**Input**: Design documents from `.specify/specs/006-add-qoder-support/`
**Prerequisites**: plan.md, requirements.md, research.md, data-model.md, contracts/qoder-support.openapi.yaml, quickstart.md

**Tests**: 为满足 requirements 中的独立验收标准以及合同/快速验证场景，自动化测试任务在每个用户故事中都作为必做项生成。

**Organization**: 任务按用户故事分组，确保每个故事都可以独立实现、独立测试和独立验收。

## Definition of Done (DoD)

- [ ] 变更满足 requirements.md 中对应的功能要求与边界条件
- [ ] 相关单元、集成、合同测试通过
- [ ] quickstart.md 中对应手工验证场景执行完成
- [ ] 用户可见文档、帮助文本与治理记录已同步更新
- [ ] 现有 Copilot/Qwen/opencode 行为未回归
- [ ] 成功标准 SC-001 ~ SC-005 有对应验证证据

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行执行（不同文件、无未完成前置依赖）
- **[Story]**: 对应的用户故事标签（如 `US1`、`US2`、`US3`）
- 每条任务都包含明确File path

## Path Conventions

- 单仓库 Python CLI：`src/`、`tests/`、`templates/`、`scripts/`、`docs/` 均位于仓库根目录
- 规格与设计产物位于 `.specify/specs/006-add-qoder-support/`
- Feature 跟踪位于 `.specify/memory/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 准备可复用的测试与审计支撑，减少后续用户故事重复搭建

- [X] T001 Create Qoder CLI bootstrap fixtures and temporary workspace helpers in tests/conftest.py
- [X] T002 [P] Add reusable CLI invocation helpers for init and refresh scenarios in tests/script_api.py
- [X] T003 [P] Create support-surface fixture definitions for Qoder audits in tests/unit/test_qoder_support_surfaces.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 先完成所有用户故事共享的治理、模板和矩阵前提

**⚠️ CRITICAL**: 本阶段完成前，不应开始任何用户故事实现

- [X] T004 Update approved assistant governance whitelist to include Qoder in .specify/memory/constitution.md
- [X] T005 [P] Align planning gate language with approved Qoder support in templates/plan-template.md
- [X] T006 [P] Align agent/provider whitelist guidance with Qoder in templates/commands/agents.md
- [X] T007 [P] Add shared assistant matrix invariants for Qoder support in tests/unit/test_qoder_support_matrix.py
- [X] T008 Record task-splitting notes and shared asset impact in .specify/memory/features/020.md

**Checkpoint**: 治理与共享支持矩阵已到位，用户故事可按优先级推进

---

## Phase 3: User Story 1 - 在初始化时选择 Qoder (Priority: P1) 🎯 MVP

**Goal**: 让用户在新项目和现有目录初始化时都能直接选择 Qoder，并立即得到可用资产

**Independent Test**: 运行一次 `specify init <dir> --ai qoder` 与一次 `specify init . --ai qoder`，确认生成 `.qoder/commands/` 且无需手工补文件

### Tests for User Story 1

- [X] T009 [P] [US1] Add contract coverage for supported-assistant listing and init request rules in tests/contract/test_qoder_init_contract.py
- [X] T010 [P] [US1] Add integration coverage for new-project and existing-directory Qoder bootstrap in tests/integration/test_qoder_init.py
- [X] T011 [P] [US1] Add unit coverage for Qoder bootstrap helper paths in tests/unit/test_qoder_bootstrap.py

### Manual Verification for User Story 1

- [ ] T012 [US1] Manual QA: validate Quickstart scenarios 1-2 in .specify/specs/006-add-qoder-support/quickstart.md

### Implementation for User Story 1

- [X] T013 [US1] Extend assistant metadata, `--ai` help text, CLI detection, and `check()` output for Qoder in src/specify_cli/__init__.py
- [X] T014 [US1] Generate `.qoder/commands/` assets during new-project and current-directory bootstrap in src/specify_cli/__init__.py

**Checkpoint**: User Story 1 完成后，Qoder 初始化主路径可独立演示并满足 MVP

---

## Phase 4: User Story 2 - 校验与更新现有 Qoder 项目 (Priority: P2)

**Goal**: 支持 Qoder CLI 缺失提示、忽略校验开关，以及对现有项目的非破坏性刷新

**Independent Test**: 在缺少 `qoder` CLI 时验证错误提示与 `--ignore-agent-tools` 绕过路径；在已有混合助手资产的目录中验证刷新不破坏其他助手文件

### Tests for User Story 2

- [X] T015 [P] [US2] Add contract coverage for Qoder validation and refresh behaviors in tests/contract/test_qoder_refresh_contract.py
- [X] T016 [P] [US2] Add integration coverage for missing-CLI guidance and non-destructive refresh in tests/integration/test_qoder_refresh.py
- [X] T017 [P] [US2] Add unit coverage for ignore-check and refresh helper behavior in tests/unit/test_qoder_refresh_helpers.py

### Manual Verification for User Story 2

- [ ] T018 [US2] Manual QA: validate Quickstart scenarios 3-5 in .specify/specs/006-add-qoder-support/quickstart.md

### Implementation for User Story 2

- [X] T019 [US2] Implement Qoder missing-CLI guidance and `--ignore-agent-tools` parity in src/specify_cli/__init__.py
- [X] T020 [US2] Extend Qoder compatibility link generation for refresh flows in scripts/bash/generate-instructions.sh
- [X] T021 [P] [US2] Align instruction generation template with approved Qoder support in templates/instructions-template.md
- [X] T022 [P] [US2] Document Qoder maintenance and refresh workflows in docs/usage.md

**Checkpoint**: User Story 2 完成后，Qoder 刷新与依赖校验路径可独立验证，且不会误伤其他助手资产

---

## Phase 5: User Story 3 - 文档与发布产物保持一致 (Priority: P3)

**Goal**: 统一 README、安装说明、指令内容与发布审计，使所有支持面一致展示 Qoder

**Independent Test**: 对候选发布执行文档与分发审计，确认帮助文本、README、安装文档、说明内容和打包资源都包含一致的 Qoder 支持信息

### Tests for User Story 3

- [X] T023 [P] [US3] Add contract coverage for support-surface and distribution audits in tests/contract/test_qoder_support_surfaces_contract.py
- [X] T024 [P] [US3] Add integration coverage for documentation and packaged resource consistency in tests/integration/test_qoder_distribution.py
- [X] T025 [P] [US3] Add unit coverage for support-surface audit rules in tests/unit/test_qoder_support_surfaces.py

### Manual Verification for User Story 3

- [ ] T026 [US3] Manual QA: validate Quickstart scenario 6 in .specify/specs/006-add-qoder-support/quickstart.md

### Implementation for User Story 3

- [X] T027 [US3] Update public support matrix and Qoder overview in README.md
- [X] T028 [P] [US3] Update installation examples and prerequisite guidance for Qoder in docs/installation.md
- [X] T029 [P] [US3] Regenerate supported-agent instruction content for Qoder in .ai/instructions.md
- [X] T030 [P] [US3] Align approved-provider guidance with Qoder in .github/prompts/speckit.agents.prompt.md
- [X] T031 [US3] Ensure packaged template resources continue shipping Qoder-facing assets via pyproject.toml

**Checkpoint**: 所有用户可见支持面和发布资源对 Qoder 的表述一致，可用于发布前验收

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 完成端到端验证、索引同步和最终审计

- [X] T032 [P] Regenerate compatibility links and Qoder project rules in scripts/bash/generate-instructions.sh
- [ ] T033 Run end-to-end Qoder quickstart validation and capture final audit notes in .specify/specs/006-add-qoder-support/quickstart.md
- [X] T034 [P] Refresh feature index timestamp while keeping Feature 020 status implemented in .specify/memory/features.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 无依赖，可立即开始
- **Phase 2 (Foundational)**: 依赖 Phase 1 完成；阻塞所有用户故事
- **Phase 3 (US1)**: 依赖 Phase 2；构成 MVP
- **Phase 4 (US2)**: 依赖 Phase 2，可在 US1 完成后顺序推进；若团队并行，也可在共享前置完成后并行实现
- **Phase 5 (US3)**: 依赖 Phase 2，建议在 US1/US2 代码路径稳定后推进
- **Phase 6 (Polish)**: 依赖目标用户故事全部完成

### User Story Dependencies

- **US1 (P1)**: 仅依赖 Foundational 阶段；无其他用户故事前置
- **US2 (P2)**: 依赖 US1 提供的 Qoder 基础接入能力
- **US3 (P3)**: 依赖 US1/US2 已确定最终的 Qoder 命名、安装地址和刷新行为

### Within Each User Story

- 先写合同/集成/单元测试任务，再实现代码与文档
- 先完成手工验证前的核心实现，再执行 quickstart 手工验收
- 同一文件的任务按顺序完成，避免冲突覆盖

### Parallel Opportunities

- Phase 1 中标记 `[P]` 的测试支撑任务可并行
- Phase 2 中模板与测试矩阵任务可并行
- 每个用户故事中的合同测试、集成测试、单元测试可以并行编写
- US3 中 README、安装文档、prompt/指令内容可分工并行

---

## Parallel Example: User Story 1

```bash
# 并行编写 US1 的自动化测试：
Task: "Add contract coverage for supported-assistant listing and init request rules in tests/contract/test_qoder_init_contract.py"
Task: "Add integration coverage for new-project and existing-directory Qoder bootstrap in tests/integration/test_qoder_init.py"
Task: "Add unit coverage for Qoder bootstrap helper paths in tests/unit/test_qoder_bootstrap.py"
```

---

## Parallel Example: User Story 3

```bash
# 并行处理 US3 的支持面更新：
Task: "Update installation examples and prerequisite guidance for Qoder in docs/installation.md"
Task: "Regenerate supported-agent instruction content for Qoder in .ai/instructions.md"
Task: "Align approved-provider guidance with Qoder in .github/prompts/speckit.agents.prompt.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. 完成 Phase 1 与 Phase 2
2. 完成 Phase 3（US1）
3. 执行 US1 的自动化测试与 quickstart 手工验证
4. 若通过，即可先交付“初始化可选 Qoder”的 MVP

### Incremental Delivery

1. 先交付 US1：初始化与资产生成
2. 再交付 US2：校验、忽略检查与刷新能力
3. 最后交付 US3：文档、说明与发布一致性
4. 每完成一个用户故事都重新跑对应测试和手工验收

### Parallel Team Strategy

1. 一名开发者完成治理/模板基础任务（Phase 2）
2. 一名开发者主攻 CLI 初始化与校验（US1/US2）
3. 一名开发者主攻文档、说明和发布审计（US3）
4. 最后共同完成 Phase 6 的端到端回归

---

## Notes

- 所有 `[P]` 任务都基于不同文件或独立测试目标设计
- 每个用户故事都保留独立自动化测试和手工验收入口
- 若实现中发现新的共享助手矩阵重构需求，应先回写 Feature 020 与相关设计文档再继续编码
- 提交实现时建议按 Phase 或单个用户故事拆分提交，便于回滚与审查