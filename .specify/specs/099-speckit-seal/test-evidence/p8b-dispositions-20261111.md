# P8b — 回合缺陷修复处置记录（099-speckit-seal）

生成时间：2026-11-11（本文件是 P8b 回合的处置记录；不建第二份台账）

## 0. 范围与输入

- 输入：P8 真实回合证据 `074-round-20261110.txt`（终态 blocked，B1–B4 具名）。
- 权威：`tasks.md` + `plan.md` / `contracts/`（FR-017/FR-027 与 merge 契约 `merge-back.contract.md` C-011…C-023）。
- 本轮修的是**引擎/合并产物缺陷**；回合裁定语义不变（FR-027(d) 与 B2 继续作为具名阻断）。
- before 快照：`074-rerun-before-snapshot-20261111.txt`；旧证据 `074-round-20261110.txt` 未改动、原样保留。

## 1. 逐缺陷处置

| 缺陷 | 根因（实测） | 修复（`scripts/python/seal-utils.py`） | 红先证据 | 修复后证据 |
|------|--------------|----------------------------------------|----------|------------|
| **B4** 内容丢失（最高优先） | `_CLAUSE_RE = ^\*\*(C-\d{3})\*\*` 只认三位条款 ID；074 的 1–2 位条款（C-1…C-67）全部不被识别 → 074b 的 C-21…C-30 未追加，`contracts/report-and-attribution.md` 只剩父级 C-47…C-54；T037–T040 的 green 认领悬空 | ① `_CLAUSE_RE` / `_canonical_id` / `_target_id` / `_ID_TOKEN_RE` 的 C 家族全部改为 `C-\d{1,3}`；② `_continuous` 连续性锚点由「恒从 1 起」改为「从序列自身最小值起」——074 的父契约按全契约集编号（`report-and-attribution.md` 从 C-47 起），1 起锚会把已合并文件判为不连续，且旧实现只有「一条条款都没识别出来」时才会通过；③ `_rewrite_ids` 新增 `(父 C-N)` 注解保护：注解指向父级自己的条款 id，不是分片本地引用，不得被分片映射改写 | `test_one_and_two_digit_clause_ids_merge_instead_of_being_lost`（未修复时红：分片 `**C-5**` 条款整条丢失；`p8b-red-first-20261111.txt`） | 重跑 plan：`id_maps.C` 77 条（全 append）；`report-and-attribution.md` = C-47…C-54 + **C-055…C-064**；`nested-invocation.md` 29 条；`validate-tasks` green-dangling = 0（`074-merge-plan-rerun-20261111.json/.txt`、`074-merge-checks-rerun-20261111.txt`） |
| **B1** 假阳性 state-drift | `_registry_row` 在 features.md 表内空行（71/76/78/80 行）处重置表头，其后的 074 行读不到 → registry=None 并误报 | 空白行保留表头（空白行是排版事实）；仅非空非表格行（散文/新标题）结束表上下文 | `test_registry_row_is_read_across_blank_lines_inside_the_table`（未修复时红：state-drift exit 2） | 重跑 seal 不再出现 state-drift；两次运行都在 `Ready for Review` 状态对上继续到后续门（`074-round-rerun-20261111.txt`） |
| **B3** 合并产物校验债 | `_tasks_content` 把分片任务行平铺追加，丢掉了分片 `## Phase ...` 阶段标题 → 33 × story-labels；green 认领的 10 × dangle 由 B4 引起 | 分片任务行按该分片的阶段标题落位（保留 `## Phase` 标题与 `<!-- source: <slug> -->` 归属标注；无阶段标题的行落入按分片命名的合成阶段） | `test_merged_slice_task_rows_keep_their_phase_headings`（未修复时红：无阶段标题，validate-tasks 报 story-labels） | 合并后父 `tasks.md`：19 个阶段标题（父 8 + 074a 6 + 074b 5）、58 闭合行、0 未勾选、57 条 superseded 引用行；`validate-tasks.py` **0 error / 2 warning**（两 warning 为分片行原样合并带来的既有 parallel-safe / green-path-divergence，非本轮新增内容） |
| **B2** 具名阻断（保持） | 074 早于 § Runtime Stack & Dependency Ownership 门禁；闭包判定器 exit 2 | **不修、不自造运行时声明**；继续作为具名阻断 | — | 重跑 seal 的**唯一**引擎条件即 `closure-input-defect`（两次运行逐字一致） |

引擎修复伴生说明：

- `_rewrite_ids` 的注解保护只认 `（父 …）` / `(父 …)` 括号组；组内 C-N 是父级条款引用，不参与分片本地重编号。若无此保护，074a/074b 的 61 处 `(父 C-N)` 注释会被本地映射改写为无关 id。
- `_continuous` 改为 min 锚定后，1 起编号的 FR/SC/STR/T/E 序列行为不变；偏移编号的契约文件按「自身连续、无空洞」判定，与本缺陷的「内容丢失」根因同一修复面。

## 2. 074 回合重跑（修复后引擎）

流程：before 快照 → 恢复 pre-merge 树（`3f2a05cba` + 保留父 requirements 的 8 条 `**Path**: final` 修复）→ merge-plan → merge-apply → 后置校验 → 提交合并产物 → seal × 2。

| 步骤 | 命令 | 读数 | 证据 |
|------|------|------|------|
| merge-plan | `seal-utils.py --action merge-plan --spec-dir .specify/specs/074-goal-team-sdd-unification --repo . --json` | exit 0；slices = 074a→074b（split-record）；open_conflicts 0；factory_doc_refs 0；id_maps C 77 / T 58 / STR 17 | `074-merge-plan-rerun-20261111.json` / `.txt` |
| merge-apply | `seal-utils.py --action merge-apply --spec-dir … --repo . --json` | exit 0；writes 75；checks: id_continuity=pass、open_rows=0、duplicate_ids=0、dangling_refs=0、dated_records_stable=true；57 supersede dispositions | `074-merge-apply-rerun-20261111.txt` |
| merge-apply 幂等 | 完成后重跑同一命令 | `idempotent: True`、`writes: 0`（C-014） | 本文件读数 |
| validate-tasks | `validate-tasks.py …/tasks.md` | **PASS：0 error / 2 warning**；未勾选行 0 | `074-merge-checks-rerun-20261111.txt` |
| validate-requirements | `validate-requirements.py …/requirements.md` | exit 0，0 error / 0 warning（path-marker pass） | 同上 |
| dated record | 47 个分片测量原件，运行前后 sha256 | 47/47 逐字节一致 | `074-dated-record-hashes-rerun-before.txt` + 同文件复算 |
| 镜像 | `sync-mirrors.py --check` | exit 0（`scripts/python/seal-utils.py` 与 `.specify/` 投影同字节） | 本文件读数 |
| seal RUN 1 | `seal-utils.py --action seal --spec-dir .specify/specs/074-goal-team-sdd-unification/` | exit 2；条件 = `closure-input-defect`（唯一） | `074-round-rerun-20261111.txt` |
| seal RUN 2 | 同上 | exit 2；与 RUN 1 逐字一致（diff 为空） | 同上 |

回合裁决（每次运行重算、逐字复现）：FR-027(a)/(b)/(c)/(e) resolved；FR-027(d) blocked（074b review P0 F1 仅驱动者豁免，`scripts/bash/common.sh:86` 仍 `^[0-9]+-`）；额外阻断 B1 resolved、B2 blocked、B3 resolved、B4 resolved。
终态：**blocked（exit 2）**——非 Sealed；具名阻断 = FR-027(d) + B2；无第三态、无静默默认。

## 3. 复跑套件

`bash scripts/bash/run-tests.sh`（8 个 seal 契约文件 + `tests/integration/test_seal_074_round.py`）：

- 未修复引擎红先：3 failed（B4/B3/B1 三个新用例）→ `p8b-red-first-20261111.txt`
- 修复后（含 074 合并树更新与集成测试改读 `074-round-rerun-20261111.txt`）：**130 passed**，exit 0 → `p8b-suite-20261111.txt`

## 4. 边界声明

- 未自造 074 的 Runtime Stack 声明（B2 保持阻断）。
- 未写入任何用户豁免，未把 FR-027(d) 读作已处置。
- 未改动旧回合证据字节；未改动分片 dated record 字节。
- 未更动 `templates/commands/seal.md`、`skills/internal/seal-artifact/SKILL.md` 的命令面（本轮只修引擎与合并产物）。
