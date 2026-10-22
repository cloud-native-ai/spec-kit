# Verification — 067-loop-efficiency-hardening（implement 期）

**Scope**: implement 期验证记录（Phase 8 · T030–T032，part P13-implement-wrapup 建档）＋ closure 定稿（Phase 9 · T033–T038，part P16-closure-audits 审计与定稿，§10）。
**Authority**: 本文件内容以 `tasks.md` Phase 8/9 任务原文与 `requirements.md` § Success Criteria 为准；本文只转录实测与已记录事实。
**Date**: 2026-10-22 · **Branch**: `067-loop-efficiency-hardening` · **HEAD at verification**: implement 期 `c8e241d7`；closure 定稿 `373f4b32`（P16 产物随本 part 提交落地）。
**Boundary**: 本文件不声称任何测试通过，除非该测试在本周期实际运行且留有 dated 证据；closure 判定（SC-006…SC-010）已在 Phase 9 回填（§7 终态表、§10 定稿）。

## 1. 镜像义务（T030）

本周期触碰的镜像面与方式：

- T023（part E2）以引擎同步 5 pair：`--only agents --only scripts --only shared --only skills/external --only skills/internal`，202 个镜像文件由 `sync-mirrors.py --write` 引擎写出，commit `1d40ebeb`；源侧（`agents/`、`scripts/`、`shared/`、`skills/`）本特性零改动，仅镜像半边（`.specify/` 侧）落盘。
- `scripts/bash/run-tests.sh` pair：预期零改动，实测确认 —— `git diff 7f9033ec..HEAD -- scripts/bash/run-tests.sh .specify/scripts/bash/run-tests.sh` 输出为空。
- `skills/external/sdd-loop-driver/` pair：同样零改动（同法 diff 为空）。
- 本 part 未手改任何镜像；修复一律走引擎。

本 part 实际运行的全仓核对（命令与完整输出）：

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (396 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (109 files)
ok    shared/ == .specify/shared/ (51 files)
exit code: 0
```

判定（plan § Mirror Obligations）：**exit 0，DIFF 计数 = 0**。触碰过的 5 pair 零 drift；全仓 `--check` 相对实施前读数（T023 盘点时 5 pair 漂移、50 条镜像类基线失败）零 NEW drift，且较实施前净回收。

## 2. Review 前置核对（T031）

以下核对均在本 part 实际执行，命令与机械输出如实转录。

### 2.1 任务行状态

- `grep -cE '^- \[[ >]\]' tasks.md`：edit 前 = 9（恰为 T030–T038）；本 part 关闭 T030–T032 后 = **6**（恰为 T033–T038）。GATE-3「grep 为 0」是 Phase 9 closure 时刻的核对点，本阶段按 brief 判据核对：T001–T029 = **29/29 closed**；T033–T038 = 保持 `[ ]`（closure 槽位，review 后执行 —— 设计如此，不是缺口）。
- 记号观察：T013–T018 六行使用小写 `[x]`（其余 23 行为 `[X]`）。两者语义同为 closed（Task State Sigil 规范形式为 `[X]`；GATE-3 的 grep 与 validate-tasks 均判为已闭合）。本 part 允许改动面仅 T030–T032 复选框，故未越权改写这六行，留作 cosmetic 残留观察（见 §9）。

### 2.2 结构校验

```text
$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/067-loop-efficiency-hardening/tasks.md
PASS: .specify/specs/067-loop-efficiency-hardening/tasks.md — 0 error(s), 0 warning(s)
exit code: 0
```

（checkbox 翻转后复跑一次，结果相同：0 error / 0 warning，exit 0。）

### 2.3 证据齐备清单（逐项 `test -e`，10/10 通过）

| # | 文件（`.specify/specs/067-loop-efficiency-hardening/test-evidence/` 下） | 结果 |
|---|---|---|
| 1 | `full-run-2026-10-22-implement-start.md`（E1） | OK |
| 2 | `w2-admission-timing-2026-10-22.md` | OK |
| 3 | `w2-partb-timing-2026-10-22.md` | OK |
| 4 | `w2-telemetry-timing-2026-10-22.md` | OK |
| 5 | `w2-partd-timing-2026-10-22.md` | OK |
| 6 | `w3-sync-2026-10-22.md` | OK |
| 7 | `injection-drill-2026-10-22.md` | OK |
| 8 | `failure-triage-2026-10-22.md` | OK |
| 9 | `test-consolidation-ledger.md` | OK |
| 10 | `pinned-roster-2026-10-22.txt` | OK |

### 2.4 Triage 表核对（V-E5-1 / FB-06）

机械提取 `failure-triage-2026-10-22.md` 表数据行（列锚定解析）：

- **V-E5-1**：数据行 = **83**；唯一 original id = **83**；重复 id = 0。
- class 分布：mirror-sync 53 / stale-pin 11 / regression 5 / pre-existing-debt 14（合计 83）。
- disposition 分布：synced 53 / pin-updated+rationale 10 / mechanism-fixed 5 / **debt-registered 15**（合计 83）。
- **debt 行 dated 记录核对**：15 条 debt-registered 行全部有 dated 记录 —— 14 条 pre-existing-debt 行在行内 evidence 指针直指 `debt-*.md`（`debt-exec-quant-darwin-proc` ×7、`debt-gate-budget-refreeze` ×2、`debt-sc002-cap-breach` ×2、`debt-cd5-heading-collision` / `debt-clause-forms-060-archive` / `debt-shipped-surface-065-feature-refs` 各 ×1）；第 15 条 = `test_i11_channel_two_mirrors_and_per_tool_copies`（class stale-pin），dated 记录经 FB-06 索引行指向 `debt-i11-per-tool-clause-render-2026-10-22.md`。brief 中「14 条」对应 pre-existing-debt 类行数；机械事实为 15 条 debt-registered，逐条均有 dated 记录，无一缺失。
- 7 个 `debt-*.md` 记录文件逐一 grep，均含「非本范围引入」（not introduced / predates scope）陈述，满足 V-E5-2。

### 2.5 台账核对（FB-07 / 无删测试）

机械提取 `test-consolidation-ledger.md` 表数据行：

- 数据行总数 = **81**；disposition = case-merge **35** + retained **46**（41 条常规 + 5 条参数化 id 含转义管道符的行，逐条确认均为 retained）；**deleted = 0**；file-merge = 0。
- 字面 `deleted` 仅出现在文件头部的封闭词表说明文字（第 10–11 行），不在任何数据行。
- 结论：无任何基线测试以删除方式处置（FB-07 台账面成立）。

## 3. implement 期实际运行的测试（T032）

来源 = 状态脊 Dispatch Log（P7–P13 行）与各 dated 证据文件；本表为转录，不新增主张。全程仅经规范运行器 `bash scripts/bash/run-tests.sh` 执行，无裸 `python3 -m pytest`。

| Part | 任务 | 实际运行 | 计数/结果 | 证据指针 |
|---|---|---|---|---|
| P7 | T001 | `run-tests.sh --collect-only -q`（基线 id 清单收集） | 基线 accounted 4551 = 83F+4467P+1S；缓存 nodeids 4553（三数对账见文件头） | `test-evidence/baseline-test-ids.txt` |
| P7 | T003–T005 | admission 家族定向（`tests/unit/test_admission_check.py -q --durations=0`） | red 家族 121.06 s → green 23.03 s；23→25 passed（T005 sibling 参数行） | `rc07-neutralization-2026-10-22.md`、`w2-admission-timing-2026-10-22.md` |
| P7 | T007 | **implement 起点全量槽位**（MP-02 冷缓存；`--names-out` 捕获 in-stage 基线） | wall **534 s**；83 failed / 4469 passed / 1 skipped；exit 1（83 条既有失败）；name diff vs pre-stage = 0 NEW / 0 FIXED | `full-run-2026-10-22-implement-start.md`、`baseline-failures-2026-10-22-implement-start.txt`（83 行） |
| P8 | T008–T012 | Part B 五家族定向复测 ×9 次 | 四家族 RC-07 后已全部落带；零代码改动 | `w2-partb-timing-2026-10-22.md` |
| P9 | T013–T014 | telemetry 家族定向 | 23.36 s → 1.14 s；CLI 子进程冒烟钉住保留 | `w2-telemetry-timing-2026-10-22.md` |
| P9 | T015–T018 | proactive + instructions 家族定向 | 32.70 s → 31.0 s；**超带**（10–12 s），归因 = 生成器子进程成本在禁改 `scripts/` 面（如实记录，未虚报落带） | `w2-partd-timing-2026-10-22.md` |
| P10 | T019–T021 | 镜像套件定向（预期 red：真实漂移） | 202F/521P（漂移期预期形态）；23 个函数折叠入台账 | `w3-part-e1-suite-fold-2026-10-22.md` |
| P11 | T022 | 折叠面定向复测 | 206F/822P（0 NEW，失败全部可定位参数行） | `w3-fold-recheck-2026-10-22.md` |
| P11 | T023–T024 | 套件 + 受修复镜像测试定向 | 同步后套件 0F/723P；合并重跑 9F/1214P（全部在册） | `w3-sync-2026-10-22.md` |
| P12 | T025–T027 | Class 2 逐名 rerun（9 个测试文件） | 19P/14F（14 条 = 已登记负债红，全部 in-register） | `part-f-salvage-2026-10-22.md`、`failure-triage-2026-10-22.md` |
| P12 | T028 | FB-08 注入演练 + FB-09 定位演练（单参数化用例） | 命中 / 定位 / 复现 / 还原四项全中；无注入残留 | `injection-drill-2026-10-22.md` |
| P13 | T030–T032 | 本 part：`sync-mirrors.py --check`、`validate-tasks.py`、表数据行机械审计（见 §1–§2） | 零 pytest 运行 | 本文件 |

## 4. 未运行（如实声明）

- **post 改动后全量运行**：implement 期内未运行 —— closure 槽位（T034）属 Phase 9，review 后、合并前执行；implement 内全量恰一次（T007）。【Phase 9 已执行：T033/T034 由驱动者完成（`e6c3e655`），见 §10】
- T033（post id 清单再生）、T035（覆盖审计）、T036（名称级差集审计）、T037（依赖边界检索）、T038（verification 定稿）：implement 期未运行。【Phase 9 closure 已全部执行，见 §10；P16 审计 part 本身零 pytest 运行，未消耗第三个全量】
- 除上表与 §1–§2 所列命令外，implement 期无其他测试运行被声称。

## 5. Waiver

**waiver = none** —— 本周期没有用户测试豁免；无任何 `waived` 记录，因此不存在「waived 写成 pass」的产物面。T038 定稿时复核：维持 none（closure 亦无测试豁免）。review 的 W-1 是 **判据形态裁定**（钉住名册核对按台账 join 执行，替代字面子集；见 `pinned-roster-addendum-2026-10-22.md`），不是测试豁免，不计入本节；T036 已按该裁定执行（§10.3）。

## 6. SC-001…SC-005（自应用证据，自状态脊 Dispatch Log 如实转录）

turn / token 计数在本周期 dispatch log 全部记 `not_evaluated`（驱动未产出计数器），按要求不编造。

| SC | 状态 | 依据（dispatch log 事实转录） |
|---|---|---|
| SC-001 | partial（事实转录） | 预算耗尽**子派发** = 0：P12 在 120 turn 耗尽，但在同一会话内抢救完成（`550d3b09`），未产生第二次子派发。完成派发数 ≤5 判据：可比数据（065a 同规模 30-task 夹具）不存在 → 该比较面 `not_evaluated`；实际可观察值 = implement 派发 7 个 part（P7–P13）/ 全线 13 part / 38 任务，大于字面 5，规模框架与本特性（38 任务实特性）不同，按 `not_evaluated` 处理不判达标也不判不达标 |
| SC-002 | 满足（按 log 事实） | 13/13 part 均有 part brief（派发载荷）+ 状态脊 Dispatch Log 行；P12 抢救即从 brief + 状态脊恢复下一动作的实例 |
| SC-003 | 满足（按 fence 与证据） | implement 内全量运行 = 1（T007）≤ 063 两槽位预算（状态脊 `<!-- test-budget -->` fence：baseline:1 / closure:0）；各 part 红面有界且可归属（定向集 + 演练/复测 dated 记录，§3 表） |
| SC-004 | 满足 | waiver = none（§5），可检索；无 waived→pass 产物。T038 定稿复核 |
| SC-005 | `not_evaluated` | 驱动往返 / 用户确认次数本周期无计数来源（dispatch log turns 列逐 part `not_evaluated`）；不编造 |

## 7. SC-006…SC-010（Phase 9 closure 终态，T033–T038 回填）

| SC | 终态 | closure 承载 | 证据指针与判定要点 |
|---|---|---|---|
| SC-006 | **满足** | T034（驱动者执行） | `full-run-2026-10-22-closure.md`：MP-02 冷缓存完整运行，wall **553 s ≤ 600 s**（epoch 差，MP-04；pytest 自报 550.62 s 仅交叉核对）；三层全执行、deselected=0（MP-05）；git_commit `00287a38`；达标主张只认此记录（MP-08）。对比：基线 750 s → 553 s（−26.3%） |
| SC-007 | **满足** | T033 + T035 | `coverage-audit-2026-10-22.md`：4551（E4 基线）→ 5239（T033 post 同法再生）；缺失集 = 38（全 contract 层）逐 id 对账台账，**严格 full-id join unmatched = 0**（行 54/76 基-id 形态缺陷经 LED-03 更正行 82–89 修复，过程在审计记录 §3 披露）；缺失集 ⊆ 折叠集；三层计数交叉核对一致（基线 3426/734/391 × E1 closure 4111/736/392，delta 逐层可解释）；post-only 726 = 723 套件参数 + 3 个 LED-08 新测试，报告性列出 |
| SC-008 | **满足** | T036 | `name-diff-2026-10-22.txt` + `name-diff-audit-2026-10-22.md`：对 T007 权威基线（83 名）`comm -13` = **0 NEW**，fixed 69；对 pre-stage 83 名清单同为 0 NEW（两基线集合相同，已验证）；14 余留名 ⊆ T007 基线、恰为 triage 表 14 条 pre-existing-debt（FB-06 dated 记录齐备，i11 已修）；W-1 名册台账 join **302 = 264 post + 38 台账映射 + 0 gap**；triage 83/83 闭环复核；本范围零新增钉住失败；closure 期未顺手修任何 debt 名 |
| SC-009 | **满足** | T028（closure 复核于 T036） | 判据记录 `injection-drill-2026-10-22.md`：注入单行失败 100% 定位到唯一 node id、定向重跑 100% 复现、演练后无残留（命中/定位/复现/还原四项全中）；closure 未新增演练运行——SC-009 判据源 = 该 dated 记录，closure 复核确认表驱动用例语义未被本范围后续改动触碰（折叠仅并字节比对半边，同 id 保留者均留原断言） |
| SC-010 | **满足** | T037 | `dependency-boundary-2026-10-22.md`：`git diff 7f9033ec..HEAD -- pyproject.toml` = **0 字节**（运行时依赖集合零扩大；测试侧新增依赖 = 0，开发组条款空洞成立）；`git diff -- tests/` 全部变更行与新增行的网络 token（urllib/requests/httpx/socket）匹配 = **0** |

不可得项说明：SC-001 比较框架面与 SC-005 维持 `not_evaluated`（§6，closure 未产生新计数来源）。

## 8. 两槽位状态

- **baseline 槽位：已消耗**（T007）。状态脊 `<!-- test-budget -->` fence seq 1：slot=baseline，wall **534 s**（epoch 差），83 failed / 4469 passed / 1 skipped，rc=1，`--names-out` = `baseline-failures-2026-10-22-implement-start.txt`（83 行，closure 名称级差集权威）。E1 全字段：`full-run-2026-10-22-implement-start.md`。
- **closure 槽位：已消耗**（T034，驱动者执行，`e6c3e655`）。fence seq 2：slot=closure，wall **553 s**（epoch 差），14 failed / 5224 passed / 1 skipped，rc=1（14 条既有负债红），`--names-out` = `closure-failures-2026-10-22.txt`（14 行）；名称级差集字段：0 NEW / 69 fixed / 14 known debt。E1 全字段：`full-run-2026-10-22-closure.md`。
- **终态读数（GATE-6 实测复核，§10.5）：`baseline:1 closure:1`，reruns=0，exceptions=0，exit 0。**两槽位纪律闭环：全量运行全程恰两次（T007、T034），无第三跑。

## 9. 残余风险与观察（如实记录，不带出 closure）

1. **proactive + instructions 家族超带**：31.0 s vs 10–12 s 带（P9 记录）；归因 = 生成器子进程成本位于禁改 `scripts/` 面，本范围不可修复；该带差按「超带如实归因」纪律记录，未虚报落带，留待 closure 对照。
2. **14 条负债红仍在失败**：全部 FB-06 dated 登记（§2.4），预期将出现在 T034 closure 运行中，并以 T007 in-stage 83 名清单为差集权威核对（预期 0 NEW）。
3. **T013–T018 记号小写 `[x]`**：与 Sigil 规范形式 `[X]` 不一致（cosmetic）；两个机械权威（GATE-3 grep、validate-tasks）均判已闭合；因允许改动面限制未越权改写。
4. **SC-001 比较框架缺失**：065a 30-task 夹具对照数据不存在，该判据面记 `not_evaluated`（§6）。
5. **P12 预算耗尽**：120 turn 耗尽后同会话抢救，无第二次子派发；耗尽事件本身已记录，属自应用过程事实。

## 10. Closure 定稿（Phase 9 · T033–T038，part P16-closure-audits）

**时点**: 2026-10-22 · HEAD `373f4b32` · review 已完成（`d32cdd70` PASS WITH WAIVER；W-1 裁定 `00287a38`）。
**本 part 运行披露**: 本 part（T035–T038）**零 pytest 运行**；实际执行的命令 = 集合差（`comm`）、`git diff`/`grep` 检索、台账/分类表机械解析（throwaway python，运行一次）、以及下列 GATE 机械命令。closure 全量运行仅 T034 一次（驱动者执行）；**未做第三次全量**（禁令遵守）。T033/T034 产物由驱动者完成于 `e6c3e655`，此处只消费。

### 10.1 Closure 运行结果并入运行记录（T033/T034）

| 项 | 结果 | 证据 |
|---|---|---|
| T033 post id 清单 | 5239 ids（contract 4111 / unit 736 / integration 392），与 T001 同法收集 | `post-test-ids-2026-10-22.txt` |
| T034 closure 全量（MP-02 冷缓存） | wall **553 s** ≤ 600；14F / 5224P / 1S；rc=1（14 条既有负债红） | `full-run-2026-10-22-closure.md`（E1 全字段） |
| 失败名单 | 14 名（排序一行一条） | `closure-failures-2026-10-22.txt` |
| 预算 fence | seq 2 slot=closure；`baseline:1 closure:1` | 状态脊 `<!-- test-budget -->` 围栏（驱动者写入） |

### 10.2 T035 — SC-007 覆盖审计（GATE-2）

`coverage-audit-2026-10-22.md`：4551 → 5239；缺失 38（全 contract 层）全部台账映射，**unmatched = 0**；缺失集恰为折叠 id 集；三层计数交叉核对一致；post-only 726 报告性列出（LED-08）。
**途经修复（披露）**：首次严格 join 报 8 unmatched——台账行 54/76 以基-id 形态记录参数化循环，偏离 E2「full node id」行规则；覆盖本身完好（两行 retained_equivalent 恰好枚举 3+5 个覆盖参数且全部绿色）。按 LED-03「更正即新行」追加行 82–89 修复形态，未改写任何既有行；修复后严格 join = 0。该修复属**纠正**（唯一与已记录意图一致的读法、局部可逆、不证伪下游前提），非裁定。

### 10.3 T036 — SC-008 漂移防护审计（GATE-1 + W-1）

`name-diff-2026-10-22.txt`（由 committed 清单实际 `comm` 输出生成）+ `name-diff-audit-2026-10-22.md`：
- 对 T007 权威基线：`comm -13` = **0 NEW**；fixed 69；14 余留 ⊆ 基线（pre-stage 清单同验 0 NEW，两基线集合恒等）。
- W-1 名册台账 join：302 = 264（post 直存）+ 38（case-merge → 绿色套件参数，含行 58 通配 29/29、行 67 通配 28/28）+ **0 gap**；名册 ⊆ 基线（302/302）。
- triage 83/83 复核（83 行、83 唯一 id，= FB-01 全集）；closure 14 名 == 14 条 pre-existing-debt 行（集合恒等）；debt 名未顺手修。

### 10.4 T037 — SC-010 依赖边界

`dependency-boundary-2026-10-22.md`：`git diff 7f9033ec..HEAD -- pyproject.toml` = 0 字节；测试侧新增依赖 = 0；`git diff 7f9033ec..HEAD -- tests/` 全行与新增行网络 token 匹配 = 0；依赖清单文件（requirements*.txt / setup.* / *.toml / *.cfg）区间零改动。

### 10.5 GATE-1…GATE-7 终审（T038，命令与机械输出如实转录）

| GATE | 判据 | 实测 | 结论 |
|---|---|---|---|
| GATE-1 | `comm -13 <T007 83 名> closure-failures` 为空 | 输出 0 行（pre-stage 清单同验 0 行）；`name-diff-2026-10-22.txt` | **PASS** |
| GATE-2 | LED-05 join unmatched = 0 | 严格 full-id join = 0（LED-03 更正后，见 §10.2）；`coverage-audit-2026-10-22.md` | **PASS** |
| GATE-3 | `grep -cE '^- \[[ >]\]' tasks.md` = 0 | `0` | **PASS** |
| GATE-4 | closure E1 存在且 wall ≤600 或含 RC-04 段 | `test -e` 通过；wall_seconds **553** ≤ 600 | **PASS** |
| GATE-5 | validate-tasks / pre-analyze-check / decomposition-check 退出 0 | `PASS … 0 error(s), 0 warning(s)` exit 0；`decision=pass errors=0 advisories=10`（外部命名空间从句引用，非阻塞）exit 0；`decision=proceed`（fr 21/30，tasks 38/40）exit 0 | **PASS** |
| GATE-6 | audit-test-budget `--stage-check closure` 退出 0 且 `baseline:1 closure:1` | `slots=baseline:1 closure:1 reruns=0 exceptions=0 unknown=0 environment_failures=0`、`stages=6 complete=6`、`status=ok`、exit 0 | **PASS** |
| GATE-7 | 触碰过的镜像对 `--check` 退出 0 且全仓零 NEW drift | 全仓 `sync-mirrors.py --check` exit 0，6 pair 全 ok（0 DIFF），与实施前读数相比零 NEW | **PASS** |

七门全过，无豁免（W-1 为判据形态裁定，非门豁免）。

### 10.6 DoD-1…DoD-7

| DoD | 状态 | 要点 |
|---|---|---|
| DoD-1 全任务闭合 + dated 证据归位 | **满足** | T001–T038 全 `[X]`（GATE-3 grep = 0）；台账/计时/差集/演练/审计记录各在 `test-evidence/` |
| DoD-2 E4 双清单 + unmatched = 0 | **满足** | §10.2 |
| DoD-3 FB-04 差集空 + W-1 join + triage 闭环 | **满足** | §10.3（DoD-3 原文字面子集子句按 W-1 口径复核，`review.md` §4 P1-1） |
| DoD-4 注入/定位演练 + 还原 | **满足** | `injection-drill-2026-10-22.md`（四项全中、无残留）；closure 未再注入 |
| DoD-5 closure E1 + wall ≤600 | **满足** | §10.1（553 s；RC-04 **未触发**） |
| DoD-6 SC-010 三项检索全过 | **满足** | §10.4 |
| DoD-7 本文件记录跑/未跑/waiver/SC 状态/not_evaluated | **满足** | §3–§7、§10（SC-001 比较面、SC-005 = `not_evaluated`；waiver = none + W-1 口径注记） |

### 10.7 RC-04 与残余风险

- **RC-04 未触发**：closure wall 553 s ≤ 600 s，无范围修订/升级记录。
- 残余风险（如实带出合并路径）：
  1. **14 条既有负债红仍失败**（exec-quant ×7、gate-budget-refreeze ×2、sc002-cap ×2、cd5/clause-forms-060/shipped-surface 各 1）——全部 FB-06 dated 登记、非本范围引入、T007 基线子集；closure 按纪律未修。
  2. **proactive + instructions 家族超带**（31.0 s vs 10–12 s）：归因禁改 `scripts/` 面生成器子进程成本；总墙钟已达标（553 s），带差如实记录在案。
  3. **tasks.md `DoD Status: pending` 行未翻转**：该行不属于本 part 允许改动面（仅 T035–T038 复选框），留待驱动者 U6 处置；七门终审（§10.5）即其「implement 闭合后按 GATE-1…GATE-7 复核翻转」的事实依据。
  4. **T013–T018 小写 `[x]`**（cosmetic）：维持 §2.1 观察，两机械权威均判已闭合。
  5. **台账 81 → 89 行**：本 part 追加 8 条 LED-03 更正行（披露于 §10.2）；review 期「81 行」为当时事实读数，非漂移。
