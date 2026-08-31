---
description: "Task list for 047-feedback-introspection"
---

# Tasks: Feedback 自省流程(Feedback Introspection)

**Requirement ID**: 047 (from branch name)
**Requirement Key**: 047-feedback-introspection
**Related Feature**: 028 Feedback Mechanism (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/047-feedback-introspection/`
**Prerequisites**: plan.md, requirements.md, data-model.md, contracts/, quickstart.md, feature-ref.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" 为 MUST 级;本特性含可执行运行时代码(引擎扩展),引擎行为走契约测试 red-first;命令模板/文档产物按 Principle VII template-only 门走**结构契约测试**)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Environment Prerequisites**: 无外部依赖(无 docker/网络/集群);仅需本仓 Python ≥3.8 + pytest。所有引擎验证经 `--workspace-root` 指向临时目录,不碰真实存储。

## Definition of Done (DoD)

- DoD-1: 引擎扩展(introspect-register / dispose --reason/--ref / package --include-introspection)按 contracts/engine-cli.md C-1..C-15 实现
- DoD-2: 命令模板 Mode 5 按 contracts/command-mode.md C-1..C-10 落地,镜像与 4 份生成副本同步
- DoD-3: 全部新增契约测试 green;全量测试套件对 `baseline-failed.txt` 零新增失败
- DoD-4: 每对镜像义务(plan.md Mirror Obligations 两行)经显式 verify 任务核验
- DoD-5: quickstart.md 端到端流程在临时工作区真实执行通过(含新动作)
- DoD-6: 红线复核:无网络、无自动传输、外部条目零上行、条目正文不改写
- DoD-7: docs/reference/{commands,skills}/feedback.md 更新;Feature 028 详情文件留递进注记

**DoD Status**: green

## Completion Gate

- GATE-1: 全量套件零新增失败 — check: `scripts/bash/run-tests.sh` 输出与 `.specify/specs/047-feedback-introspection/baseline-failed.txt` 按名比对
- GATE-2: 镜像义务核验 — check: `diff -q scripts/python/feedback-utils.py .specify/scripts/python/feedback-utils.py`;`python3 scripts/python/sync-mirrors.py --check` exit 0;4 份生成副本 `grep -l 'introspect'` 全命中(`.specify/templates/commands/` 镜像已退役,不在核验面)
- GATE-3: 无 `[ ]`/`[>]` 任务行残留 — check: `grep -cE '^- \[[ >]\]' tasks.md` 返回 0
- GATE-4: verification.md 覆盖 SC-001..006 逐条状态 — check: 与 requirements.md 的 SC 清单对账

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行(不同文件、无未完成依赖)
- **[Story]**: 用户故事标签(US1/US2/US3);Setup/Foundational/Polish 阶段无标签
- **[blockedBy: Txxx]**: 显式依赖标签

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 基线纪律——先记录既有失败,实现期才能区分"基线失败"与"我引入的回归"

- [X] T001 运行全量测试套件并将失败名单冻结到 `.specify/specs/047-feedback-introspection/baseline-failed.txt`(`scripts/bash/run-tests.sh`,按测试名排序)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 报告解析/校验助手 + 索引/条目字段扩展——三个用户故事的引擎工作都建立其上

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 [P] 编写报告 schema 契约测试(红):`tests/contract/test_feedback_introspection_report.py`,钉住 contracts/introspection-report.md C-1..C-12(命名/子目录隔离/frontmatter 七字段/Findings 五要素/Excluded 块/承继语义/unicode 写出),fixture 用临时 workspace-root
- [X] T003 [blockedBy: T002] 在 `scripts/python/feedback-utils.py` 实现报告解析与校验助手(parse_report/validate_report,含 data-model V-1..V-5)+ `index.json` 增 `introspections[]`(缺省空数组,向后兼容)+ `entry_meta` 字段清单增 `introspection_ref`/`disposition_reason`
- [X] T004 [blockedBy: T003] 引擎镜像同步:`python3 scripts/python/sync-mirrors.py --write` 后 `diff -q scripts/python/feedback-utils.py .specify/scripts/python/feedback-utils.py` 一致(Mirror Obligations 第 1 行)

**Checkpoint**: 助手层契约测试转绿;镜像一致;US1-US3 可开始

---

## Phase 3: User Story 1 - 场景化自省:从事实条目到根因发现 (Priority: P1) 🎯 MVP

**Goal**: `introspect` 模式前五步中的 1-3(范围快照→场景化分析→报告产出+register 校验关联)落地,自省报告成为持久、结构校验、条目关联的产物

**Independent Test**: 在临时工作区造 open 条目 → 写报告 → `introspect-register` 校验通过并写回 `introspection_ref`;违规报告被逐条拒绝(exit 2);命令模板 Mode 5 章节与触发关键字经结构契约核验

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T005 [P] [US1] 引擎契约测试(红):`tests/contract/test_feedback_introspection_engine.py` 钉住 engine-cli C-1/C-2/C-4/C-5/C-6/C-15(register 校验、条目关联、index 登记、幂等重注册、承继置 superseded、退出码)
- [X] T006 [P] [US1] 命令模板结构契约测试(红):`tests/contract/test_feedback_command_introspect.py` 钉住 command-mode C-1..C-3(Mode 5 章节存在且位于 Mode 4 之前、`introspect` 触发关键字、命令描述行更新、镜像与 4 生成副本含新模式)+ C-5(Token 效率纪律提示)+ C-6/C-7(红线陈述:不自动改码/不传输、外部条目永不上行)

### Implementation for User Story 1

- [X] T007 [US1] [blockedBy: T003,T005] 实现 `action_introspect_register`(register 路径:校验→`introspection_ref` 写回→`introspections[]` 登记→承继翻转;argparse 接线 + `--format json`)于 `scripts/python/feedback-utils.py`
- [X] T008 [US1] [blockedBy: T006] 在 `templates/commands/feedback.md` 撰写 Mode 5 章节(范围快照/场景化分析/报告产出三步 + FR-012 边界态 + Token 效率纪律提示)并更新命令描述行
- [X] T009 [US1] [blockedBy: T007,T008] 镜像扇出与核验:`sync-mirrors.py --write` + `python3 scripts/python/regen-command-copies.py`;verify = 引擎 `diff -q scripts/python/feedback-utils.py .specify/scripts/python/feedback-utils.py` + 4 生成副本 `grep -l 'Mode 5'`(覆盖 Mirror Obligations 两行;模板镜像已退役)

**Checkpoint**: US1 独立可用——自省报告可产出、校验、关联;MVP 达成

---

## Phase 4: User Story 2 - 分流与处置:本地下沉 vs 随包上行 (Priority: P2)

**Goal**: register `--confirm` 批量处置 + dispose 扩展(理由/引用),用户确认后条目处置与关联写回生效

**Independent Test**: 含建议处置行的报告经 `--confirm` 后:报告置 confirmed、条目 disposition/disposition_reason/introspection_ref 批量写回;dispose 无新 flag 时行为逐字节零回归;外部条目混入时 upstream-bound 被拒绝

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T010 [US2] [blockedBy: T005] 引擎契约测试(红,追加进 `tests/contract/test_feedback_introspection_engine.py`):engine-cli C-3(confirm 批量处置 + confirmed_at)、C-7(dispose 无 flag 零回归)、C-8(--ref 格式校验)、V-4(external 成员强制 local-sink);同任务追加进 `tests/contract/test_feedback_command_introspect.py`:command-mode C-4(五步完整顺序)+ C-8(重复自省承继规则)

### Implementation for User Story 2

- [X] T011 [US2] [blockedBy: T007,T010] 实现 dispose `--reason/--ref` 扩展 + register `--confirm` 批量处置路径(建议处置行驱动,等价逐条 dispose)于 `scripts/python/feedback-utils.py`
- [X] T012 [US2] [blockedBy: T008,T010] 扩展 `templates/commands/feedback.md` Mode 5 第 4-5 步(用户确认/逐问题分流覆盖留痕/本地下沉与上行候选路由建议,仅建议不执行)
- [X] T013 [US2] [blockedBy: T011,T012] 镜像扇出与核验:同 T009 两行(engine `diff -q`;4 生成副本含步骤 4-5)

**Checkpoint**: US1+US2 均独立可用;确认门后处置联动生效

---

## Phase 5: User Story 3 - 上行包富化:事实+分析一起抵达消费方 (Priority: P2)

**Goal**: `package --include-introspection` 把覆盖条目的自省报告并入 zip + MANIFEST 节;命令侧默认提议文案

**Independent Test**: 自省覆盖的条目打包:zip 含 `introspection/<report>.md` 且 MANIFEST 含 `## Introspection Reports` 节;不带 flag 打包与现状逐字节一致;引用报告缺失时 MANIFEST 标 `(missing)` 不失败

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T014 [US3] [blockedBy: T010] 引擎契约测试(红,追加进 `tests/contract/test_feedback_introspection_engine.py`):engine-cli C-9..C-12(报告入包/MANIFEST 节/无 flag 零回归/missing 标注/外部条目报告永不入包);同任务追加进 `tests/contract/test_feedback_command_introspect.py`:command-mode C-9(Mode 2 默认提议文案)+ C-10(阈值提示语顺带建议)

### Implementation for User Story 3

- [X] T015 [US3] [blockedBy: T007,T014] 实现 package `--include-introspection`(经条目 `introspection_ref` 收集报告集→并入 zip→MANIFEST 追加节)于 `scripts/python/feedback-utils.py`
- [X] T016 [US3] [blockedBy: T012,T014] 更新 `templates/commands/feedback.md`:Mode 2 package 步骤默认提议文案(C-9)、阈值提示语顺带建议先自省(C-10)、Mode 4 读取端一行提示(包内可能含 introspection/ 报告,采信其源头核验)
- [X] T017 [US3] [blockedBy: T015,T016] 镜像扇出与核验:同 T009 两行

**Checkpoint**: US1-US3 全部独立可用;上行包富化闭环

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 文档同步 + 端到端真实走查 + 全量回归

- [X] T018 [P] 更新 `docs/reference/commands/feedback.md`:新增 Mode 5 章节(触发/五步流程/边界态)与 See Also
- [X] T019 [P] 更新 `docs/reference/skills/feedback.md`:Layout 增 `introspection/` 子目录、Engine 动作清单增 introspect-register 与扩展 flag、Positioning 节补自省定位(记录→自省→上行)
- [X] T020 [blockedBy: T009,T013,T017] 按 `quickstart.md` 在临时工作区真实执行端到端全流程(造条目→快照→报告→register→confirm→富化打包→验包),输出留证于 `verification.md`
- [X] T021 [blockedBy: T018,T019,T020] 全量回归与门禁:`scripts/bash/run-tests.sh` 对 baseline 零新增失败 + `sync-mirrors.py --check` exit 0 + Completion Gate 四项全核

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖,立即开始
- **Foundational (Phase 2)**: 依赖 Phase 1;阻塞全部用户故事(助手层是三个故事引擎工作的共同地基)
- **US1 (Phase 3)**: 依赖 Foundational;MVP
- **US2 (Phase 4)**: 依赖 US1 的 register 底座(T007/T008);分流确认是报告的下游
- **US3 (Phase 5)**: 依赖 US1 的关联字段(T007);与 US2 无相互依赖,US2 完成后或并行皆可
- **Polish (Phase 6)**: 依赖全部故事完成

### User Story Dependencies

- **US1 (P1)**: 仅依赖 Foundational——可独立完成、独立测试(MVP)
- **US2 (P2)**: 依赖 US1(register/报告存在)→ 处置联动才可生效
- **US3 (P2)**: 依赖 US1(`introspection_ref` 存在)→ 富化打包才有输入

### Within Each User Story

- 契约测试先写先红(T005/T006 → T010 → T014),实现紧随
- 每个故事收尾必做镜像扇出+核验(T009/T013/T017)——镜像义务是头等任务
- 引擎改动集中在同一文件,故事间经 blockedBy 串行,禁止并行改引擎

### Parallel Opportunities

- Phase 2:T002(测试)无依赖可立即写
- Phase 3:T005 与 T006 不同测试文件,可并行(红)
- Phase 6:T018 与 T019 不同文档文件,可并行
- US2 与 US3 的实现任务在 US1 完成后可由不同执行者并行(引擎文件除外,引擎串行)

---

## Parallel Example: User Story 1

```bash
# 同时启动 US1 的两个红测试任务(不同文件):
Task: "引擎契约测试 tests/contract/test_feedback_introspection_engine.py"
Task: "命令模板结构契约测试 tests/contract/test_feedback_command_introspect.py"
```

---

## Implementation Strategy

### MVP First

**MVP = 仅 US1**(单一 P1 故事,独立可测):自省报告可产出、结构校验、条目关联——客户项目即刻获得"事实→根因发现"的深加工能力。

1. 完成 Phase 1 基线冻结 → Phase 2 助手层
2. 完成 Phase 3(US1)→ 按其 Independent Test 验证
3. 依次叠加 US2(处置联动)、US3(上行富化),各自独立验证

### Incremental Delivery

每个故事都是完整增量:US1 交付分析能力;US2 交付分流闭环;US3 交付上行富化。任一故事落地后不破坏既有行为(C-7/C-10 零回归契约守护)。

---

## Notes

- 引擎为单一共享文件:凡改 `scripts/python/feedback-utils.py` 的任务不得并行,经 blockedBy 串行
- 镜像义务(plan.md 两行)在每个故事末位任务显式核验;最终 GATE-2 再总核
- Pin 纪律:测试不断言版本字符串前缀;文件清单以存在性为准;计数用 `len(...)` 推导
- **Deferral discipline**:无法本会话完成的工作标 `[~]` 并注 `<!-- deferred: 原因 -->`,不留 `[ ]`
- 引擎无新增只读动作(C-13):自省范围快照复用 `list --disposition open --format json`
