# Tasks: Dogfooding Practice Adoption (Revised)

**Requirement ID**: 032
**Requirement Key**: 032-dogfooding-practice
**Related Feature**: 036 Dogfooding Practice (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/032-dogfooding-practice/`（修订版：零新机器）
**Prerequisites**: plan.md, requirements.md, data-model.md, contracts/dogfooding-artifacts.md (C-1…C-7), quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation"；本特性为纯模板/治理文本，按 Principle VII template-only 规则以内容契约测试为测试层)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- DoD-1: 契约条款 C-1…C-7 全部有测试且通过
- DoD-2: 全量 pytest 相对 T001 基线零新增失败
- DoD-3: instructions-template 双镜像字节一致；无其他镜像/副本被触碰
- DoD-4: quickstart.md 四场景手工验证通过（含 SC-004 无新机器自检）
- DoD-5: SC-001…SC-004 在 verification.md 有状态行（pass/deferred）

**DoD Status**: pending

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 / US2 / US3
- Include exact file paths in descriptions

### Task State Sigil (REQUIRED)

- `- [ ]` — Open. `- [X]` — Closed. `- [~]` — Deferred (reason in verification.md `deferred_tasks=`).

## Path Conventions

Single project：仓库根下 `templates/`、`tests/`、`docs/`；镜像 `.specify/templates/`；治理文本 `.specify/memory/constitution.md`。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 基线与不变性快照（供 SC-004 比对）

- [X] T001 运行全量 `pytest`，通过/失败计数与失败清单记入 .specify/specs/032-dogfooding-practice/verification.md 的 `baseline=` 行
- [X] T002 [P] 记录"无新机器"基线快照到 verification.md：`feedback-utils.py` 的 `--action` choices 集合、`templates/commands/` 文件清单与哈希、`.specify/memory/` 目录布局（C-4 比对基准）

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 无阻塞性前置 — 本特性纯文本交付，无共享基础设施需先行构建（Phase 1 基线即前置）

*(no tasks)*

**Checkpoint**: T001/T002 完成后三个用户故事均可开始

---

## Phase 3: User Story 1 - 框架自用闭环 (Priority: P1) 🎯 MVP

**Goal**: constitution 显名 Dogfooding 原则（核心理念 + 两级循环指认 + 自用/偏离留档 + 建议性声明），并经既有 Feedback 机制记录一条真实摩擦点

**Independent Test**: 契约 C-1/C-6/C-7 通过；`--action list` 可见一条来源于本特性开发真实使用的条目

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T003 [P] [US1] 新建契约测试 tests/contract/test_dogfooding_practice.py：C-1（`### XI. Dogfooding` 存在；正文含核心理念、Loop A/Loop B 指认、自用条款、偏离留档落点、建议性声明；版本 MINOR 升级）、C-6（术语规范）、C-7（落点指明）断言，先失败

### Implementation for User Story 1

- [X] T004 [US1] 在 .specify/memory/constitution.md 新增 `### XI. Dogfooding (Self-Application)`：核心理念（开发者与使用者紧密联系 → 顺畅"使用→反馈→迭代"循环）、Loop A/Loop B 指认（既有 Feedback 机制、任务记录等）、框架自用 MUST、偏离 MUST 留档（`.specify/specs/<key>/` 或 `.specify/memory/`）、对下游建议性且 MUST NOT 新增门禁/机制；更新 Sync Impact Report 并 MINOR 升版（1.5.0.1 → 1.6.0）
- [X] T005 [US1] Dogfood 自身：按 quickstart 场景 1 步骤 1 用既有 `feedback-utils.py --action record` 记录本特性开发中的一条真实摩擦点（feature 键 032-dogfooding-practice）

### Manual Verification for User Story 1

- [X] T006 [US1] Manual QA：对照 requirements.md US1 三个验收场景核验（规格产物齐全、条目落盘并计入阈值循环、偏离留档条款存在），结果记入 verification.md

**Checkpoint**: US1 独立可验 — MVP 成立

---

## Phase 4: User Story 2 - Loop A 回流路径显名 (Priority: P2)

**Goal**: instructions-template 新增 `## Dogfooding Practice` 节的 Loop A 部分：可操作回流路径（record → 阈值提示 → package → 手动提交，零自动传输）

**Independent Test**: 契约 C-2 的 Loop A 断言 + C-3 镜像一致通过；按 quickstart 场景 1 完成 record → status → package 演练（SC-003）

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T007 [US2] 在 tests/contract/test_dogfooding_practice.py 追加 C-2 Loop A 断言（节存在；回流路径四步可辨；手动提交与零自动传输明示；动作名属既有 7 动作集）与 C-3（双镜像字节一致）、C-5（非破坏送达表述）断言，先失败

### Implementation for User Story 2

- [X] T008 [US2] 在 templates/instructions-template.md 新增 `## Dogfooding Practice` 节骨架 + Loop A 小节（项目无关表述；路径步骤与既有动作名严格对应 feedback-utils 实际动作集）
- [X] T009 [US2] 镜像同步：`\cp -f templates/instructions-template.md .specify/templates/instructions-template.md` 并 `diff -q` 确认（C-3）

### Manual Verification for User Story 2

- [X] T010 [US2] Manual QA：按 quickstart 场景 1 在本工作区完成 record → status → package 全链路演练（SC-003），结果记入 verification.md

**Checkpoint**: US1 与 US2 均独立可验

---

## Phase 5: User Story 3 - Loop B 自建循环指引 (Priority: P3)

**Goal**: 指引节补全 Loop B 能力映射（feedback 引擎 / memory / history / review / 任务记录）+ 反误区清单 + 分阶段/场景裁剪建议

**Independent Test**: 契约 C-2 的 Loop B/反误区断言通过；按 quickstart 场景 2 用自定义 unit-id 为"自己的产品"记录一条发现

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T011 [US3] 在 tests/contract/test_dogfooding_practice.py 追加 C-2 Loop B 断言（五项能力映射齐全、四项反误区齐全、分阶段与场景裁剪存在、项目无关）与 C-4（无新机器：feedback-utils choices 集合不变、templates/commands/ 相对 T002 快照零 Dogfooding 新增、.specify/memory/ 布局不变）断言，先失败

### Implementation for User Story 3

- [ ] T012 [US3] 在 templates/instructions-template.md 的 `## Dogfooding Practice` 节补全 Loop B 能力映射、反误区清单、分阶段/场景裁剪建议（保持项目无关）
- [ ] T013 [US3] 镜像同步：`\cp -f templates/instructions-template.md .specify/templates/instructions-template.md` 并 `diff -q` 确认（C-3 复验）

### Manual Verification for User Story 3

- [ ] T014 [US3] Manual QA：按 quickstart 场景 2 以自定义 unit-id 记录一条"自己的产品"发现 + 场景 4 无新机器自检（对照 T002 快照），结果记入 verification.md

**Checkpoint**: 三个用户故事均独立可验

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 文档、回归与成功标准核验

- [ ] T015 [P] 更新 docs/skills/feedback.md：补注该机制即 Dogfooding Loop A 的载体（一段轻量说明 + 指向 instructions 指引节）
- [ ] T016 运行全量 `pytest` 与 T001 基线比对（零新增失败），结果记入 verification.md
- [ ] T017 按 quickstart.md 四场景完整手工回归，并在 verification.md 写入 SC-001…SC-004 状态行（SC-001 属持续性指标可 deferred；SC-002 以模板节存在性 + 非破坏机制核验代验）

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖；T002 为 C-4/SC-004 的比对基准，必须先于任何实现
- **Foundational (Phase 2)**: 空阶段
- **User Stories (Phase 3–5)**: 均仅依赖 Phase 1；US2/US3 共享 instructions-template 同一节 → 按优先级串行（T008 先建节，T012 补全）
- **Polish (Phase 6)**: 依赖全部用户故事完成

### User Story Dependencies

- **US1 (P1)**: 独立（constitution + 既有 record 动作）
- **US2 (P2)**: 独立于 US1；建立指引节骨架
- **US3 (P3)**: 弱依赖 US2（同文件同节追加），可与 US1 并行

### Within Each User Story

- 测试先行且先失败（T003→T004、T007→T008、T011→T012）
- 模板改动后立即镜像同步 + `diff -q`

### Parallel Opportunities

- T001 与 T002 并行；T003（contract 新建）与 US2/US3 模板工作不同文件可并行；T015 与 T016 前置无关可并行编写

---

## Parallel Example: User Story 1

```bash
# US1 契约测试与 US2 模板骨架并行（不同文件）：
Task: "T003 契约测试 C-1/C-6/C-7 in tests/contract/test_dogfooding_practice.py"
Task: "T008 指引节骨架 + Loop A in templates/instructions-template.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 → Phase 3（US1）
2. **STOP and VALIDATE**: 原则显名 + 首条真实条目（既有机制）
3. 即为最小可信示范：框架自用 + Loop A 亲历走通

### Incremental Delivery

1. US1 → 原则显名（MVP）
2. US2 → Loop A 路径对下游可见可走通
3. US3 → Loop B 指引齐备
4. Polish → docs + 回归 + SC 核验

---

## Notes

- [P] tasks = 不同文件且无未完成依赖
- 镜像纪律：统一 `\cp -f` + `diff -q`（cp 可能别名 -i）
- **范围红线**：任何任务不得触碰 scripts/、templates/commands/、运行时命令副本——出现此类"需要"即违反 FR-004，应回到 spec 层讨论
- 偏好 `[~]` 显式延期而非留 `[ ]`
