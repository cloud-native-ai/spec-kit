# Tasks: Skill Install Layout

**Requirement ID**: 007
**Requirement Key**: 007-skill-install-layout
**Related Feature**: 013 Skills Command
**Input**: Design documents from `.specify/specs/007-skill-install-layout/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/skill-install-layout.openapi.yaml, quickstart.md

**User Input Analysis**: `$ARGUMENTS` 为空，本次按默认策略基于现有设计文档自动生成完整任务清单，不引入额外背景约束或附加任务条目。

**Tests**: 由于本需求涉及安装路径迁移、冲突拦截、兼容入口与回滚降级，需提供 contract/integration/unit 回归覆盖。

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Definition of Done (DoD)

- [ ] 代码行为满足 requirements.md 的 FR-001 ~ FR-016
- [ ] 新增与更新的自动化测试通过（contract/integration/unit）
- [ ] quickstart 关键场景完成手工验证并记录结果
- [ ] 文档与模板中主目录/兼容入口表述一致
- [ ] Feature 记录已同步本次任务拆分结果

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no blocking dependencies)
- **[Story]**: User story label (`[US1]`, `[US2]`, `[US3]`) for story phases only
- 每个任务描述都包含明确File path

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 为技能安装布局重构准备任务骨架与测试文件。

- [X] T001 创建任务相关测试骨架文件 `tests/contracts/test_skill_install_layout_contract.py`、`tests/integration/test_skill_install_layout_integration.py`、`tests/unit/test_skills_utils_layout.py`
- [X] T002 [P] 创建迁移与冲突场景测试夹具目录 `tests/fixtures/skill-layout/`
- [X] T003 [P] 在 `.specify/specs/007-skill-install-layout/quickstart.md` 标注自动化覆盖映射段落

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 实现所有用户故事共享的基础能力（主目录、工具画像、迁移结果模型、通用错误语义）。

**⚠️ CRITICAL**: 本阶段完成前不得进入任何用户故事实现。

- [X] T004 在 `scripts/bash/create-new-skill.sh` 引入可配置主目录常量，默认指向 `.specify/skills`
- [X] T005 [P] 在 `.specify/scripts/bash/create-new-skill.sh` 同步引入 `.specify/skills` 主目录默认值
- [X] T006 在 `scripts/python/skills-utils.py` 增加 `.specify/skills/*/SKILL.md` 的资源类型推断与 canonical 识别
- [X] T007 [P] 在 `.specify/scripts/python/skills-utils.py` 同步 `.specify/skills` 类型推断逻辑
- [X] T008 在 `scripts/python/skills-utils.py` 增加入口状态枚举与迁移结果结构（created/skipped/failed/conflict, success/partial-success/failed）
- [X] T009 [P] 在 `.specify/scripts/python/skills-utils.py` 同步入口状态与结果结构
- [X] T010 在 `tests/unit/test_skills_utils_layout.py` 增加 `.specify` 主路径识别与状态枚举基础单测

**Checkpoint**: 主目录识别与通用状态模型就绪，用户故事可以开始实现。

---

## Phase 3: User Story 1 - 统一项目级技能主目录 (Priority: P1) 🎯 MVP

**Goal**: 所有项目级 skill 一律安装到 `.specify/skills/<skill-name>/`，并保持重复执行幂等。

**Independent Test**: 在空项目安装同一 skill 两次，主副本仅存在于 `.specify/skills/<skill-name>/` 且第二次为重用状态。

### Tests for User Story 1

- [X] T011 [P] [US1] 在 `tests/contracts/test_skill_install_layout_contract.py` 增加 `/skills/{skillName}/install` 的主副本路径契约断言
- [X] T012 [P] [US1] 在 `tests/integration/test_skill_install_layout_integration.py` 增加新安装落盘与重复安装幂等场景

### Implementation for User Story 1

- [X] T013 [US1] 重构 `scripts/bash/create-new-skill.sh` 的创建流程，使主内容写入 `.specify/skills/<skill-name>/`
- [X] T014 [US1] 重构 `.specify/scripts/bash/create-new-skill.sh` 的创建流程，使主内容写入 `.specify/skills/<skill-name>/`
- [X] T015 [US1] 更新 `templates/commands/skills.md` 的路径说明与流程文案，声明 `.specify/skills` 为主目录
- [X] T016 [US1] 更新 `templates/skills-template.md` 中目录描述，避免将 `.github/skills` 作为主安装路径
- [X] T017 [US1] 在 `scripts/bash/create-new-skill.sh` 输出中新增主副本状态字段（created/reused/failed）
- [X] T018 [US1] 在 `.specify/scripts/bash/create-new-skill.sh` 输出中新增主副本状态字段（created/reused/failed）

### Manual Verification for User Story 1

- [ ] T019 [US1] 按 `.specify/specs/007-skill-install-layout/quickstart.md` 执行 Scenario 1 与 Scenario 7 并记录结果

**Checkpoint**: US1 完成后，主副本统一与幂等行为独立可验收。

---

## Phase 4: User Story 2 - 为已支持工具暴露兼容入口 (Priority: P2)

**Goal**: 按已支持工具画像创建兼容入口；优先软链接，失败时使用占位目录+指引文件且不复制内容。

**Independent Test**: 安装 skill 后，`.github/skills/<skill-name>` 等入口均映射到同一主副本；软链接不可用时出现占位入口并返回 partial-success。

### Tests for User Story 2

- [X] T020 [P] [US2] 在 `tests/contracts/test_skill_install_layout_contract.py` 增加 `/skills/{skillName}/entrypoints` 的 mode/status 契约断言
- [X] T021 [P] [US2] 在 `tests/integration/test_skill_install_layout_integration.py` 增加 GitHub 入口创建与多工具跳过/创建矩阵场景
- [X] T022 [P] [US2] 在 `tests/integration/test_skill_install_layout_integration.py` 增加软链接不可用时 placeholder 降级场景

### Implementation for User Story 2

- [X] T023 [US2] 在 `scripts/bash/create-new-skill.sh` 实现兼容入口创建流程（symlink 优先，placeholder 降级）
- [X] T024 [US2] 在 `.specify/scripts/bash/create-new-skill.sh` 同步兼容入口创建流程
- [X] T025 [US2] 在 `scripts/python/skills-utils.py` 实现工具支持画像识别与入口计划生成
- [X] T026 [US2] 在 `.specify/scripts/python/skills-utils.py` 同步工具支持画像识别与入口计划生成
- [X] T027 [US2] 在 `scripts/bash/create-new-skill.sh` 实现 placeholder 指引文件写入逻辑（例如 `README.md`）并禁止复制 skill 内容
- [X] T028 [US2] 在 `.specify/scripts/bash/create-new-skill.sh` 同步 placeholder 指引文件逻辑

### Manual Verification for User Story 2

- [ ] T029 [US2] 按 `.specify/specs/007-skill-install-layout/quickstart.md` 执行 Scenario 2 与 Scenario 3 并记录结果

**Checkpoint**: US2 完成后，多工具入口暴露策略独立可验收。

---

## Phase 5: User Story 3 - 平滑迁移既有安装方式 (Priority: P3)

**Goal**: 识别旧版 `.github/skills/<skill-name>` 真实目录并迁移收敛到新布局，包含备份、删除条件、失败降级与冲突阻断。

**Independent Test**: 在旧目录存在时执行刷新，备份成功则迁移删除旧目录；备份失败则保留旧目录并标记 manual-required；冲突时禁止覆盖。

### Tests for User Story 3

- [ ] T030 [P] [US3] 在 `tests/contracts/test_skill_install_layout_contract.py` 增加 `/skills/{skillName}/migrate-legacy` 成功/422 分支契约断言
- [X] T031 [P] [US3] 在 `tests/integration/test_skill_install_layout_integration.py` 增加旧目录迁移+备份成功+删除旧目录场景
- [X] T032 [P] [US3] 在 `tests/integration/test_skill_install_layout_integration.py` 增加备份失败保留旧目录与 manual-required 场景
- [X] T033 [P] [US3] 在 `tests/integration/test_skill_install_layout_integration.py` 增加入口冲突（普通文件/目录）阻断场景

### Implementation for User Story 3

- [X] T034 [US3] 在 `scripts/bash/create-new-skill.sh` 实现旧版 `.github/skills` 真实目录检测与迁移入口
- [X] T035 [US3] 在 `.specify/scripts/bash/create-new-skill.sh` 同步旧目录检测与迁移入口
- [X] T036 [US3] 在 `scripts/bash/create-new-skill.sh` 实现迁移备份、删除前置检查、备份失败降级逻辑
- [X] T037 [US3] 在 `.specify/scripts/bash/create-new-skill.sh` 同步备份与降级逻辑
- [X] T038 [US3] 在 `scripts/bash/create-new-skill.sh` 实现入口冲突检测与显式错误码输出
- [X] T039 [US3] 在 `.specify/scripts/bash/create-new-skill.sh` 同步冲突检测与显式错误码输出

### Manual Verification for User Story 3

- [ ] T040 [US3] 按 `.specify/specs/007-skill-install-layout/quickstart.md` 执行 Scenario 4、Scenario 5、Scenario 6 并记录结果

**Checkpoint**: US3 完成后，旧布局迁移与失败降级独立可验收。

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 收敛跨故事文档、测试与特性记录，完成交付前验证。

- [X] T041 [P] 更新 `README.md` 与 `docs/skills/vscode.md`，将 `.specify/skills` 标注为主目录，`.github/skills` 标注为兼容入口
- [X] T042 [P] 更新 `docs/usage.md` 中 `/speckit.skills` 的安装路径说明与兼容入口行为
- [X] T043 更新 `.specify/memory/features/013.md`，记录 tasks 拆分带来的关键实现备注与验证范围
- [X] T044 更新 `.specify/memory/features.md` 中 Feature 013 的 Last Updated 日期（如发生变化）并确认状态保持 Implemented
- [X] T045 运行回归测试 `tests/contracts/test_skill_install_layout_contract.py`、`tests/integration/test_skill_install_layout_integration.py`、`tests/unit/test_skills_utils_layout.py`
- [ ] T046 执行 `.specify/specs/007-skill-install-layout/quickstart.md` 全量验证并补充结果摘要

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 无依赖，可立即开始
- **Phase 2 (Foundational)**: 依赖 Phase 1，阻塞所有用户故事
- **Phase 3 (US1)**: 依赖 Phase 2 完成
- **Phase 4 (US2)**: 依赖 Phase 2 完成；建议在 US1 后执行以复用主副本结果
- **Phase 5 (US3)**: 依赖 Phase 3 与 Phase 4 的安装/入口能力
- **Phase 6 (Polish)**: 依赖所选用户故事全部完成

### User Story Dependencies

- **US1 (P1)**: MVP，先交付主副本统一与幂等
- **US2 (P2)**: 建立兼容入口和降级路径
- **US3 (P3)**: 在前两者基础上补齐迁移与冲突治理

### Within Each User Story

- 先测试任务，后实现任务
- 先脚本能力，后模板与文档
- 先自动化验证，后手工 quickstart 验证

### Parallel Opportunities

- Setup 阶段 T002/T003 可并行
- Foundational 阶段 T005/T007/T009 可并行（在 T004/T006/T008 之后）
- US1 中 T011/T012 可并行；T017/T018 可并行
- US2 中 T020/T021/T022 可并行；T023/T024 与 T025/T026 可并行
- US3 中 T030/T031/T032/T033 可并行；T034/T035、T036/T037、T038/T039 可并行
- Polish 中 T041/T042 可并行

---

## Parallel Example: User Story 2

```text
Task: T020 [US2] Contract assertions for /skills/{skillName}/entrypoints in tests/contracts/test_skill_install_layout_contract.py
Task: T021 [US2] Multi-tool entrypoint integration scenarios in tests/integration/test_skill_install_layout_integration.py
Task: T022 [US2] Placeholder fallback integration scenario in tests/integration/test_skill_install_layout_integration.py

Task: T023 [US2] Implement entrypoint creation flow in scripts/bash/create-new-skill.sh
Task: T024 [US2] Mirror entrypoint creation flow in .specify/scripts/bash/create-new-skill.sh
Task: T025 [US2] Implement tool support profile planner in scripts/python/skills-utils.py
Task: T026 [US2] Mirror tool support profile planner in .specify/scripts/python/skills-utils.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. 完成 Phase 1 + Phase 2
2. 完成 Phase 3（US1）
3. 验证 quickstart Scenario 1 与 7
4. 先交付“主副本统一 + 幂等”最小可用增量

### Incremental Delivery

1. MVP：US1
2. 增量二：US2（兼容入口 + 软链接降级）
3. 增量三：US3（迁移 + 备份 + 冲突治理）
4. 最后执行 Polish 与全量验证

### Parallel Team Strategy

1. 开发者 A：`scripts/bash/create-new-skill.sh` 主流程与迁移
2. 开发者 B：`.specify/scripts/bash/create-new-skill.sh` 镜像实现
3. 开发者 C：`scripts/python/skills-utils.py` 画像/状态与测试
4. 文档与 feature 记录由任一成员在 Phase 6 收敛

---

## Notes

- 所有任务均遵循 `- [ ] T### [P?] [US?] 描述 + File path` 规范
- 本次任务拆分未引入新 Feature，也未淘汰既有 Feature；Feature 013 仍为唯一归属
- 建议 MVP 范围：Phase 1 + Phase 2 + Phase 3
