# Tasks-Stage Assumptions & Rulings — 067-loop-efficiency-hardening (P4-tasks-test-slimming)

**Date**: 2026-10-22 · **Stage**: tasks · **Executor**: fresh-context subagent per dispatch brief.
访谈式问题按派发要求就地裁决；本文件是裁决与假设的记录位（requirements.md / plan.md 本阶段只读）。

## A-1 · Part 任务数与 plan §Implementation Slicing 预估的偏差

plan 预估 ≈37 任务（A6 / B5 / C4 / D4 / E7 / F6 / G5）。实际落盘 38 行（T001–T038）：

- **T-Start +2**（T001 基线 id 清单、T002 三件证据骨架）：派发 brief 明确要求 T-Start 组，plan 预估未含。
- **A 6→5**：CLI 钉住保留并入 T004、矩阵表驱动扩展并入 T005（同一文件、同一验证轮，拆行不增可验证性）。
- **C 4→2**：CLI 冒烟钉住并入 T013、复测+台账并入 T014（单文件单机制，plan 预估偏保守）。
- **E 7→6**：台账回填并入各折叠批（T020–T022 每批逐行入台账，"随折叠同步写"本就是 plan 要求）。
- **F 6→5**：FB-08 与 FB-09 合为一个演练任务 T028（quickstart S6 即按一次演练承载两个判据）。
- **G 5→6**：verification 定稿（T038）单列——plan G 的"证据收口"落在 closure 之后才有完整输入。

约束核验：每 part ≤8 ✓；总数 38 ≤ 40（decomposition-check `--mode tasks` 机械复核 decision=proceed）✓；plan 的数字是预估而非上限，偏差不触发任何合同条款。

## A-2 · W1 的执行位置：拆为 E 组（Class 1）与 F 组（Class 2），不前置于 W2

派发 brief 的组清单按 T-Start→W1→W2→W3→W4→W5→收口 列举覆盖面；plan §Implementation Slicing（切分权威）把 W1 Class 1 放进 E 组并给出关键路径「套件先落（W3）→ 同步修复（W1 Class 1）→ 转绿」，W1 Class 2 在 F 组。本文件按 plan 切分组织（brief 要求"严格按 plan §Implementation Slicing 与 W1–W5 生成"），组覆盖完整、依赖有序（blockedBy 编码），W1 的 triage 表骨架仍在 T-Start（T002）提前建立。

## A-3 · closure FAILED 名单的提取形态（FB-04 "or equivalent"）

MP-02 固定命令逐字钉住且不含 `--names-out`；为取名单再做一次全量会违反两槽位纪律。T036 采用：从 T034 closure 运行的 tee 日志提取 FAILED 行（剥离前缀、排序、一行一条，与基线清单同格式）——FB-04 明文认可"or equivalent"，且基线 83 名清单即以同形态产生。若实施期改选在 closure 运行加 `--names-out`，该偏离须先作为 MP-01 的 recorded scope decision 记录，不得静默。

## A-4 · 套件文件名与夹具落点

- 共享参数化镜像套件落 `tests/contract/test_mirror_parity_suite.py`（新文件；本阶段不创建）。
- RC-07 autouse fixture 与模板快照/克隆 fixture 均落 `tests/conftest.py`（plan § Scale/Scope「conftest 一处」；若实施期判定 contract 层 conftest 更合适，属局部可逆纠正，回传披露即可）。

## A-5 · implement 起点槽位的时点

plan §W2 行 8 明文「RC-07 落地后 implement 起点槽位全量运行对比基线」，故 T007（起点槽位）排在 Part A 末尾而非阶段首行；E4 基线 id 清单（T001）按 requirements 定案时点「首个合并任务开工前」先于一切折叠/直调任务。

## A-6 · E1 记录的 〈date〉 写法

任务行内证据文件名用 plan §W5 的 `〈date〉` 占位写法；实施落盘时以实际 ISO 日期命名，非内容占位符。

## A-7 · T033（collect）先于 T034（测量运行）不破坏 MP-03

`--collect-only` 不是一次"运行"且 MP-02 组合在测量前清理缓存，T033 产生的字节码缓存被 T034 的清理步骤移除；T033 与 T034 之间无其他运行，MP-03 的「清理后至测量结束无其他运行」保持成立。

## A-8 · 状态脊 E2 行

T007 / T034 按派发载明的 `SPINE_WRITE_MODE=direct` 与 063 I-05 语义把两个槽位写入状态脊 `<!-- test-budget -->` 围栏（GATE-6 审计输入）；状态脊文件本身由驱动者维护，不随本 part 提交。
