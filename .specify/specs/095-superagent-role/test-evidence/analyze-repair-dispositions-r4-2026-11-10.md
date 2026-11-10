# Analyze Repair Dispositions — r4（095-superagent-role，2026-11-10）

- **Stage**: analyze 门自主修复轮 r4（round-3 报告 0C / 1H；单写者）· **Line**: `095-superagent-role`
- **Input**: `test-evidence/analyze-merged-r3-2026-11-10.md` §1（R3-01，HIGH，`validated: direct re-read, subagent unavailable`）
- **Scope of this round**: 唯一处置 **R3-01**（HIGH 1/1，`confirm → fixed`）。R3-02（MEDIUM）、R3-03（LOW）与 38 条 carried MEDIUM/LOW **不属本修复轮授权范围**，显式维持、未关闭（§5）。
- **Touched artifacts**: `requirements.md`、`data-model.md`、`contracts/role-edge-engine.contract.md`、`contracts/status-digest-role-view.contract.md`、`plan.md`、`tasks.md`、`.specify/features/095-superagent-role.md`；证据：本文件 + `test-evidence/analyze-repair-gates-r4-2026-11-10.txt`。
- **单一设计裁定（本修复轮，自行裁决并记录）**: 在两个读法中选**增加输出槽位**——引擎 `executors[]` 增加独立键 `role_set_marker`（取值 `"dual-role"` | `null`），定义为 `roles` 的**确定性投影**（集合两成员齐备 ⟺ 取 [[STR-002]] 字面量，否则 `null`；永不作第三角色取值、永不作集合成员、永不作载体声明值）；`query` 的 `parent` / `child` 对象同构；digest 全量透传该键、不重推导。理由：STR-002 的声明语义是「只出现在角色集输出」的机读标记，而引擎是唯一判定面（FR-005）——槽位必须落在引擎输出；digest C-2 已契约化「经该标记渲染」，透传保持单一消费者链。**备选读法被拒**（收窄 SC-001 断言到既有观察点）：会使 STR-002 失去任何机器消费者，且须同时改写 FR-002 / Key Entities / A15 / digest C-2 / data-model §1 等更多位点——改动面更大且弱化已声明的验收意图。

## 1. R3-01 处置（HIGH 1/1）

| Finding | Sev | 处置 | 改动文件:行 | 一句话理由 |
|---------|-----|------|-------------|------------|
| R3-01 | H | confirm → fixed | `requirements.md:210`（SC-001）；`data-model.md:10`、`:13`（§1）、`:61`、`:64`（§4）；`contracts/role-edge-engine.contract.md:36-37`（C-3）、`:46`（C-4）、`:78`（C-10）；`contracts/status-digest-role-view.contract.md:11`、`:13`（C-2）、`:28`（C-5）、`:32`（C-6）；`plan.md:36`（D-8）、`:222`（P2）、`:224`（P4）；`tasks.md:122`（T011）、`:123`（T012）、`:178`（T032）、`:179`（T033）、`:193`（T034）、`:198`（T036）；`.specify/features/095-superagent-role.md:20` | `dual-role` 标记获得**单一契约槽位**：引擎 `executors[]` 独立键 `role_set_marker`（投影自 `roles`，附带值域与三条禁止）；C-10 钉实测期望值（A=`"dual-role"`，B/root=`null`）；digest 三处（C-2/C-5/C-6）声明显式透传、不重推导；plan/tasks 的 schema、fixture 与读数行同步该键 |

## 2. 单可读性关闭（finding 的两种读法各自如何被排除）

| 原读法 | 关闭方式（落点） |
|--------|------------------|
| A：把 `dual-role` 作为**第三个 token** 塞进 `roles` 数组 | SC-001（REQ:210）「独立机读键承载、MUST NOT 作为集合成员」；data-model §1（`:10`、`:13`）与 §4（`:61`）同句；engine C-3（`:37`）「never a member of the `roles` array」；C-10 钉 A 的 `roles` 恰为两项、标记单独承载 |
| B：输出 schema **没有任何键**承载标记 | engine C-3（`:36-37`）把 `role_set_marker` 列为 `executors[]` 必备键；C-4（`:46`）query 对象同构；C-10（`:78`）钉三个执行体的期望值；digest C-2（`:11`）声明条目必备该键 |
| C（潜读法）：digest 自行由集合推导标记（形成第二判定面） | digest C-2「passed through from the engine model, never re-derived」；C-5（`:28`）把 `role_set_marker` 归入 role-edge evaluation 来源族；C-6（`:32`）`entries[]` 透传 |

- **所有权边界**：字面量 `dual-role` 仍由 requirements Shared Strings 拥有（`:239` 的消费者清单不变：FR-002 / FR-005 / SC-001）；**键名**由 `data-model.md` §4 固定（plan 阶段命名权，遵循 FR-018「机读字面量在 plan 阶段固定」的先例）；requirements 只声明「独立机读键、键名归 plan」，不复写键名——无第二套词汇（XIV）。

## 3. 全链同步清单（requirements ↔ data-model ↔ contracts ↔ plan ↔ tasks）

| 层 | 同步后的单一事实 |
|----|------------------|
| requirements | SC-001：标记由角色集输出的**独立机读键**承载（键名归 plan），MUST NOT 作为集合成员、不作载体声明值；FR-002 / FR-005 / Key Entities / A15 原文已与「输出专用标记」语义一致，**逐字复读无冲突、不改** |
| data-model | §1 表与验证句：标记以 `role_set_marker` 输出、永不入集合；§4 执行体节点新增行（值域 / 投影语义 / C-3 指针），并把该键加入「引擎输出键」清单 |
| contracts（engine） | C-3 `executors[]` 键集 + 独立定义行（投影、三条禁止）；C-4 query `parent`/`child` 对象同构；C-10 期望值钉 A / B / root 三例与 query 一致性 |
| contracts（digest） | C-2 条目必备键（透传、不重推导）+ line 行 gains 清单；C-5 来源族；C-6 JSON 形状 |
| plan | D-8 `project_entry` gains 清单；P2 验证列点名 `executors[].role_set_marker`；P4 验证列点名字段 |
| tasks | T011 schema 断言点名字键与期望值；T012 / T032 fixture 行改为「驱动该键断言」；T033 读数清单点名该键；T034 字段清单；T036 实现行点名透传 |
| 绑定 Feature | `.specify/features/095-superagent-role.md:20` 的 `dual-role` 语句补键名与本模型指针 |

- **机械复扫**（本轮实执行）：`role_set_marker` 命中 26 处（engine 契约 8 / tasks 6 / data-model 4 / digest 契约 4 / plan 3 / Feature 1），覆盖上述全部层；`dual-role` 剩余位点 = `requirements.md:197`（Key Entities 语义句）、`tasks.md:134`（US1 checkpoint 语义句）、`checklists/requirements-quality-2026-11-10.md` CHK002 / CHK038（**dated checklist 快照**，按协议不就地刷新）——无一处再声称标记为 `roles` 成员或「无槽位」。

## 4. 门禁复跑（完整捕获见 `test-evidence/analyze-repair-gates-r4-2026-11-10.txt`）

| # | 命令 | 读数 |
|---|------|------|
| 1 | `python3 scripts/python/validate-requirements.py .specify/specs/095-superagent-role/requirements.md` | `status: ok`；6 标签全 pass；`scanned: 288 lines, 48 definition rows, 6 shared strings`；**0 error / 0 warning**，exit 0 |
| 2 | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/095-superagent-role --stage requirements --repo .` | `decision=pass errors=0 advisories=81 waived=0`（fr=38 / sc=10 / tasks=54 / files=12），exit 0 |
| 3 | 同上 `--stage plan` | `decision=pass errors=0 advisories=81 waived=0`，exit 0 |
| 4 | 同上 `--stage tasks` | `decision=pass errors=0 advisories=81 waived=0`，exit 0 |
| 5 | `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements … --tasks …` | `decision=proceed`；fr_count=38 / task_count=54（ceiling 120/160），exit 0 |
| 6 | `python3 scripts/python/validate-tasks.py .specify/specs/095-superagent-role/tasks.md`（补充：本轮编辑 tasks.md） | `PASS 0 error(s), 0 warning(s)`，exit 0 |
| 7 | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/095-superagent-role`（补充：本轮编辑 plan.md） | `status: ok`；6 检查全 pass；247 行 / 2 records，exit 0 |

- **advisory 构成不变 vs r3**：81 = 79 × `missing-path`（implement 阶段才创建的交付路径）+ 2 × `blocked-by` 模板占位 token（`<行ID>`）；全部属实现前预期。
- **本修复轮不重冻覆盖率基线**（`account-clause-coverage.py` 不在本轮判据内；其 `uncovered` 读数与 W3-06 的 MEDIUM 归属不变）。

## 5. 显式维持（不属本修复轮授权范围；不静默关闭）

- **R3-02**（MEDIUM：`dispatch_duty` 在 run-agent 载体无来源）与 **R3-03**（LOW：plan P2 第三变异演练与 C-11/T011 不同名）**维持**，按 round-3 报告 §12 的归属指针留待后续轮 / 各自 owner。
- round-2/3 的 38 条 carried MEDIUM/LOW **全部维持**，未修复、未拒绝。
- **验证波**: 本修复不改 round-3 的「HIGH 为检测者提议值」状态；修复后的重过 analyze 由轮换以全新检测/验证视角裁决，本文件不冒充验证结论。

## 6. 纪律说明

- 单写者；只改本特性产物与绑定 Feature 记录；未触碰其他特性、未 push。
- **未运行测试套件**（本轮只改规格 / 计划 / 任务 / 契约文本，无产品代码变更；测试入口纪律保持 `scripts/bash/run-tests.sh`）。
- 既有脏文件未提交未还原；前序阶段遗留 `checkpoints/`（未跟踪）继续不代提交。
- **同句扇出披露**: 除 finding 点名的 T011/T012/T036 外，T032 / T033 / T034 的字段与读数表述随同一事实同步（同一 `dual-role` 标记句子在全篇的机械扫全，SO-3A 教训的应用）；不计为独立修复项。
- 异常：无；in-passing repair：0（§3 的扇出同步属 R3-01 修复本体）；假设：仅顶部「单一设计裁定」一条（选读法 A 而非收窄 SC-001）。
