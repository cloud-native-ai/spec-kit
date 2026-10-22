# Analyze Findings — 067-loop-efficiency-hardening (P6-analyze-test-slimming)

**Date**: 2026-10-22 · **Stage**: analyze (P6-analyze-test-slimming) · **Mode**: read-only cross-artifact consistency analysis
**Author**: fresh-context SDD Executor subagent, dispatched by the driver; this agent did not write any artifact under analysis (same-author gate condition not met; no delegation needed).
**Analysis objects**: `requirements.md`、`plan.md`、`tasks.md`、`checklists/test-slimming-2026-10-22.md`、`research.md`、`data-model.md`、`contracts/`（MP/LED/RC/FB ×35 条款）、`quickstart.md`、`test-evidence/` dated records、`notes/` dated records、`.specify/memory/features.md`、`.specify/memory/features/058.md`、`.specify/memory/constitution.md`、063 承载面（`contracts/test-budget.md`、`references/efficiency-model.md`、`review.md`）。
**Boundary**: 除本报告外零文件改动；未运行任何测试；未声称任何测试通过。所有结论可由引用的文件内容或 committed dated 记录复核；报告中标注「已复核」的数字均由本阶段对 committed 工件的机械重算得出（重算命令与结果随条注明）。

## 1 · Method & evidence base

- 逐条核对 21 FR / 10 SC → plan §Requirements Coverage / §W5 → tasks §Requirements Coverage / 任务行 → contracts 条款 → dated 记录的双向可溯性。
- 对四处（requirements FR-012 / clarify 裁决 / contracts MP / plan W4 / tasks T007·T034）的 ≤600s 测量口径、完整运行构成、冷缓存规则、xdist 裁决、基线失败集相对语义做了同义比对。
- 对 committed 基线证据做了机械复核：`notes/baseline-full-2026-10-22.log` 末行 `83 failed, 4467 passed, 1 skipped, 4 warnings in 748.56s`、`FAILED` 行计数 = 83、footer `wall=750s exit=1`；`baseline-failures-2026-10-22.txt` 83 行（80 contract + 3 unit）；mirror/parity/sync/drift/distribution 标记名 = 50；`baseline-durations-2026-10-22.txt` 最慢 50 条合计 **298.20s**（awk 重算）。
- 对任务行引用的 17 个测试 node id 逐一 `grep "def <name>"` 核对存在性（全部命中，含 parametrize 用例 `test_task_count_boundary_edges`）。
- 对 GATE-5/GATE-6 依赖的校验器（`validate-tasks.py`、`pre-analyze-check.py`、`audit-test-budget.py`、`decomposition-check.py`）与运行器（`scripts/bash/run-tests.sh`：`--names-out` 语义、未知参数透传、`# test runner:` 头行）做了源码级核对；以只读方式重跑 `pre-analyze-check --stage tasks`（decision=pass，errors=0，advisories=10，fr=21 sc=10 tasks=38 clauses=35）。
- 063 承载面核对：TB-02「恰两个槽位」、TB-03「首个任务前 + `--names-out`」、TB-04「closure 名称级差集 + final-failed.txt」、TB-07「`--logs-dir` 扫描未入账全量 → 违规」、efficiency-model §E2 围栏唯一台账（:98）。

## 2 · Verified-consistent surfaces（复核通过、未立 finding 的面）

1. **≤600s 口径四处同义**：冷缓存清理范围 / 清理后至运行结束无其他运行 / 至多一次先于清理的 warm-up / 墙钟 = 包装 epoch 差 / 达标主机唯一（requirements.md:159、:234；contracts/measurement.md:20-33；plan.md:113；tasks.md:107、:197）。固定命令逐字钉于 MP-02，plan/tasks 只引用。
2. **完整运行构成五要素闭合**：FR-011（requirements.md:158）↔ MP-05（contracts/measurement.md:25-28）↔ US5 场景 2（:121）↔ clarify 确认（:239）↔ T007/T034 有效性判据（tasks.md:107、:197）。deselected>0 即无效证据；MP-09 禁重试/循环包装；MP-10/RC-05 诊断标记构成中立。未发现「变窄完整运行」的可乘之漏洞：`-k`/`-m`/路径过滤在 MP-02 固定命令构造上不可携带，MP-05 + E1 layer_counts + T035 交叉核对兜底。
3. **基线失败集相对语义一致**：83 名权威（baseline-full-2026-10-22.md、FB-01、E3、requirements.md:237、GATE-1）三处同文；109 条 lastfailed 显式退役（FB-01 "superseded and is not used"）；「不新增名称级失败」判据 + `comm -13` 方向唯一（FB-02/FB-04/GATE-1/T036）。**未发现把基线失败当 green 的表述**：baseline 记录明写 "Not a passing run; do not cite as green"（baseline-full:40）；tasks Notes 红线「本文件不声称任何测试通过」（tasks.md:82）；plan Baseline Facts 标 exit 1（plan.md:24）。
4. **xdist「准入 vs 不采用」两级无冲突**：requirements.md:45/:164 准入政策、R-7/RC-03/plan.md:116/tasks.md:79 不采用决定、FR-017 等价加速分支由 W2 手段合计承载、RC-04 显式升级出口。串行默认 = 唯一测量口径。
5. **FR/SC 承载完整性**：FR-011…FR-021 每条有 plan 设计归属（plan.md:131）+ tasks 任务行承载（tasks.md:21-24，任务 id 全部真实存在）；SC-006…SC-010 逐项有 W5 验证步骤 + 指名任务 + 证据落点（plan.md:120-126）；SC-001…SC-005 证据归属 = 067 自身 dispatch log 转录（T032/T038，不可得记 `not_evaluated`，requirements.md:194-198 的 fallback 措辞一致）。FR-003 引用的 budget 固化提交 `696d5f4b` 存在（`feat(sdd-loop-driver): raise stage subagent budget and bound large stages`）。
6. **防降质四守卫正交且有载体**：构成（FR-011+MP-05）/ 覆盖（FR-015+LED-05/06+GATE-2）/ 漂移（FR-018+FB-03/04+T036+T028 注入演练）/ 定位（FR-020+FB-09+T028+T022 复测），外加 SC-010 依赖边界（T037 三检索，diff 基点划定「新增面」）。台账词表、追加式、date/commit 归因、`deleted` 行必须带等价 id（LED-02/V-E2-3）与 FB-07 禁删失败同向。
7. **CHK012 E2 消歧已闭环**：tasks.md:84 Notes 指涉注记 + T002「data-model §E2」（:93）+ T007/T034「063-E2 槽位行」（:107、:197）+ GATE-6「063 E2 槽位台账唯一来源 = 状态脊围栏」（:46）；`b9d23cc2` 只改 tasks.md（git show --stat 复核）。未发现其它**活的**跨产物符号冲突（E1 双命名空间暴露见 L-8，属预防性注记）。
8. **tasks 结构自洽**：38 任务 / 9 phases，每 part ≤8（2+5+5+2+4+6+5+3+6）；blockedBy 依赖图无环、关键路径「T019 套件 → T023 同步 → T024 转绿」编码正确；全量仅 T007/T034 两槽位；closure 槽位显式「review 后、合并前」（tasks.md:180、:192；plan.md:122）与 063 TB-02/TB-04 语义一致；A-7 裁决保证 T033 collect 不破坏 MP-03 冷缓存。
9. **任务可执行性**：17 个被引测试 node id 全部存在；T004/T013/T019 的 importlib 目标（admission-check.py、trigger-utils.py、sync-mirrors.py 的 `MIRROR_PAIRS`/`compare_pair`）均实测存在；`tests/conftest.py`、`agents/sdd-executor.agent.md` 存在；`audit-test-budget.py --spine/--spec-dir/--stage-check` 与 `decomposition-check.py --mode tasks --requirements --tasks` 旗标与 GATE-5/GATE-6 命令一致。
10. **宪法面**：宪法 v1.13.0 / 16 项与 plan Constitution Check 表一致；IV ⚠ Partial 辩护（交付物=测试组织与测量，等价演练承载 red→green）在 plan Complexity Tracking 与 tasks Tests Mode 两处引用一致（不复制）；XII Tool Reuse（sync 引擎复用、无 Tool 覆盖测量包装）与 IX（零新脚本、inline LED-05）成立。requirements「Status: Draft」与 063/065/066 三个演化规格的现状约定一致（非缺陷）。
11. **基线证据与现状锚点一致**：requirements 现状锚点的 065a 数字（30 任务/60 契约、14/30 done、83 测试 57 passed/26 failed）与 `notes/efficiency-diagnosis-2026-10-22.md` 同文；123.64s 记录在 063 review.md:361 实证；4553=3428+734+391 加法成立；slow-pattern 两口径（234/25/9 vs 110/12/6）披露一致且不进判据分母；外推 65 分钟显式标注「纯外推估计，非测量」且已被实测 750s 取代——honest extrapolation，无违规。

## 3 · Findings — MEDIUM

### M-1 · 067 槽位设计与 063 TB-02/TB-03/TB-04 字面存在三处未调和的分歧（槽位台账缺口）

**严重度**: MEDIUM（披露充分、功能上有更严补偿、GATE-6 机械上会过；但存在「第三个全量运行不入账」的静默超预算分支，须在 T007 执行前以 recorded ruling 关闭。源自 pre-analyze 的 TB-03/TB-04 external-clause advisories 暴露的真实面，按实际严重度报告——非误报升级。）

**事实与依据**（三处分歧，均已由 067 侧 A-3/A-5 部分披露，但未与 063 契约文本对账）：

1. **基线槽位的时点与归属**。063 TB-03（`.specify/specs/063-sdd-loop-efficiency/contracts/test-budget.md:9`）：implement 阶段 MUST 在「执行首个任务前」运行一次全量并写入 E2 台账；TB-02（:8）：每线全量预算「恰好为两个槽位」。067 的实际编排：改动前 750s 全量（FR-012 要求的 baseline dated 记录）发生在 implement 之前、由驱动者执行，**不写入任何槽位台账**；T007（tasks.md:107）在 T003–T006（RC-07 落地 + admission 家族改动）之后才运行并 booking `slot=baseline`。结果：本线全量运行合计 3 次（750s + T007 + T034），fence 只入账 2 次。A-5（notes/tasks-assumptions-2026-10-22.md:32-34）以 plan §W2 行 8 为据披露了「T007 排 Part A 末尾」，但未处理 750s 运行的台账归属，也未处理与 TB-03「首个任务前」字面的冲突。
2. **TB-03 的 `--names-out` 基线捕获被放弃**。TB-03 明文 baseline 槽位使用 `run-tests.sh --names-out <spec-dir>/baseline-failed.txt`；067 的 MP-02 固定命令（contracts/measurement.md:10-19）逐字不含 `--names-out`，T007/T034 均不加。A-3（tasks-assumptions:23-25）只为 closure 侧以 FB-04「or equivalent」路由为日志提取，baseline 侧（T007）则完全不产名单（名称级比较基线改用改动前 83 名清单）。
3. **closure post 侧失败名单不落 committed 工件**。TB-04（:10）要求 closure 用 `--names-out <spec-dir>/final-failed.txt` 留一份名单工件；067 T036（tasks.md:199）从 tee 日志提取（该日志 `*.log` gitignored，baseline-full:18 明示），committed 的只有差集输出 `name-diff-〈date〉.txt` 与审计段落——post 侧 83+ 名清单本身没有强制落档，独立复核 GATE-1 的能力弱于 063 TB-04 的原设计（基线侧有 committed 清单、post 侧没有，证据不对称）。

**加剧因素**：TB-07（:20）的 `--logs-dir` 扫描语义是「日志中出现但台账未入账的全量命中 → 违规」；GATE-6 的调用（tasks.md:46）不传 `--logs-dir`，故基线 750s 日志不会被机械标记——即「静默第三个全量」不会被任何现有 gate 拦截（audit-test-budget.py `--help` 实核：`--logs-dir` 为可选参数）。

**缓解因素**（为何不是 HIGH）：名称级比较基线改用改动前 83 名清单比 TB-04 原义（对 implement 起点名单比较）**更严**——T003–T006 引入的任何新失败都会被 GATE-1 捕获；750s 运行本身是 FR-012/SC-006 的显式需求且处处披露，无隐藏；GATE-6 fence 审计（baseline:1 closure:1）可机械通过。

**修复落点**（implement 派发前由驱动者 recorded ruling，一处即可）：
- 方案 A（推荐）：把改动前 750s 运行 booking 为该线真正的 baseline 槽位（E2 fence 行 slot=baseline，附 `exception_reason` 说明其发生在 implement 派发前、命令为 MP-02 同参形态），T007 改 booking 为 `out-of-slot-exception`（RC-07 全局验证点）或在 TB 语义下记 `in-slot-rerun` 不另开槽；GATE-6 期望值相应调整。
- 方案 B：保留现设计（T007=baseline 槽位），但在 tasks Notes 或 063-E2 fence 注记一行 scope ruling：FR-012 改动前基线测量不占 063 槽位预算（测量非验证），并补 T036 要求把 post FAILED 名单以 committed 工件落 `test-evidence/`（如 `final-failed-〈date〉.txt`），对齐 TB-04 证据形态。
- 无论何案：MUST NOT 静默不改——这是 CHK012 同类的「两个台账语义相邻易错写」面，只是发生在 063↔067 契约边界。

### M-2 · E4 交叉核对锚点 4553 与基线运行 accounted 结果 4551 差 2，且锚点本身无随附计数命令

**严重度**: MEDIUM（V-E4-2 把 4553 定为 T001 的停机判据锚点；锚点与唯一 committed 全量日志之间存在当前无解释的 2 条算术缺口，implement 起点可能出现无法裁决的 ANOMALY 或被迫放行）。

**事实与依据**：
- 锚点 4553 出自驱动者盘点（requirements.md:27「约 4553 条用例…计数命令未随附，待基线日志复核」；notes/test-slimming-scope-2026-10-22.md 表行「driver inventory…counting command not attached; to be cross-checked against the completed baseline log. Sum check: 3428+734+391 = 4553」）。
- 但基线日志**不能**产出该交叉核对：`-q` 模式下 pytest 不打印 `collected N items` 行——对 `notes/baseline-full-2026-10-22.log` 全文 grep `collected` 零命中（本阶段实测）。「待基线日志复核」的义务在 baseline 完成后实际上没有被（也无法被）该日志履行，而 baseline-full-2026-10-22.md:14 已把「Collected node ids: 4553 (contract 3428 / unit 734 / integration 391)」写成基线运行的字段。
- 算术缺口：83 failed + 4467 passed + 1 skipped = **4551** ≠ 4553，差 2；日志内无 `xfailed/xpassed/errors/deselected` 行可解释（grep 实测零命中）。两个数都没有任何工件解释这 2 条（候选读法：(a) 盘点与基线运行之间树上有 2 条测试增删且未记录；(b) 基线运行有 2 条测试未产生结果行且原因未知）。读法 (b) 若为真将动摇基线运行作为 SC-006/SC-008 权威记录的完整性声明，因此不能按「四舍五入」放行。
- V-E4-2（data-model.md:72-74）与 T001（tasks.md:92「行数与基线全量 collected 4553 交叉核对…实质偏差即停并 `ANOMALY:` 上报」）使 4553 成为 implement 起点的硬锚点，但工件未定义当 T001 collect 结果 = 4551（与基线运行 accounted 一致）而 ≠ 4553 时应停止还是记录解释。

**修复落点**：T001 执行时在 E4 文件头同时记录三个数（collect 实测 / 4553 盘点 / 4551 基线 accounted）并写明差异解释；若 T001 collect ≠ 4553，把 4553 标注为「被 collect 实测取代的盘点数」而非停机（V-E4-2 的「material mismatch」应以 T001 同法 collect 与基线日志的 4551 对账为准）。或在下一阶段（PLAN-EDIT/TASKS-EDIT）先修 E4 锚点定义：锚点 = T001 collect 实测，4553/4551 降为历史盘点对照。

### M-3 · Feature 058 注册表联动滞后：067 条目缺测试瘦身范围扩展，Last Updated 头陈旧

**严重度**: MEDIUM（绑定本身已登记且计数/状态正确，无门判据受损；但注册表对 067 实际范围的描述已过时，违反 feature-integration.md § Feature Continuous Evolution 的记录义务，且发生在派发 brief 点名的自查面上）。

**事实与依据**：
- `features/058.md:74` 的 067 条目（「2026-10-22 创建…有界分段派发 + part brief、测试经济学与显式豁免、派发级测量、微缺口合流与驱动往返收敛」）只描述**原始** US1–US4 派发机制范围，未含 2026-10-22 同日的范围扩展（User Story 5 / FR-011…FR-021 / SC-006…SC-010，requirements.md:6、:110-123、:156-168）——扩展后的 requirements 实际范围是注册表描述的超集，未来会话读注册表会低估 067 一半的范围。
- `features/058.md:8` **Last Updated: 2026-10-20**，而文件内已含 2026-10-22 的 067 条目——手工维护注册表的自洽性破缺（AGENTS.md：header 与行须同一趟编辑）。
- `features.md` 索引（058 行，:66）完全无 067 记录（grep "067" 零命中）；该行 dated 历史止于 2026-10-15（连 detail 文件已有的 2026-10-20 063 三条记录也未入索引行），而 064/065 行的先例是把演化记录写入行内最后一列——058 行与自身先例不一致（063 部分为既有状态，067 部分为本特性期间应联动而未联动）。
- **正确未破的面**：`Total Features: 64` 计数不变 ✓（requirements.md:14「不新增 Feature、不改注册表计数」）；058 状态 `Implemented` 不回退 ✓；绑定已在 detail 文件 Related Specifications 登记 ✓。

**修复落点**：`features/058.md` 067 行补一句范围扩展注记（US5 测试瘦身、≤600s、FR-011…FR-021）并刷新 Last Updated；`features.md` 058 行按 064/065 先例补一条 2026-10-22 演化记录（063 缺口可顺带补齐）。注意：tasks Path Conventions 把注册表列为 implement 禁改面，故该修复须由驱动者显式派发（不应由 implement 执行者顺带做），建议挂到 P7-implement 的 T-Start 或收口组。

## 4 · Findings — LOW

### L-1 · admission 家族 red 锚点「≈82.5 s」不能从其引用的 dated 记录复算（实为 87.45 s）
- **文件:行**: plan.md:92（W2 行 1「82.5 → 15–25 s」）；tasks.md:103、:104、:106（T003/T004/T006 的 red「该家族基线 ≈82.5 s」与对照基线）。
- **依据**: 对 `test-evidence/baseline-durations-2026-10-22.txt` awk 重算：`test_admission_check.py` 计 18 条、合计 **87.45 s**；同时最慢 50 条合计 298.20 s（与 plan.md:26 引用一致，说明重算方法无误）。87.45 vs 82.5 差 ~5 s，无任何工件解释该常数来源。
- **影响**: 无 gate 消费 82.5；green 带（15–25 s）不受影响；方向保守（真实 red 更大，节省主张未被夸大）。
- **修复落点**: 下一阶段 PLAN-EDIT/TASKS-EDIT 把 ≈82.5 改为 ≈87.5 或直接引用 baseline-durations 记录（Tests Mode 头已把 dated 记录定为 red 权威，tasks 行内常数应与之一致）。

### L-2 · 达标主机身份字符串跨 dated 记录不一致（OS 26.6.2 vs Darwin 25.6.0）
- **文件:行**: test-evidence/measurement-protocol-2026-10-22.md:78（「macOS arm64 (OS 26.6.2)」）vs test-evidence/baseline-full-2026-10-22.md:8 与 plan.md:41（「Darwin 25.6.0」）；notes/clarify-test-economics-2026-10-22.md:21 亦记 OS 26.6.2。
- **依据**: MP-07（contracts/measurement.md:31-33）把主机身份定为达标判据载体、要求每条记录携带；两套字符串同指一台机器但形态不一致，closure E1 记录照抄任一形态都可能被审计读作「主机不符」。
- **修复落点**: E1 host 字段规则（data-model.md E1）固定为「`uname -m` + `sw_vers` 产品版本 + 解释器/pytest 版本」双形态；协议 §6 在下次触碰该文件时统一。

### L-3 · MP-02 组合使用 bash-only `${PIPESTATUS[0]}`，而 plan 宣称测量包装为 POSIX sh
- **文件:行**: contracts/measurement.md:16（`ST=${PIPESTATUS[0]}`）vs plan.md:37（「测量包装 = POSIX sh」）。
- **依据**: `PIPESTATUS` 为 bash 独有；POSIX sh 下 `ST` 为空，`exit=$ST` 静默失去退出码记录——恰好破坏 E1.exit_code 字段的可判定性。
- **修复落点**: MP-02 注明 wrapper 以 bash 执行（或给 POSIX 等价式）；一处措辞修复。

### L-4 · tasks §Requirements Coverage 两处承载映射与任务行实文不符（映射精度缺陷）
- **文件:行**: tasks.md:22（FR-014 行列「T005 / T016 / T017 / T019–T022」，但 T016/T017（tasks.md:143-144）是快照+克隆夹具接入任务，无表驱动/参数化合并内容）；plan.md:10（Summary 称 50 条镜像失败「可由既有同步引擎确定性修复」，而 W1/FB-05 的真实语义是「可同步对修复、在途对登记负债」，plan.md:81 自身已收窄）。
- **影响**: 纯追溯性/措辞精度；无门判据受影响（FR-014 实际载体 T005/T019–T022 仍充分；W1 细化语义在正文中权威）。
- **修复落点**: 下一阶段 tasks 编辑从 FR-014 行去掉 T016/T017；plan Summary 措辞对齐 W1（或注明简化）。

### L-5 · FR-018 钉住类枚举以「等同类」收尾（开放尾部），与 CHK005「封闭列举」判定相悖
- **文件:行**: requirements.md:165（「…fast-fail 契约等同类」）vs checklists/test-slimming-2026-10-22.md:30-31（CHK005 判「类别封闭列举五类」）。
- **依据**: 「等同类」使名册完备性依赖实现者判断；T002(c)（tasks.md:93）从 `tests/contract/` 盘点能覆盖五类，但第六类钉住可能漏盘。**下界防护仍在**：任何消失 id 必须有台账行（SC-007/LED-05/06），钉住字面量丢失会被 LED-07 核对拦截，故不可能静默降强度。
- **修复落点**: 去掉「等同类」或要求 T002 名册头注记生成正则（使「封闭」成为可复算事实）。

### L-6 · T020–T022 的批切分输入「P-5 清单」在 dated 记录中只是聚合计数 + 正则，不是已持久化的枚举清单
- **文件:行**: tasks.md:156-158（「P-5 盘点 44 个候选按文件路径字典序前 1/3」）vs test-evidence/plan-probes-2026-10-22.md:71-73（P-5 只记「44 test functions matching `byte_identical|…` across ~40 files」，未附清单）。
- **依据**: 切分可复算（同一正则 + 同一 commit 确定性重生成），且 T020 的「逐函数核对后定案」已把候选当候选对待；但「按 P-5 清单三分」的字面读法指向一个不存在的文件，三个批次的文件集未被钉住。
- **修复落点**: T020 首句补「以 P-5 正则在 implement 起点重生成清单（随生成记录落盘）后三分」，或在 T001/T002 阶段把清单落 `test-evidence/`。

### L-7 · checklist 结构自校验记录的 advisory 计数（8 = 7 TB + 1 missing）不能复现（今日实跑 10 = 9 TB + 1 missing）
- **文件:行**: checklists/test-slimming-2026-10-22.md:131 vs 本阶段实跑 `pre-analyze-check --stage tasks`（decision=pass、errors=0、**advisories=10**；TB-03×4 + TB-04×5 于 checklist 行 118/119/122/123/131 + missing-path ×1 于 tasks.md:155）。
- **依据**: checklist 文件与 checker 脚本自 3db048e4 起均无提交（git log 实测），输入未变而记录计数变了——P5 记录的 8 无法由当前输入重现；被标记行内 TB-03/TB-04 实际出现 9 次（sed 计数）。`advisories` 非任何 gate 判据、decision=pass 未变，故仅影响验证记录保真。
- **修复落点**: 按 checklist 自身「原位不刷新、新 dated 清单复核」纪律，在下次 checklist recheck 记录中注记该计数勘误；不改原清单。

### L-8 · E 类符号双命名空间暴露不止 E2 一处（预防性注记，无活冲突）
- **文件:行**: data-model.md:8（E1 = FullRunMeasurement）vs skills/external/sdd-loop-driver/references/efficiency-model.md（063 E1 = 快车道准入记录，TB-07 消费）；tasks.md:107（T007 已带「(data-model.md E1)」限定）vs tasks.md:197-198（T034/T035 裸用「E1」）。
- **依据**: tasks.md 全文未引用 063-E1，故无活冲突（CHK012 的 E2 冲突已由 b9d23cc2 闭环）；但 T034 的裸「E1 全字段」在 implement brief 转写中存在与 CHK012 同类的误写暴露面。
- **修复落点**: 驱动者在 implement part brief 中沿用 T007 式限定（「E1 = data-model §E1」）；或下次 tasks 编辑把 T034 的 E1 补同款限定。E3/E4/E5 无 063 同名冲突。

## 5 · 已知非阻断输入的处置（dispatch brief 点名项）

- **9 条 external TB-03/TB-04 clause advisory**（checklists/test-slimming-2026-10-22.md 行 118/119/122/123/131）：全部是 checklist 对 063 外部命名空间条款的合法交叉引用提示，按 brief 要求未计为 CRITICAL/HIGH。其中 TB-03/TB-04 的引用把我引向 067 槽位设计与 063 契约字面的真实分歧，按实际严重度立为 **M-1**（MEDIUM）——这是本轮唯一由 advisory 暴露的真实覆盖缺口，其余 8 条 advisory 纯提示性、不立 finding。
- **1 条 missing-path advisory**（`tests/contract/test_mirror_parity_suite.py` 尚不存在）：预期形态——该文件由 T019 创建，非覆盖缺口，不立 finding。
- **baseline 83 failed / 750s 现状锚点**：requirements 现状锚点写于基线完成前、显式声明「未作为任何证据读取」且以后台基线为准（requirements.md:31-32），与 committed dated 记录（750s/83，exit 1）衔接一致；未发现任何把基线失败当 green 的表述（§2.3）。

## 6 · 裁决汇总

- **总计 11 项 finding：CRITICAL 0 · HIGH 0 · MEDIUM 3（M-1…M-3）· LOW 8（L-1…L-8）**；每条含文件:行、依据与修复落点。
- **未闭合 CRITICAL/HIGH 数量：0**。无门判据被任何 finding 击穿：≤600s 口径、完整运行构成、相对失败语义、覆盖/漂移/定位三守卫、FR/SC 双向可溯、E2 消歧、两槽位机械审计在受检产物内全部自洽。
- **三项 MEDIUM 均不阻断 analyze**，但各有明确的下一站：M-1 须在 T007 派发前由驱动者 recorded ruling（方案 A 或 B 二选一，MUST NOT 静默维持现状）；M-2 须在 T001 执行时以 E4 头注完成三数对账（或在下一阶段修 E4 锚点定义）；M-3 须由驱动者显式派发一次注册表联动编辑（implement 禁改面，不能由执行者顺带做）。
- **同作者与独立性声明**：本报告作者为派发的 fresh-context 只读分析执行者，未参与任何被分析工件的写作；每条结论均可由所引文件内容或 committed dated 记录独立复核，数字类结论（298.20/87.45/83/4551/50/advisories=10）均经本阶段机械重算，非转写自任何自报。
- **本阶段边界声明**：未修改 requirements/plan/tasks/checklist/tests/scripts/source/mirrors/registry/constitution；未运行任何测试（唯一执行的命令类 = 只读校验器 pre-analyze-check 与 git/grep/awk 静态核对）；新增文件仅本报告。

## VERDICT: GREEN

（未闭合 CRITICAL = 0；未闭合 HIGH = 0；3 MEDIUM / 8 LOW 已逐条给出修复落点，分别在 implement T-Start 前（M-1、M-2）、驱动者派发面（M-3）与后续阶段的例行编辑（L-1…L-8）落地。）
