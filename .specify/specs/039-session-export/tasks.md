# Tasks: Session 导出与导出侧重命名(/speckit.session + export-session 通用化)

**Input**: Design documents from `.specify/specs/039-session-export/`(plan.md, requirements.md, data-model.md, contracts/×3, quickstart.md, feature-ref.md)
**Prerequisites**: plan.md ✅ | requirements.md ✅ | data-model.md ✅ | contracts/ ✅ | quickstart.md ✅ | feature-ref.md ✅
**Feature**: 043 Session Export | **Branch**: `039-session-export`

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is NON-NEGOTIABLE;引擎改造为运行时代码 → 契约+集成测试先行;命令模板为模板工件 → 结构性契约测试先行)

**Validation**: 格式校验通过——所有任务均为 `- [ ] [ID] [P?] [US?] 描述+文件路径` 清单行;DoD 仅用 `- DoD-N:` 前缀。

**Environment Prerequisites**(生成期探测,2026-08-12):本机 `~/.claude/projects/` 与 `~/.qoder/projects/` 均有本仓库会话落盘(claude-code / qoder-cli 真跑可用);opencode 未安装(按"未安装"声明路径);copilot / hermes 无落盘(按退出码 4 探测声明路径,FR-010)。pytest 8.4.2 可用;无 docker/集群/网络依赖。

---

## Format: `- [ ] [TaskID] [P?] [Story] Description`

## Phase 1: Setup

**Purpose**: 冻结测试基线,区分存量失败与回归(AGENTS.md 测试基线纪律);清扫套件残留(__pycache__/集成夹具)以免污染基线

- [X] T001 清扫残留并冻结基线:`find skills .specify/skills -name '__pycache__' -o -name 'layout-int-*'` 确认 0 项后,运行 `.specify/scripts/bash/run-tests.sh --names-out .specify/specs/039-session-export/notes/baseline-failed.txt tests/ -q > .specify/specs/039-session-export/notes/baseline.txt`(实施期每阶段结束 `comm -13` 对比,零新增失败)

## Phase 2: Foundational(阻塞所有 User Story)

**Purpose**: export.py 改造核心——支持面收敛、zip→目录、`--name` 必填、meta 输出骨架,US1/US2/US3/US4 全部消费

- [X] T002 编写改造核心契约/集成测试(测试先行):新建 `tests/contract/test_export_skill_rework.py` pin `contracts/export-skill-rework.contract.md`——`PARSERS` 键集合 == 六家规范名(STR-002);被移除六标识(qwen/qoderwork/oh-my-pi/kimi/codex-app/qoder-IDE 形态)全文扫描计数 0;目录产物布局断言(构造 jsonl 夹具驱动 export.py:`main.*`/`session-meta.json`/`SESSION.md` 存在性,`subagents/`/`state/`/`large-results/`/`request-ids.jsonl` 按夹具内容);`--name` 缺省/文法越界 → 退出码 2;同名冲突 → 非零拒绝;copilot/hermes 探测无源 → 退出码 4 + "未探测到"声明;五值退出码语义;只读断言(夹具存储导出前后 hash 一致) [blockedBy: T001]
- [X] T003 实现改造核心(满足 T002):编辑 `skills/export-session/scripts/export.py`——删除 qwen/qoder-IDE/qoderwork/oh-my-pi/kimi/codex-app 六家适配器与其专属辅助函数/路径常量;`PARSERS` 收敛为六家(claude-code/codex-cli/qoder-cli/opencode 保留适配 + copilot/hermes 新增探测式适配器,`available()` 按候选路径探测);四家 `*_pack` 的 zip 写入改为目录写入(D4 布局),移除原子 zip 机制(`_open_zip_atomic`/`_commit_zip`/`_abort_zip`);新增 `--name` 必填参数(文法校验,越界退出码 2)与同名冲突拒绝;stdout 改打印导出目录绝对路径;新增 `session-meta.json` 确定性输出(D7 字段集,含 `snapshot` 与 `over_summary_budget` 骨架);退出码五值保持 [blockedBy: T002]
- [X] T004 运行 T002 测试集全绿,并以本环境真实会话(claude-code 或 qoder-cli)冒烟一次目录导出确认端到端可跑 [blockedBy: T003]

## Phase 3: User Story 1 — 当前会话导出为用户命名目录(P1)🎯 MVP

**Goal**: `/speckit.session export --name <名称>` 经 preview 门禁委托技能,生成用户命名的导出目录
**Independent Test**: quickstart §1——导出成功、目录名即指定值、显式参数路径、缺 --name/非法名拒绝、同名冲突拒绝

### Tests for User Story 1

- [X] T005 [P] [US1] 编写命令面结构性契约测试(测试先行):新建 `tests/contract/test_session_command_surface.py` pin `contracts/session-command.contract.md`——`templates/commands/session.md` 含 export 子命令文法行(`--name`/`--session`/`--tool`/`--verify`)、`--name` 必填纪律句、preview 门禁披露四要素(工具/会话/目标/规模)、同名冲突交互确认条款、无 `--force` 旁路断言、委托 `skills/export-session` 纪律句;per-tool 副本集合从既有 goal/team 命令面测试夹具风格派生(pin hygiene:不新增硬编码幻影路径) [blockedBy: T003]

### Implementation for User Story 1

- [X] T006 [US1] 撰写命令模板(author-section,满足 T005):新建 `templates/commands/session.md`——frontmatter(description/argument-hint)、User Input、export 子命令文法、preview→confirm→execute 门禁(披露四要素)、委托 export-session 技能调用块、同名冲突交互确认(无 --force)、结果回报格式、Feedback/Documentation 收尾节 [blockedBy: T003,T005]
- [X] T007 [US1] 镜像扇出 + 逐行核验(mirror-parity,覆盖 Mirror Obligations 第 2 行):运行 `python3 scripts/python/sync-mirrors.py --write`;核验 `diff -q templates/commands/session.md .specify/templates/commands/session.md`,并 grep 确认 4 份 per-tool 副本含 export 文法:`.claude/commands/speckit.session.md`、`.github/prompts/speckit.session.prompt.md`、`.qoder/commands/speckit.session.md`、`.opencode/command/speckit.session.md` [blockedBy: T006]
- [X] T008 [US1] 端到端验证(render-verify):按 quickstart §1 对本环境真实会话(claude-code/qoder-cli)执行——导出成功与目录内容、`--session`/`--tool` 显式路径、缺 `--name` 与非法名拒绝(exit 2)、同名冲突拒绝;结果回写 `quickstart.md` 走查记录 [blockedBy: T007]

**Checkpoint**: US1 完成即可独立交付——会话可导出为用户命名目录(MVP 主体)

## Phase 4: User Story 2 — 支持面收敛六家且通用化(P1)

**Goal**: 技能支持面恰好六家、零残留、去平台依赖;copilot/hermes 探测声明诚实
**Independent Test**: quickstart §2——零残留扫描、copilot/hermes 探测退出码 4、保留四家内容面不削弱、无平台依赖扫描

### Tests for User Story 2

- [X] T009 [P] [US2] 编写通用化契约测试(测试先行):新建 `tests/contract/test_export_skill_genericity.py` pin `contracts/export-skill-rework.contract.md §1/§4`——SKILL.md 与 export.py 全文无 `a1 skill report`、无 `x-source`、无 aone-open 标识、无出站 URL(http/https 调用);SKILL.md 支持矩阵恰为六家行;调用段脚本探测目录仅六家对应项;被移除六标识双文件计数 0 [blockedBy: T003]

### Implementation for User Story 2

- [X] T010 [US2] 重写技能文档(author-section,满足 T009):重写 `skills/export-session/SKILL.md`——frontmatter(description 六家表述、argument-hint 加 `--name`、去 `x-source`/`disable-model-invocation` 语义保持);移除 §1 aone-open 使用上报段;调用段(bash/PowerShell 两组,解释器探测纪律保持)探测目录收敛六家;输出节改目录形态(D4 布局 + SESSION.md/session-meta.json);`--tool` 取值表六家;支持矩阵表含 copilot/hermes「会话存储未探测到」声明行;退出码表五值保持;描述文档流程节(脚本元信息 + agent 总结补写 + 预算降级纪律) [blockedBy: T003,T009]
- [X] T011 [US2] 镜像扇出 + 逐行核验(mirror-parity,覆盖 Mirror Obligations 第 1 行):运行 `python3 scripts/python/sync-mirrors.py --write`;核验 `diff -q skills/export-session/SKILL.md .specify/skills/export-session/SKILL.md` 与 `diff -q skills/export-session/scripts/export.py .specify/skills/export-session/scripts/export.py` [blockedBy: T010]
- [X] T012 [US2] 收敛验收(render-verify):按 quickstart §2 执行——零残留 grep 双文件计数 0、`--tool copilot`/`--tool hermes` 探测退出码 4 + 声明文本、保留四家逐家真跑(本环境可用者 claude-code/qoder-cli 真跑;未安装者按未安装路径)与改造前产物内容面对照(夹具级);结果回写 quickstart §2 [blockedBy: T011]

**Checkpoint**: US1+US2 = 完整 MVP(导出可用 + 支持面收敛通用)

## Phase 5: User Story 3 — 会话描述文档(P2)

**Goal**: 导出目录内 SESSION.md + session-meta.json:元信息程序确定性提取,结构化总结 agent 补写、超预算程序判定降级
**Independent Test**: quickstart §3——meta 字段逐值对照、预算判定两侧、SESSION.md 结构断言

### Tests for User Story 3

- [X] T013 [P] [US3] 编写描述文档契约/集成测试(测试先行):新建 `tests/integration/test_session_description.py` pin `contracts/session-description.contract.md`——构造已知内容/规模 jsonl 夹具驱动 export.py:`session-meta.json` 字段逐值一致(tool/session_id/model/workspace/时间窗/计数);`over_summary_budget` 两侧(超阈值夹具 true、正常 false,阈值常量 `SUMMARY_LINE_LIMIT=50000`/`SUMMARY_BYTE_LIMIT=32MB`);`SESSION.md` 结构(STR-003 标识行、元信息节、总结占位节);meta.json 与 SESSION.md 元信息节逐字段对照;运行中会话快照夹具 → `snapshot: true` [blockedBy: T003]

### Implementation for User Story 3

- [X] T014 [US3] 实现描述文档确定性半体(满足 T013):编辑 `skills/export-session/scripts/export.py`——冻结预算常量 `SUMMARY_LINE_LIMIT`/`SUMMARY_BYTE_LIMIT`(以主记录计);`session-meta.json` 完整字段集输出(D7);`SESSION.md` 渲染:STR-003 标识行 + 元信息节(与 meta.json 逐字段一致,不可得字段 null + 「记录未含」标注)+ 固定 heading 总结占位节;stdout 输出预算判定 [blockedBy: T003,T013]
- [X] T015 [US3] 运行 T013 测试集全绿 + 对真实会话导出核验描述文档两形态一致,结果回写 quickstart §3 [blockedBy: T014]

## Phase 6: User Story 4 — 团队 run 追溯衔接(P3)

**Goal**: 派发 label 命名导出 + 运行中会话快照语义,追溯链闭合
**Independent Test**: quickstart §4——label 命名目录与映射表对应、`snapshot: true` 声明

- [X] T016 [US4] 追溯衔接演练与快照核验:按 quickstart §4 执行——以派发 label 形 `<team-slug>--<run-stamp>--<member-role>` 为 `--name` 导出(文法天然兼容,断言目录名 == label);运行中会话快照语义复验(`snapshot: true` + 总结限定声明,复用 T013 夹具证据);结果回写 quickstart §4 [blockedBy: T014]

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T017 [P] 用户文档:新建 `docs/reference/commands/session.md`——命令定位(导出侧命名降级路线,链接概念背景不复述)、export 用法、参数表、退出码、与 `/speckit.team` 追溯链衔接、See also [blockedBy: T008]
- [X] T018 全仓镜像一致性终检:`python3 scripts/python/sync-mirrors.py --check`(exit 0)+ `find` 抽查无手工双写残留 [blockedBy: T007,T011,T015,T016,T017]
- [X] T019 全套件终验:对比 T001 基线——`comm -13` 名称级零新增失败;新增测试族(test_export_skill_rework / test_session_command_surface / test_export_skill_genericity / test_session_description)全绿 [blockedBy: T018]
- [X] T020 quickstart 全走查复跑(refresh-verify):按 quickstart §1–§5 对真实引擎端到端复跑一遍,结果回写;SC-001…SC-006 逐项对照取证来源 [blockedBy: T019]

---

## Dependencies

```text
T001 (Setup 基线)
 └─▶ T002 → T003 → T004   (Foundational: export.py 改造核心,阻塞一切)
      ├─▶ US1: T005 → T006 → T007 → T008
      ├─▶ US2: T009 → T010 → T011 → T012      (代码收敛已在 T003,本阶段为文档面与验收)
      ├─▶ US3: T013 → T014 → T015             (依赖 T003 的 meta 骨架)
      └─▶ US4: T016                           (依赖 T014 快照/meta 完整面)
Polish: T017 随 US1 落定即可并行 → T018 → T019 → T020
```

- US1 ⊥ US2 ⊥ US3(测试文件各自独立,`[P]` 有效;共享 export.py 的实现任务 T003/T014 串行)
- US4 依赖 US3 的 meta/快照完整实现(T014)
- US1、US2 同为 P1,构成 MVP;US3(P2)、US4(P3)可独立延后

## Parallel Execution Examples

```text
# Foundational 完成后,三个 Story 的测试编写可同时发起:
Task: "T005 命令面结构性契约测试"   (tests/contract/test_session_command_surface.py)
Task: "T009 通用化契约测试"        (tests/contract/test_export_skill_genericity.py)
Task: "T013 描述文档集成测试"      (tests/integration/test_session_description.py)

# Polish 期:
Task: "T017 用户文档" 可与 US2/US3 收尾并行
```

## Implementation Strategy

### MVP First(User Story 1 + 2)

1. Phase 1 Setup → Phase 2 Foundational(阻塞项,最先完成)
2. US1(导出为用户命名目录)→ 独立测试:quickstart §1
3. US2(支持面收敛 + 通用化)→ 独立测试:quickstart §2
4. **MVP 就绪**:会话可导出、可命名、支持面恰好六家

### Incremental Delivery

- US1+US2 后可先交付评审;US3(描述文档)再交付;US4(追溯衔接)最后
- 每阶段结束对比基线(T001)确认零新增失败;每镜像批次结束跑 `sync-mirrors.py --check`
- 实施纪律:契约测试先行于实现;镜像只走 `sync-mirrors.py`;导出对宿主存储只读(每阶段抽查 hash)

## Notes

- `[blockedBy:]` 标记由 `/speckit.implement` 拓扑排序消费;无标记任务仅受阶段顺序约束
- Pin hygiene:per-tool 副本清单从既有命令面测试夹具风格派生;支持矩阵六家名单本身是契约(计数即契约,随矩阵改动同任务更新)
- 模板工件(命令模板)的测试为结构性契约测试(内容/镜像一致性断言),无运行时对象——符合模板特性门
- copilot/hermes 为探测式适配器:本环境无落盘,验收走退出码 4 + 声明文本路径,不臆造 pack 行为(FR-010)
- `[P]` 仅标于不同文件且无未完成依赖的任务;共享 export.py 的实现任务串行

## Definition of Done

- DoD-1: SC-001…SC-006 逐项有取证来源且通过(SC-005 以导出前后存储 hash 一致取证)
- DoD-2: 全套件对比基线零新增失败;三份契约的 Test Pins 全部落实为测试并绿
- DoD-3: `sync-mirrors.py --check` exit 0;Mirror Obligations 4 行逐行核验留痕
- DoD-4: quickstart §1–§5 全走查通过并回写结果
- DoD-5: docs/reference/commands/session.md 已创建;被移除六产品全文零残留(双文件扫描计数 0);无平台专属依赖残留
- DoD-6: 导出对宿主会话存储只读(hash 断言);同名冲突无静默覆盖、无 --force 旁路;描述文档元信息程序提取 100% 一致、降级显式声明
