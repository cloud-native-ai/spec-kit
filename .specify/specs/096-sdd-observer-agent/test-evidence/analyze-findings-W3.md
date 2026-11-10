# Analyze Findings — W3（tasks.md）

- **Wave**: W3（并发只读检测波）
- **读域**: `.specify/specs/096-sdd-observer-agent/tasks.md`（唯一被判对象；未读取其他 spec 制品）
- **报告日期**: 2026-11-10
- **写面**: 本文件与 Wrap-up 记账；未修改任何制品
- **校验状态**: W3-01、W3-04 为 HIGH，须由独立校验波确认；本波未自证（校验波载体规则禁止宿主内进程内子代理）

## Findings

| ID | Category | Severity | Anchor | 一句话事实 | 建议归属（指针） |
|----|----------|----------|--------|------------|------------------|
| W3-01 | inconsistency（包级顺序） | HIGH | `.specify/specs/096-sdd-observer-agent/tasks.md:89-100,232,337` | 包序声明 wp01 先于 wp02，但 wp01 内的 T037 被 wp02 内的 T020 阻塞，且 package 表 Edge 列未记这条反向边，三种顺序声明（Edge 列 / Declared integration order / Parallel Team Strategy）无一种能同时成立，按字面执行会死锁。 | `tasks.md` § Package Map / § Declared integration order / § Parallel Team Strategy（经 `/speckit.tasks` 收敛；优先复核 T037 的 blocker 或其包归属） |
| W3-02 | inconsistency（写域领地） | MEDIUM | `.specify/specs/096-sdd-observer-agent/tasks.md:93,95,98,186` | T023 属 wp03，却写 `tests/fixtures/sdd-observer/failure_builder.py`——该路径位于 wp01 声明的 owned 目录内、且不在 wp03 的 write domain 中，与 § Package Map 的互斥领地声明不符。 | `tasks.md` § Package Map（wp03 写域补路径，或 T023 改归 wp01） |
| W3-03 | inconsistency（并行标记） | MEDIUM | `.specify/specs/096-sdd-observer-agent/tasks.md:111,124,163,193,288-293` | § Parallel Opportunities / Parallel Example 宣称 T006、T018、T027 可并行（并称 T004 在 T001 之后），但对应行分别是无 `[P]`、无 `[P]`、`blockedBy: T026`、无 blocker，指引与行级标记相互矛盾。 | `tasks.md` 对应任务行的 `[P]` / `[blockedBy:]` 标记，或 § Parallel Opportunities 文本 |
| W3-04 | concurrency-safety（项目指令冲突） | HIGH | `.specify/specs/096-sdd-observer-agent/tasks.md:11,108,369` | 所有 red-first 证据都追加到单一 `notes/red-first-evidence.md`，而写入行分属 wp01、wp02、wp03 且 wp02/wp03 被允许并发执行，违反 `AGENTS.md` § Concurrent Development Safety 的“记录类数据一文一件、不得共享可变聚合”MUST。 | T001（落地路径改为每条记录一文件，或按包/时间戳分文件）；本波只读，不修复 |
| W3-05 | coverage-gap（DoD） | MEDIUM | `.specify/specs/096-sdd-observer-agent/tasks.md:24,66-85,109-111` | DoD-8 要求 § Premises 的 14 个生成期量在 implement entry 全部重测，但无任何任务行承担该重测（T002 只重取三个测试基线，T004 只重探环境），DoD 与任务覆盖之间存在缺口。 | DoD-8 / Setup 行 T002–T004（补一条 premise 重测行或把 DoD-8 的 owner 显式落到 implement Step 0） |
| W3-06 | underspecification（可追溯性） | LOW | `.specify/specs/096-sdd-observer-agent/tasks.md:168` | T017 只枚举 data-model 的 V-1…V-13 与 V-16/V-17，V-14、V-15、V-18、V-19、V-20 在 tasks.md 全文无任何归属行，五条规则的覆盖不可追溯。 | T017 的检查范围，或 data-model → task 映射（本波读域不含 data-model.md，需聚合波对照确认） |

## 检测波执行记录

- **A duplication**: 已执行；未发现近重复要求。DoD/GATE 对同一检查命令的成对引用属验收/收口双层引用，未按漂移副本计。
- **B ambiguity**: 已执行；全文无 `TODO` / `TKTK` / `???` / `TBD` 占位。
- **C underspecification**: 已执行；产出 W3-05、W3-06。
- **D constitution alignment**: 已执行；对照 `.specify/constitution.md` 的 22 条原则标题未发现 MUST 冲突；W3-04 是 `AGENTS.md` 项目指令冲突，非宪法原则冲突。
- **E coverage gaps**: 已执行（tasks.md 内部）；FR-001…FR-023、SC-001…SC-007 均在任务行中以文本形式出现，SC → row trace 七行齐全；缺口见 W3-05、W3-06。
- **F inconsistency**: 已执行；产出 W3-01、W3-02、W3-03。
- **G feature relevance & registry**: 仅执行 tasks.md 侧检查（T044 承担 registry reconcile）；`.specify/features.md` 与 `.specify/features/096.md` 不在本波读域，未对 index/detail 漂移下判。
- **H checklist accountability**: 未执行；`checklists/` 不在本波读域（W1 已处置）。
- **I decision tension records**: 不适用；判定对象是 plan.md，不在本波读域。

## 机器核对摘要

- 任务行：47 条，`T001`–`T047` 唯一，无缺号、无重号。
- `[blockedBy:]`：0 个未知目标、0 个自环；行级依赖图无环（47/47 可拓扑排序）。
- `[green:]`：54 条，0 碰撞；与 header 的 58 子句 − 4 条已披露未认领 = 54 相符。
- 包分区：14 + 5 + 10 + 13 = 42 打包行 + 5 Setup 行 = 47。
- 跨包行级依赖：`T031←T029`（wp02←wp03）、`T032←T020`（wp03←wp02）、`T037←T020`（wp01←wp02）、`T018←T006`（wp02←wp01）、`T033←T003`（wp04←Setup）；包表 Edge 列只部分承载这些边（见 W3-01）。
- FR / SC 文本覆盖：FR 23/23、SC 7/7（计数取自 tasks.md 文本，未回读 requirements.md 的定义行）。

## 范围与证据边界

- 本波只判 tasks.md；requirements.md、plan.md、data-model.md、contracts/、registry 与 checklists 均未读取，跨制品漂移由聚合波合并判定。
- 未执行任何修复；W3-01…W3-06 的建议归属仅为指针，修复须回到 `/speckit.tasks` 等对应入口。
