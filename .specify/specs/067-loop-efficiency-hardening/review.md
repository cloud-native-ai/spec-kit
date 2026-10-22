# Review — 067-loop-efficiency-hardening（P14-review · 独立评审）

**Date**: 2026-10-22 · **Branch**: `067-loop-efficiency-hardening` · **HEAD at review**: `55d52bed` · **Base**: `7f9033ec` · **Phase 8 close**: `8d71082c`
**Reviewer**: fresh-context 评审执行者（非本特性实现者；同作者复核义务由本次独立派发本身满足，objective-analysis-gate 不适用——被审产物非本文作者所写）。
**Inputs**: `.specify/specs/067-loop-efficiency-hardening/{requirements,plan,tasks,verification,data-model,quickstart}.md`、`contracts/`×4、`test-evidence/`×37、`notes/`（含机器本地 `full-run-2026-10-22-implement-start.log`）、git diff `7f9033ec..HEAD`（299 files）。
**Boundary**: 本文是本阶段唯一新建产物；未修改 requirements/plan/tasks/tests/source/scripts/mirrors/registry/verification.md。未运行全量套件（T034 专属 closure 槽位）；未声称任何未运行的测试通过。

## 1 · 范围与方法（实际执行）

### 1.1 实跑的 pytest（全部经规范运行器 `bash scripts/bash/run-tests.sh`，全部定向，零全量）

| # | 命令 | 结果 | 对照 |
|---|---|---|---|
| R1 | `tests/contract/test_mirror_parity_suite.py -q` | **723 passed** / 0 failed（0.98 s） | 与 w3-sync T024 读数一致（0F/723P） |
| R2 | `tests/unit/test_admission_check.py -q` | **25 passed**（21.00 s） | 25 = 23 原始 + 2 sibling 行；21.0 s 落 15–25 s 带（anchor 口径 23.03 s 在带内） |
| R3 | `tests/integration/test_trigger_telemetry.py -q` | **13 passed**（0.94 s） | 13 = 12 retained + 1 CLI 冒烟钉（LED-08）；与 w2-telemetry 1.14 s 同带 |
| R4 | Class 2 全量 33 node id（`class2-set-2026-10-22.txt` 逐条）+ `--names-out` | **19 passed / 14 failed**（8.09 s）；失败名 14 条 | 与 P12 salvage 读数（19P/14F, 7.36 s）一致；14 失败名 == triage 表 class=pre-existing-debt 14 行，集合严格相等 |

### 1.2 镜像与结构核验（非 pytest）

| # | 命令/方法 | 结果 |
|---|---|---|
| M1 | `python3 scripts/python/sync-mirrors.py --check` | exit 0，**0 DIFF**；6 pair ok（templates 22 / skills/external 396 / skills/internal 136 / agents 3 / scripts 109 / shared 51 files）；regen copies ok —— 与 verification.md §1 逐字一致 |
| M2 | `git diff --name-only 7f9033ec..HEAD` 按面分组 | 299 = `.specify/` 镜像 204 + spec-067 产物 53 + `tests/` 42；**src/ 0、pyproject.toml 0、run-tests.sh 0、canonical sources（agents/scripts/skills/shared/templates/docs/memory）0**；registry 触碰 = `features.md` + `features/058.md` 各 1（M-3 演化注记，无计数/状态变化） |
| M3 | 镜像 204 文件逐 pair 归并 | 2（agents）+26（scripts）+37（shared）+62（skills/external）+75（skills/internal）= 202 引擎写出镜像 + 2 registry 文件 —— 与 w3-sync §T023 逐 pair 表完全吻合 |
| M4 | `validate-tasks.py tasks.md` | PASS，0 error / 0 warning（GATE-5 结构面） |
| M5 | `grep -cE '^- \[[ >]\]' tasks.md` | 6（恰为 T033–T038；GATE-3 closure 时点判据，设计如此） |

### 1.3 机械审计（确定性解析，非实跑）

- **台账**（`test-consolidation-ledger.md`）：81 数据行 = case-merge **35** + retained **46**；**deleted = 0**、file-merge = 0；original_id 无重复。
- **diff 函数级勾稽**：`tests/` 内删除的测试函数签名行 46 条 = admission 夹具改写 14 条（retained 行，签名变化重加回）+ case-merge 移除 32 条；27 个折叠函数名 + 5 组重名出现，与台账行 47/64、49/50、53/54/55、56/77 一一对应；**无任何未入账的函数删除**。3 个「byte 半折叠、函数保留」行（71/78/81）签名零 diff，与台账注记一致。
- **等价覆盖存在性**：35 条 case-merge 行的 retained_equivalent_id 逐一对照套件实收参数（suite `--collect-only`，723 params）——33 条单参数引用全部命中，2 条通配子树引用实测 29（git-utils）+ 28（sdd-loop-driver）参数存在。
- **triage 表**（`failure-triage-2026-10-22.md`）：83 数据行、83 唯一 id；class = mirror-sync 53 / stale-pin 11 / regression 5 / pre-existing-debt 14；disposition = synced 53 / pin-updated+rationale 10 / mechanism-fixed 5 / **debt-registered 15**；83 id 集合 == T007 in-stage 83 名 == pre-stage 83 名（三者集合相等，即「0 NEW / 0 FIXED」成立）；15 条 debt-registered 全部指向 dated 记录，7 个 `debt-*.md` 均含 not-introduced 陈述。
- **E1 证据链**：机器本地日志尾行 `83 failed, 4469 passed, 1 skipped, 4 warnings in 532.39s`、`wall=534s exit=1`（epoch 1792654770/1792655304）与 E1 记录逐字段一致；日志 83 条 FAILED 行排序后与 `--names-out` 清单 **diff 为空**。
- **钉住名册**：610 行（含类目节重复），唯一 union = **302 id**（与文件头声明一致）。
- **基线 id 清单**（`baseline-test-ids.txt`）：body 4551 行 = contract 3426 / unit 734 / integration 391；头注三数对账（4551 == 83+4467+1；缓存 4557 vs 记录 4553 差异以 6 条 ghost id 逐条枚举解释并声明 supersede）。

## 2 · 一致性结论

**requirements ↔ plan**：FR-011…FR-021 / SC-006…SC-010 与 W1–W5、MP/LED/RC/FB 35 条款、Implementation Slicing A–G 一一对应；US1–US4 引用性归属（FR-010 owner 面、063 已承载）成立；本周期未发现 requirements 与 plan 间未调和的矛盾（analyze M-1…M-3 已闭环，remediation 记录与 registry diff 实证一致）。

**plan ↔ tasks**：38 任务 / 9 phase（≤8/part）；两槽位纪律成立——状态脊 fence `baseline:1 / closure:0`，implement 内全量恰 T007 一次（E1 + fence + verification §8 三处一致）；xdist 不采用、串行口径保持；禁改面（src/、scripts/ 引擎语义、宿主 git、注册表、requirements/plan）经 M2 证实零触碰。

**tasks ↔ 实现/证据**：29 个 implement 任务闭合且各有 dated 证据；无「删测试消灭失败」（台账 0 deleted + diff 勾稽闭合 + 15 条 debt 行保持红色未声称 green）；无伪绿（verification §4 如实列未跑面；SC-006…SC-010 全部 `pending-closure`；本次 R1–R4 实跑对四类关键主张独立复现）。W2 Part B「零代码改动」主张经 `git diff` 对四家族文件为空直接证实。loop-state 3 条 mechanism-fixed 抽查 diff：均为「import 时刻 NOW → 调用时刻锚定 + 夹具状态重置」，断言主语与强度未动，属真实隔离修复而非弱化。

**镜像义务（GATE-7 面）**：全仓 `--check` 0 DIFF（M1 实测）；202 镜像由引擎写出、源侧零改动（M2/M3）；runner 与 pyproject 在交付区间零 diff（M2），`--names-out` 经运行器源码核对为纯后处理旗标（不改 pytest argv），E1 的 MP-02「逐字 + --names-out」组合披露成立、构成中立。

**证据诚实**：E1 与原始日志逐字段互证（1.3）；注入演练记录（hit/localize/reproduce/restore）与 salvage 记录、triage 分布、当前干净工作树四角一致；w2-partd 超带（31.0 s vs 10–12 s 带）带实测归因如实记录且未声称落带——assumption 被证伪（成本在生成器子进程，禁改 `scripts/` 面），处置符合 tasks Notes「超带如实归因」红线。

## 3 · Findings

**P0（阻塞合并）：0 项。**

### P1-1 · T036/DoD-3「钉住名册 ⊆ post 清单」字面判据与已批准的折叠设计冲突（closure 前必须 recorded ruling 或显式豁免）

- **位置**：`tasks.md:201`（T036「钉住名册（T002）⊆ post id 清单 100%」）、`tasks.md:31`（DoD-3 同判据）；关联 `contracts/failure-baseline.md:11-14`（FB-03）、`contracts/consolidation-ledger.md:31-34`（LED-07）。
- **依据**：钉住名册 union = 302 id；其中 **44 id 属于 34 条 case-merge 台账行**（如 `test_agent_dispatch_mechanism.py::test_c14_mirror_pair_byte_identical`、`test_ask_record_repeat.py::test_doc_exists_with_byte_identical_mirror`），这些函数已在 `54cf98e4`/`3059f4f0` 移除且未重加——T033 post 清单中必然缺失，字面子集检查**机械上不可能通过**。而折叠正是 plan §W3 / FR-014/FR-015 批准的处置：本次评审已实证每条折叠的钉住 FACE 由套件参数承载（35 行等价 id 全部实测存在于 723 参数套件且 R1 全绿；额外断言按 LED-07 留在文件内）。冲突在验收的**机械形态**，不在防护本体。
- **修复落点**（closure 执行前二选一，MUST 记录在 T036 审计记录，不得静默择一）：
  (a) recorded ruling：该检查按 FB-03「100% retained in the complete run」的**防护面语义**执行——每个名册 id 要么出现在 post 清单，要么经台账 case-merge 行映射到存在于 post 清单的套件参数（drift 维度绿色）；本文 §1.3 的 44↔34↔套件参数机械映射即其证据基座。
  (b) closure 期落一份 dated 名册附注（roster addendum）：把 44 条折叠 id 逐一映射到套件参数 id 后，子集检查在映射集上执行。
  review 阶段禁改 tasks.md，故本判据文本无法在本阶段修正；T038 GATE 复核须按上述裁定形态执行并在豁免记录中引用本条。

### P2-1 · closure 交叉核对锚点沿用已废弃的 4553/3428 计数（陈旧数字未随 M-2 处置同步）

- **位置**：`tasks.md:200`（T035「E1 layer_counts 与基线三层计数（contract 3428 / unit 734 / integration 391）交叉核对」）、`plan.md:25`（「collect 4553（contract 3428 / …）」）；源头 `requirements.md:27`（4553 为驱动者盘点数，注明待基线日志复核）。
- **依据**：权威 E4 头注（`baseline-test-ids.txt`）三数对账定案 4551（contract **3426** / unit 734 / integration 391），并明确 4553/缓存 4557 差异由 6 条 ghost id 枚举解释、声明「superseded … for all LED-05 / SC-007 audit purposes」。若 T036 执行者按 tasks.md 字面与 3428 交叉核对 closure E1 的 layer_counts，将得到必假判据（post contract 层计数含折叠移除与 723 套件参数）。
- **修复落点**：T035/T036 执行者以 E4 头注为唯一计数权威并在 `coverage-audit-*.md` 写明口径基座；无需回改 tasks.md（E4 头注已内建 supersede 声明）。登记为改进项：计数类事实的下游引用应指向 E4 而非早期盘点值（One Source Of Truth）。

### P2-2 · 「14 条 known debt」与机械事实 15 条 debt-registered 的口径差（closure 预期须为 15）

- **位置**：`verification.md:144`（§9.2「14 条负债红仍在失败」）；对照 `verification.md:73-74`（机械事实 debt-registered = 15，第 15 条 = `test_i11_channel_two_mirrors_and_per_tool_copies`，class stale-pin）。
- **依据**：本次 R4 实证 14 条 pre-existing-debt 红全部在册；i11 的 mirror 半已同步、残留 per-tool render 钉仍红（w3-sync Residual、T024 合并重跑 9F 在册）。closure 名称级差集的两侧预期应按 **15 条在册红**（14 pre-existing-debt + i11）核对，除非 i11 在 closure 前被钉更新处置。
- **修复落点**：无需改文件（§2.4 已披露口径差）；T036 执行注记写入审计段即可——`comm -13` 两侧各含同 15 名、0 NEW 即 GATE-1 过线。

### P2-3 · Part D 家族带不可达 + 串行恢复算术实际落点高于预估带（如实记录，无在案行动）

- **位置**：`test-evidence/w2-partd-timing-2026-10-22.md`（32.70 → 31.03/31.50 s，vs plan §W2 带 10–12 s）；`plan.md:33`（算术预估 470–520 s）vs T007 实测 534 s（高出上缘 14 s，低于预算 66 s）。
- **依据**：归因经实测证伪 plan 假设（无 copytree 成本可回收；成本 = 13 次生成器子进程 ≈2.4 s/次，位于禁改 `scripts/` 面）；证据页明确「不声称落带」，SC-006 达标只认 T034 closure 槽位（MP-08）。本条为改进观察：未来 spec 候选 = 生成器子进程合并（R-10 同类），067 内无行动项。
- **修复落点**：closure 监视全量墙钟；若 >600 s 走 RC-04 显式升级，禁止静默改口径。

## 4 · Verdict

## **PASS WITH WAIVER**

- **P0 = 0；P1 = 1；P2 = 3。** 交付物（测试重组、镜像同步、triage、台账、证据链）与 requirements/plan/tasks 一致；五类关键主张（套件 723 绿、镜像 0 DIFF、83 名集合全等、Class 2 19P/14F、E1 534 s/83F/4469P/1S）经本次独立实跑复现；覆盖无静默缩水（0 deleted；diff 勾稽闭合；等价覆盖实测存在）；无伪绿、无未跑测试被写成通过。
- **Waiver W-1（对应 P1-1）**：T036/DoD-3 的「钉住名册 ⊆ post 清单 100%」字面判据对 44 条已折叠名册 id 不可能字面成立；按 FB-03 防护面语义豁免字面形态，改以台账 join 的映射集执行（每个名册 id 在 post 清单，或映射到 post 清单内且 drift 维度绿色的套件参数）。豁免理由：FR-018/LED-07 的防护意图经本次评审独立实证保持（等价 id 35/35 实测在套件、套件 723/723 绿、额外断言留档、强度只增不减）；该裁定 MUST 在 T036 审计记录中显式落字并引用本节。
- 其余 P1 级缺口：无。P2 三项不阻塞，均已给出 closure 执行注记。

## 5 · Closure 就绪与 T033–T038 注意点

**就绪结论**：可派发 closure。T033–T038 六行待办定义明确、依赖链（T033→T034→T035/T036/T037→T038）与状态脊 fence（baseline:1/closure:0）一致，无隐藏阻塞；唯一前置动作 = P1-1 的 recorded ruling（落字于 T036 审计记录，属 closure 产物，非本阶段改文件）。

1. **T033**：与 T001 同法收集 post 清单；行数预期 ≈ 4551 −（32 个被移除函数的 id 集）+（3 个已记录 post-only 新 id：2 条 admission sibling + 1 条 telemetry CLI 冒烟）+ 723 条套件参数；偏差解释写进 T035。计数口径以 E4 头注为准（P2-1）。
2. **T034**：这是**首个包含折叠套件与全部 triage 改动的全量运行**（T007 先于 E/F 组落地）；预期墙钟 ≈ T007 ± 方差（折叠收窄收集面）；MP-02 冷缓存逐字组合 + `--names-out` + fence 追加 closure 槽位行（GATE-6 期望终态 `baseline:1 closure:1`）；若 >600 s 走 RC-04，禁止子集/降层。
3. **T035**：LED-05 join 的缺失集应恰为被折叠 id 集，逐 id 对台账（case 行全 id、file 行前缀机械展开）unmatched = 0；layer_counts 交叉核对按 E4 头注 3426/734/391 基座执行并写明（P2-1）；post-only 新增报告性列出（LED-08，至少 3 条在案 + 723 套件参数）。
4. **T036**：名称级差集权威 = T007 in-stage 83 名清单；**预期两侧各含同 15 条在册红**（14 pre-existing-debt + i11；P2-2），0 NEW 即过线——不得在 closure 期「顺手修」debt 名；钉住名册检查按 W-1 裁定形态执行并落字；triage 闭环复核（V-E5-1/2/3 已由 T029 与本次评审双重复核）。
5. **T037**：`git diff 7f9033ec..HEAD -- pyproject.toml` 本评审已实测为空；网络调用检索照 quickstart S7 执行。
6. **T038**：SC-006…SC-010 回填；waiver 面在原 none 之上追加 W-1（T036 判据形态豁免，非测试豁免）；DoD-3 的名册子句按 W-1 口径复核；GATE-3 此时点方要求 grep = 0。

## 6 · 评审边界声明（未跑不声称）

- 未运行：全量套件（T034 槽位）、post collect（T033）、Part B/D 家族复测、w3 合并重跑复现——对应主张采信 committed dated 记录，本评审对其做了内部一致性与交叉勾稽（E1↔日志、triage↔双基线清单、台账↔diff、套件参数↔等价 id），凡在允许面内的主张均已独立复现实测（R1–R4、M1–M5）。
- 本文件不改任何既有产物；ANOMALY：无。

