# Tasks: /speckit.docs 文档规范与管理命令

**Requirement ID**: 033
**Requirement Key**: 033-docs-command
**Related Feature**: 037 Docs Command (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/033-docs-command/`
**Prerequisites**: plan.md, requirements.md, data-model.md, contracts/ (×3), quickstart.md, feature-ref.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" 强制；Principle VII 的 template-only gate 适用——模板/提示类交付以**结构性契约测试**（内容/章节/镜像一致性断言）替代运行时测试；docs-utils.py 为唯一可执行件，走完整契约先行)

**Organization**: Tasks grouped by user story（doc-feature taxonomy：author-section / mirror-parity / render-verify / refresh-verify）

## Definition of Done (DoD)

- DoD-1: 全部交付物按 requirements.md FR-001…FR-011 落地，每项任务可回溯到 FR/SC
- DoD-2: 全部契约测试（3 份契约文档对应的结构性测试）与集成测试通过；全量回归相对 T001 基线零新增失败
- DoD-3: 镜像义务表（plan.md § Mirror Obligations）每行的双写 + 校验任务全部关闭，`regen-command-copies.py --check` 零漂移
- DoD-4: quickstart.md 全部 CLI 示例经真实执行回验（contracts/docs-utils-cli.md C-11）
- DoD-5: verification.md 覆盖 SC-001…SC-007 的逐项状态（pass/deferred + 证据）
- DoD-6: Dogfooding 调谐留有审计日志与残差报告，符号链接/镜像/内链零破坏

**DoD Status**: green

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 调谐引擎 / US2 notes 生命周期 / US3 文档同步步骤 / US4 dogfooding / US5 feedback
- **Verification tasks**: 交互式聊天演练任务需要真实 `/speckit.*` 会话；非交互环境下按 `[~]` 延期纪律处理

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [X]` — Closed；`- [~]` — Deferred（原因记入 verification.md `deferred_tasks=` 与行内 `<!-- deferred: ... -->`）。零 `[ ]` 视为运行完成。

## Path Conventions

模板/提示框架仓库：`templates/commands/`（命令源）、`shared/`（约定源）、`scripts/python/`（引擎源），各自 `.specify/` 镜像；测试在 `tests/contract/`、`tests/integration/`、夹具在 `tests/fixtures/`。

## Environment Prerequisites

- 全部任务仅需本地文件系统 + Python ≥3.8 + pytest（已探测可用）；无 docker/网络/集群依赖。
- T015A/T019A/T026A/T029/T032 需要交互式 AI 聊天会话运行 `/speckit.*` 指令；若本轮 implement 无交互会话，按 `[~]` 延期并留原因。

---

## Phase 1: Setup

**Purpose**: 基线与夹具

- [X] T001 运行全量 pytest 并记录基线计数（P/F/E/S）到 .specify/specs/033-docs-command/verification.md 的 `baseline=` 行（基线纪律：区分既有失败与新增回归）
- [X] T002 [P] 创建测试夹具 tests/fixtures/docs_command/：blank_project/（空白）、messy_project/（含小写 readme.md、错放文档、断链）、notes_samples/（draft / 超期 draft / archived 含 target / archived 缺 target / frontmatter 损坏 五类样例）

---

## Phase 2: Foundational（确定性引擎——US1/US2 共同前置）

**Purpose**: docs-utils.py 引擎（contracts/docs-utils-cli.md）先行落地，阻塞所有故事

**⚠️ CRITICAL**: 契约测试先写并确认失败，再实现

- [X] T003 Contract test（先写、先失败）：contracts/docs-utils-cli.md C-1…C-10 断言（action 集合、scan 分组 JSON、expire 不删文件、clean 默认 dry-run/--yes 门禁、archive-check broken 清单、validate 五维校验、audit 落盘 .specify/docs/audit/、exit code 约定、不触碰 feedback 引擎）in tests/contract/test_docs_utils_cli.py
- [X] T004 实现 scripts/python/docs-utils.py：单一 argparse `--action {scan,expire,clean,archive-check,stats,validate,audit}`，标准库-only，stdout 单 JSON；字面量以 requirements.md Shared Strings（[[STR-001..004]]）为准
- [X] T005 双写镜像 .specify/scripts/python/docs-utils.py（`\cp -f` 防 cp -i 别名）
- [X] T006 校验：`diff -q scripts/python/docs-utils.py .specify/scripts/python/docs-utils.py` 零差异；T003 契约测试转绿

**Checkpoint**: 引擎可用——各用户故事可开始

---

## Phase 3: User Story 1 - 文档空间调谐（单一引擎收敛文档结构） (Priority: P1) 🎯 MVP

**Goal**: `/speckit.docs` 命令模板落地并分发：作用域判定 + R0–R6 薄调度 + 四件产物 + 分级确认 + 期望态基线（含大写特殊名注册表）

**Independent Test**: 空白夹具 bootstrap 出完整骨架；messy 夹具产出四件套且未确认移动零执行；连续两次运行第二次零收敛

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T007 [P] [US1] Contract test（先写、先失败）：contracts/docs-command-template.md C-1…C-11 结构断言（frontmatter、章节顺序、作用域表、门禁表、四产物落点、docs/archive/、薄调度、根相对 shared/ 引用、注册表种子）in tests/contract/test_docs_command_template.py
- [X] T008 [P] [US1] Integration test：bootstrap 骨架清单（SC-001）+ 防抖（同一夹具连续两次 validate/audit 第二次零新增收敛项，SC-002 确定性部分）+ 命名违规点名（SC-006，messy 夹具 validate）in tests/integration/test_docs_command_scenarios.py

### Implementation for User Story 1

- [X] T009 [US1] author-section：编写 templates/commands/docs.md（frontmatter description/handoffs；## User Input / ## Glossary / ## Outline（作用域判定表、R0–R6 薄调度引用 shared/patterns/reconcile-pattern.md、分级确认门禁、四件产物、bootstrap 骨架含 FR-010 注册表四条种子语义与 ADR decisions/ 模板节）/ ## Feedback（unit-id /speckit.docs）/ ## Documentation / ## Handoffs）
- [X] T010 [US1] mirror-parity（双写）：运行 `python3 scripts/python/regen-command-copies.py` 生成 .specify/templates/commands/docs.md 镜像 + 全部工具运行时副本（.claude/.github/.qoder/.qwen/.opencode/.codex/.hermes/.iflow 既存目录）
- [X] T011 [US1] mirror-parity（校验）：`python3 scripts/python/regen-command-copies.py --check` 零漂移；T007 契约测试转绿
- [X] T012 [P] [US1] author-section：编写命令参考文档 docs/commands/docs.md（结构对齐 docs/commands/history.md：When to Use / Syntax / Execution Flow / Output Artifacts / Tool Support）
- [X] T013 [US1] docs/quickstart.md 命令表新增 /speckit.docs 行（含 `[details →](commands/docs.md)` 链接）
- [X] T014 [US1] render-verify：以 blank/messy 夹具走一遍引擎确定性路径（validate → audit）确认四件产物落点与审计内容；T008 集成测试转绿
- [X] T015 [US1] Manual QA：交互会话运行 quickstart 场景 1/2（bootstrap + 全量调谐防抖），证据记入 verification.md

**Checkpoint**: MVP——命令可独立交付

---

## Phase 4: User Story 2 - Notes 临时文档生命周期管理 (Priority: P2)

**Goal**: notes 退场机制端到端：frontmatter 规范 + 状态机 + 三条退场路径 + 归档完整性

**Independent Test**: 五类样例笔记走完 scan → expire → 三条退场路径，状态流转与报告符合状态机

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T016 [P] [US2] Integration test：三条退场路径（合入 archived+target、续期回 draft、clean --yes 确认删除）+ 超期点名 100%（SC-003）+ invalid 修复建议（默认 expires=created+60 天）in tests/integration/test_docs_notes_lifecycle.py

### Implementation for User Story 2

- [X] T017 [US2] author-section：在 templates/commands/docs.md 的 bootstrap 骨架节补全 notes 区规则 README 内容与 frontmatter 模板（title/created/expires/status/target/tags；引用 [[STR-001..004]] 字面量）
- [X] T018 [US2] mirror-parity（双写+校验）：T017 修改后重跑 `regen-command-copies.py` 并 `--check` 零漂移
- [X] T019 [US2] refresh-verify：对 notes_samples 夹具重复执行 scan/expire/stats 两轮，确认幂等（第二轮 expire marked=0）；T016 转绿
- [X] T020 [US2] Manual QA：交互会话按 quickstart 场景 3 演练三条退场路径，证据记入 verification.md

**Checkpoint**: US1+US2 均可独立验证

---

## Phase 5: User Story 3 - 核心命令的文档同步评估步骤 (Priority: P2)

**Goal**: docs-step 单一事实源 + 注入 14 个复杂命令收尾（与 Feedback 同点、非阻断、增量）

**Independent Test**: 静态扫描 14 复杂命令含 `## Documentation` 且引用单一事实源、4 简单命令不含；一次有/无文档影响的运行各走通

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T021 [P] [US3] Contract test（先写、先失败）：contracts/docs-step-injection.md C-1…C-9 断言（单一事实源镜像一致、14/4 注入范围、## Documentation 紧邻 ## Feedback 且在 ## Handoffs 前、引用不复制、无新增持久化存储）in tests/contract/test_docs_step_injection.py

### Implementation for User Story 3

- [X] T022 [US3] author-section：编写 shared/workflow/docs-step.md（评估语义、结论二选一格式、非阻断、增量评估禁全量 R0–R6、安全写入门禁、移动/归档级动作降级为"建议运行 /speckit.docs"）
- [X] T023 [US3] mirror-parity（双写+校验）：`\cp -f` 到 .specify/shared/workflow/docs-step.md 并 `diff -q` 零差异
- [X] T024 [US3] author-section：向 13 个既有复杂命令模板 templates/commands/{agents,analyze,clarify,constitution,feature,history,implement,instructions,plan,requirements,research,review,tasks}.md 注入 `## Documentation` 引用节（紧邻 ## Feedback；根相对 `shared/workflow/docs-step.md` 引用）——以 test_feedback_command_classification.py 的 COMPLEX_COMMANDS 实际清单为准核对成员
- [X] T025 [US3] 更新 tests/contract/test_feedback_command_classification.py：COMPLEX_COMMANDS 加入 `docs`（13→14），SIMPLE_COMMANDS 保持 4，计数断言同步
- [X] T026 [US3] mirror-parity（双写+校验）：重跑 `regen-command-copies.py` 覆盖全部被注入模板的镜像与工具副本，`--check` 零漂移；T021 转绿
- [X] T027 [US3] Manual QA：交互会话运行一个复杂命令至收尾，观察 Documentation 步骤输出"需记录/无需记录"且不阻断（quickstart 场景 5），证据记入 verification.md

**Checkpoint**: 文档同步步骤全网生效

---

## Phase 6: User Story 4 - Dogfooding：对 Spec Kit 自身运行文档整理 (Priority: P3)

**Goal**: 激进重组基调的全量调谐：docs/ 向六类 taxonomy 收敛、两份设计笔记退场、一贯性约束同步更新

**Independent Test**: SC-004 全项——审计/残差在 .specify/docs/、docs/ 顶层合规、两笔记 archived 且 target 存在、零悬空链接/零符号链接破坏

### Implementation for User Story 4

- [X] T028 [US4] 为 docs/notes/docs-design.md 与 docs/notes/notes-design.md 补合规 frontmatter（status: draft、target 指向计划中的正式归宿文档）
- [X] T029 [US4] 交互会话运行 `/speckit.docs`（激进重组基调）：干跑计划逐项确认后收敛——docs/ 子目录向 concepts/tutorials/tasks/reference/decisions/contribute 归位、新建根 ARCHITECTURE.md 与 CONTRIBUTING.md（≤一屏）、归档区 docs/archive/、两份设计笔记内容合入正式文档后置 archived
- [X] T030 [US4] 同步一贯性表面：更新 .specify/instructions.md Documentation Map 与全部内部链接至新路径（经 /speckit.instructions 或手工），保持 README → docs 单向引用
- [X] T031 [US4] render-verify：`python3 scripts/python/docs-utils.py --action validate` 零断链；`find . -type l` 符号链接完好；`regen-command-copies.py --check` 零漂移；`--action archive-check` 两笔记 target 存在
- [X] T032 [US4] Manual QA：SC-004 逐项证据（审计日志/残差报告路径、docs/ 顶层清单、frontmatter 抽检）记入 verification.md

**Checkpoint**: Dogfooding 完成，框架自身文档合规

---

## Phase 7: User Story 5 - 基于 Feedback 的持续优化 (Priority: P4)

**Goal**: /speckit.docs 的 Feedback 自省链路走通（复用 028，零新机器）

**Independent Test**: 一次合格运行留有 unit-id=/speckit.docs 条目；同 run-id 重复记录去重

### Implementation for User Story 5

- [X] T033 [US5] 演练：完成一次合格 /speckit.docs 运行的 Feedback 步骤（feedback-utils.py record，unit-id "/speckit.docs"），随后以相同 run-id 重复记录验证 `duplicate: true` 去重；确认引擎动作集与存储布局零变化（SC-005），证据记入 verification.md

---

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T034 refresh-verify：执行 quickstart.md 全部 CLI 示例逐条真实回验（C-11），修正任何漂移（改文档或改实现，以契约为准）
- [X] T035 全量 pytest 回归并与 T001 基线对比：零新增失败；结果记入 verification.md
- [X] T036 完成 verification.md：SC-001…SC-007 逐项 `SC-NNN_status=pass|deferred` + 证据行 + `deferred_tasks=` 清单
- [X] T037 （运行中用户指示）保留文件名严格阻断：宪法原则 X 修订（v1.7.0）+ ADR-0002 + FR-010 强化 + 引擎 reserved-name-misplaced 校验 + 4 个嵌套 README.md → index.md + 模板/参考/夹具/契约/测试全链路同步

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 无依赖
- **Phase 2 (Foundational)**: 依赖 T001/T002 — **阻塞全部故事**（引擎为 US1/US2 的 render-verify 前提）
- **Phase 3 (US1)**: 依赖 Phase 2；T009 是 T017/T024 的文件级前置（同文件 templates/commands/docs.md）
- **Phase 4 (US2)**: 依赖 Phase 2 + T009（写同一模板文件）
- **Phase 5 (US3)**: 依赖 T009（docs.md 须先含 ## Documentation 节才计入 14）；T024/T025/T026 顺序执行
- **Phase 6 (US4)**: 依赖 US1 + US2 交付（dogfooding 用真实命令与引擎）
- **Phase 7 (US5)**: 依赖 US1（命令可运行）
- **Phase 8 (Polish)**: 依赖全部期望故事完成

### Within Each User Story

- 契约/集成测试先写并确认失败 → author-section → mirror-parity（双写+校验成对）→ render-verify → refresh-verify → Manual QA
- 同文件任务（templates/commands/docs.md：T009→T017；13 模板注入 T024）不可并行

### Parallel Opportunities

- T002 与 T001 并行；T007/T008 并行；T012 与 T009-T011 并行；T016 与 T021 并行（不同测试文件）；US4 之前 US2/US3 可由不同执行者并行（US2 改 docs.md 骨架节、US3 改 13 个其他模板——注意 docs.md 本身归 US1/US2 串行）

## Parallel Example: User Story 1

```bash
# 测试先行（并行，不同文件）：
Task: "T007 contract test in tests/contract/test_docs_command_template.py"
Task: "T008 integration test in tests/integration/test_docs_command_scenarios.py"
# 模板与参考文档（并行，不同文件）：
Task: "T009 author templates/commands/docs.md"
Task: "T012 author docs/commands/docs.md"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 → Phase 2（引擎）→ Phase 3（US1）
2. **STOP and VALIDATE**：夹具 bootstrap/防抖 + 契约全绿 → 可交付 MVP

### Incremental Delivery

US1（命令）→ US2（notes 生命周期）→ US3（docs-step 全网注入）→ US4（dogfooding，真实使用即验收）→ US5（feedback 链路演练）→ Polish；每步独立可验，互不回退。

## Notes

- 镜像纪律：每次触碰 templates/commands/ 或 shared/ 后必须成对执行"再生成 + `--check`"；`.specify/skills/`、`.venv` 内产物永不手编
- 修改 13 个既有命令模板（T024）是高扇出动作：以 COMPLEX_COMMANDS 清单为唯一成员依据，逐文件小步提交
- 交互式任务（T015/T020/T027/T029/T032/T033）无会话时置 `[~]` 并记原因，不留 `[ ]`
- `create-new-plan.sh` 等脚手架禁止在本 spec 上重跑（覆写历史）
